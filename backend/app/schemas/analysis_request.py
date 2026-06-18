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
