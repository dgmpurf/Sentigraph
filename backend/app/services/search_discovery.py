from __future__ import annotations

from datetime import datetime, timezone
import re

from app.schemas.evidence import EvidenceItem, EvidenceNormalizationMetadata
from app.schemas.search_discovery import (
    SearchDiscoveryBatch,
    SearchDiscoveryCandidate,
    SearchDiscoveryProviderStatus,
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
            "Research RSS discovery pilot with fixture tests.",
            "Research GDELT or news discovery API terms and quota.",
            "Design real provider adapters only after provider terms, quota, and no-fetch tests are reviewed.",
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


def _candidate_safety_notes() -> list[str]:
    return [
        "mock fixture only",
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
