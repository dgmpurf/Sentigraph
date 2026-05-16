from __future__ import annotations

from typing import Any, Mapping

import pytest

from app.schemas.comment import RawComment, RawPost
from app.services.crawling.adapter_factory import get_adapter, has_platform_adapter
from app.services.crawling.douban_adapter import (
    DOUBAN_REQUIRED_CREDENTIALS,
    DoubanAdapter,
    DoubanCredentials,
)


def test_douban_adapter_mock_search_posts(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOUBAN_ADAPTER_MODE", "mock")
    monkeypatch.delenv("DOUBAN_CLIENT_ID", raising=False)
    monkeypatch.delenv("DOUBAN_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("DOUBAN_ACCESS_TOKEN", raising=False)

    adapter = DoubanAdapter()
    posts = adapter.search_posts("Tesla", limit=3, sort="new")

    assert adapter.get_mode() == "mock"
    assert adapter.fallback_reason == ""
    assert posts
    assert len(posts) == 3
    assert all(isinstance(post, RawPost) for post in posts)
    assert all(post.platform == "douban" for post in posts)
    assert posts[0].post_id.startswith("douban_mock_")
    assert posts[0].raw_data["mode"] == "mock"


def test_douban_adapter_mock_fetch_comments() -> None:
    adapter = DoubanAdapter(mode="mock")
    comments = adapter.fetch_comments("douban_mock_topic_001", limit=2)

    assert len(comments) == 2
    assert all(isinstance(comment, RawComment) for comment in comments)
    assert all(comment.platform == "douban" for comment in comments)
    assert all(comment.post_id == "douban_mock_topic_001" for comment in comments)
    assert comments[0].raw_data["mode"] == "mock"


def test_douban_adapter_interface_and_health_contract() -> None:
    adapter = DoubanAdapter(mode="mock")

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

    assert health.platform_id == "douban"
    assert health.mode == "mock"
    assert health.ok is True
    assert health.real_mode_available is False
    assert "mock mode" in health.message
    assert adapter.supports_real_mode() is False
    assert adapter.get_required_credentials() == DOUBAN_REQUIRED_CREDENTIALS


def test_douban_mock_output_contains_expected_raw_schema_fields() -> None:
    adapter = DoubanAdapter(mode="mock")
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

    assert RawPost.model_validate(post_data).platform == "douban"
    assert RawComment.model_validate(comment_data).platform == "douban"
    assert post.share_count >= 0
    assert comment.reply_count >= 0


def test_douban_adapter_normalizes_real_like_topic_payload() -> None:
    adapter = DoubanAdapter(mode="mock")
    raw_post: Mapping[str, Any] = {
        "data": {
            "topic_id": "douban_fixture_topic_001",
            "subject": {"id": "subject_001", "title": "Tesla Douban group topic"},
            "content": "Public Douban fixture topic content.",
            "author": {"id": "author_001", "name": "fixture_author"},
            "statistics": {"like_count": 88, "comment_count": 24, "share_count": 7},
            "created_time": 1778754000,
            "url": "https://www.douban.com/group/topic/douban_fixture_topic_001/",
            101: "integer key should be stringified",
        }
    }
    raw_comment: Mapping[str, Any] = {
        "data": {
            "id": "comment_001",
            "topic_id": "douban_fixture_topic_001",
            "reply_to_comment_id": "0",
            "author": {"id": "commenter_001", "name": "fixture_commenter"},
            "content": "Public Douban comment fixture.",
            "useful_count": 33,
            "child_comment_count": 5,
            "created_time": 1778754300,
        }
    }

    post = adapter.normalize_post(raw_post)
    comment = adapter.normalize_comment(raw_comment)

    assert post.platform == "douban"
    assert post.post_id == "douban_fixture_topic_001"
    assert post.author_id == "author_001"
    assert post.author_name == "fixture_author"
    assert post.title == "Tesla Douban group topic"
    assert post.like_count == 88
    assert post.reply_count == 24
    assert post.share_count == 7
    assert "101" in post.raw_data

    assert comment.platform == "douban"
    assert comment.post_id == "douban_fixture_topic_001"
    assert comment.comment_id == "comment_001"
    assert comment.author_id == "commenter_001"
    assert comment.author_name == "fixture_commenter"
    assert comment.like_count == 33
    assert comment.reply_count == 5


def test_douban_real_mode_missing_credentials_does_not_crash(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOUBAN_ADAPTER_MODE", "real")
    monkeypatch.delenv("DOUBAN_CLIENT_ID", raising=False)
    monkeypatch.delenv("DOUBAN_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("DOUBAN_ACCESS_TOKEN", raising=False)

    adapter = DoubanAdapter()
    posts = adapter.search_posts("Tesla", limit=1)
    metadata = adapter.get_status_metadata()

    assert adapter.requested_mode == "real"
    assert adapter.get_mode() == "mock"
    assert adapter.has_required_credentials() is False
    assert adapter.is_real_mode_enabled() is False
    assert adapter.supports_real_mode() is False
    assert adapter.get_required_credentials() == DOUBAN_REQUIRED_CREDENTIALS
    assert adapter.fallback_reason == "config_error:missing_douban_credentials"
    assert metadata["sanitized_error_category"] == "config_error"
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert posts[0].platform == "douban"


def test_douban_real_mode_returns_api_pending_without_network(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOUBAN_ADAPTER_MODE", "real")

    adapter = DoubanAdapter(
        credentials=DoubanCredentials(
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
    assert adapter.fallback_reason == "api_pending:douban_official_api_not_implemented"
    assert health.real_mode_available is False
    assert metadata["fetch_status"] == "api_pending"
    assert metadata["sanitized_error_category"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert posts[0].raw_data["mode"] == "mock"


def test_adapter_factory_registers_douban() -> None:
    adapter = get_adapter("douban")

    assert has_platform_adapter("douban") is True
    assert isinstance(adapter, DoubanAdapter)
