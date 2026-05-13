from app.schemas.analysis import SentimentResult
from app.schemas.comment import CleanComment, UserAggregationResult
from app.services.bot_detection.bot_score_service import calculate_bot_scores
from app.services.nlp.sentiment_analyzer import SentimentAnalyzer
from app.services.nlp.topic_clusterer import SimpleKeywordEmbeddingProvider, TopicClusterer


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
