"""基本面过滤器：PE/PB/市值/换手率/ST 筛选，可在任意策略中作为前置条件。"""

from sequoia_x.core.logger import get_logger

logger = get_logger(__name__)

class FundamentalFilter:
    """基本面过滤器。

    从本地 SQLite 数据库读取每日指标和股票基础信息，
    对候选股票列表按基本面条件过滤。

    Usage:
        filter = FundamentalFilter(engine)
        symbols = filter.apply_defaults(candidates)
        symbols = filter.filter_by_pe(symbols, max_pe=50)
    """

    def __init__(self, engine: "MySQLEngine") -> None:  # noqa: F821
        self.engine = engine

    def _get_pe_map(self, symbols: list[str]) -> dict[str, float]:
        """获取最新 PE（TTM）。"""
        if not symbols:
            return {}
        placeholders = ",".join(["%s"] * len(symbols))
        try:
            rows = self.engine.fetch_all(
                f"""
                SELECT ts_code, pe_ttm FROM ts_daily_basic
                WHERE ts_code IN ({placeholders})
                AND trade_date = (SELECT MAX(trade_date) FROM ts_daily_basic WHERE ts_code = ts_daily_basic.ts_code)
                """,
                symbols,
            )
            return {r[0]: r[1] or 0 for r in rows}
        except Exception:
            return {}

    def _get_daily_basic_batch(self, symbols: list[str]) -> dict[str, dict[str, float]]:
        """获取最新 PB / 流通市值 / 换手率（合并为 1 次 SQL 查询）。"""
        if not symbols:
            return {"pb": {}, "cap": {}, "turn": {}}
        placeholders = ",".join(["%s"] * len(symbols))
        try:
            all_rows = self.engine.fetch_all(
                f"""SELECT t.ts_code, t.pb, t.circ_mv, t.turnover_rate
                FROM ts_daily_basic t
                INNER JOIN (
                    SELECT ts_code, MAX(trade_date) AS max_td
                    FROM ts_daily_basic WHERE ts_code IN ({placeholders})
                    GROUP BY ts_code
                ) m ON t.ts_code = m.ts_code AND t.trade_date = m.max_td""",
                symbols,
            )
            return {
                "pb": {r[0]: r[1] or 0 for r in all_rows},
                "cap": {r[0]: r[2] or 0 for r in all_rows},
                "turn": {r[0]: r[3] or 0 for r in all_rows},
            }
        except Exception as exc:
            logger.warning(f"_get_daily_basic_batch 失败: {exc}")
            return {"pb": {}, "cap": {}, "turn": {}}

    def _get_st_stocks(self) -> set[str]:
        """获取当前 ST 股票列表。"""
        try:
            # 通过 name 字段识别 ST
            rows = self.engine.fetch_all(
                "SELECT ts_code FROM ts_stock_basic WHERE name LIKE '%ST%'"
            )
            return {r[0] for r in rows}
        except Exception:
            return set()

    # ── 单项过滤器 ──

    def filter_by_pe(
        self, symbols: list[str], max_pe: float = 200, min_pe: float = 0
    ) -> list[str]:
        """按 PE(TTM) 过滤。排除亏损股（PE<=0）和过高估值。"""
        pe_map = self._get_pe_map(symbols)
        result = [
            s for s in symbols
            if s in pe_map and min_pe < pe_map[s] < max_pe
        ]
        logger.info(f"PE 过滤: {len(symbols)} -> {len(result)} (PE {min_pe}~{max_pe})")
        return result

    def filter_by_pb(self, symbols: list[str], max_pb: float = 10) -> list[str]:
        """按 PB 过滤。"""
        pb_map = self._get_daily_basic_batch(symbols)["pb"]
        result = [
            s for s in symbols
            if s in pb_map and 0 < pb_map[s] < max_pb
        ]
        logger.info(f"PB 过滤: {len(symbols)} -> {len(result)} (PB<{max_pb})")
        return result

    def filter_by_market_cap(
        self, symbols: list[str], min_cap_wan: float = 100000
    ) -> list[str]:
        """按流通市值过滤（默认最小 10 亿）。"""
        cap_map = self._get_daily_basic_batch(symbols)["cap"]
        result = [s for s in symbols if s in cap_map and cap_map[s] >= min_cap_wan]
        logger.info(f"市值过滤: {len(symbols)} -> {len(result)} (≥{min_cap_wan / 1e4:.0f}亿)")
        return result

    def filter_by_turnover_rate(
        self, symbols: list[str], min_rate: float = 2.0
    ) -> list[str]:
        """按换手率过滤（默认最小 2%）。"""
        turn_map = self._get_daily_basic_batch(symbols)["turn"]
        result = [s for s in symbols if s in turn_map and turn_map[s] >= min_rate]
        logger.info(f"换手率过滤: {len(symbols)} -> {len(result)} (≥{min_rate}%)")
        return result

    def filter_st_stocks(self, symbols: list[str]) -> list[str]:
        """排除 ST 股票。"""
        st_set = self._get_st_stocks()
        if not st_set:
            return symbols
        result = [s for s in symbols if s not in st_set]
        logger.info(f"ST 过滤: {len(symbols)} -> {len(result)} (排除 {len(st_set)} 只)")
        return result

    # ── 组合过滤器 ──

    def apply_defaults(self, symbols: list[str]) -> list[str]:
        """默认基本面过滤：排除 ST、市值 ≥10亿、PE 0~300。

        这是一个温和的过滤器，适合大多数技术策略作为前置条件。

        Args:
            symbols: 候选股票代码列表。

        Returns:
            过滤后的股票代码列表。
        """
        if not symbols:
            return []
        result = self.filter_st_stocks(symbols)
        result = self.filter_by_market_cap(result, min_cap_wan=100000)
        result = self.filter_by_pe(result, max_pe=300, min_pe=0)
        logger.info(f"默认基本面过滤: {len(symbols)} -> {len(result)}")
        return result
