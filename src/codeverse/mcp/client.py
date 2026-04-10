from codeverse.mcp.registry import MCPRegistry


class MCPClient:
    def __init__(self, registry: MCPRegistry) -> None:
        self.registry = registry

    def inspect_server(self, name: str) -> dict[str, object]:
        server = self.registry.get_server(name)
        return {
            "name": server.name,
            "transport": server.transport,
            "command": server.command,
            "args": server.args,
            "trusted": server.trusted,
            "tools": [],
            "resources": [],
            "prompts": [],
        }
