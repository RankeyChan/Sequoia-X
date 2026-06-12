"""数据引擎：baostock K线 + Tushare 增强数据。"""

import sqlite3
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from sequoia_x.core.config import Settings
from sequoia_x.core.logger import get_logger
from sequoia_x.data.tushare_provider import TushareProvider

logger = get_logger(__name__)

_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS stock_daily (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol   TEXT    NOT NULL,
    date     TEXT    NOT NULL,
    open     REAL,
    high     REAL,
    low      REAL,
    close    REAL,
    volume   REAL,
    turnover REAL,
    UNIQUE (symbol, date)
);
"""
_CREATE_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_symbol_date ON stock_daily (symbol, date);
"""

# 所有 Tushare 表
_TABLES_SQL = []

def _add_table(sql):
    _TABLES_SQL.append(sql)

# 按创建顺序添加所有 Tushare 表
_add_table("CREATE TABLE IF NOT EXISTS stock_basic (symbol TEXT PRIMARY KEY, name TEXT, industry TEXT, area TEXT, list_date TEXT, market TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS daily_basic (symbol TEXT NOT NULL, date TEXT NOT NULL, close REAL, pe REAL, pe_ttm REAL, pb REAL, total_mv REAL, circ_mv REAL, turnover_rate REAL, volume_ratio REAL, dv_ratio REAL, dv_ttm REAL, total_share REAL, float_share REAL, free_share REAL, UNIQUE (symbol, date))")
_add_table("CREATE TABLE IF NOT EXISTS moneyflow (symbol TEXT NOT NULL, date TEXT NOT NULL, buy_sm_vol REAL, buy_sm_amount REAL, sell_sm_vol REAL, sell_sm_amount REAL, buy_md_vol REAL, buy_md_amount REAL, sell_md_vol REAL, sell_md_amount REAL, buy_lg_vol REAL, buy_lg_amount REAL, sell_lg_vol REAL, sell_lg_amount REAL, buy_elg_vol REAL, buy_elg_amount REAL, sell_elg_vol REAL, sell_elg_amount REAL, net_mf_vol REAL, net_mf_amount REAL, UNIQUE (symbol, date))")
_add_table("CREATE TABLE IF NOT EXISTS limit_list (symbol TEXT NOT NULL, date TEXT NOT NULL, name TEXT, industry TEXT, limit_type TEXT, close REAL, pct_chg REAL, amount REAL, limit_amount REAL, float_mv REAL, total_mv REAL, turnover_ratio REAL, fd_amount REAL, first_time TEXT, last_time TEXT, open_times INTEGER, limit_times INTEGER, up_stat TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS hk_hold (symbol TEXT NOT NULL, date TEXT NOT NULL, name TEXT, vol INTEGER, ratio REAL, exchange TEXT, UNIQUE (symbol, date))")
_add_table("CREATE TABLE IF NOT EXISTS top_list (symbol TEXT NOT NULL, date TEXT NOT NULL, name TEXT, close REAL, pct_change REAL, turnover_rate REAL, amount REAL, l_sell REAL, l_buy REAL, l_amount REAL, net_amount REAL, net_rate REAL, amount_rate REAL, float_values REAL, reason TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS top_inst (symbol TEXT NOT NULL, date TEXT NOT NULL, exalter TEXT, side TEXT, buy REAL, buy_rate REAL, sell REAL, sell_rate REAL, net_buy REAL, reason TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS margin_detail (symbol TEXT NOT NULL, date TEXT NOT NULL, name TEXT, rzye REAL, rqye REAL, rzmre REAL, rqyl REAL, rzche REAL, rqchl REAL, rqmcl REAL, rzrqye REAL, UNIQUE (symbol, date))")
_add_table("CREATE TABLE IF NOT EXISTS trade_cal (cal_date TEXT PRIMARY KEY, is_open INTEGER, pretrade_date TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS fina_indicator (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, eps REAL, dt_eps REAL, roe REAL, roa REAL, grossprofit_margin REAL, netprofit_margin REAL, debt_to_assets REAL, current_ratio REAL, quick_ratio REAL, or_yoy REAL, netprofit_yoy REAL, basic_eps_yoy REAL, profit_dedt REAL, op_income REAL, bps REAL, ocqps REAL, update_flag TEXT, UNIQUE (symbol, end_date))")
_add_table("CREATE TABLE IF NOT EXISTS income (symbol TEXT NOT NULL, ann_date TEXT, f_ann_date TEXT, end_date TEXT NOT NULL, report_type TEXT, basic_eps REAL, diluted_eps REAL, total_revenue REAL, revenue REAL, operate_profit REAL, total_profit REAL, n_income REAL, n_income_attr_p REAL, ebit REAL, ebitda REAL, total_cogs REAL, rd_exp REAL, update_flag TEXT, UNIQUE (symbol, end_date, report_type))")
_add_table("CREATE TABLE IF NOT EXISTS balancesheet (symbol TEXT NOT NULL, ann_date TEXT, f_ann_date TEXT, end_date TEXT NOT NULL, report_type TEXT, total_assets REAL, total_liab REAL, total_hldr_eqy_exc_min_int REAL, total_cur_assets REAL, total_nca REAL, total_cur_liab REAL, total_ncl REAL, money_cap REAL, accounts_receiv REAL, inventories REAL, fix_assets REAL, intan_assets REAL, r_and_d REAL, goodwill REAL, lt_borr REAL, st_borr REAL, notes_payable REAL, acct_payable REAL, defer_tax_assets REAL, defer_tax_liab REAL, update_flag TEXT, UNIQUE (symbol, end_date, report_type))")
_add_table("CREATE TABLE IF NOT EXISTS cashflow (symbol TEXT NOT NULL, ann_date TEXT, f_ann_date TEXT, end_date TEXT NOT NULL, report_type TEXT, net_profit REAL, n_cashflow_act REAL, n_cashflow_inv_act REAL, n_cash_flows_fnc_act REAL, free_cashflow REAL, c_cash_equ_beg_period REAL, c_cash_equ_end_period REAL, update_flag TEXT, UNIQUE (symbol, end_date, report_type))")
_add_table("CREATE TABLE IF NOT EXISTS forecast (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, type TEXT, p_change_min REAL, p_change_max REAL, net_profit_min REAL, net_profit_max REAL, summary TEXT, change_reason TEXT, UNIQUE (symbol, end_date))")
_add_table("CREATE TABLE IF NOT EXISTS express (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, revenue REAL, operate_profit REAL, total_profit REAL, n_income REAL, diluted_eps REAL, yoy_net_profit REAL, bps REAL, yoy_sales REAL, perf_summary TEXT, UNIQUE (symbol, end_date))")
_add_table("CREATE TABLE IF NOT EXISTS dividend (symbol TEXT NOT NULL, end_date TEXT, ann_date TEXT, div_proc TEXT, stk_div REAL, stk_bo_rate REAL, cash_div REAL, cash_div_tax REAL, ex_date TEXT, pay_date TEXT, imp_ann_date TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS stk_holdertrade (symbol TEXT NOT NULL, ann_date TEXT, holder_name TEXT, holder_type TEXT, in_de TEXT, change_vol REAL, change_ratio REAL, after_share REAL, avg_price REAL, total_share REAL, begin_date TEXT, close_date TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS stk_holdernumber (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, holder_num INTEGER, UNIQUE (symbol, end_date))")
_add_table("CREATE TABLE IF NOT EXISTS pledge_stat (symbol TEXT NOT NULL, end_date TEXT NOT NULL, pledge_count INTEGER, unrest_pledge REAL, rest_pledge REAL, total_share REAL, pledge_ratio REAL, UNIQUE (symbol, end_date))")
_add_table("CREATE TABLE IF NOT EXISTS share_float (symbol TEXT NOT NULL, ann_date TEXT, float_date TEXT NOT NULL, float_share REAL, float_ratio REAL, holder_name TEXT, share_type TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS block_trade (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, price REAL, vol REAL, amount REAL, buyer TEXT, seller TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS repurchase (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT, proc TEXT, vol REAL, amount REAL, high_limit REAL, low_limit REAL)")
_add_table("CREATE TABLE IF NOT EXISTS concept (code TEXT PRIMARY KEY, name TEXT, src TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS concept_detail (id TEXT NOT NULL, concept_name TEXT, symbol TEXT NOT NULL, name TEXT, in_date TEXT, out_date TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS broker_recommend (month TEXT NOT NULL, broker TEXT, symbol TEXT NOT NULL, name TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS adj_factor (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, adj_factor REAL, UNIQUE (symbol, trade_date))")
_add_table("CREATE TABLE IF NOT EXISTS moneyflow_hsgt (trade_date TEXT PRIMARY KEY, ggt_ss REAL, ggt_sz REAL, hgt REAL, sgt REAL, north_money REAL, south_money REAL)")
_add_table("CREATE TABLE IF NOT EXISTS stk_limit (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, up_limit REAL, down_limit REAL, pre_close REAL, UNIQUE (symbol, trade_date))")
_add_table("CREATE TABLE IF NOT EXISTS cyq_perf (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, his_low REAL, his_high REAL, cost_5pct REAL, cost_50pct REAL, cost_95pct REAL, weight_avg REAL, winner_rate REAL, UNIQUE (symbol, trade_date))")
_add_table("CREATE TABLE IF NOT EXISTS hsgt_top10 (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, close REAL, change REAL, rank INTEGER, market_type INTEGER, amount REAL, net_amount REAL)")
_add_table("CREATE TABLE IF NOT EXISTS top10_holders (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, holder_name TEXT, hold_amount REAL, hold_ratio REAL, hold_change REAL, holder_type TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS suspen_d (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, suspend_timing TEXT, suspend_type TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS namechange (symbol TEXT, name TEXT, start_date TEXT, end_date TEXT, ann_date TEXT, change_reason TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS hs_const (symbol TEXT NOT NULL, hs_type TEXT, in_date TEXT, out_date TEXT, is_new TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS stk_factor (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, macd_dif REAL, macd_dea REAL, macd REAL, kdj_k REAL, kdj_d REAL, kdj_j REAL, rsi_6 REAL, rsi_12 REAL, rsi_24 REAL, UNIQUE (symbol, trade_date))")
_add_table("CREATE TABLE IF NOT EXISTS index_weight (index_code TEXT NOT NULL, symbol TEXT NOT NULL, trade_date TEXT NOT NULL, weight REAL)")

# 新增补充表
_add_table("CREATE TABLE IF NOT EXISTS stock_st (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, type TEXT, type_name TEXT, UNIQUE (symbol, trade_date))")
_add_table("CREATE TABLE IF NOT EXISTS stk_premarket (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, total_share REAL, float_share REAL, pre_close REAL, up_limit REAL, down_limit REAL, UNIQUE (symbol, trade_date))")
_add_table("CREATE TABLE IF NOT EXISTS margin (trade_date TEXT PRIMARY KEY, exchange_id TEXT, rzye REAL, rzmre REAL, rzche REAL, rqye REAL, rqmcl REAL, rzrqye REAL, rqyl REAL)")
_add_table("CREATE TABLE IF NOT EXISTS stk_shock (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, trade_market TEXT, reason TEXT, period TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS stk_high_shock (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, trade_market TEXT, reason TEXT, period TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS stk_auction_o (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, vol REAL, price REAL, amount REAL, pre_close REAL, turnover_rate REAL, volume_ratio REAL, UNIQUE (symbol, trade_date))")
_add_table("CREATE TABLE IF NOT EXISTS stk_auction_c (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, close REAL, open REAL, high REAL, low REAL, vol REAL, amount REAL, vwap REAL, UNIQUE (symbol, trade_date))")
_add_table("CREATE TABLE IF NOT EXISTS stock_company (symbol TEXT PRIMARY KEY, com_name TEXT, exchange TEXT, chairman TEXT, manager TEXT, reg_capital REAL, setup_date TEXT, province TEXT, city TEXT, website TEXT, employees INTEGER, main_business TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS stk_nineturn (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, freq TEXT, up_count INTEGER, down_count INTEGER, nine_up_turn INTEGER, nine_down_turn INTEGER, UNIQUE (symbol, trade_date, freq))")
_add_table("CREATE TABLE IF NOT EXISTS stk_ah_comparison (symbol TEXT NOT NULL, hk_code TEXT, trade_date TEXT NOT NULL, name TEXT, hk_name TEXT, close REAL, hk_close REAL, ah_premium REAL)")
_add_table("CREATE TABLE IF NOT EXISTS ccass_hold (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, shareholding REAL, hold_nums REAL, hold_ratio REAL, UNIQUE (symbol, trade_date))")
_add_table("CREATE TABLE IF NOT EXISTS report_rc (symbol TEXT NOT NULL, report_date TEXT NOT NULL, report_title TEXT, org_name TEXT, eps REAL, pe REAL, roe REAL, rating TEXT, max_price REAL, min_price REAL, UNIQUE (symbol, report_date, org_name))")
_add_table("CREATE TABLE IF NOT EXISTS stk_managers (symbol TEXT NOT NULL, ann_date TEXT, name TEXT, gender TEXT, title TEXT, edu TEXT, begin_date TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS fina_mainbz (symbol TEXT NOT NULL, end_date TEXT NOT NULL, bz_item TEXT, bz_sales REAL, bz_profit REAL, bz_cost REAL)")
_add_table("CREATE TABLE IF NOT EXISTS disclosure_date (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, pre_date TEXT, actual_date TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS stock_hsgt (symbol TEXT NOT NULL, name TEXT, type TEXT, type_name TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS new_share (symbol TEXT NOT NULL, name TEXT, ipo_date TEXT, issue_date TEXT, amount REAL, price REAL, pe REAL, limit_amount REAL, ballot REAL)")
_add_table("CREATE TABLE IF NOT EXISTS margin_secs (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, exchange TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS pledge_detail (symbol TEXT NOT NULL, ann_date TEXT, holder_name TEXT, pledge_amount REAL, start_date TEXT, end_date TEXT, is_release TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS stk_alert (symbol TEXT NOT NULL, start_date TEXT NOT NULL, end_date TEXT NOT NULL, type TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS limit_list_ths (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, price REAL, pct_chg REAL, limit_type TEXT, tag TEXT, status TEXT, turnover_rate REAL)")
_add_table("CREATE TABLE IF NOT EXISTS limit_step (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, nums INTEGER)")
_add_table("CREATE TABLE IF NOT EXISTS limit_cpt_list (ts_code TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, up_nums INTEGER, cons_nums INTEGER, pct_chg REAL, rank INTEGER)")
_add_table("CREATE TABLE IF NOT EXISTS stk_auction (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, vol REAL, price REAL, amount REAL, pre_close REAL, turnover_rate REAL, volume_ratio REAL)")
_add_table("CREATE TABLE IF NOT EXISTS ths_index (ts_code TEXT PRIMARY KEY, name TEXT, count INTEGER, type TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS ths_member (ts_code TEXT NOT NULL, con_code TEXT NOT NULL, con_name TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS hm_list (name TEXT PRIMARY KEY, desc TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS hm_detail (trade_date TEXT NOT NULL, ts_code TEXT, ts_name TEXT, buy_amount REAL, sell_amount REAL, net_amount REAL, hm_name TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS ths_hot (trade_date TEXT NOT NULL, ts_code TEXT, ts_name TEXT, rank INTEGER, pct_change REAL, hot REAL)")
_add_table("CREATE TABLE IF NOT EXISTS dc_index (ts_code TEXT NOT NULL, name TEXT, idx_type TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS tdx_index (ts_code TEXT NOT NULL, name TEXT, idx_type TEXT, idx_count INTEGER)")
_add_table("CREATE TABLE IF NOT EXISTS st (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, type TEXT, type_name TEXT, UNIQUE (symbol, trade_date))")
_add_table("CREATE TABLE IF NOT EXISTS bse_mapping (n_code TEXT, o_code TEXT, name TEXT, list_date TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS bak_basic (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, name TEXT, industry TEXT, pe REAL, float_share REAL, total_share REAL, total_assets REAL, liquid_assets REAL, fixed_assets REAL, eps REAL, bvps REAL, pb REAL, list_date TEXT, UNIQUE (trade_date, ts_code))")
_add_table("CREATE TABLE IF NOT EXISTS ggt_top10 (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, name TEXT, close REAL, amount REAL, market_type INTEGER, rank INTEGER)")
_add_table("CREATE TABLE IF NOT EXISTS ggt_daily (trade_date TEXT PRIMARY KEY, buy_amount REAL, sell_amount REAL, buy_volume REAL, sell_volume REAL)")
_add_table("CREATE TABLE IF NOT EXISTS ccass_hold_detail (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, name TEXT, col_participant_id TEXT, col_participant_name TEXT, col_shareholding REAL, col_shareholding_percent REAL)")
_add_table("CREATE TABLE IF NOT EXISTS slb_sec (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, name TEXT, ope_inv REAL, lent_qnt REAL, cls_inv REAL, end_bal REAL)")
_add_table("CREATE TABLE IF NOT EXISTS slb_len (trade_date TEXT PRIMARY KEY, ob REAL, auc_amount REAL, repo_amount REAL, repay_amount REAL, cb REAL)")
_add_table("CREATE TABLE IF NOT EXISTS moneyflow_ths (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, pct_change REAL, latest REAL, net_amount REAL, buy_lg_amount REAL, buy_sm_amount REAL)")
_add_table("CREATE TABLE IF NOT EXISTS moneyflow_dc (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, pct_change REAL, close REAL, net_amount REAL, buy_lg_amount REAL, buy_elg_amount REAL)")
_add_table("CREATE TABLE IF NOT EXISTS moneyflow_cnt_ths (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, pct_change REAL, net_amount REAL)")
_add_table("CREATE TABLE IF NOT EXISTS moneyflow_ind_ths (trade_date TEXT NOT NULL, ts_code TEXT, industry TEXT, pct_change REAL, net_amount REAL)")
_add_table("CREATE TABLE IF NOT EXISTS moneyflow_ind_dc (trade_date TEXT NOT NULL, content_type TEXT, ts_code TEXT, name TEXT, pct_change REAL, net_amount REAL)")
_add_table("CREATE TABLE IF NOT EXISTS moneyflow_mkt_dc (trade_date TEXT PRIMARY KEY, close_sh REAL, pct_change_sh REAL, close_sz REAL, pct_change_sz REAL, net_amount REAL, net_amount_rate REAL)")
_add_table("CREATE TABLE IF NOT EXISTS ths_daily (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, close REAL, pct_change REAL, vol REAL, turnover_rate REAL)")
_add_table("CREATE TABLE IF NOT EXISTS dc_member (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, con_code TEXT NOT NULL, name TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS dc_daily (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, close REAL, pct_change REAL, vol REAL)")
_add_table("CREATE TABLE IF NOT EXISTS dc_hot (trade_date TEXT NOT NULL, ts_code TEXT, ts_name TEXT, rank INTEGER, pct_change REAL)")
_add_table("CREATE TABLE IF NOT EXISTS tdx_member (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, con_code TEXT NOT NULL, con_name TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS tdx_daily (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, close REAL, pct_change REAL, vol REAL)")
_add_table("CREATE TABLE IF NOT EXISTS kpl_list (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, pct_chg REAL, tag TEXT, lu_time TEXT, status TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS kpl_concept_cons (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, name TEXT, con_code TEXT NOT NULL, con_name TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS dc_concept (trade_date TEXT NOT NULL, theme_code TEXT NOT NULL, name TEXT, pct_change REAL, hot REAL)")
_add_table("CREATE TABLE IF NOT EXISTS dc_concept_cons (trade_date TEXT NOT NULL, theme_code TEXT NOT NULL, ts_code TEXT NOT NULL, name TEXT, reason TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS fina_audit (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, audit_result TEXT, audit_fees REAL, audit_agency TEXT, audit_sign TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS stk_rewards (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, name TEXT, title TEXT, reward REAL, hold_vol REAL)")
_add_table("CREATE TABLE IF NOT EXISTS stk_surv (symbol TEXT NOT NULL, surv_date TEXT NOT NULL, fund_visitors REAL, rece_place TEXT, rece_mode TEXT, rece_org TEXT, org_type TEXT)")
_add_table("CREATE TABLE IF NOT EXISTS top10_floatholders (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, holder_name TEXT, hold_amount REAL, hold_ratio REAL, hold_change REAL, holder_type TEXT)")


def _bs_fetch_batch(tasks: list) -> list:
    import baostock as bs
    bs.login()
    results = []
    for symbol, bs_code, start, end in tasks:
        rs = bs.query_history_k_data_plus(bs_code, "date,open,high,low,close,volume,amount",
                                           start_date=start, end_date=end, frequency="d", adjustflag="1")
        if rs.error_code != "0":
            continue
        while rs.next():
            results.append([symbol] + rs.get_row_data())
    bs.logout()
    return results


class DataEngine:
    def __init__(self, settings):
        self.db_path = settings.db_path
        self.start_date = settings.start_date
        self.settings = settings
        self.target_date = ""
        self._init_db()
        self.tushare = None
        if settings.tushare_token:
            self.tushare = TushareProvider(token=settings.tushare_token, proxy_url=settings.tushare_proxy_url)
            logger.info("Tushare 已启用")

    def _init_db(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(_CREATE_TABLE_SQL)
            conn.execute(_CREATE_INDEX_SQL)
            for tsql in _TABLES_SQL:
                conn.execute(tsql)
            conn.commit()
        logger.info(f"数据库初始化完成: {self.db_path}")

    def _get_last_date(self, symbol):
        with sqlite3.connect(self.db_path) as conn:
            r = conn.execute("SELECT MAX(date) FROM stock_daily WHERE symbol=?", (symbol,)).fetchone()
        return r[0] if r and r[0] else None

    def get_ohlcv(self, symbol):
        with sqlite3.connect(self.db_path) as conn:
            if self.target_date:
                df = pd.read_sql("SELECT * FROM stock_daily WHERE symbol=? AND date<=? ORDER BY date", conn, params=(symbol, self.target_date))
            else:
                df = pd.read_sql("SELECT * FROM stock_daily WHERE symbol=? ORDER BY date", conn, params=(symbol,))
        return df

    def get_local_symbols(self):
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT DISTINCT symbol FROM stock_daily").fetchall()
        return [r[0] for r in rows]

    def is_trading_day(self, trade_date=""):
        target = trade_date or date.today().strftime("%Y%m%d")
        try:
            with sqlite3.connect(self.db_path) as conn:
                r = conn.execute("SELECT is_open FROM trade_cal WHERE cal_date=?", (target,)).fetchone()
            if r is not None:
                return r[0] == 1
            if self.tushare:
                df = self.tushare.get_trade_cal(target, target)
                if not df.empty and "is_open" in df.columns:
                    cols = ["cal_date", "is_open", "pretrade_date"]
                    df = df[[c for c in cols if c in df.columns]]
                    self._upsert_df("trade_cal", df, primary_key="cal_date")
                    return int(df.iloc[0]["is_open"]) == 1
        except: pass
        return True

    def _sync_one_day(self, trade_date: str) -> dict[str, int]:
        """同步单日所有日频表数据。"""
        import time as _tm
        c = {}

        df = self.tushare.get_daily(trade_date=trade_date)
        if not df.empty:
            df = df.rename(columns={"trade_date": "date", "vol": "volume", "amount": "turnover"})
            df = self._drop_ts_code(df)
            c["stock_daily"] = self._upsert_df("stock_daily", df)
        _tm.sleep(0.15)

        df = self.tushare.get_daily_basic(trade_date)
        if not df.empty:
            df = df.rename(columns={"trade_date": "date"})
            df = self._drop_ts_code(df)
            c["daily_basic"] = self._upsert_df("daily_basic", df)
        _tm.sleep(0.15)

        df = self.tushare.get_moneyflow(trade_date)
        if not df.empty:
            df = df.rename(columns={"trade_date": "date"})
            df = self._drop_ts_code(df)
            c["moneyflow"] = self._upsert_df("moneyflow", df)
        _tm.sleep(0.15)

        df = self.tushare.get_limit_list(trade_date)
        if not df.empty:
            df = df.rename(columns={"trade_date": "date", "limit": "limit_type"})
            df = self._drop_ts_code(df)
            c["limit_list"] = self._upsert_df("limit_list", df, primary_key="")

        df = self.tushare.get_top_list(trade_date)
        if not df.empty:
            df = df.rename(columns={"trade_date": "date"})
            df = self._drop_ts_code(df)
            c["top_list"] = self._upsert_df("top_list", df, primary_key="")

        df = self.tushare.get_margin_detail(trade_date)
        if not df.empty:
            df = df.rename(columns={"trade_date": "date"})
            df = self._drop_ts_code(df)
            c["margin_detail"] = self._upsert_df("margin_detail", df)
        _tm.sleep(0.15)

        df = self.tushare.get_block_trade(trade_date=trade_date)
        if not df.empty:
            df = self._drop_ts_code(df)
            c["block_trade"] = self._upsert_df("block_trade", df, primary_key="")

        df = self.tushare.get_adj_factor(trade_date=trade_date)
        if not df.empty:
            df = self._drop_ts_code(df)
            c["adj_factor"] = self._upsert_df("adj_factor", df, primary_key="symbol, trade_date")
        _tm.sleep(0.15)

        df = self.tushare.get_stk_limit(trade_date=trade_date)
        if not df.empty:
            df = self._drop_ts_code(df)
            c["stk_limit"] = self._upsert_df("stk_limit", df, primary_key="symbol, trade_date")

        df = self.tushare.get_hsgt_top10(trade_date)
        if not df.empty:
            df = self._drop_ts_code(df)
            c["hsgt_top10"] = self._upsert_df("hsgt_top10", df, primary_key="")

        df = self.tushare.get_moneyflow_hsgt(trade_date=trade_date)
        if not df.empty:
            c["moneyflow_hsgt"] = self._upsert_df("moneyflow_hsgt", df, primary_key="trade_date")

        return c

    def _ensure_recent_data(self, trade_date: str) -> dict[str, int]:
        """确保所有日频表有最近 60 个交易日的数据。

        以 stock_daily 为基准表，找出缺失的交易日并逐一补全。
        """
        if not self.tushare:
            return {}

        # 获取最近 60 个交易日
        try:
            with sqlite3.connect(self.db_path) as conn:
                target_dates = [r[0] for r in conn.execute(
                    "SELECT cal_date FROM trade_cal WHERE is_open=1 ORDER BY cal_date DESC LIMIT 60"
                ).fetchall()]
        except Exception:
            return {}

        if not target_dates:
            return {}

        # 检查 stock_daily 有哪些交易日缺失
        try:
            with sqlite3.connect(self.db_path) as conn:
                existing = {r[0] for r in conn.execute(
                    "SELECT DISTINCT date FROM stock_daily WHERE date >= ?",
                    (target_dates[-1],),
                ).fetchall()}
        except Exception:
            existing = set()

        missing = [d for d in target_dates if d not in existing]
        if not missing:
            return {}

        logger.info(f"补齐缺失数据: {len(missing)} 个交易日 ({missing[0]} ~ {missing[-1]})")
        total = {}
        for md in missing:
            cr = self._sync_one_day(md)
            for k, v in cr.items():
                total[k] = total.get(k, 0) + v
        logger.info(f"补齐完成: {dict(sorted(total.items()))}")
        return total

    def sync_today(self, trade_date=""):
        """全量同步：补齐缺失数据 + 同步当天。"""
        if not trade_date:
            trade_date = date.today().strftime("%Y%m%d")
        if not self.tushare:
            return {}

        c = self._ensure_recent_data(trade_date)
        today_c = self._sync_one_day(trade_date)
        for k, v in today_c.items():
            c[k] = c.get(k, 0) + v

        self._cleanup_old_data()
        logger.info(f"sync_today({trade_date}): {dict(sorted(c.items()))}")
        return c

    # ── 单表同步 ──

    _TABLE_API_MAP = {
        "stock_daily": ("get_daily", {"trade_date": "date"}),
        "daily_basic": ("get_daily_basic", {"trade_date": "date"}),
        "moneyflow": ("get_moneyflow", {"trade_date": "date"}),
        "limit_list": ("get_limit_list", {"trade_date": "date", "limit": "limit_type"}),
        "hk_hold": ("get_hk_hold", {"trade_date": "date"}),
        "top_list": ("get_top_list", {"trade_date": "date"}),
        "top_inst": ("get_top_inst", {"trade_date": "date"}),
        "margin_detail": ("get_margin_detail", {"trade_date": "date"}),
        "moneyflow_hsgt": ("get_moneyflow_hsgt", {}),
        "block_trade": ("get_block_trade", {}),
        "adj_factor": ("get_adj_factor", {}),
        "stk_limit": ("get_stk_limit", {}),
        "suspen_d": ("get_suspen_d", {}),
        "hsgt_top10": ("get_hsgt_top10", {}),
        # 补充表
        "stk_shock": ("get_stk_shock", {}),
        "stk_high_shock": ("get_stk_high_shock", {}),
        "stk_premarket": ("get_stk_premarket", {}),
        "stk_auction_o": ("get_stk_auction_o", {}),
        "stk_auction_c": ("get_stk_auction_c", {}),
        "moneyflow_ths": ("get_moneyflow_ths", {}),
        "moneyflow_dc": ("get_moneyflow_dc", {}),
        "moneyflow_cnt_ths": ("get_moneyflow_cnt_ths", {}),
        "moneyflow_ind_ths": ("get_moneyflow_ind_ths", {}),
        "moneyflow_ind_dc": ("get_moneyflow_ind_dc", {}),
        "moneyflow_mkt_dc": ("get_moneyflow_mkt_dc", {}),
        "ths_daily": ("get_ths_daily", {}),
        "dc_daily": ("get_dc_daily", {}),
        "ths_hot": ("get_ths_hot", {}),
        "dc_hot": ("get_dc_hot", {}),
        "tdx_daily": ("get_tdx_daily", {}),
        "kpl_list": ("get_kpl_list", {}),
        "hm_detail": ("get_hm_detail", {}),
        # 财务/股东/质押/解禁
        "income": ("get_income", {}),
        "balancesheet": ("get_balancesheet", {}),
        "cashflow": ("get_cashflow", {}),
        "forecast": ("get_forecast", {}),
        "express": ("get_express", {}),
        "dividend": ("get_dividend", {}),
        "fina_indicator": ("get_fina_indicator", {}),
        "fina_audit": ("get_fina_audit", {}),
        "stk_holdertrade": ("get_stk_holdertrade", {}),
        "stk_holdernumber": ("get_stk_holdernumber", {}),
        "pledge_stat": ("get_pledge_stat", {}),
        "share_float": ("get_share_float", {}),
        "repurchase": ("get_repurchase", {}),
        "stock_company": ("get_stock_company", {}),
        "stk_managers": ("get_stk_managers", {}),
        "stk_nineturn": ("get_stk_nineturn", {}),
        "stk_ah_comparison": ("get_stk_ah_comparison", {}),
        "ccass_hold": ("get_ccass_hold", {}),
        "report_rc": ("get_report_rc", {}),
        "stk_rewards": ("get_stk_rewards", {}),
        "top10_holders": ("get_top10_holders", {}),
        "top10_floatholders": ("get_top10_floatholders", {}),
        "stk_surv": ("get_stk_surv", {}),
        "hs_const": ("get_hs_const", {}),
        "namechange": ("get_namechange", {}),
        "margin_secs": ("get_margin_secs", {}),
        "new_share": ("get_new_share", {}),
        "ggt_top10": ("get_ggt_top10", {}),
        "ggt_daily": ("get_ggt_daily", {}),
        "stk_factor": ("get_stk_factor", {}),
        "stk_auction": ("get_stk_auction", {}),
        "limit_step": ("get_limit_step", {}),
        "limit_list_ths": ("get_limit_list_ths", {}),
        "broker_recommend": ("get_broker_recommend", {}),
        "concept": ("get_concept", {}),
        "concept_detail": ("get_concept_detail", {}),
        "stock_st": ("get_stock_st", {}),
        "stock_hsgt": ("get_stock_hsgt", {}),
        "st": ("get_st", {}),
        "ths_index": ("get_ths_index", {}),
        "ths_member": ("get_ths_member", {}),
        "hm_list": ("get_hm_list", {}),
        "dc_index": ("get_dc_index", {}),
        "dc_member": ("get_dc_member", {}),
        "tdx_index": ("get_tdx_index", {}),
        "tdx_member": ("get_tdx_member", {}),
        "kpl_concept_cons": ("get_kpl_concept_cons", {}),
        "dc_concept": ("get_dc_concept", {}),
        "dc_concept_cons": ("get_dc_concept_cons", {}),
        # 补齐 DB 中有但 API map 中缺失的表
        "bak_basic": ("get_bak_basic", {}),
        "bse_mapping": ("get_bse_mapping", {}),
        "ccass_hold_detail": ("get_ccass_hold_detail", {}),
        "cyq_perf": ("get_cyq_perf", {}),
        "fina_mainbz": ("get_fina_mainbz", {}),
        "index_weight": ("get_index_weight", {}),
        "margin": ("get_margin_summary", {}),
        "slb_sec": ("get_slb_sec", {}),
        "slb_len": ("get_slb_len", {}),
        # 通过 _call 直接调用的表
        "disclosure_date": (None, {}),
        "pledge_detail": (None, {}),
        "stk_alert": (None, {}),
        "limit_cpt_list": (None, {}),
        "stock_basic": (None, {}),
        "trade_cal": (None, {}),
    }

    def sync_table(self, table_name: str, trade_date: str = "") -> int:
        """同步单张表的数据。

        Args:
            table_name: 表名（如 daily_basic, moneyflow）。
            trade_date: 交易日期 YYYYMMDD，默认当天。

        Returns:
            写入记录数。
        """
        if not self.tushare:
            logger.error("Tushare 未启用")
            return 0

        if not trade_date:
            trade_date = date.today().strftime("%Y%m%d")

        if table_name not in self._TABLE_API_MAP:
            available = ", ".join(sorted(self._TABLE_API_MAP.keys()))
            logger.error(f"未知表名: {table_name}，可用: {available}")
            return 0

        api_name, rename_map = self._TABLE_API_MAP[table_name]
        import time as _tm

        logger.info(f"单表同步 [{table_name}] via {api_name or 'SDK直调'} ({trade_date})...")

        # None = 通过 SDK _call 直调（不传 trade_date，避免不支持的参数）
        if api_name is None:
            if table_name in ("stock_basic", "trade_cal"):
                df = self.tushare._call(table_name)
            else:
                df = self.tushare._call(table_name, trade_date=trade_date)
        else:
            provider_method = getattr(self.tushare, api_name, None)
            if not provider_method:
                logger.error(f"Provider 无此方法: {api_name}")
                return 0
            try:
                df = provider_method(trade_date=trade_date)
            except TypeError:
                df = pd.DataFrame()

        if df.empty:
            logger.info(f"[{table_name}] 无数据")
            return 0

        # 重命名列
        if rename_map:
            df = df.rename(columns=rename_map)
        df = self._drop_ts_code(df)

        # 确定主键
        pk_map = {
            "daily_basic": "symbol, date",
            "moneyflow": "symbol, date",
            "stock_daily": "symbol, date",
            "hk_hold": "symbol, date",
            "margin_detail": "symbol, date",
            "adj_factor": "symbol, trade_date",
            "stk_limit": "symbol, trade_date",
            "stk_shock": "symbol, trade_date",
            "stk_high_shock": "symbol, trade_date",
            "stk_premarket": "symbol, trade_date",
            "stk_auction_o": "symbol, trade_date",
            "stk_auction_c": "symbol, trade_date",
            # 无唯一键的表：直接 append
            "moneyflow_hsgt": "trade_date",
        }
        # 不在 pk_map 中的表都用空主键（append 模式，避免无 symbol 列的表报错）
        pk = pk_map.get(table_name, "")

        count = self._upsert_df(table_name, df, primary_key=pk)
        logger.info(f"[{table_name}] 写入 {count} 条")

        # 清理旧数据
        self._cleanup_old_data()

        return count

    def backfill_tushare(self, start="2026-01-01"):
        """回填：初始化基础数据 + 确保最近 60 个交易日数据完整。"""
        if not self.tushare:
            return {}
        e = date.today().strftime("%Y%m%d")
        self._init_tushare_basics()
        self._init_tushare_trade_cal(start.replace("-", ""), e)
        logger.info("开始 60 交易日数据补齐...")
        result = self._ensure_recent_data(e)
        self._cleanup_old_data()
        logger.info(f"backfill done: {dict(sorted(result.items()))}")
        return result

    def _init_tushare_basics(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                if conn.execute("SELECT COUNT(*) FROM stock_basic").fetchone()[0] > 0: return
        except: pass
        df = self.tushare.get_stock_basic()
        if not df.empty:
            self._upsert_df("stock_basic", df[[c for c in ["symbol","name","industry","area","list_date","market"] if c in df.columns]], primary_key="symbol")

    def _init_tushare_trade_cal(self, start, end):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cnt = conn.execute("SELECT COUNT(*) FROM trade_cal").fetchone()[0]
                if cnt > 20: return True
        except: pass
        df = self.tushare.get_trade_cal(start, end)
        if not df.empty:
            df = df[[c for c in ["cal_date","is_open","pretrade_date"] if c in df.columns]]
            self._upsert_df("trade_cal", df, primary_key="cal_date")
            return True
        return False

    def _get_trade_date_range(self, start, end):
        try:
            with sqlite3.connect(self.db_path) as conn:
                rows = conn.execute("SELECT cal_date FROM trade_cal WHERE cal_date>=? AND cal_date<=? AND is_open=1 ORDER BY cal_date", (start, end)).fetchall()
            return [r[0] for r in rows]
        except: return []

    @staticmethod
    def _drop_ts_code(df):
        return df.drop(columns=["ts_code"], errors="ignore") if "ts_code" in df.columns else df

    def _upsert_df(self, table, df, primary_key="symbol, date"):
        if df.empty: return 0
        try:
            # 自动过滤：只保留表中存在的列
            with sqlite3.connect(self.db_path) as conn:
                table_cols = {r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
                extra = set(df.columns) - table_cols
                if extra:
                    df = df.drop(columns=list(extra), errors="ignore")
            if df.empty: return 0
            with sqlite3.connect(self.db_path) as conn:
                if primary_key:
                    if "," in primary_key:
                        keys = [k.strip() for k in primary_key.split(",")]
                        for _, row in df.iterrows():
                            cond = " AND ".join(f"{k}=?" for k in keys)
                            vals = [row[k] for k in keys if k in row.index]
                            conn.execute(f"DELETE FROM {table} WHERE {cond}", vals)
                    else:
                        for _, row in df.iterrows():
                            if primary_key in row.index:
                                conn.execute(f"DELETE FROM {table} WHERE {primary_key}=?", (row[primary_key],))
                df.to_sql(table, conn, if_exists="append", index=False, method="multi", chunksize=500)
                conn.commit()
            return len(df)
        except Exception as exc:
            logger.warning(f"_upsert_df [{table}] 失败: {exc}")
            return 0

    def _cleanup_old_data(self, keep_days=60):
        """删除超过 keep_days 个交易日的历史数据，仅保留日频表。

        Args:
            keep_days: 保留最近 N 个交易日的日频数据。
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # 获取第 N 个最近的交易日
                rows = conn.execute(
                    "SELECT cal_date FROM trade_cal WHERE is_open=1 ORDER BY cal_date DESC LIMIT 1 OFFSET ?",
                    (keep_days - 1,),
                ).fetchone()
                if not rows:
                    return
                cutoff = rows[0]
        except Exception:
            return

        # 带 date 列的表
        date_tables = [
            "stock_daily", "daily_basic", "moneyflow", "limit_list",
            "hk_hold", "margin_detail", "top_list", "top_inst",
        ]
        # 带 trade_date 列的表
        trade_date_tables = [
            "stk_limit", "adj_factor", "block_trade", "suspen_d",
            "hsgt_top10", "stk_auction_o", "stk_auction_c", "margin",
        ]

        deleted_total = 0
        try:
            with sqlite3.connect(self.db_path) as conn:
                for tbl in date_tables:
                    try:
                        cnt = conn.execute(f"DELETE FROM {tbl} WHERE date < ?", (cutoff,)).rowcount
                        deleted_total += cnt
                    except Exception:
                        pass
                for tbl in trade_date_tables:
                    try:
                        cnt = conn.execute(f"DELETE FROM {tbl} WHERE trade_date < ?", (cutoff,)).rowcount
                        deleted_total += cnt
                    except Exception:
                        pass
                conn.commit()
            if deleted_total > 0:
                logger.info(f"数据清理: 删除 {deleted_total} 条旧数据 (保留近{keep_days}个交易日, cutoff={cutoff})")
        except Exception as exc:
            logger.warning(f"数据清理失败: {exc}")

    def get_stock_names(self, symbols):
        if not symbols: return {}
        ph = ",".join("?" * len(symbols))
        try:
            with sqlite3.connect(self.db_path) as conn:
                rows = conn.execute(f"SELECT symbol, name FROM stock_basic WHERE symbol IN ({ph})", symbols).fetchall()
            return {r[0]: r[1] or "" for r in rows}
        except: return {}

    def get_stock_meta_batch(self, symbols):
        if not symbols: return {}
        r = {}
        try:
            ph = ",".join("?" * len(symbols))
            with sqlite3.connect(self.db_path) as conn:
                basics = conn.execute(f"SELECT symbol, name, industry FROM stock_basic WHERE symbol IN ({ph})", symbols).fetchall()
                bm = {b[0]: {"name": b[1] or "", "industry": b[2] or ""} for b in basics}
                for s in symbols:
                    row = conn.execute("SELECT pe_ttm, circ_mv FROM daily_basic WHERE symbol=? ORDER BY date DESC LIMIT 1", (s,)).fetchone()
                    meta = bm.get(s, {"name": "", "industry": ""})
                    r[s] = {"symbol": s, "name": meta["name"], "industry": meta["industry"],
                            "pe_ttm": row[0] if row else None, "circ_mv": row[1] if row else None, "net_mf_amount": None}
                    mf = conn.execute("SELECT net_mf_amount FROM moneyflow WHERE symbol=? ORDER BY date DESC LIMIT 1", (s,)).fetchone()
                    if mf: r[s]["net_mf_amount"] = mf[0]
        except: pass
        return r
