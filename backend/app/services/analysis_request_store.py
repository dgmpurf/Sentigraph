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
    CaseDraftHandoff,
    CaseDraftPackageReference,
    CaseDraftProviderSummary,
    CaseDraftReadiness,
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
    ManualEvidenceImportPackageFileChecks,
    ManualEvidenceImportPreflightChecks,
    ManualEvidenceImportTargetCase,
    ManualEvidenceImportTargetCasePreflight,
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
