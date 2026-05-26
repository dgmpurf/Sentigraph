from __future__ import annotations

from datetime import datetime, timezone
import re

from app.schemas.evidence import EvidenceItem, EvidenceNormalizationMetadata
from app.schemas.search_discovery import (
    SearchDiscoveryBatch,
    SearchDiscoveryCandidate,
    SearchDiscoveryProviderStatus,
    SearchDiscoveryProviderType,
    SearchDiscoveryStatusResponse,
)
from app.services.evidence_ingestion import enrich_and_deduplicate_evidence_items


SECRET_TEXT_PATTERN = re.compile(
    r"\b(api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|password|cookie|authorization)\b\s*[:=]\s*([^\s,;]+)",
    re.IGNORECASE,
)


def get_search_discovery_status() -> SearchDiscoveryStatusResponse:
    return SearchDiscoveryStatusResponse(
        provider_statuses=get_search_discovery_provider_statuses(),
        review_flow=[
            "User enters keyword or event label.",
            "A configured provider or mock fixture returns candidate URLs, titles, and snippets only.",
            "User reviews candidates and accepts or rejects them.",
            "Accepted mock candidates can be attached as metadata-only EvidenceItems that require human review.",
            "Users can later enrich candidates through Manual URL Evidence, CSV/Excel import, or a reviewed public parser route.",
            "No automatic page fetching happens in the discovery step.",
        ],
        next_actions=[
            "Use the mock Search Discovery UI for safe candidate-review demos.",
            "Use RSS Mock and GDELT Mock providers as local fixture rehearsals only.",
            "Research real RSS/GDELT/news provider terms and quota before any live provider is added.",
            "Design real provider adapters only after provider terms, quota, and no-fetch tests are reviewed.",
            "Keep automatic scraping, URL fetching, cookies, and third-party crawler integration out of scope.",
        ],
    )


def get_search_discovery_providers() -> list[SearchDiscoveryProviderStatus]:
    return get_search_discovery_provider_statuses()


def get_search_discovery_provider_statuses() -> list[SearchDiscoveryProviderStatus]:
    return [
        _provider_status(
            provider_id="mock_static",
            provider_type="mock_static",
            display_name="Mock Static",
            status="mock_only",
            provider_class="mock_fixture",
            allowed_use="Return deterministic candidate URLs, titles, and snippets for UI/API contract testing.",
            forbidden_use="Do not present mock candidates as real search results.",
            current_sentigraph_status="implemented_static_mock",
            next_action="Use for UI planning, candidate-review demos, and regression tests only.",
        ),
        _provider_status(
            provider_id="rss_mock",
            provider_type="rss_mock",
            display_name="RSS Mock",
            status="mock_only",
            provider_class="rss_mock_fixture",
            allowed_use="Use local RSS-style fixture metadata to rehearse future feed discovery UX.",
            forbidden_use="Do not fetch RSS feeds, poll live feed URLs, or treat feed snippets as full article text.",
            current_sentigraph_status="implemented_static_mock",
            next_action="Keep as fixture-only until source-specific feed terms and no-fetch tests are reviewed.",
            safety_notes=[
                "RSS mock fixture only",
                "No live RSS fetch",
                "No URL content extraction",
                "Candidate metadata requires human review",
            ],
        ),
        _provider_status(
            provider_id="gdelt_mock",
            provider_type="gdelt_mock",
            display_name="GDELT Mock",
            status="mock_only",
            provider_class="gdelt_mock_fixture",
            allowed_use="Use local GDELT-style news-discovery fixtures to rehearse URL/title/snippet review.",
            forbidden_use="Do not call GDELT APIs, fetch article URLs, or copy full article content.",
            current_sentigraph_status="implemented_static_mock",
            next_action="Research GDELT/news API terms and quotas before any real provider adapter.",
            safety_notes=[
                "GDELT mock fixture only",
                "No real GDELT API call",
                "No URL content extraction",
                "Candidate metadata requires human review",
            ],
        ),
        _provider_status(
            provider_id="search_api_future",
            provider_type="search_api_future",
            display_name="Search API Future",
            status="future_real_provider",
            provider_class="search_api_future",
            allowed_use="Use approved search/news APIs to return URL/title/snippet metadata after terms and quota review.",
            forbidden_use="Do not scrape SERP pages, bypass captcha, evade rate limits, or collect private data.",
            requires_api_key=True,
            requires_network=True,
            current_sentigraph_status="future_only",
            next_action="Choose an approved provider and add mocked contract fixtures before any real call.",
        ),
        _provider_status(
            provider_id="user_url_list",
            provider_type="user_url_list",
            display_name="User-Provided URL Lists",
            status="planned",
            provider_class="user_provided_url_list",
            allowed_use="Users may paste or upload lawful public URLs and accompanying text for review.",
            forbidden_use="Do not treat unknown URL lists as permission to scrape or fetch pages automatically.",
            data_returned=["url", "title_if_user_provided", "snippet_if_user_provided"],
            current_sentigraph_status="manual_url_and_csv_available",
            next_action="Route accepted URLs to Manual URL Evidence or CSV/Excel import.",
        ),
        _provider_status(
            provider_id="data_vendor_future",
            provider_type="data_vendor_future",
            display_name="Data Vendor Discovery Indexes",
            status="future_real_provider",
            provider_class="data_vendor",
            allowed_use="Use licensed vendor metadata only after contract, retention, and redaction review.",
            forbidden_use="Do not ingest unlicensed payloads or credential-bearing exports.",
            data_returned=["url", "title", "snippet", "source_name", "published_at", "vendor_metadata"],
            requires_api_key=True,
            requires_network=True,
            current_sentigraph_status="future_only",
            next_action="Wait for a selected vendor and mocked contract fixtures.",
        ),
    ]


def get_mock_search_discovery_candidates(query: str = "Tesla", provider: str = "mock_static") -> SearchDiscoveryBatch:
    safe_query = _safe_query(query)
    slug = _slugify(safe_query)
    selected_provider = _normalize_provider(provider)
    candidates = _candidate_fixtures(safe_query, slug, selected_provider)
    return SearchDiscoveryBatch(
        query=safe_query,
        generated_at=datetime.now(timezone.utc),
        candidates=candidates,
        candidate_count=len(candidates),
        provider_statuses=[provider_status for provider_status in get_search_discovery_provider_statuses() if provider_status.provider_id == selected_provider],
    )


def _candidate_fixtures(
    safe_query: str,
    slug: str,
    provider: SearchDiscoveryProviderType,
) -> list[SearchDiscoveryCandidate]:
    if provider == "rss_mock":
        return [
            SearchDiscoveryCandidate(
                candidate_id=f"rss_mock_{slug}_feed_001",
                query=safe_query,
                provider="rss_mock",
                platform_hint="news_site",
                title=f"{safe_query} RSS feed item: product and policy updates",
                snippet="RSS mock metadata only: a feed item title and summary may help reviewers decide whether to attach article text later.",
                url=f"https://example.test/rss/{slug}-feed-item-001",
                published_at="2026-05-25T09:05:00Z",
                source_name="Mock RSS Feed",
                content_type_hint="search_result",
                confidence=0.74,
                safety_notes=_candidate_safety_notes("rss_mock"),
            ),
            SearchDiscoveryCandidate(
                candidate_id=f"rss_mock_{slug}_feed_002",
                query=safe_query,
                provider="rss_mock",
                platform_hint="public_web",
                title=f"{safe_query} RSS feed item: community reaction roundup",
                snippet="RSS mock metadata only: full content is not fetched; users must review and provide lawful text separately.",
                url=f"https://example.test/rss/{slug}-feed-item-002",
                published_at="2026-05-25T09:25:00Z",
                source_name="Mock Public Feed",
                content_type_hint="search_result",
                confidence=0.69,
                safety_notes=_candidate_safety_notes("rss_mock"),
            ),
            SearchDiscoveryCandidate(
                candidate_id=f"rss_mock_{slug}_feed_003",
                query=safe_query,
                provider="rss_mock",
                platform_hint="forum",
                title=f"{safe_query} RSS feed item: forum digest candidate",
                snippet="RSS mock metadata only: a digest URL can be reviewed, but Sentigraph will not fetch or parse it automatically.",
                url=f"https://example.test/rss/{slug}-forum-digest",
                published_at="2026-05-25T09:45:00Z",
                source_name="Mock Forum RSS",
                content_type_hint="post",
                confidence=0.62,
                safety_notes=_candidate_safety_notes("rss_mock"),
            ),
        ]
    if provider == "gdelt_mock":
        return [
            SearchDiscoveryCandidate(
                candidate_id=f"gdelt_mock_{slug}_news_001",
                query=safe_query,
                provider="gdelt_mock",
                platform_hint="news_site",
                title=f"{safe_query} GDELT-style news candidate: event timeline",
                snippet="GDELT mock metadata only: a news-discovery record may identify a public URL, title, source, and snippet.",
                url=f"https://example.test/gdelt/{slug}-timeline-candidate",
                published_at="2026-05-25T10:00:00Z",
                source_name="Mock GDELT News Index",
                content_type_hint="article",
                confidence=0.81,
                safety_notes=_candidate_safety_notes("gdelt_mock"),
            ),
            SearchDiscoveryCandidate(
                candidate_id=f"gdelt_mock_{slug}_news_002",
                query=safe_query,
                provider="gdelt_mock",
                platform_hint="news_site",
                title=f"{safe_query} GDELT-style news candidate: market reaction",
                snippet="GDELT mock metadata only: this is not full article content and requires human review before evidence use.",
                url=f"https://example.test/gdelt/{slug}-market-reaction",
                published_at="2026-05-25T10:25:00Z",
                source_name="Mock Global News Index",
                content_type_hint="article",
                confidence=0.77,
                safety_notes=_candidate_safety_notes("gdelt_mock"),
            ),
            SearchDiscoveryCandidate(
                candidate_id=f"gdelt_mock_{slug}_news_003",
                query=safe_query,
                provider="gdelt_mock",
                platform_hint="public_web",
                title=f"{safe_query} GDELT-style candidate: cross-source mention",
                snippet="GDELT mock metadata only: accepted candidates become review-needed EvidenceItems without fetching the URL.",
                url=f"https://example.test/gdelt/{slug}-cross-source-mention",
                published_at="2026-05-25T10:45:00Z",
                source_name="Mock Cross-Source Index",
                content_type_hint="search_result",
                confidence=0.66,
                safety_notes=_candidate_safety_notes("gdelt_mock"),
            ),
        ]

    return [
        SearchDiscoveryCandidate(
            candidate_id=f"mock_search_{slug}_article_001",
            query=safe_query,
            provider="mock_static",
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
            provider="mock_static",
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
            provider="mock_static",
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
            provider="mock_static",
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


def _provider_status(
    *,
    provider_id: str,
    provider_type: SearchDiscoveryProviderType,
    display_name: str,
    status: str,
    provider_class: str,
    allowed_use: str,
    forbidden_use: str,
    current_sentigraph_status: str,
    next_action: str,
    data_returned: list[str] | None = None,
    requires_api_key: bool = False,
    requires_network: bool = False,
    safety_notes: list[str] | None = None,
) -> SearchDiscoveryProviderStatus:
    return SearchDiscoveryProviderStatus(
        provider_id=provider_id,
        provider_type=provider_type,
        display_name=display_name,
        status=status,
        live_fetch_enabled=False,
        requires_api_key=requires_api_key,
        requires_network=requires_network,
        returns_full_content=False,
        returns_title_snippet_url=True,
        safety_notes=safety_notes
        or [
            "Static provider metadata only",
            "No live network fetch",
            "No URL content extraction",
            "Human review required before evidence use",
        ],
        provider_class=provider_class,
        allowed_use=allowed_use,
        forbidden_use=forbidden_use,
        data_returned=data_returned or ["url", "title", "snippet", "source_name", "published_at"],
        full_content_available=False,
        credential_present=False,
        user_review_required=True,
        current_sentigraph_status=current_sentigraph_status,
        next_action=next_action,
    )


def search_discovery_candidates_to_evidence_items(
    *,
    case_id: str,
    candidates: list[SearchDiscoveryCandidate],
    user_attestation_text: str | None = None,
    reviewer_label: str | None = None,
) -> tuple[list[EvidenceItem], int, int, list[str]]:
    """Convert accepted mock/static candidates into conservative EvidenceItems.

    The conversion is metadata-only. It never fetches candidate URLs or calls a
    discovery provider.
    """

    evidence_items: list[EvidenceItem] = []
    skipped_count = 0
    rejected_count = 0
    warnings: list[str] = []

    for candidate in candidates:
        if candidate.status == "rejected":
            rejected_count += 1
            continue
        if candidate.status not in {"accepted", "attached"}:
            skipped_count += 1
            warnings.append(f"candidate_not_accepted:{candidate.candidate_id}")
            continue

        redacted_title, title_redacted = _redact_text(candidate.title)
        redacted_snippet, snippet_redacted = _redact_text(candidate.snippet)
        redacted_url, url_redacted = _redact_text(candidate.url)
        redacted_source_name, source_redacted = _redact_text(candidate.source_name)
        redaction_warnings = [
            field
            for field, redacted in (
                ("title", title_redacted),
                ("snippet", snippet_redacted),
                ("url", url_redacted),
                ("source_name", source_redacted),
            )
            if redacted
        ]

        evidence_type = _candidate_evidence_type(candidate.content_type_hint)
        source_type = _candidate_source_type(candidate.platform_hint)
        platform = _candidate_platform(candidate.platform_hint)
        evidence_items.append(
            EvidenceItem(
                evidence_id=f"evidence_search_discovery_{_safe_token(candidate.candidate_id)}",
                case_id=case_id,
                platform=platform,
                source_type=source_type,
                acquisition_mode="search_discovery",
                evidence_type=evidence_type,
                title=redacted_title,
                body_text=redacted_snippet,
                url=redacted_url,
                created_at=candidate.published_at,
                raw_data_safe={
                    "candidate_id": candidate.candidate_id,
                    "query": _redact_text(candidate.query)[0],
                    "provider": _redact_text(candidate.provider)[0],
                    "source_name": redacted_source_name,
                    "platform_hint": _redact_text(candidate.platform_hint)[0],
                    "content_type_hint": _redact_text(candidate.content_type_hint)[0],
                    "candidate_status": candidate.status,
                    "safety_notes": [_redact_text(note)[0] for note in candidate.safety_notes],
                    "url_fetched": False,
                    "scraping": False,
                },
                confidence=candidate.confidence,
                language="unknown",
                content_visibility="public_metadata_only",
                access_scope="public_metadata_only",
                ingestion_metadata=EvidenceNormalizationMetadata(
                    normalized_from="search_discovery_candidate",
                    source_record_id=candidate.candidate_id,
                    source_type=source_type,
                    acquisition_mode="search_discovery",
                    warnings=[f"secret_like_candidate_field_redacted:{field}" for field in redaction_warnings],
                ),
                provenance_type="search_discovery_candidate",
                verification_status="source_url_provided_unverified",
                trust_score=0.42,
                trust_label="low",
                source_url=redacted_url,
                source_url_present=bool(redacted_url),
                source_platform_claim=candidate.platform_hint,
                source_capture_method="search_result_metadata",
                submitted_by_label=reviewer_label,
                user_attestation_required=not bool((user_attestation_text or "").strip()),
                user_attestation_text=user_attestation_text,
                review_status="not_reviewed" if user_attestation_text else "review_needed",
                risk_flags=["search_discovery_metadata_only", *[f"secret_redacted:{field}" for field in redaction_warnings]],
                verification_notes=[
                    "Search discovery candidates are metadata leads only.",
                    "Candidate URL content was not fetched.",
                    "Human review is required before treating the source as stronger evidence.",
                ],
            )
        )

    return (
        enrich_and_deduplicate_evidence_items(evidence_items),
        skipped_count,
        rejected_count,
        _dedupe_warnings(warnings),
    )


def _normalize_provider(provider: str | None) -> SearchDiscoveryProviderType:
    normalized = str(provider or "mock_static").strip().lower()
    if normalized == "mock_fixture":
        return "mock_static"
    if normalized in {"mock_static", "rss_mock", "gdelt_mock"}:
        return normalized  # type: ignore[return-value]
    return "mock_static"


def _candidate_safety_notes(provider: str = "mock_static") -> list[str]:
    provider_note = {
        "rss_mock": "RSS mock fixture only",
        "gdelt_mock": "GDELT mock fixture only",
    }.get(provider, "mock fixture only")
    return [
        provider_note,
        "URL was not fetched",
        "snippet is not full content",
        "human review required before attach",
    ]


def _candidate_evidence_type(content_type_hint: str) -> str:
    normalized = (content_type_hint or "").strip().lower()
    if normalized in {"video", "article", "post", "comment", "reply", "title", "body_text", "interaction_metric", "search_result"}:
        return normalized
    return "search_result"


def _candidate_source_type(platform_hint: str) -> str:
    normalized = (platform_hint or "").strip().lower()
    if normalized in {"youtube", "douyin", "bilibili", "weibo", "xiaohongshu", "reddit"}:
        return normalized
    if normalized in {"news_site", "the_paper", "jiemian", "toutiao"}:
        return "news_site"
    if normalized in {"forum", "hupu", "tieba", "nga", "maimai", "douban", "zhihu"}:
        return "forum"
    return "public_web"


def _candidate_platform(platform_hint: str) -> str:
    normalized = (platform_hint or "").strip().lower()
    if normalized in {"", "rss", "search", "search_discovery"}:
        return "public_web"
    return normalized


def _redact_text(value: str | None) -> tuple[str, bool]:
    text = str(value or "").strip()
    redacted = SECRET_TEXT_PATTERN.sub(lambda match: f"{match.group(1)}=[REDACTED]", text)
    return redacted, redacted != text


def _dedupe_warnings(warnings: list[str]) -> list[str]:
    values: list[str] = []
    for warning in warnings:
        if warning and warning not in values:
            values.append(warning)
    return values


def _safe_query(query: str) -> str:
    text = " ".join(str(query or "Tesla").split()).strip()
    return text[:120] or "Tesla"


def _slugify(value: str) -> str:
    slug = "".join(char.lower() if char.isalnum() else "-" for char in value)
    slug = "-".join(part for part in slug.split("-") if part)
    return slug[:64] or "query"


def _safe_token(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "_" for char in str(value or "")).strip("_") or "candidate"
