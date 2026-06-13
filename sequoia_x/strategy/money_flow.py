"""主力资金持续流入策略：跟踪大单资金动向，捕捉主力建仓信号。"""

import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy
from sequoia_x.strategy.filters import FundamentalFilter

logger = get_logger(__name__)

class MoneyFlowStrategy(BaseStrategy):
    """主力资金持续流入策略。

    选股条件：
    1. 近5日主力净流入（超大单+大单）> 0（持续买入）
    2. 近5日散户净流出（小单）> 0（散户割肉）
    3. 今日成交量 > 20日均量 * 1.2（放量确认）
    4. PE > 0 and PE < 100（排除亏损股和高估值）
    5. 流通市值 ≥ 10亿

    Attributes:
        webhook_key: 路由到 'money_flow' 专属飞书机器人。
    """

    webhook_key: str = "money_flow"
    name_cn: str = "主力资金"
    _LOOKBACK_DAYS: int = 5
    _MIN_BARS: int = 25  # 20日均量需要足够历史

    def _get_moneyflow_data(self, symbols: list[str]) -> pd.DataFrame:
        """从 moneyflow 表获取近5日资金流向数据。"""
        if not symbols:
            return pd.DataFrame()
        placeholders = ",".join(["%s"] * len(symbols))
        try:
            df = self.engine.query(
                f"""
                SELECT ts_code, trade_date, buy_elg_amount, sell_elg_amount,
                       buy_lg_amount, sell_lg_amount,
                       buy_sm_amount, sell_sm_amount,
                       net_mf_amount
                FROM ts_moneyflow
                WHERE ts_code IN ({placeholders})
                ORDER BY trade_date DESC
                """,
                params=symbols,
            )
            # 确保数值列为 float（避免 MySQL NULL → Python None → TypeError）
            _num_cols = ["buy_elg_amount", "sell_elg_amount",
                         "buy_lg_amount", "sell_lg_amount",
                         "buy_sm_amount", "sell_sm_amount",
                         "net_mf_amount"]
            for _nc in _num_cols:
                if _nc in df.columns:
                    df[_nc] = pd.to_numeric(df[_nc], errors="coerce")
            return df
        except Exception as exc:
            logger.warning(f"读取 moneyflow 失败: {exc}")
            return pd.DataFrame()

    def run(self) -> list[str]:
        """遍历全市场，返回主力资金持续流入的股票代码列表。"""
        if not self.engine.tushare:
            logger.warning("Tushare 未启用，MoneyFlowStrategy 无法运行")
            return []

        symbols = self.engine.get_local_symbols()
        if not symbols:
            return []

        # 1. 获取数据
        mf_df = self._get_moneyflow_data(symbols)
        if mf_df.empty:
            logger.info("MoneyFlowStrategy: 无资金流向数据")
            return []

        # 2. 按股票分组，计算近5日指标
        selected: list[str] = []

        for symbol in symbols:
            try:
                stock_mf = mf_df[mf_df["ts_code"] == symbol].head(self._LOOKBACK_DAYS)
                if len(stock_mf) < self._LOOKBACK_DAYS:
                    continue

                # 近5日主力净流入 = 超大单 + 大单净买入
                stock_mf["main_net"] = (
                    stock_mf["buy_elg_amount"].fillna(0)
                    + stock_mf["buy_lg_amount"].fillna(0)
                    - stock_mf["sell_elg_amount"].fillna(0)
                    - stock_mf["sell_lg_amount"].fillna(0)
                )
                # 近5日散户净流入 = 小单净买入
                stock_mf["retail_net"] = (
                    stock_mf["buy_sm_amount"].fillna(0)
                    - stock_mf["sell_sm_amount"].fillna(0)
                )

                # 条件 1：近5日主力持续净买入（每天 > 0）
                main_all_positive = (stock_mf["main_net"] > 0).all()
                # 条件 2：近5日散户净流出（每天 < 0）
                retail_all_negative = (stock_mf["retail_net"] < 0).all()
                # 条件 3：总净流入 > 0
                total_net = stock_mf["net_mf_amount"].fillna(0).sum()

                if main_all_positive and retail_all_negative and total_net > 0:
                    # 验证成交量条件
                    df = self.engine.get_ohlcv(symbol)
                    if len(df) < self._MIN_BARS:
                        continue
                    vol_ma20 = df["volume"].iloc[-21:-1].mean()
                    volume_surge = df["volume"].iloc[-1] > vol_ma20 * 1.2

                    if volume_surge:
                        selected.append(symbol)

            except Exception as exc:
                logger.warning(f"[{symbol}] MoneyFlowStrategy 计算失败：{exc}")
                continue

        # 基本面过滤（PE 0~100）
        if selected:
            f_filter = FundamentalFilter(self.engine)
            selected = f_filter.filter_st_stocks(selected)
            selected = f_filter.filter_by_market_cap(selected, min_cap=10e8)
            selected = f_filter.filter_by_pe(selected, max_pe=100, min_pe=0)

        logger.info(f"MoneyFlowStrategy 选出 {len(selected)} 只股票")
        return selected
