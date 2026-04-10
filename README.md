# CodeVerse

Codeverse is a CLI-first AI coding agent foundation with provider abstraction, MCP integration hooks, safe native tools, and a testable runtime skeleton.

## Requirements

- Python 3.10+

## Setup

Create a virtual environment and install the project in editable mode:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run The CLI

From the repository root:

```bash
source .venv/bin/activate
python -m codeverse.cli.main --help
```

If the console script is available in your environment, this also works:

```bash
codeverse --help
```

## Example Commands

```bash
python -m codeverse.cli.main chat "Hello"
python -m codeverse.cli.main analyze .
python -m codeverse.cli.main explain .
python -m codeverse.cli.main debug "Traceback: boom"
python -m codeverse.cli.main plan "add authentication"
python -m codeverse.cli.main review .
python -m codeverse.cli.main report architecture .
python -m codeverse.cli.main config show
python -m codeverse.cli.main mcp list
```

## Run Tests

```bash
.venv/bin/pytest
```
