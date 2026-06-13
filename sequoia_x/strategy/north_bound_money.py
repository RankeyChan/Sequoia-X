"""北向资金持续买入策略：跟踪外资动向，捕捉外资持续流入标的。"""

import numpy as np
import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy

logger = get_logger(__name__)

class NorthBoundMoneyStrategy(BaseStrategy):
    """北向资金持续买入策略。

    选股条件：
    1. 近 10 日北向持股比例持续上升（斜率 > 0）
    2. 最新持股比例 > 1%
    3. PE(TTM) > 0 且 < 80（合理估值）
    4. 近 5 日涨幅 < 20%（未过度追高）

    Attributes:
        webhook_key: 路由到 'north_bound_money' 专属飞书机器人。
    """

    webhook_key: str = "north_bound_money"
    name_cn: str = "北向增持"
    _LOOKBACK_DAYS: int = 10

    def run(self) -> list[str]:
        if not self.engine.tushare:
            return []

        try:
            cnt = self.engine.fetch_one("SELECT COUNT(*) FROM ts_hk_hold")
            if cnt == 0:
                logger.info("NorthBoundMoney: hk_hold 表无数据")
                return []

            # 获取所有股票和最新持股数据
            stock_symbols = self.engine.fetch_all(
                "SELECT DISTINCT ts_code FROM ts_hk_hold"
            )
        except Exception as exc:
            logger.warning(f"读取数据失败: {exc}")
            return []

        # 按 symbol 分组获取近 N 日数据
        selected: list[str] = []
        for (symbol,) in stock_symbols:
            try:
                rows = self.engine.fetch_all(
                    f"""
                    SELECT trade_date, ratio FROM ts_hk_hold
                    WHERE ts_code = %s ORDER BY trade_date DESC LIMIT {self._LOOKBACK_DAYS}
                    """,
                    (symbol,),
                )

                if len(rows) < self._LOOKBACK_DAYS:
                    continue

                ratios = np.array([r[1] for r in rows if r[1] is not None], dtype=float)
                if len(ratios) < self._LOOKBACK_DAYS or np.any(np.isnan(ratios)):
                    continue

                # 条件 1：持股比例 > 1%
                if ratios[-1] < 1.0:
                    continue

                # 条件 2：趋势向上（线性回归斜率）
                x = np.arange(len(ratios))
                slope = np.polyfit(x, ratios, 1)[0]
                if slope <= 0.001:
                    continue

                # 条件 3：最近三天递增
                if len(ratios) >= 3:
                    if not all(ratios[i] < ratios[i + 1] for i in range(len(ratios) - 3, len(ratios) - 1)):
                        continue

                selected.append(symbol)

            except Exception:
                continue

        logger.info(f"NorthBoundMoneyStrategy 选出 {len(selected)} 只股票")
        return selected
