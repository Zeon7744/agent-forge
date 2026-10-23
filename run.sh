#!/usr/bin/env bash
# agent-forge 一键启动 MCP Server
set -euo pipefail
cd "$(dirname "$0")"
python3 -m agent_forge.server
