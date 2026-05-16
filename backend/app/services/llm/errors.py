from __future__ import annotations


class LLMProviderError(RuntimeError):
    """Base error for safe LLM provider failures."""

    def __init__(
        self,
        message: str,
        *,
        category: str = "llm_provider_error",
        provider: str | None = None,
    ) -> None:
        super().__init__(message)
        self.category = category
        self.provider = provider


class LLMProviderConfigError(LLMProviderError):
    """Raised when provider configuration is invalid or incomplete."""

    def __init__(
        self,
        message: str,
        *,
        category: str = "config_error",
        provider: str | None = None,
    ) -> None:
        super().__init__(message, category=category, provider=provider)


class LLMProviderNotEnabledError(LLMProviderError):
    """Raised when a real provider is selected before real calls are enabled."""

    def __init__(
        self,
        message: str,
        *,
        category: str = "provider_not_enabled",
        provider: str | None = None,
    ) -> None:
        super().__init__(message, category=category, provider=provider)
