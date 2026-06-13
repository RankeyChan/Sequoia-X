import pandas as pd
from sequoia_x.strategy.base import BaseStrategy
from sequoia_x.strategy.filters import FundamentalFilter
from sequoia_x.core.logger import get_logger

logger = get_logger(__name__)

class RpsBreakoutStrategy(BaseStrategy):
    """RPS 极强动量突破策略"""

    webhook_key: str = "rps"
    name_cn: str = "RPS突破"
    rps_period: int = 120
    rps_threshold: int = 90

    def run(self) -> list[str]:
        try:
            df = self.engine.query("SELECT ts_code, trade_date, close, high FROM ts_daily")
        except Exception as exc:
            logger.error(f"读取数据库失败: {exc}")
            return []

        if df.empty:
            return []

        df['trade_date'] = pd.to_datetime(df['trade_date'], format='mixed')
        df = df.sort_values(['ts_code', 'trade_date'])

        # 纵向计算涨幅
        df['close_shift'] = df.groupby('ts_code')['close'].shift(self.rps_period)
        df['pct_change'] = (df['close'] - df['close_shift']) / df['close_shift']

        latest_date = df['trade_date'].max()
        latest_df = df[df['trade_date'] == latest_date].copy()
        latest_df = latest_df.dropna(subset=['pct_change'])

        # 横向排位 (RPS)
        latest_df['rps'] = latest_df['pct_change'].rank(pct=True) * 100
        strong_stocks = latest_df[latest_df['rps'] >= self.rps_threshold].copy()

        # 计算滚动最高价
        roll_high = df.groupby('ts_code')['high'].rolling(
            window=self.rps_period, min_periods=self.rps_period // 2
        ).max().reset_index(level=0, drop=True)
        df['roll_high'] = roll_high

        latest_roll_high = df[df['trade_date'] == latest_date][['ts_code', 'roll_high']]
        strong_stocks = strong_stocks.merge(latest_roll_high, on='ts_code')

        # 突破判定
        breakout_condition = strong_stocks['close'] >= strong_stocks['roll_high'] * 0.90
        selected = strong_stocks[breakout_condition]

        symbols = selected['ts_code'].tolist()

        # 基本面前置过滤
        if symbols and self.engine.tushare:
            f_filter = FundamentalFilter(self.engine)
            symbols = f_filter.apply_defaults(symbols)

        logger.info(f"RpsBreakoutStrategy 选出 {len(symbols)} 只股票")
        return symbols