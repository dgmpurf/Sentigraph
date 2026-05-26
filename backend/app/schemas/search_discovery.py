from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.evidence import EvidenceIngestionResult, EvidenceItem


SearchDiscoveryCandidateStatus = Literal["pending_review", "accepted", "rejected", "attached"]


class SearchDiscoveryQuery(BaseModel):
    query: str = Field(default="Tesla", min_length=1, max_length=120)
    providers: list[str] = Field(default_factory=lambda: ["mock_fixture"])
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


class SearchDiscoveryProviderStatus(BaseModel):
    provider_id: str
    display_name: str
    provider_class: str
    status: str
    allowed_use: str
    forbidden_use: str
    data_returned: list[str] = Field(default_factory=list)
    full_content_available: bool = False
    requires_api_key: bool = False
    credential_present: bool = False
    user_review_required: bool = True
    current_sentigraph_status: str
    next_action: str


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
