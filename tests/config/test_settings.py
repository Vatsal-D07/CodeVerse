from pathlib import Path

from codeverse.config.settings import Settings


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.app_name == "codeverse"
    assert settings.default_provider == "openrouter"
    assert settings.safety.require_edit_approval is True


def test_settings_env_override(monkeypatch) -> None:
    monkeypatch.setenv("CODEVERSE_DEFAULT_PROVIDER", "gemini")
    monkeypatch.setenv("CODEVERSE_MCP__REGISTRY_PATH", "/tmp/codeverse-mcp.json")
    monkeypatch.setenv("CODEVERSE_PROVIDERS__OPENROUTER__API_KEY", "token")
    settings = Settings()
    assert settings.default_provider == "gemini"
    assert settings.mcp.registry_path == Path("/tmp/codeverse-mcp.json")
    assert settings.providers.openrouter.api_key == "token"
