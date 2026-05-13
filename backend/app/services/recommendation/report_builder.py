from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.analysis import AnalysisResultResponse, BotScore, TopicCluster
from app.schemas.propagation import PropagationResponse
from app.schemas.visualization import VisualizationResponse


class PublicOpinionReport(BaseModel):
    overall_summary: str
    main_risk_factors: list[str] = Field(default_factory=list)
    top_negative_topics: list[str] = Field(default_factory=list)
    representative_comments: list[str] = Field(default_factory=list)
    suspected_bot_signals: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    suggested_public_response: str


def build_public_opinion_report(
    analysis: AnalysisResultResponse,
    *,
    visualization: VisualizationResponse | None = None,
    propagation: PropagationResponse | None = None,
    risk_factors: Any | None = None,
    representative_comments: list[str] | None = None,
    include_representative_comments: bool = True,
    user_type: str = "brand",
    tone: str = "professional",
) -> PublicOpinionReport:
    """Build a deterministic offline public opinion report from pipeline outputs."""
    factor_values = _risk_factor_values(risk_factors, visualization)
    top_negative_topics = _top_negative_topics(analysis.topics)
    bot_signals = _bot_signals(analysis.bot_accounts, analysis.bot_score.suspected_bot_comment_ratio)
    comments = _representative_comments(
        explicit_comments=representative_comments or [],
        topics=analysis.topics,
        include=include_representative_comments,
    )
    main_risk_factors = _main_risk_factors(analysis, factor_values, visualization, propagation)
    actions = _recommended_actions(
        risk_level=analysis.risk.risk_level,
        factors=factor_values,
        top_negative_topics=top_negative_topics,
        bot_signals=bot_signals,
        user_type=user_type,
    )

    return PublicOpinionReport(
        overall_summary=_overall_summary(analysis, factor_values, visualization, propagation),
        main_risk_factors=main_risk_factors,
        top_negative_topics=top_negative_topics,
        representative_comments=comments,
        suspected_bot_signals=bot_signals,
        recommended_actions=actions,
        suggested_public_response=_suggested_public_response(
            risk_level=analysis.risk.risk_level,
            top_negative_topics=top_negative_topics,
            tone=tone,
        ),
    )


def _overall_summary(
    analysis: AnalysisResultResponse,
    factor_values: dict[str, float],
    visualization: VisualizationResponse | None,
    propagation: PropagationResponse | None,
) -> str:
    leading_topic = analysis.topics[0].topic if analysis.topics else "general discussion"
    trend_points = len(visualization.sentiment_trend) if visualization else 0
    graph_nodes = len(propagation.nodes) if propagation else len(visualization.propagation_graph.nodes) if visualization else 0
    return (
        f"Public opinion risk is {analysis.risk.risk_level} at {analysis.risk.risk_score}/100. "
        f"Negative sentiment is {_format_percent(analysis.sentiment.negative_ratio)}, "
        f"with the strongest discussion around {leading_topic}. "
        f"The offline mock pipeline observed {trend_points} sentiment time bucket(s) "
        f"and {graph_nodes} propagation node(s). "
        f"Key risk pressure is {_dominant_factor_label(factor_values)}."
    )


def _main_risk_factors(
    analysis: AnalysisResultResponse,
    factor_values: dict[str, float],
    visualization: VisualizationResponse | None,
    propagation: PropagationResponse | None,
) -> list[str]:
    factors: list[str] = []
    if analysis.sentiment.negative_ratio >= 0.5:
        factors.append(f"Negative sentiment is elevated at {_format_percent(analysis.sentiment.negative_ratio)}.")
    elif analysis.sentiment.negative_ratio > 0:
        factors.append(f"Negative sentiment is present at {_format_percent(analysis.sentiment.negative_ratio)}.")

    if factor_values.get("bot_impact", 0.0) >= 0.3:
        factors.append(f"Bot-like comment impact is {_format_percent(factor_values['bot_impact'])}.")
    elif analysis.bot_score.suspected_bot_comment_ratio > 0:
        factors.append(
            "Suspected automated participation is visible at "
            f"{_format_percent(analysis.bot_score.suspected_bot_comment_ratio)} of comments."
        )

    if factor_values.get("propagation_speed", 0.0) >= 0.5:
        factors.append(f"Propagation speed is high at {_format_percent(factor_values['propagation_speed'])}.")

    if factor_values.get("controversy", 0.0) >= 0.5:
        factors.append(f"Controversy signal is {_format_percent(factor_values['controversy'])}.")

    if visualization and visualization.heatmap:
        peak = max(visualization.heatmap, key=lambda item: item.intensity)
        factors.append(f"Conversation intensity peaks on {peak.platform} at {peak.time_bucket}.")

    if propagation and propagation.metrics.breadth:
        factors.append(f"Propagation breadth covers {propagation.metrics.breadth} public interaction node(s).")

    return _dedupe_preserve_order(factors)[:6] or ["No major risk factor crossed the current mock threshold."]


def _top_negative_topics(topics: list[TopicCluster]) -> list[str]:
    sorted_topics = sorted(
        topics,
        key=lambda topic: (topic.average_sentiment_score, -topic.comment_count, topic.topic),
    )
    negative_topics = [
        (
            f"{topic.topic}: {topic.comment_count} comment(s), "
            f"average sentiment {topic.average_sentiment_score:.2f}"
        )
        for topic in sorted_topics
        if topic.average_sentiment_score < 0
    ]
    if negative_topics:
        return negative_topics[:3]

    return [
        f"{topic.topic}: {topic.comment_count} comment(s), average sentiment {topic.average_sentiment_score:.2f}"
        for topic in sorted(topics, key=lambda topic: (-topic.comment_count, topic.topic))[:3]
    ]


def _representative_comments(
    *,
    explicit_comments: list[str],
    topics: list[TopicCluster],
    include: bool,
) -> list[str]:
    if not include:
        return []

    candidates: list[str] = [comment for comment in explicit_comments if comment]
    for topic in topics:
        candidates.extend(comment for comment in topic.representative_comments if comment)

    return _dedupe_preserve_order(candidates)[:5]


def _bot_signals(bot_accounts: list[BotScore], suspected_bot_comment_ratio: float) -> list[str]:
    signals: list[str] = []
    if suspected_bot_comment_ratio > 0:
        signals.append(f"Suspected bot comment ratio is {_format_percent(suspected_bot_comment_ratio)}.")

    for account in sorted(bot_accounts, key=lambda item: item.bot_probability, reverse=True)[:3]:
        if account.bot_probability < 0.3:
            continue
        reasons = ", ".join(account.bot_reasons[:2])
        signals.append(
            f"{account.author_id} has bot probability {_format_percent(account.bot_probability)}"
            f" due to {reasons}."
        )

    return signals or ["No strong bot-like account signal crossed the mock threshold."]


def _recommended_actions(
    *,
    risk_level: str,
    factors: dict[str, float],
    top_negative_topics: list[str],
    bot_signals: list[str],
    user_type: str,
) -> list[str]:
    actions = [
        "Publish a factual monitoring note that acknowledges the main concern without amplifying speculation.",
        "Prepare a concise FAQ for customer service and social media teams.",
    ]

    if risk_level in {"high", "critical"}:
        actions.insert(0, "Escalate to the crisis response owner and set a 24-hour public update window.")
    elif risk_level == "medium":
        actions.insert(0, "Assign an owner to watch the topic and prepare a same-day response draft.")

    if top_negative_topics:
        actions.append("Address the leading negative topic directly with verifiable facts and support options.")

    if factors.get("bot_impact", 0.0) >= 0.3 or any("bot" in signal.lower() for signal in bot_signals):
        actions.append("Separate organic complaints from repeated-script signals before deciding escalation tone.")

    if factors.get("propagation_speed", 0.0) >= 0.5:
        actions.append("Monitor the next two hourly buckets for acceleration before expanding the response scope.")

    if user_type in {"public_figure", "artist", "influencer"}:
        actions.append("Use a calm personal statement and avoid arguing with individual accounts.")
    else:
        actions.append("Keep the response brand-safe, specific, and aligned with support operations.")

    return _dedupe_preserve_order(actions)[:6]


def _suggested_public_response(
    *,
    risk_level: str,
    top_negative_topics: list[str],
    tone: str,
) -> str:
    topic_phrase = "the concerns being discussed"
    if top_negative_topics:
        topic_phrase = top_negative_topics[0].split(":", 1)[0].lower()

    opening = "We are aware of the recent discussion around"
    if tone == "empathetic":
        opening = "We understand the concern behind the recent discussion around"
    elif tone == "direct":
        opening = "We have seen the recent discussion around"

    urgency = "We are reviewing the information and will share verified updates as soon as possible."
    if risk_level in {"high", "critical"}:
        urgency = "We are prioritizing a review and will share verified updates within the next response window."

    return (
        f"{opening} {topic_phrase}. "
        f"{urgency} "
        "In the meantime, we encourage users to send specific cases through official support channels "
        "so they can be checked and handled accurately."
    )


def _risk_factor_values(
    risk_factors: Any | None,
    visualization: VisualizationResponse | None,
) -> dict[str, float]:
    if risk_factors is not None:
        if is_dataclass(risk_factors):
            raw = asdict(risk_factors)
        elif hasattr(risk_factors, "model_dump"):
            raw = risk_factors.model_dump()
        elif isinstance(risk_factors, dict):
            raw = risk_factors
        else:
            raw = {}

        return {
            "negative_sentiment": float(raw.get("negative_sentiment_ratio", 0.0)),
            "negative_strength": float(raw.get("negative_sentiment_strength", 0.0)),
            "bot_impact": float(raw.get("bot_impact_score", 0.0)),
            "propagation_speed": float(raw.get("propagation_speed", 0.0)),
            "controversy": float(raw.get("controversy_score", 0.0)),
            "trend_shift": float(raw.get("trend_shift", 0.0)),
        }

    if visualization:
        return {
            "negative_sentiment": float(visualization.risk_radar.negative_sentiment),
            "negative_strength": 0.0,
            "bot_impact": float(visualization.risk_radar.bot_impact),
            "propagation_speed": float(visualization.risk_radar.propagation_speed),
            "controversy": float(visualization.risk_radar.controversy),
            "trend_shift": float(visualization.risk_radar.trend_shift),
        }

    return {}


def _dominant_factor_label(factors: dict[str, float]) -> str:
    labels = {
        "negative_sentiment": "negative sentiment",
        "negative_strength": "negative sentiment strength",
        "bot_impact": "bot-like amplification",
        "propagation_speed": "propagation speed",
        "controversy": "controversy",
        "trend_shift": "trend shift",
    }
    if not factors:
        return "limited in the current mock data"
    key, value = max(factors.items(), key=lambda item: item[1])
    if value <= 0:
        return "limited in the current mock data"
    return f"{labels.get(key, key)} ({_format_percent(value)})"


def _format_percent(value: float) -> str:
    return f"{round(value * 100)}%"


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped
