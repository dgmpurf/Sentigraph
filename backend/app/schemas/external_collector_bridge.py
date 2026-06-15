from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


ExternalCollectorValidationStatus = Literal["pass", "warn", "fail"]


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
