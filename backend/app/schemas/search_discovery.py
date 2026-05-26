from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.evidence import EvidenceIngestionResult, EvidenceItem


SearchDiscoveryCandidateStatus = Literal["pending_review", "accepted", "rejected", "attached"]
SearchDiscoveryProviderType = Literal[
    "mock_static",
    "rss_mock",
    "gdelt_mock",
    "search_api_future",
    "user_url_list",
    "data_vendor_future",
]
SearchDiscoveryProviderLifecycleStatus = Literal[
    "mock_only",
    "planned",
    "disabled",
    "future_real_provider",
]


class SearchDiscoveryQuery(BaseModel):
    query: str = Field(default="Tesla", min_length=1, max_length=120)
    providers: list[str] = Field(default_factory=lambda: ["mock_static"])
    max_candidates: int = Field(default=5, ge=1, le=10)
    language: str = "auto"


class SearchDiscoveryCandidate(BaseModel):
    candidate_id: str
    query: str
    provider: str
    platform_hint: str = "public_web"
    title: str
    snippet: str
    url: str
    published_at: str | None = None
    source_name: str = "Mock Search Discovery"
    content_type_hint: str = "article"
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    acquisition_mode: Literal["search_discovery"] = "search_discovery"
    status: SearchDiscoveryCandidateStatus = "pending_review"
    safety_notes: list[str] = Field(default_factory=list)


class SearchDiscoveryProviderCapability(BaseModel):
    supports_query: bool = True
    supports_provider_selection: bool = True
    returns_title_snippet_url: bool = True
    returns_full_content: bool = False
    supports_live_fetch: bool = False
    supports_url_content_extraction: bool = False


class SearchDiscoveryProviderLimit(BaseModel):
    max_candidates_per_query: int = Field(default=10, ge=1, le=50)
    max_query_length: int = Field(default=120, ge=1, le=240)
    network_call_limit: int = 0
    safe_limit_note: str = "Static/mock provider; live network calls are disabled."


class SearchDiscoveryProviderSafetyBoundary(BaseModel):
    live_fetch_enabled: bool = False
    url_fetching: bool = False
    scraping: bool = False
    cookies_used: bool = False
    captcha_bypass: bool = False
    anti_bot_bypass: bool = False
    real_search_api_calls: bool = False
    real_website_api_calls: bool = False
    real_llm_calls: bool = False
    secrets_required: bool = False
    third_party_crawler_integrated: bool = False


class SearchDiscoveryProvider(BaseModel):
    provider_id: str
    provider_type: SearchDiscoveryProviderType
    display_name: str
    status: SearchDiscoveryProviderLifecycleStatus
    live_fetch_enabled: bool = False
    requires_api_key: bool = False
    requires_network: bool = False
    returns_full_content: bool = False
    returns_title_snippet_url: bool = True
    capabilities: SearchDiscoveryProviderCapability = Field(default_factory=SearchDiscoveryProviderCapability)
    limits: SearchDiscoveryProviderLimit = Field(default_factory=SearchDiscoveryProviderLimit)
    safety_boundary: SearchDiscoveryProviderSafetyBoundary = Field(default_factory=SearchDiscoveryProviderSafetyBoundary)
    safety_notes: list[str] = Field(default_factory=list)
    next_action: str


class SearchDiscoveryProviderStatus(SearchDiscoveryProvider):
    provider_class: str
    allowed_use: str
    forbidden_use: str
    data_returned: list[str] = Field(default_factory=list)
    full_content_available: bool = False
    credential_present: bool = False
    user_review_required: bool = True
    current_sentigraph_status: str


class SearchDiscoveryReviewDecision(BaseModel):
    candidate_id: str
    decision: SearchDiscoveryCandidateStatus
    reviewer_note: str | None = None
    route_to: Literal["manual_url", "public_parser_review", "csv_import", "reject"] = "manual_url"


class SearchDiscoveryCandidateAttachRequest(BaseModel):
    candidates: list[SearchDiscoveryCandidate] = Field(default_factory=list)
    reviewer_label: str | None = None
    user_attestation_text: str | None = None


class SearchDiscoveryCandidateAttachResult(BaseModel):
    case_id: str
    status: Literal["attached", "empty", "not_found"] = "attached"
    attached_candidate_count: int = 0
    skipped_candidate_count: int = 0
    rejected_candidate_count: int = 0
    attached_evidence_items: list[EvidenceItem] = Field(default_factory=list)
    evidence_result: EvidenceIngestionResult
    warnings: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "mock_candidates_only": True,
            "real_search_api_calls": False,
            "real_website_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "cookies_used": False,
            "captcha_bypass": False,
            "anti_bot_bypass": False,
            "real_llm_calls": False,
            "secrets_exposed": False,
            "third_party_crawler_integrated": False,
        }
    )


class SearchDiscoveryBatch(BaseModel):
    query: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    candidates: list[SearchDiscoveryCandidate] = Field(default_factory=list)
    candidate_count: int = 0
    provider_statuses: list[SearchDiscoveryProviderStatus] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "static_metadata_only": True,
            "mock_candidates_only": True,
            "real_search_api_calls": False,
            "real_website_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "cookies_used": False,
            "captcha_bypass": False,
            "anti_bot_bypass": False,
            "real_llm_calls": False,
            "secrets_exposed": False,
            "third_party_crawler_integrated": False,
        }
    )


class SearchDiscoveryStatusResponse(BaseModel):
    status: Literal["planning_mock_only"] = "planning_mock_only"
    provider_statuses: list[SearchDiscoveryProviderStatus] = Field(default_factory=list)
    review_flow: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "static_metadata_only": True,
            "mock_candidates_only": True,
            "real_search_api_calls": False,
            "real_website_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "cookies_used": False,
            "captcha_bypass": False,
            "anti_bot_bypass": False,
            "real_llm_calls": False,
            "secrets_exposed": False,
            "third_party_crawler_integrated": False,
        }
    )
