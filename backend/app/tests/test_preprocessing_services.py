from app.schemas.analysis import SentimentResult
from app.schemas.comment import RawComment
from app.services.preprocessing.duplicate_detector import detect_duplicate_groups, group_duplicate_counts
from app.services.preprocessing.text_cleaner import clean_text, detect_language, fingerprint_text
from app.services.preprocessing.user_aggregator import aggregate_users


def _raw_comment(
    comment_id: str,
    author_id: str,
    content: str,
    created_at: str = "2026-05-13T10:00:00Z",
) -> RawComment:
    return RawComment(
        platform="reddit",
        post_id="post_001",
        comment_id=comment_id,
        parent_id=None,
        author_id=author_id,
        author_name="anonymous_user",
        content=content,
        like_count=1,
        reply_count=0,
        share_count=0,
        created_at=created_at,
        url=f"https://example.com/{comment_id}",
        raw_data={},
    )


def test_text_cleaner_normalizes_links_handles_html_and_language() -> None:
    text = "  @user This PRODUCT has serious issues!!! https://example.com #Quality  "
    assert clean_text(text) == "this product has serious issues! quality"
    assert fingerprint_text(text) == "thisproducthasseriousissuesquality"
    assert clean_text("<p>Hello&nbsp;<b>World</b>!!!</p>") == "hello world!"
    assert clean_text("") == ""
    assert detect_language("\u8fd9\u662f\u4e00\u4e2a\u4e2d\u6587\u95ee\u9898") == "zh"
    assert detect_language("plain english") == "en"


def test_duplicate_detector_preserves_author_level_records() -> None:
    comments = [
        _raw_comment("comment_001", "author_a", "This product has serious quality issues."),
        _raw_comment("comment_002", "author_a", "This product has serious quality issues!"),
        _raw_comment("comment_003", "author_b", "This product has serious quality issues."),
    ]

    clean_comments = detect_duplicate_groups(comments)

    assert len(clean_comments) == 2
    assert {comment.author_id for comment in clean_comments} == {"author_a", "author_b"}
    assert all(comment.duplicate_group_id == "dup_group_001" for comment in clean_comments)
    assert all(comment.is_repeated_script for comment in clean_comments)
    assert group_duplicate_counts(clean_comments) == {"dup_group_001": 3}


def test_duplicate_detector_groups_similar_content_deterministically() -> None:
    comments = [
        _raw_comment("comment_001", "author_a", "Quality issue response is delayed."),
        _raw_comment("comment_002", "author_b", "Quality issues response is delayed"),
        _raw_comment("comment_003", "author_c", "This is a separate neutral observation."),
    ]

    clean_comments = detect_duplicate_groups(comments)
    duplicate_groups = {comment.duplicate_group_id for comment in clean_comments}

    assert "dup_group_001" in duplicate_groups
    assert len(clean_comments) == 3
    assert group_duplicate_counts(clean_comments)["dup_group_001"] == 2


def test_user_aggregator_preserves_duplicate_statistics_and_weighted_sentiment() -> None:
    clean_comments = detect_duplicate_groups(
        [
            _raw_comment("comment_001", "author_a", "This product has serious quality issues."),
            _raw_comment("comment_002", "author_a", "This product has serious quality issues."),
            _raw_comment("comment_003", "author_a", "This looks fine.", "2026-05-13T12:00:00Z"),
        ]
    )
    sentiment_results = [
        SentimentResult(
            comment_id=comment.clean_comment_id,
            sentiment="negative",
            sentiment_score=-0.8,
            emotion_tags=["anger"],
            stance="opposing",
            confidence=0.9,
            reason="test",
        )
        for comment in clean_comments
    ]

    aggregates = aggregate_users(clean_comments, sentiment_results)

    assert len(aggregates) == 1
    assert aggregates[0].author_id == "author_a"
    assert aggregates[0].comment_count == 3
    assert aggregates[0].unique_comment_count == 2
    assert aggregates[0].duplicate_comment_ratio == 0.3333
    assert aggregates[0].average_sentiment_score == -0.8
