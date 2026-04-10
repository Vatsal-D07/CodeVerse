from typing import Literal

from pydantic import BaseModel, Field


class MCPServerConfig(BaseModel):
    name: str
    transport: Literal["stdio"] = "stdio"
    command: str
    args: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)
    trusted: bool = False
