from pathlib import Path

from pydantic import BaseModel, Field


class SafetyConfig(BaseModel):
    read_only_default: bool = True
    require_edit_approval: bool = True
    allow_shell: bool = False
    allow_network: bool = False
    allowed_shell_commands: list[str] = Field(default_factory=lambda: ["git", "python", "python3", "pytest"])
    max_command_timeout_seconds: int = 30


class ProviderConfig(BaseModel):
    api_key: str | None = None
    base_url: str | None = None


class ProvidersConfig(BaseModel):
    openrouter: ProviderConfig = Field(default_factory=lambda: ProviderConfig(base_url="https://openrouter.ai/api/v1"))
    gemini: ProviderConfig = Field(default_factory=lambda: ProviderConfig(base_url="https://generativelanguage.googleapis.com/v1beta/models"))
    huggingface: ProviderConfig = Field(default_factory=lambda: ProviderConfig(base_url="https://api-inference.huggingface.co/models"))


class MCPConfig(BaseModel):
    registry_path: Path = Field(default=Path.home() / ".codeverse" / "mcp_servers.json")
