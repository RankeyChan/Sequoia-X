# 数据库文档 | Database Schema

> 数据源: Tushare Pro — 10000+ 积分
> 存储: SQLite — `data/sequoia_v2.db` (94.8 MB)
> 日期格式: 统一 `yyyyMMdd`（8位纯数字）
> 表总数: **92 张**

---

## 目录

| 分类 | 表数 | 说明 |
|------|------|------|
| [K线行情](#k线行情) | 1 | stock_daily |
| [基础数据](#基础数据) | 11 | 股票列表/股本/日历/ST/公司/管理层等 |
| [行情指标](#行情指标) | 6 | daily_basic / adj_factor / stk_limit / suspen_d |
| [资金流向](#资金流向) | 9 | moneyflow / hsgt / ths/dc |
| [沪深港通](#沪深港通) | 5 | hk_hold / hsgt_top10 / ggt / hs_const |
| [两融](#两融) | 6 | margin / margin_detail / slb |
| [涨跌停/龙虎榜](#涨跌停龙虎榜) | 7 | limit_list / top_list / top_inst / kpl |
| [财务数据](#财务数据) | 10 | income / balancesheet / fina_indicator / forecast 等 |
| [股东/分红/质押](#股东分红质押) | 9 | stk_holdertrade / dividend / pledge_stat / share_float |
| [打板/概念/板块](#打板概念板块) | 14 | ths_index / dc_daily / tdx_member 等 |
| [热榜/游资](#热榜游资) | 4 | ths_hot / hm_list / hm_detail |
| [技术因子](#技术因子) | 3 | stk_factor / cyq_perf / index_weight |
| [中央结算/其他](#中央结算其他) | 5 | ccass_hold / report_rc / stk_auction / stk_nineturn |
| [港股通](#港股通) | 2 | ggt_top10 / ggt_daily |

---

## K线行情

### stock_daily — 日K线行情（核心表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 自增主键 |
| symbol | TEXT | 股票代码 |
| date | TEXT | 交易日期 |
| open | REAL | 开盘价（后复权） |
| high | REAL | 最高价（后复权） |
| low | REAL | 最低价（后复权） |
| close | REAL | 收盘价（后复权） |
| volume | REAL | 成交量（股） |
| turnover | REAL | 成交额（元） |

**数据**: ✅ 143,051 条 | **API**: `daily` | **唯一键**: (symbol, date)

---

## 基础数据

### stock_basic — 股票列表

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码（纯数字） |
| name | TEXT | 股票名称 |
| industry | TEXT | 所属行业 |
| area | TEXT | 所在地区 |
| list_date | TEXT | 上市日期 |
| market | TEXT | 市场类型（主板/创业板/科创板/北交所） |

✅ 5,528 条 | **API**: `stock_basic`

### stk_premarket — 每日股本（盘前）

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| trade_date | TEXT | 交易日期 |
| total_share | REAL | 总股本（股） |
| float_share | REAL | 流通股本（股） |
| pre_close | REAL | 昨收价 |
| up_limit | REAL | 涨停价 |
| down_limit | REAL | 跌停价 |

⬜ 0 条 | **API**: `stk_premarket`

### trade_cal — 交易日历

| 字段 | 类型 | 说明 |
|------|------|------|
| cal_date | TEXT | 日历日期 |
| is_open | INTEGER | 是否交易: 1=是, 0=否 |
| pretrade_date | TEXT | 上一个交易日 |

✅ 43 条 | **API**: `trade_cal`

### stock_company — 上市公司基本信息

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| com_name | TEXT | 公司全称 |
| exchange | TEXT | 交易所 |
| chairman | TEXT | 董事长 |
| manager | TEXT | 总经理 |
| reg_capital | REAL | 注册资本 |
| setup_date | TEXT | 成立日期 |
| province | TEXT | 省份 |
| city | TEXT | 城市 |
| website | TEXT | 公司网址 |
| employees | INTEGER | 员工人数 |
| main_business | TEXT | 主要业务 |

⬜ 0 条 | **API**: `stock_company`

### stock_st — ST股票列表

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| trade_date | TEXT | 交易日期 |
| name | TEXT | 股票名称 |
| type | TEXT | ST类型 |
| type_name | TEXT | ST类型名称 |

⬜ 0 条 | **API**: `stock_st`

### stock_hsgt — 沪深港通股票列表

⬜ 0 条 | **API**: `stock_hsgt`

### st — ST风险警示板股票

⬜ 0 条 | **API**: `st`

### stk_managers — 上市公司管理层

⬜ 0 条 | **API**: `stk_managers`

### stk_rewards — 管理层薪酬和持股

⬜ 0 条 | **API**: `stk_rewards`

### namechange — 股票曾用名

⬜ 0 条 | **API**: `namechange`

### new_share — IPO新股上市

⬜ 0 条 | **API**: `new_share`

### bse_mapping — 北交所新旧代码对照

⬜ 0 条 | **API**: `bse_mapping`

### bak_basic — 股票历史列表

⬜ 0 条 | **API**: `bak_basic`

---

## 行情指标

### daily_basic — 每日基本面指标

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| date | TEXT | 交易日期 |
| close | REAL | 收盘价（不复权） |
| pe | REAL | 市盈率（静态） |
| pe_ttm | REAL | 市盈率（TTM） |
| pb | REAL | 市净率 |
| total_mv | REAL | 总市值（万元） |
| circ_mv | REAL | 流通市值（万元） |
| turnover_rate | REAL | 换手率（%） |
| volume_ratio | REAL | 量比 |
| dv_ratio | REAL | 股息率（%） |
| dv_ttm | REAL | 股息率（TTM，%） |
| total_share | REAL | 总股本（万股） |
| float_share | REAL | 流通股本（万股） |
| free_share | REAL | 自由流通股本（万股） |

✅ 148,562 条 | **API**: `daily_basic` | **选股权重**: ⭐⭐⭐⭐⭐

### adj_factor — 复权因子

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| trade_date | TEXT | 交易日期 |
| adj_factor | REAL | 复权因子 |

✅ 149,134 条 | **API**: `adj_factor`

### stk_limit — 每日涨跌停价格

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| trade_date | TEXT | 交易日期 |
| up_limit | REAL | 涨停价 |
| down_limit | REAL | 跌停价 |
| pre_close | REAL | 昨日收盘价 |

✅ 205,552 条 | **API**: `stk_limit`

### suspen_d — 每日停复牌信息

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| trade_date | TEXT | 交易日期 |
| suspend_timing | TEXT | 停复牌时间 |
| suspend_type | TEXT | S=停牌, R=复牌 |

✅ 15 条 | **API**: `suspend_d`

### stk_shock — 个股异常波动

✅ 68 条 | **API**: `stk_shock`

### stk_high_shock — 个股严重异常波动

✅ 1 条 | **API**: `stk_high_shock`

---

## 资金流向

### moneyflow — 个股资金流向（核心）

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | TEXT | 股票代码 |
| date | TEXT | 交易日期 |
| buy_sm_amount | REAL | 小单买入额（万元，<4万） |
| sell_sm_amount | REAL | 小单卖出额 |
| buy_md_amount | REAL | 中单买入额（4~20万） |
| sell_md_amount | REAL | 中单卖出额 |
| buy_lg_amount | REAL | 大单买入额（20~100万） |
| sell_lg_amount | REAL | 大单卖出额 |
| buy_elg_amount | REAL | 超大单买入额（>100万） |
| sell_elg_amount | REAL | 超大单卖出额 |
| net_mf_amount | REAL | 净流入额（万元，正=流入） |

✅ 140,094 条 | **API**: `moneyflow` | **策略**: 主力资金

### moneyflow_hsgt — 沪深港通资金流向

✅ 26 条 | **API**: `moneyflow_hsgt`

### 其他资金流向表

| 表名 | 状态 | API |
|------|------|-----|
| moneyflow_ths | ⬜ 0条 | `moneyflow_ths` |
| moneyflow_dc | ⬜ 0条 | `moneyflow_dc` |
| moneyflow_cnt_ths | ⬜ 0条 | `moneyflow_cnt_ths` |
| moneyflow_ind_ths | ⬜ 0条 | `moneyflow_ind_ths` |
| moneyflow_ind_dc | ⬜ 0条 | `moneyflow_ind_dc` |
| moneyflow_mkt_dc | ✅ 1条 | `moneyflow_mkt_dc` |

---

## 沪深港通

### hk_hold — 沪深股通持股明细

⬜ 0 条 | **API**: `hk_hold` | **策略**: 北向资金

### hsgt_top10 — 沪深股通十大成交股

✅ 620 条 | **API**: `hsgt_top10`

### hs_const — 沪深港通成分股

⬜ 0 条 | **API**: `hs_const`

---

## 两融

### margin_detail — 融资融券交易明细

✅ 113,398 条 | **API**: `margin_detail`

### margin — 融资融券交易汇总

⬜ 0 条 | **API**: `margin`

### margin_secs — 融资融券标的

⬜ 0 条 | **API**: `margin_secs`

### slb_sec — 转融券交易汇总

⬜ 0 条 | **API**: `slb_sec`

### slb_len — 转融资交易汇总

⬜ 0 条 | **API**: `slb_len`

---

## 涨跌停/龙虎榜

### limit_list — 涨跌停及炸板数据

✅ 3,951 条 | **API**: `limit_list_d` | **策略**: 涨停洗盘

### top_list — 龙虎榜交易明细

✅ 3,086 条 | **API**: `top_list`

### top_inst — 龙虎榜机构交易明细

✅ 1,000 条 | **API**: `top_inst` | **策略**: 机构追踪

### limit_list_ths — THS涨跌停榜单

⬜ 0 条 | **API**: `limit_list_ths`

### limit_step — 涨停股票连板天梯

⬜ 0 条 | **API**: `limit_step`

### limit_cpt_list — 涨停最强板块统计

⬜ 0 条 | **API**: `limit_cpt_list`

### block_trade — 大宗交易

✅ 4,651 条 | **API**: `block_trade`

---

## 财务数据

| 表名 | 列数 | 状态 | API | 说明 |
|------|------|------|-----|------|
| income | 18 | ⬜ 0条 | `income` | 利润表 |
| balancesheet | 26 | ⬜ 0条 | `balancesheet` | 资产负债表 |
| cashflow | 13 | ⬜ 0条 | `cashflow` | 现金流量表 |
| fina_indicator | 20 | ⬜ 0条 | `fina_indicator` | 财务指标（ROE/ROA/毛利率等） |
| forecast | 10 | ⬜ 0条 | `forecast` | 业绩预告 |
| express | 13 | ⬜ 0条 | `express` | 业绩快报 |
| fina_mainbz | 6 | ⬜ 0条 | `fina_mainbz` | 主营业务构成 |
| disclosure_date | 5 | ⬜ 0条 | `disclosure_date` | 财报披露日期表 |

---

## 股东/分红/质押

| 表名 | 状态 | API | 说明 |
|------|------|-----|------|
| dividend | ⬜ 0条 | `dividend` | 分红送股 |
| stk_holdertrade | ⬜ 0条 | `stk_holdertrade` | 股东增减持 |
| stk_holdernumber | ⬜ 0条 | `stk_holdernumber` | 股东人数 |
| pledge_stat | ⬜ 0条 | `pledge_stat` | 股权质押统计 |
| pledge_detail | ⬜ 0条 | `pledge_detail` | 股权质押明细 |
| share_float | ⬜ 0条 | `share_float` | 限售股解禁 |
| repurchase | ⬜ 0条 | `repurchase` | 股票回购 |
| top10_holders | ⬜ 0条 | `top10_holders` | 前十大股东 |
| top10_floatholders | ⬜ 0条 | `top10_floatholders` | 前十大流通股东 |

---

## 打板/概念/板块

| 表名 | 状态 | API | 说明 |
|------|------|-----|------|
| dc_concept | ✅ 609条 | `dc_concept` | DC题材数据 |
| dc_concept_cons | ⬜ 0条 | `dc_concept_cons` | DC题材成分 |
| dc_daily | ⬜ 0条 | `dc_daily` | DC概念板块行情 |
| dc_index | ⬜ 0条 | `dc_index` | DC概念板块分类 |
| dc_member | ⬜ 0条 | `dc_member` | DC概念板块成分 |
| ths_daily | ⬜ 0条 | `ths_daily` | THS概念板块行情 |
| ths_index | ⬜ 0条 | `ths_index` | THS概念板块分类 |
| ths_member | ⬜ 0条 | `ths_member` | THS概念板块成分 |
| tdx_daily | ⬜ 0条 | `tdx_daily` | TDX概念板块行情 |
| tdx_index | ⬜ 0条 | `tdx_index` | TDX概念板块分类 |
| tdx_member | ⬜ 0条 | `tdx_member` | TDX概念板块成分 |
| kpl_list | ⬜ 0条 | `kpl_list` | KP榜单数据 |
| kpl_concept_cons | ⬜ 0条 | `kpl_concept_cons` | KP题材成分 |
| stk_auction | ⬜ 0条 | `stk_auction` | 开盘竞价成交 |

---

## 热榜/游资

| 表名 | 状态 | API |
|------|------|-----|
| ths_hot | ⬜ 0条 | `ths_hot` |
| dc_hot | ⬜ 0条 | `dc_hot` |
| hm_list | ⬜ 0条 | `hm_list`（游资名录） |
| hm_detail | ⬜ 0条 | `hm_detail`（游资每日明细） |

---

## 技术因子

| 表名 | 列数 | 状态 | API |
|------|------|------|-----|
| stk_factor | 11 | ⬜ 0条 | `stk_factor`（MACD/KDJ/RSI） |
| cyq_perf | 9 | ⬜ 0条 | `cyq_perf`（筹码分布及胜率） |
| index_weight | 4 | ⬜ 0条 | `index_weight`（指数成分权重） |

---

## 中央结算/其他

| 表名 | 状态 | API |
|------|------|-----|
| ccass_hold | ⬜ 0条 | `ccass_hold` |
| ccass_hold_detail | ⬜ 0条 | `ccass_hold_detail` |
| report_rc | ⬜ 0条 | `report_rc`（券商盈利预测） |
| stk_nineturn | ⬜ 0条 | `stk_nineturn`（神奇九转） |
| stk_ah_comparison | ⬜ 0条 | `stk_ah_comparison`（AH股比价） |

---

## 港股通

| 表名 | 状态 | API |
|------|------|-----|
| ggt_top10 | ⬜ 0条 | `ggt_top10`（港股通十大成交股） |
| ggt_daily | ⬜ 0条 | `ggt_daily`（港股通每日成交统计） |

---

## 数据汇总

| 状态 | 表数 | 说明 |
|------|------|------|
| ✅ **有数据** | 17 | stock_daily / daily_basic / moneyflow / stk_limit / adj_factor / margin_detail / limit_list / top_list / top_inst / block_trade / hsgt_top10 / suspen_d / stk_shock / stk_high_shock / moneyflow_hsgt / moneyflow_mkt_dc / dc_concept / stock_basic / trade_cal |
| ⬜ **无数据**（待回填） | 73 | 财务报表 / 股东 / 概念 / 板块 / 热榜 / 游资 等 |

### 同步命令

```bash
# 全量同步（自动补齐 60 个交易日）
python main.py

# 单表同步
python main.py --sync-table daily_basic --date 20260610
python main.py --sync-table limit_list --date 20260610
python main.py --sync-table margin_detail --date 20260610
```

### 常用查询

```sql
-- 最近交易日
SELECT cal_date FROM trade_cal WHERE is_open=1 ORDER BY cal_date DESC LIMIT 60;

-- 某日涨停股
SELECT * FROM limit_list WHERE date='20260610' AND limit_type='U';

-- 主力净流入 top10
SELECT symbol, SUM(net_mf_amount) total FROM moneyflow
WHERE date='20260610' GROUP BY symbol ORDER BY total DESC LIMIT 10;

-- 全市场 PE 分布
SELECT CASE WHEN pe_ttm<10 THEN '<10' WHEN pe_ttm<30 THEN '10-30'
  WHEN pe_ttm<50 THEN '30-50' ELSE '>50' END pe_range,
  COUNT(*) stocks FROM daily_basic WHERE date='20260610' AND pe_ttm>0
  GROUP BY pe_range;
```
