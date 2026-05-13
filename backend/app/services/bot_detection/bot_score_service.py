from collections import defaultdict

from app.schemas.analysis import BotImpactSummary, BotScore, SentimentResult
from app.schemas.comment import CleanComment, UserAggregationResult


SUSPECTED_BOT_THRESHOLD = 0.6


def calculate_bot_scores(
    user_aggregates: list[UserAggregationResult],
    clean_comments: list[CleanComment],
    sentiment_results: list[SentimentResult] | None = None,
) -> tuple[list[BotScore], BotImpactSummary]:
    comments_by_author: dict[str, list[CleanComment]] = defaultdict(list)
    for comment in clean_comments:
        comments_by_author[str(comment.author_id)].append(comment)
    sentiment_by_comment = {
        result.comment_id: result.sentiment_score for result in sentiment_results or []
    }

    scores: list[BotScore] = []
    suspected_comment_count = 0
    total_comment_count = sum(comment.duplicate_count for comment in clean_comments)

    for aggregate in user_aggregates:
        author_comments = comments_by_author.get(aggregate.author_id, [])
        repeated_ratio = _repeated_script_ratio(author_comments)
        frequency_score = min(1.0, aggregate.comment_count / 20)
        sync_score = _synchronization_score(author_comments)
        sentiment_uniformity_score = _sentiment_uniformity_score(
            aggregate,
            author_comments,
            sentiment_by_comment,
        )
        bot_probability = min(
            1.0,
            aggregate.duplicate_comment_ratio * 0.4
            + repeated_ratio * 0.25
            + frequency_score * 0.15
            + sync_score * 0.1
            + sentiment_uniformity_score * 0.1,
        )
        reasons = _bot_reasons(
            aggregate,
            repeated_ratio,
            frequency_score,
            sync_score,
            sentiment_uniformity_score,
        )
        if bot_probability >= SUSPECTED_BOT_THRESHOLD:
            suspected_comment_count += aggregate.comment_count

        scores.append(
            BotScore(
                author_id=aggregate.author_id,
                bot_probability=round(bot_probability, 4),
                bot_reasons=reasons,
                influence_weight=round(min(1.0, aggregate.comment_count / max(total_comment_count, 1)), 4),
            )
        )

    suspected_accounts = sum(1 for score in scores if score.bot_probability >= SUSPECTED_BOT_THRESHOLD)
    impact = BotImpactSummary(
        suspected_bot_ratio=round(suspected_accounts / len(scores), 4) if scores else 0.0,
        suspected_bot_comment_ratio=round(suspected_comment_count / total_comment_count, 4)
        if total_comment_count
        else 0.0,
    )
    return sorted(scores, key=lambda score: score.bot_probability, reverse=True), impact


def _repeated_script_ratio(comments: list[CleanComment]) -> float:
    if not comments:
        return 0.0
    repeated_count = sum(comment.duplicate_count for comment in comments if comment.is_repeated_script)
    total_count = sum(comment.duplicate_count for comment in comments)
    return repeated_count / total_count if total_count else 0.0


def _synchronization_score(comments: list[CleanComment]) -> float:
    if len(comments) < 2:
        return 0.0
    first_hours = {comment.created_at_min[:13] for comment in comments}
    return 1.0 if len(first_hours) == 1 else 0.25


def _sentiment_uniformity_score(
    aggregate: UserAggregationResult,
    comments: list[CleanComment],
    sentiment_by_comment: dict[str, float],
) -> float:
    scores = [
        sentiment_by_comment[comment.clean_comment_id]
        for comment in comments
        if comment.clean_comment_id in sentiment_by_comment
    ]
    if not scores:
        if aggregate.comment_count > aggregate.unique_comment_count and abs(aggregate.average_sentiment_score) >= 0.6:
            return 0.5
        return 0.0

    if len(scores) == 1:
        return min(1.0, abs(scores[0]))

    same_direction = all(score <= 0 for score in scores) or all(score >= 0 for score in scores)
    average = sum(scores) / len(scores)
    average_deviation = sum(abs(score - average) for score in scores) / len(scores)
    consistency = max(0.0, 1.0 - average_deviation)
    polarity_strength = min(1.0, abs(average))
    direction_bonus = 0.15 if same_direction else 0.0
    return min(1.0, consistency * 0.6 + polarity_strength * 0.25 + direction_bonus)


def _bot_reasons(
    aggregate: UserAggregationResult,
    repeated_ratio: float,
    frequency_score: float,
    sync_score: float,
    sentiment_uniformity_score: float,
) -> list[str]:
    reasons: list[str] = []
    if aggregate.duplicate_comment_ratio >= 0.4:
        reasons.append("High repeated content ratio")
    if repeated_ratio >= 0.4:
        reasons.append("Repeated-script content detected")
    if frequency_score >= 0.75:
        reasons.append("Abnormally frequent comments")
    if sync_score >= 0.75:
        reasons.append("Highly synchronized posting time")
    if sentiment_uniformity_score >= 0.6:
        reasons.append("Highly uniform sentiment pattern")
    return reasons or ["No strong bot-like behavior in rule-based mock scoring"]
