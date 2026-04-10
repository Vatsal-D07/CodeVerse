from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from codeverse.config.models import MCPConfig, ProvidersConfig, SafetyConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CODEVERSE_", env_nested_delimiter="__", extra="ignore")

    app_name: str = "codeverse"
    default_provider: str = "openrouter"
    default_model: str = "meta-llama/llama-3.1-8b-instruct"
    request_timeout_seconds: int = 30
    allow_stub_responses: bool = True
    workspace_root: Path = Field(default_factory=Path.cwd)
    providers: ProvidersConfig = Field(default_factory=ProvidersConfig)
    safety: SafetyConfig = Field(default_factory=SafetyConfig)
    mcp: MCPConfig = Field(default_factory=MCPConfig)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    get_settings.cache_clear()
