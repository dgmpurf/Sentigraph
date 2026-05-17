from __future__ import annotations

from typing import Any, Mapping

import pytest

from app.schemas.comment import RawComment, RawPost
from app.services.crawling.adapter_factory import get_adapter, has_platform_adapter
from app.services.crawling.douyin_adapter import (
    DOUYIN_API_APPROVAL_STATUS,
    DOUYIN_COMMENT_API_STATUS,
    DOUYIN_DEVELOPER_ACCESS_STATUS,
    DOUYIN_REAL_MODE_BLOCKER,
    DOUYIN_REQUIRED_CREDENTIALS,
    DouyinAdapter,
    DouyinCredentials,
)


def test_douyin_adapter_mock_search_posts(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOUYIN_ADAPTER_MODE", "mock")
    monkeypatch.delenv("DOUYIN_CLIENT_KEY", raising=False)
    monkeypatch.delenv("DOUYIN_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("DOUYIN_ACCESS_TOKEN", raising=False)

    adapter = DouyinAdapter()
    posts = adapter.search_posts("Tesla", limit=3, sort="new")

    assert adapter.get_mode() == "mock"
    assert adapter.fallback_reason == ""
    assert posts
    assert len(posts) == 3
    assert all(isinstance(post, RawPost) for post in posts)
    assert all(post.platform == "douyin" for post in posts)
    assert posts[0].post_id.startswith("douyin_mock_video_")
    assert posts[0].raw_data["mode"] == "mock"


def test_douyin_adapter_mock_fetch_comments() -> None:
    adapter = DouyinAdapter(mode="mock")
    comments = adapter.fetch_comments("douyin_mock_video_001", limit=2)

    assert len(comments) == 2
    assert all(isinstance(comment, RawComment) for comment in comments)
    assert all(comment.platform == "douyin" for comment in comments)
    assert all(comment.post_id == "douyin_mock_video_001" for comment in comments)
    assert comments[0].raw_data["mode"] == "mock"


def test_douyin_adapter_interface_and_health_contract() -> None:
    adapter = DouyinAdapter(mode="mock")

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

    assert health.platform_id == "douyin"
    assert health.mode == "mock"
    assert health.ok is True
    assert health.real_mode_available is False
    assert "mock mode" in health.message
    assert adapter.supports_real_mode() is False
    assert adapter.get_required_credentials() == DOUYIN_REQUIRED_CREDENTIALS


def test_douyin_mock_output_contains_expected_raw_schema_fields() -> None:
    adapter = DouyinAdapter(mode="mock")
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

    assert RawPost.model_validate(post_data).platform == "douyin"
    assert RawComment.model_validate(comment_data).platform == "douyin"
    assert post.share_count >= 0
    assert comment.reply_count >= 0


def test_douyin_adapter_normalizes_real_like_video_payload() -> None:
    adapter = DouyinAdapter(mode="mock")
    raw_post: Mapping[str, Any] = {
        "data": {
            "aweme_id": "douyin_fixture_001",
            "title": "Tesla short-video review",
            "desc": "Public Douyin fixture content.",
            "author": {"uid": "creator_001", "nickname": "fixture_creator"},
            "statistics": {"digg_count": 188, "comment_count": 16, "share_count": 9},
            "create_time": 1778754000,
            "share_url": "https://www.douyin.com/video/douyin_fixture_001",
            101: "integer key should be stringified",
        }
    }
    raw_comment: Mapping[str, Any] = {
        "data": {
            "cid": "comment_001",
            "aweme_id": "douyin_fixture_001",
            "reply_id": "0",
            "user": {"uid": "commenter_001", "nickname": "fixture_commenter"},
            "text": "Public Douyin comment fixture.",
            "digg_count": 21,
            "reply_comment_total": 3,
            "create_time": 1778754300,
        }
    }

    post = adapter.normalize_post(raw_post)
    comment = adapter.normalize_comment(raw_comment)

    assert post.platform == "douyin"
    assert post.post_id == "douyin_fixture_001"
    assert post.author_id == "creator_001"
    assert post.author_name == "fixture_creator"
    assert post.like_count == 188
    assert post.reply_count == 16
    assert post.share_count == 9
    assert "101" in post.raw_data

    assert comment.platform == "douyin"
    assert comment.post_id == "douyin_fixture_001"
    assert comment.comment_id == "comment_001"
    assert comment.author_id == "commenter_001"
    assert comment.author_name == "fixture_commenter"
    assert comment.like_count == 21
    assert comment.reply_count == 3


def test_douyin_real_mode_missing_credentials_does_not_crash(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOUYIN_ADAPTER_MODE", "real")
    monkeypatch.delenv("DOUYIN_CLIENT_KEY", raising=False)
    monkeypatch.delenv("DOUYIN_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("DOUYIN_ACCESS_TOKEN", raising=False)

    adapter = DouyinAdapter()
    posts = adapter.search_posts("Tesla", limit=1)
    metadata = adapter.get_status_metadata()

    assert adapter.requested_mode == "real"
    assert adapter.get_mode() == "mock"
    assert adapter.has_required_credentials() is False
    assert adapter.is_real_mode_enabled() is False
    assert adapter.supports_real_mode() is False
    assert adapter.get_required_credentials() == DOUYIN_REQUIRED_CREDENTIALS
    assert adapter.fallback_reason == "config_error:missing_douyin_credentials"
    assert metadata["sanitized_error_category"] == "config_error"
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert metadata["api_approval_status"] == DOUYIN_API_APPROVAL_STATUS
    assert metadata["developer_access_status"] == DOUYIN_DEVELOPER_ACCESS_STATUS
    assert metadata["comment_api_status"] == DOUYIN_COMMENT_API_STATUS
    assert metadata["real_mode_blocker"] == DOUYIN_REAL_MODE_BLOCKER
    assert posts[0].platform == "douyin"


def test_douyin_real_mode_returns_api_pending_without_network(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOUYIN_ADAPTER_MODE", "real")

    adapter = DouyinAdapter(
        credentials=DouyinCredentials(
            client_key="client",
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
    assert adapter.fallback_reason == "api_pending:permission_not_verified"
    assert health.real_mode_available is False
    assert metadata["fetch_status"] == "api_pending"
    assert metadata["sanitized_error_category"] == "api_pending"
    assert metadata["api_approval_status"] == DOUYIN_API_APPROVAL_STATUS
    assert metadata["developer_access_status"] == DOUYIN_DEVELOPER_ACCESS_STATUS
    assert metadata["comment_api_status"] == DOUYIN_COMMENT_API_STATUS
    assert metadata["real_mode_blocker"] == DOUYIN_REAL_MODE_BLOCKER
    assert metadata["real_mode_reached"] is False
    assert posts[0].raw_data["mode"] == "mock"


def test_adapter_factory_registers_douyin() -> None:
    adapter = get_adapter("douyin")

    assert has_platform_adapter("douyin") is True
    assert isinstance(adapter, DouyinAdapter)
