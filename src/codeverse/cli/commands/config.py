from rich.console import Console
from typer import Typer

from codeverse.config.settings import get_settings
from codeverse.providers.registry import ProviderRegistry

app = Typer(help="Manage Codeverse configuration")
console = Console()


@app.command("show")
def show() -> None:
    settings = get_settings()
    console.print_json(data=settings.model_dump(mode="json"))


@app.command("providers")
def providers() -> None:
    registry = ProviderRegistry.default(get_settings())
    console.print_json(data={"providers": registry.health()})
