# -*- coding: utf-8 -*-
"""
Agent-Forge 快速入门示例
演示工具注册、发现和调用
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent_forge.registry import ToolRegistry
from agent_forge.tools.text import TextClassifierTool, TextFormatterTool
from agent_forge.tools.data import DataStatsTool


def main():
    """主入口"""
    print("=" * 50)
    print("Agent-Forge 工具生态框架 v0.1.0")
    print("=" * 50)
    
    # 工具会自动注册到全局 registry
    # 初始化工具
    classifier = TextClassifierTool()
    formatter = TextFormatterTool()
    stats = DataStatsTool()
    
    # 查看已注册工具
    from agent_forge.registry import registry
    print(f"\n已注册工具数: {registry.count()}")
    
    # 列出工具
    print("\n可用工具:")
    for tool in registry.list():
        print(f"  - {tool['name']} ({tool['category']})")
    
    # 调用工具
    print("\n--- 测试文本分类 ---")
    result = registry.call("text.classifier", {"text": "Python 编程教程"})
    print(f"结果: {result}")
    
    print("\n--- 测试文本格式化 ---")
    result = registry.call("text.formatter", {"text": '{"key": "value"}', "format": "markdown"})
    print(f"结果: {result}")
    
    print("\n--- 测试数据统计 ---")
    result = registry.call("data.stats", {"data": [10, 20, 30, 40, 50]})
    print(f"结果: {result}")
    
    print("\n" + "=" * 50)
    print("快速入门完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
