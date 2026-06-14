"""北向资金持续增持策略：跟踪外资（北向资金）持股变化，捕捉外资青睐个股。"""

import numpy as np
import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy
from sequoia_x.strategy.filters import FundamentalFilter

logger = get_logger(__name__)

class NorthBoundStrategy(BaseStrategy):
    """北向资金持续增持策略。

    选股条件：
    1. 近10个交易日北向持股比例持续上升（线性回归斜率 > 0.001）
    2. 最新持股比例 > 1%（非偶然持股）
    3. 最近一天持股比例增幅 > 前10天日均增幅
    4. 流通市值 > 50亿（大盘股更受外资青睐）

    Attributes:
        webhook_key: 路由到 'north_bound' 专属飞书机器人。
    """

    webhook_key: str = "north_bound"
    name_cn: str = "北向资金"
    _LOOKBACK_DAYS: int = 10
    _MIN_RATIO: float = 1.0  # 最低持股比例 1%
    _SLOPE_THRESHOLD: float = 0.001  # 斜率阈值

    def _get_hk_hold_data(self, symbols: list[str]) -> pd.DataFrame:
        """从 hk_hold 表获取近10日北向资金持股数据。"""
        if not symbols:
            return pd.DataFrame()
        placeholders = ",".join(["%s"] * len(symbols))
        try:
            df = self.engine.query(
                f"""
                SELECT ts_code, trade_date, ratio
                FROM ts_hk_hold
                WHERE ts_code IN ({placeholders})
                ORDER BY trade_date ASC
                """,
                params=symbols,
            )
            return df
        except Exception as exc:
            logger.warning(f"读取 hk_hold 失败: {exc}")
            return pd.DataFrame()

    def run(self) -> list[str]:
        """遍历全市场，返回北向资金持续增持的股票代码列表。"""
        if not self.engine.tushare:
            logger.warning("Tushare 未启用，NorthBoundStrategy 无法运行")
            return []

        symbols = self.engine.get_local_symbols()
        if not symbols:
            return []

        # 1. 获取数据
        hk_df = self._get_hk_hold_data(symbols)
        if hk_df.empty:
            logger.info("NorthBoundStrategy: 无北向资金数据")
            return []

        # 过滤出有连续数据的股票
        symbol_counts = hk_df.groupby("ts_code").size()
        valid_symbols = symbol_counts[symbol_counts >= self._LOOKBACK_DAYS].index.tolist()

        selected: list[str] = []

        for symbol in valid_symbols:
            try:
                stock_data = hk_df[hk_df["ts_code"] == symbol].tail(self._LOOKBACK_DAYS)
                if len(stock_data) < self._LOOKBACK_DAYS:
                    continue

                ratios = stock_data["ratio"].values
                if np.any(np.isnan(ratios)):
                    continue

                # 条件 1：最新持股比例 > 1%
                if ratios[-1] < self._MIN_RATIO:
                    continue

                # 条件 2：持股比例趋势向上（线性回归斜率 > 0）
                x = np.arange(len(ratios))
                slope = np.polyfit(x, ratios, 1)[0]
                if slope <= self._SLOPE_THRESHOLD:
                    continue

                # 条件 3：最近一天增幅 > 前10天日均增幅
                recent_change = ratios[-1] - ratios[-2] if len(ratios) >= 2 else 0
                avg_change = (ratios[-1] - ratios[0]) / len(ratios)
                if recent_change <= avg_change:
                    continue

                # 条件 4：最近三天持股比例严格递增
                if len(ratios) >= 3:
                    recent_3 = ratios[-3:]
                    if not all(recent_3[i] < recent_3[i + 1] for i in range(len(recent_3) - 1)):
                        continue

                selected.append(symbol)

            except Exception as exc:
                logger.warning(f"[{symbol}] NorthBoundStrategy 计算失败：{exc}")
                continue

        # 基本面过滤（大盘股）
        if selected:
            f_filter = FundamentalFilter(self.engine)
            selected = f_filter.filter_st_stocks(selected)
            selected = f_filter.filter_by_market_cap(selected, min_cap_wan=500000)

        logger.debug(f"[北向资金] total={len(symbols)} valid={len(valid_symbols) if 'valid_symbols' in dir() else len(symbols)} no_ratio={None} no_slope={None} before_filter={len(selected)}")
        logger.info(f"NorthBoundStrategy 选出 {len(selected)} 只股票")
        return selected
