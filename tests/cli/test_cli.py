from pathlib import Path

from typer.testing import CliRunner

from codeverse.config.settings import Settings
from codeverse.providers.base import StubProvider
from codeverse.providers.registry import ProviderRegistry
from codeverse.cli.app import app
from codeverse.cli.commands import chat as chat_command
from codeverse.agent.runtime import AgentRuntime


runner = CliRunner()


class EditingProvider(StubProvider):
    def __init__(self, updated_content: str) -> None:
        super().__init__("fake")
        self.updated_content = updated_content

    def generate(self, messages: list[dict[str, str]], model: str, temperature: float = 0.2, stream: bool = False) -> str:
        del messages, model, temperature, stream
        return self.updated_content


class TranscriptProvider(StubProvider):
    def __init__(self) -> None:
        super().__init__("fake")

    def generate(self, messages: list[dict[str, str]], model: str, temperature: float = 0.2, stream: bool = False) -> str:
        del model, temperature, stream
        return f"turns={len(messages)} last={messages[-1]['content']}"


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Codeverse CLI" in result.stdout


def test_config_show() -> None:
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert '"app_name": "codeverse"' in result.stdout


def test_config_providers() -> None:
    result = runner.invoke(app, ["config", "providers"])
    assert result.exit_code == 0
    assert '"provider": "openrouter"' in result.stdout


def test_mcp_lifecycle() -> None:
    add_result = runner.invoke(app, ["mcp", "add", "demo", "uvx"])
    assert add_result.exit_code == 0
    list_result = runner.invoke(app, ["mcp", "list"])
    assert list_result.exit_code == 0
    assert '"name": "demo"' in list_result.stdout
    inspect_result = runner.invoke(app, ["mcp", "inspect", "demo"])
    assert inspect_result.exit_code == 0
    assert '"command": "uvx"' in inspect_result.stdout
    remove_result = runner.invoke(app, ["mcp", "remove", "demo"])
    assert remove_result.exit_code == 0


def test_explain_command() -> None:
    result = runner.invoke(app, ["explain", "."])
    assert result.exit_code == 0
    assert '"summary"' in result.stdout


def test_debug_command() -> None:
    result = runner.invoke(app, ["debug", "Traceback: boom"])
    assert result.exit_code == 0
    assert '"debug_steps"' in result.stdout


def test_review_command() -> None:
    result = runner.invoke(app, ["review", "."])
    assert result.exit_code == 0
    assert '"findings": []' in result.stdout


def test_report_architecture_command() -> None:
    result = runner.invoke(app, ["report", "architecture", "."])
    assert result.exit_code == 0
    assert '"architecture"' in result.stdout


def test_chat_prompts_for_edit_approval(monkeypatch, tmp_path: Path) -> None:
    target = tmp_path / "sample.txt"
    target.write_text("hello\n", encoding="utf-8")
    settings = Settings(workspace_root=tmp_path, default_provider="fake")
    registry = ProviderRegistry()
    registry.register(EditingProvider("goodbye\n"))
    runtime = AgentRuntime(providers=registry, settings=settings)
    monkeypatch.setattr(chat_command.AgentRuntime, "default", classmethod(lambda cls: runtime))

    result = runner.invoke(app, ["chat", "update sample.txt to say goodbye"], input="accept\n")

    assert result.exit_code == 0
    assert '"decision": "accepted"' in result.stdout
    assert '"changes_done": [' in result.stdout
    assert target.read_text(encoding="utf-8") == "goodbye\n"


def test_chat_interactive_keeps_session_history(monkeypatch, tmp_path: Path) -> None:
    settings = Settings(workspace_root=tmp_path, default_provider="fake")
    registry = ProviderRegistry()
    registry.register(TranscriptProvider())
    runtime = AgentRuntime(providers=registry, settings=settings)
    monkeypatch.setattr(chat_command.AgentRuntime, "default", classmethod(lambda cls: runtime))

    result = runner.invoke(app, ["chat"], input="hello\nwhat next\n/exit\n")

    assert result.exit_code == 0
    assert "turns=1 last=hello" in result.stdout
    assert "turns=3 last=what next" in result.stdout


def test_chat_interactive_reset_clears_session_history(monkeypatch, tmp_path: Path) -> None:
    settings = Settings(workspace_root=tmp_path, default_provider="fake")
    registry = ProviderRegistry()
    registry.register(TranscriptProvider())
    runtime = AgentRuntime(providers=registry, settings=settings)
    monkeypatch.setattr(chat_command.AgentRuntime, "default", classmethod(lambda cls: runtime))

    result = runner.invoke(app, ["chat"], input="hello\n/reset\nwhat next\n/exit\n")

    assert result.exit_code == 0
    assert "Session reset." in result.stdout
    assert result.stdout.count("turns=1") == 2
