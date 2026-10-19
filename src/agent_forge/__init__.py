# -*- coding: utf-8 -*-
"""
Agent-Forge: MCP 工具生态框架
提供 634K 工具的统一注册、发现与调用能力。
"""

__version__ = "0.1.0"
__author__ = "Zeon7744"

from .server import MCPServer, run_server
from .registry import ToolRegistry, ToolMeta, registry

__all__ = [
    "MCPServer",
    "run_server",
    "ToolRegistry",
    "ToolMeta",
    "registry",
]
