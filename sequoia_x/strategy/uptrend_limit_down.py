"""上升趋势跌停策略：趋势中放量跌停，捕捉错杀机会。"""

import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy
from sequoia_x.strategy.filters import FundamentalFilter

logger = get_logger(__name__)


class UptrendLimitDownStrategy(BaseStrategy):
    """上升趋势跌停策略。

    选股条件（向量化，严禁 iterrows）：
    1. 处于上升趋势：昨日20日均线 > 昨日60日均线
    2. 放量跌停：今日 close <= 昨日 close * 0.905
                且今日 volume > 20日均量的 2.0 倍

    Attributes:
        webhook_key: 路由到 'limit_down' 专属飞书机器人。
    """

    webhook_key: str = "limit_down"
    name_cn: str = "上升跌停"
    _MIN_BARS: int = 60  # 至少需要 60 根 K 线（60日均线）

    def run(self) -> list[str]:
        """
        遍历全市场，返回满足上升趋势跌停条件的股票代码列表。

        Returns:
            满足条件的股票代码列表。
        """
        symbols = self.engine.get_local_symbols()
        selected: list[str] = []
        _dbg = {"insufficient": 0, "no_uptrend": 0, "no_limit": 0, "no_volume": 0, "fundamental": 0}

        for symbol in symbols:
            try:
                df = self.engine.get_ohlcv(symbol)
                if len(df) < self._MIN_BARS:
                    _dbg["insufficient"] += 1
                    continue

                # 向量化计算均线
                df["ma20"] = df["close"].rolling(20).mean()
                df["ma60"] = df["close"].rolling(60).mean()
                df["vol_ma20"] = df["volume"].shift(1).rolling(20).mean()

                prev = df.iloc[-2]  # 昨日
                today = df.iloc[-1]  # 今日

                if pd.isna(prev["ma20"]) or pd.isna(prev["ma60"]) or pd.isna(today["vol_ma20"]):
                    continue

                # 条件 1：上升趋势（昨日均线多头排列）
                uptrend = prev["ma20"] > prev["ma60"]
                # 条件 2：放量跌停
                limit_down = today["close"] <= prev["close"] * 0.905
                volume_surge = today["volume"] > today["vol_ma20"] * 2.0

                if uptrend and limit_down and volume_surge:
                    selected.append(symbol)
                else:
                    if not uptrend:
                        _dbg["no_uptrend"] += 1
                    if not limit_down:
                        _dbg["no_limit"] += 1
                    if not volume_surge:
                        _dbg["no_volume"] += 1

            except Exception as exc:
                logger.warning(f"[{symbol}] UptrendLimitDownStrategy 计算失败：{exc}")
                continue

        # 基本面前置过滤
        if selected and self.engine.tushare:
            f_filter = FundamentalFilter(self.engine)
            before = len(selected)
            selected = f_filter.apply_defaults(selected)
            _dbg["fundamental"] = before - len(selected)

        logger.debug(f"[上升跌停] total={len(symbols)} insufficient={_dbg['insufficient']} no_uptrend={_dbg['no_uptrend']} no_limit={_dbg['no_limit']} no_volume={_dbg['no_volume']} fundamental_dropped={_dbg['fundamental']} selected={len(selected)}")
        logger.info(f"UptrendLimitDownStrategy 选出 {len(selected)} 只股票")
        return selected
