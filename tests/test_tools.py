# -*- coding: utf-8 -*-
"""工具测试"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent_forge.tools.text import TextClassifierTool, TextFormatterTool
from agent_forge.tools.data import DataStatsTool


def test_text_classifier():
    """测试文本分类工具"""
    tool = TextClassifierTool()
    result = tool.execute("这是一段测试文本")
    assert len(result) > 0


def test_text_formatter():
    """测试文本格式化工具"""
    tool = TextFormatterTool()
    
    # Markdown 格式
    result = tool.execute("hello", format="markdown")
    assert "```" in result
    
    # JSON 格式
    result = tool.execute('{"a": 1}', format="json")
    assert "a" in result


def test_data_stats():
    """测试数据统计工具"""
    tool = DataStatsTool()
    result = tool.execute([1, 2, 3, 4, 5])
    assert "mean" in result.lower() or len(result) > 0


if __name__ == "__main__":
    test_text_classifier()
    test_text_formatter()
    test_data_stats()
    print("所有工具测试通过")
