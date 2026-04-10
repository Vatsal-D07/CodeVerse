from pathlib import Path

from codeverse.config.settings import Settings
from codeverse.providers.base import StubProvider
from codeverse.providers.registry import ProviderRegistry
from codeverse.agent.planner import Planner
from codeverse.agent.runtime import AgentRuntime


class EditingProvider(StubProvider):
    def __init__(self, updated_content: str) -> None:
        super().__init__("fake")
        self.updated_content = updated_content

    def generate(self, messages: list[dict[str, str]], model: str, temperature: float = 0.2, stream: bool = False) -> str:
        del messages, model, temperature, stream
        return self.updated_content


class RecordingProvider(StubProvider):
    def __init__(self) -> None:
        super().__init__("fake")
        self.messages_seen: list[list[dict[str, str]]] = []

    def generate(self, messages: list[dict[str, str]], model: str, temperature: float = 0.2, stream: bool = False) -> str:
        del model, temperature, stream
        self.messages_seen.append(messages)
        return f"seen {len(messages)} messages"


def test_planner_builds_steps() -> None:
    planner = Planner()
    steps = planner.build_plan("Analyze repo")
    assert len(steps) == 4
    assert steps[0].startswith("Understand task")


def test_runtime_responds() -> None:
    runtime = AgentRuntime.default()
    result = runtime.respond("hello")
    assert result.output.startswith("[openrouter:")
    assert len(result.steps) == 4


def test_runtime_proposes_edit_for_target_file(tmp_path: Path) -> None:
    target = tmp_path / "sample.txt"
    target.write_text("hello\n", encoding="utf-8")
    settings = Settings(workspace_root=tmp_path, default_provider="fake")
    registry = ProviderRegistry()
    registry.register(EditingProvider("goodbye\n"))
    runtime = AgentRuntime(providers=registry, settings=settings)

    result = runtime.respond("update sample.txt to say goodbye")

    assert result.approval_required is True
    assert len(result.proposed_changes) == 1
    assert result.proposed_changes[0].path == "sample.txt"
    assert "goodbye" in result.proposed_changes[0].diff
    assert target.read_text(encoding="utf-8") == "hello\n"


def test_runtime_applies_approved_changes(tmp_path: Path) -> None:
    target = tmp_path / "sample.txt"
    target.write_text("hello\n", encoding="utf-8")
    settings = Settings(workspace_root=tmp_path, default_provider="fake")
    registry = ProviderRegistry()
    registry.register(EditingProvider("goodbye\n"))
    runtime = AgentRuntime(providers=registry, settings=settings)

    result = runtime.respond("update sample.txt to say goodbye")
    applied_paths = runtime.apply_changes(result)

    assert applied_paths == ["sample.txt"]
    assert target.read_text(encoding="utf-8") == "goodbye\n"


def test_runtime_includes_chat_history_in_provider_messages(tmp_path: Path) -> None:
    settings = Settings(workspace_root=tmp_path, default_provider="fake")
    registry = ProviderRegistry()
    provider = RecordingProvider()
    registry.register(provider)
    runtime = AgentRuntime(providers=registry, settings=settings)

    result = runtime.respond(
        "what should I do next?",
        history=[
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "hi"},
        ],
    )

    assert result.output == "seen 3 messages"
    assert provider.messages_seen == [
        [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "hi"},
            {"role": "user", "content": "what should I do next?"},
        ]
    ]
