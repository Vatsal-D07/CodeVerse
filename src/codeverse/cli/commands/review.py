from pathlib import Path

from rich.console import Console
from typer import Argument

from codeverse.config.settings import get_settings
from codeverse.tools.base import ToolContext
from codeverse.tools.code_analysis import CodeAnalysisTool
from codeverse.tools.git import GitTool

console = Console()


def review(path: str = Argument(".")) -> None:
    resolved = Path(path).resolve()
    context = ToolContext(workspace_root=get_settings().workspace_root.resolve())
    analysis = CodeAnalysisTool().execute({"path": str(resolved)}, context=context)
    git_status = GitTool().execute({"action": "status", "path": str(resolved)}, context=context)
    console.print_json(
        data={
            "path": str(resolved),
            "findings": [],
            "analysis": analysis.data,
            "git": git_status.data if git_status.ok else {"error": git_status.error},
        }
    )
