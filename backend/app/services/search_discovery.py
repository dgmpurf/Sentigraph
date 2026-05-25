from __future__ import annotations

from datetime import datetime, timezone

from app.schemas.search_discovery import (
    SearchDiscoveryBatch,
    SearchDiscoveryCandidate,
    SearchDiscoveryProviderStatus,
    SearchDiscoveryStatusResponse,
)


def get_search_discovery_status() -> SearchDiscoveryStatusResponse:
    return SearchDiscoveryStatusResponse(
        provider_statuses=get_search_discovery_provider_statuses(),
        review_flow=[
            "User enters keyword or event label.",
            "A configured provider or mock fixture returns candidate URLs, titles, and snippets only.",
            "User reviews candidates and accepts or rejects them.",
            "Accepted candidates become manual_url evidence, or wait for a reviewed public parser route.",
            "No automatic page fetching happens in the discovery step.",
        ],
        next_actions=[
            "Design read-only mock Search Discovery UI.",
            "Research RSS discovery pilot with fixture tests.",
            "Research GDELT or news discovery API terms and quota.",
            "Design user-reviewed candidate attach workflow.",
            "Keep automatic scraping, URL fetching, cookies, and third-party crawler integration out of scope.",
        ],
    )


def get_search_discovery_provider_statuses() -> list[SearchDiscoveryProviderStatus]:
    return [
        SearchDiscoveryProviderStatus(
            provider_id="search_engine_api",
            display_name="Search Engine APIs",
            provider_class="search_engine_api",
            status="not_configured",
            allowed_use="Use approved search APIs to return URL/title/snippet metadata after terms and quota review.",
            forbidden_use="Do not scrape SERP pages, bypass captcha, evade rate limits, or collect private data.",
            data_returned=["url", "title", "snippet", "source_name", "published_at_if_available"],
            full_content_available=False,
            requires_api_key=True,
            credential_present=False,
            current_sentigraph_status="planned_only",
            next_action="Choose an approved provider and add mocked fixtures before any real call.",
        ),
        SearchDiscoveryProviderStatus(
            provider_id="news_discovery_api",
            display_name="News Discovery APIs",
            provider_class="news_discovery_api",
            status="research_pending",
            allowed_use="Use approved news/discovery APIs for public article metadata and snippets.",
            forbidden_use="Do not copy paywalled/full content unless licensed; do not bypass website protections.",
            data_returned=["url", "title", "snippet", "source_name", "published_at"],
            full_content_available=False,
            requires_api_key=True,
            credential_present=False,
            current_sentigraph_status="planned_only",
            next_action="Research GDELT/news API terms and retention limits.",
        ),
        SearchDiscoveryProviderStatus(
            provider_id="rss_feeds",
            display_name="RSS / Atom Feeds",
            provider_class="rss",
            status="pilot_candidate",
            allowed_use="Use public feed metadata when feed terms permit it; keep tiny limits and fixture tests.",
            forbidden_use="Do not fetch private feeds, paywalled content, or subscriber-only metadata.",
            data_returned=["url", "title", "summary_or_snippet", "source_name", "published_at"],
            full_content_available=False,
            requires_api_key=False,
            credential_present=False,
            current_sentigraph_status="planned_only",
            next_action="Add an RSS fixture pilot only after source-specific review.",
        ),
        SearchDiscoveryProviderStatus(
            provider_id="site_public_search",
            display_name="Site-Specific Public Search Pages",
            provider_class="site_specific_public_search",
            status="review_required",
            allowed_use="Use only after site-specific policy and parser review, preferably as fixture-only first.",
            forbidden_use="Do not scrape dynamic search pages, use cookies, or bypass login/captcha/anti-bot systems.",
            data_returned=["url", "title", "snippet_if_public"],
            full_content_available=False,
            requires_api_key=False,
            credential_present=False,
            current_sentigraph_status="not_implemented",
            next_action="Keep out of live product until parser rules explicitly allow it.",
        ),
        SearchDiscoveryProviderStatus(
            provider_id="user_url_list",
            display_name="User-Provided URL Lists",
            provider_class="user_provided_url_list",
            status="supported_via_manual_or_upload",
            allowed_use="Users may paste or upload lawful public URLs and accompanying text for review.",
            forbidden_use="Do not treat unknown URL lists as permission to scrape or fetch pages automatically.",
            data_returned=["url", "title_if_user_provided", "snippet_if_user_provided"],
            full_content_available=False,
            requires_api_key=False,
            credential_present=False,
            current_sentigraph_status="manual_url_and_csv_available",
            next_action="Route accepted URLs to Manual URL Evidence or CSV/Excel import.",
        ),
        SearchDiscoveryProviderStatus(
            provider_id="data_vendor",
            display_name="Data Vendor Discovery Indexes",
            provider_class="data_vendor",
            status="future_contract_required",
            allowed_use="Use licensed vendor metadata only after contract, retention, and redaction review.",
            forbidden_use="Do not ingest unlicensed payloads or credential-bearing exports.",
            data_returned=["url", "title", "snippet", "source_name", "published_at", "vendor_metadata"],
            full_content_available=False,
            requires_api_key=True,
            credential_present=False,
            current_sentigraph_status="future_only",
            next_action="Wait for a selected vendor and mocked contract fixtures.",
        ),
        SearchDiscoveryProviderStatus(
            provider_id="mock_fixture",
            display_name="Mock Search Discovery Fixture",
            provider_class="mock_fixture",
            status="available_now",
            allowed_use="Return deterministic candidate URLs, titles, and snippets for UI/API contract testing.",
            forbidden_use="Do not present mock candidates as real search results.",
            data_returned=["url", "title", "snippet", "source_name", "published_at"],
            full_content_available=False,
            requires_api_key=False,
            credential_present=False,
            current_sentigraph_status="implemented_static_mock",
            next_action="Use for UI planning and regression tests only.",
        ),
    ]


def get_mock_search_discovery_candidates(query: str = "Tesla") -> SearchDiscoveryBatch:
    safe_query = _safe_query(query)
    slug = _slugify(safe_query)
    candidates = [
        SearchDiscoveryCandidate(
            candidate_id=f"mock_search_{slug}_article_001",
            query=safe_query,
            provider="mock_fixture",
            platform_hint="news_site",
            title=f"{safe_query} public article discussion",
            snippet="Mock discovery metadata only: a public article may provide timeline and stakeholder context.",
            url=f"https://example.test/news/{slug}-public-article",
            published_at="2026-05-25T08:00:00Z",
            source_name="Mock News Index",
            content_type_hint="article",
            confidence=0.82,
            safety_notes=_candidate_safety_notes(),
        ),
        SearchDiscoveryCandidate(
            candidate_id=f"mock_search_{slug}_video_001",
            query=safe_query,
            provider="mock_fixture",
            platform_hint="youtube",
            title=f"{safe_query} public video reaction",
            snippet="Mock discovery metadata only: a video URL could be reviewed before official API or manual evidence attach.",
            url=f"https://example.test/video/{slug}-public-video",
            published_at="2026-05-25T08:20:00Z",
            source_name="Mock Video Index",
            content_type_hint="video",
            confidence=0.76,
            safety_notes=_candidate_safety_notes(),
        ),
        SearchDiscoveryCandidate(
            candidate_id=f"mock_search_{slug}_forum_001",
            query=safe_query,
            provider="mock_fixture",
            platform_hint="forum",
            title=f"{safe_query} forum thread candidate",
            snippet="Mock discovery metadata only: user review is required before adding any thread text as evidence.",
            url=f"https://example.test/forum/{slug}-thread",
            published_at="2026-05-25T08:35:00Z",
            source_name="Mock Forum Index",
            content_type_hint="post",
            confidence=0.68,
            safety_notes=_candidate_safety_notes(),
        ),
        SearchDiscoveryCandidate(
            candidate_id=f"mock_search_{slug}_rss_001",
            query=safe_query,
            provider="mock_fixture",
            platform_hint="rss",
            title=f"{safe_query} RSS item candidate",
            snippet="Mock discovery metadata only: RSS pilot candidates should still be reviewed before evidence attach.",
            url=f"https://example.test/rss/{slug}-item",
            published_at="2026-05-25T08:50:00Z",
            source_name="Mock RSS Feed",
            content_type_hint="search_result",
            confidence=0.64,
            safety_notes=_candidate_safety_notes(),
        ),
    ]
    return SearchDiscoveryBatch(
        query=safe_query,
        generated_at=datetime.now(timezone.utc),
        candidates=candidates,
        candidate_count=len(candidates),
        provider_statuses=[provider for provider in get_search_discovery_provider_statuses() if provider.provider_id == "mock_fixture"],
    )


def _candidate_safety_notes() -> list[str]:
    return [
        "mock fixture only",
        "URL was not fetched",
        "snippet is not full content",
        "human review required before attach",
    ]


def _safe_query(query: str) -> str:
    text = " ".join(str(query or "Tesla").split()).strip()
    return text[:120] or "Tesla"


def _slugify(value: str) -> str:
    slug = "".join(char.lower() if char.isalnum() else "-" for char in value)
    slug = "-".join(part for part in slug.split("-") if part)
    return slug[:64] or "query"
