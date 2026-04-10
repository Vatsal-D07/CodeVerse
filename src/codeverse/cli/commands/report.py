from pathlib import Path

from rich.console import Console
from typer import Argument, Typer

from codeverse.config.settings import get_settings
from codeverse.tools.base import ToolContext
from codeverse.tools.code_analysis import CodeAnalysisTool
from codeverse.tools.search import SearchTool

app = Typer(help="Generate reports")
console = Console()


@app.command("architecture")
def architecture(path: str = Argument(".")) -> None:
    resolved = Path(path).resolve()
    context = ToolContext(workspace_root=get_settings().workspace_root.resolve())
    analysis = CodeAnalysisTool().execute({"path": str(resolved)}, context=context)
    docs = SearchTool().execute({"path": str(resolved), "pattern": "*.md"}, context=context)
    console.print_json(
        data={
            "path": str(resolved),
            "architecture": {
                "tech_stack": analysis.data.get("tech_stack", []),
                "top_extensions": analysis.data.get("top_extensions", []),
                "docs": docs.data.get("matches", [])[:10],
            },
        }
    )
