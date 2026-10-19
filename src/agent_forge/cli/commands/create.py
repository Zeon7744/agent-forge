# -*- coding: utf-8 -*-
"""
forge create 命令实现
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()


def handle_create(name: str, template: str):
    """创建新 Skill"""
    # 验证名称
    if not name.replace("-", "").replace("_", "").isalnum():
        console.print(f"[red]错误: Skill 名称只能包含字母、数字、连字符和下划线[/red]")
        sys.exit(1)
    
    # 确定目标目录
    target_dir = Path.cwd() / name
    
    if target_dir.exists():
        console.print(f"[red]错误: 目录 {name} 已存在[/red]")
        sys.exit(1)
    
    # 创建目录结构
    template_dirs = [
        f"{name}/src/{name.replace('-', '_')}",
        f"{name}/tests",
        f"{name}/docs",
    ]
    
    for d in template_dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    
    # 创建 __init__.py
    (Path(name) / "src" / name.replace("-", "_") / "__init__.py").write_text(
        '# -*- coding: utf-8 -*-\n"""' + name + '"""\n'
    )
    
    # 创建测试文件
    (Path(name) / "tests" / "test_" + name.replace("-", "_") + ".py").write_text(
        '# -*- coding: utf-8 -*-\n"""' + name + ' 测试"""\n\ndef test_' + name.replace("-", "_") + '():\n    assert True\n'
    )
    
    # 创建 README
    (Path(name) / "README.md").write_text(
        f"# {name}\n\n> {name} - Agent-Forge Skill\n\n## 快速开始\n\n```bash\npip install -e .\n```\n"
    )
    
    # 创建 pyproject.toml
    (Path(name) / "pyproject.toml").write_text(
        f'''[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "{name}"
version = "0.1.0"
description = "{name} - Agent-Forge Skill"
requires-python = ">=3.10"
dependencies = [
    "agent-forge>=0.2.0",
]

[tool.setuptools.packages.find]
where = ["src"]
'''
    )
    
    console.print(Panel(
        f"[green]✅ 创建成功![/green]\n\n"
        f"Skill 名称: {name}\n"
        f"目录路径: {target_dir}\n"
        f"模板类型: {template}\n\n"
        f"下一步:\n"
        f"  cd {name}\n"
        f"  forge test\n"
        f"  forge publish",
        title="forge create",
    ))
