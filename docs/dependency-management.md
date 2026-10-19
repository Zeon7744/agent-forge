# Agent-Forge 依赖管理方案

**版本：** v0.2.0  
**日期：** 2026-10-19

---

## 一、依赖分层策略

### 1.1 核心依赖（必须安装）

```txt
# Agent-Forge 核心运行时依赖
typer>=0.9.0              # CLI 框架，自动生成帮助文档和参数补全
rich>=13.0.0              # 终端富文本显示（面板、表格、进度条）
pyyaml>=6.0               # 配置文件解析（.mcp.json, forge.yaml）
jsonschema>=4.17.0        # 工具输入 Schema 验证
```

**理由**：
- **typer**：比 click 更现代，支持类型提示自动验证，自动生成 `--help`
- **rich**：提升 CLI 用户体验，支持彩色输出、面板、表格
- **pyyaml**：配置文件标准格式，支持中文注释
- **jsonschema**：确保工具调用参数符合规范

### 1.2 可选依赖（按需安装）

```txt
# FastMCP 兼容层（推荐）
fastmcp>=0.5.0            # FastMCP 装饰器语法，降低开发门槛
httpx>=0.27.0             # 异步 HTTP 客户端，支持 Streamable HTTP

# 注册表后端（企业版）
sqlalchemy>=2.0.0         # ORM，支持 PostgreSQL/MySQL/SQLite
psycopg2-binary>=2.9.0    # PostgreSQL 驱动
fastapi>=0.109.0          # REST API 框架
uvicorn>=0.27.0           # ASGI 服务器

# AI 能力（可选）
openai>=1.0.0             # OpenAI API 接入
anthropic>=0.18.0         # Claude API 接入

# 安全沙箱（企业版）
docker>=7.0.0             # Docker SDK for Python
gVisor>=0.4.0             # 系统调用过滤（需要内核支持）
```

### 1.3 开发依赖

```txt
# 测试框架
pytest>=7.0
pytest-cov>=4.0           # 覆盖率报告
pytest-asyncio>=0.23.0    # 异步测试支持
pytest-mock>=3.12.0       # Mock 支持

# 代码质量
black>=23.0               # 代码格式化
ruff>=0.1.0               # Linter（比 flake8 快 10 倍）
mypy>=1.8.0               # 静态类型检查
pre-commit                # Git hooks 管理

# 文档
sphinx>=7.0               # 文档生成
myst-parser               # Markdown 支持
```

---

## 二、pyproject.toml 配置

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "agent-forge"
version = "0.2.0"
description = "中文 AI Agent 工具链标准框架"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
authors = [
    {name = "Zeon7744"}
]
keywords = ["mcp", "agent", "tool", "skill", "chinese"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "pyyaml>=6.0",
    "jsonschema>=4.17.0",
]

[project.optional-dependencies]
# FastMCP 兼容层
fastmcp = [
    "fastmcp>=0.5.0",
    "httpx>=0.27.0",
]

# 注册表后端
database = [
    "sqlalchemy>=2.0.0",
    "psycopg2-binary>=2.9.0",
    "fastapi>=0.109.0",
    "uvicorn>=0.27.0",
]

# AI 能力
ai = [
    "openai>=1.0.0",
    "anthropic>=0.18.0",
]

# 安全沙箱
sandbox = [
    "docker>=7.0.0",
]

# 开发依赖
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.23.0",
    "pytest-mock>=3.12.0",
    "black>=23.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
    "pre-commit>=3.0.0",
]

# 文档
docs = [
    "sphinx>=7.0",
    "myst-parser>=0.18.0",
]

# 全部依赖
all = [
    "agent-forge[fastmcp,database,ai,sandbox]",
    "agent-forge[dev,docs]",
]

[project.scripts]
forge = "agent_forge.cli.main:app"
agent-forge = "agent_forge.server:run_server"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

[tool.black]
line-length = 100
target-version = ["py310", "py311", "py312"]

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "W"]
target-version = "py310"

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

---

## 三、requirements.txt 生成策略

### 3.1 核心 requirements.txt

```txt
# Agent-Forge 核心依赖
# 版本约束基于 MCP 2026-07-28 协议兼容性

# 核心依赖
typer>=0.9.0              # CLI 框架，自动生成帮助文档
rich>=13.0.0              # 终端富文本显示
pyyaml>=6.0               # 配置文件解析
jsonschema>=4.17.0        # Schema 验证

# 可选依赖（按需安装）
# fastmcp>=0.5.0          # FastMCP 兼容层
# httpx>=0.27.0           # 异步 HTTP 客户端
# sqlalchemy>=2.0.0       # ORM
# psycopg2-binary>=2.9.0  # PostgreSQL 驱动
# openai>=1.0.0           # AI 能力
```

### 3.2 requirements-dev.txt

```txt
# 开发依赖
-r requirements.txt

# 测试框架
pytest>=7.0
pytest-cov>=4.0
pytest-asyncio>=0.23.0
pytest-mock>=3.12.0

# 代码质量
black>=23.0
ruff>=0.1.0
mypy>=1.8.0
pre-commit>=3.0.0
```

---

## 四、依赖隔离策略

### 4.1 虚拟环境建议

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 安装核心依赖
pip install -e ".[dev]"

# 安装可选依赖
pip install -e ".[fastmcp,database]"
```

### 4.2 容器化部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装核心依赖
COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir .[prod]

# 安装开发依赖（可选）
# RUN pip install --no-cache-dir .[dev]

EXPOSE 8000

CMD ["python", "-m", "agent_forge.server", "--port", "8000"]
```

---

## 五、依赖更新策略

### 5.1 版本锁定

```bash
# 锁定依赖版本
pip freeze > requirements.lock.txt

# 检查过时依赖
pip list --outdated

# 安全更新
pip install --upgrade typer rich pyyaml jsonschema
```

### 5.2 CI/CD 依赖检查

```yaml
# .github/workflows/dependency-check.yml
name: Dependency Check
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: pip-audit --requirement requirements.txt
      - run: safety check --requirement requirements.txt
```

---

## 六、与 jianzhu-saas 的依赖共享

### 6.1 symlink 方式（推荐）

```bash
# 共享 billing.py 和 store.py
ln -s ../jianzhu-saas/billing.py src/agent_forge/gateway/billing.py
ln -s ../jianzhu-saas/store.py src/agent_forge/gateway/store.py
```

### 6.2 独立依赖方式

```txt
# agent-forge 独立依赖
# billing.py 和 store.py 通过环境变量配置，不依赖 jianzhu-saas
JZ_SAAS_BILLING_GATEWAY=afdian
JZ_SAAS_AFDIAN_USER=0c59dda8a1bb11f19b9552540025c377
JZ_SAAS_AFDIAN_TOKEN=mvBuAfHU3JnVbX8wq45KTWMRh6rgtkcP
```

---

**文档维护：** 编程专家_661
