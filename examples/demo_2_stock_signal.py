# -*- coding: utf-8 -*-
"""
Demo 2: A 股交易信号分析工具

功能：
- 计算技术指标：MA（均线）、RSI（相对强弱指标）、MACD
- 分析量价关系（放量/缩量/量价背离）
- 生成买入/卖出/持有信号
- 输出综合分析报告

使用示例::

    # CLI 方式
    python examples/demo_2_stock_signal.py analyze --prices "10,10.5,11,10.8,11.2,11.5,12" --volumes "1000,1200,1500,900,1100,1300,1800"
    python examples/demo_2_stock_signal.py report --symbol "600519"

    # Python API 方式
    from agent_forge.tools.chinese_base import ChineseTool
"""

from __future__ import annotations

import sys
import os
import math
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agent_forge.tools.chinese_base import ChineseTool, ValidationError


# ── 技术指标计算函数 ──────────────────────────────────────────

def calc_ma(prices: List[float], period: int) -> Optional[float]:
    """
    计算简单移动平均线（MA）

    Args:
        prices: 价格序列
        period: 均线周期

    Returns:
        MA 值，数据不足时返回 None
    """
    if len(prices) < period:
        return None
    return round(sum(prices[-period:]) / period, 3)


def calc_rsi(prices: List[float], period: int = 14) -> Optional[float]:
    """
    计算相对强弱指标（RSI）

    Args:
        prices: 价格序列
        period: 计算周期，默认 14

    Returns:
        RSI 值（0-100），数据不足时返回 None
    """
    if len(prices) < period + 1:
        return None
    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    recent = deltas[-period:]
    gains = sum(d for d in recent if d > 0) / period
    losses = -sum(d for d in recent if d < 0) / period
    if losses == 0:
        return 100.0
    rs = gains / losses
    return round(100 - (100 / (1 + rs)), 2)


def calc_macd(
    prices: List[float],
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> Dict[str, Optional[float]]:
    """
    计算 MACD 指标

    Args:
        prices: 价格序列
        fast: 快线周期
        slow: 慢线周期
        signal: 信号线周期

    Returns:
        包含 DIF、DEA、MACD柱 的字典
    """
    if len(prices) < slow + signal:
        return {"dif": None, "dea": None, "macd_hist": None}

    def ema(data: List[float], period: int) -> List[float]:
        k = 2 / (period + 1)
        result = [data[0]]
        for i in range(1, len(data)):
            result.append(data[i] * k + result[-1] * (1 - k))
        return result

    ema_fast = ema(prices, fast)
    ema_slow = ema(prices, slow)
    dif_series = [f - s for f, s in zip(ema_fast, ema_slow)]
    dea_series = ema(dif_series, signal)
    dif = round(dif_series[-1], 4)
    dea = round(dea_series[-1], 4)
    macd_hist = round((dif - dea) * 2, 4)
    return {"dif": dif, "dea": dea, "macd_hist": macd_hist}


def analyze_volume_price(
    volumes: List[float],
    prices: List[float],
) -> Dict[str, str]:
    """
    分析量价关系

    Args:
        volumes: 成交量序列
        prices: 价格序列

    Returns:
        量价分析结果
    """
    if len(volumes) < 3 or len(prices) < 3:
        return {"pattern": "数据不足", "description": "至少需要3日数据"}

    avg_vol = sum(volumes[:-1]) / len(volumes[:-1])
    latest_vol = volumes[-1]
    price_change = prices[-1] - prices[-2]

    # 量比
    volume_ratio = round(latest_vol / avg_vol, 2) if avg_vol > 0 else 0

    if volume_ratio > 1.5 and price_change > 0:
        pattern = "放量上涨"
        desc = "成交量显著放大，价格上涨，多方力量强势"
    elif volume_ratio > 1.5 and price_change < 0:
        pattern = "放量下跌"
        desc = "成交量显著放大，价格下跌，空方力量主导"
    elif volume_ratio < 0.7 and price_change > 0:
        pattern = "缩量上涨"
        desc = "成交量萎缩，价格小幅上涨，上涨动力存疑"
    elif volume_ratio < 0.7 and price_change < 0:
        pattern = "缩量下跌"
        desc = "成交量萎缩，价格下跌，抛压减弱"
    else:
        pattern = "量价平稳"
        desc = "成交量与价格变动匹配，市场相对平稳"

    return {
        "pattern": pattern,
        "description": desc,
        "volume_ratio": str(volume_ratio),
        "price_change": f"{price_change:+.2f}",
    }


def generate_signal(indicators: Dict[str, Any]) -> Dict[str, str]:
    """
    综合指标生成交易信号

    Args:
        indicators: 技术指标字典

    Returns:
        包含 signal、reasons、confidence 的字典
    """
    reasons = []
    bull_score = 0
    bear_score = 0

    # MA 分析
    ma5 = indicators.get("ma5")
    ma20 = indicators.get("ma20")
    current_price = indicators.get("current_price")
    if ma5 and ma20 and current_price:
        if current_price > ma5 > ma20:
            reasons.append("价格在均线上方，多头排列")
            bull_score += 2
        elif current_price < ma5 < ma20:
            reasons.append("价格在均线下方，空头排列")
            bear_score += 2

    # RSI 分析
    rsi = indicators.get("rsi")
    if rsi is not None:
        if rsi < 30:
            reasons.append(f"RSI={rsi}，超卖区域，可能反弹")
            bull_score += 1
        elif rsi > 70:
            reasons.append(f"RSI={rsi}，超买区域，注意回调")
            bear_score += 1
        elif 40 < rsi < 60:
            reasons.append(f"RSI={rsi}，中性区域")

    # MACD 分析
    macd = indicators.get("macd", {})
    dif = macd.get("dif")
    dea = macd.get("dea")
    if dif is not None and dea is not None:
        if dif > dea:
            reasons.append("MACD金叉，DIF在DEA上方")
            bull_score += 1
        else:
            reasons.append("MACD死叉，DIF在DEA下方")
            bear_score += 1

    # 综合判定
    total = bull_score + bear_score
    if total == 0:
        return {"signal": "观望", "reasons": reasons or ["指标数据不足"], "confidence": "低"}

    if bull_score > bear_score:
        signal = "买入"
        confidence = "高" if bull_score >= 3 else "中"
    elif bear_score > bull_score:
        signal = "卖出"
        confidence = "高" if bear_score >= 3 else "中"
    else:
        signal = "持有"
        confidence = "中"

    return {"signal": signal, "reasons": reasons, "confidence": confidence}


# ── 工具类 ────────────────────────────────────────────────────

class StockSignalTool(ChineseTool):
    """
    A 股交易信号分析工具

    基于技术指标（MA/RSI/MACD）和量价关系，生成交易信号。
    支持自定义价格/成交量数据输入。

    注册信息:
        tool_id: stock.signal
        name: analyze_stock_signal
        category: chinese
    """

    tool_id = "stock.signal"
    tool_name = "analyze_stock_signal"
    tool_description = "A股交易信号分析，基于MA/RSI/MACD技术指标和量价关系生成买卖信号"
    tool_category = "chinese"
    tool_tags = ["A股", "交易信号", "技术分析", "量化"]

    def get_input_properties(self) -> Dict[str, Any]:
        return {
            "prices": {
                "type": "array",
                "items": {"type": "number"},
                "description": "历史价格序列（最近 → 最新，逗号分隔的字符串也可）",
            },
            "volumes": {
                "type": "array",
                "items": {"type": "number"},
                "description": "对应成交量序列",
            },
            "symbol": {
                "type": "string",
                "description": "股票代码（用于报告标题，可选）",
            },
        }

    def get_required_fields(self) -> List[str]:
        return ["prices"]

    def process(
        self,
        prices: Any,
        volumes: Optional[Any] = None,
        symbol: str = "未知",
    ) -> dict:
        """
        执行交易信号分析

        Args:
            prices: 价格序列（list 或逗号分隔的字符串）
            volumes: 成交量序列（可选）
            symbol: 股票代码

        Returns:
            包含技术指标和交易信号的分析结果
        """
        # 参数预处理
        price_list = self._parse_series(prices)
        vol_list = self._parse_series(volumes) if volumes else None

        if len(price_list) < 5:
            raise ValidationError("价格序列至少需要5个数据点", field="prices")

        # 计算技术指标
        indicators = {
            "current_price": price_list[-1],
            "ma5": calc_ma(price_list, 5),
            "ma10": calc_ma(price_list, 10),
            "ma20": calc_ma(price_list, 20),
            "rsi": calc_rsi(price_list),
            "rsi6": calc_rsi(price_list, 6),
            "macd": calc_macd(price_list),
        }

        # 量价分析
        vol_price = {}
        if vol_list and len(vol_list) >= 3:
            vol_price = analyze_volume_price(vol_list, price_list)

        # 生成信号
        signal_info = generate_signal(indicators)

        return {
            "symbol": symbol,
            "current_price": indicators["current_price"],
            "indicators": {
                "MA5": indicators["ma5"],
                "MA10": indicators["ma10"],
                "MA20": indicators["ma20"],
                "RSI(14)": indicators["rsi"],
                "RSI(6)": indicators["rsi6"],
                "DIF": indicators["macd"]["dif"],
                "DEA": indicators["macd"]["dea"],
                "MACD柱": indicators["macd"]["macd_hist"],
            },
            "volume_price": vol_price,
            "signal": signal_info["signal"],
            "reasons": signal_info["reasons"],
            "confidence": signal_info["confidence"],
        }

    def generate_analysis_report(
        self,
        prices: Any,
        volumes: Optional[Any] = None,
        symbol: str = "未知",
    ) -> str:
        """
        生成完整的分析报告

        Args:
            prices: 价格序列
            volumes: 成交量序列
            symbol: 股票代码

        Returns:
            Markdown 格式的分析报告
        """
        result = self.process(prices, volumes, symbol)

        indicators = result["indicators"]
        indicator_lines = [f"{k}: {v}" for k, v in indicators.items() if v is not None]

        sections = [
            {
                "heading": "分析概览",
                "content": f"股票代码: {result['symbol']}  |  最新价: {result['current_price']}  |  "
                f"信号: **{result['signal']}**  |  置信度: {result['confidence']}",
            },
            {
                "heading": "技术指标",
                "content": indicator_lines,
            },
        ]

        if result["volume_price"]:
            vp = result["volume_price"]
            sections.append({
                "heading": "量价分析",
                "content": [
                    f"形态: {vp.get('pattern', 'N/A')}",
                    f"说明: {vp.get('description', '')}",
                    f"量比: {vp.get('volume_ratio', 'N/A')}",
                    f"涨跌: {vp.get('price_change', 'N/A')}",
                ],
            })

        sections.append({
            "heading": "信号依据",
            "content": result["reasons"],
        })
        sections.append({
            "heading": "风险提示",
            "content": [
                "本报告仅基于技术指标，不构成投资建议",
                "请结合基本面、政策面和资金面综合判断",
                "股市有风险，投资需谨慎",
            ],
        })

        return self.generate_report(
            title=f"A股交易信号分析报告 — {result['symbol']}",
            sections=sections,
        )

    @staticmethod
    def _parse_series(data: Any) -> List[float]:
        """将输入标准化为 float 列表"""
        if isinstance(data, str):
            return [float(x.strip()) for x in data.split(",") if x.strip()]
        if isinstance(data, (list, tuple)):
            return [float(x) for x in data]
        raise ValidationError(f"无法解析数据序列: {type(data)}", field="prices")


# ── Typer CLI ─────────────────────────────────────────────────

try:
    import typer
    from rich.console import Console
    from rich.table import Table

    app = typer.Typer(help="A 股交易信号分析工具")
    console = Console()

    @app.command("analyze")
    def analyze(
        prices: str = typer.Argument(..., help="价格序列，逗号分隔，如 10,10.5,11,10.8,11.2"),
        volumes: str = typer.Option(None, "--volumes", "-v", help="成交量序列，逗号分隔"),
        symbol: str = typer.Option("未知", "--symbol", "-s", help="股票代码"),
    ):
        """分析交易信号"""
        tool = StockSignalTool()
        vol_list = [float(x.strip()) for x in volumes.split(",")] if volumes else None
        result = tool.process(
            prices=[float(x.strip()) for x in prices.split(",")],
            volumes=vol_list,
            symbol=symbol,
        )
        console.print(f"\n[bold]股票代码:[/bold] {result['symbol']}")
        console.print(f"[bold]最新价:[/bold] {result['current_price']}")
        console.print(f"\n[bold cyan]技术指标:[/bold cyan]")
        for k, v in result["indicators"].items():
            if v is not None:
                console.print(f"  {k}: {v}")
        if result["volume_price"]:
            console.print(f"\n[bold magenta]量价分析:[/bold magenta]")
            console.print(f"  形态: {result['volume_price']['pattern']}")
            console.print(f"  {result['volume_price']['description']}")
        signal_color = {"买入": "green", "卖出": "red", "持有": "yellow", "观望": "dim"}.get(
            result["signal"], "white"
        )
        console.print(f"\n[bold {signal_color}]📊 交易信号: {result['signal']}[/bold {signal_color}]")
        console.print(f"[bold]置信度:[/bold] {result['confidence']}")
        console.print(f"[bold]依据:[/bold]")
        for r in result["reasons"]:
            console.print(f"  • {r}")

    @app.command("report")
    def report(
        prices: str = typer.Argument(..., help="价格序列，逗号分隔"),
        volumes: str = typer.Option(None, "--volumes", "-v", help="成交量序列"),
        symbol: str = typer.Option("未知", "--symbol", "-s", help="股票代码"),
    ):
        """生成分析报告"""
        tool = StockSignalTool()
        vol_list = [float(x.strip()) for x in volumes.split(",")] if volumes else None
        md = tool.generate_analysis_report(
            prices=[float(x.strip()) for x in prices.split(",")],
            volumes=vol_list,
            symbol=symbol,
        )
        console.print(md)

except ImportError:
    app = None

    def main():
        tool = StockSignalTool()
        sample_prices = [10.0, 10.3, 10.8, 10.5, 11.0, 11.2, 10.9, 11.5, 11.8, 12.0]
        result = tool.process(prices=sample_prices, symbol="示例股票")
        print(tool.format_result(result))


if __name__ == "__main__":
    if app is not None:
        app()
    else:
        main()
