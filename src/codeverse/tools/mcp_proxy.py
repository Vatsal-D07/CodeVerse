from codeverse.mcp.client import MCPClient
from codeverse.tools.base import ToolContext, ToolResult


class MCPProxyTool:
    name = "mcp_proxy"

    def __init__(self, client: MCPClient) -> None:
        self.client = client

    def execute(self, payload: dict[str, str], context: ToolContext | None = None) -> ToolResult:
        del context
        server = payload.get("server")
        if not server:
            return ToolResult(ok=False, error="Missing server")
        return ToolResult(ok=True, data={"server": server, "capabilities": self.client.inspect_server(server)})
