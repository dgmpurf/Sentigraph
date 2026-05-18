from __future__ import annotations

from typing import Any, Mapping

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.comment import RawComment, RawPost
from app.services.crawling.adapter_factory import get_adapter
from app.services.crawling.youtube_adapter import (
    YouTubeAdapter,
    YouTubeAuthError,
    YouTubeCommentsDisabledError,
    YouTubeCredentials,
    YouTubeNetworkError,
    YouTubeQuotaError,
)
from app.services.crawling.youtube_cache import YouTubeAdapterConfig, YouTubeResponseCache


client = TestClient(app)


class FakeYouTubeClient:
    def __init__(self) -> None:
        self.search_call_count = 0
        self.fetch_comments_call_count = 0
        self.search_limits: list[int] = []
        self.comment_limits: list[int] = []

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[Mapping[str, Any]]:
        del date_range
        self.search_call_count += 1
        self.search_limits.append(limit)
        return [
            {
                "source_type": "youtube_data_api_v3",
                "id": "yt_real_video_001",
                "snippet": {
                    "channelId": "yt_real_channel_001",
                    "channelTitle": "Official API Fixture Channel",
                    "title": f"{keyword} official API fixture",
                    "description": "Fixture metadata from a mocked official YouTube Data API response.",
                    "publishedAt": "2026-05-17T12:00:00Z",
                },
                "statistics": {
                    "likeCount": "42",
                    "commentCount": "7",
                    "viewCount": "1500",
                },
                "sort_seen": sort,
                "limit_seen": limit,
            }
        ]

    def fetch_comments(self, post_id: str, *, limit: int) -> list[Mapping[str, Any]]:
        self.fetch_comments_call_count += 1
        self.comment_limits.append(limit)
        return [
            {
                "id": "yt_real_comment_001",
                "snippet": {
                    "videoId": post_id,
                    "authorChannelId": {"value": "yt_real_commenter_001"},
                    "authorDisplayName": "Official API Fixture Commenter",
                    "textOriginal": "Fixture comment from a mocked official API response.",
                    "likeCount": "5",
                    "publishedAt": "2026-05-17T12:05:00Z",
                    "totalReplyCount": "1",
                },
            }
        ]


class ReplyRichYouTubeClient(FakeYouTubeClient):
    def fetch_comments(self, post_id: str, *, limit: int) -> list[Mapping[str, Any]]:
        self.fetch_comments_call_count += 1
        self.comment_limits.append(limit)
        comments: list[Mapping[str, Any]] = [
            {
                "id": "yt_real_comment_top_001",
                "snippet": {
                    "videoId": post_id,
                    "authorChannelId": {"value": "yt_real_commenter_top"},
                    "authorDisplayName": "Top Commenter",
                    "textOriginal": "Top-level comment should remain.",
                    "likeCount": "5",
                    "publishedAt": "2026-05-17T12:05:00Z",
                    "totalReplyCount": "6",
                },
            }
        ]
        comments.extend(
            {
                "id": f"yt_real_reply_{index:03d}",
                "snippet": {
                    "videoId": post_id,
                    "parentId": "yt_real_comment_top_001",
                    "authorChannelId": {"value": f"yt_real_reply_author_{index:03d}"},
                    "authorDisplayName": f"Reply Commenter {index}",
                    "textOriginal": f"Reply {index} should be limited by guardrails.",
                    "likeCount": "1",
                    "publishedAt": "2026-05-17T12:06:00Z",
                },
            }
            for index in range(1, 8)
        )
        comments.append(
            {
                "id": "yt_real_comment_top_002",
                "snippet": {
                    "videoId": post_id,
                    "authorChannelId": {"value": "yt_real_commenter_top_002"},
                    "authorDisplayName": "Second Top Commenter",
                    "textOriginal": "Second top-level comment.",
                    "likeCount": "2",
                    "publishedAt": "2026-05-17T12:07:00Z",
                },
            }
        )
        return comments[:limit]


class AuthFailingYouTubeClient(FakeYouTubeClient):
    def fetch_comments(self, post_id: str, *, limit: int) -> list[Mapping[str, Any]]:
        del post_id, limit
        raise YouTubeAuthError("youtube_comments_disabled_or_quota_error")


class QuotaFailingYouTubeClient(FakeYouTubeClient):
    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[Mapping[str, Any]]:
        del keyword, limit, sort, date_range
        raise YouTubeQuotaError("youtube_quota_error")


class CommentsDisabledYouTubeClient(FakeYouTubeClient):
    def fetch_comments(self, post_id: str, *, limit: int) -> list[Mapping[str, Any]]:
        del post_id, limit
        raise YouTubeCommentsDisabledError("youtube_comments_unavailable")


class NetworkFailingYouTubeClient(FakeYouTubeClient):
    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[Mapping[str, Any]]:
        del keyword, limit, sort, date_range
        raise YouTubeNetworkError("youtube_network_error")


def test_youtube_mock_search_posts(monkeypatch) -> None:
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "mock")
    monkeypatch.setenv("YOUTUBE_API_KEY", "")

    adapter = YouTubeAdapter()
    posts = adapter.search_posts("Tesla", limit=5, sort="new")

    assert adapter.get_mode() == "mock"
    assert posts
    assert len(posts) <= 5
    assert all(post.platform == "youtube" for post in posts)
    assert posts[0].raw_data["source_type"] == "youtube_data_api_v3"
    assert "api_key" not in posts[0].raw_data
    RawPost.model_validate(posts[0].model_dump(mode="json"))


def test_youtube_mock_fetch_comments(monkeypatch) -> None:
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "mock")
    monkeypatch.setenv("YOUTUBE_API_KEY", "")

    adapter = YouTubeAdapter()
    comments = adapter.fetch_comments("yt_mock_video_001", limit=10)

    assert adapter.get_mode() == "mock"
    assert comments
    assert len(comments) <= 10
    assert all(comment.platform == "youtube" for comment in comments)
    assert comments[0].raw_data["source_type"] == "youtube_data_api_v3"
    assert "api_key" not in comments[0].raw_data
    RawComment.model_validate(comments[0].model_dump(mode="json"))


def test_youtube_normalize_post_from_official_shape(monkeypatch) -> None:
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "mock")
    monkeypatch.setenv("YOUTUBE_API_KEY", "")

    adapter = YouTubeAdapter()
    post = adapter.normalize_post(
        {
            "id": {"videoId": "yt_normalized_video"},
            "snippet": {
                "channelId": "yt_channel_001",
                "channelTitle": "Fixture Channel",
                "title": "Fixture video",
                "description": "Fixture description",
                "publishedAt": "2026-05-17T10:00:00Z",
            },
            "statistics": {"likeCount": "11", "commentCount": "3", "viewCount": "100"},
        }
    )

    assert post.platform == "youtube"
    assert post.post_id == "yt_normalized_video"
    assert post.author_id == "yt_channel_001"
    assert post.reply_count == 3
    RawPost.model_validate(post.model_dump(mode="json"))


def test_youtube_normalize_comment_from_official_shape(monkeypatch) -> None:
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "mock")
    monkeypatch.setenv("YOUTUBE_API_KEY", "")

    adapter = YouTubeAdapter()
    comment = adapter.normalize_comment(
        {
            "id": "yt_comment_001",
            "snippet": {
                "videoId": "yt_normalized_video",
                "parentId": "yt_parent_001",
                "authorChannelId": {"value": "yt_commenter_001"},
                "authorDisplayName": "Fixture Commenter",
                "textOriginal": "Fixture comment text.",
                "likeCount": "9",
                "publishedAt": "2026-05-17T10:10:00Z",
            },
        }
    )

    assert comment.platform == "youtube"
    assert comment.post_id == "yt_normalized_video"
    assert comment.comment_id == "yt_comment_001"
    assert comment.parent_id == "yt_parent_001"
    assert comment.author_id == "yt_commenter_001"
    RawComment.model_validate(comment.model_dump(mode="json"))


def test_youtube_utf8_text_round_trips_through_normalization(monkeypatch) -> None:
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "mock")
    monkeypatch.setenv("YOUTUBE_API_KEY", "")

    adapter = YouTubeAdapter()
    title = "\u7279\u65af\u62c9\u5b89\u5168\u8bf4\u660e \u26a1"
    description = "\u4e2d\u6587\u8bf4\u660e\u548c emoji \U0001f60a should remain intact."
    comment_text = "\u652f\u6301\u900f\u660e\u8bf4\u660e \u26a1 and calm updates."
    post = adapter.normalize_post(
        {
            "id": {"videoId": "yt_utf8_video"},
            "snippet": {
                "channelId": "yt_utf8_channel",
                "channelTitle": "UTF-8 Fixture Channel",
                "title": title,
                "description": description,
                "publishedAt": "2026-05-17T10:00:00Z",
            },
            "statistics": {"likeCount": "11", "commentCount": "3", "viewCount": "100"},
        }
    )
    comment = adapter.normalize_comment(
        {
            "id": "yt_utf8_comment",
            "snippet": {
                "videoId": "yt_utf8_video",
                "authorChannelId": {"value": "yt_utf8_commenter"},
                "authorDisplayName": "UTF-8 Fixture Commenter",
                "textOriginal": comment_text,
                "likeCount": "4",
                "publishedAt": "2026-05-17T10:10:00Z",
            },
        }
    )

    assert post.title == title
    assert post.content == description
    assert comment.content == comment_text
    RawPost.model_validate(post.model_dump(mode="json"))
    RawComment.model_validate(comment.model_dump(mode="json"))


def test_youtube_comment_thread_parent_ids_defaults_and_urls(monkeypatch) -> None:
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "mock")
    monkeypatch.setenv("YOUTUBE_API_KEY", "")

    adapter = YouTubeAdapter()
    top_level = adapter.normalize_comment(
        {
            "id": "yt_thread_001",
            "snippet": {
                "videoId": "yt_thread_video",
                "totalReplyCount": "2",
                "topLevelComment": {
                    "id": "yt_top_comment_001",
                    "snippet": {
                        "videoId": "yt_thread_video",
                        "authorChannelId": {"value": "yt_top_author"},
                        "authorDisplayName": "Top Level Fixture",
                        "textOriginal": "Top-level public comment.",
                        "likeCount": "8",
                        "publishedAt": "2026-05-17T11:00:00Z",
                    },
                },
            },
        }
    )
    reply = adapter.normalize_comment(
        {
            "id": "yt_reply_comment_001",
            "snippet": {
                "videoId": "yt_thread_video",
                "parentId": "yt_top_comment_001",
                "authorChannelId": {"value": "yt_reply_author"},
                "authorDisplayName": "Reply Fixture",
                "textOriginal": "Reply to the top-level public comment.",
                "publishedAt": "2026-05-17T11:05:00Z",
            },
        }
    )

    assert top_level.comment_id == "yt_top_comment_001"
    assert top_level.parent_id is None
    assert top_level.reply_count == 2
    assert "yt_thread_video" in top_level.url
    assert "yt_top_comment_001" in top_level.url
    assert reply.parent_id == "yt_top_comment_001"
    assert reply.like_count == 0
    assert reply.reply_count == 0
    assert "yt_thread_video" in reply.url
    assert "yt_reply_comment_001" in reply.url
    RawComment.model_validate(top_level.model_dump(mode="json"))
    RawComment.model_validate(reply.model_dump(mode="json"))


def test_youtube_real_mode_missing_key_falls_back_to_mock(monkeypatch) -> None:
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", "")

    adapter = YouTubeAdapter()
    posts = adapter.search_posts("Tesla", limit=2)
    metadata = adapter.get_status_metadata()

    assert adapter.get_mode() == "mock"
    assert adapter.supports_real_mode() is False
    assert metadata["credential_present"] is False
    assert metadata["real_mode_available"] is False
    assert metadata["sanitized_error_category"] == "config_error"
    assert metadata["real_mode_blocked_reason"] == "credentials_missing"
    assert posts
    assert posts[0].raw_data["mode"] == "mock"


def test_youtube_mocked_real_api_response_normalizes_without_network(monkeypatch) -> None:
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", "youtube-test-marker-should-not-appear")

    adapter = YouTubeAdapter(
        mode="real",
        credentials=YouTubeCredentials(api_key="youtube-test-marker-should-not-appear"),
        http_client=FakeYouTubeClient(),
        config=YouTubeAdapterConfig(cache_enabled=False),
    )
    posts = adapter.search_posts("Tesla", limit=3, sort="date")
    comments = adapter.fetch_comments(posts[0].post_id, limit=3)
    metadata = adapter.get_status_metadata()

    assert adapter.get_mode() == "real"
    assert adapter.supports_real_mode() is True
    assert metadata["credential_present"] is True
    assert metadata["real_mode_available"] is True
    assert metadata["selectable_for_real"] is True
    assert metadata["real_mode_reached"] is True
    assert posts[0].post_id == "yt_real_video_001"
    assert comments[0].post_id == "yt_real_video_001"
    assert "youtube-test-marker-should-not-appear" not in str(posts[0].raw_data)
    assert "youtube-test-marker-should-not-appear" not in str(comments[0].raw_data)
    RawPost.model_validate(posts[0].model_dump(mode="json"))
    RawComment.model_validate(comments[0].model_dump(mode="json"))


def test_youtube_cache_miss_calls_mocked_real_client_and_stores_safe_payload(monkeypatch, tmp_path) -> None:
    fake_key_marker = "youtube-test-marker-should-not-appear"
    cache_path = tmp_path / "youtube_cache.json"
    fake_client = FakeYouTubeClient()
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", fake_key_marker)

    adapter = YouTubeAdapter(
        mode="real",
        credentials=YouTubeCredentials(api_key=fake_key_marker),
        http_client=fake_client,
        config=YouTubeAdapterConfig(cache_enabled=True, cache_ttl_seconds=3600),
        cache=YouTubeResponseCache(path=cache_path, enabled=True, ttl_seconds=3600),
    )

    posts = adapter.search_posts("Tesla", limit=3)
    metadata = adapter.get_status_metadata()

    assert posts
    assert fake_client.search_call_count == 1
    assert metadata["cache_hit"] is False
    assert metadata["search_call_count"] == 1
    assert metadata["videos_call_count"] == 1
    assert metadata["estimated_quota_units"] == 101
    assert metadata["quota_guardrail_status"] == "cache_miss_real_call"
    assert fake_key_marker not in cache_path.read_text(encoding="utf-8")


def test_youtube_cache_hit_skips_mocked_real_client(monkeypatch, tmp_path) -> None:
    fake_key_marker = "youtube-test-marker-should-not-appear"
    cache_path = tmp_path / "youtube_cache.json"
    config = YouTubeAdapterConfig(cache_enabled=True, cache_ttl_seconds=3600)
    cache = YouTubeResponseCache(path=cache_path, enabled=True, ttl_seconds=3600)
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", fake_key_marker)

    first_client = FakeYouTubeClient()
    first_adapter = YouTubeAdapter(
        mode="real",
        credentials=YouTubeCredentials(api_key=fake_key_marker),
        http_client=first_client,
        config=config,
        cache=cache,
    )
    first_adapter.search_posts("Tesla", limit=3)

    second_client = FakeYouTubeClient()
    second_adapter = YouTubeAdapter(
        mode="real",
        credentials=YouTubeCredentials(api_key=fake_key_marker),
        http_client=second_client,
        config=config,
        cache=cache,
    )
    cached_posts = second_adapter.search_posts("Tesla", limit=3)
    metadata = second_adapter.get_status_metadata()

    assert cached_posts
    assert first_client.search_call_count == 1
    assert second_client.search_call_count == 0
    assert metadata["cache_hit"] is True
    assert metadata["cache_age_seconds"] is not None
    assert metadata["estimated_quota_units"] == 0
    assert metadata["quota_guardrail_status"] == "cache_hit"


def test_youtube_cache_ttl_expiry_calls_mocked_real_client_again(monkeypatch, tmp_path) -> None:
    fake_key_marker = "youtube-test-marker-should-not-appear"
    cache_path = tmp_path / "youtube_cache.json"
    config = YouTubeAdapterConfig(cache_enabled=True, cache_ttl_seconds=0)
    cache = YouTubeResponseCache(path=cache_path, enabled=True, ttl_seconds=0)
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", fake_key_marker)

    first_client = FakeYouTubeClient()
    first_adapter = YouTubeAdapter(
        mode="real",
        credentials=YouTubeCredentials(api_key=fake_key_marker),
        http_client=first_client,
        config=config,
        cache=cache,
    )
    first_adapter.search_posts("Tesla", limit=3)

    second_client = FakeYouTubeClient()
    second_adapter = YouTubeAdapter(
        mode="real",
        credentials=YouTubeCredentials(api_key=fake_key_marker),
        http_client=second_client,
        config=config,
        cache=cache,
    )
    second_adapter.search_posts("Tesla", limit=3)
    metadata = second_adapter.get_status_metadata()

    assert first_client.search_call_count == 1
    assert second_client.search_call_count == 1
    assert metadata["cache_hit"] is False
    assert metadata["quota_guardrail_status"] == "cache_miss_real_call"


def test_youtube_requested_limits_are_clamped_by_guardrails(monkeypatch, tmp_path) -> None:
    fake_key_marker = "youtube-test-marker-should-not-appear"
    fake_client = FakeYouTubeClient()
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", fake_key_marker)

    adapter = YouTubeAdapter(
        mode="real",
        credentials=YouTubeCredentials(api_key=fake_key_marker),
        http_client=fake_client,
        config=YouTubeAdapterConfig(
            cache_enabled=False,
            max_search_results=2,
            max_comments_per_video=4,
            max_total_comments=3,
        ),
        cache=YouTubeResponseCache(path=tmp_path / "youtube_cache.json", enabled=False),
    )

    posts = adapter.search_posts("Tesla", limit=99)
    comments = adapter.fetch_comments("yt_real_video_001", limit=99)

    assert posts
    assert comments
    assert fake_client.search_limits == [2]
    assert fake_client.comment_limits == [3]


def test_youtube_deep_replies_disabled_by_default(monkeypatch, tmp_path) -> None:
    fake_key_marker = "youtube-test-marker-should-not-appear"
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", fake_key_marker)

    adapter = YouTubeAdapter(
        mode="real",
        credentials=YouTubeCredentials(api_key=fake_key_marker),
        http_client=ReplyRichYouTubeClient(),
        config=YouTubeAdapterConfig(cache_enabled=False, enable_deep_replies=False),
        cache=YouTubeResponseCache(path=tmp_path / "youtube_cache.json", enabled=False),
    )

    comments = adapter.fetch_comments("yt_real_video_001", limit=10)

    assert comments
    assert all(comment.parent_id is None for comment in comments)
    assert len(comments) == 2


def test_youtube_deep_replies_and_total_comments_are_strictly_limited(monkeypatch, tmp_path) -> None:
    fake_key_marker = "youtube-test-marker-should-not-appear"
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", fake_key_marker)

    adapter = YouTubeAdapter(
        mode="real",
        credentials=YouTubeCredentials(api_key=fake_key_marker),
        http_client=ReplyRichYouTubeClient(),
        config=YouTubeAdapterConfig(
            cache_enabled=False,
            enable_deep_replies=True,
            max_replies_per_comment=2,
            max_total_comments=3,
        ),
        cache=YouTubeResponseCache(path=tmp_path / "youtube_cache.json", enabled=False),
    )

    comments = adapter.fetch_comments("yt_real_video_001", limit=10)
    reply_count = sum(1 for comment in comments if comment.parent_id)

    assert len(comments) == 3
    assert reply_count == 2


def test_youtube_quota_error_falls_back_to_mock_with_safe_metadata(monkeypatch) -> None:
    fake_key_marker = "youtube-test-marker-should-not-appear"
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", fake_key_marker)

    adapter = YouTubeAdapter(
        mode="real",
        credentials=YouTubeCredentials(api_key=fake_key_marker),
        http_client=QuotaFailingYouTubeClient(),
        config=YouTubeAdapterConfig(cache_enabled=False),
    )

    posts = adapter.search_posts("Tesla", limit=3)
    metadata = adapter.get_status_metadata()

    assert posts
    assert posts[0].raw_data["mode"] == "mock"
    assert metadata["sanitized_error_category"] == "quota_error"
    assert metadata["fetch_status"] == "quota_error"
    assert metadata["quota_guardrail_status"] == "quota_error_fallback"
    assert fake_key_marker not in str(metadata)


def test_youtube_comments_disabled_returns_safe_partial_result(monkeypatch) -> None:
    fake_key_marker = "youtube-test-marker-should-not-appear"
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", fake_key_marker)

    adapter = YouTubeAdapter(
        mode="real",
        credentials=YouTubeCredentials(api_key=fake_key_marker),
        http_client=CommentsDisabledYouTubeClient(),
        config=YouTubeAdapterConfig(cache_enabled=False),
    )

    comments = adapter.fetch_comments("yt_real_video_001", limit=3)
    metadata = adapter.get_status_metadata()

    assert comments == []
    assert metadata["sanitized_error_category"] == "comments_unavailable"
    assert metadata["fetch_status"] == "comments_unavailable"
    assert metadata["quota_guardrail_status"] == "comments_unavailable_partial"
    assert fake_key_marker not in str(metadata)


def test_youtube_real_comments_disabled_or_quota_error_falls_back_to_mock(monkeypatch) -> None:
    fake_key_marker = "youtube-test-marker-should-not-appear"
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", fake_key_marker)

    adapter = YouTubeAdapter(
        mode="real",
        credentials=YouTubeCredentials(api_key=fake_key_marker),
        http_client=AuthFailingYouTubeClient(),
        config=YouTubeAdapterConfig(cache_enabled=False),
    )

    comments = adapter.fetch_comments("yt_real_video_001", limit=3)
    metadata = adapter.get_status_metadata()

    assert comments
    assert comments[0].raw_data["mode"] == "mock"
    assert metadata["sanitized_error_category"] == "auth_error"
    assert metadata["fetch_status"] == "auth_error"
    assert metadata["exception_class"] == "YouTubeAuthError"
    assert fake_key_marker not in str(comments)
    assert fake_key_marker not in str(metadata)
    RawComment.model_validate(comments[0].model_dump(mode="json"))


def test_youtube_real_network_error_falls_back_to_mock(monkeypatch) -> None:
    fake_key_marker = "youtube-test-marker-should-not-appear"
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", fake_key_marker)

    adapter = YouTubeAdapter(
        mode="real",
        credentials=YouTubeCredentials(api_key=fake_key_marker),
        http_client=NetworkFailingYouTubeClient(),
        config=YouTubeAdapterConfig(cache_enabled=False),
    )

    posts = adapter.search_posts("Tesla", limit=3)
    metadata = adapter.get_status_metadata()

    assert posts
    assert posts[0].raw_data["mode"] == "mock"
    assert metadata["sanitized_error_category"] == "network_error"
    assert metadata["fetch_status"] == "network_error"
    assert metadata["exception_class"] == "YouTubeNetworkError"
    assert fake_key_marker not in str(posts)
    assert fake_key_marker not in str(metadata)
    RawPost.model_validate(posts[0].model_dump(mode="json"))


def test_crawl_start_youtube_mocked_real_output_is_downstream_compatible(monkeypatch) -> None:
    fake_key_marker = "youtube-test-marker-should-not-appear"
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", fake_key_marker)

    def fake_get_adapter(platform_id: str) -> YouTubeAdapter:
        assert platform_id == "youtube"
        return YouTubeAdapter(
            mode="real",
            credentials=YouTubeCredentials(api_key=fake_key_marker),
            http_client=FakeYouTubeClient(),
            config=YouTubeAdapterConfig(cache_enabled=False),
        )

    monkeypatch.setattr("app.services.crawling.crawl_service.adapter_factory.get_adapter", fake_get_adapter)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["youtube"], "limit": 3},
    )

    assert response.status_code == 200
    assert fake_key_marker not in response.text
    body = response.json()
    metadata = body["platform_metadata"][0]
    post = body["raw_posts"][0]
    comment = body["raw_comments"][0]

    assert metadata["platform"] == "youtube"
    assert metadata["adapter_mode"] == "real"
    assert metadata["source_type"] == "youtube_data_api_v3"
    assert metadata["fallback_used"] is False
    assert metadata["credential_present"] is True
    assert metadata["real_mode_reached"] is True
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True

    assert set(post) >= {
        "platform",
        "post_id",
        "author_id",
        "author_name",
        "title",
        "content",
        "like_count",
        "reply_count",
        "share_count",
        "created_at",
        "url",
        "raw_data",
    }
    assert set(comment) >= {
        "platform",
        "post_id",
        "comment_id",
        "parent_id",
        "author_id",
        "author_name",
        "content",
        "like_count",
        "reply_count",
        "created_at",
        "url",
        "raw_data",
    }
    assert post["platform"] == "youtube"
    assert comment["platform"] == "youtube"
    assert comment["post_id"] == post["post_id"]
    assert post["share_count"] == 0
    assert isinstance(post["like_count"], int)
    assert isinstance(comment["like_count"], int)
    assert "api_key" not in str(post["raw_data"]).lower()
    assert "api_key" not in str(comment["raw_data"]).lower()
    RawPost.model_validate(post)
    RawComment.model_validate(comment)


def test_crawl_start_youtube_includes_cache_and_quota_metadata(monkeypatch, tmp_path) -> None:
    fake_key_marker = "youtube-test-marker-should-not-appear"
    fake_client = FakeYouTubeClient()
    cache = YouTubeResponseCache(path=tmp_path / "youtube_cache.json", enabled=True, ttl_seconds=3600)
    config = YouTubeAdapterConfig(cache_enabled=True, cache_ttl_seconds=3600)
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", fake_key_marker)

    def fake_get_adapter(platform_id: str) -> YouTubeAdapter:
        assert platform_id == "youtube"
        return YouTubeAdapter(
            mode="real",
            credentials=YouTubeCredentials(api_key=fake_key_marker),
            http_client=fake_client,
            config=config,
            cache=cache,
        )

    monkeypatch.setattr("app.services.crawling.crawl_service.adapter_factory.get_adapter", fake_get_adapter)

    first_response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["youtube"], "limit": 3},
    )
    second_response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["youtube"], "limit": 3},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert fake_key_marker not in first_response.text
    assert fake_key_marker not in second_response.text
    first_metadata = first_response.json()["platform_metadata"][0]
    second_metadata = second_response.json()["platform_metadata"][0]

    assert first_metadata["cache_hit"] is False
    assert first_metadata["estimated_quota_units"] == 102
    assert first_metadata["search_call_count"] == 1
    assert first_metadata["videos_call_count"] == 1
    assert first_metadata["comment_threads_call_count"] == 1
    assert first_metadata["comments_call_count"] == 0
    assert first_metadata["quota_guardrail_status"] == "cache_miss_real_call"

    assert second_metadata["cache_hit"] is True
    assert second_metadata["cache_age_seconds"] is not None
    assert second_metadata["estimated_quota_units"] == 0
    assert second_metadata["search_call_count"] == 0
    assert second_metadata["comment_threads_call_count"] == 0
    assert second_metadata["quota_guardrail_status"] == "cache_hit"
    assert fake_client.search_call_count == 1
    assert fake_client.fetch_comments_call_count == 1


def test_adapter_factory_returns_youtube_adapter(monkeypatch) -> None:
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "mock")
    monkeypatch.setenv("YOUTUBE_API_KEY", "")

    adapter = get_adapter("youtube")

    assert isinstance(adapter, YouTubeAdapter)
    assert adapter.get_required_credentials() == ("YOUTUBE_API_KEY",)


def test_crawl_start_with_youtube_works_in_mock_mode(monkeypatch) -> None:
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "mock")
    monkeypatch.setenv("YOUTUBE_API_KEY", "")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["youtube"], "limit": 100},
    )

    assert response.status_code == 200
    body = response.json()
    metadata = body["platform_metadata"][0]
    assert metadata["platform"] == "youtube"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "youtube_data_api_v3"
    assert metadata["fallback_used"] is False
    assert metadata["credential_present"] is False
    assert metadata["fetch_status"] == "mock"
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is False
    assert metadata["real_mode_disabled"] is False
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] <= 5
    assert metadata["comment_count"] <= 10
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert body["raw_posts"]
    assert body["raw_comments"]
    assert all(post["platform"] == "youtube" for post in body["raw_posts"])
    assert all(comment["platform"] == "youtube" for comment in body["raw_comments"])


def test_crawl_start_youtube_real_mode_missing_key_returns_safe_metadata(monkeypatch) -> None:
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    monkeypatch.setenv("YOUTUBE_API_KEY", "")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["youtube"], "limit": 100},
    )

    assert response.status_code == 200
    body = response.json()
    metadata = body["platform_metadata"][0]
    assert metadata["platform"] == "youtube"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "youtube_data_api_v3"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "config_error"
    assert metadata["fetch_status"] == "config_error"
    assert metadata["credential_present"] is False
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "credentials_missing"
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert body["raw_posts"]
    assert body["raw_comments"]
