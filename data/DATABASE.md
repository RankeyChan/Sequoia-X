# 数据库文档 | Database Schema

> 数据源: [Tushare Pro](https://tushare.pro) — 2000+ 积分  
> 存储引擎: SQLite — `data/sequoia_v2.db`  
> 日期格式: 统一 `yyyyMMdd`（8 位纯数字）

---

## 目录

1. [K 线行情](#1-k-线行情)
2. [基础数据](#2-基础数据)
3. [基本面指标（日频）](#3-基本面指标日频)
4. [资金流向](#4-资金流向)
5. [市场情绪（涨跌停/龙虎榜）](#5-市场情绪)
6. [北向/南向资金](#6-北向南向资金)
7. [融资融券](#7-融资融券)
8. [财务数据（报告期）](#8-财务数据报告期)
9. [上市公司行为](#9-上市公司行为)
10. [概念/分类/金股](#10-概念分类金股)
11. [日期/复权](#11-日期复权)

---

## 1. K 线行情

### stock_daily — 日 K 线行情

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码（纯数字，如 `000001`） |
| date | TEXT | 交易日期（`yyyyMMdd`） |
| open | REAL | 开盘价（后复权） |
| high | REAL | 最高价（后复权） |
| low | REAL | 最低价（后复权） |
| close | REAL | 收盘价（后复权） |
| volume | REAL | 成交量（股） |
| turnover | REAL | 成交额（元） |

**Tushare API**: `daily` — 按交易日期或股票代码获取  
**状态**: ✅ 已同步 44,093 条  
**查询示例**:
```sql
-- 某只股票最近 20 个交易日
SELECT * FROM stock_daily WHERE symbol = '000001' ORDER BY date DESC LIMIT 20;

-- 某日全市场行情
SELECT COUNT(*), AVG(close) FROM stock_daily WHERE date = '20260609';
```

---

## 2. 基础数据

### stock_basic — 股票列表

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| name | TEXT | 股票名称（如 `平安银行`） |
| industry | TEXT | 所属行业（如 `银行`） |
| area | TEXT | 所在地区（如 `深圳`） |
| list_date | TEXT | 上市日期（`yyyyMMdd`） |
| market | TEXT | 市场类型（主板/创业板/科创板/北交所） |

**Tushare API**: `stock_basic`  
**状态**: ✅ 已同步 5,527 条  

### trade_cal — 交易日历

| 字段 | 类型 | 说明 |
|------|------|------|
| cal_date | TEXT | 日历日期（`yyyyMMdd`） |
| is_open | INTEGER | 是否交易: 1=交易日, 0=非交易日 |
| pretrade_date | TEXT | 上一个交易日 |

**Tushare API**: `trade_cal` — 上海证券交易所  
**状态**: ✅ 已同步 10 条  

---

## 3. 基本面指标（日频）

### daily_basic — 每日基本面指标

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| date | TEXT | 交易日期 |
| close | REAL | 收盘价（不复权） |
| pe | REAL | 市盈率（静态） |
| pe_ttm | REAL | 市盈率（TTM，滚动 12 个月） |
| pb | REAL | 市净率 |
| ps | REAL | 市销率（静态） |
| ps_ttm | REAL | 市销率（TTM） |
| total_mv | REAL | 总市值（万元） |
| circ_mv | REAL | 流通市值（万元） |
| turnover_rate | REAL | 换手率（%） |
| turnover_rate_f | REAL | 换手率（自由流通股，%） |
| volume_ratio | REAL | 量比 |
| dv_ratio | REAL | 股息率（静态，%） |
| dv_ttm | REAL | 股息率（TTM，%） |
| total_share | REAL | 总股本（万股） |
| float_share | REAL | 流通股本（万股） |
| free_share | REAL | 自由流通股本（万股） |

**Tushare API**: `daily_basic`  
**状态**: ✅ 已同步 44,093 条  
**选股权重**: 极重要 — PE/PB/市值被所有策略用作基本面过滤器  

---

## 4. 资金流向

### moneyflow — 个股资金流向

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| date | TEXT | 交易日期 |
| buy_sm_vol | REAL | 小单买入量（手） |
| buy_sm_amount | REAL | 小单买入额（万元） |
| sell_sm_vol | REAL | 小单卖出量（手） |
| sell_sm_amount | REAL | 小单卖出额（万元） |
| buy_md_vol | REAL | 中单买入量（手） |
| buy_md_amount | REAL | 中单买入额（万元） |
| sell_md_vol | REAL | 中单卖出量（手） |
| sell_md_amount | REAL | 中单卖出额（万元） |
| buy_lg_vol | REAL | 大单买入量（手） |
| buy_lg_amount | REAL | 大单买入额（万元） |
| sell_lg_vol | REAL | 大单卖出量（手） |
| sell_lg_amount | REAL | 大单卖出额（万元） |
| buy_elg_vol | REAL | 超大单买入量（手） |
| buy_elg_amount | REAL | 超大单买入额（万元） |
| sell_elg_vol | REAL | 超大单卖出量（手） |
| sell_elg_amount | REAL | 超大单卖出额（万元） |
| net_mf_vol | REAL | 净流入量（手），正=流入 |
| net_mf_amount | REAL | 净流入额（万元），正=流入 |

**Tushare API**: `moneyflow`  
**状态**: ✅ 已同步 41,561 条  
**说明**: 按挂单金额分类：
- 小单: < 4 万元
- 中单: 4~20 万元
- 大单: 20~100 万元
- 超大单: > 100 万元

**对应策略**: `MoneyFlowStrategy` — 主力资金持续流入检测

### moneyflow_hsgt — 沪深港通资金流向

| 字段 | 类型 | 说明 |
|------|------|------|
| trade_date | TEXT | 交易日期 |
| ggt_ss | REAL | 港股通（沪）成交净买入（亿元） |
| ggt_sz | REAL | 港股通（深）成交净买入（亿元） |
| hgt | REAL | 沪股通成交净买入（亿元） |
| sgt | REAL | 深股通成交净买入（亿元） |
| north_money | REAL | 北向资金净流入（亿元） |
| south_money | REAL | 南向资金净流入（亿元） |

**Tushare API**: `moneyflow_hsgt`  
**状态**: ✅ 已同步 1 条  

---

## 5. 市场情绪

### limit_list — 涨跌停及炸板数据

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| date | TEXT | 交易日期 |
| name | TEXT | 股票名称 |
| industry | TEXT | 所属行业 |
| limit_type | TEXT | 类型: U=涨停, D=跌停, Z=炸板 |
| close | REAL | 收盘价 |
| pct_chg | REAL | 涨跌幅（%） |
| amount | REAL | 成交额（元） |
| limit_amount | REAL | 板上成交额（元） |
| float_mv | REAL | 流通市值（万元） |
| total_mv | REAL | 总市值（万元） |
| turnover_ratio | REAL | 换手率（%） |
| fd_amount | REAL | 封单金额（元） |
| first_time | TEXT | 首次涨停/跌停时间 |
| last_time | TEXT | 最后涨停/跌停时间 |
| open_times | INTEGER | 开板次数（涨停→打开→回封） |
| limit_times | INTEGER | 连板数（连续涨停天数） |
| up_stat | TEXT | 涨停统计（如 `1/1` 表示 1 次涨停 1 次封板） |

**Tushare API**: `limit_list_d`  
**状态**: ⏳ 待回填  
**对应策略**: `LimitUpShakeoutStrategy` — 真实涨停数据判断

### top_list — 龙虎榜交易明细

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| date | TEXT | 交易日期 |
| name | TEXT | 股票名称 |
| close | REAL | 收盘价 |
| pct_change | REAL | 涨跌幅（%） |
| turnover_rate | REAL | 换手率（%） |
| amount | REAL | 总成交额（元） |
| l_sell | REAL | 龙虎榜席位总卖出额（元） |
| l_buy | REAL | 龙虎榜席位总买入额（元） |
| l_amount | REAL | 龙虎榜席位总成交额（元） |
| net_amount | REAL | 龙虎榜净买入额（元），正=净买 |
| net_rate | REAL | 净买入额占比（%） |
| amount_rate | REAL | 龙虎榜成交额占总成交比例（%） |
| float_values | REAL | 流通市值（元） |
| reason | TEXT | 上榜原因（如 `日涨幅偏离值达7%`） |

**Tushare API**: `top_list`  
**状态**: ⏳ 待回填  
**对应策略**: `InstitutionalStrategy`

### top_inst — 龙虎榜机构交易明细

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| date | TEXT | 交易日期 |
| exalter | TEXT | 席位名称（机构专用/深股通专用/游资等） |
| side | TEXT | 交易方向: 买入/卖出/中性 |
| buy | REAL | 买入金额（元） |
| buy_rate | REAL | 买入金额占成交额比例（%） |
| sell | REAL | 卖出金额（元） |
| sell_rate | REAL | 卖出金额占成交额比例（%） |
| net_buy | REAL | 净买入（元），正=净买 |
| reason | TEXT | 上榜原因 |

**Tushare API**: `top_inst`  
**状态**: ✅ 已同步 9,180 条  
**对应策略**: `InstitutionalStrategy` — 机构买入识别

### block_trade — 大宗交易

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| trade_date | TEXT | 交易日期 |
| price | REAL | 成交价 |
| vol | REAL | 成交量（万股） |
| amount | REAL | 成交额（万元） |
| buyer | TEXT | 买方席位 |
| seller | TEXT | 卖方席位 |

**Tushare API**: `block_trade`  
**状态**: ⏳ 待回填  

---

## 6. 北向/南向资金

### hk_hold — 沪深股通持股明细

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码（A 股） |
| date | TEXT | 交易日期 |
| name | TEXT | 股票名称 |
| vol | INTEGER | 北向资金持股数量（股） |
| ratio | REAL | 北向资金持股比例（%，= vol/总股本×100） |
| exchange | TEXT | 市场: SH=沪股通, SZ=深股通, HK=港股通 |

**Tushare API**: `hk_hold`  
**状态**: ⏳ 待回填  
**对应策略**: `NorthBoundStrategy` — 北向资金持续增持检测

---

## 7. 融资融券

### margin_detail — 融资融券交易明细

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| date | TEXT | 交易日期 |
| name | TEXT | 股票名称 |
| rzye | REAL | 融资余额（元） |
| rqye | REAL | 融券余额（元） |
| rzmre | REAL | 融资买入额（元） |
| rqyl | REAL | 融券余量（股） |
| rzche | REAL | 融资偿还额（元） |
| rqchl | REAL | 融券偿还量（股） |
| rqmcl | REAL | 融券卖出量（股） |
| rzrqye | REAL | 融资融券余额（元，rzye + rqye） |

**Tushare API**: `margin_detail`  
**状态**: ✅ 已同步 30,568 条  
**说明**: 融资=看多（借钱买股）, 融券=看空（借股卖出）

---

## 8. 财务数据（报告期）

### fina_indicator — 财务指标

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| ann_date | TEXT | 公告日期 |
| end_date | TEXT | 报告期 |

#### 每股指标

| 字段 | 类型 | 说明 |
|------|------|------|
| eps | REAL | 每股收益 |
| dt_eps | REAL | 稀释每股收益 |
| total_revenue_ps | REAL | 每股营业总收入 |
| revenue_ps | REAL | 每股营业收入 |
| bps | REAL | 每股净资产 |
| ocfps | REAL | 每股经营活动现金流 |
| cfps | REAL | 每股现金流量净额 |
| ebit_ps | REAL | 每股息税前利润 |
| fcff_ps | REAL | 每股企业自由现金流 |
| fcfe_ps | REAL | 每股股东自由现金流 |
| retainedps | REAL | 每股留存收益 |
| diluted2_eps | REAL | 期末摊薄每股收益 |

#### 盈利能力

| 字段 | 类型 | 说明 |
|------|------|------|
| roe | REAL | ROE（%），净资产收益率 |
| roe_waa | REAL | ROE 加权平均（%） |
| roe_dt | REAL | ROE 扣非摊薄（%） |
| roa | REAL | ROA（%），总资产收益率 |
| npta | REAL | 总资产净利润 |
| roic | REAL | 投入资本回报率（%） |
| gross_margin | REAL | 毛利率（%） |
| grossprofit_margin | REAL | 销售毛利率（%） |
| netprofit_margin | REAL | 销售净利率（%） |
| profit_dedt | REAL | 扣非净利润 |
| extra_item | REAL | 非经常性损益 |
| roe_yearly | REAL | ROE 年化（%） |
| roa2_yearly | REAL | 年化 ROA |
| roa_yearly | REAL | 年化 ROA |

#### 收益质量

| 字段 | 类型 | 说明 |
|------|------|------|
| op_income | REAL | 经营活动净收益 |
| ebit | REAL | 息税前利润 |
| ebitda | REAL | 息税折旧摊销前利润 |
| fcff | REAL | 企业自由现金流 |
| fcfe | REAL | 股权自由现金流 |
| profit_to_op | REAL | 利润总额/营业收入 |
| profit_to_gr | REAL | 净利润/营业总收入 |

#### 偿债能力

| 字段 | 类型 | 说明 |
|------|------|------|
| current_ratio | REAL | 流动比率 |
| quick_ratio | REAL | 速动比率 |
| cash_ratio | REAL | 现金比率 |
| debt_to_assets | REAL | 资产负债率（%） |
| assets_to_eqt | REAL | 权益乘数 |
| interestdebt | REAL | 带息债务 |
| netdebt | REAL | 净债务 |
| current_exint | REAL | 无息流动负债 |
| noncurrent_exint | REAL | 无息非流动负债 |
| tangible_asset | REAL | 有形资产 |
| working_capital | REAL | 营运资本 |
| networking_capital | REAL | 净营运资本 |
| invest_capital | REAL | 投入资本 |
| retained_earnings | REAL | 留存收益 |
| int_to_talcap | REAL | 带息债务/全部投入资本 |
| eqt_to_talcapital | REAL | 归属母公司权益/全部投入资本 |
| debt_to_eqt | REAL | 产权比率 |
| eqt_to_debt | REAL | 归属母公司权益/负债 |
| eqt_to_interestdebt | REAL | 归属母公司权益/带息债务 |
| ocf_to_debt | REAL | 经营现金流/负债 |
| ocf_to_shortdebt | REAL | 经营现金流/短期债务 |
| tangibleasset_to_debt | REAL | 有形资产/负债 |
| tangasset_to_intdebt | REAL | 有形资产/带息债务 |
| tangibleasset_to_netdebt | REAL | 有形资产/净债务 |

#### 营运能力

| 字段 | 类型 | 说明 |
|------|------|------|
| ar_turn | REAL | 应收账款周转率 |
| ca_turn | REAL | 流动资产周转率 |
| fa_turn | REAL | 固定资产周转率 |
| assets_turn | REAL | 总资产周转率 |
| turn_days | REAL | 营业周期（天） |
| inv_turn_days | REAL | 存货周转天数 |
| arturn_days | REAL | 应收账款周转天数 |

#### 费用结构

| 字段 | 类型 | 说明 |
|------|------|------|
| cogs_of_sales | REAL | 销售成本率（%） |
| expense_of_sales | REAL | 销售期间费用率（%） |
| saleexp_to_gr | REAL | 销售费用/营业总收入 |
| adminexp_of_gr | REAL | 管理费用/营业总收入 |
| finaexp_of_gr | REAL | 财务费用/营业总收入 |
| gc_of_gr | REAL | 营业总成本/营业总收入 |
| op_of_gr | REAL | 营业利润/营业总收入 |
| ebit_of_gr | REAL | 息税前利润/营业总收入 |
| impai_ttm | REAL | 资产减值损失/营业总收入（TTM） |

#### 资产结构

| 字段 | 类型 | 说明 |
|------|------|------|
| ca_to_assets | REAL | 流动资产/总资产 |
| nca_to_assets | REAL | 非流动资产/总资产 |
| tbassets_to_totalassets | REAL | 有形资产/总资产 |
| fixed_assets | REAL | 固定资产合计 |
| dp_assets_to_eqt | REAL | 权益乘数（杜邦分析） |
| currentdebt_to_debt | REAL | 流动负债/负债合计 |
| longdeb_to_debt | REAL | 非流动负债/负债合计 |

#### 同比增长

| 字段 | 类型 | 说明 |
|------|------|------|
| basic_eps_yoy | REAL | 基本每股收益同比（%） |
| dt_eps_yoy | REAL | 稀释每股收益同比（%） |
| netprofit_yoy | REAL | 净利润同比（%） |
| dt_netprofit_yoy | REAL | 扣非净利润同比（%） |
| or_yoy | REAL | 营业收入同比（%） |
| tr_yoy | REAL | 营业总收入同比（%） |
| op_yoy | REAL | 营业利润同比（%） |
| ebt_yoy | REAL | 利润总额同比（%） |
| ocf_yoy | REAL | 经营现金流同比（%） |
| cfps_yoy | REAL | 每股经营现金流同比（%） |
| roe_yoy | REAL | ROE 同比（%） |
| bps_yoy | REAL | 每股净资产同比（%） |
| assets_yoy | REAL | 总资产同比（%） |
| eqt_yoy | REAL | 净资产同比（%） |
| equity_yoy | REAL | 净资产同比增长率 |

#### 单季度

| 字段 | 类型 | 说明 |
|------|------|------|
| q_roe | REAL | 单季度 ROE |
| q_dt_roe | REAL | 单季度扣非 ROE |
| q_npta | REAL | 单季度总资产净利率 |
| q_ocf_to_sales | REAL | 单季度经营现金流/营业收入 |
| q_sales_yoy | REAL | 单季度营收同比（%） |
| q_gr_yoy | REAL | 单季度营业总收入同比（%） |
| q_gr_qoq | REAL | 单季度营业总收入环比（%） |
| q_op_qoq | REAL | 单季度营业利润环比（%） |
| q_saleexp_to_gr | REAL | 单季度销售费用率 |
| q_gc_to_gr | REAL | 单季度销售成本率 |

#### 其他

| 字段 | 类型 | 说明 |
|------|------|------|
| roa_dp | REAL | 杜邦 ROA（%） |
| roa_yearly | REAL | 年化 ROA |
| update_flag | TEXT | 更新标识 |

**Tushare API**: `fina_indicator`  
**状态**: ⏳ 待回填  
**Tushare 接口说明**: [财务指标](https://tushare.pro/document/2?doc_id=79)

### income — 利润表

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| ann_date | TEXT | 公告日期 |
| f_ann_date | TEXT | 实际公告日期 |
| end_date | TEXT | 报告期 |
| report_type | TEXT | 报告类型: 1=Q1, 2=中报, 3=Q3, 4=年报 |
| comp_type | TEXT | 公司类型: 1=一般工商业, 2=银行, 3=保险, 4=证券 |
| basic_eps | REAL | 基本每股收益 |
| diluted_eps | REAL | 稀释每股收益 |
| total_revenue | REAL | 营业总收入（元） |
| revenue | REAL | 营业收入（元） |
| int_income | REAL | 利息收入 |
| operate_profit | REAL | 营业利润 |
| total_profit | REAL | 利润总额 |
| income_tax | REAL | 所得税 |
| n_income | REAL | 净利润（含少数股东损益） |
| n_income_attr_p | REAL | 归属母公司净利润 |
| ebit | REAL | 息税前利润 |
| ebitda | REAL | 息税折旧摊销前利润 |
| total_cogs | REAL | 营业总成本 |
| oper_cost | REAL | 营业成本 |
| sell_exp | REAL | 销售费用 |
| admin_exp | REAL | 管理费用 |
| fin_exp | REAL | 财务费用 |
| rd_exp | REAL | 研发费用 |
| invest_income | REAL | 投资收益 |
| fv_value_chg_gain | REAL | 公允价值变动收益 |
| forex_gain | REAL | 汇兑收益 |
| biz_tax_surchg | REAL | 营业税金及附加 |
| assets_impair_loss | REAL | 资产减值损失 |
| oth_income | REAL | 其他收益 |
| continued_net_profit | REAL | 持续经营净利润 |
| update_flag | TEXT | 更新标识 |

**Tushare API**: `income`  
**状态**: ⏳ 待回填  
**Tushare 接口说明**: [利润表](https://tushare.pro/document/2?doc_id=80)

### balancesheet — 资产负债表

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| ann_date | TEXT | 公告日期 |
| f_ann_date | TEXT | 实际公告日期 |
| end_date | TEXT | 报告期 |
| report_type | TEXT | 报告类型 |
| comp_type | TEXT | 公司类型 |
| total_assets | REAL | 总资产 |
| total_liab | REAL | 总负债 |
| total_hldr_eqy_exc_min_int | REAL | 归属母公司股东权益（不含少数股东） |
| total_cur_assets | REAL | 流动资产合计 |
| total_nca | REAL | 非流动资产合计 |
| total_cur_liab | REAL | 流动负债合计 |
| total_ncl | REAL | 非流动负债合计 |
| money_cap | REAL | 货币资金 |
| accounts_receiv | REAL | 应收账款 |
| inventories | REAL | 存货 |
| fix_assets | REAL | 固定资产 |
| intan_assets | REAL | 无形资产 |
| r_and_d | REAL | 研发支出 |
| goodwill | REAL | 商誉 |
| lt_borr | REAL | 长期借款 |
| st_borr | REAL | 短期借款 |
| notes_payable | REAL | 应付票据 |
| acct_payable | REAL | 应付账款 |
| contract_liab | REAL | 合同负债 |
| contract_assets | REAL | 合同资产 |
| defer_tax_assets | REAL | 递延所得税资产 |
| defer_tax_liab | REAL | 递延所得税负债 |
| update_flag | TEXT | 更新标识 |

**Tushare API**: `balancesheet`  
**状态**: ⏳ 待回填  
**Tushare 接口说明**: [资产负债表](https://tushare.pro/document/2?doc_id=82)

### cashflow — 现金流量表

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| ann_date | TEXT | 公告日期 |
| f_ann_date | TEXT | 实际公告日期 |
| end_date | TEXT | 报告期 |
| report_type | TEXT | 报告类型 |
| comp_type | TEXT | 公司类型 |
| net_profit | REAL | 净利润 |
| n_cashflow_act | REAL | 经营活动现金流量净额 |
| n_cashflow_inv_act | REAL | 投资活动现金流量净额 |
| n_cash_flows_fnc_act | REAL | 筹资活动现金流量净额 |
| free_cashflow | REAL | 自由现金流 |
| c_cash_equ_beg_period | REAL | 期初现金及等价物余额 |
| c_cash_equ_end_period | REAL | 期末现金及等价物余额 |
| update_flag | TEXT | 更新标识 |

**Tushare API**: `cashflow`  
**状态**: ⏳ 待回填  
**Tushare 接口说明**: [现金流量表](https://tushare.pro/document/2?doc_id=84)

### forecast — 业绩预告

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| ann_date | TEXT | 公告日期 |
| end_date | TEXT | 报告期 |
| type | TEXT | 预告类型: 预增/预减/扭亏/首亏/续亏/续盈/略增/略减 |
| p_change_min | REAL | 净利润变动下限（%） |
| p_change_max | REAL | 净利润变动上限（%） |
| net_profit_min | REAL | 净利润下限（万元） |
| net_profit_max | REAL | 净利润上限（万元） |
| last_parent_net | REAL | 上年同期净利润 |
| first_ann_date | TEXT | 首次公告日期 |
| summary | TEXT | 业绩摘要 |
| change_reason | TEXT | 变动原因 |

**Tushare API**: `forecast`  
**状态**: ⏳ 待回填  
**Tushare 接口说明**: [业绩预告](https://tushare.pro/document/2?doc_id=86)

### express — 业绩快报

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| ann_date | TEXT | 公告日期 |
| end_date | TEXT | 报告期 |
| revenue | REAL | 营业收入 |
| operate_profit | REAL | 营业利润 |
| total_profit | REAL | 利润总额 |
| n_income | REAL | 净利润 |
| total_assets | REAL | 总资产 |
| total_hldr_eqy_exc_min_int | REAL | 归属母公司股东权益 |
| diluted_eps | REAL | 每股收益 |
| diluted_roe | REAL | ROE |
| yoy_net_profit | REAL | 净利润同比（%） |
| bps | REAL | 每股净资产 |
| yoy_sales | REAL | 营收同比（%） |
| yoy_op | REAL | 营业利润同比（%） |
| yoy_tp | REAL | 利润总额同比（%） |
| yoy_dedu_np | REAL | 扣非净利润同比（%） |
| yoy_eps | REAL | EPS 同比（%） |
| yoy_roe | REAL | ROE 同比（%） |
| growth_assets | REAL | 总资产增长率（%） |
| yoy_equity | REAL | 净资产增长率（%） |
| growth_bps | REAL | 每股净资产增长率（%） |
| perf_summary | TEXT | 业绩摘要 |
| is_audit | INTEGER | 是否审计: 1=是, 0=否 |

**Tushare API**: `express`  
**状态**: ⏳ 待回填  
**Tushare 接口说明**: [业绩快报](https://tushare.pro/document/2?doc_id=87)

---

## 9. 上市公司行为

### dividend — 分红送股

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| end_date | TEXT | 分红年度 |
| ann_date | TEXT | 公告日期 |
| div_proc | TEXT | 分红进度: 预案/决案/实施 |
| stk_div | REAL | 每股送股 |
| stk_bo_rate | REAL | 每股转增 |
| stk_co_rate | REAL | 每股转赠 |
| cash_div | REAL | 每股分红（税前，元） |
| cash_div_tax | REAL | 每股分红（税后，元） |
| record_date | TEXT | 股权登记日 |
| ex_date | TEXT | 除权除息日 |
| pay_date | TEXT | 派息日 |
| div_listdate | TEXT | 红股上市日 |
| imp_ann_date | TEXT | 实施公告日 |
| base_date | TEXT | 基准日 |
| base_share | REAL | 基准股本（万股） |

**Tushare API**: `dividend`  
**状态**: ⏳ 待回填  
**Tushare 接口说明**: [分红送股](https://tushare.pro/document/2?doc_id=93)

### stk_holdertrade — 股东增减持

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| ann_date | TEXT | 公告日期 |
| holder_name | TEXT | 股东名称 |
| holder_type | TEXT | 股东类型: C=公司, P=个人, G=高管 |
| in_de | TEXT | 方向: IN=增持, DE=减持 |
| change_vol | REAL | 变动数量（股） |
| change_ratio | REAL | 变动比例（%） |
| after_share | REAL | 变动后持股 |
| after_ratio | REAL | 变动后比例（%） |
| avg_price | REAL | 均价 |
| total_share | REAL | 总股本 |
| begin_date | TEXT | 开始日期 |
| close_date | TEXT | 结束日期 |

**Tushare API**: `stk_holdertrade`  
**状态**: ⏳ 待回填

### stk_holdernumber — 股东人数

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| ann_date | TEXT | 公告日期 |
| end_date | TEXT | 截止日期 |
| holder_num | INTEGER | 股东户数 |

**Tushare API**: `stk_holdernumber`  
**状态**: ⏳ 待回填  
**说明**: 股东人数减少通常意味着筹码集中

### pledge_stat — 股权质押统计

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| end_date | TEXT | 截止日期 |
| pledge_count | INTEGER | 质押次数 |
| unrest_pledge | REAL | 无限售质押数量（万股） |
| rest_pledge | REAL | 限售质押数量（万股） |
| total_share | REAL | 总股本（万股） |
| pledge_ratio | REAL | 质押比例（%） |

**Tushare API**: `pledge_stat`  
**状态**: ⏳ 待回填  
**说明**: 质押比例过高（>50%）需警惕平仓风险

### share_float — 限售股解禁

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| ann_date | TEXT | 公告日期 |
| float_date | TEXT | 解禁日期 |
| float_share | REAL | 解禁数量（万股） |
| float_ratio | REAL | 解禁比例（占总股本%） |
| holder_name | TEXT | 持有人名称 |
| share_type | TEXT | 股份类型 |

**Tushare API**: `share_float`  
**状态**: ⏳ 待回填  
**说明**: 解禁比例高且持有人分散时需注意减持压力

### repurchase — 股票回购

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| ann_date | TEXT | 公告日期 |
| end_date | TEXT | 回购截止日期 |
| proc | TEXT | 进度: 实施/完成/停止 |
| exp_date | TEXT | 预计截止日期 |
| vol | REAL | 已回购数量（万股） |
| amount | REAL | 已回购金额（万元） |
| high_limit | REAL | 回购价格上限 |
| low_limit | REAL | 回购价格下限 |

**Tushare API**: `repurchase`  
**状态**: ⏳ 待回填  
**说明**: 回购通常被市场视为积极信号

---

## 10. 概念/分类/金股

### concept — 概念股分类

| 字段 | 类型 | 说明 |
|------|------|------|
| code | TEXT | 概念代码 |
| name | TEXT | 概念名称（如 `5G概念`, `新能源汽车`） |
| src | TEXT | 来源: `ts`=同花顺 |

**Tushare API**: `concept`  
**状态**: ⏳ 待回填

### concept_detail — 概念股明细

| 字段 | 类型 | 说明 |
|------|------|------|
| id | TEXT | 概念 ID |
| concept_name | TEXT | 概念名称 |
| symbol | TEXT | 股票代码 |
| name | TEXT | 股票名称 |
| in_date | TEXT | 纳入日期 |
| out_date | TEXT | 剔除日期（空=仍在概念中） |

**Tushare API**: `concept_detail`  
**状态**: ⏳ 待回填

### broker_recommend — 券商月度金股

| 字段 | 类型 | 说明 |
|------|------|------|
| month | TEXT | 月份（`yyyyMM`） |
| broker | TEXT | 券商名称（如 `中信证券`） |
| symbol | TEXT | 股票代码 |
| name | TEXT | 股票名称 |

**Tushare API**: `broker_recommend`  
**状态**: ⏳ 待回填  
**说明**: 每月初更新，可跟踪券商集体推荐的方向

---

## 11. 日期/复权

### adj_factor — 复权因子

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| trade_date | TEXT | 交易日期 |
| adj_factor | REAL | 复权因子（前复权 = 不复权价 × 累计因子） |

**Tushare API**: `adj_factor`  
**状态**: ⏳ 待回填  
**说明**: 后复权价 = 不复权价 × 截至今日的累计复权因子。`stock_daily` 表已预置后复权数据

---

## 数据状态汇总

| 表名 | 状态 | 数据量 | 更新频率 |
|------|------|--------|---------|
| **stock_daily** | ✅ | 44,093 条 | 每日 |
| **stock_basic** | ✅ | 5,527 条 | 低频 |
| **daily_basic** | ✅ | 44,093 条 | 每日 |
| **moneyflow** | ✅ | 41,561 条 | 每日 |
| **margin_detail** | ✅ | 30,568 条 | 每日 |
| **top_inst** | ✅ | 9,180 条 | 每日 |
| **trade_cal** | ✅ | 10 条 | 低频 |
| **moneyflow_hsgt** | ✅ | 1 条 | 每日 |
| limit_list | ⏳ | 0 条 | 每日 |
| hk_hold | ⏳ | 0 条 | 每日 |
| top_list | ⏳ | 0 条 | 每日 |
| fina_indicator | ⏳ | 0 条 | 季度 |
| income | ⏳ | 0 条 | 季度 |
| balancesheet | ⏳ | 0 条 | 季度 |
| cashflow | ⏳ | 0 条 | 季度 |
| forecast | ⏳ | 0 条 | 不定期 |
| express | ⏳ | 0 条 | 不定期 |
| dividend | ⏳ | 0 条 | 低频 |
| stk_holdertrade | ⏳ | 0 条 | 不定期 |
| stk_holdernumber | ⏳ | 0 条 | 不定期 |
| pledge_stat | ⏳ | 0 条 | 低频 |
| share_float | ⏳ | 0 条 | 每日 |
| block_trade | ⏳ | 0 条 | 每日 |
| repurchase | ⏳ | 0 条 | 不定期 |
| concept | ⏳ | 0 条 | 低频 |
| concept_detail | ⏳ | 0 条 | 低频 |
| broker_recommend | ⏳ | 0 条 | 月度 |
| adj_factor | ⏳ | 0 条 | 每日 |

**状态说明**:
- ✅ 已同步（数据可用）
- ⏳ 待回填（表结构已创建，运行 `python main.py --backfill` 后填充）

---

## 常用查询示例

```sql
-- 最近 N 个交易日列表
SELECT cal_date FROM trade_cal WHERE is_open = 1 ORDER BY cal_date DESC LIMIT 5;

-- 某日涨停股票
SELECT * FROM limit_list WHERE date = '20260609' AND limit_type = 'U';

-- 某日主力净流入前 10
SELECT symbol, SUM(net_mf_amount) AS total_net
FROM moneyflow WHERE date = '20260609'
GROUP BY symbol ORDER BY total_net DESC LIMIT 10;

-- 北向资金增持排名
SELECT symbol, ratio FROM hk_hold
WHERE date = (SELECT MAX(date) FROM hk_hold)
ORDER BY ratio DESC LIMIT 20;

-- 全市场估值分布
SELECT
  CASE
    WHEN pe_ttm < 10 THEN '<10'
    WHEN pe_ttm < 20 THEN '10-20'
    WHEN pe_ttm < 50 THEN '20-50'
    WHEN pe_ttm < 100 THEN '50-100'
    ELSE '>100'
  END AS pe_range,
  COUNT(*) AS stock_count
FROM daily_basic WHERE date = '20260609' AND pe_ttm > 0
GROUP BY pe_range ORDER BY MIN(pe_ttm);
```
