from __future__ import annotations

import difflib
import re
from pathlib import Path

from codeverse.agent.parser import IntentParser
from codeverse.agent.planner import Planner
from codeverse.agent.state import AgentResult, ProposedChange
from codeverse.config.settings import Settings, get_settings
from codeverse.providers.registry import ProviderRegistry


class AgentRuntime:
    def __init__(self, providers: ProviderRegistry | None = None, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.providers = providers or ProviderRegistry.default(self.settings)
        self.parser = IntentParser()
        self.planner = Planner()

    @classmethod
    def default(cls) -> "AgentRuntime":
        return cls()

    def respond(self, prompt: str, history: list[dict[str, str]] | None = None) -> AgentResult:
        parsed = self.parser.parse(prompt)
        steps = self.planner.build_plan(prompt)
        if parsed["action"] == "edit":
            return self._build_edit_proposal(prompt=prompt, steps=steps)
        provider = self.providers.get(self.settings.default_provider)
        messages = list(history or []) + [{"role": "user", "content": parsed["prompt"]}]
        output = provider.generate(
            messages=messages,
            model=self.settings.default_model,
        )
        return AgentResult(output=output, steps=steps)

    def apply_changes(self, result: AgentResult) -> list[str]:
        applied_paths: list[str] = []
        workspace_root = self.settings.workspace_root.resolve()
        for change in result.proposed_changes:
            path = (workspace_root / change.path).resolve()
            path.relative_to(workspace_root)
            path.write_text(change.new_content, encoding="utf-8")
            applied_paths.append(change.path)
        return applied_paths

    def _build_edit_proposal(self, prompt: str, steps: list[str]) -> AgentResult:
        target_path = self._extract_target_path(prompt)
        if target_path is None:
            return AgentResult(
                output="I need a target file path before I can propose a change. Mention a file like `README.md` or `src/codeverse/cli/app.py`.",
                steps=steps,
            )

        original_content = target_path.read_text(encoding="utf-8")
        provider = self.providers.get(self.settings.default_provider)
        generated_content = provider.generate(
            messages=[
                {
                    "role": "system",
                    "content": "You edit one existing file. Return only the complete updated file contents with no markdown fences or commentary.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Target file: {target_path.relative_to(self.settings.workspace_root.resolve())}\n"
                        f"Instruction: {prompt}\n"
                        "Current file contents:\n"
                        f"{original_content}"
                    ),
                },
            ],
            model=self.settings.default_model,
        )
        updated_content = self._normalize_generated_content(generated_content)
        if not updated_content or updated_content == original_content:
            return AgentResult(output="No file changes were proposed.", steps=steps)

        relative_path = str(target_path.relative_to(self.settings.workspace_root.resolve()))
        diff = self._build_diff(relative_path, original_content, updated_content)
        change = ProposedChange(
            path=relative_path,
            summary=f"Update {relative_path} based on the requested instruction.",
            diff=diff,
            new_content=updated_content,
        )
        return AgentResult(
            output=f"Proposed 1 change for {relative_path}. Review it and choose accept or reject.",
            steps=steps,
            proposed_changes=[change],
            approval_required=self.settings.safety.require_edit_approval,
        )

    def _extract_target_path(self, prompt: str) -> Path | None:
        workspace_root = self.settings.workspace_root.resolve()
        tokens = re.findall(r"[A-Za-z0-9_./-]+", prompt)
        for token in tokens:
            if "." not in token and "/" not in token:
                continue
            candidate = token.strip("'\"`.,:;()[]{}")
            if not candidate:
                continue
            path = Path(candidate)
            resolved = path.resolve() if path.is_absolute() else (workspace_root / path).resolve()
            if resolved.is_file():
                try:
                    resolved.relative_to(workspace_root)
                except ValueError:
                    continue
                return resolved
        return None

    @staticmethod
    def _normalize_generated_content(content: str) -> str:
        if content.startswith("```"):
            lines = content.splitlines(keepends=True)
            if len(lines) >= 3 and lines[-1].strip() == "```":
                body = lines[1:-1]
                if body:
                    first_line = body[0].strip()
                    if first_line.isidentifier() or all(ch.isalnum() or ch in {"-", ".", "+", "_"} for ch in first_line):
                        body = body[1:]
                return "".join(body)
        return content

    @staticmethod
    def _build_diff(path: str, before: str, after: str) -> str:
        lines = difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile=f"a/{path}",
            tofile=f"b/{path}",
            lineterm="",
        )
        return "\n".join(lines)
