# -*- coding: utf-8 -*-
"""
分析模块 - Tool 使用统计与优化建议
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time
import statistics
from datetime import datetime, timedelta


@dataclass
class ToolCallRecord:
    """工具调用记录"""
    tool_id: str
    params: Dict[str, Any]
    result: Any
    duration_ms: float
    timestamp: float = field(default_factory=time.time)
    success: bool = True
    error: Optional[str] = None


@dataclass
class ToolAnalytics:
    """工具分析数据"""
    tool_id: str
    total_calls: int = 0
    total_duration_ms: float = 0.0
    error_count: int = 0
    avg_duration_ms: float = 0.0
    last_call_at: Optional[float] = None
    peak_hours: List[int] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "total_calls": self.total_calls,
            "avg_duration_ms": round(self.avg_duration_ms, 2),
            "error_rate": round(self.error_count / max(self.total_calls, 1) * 100, 2),
            "last_call_at": datetime.fromtimestamp(self.last_call_at or 0).isoformat() if self.last_call_at else None,
        }


class AnalyticsEngine:
    """分析引擎 - 工具使用统计与优化建议"""
    
    def __init__(self):
        self._records: List[ToolCallRecord] = []
        self._analytics: Dict[str, ToolAnalytics] = {}
        self._max_records = 10000  # 保留最近 10K 条记录
    
    def record_call(
        self,
        tool_id: str,
        params: Dict[str, Any],
        result: Any,
        duration_ms: float,
        success: bool = True,
        error: Optional[str] = None,
    ):
        """记录一次工具调用"""
        record = ToolCallRecord(
            tool_id=tool_id,
            params=params,
            result=result,
            duration_ms=duration_ms,
            success=success,
            error=error,
        )
        
        self._records.append(record)
        
        # 限制记录数量
        if len(self._records) > self._max_records:
            self._records = self._records[-self._max_records:]
        
        # 更新分析数据
        if tool_id not in self._analytics:
            self._analytics[tool_id] = ToolAnalytics(tool_id=tool_id)
        
        analytics = self._analytics[tool_id]
        analytics.total_calls += 1
        analytics.total_duration_ms += duration_ms
        analytics.avg_duration_ms = analytics.total_duration_ms / analytics.total_calls
        analytics.last_call_at = record.timestamp
        
        if not success:
            analytics.error_count += 1
        
        # 更新高峰时段
        hour = datetime.fromtimestamp(record.timestamp).hour
        if hour not in analytics.peak_hours:
            analytics.peak_hours.append(hour)
        analytics.peak_hours.sort()
    
    def get_tool_stats(self, tool_id: str) -> Optional[Dict]:
        """获取单个工具统计"""
        analytics = self._analytics.get(tool_id)
        if not analytics:
            return None
        return analytics.to_dict()
    
    def get_all_stats(self) -> Dict[str, Dict]:
        """获取所有工具统计"""
        return {tid: a.to_dict() for tid, a in self._analytics.items()}
    
    def get_recent_calls(self, hours: int = 1, limit: int = 100) -> List[Dict]:
        """获取最近 N 小时的调用记录"""
        cutoff = time.time() - hours * 3600
        recent = [r for r in self._records if r.timestamp >= cutoff]
        recent.sort(key=lambda x: x.timestamp, reverse=True)
        
        return [
            {
                "tool_id": r.tool_id,
                "duration_ms": r.duration_ms,
                "success": r.success,
                "timestamp": datetime.fromtimestamp(r.timestamp).isoformat(),
            }
            for r in recent[:limit]
        ]
    
    def get_optimization_suggestions(self) -> List[Dict]:
        """获取优化建议"""
        suggestions = []
        
        for tool_id, analytics in self._analytics.items():
            # 高错误率建议
            error_rate = analytics.error_count / max(analytics.total_calls, 1)
            if error_rate > 0.1:
                suggestions.append({
                    "tool_id": tool_id,
                    "type": "error_rate",
                    "severity": "high" if error_rate > 0.3 else "medium",
                    "message": f"工具 {tool_id} 错误率 {error_rate*100:.1f}%，建议检查输入参数",
                })
            
            # 慢调用建议
            if analytics.avg_duration_ms > 1000:
                suggestions.append({
                    "tool_id": tool_id,
                    "type": "slow_call",
                    "severity": "medium",
                    "message": f"工具 {tool_id} 平均耗时 {analytics.avg_duration_ms:.0f}ms，建议添加缓存",
                })
            
            # 低使用率建议
            if analytics.total_calls < 5 and analytics.total_calls > 0:
                suggestions.append({
                    "tool_id": tool_id,
                    "type": "low_usage",
                    "severity": "low",
                    "message": f"工具 {tool_id} 使用次数少 ({analytics.total_calls})，考虑合并或移除",
                })
        
        return suggestions
    
    def get_context_optimization(self) -> Dict:
        """Context 优化建议"""
        if not self._analytics:
            return {"savings": 0, "messages": []}
        
        # 统计各工具 token 消耗（简化估算）
        total_tokens = 0
        savings = 0
        messages = []
        
        for tool_id, analytics in self._analytics.items():
            # 估算每次调用的 token 消耗（平均 200 tokens）
            tool_tokens = analytics.total_calls * 200
            total_tokens += tool_tokens
            
            # 如果错误率高，节省的 token 可以通过重试避免
            if analytics.error_count > 0:
                wasted_tokens = analytics.error_count * 200
                savings += wasted_tokens
                messages.append(f"工具 {tool_id} 错误消耗 {wasted_tokens} tokens")
        
        return {
            "total_tokens_estimated": total_tokens,
            "potential_savings": savings,
            "optimization_rate": f"{savings/max(total_tokens, 1)*100:.1f}%",
            "messages": messages,
        }
    
    def clear_records(self, hours: int = 24):
        """清理过期记录"""
        cutoff = time.time() - hours * 3600
        self._records = [r for r in self._records if r.timestamp >= cutoff]
    
    def export_report(self, format: str = "json") -> str:
        """导出分析报告"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_tools": len(self._analytics),
            "total_calls": sum(a.total_calls for a in self._analytics.values()),
            "total_duration_ms": sum(a.total_duration_ms for a in self._analytics.values()),
            "analytics": {tid: a.to_dict() for tid, a in self._analytics.items()},
            "suggestions": self.get_optimization_suggestions(),
            "context_optimization": self.get_context_optimization(),
        }
        
        import json
        if format == "json":
            return json.dumps(report, ensure_ascii=False, indent=2)
        else:
            # Markdown 格式
            lines = ["# Agent-Forge 分析报告", ""]
            lines.append(f"生成时间: {report['generated_at']}")
            lines.append(f"工具数量: {report['total_tools']}")
            lines.append(f"总调用次数: {report['total_calls']}")
            lines.append("")
            
            for tool_id, stats in report['analytics'].items():
                lines.append(f"## {tool_id}")
                lines.append(f"- 调用次数: {stats['total_calls']}")
                lines.append(f"- 平均耗时: {stats['avg_duration_ms']:.0f}ms")
                lines.append(f"- 错误率: {stats['error_rate']:.1f}%")
                lines.append("")
            
            return "\n".join(lines)
