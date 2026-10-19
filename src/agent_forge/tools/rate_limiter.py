# -*- coding: utf-8 -*-
"""
限流器模块 - Token 配额与调用频率控制
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time
import threading
from collections import defaultdict


@dataclass
class RateLimitConfig:
    """限流配置"""
    max_requests: int  # 最大请求数
    window_seconds: int  # 时间窗口（秒）
    burst_limit: int = 0  # 突发限制（0 = 不限）
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "max_requests": self.max_requests,
            "window_seconds": self.window_seconds,
            "burst_limit": self.burst_limit,
        }


@dataclass
class QuotaInfo:
    """配额信息"""
    plan: str  # free, pro, enterprise
    daily_limit: int
    monthly_limit: int
    used_today: int = 0
    used_month: int = 0
    reset_time: Optional[float] = None
    
    @property
    def remaining_today(self) -> int:
        return max(0, self.daily_limit - self.used_today)
    
    @property
    def remaining_month(self) -> int:
        return max(0, self.monthly_limit - self.used_month)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan": self.plan,
            "daily_limit": self.daily_limit,
            "monthly_limit": self.monthly_limit,
            "used_today": self.used_today,
            "used_month": self.used_month,
            "remaining_today": self.remaining_today,
            "remaining_month": self.remaining_month,
        }


class TokenBucket:
    """令牌桶限流器"""
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate  # 每秒补充的令牌数
        self.tokens = capacity
        self.last_refill = time.time()
        self._lock = threading.Lock()
    
    def consume(self, tokens: int = 1) -> bool:
        """消耗令牌，返回是否成功"""
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def _refill(self):
        """补充令牌"""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now


class RateLimiter:
    """限流管理器"""
    
    # 默认配额配置（按套餐）
    QUOTA_CONFIG = {
        "free": RateLimitConfig(max_requests=100, window_seconds=3600),
        "pro": RateLimitConfig(max_requests=10000, window_seconds=3600),
        "enterprise": RateLimitConfig(max_requests=1000000, window_seconds=3600),
    }
    
    # 每日/每月配额
    DAILY_QUOTA = {
        "free": 50,
        "pro": 5000,
        "enterprise": 100000,
    }
    
    MONTHLY_QUOTA = {
        "free": 500,
        "pro": 50000,
        "enterprise": 1000000,
    }
    
    def __init__(self):
        self._buckets: Dict[str, TokenBucket] = {}
        self._quotas: Dict[str, QuotaInfo] = {}
        self._request_counts: Dict[str, Dict[int, int]] = defaultdict(lambda: defaultdict(int))
        self._lock = threading.Lock()
    
    def get_quota(self, tenant_id: str, plan: str = "free") -> QuotaInfo:
        """获取租户配额"""
        if tenant_id not in self._quotas:
            self._quotas[tenant_id] = QuotaInfo(
                plan=plan,
                daily_limit=self.DAILY_QUOTA.get(plan, 50),
                monthly_limit=self.MONTHLY_QUOTA.get(plan, 500),
            )
        return self._quotas[tenant_id]
    
    def update_quota_usage(self, tenant_id: str, used_today: int = 0, used_month: int = 0):
        """更新配额使用量"""
        quota = self.get_quota(tenant_id)
        quota.used_today = used_today
        quota.used_month = used_month
    
    def check_rate_limit(self, tenant_id: str, tool_id: Optional[str] = None) -> Dict:
        """检查限流状态"""
        quota = self.get_quota(tenant_id)
        plan = quota.plan
        
        config = self.QUOTA_CONFIG.get(plan, self.QUOTA_CONFIG["free"])
        
        # 检查时间窗口
        now = time.time()
        window_start = int(now // config.window_seconds) * config.window_seconds
        
        with self._lock:
            current_count = self._request_counts[tenant_id][window_start]
            
            # 检查日配额
            if quota.used_today >= quota.daily_limit:
                return {
                    "allowed": False,
                    "reason": "daily_limit_exceeded",
                    "quota": quota.to_dict(),
                    "retry_after": self._get_reset_time(quota),
                }
            
            # 检查月配额
            if quota.used_month >= quota.monthly_limit:
                return {
                    "allowed": False,
                    "reason": "monthly_limit_exceeded",
                    "quota": quota.to_dict(),
                }
            
            # 检查瞬时速率
            if current_count >= config.max_requests:
                return {
                    "allowed": False,
                    "reason": "rate_limit_exceeded",
                    "quota": quota.to_dict(),
                    "retry_after": config.window_seconds,
                }
            
            # 允许请求
            self._request_counts[tenant_id][window_start] += 1
            return {
                "allowed": True,
                "quota": quota.to_dict(),
                "current_count": current_count + 1,
                "max_requests": config.max_requests,
            }
    
    def _get_reset_time(self, quota: QuotaInfo) -> int:
        """获取下一个重置时间（秒）"""
        now = time.time()
        tomorrow = (now // 86400 + 1) * 86400
        return int(tomorrow - now)
    
    def consume_credit(self, tenant_id: str, amount: int = 1) -> bool:
        """消耗 Credit"""
        quota = self.get_quota(tenant_id)
        
        with self._lock:
            if quota.used_today + amount > quota.daily_limit:
                return False
            if quota.used_month + amount > quota.monthly_limit:
                return False
            
            quota.used_today += amount
            quota.used_month += amount
            return True
    
    def get_tenant_stats(self, tenant_id: str) -> Dict:
        """获取租户统计"""
        quota = self.get_quota(tenant_id)
        plan = quota.plan
        config = self.QUOTA_CONFIG.get(plan, self.QUOTA_CONFIG["free"])
        
        now = time.time()
        window_start = int(now // config.window_seconds) * config.window_seconds
        
        with self._lock:
            current_window_count = self._request_counts[tenant_id].get(window_start, 0)
        
        return {
            "tenant_id": tenant_id,
            "plan": plan,
            "quota": quota.to_dict(),
            "current_window_requests": current_window_count,
            "rate_limit": config.to_dict(),
        }
    
    def upgrade_plan(self, tenant_id: str, new_plan: str):
        """升级套餐"""
        if new_plan not in self.QUOTA_CONFIG:
            raise ValueError(f"Unknown plan: {new_plan}")
        
        if tenant_id not in self._quotas:
            self._quotas[tenant_id] = QuotaInfo(
                plan=new_plan,
                daily_limit=self.DAILY_QUOTA.get(new_plan, 50),
                monthly_limit=self.MONTHLY_QUOTA.get(new_plan, 500),
            )
        else:
            self._quotas[tenant_id].plan = new_plan
            self._quotas[tenant_id].daily_limit = self.DAILY_QUOTA.get(new_plan, 50)
            self._quotas[tenant_id].monthly_limit = self.MONTHLY_QUOTA.get(new_plan, 500)
    
    def reset_quota(self, tenant_id: str):
        """重置配额（每日/每月）"""
        if tenant_id in self._quotas:
            self._quotas[tenant_id].used_today = 0
            self._quotas[tenant_id].used_month = 0
        
        # 清空请求计数
        with self._lock:
            if tenant_id in self._request_counts:
                del self._request_counts[tenant_id]
