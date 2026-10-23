#!/usr/bin/env bash
# agent-forge 冒烟：import + billing.check_access + PASS/FAIL
set -euo pipefail
cd "$(dirname "$0")"
PASS=0; FAIL=0
python3 -c "import sys; sys.path.insert(0,'src'); import agent_forge; print('import agent_forge OK')" && PASS=$((PASS+1)) || { echo "FAIL: import"; FAIL=$((FAIL+1)); }
python3 -c "import billing; r=billing.check_access('free','tool_call'); assert r['allowed'] is True; print('billing.check_access OK', r)" && PASS=$((PASS+1)) || { echo "FAIL: billing"; FAIL=$((FAIL+1)); }
echo "smoke_test: PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ] && echo "=== SMOKE PASS ===" && exit 0 || { echo "=== SMOKE FAIL ==="; exit 1; }
