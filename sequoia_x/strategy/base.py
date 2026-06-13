"""策略基类模块：定义所有选股策略的抽象接口。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from sequoia_x.core.config import Settings

if TYPE_CHECKING:
    from sequoia_x.data.mysql_engine import MySQLEngine


class BaseStrategy(ABC):
    """选股策略抽象基类。

    所有具体策略必须继承此类并实现 run() 方法。

    Attributes:
        webhook_key: 策略对应的飞书 webhook 标识，用于路由到不同机器人。
        name_cn: 策略中文名称，用于飞书推送显示。
    """

    webhook_key: str = "default"
    name_cn: str = ""

    def __init__(self, engine: MySQLEngine, settings: Settings) -> None:
        """
        初始化策略。

        Args:
            engine: MySQLEngine 实例，用于读取行情数据。
            settings: Settings 实例，用于读取配置。
        """
        self.engine = engine
        self.settings = settings

    @abstractmethod
    def run(self) -> list[str]:
        """
        执行选股逻辑，返回选中的股票代码列表。

        Returns:
            满足策略条件的股票代码列表，如 ['000001', '600519']。
            无选股结果时返回空列表。
        """
        ...
