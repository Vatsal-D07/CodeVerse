import fnmatch
from pathlib import Path

from codeverse.tools.base import ToolContext, ToolResult


class SearchTool:
    name = "search"

    def execute(self, payload: dict[str, str], context: ToolContext | None = None) -> ToolResult:
        root_value = payload.get("path")
        pattern = payload.get("pattern", "*")
        if not root_value:
            return ToolResult(ok=False, error="Missing path")

        root = Path(root_value).resolve()
        if context is not None:
            try:
                root.relative_to(context.workspace_root.resolve())
            except ValueError:
                return ToolResult(ok=False, error=f"Path is outside workspace: {root}")
        if not root.exists() or not root.is_dir():
            return ToolResult(ok=False, error=f"Path is not a directory: {root}")

        matches = []
        for item in root.rglob("*"):
            if fnmatch.fnmatch(item.name, pattern):
                matches.append(str(item.relative_to(root)))
        return ToolResult(ok=True, data={"matches": sorted(matches)})
