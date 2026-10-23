# agent-forge 收款与门控（爱发电 afdian）

## 定价档位（与 billing.py PAYWALL_RULES 对齐）
| 档位 | 价格 | 限制 | 说明 |
|---|---|---|---|
| Free | ¥0 | 3 次/天 | 基础体验 |
| Pro | ¥99/月 | 不限次 | 完整工具集 |
| 企业 | ¥999/月 | 不限次+SLA | 定制因子/API |

## 收款流程（先体验后付费）
1. 用户免费调用（每天 3 次），超限返回 402 + 升级链接
2. 升级链接指向 爱发电 https://afdian.com/@Zeon7744
3. 付款后订单回调 → `billing.AfdianGateway.query_callback` 核验 → 本地提权
4. 网关默认 `noop`（无 key 时安全降级），生产配 `JZ_AFDIAN_USER` / `JZ_AFDIAN_TOKEN`

## 环境变量
- `JZ_AFDIAN_USER` 爱发电 user_id
- `JZ_AFDIAN_TOKEN` 爱发电 token
- `BILLING_GATEWAY` `noop`（默认）/ `afdian`
