from __future__ import annotations

from pathlib import Path

from app.schemas.comment import RawComment, RawPost
from app.services.crawling.public_parser.base_public_parser import BasePublicParser
from app.services.crawling.public_parser.html_cleaner import extract_all_text, extract_first_text
from app.services.crawling.public_parser.public_fetcher import PublicFetcher
from app.services.crawling.public_parser.selector_profile import (
    SelectorProfile,
    load_selector_profile,
)


FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "public_parser" / "the_paper_article.html"


def _fixture_html() -> str:
    return FIXTURE_PATH.read_text(encoding="utf-8")


def test_selector_profile_loads_the_paper_profile() -> None:
    profile = load_selector_profile("the_paper")

    assert profile.platform_id == "the_paper"
    assert profile.status == "fixture_only"
    assert profile.search_url_template is None
    assert profile.rate_limit_seconds == 3


def test_html_cleaner_extracts_fixture_title_content_and_comments() -> None:
    html = _fixture_html()

    assert extract_first_text(html, "h1.article-title") == "新能源汽车质量讨论升温"
    assert "售后响应" in extract_first_text(html, ".article-content")
    comments = extract_all_text(html, ".public-comment")
    assert len(comments) == 2
    assert comments[0].startswith("公开评论")


def test_public_parser_extracts_raw_post_from_fixture() -> None:
    profile = load_selector_profile("the_paper")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.parse_html(_fixture_html(), source_url=profile.fixture_url, keyword="Tesla")

    assert result.metadata["schema_valid"] is True
    assert result.metadata["parser_status"] == "fixture_only"
    assert len(result.posts) == 1
    assert result.comments == []
    post = result.posts[0]
    assert isinstance(post, RawPost)
    assert post.platform == "the_paper"
    assert post.title == "新能源汽车质量讨论升温"
    assert "public_parser_fixture" in post.raw_data["mode"]


def test_public_parser_can_extract_comments_when_profile_allows_public_comments() -> None:
    profile = SelectorProfile(
        platform_id="test_public",
        display_name="Test Public",
        base_url="https://example.com",
        allowed_public_paths=["/"],
        article_selector="article",
        title_selector="h1.article-title",
        content_selector=".article-content",
        author_selector=".article-author",
        created_at_selector=".article-date",
        comment_selector=".public-comment",
        status="fixture_only",
    )
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.parse_html(_fixture_html(), source_url="https://example.com/public", keyword="Tesla")

    assert len(result.comments) == 2
    assert all(isinstance(comment, RawComment) for comment in result.comments)
    assert result.comments[0].platform == "test_public"
    assert result.comments[0].content.startswith("公开评论")


def test_public_parser_missing_selector_fails_safely() -> None:
    profile = SelectorProfile(
        platform_id="broken_public",
        display_name="Broken Public",
        base_url="https://example.com",
        allowed_public_paths=["/"],
        article_selector="article",
        title_selector=".missing-title",
        content_selector=".missing-content",
        status="fixture_only",
    )
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.parse_html(_fixture_html(), source_url="https://example.com/public", keyword="Tesla")

    assert result.posts == []
    assert result.comments == []
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "selector_missing"


def test_public_fetcher_default_request_uses_no_cookie_or_auth_headers() -> None:
    fetcher = PublicFetcher(
        live_fetch_enabled=False,
        rate_limit_seconds=0,
        user_agent="sentigraph-public-parser-dev-test",
    )

    request = fetcher.build_request("https://example.com/public")
    headers = {key.lower(): value for key, value in request.header_items()}

    assert "user-agent" in headers
    assert "cookie" not in headers
    assert "authorization" not in headers


def test_public_parser_search_falls_back_to_fixture_mock_when_live_disabled() -> None:
    profile = load_selector_profile("the_paper")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.search_public_pages("Tesla", limit=10)

    assert result.metadata["live_fetch_enabled"] is False
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert 1 <= len(result.posts) <= 5
    assert result.posts[0].platform == "the_paper"
    assert result.posts[0].raw_data["mode"] == "fixture"

