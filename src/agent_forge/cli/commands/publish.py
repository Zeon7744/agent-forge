# -*- coding: utf-8 -*-
"""
forge publish 命令实现
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()


def handle_publish(skill_path: str):
    """发布 Skill 到注册表"""
    path = Path(skill_path).resolve()
    
    # 检查必要文件
    required_files = ["pyproject.toml", "README.md"]
    for f in required_files:
        if not (path / f).exists():
            console.print(f"[red]错误: 缺少必要文件 {f}[/red]")
            sys.exit(1)
    
    console.print(Panel(
        f"[bold]发布 Skill[/bold]\n\n"
        f"名称: {path.name}\n"
        f"路径: {path}\n\n"
        f"下一步:\n"
        f"  1. 构建包: pip wheel -w dist .\n"
        f"  2. 上传到注册表: twine upload dist/*\n"
        f"  3. 通知社区: forge announce {path.name}",
        title="forge publish",
    ))
