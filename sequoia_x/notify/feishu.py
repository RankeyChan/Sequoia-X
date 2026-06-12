"""飞书通知模块：将选股结果通过 Webhook 推送至飞书群。

使用本地 stock_basic 表查询股票名称、PE、行业等信息，快速构建推送卡片。
"""

import json
from datetime import date

import requests

from sequoia_x.core.config import Settings
from sequoia_x.core.logger import get_logger

logger = get_logger(__name__)


class FeishuNotifier:
    """飞书 Webhook 推送器（Tushare 增强版）。

    根据策略的 webhook_key 路由到对应的飞书机器人。
    若 webhook_key 未在 Settings.strategy_webhooks 中配置，
    则 fallback 到 Settings.feishu_webhook_url。

    推送卡片包含：股票名称、PE、行业、市值、资金流向等丰富信息。
    """

    def __init__(self, settings, engine=None, trade_date=""):
        """初始化 FeishuNotifier。

        Args:
            settings: Settings 实例。
            engine: DataEngine 实例，用于查询股票元数据。
            trade_date: 策略执行日期 (YYYYMMDD)，用于卡片日期显示。
        """
        self.settings = settings
        self.engine = engine
        self.trade_date = trade_date or date.today().strftime("%Y%m%d")

    @staticmethod
    def _to_xueqiu_code(code: str) -> str:
        """将纯数字代码转为雪球格式：6开头→SH，4/8开头→BJ，其余→SZ。"""
        if code.startswith("6"):
            return f"SH{code}"
        elif code.startswith(("4", "8")):
            return f"BJ{code}"
        return f"SZ{code}"

    def _get_stock_names(self, symbols: list[str]) -> dict[str, str]:
        """从本地 stock_basic 表批量查询股票名称。"""
        if self.engine:
            return self.engine.get_stock_names(symbols)
        return {}

    def _build_market_overview(self) -> str:
        """构建市场概览文本。"""
        if not self.engine or not self.engine.tushare:
            return ""

        overview = self.engine.tushare.get_market_overview(self.trade_date)
        if not overview:
            return ""

        parts = []
        if "sh_close" in overview:
            parts.append(
                f"上证: {overview['sh_close']:.2f} ({overview.get('sh_pct', 0):+.2f}%)"
            )
        if "sz_close" in overview:
            parts.append(
                f"深证: {overview['sz_close']:.2f} ({overview.get('sz_pct', 0):+.2f}%)"
            )
        if "north_net" in overview:
            north_b = overview["north_net"] / 1e4
            parts.append(f"北向资金净流入: {north_b:.1f}亿")

        return " | ".join(parts) if parts else ""

    def _format_stock_text(self, symbols: list[str], names: dict[str, str],
                            metas: dict[str, dict]) -> str:
        """将股票列表格式化为对齐的表格文本（使用等宽字体保持对齐）。"""
        lines: list[str] = []
        for code in symbols:
            xq_code = self._to_xueqiu_code(code)
            name = names.get(code, code)
            stock = f"[{name}({code})](https://xueqiu.com/S/{xq_code})"
            meta = metas.get(code)

            pe = f"{meta['pe_ttm']:.1f}" if (meta and meta.get("pe_ttm") and meta["pe_ttm"] > 0) else "-"
            industry = meta.get("industry", "-") if (meta and meta.get("industry") and meta["industry"] not in ("", "None")) else "-"
            mv = f"{meta['circ_mv']/1e4:.0f}亿" if (meta and meta.get("circ_mv") and meta["circ_mv"] > 0) else "-"
            mf = "-"
            if meta and meta.get("net_mf_amount") and meta["net_mf_amount"] != 0:
                val = meta["net_mf_amount"] / 1e4
                direction = "流入" if val > 0 else "流出"
                mf = f"主力{direction}{abs(val):.1f}亿"

            lines.append(f"`{stock}  PE:{pe}  {industry}  {mv}  {mf}`")
        return "\n".join(lines)

    def _build_card(self, symbols: list[str], strategy_name: str) -> dict:
        today = f"{self.trade_date[:4]}-{self.trade_date[4:6]}-{self.trade_date[6:8]}"
        names = self._get_stock_names(symbols)

        stock_metas: dict[str, dict] = {}
        if self.engine and self.engine.tushare:
            stock_metas = self.engine.get_stock_meta_batch(symbols)

        # 构建卡片正文
        content = (
            f"**日期：** {today}\n"
            f"**策略：** {strategy_name}\n"
            f"**选股数量：** {len(symbols)}"
        )

        if symbols:
            content += "\n"
            stock_text = self._format_stock_text(symbols, names, stock_metas)
            content += "\n" + stock_text

        market_text = self._build_market_overview()
        if market_text:
            content += f"\n\n📊 **今日市场概览：**\n{market_text}"

        return {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": f"📈 Sequoia-X 选股播报 | {strategy_name}",
                    },
                    "template": "blue",
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": content,
                        },
                    },
                ],
            },
        }

    def send(
        self,
        symbols: list[str],
        strategy_name: str,
        webhook_key: str = "default",
    ) -> None:
        """将选股结果格式化为飞书卡片消息并 POST 至对应 Webhook。

        Args:
            symbols: 选股结果代码列表。
            strategy_name: 策略名称，用于卡片标题。
            webhook_key: 策略标识，用于路由到对应飞书机器人。

        Raises:
            不抛出异常，HTTP 失败时记录 ERROR 日志。
        """
        url = self.settings.get_webhook_url(webhook_key)
        payload = self._build_card(symbols, strategy_name)

        try:
            resp = requests.post(
                url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            resp_json = resp.json()

            if resp.status_code != 200 or resp_json.get("code") != 0:
                logger.error(
                    f"飞书推送失败 [{webhook_key}] "
                    f"HTTP状态={resp.status_code} 飞书响应={resp.text}"
                )
            else:
                logger.info(f"飞书推送成功 [{webhook_key}]，共 {len(symbols)} 只股票")

        except requests.RequestException as exc:
            logger.error(f"飞书推送请求异常 [{webhook_key}]：{exc}")
