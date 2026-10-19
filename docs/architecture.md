# Agent-Forge 技术架构设计文档

**版本：** v0.2.0  
**日期：** 2026-10-19  
**作者：** 编程专家_661（基于运营专家市场分析报告）

---

## 一、项目定位与机会分析

### 1.1 市场机会

**核心痛点**：
- GitHub 工具生态日增 1,719 个工具，但 Skills/MCP 开发工具链几乎空白
- 中文 MCP Server 稀缺（14K+ MCP Servers 中中文垂直场景 < 5%）
- MCP token 开销问题（5 个 Server 消耗 55K tokens，占 200K 模型的 27%）

**差异化定位**：
> agent-forge — 中文 AI Agent 的工具链标准框架，填补 634K 工具生态的中文框架空白

### 1.2 竞品对比矩阵

| 框架 | 语言 | Stars | 核心特点 | agent-forge 追赶策略 |
|------|------|-------|---------|-------------------|
| **FastMCP** | Python | 25K+ | 装饰器语法，开箱即用 | 提供中文适配 + Skills 生命周期管理 |
| **Official MCP SDK** | TS/Py/Go | 12K+ | 协议最准确 | 兼容层 + 中文文档 |
| **Mastra** | TypeScript | 15K+ | Agent runtime + MCP | 聚焦垂直场景（建筑/金融/内容审核） |
| **Vercel AI SDK** | TypeScript | 20K+ | Streamable UI | 提供 Context 压缩优化 |
| **LangChain** | Python/TS | 85K+ | 生态最大 | 不做通用框架，做垂直工具链 |

### 1.3 变现路径验证

| 档位 | 价格 | 目标用户 | 验证结论 |
|------|------|---------|---------|
| **免费** | ¥0 | 个人开发者 | ✅ 低门槛引流 |
| **Pro** | ¥99/月 | 中小企业 | ✅ 符合 SaaS 工具定价区间 |
| **企业** | 定制 | 大型企业 | ⚠️ 需验证支付意愿 |

---

## 二、技术架构设计

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent-Forge Core                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  CLI Forge   │  │ MCP Server   │  │  Skill Mgr   │      │
│  │  (Typer)     │  │ (FastMCP兼容)│  │  (生命周期)   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │               │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐      │
│  │ Tool Registry│  │ Gateway Layer│  │  Context Opt │      │
│  │  (PostgreSQL)│  │ (爱发电/微信) │  │  (预筛+压缩) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│  Ecosystem Layer (634K Tools)                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Text Tools  │  │  Code Tools  │  │  Data Tools  │      │
│  │  (分类/格式)  │  │  (分析/生成)  │  │  (统计/可视化)│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 技术栈选型

| 层级 | 技术选型 | 理由 |
|------|---------|------|
| **核心框架** | Python 3.10+ + FastMCP 兼容层 | 中文开发者 Python 占比高，降低学习成本 |
| **CLI** | Typer | 轻量、快速启动，自动生成帮助文档 |
| **MCP 协议** | MCP 2026-07-28 + FastMCP 兼容 | 兼容官方协议，支持装饰器语法 |
| **注册表** | PostgreSQL + FastAPI | 成熟稳定，支持 RBAC |
| **安全沙箱** | Docker + gVisor | 企业级隔离 |
| **文档** | Docusaurus + 中文 i18n | 双语言支持 |

---

## 三、核心模块设计

### 3.1 CLI 脚手架 (forge)

```bash
# 常用命令
forge create my-skill              # 创建新 Skill
forge test my-skill                # 测试 Skill
forge publish my-skill             # 发布到注册表
forge serve --port 8000            # 启动 MCP 服务器
forge docs my-skill                # 生成文档
```

**CLI 架构**：
```
src/agent_forge/cli/
├── __init__.py          # CLI 入口
├── main.py              # Typer 应用
├── commands/
│   ├── create.py        # forge create
│   ├── test.py          # forge test
│   ├── publish.py       # forge publish
│   └── serve.py         # forge serve
└── templates/
    ├── skill-template/  # Skill 模板
    └── mcp-server-template/  # MCP Server 模板
```

### 3.2 工具注册表 (ToolRegistry)

```python
class ToolRegistry:
    """工具注册与发现管理器"""
    
    def register(self, tool: ToolBase) -> str:
        """注册工具，返回 tool_id"""
        
    def discover(self) -> Dict[str, ToolMeta]:
        """能力发现，返回所有活跃工具"""
        
    def call(self, tool_id: str, params: Dict) -> Dict:
        """调用工具"""
        
    def list(self) -> List[Dict]:
        """列出所有工具（MCP tools/list 格式）"""
```

### 3.3 MCP 服务器 (FastMCP 兼容层)

```python
from agent_forge import FastMCP

app = FastMCP("agent-forge")

@app.tool
def classify_text(text: str, categories: list = None) -> dict:
    """对文本进行多标签分类"""
    return {"text": text, "categories": categories or ["general"]}

# 启动
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

### 3.4 Context 优化模块

```python
class ContextOptimizer:
    """工具预筛 + Context 压缩"""
    
    def prefilter_tools(self, query: str, all_tools: List) -> List:
        """根据查询预筛相关工具"""
        
    def compress_context(self, context: str, max_tokens: int) -> str:
        """压缩上下文，减少 token 消耗"""
```

---

## 四、依赖管理方案

### 4.1 核心依赖 (requirements.txt)

```txt
# Agent-Forge 核心依赖
# 版本约束基于 MCP 2026-07-28 协议兼容性

# 核心依赖
typer>=0.9.0              # CLI 框架，自动生成帮助文档
rich>=13.0.0              # 终端富文本显示
pyyaml>=6.0               # 配置文件解析（.mcp.json）
jsonschema>=4.17.0        # 工具输入 Schema 验证

# FastMCP 兼容层（可选，但推荐）
fastmcp>=0.5.0            # FastMCP 装饰器语法支持
httpx>=0.27.0             # 异步 HTTP 客户端

# 注册表后端（可选）
sqlalchemy>=2.0.0         # ORM
psycopg2-binary>=2.9.0    # PostgreSQL 驱动
fastapi>=0.109.0          # REST API 框架

# 收款网关（集成 jianzhu-saas）
# billing.py 通过 symlink 引用
```

### 4.2 开发依赖

```txt
# 开发工具
pytest>=7.0
pytest-cov>=4.0
pytest-asyncio>=0.23.0    # 异步测试
black>=23.0
ruff>=0.1.0
mypy>=1.8.0               # 类型检查
```

### 4.3 pyproject.toml 配置

```toml
[project]
name = "agent-forge"
version = "0.2.0"
description = "中文 AI Agent 工具链标准框架"
requires-python = ">=3.10"
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "pyyaml>=6.0",
    "jsonschema>=4.17.0",
]

[project.optional-dependencies]
fastmcp = ["fastmcp>=0.5.0", "httpx>=0.27.0"]
database = ["sqlalchemy>=2.0.0", "psycopg2-binary>=2.9.0", "fastapi>=0.109.0"]
dev = ["pytest>=7.0", "pytest-cov>=4.0", "black>=23.0", "ruff>=0.1.0"]

[project.scripts]
forge = "agent_forge.cli.main:app"
agent-forge = "agent_forge.server:run_server"
```

---

## 五、演进路线

| 阶段 | 时间 | 目标 | 关键指标 |
|------|------|------|---------|
| **v0.1** | 2026-10 | 核心框架 + 基础工具 | 3 个内置工具，CLI 可用 |
| **v0.2** | 2026-11 | FastMCP 兼容层 + 中文模板 | 100 GitHub Stars |
| **v0.5** | 2026-12 | 注册表上线 + Pro 订阅 | 10 付费用户，¥1K MRR |
| **v1.0** | 2027-Q1 | 企业版 + 安全沙箱 | 50 付费用户，¥5K MRR |

---

## 六、与 jianzhu-saas 集成

```bash
# symlink 方式（推荐）
ln -s ../jianzhu-saas/billing.py src/agent_forge/gateway/billing.py
ln -s ../jianzhu-saas/store.py src/agent_forge/gateway/store.py
```

**配置项**：
```bash
export JZ_SAAS_BILLING_GATEWAY=afdian
export JZ_SAAS_AFDIAN_USER=0c59dda8a1bb11f19b9552540025c377
export JZ_SAAS_AFDIAN_TOKEN=mvBuAfHU3JnVbX8wq45KTWMRh6rgtkcP
```

---

**文档维护：** 编程专家_661  
**更新日志：** 见 CHANGELOG.md
