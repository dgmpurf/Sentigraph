from collections import defaultdict

from app.schemas.analysis import SentimentResult
from app.schemas.comment import CleanComment, UserAggregationResult


def aggregate_users(
    clean_comments: list[CleanComment],
    sentiment_results: list[SentimentResult] | None = None,
) -> list[UserAggregationResult]:
    sentiment_by_comment = {
        result.comment_id: result.sentiment_score for result in sentiment_results or []
    }
    grouped: dict[str, list[CleanComment]] = defaultdict(list)
    for comment in clean_comments:
        grouped[str(comment.author_id)].append(comment)

    results: list[UserAggregationResult] = []
    for author_id, comments in sorted(grouped.items()):
        comment_count = sum(comment.duplicate_count for comment in comments)
        unique_comment_count = len(comments)
        duplicate_comment_ratio = 0.0
        if comment_count:
            duplicate_comment_ratio = max(0.0, (comment_count - unique_comment_count) / comment_count)

        weighted_sentiment_total = 0.0
        weighted_sentiment_count = 0
        for comment in comments:
            if comment.clean_comment_id in sentiment_by_comment:
                weighted_sentiment_total += sentiment_by_comment[comment.clean_comment_id] * comment.duplicate_count
                weighted_sentiment_count += comment.duplicate_count

        average_sentiment_score = (
            weighted_sentiment_total / weighted_sentiment_count if weighted_sentiment_count else 0.0
        )
        results.append(
            UserAggregationResult(
                author_id=author_id,
                platforms=sorted({platform for comment in comments for platform in comment.platforms}),
                comment_count=comment_count,
                unique_comment_count=unique_comment_count,
                duplicate_comment_ratio=round(duplicate_comment_ratio, 4),
                average_sentiment_score=round(average_sentiment_score, 4),
                first_seen_at=min(comment.created_at_min for comment in comments),
                last_seen_at=max(comment.created_at_max for comment in comments),
            )
        )
    return results

