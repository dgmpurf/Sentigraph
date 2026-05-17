from __future__ import annotations

from fastapi import APIRouter

from app.services.llm.provider_factory import (
    SUPPORTED_PROVIDERS,
    get_llm_provider_diagnostics,
)
from app.services.llm.schemas import (
    LLMProviderPublicStatus,
    LLMSafetyStatusResponse,
    LLMUsageSummary,
)
from app.services.llm.usage_guardrails import get_usage_summary


router = APIRouter()


@router.get("/status", response_model=LLMSafetyStatusResponse)
def get_llm_status() -> LLMSafetyStatusResponse:
    """Return safe LLM readiness metadata without exposing credentials."""

    usage_summary = get_usage_summary()
    current = get_llm_provider_diagnostics()
    provider_statuses = [_public_provider_status(provider) for provider in sorted(SUPPORTED_PROVIDERS)]

    return LLMSafetyStatusResponse(
        provider_name=current.provider_name,
        provider_status=current.provider_status,
        real_calls_enabled=current.real_calls_enabled,
        api_key_present=current.api_key_present,
        available_providers=sorted(SUPPORTED_PROVIDERS),
        providers=provider_statuses,
        tracking_enabled=usage_summary.tracking_enabled,
        daily_call_limit=usage_summary.daily_call_limit,
        daily_token_limit=usage_summary.daily_token_limit,
        max_input_chars=usage_summary.max_input_chars,
        guardrail_mode=usage_summary.guardrail_mode,
        safety_flags={
            "mock_default": current.provider_name == "mock",
            "real_calls_disabled_by_default": not current.real_calls_enabled,
            "api_key_values_exposed": False,
            "raw_prompt_logging": False,
            "raw_user_content_logging": False,
        },
    )


@router.get("/usage", response_model=LLMUsageSummary)
def get_llm_usage() -> LLMUsageSummary:
    """Return metadata-only LLM usage summary.

    Usage records intentionally include only provider/operation labels, character
    counts, token estimates, timestamps, and success/failure categories.
    """

    return get_usage_summary()


def _public_provider_status(provider_name: str) -> LLMProviderPublicStatus:
    diagnostics = get_llm_provider_diagnostics(provider_name)
    return LLMProviderPublicStatus(
        provider_name=diagnostics.provider_name,
        provider_status=diagnostics.provider_status,
        real_calls_enabled=diagnostics.real_calls_enabled,
        api_key_present=diagnostics.api_key_present,
        api_key_required=bool(diagnostics.required_credentials),
        available=diagnostics.provider_status == "mock_ready",
    )
