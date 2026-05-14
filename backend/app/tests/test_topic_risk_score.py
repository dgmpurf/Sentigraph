from app.schemas.analysis import BotImpactSummary, BotScore, SentimentResult, TopicCluster
from app.schemas.comment import CleanComment, RawComment
from app.schemas.propagation import PropagationEdge, PropagationMetrics, PropagationNode, PropagationResponse
from app.schemas.risk import TOPIC_RISK_MODEL_VERSION
from app.services.recommendation.report_builder import build_public_opinion_report
from app.services.scoring.topic_risk_score import calculate_topic_risk_score, risk_level_from_score


def _topic() -> TopicCluster:
    return TopicCluster(
        cluster_id="topic_001",
        topic="Product quality issues",
        summary="Quality issues dominate.",
        comment_count=10,
        average_sentiment_score=-0.7,
        representative_comments=["serious quality issues"],
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
        duplicate_count=10,
        semantic_similarity_group="sem_group_001",
        is_repeated_script=True,
        created_at_min="2026-05-13T10:00:00Z",
        created_at_max="2026-05-13T10:05:00Z",
    )


def _sentiment() -> SentimentResult:
    return SentimentResult(
        comment_id="clean_001",
        sentiment="negative",
        sentiment_score=-0.8,
        emotion_tags=["anger"],
        stance="opposing",
        confidence=0.9,
        reason="test",
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
        like_count=40,
        reply_count=12,
        share_count=4,
        created_at="2026-05-13T10:00:00Z",
        url="https://example.com/comment_001",
        raw_data={},
    )


def _propagation() -> PropagationResponse:
    return PropagationResponse(
        project_id="project_001",
        nodes=[
            PropagationNode(
                node_id="comment_001",
                type="comment",
                platform="reddit",
                content="serious quality issues",
                author_id="author_a",
                created_at="2026-05-13T10:00:00Z",
                sentiment_score=-0.8,
                influence_score=0.65,
            )
        ],
        edges=[PropagationEdge(source="post_001", target="comment_001", relation="reply", weight=0.5)],
        metrics=PropagationMetrics(
            depth=1,
            breadth=10,
            central_node_id="post_001",
            propagation_speed=0.7,
        ),
    )


def test_topic_risk_score_range_and_output_shape() -> None:
    result = calculate_topic_risk_score(
        [_topic()],
        clean_comments=[_clean_comment()],
        sentiment_results=[_sentiment()],
        bot_accounts=[
            BotScore(
                author_id="author_a",
                bot_probability=0.72,
                bot_reasons=["Repeated-script content detected"],
                influence_weight=1.0,
            )
        ],
        bot_impact=BotImpactSummary(suspected_bot_ratio=1.0, suspected_bot_comment_ratio=1.0),
        propagation=_propagation(),
        raw_comments=[_raw_comment()],
    )

    assert result.risk_model_version == TOPIC_RISK_MODEL_VERSION
    assert result.topic_risks
    topic_risk = result.topic_risks[0]
    assert 0 <= topic_risk.topic_risk_score <= 100
    assert topic_risk.topic_risk_score == topic_risk.risk_score
    assert topic_risk.topic_risk_level == topic_risk.risk_level
    assert topic_risk.topic_id == "topic_001"
    assert topic_risk.negative_ratio == 1.0
    assert topic_risk.risk_explanation


def test_topic_risk_level_mapping() -> None:
    assert risk_level_from_score(0) == "low"
    assert risk_level_from_score(39) == "low"
    assert risk_level_from_score(40) == "medium"
    assert risk_level_from_score(69) == "medium"
    assert risk_level_from_score(70) == "high"
    assert risk_level_from_score(84) == "high"
    assert risk_level_from_score(85) == "critical"
    assert risk_level_from_score(100) == "critical"


def test_topic_risk_missing_optional_fields_do_not_crash() -> None:
    result = calculate_topic_risk_score([_topic()])

    assert result.topic_risks
    assert result.topic_risks[0].topic == "Product quality issues"
    assert 0 <= result.overall_risk <= 100
    assert result.top_risk_topics


def test_topic_risk_overall_aggregation() -> None:
    first = _topic()
    second = TopicCluster(
        cluster_id="topic_002",
        topic="General discussion",
        summary="General discussion.",
        comment_count=2,
        average_sentiment_score=0.0,
        representative_comments=[],
    )

    result = calculate_topic_risk_score([first, second])

    expected = round(result.max_topic_risk * 0.65 + result.average_topic_risk * 0.35, 2)
    assert result.overall_risk == expected
    assert result.risk_level == risk_level_from_score(result.overall_risk)


def test_top_risk_topics_are_sorted_by_score_descending() -> None:
    high = TopicCluster(
        cluster_id="topic_high",
        topic="High risk topic",
        summary="High risk.",
        comment_count=20,
        average_sentiment_score=-0.9,
        representative_comments=[],
    )
    medium = TopicCluster(
        cluster_id="topic_medium",
        topic="Medium risk topic",
        summary="Medium risk.",
        comment_count=8,
        average_sentiment_score=-0.4,
        representative_comments=[],
    )
    low = TopicCluster(
        cluster_id="topic_low",
        topic="Low risk topic",
        summary="Low risk.",
        comment_count=1,
        average_sentiment_score=0.1,
        representative_comments=[],
    )

    result = calculate_topic_risk_score([low, medium, high])

    sorted_scores = [topic.topic_risk_score for topic in result.top_risk_topics]
    assert sorted_scores == sorted(sorted_scores, reverse=True)
    assert result.top_risk_topics[0].topic == "High risk topic"


def test_report_builder_includes_v1_5_topic_risk_fields_when_available() -> None:
    from app.schemas.analysis import AnalysisResultResponse, RiskBrief, SentimentSummary

    analysis = AnalysisResultResponse(
        project_id="project_001",
        summary="Mock result",
        sentiment=SentimentSummary(
            positive_ratio=0.0,
            neutral_ratio=0.0,
            negative_ratio=1.0,
            average_sentiment_score=-0.8,
        ),
        topics=[_topic()],
        conflicts=[],
        bot_score=BotImpactSummary(suspected_bot_ratio=1.0, suspected_bot_comment_ratio=1.0),
        risk=RiskBrief(risk_score=70, risk_level="high"),
        sentiment_results=[_sentiment()],
        ai_generated=[],
        bot_accounts=[],
    )
    topic_risk = calculate_topic_risk_score(
        [_topic()],
        clean_comments=[_clean_comment()],
        sentiment_results=[_sentiment()],
        bot_impact=BotImpactSummary(suspected_bot_ratio=1.0, suspected_bot_comment_ratio=1.0),
    )

    report = build_public_opinion_report(analysis, topic_risk_result=topic_risk)

    assert report.risk_model_version == TOPIC_RISK_MODEL_VERSION
    assert report.topic_risks
    assert report.top_risk_topics
    assert report.overall_risk == topic_risk.overall_risk
    assert report.real_crisis_risk == topic_risk.real_crisis_risk
    assert report.manipulation_risk == topic_risk.manipulation_risk
    assert any("V1.5" in finding for finding in report.key_findings)
