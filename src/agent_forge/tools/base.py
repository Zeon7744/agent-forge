# -*- coding: utf-8 -*-
"""
工具基类
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ToolInputSchema:
    """工具输入 Schema"""
    type: str = "object"
    properties: Dict[str, Any] = None
    required: List[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        schema = {"type": self.type}
        if self.properties:
            schema["properties"] = self.properties
        if self.required:
            schema["required"] = self.required
        return schema


class ToolBase(ABC):
    """工具抽象基类"""
    
    def __init__(self, tool_id: str, name: str, description: str, input_schema: ToolInputSchema):
        self.tool_id = tool_id
        self.name = name
        self.description = description
        self.input_schema = input_schema
    
    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Any:
        """执行工具逻辑"""
        pass
    
    def to_mcp_format(self) -> Dict[str, Any]:
        """转换为 MCP 格式"""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema.to_dict(),
        }
