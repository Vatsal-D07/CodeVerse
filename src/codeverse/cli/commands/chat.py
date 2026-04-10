from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from typer import Argument, Option

from codeverse.agent.runtime import AgentRuntime
from codeverse.output.renderer import render_summary

console = Console()


def chat(prompt: str | None = Argument(None), interactive: bool = Option(False, "--interactive", "-i")) -> None:
    runtime = AgentRuntime.default()
    if interactive or prompt is None:
        _interactive_chat(runtime)
        return
    _handle_prompt(runtime, prompt)


def _interactive_chat(runtime: AgentRuntime) -> None:
    history: list[dict[str, str]] = []
    console.print("Interactive chat started. Type `/exit` to quit or `/reset` to clear the session.")
    while True:
        prompt = Prompt.ask("codeverse")
        command = prompt.strip().lower()
        if command in {"exit", "quit", "/exit", "/quit"}:
            break
        if command == "/reset":
            history.clear()
            console.print("Session reset.")
            continue
        if not prompt.strip():
            continue
        _handle_prompt(runtime, prompt, history)


def _handle_prompt(runtime: AgentRuntime, prompt: str, history: list[dict[str, str]] | None = None) -> None:
    result = runtime.respond(prompt, history=history)
    console.print(render_summary(result.output))
    if history is not None:
        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": result.output})
    if not result.proposed_changes:
        return
    for change in result.proposed_changes:
        console.print(Panel(change.diff or change.summary, title=f"Proposed change: {change.path}"))

    decision = "accept"
    if result.approval_required:
        decision = Prompt.ask("Apply these changes?", choices=["accept", "reject"], default="reject")
    if decision == "accept":
        applied_paths = runtime.apply_changes(result)
        console.print_json(data={"decision": "accepted", "changes_done": applied_paths})
        return
    console.print_json(data={"decision": "rejected", "changes_done": []})
