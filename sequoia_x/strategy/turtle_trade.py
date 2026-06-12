"""海龟交易策略：20日新高突破 + 成交额过亿 + 动量阳线过滤 + 基本面筛选。"""

import sqlite3

import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy
from sequoia_x.strategy.filters import FundamentalFilter

logger = get_logger(__name__)


class TurtleTradeStrategy(BaseStrategy):
    """海龟交易策略（A股防诱多改良版 + Tushare 基本面增强）。

    选股条件（向量化，严禁 iterrows）：
    1. 突破新高：今日 close > 前20个交易日 high 的最大值
    2. 流动性：今日 turnover > 100,000,000
    3. 防诱多过滤：今日必须是实体阳线（今日 close > 今日 open），且必须真涨（今日 close > 昨日 close）
    4. 基本面过滤：排除 ST、市值≥10亿、PE 0~300

    Attributes:
        webhook_key: 路由到 'turtle' 专属飞书机器人。
    """

    webhook_key: str = "turtle"
    name_cn: str = "海龟突破"
    _MIN_BARS: int = 21  # 至少需要 21 根 K 线（20日窗口 + 当日）

    def _get_market_caps_from_db(self, symbols: list[str]) -> dict[str, float]:
        """从本地 daily_basic 表查询流通市值。"""
        if not symbols:
            return {}
        placeholders = ",".join("?" * len(symbols))
        try:
            with sqlite3.connect(self.engine.db_path) as conn:
                rows = conn.execute(
                    f"""
                    SELECT symbol, circ_mv FROM daily_basic
                    WHERE symbol IN ({placeholders})
                    AND date = (SELECT MAX(date) FROM daily_basic WHERE symbol = daily_basic.symbol)
                    """,
                    symbols,
                ).fetchall()
            return {r[0]: r[1] or 0 for r in rows}
        except Exception:
            return {}

    def run(self) -> list[str]:
        """遍历全市场，返回满足海龟突破条件的股票代码列表。"""
        symbols = self.engine.get_local_symbols()
        candidates: list[str] = []

        for symbol in symbols:
            try:
                df = self.engine.get_ohlcv(symbol)
                if len(df) < self._MIN_BARS:
                    continue

                # 向量化：前20日 high 的滚动最大值（不含当日，shift(1) 后取 rolling(20)）
                df["high_20"] = df["high"].shift(1).rolling(20).max()

                last = df.iloc[-1]
                prev = df.iloc[-2]  # 获取昨日数据，用于对比

                if pd.isna(last["high_20"]):
                    continue

                # 核心条件 1：突破前 20 天最高点
                breakout = last["close"] > last["high_20"]
                # 核心条件 2：流动性过亿
                liquid = last["turnover"] > 100_000_000
                # 防诱多过滤：实体阳线 + 真涨
                is_yang = last["close"] > last["open"]
                is_up = last["close"] > prev["close"]

                if breakout and liquid and is_yang and is_up:
                    candidates.append(symbol)

            except Exception as exc:
                logger.warning(f"[{symbol}] TurtleTradeStrategy 计算失败：{exc}")
                continue

        # 基本面前置过滤
        if candidates and self.engine.tushare:
            f_filter = FundamentalFilter(self.engine)
            candidates = f_filter.apply_defaults(candidates)

        # 按流通市值从大到小排序（从本地 DB）
        if candidates:
            market_caps = self._get_market_caps_from_db(candidates)
            candidates.sort(key=lambda s: market_caps.get(s, 0), reverse=True)

        logger.info(f"TurtleTradeStrategy 选出 {len(candidates)} 只股票")
        return candidates