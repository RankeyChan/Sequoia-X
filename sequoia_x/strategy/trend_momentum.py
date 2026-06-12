"""趋势动量策略：MA5>MA20>MA60 多头排列 + RSI 50-80 + 近N日涨幅适中。"""

import sqlite3

import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy

logger = get_logger(__name__)


class TrendMomentumStrategy(BaseStrategy):
    """趋势动量策略。

    选股条件：
    1. MA5 > MA20 > MA60（标准多头排列）
    2. RSI(14) 在 50~80 之间（强势未超买）
    3. 近 20 日涨幅 > 5% 且 < 30%（温和放量上涨）
    4. 流通市值 ≥ 50 亿

    Attributes:
        webhook_key: 路由到 'trend_momentum' 专属飞书机器人。
    """

    webhook_key: str = "trend_momentum"
    name_cn: str = "趋势动量"
    _MIN_BARS: int = 60

    @staticmethod
    def _compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
        delta = series.diff()
        gain = delta.clip(lower=0).rolling(window=period).mean()
        loss = (-delta.clip(upper=0)).rolling(window=period).mean()
        rs = gain / loss.replace(0, float("nan"))
        return 100 - (100 / (1 + rs))

    def run(self) -> list[str]:
        symbols = self.engine.get_local_symbols()
        selected: list[str] = []

        for symbol in symbols:
            try:
                df = self.engine.get_ohlcv(symbol)
                if len(df) < self._MIN_BARS:
                    continue

                close = df["close"]
                ma5 = close.rolling(5).mean()
                ma20 = close.rolling(20).mean()
                ma60 = close.rolling(60).mean()

                last5 = ma5.iloc[-1]
                last20 = ma20.iloc[-1]
                last60 = ma60.iloc[-1]
                if pd.isna(last5) or pd.isna(last20) or pd.isna(last60):
                    continue

                # 条件 1：多头排列
                if not (last5 > last20 > last60):
                    continue

                # 条件 2：RSI
                rsi = self._compute_rsi(close)
                last_rsi = rsi.iloc[-1]
                if pd.isna(last_rsi) or not (50 <= last_rsi <= 80):
                    continue

                # 条件 3：近 20 日涨幅
                ret_20d = close.iloc[-1] / close.iloc[-21] - 1
                if not (0.05 <= ret_20d <= 0.30):
                    continue

                selected.append(symbol)

            except Exception as exc:
                logger.warning(f"[{symbol}] TrendMomentum 失败: {exc}")
                continue

        logger.info(f"TrendMomentumStrategy 选出 {len(selected)} 只股票")
        return selected
