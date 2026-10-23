# agent-forge 快速上手（5 分钟跑通）

## 1. 克隆与依赖
```bash
git clone https://github.com/Zeon7744/agent-forge.git
cd agent-forge
pip install -r requirements.txt   # 无 requirements 则: pip install fastmcp
```

## 2. 注册 MCP Server 到 Coze
按 `08_SOP与模板/` 或 README 指引，将 `src/agent_forge/server.py` 暴露的 MCP 端点注册到扣子/Coze 工作区。

## 3. 发起一次调用
```bash
python -c "from agent_forge.server import *; help()"   # 验证模块可导入
```

## 4. 收款与门控
- 免费版：3 次/天调用；Pro ¥99/月 不限次；企业 ¥999/月 定制
- 爱发电入口：https://afdian.com/@Zeon7744
- 本地冒烟：`bash smoke_test.sh`
