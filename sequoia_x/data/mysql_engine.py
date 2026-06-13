"""MySQL 数据引擎：连接管理、DDL 初始化、数据读写、元数据查询。"""

from __future__ import annotations

from typing import Optional
import pymysql
import pandas as pd

from sequoia_x.core.config import Settings
from sequoia_x.core.logger import get_logger
from sequoia_x.data.tushare_provider import TushareProvider

logger = get_logger(__name__)


class MySQLEngine:
    """MySQL 数据引擎。

    统一管理 MySQL 连接池、DDL 初始化、数据读写和元数据查询。
    所有策略通过此引擎访问数据库。
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.conn_params: dict[str, object] = {
            "host": settings.mysql_host,
            "port": settings.mysql_port,
            "user": settings.mysql_user,
            "password": settings.mysql_password,
            "database": settings.mysql_database,
            "charset": "utf8mb4",
            "autocommit": True,
        }
        self._sqlalchemy_engine: object | None = None  # cached engine with pool
        self.target_date: str = ""
        self._init_db()
        self.tushare: TushareProvider | None = None
        if settings.tushare_token:
            self.tushare = TushareProvider(
                token=settings.tushare_token,
                proxy_url=settings.tushare_proxy_url,
            )
            logger.info("Tushare 已启用")

    def _init_db(self) -> None:
        """初始化 MySQL 数据库和表（幂等，已存在的表不重建）。"""
        # ── 创建数据库（如果不存在）──
        params: dict[str, object] = {
            "host": self.settings.mysql_host,
            "port": self.settings.mysql_port,
            "user": self.settings.mysql_user,
            "password": self.settings.mysql_password,
            "charset": "utf8mb4",
            "autocommit": True,
        }
        try:
            conn = pymysql.connect(**params)  # type: ignore[arg-type]
            with conn.cursor() as cur:
                cur.execute(
                    "CREATE DATABASE IF NOT EXISTS `%s` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                    % self.settings.mysql_database
                )
            conn.close()
        except Exception as exc:
            logger.warning(f"创建数据库失败（可能已存在）: {exc}")

        # ── 执行 DDL（仅创建不存在的表）──
        try:
            conn = self._get_conn()
            with conn.cursor() as cur:
                cur.execute("SHOW TABLES LIKE 'ts_%'")
                existing = {r[0] for r in cur.fetchall()}

            ddl_path = "data/tushare_ddl.sql"
            with open(ddl_path) as f:
                ddl_content = f.read()

            import re
            # 提取每个 CREATE TABLE 语句（不执行 DROP）
            creates = re.findall(
                r"CREATE TABLE `(\w+)` \(.*?\) ENGINE=.*?;",
                ddl_content, re.DOTALL
            )
            # 找到完整的 CREATE TABLE 匹配
            for m in re.finditer(
                r"CREATE TABLE `(\w+)` \(.*?\) ENGINE=.*?;",
                ddl_content, re.DOTALL
            ):
                table_name = m.group(1)
                if table_name in existing:
                    continue  # 表已存在，跳过
                stmt = m.group(0)
                try:
                    conn.cursor().execute(stmt)
                    logger.info(f"创建表: {table_name}")
                except Exception as exc:
                    logger.warning(f"创建表失败 {table_name}: {exc}")

            # ── 已有表：自动补齐缺失的列 ──
            self._migrate_schema(conn, existing)

            # ── 迁移：删除旧版 row_hash 列（去重方案已移除）──
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT TABLE_NAME FROM information_schema.COLUMNS"
                    " WHERE COLUMN_NAME = 'row_hash'"
                    "   AND TABLE_SCHEMA = %s",
                    (self.settings.mysql_database,),
                )
                for (tbl,) in cur.fetchall():
                    try:
                        cur.execute(f"ALTER TABLE `{tbl}` DROP COLUMN `row_hash`")
                        logger.info(f"迁移: {tbl} 已删除 row_hash 列")
                    except Exception:
                        pass

            conn.close()
            logger.info("MySQL DDL 初始化完成")
        except Exception as exc:
            logger.warning(f"DDL 初始化: {exc}")

    def _migrate_schema(self, conn: pymysql.Connection, tables: set[str]) -> None:
        """为已有表补齐缺失列（对比 DDL 定义，幂等）。"""
        import re

        # 从 DDL 中提取每张表的列定义
        with open("data/tushare_ddl.sql") as f:
            ddl_text = f.read()
        ddl_cols: dict[str, dict[str, str]] = {}  # table → {col_name: col_def}
        for m in re.finditer(
            r"CREATE TABLE `(\w+)` \((.*?)\) ENGINE=", ddl_text, re.DOTALL
        ):
            tname = m.group(1)
            body = m.group(2)
            ddl_cols[tname] = {}
            for cm in re.finditer(
                r"`(\w+)`\s+(\w[\w\s\(\),'-]*?)(?:\s+COMMENT\s+'[^']*')?\s*,?\n",
                body,
            ):
                ddl_cols[tname][cm.group(1)] = cm.group(2).strip()

        for table in sorted(tables):
            if table not in ddl_cols:
                continue
            try:
                with conn.cursor() as cur:
                    cur.execute(f"SHOW COLUMNS FROM `{table}`")
                    existing_cols = {r[0]: r[1] for r in cur.fetchall()}

                for col_name, col_def in ddl_cols[table].items():
                    if col_name == "id":
                        continue
                    if col_name not in existing_cols:
                        # 简化类型：直接取 DDL 中的列定义
                        col_def_clean = re.sub(
                            r"\s+COMMENT\s+'[^']*'", "", col_def
                        )
                        sql = (
                            f"ALTER TABLE `{table}` ADD COLUMN `{col_name}`"
                            f" {col_def_clean}"
                        )
                        try:
                            conn.cursor().execute(sql)
                            logger.info(f"表 {table}: +{col_name} ({col_def_clean})")
                        except Exception as exc:
                            logger.warning(
                                f"表 {table} 添加列 {col_name} 失败: {exc}"
                            )


            except Exception as exc:
                logger.warning(f"表 {table} schema 迁移失败: {exc}")

    def _get_conn(self) -> pymysql.Connection:
        """获取 MySQL 连接。"""
        return pymysql.connect(**self.conn_params)  # type: ignore[arg-type]

    # ── 通用查询 ──

    def query(self, sql: str, params: object = None) -> "pd.DataFrame":
        """执行 SQL 查询，返回 DataFrame。

        含参数时用原生 PyMySQL 连接（避免 SQLAlchemy 的 %s 混淆）。
        无参数时用 SQLAlchemy 引擎。
        """
        import warnings
        if params is not None:
            if isinstance(params, (list, set)):
                params = tuple(params)
            conn = self._get_conn()
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    return pd.read_sql(sql, conn, params=params)
            finally:
                conn.close()
        return pd.read_sql(sql, self._get_sqlalchemy_engine())

    def fetch_all(self, sql: str, params: object = None) -> list[tuple]:
        """执行 SQL 查询，返回所有行（list of tuples）。"""
        if isinstance(params, (list, set)):
            params = tuple(params)
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()
        finally:
            conn.close()

    def fetch_one(self, sql: str, params: object = None) -> object:
        """执行 SQL 查询，返回单个标量值。"""
        if isinstance(params, (list, set)):
            params = tuple(params)
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                row = cur.fetchone()
                return row[0] if row else None
        finally:
            conn.close()

    def execute(self, sql: str, params: object = None) -> int:
        """执行非查询 SQL（INSERT/UPDATE/DELETE），返回影响行数。"""
        if isinstance(params, (list, set)):
            params = tuple(params)
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                return cur.execute(sql, params)
        finally:
            conn.close()

    # ── 股票数据读取 ──

    _ohlcv_cache: dict[str, "pd.DataFrame"] | None = None  # class-level cache, reset per run

    def get_ohlcv(self, symbol: str) -> pd.DataFrame:
        """获取单只股票日K线数据（内置批量缓存）。

        首次调用时一次性加载全市场 K 线到内存，
        后续调用直接从缓存字典返回，避免逐条 DB 往返。
        """
        if MySQLEngine._ohlcv_cache is None:
            self._preload_ohlcv_cache()
        cache = MySQLEngine._ohlcv_cache or {}
        # 按 ts_code 精确匹配（symbol 可能是纯数字，ts_code 带后缀）
        for ts_code, df in cache.items():
            if ts_code.startswith(symbol):
                return df.copy()
        # Fallback: 缓存中未找到时单独查询
        return self._get_ohlcv_direct(symbol)

    def _preload_ohlcv_cache(self) -> None:
        """预加载全市场 OHLCV 到类级缓存。"""
        cols = "ts_code, trade_date, open, high, low, close, pre_close, `change`, pct_chg, vol, amount"
        eng = self._get_sqlalchemy_engine()
        if self.target_date:
            sql = f"SELECT {cols} FROM ts_daily WHERE trade_date <= '{self.target_date}' ORDER BY ts_code, trade_date"
        else:
            sql = f"SELECT {cols} FROM ts_daily ORDER BY ts_code, trade_date"
        df = pd.read_sql(sql, eng)
        if df.empty:
            MySQLEngine._ohlcv_cache = {}
            return
        # 标准化列名
        if "vol" in df.columns:
            df = df.rename(columns={"vol": "volume", "trade_date": "date"})
        if "amount" in df.columns and "turnover" not in df.columns:
            df = df.rename(columns={"amount": "turnover"})
        # 确保数值列为 float（MySQL NULL → pd.to_numeric → NaN，避免 Python None）
        _numeric_cols = ["open", "high", "low", "close", "pre_close",
                         "pct_chg", "volume", "turnover"]
        for _nc in _numeric_cols:
            if _nc in df.columns:
                df[_nc] = pd.to_numeric(df[_nc], errors="coerce")
        cache: dict[str, "pd.DataFrame"] = {}
        for code, group in df.groupby("ts_code"):
            cache[code] = group.reset_index(drop=True)
        MySQLEngine._ohlcv_cache = cache
        logger.info(f"OHLCV 缓存预加载完成: {len(cache)} 只股票")

    def _get_ohlcv_direct(self, symbol: str) -> pd.DataFrame:
        """直接查询单只股票 K 线（缓存未命中时的降级路径）。"""
        cols = "ts_code, trade_date, open, high, low, close, pre_close, `change`, pct_chg, vol, amount"
        eng = self._get_sqlalchemy_engine()
        if self.target_date:
            df = pd.read_sql(
                f"SELECT {cols} FROM ts_daily WHERE ts_code LIKE %s AND trade_date <= %s ORDER BY trade_date",
                eng, params=(f"{symbol}%", self.target_date),
            )
        else:
            df = pd.read_sql(
                f"SELECT {cols} FROM ts_daily WHERE ts_code LIKE %s ORDER BY trade_date",
                eng, params=(f"{symbol}%",),
            )
        if "vol" in df.columns:
            df = df.rename(columns={"vol": "volume", "trade_date": "date"})
        if "amount" in df.columns and "turnover" not in df.columns:
            df = df.rename(columns={"amount": "turnover"})
        # 确保数值列为 float
        _numeric_cols = ["open", "high", "low", "close", "pre_close",
                         "pct_chg", "volume", "turnover"]
        for _nc in _numeric_cols:
            if _nc in df.columns:
                df[_nc] = pd.to_numeric(df[_nc], errors="coerce")
        return df

    def get_all_ohlcv(self, symbols: list[str] | None = None) -> dict[str, 'pd.DataFrame']:
        """批量获取全市场 OHLCV 数据（单次 SQL 查询）。

        避免 per-symbol 逐条查询，将 ~5000 次 DB 往返降为 1 次。
        返回 {ts_code: DataFrame}，DataFrame 已按 trade_date 排序且列名已标准化。

        Args:
            symbols: 可选，指定股票代码列表；默认查询全市场。
        """
        eng = self._get_sqlalchemy_engine()
        cols = "ts_code, trade_date, open, high, low, close, pre_close, `change`, pct_chg, vol, amount"
        if symbols:
            placeholders = ",".join([f"'{s}%'" for s in symbols])
            where = f"WHERE ts_code IN ({placeholders})"
        else:
            where = ""
        if self.target_date:
            date_filter = f"{'AND' if where else 'WHERE'} trade_date <= '{self.target_date}'"
        else:
            date_filter = ""
        sql = f"SELECT {cols} FROM ts_daily {where} {date_filter} ORDER BY ts_code, trade_date"
        df = pd.read_sql(sql, eng)
        if df.empty:
            return {}
        # 标准化列名
        if "vol" in df.columns:
            df = df.rename(columns={"vol": "volume", "trade_date": "date"})
        if "amount" in df.columns and "turnover" not in df.columns:
            df = df.rename(columns={"amount": "turnover"})
        # 按 ts_code 分组返回
        result: dict[str, pd.DataFrame] = {}
        for code, group in df.groupby("ts_code"):
            result[code] = group.reset_index(drop=True)
        return result

    @staticmethod
    def _limit_bars_per_symbol(df_map: dict[str, 'pd.DataFrame'], n: int = 300) -> dict[str, 'pd.DataFrame']:
        """每个 symbol 只保留最近 n 根 K 线，减少内存和计算量。"""
        return {k: v.tail(n) for k, v in df_map.items()}

    def _get_sqlalchemy_engine(self) -> object:
        """获取缓存的 SQLAlchemy engine（用于 pandas read_sql）。

        首次调用时创建带连接池的 engine，后续复用。
        避免每次查询都重建 engine 的开销。
        """
        if self._sqlalchemy_engine is not None:
            return self._sqlalchemy_engine
        from sqlalchemy import create_engine
        url = f"mysql+pymysql://{self.settings.mysql_user}:{self.settings.mysql_password}@{self.settings.mysql_host}:{self.settings.mysql_port}/{self.settings.mysql_database}?charset=utf8mb4"
        self._sqlalchemy_engine = create_engine(
            url,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
            pool_pre_ping=True,
        )
        return self._sqlalchemy_engine

    def get_local_symbols(self) -> list[str]:
        """获取数据库中已有K线的股票代码列表。"""
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT ts_code FROM ts_daily ORDER BY ts_code")
                return [r[0] for r in cur.fetchall()]
        finally:
            conn.close()

    # ── 元数据查询 ──

    def get_stock_names(self, symbols: list[str]) -> dict[str, str]:
        """批量查询股票名称（单次 SQL 查询，避免 N 次往返）。"""
        if not symbols:
            return {}
        result: dict[str, str] = {s: "" for s in symbols}
        placeholders = ",".join(["%s"] * len(symbols))
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT ts_code, name FROM ts_stock_basic WHERE ts_code IN ({placeholders})",
                    symbols,
                )
                for row in cur.fetchall():
                    result[row[0]] = row[1] or ""
        finally:
            conn.close()
        return result

    def get_stock_meta_batch(self, symbols: list[str]) -> dict[str, dict[str, object]]:
        """批量获取股票元数据（名称、行业、PE、市值、资金流向）。
        
        优化为 3 次批量查询（而非每只股票 3 次查询）。
        """
        if not symbols:
            return {}
        result: dict[str, dict[str, object]] = {
            s: {"symbol": s, "name": "", "industry": "",
                "pe_ttm": None, "circ_mv": None, "net_mf_amount": None}
            for s in symbols
        }
        placeholders = ",".join(["%s"] * len(symbols))
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                # 查询 1：股票名称 + 行业
                cur.execute(
                    f"SELECT ts_code, name, industry FROM ts_stock_basic WHERE ts_code IN ({placeholders})",
                    symbols,
                )
                for row in cur.fetchall():
                    if row[0] in result:
                        result[row[0]]["name"] = row[1] or ""
                        result[row[0]]["industry"] = row[2] or ""

                # 查询 2：最新 PE + 流通市值（窗口函数取每个 ts_code 最新一条）
                cur.execute(
                    f"""SELECT ts_code, pe_ttm, circ_mv FROM (
                        SELECT ts_code, pe_ttm, circ_mv,
                            ROW_NUMBER() OVER (PARTITION BY ts_code ORDER BY trade_date DESC) AS rn
                        FROM ts_daily_basic WHERE ts_code IN ({placeholders})
                    ) t WHERE rn = 1""",
                    symbols,
                )
                for row in cur.fetchall():
                    if row[0] in result:
                        result[row[0]]["pe_ttm"] = row[1]
                        result[row[0]]["circ_mv"] = row[2]

                # 查询 3：最新资金流向
                cur.execute(
                    f"""SELECT ts_code, net_mf_amount FROM (
                        SELECT ts_code, net_mf_amount,
                            ROW_NUMBER() OVER (PARTITION BY ts_code ORDER BY trade_date DESC) AS rn
                        FROM ts_moneyflow WHERE ts_code IN ({placeholders})
                    ) t WHERE rn = 1""",
                    symbols,
                )
                for row in cur.fetchall():
                    if row[0] in result:
                        result[row[0]]["net_mf_amount"] = row[1]
        finally:
            conn.close()
        return result

    def is_trading_day(self, trade_date: str = "") -> bool:
        """检查是否为交易日。"""
        from datetime import date
        target = trade_date or date.today().strftime("%Y%m%d")
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT is_open FROM ts_trade_cal WHERE cal_date = %s",
                    (target,),
                )
                row = cur.fetchone()
            if row is not None:
                return row[0] == "1"
            return True
        except Exception:
            return True
        finally:
            conn.close()

    @staticmethod
    def _drop_ts_code(df: pd.DataFrame) -> pd.DataFrame:
        """移除 ts_code 列。"""
        if "ts_code" in df.columns:
            return df.drop(columns=["ts_code"])
        return df
