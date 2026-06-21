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


ReviewQueueActionName = Literal[
    "approve",
    "reject",
    "mark_weak",
    "request_more_source",
    "merge_duplicate",
    "hold_for_privacy_review",
    "reset_review",
]


class ReviewQueueActionRequest(BaseModel):
    action: ReviewQueueActionName
    reviewer_label: str = ""
    note: str = ""
    duplicate_group_id: str | None = None
    duplicate_of_review_item_id: str | None = None
    acknowledge_review_only_action: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_no_dedup: bool = False
    acknowledge_no_analysis: bool = False
    acknowledge_no_report: bool = False
    production_case_id: str | None = None
    target_production_case_id: str | None = None
    trust_label: str | None = None
    verification_status: str | None = None
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
    run_dedup_now: bool = False
    run_analysis_now: bool = False


class ReviewQueueActionAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_review_queue_action_audit_v1"] = Field(
        default="sentigraph_review_queue_action_audit_v1",
        alias="schema",
    )
    audit_id: str
    review_item_id: str
    queue_init_id: str
    review_case_id: str
    staging_import_id: str
    request_id: str
    previous_status: str
    new_status: str
    action: ReviewQueueActionName
    reviewer_label: str
    reviewed_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    analysis_effect: Literal["still_excluded", "eligible_for_future_dedup", "blocked"] = "still_excluded"
    trust_label_before: str = "medium_low"
    trust_label_after: str = "medium_low"
    verification_status_before: str = "source_url_provided_unverified"
    verification_status_after: str = "source_url_provided_unverified"
    dedup_effect: Literal["not_run", "duplicate_candidate_marked"] = "not_run"
    downstream_blockers: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "review_only_action": True,
            "no_ai_verification": True,
            "no_url_fetch": True,
            "no_secret_exposed": True,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "dedup_run": False,
            "analysis_generated": False,
            "report_generated": False,
            "sandbox_generated": False,
            "public_event_generated": False,
            "real_api_calls": False,
            "scraping": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class ReviewQueueActionResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_review_queue_action_result_v1"] = Field(
        default="sentigraph_review_queue_action_result_v1",
        alias="schema",
    )
    action_id: str
    audit_id: str
    review_item_id: str
    queue_init_id: str
    review_case_id: str
    request_id: str
    action: ReviewQueueActionName
    previous_status: str
    new_status: str
    updated_item: ReviewQueueItem
    audit_record: ReviewQueueActionAudit
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
            "create_production_review_queue_now": False,
            "run_dedup_now": False,
            "run_analysis_now": False,
            "generate_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
        }
    )
    readiness: dict[str, bool | str] = Field(
        default_factory=lambda: {
            "state": "review_action_recorded",
            "can_run_analysis_now": False,
            "can_generate_report_now": False,
            "requires_completion_gate": True,
            "requires_dedup_phase": True,
        }
    )


class ReviewQueueCompletionGateRequest(BaseModel):
    queue_init_id: str | None = None
    review_case_id: str | None = None
    minimum_reviewed_ratio: float = Field(default=1.0, ge=0.0, le=1.0)
    allow_deferred_items: bool = False
    created_by: str = "sentigraph_local_ui"
    acknowledge_completion_is_not_dedup: bool = False
    acknowledge_completion_is_not_analysis: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_no_report: bool = False
    production_case_id: str | None = None
    target_production_case_id: str | None = None
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
    create_production_case_now: bool = False
    create_production_review_queue_now: bool = False
    run_dedup_now: bool = False
    run_analysis_now: bool = False
    generate_report_now: bool = False
    generate_sandbox_now: bool = False
    generate_public_event_now: bool = False


class ReviewQueueCompletionGateCounts(BaseModel):
    total_items: int = 0
    review_needed: int = 0
    approved: int = 0
    rejected: int = 0
    marked_weak: int = 0
    needs_more_source: int = 0
    duplicate_merged: int = 0
    privacy_hold: int = 0
    reviewed_count: int = 0
    reviewed_ratio: float = 0.0


class ReviewQueueCompletionGateAuditSummary(BaseModel):
    items_with_audit: int = 0
    items_missing_audit: int = 0
    latest_action_at: datetime | None = None
    reviewer_labels: list[str] = Field(default_factory=list)


class ReviewQueueCompletionGateDownstreamEligibility(BaseModel):
    eligible_for_future_dedup_preview: bool = False
    can_run_dedup_now: bool = False
    can_run_analysis_now: bool = False
    can_generate_report_now: bool = False
    can_generate_sandbox_now: bool = False
    can_create_public_event_now: bool = False


class ReviewQueueCompletionGate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_review_queue_completion_gate_v1"] = Field(
        default="sentigraph_review_queue_completion_gate_v1",
        alias="schema",
    )
    completion_gate_id: str
    request_id: str
    review_case_id: str
    queue_init_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    status: Literal[
        "complete_enough_for_future_dedup_preview",
        "incomplete",
        "blocked",
        "privacy_hold",
    ] = "incomplete"
    counts: ReviewQueueCompletionGateCounts = Field(default_factory=ReviewQueueCompletionGateCounts)
    audit_summary: ReviewQueueCompletionGateAuditSummary = Field(default_factory=ReviewQueueCompletionGateAuditSummary)
    downstream_eligibility: ReviewQueueCompletionGateDownstreamEligibility = Field(
        default_factory=ReviewQueueCompletionGateDownstreamEligibility
    )
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
            "create_production_review_queue_now": False,
            "run_dedup_now": False,
            "run_analysis_now": False,
            "generate_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
        }
    )
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "review_queue_completion_gate_only": True,
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


class DedupPreviewRequest(BaseModel):
    review_case_id: str | None = None
    queue_init_id: str | None = None
    completion_gate_id: str | None = None
    include_marked_weak: bool = True
    include_duplicate_merged: bool = True
    created_by: str = "sentigraph_local_ui"
    acknowledge_dedup_preview_only: bool = False
    acknowledge_no_production_dedup: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_analysis: bool = False
    acknowledge_no_report: bool = False
    production_case_id: str | None = None
    target_production_case_id: str | None = None
    evidence_layer_written: bool = False
    production_case_created: bool = False
    production_review_queue_created: bool = False
    production_dedup_run: bool = False
    analysis_included: bool = False
    analysis_run: bool = False
    report_generated: bool = False
    sandbox_generated: bool = False
    public_event_generated: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    create_production_review_queue_now: bool = False
    run_dedup_now: bool = False
    run_analysis_now: bool = False
    generate_report_now: bool = False
    generate_sandbox_now: bool = False
    generate_public_event_now: bool = False


class DedupPreviewInputScope(BaseModel):
    source: Literal["review_only_queue_items"] = "review_only_queue_items"
    include_statuses: list[str] = Field(default_factory=lambda: ["approved", "marked_weak", "duplicate_merged"])
    exclude_statuses: list[str] = Field(default_factory=lambda: ["rejected", "needs_more_source", "privacy_hold", "review_needed"])
    analysis_included: bool = False


class DedupPreviewCounts(BaseModel):
    items_seen: int = 0
    items_eligible_for_preview: int = 0
    items_excluded: int = 0
    duplicate_group_candidates: int = 0
    unique_candidate_count: int = 0


class DedupPreviewSignals(BaseModel):
    exact_url_match: bool = True
    normalized_url_match: bool = True
    content_preview_hash_match: bool = True
    lineage_match: bool = True
    reviewer_merge_hint: bool = True
    semantic_llm_match: bool = False


class DedupPreviewPrivacyScan(BaseModel):
    raw_identifier_found: bool = False
    secret_like_found: bool = False
    privacy_stop: bool = False


class DedupPreviewReadiness(BaseModel):
    state: Literal["dedup_preview_ready", "blocked", "privacy_hold", "incomplete"] = "incomplete"
    can_run_dedup_now: bool = False
    can_run_analysis_now: bool = False
    requires_human_dedup_confirmation: bool = True
    requires_analysis_promotion_gate: bool = True


class DedupPreviewExcludedItem(BaseModel):
    review_item_id: str
    reason: str
    queue_status: str = ""
    review_status: str = ""


class DedupGroupCandidate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_dedup_group_candidate_v1"] = Field(
        default="sentigraph_dedup_group_candidate_v1",
        alias="schema",
    )
    group_candidate_id: str
    review_case_id: str
    queue_init_id: str
    dedup_preview_id: str
    reason: Literal["exact_url_match", "normalized_url_match", "content_preview_hash_match", "lineage_match", "reviewer_merge_hint", "mixed"]
    confidence: Literal["high", "medium", "low"] = "medium"
    group_status: Literal[
        "review_needed",
        "confirmed",
        "split",
        "representative_changed",
        "marked_weak",
        "rejected",
        "needs_more_source",
        "privacy_hold",
    ] = "review_needed"
    item_ids: list[str] = Field(default_factory=list)
    representative_item_id: str = ""
    split_item_ids: list[str] = Field(default_factory=list)
    duplicate_count_preview: int = 0
    may_amplify_risk: bool = False
    human_confirmation_required: bool = True
    analysis_effect: Literal["preview_only_no_analysis_effect", "blocked", "eligible_for_future_promotion_gate"] = (
        "preview_only_no_analysis_effect"
    )
    notes: list[str] = Field(default_factory=list)


DedupGroupReviewActionName = Literal[
    "confirm_group",
    "split_group",
    "change_representative",
    "mark_group_weak",
    "reject_group",
    "request_more_source",
    "hold_group_for_privacy",
    "reset_group_review",
]


class DedupGroupReviewActionRequest(BaseModel):
    action: DedupGroupReviewActionName
    reviewer_label: str = ""
    note: str = ""
    representative_item_id: str | None = None
    split_item_ids: list[str] = Field(default_factory=list)
    target_group_candidate_id: str | None = None
    acknowledge_review_only_group_action: bool = False
    acknowledge_no_production_dedup: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_analysis: bool = False
    acknowledge_no_report: bool = False
    production_case_id: str | None = None
    target_production_case_id: str | None = None
    trust_label: str | None = None
    verification_status: str | None = None
    evidence_layer_written: bool = False
    production_case_created: bool = False
    production_review_queue_created: bool = False
    production_dedup_run: bool = False
    analysis_included: bool = False
    analysis_run: bool = False
    report_generated: bool = False
    sandbox_generated: bool = False
    public_event_generated: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    create_production_review_queue_now: bool = False
    run_production_dedup_now: bool = False
    run_dedup_now: bool = False
    run_analysis_now: bool = False
    generate_report_now: bool = False
    generate_sandbox_now: bool = False
    generate_public_event_now: bool = False


class DedupGroupReviewAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_dedup_group_review_audit_v1"] = Field(
        default="sentigraph_dedup_group_review_audit_v1",
        alias="schema",
    )
    audit_id: str
    request_id: str
    review_case_id: str
    dedup_preview_id: str
    group_candidate_id: str
    previous_group_status: str
    new_group_status: str
    action: DedupGroupReviewActionName
    reviewer_label: str
    reviewed_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    affected_item_ids: list[str] = Field(default_factory=list)
    representative_before: str = ""
    representative_after: str = ""
    split_item_ids: list[str] = Field(default_factory=list)
    analysis_effect: Literal["preview_only_no_analysis_effect", "blocked", "eligible_for_future_promotion_gate"] = (
        "preview_only_no_analysis_effect"
    )
    dedup_effect: Literal[
        "review_only_group_confirmed",
        "review_only_group_split",
        "review_only_group_blocked",
        "review_only_representative_changed",
        "review_only_group_reset",
        "not_run",
    ] = "not_run"
    trust_label_effect: Literal["no_upgrade", "weak_warning", "rejected"] = "no_upgrade"
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
            "create_production_review_queue_now": False,
            "run_production_dedup_now": False,
            "run_analysis_now": False,
            "generate_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
        }
    )
    boundary_notes: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "review_only_group_action": True,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "production_dedup_run": False,
            "analysis_generated": False,
            "report_generated": False,
            "sandbox_generated": False,
            "public_event_page_generated": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class DedupGroupReviewActionResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_dedup_group_review_action_result_v1"] = Field(
        default="sentigraph_dedup_group_review_action_result_v1",
        alias="schema",
    )
    action_id: str
    audit_id: str
    request_id: str
    review_case_id: str
    dedup_preview_id: str
    group_candidate_id: str
    action: DedupGroupReviewActionName
    previous_group_status: str
    new_group_status: str
    updated_group: DedupGroupCandidate
    audit_record: DedupGroupReviewAudit
    readiness: dict[str, bool | str] = Field(
        default_factory=lambda: {
            "state": "group_review_action_recorded",
            "can_run_production_dedup_now": False,
            "can_run_analysis_now": False,
            "requires_group_review_completion_gate": True,
            "requires_analysis_promotion_gate": True,
        }
    )


class DedupPreview(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_dedup_preview_v1"] = Field(
        default="sentigraph_dedup_preview_v1",
        alias="schema",
    )
    dedup_preview_id: str
    request_id: str
    review_case_id: str
    queue_init_id: str
    completion_gate_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    execution_mode: Literal["review_only_dedup_preview"] = "review_only_dedup_preview"
    status: Literal["preview_ready", "incomplete", "blocked", "privacy_hold"] = "incomplete"
    input_scope: DedupPreviewInputScope = Field(default_factory=DedupPreviewInputScope)
    counts: DedupPreviewCounts = Field(default_factory=DedupPreviewCounts)
    dedup_signals: DedupPreviewSignals = Field(default_factory=DedupPreviewSignals)
    groups: list[DedupGroupCandidate] = Field(default_factory=list)
    excluded_items: list[DedupPreviewExcludedItem] = Field(default_factory=list)
    privacy_scan: DedupPreviewPrivacyScan = Field(default_factory=DedupPreviewPrivacyScan)
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
            "create_production_review_queue_now": False,
            "run_production_dedup_now": False,
            "run_analysis_now": False,
            "generate_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
        }
    )
    readiness: DedupPreviewReadiness = Field(default_factory=DedupPreviewReadiness)
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "dedup_preview_only": True,
            "source_review_only_queue_items_only": True,
            "original_package_rows_re_read": False,
            "evidence_rows_imported": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "production_dedup_run": False,
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


class AnalysisReadyPromotionGateRequest(BaseModel):
    review_case_id: str | None = None
    queue_init_id: str | None = None
    completion_gate_id: str | None = None
    dedup_preview_id: str | None = None
    promotion_decision: str = "approve_for_future_manual_analysis_trigger"
    reviewer_label: str = ""
    note: str = ""
    created_by: str = "sentigraph_local_ui"
    coverage_limitations_acknowledged: bool = False
    privacy_acknowledged: bool = False
    weak_evidence_warning_acknowledged: bool = False
    dedup_preview_warning_acknowledged: bool = False
    provider_output_is_evidence_not_truth_acknowledged: bool = False
    acknowledge_promotion_is_not_analysis: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_no_production_dedup: bool = False
    acknowledge_no_report: bool = False
    production_case_id: str | None = None
    target_production_case_id: str | None = None
    trust_label: str | None = None
    verification_status: str | None = None
    evidence_layer_written: bool = False
    production_case_created: bool = False
    production_review_queue_created: bool = False
    production_dedup_run: bool = False
    analysis_included: bool = False
    analysis_run: bool = False
    report_generated: bool = False
    sandbox_generated: bool = False
    public_event_generated: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    create_production_review_queue_now: bool = False
    run_production_dedup_now: bool = False
    run_dedup_now: bool = False
    run_analysis_now: bool = False
    generate_report_now: bool = False
    generate_sandbox_now: bool = False
    generate_public_event_now: bool = False


class AnalysisReadyPromotionGateInputScope(BaseModel):
    source: Literal["review_only_queue_items"] = "review_only_queue_items"
    include_statuses: list[str] = Field(default_factory=lambda: ["approved", "marked_weak", "duplicate_merged"])
    exclude_statuses: list[str] = Field(default_factory=lambda: ["rejected", "needs_more_source", "privacy_hold", "review_needed"])
    analysis_included: bool = False
    provider_output_is_truth: bool = False
    official_verification: bool = False


class AnalysisReadyPromotionGateCounts(BaseModel):
    items_seen: int = 0
    items_eligible_for_promotion_preview: int = 0
    items_excluded: int = 0
    approved_items: int = 0
    weak_items: int = 0
    duplicate_merged_items: int = 0
    rejected_items: int = 0
    confirmed_duplicate_groups: int = 0
    warning_group_count: int = 0


class AnalysisReadyPromotionSetPreview(BaseModel):
    item_ids: list[str] = Field(default_factory=list)
    group_ids: list[str] = Field(default_factory=list)
    excluded_item_ids: list[str] = Field(default_factory=list)
    weak_item_ids: list[str] = Field(default_factory=list)
    rejected_item_ids: list[str] = Field(default_factory=list)
    warning_notes: list[str] = Field(default_factory=list)


class AnalysisReadyPromotionGateReadiness(BaseModel):
    state: Literal[
        "eligible_for_future_manual_analysis_trigger",
        "held_by_human",
        "rejected_by_human",
        "blocked",
        "privacy_hold",
    ] = "blocked"
    eligible_for_future_manual_analysis_trigger: bool = False
    can_run_analysis_now: bool = False
    can_generate_report_now: bool = False
    requires_human_manual_analysis_trigger: bool = True
    requires_separate_analysis_runtime: bool = True


class AnalysisReadyPromotionDecision(BaseModel):
    promotion_decision_id: str = ""
    decision: str = "approve_for_future_manual_analysis_trigger"
    reviewer_label: str = ""
    decided_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    analysis_effect: Literal[
        "eligible_for_manual_trigger_only",
        "held",
        "rejected",
        "blocked",
    ] = "blocked"


class PromotionDecisionAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_promotion_decision_audit_v1"] = Field(
        default="sentigraph_promotion_decision_audit_v1",
        alias="schema",
    )
    promotion_decision_id: str
    promotion_gate_id: str
    request_id: str
    review_case_id: str
    queue_init_id: str
    completion_gate_id: str
    dedup_preview_id: str
    previous_status: str = "not_created"
    new_status: str = "blocked"
    decision: str = "approve_for_future_manual_analysis_trigger"
    reviewer_label: str = ""
    reviewed_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    affected_item_ids: list[str] = Field(default_factory=list)
    affected_group_ids: list[str] = Field(default_factory=list)
    analysis_effect: Literal[
        "eligible_for_manual_trigger_only",
        "held",
        "rejected",
        "blocked",
    ] = "blocked"
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
            "create_production_review_queue_now": False,
            "run_production_dedup_now": False,
            "run_analysis_now": False,
            "generate_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
        }
    )
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "analysis_ready_promotion_gate_only": True,
            "original_package_rows_re_read": False,
            "evidence_rows_imported": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "production_dedup_run": False,
            "analysis_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )
    boundary_notes: list[str] = Field(default_factory=list)


class AnalysisReadyPromotionGate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_analysis_ready_promotion_gate_v1"] = Field(
        default="sentigraph_analysis_ready_promotion_gate_v1",
        alias="schema",
    )
    promotion_gate_id: str
    request_id: str
    review_case_id: str
    queue_init_id: str
    completion_gate_id: str
    dedup_preview_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    status: Literal[
        "eligible_for_future_manual_analysis_trigger",
        "held_by_human",
        "rejected_by_human",
        "blocked",
        "privacy_hold",
    ] = "blocked"
    input_scope: AnalysisReadyPromotionGateInputScope = Field(default_factory=AnalysisReadyPromotionGateInputScope)
    counts: AnalysisReadyPromotionGateCounts = Field(default_factory=AnalysisReadyPromotionGateCounts)
    promotion_set_preview: AnalysisReadyPromotionSetPreview = Field(default_factory=AnalysisReadyPromotionSetPreview)
    promotion_decision: AnalysisReadyPromotionDecision = Field(default_factory=AnalysisReadyPromotionDecision)
    readiness: AnalysisReadyPromotionGateReadiness = Field(default_factory=AnalysisReadyPromotionGateReadiness)
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
            "create_production_review_queue_now": False,
            "run_production_dedup_now": False,
            "run_analysis_now": False,
            "generate_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
        }
    )
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "analysis_ready_promotion_gate_only": True,
            "source_review_only_queue_items_only": True,
            "original_package_rows_re_read": False,
            "evidence_rows_imported": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "production_dedup_run": False,
            "analysis_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


ManualAnalysisTriggerDecision = Literal["trigger_analysis", "hold", "cancel"]
ManualAnalysisTriggerStatus = Literal[
    "trigger_recorded_ready_for_future_analysis_runtime",
    "held",
    "cancelled",
    "incomplete",
    "blocked",
    "privacy_hold",
]


class ManualAnalysisTriggerRequest(BaseModel):
    promotion_gate_id: str
    review_case_id: str | None = None
    trigger_decision: ManualAnalysisTriggerDecision
    reviewer_label: str
    note: str
    analysis_scope_mode: Literal["promotion_set_preview"] = "promotion_set_preview"
    coverage_acknowledged: bool = False
    privacy_acknowledged: bool = False
    weak_warning_acknowledged: bool = False
    dedup_warning_acknowledged: bool = False
    provider_output_is_evidence_not_truth_acknowledged: bool = False
    not_official_verification_acknowledged: bool = False
    not_full_web_coverage_acknowledged: bool = False
    acknowledge_trigger_record_only: bool = False
    acknowledge_no_analysis_run: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_no_report: bool = False
    acknowledge_no_sandbox_or_public_event: bool = False
    production_case_id: str | None = None
    target_production_case_id: str | None = None
    trust_label: str | None = None
    verification_status: str | None = None
    evidence_layer_written: bool = False
    production_case_created: bool = False
    production_review_queue_created: bool = False
    production_dedup_run: bool = False
    analysis_included: bool = False
    analysis_run: bool = False
    analysis_result_generated: bool = False
    report_generated: bool = False
    sandbox_generated: bool = False
    public_event_generated: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    create_production_review_queue_now: bool = False
    run_production_dedup_now: bool = False
    run_dedup_now: bool = False
    run_analysis_now: bool = False
    generate_analysis_result_now: bool = False
    generate_report_now: bool = False
    generate_sandbox_now: bool = False
    generate_public_event_now: bool = False


class ManualAnalysisScope(BaseModel):
    source: Literal["review_only_promoted_set"] = "review_only_promoted_set"
    include_item_ids: list[str] = Field(default_factory=list)
    include_group_ids: list[str] = Field(default_factory=list)
    exclude_item_ids: list[str] = Field(default_factory=list)
    exclude_group_ids: list[str] = Field(default_factory=list)
    weak_warning_item_ids: list[str] = Field(default_factory=list)
    weak_warning_group_ids: list[str] = Field(default_factory=list)
    analysis_input_source: Literal["review_only_promoted_candidates"] = "review_only_promoted_candidates"
    analysis_included_after_runtime: Literal["not_set_by_this_phase"] = "not_set_by_this_phase"


class ManualAnalysisRequiredWarnings(BaseModel):
    coverage_limitations: list[str] = Field(default_factory=list)
    weak_evidence_warnings: list[str] = Field(default_factory=list)
    dedup_preview_warnings: list[str] = Field(default_factory=list)
    provider_output_is_evidence_not_truth: bool = True
    not_official_verification: bool = True
    not_full_web_coverage: bool = True


class ManualAnalysisTriggerReadiness(BaseModel):
    can_run_analysis_now: bool = False
    analysis_runtime_not_implemented_here: bool = True
    requires_analysis_result_boundary_gate: bool = True
    requires_future_explicit_analysis_execution_phase: bool = True


class ManualAnalysisTrigger(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_manual_analysis_trigger_v1"] = Field(
        default="sentigraph_manual_analysis_trigger_v1",
        alias="schema",
    )
    manual_trigger_id: str
    request_id: str
    review_case_id: str
    promotion_gate_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    trigger_decision: ManualAnalysisTriggerDecision
    status: ManualAnalysisTriggerStatus = "blocked"
    analysis_scope: ManualAnalysisScope = Field(default_factory=ManualAnalysisScope)
    required_warnings: ManualAnalysisRequiredWarnings = Field(default_factory=ManualAnalysisRequiredWarnings)
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
            "create_production_review_queue_now": False,
            "run_production_dedup_now": False,
            "run_analysis_now": False,
            "generate_analysis_result_now": False,
            "generate_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
        }
    )
    readiness: ManualAnalysisTriggerReadiness = Field(default_factory=ManualAnalysisTriggerReadiness)
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "manual_trigger_record_only": True,
            "original_package_rows_re_read": False,
            "evidence_rows_imported": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "production_dedup_run": False,
            "analysis_generated": False,
            "analysis_result_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class ManualAnalysisTriggerAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_manual_analysis_trigger_audit_v1"] = Field(
        default="sentigraph_manual_analysis_trigger_audit_v1",
        alias="schema",
    )
    manual_trigger_audit_id: str
    manual_trigger_id: str
    promotion_gate_id: str
    request_id: str
    review_case_id: str
    decision: ManualAnalysisTriggerDecision
    reviewer_label: str
    decided_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    included_item_ids: list[str] = Field(default_factory=list)
    excluded_item_ids: list[str] = Field(default_factory=list)
    weak_warning_item_ids: list[str] = Field(default_factory=list)
    included_group_ids: list[str] = Field(default_factory=list)
    excluded_group_ids: list[str] = Field(default_factory=list)
    coverage_acknowledgement: bool = True
    privacy_acknowledgement: bool = True
    dedup_warning_acknowledgement: bool = True
    provider_output_is_evidence_not_truth_acknowledgement: bool = True
    analysis_effect: Literal["trigger_record_only_no_analysis_run"] = "trigger_record_only_no_analysis_run"
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "run_analysis_now": False,
            "write_evidence_layer_now": False,
            "generate_analysis_result_now": False,
            "generate_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
        }
    )
    boundary_notes: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "manual_trigger_audit_only": True,
            "analysis_generated": False,
            "analysis_result_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


AnalysisResultBoundaryGateStatus = Literal[
    "boundary_ready_for_future_analysis_result_runtime",
    "incomplete",
    "blocked",
    "privacy_hold",
]


class AnalysisResultBoundaryGateRequest(BaseModel):
    manual_trigger_id: str
    promotion_gate_id: str
    review_case_id: str | None = None
    reviewer_label: str
    note: str
    coverage_limitation_acknowledged: bool = False
    weak_evidence_warning_acknowledged: bool = False
    rejected_evidence_exclusion_acknowledged: bool = False
    dedup_warning_acknowledged: bool = False
    provider_output_is_evidence_not_truth_acknowledged: bool = False
    not_official_verification_acknowledged: bool = False
    not_full_web_coverage_acknowledged: bool = False
    audit_trace_acknowledged: bool = False
    acknowledge_boundary_gate_only: bool = False
    acknowledge_no_analysis_run: bool = False
    acknowledge_no_analysis_result_generation: bool = False
    acknowledge_no_report_generation: bool = False
    acknowledge_no_sandbox_or_public_event: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    run_analysis_now: bool = False
    generate_analysis_result_now: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    run_production_dedup_now: bool = False
    generate_report_now: bool = False
    generate_sandbox_now: bool = False
    generate_public_event_now: bool = False
    provider_output_is_truth: bool = False
    official_verification: bool = False
    full_web_coverage: bool = False
    analysis_includes_rejected: bool = False
    duplicates_amplify_risk: bool = False
    remove_weak_warnings: bool = False
    include_rejected_evidence: bool = False
    include_privacy_hold_evidence: bool = False
    include_needs_more_source_evidence: bool = False


class AnalysisResultInputBoundary(BaseModel):
    source: Literal["review_only_promoted_candidates"] = "review_only_promoted_candidates"
    provider_output_is_truth: bool = False
    official_verification: bool = False
    full_web_coverage: bool = False
    analysis_includes_rejected: bool = False
    duplicates_amplify_risk: bool = False


class AnalysisResultRequiredBoundarySections(BaseModel):
    coverage_limitation: bool = True
    weak_evidence_warning: bool = True
    rejected_evidence_exclusion_note: bool = True
    dedup_warning: bool = True
    provider_output_evidence_not_truth_note: bool = True
    not_official_verification_note: bool = True
    not_full_web_coverage_note: bool = True
    audit_trace_note: bool = True


class AnalysisResultBoundaryCounts(BaseModel):
    included_item_count: int = 0
    excluded_rejected_count: int = 0
    weak_warning_count: int = 0
    duplicate_group_count: int = 0
    privacy_excluded_count: int = 0
    needs_more_source_excluded_count: int = 0


class AnalysisResultBoundaryReadiness(BaseModel):
    can_present_analysis_result_now: bool = False
    requires_future_analysis_execution: bool = True
    requires_boundary_runtime: bool = False
    requires_report_gate: bool = True
    requires_sandbox_gate: bool = True


class AnalysisResultBoundaryGate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_analysis_result_boundary_gate_v1"] = Field(
        default="sentigraph_analysis_result_boundary_gate_v1",
        alias="schema",
    )
    boundary_gate_id: str
    request_id: str
    review_case_id: str
    manual_trigger_id: str
    promotion_gate_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    status: AnalysisResultBoundaryGateStatus = "blocked"
    analysis_input_boundary: AnalysisResultInputBoundary = Field(default_factory=AnalysisResultInputBoundary)
    required_boundary_sections: AnalysisResultRequiredBoundarySections = Field(default_factory=AnalysisResultRequiredBoundarySections)
    counts: AnalysisResultBoundaryCounts = Field(default_factory=AnalysisResultBoundaryCounts)
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
            "run_analysis_now": False,
            "generate_analysis_result_now": False,
            "generate_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
        }
    )
    readiness: AnalysisResultBoundaryReadiness = Field(default_factory=AnalysisResultBoundaryReadiness)
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "analysis_result_boundary_gate_only": True,
            "original_package_rows_re_read": False,
            "evidence_rows_imported": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "production_dedup_run": False,
            "analysis_generated": False,
            "analysis_result_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class AnalysisResultBoundaryGateAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_analysis_result_boundary_gate_audit_v1"] = Field(
        default="sentigraph_analysis_result_boundary_gate_audit_v1",
        alias="schema",
    )
    boundary_gate_audit_id: str
    boundary_gate_id: str
    manual_trigger_id: str
    promotion_gate_id: str
    request_id: str
    review_case_id: str
    reviewer_label: str
    decided_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    coverage_limitation_acknowledged: bool = True
    weak_evidence_warning_acknowledged: bool = True
    rejected_evidence_exclusion_acknowledged: bool = True
    dedup_warning_acknowledged: bool = True
    provider_output_is_evidence_not_truth_acknowledged: bool = True
    not_official_verification_acknowledged: bool = True
    not_full_web_coverage_acknowledged: bool = True
    audit_trace_acknowledged: bool = True
    analysis_effect: Literal["boundary_gate_record_only_no_analysis_run"] = "boundary_gate_record_only_no_analysis_run"
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "run_analysis_now": False,
            "generate_analysis_result_now": False,
            "write_evidence_layer_now": False,
            "generate_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
        }
    )
    boundary_notes: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "analysis_result_boundary_gate_audit_only": True,
            "analysis_generated": False,
            "analysis_result_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class ManualAnalysisExecutionRequest(BaseModel):
    manual_trigger_id: str
    boundary_gate_id: str
    promotion_gate_id: str
    review_case_id: str | None = None
    reviewer_label: str
    note: str
    analysis_execution_mode: Literal["local_review_only_candidate"] = "local_review_only_candidate"
    acknowledge_local_candidate_only: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_no_report_generation: bool = False
    acknowledge_no_sandbox_or_public_event: bool = False
    acknowledge_provider_output_is_evidence_not_truth: bool = False
    acknowledge_not_official_verification: bool = False
    acknowledge_not_full_web_coverage: bool = False
    acknowledge_weak_evidence_warning: bool = False
    acknowledge_rejected_exclusion: bool = False
    acknowledge_dedup_no_risk_amplification: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    run_production_dedup_now: bool = False
    run_analysis_now: bool = False
    generate_analysis_result_now: bool = False
    generate_summary_report_now: bool = False
    generate_report_now: bool = False
    generate_sandbox_now: bool = False
    generate_public_event_now: bool = False
    generate_b_end_report_now: bool = False
    include_rejected_evidence: bool = False
    include_privacy_hold_evidence: bool = False
    include_needs_more_source_evidence: bool = False
    remove_weak_warnings: bool = False
    duplicates_amplify_risk: bool = False
    provider_output_is_truth: bool = False
    official_verification: bool = False
    full_web_coverage: bool = False
    real_api_call_requested: bool = False
    real_llm_call_requested: bool = False
    provider_execution_requested: bool = False
    collector_job_requested: bool = False
    original_package_rows_read: bool = False


class ManualAnalysisExecutionInputScope(BaseModel):
    source: Literal["review_only_promoted_candidates"] = "review_only_promoted_candidates"
    included_item_ids: list[str] = Field(default_factory=list)
    included_group_ids: list[str] = Field(default_factory=list)
    excluded_item_ids: list[str] = Field(default_factory=list)
    excluded_group_ids: list[str] = Field(default_factory=list)
    weak_warning_item_ids: list[str] = Field(default_factory=list)
    weak_warning_group_ids: list[str] = Field(default_factory=list)
    analysis_input_source: Literal["manual_trigger_scope"] = "manual_trigger_scope"
    original_package_rows_read: bool = False


class ManualAnalysisBoundaryBlock(BaseModel):
    coverage_limitation: bool | str = True
    weak_evidence_warning: bool | str = True
    rejected_evidence_exclusion_note: bool | str = True
    dedup_warning: bool | str = True
    provider_output_evidence_not_truth_note: bool | str = True
    not_official_verification_note: bool | str = True
    not_full_web_coverage_note: bool | str = True
    audit_trace_note: bool | str = True
    candidate_only_note: bool | str = True


class ManualAnalysisExecutionReadiness(BaseModel):
    analysis_result_candidate_created: bool = True
    can_generate_report_now: bool = False
    can_generate_sandbox_now: bool = False
    can_generate_public_event_now: bool = False
    requires_result_review_or_report_gate: bool = True


class ManualAnalysisExecution(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_manual_analysis_execution_v1"] = Field(
        default="sentigraph_manual_analysis_execution_v1",
        alias="schema",
    )
    manual_analysis_execution_id: str
    request_id: str
    review_case_id: str
    manual_trigger_id: str
    boundary_gate_id: str
    promotion_gate_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    execution_mode: Literal["local_review_only_candidate"] = "local_review_only_candidate"
    status: Literal["analysis_result_candidate_created", "incomplete", "blocked", "privacy_hold"] = "blocked"
    input_scope: ManualAnalysisExecutionInputScope = Field(default_factory=ManualAnalysisExecutionInputScope)
    boundary_block: ManualAnalysisBoundaryBlock = Field(default_factory=ManualAnalysisBoundaryBlock)
    result_candidate_id: str
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
            "run_production_dedup_now": False,
            "run_analysis_now": False,
            "generate_analysis_result_now": False,
            "generate_summary_report_now": False,
            "generate_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
            "generate_b_end_report_now": False,
        }
    )
    readiness: ManualAnalysisExecutionReadiness = Field(default_factory=ManualAnalysisExecutionReadiness)
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "local_analysis_result_candidate_only": True,
            "original_package_rows_re_read": False,
            "evidence_rows_imported": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "production_dedup_run": False,
            "summary_report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "b_end_report_generated": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class ManualAnalysisSourceScopeSummary(BaseModel):
    included_item_count: int = 0
    included_group_count: int = 0
    excluded_rejected_count: int = 0
    weak_warning_count: int = 0
    duplicate_group_count: int = 0
    privacy_excluded_count: int = 0
    needs_more_source_excluded_count: int = 0


class ManualAnalysisResultCandidate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_manual_analysis_result_candidate_v1"] = Field(
        default="sentigraph_manual_analysis_result_candidate_v1",
        alias="schema",
    )
    result_candidate_id: str
    manual_analysis_execution_id: str
    request_id: str
    review_case_id: str
    created_at: datetime = Field(default_factory=utc_now)
    analysis_input_source: Literal["manual_trigger_scope"] = "manual_trigger_scope"
    source_scope_summary: ManualAnalysisSourceScopeSummary = Field(default_factory=ManualAnalysisSourceScopeSummary)
    boundary_block: dict[str, str] = Field(default_factory=dict)
    analysis_summary: dict[str, Any] = Field(default_factory=dict)
    confidence_notes: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    audit_refs: dict[str, str] = Field(default_factory=dict)
    downstream_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "summary_report_ready": False,
            "sandbox_ready": False,
            "public_event_ready": False,
            "b_end_report_ready": False,
        }
    )


class ManualAnalysisExecutionAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_manual_analysis_execution_audit_v1"] = Field(
        default="sentigraph_manual_analysis_execution_audit_v1",
        alias="schema",
    )
    manual_analysis_execution_audit_id: str
    manual_analysis_execution_id: str
    result_candidate_id: str
    request_id: str
    review_case_id: str
    reviewer_label: str
    decided_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    analysis_effect: Literal["local_result_candidate_created"] = "local_result_candidate_created"
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
            "run_production_dedup_now": False,
            "run_analysis_now": False,
            "generate_analysis_result_now": False,
            "generate_summary_report_now": False,
            "generate_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
            "generate_b_end_report_now": False,
        }
    )
    boundary_notes: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "manual_analysis_execution_audit_only": True,
            "evidence_layer_written": False,
            "production_case_created": False,
            "summary_report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "b_end_report_generated": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


ReportGenerationGateStatus = Literal[
    "report_gate_ready_for_future_runtime",
    "incomplete",
    "blocked",
    "privacy_hold",
]


class ReportGenerationGateRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    manual_analysis_execution_id: str
    result_candidate_id: str
    boundary_gate_id: str
    review_case_id: str | None = None
    reviewer_label: str
    note: str
    requested_future_output: Literal["summary_report_candidate"] = "summary_report_candidate"
    acknowledge_gate_only: bool = False
    acknowledge_no_summary_report_generation: bool = False
    acknowledge_no_b_end_report_generation: bool = False
    acknowledge_no_export_generation: bool = False
    acknowledge_no_sandbox_or_public_event: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_provider_output_is_evidence_not_truth: bool = False
    acknowledge_not_official_verification: bool = False
    acknowledge_not_full_web_coverage: bool = False
    acknowledge_weak_evidence_warning: bool = False
    acknowledge_rejected_exclusion: bool = False
    acknowledge_dedup_no_risk_amplification: bool = False
    acknowledge_audit_trace_required: bool = False
    generate_summary_report_now: bool = False
    generate_report_now: bool = False
    generate_b_end_report_now: bool = False
    export_now: bool = False
    generate_sandbox_now: bool = False
    generate_public_event_now: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    read_original_package_rows_now: bool = False
    call_llm_now: bool = False
    call_external_api_now: bool = False
    provider_execution_requested: bool = False
    collector_job_requested: bool = False
    include_rejected_evidence: bool = False
    include_privacy_hold_evidence: bool = False
    include_needs_more_source_evidence: bool = False
    remove_weak_warnings: bool = False
    duplicates_amplify_risk: bool = False
    provider_output_is_truth: bool = False
    official_verification: bool = False
    full_web_coverage: bool = False


class ReportGenerationAllowedFutureOutputs(BaseModel):
    summary_report_candidate: bool = True
    b_end_report_candidate: bool = False
    pdf_export: bool = False
    markdown_export: bool = False
    briefing_deck_export: bool = False
    sandbox: bool = False
    public_event: bool = False


class ReportGenerationRequiredSections(BaseModel):
    executive_summary: bool = True
    evidence_scope: bool = True
    boundary_block: bool = True
    coverage_limitation: bool = True
    weak_evidence_warning: bool = True
    rejected_evidence_exclusion: bool = True
    dedup_no_amplification: bool = True
    provider_output_evidence_not_truth: bool = True
    not_official_verification: bool = True
    not_full_web_coverage: bool = True
    audit_trace: bool = True
    limitations: bool = True


class ReportGenerationInputBoundary(BaseModel):
    source: Literal["manual_analysis_result_candidate"] = "manual_analysis_result_candidate"
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    read_original_package_rows_now: bool = False
    call_llm_now: bool = False
    call_external_api_now: bool = False


class ReportGenerationReadiness(BaseModel):
    can_generate_summary_report_candidate_in_future: bool = True
    can_generate_summary_report_now: bool = False
    can_generate_b_end_report_now: bool = False
    can_export_now: bool = False
    can_generate_sandbox_now: bool = False
    can_generate_public_event_now: bool = False
    requires_report_runtime: bool = True
    requires_export_gate: bool = True
    requires_sandbox_gate: bool = True
    requires_public_event_gate: bool = True


class ReportGenerationGate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_report_generation_gate_v1"] = Field(
        default="sentigraph_report_generation_gate_v1",
        alias="schema",
    )
    report_gate_id: str
    request_id: str
    review_case_id: str
    manual_analysis_execution_id: str
    result_candidate_id: str
    boundary_gate_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    status: ReportGenerationGateStatus = "blocked"
    allowed_future_outputs: ReportGenerationAllowedFutureOutputs = Field(default_factory=ReportGenerationAllowedFutureOutputs)
    required_report_sections: ReportGenerationRequiredSections = Field(default_factory=ReportGenerationRequiredSections)
    input_boundary: ReportGenerationInputBoundary = Field(default_factory=ReportGenerationInputBoundary)
    readiness: ReportGenerationReadiness = Field(default_factory=ReportGenerationReadiness)
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "report_generation_gate_only": True,
            "summary_report_generated": False,
            "b_end_report_generated": False,
            "pdf_export_generated": False,
            "markdown_export_generated": False,
            "briefing_deck_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "production_dedup_run": False,
            "original_package_rows_re_read": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class ReportGenerationGateAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_report_generation_gate_audit_v1"] = Field(
        default="sentigraph_report_generation_gate_audit_v1",
        alias="schema",
    )
    report_gate_audit_id: str
    report_gate_id: str
    manual_analysis_execution_id: str
    result_candidate_id: str
    boundary_gate_id: str
    request_id: str
    review_case_id: str
    reviewer_label: str
    decided_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    requested_future_output: Literal["summary_report_candidate"] = "summary_report_candidate"
    analysis_effect: Literal["report_generation_gate_record_only_no_report_generated"] = (
        "report_generation_gate_record_only_no_report_generated"
    )
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "generate_summary_report_now": False,
            "generate_b_end_report_now": False,
            "export_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
        }
    )
    boundary_notes: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "report_generation_gate_audit_only": True,
            "summary_report_generated": False,
            "b_end_report_generated": False,
            "export_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


SummaryReportCandidateStatus = Literal[
    "summary_report_candidate_created",
    "incomplete",
    "blocked",
    "privacy_hold",
]


class SummaryReportCandidateRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    report_gate_id: str
    result_candidate_id: str
    manual_analysis_execution_id: str
    boundary_gate_id: str
    review_case_id: str | None = None
    reviewer_label: str
    note: str
    candidate_mode: Literal["local_summary_report_candidate"] = "local_summary_report_candidate"
    acknowledge_candidate_only: bool = False
    acknowledge_not_final_summary_report: bool = False
    acknowledge_no_b_end_report: bool = False
    acknowledge_no_export_generation: bool = False
    acknowledge_no_sandbox_or_public_event: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_provider_output_is_evidence_not_truth: bool = False
    acknowledge_not_official_verification: bool = False
    acknowledge_not_full_web_coverage: bool = False
    acknowledge_weak_evidence_warning: bool = False
    acknowledge_rejected_exclusion: bool = False
    acknowledge_dedup_no_risk_amplification: bool = False
    acknowledge_audit_trace_required: bool = False
    final_report_now: bool = False
    b_end_report_now: bool = False
    export_now: bool = False
    sandbox_now: bool = False
    public_event_now: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    read_original_package_rows_now: bool = False
    call_llm_now: bool = False
    call_external_api_now: bool = False
    provider_execution_requested: bool = False
    collector_job_requested: bool = False
    include_rejected_evidence: bool = False
    include_privacy_hold_evidence: bool = False
    include_needs_more_source_evidence: bool = False
    remove_weak_warnings: bool = False
    duplicates_amplify_risk: bool = False
    provider_output_is_truth: bool = False
    official_verification: bool = False
    full_web_coverage: bool = False


class SummaryReportCandidateInputRefs(BaseModel):
    manual_analysis_execution_id: str
    result_candidate_id: str
    boundary_gate_id: str
    report_gate_id: str
    manual_analysis_execution_audit_ids: list[str] = Field(default_factory=list)
    boundary_gate_audit_ids: list[str] = Field(default_factory=list)
    report_generation_gate_audit_ids: list[str] = Field(default_factory=list)


class SummaryReportExecutiveSummaryCandidate(BaseModel):
    title: str = ""
    one_sentence_summary: str = ""
    key_findings: list[str] = Field(default_factory=list)
    confidence_note: str = ""
    candidate_only_note: str = ""


class SummaryReportEvidenceScopeSection(BaseModel):
    source_scope_summary: dict[str, Any] = Field(default_factory=dict)
    coverage_limitation: str = ""
    selected_reviewed_scope_note: str = ""
    not_full_web_coverage_note: str = ""
    not_official_verification_note: str = ""


class SummaryReportAnalysisSummarySection(BaseModel):
    analysis_summary: dict[str, Any] = Field(default_factory=dict)
    stance_distribution: dict[str, Any] = Field(default_factory=dict)
    sentiment_distribution: dict[str, Any] = Field(default_factory=dict)
    topic_summary: list[Any] = Field(default_factory=list)
    risk_summary: dict[str, Any] = Field(default_factory=dict)


class SummaryReportRiskAndTopicSection(BaseModel):
    risk_summary: dict[str, Any] = Field(default_factory=dict)
    topic_summary: list[Any] = Field(default_factory=list)
    risk_caveats: list[str] = Field(default_factory=list)


class SummaryReportRepresentativeEvidenceSection(BaseModel):
    items: list[dict[str, Any]] = Field(default_factory=list)
    redaction_note: str = ""
    rejected_exclusion_note: str = ""
    weak_evidence_note: str = ""
    duplicate_no_amplification_note: str = ""


class SummaryReportAuditTrace(BaseModel):
    manual_analysis_execution_id: str
    result_candidate_id: str
    boundary_gate_id: str
    report_gate_id: str
    audit_ids: list[str] = Field(default_factory=list)


class SummaryReportCandidate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_summary_report_candidate_v1"] = Field(
        default="sentigraph_summary_report_candidate_v1",
        alias="schema",
    )
    summary_report_candidate_id: str
    request_id: str
    review_case_id: str
    result_candidate_id: str
    manual_analysis_execution_id: str
    report_gate_id: str
    boundary_gate_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    status: SummaryReportCandidateStatus = "blocked"
    input_refs: SummaryReportCandidateInputRefs
    executive_summary_candidate: SummaryReportExecutiveSummaryCandidate = Field(default_factory=SummaryReportExecutiveSummaryCandidate)
    evidence_scope_section: SummaryReportEvidenceScopeSection = Field(default_factory=SummaryReportEvidenceScopeSection)
    analysis_summary_section: SummaryReportAnalysisSummarySection = Field(default_factory=SummaryReportAnalysisSummarySection)
    risk_and_topic_section: SummaryReportRiskAndTopicSection = Field(default_factory=SummaryReportRiskAndTopicSection)
    representative_evidence_section: SummaryReportRepresentativeEvidenceSection = Field(default_factory=SummaryReportRepresentativeEvidenceSection)
    boundary_block: ManualAnalysisBoundaryBlock = Field(default_factory=ManualAnalysisBoundaryBlock)
    limitations: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    audit_trace: SummaryReportAuditTrace
    downstream_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "final_summary_report_ready": False,
            "b_end_report_ready": False,
            "pdf_export_ready": False,
            "markdown_export_ready": False,
            "deck_export_ready": False,
            "sandbox_ready": False,
            "public_event_ready": False,
        }
    )
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "summary_report_candidate_only": True,
            "final_report_generated": False,
            "b_end_report_generated": False,
            "pdf_export_generated": False,
            "markdown_export_generated": False,
            "briefing_deck_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "original_package_rows_re_read": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class SummaryReportCandidateAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_summary_report_candidate_audit_v1"] = Field(
        default="sentigraph_summary_report_candidate_audit_v1",
        alias="schema",
    )
    summary_report_candidate_audit_id: str
    summary_report_candidate_id: str
    request_id: str
    review_case_id: str
    result_candidate_id: str
    manual_analysis_execution_id: str
    report_gate_id: str
    boundary_gate_id: str
    reviewer_label: str
    decided_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    analysis_effect: Literal["summary_report_candidate_created_no_final_report_generated"] = (
        "summary_report_candidate_created_no_final_report_generated"
    )
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "final_summary_report_now": False,
            "b_end_report_now": False,
            "export_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
        }
    )
    boundary_notes: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "summary_report_candidate_audit_only": True,
            "final_report_generated": False,
            "b_end_report_generated": False,
            "export_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


FinalSummaryReportReviewDecision = Literal[
    "approve_for_future_final_runtime",
    "request_revision",
    "block",
    "privacy_hold",
]


FinalSummaryReportReviewGateStatus = Literal[
    "ready_for_future_final_summary_report_runtime",
    "needs_revision",
    "blocked",
    "privacy_hold",
]


class FinalSummaryReportReviewGateRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    summary_report_candidate_id: str
    report_gate_id: str
    result_candidate_id: str
    manual_analysis_execution_id: str
    boundary_gate_id: str
    review_case_id: str | None = None
    reviewer_label: str
    note: str
    review_decision: FinalSummaryReportReviewDecision
    required_revisions: list[str] = Field(default_factory=list)
    acknowledge_review_gate_only: bool = False
    acknowledge_no_final_summary_report_generation: bool = False
    acknowledge_no_b_end_report_generation: bool = False
    acknowledge_no_export_generation: bool = False
    acknowledge_no_sandbox_or_public_event: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_provider_output_is_evidence_not_truth: bool = False
    acknowledge_not_official_verification: bool = False
    acknowledge_not_full_web_coverage: bool = False
    acknowledge_weak_evidence_warning: bool = False
    acknowledge_rejected_exclusion: bool = False
    acknowledge_dedup_no_risk_amplification: bool = False
    acknowledge_audit_trace_required: bool = False
    final_report_now: bool = False
    final_summary_report_now: bool = False
    b_end_report_now: bool = False
    export_now: bool = False
    sandbox_now: bool = False
    public_event_now: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    read_original_package_rows_now: bool = False
    call_llm_now: bool = False
    call_external_api_now: bool = False
    provider_execution_requested: bool = False
    collector_job_requested: bool = False
    include_rejected_evidence: bool = False
    include_privacy_hold_evidence: bool = False
    include_needs_more_source_evidence: bool = False
    remove_weak_warnings: bool = False
    duplicates_amplify_risk: bool = False
    provider_output_is_truth: bool = False
    official_verification: bool = False
    full_web_coverage: bool = False
    full_platform_coverage: bool = False
    full_thread_coverage: bool = False


class FinalSummaryReportRequiredSections(BaseModel):
    executive_summary: bool = True
    evidence_scope: bool = True
    analysis_summary: bool = True
    risk_and_topic: bool = True
    representative_evidence: bool = True
    boundary_block: bool = True
    limitations: bool = True
    warnings: bool = True
    audit_trace: bool = True


class FinalSummaryReportInputBoundary(BaseModel):
    source: Literal["summary_report_candidate"] = "summary_report_candidate"
    read_original_package_rows_now: bool = False
    call_llm_now: bool = False
    call_external_api_now: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False


class FinalSummaryReportDownstreamReadiness(BaseModel):
    can_run_future_final_summary_report_runtime: bool = False
    can_generate_final_summary_report_now: bool = False
    can_export_now: bool = False
    can_generate_b_end_report_now: bool = False
    can_generate_sandbox_now: bool = False
    can_generate_public_event_now: bool = False
    requires_export_gate: bool = True
    requires_b_end_report_gate: bool = True
    requires_sandbox_gate: bool = True
    requires_public_event_gate: bool = True


class FinalSummaryReportReviewGate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_final_summary_report_review_gate_v1"] = Field(
        default="sentigraph_final_summary_report_review_gate_v1",
        alias="schema",
    )
    final_report_review_gate_id: str
    request_id: str
    review_case_id: str
    summary_report_candidate_id: str
    report_gate_id: str
    result_candidate_id: str
    manual_analysis_execution_id: str
    boundary_gate_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    status: FinalSummaryReportReviewGateStatus
    review_decision: FinalSummaryReportReviewDecision
    required_final_report_sections: FinalSummaryReportRequiredSections = Field(default_factory=FinalSummaryReportRequiredSections)
    input_boundary: FinalSummaryReportInputBoundary = Field(default_factory=FinalSummaryReportInputBoundary)
    downstream_readiness: FinalSummaryReportDownstreamReadiness = Field(default_factory=FinalSummaryReportDownstreamReadiness)
    blocked_reasons: list[str] = Field(default_factory=list)
    required_revisions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    audit_refs: dict[str, list[str]] = Field(default_factory=dict)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "final_summary_report_review_gate_only": True,
            "final_summary_report_generated": False,
            "b_end_report_generated": False,
            "export_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "original_package_rows_re_read": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class FinalSummaryReportReviewGateAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_final_summary_report_review_gate_audit_v1"] = Field(
        default="sentigraph_final_summary_report_review_gate_audit_v1",
        alias="schema",
    )
    final_report_review_gate_audit_id: str
    final_report_review_gate_id: str
    summary_report_candidate_id: str
    report_gate_id: str
    result_candidate_id: str
    manual_analysis_execution_id: str
    boundary_gate_id: str
    request_id: str
    review_case_id: str
    reviewer_label: str
    decided_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    review_decision: FinalSummaryReportReviewDecision
    analysis_effect: Literal["final_summary_report_review_gate_record_only_no_final_report_generated"] = (
        "final_summary_report_review_gate_record_only_no_final_report_generated"
    )
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "final_summary_report_now": False,
            "b_end_report_now": False,
            "export_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
        }
    )
    required_revisions: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "final_summary_report_review_gate_audit_only": True,
            "final_summary_report_generated": False,
            "b_end_report_generated": False,
            "export_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class FinalSummaryReportRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    summary_report_candidate_id: str
    final_report_review_gate_id: str
    report_gate_id: str
    result_candidate_id: str
    manual_analysis_execution_id: str
    boundary_gate_id: str
    review_case_id: str | None = None
    reviewer_label: str
    note: str
    acknowledge_local_final_summary_report_only: bool = False
    acknowledge_no_pdf_export: bool = False
    acknowledge_no_markdown_export: bool = False
    acknowledge_no_deck_export: bool = False
    acknowledge_no_b_end_report: bool = False
    acknowledge_no_sandbox_or_public_event: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_provider_output_is_evidence_not_truth: bool = False
    acknowledge_not_official_verification: bool = False
    acknowledge_not_full_web_coverage: bool = False
    acknowledge_weak_evidence_warning: bool = False
    acknowledge_rejected_exclusion: bool = False
    acknowledge_dedup_no_risk_amplification: bool = False
    acknowledge_audit_trace_required: bool = False
    pdf_export_now: bool = False
    markdown_export_now: bool = False
    deck_export_now: bool = False
    b_end_report_now: bool = False
    sandbox_now: bool = False
    public_event_now: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    read_original_package_rows_now: bool = False
    call_llm_now: bool = False
    call_external_api_now: bool = False
    provider_execution_requested: bool = False
    collector_job_requested: bool = False
    include_rejected_evidence: bool = False
    include_privacy_hold_evidence: bool = False
    include_needs_more_source_evidence: bool = False
    remove_weak_warnings: bool = False
    duplicates_amplify_risk: bool = False
    provider_output_is_truth: bool = False
    official_verification: bool = False
    full_web_coverage: bool = False
    full_platform_coverage: bool = False
    full_thread_coverage: bool = False


FinalSummaryReportStatus = Literal["final_summary_report_created", "incomplete", "blocked", "privacy_hold"]


class FinalSummaryReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_final_summary_report_v1"] = Field(
        default="sentigraph_final_summary_report_v1",
        alias="schema",
    )
    final_summary_report_id: str
    request_id: str
    review_case_id: str
    summary_report_candidate_id: str
    final_report_review_gate_id: str
    report_gate_id: str
    result_candidate_id: str
    manual_analysis_execution_id: str
    boundary_gate_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    status: FinalSummaryReportStatus = "final_summary_report_created"
    report_sections: dict[str, Any] = Field(default_factory=dict)
    source_and_scope: dict[str, bool | str] = Field(
        default_factory=lambda: {
            "source": "summary_report_candidate",
            "provider_output_evidence_not_truth": True,
            "not_official_verification": True,
            "not_full_web_coverage": True,
            "not_full_platform_coverage": True,
            "not_full_thread_coverage": True,
        }
    )
    downstream_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "pdf_export_ready": False,
            "markdown_export_ready": False,
            "deck_export_ready": False,
            "b_end_report_ready": False,
            "sandbox_ready": False,
            "public_event_ready": False,
        }
    )
    required_next_gates: dict[str, bool] = Field(
        default_factory=lambda: {
            "export_gate": True,
            "b_end_report_gate": True,
            "sandbox_generation_gate": True,
            "public_event_generation_gate": True,
        }
    )
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    audit_refs: dict[str, list[str]] = Field(default_factory=dict)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "local_final_summary_report_only": True,
            "pdf_export_generated": False,
            "markdown_export_generated": False,
            "briefing_deck_generated": False,
            "b_end_report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "production_dedup_run": False,
            "analysis_engine_called_again": False,
            "original_package_rows_re_read": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class FinalSummaryReportAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_final_summary_report_audit_v1"] = Field(
        default="sentigraph_final_summary_report_audit_v1",
        alias="schema",
    )
    final_summary_report_audit_id: str
    final_summary_report_id: str
    summary_report_candidate_id: str
    final_report_review_gate_id: str
    report_gate_id: str
    result_candidate_id: str
    manual_analysis_execution_id: str
    boundary_gate_id: str
    request_id: str
    review_case_id: str
    reviewer_label: str
    decided_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    analysis_effect: Literal["local_final_summary_report_created_no_export_no_b_end_no_sandbox_no_public_event"] = (
        "local_final_summary_report_created_no_export_no_b_end_no_sandbox_no_public_event"
    )
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "pdf_export_now": False,
            "markdown_export_now": False,
            "deck_export_now": False,
            "b_end_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
        }
    )
    boundary_notes: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "final_summary_report_audit_only": True,
            "pdf_export_generated": False,
            "markdown_export_generated": False,
            "briefing_deck_generated": False,
            "b_end_report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


FinalSummaryReportExportDecision = Literal[
    "approve_for_future_export_runtime",
    "request_revision",
    "block",
    "privacy_hold",
]

FinalSummaryReportExportGateStatus = Literal[
    "ready_for_future_export_runtime",
    "needs_revision",
    "blocked",
    "privacy_hold",
]


class FinalSummaryReportExportGateRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    final_summary_report_id: str
    final_summary_report_audit_id: str
    summary_report_candidate_id: str
    final_report_review_gate_id: str
    report_gate_id: str
    result_candidate_id: str
    manual_analysis_execution_id: str
    boundary_gate_id: str
    review_case_id: str | None = None
    reviewer_label: str
    note: str
    export_decision: FinalSummaryReportExportDecision
    required_revisions: list[str] = Field(default_factory=list)
    acknowledge_export_gate_only: bool = False
    acknowledge_no_markdown_file_now: bool = False
    acknowledge_no_pdf_file_now: bool = False
    acknowledge_no_pptx_file_now: bool = False
    acknowledge_no_b_end_report_generation: bool = False
    acknowledge_no_sandbox_or_public_event: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_provider_output_is_evidence_not_truth: bool = False
    acknowledge_not_official_verification: bool = False
    acknowledge_not_full_web_coverage: bool = False
    acknowledge_weak_evidence_warning: bool = False
    acknowledge_rejected_exclusion: bool = False
    acknowledge_dedup_no_risk_amplification: bool = False
    acknowledge_audit_trace_required: bool = False
    markdown_file_now: bool = False
    pdf_file_now: bool = False
    pptx_file_now: bool = False
    b_end_report_now: bool = False
    sandbox_now: bool = False
    public_event_now: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    read_original_package_rows_now: bool = False
    call_llm_now: bool = False
    call_external_api_now: bool = False
    provider_execution_requested: bool = False
    collector_job_requested: bool = False
    include_rejected_evidence: bool = False
    include_privacy_hold_evidence: bool = False
    include_needs_more_source_evidence: bool = False
    remove_weak_warnings: bool = False
    duplicates_amplify_risk: bool = False
    provider_output_is_truth: bool = False
    official_verification: bool = False
    full_web_coverage: bool = False
    full_platform_coverage: bool = False
    full_thread_coverage: bool = False


class FinalSummaryReportExportGate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_final_summary_report_export_gate_v1"] = Field(
        default="sentigraph_final_summary_report_export_gate_v1",
        alias="schema",
    )
    export_gate_id: str
    request_id: str
    review_case_id: str
    final_summary_report_id: str
    final_summary_report_audit_id: str
    summary_report_candidate_id: str
    final_report_review_gate_id: str
    report_gate_id: str
    result_candidate_id: str
    manual_analysis_execution_id: str
    boundary_gate_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    status: FinalSummaryReportExportGateStatus
    export_decision: FinalSummaryReportExportDecision
    allowed_future_exports: dict[str, bool] = Field(
        default_factory=lambda: {
            "markdown_export_candidate": True,
            "pdf_export_candidate": True,
            "briefing_deck_outline_candidate": True,
            "evidence_appendix_package_candidate": True,
        }
    )
    not_allowed_now: dict[str, bool] = Field(
        default_factory=lambda: {
            "markdown_file_now": True,
            "pdf_file_now": True,
            "pptx_file_now": True,
            "b_end_report_now": True,
            "sandbox_now": True,
            "public_event_now": True,
        }
    )
    input_boundary: dict[str, bool | str] = Field(
        default_factory=lambda: {
            "source": "final_summary_report",
            "read_original_package_rows_now": False,
            "call_llm_now": False,
            "call_external_api_now": False,
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
        }
    )
    required_export_sections: dict[str, bool] = Field(
        default_factory=lambda: {
            "boundary_block": True,
            "evidence_scope": True,
            "coverage_limitation": True,
            "warnings": True,
            "audit_trace": True,
            "source_and_scope": True,
        }
    )
    downstream_readiness: dict[str, bool] = Field(
        default_factory=lambda: {
            "can_run_future_markdown_export_runtime": True,
            "can_run_future_pdf_export_runtime": True,
            "can_run_future_deck_outline_runtime": True,
            "can_generate_export_now": False,
            "can_generate_b_end_report_now": False,
            "can_generate_sandbox_now": False,
            "can_generate_public_event_now": False,
            "requires_b_end_report_gate": True,
            "requires_sandbox_gate": True,
            "requires_public_event_gate": True,
        }
    )
    blocked_reasons: list[str] = Field(default_factory=list)
    required_revisions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    audit_refs: dict[str, list[str]] = Field(default_factory=dict)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "final_summary_report_export_gate_only": True,
            "markdown_file_generated": False,
            "pdf_file_generated": False,
            "pptx_file_generated": False,
            "b_end_report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "production_dedup_run": False,
            "analysis_engine_called_again": False,
            "original_package_rows_re_read": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class FinalSummaryReportExportGateAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_final_summary_report_export_gate_audit_v1"] = Field(
        default="sentigraph_final_summary_report_export_gate_audit_v1",
        alias="schema",
    )
    export_gate_audit_id: str
    export_gate_id: str
    final_summary_report_id: str
    final_summary_report_audit_id: str
    summary_report_candidate_id: str
    final_report_review_gate_id: str
    report_gate_id: str
    result_candidate_id: str
    manual_analysis_execution_id: str
    boundary_gate_id: str
    request_id: str
    review_case_id: str
    reviewer_label: str
    decided_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    export_decision: FinalSummaryReportExportDecision
    analysis_effect: Literal["final_summary_report_export_gate_record_only_no_export_generated"] = (
        "final_summary_report_export_gate_record_only_no_export_generated"
    )
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "markdown_file_now": False,
            "pdf_file_now": False,
            "pptx_file_now": False,
            "b_end_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
        }
    )
    required_revisions: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "final_summary_report_export_gate_audit_only": True,
            "markdown_file_generated": False,
            "pdf_file_generated": False,
            "pptx_file_generated": False,
            "b_end_report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


FinalSummaryReportExportArtifactType = Literal[
    "analyst_markdown",
    "executive_pdf",
    "briefing_deck_outline",
    "evidence_appendix_package",
]

FinalSummaryReportExportArtifactFormat = Literal["md", "pdf", "pptx_outline", "json_bundle"]

FinalSummaryReportExportArtifactStatus = Literal[
    "export_artifact_created",
    "unsupported_format",
    "blocked",
    "privacy_hold",
]


class FinalSummaryReportExportArtifactRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    final_summary_report_id: str
    export_gate_id: str
    export_gate_audit_id: str
    review_case_id: str | None = None
    artifact_type: FinalSummaryReportExportArtifactType
    reviewer_label: str
    note: str
    acknowledge_export_artifact_only: bool = False
    acknowledge_no_b_end_report: bool = False
    acknowledge_no_sandbox_or_public_event: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_provider_output_is_evidence_not_truth: bool = False
    acknowledge_not_official_verification: bool = False
    acknowledge_not_full_web_coverage: bool = False
    acknowledge_weak_evidence_warning: bool = False
    acknowledge_rejected_exclusion: bool = False
    acknowledge_dedup_no_risk_amplification: bool = False
    acknowledge_audit_trace_required: bool = False


class FinalSummaryReportExportArtifact(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_final_summary_report_export_artifact_v1"] = Field(
        default="sentigraph_final_summary_report_export_artifact_v1",
        alias="schema",
    )
    export_artifact_id: str
    request_id: str
    review_case_id: str
    final_summary_report_id: str
    export_gate_id: str
    export_gate_audit_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    status: FinalSummaryReportExportArtifactStatus = "export_artifact_created"
    artifact_type: FinalSummaryReportExportArtifactType
    artifact_format: FinalSummaryReportExportArtifactFormat
    artifact_scope: dict[str, bool | str] = Field(
        default_factory=lambda: {
            "source": "final_summary_report",
            "is_b_end_report": False,
            "is_public_event": False,
            "is_sandbox": False,
            "is_production_case": False,
        }
    )
    artifact_paths: dict[str, str | None] = Field(default_factory=dict)
    export_sections: dict[str, bool] = Field(
        default_factory=lambda: {
            "boundary_block": True,
            "evidence_scope": True,
            "coverage_limitation": True,
            "warnings": True,
            "audit_trace": True,
            "source_and_scope": True,
        }
    )
    source_and_scope: dict[str, bool | str] = Field(
        default_factory=lambda: {
            "provider_output_evidence_not_truth": True,
            "not_official_verification": True,
            "not_full_web_coverage": True,
            "not_full_platform_coverage": True,
            "not_full_thread_coverage": True,
        }
    )
    downstream_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "b_end_report_ready": False,
            "sandbox_ready": False,
            "public_event_ready": False,
        }
    )
    required_next_gates: dict[str, bool] = Field(
        default_factory=lambda: {
            "b_end_report_gate": True,
            "sandbox_generation_gate": True,
            "public_event_generation_gate": True,
        }
    )
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    audit_refs: dict[str, list[str]] = Field(default_factory=dict)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "local_export_artifact_only": True,
            "b_end_report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "production_dedup_run": False,
            "analysis_engine_called_again": False,
            "original_package_rows_re_read": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class FinalSummaryReportExportArtifactAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_final_summary_report_export_artifact_audit_v1"] = Field(
        default="sentigraph_final_summary_report_export_artifact_audit_v1",
        alias="schema",
    )
    export_artifact_audit_id: str
    export_artifact_id: str
    final_summary_report_id: str
    export_gate_id: str
    export_gate_audit_id: str
    request_id: str
    review_case_id: str
    reviewer_label: str
    created_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    artifact_type: FinalSummaryReportExportArtifactType
    artifact_format: FinalSummaryReportExportArtifactFormat
    analysis_effect: Literal["local_export_artifact_created_no_b_end_no_sandbox_no_public_event"] = (
        "local_export_artifact_created_no_b_end_no_sandbox_no_public_event"
    )
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "b_end_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
            "call_llm_now": False,
            "fetch_url_now": False,
            "read_original_rows_now": False,
        }
    )
    boundary_notes: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "final_summary_report_export_artifact_audit_only": True,
            "b_end_report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


ReportExportDownloadPackageDeliveryDecision = Literal[
    "approve_for_future_download_package_runtime",
    "request_revision",
    "block",
    "privacy_hold",
]

ReportExportDownloadPackageGateStatus = Literal[
    "ready_for_future_download_package_runtime",
    "needs_revision",
    "blocked",
    "privacy_hold",
]


class ReportExportDownloadPackageGateRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    export_artifact_id: str
    export_artifact_audit_id: str
    final_summary_report_id: str
    export_gate_id: str
    review_case_id: str
    reviewer_label: str
    note: str
    delivery_decision: ReportExportDownloadPackageDeliveryDecision
    required_revisions: list[str] = Field(default_factory=list)
    acknowledge_download_package_gate_only: bool = False
    acknowledge_no_download_route_now: bool = False
    acknowledge_no_package_or_zip_now: bool = False
    acknowledge_no_public_or_signed_url_now: bool = False
    acknowledge_no_b_end_report: bool = False
    acknowledge_no_sandbox_or_public_event: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_provider_output_is_evidence_not_truth: bool = False
    acknowledge_not_official_verification: bool = False
    acknowledge_not_full_web_coverage: bool = False
    acknowledge_weak_evidence_warning: bool = False
    acknowledge_rejected_exclusion: bool = False
    acknowledge_dedup_no_risk_amplification: bool = False
    acknowledge_audit_trace_required: bool = False
    download_route_now: bool = False
    zip_package_now: bool = False
    package_now: bool = False
    public_url_now: bool = False
    signed_url_now: bool = False
    b_end_report_now: bool = False
    sandbox_now: bool = False
    public_event_now: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    read_runtime_file_content_now: bool = False
    read_original_rows_now: bool = False
    read_original_package_rows_now: bool = False
    call_llm_now: bool = False
    fetch_url_now: bool = False
    call_external_api_now: bool = False
    provider_execution_requested: bool = False
    collector_job_requested: bool = False
    include_rejected_evidence: bool = False
    include_privacy_hold_evidence: bool = False
    include_needs_more_source_evidence: bool = False
    remove_weak_warnings: bool = False
    duplicates_amplify_risk: bool = False
    provider_output_is_truth: bool = False
    official_verification: bool = False
    full_web_coverage: bool = False
    full_platform_coverage: bool = False
    full_thread_coverage: bool = False


class ReportExportDownloadPackageGate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_report_export_download_package_gate_v1"] = Field(
        default="sentigraph_report_export_download_package_gate_v1",
        alias="schema",
    )
    download_package_gate_id: str
    request_id: str
    review_case_id: str
    export_artifact_id: str
    export_artifact_audit_id: str
    final_summary_report_id: str
    export_gate_id: str
    created_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    status: ReportExportDownloadPackageGateStatus
    delivery_decision: ReportExportDownloadPackageDeliveryDecision
    allowed_future_delivery: dict[str, bool] = Field(
        default_factory=lambda: {
            "local_metadata_download_candidate": True,
            "local_file_download_candidate": True,
            "zip_package_candidate": True,
            "signed_url_candidate": False,
            "public_url_candidate": False,
        }
    )
    not_allowed_now: dict[str, bool] = Field(
        default_factory=lambda: {
            "download_route_now": True,
            "zip_package_now": True,
            "public_url_now": True,
            "signed_url_now": True,
            "b_end_report_now": True,
            "sandbox_now": True,
            "public_event_now": True,
        }
    )
    input_boundary: dict[str, bool | str] = Field(
        default_factory=lambda: {
            "source": "final_summary_report_export_artifact",
            "read_runtime_file_content_now": False,
            "read_original_package_rows_now": False,
            "call_llm_now": False,
            "call_external_api_now": False,
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
        }
    )
    delivery_boundary: dict[str, bool] = Field(
        default_factory=lambda: {
            "runtime_path_only": True,
            "public_url": False,
            "download_requires_future_runtime": True,
            "package_requires_future_runtime": True,
            "human_review_required": True,
        }
    )
    downstream_readiness: dict[str, bool] = Field(
        default_factory=lambda: {
            "can_run_future_download_package_runtime": True,
            "can_generate_download_now": False,
            "can_generate_package_now": False,
            "can_generate_b_end_report_now": False,
            "can_generate_sandbox_now": False,
            "can_generate_public_event_now": False,
            "requires_b_end_report_gate": True,
            "requires_sandbox_gate": True,
            "requires_public_event_gate": True,
        }
    )
    blocked_reasons: list[str] = Field(default_factory=list)
    required_revisions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    audit_refs: dict[str, list[str]] = Field(default_factory=dict)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "report_export_download_package_gate_only": True,
            "download_route_created": False,
            "zip_package_created": False,
            "public_url_created": False,
            "signed_url_created": False,
            "b_end_report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "production_dedup_run": False,
            "analysis_engine_called_again": False,
            "runtime_file_content_read": False,
            "original_package_rows_re_read": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class ReportExportDownloadPackageGateAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_report_export_download_package_gate_audit_v1"] = Field(
        default="sentigraph_report_export_download_package_gate_audit_v1",
        alias="schema",
    )
    download_package_gate_audit_id: str
    download_package_gate_id: str
    export_artifact_id: str
    export_artifact_audit_id: str
    final_summary_report_id: str
    export_gate_id: str
    request_id: str
    review_case_id: str
    reviewer_label: str
    decided_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    delivery_decision: ReportExportDownloadPackageDeliveryDecision
    analysis_effect: Literal["report_export_download_package_gate_record_only_no_download_or_package_generated"] = (
        "report_export_download_package_gate_record_only_no_download_or_package_generated"
    )
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "download_route_now": False,
            "zip_package_now": False,
            "public_url_now": False,
            "signed_url_now": False,
            "b_end_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
            "read_runtime_file_content_now": False,
            "read_original_rows_now": False,
            "call_llm_now": False,
            "fetch_url_now": False,
        }
    )
    required_revisions: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "report_export_download_package_gate_audit_only": True,
            "download_route_created": False,
            "zip_package_created": False,
            "public_url_created": False,
            "signed_url_created": False,
            "b_end_report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


ReportExportDownloadPackageArtifactMode = Literal[
    "local_manifest_only",
    "local_controlled_bundle",
    "local_zip_candidate",
    "local_download_candidate",
]

ReportExportDownloadPackageArtifactStatus = Literal[
    "local_manifest_ready",
    "blocked",
    "privacy_hold",
    "failed_safe",
]


class ReportExportDownloadPackageArtifactRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    download_package_gate_id: str
    review_case_id: str
    package_mode: ReportExportDownloadPackageArtifactMode = "local_manifest_only"
    operator_label: str
    note: str
    acknowledge_local_manifest_only: bool = False
    acknowledge_no_download_route: bool = False
    acknowledge_no_file_bytes: bool = False
    acknowledge_no_zip: bool = False
    acknowledge_no_public_or_signed_url: bool = False
    acknowledge_no_runtime_file_exposure: bool = False
    acknowledge_no_artifact_content_read: bool = False
    acknowledge_no_b_end_report: bool = False
    acknowledge_no_sandbox_or_public_event: bool = False
    acknowledge_no_evidence_layer_write: bool = False
    acknowledge_no_production_case: bool = False
    acknowledge_provider_output_is_evidence_not_truth: bool = False
    acknowledge_not_official_verification: bool = False
    acknowledge_not_full_web_coverage: bool = False
    acknowledge_weak_evidence_warning: bool = False
    acknowledge_rejected_exclusion: bool = False
    acknowledge_dedup_no_risk_amplification: bool = False
    acknowledge_audit_trace_required: bool = False
    create_download_route_now: bool = False
    return_file_bytes_now: bool = False
    generate_public_url_now: bool = False
    generate_signed_url_now: bool = False
    generate_zip_now: bool = False
    generate_binary_archive_now: bool = False
    expose_runtime_file_now: bool = False
    expose_absolute_path_now: bool = False
    copy_artifact_file_content_now: bool = False
    read_artifact_file_content_now: bool = False
    parse_artifact_file_content_now: bool = False
    generate_b_end_report_now: bool = False
    generate_sandbox_now: bool = False
    generate_public_event_now: bool = False
    write_evidence_layer_now: bool = False
    create_production_case_now: bool = False
    call_real_api_now: bool = False
    call_real_llm_now: bool = False
    fetch_url_now: bool = False
    scrape_now: bool = False
    read_original_package_rows_now: bool = False


class ReportExportDownloadPackageArtifact(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_report_export_download_package_artifact_v1"] = Field(
        default="sentigraph_report_export_download_package_artifact_v1",
        alias="schema",
    )
    package_artifact_id: str
    request_id: str
    review_case_id: str
    download_package_gate_id: str
    final_summary_report_export_artifact_ids: list[str] = Field(default_factory=list)
    final_summary_report_id: str
    final_summary_report_export_gate_id: str
    package_type: Literal["report_export_download_package_artifact"] = "report_export_download_package_artifact"
    package_version: Literal["sentigraph_report_export_download_package_artifact_v1"] = (
        "sentigraph_report_export_download_package_artifact_v1"
    )
    package_mode: Literal["local_manifest_only"] = "local_manifest_only"
    package_status: ReportExportDownloadPackageArtifactStatus = "local_manifest_ready"
    manifest_id: str
    manifest_runtime_ref: str
    manifest_summary: dict[str, bool | int | str] = Field(default_factory=dict)
    file_inventory_summary: dict[str, bool | int | list[str]] = Field(default_factory=dict)
    source_export_artifact_refs: list[dict[str, str]] = Field(default_factory=list)
    unsupported_modes: list[str] = Field(
        default_factory=lambda: [
            "local_controlled_bundle",
            "local_zip_candidate",
            "public_download_route",
            "signed_url_delivery",
            "external_delivery",
        ]
    )
    boundary_block: dict[str, bool] = Field(
        default_factory=lambda: {
            "creates_download_route_now": False,
            "returns_file_bytes_now": False,
            "generates_public_url_now": False,
            "generates_signed_url_now": False,
            "generates_zip_now": False,
            "generates_binary_archive_now": False,
            "exposes_runtime_file_now": False,
            "exposes_absolute_path_now": False,
            "copies_artifact_file_content_now": False,
            "reads_artifact_file_content_now": False,
            "parses_artifact_file_content_now": False,
            "generates_local_manifest_package_now": True,
            "generates_b_end_report_now": False,
            "generates_sandbox_now": False,
            "generates_public_event_now": False,
            "writes_evidence_layer_now": False,
            "creates_production_case_now": False,
            "calls_real_api_now": False,
            "calls_real_llm_now": False,
            "fetches_url_now": False,
            "scrapes_now": False,
            "reads_original_package_rows_now": False,
        }
    )
    warnings: list[str] = Field(default_factory=list)
    boundary_notes: list[str] = Field(default_factory=list)
    audit_trace: dict[str, list[str]] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    created_by: str = "sentigraph_local_ui"
    note: str = ""
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "local_manifest_package_artifact_only": True,
            "download_route_created": False,
            "file_bytes_returned": False,
            "zip_package_created": False,
            "binary_archive_created": False,
            "public_url_created": False,
            "signed_url_created": False,
            "runtime_file_exposed": False,
            "absolute_path_exposed": False,
            "artifact_file_content_read": False,
            "artifact_file_content_copied": False,
            "b_end_report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "production_review_queue_created": False,
            "production_dedup_run": False,
            "analysis_engine_called_again": False,
            "original_package_rows_re_read": False,
            "provider_execution": False,
            "collector_jobs_run": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
        }
    )


class ReportExportDownloadPackageArtifactAudit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_: Literal["sentigraph_report_export_download_package_artifact_audit_v1"] = Field(
        default="sentigraph_report_export_download_package_artifact_audit_v1",
        alias="schema",
    )
    package_artifact_audit_id: str
    package_artifact_id: str
    request_id: str
    review_case_id: str
    download_package_gate_id: str
    final_summary_report_export_artifact_ids: list[str] = Field(default_factory=list)
    final_summary_report_id: str
    final_summary_report_export_gate_id: str
    action: Literal["package_artifact_created", "package_artifact_blocked", "manifest_created"] = (
        "package_artifact_created"
    )
    previous_status: str = "not_created"
    new_status: ReportExportDownloadPackageArtifactStatus = "local_manifest_ready"
    operator_label: str = "sentigraph_local_ui"
    created_at: datetime = Field(default_factory=utc_now)
    note: str = ""
    analysis_effect: Literal["local_manifest_package_created_no_download_no_zip_no_public_delivery"] = (
        "local_manifest_package_created_no_download_no_zip_no_public_delivery"
    )
    boundary_confirmation_snapshot: dict[str, bool] = Field(default_factory=dict)
    manifest_summary_snapshot: dict[str, bool | int | str] = Field(default_factory=dict)
    upstream_gate_refs: dict[str, list[str]] = Field(default_factory=dict)
    now_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "download_route_now": False,
            "return_file_bytes_now": False,
            "zip_now": False,
            "binary_archive_now": False,
            "public_url_now": False,
            "signed_url_now": False,
            "expose_runtime_file_now": False,
            "expose_absolute_path_now": False,
            "read_artifact_file_content_now": False,
            "copy_artifact_file_content_now": False,
            "generate_b_end_report_now": False,
            "generate_sandbox_now": False,
            "generate_public_event_now": False,
            "write_evidence_layer_now": False,
            "create_production_case_now": False,
            "call_llm_now": False,
            "fetch_url_now": False,
            "read_original_rows_now": False,
        }
    )
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "report_export_download_package_artifact_audit_only": True,
            "download_route_created": False,
            "file_bytes_returned": False,
            "zip_package_created": False,
            "public_url_created": False,
            "signed_url_created": False,
            "runtime_file_exposed": False,
            "artifact_file_content_read": False,
            "b_end_report_generated": False,
            "sandbox_fixture_generated": False,
            "public_event_page_generated": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "real_api_calls": False,
            "real_llm_calls": False,
            "url_fetching": False,
            "scraping": False,
            "secrets_exposed": False,
            "raw_author_identifiers_exposed": False,
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
