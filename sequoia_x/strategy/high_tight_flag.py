"""高旗形整理策略：强动量后极度收敛缩量。"""

import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy
from sequoia_x.strategy.filters import FundamentalFilter

logger = get_logger(__name__)


class HighTightFlagStrategy(BaseStrategy):
    """高旗形整理策略。

    选股条件（向量化，严禁 iterrows）：
    1. 强动量：过去40天区间最高价 / 区间最低价 > 1.6（涨幅超60%）
    2. 极度收敛：最近10天区间最高价 / 区间最低价 < 1.15（振幅低于15%）
    3. 缩量：今日 volume < 过去20日 volume 均值的 0.6 倍

    Attributes:
        webhook_key: 路由到 'flag' 专属飞书机器人。
    """

    webhook_key: str = "flag"
    name_cn: str = "高窄旗形"
    _MIN_BARS: int = 40  # 至少需要 40 根 K 线

    def run(self) -> list[str]:
        """
        遍历全市场，返回满足高旗形整理条件的股票代码列表。

        Returns:
            满足条件的股票代码列表。
        """
        symbols = self.engine.get_local_symbols()
        selected: list[str] = []
        _dbg = {"insufficient": 0, "no_momentum": 0, "no_consolidation": 0, "no_level": 0, "no_shrink": 0, "fundamental": 0}

        for symbol in symbols:
            try:
                df = self.engine.get_ohlcv(symbol)
                if len(df) < self._MIN_BARS:
                    _dbg["insufficient"] += 1
                    continue

                # 向量化计算各窗口指标
                tail40 = df.tail(40)
                tail10 = df.tail(10)

                high40 = tail40["high"].max()
                low40 = tail40["low"].min()
                high10 = tail10["high"].max()
                low10 = tail10["low"].min()

                if low40 == 0 or low10 == 0:
                    continue

                # 条件 1：强动量
                momentum = high40 / low40 > 1.6
                # 条件 2：极度收敛
                consolidation = high10 / low10 < 1.15
                # 条件 3：高位抗跌（近10天最低点不得低于40天最高点的80%）
                high_level = low10 >= high40 * 0.8
                # 条件 4：缩量（向量化均值）
                recent_vol = df["volume"].iloc[-21:-1].dropna()
                if len(recent_vol) < 10:
                    _dbg["no_shrink"] += 1
                    continue
                vol_ma20 = recent_vol.mean()
                shrink = df["volume"].iloc[-1] < vol_ma20 * 0.6

                if momentum and consolidation and high_level and shrink:
                    selected.append(symbol)
                else:
                    if not momentum: _dbg["no_momentum"] += 1
                    if not consolidation: _dbg["no_consolidation"] += 1
                    if not high_level: _dbg["no_level"] += 1
                    if not shrink: _dbg["no_shrink"] += 1

            except Exception as exc:
                logger.warning(f"[{symbol}] HighTightFlagStrategy 计算失败：{exc}")
                continue

        # 基本面前置过滤
        if selected and self.engine.tushare:
            f_filter = FundamentalFilter(self.engine)
            before = len(selected)
            selected = f_filter.apply_defaults(selected)
            _dbg["fundamental"] = before - len(selected)

        logger.debug(f"[高窄旗形] total={len(symbols)} insufficient={_dbg['insufficient']} no_momentum={_dbg['no_momentum']} no_consolidation={_dbg['no_consolidation']} no_level={_dbg['no_level']} no_shrink={_dbg['no_shrink']} fundamental_dropped={_dbg['fundamental']} selected={len(selected)}")
        logger.info(f"HighTightFlagStrategy 选出 {len(selected)} 只股票")
        return selected
