# -*- coding: utf-8 -*-
"""
Demo 3 单元测试
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples"))

from demo_3_content_audit import ContentAuditTool, SENSITIVE_WORDS, ALL_SENSITIVE_TERMS


class TestContentAuditTool:
    """内容安全审核工具测试"""

    @pytest.fixture
    def tool(self):
        return ContentAuditTool()

    @pytest.fixture
    def clean_text(self):
        return "这是一段正常的测试文本，没有任何违规内容"

    @pytest.fixture
    def flagged_text(self):
        """使用真实在词库中的敏感词构造测试文本"""
        # 从词库中取第一个分类的第一个词
        first_cat = list(SENSITIVE_WORDS.keys())[0]
        first_word = SENSITIVE_WORDS[first_cat][0]
        return f"这是一段包含{first_word}的测试文本"

    def test_process_clean_text(self, tool, clean_text):
        """测试正常文本处理"""
        result = tool.process(clean_text)
        assert result["risk_score"] == 0
        assert result["risk_level"] == "无风险"
        assert result["findings_count"] == 0

    def test_process_flagged_text(self, tool, flagged_text):
        """测试违规文本处理"""
        result = tool.process(flagged_text)
        assert result["findings_count"] > 0
        assert result["risk_score"] > 0

    def test_process_empty_text_raises_error(self, tool):
        """测试空文本异常"""
        from agent_forge.tools.chinese_base import ValidationError
        with pytest.raises(ValidationError):
            tool.process("")

    def test_filter_text(self, tool):
        """测试文本过滤 - 敏感词应被替换"""
        first_cat = list(SENSITIVE_WORDS.keys())[0]
        first_word = SENSITIVE_WORDS[first_cat][0]
        text = f"包含{first_word}的文本"
        filtered = tool.filter_text(text, level="全部")
        assert first_word not in filtered
        assert "***" in filtered or "****" in filtered or "***" in filtered

    def test_filter_text_preserve_clean(self, tool, clean_text):
        """测试正常文本不被修改"""
        filtered = tool.filter_text(clean_text)
        assert filtered == clean_text

    def test_generate_audit_report(self, tool, clean_text):
        """测试报告生成"""
        report = tool.generate_audit_report(clean_text)
        assert isinstance(report, str)
        assert "内容安全审核报告" in report
        assert "审核概览" in report

    def test_classify_risk_levels(self, tool):
        """测试风险等级分类"""
        assert tool._classify_risk(0) == "无风险"
        assert tool._classify_risk(9) == "无风险"
        assert tool._classify_risk(10) == "低风险"
        assert tool._classify_risk(15) == "低风险"
        assert tool._classify_risk(50) == "中风险"
        assert tool._classify_risk(55) == "中风险"
        assert tool._classify_risk(80) == "高风险"
        assert tool._classify_risk(85) == "高风险"

    def test_detect_sensitive_by_category(self, tool):
        """测试按类别检测"""
        first_cat = list(SENSITIVE_WORDS.keys())[0]
        first_word = SENSITIVE_WORDS[first_cat][0]
        text = f"包含{first_word}的文本"
        findings = tool._detect_sensitive(text, first_cat)
        assert isinstance(findings, list)
        assert len(findings) > 0
        assert findings[0]["word"] == first_word

    def test_strict_mode_increases_score(self, tool):
        """测试严格模式提高风险分"""
        first_cat = list(SENSITIVE_WORDS.keys())[0]
        first_word = SENSITIVE_WORDS[first_cat][0]
        text = f"包含{first_word}的文本"
        result_normal = tool.process(text, strict=False)
        result_strict = tool.process(text, strict=True)
        assert result_strict["risk_score"] >= result_normal["risk_score"]

    def test_recommendations_for_clean_text(self, tool, clean_text):
        """测试正常文本的建议"""
        result = tool.process(clean_text)
        recs = result["recommendations"]
        assert any("通过审核" in r for r in recs)

    def test_tool_registered(self, tool):
        """测试工具已注册到全局注册表"""
        from agent_forge.registry import registry
        meta = registry.get("content.audit")
        assert meta is not None
        assert meta.name == "audit_content"
