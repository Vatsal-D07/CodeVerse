from pathlib import Path

from rich.console import Console
from typer import Argument

from codeverse.config.settings import get_settings
from codeverse.tools.base import ToolContext
from codeverse.tools.code_analysis import CodeAnalysisTool
from codeverse.tools.filesystem import FilesystemTool

console = Console()


def explain(path: str = Argument(".")) -> None:
    resolved = Path(path).resolve()
    context = ToolContext(workspace_root=get_settings().workspace_root.resolve())
    filesystem = FilesystemTool().execute({"action": "list", "path": str(resolved)}, context=context)
    analysis = CodeAnalysisTool().execute({"path": str(resolved)}, context=context)
    console.print_json(
        data={
            "path": str(resolved),
            "summary": {
                "file_count": analysis.data.get("file_count", 0),
                "tech_stack": analysis.data.get("tech_stack", []),
                "sample_entries": filesystem.data.get("entries", [])[:10],
            },
        }
    )
