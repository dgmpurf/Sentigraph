from __future__ import annotations

import json
import os
import re
import uuid
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
    ManualEvidenceImportJob,
    ManualEvidenceImportJobCreate,
    ManualEvidenceImportJobReadiness,
    ManualEvidenceImportPreflightChecks,
    ManualEvidenceImportTargetCase,
    ProviderJobResult,
)


ANALYSIS_REQUESTS_ENV_VAR = "SENTIGRAPH_ANALYSIS_REQUESTS_DIR"
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ROOT = PROJECT_ROOT / "runtime" / "analysis_requests"
REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")

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
