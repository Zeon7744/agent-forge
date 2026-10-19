# -*- coding: utf-8 -*-
"""
工具注册表 - 管理工具的生命周期
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import time


@dataclass
class ToolMeta:
    """工具元数据"""
    tool_id: str
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Optional[Dict[str, Any]] = None
    version: str = "1.0.0"
    category: str = "general"
    tags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    is_active: bool = True


class ToolRegistry:
    """工具注册与发现管理器"""
    
    def __init__(self):
        self._tools: Dict[str, ToolMeta] = {}
        self._handlers: Dict[str, Callable] = {}
    
    def register(
        self,
        tool_id: str,
        name: str,
        description: str,
        handler: Callable,
        input_schema: Dict[str, Any],
        output_schema: Optional[Dict[str, Any]] = None,
        version: str = "1.0.0",
        category: str = "general",
        tags: Optional[List[str]] = None,
    ) -> str:
        """注册工具，返回 tool_id"""
        meta = ToolMeta(
            tool_id=tool_id,
            name=name,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
            version=version,
            category=category,
            tags=tags or [],
        )
        self._tools[tool_id] = meta
        self._handlers[tool_id] = handler
        return tool_id
    
    def unregister(self, tool_id: str) -> bool:
        """注销工具"""
        if tool_id in self._tools:
            del self._tools[tool_id]
            del self._handlers[tool_id]
            return True
        return False
    
    def discover(self) -> Dict[str, ToolMeta]:
        """能力发现，返回所有活跃工具"""
        return {
            tid: meta for tid, meta in self._tools.items()
            if meta.is_active
        }
    
    def list(self) -> List[Dict[str, Any]]:
        """列出工具列表（MCP tools/list 格式）"""
        return [
            {
                "name": meta.name,
                "description": meta.description,
                "inputSchema": meta.input_schema,
                "version": meta.version,
                "category": meta.category,
                "tags": meta.tags,
            }
            for meta in self._tools.values()
            if meta.is_active
        ]
    
    def call(self, tool_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """调用工具"""
        if tool_id not in self._handlers:
            return {
                "error": f"Tool not found: {tool_id}",
                "status": "not_found",
            }
        handler = self._handlers[tool_id]
        try:
            result = handler(**params)
            return {
                "content": [{"type": "text", "text": str(result)}],
                "status": "success",
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "error",
            }
    
    def get(self, tool_id: str) -> Optional[ToolMeta]:
        """获取工具元数据"""
        return self._tools.get(tool_id)
    
    def count(self) -> int:
        """返回注册工具数量"""
        return len([t for t in self._tools.values() if t.is_active])


# 全局注册表实例
registry = ToolRegistry()
