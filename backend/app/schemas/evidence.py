from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


EvidenceType = Literal[
    "video",
    "article",
    "post",
    "comment",
    "reply",
    "title",
    "body_text",
    "metadata",
    "interaction_metric",
    "interaction_metrics",
    "search_result",
    "uploaded_record",
]

EvidenceAcquisitionMode = Literal[
    "official_api_public",
    "official_api_oauth",
    "public_parser",
    "search_discovery",
    "user_upload",
    "manual_url",
    "data_vendor",
    "mock_fixture",
]

EvidenceSourceType = Literal[
    "youtube",
    "douyin",
    "bilibili",
    "weibo",
    "xiaohongshu",
    "reddit",
    "news_site",
    "forum",
    "public_web",
    "uploaded_dataset",
    "mock",
]


class EvidenceNormalizationMetadata(BaseModel):
    normalized_from: str = "manual_payload"
    source_record_id: str | None = None
    source_type: EvidenceSourceType = "uploaded_dataset"
    acquisition_mode: EvidenceAcquisitionMode = "user_upload"
    normalized_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    warnings: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "secrets_redacted": True,
            "real_api_calls": False,
            "real_llm_calls": False,
            "private_data": False,
        }
    )


class EvidenceSource(BaseModel):
    platform: str = "uploaded_dataset"
    source_type: EvidenceSourceType = "uploaded_dataset"
    acquisition_mode: EvidenceAcquisitionMode = "user_upload"
    source_name: str | None = None
    source_url: str | None = None
    access_scope: str = "public_or_user_provided"
    credential_present: bool = False
    notes: str | None = None


class EvidenceItem(BaseModel):
    evidence_id: str = ""
    case_id: str | None = None
    platform: str = "uploaded_dataset"
    source_type: EvidenceSourceType = "uploaded_dataset"
    acquisition_mode: EvidenceAcquisitionMode = "user_upload"
    evidence_type: EvidenceType = "body_text"
    title: str | None = None
    body_text: str | None = None
    comment_text: str | None = None
    parent_id: str | None = None
    root_id: str | None = None
    author_id: str | None = None
    author_name: str | None = None
    url: str | None = None
    created_at: str | None = None
    like_count: int = 0
    reply_count: int = 0
    share_count: int = 0
    view_count: int = 0
    raw_data_safe: dict[str, Any] = Field(default_factory=dict)
    language: str = "unknown"
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    content_visibility: str = "public_or_user_provided"
    access_scope: str = "public_or_user_provided"
    ingestion_metadata: EvidenceNormalizationMetadata = Field(default_factory=EvidenceNormalizationMetadata)


class EvidenceIngestionBatch(BaseModel):
    source: EvidenceSource | None = None
    evidence_items: list[EvidenceItem] = Field(default_factory=list)
    ingestion_metadata: EvidenceNormalizationMetadata | None = None


class EvidenceIngestionResult(BaseModel):
    case_id: str
    status: Literal["attached", "empty", "not_found"] = "attached"
    evidence_items: list[EvidenceItem] = Field(default_factory=list)
    evidence_item_count: int = 0
    source_distribution: dict[str, int] = Field(default_factory=dict)
    evidence_type_counts: dict[str, int] = Field(default_factory=dict)
    top_titles: list[str] = Field(default_factory=list)
    representative_comments: list[str] = Field(default_factory=list)
    ingestion_metadata: EvidenceNormalizationMetadata = Field(default_factory=EvidenceNormalizationMetadata)
    warnings: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "secrets_exposed": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "scraping_bypass": False,
        }
    )
