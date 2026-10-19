# -*- coding: utf-8 -*-
"""收款网关测试"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent_forge.gateway.base import BaseGateway, GatewayResult


def test_gateway_result():
    """测试 GatewayResult 数据结构"""
    result = GatewayResult(success=True, order_id="ord_123", data={"amount": 100})
    assert result.success is True
    assert result.order_id == "ord_123"
    assert result.needs_secret is False


def test_gateway_result_error():
    """测试错误结果"""
    result = GatewayResult(success=False, error="Token missing")
    assert result.success is False
    assert result.error == "Token missing"


def test_needs_secret():
    """测试缺少凭证标记"""
    result = GatewayResult(success=False, needs_secret=True)
    assert result.needs_secret is True


if __name__ == "__main__":
    test_gateway_result()
    test_gateway_result_error()
    test_needs_secret()
    print("所有网关测试通过")
