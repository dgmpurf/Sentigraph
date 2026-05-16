from __future__ import annotations

from typing import Any, Mapping

import pytest

from app.schemas.comment import RawComment, RawPost
from app.services.crawling.adapter_factory import get_adapter, has_platform_adapter
from app.services.crawling.weibo_adapter import (
    WEIBO_REQUIRED_CREDENTIALS,
    WeiboAdapter,
    WeiboCredentials,
)


def test_weibo_adapter_mock_search_posts(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WEIBO_ADAPTER_MODE", "mock")
    monkeypatch.delenv("WEIBO_CLIENT_ID", raising=False)
    monkeypatch.delenv("WEIBO_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("WEIBO_ACCESS_TOKEN", raising=False)

    adapter = WeiboAdapter()
    posts = adapter.search_posts("Tesla", limit=3, sort="new")

    assert adapter.get_mode() == "mock"
    assert adapter.fallback_reason == ""
    assert posts
    assert len(posts) == 3
    assert all(isinstance(post, RawPost) for post in posts)
    assert all(post.platform == "weibo" for post in posts)
    assert posts[0].post_id.startswith("weibo_mock_status_")
    assert posts[0].raw_data["mode"] == "mock"


def test_weibo_adapter_mock_fetch_comments() -> None:
    adapter = WeiboAdapter(mode="mock")
    comments = adapter.fetch_comments("weibo_mock_status_001", limit=2)

    assert len(comments) == 2
    assert all(isinstance(comment, RawComment) for comment in comments)
    assert all(comment.platform == "weibo" for comment in comments)
    assert all(comment.post_id == "weibo_mock_status_001" for comment in comments)
    assert comments[0].raw_data["mode"] == "mock"


def test_weibo_adapter_interface_and_health_contract() -> None:
    adapter = WeiboAdapter(mode="mock")

    for method_name in (
        "search_posts",
        "fetch_comments",
        "normalize_post",
        "normalize_comment",
        "health_check",
        "supports_real_mode",
        "get_required_credentials",
    ):
        assert callable(getattr(adapter, method_name))

    health = adapter.health_check()

    assert health.platform_id == "weibo"
    assert health.mode == "mock"
    assert health.ok is True
    assert health.real_mode_available is False
    assert "mock mode" in health.message
    assert adapter.supports_real_mode() is False
    assert adapter.get_required_credentials() == WEIBO_REQUIRED_CREDENTIALS


def test_weibo_mock_output_contains_expected_raw_schema_fields() -> None:
    adapter = WeiboAdapter(mode="mock")
    post = adapter.search_posts("Tesla", limit=1, sort="new")[0]
    comment = adapter.fetch_comments(post.post_id, limit=1)[0]

    post_data = post.model_dump(mode="json")
    comment_data = comment.model_dump(mode="json")

    for field_name in (
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
    ):
        assert field_name in post_data

    for field_name in (
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
    ):
        assert field_name in comment_data

    assert RawPost.model_validate(post_data).platform == "weibo"
    assert RawComment.model_validate(comment_data).platform == "weibo"
    assert post.share_count >= 0
    assert comment.reply_count >= 0


def test_weibo_adapter_normalizes_real_like_status_payload() -> None:
    adapter = WeiboAdapter(mode="mock")
    raw_post: Mapping[str, Any] = {
        "data": {
            "idstr": "status_fixture_001",
            "title": "#Tesla# launch review",
            "text": "Public Weibo fixture content.",
            "user": {"idstr": "user_001", "screen_name": "fixture_author"},
            "attitudes_count": 88,
            "comments_count": 6,
            "reposts_count": 3,
            "created_at": 1778754000,
            "url": "https://weibo.com/status_fixture_001",
            101: "integer key should be stringified",
        }
    }
    raw_comment: Mapping[str, Any] = {
        "data": {
            "idstr": "comment_001",
            "status_id": "status_fixture_001",
            "rootid": "0",
            "user": {"idstr": "commenter_001", "screen_name": "fixture_commenter"},
            "text": "Public Weibo comment fixture.",
            "like_counts": 11,
            "comments_count": 2,
            "created_at": 1778754300,
        }
    }

    post = adapter.normalize_post(raw_post)
    comment = adapter.normalize_comment(raw_comment)

    assert post.platform == "weibo"
    assert post.post_id == "status_fixture_001"
    assert post.author_id == "user_001"
    assert post.author_name == "fixture_author"
    assert post.like_count == 88
    assert post.reply_count == 6
    assert post.share_count == 3
    assert "101" in post.raw_data

    assert comment.platform == "weibo"
    assert comment.post_id == "status_fixture_001"
    assert comment.comment_id == "comment_001"
    assert comment.author_id == "commenter_001"
    assert comment.author_name == "fixture_commenter"
    assert comment.like_count == 11
    assert comment.reply_count == 2


def test_weibo_real_mode_missing_credentials_does_not_crash(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WEIBO_ADAPTER_MODE", "real")
    monkeypatch.delenv("WEIBO_CLIENT_ID", raising=False)
    monkeypatch.delenv("WEIBO_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("WEIBO_ACCESS_TOKEN", raising=False)

    adapter = WeiboAdapter()
    posts = adapter.search_posts("Tesla", limit=1)
    metadata = adapter.get_status_metadata()

    assert adapter.requested_mode == "real"
    assert adapter.get_mode() == "mock"
    assert adapter.has_required_credentials() is False
    assert adapter.is_real_mode_enabled() is False
    assert adapter.supports_real_mode() is False
    assert adapter.get_required_credentials() == WEIBO_REQUIRED_CREDENTIALS
    assert adapter.fallback_reason == "config_error:missing_weibo_credentials"
    assert metadata["sanitized_error_category"] == "config_error"
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert posts[0].platform == "weibo"


def test_weibo_real_mode_returns_api_pending_without_network(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WEIBO_ADAPTER_MODE", "real")

    adapter = WeiboAdapter(
        credentials=WeiboCredentials(
            client_id="client",
            client_secret="secret",
            access_token="token",
        )
    )
    posts = adapter.search_posts("Tesla", limit=1)
    health = adapter.health_check()
    metadata = adapter.get_status_metadata()

    assert adapter.get_mode() == "mock"
    assert adapter.has_required_credentials() is True
    assert adapter.is_real_mode_enabled() is False
    assert adapter.supports_real_mode() is False
    assert adapter.fallback_reason == "api_pending:weibo_official_api_not_implemented"
    assert health.real_mode_available is False
    assert metadata["fetch_status"] == "api_pending"
    assert metadata["sanitized_error_category"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert posts[0].raw_data["mode"] == "mock"


def test_adapter_factory_registers_weibo() -> None:
    adapter = get_adapter("weibo")

    assert has_platform_adapter("weibo") is True
    assert isinstance(adapter, WeiboAdapter)
