from typing import Any

from codeverse.config.models import ProviderConfig
from codeverse.config.settings import Settings
from codeverse.providers.base import HTTPProvider


class OpenRouterProvider(HTTPProvider):
    def __init__(self, settings: Settings, config: ProviderConfig) -> None:
        super().__init__(name="openrouter", settings=settings, config=config)

    def _build_url(self, model: str) -> str:
        del model
        return f"{self.config.base_url}/chat/completions"

    def _build_headers(self) -> dict[str, str]:
        headers = super()._build_headers()
        headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def _build_payload(self, messages: list[dict[str, str]], model: str, temperature: float) -> dict[str, Any]:
        return {"model": model, "messages": messages, "temperature": temperature}

    def _extract_text(self, response: dict[str, Any]) -> str:
        return response["choices"][0]["message"]["content"]
