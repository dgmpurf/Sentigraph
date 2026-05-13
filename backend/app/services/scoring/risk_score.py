from dataclasses import dataclass

from app.schemas.analysis import BotImpactSummary, ConflictResult, RiskBrief, SentimentSummary, TopicCluster


@dataclass(frozen=True)
class RiskFactors:
    negative_sentiment_ratio: float
    negative_sentiment_strength: float
    bot_impact_score: float
    propagation_speed: float
    controversy_score: float
    trend_shift: float


@dataclass(frozen=True)
class RiskScoreResult:
    risk: RiskBrief
    factors: RiskFactors
    explanation: str


def calculate_risk_score(
    sentiment: SentimentSummary,
    bot_impact: BotImpactSummary,
    topics: list[TopicCluster] | None = None,
    conflicts: list[ConflictResult] | None = None,
    propagation_speed: float = 0.0,
    trend_shift: float = 0.0,
) -> RiskScoreResult:
    topics = topics or []
    conflicts = conflicts or []
    negative_strength = min(1.0, abs(min(sentiment.average_sentiment_score, 0.0)))
    controversy = max([conflict.intensity for conflict in conflicts] or [0.0])
    if not controversy and topics:
        negative_topics = [abs(topic.average_sentiment_score) for topic in topics if topic.average_sentiment_score < 0]
        controversy = min(1.0, sum(negative_topics) / max(len(topics), 1))

    factors = RiskFactors(
        negative_sentiment_ratio=round(sentiment.negative_ratio, 4),
        negative_sentiment_strength=round(negative_strength, 4),
        bot_impact_score=round(bot_impact.suspected_bot_comment_ratio, 4),
        propagation_speed=round(propagation_speed, 4),
        controversy_score=round(controversy, 4),
        trend_shift=round(trend_shift, 4),
    )
    weighted_score = (
        factors.negative_sentiment_ratio * 30
        + factors.negative_sentiment_strength * 20
        + factors.bot_impact_score * 15
        + factors.propagation_speed * 15
        + factors.controversy_score * 12
        + factors.trend_shift * 8
    )
    score = int(round(max(0, min(100, weighted_score))))
    level = _risk_level(score)
    explanation = _explanation(factors)
    return RiskScoreResult(risk=RiskBrief(risk_score=score, risk_level=level), factors=factors, explanation=explanation)


def _risk_level(score: int) -> str:
    if score >= 90:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def _explanation(factors: RiskFactors) -> str:
    if factors.negative_sentiment_ratio >= 0.6 and factors.bot_impact_score >= 0.3:
        return "Negative sentiment is elevated with repeated-script or bot-like amplification."
    if factors.negative_sentiment_ratio >= 0.6:
        return "Negative sentiment is the main driver of risk."
    if factors.bot_impact_score >= 0.3:
        return "Bot-like amplification is the main driver of risk."
    return "Risk remains limited in the current rule-based mock scoring."

