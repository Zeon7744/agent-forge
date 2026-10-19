# Agent-Forge 技术架构设计文档

**版本：** v0.1.0  
**日期：** 2026-10-19  
**作者：** 编程专家_661

---

## 一、项目概述

### 1.1 背景
Agent-Forge 是一个面向 634K 工具生态的 MCP（Model Context Protocol）框架，提供：
- 统一的工具注册与发现机制
- 多协议支持（HTTP Streamable / SSE / stdio）
- 插件化架构，支持热加载工具
- 与 jianzhu-saas 收款系统无缝集成

### 1.2 目标
1. **标准化**：遵循 MCP 2026-07-28 协议规范
2. **可扩展**：支持动态工具注册/注销
3. **可观测**：内置请求日志、性能监控、错误追踪
4. **可商用**：集成爱发电/微信商户收款网关

---

## 二、技术架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     Agent-Forge Core                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  MCP Server  │  │ Tool Registry │  │  PluginMgr   │      │
│  │  (HTTP/SSE)  │  │   (内存/DB)   │  │  (热加载)    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │               │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐      │
│  │  Protocol    │  │  Tool Base   │  │  Gateway     │      │
│  │  Handler     │  │  Class       │  │  (爱发电/微信)│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│  Ecosystem Layer (634K Tools)                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Text Tools  │  │  Code Tools  │  │  Data Tools  │      │
│  │  (分类/格式)  │  │  (分析/生成)  │  │  (统计/可视化)│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 核心模块

| 模块 | 职责 | 技术栈 |
|------|------|--------|
| `server.py` | HTTP/SSE 服务器，协议处理 | http.server, json |
| `registry.py` | 工具注册、发现、元数据管理 | dataclass, dict |
| `plugin.py` | 插件热加载、版本管理 | importlib, pkg_resources |
| `gateway/` | 收款网关抽象层 | urllib.request, hmac |
| `tools/` | 工具实现库 | 标准库 + 可选第三方 |

### 2.3 目录结构

```
agent-forge/
├── docs/
│   ├── architecture.md      # 本文档
│   ├── api-reference.md     # API 参考
│   └── deployment.md        # 部署指南
├── src/
│   └── agent_forge/
│       ├── __init__.py
│       ├── server.py        # MCP 服务器主入口
│       ├── registry.py      # 工具注册表
│       ├── plugin.py        # 插件管理器
│       ├── gateway/         # 收款网关
│       │   ├── __init__.py
│       │   ├── base.py      # Gateway 基类
│       │   ├── afdian.py    # 爱发电
│       │   └── wxpay.py     # 微信商户
│       └── tools/           # 工具实现
│           ├── __init__.py
│           ├── base.py      # ToolBase 基类
│           ├── text.py      # 文本处理工具
│           ├── code.py      # 代码分析工具
│           └── data.py      # 数据分析工具
├── tests/
│   ├── test_registry.py
│   ├── test_gateway.py
│   └── test_tools.py
├── examples/
│   └── hello_world.py
├── .mcp.json                # MCP 配置
├── pyproject.toml           # 项目配置
├── requirements.txt         # 依赖清单
└── README.md
```

---

## 三、核心设计

### 3.1 MCP 协议实现

遵循 MCP 2026-07-28 规范：

```python
# 支持的 RPC 方法
SUPPORTED_METHODS = {
    "server/discover": "能力发现",
    "tools/list": "列出可用工具",
    "tools/call": "调用工具",
    "resources/list": "列出资源",
    "prompts/list": "列出提示模板",
}

# 请求处理流程
POST /mcp
  Header: Mcp-Method: tools/call
  Header: Mcp-Name: <tool_name>
  Body: { "params": {...} }
  
Response:
  { "result": { "content": [...] } }
```

### 3.2 工具注册表

```python
class ToolRegistry:
    """工具注册与发现"""
    
    def register(self, tool: ToolBase) -> str:
        """注册工具，返回 tool_id"""
        
    def discover(self) -> Dict[str, ToolMeta]:
        """能力发现，返回所有工具元数据"""
        
    def call(self, tool_id: str, params: Dict) -> Dict:
        """调用工具"""
        
    def list(self) -> List[ToolMeta]:
        """列出所有工具"""
```

### 3.3 收款网关集成

复用 jianzhu-saas/billing.py 架构：

```python
# 网关选择
JZ_SAAS_BILLING_GATEWAY=afdian  # 或 wxpay/aishouqian/noop

# 爱发电配置
JZ_SAAS_AFDIAN_USER=0c59dda8a1bb11f19b9552540025c377
JZ_SAAS_AFDIAN_TOKEN=mvBuAfHU3JnVbX8wq45KTWMRh6rgtkcP
JZ_SAAS_AFDIAN_RETURN=https://example.com/success
```

---

## 四、依赖管理

### 4.1 核心依赖（requirements.txt）

```txt
# Agent-Forge 核心依赖
mcp>=1.0.0              # MCP SDK
typer>=0.9.0            # CLI 框架
rich>=13.0.0            # 终端富文本
pyyaml>=6.0             # 配置解析
jsonschema>=4.17.0      # Schema 验证
```

### 4.2 可选依赖

```txt
# AI 能力（可选）
openai>=1.0.0
anthropic>=0.18.0

# 开发工具（可选）
pytest>=7.0
pytest-cov>=4.0
black>=23.0
ruff>=0.1.0
```

### 4.3 依赖隔离策略

- **核心依赖**：标准库 + 轻量级第三方
- **AI 依赖**：optional extras，不强制安装
- **开发依赖**：dev extras，分离管理

---

## 五、测试策略

### 5.1 测试分层

| 层级 | 工具 | 覆盖范围 |
|------|------|---------|
| 单元测试 | pytest | 工具函数、网关逻辑 |
| 集成测试 | pytest + testclient | MCP 协议、端到端流程 |
| 性能测试 | locust | 并发请求、吞吐量 |

### 5.2 测试覆盖率目标

- 核心模块：>=90%
- 工具实现：>=80%
- 网关模块：>=95%

### 5.3 CI/CD

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e ".[dev]"
      - run: pytest --cov=src/agent_forge -v
      - run: coverage report --fail-under=90
```

---

## 六、部署方案

### 6.1 单机部署

```bash
# 安装
pip install -e ".[dev]"

# 启动 MCP 服务器
python -m agent_forge.server --port 8000

# 或作为模块导入
from agent_forge import MCPClient
client = MCPClient("http://localhost:8000")
```

### 6.2 Docker 部署

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -e ".[prod]"
EXPOSE 8000
CMD ["python", "-m", "agent_forge.server", "--port", "8000"]
```

### 6.3 与 jianzhu-saas 集成

```python
# 方式 1：直接引用
import sys
sys.path.insert(0, "../jianzhu-saas")
from billing import get_gateway

# 方式 2：symlink（推荐）
# ln -s ../jianzhu-saas/billing.py billing.py
# ln -s ../jianzhu-saas/store.py store.py
```

---

## 七、演进路线

| 阶段 | 目标 | 时间 |
|------|------|------|
| v0.1 | 核心框架 + 基础工具 | 2026-10 |
| v0.5 | 完整 MCP 协议 + 插件系统 | 2026-11 |
| v1.0 | 生产就绪 + 收款集成 | 2026-12 |
| v2.0 | 分布式工具市场 | 2027-Q1 |

---

**文档维护：** 编程专家_661  
**更新日志：** 见 CHANGELOG.md
