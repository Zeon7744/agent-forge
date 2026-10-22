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


---

## ⚖️ 商用与合规

### 开源范围
- 代码以 MIT License 开放，可自由使用、修改与商用。
- 以下部分不属于开源范围：Pro/企业档位的托管服务（私有部署、SLA、定制工具开发）。

### 付费功能边界
- 免费（¥0）：基础工具集 + 社区支持 + 5 个 MCP Server
- Pro（¥99/月）：全部内置工具 + Registry 发布 + 优先技术支持
- 企业（¥999/月）：私有部署 + 定制工具开发 + SLA 保障

### 合规免责
- 本工具涉及文件读写、终端命令、外部 API 调用等**高风险操作**，使用者应在受控环境执行并自行复核结果。
- 使用本工具产生的数据丢失、越权操作或任何业务后果由使用者自行承担。
- 调用外部 MCP/LLM API 的费用与合规责任由使用者按对应服务商协议自行承担。


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

## 💛 支持 & 发布（爱发电双通道）

本仓通过**爱发电**完成「**创作者赞赏/订阅收款**」与「**作品/内容社区发布**」双通道运营，二者共存：

| 通道 | 用途 | 入口 |
|------|------|------|
| 💰 爱发电收款 | 赞赏、订阅、Pro 会员、赞助维护 | [爱发电 @Zeon7744](https://afdian.net/@Zeon7744) |
| 📣 爱发电社区发布 | 作品展示、内容连载、粉丝互动、发布分发 | [爱发电社区 @Zeon7744](https://afdian.com/user/0c59dda8a1bb11f19b9552540025c377) |

- **收款**：赞赏 / 订阅 Pro / 企业赞助，支付宝 + 微信支付，无需备案域名
- **社区发布**：把本仓产出（作品 / 剧本 / 工具演示 / 案例）在爱发电社区连载发布，沉淀粉丝、引流回仓
- 两通道独立共存，按需选用；收款不强制绑定社区发布

> 本仓内容仅供创作参考，发布前请完成人工合规审查与平台备案。

---

## 🎯 定价理念：先体验，后付费

**以人为本，让使用者深度体验价值后再做决定：**

- **免费额度拉满**：所有仓库的免费版本提供足够深度的体验额度，不人为设限——把核心能力先跑起来，让你真正用到
- **深度体验再付费**：付费版解锁的是更高频次、更完整功能、更高级资源（模板/工具/分成），不是限制基础体验
- **你的反馈驱动迭代**：每一条回馈都是产品优化的第一手依据，我们据此持续完善

## 💬 用户回馈（驱动迭代）

**使用中发现任何问题、想法、建议 → 直接回馈，驱动下一版：**

| 方式 | 入口 | 说明 |
|------|------|------|
| 社区评论 | [爱发电社区 @Zeon7744](https://afdian.com/user/0c59dda8a1bb11f19b9552540025c377) | 作品下评论/留言，直接驱动迭代 |
| Issue | 本仓 GitHub / Gitee / GitCode 的 Issues | Bug / 功能建议 / 定价反馈 |
| 赞赏反馈 | 爱发电赞赏留言 | 支持的同时留下使用心得 |

> 每一条回馈都是产品优化的第一手依据。不强制，但真诚欢迎。
