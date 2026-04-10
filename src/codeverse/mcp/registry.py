import json
from pathlib import Path

from codeverse.config.settings import get_settings
from codeverse.mcp.models import MCPServerConfig


class MCPRegistry:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    @classmethod
    def default(cls) -> "MCPRegistry":
        return cls(get_settings().mcp.registry_path)

    def list_servers(self) -> list[MCPServerConfig]:
        return [MCPServerConfig.model_validate(item) for item in self._read()]

    def get_server(self, name: str) -> MCPServerConfig:
        for server in self.list_servers():
            if server.name == name:
                return server
        raise KeyError(f"Unknown MCP server '{name}'")

    def add_stdio_server(self, name: str, command: str, args: list[str] | None = None, trusted: bool = False) -> MCPServerConfig:
        servers = self.list_servers()
        if any(server.name == name for server in servers):
            raise ValueError(f"MCP server '{name}' is already registered")
        server = MCPServerConfig(name=name, command=command, args=args or [], trusted=trusted)
        servers.append(server)
        self._write([item.model_dump(mode="json") for item in servers])
        return server

    def remove_server(self, name: str) -> None:
        servers = self.list_servers()
        remaining = [server for server in servers if server.name != name]
        if len(remaining) == len(servers):
            raise KeyError(f"Unknown MCP server '{name}'")
        self._write([item.model_dump(mode="json") for item in remaining])

    def _read(self) -> list[dict]:
        raw = self.path.read_text(encoding="utf-8")
        return json.loads(raw)

    def _write(self, data: list[dict]) -> None:
        self.path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
