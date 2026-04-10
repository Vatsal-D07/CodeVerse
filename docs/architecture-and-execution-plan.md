# Codeverse Architecture And Execution Plan

## 1. Overview

Codeverse is an AI-powered terminal coding agent designed to help developers understand, analyze, debug, improve, and modify codebases from the command line.

The system should behave like a practical engineering assistant, not just a chat wrapper around an LLM. It should be able to:

- understand user intent
- inspect repositories safely
- plan and execute multi-step workflows
- call tools for files, shell, git, search, and code analysis
- connect to MCP servers for external tools and context
- generate structured reports
- optionally propose or apply code changes with user approval

The product should feel like an AI operating layer for developer workflows inside the terminal.

---

## 2. Product Goals

### Primary Goals

- Provide a strong CLI-first AI developer experience
- Analyze codebases with real repository context
- Generate useful outputs such as architecture summaries, debug plans, and code reports
- Support autonomous multi-step agent execution
- Keep actions observable, safe, and easy to approve

### Non-Goals For MVP

- Full IDE replacement
- Multi-user cloud collaboration platform
- Browser-based UI
- Complex plugin marketplace at launch
- Heavy fine-tuning or custom model training

---

## 3. User Personas

### Solo Developer

Needs quick repo understanding, debugging help, and code change suggestions.

### Team Developer

Needs architecture summaries, onboarding help, and safe command-line automation.

### Technical Lead

Needs project health analysis, scalability risks, dependency insights, and code review assistance.

### New Contributor

Needs guided repository walkthroughs, file explanations, and workflow discovery.

---

## 4. Core Use Cases

- Explain an entire repository like a senior engineer
- Analyze project architecture and dependencies
- Debug a stack trace using repository context
- Generate implementation plans for requested features
- Search and answer questions across a codebase
- Propose safe code changes with diffs
- Review code for correctness, regressions, and quality risks
- Generate onboarding docs and interview questions from a repo
- Suggest performance, security, and scalability improvements

---

## 5. CLI Product Surface

### Initial Commands

- `codeverse chat`
- `codeverse analyze <path>`
- `codeverse explain <path>`
- `codeverse report architecture <path>`
- `codeverse debug <file-or-error-input>`
- `codeverse plan "<task>"`
- `codeverse review <path-or-diff>`
- `codeverse config show`
- `codeverse config set-provider <provider>`
- `codeverse config set-model <model>`
- `codeverse mcp list`
- `codeverse mcp add <name>`
- `codeverse mcp remove <name>`

### Future Commands

- `codeverse fix "<issue>"`
- `codeverse onboard <path>`
- `codeverse scale-check <path>`
- `codeverse security-scan <path>`
- `codeverse pr-summary`
- `codeverse plugin install <name>`
- `codeverse mcp inspect <name>`

### Interactive Mode

- `codeverse`
- slash commands such as `/analyze`, `/explain`, `/debug`, `/plan`, `/review`
- session history
- streamed output
- optional approval prompts before risky actions

---

## 6. High-Level Architecture

```text
User Terminal
  -> CLI Interface
  -> Command Router
  -> Session Manager
  -> Agent Runtime
       -> Parser
       -> Planner
       -> Reasoner
       -> Memory
       -> Safety Guard
       -> Tool Orchestrator
  -> Tool Layer
       -> Filesystem Tool
       -> Search Tool
       -> Shell Tool
       -> Git Tool
       -> Code Analysis Tool
       -> Reporting Tool
  -> MCP Layer
       -> MCP Client
       -> MCP Server Registry
       -> MCP Tool Adapter
       -> MCP Resource Adapter
       -> MCP Prompt Adapter
  -> Provider Layer
       -> LLM Providers
       -> Embedding Providers
  -> RAG Layer
       -> Ingestion
       -> Chunking
       -> Vector Store
       -> Retrieval
  -> Output Layer
       -> Terminal Renderer
       -> Markdown/JSON Exporter
       -> Logs/Tracing
```

### Core Flow

```text
User Input
  -> Parse Intent
  -> Build Task Plan
  -> Execute Agent Loop
  -> Call Tools
  -> Observe Results
  -> Update Session Memory
  -> Produce Final Answer / Report / Diff
```

---

## 7. Architecture Principles

- CLI-first, fast, and observable
- Keep the agent loop explicit and debuggable
- Separate reasoning from tool execution
- Treat tools as typed capabilities
- Treat MCP-exposed capabilities as first-class tools with safety controls
- Keep model providers swappable
- Default to safe read-only behavior unless user enables edits
- Prefer small, composable modules over framework-heavy abstractions
- Optimize for practical usefulness over novelty

---

## 8. Recommended Tech Stack

### Language

- Python

### CLI

- `typer`
- `rich`

### Config

- `pydantic-settings`

### Testing

- `pytest`

### LLM Providers

- OpenRouter
- Gemini
- Hugging Face Inference API

### Embeddings

- Hugging Face sentence-transformers
- optional provider-based embeddings later

### Vector Store

- `chromadb`

### Parsing And Code Analysis

- Python: `ast`, `pathlib`
- JavaScript/TypeScript: optional tree-sitter or external parser integration later
- Search: `ripgrep`-style fast search approach where appropriate

### Logging

- Python `logging`
- optional structured JSON logs

### MCP Integration

- Python MCP SDK or protocol-compatible client implementation
- stdio transport first
- HTTP/SSE transport later if needed

### Why Python

- Best ecosystem for agent systems, embeddings, orchestration, parsing, and local tooling
- Fastest path to a practical CLI product
- Easier integration with multiple LAG and retrieval workflows

---

## 9. Repository Structure

```text
project/
├── docs/
│   └── architecture-and-execution-plan.md
├── src/
│   └── codeverse/
│       ├── cli/
│       │   ├── main.py
│       │   ├── app.py
│       │   └── commands/
│       │       ├── chat.py
│       │       ├── analyze.py
│       │       ├── explain.py
│       │       ├── debug.py
│       │       ├── report.py
│       │       ├── review.py
│       │       └── config.py
│       ├── agent/
│       │   ├── runtime.py
│       │   ├── parser.py
│       │   ├── planner.py
│       │   ├── memory.py
│       │   ├── state.py
│       │   ├── safety.py
│       │   └── prompts.py
│       ├── providers/
│       │   ├── base.py
│       │   ├── openrouter.py
│       │   ├── gemini.py
│       │   ├── huggingface.py
│       │   ├── embeddings.py
│       │   └── registry.py
│       ├── mcp/
│       │   ├── client.py
│       │   ├── registry.py
│       │   ├── adapters.py
│       │   ├── transport.py
│       │   └── models.py
│       ├── tools/
│       │   ├── base.py
│       │   ├── filesystem.py
│       │   ├── search.py
│       │   ├── shell.py
│       │   ├── git.py
│       │   ├── code_analysis.py
│       │   ├── reporting.py
│       │   ├── diff.py
│       │   └── mcp_proxy.py
│       ├── rag/
│       │   ├── ingest.py
│       │   ├── chunking.py
│       │   ├── retriever.py
│       │   ├── index.py
│       │   └── context_builder.py
│       ├── output/
│       │   ├── renderer.py
│       │   ├── markdown.py
│       │   ├── json_output.py
│       │   └── streaming.py
│       ├── config/
│       │   ├── settings.py
│       │   └── models.py
│       ├── telemetry/
│       │   ├── logging.py
│       │   └── tracing.py
│       └── utils/
│           ├── paths.py
│           ├── text.py
│           └── tokens.py
├── tests/
│   ├── cli/
│   ├── agent/
│   ├── providers/
│   ├── tools/
│   └── rag/
├── pyproject.toml
├── README.md
└── .env.example
```

---

## 10. Core Modules

## 10.1 CLI Layer

Responsible for user interaction.

### Responsibilities

- parse CLI commands and arguments
- dispatch workflows
- support interactive chat mode
- render streaming output
- show progress, warnings, and approvals

### Implementation Notes

- Use `typer` for command definition and subcommands
- Use `rich` for tables, panels, progress bars, and colored status output
- Keep CLI handlers thin and delegate business logic to service modules

## 10.2 Command Parser

Responsible for converting free-form user input into structured intent.

### Responsibilities

- classify command intent
- extract targets such as file paths or repo scope
- normalize prompts for the agent runtime

### Strategy

- Start with rule-based parsing for explicit CLI commands
- Add LLM-based intent parsing later for interactive mode

### Example

```json
{
  "action": "analyze",
  "target": ".",
  "mode": "architecture"
}
```

## 10.3 Agent Runtime

The central execution engine that coordinates planning, reasoning, tool calls, and output.

### Responsibilities

- receive structured tasks from CLI or interactive mode
- generate a step-by-step plan
- select and run tools
- observe results and continue until task completion
- maintain memory and execution state

### Submodules

- `parser.py`: intent normalization
- `planner.py`: task decomposition
- `runtime.py`: think-act-observe loop
- `memory.py`: session context and retrieval integration
- `state.py`: task state, tool outputs, execution metadata
- `safety.py`: permission checks and guarded actions
- `prompts.py`: centralized system and task prompt templates

## 10.4 Tool Layer

The tool layer exposes real capabilities to the agent.

Tools can be native Codeverse tools or MCP-backed tools surfaced through the same execution contract.

### Filesystem Tool

- list directories
- read files
- write files only when allowed
- create patches or diffs

### Search Tool

- search filenames
- search file contents
- support scoped repo search

### Shell Tool

- run safe shell commands
- capture stdout and stderr
- support timeouts and allowlists

### Git Tool

- show status
- diff working tree
- inspect commit history
- support branch-aware analysis

### Code Analysis Tool

- detect tech stack
- parse source files
- compute basic metrics
- identify complexity or structural risks

### Reporting Tool

- generate architecture reports
- produce markdown summaries
- create implementation plans and issue breakdowns

### MCP Tool Bridge

- discover tools exposed by MCP servers
- normalize external tool schemas into internal tool contracts
- route tool invocations through MCP transports
- capture structured tool results for the agent runtime

## 10.5 MCP Layer

The MCP layer allows Codeverse to connect to external tool servers using the Model Context Protocol.

### Responsibilities

- manage MCP server definitions
- establish stdio or network transports
- discover tools, prompts, and resources from connected servers
- adapt MCP capabilities into the agent runtime
- enforce safety policy on external tool execution

### Initial Scope

- support stdio-based MCP servers first
- load server definitions from local config
- expose MCP tools through the existing tool orchestrator
- support resource reads and prompt templates where useful

### Design Rules

- MCP tools should look identical to native tools from the planner's perspective
- all MCP actions must pass through the same approval and logging pipeline
- server failures should degrade gracefully without breaking the whole session
- connected server metadata should be inspectable from the CLI

## 10.6 Provider Layer

Abstracts all LLM and embedding backends.

### Provider Requirements

- unified generate interface
- optional streaming support
- retry and timeout handling
- model metadata
- fallback support

### Initial Providers

- OpenRouter
- Gemini
- Hugging Face Inference API

### Base Interface

```python
class BaseLLMProvider:
    def generate(self, messages, model, temperature=0.2, stream=False):
        ...

    def health_check(self):
        ...
```

### Embedding Interface

```python
class BaseEmbeddingProvider:
    def embed(self, texts, model=None):
        ...
```

## 10.7 RAG Layer

Used for repository understanding at scale.

### Responsibilities

- scan project files
- chunk files intelligently
- generate embeddings
- store vectors
- retrieve relevant context for prompts

### Initial Scope

- local project indexing only
- ignore generated directories such as `node_modules`, `.git`, `dist`, `build`, `.venv`
- prioritize source files, configs, docs, and tests

### Retrieval Flow

```text
User query
  -> retrieve top relevant chunks
  -> merge with session context
  -> build final prompt
  -> ask model
```

## 10.8 Output Layer

Responsible for presenting results clearly.

### Output Types

- terminal summary
- streamed thought/action updates
- markdown report
- JSON output for automation
- diff preview for file edits

### UX Goals

- readable in terminal
- concise by default
- expandable for detailed mode
- consistent status markers for success, warning, and error states

---

## 11. Agent Execution Model

The runtime should follow a transparent think-act-observe loop.

### Loop

```text
1. Receive task
2. Build plan
3. Select next action
4. Execute tool
5. Observe tool result
6. Update memory and state
7. Decide whether to continue or finish
8. Render final output
```

### Pseudocode

```python
while not state.done:
    thought = reason_about_next_step(state)
    action = choose_tool(thought, state)
    result = run_tool(action)
    state.record(action, result)
    update_memory(state, result)
```

### Runtime Requirements

- max iteration limit to prevent runaway loops
- per-tool timeout support
- structured action/result logging
- fallback behavior on provider failures
- graceful interruption and resume support later

---

## 12. Memory Strategy

### Short-Term Memory

Stores the current session context.

Includes:

- current user goal
- intermediate plan
- recent tool outputs
- selected files and context snippets

### Long-Term Memory

Stores reusable repository knowledge.

Includes:

- embedded code chunks
- previous reports
- architectural summaries
- common project patterns

### Design Principles

- keep session state lightweight and inspectable
- keep retrieval deterministic where possible
- never hide critical context decisions from the user in safety-sensitive flows

---

## 13. LLM Provider Strategy

The system should support free or low-cost providers first, with the ability to add premium providers later.

### Initial Provider Priority

1. OpenRouter
2. Gemini
3. Hugging Face Inference API

### Selection Rules

- choose provider based on config and availability
- allow per-command override later
- support model fallback on quota or failure
- display provider and model used in verbose mode

### Free-Tier Oriented Defaults

- use smaller, cheaper models for planning and classification
- reserve larger models for repo summarization and final report generation
- support local embeddings to reduce cost

---

## 14. Safety And Permission Model

Safety is required because the system can inspect, execute, and eventually edit project files.

### Default Safety Policy

- read-only by default
- shell execution restricted or explicitly approved
- file edits require confirmation in early versions
- networked or destructive actions blocked unless enabled
- MCP servers must be explicitly configured and trusted before use

### Safety Controls

- command allowlist and denylist for shell actions
- path restrictions to project root
- iteration and timeout caps
- diff preview before file writes
- clear logs of every action taken
- per-server MCP trust policy and capability visibility
- transport-level timeouts and server isolation rules

### Risky Actions

Examples:

- deleting files
- overwriting many files
- running install scripts
- executing arbitrary shell commands
- writing outside workspace
- invoking high-risk MCP tools from external servers

These should require explicit approval.

---

## 15. Observability And Debuggability

The product should make its behavior understandable.

### Logging Requirements

- command start and end
- provider selection
- tool calls and results summary
- execution time per step
- failures and retries

### Optional Tracing

- session trace files
- JSON logs for machine analysis
- replayable task history for debugging later

### Why This Matters

- easier to debug agent mistakes
- easier to improve prompts and tools
- better trust for developers using the system

---

## 16. Reporting Outputs

Codeverse should generate structured, useful outputs rather than vague assistant text.

### Report Types

- architecture overview
- dependency summary
- bug investigation report
- implementation plan
- code review findings
- scalability assessment
- onboarding guide

### Report Characteristics

- markdown-first
- include file references when possible
- include risks, assumptions, and recommended next steps
- distinguish fact from model inference

---

## 17. MVP Scope

The MVP should focus on a narrow but valuable set of capabilities.

### MVP Features

- CLI setup with `typer` and `rich`
- provider abstraction with OpenRouter, Gemini, and Hugging Face
- filesystem read and search tools
- MCP client integration with local server registry
- repository analysis command
- architecture report generation
- interactive chat with repo context
- basic agent loop for planning and tool execution
- config management for providers and models
- safe read-only default behavior

### Explicitly Deferred

- plugin marketplace
- autonomous full-repo edits
- advanced multi-agent orchestration
- remote team memory sync
- web dashboard

---

## 18. Execution Plan

## Phase 0: Specification

### Objectives

- finalize product architecture
- define module contracts
- define safety boundaries

### Deliverables

- `docs/architecture-and-execution-plan.md`
- initial README outline

## Phase 1: Project Foundation

### Objectives

- initialize Python package
- set up CLI entrypoint
- add config loading
- add renderer and logging

### Deliverables

- `pyproject.toml`
- base package structure
- working `codeverse --help`

## Phase 2: Provider Abstraction

### Objectives

- implement base provider interfaces
- add OpenRouter, Gemini, and Hugging Face integrations
- support streaming and retries

### Deliverables

- provider registry
- health checks
- basic chat completion command

## Phase 3: Tooling Layer

### Objectives

- add filesystem, search, shell, and git tools
- standardize tool request/response objects
- add timeouts and guarded execution
- add MCP tool adaptation for external capabilities

### Deliverables

- reusable tool modules
- repo inspection capability
- MCP-backed tools available through a common tool interface

## Phase 4: Agent Runtime

### Objectives

- implement parser, planner, runtime loop, and memory
- support multi-step execution
- show intermediate status in terminal
- allow planner to select native or MCP-backed tools

### Deliverables

- task planning flow
- tool-using agent loop

## Phase 5: RAG And Repository Understanding

### Objectives

- add file ingestion and chunking
- generate embeddings
- support retrieval over repository context

### Deliverables

- code-aware retrieval pipeline
- repo Q&A mode

## Phase 6: Reporting And Review Workflows

### Objectives

- build architecture report generator
- build debug report generator
- build code review output mode

### Deliverables

- high-value markdown reports

## Phase 7: Safe Edit Workflows

### Objectives

- add diff generation
- allow controlled file modification
- run validations after edits

### Deliverables

- patch proposal flow
- approval-based edit workflow

## Phase 8: Advanced UX

### Objectives

- add interactive shell-like experience
- add session resume and slash commands
- add provider fallback and usage metrics

### Deliverables

- polished daily-driver experience

---

## 19. Testing Strategy

### Unit Tests

- parser behavior
- planner output shape
- provider adapters
- tool contracts
- config loading

### Integration Tests

- CLI command execution
- provider request mocking
- repository analysis flow
- retrieval pipeline behavior

### End-To-End Tests

- analyze sample repo
- explain file/module
- generate architecture report
- debug an error log with repo context

### Safety Tests

- blocked shell command behavior
- write restriction checks
- path traversal prevention
- timeout handling

---

## 20. Developer Experience Features To Add

These features will significantly improve usability and trust.

### High-Impact DX Features

- diff preview before any code change
- explanation of why a patch is proposed
- repo-aware chat with source citations
- provider fallback when an API fails
- command progress and step rendering
- token and cost visibility in verbose mode
- session resume from previous history
- auto-run tests and lint after edits
- markdown and JSON export modes
- deterministic read-only mode for analysis tasks
- one-command MCP server discovery and health diagnostics

### Advanced Features

- multi-agent roles such as analyzer, debugger, reviewer, and refactorer
- architecture graph generation
- security smell detection
- performance bottleneck discovery
- scalability analysis mode
- new contributor onboarding mode
- issue-to-fix workflow from stack traces or bug reports
- interview question generation from repository code
- plugin system for custom tools
- MCP marketplace-style server packs later
- local model support later for hybrid offline usage

### Differentiating Features

- `codeverse architecture`: explain the repo like a senior engineer
- `codeverse onboard`: create a repo onboarding guide for a new developer
- `codeverse scale-check`: identify coupling and scaling risks
- `codeverse issue-from-stacktrace`: map runtime errors to likely root causes and files
- `codeverse review --senior`: focus on correctness, regressions, and engineering risks instead of generic feedback

---

## 21. Design Decisions To Keep Stable

- provider interfaces must remain swappable
- tools must have structured inputs and outputs
- CLI commands should stay human-readable and scriptable
- safety policies should be centralized
- reports should be markdown-first
- repository knowledge should be separable from session memory

These choices reduce coupling and make later expansion easier.

---

## 22. Initial Risks

### Risk: LLM Inconsistency

Mitigation:

- use structured prompts
- constrain tool outputs
- add retries and fallback models

### Risk: Unsafe Or Excessive Actions

Mitigation:

- read-only default mode
- approval requirements for writes and shell execution
- explicit path and command restrictions

### Risk: Weak Large-Repo Understanding

Mitigation:

- add RAG early
- chunk intelligently by file type
- prioritize relevant retrieval over full-context dumping

### Risk: Slow UX

Mitigation:

- stream output
- cache repo metadata
- use smaller models for planning

---

## 23. Immediate Next Files To Create

After this document, the next recommended files are:

1. `pyproject.toml`
2. `README.md`
3. `src/codeverse/cli/main.py`
4. `src/codeverse/config/settings.py`
5. `src/codeverse/providers/base.py`
6. `src/codeverse/providers/registry.py`
7. `src/codeverse/tools/base.py`
8. `src/codeverse/mcp/client.py`
9. `src/codeverse/mcp/registry.py`

This sequence establishes the package, CLI, config, provider abstraction, and tool contracts first.

---

## 24. Final Recommendation

Build the product in this order:

1. architecture and contracts
2. CLI foundation
3. provider abstraction
4. repo inspection tools
5. agent loop
6. retrieval and memory
7. reporting workflows
8. safe edit workflows
9. advanced UX and plugin support

The fastest path to a strong MVP is to focus first on:

- ask questions about a repo
- analyze architecture
- debug with project context
- generate implementation plans
- produce safe, high-quality reports

That creates a useful product quickly and leaves room for deeper automation later.
