from pathlib import Path

import pytest

from codeverse.config.settings import reset_settings_cache
from codeverse.tools.base import ToolRegistry
from codeverse.tools.code_analysis import CodeAnalysisTool
from codeverse.tools.filesystem import FilesystemTool
from codeverse.tools.git import GitTool
from codeverse.tools.search import SearchTool
from codeverse.tools.shell import ShellTool


def test_filesystem_blocks_outside_workspace(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.txt"
    outside.write_text("x", encoding="utf-8")
    tool = FilesystemTool()
    result = tool.execute({"action": "read", "path": str(outside)}, context=type("Ctx", (), {"workspace_root": tmp_path, "read_only": True})())
    assert result.ok is False


def test_tool_registry_duplicate_rejected() -> None:
    registry = ToolRegistry()
    tool = FilesystemTool()
    registry.register(tool)
    with pytest.raises(ValueError):
        registry.register(tool)


def test_filesystem_list_and_read(tmp_path: Path) -> None:
    file_path = tmp_path / "hello.txt"
    file_path.write_text("hello", encoding="utf-8")
    tool = FilesystemTool()
    list_result = tool.execute({"action": "list", "path": str(tmp_path)})
    assert list_result.ok is True
    assert "hello.txt" in list_result.data["entries"]
    read_result = tool.execute({"action": "read", "path": str(file_path)})
    assert read_result.ok is True
    assert read_result.data["content"] == "hello"


def test_search_tool_matches_files(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("print('x')", encoding="utf-8")
    (tmp_path / "b.txt").write_text("x", encoding="utf-8")
    tool = SearchTool()
    result = tool.execute({"path": str(tmp_path), "pattern": "*.py"})
    assert result.ok is True
    assert result.data["matches"] == ["a.py"]


def test_code_analysis_detects_stack(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text("print('x')", encoding="utf-8")
    (tmp_path / "app.ts").write_text("export {}", encoding="utf-8")
    result = CodeAnalysisTool().execute({"path": str(tmp_path)})
    assert result.ok is True
    assert "Python" in result.data["tech_stack"]
    assert "TypeScript" in result.data["tech_stack"]


def test_git_tool_non_repo(tmp_path: Path) -> None:
    result = GitTool().execute({"action": "status", "path": str(tmp_path)})
    assert result.ok is False


def test_shell_tool_blocks_when_disabled(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CODEVERSE_SAFETY__ALLOW_SHELL", "false")
    reset_settings_cache()
    result = ShellTool().execute({"command": ["git", "status"]})
    assert result.ok is False


def test_shell_tool_runs_allowed_command(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CODEVERSE_SAFETY__ALLOW_SHELL", "true")
    monkeypatch.setenv("CODEVERSE_SAFETY__ALLOWED_SHELL_COMMANDS", '["python3"]')
    reset_settings_cache()
    result = ShellTool().execute({"command": ["python3", "-c", "print('ok')"], "cwd": str(tmp_path)})
    assert result.ok is True
    assert result.data["stdout"].strip() == "ok"
