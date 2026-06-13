"""策略引擎属性测试。"""

from unittest.mock import MagicMock, patch

import pandas as pd
from hypothesis import given, settings as h_settings
from hypothesis import strategies as st

from sequoia_x.core.config import Settings
from sequoia_x.strategy.ma_volume import MaVolumeStrategy


def _mock_engine():
    """创建 mock MySQLEngine，避免真实 MySQL 连接。"""
    engine = MagicMock()
    engine.get_all_symbols = MagicMock()
    engine.get_ohlcv = MagicMock(return_value=pd.DataFrame())
    engine.fetch_all = MagicMock(return_value=[])
    engine.fetch_one = MagicMock(return_value=None)
    engine.query = MagicMock(return_value=pd.DataFrame())
    engine.tushare = None
    return engine


# Feature: sequoia-x-v2, Property 9: 策略 run() 返回值类型正确
@given(
    symbols=st.lists(
        st.text(min_size=6, max_size=6, alphabet="0123456789"),
        min_size=0, max_size=3, unique=True,
    )
)
@h_settings(max_examples=30, deadline=None)
def test_strategy_run_returns_list_of_str(symbols: list[str]) -> None:
    """属性 9：run() 应返回 list[str]，每个元素为非空字符串。"""
    settings = Settings(
        start_date="2024-01-01",
        feishu_webhook_url="https://example.com/hook",
    )
    engine = _mock_engine()
    engine.get_all_symbols.return_value = symbols

    strategy = MaVolumeStrategy(engine=engine, settings=settings)
    result = strategy.run()

    assert isinstance(result, list)
    assert all(isinstance(s, str) and len(s) > 0 for s in result)
