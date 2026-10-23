"""
agent-forge 收款层 — 爱发电 afdian 网关 + 免费版限次门控

定价锚点（与 README 对齐）：
  免费: ¥0 — 基础 5 个 MCP Server，3 次/天
  Pro:  ¥99/月 — 全部工具 + Registry 发布 + 高级 NLP
  企业:  ¥999/月 — 私有部署 + SLA
"""
import os
import time
import uuid
import json
import urllib.request

PAYWALL_RULES = {
    "free":       {"daily_limit": 3, "label": "免费版"},
    "pro":        {"daily_limit": -1, "label": "Pro ¥99/月"},
    "enterprise": {"daily_limit": -1, "label": "企业 ¥999/月"},
}

_STATE = {"date": "", "count": 0}


def _today():
    return time.strftime("%Y-%m-%d")


def check_access(plan: str = "free", action: str = "tool_call") -> dict:
    """门控函数：免费版 3 次/天，Pro/企业不限次。"""
    rules = PAYWALL_RULES.get(plan, PAYWALL_RULES["free"])
    limit = rules["daily_limit"]

    if limit == -1:
        return {"allowed": True, "remaining": -1, "reason": ""}

    if _STATE["date"] != _today():
        _STATE["date"] = _today()
        _STATE["count"] = 0

    if _STATE["count"] >= limit:
        return {
            "allowed": False,
            "remaining": 0,
            "reason": f"免费版每日 {limit} 次已用完，请升级 Pro 解锁全部工具",
            "upgrade_url": "https://afdian.com/@Zeon7744",
            "http_status": 402,
        }

    _STATE["count"] += 1
    return {"allowed": True, "remaining": limit - _STATE["count"], "reason": ""}


def get_pricing() -> list[dict]:
    return [
        {"plan": "free", "price": 0, "price_label": "¥0",
         "features": ["基础 5 个 MCP Server", "3 次/天", "社区支持"]},
        {"plan": "pro", "price": 99, "price_label": "¥99/月",
         "features": ["全部内置工具", "Registry 发布", "高级 NLP", "优先技术支持"]},
        {"plan": "enterprise", "price": 999, "price_label": "¥999/月",
         "features": ["私有部署", "定制工具开发", "SLA 99.9%", "多 Agent 编排"]},
    ]


# ── 网关 ──
class NoopGateway:
    name = "noop"
    def create_order(self, tenant_id, amount_cents, product, plan, order_meta=None):
        return {"order_id": "noop_" + str(uuid.uuid4())[:12], "status": "created", "gateway": "noop"}
    def query_callback(self, order_id):
        return {"order_id": order_id, "status": "unpaid", "paid": False}
    def refund(self, order_id, amount_cents, reason=""):
        return {"order_id": order_id, "ok": True}


class AfdianGateway:
    """爱发电网关"""
    name = "afdian"
    DEFAULT_BASE = "https://afdian.com/api"

    def __init__(self):
        self.user_id = os.environ.get("JZ_AFDIAN_USER", "")
        self.token = os.environ.get("JZ_AFDIAN_TOKEN", "")
        self.base = os.environ.get("JZ_AFDIAN_BASE", self.DEFAULT_BASE)

    def _post(self, path, payload):
        body = dict(payload)
        if self.token:
            body["token"] = self.token
        req = urllib.request.Request(
            f"{self.base}{path}",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def create_order(self, tenant_id, amount_cents, product, plan, order_meta=None):
        if not self.user_id or not self.token:
            return {"order_id": "pending", "status": "created_pending_key",
                    "needs_secret": ["JZ_AFDIAN_USER", "JZ_AFDIAN_TOKEN"]}
        price = round(amount_cents / 100.0, 2)
        out_trade_no = "af_" + str(uuid.uuid4())[:16]
        payload = {"user_id": self.user_id, "price": str(price),
                   "name": f"agent-forge({plan})"[:42], "out_trade_no": out_trade_no}
        try:
            result = self._post("/payment/create", payload)
            if result.get("code") != 0:
                return {"order_id": out_trade_no, "status": "gateway_rejected", "code": result.get("code")}
            data = result.get("data", {})
            return {"order_id": out_trade_no, "status": "created",
                    "pay_url": data.get("url", ""), "gateway": "afdian"}
        except Exception as e:
            return {"order_id": out_trade_no, "status": "gateway_error", "error": str(e)}

    def query_callback(self, order_id):
        if not self.user_id or not self.token:
            return {"order_id": order_id, "status": "pending_key", "paid": False}
        payload = {"user_id": self.user_id, "out_trade_no": order_id}
        try:
            result = self._post("/payment/query", payload)
            data = result.get("data", {})
            return {"order_id": order_id, "status": data.get("status", "unknown"),
                    "paid": data.get("status") in ("paid", "success")}
        except Exception as e:
            return {"order_id": order_id, "status": "query_failed", "paid": False, "error": str(e)}

    def refund(self, order_id, amount_cents, reason=""):
        if not self.user_id or not self.token:
            return {"order_id": order_id, "ok": False, "note": "凭据未配"}
        price = round(amount_cents / 100.0, 2)
        payload = {"user_id": self.user_id, "out_trade_no": order_id, "price": str(price)}
        try:
            result = self._post("/payment/refund", payload)
            return {"order_id": order_id, "ok": result.get("code") == 0, "refunded_cents": amount_cents}
        except Exception as e:
            return {"order_id": order_id, "ok": False, "error": str(e)}


_REGISTRY = {"noop": NoopGateway, "afdian": AfdianGateway}

def get_gateway(name=None):
    name = name or os.environ.get("BILLING_GATEWAY", "noop")
    return _REGISTRY.get(name, NoopGateway)()

def create_order_for_plan(tenant_id, plan, product="agent-forge"):
    g = get_gateway()
    prices = {p["plan"]: p["price"] for p in get_pricing()}
    amount = prices.get(plan, 0) * 100
    return g.create_order(tenant_id, amount, product, plan)
