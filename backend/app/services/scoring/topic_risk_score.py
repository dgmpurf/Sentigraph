from __future__ import annotations

from math import log10

from app.schemas.analysis import BotImpactSummary, BotScore, SentimentResult, TopicCluster
from app.schemas.comment import CleanComment, RawComment
from app.schemas.propagation import PropagationResponse
from app.schemas.risk import TOPIC_RISK_MODEL_VERSION, TopicRiskScore, TopicRiskScoreResult
from app.services.nlp.topic_clusterer import TopicClusterer


def calculate_topic_risk_score(
    topics: list[TopicCluster] | None,
    *,
    clean_comments: list[CleanComment] | None = None,
    sentiment_results: list[SentimentResult] | None = None,
    bot_accounts: list[BotScore] | None = None,
    bot_impact: BotImpactSummary | None = None,
    propagation: PropagationResponse | None = None,
    raw_comments: list[RawComment] | None = None,
) -> TopicRiskScoreResult:
    """Calculate deterministic V1.5 topic-level risk from current mock pipeline outputs."""
    topic_list = topics or []
    if not topic_list:
        return TopicRiskScoreResult(risk_model_version=TOPIC_RISK_MODEL_VERSION)

    clean_list = clean_comments or []
    sentiment_by_comment = {result.comment_id: result for result in sentiment_results or []}
    bot_by_author = {score.author_id: score for score in bot_accounts or []}
    raw_by_id = {comment.comment_id: comment for comment in raw_comments or []}
    influence_by_node = {
        node.node_id: node.influence_score
        for node in (propagation.nodes if propagation else [])
    }
    topic_assignments = _comments_by_topic(clean_list)
    max_comment_count = max([max(topic.comment_count, 0) for topic in topic_list] or [0])
    propagation_speed = propagation.metrics.propagation_speed if propagation else 0.0
    global_bot_impact = bot_impact.suspected_bot_comment_ratio if bot_impact else 0.0

    topic_risks: list[TopicRiskScore] = []
    for topic in topic_list:
        topic_comments = topic_assignments.get(topic.topic, [])
        metrics = _topic_metrics(
            topic,
            topic_comments,
            sentiment_by_comment,
            bot_by_author,
            raw_by_id,
            influence_by_node,
            max_comment_count,
            propagation_speed,
            global_bot_impact,
        )
        topic_risks.append(metrics)

    topic_risks = sorted(
        topic_risks,
        key=lambda item: (-item.topic_risk_score, -item.comment_count, item.topic),
    )
    risk_scores = [item.topic_risk_score for item in topic_risks]
    max_topic_risk = _round_score(max(risk_scores) if risk_scores else 0.0)
    average_topic_risk = _round_score(sum(risk_scores) / len(risk_scores) if risk_scores else 0.0)
    overall_risk = _round_score(max_topic_risk * 0.65 + average_topic_risk * 0.35)
    real_crisis_risk = _aggregate_driver(
        [
            _round_score(
                topic.neg_severity * 45
                + topic.spread_signal * 20
                + topic.controversy_signal * 15
                + topic.influence_proxy * 20
            )
            for topic in topic_risks
        ]
    )
    manipulation_risk = _aggregate_driver([topic.bot_signal * 100 for topic in topic_risks])
    top_risk_topics = topic_risks[:3]

    return TopicRiskScoreResult(
        risk_model_version=TOPIC_RISK_MODEL_VERSION,
        topic_risks=topic_risks,
        top_risk_topics=top_risk_topics,
        max_topic_risk=max_topic_risk,
        average_topic_risk=average_topic_risk,
        overall_risk=overall_risk,
        risk_level=risk_level_from_score(overall_risk),
        real_crisis_risk=real_crisis_risk,
        manipulation_risk=manipulation_risk,
        risk_explanation=_overall_explanation(top_risk_topics, overall_risk, real_crisis_risk, manipulation_risk),
    )


def risk_level_from_score(score: float) -> str:
    if score >= 85:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def _comments_by_topic(clean_comments: list[CleanComment]) -> dict[str, list[CleanComment]]:
    clusterer = TopicClusterer()
    buckets: dict[str, list[CleanComment]] = {}
    for comment in clean_comments:
        topic = clusterer._assign_topic(comment.clean_text)
        buckets.setdefault(topic, []).append(comment)
    return buckets


def _topic_metrics(
    topic: TopicCluster,
    topic_comments: list[CleanComment],
    sentiment_by_comment: dict[str, SentimentResult],
    bot_by_author: dict[str, BotScore],
    raw_by_id: dict[str, RawComment],
    influence_by_node: dict[str, float],
    max_comment_count: int,
    propagation_speed: float,
    global_bot_impact: float,
) -> TopicRiskScore:
    comment_count = max(topic.comment_count, _weighted_comment_count(topic_comments), 0)
    weighted_total = max(_weighted_comment_count(topic_comments), 0)
    sentiment_values = _weighted_sentiment_values(topic_comments, sentiment_by_comment)

    if sentiment_values:
        weighted_score_total = sum(score * weight for score, weight, _label in sentiment_values)
        weighted_count = sum(weight for _score, weight, _label in sentiment_values)
        average_sentiment_score = weighted_score_total / max(weighted_count, 1)
        negative_ratio = sum(weight for _score, weight, label in sentiment_values if label == "negative") / max(
            weighted_count,
            1,
        )
        positive_ratio = sum(weight for _score, weight, label in sentiment_values if label == "positive") / max(
            weighted_count,
            1,
        )
    else:
        average_sentiment_score = topic.average_sentiment_score
        negative_ratio = _fallback_negative_ratio(topic.average_sentiment_score)
        positive_ratio = max(0.0, topic.average_sentiment_score)

    negative_strength = _clamp(abs(min(average_sentiment_score, 0.0)))
    if negative_ratio > 0 and negative_strength <= 0:
        negative_strength = 0.2
    neg_severity = _clamp(negative_ratio * negative_strength)
    spread_signal = _clamp(
        _volume_signal(comment_count, max_comment_count) * 0.7
        + propagation_speed * 0.3
    )
    controversy_signal = _clamp(4 * positive_ratio * negative_ratio)
    repeated_ratio = _repeated_script_ratio(topic_comments)
    account_bot_signal = _account_bot_signal(topic_comments, bot_by_author)
    bot_signal = _clamp(repeated_ratio * 0.45 + account_bot_signal * 0.35 + global_bot_impact * 0.2)
    influence_proxy = _influence_proxy(topic_comments, raw_by_id, influence_by_node, comment_count)

    topic_risk_score = _round_score(
        neg_severity * 35
        + spread_signal * 20
        + controversy_signal * 15
        + bot_signal * 15
        + influence_proxy * 15
    )
    topic_risk_level = risk_level_from_score(topic_risk_score)

    return TopicRiskScore(
        topic_id=topic.cluster_id,
        cluster_id=topic.cluster_id,
        topic=topic.topic,
        comment_count=int(comment_count),
        negative_ratio=round(_clamp(negative_ratio), 4),
        average_sentiment_score=round(average_sentiment_score, 4),
        neg_severity=round(neg_severity, 4),
        spread_signal=round(spread_signal, 4),
        controversy_signal=round(controversy_signal, 4),
        bot_signal=round(bot_signal, 4),
        influence_proxy=round(influence_proxy, 4),
        topic_risk_score=topic_risk_score,
        topic_risk_level=topic_risk_level,
        risk_explanation=_topic_explanation(
            topic.topic,
            topic_risk_score,
            neg_severity,
            spread_signal,
            controversy_signal,
            bot_signal,
            influence_proxy,
        ),
        risk_score=topic_risk_score,
        risk_level=topic_risk_level,
    )


def _weighted_sentiment_values(
    topic_comments: list[CleanComment],
    sentiment_by_comment: dict[str, SentimentResult],
) -> list[tuple[float, int, str]]:
    values: list[tuple[float, int, str]] = []
    for comment in topic_comments:
        result = sentiment_by_comment.get(comment.clean_comment_id)
        if result:
            values.append((result.sentiment_score, max(comment.duplicate_count, 1), result.sentiment))
    return values


def _weighted_comment_count(comments: list[CleanComment]) -> int:
    return sum(max(comment.duplicate_count, 1) for comment in comments)


def _fallback_negative_ratio(average_sentiment_score: float) -> float:
    if average_sentiment_score < 0:
        return _clamp(abs(average_sentiment_score))
    return 0.0


def _volume_signal(comment_count: int, max_comment_count: int) -> float:
    if comment_count <= 0 or max_comment_count <= 0:
        return 0.0
    return _clamp(comment_count / max_comment_count)


def _repeated_script_ratio(comments: list[CleanComment]) -> float:
    total = _weighted_comment_count(comments)
    if total <= 0:
        return 0.0
    repeated = sum(max(comment.duplicate_count, 1) for comment in comments if comment.is_repeated_script)
    return _clamp(repeated / total)


def _account_bot_signal(comments: list[CleanComment], bot_by_author: dict[str, BotScore]) -> float:
    weighted_total = _weighted_comment_count(comments)
    if weighted_total <= 0:
        return 0.0
    weighted_probability = 0.0
    for comment in comments:
        bot_score = bot_by_author.get(comment.author_id)
        if bot_score:
            weighted_probability += bot_score.bot_probability * max(comment.duplicate_count, 1)
    return _clamp(weighted_probability / weighted_total)


def _influence_proxy(
    comments: list[CleanComment],
    raw_by_id: dict[str, RawComment],
    influence_by_node: dict[str, float],
    comment_count: int,
) -> float:
    interaction_values: list[int] = []
    influence_values: list[float] = []
    for comment in comments:
        for original_id in comment.original_comment_ids:
            raw = raw_by_id.get(original_id)
            if raw:
                interaction_values.append(raw.like_count + raw.reply_count + raw.share_count)
            if original_id in influence_by_node:
                influence_values.append(influence_by_node[original_id])

    if interaction_values or influence_values:
        average_interaction = sum(interaction_values) / len(interaction_values) if interaction_values else 0.0
        average_influence = sum(influence_values) / len(influence_values) if influence_values else 0.0
        return _clamp(min(1.0, average_interaction / 120) * 0.7 + average_influence * 0.3)

    if comment_count <= 0:
        return 0.0
    return _clamp(log10(comment_count + 1) / 2)


def _aggregate_driver(scores: list[float]) -> float:
    if not scores:
        return 0.0
    max_score = max(scores)
    average_score = sum(scores) / len(scores)
    return _round_score(max_score * 0.65 + average_score * 0.35)


def _topic_explanation(
    topic: str,
    score: float,
    neg_severity: float,
    spread_signal: float,
    controversy_signal: float,
    bot_signal: float,
    influence_proxy: float,
) -> str:
    drivers = {
        "negative severity": neg_severity,
        "spread": spread_signal,
        "controversy": controversy_signal,
        "bot/repeated-script signal": bot_signal,
        "influence": influence_proxy,
    }
    top_driver = max(drivers.items(), key=lambda item: item[1])[0]
    return f"{topic} has topic risk {score:.1f}/100, mainly driven by {top_driver}."


def _overall_explanation(
    top_risk_topics: list[TopicRiskScore],
    overall_risk: float,
    real_crisis_risk: float,
    manipulation_risk: float,
) -> str:
    if not top_risk_topics:
        return "No topic-level risk signal crossed the V1.5 mock threshold."
    leading = top_risk_topics[0]
    return (
        f"V1.5 topic risk is {overall_risk:.1f}/100. "
        f"The leading risk topic is {leading.topic} ({leading.topic_risk_score:.1f}/100). "
        f"Real-crisis signal is {real_crisis_risk:.1f}/100 and manipulation signal is "
        f"{manipulation_risk:.1f}/100."
    )


def _round_score(value: float) -> float:
    return round(_clamp(value, 0.0, 100.0), 2)


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, float(value)))

