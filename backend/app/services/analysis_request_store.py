from __future__ import annotations

import json
import os
import re
import uuid
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from app.schemas.analysis_request import (
    AnalysisRequestCancelResult,
    AnalysisRequestConfig,
    AnalysisRequestCreate,
    AnalysisRequestFile,
    AnalysisRequestRecord,
    AnalysisReadyPromotionDecision,
    AnalysisReadyPromotionGate,
    AnalysisReadyPromotionGateCounts,
    AnalysisReadyPromotionGateInputScope,
    AnalysisReadyPromotionGateReadiness,
    AnalysisReadyPromotionGateRequest,
    AnalysisReadyPromotionSetPreview,
    CaseDraftHandoff,
    CaseDraftPackageReference,
    CaseDraftProviderSummary,
    CaseDraftReadiness,
    DedupGroupCandidate,
    DedupGroupReviewActionRequest,
    DedupGroupReviewActionResult,
    DedupGroupReviewAudit,
    DedupPreview,
    DedupPreviewCounts,
    DedupPreviewExcludedItem,
    DedupPreviewInputScope,
    DedupPreviewPrivacyScan,
    DedupPreviewReadiness,
    DedupPreviewRequest,
    EvidenceImportPlan,
    EvidenceImportPlanReadiness,
    EvidenceImportPreview,
    EvidenceImportPreviewReadiness,
    EvidenceImportReviewAudit,
    EvidenceImportReviewDecision,
    EvidenceImportReviewDecisionCreate,
    EvidenceImportReviewReadiness,
    EvidenceRowReaderCandidate,
    EvidenceRowReaderCounts,
    EvidenceRowReaderDryRun,
    EvidenceRowReaderDryRunCreate,
    EvidenceRowReaderFixturePolicy,
    EvidenceRowReaderGovernanceDefaults,
    EvidenceRowReaderNowFlags,
    EvidenceRowReaderPreviewRow,
    EvidenceRowReaderPrivacyCheck,
    EvidenceRowReaderPrivacyScan,
    EvidenceRowReaderReadiness,
    EvidenceRowReaderRowSource,
    EvidenceRowReaderSummaryItem,
    ManualEvidenceImportExecutionPreflight,
    ManualEvidenceImportExecutionPreflightCreate,
    ManualEvidenceImportExecutionPreflightReadiness,
    ManualEvidenceImportFutureGovernancePlan,
    ManualEvidenceImportFutureRowReaderPlan,
    ManualEvidenceImportFutureStagingPlan,
    ManualEvidenceImportJob,
    ManualEvidenceImportJobCreate,
    ManualEvidenceImportJobReadiness,
    ManualAnalysisRequiredWarnings,
    ManualAnalysisScope,
    ManualAnalysisTrigger,
    ManualAnalysisTriggerAudit,
    ManualAnalysisTriggerReadiness,
    ManualAnalysisTriggerRequest,
    ManualEvidenceImportPackageFileChecks,
    ManualEvidenceImportPreflightChecks,
    ManualEvidenceImportTargetCase,
    ManualEvidenceImportTargetCasePreflight,
    PromotionDecisionAudit,
    ProviderJobResult,
    RealPackageRowPreview,
    RealPackageRowPreviewCandidate,
    RealPackageRowPreviewCreate,
    RealPackageRowPreviewLimits,
    RealPackageRowPreviewPackageReference,
    RealPackageRowPreviewPrivacyCheck,
    RealPackageRowPreviewPrivacyScan,
    RealPackageRowPreviewReadiness,
    RealPackageRowPreviewRow,
    RealPackageRowPreviewRows,
    ReviewOnlyCase,
    ReviewOnlyCaseAudit,
    ReviewOnlyCaseCreate,
    ReviewOnlyCaseGovernanceDefaults,
    ReviewOnlyCaseReadiness,
    ReviewOnlyCaseSourcePreviewSummary,
    ReviewOnlyCaseStagingImport,
    ReviewOnlyCaseStagingImportCounts,
    ReviewOnlyCaseStagingImportCreate,
    ReviewOnlyCaseStagingReadiness,
    ReviewOnlyCaseStagingRollback,
    ReviewOnlyCaseStagingTarget,
    ReviewOnlyCaseTargetReference,
    ReviewOnlyStagedGovernance,
    ReviewQueueActionAudit,
    ReviewQueueActionRequest,
    ReviewQueueActionResult,
    ReviewQueueCompletionGate,
    ReviewQueueCompletionGateAuditSummary,
    ReviewQueueCompletionGateCounts,
    ReviewQueueCompletionGateDownstreamEligibility,
    ReviewQueueCompletionGateRequest,
    ReviewQueueDefaults,
    ReviewQueueInitialization,
    ReviewQueueInitializationCounts,
    ReviewQueueInitializationCreate,
    ReviewQueueInitializationReadiness,
    ReviewQueueInitializationSource,
    ReviewQueueInitializationTarget,
    ReviewQueueItem,
    ReviewQueueItemAudit,
    ReviewQueueItemBatch,
    ReviewQueueItemDedup,
    StagedEvidenceCandidate,
    StagedEvidenceCandidateAudit,
    StagedEvidenceCandidateBatch,
    StagedEvidenceCandidateDedup,
    StagedEvidenceCandidatePreview,
    StagedEvidenceCandidatePrivacy,
)


ANALYSIS_REQUESTS_ENV_VAR = "SENTIGRAPH_ANALYSIS_REQUESTS_DIR"
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ROOT = PROJECT_ROOT / "runtime" / "analysis_requests"
REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")
ROW_READER_FIXTURE_ROOT = PROJECT_ROOT / "backend" / "app" / "tests" / "fixtures" / "analysis_request_row_reader"
ROW_READER_FIXTURES = {
    "safe_evidence_items": "safe_evidence_items.jsonl",
    "mixed_evidence_items": "mixed_evidence_items.jsonl",
}
ROW_READER_FORBIDDEN_FIELDS = {"raw_author_id", "raw_author_name", "profile_url", "private_message"}
ROW_READER_SECRET_PATTERNS = ("api_key", "access_token", "refresh_token", "client_secret", "password", "cookie", "token")
ROW_READER_ALLOWED_FIELDS = {"platform", "evidence_type", "source_url", "title", "body_text", "created_at", "language"}
REAL_PREVIEW_FORBIDDEN_FIELDS = {
    "raw_author_id",
    "raw_author_name",
    "author_name",
    "profile_url",
    "avatar_url",
    "private_message",
}
REAL_PREVIEW_COUNT_FIELDS = {"like_count", "reply_count", "share_count", "view_count", "repost_count"}
EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)")

REVIEW_DECISION_STATES = {
    "approve_import": "approved_for_future_manual_import",
    "reject_import": "rejected",
    "request_more_source": "needs_more_source",
    "mark_limited_sample": "limited_sample_only",
    "hold_for_privacy_review": "held_for_privacy_review",
}

REVIEW_DECISION_NEXT_STEPS = {
    "approve_import": "Next phase may create a manual evidence import job, still with human confirmation.",
    "reject_import": "Package remains visible for audit but should not be imported.",
    "request_more_source": "Ask provider for more sources or clearer coverage/validation.",
    "mark_limited_sample": "May only be used as controlled sample; do not present as broad coverage.",
    "hold_for_privacy_review": "Requires privacy/legal/security review before any import job.",
}


class AnalysisRequestStoreError(Exception):
    pass


class AnalysisRequestNotFoundError(AnalysisRequestStoreError):
    pass


class AnalysisRequestValidationError(AnalysisRequestStoreError):
    pass


def get_analysis_request_config() -> AnalysisRequestConfig:
    root = _request_root()
    requests_dir = root / "requests"
    results_dir = root / "results"
    return AnalysisRequestConfig(
        configured_by_env=bool(os.environ.get(ANALYSIS_REQUESTS_ENV_VAR, "").strip()),
        root_exists=root.exists(),
        requests_dir_exists=requests_dir.exists(),
        results_dir_exists=results_dir.exists(),
        request_count=_json_count(requests_dir),
        result_count=_json_count(results_dir),
        root_label=_safe_root_label(root),
    )


def create_analysis_request(payload: AnalysisRequestCreate) -> AnalysisRequestRecord:
    root = _ensure_root()
    request_id = _new_request_id(payload.case_seed.title)
    output = payload.output.model_copy()
    if not output.package_slug:
        output.package_slug = _slugify(payload.case_seed.title) or request_id
    request = AnalysisRequestFile(
        request_id=request_id,
        created_by=payload.created_by or "sentigraph_local_user",
        case_seed=payload.case_seed,
        sampling_plan=payload.sampling_plan,
        safety_policy=payload.safety_policy,
        privacy_policy=payload.privacy_policy,
        output=output,
        sentigraph_metadata={
            "request_status": "draft",
            "provider_execution": "outside_sentigraph_core",
            "collector_jobs_run": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
        },
    )
    _write_json(root / "requests" / f"{request_id}.json", request.model_dump(mode="json", by_alias=True))
    return read_analysis_request(request_id)


def list_analysis_requests() -> list[AnalysisRequestRecord]:
    root = _ensure_root()
    records: list[AnalysisRequestRecord] = []
    for path in sorted((root / "requests").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            records.append(_record_from_path(path))
        except AnalysisRequestValidationError:
            continue
    return records


def read_analysis_request(request_id: str) -> AnalysisRequestRecord:
    request_path = _request_path(request_id)
    if not request_path.exists():
        raise AnalysisRequestNotFoundError(f"Analysis request {request_id} was not found.")
    return _record_from_path(request_path)


def cancel_analysis_request(request_id: str) -> AnalysisRequestCancelResult:
    record = read_analysis_request(request_id)
    if record.provider_result and record.provider_result.status == "package_ready":
        return AnalysisRequestCancelResult(
            request_id=request_id,
            status=record.request_status,
            request=record.request,
            warning="Provider result is already package_ready; local cancel did not call provider or change provider state.",
        )

    metadata = dict(record.request.sentigraph_metadata or {})
    metadata.update(
        {
            "request_status": "canceled",
            "canceled_at": datetime.now(timezone.utc).isoformat(),
            "provider_cancel_called": False,
            "collector_jobs_run": False,
        }
    )
    updated = record.request.model_copy(update={"sentigraph_metadata": metadata})
    _write_json(_request_path(request_id), updated.model_dump(mode="json", by_alias=True))
    return AnalysisRequestCancelResult(request_id=request_id, status="canceled", request=updated)


def read_case_draft_handoff(request_id: str) -> CaseDraftHandoff:
    draft_path = _case_draft_path(request_id)
    if not draft_path.exists():
        raise AnalysisRequestNotFoundError(f"Case draft handoff for {request_id} was not found.")
    try:
        parsed = json.loads(draft_path.read_text(encoding="utf-8-sig"))
        return CaseDraftHandoff.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{draft_path.name} is not a valid case draft handoff: {type(exc).__name__}") from exc


def list_case_draft_handoffs() -> list[CaseDraftHandoff]:
    root = _ensure_root()
    drafts: list[CaseDraftHandoff] = []
    for path in sorted((root / "case_drafts").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            drafts.append(CaseDraftHandoff.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return drafts


def create_case_draft_handoff(request_id: str) -> CaseDraftHandoff:
    draft_path = _case_draft_path(request_id)
    if draft_path.exists():
        return read_case_draft_handoff(request_id)

    record = read_analysis_request(request_id)
    _validate_case_draft_eligibility(record)
    result = record.provider_result
    assert result is not None

    draft = CaseDraftHandoff(
        draft_id=f"draft_{request_id}",
        request_id=request_id,
        case_seed=record.request.case_seed,
        provider_summary=CaseDraftProviderSummary(
            provider_job_id=result.provider_job_id,
            provider_type=result.provider_type,
            status=result.status,
            safety_status=result.safety_status,
        ),
        package_reference=CaseDraftPackageReference(
            package_name=result.package_name,
            package_role=result.package_role,
            package_path=result.package_path,
            package_index_path=result.package_index_path,
        ),
        counts=result.counts,
        validation=result.validation,
        coverage=result.coverage,
        privacy=result.privacy,
        readiness=CaseDraftReadiness(
            state="ready_for_manual_review",
            can_import_evidence=False,
            requires_human_review=True,
            reason="Provider result is validation_warn/package_ready but evidence import is not automatic.",
        ),
        boundary_notes=[
            "Provider output is evidence metadata, not official truth.",
            "Draft creation does not import evidence rows.",
            "Draft creation does not run analysis, generate reports, or create public event pages.",
            "Coverage is selected/controlled available evidence, not full-web or full-platform coverage.",
        ],
        recommended_next_steps=[
            "Review provider result and coverage note.",
            "Run or open the external package validator manually if needed.",
            "Decide whether to import the package into the Evidence layer.",
            "If imported, mark review_status and verification_status clearly.",
            "Only after manual review generate public event sample, Sandbox fixture, or B-end report draft.",
        ],
    )
    _write_json(draft_path, draft.model_dump(mode="json", by_alias=True))
    return read_case_draft_handoff(request_id)


def read_evidence_import_plan(request_id: str) -> EvidenceImportPlan:
    plan_path = _import_plan_path(request_id)
    if not plan_path.exists():
        raise AnalysisRequestNotFoundError(f"Evidence import plan for {request_id} was not found.")
    try:
        parsed = json.loads(plan_path.read_text(encoding="utf-8-sig"))
        return EvidenceImportPlan.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{plan_path.name} is not a valid evidence import plan: {type(exc).__name__}") from exc


def list_evidence_import_plans() -> list[EvidenceImportPlan]:
    root = _ensure_root()
    plans: list[EvidenceImportPlan] = []
    for path in sorted((root / "import_plans").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            plans.append(EvidenceImportPlan.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return plans


def create_evidence_import_plan(request_id: str) -> EvidenceImportPlan:
    plan_path = _import_plan_path(request_id)
    if plan_path.exists():
        return read_evidence_import_plan(request_id)

    draft = read_case_draft_handoff(request_id)
    _validate_import_plan_eligibility(draft)

    plan = EvidenceImportPlan(
        plan_id=f"import_plan_{request_id}",
        draft_id=draft.draft_id,
        request_id=request_id,
        package_reference=draft.package_reference,
        counts=draft.counts,
        validation=draft.validation,
        coverage=draft.coverage,
        privacy=draft.privacy,
        readiness=EvidenceImportPlanReadiness(
            state="ready_for_manual_import_review",
            can_import_now=False,
            requires_human_review=True,
            reason="Import plan only. Evidence rows are not imported automatically.",
        ),
        manual_review_checklist=[
            "Review coverage_note and validation_report before any import.",
            "Confirm the package is a selected/controlled public sample, not full-web coverage.",
            "Confirm privacy flags are present.",
            "Confirm raw author ids/names/profile URLs/private messages are not included.",
            "Confirm evidence should default to review_needed.",
            "Confirm verification_status should default to source_url_provided_unverified unless official API proof exists.",
            "Confirm trust_label should default to medium_low unless upgraded by human review.",
            "Confirm duplicate folding/dedup should run before analysis.",
            "Confirm rejected/weak evidence must not amplify risk.",
            "Confirm no report, Sandbox fixture, or public event page should be generated before import review.",
        ],
        blockers=[],
        boundary_notes=[
            "This is an Evidence import plan only; no evidence rows are imported.",
            "No production case is created by this plan.",
            "No analysis, report, Sandbox fixture, or public event page is generated by this plan.",
            "Provider output is evidence, not official truth.",
            "Coverage remains a selected/controlled available evidence sample, not full-web or full-platform coverage.",
        ],
        recommended_next_steps=[
            "Human reviewer opens the package README, coverage note, and validation report.",
            "Decide whether to import evidence rows into the Evidence layer.",
            "Choose an import target case or create a new case manually in a later task.",
            "Run deduplication and review queue after import.",
            "Only after evidence governance generate analysis, public event page, Sandbox fixture, or B-end report.",
        ],
    )
    _write_json(plan_path, plan.model_dump(mode="json", by_alias=True))
    return read_evidence_import_plan(request_id)


def read_evidence_import_preview(request_id: str) -> EvidenceImportPreview:
    preview_path = _import_preview_path(request_id)
    if not preview_path.exists():
        raise AnalysisRequestNotFoundError(f"Evidence import preview for {request_id} was not found.")
    try:
        parsed = json.loads(preview_path.read_text(encoding="utf-8-sig"))
        return EvidenceImportPreview.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{preview_path.name} is not a valid evidence import preview: {type(exc).__name__}") from exc


def list_evidence_import_previews() -> list[EvidenceImportPreview]:
    root = _ensure_root()
    previews: list[EvidenceImportPreview] = []
    for path in sorted((root / "import_previews").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            previews.append(EvidenceImportPreview.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return previews


def create_evidence_import_preview(request_id: str) -> EvidenceImportPreview:
    preview_path = _import_preview_path(request_id)
    if preview_path.exists():
        return read_evidence_import_preview(request_id)

    plan = read_evidence_import_plan(request_id)
    _validate_import_preview_eligibility(plan)

    preview = EvidenceImportPreview(
        preview_id=f"import_preview_{request_id}",
        plan_id=plan.plan_id,
        draft_id=plan.draft_id,
        request_id=request_id,
        package_reference=plan.package_reference,
        metadata_summary=plan.counts,
        validation_summary=plan.validation,
        coverage_summary=plan.coverage,
        privacy_summary=plan.privacy,
        proposed_evidence_defaults=plan.default_evidence_policy,
        blockers=[],
        warnings=[
            "Preview is metadata-only and does not read evidence rows.",
            "Provider output is evidence, not truth.",
            "Coverage is selected/controlled public sample metadata, not full-web or full-platform coverage.",
        ],
        readiness=EvidenceImportPreviewReadiness(
            state="ready_for_human_review",
            can_import_now=False,
            requires_review_decision=True,
            reason="Import preview only. Evidence rows are not imported.",
        ),
        boundary_notes=[
            "Import preview is not import.",
            "Preview does not create a production case.",
            "Preview does not run analysis, generate reports, or create Sandbox/public event outputs.",
            "Preview does not verify truth or official status.",
            "Evidence rows require a later human review decision and manual import job.",
        ],
        recommended_next_steps=[
            "Human reviewer opens package README, coverage_note, and validation_report.",
            "Reviewer decides approve_import, reject_import, request_more_source, or hold_for_privacy_review.",
            "Only after review decision create a manual Evidence import job.",
            "Dedup and review queue must run before analysis.",
            "Analysis, Sandbox, public event, and report generation are later explicit actions only.",
        ],
    )
    _write_json(preview_path, preview.model_dump(mode="json", by_alias=True))
    return read_evidence_import_preview(request_id)


def read_evidence_import_review_decision(request_id: str, decision_id: str) -> EvidenceImportReviewDecision:
    decision_path = _review_decision_path(request_id, decision_id)
    if not decision_path.exists():
        raise AnalysisRequestNotFoundError(f"Evidence import review decision {decision_id} for {request_id} was not found.")
    try:
        parsed = json.loads(decision_path.read_text(encoding="utf-8-sig"))
        return EvidenceImportReviewDecision.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{decision_path.name} is not a valid review decision: {type(exc).__name__}") from exc


def list_evidence_import_review_decisions(request_id: str) -> list[EvidenceImportReviewDecision]:
    _validate_request_id(request_id)
    root = _ensure_root()
    decisions: list[EvidenceImportReviewDecision] = []
    for path in sorted((root / "review_decisions").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            decisions.append(EvidenceImportReviewDecision.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return decisions


def list_all_evidence_import_review_decisions() -> list[EvidenceImportReviewDecision]:
    root = _ensure_root()
    decisions: list[EvidenceImportReviewDecision] = []
    for path in sorted((root / "review_decisions").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            decisions.append(EvidenceImportReviewDecision.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return decisions


def create_evidence_import_review_decision(
    request_id: str,
    payload: EvidenceImportReviewDecisionCreate | dict[str, Any],
) -> EvidenceImportReviewDecision:
    try:
        decision_payload = (
            payload
            if isinstance(payload, EvidenceImportReviewDecisionCreate)
            else EvidenceImportReviewDecisionCreate.model_validate(payload)
        )
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create review decision: invalid decision payload ({exc}).") from exc

    if not decision_payload.reviewer_label.strip():
        raise AnalysisRequestValidationError("Cannot create review decision: reviewer_label is required.")
    if decision_payload.decision not in REVIEW_DECISION_STATES:
        raise AnalysisRequestValidationError("Cannot create review decision: decision value is unknown.")
    if decision_payload.decision == "approve_import":
        missing_acknowledgements = decision_payload.checklist.missing_acknowledgements()
        if missing_acknowledgements:
            raise AnalysisRequestValidationError(
                f"Cannot create review decision: approve_import requires all checklist acknowledgements ({', '.join(missing_acknowledgements)})."
            )
    elif not decision_payload.notes.strip():
        raise AnalysisRequestValidationError("Cannot create review decision: notes are required for non-approve decisions.")

    preview = read_evidence_import_preview(request_id)
    _validate_review_decision_preview_eligibility(preview)
    decision_id = _new_review_decision_id()
    now = datetime.now(timezone.utc)
    decision = EvidenceImportReviewDecision(
        decision_id=decision_id,
        preview_id=preview.preview_id,
        plan_id=preview.plan_id,
        draft_id=preview.draft_id,
        request_id=request_id,
        reviewer_label=decision_payload.reviewer_label.strip(),
        reviewed_at=now,
        decision=decision_payload.decision,
        target_case_mode=decision_payload.target_case_mode,
        target_case_id=decision_payload.target_case_id,
        notes=decision_payload.notes.strip(),
        checklist=decision_payload.checklist,
        approved_defaults=preview.proposed_evidence_defaults,
        readiness=EvidenceImportReviewReadiness(
            state=REVIEW_DECISION_STATES[decision_payload.decision],
            can_create_import_job_now=False,
            requires_future_manual_import_phase=True,
            reason="Review decision recorded. Evidence rows are not imported in Phase 6H.",
        ),
        boundary_notes=[
            "Review decision is not import.",
            "Approval only allows a future manual import job phase.",
            "Evidence rows are still not imported.",
            "No production case is created.",
            "No analysis, report, Sandbox fixture, or public event page is generated.",
            "Provider output remains evidence, not official truth.",
            REVIEW_DECISION_NEXT_STEPS[decision_payload.decision],
        ],
        audit=EvidenceImportReviewAudit(
            created_by=decision_payload.created_by or "sentigraph_local_ui",
            created_at=now,
            source="manual_review",
        ),
    )
    _write_json(_review_decision_path(request_id, decision_id), decision.model_dump(mode="json", by_alias=True))
    return read_evidence_import_review_decision(request_id, decision_id)


def read_manual_evidence_import_job(request_id: str, job_id: str) -> ManualEvidenceImportJob:
    job_path = _import_job_path(request_id, job_id)
    if not job_path.exists():
        raise AnalysisRequestNotFoundError(f"Manual evidence import job {job_id} for {request_id} was not found.")
    try:
        parsed = json.loads(job_path.read_text(encoding="utf-8-sig"))
        return ManualEvidenceImportJob.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{job_path.name} is not a valid manual import job: {type(exc).__name__}") from exc


def list_manual_evidence_import_jobs(request_id: str) -> list[ManualEvidenceImportJob]:
    _validate_request_id(request_id)
    root = _ensure_root()
    jobs: list[ManualEvidenceImportJob] = []
    for path in sorted((root / "import_jobs").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            jobs.append(ManualEvidenceImportJob.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return jobs


def list_all_manual_evidence_import_jobs() -> list[ManualEvidenceImportJob]:
    root = _ensure_root()
    jobs: list[ManualEvidenceImportJob] = []
    for path in sorted((root / "import_jobs").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            jobs.append(ManualEvidenceImportJob.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return jobs


def create_manual_evidence_import_job(
    request_id: str,
    payload: ManualEvidenceImportJobCreate | dict[str, Any] | None = None,
) -> ManualEvidenceImportJob:
    try:
        job_payload = (
            payload
            if isinstance(payload, ManualEvidenceImportJobCreate)
            else ManualEvidenceImportJobCreate.model_validate(payload or {})
        )
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create manual import job draft: invalid job payload ({exc}).") from exc

    decision = _select_review_decision_for_import_job(request_id, job_payload.decision_id)
    _validate_import_job_decision_eligibility(decision)
    preview = read_evidence_import_preview(request_id)
    _validate_import_job_preview_eligibility(preview)

    target_case_mode = job_payload.target_case_mode or decision.target_case_mode
    if target_case_mode not in {"new_review_case", "existing_case"}:
        raise AnalysisRequestValidationError("Cannot create manual import job draft: target_case_mode must be new_review_case or existing_case.")
    target_case_id = job_payload.target_case_id or decision.target_case_id
    if target_case_mode == "existing_case" and not target_case_id:
        raise AnalysisRequestValidationError("Cannot create manual import job draft: target_case_id is required for existing_case.")

    job_id = _new_import_job_id()
    job = ManualEvidenceImportJob(
        job_id=job_id,
        decision_id=decision.decision_id,
        preview_id=preview.preview_id,
        plan_id=preview.plan_id,
        draft_id=preview.draft_id,
        request_id=request_id,
        created_by=job_payload.created_by or "sentigraph_local_ui",
        target_case=ManualEvidenceImportTargetCase(
            mode=target_case_mode,
            target_case_id=target_case_id,
            create_case_now=False,
        ),
        package_reference=preview.package_reference,
        metadata_summary=preview.metadata_summary,
        approved_defaults=decision.approved_defaults,
        preflight_checks=ManualEvidenceImportPreflightChecks(
            approved_import_decision_present=True,
            coverage_acknowledged=decision.checklist.coverage_reviewed,
            validation_acknowledged=decision.checklist.validation_reviewed,
            privacy_acknowledged=decision.checklist.privacy_reviewed,
            no_raw_author_identifiers_acknowledged=decision.checklist.no_raw_author_identifiers,
            not_full_web_acknowledged=decision.checklist.not_full_web_acknowledged,
            not_full_platform_acknowledged=decision.checklist.not_full_platform_acknowledged,
            not_full_thread_acknowledged=decision.checklist.not_full_thread_acknowledged,
            review_needed_default_acknowledged=decision.checklist.review_needed_default_acknowledged,
            trust_label_default_acknowledged=decision.checklist.trust_label_default_acknowledged,
            dedup_required_acknowledged=decision.checklist.dedup_required_acknowledged,
            no_auto_analysis_acknowledged=decision.checklist.no_auto_analysis_acknowledged,
            no_auto_report_acknowledged=decision.checklist.no_auto_report_acknowledged,
        ),
        readiness=ManualEvidenceImportJobReadiness(
            state="ready_for_future_manual_import_execution",
            can_execute_now=False,
            requires_separate_import_phase=True,
            reason="Dry-run gate only. Evidence rows are not imported in Phase 6I.",
        ),
        blockers=[],
        boundary_notes=[
            "Job draft is not import.",
            "Dry-run gate does not read evidence rows.",
            "Dry-run gate does not create a production case.",
            "Dry-run gate does not run dedup, create review queue items, run analysis, or generate reports.",
            "Future phase must explicitly execute manual import after another review.",
            "Provider output remains evidence, not official truth.",
        ],
        recommended_next_steps=[
            "Future Phase 6J may implement manual import execution against a review-only case.",
            "Import execution must read rows only in the execution phase.",
            "Dedup and review queue must run before analysis.",
            "Analysis, Sandbox, public event, and report generation are later explicit actions only.",
            "If package is limited sample, do not present it as broad coverage.",
        ],
    )
    _write_json(_import_job_path(request_id, job_id), job.model_dump(mode="json", by_alias=True))
    return read_manual_evidence_import_job(request_id, job_id)


def read_manual_evidence_import_execution_preflight(
    request_id: str,
    preflight_id: str,
) -> ManualEvidenceImportExecutionPreflight:
    preflight_path = _execution_preflight_path(request_id, preflight_id)
    if not preflight_path.exists():
        raise AnalysisRequestNotFoundError(f"Manual evidence import execution preflight {preflight_id} for {request_id} was not found.")
    try:
        parsed = json.loads(preflight_path.read_text(encoding="utf-8-sig"))
        return ManualEvidenceImportExecutionPreflight.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{preflight_path.name} is not a valid execution preflight: {type(exc).__name__}") from exc


def list_manual_evidence_import_execution_preflights(request_id: str) -> list[ManualEvidenceImportExecutionPreflight]:
    _validate_request_id(request_id)
    root = _ensure_root()
    preflights: list[ManualEvidenceImportExecutionPreflight] = []
    for path in sorted((root / "execution_preflights").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            preflights.append(ManualEvidenceImportExecutionPreflight.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return preflights


def list_all_manual_evidence_import_execution_preflights() -> list[ManualEvidenceImportExecutionPreflight]:
    root = _ensure_root()
    preflights: list[ManualEvidenceImportExecutionPreflight] = []
    for path in sorted((root / "execution_preflights").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            preflights.append(ManualEvidenceImportExecutionPreflight.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return preflights


def create_manual_evidence_import_execution_preflight(
    request_id: str,
    payload: ManualEvidenceImportExecutionPreflightCreate | dict[str, Any] | None = None,
) -> ManualEvidenceImportExecutionPreflight:
    try:
        preflight_payload = (
            payload
            if isinstance(payload, ManualEvidenceImportExecutionPreflightCreate)
            else ManualEvidenceImportExecutionPreflightCreate.model_validate(payload or {})
        )
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create execution preflight: invalid preflight payload ({exc}).") from exc

    job = _select_manual_import_job_for_preflight(request_id, preflight_payload.job_id)
    _validate_execution_preflight_job_eligibility(job)
    decision = read_evidence_import_review_decision(request_id, job.decision_id)
    _validate_execution_preflight_decision_eligibility(request_id, decision, job)
    preview = read_evidence_import_preview(request_id)
    _validate_execution_preflight_preview_eligibility(preview)
    package_file_checks, file_warnings = _build_execution_preflight_package_file_checks(job.package_reference)

    if job.target_case.mode not in {"new_review_case", "existing_case"}:
        raise AnalysisRequestValidationError("Cannot create execution preflight: target_case mode must be new_review_case or existing_case.")
    if job.target_case.mode == "existing_case" and not job.target_case.target_case_id:
        raise AnalysisRequestValidationError("Cannot create execution preflight: target_case_id is required for existing_case.")

    preflight_id = _new_execution_preflight_id()
    status = "preflight_warn" if file_warnings else "preflight_passed"
    preflight = ManualEvidenceImportExecutionPreflight(
        preflight_id=preflight_id,
        job_id=job.job_id,
        decision_id=job.decision_id,
        preview_id=job.preview_id,
        plan_id=job.plan_id,
        draft_id=job.draft_id,
        request_id=request_id,
        created_by=preflight_payload.created_by or "sentigraph_local_ui",
        status=status,
        package_reference=job.package_reference,
        package_file_checks=package_file_checks,
        metadata_summary=preview.metadata_summary,
        validation_summary=preview.validation_summary,
        coverage_summary=preview.coverage_summary,
        privacy_summary=preview.privacy_summary,
        target_case_preflight=ManualEvidenceImportTargetCasePreflight(
            mode=job.target_case.mode,
            target_case_id=job.target_case.target_case_id,
            create_case_now=False,
            review_only_required=True,
            analysis_included_default=False,
        ),
        future_row_reader_plan=ManualEvidenceImportFutureRowReaderPlan(
            would_read_rows_in_future_phase=True,
            read_rows_now=False,
            streaming_required=True,
            max_rows_first_mvp=100,
            fail_closed_on_privacy_violation=True,
        ),
        future_staging_plan=ManualEvidenceImportFutureStagingPlan(
            would_stage_rows_in_future_phase=True,
            stage_rows_now=False,
            default_review_status="review_needed",
            default_verification_status="source_url_provided_unverified",
            default_trust_label="medium_low",
            analysis_included=False,
        ),
        future_governance_plan=ManualEvidenceImportFutureGovernancePlan(
            dedup_required=True,
            dedup_run_now=False,
            review_queue_required=True,
            review_queue_created_now=False,
            audit_required=True,
            rollback_required=True,
        ),
        blockers=[],
        warnings=file_warnings,
        readiness=ManualEvidenceImportExecutionPreflightReadiness(
            state="ready_for_future_manual_import_execution" if not file_warnings else "needs_attention",
            can_execute_now=False,
            requires_separate_execution_phase=True,
            reason="Preflight only. Evidence rows are not imported in Phase 6K.",
        ),
        boundary_notes=[
            "Preflight is not import.",
            "Preflight does not open, read, or parse evidence row files.",
            "Preflight does not create a production case.",
            "Preflight does not write to the Evidence Layer.",
            "Preflight does not run dedup or create review queue items.",
            "Preflight does not run analysis or generate Sandbox/public event/report output.",
            "Future execution phase must be separate.",
            "Provider output remains evidence, not truth.",
        ],
        recommended_next_steps=[
            "Future Phase 6L may implement row reader dry-run with synthetic fixture only.",
            "Future Phase 6M may implement staging import to a review-only case.",
            "Import rows only in a separate manual execution phase.",
            "Dedup and review queue must run before analysis.",
            "Analysis, Sandbox, public event, and report generation are later explicit actions only.",
        ],
    )
    _write_json(_execution_preflight_path(request_id, preflight_id), preflight.model_dump(mode="json", by_alias=True))
    return read_manual_evidence_import_execution_preflight(request_id, preflight_id)


def read_evidence_row_reader_dry_run(request_id: str, dry_run_id: str) -> EvidenceRowReaderDryRun:
    dry_run_path = _row_reader_dry_run_path(request_id, dry_run_id)
    if not dry_run_path.exists():
        raise AnalysisRequestNotFoundError(f"Evidence row reader dry-run {dry_run_id} for {request_id} was not found.")
    try:
        parsed = json.loads(dry_run_path.read_text(encoding="utf-8-sig"))
        return EvidenceRowReaderDryRun.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{dry_run_path.name} is not a valid row reader dry-run: {type(exc).__name__}") from exc


def list_evidence_row_reader_dry_runs(request_id: str) -> list[EvidenceRowReaderDryRun]:
    _validate_request_id(request_id)
    root = _ensure_root()
    dry_runs: list[EvidenceRowReaderDryRun] = []
    for path in sorted((root / "row_reader_dry_runs").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            dry_runs.append(EvidenceRowReaderDryRun.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return dry_runs


def list_all_evidence_row_reader_dry_runs() -> list[EvidenceRowReaderDryRun]:
    root = _ensure_root()
    dry_runs: list[EvidenceRowReaderDryRun] = []
    for path in sorted((root / "row_reader_dry_runs").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            dry_runs.append(EvidenceRowReaderDryRun.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return dry_runs


def read_real_package_row_preview(request_id: str, preview_run_id: str) -> RealPackageRowPreview:
    preview_path = _real_package_row_preview_path(request_id, preview_run_id)
    if not preview_path.exists():
        raise AnalysisRequestNotFoundError(f"Real package row preview {preview_run_id} for {request_id} was not found.")
    try:
        parsed = json.loads(preview_path.read_text(encoding="utf-8-sig"))
        return RealPackageRowPreview.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{preview_path.name} is not a valid real package row preview: {type(exc).__name__}") from exc


def list_real_package_row_previews(request_id: str) -> list[RealPackageRowPreview]:
    _validate_request_id(request_id)
    root = _ensure_root()
    previews: list[RealPackageRowPreview] = []
    for path in sorted((root / "real_package_row_previews").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            previews.append(RealPackageRowPreview.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return previews


def list_all_real_package_row_previews() -> list[RealPackageRowPreview]:
    root = _ensure_root()
    previews: list[RealPackageRowPreview] = []
    for path in sorted((root / "real_package_row_previews").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            previews.append(RealPackageRowPreview.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return previews


def read_review_only_case(request_id: str, review_case_id: str) -> ReviewOnlyCase:
    review_case_path = _review_only_case_path(request_id, review_case_id)
    if not review_case_path.exists():
        raise AnalysisRequestNotFoundError(f"Review-only case {review_case_id} for {request_id} was not found.")
    try:
        parsed = json.loads(review_case_path.read_text(encoding="utf-8-sig"))
        return ReviewOnlyCase.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{review_case_path.name} is not a valid review-only case: {type(exc).__name__}") from exc


def list_review_only_cases(request_id: str) -> list[ReviewOnlyCase]:
    _validate_request_id(request_id)
    root = _ensure_root()
    review_cases: list[ReviewOnlyCase] = []
    for path in sorted((root / "review_only_cases").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            review_cases.append(ReviewOnlyCase.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return review_cases


def list_all_review_only_cases() -> list[ReviewOnlyCase]:
    root = _ensure_root()
    review_cases: list[ReviewOnlyCase] = []
    for path in sorted((root / "review_only_cases").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            review_cases.append(ReviewOnlyCase.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return review_cases


def read_review_only_case_staging_import(request_id: str, staging_import_id: str) -> ReviewOnlyCaseStagingImport:
    staging_path = _staging_import_path(request_id, staging_import_id)
    if not staging_path.exists():
        raise AnalysisRequestNotFoundError(f"Review-only staging import {staging_import_id} for {request_id} was not found.")
    try:
        parsed = json.loads(staging_path.read_text(encoding="utf-8-sig"))
        return ReviewOnlyCaseStagingImport.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{staging_path.name} is not a valid review-only staging import: {type(exc).__name__}") from exc


def list_review_only_case_staging_imports(request_id: str) -> list[ReviewOnlyCaseStagingImport]:
    _validate_request_id(request_id)
    root = _ensure_root()
    imports: list[ReviewOnlyCaseStagingImport] = []
    for path in sorted((root / "staging_imports").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            imports.append(ReviewOnlyCaseStagingImport.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return imports


def list_all_review_only_case_staging_imports() -> list[ReviewOnlyCaseStagingImport]:
    root = _ensure_root()
    imports: list[ReviewOnlyCaseStagingImport] = []
    for path in sorted((root / "staging_imports").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            imports.append(ReviewOnlyCaseStagingImport.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return imports


def read_staged_evidence_candidate_batch(request_id: str, staging_import_id: str) -> StagedEvidenceCandidateBatch:
    batch_path = _staged_candidate_batch_path(request_id, staging_import_id)
    if not batch_path.exists():
        raise AnalysisRequestNotFoundError(f"Staged evidence candidate batch {staging_import_id} for {request_id} was not found.")
    try:
        parsed = json.loads(batch_path.read_text(encoding="utf-8-sig"))
        return StagedEvidenceCandidateBatch.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{batch_path.name} is not a valid staged evidence candidate batch: {type(exc).__name__}") from exc


def read_review_queue_initialization(request_id: str, queue_init_id: str) -> ReviewQueueInitialization:
    init_path = _review_queue_initialization_path(request_id, queue_init_id)
    if not init_path.exists():
        raise AnalysisRequestNotFoundError(f"Review queue initialization {queue_init_id} for {request_id} was not found.")
    try:
        parsed = json.loads(init_path.read_text(encoding="utf-8-sig"))
        return ReviewQueueInitialization.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{init_path.name} is not a valid review queue initialization: {type(exc).__name__}") from exc


def list_review_queue_initializations(request_id: str) -> list[ReviewQueueInitialization]:
    _validate_request_id(request_id)
    root = _ensure_root()
    initializations: list[ReviewQueueInitialization] = []
    for path in sorted((root / "review_queue_initializations").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            initializations.append(ReviewQueueInitialization.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return initializations


def list_all_review_queue_initializations() -> list[ReviewQueueInitialization]:
    root = _ensure_root()
    initializations: list[ReviewQueueInitialization] = []
    for path in sorted((root / "review_queue_initializations").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            initializations.append(ReviewQueueInitialization.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return initializations


def read_review_queue_item_batch(request_id: str, queue_init_id: str) -> ReviewQueueItemBatch:
    batch_path = _review_queue_item_batch_path(request_id, queue_init_id)
    if not batch_path.exists():
        raise AnalysisRequestNotFoundError(f"Review queue item batch {queue_init_id} for {request_id} was not found.")
    try:
        parsed = json.loads(batch_path.read_text(encoding="utf-8-sig"))
        return ReviewQueueItemBatch.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{batch_path.name} is not a valid review queue item batch: {type(exc).__name__}") from exc


def read_review_queue_action_audit(request_id: str, audit_id: str) -> ReviewQueueActionAudit:
    matches = list((_ensure_root() / "review_queue_action_audits").glob(f"{request_id}_*_{audit_id}.json"))
    if not matches:
        raise AnalysisRequestNotFoundError(f"Review queue action audit {audit_id} for {request_id} was not found.")
    try:
        parsed = json.loads(matches[0].read_text(encoding="utf-8-sig"))
        return ReviewQueueActionAudit.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{matches[0].name} is not a valid review queue action audit: {type(exc).__name__}") from exc


def list_review_queue_action_audits(request_id: str) -> list[ReviewQueueActionAudit]:
    _validate_request_id(request_id)
    root = _ensure_root()
    audits: list[ReviewQueueActionAudit] = []
    for path in sorted((root / "review_queue_action_audits").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            audits.append(ReviewQueueActionAudit.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return audits


def list_all_review_queue_action_audits() -> list[ReviewQueueActionAudit]:
    root = _ensure_root()
    audits: list[ReviewQueueActionAudit] = []
    for path in sorted((root / "review_queue_action_audits").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            audits.append(ReviewQueueActionAudit.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return audits


def read_review_queue_action_audits_for_item(request_id: str, review_item_id: str) -> list[ReviewQueueActionAudit]:
    return [audit for audit in list_review_queue_action_audits(request_id) if audit.review_item_id == review_item_id]


def read_review_queue_completion_gate(request_id: str, completion_gate_id: str) -> ReviewQueueCompletionGate:
    gate_path = _review_queue_completion_gate_path(request_id, completion_gate_id)
    if not gate_path.exists():
        raise AnalysisRequestNotFoundError(f"Review queue completion gate {completion_gate_id} for {request_id} was not found.")
    try:
        parsed = json.loads(gate_path.read_text(encoding="utf-8-sig"))
        return ReviewQueueCompletionGate.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{gate_path.name} is not a valid review queue completion gate: {type(exc).__name__}") from exc


def list_review_queue_completion_gates(request_id: str) -> list[ReviewQueueCompletionGate]:
    _validate_request_id(request_id)
    root = _ensure_root()
    gates: list[ReviewQueueCompletionGate] = []
    for path in sorted((root / "review_queue_completion_gates").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            gates.append(ReviewQueueCompletionGate.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return gates


def list_all_review_queue_completion_gates() -> list[ReviewQueueCompletionGate]:
    root = _ensure_root()
    gates: list[ReviewQueueCompletionGate] = []
    for path in sorted((root / "review_queue_completion_gates").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            gates.append(ReviewQueueCompletionGate.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return gates


def read_dedup_preview(request_id: str, dedup_preview_id: str) -> DedupPreview:
    preview_path = _dedup_preview_path(request_id, dedup_preview_id)
    if not preview_path.exists():
        raise AnalysisRequestNotFoundError(f"Dedup preview {dedup_preview_id} for {request_id} was not found.")
    try:
        parsed = json.loads(preview_path.read_text(encoding="utf-8-sig"))
        return DedupPreview.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{preview_path.name} is not a valid dedup preview: {type(exc).__name__}") from exc


def list_dedup_previews(request_id: str) -> list[DedupPreview]:
    _validate_request_id(request_id)
    root = _ensure_root()
    previews: list[DedupPreview] = []
    for path in sorted((root / "dedup_previews").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            previews.append(DedupPreview.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return previews


def list_all_dedup_previews() -> list[DedupPreview]:
    root = _ensure_root()
    previews: list[DedupPreview] = []
    for path in sorted((root / "dedup_previews").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            previews.append(DedupPreview.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return previews


def list_dedup_group_review_audits(request_id: str) -> list[DedupGroupReviewAudit]:
    _validate_request_id(request_id)
    root = _ensure_root()
    audits: list[DedupGroupReviewAudit] = []
    for path in sorted((root / "dedup_group_review_audits").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            audits.append(DedupGroupReviewAudit.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return audits


def list_all_dedup_group_review_audits() -> list[DedupGroupReviewAudit]:
    root = _ensure_root()
    audits: list[DedupGroupReviewAudit] = []
    for path in sorted((root / "dedup_group_review_audits").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            audits.append(DedupGroupReviewAudit.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return audits


def read_dedup_group_review_audits_for_group(
    request_id: str,
    dedup_preview_id: str,
    group_candidate_id: str,
) -> list[DedupGroupReviewAudit]:
    return [
        audit
        for audit in list_dedup_group_review_audits(request_id)
        if audit.dedup_preview_id == dedup_preview_id and audit.group_candidate_id == group_candidate_id
    ]


def read_analysis_ready_promotion_gate(request_id: str, promotion_gate_id: str) -> AnalysisReadyPromotionGate:
    gate_path = _analysis_ready_promotion_gate_path(request_id, promotion_gate_id)
    if not gate_path.exists():
        raise AnalysisRequestNotFoundError(f"Analysis-ready promotion gate {promotion_gate_id} for {request_id} was not found.")
    try:
        parsed = json.loads(gate_path.read_text(encoding="utf-8-sig"))
        return AnalysisReadyPromotionGate.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{gate_path.name} is not a valid analysis-ready promotion gate: {type(exc).__name__}") from exc


def list_analysis_ready_promotion_gates(request_id: str) -> list[AnalysisReadyPromotionGate]:
    _validate_request_id(request_id)
    root = _ensure_root()
    gates: list[AnalysisReadyPromotionGate] = []
    for path in sorted((root / "analysis_ready_promotion_gates").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            gates.append(AnalysisReadyPromotionGate.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return gates


def list_all_analysis_ready_promotion_gates() -> list[AnalysisReadyPromotionGate]:
    root = _ensure_root()
    gates: list[AnalysisReadyPromotionGate] = []
    for path in sorted((root / "analysis_ready_promotion_gates").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            gates.append(AnalysisReadyPromotionGate.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return gates


def list_promotion_decision_audits(request_id: str) -> list[PromotionDecisionAudit]:
    _validate_request_id(request_id)
    root = _ensure_root()
    audits: list[PromotionDecisionAudit] = []
    for path in sorted((root / "promotion_decision_audits").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            audits.append(PromotionDecisionAudit.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return audits


def list_all_promotion_decision_audits() -> list[PromotionDecisionAudit]:
    root = _ensure_root()
    audits: list[PromotionDecisionAudit] = []
    for path in sorted((root / "promotion_decision_audits").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            audits.append(PromotionDecisionAudit.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return audits


def list_promotion_decision_audits_for_gate(request_id: str, promotion_gate_id: str) -> list[PromotionDecisionAudit]:
    return [
        audit
        for audit in list_promotion_decision_audits(request_id)
        if audit.promotion_gate_id == promotion_gate_id
    ]


def read_manual_analysis_trigger(request_id: str, manual_trigger_id: str) -> ManualAnalysisTrigger:
    trigger_path = _manual_analysis_trigger_path(request_id, manual_trigger_id)
    if not trigger_path.exists():
        raise AnalysisRequestNotFoundError(f"Manual analysis trigger {manual_trigger_id} for {request_id} was not found.")
    try:
        parsed = json.loads(trigger_path.read_text(encoding="utf-8-sig"))
        return ManualAnalysisTrigger.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{trigger_path.name} is not a valid manual analysis trigger: {type(exc).__name__}") from exc


def list_manual_analysis_triggers(request_id: str) -> list[ManualAnalysisTrigger]:
    _validate_request_id(request_id)
    root = _ensure_root()
    triggers: list[ManualAnalysisTrigger] = []
    for path in sorted((root / "manual_analysis_triggers").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            triggers.append(ManualAnalysisTrigger.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return triggers


def list_all_manual_analysis_triggers() -> list[ManualAnalysisTrigger]:
    root = _ensure_root()
    triggers: list[ManualAnalysisTrigger] = []
    for path in sorted((root / "manual_analysis_triggers").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            triggers.append(ManualAnalysisTrigger.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return triggers


def list_manual_analysis_trigger_audits(request_id: str) -> list[ManualAnalysisTriggerAudit]:
    _validate_request_id(request_id)
    root = _ensure_root()
    audits: list[ManualAnalysisTriggerAudit] = []
    for path in sorted((root / "manual_analysis_trigger_audits").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            audits.append(ManualAnalysisTriggerAudit.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return audits


def list_all_manual_analysis_trigger_audits() -> list[ManualAnalysisTriggerAudit]:
    root = _ensure_root()
    audits: list[ManualAnalysisTriggerAudit] = []
    for path in sorted((root / "manual_analysis_trigger_audits").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            audits.append(ManualAnalysisTriggerAudit.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return audits


def list_manual_analysis_trigger_audits_for_trigger(request_id: str, manual_trigger_id: str) -> list[ManualAnalysisTriggerAudit]:
    return [
        audit
        for audit in list_manual_analysis_trigger_audits(request_id)
        if audit.manual_trigger_id == manual_trigger_id
    ]


def create_evidence_row_reader_dry_run(
    request_id: str,
    payload: EvidenceRowReaderDryRunCreate | dict[str, Any] | None = None,
) -> EvidenceRowReaderDryRun:
    try:
        dry_run_payload = (
            payload
            if isinstance(payload, EvidenceRowReaderDryRunCreate)
            else EvidenceRowReaderDryRunCreate.model_validate(payload or {})
        )
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create row reader dry-run: invalid dry-run payload ({exc}).") from exc

    preflight = _select_execution_preflight_for_row_reader(request_id, dry_run_payload.preflight_id)
    _validate_row_reader_preflight_eligibility(preflight)
    _validate_row_reader_payload(dry_run_payload)
    fixture_path = _resolve_row_reader_fixture_path(dry_run_payload)
    accepted_rows, quarantine_summary, rejection_summary, counts, privacy_scan = _read_synthetic_fixture_rows(
        fixture_path,
        dry_run_payload.max_rows,
    )
    status = "warn" if counts.quarantined or counts.rejected or privacy_scan.privacy_stop_triggered else "passed"
    warnings: list[str] = []
    if counts.quarantined:
        warnings.append("One or more synthetic fixture rows were quarantined because forbidden fields were detected.")
    if counts.rejected:
        warnings.append("One or more synthetic fixture rows were rejected because JSON parsing failed.")
    if counts.rows_seen >= dry_run_payload.max_rows:
        warnings.append("Synthetic fixture row reader stopped at max_rows limit.")

    dry_run_id = _new_row_reader_dry_run_id()
    dry_run = EvidenceRowReaderDryRun(
        dry_run_id=dry_run_id,
        preflight_id=preflight.preflight_id,
        job_id=preflight.job_id,
        decision_id=preflight.decision_id,
        preview_id=preflight.preview_id,
        plan_id=preflight.plan_id,
        draft_id=preflight.draft_id,
        request_id=request_id,
        created_by=dry_run_payload.created_by or "sentigraph_local_ui",
        status=status,
        fixture_policy=EvidenceRowReaderFixturePolicy(max_rows=dry_run_payload.max_rows),
        row_source=EvidenceRowReaderRowSource(
            source_type="synthetic_fixture",
            source_name=dry_run_payload.fixture_name,
            source_path=str(fixture_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            real_package_path_used=False,
        ),
        counts=counts,
        privacy_scan=privacy_scan,
        redacted_preview_rows=accepted_rows,
        quarantine_summary=quarantine_summary,
        rejection_summary=rejection_summary,
        governance_defaults=EvidenceRowReaderGovernanceDefaults(),
        now_flags=EvidenceRowReaderNowFlags(),
        readiness=EvidenceRowReaderReadiness(
            state="ready_for_future_real_package_row_preview" if status == "passed" else "warn",
            can_import_now=False,
            requires_future_phase=True,
            reason="Synthetic fixture dry-run only. No real provider package rows were read.",
        ),
        blockers=[],
        warnings=warnings,
        boundary_notes=[
            "Synthetic fixture row reader dry-run only.",
            "Real provider package rows are not read.",
            "External collector package rows are not read.",
            "Evidence rows are not imported.",
            "Redacted preview rows are not analysis input.",
            "Quarantined rows are not imported.",
            "Invalid rows are rejected without crashing.",
            "Future real package row preview requires a separate phase.",
        ],
        recommended_next_steps=[
            "Review quarantine and rejection summaries before designing real package row preview.",
            "Keep review_needed/source_url_provided_unverified/medium_low defaults for future staged rows.",
            "Do not run analysis until rows are staged, deduped, reviewed, and explicitly included.",
        ],
    )
    _write_json(_row_reader_dry_run_path(request_id, dry_run_id), dry_run.model_dump(mode="json", by_alias=True))
    return read_evidence_row_reader_dry_run(request_id, dry_run_id)


def create_real_package_row_preview(
    request_id: str,
    payload: RealPackageRowPreviewCreate | dict[str, Any] | None = None,
) -> RealPackageRowPreview:
    try:
        preview_payload = (
            payload
            if isinstance(payload, RealPackageRowPreviewCreate)
            else RealPackageRowPreviewCreate.model_validate(payload or {})
        )
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create real package row preview: invalid payload ({exc}).") from exc

    preflight = _select_execution_preflight_for_row_reader(request_id, preview_payload.preflight_id)
    _validate_real_package_preview_preflight_eligibility(preflight)
    _validate_real_package_preview_payload(preview_payload)
    _validate_real_package_preview_review_decision(request_id, preflight)
    _validate_real_package_preview_job(preflight)
    _validate_real_package_preview_synthetic_dry_run(request_id)
    package_path = _resolve_real_package_preview_package_path(preflight)
    _validate_real_package_preview_package_files(package_path, preflight)

    accepted_rows, quarantine_summary, rejection_summary, rows, privacy_scan = _read_real_package_preview_rows(
        package_path / "evidence_items.jsonl",
        preview_payload.max_rows,
    )

    status = "passed"
    readiness_state = "ready_for_future_staging_import_design"
    warnings: list[str] = []
    recommended_next_steps = [
        "Reviewer may inspect redacted preview rows.",
        "Future staging import still requires a separate phase and decision.",
    ]
    if privacy_scan.privacy_stop_triggered:
        status = "privacy_stop"
        readiness_state = "privacy_stop"
        warnings.append("Privacy stop triggered; future staging import is blocked until privacy/security review.")
        recommended_next_steps = ["Privacy/security review required before any future staging import design."]
    elif rows.quarantined or rows.rejected:
        status = "warn"
        warnings.append("Some preview rows were quarantined or rejected; inspect summaries before any future phase.")
    if rows.rows_seen >= preview_payload.max_rows:
        warnings.append("Real package row preview stopped at max_rows limit.")

    manifest_payload = _read_safe_json_file(package_path / "manifest.json")
    preview_run_id = _new_real_package_row_preview_id()
    preview = RealPackageRowPreview(
        preview_run_id=preview_run_id,
        preflight_id=preflight.preflight_id,
        import_job_id=preflight.job_id,
        decision_id=preflight.decision_id,
        preview_id=preflight.preview_id,
        plan_id=preflight.plan_id,
        draft_id=preflight.draft_id,
        request_id=request_id,
        created_by=preview_payload.created_by or "sentigraph_local_ui",
        status=status,
        package_reference=RealPackageRowPreviewPackageReference(
            package_name=str(manifest_payload.get("package_name") or preflight.package_reference.package_name or package_path.name),
            package_role=str(manifest_payload.get("package_role") or preflight.package_reference.package_role or "selected_public_sample"),
            package_path=str(package_path),
            package_hash=None,
            manifest_hash=_safe_file_sha256(package_path / "manifest.json"),
        ),
        limits=RealPackageRowPreviewLimits(max_rows=preview_payload.max_rows),
        rows=rows,
        privacy_scan=privacy_scan,
        redacted_preview_rows=accepted_rows,
        quarantine_summary=quarantine_summary,
        rejection_summary=rejection_summary,
        governance_defaults=EvidenceRowReaderGovernanceDefaults(),
        now_flags=EvidenceRowReaderNowFlags(),
        readiness=RealPackageRowPreviewReadiness(state=readiness_state),
        warnings=warnings,
        boundary_notes=[
            "Real package row preview only; evidence rows are not imported.",
            "Preview rows are redacted and not representative of full package coverage.",
            "Provider output is evidence, not truth.",
            "No case, review queue, dedup, analysis, Sandbox, public event, or report is generated.",
        ],
        recommended_next_steps=recommended_next_steps,
    )
    _write_json(_real_package_row_preview_path(request_id, preview_run_id), preview.model_dump(mode="json", by_alias=True))
    return read_real_package_row_preview(request_id, preview_run_id)


def create_review_only_case(
    request_id: str,
    payload: ReviewOnlyCaseCreate | dict[str, Any] | None = None,
) -> ReviewOnlyCase:
    try:
        review_case_payload = (
            payload
            if isinstance(payload, ReviewOnlyCaseCreate)
            else ReviewOnlyCaseCreate.model_validate(payload or {})
        )
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create review-only case: invalid payload ({exc}).") from exc

    _validate_review_only_case_payload(review_case_payload)
    preview = _select_review_only_case_preview(request_id, review_case_payload.source_preview_run_id)
    preflight = read_manual_evidence_import_execution_preflight(request_id, preview.preflight_id)
    job = read_manual_evidence_import_job(request_id, preview.import_job_id)
    _validate_review_only_case_eligibility(request_id, preview, preflight, job)

    review_case_id = _new_review_only_case_id()
    created_at = datetime.now(timezone.utc)
    review_case = ReviewOnlyCase(
        review_case_id=review_case_id,
        request_id=request_id,
        source_import_job_id=preview.import_job_id,
        source_preview_run_id=preview.preview_run_id,
        source_preflight_id=preview.preflight_id,
        created_at=created_at,
        created_by=review_case_payload.created_by or "sentigraph_local_ui",
        status="staging_pending",
        package_reference=preview.package_reference,
        source_preview_summary=ReviewOnlyCaseSourcePreviewSummary(
            preview_run_id=preview.preview_run_id,
            status=preview.status,
            rows_seen=preview.rows.rows_seen,
            accepted_for_preview=preview.rows.accepted_for_preview,
            quarantined=preview.rows.quarantined,
            rejected=preview.rows.rejected,
            privacy_stop_triggered=preview.privacy_scan.privacy_stop_triggered,
        ),
        coverage=preflight.coverage_summary,
        governance_defaults=ReviewOnlyCaseGovernanceDefaults(),
        target_case_reference=ReviewOnlyCaseTargetReference(
            mode=review_case_payload.target_case_mode,
            target_case_id=review_case_payload.target_case_id,
            attach_to_production_case_now=False,
        ),
        allowed_actions=[
            "inspect package metadata",
            "inspect limited redacted preview",
            "prepare future staging import",
            "view coverage / validation / privacy notes",
            "create future staging import design/action after another phase",
        ],
        blocked_actions=[
            "import evidence rows now",
            "write Evidence Layer now",
            "create production case now",
            "create review queue now",
            "run dedup now",
            "run analysis now",
            "generate Sandbox now",
            "generate public event now",
            "generate B-end report now",
            "run Strategy Lab now",
        ],
        promotion_requirements=[
            "future staging import completed",
            "review queue initialized and completed or threshold met",
            "dedup completed",
            "rejected evidence excluded",
            "weak evidence marked",
            "coverage acknowledged",
            "audit complete",
            "no privacy blockers",
            "separate promotion decision",
        ],
        readiness=ReviewOnlyCaseReadiness(),
        boundary_notes=[
            "Review-only case is not a production case.",
            "Evidence rows are not imported.",
            "Analysis, Sandbox, public event, and report generation remain disabled.",
            "Provider output is evidence, not truth.",
            "Package validation is structural/safety/coverage metadata, not official verification.",
            "Coverage remains selected sample only; do not claim full-web, full-platform, or full-thread coverage.",
        ],
        recommended_next_steps=[
            "Design future staging import before moving beyond this container.",
            "Keep review_needed/source_url_provided_unverified/medium_low defaults.",
            "Do not run analysis until future staging, review, dedup, audit, and promotion gates are complete.",
        ],
        audit=ReviewOnlyCaseAudit(
            created_by=review_case_payload.created_by or "sentigraph_local_ui",
            created_at=created_at,
            source="limited_real_package_row_preview",
        ),
    )
    _write_json(_review_only_case_path(request_id, review_case_id), review_case.model_dump(mode="json", by_alias=True))
    return read_review_only_case(request_id, review_case_id)


def create_review_only_case_staging_import(
    request_id: str,
    payload: ReviewOnlyCaseStagingImportCreate | dict[str, Any] | None = None,
) -> ReviewOnlyCaseStagingImport:
    try:
        staging_payload = (
            payload
            if isinstance(payload, ReviewOnlyCaseStagingImportCreate)
            else ReviewOnlyCaseStagingImportCreate.model_validate(payload or {})
        )
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create review-only staging import: invalid payload ({exc}).") from exc

    _validate_staging_import_payload(staging_payload)
    review_case = _select_staging_import_review_case(request_id, staging_payload.review_case_id)
    preview = _select_staging_import_preview(request_id, review_case, staging_payload.preview_run_id)
    _validate_staging_import_eligibility(request_id, review_case, preview)

    staging_import_id = _new_staging_import_id()
    created_at = datetime.now(timezone.utc)
    candidates = [
        _candidate_from_redacted_preview_row(
            row,
            staging_import_id=staging_import_id,
            review_case=review_case,
            preview=preview,
            created_at=created_at,
        )
        for row in preview.redacted_preview_rows
        if row.status == "accepted_for_preview" and row.privacy_check.passed
    ]
    if not candidates:
        raise AnalysisRequestValidationError("Cannot create review-only staging import: no accepted redacted preview rows are available.")

    status = "completed"
    warnings: list[str] = []
    if preview.rows.quarantined or preview.rows.rejected:
        status = "partial"
        warnings.append("Some preview rows were quarantined or rejected and were not staged.")

    staging_import = ReviewOnlyCaseStagingImport(
        staging_import_id=staging_import_id,
        review_case_id=review_case.review_case_id,
        request_id=request_id,
        package_name=preview.package_reference.package_name,
        source_preview_run_id=preview.preview_run_id,
        source_import_job_id=preview.import_job_id,
        created_at=created_at,
        created_by=staging_payload.created_by or "sentigraph_local_ui",
        status=status,
        counts=ReviewOnlyCaseStagingImportCounts(
            preview_rows_seen=len(preview.redacted_preview_rows),
            accepted_for_staging=len(candidates),
            quarantined_from_staging=preview.rows.quarantined,
            rejected_from_staging=preview.rows.rejected,
            privacy_stop=False,
        ),
        default_governance=ReviewOnlyStagedGovernance(),
        target=ReviewOnlyCaseStagingTarget(
            review_case_id=review_case.review_case_id,
            production_case_id=None,
            production_case_created=False,
            evidence_layer_written=False,
        ),
        rollback=ReviewOnlyCaseStagingRollback(
            rollback_available=True,
            rollback_id=f"rollback_{staging_import_id}",
            rollback_required_before_analysis=True,
        ),
        readiness=ReviewOnlyCaseStagingReadiness(),
        warnings=warnings,
        boundary_notes=[
            "Review-only staging import uses redacted preview rows only.",
            "Original package evidence rows are not re-read.",
            "Staged candidates are not production evidence.",
            "Staged candidates are not analysis-included.",
            "Review queue is not created yet.",
            "Dedup is not run yet.",
            "Reports, Sandbox, public event, and production case generation remain disabled.",
            "Provider output is evidence, not truth.",
        ],
        recommended_next_steps=[
            "Initialize review queue in a future explicit phase.",
            "Run dedup preview before any analysis-ready promotion.",
            "Keep rejected or weak evidence analysis-excluded until governance is complete.",
            "Rollback staged candidates before any unsafe promotion attempt.",
        ],
    )
    candidate_batch = StagedEvidenceCandidateBatch(
        staging_import_id=staging_import_id,
        review_case_id=review_case.review_case_id,
        request_id=request_id,
        created_at=created_at,
        candidates=candidates,
    )
    _write_json(_staging_import_path(request_id, staging_import_id), staging_import.model_dump(mode="json", by_alias=True))
    _write_json(_staged_candidate_batch_path(request_id, staging_import_id), candidate_batch.model_dump(mode="json", by_alias=True))
    return read_review_only_case_staging_import(request_id, staging_import_id)


def create_review_queue_initialization(
    request_id: str,
    payload: ReviewQueueInitializationCreate | dict[str, Any] | None = None,
) -> ReviewQueueInitialization:
    try:
        queue_payload = (
            payload
            if isinstance(payload, ReviewQueueInitializationCreate)
            else ReviewQueueInitializationCreate.model_validate(payload or {})
        )
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create review queue initialization: invalid payload ({exc}).") from exc

    _validate_review_queue_init_payload(queue_payload)
    review_case = _select_review_queue_init_review_case(request_id, queue_payload.review_case_id)
    staging_import = _select_review_queue_init_staging_import(request_id, review_case, queue_payload.staging_import_id)
    candidate_batch = read_staged_evidence_candidate_batch(request_id, staging_import.staging_import_id)
    _validate_review_queue_init_eligibility(request_id, review_case, staging_import, candidate_batch)

    queue_init_id = _new_review_queue_init_id()
    created_at = datetime.now(timezone.utc)
    items = [
        _review_queue_item_from_staged_candidate(
            candidate,
            queue_init_id=queue_init_id,
            created_at=created_at,
            created_by=queue_payload.created_by or "sentigraph_local_ui",
        )
        for candidate in candidate_batch.candidates
        if _staged_candidate_is_queue_eligible(candidate)
    ]
    if not items:
        raise AnalysisRequestValidationError("Cannot create review queue initialization: no eligible staged evidence candidates are available.")

    excluded_candidates = len(candidate_batch.candidates) - len(items)
    status = "completed" if excluded_candidates == 0 else "partial"
    warnings = ["Some staged candidates were excluded from review queue initialization."] if excluded_candidates else []
    queue_init = ReviewQueueInitialization(
        queue_init_id=queue_init_id,
        review_case_id=review_case.review_case_id,
        staging_import_id=staging_import.staging_import_id,
        request_id=request_id,
        package_name=staging_import.package_name,
        created_at=created_at,
        created_by=queue_payload.created_by or "sentigraph_local_ui",
        status=status,
        source=ReviewQueueInitializationSource(staging_import_id=staging_import.staging_import_id),
        counts=ReviewQueueInitializationCounts(
            staged_candidates_seen=len(candidate_batch.candidates),
            queue_items_created=len(items),
            excluded_candidates=excluded_candidates,
            privacy_hold_items=0,
        ),
        defaults=ReviewQueueDefaults(),
        target=ReviewQueueInitializationTarget(
            review_case_id=review_case.review_case_id,
            production_case_id=None,
            production_case_created=False,
            evidence_layer_written=False,
            production_review_queue_created=False,
        ),
        readiness=ReviewQueueInitializationReadiness(),
        warnings=warnings,
        boundary_notes=[
            "Review queue initialization uses staged evidence candidates only.",
            "Original package evidence rows are not re-read.",
            "Review queue items are not production EvidenceItems.",
            "Review queue items are not analysis-included.",
            "Dedup is not run yet.",
            "Reports, Sandbox, public event, and production case generation remain disabled.",
            "Duplicate evidence must not amplify risk.",
            "Provider output is evidence, not official truth.",
        ],
        recommended_next_steps=[
            "Run future review action runtime before dedup.",
            "Keep review_needed/source_url_provided_unverified/medium_low defaults.",
            "Run dedup preview before any analysis-ready promotion.",
            "Keep rejected or weak evidence analysis-excluded until governance is complete.",
        ],
    )
    item_batch = ReviewQueueItemBatch(
        queue_init_id=queue_init_id,
        review_case_id=review_case.review_case_id,
        staging_import_id=staging_import.staging_import_id,
        request_id=request_id,
        created_at=created_at,
        items=items,
    )
    _write_json(_review_queue_initialization_path(request_id, queue_init_id), queue_init.model_dump(mode="json", by_alias=True))
    _write_json(_review_queue_item_batch_path(request_id, queue_init_id), item_batch.model_dump(mode="json", by_alias=True))
    return read_review_queue_initialization(request_id, queue_init_id)


def create_review_queue_item_action(
    request_id: str,
    review_item_id: str,
    payload: ReviewQueueActionRequest | dict[str, Any],
) -> ReviewQueueActionResult:
    try:
        action_payload = payload if isinstance(payload, ReviewQueueActionRequest) else ReviewQueueActionRequest.model_validate(payload or {})
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create review queue action: invalid payload ({exc}).") from exc

    _validate_review_queue_action_payload(action_payload)
    batch_path, batch, item_index = _find_review_queue_item_batch(request_id, review_item_id)
    item = batch.items[item_index]
    queue_init = read_review_queue_initialization(request_id, item.queue_init_id)
    review_case = read_review_only_case(request_id, item.review_case_id)
    _validate_review_queue_action_eligibility(request_id, queue_init, review_case, batch, item, action_payload)

    previous_status = item.queue_status
    trust_before = item.governance.trust_label
    verification_before = item.governance.verification_status
    new_status, analysis_effect, dedup_effect = _review_queue_action_effect(action_payload.action)

    item.queue_status = new_status
    item.governance.review_status = new_status
    item.governance.analysis_included = False
    item.governance.public_visible = False
    item.governance.report_visible = False
    item.governance.sandbox_visible = False
    if action_payload.action == "reject":
        item.governance.trust_label = "rejected"
    elif action_payload.action == "reset_review":
        item.governance.trust_label = "medium_low"
        item.governance.verification_status = "source_url_provided_unverified"
    elif action_payload.action == "mark_weak":
        item.governance.trust_label = "medium_low"
    if action_payload.action == "merge_duplicate":
        item.dedup.dedup_status = "duplicate_candidate_marked"
        item.dedup.duplicate_group_id = action_payload.duplicate_group_id or f"duplicate_candidate_{review_item_id}"
        item.dedup.duplicate_count = max(1, int(item.dedup.duplicate_count or 1))
        item.dedup.may_amplify_risk = False
    elif action_payload.action == "reset_review":
        item.dedup.dedup_status = "not_run"
        item.dedup.duplicate_group_id = None
        item.dedup.duplicate_count = 1
        item.dedup.may_amplify_risk = False
    else:
        item.dedup.may_amplify_risk = False

    reviewed_at = datetime.now(timezone.utc)
    audit_id = _new_review_queue_action_audit_id()
    audit = ReviewQueueActionAudit(
        audit_id=audit_id,
        review_item_id=review_item_id,
        queue_init_id=item.queue_init_id,
        review_case_id=item.review_case_id,
        staging_import_id=item.staging_import_id,
        request_id=request_id,
        previous_status=previous_status,
        new_status=new_status,
        action=action_payload.action,
        reviewer_label=action_payload.reviewer_label.strip(),
        reviewed_at=reviewed_at,
        note=action_payload.note.strip(),
        analysis_effect=analysis_effect,
        trust_label_before=trust_before,
        trust_label_after=item.governance.trust_label,
        verification_status_before=verification_before,
        verification_status_after=item.governance.verification_status,
        dedup_effect=dedup_effect,
        downstream_blockers=_review_queue_action_downstream_blockers(action_payload.action),
        boundary_notes=[
            "Review action updates local review-only queue item status only.",
            "Item remains analysis-excluded until a future completion and dedup gate.",
            "No production Evidence Layer write is performed.",
            "No production case or production review queue is created.",
            "No dedup, analysis, report, Sandbox, or public event generation is run.",
        ],
    )
    item.audit = ReviewQueueItemAudit(source="review_queue_action", queue_init_id=item.queue_init_id, created_at=reviewed_at)
    batch.items[item_index] = item
    _write_json(batch_path, batch.model_dump(mode="json", by_alias=True))
    _write_json(_review_queue_action_audit_path(request_id, review_item_id, audit_id), audit.model_dump(mode="json", by_alias=True))

    return ReviewQueueActionResult(
        action_id=f"review_queue_action_{audit_id}",
        audit_id=audit_id,
        review_item_id=review_item_id,
        queue_init_id=item.queue_init_id,
        review_case_id=item.review_case_id,
        request_id=request_id,
        action=action_payload.action,
        previous_status=previous_status,
        new_status=new_status,
        updated_item=item,
        audit_record=audit,
    )


def create_review_queue_completion_gate(
    request_id: str,
    payload: ReviewQueueCompletionGateRequest | dict[str, Any],
) -> ReviewQueueCompletionGate:
    try:
        gate_payload = payload if isinstance(payload, ReviewQueueCompletionGateRequest) else ReviewQueueCompletionGateRequest.model_validate(payload or {})
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create review queue completion gate: invalid payload ({exc}).") from exc

    _validate_review_queue_completion_gate_payload(gate_payload)
    queue_init = read_review_queue_initialization(request_id, gate_payload.queue_init_id or "")
    review_case_id = gate_payload.review_case_id or queue_init.review_case_id
    review_case = read_review_only_case(request_id, review_case_id)
    batch = read_review_queue_item_batch(request_id, queue_init.queue_init_id)
    gate = _build_review_queue_completion_gate(request_id, gate_payload, queue_init, review_case, batch)
    _write_json(
        _review_queue_completion_gate_path(request_id, gate.completion_gate_id),
        gate.model_dump(mode="json", by_alias=True),
    )
    return read_review_queue_completion_gate(request_id, gate.completion_gate_id)


def create_dedup_preview(
    request_id: str,
    payload: DedupPreviewRequest | dict[str, Any],
) -> DedupPreview:
    try:
        preview_payload = payload if isinstance(payload, DedupPreviewRequest) else DedupPreviewRequest.model_validate(payload or {})
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create dedup preview: invalid payload ({exc}).") from exc

    _validate_dedup_preview_payload(preview_payload)
    gate = read_review_queue_completion_gate(request_id, preview_payload.completion_gate_id or "")
    if gate.request_id != request_id:
        raise AnalysisRequestValidationError("Cannot create dedup preview: completion gate request_id mismatch.")
    if gate.status != "complete_enough_for_future_dedup_preview":
        raise AnalysisRequestValidationError("Cannot create dedup preview: completion gate is not complete_enough_for_future_dedup_preview.")
    if not gate.downstream_eligibility.eligible_for_future_dedup_preview:
        raise AnalysisRequestValidationError("Cannot create dedup preview: completion gate is not eligible for future dedup preview.")
    if gate.counts.privacy_hold:
        raise AnalysisRequestValidationError("Cannot create dedup preview: completion gate contains privacy_hold items.")

    queue_init_id = preview_payload.queue_init_id or gate.queue_init_id
    review_case_id = preview_payload.review_case_id or gate.review_case_id
    if queue_init_id != gate.queue_init_id:
        raise AnalysisRequestValidationError("Cannot create dedup preview: queue_init_id does not match completion gate.")
    if review_case_id != gate.review_case_id:
        raise AnalysisRequestValidationError("Cannot create dedup preview: review_case_id does not match completion gate.")

    queue_init = read_review_queue_initialization(request_id, queue_init_id)
    review_case = read_review_only_case(request_id, review_case_id)
    batch = read_review_queue_item_batch(request_id, queue_init_id)
    preview = _build_dedup_preview(request_id, preview_payload, gate, queue_init, review_case, batch)
    if preview.status != "preview_ready":
        raise AnalysisRequestValidationError(f"Cannot create dedup preview: {', '.join(preview.blockers) or preview.status}.")
    _write_json(_dedup_preview_path(request_id, preview.dedup_preview_id), preview.model_dump(mode="json", by_alias=True))
    return read_dedup_preview(request_id, preview.dedup_preview_id)


def create_dedup_group_review_action(
    request_id: str,
    dedup_preview_id: str,
    group_candidate_id: str,
    payload: DedupGroupReviewActionRequest | dict[str, Any],
) -> DedupGroupReviewActionResult:
    try:
        action_payload = (
            payload
            if isinstance(payload, DedupGroupReviewActionRequest)
            else DedupGroupReviewActionRequest.model_validate(payload or {})
        )
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create dedup group review action: invalid payload ({exc}).") from exc

    _validate_dedup_group_review_action_payload(action_payload, group_candidate_id)
    preview = read_dedup_preview(request_id, dedup_preview_id)
    if preview.status != "preview_ready":
        raise AnalysisRequestValidationError("Cannot create dedup group review action: dedup preview is not preview_ready.")
    gate = read_review_queue_completion_gate(request_id, preview.completion_gate_id)
    if gate.status != "complete_enough_for_future_dedup_preview":
        raise AnalysisRequestValidationError("Cannot create dedup group review action: completion gate is not complete.")
    review_case = read_review_only_case(request_id, preview.review_case_id)
    batch = read_review_queue_item_batch(request_id, preview.queue_init_id)
    group_index = next((index for index, item in enumerate(preview.groups) if item.group_candidate_id == group_candidate_id), -1)
    if group_index < 0:
        raise AnalysisRequestNotFoundError(f"Dedup group candidate {group_candidate_id} for {dedup_preview_id} was not found.")
    group = preview.groups[group_index]
    _validate_dedup_group_review_eligibility(request_id, preview, gate, review_case, batch, group, action_payload)

    previous_status = group.group_status or "review_needed"
    new_status = _dedup_group_new_status(action_payload.action)
    _validate_dedup_group_review_transition(previous_status, action_payload.action)
    representative_before = group.representative_item_id
    updated_group = group.model_copy(deep=True)
    updated_group.group_status = new_status
    updated_group.may_amplify_risk = False
    if action_payload.action == "confirm_group":
        updated_group.human_confirmation_required = False
        updated_group.analysis_effect = "eligible_for_future_promotion_gate"
    elif action_payload.action == "change_representative":
        updated_group.representative_item_id = action_payload.representative_item_id or updated_group.representative_item_id
        updated_group.human_confirmation_required = True
        updated_group.analysis_effect = "preview_only_no_analysis_effect"
    elif action_payload.action == "split_group":
        updated_group.split_item_ids = list(action_payload.split_item_ids)
        updated_group.human_confirmation_required = True
        updated_group.analysis_effect = "preview_only_no_analysis_effect"
    elif action_payload.action in {"reject_group", "request_more_source", "hold_group_for_privacy"}:
        updated_group.human_confirmation_required = True
        updated_group.analysis_effect = "blocked"
    elif action_payload.action == "mark_group_weak":
        updated_group.human_confirmation_required = True
        updated_group.analysis_effect = "preview_only_no_analysis_effect"
    elif action_payload.action == "reset_group_review":
        updated_group.human_confirmation_required = True
        updated_group.analysis_effect = "preview_only_no_analysis_effect"
        updated_group.split_item_ids = []

    note = action_payload.note.strip()
    if note and note not in updated_group.notes:
        updated_group.notes = [*updated_group.notes, note]
    preview.groups[group_index] = updated_group

    audit_id = _new_dedup_group_review_audit_id()
    audit = DedupGroupReviewAudit(
        audit_id=audit_id,
        request_id=request_id,
        review_case_id=preview.review_case_id,
        dedup_preview_id=preview.dedup_preview_id,
        group_candidate_id=group.group_candidate_id,
        previous_group_status=previous_status,
        new_group_status=new_status,
        action=action_payload.action,
        reviewer_label=action_payload.reviewer_label.strip(),
        reviewed_at=datetime.now(timezone.utc),
        note=note,
        affected_item_ids=list(group.item_ids),
        representative_before=representative_before,
        representative_after=updated_group.representative_item_id,
        split_item_ids=list(action_payload.split_item_ids),
        analysis_effect=_dedup_group_analysis_effect(action_payload.action),
        dedup_effect=_dedup_group_dedup_effect(action_payload.action),
        trust_label_effect=_dedup_group_trust_effect(action_payload.action),
        boundary_notes=[
            "Dedup group review is local governance only.",
            "This action does not run production dedup.",
            "This action does not write the production Evidence Layer.",
            "This action does not make evidence analysis-ready.",
            "Duplicate evidence must not amplify risk.",
            "A future group review completion gate and analysis promotion gate are still required.",
        ],
    )
    _write_json(_dedup_preview_path(request_id, preview.dedup_preview_id), preview.model_dump(mode="json", by_alias=True))
    _write_json(_dedup_group_review_audit_path(request_id, group.group_candidate_id, audit.audit_id), audit.model_dump(mode="json", by_alias=True))
    return DedupGroupReviewActionResult(
        action_id=f"dedup_group_review_action_{audit_id}",
        audit_id=audit_id,
        request_id=request_id,
        review_case_id=preview.review_case_id,
        dedup_preview_id=preview.dedup_preview_id,
        group_candidate_id=group.group_candidate_id,
        action=action_payload.action,
        previous_group_status=previous_status,
        new_group_status=new_status,
        updated_group=updated_group,
        audit_record=audit,
    )


def create_analysis_ready_promotion_gate(
    request_id: str,
    payload: AnalysisReadyPromotionGateRequest | dict[str, Any],
) -> AnalysisReadyPromotionGate:
    try:
        gate_payload = (
            payload
            if isinstance(payload, AnalysisReadyPromotionGateRequest)
            else AnalysisReadyPromotionGateRequest.model_validate(payload or {})
        )
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create analysis-ready promotion gate: invalid payload ({exc}).") from exc

    _validate_analysis_ready_promotion_payload(gate_payload)
    read_analysis_request(request_id)
    preview = read_dedup_preview(request_id, gate_payload.dedup_preview_id or "")
    completion_gate = read_review_queue_completion_gate(request_id, gate_payload.completion_gate_id or preview.completion_gate_id)
    queue_init = read_review_queue_initialization(request_id, gate_payload.queue_init_id or preview.queue_init_id)
    review_case = read_review_only_case(request_id, gate_payload.review_case_id or preview.review_case_id)
    batch = read_review_queue_item_batch(request_id, queue_init.queue_init_id)
    staging_import = _select_review_queue_init_staging_import(request_id, review_case, queue_init.staging_import_id)

    gate = _build_analysis_ready_promotion_gate(
        request_id=request_id,
        payload=gate_payload,
        preview=preview,
        completion_gate=completion_gate,
        queue_init=queue_init,
        review_case=review_case,
        batch=batch,
        staging_import=staging_import,
    )
    if gate.status in {"blocked", "privacy_hold"}:
        raise AnalysisRequestValidationError(
            f"Cannot create analysis-ready promotion gate: {', '.join(gate.blockers) or gate.status}."
        )

    audit = PromotionDecisionAudit(
        promotion_decision_id=gate.promotion_decision.promotion_decision_id,
        promotion_gate_id=gate.promotion_gate_id,
        request_id=request_id,
        review_case_id=gate.review_case_id,
        queue_init_id=gate.queue_init_id,
        completion_gate_id=gate.completion_gate_id,
        dedup_preview_id=gate.dedup_preview_id,
        previous_status="not_created",
        new_status=gate.status,
        decision=gate.promotion_decision.decision,
        reviewer_label=gate.promotion_decision.reviewer_label,
        reviewed_at=gate.promotion_decision.decided_at,
        note=gate.promotion_decision.note,
        affected_item_ids=list(gate.promotion_set_preview.item_ids),
        affected_group_ids=list(gate.promotion_set_preview.group_ids),
        analysis_effect=gate.promotion_decision.analysis_effect,
        boundary_notes=[
            "Analysis-ready promotion gate is local governance only.",
            "This decision does not run analysis.",
            "This decision does not write the production Evidence Layer.",
            "This decision does not create a production case.",
            "This decision does not run production dedup.",
            "This decision does not generate reports, Sandbox fixtures, or public event pages.",
            "Provider output is evidence, not truth.",
        ],
    )
    _write_json(_analysis_ready_promotion_gate_path(request_id, gate.promotion_gate_id), gate.model_dump(mode="json", by_alias=True))
    _write_json(
        _promotion_decision_audit_path(request_id, gate.promotion_gate_id, audit.promotion_decision_id),
        audit.model_dump(mode="json", by_alias=True),
    )
    return read_analysis_ready_promotion_gate(request_id, gate.promotion_gate_id)


def create_manual_analysis_trigger(
    request_id: str,
    payload: ManualAnalysisTriggerRequest | dict[str, Any],
) -> ManualAnalysisTrigger:
    try:
        trigger_payload = (
            payload
            if isinstance(payload, ManualAnalysisTriggerRequest)
            else ManualAnalysisTriggerRequest.model_validate(payload or {})
        )
    except ValidationError as exc:
        raise AnalysisRequestValidationError(f"Cannot create manual analysis trigger: invalid payload ({exc}).") from exc

    _validate_manual_analysis_trigger_payload(trigger_payload)
    read_analysis_request(request_id)
    gate = read_analysis_ready_promotion_gate(request_id, trigger_payload.promotion_gate_id)
    _validate_manual_analysis_trigger_gate(request_id, gate)
    if trigger_payload.review_case_id and trigger_payload.review_case_id != gate.review_case_id:
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: review_case_id does not match promotion gate.")
    batch = read_review_queue_item_batch(request_id, gate.queue_init_id)
    _validate_manual_analysis_trigger_scope(gate, batch)

    manual_trigger_id = _new_manual_analysis_trigger_id()
    audit_id = _new_manual_analysis_trigger_audit_id()
    status = _manual_analysis_trigger_status(trigger_payload.trigger_decision)
    analysis_scope = ManualAnalysisScope(
        include_item_ids=list(gate.promotion_set_preview.item_ids),
        include_group_ids=list(gate.promotion_set_preview.group_ids),
        exclude_item_ids=list(gate.promotion_set_preview.excluded_item_ids),
        exclude_group_ids=[],
        weak_warning_item_ids=list(gate.promotion_set_preview.weak_item_ids),
        weak_warning_group_ids=[],
        analysis_input_source="review_only_promoted_candidates",
        analysis_included_after_runtime="not_set_by_this_phase",
    )
    required_warnings = ManualAnalysisRequiredWarnings(
        coverage_limitations=[
            "Coverage is limited to reviewed promoted candidates, not full-web coverage.",
            "Coverage is limited to available/imported evidence, not full-platform coverage.",
        ],
        weak_evidence_warnings=_manual_analysis_weak_warnings(gate),
        dedup_preview_warnings=[
            "Duplicate evidence must not amplify risk, sentiment, coverage, or conclusions.",
            "Duplicate group size is context/density only, not truth strength.",
        ],
        provider_output_is_evidence_not_truth=True,
        not_official_verification=True,
        not_full_web_coverage=True,
    )
    boundary_notes = [
        "Manual Analysis Trigger records a human decision only.",
        "This trigger does not run analysis.",
        "This trigger does not generate Analysis Result.",
        "This trigger does not write the production Evidence Layer.",
        "This trigger does not create a production case.",
        "This trigger does not generate reports, Sandbox fixtures, or public event pages.",
        "Eligible promotion gate is not automatic analysis.",
        "Provider output is evidence, not truth.",
    ]
    trigger = ManualAnalysisTrigger(
        manual_trigger_id=manual_trigger_id,
        request_id=request_id,
        review_case_id=gate.review_case_id,
        promotion_gate_id=gate.promotion_gate_id,
        created_at=datetime.now(timezone.utc),
        created_by=trigger_payload.reviewer_label.strip(),
        trigger_decision=trigger_payload.trigger_decision,
        status=status,
        analysis_scope=analysis_scope,
        required_warnings=required_warnings,
        blocked_reasons=[],
        warnings=_unique_preserve_order(
            list(gate.warnings)
            + list(gate.promotion_set_preview.warning_notes)
            + required_warnings.coverage_limitations
            + required_warnings.weak_evidence_warnings
            + required_warnings.dedup_preview_warnings
        ),
        boundary_notes=boundary_notes,
        recommended_next_steps=_manual_analysis_trigger_next_steps(status),
    )
    audit = ManualAnalysisTriggerAudit(
        manual_trigger_audit_id=audit_id,
        manual_trigger_id=manual_trigger_id,
        promotion_gate_id=gate.promotion_gate_id,
        request_id=request_id,
        review_case_id=gate.review_case_id,
        decision=trigger_payload.trigger_decision,
        reviewer_label=trigger_payload.reviewer_label.strip(),
        decided_at=datetime.now(timezone.utc),
        note=trigger_payload.note.strip(),
        included_item_ids=list(analysis_scope.include_item_ids),
        excluded_item_ids=list(analysis_scope.exclude_item_ids),
        weak_warning_item_ids=list(analysis_scope.weak_warning_item_ids),
        included_group_ids=list(analysis_scope.include_group_ids),
        excluded_group_ids=list(analysis_scope.exclude_group_ids),
        coverage_acknowledgement=trigger_payload.coverage_acknowledged,
        privacy_acknowledgement=trigger_payload.privacy_acknowledged,
        dedup_warning_acknowledgement=trigger_payload.dedup_warning_acknowledged,
        provider_output_is_evidence_not_truth_acknowledgement=trigger_payload.provider_output_is_evidence_not_truth_acknowledged,
        boundary_notes=boundary_notes,
    )
    _write_json(_manual_analysis_trigger_path(request_id, manual_trigger_id), trigger.model_dump(mode="json", by_alias=True))
    _write_json(_manual_analysis_trigger_audit_path(request_id, manual_trigger_id, audit_id), audit.model_dump(mode="json", by_alias=True))
    return read_manual_analysis_trigger(request_id, manual_trigger_id)


def _record_from_path(path: Path) -> AnalysisRequestRecord:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8-sig"))
        request = AnalysisRequestFile.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{path.name} is not a valid analysis request: {type(exc).__name__}") from exc

    result, result_warning, result_file = _read_result(request.request_id)
    request_status = str((request.sentigraph_metadata or {}).get("request_status") or "draft")
    stat = path.stat()
    return AnalysisRequestRecord(
        request_id=request.request_id,
        request=request,
        request_status=request_status,
        request_file=f"runtime/analysis_requests/requests/{path.name}",
        result_file=f"runtime/analysis_requests/results/{result_file.name}" if result_file else None,
        provider_result=result,
        result_warning=result_warning,
        provider_status=result.status if result else None,
        safety_status=result.safety_status if result else None,
        package_name=result.package_name if result else None,
        created_at=request.created_at,
        updated_at=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
    )


def _read_result(request_id: str) -> tuple[ProviderJobResult | None, str | None, Path | None]:
    result_path = _result_path(request_id)
    if not result_path.exists():
        return None, None, None
    try:
        parsed = json.loads(result_path.read_text(encoding="utf-8-sig"))
        result = ProviderJobResult.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        return None, f"Matching provider result JSON is invalid: {type(exc).__name__}", result_path
    if result.request_id != request_id:
        return None, "Matching provider result request_id does not match file name.", result_path
    return result, None, result_path


def _validate_case_draft_eligibility(record: AnalysisRequestRecord) -> None:
    if record.result_warning:
        raise AnalysisRequestValidationError(f"Cannot create case draft: provider result is invalid ({record.result_warning}).")
    result = record.provider_result
    if not result:
        raise AnalysisRequestValidationError("Cannot create case draft: provider result is missing.")
    if result.status not in {"package_ready", "validation_warn"}:
        raise AnalysisRequestValidationError(f"Cannot create case draft: provider status {result.status} is not eligible.")
    if result.safety_status not in {"safe", "medium"}:
        raise AnalysisRequestValidationError(f"Cannot create case draft: safety status {result.safety_status} is not eligible.")
    if result.validation.errors > 0:
        raise AnalysisRequestValidationError("Cannot create case draft: provider validation errors must be 0.")
    if not result.package_name:
        raise AnalysisRequestValidationError("Cannot create case draft: package_name is missing.")
    if result.counts.evidence <= 0:
        raise AnalysisRequestValidationError("Cannot create case draft: counts.evidence must be greater than 0.")

    raw = _read_result_payload(record.request_id)
    raw_privacy = raw.get("privacy") if isinstance(raw.get("privacy"), dict) else {}
    required_privacy = [
        "raw_author_ids_removed",
        "raw_author_names_removed",
        "profile_urls_removed",
        "private_messages_excluded",
    ]
    missing_privacy = [field for field in required_privacy if field not in raw_privacy]
    if missing_privacy:
        raise AnalysisRequestValidationError(f"Cannot create case draft: privacy fields missing ({', '.join(missing_privacy)}).")
    if not all(bool(raw_privacy.get(field)) for field in required_privacy):
        raise AnalysisRequestValidationError("Cannot create case draft: privacy flags must all be true.")

    raw_coverage = raw.get("coverage") if isinstance(raw.get("coverage"), dict) else {}
    required_coverage = ["not_full_web", "not_full_platform", "not_full_thread"]
    missing_coverage = [field for field in required_coverage if field not in raw_coverage]
    if missing_coverage:
        raise AnalysisRequestValidationError(f"Cannot create case draft: coverage limitation fields missing ({', '.join(missing_coverage)}).")
    if not all(bool(raw_coverage.get(field)) for field in required_coverage):
        raise AnalysisRequestValidationError("Cannot create case draft: coverage must not claim full-web/full-platform/full-thread coverage.")


def _validate_import_plan_eligibility(draft: CaseDraftHandoff) -> None:
    if draft.readiness.state not in {"ready_for_manual_review", "ready_for_manual_import_review"}:
        raise AnalysisRequestValidationError(f"Cannot create evidence import plan: draft readiness {draft.readiness.state} is not eligible.")
    if draft.provider_summary.safety_status not in {"safe", "medium"}:
        raise AnalysisRequestValidationError(f"Cannot create evidence import plan: safety status {draft.provider_summary.safety_status} is not eligible.")
    if not draft.package_reference.package_name:
        raise AnalysisRequestValidationError("Cannot create evidence import plan: package_name is missing.")
    if draft.counts.evidence <= 0:
        raise AnalysisRequestValidationError("Cannot create evidence import plan: counts.evidence must be greater than 0.")
    if draft.validation.status not in {"passed", "warn", "not_run"}:
        raise AnalysisRequestValidationError(f"Cannot create evidence import plan: validation status {draft.validation.status} is not eligible.")
    if draft.validation.errors > 0:
        raise AnalysisRequestValidationError("Cannot create evidence import plan: validation errors must be 0.")
    required_privacy = [
        draft.privacy.raw_author_ids_removed,
        draft.privacy.raw_author_names_removed,
        draft.privacy.profile_urls_removed,
        draft.privacy.private_messages_excluded,
    ]
    if not all(required_privacy):
        raise AnalysisRequestValidationError("Cannot create evidence import plan: privacy flags must all be true.")
    if not (draft.coverage.not_full_web and draft.coverage.not_full_platform and draft.coverage.not_full_thread):
        raise AnalysisRequestValidationError("Cannot create evidence import plan: coverage must not claim full-web/full-platform/full-thread coverage.")


def _validate_import_preview_eligibility(plan: EvidenceImportPlan) -> None:
    if plan.readiness.state not in {"ready_for_manual_import_review", "ready_for_human_review"}:
        raise AnalysisRequestValidationError(f"Cannot create evidence import preview: import plan readiness {plan.readiness.state} is not eligible.")
    if not plan.package_reference.package_name:
        raise AnalysisRequestValidationError("Cannot create evidence import preview: package_name is missing.")
    if plan.counts.evidence <= 0:
        raise AnalysisRequestValidationError("Cannot create evidence import preview: counts.evidence must be greater than 0.")
    if plan.validation.status not in {"passed", "warn"}:
        raise AnalysisRequestValidationError(f"Cannot create evidence import preview: validation status {plan.validation.status} is not eligible.")
    if plan.validation.errors > 0:
        raise AnalysisRequestValidationError("Cannot create evidence import preview: validation errors must be 0.")
    required_privacy = [
        plan.privacy.raw_author_ids_removed,
        plan.privacy.raw_author_names_removed,
        plan.privacy.profile_urls_removed,
        plan.privacy.private_messages_excluded,
    ]
    if not all(required_privacy):
        raise AnalysisRequestValidationError("Cannot create evidence import preview: privacy flags must all be true.")
    if not (plan.coverage.not_full_web and plan.coverage.not_full_platform and plan.coverage.not_full_thread):
        raise AnalysisRequestValidationError("Cannot create evidence import preview: coverage must not claim full-web/full-platform/full-thread coverage.")

    immediate_flags = {
        "import_evidence_rows_now": plan.proposed_import.import_evidence_rows_now,
        "create_case_now": plan.proposed_import.create_case_now,
        "run_analysis_now": plan.proposed_import.run_analysis_now,
        "generate_sandbox_now": plan.proposed_import.generate_sandbox_now,
        "generate_report_now": plan.proposed_import.generate_report_now,
    }
    enabled_flags = [name for name, enabled in immediate_flags.items() if enabled]
    if enabled_flags:
        raise AnalysisRequestValidationError(
            f"Cannot create evidence import preview: import plan suggests immediate execution ({', '.join(enabled_flags)})."
        )


def _validate_review_decision_preview_eligibility(preview: EvidenceImportPreview) -> None:
    if preview.readiness.state not in {"ready_for_human_review", "ready_for_manual_review"}:
        raise AnalysisRequestValidationError(f"Cannot create review decision: import preview readiness {preview.readiness.state} is not eligible.")
    if not preview.package_reference.package_name:
        raise AnalysisRequestValidationError("Cannot create review decision: package_name is missing.")
    if preview.metadata_summary.evidence <= 0:
        raise AnalysisRequestValidationError("Cannot create review decision: metadata_summary.evidence must be greater than 0.")
    if preview.validation_summary.errors > 0:
        raise AnalysisRequestValidationError("Cannot create review decision: validation errors must be 0.")
    required_privacy = [
        preview.privacy_summary.raw_author_ids_removed,
        preview.privacy_summary.raw_author_names_removed,
        preview.privacy_summary.profile_urls_removed,
        preview.privacy_summary.private_messages_excluded,
    ]
    if not all(required_privacy):
        raise AnalysisRequestValidationError("Cannot create review decision: privacy flags must all be true.")
    if not (
        preview.coverage_summary.not_full_web
        and preview.coverage_summary.not_full_platform
        and preview.coverage_summary.not_full_thread
    ):
        raise AnalysisRequestValidationError("Cannot create review decision: coverage must not claim full-web/full-platform/full-thread coverage.")
    if preview.proposed_evidence_defaults.review_status != "review_needed":
        raise AnalysisRequestValidationError("Cannot create review decision: proposed review_status must be review_needed.")
    if preview.proposed_evidence_defaults.verification_status != "source_url_provided_unverified":
        raise AnalysisRequestValidationError("Cannot create review decision: proposed verification_status must be source_url_provided_unverified.")
    if preview.proposed_evidence_defaults.trust_label != "medium_low":
        raise AnalysisRequestValidationError("Cannot create review decision: proposed trust_label must be medium_low.")
    if preview.sample_preview_policy.read_rows_now:
        raise AnalysisRequestValidationError("Cannot create review decision: sample_preview_policy.read_rows_now must be false.")

    unsafe_flags = {
        "evidence_rows_read": preview.safe_mode.get("evidence_rows_read", False),
        "evidence_rows_parsed": preview.safe_mode.get("evidence_rows_parsed", False),
        "evidence_rows_imported": preview.safe_mode.get("evidence_rows_imported", False),
        "production_case_created": preview.safe_mode.get("production_case_created", False),
        "analysis_generated": preview.safe_mode.get("analysis_generated", False),
        "sandbox_fixture_generated": preview.safe_mode.get("sandbox_fixture_generated", False),
        "public_event_page_generated": preview.safe_mode.get("public_event_page_generated", False),
        "report_generated": preview.safe_mode.get("report_generated", False),
    }
    enabled_flags = [name for name, enabled in unsafe_flags.items() if enabled]
    if enabled_flags:
        raise AnalysisRequestValidationError(
            f"Cannot create review decision: preview suggests immediate execution or row access ({', '.join(enabled_flags)})."
        )


def _select_review_decision_for_import_job(
    request_id: str,
    decision_id: str | None,
) -> EvidenceImportReviewDecision:
    if decision_id:
        return read_evidence_import_review_decision(request_id, decision_id)
    decisions = list_evidence_import_review_decisions(request_id)
    if not decisions:
        raise AnalysisRequestNotFoundError(f"Evidence import review decision for {request_id} was not found.")
    return decisions[0]


def _validate_import_job_decision_eligibility(decision: EvidenceImportReviewDecision) -> None:
    if decision.decision != "approve_import":
        raise AnalysisRequestValidationError("Cannot create manual import job draft: latest review decision must be approve_import.")
    if decision.readiness.state != "approved_for_future_manual_import":
        raise AnalysisRequestValidationError(
            f"Cannot create manual import job draft: decision readiness {decision.readiness.state} is not eligible."
        )
    missing_acknowledgements = decision.checklist.missing_acknowledgements()
    if missing_acknowledgements:
        missing = ", ".join(missing_acknowledgements)
        raise AnalysisRequestValidationError(f"Cannot create manual import job draft: missing acknowledgements ({missing}).")
    if decision.approved_defaults.review_status != "review_needed":
        raise AnalysisRequestValidationError("Cannot create manual import job draft: approved review_status must be review_needed.")
    if decision.approved_defaults.verification_status != "source_url_provided_unverified":
        raise AnalysisRequestValidationError(
            "Cannot create manual import job draft: approved verification_status must be source_url_provided_unverified."
        )
    if decision.approved_defaults.trust_label != "medium_low":
        raise AnalysisRequestValidationError("Cannot create manual import job draft: approved trust_label must be medium_low.")

    unsafe_flags = {
        "evidence_rows_read": decision.safe_mode.get("evidence_rows_read", False),
        "evidence_rows_parsed": decision.safe_mode.get("evidence_rows_parsed", False),
        "evidence_rows_imported": decision.safe_mode.get("evidence_rows_imported", False),
        "production_case_created": decision.safe_mode.get("production_case_created", False),
        "analysis_generated": decision.safe_mode.get("analysis_generated", False),
        "sandbox_fixture_generated": decision.safe_mode.get("sandbox_fixture_generated", False),
        "public_event_page_generated": decision.safe_mode.get("public_event_page_generated", False),
        "report_generated": decision.safe_mode.get("report_generated", False),
    }
    enabled_flags = [name for name, enabled in unsafe_flags.items() if enabled]
    if enabled_flags:
        raise AnalysisRequestValidationError(
            f"Cannot create manual import job draft: decision suggests immediate execution or row access ({', '.join(enabled_flags)})."
        )


def _validate_import_job_preview_eligibility(preview: EvidenceImportPreview) -> None:
    if not preview.package_reference.package_name:
        raise AnalysisRequestValidationError("Cannot create manual import job draft: package_name is missing.")
    if preview.metadata_summary.evidence <= 0:
        raise AnalysisRequestValidationError("Cannot create manual import job draft: metadata_summary.evidence must be greater than 0.")
    if preview.validation_summary.errors > 0:
        raise AnalysisRequestValidationError("Cannot create manual import job draft: validation errors must be 0.")
    required_privacy = [
        preview.privacy_summary.raw_author_ids_removed,
        preview.privacy_summary.raw_author_names_removed,
        preview.privacy_summary.profile_urls_removed,
        preview.privacy_summary.private_messages_excluded,
    ]
    if not all(required_privacy):
        raise AnalysisRequestValidationError("Cannot create manual import job draft: privacy flags must all be true.")
    if not (
        preview.coverage_summary.not_full_web
        and preview.coverage_summary.not_full_platform
        and preview.coverage_summary.not_full_thread
    ):
        raise AnalysisRequestValidationError("Cannot create manual import job draft: coverage must not claim full-web/full-platform/full-thread coverage.")
    if preview.sample_preview_policy.read_rows_now:
        raise AnalysisRequestValidationError("Cannot create manual import job draft: sample_preview_policy.read_rows_now must be false.")
    if not preview.readiness.requires_review_decision:
        raise AnalysisRequestValidationError("Cannot create manual import job draft: preview must require review decision.")

    unsafe_flags = {
        "evidence_rows_read": preview.safe_mode.get("evidence_rows_read", False),
        "evidence_rows_parsed": preview.safe_mode.get("evidence_rows_parsed", False),
        "evidence_rows_imported": preview.safe_mode.get("evidence_rows_imported", False),
        "production_case_created": preview.safe_mode.get("production_case_created", False),
        "analysis_generated": preview.safe_mode.get("analysis_generated", False),
        "sandbox_fixture_generated": preview.safe_mode.get("sandbox_fixture_generated", False),
        "public_event_page_generated": preview.safe_mode.get("public_event_page_generated", False),
        "report_generated": preview.safe_mode.get("report_generated", False),
    }
    enabled_flags = [name for name, enabled in unsafe_flags.items() if enabled]
    if enabled_flags:
        raise AnalysisRequestValidationError(
            f"Cannot create manual import job draft: preview suggests immediate execution or row access ({', '.join(enabled_flags)})."
        )


def _select_manual_import_job_for_preflight(request_id: str, job_id: str | None) -> ManualEvidenceImportJob:
    if job_id:
        return read_manual_evidence_import_job(request_id, job_id)
    jobs = list_manual_evidence_import_jobs(request_id)
    if not jobs:
        raise AnalysisRequestNotFoundError(f"manual import job for {request_id} was not found.")
    return jobs[0]


def _validate_execution_preflight_job_eligibility(job: ManualEvidenceImportJob) -> None:
    if job.status != "draft_not_executed":
        raise AnalysisRequestValidationError(f"Cannot create execution preflight: job status {job.status} is not eligible.")
    if job.execution_mode != "dry_run_gate":
        raise AnalysisRequestValidationError(f"Cannot create execution preflight: job execution_mode {job.execution_mode} is not eligible.")
    if job.readiness.state != "ready_for_future_manual_import_execution":
        raise AnalysisRequestValidationError(f"Cannot create execution preflight: job readiness {job.readiness.state} is not eligible.")
    if job.readiness.can_execute_now:
        raise AnalysisRequestValidationError("Cannot create execution preflight: job readiness can_execute_now must be false.")
    if not job.package_reference.package_name:
        raise AnalysisRequestValidationError("Cannot create execution preflight: package_name is missing.")
    if not job.package_reference.package_path:
        raise AnalysisRequestValidationError("Cannot create execution preflight: package_path is missing.")

    unsafe_dry_run_flags = {
        "import_evidence_rows_now": job.dry_run_result.import_evidence_rows_now,
        "create_case_now": job.dry_run_result.create_case_now,
        "run_dedup_now": job.dry_run_result.run_dedup_now,
        "create_review_queue_now": job.dry_run_result.create_review_queue_now,
        "run_analysis_now": job.dry_run_result.run_analysis_now,
        "generate_sandbox_now": job.dry_run_result.generate_sandbox_now,
        "generate_report_now": job.dry_run_result.generate_report_now,
    }
    enabled_dry_run_flags = [name for name, enabled in unsafe_dry_run_flags.items() if enabled]
    if enabled_dry_run_flags:
        raise AnalysisRequestValidationError(
            f"Cannot create execution preflight: dry-run job has unsafe now flags ({', '.join(enabled_dry_run_flags)})."
        )

    unsafe_safe_mode_flags = {
        "evidence_rows_read": job.safe_mode.get("evidence_rows_read", False),
        "evidence_rows_parsed": job.safe_mode.get("evidence_rows_parsed", False),
        "evidence_rows_imported": job.safe_mode.get("evidence_rows_imported", False),
        "production_case_created": job.safe_mode.get("production_case_created", False),
        "analysis_generated": job.safe_mode.get("analysis_generated", False),
        "sandbox_fixture_generated": job.safe_mode.get("sandbox_fixture_generated", False),
        "public_event_page_generated": job.safe_mode.get("public_event_page_generated", False),
        "report_generated": job.safe_mode.get("report_generated", False),
        "provider_execution": job.safe_mode.get("provider_execution", False),
        "collector_jobs_run": job.safe_mode.get("collector_jobs_run", False),
    }
    enabled_safe_mode_flags = [name for name, enabled in unsafe_safe_mode_flags.items() if enabled]
    if enabled_safe_mode_flags:
        raise AnalysisRequestValidationError(
            f"Cannot create execution preflight: dry-run job suggests execution already happened ({', '.join(enabled_safe_mode_flags)})."
        )


def _validate_execution_preflight_decision_eligibility(
    request_id: str,
    decision: EvidenceImportReviewDecision,
    job: ManualEvidenceImportJob,
) -> None:
    latest_decisions = list_evidence_import_review_decisions(request_id)
    latest_decision = latest_decisions[0] if latest_decisions else None
    if not latest_decision:
        raise AnalysisRequestNotFoundError(f"Evidence import review decision for {request_id} was not found.")
    if latest_decision.decision_id != decision.decision_id:
        raise AnalysisRequestValidationError("Cannot create execution preflight: selected approval is stale; latest review decision must be approve_import.")
    if decision.decision != "approve_import":
        raise AnalysisRequestValidationError("Cannot create execution preflight: latest review decision must be approve_import.")
    if job.decision_id != decision.decision_id:
        raise AnalysisRequestValidationError("Cannot create execution preflight: job decision_id does not match selected review decision.")
    _validate_import_job_decision_eligibility(decision)


def _validate_execution_preflight_preview_eligibility(preview: EvidenceImportPreview) -> None:
    if preview.validation_summary.status not in {"passed", "warn"}:
        raise AnalysisRequestValidationError(f"Cannot create execution preflight: validation status {preview.validation_summary.status} is not eligible.")
    _validate_import_job_preview_eligibility(preview)


def _build_execution_preflight_package_file_checks(
    package_reference: CaseDraftPackageReference,
) -> tuple[ManualEvidenceImportPackageFileChecks, list[str]]:
    checks = ManualEvidenceImportPackageFileChecks()
    warnings: list[str] = []
    package_path_value = (package_reference.package_path or "").strip()
    if not package_path_value:
        raise AnalysisRequestValidationError("Cannot create execution preflight: package_path is missing.")

    package_path = Path(package_path_value).expanduser()
    if not package_path.is_absolute():
        package_path = (PROJECT_ROOT / package_path).resolve()

    if not package_path.exists() or not package_path.is_dir():
        warnings.append("Package path is not available locally; preflight used stored metadata only.")
        return checks, warnings

    checks.package_path_checked = True
    checks.package_path_exists = True
    checks.manifest_present = (package_path / "manifest.json").is_file()
    checks.validation_report_present = (package_path / "validation_report.json").is_file()
    checks.coverage_note_present = (package_path / "coverage_note.md").is_file()
    checks.readme_present = (package_path / "README.md").is_file()
    checks.evidence_items_jsonl_present = (package_path / "evidence_items.jsonl").is_file()
    checks.evidence_items_csv_present = (package_path / "evidence_items.csv").is_file()
    checks.row_files_opened = False
    checks.row_files_parsed = False

    missing_required: list[str] = []
    if not checks.manifest_present:
        missing_required.append("manifest.json")
    if not checks.validation_report_present:
        missing_required.append("validation_report.json")
    if not checks.coverage_note_present:
        missing_required.append("coverage_note.md")
    if missing_required:
        raise AnalysisRequestValidationError(
            f"Cannot create execution preflight: required package files missing ({', '.join(missing_required)})."
        )
    if not checks.readme_present:
        warnings.append("Package README.md is missing; continue only with reviewer-visible package notes.")
    if not checks.evidence_items_jsonl_present and not checks.evidence_items_csv_present:
        warnings.append("No evidence row file name was found; future row reader cannot execute without a row file.")
    return checks, warnings


def _select_execution_preflight_for_row_reader(
    request_id: str,
    preflight_id: str | None,
) -> ManualEvidenceImportExecutionPreflight:
    if preflight_id:
        return read_manual_evidence_import_execution_preflight(request_id, preflight_id)
    preflights = list_manual_evidence_import_execution_preflights(request_id)
    if not preflights:
        raise AnalysisRequestNotFoundError(f"execution preflight for {request_id} was not found.")
    return preflights[0]


def _validate_row_reader_preflight_eligibility(preflight: ManualEvidenceImportExecutionPreflight) -> None:
    if preflight.status not in {"preflight_passed", "preflight_warn"}:
        raise AnalysisRequestValidationError(f"Cannot create row reader dry-run: execution preflight status {preflight.status} is not eligible.")
    if not preflight.readiness.requires_separate_execution_phase:
        raise AnalysisRequestValidationError("Cannot create row reader dry-run: preflight must require a separate execution phase.")
    if preflight.package_file_checks.row_files_opened or preflight.package_file_checks.row_files_parsed:
        raise AnalysisRequestValidationError("Cannot create row reader dry-run: preflight already indicates row file access.")
    if preflight.future_row_reader_plan.read_rows_now:
        raise AnalysisRequestValidationError("Cannot create row reader dry-run: preflight read_rows_now must be false.")
    unsafe_flags = {
        "evidence_rows_opened": preflight.safe_mode.get("evidence_rows_opened", False),
        "evidence_rows_parsed": preflight.safe_mode.get("evidence_rows_parsed", False),
        "evidence_rows_imported": preflight.safe_mode.get("evidence_rows_imported", False),
        "evidence_layer_written": preflight.safe_mode.get("evidence_layer_written", False),
        "production_case_created": preflight.safe_mode.get("production_case_created", False),
        "analysis_generated": preflight.safe_mode.get("analysis_generated", False),
        "sandbox_fixture_generated": preflight.safe_mode.get("sandbox_fixture_generated", False),
        "public_event_page_generated": preflight.safe_mode.get("public_event_page_generated", False),
        "report_generated": preflight.safe_mode.get("report_generated", False),
        "provider_execution": preflight.safe_mode.get("provider_execution", False),
        "collector_jobs_run": preflight.safe_mode.get("collector_jobs_run", False),
    }
    enabled = [name for name, value in unsafe_flags.items() if value]
    if enabled:
        raise AnalysisRequestValidationError(f"Cannot create row reader dry-run: preflight unsafe flags are true ({', '.join(enabled)}).")


def _validate_row_reader_payload(payload: EvidenceRowReaderDryRunCreate) -> None:
    if payload.fixture_mode != "synthetic_fixture":
        raise AnalysisRequestValidationError("Cannot create row reader dry-run: fixture_mode must be synthetic_fixture.")
    if payload.fixture_name not in ROW_READER_FIXTURES:
        raise AnalysisRequestValidationError("Cannot create row reader dry-run: fixture must be an allowed synthetic fixture.")
    if payload.max_rows > 20:
        raise AnalysisRequestValidationError("Cannot create row reader dry-run: max_rows must be <= 20.")
    if payload.row_source_path:
        raise AnalysisRequestValidationError("Cannot create row reader dry-run: row_source_path is not allowed; use an allowlisted synthetic fixture.")
    now_flags = EvidenceRowReaderNowFlags.model_validate(payload.now_flags or {})
    enabled_now_flags = [name for name, value in now_flags.model_dump().items() if value]
    if enabled_now_flags:
        raise AnalysisRequestValidationError(f"Cannot create row reader dry-run: now flags must remain false ({', '.join(enabled_now_flags)}).")


def _validate_real_package_preview_preflight_eligibility(preflight: ManualEvidenceImportExecutionPreflight) -> None:
    _validate_row_reader_preflight_eligibility(preflight)
    if not preflight.package_reference.package_path:
        raise AnalysisRequestValidationError("Cannot create real package row preview: package_path is missing.")
    if not preflight.package_file_checks.package_path_exists:
        raise AnalysisRequestValidationError("Cannot create real package row preview: package path was not confirmed by preflight.")
    if not preflight.package_file_checks.manifest_present:
        raise AnalysisRequestValidationError("Cannot create real package row preview: manifest.json is missing.")
    if not preflight.package_file_checks.validation_report_present:
        raise AnalysisRequestValidationError("Cannot create real package row preview: validation_report.json is missing.")
    if not preflight.package_file_checks.coverage_note_present:
        raise AnalysisRequestValidationError("Cannot create real package row preview: coverage_note.md is missing.")
    if preflight.validation_summary.errors > 0:
        raise AnalysisRequestValidationError("Cannot create real package row preview: validation errors must be 0.")
    if not (preflight.coverage_summary.not_full_web and preflight.coverage_summary.not_full_platform and preflight.coverage_summary.not_full_thread):
        raise AnalysisRequestValidationError("Cannot create real package row preview: coverage limitations must be explicit.")
    if not (
        preflight.privacy_summary.raw_author_ids_removed
        and preflight.privacy_summary.raw_author_names_removed
        and preflight.privacy_summary.profile_urls_removed
        and preflight.privacy_summary.private_messages_excluded
    ):
        raise AnalysisRequestValidationError("Cannot create real package row preview: privacy flags are incomplete.")


def _validate_real_package_preview_payload(payload: RealPackageRowPreviewCreate) -> None:
    if payload.max_rows > 20:
        raise AnalysisRequestValidationError("Cannot create real package row preview: max_rows must be <= 20.")
    acknowledgements = {
        "acknowledge_real_package_preview": payload.acknowledge_real_package_preview,
        "acknowledge_no_import": payload.acknowledge_no_import,
        "acknowledge_preview_not_representative": payload.acknowledge_preview_not_representative,
        "acknowledge_privacy_stop": payload.acknowledge_privacy_stop,
    }
    missing = [name for name, value in acknowledgements.items() if not value]
    if missing:
        raise AnalysisRequestValidationError(f"Cannot create real package row preview: acknowledgement required ({', '.join(missing)}).")
    now_flags = EvidenceRowReaderNowFlags.model_validate(payload.now_flags or {})
    enabled_now_flags = [name for name, value in now_flags.model_dump().items() if value]
    if enabled_now_flags:
        raise AnalysisRequestValidationError(f"Cannot create real package row preview: now flags must remain false ({', '.join(enabled_now_flags)}).")


def _validate_real_package_preview_review_decision(request_id: str, preflight: ManualEvidenceImportExecutionPreflight) -> None:
    decisions = list_evidence_import_review_decisions(request_id)
    if not decisions:
        raise AnalysisRequestNotFoundError(f"review decision for {request_id} was not found.")
    latest = decisions[0]
    if latest.decision != "approve_import":
        raise AnalysisRequestValidationError("Cannot create real package row preview: latest review decision must be approve_import.")
    if latest.decision_id != preflight.decision_id:
        raise AnalysisRequestValidationError("Cannot create real package row preview: execution preflight review decision is stale.")


def _validate_real_package_preview_job(preflight: ManualEvidenceImportExecutionPreflight) -> None:
    job = read_manual_evidence_import_job(preflight.request_id, preflight.job_id)
    if job.execution_mode != "dry_run_gate":
        raise AnalysisRequestValidationError("Cannot create real package row preview: import job must remain dry_run_gate.")
    unsafe_flags = {
        "evidence_rows_read": job.safe_mode.get("evidence_rows_read", False),
        "evidence_rows_parsed": job.safe_mode.get("evidence_rows_parsed", False),
        "evidence_rows_imported": job.safe_mode.get("evidence_rows_imported", False),
        "production_case_created": job.safe_mode.get("production_case_created", False),
        "analysis_generated": job.safe_mode.get("analysis_generated", False),
        "report_generated": job.safe_mode.get("report_generated", False),
        "provider_execution": job.safe_mode.get("provider_execution", False),
        "collector_jobs_run": job.safe_mode.get("collector_jobs_run", False),
    }
    enabled = [name for name, value in unsafe_flags.items() if value]
    if enabled:
        raise AnalysisRequestValidationError(f"Cannot create real package row preview: import job unsafe flags are true ({', '.join(enabled)}).")


def _validate_real_package_preview_synthetic_dry_run(request_id: str) -> None:
    dry_runs = list_evidence_row_reader_dry_runs(request_id)
    if not dry_runs:
        raise AnalysisRequestValidationError("Cannot create real package row preview: synthetic row reader dry-run is required first.")
    latest = dry_runs[0]
    if latest.status not in {"passed", "warn"}:
        raise AnalysisRequestValidationError("Cannot create real package row preview: latest synthetic row reader dry-run must be passed or warn.")
    if latest.row_source.real_package_path_used:
        raise AnalysisRequestValidationError("Cannot create real package row preview: synthetic dry-run must not use real package rows.")


def _resolve_real_package_preview_package_path(preflight: ManualEvidenceImportExecutionPreflight) -> Path:
    raw_value = preflight.package_reference.package_path.strip()
    if not raw_value:
        raise AnalysisRequestValidationError("Cannot create real package row preview: package_path is missing.")
    package_path = Path(raw_value).expanduser()
    if not package_path.is_absolute():
        package_path = (PROJECT_ROOT / package_path).resolve()
    else:
        package_path = package_path.resolve()
    allowed_roots = [
        (PROJECT_ROOT / "docs" / "samples").resolve(),
        _request_root().resolve(),
        (PROJECT_ROOT / "runtime").resolve(),
        (PROJECT_ROOT / "exports").resolve(),
    ]
    if not any(_is_relative_to(package_path, root) for root in allowed_roots):
        raise AnalysisRequestValidationError("Cannot create real package row preview: package path must stay inside allowed local package roots.")
    if not package_path.exists() or not package_path.is_dir():
        raise AnalysisRequestValidationError("Cannot create real package row preview: package path does not exist.")
    return package_path


def _validate_real_package_preview_package_files(package_path: Path, preflight: ManualEvidenceImportExecutionPreflight) -> None:
    required_files = ["manifest.json", "validation_report.json", "coverage_note.md", "evidence_items.jsonl"]
    missing = [name for name in required_files if not (package_path / name).is_file()]
    if missing:
        raise AnalysisRequestValidationError(f"Cannot create real package row preview: required package files missing ({', '.join(missing)}).")
    validation_payload = _read_safe_json_file(package_path / "validation_report.json")
    validation_errors = _extract_validation_error_count(validation_payload)
    if validation_errors > 0:
        raise AnalysisRequestValidationError("Cannot create real package row preview: validation_report errors must be 0.")
    manifest_payload = _read_safe_json_file(package_path / "manifest.json")
    package_role = str(manifest_payload.get("package_role") or preflight.package_reference.package_role or "")
    if package_role and package_role not in {"selected_public_sample", "controlled_candidate_public_sample"}:
        raise AnalysisRequestValidationError("Cannot create real package row preview: package role must be selected or controlled public sample.")
    coverage_text = (package_path / "coverage_note.md").read_text(encoding="utf-8-sig", errors="replace").lower()
    if "full-web coverage" in coverage_text or "full-platform coverage" in coverage_text or "full-thread coverage" in coverage_text:
        raise AnalysisRequestValidationError("Cannot create real package row preview: coverage note must not claim full coverage.")


def _select_review_only_case_preview(request_id: str, preview_run_id: str | None) -> RealPackageRowPreview:
    if preview_run_id:
        return read_real_package_row_preview(request_id, preview_run_id)
    previews = list_real_package_row_previews(request_id)
    if not previews:
        raise AnalysisRequestNotFoundError(f"Real package row preview for {request_id} was not found.")
    return previews[0]


def _validate_review_only_case_payload(payload: ReviewOnlyCaseCreate) -> None:
    if payload.target_case_mode not in {"new_review_case", "existing_case_review_wrapper"}:
        raise AnalysisRequestValidationError("Cannot create review-only case: target_case_mode is invalid.")
    if payload.target_case_mode == "existing_case_review_wrapper" and not (payload.target_case_id or "").strip():
        raise AnalysisRequestValidationError("Cannot create review-only case: target_case_id is required for existing_case_review_wrapper.")
    side_effect_flags = {
        "analysis_included": payload.analysis_included,
        "production_case_created": payload.production_case_created,
        "evidence_rows_imported": payload.evidence_rows_imported,
        "evidence_layer_written": payload.evidence_layer_written,
        "review_queue_created": payload.review_queue_created,
        "dedup_run": payload.dedup_run,
        "analysis_run": payload.analysis_run,
        "report_allowed": payload.report_allowed,
        "sandbox_allowed": payload.sandbox_allowed,
        "public_visible": payload.public_visible,
        "strategy_lab_allowed": payload.strategy_lab_allowed,
    }
    enabled = [name for name, value in side_effect_flags.items() if value]
    if enabled:
        raise AnalysisRequestValidationError(f"Cannot create review-only case: side effect flags must remain false ({', '.join(enabled)}).")


def _validate_review_only_case_eligibility(
    request_id: str,
    preview: RealPackageRowPreview,
    preflight: ManualEvidenceImportExecutionPreflight,
    job: ManualEvidenceImportJob,
) -> None:
    if preview.request_id != request_id:
        raise AnalysisRequestValidationError("Cannot create review-only case: preview request_id mismatch.")
    if preview.status not in {"passed", "warn"}:
        raise AnalysisRequestValidationError(f"Cannot create review-only case: real package row preview status {preview.status} is not eligible.")
    if preview.status in {"privacy_stop", "blocked"} or preview.privacy_scan.privacy_stop_triggered:
        raise AnalysisRequestValidationError("Cannot create review-only case: privacy_stop preview blocks review-only case creation.")
    if preview.readiness.can_import_now:
        raise AnalysisRequestValidationError("Cannot create review-only case: preview can_import_now must remain false.")
    enabled_now_flags = [name for name, value in preview.now_flags.model_dump().items() if value]
    if enabled_now_flags:
        raise AnalysisRequestValidationError(f"Cannot create review-only case: preview now flags must remain false ({', '.join(enabled_now_flags)}).")
    if not preview.package_reference.package_name:
        raise AnalysisRequestValidationError("Cannot create review-only case: package_name is missing.")
    if preview.rows.accepted_for_preview <= 0:
        raise AnalysisRequestValidationError("Cannot create review-only case: preview must contain at least one accepted redacted row.")
    privacy_hits = (
        preview.privacy_scan.raw_author_id_detected
        + preview.privacy_scan.raw_author_name_detected
        + preview.privacy_scan.profile_url_detected
        + preview.privacy_scan.private_message_detected
        + preview.privacy_scan.secret_like_value_detected
        + preview.privacy_scan.email_detected
        + preview.privacy_scan.phone_detected
    )
    if privacy_hits:
        raise AnalysisRequestValidationError("Cannot create review-only case: preview detected raw forbidden values or privacy risk.")
    decisions = list_evidence_import_review_decisions(request_id)
    if not decisions:
        raise AnalysisRequestNotFoundError(f"review decision for {request_id} was not found.")
    latest_decision = decisions[0]
    if latest_decision.decision != "approve_import":
        raise AnalysisRequestValidationError("Cannot create review-only case: latest review decision must be approve_import.")
    if latest_decision.decision_id != preview.decision_id:
        raise AnalysisRequestValidationError("Cannot create review-only case: preview review decision is stale.")
    if preflight.status not in {"preflight_passed", "preflight_warn"}:
        raise AnalysisRequestValidationError("Cannot create review-only case: execution preflight is not eligible.")
    if preflight.preflight_id != preview.preflight_id:
        raise AnalysisRequestValidationError("Cannot create review-only case: preflight_id mismatch.")
    if preflight.validation_summary.errors > 0:
        raise AnalysisRequestValidationError("Cannot create review-only case: validation errors must be 0.")
    if not (preflight.coverage_summary.not_full_web and preflight.coverage_summary.not_full_platform and preflight.coverage_summary.not_full_thread):
        raise AnalysisRequestValidationError("Cannot create review-only case: coverage limitations must be explicit.")
    if not (
        preflight.privacy_summary.raw_author_ids_removed
        and preflight.privacy_summary.raw_author_names_removed
        and preflight.privacy_summary.profile_urls_removed
        and preflight.privacy_summary.private_messages_excluded
    ):
        raise AnalysisRequestValidationError("Cannot create review-only case: privacy flags are incomplete.")
    if job.job_id != preview.import_job_id or job.execution_mode != "dry_run_gate":
        raise AnalysisRequestValidationError("Cannot create review-only case: dry-run import job is missing or invalid.")
    unsafe_job_flags = {
        "evidence_rows_read": job.safe_mode.get("evidence_rows_read", False),
        "evidence_rows_parsed": job.safe_mode.get("evidence_rows_parsed", False),
        "evidence_rows_imported": job.safe_mode.get("evidence_rows_imported", False),
        "production_case_created": job.safe_mode.get("production_case_created", False),
        "analysis_generated": job.safe_mode.get("analysis_generated", False),
        "report_generated": job.safe_mode.get("report_generated", False),
        "provider_execution": job.safe_mode.get("provider_execution", False),
        "collector_jobs_run": job.safe_mode.get("collector_jobs_run", False),
    }
    enabled_job_flags = [name for name, value in unsafe_job_flags.items() if value]
    if enabled_job_flags:
        raise AnalysisRequestValidationError(f"Cannot create review-only case: import job unsafe flags are true ({', '.join(enabled_job_flags)}).")


def _select_staging_import_review_case(request_id: str, review_case_id: str | None) -> ReviewOnlyCase:
    if review_case_id:
        return read_review_only_case(request_id, review_case_id)
    review_cases = list_review_only_cases(request_id)
    if not review_cases:
        raise AnalysisRequestNotFoundError(f"Review-only case for {request_id} was not found.")
    return review_cases[0]


def _select_staging_import_preview(
    request_id: str,
    review_case: ReviewOnlyCase,
    preview_run_id: str | None,
) -> RealPackageRowPreview:
    selected_preview_id = preview_run_id or review_case.source_preview_run_id
    if not selected_preview_id:
        raise AnalysisRequestNotFoundError(f"Real package row preview for review-only case {review_case.review_case_id} was not found.")
    preview = read_real_package_row_preview(request_id, selected_preview_id)
    if preview.preview_run_id != review_case.source_preview_run_id:
        raise AnalysisRequestValidationError("Cannot create review-only staging import: preview_run_id must match the review-only case source preview.")
    return preview


def _validate_staging_import_payload(payload: ReviewOnlyCaseStagingImportCreate) -> None:
    acknowledgements = {
        "acknowledge_review_only_staging": payload.acknowledge_review_only_staging,
        "acknowledge_no_evidence_layer_write": payload.acknowledge_no_evidence_layer_write,
        "acknowledge_no_production_case": payload.acknowledge_no_production_case,
        "acknowledge_no_analysis": payload.acknowledge_no_analysis,
        "acknowledge_no_report": payload.acknowledge_no_report,
    }
    missing = [name for name, value in acknowledgements.items() if not value]
    if missing:
        raise AnalysisRequestValidationError(f"Cannot create review-only staging import: acknowledgement flags are required ({', '.join(missing)}).")
    if payload.package_path:
        raise AnalysisRequestValidationError("Cannot create review-only staging import: package_path is not accepted; staging uses redacted preview rows only.")
    if payload.target_production_case_id:
        raise AnalysisRequestValidationError("Cannot create review-only staging import: production_case_id is not allowed.")
    side_effect_flags = {
        "production_case_created": payload.production_case_created,
        "evidence_rows_imported": payload.evidence_rows_imported,
        "evidence_layer_written": payload.evidence_layer_written,
        "review_queue_created": payload.review_queue_created,
        "dedup_run": payload.dedup_run,
        "analysis_run": payload.analysis_run,
        "report_generated": payload.report_generated,
        "sandbox_generated": payload.sandbox_generated,
        "public_event_generated": payload.public_event_generated,
        "write_evidence_layer_now": payload.write_evidence_layer_now,
        "run_analysis_now": payload.run_analysis_now,
    }
    enabled = [name for name, value in side_effect_flags.items() if value]
    if enabled:
        raise AnalysisRequestValidationError(f"Cannot create review-only staging import: side effect flags must remain false ({', '.join(enabled)}).")


def _validate_staging_import_eligibility(
    request_id: str,
    review_case: ReviewOnlyCase,
    preview: RealPackageRowPreview,
) -> None:
    if review_case.request_id != request_id:
        raise AnalysisRequestValidationError("Cannot create review-only staging import: review-only case request_id mismatch.")
    if review_case.status not in {"draft", "staging_pending"}:
        raise AnalysisRequestValidationError("Cannot create review-only staging import: review-only case status is not eligible.")
    if review_case.visibility != "internal_review_only":
        raise AnalysisRequestValidationError("Cannot create review-only staging import: review-only case must be internal_review_only.")
    review_case_flags = {
        "analysis_included": review_case.analysis_included,
        "production_case_created": review_case.production_case_created,
        "evidence_rows_imported": review_case.evidence_rows_imported,
        "evidence_layer_written": review_case.evidence_layer_written,
        "review_queue_created": review_case.review_queue_created,
        "dedup_run": review_case.dedup_run,
        "analysis_run": review_case.analysis_run,
    }
    enabled_review_case_flags = [name for name, value in review_case_flags.items() if value]
    if enabled_review_case_flags:
        raise AnalysisRequestValidationError(
            f"Cannot create review-only staging import: review-only case unsafe flags must remain false ({', '.join(enabled_review_case_flags)})."
        )
    if list_review_only_case_staging_imports(request_id):
        matching = [item for item in list_review_only_case_staging_imports(request_id) if item.review_case_id == review_case.review_case_id]
        if matching:
            raise AnalysisRequestValidationError("Cannot create review-only staging import: review-only case already has staging import.")
    if preview.request_id != request_id:
        raise AnalysisRequestValidationError("Cannot create review-only staging import: preview request_id mismatch.")
    if preview.status not in {"passed", "warn"}:
        raise AnalysisRequestValidationError(f"Cannot create review-only staging import: real package row preview status {preview.status} is not eligible.")
    if preview.status in {"privacy_stop", "blocked"} or preview.privacy_scan.privacy_stop_triggered:
        raise AnalysisRequestValidationError("Cannot create review-only staging import: privacy_stop preview blocks staging.")
    if not preview.redacted_preview_rows or preview.rows.accepted_for_preview <= 0:
        raise AnalysisRequestValidationError("Cannot create review-only staging import: no accepted redacted preview rows are available.")
    enabled_now_flags = [name for name, value in preview.now_flags.model_dump().items() if value]
    if enabled_now_flags:
        raise AnalysisRequestValidationError(f"Cannot create review-only staging import: preview now flags must remain false ({', '.join(enabled_now_flags)}).")
    if review_case.source_import_job_id != preview.import_job_id:
        raise AnalysisRequestValidationError("Cannot create review-only staging import: import_job_id mismatch.")
    decisions = list_evidence_import_review_decisions(request_id)
    if not decisions:
        raise AnalysisRequestNotFoundError(f"review decision for {request_id} was not found.")
    latest_decision = decisions[0]
    if latest_decision.decision != "approve_import":
        raise AnalysisRequestValidationError("Cannot create review-only staging import: latest review decision must be approve_import.")
    if latest_decision.decision_id != preview.decision_id:
        raise AnalysisRequestValidationError("Cannot create review-only staging import: preview review decision is stale.")
    privacy_hits = (
        preview.privacy_scan.raw_author_id_detected
        + preview.privacy_scan.raw_author_name_detected
        + preview.privacy_scan.profile_url_detected
        + preview.privacy_scan.private_message_detected
        + preview.privacy_scan.secret_like_value_detected
        + preview.privacy_scan.email_detected
        + preview.privacy_scan.phone_detected
    )
    if privacy_hits:
        raise AnalysisRequestValidationError("Cannot create review-only staging import: preview detected raw forbidden values or privacy risk.")
    forbidden_preview_rows = [
        row.row_index
        for row in preview.redacted_preview_rows
        if row.status != "accepted_for_preview" or not row.privacy_check.passed or row.privacy_check.forbidden_fields_detected
    ]
    if forbidden_preview_rows:
        raise AnalysisRequestValidationError("Cannot create review-only staging import: preview rows contain forbidden fields.")


def _candidate_from_redacted_preview_row(
    row: RealPackageRowPreviewRow,
    *,
    staging_import_id: str,
    review_case: ReviewOnlyCase,
    preview: RealPackageRowPreview,
    created_at: datetime,
) -> StagedEvidenceCandidate:
    staging_id = f"staged_candidate_{row.row_index}_{uuid.uuid4().hex[:8]}"
    return StagedEvidenceCandidate(
        staging_id=staging_id,
        staging_import_id=staging_import_id,
        review_case_id=review_case.review_case_id,
        request_id=review_case.request_id,
        package_name=preview.package_reference.package_name,
        source_preview_run_id=preview.preview_run_id,
        source_preview_row_index=row.row_index,
        created_at=created_at,
        evidence_candidate=StagedEvidenceCandidatePreview(
            evidence_type=row.evidence_candidate.evidence_type,
            platform=row.evidence_candidate.platform,
            source_url=row.evidence_candidate.source_url,
            title_preview=row.evidence_candidate.title_preview,
            body_text_preview=row.evidence_candidate.body_text_preview,
            created_at=row.evidence_candidate.created_at,
            language=row.evidence_candidate.language,
            safe_counts=row.evidence_candidate.counts,
        ),
        governance=ReviewOnlyStagedGovernance(),
        privacy=StagedEvidenceCandidatePrivacy(),
        dedup=StagedEvidenceCandidateDedup(),
        audit=StagedEvidenceCandidateAudit(staging_import_id=staging_import_id, created_at=created_at),
    )


def _select_review_queue_init_review_case(request_id: str, review_case_id: str | None) -> ReviewOnlyCase:
    if review_case_id:
        return read_review_only_case(request_id, review_case_id)
    review_cases = list_review_only_cases(request_id)
    if not review_cases:
        raise AnalysisRequestNotFoundError(f"Review-only case for {request_id} was not found.")
    return review_cases[0]


def _select_review_queue_init_staging_import(
    request_id: str,
    review_case: ReviewOnlyCase,
    staging_import_id: str | None,
) -> ReviewOnlyCaseStagingImport:
    if staging_import_id:
        staging_import = read_review_only_case_staging_import(request_id, staging_import_id)
    else:
        imports = [item for item in list_review_only_case_staging_imports(request_id) if item.review_case_id == review_case.review_case_id]
        if not imports:
            raise AnalysisRequestNotFoundError(f"Review-only staging import for review-only case {review_case.review_case_id} was not found.")
        staging_import = imports[0]
    if staging_import.review_case_id != review_case.review_case_id:
        raise AnalysisRequestValidationError("Cannot create review queue initialization: staging import must belong to the selected review-only case.")
    return staging_import


def _validate_review_queue_init_payload(payload: ReviewQueueInitializationCreate) -> None:
    acknowledgements = {
        "acknowledge_review_only_queue": payload.acknowledge_review_only_queue,
        "acknowledge_no_evidence_layer_write": payload.acknowledge_no_evidence_layer_write,
        "acknowledge_no_production_case": payload.acknowledge_no_production_case,
        "acknowledge_no_dedup": payload.acknowledge_no_dedup,
        "acknowledge_no_analysis": payload.acknowledge_no_analysis,
        "acknowledge_no_report": payload.acknowledge_no_report,
    }
    missing = [name for name, value in acknowledgements.items() if not value]
    if missing:
        raise AnalysisRequestValidationError(f"Cannot create review queue initialization: acknowledgement flags are required ({', '.join(missing)}).")
    if payload.package_path:
        raise AnalysisRequestValidationError("Cannot create review queue initialization: package_path is not accepted; queue uses staged evidence candidates only.")
    if payload.target_production_case_id or payload.production_case_id:
        raise AnalysisRequestValidationError("Cannot create review queue initialization: production_case_id is not allowed.")
    side_effect_flags = {
        "production_case_created": payload.production_case_created,
        "evidence_layer_written": payload.evidence_layer_written,
        "production_review_queue_created": payload.production_review_queue_created,
        "analysis_included": payload.analysis_included,
        "dedup_run": payload.dedup_run,
        "analysis_run": payload.analysis_run,
        "report_generated": payload.report_generated,
        "sandbox_generated": payload.sandbox_generated,
        "public_event_generated": payload.public_event_generated,
        "write_evidence_layer_now": payload.write_evidence_layer_now,
        "run_analysis_now": payload.run_analysis_now,
    }
    enabled = [name for name, value in side_effect_flags.items() if value]
    if enabled:
        raise AnalysisRequestValidationError(f"Cannot create review queue initialization: side effect flags must remain false ({', '.join(enabled)}).")


def _validate_review_queue_init_eligibility(
    request_id: str,
    review_case: ReviewOnlyCase,
    staging_import: ReviewOnlyCaseStagingImport,
    candidate_batch: StagedEvidenceCandidateBatch,
) -> None:
    if review_case.request_id != request_id:
        raise AnalysisRequestValidationError("Cannot create review queue initialization: review-only case request_id mismatch.")
    if review_case.status not in {"draft", "staging_pending"}:
        raise AnalysisRequestValidationError("Cannot create review queue initialization: review-only case status is not eligible.")
    if review_case.visibility != "internal_review_only":
        raise AnalysisRequestValidationError("Cannot create review queue initialization: review-only case must be internal_review_only.")
    review_case_flags = {
        "analysis_included": review_case.analysis_included,
        "production_case_created": review_case.production_case_created,
        "evidence_layer_written": review_case.evidence_layer_written,
        "review_queue_created": review_case.review_queue_created,
        "dedup_run": review_case.dedup_run,
        "analysis_run": review_case.analysis_run,
    }
    enabled_review_case_flags = [name for name, value in review_case_flags.items() if value]
    if enabled_review_case_flags:
        raise AnalysisRequestValidationError(
            f"Cannot create review queue initialization: review-only case unsafe flags must remain false ({', '.join(enabled_review_case_flags)})."
        )
    matching_existing = [
        item for item in list_review_queue_initializations(request_id)
        if item.review_case_id == review_case.review_case_id or item.staging_import_id == staging_import.staging_import_id
    ]
    if matching_existing:
        raise AnalysisRequestValidationError("Cannot create review queue initialization: review-only case already has review queue initialization.")
    if staging_import.request_id != request_id:
        raise AnalysisRequestValidationError("Cannot create review queue initialization: staging import request_id mismatch.")
    if staging_import.status not in {"completed", "partial"}:
        raise AnalysisRequestValidationError(f"Cannot create review queue initialization: staging import status {staging_import.status} is not eligible.")
    if staging_import.status in {"privacy_stop", "blocked"}:
        raise AnalysisRequestValidationError("Cannot create review queue initialization: privacy_stop or blocked staging import is not eligible.")
    if staging_import.readiness.state != "staged_for_review_only":
        raise AnalysisRequestValidationError("Cannot create review queue initialization: staging import readiness must be staged_for_review_only.")
    if staging_import.target.production_case_created or staging_import.target.evidence_layer_written:
        raise AnalysisRequestValidationError("Cannot create review queue initialization: staging import target has unsafe production flags.")
    if candidate_batch.request_id != request_id or candidate_batch.staging_import_id != staging_import.staging_import_id:
        raise AnalysisRequestValidationError("Cannot create review queue initialization: staged candidate batch does not match the staging import.")
    if not candidate_batch.candidates:
        raise AnalysisRequestValidationError("Cannot create review queue initialization: staged candidate batch has no candidates.")
    decisions = list_evidence_import_review_decisions(request_id)
    if not decisions:
        raise AnalysisRequestNotFoundError(f"review decision for {request_id} was not found.")
    latest_decision = decisions[0]
    if latest_decision.decision != "approve_import":
        raise AnalysisRequestValidationError("Cannot create review queue initialization: latest review decision must be approve_import.")
    unsafe_candidate_indexes = [
        index
        for index, candidate in enumerate(candidate_batch.candidates)
        if not _staged_candidate_is_queue_eligible(candidate)
    ]
    if unsafe_candidate_indexes:
        raise AnalysisRequestValidationError("Cannot create review queue initialization: staged candidates contain forbidden or unsafe fields.")


def _staged_candidate_is_queue_eligible(candidate: StagedEvidenceCandidate) -> bool:
    if candidate.row_status != "accepted_for_review":
        return False
    governance = candidate.governance
    if governance.review_status != "review_needed":
        return False
    if governance.verification_status != "source_url_provided_unverified":
        return False
    if governance.trust_label != "medium_low":
        return False
    if governance.analysis_included or governance.public_visible or governance.report_visible or governance.sandbox_visible:
        return False
    if not governance.dedup_required or not governance.audit_required:
        return False
    privacy = candidate.privacy
    if not privacy.passed:
        return False
    if privacy.raw_author_id_present or privacy.raw_author_name_present or privacy.profile_url_present or privacy.private_message_present:
        return False
    candidate_text = " ".join(
        [
            candidate.evidence_candidate.title_preview,
            candidate.evidence_candidate.body_text_preview,
            candidate.evidence_candidate.source_url,
        ]
    )
    if EMAIL_PATTERN.search(candidate_text) or PHONE_PATTERN.search(candidate_text):
        return False
    lowered = candidate_text.lower()
    if any(pattern in lowered for pattern in ROW_READER_SECRET_PATTERNS):
        return False
    if not (candidate.evidence_candidate.title_preview or candidate.evidence_candidate.body_text_preview or candidate.evidence_candidate.source_url):
        return False
    return True


def _review_queue_item_from_staged_candidate(
    candidate: StagedEvidenceCandidate,
    *,
    queue_init_id: str,
    created_at: datetime,
    created_by: str,
) -> ReviewQueueItem:
    review_item_id = f"review_queue_item_{candidate.source_preview_row_index}_{uuid.uuid4().hex[:8]}"
    return ReviewQueueItem(
        review_item_id=review_item_id,
        queue_init_id=queue_init_id,
        review_case_id=candidate.review_case_id,
        staging_import_id=candidate.staging_import_id,
        staging_id=candidate.staging_id,
        request_id=candidate.request_id,
        package_name=candidate.package_name,
        created_at=created_at,
        created_by=created_by,
        queue_status="review_needed",
        evidence_candidate=candidate.evidence_candidate,
        governance=ReviewOnlyStagedGovernance(),
        privacy=StagedEvidenceCandidatePrivacy(
            from_redacted_preview=True,
            raw_author_id_present=False,
            raw_author_name_present=False,
            profile_url_present=False,
            private_message_present=False,
            passed=True,
        ),
        dedup=ReviewQueueItemDedup(),
        audit=ReviewQueueItemAudit(queue_init_id=queue_init_id, created_at=created_at),
    )


def _find_review_queue_item_batch(request_id: str, review_item_id: str) -> tuple[Path, ReviewQueueItemBatch, int]:
    _validate_request_id(request_id)
    root = _ensure_root()
    for path in sorted((root / "review_queue_items").glob(f"{request_id}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            batch = ReviewQueueItemBatch.model_validate(parsed)
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
        for index, item in enumerate(batch.items):
            if item.review_item_id == review_item_id:
                return path, batch, index
    raise AnalysisRequestNotFoundError(f"Review queue item {review_item_id} for {request_id} was not found.")


def _validate_review_queue_action_payload(payload: ReviewQueueActionRequest) -> None:
    if not payload.reviewer_label or not payload.reviewer_label.strip():
        raise AnalysisRequestValidationError("Cannot create review queue action: reviewer_label is required.")
    acknowledgements = {
        "acknowledge_review_only_action": payload.acknowledge_review_only_action,
        "acknowledge_no_evidence_layer_write": payload.acknowledge_no_evidence_layer_write,
        "acknowledge_no_production_case": payload.acknowledge_no_production_case,
        "acknowledge_no_dedup": payload.acknowledge_no_dedup,
        "acknowledge_no_analysis": payload.acknowledge_no_analysis,
        "acknowledge_no_report": payload.acknowledge_no_report,
    }
    missing = [name for name, value in acknowledgements.items() if not value]
    if missing:
        raise AnalysisRequestValidationError(f"Cannot create review queue action: acknowledgement flags are required ({', '.join(missing)}).")
    note_required_actions = {"reject", "mark_weak", "request_more_source", "merge_duplicate", "hold_for_privacy_review", "reset_review"}
    if payload.action in note_required_actions and not payload.note.strip():
        raise AnalysisRequestValidationError("Cannot create review queue action: note is required for this action.")
    if payload.production_case_id or payload.target_production_case_id:
        raise AnalysisRequestValidationError("Cannot create review queue action: production_case_id is not allowed.")
    if payload.trust_label == "high":
        raise AnalysisRequestValidationError("Cannot create review queue action: trust_label high is not allowed in review-only runtime.")
    if payload.verification_status and payload.verification_status.startswith("verified_by_"):
        raise AnalysisRequestValidationError("Cannot create review queue action: verification upgrade is not allowed in review-only runtime.")
    side_effect_flags = {
        "production_case_created": payload.production_case_created,
        "evidence_layer_written": payload.evidence_layer_written,
        "production_review_queue_created": payload.production_review_queue_created,
        "analysis_included": payload.analysis_included,
        "dedup_run": payload.dedup_run,
        "analysis_run": payload.analysis_run,
        "report_generated": payload.report_generated,
        "sandbox_generated": payload.sandbox_generated,
        "public_event_generated": payload.public_event_generated,
        "write_evidence_layer_now": payload.write_evidence_layer_now,
        "run_dedup_now": payload.run_dedup_now,
        "run_analysis_now": payload.run_analysis_now,
    }
    enabled = [name for name, value in side_effect_flags.items() if value]
    if enabled:
        raise AnalysisRequestValidationError(f"Cannot create review queue action: side effect flags must remain false ({', '.join(enabled)}).")


def _validate_review_queue_action_eligibility(
    request_id: str,
    queue_init: ReviewQueueInitialization,
    review_case: ReviewOnlyCase,
    batch: ReviewQueueItemBatch,
    item: ReviewQueueItem,
    payload: ReviewQueueActionRequest,
) -> None:
    if item.request_id != request_id or queue_init.request_id != request_id or review_case.request_id != request_id or batch.request_id != request_id:
        raise AnalysisRequestValidationError("Cannot create review queue action: request_id mismatch.")
    if item.queue_init_id != queue_init.queue_init_id or batch.queue_init_id != queue_init.queue_init_id:
        raise AnalysisRequestValidationError("Cannot create review queue action: queue initialization mismatch.")
    if item.review_case_id != review_case.review_case_id or queue_init.review_case_id != review_case.review_case_id:
        raise AnalysisRequestValidationError("Cannot create review queue action: review-only case mismatch.")
    if queue_init.target.production_case_created or queue_init.target.evidence_layer_written or queue_init.target.production_review_queue_created:
        raise AnalysisRequestValidationError("Cannot create review queue action: queue initialization has unsafe production flags.")
    if review_case.production_case_created or review_case.evidence_layer_written or review_case.review_queue_created:
        raise AnalysisRequestValidationError("Cannot create review queue action: review-only case has unsafe production flags.")
    if review_case.visibility != "internal_review_only":
        raise AnalysisRequestValidationError("Cannot create review queue action: review-only case must be internal_review_only.")
    if item.governance.analysis_included or item.governance.public_visible or item.governance.report_visible or item.governance.sandbox_visible:
        raise AnalysisRequestValidationError("Cannot create review queue action: item visibility or analysis flags must remain false.")
    if _review_queue_item_has_forbidden_fields(item):
        raise AnalysisRequestValidationError("Cannot create review queue action: item contains forbidden raw author, secret, email, phone, or private fields.")
    allowed_from = {
        "approve": {"review_needed", "marked_weak", "needs_more_source"},
        "reject": {"review_needed", "approved", "marked_weak", "needs_more_source"},
        "mark_weak": {"review_needed", "approved", "needs_more_source"},
        "request_more_source": {"review_needed", "approved", "marked_weak"},
        "merge_duplicate": {"review_needed", "approved", "marked_weak"},
        "hold_for_privacy_review": {"review_needed", "approved", "marked_weak", "needs_more_source", "duplicate_merged"},
        "reset_review": {"approved", "rejected", "marked_weak", "needs_more_source", "duplicate_merged", "privacy_hold"},
    }
    if item.queue_status not in allowed_from[payload.action]:
        raise AnalysisRequestValidationError(
            f"Cannot create review queue action: transition from {item.queue_status} via {payload.action} is not allowed."
        )


def _review_queue_item_has_forbidden_fields(item: ReviewQueueItem) -> bool:
    privacy = item.privacy
    if not privacy.passed:
        return True
    if privacy.raw_author_id_present or privacy.raw_author_name_present or privacy.profile_url_present or privacy.private_message_present:
        return True
    candidate_text = " ".join(
        [
            item.evidence_candidate.title_preview,
            item.evidence_candidate.body_text_preview,
            item.evidence_candidate.source_url,
        ]
    )
    if EMAIL_PATTERN.search(candidate_text) or PHONE_PATTERN.search(candidate_text):
        return True
    lowered = candidate_text.lower()
    return any(pattern in lowered for pattern in ROW_READER_SECRET_PATTERNS)


def _review_queue_action_effect(action: str) -> tuple[str, str, str]:
    if action == "approve":
        return "approved", "eligible_for_future_dedup", "not_run"
    if action == "reject":
        return "rejected", "blocked", "not_run"
    if action == "mark_weak":
        return "marked_weak", "still_excluded", "not_run"
    if action == "request_more_source":
        return "needs_more_source", "blocked", "not_run"
    if action == "merge_duplicate":
        return "duplicate_merged", "still_excluded", "duplicate_candidate_marked"
    if action == "hold_for_privacy_review":
        return "privacy_hold", "blocked", "not_run"
    if action == "reset_review":
        return "review_needed", "still_excluded", "not_run"
    raise AnalysisRequestValidationError(f"Cannot create review queue action: action {action} is not supported.")


def _review_queue_action_downstream_blockers(action: str) -> list[str]:
    blockers = ["analysis_not_allowed_now", "dedup_not_run", "production_promotion_not_allowed_now"]
    if action in {"reject", "request_more_source", "hold_for_privacy_review"}:
        blockers.append(f"{action}_blocks_promotion")
    if action == "merge_duplicate":
        blockers.append("duplicate_requires_future_dedup_gate")
    if action == "mark_weak":
        blockers.append("weak_evidence_requires_warning")
    return blockers


def _validate_review_queue_completion_gate_payload(payload: ReviewQueueCompletionGateRequest) -> None:
    if not payload.queue_init_id or not payload.queue_init_id.strip():
        raise AnalysisRequestValidationError("Cannot create review queue completion gate: queue_init_id is required.")
    acknowledgements = {
        "acknowledge_completion_is_not_dedup": payload.acknowledge_completion_is_not_dedup,
        "acknowledge_completion_is_not_analysis": payload.acknowledge_completion_is_not_analysis,
        "acknowledge_no_evidence_layer_write": payload.acknowledge_no_evidence_layer_write,
        "acknowledge_no_production_case": payload.acknowledge_no_production_case,
        "acknowledge_no_report": payload.acknowledge_no_report,
    }
    missing = [name for name, value in acknowledgements.items() if not value]
    if missing:
        raise AnalysisRequestValidationError(f"Cannot create review queue completion gate: acknowledgement flags are required ({', '.join(missing)}).")
    if payload.production_case_id or payload.target_production_case_id:
        raise AnalysisRequestValidationError("Cannot create review queue completion gate: production_case_id is not allowed.")
    side_effect_flags = {
        "production_case_created": payload.production_case_created,
        "evidence_layer_written": payload.evidence_layer_written,
        "production_review_queue_created": payload.production_review_queue_created,
        "analysis_included": payload.analysis_included,
        "dedup_run": payload.dedup_run,
        "analysis_run": payload.analysis_run,
        "report_generated": payload.report_generated,
        "sandbox_generated": payload.sandbox_generated,
        "public_event_generated": payload.public_event_generated,
        "write_evidence_layer_now": payload.write_evidence_layer_now,
        "create_production_case_now": payload.create_production_case_now,
        "create_production_review_queue_now": payload.create_production_review_queue_now,
        "run_dedup_now": payload.run_dedup_now,
        "run_analysis_now": payload.run_analysis_now,
        "generate_report_now": payload.generate_report_now,
        "generate_sandbox_now": payload.generate_sandbox_now,
        "generate_public_event_now": payload.generate_public_event_now,
    }
    enabled = [name for name, value in side_effect_flags.items() if value]
    if enabled:
        raise AnalysisRequestValidationError(f"Cannot create review queue completion gate: side effect flags must remain false ({', '.join(enabled)}).")


def _build_review_queue_completion_gate(
    request_id: str,
    payload: ReviewQueueCompletionGateRequest,
    queue_init: ReviewQueueInitialization,
    review_case: ReviewOnlyCase,
    batch: ReviewQueueItemBatch,
) -> ReviewQueueCompletionGate:
    created_at = datetime.now(timezone.utc)
    counts = ReviewQueueCompletionGateCounts(total_items=len(batch.items))
    hard_blockers: list[str] = []
    incomplete_reasons: list[str] = []
    warnings: list[str] = []

    if queue_init.request_id != request_id or review_case.request_id != request_id or batch.request_id != request_id:
        hard_blockers.append("request_id_mismatch")
    if payload.review_case_id and payload.review_case_id != queue_init.review_case_id:
        hard_blockers.append("review_case_id_mismatch")
    if queue_init.queue_init_id != batch.queue_init_id:
        hard_blockers.append("queue_init_batch_mismatch")
    if queue_init.review_case_id != review_case.review_case_id or batch.review_case_id != review_case.review_case_id:
        hard_blockers.append("review_only_case_mismatch")
    if review_case.status not in {"draft", "staging_pending"}:
        hard_blockers.append(f"review_only_case_status_{review_case.status}")
    if review_case.visibility != "internal_review_only":
        hard_blockers.append("review_only_case_not_internal")
    if review_case.production_case_created or review_case.evidence_layer_written or review_case.review_queue_created:
        hard_blockers.append("review_only_case_unsafe_production_flags")
    if review_case.dedup_run or review_case.analysis_run or review_case.analysis_included:
        hard_blockers.append("review_only_case_unsafe_analysis_flags")
    if queue_init.target.production_case_created or queue_init.target.evidence_layer_written or queue_init.target.production_review_queue_created:
        hard_blockers.append("queue_init_unsafe_production_flags")
    if counts.total_items == 0:
        incomplete_reasons.append("no_review_queue_items")

    audits = list_review_queue_action_audits(request_id)
    audits_by_item: dict[str, list[ReviewQueueActionAudit]] = {}
    for audit in audits:
        if audit.queue_init_id != queue_init.queue_init_id:
            continue
        audits_by_item.setdefault(audit.review_item_id, []).append(audit)

    reviewer_labels = sorted({audit.reviewer_label for item_audits in audits_by_item.values() for audit in item_audits if audit.reviewer_label})
    latest_action_at = max(
        (audit.reviewed_at for item_audits in audits_by_item.values() for audit in item_audits),
        default=None,
    )
    items_with_audit = 0
    items_missing_audit = 0

    known_statuses = {
        "review_needed",
        "approved",
        "rejected",
        "marked_weak",
        "needs_more_source",
        "duplicate_merged",
        "privacy_hold",
    }
    for item in batch.items:
        status = item.queue_status
        if status not in known_statuses:
            hard_blockers.append("unknown_review_queue_status")
            continue
        setattr(counts, status, getattr(counts, status) + 1)
        if status != "review_needed":
            counts.reviewed_count += 1
            if audits_by_item.get(item.review_item_id):
                items_with_audit += 1
            else:
                items_missing_audit += 1
                incomplete_reasons.append("missing_action_audit_for_reviewed_item")
        if item.request_id != request_id or item.queue_init_id != queue_init.queue_init_id or item.review_case_id != review_case.review_case_id:
            hard_blockers.append("review_queue_item_parent_mismatch")
        if item.governance.analysis_included or item.governance.public_visible or item.governance.report_visible or item.governance.sandbox_visible:
            hard_blockers.append("item_visibility_or_analysis_flag_true")
        if _review_queue_item_has_forbidden_fields(item):
            hard_blockers.append("raw_forbidden_field_risk")
        if status == "needs_more_source" and not payload.allow_deferred_items:
            incomplete_reasons.append("needs_more_source_items_present")
        if status == "needs_more_source" and payload.allow_deferred_items:
            warnings.append("needs_more_source items were treated as deferred for this local completion gate.")
        if status == "marked_weak":
            warnings.append("marked_weak evidence remains warning-marked and analysis-excluded.")
        if status == "rejected" and item.governance.analysis_included:
            hard_blockers.append("rejected_item_analysis_included")
        if status == "approved" and item.governance.analysis_included:
            hard_blockers.append("approved_item_analysis_included")
        if status == "duplicate_merged" and item.dedup.may_amplify_risk:
            hard_blockers.append("duplicate_may_amplify_risk")
        if status == "duplicate_merged" and item.dedup.dedup_status != "duplicate_candidate_marked":
            warnings.append("duplicate_merged item is marked for future dedup preview but dedup has not run.")

    counts.reviewed_ratio = round(counts.reviewed_count / counts.total_items, 4) if counts.total_items else 0.0
    if counts.reviewed_ratio < payload.minimum_reviewed_ratio:
        incomplete_reasons.append("reviewed_ratio_below_minimum")
    if items_missing_audit:
        warnings.append("Reviewed items without action audit cannot pass completion gate.")

    status = "complete_enough_for_future_dedup_preview"
    if hard_blockers:
        status = "blocked"
    elif counts.privacy_hold:
        status = "privacy_hold"
        incomplete_reasons.append("privacy_hold_items_present")
    elif incomplete_reasons:
        status = "incomplete"

    blocked_reasons = _unique_preserve_order([*hard_blockers, *incomplete_reasons])
    eligible = status == "complete_enough_for_future_dedup_preview"
    gate_id = _new_review_queue_completion_gate_id()
    return ReviewQueueCompletionGate(
        completion_gate_id=gate_id,
        request_id=request_id,
        review_case_id=review_case.review_case_id,
        queue_init_id=queue_init.queue_init_id,
        created_at=created_at,
        created_by=payload.created_by or "sentigraph_local_ui",
        status=status,
        counts=counts,
        audit_summary=ReviewQueueCompletionGateAuditSummary(
            items_with_audit=items_with_audit,
            items_missing_audit=items_missing_audit,
            latest_action_at=latest_action_at,
            reviewer_labels=reviewer_labels,
        ),
        downstream_eligibility=ReviewQueueCompletionGateDownstreamEligibility(
            eligible_for_future_dedup_preview=eligible,
            can_run_dedup_now=False,
            can_run_analysis_now=False,
            can_generate_report_now=False,
            can_generate_sandbox_now=False,
            can_create_public_event_now=False,
        ),
        blocked_reasons=blocked_reasons,
        warnings=_unique_preserve_order(warnings),
        boundary_notes=[
            "Completion gate evaluates local review-only queue status only.",
            "Completion does not run dedup.",
            "Completion does not run analysis.",
            "Completion does not make items public.",
            "Completion does not write the production Evidence Layer.",
            "Completion only allows future dedup preview consideration when eligible.",
            "Rejected evidence remains audit-visible but analysis-excluded.",
            "Weak evidence remains warning-marked.",
            "Duplicate evidence must not amplify risk.",
        ],
        recommended_next_steps=_review_queue_completion_next_steps(status),
    )


def _validate_dedup_preview_payload(payload: DedupPreviewRequest) -> None:
    if not payload.completion_gate_id or not payload.completion_gate_id.strip():
        raise AnalysisRequestValidationError("Cannot create dedup preview: completion_gate_id is required.")
    acknowledgements = {
        "acknowledge_dedup_preview_only": payload.acknowledge_dedup_preview_only,
        "acknowledge_no_production_dedup": payload.acknowledge_no_production_dedup,
        "acknowledge_no_evidence_layer_write": payload.acknowledge_no_evidence_layer_write,
        "acknowledge_no_analysis": payload.acknowledge_no_analysis,
        "acknowledge_no_report": payload.acknowledge_no_report,
    }
    missing = [name for name, value in acknowledgements.items() if not value]
    if missing:
        raise AnalysisRequestValidationError(f"Cannot create dedup preview: acknowledgement flags are required ({', '.join(missing)}).")
    if payload.production_case_id or payload.target_production_case_id:
        raise AnalysisRequestValidationError("Cannot create dedup preview: production_case_id is not allowed.")
    side_effect_flags = {
        "evidence_layer_written": payload.evidence_layer_written,
        "production_case_created": payload.production_case_created,
        "production_review_queue_created": payload.production_review_queue_created,
        "production_dedup_run": payload.production_dedup_run,
        "analysis_included": payload.analysis_included,
        "analysis_run": payload.analysis_run,
        "report_generated": payload.report_generated,
        "sandbox_generated": payload.sandbox_generated,
        "public_event_generated": payload.public_event_generated,
        "write_evidence_layer_now": payload.write_evidence_layer_now,
        "create_production_case_now": payload.create_production_case_now,
        "create_production_review_queue_now": payload.create_production_review_queue_now,
        "run_dedup_now": payload.run_dedup_now,
        "run_analysis_now": payload.run_analysis_now,
        "generate_report_now": payload.generate_report_now,
        "generate_sandbox_now": payload.generate_sandbox_now,
        "generate_public_event_now": payload.generate_public_event_now,
    }
    enabled = [name for name, value in side_effect_flags.items() if value]
    if enabled:
        raise AnalysisRequestValidationError(f"Cannot create dedup preview: side effect flags must remain false ({', '.join(enabled)}).")


def _build_dedup_preview(
    request_id: str,
    payload: DedupPreviewRequest,
    gate: ReviewQueueCompletionGate,
    queue_init: ReviewQueueInitialization,
    review_case: ReviewOnlyCase,
    batch: ReviewQueueItemBatch,
) -> DedupPreview:
    preview_id = _new_dedup_preview_id()
    allowed_statuses = ["approved"]
    if payload.include_marked_weak:
        allowed_statuses.append("marked_weak")
    if payload.include_duplicate_merged:
        allowed_statuses.append("duplicate_merged")

    blockers: list[str] = []
    warnings: list[str] = []
    excluded_items: list[DedupPreviewExcludedItem] = []
    eligible_items: list[ReviewQueueItem] = []
    privacy_scan = DedupPreviewPrivacyScan()

    if gate.request_id != request_id or queue_init.request_id != request_id or review_case.request_id != request_id or batch.request_id != request_id:
        blockers.append("request_id_mismatch")
    if gate.queue_init_id != queue_init.queue_init_id or batch.queue_init_id != queue_init.queue_init_id:
        blockers.append("queue_init_mismatch")
    if gate.review_case_id != review_case.review_case_id or batch.review_case_id != review_case.review_case_id:
        blockers.append("review_case_mismatch")
    if gate.status != "complete_enough_for_future_dedup_preview":
        blockers.append("completion_gate_not_complete")
    if not gate.downstream_eligibility.eligible_for_future_dedup_preview:
        blockers.append("completion_gate_not_eligible")
    if gate.counts.privacy_hold:
        blockers.append("completion_gate_privacy_hold")
        privacy_scan.privacy_stop = True
    if review_case.production_case_created or review_case.evidence_layer_written or review_case.review_queue_created:
        blockers.append("review_only_case_unsafe_production_flags")
    if review_case.dedup_run or review_case.analysis_run or review_case.analysis_included:
        blockers.append("review_only_case_unsafe_analysis_flags")
    if queue_init.target.production_case_created or queue_init.target.evidence_layer_written or queue_init.target.production_review_queue_created:
        blockers.append("queue_init_unsafe_production_flags")

    for item in batch.items:
        exclude_reason = ""
        if item.request_id != request_id or item.queue_init_id != queue_init.queue_init_id or item.review_case_id != review_case.review_case_id:
            blockers.append("review_queue_item_parent_mismatch")
            exclude_reason = "parent_mismatch"
        elif item.governance.analysis_included or item.governance.public_visible or item.governance.report_visible or item.governance.sandbox_visible:
            blockers.append("item_visibility_or_analysis_flag_true")
            exclude_reason = "unsafe_visibility_or_analysis_flag"
        elif _review_queue_item_has_forbidden_fields(item):
            privacy_scan.raw_identifier_found = True
            privacy_scan.secret_like_found = True
            privacy_scan.privacy_stop = True
            blockers.append("raw_forbidden_field_risk")
            exclude_reason = "privacy_scan_failed"
        elif not _dedup_item_has_safe_content(item):
            exclude_reason = "missing_safe_content"
        elif item.queue_status == "marked_weak" and not payload.include_marked_weak:
            exclude_reason = "marked_weak_not_included"
        elif item.queue_status == "duplicate_merged" and not payload.include_duplicate_merged:
            exclude_reason = "duplicate_merged_not_included"
        elif item.queue_status not in allowed_statuses:
            exclude_reason = f"status_{item.queue_status}"

        if exclude_reason:
            excluded_items.append(
                DedupPreviewExcludedItem(
                    review_item_id=item.review_item_id,
                    reason=exclude_reason,
                    queue_status=item.queue_status,
                    review_status=item.governance.review_status,
                )
            )
        else:
            eligible_items.append(item)

    groups = _build_dedup_group_candidates(preview_id, review_case.review_case_id, queue_init.queue_init_id, eligible_items)
    duplicate_item_ids = {item_id for group in groups for item_id in group.item_ids}
    unique_candidate_count = len(groups) + sum(1 for item in eligible_items if item.review_item_id not in duplicate_item_ids)
    status = "preview_ready"
    if blockers:
        status = "privacy_hold" if privacy_scan.privacy_stop else "blocked"
    readiness_state = "dedup_preview_ready" if status == "preview_ready" else status
    if not groups:
        warnings.append("No duplicate group candidates were found in eligible review-only queue items.")

    return DedupPreview(
        dedup_preview_id=preview_id,
        request_id=request_id,
        review_case_id=review_case.review_case_id,
        queue_init_id=queue_init.queue_init_id,
        completion_gate_id=gate.completion_gate_id,
        created_at=datetime.now(timezone.utc),
        created_by=payload.created_by or "sentigraph_local_ui",
        status=status,
        input_scope=DedupPreviewInputScope(
            include_statuses=allowed_statuses,
            exclude_statuses=["rejected", "needs_more_source", "privacy_hold", "review_needed"],
            analysis_included=False,
        ),
        counts=DedupPreviewCounts(
            items_seen=len(batch.items),
            items_eligible_for_preview=len(eligible_items),
            items_excluded=len(excluded_items),
            duplicate_group_candidates=len(groups),
            unique_candidate_count=unique_candidate_count,
        ),
        groups=groups,
        excluded_items=excluded_items,
        privacy_scan=privacy_scan,
        readiness=DedupPreviewReadiness(
            state=readiness_state,
            can_run_dedup_now=False,
            can_run_analysis_now=False,
            requires_human_dedup_confirmation=True,
            requires_analysis_promotion_gate=True,
        ),
        blockers=_unique_preserve_order(blockers),
        warnings=_unique_preserve_order(warnings),
        boundary_notes=[
            "Dedup preview uses local review-only queue item safe fields only.",
            "Dedup preview does not run production dedup.",
            "Dedup preview does not write the production Evidence Layer.",
            "Dedup preview does not make items analysis-ready.",
            "Dedup preview does not run analysis or generate reports.",
            "Duplicate evidence must not amplify risk, sentiment, coverage, or conclusions.",
            "Human confirmation is required before any future merge effect.",
            "Provider output is evidence, not truth.",
        ],
        recommended_next_steps=_dedup_preview_next_steps(status, bool(groups)),
    )


def _build_dedup_group_candidates(
    dedup_preview_id: str,
    review_case_id: str,
    queue_init_id: str,
    items: list[ReviewQueueItem],
) -> list[DedupGroupCandidate]:
    item_by_id = {item.review_item_id: item for item in items}
    parent = {item.review_item_id: item.review_item_id for item in items}
    reasons_by_root: dict[str, set[str]] = {}

    def find(item_id: str) -> str:
        while parent[item_id] != item_id:
            parent[item_id] = parent[parent[item_id]]
            item_id = parent[item_id]
        return item_id

    def union(ids: list[str], reason: str) -> None:
        ids = sorted(set(ids))
        if len(ids) < 2:
            return
        base = find(ids[0])
        for item_id in ids[1:]:
            other = find(item_id)
            if other != base:
                parent[other] = base
        root = find(base)
        reasons_by_root.setdefault(root, set()).add(reason)

    signal_maps: dict[str, dict[str, list[str]]] = {
        "exact_url_match": {},
        "normalized_url_match": {},
        "content_preview_hash_match": {},
        "lineage_match": {},
        "reviewer_merge_hint": {},
    }
    for item in items:
        candidate = item.evidence_candidate
        if candidate.source_url.strip():
            signal_maps["exact_url_match"].setdefault(candidate.source_url.strip(), []).append(item.review_item_id)
            normalized_url = _normalize_dedup_url(candidate.source_url)
            if normalized_url:
                signal_maps["normalized_url_match"].setdefault(normalized_url, []).append(item.review_item_id)
        content_hash = _dedup_content_preview_hash(candidate.title_preview, candidate.body_text_preview)
        if content_hash:
            signal_maps["content_preview_hash_match"].setdefault(content_hash, []).append(item.review_item_id)
        if item.staging_id.strip():
            signal_maps["lineage_match"].setdefault(item.staging_id.strip(), []).append(item.review_item_id)
        if item.dedup.duplicate_group_id:
            signal_maps["reviewer_merge_hint"].setdefault(item.dedup.duplicate_group_id, []).append(item.review_item_id)

    for reason, values in signal_maps.items():
        for ids in values.values():
            union(ids, reason)

    grouped_ids: dict[str, list[str]] = {}
    for item_id in parent:
        grouped_ids.setdefault(find(item_id), []).append(item_id)
    groups: list[DedupGroupCandidate] = []
    for root, ids in grouped_ids.items():
        ids = sorted(set(ids))
        if len(ids) < 2:
            continue
        reasons = set()
        for item_id in ids:
            reasons.update(reasons_by_root.get(find(item_id), set()))
        reason = _dedup_group_reason(reasons)
        representative = _select_dedup_representative([item_by_id[item_id] for item_id in ids])
        group_hash = hashlib.sha256("|".join(ids).encode("utf-8")).hexdigest()[:12]
        groups.append(
            DedupGroupCandidate(
                group_candidate_id=f"dedup_group_candidate_{group_hash}",
                review_case_id=review_case_id,
                queue_init_id=queue_init_id,
                dedup_preview_id=dedup_preview_id,
                reason=reason,
                confidence=_dedup_group_confidence(reason, reasons),
                item_ids=ids,
                representative_item_id=representative.review_item_id if representative else ids[0],
                duplicate_count_preview=len(ids),
                may_amplify_risk=False,
                human_confirmation_required=True,
                analysis_effect="preview_only_no_analysis_effect",
                notes=[
                    "Preview-only duplicate candidate.",
                    "Human confirmation required before future merge effect.",
                    "Duplicate count is not risk or truth strength.",
                ],
            )
        )
    return sorted(groups, key=lambda group: (group.reason, group.group_candidate_id))


def _dedup_item_has_safe_content(item: ReviewQueueItem) -> bool:
    candidate = item.evidence_candidate
    return any(
        value.strip()
        for value in [
            candidate.source_url,
            candidate.title_preview,
            candidate.body_text_preview,
            item.staging_id,
            item.dedup.duplicate_group_id or "",
        ]
    )


def _normalize_dedup_url(url: str) -> str:
    text = url.strip()
    if not text:
        return ""
    fragmentless = text.split("#", 1)[0]
    base, _, query = fragmentless.partition("?")
    match = re.match(r"^(?P<scheme>[A-Za-z][A-Za-z0-9+.-]*://)(?P<host>[^/]+)(?P<path>/.*)?$", base)
    if match:
        scheme = match.group("scheme").lower()
        host = match.group("host").lower()
        path = (match.group("path") or "").rstrip("/")
        normalized_base = f"{scheme}{host}{path}"
    else:
        normalized_base = base.lower().rstrip("/")
    kept_params: list[str] = []
    for part in query.split("&"):
        if not part:
            continue
        key = part.split("=", 1)[0].lower()
        if key.startswith("utm_") or key in {"fbclid", "gclid", "yclid", "mc_cid", "mc_eid", "spm"}:
            continue
        kept_params.append(part)
    return f"{normalized_base}?{'&'.join(kept_params)}" if kept_params else normalized_base


def _dedup_content_preview_hash(title: str, body: str) -> str:
    normalized = re.sub(r"[\W_]+", " ", f"{title} {body}".lower(), flags=re.UNICODE)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    if not normalized:
        return ""
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _dedup_group_reason(reasons: set[str]) -> str:
    if len(reasons) != 1:
        return "mixed"
    return next(iter(reasons))


def _dedup_group_confidence(reason: str, reasons: set[str]) -> str:
    if reason == "mixed" or "exact_url_match" in reasons or "lineage_match" in reasons:
        return "high"
    if "normalized_url_match" in reasons:
        return "high"
    if "content_preview_hash_match" in reasons or "reviewer_merge_hint" in reasons:
        return "medium"
    return "low"


def _select_dedup_representative(items: list[ReviewQueueItem]) -> ReviewQueueItem | None:
    if not items:
        return None
    status_rank = {"approved": 0, "marked_weak": 1, "duplicate_merged": 2}

    def key(item: ReviewQueueItem) -> tuple[int, int, int, str, str]:
        candidate = item.evidence_candidate
        preview_len = len(candidate.title_preview.strip()) + len(candidate.body_text_preview.strip())
        return (
            status_rank.get(item.queue_status, 9),
            0 if candidate.source_url.strip() else 1,
            -preview_len,
            candidate.created_at or item.created_at.isoformat(),
            item.review_item_id,
        )

    return sorted(items, key=key)[0]


def _dedup_preview_next_steps(status: str, has_groups: bool) -> list[str]:
    if status != "preview_ready":
        return [
            "Resolve blockers before any future dedup preview.",
            "Do not promote evidence to analysis while blockers remain.",
        ]
    if not has_groups:
        return [
            "No duplicate group candidates found in this preview.",
            "Future analysis promotion still requires a separate gate.",
        ]
    return [
        "Review duplicate group candidates with a human reviewer.",
        "Do not use duplicate_count_preview to amplify risk or sentiment.",
        "Proceed to a future dedup group review phase before any analysis promotion.",
    ]


def _validate_dedup_group_review_action_payload(payload: DedupGroupReviewActionRequest, group_candidate_id: str) -> None:
    if payload.target_group_candidate_id and payload.target_group_candidate_id != group_candidate_id:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: target_group_candidate_id mismatch.")
    if not payload.reviewer_label.strip():
        raise AnalysisRequestValidationError("Cannot create dedup group review action: reviewer_label is required.")
    acknowledgements = {
        "acknowledge_review_only_group_action": payload.acknowledge_review_only_group_action,
        "acknowledge_no_production_dedup": payload.acknowledge_no_production_dedup,
        "acknowledge_no_evidence_layer_write": payload.acknowledge_no_evidence_layer_write,
        "acknowledge_no_analysis": payload.acknowledge_no_analysis,
        "acknowledge_no_report": payload.acknowledge_no_report,
    }
    missing = [name for name, value in acknowledgements.items() if not value]
    if missing:
        raise AnalysisRequestValidationError(f"Cannot create dedup group review action: acknowledgement flags are required ({', '.join(missing)}).")
    if payload.action != "confirm_group" and not payload.note.strip():
        raise AnalysisRequestValidationError("Cannot create dedup group review action: note is required for this action.")
    if payload.action == "change_representative" and not (payload.representative_item_id or "").strip():
        raise AnalysisRequestValidationError("Cannot create dedup group review action: representative_item_id is required.")
    if payload.action == "split_group" and not payload.split_item_ids:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: split_item_ids are required.")
    if payload.production_case_id or payload.target_production_case_id:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: production_case_id is not allowed.")
    if (payload.trust_label or "").lower() in {"high", "verified", "official", "official_api"}:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: trust upgrade is not allowed.")
    if (payload.verification_status or "").lower() in {"verified", "verified_by_official_api", "official_verified"}:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: official verification upgrade is not allowed.")
    side_effect_flags = {
        "evidence_layer_written": payload.evidence_layer_written,
        "production_case_created": payload.production_case_created,
        "production_review_queue_created": payload.production_review_queue_created,
        "production_dedup_run": payload.production_dedup_run,
        "analysis_included": payload.analysis_included,
        "analysis_run": payload.analysis_run,
        "report_generated": payload.report_generated,
        "sandbox_generated": payload.sandbox_generated,
        "public_event_generated": payload.public_event_generated,
        "write_evidence_layer_now": payload.write_evidence_layer_now,
        "create_production_case_now": payload.create_production_case_now,
        "create_production_review_queue_now": payload.create_production_review_queue_now,
        "run_production_dedup_now": payload.run_production_dedup_now,
        "run_dedup_now": payload.run_dedup_now,
        "run_analysis_now": payload.run_analysis_now,
        "generate_report_now": payload.generate_report_now,
        "generate_sandbox_now": payload.generate_sandbox_now,
        "generate_public_event_now": payload.generate_public_event_now,
    }
    enabled = [name for name, value in side_effect_flags.items() if value]
    if enabled:
        raise AnalysisRequestValidationError(f"Cannot create dedup group review action: side effect flags must remain false ({', '.join(enabled)}).")


def _validate_dedup_group_review_eligibility(
    request_id: str,
    preview: DedupPreview,
    gate: ReviewQueueCompletionGate,
    review_case: ReviewOnlyCase,
    batch: ReviewQueueItemBatch,
    group: DedupGroupCandidate,
    payload: DedupGroupReviewActionRequest,
) -> None:
    if preview.request_id != request_id or gate.request_id != request_id or review_case.request_id != request_id or batch.request_id != request_id:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: request_id mismatch.")
    if preview.completion_gate_id != gate.completion_gate_id:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: completion gate mismatch.")
    if preview.review_case_id != review_case.review_case_id or gate.review_case_id != review_case.review_case_id or batch.review_case_id != review_case.review_case_id:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: review_case_id mismatch.")
    if preview.queue_init_id != gate.queue_init_id or preview.queue_init_id != batch.queue_init_id:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: queue_init_id mismatch.")
    if group.dedup_preview_id != preview.dedup_preview_id or group.review_case_id != preview.review_case_id:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: group parent mismatch.")
    if len(group.item_ids) < 2:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: group must contain at least two item ids.")
    if group.may_amplify_risk:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: group may_amplify_risk must remain false.")
    if payload.representative_item_id and payload.representative_item_id not in group.item_ids:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: representative_item_id must be inside group.")
    if payload.split_item_ids and any(item_id not in group.item_ids for item_id in payload.split_item_ids):
        raise AnalysisRequestValidationError("Cannot create dedup group review action: split_item_ids must be inside group.")
    if len(set(payload.split_item_ids)) != len(payload.split_item_ids):
        raise AnalysisRequestValidationError("Cannot create dedup group review action: split_item_ids must be unique.")
    if review_case.production_case_created or review_case.evidence_layer_written or review_case.review_queue_created:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: review-only case has unsafe production flags.")
    if review_case.dedup_run or review_case.analysis_run or review_case.analysis_included:
        raise AnalysisRequestValidationError("Cannot create dedup group review action: review-only case has unsafe analysis flags.")
    item_map = {item.review_item_id: item for item in batch.items}
    for item_id in group.item_ids:
        item = item_map.get(item_id)
        if item is None:
            raise AnalysisRequestValidationError("Cannot create dedup group review action: group item is missing from review queue item batch.")
        if item.governance.analysis_included or item.governance.public_visible or item.governance.report_visible or item.governance.sandbox_visible:
            raise AnalysisRequestValidationError("Cannot create dedup group review action: item visibility or analysis flag is true.")
        if _review_queue_item_has_forbidden_fields(item):
            raise AnalysisRequestValidationError("Cannot create dedup group review action: group item contains forbidden raw/private fields.")


def _validate_dedup_group_review_transition(previous_status: str, action: str) -> None:
    allowed: dict[str, set[str]] = {
        "confirm_group": {"review_needed", "representative_changed", "marked_weak"},
        "split_group": {"review_needed", "confirmed", "representative_changed", "marked_weak"},
        "change_representative": {"review_needed", "confirmed", "marked_weak"},
        "mark_group_weak": {"review_needed", "confirmed", "representative_changed"},
        "reject_group": {"review_needed", "confirmed", "representative_changed", "marked_weak"},
        "request_more_source": {"review_needed", "confirmed", "representative_changed", "marked_weak"},
        "hold_group_for_privacy": {
            "review_needed",
            "confirmed",
            "split",
            "representative_changed",
            "marked_weak",
            "rejected",
            "needs_more_source",
        },
        "reset_group_review": {"confirmed", "split", "representative_changed", "marked_weak", "rejected", "needs_more_source", "privacy_hold"},
    }
    if previous_status not in allowed[action]:
        raise AnalysisRequestValidationError(
            f"Cannot create dedup group review action: transition from {previous_status} via {action} is not allowed."
        )


def _dedup_group_new_status(action: str) -> str:
    return {
        "confirm_group": "confirmed",
        "split_group": "split",
        "change_representative": "representative_changed",
        "mark_group_weak": "marked_weak",
        "reject_group": "rejected",
        "request_more_source": "needs_more_source",
        "hold_group_for_privacy": "privacy_hold",
        "reset_group_review": "review_needed",
    }[action]


def _dedup_group_analysis_effect(action: str) -> str:
    if action == "confirm_group":
        return "eligible_for_future_promotion_gate"
    if action in {"reject_group", "request_more_source", "hold_group_for_privacy"}:
        return "blocked"
    return "preview_only_no_analysis_effect"


def _dedup_group_dedup_effect(action: str) -> str:
    return {
        "confirm_group": "review_only_group_confirmed",
        "split_group": "review_only_group_split",
        "change_representative": "review_only_representative_changed",
        "mark_group_weak": "not_run",
        "reject_group": "review_only_group_blocked",
        "request_more_source": "review_only_group_blocked",
        "hold_group_for_privacy": "review_only_group_blocked",
        "reset_group_review": "review_only_group_reset",
    }[action]


def _dedup_group_trust_effect(action: str) -> str:
    if action == "mark_group_weak":
        return "weak_warning"
    if action == "reject_group":
        return "rejected"
    return "no_upgrade"


def _validate_analysis_ready_promotion_payload(payload: AnalysisReadyPromotionGateRequest) -> None:
    if not (payload.reviewer_label or "").strip():
        raise AnalysisRequestValidationError("Cannot create analysis-ready promotion gate: reviewer_label is required.")
    if not (payload.promotion_decision or "").strip():
        raise AnalysisRequestValidationError("Cannot create analysis-ready promotion gate: promotion_decision is required.")
    acknowledgements = {
        "coverage_limitations_acknowledged": payload.coverage_limitations_acknowledged,
        "privacy_acknowledged": payload.privacy_acknowledged,
        "weak_evidence_warning_acknowledged": payload.weak_evidence_warning_acknowledged,
        "dedup_preview_warning_acknowledged": payload.dedup_preview_warning_acknowledged,
        "provider_output_is_evidence_not_truth_acknowledged": payload.provider_output_is_evidence_not_truth_acknowledged,
        "acknowledge_promotion_is_not_analysis": payload.acknowledge_promotion_is_not_analysis,
        "acknowledge_no_evidence_layer_write": payload.acknowledge_no_evidence_layer_write,
        "acknowledge_no_production_case": payload.acknowledge_no_production_case,
        "acknowledge_no_production_dedup": payload.acknowledge_no_production_dedup,
        "acknowledge_no_report": payload.acknowledge_no_report,
    }
    missing = [name for name, value in acknowledgements.items() if not value]
    if missing:
        raise AnalysisRequestValidationError(
            f"Cannot create analysis-ready promotion gate: acknowledgement flags are required ({', '.join(missing)})."
        )
    if payload.production_case_id or payload.target_production_case_id:
        raise AnalysisRequestValidationError("Cannot create analysis-ready promotion gate: production_case_id is not allowed.")
    if (payload.trust_label or "").lower() in {"high", "verified", "official", "official_api"}:
        raise AnalysisRequestValidationError("Cannot create analysis-ready promotion gate: trust upgrade is not allowed.")
    if (payload.verification_status or "").lower() in {"verified", "verified_by_official_api", "official_verified"}:
        raise AnalysisRequestValidationError("Cannot create analysis-ready promotion gate: official verification upgrade is not allowed.")
    side_effect_flags = {
        "evidence_layer_written": payload.evidence_layer_written,
        "production_case_created": payload.production_case_created,
        "production_review_queue_created": payload.production_review_queue_created,
        "production_dedup_run": payload.production_dedup_run,
        "analysis_included": payload.analysis_included,
        "analysis_run": payload.analysis_run,
        "report_generated": payload.report_generated,
        "sandbox_generated": payload.sandbox_generated,
        "public_event_generated": payload.public_event_generated,
        "write_evidence_layer_now": payload.write_evidence_layer_now,
        "create_production_case_now": payload.create_production_case_now,
        "create_production_review_queue_now": payload.create_production_review_queue_now,
        "run_production_dedup_now": payload.run_production_dedup_now,
        "run_dedup_now": payload.run_dedup_now,
        "run_analysis_now": payload.run_analysis_now,
        "generate_report_now": payload.generate_report_now,
        "generate_sandbox_now": payload.generate_sandbox_now,
        "generate_public_event_now": payload.generate_public_event_now,
    }
    enabled = [name for name, value in side_effect_flags.items() if value]
    if enabled:
        raise AnalysisRequestValidationError(
            f"Cannot create analysis-ready promotion gate: side effect flags must remain false ({', '.join(enabled)})."
        )


def _build_analysis_ready_promotion_gate(
    request_id: str,
    payload: AnalysisReadyPromotionGateRequest,
    preview: DedupPreview,
    completion_gate: ReviewQueueCompletionGate,
    queue_init: ReviewQueueInitialization,
    review_case: ReviewOnlyCase,
    batch: ReviewQueueItemBatch,
    staging_import: ReviewOnlyCaseStagingImport,
) -> AnalysisReadyPromotionGate:
    blockers: list[str] = []
    warnings: list[str] = []
    eligible_items: list[ReviewQueueItem] = []
    excluded_item_ids: list[str] = []
    weak_item_ids: list[str] = []
    rejected_item_ids: list[str] = []
    group_ids: list[str] = []

    if preview.request_id != request_id or completion_gate.request_id != request_id or queue_init.request_id != request_id:
        blockers.append("request_id_mismatch")
    if review_case.request_id != request_id or batch.request_id != request_id or staging_import.request_id != request_id:
        blockers.append("request_id_mismatch")
    if payload.review_case_id and payload.review_case_id != review_case.review_case_id:
        blockers.append("review_case_id_payload_mismatch")
    if payload.queue_init_id and payload.queue_init_id != queue_init.queue_init_id:
        blockers.append("queue_init_id_payload_mismatch")
    if payload.completion_gate_id and payload.completion_gate_id != completion_gate.completion_gate_id:
        blockers.append("completion_gate_id_payload_mismatch")
    if payload.dedup_preview_id and payload.dedup_preview_id != preview.dedup_preview_id:
        blockers.append("dedup_preview_id_payload_mismatch")
    if preview.review_case_id != review_case.review_case_id or completion_gate.review_case_id != review_case.review_case_id:
        blockers.append("review_case_mismatch")
    if preview.queue_init_id != queue_init.queue_init_id or completion_gate.queue_init_id != queue_init.queue_init_id:
        blockers.append("queue_init_mismatch")
    if batch.queue_init_id != queue_init.queue_init_id or batch.review_case_id != review_case.review_case_id:
        blockers.append("review_queue_batch_mismatch")
    if staging_import.review_case_id != review_case.review_case_id or staging_import.staging_import_id != queue_init.staging_import_id:
        blockers.append("staging_import_mismatch")
    if completion_gate.status != "complete_enough_for_future_dedup_preview":
        blockers.append("completion_gate_not_complete")
    if not completion_gate.downstream_eligibility.eligible_for_future_dedup_preview:
        blockers.append("completion_gate_not_eligible")
    if preview.status != "preview_ready" or preview.readiness.state != "dedup_preview_ready":
        blockers.append("dedup_preview_not_ready")
    if preview.privacy_scan.privacy_stop or preview.privacy_scan.raw_identifier_found or preview.privacy_scan.secret_like_found:
        blockers.append("dedup_preview_privacy_stop")
    if preview.now_flags.get("run_analysis_now") or preview.now_flags.get("write_evidence_layer_now"):
        blockers.append("dedup_preview_unsafe_now_flags")
    if review_case.production_case_created or review_case.evidence_layer_written or review_case.review_queue_created:
        blockers.append("review_only_case_unsafe_production_flags")
    if review_case.dedup_run or review_case.analysis_run or review_case.analysis_included:
        blockers.append("review_only_case_unsafe_analysis_flags")
    if queue_init.target.production_case_created or queue_init.target.evidence_layer_written or queue_init.target.production_review_queue_created:
        blockers.append("queue_init_unsafe_production_flags")
    if staging_import.target.production_case_created or staging_import.target.evidence_layer_written:
        blockers.append("staging_import_unsafe_production_flags")

    for item in batch.items:
        if item.request_id != request_id or item.queue_init_id != queue_init.queue_init_id or item.review_case_id != review_case.review_case_id:
            blockers.append("review_queue_item_parent_mismatch")
            excluded_item_ids.append(item.review_item_id)
            continue
        if item.governance.analysis_included or item.governance.public_visible or item.governance.report_visible or item.governance.sandbox_visible:
            blockers.append("item_visibility_or_analysis_flag_true")
            excluded_item_ids.append(item.review_item_id)
            continue
        if _review_queue_item_has_forbidden_fields(item):
            blockers.append("raw_forbidden_field_risk")
            excluded_item_ids.append(item.review_item_id)
            continue
        if item.dedup.may_amplify_risk:
            blockers.append("item_duplicate_may_amplify_risk")
            excluded_item_ids.append(item.review_item_id)
            continue
        if item.queue_status == "approved":
            eligible_items.append(item)
        elif item.queue_status == "marked_weak":
            eligible_items.append(item)
            weak_item_ids.append(item.review_item_id)
            warnings.append("Marked weak evidence remains warning-marked for any future manual analysis trigger.")
        elif item.queue_status == "duplicate_merged":
            eligible_items.append(item)
        elif item.queue_status == "rejected":
            rejected_item_ids.append(item.review_item_id)
            excluded_item_ids.append(item.review_item_id)
        elif item.queue_status == "privacy_hold":
            blockers.append("review_queue_privacy_hold")
            excluded_item_ids.append(item.review_item_id)
        else:
            blockers.append(f"unresolved_review_queue_status_{item.queue_status}")
            excluded_item_ids.append(item.review_item_id)

    group_warnings = _validate_promotion_dedup_groups(request_id, preview, batch, blockers)
    warnings.extend(group_warnings)
    for group in preview.groups:
        if group.group_status in {"confirmed", "marked_weak", "representative_changed"}:
            group_ids.append(group.group_candidate_id)

    decision = payload.promotion_decision.strip()
    status = _promotion_gate_status_for_decision(decision)
    if blockers:
        status = "privacy_hold" if any("privacy" in item or "forbidden" in item for item in blockers) else "blocked"
    effect = _promotion_gate_analysis_effect(status)
    eligible = status == "eligible_for_future_manual_analysis_trigger"
    promotion_gate_id = _new_analysis_ready_promotion_gate_id()
    decision_id = _new_promotion_decision_id()
    warning_notes = [
        "Promotion gate is not analysis.",
        "Future analysis requires a separate manual trigger.",
        "Coverage remains imported/available evidence only, not full-web or full-platform coverage.",
        "Provider output is evidence, not truth.",
    ]
    if weak_item_ids:
        warning_notes.append("Weak evidence remains warning-marked.")
    if rejected_item_ids:
        warning_notes.append("Rejected evidence is excluded from the promotion set preview.")

    return AnalysisReadyPromotionGate(
        promotion_gate_id=promotion_gate_id,
        request_id=request_id,
        review_case_id=review_case.review_case_id,
        queue_init_id=queue_init.queue_init_id,
        completion_gate_id=completion_gate.completion_gate_id,
        dedup_preview_id=preview.dedup_preview_id,
        created_at=datetime.now(timezone.utc),
        created_by=payload.created_by or "sentigraph_local_ui",
        status=status,
        input_scope=AnalysisReadyPromotionGateInputScope(
            include_statuses=["approved", "marked_weak", "duplicate_merged"],
            exclude_statuses=["rejected", "needs_more_source", "privacy_hold", "review_needed"],
            analysis_included=False,
            provider_output_is_truth=False,
            official_verification=False,
        ),
        counts=AnalysisReadyPromotionGateCounts(
            items_seen=len(batch.items),
            items_eligible_for_promotion_preview=len(eligible_items),
            items_excluded=len(set(excluded_item_ids)),
            approved_items=sum(1 for item in batch.items if item.queue_status == "approved"),
            weak_items=len(weak_item_ids),
            duplicate_merged_items=sum(1 for item in batch.items if item.queue_status == "duplicate_merged"),
            rejected_items=len(rejected_item_ids),
            confirmed_duplicate_groups=len(group_ids),
            warning_group_count=sum(1 for group in preview.groups if group.group_status in {"marked_weak", "representative_changed"}),
        ),
        promotion_set_preview=AnalysisReadyPromotionSetPreview(
            item_ids=[item.review_item_id for item in eligible_items],
            group_ids=group_ids,
            excluded_item_ids=sorted(set(excluded_item_ids)),
            weak_item_ids=weak_item_ids,
            rejected_item_ids=rejected_item_ids,
            warning_notes=_unique_preserve_order(warning_notes),
        ),
        promotion_decision=AnalysisReadyPromotionDecision(
            promotion_decision_id=decision_id,
            decision=decision,
            reviewer_label=payload.reviewer_label.strip(),
            decided_at=datetime.now(timezone.utc),
            note=payload.note.strip(),
            analysis_effect=effect,
        ),
        readiness=AnalysisReadyPromotionGateReadiness(
            state=status,
            eligible_for_future_manual_analysis_trigger=eligible,
            can_run_analysis_now=False,
            can_generate_report_now=False,
            requires_human_manual_analysis_trigger=True,
            requires_separate_analysis_runtime=True,
        ),
        blockers=_unique_preserve_order(blockers),
        warnings=_unique_preserve_order(warnings),
        boundary_notes=[
            "Analysis-ready promotion gate uses review-only governance records only.",
            "This gate does not re-read original package rows.",
            "This gate does not write the production Evidence Layer.",
            "This gate does not create production cases or production review queues.",
            "This gate does not run production dedup.",
            "This gate does not run analysis or generate reports.",
            "Duplicate evidence must not amplify risk, sentiment, coverage, or conclusions.",
            "Rejected evidence remains excluded by default.",
            "Provider output is evidence, not truth.",
        ],
        recommended_next_steps=_analysis_ready_promotion_next_steps(status),
    )


def _validate_promotion_dedup_groups(
    request_id: str,
    preview: DedupPreview,
    batch: ReviewQueueItemBatch,
    blockers: list[str],
) -> list[str]:
    warnings: list[str] = []
    item_ids = {item.review_item_id for item in batch.items}
    for group in preview.groups:
        if group.may_amplify_risk:
            blockers.append("dedup_group_may_amplify_risk")
        if group.dedup_preview_id != preview.dedup_preview_id or group.review_case_id != preview.review_case_id:
            blockers.append("dedup_group_parent_mismatch")
        if any(item_id not in item_ids for item_id in group.item_ids):
            blockers.append("dedup_group_item_missing_from_queue")
        if group.representative_item_id and group.representative_item_id not in group.item_ids:
            blockers.append("dedup_group_representative_missing")
        audits = read_dedup_group_review_audits_for_group(request_id, preview.dedup_preview_id, group.group_candidate_id)
        if group.group_status == "confirmed":
            if not any(audit.new_group_status == "confirmed" for audit in audits):
                blockers.append("dedup_group_confirmed_without_audit")
        elif group.group_status == "marked_weak":
            if not any(audit.new_group_status == "marked_weak" for audit in audits):
                blockers.append("dedup_group_marked_weak_without_audit")
            warnings.append("Dedup group marked weak remains warning-marked for future manual analysis trigger.")
        elif group.group_status == "representative_changed":
            if not any(audit.new_group_status == "representative_changed" for audit in audits):
                blockers.append("dedup_group_representative_changed_without_audit")
            warnings.append("Dedup group representative was changed by a human reviewer.")
        elif group.group_status == "rejected":
            if not any(audit.new_group_status == "rejected" for audit in audits):
                blockers.append("dedup_group_rejected_without_audit")
            warnings.append("Rejected duplicate group is excluded from promotion set preview.")
        elif group.group_status == "privacy_hold":
            blockers.append("dedup_group_privacy_hold")
        else:
            blockers.append(f"unresolved_dedup_group_status_{group.group_status}")
    return warnings


def _promotion_gate_status_for_decision(decision: str) -> str:
    normalized = decision.strip().lower()
    if normalized in {"approve_for_future_manual_analysis_trigger", "approve", "approve_promotion"}:
        return "eligible_for_future_manual_analysis_trigger"
    if normalized in {"hold_promotion", "hold_for_more_review", "request_more_review"}:
        return "held_by_human"
    if normalized in {"reject_promotion", "reject", "reject_for_analysis"}:
        return "rejected_by_human"
    raise AnalysisRequestValidationError(f"Cannot create analysis-ready promotion gate: unsupported promotion_decision {decision}.")


def _promotion_gate_analysis_effect(status: str) -> str:
    if status == "eligible_for_future_manual_analysis_trigger":
        return "eligible_for_manual_trigger_only"
    if status == "held_by_human":
        return "held"
    if status == "rejected_by_human":
        return "rejected"
    return "blocked"


def _analysis_ready_promotion_next_steps(status: str) -> list[str]:
    if status == "eligible_for_future_manual_analysis_trigger":
        return [
            "Design Phase 7C manual analysis trigger before running analysis.",
            "Keep analysis_included=false until a separate manual trigger executes.",
            "Do not generate reports, Sandbox fixtures, or public event pages from this gate alone.",
        ]
    if status == "held_by_human":
        return [
            "Resolve reviewer concerns before creating a new promotion gate decision.",
            "Keep all review-only items excluded from analysis.",
        ]
    if status == "rejected_by_human":
        return [
            "Do not trigger analysis for this review-only case.",
            "Keep the rejection audit visible for governance review.",
        ]
    if status == "privacy_hold":
        return [
            "Resolve privacy blockers before any future promotion gate.",
            "Do not run analysis or generate reports while privacy hold remains.",
        ]
    return [
        "Resolve blockers before promotion.",
        "Do not run analysis, dedup, report, Sandbox, or public event generation.",
    ]


def _validate_manual_analysis_trigger_payload(payload: ManualAnalysisTriggerRequest) -> None:
    if not (payload.promotion_gate_id or "").strip():
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: promotion_gate_id is required.")
    if payload.trigger_decision not in {"trigger_analysis", "hold", "cancel"}:
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: trigger_decision is required.")
    if not (payload.reviewer_label or "").strip():
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: reviewer_label is required.")
    if not (payload.note or "").strip():
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: note is required.")
    if payload.analysis_scope_mode != "promotion_set_preview":
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: analysis_scope_mode must be promotion_set_preview.")
    acknowledgements = {
        "coverage_acknowledged": payload.coverage_acknowledged,
        "privacy_acknowledged": payload.privacy_acknowledged,
        "weak_warning_acknowledged": payload.weak_warning_acknowledged,
        "dedup_warning_acknowledged": payload.dedup_warning_acknowledged,
        "provider_output_is_evidence_not_truth_acknowledged": payload.provider_output_is_evidence_not_truth_acknowledged,
        "not_official_verification_acknowledged": payload.not_official_verification_acknowledged,
        "not_full_web_coverage_acknowledged": payload.not_full_web_coverage_acknowledged,
        "acknowledge_trigger_record_only": payload.acknowledge_trigger_record_only,
        "acknowledge_no_analysis_run": payload.acknowledge_no_analysis_run,
        "acknowledge_no_evidence_layer_write": payload.acknowledge_no_evidence_layer_write,
        "acknowledge_no_production_case": payload.acknowledge_no_production_case,
        "acknowledge_no_report": payload.acknowledge_no_report,
        "acknowledge_no_sandbox_or_public_event": payload.acknowledge_no_sandbox_or_public_event,
    }
    missing = [name for name, value in acknowledgements.items() if not value]
    if missing:
        raise AnalysisRequestValidationError(
            f"Cannot create manual analysis trigger: acknowledgement flags are required ({', '.join(missing)})."
        )
    if payload.production_case_id or payload.target_production_case_id:
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: production_case_id is not allowed.")
    if (payload.trust_label or "").lower() in {"high", "verified", "official", "official_api"}:
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: trust upgrade is not allowed.")
    if (payload.verification_status or "").lower() in {"verified", "verified_by_official_api", "official_verified"}:
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: official verification upgrade is not allowed.")
    side_effect_flags = {
        "evidence_layer_written": payload.evidence_layer_written,
        "production_case_created": payload.production_case_created,
        "production_review_queue_created": payload.production_review_queue_created,
        "production_dedup_run": payload.production_dedup_run,
        "analysis_included": payload.analysis_included,
        "analysis_run": payload.analysis_run,
        "analysis_result_generated": payload.analysis_result_generated,
        "report_generated": payload.report_generated,
        "sandbox_generated": payload.sandbox_generated,
        "public_event_generated": payload.public_event_generated,
        "write_evidence_layer_now": payload.write_evidence_layer_now,
        "create_production_case_now": payload.create_production_case_now,
        "create_production_review_queue_now": payload.create_production_review_queue_now,
        "run_production_dedup_now": payload.run_production_dedup_now,
        "run_dedup_now": payload.run_dedup_now,
        "run_analysis_now": payload.run_analysis_now,
        "generate_analysis_result_now": payload.generate_analysis_result_now,
        "generate_report_now": payload.generate_report_now,
        "generate_sandbox_now": payload.generate_sandbox_now,
        "generate_public_event_now": payload.generate_public_event_now,
    }
    enabled = [name for name, value in side_effect_flags.items() if value]
    if enabled:
        raise AnalysisRequestValidationError(
            f"Cannot create manual analysis trigger: side effect flags must remain false ({', '.join(enabled)})."
        )


def _validate_manual_analysis_trigger_gate(request_id: str, gate: AnalysisReadyPromotionGate) -> None:
    if gate.request_id != request_id:
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: promotion gate request_id mismatch.")
    if gate.status != "eligible_for_future_manual_analysis_trigger":
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: promotion gate is not eligible.")
    if not gate.readiness.eligible_for_future_manual_analysis_trigger:
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: promotion gate readiness is not eligible.")
    if gate.readiness.can_run_analysis_now or gate.readiness.can_generate_report_now:
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: promotion gate has unsafe readiness flags.")
    if gate.blockers:
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: promotion gate has blockers.")
    unsafe_now_flags = [
        name
        for name, value in gate.now_flags.items()
        if value and name in {"write_evidence_layer_now", "create_production_case_now", "run_production_dedup_now", "run_analysis_now", "generate_report_now", "generate_sandbox_now", "generate_public_event_now"}
    ]
    if unsafe_now_flags:
        raise AnalysisRequestValidationError(
            f"Cannot create manual analysis trigger: promotion gate side effect flags are unsafe ({', '.join(unsafe_now_flags)})."
        )
    unsafe_safe_mode = [
        name
        for name in (
            "original_package_rows_re_read",
            "evidence_rows_imported",
            "evidence_layer_written",
            "production_case_created",
            "production_review_queue_created",
            "production_dedup_run",
            "analysis_generated",
            "sandbox_fixture_generated",
            "public_event_page_generated",
            "report_generated",
            "provider_execution",
            "collector_jobs_run",
            "real_api_calls",
            "url_fetching",
            "scraping",
            "secrets_exposed",
            "raw_author_identifiers_exposed",
        )
        if gate.safe_mode.get(name)
    ]
    if unsafe_safe_mode:
        raise AnalysisRequestValidationError(
            f"Cannot create manual analysis trigger: promotion gate safe_mode is unsafe ({', '.join(unsafe_safe_mode)})."
        )
    if not gate.promotion_set_preview.item_ids and not gate.promotion_set_preview.group_ids:
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: promotion_set_preview is empty.")
    audits = list_promotion_decision_audits_for_gate(request_id, gate.promotion_gate_id)
    if not any(audit.analysis_effect == "eligible_for_manual_trigger_only" for audit in audits):
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: promotion decision audit is missing.")


def _validate_manual_analysis_trigger_scope(gate: AnalysisReadyPromotionGate, batch: ReviewQueueItemBatch) -> None:
    item_map = {item.review_item_id: item for item in batch.items}
    include_ids = set(gate.promotion_set_preview.item_ids)
    excluded_ids = set(gate.promotion_set_preview.excluded_item_ids)
    rejected_ids = set(gate.promotion_set_preview.rejected_item_ids)
    weak_ids = set(gate.promotion_set_preview.weak_item_ids)
    missing = [item_id for item_id in include_ids | excluded_ids | rejected_ids | weak_ids if item_id not in item_map]
    if missing:
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: promotion_set_preview references unknown review items.")
    if include_ids & rejected_ids:
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: rejected items cannot be included.")
    for item_id in include_ids:
        item = item_map[item_id]
        if _review_queue_item_has_forbidden_fields(item):
            raise AnalysisRequestValidationError("Cannot create manual analysis trigger: raw/private/secret-like review item is not allowed.")
        if item.queue_status in {"rejected", "privacy_hold", "needs_more_source", "review_needed"}:
            raise AnalysisRequestValidationError("Cannot create manual analysis trigger: unresolved or rejected review item cannot be included.")
        if item.dedup.may_amplify_risk:
            raise AnalysisRequestValidationError("Cannot create manual analysis trigger: duplicate evidence may amplify risk.")
        if item.queue_status == "marked_weak" and item_id not in weak_ids:
            raise AnalysisRequestValidationError("Cannot create manual analysis trigger: weak evidence warning was removed.")
        if item.governance.analysis_included or item.governance.public_visible or item.governance.report_visible or item.governance.sandbox_visible:
            raise AnalysisRequestValidationError("Cannot create manual analysis trigger: item already has unsafe analysis or visibility flags.")
    for item_id in rejected_ids:
        if item_id in include_ids:
            raise AnalysisRequestValidationError("Cannot create manual analysis trigger: rejected item leaked into include scope.")
    if any(item_map[item_id].queue_status == "privacy_hold" for item_id in excluded_ids if item_id in item_map):
        raise AnalysisRequestValidationError("Cannot create manual analysis trigger: privacy_hold item blocks manual trigger.")


def _manual_analysis_trigger_status(decision: str) -> str:
    if decision == "trigger_analysis":
        return "trigger_recorded_ready_for_future_analysis_runtime"
    if decision == "hold":
        return "held"
    if decision == "cancel":
        return "cancelled"
    return "blocked"


def _manual_analysis_weak_warnings(gate: AnalysisReadyPromotionGate) -> list[str]:
    warnings: list[str] = []
    if gate.promotion_set_preview.weak_item_ids:
        warnings.append("Weak evidence remains warning-marked in future analysis scope.")
    if any("weak" in warning.lower() for warning in gate.warnings + gate.promotion_set_preview.warning_notes):
        warnings.append("Promotion gate carried weak-evidence warnings that must be displayed downstream.")
    return _unique_preserve_order(warnings)


def _manual_analysis_trigger_next_steps(status: str) -> list[str]:
    if status == "trigger_recorded_ready_for_future_analysis_runtime":
        return [
            "Design or run a future explicit analysis execution phase; this record does not run analysis.",
            "Apply Analysis Result Boundary Gate before displaying any analysis result.",
            "Keep rejected evidence excluded and weak evidence warning-marked.",
            "Do not generate reports, Sandbox fixtures, or public event pages from this trigger record alone.",
        ]
    if status == "held":
        return [
            "Resolve reviewer concerns before recording a new manual trigger decision.",
            "Keep promoted candidates out of analysis until a future explicit trigger.",
        ]
    if status == "cancelled":
        return [
            "Do not run analysis for this cancelled trigger decision.",
            "Create a new audited trigger record only if human review later changes the decision.",
        ]
    if status == "privacy_hold":
        return [
            "Resolve privacy blockers before any future analysis trigger.",
            "Do not run analysis or generate outputs while privacy hold remains.",
        ]
    return [
        "Resolve blockers before any future analysis trigger.",
        "Do not run analysis, report, Sandbox, or public event generation.",
    ]


def _unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _review_queue_completion_next_steps(status: str) -> list[str]:
    if status == "complete_enough_for_future_dedup_preview":
        return [
            "Design Phase 6W future dedup preview gate.",
            "Keep all items analysis-excluded until a future dedup and promotion phase.",
        ]
    if status == "privacy_hold":
        return [
            "Resolve privacy hold items before future dedup preview.",
            "Do not promote or analyze any review-only item.",
        ]
    if status == "blocked":
        return [
            "Inspect blocked_reasons and remove unsafe local-only queue state.",
            "Do not run dedup, analysis, report, Sandbox, or public event generation.",
        ]
    return [
        "Complete human review actions or explicitly defer source follow-up items.",
        "Re-run completion gate only after required review action audits exist.",
    ]


def _read_real_package_preview_rows(
    row_file: Path,
    max_rows: int,
) -> tuple[list[RealPackageRowPreviewRow], list[EvidenceRowReaderSummaryItem], list[EvidenceRowReaderSummaryItem], RealPackageRowPreviewRows, RealPackageRowPreviewPrivacyScan]:
    accepted_rows: list[RealPackageRowPreviewRow] = []
    quarantine_summary: list[EvidenceRowReaderSummaryItem] = []
    rejection_summary: list[EvidenceRowReaderSummaryItem] = []
    rows = RealPackageRowPreviewRows()
    privacy_scan = RealPackageRowPreviewPrivacyScan()

    try:
        with row_file.open("r", encoding="utf-8-sig") as handle:
            for line_number, line in enumerate(handle, start=1):
                if rows.rows_seen >= max_rows:
                    break
                raw_line = line.strip()
                if not raw_line:
                    continue
                rows.rows_seen += 1
                try:
                    parsed = json.loads(raw_line)
                except json.JSONDecodeError:
                    rows.rejected += 1
                    rejection_summary.append(
                        EvidenceRowReaderSummaryItem(
                            row_index=line_number,
                            status="rejected",
                            reason_code="invalid_json",
                            message="Real package preview row is not valid JSON.",
                        )
                    )
                    continue
                if not isinstance(parsed, dict):
                    rows.rejected += 1
                    rejection_summary.append(
                        EvidenceRowReaderSummaryItem(
                            row_index=line_number,
                            status="rejected",
                            reason_code="non_object_json",
                            message="Real package preview row must be a JSON object.",
                        )
                    )
                    continue

                forbidden_fields = _real_package_preview_forbidden_fields(parsed)
                _update_real_package_preview_privacy_scan(privacy_scan, parsed, forbidden_fields)
                severe_fields = _real_package_preview_severe_fields(parsed, forbidden_fields)
                if severe_fields:
                    privacy_scan.privacy_stop_triggered = True
                    rows.privacy_stop_at_row = line_number
                    quarantine_summary.append(
                        EvidenceRowReaderSummaryItem(
                            row_index=line_number,
                            status="privacy_stop",
                            reason_code="privacy_stop",
                            message="Real package preview stopped because severe privacy fields were detected.",
                            forbidden_fields_detected=severe_fields,
                        )
                    )
                    break
                if forbidden_fields:
                    rows.quarantined += 1
                    quarantine_summary.append(
                        EvidenceRowReaderSummaryItem(
                            row_index=line_number,
                            status="quarantined",
                            reason_code="forbidden_fields_detected",
                            message="Real package preview row contains forbidden privacy fields and was excluded from preview.",
                            forbidden_fields_detected=forbidden_fields,
                        )
                    )
                    continue

                rows.accepted_for_preview += 1
                accepted_rows.append(_build_real_package_preview_row(line_number, parsed))
    except OSError as exc:
        raise AnalysisRequestValidationError(f"Cannot create real package row preview: evidence_items.jsonl cannot be read ({type(exc).__name__}).") from exc

    return accepted_rows, quarantine_summary, rejection_summary, rows, privacy_scan


def _real_package_preview_forbidden_fields(row: dict[str, Any]) -> list[str]:
    forbidden_fields = [field for field in sorted(REAL_PREVIEW_FORBIDDEN_FIELDS) if field in row]
    if _row_reader_has_secret_like_value(row):
        forbidden_fields.append("secret_like_value")
    if _row_has_email_like_value(row):
        forbidden_fields.append("email")
    if _row_has_phone_like_value(row):
        forbidden_fields.append("phone")
    return forbidden_fields


def _real_package_preview_severe_fields(row: dict[str, Any], forbidden_fields: list[str]) -> list[str]:
    severe = []
    for field in ("private_message", "secret_like_value", "email", "phone"):
        if field in forbidden_fields:
            severe.append(field)
    return severe


def _update_real_package_preview_privacy_scan(
    privacy_scan: RealPackageRowPreviewPrivacyScan,
    row: dict[str, Any],
    forbidden_fields: list[str],
) -> None:
    _update_row_reader_privacy_scan(privacy_scan, row, forbidden_fields)
    if "email" in forbidden_fields:
        privacy_scan.email_detected += 1
    if "phone" in forbidden_fields:
        privacy_scan.phone_detected += 1


def _build_real_package_preview_row(row_index: int, row: dict[str, Any]) -> RealPackageRowPreviewRow:
    body_text = _safe_text_preview(str(row.get("body_text") or row.get("comment_text") or ""))
    title = _safe_text_preview(str(row.get("title") or ""), limit=120)
    source_url = _safe_source_url(str(row.get("source_url") or row.get("url") or ""))
    counts: dict[str, int | float] = {}
    for field in REAL_PREVIEW_COUNT_FIELDS:
        value = row.get(field)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            counts[field] = value
    return RealPackageRowPreviewRow(
        row_index=row_index,
        status="accepted_for_preview",
        evidence_candidate=RealPackageRowPreviewCandidate(
            evidence_type=str(row.get("evidence_type") or ""),
            platform=str(row.get("platform") or ""),
            source_url=source_url,
            title_preview=title,
            body_text_preview=body_text,
            created_at=str(row.get("created_at") or ""),
            language=str(row.get("language") or ""),
            counts=counts,
        ),
        governance_defaults=EvidenceRowReaderGovernanceDefaults(),
        privacy_check=RealPackageRowPreviewPrivacyCheck(passed=True, forbidden_fields_detected=[]),
    )


def _safe_text_preview(value: str, *, limit: int = 160) -> str:
    collapsed = re.sub(r"\s+", " ", value).strip()
    collapsed = re.sub(r"@\w+", "@[redacted]", collapsed)
    collapsed = EMAIL_PATTERN.sub("[redacted-email]", collapsed)
    collapsed = PHONE_PATTERN.sub("[redacted-phone]", collapsed)
    return collapsed[:limit]


def _safe_source_url(value: str) -> str:
    lowered = value.lower()
    if not value or "profile" in lowered or "token" in lowered or "session" in lowered or "cookie" in lowered:
        return ""
    return value


def _row_has_email_like_value(row: dict[str, Any]) -> bool:
    return any(
        isinstance(row.get(field), str) and EMAIL_PATTERN.search(str(row.get(field)))
        for field in ("title", "body_text", "comment_text", "private_message")
    )


def _row_has_phone_like_value(row: dict[str, Any]) -> bool:
    return any(
        isinstance(row.get(field), str) and PHONE_PATTERN.search(str(row.get(field)))
        for field in ("title", "body_text", "comment_text", "private_message")
    )


def _read_safe_json_file(path: Path) -> dict[str, Any]:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AnalysisRequestValidationError(f"Cannot create real package row preview: {path.name} must be valid JSON.") from exc
    return parsed if isinstance(parsed, dict) else {}


def _extract_validation_error_count(payload: dict[str, Any]) -> int:
    if isinstance(payload.get("validation"), dict):
        return int(payload["validation"].get("errors") or payload["validation"].get("errors_count") or 0)
    return int(payload.get("errors") or payload.get("errors_count") or 0)


def _safe_file_sha256(path: Path) -> str | None:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 64), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _resolve_row_reader_fixture_path(payload: EvidenceRowReaderDryRunCreate) -> Path:
    fixture_file = ROW_READER_FIXTURES.get(payload.fixture_name)
    if not fixture_file:
        raise AnalysisRequestValidationError("Cannot create row reader dry-run: fixture must be an allowed synthetic fixture.")
    fixture_path = (ROW_READER_FIXTURE_ROOT / fixture_file).resolve()
    try:
        fixture_path.relative_to(ROW_READER_FIXTURE_ROOT.resolve())
    except ValueError as exc:
        raise AnalysisRequestValidationError("Cannot create row reader dry-run: fixture path must stay inside synthetic fixture directory.") from exc
    if not fixture_path.is_file():
        raise AnalysisRequestNotFoundError(f"Synthetic row reader fixture {payload.fixture_name} was not found.")
    return fixture_path


def _read_synthetic_fixture_rows(
    fixture_path: Path,
    max_rows: int,
) -> tuple[list[EvidenceRowReaderPreviewRow], list[EvidenceRowReaderSummaryItem], list[EvidenceRowReaderSummaryItem], EvidenceRowReaderCounts, EvidenceRowReaderPrivacyScan]:
    accepted_rows: list[EvidenceRowReaderPreviewRow] = []
    quarantine_summary: list[EvidenceRowReaderSummaryItem] = []
    rejection_summary: list[EvidenceRowReaderSummaryItem] = []
    counts = EvidenceRowReaderCounts()
    privacy_scan = EvidenceRowReaderPrivacyScan()

    try:
        with fixture_path.open("r", encoding="utf-8-sig") as handle:
            for line_number, line in enumerate(handle, start=1):
                if counts.rows_seen >= max_rows:
                    break
                raw_line = line.strip()
                if not raw_line:
                    continue
                counts.rows_seen += 1
                try:
                    parsed = json.loads(raw_line)
                except json.JSONDecodeError:
                    counts.rejected += 1
                    rejection_summary.append(
                        EvidenceRowReaderSummaryItem(
                            row_index=line_number,
                            status="rejected",
                            reason_code="invalid_json",
                            message="Synthetic fixture row is not valid JSON.",
                        )
                    )
                    continue
                if not isinstance(parsed, dict):
                    counts.rejected += 1
                    rejection_summary.append(
                        EvidenceRowReaderSummaryItem(
                            row_index=line_number,
                            status="rejected",
                            reason_code="non_object_json",
                            message="Synthetic fixture row must be a JSON object.",
                        )
                    )
                    continue

                forbidden_fields = _row_reader_forbidden_fields(parsed)
                _update_row_reader_privacy_scan(privacy_scan, parsed, forbidden_fields)
                if forbidden_fields:
                    counts.quarantined += 1
                    quarantine_summary.append(
                        EvidenceRowReaderSummaryItem(
                            row_index=line_number,
                            status="quarantined",
                            reason_code="forbidden_fields_detected",
                            message="Synthetic fixture row contains forbidden privacy fields and was excluded from preview.",
                            forbidden_fields_detected=forbidden_fields,
                        )
                    )
                    continue

                counts.accepted_for_preview += 1
                accepted_rows.append(_build_row_reader_preview_row(line_number, parsed))
    except OSError as exc:
        raise AnalysisRequestValidationError(f"Cannot create row reader dry-run: synthetic fixture cannot be read ({type(exc).__name__}).") from exc

    privacy_scan.privacy_stop_triggered = bool(
        privacy_scan.raw_author_id_detected
        or privacy_scan.raw_author_name_detected
        or privacy_scan.profile_url_detected
        or privacy_scan.private_message_detected
        or privacy_scan.secret_like_value_detected
    )
    return accepted_rows, quarantine_summary, rejection_summary, counts, privacy_scan


def _row_reader_forbidden_fields(row: dict[str, Any]) -> list[str]:
    forbidden_fields = [field for field in sorted(ROW_READER_FORBIDDEN_FIELDS) if field in row]
    if _row_reader_has_secret_like_value(row):
        forbidden_fields.append("secret_like_value")
    return forbidden_fields


def _update_row_reader_privacy_scan(
    privacy_scan: EvidenceRowReaderPrivacyScan,
    row: dict[str, Any],
    forbidden_fields: list[str],
) -> None:
    if "raw_author_id" in forbidden_fields:
        privacy_scan.raw_author_id_detected += 1
    if "raw_author_name" in forbidden_fields:
        privacy_scan.raw_author_name_detected += 1
    if "profile_url" in forbidden_fields:
        privacy_scan.profile_url_detected += 1
    if "private_message" in forbidden_fields:
        privacy_scan.private_message_detected += 1
    if "secret_like_value" in forbidden_fields or _row_reader_has_secret_like_value(row):
        privacy_scan.secret_like_value_detected += 1


def _row_reader_has_secret_like_value(row: dict[str, Any]) -> bool:
    for key, value in row.items():
        key_text = str(key).lower()
        value_text = str(value).lower() if isinstance(value, (str, int, float, bool)) else ""
        if any(pattern in key_text for pattern in ROW_READER_SECRET_PATTERNS):
            return True
        if any(pattern in value_text for pattern in ROW_READER_SECRET_PATTERNS):
            return True
    return False


def _build_row_reader_preview_row(row_index: int, row: dict[str, Any]) -> EvidenceRowReaderPreviewRow:
    safe_row = {field: row.get(field) for field in ROW_READER_ALLOWED_FIELDS}
    body_text = str(safe_row.get("body_text") or "")
    return EvidenceRowReaderPreviewRow(
        row_index=row_index,
        status="accepted_for_preview",
        evidence_candidate=EvidenceRowReaderCandidate(
            evidence_type=str(safe_row.get("evidence_type") or ""),
            platform=str(safe_row.get("platform") or ""),
            source_url=str(safe_row.get("source_url") or ""),
            title=str(safe_row.get("title") or ""),
            body_text_preview=body_text[:160],
            created_at=str(safe_row.get("created_at") or ""),
            language=str(safe_row.get("language") or ""),
        ),
        governance_defaults=EvidenceRowReaderGovernanceDefaults(),
        privacy_check=EvidenceRowReaderPrivacyCheck(passed=True, forbidden_fields_detected=[]),
    )


def _read_result_payload(request_id: str) -> dict[str, Any]:
    result_path = _result_path(request_id)
    try:
        parsed = json.loads(result_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _request_root() -> Path:
    raw_value = os.environ.get(ANALYSIS_REQUESTS_ENV_VAR, "").strip()
    if raw_value:
        return Path(raw_value).expanduser().resolve()
    return DEFAULT_ROOT


def _ensure_root() -> Path:
    root = _request_root()
    (root / "requests").mkdir(parents=True, exist_ok=True)
    (root / "results").mkdir(parents=True, exist_ok=True)
    (root / "case_drafts").mkdir(parents=True, exist_ok=True)
    (root / "import_plans").mkdir(parents=True, exist_ok=True)
    (root / "import_previews").mkdir(parents=True, exist_ok=True)
    (root / "review_decisions").mkdir(parents=True, exist_ok=True)
    (root / "import_jobs").mkdir(parents=True, exist_ok=True)
    (root / "execution_preflights").mkdir(parents=True, exist_ok=True)
    (root / "row_reader_dry_runs").mkdir(parents=True, exist_ok=True)
    (root / "real_package_row_previews").mkdir(parents=True, exist_ok=True)
    (root / "review_only_cases").mkdir(parents=True, exist_ok=True)
    (root / "staging_imports").mkdir(parents=True, exist_ok=True)
    (root / "staged_evidence_candidates").mkdir(parents=True, exist_ok=True)
    (root / "review_queue_initializations").mkdir(parents=True, exist_ok=True)
    (root / "review_queue_items").mkdir(parents=True, exist_ok=True)
    (root / "review_queue_action_audits").mkdir(parents=True, exist_ok=True)
    (root / "review_queue_completion_gates").mkdir(parents=True, exist_ok=True)
    (root / "dedup_previews").mkdir(parents=True, exist_ok=True)
    (root / "dedup_group_review_audits").mkdir(parents=True, exist_ok=True)
    (root / "analysis_ready_promotion_gates").mkdir(parents=True, exist_ok=True)
    (root / "promotion_decision_audits").mkdir(parents=True, exist_ok=True)
    (root / "manual_analysis_triggers").mkdir(parents=True, exist_ok=True)
    (root / "manual_analysis_trigger_audits").mkdir(parents=True, exist_ok=True)
    return root


def _request_path(request_id: str) -> Path:
    _validate_request_id(request_id)
    root = _ensure_root()
    return root / "requests" / f"{request_id}.json"


def _result_path(request_id: str) -> Path:
    _validate_request_id(request_id)
    root = _ensure_root()
    return root / "results" / f"{request_id}.json"


def _case_draft_path(request_id: str) -> Path:
    _validate_request_id(request_id)
    root = _ensure_root()
    return root / "case_drafts" / f"{request_id}.json"


def _import_plan_path(request_id: str) -> Path:
    _validate_request_id(request_id)
    root = _ensure_root()
    return root / "import_plans" / f"{request_id}.json"


def _import_preview_path(request_id: str) -> Path:
    _validate_request_id(request_id)
    root = _ensure_root()
    return root / "import_previews" / f"{request_id}.json"


def _review_decision_path(request_id: str, decision_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(decision_id)
    root = _ensure_root()
    return root / "review_decisions" / f"{request_id}_{decision_id}.json"


def _import_job_path(request_id: str, job_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(job_id)
    root = _ensure_root()
    return root / "import_jobs" / f"{request_id}_{job_id}.json"


def _execution_preflight_path(request_id: str, preflight_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(preflight_id)
    root = _ensure_root()
    return root / "execution_preflights" / f"{request_id}_{preflight_id}.json"


def _row_reader_dry_run_path(request_id: str, dry_run_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(dry_run_id)
    root = _ensure_root()
    return root / "row_reader_dry_runs" / f"{request_id}_{dry_run_id}.json"


def _real_package_row_preview_path(request_id: str, preview_run_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(preview_run_id)
    root = _ensure_root()
    return root / "real_package_row_previews" / f"{request_id}_{preview_run_id}.json"


def _review_only_case_path(request_id: str, review_case_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(review_case_id)
    root = _ensure_root()
    return root / "review_only_cases" / f"{request_id}_{review_case_id}.json"


def _staging_import_path(request_id: str, staging_import_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(staging_import_id)
    root = _ensure_root()
    return root / "staging_imports" / f"{request_id}_{staging_import_id}.json"


def _staged_candidate_batch_path(request_id: str, staging_import_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(staging_import_id)
    root = _ensure_root()
    return root / "staged_evidence_candidates" / f"{request_id}_{staging_import_id}.json"


def _review_queue_initialization_path(request_id: str, queue_init_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(queue_init_id)
    root = _ensure_root()
    return root / "review_queue_initializations" / f"{request_id}_{queue_init_id}.json"


def _review_queue_item_batch_path(request_id: str, queue_init_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(queue_init_id)
    root = _ensure_root()
    return root / "review_queue_items" / f"{request_id}_{queue_init_id}.json"


def _review_queue_action_audit_path(request_id: str, review_item_id: str, audit_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(review_item_id)
    _validate_request_id(audit_id)
    root = _ensure_root()
    return root / "review_queue_action_audits" / f"{request_id}_{review_item_id}_{audit_id}.json"


def _review_queue_completion_gate_path(request_id: str, completion_gate_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(completion_gate_id)
    root = _ensure_root()
    return root / "review_queue_completion_gates" / f"{request_id}_{completion_gate_id}.json"


def _dedup_preview_path(request_id: str, dedup_preview_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(dedup_preview_id)
    root = _ensure_root()
    return root / "dedup_previews" / f"{request_id}_{dedup_preview_id}.json"


def _dedup_group_review_audit_path(request_id: str, group_candidate_id: str, audit_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(group_candidate_id)
    _validate_request_id(audit_id)
    root = _ensure_root()
    return root / "dedup_group_review_audits" / f"{request_id}_{group_candidate_id}_{audit_id}.json"


def _analysis_ready_promotion_gate_path(request_id: str, promotion_gate_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(promotion_gate_id)
    root = _ensure_root()
    return root / "analysis_ready_promotion_gates" / f"{request_id}_{promotion_gate_id}.json"


def _promotion_decision_audit_path(request_id: str, promotion_gate_id: str, promotion_decision_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(promotion_gate_id)
    _validate_request_id(promotion_decision_id)
    root = _ensure_root()
    return root / "promotion_decision_audits" / f"{request_id}_{promotion_gate_id}_{promotion_decision_id}.json"


def _manual_analysis_trigger_path(request_id: str, manual_trigger_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(manual_trigger_id)
    root = _ensure_root()
    return root / "manual_analysis_triggers" / f"{request_id}_{manual_trigger_id}.json"


def _manual_analysis_trigger_audit_path(request_id: str, manual_trigger_id: str, manual_trigger_audit_id: str) -> Path:
    _validate_request_id(request_id)
    _validate_request_id(manual_trigger_id)
    _validate_request_id(manual_trigger_audit_id)
    root = _ensure_root()
    return root / "manual_analysis_trigger_audits" / f"{request_id}_{manual_trigger_id}_{manual_trigger_audit_id}.json"


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def _validate_request_id(request_id: str) -> None:
    if not REQUEST_ID_PATTERN.fullmatch(request_id) or request_id in {".", ".."}:
        raise AnalysisRequestValidationError("Invalid request_id.")


def _new_request_id(title: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = _slugify(title)[:40] or "analysis-request"
    return f"req_{timestamp}_{slug}_{uuid.uuid4().hex[:8]}"


def _new_review_decision_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"review_decision_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_import_job_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"manual_import_job_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_execution_preflight_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"manual_import_preflight_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_row_reader_dry_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"row_reader_dry_run_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_real_package_row_preview_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"real_package_row_preview_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_review_only_case_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"review_only_case_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_staging_import_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"review_only_staging_import_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_review_queue_init_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"review_queue_init_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_review_queue_action_audit_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"review_queue_action_audit_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_review_queue_completion_gate_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"review_queue_completion_gate_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_dedup_preview_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"dedup_preview_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_dedup_group_review_audit_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"dedup_group_review_audit_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_analysis_ready_promotion_gate_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"analysis_ready_promotion_gate_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_promotion_decision_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"promotion_decision_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_manual_analysis_trigger_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"manual_analysis_trigger_{timestamp}_{uuid.uuid4().hex[:8]}"


def _new_manual_analysis_trigger_audit_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"manual_analysis_trigger_audit_{timestamp}_{uuid.uuid4().hex[:8]}"


def _slugify(value: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return text or "public-opinion-event"


def _json_count(path: Path) -> int:
    if not path.exists() or not path.is_dir():
        return 0
    return sum(1 for item in path.glob("*.json") if item.is_file())


def _safe_root_label(root: Path) -> str:
    try:
        relative = root.resolve().relative_to(PROJECT_ROOT.resolve())
        return str(relative).replace("\\", "/")
    except ValueError:
        return "configured_external_analysis_requests_dir"
