"""MySQL 数据引擎：连接管理、DDL 初始化、数据读写、元数据查询。"""

from __future__ import annotations

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
                    if col_name in ("id", "row_hash", "uk_row_hash"):
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

                # 确保 row_hash 存在
                if "row_hash" in ddl_cols[table] and "row_hash" not in existing_cols:
                    conn.cursor().execute(
                        f"ALTER TABLE `{table}` ADD COLUMN `row_hash`"
                        f" CHAR(32) NOT NULL"
                        f" COMMENT 'MD5 of all field values for dedup'"
                    )
                    try:
                        conn.cursor().execute(
                            f"ALTER TABLE `{table}`"
                            f" ADD UNIQUE KEY `uk_row_hash` (`row_hash`)"
                        )
                    except Exception:
                        pass
                    # 计算已有数据的 hash
                    with conn.cursor() as cur:
                        cur.execute(f"SHOW COLUMNS FROM `{table}`")
                        all_cols = [r[0] for r in cur.fetchall()]
                    data_cols = [
                        c for c in all_cols if c not in ("id", "row_hash")
                    ]
                    if data_cols:
                        parts = ", '|', ".join(
                            f"IFNULL(`{c}`, '\\0')" for c in data_cols
                        )
                        conn.cursor().execute(
                            f"UPDATE `{table}` SET `row_hash` ="
                            f" MD5(CONCAT({parts}))"
                        )
                    logger.info(f"表 {table}: 已添加 row_hash 列")
            except Exception as exc:
                logger.warning(f"表 {table} schema 迁移失败: {exc}")

    def _get_conn(self) -> pymysql.Connection:
        """获取 MySQL 连接。"""
        return pymysql.connect(**self.conn_params)  # type: ignore[arg-type]

    # ── 通用查询 ──

    def query(self, sql: str, params: object = None) -> "pd.DataFrame":
        """执行 SQL 查询，返回 DataFrame。

        含参数时用原生 PyMySQL 连接（避免 SQLAlchemy 的 %s 混淆）。
        无参数时用 SQLAlchemy 引擎（pandas read_sql 效率更高）。
        """
        if params is not None:
            if isinstance(params, (list, set)):
                params = tuple(params)
            conn = self._get_conn()
            try:
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

    def get_ohlcv(self, symbol: str) -> pd.DataFrame:
        """获取单只股票日K线数据。"""
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
        # 重命名列以兼容策略层
        if "vol" in df.columns:
            df = df.rename(columns={"vol": "volume", "trade_date": "date"})
        if "amount" in df.columns and "turnover" not in df.columns:
            df = df.rename(columns={"amount": "turnover"})
        return df

    def _get_sqlalchemy_engine(self):
        """获取 SQLAlchemy engine（用于 pandas read_sql）。"""
        from sqlalchemy import create_engine
        url = f"mysql+pymysql://{self.settings.mysql_user}:{self.settings.mysql_password}@{self.settings.mysql_host}:{self.settings.mysql_port}/{self.settings.mysql_database}?charset=utf8mb4"
        return create_engine(url)

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
        """批量查询股票名称。"""
        if not symbols:
            return {}
        conn = self._get_conn()
        try:
            result: dict[str, str] = {}
            for s in symbols:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT name FROM ts_stock_basic WHERE ts_code LIKE %s LIMIT 1",
                        (f"{s}%",),
                    )
                    row = cur.fetchone()
                    result[s] = row[0] if row else ""
            return result
        finally:
            conn.close()

    def get_stock_meta_batch(self, symbols: list[str]) -> dict[str, dict[str, object]]:
        """批量获取股票元数据（名称、行业、PE、市值、资金流向）。"""
        if not symbols:
            return {}
        conn = self._get_conn()
        result: dict[str, dict[str, object]] = {}
        try:
            for s in symbols:
                meta: dict[str, object] = {
                    "symbol": s, "name": "", "industry": "",
                    "pe_ttm": None, "circ_mv": None, "net_mf_amount": None,
                }
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT name, industry FROM ts_stock_basic WHERE ts_code LIKE %s LIMIT 1",
                        (f"{s}%",),
                    )
                    row = cur.fetchone()
                    if row:
                        meta["name"] = row[0] or ""
                        meta["industry"] = row[1] or ""

                    cur.execute(
                        "SELECT pe_ttm, circ_mv FROM ts_daily_basic WHERE ts_code LIKE %s ORDER BY trade_date DESC LIMIT 1",
                        (f"{s}%",),
                    )
                    row = cur.fetchone()
                    if row:
                        meta["pe_ttm"] = row[0]
                        meta["circ_mv"] = row[1]

                    cur.execute(
                        "SELECT net_mf_amount FROM ts_moneyflow WHERE ts_code LIKE %s ORDER BY trade_date DESC LIMIT 1",
                        (f"{s}%",),
                    )
                    row = cur.fetchone()
                    if row:
                        meta["net_mf_amount"] = row[0]

                result[s] = meta
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
