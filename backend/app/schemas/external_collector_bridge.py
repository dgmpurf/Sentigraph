from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


ExternalCollectorValidationStatus = Literal["pass", "warn", "fail"]
ExternalCollectorMatchedField = Literal[
    "package_name", "case_id", "case_title", "sample_labels", "sample_quality_label"
]


class ExternalCollectorDiscoveryResult(BaseModel):
    """Metadata for an existing export package, never a search candidate."""

    package_name: str = Field(min_length=1, max_length=255)
    case_id: str = Field(default="", max_length=120)
    case_title: str = Field(default="", max_length=200)
    sample_labels: list[str] = Field(default_factory=list, max_length=8)
    package_role: str = Field(default="", max_length=80)
    validation_status: str = Field(default="unknown", max_length=40)
    exported_at: str | None = Field(default=None, max_length=40)
    evidence_count: int = Field(default=0, ge=0, le=1_000_000_000)
    source_count: int = Field(default=0, ge=0, le=1_000_000_000)
    comment_count: int = Field(default=0, ge=0, le=1_000_000_000)
    root_count: int = Field(default=0, ge=0, le=1_000_000_000)
    recommended_for_sentigraph_demo: bool = False
    sample_quality_label: str = Field(default="", max_length=120)
    recommended_next_action: str = Field(default="needs_manual_review", max_length=80)
    matched_fields: list[ExternalCollectorMatchedField] = Field(default_factory=list)
    provenance: Literal["external_collector_handoff"] = "external_collector_handoff"
    stored_validation_not_fresh: Literal[True] = True
    collector_job_run: Literal[False] = False
    package_validation_performed: Literal[False] = False
    evidence_content_read: Literal[False] = False
    url_fetching: Literal[False] = False
    scraping: Literal[False] = False
    full_web_coverage: Literal[False] = False
    full_platform_coverage: Literal[False] = False
    human_review_required: Literal[True] = True


class ExternalCollectorDiscoveryResponse(BaseModel):
    query: str = Field(min_length=1, max_length=120)
    result_count: int = Field(ge=0, le=5)
    results: list[ExternalCollectorDiscoveryResult] = Field(default_factory=list, max_length=5)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "local_only": True,
            "metadata_only": True,
            "stored_validation_not_fresh": True,
            "collector_job_run": False,
            "package_validation_performed": False,
            "evidence_content_read": False,
            "url_fetching": False,
            "scraping": False,
            "full_web_coverage": False,
            "full_platform_coverage": False,
            "human_review_required": True,
            "evidence_write": False,
            "analysis_run": False,
        }
    )


class ExternalCollectorStatus(BaseModel):
    configured: bool = False
    exports_dir: str = ""
    exists: bool = False
    package_count: int = 0
    index_available: bool = False
    index_warning: str = ""
    message: str = ""
    suggested_env_var: str = "SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR"
    suggested_local_path: str = r"G:\AICODING\网页端任务二\exports\sentigraph-evidence-v1"
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "local_only": True,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "cookies_used": False,
            "real_llm_calls": False,
            "third_party_crawler_integrated": False,
            "secrets_exposed": False,
        }
    )


class ExternalCollectorPackageSummary(BaseModel):
    package_name: str
    package_path: str
    manifest_exists: bool = False
    validation_report_exists: bool = False
    case_id: str = ""
    case_title: str = ""
    exported_at: str | None = None
    evidence_count: int = 0
    source_count: int = 0
    comment_count: int = 0
    root_count: int = 0
    validation_status: str = "unknown"
    errors_count: int = 0
    warnings_count: int = 0
    package_role: str = ""
    demo_recommendation: str = ""
    recommended_for_sentigraph_demo: bool = False
    sample_quality_label: str = ""
    index_notes: str = ""
    index_available: bool = False
    index_warning: str = ""
    sample_labels: list[str] = Field(default_factory=list)
    coverage_warnings: list[str] = Field(default_factory=list)
    recommended_next_action: str = "needs_manual_review"


class ExternalCollectorPackageDetail(BaseModel):
    package_name: str
    package_path: str
    manifest_summary: dict[str, Any] = Field(default_factory=dict)
    validation_report_summary: dict[str, Any] = Field(default_factory=dict)
    expected_files: dict[str, bool] = Field(default_factory=dict)
    coverage_note_excerpt: str = ""
    readme_excerpt: str = ""
    privacy_summary: dict[str, Any] = Field(default_factory=dict)
    package_role: str = ""
    demo_recommendation: str = ""
    recommended_for_sentigraph_demo: bool = False
    sample_quality_label: str = ""
    index_notes: str = ""
    index_source: str = "folder scan fallback"
    index_available: bool = False
    index_warning: str = ""
    recommended_next_action: str = "needs_manual_review"
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "full_evidence_dump_returned": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "cookies_used": False,
            "real_llm_calls": False,
            "secrets_exposed": False,
        }
    )


class ExternalCollectorValidationResult(BaseModel):
    package_name: str
    status: ExternalCollectorValidationStatus = "fail"
    errors: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[dict[str, Any]] = Field(default_factory=list)
    counts: dict[str, int] = Field(default_factory=dict)
    privacy_status: str = "unknown"
    coverage_status: str = "unknown"
    recommended_next_action: str = "needs_manual_review"
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "local_only": True,
            "collector_jobs_run": False,
            "package_code_executed": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "cookies_used": False,
            "real_llm_calls": False,
            "secrets_exposed": False,
            "full_evidence_dump_returned": False,
        }
    )
