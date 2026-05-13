from collections import defaultdict
from typing import Any

from app.schemas.analysis import AnalysisResultResponse, SentimentResult
from app.schemas.comment import CleanComment, RawComment
from app.schemas.propagation import PropagationEdge, PropagationNode, PropagationResponse
from app.schemas.visualization import (
    BotImpactVisualization,
    HeatmapPoint,
    RiskRadar,
    SentimentTrendPoint,
    VisualizationGraph,
    VisualizationResponse,
    VisualizationTopicCluster,
)
from app.services.scoring.risk_score import RiskScoreResult


def build_visualization_response(
    project_id: str,
    analysis: AnalysisResultResponse,
    *,
    clean_comments: list[CleanComment] | None = None,
    raw_comments: list[RawComment] | None = None,
    propagation: PropagationResponse | None = None,
    risk_result: RiskScoreResult | None = None,
) -> VisualizationResponse:
    risk_score = risk_result.risk.risk_score if risk_result else analysis.risk.risk_score
    risk_level = risk_result.risk.risk_level if risk_result else analysis.risk.risk_level

    return VisualizationResponse(
        project_id=project_id,
        risk_score=risk_score,
        risk_level=risk_level,
        sentiment_trend=build_sentiment_trend(clean_comments or [], analysis.sentiment_results),
        risk_radar=build_risk_radar(analysis, risk_result),
        heatmap=build_heatmap(raw_comments or []),
        propagation_graph=build_propagation_graph(propagation),
        topic_clusters=[
            VisualizationTopicCluster(
                name=topic.topic,
                value=topic.comment_count,
                sentiment_score=topic.average_sentiment_score,
            )
            for topic in analysis.topics
        ],
        bot_impact=BotImpactVisualization(**analysis.bot_score.model_dump()),
    )


def build_sentiment_trend(
    clean_comments: list[CleanComment],
    sentiment_results: list[SentimentResult],
) -> list[SentimentTrendPoint]:
    if not clean_comments or not sentiment_results:
        return []
    sentiment_by_comment = {result.comment_id: result.sentiment for result in sentiment_results}
    buckets: dict[str, dict[str, int]] = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0})
    for comment in clean_comments:
        bucket = comment.created_at_min[:13] + ":00:00Z"
        sentiment = sentiment_by_comment.get(comment.clean_comment_id, "neutral")
        key = sentiment if sentiment in {"positive", "negative"} else "neutral"
        buckets[bucket][key] += comment.duplicate_count
    return [
        SentimentTrendPoint(time=time, **counts)
        for time, counts in sorted(buckets.items())
    ]


def build_risk_radar(analysis: AnalysisResultResponse, risk_result: RiskScoreResult | None = None) -> RiskRadar:
    if risk_result:
        factors = risk_result.factors
        return RiskRadar(
            negative_sentiment=factors.negative_sentiment_ratio,
            bot_impact=factors.bot_impact_score,
            propagation_speed=factors.propagation_speed,
            controversy=factors.controversy_score,
            trend_shift=factors.trend_shift,
        )
    controversy = max([conflict.intensity for conflict in analysis.conflicts] or [0.0])
    return RiskRadar(
        negative_sentiment=analysis.sentiment.negative_ratio,
        bot_impact=analysis.bot_score.suspected_bot_comment_ratio,
        propagation_speed=0.0,
        controversy=controversy,
        trend_shift=0.0,
    )


def build_heatmap(raw_comments: list[RawComment]) -> list[HeatmapPoint]:
    buckets: dict[tuple[str, str], int] = defaultdict(int)
    for comment in raw_comments:
        time_bucket = comment.created_at[11:16]
        key = (str(comment.platform), str(time_bucket))
        buckets[key] += max(1, comment.like_count + comment.reply_count + comment.share_count)
    return [
        HeatmapPoint(platform=platform, time_bucket=time_bucket, intensity=min(100, intensity))
        for (platform, time_bucket), intensity in sorted(buckets.items())
    ]


def build_propagation_graph(propagation: PropagationResponse | None) -> VisualizationGraph:
    if not propagation:
        return VisualizationGraph(nodes=[], edges=[])
    nodes = [PropagationNode(**node.model_dump()) for node in propagation.nodes]
    edges = [PropagationEdge(**edge.model_dump()) for edge in propagation.edges]
    return VisualizationGraph(nodes=nodes, edges=edges)


def ensure_mongodb_safe_keys(value: Any) -> Any:
    """Recursively coerce dictionary keys to strings for MongoDB compatibility."""
    if isinstance(value, dict):
        return {str(key): ensure_mongodb_safe_keys(inner_value) for key, inner_value in value.items()}
    if isinstance(value, list):
        return [ensure_mongodb_safe_keys(item) for item in value]
    return value

