# -*- coding: utf-8 -*-
"""
Demo 3: 内容安全审核工具

功能：
- 敏感词检测（内置中文敏感词库）
- 违禁词过滤（政治/暴力/色情等分类）
- 违规程度评分（低/中/高风险）
- 生成审核报告和合规建议

使用示例::

    # CLI 方式
    python examples/demo_3_content_audit.py check --text "这是一段测试文本"
    python examples/demo_3_content_audit.py filter --text "需要过滤的文本" --level high
    python examples/demo_3_content_audit.py report --text "长文本内容"

    # Python API 方式
    from agent_forge.tools.chinese_base import ChineseTool
"""

from __future__ import annotations

import sys
import os
import re
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agent_forge.tools.chinese_base import ChineseTool, ValidationError


# ── 内置敏感词库（分类示例）────────────────────────────────────

SENSITIVE_WORDS: Dict[str, List[str]] = {
    "政治敏感": [
        "涉政关键词1", "涉政关键词2", "涉政关键词3",
    ],
    "暴力恐怖": [
        "暴力关键词1", "暴力关键词2", "恐怖关键词1",
    ],
    "色情低俗": [
        "色情关键词1", "低俗关键词1",
    ],
    "谣言欺诈": [
        "谣言关键词1", "欺诈关键词1", "虚假关键词1",
    ],
    "广告 spam": [
        "加微信", "扫码领取", "限时优惠", "点击链接",
    ],
}

# 合并所有敏感词用于快速检索
ALL_SENSITIVE_TERMS = []
for terms in SENSITIVE_WORDS.values():
    ALL_SENSITIVE_TERMS.extend(terms)

# ── 风险等级映射 ──────────────────────────────────────────────

RISK_LEVELS = {
    "政治敏感": {"level": "高", "score": 90, "action": "立即删除"},
    "暴力恐怖": {"level": "高", "score": 85, "action": "立即删除"},
    "色情低俗": {"level": "高", "score": 80, "action": "删除并封号"},
    "谣言欺诈": {"level": "中", "score": 60, "action": "标记可疑"},
    "广告 spam": {"level": "低", "score": 30, "action": "建议删除"},
}


# ── 工具类 ────────────────────────────────────────────────────

class ContentAuditTool(ChineseTool):
    """
    内容安全审核工具

    对中文文本进行敏感词检测、违禁词过滤和风险评分，
    生成审核报告并提供合规建议。

    注册信息:
        tool_id: content.audit
        name: audit_content
        category: chinese
    """

    tool_id = "content.audit"
    tool_name = "audit_content"
    tool_description = "内容安全审核，检测敏感词、违禁词并生成风险评分和合规建议"
    tool_category = "chinese"
    tool_tags = ["内容安全", "敏感词检测", "风控", "审核"]

    def get_input_properties(self) -> Dict[str, Any]:
        return {
            "text": {
                "type": "string",
                "description": "待审核的文本内容",
            },
            "strict": {
                "type": "boolean",
                "description": "是否启用严格模式（默认 False）",
                "default": False,
            },
            "category": {
                "type": "string",
                "enum": ["全部", "政治敏感", "暴力恐怖", "色情低俗", "谣言欺诈", "广告 spam"],
                "description": "审核类别（默认全部）",
            },
        }

    def get_required_fields(self) -> List[str]:
        return ["text"]

    def process(
        self,
        text: str,
        strict: bool = False,
        category: str = "全部",
    ) -> dict:
        """
        执行内容审核

        Args:
            text: 待审核文本
            strict: 严格模式
            category: 审核类别

        Returns:
            包含检测结果和风险评分的分析结果
        """
        if not text or not text.strip():
            raise ValidationError("待审核文本不能为空", field="text")

        # 执行检测
        findings = self._detect_sensitive(text, category)

        # 计算风险评分
        risk_score = self._calculate_risk_score(findings, strict)

        # 判定风险等级
        risk_level = self._classify_risk(risk_score)

        # 生成建议
        recommendations = self._generate_recommendations(findings, risk_level)

        return {
            "text_length": len(text),
            "findings_count": len(findings),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "findings": findings,
            "recommendations": recommendations,
            "strict_mode": strict,
        }

    def _detect_sensitive(
        self, text: str, category: str
    ) -> List[Dict[str, Any]]:
        """
        检测敏感词

        Args:
            text: 待检测文本
            category: 审核类别

        Returns:
            敏感词列表
        """
        findings = []
        text_lower = text.lower()

        if category == "全部":
            categories = list(SENSITIVE_WORDS.keys())
        else:
            categories = [category]

        for cat in categories:
            for word in SENSITIVE_WORDS.get(cat, []):
                if word in text_lower:
                    findings.append({
                        "word": word,
                        "category": cat,
                        "position": text_lower.find(word),
                        "severity": RISK_LEVELS.get(cat, {}).get("score", 50),
                    })

        # 去重并按位置排序
        seen = set()
        unique_findings = []
        for f in sorted(findings, key=lambda x: x["position"]):
            if f["word"] not in seen:
                seen.add(f["word"])
                unique_findings.append(f)

        return unique_findings

    def _calculate_risk_score(
        self, findings: List[Dict[str, Any]], strict: bool
    ) -> int:
        """
        计算综合风险评分

        Args:
            findings: 检测结果列表
            strict: 严格模式

        Returns:
            0-100 的风险评分
        """
        if not findings:
            return 0

        total_score = sum(f["severity"] for f in findings)
        max_possible = len(findings) * 100

        # 归一化到 0-100
        score = min(100, int(total_score / max(max_possible, 1) * 100))

        # 严格模式额外加权
        if strict:
            score = min(100, int(score * 1.3))

        return score

    def _classify_risk(self, score: int) -> str:
        """
        判定风险等级

        Args:
            score: 风险评分

        Returns:
            风险等级字符串
        """
        if score >= 80:
            return "高风险"
        elif score >= 50:
            return "中风险"
        elif score >= 10:
            return "低风险"
        return "无风险"

    def _generate_recommendations(
        self, findings: List[Dict[str, Any]], risk_level: str
    ) -> List[str]:
        """
        生成合规建议

        Args:
            findings: 检测结果
            risk_level: 风险等级

        Returns:
            建议列表
        """
        recs = []

        if risk_level == "无风险":
            recs.append("✅ 内容通过审核，可以正常发布")
        elif risk_level == "低风险":
            recs.append("⚠️ 检测到轻微违规内容，建议修改后重新提交")
            recs.append("请检查以下内容并调整措辞")
        elif risk_level == "中风险":
            recs.append("🚫 检测到中等风险内容，建议删除违规部分")
            recs.append("违规内容占比超过 20%，需人工复核")
        else:
            recs.append("❌ 检测到高风险内容，建议立即删除")
            recs.append("请立即下架该内容并进行合规审查")
            recs.append("考虑对相关账号进行警告或限制")

        # 根据具体发现添加针对性建议
        categories_found = set(f["category"] for f in findings)
        for cat in categories_found:
            action = RISK_LEVELS.get(cat, {}).get("action", "处理")
            recs.append(f"涉及「{cat}」类问题，建议：{action}")

        return recs

    def filter_text(
        self, text: str, level: str = "全部", replace_char: str = "*"
    ) -> str:
        """
        过滤敏感词

        Args:
            text: 原文本
            level: 过滤级别（全部/高/中/低）
            replace_char: 替换字符

        Returns:
            过滤后的文本
        """
        result = text
        terms_to_filter = []

        if level == "全部":
            terms_to_filter = ALL_SENSITIVE_TERMS
        else:
            # 根据级别筛选
            if level == "高":
                for cat, info in RISK_LEVELS.items():
                    if info["score"] >= 80:
                        terms_to_filter.extend(SENSITIVE_WORDS.get(cat, []))
            elif level == "中":
                for cat, info in RISK_LEVELS.items():
                    if 50 <= info["score"] < 80:
                        terms_to_filter.extend(SENSITIVE_WORDS.get(cat, []))
            else:
                for cat, info in RISK_LEVELS.items():
                    if info["score"] < 50:
                        terms_to_filter.extend(SENSITIVE_WORDS.get(cat, []))

        # 执行替换
        for term in terms_to_filter:
            result = result.replace(term, replace_char * len(term))

        return result

    def generate_audit_report(
        self, text: str, strict: bool = False, category: str = "全部"
    ) -> str:
        """
        生成完整审核报告

        Args:
            text: 待审核文本
            strict: 严格模式
            category: 审核类别

        Returns:
            Markdown 格式的审核报告
        """
        result = self.process(text, strict, category)

        sections = [
            {
                "heading": "审核概览",
                "content": [
                    f"文本长度: {result['text_length']} 字符",
                    f"检测结果: {result['findings_count']} 条敏感词",
                    f"风险评分: {result['risk_score']}/100",
                    f"风险等级: **{result['risk_level']}**",
                    f"审核模式: {'严格模式' if result['strict_mode'] else '普通模式'}",
                ],
            },
        ]

        if result["findings"]:
            findings_lines = [
                f"- {f['word']}（{f['category']}，严重程度: {f['severity']}）"
                for f in result["findings"]
            ]
            sections.append({
                "heading": "敏感词详情",
                "content": findings_lines,
            })

        sections.append({
            "heading": "处理建议",
            "content": result["recommendations"],
        })

        return self.generate_report(
            title="内容安全审核报告",
            sections=sections,
        )


# ── Typer CLI ─────────────────────────────────────────────────

try:
    import typer
    from rich.console import Console
    from rich.table import Table

    app = typer.Typer(help="内容安全审核工具")
    console = Console()

    @app.command("check")
    def check(
        text: str = typer.Argument(..., help="待审核文本"),
        strict: bool = typer.Option(False, "--strict", "-s", help="严格模式"),
        category: str = typer.Option("全部", "--category", "-c", help="审核类别"),
    ):
        """审核文本内容"""
        tool = ContentAuditTool()
        result = tool.process(text, strict, category)
        
        console.print(f"\n[bold]文本长度:[/bold] {result['text_length']} 字符")
        console.print(f"[bold]检测结果:[/bold] {result['findings_count']} 条敏感词")
        console.print(f"[bold]风险评分:[/bold] {result['risk_score']}/100")
        
        risk_color = {
            "高风险": "red",
            "中风险": "yellow",
            "低风险": "blue",
            "无风险": "green",
        }.get(result["risk_level"], "white")
        
        console.print(f"[bold {risk_color}]风险等级: {result['risk_level']}[/bold {risk_color}]")
        
        if result["findings"]:
            console.print("\n[bold]敏感词列表:[/bold]")
            for f in result["findings"]:
                console.print(f"  • {f['word']} — {f['category']}（严重程度: {f['severity']}）")
        
        console.print("\n[bold]处理建议:[/bold]")
        for rec in result["recommendations"]:
            console.print(f"  {rec}")

    @app.command("filter")
    def filter_text(
        text: str = typer.Argument(..., help="待过滤文本"),
        level: str = typer.Option("全部", "--level", "-l", help="过滤级别: 全部/高/中/低"),
        char: str = typer.Option("*", "--char", help="替换字符"),
    ):
        """过滤敏感词"""
        tool = ContentAuditTool()
        result = tool.filter_text(text, level, char)
        console.print(f"\n[bold]过滤后文本:[/bold]")
        console.print(result)

    @app.command("report")
    def report(
        text: str = typer.Argument(..., help="待审核文本"),
        strict: bool = typer.Option(False, "--strict", "-s", help="严格模式"),
        category: str = typer.Option("全部", "--category", "-c", help="审核类别"),
    ):
        """生成完整审核报告"""
        tool = ContentAuditTool()
        md = tool.generate_audit_report(text, strict, category)
        console.print(md)

    @app.command("categories")
    def categories():
        """列出所有审核类别"""
        console.print("[bold]可用审核类别:[/bold]")
        for cat, words in SENSITIVE_WORDS.items():
            console.print(f"  • {cat}: {len(words)} 个词")

except ImportError:
    app = None

    def main():
        tool = ContentAuditTool()
        sample_text = "这是一段包含敏感词的测试文本：敏感词1、敏感词2"
        result = tool.process(sample_text)
        print(tool.format_result(result))


if __name__ == "__main__":
    if app is not None:
        app()
    else:
        main()
