# -*- coding: utf-8 -*-
"""
收款网关基类
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional
import time
import abc


@dataclass
class GatewayResult:
    """网关操作结果"""
    success: bool
    order_id: Optional[str] = None
    data: Dict[str, Any] = None
    error: Optional[str] = None
    needs_secret: bool = False


class BaseGateway(abc.ABC):
    """收款网关抽象基类"""
    
    @abc.abstractmethod
    def create_order(self, amount: int, plan: str, description: str = "", **kwargs) -> GatewayResult:
        """创建支付订单"""
        pass
    
    @abc.abstractmethod
    def query_order(self, order_id: str) -> GatewayResult:
        """查询订单状态"""
        pass
    
    @abc.abstractmethod
    def refund(self, order_id: str, amount: int = 0) -> GatewayResult:
        """退款"""
        pass
    
    def get_payment_url(self, order_id: str) -> Optional[str]:
        """获取支付链接"""
        return None
