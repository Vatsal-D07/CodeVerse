import json
from dataclasses import dataclass
from typing import Any, Protocol
from urllib import error, parse, request

from codeverse.config.models import ProviderConfig
from codeverse.config.settings import Settings


@dataclass(frozen=True)
class ProviderInfo:
    name: str
    supports_streaming: bool = True
    supports_embeddings: bool = False


class BaseLLMProvider(Protocol):
    info: ProviderInfo

    def generate(self, messages: list[dict[str, str]], model: str, temperature: float = 0.2, stream: bool = False) -> str:
        ...

    def health_check(self) -> dict[str, str]:
        ...


class BaseEmbeddingProvider(Protocol):
    def embed(self, texts: list[str], model: str | None = None) -> list[list[float]]:
        ...


class StubProvider:
    def __init__(self, name: str, supports_embeddings: bool = False) -> None:
        self.info = ProviderInfo(name=name, supports_embeddings=supports_embeddings)

    def generate(self, messages: list[dict[str, str]], model: str, temperature: float = 0.2, stream: bool = False) -> str:
        prompt = messages[-1]["content"] if messages else ""
        return f"[{self.info.name}:{model}] {prompt}"

    def health_check(self) -> dict[str, str]:
        return {"status": "ok", "provider": self.info.name}


class HTTPProvider:
    def __init__(self, name: str, settings: Settings, config: ProviderConfig, supports_embeddings: bool = False) -> None:
        self.info = ProviderInfo(name=name, supports_embeddings=supports_embeddings)
        self.settings = settings
        self.config = config

    def generate(self, messages: list[dict[str, str]], model: str, temperature: float = 0.2, stream: bool = False) -> str:
        if stream:
            raise ValueError(f"Provider '{self.info.name}' does not support streaming yet")
        if not self.config.api_key:
            if self.settings.allow_stub_responses:
                prompt = messages[-1]["content"] if messages else ""
                return f"[{self.info.name}:{model}] {prompt}"
            raise ValueError(f"Provider '{self.info.name}' requires an API key")
        payload = self._build_payload(messages=messages, model=model, temperature=temperature)
        response = self._post_json(url=self._build_url(model), headers=self._build_headers(), payload=payload)
        return self._extract_text(response)

    def health_check(self) -> dict[str, str]:
        return {
            "status": "stub" if not self.config.api_key else "configured",
            "provider": self.info.name,
        }

    def _build_url(self, model: str) -> str:
        raise NotImplementedError

    def _build_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}

    def _build_payload(self, messages: list[dict[str, str]], model: str, temperature: float) -> dict[str, Any]:
        raise NotImplementedError

    def _extract_text(self, response: dict[str, Any]) -> str:
        raise NotImplementedError

    def _post_json(self, url: str, headers: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
        req = request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        timeout = self.settings.request_timeout_seconds
        try:
            with request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"{self.info.name} request failed: {exc.code} {body}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"{self.info.name} request failed: {exc.reason}") from exc


def append_query_params(url: str, params: dict[str, str]) -> str:
    return f"{url}?{parse.urlencode(params)}"
