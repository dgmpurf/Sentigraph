from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


ProviderStatus = Literal[
    "draft",
    "queued",
    "accepted",
    "planning",
    "safety_check",
    "blocked_by_safety_gate",
    "needs_manual_snapshot",
    "running_safe",
    "cooldown",
    "partial_success",
    "package_generated",
    "validation_running",
    "validation_warn",
    "validation_failed",
    "package_ready",
    "canceled",
    "expired",
]

SafetyStatus = Literal["safe", "medium", "hold", "cooldown", "blocked"]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AnalysisRequestCaseSeed(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    keywords: list[str] = Field(default_factory=list)
    negative_keywords: list[str] = Field(default_factory=list)
    language: list[str] = Field(default_factory=lambda: ["zh-CN"])
    event_type: str = "public_opinion_event"
    sensitive_flags: list[str] = Field(default_factory=list)


class AnalysisRequestSamplingPlan(BaseModel):
    platforms: list[str] = Field(default_factory=list)
    time_range: dict[str, str] = Field(default_factory=dict)
    target_comment_count: int = Field(default=500, ge=0, le=100000)
    target_source_count: int = Field(default=30, ge=0, le=10000)
    max_runtime_minutes: int = Field(default=60, ge=1, le=1440)
    sample_strategy: str = "stratified_public_sample"


class AnalysisRequestSafetyPolicy(BaseModel):
    allow_live_collection: bool = False
    allow_saved_profile: bool = False
    allow_manual_snapshot: bool = True
    allow_official_api: bool = True
    allow_vendor_api: bool = True
    forbid_proxy_pool: bool = True
    forbid_captcha_bypass: bool = True
    forbid_private_content: bool = True


class AnalysisRequestPrivacyPolicy(BaseModel):
    remove_raw_author_id: bool = True
    remove_raw_author_name: bool = True
    remove_profile_url: bool = True
    remove_private_messages: bool = True
    minor_sensitive_mode: bool = True


class AnalysisRequestOutput(BaseModel):
    package_schema: str = "sentigraph_evidence_export_v1"
    package_slug: str = ""
    package_index_required: bool = True


class AnalysisRequestCreate(BaseModel):
    created_by: str = "sentigraph_local_user"
    case_seed: AnalysisRequestCaseSeed
    sampling_plan: AnalysisRequestSamplingPlan = Field(default_factory=AnalysisRequestSamplingPlan)
    safety_policy: AnalysisRequestSafetyPolicy = Field(default_factory=AnalysisRequestSafetyPolicy)
    privacy_policy: AnalysisRequestPrivacyPolicy = Field(default_factory=AnalysisRequestPrivacyPolicy)
    output: AnalysisRequestOutput = Field(default_factory=AnalysisRequestOutput)


class AnalysisRequestFile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_analysis_request_v1"] = Field(
        default="sentigraph_analysis_request_v1",
        alias="schema",
    )
    request_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_user"
    case_seed: AnalysisRequestCaseSeed
    sampling_plan: AnalysisRequestSamplingPlan = Field(default_factory=AnalysisRequestSamplingPlan)
    safety_policy: AnalysisRequestSafetyPolicy = Field(default_factory=AnalysisRequestSafetyPolicy)
    privacy_policy: AnalysisRequestPrivacyPolicy = Field(default_factory=AnalysisRequestPrivacyPolicy)
    output: AnalysisRequestOutput = Field(default_factory=AnalysisRequestOutput)
    sentigraph_metadata: dict[str, Any] = Field(
        default_factory=lambda: {
            "request_status": "draft",
            "provider_execution": "outside_sentigraph_core",
            "collector_jobs_run": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
        }
    )


class ProviderJobCounts(BaseModel):
    evidence: int = 0
    comments: int = 0
    sources: int = 0
    roots: int = 0


class ProviderJobValidation(BaseModel):
    status: Literal["passed", "warn", "failed"] = "warn"
    errors: int = 0
    warnings: int = 0


class ProviderJobCoverage(BaseModel):
    coverage_level: str = "selected_public_sample"
    not_full_web: bool = True
    not_full_platform: bool = True
    not_full_thread: bool = True


class ProviderJobPrivacy(BaseModel):
    raw_author_ids_removed: bool = True
    raw_author_names_removed: bool = True
    profile_urls_removed: bool = True
    private_messages_excluded: bool = True


class ProviderJobResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_provider_job_result_v1"] = Field(
        default="sentigraph_provider_job_result_v1",
        alias="schema",
    )
    request_id: str
    provider_job_id: str = ""
    provider_type: str = "private_collector"
    status: ProviderStatus = "draft"
    safety_status: SafetyStatus = "safe"
    package_path: str = ""
    package_name: str = ""
    package_role: str = ""
    package_index_path: str = ""
    counts: ProviderJobCounts = Field(default_factory=ProviderJobCounts)
    validation: ProviderJobValidation = Field(default_factory=ProviderJobValidation)
    coverage: ProviderJobCoverage = Field(default_factory=ProviderJobCoverage)
    privacy: ProviderJobPrivacy = Field(default_factory=ProviderJobPrivacy)
    skipped: list[Any] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class AnalysisRequestConfig(BaseModel):
    configured_by_env: bool = False
    root_exists: bool = False
    requests_dir_exists: bool = False
    results_dir_exists: bool = False
    request_count: int = 0
    result_count: int = 0
    root_label: str = "runtime/analysis_requests"
    suggested_env_var: str = "SENTIGRAPH_ANALYSIS_REQUESTS_DIR"
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "local_file_exchange_only": True,
            "provider_execution": False,
            "collector_jobs_run": False,
            "subprocess_provider_execution": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
        }
    )


class AnalysisRequestRecord(BaseModel):
    request_id: str
    request: AnalysisRequestFile
    request_status: str = "draft"
    request_file: str = ""
    result_file: str | None = None
    provider_result: ProviderJobResult | None = None
    result_warning: str | None = None
    provider_status: str | None = None
    safety_status: str | None = None
    package_name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "local_file_exchange_only": True,
            "provider_execution": False,
            "collector_jobs_run": False,
            "subprocess_provider_execution": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
        }
    )


class AnalysisRequestCancelResult(BaseModel):
    request_id: str
    status: str = "canceled"
    request: AnalysisRequestFile
    warning: str | None = None
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "local_only": True,
            "provider_cancel_called": False,
            "collector_jobs_run": False,
            "subprocess_provider_execution": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
        }
    )
