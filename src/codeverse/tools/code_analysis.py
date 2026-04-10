from collections import Counter
from pathlib import Path
from typing import Any

from codeverse.tools.base import ToolContext, ToolResult


class CodeAnalysisTool:
    name = "code_analysis"

    STACK_HINTS = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "React/TypeScript",
        ".jsx": "React/JavaScript",
        ".go": "Go",
        ".rs": "Rust",
    }

    def execute(self, payload: dict[str, Any], context: ToolContext | None = None) -> ToolResult:
        root = Path(payload.get("path") or (context.workspace_root if context else Path.cwd())).resolve()
        if not root.exists() or not root.is_dir():
            return ToolResult(ok=False, error=f"Path is not a directory: {root}")

        suffix_counts: Counter[str] = Counter()
        file_count = 0
        for item in root.rglob("*"):
            if item.is_file() and ".git" not in item.parts and "node_modules" not in item.parts:
                file_count += 1
                suffix_counts[item.suffix] += 1

        tech_stack = sorted({self.STACK_HINTS[suffix] for suffix in suffix_counts if suffix in self.STACK_HINTS})
        return ToolResult(
            ok=True,
            data={
                "file_count": file_count,
                "top_extensions": suffix_counts.most_common(8),
                "tech_stack": tech_stack,
            },
        )
