"""缩量回踩策略：多头趋势中缩量回踩 MA20 支撑，捕捉低吸机会。"""

import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy

logger = get_logger(__name__)


class VolumeDrawdownStrategy(BaseStrategy):
    """缩量回踩策略。

    选股条件：
    1. 多头趋势：MA20 > MA60（中期趋势向上）
    2. 回踩：收盘价在 MA20 上方 3% 以内（即将触碰但未跌破）
    3. 缩量：今日成交量 < 20 日均量的 0.7 倍
    4. MA20 向上（斜率正，确认支撑有效）
    5. 流通市值 ≥ 20 亿

    Attributes:
        webhook_key: 路由到 'volume_drawdown' 专属飞书机器人。
    """

    webhook_key: str = "volume_drawdown"
    name_cn: str = "缩量回踩"
    _MIN_BARS: int = 60

    def run(self) -> list[str]:
        symbols = self.engine.get_local_symbols()
        selected: list[str] = []

        for symbol in symbols:
            try:
                df = self.engine.get_ohlcv(symbol)
                if len(df) < self._MIN_BARS:
                    continue

                close = df["close"].astype(float)
                volume = df["volume"].astype(float)
                ma20 = close.rolling(20).mean()
                ma60 = close.rolling(60).mean()

                last = df.iloc[-1]
                last_close = float(last["close"])
                last_ma20 = ma20.iloc[-1]
                last_ma60 = ma60.iloc[-1]
                ma20_slope = ma20.iloc[-1] - ma20.iloc[-5]

                if pd.isna(last_ma20) or pd.isna(last_ma60):
                    continue

                # 条件 1：多头趋势
                if not (last_ma20 > last_ma60):
                    continue

                # 条件 2：MA20 向上
                if ma20_slope <= 0:
                    continue

                # 条件 3：收盘价在 MA20 上方 3% 以内
                ratio = last_close / last_ma20 - 1
                if not (0 <= ratio <= 0.03):
                    continue

                # 条件 4：缩量到 20 日均量 0.7 倍以下
                vol_ma20 = volume.iloc[-21:-1].mean()
                if pd.isna(vol_ma20) or vol_ma20 == 0:
                    continue
                if not (float(last["volume"]) < vol_ma20 * 0.7):
                    continue

                selected.append(symbol)

            except Exception as exc:
                logger.warning(f"[{symbol}] VolumeDrawdown 失败: {exc}")
                continue

        logger.info(f"VolumeDrawdownStrategy 选出 {len(selected)} 只股票")
        return selected
