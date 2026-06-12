"""涨停洗盘策略：昨日涨停后今日放量收阴但不破昨收（Tushare 增强版）。

使用 Tushare 的 limit_list 真实涨停数据替代 price-based 涨停判断，
可区分主板(10%)/创业板科创板(20%)的不同涨停幅度。
"""

import sqlite3
from datetime import date, timedelta

import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy
from sequoia_x.strategy.filters import FundamentalFilter

logger = get_logger(__name__)


class LimitUpShakeoutStrategy(BaseStrategy):
    """涨停洗盘策略（Tushare 增强版）。

    选股条件（向量化，严禁 iterrows）：
    1. 昨日涨停：使用 limit_list 表中的真实涨停数据（区分板块涨停幅度）
    2. 今日收阴：今日 close < 今日 open
    3. 今日放量：今日 volume > 昨日 volume * 2.0
    4. 支撑不破：今日 low >= 昨日 close
    5. 基本面过滤：排除 ST、市值≥10亿

    Attributes:
        webhook_key: 路由到 'shakeout' 专属飞书机器人。
    """

    webhook_key: str = "shakeout"
    name_cn: str = "涨停洗盘"
    _MIN_BARS: int = 3  # 至少需要 3 根 K 线（前日、昨日、今日）

    def _get_limit_up_symbols(self) -> set[str]:
        """从 limit_list 表获取昨日真实涨停的股票列表。"""
        yesterday = (date.today() - timedelta(days=1)).strftime("%Y%m%d")
        try:
            with sqlite3.connect(self.engine.db_path) as conn:
                rows = conn.execute(
                    "SELECT symbol FROM limit_list WHERE date = ? AND limit_type = 'U'",
                    (yesterday,),
                ).fetchall()
            return {r[0] for r in rows}
        except Exception:
            return set()

    def run(self) -> list[str]:
        """遍历全市场，返回满足涨停洗盘条件的股票代码列表。"""
        symbols = self.engine.get_local_symbols()
        selected: list[str] = []

        # 尝试使用 limit_list 获取真实涨停股票
        limit_up_set = self._get_limit_up_symbols() if self.engine.tushare else set()

        for symbol in symbols:
            try:
                df = self.engine.get_ohlcv(symbol)
                if len(df) < self._MIN_BARS:
                    continue

                # 取最近三根 K 线
                prev2 = df.iloc[-3]  # 前日
                prev1 = df.iloc[-2]  # 昨日
                today = df.iloc[-1]  # 今日

                # 条件 1：昨日涨停
                if limit_up_set:
                    # Tushare 模式：使用真实涨停数据
                    limit_up_yesterday = symbol in limit_up_set
                else:
                    # 降级模式：价格比例判断（10% 涨停）
                    limit_up_yesterday = prev1["close"] >= prev2["close"] * 1.095

                if not limit_up_yesterday:
                    continue

                # 条件 2：今日收阴
                bearish_today = today["close"] < today["open"]
                # 条件 3：今日放量
                volume_surge = today["volume"] > prev1["volume"] * 2.0
                # 条件 4：支撑不破
                support_hold = today["low"] >= prev1["close"]

                if bearish_today and volume_surge and support_hold:
                    selected.append(symbol)

            except Exception as exc:
                logger.warning(f"[{symbol}] LimitUpShakeoutStrategy 计算失败：{exc}")
                continue

        # 基本面前置过滤
        if selected and self.engine.tushare:
            f_filter = FundamentalFilter(self.engine)
            selected = f_filter.apply_defaults(selected)

        logger.info(f"LimitUpShakeoutStrategy 选出 {len(selected)} 只股票")
        return selected
