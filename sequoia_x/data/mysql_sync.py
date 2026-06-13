"""MySQL 数据同步：日频数据同步、回填。

通过 monkey-patch 注册到 MySQLEngine 上。
仅同步 DDL 中已有的表。
"""

from __future__ import annotations

from datetime import date

import pandas as pd
import pymysql

from sequoia_x.core.logger import get_logger

logger = get_logger(__name__)


# ── 错误分类 ──

def _is_db_error(exc: Exception) -> bool:
    """判断是否为数据库连接/执行错误（需要立即中止，不应重试）。"""
    return isinstance(exc, (
        pymysql.err.OperationalError,
        pymysql.err.ProgrammingError,
        pymysql.err.InternalError,
        pymysql.err.IntegrityError,
    ))


# ── MySQL 写入 ──


def _write_mysql(conn: pymysql.Connection, table: str, df: pd.DataFrame) -> int:
    """Plain INSERT，无 row_hash。"""
    if df.empty:
        return 0
    with conn.cursor() as cur:
        cur.execute(f"SHOW COLUMNS FROM `{table}`")
        table_cols = {r[0] for r in cur.fetchall()}
    available = [c for c in df.columns if c in table_cols and c != "id"]
    if not available:
        return 0
    sub = df[available]
    import numpy as np
    arrays = {c: sub[c].to_numpy(dtype=object, na_value=None) for c in available}
    n_rows = len(sub)
    rows = [tuple(arrays[c][i] for c in available) for i in range(n_rows)]
    cols = ", ".join(f"`{c}`" for c in available)
    placeholders = ", ".join(["%s"] * len(available))
    sql = f"INSERT INTO `{table}` ({cols}) VALUES ({placeholders})"
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM `{table}`")
        before = cur.fetchone()[0]
        cur.executemany(sql, rows)
        cur.execute(f"SELECT COUNT(*) FROM `{table}`")
        after = cur.fetchone()[0]
    inserted = after - before
    logger.info(f"[{table}] 写入 {inserted} 行")
    return inserted
# ══════════════════════════════════════════════════════════════════════
# API 分类（按同步频率）
# ══════════════════════════════════════════════════════════════════════

# 每日同步：日线、资金流向、涨跌停、龙虎榜等
_DAILY_APIS = [
    ("get_daily", "ts_daily", {"vol": "volume"}),
    ("get_daily_basic", "ts_daily_basic", {}),
    ("get_moneyflow", "ts_moneyflow", {}),
    ("get_margin_detail", "ts_margin_detail", {}),
    ("get_limit_list", "ts_limit_list_d", {}),
    ("get_top_list", "ts_top_list", {}),
    ("get_top_inst", "ts_top_inst", {}),
    ("get_hk_hold", "ts_hk_hold", {}),
    ("get_block_trade", "ts_block_trade", {}),
    ("get_stk_limit", "ts_stk_limit", {}),
    ("get_adj_factor", "ts_adj_factor", {}),
    ("get_hsgt_top10", "ts_hsgt_top10", {}),
    ("get_moneyflow_hsgt", "ts_moneyflow_hsgt", {}),
    ("get_suspend_d", "ts_suspend_d", {}),
    ("get_cyq_perf", "ts_cyq_perf", {}),
    ("get_moneyflow_ths", "ts_moneyflow_ths", {}),
    ("get_moneyflow_dc", "ts_moneyflow_dc", {}),
    ("get_moneyflow_cnt_ths", "ts_moneyflow_cnt_ths", {}),
    ("get_moneyflow_ind_ths", "ts_moneyflow_ind_ths", {}),
    ("get_moneyflow_ind_dc", "ts_moneyflow_ind_dc", {}),
    ("get_moneyflow_mkt_dc", "ts_moneyflow_mkt_dc", {}),
    ("get_ggt_top10", "ts_ggt_top10", {}),
    ("get_ths_hot", "ts_ths_hot", {}),
    ("get_dc_hot", "ts_dc_hot", {}),
    ("get_kpl_list", "ts_kpl_list", {}),
    ("get_limit_list_ths", "ts_limit_list_ths", {}),
    ("get_hm_detail", "ts_hm_detail", {}),
]

# 每周最后交易日同步
_WEEKLY_APIS = [
    ("get_weekly", "ts_weekly", {}),
]

# 每月最后交易日同步
_MONTHLY_APIS = [
    ("get_monthly", "ts_monthly", {}),
]

# 周月线（每日调用，需传 freq 参数）
_WEEK_MONTH_FREQ_APIS = [
    ("get_stk_weekly_monthly", "ts_stk_weekly_monthly", {}),
    ("get_stk_week_month_adj", "ts_stk_week_month_adj", {}),
]

# 财务数据（VIP 接口，period 一次返回全量）
_FINANCIAL_VIP = [
    "income_vip", "balancesheet_vip", "cashflow_vip",
    "forecast_vip", "express_vip", "fina_indicator_vip",
    "fina_mainbz_vip",
]

# 仍保留非 VIP 的逐股财务
_FINANCIAL_PER_STOCK = [
    "dividend", "fina_audit",
]

# 保留但不自动同步
_RESERVED_APIS = {
    "rt_k", "rt_min", "rt_min_daily",
    "stk_auction", "stk_auction_c", "stk_auction_o",
    "stk_premarket",
}

# ══════════════════════════════════════════════════════════════════════
# 日期工具
# ══════════════════════════════════════════════════════════════════════

def _is_last_trade_day(trade_date: str, freq: str = "month") -> bool:
    """检查 trade_date 是否为当月/周最后一个交易日。"""
    conn = _get_global_conn()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            if freq == "week":
                cur.execute(
                    "SELECT MAX(cal_date) FROM ts_trade_cal WHERE is_open='1' "
                    "AND YEARWEEK(cal_date,1) = YEARWEEK(%s,1)", (trade_date,)
                )
            else:
                cur.execute(
                    "SELECT MAX(cal_date) FROM ts_trade_cal WHERE is_open='1' "
                    "AND SUBSTRING(cal_date,1,6) = SUBSTRING(%s,1,6)", (trade_date,)
                )
            row = cur.fetchone()
            return row is not None and row[0] == trade_date
    except Exception:
        return False
    finally:
        conn.close()


def _get_global_conn():
    """获取临时 MySQL 连接（用于日期查询）。"""
    try:
        from sequoia_x.core.config import get_settings
        s = get_settings()
        return pymysql.connect(
            host=s.mysql_host, port=s.mysql_port,
            user=s.mysql_user, password=s.mysql_password,
            database=s.mysql_database, charset="utf8mb4",
        )
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════════
# 同步执行器
# ══════════════════════════════════════════════════════════════════════

def _clear_trade_date(conn: pymysql.Connection, table: str, trade_date: str) -> int:
    """按 trade_date 删除旧数据，使同步幂等。

    若表无 trade_date 列（如 ts_stock_basic），静默跳过。
    调用方确保在 INSERT 新数据前调用。
    """
    try:
        with conn.cursor() as cur:
            return cur.execute(
                f"DELETE FROM `{table}` WHERE trade_date = %s", (trade_date,)
            )
    except Exception:
        return 0


def _clear_table(conn: pymysql.Connection, table: str) -> int:
    """全表清理，用于无 trade_date 列的静态参考表。"""
    try:
        with conn.cursor() as cur:
            return cur.execute(f"DELETE FROM `{table}`")
    except Exception:
        return 0


def _sync_task_list(self, tasks: list, trade_date: str) -> dict[str, int]:
    """执行一批同步任务，返回 {table: count}。

    复用同一个 DB 连接，只在与 Tushare API 间加入最小间隔以防止限流。
    """
    import time as _tm
    result: dict[str, int] = {}
    conn = self._get_conn()
    try:
        for api_method, table, rename in tasks:
            try:
                method = getattr(self.tushare, api_method)
                try:
                    df = method(trade_date=trade_date)
                except TypeError:
                    try:
                        df = method(trade_date)
                    except Exception:
                        continue
                if df is not None and not df.empty:
                    if rename:
                        df = df.rename(columns=rename)
                    _clear_trade_date(conn, table, trade_date)
                    result[table] = _write_mysql(conn, table, df)
            except Exception as exc:
                if _is_db_error(exc):
                    raise
                pass
            _tm.sleep(0.06)  # 最小间隔，HTTP 往返已提供大部分延迟
    finally:
        conn.close()
    return result


def _sync_week_month_freq(self, trade_date: str) -> dict[str, int]:
    """同步周月线表（每日调用，分别传 freq=week 和 freq=month）。"""
    import time as _tm
    result: dict[str, int] = {}
    conn = self._get_conn()
    try:
        for api_method, table, _ in _WEEK_MONTH_FREQ_APIS:
            for freq in ("week", "month"):
                try:
                    method = getattr(self.tushare, api_method)
                    df = method(trade_date=trade_date, freq=freq)
                    if df is not None and not df.empty:
                        result[table] = result.get(table, 0) + _write_mysql(conn, table, df)
                except Exception:
                    pass
            # 速率限制由 TushareProvider._call 内置的 RateLimiter 统一管理
    finally:
        conn.close()
    return result


def _sync_financial(self, trade_date: str = "") -> dict[str, int]:
    """同步财务数据（每月最后交易日）。

    分两类：
    - VIP（period 一次性取全量）
    - 逐股（ts_code 必填）
    """
    import time as _tm
    result: dict[str, int] = {}

    # ── 从交易日推算最近季度末 ──
    if not trade_date:
        trade_date = date.today().strftime("%Y%m%d")
    y, m = int(trade_date[:4]), int(trade_date[4:6])
    if m <= 3:
        period = f"{y-1}1231"
    elif m <= 6:
        period = f"{y}0331"
    elif m <= 9:
        period = f"{y}0630"
    else:
        period = f"{y}0930"

    # ── 1. VIP + 批量同步（一次性取全量）──
    for api_name in _FINANCIAL_VIP:
        method = getattr(self.tushare, f"get_{api_name}", None)
        if method is None:
            continue

        table = f"ts_{api_name.replace('_vip', '')}"
        try:
            df = method(period=period)
        except Exception:
            continue
        if df is not None and not df.empty:
            conn = self._get_conn()
            try:
                result[table] = _write_mysql(conn, table, df)
            finally:
                conn.close()
            logger.info(f"[财务] {api_name}: {len(df)} 行（全量）")
            _tm.sleep(0.3)

    # ── disclosure_date（end_date 一次返回全量）──
    try:
        df = self.tushare.get_disclosure_date(end_date=period)
        if df is not None and not df.empty:
            conn = self._get_conn()
            try:
                result["ts_disclosure_date"] = _write_mysql(conn, "ts_disclosure_date", df)
            finally:
                conn.close()
            logger.info(f"[财务] disclosure_date: {len(df)} 行（全量）")
    except Exception:
        pass
    _tm.sleep(0.3)

    # ── stk_rewards（200 个 ts_code 一组批量调用）──
    conn = self._get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT ts_code FROM ts_stock_basic")
            all_codes = [r[0] for r in cur.fetchall()]
    finally:
        conn.close()

    if all_codes:
        frames = []
        batch_size = 200
        total = len(all_codes)
        logger.info(f"[财务] stk_rewards: 批量同步 {total} 只（每批 {batch_size} 个）...")
        for i in range(0, total, batch_size):
            batch = all_codes[i:i + batch_size]
            try:
                df = self.tushare.get_stk_rewards(ts_code=",".join(batch), end_date=period)
            except Exception:
                continue
            if df is not None and not df.empty:
                frames.append(df)
            _tm.sleep(0.3)
            if (i + batch_size) % 1000 == 0:
                logger.info(f"[财务] stk_rewards: {min(i+batch_size, total)}/{total}")
        if frames:
            all_df = pd.concat(frames, ignore_index=True)
            conn = self._get_conn()
            try:
                result["ts_stk_rewards"] = _write_mysql(conn, "ts_stk_rewards", all_df)
            finally:
                conn.close()
            logger.info(f"[财务] stk_rewards: 完成 {len(frames)} 批, 写入 {len(all_df)} 行")
    _tm.sleep(0.3)

    # ── 2. 批量同步（dividend/fina_audit 支持逗号分隔 ts_code）──
    conn = self._get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT ts_code FROM ts_stock_basic")
            codes = [r[0] for r in cur.fetchall()]
    finally:
        conn.close()

    if not codes:
        logger.warning("无法获取股票列表，跳过财务同步")
        return result

    total = len(codes)
    batch_size = 200
    for api_name in _FINANCIAL_PER_STOCK:
        table = f"ts_{api_name}"
        method = getattr(self.tushare, f"get_{api_name}", None)
        if method is None:
            continue

        frames = []
        logger.info(f"[财务] {api_name}: 批量同步 {total} 只（每批 {batch_size} 个）...")
        for i in range(0, total, batch_size):
            batch = codes[i:i + batch_size]
            batch_str = ",".join(batch)
            try:
                if api_name == "dividend":
                    df = method(ts_code=batch_str, end_date=period)
                else:
                    df = method(ts_code=batch_str, period=period)
            except Exception as exc:
                if _is_db_error(exc):
                    logger.error(f"[财务] {api_name}: 数据库错误，停止同步: {exc}")
                    raise
                logger.warning(f"[财务] {api_name} batch failed at {i}: {exc}")
                continue
            if df is not None and not df.empty:
                frames.append(df)
            _tm.sleep(0.3)
            if (i + batch_size) % 2000 == 0:
                logger.info(f"[财务] {api_name}: {min(i+batch_size, total)}/{total}")
        if frames:
            all_df = pd.concat(frames, ignore_index=True)
            conn = self._get_conn()
            try:
                n = _write_mysql(conn, table, all_df)
                result[table] = n
            finally:
                conn.close()
            logger.info(f"[财务] {api_name}: 完成 {len(frames)} 批, 写入 {n} 条")
        else:
            logger.info(f"[财务] {api_name}: 无数据")

    return result


# ══════════════════════════════════════════════════════════════════════
# 补齐缺失数据
# ══════════════════════════════════════════════════════════════════════

def _ensure_recent_data(self, trade_date: str) -> dict[str, int]:
    """补齐最近 60 个交易日的缺失数据。"""
    if not self.tushare:
        logger.debug("[回填] Tushare 未启用，跳过")
        return {}
    conn = self._get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT cal_date FROM ts_trade_cal WHERE is_open='1' AND cal_date <= %s"
                " ORDER BY cal_date DESC LIMIT 60",
                (trade_date,),
            )
            target = [r[0] for r in cur.fetchall()]
    finally:
        conn.close()
    if not target:
        logger.debug("[回填] ts_trade_cal 无交易日数据，跳过")
        return {}

    logger.debug(f"[回填] 最近 60 个交易日: {target[-1]} ~ {target[0]}")

    conn = self._get_conn()
    try:
        existing: set[str] = set()
        with conn.cursor() as cur:
            cur.execute(f"SELECT DISTINCT trade_date FROM ts_daily WHERE trade_date >= '{target[-1]}'")
            existing = {r[0] for r in cur.fetchall()}
    finally:
        conn.close()

    missing = [d for d in target if d not in existing]
    logger.debug(f"[回填] ts_daily 已有 {len(existing)} 天, 缺失 {len(missing)} 天")
    if not missing:
        logger.info("[回填] 无缺失数据，跳过")
        return {}

    logger.info(f"[回填] 补齐缺失数据: {len(missing)} 个交易日 ({missing[0]}~{missing[-1]})")
    total: dict[str, int] = {}
    for idx, md in enumerate(missing):
        logger.debug(f"[回填] 同步 {md} ({idx+1}/{len(missing)})...")
        cr = _sync_task_list(self, _DAILY_APIS, md)
        for k, v in cr.items():
            total[k] = total.get(k, 0) + v
        if (idx + 1) % 10 == 0:
            logger.info(f"[回填] 进度: {idx+1}/{len(missing)}")
    return total


# ══════════════════════════════════════════════════════════════════════
# 主入口：日常同步
# ══════════════════════════════════════════════════════════════════════

def sync_today(self, trade_date: str = "") -> dict[str, int]:
    """日常同步：日线 + 周月线 + 月度/周度表 + 财务（按需）。"""
    if not trade_date:
        trade_date = date.today().strftime("%Y%m%d")
    if not self.tushare:
        return {}
    result: dict[str, int] = {}

    # 1. 每日同步
    c = _sync_task_list(self, _DAILY_APIS, trade_date)
    result.update(c)

    # 3. 周月线（每日调用，freq=week + freq=month）
    c = _sync_week_month_freq(self, trade_date)
    result.update(c)

    # 4. 周线表（每周最后交易日）
    if _is_last_trade_day(trade_date, "week"):
        logger.info(f"{trade_date} 是周最后交易日，同步周线表")
        c = _sync_task_list(self, _WEEKLY_APIS, trade_date)
        result.update(c)

    # 5. 月线 + 财务（每月最后交易日）
    if _is_last_trade_day(trade_date, "month"):
        logger.info(f"{trade_date} 是月最后交易日，同步月线 + 财务表")
        c = _sync_task_list(self, _MONTHLY_APIS, trade_date)
        result.update(c)
        c = _sync_financial(self)
        result.update(c)

    logger.info(f"sync_today({trade_date}): {dict(sorted(result.items()))}")
    return result


# ── 回填 ──

def backfill_tushare(self, start: str = "") -> dict[str, int]:
    """回填最近 60 个交易日缺失的数据。

    Args:
        start: 回填起始日期 (YYYYMMDD)。为空时自动计算：最近交易日前 60 个交易日。
    """
    if not self.tushare:
        logger.warning("[回填] Tushare 未启用")
        return {}

    # 计算动态起始日期
    if not start:
        start = _compute_backfill_start(self)
        logger.info(f"[回填] 自动计算起始日期: {start}")
    else:
        start = start.replace("-", "")
        logger.info(f"[回填] 指定起始日期: {start}")

    # 初始化基础数据
    logger.debug("[回填] 初始化 stock_basic...")
    _init_tushare_basics(self)

    logger.debug(f"[回填] 初始化 trade_cal ({start} ~ {date.today().strftime('%Y%m%d')})...")
    _init_tushare_trade_cal(self, start, date.today().strftime("%Y%m%d"))

    logger.info(f"[回填] 开始 60 交易日数据补齐 (起始: {start})...")
    result = _ensure_recent_data(self, date.today().strftime("%Y%m%d"))
    logger.info(f"[回填] 完成: {dict(sorted(result.items()))}")
    return result


def _compute_backfill_start(self) -> str:
    """计算回填起始日期：最近交易日前推 60 个交易日。

    优先从本地 ts_trade_cal 查询，若无数据则以今日前 90 个自然日兜底。
    """
    from datetime import date as dt, timedelta

    # 尝试从已有 trade_cal 计算
    try:
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                today = dt.today().strftime("%Y%m%d")
                cur.execute(
                    "SELECT COUNT(*) FROM ts_trade_cal"
                    " WHERE is_open='1' AND cal_date <= %s", (today,)
                )
                if cur.fetchone()[0] >= 60:
                    cur.execute(
                        "SELECT cal_date FROM ts_trade_cal"
                        " WHERE is_open='1' AND cal_date <= %s"
                        " ORDER BY cal_date DESC LIMIT 60", (today,)
                    )
                    dates = [r[0] for r in cur.fetchall()]
                    if dates:
                        start = dates[-1]
                        logger.debug(
                            f"[回填] 从 trade_cal 推算: 最近 60 交易日 "
                            f"{dates[-1]} ~ {dates[0]}, 起始={start}"
                        )
                        return start
        finally:
            conn.close()
    except Exception as exc:
        logger.debug(f"[回填] 从 trade_cal 推算失败: {exc}")

    # 兜底：今日前 90 个自然日（约覆盖 60 个交易日）
    fallback = (dt.today() - timedelta(days=90)).strftime("%Y%m%d")
    logger.debug(f"[回填] 日历兜底起始: {fallback}")
    return fallback


def _init_tushare_basics(self) -> None:
    conn = self._get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM ts_stock_basic")
            cnt = cur.fetchone()[0]
            if cnt > 0:
                logger.debug(f"[回填] stock_basic 已有 {cnt} 条, 跳过")
                return
    finally:
        conn.close()
    logger.debug("[回填] stock_basic 为空, 从 Tushare 拉取...")
    df = self.tushare.get_stock_basic()
    if not df.empty:
        conn = self._get_conn()
        try:
            n = _write_mysql(conn, "ts_stock_basic", df)
            logger.debug(f"[回填] stock_basic 写入 {n} 条")
        finally:
            conn.close()


def _init_tushare_trade_cal(self, start: str, end: str) -> None:
    conn = self._get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM ts_trade_cal")
            cnt = cur.fetchone()[0]
            if cnt > 20:
                logger.debug(f"[回填] trade_cal 已有 {cnt} 条, 跳过")
                return
    finally:
        conn.close()
    logger.debug(f"[回填] trade_cal 不足, 从 Tushare 拉取 ({start}~{end})...")
    df = self.tushare.get_trade_cal(start, end)
    if not df.empty:
        conn = self._get_conn()
        try:
            n = _write_mysql(conn, "ts_trade_cal", df)
            logger.debug(f"[回填] trade_cal 写入 {n} 条")
        finally:
            conn.close()


# ── 单表同步 ──

def sync_table(self, table_name: str, trade_date: str = "") -> int:
    """同步任意 ts_ 表。根据 API 类型自动选择参数策略。"""
    if not self.tushare:
        logger.error("Tushare 未启用")
        return 0
    if not trade_date:
        trade_date = date.today().strftime("%Y%m%d")

    # 自动补 ts_ 前缀
    if not table_name.startswith("ts_"):
        table_name = f"ts_{table_name}"

    api_name = table_name.replace("ts_", "")

    # 保留接口：不同步
    if api_name in _RESERVED_APIS:
        logger.info(f"[{table_name}] 保留接口，跳过同步")
        return 0

    logger.info(f"单表同步 [{table_name}] via {api_name} ({trade_date})...")

    # ── 参数策略 ──
    _MONTH_APIS = {"broker_recommend"}
    _PER_STOCK_APIS = {"cyq_chips", "cyq_perf"} | set(_FINANCIAL_PER_STOCK)
    _POSITIONAL_APIS = {
        "stock_basic", "trade_cal", "concept", "concept_detail",
        "namechange", "hs_const", "new_share", "bak_basic", "bse_mapping",
        "stk_account", "stk_account_old", "stock_hsgt", "hm_list",
        "ths_index", "ths_member", "tdx_index", "dc_index",
    }

    # ── 获取股票列表（供逐股循环使用）──
    def _get_codes(engine) -> list[str]:
        conn = engine._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT ts_code FROM ts_stock_basic")
                return [r[0] for r in cur.fetchall()]
        except Exception:
            return []
        finally:
            conn.close()

    # 检查 provider 是否有对应方法
    df = pd.DataFrame()
    method = getattr(self.tushare, f"get_{api_name}", None)
    if method:
        if api_name in _MONTH_APIS:
            df = method(month=trade_date[:6])
        elif api_name in _POSITIONAL_APIS:
            try:
                df = method()
            except Exception:
                pass
        elif api_name in _PER_STOCK_APIS:
            # ── 逐股循环同步 ──
            codes = _get_codes(self)
            if not codes:
                logger.warning(f"[{table_name}] 无法获取股票列表")
                return 0
            frames = []
            total_codes = len(codes)
            logger.info(f"[{table_name}] 逐股同步 {total_codes} 只股票...")
            for idx, ts_code in enumerate(codes):
                try:
                    chunk = method(ts_code=ts_code, trade_date=trade_date)
                except TypeError:
                    try:
                        chunk = method(ts_code=ts_code)
                    except Exception:
                        continue
                except Exception:
                    continue
                if chunk is not None and not chunk.empty:
                    frames.append(chunk)
                if (idx + 1) % 500 == 0:
                    logger.info(f"[{table_name}] 进度: {idx + 1}/{total_codes}")
                if (idx + 1) % 100 == 0:
                    import time as _t
                    _t.sleep(0.05)  # 控制 API 调用频率
            if frames:
                df = pd.concat(frames, ignore_index=True)
            logger.info(f"[{table_name}] 逐股完成: {len(frames)} 只有数据")
        else:
            try:
                df = method(trade_date=trade_date)
            except TypeError:
                try:
                    df = method(trade_date)
                except Exception:
                    try:
                        df = method()
                    except Exception:
                        pass

    # 无 provider 方法，通过 SDK _call 直调
    if df.empty and api_name not in _PER_STOCK_APIS:
        if api_name in _MONTH_APIS:
            df = self.tushare._call(api_name, month=trade_date[:6])
        else:
            try:
                df = self.tushare._call(api_name, trade_date=trade_date)
            except Exception:
                df = pd.DataFrame()

    if df.empty:
        logger.info(f"[{table_name}] 无数据或API不支持")
        return 0

    conn = self._get_conn()
    try:
        if api_name in _POSITIONAL_APIS:
            # 静态参考表：全表替换
            _clear_table(conn, table_name)
        else:
            # 日频/财务表：按 trade_date 清理
            _clear_trade_date(conn, table_name, trade_date)
        count = _write_mysql(conn, table_name, df)
    finally:
        conn.close()
    logger.info(f"[{table_name}] 写入 {count} 条")
    return count


# ── 注册 ──

from sequoia_x.data.mysql_engine import MySQLEngine

MySQLEngine._sync_task_list = _sync_task_list
MySQLEngine._sync_week_month_freq = _sync_week_month_freq
MySQLEngine._sync_financial = _sync_financial
MySQLEngine._ensure_recent_data = _ensure_recent_data
MySQLEngine.sync_today = sync_today
MySQLEngine.sync_table = sync_table
MySQLEngine.backfill_tushare = backfill_tushare
