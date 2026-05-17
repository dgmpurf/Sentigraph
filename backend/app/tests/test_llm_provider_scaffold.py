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
from app.services.llm.provider_factory import get_llm_provider, get_llm_provider_diagnostics
from app.services.llm.qwen_provider import QwenProvider
from app.services.llm.redaction import redact_api_key, redact_config_dict
import app.services.keyword.keyword_expander as keyword_expander


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
        "redaction.py",
        "usage_guardrails.py",
        "schemas.py",
        "json_guard.py",
        "errors.py",
    }

    assert expected_files <= {path.name for path in llm_dir.iterdir()}


def test_mock_provider_expands_keywords_deterministically() -> None:
    result = MockProvider().expand_keywords("Tesla", language="auto")

    assert result.provider == "mock"
    assert result.original_keyword == "Tesla"
    assert result.expanded_keywords == [
        "Tesla",
        "特斯拉",
        "Model Y",
        "Model 3",
        "电动车",
        "自动驾驶",
        "召回",
        "降价",
    ]
    assert result.search_queries == [
        "Tesla problem",
        "Tesla recall",
        "Tesla price cut",
        "特斯拉 召回",
        "特斯拉 降价",
        "特斯拉 自动驾驶",
    ]


def test_mock_provider_expands_bilibili_and_chinese_keywords() -> None:
    provider = MockProvider()

    bilibili = provider.expand_keywords("Bilibili", language="auto")
    chinese = provider.expand_keywords("新能源汽车", language="en-US")

    assert bilibili.expanded_keywords == ["Bilibili", "B站", "哔哩哔哩", "UP主", "弹幕", "视频评论"]
    assert "B站 视频评论" in bilibili.search_queries
    assert chinese.expanded_keywords == [
        "新能源汽车",
        "新能源汽车 舆情",
        "新能源汽车 投诉",
        "新能源汽车 争议",
        "新能源汽车 回应",
        "新能源汽车 风险",
    ]
    assert chinese.search_queries == [
        "新能源汽车 舆情",
        "新能源汽车 投诉",
        "新能源汽车 争议",
        "新能源汽车 官方回应",
    ]


def test_mock_provider_unknown_keyword_uses_public_opinion_variants() -> None:
    result = MockProvider().expand_keywords("Acme", language="auto")

    assert result.expanded_keywords == [
        "Acme",
        "Acme public opinion",
        "Acme complaints",
        "Acme controversy",
        "Acme response",
        "Acme 舆情",
    ]
    assert result.search_queries == [
        "Acme problem",
        "Acme complaints",
        "Acme controversy",
        "Acme response",
        "Acme 舆情",
    ]


def test_mock_provider_sentiment_output_is_stable() -> None:
    negative = MockProvider().analyze_sentiment("The product has a serious quality problem.")
    positive = MockProvider().analyze_sentiment("Great support resolved the issue.")
    neutral = MockProvider().analyze_sentiment("Users are discussing the topic.")
    questioning = MockProvider().analyze_sentiment("Why are users uncertain about this?")

    assert negative.sentiment == "negative"
    assert negative.sentiment_score < 0
    assert positive.sentiment in {"positive", "mixed"}
    assert neutral.sentiment == "neutral"
    assert questioning.sentiment == "neutral"
    assert questioning.stance == "questioning"
    assert "questioning" in questioning.emotion_tags


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
    monkeypatch.setattr(
        OpenAIProvider,
        "expand_keywords",
        lambda *args, **kwargs: pytest.fail("OpenAIProvider.expand_keywords must not be called"),
    )

    response = client.post(
        "/api/v1/keywords/expand",
        json={"keyword": "Tesla", "platforms": ["weibo"], "language": "auto"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["expanded_keywords"] == [
        "Tesla",
        "特斯拉",
        "Model Y",
        "Model 3",
        "电动车",
        "自动驾驶",
        "召回",
        "降价",
    ]
    assert "secret-value-should-not-appear" not in response.text


def test_keyword_expansion_uses_provider_factory_and_mock_by_default(monkeypatch) -> None:
    calls = {"count": 0}

    def fake_get_llm_provider():
        calls["count"] += 1
        return MockProvider()

    monkeypatch.setattr(keyword_expander, "get_llm_provider", fake_get_llm_provider)

    response = client.post(
        "/api/v1/keywords/expand",
        json={"keyword": "Bilibili", "platforms": ["bilibili"], "language": "auto"},
    )

    assert response.status_code == 200
    assert calls["count"] == 1
    body = response.json()
    assert body["expanded_keywords"] == ["Bilibili", "B站", "哔哩哔哩", "UP主", "弹幕", "视频评论"]


def test_keyword_expansion_missing_real_provider_keys_are_safe(monkeypatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("LLM_ENABLE_REAL_CALLS", "true")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(
        OpenAIProvider,
        "expand_keywords",
        lambda *args, **kwargs: pytest.fail("OpenAIProvider.expand_keywords must not be called"),
    )

    response = client.post(
        "/api/v1/keywords/expand",
        json={"keyword": "Tesla", "platforms": ["weibo"], "language": "auto"},
    )

    assert response.status_code == 200
    assert "OPENAI_API_KEY" not in response.text
    assert "not_configured" not in response.text
    assert "Tesla" in response.json()["expanded_keywords"]


def test_keyword_expand_api_keeps_existing_response_schema(monkeypatch) -> None:
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("LLM_ENABLE_REAL_CALLS", raising=False)

    response = client.post(
        "/api/v1/keywords/expand",
        json={"keyword": "Tesla", "platforms": ["weibo"], "language": "auto"},
    )

    assert response.status_code == 200
    assert set(response.json()) == {"original_keyword", "expanded_keywords", "search_queries"}


def test_keyword_expand_api_handles_chinese_tesla_keyword(monkeypatch) -> None:
    monkeypatch.delenv("LLM_PROVIDER", raising=False)

    response = client.post(
        "/api/v1/keywords/expand",
        json={"keyword": "特斯拉", "platforms": ["weibo"], "language": "auto"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["original_keyword"] == "特斯拉"
    assert body["expanded_keywords"] == [
        "特斯拉",
        "Tesla",
        "Model Y",
        "Model 3",
        "电动车",
        "自动驾驶",
        "召回",
        "降价",
    ]
    assert "特斯拉 召回" in body["search_queries"]


def test_keyword_expand_api_handles_chinese_keyword_and_unknown_provider(monkeypatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "unknown-provider")

    response = client.post(
        "/api/v1/keywords/expand",
        json={"keyword": "一个未知关键词", "platforms": ["weibo"], "language": "auto"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["original_keyword"] == "一个未知关键词"
    assert body["expanded_keywords"] == [
        "一个未知关键词",
        "一个未知关键词 舆情",
        "一个未知关键词 投诉",
        "一个未知关键词 争议",
        "一个未知关键词 回应",
        "一个未知关键词 风险",
    ]
    assert body["search_queries"] == [
        "一个未知关键词 舆情",
        "一个未知关键词 投诉",
        "一个未知关键词 争议",
        "一个未知关键词 官方回应",
    ]


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


def test_llm_redaction_helpers_report_presence_only() -> None:
    secret_value = "secret-value-should-not-appear"

    assert redact_api_key(secret_value) == "present"
    assert redact_api_key("") == "missing"
    redacted = redact_config_dict(
        {
            "LLM_PROVIDER": "openai",
            "OPENAI_API_KEY": secret_value,
            "nested": {
                "client_secret": secret_value,
                "access_token": secret_value,
                "safe_value": "visible",
            },
            "items": [{"QWEN_API_KEY": secret_value}],
        }
    )

    assert redacted == {
        "LLM_PROVIDER": "openai",
        "OPENAI_API_KEY": "present",
        "nested": {
            "client_secret": "present",
            "access_token": "present",
            "safe_value": "visible",
        },
        "items": [{"QWEN_API_KEY": "present"}],
    }
    assert secret_value not in str(redacted)


def test_llm_provider_diagnostics_default_to_mock(monkeypatch) -> None:
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("LLM_ENABLE_REAL_CALLS", raising=False)

    diagnostics = get_llm_provider_diagnostics()

    assert diagnostics.provider_name == "mock"
    assert diagnostics.real_calls_enabled is False
    assert diagnostics.api_key_present is False
    assert diagnostics.provider_status == "mock_ready"
    assert diagnostics.required_credentials == []
    assert diagnostics.credential_presence == {}


@pytest.mark.parametrize(
    ("provider_name", "credential_name"),
    [
        ("openai", "OPENAI_API_KEY"),
        ("deepseek", "DEEPSEEK_API_KEY"),
        ("qwen", "QWEN_API_KEY"),
    ],
)
def test_llm_provider_diagnostics_show_presence_only(monkeypatch, provider_name, credential_name) -> None:
    secret_value = f"{provider_name}-secret-value-should-not-appear"
    monkeypatch.setenv("LLM_ENABLE_REAL_CALLS", "false")
    monkeypatch.setenv(credential_name, secret_value)

    diagnostics = get_llm_provider_diagnostics(provider_name)

    assert diagnostics.provider_name == provider_name
    assert diagnostics.real_calls_enabled is False
    assert diagnostics.api_key_present is True
    assert diagnostics.provider_status == "provider_not_enabled"
    assert diagnostics.credential_presence == {credential_name: True}
    assert secret_value not in diagnostics.model_dump_json()


def test_llm_provider_diagnostics_missing_real_key_is_not_configured(monkeypatch) -> None:
    monkeypatch.setenv("LLM_ENABLE_REAL_CALLS", "true")
    monkeypatch.delenv("QWEN_API_KEY", raising=False)

    diagnostics = get_llm_provider_diagnostics("qwen")

    assert diagnostics.provider_name == "qwen"
    assert diagnostics.real_calls_enabled is True
    assert diagnostics.api_key_present is False
    assert diagnostics.provider_status == "not_configured"
    assert diagnostics.credential_presence == {"QWEN_API_KEY": False}


def test_llm_provider_diagnostics_unknown_provider_fails_safely(monkeypatch) -> None:
    monkeypatch.setenv("LLM_ENABLE_REAL_CALLS", "true")

    diagnostics = get_llm_provider_diagnostics("unknown-provider")

    assert diagnostics.provider_name == "unknown-provider"
    assert diagnostics.real_calls_enabled is True
    assert diagnostics.api_key_present is False
    assert diagnostics.provider_status == "unknown_provider"
    assert diagnostics.required_credentials == []
    assert diagnostics.credential_presence == {}


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
