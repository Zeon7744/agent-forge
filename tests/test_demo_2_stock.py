# -*- coding: utf-8 -*-
"""
Demo 2 单元测试
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples"))

from demo_2_stock_signal import (
    StockSignalTool,
    calc_ma,
    calc_rsi,
    calc_macd,
    analyze_volume_price,
    generate_signal,
)


class TestStockSignalTool:
    """A股信号分析工具测试"""

    @pytest.fixture
    def tool(self):
        return StockSignalTool()

    @pytest.fixture
    def sample_prices(self):
        return [10.0, 10.5, 11.0, 10.8, 11.2, 11.5, 12.0, 11.8, 12.2, 12.5]

    @pytest.fixture
    def sample_volumes(self):
        return [1000, 1200, 1500, 900, 1100, 1300, 1800, 1600, 1400, 1700]

    def test_calc_ma(self):
        """测试 MA 计算"""
        prices = [10, 11, 12, 13, 14]
        ma = calc_ma(prices, 3)
        assert ma is not None
        assert ma == 13.0  # (12+13+14)/3

    def test_calc_rsi(self):
        """测试 RSI 计算"""
        prices = [10, 10.5, 11, 10.8, 11.2, 11.5, 12, 12.5, 13, 12.8]
        rsi = calc_rsi(prices, 6)
        assert rsi is not None
        assert 0 <= rsi <= 100

    def test_calc_macd(self):
        """测试 MACD 计算"""
        prices = [10] * 35 + [11, 11.5, 12]  # 足够长的序列
        macd = calc_macd(prices)
        assert "dif" in macd
        assert "dea" in macd
        assert "macd_hist" in macd

    def test_analyze_volume_price(self):
        """测试量价分析"""
        prices = [10, 10.5, 11, 11.5, 12]
        volumes = [1000, 1200, 1500, 1800, 2500]
        result = analyze_volume_price(volumes, prices)
        assert "pattern" in result
        assert "description" in result

    def test_process_with_prices(self, tool, sample_prices):
        """测试基本处理流程"""
        result = tool.process(prices=sample_prices, symbol="TEST")
        assert result["symbol"] == "TEST"
        assert "indicators" in result
        assert "signal" in result
        assert result["signal"] in ["买入", "卖出", "持有", "观望"]

    def test_process_with_string_prices(self, tool):
        """测试字符串输入"""
        result = tool.process(prices="10,10.5,11,11.5,12,12.5", symbol="TEST")
        assert result["current_price"] == 12.5

    def test_too_few_prices_raises_error(self, tool):
        """测试数据不足时的异常"""
        from agent_forge.tools.chinese_base import ValidationError
        with pytest.raises(ValidationError):
            tool.process(prices=[10.0, 10.5])  # 不足 5 个

    def test_generate_analysis_report(self, tool, sample_prices):
        """测试报告生成"""
        report = tool.generate_analysis_report(sample_prices, symbol="TEST")
        assert isinstance(report, str)
        assert "A股交易信号分析报告" in report
        assert "TEST" in report

    def test_signal_generation_bull(self):
        """测试买入信号生成"""
        indicators = {
            "current_price": 12.5,
            "ma5": 11.5,
            "ma20": 10.5,
            "rsi": 55.0,
            "macd": {"dif": 0.5, "dea": 0.3},
        }
        result = generate_signal(indicators)
        assert result["signal"] in ["买入", "持有"]

    def test_signal_generation_bear(self):
        """测试卖出信号生成"""
        indicators = {
            "current_price": 10.0,
            "ma5": 11.0,
            "ma20": 11.5,
            "rsi": 75.0,
            "macd": {"dif": -0.3, "dea": -0.1},
        }
        result = generate_signal(indicators)
        assert result["signal"] in ["卖出", "持有"]
