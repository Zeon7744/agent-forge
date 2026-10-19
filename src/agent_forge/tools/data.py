# -*- coding: utf-8 -*-
"""
数据分析工具
"""

from .base import ToolBase, ToolInputSchema
from agent_forge.registry import registry


class DataStatsTool(ToolBase):
    """数据统计工具"""
    
    def __init__(self):
        super().__init__(
            tool_id="data.stats",
            name="data_statistics",
            description="计算数据集的统计指标",
            input_schema=ToolInputSchema(
                properties={
                    "data": {"type": "array", "items": {"type": "number"}, "description": "数值数据"},
                    "metrics": {"type": "array", "items": {"type": "string"}, "description": "需要计算的指标"},
                },
                required=["data"],
            ),
        )
        registry.register(
            tool_id=self.tool_id,
            name=self.name,
            description=self.description,
            handler=self.execute,
            input_schema=self.input_schema.to_dict(),
            category="data",
            tags=["统计", "分析"],
        )
    
    def execute(self, data: list, metrics: list = None) -> str:
        """执行数据统计"""
        if not data:
            return "数据为空"
        
        import statistics
        result = {
            "count": len(data),
            "mean": statistics.mean(data),
            "median": statistics.median(data),
            "stdev": statistics.stdev(data) if len(data) > 1 else 0,
            "min": min(data),
            "max": max(data),
        }
        return str(result)
