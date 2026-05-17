from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.services.llm.usage_guardrails import record_mock_call, reset_usage_for_tests


client = TestClient(app)


def test_llm_status_endpoint_returns_safe_provider_metadata(monkeypatch) -> None:
    secret = "sk-secret-value-should-not-appear"
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.setenv("LLM_ENABLE_REAL_CALLS", "false")
    monkeypatch.setenv("OPENAI_API_KEY", secret)

    response = client.get("/api/v1/llm/status")

    assert response.status_code == 200
    body = response.json()
    assert body["provider_name"] == "mock"
    assert body["provider_status"] == "mock_ready"
    assert body["real_calls_enabled"] is False
    assert body["api_key_present"] is False
    assert set(body["available_providers"]) == {"mock", "openai", "deepseek", "qwen"}
    assert body["tracking_enabled"] is True
    assert body["daily_call_limit"] == 100
    assert body["daily_token_limit"] == 100000
    assert body["max_input_chars"] == 20000
    assert body["safety_flags"]["api_key_values_exposed"] is False
    assert body["safety_flags"]["raw_prompt_logging"] is False
    assert secret not in response.text
    assert "OPENAI_API_KEY" not in response.text


def test_llm_status_endpoint_reports_selected_real_placeholder_safely(monkeypatch) -> None:
    secret = "qwen-secret-value-should-not-appear"
    monkeypatch.setenv("LLM_PROVIDER", "qwen")
    monkeypatch.setenv("LLM_ENABLE_REAL_CALLS", "false")
    monkeypatch.setenv("QWEN_API_KEY", secret)

    response = client.get("/api/v1/llm/status")

    assert response.status_code == 200
    body = response.json()
    assert body["provider_name"] == "qwen"
    assert body["provider_status"] == "provider_not_enabled"
    assert body["real_calls_enabled"] is False
    assert body["api_key_present"] is True
    assert secret not in response.text
    assert "QWEN_API_KEY" not in response.text


def test_llm_status_endpoint_handles_unknown_provider_safely(monkeypatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "unknown-provider")

    response = client.get("/api/v1/llm/status")

    assert response.status_code == 200
    body = response.json()
    assert body["provider_name"] == "unknown-provider"
    assert body["provider_status"] == "unknown_provider"
    assert body["api_key_present"] is False
    assert body["providers"]


def test_llm_usage_endpoint_exposes_metadata_only(monkeypatch) -> None:
    reset_usage_for_tests()
    secret = "raw-prompt-and-key-should-not-appear"
    monkeypatch.setenv("OPENAI_API_KEY", secret)
    record_mock_call(
        "mock",
        "expand_keywords",
        input_chars=len(secret),
        output_chars=42,
        success=True,
    )

    response = client.get("/api/v1/llm/usage")

    assert response.status_code == 200
    body = response.json()
    assert body["total_calls"] == 1
    assert body["daily_calls"] == 1
    assert body["recent_records"][0]["provider"] == "mock"
    assert body["recent_records"][0]["operation"] == "expand_keywords"
    assert set(body["recent_records"][0]) == {
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
    assert secret not in response.text
    assert "OPENAI_API_KEY" not in response.text
    reset_usage_for_tests()
