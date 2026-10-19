# -*- coding: utf-8 -*-
"""
合规模块 - AI内容标注与数字人使用合规检查

参考 ai-mcn-studio 的 AI 标注规则，适配 Agent-Forge 场景：
- 各平台 AI 标识要求校验（抖音 / B站 / 小红书 / YouTube）
- 数字人出镜披露检查
- 虚拟 UP 主商业化限制提示
- 自动生成合规页脚
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .base import ToolBase, ToolInputSchema


class Platform(str, Enum):
    DOUYIN = "douyin"
    BILIBILI = "bilibili"
    XIAOHONGSHU = "xiaohongshu"
    YOUTUBE = "youtube"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ComplianceIssue:
    """一条合规问题记录"""
    issue_id: str
    platform: Optional[Platform]
    rule: str
    description: str
    risk_level: RiskLevel
    suggestion: str
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "platform": self.platform.value if self.platform else "all",
            "rule": self.rule,
            "description": self.description,
            "risk_level": self.risk_level.value,
            "suggestion": self.suggestion,
        }


class ComplianceTool(ToolBase):
    """
    合规模块工具。

    支持操作：check_content / check_digital_human / generate_footer / list_rules
    """

    def __init__(self):
        super().__init__(
            tool_id="compliance",
            name="compliance",
            description=(
                "AI内容合规模块：检测AI生成内容、数字人出镜合规、"
                "各平台标注要求校验，生成合规页脚。"
            ),
            input_schema=ToolInputSchema(
                properties={
                    "action": {"type": "string", "enum": ["check_content", "check_digital_human", "generate_footer", "list_rules"], "description": "操作类型"},
                    "content": {"type": "string", "description": "待检测的内容文本"},
                    "platforms": {"type": "array", "items": {"type": "string"}, "description": "目标平台列表"},
                    "has_digital_human": {"type": "boolean", "description": "是否包含数字人出镜"},
                    "is_commercial": {"type": "boolean", "description": "是否用于商业目的"},
                },
                required=["action"],
            ),
        )
        self._rules: Dict[str, Dict[str, Any]] = self._load_rules()

    # ------------------------------------------------------------------
    # 规则库
    # ------------------------------------------------------------------
    def _load_rules(self) -> Dict[str, Dict[str, Any]]:
        """加载各平台 AI 标注规则"""
        return {
            "douyin": {
                "ai_label_required": True,
                "label_text": "本内容由AI生成",
                "placement": "视频角落",
                "risk_high_keywords": ["虚拟主播", "数字人", "AI合成", "虚拟形象"],
            },
            "bilibili": {
                "ai_label_required": True,
                "label_text": "AI生成内容",
                "placement": "简介区声明",
                "risk_high_keywords": ["AI配音", "数字人", "虚拟UP主"],
            },
            "xiaohongshu": {
                "ai_label_required": True,
                "label_text": "AI辅助创作",
                "placement": "正文或评论区",
                "risk_high_keywords": ["AI绘图", "数字人", "虚拟博主"],
            },
            "youtube": {
                "ai_label_required": True,
                "label_text": "Altered content",
                "placement": "上传时声明",
                "risk_high_keywords": ["synthetic media", "digital human"],
            },
        }

    # ------------------------------------------------------------------
    # 工具接口
    # ------------------------------------------------------------------
    def execute(self, params: Dict[str, Any]) -> Any:
        action = params.get("action", "check_content")
        handlers = {
            "check_content": self._check_content,
            "check_digital_human": self._check_digital_human,
            "generate_footer": self._generate_footer,
            "list_rules": self._list_rules,
        }
        handler = handlers.get(action)
        if not handler:
            return {"error": f"Unknown action: {action}"}
        return handler(params)

    def _check_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """检查内容是否符合各平台 AI 标注要求"""
        content = params.get("content", "")
        platforms_str = params.get("platforms", ["douyin", "bilibili", "xiaohongshu", "youtube"])
        platforms = [Platform(p) for p in platforms_str if p in Platform.__members__]

        issues: List[ComplianceIssue] = []
        for plat in platforms:
            rule = self._rules.get(plat.value, {})
            # 检查高风险关键词
            for kw in rule.get("risk_high_keywords", []):
                if kw in content:
                    issues.append(ComplianceIssue(
                        issue_id=f"{plat.value}-{kw}",
                        platform=plat,
                        rule="high_risk_keyword",
                        description=f"内容包含高风险关键词：'{kw}'",
                        risk_level=RiskLevel.MEDIUM,
                        suggestion=f"请在平台发布时添加AI标注：{rule.get('label_text', '')}",
                    ))
            # 检查是否缺少AI标注
            if not self._has_ai_label(content):
                issues.append(ComplianceIssue(
                    issue_id=f"{plat.value}-no-label",
                    platform=plat,
                    rule="ai_label_missing",
                    description=f"未在内容中添加AI生成标识",
                    risk_level=RiskLevel.LOW,
                    suggestion=f"建议在内容中添加：{rule.get('label_text', '')}",
                ))

        return {
            "checked_at": time.time(),
            "platforms": [p.value for p in platforms],
            "issues_count": len(issues),
            "issues": [i.to_dict() for i in issues],
            "passed": len(issues) == 0,
        }

    def _check_digital_human(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """检查数字人出镜合规性"""
        has_digital_human = params.get("has_digital_human", False)
        is_commercial = params.get("is_commercial", False)
        platforms_str = params.get("platforms", ["douyin", "bilibili"])

        issues: List[ComplianceIssue] = []
        if has_digital_human:
            for plat_str in platforms_str:
                if plat_str not in Platform.__members__:
                    continue
                plat = Platform(plat_str)
                if is_commercial:
                    issues.append(ComplianceIssue(
                        issue_id=f"{plat.value}-commercial-dh",
                        platform=plat,
                        rule="digital_human_commercial",
                        description="数字人用于商业用途，需额外披露",
                        risk_level=RiskLevel.HIGH,
                        suggestion=(
                            "根据《互联网信息服务深度合成管理规定》，"
                            "数字人商业出镜必须在显著位置标注'本视频含AI生成数字人内容'，"
                            "并确保用户知情同意。"
                        ),
                    ))
                else:
                    issues.append(ComplianceIssue(
                        issue_id=f"{plat.value}-dh-disclose",
                        platform=plat,
                        rule="digital_human_disclosure",
                        description="数字人出镜需进行披露",
                        risk_level=RiskLevel.MEDIUM,
                        suggestion="请在视频描述或画面中添加AI数字人标识。",
                    ))

        return {
            "has_digital_human": has_digital_human,
            "is_commercial": is_commercial,
            "issues_count": len(issues),
            "issues": [i.to_dict() for i in issues],
            "passed": len(issues) == 0,
        }

    def _generate_footer(self, params: Dict[str, Any]) -> str:
        """生成合规页脚文本"""
        platforms_str = params.get("platforms", ["douyin", "bilibili"])
        has_dh = params.get("has_digital_human", False)
        lines: List[str] = ["---"]
        lines.append("【AI生成内容声明】")
        lines.append("本内容部分或全部由人工智能生成，仅供参考。")
        if has_dh:
            lines.append("⚠️ 本内容包含AI生成的数字人形象，请知悉。")
        for plat in platforms_str:
            if plat in self._rules:
                lines.append(f"• {plat}: {self._rules[plat]['label_text']}")
        lines.append("生成时间：" + time.strftime("%Y-%m-%d %H:%M:%S"))
        lines.append("---")
        return "\n".join(lines)

    def _list_rules(self) -> Dict[str, Any]:
        """列出所有合规模则"""
        return {
            "platforms": list(self._rules.keys()),
            "rules": {
                plat: {
                    "ai_label_required": info["ai_label_required"],
                    "label_text": info["label_text"],
                    "placement": info["placement"],
                }
                for plat, info in self._rules.items()
            },
            "legal_basis": [
                "《互联网信息服务深度合成管理规定》（2023年1月10日起施行）",
                "《生成式人工智能服务管理暂行办法》（2023年8月15日起施行）",
                "《广告法》《反不正当竞争法》相关条款",
            ],
        }

    # ------------------------------------------------------------------
    # 内部辅助
    # ------------------------------------------------------------------
    @staticmethod
    def _has_ai_label(content: str) -> bool:
        """检查内容中是否已包含AI标识关键词"""
        ai_keywords = ["AI", "ai", "人工智能", "深度合成", "数字人", "虚拟主播"]
        return any(kw in content for kw in ai_keywords)
