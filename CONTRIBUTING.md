# 贡献指南

感谢你对 agent-forge 的贡献兴趣！本文档帮助你快速上手。

## 🌈 贡献方式

| 方式 | 难度 | 说明 |
|------|------|------|
| 🐛 报告 Bug | ⭐ | 发现并报告问题 |
| 💡 功能建议 | ⭐⭐ | 提出新功能想法 |
| 📝 改进文档 | ⭐ | 修正或补充文档 |
| 💻 提交 PR | ⭐⭐⭐ | 贡献代码 |
| 🎬 分享 Demo | ⭐⭐ | 展示使用案例 |

## 🚀 首次贡献流程

### Step 1: Fork & Clone

```bash
git clone https://github.com/YOUR-USERNAME/agent-forge.git
cd agent-forge
```

### Step 2: 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-fix-name
```

### Step 3: 开发 & 测试

```bash
pip install -e ".[dev]"
pytest tests/
pytest tests/ -v
```

### Step 4: 提交 PR

1. 推送分支：`git push origin feature/your-feature-name`
2. 在 GitHub 创建 Pull Request
3. 填写 PR 描述
4. 等待 Review

## 📋 PR 规范

### 提交信息格式

```
<type>(<scope>): <subject>

body

footer
```

**Type 类型：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

### PR 描述模板

```markdown
## 类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 其他

## 变更内容
简述本次 PR 的改动

## 测试
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 已手动测试

## 相关 Issue
Closes #xxx
```

## 🎯 新手友好任务

| 任务 | 标签 | 难度 |
|------|------|------|
| 修正 README 拼写错误 | `documentation` | ⭐ |
| 添加中文 Demo 示例 | `good first issue` | ⭐⭐ |
| 完善文档翻译 | `documentation` | ⭐ |
| 修复简单 Bug | `beginner-friendly` | ⭐⭐ |

## 📚 代码规范

### Python 风格

- 遵循 [PEP 8](https://peps.python.org/pep-0008/)
- 使用 [Black](https://black.readthedocs.io/) 格式化
- 类型注解：[mypy](https://mypy.readthedocs.io/) 检查

### Commit 规范

- 使用 [Conventional Commits](https://www.conventionalcommits.org/)
- 单次提交只做一个变更
- 描述清晰、简洁

## 🙋 需要帮助？

在 [Discussions](https://github.com/Zeon7744/agent-forge/discussions) 发帖，我们会及时回复。

**感谢你的贡献！** 🎉
