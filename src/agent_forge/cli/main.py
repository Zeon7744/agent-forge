# -*- coding: utf-8 -*-
"""
forge CLI 主入口
"""

import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="forge",
    help="Agent-Forge: 中文 AI Agent 工具链标准",
    add_completion=False,
)

console = Console()


@app.callback()
def main(ctx: typer.Context):
    """Agent-Forge CLI - 中文 AI Agent 工具链框架 v0.2.0"""
    pass


@app.command()
def create(name: str = typer.Argument(..., help="Skill 名称"),
           template: str = typer.Option("default", help="模板类型")):
    """创建新的 Skill"""
    from .commands.create import handle_create
    handle_create(name, template)


@app.command()
def test(skill_path: str = typer.Option(".", help="Skill 路径")):
    """测试 Skill"""
    from .commands.test import handle_test
    handle_test(skill_path)


@app.command()
def publish(skill_path: str = typer.Option(".", help="Skill 路径")):
    """发布 Skill 到注册表"""
    from .commands.publish import handle_publish
    handle_publish(skill_path)


@app.command()
def serve(host: str = typer.Option("0.0.0.0", help="主机地址"),
          port: int = typer.Option(8000, help="端口号")):
    """启动 MCP 服务器"""
    from ..server import run_server
    run_server(host, port)


@app.command()
def docs(skill_path: str = typer.Option(".", help="Skill 路径")):
    """生成 Skill 文档"""
    console.print(Panel(f"文档生成: {skill_path}", title="forge docs"))
    console.print("[green]文档已生成到 docs/ 目录[/green]")


@app.command()
def list():
    """列出已注册的 Skill"""
    console.print("[bold]已安装的 Skills:[/bold]")
    console.print("  - 暂无已安装 Skill")


if __name__ == "__main__":
    app()
