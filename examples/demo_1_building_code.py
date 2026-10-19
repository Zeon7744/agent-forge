# -*- coding: utf-8 -*-
"""
Demo 1: 建筑规范查询工具（GB 标准条款查询）

功能：
- 查询中国国家标准（GB）建筑相关条款
- 支持按关键词、标准号、分类检索
- 内置常用建筑规范知识库
- 生成中文合规检查报告

使用示例::

    # CLI 方式
    python examples/demo_1_building_code.py search --keyword "防火"
    python examples/demo_1_building_code.py detail --code "GB50016"
    python examples/demo_1_building_code.py report --category "结构"

    # Python API 方式
    from agent_forge.tools.chinese_base import ChineseTool
    # 工具会自动注册到 registry
"""

from __future__ import annotations

import sys
import os
from typing import Any, Dict, List, Optional

# 确保可以导入 src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agent_forge.tools.chinese_base import ChineseTool, DataNotFoundError

# ── 内置建筑规范知识库 ────────────────────────────────────────

GB_DATABASE: List[Dict[str, Any]] = [
    {
        "code": "GB50016-2014",
        "name": "建筑设计防火规范",
        "category": "防火",
        "version": "2014版（2018年修订）",
        "key_clauses": [
            "5.1.1 民用建筑根据其建筑高度和层数可分为单层、多层和高层建筑",
            "5.4.3 住宅建筑中设置托育场所时，应采用耐火极限不低于2h的防火隔墙分隔",
            "6.2.4 建筑内的电缆井、管道井应在每层楼板处采用不低于楼板耐火极限的不燃材料封堵",
        ],
        "scope": "适用于新建、扩建和改建的建筑及其附属设施的防火设计",
        "effective_date": "2015-05-01",
    },
    {
        "code": "GB50011-2010",
        "name": "建筑抗震设计规范",
        "category": "结构",
        "version": "2010版（2016年修订）",
        "key_clauses": [
            "3.1.1 建筑应根据其使用功能的重要性和遭遇地震后造成后果的严重性分为四类",
            "4.1.4 建筑场地类别可分为Ⅰ、Ⅱ、Ⅲ、Ⅳ类",
            "5.1.1 各类建筑结构的抗震计算应采用振型分解反应谱法",
        ],
        "scope": "适用于抗震设防烈度为6、7、8、9度地区建筑工程的抗震设计",
        "effective_date": "2010-10-01",
    },
    {
        "code": "GB50007-2011",
        "name": "建筑地基基础设计规范",
        "category": "结构",
        "version": "2011版",
        "key_clauses": [
            "3.0.1 地基基础设计应根据岩土工程勘察成果进行",
            "5.2.1 基础底面的压力不应大于地基承载力特征值",
            "8.5.1 桩基础应按单桩承载力确定桩的竖向承载力",
        ],
        "scope": "适用于工业与民用建筑（包括轻型建筑）的地基基础设计",
        "effective_date": "2012-08-01",
    },
    {
        "code": "GB50009-2012",
        "name": "建筑结构荷载规范",
        "category": "结构",
        "version": "2012版",
        "key_clauses": [
            "5.1.1 楼面均布活荷载的标准值应按规范表5.1.1采用",
            "7.1.1 垂直于建筑物表面上的风荷载标准值按公式计算",
            "8.1.1 屋面活荷载不应与雪荷载同时组合",
        ],
        "scope": "适用于建筑工程的结构设计荷载取值",
        "effective_date": "2012-03-01",
    },
    {
        "code": "GB55037-2022",
        "name": "建筑防火通用规范",
        "category": "防火",
        "version": "2022版（全文强制）",
        "key_clauses": [
            "2.1.1 建筑防火设计应根据建筑的用途、火灾危险性合理确定防火措施",
            "3.2.1 厂房和仓库的火灾危险性应根据生产和储存物品的火灾危险性分类",
            "4.3.2 建筑的疏散门应向疏散方向开启",
        ],
        "scope": "新建、扩建和改建建筑工程的防火设计、施工和使用维护",
        "effective_date": "2023-06-01",
    },
    {
        "code": "GB50018-2002",
        "name": "冷弯薄壁型钢结构技术规范",
        "category": "结构",
        "version": "2002版",
        "key_clauses": [
            "3.1.1 冷弯薄壁型钢构件应在常温下采用冷轧或冷弯成型",
            "4.1.1 受压构件的稳定性应按有效截面计算",
            "8.1.1 焊接连接应采用电弧焊",
        ],
        "scope": "适用于房屋、构筑物中采用的冷弯薄壁型钢结构",
        "effective_date": "2003-03-01",
    },
    {
        "code": "GB50034-2013",
        "name": "建筑照明设计标准",
        "category": "机电",
        "version": "2013版",
        "key_clauses": [
            "4.1.1 各类房间或场所的照明功率密度值不应大于规范表6.1.1的规定",
            "5.1.1 公共走道的地面照度不应低于50lx",
            "6.1.1 办公建筑的照明功率密度限值",
        ],
        "scope": "适用于新建、改建和扩建的建筑照明设计",
        "effective_date": "2014-08-01",
    },
    {
        "code": "GB50189-2015",
        "name": "公共建筑节能设计标准",
        "category": "节能",
        "version": "2015版",
        "key_clauses": [
            "3.2.1 建筑体形系数不应大于规范表3.2.1的规定",
            "4.2.2 外墙的传热系数应满足热工设计要求",
            "5.1.1 暖通空调系统应进行节能设计",
        ],
        "scope": "适用于新建、扩建和改建的公共建筑节能设计",
        "effective_date": "2015-10-01",
    },
]


# ── 工具类 ────────────────────────────────────────────────────

class BuildingCodeTool(ChineseTool):
    """
    建筑规范查询工具

    提供中国国家标准（GB）建筑相关规范的检索、详情查询和合规报告生成功能。
    支持关键词搜索、标准号精确查询和分类筛选。

    注册信息:
        tool_id: building.code
        name: query_building_code
        category: chinese
    """

    tool_id = "building.code"
    tool_name = "query_building_code"
    tool_description = "查询中国国家标准（GB）建筑规范条款，支持关键词搜索和分类筛选"
    tool_category = "chinese"
    tool_tags = ["建筑", "GB标准", "合规", "查询"]

    def get_input_properties(self) -> Dict[str, Any]:
        return {
            "keyword": {
                "type": "string",
                "description": "搜索关键词（如：防火、抗震、荷载）",
            },
            "code": {
                "type": "string",
                "description": "标准编号（如：GB50016）",
            },
            "category": {
                "type": "string",
                "enum": ["防火", "结构", "机电", "节能", "全部"],
                "description": "规范分类",
            },
        }

    def get_required_fields(self) -> List[str]:
        return []  # 全部可选，至少提供一个查询条件

    def process(
        self,
        keyword: Optional[str] = None,
        code: Optional[str] = None,
        category: Optional[str] = None,
    ) -> dict:
        """
        执行建筑规范查询

        Args:
            keyword: 搜索关键词
            code: 标准编号
            category: 分类筛选

        Returns:
            查询结果字典
        """
        # 精确查找标准号
        if code:
            matches = self._search_by_code(code)
            if not matches:
                raise DataNotFoundError(f"未找到标准号: {code}")
            return {
                "query": f"标准号: {code}",
                "status": "success",
                "count": len(matches),
                "items": matches,
            }

        # 关键词搜索
        if keyword:
            matches = self._search_by_keyword(keyword)
            return {
                "query": f"关键词: {keyword}",
                "status": "success",
                "count": len(matches),
                "items": matches,
            }

        # 分类筛选
        if category and category != "全部":
            matches = self._search_by_category(category)
            return {
                "query": f"分类: {category}",
                "status": "success",
                "count": len(matches),
                "items": matches,
            }

        # 无参数时返回全部
        return {
            "query": "全部规范",
            "status": "success",
            "count": len(GB_DATABASE),
            "items": [self._brief(r) for r in GB_DATABASE],
        }

    def _search_by_code(self, code: str) -> List[Dict[str, Any]]:
        """按标准号搜索（支持模糊匹配）"""
        results = []
        code_upper = code.upper().replace(" ", "")
        for record in GB_DATABASE:
            if code_upper in record["code"].upper():
                results.append(record)
        return results

    def _search_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """按关键词全文搜索"""
        results = []
        for record in GB_DATABASE:
            searchable = (
                record["name"]
                + record["category"]
                + record["scope"]
                + " ".join(record["key_clauses"])
            )
            if keyword in searchable:
                results.append(record)
        return results

    def _search_by_category(self, category: str) -> List[Dict[str, Any]]:
        """按分类筛选"""
        return [r for r in GB_DATABASE if r["category"] == category]

    def generate_compliance_report(self, category: str = "全部") -> str:
        """
        生成建筑合规检查报告

        Args:
            category: 报告涉及的分类

        Returns:
            Markdown 格式的报告
        """
        if category == "全部":
            records = GB_DATABASE
        else:
            records = [r for r in GB_DATABASE if r["category"] == category]

        clauses_summary = []
        for r in records:
            clauses_summary.append(f"**{r['code']} {r['name']}** — {len(r['key_clauses'])} 条关键条款")

        sections = [
            {
                "heading": "查询概览",
                "content": f"本次查询分类: {category}，共检索到 {len(records)} 部国家标准。",
            },
            {
                "heading": "涉及标准",
                "content": clauses_summary,
            },
            {
                "heading": "关键条款索引",
                "content": [
                    f"{r['code']} 第{'、'.join(c.split(' ')[0] for c in r['key_clauses'][:3])} 条"
                    for r in records
                ],
            },
            {
                "heading": "合规建议",
                "content": [
                    "请确保设计文件符合最新版本标准要求",
                    "注意地方标准与国家标准的协调执行",
                    "强制条文必须严格执行，不得降低标准",
                    "建议结合当地住建部门要求综合判定",
                ],
            },
        ]
        return self.generate_report(
            title=f"建筑规范合规检查报告（{category}类）",
            sections=sections,
        )

    @staticmethod
    def _brief(record: Dict[str, Any]) -> Dict[str, str]:
        """生成简要条目"""
        return {
            "code": record["code"],
            "name": record["name"],
            "category": record["category"],
            "version": record["version"],
        }

    @staticmethod
    def list_categories() -> List[str]:
        """列出所有可用分类"""
        return sorted(set(r["category"] for r in GB_DATABASE))


# ── Typer CLI ─────────────────────────────────────────────────

try:
    import typer
    from rich.console import Console
    from rich.table import Table

    app = typer.Typer(help="建筑规范查询工具 - 查询 GB 标准条款")
    console = Console()

    @app.command("search")
    def search(
        keyword: str = typer.Argument(..., help="搜索关键词"),
    ):
        """按关键词搜索建筑规范"""
        tool = BuildingCodeTool()
        result = tool.process(keyword=keyword)
        _display_results(result)

    @app.command("detail")
    def detail(
        code: str = typer.Argument(..., help="标准编号（如 GB50016）"),
    ):
        """查看标准详情"""
        tool = BuildingCodeTool()
        result = tool.process(code=code)
        if result["count"] == 0:
            console.print("[red]未找到匹配的标准[/red]")
            raise typer.Exit(1)
        item = result["items"][0]
        console.print(f"\n[bold cyan]{item['code']} {item['name']}[/bold cyan]")
        console.print(f"分类: {item['category']}  |  版本: {item['version']}")
        console.print(f"适用范围: {item['scope']}")
        console.print(f"生效日期: {item['effective_date']}")
        console.print("\n[bold]关键条款:[/bold]")
        for clause in item["key_clauses"]:
            console.print(f"  • {clause}")

    @app.command("report")
    def report(
        category: str = typer.Option("全部", "--category", "-c", help="规范分类"),
    ):
        """生成合规检查报告"""
        tool = BuildingCodeTool()
        md = tool.generate_compliance_report(category)
        console.print(md)

    @app.command("categories")
    def categories():
        """列出所有可用分类"""
        cats = BuildingCodeTool.list_categories()
        console.print("[bold]可用分类:[/bold]")
        for c in cats:
            console.print(f"  • {c}")

    def _display_results(result: dict):
        """Rich 表格展示查询结果"""
        items = result.get("items", [])
        if not items:
            console.print("[yellow]未找到匹配结果[/yellow]")
            return
        table = Table(title=f"查询结果: {result['query']}（共 {result['count']} 条）")
        table.add_column("标准号", style="cyan")
        table.add_column("名称", style="green")
        table.add_column("分类", style="magenta")
        table.add_column("版本")
        for item in items:
            table.add_row(
                item.get("code", ""),
                item.get("name", ""),
                item.get("category", ""),
                item.get("version", ""),
            )
        console.print(table)

except ImportError:
    # 无 typer/rich 时的降级入口
    app = None

    def main():
        tool = BuildingCodeTool()
        result = tool.process(category="防火")
        print(tool.format_result(result))


if __name__ == "__main__":
    if app is not None:
        app()
    else:
        main()
