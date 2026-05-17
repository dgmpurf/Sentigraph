from __future__ import annotations

from pathlib import Path

import pytest

from app.core.config import settings
from app.schemas.selector_repair import SelectorRepairRequest
from app.services.llm.errors import LLMProviderNotEnabledError
from app.services.llm.mock_provider import MockProvider
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.provider_factory import get_llm_provider
from app.services.llm.usage_guardrails import (
    check_call_allowed,
    estimate_tokens_from_chars,
    get_usage_summary,
    record_mock_call,
    reset_usage_for_tests,
)


GUARDRAIL_ENV_NAMES = [
    "LLM_USAGE_TRACKING_ENABLED",
    "LLM_DAILY_CALL_LIMIT",
    "LLM_DAILY_TOKEN_LIMIT",
    "LLM_MAX_INPUT_CHARS",
    "LLM_FAIL_CLOSED_ON_LIMIT",
    "LLM_COST_GUARDRAIL_MODE",
]


@pytest.fixture(autouse=True)
def clean_usage_state(monkeypatch):
    reset_usage_for_tests()
    for name in GUARDRAIL_ENV_NAMES:
        monkeypatch.delenv(name, raising=False)
    yield
    reset_usage_for_tests()


def test_guardrail_config_defaults_are_safe() -> None:
    assert settings.llm_usage_tracking_enabled is True
    assert settings.llm_daily_call_limit == 100
    assert settings.llm_daily_token_limit == 100000
    assert settings.llm_max_input_chars == 20000
    assert settings.llm_fail_closed_on_limit is True
    assert settings.llm_cost_guardrail_mode == "mock"


def test_env_example_documents_guardrail_defaults() -> None:
    env_example = (Path(__file__).resolve().parents[3] / ".env.example").read_text(encoding="utf-8")

    assert "LLM_USAGE_TRACKING_ENABLED=true" in env_example
    assert "LLM_DAILY_CALL_LIMIT=100" in env_example
    assert "LLM_DAILY_TOKEN_LIMIT=100000" in env_example
    assert "LLM_MAX_INPUT_CHARS=20000" in env_example
    assert "LLM_FAIL_CLOSED_ON_LIMIT=true" in env_example
    assert "LLM_COST_GUARDRAIL_MODE=mock" in env_example


def test_token_estimate_is_deterministic() -> None:
    assert estimate_tokens_from_chars(0) == 0
    assert estimate_tokens_from_chars(1) == 1
    assert estimate_tokens_from_chars(4) == 1
    assert estimate_tokens_from_chars(5) == 2
    assert estimate_tokens_from_chars(20000) == 5000
    assert estimate_tokens_from_chars(-5) == 0


def test_call_allowed_under_limit(monkeypatch) -> None:
    monkeypatch.setenv("LLM_DAILY_CALL_LIMIT", "2")
    monkeypatch.setenv("LLM_DAILY_TOKEN_LIMIT", "100")
    monkeypatch.setenv("LLM_MAX_INPUT_CHARS", "1000")

    decision = check_call_allowed("openai", "keyword_expansion", input_chars=20)

    assert decision.allowed is True
    assert decision.provider == "openai"
    assert decision.operation == "keyword_expansion"
    assert decision.estimated_input_tokens == 5
    assert decision.reason_category is None


def test_call_blocked_over_call_limit(monkeypatch) -> None:
    monkeypatch.setenv("LLM_DAILY_CALL_LIMIT", "1")
    record_mock_call("mock", "expand_keywords", input_chars=8, output_chars=8)

    decision = check_call_allowed("openai", "keyword_expansion", input_chars=8)

    assert decision.allowed is False
    assert decision.reason_category == "daily_call_limit_exceeded"
    assert decision.daily_calls_remaining == 0


def test_call_blocked_over_input_limit(monkeypatch) -> None:
    monkeypatch.setenv("LLM_MAX_INPUT_CHARS", "10")

    decision = check_call_allowed("openai", "keyword_expansion", input_chars=11)

    assert decision.allowed is False
    assert decision.reason_category == "input_too_large"


def test_call_blocked_over_token_limit(monkeypatch) -> None:
    monkeypatch.setenv("LLM_DAILY_TOKEN_LIMIT", "2")

    decision = check_call_allowed("openai", "keyword_expansion", input_chars=9)

    assert decision.allowed is False
    assert decision.reason_category == "daily_token_limit_exceeded"


def test_fail_open_mode_keeps_reason_but_allows(monkeypatch) -> None:
    monkeypatch.setenv("LLM_MAX_INPUT_CHARS", "10")
    monkeypatch.setenv("LLM_FAIL_CLOSED_ON_LIMIT", "false")

    decision = check_call_allowed("openai", "keyword_expansion", input_chars=11)

    assert decision.allowed is True
    assert decision.reason_category == "input_too_large"


def test_mock_provider_records_usage_without_raw_prompt_text() -> None:
    raw_prompt = "RAW_PROMPT_SHOULD_NOT_APPEAR quality issue"

    result = MockProvider().analyze_sentiment(raw_prompt)
    summary = get_usage_summary()

    assert result.provider == "mock"
    assert summary.tracking_enabled is True
    assert summary.total_calls == 1
    assert summary.daily_calls == 1
    assert summary.recent_records[0].provider == "mock"
    assert summary.recent_records[0].operation == "analyze_sentiment"
    assert summary.recent_records[0].input_chars == len(raw_prompt)
    assert "RAW_PROMPT_SHOULD_NOT_APPEAR" not in summary.model_dump_json()
    assert "quality issue" not in summary.model_dump_json()


def test_mock_provider_records_report_and_selector_operations() -> None:
    provider = MockProvider()

    provider.generate_report({"project_id": "project_001", "keyword": "Tesla"})
    provider.suggest_selector_repair(
        request=SelectorRepairRequest(
            platform_id="hupu",
            sanitized_html="<article><h1>Fixture</h1></article>",
            extraction_targets=["title"],
        )
    )

    summary = get_usage_summary()
    operations = {record.operation for record in summary.recent_records}
    assert {"generate_report", "suggest_selector_repair"} <= operations
    assert "<article>" not in summary.model_dump_json()
    assert "Tesla" not in summary.model_dump_json()


def test_mock_provider_records_all_supported_mock_operations_without_raw_content() -> None:
    provider = MockProvider()

    provider.expand_keywords("RAW_KEYWORD_SHOULD_NOT_APPEAR")
    provider.analyze_sentiment("RAW_SENTIMENT_SHOULD_NOT_APPEAR quality problem")
    provider.summarize_cluster(["RAW_TOPIC_SHOULD_NOT_APPEAR quality problem"])
    provider.generate_report({"project_id": "RAW_REPORT_SHOULD_NOT_APPEAR", "keyword": "Tesla"})
    provider.generate_recommendations({"keyword": "RAW_RECOMMENDATION_SHOULD_NOT_APPEAR", "risk_level": "high"})
    provider.suggest_selector_repair(
        request=SelectorRepairRequest(
            platform_id="hupu",
            sanitized_html="<article>RAW_HTML_SHOULD_NOT_APPEAR</article>",
            extraction_targets=["title"],
            parser_error_summary="RAW_ERROR_SHOULD_NOT_APPEAR",
        )
    )

    summary = get_usage_summary()
    operations = {record.operation for record in summary.recent_records}
    assert {
        "expand_keywords",
        "analyze_sentiment",
        "extract_topics",
        "summarize_cluster",
        "generate_report",
        "generate_recommendations",
        "suggest_selector_repair",
    } <= operations

    summary_json = summary.model_dump_json()
    assert "RAW_KEYWORD_SHOULD_NOT_APPEAR" not in summary_json
    assert "RAW_SENTIMENT_SHOULD_NOT_APPEAR" not in summary_json
    assert "RAW_TOPIC_SHOULD_NOT_APPEAR" not in summary_json
    assert "RAW_REPORT_SHOULD_NOT_APPEAR" not in summary_json
    assert "RAW_RECOMMENDATION_SHOULD_NOT_APPEAR" not in summary_json
    assert "RAW_HTML_SHOULD_NOT_APPEAR" not in summary_json
    assert "RAW_ERROR_SHOULD_NOT_APPEAR" not in summary_json


def test_usage_record_contains_safe_metadata_fields_only() -> None:
    record = record_mock_call("mock", "expand_keywords", input_chars=8, output_chars=16)

    assert record is not None
    assert set(record.model_dump()) == {
        "provider",
        "operation",
        "input_chars",
        "output_chars",
        "estimated_input_tokens",
        "estimated_output_tokens",
        "timestamp",
        "success",
        "failure_category",
    }


def test_usage_summary_and_reset_work() -> None:
    record_mock_call("mock", "expand_keywords", input_chars=8, output_chars=16)
    record_mock_call("mock", "summarize_cluster", input_chars=20, output_chars=10)

    summary = get_usage_summary()

    assert summary.total_calls == 2
    assert summary.daily_calls == 2
    assert summary.daily_input_tokens == 7
    assert summary.daily_output_tokens == 7
    assert summary.daily_total_tokens == 14

    reset_usage_for_tests()
    reset_summary = get_usage_summary()
    assert reset_summary.total_calls == 0
    assert reset_summary.recent_records == []


def test_tracking_disabled_does_not_record(monkeypatch) -> None:
    monkeypatch.setenv("LLM_USAGE_TRACKING_ENABLED", "false")

    record = record_mock_call("mock", "expand_keywords", input_chars=8, output_chars=16)
    decision = check_call_allowed("openai", "keyword_expansion", input_chars=8)
    summary = get_usage_summary()

    assert record is None
    assert decision.allowed is True
    assert decision.reason_category == "tracking_disabled"
    assert summary.tracking_enabled is False
    assert summary.total_calls == 0


def test_safe_provider_and_operation_labels_only() -> None:
    record = record_mock_call(
        "mock provider with spaces",
        "selector repair / weird op",
        input_chars=8,
        output_chars=16,
    )

    assert record is not None
    assert record.provider == "mock_provider_with_spaces"
    assert record.operation == "selector_repair_weird_op"


def test_real_providers_remain_disabled_and_do_not_print_keys(monkeypatch) -> None:
    secret_value = "secret-value-should-not-appear"
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("LLM_ENABLE_REAL_CALLS", "true")
    monkeypatch.setenv("OPENAI_API_KEY", secret_value)

    provider = get_llm_provider()
    health = provider.health_check()

    assert isinstance(provider, OpenAIProvider)
    assert health.ok is False
    assert health.error_category == "provider_not_enabled"
    assert secret_value not in health.model_dump_json()
    with pytest.raises(LLMProviderNotEnabledError) as exc_info:
        provider.expand_keywords("Tesla")
    assert secret_value not in str(exc_info.value)


def test_placeholder_real_provider_checks_guardrails_before_future_call(monkeypatch) -> None:
    secret_value = "secret-value-should-not-appear"
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("LLM_ENABLE_REAL_CALLS", "true")
    monkeypatch.setenv("OPENAI_API_KEY", secret_value)
    monkeypatch.setenv("LLM_MAX_INPUT_CHARS", "5")

    provider = get_llm_provider()

    with pytest.raises(LLMProviderNotEnabledError) as exc_info:
        provider.expand_keywords("longer-than-five")

    assert exc_info.value.category == "input_too_large"
    assert secret_value not in str(exc_info.value)
