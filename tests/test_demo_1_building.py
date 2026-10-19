# -*- coding: utf-8 -*-
"""
Demo 1 单元测试
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples"))

from demo_1_building_code import BuildingCodeTool, GB_DATABASE


class TestBuildingCodeTool:
    """建筑规范查询工具测试"""

    @pytest.fixture
    def tool(self):
        return BuildingCodeTool()

    def test_search_by_code(self, tool):
        """按标准号搜索"""
        result = tool.process(code="GB50016")
        assert result["count"] == 1
        assert result["items"][0]["code"] == "GB50016-2014"

    def test_search_by_keyword(self, tool):
        """按关键词搜索"""
        result = tool.process(keyword="防火")
        assert result["count"] >= 2  # 至少有防火类规范

    def test_search_by_category(self, tool):
        """按分类筛选"""
        result = tool.process(category="结构")
        assert result["count"] > 0
        for item in result["items"]:
            assert item["category"] == "结构"

    def test_list_categories(self):
        """列出所有分类"""
        cats = BuildingCodeTool.list_categories()
        assert isinstance(cats, list)
        assert "防火" in cats
        assert "结构" in cats

    def test_generate_compliance_report(self, tool):
        """生成合规报告"""
        report = tool.generate_compliance_report("防火")
        assert isinstance(report, str)
        assert "建筑规范合规检查报告" in report
        assert "防火" in report

    def test_database_has_data(self):
        """数据库非空"""
        assert len(GB_DATABASE) > 0

    def test_invalid_code_raises_error(self, tool):
        """无效标准号应抛出异常"""
        from agent_forge.tools.chinese_base import DataNotFoundError
        with pytest.raises(DataNotFoundError):
            tool.process(code="GB99999")
