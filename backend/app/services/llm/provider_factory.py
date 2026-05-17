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
from app.services.llm.schemas import ProviderDiagnostics


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


def get_llm_provider_diagnostics(provider_name: str | None = None) -> ProviderDiagnostics:
    """Return non-secret provider readiness diagnostics.

    This helper is intentionally read-only: it does not make external calls,
    validate remote credentials, or expose credential values.
    """

    load_project_env()
    name = _normalize_provider(provider_name or os.getenv("LLM_PROVIDER", "mock"))
    real_calls_enabled = False if name == "mock" else _env_bool("LLM_ENABLE_REAL_CALLS", default=False)
    provider_cls = SUPPORTED_PROVIDERS.get(name)
    if provider_cls is None:
        return ProviderDiagnostics(
            provider_name=name,
            real_calls_enabled=real_calls_enabled,
            api_key_present=False,
            provider_status="unknown_provider",
        )

    required_credentials = list(provider_cls.get_required_credentials())
    credential_presence = {
        credential: bool(os.getenv(credential, "").strip())
        for credential in required_credentials
    }
    api_key_present = bool(required_credentials) and all(credential_presence.values())

    if name == "mock":
        provider_status = "mock_ready"
    elif not real_calls_enabled:
        provider_status = "provider_not_enabled"
    elif not api_key_present:
        provider_status = "not_configured"
    else:
        provider_status = "provider_not_enabled"

    return ProviderDiagnostics(
        provider_name=name,
        real_calls_enabled=real_calls_enabled,
        api_key_present=api_key_present,
        provider_status=provider_status,
        required_credentials=required_credentials,
        credential_presence=credential_presence,
    )


def _normalize_provider(value: str) -> str:
    return (value or "mock").strip().lower()


def _env_bool(name: str, *, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}
