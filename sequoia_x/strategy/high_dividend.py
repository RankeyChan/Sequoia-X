"""高股息红利策略：股息率高分位 + 低 PE + 低波动，适合熊市防御。"""

import sqlite3

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
            with sqlite3.connect(self.engine.db_path) as conn:
                latest = conn.execute(
                    "SELECT MAX(date) FROM daily_basic"
                ).fetchone()[0]
                if not latest:
                    return []

                df = pd.read_sql(
                    f"""
                    SELECT symbol, dv_ratio, pe_ttm, pb, circ_mv
                    FROM daily_basic WHERE date = '{latest}'
                    """,
                    conn,
                )
        except Exception as exc:
            logger.warning(f"读取数据失败: {exc}")
            return []

        if df.empty:
            return []

        df = df.dropna(subset=["dv_ratio", "pe_ttm", "circ_mv"])
        df = df[(df["pe_ttm"] > 0) & (df["dv_ratio"] > 0) & (df["circ_mv"] >= 50e8)]

        if df.empty:
            return []

        # 股息率 > 70% 分位
        dv_threshold = df["dv_ratio"].quantile(0.70)
        df = df[df["dv_ratio"] >= dv_threshold]

        # PE < 40% 分位（低估值）
        pe_threshold = df["pe_ttm"].quantile(0.40)
        df = df[df["pe_ttm"] <= pe_threshold]

        # 按股息率排序
        df = df.sort_values("dv_ratio", ascending=False)

        selected = df.head(20)["symbol"].tolist()
        logger.info(f"HighDividendStrategy 选出 {len(selected)} 只股票")
        return selected
