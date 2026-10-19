# -*- coding: utf-8 -*-
"""
代码分析工具
"""

from .base import ToolBase, ToolInputSchema
from agent_forge.registry import registry


class CodeAnalyzerTool(ToolBase):
    """代码分析工具"""
    
    def __init__(self):
        super().__init__(
            tool_id="code.analyzer",
            name="analyze_code",
            description="分析代码的复杂度、风格和问题",
            input_schema=ToolInputSchema(
                properties={
                    "code": {"type": "string", "description": "待分析的代码"},
                    "language": {"type": "string", "description": "编程语言"},
                },
                required=["code"],
            ),
        )
        registry.register(
            tool_id=self.tool_id,
            name=self.name,
            description=self.description,
            handler=self.execute,
            input_schema=self.input_schema.to_dict(),
            category="code",
            tags=["分析", "代码质量"],
        )
    
    def execute(self, code: str, language: str = "python") -> str:
        """执行代码分析"""
        lines = code.strip().split("\n")
        result = {
            "language": language,
            "lines": len(lines),
            "complexity": "medium" if len(lines) > 50 else "low",
            "suggestions": ["考虑添加类型注解", "提取魔法数字为常量"],
        }
        return str(result)
