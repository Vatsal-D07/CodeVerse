from typing import Any

from codeverse.config.models import ProviderConfig
from codeverse.config.settings import Settings
from codeverse.providers.base import HTTPProvider, append_query_params


class GeminiProvider(HTTPProvider):
    def __init__(self, settings: Settings, config: ProviderConfig) -> None:
        super().__init__(name="gemini", settings=settings, config=config)

    def _build_url(self, model: str) -> str:
        base = f"{self.config.base_url}/{model}:generateContent"
        return append_query_params(base, {"key": self.config.api_key or ""})

    def _build_payload(self, messages: list[dict[str, str]], model: str, temperature: float) -> dict[str, Any]:
        del model
        parts = [{"text": message["content"]} for message in messages]
        return {
            "contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"temperature": temperature},
        }

    def _extract_text(self, response: dict[str, Any]) -> str:
        return response["candidates"][0]["content"]["parts"][0]["text"]
