from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from typing import Iterable

from app.core.environment import load_project_env
from app.services.llm.schemas import (
    LLMGuardrailConfig,
    LLMGuardrailDecision,
    LLMUsageRecord,
    LLMUsageSummary,
)


_USAGE_RECORDS: list[LLMUsageRecord] = []
_SAFE_LABEL_PATTERN = re.compile(r"[^a-zA-Z0-9_.-]+")


def estimate_tokens_from_chars(chars: int) -> int:
    """Deterministically estimate tokens without inspecting raw content."""

    safe_chars = max(0, int(chars or 0))
    if safe_chars == 0:
        return 0
    return (safe_chars + 3) // 4


def check_call_allowed(provider: str, operation: str, input_chars: int) -> LLMGuardrailDecision:
    """Check future LLM call limits using metadata only."""

    config = load_guardrail_config()
    safe_provider = _safe_label(provider, fallback="unknown_provider")
    safe_operation = _safe_label(operation, fallback="unknown_operation")
    safe_input_chars = max(0, int(input_chars or 0))
    estimated_input_tokens = estimate_tokens_from_chars(safe_input_chars)
    daily_records = _daily_records()
    daily_calls = len(daily_records)
    daily_tokens = _total_tokens(daily_records)
    calls_remaining = max(0, config.daily_call_limit - daily_calls)
    tokens_remaining = max(0, config.daily_token_limit - daily_tokens)

    if not config.tracking_enabled:
        return LLMGuardrailDecision(
            allowed=True,
            provider=safe_provider,
            operation=safe_operation,
            estimated_input_tokens=estimated_input_tokens,
            reason_category="tracking_disabled",
            daily_calls_remaining=calls_remaining,
            daily_tokens_remaining=tokens_remaining,
            message="LLM usage tracking is disabled; call allowed by scaffold policy.",
        )

    blocked_reason: str | None = None
    if safe_input_chars > config.max_input_chars:
        blocked_reason = "input_too_large"
    elif daily_calls >= config.daily_call_limit:
        blocked_reason = "daily_call_limit_exceeded"
    elif daily_tokens + estimated_input_tokens > config.daily_token_limit:
        blocked_reason = "daily_token_limit_exceeded"

    if blocked_reason and config.fail_closed_on_limit:
        return LLMGuardrailDecision(
            allowed=False,
            provider=safe_provider,
            operation=safe_operation,
            estimated_input_tokens=estimated_input_tokens,
            reason_category=blocked_reason,
            daily_calls_remaining=calls_remaining,
            daily_tokens_remaining=tokens_remaining,
            message=f"LLM guardrail blocked call: {blocked_reason}.",
        )

    return LLMGuardrailDecision(
        allowed=True,
        provider=safe_provider,
        operation=safe_operation,
        estimated_input_tokens=estimated_input_tokens,
        reason_category=blocked_reason,
        daily_calls_remaining=calls_remaining,
        daily_tokens_remaining=tokens_remaining,
        message="LLM guardrail allowed call.",
    )


def record_mock_call(
    provider: str,
    operation: str,
    input_chars: int,
    output_chars: int,
    *,
    success: bool = True,
    failure_category: str | None = None,
) -> LLMUsageRecord | None:
    """Record mock usage metadata without storing prompts or raw text."""

    config = load_guardrail_config()
    if not config.tracking_enabled:
        return None

    safe_input_chars = max(0, int(input_chars or 0))
    safe_output_chars = max(0, int(output_chars or 0))
    record = LLMUsageRecord(
        provider=_safe_label(provider, fallback="unknown_provider"),
        operation=_safe_label(operation, fallback="unknown_operation"),
        input_chars=safe_input_chars,
        output_chars=safe_output_chars,
        estimated_input_tokens=estimate_tokens_from_chars(safe_input_chars),
        estimated_output_tokens=estimate_tokens_from_chars(safe_output_chars),
        timestamp=_utc_now_iso(),
        success=bool(success),
        failure_category=_safe_label(failure_category, fallback="") if failure_category else None,
    )
    _USAGE_RECORDS.append(record)
    return record


def get_usage_summary() -> LLMUsageSummary:
    config = load_guardrail_config()
    daily_records = _daily_records()
    return LLMUsageSummary(
        tracking_enabled=config.tracking_enabled,
        guardrail_mode=config.mode,
        daily_call_limit=config.daily_call_limit,
        daily_token_limit=config.daily_token_limit,
        max_input_chars=config.max_input_chars,
        total_calls=len(_USAGE_RECORDS),
        daily_calls=len(daily_records),
        daily_input_tokens=sum(record.estimated_input_tokens for record in daily_records),
        daily_output_tokens=sum(record.estimated_output_tokens for record in daily_records),
        daily_total_tokens=_total_tokens(daily_records),
        recent_records=list(_USAGE_RECORDS[-20:]),
    )


def reset_usage_for_tests() -> None:
    _USAGE_RECORDS.clear()


def load_guardrail_config() -> LLMGuardrailConfig:
    load_project_env()
    return LLMGuardrailConfig(
        tracking_enabled=_env_bool("LLM_USAGE_TRACKING_ENABLED", True),
        daily_call_limit=max(0, _env_int("LLM_DAILY_CALL_LIMIT", 100)),
        daily_token_limit=max(0, _env_int("LLM_DAILY_TOKEN_LIMIT", 100000)),
        max_input_chars=max(0, _env_int("LLM_MAX_INPUT_CHARS", 20000)),
        fail_closed_on_limit=_env_bool("LLM_FAIL_CLOSED_ON_LIMIT", True),
        mode=_safe_label(os.getenv("LLM_COST_GUARDRAIL_MODE", "mock"), fallback="mock"),
    )


def _daily_records() -> list[LLMUsageRecord]:
    today = datetime.now(timezone.utc).date().isoformat()
    return [record for record in _USAGE_RECORDS if record.timestamp[:10] == today]


def _total_tokens(records: Iterable[LLMUsageRecord]) -> int:
    return sum(record.estimated_input_tokens + record.estimated_output_tokens for record in records)


def _safe_label(value: str | None, *, fallback: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return fallback
    sanitized = _SAFE_LABEL_PATTERN.sub("_", raw)[:64].strip("._-")
    return sanitized or fallback


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default
