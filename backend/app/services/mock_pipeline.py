from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from app.schemas.analysis import AnalysisResultResponse, ConflictResult, SentimentResult
from app.schemas.comment import CleanComment, RawComment
from app.schemas.propagation import PropagationEdge, PropagationMetrics, PropagationNode, PropagationResponse
from app.schemas.risk import TopicRiskScoreResult
from app.schemas.visualization import VisualizationResponse
from app.services.bot_detection.bot_score_service import calculate_bot_scores
from app.services.nlp.sentiment_analyzer import SentimentAnalyzer
from app.services.nlp.topic_clusterer import TopicClusterer
from app.services.preprocessing.duplicate_detector import detect_duplicate_groups
from app.services.preprocessing.user_aggregator import aggregate_users
from app.services.scoring.risk_score import RiskScoreResult, calculate_risk_score
from app.services.scoring.topic_risk_score import calculate_topic_risk_score
from app.services.visualization.chart_data_builder import build_visualization_response


MOCK_DATA_DIR = Path(__file__).resolve().parents[3] / "mock_data"


@dataclass(frozen=True)
class MockPipelineResult:
    project_id: str
    raw_comments: list[RawComment]
    clean_comments: list[CleanComment]
    sentiment_results: list[SentimentResult]
    analysis: AnalysisResultResponse
    propagation: PropagationResponse
    risk_result: RiskScoreResult
    topic_risk_result: TopicRiskScoreResult


def build_mock_pipeline(
    project_id: str,
    *,
    platforms: list[str] | None = None,
) -> MockPipelineResult:
    raw_comments = _load_raw_comments(platforms)
    clean_comments = detect_duplicate_groups(raw_comments)

    sentiment_analyzer = SentimentAnalyzer()
    sentiment_results = sentiment_analyzer.analyze(clean_comments)
    sentiment_summary = sentiment_analyzer.summarize(sentiment_results)

    user_aggregates = aggregate_users(clean_comments, sentiment_results)
    bot_accounts, bot_impact = calculate_bot_scores(user_aggregates, clean_comments, sentiment_results)
    topics = TopicClusterer().cluster(clean_comments, sentiment_results)
    conflicts = _build_mock_conflicts(topics, clean_comments)
    propagation = build_mock_propagation(project_id, raw_comments, clean_comments, sentiment_results)
    trend_shift = _calculate_trend_shift(clean_comments, sentiment_results)
    risk_result = calculate_risk_score(
        sentiment_summary,
        bot_impact,
        topics=topics,
        conflicts=conflicts,
        propagation_speed=propagation.metrics.propagation_speed,
        trend_shift=trend_shift,
    )
    topic_risk_result = calculate_topic_risk_score(
        topics,
        clean_comments=clean_comments,
        sentiment_results=sentiment_results,
        bot_accounts=bot_accounts,
        bot_impact=bot_impact,
        propagation=propagation,
        raw_comments=raw_comments,
    )
    analysis = AnalysisResultResponse(
        project_id=project_id,
        summary=_build_analysis_summary(topic_risk_result.risk_level, topics),
        sentiment=sentiment_summary,
        topics=topics,
        conflicts=conflicts,
        bot_score=bot_impact,
        risk=risk_result.risk.model_copy(
            update={
                "risk_score": int(round(topic_risk_result.overall_risk)),
                "risk_level": topic_risk_result.risk_level,
            }
        ),
        sentiment_results=sentiment_results,
        ai_generated=[],
        bot_accounts=bot_accounts,
        risk_model_version=topic_risk_result.risk_model_version,
        topic_risks=topic_risk_result.topic_risks,
        top_risk_topics=topic_risk_result.top_risk_topics,
        max_topic_risk=topic_risk_result.max_topic_risk,
        average_topic_risk=topic_risk_result.average_topic_risk,
        overall_risk=topic_risk_result.overall_risk,
        real_crisis_risk=topic_risk_result.real_crisis_risk,
        manipulation_risk=topic_risk_result.manipulation_risk,
        risk_explanation=topic_risk_result.risk_explanation,
    )

    return MockPipelineResult(
        project_id=project_id,
        raw_comments=raw_comments,
        clean_comments=clean_comments,
        sentiment_results=sentiment_results,
        analysis=analysis,
        propagation=propagation,
        risk_result=risk_result,
        topic_risk_result=topic_risk_result,
    )


def build_pipeline_visualization(
    project_id: str,
    *,
    platforms: list[str] | None = None,
) -> VisualizationResponse:
    pipeline = build_mock_pipeline(project_id, platforms=platforms)
    return build_visualization_response(
        project_id,
        pipeline.analysis,
        clean_comments=pipeline.clean_comments,
        raw_comments=pipeline.raw_comments,
        propagation=pipeline.propagation,
        risk_result=pipeline.risk_result,
        topic_risk_result=pipeline.topic_risk_result,
    )


def build_pipeline_analysis(
    project_id: str,
    *,
    platforms: list[str] | None = None,
) -> AnalysisResultResponse:
    return build_mock_pipeline(project_id, platforms=platforms).analysis


def build_pipeline_propagation(
    project_id: str,
    *,
    platforms: list[str] | None = None,
) -> PropagationResponse:
    return build_mock_pipeline(project_id, platforms=platforms).propagation


def build_mock_propagation(
    project_id: str,
    raw_comments: list[RawComment],
    clean_comments: list[CleanComment],
    sentiment_results: list[SentimentResult],
) -> PropagationResponse:
    sentiment_by_raw_comment = _sentiment_by_raw_comment(clean_comments, sentiment_results)
    comments_by_post: dict[str, list[RawComment]] = defaultdict(list)
    for comment in raw_comments:
        comments_by_post[str(comment.post_id)].append(comment)

    nodes: list[PropagationNode] = []
    edges: list[PropagationEdge] = []

    for post_id, comments in sorted(comments_by_post.items()):
        first_comment = min(comments, key=lambda comment: comment.created_at)
        post_sentiment = _average(
            sentiment_by_raw_comment.get(comment.comment_id, 0.0) for comment in comments
        )
        post_influence = _normalized_interaction_score(comments)
        nodes.append(
            PropagationNode(
                node_id=post_id,
                type="post",
                platform=first_comment.platform,
                content=f"Mock source discussion for {post_id}",
                author_id=f"source_{post_id}",
                created_at=first_comment.created_at,
                sentiment_score=round(post_sentiment, 4),
                influence_score=round(post_influence, 4),
            )
        )

        raw_ids = {comment.comment_id for comment in comments}
        for comment in sorted(comments, key=lambda item: item.created_at):
            interactions = comment.like_count + comment.reply_count + comment.share_count
            nodes.append(
                PropagationNode(
                    node_id=comment.comment_id,
                    type="comment",
                    platform=comment.platform,
                    content=comment.content[:120],
                    author_id=comment.author_id,
                    created_at=comment.created_at,
                    sentiment_score=round(sentiment_by_raw_comment.get(comment.comment_id, 0.0), 4),
                    influence_score=round(min(1.0, max(0.05, interactions / 160)), 4),
                )
            )
            source = comment.parent_id if comment.parent_id in raw_ids else post_id
            edges.append(
                PropagationEdge(
                    source=source,
                    target=comment.comment_id,
                    relation="reply",
                    weight=round(min(1.0, max(0.1, (interactions + 1) / 100)), 4),
                )
            )

    central_node_id = _central_post_id(comments_by_post) or "post_001"
    metrics = PropagationMetrics(
        depth=2 if any(comment.parent_id for comment in raw_comments) else 1,
        breadth=len(raw_comments),
        central_node_id=central_node_id,
        propagation_speed=_propagation_speed(raw_comments),
    )
    return PropagationResponse(project_id=project_id, nodes=nodes, edges=edges, metrics=metrics)


def _load_raw_comments(platforms: list[str] | None = None) -> list[RawComment]:
    with (MOCK_DATA_DIR / "raw_comments.json").open("r", encoding="utf-8") as file:
        raw_data: list[dict[str, Any]] = json.load(file)
    selected_platforms = {platform.lower() for platform in platforms or []}
    comments = [RawComment(**item) for item in raw_data]
    if not selected_platforms:
        return comments
    filtered = [comment for comment in comments if comment.platform.lower() in selected_platforms]
    return filtered or comments


def _sentiment_by_raw_comment(
    clean_comments: list[CleanComment],
    sentiment_results: list[SentimentResult],
) -> dict[str, float]:
    sentiment_by_clean_comment = {
        result.comment_id: result.sentiment_score for result in sentiment_results
    }
    sentiment_by_raw: dict[str, float] = {}
    for comment in clean_comments:
        score = sentiment_by_clean_comment.get(comment.clean_comment_id, 0.0)
        for original_id in comment.original_comment_ids:
            sentiment_by_raw[str(original_id)] = score
    return sentiment_by_raw


def _build_mock_conflicts(
    topics: list,
    clean_comments: list[CleanComment],
) -> list[ConflictResult]:
    topic_names = {topic.topic for topic in topics}
    if "Product quality issues" not in topic_names and "Coordinated amplification" not in topic_names:
        return []

    evidence = [comment.clean_text for comment in clean_comments[:2]]
    return [
        ConflictResult(
            conflict_id="conflict_001",
            side_a="Users describe product or service issues as real incidents.",
            side_b="Other comments question whether the spread is coordinated amplification.",
            intensity=0.72,
            evidence_comments=evidence,
        )
    ]


def _build_analysis_summary(risk_level: str, topics: list) -> str:
    if topics:
        leading_topic = topics[0].topic.lower()
    else:
        leading_topic = "general discussion"
    return (
        f"Mock pipeline analysis rates the current project as {risk_level} risk, "
        f"with conversation concentrated around {leading_topic}."
    )


def _calculate_trend_shift(
    clean_comments: list[CleanComment],
    sentiment_results: list[SentimentResult],
) -> float:
    if len(clean_comments) < 2:
        return 0.0

    sentiment_by_comment = {
        result.comment_id: result.sentiment_score for result in sentiment_results
    }
    ordered = sorted(clean_comments, key=lambda comment: comment.created_at_min)
    midpoint = max(1, len(ordered) // 2)
    early = ordered[:midpoint]
    late = ordered[midpoint:]
    early_score = _average(sentiment_by_comment.get(comment.clean_comment_id, 0.0) for comment in early)
    late_score = _average(sentiment_by_comment.get(comment.clean_comment_id, 0.0) for comment in late)
    return round(min(1.0, abs(late_score - early_score)), 4)


def _propagation_speed(raw_comments: list[RawComment]) -> float:
    if len(raw_comments) < 2:
        return 0.0

    timestamps = [_parse_timestamp(comment.created_at) for comment in raw_comments]
    timestamps = [timestamp for timestamp in timestamps if timestamp is not None]
    if len(timestamps) < 2:
        return 0.0

    span_hours = max((max(timestamps) - min(timestamps)).total_seconds() / 3600, 0.25)
    comments_per_hour = len(raw_comments) / span_hours
    return round(min(1.0, comments_per_hour / 8), 4)


def _parse_timestamp(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _central_post_id(comments_by_post: dict[str, list[RawComment]]) -> str | None:
    if not comments_by_post:
        return None
    return max(comments_by_post.items(), key=lambda item: len(item[1]))[0]


def _normalized_interaction_score(comments: list[RawComment]) -> float:
    interactions = sum(comment.like_count + comment.reply_count + comment.share_count for comment in comments)
    return min(1.0, max(0.1, interactions / 220))


def _average(values) -> float:
    value_list = list(values)
    if not value_list:
        return 0.0
    return sum(value_list) / len(value_list)
