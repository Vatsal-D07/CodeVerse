from typing import Any

from codeverse.config.models import ProviderConfig
from codeverse.config.settings import Settings
from codeverse.providers.base import HTTPProvider


class HuggingFaceProvider(HTTPProvider):
    def __init__(self, settings: Settings, config: ProviderConfig) -> None:
        super().__init__(name="huggingface", settings=settings, config=config, supports_embeddings=True)

    def _build_url(self, model: str) -> str:
        return f"{self.config.base_url}/{model}"

    def _build_headers(self) -> dict[str, str]:
        headers = super()._build_headers()
        headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def _build_payload(self, messages: list[dict[str, str]], model: str, temperature: float) -> dict[str, Any]:
        del model
        prompt = "\n".join(message["content"] for message in messages)
        return {"inputs": prompt, "parameters": {"temperature": temperature, "return_full_text": False}}

    def _extract_text(self, response: dict[str, Any]) -> str:
        if isinstance(response, list):
            return response[0]["generated_text"]
        if "generated_text" in response:
            return response["generated_text"]
        raise KeyError("generated_text")
