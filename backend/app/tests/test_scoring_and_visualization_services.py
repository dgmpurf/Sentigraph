from app.schemas.analysis import (
    AnalysisResultResponse,
    BotImpactSummary,
    ConflictResult,
    SentimentResult,
    SentimentSummary,
    TopicCluster,
)
from app.schemas.comment import CleanComment, RawComment
from app.schemas.propagation import PropagationEdge, PropagationMetrics, PropagationNode, PropagationResponse
from app.services.scoring.risk_score import calculate_risk_score
from app.services.visualization.chart_data_builder import (
    build_visualization_response,
    ensure_mongodb_safe_keys,
)


def _analysis_result() -> AnalysisResultResponse:
    sentiment = SentimentSummary(
        positive_ratio=0.1,
        neutral_ratio=0.2,
        negative_ratio=0.7,
        average_sentiment_score=-0.65,
    )
    topic = TopicCluster(
        cluster_id="topic_001",
        topic="Product quality issues",
        summary="Quality issues dominate.",
        comment_count=12,
        average_sentiment_score=-0.7,
        representative_comments=["serious quality issues"],
    )
    conflict = ConflictResult(
        conflict_id="conflict_001",
        side_a="Quality issue is real.",
        side_b="Competitor attack.",
        intensity=0.8,
        evidence_comments=["issue", "attack"],
    )
    bot = BotImpactSummary(suspected_bot_ratio=0.25, suspected_bot_comment_ratio=0.4)
    risk = calculate_risk_score(
        sentiment,
        bot,
        topics=[topic],
        conflicts=[conflict],
        propagation_speed=0.6,
        trend_shift=0.5,
    ).risk
    return AnalysisResultResponse(
        project_id="project_001",
        summary="Mock result",
        sentiment=sentiment,
        topics=[topic],
        conflicts=[conflict],
        bot_score=bot,
        risk=risk,
        sentiment_results=[
            SentimentResult(
                comment_id="clean_001",
                sentiment="negative",
                sentiment_score=-0.8,
                emotion_tags=["anger"],
                stance="opposing",
                confidence=0.9,
                reason="test",
            )
        ],
        ai_generated=[],
        bot_accounts=[],
    )


def _clean_comment() -> CleanComment:
    return CleanComment(
        clean_comment_id="clean_001",
        original_comment_ids=["comment_001"],
        platforms=["reddit"],
        post_ids=["post_001"],
        author_id="author_a",
        clean_text="serious quality issues",
        language="en",
        duplicate_group_id="dup_group_001",
        duplicate_count=3,
        semantic_similarity_group="sem_group_001",
        is_repeated_script=True,
        created_at_min="2026-05-13T10:00:00Z",
        created_at_max="2026-05-13T10:05:00Z",
    )


def _raw_comment() -> RawComment:
    return RawComment(
        platform="reddit",
        post_id="post_001",
        comment_id="comment_001",
        parent_id=None,
        author_id="author_a",
        author_name="anonymous_user",
        content="serious quality issues",
        like_count=12,
        reply_count=3,
        share_count=1,
        created_at="2026-05-13T10:00:00Z",
        url="https://example.com/comment_001",
        raw_data={},
    )


def _propagation() -> PropagationResponse:
    return PropagationResponse(
        project_id="project_001",
        nodes=[
            PropagationNode(
                node_id="post_001",
                type="post",
                platform="reddit",
                content="Original post",
                author_id="author_a",
                created_at="2026-05-13T10:00:00Z",
                sentiment_score=-0.7,
                influence_score=0.8,
            )
        ],
        edges=[PropagationEdge(source="post_001", target="comment_001", relation="reply", weight=0.5)],
        metrics=PropagationMetrics(
            depth=1,
            breadth=1,
            central_node_id="post_001",
            propagation_speed=0.6,
        ),
    )


def test_risk_score_returns_schema_compatible_level_and_factors() -> None:
    sentiment = SentimentSummary(
        positive_ratio=0.1,
        neutral_ratio=0.2,
        negative_ratio=0.7,
        average_sentiment_score=-0.65,
    )
    bot = BotImpactSummary(suspected_bot_ratio=0.25, suspected_bot_comment_ratio=0.4)

    result = calculate_risk_score(sentiment, bot, propagation_speed=0.6, trend_shift=0.5)

    assert result.risk.risk_score >= 50
    assert result.risk.risk_level in {"medium", "high", "critical"}
    assert result.factors.negative_sentiment_ratio == 0.7
    assert result.explanation


def test_chart_data_builder_outputs_visualization_schema() -> None:
    analysis = _analysis_result()
    risk_result = calculate_risk_score(
        analysis.sentiment,
        analysis.bot_score,
        topics=analysis.topics,
        conflicts=analysis.conflicts,
        propagation_speed=0.6,
        trend_shift=0.5,
    )

    visualization = build_visualization_response(
        "project_001",
        analysis,
        clean_comments=[_clean_comment()],
        raw_comments=[_raw_comment()],
        propagation=_propagation(),
        risk_result=risk_result,
    )

    assert visualization.project_id == "project_001"
    assert visualization.sentiment_trend[0].negative == 3
    assert visualization.heatmap[0].platform == "reddit"
    assert visualization.propagation_graph.nodes[0].node_id == "post_001"
    assert visualization.topic_clusters[0].name == "Product quality issues"
    assert visualization.risk_radar.bot_impact == 0.4


def test_ensure_mongodb_safe_keys_coerces_nested_keys_to_strings() -> None:
    result = ensure_mongodb_safe_keys({1: {"nested": [{2: "value"}]}})

    assert result == {"1": {"nested": [{"2": "value"}]}}
    assert all(isinstance(key, str) for key in result.keys())

