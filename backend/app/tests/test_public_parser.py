from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from app.schemas.comment import RawComment, RawPost
from app.services.crawling.public_parser.base_public_parser import BasePublicParser
from app.services.crawling.public_parser.html_cleaner import extract_all_text, extract_first_text
from app.services.crawling.public_parser.public_fetcher import PublicFetcher, PublicFetchResult
from app.services.crawling.public_parser.selector_profile import (
    SelectorProfile,
    load_selector_profile,
)


FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "public_parser"
FIXTURE_PATH = FIXTURE_DIR / "the_paper_article.html"
JIEMIAN_FIXTURE_PATH = FIXTURE_DIR / "jiemian_article.html"
HUPU_FIXTURE_PATH = FIXTURE_DIR / "hupu_thread.html"
MAIMAI_FIXTURE_PATH = FIXTURE_DIR / "maimai_post.html"
TIEBA_FIXTURE_PATH = FIXTURE_DIR / "tieba_thread.html"
NGA_FIXTURE_PATH = FIXTURE_DIR / "nga_thread.html"
PARSER_BENCHMARK_CASES_PATH = Path(__file__).resolve().parents[3] / "benchmarks" / "parser_fixture_cases.json"


def _fixture_html() -> str:
    return FIXTURE_PATH.read_text(encoding="utf-8")


def _jiemian_fixture_html() -> str:
    return JIEMIAN_FIXTURE_PATH.read_text(encoding="utf-8")


def _hupu_fixture_html() -> str:
    return HUPU_FIXTURE_PATH.read_text(encoding="utf-8")


def _maimai_fixture_html() -> str:
    return MAIMAI_FIXTURE_PATH.read_text(encoding="utf-8")


def _tieba_fixture_html() -> str:
    return TIEBA_FIXTURE_PATH.read_text(encoding="utf-8")


def _nga_fixture_html() -> str:
    return NGA_FIXTURE_PATH.read_text(encoding="utf-8")


def _parser_benchmark_case(case_id: str) -> dict:
    cases = json.loads(PARSER_BENCHMARK_CASES_PATH.read_text(encoding="utf-8"))
    return next(case for case in cases if case["case_id"] == case_id)


def _parse_inline_benchmark_case(case_id: str):
    case = _parser_benchmark_case(case_id)
    profile = load_selector_profile(case["platform_id"])
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )
    return parser.parse_html(
        case["fixture_html"],
        source_url=profile.fixture_url or profile.base_url,
        keyword="benchmark",
        limit=case.get("limit", 3),
        metadata_extra={"fetch_status": "inline_fixture"},
    )


class FakeLiveFetcher:
    live_fetch_enabled = True

    def __init__(self, fetch_result: PublicFetchResult) -> None:
        self.fetch_result = fetch_result
        self.requested_urls: list[str] = []

    def fetch(self, url: str, profile) -> PublicFetchResult:
        del profile
        self.requested_urls.append(url)
        return self.fetch_result


def test_selector_profile_loads_the_paper_profile() -> None:
    profile = load_selector_profile("the_paper")

    assert profile.platform_id == "the_paper"
    assert profile.status == "fixture_only"
    assert profile.search_url_template == "https://www.thepaper.cn/newsDetail_forward_{keyword}"
    assert profile.rate_limit_seconds == 3


def test_selector_profile_loads_jiemian_profile() -> None:
    profile = load_selector_profile("jiemian")

    assert profile.platform_id == "jiemian"
    assert profile.display_name == "Jiemian News / 界面新闻"
    assert profile.status == "fixture_only"
    assert profile.search_url_template is None
    assert profile.comment_selector is None
    assert "comments_unavailable_without_login_or_dynamic_loading" in profile.notes
    assert "comments are not parsed" in profile.notes


def test_selector_profile_loads_hupu_profile() -> None:
    profile = load_selector_profile("hupu")

    assert profile.platform_id == "hupu"
    assert profile.display_name.startswith("Hupu /")
    assert profile.status == "fixture_only"
    assert profile.search_url_template is None
    assert profile.comment_selector == ".reply-item"
    assert profile.comment_content_selector == ".reply-content"
    assert "forum-style Hupu threads" in profile.notes


def test_selector_profile_loads_maimai_profile() -> None:
    profile = load_selector_profile("maimai")

    assert profile.platform_id == "maimai"
    assert profile.display_name == "Maimai / 脉脉"
    assert profile.status == "fixture_only"
    assert profile.search_url_template is None
    assert profile.comment_selector == ".comment-item"
    assert profile.comment_content_selector == ".comment-content"
    assert "workplace and industry discussion" in profile.notes


def test_selector_profile_loads_tieba_profile() -> None:
    profile = load_selector_profile("tieba")

    assert profile.platform_id == "tieba"
    assert profile.display_name.startswith("Baidu Tieba")
    assert profile.status == "fixture_only"
    assert profile.search_url_template is None
    assert profile.comment_selector == ".reply-item"
    assert profile.comment_content_selector == ".reply-content"
    assert profile.comment_floor_selector == ".reply-floor"
    assert "forum-style threads" in profile.notes


def test_selector_profile_loads_nga_profile() -> None:
    profile = load_selector_profile("nga")

    assert profile.platform_id == "nga"
    assert profile.display_name == "NGA"
    assert profile.status == "fixture_only"
    assert profile.search_url_template is None
    assert profile.comment_selector == ".reply-item"
    assert profile.comment_content_selector == ".reply-content"
    assert profile.comment_floor_selector == ".reply-floor"
    assert "forum-style threads" in profile.notes


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
    assert post.content
    assert post.author_name != "public_source"
    assert post.created_at == "2026-05-15T08:00:00Z"
    assert post.url == profile.fixture_url
    assert post.title == "新能源汽车质量讨论升温"
    assert "public_parser_fixture" in post.raw_data["mode"]


def test_jiemian_public_parser_extracts_raw_post_from_fixture() -> None:
    profile = load_selector_profile("jiemian")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.parse_html(_jiemian_fixture_html(), source_url=profile.fixture_url, keyword="Tesla")

    assert result.metadata["schema_valid"] is True
    assert result.metadata["parser_status"] == "fixture_only"
    assert len(result.posts) == 1
    assert result.comments == []
    post = result.posts[0]
    assert isinstance(post, RawPost)
    assert post.platform == "jiemian"
    assert post.title == "新能源车售后服务体验引发公开讨论"
    assert "售后响应" in post.content
    assert post.author_name == "界面新闻 · 消费报道"
    assert post.created_at == "2026-05-15T09:30:00Z"
    assert post.url == profile.fixture_url
    assert post.raw_data["mode"] == "public_parser_fixture"


def test_hupu_public_parser_extracts_thread_and_visible_replies_from_fixture() -> None:
    profile = load_selector_profile("hupu")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.parse_html(_hupu_fixture_html(), source_url=profile.fixture_url, keyword="Tesla")

    assert result.metadata["schema_valid"] is True
    assert result.metadata["parser_status"] == "fixture_only"
    assert len(result.posts) == 1
    assert len(result.comments) == 2
    post = result.posts[0]
    assert isinstance(post, RawPost)
    assert post.platform == "hupu"
    assert post.title == "Tesla service discussion on Hupu"
    assert "repair dispute" in post.content
    assert post.author_name == "hupu_fixture_author"
    assert post.created_at == "2026-05-15T11:00:00Z"
    assert post.like_count == 128
    assert post.reply_count == 2
    assert post.url == profile.fixture_url

    first_comment = result.comments[0]
    second_comment = result.comments[1]
    assert isinstance(first_comment, RawComment)
    assert first_comment.platform == "hupu"
    assert first_comment.post_id == post.post_id
    assert first_comment.comment_id == "hupu_reply_001"
    assert first_comment.parent_id is None
    assert first_comment.author_name == "reply_user_alpha"
    assert "repair timeline" in first_comment.content
    assert first_comment.created_at == "2026-05-15T11:08:00Z"
    assert first_comment.like_count == 24
    assert second_comment.comment_id == "hupu_reply_002"
    assert second_comment.parent_id == "hupu_reply_001"
    assert second_comment.like_count == 11


def test_maimai_public_parser_extracts_post_and_visible_replies_from_fixture() -> None:
    profile = load_selector_profile("maimai")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.parse_html(_maimai_fixture_html(), source_url=profile.fixture_url, keyword="Tesla")

    assert result.metadata["schema_valid"] is True
    assert result.metadata["parser_status"] == "fixture_only"
    assert len(result.posts) == 1
    assert len(result.comments) == 2
    post = result.posts[0]
    assert isinstance(post, RawPost)
    assert post.platform == "maimai"
    assert post.title == "Tesla workplace discussion on Maimai"
    assert "workplace and industry discussion" in post.content
    assert post.author_name == "maimai_public_source"
    assert post.created_at == "2026-05-15T14:00:00Z"
    assert post.like_count == 93
    assert post.reply_count == 2
    assert post.url == profile.fixture_url

    first_comment = result.comments[0]
    second_comment = result.comments[1]
    assert isinstance(first_comment, RawComment)
    assert first_comment.platform == "maimai"
    assert first_comment.post_id == post.post_id
    assert first_comment.comment_id == "maimai_reply_001"
    assert first_comment.parent_id is None
    assert first_comment.author_name == "maimai_user_alpha"
    assert "service workflow" in first_comment.content
    assert first_comment.created_at == "2026-05-15T14:09:00Z"
    assert first_comment.like_count == 16
    assert second_comment.comment_id == "maimai_reply_002"
    assert second_comment.parent_id == "maimai_reply_001"
    assert second_comment.like_count == 9


def test_tieba_public_parser_extracts_thread_and_visible_replies_from_fixture() -> None:
    profile = load_selector_profile("tieba")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.parse_html(_tieba_fixture_html(), source_url=profile.fixture_url, keyword="Tesla")

    assert result.metadata["schema_valid"] is True
    assert result.metadata["parser_status"] == "fixture_only"
    assert len(result.posts) == 1
    assert len(result.comments) == 3
    post = result.posts[0]
    assert isinstance(post, RawPost)
    assert post.platform == "tieba"
    assert post.title == "Tesla service discussion on Baidu Tieba"
    assert "customer service dispute" in post.content
    assert post.author_name == "tieba_fixture_author"
    assert post.created_at == "2026-05-15T12:00:00Z"
    assert post.like_count == 76
    assert post.reply_count == 3
    assert post.url == profile.fixture_url

    first_comment = result.comments[0]
    second_comment = result.comments[1]
    third_comment = result.comments[2]
    assert isinstance(first_comment, RawComment)
    assert first_comment.platform == "tieba"
    assert first_comment.post_id == post.post_id
    assert first_comment.comment_id == "tieba_reply_001"
    assert first_comment.parent_id is None
    assert first_comment.author_name == "tieba_user_alpha"
    assert "factual timeline" in first_comment.content
    assert first_comment.created_at == "2026-05-15T12:08:00Z"
    assert first_comment.like_count == 18
    assert first_comment.raw_data["floor_number"] == "1F"
    assert second_comment.comment_id == "tieba_reply_002"
    assert second_comment.parent_id == "tieba_reply_001"
    assert second_comment.raw_data["floor_number"] == "2F"
    assert third_comment.comment_id == "tieba_reply_003"
    assert third_comment.raw_data["floor_number"] == "3F"


def test_nga_public_parser_extracts_thread_and_visible_replies_from_fixture() -> None:
    profile = load_selector_profile("nga")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.parse_html(_nga_fixture_html(), source_url=profile.fixture_url, keyword="Tesla")

    assert result.metadata["schema_valid"] is True
    assert result.metadata["parser_status"] == "fixture_only"
    assert len(result.posts) == 1
    assert len(result.comments) == 3
    post = result.posts[0]
    assert isinstance(post, RawPost)
    assert post.platform == "nga"
    assert post.title == "Tesla service discussion on NGA"
    assert "customer service dispute" in post.content
    assert post.author_name == "nga_fixture_author"
    assert post.created_at == "2026-05-15T13:00:00Z"
    assert post.like_count == 64
    assert post.reply_count == 3
    assert post.url == profile.fixture_url

    first_comment = result.comments[0]
    second_comment = result.comments[1]
    third_comment = result.comments[2]
    assert isinstance(first_comment, RawComment)
    assert first_comment.platform == "nga"
    assert first_comment.post_id == post.post_id
    assert first_comment.comment_id == "nga_reply_001"
    assert first_comment.parent_id is None
    assert first_comment.author_name == "nga_user_alpha"
    assert "timeline should be listed" in first_comment.content
    assert first_comment.created_at == "2026-05-15T13:08:00Z"
    assert first_comment.like_count == 22
    assert first_comment.raw_data["floor_number"] == "1F"
    assert second_comment.comment_id == "nga_reply_002"
    assert second_comment.parent_id == "nga_reply_001"
    assert second_comment.raw_data["floor_number"] == "2F"
    assert third_comment.comment_id == "nga_reply_003"
    assert third_comment.raw_data["floor_number"] == "3F"


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


def test_jiemian_missing_selectors_fail_safely() -> None:
    profile = SelectorProfile(
        platform_id="jiemian_broken",
        display_name="Jiemian Broken",
        base_url="https://www.jiemian.com",
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

    result = parser.parse_html(_jiemian_fixture_html(), source_url="https://www.jiemian.com/article/broken", keyword="Tesla")

    assert result.posts == []
    assert result.comments == []
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "selector_missing"


def test_hupu_missing_selectors_fail_safely() -> None:
    profile = SelectorProfile(
        platform_id="hupu_broken",
        display_name="Hupu Broken",
        base_url="https://bbs.hupu.com",
        allowed_public_paths=["/"],
        article_selector="article.thread",
        title_selector=".missing-title",
        content_selector=".missing-content",
        comment_selector=".reply-item",
        status="fixture_only",
    )
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.parse_html(_hupu_fixture_html(), source_url="https://bbs.hupu.com/thread-broken", keyword="Tesla")

    assert result.posts == []
    assert result.comments == []
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "selector_missing"


def test_maimai_missing_selectors_fail_safely() -> None:
    profile = SelectorProfile(
        platform_id="maimai_broken",
        display_name="Maimai Broken",
        base_url="https://maimai.cn",
        allowed_public_paths=["/"],
        article_selector="article.maimai-post",
        title_selector=".missing-title",
        content_selector=".missing-content",
        comment_selector=".comment-item",
        status="fixture_only",
    )
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.parse_html(_maimai_fixture_html(), source_url="https://maimai.cn/web/broken", keyword="Tesla")

    assert result.posts == []
    assert result.comments == []
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "selector_missing"


def test_tieba_missing_selectors_fail_safely() -> None:
    profile = SelectorProfile(
        platform_id="tieba_broken",
        display_name="Tieba Broken",
        base_url="https://tieba.baidu.com",
        allowed_public_paths=["/p/"],
        article_selector="article.thread",
        title_selector=".missing-title",
        content_selector=".missing-content",
        comment_selector=".reply-item",
        status="fixture_only",
    )
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.parse_html(_tieba_fixture_html(), source_url="https://tieba.baidu.com/p/broken", keyword="Tesla")

    assert result.posts == []
    assert result.comments == []
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "selector_missing"


def test_nga_missing_selectors_fail_safely() -> None:
    profile = SelectorProfile(
        platform_id="nga_broken",
        display_name="NGA Broken",
        base_url="https://bbs.nga.cn",
        allowed_public_paths=["/read.php"],
        article_selector="article.thread",
        title_selector=".missing-title",
        content_selector=".missing-content",
        comment_selector=".reply-item",
        status="fixture_only",
    )
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.parse_html(_nga_fixture_html(), source_url="https://bbs.nga.cn/read.php?tid=broken", keyword="Tesla")

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


def test_public_fetcher_checks_robots_before_page_fetch(monkeypatch) -> None:
    profile = load_selector_profile("the_paper")
    requested_urls: list[str] = []

    class FakeResponse:
        headers = {"Content-Type": "text/plain; charset=utf-8"}
        status = 200

        def __init__(self, text: str) -> None:
            self.text = text

        def __enter__(self) -> "FakeResponse":
            return self

        def __exit__(self, *args) -> None:
            return None

        def read(self, limit: int = -1) -> bytes:
            del limit
            return self.text.encode("utf-8")

    def fake_urlopen(request, timeout=0):  # noqa: ANN001
        del timeout
        url = request.full_url
        requested_urls.append(url)
        if url.endswith("/robots.txt"):
            return FakeResponse("User-agent: *\nDisallow: /\n")
        raise AssertionError("Page fetch should not run when robots disallows access")

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    fetcher = PublicFetcher(live_fetch_enabled=True, rate_limit_seconds=0)

    result = fetcher.fetch("https://www.thepaper.cn/newsDetail_forward_fixture", profile)

    assert requested_urls == ["https://www.thepaper.cn/robots.txt"]
    assert result.ok is False
    assert result.live_fetch_attempted is True
    assert result.live_fetch_allowed is False
    assert result.fallback_reason_category == "robots_disallowed"
    assert result.fetch_status == "robots_disallowed"


def test_public_fetcher_live_fetch_uses_safe_headers_after_robots_allow(monkeypatch) -> None:
    profile = load_selector_profile("the_paper")
    requested_headers: list[dict[str, str]] = []

    class FakeResponse:
        status = 200

        def __init__(self, text: str, content_type: str) -> None:
            self.text = text
            self.headers = {"Content-Type": content_type}

        def __enter__(self) -> "FakeResponse":
            return self

        def __exit__(self, *args) -> None:
            return None

        def read(self, limit: int = -1) -> bytes:
            del limit
            return self.text.encode("utf-8")

    def fake_urlopen(request, timeout=0):  # noqa: ANN001
        del timeout
        requested_headers.append({key.lower(): value for key, value in request.header_items()})
        if request.full_url.endswith("/robots.txt"):
            return FakeResponse("User-agent: *\nAllow: /\n", "text/plain; charset=utf-8")
        return FakeResponse(_fixture_html(), "text/html; charset=utf-8")

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    fetcher = PublicFetcher(
        live_fetch_enabled=True,
        rate_limit_seconds=0,
        user_agent="sentigraph-public-parser-dev-test",
    )

    result = fetcher.fetch("https://www.thepaper.cn/newsDetail_forward_fixture", profile)

    assert result.ok is True
    assert result.live_fetch_attempted is True
    assert result.live_fetch_allowed is True
    assert result.fetch_status == "ok"
    assert result.html and "article-title" in result.html
    assert len(requested_headers) == 2
    for headers in requested_headers:
        assert "user-agent" in headers
        assert "cookie" not in headers
        assert "authorization" not in headers


def test_public_fetcher_from_env_keeps_live_fetch_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", raising=False)
    monkeypatch.delenv("PUBLIC_PARSER_RATE_LIMIT_SECONDS", raising=False)
    monkeypatch.delenv("PUBLIC_PARSER_USER_AGENT", raising=False)

    fetcher = PublicFetcher.from_env()

    assert fetcher.live_fetch_enabled is False
    assert fetcher.rate_limit_seconds == 3.0
    assert fetcher.user_agent == "sentigraph-public-parser-dev"


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


def test_jiemian_public_parser_search_falls_back_to_fixture_mock_when_live_disabled() -> None:
    profile = load_selector_profile("jiemian")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.search_public_pages("Tesla", limit=10)

    assert result.metadata["live_fetch_enabled"] is False
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert 1 <= len(result.posts) <= 5
    assert result.posts[0].platform == "jiemian"
    assert result.posts[0].raw_data["mode"] == "fixture"


def test_hupu_public_parser_search_uses_fixture_thread_when_live_disabled() -> None:
    profile = load_selector_profile("hupu")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.search_public_pages("Tesla", limit=10)

    assert result.metadata["live_fetch_enabled"] is False
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert result.metadata["post_count"] == 1
    assert result.metadata["comment_count"] == 2
    assert result.metadata["schema_valid"] is True
    assert len(result.posts) == 1
    assert len(result.comments) == 2
    assert result.posts[0].platform == "hupu"
    assert result.posts[0].title == "Tesla service discussion on Hupu"
    assert result.comments[0].comment_id == "hupu_reply_001"


def test_maimai_public_parser_search_uses_fixture_post_when_live_disabled() -> None:
    profile = load_selector_profile("maimai")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.search_public_pages("Tesla", limit=10)

    assert result.metadata["live_fetch_enabled"] is False
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert result.metadata["post_count"] == 1
    assert result.metadata["comment_count"] == 2
    assert result.metadata["schema_valid"] is True
    assert len(result.posts) == 1
    assert len(result.comments) == 2
    assert result.posts[0].platform == "maimai"
    assert result.posts[0].title == "Tesla workplace discussion on Maimai"
    assert result.comments[0].comment_id == "maimai_reply_001"


def test_maimai_public_parser_remains_fixture_only_when_global_live_fetch_enabled() -> None:
    profile = load_selector_profile("maimai")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=True, rate_limit_seconds=0),
    )

    result = parser.search_public_pages("Tesla", limit=10)

    assert parser.fetcher.live_fetch_enabled is False
    assert result.metadata["live_fetch_enabled"] is False
    assert result.metadata["live_fetch_attempted"] is False
    assert result.metadata["live_fetch_allowed"] is False
    assert result.metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert result.metadata["fetch_status"] == "disabled"
    assert len(result.posts) == 1
    assert len(result.comments) == 2


def test_tieba_public_parser_search_uses_fixture_thread_when_live_disabled() -> None:
    profile = load_selector_profile("tieba")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.search_public_pages("Tesla", limit=10)

    assert result.metadata["live_fetch_enabled"] is False
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert result.metadata["post_count"] == 1
    assert result.metadata["comment_count"] == 3
    assert result.metadata["schema_valid"] is True
    assert len(result.posts) == 1
    assert len(result.comments) == 3
    assert result.posts[0].platform == "tieba"
    assert result.posts[0].title == "Tesla service discussion on Baidu Tieba"
    assert result.comments[0].comment_id == "tieba_reply_001"
    assert result.comments[0].raw_data["floor_number"] == "1F"


def test_tieba_public_parser_remains_fixture_only_when_global_live_fetch_enabled() -> None:
    profile = load_selector_profile("tieba")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=True, rate_limit_seconds=0),
    )

    result = parser.search_public_pages("Tesla", limit=10)

    assert parser.fetcher.live_fetch_enabled is False
    assert result.metadata["live_fetch_enabled"] is False
    assert result.metadata["live_fetch_attempted"] is False
    assert result.metadata["live_fetch_allowed"] is False
    assert result.metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert result.metadata["fetch_status"] == "disabled"
    assert len(result.posts) == 1
    assert len(result.comments) == 3


def test_nga_public_parser_search_uses_fixture_thread_when_live_disabled() -> None:
    profile = load_selector_profile("nga")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )

    result = parser.search_public_pages("Tesla", limit=10)

    assert result.metadata["live_fetch_enabled"] is False
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert result.metadata["post_count"] == 1
    assert result.metadata["comment_count"] == 3
    assert result.metadata["schema_valid"] is True
    assert len(result.posts) == 1
    assert len(result.comments) == 3
    assert result.posts[0].platform == "nga"
    assert result.posts[0].title == "Tesla service discussion on NGA"
    assert result.comments[0].comment_id == "nga_reply_001"
    assert result.comments[0].raw_data["floor_number"] == "1F"


def test_nga_public_parser_remains_fixture_only_when_global_live_fetch_enabled() -> None:
    profile = load_selector_profile("nga")
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=True, rate_limit_seconds=0),
    )

    result = parser.search_public_pages("Tesla", limit=10)

    assert parser.fetcher.live_fetch_enabled is False
    assert result.metadata["live_fetch_enabled"] is False
    assert result.metadata["live_fetch_attempted"] is False
    assert result.metadata["live_fetch_allowed"] is False
    assert result.metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert result.metadata["fetch_status"] == "disabled"
    assert len(result.posts) == 1
    assert len(result.comments) == 3


def test_the_paper_live_enabled_robots_blocked_falls_back_to_fixture_mock() -> None:
    profile = load_selector_profile("the_paper")
    fetcher = FakeLiveFetcher(
        PublicFetchResult(
            ok=False,
            url="https://www.thepaper.cn/newsDetail_forward_fixture",
            fallback_reason_category="robots_disallowed",
            live_fetch_enabled=True,
            live_fetch_attempted=True,
            live_fetch_allowed=False,
            fetch_status="robots_disallowed",
        )
    )
    parser = BasePublicParser(profile, fetcher=fetcher)

    result = parser.search_public_pages("fixture", limit=3)

    assert result.metadata["live_fetch_enabled"] is True
    assert result.metadata["live_fetch_attempted"] is True
    assert result.metadata["live_fetch_allowed"] is False
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "robots_disallowed"
    assert result.metadata["fetch_status"] == "robots_disallowed"
    assert result.posts
    assert result.posts[0].raw_data["mode"] == "fixture"


def test_the_paper_live_enabled_network_error_falls_back_to_fixture_mock() -> None:
    profile = load_selector_profile("the_paper")
    fetcher = FakeLiveFetcher(
        PublicFetchResult(
            ok=False,
            url="https://www.thepaper.cn/newsDetail_forward_fixture",
            fallback_reason_category="network_error",
            live_fetch_enabled=True,
            live_fetch_attempted=True,
            live_fetch_allowed=True,
            fetch_status="network_error",
        )
    )
    parser = BasePublicParser(profile, fetcher=fetcher)

    result = parser.search_public_pages("fixture", limit=3)

    assert result.metadata["live_fetch_enabled"] is True
    assert result.metadata["live_fetch_attempted"] is True
    assert result.metadata["live_fetch_allowed"] is True
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "network_error"
    assert result.metadata["fetch_status"] == "network_error"
    assert result.posts
    assert result.posts[0].platform == "the_paper"


def test_the_paper_live_enabled_selector_error_falls_back_to_fixture_mock() -> None:
    profile = load_selector_profile("the_paper")
    fetcher = FakeLiveFetcher(
        PublicFetchResult(
            ok=True,
            url="https://www.thepaper.cn/newsDetail_forward_fixture",
            html="<html><body><article><h1>No matching selector</h1></article></body></html>",
            live_fetch_enabled=True,
            live_fetch_attempted=True,
            live_fetch_allowed=True,
            fetch_status="ok",
        )
    )
    parser = BasePublicParser(profile, fetcher=fetcher)

    result = parser.search_public_pages("fixture", limit=3)

    assert result.metadata["live_fetch_enabled"] is True
    assert result.metadata["live_fetch_attempted"] is True
    assert result.metadata["live_fetch_allowed"] is True
    assert result.metadata["fallback_used"] is True
    assert result.metadata["fallback_reason_category"] == "selector_missing"
    assert result.metadata["fetch_status"] == "selector_missing"
    assert result.posts
    assert result.posts[0].raw_data["mode"] == "fixture"


def test_the_paper_live_enabled_valid_html_returns_raw_post() -> None:
    profile = load_selector_profile("the_paper")
    fetcher = FakeLiveFetcher(
        PublicFetchResult(
            ok=True,
            url="https://www.thepaper.cn/newsDetail_forward_fixture",
            html=_fixture_html(),
            status_code=200,
            live_fetch_enabled=True,
            live_fetch_attempted=True,
            live_fetch_allowed=True,
            fetch_status="ok",
        )
    )
    parser = BasePublicParser(profile, fetcher=fetcher)

    result = parser.search_public_pages("fixture", limit=3)

    assert result.metadata["live_fetch_enabled"] is True
    assert result.metadata["live_fetch_attempted"] is True
    assert result.metadata["live_fetch_allowed"] is True
    assert result.metadata["fallback_used"] is False
    assert result.metadata["fallback_reason_category"] is None
    assert result.metadata["fetch_status"] == "ok"
    assert result.metadata["schema_valid"] is True
    assert len(result.posts) == 1
    assert isinstance(result.posts[0], RawPost)
    assert result.posts[0].platform == "the_paper"
    assert result.posts[0].raw_data["mode"] == "public_parser_live"


def test_public_parser_regression_corpus_handles_missing_optional_fields() -> None:
    for case_id in [
        "parser_the_paper_missing_author_edge",
        "parser_jiemian_missing_created_at_edge",
        "parser_hupu_missing_author_variant",
        "parser_tieba_missing_created_at_variant",
        "parser_nga_missing_author_variant",
        "parser_maimai_missing_created_at_variant",
    ]:
        result = _parse_inline_benchmark_case(case_id)

        assert len(result.posts) == 1
        assert all(RawPost.model_validate(post.model_dump(mode="json")) for post in result.posts)
        assert all(RawComment.model_validate(comment.model_dump(mode="json")) for comment in result.comments)
        assert result.metadata["live_fetch_enabled"] is False
        assert result.metadata["schema_valid"] is True


def test_public_parser_regression_corpus_handles_no_comments_and_nested_content() -> None:
    for case_id in [
        "parser_hupu_no_comments_edge",
        "parser_tieba_no_comments_variant",
        "parser_nga_nested_content_variant",
        "parser_maimai_nested_content_variant",
    ]:
        case = _parser_benchmark_case(case_id)
        result = _parse_inline_benchmark_case(case_id)

        assert len(result.posts) >= case["min_posts"]
        assert len(result.comments) >= case["min_comments"]
        assert all(RawPost.model_validate(post.model_dump(mode="json")) for post in result.posts)
        assert all(RawComment.model_validate(comment.model_dump(mode="json")) for comment in result.comments)
        assert result.metadata["live_fetch_enabled"] is False
        assert result.metadata["schema_valid"] is True


def test_public_parser_regression_corpus_malformed_variants_fail_safely() -> None:
    for case_id in [
        "parser_the_paper_malformed_partial_variant",
        "parser_jiemian_malformed_partial_variant",
        "parser_hupu_malformed_partial_variant",
        "parser_tieba_malformed_partial_variant",
        "parser_nga_malformed_partial_variant",
        "parser_maimai_malformed_partial_variant",
    ]:
        result = _parse_inline_benchmark_case(case_id)

        assert result.posts == []
        assert result.comments == []
        assert result.metadata["fallback_used"] is True
        assert result.metadata["fallback_reason_category"] == "selector_missing"
        assert result.metadata["live_fetch_enabled"] is False
        assert result.metadata["schema_valid"] is True
