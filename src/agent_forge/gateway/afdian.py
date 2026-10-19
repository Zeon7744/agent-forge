# -*- coding: utf-8 -*-
"""
爱发电收款网关
"""

from __future__ import annotations
import os
import json
import time
import hmac
import hashlib
from typing import Any, Dict, Optional
from .base import BaseGateway, GatewayResult


class AfdianGateway(BaseGateway):
    """爱发电支付网关"""
    
    API_BASE = "https://afdian.net/api"
    
    def __init__(self):
        self.user_id = os.getenv("JZ_SAAS_AFDIAN_USER")
        self.token = os.getenv("JZ_SAAS_AFDIAN_TOKEN")
    
    def _check_credentials(self) -> bool:
        """检查凭证是否配置"""
        return bool(self.user_id and self.token)
    
    def create_order(self, amount: int, plan: str, description: str = "", **kwargs) -> GatewayResult:
        """创建支付订单"""
        if not self._check_credentials():
            return GatewayResult(
                success=False,
                needs_secret=True,
                error="AFDIAN_TOKEN not configured",
            )
        
        # 构建请求参数
        payload = {
            "user_id": self.user_id,
            "token": self.token,
            "amount": amount,
            "plan": plan,
            "description": description or f"Agent-Forge {plan} 订阅",
            "callback_url": kwargs.get("callback_url"),
            "return_url": kwargs.get("return_url", "https://afdian.net"),
        }
        
        # 发送请求（实际实现需要调用爱发电 API）
        try:
            import urllib.request
            req = urllib.request.Request(
                f"{self.API_BASE}/payment/create",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            
            if result.get("code") == 0:
                return GatewayResult(
                    success=True,
                    order_id=result.get("data", {}).get("order_id"),
                    data=result.get("data"),
                )
            else:
                return GatewayResult(
                    success=False,
                    error=result.get("message", "Unknown error"),
                )
        except Exception as e:
            return GatewayResult(success=False, error=str(e))
    
    def query_order(self, order_id: str) -> GatewayResult:
        """查询订单状态"""
        if not self._check_credentials():
            return GatewayResult(success=False, needs_secret=True)
        
        try:
            import urllib.request
            payload = {
                "user_id": self.user_id,
                "token": self.token,
                "order_id": order_id,
            }
            req = urllib.request.Request(
                f"{self.API_BASE}/payment/query",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            
            if result.get("code") == 0:
                return GatewayResult(success=True, data=result.get("data"))
            else:
                return GatewayResult(success=False, error=result.get("message"))
        except Exception as e:
            return GatewayResult(success=False, error=str(e))
    
    def refund(self, order_id: str, amount: int = 0) -> GatewayResult:
        """退款"""
        if not self._check_credentials():
            return GatewayResult(success=False, needs_secret=True)
        
        try:
            import urllib.request
            payload = {
                "user_id": self.user_id,
                "token": self.token,
                "order_id": order_id,
                "amount": amount,
            }
            req = urllib.request.Request(
                f"{self.API_BASE}/payment/refund",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            
            return GatewayResult(success=result.get("code") == 0, data=result.get("data"))
        except Exception as e:
            return GatewayResult(success=False, error=str(e))
