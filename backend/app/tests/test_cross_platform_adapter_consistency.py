from __future__ import annotations

import urllib.request
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.comment import RawComment, RawPost
from app.services.crawling.adapter_factory import (
    get_adapter,
    get_supported_adapter_ids,
    has_platform_adapter,
)
from app.services.crawling.base_adapter import PlatformAdapterError
from app.services.crawling.bilibili_adapter import BilibiliAdapter
from app.services.crawling.douban_adapter import DoubanAdapter
from app.services.crawling.douyin_adapter import DouyinAdapter
from app.services.crawling.kuaishou_adapter import KuaishouAdapter
from app.services.crawling.public_parser.parser_registry import get_public_parser_platform_ids
from app.services.crawling.public_parser.public_parser_adapter import PublicParserPlatformAdapter
from app.services.crawling.reddit_adapter import RedditAdapter
from app.services.crawling.toutiao_adapter import ToutiaoAdapter
from app.services.crawling.weibo_adapter import WeiboAdapter
from app.services.crawling.xiaohongshu_adapter import XiaohongshuAdapter
from app.services.crawling.youtube_adapter import YouTubeAdapter
from app.services.crawling.zhihu_adapter import ZhihuAdapter


client = TestClient(app)


OFFICIAL_PLATFORM_CONFIG: dict[str, dict[str, Any]] = {
    "bilibili": {
        "class": BilibiliAdapter,
        "mode_env": "BILIBILI_ADAPTER_MODE",
        "credentials": (
            "BILIBILI_CLIENT_ID",
            "BILIBILI_CLIENT_SECRET",
            "BILIBILI_ACCESS_TOKEN",
        ),
    },
    "weibo": {
        "class": WeiboAdapter,
        "mode_env": "WEIBO_ADAPTER_MODE",
        "credentials": (
            "WEIBO_CLIENT_ID",
            "WEIBO_CLIENT_SECRET",
            "WEIBO_ACCESS_TOKEN",
        ),
    },
    "douyin": {
        "class": DouyinAdapter,
        "mode_env": "DOUYIN_ADAPTER_MODE",
        "credentials": (
            "DOUYIN_CLIENT_KEY",
            "DOUYIN_CLIENT_SECRET",
            "DOUYIN_REDIRECT_URI",
            "DOUYIN_ACCESS_TOKEN",
            "DOUYIN_REFRESH_TOKEN",
        ),
        "api_approval_status": "developer_access_obtained_permission_unverified",
        "developer_access_status": "obtained",
        "app_type": "web_app",
        "comment_api_status": "item_comment_scope_not_verified",
        "recommended_comment_scope": "item.comment",
        "video_comment_scope_status": "not_recommended_for_mvp",
        "real_mode_blocker": "oauth_and_scope_not_verified",
        "real_mode_blocked_reason_when_credentials": "permission_not_verified",
    },
    "kuaishou": {
        "class": KuaishouAdapter,
        "mode_env": "KUAISHOU_ADAPTER_MODE",
        "credentials": (
            "KUAISHOU_CLIENT_ID",
            "KUAISHOU_CLIENT_SECRET",
            "KUAISHOU_ACCESS_TOKEN",
        ),
    },
    "xiaohongshu": {
        "class": XiaohongshuAdapter,
        "mode_env": "XIAOHONGSHU_ADAPTER_MODE",
        "credentials": (
            "XIAOHONGSHU_CLIENT_ID",
            "XIAOHONGSHU_CLIENT_SECRET",
            "XIAOHONGSHU_ACCESS_TOKEN",
        ),
        "api_approval_status": "developer_access_obtained_permission_unverified",
        "developer_access_status": "obtained",
        "comment_api_status": "unknown_or_not_confirmed",
        "real_mode_blocker": "permission_not_verified",
    },
    "zhihu": {
        "class": ZhihuAdapter,
        "mode_env": "ZHIHU_ADAPTER_MODE",
        "credentials": (
            "ZHIHU_CLIENT_ID",
            "ZHIHU_CLIENT_SECRET",
            "ZHIHU_ACCESS_TOKEN",
        ),
    },
    "douban": {
        "class": DoubanAdapter,
        "mode_env": "DOUBAN_ADAPTER_MODE",
        "credentials": (
            "DOUBAN_CLIENT_ID",
            "DOUBAN_CLIENT_SECRET",
            "DOUBAN_ACCESS_TOKEN",
        ),
    },
    "toutiao": {
        "class": ToutiaoAdapter,
        "mode_env": "TOUTIAO_ADAPTER_MODE",
        "credentials": (
            "TOUTIAO_CLIENT_ID",
            "TOUTIAO_CLIENT_SECRET",
            "TOUTIAO_ACCESS_TOKEN",
        ),
    },
}

OFFICIAL_PLATFORM_IDS = tuple(OFFICIAL_PLATFORM_CONFIG)
PUBLIC_PARSER_IDS = ("the_paper", "jiemian", "hupu", "tieba", "nga", "maimai")
REQUIRED_OFFICIAL_CRAWL_METADATA_FIELDS = {
    "platform",
    "adapter_mode",
    "source_type",
    "fallback_used",
    "fallback_reason_category",
    "post_count",
    "comment_count",
    "raw_post_schema_valid",
    "raw_comment_schema_valid",
    "real_mode_available",
    "credential_present",
}


def test_adapter_factory_registers_all_active_adapter_groups() -> None:
    expected_ids = sorted(("reddit", *OFFICIAL_PLATFORM_IDS, "youtube", *PUBLIC_PARSER_IDS))

    assert get_supported_adapter_ids() == expected_ids

    reddit = get_adapter("reddit")
    assert isinstance(reddit, RedditAdapter)
    for platform_id, config in OFFICIAL_PLATFORM_CONFIG.items():
        adapter = get_adapter(platform_id)
        assert isinstance(adapter, config["class"])
        assert has_platform_adapter(platform_id) is True
    for platform_id in PUBLIC_PARSER_IDS:
        adapter = get_adapter(platform_id)
        assert isinstance(adapter, PublicParserPlatformAdapter)
        assert has_platform_adapter(platform_id) is True
    youtube = get_adapter("youtube")
    assert isinstance(youtube, YouTubeAdapter)
    assert has_platform_adapter("youtube") is True

    assert has_platform_adapter("unknown_platform") is False
    with pytest.raises(PlatformAdapterError):
        get_adapter("unknown_platform")


@pytest.mark.parametrize("platform_id", OFFICIAL_PLATFORM_IDS)
def test_official_api_scaffold_contract_and_mock_schema(
    monkeypatch: pytest.MonkeyPatch,
    platform_id: str,
) -> None:
    _set_official_env(monkeypatch, platform_id, mode="mock", credentials_present=False)

    adapter = get_adapter(platform_id)
    posts = adapter.search_posts("Tesla", limit=3, sort="new", date_range={"start": "2026-05-01"})
    comments = adapter.fetch_comments(posts[0].post_id, limit=3)
    health = adapter.health_check()
    metadata = adapter.get_status_metadata()

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

    assert adapter.get_mode() == "mock"
    assert adapter.supports_real_mode() is False
    assert adapter.get_required_credentials() == OFFICIAL_PLATFORM_CONFIG[platform_id]["credentials"]
    assert health.ok is True
    assert health.mode == "mock"
    assert health.real_mode_available is False
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["selectable_for_real"] is False

    assert posts
    assert comments
    for post in posts:
        assert post.platform == platform_id
        RawPost.model_validate(post.model_dump(mode="json"))
        assert all(isinstance(key, str) for key in post.raw_data)
    for comment in comments:
        assert comment.platform == platform_id
        RawComment.model_validate(comment.model_dump(mode="json"))
        assert all(isinstance(key, str) for key in comment.raw_data)


@pytest.mark.parametrize(
    ("credentials_present", "expected_category", "expected_blocked_reason"),
    [
        (False, "config_error", "credentials_missing"),
        (True, "api_pending", "api_pending"),
    ],
)
@pytest.mark.parametrize("platform_id", OFFICIAL_PLATFORM_IDS)
def test_official_api_real_mode_is_blocked_without_network(
    monkeypatch: pytest.MonkeyPatch,
    platform_id: str,
    credentials_present: bool,
    expected_category: str,
    expected_blocked_reason: str,
) -> None:
    _set_official_env(
        monkeypatch,
        platform_id,
        mode="real",
        credentials_present=credentials_present,
    )
    _fail_if_urlopen_is_called(monkeypatch)

    adapter = get_adapter(platform_id)
    posts = adapter.search_posts("Tesla", limit=1)
    comments = adapter.fetch_comments(posts[0].post_id, limit=1)
    metadata = adapter.get_status_metadata()
    expected_blocked_reason_for_platform = OFFICIAL_PLATFORM_CONFIG[platform_id].get(
        "real_mode_blocked_reason_when_credentials",
        expected_blocked_reason,
    )
    if not credentials_present:
        expected_blocked_reason_for_platform = expected_blocked_reason

    assert adapter.get_mode() == "mock"
    assert adapter.supports_real_mode() is False
    assert adapter.has_required_credentials() is credentials_present
    assert metadata["requested_mode"] == "real"
    assert metadata["active_mode"] == "mock"
    assert metadata["real_mode_reached"] is False
    assert metadata["real_mode_available"] is False
    assert metadata["sanitized_error_category"] == expected_category
    assert metadata["real_mode_blocked_reason"] == expected_blocked_reason_for_platform
    assert posts[0].raw_data["mode"] == "mock"
    assert comments[0].raw_data["mode"] == "mock"


@pytest.mark.parametrize("platform_id", OFFICIAL_PLATFORM_IDS)
def test_crawl_start_official_scaffolds_have_consistent_metadata(
    monkeypatch: pytest.MonkeyPatch,
    platform_id: str,
) -> None:
    _set_official_env(monkeypatch, platform_id, mode="mock", credentials_present=False)
    _fail_if_urlopen_is_called(monkeypatch)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": [platform_id], "limit": 100},
    )

    assert response.status_code == 200
    body = response.json()
    metadata = body["platform_metadata"][0]

    assert REQUIRED_OFFICIAL_CRAWL_METADATA_FIELDS <= set(metadata)
    assert metadata["platform"] == platform_id
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["post_count"] <= 3
    assert metadata["comment_count"] <= 3
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_reached"] is False
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert body["raw_posts"]
    assert body["raw_comments"]
    for post in body["raw_posts"]:
        assert post["platform"] == platform_id
        RawPost.model_validate(post)
    for comment in body["raw_comments"]:
        assert comment["platform"] == platform_id
        RawComment.model_validate(comment)


@pytest.mark.parametrize("platform_id", OFFICIAL_PLATFORM_IDS)
def test_crawl_start_official_real_mode_stays_mock_api_pending(
    monkeypatch: pytest.MonkeyPatch,
    platform_id: str,
) -> None:
    _set_official_env(monkeypatch, platform_id, mode="real", credentials_present=True)
    _fail_if_urlopen_is_called(monkeypatch)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": [platform_id], "limit": 100},
    )

    assert response.status_code == 200
    body = response.json()
    metadata = body["platform_metadata"][0]

    assert metadata["platform"] == platform_id
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "api_pending"
    assert metadata["fetch_status"] == "api_pending"
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_reached"] is False
    expected_blocked_reason = OFFICIAL_PLATFORM_CONFIG[platform_id].get(
        "real_mode_blocked_reason_when_credentials",
        "api_pending",
    )
    assert metadata["real_mode_blocked_reason"] == expected_blocked_reason
    assert metadata["sanitized_error_category"] == "api_pending"
    assert body["raw_posts"][0]["raw_data"]["mode"] == "mock"


def test_platform_status_is_complete_and_does_not_expose_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    secret_markers = []
    monkeypatch.setenv("REDDIT_CLIENT_ID", "reddit-client-secret-marker")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "reddit-secret-marker")
    monkeypatch.setenv("REDDIT_USER_AGENT", "reddit-agent-secret-marker")
    secret_markers.extend(
        ["reddit-client-secret-marker", "reddit-secret-marker", "reddit-agent-secret-marker"]
    )
    for platform_id in OFFICIAL_PLATFORM_IDS:
        for credential_name in OFFICIAL_PLATFORM_CONFIG[platform_id]["credentials"]:
            marker = f"{credential_name.lower()}-secret-marker"
            monkeypatch.setenv(credential_name, marker)
            secret_markers.append(marker)
    monkeypatch.setenv("YOUTUBE_API_KEY", "youtube-key-secret-marker")
    monkeypatch.setenv("YOUTUBE_ADAPTER_MODE", "real")
    secret_markers.append("youtube-key-secret-marker")

    response = client.get("/api/v1/platforms/status")

    assert response.status_code == 200
    body = response.json()
    by_id = {platform["platform_id"]: platform for platform in body["platforms"]}
    expected_platforms = {
        "reddit",
        *OFFICIAL_PLATFORM_IDS,
        *PUBLIC_PARSER_IDS,
        "tianya",
        "youtube",
    }

    assert expected_platforms <= set(by_id)
    assert by_id["reddit"]["status"] == "api_pending"
    assert by_id["reddit"]["mock_available"] is True
    assert by_id["reddit"]["real_mode_available"] is False
    assert by_id["reddit"]["selectable_for_real"] is False
    assert by_id["youtube"]["status"] == "real_api_available_when_configured"
    assert by_id["youtube"]["integration_type"] == "official_api"
    assert by_id["youtube"]["source_type"] == "youtube_data_api_v3"
    assert by_id["youtube"]["mock_available"] is True
    assert by_id["youtube"]["real_mode_available"] is True
    assert by_id["youtube"]["api_approval_required"] is False
    assert by_id["youtube"]["api_pending"] is False
    assert by_id["youtube"]["real_mode_disabled"] is False
    assert by_id["youtube"]["credentials_required"] == ["YOUTUBE_API_KEY"]
    assert by_id["youtube"]["required_credentials"] == ["YOUTUBE_API_KEY"]
    assert by_id["youtube"]["credentials_present"] == {"YOUTUBE_API_KEY": True}
    assert by_id["youtube"]["credential_present"] is True
    assert by_id["youtube"]["required_scopes"] == []
    assert by_id["youtube"]["scope_status"] == "not_required"
    assert by_id["youtube"]["oauth_required"] is False
    assert by_id["youtube"]["real_mode_configured"] is True
    assert by_id["youtube"]["real_mode_blocker"] is None
    assert by_id["youtube"]["data_access_level"] == "public_video_comment_data"
    assert by_id["youtube"]["quota_cache_protected"] is True
    assert by_id["youtube"]["selectable_for_mock"] is True
    assert by_id["youtube"]["selectable_for_real"] is True
    for platform_id in OFFICIAL_PLATFORM_IDS:
        item = by_id[platform_id]
        assert item["category"] == "official_api_planned"
        assert item["source_type"] == "official_api_adapter_scaffold"
        assert item["status"] == "official_api_planned"
        assert item["integration_type"] in {"official_api_scaffold", "official_api_oauth"}
        assert item["mock_available"] is True
        assert item["real_mode_available"] is False
        assert item["api_approval_required"] is True
        if expected_status := OFFICIAL_PLATFORM_CONFIG[platform_id].get("api_approval_status"):
            assert item["api_approval_status"] == expected_status
        if expected_developer_status := OFFICIAL_PLATFORM_CONFIG[platform_id].get("developer_access_status"):
            assert item["developer_access_status"] == expected_developer_status
        if expected_app_type := OFFICIAL_PLATFORM_CONFIG[platform_id].get("app_type"):
            assert item["app_type"] == expected_app_type
        if expected_comment_status := OFFICIAL_PLATFORM_CONFIG[platform_id].get("comment_api_status"):
            assert item["comment_api_status"] == expected_comment_status
        if expected_scope := OFFICIAL_PLATFORM_CONFIG[platform_id].get("recommended_comment_scope"):
            assert item["recommended_comment_scope"] == expected_scope
        if expected_video_scope := OFFICIAL_PLATFORM_CONFIG[platform_id].get("video_comment_scope_status"):
            assert item["video_comment_scope_status"] == expected_video_scope
        if expected_blocker := OFFICIAL_PLATFORM_CONFIG[platform_id].get("real_mode_blocker"):
            assert item["real_mode_blocker"] == expected_blocker
        assert "required_credentials" in item
        assert item["credential_present"] is True
        assert isinstance(item["required_scopes"], list)
        assert isinstance(item["scope_status"], str)
        assert isinstance(item["oauth_required"], bool)
        assert isinstance(item["oauth_status"], str)
        assert isinstance(item["next_user_action"], str)
        assert item["credentials_required"] == list(OFFICIAL_PLATFORM_CONFIG[platform_id]["credentials"])
        assert all(item["credentials_present"].values())
        assert item["selectable_for_mock"] is True
        assert item["selectable_for_real"] is False
    for platform_id in PUBLIC_PARSER_IDS:
        item = by_id[platform_id]
        assert item["source_type"] == "public_page_parser"
        assert item["status"] == "fixture_only"
        assert item["mock_available"] is True
        assert item["selectable_for_real"] is False

    response_text = response.text
    for marker in secret_markers:
        assert marker not in response_text


def test_public_parser_status_and_preview_matrix_remains_fixture_first(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "false")

    status_response = client.get("/api/v1/public-parsers/status")

    assert status_response.status_code == 200
    status_body = status_response.json()
    status_by_id = {parser["platform_id"]: parser for parser in status_body["parsers"]}
    assert tuple(get_public_parser_platform_ids()) == tuple(sorted(PUBLIC_PARSER_IDS))
    assert set(status_by_id) == set(PUBLIC_PARSER_IDS)
    assert status_body["live_fetch_enabled_default"] is False

    for platform_id in PUBLIC_PARSER_IDS:
        status_item = status_by_id[platform_id]
        assert status_item["source_type"] == "public_page_parser"
        assert status_item["parser_status"] == "fixture_only"
        assert status_item["live_fetch_enabled"] is False
        assert status_item["fixture_available"] is True
        assert status_item["profile_available"] is True
        assert status_item["safe_limit"] == 3
        assert status_item["rate_limit_seconds"] == 3.0

        preview_response = client.post(
            "/api/v1/public-parsers/preview",
            json={"platform": platform_id, "limit": 3, "use_live_fetch": False},
        )
        assert preview_response.status_code == 200
        preview = preview_response.json()
        assert preview["platform"] == platform_id
        assert preview["source_type"] == "public_page_parser"
        assert preview["live_fetch_enabled"] is False
        assert preview["live_fetch_attempted"] is False
        assert preview["fallback_used"] is True
        assert preview["fallback_reason_category"] == "fixture_preview"
        assert preview["raw_post_schema_valid"] is True
        assert preview["raw_comment_schema_valid"] is True
        assert preview["sample_posts"]
        RawPost.model_validate(preview["sample_posts"][0])
        for comment in preview["sample_comments"]:
            RawComment.model_validate(comment)


def _set_official_env(
    monkeypatch: pytest.MonkeyPatch,
    platform_id: str,
    *,
    mode: str,
    credentials_present: bool,
) -> None:
    config = OFFICIAL_PLATFORM_CONFIG[platform_id]
    monkeypatch.setenv(config["mode_env"], mode)
    for credential_name in config["credentials"]:
        monkeypatch.setenv(
            credential_name,
            f"{platform_id}-placeholder" if credentials_present else "",
        )


def _fail_if_urlopen_is_called(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_urlopen(*args: object, **kwargs: object) -> object:
        del args, kwargs
        raise AssertionError("Network fetch should not be called by mock-only adapter QA.")

    monkeypatch.setattr(urllib.request, "urlopen", fail_urlopen)
