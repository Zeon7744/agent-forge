# -*- coding: utf-8 -*-
"""
文本处理工具
"""

from .base import ToolBase, ToolInputSchema
from agent_forge.registry import registry


class TextClassifierTool(ToolBase):
    """文本分类工具"""
    
    def __init__(self):
        super().__init__(
            tool_id="text.classifier",
            name="classify_text",
            description="对文本进行多标签分类",
            input_schema=ToolInputSchema(
                properties={
                    "text": {"type": "string", "description": "待分类的文本"},
                    "categories": {"type": "array", "items": {"type": "string"}, "description": "可选的分类列表"},
                },
                required=["text"],
            ),
        )
        registry.register(
            tool_id=self.tool_id,
            name=self.name,
            description=self.description,
            handler=self.execute,
            input_schema=self.input_schema.to_dict(),
            category="text",
            tags=["分类", "NLP"],
        )
    
    def execute(self, text: str, categories: list = None) -> str:
        """执行文本分类"""
        # 简化版分类逻辑（实际应接入 ML 模型）
        result = {
            "text": text[:50] + "..." if len(text) > 50 else text,
            "categories": categories or ["general", "technical"],
            "confidence": 0.85,
        }
        return str(result)


class TextFormatterTool(ToolBase):
    """文本格式化工具"""
    
    def __init__(self):
        super().__init__(
            tool_id="text.formatter",
            name="format_text",
            description="将文本格式化为指定格式（Markdown/JSON/CSV）",
            input_schema=ToolInputSchema(
                properties={
                    "text": {"type": "string", "description": "待格式化的文本"},
                    "format": {"type": "string", "enum": ["markdown", "json", "csv"], "description": "目标格式"},
                },
                required=["text", "format"],
            ),
        )
        registry.register(
            tool_id=self.tool_id,
            name=self.name,
            description=self.description,
            handler=self.execute,
            input_schema=self.input_schema.to_dict(),
            category="text",
            tags=["格式化", "转换"],
        )
    
    def execute(self, text: str, format: str) -> str:
        """执行文本格式化"""
        if format == "json":
            try:
                import json
                data = json.loads(text)
                return json.dumps(data, indent=2, ensure_ascii=False)
            except:
                return json.dumps({"raw": text}, indent=2)
        elif format == "markdown":
            return f"```\n{text}\n```"
        else:
            return text
