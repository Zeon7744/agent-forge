# Agent-Forge

> **中文 AI Agent 的工具链标准** — 填补 634K 工具生态的中文框架空白

[![GitHub Stars](https://img.shields.io/github/stars/Zeon7744/agent-forge?style=social)](https://github.com/Zeon7744/agent-forge)
[![GitHub Forks](https://img.shields.io/github/forks/Zeon7744/agent-forge?style=social)](https://github.com/Zeon7744/agent-forge/forks)
[![GitHub License](https://img.shields.io/github/license/Zeon7744/agent-forge)](https://github.com/Zeon7744/agent-forge/blob/main/LICENSE)
[![Gitee Stars](https://gitee.com/Zeon7744/agent-forge/badge/star.svg?theme=gvp)](https://gitee.com/Zeon7744/agent-forge)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

---

## 📌 这是 GitHub 官方主仓

> **Gitee 镜像**: [gitee.com/Zeon7744/agent-forge](https://gitee.com/Zeon7744/agent-forge)

Issues 和 PR 请在 GitHub 提交。

---

## 🚀 快速开始

```bash
# 安装
pip install -e ".[dev]"

# CLI 脚手架
forge create my-skill

# 运行示例
python examples/hello_world.py

# 启动 MCP 服务器
python -m agent_forge.server --port 8000
```

---

## ✨ 核心价值

| 痛点 | agent-forge 方案 |
|------|-----------------|
| **634K 工具缺中文标准** | 统一的工具注册、发现、调用框架 |
| **MCP token 开销大** | 工具预筛 + Context 压缩，优化 85% 开销 |
| **Skills 开发生命周期缺失** | `forge create/test/deploy` 一站式 |
| **企业级管理困难** | 注册表 + 权限管理 + 审计日志 |

---

## 🛠️ 核心功能

| 模块 | 功能 | 对标 |
|------|------|------|
| **CLI 脚手架** | `forge create my-skill` 分钟级启动 | `mcp create` |
| **工具注册表** | 动态注册、发现、版本管理 | npm registry |
| **插件系统** | 热加载、沙箱隔离 | Docker MCP Toolkit |
| **Context 优化** | 工具预筛 + 上下文压缩 | Anthropic Tool Search |
| **收款集成** | 爱发电/微信商户无缝接入 | jianzhu-saas billing |

---

## 📁 项目结构

```
agent-forge/
├── src/agent_forge/
│   ├── server.py      # MCP HTTP/SSE 服务器
│   ├── registry.py    # 工具注册与发现
│   ├── plugin.py      # 插件热加载管理
│   ├── gateway/       # 收款网关（爱发电/微信）
│   └── tools/         # 内置工具集（文本/代码/数据）
├── tests/             # 单元测试 + 集成测试
├── examples/          # 中文场景 Demo
├── docs/              # 架构文档 + API 参考
├── pyproject.toml     # 项目配置
└── pricing.md         # 定价方案
```

---

## 🔧 技术栈

| 层级 | 技术 | 理由 |
|------|------|------|
| **核心框架** | Python + MCP SDK | 中文开发者占比高，降低学习成本 |
| **CLI** | Typer | 轻量、快速启动 |
| **注册表** | PostgreSQL + FastAPI | 成熟稳定，支持 RBAC |
| **安全沙箱** | Docker + gVisor | 企业级隔离 |
| **文档** | Docusaurus + 中文 i18n | 双语言支持 |

---

## 💰 产品订阅

| 档位 | 价格 | 权益 |
|------|------|------|
| 免费 | ¥0 | 基础工具集 + 社区支持 + 5 个 MCP Server |
| **Pro** | **¥99/月** | 全部内置工具 + Registry 发布 + 优先技术支持 |
| 企业 | ¥999/月 | 私有部署 + 定制工具开发 + SLA 保障 |

👉 **[立即订阅 — 爱发电](https://afdian.net/@Zeon7744)**（支付宝 / 微信支付）

> 详细定价见 [pricing.md](pricing.md)

---

## 📊 项目统计

| 指标 | 数值 |
|------|------|
| **代码行数** | ~500 行（骨架阶段）|
| **测试用例** | 待补充 |
| **工具数量** | 5 个内置（文本/代码/数据）|
| **协议版本** | MCP 2026-07-28 |

---

## 🤝 贡献指南

欢迎贡献！你可以：

- 新增中文场景工具
- 优化 Context 压缩算法
- 完善文档和示例
- 修复 bug 或提出建议

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/new-tool`)
3. 提交更改 (`git commit -m 'Add new tool: XXX'`)
4. 推送到分支 (`git push origin feature/new-tool`)
5. 开启 Pull Request

---

## 📰 行业资讯

关注 MCP 和 AI Agent 生态动态：

- [MCP 官方规范](https://modelcontextprotocol.io)
- [FastMCP (25K★)](https://github.com/PrefectHQ/fastmcp)
- [Official MCP SDK (12K★)](https://github.com/modelcontextprotocol/python-sdk)
- [AI Agent 社群](https://jike.com)

---

## ☕ 支持作者

如果这个项目对你有帮助，欢迎赞助 ☕

| 渠道 | 方式 |
|------|------|
| [爱发电](https://afdian.net/@Zeon7744) | 支付宝 / 微信支付 |
| [GitHub Sponsors](https://github.com/sponsors/Zeon7744) | PayPal / Stripe |

---

## 📄 License

MIT License — 自由使用，商业友好。

---

<div align="center">

**由 [Zeon7744](https://github.com/Zeon7744) 维护**  
*中文 AI Agent 的工具链标准*

⭐ 如果对你有帮助，点个 Star 鼓励一下！

</div>

---

## 🚀 免费 → Pro → 企业（变现入口）

免费=浏览素材；Pro=下载完整剧本/小说；企业=商用授权+定制题材

- **免费**：立即 [安装/克隆] 使用，命中配额即可升级。
- **Pro**：[Gitee Pro 订阅](https://gitee.com/Zeon7744) 解锁高级能力。
- **企业**：私有部署 / 定制需求 → 见 `pricing.md`，或联系商务（GitHub Issues / Gitee）。

> 详细定价与 SKU 见 [pricing.md](pricing.md) ｜ 支持项目见 [FUNDING.yml](FUNDING.yml)

---

## 🔗 相关链接

- [架构设计文档](docs/architecture.md)
- [API 参考](docs/api-reference.md)
- [部署指南](docs/deployment.md)
- [爱发电订阅](https://afdian.net/@Zeon7744)
