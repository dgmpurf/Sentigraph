from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


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

    @model_validator(mode="before")
    @classmethod
    def normalize_legacy_aliases(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        normalized = dict(data)
        if "evidence" not in normalized and "evidence_items" in normalized:
            normalized["evidence"] = normalized.get("evidence_items")
        if "roots" not in normalized and "root_content" in normalized:
            normalized["roots"] = normalized.get("root_content")
        return normalized


class ProviderJobValidation(BaseModel):
    status: Literal["not_run", "passed", "warn", "failed"] = "warn"
    errors: int = 0
    warnings: int = 0

    @model_validator(mode="before")
    @classmethod
    def normalize_legacy_aliases(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        normalized = dict(data)
        if "errors" not in normalized and "errors_count" in normalized:
            normalized["errors"] = normalized.get("errors_count")
        if "warnings" not in normalized and "warnings_count" in normalized:
            normalized["warnings"] = normalized.get("warnings_count")
        return normalized


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


class CaseDraftProviderSummary(BaseModel):
    provider_job_id: str = ""
    provider_type: str = "private_collector"
    status: str = ""
    safety_status: str = ""


class CaseDraftPackageReference(BaseModel):
    package_name: str = ""
    package_role: str = ""
    package_path: str = ""
    package_index_path: str = ""


class CaseDraftReadiness(BaseModel):
    state: str = "ready_for_manual_review"
    can_import_evidence: bool = False
    requires_human_review: bool = True
    reason: str = "Provider result is validation_warn/package_ready but evidence import is not automatic."


class CaseDraftHandoff(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_case_draft_handoff_v1"] = Field(
        default="sentigraph_case_draft_handoff_v1",
        alias="schema",
    )
    draft_id: str
    request_id: str
    created_at: datetime = Field(default_factory=utc_now)
    source: str = "analysis_request_provider_result"
    case_seed: AnalysisRequestCaseSeed
    provider_summary: CaseDraftProviderSummary = Field(default_factory=CaseDraftProviderSummary)
    package_reference: CaseDraftPackageReference = Field(default_factory=CaseDraftPackageReference)
    counts: ProviderJobCounts = Field(default_factory=ProviderJobCounts)
    validation: ProviderJobValidation = Field(default_factory=ProviderJobValidation)
    coverage: ProviderJobCoverage = Field(default_factory=ProviderJobCoverage)
    privacy: ProviderJobPrivacy = Field(default_factory=ProviderJobPrivacy)
    readiness: CaseDraftReadiness = Field(default_factory=CaseDraftReadiness)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "local_handoff_only": True,
            "evidence_rows_imported": False,
            "analysis_generated": False,
            "sandbox_fixture_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
        }
    )


class EvidenceImportProposedAction(BaseModel):
    mode: str = "manual_review_required"
    target: str = "future_evidence_layer"
    import_evidence_rows_now: bool = False
    create_case_now: bool = False
    run_analysis_now: bool = False
    generate_sandbox_now: bool = False
    generate_report_now: bool = False


class EvidenceImportDefaultPolicy(BaseModel):
    review_status: str = "review_needed"
    verification_status: str = "source_url_provided_unverified"
    trust_label: str = "medium_low"
    dedup_required: bool = True
    audit_required: bool = True


class EvidenceImportPlanReadiness(BaseModel):
    state: str = "ready_for_manual_import_review"
    can_import_now: bool = False
    requires_human_review: bool = True
    reason: str = "Import plan only. Evidence rows are not imported automatically."


class EvidenceImportPlan(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_evidence_import_plan_v1"] = Field(
        default="sentigraph_evidence_import_plan_v1",
        alias="schema",
    )
    plan_id: str
    draft_id: str
    request_id: str
    created_at: datetime = Field(default_factory=utc_now)
    source: str = "case_draft_handoff"
    package_reference: CaseDraftPackageReference = Field(default_factory=CaseDraftPackageReference)
    counts: ProviderJobCounts = Field(default_factory=ProviderJobCounts)
    validation: ProviderJobValidation = Field(default_factory=ProviderJobValidation)
    coverage: ProviderJobCoverage = Field(default_factory=ProviderJobCoverage)
    privacy: ProviderJobPrivacy = Field(default_factory=ProviderJobPrivacy)
    proposed_import: EvidenceImportProposedAction = Field(default_factory=EvidenceImportProposedAction)
    default_evidence_policy: EvidenceImportDefaultPolicy = Field(default_factory=EvidenceImportDefaultPolicy)
    manual_review_checklist: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    readiness: EvidenceImportPlanReadiness = Field(default_factory=EvidenceImportPlanReadiness)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "local_planning_only": True,
            "evidence_rows_imported": False,
            "production_case_created": False,
            "analysis_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "subprocess_provider_execution": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
        }
    )


class EvidenceImportDedupPreview(BaseModel):
    required: bool = True
    computed_now: bool = False
    reason: str = "Preview phase does not import or compute final dedup."


class EvidenceImportSamplePreviewPolicy(BaseModel):
    read_rows_now: bool = False
    max_safe_sample_rows_future: int = 20
    redact_author_fields: bool = True


class EvidenceImportPreviewReadiness(BaseModel):
    state: str = "ready_for_human_review"
    can_import_now: bool = False
    requires_review_decision: bool = True
    reason: str = "Import preview only. Evidence rows are not imported."


class EvidenceImportPreview(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_evidence_import_preview_v1"] = Field(
        default="sentigraph_evidence_import_preview_v1",
        alias="schema",
    )
    preview_id: str
    plan_id: str
    draft_id: str
    request_id: str
    created_at: datetime = Field(default_factory=utc_now)
    source: str = "evidence_import_plan"
    package_reference: CaseDraftPackageReference = Field(default_factory=CaseDraftPackageReference)
    metadata_summary: ProviderJobCounts = Field(default_factory=ProviderJobCounts)
    validation_summary: ProviderJobValidation = Field(default_factory=ProviderJobValidation)
    coverage_summary: ProviderJobCoverage = Field(default_factory=ProviderJobCoverage)
    privacy_summary: ProviderJobPrivacy = Field(default_factory=ProviderJobPrivacy)
    proposed_evidence_defaults: EvidenceImportDefaultPolicy = Field(default_factory=EvidenceImportDefaultPolicy)
    dedup_preview: EvidenceImportDedupPreview = Field(default_factory=EvidenceImportDedupPreview)
    sample_preview_policy: EvidenceImportSamplePreviewPolicy = Field(default_factory=EvidenceImportSamplePreviewPolicy)
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    readiness: EvidenceImportPreviewReadiness = Field(default_factory=EvidenceImportPreviewReadiness)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "metadata_only_preview": True,
            "evidence_rows_read": False,
            "evidence_rows_parsed": False,
            "evidence_rows_imported": False,
            "production_case_created": False,
            "analysis_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "subprocess_provider_execution": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
        }
    )


EvidenceImportDecisionValue = Literal[
    "approve_import",
    "reject_import",
    "request_more_source",
    "mark_limited_sample",
    "hold_for_privacy_review",
]

EvidenceImportTargetCaseMode = Literal["new_review_case", "existing_case", "reject_no_case"]


class EvidenceImportReviewChecklist(BaseModel):
    coverage_reviewed: bool = False
    validation_reviewed: bool = False
    privacy_reviewed: bool = False
    no_raw_author_identifiers: bool = False
    not_full_web_acknowledged: bool = False
    not_full_platform_acknowledged: bool = False
    not_full_thread_acknowledged: bool = False
    review_needed_default_acknowledged: bool = False
    trust_label_default_acknowledged: bool = False
    dedup_required_acknowledged: bool = False
    no_auto_analysis_acknowledged: bool = False
    no_auto_report_acknowledged: bool = False

    def missing_acknowledgements(self) -> list[str]:
        return [key for key, value in self.model_dump().items() if value is not True]


class EvidenceImportReviewDecisionCreate(BaseModel):
    reviewer_label: str = Field(..., min_length=1, max_length=120)
    decision: EvidenceImportDecisionValue
    target_case_mode: EvidenceImportTargetCaseMode = "new_review_case"
    target_case_id: str | None = None
    notes: str = Field(default="", max_length=3000)
    checklist: EvidenceImportReviewChecklist = Field(default_factory=EvidenceImportReviewChecklist)
    created_by: str = "sentigraph_local_ui"


class EvidenceImportReviewReadiness(BaseModel):
    state: str = "needs_more_source"
    can_create_import_job_now: bool = False
    requires_future_manual_import_phase: bool = True
    reason: str = "Review decision recorded. Evidence rows are not imported in Phase 6H."


class EvidenceImportReviewAudit(BaseModel):
    created_by: str = "sentigraph_local_ui"
    created_at: datetime = Field(default_factory=utc_now)
    source: str = "manual_review"


class EvidenceImportReviewDecision(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_evidence_import_review_decision_v1"] = Field(
        default="sentigraph_evidence_import_review_decision_v1",
        alias="schema",
    )
    decision_id: str
    preview_id: str
    plan_id: str
    draft_id: str
    request_id: str
    reviewer_label: str
    reviewed_at: datetime = Field(default_factory=utc_now)
    decision: EvidenceImportDecisionValue
    target_case_mode: EvidenceImportTargetCaseMode = "new_review_case"
    target_case_id: str | None = None
    notes: str = ""
    checklist: EvidenceImportReviewChecklist = Field(default_factory=EvidenceImportReviewChecklist)
    approved_defaults: EvidenceImportDefaultPolicy = Field(default_factory=EvidenceImportDefaultPolicy)
    readiness: EvidenceImportReviewReadiness = Field(default_factory=EvidenceImportReviewReadiness)
    boundary_notes: list[str] = Field(default_factory=list)
    audit: EvidenceImportReviewAudit = Field(default_factory=EvidenceImportReviewAudit)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "review_record_only": True,
            "evidence_rows_read": False,
            "evidence_rows_parsed": False,
            "evidence_rows_imported": False,
            "production_case_created": False,
            "analysis_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "subprocess_provider_execution": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
        }
    )


class ManualEvidenceImportJobCreate(BaseModel):
    decision_id: str | None = None
    target_case_mode: Literal["new_review_case", "existing_case"] | None = None
    target_case_id: str | None = None
    created_by: str = "sentigraph_local_ui"


class ManualEvidenceImportTargetCase(BaseModel):
    mode: Literal["new_review_case", "existing_case", "reject_no_case"] = "new_review_case"
    target_case_id: str | None = None
    create_case_now: bool = False


class ManualEvidenceImportDryRunResult(BaseModel):
    would_import_evidence_rows: bool = True
    import_evidence_rows_now: bool = False
    would_create_or_attach_case: bool = True
    create_case_now: bool = False
    would_run_dedup: bool = True
    run_dedup_now: bool = False
    would_create_review_queue_items: bool = True
    create_review_queue_now: bool = False
    would_run_analysis: bool = False
    run_analysis_now: bool = False
    would_generate_sandbox: bool = False
    generate_sandbox_now: bool = False
    would_generate_report: bool = False
    generate_report_now: bool = False


class ManualEvidenceImportPreflightChecks(BaseModel):
    approved_import_decision_present: bool = True
    coverage_acknowledged: bool = True
    validation_acknowledged: bool = True
    privacy_acknowledged: bool = True
    no_raw_author_identifiers_acknowledged: bool = True
    not_full_web_acknowledged: bool = True
    not_full_platform_acknowledged: bool = True
    not_full_thread_acknowledged: bool = True
    review_needed_default_acknowledged: bool = True
    trust_label_default_acknowledged: bool = True
    dedup_required_acknowledged: bool = True
    no_auto_analysis_acknowledged: bool = True
    no_auto_report_acknowledged: bool = True


class ManualEvidenceImportJobReadiness(BaseModel):
    state: str = "ready_for_future_manual_import_execution"
    can_execute_now: bool = False
    requires_separate_import_phase: bool = True
    reason: str = "Dry-run gate only. Evidence rows are not imported in Phase 6I."


class ManualEvidenceImportJob(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_manual_evidence_import_job_v1"] = Field(
        default="sentigraph_manual_evidence_import_job_v1",
        alias="schema",
    )
    job_id: str
    decision_id: str
    preview_id: str
    plan_id: str
    draft_id: str
    request_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    job_type: str = "manual_evidence_import"
    execution_mode: str = "dry_run_gate"
    status: str = "draft_not_executed"
    source: str = "human_review_decision"
    target_case: ManualEvidenceImportTargetCase = Field(default_factory=ManualEvidenceImportTargetCase)
    package_reference: CaseDraftPackageReference = Field(default_factory=CaseDraftPackageReference)
    metadata_summary: ProviderJobCounts = Field(default_factory=ProviderJobCounts)
    approved_defaults: EvidenceImportDefaultPolicy = Field(default_factory=EvidenceImportDefaultPolicy)
    dry_run_result: ManualEvidenceImportDryRunResult = Field(default_factory=ManualEvidenceImportDryRunResult)
    preflight_checks: ManualEvidenceImportPreflightChecks = Field(default_factory=ManualEvidenceImportPreflightChecks)
    readiness: ManualEvidenceImportJobReadiness = Field(default_factory=ManualEvidenceImportJobReadiness)
    blockers: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "dry_run_gate_only": True,
            "evidence_rows_read": False,
            "evidence_rows_parsed": False,
            "evidence_rows_imported": False,
            "production_case_created": False,
            "analysis_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "subprocess_provider_execution": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
        }
    )


class ManualEvidenceImportExecutionPreflightCreate(BaseModel):
    job_id: str | None = None
    created_by: str = "sentigraph_local_ui"


class ManualEvidenceImportPackageFileChecks(BaseModel):
    package_path_checked: bool = False
    package_path_exists: bool = False
    manifest_present: bool = False
    validation_report_present: bool = False
    coverage_note_present: bool = False
    readme_present: bool = False
    evidence_items_jsonl_present: bool = False
    evidence_items_csv_present: bool = False
    row_files_opened: bool = False
    row_files_parsed: bool = False


class ManualEvidenceImportTargetCasePreflight(BaseModel):
    mode: Literal["new_review_case", "existing_case"] = "new_review_case"
    target_case_id: str | None = None
    create_case_now: bool = False
    review_only_required: bool = True
    analysis_included_default: bool = False


class ManualEvidenceImportFutureRowReaderPlan(BaseModel):
    would_read_rows_in_future_phase: bool = True
    read_rows_now: bool = False
    streaming_required: bool = True
    max_rows_first_mvp: int = 100
    fail_closed_on_privacy_violation: bool = True


class ManualEvidenceImportFutureStagingPlan(BaseModel):
    would_stage_rows_in_future_phase: bool = True
    stage_rows_now: bool = False
    default_review_status: str = "review_needed"
    default_verification_status: str = "source_url_provided_unverified"
    default_trust_label: str = "medium_low"
    analysis_included: bool = False


class ManualEvidenceImportFutureGovernancePlan(BaseModel):
    dedup_required: bool = True
    dedup_run_now: bool = False
    review_queue_required: bool = True
    review_queue_created_now: bool = False
    audit_required: bool = True
    rollback_required: bool = True


class ManualEvidenceImportExecutionPreflightReadiness(BaseModel):
    state: str = "ready_for_future_manual_import_execution"
    can_execute_now: bool = False
    requires_separate_execution_phase: bool = True
    reason: str = "Preflight only. Evidence rows are not imported in Phase 6K."


class ManualEvidenceImportExecutionPreflight(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_manual_evidence_import_execution_preflight_v1"] = Field(
        default="sentigraph_manual_evidence_import_execution_preflight_v1",
        alias="schema",
    )
    preflight_id: str
    job_id: str
    decision_id: str
    preview_id: str
    plan_id: str
    draft_id: str
    request_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    source: str = "manual_evidence_import_job_dry_run"
    execution_mode: str = "preflight_only"
    status: Literal["preflight_passed", "preflight_warn", "preflight_blocked"] = "preflight_passed"
    package_reference: CaseDraftPackageReference = Field(default_factory=CaseDraftPackageReference)
    package_file_checks: ManualEvidenceImportPackageFileChecks = Field(default_factory=ManualEvidenceImportPackageFileChecks)
    metadata_summary: ProviderJobCounts = Field(default_factory=ProviderJobCounts)
    validation_summary: ProviderJobValidation = Field(default_factory=ProviderJobValidation)
    coverage_summary: ProviderJobCoverage = Field(default_factory=ProviderJobCoverage)
    privacy_summary: ProviderJobPrivacy = Field(default_factory=ProviderJobPrivacy)
    target_case_preflight: ManualEvidenceImportTargetCasePreflight = Field(default_factory=ManualEvidenceImportTargetCasePreflight)
    future_row_reader_plan: ManualEvidenceImportFutureRowReaderPlan = Field(default_factory=ManualEvidenceImportFutureRowReaderPlan)
    future_staging_plan: ManualEvidenceImportFutureStagingPlan = Field(default_factory=ManualEvidenceImportFutureStagingPlan)
    future_governance_plan: ManualEvidenceImportFutureGovernancePlan = Field(default_factory=ManualEvidenceImportFutureGovernancePlan)
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    readiness: ManualEvidenceImportExecutionPreflightReadiness = Field(default_factory=ManualEvidenceImportExecutionPreflightReadiness)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "preflight_only": True,
            "evidence_rows_opened": False,
            "evidence_rows_parsed": False,
            "evidence_rows_imported": False,
            "production_case_created": False,
            "evidence_layer_written": False,
            "review_queue_created": False,
            "dedup_run": False,
            "analysis_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "subprocess_provider_execution": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
        }
    )


class EvidenceRowReaderDryRunCreate(BaseModel):
    preflight_id: str | None = None
    fixture_name: str = "safe_evidence_items"
    fixture_mode: str = "synthetic_fixture"
    max_rows: int = Field(default=20, ge=1)
    row_source_path: str | None = None
    created_by: str = "sentigraph_local_ui"
    now_flags: dict[str, bool] = Field(default_factory=dict)


class EvidenceRowReaderFixturePolicy(BaseModel):
    synthetic_fixture_only: bool = True
    real_provider_package_allowed: bool = False
    external_collector_package_allowed: bool = False
    max_rows: int = 20
    redact_author_fields: bool = True


class EvidenceRowReaderRowSource(BaseModel):
    source_type: str = "synthetic_fixture"
    source_name: str = ""
    source_path: str = ""
    real_package_path_used: bool = False


class EvidenceRowReaderCounts(BaseModel):
    rows_seen: int = 0
    accepted_for_preview: int = 0
    quarantined: int = 0
    rejected: int = 0


class EvidenceRowReaderPrivacyScan(BaseModel):
    raw_author_id_detected: int = 0
    raw_author_name_detected: int = 0
    profile_url_detected: int = 0
    private_message_detected: int = 0
    secret_like_value_detected: int = 0
    privacy_stop_triggered: bool = False


class EvidenceRowReaderGovernanceDefaults(BaseModel):
    review_status: str = "review_needed"
    verification_status: str = "source_url_provided_unverified"
    trust_label: str = "medium_low"
    analysis_included: bool = False
    dedup_required_before_analysis: bool = True
    audit_required: bool = True


class EvidenceRowReaderCandidate(BaseModel):
    evidence_type: str = ""
    platform: str = ""
    source_url: str = ""
    title: str = ""
    body_text_preview: str = ""
    created_at: str = ""
    language: str = ""


class EvidenceRowReaderPrivacyCheck(BaseModel):
    passed: bool = True
    forbidden_fields_detected: list[str] = Field(default_factory=list)


class EvidenceRowReaderPreviewRow(BaseModel):
    row_index: int
    status: str = "accepted_for_preview"
    evidence_candidate: EvidenceRowReaderCandidate = Field(default_factory=EvidenceRowReaderCandidate)
    governance_defaults: EvidenceRowReaderGovernanceDefaults = Field(default_factory=EvidenceRowReaderGovernanceDefaults)
    privacy_check: EvidenceRowReaderPrivacyCheck = Field(default_factory=EvidenceRowReaderPrivacyCheck)


class EvidenceRowReaderSummaryItem(BaseModel):
    row_index: int
    status: str
    reason_code: str
    message: str
    forbidden_fields_detected: list[str] = Field(default_factory=list)


class EvidenceRowReaderNowFlags(BaseModel):
    import_evidence_rows_now: bool = False
    write_evidence_layer_now: bool = False
    create_case_now: bool = False
    create_review_queue_now: bool = False
    run_dedup_now: bool = False
    run_analysis_now: bool = False
    generate_sandbox_now: bool = False
    generate_report_now: bool = False


class EvidenceRowReaderReadiness(BaseModel):
    state: str = "ready_for_future_real_package_row_preview"
    can_import_now: bool = False
    requires_future_phase: bool = True
    reason: str = "Synthetic fixture dry-run only. No real provider package rows were read."


class EvidenceRowReaderDryRun(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_evidence_row_reader_dry_run_v1"] = Field(
        default="sentigraph_evidence_row_reader_dry_run_v1",
        alias="schema",
    )
    dry_run_id: str
    preflight_id: str
    job_id: str
    decision_id: str
    preview_id: str
    plan_id: str
    draft_id: str
    request_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    source: str = "execution_preflight"
    execution_mode: str = "synthetic_fixture_row_reader_dry_run"
    status: Literal["passed", "warn", "blocked"] = "passed"
    fixture_policy: EvidenceRowReaderFixturePolicy = Field(default_factory=EvidenceRowReaderFixturePolicy)
    row_source: EvidenceRowReaderRowSource = Field(default_factory=EvidenceRowReaderRowSource)
    counts: EvidenceRowReaderCounts = Field(default_factory=EvidenceRowReaderCounts)
    privacy_scan: EvidenceRowReaderPrivacyScan = Field(default_factory=EvidenceRowReaderPrivacyScan)
    redacted_preview_rows: list[EvidenceRowReaderPreviewRow] = Field(default_factory=list)
    quarantine_summary: list[EvidenceRowReaderSummaryItem] = Field(default_factory=list)
    rejection_summary: list[EvidenceRowReaderSummaryItem] = Field(default_factory=list)
    governance_defaults: EvidenceRowReaderGovernanceDefaults = Field(default_factory=EvidenceRowReaderGovernanceDefaults)
    now_flags: EvidenceRowReaderNowFlags = Field(default_factory=EvidenceRowReaderNowFlags)
    readiness: EvidenceRowReaderReadiness = Field(default_factory=EvidenceRowReaderReadiness)
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "synthetic_fixture_only": True,
            "real_provider_package_rows_parsed": False,
            "external_collector_package_rows_parsed": False,
            "evidence_rows_imported": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "review_queue_created": False,
            "dedup_run": False,
            "analysis_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "subprocess_provider_execution": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class RealPackageRowPreviewCreate(BaseModel):
    preflight_id: str | None = None
    max_rows: int = Field(default=10, ge=1)
    acknowledge_real_package_preview: bool = False
    acknowledge_no_import: bool = False
    acknowledge_preview_not_representative: bool = False
    acknowledge_privacy_stop: bool = False
    created_by: str = "sentigraph_local_ui"
    now_flags: dict[str, bool] = Field(default_factory=dict)


class RealPackageRowPreviewPackageReference(BaseModel):
    package_name: str = ""
    package_role: str = ""
    package_path: str = ""
    package_hash: str | None = None
    manifest_hash: str | None = None


class RealPackageRowPreviewLimits(BaseModel):
    max_rows: int = 10
    hard_max_rows: int = 20
    full_scan: bool = False
    import_rows: bool = False
    analysis: bool = False
    report: bool = False


class RealPackageRowPreviewRows(BaseModel):
    rows_seen: int = 0
    accepted_for_preview: int = 0
    quarantined: int = 0
    rejected: int = 0
    privacy_stop_at_row: int | None = None


class RealPackageRowPreviewPrivacyScan(EvidenceRowReaderPrivacyScan):
    email_detected: int = 0
    phone_detected: int = 0


class RealPackageRowPreviewCandidate(BaseModel):
    evidence_type: str = ""
    platform: str = ""
    source_url: str = ""
    title_preview: str = ""
    body_text_preview: str = ""
    created_at: str = ""
    language: str = ""
    counts: dict[str, int | float] = Field(default_factory=dict)


class RealPackageRowPreviewPrivacyCheck(BaseModel):
    passed: bool = True
    forbidden_fields_detected: list[str] = Field(default_factory=list)


class RealPackageRowPreviewRow(BaseModel):
    row_index: int
    status: str = "accepted_for_preview"
    evidence_candidate: RealPackageRowPreviewCandidate = Field(default_factory=RealPackageRowPreviewCandidate)
    governance_defaults: EvidenceRowReaderGovernanceDefaults = Field(default_factory=EvidenceRowReaderGovernanceDefaults)
    privacy_check: RealPackageRowPreviewPrivacyCheck = Field(default_factory=RealPackageRowPreviewPrivacyCheck)


class RealPackageRowPreviewReadiness(BaseModel):
    state: str = "ready_for_future_staging_import_design"
    can_import_now: bool = False
    requires_future_phase: bool = True
    reason: str = "Real package row preview only. Evidence rows are not imported."


class RealPackageRowPreview(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_real_package_row_preview_v1"] = Field(
        default="sentigraph_real_package_row_preview_v1",
        alias="schema",
    )
    preview_run_id: str
    preflight_id: str
    import_job_id: str
    decision_id: str
    preview_id: str
    plan_id: str
    draft_id: str
    request_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    execution_mode: str = "real_package_row_preview_only"
    status: Literal["passed", "warn", "blocked", "privacy_stop"] = "passed"
    package_reference: RealPackageRowPreviewPackageReference = Field(default_factory=RealPackageRowPreviewPackageReference)
    limits: RealPackageRowPreviewLimits = Field(default_factory=RealPackageRowPreviewLimits)
    rows: RealPackageRowPreviewRows = Field(default_factory=RealPackageRowPreviewRows)
    privacy_scan: RealPackageRowPreviewPrivacyScan = Field(default_factory=RealPackageRowPreviewPrivacyScan)
    redacted_preview_rows: list[RealPackageRowPreviewRow] = Field(default_factory=list)
    quarantine_summary: list[EvidenceRowReaderSummaryItem] = Field(default_factory=list)
    rejection_summary: list[EvidenceRowReaderSummaryItem] = Field(default_factory=list)
    governance_defaults: EvidenceRowReaderGovernanceDefaults = Field(default_factory=EvidenceRowReaderGovernanceDefaults)
    now_flags: EvidenceRowReaderNowFlags = Field(default_factory=EvidenceRowReaderNowFlags)
    readiness: RealPackageRowPreviewReadiness = Field(default_factory=RealPackageRowPreviewReadiness)
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "real_package_row_preview_only": True,
            "full_scan": False,
            "evidence_rows_imported": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "review_queue_created": False,
            "dedup_run": False,
            "analysis_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "subprocess_provider_execution": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class ReviewOnlyCaseCreate(BaseModel):
    source_preview_run_id: str | None = None
    target_case_mode: str = "new_review_case"
    target_case_id: str | None = None
    created_by: str = "sentigraph_local_ui"
    analysis_included: bool = False
    production_case_created: bool = False
    evidence_rows_imported: bool = False
    evidence_layer_written: bool = False
    review_queue_created: bool = False
    dedup_run: bool = False
    analysis_run: bool = False
    report_allowed: bool = False
    sandbox_allowed: bool = False
    public_visible: bool = False
    strategy_lab_allowed: bool = False


class ReviewOnlyCaseSourcePreviewSummary(BaseModel):
    preview_run_id: str = ""
    status: str = ""
    rows_seen: int = 0
    accepted_for_preview: int = 0
    quarantined: int = 0
    rejected: int = 0
    privacy_stop_triggered: bool = False


class ReviewOnlyCaseGovernanceDefaults(BaseModel):
    review_status: str = "review_needed"
    verification_status: str = "source_url_provided_unverified"
    trust_label: str = "medium_low"
    dedup_required: bool = True
    audit_required: bool = True
    analysis_included: bool = False


class ReviewOnlyCaseTargetReference(BaseModel):
    mode: Literal["new_review_case", "existing_case_review_wrapper"] = "new_review_case"
    target_case_id: str | None = None
    attach_to_production_case_now: bool = False


class ReviewOnlyCaseReadiness(BaseModel):
    state: str = "review_only_case_created"
    can_import_rows_now: bool = False
    can_run_analysis_now: bool = False
    can_generate_report_now: bool = False
    requires_future_staging_import_phase: bool = True
    reason: str = "Review-only case container only. No evidence rows are imported in Phase 6P."


class ReviewOnlyCaseAudit(BaseModel):
    created_by: str = "sentigraph_local_ui"
    created_at: datetime = Field(default_factory=utc_now)
    source: str = "limited_real_package_row_preview"


class ReviewOnlyCase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_review_only_case_v1"] = Field(
        default="sentigraph_review_only_case_v1",
        alias="schema",
    )
    review_case_id: str
    request_id: str
    source_import_job_id: str
    source_preview_run_id: str
    source_preflight_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    status: Literal["draft", "staging_pending", "privacy_hold", "rejected", "archived"] = "staging_pending"
    visibility: str = "internal_review_only"
    analysis_included: bool = False
    public_visible: bool = False
    report_allowed: bool = False
    sandbox_allowed: bool = False
    strategy_lab_allowed: bool = False
    production_case_created: bool = False
    evidence_rows_imported: bool = False
    evidence_layer_written: bool = False
    review_queue_created: bool = False
    dedup_run: bool = False
    analysis_run: bool = False
    package_reference: RealPackageRowPreviewPackageReference = Field(default_factory=RealPackageRowPreviewPackageReference)
    source_preview_summary: ReviewOnlyCaseSourcePreviewSummary = Field(default_factory=ReviewOnlyCaseSourcePreviewSummary)
    coverage: ProviderJobCoverage = Field(default_factory=ProviderJobCoverage)
    governance_defaults: ReviewOnlyCaseGovernanceDefaults = Field(default_factory=ReviewOnlyCaseGovernanceDefaults)
    target_case_reference: ReviewOnlyCaseTargetReference = Field(default_factory=ReviewOnlyCaseTargetReference)
    allowed_actions: list[str] = Field(default_factory=list)
    blocked_actions: list[str] = Field(default_factory=list)
    promotion_requirements: list[str] = Field(default_factory=list)
    readiness: ReviewOnlyCaseReadiness = Field(default_factory=ReviewOnlyCaseReadiness)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    audit: ReviewOnlyCaseAudit = Field(default_factory=ReviewOnlyCaseAudit)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "review_only_case_container_only": True,
            "evidence_rows_imported": False,
            "evidence_rows_parsed": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "review_queue_created": False,
            "dedup_run": False,
            "analysis_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "subprocess_provider_execution": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class ReviewOnlyCaseStagingImportCreate(BaseModel):
    review_case_id: str | None = None
    preview_run_id: str | None = None
    created_by: str = "sentigraph_local_ui"
    acknowledge_review_only_staging: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_no_analysis: bool = False
    acknowledge_no_report: bool = False
    package_path: str | None = None
    target_production_case_id: str | None = None
    production_case_created: bool = False
    evidence_rows_imported: bool = False
    evidence_layer_written: bool = False
    review_queue_created: bool = False
    dedup_run: bool = False
    analysis_run: bool = False
    report_generated: bool = False
    sandbox_generated: bool = False
    public_event_generated: bool = False
    write_evidence_layer_now: bool = False
    run_analysis_now: bool = False


class ReviewOnlyCaseStagingImportLimits(BaseModel):
    source: str = "limited_real_package_row_preview"
    max_rows_from_preview: int = 20
    full_scan: bool = False
    read_package_rows_now: bool = False
    analysis_inclusion: bool = False
    public_visibility: bool = False


class ReviewOnlyCaseStagingImportCounts(BaseModel):
    preview_rows_seen: int = 0
    accepted_for_staging: int = 0
    quarantined_from_staging: int = 0
    rejected_from_staging: int = 0
    privacy_stop: bool = False


class ReviewOnlyStagedGovernance(BaseModel):
    review_status: str = "review_needed"
    verification_status: str = "source_url_provided_unverified"
    trust_label: str = "medium_low"
    analysis_included: bool = False
    public_visible: bool = False
    report_visible: bool = False
    sandbox_visible: bool = False
    dedup_required: bool = True
    audit_required: bool = True


class ReviewOnlyCaseStagingTarget(BaseModel):
    target_type: str = "review_only_case_staging"
    review_case_id: str = ""
    production_case_id: str | None = None
    production_case_created: bool = False
    evidence_layer_written: bool = False


class ReviewOnlyCaseStagingRollback(BaseModel):
    rollback_available: bool = True
    rollback_id: str = ""
    rollback_required_before_analysis: bool = True


class ReviewOnlyCaseStagingReadiness(BaseModel):
    state: str = "staged_for_review_only"
    can_run_analysis_now: bool = False
    can_generate_report_now: bool = False
    requires_review_queue_phase: bool = True
    reason: str = "Rows are staged as review-only candidates from redacted preview rows only."


class ReviewOnlyCaseStagingImport(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_review_only_case_staging_import_v1"] = Field(
        default="sentigraph_review_only_case_staging_import_v1",
        alias="schema",
    )
    staging_import_id: str
    review_case_id: str
    request_id: str
    package_name: str
    source_preview_run_id: str
    source_import_job_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    execution_mode: str = "review_only_redacted_preview_staging"
    status: Literal["completed", "partial", "blocked", "privacy_stop"] = "completed"
    limits: ReviewOnlyCaseStagingImportLimits = Field(default_factory=ReviewOnlyCaseStagingImportLimits)
    counts: ReviewOnlyCaseStagingImportCounts = Field(default_factory=ReviewOnlyCaseStagingImportCounts)
    default_governance: ReviewOnlyStagedGovernance = Field(default_factory=ReviewOnlyStagedGovernance)
    target: ReviewOnlyCaseStagingTarget = Field(default_factory=ReviewOnlyCaseStagingTarget)
    rollback: ReviewOnlyCaseStagingRollback = Field(default_factory=ReviewOnlyCaseStagingRollback)
    readiness: ReviewOnlyCaseStagingReadiness = Field(default_factory=ReviewOnlyCaseStagingReadiness)
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "review_only_redacted_preview_staging": True,
            "original_package_rows_re_read": False,
            "evidence_rows_imported": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "review_queue_created": False,
            "dedup_run": False,
            "analysis_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "subprocess_provider_execution": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class StagedEvidenceCandidatePreview(BaseModel):
    evidence_type: str = ""
    platform: str = ""
    source_url: str = ""
    title_preview: str = ""
    body_text_preview: str = ""
    created_at: str = ""
    language: str = ""
    safe_counts: dict[str, int | float] = Field(default_factory=dict)


class StagedEvidenceCandidatePrivacy(BaseModel):
    from_redacted_preview: bool = True
    raw_author_id_present: bool = False
    raw_author_name_present: bool = False
    profile_url_present: bool = False
    private_message_present: bool = False
    passed: bool = True


class StagedEvidenceCandidateDedup(BaseModel):
    computed_now: bool = False
    required_before_analysis: bool = True
    content_hash: str | None = None


class StagedEvidenceCandidateAudit(BaseModel):
    source: str = "review_only_staging_import"
    staging_import_id: str = ""
    created_at: datetime = Field(default_factory=utc_now)


class StagedEvidenceCandidate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_staged_evidence_candidate_v1"] = Field(
        default="sentigraph_staged_evidence_candidate_v1",
        alias="schema",
    )
    staging_id: str
    staging_import_id: str
    review_case_id: str
    request_id: str
    package_name: str
    source_preview_run_id: str
    source_preview_row_index: int
    created_at: datetime = Field(default_factory=utc_now)
    row_status: Literal["accepted_for_review"] = "accepted_for_review"
    evidence_candidate: StagedEvidenceCandidatePreview = Field(default_factory=StagedEvidenceCandidatePreview)
    governance: ReviewOnlyStagedGovernance = Field(default_factory=ReviewOnlyStagedGovernance)
    privacy: StagedEvidenceCandidatePrivacy = Field(default_factory=StagedEvidenceCandidatePrivacy)
    dedup: StagedEvidenceCandidateDedup = Field(default_factory=StagedEvidenceCandidateDedup)
    audit: StagedEvidenceCandidateAudit = Field(default_factory=StagedEvidenceCandidateAudit)


class StagedEvidenceCandidateBatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_staged_evidence_candidate_batch_v1"] = Field(
        default="sentigraph_staged_evidence_candidate_batch_v1",
        alias="schema",
    )
    staging_import_id: str
    review_case_id: str
    request_id: str
    created_at: datetime = Field(default_factory=utc_now)
    candidates: list[StagedEvidenceCandidate] = Field(default_factory=list)


class ReviewQueueInitializationCreate(BaseModel):
    review_case_id: str | None = None
    staging_import_id: str | None = None
    created_by: str = "sentigraph_local_ui"
    acknowledge_review_only_queue: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_no_dedup: bool = False
    acknowledge_no_analysis: bool = False
    acknowledge_no_report: bool = False
    package_path: str | None = None
    target_production_case_id: str | None = None
    production_case_id: str | None = None
    production_case_created: bool = False
    evidence_layer_written: bool = False
    production_review_queue_created: bool = False
    analysis_included: bool = False
    dedup_run: bool = False
    analysis_run: bool = False
    report_generated: bool = False
    sandbox_generated: bool = False
    public_event_generated: bool = False
    write_evidence_layer_now: bool = False
    run_analysis_now: bool = False


class ReviewQueueInitializationSource(BaseModel):
    source_type: str = "staged_evidence_candidates"
    staging_import_id: str = ""
    candidate_batch_schema: str = "sentigraph_staged_evidence_candidate_batch_v1"


class ReviewQueueInitializationCounts(BaseModel):
    staged_candidates_seen: int = 0
    queue_items_created: int = 0
    excluded_candidates: int = 0
    privacy_hold_items: int = 0


class ReviewQueueDefaults(BaseModel):
    queue_status: str = "review_needed"
    review_status: str = "review_needed"
    verification_status: str = "source_url_provided_unverified"
    trust_label: str = "medium_low"
    analysis_included: bool = False
    public_visible: bool = False
    report_visible: bool = False
    sandbox_visible: bool = False
    dedup_required: bool = True
    audit_required: bool = True


class ReviewQueueInitializationTarget(BaseModel):
    target_type: str = "review_only_case_queue"
    review_case_id: str = ""
    production_case_id: str | None = None
    production_case_created: bool = False
    evidence_layer_written: bool = False
    production_review_queue_created: bool = False


class ReviewQueueInitializationReadiness(BaseModel):
    state: str = "review_queue_initialized"
    can_run_analysis_now: bool = False
    can_generate_report_now: bool = False
    requires_review_actions_phase: bool = True
    requires_dedup_phase: bool = True
    reason: str = "Review-only queue items created for human governance only."


class ReviewQueueInitialization(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_review_queue_initialization_v1"] = Field(
        default="sentigraph_review_queue_initialization_v1",
        alias="schema",
    )
    queue_init_id: str
    review_case_id: str
    staging_import_id: str
    request_id: str
    package_name: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    execution_mode: str = "review_only_queue_initialization"
    status: Literal["completed", "partial", "blocked", "privacy_stop"] = "completed"
    source: ReviewQueueInitializationSource = Field(default_factory=ReviewQueueInitializationSource)
    counts: ReviewQueueInitializationCounts = Field(default_factory=ReviewQueueInitializationCounts)
    defaults: ReviewQueueDefaults = Field(default_factory=ReviewQueueDefaults)
    target: ReviewQueueInitializationTarget = Field(default_factory=ReviewQueueInitializationTarget)
    readiness: ReviewQueueInitializationReadiness = Field(default_factory=ReviewQueueInitializationReadiness)
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "review_only_queue_initialization": True,
            "source_staged_candidates_only": True,
            "original_package_rows_re_read": False,
            "evidence_rows_imported": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "dedup_run": False,
            "analysis_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "subprocess_provider_execution": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class ReviewQueueItemDedup(BaseModel):
    dedup_status: str = "not_run"
    duplicate_group_id: str | None = None
    duplicate_count: int = 1
    may_amplify_risk: bool = False


class ReviewQueueItemAudit(BaseModel):
    source: str = "review_queue_initialization"
    queue_init_id: str = ""
    created_at: datetime = Field(default_factory=utc_now)


class ReviewQueueItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_review_queue_item_v1"] = Field(
        default="sentigraph_review_queue_item_v1",
        alias="schema",
    )
    review_item_id: str
    queue_init_id: str
    review_case_id: str
    staging_import_id: str
    staging_id: str
    request_id: str
    package_name: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    queue_status: Literal[
        "review_needed",
        "approved",
        "rejected",
        "marked_weak",
        "needs_more_source",
        "duplicate_merged",
        "privacy_hold",
    ] = "review_needed"
    evidence_candidate: StagedEvidenceCandidatePreview = Field(default_factory=StagedEvidenceCandidatePreview)
    governance: ReviewOnlyStagedGovernance = Field(default_factory=ReviewOnlyStagedGovernance)
    privacy: StagedEvidenceCandidatePrivacy = Field(default_factory=StagedEvidenceCandidatePrivacy)
    dedup: ReviewQueueItemDedup = Field(default_factory=ReviewQueueItemDedup)
    audit: ReviewQueueItemAudit = Field(default_factory=ReviewQueueItemAudit)


class ReviewQueueItemBatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_review_queue_item_batch_v1"] = Field(
        default="sentigraph_review_queue_item_batch_v1",
        alias="schema",
    )
    queue_init_id: str
    review_case_id: str
    staging_import_id: str
    request_id: str
    created_at: datetime = Field(default_factory=utc_now)
    items: list[ReviewQueueItem] = Field(default_factory=list)


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
