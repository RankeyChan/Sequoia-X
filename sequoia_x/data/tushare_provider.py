"""Tushare 数据提供者：基于官方 tushare SDK。

支持通过代理访问（tushare_proxy_url 配置），自动关闭环境代理避免冲突。
"""

import os
from typing import Any

import pandas as pd

from sequoia_x.core.logger import get_logger

logger = get_logger(__name__)


class TushareProvider:
    """Tushare 数据提供者（官方 SDK 封装）。

    封装 ts.pro_api()，支持代理配置和数据抽取接口。
    所有 get_* 方法返回统一格式：带 symbol 列的 DataFrame。

    Attributes:
        token: Tushare API token。
        proxy_url: 代理地址（可选）。
    """

    def __init__(
        self,
        token: str,
        proxy_url: str = "",
    ) -> None:
        self.token = token

        # 关闭环境代理，防止与 Tushare SDK 内置请求冲突
        for k in [
            "HTTP_PROXY", "HTTPS_PROXY",
            "http_proxy", "https_proxy",
            "ALL_PROXY", "all_proxy",
        ]:
            os.environ.pop(k, None)

        import tushare as ts

        self._pro = ts.pro_api(token)
        self._pro._DataApi__http_url = (
            proxy_url or "http://api.tushare.pro"
        )

        logger.info(
            f"TushareProvider 初始化完成"
            + (f" (代理: {proxy_url})" if proxy_url else "")
        )

    # ── 通用查询 ──

    def _call(self, api_name: str, **params: Any) -> pd.DataFrame:
        """调用 Tushare SDK 接口，返回 DataFrame。"""
        try:
            func = getattr(self._pro, api_name, None)
            if func is None:
                logger.error(f"Tushare SDK 无此接口: {api_name}")
                return pd.DataFrame()
            df = func(**{k: v for k, v in params.items() if v is not None and v != ""})
            if df is None or df.empty:
                return pd.DataFrame()
            return df
        except Exception as exc:
            logger.warning(f"Tushare [{api_name}] 调用失败: {exc}")
            return pd.DataFrame()

    @staticmethod
    def _extract_symbol(df: pd.DataFrame) -> pd.DataFrame:
        """从 ts_code 或 code 列提取纯数字 symbol。"""
        if df.empty:
            return df
        col = "ts_code" if "ts_code" in df.columns else ("code" if "code" in df.columns else None)
        if col:
            df["symbol"] = df[col].astype(str).str.extract(r"(\d{6})")
        return df

    # ── K 线行情 ──

    def get_daily(
        self, trade_date: str = "", ts_code: str = "",
        start_date: str = "", end_date: str = "",
    ) -> pd.DataFrame:
        params = dict(trade_date=trade_date, ts_code=ts_code,
                       start_date=start_date, end_date=end_date)
        df = self._call("daily", **params)
        return self._extract_symbol(df)

    def get_daily_batch(self, trade_dates: list[str]) -> pd.DataFrame:
        frames = []
        for i, td in enumerate(trade_dates):
            if (i + 1) % 50 == 0:
                logger.info(f"daily 进度: {i + 1}/{len(trade_dates)}")
            df = self.get_daily(trade_date=td)
            if not df.empty:
                frames.append(df)
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    # ── 基础数据 ──

    def get_stock_basic(self) -> pd.DataFrame:
        df = self._call("stock_basic", list_status="L")
        if not df.empty:
            df["symbol"] = df["ts_code"].str.extract(r"(\d{6})")
        return df

    def get_trade_cal(self, start_date: str, end_date: str) -> pd.DataFrame:
        return self._call("trade_cal", exchange="SSE",
                          start_date=start_date, end_date=end_date)

    # ── 每日指标 ──

    def get_daily_basic(self, trade_date: str) -> pd.DataFrame:
        df = self._call("daily_basic", trade_date=trade_date)
        return self._extract_symbol(df)

    def get_daily_basic_batch(self, trade_dates: list[str]) -> pd.DataFrame:
        frames = [self.get_daily_basic(td) for td in trade_dates if self.get_daily_basic(td) is not None and not self.get_daily_basic(td).empty]
        # simpler approach:
        frames = []
        for td in trade_dates:
            df = self.get_daily_basic(td)
            if not df.empty:
                frames.append(df)
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    # ── 资金流向 ──

    def get_moneyflow(self, trade_date: str) -> pd.DataFrame:
        df = self._call("moneyflow", trade_date=trade_date)
        return self._extract_symbol(df)

    def get_moneyflow_batch(self, trade_dates: list[str]) -> pd.DataFrame:
        frames = []
        for td in trade_dates:
            df = self.get_moneyflow(td)
            if not df.empty:
                frames.append(df)
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    # ── 涨跌停 ──

    def get_limit_list(self, trade_date: str) -> pd.DataFrame:
        df = self._call("limit_list_d", trade_date=trade_date)
        return self._extract_symbol(df)

    def get_limit_list_batch(self, trade_dates: list[str]) -> pd.DataFrame:
        frames = []
        for td in trade_dates:
            df = self.get_limit_list(td)
            if not df.empty:
                frames.append(df)
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    # ── 北向资金 ──

    def get_hk_hold(self, trade_date: str) -> pd.DataFrame:
        df = self._call("hk_hold", trade_date=trade_date)
        if df.empty:
            return df
        # 只保留 A 股（北向资金），排除港股
        if "exchange" in df.columns:
            df = df[df["exchange"].isin(["SH", "SZ"])].copy()
        if df.empty:
            return df
        df = self._extract_symbol(df)
        if "symbol" in df.columns:
            df = df.dropna(subset=["symbol"])
        return df

    def get_hk_hold_batch(self, trade_dates: list[str]) -> pd.DataFrame:
        frames = []
        for td in trade_dates:
            df = self.get_hk_hold(td)
            if not df.empty:
                frames.append(df)
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    # ── 龙虎榜 ──

    def get_top_list(self, trade_date: str) -> pd.DataFrame:
        df = self._call("top_list", trade_date=trade_date)
        return self._extract_symbol(df)

    def get_top_inst(self, trade_date: str) -> pd.DataFrame:
        df = self._call("top_inst", trade_date=trade_date)
        return self._extract_symbol(df)

    # ── 融资融券 ──

    def get_margin_detail(self, trade_date: str) -> pd.DataFrame:
        df = self._call("margin_detail", trade_date=trade_date)
        return self._extract_symbol(df)

    # ── 财务数据 ──

    def get_income(
        self, ts_code: str = "", period: str = "",
        start_date: str = "", end_date: str = "",
        report_type: str = "",
    ) -> pd.DataFrame:
        params = dict(ts_code=ts_code, period=period,
                       start_date=start_date, end_date=end_date,
                       report_type=report_type)
        df = self._call("income", **params)
        return self._extract_symbol(df)

    def get_balancesheet(
        self, ts_code: str = "", period: str = "",
        start_date: str = "", end_date: str = "",
        report_type: str = "",
    ) -> pd.DataFrame:
        params = dict(ts_code=ts_code, period=period,
                       start_date=start_date, end_date=end_date,
                       report_type=report_type)
        df = self._call("balancesheet", **params)
        return self._extract_symbol(df)

    def get_cashflow(
        self, ts_code: str = "", period: str = "",
        start_date: str = "", end_date: str = "",
        report_type: str = "",
    ) -> pd.DataFrame:
        params = dict(ts_code=ts_code, period=period,
                       start_date=start_date, end_date=end_date,
                       report_type=report_type)
        df = self._call("cashflow", **params)
        return self._extract_symbol(df)

    def get_forecast(
        self, ts_code: str = "", period: str = "",
        ann_date: str = "", start_date: str = "",
        end_date: str = "",
        forecast_type: str = "",
    ) -> pd.DataFrame:
        params = dict(ts_code=ts_code, period=period, ann_date=ann_date,
                       start_date=start_date, end_date=end_date)
        if forecast_type:
            params["type"] = forecast_type
        df = self._call("forecast", **params)
        return self._extract_symbol(df)

    def get_express(
        self, ts_code: str = "", period: str = "",
        ann_date: str = "", start_date: str = "",
        end_date: str = "",
    ) -> pd.DataFrame:
        params = dict(ts_code=ts_code, period=period, ann_date=ann_date,
                       start_date=start_date, end_date=end_date)
        df = self._call("express", **params)
        return self._extract_symbol(df)

    def get_fina_indicator(
        self, ts_code: str = "",
        start_date: str = "", end_date: str = "",
    ) -> pd.DataFrame:
        params = dict(ts_code=ts_code,
                       start_date=start_date, end_date=end_date)
        df = self._call("fina_indicator", **params)
        return self._extract_symbol(df)

    # ── 分红/股东 ──

    def get_dividend(
        self, ts_code: str = "", ann_date: str = "",
        ex_date: str = "", record_date: str = "",
        start_date: str = "", end_date: str = "",
    ) -> pd.DataFrame:
        params = dict(ts_code=ts_code, ann_date=ann_date, ex_date=ex_date,
                       record_date=record_date, start_date=start_date,
                       end_date=end_date)
        df = self._call("dividend", **params)
        return self._extract_symbol(df)

    def get_stk_holdertrade(
        self, ts_code: str = "", ann_date: str = "",
        start_date: str = "", end_date: str = "",
        trade_type: str = "", holder_type: str = "",
    ) -> pd.DataFrame:
        params = dict(ts_code=ts_code, ann_date=ann_date,
                       start_date=start_date, end_date=end_date,
                       trade_type=trade_type, holder_type=holder_type)
        df = self._call("stk_holdertrade", **params)
        return self._extract_symbol(df)

    def get_stk_holdernumber(
        self, ts_code: str = "", ann_date: str = "",
        start_date: str = "", end_date: str = "",
    ) -> pd.DataFrame:
        params = dict(ts_code=ts_code, ann_date=ann_date,
                       start_date=start_date, end_date=end_date)
        df = self._call("stk_holdernumber", **params)
        return self._extract_symbol(df)

    def get_pledge_stat(self, ts_code: str = "",
                        end_date: str = "") -> pd.DataFrame:
        df = self._call("pledge_stat", ts_code=ts_code, end_date=end_date)
        return self._extract_symbol(df)

    def get_share_float(
        self, ts_code: str = "", ann_date: str = "",
        start_date: str = "", end_date: str = "",
        float_date: str = "",
    ) -> pd.DataFrame:
        params = dict(ts_code=ts_code, ann_date=ann_date,
                       start_date=start_date, end_date=end_date,
                       float_date=float_date)
        df = self._call("share_float", **params)
        return self._extract_symbol(df)

    def get_block_trade(
        self, ts_code: str = "", trade_date: str = "",
        start_date: str = "", end_date: str = "",
    ) -> pd.DataFrame:
        params = dict(ts_code=ts_code, trade_date=trade_date,
                       start_date=start_date, end_date=end_date)
        df = self._call("block_trade", **params)
        return self._extract_symbol(df)

    def get_repurchase(
        self, ann_date: str = "",
        start_date: str = "", end_date: str = "",
    ) -> pd.DataFrame:
        params = dict(ann_date=ann_date, start_date=start_date,
                       end_date=end_date)
        df = self._call("repurchase", **params)
        return self._extract_symbol(df)

    # ══════════════════════════════════════════════════════════════════════
    # 10000+ 积分新增 — 涨跌停/筹码/股东/停复牌/审计/因子
    # ══════════════════════════════════════════════════════════════════════

    def get_stk_limit(self, trade_date: str = "",
                      ts_code: str = "", start_date: str = "",
                      end_date: str = "") -> pd.DataFrame:
        """获取每日涨跌停价格。"""
        params = dict(trade_date=trade_date, ts_code=ts_code,
                       start_date=start_date, end_date=end_date)
        df = self._call("stk_limit", **params)
        return self._extract_symbol(df)

    def get_cyq_perf(self, ts_code: str, trade_date: str = "",
                     start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """获取每日筹码分布及胜率。"""
        params = dict(ts_code=ts_code, trade_date=trade_date,
                       start_date=start_date, end_date=end_date)
        df = self._call("cyq_perf", **params)
        return self._extract_symbol(df)

    def get_cyq_chips(self, ts_code: str, trade_date: str = "",
                      start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """获取每日筹码分布明细（各价位占比）。"""
        params = dict(ts_code=ts_code, trade_date=trade_date,
                       start_date=start_date, end_date=end_date)
        df = self._call("cyq_chips", **params)
        return self._extract_symbol(df)

    def get_hsgt_top10(self, trade_date: str, market_type: str = "") -> pd.DataFrame:
        """获取沪深股通十大成交股。market_type: 1=沪市 3=深市（空=全部）。"""
        params = dict(trade_date=trade_date)
        if market_type:
            params["market_type"] = market_type
        df = self._call("hsgt_top10", **params)
        return self._extract_symbol(df)

    def get_top10_holders(self, ts_code: str, period: str = "",
                          start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """获取前十大股东。period: 报告期如 '20251231'。"""
        params = dict(ts_code=ts_code, period=period,
                       start_date=start_date, end_date=end_date)
        df = self._call("top10_holders", **params)
        return self._extract_symbol(df)

    def get_top10_floatholders(self, ts_code: str, period: str = "",
                                start_date: str = "",
                                end_date: str = "") -> pd.DataFrame:
        """获取前十大流通股东。"""
        params = dict(ts_code=ts_code, period=period,
                       start_date=start_date, end_date=end_date)
        df = self._call("top10_floatholders", **params)
        return self._extract_symbol(df)

    def get_suspen_d(self, trade_date: str = "",
                     ts_code: str = "", start_date: str = "",
                     end_date: str = "") -> pd.DataFrame:
        """获取每日停复牌信息。suspend_type: S=停牌 R=复牌。"""
        params = dict(trade_date=trade_date, ts_code=ts_code,
                       start_date=start_date, end_date=end_date)
        df = self._call("suspend_d", **params)
        return self._extract_symbol(df)

    def get_namechange(self, ts_code: str = "", start_date: str = "",
                       end_date: str = "") -> pd.DataFrame:
        """获取股票曾用名。"""
        params = dict(ts_code=ts_code, start_date=start_date, end_date=end_date)
        df = self._call("namechange", **params)
        return self._extract_symbol(df)

    def get_hs_const(self, hs_type: str = "", is_new: str = "1") -> pd.DataFrame:
        """获取沪深港通成分股。hs_type: SH=沪股通 SZ=深股通。"""
        df = self._call("hs_const", hs_type=hs_type, is_new=is_new)
        return self._extract_symbol(df)

    def get_stk_rewards(self, ts_code: str,
                        end_date: str = "") -> pd.DataFrame:
        """获取管理层薪酬和持股。"""
        df = self._call("stk_rewards", ts_code=ts_code, end_date=end_date)
        return self._extract_symbol(df)

    def get_fina_audit(self, ts_code: str, period: str = "",
                       start_date: str = "", end_date: str = "",
                       ann_date: str = "") -> pd.DataFrame:
        """获取财务审计意见。"""
        params = dict(ts_code=ts_code, period=period,
                       start_date=start_date, end_date=end_date,
                       ann_date=ann_date)
        df = self._call("fina_audit", **params)
        return self._extract_symbol(df)

    def get_stk_factor(self, ts_code: str = "", trade_date: str = "",
                       start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """获取股票技术面因子（MACD/KDJ/RSI/BOLL/CCI 等预计算值）。"""
        params = dict(ts_code=ts_code, trade_date=trade_date,
                       start_date=start_date, end_date=end_date)
        df = self._call("stk_factor", **params)
        return self._extract_symbol(df)

    def get_index_weight(self, index_code: str, trade_date: str = "",
                         start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """获取指数成分权重。index_code: 如 '000300.SH'（沪深300）。"""
        params = dict(index_code=index_code, trade_date=trade_date,
                       start_date=start_date, end_date=end_date)
        df = self._call("index_weight", **params)
        if df.empty:
            return df
        df["symbol"] = df["con_code"].str.extract(r"(\d{6})")
        return df

    def get_ggt_top10(self, trade_date: str, market_type: str = "") -> pd.DataFrame:
        """获取港股通十大成交股。market_type: 2=港股通(沪) 4=港股通(深)。"""
        params = dict(trade_date=trade_date)
        if market_type:
            params["market_type"] = market_type
        df = self._call("ggt_top10", **params)
        return self._extract_symbol(df)

    def get_ggt_daily(self, trade_date: str = "", start_date: str = "",
                      end_date: str = "") -> pd.DataFrame:
        """获取港股通每日成交统计。"""
        params = dict(trade_date=trade_date, start_date=start_date,
                       end_date=end_date)
        return self._call("ggt_daily", **params)

    def get_limit_list_orig(self, trade_date: str = "", ts_code: str = "",
                            start_date: str = "", end_date: str = "",
                            limit_type: str = "") -> pd.DataFrame:
        """获取每日涨跌停统计（原始版，数据早于 limit_list_d）。"""
        params = dict(trade_date=trade_date, ts_code=ts_code,
                       start_date=start_date, end_date=end_date)
        if limit_type:
            params["limit_type"] = limit_type
        df = self._call("limit_list", **params)
        return self._extract_symbol(df)

    # ── 概念/金股/复权/沪深港通 ──

    def get_concept(self) -> pd.DataFrame:
        return self._call("concept")

    def get_concept_detail(self, concept_id: str = "",
                           ts_code: str = "") -> pd.DataFrame:
        df = self._call("concept_detail", id=concept_id, ts_code=ts_code)
        return self._extract_symbol(df)

    def get_broker_recommend(self, month: str) -> pd.DataFrame:
        df = self._call("broker_recommend", month=month)
        return self._extract_symbol(df)

    def get_adj_factor(
        self, ts_code: str = "", trade_date: str = "",
        start_date: str = "", end_date: str = "",
    ) -> pd.DataFrame:
        params = dict(ts_code=ts_code, trade_date=trade_date,
                       start_date=start_date, end_date=end_date)
        df = self._call("adj_factor", **params)
        return self._extract_symbol(df)

    def get_moneyflow_hsgt(
        self, trade_date: str = "",
        start_date: str = "", end_date: str = "",
    ) -> pd.DataFrame:
        params = dict(trade_date=trade_date,
                       start_date=start_date, end_date=end_date)
        return self._call("moneyflow_hsgt", **params)

    def get_stk_surv(self, trade_date: str) -> pd.DataFrame:
        df = self._call("stk_surv", trade_date=trade_date)
        return self._extract_symbol(df)


    # ══════════════════════════════════════════════════════════════════════
    # 补充表 Provider 方法
    # ══════════════════════════════════════════════════════════════════════

    def get_stk_managers(self, ts_code: str = "", ann_date: str = "") -> pd.DataFrame:
        """获取上市公司管理层。"""
        return self._extract_symbol(self._call("stk_managers", ts_code=ts_code, ann_date=ann_date))

    def get_fina_mainbz(self, ts_code: str, end_date: str = "") -> pd.DataFrame:
        """获取主营业务构成。"""
        return self._extract_symbol(self._call("fina_mainbz", ts_code=ts_code, end_date=end_date))

    def get_stock_hsgt(self, ts_code: str = "", trade_date: str = "") -> pd.DataFrame:
        """获取沪深港通股票列表。"""
        return self._extract_symbol(self._call("stock_hsgt", ts_code=ts_code, trade_date=trade_date))

    def get_new_share(self, start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """获取IPO新股上市。"""
        df = self._call("new_share", start_date=start_date, end_date=end_date)
        return self._extract_symbol(df)

    def get_margin_secs(self, trade_date: str = "", exchange: str = "") -> pd.DataFrame:
        """获取融资融券标的。"""
        return self._extract_symbol(self._call("margin_secs", trade_date=trade_date, exchange=exchange))

    def get_limit_list_ths(self, trade_date: str = "", limit_type: str = "") -> pd.DataFrame:
        """获取THS涨跌停榜单。"""
        return self._extract_symbol(self._call("limit_list_ths", trade_date=trade_date, limit_type=limit_type))

    def get_limit_step(self, trade_date: str = "", nums: str = "") -> pd.DataFrame:
        """获取涨停股票连板天梯。"""
        return self._extract_symbol(self._call("limit_step", trade_date=trade_date, nums=nums))

    def get_stk_auction(self, trade_date: str = "", ts_code: str = "") -> pd.DataFrame:
        """获取开盘竞价成交。"""
        return self._extract_symbol(self._call("stk_auction", trade_date=trade_date, ts_code=ts_code))

    def get_new_share(self, start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """获取IPO新股上市。"""
        return self._extract_symbol(self._call("new_share", start_date=start_date, end_date=end_date))
    # ══════════════════════════════════════════════════════════════════════
    # 新增补充数据
    # ══════════════════════════════════════════════════════════════════════

    def get_stock_st(self, trade_date: str = "", ts_code: str = "",
                     start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """获取ST股票列表。"""
        params = dict(trade_date=trade_date, ts_code=ts_code,
                       start_date=start_date, end_date=end_date)
        return self._extract_symbol(self._call("stock_st", **params))

    def get_stk_premarket(self, trade_date: str = "",
                          ts_code: str = "", start_date: str = "",
                          end_date: str = "") -> pd.DataFrame:
        """获取每日股本（盘前）。"""
        params = dict(trade_date=trade_date, ts_code=ts_code,
                       start_date=start_date, end_date=end_date)
        return self._extract_symbol(self._call("stk_premarket", **params))

    def get_margin_summary(self, trade_date: str = "",
                           exchange_id: str = "",
                           start_date: str = "",
                           end_date: str = "") -> pd.DataFrame:
        """获取融资融券交易汇总。"""
        params = dict(trade_date=trade_date, exchange_id=exchange_id,
                       start_date=start_date, end_date=end_date)
        return self._call("margin", **params)

    def get_stk_shock(self, trade_date: str = "", ts_code: str = "",
                      start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """获取个股异常波动。"""
        params = dict(trade_date=trade_date, ts_code=ts_code,
                       start_date=start_date, end_date=end_date)
        return self._extract_symbol(self._call("stk_shock", **params))

    def get_stk_high_shock(self, trade_date: str = "", ts_code: str = "",
                           start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """获取个股严重异常波动。"""
        params = dict(trade_date=trade_date, ts_code=ts_code,
                       start_date=start_date, end_date=end_date)
        return self._extract_symbol(self._call("stk_high_shock", **params))

    def get_stk_auction_o(self, trade_date: str = "",
                          ts_code: str = "", start_date: str = "",
                          end_date: str = "") -> pd.DataFrame:
        """获取开盘集合竞价。"""
        params = dict(trade_date=trade_date, ts_code=ts_code,
                       start_date=start_date, end_date=end_date)
        return self._extract_symbol(self._call("stk_auction_o", **params))

    def get_stk_auction_c(self, trade_date: str = "",
                          ts_code: str = "", start_date: str = "",
                          end_date: str = "") -> pd.DataFrame:
        """获取收盘集合竞价。"""
        params = dict(trade_date=trade_date, ts_code=ts_code,
                       start_date=start_date, end_date=end_date)
        return self._extract_symbol(self._call("stk_auction_c", **params))

    def get_stock_company(self, ts_code: str = "", exchange: str = "") -> pd.DataFrame:
        """获取上市公司基本信息。"""
        params = dict(ts_code=ts_code, exchange=exchange)
        return self._extract_symbol(self._call("stock_company", **params))

    def get_stk_nineturn(self, ts_code: str = "", trade_date: str = "",
                         freq: str = "daily", start_date: str = "",
                         end_date: str = "") -> pd.DataFrame:
        """获取神奇九转指标。"""
        params = dict(ts_code=ts_code, trade_date=trade_date,
                       freq=freq, start_date=start_date, end_date=end_date)
        return self._extract_symbol(self._call("stk_nineturn", **params))

    def get_ccass_hold(self, ts_code: str = "", trade_date: str = "",
                       start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """获取中央结算系统持股统计。"""
        params = dict(ts_code=ts_code, trade_date=trade_date,
                       start_date=start_date, end_date=end_date)
        return self._extract_symbol(self._call("ccass_hold", **params))

    def get_report_rc(self, ts_code: str = "", report_date: str = "",
                      start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """获取券商盈利预测。"""
        params = dict(ts_code=ts_code, report_date=report_date,
                       start_date=start_date, end_date=end_date)
        return self._extract_symbol(self._call("report_rc", **params))

    def get_index_daily(self, ts_code: str, start_date: str,
                        end_date: str) -> pd.DataFrame:
        return self._call("index_daily", ts_code=ts_code,
                          start_date=start_date, end_date=end_date)

    def get_stk_factor_pro(
        self, ts_code: str, start_date: str, end_date: str,
    ) -> pd.DataFrame:
        df = self._call("stk_factor_pro", ts_code=ts_code,
                         start_date=start_date, end_date=end_date)
        return self._extract_symbol(df)


    def get_st(self, trade_date: str = "") -> pd.DataFrame:
        """ST风险警示板股票。"""
        return self._extract_symbol(self._call("st", trade_date=trade_date))

    def get_bse_mapping(self, ts_code: str = "") -> pd.DataFrame:
        """北交所新旧代码对照。"""
        return self._call("bse_mapping", ts_code=ts_code)

    def get_bak_basic(self, trade_date: str = "", ts_code: str = "") -> pd.DataFrame:
        """股票历史列表。"""
        return self._extract_symbol(self._call("bak_basic", trade_date=trade_date, ts_code=ts_code))

    def get_ggt_top10(self, trade_date: str = "", market_type: str = "") -> pd.DataFrame:
        """港股通十大成交股。"""
        return self._extract_symbol(self._call("ggt_top10", trade_date=trade_date, market_type=market_type))

    def get_ggt_daily(self, trade_date: str = "", start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """港股通每日成交统计。"""
        return self._call("ggt_daily", trade_date=trade_date, start_date=start_date, end_date=end_date)

    def get_ccass_hold_detail(self, ts_code: str = "", trade_date: str = "") -> pd.DataFrame:
        """中央结算系统持股明细。"""
        return self._extract_symbol(self._call("ccass_hold_detail", ts_code=ts_code, trade_date=trade_date))

    def get_slb_sec(self, trade_date: str = "", ts_code: str = "") -> pd.DataFrame:
        """转融券交易汇总。"""
        return self._extract_symbol(self._call("slb_sec", trade_date=trade_date, ts_code=ts_code))

    def get_slb_len(self, trade_date: str = "", start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """转融资交易汇总。"""
        return self._call("slb_len", trade_date=trade_date, start_date=start_date, end_date=end_date)

    def get_moneyflow_ths(self, trade_date: str = "", ts_code: str = "") -> pd.DataFrame:
        """个股资金流向(THS)。"""
        return self._extract_symbol(self._call("moneyflow_ths", trade_date=trade_date, ts_code=ts_code))

    def get_moneyflow_dc(self, trade_date: str = "", ts_code: str = "") -> pd.DataFrame:
        """个股资金流向(DC)。"""
        return self._extract_symbol(self._call("moneyflow_dc", trade_date=trade_date, ts_code=ts_code))

    def get_moneyflow_cnt_ths(self, trade_date: str = "") -> pd.DataFrame:
        """板块资金流向(THS)。"""
        return self._extract_symbol(self._call("moneyflow_cnt_ths", trade_date=trade_date))

    def get_moneyflow_ind_ths(self, trade_date: str = "") -> pd.DataFrame:
        """行业资金流向(THS)。"""
        return self._extract_symbol(self._call("moneyflow_ind_ths", trade_date=trade_date))

    def get_moneyflow_ind_dc(self, trade_date: str = "", content_type: str = "") -> pd.DataFrame:
        """板块资金流向(DC)。"""
        return self._extract_symbol(self._call("moneyflow_ind_dc", trade_date=trade_date, content_type=content_type))

    def get_moneyflow_mkt_dc(self, trade_date: str = "") -> pd.DataFrame:
        """大盘资金流向(DC)。"""
        return self._call("moneyflow_mkt_dc", trade_date=trade_date)

    def get_ths_daily(self, ts_code: str = "", trade_date: str = "") -> pd.DataFrame:
        """THS概念板块行情。"""
        return self._extract_symbol(self._call("ths_daily", ts_code=ts_code, trade_date=trade_date))

    def get_dc_member(self, ts_code: str = "", trade_date: str = "") -> pd.DataFrame:
        """DC概念板块成分。"""
        return self._extract_symbol(self._call("dc_member", ts_code=ts_code, trade_date=trade_date))

    def get_dc_daily(self, ts_code: str = "", trade_date: str = "") -> pd.DataFrame:
        """DC概念板块行情。"""
        return self._extract_symbol(self._call("dc_daily", ts_code=ts_code, trade_date=trade_date))

    def get_dc_hot(self, trade_date: str = "", market: str = "") -> pd.DataFrame:
        """DC热榜。"""
        return self._extract_symbol(self._call("dc_hot", trade_date=trade_date, market=market))

    def get_tdx_member(self, ts_code: str = "", trade_date: str = "") -> pd.DataFrame:
        """TDX概念板块成分。"""
        return self._extract_symbol(self._call("tdx_member", ts_code=ts_code, trade_date=trade_date))

    def get_tdx_daily(self, ts_code: str = "", trade_date: str = "") -> pd.DataFrame:
        """TDX概念板块行情。"""
        return self._extract_symbol(self._call("tdx_daily", ts_code=ts_code, trade_date=trade_date))

    def get_kpl_list(self, trade_date: str = "", tag: str = "") -> pd.DataFrame:
        """榜单数据(KP)。"""
        return self._extract_symbol(self._call("kpl_list", trade_date=trade_date, tag=tag))

    def get_kpl_concept_cons(self, ts_code: str = "", trade_date: str = "") -> pd.DataFrame:
        """题材成分(KP)。"""
        return self._extract_symbol(self._call("kpl_concept_cons", ts_code=ts_code, trade_date=trade_date))

    def get_dc_concept(self, trade_date: str = "", name: str = "") -> pd.DataFrame:
        """题材数据(DC)。"""
        return self._call("dc_concept", trade_date=trade_date, name=name)

    def get_dc_concept_cons(self, theme_code: str = "", trade_date: str = "") -> pd.DataFrame:
        """题材成分(DC)。"""
        return self._extract_symbol(self._call("dc_concept_cons", theme_code=theme_code, trade_date=trade_date))


    def get_market_overview(self, trade_date: str = "") -> dict:
        """获取当日市场概览（上证/深证指数 + 北向资金）。"""
        result = {}
        try:
            df = self.get_index_daily("000001.SH", trade_date, trade_date)
            if not df.empty:
                result["sh_close"] = float(df.iloc[-1]["close"])
                result["sh_pct"] = float(df.iloc[-1]["pct_chg"])
            df = self.get_index_daily("399001.SZ", trade_date, trade_date)
            if not df.empty:
                result["sz_close"] = float(df.iloc[-1]["close"])
                result["sz_pct"] = float(df.iloc[-1]["pct_chg"])
            df = self.get_moneyflow_hsgt(trade_date=trade_date)
            if not df.empty:
                result["north_net"] = float(df.iloc[-1]["north_money"])
        except Exception as exc:
            logger.warning(f"获取市场概览失败: {exc}")
        return result

    def get_index_daily(self, ts_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取指数日线行情。"""
        return self._call("index_daily", ts_code=ts_code, start_date=start_date, end_date=end_date)


    def get_ths_hot(self, trade_date: str = "", market: str = "") -> pd.DataFrame:
        """THS热榜。"""
        return self._extract_symbol(self._call("ths_hot", trade_date=trade_date, market=market))

    def get_hm_detail(self, trade_date: str = "", ts_code: str = "") -> pd.DataFrame:
        """游资交易每日明细。"""
        return self._extract_symbol(self._call("hm_detail", trade_date=trade_date, ts_code=ts_code))
