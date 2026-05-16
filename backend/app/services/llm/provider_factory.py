from __future__ import annotations

import os
from typing import Type

from app.core.environment import load_project_env
from app.services.llm.base_provider import BaseLLMProvider
from app.services.llm.deepseek_provider import DeepSeekProvider
from app.services.llm.errors import LLMProviderConfigError
from app.services.llm.mock_provider import MockProvider
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.qwen_provider import QwenProvider


SUPPORTED_PROVIDERS: dict[str, Type[BaseLLMProvider]] = {
    "mock": MockProvider,
    "openai": OpenAIProvider,
    "deepseek": DeepSeekProvider,
    "qwen": QwenProvider,
}


def get_llm_provider(provider_name: str | None = None) -> BaseLLMProvider:
    """Return the configured LLM provider without making external calls."""

    load_project_env()
    name = _normalize_provider(provider_name or os.getenv("LLM_PROVIDER", "mock"))
    provider_cls = SUPPORTED_PROVIDERS.get(name)
    if provider_cls is None:
        raise LLMProviderConfigError(
            f"Unknown LLM_PROVIDER '{name}'. Supported providers: {', '.join(sorted(SUPPORTED_PROVIDERS))}.",
            category="unknown_provider",
            provider=name,
        )

    if name == "mock":
        return provider_cls(real_calls_enabled=False)

    return provider_cls(real_calls_enabled=_env_bool("LLM_ENABLE_REAL_CALLS", default=False))


def _normalize_provider(value: str) -> str:
    return (value or "mock").strip().lower()


def _env_bool(name: str, *, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}
