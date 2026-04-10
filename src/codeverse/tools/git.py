import subprocess
from pathlib import Path
from typing import Any

from codeverse.tools.base import ToolContext, ToolResult


class GitTool:
    name = "git"

    def execute(self, payload: dict[str, Any], context: ToolContext | None = None) -> ToolResult:
        action = payload.get("action", "status")
        root = Path(payload.get("path") or (context.workspace_root if context else Path.cwd())).resolve()
        if action not in {"status", "branch"}:
            return ToolResult(ok=False, error=f"Unsupported action: {action}")
        command = ["git", "-C", str(root), "status", "--short"] if action == "status" else ["git", "-C", str(root), "branch", "--show-current"]
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            return ToolResult(ok=False, error=completed.stderr.strip() or "Not a git repository")
        key = "entries" if action == "status" else "branch"
        value = [line for line in completed.stdout.splitlines() if line] if action == "status" else completed.stdout.strip()
        return ToolResult(ok=True, data={key: value})
