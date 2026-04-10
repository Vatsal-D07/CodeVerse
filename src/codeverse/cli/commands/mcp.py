from rich.console import Console
from typer import Argument, Typer

from codeverse.mcp.registry import MCPRegistry

app = Typer(help="Manage MCP servers")
console = Console()


@app.command("list")
def list_servers() -> None:
    registry = MCPRegistry.default()
    servers = [server.model_dump(mode="json") for server in registry.list_servers()]
    console.print_json(data={"servers": servers})


@app.command("add")
def add_server(name: str = Argument(...), command: str = Argument(...)) -> None:
    registry = MCPRegistry.default()
    server = registry.add_stdio_server(name=name, command=command)
    console.print_json(data=server.model_dump(mode="json"))


@app.command("remove")
def remove_server(name: str = Argument(...)) -> None:
    registry = MCPRegistry.default()
    registry.remove_server(name)
    console.print_json(data={"removed": name})


@app.command("inspect")
def inspect_server(name: str = Argument(...)) -> None:
    registry = MCPRegistry.default()
    server = registry.get_server(name)
    console.print_json(data=server.model_dump(mode="json"))
