# -*- coding: utf-8 -*-
"""
ChineseTool 基类 - 中文场景工具的公共基础设施

提供统一异常处理、中文文档生成、中文日志格式化等能力，
所有中文场景 Demo 工具均继承此基类。

使用示例::

    from agent_forge.tools.chinese_base import ChineseTool, ChineseToolInputSchema

    class MyTool(ChineseTool):
        tool_id = "my.tool"
        tool_name = "my_tool"
        tool_description = "我的中文工具"
        tool_category = "demo"
        tool_tags = ["示例"]

        def get_input_properties(self):
            return {"query": {"type": "string", "description": "查询内容"}}

        def get_required_fields(self):
            return ["query"]

        def process(self, query: str) -> dict:
            return {"result": f"查询结果: {query}"}
"""

from __future__ import annotations

import logging
import traceback
from abc import abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import ToolBase, ToolInputSchema
from agent_forge.registry import registry

# 中文日志格式化器
logger = logging.getLogger("agent_forge.chinese")


class ChineseToolError(Exception):
    """中文工具统一异常基类"""

    def __init__(self, message: str, code: str = "UNKNOWN_ERROR", details: str = ""):
        self.message = message
        self.code = code
        self.details = details
        super().__init__(self.message)


class ValidationError(ChineseToolError):
    """输入校验异常"""

    def __init__(self, message: str, field: str = ""):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details=f"字段: {field}" if field else "",
        )


class DataNotFoundError(ChineseToolError):
    """数据未找到异常"""

    def __init__(self, message: str = "未找到匹配的数据"):
        super().__init__(message=message, code="DATA_NOT_FOUND")


class ChineseToolInputSchema(ToolInputSchema):
    """中文工具输入 Schema（扩展 ToolInputSchema，增加中文描述支持）"""

    def __init__(
        self,
        properties: Optional[Dict[str, Any]] = None,
        required: Optional[List[str]] = None,
        chinese_description: str = "",
    ):
        super().__init__(properties=properties, required=required)
        self.chinese_description = chinese_description


class ChineseTool(ToolBase):
    """
    中文场景工具抽象基类

    继承 ToolBase，提供：
    - 统一异常捕获与中文错误消息
    - 中文报告/文档生成辅助方法
    - 自动注册到全局 ToolRegistry
    - 输入参数校验
    """

    # 子类必须覆盖的类属性
    tool_id: str = ""
    tool_name: str = ""
    tool_description: str = ""
    tool_category: str = "chinese"
    tool_tags: List[str] = []

    def __init__(self):
        schema = ChineseToolInputSchema(
            properties=self.get_input_properties(),
            required=self.get_required_fields(),
            chinese_description=self.tool_description,
        )
        super().__init__(
            tool_id=self.tool_id,
            name=self.tool_name,
            description=self.tool_description,
            input_schema=schema,
        )
        # 自动注册到全局注册表
        registry.register(
            tool_id=self.tool_id,
            name=self.tool_name,
            description=self.tool_description,
            handler=self.execute,
            input_schema=schema.to_dict(),
            category=self.tool_category,
            tags=self.tool_tags,
        )

    # ── 子类必须实现 ──────────────────────────────────────────

    @abstractmethod
    def get_input_properties(self) -> Dict[str, Any]:
        """返回输入参数的 JSON Schema properties"""
        ...

    @abstractmethod
    def process(self, **kwargs) -> dict:
        """核心业务逻辑，子类实现。返回 dict 结果。"""
        ...

    def get_required_fields(self) -> List[str]:
        """返回必填字段列表，默认空（子类覆盖）"""
        return []

    # ── 公共能力 ──────────────────────────────────────────────

    def execute(self, **kwargs) -> str:
        """
        统一执行入口：校验 → 处理 → 格式化。
        自动捕获异常并返回中文错误信息。
        """
        try:
            self._validate(kwargs)
            result = self.process(**kwargs)
            return self.format_result(result)
        except ChineseToolError as e:
            return self.format_error(e)
        except Exception as e:
            logger.error("工具 %s 执行异常: %s\n%s", self.tool_id, e, traceback.format_exc())
            err = ChineseToolError(
                message=f"工具执行异常: {e}",
                code="RUNTIME_ERROR",
            )
            return self.format_error(err)

    def _validate(self, params: Dict[str, Any]) -> None:
        """校验必填字段"""
        for field_name in self.get_required_fields():
            if field_name not in params or params[field_name] is None:
                raise ValidationError(f"缺少必填参数: {field_name}", field=field_name)

    def format_result(self, data: dict) -> str:
        """将结果 dict 格式化为中文可读字符串"""
        lines = []
        for key, value in data.items():
            cn_key = self._translate_key(key)
            if isinstance(value, list):
                lines.append(f"【{cn_key}】")
                for item in value:
                    if isinstance(item, dict):
                        sub = ", ".join(f"{k}={v}" for k, v in item.items())
                        lines.append(f"  • {sub}")
                    else:
                        lines.append(f"  • {item}")
            elif isinstance(value, dict):
                lines.append(f"【{cn_key}】")
                for sub_k, sub_v in value.items():
                    lines.append(f"  {sub_k}: {sub_v}")
            else:
                lines.append(f"【{cn_key}】{value}")
        return "\n".join(lines)

    def format_error(self, error: ChineseToolError) -> str:
        """格式化错误信息为中文"""
        return f"[错误-{error.code}] {error.message}" + (
            f" ({error.details})" if error.details else ""
        )

    @staticmethod
    def generate_report(
        title: str,
        sections: List[Dict[str, Any]],
        author: str = "agent-forge",
    ) -> str:
        """
        生成中文 Markdown 报告

        Args:
            title: 报告标题
            sections: 报告段落列表，每项包含 heading 和 content
            author: 作者

        Returns:
            格式化的 Markdown 字符串
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = [
            f"# {title}",
            f"",
            f"> 生成时间: {now}  ",
            f"> 作者: {author}  ",
            f"> 框架: agent-forge v0.1.0",
            "",
            "---",
            "",
        ]
        for section in sections:
            heading = section.get("heading", "")
            content = section.get("content", "")
            lines.append(f"## {heading}")
            lines.append("")
            if isinstance(content, list):
                for item in content:
                    lines.append(f"- {item}")
            else:
                lines.append(str(content))
            lines.append("")
        lines.append("---")
        lines.append("*本报告由 agent-forge 自动生成*")
        return "\n".join(lines)

    @staticmethod
    def _translate_key(key: str) -> str:
        """简单的键名中文映射（子类可覆盖扩展）"""
        mapping = {
            "query": "查询条件",
            "result": "结果",
            "count": "数量",
            "status": "状态",
            "data": "数据",
            "message": "消息",
            "items": "条目",
            "summary": "摘要",
            "details": "详情",
            "score": "评分",
            "level": "级别",
            "time": "时间",
            "source": "来源",
            "signal": "信号",
            "risk": "风险",
            "confidence": "置信度",
            "total": "总计",
            "passed": "通过",
            "failed": "未通过",
            "warnings": "警告",
        }
        return mapping.get(key, key)
