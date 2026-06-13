"""行业动量策略：先识别强势行业，再从中筛选趋势动量个股。"""

from datetime import date, timedelta

import numpy as np
import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy

logger = get_logger(__name__)

class SectorMomentumStrategy(BaseStrategy):
    """行业动量策略（融合行业轮动 + 趋势动量）。

    两步法：
    第一步 — 行业轮动筛选：
      1. 计算各行业近 20 日平均涨幅
      2. 选取前 N 强行业（默认 3 个）

    第二步 — 行业内趋势动量精选：
      1. MA5 > MA20 > MA60（标准多头排列）
      2. RSI(14) 在 50~80 之间（强势未超买）
      3. 近 20 日涨幅 5%~30%（温和放量上涨）
      4. 行业内涨幅排名前 50%

    Attributes:
        webhook_key: 路由到 'sector_momentum' 专属飞书机器人。
    """

    webhook_key: str = "sector_momentum"
    name_cn: str = "行业动量"
    _MIN_BARS: int = 60
    _LOOKBACK: int = 20
    _TOP_SECTORS: int = 3
    _INDUSTRY_MIN_STOCKS: int = 5  # 行业至少 N 只股票才统计

    @staticmethod
    def _compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
        delta = series.diff()
        gain = delta.clip(lower=0).rolling(window=period).mean()
        loss = (-delta.clip(upper=0)).rolling(window=period).mean()
        rs = gain / loss.replace(0, float("nan"))
        return 100 - (100 / (1 + rs))

    def run(self) -> list[str]:
        symbols = self.engine.get_local_symbols()
        if not symbols:
            return []

        # ── 第一步：计算全市场个股近 N 日涨幅 ──
        stock_pct: dict[str, float] = {}
        stock_ma_valid: dict[str, bool] = {}
        stock_rsi: dict[str, float] = {}

        for symbol in symbols:
            try:
                df = self.engine.get_ohlcv(symbol)
                if len(df) < self._MIN_BARS:
                    continue

                close = df["close"].astype(float)
                ma5 = close.rolling(5).mean()
                ma20 = close.rolling(20).mean()
                ma60 = close.rolling(60).mean()

                last5 = ma5.iloc[-1]
                last20 = ma20.iloc[-1]
                last60 = ma60.iloc[-1]
                if pd.isna(last5) or pd.isna(last20) or pd.isna(last60):
                    continue

                # 涨幅
                pct_20d = close.iloc[-1] / close.iloc[-self._LOOKBACK - 1] - 1
                stock_pct[symbol] = pct_20d

                # 多头排列
                stock_ma_valid[symbol] = (last5 > last20 > last60)

                # RSI
                rsi = self._compute_rsi(close)
                last_rsi = rsi.iloc[-1]
                stock_rsi[symbol] = last_rsi if not pd.isna(last_rsi) else 0.0

            except Exception:
                continue

        if not stock_pct:
            return []

        # ── 第二步：行业轮动分析 ──
        try:
            rows = self.engine.fetch_all(
                "SELECT ts_code, industry FROM ts_stock_basic WHERE industry IS NOT NULL"
            )
        except Exception as exc:
            logger.warning(f"读取行业数据失败: {exc}")
            return []

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
            if len(pcts) >= self._INDUSTRY_MIN_STOCKS:
                industry_perf[industry] = float(np.mean(pcts))

        if not industry_perf:
            return []

        # 取前 N 强行业
        top_industries = sorted(
            industry_perf, key=industry_perf.get, reverse=True
        )[:self._TOP_SECTORS]

        logger.info(
            f"SectorMomentum: 前{self._TOP_SECTORS}行业: "
            + ", ".join(f"{ind}({industry_perf[ind]:.1%})" for ind in top_industries)
        )

        # ── 第三步：行业内趋势动量精选 ──
        selected: list[str] = []
        for industry in top_industries:
            candidates = industry_map[industry]
            # 只保留有涨幅数据且多头排列的
            valid = [
                s for s in candidates
                if s in stock_pct and stock_ma_valid.get(s, False)
            ]
            if not valid:
                continue

            # 行业内按涨幅排序
            valid.sort(key=lambda s: stock_pct[s], reverse=True)

            # 取涨幅前 50%（行业内相对强势）
            top_n = max(1, len(valid) // 2)
            for symbol in valid[:top_n]:
                pct = stock_pct[symbol]
                rsi_val = stock_rsi.get(symbol, 50)

                # 趋势动量条件
                if not (0.05 <= pct <= 0.30):
                    continue
                if not (50 <= rsi_val <= 80):
                    continue

                selected.append(symbol)

        logger.info(f"SectorMomentumStrategy 选出 {len(selected)} 只股票")
        return selected
