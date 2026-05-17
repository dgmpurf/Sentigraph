from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


SelectorRepairStatus = Literal[
    "suggested",
    "draft",
    "preview_ok",
    "preview_failed",
    "invalid_platform",
    "provider_not_enabled",
    "not_configured",
    "error",
]


class SelectorCandidate(BaseModel):
    target: str
    selector: str
    selector_type: Literal["css"] = "css"
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    rationale: str = ""
    source: str = "mock_provider"


class SelectorRepairRequest(BaseModel):
    platform_id: str
    sanitized_html: str
    current_profile: dict[str, Any] = Field(default_factory=dict)
    extraction_targets: list[str] = Field(default_factory=list)
    parser_error_summary: str = ""
    mode: str = "mock"
    max_html_chars: int = 20000


class SelectorRepairSuggestion(BaseModel):
    platform_id: str
    status: SelectorRepairStatus = "suggested"
    candidates: list[SelectorCandidate] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    provider: str = "mock"
    generated_by_mock: bool = True
    applied: bool = False
    review_required: bool = True
    draft_id: str | None = None


class SelectorRepairPreviewResult(BaseModel):
    platform_id: str
    status: SelectorRepairStatus
    matched_targets: dict[str, bool] = Field(default_factory=dict)
    sample_values: dict[str, str] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    suggestion: SelectorRepairSuggestion | None = None
    profile_modified: bool = False


class SelectorRepairSuggestApiRequest(BaseModel):
    platform_id: str = Field(..., min_length=1, examples=["hupu"])
    html: str = Field(..., min_length=1)
    profile: dict[str, Any] = Field(default_factory=dict)
    extraction_targets: list[str] = Field(default_factory=list)
    error_summary: str = ""


class SelectorRepairPreviewApiRequest(BaseModel):
    platform_id: str = Field(..., min_length=1, examples=["hupu"])
    suggestion: SelectorRepairSuggestion
    fixture_html: str = Field(..., min_length=1)
