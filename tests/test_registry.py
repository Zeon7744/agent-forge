# -*- coding: utf-8 -*-
"""工具注册表测试"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent_forge.registry import ToolRegistry, ToolMeta


def test_register_and_discover():
    """测试工具注册和发现"""
    registry = ToolRegistry()
    
    def dummy_handler(x: str) -> str:
        return f"handled: {x}"
    
    tool_id = registry.register(
        tool_id="test.hello",
        name="hello",
        description="A test tool",
        handler=dummy_handler,
        input_schema={"type": "object", "properties": {"x": {"type": "string"}}},
        category="test",
    )
    
    assert tool_id == "test.hello"
    assert registry.count() == 1
    
    discovered = registry.discover()
    assert "test.hello" in discovered
    assert discovered["test.hello"].name == "hello"


def test_call_tool():
    """测试工具调用"""
    registry = ToolRegistry()
    
    def echo(text: str) -> str:
        return f"echo: {text}"
    
    registry.register(
        tool_id="test.echo",
        name="echo",
        description="Echo tool",
        handler=echo,
        input_schema={"type": "object", "properties": {"text": {"type": "string"}}},
    )
    
    result = registry.call("test.echo", {"text": "hello"})
    assert result["status"] == "success"
    assert "echo: hello" in result["content"][0]["text"]


def test_call_missing_tool():
    """测试调用不存在的工具"""
    registry = ToolRegistry()
    result = registry.call("nonexistent", {})
    assert result["status"] == "not_found"


def test_unregister():
    """测试工具注销"""
    registry = ToolRegistry()
    
    def dummy(x: str) -> str:
        return x
    
    registry.register("test.remove", "remove", "Remove tool", dummy, {"type": "object"})
    assert registry.count() == 1
    
    registry.unregister("test.remove")
    assert registry.count() == 0


if __name__ == "__main__":
    test_register_and_discover()
    test_call_tool()
    test_call_missing_tool()
    test_unregister()
    print("所有测试通过")
