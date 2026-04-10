from pathlib import Path

import pytest

from codeverse.mcp.client import MCPClient
from codeverse.mcp.registry import MCPRegistry


def test_mcp_registry_lifecycle(tmp_path: Path) -> None:
    registry = MCPRegistry(tmp_path / "servers.json")
    server = registry.add_stdio_server(name="demo", command="uvx", trusted=True)
    assert server.name == "demo"
    assert registry.get_server("demo").command == "uvx"
    registry.remove_server("demo")
    assert registry.list_servers() == []


def test_duplicate_server_rejected(tmp_path: Path) -> None:
    registry = MCPRegistry(tmp_path / "servers.json")
    registry.add_stdio_server(name="demo", command="uvx")
    with pytest.raises(ValueError):
        registry.add_stdio_server(name="demo", command="uvx")


def test_client_inspect(tmp_path: Path) -> None:
    registry = MCPRegistry(tmp_path / "servers.json")
    registry.add_stdio_server(name="demo", command="uvx")
    client = MCPClient(registry)
    details = client.inspect_server("demo")
    assert details["name"] == "demo"
    assert details["tools"] == []
