# -*- coding: utf-8 -*-
"""
收款网关模块
"""

from .base import BaseGateway, GatewayResult
from .afdian import AfdianGateway

__all__ = ["BaseGateway", "GatewayResult", "AfdianGateway", "get_gateway"]

# 内置网关注册表
BUILTIN_REGISTRY = {
    "afdian": AfdianGateway,
    "noop": None,  # 默认使用 NoOp
}


def get_gateway():
    """根据环境变量获取网关实例"""
    import os
    gateway_name = os.getenv("JZ_SAAS_BILLING_GATEWAY", "noop")
    
    if gateway_name == "afdian":
        return AfdianGateway()
    return None  # NoOp
