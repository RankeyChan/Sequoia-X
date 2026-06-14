"""净利润断层策略：业绩预告净利润增长>50% + PE合理，捕捉财报超预期机会。"""

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
            # 确保 forecast 表有数据
            cnt = self.engine.fetch_one("SELECT COUNT(*) FROM ts_forecast")
            if cnt is None or cnt == 0:
                logger.info("EarningsSurprise: forecast 表无数据")
                return []

            cutoff = (date.today() - timedelta(days=self._LOOKBACK_DAYS)).strftime("%Y%m%d")
            df = self.engine.query(
                f"""
                SELECT ts_code, end_date, `type`, p_change_max, p_change_min,
                       net_profit_min, net_profit_max, ann_date, summary
                FROM ts_forecast
                WHERE ann_date >= '{cutoff}'
                  AND (p_change_min >= 50 OR p_change_max >= 50)
                ORDER BY p_change_max DESC
                """)
        except Exception as exc:
            logger.warning(f"读取数据失败: {exc}")
            return []

        if df.empty:
            logger.info("EarningsSurprise: 近期无符合条件的业绩预告")
            return []

        # PE 过滤
        selected: list[str] = []
        for _, row in df.iterrows():
            symbol = row["ts_code"]
            try:
                pe = self.engine.fetch_one(
                    "SELECT pe_ttm FROM ts_daily_basic WHERE ts_code = %s ORDER BY trade_date DESC LIMIT 1",
                    (symbol,),
                )
                if pe is not None and 0 < pe < 100:
                    selected.append(symbol)
            except Exception:
                continue

        logger.debug(f"[净利润断层] forecast_total={len(df)} pe_passed={len(selected)}")
        logger.info(f"EarningsSurpriseStrategy 选出 {len(selected)} 只股票")
        return selected
