# Agent-Forge

## 💰 价值主张 & 定价
> **能卖什么**：中文 AI Agent 工具链标准 — 5 分钟开发一个中文 MCP 工具，20+ 内置中文 NLP 工具 + Registry 一键发布。
>
> **定价**：免费（基础 5 个 MCP Server）/ **Pro ¥99/月**（全部工具 + 发布 + 高级 NLP）/ **企业 ¥999/月**（私有部署 + SLA 99.9%）。付费渠道：[爱发电 @Zeon7744](https://afdian.net/@Zeon7744)


> **中文 AI Agent 的工具链标准** — 填补 634K 工具生态的中文框架空白

mcp-name: io.github.Zeon7744/agent-forge

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

### 验证安装

```bash
$ forge --version
Agent-Forge v0.2.0

$ forge test ./examples/hello_world/
✅ All tests passed (5/5)
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

### CLI 脚手架

```bash
# 创建新 Skill
forge create my-tool --template text

# 测试 Skill
forge test ./my-tool/

# 发布到注册表
forge publish ./my-tool/

# 启动 MCP 服务器
forge serve --port 8000
```

### 内置工具

| 模块 | 功能 | 示例 |
|------|------|------|
| **text** | 文本分类、格式化 | `python -m agent_forge.tools.text classify "文本"` |
| **code** | 代码分析、格式化 | `python -m agent_forge.tools.code analyze ./main.py` |
| **data** | 数据统计、可视化 | `python -m agent_forge.tools.data stats ./data.csv` |

### Pro 功能模块

| 模块 | 功能 | 说明 |
|------|------|------|
| **marketplace** | Skills 注册表与分发市场 | 发布/下载/评分 |
| **analytics** | 工具使用统计与优化建议 | 调用计数、耗时分析 |
| **rate_limiter** | Token 配额与调用频率控制 | 令牌桶算法 |

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
| **代码行数** | ~33 个 Python 文件 |
| **测试用例** | 38/38 通过 |
| **工具数量** | 15+ 内置工具 |
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

👉 **[查看完整贡献指南](CONTRIBUTING.md)**

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
