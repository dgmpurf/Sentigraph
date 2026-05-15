from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.comment import RawComment, RawPost
from app.services.crawling.public_parser.parser_status_service import preview_public_parser


client = TestClient(app)


PUBLIC_PARSER_IDS = {"the_paper", "jiemian", "hupu", "tieba", "nga"}


def test_public_parser_status_endpoint_returns_all_fixture_sources(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "false")

    response = client.get("/api/v1/public-parsers/status")

    assert response.status_code == 200
    body = response.json()
    parsers = {item["platform_id"]: item for item in body["parsers"]}

    assert body["total"] == 5
    assert set(parsers) == PUBLIC_PARSER_IDS
    assert body["live_fetch_enabled_default"] is False
    for platform_id, item in parsers.items():
        assert item["platform_id"] == platform_id
        assert item["source_type"] == "public_page_parser"
        assert item["parser_status"] == "fixture_only"
        assert item["live_fetch_enabled"] is False
        assert item["fixture_available"] is True
        assert item["profile_available"] is True
        assert item["last_test_status"] == "fixture_available"
        assert item["safe_limit"] == 3
        assert item["rate_limit_seconds"] == 3.0
        assert item["notes"]

    assert parsers["hupu"]["comments_supported"] is True
    assert parsers["tieba"]["comments_supported"] is True
    assert parsers["nga"]["comments_supported"] is True
    assert parsers["the_paper"]["comments_supported"] is False
    assert parsers["jiemian"]["comments_supported"] is False


@pytest.mark.parametrize(
    ("platform_id", "expected_comments"),
    [
        ("the_paper", 0),
        ("jiemian", 0),
        ("hupu", 2),
        ("tieba", 3),
        ("nga", 3),
    ],
)
def test_public_parser_preview_endpoint_returns_fixture_sample(
    monkeypatch,
    platform_id: str,
    expected_comments: int,
) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "false")

    response = client.post(
        "/api/v1/public-parsers/preview",
        json={"platform": platform_id, "limit": 3, "use_live_fetch": False},
    )

    assert response.status_code == 200
    body = response.json()

    assert body["platform"] == platform_id
    assert body["source_type"] == "public_page_parser"
    assert body["parser_status"] == "fixture_only"
    assert body["live_fetch_enabled"] is False
    assert body["live_fetch_attempted"] is False
    assert body["fallback_used"] is True
    assert body["fallback_reason_category"] == "fixture_preview"
    assert body["post_count"] == 1
    assert body["comment_count"] == expected_comments
    assert body["raw_post_schema_valid"] is True
    assert body["raw_comment_schema_valid"] is True
    assert body["sample_posts"]
    assert body["sample_posts"][0]["platform"] == platform_id
    RawPost.model_validate(body["sample_posts"][0])

    for comment in body["sample_comments"]:
        assert comment["platform"] == platform_id
        RawComment.model_validate(comment)


def test_public_parser_preview_unknown_platform_fails_safely() -> None:
    response = client.post(
        "/api/v1/public-parsers/preview",
        json={"platform": "unknown_source", "limit": 3, "use_live_fetch": False},
    )

    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]


def test_public_parser_preview_live_requested_while_disabled_uses_fixture(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "false")

    response = client.post(
        "/api/v1/public-parsers/preview",
        json={"platform": "the_paper", "limit": 3, "use_live_fetch": True},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["platform"] == "the_paper"
    assert body["live_fetch_enabled"] is False
    assert body["live_fetch_attempted"] is False
    assert body["fallback_used"] is True
    assert body["fallback_reason_category"] == "fixture_preview"
    assert "live_fetch_disabled" in body["warnings"]
    assert body["sample_posts"]
    assert body["raw_post_schema_valid"] is True


def test_public_parser_status_live_flag_only_marks_live_capable_profile(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "true")

    response = client.get("/api/v1/public-parsers/status")

    assert response.status_code == 200
    body = response.json()
    parsers = {item["platform_id"]: item for item in body["parsers"]}

    assert body["live_fetch_enabled_default"] is True
    assert parsers["the_paper"]["live_fetch_enabled"] is True
    assert parsers["jiemian"]["live_fetch_enabled"] is False
    assert parsers["hupu"]["live_fetch_enabled"] is False
    assert parsers["tieba"]["live_fetch_enabled"] is False
    assert parsers["nga"]["live_fetch_enabled"] is False


def test_public_parser_preview_does_not_use_live_fetch_without_request_opt_in(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "true")

    response = client.post(
        "/api/v1/public-parsers/preview",
        json={"platform": "the_paper", "limit": 3, "use_live_fetch": False},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["platform"] == "the_paper"
    assert body["live_fetch_enabled"] is False
    assert body["live_fetch_attempted"] is False
    assert body["fallback_used"] is True
    assert body["fallback_reason_category"] == "fixture_preview"
    assert body["sample_posts"]


def test_public_parser_preview_live_requested_for_fixture_only_platform_stays_fixture(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "true")

    response = client.post(
        "/api/v1/public-parsers/preview",
        json={"platform": "hupu", "limit": 3, "use_live_fetch": True},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["platform"] == "hupu"
    assert body["live_fetch_enabled"] is False
    assert body["live_fetch_attempted"] is False
    assert body["fallback_used"] is True
    assert body["fallback_reason_category"] == "fixture_preview"
    assert "live_fetch_disabled" in body["warnings"]
    assert body["post_count"] == 1
    assert body["comment_count"] == 2


def test_public_parser_preview_service_validates_raw_schemas(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "false")

    preview = preview_public_parser("hupu", limit=3, use_live_fetch=False)

    assert preview.raw_post_schema_valid is True
    assert preview.raw_comment_schema_valid is True
    assert preview.sample_posts[0].platform == "hupu"
    assert preview.sample_comments[0].platform == "hupu"
