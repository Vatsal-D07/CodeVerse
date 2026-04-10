import shlex
import subprocess
from pathlib import Path
from typing import Any

from codeverse.config.settings import get_settings
from codeverse.tools.base import ToolContext, ToolResult


class ShellTool:
    name = "shell"

    def execute(self, payload: dict[str, Any], context: ToolContext | None = None) -> ToolResult:
        settings = get_settings()
        if not settings.safety.allow_shell:
            return ToolResult(ok=False, error="Shell execution is disabled")

        command = payload.get("command")
        if not command:
            return ToolResult(ok=False, error="Missing command")

        argv = command if isinstance(command, list) else shlex.split(str(command))
        if not argv:
            return ToolResult(ok=False, error="Missing command")
        if argv[0] not in settings.safety.allowed_shell_commands:
            return ToolResult(ok=False, error=f"Command '{argv[0]}' is not allowed")

        cwd_value = payload.get("cwd")
        cwd = Path(cwd_value).resolve() if cwd_value else (context.workspace_root if context else Path.cwd())
        timeout = int(payload.get("timeout", settings.safety.max_command_timeout_seconds))
        try:
            completed = subprocess.run(
                argv,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return ToolResult(ok=False, error=f"Command timed out after {timeout} seconds")

        return ToolResult(
            ok=completed.returncode == 0,
            data={"stdout": completed.stdout, "stderr": completed.stderr, "returncode": completed.returncode},
            error=None if completed.returncode == 0 else f"Command failed with exit code {completed.returncode}",
        )
