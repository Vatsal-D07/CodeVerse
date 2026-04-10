# Codeverse Execution Plan

## 1. Delivery Strategy

Codeverse will be built in vertical slices with hard verification gates between layers. Each slice must be independently testable, minimally coupled, and safe to evolve without breaking downstream modules.

The implementation order is designed to preserve long-term scalability while delivering a working CLI agent early.

## 2. Delivery Principles

- Keep public interfaces small and typed
- Build contracts before concrete integrations
- Ship read-only workflows before edit workflows
- Make every layer testable in isolation
- Prefer adapter boundaries over direct provider/tool coupling
- Add observability with each module, not as a later patch
- Keep the runtime deterministic where possible

## 3. Module Breakdown

### Chunk 1: Project Foundation

Scope:

- Python package structure
- dependency management
- CLI entrypoint
- version metadata
- base test harness

Outputs:

- `pyproject.toml`
- `src/codeverse/__init__.py`
- `src/codeverse/cli/main.py`
- `tests/`

Gate:

- `codeverse --help` works
- test runner works

### Chunk 2: Configuration And Runtime Settings

Scope:

- environment-backed settings
- provider selection
- model defaults
- MCP config storage paths
- safety defaults

Outputs:

- `src/codeverse/config/settings.py`
- `src/codeverse/config/models.py`

Gate:

- settings load cleanly from env
- invalid configuration is rejected predictably

### Chunk 3: Provider Contracts And Registry

Scope:

- base LLM interface
- base embeddings interface
- provider registry
- provider health metadata
- stub provider implementations for OpenRouter, Gemini, Hugging Face

Outputs:

- `src/codeverse/providers/base.py`
- `src/codeverse/providers/registry.py`
- provider adapter modules

Gate:

- providers can be registered, resolved, and validated
- tests run without external API calls

### Chunk 4: Core Tool Contracts

Scope:

- canonical tool request/response models
- tool execution context
- tool registry
- error classification

Outputs:

- `src/codeverse/tools/base.py`
- `src/codeverse/tools/registry.py`

Gate:

- native and MCP-backed tools can share the same interface

### Chunk 5: Native Read-Only Tools

Scope:

- filesystem read/list
- search
- git inspection
- shell command abstraction with safety guard
- minimal code analysis

Outputs:

- native tool modules

Gate:

- repo inspection commands work without edits
- all dangerous actions remain blocked by default

### Chunk 6: MCP Integration Layer

Scope:

- MCP server definitions
- local registry persistence
- client abstraction
- stdio transport contract
- MCP capability adaptation into tool contracts

Outputs:

- `src/codeverse/mcp/client.py`
- `src/codeverse/mcp/registry.py`
- `src/codeverse/mcp/models.py`
- `src/codeverse/tools/mcp_proxy.py`

Gate:

- MCP servers can be added, listed, removed, and inspected
- MCP tool metadata can be surfaced through the shared tool interface

### Chunk 7: Agent Runtime Skeleton

Scope:

- task state model
- intent parser
- planner
- runtime loop
- safety checks

Outputs:

- `src/codeverse/agent/*.py`

Gate:

- runtime can execute simple planned tasks using registered tools

### Chunk 8: CLI Command Handlers

Scope:

- `config` commands
- `mcp` commands
- `chat`, `analyze`, and `plan` skeletons
- output formatting

Outputs:

- command modules under `src/codeverse/cli/commands/`

Gate:

- CLI commands produce stable output and exit codes

### Chunk 9: Testing And Hardening

Scope:

- unit tests
- CLI tests
- config validation tests
- registry tests
- MCP persistence tests
- runtime smoke tests

Gate:

- green test suite
- no hidden network dependency in tests

## 4. Build Order

1. Foundation
2. Config
3. Providers
4. Tool contracts
5. Native tools
6. MCP integration
7. Agent runtime
8. CLI commands
9. Tests and hardening

## 5. Dependencies Between Chunks

- Config depends on foundation
- Providers depend on config
- Tool contracts depend on config only
- Native tools depend on tool contracts
- MCP integration depends on tool contracts and config
- Agent runtime depends on providers, tools, and MCP bridge
- CLI commands depend on runtime and registries
- Tests depend on all implemented layers

## 6. Testing Strategy Per Chunk

### Chunk 1

- import tests
- CLI help smoke test

### Chunk 2

- settings defaults
- env override behavior
- validation failures

### Chunk 3

- provider registration and lookup
- duplicate provider rejection
- unknown provider rejection

### Chunk 4

- tool request validation
- registry behavior
- execution result shape

### Chunk 5

- filesystem list/read behavior
- blocked path handling
- search results formatting
- git tool behavior in non-git folders

### Chunk 6

- server registry persistence
- duplicate MCP server handling
- MCP metadata normalization

### Chunk 7

- plan generation shape
- state transitions
- runtime iteration limits

### Chunk 8

- CLI exit codes
- human-readable output assertions
- command wiring correctness

## 7. Scalability Design Requirements

To support very large usage over time, the codebase must preserve these constraints from the start:

- stateless request processing where practical
- provider and tool clients must be replaceable with pooled or remote implementations later
- configuration must support per-user and per-workspace overrides
- logging and tracing must allow later integration with centralized observability
- tool execution and agent runtime should be safe to move behind API workers later
- storage models must avoid tight coupling to a local-only execution model

Scalability to millions of users will require later infrastructure beyond this local CLI foundation, but the module boundaries should avoid blocking that path.

## 8. Near-Term Scope Boundary

This implementation pass will build a strong local-first foundation with:

- typed module contracts
- real CLI commands
- provider registry
- MCP registry support
- native tool abstractions
- runtime skeleton
- complete automated tests for shipped code

This pass will not yet include:

- distributed control plane
- hosted multi-tenant backend
- usage billing
- remote session sync
- web UI

Those will be enabled later by the same boundaries if the local architecture remains clean.

## 9. Immediate Implementation Sequence

1. Create Python project foundation and tests
2. Add settings and models
3. Add providers and registry
4. Add tool base and registry
5. Add native filesystem and search tools
6. Add MCP models and registry
7. Add runtime state/parser/planner skeleton
8. Wire CLI commands
9. Run tests and fix until green

## 10. Definition Of Done For This Iteration

- package installs in editable mode
- `codeverse --help` works
- `codeverse config show` works
- `codeverse mcp list` works
- provider registry is tested
- MCP registry is tested
- tool registry is tested
- runtime skeleton executes a simple task path
- all tests pass locally
