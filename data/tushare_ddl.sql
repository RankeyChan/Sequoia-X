-- ===================================================
-- Tushare Pro Stock Data - MySQL DDL
-- Auto-generated from api_summary.json (104 tables)
-- ===================================================

CREATE DATABASE IF NOT EXISTS tushare DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tushare;


-- 本接口由Tushare自行生产，获取股票复权因子，可提取单只股票全部历史复权因子，也可以提取单日全部股票的复权因子。
DROP TABLE IF EXISTS `ts_adj_factor`;
CREATE TABLE `ts_adj_factor` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `adj_factor` DECIMAL(20,4) DEFAULT NULL COMMENT 'adj_factor',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='本接口由Tushare自行生产，获取股票复权因子，可提取单只股票全部历史复权因子，也可以提取单日全部股票的复权因子。';

-- 获取备用基础列表，数据从2016年开始
DROP TABLE IF EXISTS `ts_bak_basic`;
CREATE TABLE `ts_bak_basic` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `industry` VARCHAR(64) DEFAULT NULL COMMENT 'industry',
  `area` VARCHAR(64) DEFAULT NULL COMMENT 'area',
  `pe` DECIMAL(20,4) DEFAULT NULL COMMENT 'pe',
  `float_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_share',
  `total_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_share',
  `total_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_assets',
  `liquid_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'liquid_assets',
  `fixed_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'fixed_assets',
  `reserved` DECIMAL(20,4) DEFAULT NULL COMMENT 'reserved',
  `reserved_pershare` DECIMAL(20,4) DEFAULT NULL COMMENT 'reserved_pershare',
  `eps` DECIMAL(20,4) DEFAULT NULL COMMENT 'eps',
  `bvps` DECIMAL(20,4) DEFAULT NULL COMMENT 'bvps',
  `pb` DECIMAL(20,4) DEFAULT NULL COMMENT 'pb',
  `list_date` VARCHAR(64) DEFAULT NULL COMMENT 'list_date',
  `undp` DECIMAL(20,4) DEFAULT NULL COMMENT 'undp',
  `per_undp` DECIMAL(20,4) DEFAULT NULL COMMENT 'per_undp',
  `rev_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'rev_yoy',
  `profit_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'profit_yoy',
  `gpr` DECIMAL(20,4) DEFAULT NULL COMMENT 'gpr',
  `npr` DECIMAL(20,4) DEFAULT NULL COMMENT 'npr',
  `holder_num` INT DEFAULT NULL COMMENT 'holder_num',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取备用基础列表，数据从2016年开始';

-- 获取备用行情，包括特定的行情指标(数据从2017年中左右开始，早期有几天数据缺失，近期正常)
DROP TABLE IF EXISTS `ts_bak_daily`;
CREATE TABLE `ts_bak_daily` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `change` DECIMAL(20,4) DEFAULT NULL COMMENT 'change',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `pre_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close',
  `vol_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'vol_ratio',
  `turn_over` DECIMAL(20,4) DEFAULT NULL COMMENT 'turn_over',
  `swing` DECIMAL(20,4) DEFAULT NULL COMMENT 'swing',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `selling` DECIMAL(20,4) DEFAULT NULL COMMENT 'selling',
  `buying` DECIMAL(20,4) DEFAULT NULL COMMENT 'buying',
  `total_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_share',
  `float_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_share',
  `pe` DECIMAL(20,4) DEFAULT NULL COMMENT 'pe',
  `industry` VARCHAR(64) DEFAULT NULL COMMENT 'industry',
  `area` VARCHAR(64) DEFAULT NULL COMMENT 'area',
  `float_mv` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_mv',
  `total_mv` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_mv',
  `avg_price` DECIMAL(20,4) DEFAULT NULL COMMENT 'avg_price',
  `strength` VARCHAR(64) DEFAULT NULL COMMENT 'strength',
  `activity` DECIMAL(20,4) DEFAULT NULL COMMENT 'activity',
  `avg_turnover` DECIMAL(20,4) DEFAULT NULL COMMENT 'avg_turnover',
  `attack` DECIMAL(20,4) DEFAULT NULL COMMENT 'attack',
  `interval_3` DECIMAL(20,4) DEFAULT NULL COMMENT 'interval_3',
  `interval_6` DECIMAL(20,4) DEFAULT NULL COMMENT 'interval_6',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取备用行情，包括特定的行情指标(数据从2017年中左右开始，早期有几天数据缺失，近期正常)';

-- 获取上市公司资产负债表
DROP TABLE IF EXISTS `ts_balancesheet`;
CREATE TABLE `ts_balancesheet` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `f_ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'f_ann_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `report_type` VARCHAR(64) DEFAULT NULL COMMENT 'report_type',
  `comp_type` VARCHAR(64) DEFAULT NULL COMMENT 'comp_type',
  `end_type` VARCHAR(64) DEFAULT NULL COMMENT 'end_type',
  `total_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_share',
  `cap_rese` DECIMAL(20,4) DEFAULT NULL COMMENT 'cap_rese',
  `undistr_porfit` DECIMAL(20,4) DEFAULT NULL COMMENT 'undistr_porfit',
  `surplus_rese` DECIMAL(20,4) DEFAULT NULL COMMENT 'surplus_rese',
  `special_rese` DECIMAL(20,4) DEFAULT NULL COMMENT 'special_rese',
  `money_cap` DECIMAL(20,4) DEFAULT NULL COMMENT 'money_cap',
  `trad_asset` DECIMAL(20,4) DEFAULT NULL COMMENT 'trad_asset',
  `notes_receiv` DECIMAL(20,4) DEFAULT NULL COMMENT 'notes_receiv',
  `accounts_receiv` DECIMAL(20,4) DEFAULT NULL COMMENT 'accounts_receiv',
  `oth_receiv` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_receiv',
  `prepayment` DECIMAL(20,4) DEFAULT NULL COMMENT 'prepayment',
  `div_receiv` DECIMAL(20,4) DEFAULT NULL COMMENT 'div_receiv',
  `int_receiv` DECIMAL(20,4) DEFAULT NULL COMMENT 'int_receiv',
  `inventories` DECIMAL(20,4) DEFAULT NULL COMMENT 'inventories',
  `amor_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'amor_exp',
  `nca_within_1y` DECIMAL(20,4) DEFAULT NULL COMMENT 'nca_within_1y',
  `sett_rsrv` DECIMAL(20,4) DEFAULT NULL COMMENT 'sett_rsrv',
  `loanto_oth_bank_fi` DECIMAL(20,4) DEFAULT NULL COMMENT 'loanto_oth_bank_fi',
  `premium_receiv` DECIMAL(20,4) DEFAULT NULL COMMENT 'premium_receiv',
  `reinsur_receiv` DECIMAL(20,4) DEFAULT NULL COMMENT 'reinsur_receiv',
  `reinsur_res_receiv` DECIMAL(20,4) DEFAULT NULL COMMENT 'reinsur_res_receiv',
  `pur_resale_fa` DECIMAL(20,4) DEFAULT NULL COMMENT 'pur_resale_fa',
  `oth_cur_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_cur_assets',
  `total_cur_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_cur_assets',
  `fa_avail_for_sale` DECIMAL(20,4) DEFAULT NULL COMMENT 'fa_avail_for_sale',
  `htm_invest` DECIMAL(20,4) DEFAULT NULL COMMENT 'htm_invest',
  `lt_eqt_invest` DECIMAL(20,4) DEFAULT NULL COMMENT 'lt_eqt_invest',
  `invest_real_estate` DECIMAL(20,4) DEFAULT NULL COMMENT 'invest_real_estate',
  `time_deposits` DECIMAL(20,4) DEFAULT NULL COMMENT 'time_deposits',
  `oth_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_assets',
  `lt_rec` DECIMAL(20,4) DEFAULT NULL COMMENT 'lt_rec',
  `fix_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'fix_assets',
  `cip` DECIMAL(20,4) DEFAULT NULL COMMENT 'cip',
  `const_materials` DECIMAL(20,4) DEFAULT NULL COMMENT 'const_materials',
  `fixed_assets_disp` DECIMAL(20,4) DEFAULT NULL COMMENT 'fixed_assets_disp',
  `produc_bio_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'produc_bio_assets',
  `oil_and_gas_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'oil_and_gas_assets',
  `intan_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'intan_assets',
  `r_and_d` DECIMAL(20,4) DEFAULT NULL COMMENT 'r_and_d',
  `goodwill` DECIMAL(20,4) DEFAULT NULL COMMENT 'goodwill',
  `lt_amor_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'lt_amor_exp',
  `defer_tax_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'defer_tax_assets',
  `decr_in_disbur` DECIMAL(20,4) DEFAULT NULL COMMENT 'decr_in_disbur',
  `oth_nca` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_nca',
  `total_nca` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_nca',
  `cash_reser_cb` DECIMAL(20,4) DEFAULT NULL COMMENT 'cash_reser_cb',
  `depos_in_oth_bfi` DECIMAL(20,4) DEFAULT NULL COMMENT 'depos_in_oth_bfi',
  `prec_metals` DECIMAL(20,4) DEFAULT NULL COMMENT 'prec_metals',
  `deriv_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'deriv_assets',
  `rr_reins_une_prem` DECIMAL(20,4) DEFAULT NULL COMMENT 'rr_reins_une_prem',
  `rr_reins_outstd_cla` DECIMAL(20,4) DEFAULT NULL COMMENT 'rr_reins_outstd_cla',
  `rr_reins_lins_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'rr_reins_lins_liab',
  `rr_reins_lthins_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'rr_reins_lthins_liab',
  `refund_depos` DECIMAL(20,4) DEFAULT NULL COMMENT 'refund_depos',
  `ph_pledge_loans` DECIMAL(20,4) DEFAULT NULL COMMENT 'ph_pledge_loans',
  `refund_cap_depos` DECIMAL(20,4) DEFAULT NULL COMMENT 'refund_cap_depos',
  `indep_acct_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'indep_acct_assets',
  `client_depos` DECIMAL(20,4) DEFAULT NULL COMMENT 'client_depos',
  `client_prov` DECIMAL(20,4) DEFAULT NULL COMMENT 'client_prov',
  `transac_seat_fee` DECIMAL(20,4) DEFAULT NULL COMMENT 'transac_seat_fee',
  `invest_as_receiv` DECIMAL(20,4) DEFAULT NULL COMMENT 'invest_as_receiv',
  `total_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_assets',
  `lt_borr` DECIMAL(20,4) DEFAULT NULL COMMENT 'lt_borr',
  `st_borr` DECIMAL(20,4) DEFAULT NULL COMMENT 'st_borr',
  `cb_borr` DECIMAL(20,4) DEFAULT NULL COMMENT 'cb_borr',
  `depos_ib_deposits` DECIMAL(20,4) DEFAULT NULL COMMENT 'depos_ib_deposits',
  `loan_oth_bank` DECIMAL(20,4) DEFAULT NULL COMMENT 'loan_oth_bank',
  `trading_fl` DECIMAL(20,4) DEFAULT NULL COMMENT 'trading_fl',
  `notes_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'notes_payable',
  `acct_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'acct_payable',
  `adv_receipts` DECIMAL(20,4) DEFAULT NULL COMMENT 'adv_receipts',
  `sold_for_repur_fa` DECIMAL(20,4) DEFAULT NULL COMMENT 'sold_for_repur_fa',
  `comm_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'comm_payable',
  `payroll_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'payroll_payable',
  `taxes_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'taxes_payable',
  `int_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'int_payable',
  `div_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'div_payable',
  `oth_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_payable',
  `acc_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'acc_exp',
  `deferred_inc` DECIMAL(20,4) DEFAULT NULL COMMENT 'deferred_inc',
  `st_bonds_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'st_bonds_payable',
  `payable_to_reinsurer` DECIMAL(20,4) DEFAULT NULL COMMENT 'payable_to_reinsurer',
  `rsrv_insur_cont` DECIMAL(20,4) DEFAULT NULL COMMENT 'rsrv_insur_cont',
  `acting_trading_sec` DECIMAL(20,4) DEFAULT NULL COMMENT 'acting_trading_sec',
  `acting_uw_sec` DECIMAL(20,4) DEFAULT NULL COMMENT 'acting_uw_sec',
  `non_cur_liab_due_1y` DECIMAL(20,4) DEFAULT NULL COMMENT 'non_cur_liab_due_1y',
  `oth_cur_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_cur_liab',
  `total_cur_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_cur_liab',
  `bond_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'bond_payable',
  `lt_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'lt_payable',
  `specific_payables` DECIMAL(20,4) DEFAULT NULL COMMENT 'specific_payables',
  `estimated_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'estimated_liab',
  `defer_tax_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'defer_tax_liab',
  `defer_inc_non_cur_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'defer_inc_non_cur_liab',
  `oth_ncl` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_ncl',
  `total_ncl` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_ncl',
  `depos_oth_bfi` DECIMAL(20,4) DEFAULT NULL COMMENT 'depos_oth_bfi',
  `deriv_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'deriv_liab',
  `depos` DECIMAL(20,4) DEFAULT NULL COMMENT 'depos',
  `agency_bus_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'agency_bus_liab',
  `oth_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_liab',
  `prem_receiv_adva` DECIMAL(20,4) DEFAULT NULL COMMENT 'prem_receiv_adva',
  `depos_received` DECIMAL(20,4) DEFAULT NULL COMMENT 'depos_received',
  `ph_invest` DECIMAL(20,4) DEFAULT NULL COMMENT 'ph_invest',
  `reser_une_prem` DECIMAL(20,4) DEFAULT NULL COMMENT 'reser_une_prem',
  `reser_outstd_claims` DECIMAL(20,4) DEFAULT NULL COMMENT 'reser_outstd_claims',
  `reser_lins_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'reser_lins_liab',
  `reser_lthins_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'reser_lthins_liab',
  `indept_acc_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'indept_acc_liab',
  `pledge_borr` DECIMAL(20,4) DEFAULT NULL COMMENT 'pledge_borr',
  `indem_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'indem_payable',
  `policy_div_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'policy_div_payable',
  `total_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_liab',
  `treasury_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'treasury_share',
  `ordin_risk_reser` DECIMAL(20,4) DEFAULT NULL COMMENT 'ordin_risk_reser',
  `forex_differ` DECIMAL(20,4) DEFAULT NULL COMMENT 'forex_differ',
  `invest_loss_unconf` DECIMAL(20,4) DEFAULT NULL COMMENT 'invest_loss_unconf',
  `minority_int` DECIMAL(20,4) DEFAULT NULL COMMENT 'minority_int',
  `total_hldr_eqy_exc_min_int` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_hldr_eqy_exc_min_int',
  `total_hldr_eqy_inc_min_int` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_hldr_eqy_inc_min_int',
  `total_liab_hldr_eqy` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_liab_hldr_eqy',
  `lt_payroll_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'lt_payroll_payable',
  `oth_comp_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_comp_income',
  `oth_eqt_tools` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_eqt_tools',
  `oth_eqt_tools_p_shr` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_eqt_tools_p_shr',
  `lending_funds` DECIMAL(20,4) DEFAULT NULL COMMENT 'lending_funds',
  `acc_receivable` DECIMAL(20,4) DEFAULT NULL COMMENT 'acc_receivable',
  `st_fin_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'st_fin_payable',
  `payables` DECIMAL(20,4) DEFAULT NULL COMMENT 'payables',
  `hfs_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'hfs_assets',
  `hfs_sales` DECIMAL(20,4) DEFAULT NULL COMMENT 'hfs_sales',
  `cost_fin_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'cost_fin_assets',
  `fair_value_fin_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'fair_value_fin_assets',
  `contract_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'contract_assets',
  `contract_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'contract_liab',
  `accounts_receiv_bill` DECIMAL(20,4) DEFAULT NULL COMMENT 'accounts_receiv_bill',
  `accounts_pay` DECIMAL(20,4) DEFAULT NULL COMMENT 'accounts_pay',
  `oth_rcv_total` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_rcv_total',
  `fix_assets_total` DECIMAL(20,4) DEFAULT NULL COMMENT 'fix_assets_total',
  `cip_total` DECIMAL(20,4) DEFAULT NULL COMMENT 'cip_total',
  `oth_pay_total` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_pay_total',
  `long_pay_total` DECIMAL(20,4) DEFAULT NULL COMMENT 'long_pay_total',
  `debt_invest` DECIMAL(20,4) DEFAULT NULL COMMENT 'debt_invest',
  `oth_debt_invest` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_debt_invest',
  `update_flag` VARCHAR(64) DEFAULT NULL COMMENT 'update_flag',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司资产负债表';

-- 大宗交易
DROP TABLE IF EXISTS `ts_block_trade`;
CREATE TABLE `ts_block_trade` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `price` DECIMAL(20,4) DEFAULT NULL COMMENT 'price',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `buyer` VARCHAR(64) DEFAULT NULL COMMENT 'buyer',
  `seller` VARCHAR(64) DEFAULT NULL COMMENT 'seller',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='大宗交易';

-- 获取券商月度金股，一般1日~3日内更新当月数据
DROP TABLE IF EXISTS `ts_broker_recommend`;
CREATE TABLE `ts_broker_recommend` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `month` DECIMAL(20,4) DEFAULT NULL COMMENT 'month',
  `broker` VARCHAR(64) DEFAULT NULL COMMENT 'broker',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取券商月度金股，一般1日~3日内更新当月数据';

-- 获取北交所股票代码变更后新旧代码映射表数据
DROP TABLE IF EXISTS `ts_bse_mapping`;
CREATE TABLE `ts_bse_mapping` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `o_code` VARCHAR(64) NOT NULL COMMENT 'o_code',
  `n_code` VARCHAR(64) NOT NULL COMMENT 'n_code',
  `list_date` VARCHAR(64) DEFAULT NULL COMMENT 'list_date',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取北交所股票代码变更后新旧代码映射表数据';

-- 获取上市公司现金流量表
DROP TABLE IF EXISTS `ts_cashflow`;
CREATE TABLE `ts_cashflow` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `f_ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'f_ann_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `comp_type` VARCHAR(64) DEFAULT NULL COMMENT 'comp_type',
  `report_type` VARCHAR(64) DEFAULT NULL COMMENT 'report_type',
  `end_type` VARCHAR(64) DEFAULT NULL COMMENT 'end_type',
  `net_profit` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_profit',
  `finan_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'finan_exp',
  `c_fr_sale_sg` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_fr_sale_sg',
  `recp_tax_rends` DECIMAL(20,4) DEFAULT NULL COMMENT 'recp_tax_rends',
  `n_depos_incr_fi` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_depos_incr_fi',
  `n_incr_loans_cb` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_incr_loans_cb',
  `n_inc_borr_oth_fi` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_inc_borr_oth_fi',
  `prem_fr_orig_contr` DECIMAL(20,4) DEFAULT NULL COMMENT 'prem_fr_orig_contr',
  `n_incr_insured_dep` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_incr_insured_dep',
  `n_reinsur_prem` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_reinsur_prem',
  `n_incr_disp_tfa` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_incr_disp_tfa',
  `ifc_cash_incr` DECIMAL(20,4) DEFAULT NULL COMMENT 'ifc_cash_incr',
  `n_incr_disp_faas` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_incr_disp_faas',
  `n_incr_loans_oth_bank` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_incr_loans_oth_bank',
  `n_cap_incr_repur` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_cap_incr_repur',
  `c_fr_oth_operate_a` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_fr_oth_operate_a',
  `c_inf_fr_operate_a` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_inf_fr_operate_a',
  `c_paid_goods_s` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_paid_goods_s',
  `c_paid_to_for_empl` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_paid_to_for_empl',
  `c_paid_for_taxes` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_paid_for_taxes',
  `n_incr_clt_loan_adv` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_incr_clt_loan_adv',
  `n_incr_dep_cbob` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_incr_dep_cbob',
  `c_pay_claims_orig_inco` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_pay_claims_orig_inco',
  `pay_handling_chrg` DECIMAL(20,4) DEFAULT NULL COMMENT 'pay_handling_chrg',
  `pay_comm_insur_plcy` DECIMAL(20,4) DEFAULT NULL COMMENT 'pay_comm_insur_plcy',
  `oth_cash_pay_oper_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_cash_pay_oper_act',
  `st_cash_out_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'st_cash_out_act',
  `n_cashflow_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_cashflow_act',
  `oth_recp_ral_inv_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_recp_ral_inv_act',
  `c_disp_withdrwl_invest` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_disp_withdrwl_invest',
  `c_recp_return_invest` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_recp_return_invest',
  `n_recp_disp_fiolta` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_recp_disp_fiolta',
  `n_recp_disp_sobu` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_recp_disp_sobu',
  `stot_inflows_inv_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'stot_inflows_inv_act',
  `c_pay_acq_const_fiolta` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_pay_acq_const_fiolta',
  `c_paid_invest` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_paid_invest',
  `n_disp_subs_oth_biz` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_disp_subs_oth_biz',
  `oth_pay_ral_inv_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_pay_ral_inv_act',
  `n_incr_pledge_loan` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_incr_pledge_loan',
  `stot_out_inv_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'stot_out_inv_act',
  `n_cashflow_inv_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_cashflow_inv_act',
  `c_recp_borrow` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_recp_borrow',
  `proc_issue_bonds` DECIMAL(20,4) DEFAULT NULL COMMENT 'proc_issue_bonds',
  `oth_cash_recp_ral_fnc_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_cash_recp_ral_fnc_act',
  `stot_cash_in_fnc_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'stot_cash_in_fnc_act',
  `free_cashflow` DECIMAL(20,4) DEFAULT NULL COMMENT 'free_cashflow',
  `c_prepay_amt_borr` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_prepay_amt_borr',
  `c_pay_dist_dpcp_int_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_pay_dist_dpcp_int_exp',
  `incl_dvd_profit_paid_sc_ms` DECIMAL(20,4) DEFAULT NULL COMMENT 'incl_dvd_profit_paid_sc_ms',
  `oth_cashpay_ral_fnc_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_cashpay_ral_fnc_act',
  `stot_cashout_fnc_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'stot_cashout_fnc_act',
  `n_cash_flows_fnc_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_cash_flows_fnc_act',
  `eff_fx_flu_cash` DECIMAL(20,4) DEFAULT NULL COMMENT 'eff_fx_flu_cash',
  `n_incr_cash_cash_equ` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_incr_cash_cash_equ',
  `c_cash_equ_beg_period` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_cash_equ_beg_period',
  `c_cash_equ_end_period` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_cash_equ_end_period',
  `c_recp_cap_contrib` DECIMAL(20,4) DEFAULT NULL COMMENT 'c_recp_cap_contrib',
  `incl_cash_rec_saims` DECIMAL(20,4) DEFAULT NULL COMMENT 'incl_cash_rec_saims',
  `uncon_invest_loss` DECIMAL(20,4) DEFAULT NULL COMMENT 'uncon_invest_loss',
  `prov_depr_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'prov_depr_assets',
  `depr_fa_coga_dpba` DECIMAL(20,4) DEFAULT NULL COMMENT 'depr_fa_coga_dpba',
  `amort_intang_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'amort_intang_assets',
  `lt_amort_deferred_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'lt_amort_deferred_exp',
  `decr_deferred_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'decr_deferred_exp',
  `incr_acc_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'incr_acc_exp',
  `loss_disp_fiolta` DECIMAL(20,4) DEFAULT NULL COMMENT 'loss_disp_fiolta',
  `loss_scr_fa` DECIMAL(20,4) DEFAULT NULL COMMENT 'loss_scr_fa',
  `loss_fv_chg` DECIMAL(20,4) DEFAULT NULL COMMENT 'loss_fv_chg',
  `invest_loss` DECIMAL(20,4) DEFAULT NULL COMMENT 'invest_loss',
  `decr_def_inc_tax_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'decr_def_inc_tax_assets',
  `incr_def_inc_tax_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'incr_def_inc_tax_liab',
  `decr_inventories` DECIMAL(20,4) DEFAULT NULL COMMENT 'decr_inventories',
  `decr_oper_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'decr_oper_payable',
  `incr_oper_payable` DECIMAL(20,4) DEFAULT NULL COMMENT 'incr_oper_payable',
  `others` DECIMAL(20,4) DEFAULT NULL COMMENT 'others',
  `im_net_cashflow_oper_act` DECIMAL(20,4) DEFAULT NULL COMMENT 'im_net_cashflow_oper_act',
  `conv_debt_into_cap` DECIMAL(20,4) DEFAULT NULL COMMENT 'conv_debt_into_cap',
  `conv_copbonds_due_within_1y` DECIMAL(20,4) DEFAULT NULL COMMENT 'conv_copbonds_due_within_1y',
  `fa_fnc_leases` DECIMAL(20,4) DEFAULT NULL COMMENT 'fa_fnc_leases',
  `im_n_incr_cash_equ` DECIMAL(20,4) DEFAULT NULL COMMENT 'im_n_incr_cash_equ',
  `net_dism_capital_add` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_dism_capital_add',
  `net_cash_rece_sec` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_cash_rece_sec',
  `credit_impa_loss` DECIMAL(20,4) DEFAULT NULL COMMENT 'credit_impa_loss',
  `use_right_asset_dep` DECIMAL(20,4) DEFAULT NULL COMMENT 'use_right_asset_dep',
  `oth_loss_asset` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_loss_asset',
  `end_bal_cash` DECIMAL(20,4) DEFAULT NULL COMMENT 'end_bal_cash',
  `beg_bal_cash` DECIMAL(20,4) DEFAULT NULL COMMENT 'beg_bal_cash',
  `end_bal_cash_equ` DECIMAL(20,4) DEFAULT NULL COMMENT 'end_bal_cash_equ',
  `beg_bal_cash_equ` DECIMAL(20,4) DEFAULT NULL COMMENT 'beg_bal_cash_equ',
  `update_flag` VARCHAR(64) DEFAULT NULL COMMENT 'update_flag',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司现金流量表';

-- 获取中央结算系统持股汇总数据，覆盖全部历史数据，根据交易所披露时间，当日数据在下一交易日早上9点前完成入库
DROP TABLE IF EXISTS `ts_ccass_hold`;
CREATE TABLE `ts_ccass_hold` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `shareholding` DECIMAL(20,4) DEFAULT NULL COMMENT 'shareholding',
  `hold_nums` VARCHAR(64) DEFAULT NULL COMMENT 'hold_nums',
  `hold_ratio` VARCHAR(64) DEFAULT NULL COMMENT 'hold_ratio',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取中央结算系统持股汇总数据，覆盖全部历史数据，根据交易所披露时间，当日数据在下一交易日早上9点前完成入库';

-- 获取中央结算系统机构席位持股明细，数据覆盖
DROP TABLE IF EXISTS `ts_ccass_hold_detail`;
CREATE TABLE `ts_ccass_hold_detail` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `col_participant_id` VARCHAR(64) DEFAULT NULL COMMENT 'col_participant_id',
  `col_participant_name` VARCHAR(64) DEFAULT NULL COMMENT 'col_participant_name',
  `col_shareholding` DECIMAL(20,4) DEFAULT NULL COMMENT 'col_shareholding',
  `col_shareholding_percent` DECIMAL(20,4) DEFAULT NULL COMMENT 'col_shareholding_percent',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取中央结算系统机构席位持股明细，数据覆盖';

-- 获取A股每日的筹码分布情况，提供各价位占比，数据从2018年开始，每天18~19点之间更新当日数据
DROP TABLE IF EXISTS `ts_cyq_chips`;
CREATE TABLE `ts_cyq_chips` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `price` DECIMAL(20,4) DEFAULT NULL COMMENT 'price',
  `percent` DECIMAL(20,4) DEFAULT NULL COMMENT 'percent',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取A股每日的筹码分布情况，提供各价位占比，数据从2018年开始，每天18~19点之间更新当日数据';

-- 获取A股每日筹码平均成本和胜率情况，每天18~19点左右更新，数据从2018年开始
DROP TABLE IF EXISTS `ts_cyq_perf`;
CREATE TABLE `ts_cyq_perf` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `his_low` DECIMAL(20,4) DEFAULT NULL COMMENT 'his_low',
  `his_high` DECIMAL(20,4) DEFAULT NULL COMMENT 'his_high',
  `cost_5pct` DECIMAL(20,4) DEFAULT NULL COMMENT 'cost_5pct',
  `cost_15pct` DECIMAL(20,4) DEFAULT NULL COMMENT 'cost_15pct',
  `cost_50pct` DECIMAL(20,4) DEFAULT NULL COMMENT 'cost_50pct',
  `cost_85pct` DECIMAL(20,4) DEFAULT NULL COMMENT 'cost_85pct',
  `cost_95pct` DECIMAL(20,4) DEFAULT NULL COMMENT 'cost_95pct',
  `weight_avg` DECIMAL(20,4) DEFAULT NULL COMMENT 'weight_avg',
  `winner_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'winner_rate',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取A股每日筹码平均成本和胜率情况，每天18~19点左右更新，数据从2018年开始';

-- 获取股票行情数据，或通过通用行情接口获取数据，包含了前后复权数据
DROP TABLE IF EXISTS `ts_daily`;
CREATE TABLE `ts_daily` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `pre_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close',
  `change` DECIMAL(20,4) DEFAULT NULL COMMENT 'change',
  `pct_chg` VARCHAR(64) DEFAULT NULL COMMENT 'pct_chg',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取股票行情数据，或通过通用行情接口获取数据，包含了前后复权数据';

-- 获取全部股票每日重要的基本面指标，可用于选股分析、报表展示等。单次请求最大返回6000条数据，可按日线循环提取全部历史。
DROP TABLE IF EXISTS `ts_daily_basic`;
CREATE TABLE `ts_daily_basic` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `turnover_rate` VARCHAR(64) DEFAULT NULL COMMENT 'turnover_rate',
  `turnover_rate_f` DECIMAL(20,4) DEFAULT NULL COMMENT 'turnover_rate_f',
  `volume_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'volume_ratio',
  `pe` DECIMAL(20,4) DEFAULT NULL COMMENT 'pe',
  `pe_ttm` DECIMAL(20,4) DEFAULT NULL COMMENT 'pe_ttm',
  `pb` DECIMAL(20,4) DEFAULT NULL COMMENT 'pb',
  `ps` DECIMAL(20,4) DEFAULT NULL COMMENT 'ps',
  `ps_ttm` DECIMAL(20,4) DEFAULT NULL COMMENT 'ps_ttm',
  `dv_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'dv_ratio',
  `dv_ttm` DECIMAL(20,4) DEFAULT NULL COMMENT 'dv_ttm',
  `total_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_share',
  `float_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_share',
  `free_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'free_share',
  `total_mv` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_mv',
  `circ_mv` DECIMAL(20,4) DEFAULT NULL COMMENT 'circ_mv',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取全部股票每日重要的基本面指标，可用于选股分析、报表展示等。单次请求最大返回6000条数据，可按日线循环提取全部历史。';

-- 获取概念题材列表，每天盘后更新
DROP TABLE IF EXISTS `ts_dc_concept`;
CREATE TABLE `ts_dc_concept` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `theme_code` VARCHAR(64) NOT NULL COMMENT 'theme_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `hot` VARCHAR(64) DEFAULT NULL COMMENT 'hot',
  `sort` VARCHAR(64) DEFAULT NULL COMMENT 'sort',
  `strength` VARCHAR(64) DEFAULT NULL COMMENT 'strength',
  `z_t_num` VARCHAR(64) DEFAULT NULL COMMENT 'z_t_num',
  `main_change` VARCHAR(64) DEFAULT NULL COMMENT 'main_change',
  `lead_stock` VARCHAR(64) DEFAULT NULL COMMENT 'lead_stock',
  `lead_stock_code` VARCHAR(64) DEFAULT NULL COMMENT 'lead_stock_code',
  `lead_stock_pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'lead_stock_pct_change',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_trade_date` (`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取概念题材列表，每天盘后更新';

-- 获取概念题材的成分股，每天盘后更新
DROP TABLE IF EXISTS `ts_dc_concept_cons`;
CREATE TABLE `ts_dc_concept_cons` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `theme_code` VARCHAR(64) NOT NULL COMMENT 'theme_code',
  `industry_code` VARCHAR(64) DEFAULT NULL COMMENT 'industry_code',
  `industry` VARCHAR(64) DEFAULT NULL COMMENT 'industry',
  `reason` VARCHAR(64) DEFAULT NULL COMMENT 'reason',
  `hot_num` VARCHAR(64) DEFAULT NULL COMMENT 'hot_num',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取概念题材的成分股，每天盘后更新';

-- 获取概念板块、行业指数板块、地域板块行情数据，历史数据开始于2020年
DROP TABLE IF EXISTS `ts_dc_daily`;
CREATE TABLE `ts_dc_daily` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `change` DECIMAL(20,4) DEFAULT NULL COMMENT 'change',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `swing` DECIMAL(20,4) DEFAULT NULL COMMENT 'swing',
  `turnover_rate` VARCHAR(64) DEFAULT NULL COMMENT 'turnover_rate',
  `category` VARCHAR(64) DEFAULT NULL COMMENT 'category',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取概念板块、行业指数板块、地域板块行情数据，历史数据开始于2020年';

-- 获取热榜数据，包括A股市场、ETF基金、港股市场、美股市场等等，每日盘中提取4次，收盘后4次，最晚22点提取一次。
DROP TABLE IF EXISTS `ts_dc_hot`;
CREATE TABLE `ts_dc_hot` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `data_type` VARCHAR(64) DEFAULT NULL COMMENT 'data_type',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ts_name` DECIMAL(20,4) DEFAULT NULL COMMENT 'ts_name',
  `rank` INT DEFAULT NULL COMMENT 'rank',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `current_price` DECIMAL(20,4) DEFAULT NULL COMMENT 'current_price',
  `hot` VARCHAR(64) DEFAULT NULL COMMENT 'hot',
  `concept` VARCHAR(64) DEFAULT NULL COMMENT 'concept',
  `rank_time` VARCHAR(64) DEFAULT NULL COMMENT 'rank_time',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取热榜数据，包括A股市场、ETF基金、港股市场、美股市场等等，每日盘中提取4次，收盘后4次，最晚22点提取一次。';

-- 获取每个交易日的概念板块数据，支持按日期查询
DROP TABLE IF EXISTS `ts_dc_index`;
CREATE TABLE `ts_dc_index` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `leading` DECIMAL(20,4) DEFAULT NULL COMMENT 'leading',
  `leading_code` DECIMAL(20,4) DEFAULT NULL COMMENT 'leading_code',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `leading_pct` DECIMAL(20,4) DEFAULT NULL COMMENT 'leading_pct',
  `total_mv` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_mv',
  `turnover_rate` VARCHAR(64) DEFAULT NULL COMMENT 'turnover_rate',
  `up_num` INT DEFAULT NULL COMMENT 'up_num',
  `down_num` INT DEFAULT NULL COMMENT 'down_num',
  `idx_type` VARCHAR(64) DEFAULT NULL COMMENT 'idx_type',
  `level` DECIMAL(20,4) DEFAULT NULL COMMENT 'level',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取每个交易日的概念板块数据，支持按日期查询';

-- 获取板块每日成分数据，可以根据概念板块代码和交易日期，获取历史成分
DROP TABLE IF EXISTS `ts_dc_member`;
CREATE TABLE `ts_dc_member` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `con_code` VARCHAR(64) NOT NULL COMMENT 'con_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取板块每日成分数据，可以根据概念板块代码和交易日期，获取历史成分';

-- 获取财报披露计划日期
DROP TABLE IF EXISTS `ts_disclosure_date`;
CREATE TABLE `ts_disclosure_date` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `pre_date` VARCHAR(64) DEFAULT NULL COMMENT 'pre_date',
  `actual_date` VARCHAR(64) DEFAULT NULL COMMENT 'actual_date',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取财报披露计划日期';

-- 分红送股数据
DROP TABLE IF EXISTS `ts_dividend`;
CREATE TABLE `ts_dividend` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `div_proc` VARCHAR(64) DEFAULT NULL COMMENT 'div_proc',
  `stk_div` DECIMAL(20,4) DEFAULT NULL COMMENT 'stk_div',
  `stk_bo_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'stk_bo_rate',
  `stk_co_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'stk_co_rate',
  `cash_div` DECIMAL(20,4) DEFAULT NULL COMMENT 'cash_div',
  `cash_div_tax` DECIMAL(20,4) DEFAULT NULL COMMENT 'cash_div_tax',
  `record_date` VARCHAR(64) DEFAULT NULL COMMENT 'record_date',
  `ex_date` VARCHAR(64) DEFAULT NULL COMMENT 'ex_date',
  `pay_date` VARCHAR(64) DEFAULT NULL COMMENT 'pay_date',
  `div_listdate` VARCHAR(64) DEFAULT NULL COMMENT 'div_listdate',
  `imp_ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'imp_ann_date',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='分红送股数据';

-- 获取上市公司业绩快报
DROP TABLE IF EXISTS `ts_express`;
CREATE TABLE `ts_express` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `revenue` DECIMAL(20,4) DEFAULT NULL COMMENT 'revenue',
  `operate_profit` DECIMAL(20,4) DEFAULT NULL COMMENT 'operate_profit',
  `total_profit` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_profit',
  `n_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_income',
  `total_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_assets',
  `total_hldr_eqy_exc_min_int` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_hldr_eqy_exc_min_int',
  `diluted_eps` DECIMAL(20,4) DEFAULT NULL COMMENT 'diluted_eps',
  `diluted_roe` DECIMAL(20,4) DEFAULT NULL COMMENT 'diluted_roe',
  `yoy_net_profit` DECIMAL(20,4) DEFAULT NULL COMMENT 'yoy_net_profit',
  `bps` DECIMAL(20,4) DEFAULT NULL COMMENT 'bps',
  `perf_summary` VARCHAR(64) DEFAULT NULL COMMENT 'perf_summary',
  `update_flag` VARCHAR(64) DEFAULT NULL COMMENT 'update_flag',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司业绩快报';

-- 获取上市公司定期财务审计意见数据
DROP TABLE IF EXISTS `ts_fina_audit`;
CREATE TABLE `ts_fina_audit` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `audit_result` VARCHAR(64) DEFAULT NULL COMMENT 'audit_result',
  `audit_fees` DECIMAL(20,4) DEFAULT NULL COMMENT 'audit_fees',
  `audit_agency` VARCHAR(64) DEFAULT NULL COMMENT 'audit_agency',
  `audit_sign` VARCHAR(64) DEFAULT NULL COMMENT 'audit_sign',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司定期财务审计意见数据';

-- 获取上市公司财务指标数据，为避免服务器压力，现阶段每次请求最多返回100条记录，可通过设置日期多次请求获取更多数据。
DROP TABLE IF EXISTS `ts_fina_indicator`;
CREATE TABLE `ts_fina_indicator` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `eps` DECIMAL(20,4) DEFAULT NULL COMMENT 'eps',
  `dt_eps` DECIMAL(20,4) DEFAULT NULL COMMENT 'dt_eps',
  `total_revenue_ps` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_revenue_ps',
  `revenue_ps` DECIMAL(20,4) DEFAULT NULL COMMENT 'revenue_ps',
  `capital_rese_ps` DECIMAL(20,4) DEFAULT NULL COMMENT 'capital_rese_ps',
  `surplus_rese_ps` DECIMAL(20,4) DEFAULT NULL COMMENT 'surplus_rese_ps',
  `undist_profit_ps` DECIMAL(20,4) DEFAULT NULL COMMENT 'undist_profit_ps',
  `extra_item` DECIMAL(20,4) DEFAULT NULL COMMENT 'extra_item',
  `profit_dedt` DECIMAL(20,4) DEFAULT NULL COMMENT 'profit_dedt',
  `gross_margin` DECIMAL(20,4) DEFAULT NULL COMMENT 'gross_margin',
  `current_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'current_ratio',
  `quick_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'quick_ratio',
  `cash_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'cash_ratio',
  `ar_turn` DECIMAL(20,4) DEFAULT NULL COMMENT 'ar_turn',
  `ca_turn` DECIMAL(20,4) DEFAULT NULL COMMENT 'ca_turn',
  `fa_turn` DECIMAL(20,4) DEFAULT NULL COMMENT 'fa_turn',
  `assets_turn` DECIMAL(20,4) DEFAULT NULL COMMENT 'assets_turn',
  `op_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'op_income',
  `ebit` DECIMAL(20,4) DEFAULT NULL COMMENT 'ebit',
  `ebitda` DECIMAL(20,4) DEFAULT NULL COMMENT 'ebitda',
  `fcff` DECIMAL(20,4) DEFAULT NULL COMMENT 'fcff',
  `fcfe` DECIMAL(20,4) DEFAULT NULL COMMENT 'fcfe',
  `current_exint` DECIMAL(20,4) DEFAULT NULL COMMENT 'current_exint',
  `noncurrent_exint` DECIMAL(20,4) DEFAULT NULL COMMENT 'noncurrent_exint',
  `interestdebt` DECIMAL(20,4) DEFAULT NULL COMMENT 'interestdebt',
  `netdebt` DECIMAL(20,4) DEFAULT NULL COMMENT 'netdebt',
  `tangible_asset` DECIMAL(20,4) DEFAULT NULL COMMENT 'tangible_asset',
  `working_capital` DECIMAL(20,4) DEFAULT NULL COMMENT 'working_capital',
  `networking_capital` DECIMAL(20,4) DEFAULT NULL COMMENT 'networking_capital',
  `invest_capital` DECIMAL(20,4) DEFAULT NULL COMMENT 'invest_capital',
  `retained_earnings` DECIMAL(20,4) DEFAULT NULL COMMENT 'retained_earnings',
  `diluted2_eps` DECIMAL(20,4) DEFAULT NULL COMMENT 'diluted2_eps',
  `bps` DECIMAL(20,4) DEFAULT NULL COMMENT 'bps',
  `ocfps` DECIMAL(20,4) DEFAULT NULL COMMENT 'ocfps',
  `retainedps` DECIMAL(20,4) DEFAULT NULL COMMENT 'retainedps',
  `cfps` DECIMAL(20,4) DEFAULT NULL COMMENT 'cfps',
  `ebit_ps` DECIMAL(20,4) DEFAULT NULL COMMENT 'ebit_ps',
  `fcff_ps` DECIMAL(20,4) DEFAULT NULL COMMENT 'fcff_ps',
  `fcfe_ps` DECIMAL(20,4) DEFAULT NULL COMMENT 'fcfe_ps',
  `netprofit_margin` DECIMAL(20,4) DEFAULT NULL COMMENT 'netprofit_margin',
  `grossprofit_margin` DECIMAL(20,4) DEFAULT NULL COMMENT 'grossprofit_margin',
  `cogs_of_sales` DECIMAL(20,4) DEFAULT NULL COMMENT 'cogs_of_sales',
  `expense_of_sales` DECIMAL(20,4) DEFAULT NULL COMMENT 'expense_of_sales',
  `profit_to_gr` DECIMAL(20,4) DEFAULT NULL COMMENT 'profit_to_gr',
  `saleexp_to_gr` DECIMAL(20,4) DEFAULT NULL COMMENT 'saleexp_to_gr',
  `adminexp_of_gr` DECIMAL(20,4) DEFAULT NULL COMMENT 'adminexp_of_gr',
  `finaexp_of_gr` DECIMAL(20,4) DEFAULT NULL COMMENT 'finaexp_of_gr',
  `impai_ttm` DECIMAL(20,4) DEFAULT NULL COMMENT 'impai_ttm',
  `gc_of_gr` DECIMAL(20,4) DEFAULT NULL COMMENT 'gc_of_gr',
  `op_of_gr` DECIMAL(20,4) DEFAULT NULL COMMENT 'op_of_gr',
  `ebit_of_gr` DECIMAL(20,4) DEFAULT NULL COMMENT 'ebit_of_gr',
  `roe` DECIMAL(20,4) DEFAULT NULL COMMENT 'roe',
  `roe_waa` DECIMAL(20,4) DEFAULT NULL COMMENT 'roe_waa',
  `roe_dt` DECIMAL(20,4) DEFAULT NULL COMMENT 'roe_dt',
  `roa` DECIMAL(20,4) DEFAULT NULL COMMENT 'roa',
  `npta` DECIMAL(20,4) DEFAULT NULL COMMENT 'npta',
  `roic` DECIMAL(20,4) DEFAULT NULL COMMENT 'roic',
  `roe_yearly` DECIMAL(20,4) DEFAULT NULL COMMENT 'roe_yearly',
  `roa2_yearly` DECIMAL(20,4) DEFAULT NULL COMMENT 'roa2_yearly',
  `debt_to_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'debt_to_assets',
  `assets_to_eqt` DECIMAL(20,4) DEFAULT NULL COMMENT 'assets_to_eqt',
  `dp_assets_to_eqt` DECIMAL(20,4) DEFAULT NULL COMMENT 'dp_assets_to_eqt',
  `ca_to_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'ca_to_assets',
  `nca_to_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'nca_to_assets',
  `tbassets_to_totalassets` DECIMAL(20,4) DEFAULT NULL COMMENT 'tbassets_to_totalassets',
  `int_to_talcap` DECIMAL(20,4) DEFAULT NULL COMMENT 'int_to_talcap',
  `eqt_to_talcapital` DECIMAL(20,4) DEFAULT NULL COMMENT 'eqt_to_talcapital',
  `currentdebt_to_debt` DECIMAL(20,4) DEFAULT NULL COMMENT 'currentdebt_to_debt',
  `longdeb_to_debt` DECIMAL(20,4) DEFAULT NULL COMMENT 'longdeb_to_debt',
  `ocf_to_shortdebt` DECIMAL(20,4) DEFAULT NULL COMMENT 'ocf_to_shortdebt',
  `debt_to_eqt` DECIMAL(20,4) DEFAULT NULL COMMENT 'debt_to_eqt',
  `eqt_to_debt` DECIMAL(20,4) DEFAULT NULL COMMENT 'eqt_to_debt',
  `eqt_to_interestdebt` DECIMAL(20,4) DEFAULT NULL COMMENT 'eqt_to_interestdebt',
  `tangibleasset_to_debt` DECIMAL(20,4) DEFAULT NULL COMMENT 'tangibleasset_to_debt',
  `tangasset_to_intdebt` DECIMAL(20,4) DEFAULT NULL COMMENT 'tangasset_to_intdebt',
  `tangibleasset_to_netdebt` DECIMAL(20,4) DEFAULT NULL COMMENT 'tangibleasset_to_netdebt',
  `ocf_to_debt` DECIMAL(20,4) DEFAULT NULL COMMENT 'ocf_to_debt',
  `turn_days` DECIMAL(20,4) DEFAULT NULL COMMENT 'turn_days',
  `roa_yearly` DECIMAL(20,4) DEFAULT NULL COMMENT 'roa_yearly',
  `roa_dp` DECIMAL(20,4) DEFAULT NULL COMMENT 'roa_dp',
  `fixed_assets` DECIMAL(20,4) DEFAULT NULL COMMENT 'fixed_assets',
  `profit_to_op` DECIMAL(20,4) DEFAULT NULL COMMENT 'profit_to_op',
  `q_saleexp_to_gr` DECIMAL(20,4) DEFAULT NULL COMMENT 'q_saleexp_to_gr',
  `q_gc_to_gr` DECIMAL(20,4) DEFAULT NULL COMMENT 'q_gc_to_gr',
  `q_roe` DECIMAL(20,4) DEFAULT NULL COMMENT 'q_roe',
  `q_dt_roe` DECIMAL(20,4) DEFAULT NULL COMMENT 'q_dt_roe',
  `q_npta` DECIMAL(20,4) DEFAULT NULL COMMENT 'q_npta',
  `q_ocf_to_sales` DECIMAL(20,4) DEFAULT NULL COMMENT 'q_ocf_to_sales',
  `basic_eps_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'basic_eps_yoy',
  `dt_eps_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'dt_eps_yoy',
  `cfps_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'cfps_yoy',
  `op_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'op_yoy',
  `ebt_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'ebt_yoy',
  `netprofit_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'netprofit_yoy',
  `dt_netprofit_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'dt_netprofit_yoy',
  `ocf_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'ocf_yoy',
  `roe_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'roe_yoy',
  `bps_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'bps_yoy',
  `assets_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'assets_yoy',
  `eqt_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'eqt_yoy',
  `tr_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'tr_yoy',
  `or_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'or_yoy',
  `q_sales_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'q_sales_yoy',
  `q_op_qoq` DECIMAL(20,4) DEFAULT NULL COMMENT 'q_op_qoq',
  `equity_yoy` DECIMAL(20,4) DEFAULT NULL COMMENT 'equity_yoy',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司财务指标数据，为避免服务器压力，现阶段每次请求最多返回100条记录，可通过设置日期多次请求获取更多数据。';

-- 获得上市公司主营业务构成，分地区和产品两种方式
DROP TABLE IF EXISTS `ts_fina_mainbz`;
CREATE TABLE `ts_fina_mainbz` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `bz_item` DECIMAL(20,4) DEFAULT NULL COMMENT 'bz_item',
  `bz_code` DECIMAL(20,4) DEFAULT NULL COMMENT 'bz_code',
  `bz_sales` DECIMAL(20,4) DEFAULT NULL COMMENT 'bz_sales',
  `bz_profit` DECIMAL(20,4) DEFAULT NULL COMMENT 'bz_profit',
  `bz_cost` DECIMAL(20,4) DEFAULT NULL COMMENT 'bz_cost',
  `curr_type` VARCHAR(64) DEFAULT NULL COMMENT 'curr_type',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获得上市公司主营业务构成，分地区和产品两种方式';

-- 获取业绩预告数据
DROP TABLE IF EXISTS `ts_forecast`;
CREATE TABLE `ts_forecast` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `type` VARCHAR(64) DEFAULT NULL COMMENT 'type',
  `p_change_min` DECIMAL(20,4) DEFAULT NULL COMMENT 'p_change_min',
  `p_change_max` DECIMAL(20,4) DEFAULT NULL COMMENT 'p_change_max',
  `net_profit_min` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_profit_min',
  `net_profit_max` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_profit_max',
  `last_parent_net` DECIMAL(20,4) DEFAULT NULL COMMENT 'last_parent_net',
  `first_ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'first_ann_date',
  `summary` VARCHAR(64) DEFAULT NULL COMMENT 'summary',
  `change_reason` VARCHAR(64) DEFAULT NULL COMMENT 'change_reason',
  `update_flag` VARCHAR(64) DEFAULT NULL COMMENT 'update_flag',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取业绩预告数据';

-- 获取港股通每日成交信息，数据从2014年开始
DROP TABLE IF EXISTS `ts_ggt_daily`;
CREATE TABLE `ts_ggt_daily` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `buy_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_amount',
  `buy_volume` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_volume',
  `sell_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell_amount',
  `sell_volume` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell_volume',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_trade_date` (`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取港股通每日成交信息，数据从2014年开始';

-- 获取港股通每日成交数据，其中包括沪市、深市详细数据，每天18~20点之间完成当日更新
DROP TABLE IF EXISTS `ts_ggt_top10`;
CREATE TABLE `ts_ggt_top10` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `p_change` DECIMAL(20,4) DEFAULT NULL COMMENT 'p_change',
  `rank` INT DEFAULT NULL COMMENT 'rank',
  `market_type` VARCHAR(64) DEFAULT NULL COMMENT 'market_type',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `net_amount` VARCHAR(64) DEFAULT NULL COMMENT 'net_amount',
  `sh_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'sh_amount',
  `sh_net_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'sh_net_amount',
  `sh_buy` DECIMAL(20,4) DEFAULT NULL COMMENT 'sh_buy',
  `sh_sell` DECIMAL(20,4) DEFAULT NULL COMMENT 'sh_sell',
  `sz_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'sz_amount',
  `sz_net_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'sz_net_amount',
  `sz_buy` DECIMAL(20,4) DEFAULT NULL COMMENT 'sz_buy',
  `sz_sell` DECIMAL(20,4) DEFAULT NULL COMMENT 'sz_sell',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取港股通每日成交数据，其中包括沪市、深市详细数据，每天18~20点之间完成当日更新';

-- 获取沪深港股通持股明细，数据来源港交所。
DROP TABLE IF EXISTS `ts_hk_hold`;
CREATE TABLE `ts_hk_hold` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `code` VARCHAR(64) NOT NULL COMMENT 'code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'ratio',
  `exchange` VARCHAR(64) DEFAULT NULL COMMENT 'exchange',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取沪深港股通持股明细，数据来源港交所。';

-- 获取每日游资交易明细，数据开始于2022年8。游资分类名录，请点击
DROP TABLE IF EXISTS `ts_hm_detail`;
CREATE TABLE `ts_hm_detail` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ts_name` DECIMAL(20,4) DEFAULT NULL COMMENT 'ts_name',
  `buy_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_amount',
  `sell_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell_amount',
  `net_amount` VARCHAR(64) DEFAULT NULL COMMENT 'net_amount',
  `hm_name` VARCHAR(64) DEFAULT NULL COMMENT 'hm_name',
  `hm_orgs` VARCHAR(64) DEFAULT NULL COMMENT 'hm_orgs',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取每日游资交易明细，数据开始于2022年8。游资分类名录，请点击';

-- 获取游资分类名录信息
DROP TABLE IF EXISTS `ts_hm_list`;
CREATE TABLE `ts_hm_list` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `desc` VARCHAR(64) DEFAULT NULL COMMENT 'desc',
  `orgs` DECIMAL(20,4) DEFAULT NULL COMMENT 'orgs',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取游资分类名录信息';

-- 获取沪股通、深股通每日前十大成交详细数据，每天18~20点之间完成当日更新
DROP TABLE IF EXISTS `ts_hsgt_top10`;
CREATE TABLE `ts_hsgt_top10` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `change` DECIMAL(20,4) DEFAULT NULL COMMENT 'change',
  `rank` INT DEFAULT NULL COMMENT 'rank',
  `market_type` VARCHAR(64) DEFAULT NULL COMMENT 'market_type',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `net_amount` VARCHAR(64) DEFAULT NULL COMMENT 'net_amount',
  `buy` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy',
  `sell` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取沪股通、深股通每日前十大成交详细数据，每天18~20点之间完成当日更新';

-- 获取上市公司财务利润表数据
DROP TABLE IF EXISTS `ts_income`;
CREATE TABLE `ts_income` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `f_ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'f_ann_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `report_type` VARCHAR(64) DEFAULT NULL COMMENT 'report_type',
  `comp_type` VARCHAR(64) DEFAULT NULL COMMENT 'comp_type',
  `end_type` VARCHAR(64) DEFAULT NULL COMMENT 'end_type',
  `basic_eps` DECIMAL(20,4) DEFAULT NULL COMMENT 'basic_eps',
  `diluted_eps` DECIMAL(20,4) DEFAULT NULL COMMENT 'diluted_eps',
  `total_revenue` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_revenue',
  `revenue` DECIMAL(20,4) DEFAULT NULL COMMENT 'revenue',
  `int_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'int_income',
  `prem_earned` DECIMAL(20,4) DEFAULT NULL COMMENT 'prem_earned',
  `comm_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'comm_income',
  `n_commis_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_commis_income',
  `n_oth_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_oth_income',
  `n_oth_b_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_oth_b_income',
  `prem_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'prem_income',
  `out_prem` DECIMAL(20,4) DEFAULT NULL COMMENT 'out_prem',
  `une_prem_reser` DECIMAL(20,4) DEFAULT NULL COMMENT 'une_prem_reser',
  `reins_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'reins_income',
  `n_sec_tb_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_sec_tb_income',
  `n_sec_uw_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_sec_uw_income',
  `n_asset_mg_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_asset_mg_income',
  `oth_b_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_b_income',
  `fv_value_chg_gain` DECIMAL(20,4) DEFAULT NULL COMMENT 'fv_value_chg_gain',
  `invest_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'invest_income',
  `ass_invest_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'ass_invest_income',
  `forex_gain` DECIMAL(20,4) DEFAULT NULL COMMENT 'forex_gain',
  `total_cogs` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_cogs',
  `oper_cost` DECIMAL(20,4) DEFAULT NULL COMMENT 'oper_cost',
  `int_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'int_exp',
  `comm_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'comm_exp',
  `biz_tax_surchg` DECIMAL(20,4) DEFAULT NULL COMMENT 'biz_tax_surchg',
  `sell_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell_exp',
  `admin_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'admin_exp',
  `fin_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'fin_exp',
  `assets_impair_loss` DECIMAL(20,4) DEFAULT NULL COMMENT 'assets_impair_loss',
  `prem_refund` DECIMAL(20,4) DEFAULT NULL COMMENT 'prem_refund',
  `compens_payout` DECIMAL(20,4) DEFAULT NULL COMMENT 'compens_payout',
  `reser_insur_liab` DECIMAL(20,4) DEFAULT NULL COMMENT 'reser_insur_liab',
  `div_payt` DECIMAL(20,4) DEFAULT NULL COMMENT 'div_payt',
  `reins_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'reins_exp',
  `oper_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'oper_exp',
  `compens_payout_refu` DECIMAL(20,4) DEFAULT NULL COMMENT 'compens_payout_refu',
  `insur_reser_refu` DECIMAL(20,4) DEFAULT NULL COMMENT 'insur_reser_refu',
  `reins_cost_refund` DECIMAL(20,4) DEFAULT NULL COMMENT 'reins_cost_refund',
  `other_bus_cost` DECIMAL(20,4) DEFAULT NULL COMMENT 'other_bus_cost',
  `operate_profit` DECIMAL(20,4) DEFAULT NULL COMMENT 'operate_profit',
  `non_oper_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'non_oper_income',
  `non_oper_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'non_oper_exp',
  `nca_disploss` DECIMAL(20,4) DEFAULT NULL COMMENT 'nca_disploss',
  `total_profit` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_profit',
  `income_tax` DECIMAL(20,4) DEFAULT NULL COMMENT 'income_tax',
  `n_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_income',
  `n_income_attr_p` DECIMAL(20,4) DEFAULT NULL COMMENT 'n_income_attr_p',
  `minority_gain` DECIMAL(20,4) DEFAULT NULL COMMENT 'minority_gain',
  `oth_compr_income` DECIMAL(20,4) DEFAULT NULL COMMENT 'oth_compr_income',
  `t_compr_income` DECIMAL(20,4) DEFAULT NULL COMMENT 't_compr_income',
  `compr_inc_attr_p` DECIMAL(20,4) DEFAULT NULL COMMENT 'compr_inc_attr_p',
  `compr_inc_attr_m_s` DECIMAL(20,4) DEFAULT NULL COMMENT 'compr_inc_attr_m_s',
  `ebit` DECIMAL(20,4) DEFAULT NULL COMMENT 'ebit',
  `ebitda` DECIMAL(20,4) DEFAULT NULL COMMENT 'ebitda',
  `insurance_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'insurance_exp',
  `undist_profit` DECIMAL(20,4) DEFAULT NULL COMMENT 'undist_profit',
  `distable_profit` DECIMAL(20,4) DEFAULT NULL COMMENT 'distable_profit',
  `rd_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'rd_exp',
  `fin_exp_int_exp` DECIMAL(20,4) DEFAULT NULL COMMENT 'fin_exp_int_exp',
  `fin_exp_int_inc` DECIMAL(20,4) DEFAULT NULL COMMENT 'fin_exp_int_inc',
  `transfer_surplus_rese` DECIMAL(20,4) DEFAULT NULL COMMENT 'transfer_surplus_rese',
  `transfer_housing_imprest` DECIMAL(20,4) DEFAULT NULL COMMENT 'transfer_housing_imprest',
  `transfer_oth` DECIMAL(20,4) DEFAULT NULL COMMENT 'transfer_oth',
  `adj_lossgain` DECIMAL(20,4) DEFAULT NULL COMMENT 'adj_lossgain',
  `withdra_legal_surplus` DECIMAL(20,4) DEFAULT NULL COMMENT 'withdra_legal_surplus',
  `withdra_legal_pubfund` DECIMAL(20,4) DEFAULT NULL COMMENT 'withdra_legal_pubfund',
  `withdra_biz_devfund` DECIMAL(20,4) DEFAULT NULL COMMENT 'withdra_biz_devfund',
  `withdra_rese_fund` DECIMAL(20,4) DEFAULT NULL COMMENT 'withdra_rese_fund',
  `withdra_oth_ersu` DECIMAL(20,4) DEFAULT NULL COMMENT 'withdra_oth_ersu',
  `workers_welfare` DECIMAL(20,4) DEFAULT NULL COMMENT 'workers_welfare',
  `distr_profit_shrhder` DECIMAL(20,4) DEFAULT NULL COMMENT 'distr_profit_shrhder',
  `prfshare_payable_dvd` DECIMAL(20,4) DEFAULT NULL COMMENT 'prfshare_payable_dvd',
  `comshare_payable_dvd` DECIMAL(20,4) DEFAULT NULL COMMENT 'comshare_payable_dvd',
  `capit_comstock_div` DECIMAL(20,4) DEFAULT NULL COMMENT 'capit_comstock_div',
  `continued_net_profit` DECIMAL(20,4) DEFAULT NULL COMMENT 'continued_net_profit',
  `update_flag` VARCHAR(64) DEFAULT NULL COMMENT 'update_flag',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司财务利润表数据';

-- 获取概念题材的成分股
DROP TABLE IF EXISTS `ts_kpl_concept_cons`;
CREATE TABLE `ts_kpl_concept_cons` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `con_name` VARCHAR(64) DEFAULT NULL COMMENT 'con_name',
  `con_code` VARCHAR(64) NOT NULL COMMENT 'con_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `desc` VARCHAR(64) DEFAULT NULL COMMENT 'desc',
  `hot_num` VARCHAR(64) DEFAULT NULL COMMENT 'hot_num',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取概念题材的成分股';

-- 获取涨停、跌停、炸板等榜单数据
DROP TABLE IF EXISTS `ts_kpl_list`;
CREATE TABLE `ts_kpl_list` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `lu_time` VARCHAR(64) DEFAULT NULL COMMENT 'lu_time',
  `ld_time` VARCHAR(64) DEFAULT NULL COMMENT 'ld_time',
  `open_time` VARCHAR(64) DEFAULT NULL COMMENT 'open_time',
  `last_time` VARCHAR(64) DEFAULT NULL COMMENT 'last_time',
  `lu_desc` VARCHAR(64) DEFAULT NULL COMMENT 'lu_desc',
  `tag` VARCHAR(64) DEFAULT NULL COMMENT 'tag',
  `theme` VARCHAR(64) DEFAULT NULL COMMENT 'theme',
  `net_change` VARCHAR(64) DEFAULT NULL COMMENT 'net_change',
  `bid_amount` VARCHAR(64) DEFAULT NULL COMMENT 'bid_amount',
  `status` VARCHAR(64) DEFAULT NULL COMMENT 'status',
  `bid_change` VARCHAR(64) DEFAULT NULL COMMENT 'bid_change',
  `bid_turnover` VARCHAR(64) DEFAULT NULL COMMENT 'bid_turnover',
  `lu_bid_vol` VARCHAR(64) DEFAULT NULL COMMENT 'lu_bid_vol',
  `pct_chg` VARCHAR(64) DEFAULT NULL COMMENT 'pct_chg',
  `bid_pct_chg` VARCHAR(64) DEFAULT NULL COMMENT 'bid_pct_chg',
  `rt_pct_chg` VARCHAR(64) DEFAULT NULL COMMENT 'rt_pct_chg',
  `limit_order` DECIMAL(20,4) DEFAULT NULL COMMENT 'limit_order',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `turnover_rate` VARCHAR(64) DEFAULT NULL COMMENT 'turnover_rate',
  `free_float` VARCHAR(64) DEFAULT NULL COMMENT 'free_float',
  `lu_limit_order` VARCHAR(64) DEFAULT NULL COMMENT 'lu_limit_order',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取涨停、跌停、炸板等榜单数据';

-- 获取每天涨停股票最多最强的概念板块，可以分析强势板块的轮动，判断资金动向
DROP TABLE IF EXISTS `ts_limit_cpt_list`;
CREATE TABLE `ts_limit_cpt_list` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `days` INT DEFAULT NULL COMMENT 'days',
  `up_stat` VARCHAR(64) DEFAULT NULL COMMENT 'up_stat',
  `cons_nums` INT DEFAULT NULL COMMENT 'cons_nums',
  `up_nums` INT DEFAULT NULL COMMENT 'up_nums',
  `pct_chg` VARCHAR(64) DEFAULT NULL COMMENT 'pct_chg',
  `rank` INT DEFAULT NULL COMMENT 'rank',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取每天涨停股票最多最强的概念板块，可以分析强势板块的轮动，判断资金动向';

-- 获取A股每日涨跌停、炸板数据情况，数据从2020年开始（不提供ST股票的统计）
DROP TABLE IF EXISTS `ts_limit_list_d`;
CREATE TABLE `ts_limit_list_d` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `industry` VARCHAR(64) DEFAULT NULL COMMENT 'industry',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `pct_chg` VARCHAR(64) DEFAULT NULL COMMENT 'pct_chg',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `limit_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'limit_amount',
  `float_mv` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_mv',
  `total_mv` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_mv',
  `turnover_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'turnover_ratio',
  `fd_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'fd_amount',
  `first_time` VARCHAR(64) DEFAULT NULL COMMENT 'first_time',
  `last_time` VARCHAR(64) DEFAULT NULL COMMENT 'last_time',
  `open_times` INT DEFAULT NULL COMMENT 'open_times',
  `up_stat` VARCHAR(64) DEFAULT NULL COMMENT 'up_stat',
  `limit_times` INT DEFAULT NULL COMMENT 'limit_times',
  `limit` DECIMAL(20,4) DEFAULT NULL COMMENT 'limit',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取A股每日涨跌停、炸板数据情况，数据从2020年开始（不提供ST股票的统计）';

-- 获取同花顺每日涨跌停榜单数据，历史数据从20231101开始提供，增量每天16点左右更新
DROP TABLE IF EXISTS `ts_limit_list_ths`;
CREATE TABLE `ts_limit_list_ths` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `price` DECIMAL(20,4) DEFAULT NULL COMMENT 'price',
  `pct_chg` VARCHAR(64) DEFAULT NULL COMMENT 'pct_chg',
  `open_num` DECIMAL(20,4) DEFAULT NULL COMMENT 'open_num',
  `lu_desc` VARCHAR(64) DEFAULT NULL COMMENT 'lu_desc',
  `limit_type` DECIMAL(20,4) DEFAULT NULL COMMENT 'limit_type',
  `tag` VARCHAR(64) DEFAULT NULL COMMENT 'tag',
  `status` VARCHAR(64) DEFAULT NULL COMMENT 'status',
  `limit_order` DECIMAL(20,4) DEFAULT NULL COMMENT 'limit_order',
  `limit_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'limit_amount',
  `turnover_rate` VARCHAR(64) DEFAULT NULL COMMENT 'turnover_rate',
  `free_float` VARCHAR(64) DEFAULT NULL COMMENT 'free_float',
  `lu_limit_order` VARCHAR(64) DEFAULT NULL COMMENT 'lu_limit_order',
  `limit_up_suc_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'limit_up_suc_rate',
  `turnover` DECIMAL(20,4) DEFAULT NULL COMMENT 'turnover',
  `market_type` VARCHAR(64) DEFAULT NULL COMMENT 'market_type',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取同花顺每日涨跌停榜单数据，历史数据从20231101开始提供，增量每天16点左右更新';

-- 获取每天连板个数晋级的股票
DROP TABLE IF EXISTS `ts_limit_step`;
CREATE TABLE `ts_limit_step` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `nums` VARCHAR(64) DEFAULT NULL COMMENT 'nums',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取每天连板个数晋级的股票';

-- 获取融资融券每日交易汇总数据，交易所于每天8点30左右更新上一日数据
DROP TABLE IF EXISTS `ts_margin`;
CREATE TABLE `ts_margin` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `exchange_id` VARCHAR(64) DEFAULT NULL COMMENT 'exchange_id',
  `rzye` DECIMAL(20,4) DEFAULT NULL COMMENT 'rzye',
  `rzmre` DECIMAL(20,4) DEFAULT NULL COMMENT 'rzmre',
  `rzche` DECIMAL(20,4) DEFAULT NULL COMMENT 'rzche',
  `rqye` DECIMAL(20,4) DEFAULT NULL COMMENT 'rqye',
  `rqmcl` DECIMAL(20,4) DEFAULT NULL COMMENT 'rqmcl',
  `rzrqye` DECIMAL(20,4) DEFAULT NULL COMMENT 'rzrqye',
  `rqyl` DECIMAL(20,4) DEFAULT NULL COMMENT 'rqyl',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_trade_date` (`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取融资融券每日交易汇总数据，交易所于每天8点30左右更新上一日数据';

-- 获取沪深两市每日融资融券明细，，交易所于每天8点30左右更新上一日数据
DROP TABLE IF EXISTS `ts_margin_detail`;
CREATE TABLE `ts_margin_detail` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `rzye` DECIMAL(20,4) DEFAULT NULL COMMENT 'rzye',
  `rqye` DECIMAL(20,4) DEFAULT NULL COMMENT 'rqye',
  `rzmre` DECIMAL(20,4) DEFAULT NULL COMMENT 'rzmre',
  `rqyl` DECIMAL(20,4) DEFAULT NULL COMMENT 'rqyl',
  `rzche` DECIMAL(20,4) DEFAULT NULL COMMENT 'rzche',
  `rqchl` DECIMAL(20,4) DEFAULT NULL COMMENT 'rqchl',
  `rqmcl` DECIMAL(20,4) DEFAULT NULL COMMENT 'rqmcl',
  `rzrqye` DECIMAL(20,4) DEFAULT NULL COMMENT 'rzrqye',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取沪深两市每日融资融券明细，，交易所于每天8点30左右更新上一日数据';

-- 获取沪深京三大交易所融资融券标的（包括ETF），每天盘前更新
DROP TABLE IF EXISTS `ts_margin_secs`;
CREATE TABLE `ts_margin_secs` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `exchange` VARCHAR(64) DEFAULT NULL COMMENT 'exchange',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取沪深京三大交易所融资融券标的（包括ETF），每天盘前更新';

-- 获取沪深A股票资金流向数据，分析大单小单成交情况，用于判别资金动向，数据开始于2010年。
DROP TABLE IF EXISTS `ts_moneyflow`;
CREATE TABLE `ts_moneyflow` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `buy_sm_vol` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_sm_vol',
  `buy_sm_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_sm_amount',
  `sell_sm_vol` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell_sm_vol',
  `sell_sm_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell_sm_amount',
  `buy_md_vol` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_md_vol',
  `buy_md_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_md_amount',
  `sell_md_vol` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell_md_vol',
  `sell_md_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell_md_amount',
  `buy_lg_vol` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_lg_vol',
  `buy_lg_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_lg_amount',
  `sell_lg_vol` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell_lg_vol',
  `sell_lg_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell_lg_amount',
  `buy_elg_vol` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_elg_vol',
  `buy_elg_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_elg_amount',
  `sell_elg_vol` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell_elg_vol',
  `sell_elg_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell_elg_amount',
  `net_mf_vol` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_mf_vol',
  `net_mf_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_mf_amount',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取沪深A股票资金流向数据，分析大单小单成交情况，用于判别资金动向，数据开始于2010年。';

-- 获取同花顺概念板块每日资金流向
DROP TABLE IF EXISTS `ts_moneyflow_cnt_ths`;
CREATE TABLE `ts_moneyflow_cnt_ths` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `lead_stock` VARCHAR(64) DEFAULT NULL COMMENT 'lead_stock',
  `close_price` DECIMAL(20,4) DEFAULT NULL COMMENT 'close_price',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `industry_index` DECIMAL(20,4) DEFAULT NULL COMMENT 'industry_index',
  `company_num` INT DEFAULT NULL COMMENT 'company_num',
  `pct_change_stock` DECIMAL(20,4) DEFAULT NULL COMMENT 'pct_change_stock',
  `net_buy_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_buy_amount',
  `net_sell_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_sell_amount',
  `net_amount` VARCHAR(64) DEFAULT NULL COMMENT 'net_amount',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取同花顺概念板块每日资金流向';

-- 获取东方财富个股资金流向数据，每日盘后更新，数据开始于20230911
DROP TABLE IF EXISTS `ts_moneyflow_dc`;
CREATE TABLE `ts_moneyflow_dc` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `net_amount` VARCHAR(64) DEFAULT NULL COMMENT 'net_amount',
  `net_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_amount_rate',
  `buy_elg_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_elg_amount',
  `buy_elg_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_elg_amount_rate',
  `buy_lg_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_lg_amount',
  `buy_lg_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_lg_amount_rate',
  `buy_md_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_md_amount',
  `buy_md_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_md_amount_rate',
  `buy_sm_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_sm_amount',
  `buy_sm_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_sm_amount_rate',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取东方财富个股资金流向数据，每日盘后更新，数据开始于20230911';

-- 获取沪股通、深股通、港股通每日资金流向数据，每次最多返回300条记录，总量不限制。
DROP TABLE IF EXISTS `ts_moneyflow_hsgt`;
CREATE TABLE `ts_moneyflow_hsgt` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ggt_ss` DECIMAL(20,4) DEFAULT NULL COMMENT 'ggt_ss',
  `ggt_sz` DECIMAL(20,4) DEFAULT NULL COMMENT 'ggt_sz',
  `hgt` DECIMAL(20,4) DEFAULT NULL COMMENT 'hgt',
  `sgt` DECIMAL(20,4) DEFAULT NULL COMMENT 'sgt',
  `north_money` DECIMAL(20,4) DEFAULT NULL COMMENT 'north_money',
  `south_money` DECIMAL(20,4) DEFAULT NULL COMMENT 'south_money',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_trade_date` (`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取沪股通、深股通、港股通每日资金流向数据，每次最多返回300条记录，总量不限制。';

-- 获取东方财富板块资金流向，每天盘后更新
DROP TABLE IF EXISTS `ts_moneyflow_ind_dc`;
CREATE TABLE `ts_moneyflow_ind_dc` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `content_type` VARCHAR(64) DEFAULT NULL COMMENT 'content_type',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `net_amount` VARCHAR(64) DEFAULT NULL COMMENT 'net_amount',
  `net_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_amount_rate',
  `buy_elg_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_elg_amount',
  `buy_elg_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_elg_amount_rate',
  `buy_lg_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_lg_amount',
  `buy_lg_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_lg_amount_rate',
  `buy_md_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_md_amount',
  `buy_md_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_md_amount_rate',
  `buy_sm_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_sm_amount',
  `buy_sm_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_sm_amount_rate',
  `buy_sm_amount_stock` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_sm_amount_stock',
  `rank` INT DEFAULT NULL COMMENT 'rank',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取东方财富板块资金流向，每天盘后更新';

-- 获取同花顺行业资金流向，每日盘后更新
DROP TABLE IF EXISTS `ts_moneyflow_ind_ths`;
CREATE TABLE `ts_moneyflow_ind_ths` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `industry` VARCHAR(64) DEFAULT NULL COMMENT 'industry',
  `lead_stock` VARCHAR(64) DEFAULT NULL COMMENT 'lead_stock',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `company_num` INT DEFAULT NULL COMMENT 'company_num',
  `pct_change_stock` DECIMAL(20,4) DEFAULT NULL COMMENT 'pct_change_stock',
  `close_price` DECIMAL(20,4) DEFAULT NULL COMMENT 'close_price',
  `net_buy_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_buy_amount',
  `net_sell_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_sell_amount',
  `net_amount` VARCHAR(64) DEFAULT NULL COMMENT 'net_amount',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取同花顺行业资金流向，每日盘后更新';

-- 获取东方财富大盘资金流向数据，每日盘后更新
DROP TABLE IF EXISTS `ts_moneyflow_mkt_dc`;
CREATE TABLE `ts_moneyflow_mkt_dc` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `close_sh` DECIMAL(20,4) DEFAULT NULL COMMENT 'close_sh',
  `pct_change_sh` DECIMAL(20,4) DEFAULT NULL COMMENT 'pct_change_sh',
  `close_sz` DECIMAL(20,4) DEFAULT NULL COMMENT 'close_sz',
  `pct_change_sz` DECIMAL(20,4) DEFAULT NULL COMMENT 'pct_change_sz',
  `net_amount` VARCHAR(64) DEFAULT NULL COMMENT 'net_amount',
  `net_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_amount_rate',
  `buy_elg_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_elg_amount',
  `buy_elg_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_elg_amount_rate',
  `buy_lg_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_lg_amount',
  `buy_lg_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_lg_amount_rate',
  `buy_md_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_md_amount',
  `buy_md_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_md_amount_rate',
  `buy_sm_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_sm_amount',
  `buy_sm_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_sm_amount_rate',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_trade_date` (`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取东方财富大盘资金流向数据，每日盘后更新';

-- 获取同花顺个股资金流向数据，每日盘后更新
DROP TABLE IF EXISTS `ts_moneyflow_ths`;
CREATE TABLE `ts_moneyflow_ths` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `latest` DECIMAL(20,4) DEFAULT NULL COMMENT 'latest',
  `net_amount` VARCHAR(64) DEFAULT NULL COMMENT 'net_amount',
  `net_d5_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_d5_amount',
  `buy_lg_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_lg_amount',
  `buy_lg_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_lg_amount_rate',
  `buy_md_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_md_amount',
  `buy_md_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_md_amount_rate',
  `buy_sm_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_sm_amount',
  `buy_sm_amount_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_sm_amount_rate',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取同花顺个股资金流向数据，每日盘后更新';

-- 获取A股月线数据
DROP TABLE IF EXISTS `ts_monthly`;
CREATE TABLE `ts_monthly` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `pre_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close',
  `change` DECIMAL(20,4) DEFAULT NULL COMMENT 'change',
  `pct_chg` VARCHAR(64) DEFAULT NULL COMMENT 'pct_chg',
  `Y` DECIMAL(20,4) DEFAULT NULL COMMENT 'Y',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取A股月线数据';

-- 历史名称变更记录
DROP TABLE IF EXISTS `ts_namechange`;
CREATE TABLE `ts_namechange` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `start_date` VARCHAR(64) DEFAULT NULL COMMENT 'start_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `change_reason` VARCHAR(64) DEFAULT NULL COMMENT 'change_reason',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='历史名称变更记录';

-- 获取新股上市列表数据
DROP TABLE IF EXISTS `ts_new_share`;
CREATE TABLE `ts_new_share` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `sub_code` VARCHAR(64) DEFAULT NULL COMMENT 'sub_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `ipo_date` VARCHAR(64) DEFAULT NULL COMMENT 'ipo_date',
  `issue_date` VARCHAR(64) DEFAULT NULL COMMENT 'issue_date',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `market_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'market_amount',
  `price` DECIMAL(20,4) DEFAULT NULL COMMENT 'price',
  `pe` DECIMAL(20,4) DEFAULT NULL COMMENT 'pe',
  `limit_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'limit_amount',
  `funds` DECIMAL(20,4) DEFAULT NULL COMMENT 'funds',
  `ballot` DECIMAL(20,4) DEFAULT NULL COMMENT 'ballot',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取新股上市列表数据';

-- 获取股票质押明细数据
DROP TABLE IF EXISTS `ts_pledge_detail`;
CREATE TABLE `ts_pledge_detail` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `holder_name` VARCHAR(64) DEFAULT NULL COMMENT 'holder_name',
  `pledge_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'pledge_amount',
  `start_date` VARCHAR(64) DEFAULT NULL COMMENT 'start_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `is_release` VARCHAR(64) DEFAULT NULL COMMENT 'is_release',
  `release_date` VARCHAR(64) DEFAULT NULL COMMENT 'release_date',
  `pledgor` VARCHAR(64) DEFAULT NULL COMMENT 'pledgor',
  `holding_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'holding_amount',
  `pledged_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'pledged_amount',
  `p_total_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'p_total_ratio',
  `h_total_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'h_total_ratio',
  `is_buyback` VARCHAR(64) DEFAULT NULL COMMENT 'is_buyback',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取股票质押明细数据';

-- 获取股票质押统计数据
DROP TABLE IF EXISTS `ts_pledge_stat`;
CREATE TABLE `ts_pledge_stat` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `pledge_count` INT DEFAULT NULL COMMENT 'pledge_count',
  `unrest_pledge` DECIMAL(20,4) DEFAULT NULL COMMENT 'unrest_pledge',
  `rest_pledge` DECIMAL(20,4) DEFAULT NULL COMMENT 'rest_pledge',
  `total_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_share',
  `pledge_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'pledge_ratio',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取股票质押统计数据';

-- 获取券商（卖方）每天研报的盈利预测数据，数据从2010年开始，每晚19~22点更新当日数据
DROP TABLE IF EXISTS `ts_report_rc`;
CREATE TABLE `ts_report_rc` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `report_date` VARCHAR(64) DEFAULT NULL COMMENT 'report_date',
  `report_title` DECIMAL(20,4) DEFAULT NULL COMMENT 'report_title',
  `report_type` VARCHAR(64) DEFAULT NULL COMMENT 'report_type',
  `classify` VARCHAR(64) DEFAULT NULL COMMENT 'classify',
  `org_name` VARCHAR(64) DEFAULT NULL COMMENT 'org_name',
  `author_name` VARCHAR(64) DEFAULT NULL COMMENT 'author_name',
  `quarter` VARCHAR(64) DEFAULT NULL COMMENT 'quarter',
  `op_rt` DECIMAL(20,4) DEFAULT NULL COMMENT 'op_rt',
  `op_pr` DECIMAL(20,4) DEFAULT NULL COMMENT 'op_pr',
  `tp` DECIMAL(20,4) DEFAULT NULL COMMENT 'tp',
  `np` DECIMAL(20,4) DEFAULT NULL COMMENT 'np',
  `eps` DECIMAL(20,4) DEFAULT NULL COMMENT 'eps',
  `pe` DECIMAL(20,4) DEFAULT NULL COMMENT 'pe',
  `rd` DECIMAL(20,4) DEFAULT NULL COMMENT 'rd',
  `roe` DECIMAL(20,4) DEFAULT NULL COMMENT 'roe',
  `ev_ebitda` DECIMAL(20,4) DEFAULT NULL COMMENT 'ev_ebitda',
  `rating` VARCHAR(64) DEFAULT NULL COMMENT 'rating',
  `max_price` DECIMAL(20,4) DEFAULT NULL COMMENT 'max_price',
  `min_price` DECIMAL(20,4) DEFAULT NULL COMMENT 'min_price',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取券商（卖方）每天研报的盈利预测数据，数据从2010年开始，每晚19~22点更新当日数据';

-- 获取上市公司回购股票数据
DROP TABLE IF EXISTS `ts_repurchase`;
CREATE TABLE `ts_repurchase` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `proc` DECIMAL(20,4) DEFAULT NULL COMMENT 'proc',
  `exp_date` DECIMAL(20,4) DEFAULT NULL COMMENT 'exp_date',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `high_limit` DECIMAL(20,4) DEFAULT NULL COMMENT 'high_limit',
  `low_limit` DECIMAL(20,4) DEFAULT NULL COMMENT 'low_limit',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司回购股票数据';

-- 获取实时日k线行情，支持按股票代码及股票代码通配符一次性提取全部股票实时日k线行情
DROP TABLE IF EXISTS `ts_rt_k`;
CREATE TABLE `ts_rt_k` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `pre_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `num` INT DEFAULT NULL COMMENT 'num',
  `ask_price1` DECIMAL(20,4) DEFAULT NULL COMMENT 'ask_price1',
  `ask_volume1` DECIMAL(20,4) DEFAULT NULL COMMENT 'ask_volume1',
  `bid_price1` DECIMAL(20,4) DEFAULT NULL COMMENT 'bid_price1',
  `bid_volume1` DECIMAL(20,4) DEFAULT NULL COMMENT 'bid_volume1',
  `trade_time` DECIMAL(20,4) DEFAULT NULL COMMENT 'trade_time',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取实时日k线行情，支持按股票代码及股票代码通配符一次性提取全部股票实时日k线行情';

-- 获取全A股票实时分钟数据，包括1~60min
DROP TABLE IF EXISTS `ts_rt_min`;
CREATE TABLE `ts_rt_min` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `code` VARCHAR(64) NOT NULL COMMENT 'code',
  `time` VARCHAR(64) DEFAULT NULL COMMENT 'time',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取全A股票实时分钟数据，包括1~60min';

-- 获取A股当日盘中历史分钟数据，可以提取单只股票当日开盘以来的所有分钟数据
DROP TABLE IF EXISTS `ts_rt_min_daily`;
CREATE TABLE `ts_rt_min_daily` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `freq` VARCHAR(64) DEFAULT NULL COMMENT 'freq',
  `time` VARCHAR(64) DEFAULT NULL COMMENT 'time',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取A股当日盘中历史分钟数据，可以提取单只股票当日开盘以来的所有分钟数据';

-- 获取限售股解禁
DROP TABLE IF EXISTS `ts_share_float`;
CREATE TABLE `ts_share_float` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `float_date` VARCHAR(64) DEFAULT NULL COMMENT 'float_date',
  `float_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_share',
  `float_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_ratio',
  `holder_name` VARCHAR(64) DEFAULT NULL COMMENT 'holder_name',
  `share_type` VARCHAR(64) DEFAULT NULL COMMENT 'share_type',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取限售股解禁';

-- 转融通融资汇总
DROP TABLE IF EXISTS `ts_slb_len`;
CREATE TABLE `ts_slb_len` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ob` DECIMAL(20,4) DEFAULT NULL COMMENT 'ob',
  `auc_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'auc_amount',
  `repo_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'repo_amount',
  `repay_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'repay_amount',
  `cb` DECIMAL(20,4) DEFAULT NULL COMMENT 'cb',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_trade_date` (`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='转融通融资汇总';

-- ST风险警示板股票列表
DROP TABLE IF EXISTS `ts_st`;
CREATE TABLE `ts_st` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `pub_date` VARCHAR(64) DEFAULT NULL COMMENT 'pub_date',
  `imp_date` VARCHAR(64) DEFAULT NULL COMMENT 'imp_date',
  `st_tpye` VARCHAR(64) DEFAULT NULL COMMENT 'st_tpye',
  `st_reason` VARCHAR(64) DEFAULT NULL COMMENT 'st_reason',
  `st_explain` VARCHAR(64) DEFAULT NULL COMMENT 'st_explain',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ST风险警示板股票列表';

-- 获取股票账户开户数据，统计周期为一周
DROP TABLE IF EXISTS `ts_stk_account`;
CREATE TABLE `ts_stk_account` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `date` DECIMAL(20,4) DEFAULT NULL COMMENT 'date',
  `weekly_new` DECIMAL(20,4) DEFAULT NULL COMMENT 'weekly_new',
  `total` DECIMAL(20,4) DEFAULT NULL COMMENT 'total',
  `weekly_hold` DECIMAL(20,4) DEFAULT NULL COMMENT 'weekly_hold',
  `weekly_trade` DECIMAL(20,4) DEFAULT NULL COMMENT 'weekly_trade',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取股票账户开户数据，统计周期为一周';

-- 获取股票账户开户数据旧版格式数据，数据从2008年1月开始，到2015年5月29，新数据请通过
DROP TABLE IF EXISTS `ts_stk_account_old`;
CREATE TABLE `ts_stk_account_old` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `date` DECIMAL(20,4) DEFAULT NULL COMMENT 'date',
  `new_sh` DECIMAL(20,4) DEFAULT NULL COMMENT 'new_sh',
  `new_sz` DECIMAL(20,4) DEFAULT NULL COMMENT 'new_sz',
  `active_sh` DECIMAL(20,4) DEFAULT NULL COMMENT 'active_sh',
  `active_sz` DECIMAL(20,4) DEFAULT NULL COMMENT 'active_sz',
  `total_sh` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_sh',
  `total_sz` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_sz',
  `trade_sh` DECIMAL(20,4) DEFAULT NULL COMMENT 'trade_sh',
  `trade_sz` DECIMAL(20,4) DEFAULT NULL COMMENT 'trade_sz',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取股票账户开户数据旧版格式数据，数据从2008年1月开始，到2015年5月29，新数据请通过';

-- AH股比价数据，可根据交易日期获取历史
DROP TABLE IF EXISTS `ts_stk_ah_comparison`;
CREATE TABLE `ts_stk_ah_comparison` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `hk_code` VARCHAR(64) DEFAULT NULL COMMENT 'hk_code',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `hk_name` DECIMAL(20,4) DEFAULT NULL COMMENT 'hk_name',
  `hk_pct_chg` DECIMAL(20,4) DEFAULT NULL COMMENT 'hk_pct_chg',
  `hk_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'hk_close',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `pct_chg` VARCHAR(64) DEFAULT NULL COMMENT 'pct_chg',
  `ah_comparison` DECIMAL(20,4) DEFAULT NULL COMMENT 'ah_comparison',
  `ah_premium` DECIMAL(20,4) DEFAULT NULL COMMENT 'ah_premium',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AH股比价数据，可根据交易日期获取历史';

-- 根据证券交易所交易规则的有关规定，交易所每日发布重点提示证券
DROP TABLE IF EXISTS `ts_stk_alert`;
CREATE TABLE `ts_stk_alert` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `start_date` VARCHAR(64) DEFAULT NULL COMMENT 'start_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `type` VARCHAR(64) DEFAULT NULL COMMENT 'type',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='根据证券交易所交易规则的有关规定，交易所每日发布重点提示证券';

-- 获取当日个股和ETF的集合竞价成交情况，每天9点26~29分之间可以获取当日的集合竞价成交数据
DROP TABLE IF EXISTS `ts_stk_auction`;
CREATE TABLE `ts_stk_auction` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `price` DECIMAL(20,4) DEFAULT NULL COMMENT 'price',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `pre_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close',
  `turnover_rate` VARCHAR(64) DEFAULT NULL COMMENT 'turnover_rate',
  `volume_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'volume_ratio',
  `float_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_share',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取当日个股和ETF的集合竞价成交情况，每天9点26~29分之间可以获取当日的集合竞价成交数据';

-- 股票收盘15:00集合竞价数据，每天盘后更新
DROP TABLE IF EXISTS `ts_stk_auction_c`;
CREATE TABLE `ts_stk_auction_c` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `vwap` DECIMAL(20,4) DEFAULT NULL COMMENT 'vwap',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票收盘15:00集合竞价数据，每天盘后更新';

-- 股票开盘9:30集合竞价数据，每天盘后更新
DROP TABLE IF EXISTS `ts_stk_auction_o`;
CREATE TABLE `ts_stk_auction_o` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `vwap` DECIMAL(20,4) DEFAULT NULL COMMENT 'vwap',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票开盘9:30集合竞价数据，每天盘后更新';

-- 获取股票每日技术面因子数据，用于跟踪股票当前走势情况，数据由Tushare社区自产，覆盖全历史
DROP TABLE IF EXISTS `ts_stk_factor`;
CREATE TABLE `ts_stk_factor` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `pre_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close',
  `change` DECIMAL(20,4) DEFAULT NULL COMMENT 'change',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `adj_factor` DECIMAL(20,4) DEFAULT NULL COMMENT 'adj_factor',
  `open_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'open_hfq',
  `open_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'open_qfq',
  `close_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'close_hfq',
  `close_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'close_qfq',
  `high_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'high_hfq',
  `high_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'high_qfq',
  `low_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'low_hfq',
  `low_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'low_qfq',
  `pre_close_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close_hfq',
  `pre_close_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close_qfq',
  `macd_dif` DECIMAL(20,4) DEFAULT NULL COMMENT 'macd_dif',
  `macd_dea` DECIMAL(20,4) DEFAULT NULL COMMENT 'macd_dea',
  `macd` DECIMAL(20,4) DEFAULT NULL COMMENT 'macd',
  `kdj_k` DECIMAL(20,4) DEFAULT NULL COMMENT 'kdj_k',
  `kdj_d` DECIMAL(20,4) DEFAULT NULL COMMENT 'kdj_d',
  `kdj_j` DECIMAL(20,4) DEFAULT NULL COMMENT 'kdj_j',
  `rsi_6` DECIMAL(20,4) DEFAULT NULL COMMENT 'rsi_6',
  `rsi_12` DECIMAL(20,4) DEFAULT NULL COMMENT 'rsi_12',
  `rsi_24` DECIMAL(20,4) DEFAULT NULL COMMENT 'rsi_24',
  `boll_upper` DECIMAL(20,4) DEFAULT NULL COMMENT 'boll_upper',
  `boll_mid` DECIMAL(20,4) DEFAULT NULL COMMENT 'boll_mid',
  `boll_lower` DECIMAL(20,4) DEFAULT NULL COMMENT 'boll_lower',
  `cci` DECIMAL(20,4) DEFAULT NULL COMMENT 'cci',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取股票每日技术面因子数据，用于跟踪股票当前走势情况，数据由Tushare社区自产，覆盖全历史';

-- 获取股票每日技术面因子数据，用于跟踪股票当前走势情况，数据由Tushare社区自产，覆盖全历史；输出参数_bfq表示不复权，_qfq表示前复权 _hfq表示后复
DROP TABLE IF EXISTS `ts_stk_factor_pro`;
CREATE TABLE `ts_stk_factor_pro` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `open_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'open_hfq',
  `open_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'open_qfq',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `high_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'high_hfq',
  `high_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'high_qfq',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `low_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'low_hfq',
  `low_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'low_qfq',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `close_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'close_hfq',
  `close_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'close_qfq',
  `pre_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close',
  `change` DECIMAL(20,4) DEFAULT NULL COMMENT 'change',
  `pct_chg` VARCHAR(64) DEFAULT NULL COMMENT 'pct_chg',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `turnover_rate` VARCHAR(64) DEFAULT NULL COMMENT 'turnover_rate',
  `turnover_rate_f` DECIMAL(20,4) DEFAULT NULL COMMENT 'turnover_rate_f',
  `volume_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'volume_ratio',
  `pe` DECIMAL(20,4) DEFAULT NULL COMMENT 'pe',
  `pe_ttm` DECIMAL(20,4) DEFAULT NULL COMMENT 'pe_ttm',
  `pb` DECIMAL(20,4) DEFAULT NULL COMMENT 'pb',
  `ps` DECIMAL(20,4) DEFAULT NULL COMMENT 'ps',
  `ps_ttm` DECIMAL(20,4) DEFAULT NULL COMMENT 'ps_ttm',
  `dv_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'dv_ratio',
  `dv_ttm` DECIMAL(20,4) DEFAULT NULL COMMENT 'dv_ttm',
  `total_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_share',
  `float_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_share',
  `free_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'free_share',
  `total_mv` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_mv',
  `circ_mv` DECIMAL(20,4) DEFAULT NULL COMMENT 'circ_mv',
  `adj_factor` DECIMAL(20,4) DEFAULT NULL COMMENT 'adj_factor',
  `asi_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'asi_bfq',
  `asi_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'asi_hfq',
  `asi_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'asi_qfq',
  `asit_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'asit_bfq',
  `asit_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'asit_hfq',
  `asit_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'asit_qfq',
  `atr_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'atr_bfq',
  `atr_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'atr_hfq',
  `atr_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'atr_qfq',
  `bbi_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'bbi_bfq',
  `bbi_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'bbi_hfq',
  `bbi_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'bbi_qfq',
  `bias1_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'bias1_bfq',
  `bias1_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'bias1_hfq',
  `bias1_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'bias1_qfq',
  `bias2_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'bias2_bfq',
  `bias2_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'bias2_hfq',
  `bias2_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'bias2_qfq',
  `bias3_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'bias3_bfq',
  `bias3_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'bias3_hfq',
  `bias3_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'bias3_qfq',
  `boll_lower_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'boll_lower_bfq',
  `boll_lower_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'boll_lower_hfq',
  `boll_lower_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'boll_lower_qfq',
  `boll_mid_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'boll_mid_bfq',
  `boll_mid_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'boll_mid_hfq',
  `boll_mid_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'boll_mid_qfq',
  `boll_upper_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'boll_upper_bfq',
  `boll_upper_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'boll_upper_hfq',
  `boll_upper_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'boll_upper_qfq',
  `brar_ar_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'brar_ar_bfq',
  `brar_ar_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'brar_ar_hfq',
  `brar_ar_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'brar_ar_qfq',
  `brar_br_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'brar_br_bfq',
  `brar_br_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'brar_br_hfq',
  `brar_br_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'brar_br_qfq',
  `cci_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'cci_bfq',
  `cci_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'cci_hfq',
  `cci_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'cci_qfq',
  `cr_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'cr_bfq',
  `cr_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'cr_hfq',
  `cr_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'cr_qfq',
  `dfma_dif_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dfma_dif_bfq',
  `dfma_dif_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dfma_dif_hfq',
  `dfma_dif_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dfma_dif_qfq',
  `dfma_difma_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dfma_difma_bfq',
  `dfma_difma_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dfma_difma_hfq',
  `dfma_difma_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dfma_difma_qfq',
  `dmi_adx_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dmi_adx_bfq',
  `dmi_adx_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dmi_adx_hfq',
  `dmi_adx_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dmi_adx_qfq',
  `dmi_adxr_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dmi_adxr_bfq',
  `dmi_adxr_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dmi_adxr_hfq',
  `dmi_adxr_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dmi_adxr_qfq',
  `dmi_mdi_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dmi_mdi_bfq',
  `dmi_mdi_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dmi_mdi_hfq',
  `dmi_mdi_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dmi_mdi_qfq',
  `dmi_pdi_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dmi_pdi_bfq',
  `dmi_pdi_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dmi_pdi_hfq',
  `dmi_pdi_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dmi_pdi_qfq',
  `downdays` DECIMAL(20,4) DEFAULT NULL COMMENT 'downdays',
  `updays` DECIMAL(20,4) DEFAULT NULL COMMENT 'updays',
  `dpo_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dpo_bfq',
  `dpo_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dpo_hfq',
  `dpo_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'dpo_qfq',
  `madpo_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'madpo_bfq',
  `madpo_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'madpo_hfq',
  `madpo_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'madpo_qfq',
  `ema_bfq_10` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_bfq_10',
  `ema_bfq_20` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_bfq_20',
  `ema_bfq_250` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_bfq_250',
  `ema_bfq_30` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_bfq_30',
  `ema_bfq_5` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_bfq_5',
  `ema_bfq_60` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_bfq_60',
  `ema_bfq_90` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_bfq_90',
  `ema_hfq_10` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_hfq_10',
  `ema_hfq_20` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_hfq_20',
  `ema_hfq_250` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_hfq_250',
  `ema_hfq_30` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_hfq_30',
  `ema_hfq_5` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_hfq_5',
  `ema_hfq_60` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_hfq_60',
  `ema_hfq_90` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_hfq_90',
  `ema_qfq_10` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_qfq_10',
  `ema_qfq_20` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_qfq_20',
  `ema_qfq_250` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_qfq_250',
  `ema_qfq_30` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_qfq_30',
  `ema_qfq_5` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_qfq_5',
  `ema_qfq_60` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_qfq_60',
  `ema_qfq_90` DECIMAL(20,4) DEFAULT NULL COMMENT 'ema_qfq_90',
  `emv_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'emv_bfq',
  `emv_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'emv_hfq',
  `emv_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'emv_qfq',
  `maemv_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'maemv_bfq',
  `maemv_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'maemv_hfq',
  `maemv_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'maemv_qfq',
  `expma_12_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'expma_12_bfq',
  `expma_12_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'expma_12_hfq',
  `expma_12_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'expma_12_qfq',
  `expma_50_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'expma_50_bfq',
  `expma_50_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'expma_50_hfq',
  `expma_50_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'expma_50_qfq',
  `kdj_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'kdj_bfq',
  `kdj_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'kdj_hfq',
  `kdj_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'kdj_qfq',
  `kdj_d_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'kdj_d_bfq',
  `kdj_d_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'kdj_d_hfq',
  `kdj_d_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'kdj_d_qfq',
  `kdj_k_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'kdj_k_bfq',
  `kdj_k_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'kdj_k_hfq',
  `kdj_k_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'kdj_k_qfq',
  `ktn_down_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'ktn_down_bfq',
  `ktn_down_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'ktn_down_hfq',
  `ktn_down_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'ktn_down_qfq',
  `ktn_mid_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'ktn_mid_bfq',
  `ktn_mid_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'ktn_mid_hfq',
  `ktn_mid_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'ktn_mid_qfq',
  `ktn_upper_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'ktn_upper_bfq',
  `ktn_upper_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'ktn_upper_hfq',
  `ktn_upper_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'ktn_upper_qfq',
  `lowdays` DECIMAL(20,4) DEFAULT NULL COMMENT 'lowdays',
  `topdays` DECIMAL(20,4) DEFAULT NULL COMMENT 'topdays',
  `ma_bfq_10` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_bfq_10',
  `ma_bfq_20` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_bfq_20',
  `ma_bfq_250` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_bfq_250',
  `ma_bfq_30` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_bfq_30',
  `ma_bfq_5` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_bfq_5',
  `ma_bfq_60` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_bfq_60',
  `ma_bfq_90` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_bfq_90',
  `ma_hfq_10` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_hfq_10',
  `ma_hfq_20` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_hfq_20',
  `ma_hfq_250` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_hfq_250',
  `ma_hfq_30` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_hfq_30',
  `ma_hfq_5` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_hfq_5',
  `ma_hfq_60` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_hfq_60',
  `ma_hfq_90` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_hfq_90',
  `ma_qfq_10` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_qfq_10',
  `ma_qfq_20` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_qfq_20',
  `ma_qfq_250` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_qfq_250',
  `ma_qfq_30` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_qfq_30',
  `ma_qfq_5` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_qfq_5',
  `ma_qfq_60` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_qfq_60',
  `ma_qfq_90` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_qfq_90',
  `macd_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'macd_bfq',
  `macd_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'macd_hfq',
  `macd_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'macd_qfq',
  `macd_dea_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'macd_dea_bfq',
  `macd_dea_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'macd_dea_hfq',
  `macd_dea_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'macd_dea_qfq',
  `macd_dif_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'macd_dif_bfq',
  `macd_dif_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'macd_dif_hfq',
  `macd_dif_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'macd_dif_qfq',
  `mass_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'mass_bfq',
  `mass_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'mass_hfq',
  `mass_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'mass_qfq',
  `ma_mass_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_mass_bfq',
  `ma_mass_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_mass_hfq',
  `ma_mass_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'ma_mass_qfq',
  `mfi_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'mfi_bfq',
  `mfi_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'mfi_hfq',
  `mfi_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'mfi_qfq',
  `mtm_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'mtm_bfq',
  `mtm_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'mtm_hfq',
  `mtm_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'mtm_qfq',
  `mtmma_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'mtmma_bfq',
  `mtmma_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'mtmma_hfq',
  `mtmma_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'mtmma_qfq',
  `obv_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'obv_bfq',
  `obv_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'obv_hfq',
  `obv_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'obv_qfq',
  `psy_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'psy_bfq',
  `psy_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'psy_hfq',
  `psy_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'psy_qfq',
  `psyma_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'psyma_bfq',
  `psyma_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'psyma_hfq',
  `psyma_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'psyma_qfq',
  `roc_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'roc_bfq',
  `roc_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'roc_hfq',
  `roc_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'roc_qfq',
  `maroc_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'maroc_bfq',
  `maroc_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'maroc_hfq',
  `maroc_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'maroc_qfq',
  `rsi_bfq_12` DECIMAL(20,4) DEFAULT NULL COMMENT 'rsi_bfq_12',
  `rsi_bfq_24` DECIMAL(20,4) DEFAULT NULL COMMENT 'rsi_bfq_24',
  `rsi_bfq_6` DECIMAL(20,4) DEFAULT NULL COMMENT 'rsi_bfq_6',
  `rsi_hfq_12` DECIMAL(20,4) DEFAULT NULL COMMENT 'rsi_hfq_12',
  `rsi_hfq_24` DECIMAL(20,4) DEFAULT NULL COMMENT 'rsi_hfq_24',
  `rsi_hfq_6` DECIMAL(20,4) DEFAULT NULL COMMENT 'rsi_hfq_6',
  `rsi_qfq_12` DECIMAL(20,4) DEFAULT NULL COMMENT 'rsi_qfq_12',
  `rsi_qfq_24` DECIMAL(20,4) DEFAULT NULL COMMENT 'rsi_qfq_24',
  `rsi_qfq_6` DECIMAL(20,4) DEFAULT NULL COMMENT 'rsi_qfq_6',
  `taq_down_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'taq_down_bfq',
  `taq_down_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'taq_down_hfq',
  `taq_down_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'taq_down_qfq',
  `taq_mid_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'taq_mid_bfq',
  `taq_mid_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'taq_mid_hfq',
  `taq_mid_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'taq_mid_qfq',
  `taq_up_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'taq_up_bfq',
  `taq_up_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'taq_up_hfq',
  `taq_up_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'taq_up_qfq',
  `trix_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'trix_bfq',
  `trix_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'trix_hfq',
  `trix_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'trix_qfq',
  `trma_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'trma_bfq',
  `trma_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'trma_hfq',
  `trma_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'trma_qfq',
  `vr_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'vr_bfq',
  `vr_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'vr_hfq',
  `vr_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'vr_qfq',
  `wr_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'wr_bfq',
  `wr_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'wr_hfq',
  `wr_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'wr_qfq',
  `wr1_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'wr1_bfq',
  `wr1_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'wr1_hfq',
  `wr1_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'wr1_qfq',
  `xsii_td1_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'xsii_td1_bfq',
  `xsii_td1_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'xsii_td1_hfq',
  `xsii_td1_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'xsii_td1_qfq',
  `xsii_td2_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'xsii_td2_bfq',
  `xsii_td2_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'xsii_td2_hfq',
  `xsii_td2_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'xsii_td2_qfq',
  `xsii_td3_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'xsii_td3_bfq',
  `xsii_td3_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'xsii_td3_hfq',
  `xsii_td3_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'xsii_td3_qfq',
  `xsii_td4_bfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'xsii_td4_bfq',
  `xsii_td4_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'xsii_td4_hfq',
  `xsii_td4_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'xsii_td4_qfq',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取股票每日技术面因子数据，用于跟踪股票当前走势情况，数据由Tushare社区自产，覆盖全历史；输出参数_bfq表示不复权，_qfq表示前复权 _hfq表示后复';

-- 根据证券交易所交易规则的有关规定，交易所每日发布股票交易严重异常波动情况
DROP TABLE IF EXISTS `ts_stk_high_shock`;
CREATE TABLE `ts_stk_high_shock` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `trade_market` DECIMAL(20,4) DEFAULT NULL COMMENT 'trade_market',
  `reason` VARCHAR(64) DEFAULT NULL COMMENT 'reason',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='根据证券交易所交易规则的有关规定，交易所每日发布股票交易严重异常波动情况';

-- 获取上市公司股东户数数据，数据不定期公布
DROP TABLE IF EXISTS `ts_stk_holdernumber`;
CREATE TABLE `ts_stk_holdernumber` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `holder_num` INT DEFAULT NULL COMMENT 'holder_num',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司股东户数数据，数据不定期公布';

-- 获取上市公司增减持数据，了解重要股东近期及历史上的股份增减变化
DROP TABLE IF EXISTS `ts_stk_holdertrade`;
CREATE TABLE `ts_stk_holdertrade` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `holder_name` VARCHAR(64) DEFAULT NULL COMMENT 'holder_name',
  `holder_type` VARCHAR(64) DEFAULT NULL COMMENT 'holder_type',
  `in_de` VARCHAR(64) DEFAULT NULL COMMENT 'in_de',
  `change_vol` DECIMAL(20,4) DEFAULT NULL COMMENT 'change_vol',
  `change_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'change_ratio',
  `after_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'after_share',
  `after_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'after_ratio',
  `avg_price` DECIMAL(20,4) DEFAULT NULL COMMENT 'avg_price',
  `total_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_share',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司增减持数据，了解重要股东近期及历史上的股份增减变化';

-- 获取全市场（包含A/B股和基金）每日涨跌停价格，包括涨停价格，跌停价格等，每个交易日8点40左右更新当日股票涨跌停价格。
DROP TABLE IF EXISTS `ts_stk_limit`;
CREATE TABLE `ts_stk_limit` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `up_limit` DECIMAL(20,4) DEFAULT NULL COMMENT 'up_limit',
  `down_limit` DECIMAL(20,4) DEFAULT NULL COMMENT 'down_limit',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取全市场（包含A/B股和基金）每日涨跌停价格，包括涨停价格，跌停价格等，每个交易日8点40左右更新当日股票涨跌停价格。';

-- 获取上市公司管理层
DROP TABLE IF EXISTS `ts_stk_managers`;
CREATE TABLE `ts_stk_managers` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `gender` VARCHAR(64) DEFAULT NULL COMMENT 'gender',
  `lev` VARCHAR(64) DEFAULT NULL COMMENT 'lev',
  `title` VARCHAR(64) DEFAULT NULL COMMENT 'title',
  `edu` VARCHAR(64) DEFAULT NULL COMMENT 'edu',
  `national` VARCHAR(64) DEFAULT NULL COMMENT 'national',
  `birthday` VARCHAR(64) DEFAULT NULL COMMENT 'birthday',
  `begin_date` VARCHAR(64) DEFAULT NULL COMMENT 'begin_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司管理层';

-- 获取A股分钟数据，支持1min/5min/15min/30min/60min行情
DROP TABLE IF EXISTS `ts_stk_mins`;
CREATE TABLE `ts_stk_mins` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_time` DECIMAL(20,4) DEFAULT NULL COMMENT 'trade_time',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取A股分钟数据，支持1min/5min/15min/30min/60min行情';

-- 神奇九转（又称“九转序列”）是一种基于技术分析的股票趋势反转指标，其思想来源于技术分析大师汤姆·迪马克（Tom DeMark）的TD序列。该指标的核心功能是通过
DROP TABLE IF EXISTS `ts_stk_nineturn`;
CREATE TABLE `ts_stk_nineturn` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `freq` VARCHAR(64) DEFAULT NULL COMMENT 'freq',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `up_count` VARCHAR(64) DEFAULT NULL COMMENT 'up_count',
  `down_count` VARCHAR(64) DEFAULT NULL COMMENT 'down_count',
  `nine_up_turn` VARCHAR(64) DEFAULT NULL COMMENT 'nine_up_turn',
  `nine_down_turn` VARCHAR(64) DEFAULT NULL COMMENT 'nine_down_turn',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='神奇九转（又称“九转序列”）是一种基于技术分析的股票趋势反转指标，其思想来源于技术分析大师汤姆·迪马克（Tom DeMark）的TD序列。该指标的核心功能是通过';

-- 每日开盘前获取当日股票的股本情况，包括总股本和流通股本，涨跌停价格等。
DROP TABLE IF EXISTS `ts_stk_premarket`;
CREATE TABLE `ts_stk_premarket` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `total_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_share',
  `float_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_share',
  `pre_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close',
  `up_limit` DECIMAL(20,4) DEFAULT NULL COMMENT 'up_limit',
  `down_limit` DECIMAL(20,4) DEFAULT NULL COMMENT 'down_limit',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='每日开盘前获取当日股票的股本情况，包括总股本和流通股本，涨跌停价格等。';

-- 获取上市公司管理层薪酬和持股
DROP TABLE IF EXISTS `ts_stk_rewards`;
CREATE TABLE `ts_stk_rewards` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `title` VARCHAR(64) DEFAULT NULL COMMENT 'title',
  `reward` DECIMAL(20,4) DEFAULT NULL COMMENT 'reward',
  `hold_vol` DECIMAL(20,4) DEFAULT NULL COMMENT 'hold_vol',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司管理层薪酬和持股';

-- 根据证券交易所交易规则的有关规定，交易所每日发布股票交易异常波动情况
DROP TABLE IF EXISTS `ts_stk_shock`;
CREATE TABLE `ts_stk_shock` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `trade_market` DECIMAL(20,4) DEFAULT NULL COMMENT 'trade_market',
  `reason` VARCHAR(64) DEFAULT NULL COMMENT 'reason',
  `period` VARCHAR(64) DEFAULT NULL COMMENT 'period',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='根据证券交易所交易规则的有关规定，交易所每日发布股票交易异常波动情况';

-- 获取上市公司机构调研记录数据
DROP TABLE IF EXISTS `ts_stk_surv`;
CREATE TABLE `ts_stk_surv` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `surv_date` VARCHAR(64) DEFAULT NULL COMMENT 'surv_date',
  `fund_visitors` DECIMAL(20,4) DEFAULT NULL COMMENT 'fund_visitors',
  `rece_place` VARCHAR(64) DEFAULT NULL COMMENT 'rece_place',
  `rece_mode` VARCHAR(64) DEFAULT NULL COMMENT 'rece_mode',
  `rece_org` VARCHAR(64) DEFAULT NULL COMMENT 'rece_org',
  `org_type` VARCHAR(64) DEFAULT NULL COMMENT 'org_type',
  `comp_rece` VARCHAR(64) DEFAULT NULL COMMENT 'comp_rece',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司机构调研记录数据';

-- 周月线复权行情数据
DROP TABLE IF EXISTS `ts_stk_week_month_adj`;
CREATE TABLE `ts_stk_week_month_adj` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `freq` VARCHAR(64) DEFAULT NULL COMMENT 'freq',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `pre_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close',
  `open_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'open_qfq',
  `high_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'high_qfq',
  `low_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'low_qfq',
  `close_qfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'close_qfq',
  `open_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'open_hfq',
  `high_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'high_hfq',
  `low_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'low_hfq',
  `close_hfq` DECIMAL(20,4) DEFAULT NULL COMMENT 'close_hfq',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `change` DECIMAL(20,4) DEFAULT NULL COMMENT 'change',
  `pct_chg` VARCHAR(64) DEFAULT NULL COMMENT 'pct_chg',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='周月线复权行情数据';

-- 股票周/月线行情(每日更新)
DROP TABLE IF EXISTS `ts_stk_weekly_monthly`;
CREATE TABLE `ts_stk_weekly_monthly` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `freq` VARCHAR(64) DEFAULT NULL COMMENT 'freq',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `pre_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `change` DECIMAL(20,4) DEFAULT NULL COMMENT 'change',
  `pct_chg` VARCHAR(64) DEFAULT NULL COMMENT 'pct_chg',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票周/月线行情(每日更新)';

-- 获取基础信息数据，包括股票代码、名称、上市日期、退市日期等
DROP TABLE IF EXISTS `ts_stock_basic`;
CREATE TABLE `ts_stock_basic` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `area` VARCHAR(64) DEFAULT NULL COMMENT 'area',
  `industry` VARCHAR(64) DEFAULT NULL COMMENT 'industry',
  `cnspell` VARCHAR(64) DEFAULT NULL COMMENT 'cnspell',
  `market` VARCHAR(64) DEFAULT NULL COMMENT 'market',
  `list_date` VARCHAR(64) DEFAULT NULL COMMENT 'list_date',
  `act_name` VARCHAR(64) DEFAULT NULL COMMENT 'act_name',
  `act_ent_type` VARCHAR(64) DEFAULT NULL COMMENT 'act_ent_type',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取基础信息数据，包括股票代码、名称、上市日期、退市日期等';

-- 获取上市公司基础信息，单次提取4500条，可以根据交易所分批提取
DROP TABLE IF EXISTS `ts_stock_company`;
CREATE TABLE `ts_stock_company` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `com_name` DECIMAL(20,4) DEFAULT NULL COMMENT 'com_name',
  `com_id` VARCHAR(64) DEFAULT NULL COMMENT 'com_id',
  `exchange` VARCHAR(64) DEFAULT NULL COMMENT 'exchange',
  `chairman` VARCHAR(64) DEFAULT NULL COMMENT 'chairman',
  `manager` VARCHAR(64) DEFAULT NULL COMMENT 'manager',
  `secretary` VARCHAR(64) DEFAULT NULL COMMENT 'secretary',
  `reg_capital` DECIMAL(20,4) DEFAULT NULL COMMENT 'reg_capital',
  `setup_date` VARCHAR(64) DEFAULT NULL COMMENT 'setup_date',
  `province` VARCHAR(64) DEFAULT NULL COMMENT 'province',
  `city` VARCHAR(64) DEFAULT NULL COMMENT 'city',
  `introduction` VARCHAR(64) DEFAULT NULL COMMENT 'introduction',
  `website` VARCHAR(64) DEFAULT NULL COMMENT 'website',
  `email` VARCHAR(64) DEFAULT NULL COMMENT 'email',
  `office` VARCHAR(64) DEFAULT NULL COMMENT 'office',
  `employees` INT DEFAULT NULL COMMENT 'employees',
  `main_business` VARCHAR(64) DEFAULT NULL COMMENT 'main_business',
  `business_scope` VARCHAR(64) DEFAULT NULL COMMENT 'business_scope',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司基础信息，单次提取4500条，可以根据交易所分批提取';

-- 获取沪深港通股票列表
DROP TABLE IF EXISTS `ts_stock_hsgt`;
CREATE TABLE `ts_stock_hsgt` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `type` VARCHAR(64) DEFAULT NULL COMMENT 'type',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `type_name` VARCHAR(64) DEFAULT NULL COMMENT 'type_name',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取沪深港通股票列表';

-- 获取ST股票列表，可根据交易日期获取历史上每天的ST列表权限：3000积分起提示：每天上午9:20更新，单次请求最大返回1000行数据，可循环提取,本接口数据从
DROP TABLE IF EXISTS `ts_stock_st`;
CREATE TABLE `ts_stock_st` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `type` VARCHAR(64) DEFAULT NULL COMMENT 'type',
  `type_name` VARCHAR(64) DEFAULT NULL COMMENT 'type_name',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取ST股票列表，可根据交易日期获取历史上每天的ST列表权限：3000积分起提示：每天上午9:20更新，单次请求最大返回1000行数据，可循环提取,本接口数据从';

-- 按日期方式获取股票每日停复牌信息
DROP TABLE IF EXISTS `ts_suspend_d`;
CREATE TABLE `ts_suspend_d` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `suspend_timing` VARCHAR(64) DEFAULT NULL COMMENT 'suspend_timing',
  `suspend_type` VARCHAR(64) DEFAULT NULL COMMENT 'suspend_type',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='按日期方式获取股票每日停复牌信息';

-- 获取各板块行情，包括成交和估值等数据
DROP TABLE IF EXISTS `ts_tdx_daily`;
CREATE TABLE `ts_tdx_daily` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `pre_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close',
  `change` DECIMAL(20,4) DEFAULT NULL COMMENT 'change',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `rise` DECIMAL(20,4) DEFAULT NULL COMMENT 'rise',
  `vol_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'vol_ratio',
  `turnover_rate` VARCHAR(64) DEFAULT NULL COMMENT 'turnover_rate',
  `swing` DECIMAL(20,4) DEFAULT NULL COMMENT 'swing',
  `up_num` INT DEFAULT NULL COMMENT 'up_num',
  `down_num` INT DEFAULT NULL COMMENT 'down_num',
  `limit_up_num` INT DEFAULT NULL COMMENT 'limit_up_num',
  `limit_down_num` INT DEFAULT NULL COMMENT 'limit_down_num',
  `lu_days` INT DEFAULT NULL COMMENT 'lu_days',
  `3day` DECIMAL(20,4) DEFAULT NULL COMMENT '3day',
  `5day` DECIMAL(20,4) DEFAULT NULL COMMENT '5day',
  `10day` DECIMAL(20,4) DEFAULT NULL COMMENT '10day',
  `20day` DECIMAL(20,4) DEFAULT NULL COMMENT '20day',
  `60day` DECIMAL(20,4) DEFAULT NULL COMMENT '60day',
  `mtd` DECIMAL(20,4) DEFAULT NULL COMMENT 'mtd',
  `ytd` DECIMAL(20,4) DEFAULT NULL COMMENT 'ytd',
  `1year` DECIMAL(20,4) DEFAULT NULL COMMENT '1year',
  `pe` DECIMAL(20,4) DEFAULT NULL COMMENT 'pe',
  `pb` DECIMAL(20,4) DEFAULT NULL COMMENT 'pb',
  `float_mv` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_mv',
  `ab_total_mv` DECIMAL(20,4) DEFAULT NULL COMMENT 'ab_total_mv',
  `float_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_share',
  `total_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_share',
  `bm_buy_net` DECIMAL(20,4) DEFAULT NULL COMMENT 'bm_buy_net',
  `bm_buy_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'bm_buy_ratio',
  `bm_net` DECIMAL(20,4) DEFAULT NULL COMMENT 'bm_net',
  `bm_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'bm_ratio',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取各板块行情，包括成交和估值等数据';

-- 获取板块基础信息，包括概念板块、行业、风格、地域等
DROP TABLE IF EXISTS `ts_tdx_index`;
CREATE TABLE `ts_tdx_index` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `idx_type` VARCHAR(64) DEFAULT NULL COMMENT 'idx_type',
  `idx_count` INT DEFAULT NULL COMMENT 'idx_count',
  `total_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_share',
  `float_share` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_share',
  `total_mv` DECIMAL(20,4) DEFAULT NULL COMMENT 'total_mv',
  `float_mv` DECIMAL(20,4) DEFAULT NULL COMMENT 'float_mv',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取板块基础信息，包括概念板块、行业、风格、地域等';

-- 获取各板块成分股信息
DROP TABLE IF EXISTS `ts_tdx_member`;
CREATE TABLE `ts_tdx_member` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `con_code` VARCHAR(64) NOT NULL COMMENT 'con_code',
  `con_name` VARCHAR(64) DEFAULT NULL COMMENT 'con_name',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取各板块成分股信息';

-- 获取板块指数行情
DROP TABLE IF EXISTS `ts_ths_daily`;
CREATE TABLE `ts_ths_daily` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `pre_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close',
  `avg_price` DECIMAL(20,4) DEFAULT NULL COMMENT 'avg_price',
  `change` DECIMAL(20,4) DEFAULT NULL COMMENT 'change',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `turnover_rate` VARCHAR(64) DEFAULT NULL COMMENT 'turnover_rate',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取板块指数行情';

-- 获取热榜数据，包括热股、概念板块、ETF、可转债、港美股等等，每日盘中提取4次，收盘后4次，最晚22点提取一次。
DROP TABLE IF EXISTS `ts_ths_hot`;
CREATE TABLE `ts_ths_hot` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `data_type` VARCHAR(64) DEFAULT NULL COMMENT 'data_type',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ts_name` DECIMAL(20,4) DEFAULT NULL COMMENT 'ts_name',
  `rank` INT DEFAULT NULL COMMENT 'rank',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `current_price` DECIMAL(20,4) DEFAULT NULL COMMENT 'current_price',
  `concept` VARCHAR(64) DEFAULT NULL COMMENT 'concept',
  `rank_reason` VARCHAR(64) DEFAULT NULL COMMENT 'rank_reason',
  `hot` VARCHAR(64) DEFAULT NULL COMMENT 'hot',
  `rank_time` VARCHAR(64) DEFAULT NULL COMMENT 'rank_time',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取热榜数据，包括热股、概念板块、ETF、可转债、港美股等等，每日盘中提取4次，收盘后4次，最晚22点提取一次。';

-- 获取板块指数，包括概念、行业、特色指数
DROP TABLE IF EXISTS `ts_ths_index`;
CREATE TABLE `ts_ths_index` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `count` INT DEFAULT NULL COMMENT 'count',
  `exchange` VARCHAR(64) DEFAULT NULL COMMENT 'exchange',
  `list_date` VARCHAR(64) DEFAULT NULL COMMENT 'list_date',
  `type` VARCHAR(64) DEFAULT NULL COMMENT 'type',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取板块指数，包括概念、行业、特色指数';

-- 获取概念板块成分列表
DROP TABLE IF EXISTS `ts_ths_member`;
CREATE TABLE `ts_ths_member` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `con_code` VARCHAR(64) NOT NULL COMMENT 'con_code',
  `con_name` VARCHAR(64) DEFAULT NULL COMMENT 'con_name',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取概念板块成分列表';

-- 获取上市公司前十大流通股东数据
DROP TABLE IF EXISTS `ts_top10_floatholders`;
CREATE TABLE `ts_top10_floatholders` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `holder_name` VARCHAR(64) DEFAULT NULL COMMENT 'holder_name',
  `hold_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'hold_amount',
  `hold_ratio` VARCHAR(64) DEFAULT NULL COMMENT 'hold_ratio',
  `hold_float_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'hold_float_ratio',
  `hold_change` DECIMAL(20,4) DEFAULT NULL COMMENT 'hold_change',
  `holder_type` VARCHAR(64) DEFAULT NULL COMMENT 'holder_type',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司前十大流通股东数据';

-- 获取上市公司前十大股东数据，包括持有数量和比例等信息
DROP TABLE IF EXISTS `ts_top10_holders`;
CREATE TABLE `ts_top10_holders` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `ann_date` VARCHAR(64) DEFAULT NULL COMMENT 'ann_date',
  `end_date` VARCHAR(64) DEFAULT NULL COMMENT 'end_date',
  `holder_name` VARCHAR(64) DEFAULT NULL COMMENT 'holder_name',
  `hold_amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'hold_amount',
  `hold_ratio` VARCHAR(64) DEFAULT NULL COMMENT 'hold_ratio',
  `hold_float_ratio` DECIMAL(20,4) DEFAULT NULL COMMENT 'hold_float_ratio',
  `hold_change` DECIMAL(20,4) DEFAULT NULL COMMENT 'hold_change',
  `holder_type` VARCHAR(64) DEFAULT NULL COMMENT 'holder_type',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取上市公司前十大股东数据，包括持有数量和比例等信息';

-- 龙虎榜机构成交明细
DROP TABLE IF EXISTS `ts_top_inst`;
CREATE TABLE `ts_top_inst` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `exalter` DECIMAL(20,4) DEFAULT NULL COMMENT 'exalter',
  `side` DECIMAL(20,4) DEFAULT NULL COMMENT 'side',
  `buy` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy',
  `buy_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'buy_rate',
  `sell` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell',
  `sell_rate` DECIMAL(20,4) DEFAULT NULL COMMENT 'sell_rate',
  `net_buy` DECIMAL(20,4) DEFAULT NULL COMMENT 'net_buy',
  `reason` VARCHAR(64) DEFAULT NULL COMMENT 'reason',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='龙虎榜机构成交明细';

-- 龙虎榜每日交易明细
DROP TABLE IF EXISTS `ts_top_list`;
CREATE TABLE `ts_top_list` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `name` VARCHAR(64) DEFAULT NULL COMMENT 'name',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `pct_change` VARCHAR(64) DEFAULT NULL COMMENT 'pct_change',
  `turnover_rate` VARCHAR(64) DEFAULT NULL COMMENT 'turnover_rate',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  `l_sell` VARCHAR(64) DEFAULT NULL COMMENT 'l_sell',
  `l_buy` VARCHAR(64) DEFAULT NULL COMMENT 'l_buy',
  `l_amount` VARCHAR(64) DEFAULT NULL COMMENT 'l_amount',
  `net_amount` VARCHAR(64) DEFAULT NULL COMMENT 'net_amount',
  `net_rate` VARCHAR(64) DEFAULT NULL COMMENT 'net_rate',
  `amount_rate` VARCHAR(64) DEFAULT NULL COMMENT 'amount_rate',
  `float_values` VARCHAR(64) DEFAULT NULL COMMENT 'float_values',
  `reason` VARCHAR(64) DEFAULT NULL COMMENT 'reason',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='龙虎榜每日交易明细';

-- 获取各大交易所交易日历数据,默认提取的是上交所
DROP TABLE IF EXISTS `ts_trade_cal`;
CREATE TABLE `ts_trade_cal` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `exchange` VARCHAR(64) DEFAULT NULL COMMENT 'exchange',
  `cal_date` VARCHAR(64) DEFAULT NULL COMMENT 'cal_date',
  `is_open` VARCHAR(64) DEFAULT NULL COMMENT 'is_open',
  `pretrade_date` VARCHAR(64) DEFAULT NULL COMMENT 'pretrade_date',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取各大交易所交易日历数据,默认提取的是上交所';

-- 获取A股周线行情，本接口每周最后一个交易日更新，如需要使用每天更新的周线数据，请使用
DROP TABLE IF EXISTS `ts_weekly`;
CREATE TABLE `ts_weekly` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `row_hash` CHAR(32) NOT NULL COMMENT 'MD5 of all field values for dedup',
  `ts_code` VARCHAR(64) NOT NULL COMMENT 'ts_code',
  `trade_date` VARCHAR(64) DEFAULT NULL COMMENT 'trade_date',
  `close` DECIMAL(20,4) DEFAULT NULL COMMENT 'close',
  `open` DECIMAL(20,4) DEFAULT NULL COMMENT 'open',
  `high` DECIMAL(20,4) DEFAULT NULL COMMENT 'high',
  `low` DECIMAL(20,4) DEFAULT NULL COMMENT 'low',
  `pre_close` DECIMAL(20,4) DEFAULT NULL COMMENT 'pre_close',
  `change` DECIMAL(20,4) DEFAULT NULL COMMENT 'change',
  `pct_chg` VARCHAR(64) DEFAULT NULL COMMENT 'pct_chg',
  `vol` INT DEFAULT NULL COMMENT 'vol',
  `amount` DECIMAL(20,4) DEFAULT NULL COMMENT 'amount',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_row_hash` (`row_hash`),
  INDEX `idx_ts_trade` (`ts_code`, `trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='获取A股周线行情，本接口每周最后一个交易日更新，如需要使用每天更新的周线数据，请使用';

