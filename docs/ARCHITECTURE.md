# agent-forge 模块结构

## 目录
```
agent-forge/
├── src/agent_forge/
│   ├── __init__.py      # 包入口
│   ├── registry.py      # 工具/Agent 注册表
│   └── server.py        # MCP Server（暴露 tools/call 等）
├── billing.py           # 收款层：NoopGateway + AfdianGateway + PAYWALL_RULES + check_access
└── docs/               # 本文档组
```

## 数据流
1. 客户端 → MCP 协议 → `server.py` 接收 `tools/call`
2. `server.py` 调 `registry.py` 路由到对应工具实现
3. 每次调用前走 `billing.check_access(plan, action)` 门控
4. 未付费 → 402 + upgrade_url（爱发电）；付费/Pro → 放行

## 门控模型
- `PAYWALL_RULES`: free=3 次/天, pro=不限, enterprise=不限
- 计数器文件存储（见 billing.py 内实现）
