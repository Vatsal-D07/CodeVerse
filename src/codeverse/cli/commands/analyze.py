from pathlib import Path

from rich.console import Console

from codeverse.config.settings import get_settings
from codeverse.tools.code_analysis import CodeAnalysisTool
from codeverse.tools.filesystem import FilesystemTool
from codeverse.tools.git import GitTool
from codeverse.tools.search import SearchTool
from codeverse.tools.base import ToolContext

console = Console()


def analyze(path: str = ".") -> None:
    resolved = Path(path).resolve()
    context = ToolContext(workspace_root=get_settings().workspace_root.resolve())
    filesystem = FilesystemTool().execute({"action": "list", "path": str(resolved)}, context=context)
    analysis = CodeAnalysisTool().execute({"path": str(resolved)}, context=context)
    git_status = GitTool().execute({"action": "status", "path": str(resolved)}, context=context)
    readme = SearchTool().execute({"path": str(resolved), "pattern": "README*"}, context=context)
    console.print_json(
        data={
            "path": str(resolved),
            "entries": filesystem.data.get("entries", []),
            "analysis": analysis.data,
            "git": git_status.data if git_status.ok else {"error": git_status.error},
            "docs": readme.data.get("matches", []),
        }
    )
