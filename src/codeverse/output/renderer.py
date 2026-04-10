from rich.panel import Panel


def render_summary(text: str) -> Panel:
    return Panel.fit(text, title="Codeverse")
