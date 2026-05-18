from __future__ import annotations

from typing import Any, Mapping

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.comment import RawComment, RawPost
from app.services.crawling.adapter_factory import get_adapter
from app.services.crawling.youtube_adapter import (
    YouTubeAdapter,
    YouTubeCredentials,
)


client = TestClient(app)


class FakeYouTubeClient:
    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[Mapping[str, Any]]:
        del date_range
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
        del limit
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
    post = adapter.normalize_post(
        {
            "id": {"videoId": "yt_utf8_video"},
            "snippet": {
                "channelId": "yt_utf8_channel",
                "channelTitle": "UTF-8 Fixture Channel",
                "title": "特斯拉安全说明 ⚡",
                "description": "中文说明和 emoji 😊 should remain intact.",
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
                "textOriginal": "支持透明说明 ⚡ and calm updates.",
                "likeCount": "4",
                "publishedAt": "2026-05-17T10:10:00Z",
            },
        }
    )

    assert post.title == "特斯拉安全说明 ⚡"
    assert post.content == "中文说明和 emoji 😊 should remain intact."
    assert comment.content == "支持透明说明 ⚡ and calm updates."
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
