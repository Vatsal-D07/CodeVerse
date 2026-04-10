from rich.console import Console

from codeverse.agent.planner import Planner

console = Console()


def debug(error_input: str) -> None:
    planner = Planner()
    console.print_json(
        data={
            "error": error_input,
            "debug_steps": planner.build_plan(f"debug {error_input}"),
        }
    )
