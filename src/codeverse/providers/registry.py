from codeverse.config.settings import Settings, get_settings
from codeverse.providers.base import BaseLLMProvider
from codeverse.providers.gemini import GeminiProvider
from codeverse.providers.huggingface import HuggingFaceProvider
from codeverse.providers.openrouter import OpenRouterProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, BaseLLMProvider] = {}

    def register(self, provider: BaseLLMProvider) -> None:
        name = provider.info.name
        if name in self._providers:
            raise ValueError(f"Provider '{name}' is already registered")
        self._providers[name] = provider

    def get(self, name: str) -> BaseLLMProvider:
        try:
            return self._providers[name]
        except KeyError as exc:
            raise KeyError(f"Unknown provider '{name}'") from exc

    def list_names(self) -> list[str]:
        return sorted(self._providers)

    def health(self) -> list[dict[str, str]]:
        return [self._providers[name].health_check() for name in self.list_names()]

    @classmethod
    def default(cls, settings: Settings | None = None) -> "ProviderRegistry":
        settings = settings or get_settings()
        registry = cls()
        registry.register(OpenRouterProvider(settings=settings, config=settings.providers.openrouter))
        registry.register(GeminiProvider(settings=settings, config=settings.providers.gemini))
        registry.register(HuggingFaceProvider(settings=settings, config=settings.providers.huggingface))
        return registry
