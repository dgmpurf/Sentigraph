from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.llm.deepseek_provider import DeepSeekProvider
from app.services.llm.errors import LLMProviderConfigError, LLMProviderNotEnabledError
from app.services.llm.json_guard import parse_json_array, parse_json_object
from app.services.llm.mock_provider import MockProvider
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.provider_factory import get_llm_provider
from app.services.llm.qwen_provider import QwenProvider


client = TestClient(app)


def test_llm_provider_module_files_exist() -> None:
    llm_dir = Path(__file__).resolve().parents[1] / "services" / "llm"

    expected_files = {
        "__init__.py",
        "base_provider.py",
        "mock_provider.py",
        "openai_provider.py",
        "deepseek_provider.py",
        "qwen_provider.py",
        "provider_factory.py",
        "schemas.py",
        "json_guard.py",
        "errors.py",
    }

    assert expected_files <= {path.name for path in llm_dir.iterdir()}


def test_mock_provider_expands_keywords_deterministically() -> None:
    result = MockProvider().expand_keywords("Tesla", language="auto")

    assert result.provider == "mock"
    assert result.original_keyword == "Tesla"
    assert result.expanded_keywords == ["Tesla", "特斯拉", "Model Y", "自动驾驶", "降价"]
    assert result.search_queries == ["Tesla problem", "Tesla recall", "特斯拉 刹车", "特斯拉 降价"]


def test_mock_provider_sentiment_output_is_stable() -> None:
    negative = MockProvider().analyze_sentiment("The product has a serious quality problem.")
    positive = MockProvider().analyze_sentiment("Great support resolved the issue.")
    neutral = MockProvider().analyze_sentiment("Users are discussing the topic.")

    assert negative.sentiment == "negative"
    assert negative.sentiment_score < 0
    assert positive.sentiment in {"positive", "mixed"}
    assert neutral.sentiment == "neutral"


def test_mock_provider_topics_and_cluster_summary_are_deterministic() -> None:
    provider = MockProvider()
    texts = [
        "quality issue and broken part",
        "official response statement",
        "quality problem needs response",
    ]

    first_topics = provider.extract_topics(texts, language="en-US")
    second_topics = provider.extract_topics(texts, language="en-US")
    summary = provider.summarize_cluster(
        [{"content": texts[0]}, {"text": texts[1]}, texts[2]],
        language="en-US",
    )

    assert first_topics.model_dump() == second_topics.model_dump()
    assert first_topics.provider == "mock"
    assert first_topics.topics[0].topic == "Product quality issues"
    assert first_topics.topics[0].count == 2
    assert summary.provider == "mock"
    assert summary.comment_count == 3
    assert "public comment(s)" in summary.summary


def test_mock_provider_report_and_recommendations_are_offline() -> None:
    provider = MockProvider()
    report = provider.generate_report(
        {"project_id": "project_001", "keyword": "Tesla", "risk_level": "medium", "risk_score": 56}
    )
    recommendations = provider.generate_recommendations({"risk_level": "high"}, user_type="brand")

    assert report.provider == "mock"
    assert report.generated_from_mock_provider is True
    assert "MockProvider" in report.key_findings[-1]
    assert recommendations.provider == "mock"
    assert recommendations.escalation_level == "escalate"


def test_keyword_expansion_falls_back_to_mock_when_real_provider_is_disabled(monkeypatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("LLM_ENABLE_REAL_CALLS", "false")
    monkeypatch.setenv("OPENAI_API_KEY", "secret-value-should-not-appear")

    response = client.post(
        "/api/v1/keywords/expand",
        json={"keyword": "Tesla", "platforms": ["weibo"], "language": "auto"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["expanded_keywords"] == ["Tesla", "特斯拉", "Model Y", "自动驾驶", "降价"]
    assert "secret-value-should-not-appear" not in response.text


def test_provider_factory_defaults_to_mock(monkeypatch) -> None:
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("LLM_ENABLE_REAL_CALLS", raising=False)

    provider = get_llm_provider()

    assert isinstance(provider, MockProvider)
    assert provider.health_check().ok is True


def test_provider_factory_unknown_provider_fails_safely(monkeypatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "unknown-model")

    with pytest.raises(LLMProviderConfigError) as exc_info:
        get_llm_provider()

    assert exc_info.value.category == "unknown_provider"
    assert "unknown-model" in str(exc_info.value)


@pytest.mark.parametrize(
    ("provider_name", "provider_cls"),
    [
        ("openai", OpenAIProvider),
        ("deepseek", DeepSeekProvider),
        ("qwen", QwenProvider),
    ],
)
def test_real_providers_are_disabled_by_default(monkeypatch, provider_name, provider_cls) -> None:
    monkeypatch.setenv("LLM_PROVIDER", provider_name)
    monkeypatch.delenv("LLM_ENABLE_REAL_CALLS", raising=False)
    for credential in provider_cls.get_required_credentials():
        monkeypatch.delenv(credential, raising=False)

    provider = get_llm_provider()
    health = provider.health_check()

    assert isinstance(provider, provider_cls)
    assert health.ok is False
    assert health.error_category == "provider_not_enabled"
    with pytest.raises(LLMProviderNotEnabledError) as exc_info:
        provider.expand_keywords("Tesla")
    assert exc_info.value.category == "provider_not_enabled"


@pytest.mark.parametrize(
    ("provider_name", "provider_cls"),
    [
        ("openai", OpenAIProvider),
        ("deepseek", DeepSeekProvider),
        ("qwen", QwenProvider),
    ],
)
def test_missing_real_provider_api_keys_do_not_crash(monkeypatch, provider_name, provider_cls) -> None:
    monkeypatch.setenv("LLM_PROVIDER", provider_name)
    monkeypatch.setenv("LLM_ENABLE_REAL_CALLS", "true")
    for credential in provider_cls.get_required_credentials():
        monkeypatch.delenv(credential, raising=False)

    provider = get_llm_provider()
    health = provider.health_check()

    assert health.ok is False
    assert health.configured is False
    assert health.error_category == "not_configured"
    with pytest.raises(LLMProviderConfigError) as exc_info:
        provider.generate_report({"keyword": "Tesla"})
    assert exc_info.value.category == "not_configured"


def test_real_provider_placeholder_does_not_make_network_calls(monkeypatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("LLM_ENABLE_REAL_CALLS", "true")
    monkeypatch.setenv("OPENAI_API_KEY", "secret-value-should-not-appear")

    provider = get_llm_provider()
    health = provider.health_check()

    assert health.ok is False
    assert health.configured is True
    assert "secret-value-should-not-appear" not in health.model_dump_json()
    with pytest.raises(LLMProviderNotEnabledError) as exc_info:
        provider.analyze_sentiment("test")
    assert exc_info.value.category == "provider_not_enabled"
    assert "secret-value-should-not-appear" not in str(exc_info.value)


@pytest.mark.parametrize(
    ("provider_name", "provider_cls", "credential_name"),
    [
        ("openai", OpenAIProvider, "OPENAI_API_KEY"),
        ("deepseek", DeepSeekProvider, "DEEPSEEK_API_KEY"),
        ("qwen", QwenProvider, "QWEN_API_KEY"),
    ],
)
def test_real_provider_errors_do_not_expose_key_values(
    monkeypatch,
    provider_name,
    provider_cls,
    credential_name,
) -> None:
    secret_value = f"{provider_name}-secret-value-should-not-appear"
    monkeypatch.setenv("LLM_PROVIDER", provider_name)
    monkeypatch.setenv("LLM_ENABLE_REAL_CALLS", "true")
    monkeypatch.setenv(credential_name, secret_value)

    provider = get_llm_provider()
    health = provider.health_check()

    assert isinstance(provider, provider_cls)
    assert provider.credential_presence() == {credential_name: True}
    assert secret_value not in health.model_dump_json()
    with pytest.raises(LLMProviderNotEnabledError) as exc_info:
        provider.generate_recommendations({"risk_level": "medium"})
    assert secret_value not in str(exc_info.value)


def test_json_guard_valid_and_invalid_json() -> None:
    assert parse_json_object('{"status": "ok"}') == {"status": "ok"}
    assert parse_json_object("[1, 2]", fallback={"status": "fallback"}) == {"status": "fallback"}
    assert parse_json_object("not json", fallback={"error": "malformed"}) == {"error": "malformed"}

    assert parse_json_array('[{"id": 1}]') == [{"id": 1}]
    assert parse_json_array('{"id": 1}', fallback=[]) == []
    assert parse_json_array("```json\n[1, 2]\n```") == [1, 2]
