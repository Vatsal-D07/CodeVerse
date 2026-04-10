import pytest

from codeverse.config.settings import Settings
from codeverse.providers.base import StubProvider
from codeverse.providers.gemini import GeminiProvider
from codeverse.providers.huggingface import HuggingFaceProvider
from codeverse.providers.openrouter import OpenRouterProvider
from codeverse.providers.registry import ProviderRegistry


def test_default_registry_contains_expected_providers() -> None:
    registry = ProviderRegistry.default(Settings())
    assert registry.list_names() == ["gemini", "huggingface", "openrouter"]


def test_duplicate_provider_rejected() -> None:
    registry = ProviderRegistry()
    registry.register(StubProvider("demo"))
    with pytest.raises(ValueError):
        registry.register(StubProvider("demo"))


def test_unknown_provider_rejected() -> None:
    registry = ProviderRegistry()
    with pytest.raises(KeyError):
        registry.get("missing")


def test_openrouter_http_payload() -> None:
    settings = Settings(allow_stub_responses=False, providers={"openrouter": {"api_key": "token"}})
    provider = OpenRouterProvider(settings=settings, config=settings.providers.openrouter)
    provider._post_json = lambda url, headers, payload: {"choices": [{"message": {"content": payload["messages"][0]["content"]}}]}  # type: ignore[method-assign]
    output = provider.generate(messages=[{"role": "user", "content": "hello"}], model="demo")
    assert output == "hello"


def test_gemini_http_payload() -> None:
    settings = Settings(allow_stub_responses=False, providers={"gemini": {"api_key": "token"}})
    provider = GeminiProvider(settings=settings, config=settings.providers.gemini)
    provider._post_json = lambda url, headers, payload: {"candidates": [{"content": {"parts": [{"text": payload["contents"][0]["parts"][0]["text"]}]}}]}  # type: ignore[method-assign]
    output = provider.generate(messages=[{"role": "user", "content": "hello"}], model="gemini-1.5-flash")
    assert output == "hello"


def test_huggingface_http_payload() -> None:
    settings = Settings(allow_stub_responses=False, providers={"huggingface": {"api_key": "token"}})
    provider = HuggingFaceProvider(settings=settings, config=settings.providers.huggingface)
    provider._post_json = lambda url, headers, payload: [{"generated_text": payload["inputs"]}]  # type: ignore[method-assign]
    output = provider.generate(messages=[{"role": "user", "content": "hello"}], model="demo-model")
    assert output == "hello"
