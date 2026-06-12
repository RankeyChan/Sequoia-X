"""机构追踪策略：综合龙虎榜机构买入 + 机构调研记录，捕捉机构关注信号。"""

import sqlite3
from datetime import date, timedelta

import pandas as pd

from sequoia_x.core.logger import get_logger
from sequoia_x.strategy.base import BaseStrategy
from sequoia_x.strategy.filters import FundamentalFilter

logger = get_logger(__name__)


class InstitutionalStrategy(BaseStrategy):
    """机构追踪策略。

    选股条件（满足任一即可）：
    1. 近5日龙虎榜有机构买入（top_inst net_buy > 0）
    2. 或近30天有机构调研记录

    额外过滤：
    - 近5日涨幅 < 15%（防止追高）
    - PE > 0（非亏损股）
    - 流通市值 ≥ 20亿

    Attributes:
        webhook_key: 路由到 'institutional' 专属飞书机器人。
    """

    webhook_key: str = "institutional"
    name_cn: str = "机构追踪"
    _INST_LOOKBACK: int = 5   # 龙虎榜回看天数
    _SURV_LOOKBACK: int = 30  # 调研回看天数

    def _get_institutional_buys(self) -> set[str]:
        """获取近5日龙虎榜有机构净买入的股票列表。"""
        cutoff = (date.today() - timedelta(days=self._INST_LOOKBACK)).strftime("%Y%m%d")
        try:
            with sqlite3.connect(self.engine.db_path) as conn:
                # 只取机构（排除游资）
                rows = conn.execute(
                    """
                    SELECT DISTINCT symbol FROM top_inst
                    WHERE date >= ?
                    AND side = '买入'
                    AND net_buy > 0
                    AND (exalter LIKE '%机构%' OR exalter LIKE '%专用%')
                    """,
                    (cutoff,),
                ).fetchall()
            return {r[0] for r in rows}
        except Exception:
            return set()

    def _get_survey_stocks(self) -> set[str]:
        """获取近30天有机构调研的股票列表（需实时调 Tushare 或检查本地缓存）。"""
        # 尝试从本地 top_list 表获取（如果存了 reason 包含调研）
        cutoff = (date.today() - timedelta(days=self._SURV_LOOKBACK)).strftime("%Y%m%d")
        try:
            with sqlite3.connect(self.engine.db_path) as conn:
                # 从龙虎榜 reason 字段找调研相关
                rows = conn.execute(
                    """
                    SELECT DISTINCT symbol FROM top_list
                    WHERE date >= ? AND reason LIKE '%调研%'
                    """,
                    (cutoff,),
                ).fetchall()
            return {r[0] for r in rows}
        except Exception:
            return set()

    def run(self) -> list[str]:
        """返回近期有机构关注信号的股票代码列表。"""
        if not self.engine.tushare:
            logger.warning("Tushare 未启用，InstitutionalStrategy 无法运行")
            return []

        symbols = self.engine.get_local_symbols()
        if not symbols:
            return []

        # 1. 获取机构买入股票
        inst_buys = self._get_institutional_buys()
        logger.info(f"InstitutionalStrategy: 近{self._INST_LOOKBACK}日机构买入 {len(inst_buys)} 只")

        # 2. 获取机构调研股票
        surv_stocks = self._get_survey_stocks()
        logger.info(f"InstitutionalStrategy: 近{self._SURV_LOOKBACK}日机构调研 {len(surv_stocks)} 只")

        # 3. 合并
        candidates = list(inst_buys | surv_stocks)

        if not candidates:
            return []

        # 4. 涨幅过滤（近5日涨幅 < 15%）
        selected: list[str] = []
        for symbol in candidates:
            try:
                df = self.engine.get_ohlcv(symbol)
                if len(df) < 5:
                    continue
                pct_5d = (df["close"].iloc[-1] / df["close"].iloc[-6] - 1) * 100
                if pct_5d < 15:
                    selected.append(symbol)
            except Exception:
                continue

        # 5. 基本面过滤
        if selected:
            f_filter = FundamentalFilter(self.engine)
            selected = f_filter.filter_st_stocks(selected)
            selected = f_filter.filter_by_market_cap(selected, min_cap=20e8)
            selected = f_filter.filter_by_pe(selected, max_pe=200, min_pe=0)

        logger.info(f"InstitutionalStrategy 选出 {len(selected)} 只股票")
        return selected
