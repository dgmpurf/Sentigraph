import pytest

from app.schemas.analysis import SentimentResult
from app.schemas.comment import CleanComment, UserAggregationResult
from app.schemas.risk import TOPIC_RISK_MODEL_VERSION
from app.services.bot_detection.bot_score_service import calculate_bot_scores
from app.services.llm.errors import LLMProviderError
from app.services.llm.schemas import LLMSentimentResult
from app.services.mock_pipeline import build_mock_pipeline, build_pipeline_analysis
from app.services.nlp import sentiment_analyzer as sentiment_module
from app.services.nlp.sentiment_analyzer import (
    FUTURE_REAL_LLM_MODE,
    MOCK_LLM_MODE,
    RULE_BASED_MODE,
    SentimentAnalyzer,
    get_sentiment_analyzer_mode,
)
from app.services.nlp.topic_clusterer import SimpleKeywordEmbeddingProvider, TopicClusterer
from app.services.recommendation.report_builder import build_public_opinion_report


def _clean_comment(
    clean_id: str,
    author_id: str,
    text: str,
    duplicate_count: int = 1,
    is_repeated_script: bool = False,
) -> CleanComment:
    return CleanComment(
        clean_comment_id=clean_id,
        original_comment_ids=[clean_id.replace("clean", "comment")],
        platforms=["reddit"],
        post_ids=["post_001"],
        author_id=author_id,
        clean_text=text,
        language="zh" if "\u95ee\u9898" in text else "en",
        duplicate_group_id="dup_group_001" if duplicate_count > 1 else None,
        duplicate_count=duplicate_count,
        semantic_similarity_group="sem_group_001",
        is_repeated_script=is_repeated_script,
        created_at_min="2026-05-13T10:00:00Z",
        created_at_max="2026-05-13T10:05:00Z",
    )


def test_sentiment_analyzer_mock_mode_outputs_schema_values() -> None:
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_comment(
        _clean_comment("clean_001", "author_a", "this product has serious quality issues")
    )

    assert result.comment_id == "clean_001"
    assert result.sentiment == "negative"
    assert result.stance == "opposing"
    assert result.sentiment_score < 0
    assert result.confidence > 0


def test_sentiment_analyzer_defaults_to_rule_based_mode(monkeypatch) -> None:
    monkeypatch.delenv("SENTIMENT_ANALYZER_MODE", raising=False)

    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_comment(
        _clean_comment("clean_001", "author_a", "this product has serious quality issues")
    )

    assert get_sentiment_analyzer_mode() == RULE_BASED_MODE
    assert analyzer.mode == RULE_BASED_MODE
    assert result.sentiment == "negative"
    assert result.reason == "Rule-based mock analysis found 3 negative signal(s)."


def test_sentiment_analyzer_keeps_legacy_mock_alias() -> None:
    analyzer = SentimentAnalyzer(mode="mock")

    assert analyzer.mode == RULE_BASED_MODE


def test_sentiment_analyzer_unknown_mode_falls_back_to_rule_based() -> None:
    comment = _clean_comment("clean_001", "author_a", "this product has serious quality issues")

    fallback = SentimentAnalyzer(mode="not_a_mode")
    rule_based = SentimentAnalyzer(mode=RULE_BASED_MODE).analyze_comment(comment)

    assert get_sentiment_analyzer_mode("not_a_mode") == RULE_BASED_MODE
    assert fallback.mode == RULE_BASED_MODE
    assert fallback.analyze_comment(comment).model_dump() == rule_based.model_dump()


def test_rule_based_mode_does_not_use_llm_provider(monkeypatch) -> None:
    monkeypatch.setenv("SENTIMENT_ANALYZER_MODE", RULE_BASED_MODE)
    monkeypatch.setattr(
        sentiment_module,
        "get_llm_provider",
        lambda: pytest.fail("rule_based mode must not call the LLM provider factory"),
    )

    result = SentimentAnalyzer().analyze_comment(
        _clean_comment("clean_001", "author_a", "this product has serious quality issues")
    )

    assert result.sentiment == "negative"
    assert result.reason.startswith("Rule-based mock analysis")


def test_sentiment_analyzer_mock_llm_mode_uses_provider_factory(monkeypatch) -> None:
    calls: list[tuple[str, str]] = []

    class RecordingMockProvider:
        provider_id = "mock"

        def analyze_sentiment(self, text: str, language: str = "auto") -> LLMSentimentResult:
            calls.append((text, language))
            return LLMSentimentResult(
                sentiment="negative",
                sentiment_score=-0.42,
                emotion_tags=["anger", "disappointment"],
                stance="opposing",
                confidence=0.77,
                reason="recording mock provider",
                language=language,
                provider="mock",
            )

    monkeypatch.setenv("SENTIMENT_ANALYZER_MODE", MOCK_LLM_MODE)
    monkeypatch.setattr(sentiment_module, "get_llm_provider", lambda: RecordingMockProvider())
    comment = _clean_comment("clean_001", "author_a", "this product has serious quality issues")

    result = SentimentAnalyzer().analyze_comment(comment)

    assert calls == [(comment.clean_text, "auto")]
    assert result.comment_id == "clean_001"
    assert result.sentiment == "negative"
    assert result.sentiment_score == -0.42
    assert result.reason == "recording mock provider"


def test_sentiment_analyzer_mock_llm_mode_is_deterministic(monkeypatch) -> None:
    monkeypatch.setenv("SENTIMENT_ANALYZER_MODE", MOCK_LLM_MODE)
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    comment = _clean_comment("clean_001", "author_a", "this product has serious quality issues")

    first = SentimentAnalyzer().analyze_comment(comment)
    second = SentimentAnalyzer().analyze_comment(comment)

    assert first.model_dump() == second.model_dump()
    assert first.sentiment == "negative"
    assert first.reason == "Deterministic mock provider used keyword sentiment signals only."


def test_mock_llm_mode_handles_chinese_and_neutral_text(monkeypatch) -> None:
    monkeypatch.setenv("SENTIMENT_ANALYZER_MODE", MOCK_LLM_MODE)
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    chinese_comment = _clean_comment(
        "clean_zh",
        "author_cn",
        "\u8fd9\u4e2a\u4ea7\u54c1\u8d28\u91cf\u95ee\u9898\u592a\u4e25\u91cd",
    )
    neutral_comment = _clean_comment("clean_neutral", "author_n", "Users are discussing the topic.")

    chinese_result = SentimentAnalyzer().analyze_comment(chinese_comment)
    neutral_result = SentimentAnalyzer().analyze_comment(neutral_comment)

    expected_fields = {
        "comment_id",
        "sentiment",
        "sentiment_score",
        "emotion_tags",
        "stance",
        "confidence",
        "reason",
    }
    assert set(chinese_result.model_dump()) == expected_fields
    assert chinese_result.sentiment == "negative"
    assert chinese_result.stance == "opposing"
    assert neutral_result.sentiment == "neutral"
    assert neutral_result.stance == "neutral"
    assert neutral_result.reason == "Deterministic mock provider used keyword sentiment signals only."


def test_future_real_llm_mode_never_calls_provider_factory(monkeypatch) -> None:
    monkeypatch.setenv("SENTIMENT_ANALYZER_MODE", FUTURE_REAL_LLM_MODE)
    monkeypatch.setattr(
        sentiment_module,
        "get_llm_provider",
        lambda: pytest.fail("future_real_llm placeholder must not call a provider"),
    )

    result = SentimentAnalyzer().analyze_comment(
        _clean_comment("clean_001", "author_a", "this product has serious quality issues")
    )

    assert result.sentiment == "negative"
    assert result.reason.startswith("Rule-based mock analysis")


def test_mock_llm_missing_real_provider_keys_do_not_crash(monkeypatch) -> None:
    monkeypatch.setenv("SENTIMENT_ANALYZER_MODE", MOCK_LLM_MODE)
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("LLM_ENABLE_REAL_CALLS", "true")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = SentimentAnalyzer().analyze_comment(
        _clean_comment("clean_001", "author_a", "this product has serious quality issues")
    )

    assert result.sentiment == "negative"
    assert result.reason == "Deterministic mock provider used keyword sentiment signals only."


def test_mock_llm_failure_falls_back_to_rule_based(monkeypatch) -> None:
    class BrokenMockProvider:
        provider_id = "mock"

        def analyze_sentiment(self, text: str, language: str = "auto") -> LLMSentimentResult:
            raise LLMProviderError("mock failure", provider="mock")

    comment = _clean_comment("clean_001", "author_a", "this product has serious quality issues")
    rule_based = SentimentAnalyzer(mode=RULE_BASED_MODE).analyze_comment(comment)
    monkeypatch.setenv("SENTIMENT_ANALYZER_MODE", MOCK_LLM_MODE)
    monkeypatch.setattr(sentiment_module, "get_llm_provider", lambda: BrokenMockProvider())

    result = SentimentAnalyzer().analyze_comment(comment)

    assert result.model_dump() == rule_based.model_dump()


def test_sentiment_summary_ratios_are_deterministic() -> None:
    analyzer = SentimentAnalyzer()
    results = analyzer.analyze(
        [
            _clean_comment("clean_001", "author_a", "serious issues and defects"),
            _clean_comment("clean_002", "author_b", "great support and trust"),
            _clean_comment("clean_003", "author_c", "plain observation"),
        ]
    )
    summary = analyzer.summarize(results)

    assert summary.negative_ratio == 0.3333
    assert summary.positive_ratio == 0.3333
    assert summary.neutral_ratio == 0.3333


def test_analysis_pipeline_still_produces_v1_5_topic_risk(monkeypatch) -> None:
    monkeypatch.delenv("SENTIMENT_ANALYZER_MODE", raising=False)

    analysis = build_pipeline_analysis("project_sentiment_mode")

    assert analysis.risk_model_version == TOPIC_RISK_MODEL_VERSION
    assert analysis.topic_risks
    assert analysis.sentiment_results


def test_report_builder_still_works_with_default_sentiment_mode(monkeypatch) -> None:
    monkeypatch.delenv("SENTIMENT_ANALYZER_MODE", raising=False)

    pipeline = build_mock_pipeline("project_sentiment_report")
    report = build_public_opinion_report(
        pipeline.analysis,
        topic_risk_result=pipeline.topic_risk_result,
    )

    assert report.generated_from_mock_pipeline is True
    assert report.risk_model_version == TOPIC_RISK_MODEL_VERSION
    assert report.overall_summary


def test_topic_clusterer_has_embedding_compatible_interface() -> None:
    provider = SimpleKeywordEmbeddingProvider()
    vector = provider.embed("quality issue and official response")
    clusters = TopicClusterer(embedding_provider=provider).cluster(
        [
            _clean_comment("clean_001", "author_a", "quality issue defect"),
            _clean_comment("clean_002", "author_b", "official response silence"),
        ]
    )

    assert len(vector) >= 4
    assert {cluster.topic for cluster in clusters} == {
        "Product quality issues",
        "Delayed official response",
    }
    assert all(cluster.cluster_id.startswith("topic_") for cluster in clusters)


def test_bot_score_service_uses_rule_based_features() -> None:
    comments = [
        _clean_comment("clean_001", "author_a", "same script", duplicate_count=8, is_repeated_script=True),
        _clean_comment("clean_002", "author_b", "normal comment", duplicate_count=1),
    ]
    aggregates = [
        UserAggregationResult(
            author_id="author_a",
            platforms=["reddit"],
            comment_count=8,
            unique_comment_count=1,
            duplicate_comment_ratio=0.875,
            average_sentiment_score=-0.7,
            first_seen_at="2026-05-13T10:00:00Z",
            last_seen_at="2026-05-13T10:05:00Z",
        ),
        UserAggregationResult(
            author_id="author_b",
            platforms=["reddit"],
            comment_count=1,
            unique_comment_count=1,
            duplicate_comment_ratio=0.0,
            average_sentiment_score=0.0,
            first_seen_at="2026-05-13T11:00:00Z",
            last_seen_at="2026-05-13T11:00:00Z",
        ),
    ]
    sentiment_results = [
        SentimentResult(
            comment_id="clean_001",
            sentiment="negative",
            sentiment_score=-0.85,
            emotion_tags=["anger"],
            stance="opposing",
            confidence=0.9,
            reason="test",
        ),
        SentimentResult(
            comment_id="clean_002",
            sentiment="neutral",
            sentiment_score=0.0,
            emotion_tags=["uncertainty"],
            stance="neutral",
            confidence=0.6,
            reason="test",
        ),
    ]

    scores, impact = calculate_bot_scores(aggregates, comments, sentiment_results)

    assert scores[0].author_id == "author_a"
    assert scores[0].bot_probability >= 0.6
    assert "High repeated content ratio" in scores[0].bot_reasons
    assert "Highly uniform sentiment pattern" in scores[0].bot_reasons
    assert impact.suspected_bot_ratio == 0.5
    assert impact.suspected_bot_comment_ratio == 0.8889
