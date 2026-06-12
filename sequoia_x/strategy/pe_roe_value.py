"""PE-ROE 价值选股策略：PE最低20% + ROE最高30% + PB最低30% 综合评分。"""

import sqlite3

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
            with sqlite3.connect(self.engine.db_path) as conn:
                # 获取最新交易日数据
                latest = conn.execute(
                    "SELECT MAX(date) FROM daily_basic"
                ).fetchone()[0]
                if not latest:
                    return []

                df = pd.read_sql(
                    f"""
                    SELECT symbol, pe_ttm, pb, circ_mv
                    FROM daily_basic WHERE date = '{latest}'
                    """,
                    conn,
                )
        except Exception as exc:
            logger.warning(f"读取数据失败: {exc}")
            return []

        if df.empty:
            return []

        # 过滤
        df = df.dropna(subset=["pe_ttm", "pb"])
        df = df[(df["pe_ttm"] > 0) & (df["pb"] > 0)]
        df = df[df["circ_mv"] >= 50e8]

        if df.empty:
            return []

        # PE 最低 30%
        pe_threshold = df["pe_ttm"].quantile(self._PERCENTILE)
        df["pe_score"] = (df["pe_ttm"] <= pe_threshold).astype(int)

        # PB 最低 30%
        pb_threshold = df["pb"].quantile(self._PERCENTILE)
        df["pb_score"] = (df["pb"] <= pb_threshold).astype(int)

        # ROE 从 fina_indicator 获取
        try:
            conn = sqlite3.connect(self.engine.db_path)
            latest_roe = conn.execute(
                "SELECT MAX(end_date) FROM fina_indicator"
            ).fetchone()[0]
            if latest_roe:
                roe_df = pd.read_sql(
                    f"""
                    SELECT symbol, roe FROM fina_indicator
                    WHERE end_date = '{latest_roe}'
                    """,
                    conn,
                )
                roe_df = roe_df.dropna(subset=["roe"])
                if not roe_df.empty:
                    roe_top = roe_df["roe"].quantile(1 - self._PERCENTILE)
                    roe_df["roe_score"] = (roe_df["roe"] >= roe_top).astype(int)
                    df = df.merge(roe_df[["symbol", "roe_score"]], on="symbol", how="left")
                    df["roe_score"] = df["roe_score"].fillna(0)
                else:
                    df["roe_score"] = 0
            else:
                df["roe_score"] = 0
        except Exception:
            df["roe_score"] = 0

        # 综合评分
        df["total_score"] = df["pe_score"] + df["pb_score"] + df["roe_score"]
        df = df.sort_values("total_score", ascending=False)

        selected = df.head(20)["symbol"].tolist()
        logger.info(f"PeRoeValueStrategy 选出 {len(selected)} 只股票")
        return selected
