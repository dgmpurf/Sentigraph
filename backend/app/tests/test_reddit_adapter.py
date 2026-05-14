from __future__ import annotations

from typing import Any, Mapping

import pytest

from app.schemas.comment import RawComment, RawPost
from app.services.crawling.adapter_factory import (
    get_adapter,
    get_platform_adapter,
    get_supported_adapter_ids,
    has_platform_adapter,
)
from app.services.crawling.base_adapter import AdapterHealth, BasePlatformAdapter, PlatformAdapterError
from app.services.crawling.platform_registry import get_platform_registry
from app.services.crawling.reddit_adapter import REDDIT_REQUIRED_CREDENTIALS, RedditAdapter, RedditCredentials


class FakeRedditClient:
    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[Mapping[str, Any]]:
        return [
            {
                "kind": "t3",
                "data": {
                    "id": "abc123",
                    "name": "t3_abc123",
                    "author": "public_redditor",
                    "author_fullname": "t2_public",
                    "title": f"{keyword} quality discussion",
                    "selftext": "Public discussion about product quality.",
                    "ups": 42,
                    "num_comments": 3,
                    "created_utc": 1778754000,
                    "permalink": "/r/test/comments/abc123/quality_discussion/",
                    "sort_seen": sort,
                    "date_range_seen": date_range,
                    101: "integer key should be stringified",
                },
            }
        ][:limit]

    def fetch_comments(self, post_id: str, *, limit: int) -> list[Mapping[str, Any]]:
        return [
            {
                "kind": "t1",
                "data": {
                    "id": "comment123",
                    "name": "t1_comment123",
                    "link_id": post_id,
                    "parent_id": post_id,
                    "author": "comment_author",
                    "author_fullname": "t2_comment_author",
                    "body": "This is a public Reddit comment.",
                    "ups": 12,
                    "created_utc": 1778754300,
                    "permalink": "/r/test/comments/abc123/comment123/",
                    "replies": {
                        "data": {
                            "children": [
                                {"kind": "t1", "data": {"id": "reply1"}},
                                {"kind": "more", "data": {}},
                            ]
                        }
                    },
                },
            }
        ][:limit]


def test_base_adapter_contract_includes_safe_adapter_operations() -> None:
    required_operations = {
        "search_posts",
        "fetch_comments",
        "normalize_post",
        "normalize_comment",
        "health_check",
        "supports_real_mode",
        "get_required_credentials",
    }

    for operation in required_operations:
        assert hasattr(BasePlatformAdapter, operation)
        assert callable(getattr(BasePlatformAdapter, operation))


def test_reddit_adapter_defaults_to_mock_mode_without_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("REDDIT_CLIENT_ID", raising=False)
    monkeypatch.delenv("REDDIT_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("REDDIT_USER_AGENT", raising=False)

    adapter = RedditAdapter(mode="real")
    posts = adapter.search_posts("Tesla", limit=5)
    comments = adapter.fetch_comments("post_001", limit=5)

    assert adapter.mode == "mock"
    assert adapter.fallback_reason == "missing_reddit_credentials"
    assert posts
    assert comments
    assert all(isinstance(post, RawPost) for post in posts)
    assert all(isinstance(comment, RawComment) for comment in comments)
    assert all(post.platform == "reddit" for post in posts)
    assert all(comment.platform == "reddit" for comment in comments)


def test_reddit_adapter_uses_env_mode_and_falls_back_without_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("REDDIT_ADAPTER_MODE", "real")
    monkeypatch.delenv("REDDIT_CLIENT_ID", raising=False)
    monkeypatch.delenv("REDDIT_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("REDDIT_USER_AGENT", raising=False)

    adapter = RedditAdapter()
    health = adapter.health_check()

    assert adapter.requested_mode == "real"
    assert adapter.mode == "mock"
    assert adapter.supports_real_mode() is False
    assert adapter.get_required_credentials() == REDDIT_REQUIRED_CREDENTIALS
    assert isinstance(health, AdapterHealth)
    assert health.ok is True
    assert health.real_mode_available is False
    assert health.fallback_reason == "missing_reddit_credentials"


def test_reddit_adapter_normalizes_mocked_reddit_payloads() -> None:
    adapter = RedditAdapter(mode="mock")
    raw_post = FakeRedditClient().search_posts("Tesla", limit=1, sort="new")[0]
    raw_comment = FakeRedditClient().fetch_comments("t3_abc123", limit=1)[0]

    post = adapter.normalize_post(raw_post)
    comment = adapter.normalize_comment(raw_comment)

    assert post.platform == "reddit"
    assert post.post_id == "t3_abc123"
    assert post.author_id == "t2_public"
    assert post.title == "Tesla quality discussion"
    assert post.like_count == 42
    assert post.reply_count == 3
    assert post.url == "https://www.reddit.com/r/test/comments/abc123/quality_discussion/"
    assert "101" in post.raw_data

    assert comment.platform == "reddit"
    assert comment.post_id == "t3_abc123"
    assert comment.comment_id == "t1_comment123"
    assert comment.parent_id is None
    assert comment.author_id == "t2_comment_author"
    assert comment.reply_count == 1
    assert comment.url == "https://www.reddit.com/r/test/comments/abc123/comment123/"


def test_reddit_adapter_real_mode_uses_mocked_client_when_credentials_exist() -> None:
    adapter = RedditAdapter(
        mode="real",
        credentials=RedditCredentials(
            client_id="client",
            client_secret="secret",
            user_agent="sentigraph-test",
        ),
        http_client=FakeRedditClient(),
    )

    posts = adapter.search_posts("Tesla", limit=1, sort="new")
    comments = adapter.fetch_comments(posts[0].post_id, limit=1)

    assert adapter.mode == "real"
    assert adapter.real_mode_available is True
    assert adapter.supports_real_mode() is True
    assert adapter.health_check().real_mode_available is True
    assert posts[0].post_id == "t3_abc123"
    assert comments[0].post_id == "t3_abc123"
    assert comments[0].content == "This is a public Reddit comment."


def test_adapter_factory_registers_reddit_only_for_now() -> None:
    adapter = get_platform_adapter("reddit")
    alias_adapter = get_adapter("Reddit")

    assert has_platform_adapter("reddit") is True
    assert get_supported_adapter_ids() == ["reddit"]
    assert isinstance(adapter, RedditAdapter)
    assert isinstance(alias_adapter, RedditAdapter)
    assert adapter.mode == "mock"
    assert alias_adapter.mode == "mock"

    with pytest.raises(PlatformAdapterError):
        get_platform_adapter("weibo")


def test_adapter_factory_does_not_activate_planned_or_crawler_later_platforms() -> None:
    inactive_adapter_platforms = [
        platform.platform_id
        for platform in get_platform_registry()
        if platform.platform_id != "reddit"
    ]

    assert inactive_adapter_platforms

    for platform_id in inactive_adapter_platforms:
        assert has_platform_adapter(platform_id) is False
        with pytest.raises(PlatformAdapterError):
            get_adapter(platform_id)
