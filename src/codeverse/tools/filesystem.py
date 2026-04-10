from pathlib import Path

from codeverse.tools.base import ToolContext, ToolResult


class FilesystemTool:
    name = "filesystem"

    def execute(self, payload: dict[str, str], context: ToolContext | None = None) -> ToolResult:
        action = payload.get("action")
        path_value = payload.get("path")
        if not path_value:
            return ToolResult(ok=False, error="Missing path")

        path = Path(path_value).resolve()
        if context is not None and not self._is_within_workspace(path, context.workspace_root.resolve()):
            return ToolResult(ok=False, error=f"Path is outside workspace: {path}")
        if not path.exists():
            return ToolResult(ok=False, error=f"Path does not exist: {path}")

        if action == "list":
            if not path.is_dir():
                return ToolResult(ok=False, error=f"Path is not a directory: {path}")
            entries = sorted(item.name + ("/" if item.is_dir() else "") for item in path.iterdir())
            return ToolResult(ok=True, data={"entries": entries})

        if action == "read":
            if not path.is_file():
                return ToolResult(ok=False, error=f"Path is not a file: {path}")
            return ToolResult(ok=True, data={"content": path.read_text(encoding="utf-8")})

        return ToolResult(ok=False, error=f"Unsupported action: {action}")

    @staticmethod
    def _is_within_workspace(path: Path, workspace_root: Path) -> bool:
        try:
            path.relative_to(workspace_root)
            return True
        except ValueError:
            return False
