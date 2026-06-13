-- =========================================================
-- Sequoia-X 数据库 DDL (含字段注释)
-- 共 97 张表
-- =========================================================

-- =========================================================
-- adj_factor
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- adj_factor  复权因子
CREATE TABLE adj_factor (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, adj_factor REAL, UNIQUE (symbol, trade_date));

-- =========================================================
-- bak_basic
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- name  名称
-- industry  所属行业
-- pe  市盈率
-- float_share  流通股本(万股)
-- total_share  总股本(万股)
-- total_assets  总资产
-- liquid_assets  流动资产
-- eps  每股收益
-- bvps  每股净资产
-- pb  市净率
-- list_date  上市日期
CREATE TABLE bak_basic (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, name TEXT, industry TEXT, pe REAL, float_share REAL, total_share REAL, total_assets REAL, liquid_assets REAL, fixed_assets REAL, eps REAL, bvps REAL, pb REAL, list_date TEXT, UNIQUE (trade_date, ts_code));

-- =========================================================
-- balancesheet
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- f_ann_date  实际公告日期
-- end_date  报告期
-- report_type  报告类型
-- total_assets  总资产
-- total_liab  总负债
-- total_hldr_eqy_exc_min_int  归母权益(不含少数)
-- money_cap  货币资金
-- accounts_receiv  应收账款
-- inventories  存货
-- fix_assets  固定资产
-- intan_assets  无形资产
-- r_and_d  研发支出
-- goodwill  商誉
-- lt_borr  长期借款
-- st_borr  短期借款
-- notes_payable  应付票据
-- acct_payable  应付账款
-- defer_tax_assets  递延所得税资产
-- defer_tax_liab  递延所得税负债
-- update_flag  更新标识
CREATE TABLE balancesheet (symbol TEXT NOT NULL, ann_date TEXT, f_ann_date TEXT, end_date TEXT NOT NULL, report_type TEXT, total_assets REAL, total_liab REAL, total_hldr_eqy_exc_min_int REAL, total_cur_assets REAL, total_nca REAL, total_cur_liab REAL, total_ncl REAL, money_cap REAL, accounts_receiv REAL, inventories REAL, fix_assets REAL, intan_assets REAL, r_and_d REAL, goodwill REAL, lt_borr REAL, st_borr REAL, notes_payable REAL, acct_payable REAL, defer_tax_assets REAL, defer_tax_liab REAL, update_flag TEXT, UNIQUE (symbol, end_date, report_type));

-- =========================================================
-- block_trade
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- price  价格
-- vol  成交量
-- amount  成交额
-- buyer  买方席位
-- seller  卖方席位
CREATE TABLE block_trade (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, price REAL, vol REAL, amount REAL, buyer TEXT, seller TEXT, UNIQUE (symbol, trade_date));

-- =========================================================
-- broker_recommend
-- =========================================================
-- month  月份
-- broker  券商名称
-- symbol  股票代码
-- name  名称
CREATE TABLE broker_recommend (month TEXT NOT NULL, broker TEXT, symbol TEXT NOT NULL, name TEXT, UNIQUE (month, broker, symbol));

-- =========================================================
-- bse_mapping
-- =========================================================
-- n_code  新代码
-- o_code  旧代码
-- name  名称
-- list_date  上市日期
CREATE TABLE bse_mapping (n_code TEXT, o_code TEXT, name TEXT, list_date TEXT, UNIQUE (n_code));

-- =========================================================
-- cashflow
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- f_ann_date  实际公告日期
-- end_date  报告期
-- report_type  报告类型
-- net_profit  净利润
-- n_cashflow_act  经营活动现金流净额
-- n_cashflow_inv_act  投资活动现金流净额
-- n_cash_flows_fnc_act  筹资活动现金流净额
-- free_cashflow  自由现金流
-- c_cash_equ_beg_period  期初现金余额
-- c_cash_equ_end_period  期末现金余额
-- update_flag  更新标识
CREATE TABLE cashflow (symbol TEXT NOT NULL, ann_date TEXT, f_ann_date TEXT, end_date TEXT NOT NULL, report_type TEXT, net_profit REAL, n_cashflow_act REAL, n_cashflow_inv_act REAL, n_cash_flows_fnc_act REAL, free_cashflow REAL, c_cash_equ_beg_period REAL, c_cash_equ_end_period REAL, update_flag TEXT, UNIQUE (symbol, end_date, report_type));

-- =========================================================
-- ccass_hold
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- name  名称
-- shareholding  持股数量
-- hold_nums  持仓机构数
-- hold_ratio  持股比例(%)
CREATE TABLE ccass_hold (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, shareholding REAL, hold_nums REAL, hold_ratio REAL, UNIQUE (symbol, trade_date));

-- =========================================================
-- ccass_hold_detail
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- name  名称
-- col_participant_id  参与者ID
-- col_participant_name  参与者名称
-- col_shareholding  持股数量
-- col_shareholding_percent  持股比例(%)
CREATE TABLE ccass_hold_detail (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, name TEXT, col_participant_id TEXT, col_participant_name TEXT, col_shareholding REAL, col_shareholding_percent REAL, UNIQUE (trade_date, ts_code, col_participant_id));

-- =========================================================
-- concept
-- =========================================================
-- code  代码
-- name  名称
-- src  来源
CREATE TABLE concept (code TEXT PRIMARY KEY, name TEXT, src TEXT, UNIQUE (code));

-- =========================================================
-- concept_detail
-- =========================================================
-- id  ID
-- concept_name  概念名称
-- symbol  股票代码
-- name  名称
-- in_date  纳入日期
-- out_date  剔除日期
CREATE TABLE concept_detail (id TEXT NOT NULL, concept_name TEXT, symbol TEXT NOT NULL, name TEXT, in_date TEXT, out_date TEXT, UNIQUE (id, symbol));

-- =========================================================
-- cyq_chips
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- price  价格
CREATE TABLE cyq_chips (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, price REAL, percent REAL);

-- =========================================================
-- cyq_perf
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- cost_5pct  5%筹码成本价
-- cost_50pct  50%筹码成本价(中位成本)
-- cost_95pct  95%筹码成本价
-- weight_avg  加权平均成本
-- winner_rate  胜率(获利盘比例%)
CREATE TABLE cyq_perf (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, his_low REAL, his_high REAL, cost_5pct REAL, cost_50pct REAL, cost_95pct REAL, weight_avg REAL, winner_rate REAL, UNIQUE (symbol, trade_date));

-- =========================================================
-- daily_basic
-- =========================================================
-- symbol  股票代码
-- date  交易日期
-- close  收盘价
-- pe  市盈率
-- pe_ttm  市盈率TTM
-- pb  市净率
-- total_mv  总市值(万元)
-- circ_mv  流通市值(万元)
-- turnover_rate  换手率(%)
-- volume_ratio  量比
-- dv_ratio  股息率(%)
-- dv_ttm  股息率TTM(%)
-- total_share  总股本(万股)
-- float_share  流通股本(万股)
-- free_share  自由流通股本(万股)
CREATE TABLE daily_basic (symbol TEXT NOT NULL, date TEXT NOT NULL, close REAL, pe REAL, pe_ttm REAL, pb REAL, total_mv REAL, circ_mv REAL, turnover_rate REAL, volume_ratio REAL, dv_ratio REAL, dv_ttm REAL, total_share REAL, float_share REAL, free_share REAL, UNIQUE (symbol, date));

-- =========================================================
-- dc_concept
-- =========================================================
-- trade_date  交易日期
-- theme_code  题材代码
-- name  名称
-- pct_change  涨跌幅(%)
-- hot  热度
CREATE TABLE dc_concept (trade_date TEXT NOT NULL, theme_code TEXT NOT NULL, name TEXT, pct_change REAL, hot REAL, UNIQUE (trade_date, theme_code));

-- =========================================================
-- dc_concept_cons
-- =========================================================
-- trade_date  交易日期
-- theme_code  题材代码
-- ts_code  TS代码
-- name  名称
-- reason  原因/说明
CREATE TABLE dc_concept_cons (trade_date TEXT NOT NULL, theme_code TEXT NOT NULL, ts_code TEXT NOT NULL, name TEXT, reason TEXT, UNIQUE (trade_date, theme_code, ts_code));

-- =========================================================
-- dc_daily
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- name  名称
-- close  收盘价
-- pct_change  涨跌幅(%)
-- vol  成交量
CREATE TABLE dc_daily (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, close REAL, pct_change REAL, vol REAL, UNIQUE (trade_date, ts_code));

-- =========================================================
-- dc_hot
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- rank  排名
-- pct_change  涨跌幅(%)
CREATE TABLE dc_hot (trade_date TEXT NOT NULL, ts_code TEXT, ts_name TEXT, rank INTEGER, pct_change REAL, UNIQUE (trade_date, ts_code));

-- =========================================================
-- dc_index
-- =========================================================
-- ts_code  TS代码
-- name  名称
-- idx_type  板块类型
CREATE TABLE dc_index (ts_code TEXT NOT NULL, name TEXT, idx_type TEXT, UNIQUE (ts_code));

-- =========================================================
-- dc_member
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- con_code  成分代码
-- name  名称
CREATE TABLE dc_member (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, con_code TEXT NOT NULL, name TEXT, UNIQUE (trade_date, ts_code, con_code));

-- =========================================================
-- disclosure_date
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- end_date  报告期
-- pre_date  预计披露日期
-- actual_date  实际披露日期
CREATE TABLE disclosure_date (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, pre_date TEXT, actual_date TEXT, UNIQUE (symbol, end_date));

-- =========================================================
-- dividend
-- =========================================================
-- symbol  股票代码
-- end_date  报告期
-- ann_date  公告日期
-- div_proc  分红进度
-- stk_div  每股送股
-- stk_bo_rate  每股转增
-- cash_div  每股分红(税前)
-- cash_div_tax  每股分红(税后)
-- ex_date  除权除息日
-- pay_date  派息日
-- imp_ann_date  实施公告日
CREATE TABLE dividend (symbol TEXT NOT NULL, end_date TEXT, ann_date TEXT, div_proc TEXT, stk_div REAL, stk_bo_rate REAL, cash_div REAL, cash_div_tax REAL, ex_date TEXT, pay_date TEXT, imp_ann_date TEXT, UNIQUE (symbol, end_date, div_proc));

-- =========================================================
-- express
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- end_date  报告期
-- revenue  营业收入
-- operate_profit  营业利润
-- total_profit  利润总额
-- n_income  净利润
-- diluted_eps  稀释每股收益
-- yoy_net_profit  净利润同比(%)
-- bps  每股净资产
-- yoy_sales  营收同比(%)
-- perf_summary  业绩摘要
CREATE TABLE express (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, revenue REAL, operate_profit REAL, total_profit REAL, n_income REAL, diluted_eps REAL, yoy_net_profit REAL, bps REAL, yoy_sales REAL, perf_summary TEXT, UNIQUE (symbol, end_date));

-- =========================================================
-- fina_audit
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- end_date  报告期
-- audit_result  审计意见
-- audit_fees  审计费用
-- audit_agency  审计机构
-- audit_sign  签字会计师
CREATE TABLE fina_audit (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, audit_result TEXT, audit_fees REAL, audit_agency TEXT, audit_sign TEXT, UNIQUE (symbol, end_date));

-- =========================================================
-- fina_indicator
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- end_date  报告期
-- eps  每股收益
-- dt_eps  稀释每股收益
-- roe  净资产收益率(%)
-- roa  总资产收益率(%)
-- grossprofit_margin  销售毛利率(%)
-- netprofit_margin  销售净利率(%)
-- debt_to_assets  资产负债率(%)
-- current_ratio  流动比率
-- quick_ratio  速动比率
-- or_yoy  营业收入同比(%)
-- netprofit_yoy  净利润同比(%)
-- basic_eps_yoy  基本每股收益同比(%)
-- profit_dedt  扣非净利润
-- op_income  经营活动净收益
-- bps  每股净资产
-- update_flag  更新标识
CREATE TABLE fina_indicator (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, eps REAL, dt_eps REAL, roe REAL, roa REAL, grossprofit_margin REAL, netprofit_margin REAL, debt_to_assets REAL, current_ratio REAL, quick_ratio REAL, or_yoy REAL, netprofit_yoy REAL, basic_eps_yoy REAL, profit_dedt REAL, op_income REAL, bps REAL, ocqps REAL, update_flag TEXT, UNIQUE (symbol, end_date));

-- =========================================================
-- fina_mainbz
-- =========================================================
-- symbol  股票代码
-- end_date  报告期
-- bz_item  业务项目
-- bz_sales  业务收入
-- bz_profit  业务利润
-- bz_cost  业务成本
CREATE TABLE fina_mainbz (symbol TEXT NOT NULL, end_date TEXT NOT NULL, bz_item TEXT, bz_sales REAL, bz_profit REAL, bz_cost REAL, UNIQUE (symbol, end_date, bz_item));

-- =========================================================
-- forecast
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- end_date  报告期
-- type  类型
-- p_change_min  净利润变动下限(%)
-- p_change_max  净利润变动上限(%)
-- net_profit_min  净利润下限(万元)
-- net_profit_max  净利润上限(万元)
-- summary  摘要
-- change_reason  变动原因
CREATE TABLE forecast (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, type TEXT, p_change_min REAL, p_change_max REAL, net_profit_min REAL, net_profit_max REAL, summary TEXT, change_reason TEXT, UNIQUE (symbol, end_date));

-- =========================================================
-- ggt_daily
-- =========================================================
-- trade_date  交易日期
-- buy_volume  买入量
-- sell_volume  卖出量
CREATE TABLE ggt_daily (trade_date TEXT PRIMARY KEY, buy_amount REAL, sell_amount REAL, buy_volume REAL, sell_volume REAL, UNIQUE (trade_date));

-- =========================================================
-- ggt_top10
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- name  名称
-- close  收盘价
-- amount  成交额
-- market_type  市场类型
-- rank  排名
CREATE TABLE ggt_top10 (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, name TEXT, close REAL, amount REAL, market_type INTEGER, rank INTEGER, UNIQUE (trade_date, ts_code));

-- =========================================================
-- hk_hold
-- =========================================================
-- symbol  股票代码
-- date  交易日期
-- name  名称
-- vol  成交量
-- exchange  交易所
CREATE TABLE hk_hold (symbol TEXT NOT NULL, date TEXT NOT NULL, name TEXT, vol INTEGER, ratio REAL, exchange TEXT, UNIQUE (symbol, date));

-- =========================================================
-- hm_detail
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- net_amount  净额
-- hm_name  游资名称
CREATE TABLE hm_detail (trade_date TEXT NOT NULL, ts_code TEXT, ts_name TEXT, buy_amount REAL, sell_amount REAL, net_amount REAL, hm_name TEXT, UNIQUE (trade_date, ts_code));

-- =========================================================
-- hm_list
-- =========================================================
-- name  名称
-- desc  描述
CREATE TABLE hm_list (name TEXT PRIMARY KEY, desc TEXT, UNIQUE (name));

-- =========================================================
-- hs_const
-- =========================================================
-- symbol  股票代码
-- hs_type  类型 SH沪股通 SZ深股通
-- in_date  纳入日期
-- out_date  剔除日期
-- is_new  是否最新 1=是
CREATE TABLE hs_const (symbol TEXT NOT NULL, hs_type TEXT, in_date TEXT, out_date TEXT, is_new TEXT, UNIQUE (symbol, hs_type));

-- =========================================================
-- hsgt_top10
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- name  名称
-- close  收盘价
-- change  涨跌额
-- rank  排名
-- market_type  市场类型
-- amount  成交额
-- net_amount  净额
CREATE TABLE hsgt_top10 (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, close REAL, change REAL, rank INTEGER, market_type INTEGER, amount REAL, net_amount REAL, UNIQUE (symbol, trade_date));

-- =========================================================
-- income
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- f_ann_date  实际公告日期
-- end_date  报告期
-- report_type  报告类型
-- basic_eps  基本每股收益
-- diluted_eps  稀释每股收益
-- total_revenue  营业总收入
-- revenue  营业收入
-- operate_profit  营业利润
-- total_profit  利润总额
-- n_income  净利润
-- n_income_attr_p  归母净利润
-- ebit  息税前利润
-- ebitda  息税折旧摊销前利润
-- total_cogs  营业总成本
-- rd_exp  研发费用
-- update_flag  更新标识
CREATE TABLE income (symbol TEXT NOT NULL, ann_date TEXT, f_ann_date TEXT, end_date TEXT NOT NULL, report_type TEXT, basic_eps REAL, diluted_eps REAL, total_revenue REAL, revenue REAL, operate_profit REAL, total_profit REAL, n_income REAL, n_income_attr_p REAL, ebit REAL, ebitda REAL, total_cogs REAL, rd_exp REAL, update_flag TEXT, UNIQUE (symbol, end_date, report_type));

-- =========================================================
-- index_weight
-- =========================================================
-- index_code  指数代码
-- symbol  股票代码
-- trade_date  交易日期
-- weight  权重
CREATE TABLE index_weight (index_code TEXT NOT NULL, symbol TEXT NOT NULL, trade_date TEXT NOT NULL, weight REAL, UNIQUE (index_code, symbol, trade_date));

-- =========================================================
-- kpl_concept_cons
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- name  名称
-- con_code  成分代码
-- con_name  成分名称
CREATE TABLE kpl_concept_cons (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, name TEXT, con_code TEXT NOT NULL, con_name TEXT, UNIQUE (trade_date, ts_code, con_code));

-- =========================================================
-- kpl_list
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- name  名称
-- pct_chg  涨跌幅(%)
-- tag  标签
-- lu_time  涨停时间
-- status  状态
CREATE TABLE kpl_list (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, pct_chg REAL, tag TEXT, lu_time TEXT, status TEXT, UNIQUE (trade_date, ts_code));

-- =========================================================
-- limit_cpt_list
-- =========================================================
-- ts_code  TS代码
-- trade_date  交易日期
-- name  名称
-- pct_chg  涨跌幅(%)
-- rank  排名
CREATE TABLE limit_cpt_list (ts_code TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, up_nums INTEGER, cons_nums INTEGER, pct_chg REAL, rank INTEGER, UNIQUE (ts_code, trade_date));

-- =========================================================
-- limit_list
-- =========================================================
-- symbol  股票代码
-- date  交易日期
-- name  名称
-- industry  所属行业
-- limit_type  类型 U涨停 D跌停 Z炸板
-- close  收盘价
-- pct_chg  涨跌幅(%)
-- amount  成交额
-- limit_amount  板上成交额
-- float_mv  流通市值
-- total_mv  总市值(万元)
-- turnover_ratio  换手率
-- fd_amount  封单金额
-- first_time  首次封板时间
-- last_time  最后封板时间
-- open_times  开板次数
-- limit_times  连板数
-- up_stat  涨停统计
CREATE TABLE limit_list (symbol TEXT NOT NULL, date TEXT NOT NULL, name TEXT, industry TEXT, limit_type TEXT, close REAL, pct_chg REAL, amount REAL, limit_amount REAL, float_mv REAL, total_mv REAL, turnover_ratio REAL, fd_amount REAL, first_time TEXT, last_time TEXT, open_times INTEGER, limit_times INTEGER, up_stat TEXT, UNIQUE (symbol, date, limit_type));

-- =========================================================
-- limit_list_ths
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- name  名称
-- price  价格
-- pct_chg  涨跌幅(%)
-- limit_type  类型 U涨停 D跌停 Z炸板
-- tag  标签
-- status  状态
-- turnover_rate  换手率(%)
CREATE TABLE limit_list_ths (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, price REAL, pct_chg REAL, limit_type TEXT, tag TEXT, status TEXT, turnover_rate REAL, UNIQUE (symbol, trade_date));

-- =========================================================
-- limit_step
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- name  名称
CREATE TABLE limit_step (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, nums INTEGER, UNIQUE (symbol, trade_date));

-- =========================================================
-- margin
-- =========================================================
-- trade_date  交易日期
-- exchange_id  交易所代码
-- rzye  融资余额
-- rzmre  融资买入额
-- rzche  融资偿还额
-- rqye  融券余额
-- rqmcl  融券卖出量
-- rzrqye  融资融券余额
-- rqyl  融券余量
CREATE TABLE margin (trade_date TEXT PRIMARY KEY, exchange_id TEXT, rzye REAL, rzmre REAL, rzche REAL, rqye REAL, rqmcl REAL, rzrqye REAL, rqyl REAL, UNIQUE (trade_date));

-- =========================================================
-- margin_detail
-- =========================================================
-- symbol  股票代码
-- date  交易日期
-- name  名称
-- rzye  融资余额
-- rqye  融券余额
-- rzmre  融资买入额
-- rqyl  融券余量
-- rzche  融资偿还额
-- rqmcl  融券卖出量
-- rzrqye  融资融券余额
CREATE TABLE margin_detail (symbol TEXT NOT NULL, date TEXT NOT NULL, name TEXT, rzye REAL, rqye REAL, rzmre REAL, rqyl REAL, rzche REAL, rqchl REAL, rqmcl REAL, rzrqye REAL, UNIQUE (symbol, date));

-- =========================================================
-- margin_secs
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- name  名称
-- exchange  交易所
CREATE TABLE margin_secs (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, exchange TEXT, UNIQUE (symbol, trade_date));

-- =========================================================
-- moneyflow
-- =========================================================
-- symbol  股票代码
-- date  交易日期
-- buy_sm_amount  小单买入额(万元)
-- sell_sm_amount  小单卖出额
-- buy_md_amount  中单买入额
-- sell_md_amount  中单卖出额
-- buy_lg_amount  大单买入额
-- sell_lg_amount  大单卖出额
-- buy_elg_amount  超大单买入额
-- sell_elg_amount  超大单卖出额
-- net_mf_amount  净流入额(万元)
CREATE TABLE moneyflow (symbol TEXT NOT NULL, date TEXT NOT NULL, buy_sm_vol REAL, buy_sm_amount REAL, sell_sm_vol REAL, sell_sm_amount REAL, buy_md_vol REAL, buy_md_amount REAL, sell_md_vol REAL, sell_md_amount REAL, buy_lg_vol REAL, buy_lg_amount REAL, sell_lg_vol REAL, sell_lg_amount REAL, buy_elg_vol REAL, buy_elg_amount REAL, sell_elg_vol REAL, sell_elg_amount REAL, net_mf_vol REAL, net_mf_amount REAL, UNIQUE (symbol, date));

-- =========================================================
-- moneyflow_cnt_ths
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- name  名称
-- pct_change  涨跌幅(%)
-- net_amount  净额
CREATE TABLE moneyflow_cnt_ths (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, pct_change REAL, net_amount REAL, UNIQUE (trade_date, ts_code));

-- =========================================================
-- moneyflow_dc
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- name  名称
-- pct_change  涨跌幅(%)
-- close  收盘价
-- net_amount  净额
-- buy_lg_amount  大单买入额
-- buy_elg_amount  超大单买入额
CREATE TABLE moneyflow_dc (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, pct_change REAL, close REAL, net_amount REAL, buy_lg_amount REAL, buy_elg_amount REAL, UNIQUE (trade_date, ts_code));

-- =========================================================
-- moneyflow_hsgt
-- =========================================================
-- trade_date  交易日期
-- ggt_ss  港股通沪净买入
-- ggt_sz  港股通深净买入
-- hgt  沪股通净买入
-- sgt  深股通净买入
-- north_money  北向资金净流入
-- south_money  南向资金净流入
CREATE TABLE moneyflow_hsgt (trade_date TEXT PRIMARY KEY, ggt_ss REAL, ggt_sz REAL, hgt REAL, sgt REAL, north_money REAL, south_money REAL, UNIQUE (trade_date));

-- =========================================================
-- moneyflow_ind_dc
-- =========================================================
-- trade_date  交易日期
-- content_type  内容类型
-- ts_code  TS代码
-- name  名称
-- pct_change  涨跌幅(%)
-- net_amount  净额
CREATE TABLE moneyflow_ind_dc (trade_date TEXT NOT NULL, content_type TEXT, ts_code TEXT, name TEXT, pct_change REAL, net_amount REAL, UNIQUE (trade_date, ts_code, content_type));

-- =========================================================
-- moneyflow_ind_ths
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- industry  所属行业
-- pct_change  涨跌幅(%)
-- net_amount  净额
CREATE TABLE moneyflow_ind_ths (trade_date TEXT NOT NULL, ts_code TEXT, industry TEXT, pct_change REAL, net_amount REAL, UNIQUE (trade_date, ts_code));

-- =========================================================
-- moneyflow_mkt_dc
-- =========================================================
-- trade_date  交易日期
-- close_sh  上证收盘
-- pct_change_sh  上证涨跌幅
-- close_sz  深证收盘
-- pct_change_sz  深证涨跌幅
-- net_amount  净额
-- net_amount_rate  净流入率
CREATE TABLE moneyflow_mkt_dc (trade_date TEXT PRIMARY KEY, close_sh REAL, pct_change_sh REAL, close_sz REAL, pct_change_sz REAL, net_amount REAL, net_amount_rate REAL, UNIQUE (trade_date));

-- =========================================================
-- moneyflow_ths
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- name  名称
-- pct_change  涨跌幅(%)
-- net_amount  净额
-- buy_lg_amount  大单买入额
-- buy_sm_amount  小单买入额(万元)
CREATE TABLE moneyflow_ths (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, pct_change REAL, latest REAL, net_amount REAL, buy_lg_amount REAL, buy_sm_amount REAL, UNIQUE (trade_date, ts_code));

-- =========================================================
-- namechange
-- =========================================================
-- symbol  股票代码
-- name  名称
-- start_date  开始日期
-- end_date  报告期
-- ann_date  公告日期
-- change_reason  变动原因
CREATE TABLE namechange (symbol TEXT, name TEXT, start_date TEXT, end_date TEXT, ann_date TEXT, change_reason TEXT, UNIQUE (symbol, start_date));

-- =========================================================
-- new_share
-- =========================================================
-- symbol  股票代码
-- name  名称
-- ipo_date  上网发行日期
-- issue_date  上市日期
-- amount  成交额
-- price  价格
-- pe  市盈率
-- limit_amount  板上成交额
-- ballot  中签率
CREATE TABLE new_share (symbol TEXT NOT NULL, name TEXT, ipo_date TEXT, issue_date TEXT, amount REAL, price REAL, pe REAL, limit_amount REAL, ballot REAL, UNIQUE (symbol));

-- =========================================================
-- pledge_detail
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- holder_name  股东名称
-- pledge_amount  质押数量
-- start_date  开始日期
-- end_date  报告期
-- is_release  是否解除
CREATE TABLE pledge_detail (symbol TEXT NOT NULL, ann_date TEXT, holder_name TEXT, pledge_amount REAL, start_date TEXT, end_date TEXT, is_release TEXT, UNIQUE (symbol, ann_date, holder_name));

-- =========================================================
-- pledge_stat
-- =========================================================
-- symbol  股票代码
-- end_date  报告期
-- pledge_count  质押次数
-- unrest_pledge  无限售质押(万股)
-- rest_pledge  限售质押(万股)
-- total_share  总股本(万股)
-- pledge_ratio  质押比例(%)
CREATE TABLE pledge_stat (symbol TEXT NOT NULL, end_date TEXT NOT NULL, pledge_count INTEGER, unrest_pledge REAL, rest_pledge REAL, total_share REAL, pledge_ratio REAL, UNIQUE (symbol, end_date));

-- =========================================================
-- report_rc
-- =========================================================
-- symbol  股票代码
-- report_date  报告日期
-- report_title  报告标题
-- org_name  机构名称
-- eps  每股收益
-- pe  市盈率
-- roe  净资产收益率(%)
-- rating  评级
-- max_price  目标价上限
-- min_price  目标价下限
CREATE TABLE report_rc (symbol TEXT NOT NULL, report_date TEXT NOT NULL, report_title TEXT, org_name TEXT, eps REAL, pe REAL, roe REAL, rating TEXT, max_price REAL, min_price REAL, UNIQUE (symbol, report_date, org_name));

-- =========================================================
-- repurchase
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- end_date  报告期
-- proc  进度
-- vol  成交量
-- amount  成交额
-- high_limit  回购价格上限
-- low_limit  回购价格下限
CREATE TABLE repurchase (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT, proc TEXT, vol REAL, amount REAL, high_limit REAL, low_limit REAL, UNIQUE (symbol, ann_date));

-- =========================================================
-- share_float
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- float_date  解禁日期
-- float_share  流通股本(万股)
-- float_ratio  解禁比例(%)
-- holder_name  股东名称
CREATE TABLE share_float (symbol TEXT NOT NULL, ann_date TEXT, float_date TEXT NOT NULL, float_share REAL, float_ratio REAL, holder_name TEXT, share_type TEXT, UNIQUE (symbol, float_date, holder_name));

-- =========================================================
-- slb_len
-- =========================================================
-- trade_date  交易日期
-- ob  期初余额
-- auc_amount  竞价交易
-- repo_amount  协议回购
-- repay_amount  偿还
-- cb  期末余额
CREATE TABLE slb_len (trade_date TEXT PRIMARY KEY, ob REAL, auc_amount REAL, repo_amount REAL, repay_amount REAL, cb REAL, UNIQUE (trade_date));

-- =========================================================
-- slb_sec
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- name  名称
-- ope_inv  期初余量
-- lent_qnt  融出量
-- cls_inv  期末余量
-- end_bal  期末余额
CREATE TABLE slb_sec (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, name TEXT, ope_inv REAL, lent_qnt REAL, cls_inv REAL, end_bal REAL, UNIQUE (trade_date, ts_code));

-- =========================================================
-- st
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- name  名称
-- type  类型
-- type_name  类型名称
CREATE TABLE st (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, type TEXT, type_name TEXT, UNIQUE (symbol, trade_date));

-- =========================================================
-- stk_ah_comparison
-- =========================================================
-- symbol  股票代码
-- hk_code  H股代码
-- trade_date  交易日期
-- name  名称
-- hk_name  H股名称
-- close  收盘价
-- ah_premium  AH溢价率(%)
CREATE TABLE stk_ah_comparison (symbol TEXT NOT NULL, hk_code TEXT, trade_date TEXT NOT NULL, name TEXT, hk_name TEXT, close REAL, hk_close REAL, ah_premium REAL, UNIQUE (symbol, trade_date));

-- =========================================================
-- stk_alert
-- =========================================================
-- symbol  股票代码
-- start_date  开始日期
-- end_date  报告期
-- type  类型
CREATE TABLE stk_alert (symbol TEXT NOT NULL, start_date TEXT NOT NULL, end_date TEXT NOT NULL, type TEXT, UNIQUE (symbol, start_date));

-- =========================================================
-- stk_auction
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- vol  成交量
-- price  价格
-- amount  成交额
-- pre_close  昨收价
-- turnover_rate  换手率(%)
-- volume_ratio  量比
CREATE TABLE stk_auction (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, vol REAL, price REAL, amount REAL, pre_close REAL, turnover_rate REAL, volume_ratio REAL, UNIQUE (symbol, trade_date));

-- =========================================================
-- stk_auction_c
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- close  收盘价
-- open  开盘价
-- high  最高价
-- low  最低价
-- vol  成交量
-- amount  成交额
-- vwap  均价
CREATE TABLE stk_auction_c (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, close REAL, open REAL, high REAL, low REAL, vol REAL, amount REAL, vwap REAL, UNIQUE (symbol, trade_date));

-- =========================================================
-- stk_auction_o
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- vol  成交量
-- price  价格
-- amount  成交额
-- pre_close  昨收价
-- turnover_rate  换手率(%)
-- volume_ratio  量比
CREATE TABLE stk_auction_o (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, vol REAL, price REAL, amount REAL, pre_close REAL, turnover_rate REAL, volume_ratio REAL, UNIQUE (symbol, trade_date));

-- =========================================================
-- stk_factor
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- macd_dif  MACD DIF
-- macd_dea  MACD DEA
-- macd  MACD柱
-- kdj_k  KDJ K
-- kdj_d  KDJ D
-- kdj_j  KDJ J
-- rsi_6  RSI 6日
-- rsi_12  RSI 12日
-- rsi_24  RSI 24日
CREATE TABLE stk_factor (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, macd_dif REAL, macd_dea REAL, macd REAL, kdj_k REAL, kdj_d REAL, kdj_j REAL, rsi_6 REAL, rsi_12 REAL, rsi_24 REAL, UNIQUE (symbol, trade_date));

-- =========================================================
-- stk_high_shock
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- name  名称
-- trade_market  交易市场
-- reason  原因/说明
-- period  周期
CREATE TABLE stk_high_shock (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, trade_market TEXT, reason TEXT, period TEXT, UNIQUE (symbol, trade_date));

-- =========================================================
-- stk_holdernumber
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- end_date  报告期
-- holder_num  股东户数
CREATE TABLE stk_holdernumber (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, holder_num INTEGER, UNIQUE (symbol, end_date));

-- =========================================================
-- stk_holdertrade
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- holder_name  股东名称
-- holder_type  股东类型
-- in_de  方向 IN增持 DE减持
-- change_vol  变动数量
-- change_ratio  变动比例(%)
-- after_share  变动后持股
-- avg_price  均价
-- total_share  总股本(万股)
-- begin_date  开始日期
-- close_date  结束日期
CREATE TABLE stk_holdertrade (symbol TEXT NOT NULL, ann_date TEXT, holder_name TEXT, holder_type TEXT, in_de TEXT, change_vol REAL, change_ratio REAL, after_share REAL, avg_price REAL, total_share REAL, begin_date TEXT, close_date TEXT, UNIQUE (symbol, ann_date, holder_name, in_de));

-- =========================================================
-- stk_limit
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- up_limit  涨停价
-- down_limit  跌停价
-- pre_close  昨收价
CREATE TABLE stk_limit (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, up_limit REAL, down_limit REAL, pre_close REAL, UNIQUE (symbol, trade_date));

-- =========================================================
-- stk_managers
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- name  名称
-- title  职务
-- edu  学历
-- begin_date  开始日期
CREATE TABLE stk_managers (symbol TEXT NOT NULL, ann_date TEXT, name TEXT, gender TEXT, title TEXT, edu TEXT, begin_date TEXT, UNIQUE (symbol, ann_date, name, title));

-- =========================================================
-- stk_nineturn
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- freq  频率
-- up_count  上涨计数
-- down_count  下跌计数
-- nine_up_turn  上涨九转信号
-- nine_down_turn  下跌九转信号
CREATE TABLE stk_nineturn (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, freq TEXT, up_count INTEGER, down_count INTEGER, nine_up_turn INTEGER, nine_down_turn INTEGER, UNIQUE (symbol, trade_date, freq));

-- =========================================================
-- stk_premarket
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- total_share  总股本(万股)
-- float_share  流通股本(万股)
-- pre_close  昨收价
-- up_limit  涨停价
-- down_limit  跌停价
CREATE TABLE stk_premarket (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, total_share REAL, float_share REAL, pre_close REAL, up_limit REAL, down_limit REAL, UNIQUE (symbol, trade_date));

-- =========================================================
-- stk_rewards
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- end_date  报告期
-- name  名称
-- title  职务
-- reward  薪酬(万元)
-- hold_vol  持股数
CREATE TABLE stk_rewards (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, name TEXT, title TEXT, reward REAL, hold_vol REAL, UNIQUE (symbol, end_date, name));

-- =========================================================
-- stk_shock
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- name  名称
-- trade_market  交易市场
-- reason  原因/说明
-- period  周期
CREATE TABLE stk_shock (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, trade_market TEXT, reason TEXT, period TEXT, UNIQUE (symbol, trade_date));

-- =========================================================
-- stk_surv
-- =========================================================
-- symbol  股票代码
-- surv_date  调研日期
-- fund_visitors  调研机构数
-- rece_place  接待地点
-- rece_mode  接待方式
-- rece_org  接待机构
-- org_type  机构类型
CREATE TABLE stk_surv (symbol TEXT NOT NULL, surv_date TEXT NOT NULL, fund_visitors REAL, rece_place TEXT, rece_mode TEXT, rece_org TEXT, org_type TEXT, UNIQUE (symbol, surv_date));

-- =========================================================
-- stock_basic
-- =========================================================
-- symbol  股票代码
-- name  名称
-- industry  所属行业
-- area  地区
-- list_date  上市日期
-- market  市场类型
CREATE TABLE stock_basic (symbol TEXT PRIMARY KEY, name TEXT, industry TEXT, area TEXT, list_date TEXT, market TEXT, UNIQUE (symbol));

-- =========================================================
-- stock_company
-- =========================================================
-- symbol  股票代码
-- com_name  公司全称
-- exchange  交易所
-- chairman  董事长
-- manager  总经理
-- reg_capital  注册资本
-- setup_date  成立日期
-- province  省份
-- city  城市
-- website  网址
-- employees  员工人数
-- main_business  主要业务
CREATE TABLE stock_company (symbol TEXT PRIMARY KEY, com_name TEXT, exchange TEXT, chairman TEXT, manager TEXT, reg_capital REAL, setup_date TEXT, province TEXT, city TEXT, website TEXT, employees INTEGER, main_business TEXT, UNIQUE (symbol));

-- =========================================================
-- stock_daily
-- =========================================================
-- id  ID
-- symbol  股票代码
-- date  交易日期
-- open  开盘价
-- high  最高价
-- low  最低价
-- close  收盘价
-- volume  成交量
-- turnover  成交额
CREATE TABLE stock_daily (
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

-- =========================================================
-- stock_hsgt
-- =========================================================
-- symbol  股票代码
-- name  名称
-- type  类型
-- type_name  类型名称
CREATE TABLE stock_hsgt (symbol TEXT NOT NULL, name TEXT, type TEXT, type_name TEXT, UNIQUE (symbol, type));

-- =========================================================
-- stock_st
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- name  名称
-- type  类型
-- type_name  类型名称
CREATE TABLE stock_st (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, name TEXT, type TEXT, type_name TEXT, UNIQUE (symbol, trade_date));

-- =========================================================
-- suspen_d
-- =========================================================
-- symbol  股票代码
-- trade_date  交易日期
-- suspend_timing  停复牌时间
-- suspend_type  S=停牌 R=复牌
CREATE TABLE suspen_d (symbol TEXT NOT NULL, trade_date TEXT NOT NULL, suspend_timing TEXT, suspend_type TEXT, UNIQUE (symbol, trade_date, suspend_type));

-- =========================================================
-- tdx_daily
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- name  名称
-- close  收盘价
-- pct_change  涨跌幅(%)
-- vol  成交量
CREATE TABLE tdx_daily (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, close REAL, pct_change REAL, vol REAL, UNIQUE (trade_date, ts_code));

-- =========================================================
-- tdx_index
-- =========================================================
-- ts_code  TS代码
-- name  名称
-- idx_type  板块类型
-- idx_count  成分数量
CREATE TABLE tdx_index (ts_code TEXT NOT NULL, name TEXT, idx_type TEXT, idx_count INTEGER, UNIQUE (ts_code));

-- =========================================================
-- tdx_member
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- con_code  成分代码
-- con_name  成分名称
CREATE TABLE tdx_member (trade_date TEXT NOT NULL, ts_code TEXT NOT NULL, con_code TEXT NOT NULL, con_name TEXT, UNIQUE (trade_date, ts_code, con_code));

-- =========================================================
-- ths_daily
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- name  名称
-- close  收盘价
-- pct_change  涨跌幅(%)
-- vol  成交量
-- turnover_rate  换手率(%)
CREATE TABLE ths_daily (trade_date TEXT NOT NULL, ts_code TEXT, name TEXT, close REAL, pct_change REAL, vol REAL, turnover_rate REAL, UNIQUE (trade_date, ts_code));

-- =========================================================
-- ths_hot
-- =========================================================
-- trade_date  交易日期
-- ts_code  TS代码
-- rank  排名
-- pct_change  涨跌幅(%)
-- hot  热度
CREATE TABLE ths_hot (trade_date TEXT NOT NULL, ts_code TEXT, ts_name TEXT, rank INTEGER, pct_change REAL, hot REAL, UNIQUE (trade_date, ts_code));

-- =========================================================
-- ths_index
-- =========================================================
-- ts_code  TS代码
-- name  名称
-- count  数量
-- type  类型
CREATE TABLE ths_index (ts_code TEXT PRIMARY KEY, name TEXT, count INTEGER, type TEXT, UNIQUE (ts_code));

-- =========================================================
-- ths_member
-- =========================================================
-- ts_code  TS代码
-- con_code  成分代码
-- con_name  成分名称
CREATE TABLE ths_member (ts_code TEXT NOT NULL, con_code TEXT NOT NULL, con_name TEXT, UNIQUE (ts_code, con_code));

-- =========================================================
-- top10_floatholders
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- end_date  报告期
-- holder_name  股东名称
-- hold_amount  持股数量
-- hold_ratio  持股比例(%)
-- hold_change  持股变动
-- holder_type  股东类型
CREATE TABLE top10_floatholders (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, holder_name TEXT, hold_amount REAL, hold_ratio REAL, hold_change REAL, holder_type TEXT, UNIQUE (symbol, end_date, holder_name));

-- =========================================================
-- top10_holders
-- =========================================================
-- symbol  股票代码
-- ann_date  公告日期
-- end_date  报告期
-- holder_name  股东名称
-- hold_amount  持股数量
-- hold_ratio  持股比例(%)
-- hold_change  持股变动
-- holder_type  股东类型
CREATE TABLE top10_holders (symbol TEXT NOT NULL, ann_date TEXT, end_date TEXT NOT NULL, holder_name TEXT, hold_amount REAL, hold_ratio REAL, hold_change REAL, holder_type TEXT, UNIQUE (symbol, end_date, holder_name));

-- =========================================================
-- top_inst
-- =========================================================
-- symbol  股票代码
-- date  交易日期
-- exalter  席位名称
-- side  方向 买入/卖出
-- buy  买入金额
-- buy_rate  买入占比(%)
-- sell  卖出金额
-- sell_rate  卖出占比(%)
-- net_buy  净买入
-- reason  原因/说明
CREATE TABLE top_inst (symbol TEXT NOT NULL, date TEXT NOT NULL, exalter TEXT, side TEXT, buy REAL, buy_rate REAL, sell REAL, sell_rate REAL, net_buy REAL, reason TEXT, UNIQUE (symbol, date, exalter));

-- =========================================================
-- top_list
-- =========================================================
-- symbol  股票代码
-- date  交易日期
-- name  名称
-- close  收盘价
-- pct_change  涨跌幅(%)
-- turnover_rate  换手率(%)
-- amount  成交额
-- l_sell  龙虎榜总卖出
-- l_buy  龙虎榜总买入
-- l_amount  龙虎榜总成交额
-- net_amount  净额
-- net_rate  净占比(%)
-- amount_rate  成交占比(%)
-- float_values  流通市值
-- reason  原因/说明
CREATE TABLE top_list (symbol TEXT NOT NULL, date TEXT NOT NULL, name TEXT, close REAL, pct_change REAL, turnover_rate REAL, amount REAL, l_sell REAL, l_buy REAL, l_amount REAL, net_amount REAL, net_rate REAL, amount_rate REAL, float_values REAL, reason TEXT, UNIQUE (symbol, date, reason));

-- =========================================================
-- trade_cal
-- =========================================================
-- cal_date  日历日期
-- is_open  是否交易 1=是 0=否
-- pretrade_date  上一个交易日
CREATE TABLE trade_cal (cal_date TEXT PRIMARY KEY, is_open INTEGER, pretrade_date TEXT, UNIQUE (cal_date));

