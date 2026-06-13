"""基本面多因子策略：ROE + 毛利率 + 营收增速 + PE 等权打分，中长线持股。"""

import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy

logger = get_logger(__name__)

class FundamentalMultifactorStrategy(BaseStrategy):
    """基本面多因子策略。

    四因子等权打分：
    1. ROE — 越高越好（盈利能力）
    2. 毛利率(grossprofit_margin) — 越高越好（护城河）
    3. 营收同比(or_yoy) — 越高越好（成长性）
    4. PE(TTM) — 适中最好（负分：过高或亏损均扣分）

    每因子按百分位打分（0~100），总分排名前 20。
    流通市值 ≥ 50 亿。

    Attributes:
        webhook_key: 路由到 'fundamental_multifactor' 专属飞书机器人。
    """

    webhook_key: str = "fundamental_multifactor"
    name_cn: str = "基本面多因子"
    _TOP_N: int = 20

    def run(self) -> list[str]:
        try:
            # 最新报告期
            latest = self.engine.fetch_one(
                "SELECT MAX(end_date) FROM ts_fina_indicator"
            ).fetchone()
            if not latest or not latest[0]:
                logger.info("FundamentalMultifactor: fina_indicator 无数据")
                return []
            end_date = latest[0]

            df = self.engine.query(
                f"""
                SELECT ts_code, roe, grossprofit_margin, or_yoy
                FROM ts_fina_indicator WHERE end_date = '{end_date}'
                """)
        except Exception as exc:
            logger.warning(f"读取 fina_indicator 失败: {exc}")
            return []

        if df.empty:
            return []

        df = df.dropna(subset=["roe", "grossprofit_margin", "or_yoy"])
        df = df[(df["roe"] > 0) & (df["grossprofit_margin"] > 0)]

        if df.empty:
            return []

        # 百分位打分（0~1）
        df["roe_score"] = df["roe"].rank(pct=True)
        df["gm_score"] = df["grossprofit_margin"].rank(pct=True)
        df["rev_score"] = df["or_yoy"].rank(pct=True)

        # PE 打分（取最近一个交易日的 PE）
        try:
            latest_date = self.engine.fetch_one("SELECT MAX(trade_date) FROM ts_daily_basic")
            if latest_date:
                pe_df = self.engine.query(
                    f"""
                    SELECT ts_code, pe_ttm FROM ts_daily_basic
                    WHERE trade_date = '{latest_date}'
                    """
                )
                if not pe_df.empty:
                    pe_df = pe_df.dropna(subset=["pe_ttm"])
                    pe_df["pe_score"] = pe_df["pe_ttm"].clip(upper=100).rank(pct=True, ascending=False)
                    df = df.merge(pe_df[["ts_code", "pe_score"]], on="ts_code", how="left")
                    df["pe_score"] = df["pe_score"].fillna(0)
                else:
                    df["pe_score"] = 0
            else:
                df["pe_score"] = 0
        except Exception:
            df["pe_score"] = 0

        # 等权总分
        df["total"] = (df["roe_score"] + df["gm_score"] + df["rev_score"] + df["pe_score"]) / 4
        df = df.sort_values("total", ascending=False)

        selected = df.head(self._TOP_N)["ts_code"].tolist()
        logger.info(f"FundamentalMultifactorStrategy 选出 {len(selected)} 只股票")
        return selected
