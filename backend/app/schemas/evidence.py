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


class EvidenceImportColumnMapping(BaseModel):
    platform: str | None = None
    source_type: str | None = None
    acquisition_mode: str | None = None
    evidence_type: str | None = None
    title: str | None = None
    body_text: str | None = None
    comment_text: str | None = None
    parent_id: str | None = None
    root_id: str | None = None
    author_id: str | None = None
    author_name: str | None = None
    url: str | None = None
    created_at: str | None = None
    like_count: str | None = None
    reply_count: str | None = None
    share_count: str | None = None
    view_count: str | None = None
    language: str | None = None


class EvidenceImportValidationWarning(BaseModel):
    row_number: int | None = None
    field: str | None = None
    code: str
    message: str
    severity: Literal["info", "warning", "error"] = "warning"


class EvidenceImportRowPreview(BaseModel):
    row_number: int
    evidence_id: str
    platform: str = "uploaded_dataset"
    source_type: EvidenceSourceType = "uploaded_dataset"
    acquisition_mode: EvidenceAcquisitionMode = "user_upload"
    evidence_type: EvidenceType = "comment"
    title: str | None = None
    body_text: str | None = None
    comment_text: str | None = None
    author_name: str | None = None
    url: str | None = None
    created_at: str | None = None
    like_count: int = 0
    reply_count: int = 0
    share_count: int = 0
    view_count: int = 0
    warnings: list[EvidenceImportValidationWarning] = Field(default_factory=list)


class EvidenceImportPreviewRequest(BaseModel):
    filename: str = Field(..., min_length=1)
    content_base64: str | None = None
    content_text: str | None = None
    column_mapping: EvidenceImportColumnMapping = Field(default_factory=EvidenceImportColumnMapping)
    preview_limit: int = Field(default=10, ge=1, le=50)
    max_rows: int = Field(default=500, ge=1, le=1000)


class EvidenceImportPreviewResult(BaseModel):
    case_id: str
    filename: str
    status: Literal["preview_ready", "empty", "rejected"] = "preview_ready"
    detected_format: Literal["csv", "xlsx"] | None = None
    detected_columns: list[str] = Field(default_factory=list)
    column_mapping: EvidenceImportColumnMapping = Field(default_factory=EvidenceImportColumnMapping)
    total_rows: int = 0
    valid_row_count: int = 0
    duplicate_row_count: int = 0
    skipped_row_count: int = 0
    preview_rows: list[EvidenceImportRowPreview] = Field(default_factory=list)
    warnings: list[EvidenceImportValidationWarning] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "raw_file_persisted": False,
            "formulas_executed": False,
            "secrets_exposed": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "scraping_bypass": False,
        }
    )


class EvidenceImportCommitRequest(EvidenceImportPreviewRequest):
    pass


class EvidenceImportCommitResult(BaseModel):
    case_id: str
    filename: str
    status: Literal["committed", "empty", "rejected", "not_found"] = "committed"
    detected_format: Literal["csv", "xlsx"] | None = None
    imported_count: int = 0
    total_evidence_item_count: int = 0
    duplicate_row_count: int = 0
    skipped_row_count: int = 0
    evidence_items: list[EvidenceItem] = Field(default_factory=list)
    source_distribution: dict[str, int] = Field(default_factory=dict)
    evidence_type_counts: dict[str, int] = Field(default_factory=dict)
    warnings: list[EvidenceImportValidationWarning] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "raw_file_persisted": False,
            "formulas_executed": False,
            "secrets_exposed": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "scraping_bypass": False,
        }
    )
