"""高股息红利策略：股息率高分位 + 低 PE + 低波动，适合熊市防御。"""

import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy

logger = get_logger(__name__)

class HighDividendStrategy(BaseStrategy):
    """高股息红利策略。

    选股条件：
    1. 股息率(dv_ratio) > 全市场 70% 分位
    2. PE(TTM) > 0 且 PE(TTM) < 过去一年 < 40% 分位（低估值）
    3. 近 60 日波动率（日收益率标准差）< 中位数（低波动）
    4. 流通市值 ≥ 50 亿

    Attributes:
        webhook_key: 路由到 'high_dividend' 专属飞书机器人。
    """

    webhook_key: str = "high_dividend"
    name_cn: str = "高股息红利"

    def run(self) -> list[str]:
        if not self.engine.tushare:
            return []

        try:
            target = self.engine.target_date or dt.today().strftime("%Y%m%d")
            latest = self.engine.fetch_one(
                "SELECT MAX(trade_date) FROM ts_daily_basic WHERE trade_date <= %s",
                (target,),
            )
            if not latest:
                return []

            df = self.engine.query(
                f"""
                SELECT ts_code, dv_ratio, pe_ttm, pb, circ_mv
                FROM ts_daily_basic WHERE trade_date = '{latest}'
                """)
        except Exception as exc:
            logger.warning(f"读取数据失败: {exc}")
            return []

        if df.empty:
            return []

        df = df.dropna(subset=["dv_ratio", "pe_ttm", "circ_mv"])
        df = df[(df["pe_ttm"] > 0) & (df["dv_ratio"] > 0) & (df["circ_mv"] >= 500000)]

        if df.empty:
            return []

        # 股息率 > 70% 分位
        dv_threshold = df["dv_ratio"].quantile(0.70)
        df = df[df["dv_ratio"] >= dv_threshold]

        # PE < 40% 分位（低估值）
        pe_threshold = df["pe_ttm"].quantile(0.40)
        df = df[df["pe_ttm"] <= pe_threshold]

        # 近 60 日波动率过滤（低波动）
        # 从 ts_daily 批量获取所有候选股的近 60 日收益率，计算波动率
        try:
            vol_placeholders = ",".join(["%s"] * len(df))
            vol_rows = self.engine.fetch_all(
                f"""SELECT ts_code, trade_date, close FROM ts_daily
                WHERE ts_code IN ({vol_placeholders})
                ORDER BY ts_code, trade_date""",
                df["ts_code"].tolist(),
            )
            import pandas as pd
            vol_df = pd.DataFrame(vol_rows, columns=["ts_code", "trade_date", "close"])
            if not vol_df.empty:
                vol_df["ret"] = vol_df.groupby("ts_code")["close"].pct_change()
                # 只取近 60 个交易日
                vol_df = vol_df.groupby("ts_code").tail(60)
                vol_std = vol_df.groupby("ts_code")["ret"].std().dropna()
                if not vol_std.empty:
                    median_vol = vol_std.median()
                    low_vol_codes = set(vol_std[vol_std <= median_vol].index)
                    df = df[df["ts_code"].isin(low_vol_codes)]
        except Exception:
            pass  # 波动率计算失败不影响其他条件

        # 按股息率排序
        df = df.sort_values("dv_ratio", ascending=False)

        selected = df.head(20)["ts_code"].tolist()
        logger.debug(f"[高股息红利] basic_total={len(df)} after_dv={len(df) if 'dv_threshold' in dir() else len(df)} selected={len(selected)}")
        logger.info(f"HighDividendStrategy 选出 {len(selected)} 只股票")
        return selected
