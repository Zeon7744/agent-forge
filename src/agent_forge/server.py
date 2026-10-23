# -*- coding: utf-8 -*-
"""
MCP 服务器 - HTTP Streamable 协议实现
"""

from __future__ import annotations
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from typing import Any, Dict

from .registry import registry
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
try:
    import billing
except ImportError:
    billing = None

# MCP 协议常量
MCP_PROTOCOL_VERSION = "2026-07-28"
MCP_HEADER_METHOD = "Mcp-Method"
MCP_HEADER_NAME = "Mcp-Name"

SUPPORTED_METHODS = {
    "server/discover": "能力发现",
    "tools/list": "列出可用工具",
    "tools/call": "调用工具",
    "resources/list": "列出资源（预留）",
    "prompts/list": "列出提示模板（预留）",
}


class MCPRequestHandler(BaseHTTPRequestHandler):
    """MCP HTTP 请求处理器"""
    
    def do_POST(self):
        """处理 POST 请求"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON"})
            return
        
        method = self.headers.get(MCP_HEADER_METHOD, "")
        
        if method == "tools/list":
            result = self._handle_tools_list()
        elif method == "tools/call":
            result = self._handle_tools_call(payload)
        elif method == "server/discover":
            result = self._handle_server_discover()
        else:
            result = {"error": f"Unknown method: {method}"}
        
        self._send_json(200, result)
    
    def do_GET(self):
        """处理 GET 请求（用于 discover）"""
        parsed = urlparse(self.path)
        if parsed.path in ("/mcp", "/"):
            result = self._handle_server_discover()
            self._send_json(200, result)
        else:
            self._send_json(404, {"error": "Not found"})
    
    def _handle_server_discover(self) -> Dict:
        """服务器能力发现"""
        return {
            "protocolVersion": MCP_PROTOCOL_VERSION,
            "serverInfo": {
                "name": "agent-forge",
                "version": "0.1.0",
            },
            "methods": list(SUPPORTED_METHODS.keys()),
            "tools": {
                "count": registry.count(),
                "list": registry.list(),
            },
        }
    
    def _handle_tools_list(self) -> Dict:
        """列出可用工具"""
        return {
            "tools": registry.list(),
            "count": registry.count(),
        }
    
    def _handle_tools_call(self, payload: Dict) -> Dict:
        """调用工具"""
        tool_id = payload.get("tool_id", "")
        params = payload.get("params", {})
        
        if not tool_id:
            return {"error": "tool_id is required"}
        
        return registry.call(tool_id, params)
    
    def _send_json(self, status: int, data: Dict):
        """发送 JSON 响应"""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[MCP] {self.log_date_time_string()} {format % args}")


class MCPServer:
    """MCP 服务器封装"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port
        self._server: HTTPServer | None = None
    
    def start(self):
        """启动服务器"""
        self._server = HTTPServer((self.host, self.port), MCPRequestHandler)
        print(f"Agent-Forge MCP Server running on http://{self.host}:{self.port}")
        print(f"Protocol: {MCP_PROTOCOL_VERSION}")
        print(f"Tools registered: {registry.count()}")
        self._server.serve_forever()
    
    def stop(self):
        """停止服务器"""
        if self._server:
            self._server.shutdown()
            self._server = None


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """启动 MCP 服务器（命令行入口）"""
    server = MCPServer(host, port)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.stop()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Agent-Forge MCP Server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    run_server(args.host, args.port)
