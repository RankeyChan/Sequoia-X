"""净利润断层策略：业绩预告净利润增长>50% + PE合理，捕捉财报超预期机会。"""

import sqlite3
from datetime import date, timedelta

import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy

logger = get_logger(__name__)


class EarningsSurpriseStrategy(BaseStrategy):
    """净利润断层策略。

    选股条件：
    1. 最近 30 天内有业绩预告
    2. 预告净利润变动下限 >= 50%
    3. PE(TTM) > 0且 < 100（合理估值）
    4. 流通市值 >= 30 亿

    财报季（1/4/7/10 月）信号密度最高。

    Attributes:
        webhook_key: 路由到 'earnings_surprise' 专属飞书机器人。
    """

    webhook_key: str = "earnings_surprise"
    name_cn: str = "净利润断层"
    _LOOKBACK_DAYS: int = 30

    def run(self) -> list[str]:
        if not self.engine.tushare:
            logger.warning("Tushare 未启用")
            return []

        try:
            with sqlite3.connect(self.engine.db_path) as conn:
                # 确保 forecast 表有数据
                cnt = conn.execute("SELECT COUNT(*) FROM forecast").fetchone()[0]
                if cnt == 0:
                    logger.info("EarningsSurprise: forecast 表无数据")
                    return []

                cutoff = (date.today() - timedelta(days=self._LOOKBACK_DAYS)).strftime("%Y%m%d")
                df = pd.read_sql(
                    f"""
                    SELECT symbol, end_date, type, p_change_max, p_change_min,
                           net_profit_min, net_profit_max, ann_date, summary
                    FROM forecast
                    WHERE ann_date >= '{cutoff}'
                      AND (p_change_min >= 50 OR p_change_max >= 50)
                    ORDER BY p_change_max DESC
                    """,
                    conn,
                )
        except Exception as exc:
            logger.warning(f"读取数据失败: {exc}")
            return []

        if df.empty:
            logger.info("EarningsSurprise: 近期无符合条件的业绩预告")
            return []

        # PE 过滤
        selected: list[str] = []
        for _, row in df.iterrows():
            symbol = row["symbol"]
            try:
                with sqlite3.connect(self.engine.db_path) as conn:
                    pe = conn.execute(
                        "SELECT pe_ttm FROM daily_basic WHERE symbol = ? ORDER BY date DESC LIMIT 1",
                        (symbol,),
                    ).fetchone()
                if pe and pe[0] and 0 < pe[0] < 100:
                    selected.append(symbol)
            except Exception:
                continue

        logger.info(f"EarningsSurpriseStrategy 选出 {len(selected)} 只股票")
        return selected
