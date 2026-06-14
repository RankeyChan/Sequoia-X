"""PE-ROE 价值选股策略：PE最低20% + ROE最高30% + PB最低30% 综合评分。"""

import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy

logger = get_logger(__name__)

class PeRoeValueStrategy(BaseStrategy):
    """PE-ROE 价值选股策略。

    选股条件：
    1. PE(TTM) 最低 30% 分位（排除亏损股 PE > 0）
    2. ROE 最高 30% 分位
    3. PB 最低 30% 分位
    4. 三因子等权打分，选综合排名前 20
    5. 流通市值 ≥ 50 亿

    Attributes:
        webhook_key: 路由到 'pe_roe' 专属飞书机器人。
    """

    webhook_key: str = "pe_roe"
    name_cn: str = "PE-ROE价值"
    _PERCENTILE: float = 0.30

    def run(self) -> list[str]:
        if not self.engine.tushare:
            logger.warning("Tushare 未启用")
            return []

        try:
            # 获取最新交易日数据
            target = self.engine.target_date or dt.today().strftime("%Y%m%d")
            latest = self.engine.fetch_one(
                "SELECT MAX(trade_date) FROM ts_daily_basic WHERE trade_date <= %s",
                (target,),
            )
            if not latest:
                return []

            df = self.engine.query(
                f"""
                SELECT ts_code, pe_ttm, pb, circ_mv
                FROM ts_daily_basic WHERE trade_date = '{latest}'
                """)
        except Exception as exc:
            logger.warning(f"读取数据失败: {exc}")
            return []

        if df.empty:
            return []

        # 过滤
        df = df.dropna(subset=["pe_ttm", "pb"])
        df = df[(df["pe_ttm"] > 0) & (df["pb"] > 0)]
        df = df[df["circ_mv"] >= 500000]

        if df.empty:
            return []

        # PE 越低分越高（百分位反转，连续打分 0~1）
        df["pe_score"] = 1 - df["pe_ttm"].rank(pct=True)

        # PB 越低分越高（百分位反转，连续打分 0~1）
        df["pb_score"] = 1 - df["pb"].rank(pct=True)

        # ROE 从 fina_indicator 获取
        try:
            latest_roe = self.engine.fetch_one(
                "SELECT MAX(end_date) FROM ts_fina_indicator WHERE end_date <= %s",
                (target,),
            )
            if latest_roe:
                roe_df = self.engine.query(
                    f"""
                    SELECT ts_code, roe FROM ts_fina_indicator
                    WHERE end_date = '{latest_roe}'
                    """)
                roe_df = roe_df.dropna(subset=["roe"])
                if not roe_df.empty:
                    roe_df["roe_score"] = roe_df["roe"].rank(pct=True)
                    df = df.merge(roe_df[["ts_code", "roe_score"]], on="ts_code", how="left")
                    df["roe_score"] = df["roe_score"].fillna(0)
                else:
                    df["roe_score"] = 0
            else:
                df["roe_score"] = 0
        except Exception:
            df["roe_score"] = 0

        # 综合评分（三因子等权平均）
        df["total_score"] = (df["pe_score"] + df["pb_score"] + df["roe_score"]) / 3
        df = df.sort_values("total_score", ascending=False)

        selected = df.head(20)["ts_code"].tolist()
        logger.debug(f"[PE-ROE价值] basic_total={len(df)} with_roe={len(df) if 'roe_score' in df.columns else 'N/A'} selected={len(selected)}")
        logger.info(f"PeRoeValueStrategy 选出 {len(selected)} 只股票")
        return selected
