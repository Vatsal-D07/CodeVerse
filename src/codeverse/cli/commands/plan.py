from rich.console import Console

from codeverse.agent.planner import Planner

console = Console()


def plan(task: str) -> None:
    planner = Planner()
    console.print_json(data={"task": task, "steps": planner.build_plan(task)})
