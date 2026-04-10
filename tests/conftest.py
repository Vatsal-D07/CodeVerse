from pathlib import Path

import pytest

from codeverse.config.settings import reset_settings_cache


@pytest.fixture(autouse=True)
def isolated_home(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("CODEVERSE_MCP__REGISTRY_PATH", str(tmp_path / ".codeverse" / "mcp_servers.json"))
    reset_settings_cache()
