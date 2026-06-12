"""Sequoia-X V2 主程序入口（Tushare 唯一数据源）。

运行模式：
  python main.py                        # 日常模式：Tushare 全量数据同步 + 19策略 + 飞书推送
  python main.py --date 20260610        # 指定日期执行（同步 + 策略 + 推送）
  python main.py --no-sync --date 20260610  # 用当前 DB 数据，指定日期窗口执行策略
  python main.py --backfill             # 回填模式：全量历史数据回填
  python main.py --backfill --start 2026-01-01  # 指定回填起始日期
  python main.py --no-sync              # 跳过同步，直接用现有 DB 数据执行策略并推送
  python main.py --no-sync --strategy limit_up_shakeout  # 只跑指定策略
"""

import argparse
import re
import sys
from datetime import date
from dotenv import load_dotenv
load_dotenv()

import socket
socket.setdefaulttimeout(10.0)

from sequoia_x.core.config import get_settings
from sequoia_x.core.logger import get_logger
from sequoia_x.data.engine import DataEngine
from sequoia_x.notify.feishu import FeishuNotifier
from sequoia_x.strategy.base import BaseStrategy
from sequoia_x.strategy.high_tight_flag import HighTightFlagStrategy
from sequoia_x.strategy.institutional import InstitutionalStrategy
from sequoia_x.strategy.limit_up_shakeout import LimitUpShakeoutStrategy
from sequoia_x.strategy.ma_volume import MaVolumeStrategy
from sequoia_x.strategy.money_flow import MoneyFlowStrategy
from sequoia_x.strategy.north_bound import NorthBoundStrategy
from sequoia_x.strategy.private_placement import PrivatePlacementStrategy
from sequoia_x.strategy.rps_breakout import RpsBreakoutStrategy
from sequoia_x.strategy.turtle_trade import TurtleTradeStrategy
from sequoia_x.strategy.uptrend_limit_down import UptrendLimitDownStrategy
# 新策略
from sequoia_x.strategy.pe_roe_value import PeRoeValueStrategy
from sequoia_x.strategy.earnings_surprise import EarningsSurpriseStrategy
from sequoia_x.strategy.trend_momentum import TrendMomentumStrategy
from sequoia_x.strategy.north_bound_money import NorthBoundMoneyStrategy
from sequoia_x.strategy.high_dividend import HighDividendStrategy
from sequoia_x.strategy.sector_rotation import SectorRotationStrategy
from sequoia_x.strategy.volume_drawdown import VolumeDrawdownStrategy
from sequoia_x.strategy.fundamental_multifactor import FundamentalMultifactorStrategy
from sequoia_x.strategy.sector_momentum import SectorMomentumStrategy


def _match_strategies(args_strategy: str, all_strategies: list[BaseStrategy]) -> list[BaseStrategy]:
    """按用户输入匹配策略列表（支持 CamelCase / snake_case / webhook_key）。"""
    target_keys = set(k.strip().lower() for k in args_strategy.split(","))
    matched = []
    for s in all_strategies:
        s_name = type(s).__name__
        s_key = s.webhook_key
        s_snake = re.sub(r'(?<!^)(?=[A-Z])', '_', s_name).lower()
        s_snake_short = s_snake.replace("_strategy", "")
        if (s_name.lower() in target_keys
            or s_key in target_keys
            or s_snake_short in target_keys
            or any(t in s_name.lower() for t in target_keys)):
            matched.append(s)
    return matched


def main() -> None:
    parser = argparse.ArgumentParser(description="Sequoia-X V2 选股系统（Tushare）")
    parser.add_argument(
        "--backfill",
        action="store_true",
        help="回填模式：全量历史数据（K线+指标+资金流向+涨跌停+北向资金）",
    )
    parser.add_argument(
        "--start",
        type=str,
        default=None,
        help="回填起始日期（YYYYMMDD 或 YYYY-MM-DD），如 2026-01-01",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="执行日期（YYYYMMDD），默认当天。影响数据同步和策略选股的日期窗口",
    )
    parser.add_argument(
        "--no-sync",
        action="store_true",
        help="跳过数据同步，直接用现有数据库执行策略并推送飞书",
    )
    parser.add_argument(
        "--sync-table",
        type=str,
        default=None,
        help="只同步指定表（如 daily_basic, moneyflow, adj_factor, stk_limit），不跑策略",
    )
    parser.add_argument(
        "--strategy",
        type=str,
        default=None,
        help="只运行指定策略（支持类名/snake_case/webhook_key，逗号分隔多个）",
    )
    args = parser.parse_args()

    try:
        # 1. 初始化
        settings = get_settings()
        logger = get_logger(__name__)
        logger.info("Sequoia-X V2 启动 (Tushare)")

        engine = DataEngine(settings)

        # ── 单表同步模式 ──
        if args.sync_table:
            trade_date = args.date or date.today().strftime("%Y%m%d")
            logger.info(f"单表同步: {args.sync_table} (日期: {trade_date})")
            result = engine.sync_table(args.sync_table, trade_date)
            logger.info(f"同步结果: {result}")
            return

        # ── 回填模式 ──
        if args.backfill:
            start = args.start or settings.start_date
            logger.info(f"进入回填模式（起始日期: {start}）...")
            engine.backfill_tushare(start)
            logger.info("回填完成")
            return

        # ── 日常模式 ──
        trade_date = args.date or date.today().strftime("%Y%m%d")
        engine.target_date = trade_date

        if args.no_sync:
            logger.info(f"--no-sync 模式：跳过数据同步，直接用现有数据执行策略（日期: {trade_date}）")
        else:
            logger.info(f"交易日期: {trade_date}")

            if not engine.is_trading_day(trade_date):
                logger.info(f"{trade_date} 非交易日，退出")
                return

            logger.info("开始 Tushare 全量数据同步...")
            counts = engine.sync_today(trade_date)
            logger.info(f"数据同步完成: {counts}")

        # 策略列表
        all_strategies: list[BaseStrategy] = [
            # 技术面（6个）
            MaVolumeStrategy(engine=engine, settings=settings),
            TurtleTradeStrategy(engine=engine, settings=settings),
            HighTightFlagStrategy(engine=engine, settings=settings),
            LimitUpShakeoutStrategy(engine=engine, settings=settings),
            UptrendLimitDownStrategy(engine=engine, settings=settings),
            RpsBreakoutStrategy(engine=engine, settings=settings),
            # 资金/机构（3个）
            MoneyFlowStrategy(engine=engine, settings=settings),
            NorthBoundStrategy(engine=engine, settings=settings),
            InstitutionalStrategy(engine=engine, settings=settings),
            # 事件驱动（1个）
            PrivatePlacementStrategy(engine=engine, settings=settings),
            # 新增策略（8个）
            PeRoeValueStrategy(engine=engine, settings=settings),
            EarningsSurpriseStrategy(engine=engine, settings=settings),
            TrendMomentumStrategy(engine=engine, settings=settings),
            NorthBoundMoneyStrategy(engine=engine, settings=settings),
            HighDividendStrategy(engine=engine, settings=settings),
            SectorRotationStrategy(engine=engine, settings=settings),
            SectorMomentumStrategy(engine=engine, settings=settings),
            VolumeDrawdownStrategy(engine=engine, settings=settings),
            FundamentalMultifactorStrategy(engine=engine, settings=settings),
        ]

        if args.strategy:
            strategies = _match_strategies(args.strategy, all_strategies)
            if not strategies:
                logger.error(f"未找到匹配策略: {args.strategy}")
                available = [f"{type(s).__name__}/{s.webhook_key}" for s in all_strategies]
                logger.info(f"可用策略: {available}")
                return
            logger.info(f"只运行策略: {[type(s).__name__ for s in strategies]}")
        else:
            strategies = all_strategies

        # 执行策略 + 推送
        notifier = FeishuNotifier(settings, engine=engine, trade_date=trade_date)

        for strategy in strategies:
            # 优先使用中文名称，降级到类名
            strategy_name = getattr(strategy, "name_cn", "") or type(strategy).__name__
            logger.info(f"执行策略：{strategy_name}")

            selected: list[str] = strategy.run()
            logger.info(f"{strategy_name} 选出 {len(selected)} 只股票")

            if selected:
                notifier.send(
                    symbols=selected,
                    strategy_name=strategy_name,
                    webhook_key=strategy.webhook_key,
                )
            else:
                logger.info(f"{strategy_name} 无选股结果，跳过推送")

    except Exception:
        try:
            _logger = get_logger(__name__)
            _logger.exception("主流程发生未捕获异常，程序终止")
        except Exception:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    logger.info("Sequoia-X V2 运行完成")


if __name__ == "__main__":
    main()
