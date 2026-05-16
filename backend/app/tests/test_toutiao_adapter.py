from __future__ import annotations

import pytest

from app.schemas.comment import RawComment, RawPost
from app.services.crawling.adapter_factory import get_adapter, has_platform_adapter
from app.services.crawling.toutiao_adapter import (
    TOUTIAO_REQUIRED_CREDENTIALS,
    ToutiaoAdapter,
    ToutiaoCredentials,
)


def test_toutiao_adapter_defaults_to_mock_mode_without_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TOUTIAO_ADAPTER_MODE", "mock")
    monkeypatch.delenv("TOUTIAO_CLIENT_ID", raising=False)
    monkeypatch.delenv("TOUTIAO_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("TOUTIAO_ACCESS_TOKEN", raising=False)

    adapter = ToutiaoAdapter()
    posts = adapter.search_posts("Tesla", limit=5)
    comments = adapter.fetch_comments(posts[0].post_id, limit=5)

    assert adapter.get_mode() == "mock"
    assert adapter.fallback_reason == ""
    assert posts
    assert comments
    assert all(isinstance(post, RawPost) for post in posts)
    assert all(isinstance(comment, RawComment) for comment in comments)
    assert all(post.platform == "toutiao" for post in posts)
    assert all(comment.platform == "toutiao" for comment in comments)


def test_toutiao_adapter_mock_search_posts_are_normalized() -> None:
    adapter = ToutiaoAdapter(mode="mock")
    posts = adapter.search_posts("Tesla", limit=3, sort="new", date_range={"start": "2026-05-01"})

    assert len(posts) == 3
    first = posts[0]
    assert first.platform == "toutiao"
    assert first.post_id == "toutiao_mock_article_001"
    assert first.author_id == "toutiao_mock_author_001"
    assert first.author_name == "Mock Toutiao News"
    assert first.title == "Tesla news article public reaction"
    assert first.content
    assert first.like_count == 512
    assert first.reply_count == 86
    assert first.share_count == 27
    assert first.created_at == "2026-05-15T08:45:00Z"
    assert first.url == "https://www.toutiao.com/article/toutiao_mock_article_001/"
    assert first.raw_data["mode"] == "mock"


def test_toutiao_adapter_mock_fetch_comments_are_normalized() -> None:
    adapter = ToutiaoAdapter(mode="mock")
    comments = adapter.fetch_comments("toutiao_mock_article_001", limit=3)

    assert len(comments) == 3
    first = comments[0]
    assert first.platform == "toutiao"
    assert first.post_id == "toutiao_mock_article_001"
    assert first.comment_id == "toutiao_mock_article_001_comment_001"
    assert first.parent_id is None
    assert first.author_id == "toutiao_mock_commenter_001"
    assert first.author_name == "mock_toutiao_user_a"
    assert first.content
    assert first.like_count == 64
    assert first.reply_count == 5
    assert first.created_at == "2026-05-15T08:55:00Z"
    assert first.url == "https://www.toutiao.com/article/toutiao_mock_article_001/#comment001"
    assert first.raw_data["mode"] == "mock"


def test_toutiao_adapter_interface_and_health_check() -> None:
    adapter = ToutiaoAdapter(mode="mock")
    health = adapter.health_check()

    assert callable(adapter.search_posts)
    assert callable(adapter.fetch_comments)
    assert callable(adapter.normalize_post)
    assert callable(adapter.normalize_comment)
    assert callable(adapter.health_check)
    assert adapter.supports_real_mode() is False
    assert adapter.get_required_credentials() == TOUTIAO_REQUIRED_CREDENTIALS
    assert health.ok is True
    assert health.mode == "mock"
    assert health.real_mode_available is False


def test_toutiao_normalizes_official_api_like_payloads() -> None:
    adapter = ToutiaoAdapter(mode="mock")

    post = adapter.normalize_post(
        {
            "data": {
                "article_id": "article_123",
                "author": {"id": "author_123", "name": "Toutiao Author"},
                "title": "Toutiao topic summary",
                "abstract": "A public article summary.",
                "statistics": {
                    "like_count": 42,
                    "comment_count": 7,
                    "share_count": 3,
                },
                "publish_time": "2026-05-15T11:00:00Z",
                "url": "https://www.toutiao.com/article/article_123/",
                101: "integer key should be stringified",
            }
        }
    )
    comment = adapter.normalize_comment(
        {
            "data": {
                "article_id": "article_123",
                "comment_id": "comment_123",
                "author": {"uid": "commenter_123", "name": "Comment Author"},
                "text": "A public comment.",
                "digg_count": 9,
                "child_comment_count": 2,
                "created_at": "2026-05-15T11:10:00Z",
            }
        }
    )

    assert post.platform == "toutiao"
    assert post.post_id == "article_123"
    assert post.author_id == "author_123"
    assert post.author_name == "Toutiao Author"
    assert post.like_count == 42
    assert post.reply_count == 7
    assert post.share_count == 3
    assert "101" in post.raw_data

    assert comment.platform == "toutiao"
    assert comment.post_id == "article_123"
    assert comment.comment_id == "comment_123"
    assert comment.author_id == "commenter_123"
    assert comment.author_name == "Comment Author"
    assert comment.like_count == 9
    assert comment.reply_count == 2


def test_toutiao_real_mode_without_credentials_returns_safe_config_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TOUTIAO_ADAPTER_MODE", "real")
    monkeypatch.delenv("TOUTIAO_CLIENT_ID", raising=False)
    monkeypatch.delenv("TOUTIAO_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("TOUTIAO_ACCESS_TOKEN", raising=False)

    adapter = ToutiaoAdapter()
    metadata = adapter.get_status_metadata()

    assert adapter.get_mode() == "mock"
    assert adapter.has_required_credentials() is False
    assert adapter.supports_real_mode() is False
    assert adapter.fallback_reason == "config_error:missing_toutiao_credentials"
    assert metadata["sanitized_error_category"] == "config_error"
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert metadata["credentials_present"] == {
        "TOUTIAO_CLIENT_ID": False,
        "TOUTIAO_CLIENT_SECRET": False,
        "TOUTIAO_ACCESS_TOKEN": False,
    }


def test_toutiao_real_mode_with_credentials_stays_api_pending_without_network(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TOUTIAO_ADAPTER_MODE", "real")

    adapter = ToutiaoAdapter(
        credentials=ToutiaoCredentials(
            client_id="client",
            client_secret="secret",
            access_token="token",
        )
    )
    posts = adapter.search_posts("Tesla", limit=1)
    metadata = adapter.get_status_metadata()

    assert adapter.get_mode() == "mock"
    assert adapter.has_required_credentials() is True
    assert adapter.supports_real_mode() is False
    assert adapter.fallback_reason == "api_pending:toutiao_official_api_not_implemented"
    assert metadata["sanitized_error_category"] == "api_pending"
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert posts[0].raw_data["mode"] == "mock"


def test_adapter_factory_registers_toutiao() -> None:
    assert has_platform_adapter("toutiao") is True
    adapter = get_adapter("toutiao")
    assert isinstance(adapter, ToutiaoAdapter)
