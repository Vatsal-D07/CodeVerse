from typer import Typer

from codeverse.cli.commands import analyze, chat, config, debug, explain, mcp, plan, report, review


def build_app() -> Typer:
    app = Typer(help="Codeverse CLI")
    app.add_typer(config.app, name="config")
    app.add_typer(mcp.app, name="mcp")
    app.add_typer(report.app, name="report")
    app.command()(chat.chat)
    app.command()(analyze.analyze)
    app.command()(explain.explain)
    app.command()(debug.debug)
    app.command()(plan.plan)
    app.command()(review.review)
    return app


app = build_app()
