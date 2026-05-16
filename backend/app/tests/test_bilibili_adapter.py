from __future__ import annotations

from typing import Any, Mapping

import pytest

from app.schemas.comment import RawComment, RawPost
from app.services.crawling.adapter_factory import get_adapter, has_platform_adapter
from app.services.crawling.bilibili_adapter import (
    BILIBILI_REQUIRED_CREDENTIALS,
    BilibiliAdapter,
    BilibiliCredentials,
)


def test_bilibili_adapter_mock_search_posts(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILIBILI_ADAPTER_MODE", "mock")
    monkeypatch.delenv("BILIBILI_CLIENT_ID", raising=False)
    monkeypatch.delenv("BILIBILI_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("BILIBILI_ACCESS_TOKEN", raising=False)

    adapter = BilibiliAdapter()
    posts = adapter.search_posts("Tesla", limit=3, sort="new")

    assert adapter.get_mode() == "mock"
    assert adapter.fallback_reason == ""
    assert posts
    assert len(posts) == 3
    assert all(isinstance(post, RawPost) for post in posts)
    assert all(post.platform == "bilibili" for post in posts)
    assert posts[0].post_id.startswith("BV")
    assert posts[0].raw_data["mode"] == "mock"


def test_bilibili_adapter_mock_fetch_comments() -> None:
    adapter = BilibiliAdapter(mode="mock")
    comments = adapter.fetch_comments("BV1sentigraph001", limit=2)

    assert len(comments) == 2
    assert all(isinstance(comment, RawComment) for comment in comments)
    assert all(comment.platform == "bilibili" for comment in comments)
    assert all(comment.post_id == "BV1sentigraph001" for comment in comments)
    assert comments[0].raw_data["mode"] == "mock"


def test_bilibili_adapter_normalizes_real_like_video_payload() -> None:
    adapter = BilibiliAdapter(mode="mock")
    raw_post: Mapping[str, Any] = {
        "data": {
            "bvid": "BV1fixture001",
            "title": "Tesla launch review",
            "description": "Public video fixture content.",
            "owner": {"mid": "up_001", "name": "fixture_uploader"},
            "stat": {"like": 88, "reply": 6, "share": 3},
            "pubdate": 1778754000,
            "url": "https://www.bilibili.com/video/BV1fixture001",
            101: "integer key should be stringified",
        }
    }
    raw_comment: Mapping[str, Any] = {
        "data": {
            "rpid": "reply_001",
            "oid": "BV1fixture001",
            "parent": "0",
            "member": {"mid": "user_001", "uname": "fixture_commenter"},
            "message": "Public Bilibili comment fixture.",
            "like": 11,
            "reply": 2,
            "ctime": 1778754300,
        }
    }

    post = adapter.normalize_post(raw_post)
    comment = adapter.normalize_comment(raw_comment)

    assert post.platform == "bilibili"
    assert post.post_id == "BV1fixture001"
    assert post.author_id == "up_001"
    assert post.author_name == "fixture_uploader"
    assert post.like_count == 88
    assert post.reply_count == 6
    assert post.share_count == 3
    assert "101" in post.raw_data

    assert comment.platform == "bilibili"
    assert comment.post_id == "BV1fixture001"
    assert comment.comment_id == "reply_001"
    assert comment.author_id == "user_001"
    assert comment.author_name == "fixture_commenter"
    assert comment.like_count == 11
    assert comment.reply_count == 2


def test_bilibili_real_mode_missing_credentials_does_not_crash(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILIBILI_ADAPTER_MODE", "real")
    monkeypatch.delenv("BILIBILI_CLIENT_ID", raising=False)
    monkeypatch.delenv("BILIBILI_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("BILIBILI_ACCESS_TOKEN", raising=False)

    adapter = BilibiliAdapter()
    posts = adapter.search_posts("Tesla", limit=1)
    metadata = adapter.get_status_metadata()

    assert adapter.requested_mode == "real"
    assert adapter.get_mode() == "mock"
    assert adapter.has_required_credentials() is False
    assert adapter.is_real_mode_enabled() is False
    assert adapter.supports_real_mode() is False
    assert adapter.get_required_credentials() == BILIBILI_REQUIRED_CREDENTIALS
    assert adapter.fallback_reason == "config_error:missing_bilibili_credentials"
    assert metadata["sanitized_error_category"] == "config_error"
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert posts[0].platform == "bilibili"


def test_bilibili_real_mode_returns_api_pending_without_network(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILIBILI_ADAPTER_MODE", "real")

    adapter = BilibiliAdapter(
        credentials=BilibiliCredentials(
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
    assert adapter.fallback_reason == "api_pending:bilibili_official_api_not_implemented"
    assert health.real_mode_available is False
    assert metadata["fetch_status"] == "api_pending"
    assert metadata["sanitized_error_category"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert posts[0].raw_data["mode"] == "mock"


def test_adapter_factory_registers_bilibili() -> None:
    adapter = get_adapter("bilibili")

    assert has_platform_adapter("bilibili") is True
    assert isinstance(adapter, BilibiliAdapter)
