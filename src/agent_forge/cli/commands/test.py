# -*- coding: utf-8 -*-
"""
forge test 命令实现
"""

import sys
import subprocess
from pathlib import Path
from rich.console import Console

console = Console()


def handle_test(skill_path: str):
    """测试 Skill"""
    path = Path(skill_path).resolve()
    
    if not (path / "pyproject.toml").exists():
        console.print(f"[red]错误: 找不到 {path}/pyproject.toml[/red]")
        sys.exit(1)
    
    # 运行 pytest
    console.print(f"[bold]运行测试: {path}[/bold]")
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(path / "tests"), "-v", "--tb=short"],
        cwd=path,
        capture_output=True,
        text=True,
    )
    
    console.print(result.stdout)
    if result.stderr:
        console.print(result.stderr, style="red")
    
    if result.returncode == 0:
        console.print("[green]✅ 测试通过[/green]")
    else:
        console.print("[red]❌ 测试失败[/red]")
        sys.exit(result.returncode)
