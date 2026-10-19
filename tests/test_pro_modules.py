# -*- coding: utf-8 -*-
"""Pro 功能模块测试"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent_forge.tools.marketplace import Marketplace, SkillMeta
from agent_forge.tools.analytics import AnalyticsEngine
from agent_forge.tools.rate_limiter import RateLimiter


def test_marketplace_register():
    """测试市场注册"""
    market = Marketplace()
    
    skill = SkillMeta(
        skill_id="test.hello",
        name="Hello World",
        description="A test skill",
        version="1.0.0",
        author="Test Author",
        tags=["test", "hello"],
    )
    
    market.register(skill)
    assert "test.hello" in market._skills
    
    listed = market.list()
    assert listed["total"] == 1
    assert listed["skills"][0]["name"] == "Hello World"


def test_marketplace_search():
    """测试市场搜索"""
    market = Marketplace()
    
    market.register(SkillMeta(
        skill_id="test.a",
        name="AI Classifier",
        description="AI 文本分类工具",
        version="1.0.0",
        author="Author",
        tags=["ai", "classifier"],
    ))
    
    # 搜索 "ai"（英文匹配 name）
    results = market.search("ai")
    assert len(results) > 0
    assert results[0]["name"] == "AI Classifier"
    
    # 搜索 "分类"（中文匹配 description）
    results_zh = market.search("分类")
    assert len(results_zh) > 0


def test_analytics_record():
    """测试分析记录"""
    engine = AnalyticsEngine()
    
    engine.record_call(
        tool_id="test.tool",
        params={"text": "hello"},
        result={"output": "world"},
        duration_ms=50.0,
        success=True,
    )
    
    stats = engine.get_tool_stats("test.tool")
    assert stats["total_calls"] == 1
    assert stats["avg_duration_ms"] == 50.0


def test_analytics_suggestions():
    """测试优化建议"""
    engine = AnalyticsEngine()
    
    # 模拟高错误率
    for i in range(10):
        engine.record_call("slow.tool", {}, "ok", 2000.0, success=(i < 2))
    
    suggestions = engine.get_optimization_suggestions()
    assert any(s["tool_id"] == "slow.tool" for s in suggestions)


def test_rate_limiter_free():
    """测试免费套餐限流"""
    limiter = RateLimiter()
    
    # 免费用户每日限制 50 次
    quota = limiter.get_quota("tenant_free", "free")
    assert quota.daily_limit == 50
    
    # 消耗额度
    for i in range(50):
        limiter.consume_credit("tenant_free")
    
    # 超过限制
    assert not limiter.consume_credit("tenant_free")
    
    stats = limiter.get_tenant_stats("tenant_free")
    assert stats["quota"]["used_today"] == 50


def test_rate_limiter_pro():
    """测试 Pro 套餐"""
    limiter = RateLimiter()
    
    limiter.upgrade_plan("tenant_pro", "pro")
    quota = limiter.get_quota("tenant_pro", "pro")
    assert quota.daily_limit == 5000


def test_rate_limiter_enterprise():
    """测试企业套餐"""
    limiter = RateLimiter()
    
    limiter.upgrade_plan("tenant_ent", "enterprise")
    quota = limiter.get_quota("tenant_ent", "enterprise")
    assert quota.daily_limit == 100000


def test_check_rate_limit():
    """测试限流检查"""
    limiter = RateLimiter()
    
    result = limiter.check_rate_limit("tenant1", "test.tool")
    assert result["allowed"] is True
    assert "quota" in result


def test_marketplace_stats():
    """测试市场统计"""
    market = Marketplace()
    
    market.register(SkillMeta(
        skill_id="s1", name="A", description="d",
        version="1.0", author="a", tags=["t"],
    ))
    market.register(SkillMeta(
        skill_id="s2", name="B", description="d",
        version="1.0", author="a", tags=["t"],
    ))
    
    stats = market.stats()
    assert stats["total_skills"] == 2


def test_analytics_export():
    """测试分析报告导出"""
    engine = AnalyticsEngine()
    engine.record_call("tool1", {}, "ok", 100.0)
    
    json_report = engine.export_report("json")
    assert "tool1" in json_report
    
    md_report = engine.export_report("md")
    assert "# Agent-Forge" in md_report


if __name__ == "__main__":
    test_marketplace_register()
    test_marketplace_search()
    test_analytics_record()
    test_analytics_suggestions()
    test_rate_limiter_free()
    test_rate_limiter_pro()
    test_rate_limiter_enterprise()
    test_check_rate_limit()
    test_marketplace_stats()
    test_analytics_export()
    print("✅ 所有 Pro 模块测试通过")
