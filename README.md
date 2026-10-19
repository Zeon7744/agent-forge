# Agent Forge —— 中文 AI Agent 工具链框架

> 🇨🇳 面向中文场景的 MCP 工具链标准框架，让 Agent 真正用起来中国生态的工具。

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Protocol-green.svg)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)

## 为什么需要 Agent Forge？

GitHub 上已有 **634K+ 工具生态**，每天新增 **1,719 个工具**。但——

- ❌ 中文垂直场景没有标准化的 Agent 工具链框架
- ❌ 微信/支付宝/飞书/钉钉/企业微信等中国生态工具缺少 MCP 适配
- ❌ 国内开发者搭建 Agent 时，重复造轮子、工具对接碎片化

**Agent Forge 解决这个问题。**

## 核心价值

### 🔧 开箱即用的中文工具集
内置中国生态高频工具的 MCP Server 实现：
- 飞书 / 钉钉 / 企业微信消息推送
- 微信/支付宝支付网关对接
- 中文 NLP 工具（分词、NER、情感分析）
- 国内云服务适配（阿里云/腾讯云/华为云）

### 📐 标准化的工具开发范式
- 基于 MCP Protocol 的标准工具定义
- 统一的输入/输出 Schema 规范
- 内置工具测试框架 + Mock Server
- 一键打包发布到 Agent Forge Registry

### 🚀 零门槛接入主流 Agent 框架
- 原生支持 Claude MCP SDK
- 兼容 LangChain / AutoGen / CrewAI
- 提供 Python SDK + CLI 双入口

## 快速开始

### 安装

```bash
# 从源码安装（开发版）
git clone https://github.com/yourusername/agent-forge.git
cd agent-forge
pip install -e .

# 或 PyPI 安装（稳定版）
pip install agent-forge
```

### 使用内置工具

```python
from agent_forge import AgentToolkit

# 初始化工具包
toolkit = AgentToolkit()

# 加载飞书消息工具
feishu = toolkit.load("feishu.message")
feishu.send(webhook_url="https://open.feishu.cn/...", content="Hello Agent!")

# 加载中文 NLP 工具
nlp = toolkit.load("nlp.chinese")
result = nlp.segment("Agent Forge 是一个中文工具链框架")
print(result)  # ['Agent', 'Forge', '是', '一个', '中文', '工具链', '框架']
```

### 开发自定义工具

```python
from agent_forge import MCPTool, tool

@tool(
    name="weather_cn",
    description="查询中国城市天气",
    params={"city": str},
)
async def weather_cn(city: str) -> dict:
    """查询中国城市实时天气"""
    # 你的实现
    return {"city": city, "temp": 25, "condition": "晴"}

# 注册到工具包
toolkit.register(weather_cn)
```

### 启动 MCP Server

```bash
# 启动内置 MCP Server
agent-forge serve --port 8080

# 或指定工具集
agent-forge serve --tools feishu,nlp,payment --port 8080
```

## 项目结构

```
agent-forge/
├── src/
│   ├── agent_forge/
│   │   ├── __init__.py          # 包入口
│   │   ├── core/                # 核心框架
│   │   │   ├── toolkit.py       # 工具包管理
│   │   │   ├── registry.py      # 工具注册表
│   │   │   └── schema.py        # Schema 定义
│   │   ├── tools/               # 内置工具集
│   │   │   ├── feishu/          # 飞书工具
│   │   │   ├── dingtalk/        # 钉钉工具
│   │   │   ├── nlp/             # 中文 NLP 工具
│   │   │   └── payment/         # 支付工具
│   │   ├── server/              # MCP Server 实现
│   │   ├── cli/                 # CLI 入口
│   │   └── sdk/                 # Python SDK
│   └── tests/                   # 测试用例
├── examples/                    # 示例代码
├── docs/                        # 文档
├── pricing.md                   # 定价方案
├── CHANGELOG.md                 # 版本记录
├── pyproject.toml               # 项目配置
└── README.md                    # 本文件
```

## 技术栈

| 组件 | 选型 | 说明 |
|------|------|------|
| 语言 | Python 3.10+ | 主开发语言 |
| 协议 | MCP (Model Context Protocol) | 工具标准化协议 |
| SDK | mcp-python-sdk | 官方 Python SDK |
| 异步 | asyncio + aiohttp | 高并发工具调用 |
| CLI | click / typer | 命令行工具 |
| 测试 | pytest + pytest-asyncio | 测试框架 |

## 路线图

- [ ] **v0.1.0** — 核心框架 + MCP Server 基础实现
- [ ] **v0.2.0** — 飞书/钉钉工具集 + 中文 NLP 工具
- [ ] **v0.3.0** — 支付网关对接 + Registry 发布
- [ ] **v1.0.0** — 稳定版 + 文档站上线

---

## 🚀 免费 → Pro → 企业（变现入口）

免费=基础工具集 + 社区支持；Pro=¥99/月（高级工具 + 优先支持）；企业=¥999/月（私有部署 + 定制工具开发）

- **免费**：立即 [克隆/安装] 使用，基础工具集开箱即用。
- **Pro（¥99/月）**：[爱发电订阅](https://afdian.net/@Zeon7744) 解锁高级工具集 + 优先技术支持。
- **企业（¥999/月）**：私有部署 / 定制工具开发 → [联系商务](https://afdian.net/@Zeon7744)。

> 详细定价见 [pricing.md](pricing.md)

---

## 💰 订阅支持

| 档位 | 价格 | 核心权益 |
|------|------|----------|
| 免费 | ¥0 | 基础工具集 + 社区支持 |
| Pro | ¥99/月 | 全部工具 + 优先支持 + Registry 发布 |
| 企业 | ¥999/月 | 私有部署 + 定制工具 + SLA |

👉 **[立即订阅 — 爱发电](https://afdian.net/@Zeon7744)**（支付宝 / 微信支付）

> 详细定价见 [pricing.md](pricing.md)

---

## License

MIT License. 详见 [LICENSE](LICENSE).
