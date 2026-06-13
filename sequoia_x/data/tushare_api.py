"""Tushare Pro Stock Data - Python API Client (108 interfaces)."""
import tushare as ts
from typing import Optional


class TushareAPI:
    """Tushare Pro API wrapper."""

    def __init__(self, token: str):
        """Initialize."""
        ts.set_token(token)
        self.pro = ts.pro_api()

    def __init__(self, token: str):
        """Initialize.
        Args:
        """
        pass  # stub

    def adj_factor(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """本接口由Tushare自行生产，获取股票复权因子，可提取单只股票全部历史复权因子，也可以提取单日全部股票的复权因子。
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期
        - adj_factor (float): 复权因子
        """
        pass  # stub

    def bak_basic(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None):
        """获取备用基础列表，数据从2016年开始
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): TS股票代码
        - name (str): 股票名称
        - industry (str): 行业
        - area (str): 地域
        - pe (float): 市盈率（动）
        - float_share (float): 流通股本（亿）
        - total_share (float): 总股本（亿）
        - total_assets (float): 总资产（亿）
        - liquid_assets (float): 流动资产（亿）
        - fixed_assets (float): 固定资产（亿）
        - reserved (float): 公积金
        - reserved_pershare (float): 每股公积金
        - eps (float): 每股收益
        - bvps (float): 每股净资产
        - pb (float): 市净率
        - list_date (str): 上市日期
        - undp (float): 未分配利润
        - per_undp (float): 每股未分配利润
        - rev_yoy (float): 收入同比（%）
        - profit_yoy (float): 利润同比（%）
        - gpr (float): 毛利率（%）
        - npr (float): 净利润率（%）
        - holder_num (int): 股东人数
        """
        pass  # stub

    def bak_daily(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, offset: Optional[str] = None, limit: Optional[str] = None):
        """获取备用行情，包括特定的行情指标(数据从2017年中左右开始，早期有几天数据缺失，近期正常)
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期
        - name (str): 股票名称
        - pct_change (float): 涨跌幅
        - close (float): 收盘价
        - change (float): 涨跌额
        - open (float): 开盘价
        - high (float): 最高价
        - low (float): 最低价
        - pre_close (float): 昨收价
        - vol_ratio (float): 量比
        - turn_over (float): 换手率
        - swing (float): 振幅
        - vol (float): 成交量
        - amount (float): 成交额
        - selling (float): 内盘（主动卖，手）
        - buying (float): 外盘（主动买， 手）
        - total_share (float): 总股本(亿)
        - float_share (float): 流通股本(亿)
        - pe (float): 市盈(动)
        - industry (str): 所属行业
        - area (str): 所属地域
        - float_mv (float): 流通市值
        - total_mv (float): 总市值
        - avg_price (float): 平均价
        - strength (float): 强弱度(%)
        - activity (float): 活跃度(%)
        - avg_turnover (float): 笔换手
        - attack (float): 攻击波(%)
        - interval_3 (float): 近3月涨幅
        - interval_6 (float): 近6月涨幅
        """
        pass  # stub

    def balancesheet(self, ts_code: Optional[str] = None, ann_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, period: Optional[str] = None, report_type: Optional[str] = None):
        """获取上市公司资产负债表
        Args:
        Returns:
        Columns:
        - ts_code (str): TS股票代码
        - ann_date (str): 公告日期
        - f_ann_date (str): 实际公告日期
        - end_date (str): 报告期
        - report_type (str): 报表类型
        - comp_type (str): 公司类型(1一般工商业2银行3保险4证券)
        - end_type (str): 报告期类型
        - total_share (float): 期末总股本
        - cap_rese (float): 资本公积金
        - undistr_porfit (float): 未分配利润
        - surplus_rese (float): 盈余公积金
        - special_rese (float): 专项储备
        - money_cap (float): 货币资金
        - trad_asset (float): 交易性金融资产
        - notes_receiv (float): 应收票据
        - accounts_receiv (float): 应收账款
        - oth_receiv (float): 其他应收款
        - prepayment (float): 预付款项
        - div_receiv (float): 应收股利
        - int_receiv (float): 应收利息
        - inventories (float): 存货
        - amor_exp (float): 待摊费用
        - nca_within_1y (float): 一年内到期的非流动资产
        - sett_rsrv (float): 结算备付金
        - loanto_oth_bank_fi (float): 拆出资金
        - premium_receiv (float): 应收保费
        - reinsur_receiv (float): 应收分保账款
        - reinsur_res_receiv (float): 应收分保合同准备金
        - pur_resale_fa (float): 买入返售金融资产
        - oth_cur_assets (float): 其他流动资产
        - total_cur_assets (float): 流动资产合计
        - fa_avail_for_sale (float): 可供出售金融资产
        - htm_invest (float): 持有至到期投资
        - lt_eqt_invest (float): 长期股权投资
        - invest_real_estate (float): 投资性房地产
        - time_deposits (float): 定期存款
        - oth_assets (float): 其他资产
        - lt_rec (float): 长期应收款
        - fix_assets (float): 固定资产
        - cip (float): 在建工程
        - const_materials (float): 工程物资
        - fixed_assets_disp (float): 固定资产清理
        - produc_bio_assets (float): 生产性生物资产
        - oil_and_gas_assets (float): 油气资产
        - intan_assets (float): 无形资产
        - r_and_d (float): 研发支出
        - goodwill (float): 商誉
        - lt_amor_exp (float): 长期待摊费用
        - defer_tax_assets (float): 递延所得税资产
        - decr_in_disbur (float): 发放贷款及垫款
        - oth_nca (float): 其他非流动资产
        - total_nca (float): 非流动资产合计
        - cash_reser_cb (float): 现金及存放中央银行款项
        - depos_in_oth_bfi (float): 存放同业和其它金融机构款项
        - prec_metals (float): 贵金属
        - deriv_assets (float): 衍生金融资产
        - rr_reins_une_prem (float): 应收分保未到期责任准备金
        - rr_reins_outstd_cla (float): 应收分保未决赔款准备金
        - rr_reins_lins_liab (float): 应收分保寿险责任准备金
        - rr_reins_lthins_liab (float): 应收分保长期健康险责任准备金
        - refund_depos (float): 存出保证金
        - ph_pledge_loans (float): 保户质押贷款
        - refund_cap_depos (float): 存出资本保证金
        - indep_acct_assets (float): 独立账户资产
        - client_depos (float): 其中：客户资金存款
        - client_prov (float): 其中：客户备付金
        - transac_seat_fee (float): 其中:交易席位费
        - invest_as_receiv (float): 应收款项类投资
        - total_assets (float): 资产总计
        - lt_borr (float): 长期借款
        - st_borr (float): 短期借款
        - cb_borr (float): 向中央银行借款
        - depos_ib_deposits (float): 吸收存款及同业存放
        - loan_oth_bank (float): 拆入资金
        - trading_fl (float): 交易性金融负债
        - notes_payable (float): 应付票据
        - acct_payable (float): 应付账款
        - adv_receipts (float): 预收款项
        - sold_for_repur_fa (float): 卖出回购金融资产款
        - comm_payable (float): 应付手续费及佣金
        - payroll_payable (float): 应付职工薪酬
        - taxes_payable (float): 应交税费
        - int_payable (float): 应付利息
        - div_payable (float): 应付股利
        - oth_payable (float): 其他应付款
        - acc_exp (float): 预提费用
        - deferred_inc (float): 递延收益
        - st_bonds_payable (float): 应付短期债券
        - payable_to_reinsurer (float): 应付分保账款
        - rsrv_insur_cont (float): 保险合同准备金
        - acting_trading_sec (float): 代理买卖证券款
        - acting_uw_sec (float): 代理承销证券款
        - non_cur_liab_due_1y (float): 一年内到期的非流动负债
        - oth_cur_liab (float): 其他流动负债
        - total_cur_liab (float): 流动负债合计
        - bond_payable (float): 应付债券
        - lt_payable (float): 长期应付款
        - specific_payables (float): 专项应付款
        - estimated_liab (float): 预计负债
        - defer_tax_liab (float): 递延所得税负债
        - defer_inc_non_cur_liab (float): 递延收益-非流动负债
        - oth_ncl (float): 其他非流动负债
        - total_ncl (float): 非流动负债合计
        - depos_oth_bfi (float): 同业和其它金融机构存放款项
        - deriv_liab (float): 衍生金融负债
        - depos (float): 吸收存款
        - agency_bus_liab (float): 代理业务负债
        - oth_liab (float): 其他负债
        - prem_receiv_adva (float): 预收保费
        - depos_received (float): 存入保证金
        - ph_invest (float): 保户储金及投资款
        - reser_une_prem (float): 未到期责任准备金
        - reser_outstd_claims (float): 未决赔款准备金
        - reser_lins_liab (float): 寿险责任准备金
        - reser_lthins_liab (float): 长期健康险责任准备金
        - indept_acc_liab (float): 独立账户负债
        - pledge_borr (float): 其中:质押借款
        - indem_payable (float): 应付赔付款
        - policy_div_payable (float): 应付保单红利
        - total_liab (float): 负债合计
        - treasury_share (float): 减:库存股
        - ordin_risk_reser (float): 一般风险准备
        - forex_differ (float): 外币报表折算差额
        - invest_loss_unconf (float): 未确认的投资损失
        - minority_int (float): 少数股东权益
        - total_hldr_eqy_exc_min_int (float): 股东权益合计(不含少数股东权益)
        - total_hldr_eqy_inc_min_int (float): 股东权益合计(含少数股东权益)
        - total_liab_hldr_eqy (float): 负债及股东权益总计
        - lt_payroll_payable (float): 长期应付职工薪酬
        - oth_comp_income (float): 其他综合收益
        - oth_eqt_tools (float): 其他权益工具
        - oth_eqt_tools_p_shr (float): 其他权益工具(优先股)
        - lending_funds (float): 融出资金
        - acc_receivable (float): 应收款项
        - st_fin_payable (float): 应付短期融资款
        - payables (float): 应付款项
        - hfs_assets (float): 持有待售的资产
        - hfs_sales (float): 持有待售的负债
        - cost_fin_assets (float): 以摊余成本计量的金融资产
        - fair_value_fin_assets (float): 以公允价值计量且其变动计入其他综合收益的金融资产
        - cip_total (float): 在建工程(合计)(元)
        - oth_pay_total (float): 其他应付款(合计)(元)
        - long_pay_total (float): 长期应付款(合计)(元)
        - debt_invest (float): 债权投资(元)
        - oth_debt_invest (float): 其他债权投资(元)
        - oth_eq_invest (float): 其他权益工具投资(元)
        - oth_illiq_fin_assets (float): 其他非流动金融资产(元)
        - oth_eq_ppbond (float): 其他权益工具:永续债(元)
        - receiv_financing (float): 应收款项融资
        - use_right_assets (float): 使用权资产
        - lease_liab (float): 租赁负债
        - contract_assets (float): 合同资产
        - contract_liab (float): 合同负债
        - accounts_receiv_bill (float): 应收票据及应收账款
        - accounts_pay (float): 应付票据及应付账款
        - oth_rcv_total (float): 其他应收款(合计)（元）
        - fix_assets_total (float): 固定资产(合计)(元)
        - update_flag (str): 更新标识
        """
        pass  # stub

    def block_trade(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """大宗交易
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - trade_date (str): 交易日历
        - price (float): 成交价
        - vol (float): 成交量（万股）
        - amount (float): 成交金额
        - buyer (str): 买方营业部
        - seller (str): 卖方营业部
        """
        pass  # stub

    def broker_recommend(self, month: Optional[str] = None):
        """获取券商月度金股，一般1日~3日内更新当月数据
        Args:
        Returns:
        Columns:
        - month (str): 月度
        - broker (str): 券商
        - ts_code (str): 股票代码
        - name (str): 股票简称
        """
        pass  # stub

    def bse_mapping(self, o_code: Optional[str] = None, n_code: Optional[str] = None):
        """获取北交所股票代码变更后新旧代码映射表数据
        Args:
        Returns:
        Columns:
        - name (str): 股票名称
        - o_code (str): 原代码
        - n_code (str): 新代码
        - list_date (str): 上市日期
        """
        pass  # stub

    def cashflow(self, ts_code: Optional[str] = None, ann_date: Optional[str] = None, f_ann_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, period: Optional[str] = None, report_type: Optional[str] = None):
        """获取上市公司现金流量表
        Args:
        Returns:
        Columns:
        - ts_code (str): TS股票代码
        - ann_date (str): 公告日期
        - f_ann_date (str): 实际公告日期
        - end_date (str): 报告期
        - comp_type (str): 公司类型(1一般工商业2银行3保险4证券)
        - report_type (str): 报表类型
        - end_type (str): 报告期类型
        - net_profit (float): 净利润
        - finan_exp (float): 财务费用
        - c_fr_sale_sg (float): 销售商品、提供劳务收到的现金
        - recp_tax_rends (float): 收到的税费返还
        - n_depos_incr_fi (float): 客户存款和同业存放款项净增加额
        - n_incr_loans_cb (float): 向中央银行借款净增加额
        - n_inc_borr_oth_fi (float): 向其他金融机构拆入资金净增加额
        - prem_fr_orig_contr (float): 收到原保险合同保费取得的现金
        - n_incr_insured_dep (float): 保户储金净增加额
        - n_reinsur_prem (float): 收到再保业务现金净额
        - n_incr_disp_tfa (float): 处置交易性金融资产净增加额
        - ifc_cash_incr (float): 收取利息和手续费净增加额
        - n_incr_disp_faas (float): 处置可供出售金融资产净增加额
        - n_incr_loans_oth_bank (float): 拆入资金净增加额
        - n_cap_incr_repur (float): 回购业务资金净增加额
        - c_fr_oth_operate_a (float): 收到其他与经营活动有关的现金
        - c_inf_fr_operate_a (float): 经营活动现金流入小计
        - c_paid_goods_s (float): 购买商品、接受劳务支付的现金
        - c_paid_to_for_empl (float): 支付给职工以及为职工支付的现金
        - c_paid_for_taxes (float): 支付的各项税费
        - n_incr_clt_loan_adv (float): 客户贷款及垫款净增加额
        - n_incr_dep_cbob (float): 存放央行和同业款项净增加额
        - c_pay_claims_orig_inco (float): 支付原保险合同赔付款项的现金
        - pay_handling_chrg (float): 支付手续费的现金
        - pay_comm_insur_plcy (float): 支付保单红利的现金
        - oth_cash_pay_oper_act (float): 支付其他与经营活动有关的现金
        - st_cash_out_act (float): 经营活动现金流出小计
        - n_cashflow_act (float): 经营活动产生的现金流量净额
        - oth_recp_ral_inv_act (float): 收到其他与投资活动有关的现金
        - c_disp_withdrwl_invest (float): 收回投资收到的现金
        - c_recp_return_invest (float): 取得投资收益收到的现金
        - n_recp_disp_fiolta (float): 处置固定资产、无形资产和其他长期资产收回的现金净额
        - n_recp_disp_sobu (float): 处置子公司及其他营业单位收到的现金净额
        - stot_inflows_inv_act (float): 投资活动现金流入小计
        - c_pay_acq_const_fiolta (float): 购建固定资产、无形资产和其他长期资产支付的现金
        - c_paid_invest (float): 投资支付的现金
        - n_disp_subs_oth_biz (float): 取得子公司及其他营业单位支付的现金净额
        - oth_pay_ral_inv_act (float): 支付其他与投资活动有关的现金
        - n_incr_pledge_loan (float): 质押贷款净增加额
        - stot_out_inv_act (float): 投资活动现金流出小计
        - n_cashflow_inv_act (float): 投资活动产生的现金流量净额
        - c_recp_borrow (float): 取得借款收到的现金
        - proc_issue_bonds (float): 发行债券收到的现金
        - oth_cash_recp_ral_fnc_act (float): 收到其他与筹资活动有关的现金
        - stot_cash_in_fnc_act (float): 筹资活动现金流入小计
        - free_cashflow (float): 企业自由现金流量
        - c_prepay_amt_borr (float): 偿还债务支付的现金
        - c_pay_dist_dpcp_int_exp (float): 分配股利、利润或偿付利息支付的现金
        - incl_dvd_profit_paid_sc_ms (float): 其中:子公司支付给少数股东的股利、利润
        - oth_cashpay_ral_fnc_act (float): 支付其他与筹资活动有关的现金
        - stot_cashout_fnc_act (float): 筹资活动现金流出小计
        - n_cash_flows_fnc_act (float): 筹资活动产生的现金流量净额
        - eff_fx_flu_cash (float): 汇率变动对现金的影响
        - n_incr_cash_cash_equ (float): 现金及现金等价物净增加额
        - c_cash_equ_beg_period (float): 期初现金及现金等价物余额
        - c_cash_equ_end_period (float): 期末现金及现金等价物余额
        - c_recp_cap_contrib (float): 吸收投资收到的现金
        - incl_cash_rec_saims (float): 其中:子公司吸收少数股东投资收到的现金
        - uncon_invest_loss (float): 未确认投资损失
        - prov_depr_assets (float): 加:资产减值准备
        - depr_fa_coga_dpba (float): 固定资产折旧、油气资产折耗、生产性生物资产折旧
        - amort_intang_assets (float): 无形资产摊销
        - lt_amort_deferred_exp (float): 长期待摊费用摊销
        - decr_deferred_exp (float): 待摊费用减少
        - incr_acc_exp (float): 预提费用增加
        - loss_disp_fiolta (float): 处置固定、无形资产和其他长期资产的损失
        - loss_scr_fa (float): 固定资产报废损失
        - loss_fv_chg (float): 公允价值变动损失
        - invest_loss (float): 投资损失
        - decr_def_inc_tax_assets (float): 递延所得税资产减少
        - incr_def_inc_tax_liab (float): 递延所得税负债增加
        - decr_inventories (float): 存货的减少
        - decr_oper_payable (float): 经营性应收项目的减少
        - incr_oper_payable (float): 经营性应付项目的增加
        - others (float): 其他
        - im_net_cashflow_oper_act (float): 经营活动产生的现金流量净额(间接法)
        - conv_debt_into_cap (float): 债务转为资本
        - conv_copbonds_due_within_1y (float): 一年内到期的可转换公司债券
        - fa_fnc_leases (float): 融资租入固定资产
        - im_n_incr_cash_equ (float): 现金及现金等价物净增加额(间接法)
        - net_dism_capital_add (float): 拆出资金净增加额
        - net_cash_rece_sec (float): 代理买卖证券收到的现金净额(元)
        - credit_impa_loss (float): 信用减值损失
        - use_right_asset_dep (float): 使用权资产折旧
        - oth_loss_asset (float): 其他资产减值损失
        - end_bal_cash (float): 现金的期末余额
        - beg_bal_cash (float): 减:现金的期初余额
        - end_bal_cash_equ (float): 加:现金等价物的期末余额
        - beg_bal_cash_equ (float): 减:现金等价物的期初余额
        - update_flag (str): 更新标志(1最新）
        """
        pass  # stub

    def ccass_hold(self, ts_code: Optional[str] = None, hk_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取中央结算系统持股汇总数据，覆盖全部历史数据，根据交易所披露时间，当日数据在下一交易日早上9点前完成入库
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): 股票代号
        - name (str): 股票名称
        - shareholding (str): 于中央结算系统的持股量(股)
        """
        pass  # stub

    def ccass_hold_detail(self, ts_code: Optional[str] = None, hk_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取中央结算系统机构席位持股明细，数据覆盖
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): 股票代号
        - name (str): 股票名称
        - col_participant_id (str): 参与者编号
        - col_participant_name (str): 机构名称
        - col_shareholding (str): 持股量(股)
        - col_shareholding_percent (str): 占已发行股份/权证/单位百分比(%)
        """
        pass  # stub

    def cyq_chips(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取A股每日的筹码分布情况，提供各价位占比，数据从2018年开始，每天18~19点之间更新当日数据
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期
        - price (float): 成本价格
        - percent (float): 价格占比（%）
        """
        pass  # stub

    def cyq_perf(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取A股每日筹码平均成本和胜率情况，每天18~19点左右更新，数据从2018年开始
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期
        - his_low (float): 历史最低价
        - his_high (float): 历史最高价
        - cost_5pct (float): 5分位成本
        - cost_15pct (float): 15分位成本
        - cost_50pct (float): 50分位成本
        - cost_85pct (float): 85分位成本
        - cost_95pct (float): 95分位成本
        - weight_avg (float): 加权平均成本
        - winner_rate (float): 胜率
        """
        pass  # stub

    def daily(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取股票行情数据，或通过通用行情接口获取数据，包含了前后复权数据
        Args:
        Returns:
        Columns:
        - ts_code (str):
        - trade_date (str):
        - open (float):
        - high (float):
        - low (float):
        - close (float):
        - pre_close (float):
        - change (float):
        - pct_chg (float):
        - vol (float):
        - amount (float):
        """
        pass  # stub

    def daily_basic(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取全部股票每日重要的基本面指标，可用于选股分析、报表展示等。单次请求最大返回6000条数据，可按日线循环提取全部历史。
        Args:
        Returns:
        Columns:
        - ts_code (str): TS股票代码
        - trade_date (str): 交易日期
        - close (float): 当日收盘价
        - turnover_rate (float): 换手率（%）
        - turnover_rate_f (float): 换手率（自由流通股）
        - volume_ratio (float): 量比
        - pe (float): 市盈率（总市值/净利润， 亏损的PE为空）
        - pe_ttm (float): 市盈率（TTM，亏损的PE为空）
        - pb (float): 市净率（总市值/净资产）
        - ps (float): 市销率
        - ps_ttm (float): 市销率（TTM）
        - dv_ratio (float): 股息率 （%），除息日发生在去年期间的派现
        - dv_ttm (float): 股息率（TTM）（%），除息日在近12个月且分红报告期在12个月以内的派现
        - total_share (float): 总股本 （万股）
        - float_share (float): 流通股本 （万股）
        - free_share (float): 自由流通股本 （万）
        - total_mv (float): 总市值 （万元）
        - circ_mv (float): 流通市值（万元）
        - ts (.): pro_api
        - pro (.): daily_basic
        - fields (=): 'ts_code,trade_date,turnover_rate,volume_ratio,pe,pb'
        - query ((): 'daily_basic'
        """
        pass  # stub

    def dc_concept(self, trade_date: Optional[str] = None, theme_code: Optional[str] = None, name: Optional[str] = None):
        """获取概念题材列表，每天盘后更新
        Args:
        Returns:
        Columns:
        - theme_code (str): 题材code
        - trade_date (str): 交易日期
        """
        pass  # stub

    def dc_concept_cons(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, theme_code: Optional[str] = None):
        """获取概念题材的成分股，每天盘后更新
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期
        """
        pass  # stub

    def dc_daily(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, idx_type: Optional[str] = None):
        """获取概念板块、行业指数板块、地域板块行情数据，历史数据开始于2020年
        Args:
        Returns:
        Columns:
        - ts_code (str): 板块代码
        - trade_date (str): 交易日
        - close (float): 收盘点位
        - open (float): 开盘点位
        - high (float): 最高点位
        - low (float): 最低点位
        - change (float): 涨跌点位
        - pct_change (float): 涨跌幅
        - vol (float): 成交量(股)
        - amount (float): 成交额(元)
        - swing (float): 振幅
        - turnover_rate (float): 换手率
        """
        pass  # stub

    def dc_hot(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None, market: Optional[str] = None, hot_type: Optional[str] = None, is_new: Optional[str] = None):
        """获取热榜数据，包括A股市场、ETF基金、港股市场、美股市场等等，每日盘中提取4次，收盘后4次，最晚22点提取一次。
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - data_type (str): 数据类型
        - ts_code (str): 股票代码
        - ts_name (str): 股票名称
        - rank (int): 排行或者热度
        - pct_change (float): 涨跌幅%
        - current_price (float): 当前价
        - rank_time (str): 排行榜获取时间
        """
        pass  # stub

    def dc_index(self, ts_code: Optional[str] = None, name: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, idx_type: Optional[str] = None):
        """获取每个交易日的概念板块数据，支持按日期查询
        Args:
        Returns:
        Columns:
        - ts_code (str): 概念代码
        - trade_date (str): 交易日期
        - name (str): 概念名称
        - leading (str): 领涨股票名称
        - leading_code (str): 领涨股票代码
        - pct_change (float): 涨跌幅
        - leading_pct (float): 领涨股票涨跌幅
        - total_mv (float): 总市值（万元）
        - turnover_rate (float): 换手率
        - up_num (int): 上涨家数
        - down_num (int): 下降家数
        - idx_type (str): 板块类型(行业板块、概念板块、地域板块)
        - level (str): 行业层级
        """
        pass  # stub

    def dc_member(self, ts_code: Optional[str] = None, con_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取板块每日成分数据，可以根据概念板块代码和交易日期，获取历史成分
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): 概念代码
        - con_code (str): 成分代码
        - name (str): 成分股名称
        """
        pass  # stub

    def disclosure_date(self, ts_code: Optional[str] = None, end_date: Optional[str] = None, pre_date: Optional[str] = None, ann_date: Optional[str] = None, actual_date: Optional[str] = None):
        """获取财报披露计划日期
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - ann_date (str): 最新披露公告日
        - end_date (str): 报告期
        - pre_date (str): 预计披露日期
        - actual_date (str): 实际披露日期
        - modify_date (str): 披露日期修正记录
        """
        pass  # stub

    def dividend(self, ts_code: Optional[str] = None, ann_date: Optional[str] = None, record_date: Optional[str] = None, ex_date: Optional[str] = None, imp_ann_date: Optional[str] = None):
        """分红送股数据
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - end_date (str): 分红年度
        - ann_date (str): 预案公告日
        - div_proc (str): 实施进度
        - stk_div (float): 每股送转
        - stk_bo_rate (float): 每股送股比例
        - stk_co_rate (float): 每股转增比例
        - cash_div (float): 每股分红（税后）
        - cash_div_tax (float): 每股分红（税前）
        - record_date (str): 股权登记日
        - ex_date (str): 除权除息日
        - pay_date (str): 派息日
        - div_listdate (str): 红股上市日
        - imp_ann_date (str): 实施公告日
        - base_date (str): 基准日
        - base_share (float): 基准股本（万）
        """
        pass  # stub

    def express(self, ts_code: Optional[str] = None, ann_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, period: Optional[str] = None):
        """获取上市公司业绩快报
        Args:
        Returns:
        Columns:
        - ts_code (str): TS股票代码
        - ann_date (str): 公告日期
        - end_date (str): 报告期
        - revenue (float): 营业收入(元)
        - operate_profit (float): 营业利润(元)
        - total_profit (float): 利润总额(元)
        - n_income (float): 净利润(元)
        - total_assets (float): 总资产(元)
        - total_hldr_eqy_exc_min_int (float): 股东权益合计(不含少数股东权益)(元)
        - diluted_eps (float): 每股收益(摊薄)(元)
        - diluted_roe (float): 净资产收益率(摊薄)(%)
        - yoy_net_profit (float): 去年同期修正后净利润
        - bps (float): 每股净资产
        - yoy_sales (float): 同比增长率:营业收入
        - yoy_op (float): 同比增长率:营业利润
        - yoy_tp (float): 同比增长率:利润总额
        - yoy_dedu_np (float): 同比增长率:归属母公司股东的净利润
        - yoy_eps (float): 同比增长率:基本每股收益
        - yoy_roe (float): 同比增减:加权平均净资产收益率
        - growth_assets (float): 比年初增长率:总资产
        - yoy_equity (float): 比年初增长率:归属母公司的股东权益
        - growth_bps (float): 比年初增长率:归属于母公司股东的每股净资产
        - or_last_year (float): 去年同期营业收入
        - op_last_year (float): 去年同期营业利润
        - tp_last_year (float): 去年同期利润总额
        - np_last_year (float): 去年同期净利润
        - eps_last_year (float): 去年同期每股收益
        - open_net_assets (float): 期初净资产
        - open_bps (float): 期初每股净资产
        - perf_summary (str): 业绩简要
        """
        pass  # stub

    def fina_audit(self, ts_code: Optional[str] = None, ann_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, period: Optional[str] = None):
        """获取上市公司定期财务审计意见数据
        Args:
        Returns:
        Columns:
        - ts_code (str): TS股票代码
        - ann_date (str): 公告日期
        - end_date (str): 报告期
        - audit_result (str): 审计结果
        - audit_fees (float): 审计总费用（元）
        - audit_agency (str): 会计事务所
        - audit_sign (str): 签字会计师
        - ts (.): pro_api
        - pro (.): fina_audit
        """
        pass  # stub

    def fina_indicator(self, ts_code: Optional[str] = None, ann_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, period: Optional[str] = None):
        """获取上市公司财务指标数据，为避免服务器压力，现阶段每次请求最多返回100条记录，可通过设置日期多次请求获取更多数据。
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - ann_date (str): 公告日期
        - end_date (str): 报告期
        - eps (float): 基本每股收益
        - dt_eps (float): 稀释每股收益
        - total_revenue_ps (float): 每股营业总收入
        - revenue_ps (float): 每股营业收入
        - capital_rese_ps (float): 每股资本公积
        - surplus_rese_ps (float): 每股盈余公积
        - undist_profit_ps (float): 每股未分配利润
        - extra_item (float): 非经常性损益
        - profit_dedt (float): 扣除非经常性损益后的净利润（扣非净利润）
        - gross_margin (float): 毛利
        - current_ratio (float): 流动比率
        - quick_ratio (float): 速动比率
        - cash_ratio (float): 保守速动比率
        - invturn_days (float): 存货周转天数
        - arturn_days (float): 应收账款周转天数
        - inv_turn (float): 存货周转率
        - ar_turn (float): 应收账款周转率
        - ca_turn (float): 流动资产周转率
        - fa_turn (float): 固定资产周转率
        - assets_turn (float): 总资产周转率
        - op_income (float): 经营活动净收益
        - valuechange_income (float): 价值变动净收益
        - interst_income (float): 利息费用
        - daa (float): 折旧与摊销
        - ebit (float): 息税前利润
        - ebitda (float): 息税折旧摊销前利润
        - fcff (float): 企业自由现金流量
        - fcfe (float): 股权自由现金流量
        - current_exint (float): 无息流动负债
        - noncurrent_exint (float): 无息非流动负债
        - interestdebt (float): 带息债务
        - netdebt (float): 净债务
        - tangible_asset (float): 有形资产
        - working_capital (float): 营运资金
        - networking_capital (float): 营运流动资本
        - invest_capital (float): 全部投入资本
        - retained_earnings (float): 留存收益
        - diluted2_eps (float): 期末摊薄每股收益
        - bps (float): 每股净资产
        - ocfps (float): 每股经营活动产生的现金流量净额
        - retainedps (float): 每股留存收益
        - cfps (float): 每股现金流量净额
        - ebit_ps (float): 每股息税前利润
        - fcff_ps (float): 每股企业自由现金流量
        - fcfe_ps (float): 每股股东自由现金流量
        - netprofit_margin (float): 销售净利率
        - grossprofit_margin (float): 销售毛利率
        - cogs_of_sales (float): 销售成本率
        - expense_of_sales (float): 销售期间费用率
        - profit_to_gr (float): 净利润/营业总收入
        - saleexp_to_gr (float): 销售费用/营业总收入
        - adminexp_of_gr (float): 管理费用/营业总收入
        - finaexp_of_gr (float): 财务费用/营业总收入
        - impai_ttm (float): 资产减值损失/营业总收入
        - gc_of_gr (float): 营业总成本/营业总收入
        - op_of_gr (float): 营业利润/营业总收入
        - ebit_of_gr (float): 息税前利润/营业总收入
        - roe (float): 净资产收益率
        - roe_waa (float): 加权平均净资产收益率
        - roe_dt (float): 净资产收益率(扣除非经常损益)
        - roa (float): 总资产报酬率
        - npta (float): 总资产净利润
        - roic (float): 投入资本回报率
        - roe_yearly (float): 年化净资产收益率
        - roa2_yearly (float): 年化总资产报酬率
        - roe_avg (float): 平均净资产收益率(增发条件)
        - opincome_of_ebt (float): 经营活动净收益/利润总额
        - investincome_of_ebt (float): 价值变动净收益/利润总额
        - n_op_profit_of_ebt (float): 营业外收支净额/利润总额
        - tax_to_ebt (float): 所得税/利润总额
        - dtprofit_to_profit (float): 扣除非经常损益后的净利润/净利润
        - salescash_to_or (float): 销售商品提供劳务收到的现金/营业收入
        - ocf_to_or (float): 经营活动产生的现金流量净额/营业收入
        - ocf_to_opincome (float): 经营活动产生的现金流量净额/经营活动净收益
        - capitalized_to_da (float): 资本支出/折旧和摊销
        - debt_to_assets (float): 资产负债率
        - assets_to_eqt (float): 权益乘数
        - dp_assets_to_eqt (float): 权益乘数(杜邦分析)
        - ca_to_assets (float): 流动资产/总资产
        - nca_to_assets (float): 非流动资产/总资产
        - tbassets_to_totalassets (float): 有形资产/总资产
        - int_to_talcap (float): 带息债务/全部投入资本
        - eqt_to_talcapital (float): 归属于母公司的股东权益/全部投入资本
        - currentdebt_to_debt (float): 流动负债/负债合计
        - longdeb_to_debt (float): 非流动负债/负债合计
        - ocf_to_shortdebt (float): 经营活动产生的现金流量净额/流动负债
        - debt_to_eqt (float): 产权比率
        - eqt_to_debt (float): 归属于母公司的股东权益/负债合计
        - eqt_to_interestdebt (float): 归属于母公司的股东权益/带息债务
        - tangibleasset_to_debt (float): 有形资产/负债合计
        - tangasset_to_intdebt (float): 有形资产/带息债务
        - tangibleasset_to_netdebt (float): 有形资产/净债务
        - ocf_to_debt (float): 经营活动产生的现金流量净额/负债合计
        - ocf_to_interestdebt (float): 经营活动产生的现金流量净额/带息债务
        - ocf_to_netdebt (float): 经营活动产生的现金流量净额/净债务
        - ebit_to_interest (float): 已获利息倍数(EBIT/利息费用)
        - longdebt_to_workingcapital (float): 长期债务与营运资金比率
        - ebitda_to_debt (float): 息税折旧摊销前利润/负债合计
        - turn_days (float): 营业周期
        - roa_yearly (float): 年化总资产净利率
        - roa_dp (float): 总资产净利率(杜邦分析)
        - fixed_assets (float): 固定资产合计
        - profit_prefin_exp (float): 扣除财务费用前营业利润
        - non_op_profit (float): 非营业利润
        - op_to_ebt (float): 营业利润／利润总额
        - nop_to_ebt (float): 非营业利润／利润总额
        - ocf_to_profit (float): 经营活动产生的现金流量净额／营业利润
        - cash_to_liqdebt (float): 货币资金／流动负债
        - cash_to_liqdebt_withinterest (float): 货币资金／带息流动负债
        - op_to_liqdebt (float): 营业利润／流动负债
        - op_to_debt (float): 营业利润／负债合计
        - roic_yearly (float): 年化投入资本回报率
        - total_fa_trun (float): 固定资产合计周转率
        - profit_to_op (float): 利润总额／营业收入
        - q_opincome (float): 经营活动单季度净收益
        - q_investincome (float): 价值变动单季度净收益
        - q_dtprofit (float): 扣除非经常损益后的单季度净利润
        - q_eps (float): 每股收益(单季度)
        - q_netprofit_margin (float): 销售净利率(单季度)
        - q_gsprofit_margin (float): 销售毛利率(单季度)
        - q_exp_to_sales (float): 销售期间费用率(单季度)
        - q_profit_to_gr (float): 净利润／营业总收入(单季度)
        - q_saleexp_to_gr (float): 销售费用／营业总收入 (单季度)
        - q_adminexp_to_gr (float): 管理费用／营业总收入 (单季度)
        - q_finaexp_to_gr (float): 财务费用／营业总收入 (单季度)
        - q_impair_to_gr_ttm (float): 资产减值损失／营业总收入(单季度)
        - q_gc_to_gr (float): 营业总成本／营业总收入 (单季度)
        - q_op_to_gr (float): 营业利润／营业总收入(单季度)
        - q_roe (float): 净资产收益率(单季度)
        - q_dt_roe (float): 净资产单季度收益率(扣除非经常损益)
        - q_npta (float): 总资产净利润(单季度)
        - q_opincome_to_ebt (float): 经营活动净收益／利润总额(单季度)
        - q_investincome_to_ebt (float): 价值变动净收益／利润总额(单季度)
        - q_dtprofit_to_profit (float): 扣除非经常损益后的净利润／净利润(单季度)
        - q_salescash_to_or (float): 销售商品提供劳务收到的现金／营业收入(单季度)
        - q_ocf_to_sales (float): 经营活动产生的现金流量净额／营业收入(单季度)
        - q_ocf_to_or (float): 经营活动产生的现金流量净额／经营活动净收益(单季度)
        - basic_eps_yoy (float): 基本每股收益同比增长率(%)
        - dt_eps_yoy (float): 稀释每股收益同比增长率(%)
        - cfps_yoy (float): 每股经营活动产生的现金流量净额同比增长率(%)
        - op_yoy (float): 营业利润同比增长率(%)
        - ebt_yoy (float): 利润总额同比增长率(%)
        - netprofit_yoy (float): 归属母公司股东的净利润同比增长率(%)
        - dt_netprofit_yoy (float): 归属母公司股东的净利润-扣除非经常损益同比增长率(%)
        - ocf_yoy (float): 经营活动产生的现金流量净额同比增长率(%)
        - roe_yoy (float): 净资产收益率(摊薄)同比增长率(%)
        - bps_yoy (float): 每股净资产相对年初增长率(%)
        - assets_yoy (float): 资产总计相对年初增长率(%)
        - eqt_yoy (float): 归属母公司的股东权益相对年初增长率(%)
        - tr_yoy (float): 营业总收入同比增长率(%)
        - or_yoy (float): 营业收入同比增长率(%)
        - q_gr_yoy (float): 营业总收入同比增长率(%)(单季度)
        - q_gr_qoq (float): 营业总收入环比增长率(%)(单季度)
        - q_sales_yoy (float): 营业收入同比增长率(%)(单季度)
        - q_sales_qoq (float): 营业收入环比增长率(%)(单季度)
        - q_op_yoy (float): 营业利润同比增长率(%)(单季度)
        - q_op_qoq (float): 营业利润环比增长率(%)(单季度)
        - q_profit_yoy (float): 净利润同比增长率(%)(单季度)
        - q_profit_qoq (float): 净利润环比增长率(%)(单季度)
        - q_netprofit_yoy (float): 归属母公司股东的净利润同比增长率(%)(单季度)
        - q_netprofit_qoq (float): 归属母公司股东的净利润环比增长率(%)(单季度)
        - equity_yoy (float): 净资产同比增长率
        - rd_exp (float): 研发费用
        - update_flag (str): 更新标识
        """
        pass  # stub

    def fina_mainbz(self, ts_code: Optional[str] = None, period: Optional[str] = None, type: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获得上市公司主营业务构成，分地区和产品两种方式
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - end_date (str): 报告期
        - bz_item (str): 主营业务来源
        - bz_code (str): 主营业务来源类型（P按产品 D按地区 I按行业）
        - bz_sales (float): 主营业务收入(元)
        - bz_profit (float): 主营业务利润(元)
        - bz_cost (float): 主营业务成本(元)
        - curr_type (str): 货币代码
        - update_flag (str): 是否更新
        - ts (.): pro_api
        - pro (.): fina_mainbz
        - fields (=): 'ts_code,end_date,bz_item,bz_sales'
        """
        pass  # stub

    def forecast(self, ts_code: Optional[str] = None, ann_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, period: Optional[str] = None, type: Optional[str] = None):
        """获取业绩预告数据
        Args:
        Returns:
        Columns:
        - ts_code (str): TS股票代码
        - ann_date (str): 公告日期
        - end_date (str): 报告期
        - type (str): 业绩预告类型(预增/预减/扭亏/首亏/续亏/续盈/略增/略减)
        - p_change_min (float): 预告净利润变动幅度下限（%）
        - p_change_max (float): 预告净利润变动幅度上限（%）
        - net_profit_min (float): 预告净利润下限（万元）
        - net_profit_max (float): 预告净利润上限（万元）
        - last_parent_net (float): 上年同期归属母公司净利润
        - first_ann_date (str): 首次公告日
        - summary (str): 业绩预告摘要
        - change_reason (str): 业绩变动原因
        """
        pass  # stub

    def ggt_daily(self, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取港股通每日成交信息，数据从2014年开始
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - buy_amount (float): 买入成交金额（亿元）
        - buy_volume (float): 买入成交笔数（万笔）
        - sell_amount (float): 卖出成交金额（亿元）
        - sell_volume (float): 卖出成交笔数（万笔）
        """
        pass  # stub

    def ggt_top10(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, market_type: Optional[str] = None):
        """获取港股通每日成交数据，其中包括沪市、深市详细数据，每天18~20点之间完成当日更新
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): 股票代码
        - name (str): 股票名称
        - close (float): 收盘价
        - p_change (float): 涨跌幅
        - rank (int): 资金排名
        - market_type (str): 市场类型 2：港股通（沪） 4：港股通（深）
        - amount (float): 累计成交金额（元）
        - net_amount (float): 净买入金额（元）
        - sh_amount (float): 沪市成交金额（元）
        - sh_net_amount (float): 沪市净买入金额（元）
        - sh_buy (float): 沪市买入金额（元）
        - sh_sell (float): 沪市卖出金额
        - sz_amount (float): 深市成交金额（元）
        - sz_net_amount (float): 深市净买入金额（元）
        - sz_buy (float): 深市买入金额（元）
        - sz_sell (float): 深市卖出金额（元）
        - ts (.): pro_api
        - ggt_top10 ((): trade_date
        - query ((): 'ggt_top10'
        - end_date (=): '20180727'
        """
        pass  # stub

    def hk_hold(self, code: Optional[str] = None, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, exchange: Optional[str] = None):
        """获取沪深港股通持股明细，数据来源港交所。
        Args:
        Returns:
        Columns:
        - code (str): 原始代码
        - trade_date (str): 交易日期
        - ts_code (str): TS代码
        - name (str): 股票名称
        - vol (int): 持股数量(股)
        - ratio (float): 持股占比（%），占已发行股份百分比
        - exchange (str): 类型：SH沪股通SZ深股通HK港股通
        """
        pass  # stub

    def hm_detail(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None, hm_name: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取每日游资交易明细，数据开始于2022年8。游资分类名录，请点击
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): 股票代码
        - ts_name (str): 股票名称
        - buy_amount (float): 买入金额（元）
        - sell_amount (float): 卖出金额（元）
        - net_amount (float): 净买卖（元）
        - hm_name (str): 游资名称
        - hm_orgs (str): 关联机构（一般为营业部或机构专用）
        - tag (str): 标签
        """
        pass  # stub

    def hm_list(self, name: Optional[str] = None):
        """获取游资分类名录信息
        Args:
        Returns:
        Columns:
        - name (str): 游资名称
        """
        pass  # stub

    def hsgt_top10(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, market_type: Optional[str] = None):
        """获取沪股通、深股通每日前十大成交详细数据，每天18~20点之间完成当日更新
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): 股票代码
        - name (str): 股票名称
        - close (float): 收盘价
        - change (float): 涨跌额
        - rank (int): 资金排名
        - market_type (str): 市场类型（1：沪市 3：深市）
        - amount (float): 成交金额（元）
        - net_amount (float): 净成交金额（元）
        - buy (float): 买入金额（元）
        - sell (float): 卖出金额（元）
        """
        pass  # stub

    def income(self, ts_code: Optional[str] = None, ann_date: Optional[str] = None, f_ann_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, period: Optional[str] = None, report_type: Optional[str] = None):
        """获取上市公司财务利润表数据
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - ann_date (str): 公告日期
        - f_ann_date (str): 实际公告日期
        - end_date (str): 报告期
        - report_type (str): 报告类型 见底部表
        - comp_type (str): 公司类型(1一般工商业2银行3保险4证券)
        - end_type (str): 报告期类型
        - basic_eps (float): 基本每股收益
        - diluted_eps (float): 稀释每股收益
        - total_revenue (float): 营业总收入
        - revenue (float): 营业收入
        - int_income (float): 利息收入
        - prem_earned (float): 已赚保费
        - comm_income (float): 手续费及佣金收入
        - n_commis_income (float): 手续费及佣金净收入
        - n_oth_income (float): 其他经营净收益
        - n_oth_b_income (float): 加:其他业务净收益
        - prem_income (float): 保险业务收入
        - out_prem (float): 减:分出保费
        - une_prem_reser (float): 提取未到期责任准备金
        - reins_income (float): 其中:分保费收入
        - n_sec_tb_income (float): 代理买卖证券业务净收入
        - n_sec_uw_income (float): 证券承销业务净收入
        - n_asset_mg_income (float): 受托客户资产管理业务净收入
        - oth_b_income (float): 其他业务收入
        - fv_value_chg_gain (float): 加:公允价值变动净收益
        - invest_income (float): 加:投资净收益
        - ass_invest_income (float): 其中:对联营企业和合营企业的投资收益
        - forex_gain (float): 加:汇兑净收益
        - total_cogs (float): 营业总成本
        - oper_cost (float): 减:营业成本
        - int_exp (float): 减:利息支出
        - comm_exp (float): 减:手续费及佣金支出
        - biz_tax_surchg (float): 减:营业税金及附加
        - sell_exp (float): 减:销售费用
        - admin_exp (float): 减:管理费用
        - fin_exp (float): 减:财务费用
        - assets_impair_loss (float): 减:资产减值损失
        - prem_refund (float): 退保金
        - compens_payout (float): 赔付总支出
        - reser_insur_liab (float): 提取保险责任准备金
        - div_payt (float): 保户红利支出
        - reins_exp (float): 分保费用
        - oper_exp (float): 营业支出
        - compens_payout_refu (float): 减:摊回赔付支出
        - insur_reser_refu (float): 减:摊回保险责任准备金
        - reins_cost_refund (float): 减:摊回分保费用
        - other_bus_cost (float): 其他业务成本
        - operate_profit (float): 营业利润
        - non_oper_income (float): 加:营业外收入
        - non_oper_exp (float): 减:营业外支出
        - nca_disploss (float): 其中:减:非流动资产处置净损失
        - total_profit (float): 利润总额
        - income_tax (float): 所得税费用
        - n_income (float): 净利润(含少数股东损益)
        - n_income_attr_p (float): 净利润(不含少数股东损益)
        - minority_gain (float): 少数股东损益
        - oth_compr_income (float): 其他综合收益
        - t_compr_income (float): 综合收益总额
        - compr_inc_attr_p (float): 归属于母公司(或股东)的综合收益总额
        - compr_inc_attr_m_s (float): 归属于少数股东的综合收益总额
        - ebit (float): 息税前利润
        - ebitda (float): 息税折旧摊销前利润
        - insurance_exp (float): 保险业务支出
        - undist_profit (float): 年初未分配利润
        - distable_profit (float): 可分配利润
        - rd_exp (float): 研发费用
        - fin_exp_int_exp (float): 财务费用:利息费用
        - fin_exp_int_inc (float): 财务费用:利息收入
        - transfer_surplus_rese (float): 盈余公积转入
        - transfer_housing_imprest (float): 住房周转金转入
        - transfer_oth (float): 其他转入
        - adj_lossgain (float): 调整以前年度损益
        - withdra_legal_surplus (float): 提取法定盈余公积
        - withdra_legal_pubfund (float): 提取法定公益金
        - withdra_biz_devfund (float): 提取企业发展基金
        - withdra_rese_fund (float): 提取储备基金
        - withdra_oth_ersu (float): 提取任意盈余公积金
        - workers_welfare (float): 职工奖金福利
        - distr_profit_shrhder (float): 可供股东分配的利润
        - prfshare_payable_dvd (float): 应付优先股股利
        - comshare_payable_dvd (float): 应付普通股股利
        - capit_comstock_div (float): 转作股本的普通股股利
        - net_after_nr_lp_correct (float): 扣除非经常性损益后的净利润（更正前）
        - credit_impa_loss (float): 信用减值损失
        - net_expo_hedging_benefits (float): 净敞口套期收益
        - oth_impair_loss_assets (float): 其他资产减值损失
        - total_opcost (float): 营业总成本（二）
        - amodcost_fin_assets (float): 以摊余成本计量的金融资产终止确认收益
        - oth_income (float): 其他收益
        - asset_disp_income (float): 资产处置收益
        - continued_net_profit (float): 持续经营净利润
        - end_net_profit (float): 终止经营净利润
        - update_flag (str): 更新标识
        """
        pass  # stub

    def kpl_concept_cons(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None, con_code: Optional[str] = None):
        """获取概念题材的成分股
        Args:
        Returns:
        Columns:
        - ts_code (str): 题材ID
        - name (str): 题材名称
        - con_name (str): 股票名称
        - con_code (str): 股票代码
        - trade_date (str): 交易日期
        """
        pass  # stub

    def kpl_list(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, tag: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取涨停、跌停、炸板等榜单数据
        Args:
        Returns:
        Columns:
        - ts_code (str): 代码
        """
        pass  # stub

    def limit_cpt_list(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取每天涨停股票最多最强的概念板块，可以分析强势板块的轮动，判断资金动向
        Args:
        Returns:
        Columns:
        - ts_code (str): 板块代码
        - name (str): 板块名称
        - trade_date (str): 交易日期
        - days (int): 上榜天数
        - up_stat (str): 连板高度
        - cons_nums (int): 连板家数
        - up_nums (int): 涨停家数
        - pct_chg (float): 涨跌幅%
        - rank (str): 板块热点排名
        """
        pass  # stub

    def limit_list_d(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None, limit_type: Optional[str] = None, exchange: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取A股每日涨跌停、炸板数据情况，数据从2020年开始（不提供ST股票的统计）
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): 股票代码
        - industry (str): 所属行业
        - name (str): 股票名称
        - close (float): 收盘价
        - pct_chg (float): 涨跌幅
        - amount (float): 成交额
        - limit_amount (float): 板上成交金额(成交价格为该股票跌停价的所有成交额的总和，涨停无此数据)
        - float_mv (float): 流通市值
        - total_mv (float): 总市值
        - turnover_ratio (float): 换手率
        - fd_amount (float): 封单金额（以涨停价买入挂单的资金总量）
        - first_time (str): 首次封板时间（跌停无此数据）
        - last_time (str): 最后封板时间
        - open_times (int): 炸板次数(跌停为开板次数)
        - up_stat (str): 涨停统计（N/T T天有N次涨停）
        - limit_times (int): 连板数（个股连续封板数量）
        - limit (str): D跌停U涨停Z炸板
        """
        pass  # stub

    def limit_list_ths(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None, limit_type: Optional[str] = None, market: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取同花顺每日涨跌停榜单数据，历史数据从20231101开始提供，增量每天16点左右更新
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): 股票代码
        - name (str): 股票名称
        - price (float): 收盘价(元)
        - pct_chg (float): 涨跌幅%
        - open_num (int): 打开次数
        - lu_desc (str): 涨停原因
        - limit_type (str): 板单类别
        - tag (str): 涨停标签
        - status (str): 涨停状态（N连板、一字板）
        - first_lu_time (str): 首次涨停时间
        - last_lu_time (str): 最后涨停时间
        - first_ld_time (str): 首次跌停时间
        - last_ld_time (str): 最后跌停时间
        - limit_order (float): 封单量(元
        - limit_amount (float): 封单额(元
        - turnover_rate (float): 换手率%
        - free_float (float): 实际流通(元
        - lu_limit_order (float): 最大封单(元
        - limit_up_suc_rate (float): 近一年涨停封板率
        - turnover (float): 成交额
        - rise_rate (float): 涨速
        - sum_float (float): 总市值（亿元）
        - market_type (str): 股票类型：HS沪深主板、GEM创业板、STAR科创板
        """
        pass  # stub

    def limit_step(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, nums: Optional[str] = None):
        """获取每天连板个数晋级的股票，可以分析出每天连续涨停进阶个数，判断强势热度
        Args:
        Returns:
        Columns:
        - ts_code (str): 代码
        """
        pass  # stub

    def margin(self, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, exchange_id: Optional[str] = None):
        """获取融资融券每日交易汇总数据，交易所于每天8点30左右更新上一日数据
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - exchange_id (str): 交易所代码（SSE上交所SZSE深交所BSE北交所）
        - rzye (float): 融资余额(元)
        - rzmre (float): 融资买入额(元)
        - rzche (float): 融资偿还额(元)
        - rqye (float): 融券余额(元)
        - rqmcl (float): 融券卖出量(股,份,手)
        - rzrqye (float): 融资融券余额(元)
        - rqyl (float): 融券余量(股,份,手)
        - ts (.): pro_api
        - pro (.): margin
        - df (=): pro
        """
        pass  # stub

    def margin_detail(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取沪深两市每日融资融券明细，，交易所于每天8点30左右更新上一日数据
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): TS股票代码
        - name (str): 股票名称 （20190910后有数据）
        - rzye (float): 融资余额(元)
        - rqye (float): 融券余额(元)
        - rzmre (float): 融资买入额(元)
        - rqyl (float): 融券余量（股）
        - rzche (float): 融资偿还额(元)
        - rqchl (float): 融券偿还量(股)
        - rqmcl (float): 融券卖出量(股,份,手)
        - rzrqye (float): 融资融券余额(元)
        - ts (.): pro_api
        - pro (.): margin_detail
        - df (=): pro
        """
        pass  # stub

    def margin_secs(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, exchange: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取沪深京三大交易所融资融券标的（包括ETF），每天盘前更新
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): 标的代码
        - name (str): 标的名称
        - exchange (str): 交易所
        """
        pass  # stub

    def moneyflow(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取沪深A股票资金流向数据，分析大单小单成交情况，用于判别资金动向，数据开始于2010年。
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - trade_date (str): 交易日期
        - buy_sm_vol (int): 小单买入量（手）
        - buy_sm_amount (float): 小单买入金额（万元）
        - sell_sm_vol (int): 小单卖出量（手）
        - sell_sm_amount (float): 小单卖出金额（万元）
        - buy_md_vol (int): 中单买入量（手）
        - buy_md_amount (float): 中单买入金额（万元）
        - sell_md_vol (int): 中单卖出量（手）
        - sell_md_amount (float): 中单卖出金额（万元）
        - buy_lg_vol (int): 大单买入量（手）
        - buy_lg_amount (float): 大单买入金额（万元）
        - sell_lg_vol (int): 大单卖出量（手）
        - sell_lg_amount (float): 大单卖出金额（万元）
        - buy_elg_vol (int): 特大单买入量（手）
        - buy_elg_amount (float): 特大单买入金额（万元）
        - sell_elg_vol (int): 特大单卖出量（手）
        - sell_elg_amount (float): 特大单卖出金额（万元）
        - net_mf_vol (int): 净流入量（手）
        - net_mf_amount (float): 净流入额（万元）
        """
        pass  # stub

    def moneyflow_cnt_ths(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取同花顺概念板块每日资金流向
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): 板块代码
        - name (str): 板块名称
        - lead_stock (str): 领涨股票名称
        - close_price (float): 最新价
        - pct_change (float): 行业涨跌幅
        - industry_index (float): 板块指数点位
        - company_num (int): 公司数量
        - pct_change_stock (float): 领涨股涨跌幅
        - net_buy_amount (float): 流入资金(亿元)
        - net_sell_amount (float): 流出资金(亿元)
        - net_amount (float): 净额(亿元)
        """
        pass  # stub

    def moneyflow_dc(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取东方财富个股资金流向数据，每日盘后更新，数据开始于20230911
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): 股票代码
        - name (str): 股票名称
        - pct_change (float): 涨跌幅
        - close (float): 最新价
        - net_amount (float): 今日主力净流入额（万元）
        - net_amount_rate (float): 今日主力净流入净占比（%）
        - buy_elg_amount (float): 今日超大单净流入额（万元）
        - buy_elg_amount_rate (float): 今日超大单净流入占比（%）
        - buy_lg_amount (float): 今日大单净流入额（万元）
        - buy_lg_amount_rate (float): 今日大单净流入占比（%）
        - buy_md_amount (float): 今日中单净流入额（万元）
        - buy_md_amount_rate (float): 今日中单净流入占比（%）
        - buy_sm_amount (float): 今日小单净流入额（万元）
        - buy_sm_amount_rate (float): 今日小单净流入占比（%）
        """
        pass  # stub

    def moneyflow_hsgt(self, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取沪股通、深股通、港股通每日资金流向数据，每次最多返回300条记录，总量不限制。
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ggt_ss (float): 港股通（上海）
        - ggt_sz (float): 港股通（深圳）
        - hgt (float): 沪股通（百万元）
        - sgt (float): 深股通（百万元）
        - north_money (float): 北向资金（百万元）
        - south_money (float): 南向资金（百万元）
        - ts (.): pro_api
        - moneyflow_hsgt ((): start_date
        - end_date (=): '20180808'
        """
        pass  # stub

    def moneyflow_ind_dc(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, content_type: Optional[str] = None):
        """获取东方财富板块资金流向，每天盘后更新
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - content_type (str): 数据类型
        - ts_code (str): DC板块代码（行业、概念、地域）
        - name (str): 板块名称
        - pct_change (float): 板块涨跌幅（%）
        - close (float): 板块最新指数
        - net_amount (float): 今日主力净流入 净额（元）
        - net_amount_rate (float): 今日主力净流入净占比%
        - buy_elg_amount (float): 今日超大单净流入 净额（元）
        - buy_elg_amount_rate (float): 今日超大单净流入 净占比%
        - buy_lg_amount (float): 今日大单净流入 净额（元）
        - buy_lg_amount_rate (float): 今日大单净流入 净占比%
        - buy_md_amount (float): 今日中单净流入 净额（元）
        - buy_md_amount_rate (float): 今日中单净流入 净占比%
        - buy_sm_amount (float): 今日小单净流入 净额（元）
        - buy_sm_amount_rate (float): 今日小单净流入 净占比%
        - buy_sm_amount_stock (str): 今日主力净流入最大股
        - rank (int): 序号
        """
        pass  # stub

    def moneyflow_ind_ths(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取同花顺行业资金流向，每日盘后更新
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): 板块代码
        - industry (str): 板块名称
        - lead_stock (str): 领涨股票名称
        - close (float): 收盘指数
        - pct_change (float): 指数涨跌幅
        - company_num (int): 公司数量
        - pct_change_stock (float): 领涨股涨跌幅
        - close_price (float): 领涨股最新价
        - net_buy_amount (float): 流入资金(亿元)
        - net_sell_amount (float): 流出资金(亿元)
        - net_amount (float): 净额(亿元)
        """
        pass  # stub

    def moneyflow_mkt_dc(self, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取东方财富大盘资金流向数据，每日盘后更新
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - close_sh (float): 上证收盘价（点）
        - pct_change_sh (float): 上证涨跌幅(%)
        - close_sz (float): 深证收盘价（点）
        - pct_change_sz (float): 深证涨跌幅(%)
        - net_amount (float): 今日主力净流入 净额（元）
        - net_amount_rate (float): 今日主力净流入净占比%
        - buy_elg_amount (float): 今日超大单净流入 净额（元）
        - buy_elg_amount_rate (float): 今日超大单净流入 净占比%
        - buy_lg_amount (float): 今日大单净流入 净额（元）
        - buy_lg_amount_rate (float): 今日大单净流入 净占比%
        - buy_md_amount (float): 今日中单净流入 净额（元）
        - buy_md_amount_rate (float): 今日中单净流入 净占比%
        - buy_sm_amount (float): 今日小单净流入 净额（元）
        - buy_sm_amount_rate (float): 今日小单净流入 净占比%
        """
        pass  # stub

    def moneyflow_ths(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取同花顺个股资金流向数据，每日盘后更新
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): 股票代码
        - name (str): 股票名称
        - pct_change (float): 涨跌幅
        - latest (float): 最新价
        - net_amount (float): 资金净流入(万元)
        - net_d5_amount (float): 5日主力净额(万元)
        - buy_lg_amount (float): 今日大单净流入额(万元)
        - buy_lg_amount_rate (float): 今日大单净流入占比(%)
        - buy_md_amount (float): 今日中单净流入额(万元)
        - buy_md_amount_rate (float): 今日中单净流入占比(%)
        - buy_sm_amount (float): 今日小单净流入额(万元)
        - buy_sm_amount_rate (float): 今日小单净流入占比(%)
        """
        pass  # stub

    def monthly(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取A股月线数据
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期
        - close (float): 月收盘价
        - open (float): 月开盘价
        - high (float): 月最高价
        - low (float): 月最低价
        - pre_close (float): 上月收盘价
        - change (float): 月涨跌额
        - pct_chg (float): 月涨跌幅 （未复权，如果是复权请用
        - Y (月成交量): float
        """
        pass  # stub

    def namechange(self, ts_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """历史名称变更记录
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - name (str): 证券名称
        - start_date (str): 开始日期
        - end_date (str): 结束日期
        - ann_date (str): 公告日期
        - change_reason (str): 变更原因
        """
        pass  # stub

    def new_share(self, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取新股上市列表数据
        Args:
        Returns:
        Columns:
        - ts_code (str): TS股票代码
        - sub_code (str): 申购代码
        - name (str): 名称
        - ipo_date (str): 上网发行日期
        - issue_date (str): 上市日期
        - amount (float): 发行总量（万股）
        - market_amount (float): 上网发行总量（万股）
        - price (float): 发行价格
        - pe (float): 市盈率
        - limit_amount (float): 个人申购上限（万股）
        - funds (float): 募集资金（亿元）
        - ballot (float): 中签率
        """
        pass  # stub

    def pledge_detail(self, ts_code: Optional[str] = None, ann_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取股票质押明细数据
        Args:
        Returns:
        Columns:
        - ts_code (str): TS股票代码
        - ann_date (str): 公告日期
        - holder_name (str): 股东名称
        - pledge_amount (float): 质押数量（万股）
        - start_date (str): 质押开始日期
        - end_date (str): 质押结束日期
        - is_release (str): 是否已解押
        - release_date (str): 解押日期
        - pledgor (str): 质押方
        - holding_amount (float): 持股总数（万股）
        - pledged_amount (float): 质押总数（万股）
        - p_total_ratio (float): 本次质押占总股本比例
        - h_total_ratio (float): 持股总数占总股本比例
        - is_buyback (str): 是否回购（0否 1是）
        - df (=): .
        - query ((): ,
        """
        pass  # stub

    def pledge_stat(self, ts_code: Optional[str] = None, end_date: Optional[str] = None):
        """获取股票质押统计数据
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - end_date (str): 截止日期
        - pledge_count (int): 质押次数
        - unrest_pledge (float): 无限售股质押数量（万）
        - rest_pledge (float): 限售股份质押数量（万）
        - total_share (float): 总股本
        - pledge_ratio (float): 质押比例
        - df (=): .
        - query ((): ,
        """
        pass  # stub

    def report_rc(self, ts_code: Optional[str] = None, report_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取券商（卖方）每天研报的盈利预测数据，数据从2010年开始，每晚19~22点更新当日数据
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - name (str): 股票名称
        - report_date (str): 研报日期
        - report_title (str): 报告标题
        - report_type (str): 报告类型
        - classify (str): 报告分类
        - org_name (str): 机构名称
        - author_name (str): 作者
        - quarter (str): 预测报告期
        - op_rt (float): 预测营业收入（万元）
        - op_pr (float): 预测营业利润（万元）
        - tp (float): 预测利润总额（万元）
        - np (float): 预测净利润（万元）
        - eps (float): 预测每股收益（元）
        - pe (float): 预测市盈率
        - rd (float): 预测股息率
        - roe (float): 预测净资产收益率
        - ev_ebitda (float): 预测EV/EBITDA
        - rating (str): 卖方评级
        - max_price (float): 预测最高目标价
        - min_price (float): 预测最低目标价
        - imp_dg (str): 机构关注度
        - create_time (datetime): TS数据更新时间
        """
        pass  # stub

    def repurchase(self, ann_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取上市公司回购股票数据
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - ann_date (str): 公告日期
        - end_date (str): 截止日期
        - proc (str): 进度
        - exp_date (str): 过期日期
        - vol (float): 回购数量
        - amount (float): 回购金额
        - high_limit (float): 回购最高价
        - low_limit (float): 回购最低价
        """
        pass  # stub

    def rt_k(self, ts_code: Optional[str] = None):
        """获取实时日k线行情，支持按股票代码及股票代码通配符一次性提取全部股票实时日k线行情
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - name (None): 股票名称
        - pre_close (float): 昨收价
        - high (float): 最高价
        - open (float): 开盘价
        - low (float): 最低价
        - close (float): 收盘价（最新价）
        - vol (int): 成交量（股）
        - amount (int): 成交金额（元）
        - num (int): 开盘以来成交笔数
        - ask_price1 (float): 委托卖盘（元）
        - ask_volume1 (int): 委托卖盘（股）
        - bid_price1 (float): 委托买盘（元）
        - bid_volume1 (int): 委托买盘（股）
        - trade_time (str): 交易时间
        """
        pass  # stub

    def rt_min(self, freq: Optional[str] = None, ts_code: Optional[str] = None):
        """获取全A股票实时分钟数据，包括1~60min
        Args:
        Returns:
        Columns:
        - code (str): 股票代码
        - time (None): 交易时间
        - open (float): 开盘价
        - close (float): 收盘价
        - high (float): 最高价
        - low (float): 最低价
        - vol (float): 成交量(股）
        - amount (float): 成交额（元）
        - pro (=):
        - df (=): freq='1MIN')
        """
        pass  # stub

    def rt_min_daily(self, freq: Optional[str] = None, ts_code: Optional[str] = None):
        """获取A股当日盘中历史分钟数据，可以提取单只股票当日开盘以来的所有分钟数据
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - freq (None): 频次
        - time (None): 交易时间
        - open (float): 开盘价
        - close (float): 收盘价
        - high (float): 最高价
        - low (float): 最低价
        - vol (float): 成交量(股）
        - amount (float): 成交额（元）
        - import (tushare): ts
        - pro (=):
        - df (=): ts_code="600000.SH")
        - code (freq): open close high low vol amount
        """
        pass  # stub

    def share_float(self, ts_code: Optional[str] = None, ann_date: Optional[str] = None, float_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取限售股解禁
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - ann_date (str): 公告日期
        - float_date (str): 解禁日期
        - float_share (float): 流通股份(股)
        - float_ratio (float): 流通股份占总股本比率
        - holder_name (str): 股东名称
        - share_type (str): 股份类型
        """
        pass  # stub

    def slb_len(self, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """转融通融资汇总
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ob (float): 期初余额(亿元)
        - auc_amount (float): 竞价成交金额(亿元)
        - repo_amount (float): 再借成交金额(亿元)
        - repay_amount (float): 偿还金额(亿元)
        - cb (float): 期末余额(亿元)
        """
        pass  # stub

    def slb_len_mm(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """做市借券交易汇总
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期（YYYYMMDD）
        - ts_code (str): 股票代码
        - name (str): 股票名称
        - ope_inv (float): 期初余量(万股)
        - lent_qnt (float): 融出数量(万股)
        - cls_inv (float): 期末余量(万股)
        - end_bal (float): 期末余额(万元)
        """
        pass  # stub

    def slb_sec(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """转融通转融券交易汇总
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期（YYYYMMDD）
        - ts_code (str): 股票代码
        - name (str): 股票名称
        - ope_inv (float): 期初余量(万股)
        - lent_qnt (float): 转融券融出数量(万股)
        - cls_inv (float): 期末余量(万股)
        - end_bal (float): 期末余额(万元)
        """
        pass  # stub

    def slb_sec_detail(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """转融券交易明细
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期（YYYYMMDD）
        - ts_code (str): 股票代码
        - name (str): 股票名称
        - tenor (str): 期 限(天)
        - fee_rate (float): 融出费率(%)
        - lent_qnt (float): 转融券融出数量(万股)
        """
        pass  # stub

    def st(self, ts_code: Optional[str] = None, pub_date: Optional[str] = None, imp_date: Optional[str] = None):
        """ST风险警示板股票列表
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - name (str): 股票名称
        - pub_date (str): 发布日期
        - imp_date (str): 实施日期
        - st_tpye (str): 类型
        - st_reason (str): st变更原因
        - st_explain (str): st变更详细原因
        - df (=): "ts_code": "300125.SZ", "pub_date": "", "imp_date": "" }, fi
        """
        pass  # stub

    def stk_account(self, date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取股票账户开户数据，统计周期为一周
        Args:
        Returns:
        Columns:
        - date (str): 统计周期
        - weekly_new (float): 本周新增（万）
        - total (float): 期末总账户数（万）
        - weekly_hold (float): 本周持仓账户数（万）
        - weekly_trade (float): 本周参与交易账户数（万）
        """
        pass  # stub

    def stk_account_old(self, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取股票账户开户数据旧版格式数据，数据从2008年1月开始，到2015年5月29，新数据请通过
        Args:
        Returns:
        Columns:
        - date (str): 统计周期
        - new_sh (int): 本周新增（上海，户）
        - new_sz (int): 本周新增（深圳，户）
        - active_sh (float): 期末有效账户（上海，万户）
        - active_sz (float): 期末有效账户（深圳，万户）
        - total_sh (float): 期末账户数（上海，万户）
        - total_sz (float): 期末账户数（深圳，万户）
        - trade_sh (float): 参与交易账户数（上海，万户）
        - trade_sz (float): 参与交易账户数（深圳，万户）
        """
        pass  # stub

    def stk_ah_comparison(self, hk_code: Optional[str] = None, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """AH股比价数据，可根据交易日期获取历史
        Args:
        Returns:
        Columns:
        - hk_code (str): 港股股票代码
        - ts_code (str): A股股票代码
        - trade_date (str): 交易日期
        - hk_name (str): 港股股票名称
        - hk_pct_chg (float): 港股股票涨跌幅
        - hk_close (float): 港股股票收盘价
        - name (str): A股股票名称
        - close (float): A股股票收盘价
        - pct_chg (float): A股股票涨跌幅
        - ah_comparison (float): 比价(A/H)
        - ah_premium (float): 溢价(A/H)%
        """
        pass  # stub

    def stk_alert(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """根据证券交易所交易规则的有关规定，交易所每日发布重点提示证券
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - name (str): 股票名称
        - start_date (str): 交易所重点提示起始日期
        - end_date (str): 交易所重点提示参考截至日期
        - type (str): 提示类型
        - as (ts): ts
        - ts (.): ()
        - df (=): .
        - stk_alert ((): =
        """
        pass  # stub

    def stk_auction(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取当日个股和ETF的集合竞价成交情况，每天9点26~29分之间可以获取当日的集合竞价成交数据
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 数据日期
        - vol (int): 成交量（股）
        - price (int): 成交均价（元）
        - amount (float): 成交金额（元）
        - pre_close (float): 昨收价（元）
        - turnover_rate (float): 换手率（%）
        - volume_ratio (float): 量比
        - float_share (float): 流通股本（万股）
        """
        pass  # stub

    def stk_auction_c(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """股票收盘15:00集合竞价数据，每天盘后更新
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期
        - close (float): 收盘集合竞价收盘价
        - open (float): 收盘集合竞价开盘价
        - high (float): 收盘集合竞价最高价
        - low (float): 收盘集合竞价最低价
        - vol (float): 收盘集合竞价成交量
        - amount (float): 收盘集合竞价成交额
        - vwap (float): 收盘集合竞价均价
        """
        pass  # stub

    def stk_auction_o(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """股票开盘9:30集合竞价数据，每天盘后更新
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期
        - close (float): 开盘集合竞价收盘价
        - open (float): 开盘集合竞价开盘价
        - high (float): 开盘集合竞价最高价
        - low (float): 开盘集合竞价最低价
        - vol (float): 开盘集合竞价成交量
        - amount (float): 开盘集合竞价成交额
        - vwap (float): 开盘集合竞价均价
        """
        pass  # stub

    def stk_factor(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取股票每日技术面因子数据，用于跟踪股票当前走势情况，数据由Tushare社区自产，覆盖全历史
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期
        - close (float): 收盘价
        - open (float): 开盘价
        - high (float): 最高价
        - low (float): 最低价
        - pre_close (float): 昨收价
        - change (float): 涨跌额
        - pct_change (float): 涨跌幅
        - vol (float): 成交量 （手）
        - amount (float): 成交额 （千元）
        - adj_factor (float): 复权因子
        - open_hfq (float): 开盘价后复权
        - open_qfq (float): 开盘价前复权
        - close_hfq (float): 收盘价后复权
        - close_qfq (float): 收盘价前复权
        - high_hfq (float): 最高价后复权
        - high_qfq (float): 最高价前复权
        - low_hfq (float): 最低价后复权
        - low_qfq (float): 最低价前复权
        - pre_close_hfq (float): 昨收价后复权
        - pre_close_qfq (float): 昨收价前复权
        - macd_dif (float): MACD_DIF (基于前复权价格计算，下同)
        - macd_dea (float): MACD_DEA
        - macd (float): MACD
        - kdj_k (float): KDJ_K
        - kdj_d (float): KDJ_D
        - kdj_j (float): KDJ_J
        - rsi_6 (float): RSI_6
        - rsi_12 (float): RSI_12
        - rsi_24 (float): RSI_24
        - boll_upper (float): BOLL_UPPER
        - boll_mid (float): BOLL_MID
        - boll_lower (float): BOLL_LOWER
        - cci (float): CCI
        """
        pass  # stub

    def stk_factor_pro(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取股票每日技术面因子数据，用于跟踪股票当前走势情况，数据由Tushare社区自产，覆盖全历史；输出参数_bfq表示不复权，_qfq表示前复权 _hfq表示后复权，描述中说明了因子的默认传参，如需要特殊参数或者更多因子可以联系管理员评估
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期
        - open (float): 开盘价
        - open_hfq (float): 开盘价（后复权）
        - open_qfq (float): 开盘价（前复权）
        - high (float): 最高价
        - high_hfq (float): 最高价（后复权）
        - high_qfq (float): 最高价（前复权）
        - low (float): 最低价
        - low_hfq (float): 最低价（后复权）
        - low_qfq (float): 最低价（前复权）
        - close (float): 收盘价
        - close_hfq (float): 收盘价（后复权）
        - close_qfq (float): 收盘价（前复权）
        - pre_close (float): 昨收价(前复权)--为daily接口的pre_close,以当时复权因子计算值跟前一日close_qfq对不上，可不用
        - change (float): 涨跌额
        - pct_chg (float): 涨跌幅 （除权后的涨跌幅）
        - vol (float): 成交量 （手）
        - amount (float): 成交额 （千元）
        - turnover_rate (float): 换手率（%）
        - turnover_rate_f (float): 换手率（自由流通股）
        - volume_ratio (float): 量比
        - pe (float): 市盈率（总市值/净利润， 亏损的PE为空）
        - pe_ttm (float): 市盈率（TTM，亏损的PE为空）
        - pb (float): 市净率（总市值/净资产）
        - ps (float): 市销率
        - ps_ttm (float): 市销率（TTM）
        - dv_ratio (float): 股息率 （%）
        - dv_ttm (float): 股息率（TTM）（%）
        - total_share (float): 总股本 （万股）
        - float_share (float): 流通股本 （万股）
        - free_share (float): 自由流通股本 （万）
        - total_mv (float): 总市值 （万元）
        - circ_mv (float): 流通市值（万元）
        - adj_factor (float): 复权因子
        - asi_bfq (float): 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
        - asi_hfq (float): 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
        - asi_qfq (float): 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
        - asit_bfq (float): 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
        - asit_hfq (float): 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
        - asit_qfq (float): 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
        - atr_bfq (float): 真实波动N日平均值-CLOSE, HIGH, LOW, N=20
        - atr_hfq (float): 真实波动N日平均值-CLOSE, HIGH, LOW, N=20
        - atr_qfq (float): 真实波动N日平均值-CLOSE, HIGH, LOW, N=20
        - bbi_bfq (float): BBI多空指标-CLOSE, M1=3, M2=6, M3=12, M4=20
        - bbi_hfq (float): BBI多空指标-CLOSE, M1=3, M2=6, M3=12, M4=21
        - bbi_qfq (float): BBI多空指标-CLOSE, M1=3, M2=6, M3=12, M4=22
        - bias1_bfq (float): BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
        - bias1_hfq (float): BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
        - bias1_qfq (float): BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
        - bias2_bfq (float): BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
        - bias2_hfq (float): BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
        - bias2_qfq (float): BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
        - bias3_bfq (float): BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
        - bias3_hfq (float): BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
        - bias3_qfq (float): BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
        - boll_lower_bfq (float): BOLL指标，布林带-CLOSE, N=20, P=2
        - boll_lower_hfq (float): BOLL指标，布林带-CLOSE, N=20, P=2
        - boll_lower_qfq (float): BOLL指标，布林带-CLOSE, N=20, P=2
        - boll_mid_bfq (float): BOLL指标，布林带-CLOSE, N=20, P=2
        - boll_mid_hfq (float): BOLL指标，布林带-CLOSE, N=20, P=2
        - boll_mid_qfq (float): BOLL指标，布林带-CLOSE, N=20, P=2
        - boll_upper_bfq (float): BOLL指标，布林带-CLOSE, N=20, P=2
        - boll_upper_hfq (float): BOLL指标，布林带-CLOSE, N=20, P=2
        - boll_upper_qfq (float): BOLL指标，布林带-CLOSE, N=20, P=2
        - brar_ar_bfq (float): BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
        - brar_ar_hfq (float): BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
        - brar_ar_qfq (float): BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
        - brar_br_bfq (float): BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
        - brar_br_hfq (float): BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
        - brar_br_qfq (float): BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
        - cci_bfq (float): 顺势指标又叫CCI指标-CLOSE, HIGH, LOW, N=14
        - cci_hfq (float): 顺势指标又叫CCI指标-CLOSE, HIGH, LOW, N=14
        - cci_qfq (float): 顺势指标又叫CCI指标-CLOSE, HIGH, LOW, N=14
        - cr_bfq (float): CR价格动量指标-CLOSE, HIGH, LOW, N=20
        - cr_hfq (float): CR价格动量指标-CLOSE, HIGH, LOW, N=20
        - cr_qfq (float): CR价格动量指标-CLOSE, HIGH, LOW, N=20
        - dfma_dif_bfq (float): 平行线差指标-CLOSE, N1=10, N2=50, M=10
        - dfma_dif_hfq (float): 平行线差指标-CLOSE, N1=10, N2=50, M=10
        - dfma_dif_qfq (float): 平行线差指标-CLOSE, N1=10, N2=50, M=10
        - dfma_difma_bfq (float): 平行线差指标-CLOSE, N1=10, N2=50, M=10
        - dfma_difma_hfq (float): 平行线差指标-CLOSE, N1=10, N2=50, M=10
        - dfma_difma_qfq (float): 平行线差指标-CLOSE, N1=10, N2=50, M=10
        - dmi_adx_bfq (float): 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
        - dmi_adx_hfq (float): 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
        - dmi_adx_qfq (float): 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
        - dmi_adxr_bfq (float): 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
        - dmi_adxr_hfq (float): 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
        - dmi_adxr_qfq (float): 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
        - dmi_mdi_bfq (float): 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
        - dmi_mdi_hfq (float): 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
        - dmi_mdi_qfq (float): 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
        - dmi_pdi_bfq (float): 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
        - dmi_pdi_hfq (float): 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
        - dmi_pdi_qfq (float): 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
        - downdays (float): 连跌天数
        - updays (float): 连涨天数
        - dpo_bfq (float): 区间震荡线-CLOSE, M1=20, M2=10, M3=6
        - dpo_hfq (float): 区间震荡线-CLOSE, M1=20, M2=10, M3=6
        - dpo_qfq (float): 区间震荡线-CLOSE, M1=20, M2=10, M3=6
        - madpo_bfq (float): 区间震荡线-CLOSE, M1=20, M2=10, M3=6
        - madpo_hfq (float): 区间震荡线-CLOSE, M1=20, M2=10, M3=6
        - madpo_qfq (float): 区间震荡线-CLOSE, M1=20, M2=10, M3=6
        - ema_bfq_10 (float): 指数移动平均-N=10
        - ema_bfq_20 (float): 指数移动平均-N=20
        - ema_bfq_250 (float): 指数移动平均-N=250
        - ema_bfq_30 (float): 指数移动平均-N=30
        - ema_bfq_5 (float): 指数移动平均-N=5
        - ema_bfq_60 (float): 指数移动平均-N=60
        - ema_bfq_90 (float): 指数移动平均-N=90
        - ema_hfq_10 (float): 指数移动平均-N=10
        - ema_hfq_20 (float): 指数移动平均-N=20
        - ema_hfq_250 (float): 指数移动平均-N=250
        - ema_hfq_30 (float): 指数移动平均-N=30
        - ema_hfq_5 (float): 指数移动平均-N=5
        - ema_hfq_60 (float): 指数移动平均-N=60
        - ema_hfq_90 (float): 指数移动平均-N=90
        - ema_qfq_10 (float): 指数移动平均-N=10
        - ema_qfq_20 (float): 指数移动平均-N=20
        - ema_qfq_250 (float): 指数移动平均-N=250
        - ema_qfq_30 (float): 指数移动平均-N=30
        - ema_qfq_5 (float): 指数移动平均-N=5
        - ema_qfq_60 (float): 指数移动平均-N=60
        - ema_qfq_90 (float): 指数移动平均-N=90
        - emv_bfq (float): 简易波动指标-HIGH, LOW, VOL, N=14, M=9
        - emv_hfq (float): 简易波动指标-HIGH, LOW, VOL, N=14, M=9
        - emv_qfq (float): 简易波动指标-HIGH, LOW, VOL, N=14, M=9
        - maemv_bfq (float): 简易波动指标-HIGH, LOW, VOL, N=14, M=9
        - maemv_hfq (float): 简易波动指标-HIGH, LOW, VOL, N=14, M=9
        - maemv_qfq (float): 简易波动指标-HIGH, LOW, VOL, N=14, M=9
        - expma_12_bfq (float): EMA指数平均数指标-CLOSE, N1=12, N2=50
        - expma_12_hfq (float): EMA指数平均数指标-CLOSE, N1=12, N2=50
        - expma_12_qfq (float): EMA指数平均数指标-CLOSE, N1=12, N2=50
        - expma_50_bfq (float): EMA指数平均数指标-CLOSE, N1=12, N2=50
        - expma_50_hfq (float): EMA指数平均数指标-CLOSE, N1=12, N2=50
        - expma_50_qfq (float): EMA指数平均数指标-CLOSE, N1=12, N2=50
        - kdj_bfq (float): KDJ指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
        - kdj_hfq (float): KDJ指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
        - kdj_qfq (float): KDJ指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
        - kdj_d_bfq (float): KDJ指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
        - kdj_d_hfq (float): KDJ指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
        - kdj_d_qfq (float): KDJ指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
        - kdj_k_bfq (float): KDJ指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
        - kdj_k_hfq (float): KDJ指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
        - kdj_k_qfq (float): KDJ指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
        - ktn_down_bfq (float): 肯特纳交易通道, N选20日，ATR选10日-CLOSE, HIGH, LOW, N=20, M=10
        - ktn_down_hfq (float): 肯特纳交易通道, N选20日，ATR选10日-CLOSE, HIGH, LOW, N=20, M=10
        - ktn_down_qfq (float): 肯特纳交易通道, N选20日，ATR选10日-CLOSE, HIGH, LOW, N=20, M=10
        - ktn_mid_bfq (float): 肯特纳交易通道, N选20日，ATR选10日-CLOSE, HIGH, LOW, N=20, M=10
        - ktn_mid_hfq (float): 肯特纳交易通道, N选20日，ATR选10日-CLOSE, HIGH, LOW, N=20, M=10
        - ktn_mid_qfq (float): 肯特纳交易通道, N选20日，ATR选10日-CLOSE, HIGH, LOW, N=20, M=10
        - ktn_upper_bfq (float): 肯特纳交易通道, N选20日，ATR选10日-CLOSE, HIGH, LOW, N=20, M=10
        - ktn_upper_hfq (float): 肯特纳交易通道, N选20日，ATR选10日-CLOSE, HIGH, LOW, N=20, M=10
        - ktn_upper_qfq (float): 肯特纳交易通道, N选20日，ATR选10日-CLOSE, HIGH, LOW, N=20, M=10
        - lowdays (float): LOWRANGE(LOW)表示当前最低价是近多少周期内最低价的最小值
        - topdays (float): TOPRANGE(HIGH)表示当前最高价是近多少周期内最高价的最大值
        - ma_bfq_10 (float): 简单移动平均-N=10
        - ma_bfq_20 (float): 简单移动平均-N=20
        - ma_bfq_250 (float): 简单移动平均-N=250
        - ma_bfq_30 (float): 简单移动平均-N=30
        - ma_bfq_5 (float): 简单移动平均-N=5
        - ma_bfq_60 (float): 简单移动平均-N=60
        - ma_bfq_90 (float): 简单移动平均-N=90
        - ma_hfq_10 (float): 简单移动平均-N=10
        - ma_hfq_20 (float): 简单移动平均-N=20
        - ma_hfq_250 (float): 简单移动平均-N=250
        - ma_hfq_30 (float): 简单移动平均-N=30
        - ma_hfq_5 (float): 简单移动平均-N=5
        - ma_hfq_60 (float): 简单移动平均-N=60
        - ma_hfq_90 (float): 简单移动平均-N=90
        - ma_qfq_10 (float): 简单移动平均-N=10
        - ma_qfq_20 (float): 简单移动平均-N=20
        - ma_qfq_250 (float): 简单移动平均-N=250
        - ma_qfq_30 (float): 简单移动平均-N=30
        - ma_qfq_5 (float): 简单移动平均-N=5
        - ma_qfq_60 (float): 简单移动平均-N=60
        - ma_qfq_90 (float): 简单移动平均-N=90
        - macd_bfq (float): MACD指标-CLOSE, SHORT=12, LONG=26, M=9
        - macd_hfq (float): MACD指标-CLOSE, SHORT=12, LONG=26, M=9
        - macd_qfq (float): MACD指标-CLOSE, SHORT=12, LONG=26, M=9
        - macd_dea_bfq (float): MACD指标-CLOSE, SHORT=12, LONG=26, M=9
        - macd_dea_hfq (float): MACD指标-CLOSE, SHORT=12, LONG=26, M=9
        - macd_dea_qfq (float): MACD指标-CLOSE, SHORT=12, LONG=26, M=9
        - macd_dif_bfq (float): MACD指标-CLOSE, SHORT=12, LONG=26, M=9
        - macd_dif_hfq (float): MACD指标-CLOSE, SHORT=12, LONG=26, M=9
        - macd_dif_qfq (float): MACD指标-CLOSE, SHORT=12, LONG=26, M=9
        - mass_bfq (float): 梅斯线-HIGH, LOW, N1=9, N2=25, M=6
        - mass_hfq (float): 梅斯线-HIGH, LOW, N1=9, N2=25, M=6
        - mass_qfq (float): 梅斯线-HIGH, LOW, N1=9, N2=25, M=6
        - ma_mass_bfq (float): 梅斯线-HIGH, LOW, N1=9, N2=25, M=6
        - ma_mass_hfq (float): 梅斯线-HIGH, LOW, N1=9, N2=25, M=6
        - ma_mass_qfq (float): 梅斯线-HIGH, LOW, N1=9, N2=25, M=6
        - mfi_bfq (float): MFI指标是成交量的RSI指标-CLOSE, HIGH, LOW, VOL, N=14
        - mfi_hfq (float): MFI指标是成交量的RSI指标-CLOSE, HIGH, LOW, VOL, N=14
        - mfi_qfq (float): MFI指标是成交量的RSI指标-CLOSE, HIGH, LOW, VOL, N=14
        - mtm_bfq (float): 动量指标-CLOSE, N=12, M=6
        - mtm_hfq (float): 动量指标-CLOSE, N=12, M=6
        - mtm_qfq (float): 动量指标-CLOSE, N=12, M=6
        - mtmma_bfq (float): 动量指标-CLOSE, N=12, M=6
        - mtmma_hfq (float): 动量指标-CLOSE, N=12, M=6
        - mtmma_qfq (float): 动量指标-CLOSE, N=12, M=6
        - obv_bfq (float): 能量潮指标-CLOSE, VOL
        - obv_hfq (float): 能量潮指标-CLOSE, VOL
        - obv_qfq (float): 能量潮指标-CLOSE, VOL
        - psy_bfq (float): 投资者对股市涨跌产生心理波动的情绪指标-CLOSE, N=12, M=6
        - psy_hfq (float): 投资者对股市涨跌产生心理波动的情绪指标-CLOSE, N=12, M=6
        - psy_qfq (float): 投资者对股市涨跌产生心理波动的情绪指标-CLOSE, N=12, M=6
        - psyma_bfq (float): 投资者对股市涨跌产生心理波动的情绪指标-CLOSE, N=12, M=6
        - psyma_hfq (float): 投资者对股市涨跌产生心理波动的情绪指标-CLOSE, N=12, M=6
        - psyma_qfq (float): 投资者对股市涨跌产生心理波动的情绪指标-CLOSE, N=12, M=6
        - roc_bfq (float): 变动率指标-CLOSE, N=12, M=6
        - roc_hfq (float): 变动率指标-CLOSE, N=12, M=6
        - roc_qfq (float): 变动率指标-CLOSE, N=12, M=6
        - maroc_bfq (float): 变动率指标-CLOSE, N=12, M=6
        - maroc_hfq (float): 变动率指标-CLOSE, N=12, M=6
        - maroc_qfq (float): 变动率指标-CLOSE, N=12, M=6
        - rsi_bfq_12 (float): RSI指标-CLOSE, N=12
        - rsi_bfq_24 (float): RSI指标-CLOSE, N=24
        - rsi_bfq_6 (float): RSI指标-CLOSE, N=6
        - rsi_hfq_12 (float): RSI指标-CLOSE, N=12
        - rsi_hfq_24 (float): RSI指标-CLOSE, N=24
        - rsi_hfq_6 (float): RSI指标-CLOSE, N=6
        - rsi_qfq_12 (float): RSI指标-CLOSE, N=12
        - rsi_qfq_24 (float): RSI指标-CLOSE, N=24
        - rsi_qfq_6 (float): RSI指标-CLOSE, N=6
        - taq_down_bfq (float): 唐安奇通道(海龟)交易指标-HIGH, LOW, 20
        - taq_down_hfq (float): 唐安奇通道(海龟)交易指标-HIGH, LOW, 20
        - taq_down_qfq (float): 唐安奇通道(海龟)交易指标-HIGH, LOW, 20
        - taq_mid_bfq (float): 唐安奇通道(海龟)交易指标-HIGH, LOW, 20
        - taq_mid_hfq (float): 唐安奇通道(海龟)交易指标-HIGH, LOW, 20
        - taq_mid_qfq (float): 唐安奇通道(海龟)交易指标-HIGH, LOW, 20
        - taq_up_bfq (float): 唐安奇通道(海龟)交易指标-HIGH, LOW, 20
        - taq_up_hfq (float): 唐安奇通道(海龟)交易指标-HIGH, LOW, 20
        - taq_up_qfq (float): 唐安奇通道(海龟)交易指标-HIGH, LOW, 20
        - trix_bfq (float): 三重指数平滑平均线-CLOSE, M1=12, M2=20
        - trix_hfq (float): 三重指数平滑平均线-CLOSE, M1=12, M2=20
        - trix_qfq (float): 三重指数平滑平均线-CLOSE, M1=12, M2=20
        - trma_bfq (float): 三重指数平滑平均线-CLOSE, M1=12, M2=20
        - trma_hfq (float): 三重指数平滑平均线-CLOSE, M1=12, M2=20
        - trma_qfq (float): 三重指数平滑平均线-CLOSE, M1=12, M2=20
        - vr_bfq (float): VR容量比率-CLOSE, VOL, M1=26
        - vr_hfq (float): VR容量比率-CLOSE, VOL, M1=26
        - vr_qfq (float): VR容量比率-CLOSE, VOL, M1=26
        - wr_bfq (float): W&R 威廉指标-CLOSE, HIGH, LOW, N=10, N1=6
        - wr_hfq (float): W&R 威廉指标-CLOSE, HIGH, LOW, N=10, N1=6
        - wr_qfq (float): W&R 威廉指标-CLOSE, HIGH, LOW, N=10, N1=6
        - wr1_bfq (float): W&R 威廉指标-CLOSE, HIGH, LOW, N=10, N1=6
        - wr1_hfq (float): W&R 威廉指标-CLOSE, HIGH, LOW, N=10, N1=6
        - wr1_qfq (float): W&R 威廉指标-CLOSE, HIGH, LOW, N=10, N1=6
        - xsii_td1_bfq (float): 薛斯通道II-CLOSE, HIGH, LOW, N=102, M=7
        - xsii_td1_hfq (float): 薛斯通道II-CLOSE, HIGH, LOW, N=102, M=7
        - xsii_td1_qfq (float): 薛斯通道II-CLOSE, HIGH, LOW, N=102, M=7
        - xsii_td2_bfq (float): 薛斯通道II-CLOSE, HIGH, LOW, N=102, M=7
        - xsii_td2_hfq (float): 薛斯通道II-CLOSE, HIGH, LOW, N=102, M=7
        - xsii_td2_qfq (float): 薛斯通道II-CLOSE, HIGH, LOW, N=102, M=7
        - xsii_td3_bfq (float): 薛斯通道II-CLOSE, HIGH, LOW, N=102, M=7
        - xsii_td3_hfq (float): 薛斯通道II-CLOSE, HIGH, LOW, N=102, M=7
        - xsii_td3_qfq (float): 薛斯通道II-CLOSE, HIGH, LOW, N=102, M=7
        - xsii_td4_bfq (float): 薛斯通道II-CLOSE, HIGH, LOW, N=102, M=7
        - xsii_td4_hfq (float): 薛斯通道II-CLOSE, HIGH, LOW, N=102, M=7
        - xsii_td4_qfq (float): 薛斯通道II-CLOSE, HIGH, LOW, N=102, M=7
        - df (=): .
        - stk_factor_pro ((): =
        """
        pass  # stub

    def stk_high_shock(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """根据证券交易所交易规则的有关规定，交易所每日发布股票交易严重异常波动情况
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 公告日期
        - name (str): 股票名称
        - trade_market (str): 交易所
        - reason (str): 异常
        """
        pass  # stub

    def stk_holdernumber(self, ts_code: Optional[str] = None, ann_date: Optional[str] = None, enddate: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取上市公司股东户数数据，数据不定期公布
        Args:
        Returns:
        Columns:
        - ts_code (str): TS股票代码
        - ann_date (str): 公告日期
        - end_date (str): 截止日期
        - holder_num (int): 股东户数
        """
        pass  # stub

    def stk_holdertrade(self, ts_code: Optional[str] = None, ann_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, trade_type: Optional[str] = None, holder_type: Optional[str] = None):
        """获取上市公司增减持数据，了解重要股东近期及历史上的股份增减变化
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - ann_date (str): 公告日期
        - holder_name (str): 股东名称
        - holder_type (str): 股东类型G高管P个人C公司
        - in_de (str): 类型IN增持DE减持
        - change_vol (float): 变动数量
        - change_ratio (float): 占流通比例（%）
        - after_share (float): 变动后持股
        - after_ratio (float): 变动后占流通比例（%）
        - avg_price (float): 平均价格
        - total_share (float): 持股总数
        - begin_date (str): 增减持开始日期
        - close_date (str): 增减持结束日期
        """
        pass  # stub

    def stk_limit(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取全市场（包含A/B股和基金）每日涨跌停价格，包括涨停价格，跌停价格等，每个交易日8点40左右更新当日股票涨跌停价格。
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): TS股票代码
        - pre_close (float): 昨日收盘价
        - up_limit (float): 涨停价
        - down_limit (float): 跌停价
        """
        pass  # stub

    def stk_managers(self, ts_code: Optional[str] = None, ann_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取上市公司管理层
        Args:
        Returns:
        Columns:
        - ts_code (str): TS股票代码
        - ann_date (str): 公告日期
        - name (str): 姓名
        - gender (str): 性别
        - lev (str): 岗位类别
        - title (str): 岗位
        - edu (str): 学历
        - national (str): 国籍
        - birthday (str): 出生年月
        - begin_date (str): 上任日期
        - end_date (str): 离任日期
        - resume (str): 个人简历
        - pro (=):
        - df (=):
        """
        pass  # stub

    def stk_mins(self, ts_code: Optional[str] = None, freq: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取A股分钟数据，支持1min/5min/15min/30min/60min行情
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_time (str): 交易时间
        - open (float): 开盘价
        - close (float): 收盘价
        - high (float): 最高价
        - low (float): 最低价
        - vol (int): 成交量(股)
        - amount (float): 成交金额（元）
        - pro (=):
        - df (=): freq='1min', start_date='2023-08-25 09:00:00', end_date='202
        """
        pass  # stub

    def stk_nineturn(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, freq: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """神奇九转（又称“九转序列”）是一种基于技术分析的股票趋势反转指标，其思想来源于技术分析大师汤姆·迪马克（Tom DeMark）的TD序列。该指标的核心功能是通过识别股价在上涨或下跌过程中连续9天的特定走势，来判断股价的潜在反转点，从而帮助投资者提高抄底和逃顶的成功率，日线级别配合60min的九转效果更好，数据从20230101开始。
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (datetime): 交易日期
        - freq (str): 频率(日daily)
        - open (float): 开盘价
        - high (float): 最高价
        - low (float): 最低价
        - close (float): 收盘价
        - vol (float): 成交量
        - amount (float): 成交额
        - up_count (float): 上九转计数
        - down_count (float): 下九转计数
        - nine_up_turn (str): 是否上九转)+9表示上九转
        - nine_down_turn (str): 是否下九转-9表示下九转
        """
        pass  # stub

    def stk_premarket(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """每日开盘前获取当日股票的股本情况，包括总股本和流通股本，涨跌停价格等。
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): TS股票代码
        - total_share (float): 总股本（万股）
        - float_share (float): 流通股本（万股）
        - pre_close (float): 昨日收盘价
        - up_limit (float): 今日涨停价
        - down_limit (float): 今日跌停价
        """
        pass  # stub

    def stk_rewards(self, ts_code: Optional[str] = None, end_date: Optional[str] = None):
        """获取上市公司管理层薪酬和持股
        Args:
        Returns:
        Columns:
        - ts_code (str): TS股票代码
        - ann_date (str): 公告日期
        - end_date (str): 截止日期
        - name (str): 姓名
        - title (str): 职务
        - reward (float): 报酬
        - hold_vol (float): 持股数
        - pro (=):
        - df (=):
        """
        pass  # stub

    def stk_shock(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """根据证券交易所交易规则的有关规定，交易所每日发布股票交易异常波动情况
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 公告日期
        - name (str): 股票名称
        - trade_market (str): 交易所
        - reason (str): 异常
        """
        pass  # stub

    def stk_surv(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取上市公司机构调研记录数据
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - name (str): 股票名称
        - surv_date (str): 调研日期
        - fund_visitors (str): 机构参与人员
        - rece_place (str): 接待地点
        - rece_mode (str): 接待方式
        - rece_org (str): 接待的公司
        - org_type (str): 接待公司类型
        - comp_rece (str): 上市公司接待人员
        - content (None): 调研内容
        """
        pass  # stub

    def stk_week_month_adj(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, freq: Optional[str] = None):
        """周月线复权行情数据
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期（每周五或者月末日期）
        - end_date (str): 计算截至日期
        - freq (str): 频率(周week,月month)
        - open (float): (周/月)开盘价
        - high (float): (周/月)最高价
        - low (float): (周/月)最低价
        - close (float): (周/月)收盘价
        - pre_close (float): 上一(周/月)收盘价【除权价，前复权】
        - open_qfq (float): 前复权(周/月)开盘价
        - high_qfq (float): 前复权(周/月)最高价
        - low_qfq (float): 前复权(周/月)最低价
        - close_qfq (float): 前复权(周/月)收盘价
        - open_hfq (float): 后复权(周/月)开盘价
        - high_hfq (float): 后复权(周/月)最高价
        - low_hfq (float): 后复权(周/月)最低价
        - close_hfq (float): 后复权(周/月)收盘价
        - vol (float): (周/月)成交量
        - amount (float): (周/月)成交额
        - change (float): (周/月)涨跌额
        - pct_chg (float): (周/月)涨跌幅 【基于除权后的昨收计算的涨跌幅：（今收-除权昨收）/除权昨收 】
        """
        pass  # stub

    def stk_weekly_monthly(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, freq: Optional[str] = None):
        """股票周/月线行情(每日更新)
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期
        - end_date (str): 计算截至日期
        - freq (str): 频率(周week,月month)
        - open (float): (周/月)开盘价
        - high (float): (周/月)最高价
        - low (float): (周/月)最低价
        - close (float): (周/月)收盘价
        - pre_close (float): 上一(周/月)收盘价
        - vol (float): (周/月)成交量
        - amount (float): (周/月)成交额
        - change (float): (周/月)涨跌额
        - pct_chg (float): (周/月)涨跌幅(未复权,如果是复权请用 通用行情接口)
        """
        pass  # stub

    def stock_basic(self, ts_code: Optional[str] = None):
        """获取基础信息数据，包括股票代码、名称、上市日期、退市日期等
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - symbol (str): 股票代码
        - name (str): 股票名称
        - area (str): 地域
        - industry (str): 所属行业
        - fullname (str): 股票全称
        - enname (str): 英文全称
        - cnspell (str): 拼音缩写
        - market (str): 市场类型（主板/创业板/科创板/CDR）
        - exchange (str): 交易所代码
        - curr_type (str): 交易货币
        - list_status (str): 上市状态 L上市 D退市 G过会未交易 P暂停上市
        - list_date (str): 上市日期
        - delist_date (str): 退市日期
        - is_hs (str): 是否沪深港通标的，N否 H沪股通 S深股通
        - act_name (str): 实控人名称
        - act_ent_type (str): 实控人企业性质
        """
        pass  # stub

    def stock_company(self, ts_code: Optional[str] = None, exchange: Optional[str] = None):
        """获取上市公司基础信息，单次提取4500条，可以根据交易所分批提取
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - com_name (str): 公司全称
        - com_id (str): 统一社会信用代码
        - exchange (str): 交易所代码
        - chairman (str): 法人代表
        - manager (str): 总经理
        - secretary (str): 董秘
        - reg_capital (float): 注册资本(万元)
        - setup_date (str): 注册日期
        - province (str): 所在省份
        - city (str): 所在城市
        - introduction (str): 公司介绍
        - website (str): 公司主页
        - email (str): 电子邮件
        - office (str): 办公室
        - employees (int): 员工人数
        - main_business (str): 主要业务及产品
        - business_scope (str): 经营范围
        """
        pass  # stub

    def stock_hsgt(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, type: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取沪深港通股票列表
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期
        - type (str): 类型
        - name (str): 股票名称
        - type_name (str): 类型名称
        - pro (=):
        - df (=):
        """
        pass  # stub

    def stock_st(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取ST股票列表，可根据交易日期获取历史上每天的ST列表权限：3000积分起提示：每天上午9:20更新，单次请求最大返回1000行数据，可循环提取,本接口数据从20160101开始,太早历史无法补齐
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - name (str): 股票名称
        - trade_date (str): 交易日期
        - type (str): 类型
        - type_name (str): 类型名称
        - pro (=):
        - df (=):
        """
        pass  # stub

    def suspend_d(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, suspend_type: Optional[str] = None):
        """按日期方式获取股票每日停复牌信息
        Args:
        Returns:
        Columns:
        - ts_code (str): TS代码
        - trade_date (str): 停复牌日期
        - suspend_timing (str): 日内停牌时间段
        - suspend_type (str): 停复牌类型：S-停牌，R-复牌
        """
        pass  # stub

    def tdx_daily(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取各板块行情，包括成交和估值等数据
        Args:
        Returns:
        Columns:
        - ts_code (str): 板块代码
        - trade_date (str): 交易日期
        - close (float): 收盘点位
        - open (float): 开盘点位
        - high (float): 最高点位
        - low (float): 最低点位
        - pre_close (float): 昨日收盘点
        - change (float): 涨跌点位
        - pct_change (float): 涨跌幅%
        - vol (float): 成交量（手）
        - amount (float): 成交额（万元）, 对于期货指数，该字段存储持仓量
        - rise (str): 收盘涨速%
        - vol_ratio (float): 量比
        - turnover_rate (float): 换手%
        - swing (float): 振幅%
        - up_num (int): 上涨家数
        - down_num (int): 下跌家数
        - limit_up_num (int): 涨停家数
        - limit_down_num (int): 跌停家数
        - lu_days (int): 连涨天数
        - mtd (float): 月初至今%
        - ytd (float): 年初至今%
        - pe (str): 市盈率
        - pb (str): 市净率
        - float_mv (float): 流通市值(亿)
        - ab_total_mv (float): AB股总市值（亿）
        - float_share (float): 流通股(亿)
        - total_share (float): 总股本(亿)
        - bm_buy_net (float): 主买净额(元)
        - bm_buy_ratio (float): 主买占比%
        - bm_net (float): 主力净额
        - bm_ratio (float): 主力占比%
        """
        pass  # stub

    def tdx_index(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, idx_type: Optional[str] = None):
        """获取板块基础信息，包括概念板块、行业、风格、地域等
        Args:
        Returns:
        Columns:
        - ts_code (str): 板块代码
        - trade_date (str): 交易日期
        - name (str): 板块名称
        - idx_type (str): 板块类型
        - idx_count (int): 成分个数
        - total_share (float): 总股本(亿)
        - float_share (float): 流通股(亿)
        - total_mv (float): 总市值(亿)
        - float_mv (float): 流通市值(亿)
        """
        pass  # stub

    def tdx_member(self, ts_code: Optional[str] = None, con_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取各板块成分股信息
        Args:
        Returns:
        Columns:
        - ts_code (str): 板块代码
        - trade_date (str): 交易日期
        - con_code (str): 成分股票代码
        - con_name (str): 成分股票名称
        """
        pass  # stub

    def ths_daily(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取板块指数行情
        Args:
        Returns:
        Columns:
        - ts_code (str): TS指数代码
        - trade_date (str): 交易日
        - close (float): 收盘点位
        - open (float): 开盘点位
        - high (float): 最高点位
        - low (float): 最低点位
        - pre_close (float): 昨日收盘点
        - avg_price (float): 平均价
        - change (float): 涨跌点位
        - pct_change (float): 涨跌幅
        - vol (float): 成交量（手）
        - turnover_rate (float): 换手率（%）
        - total_mv (float): 总市值（元）
        - float_mv (float): 流通市值（元）
        """
        pass  # stub

    def ths_hot(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None, market: Optional[str] = None, is_new: Optional[str] = None):
        """获取热榜数据，包括热股、概念板块、ETF、可转债、港美股等等，每日盘中提取4次，收盘后4次，最晚22点提取一次。
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - data_type (str): 数据类型
        - ts_code (str): 股票代码
        - ts_name (str): 股票名称
        - rank (int): 排行
        - pct_change (float): 涨跌幅%
        - current_price (float): 当前价格
        - concept (str): 标签
        - rank_reason (str): 上榜解读
        - hot (float): 热度值
        - rank_time (str): 排行榜获取时间
        """
        pass  # stub

    def ths_index(self, ts_code: Optional[str] = None, exchange: Optional[str] = None, type: Optional[str] = None):
        """获取板块指数，包括概念、行业、特色指数。
        Args:
        Returns:
        Columns:
        - ts_code (str): 代码
        """
        pass  # stub

    def ths_member(self, ts_code: Optional[str] = None, con_code: Optional[str] = None):
        """获取概念板块成分列表
        Args:
        Returns:
        Columns:
        - ts_code (str): 指数代码
        - con_code (str): 股票代码
        - con_name (str): 股票名称
        - weight (float): 权重(暂无)
        - in_date (str): 纳入日期(暂无)
        - out_date (str): 剔除日期(暂无)
        - is_new (str): 是否最新Y是N否
        """
        pass  # stub

    def top10_floatholders(self, ts_code: Optional[str] = None, period: Optional[str] = None, ann_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取上市公司前十大流通股东数据
        Args:
        Returns:
        Columns:
        - ts_code (str): TS股票代码
        - ann_date (str): 公告日期
        - end_date (str): 报告期
        - holder_name (str): 股东名称
        - hold_amount (float): 持有数量（股）
        - hold_ratio (float): 占总股本比例(%)
        - hold_float_ratio (float): 占流通股本比例(%)
        - hold_change (float): 持股变动
        - holder_type (str): 股东类型
        """
        pass  # stub

    def top10_holders(self, ts_code: Optional[str] = None, period: Optional[str] = None, ann_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取上市公司前十大股东数据，包括持有数量和比例等信息
        Args:
        Returns:
        Columns:
        - ts_code (str): TS股票代码
        - ann_date (str): 公告日期
        - end_date (str): 报告期
        - holder_name (str): 股东名称
        - hold_amount (float): 持有数量（股）
        - hold_ratio (float): 占总股本比例(%)
        - hold_float_ratio (float): 占流通股本比例(%)
        - hold_change (float): 持股变动
        - holder_type (str): 股东类型
        """
        pass  # stub

    def top_inst(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None):
        """龙虎榜机构成交明细
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): TS代码
        - exalter (str): 营业部名称
        - side (str): 买卖类型0：买入金额最大的前5名， 1：卖出金额最大的前5名
        - buy (float): 买入额（元）
        - buy_rate (float): 买入占总成交比例
        - sell (float): 卖出额（元）
        - sell_rate (float): 卖出占总成交比例
        - net_buy (float): 净成交额（元）
        - reason (str): 上榜理由
        """
        pass  # stub

    def top_list(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None):
        """龙虎榜每日交易明细
        Args:
        Returns:
        Columns:
        - trade_date (str): 交易日期
        - ts_code (str): TS代码
        """
        pass  # stub

    def trade_cal(self, exchange: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, is_open: Optional[str] = None):
        """获取各大交易所交易日历数据,默认提取的是上交所
        Args:
        Returns:
        Columns:
        - exchange (str): 交易所 SSE上交所 SZSE深交所
        - cal_date (str): 日历日期
        - is_open (str): 是否交易 0休市 1交易
        - pretrade_date (str): 上一个交易日
        """
        pass  # stub

    def weekly(self, ts_code: Optional[str] = None, trade_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """获取A股周线行情，本接口每周最后一个交易日更新，如需要使用每天更新的周线数据，请使用
        Args:
        Returns:
        Columns:
        - ts_code (str): 股票代码
        - trade_date (str): 交易日期
        - close (float): 周收盘价
        - open (float): 周开盘价
        - high (float): 周最高价
        - low (float): 周最低价
        - pre_close (float): 上一周收盘价
        - change (float): 周涨跌额
        - pct_chg (float): 周涨跌 （未复权，未
        - vol (float): 周成交量
        - amount (float): 周成交额
        """
        pass  # stub
