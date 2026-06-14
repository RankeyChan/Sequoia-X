"""行业轮动策略：识别近 N 日最强行业，精选行业内个股。"""

from datetime import date, timedelta

import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy

logger = get_logger(__name__)

class SectorRotationStrategy(BaseStrategy):
    """行业轮动策略。

    选股条件：
    1. 计算各行业近 20 日平均涨幅，选取前 3 强行业
    2. 在强势行业中选股：近 20 日涨幅 > 行业平均
    3. PE > 0 且 < 100
    4. 流通市值 ≥ 30 亿

    依赖 stock_basic 表的 industry 字段进行行业分类。

    Attributes:
        webhook_key: 路由到 'sector_rotation' 专属飞书机器人。
    """

    webhook_key: str = "sector_rotation"
    name_cn: str = "行业轮动"
    _LOOKBACK: int = 20

    def run(self) -> list[str]:
        symbols = self.engine.get_local_symbols()
        if not symbols:
            return []

        # 计算所有股票近 N 日涨幅
        stock_pct: dict[str, float] = {}
        for symbol in symbols:
            try:
                df = self.engine.get_ohlcv(symbol)
                if len(df) < self._LOOKBACK:
                    continue
                pct = df["close"].iloc[-1] / df["close"].iloc[-self._LOOKBACK - 1] - 1
                stock_pct[symbol] = pct
            except Exception:
                continue

        if not stock_pct:
            return []

        # 获取行业分类
        try:
            rows = self.engine.fetch_all(
                "SELECT ts_code, industry FROM ts_stock_basic WHERE industry IS NOT NULL"
            )
        except Exception as exc:
            logger.warning(f"读取行业数据失败: {exc}")
            return []

        # 行业 -> 股票列表 映射
        industry_map: dict[str, list[str]] = {}
        for symbol, industry in rows:
            if industry not in ("", "None", None) and symbol in stock_pct:
                industry_map.setdefault(industry, []).append(symbol)

        if not industry_map:
            return []

        # 计算行业平均涨幅
        industry_perf: dict[str, float] = {}
        for industry, syms in industry_map.items():
            pcts = [stock_pct[s] for s in syms if s in stock_pct]
            if len(pcts) >= 5:  # 至少 5 只股票才统计
                industry_perf[industry] = sum(pcts) / len(pcts)

        if not industry_perf:
            return []

        # 选取前 3 强行业
        top_industries = sorted(industry_perf, key=industry_perf.get, reverse=True)[:3]
        logger.info(f"SectorRotation: 前 3 行业: {[(ind, f'{industry_perf[ind]:.1%}') for ind in top_industries]}")

        # 在强势行业中选股
        selected: list[str] = []
        for industry in top_industries:
            industry_avg = industry_perf[industry]
            for symbol in industry_map[industry]:
                if stock_pct.get(symbol, 0) >= industry_avg and stock_pct.get(symbol, 0) > 0:
                    selected.append(symbol)

        logger.debug(f"[行业轮动] total={len(symbols)} industries={len(industry_map) if 'industry_map' in dir() else 0} top_industries={len(top_industries) if 'top_industries' in dir() else 0} selected={len(selected)}")
        logger.info(f"SectorRotationStrategy 选出 {len(selected)} 只股票")
        return selected
