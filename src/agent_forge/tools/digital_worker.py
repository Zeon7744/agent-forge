# -*- coding: utf-8 -*-
"""
数字员工工具 - 24名数字员工调度编排

提供数字员工注册、调度、限流与订阅层级控制能力。
免费版限制 3 名员工，Pro 版解锁全部 24 名。

角色清单：
  编剧(1-3)、导演(4-6)、运营(7-9)、合规(10-12)、
  视觉(13-15)、配音(16-18)、剪辑(19-21)、数据(22-24)
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .base import ToolBase, ToolInputSchema


class EmployeeRole(str, Enum):
    """数字员工角色枚举"""
    SCREENWRITER = "screenwriter"    # 编剧
    DIRECTOR = "director"            # 导演
    OPERATOR = "operator"            # 运营
    COMPLIANCE = "compliance"        # 合规
    VISUAL = "visual"                # 视觉
    VOICE = "voice"                  # 配音
    EDITOR = "editor"                # 剪辑
    DATA = "data"                    # 数据


@dataclass
class DigitalEmployee:
    """单个数字员工实体"""
    employee_id: str
    role: EmployeeRole
    name: str
    status: str = "idle"           # idle / busy / offline
    current_task: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    tasks_completed: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "employee_id": self.employee_id,
            "role": self.role.value,
            "name": self.name,
            "status": self.status,
            "current_task": self.current_task,
            "created_at": self.created_at,
            "tasks_completed": self.tasks_completed,
        }


class DigitalWorkerTool(ToolBase):
    """
    数字员工调度工具。

    支持操作：list / assign / execute / status / free
    免费版最多 3 名员工，Pro 版解锁全部 24 名。
    """

    def __init__(self):
        super().__init__(
            tool_id="digital_worker",
            name="digital_worker",
            description=(
                "数字员工调度工具：注册、分配任务、查询状态。"
                "免费版限 3 名员工，Pro 版解锁 24 名。"
            ),
            input_schema=ToolInputSchema(
                properties={
                    "action": {"type": "string", "enum": ["list", "assign", "execute", "status", "free"], "description": "操作类型"},
                    "employee_id": {"type": "string", "description": "员工 ID（assign/execute/status/free 时使用）"},
                    "role": {"type": "string", "enum": [r.value for r in EmployeeRole], "description": "员工角色"},
                    "task": {"type": "string", "description": "任务描述"},
                    "plan": {"type": "string", "enum": ["free", "pro"], "description": "订阅层级"},
                },
                required=["action"],
            ),
        )
        self._employees: Dict[str, DigitalEmployee] = {}
        self._plan: str = "free"
        self._MAX_FREE = 3
        self._MAX_PRO = 24
        self._init_default_employees()

    # ------------------------------------------------------------------
    # 初始化
    # ------------------------------------------------------------------
    def _init_default_employees(self):
        """按角色生成 24 名默认数字员工（仅 Pro 可见，free 时只暴露前 3 名）"""
        role_map = {
            EmployeeRole.SCREENWRITER: ("编剧-{n}", 3),
            EmployeeRole.DIRECTOR: ("导演-{n}", 3),
            EmployeeRole.OPERATOR: ("运营-{n}", 3),
            EmployeeRole.COMPLIANCE: ("合规-{n}", 3),
            EmployeeRole.VISUAL: ("视觉-{n}", 3),
            EmployeeRole.VOICE: ("配音-{n}", 3),
            EmployeeRole.EDITOR: ("剪辑-{n}", 3),
            EmployeeRole.DATA: ("数据-{n}", 3),
        }
        idx = 1
        for role, (template, count) in role_map.items():
            for n in range(1, count + 1):
                eid = f"emp-{idx:03d}"
                self._employees[eid] = DigitalEmployee(
                    employee_id=eid,
                    role=role,
                    name=template.format(n=n),
                )
                idx += 1

    def set_plan(self, plan: str):
        """设置订阅层级（free / pro）"""
        self._plan = plan

    @property
    def active_limit(self) -> int:
        return self._MAX_PRO if self._plan == "pro" else self._MAX_FREE

    # ------------------------------------------------------------------
    # 工具接口
    # ------------------------------------------------------------------
    def execute(self, params: Dict[str, Any]) -> Any:
        action = params.get("action", "list")

        handlers = {
            "list": self._action_list,
            "assign": self._action_assign,
            "execute": self._action_execute,
            "status": self._action_status,
            "free": self._action_free,
        }
        handler = handlers.get(action)
        if not handler:
            return {"error": f"Unknown action: {action}"}
        return handler(params)

    def _action_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """列出当前可用员工"""
        plan = params.get("plan", self._plan)
        limit = self._MAX_PRO if plan == "pro" else self._MAX_FREE
        available = [
            emp.to_dict()
            for emp in self._employees.values()
            if emp.status == "idle"
        ][:limit]
        return {
            "plan": plan,
            "limit": limit,
            "total_idle": len(available),
            "employees": available,
        }

    def _action_assign(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """将任务分配给指定员工"""
        employee_id = params.get("employee_id")
        task = params.get("task", "")
        if not employee_id or employee_id not in self._employees:
            return {"error": f"Employee not found: {employee_id}"}
        emp = self._employees[employee_id]
        if emp.status != "idle":
            return {"error": f"Employee {employee_id} is {emp.status}"}
        emp.status = "busy"
        emp.current_task = task
        return {
            "assigned": True,
            "employee": emp.to_dict(),
        }

    def _action_execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行已分配任务（模拟）"""
        employee_id = params.get("employee_id")
        if not employee_id or employee_id not in self._employees:
            return {"error": f"Employee not found: {employee_id}"}
        emp = self._employees[employee_id]
        if emp.status != "busy":
            return {"error": f"Employee {employee_id} is not busy"}
        result = {
            "employee_id": employee_id,
            "task": emp.current_task,
            "output": f"[模拟] {emp.role.value}完成：{emp.current_task}",
            "timestamp": time.time(),
        }
        emp.status = "idle"
        emp.current_task = None
        emp.tasks_completed += 1
        return result

    def _action_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """查询员工状态"""
        employee_id = params.get("employee_id")
        if employee_id and employee_id in self._employees:
            return self._employees[employee_id].to_dict()
        # 汇总
        idle = sum(1 for e in self._employees.values() if e.status == "idle")
        busy = sum(1 for e in self._employees.values() if e.status == "busy")
        return {
            "total": len(self._employees),
            "idle": idle,
            "busy": busy,
            "plan": self._plan,
            "limit": self.active_limit,
        }

    def _action_free(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """释放指定员工（停止当前任务）"""
        employee_id = params.get("employee_id")
        if not employee_id or employee_id not in self._employees:
            return {"error": f"Employee not found: {employee_id}"}
        emp = self._employees[employee_id]
        if emp.status == "busy":
            emp.status = "idle"
            emp.current_task = None
        return {"freed": True, "employee": emp.to_dict()}
