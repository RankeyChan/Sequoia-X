# Sequoia-X: 王者回归 | The King Returns

> A 股量化选股系统 V3 | A-Share Quantitative Stock Selection System V3  
> 数据源: [Tushare Pro](https://tushare.pro)（2000+ 积分）

---

## 简介 | Introduction

Sequoia-X V3 是基于 Tushare 的 A 股量化选股系统。每天收盘后自动拉取全市场数据，执行 10 个策略，选股结果推送至飞书群。

**核心特性：**
- **Tushare 唯一数据源**：K 线、基本面、资金流向、涨跌停、北向资金、龙虎榜一站式覆盖
- **全市场单次 API 调用**：`daily(trade_date)` 一次获取当日所有股票日 K 线（~5000 条）
- **回填速度**：120 个交易日完整数据回填约 5 分钟（vs baostock 的 5 小时）
- **OOP 架构**：策略抽象基类 + 向量化计算 + 本地 SQLite 存储

---

## 快速开始 | Quick Start

### 1. 安装依赖

```bash
uv sync
```

### 2. 配置

```bash
cp .env.example .env
# 编辑 .env，填写 TUSHARE_TOKEN 和 FEISHU_WEBHOOK_URL
```

### 3. 首次回填历史数据

```bash
python main.py --backfill --start 2026-01-01
```

约 5 分钟完成全市场数据回填（K 线 + PE/PB/市值 + 资金流向 + 涨跌停 + 北向资金 + 龙虎榜）。

### 4. 日常运行

```bash
python main.py                     # 全量数据同步 + 10策略 + 飞书推送
python main.py --no-sync           # 跳过同步，直接用现有数据跑策略
python main.py --strategy turtle_trade  # 只跑指定策略
```

---

## CLI 用法

```bash
python main.py                     # 日常模式：Tushare 全量同步 + 10策略 + 飞书推送
python main.py --backfill          # 回填模式：全量历史数据
python main.py --backfill --start 2026-01-01  # 指定起始日期
python main.py --no-sync           # 跳过同步，直接执行策略并推送
python main.py --no-sync --strategy limit_up_shakeout  # 指定策略
```

---

## 内置策略 | Strategies

### 技术面策略
| 策略 | 说明 | 数据依赖 |
|------|------|---------|
| **TurtleTrade** | 海龟突破：20日新高 + 成交额过亿 + 阳线防诱多 + 市值排序 | stock_daily + daily_basic |
| **MaVolume** | 均线金叉：5日均线上穿20日均线 + 成交量放大 | stock_daily |
| **HighTightFlag** | 高窄旗形：强动量后极度收敛缩量整理 | stock_daily |
| **LimitUpShakeout** | 涨停洗盘：真实涨停 + 放量收阴 + 支撑不破 | stock_daily + limit_list |
| **UptrendLimitDown** | 上升趋势跌停：趋势中放量跌停捕捉错杀 | stock_daily |
| **RpsBreakout** | 欧奈尔 RPS 相对强度突破 | stock_daily |

### 资金面策略
| 策略 | 说明 | 数据依赖 |
|------|------|---------|
| **MoneyFlow** | 主力资金持续流入 + 散户流出 | stock_daily + moneyflow |
| **NorthBound** | 北向资金持续增持 | stock_daily + hk_hold |
| **Institutional** | 龙虎榜机构买入 + 机构调研 | stock_daily + top_list + top_inst |

### 事件驱动策略
| 策略 | 说明 |
|------|------|
| **PrivatePlacement** | 定增公告监控（基于 akshare） |

---

## 数据库表

| 表名 | 说明 | 来源 |
|------|------|------|
| `stock_daily` | 日K线行情（后复权） | Tushare daily |
| `stock_basic` | 股票基础信息（名称/行业） | Tushare stock_basic |
| `daily_basic` | 每日指标（PE/PB/市值/换手率） | Tushare daily_basic |
| `moneyflow` | 个股资金流向（小/中/大/超大单） | Tushare moneyflow |
| `limit_list` | 涨跌停及炸板数据 | Tushare limit_list_d |
| `hk_hold` | 北向资金持股明细 | Tushare hk_hold |
| `top_list` | 龙虎榜每日交易明细 | Tushare top_list |
| `top_inst` | 龙虎榜机构交易明细 | Tushare top_inst |
| `margin_detail` | 融资融券交易明细 | Tushare margin_detail |
| `trade_cal` | 交易日历 | Tushare trade_cal |

---

## 目录结构

```
Sequoia-X/
├── main.py                      # 入口
├── pyproject.toml               # 依赖 + 配置
├── .env.example                 # 环境变量模板
├── data/                        # SQLite 数据库
├── sequoia_x/
│   ├── core/
│   │   ├── config.py            # 配置管理
│   │   └── logger.py            # 日志
│   ├── data/
│   │   ├── tushare_provider.py  # Tushare API 封装
│   │   └── engine.py            # 数据引擎（SQLite + 同步调度）
│   ├── strategy/
│   │   ├── base.py              # 策略抽象基类
│   │   ├── filters.py           # 基本面过滤器
│   │   ├── turtle_trade.py / ma_volume.py / ... # 10个策略
│   └── notify/
│       └── feishu.py            # 飞书推送
└── tests/
```

---

## 许可证 | License

MIT
