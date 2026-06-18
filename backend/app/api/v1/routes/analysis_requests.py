from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.analysis_request import (
    AnalysisRequestCancelResult,
    AnalysisRequestConfig,
    AnalysisRequestCreate,
    AnalysisRequestRecord,
    CaseDraftHandoff,
    EvidenceImportPlan,
    EvidenceImportPreview,
    EvidenceImportReviewDecision,
    EvidenceImportReviewDecisionCreate,
    EvidenceRowReaderDryRun,
    EvidenceRowReaderDryRunCreate,
    ManualEvidenceImportExecutionPreflight,
    ManualEvidenceImportExecutionPreflightCreate,
    ManualEvidenceImportJob,
    ManualEvidenceImportJobCreate,
)
from app.services.analysis_request_store import (
    AnalysisRequestNotFoundError,
    AnalysisRequestValidationError,
    cancel_analysis_request,
    create_case_draft_handoff,
    create_evidence_import_plan,
    create_evidence_import_preview,
    create_evidence_import_review_decision,
    create_evidence_row_reader_dry_run,
    create_manual_evidence_import_execution_preflight,
    create_analysis_request,
    create_manual_evidence_import_job,
    get_analysis_request_config,
    list_case_draft_handoffs,
    list_all_evidence_row_reader_dry_runs,
    list_all_manual_evidence_import_execution_preflights,
    list_all_manual_evidence_import_jobs,
    list_all_evidence_import_review_decisions,
    list_evidence_import_plans,
    list_evidence_import_previews,
    list_evidence_import_review_decisions,
    list_evidence_row_reader_dry_runs,
    list_analysis_requests,
    list_manual_evidence_import_execution_preflights,
    list_manual_evidence_import_jobs,
    read_case_draft_handoff,
    read_evidence_import_plan,
    read_evidence_import_preview,
    read_evidence_import_review_decision,
    read_evidence_row_reader_dry_run,
    read_analysis_request,
    read_manual_evidence_import_execution_preflight,
    read_manual_evidence_import_job,
)

router = APIRouter()


@router.get("/config", response_model=AnalysisRequestConfig)
def analysis_request_config() -> AnalysisRequestConfig:
    return get_analysis_request_config()


@router.post("", response_model=AnalysisRequestRecord)
def analysis_request_create(payload: AnalysisRequestCreate) -> AnalysisRequestRecord:
    return create_analysis_request(payload)


@router.get("", response_model=list[AnalysisRequestRecord])
def analysis_request_list() -> list[AnalysisRequestRecord]:
    return list_analysis_requests()


@router.get("/case-drafts", response_model=list[CaseDraftHandoff])
def analysis_request_case_draft_list() -> list[CaseDraftHandoff]:
    return list_case_draft_handoffs()


@router.get("/import-plans", response_model=list[EvidenceImportPlan])
def analysis_request_import_plan_list() -> list[EvidenceImportPlan]:
    return list_evidence_import_plans()


@router.get("/import-previews", response_model=list[EvidenceImportPreview])
def analysis_request_import_preview_list() -> list[EvidenceImportPreview]:
    return list_evidence_import_previews()


@router.get("/review-decisions", response_model=list[EvidenceImportReviewDecision])
def analysis_request_review_decision_all_list() -> list[EvidenceImportReviewDecision]:
    return list_all_evidence_import_review_decisions()


@router.get("/import-jobs", response_model=list[ManualEvidenceImportJob])
def analysis_request_import_job_all_list() -> list[ManualEvidenceImportJob]:
    return list_all_manual_evidence_import_jobs()


@router.get("/execution-preflights", response_model=list[ManualEvidenceImportExecutionPreflight])
def analysis_request_execution_preflight_all_list() -> list[ManualEvidenceImportExecutionPreflight]:
    return list_all_manual_evidence_import_execution_preflights()


@router.get("/row-reader-dry-runs", response_model=list[EvidenceRowReaderDryRun])
def analysis_request_row_reader_dry_run_all_list() -> list[EvidenceRowReaderDryRun]:
    return list_all_evidence_row_reader_dry_runs()


@router.get("/{request_id}/case-draft", response_model=CaseDraftHandoff)
def analysis_request_case_draft_detail(request_id: str) -> CaseDraftHandoff:
    try:
        return read_case_draft_handoff(request_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/case-draft", response_model=CaseDraftHandoff)
def analysis_request_case_draft_create(request_id: str) -> CaseDraftHandoff:
    try:
        return create_case_draft_handoff(request_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/import-plan", response_model=EvidenceImportPlan)
def analysis_request_import_plan_detail(request_id: str) -> EvidenceImportPlan:
    try:
        return read_evidence_import_plan(request_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/import-plan", response_model=EvidenceImportPlan)
def analysis_request_import_plan_create(request_id: str) -> EvidenceImportPlan:
    try:
        return create_evidence_import_plan(request_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/import-preview", response_model=EvidenceImportPreview)
def analysis_request_import_preview_detail(request_id: str) -> EvidenceImportPreview:
    try:
        return read_evidence_import_preview(request_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/import-preview", response_model=EvidenceImportPreview)
def analysis_request_import_preview_create(request_id: str) -> EvidenceImportPreview:
    try:
        return create_evidence_import_preview(request_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/review-decisions", response_model=list[EvidenceImportReviewDecision])
def analysis_request_review_decision_list(request_id: str) -> list[EvidenceImportReviewDecision]:
    try:
        return list_evidence_import_review_decisions(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/review-decisions", response_model=EvidenceImportReviewDecision)
def analysis_request_review_decision_create(
    request_id: str,
    payload: EvidenceImportReviewDecisionCreate,
) -> EvidenceImportReviewDecision:
    try:
        return create_evidence_import_review_decision(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/review-decisions/{decision_id}", response_model=EvidenceImportReviewDecision)
def analysis_request_review_decision_detail(request_id: str, decision_id: str) -> EvidenceImportReviewDecision:
    try:
        return read_evidence_import_review_decision(request_id, decision_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/import-jobs", response_model=list[ManualEvidenceImportJob])
def analysis_request_import_job_list(request_id: str) -> list[ManualEvidenceImportJob]:
    try:
        return list_manual_evidence_import_jobs(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/import-jobs", response_model=ManualEvidenceImportJob)
def analysis_request_import_job_create(
    request_id: str,
    payload: ManualEvidenceImportJobCreate | None = None,
) -> ManualEvidenceImportJob:
    try:
        return create_manual_evidence_import_job(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/import-jobs/{job_id}", response_model=ManualEvidenceImportJob)
def analysis_request_import_job_detail(request_id: str, job_id: str) -> ManualEvidenceImportJob:
    try:
        return read_manual_evidence_import_job(request_id, job_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/execution-preflights", response_model=list[ManualEvidenceImportExecutionPreflight])
def analysis_request_execution_preflight_list(request_id: str) -> list[ManualEvidenceImportExecutionPreflight]:
    try:
        return list_manual_evidence_import_execution_preflights(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/execution-preflights", response_model=ManualEvidenceImportExecutionPreflight)
def analysis_request_execution_preflight_create(
    request_id: str,
    payload: ManualEvidenceImportExecutionPreflightCreate | None = None,
) -> ManualEvidenceImportExecutionPreflight:
    try:
        return create_manual_evidence_import_execution_preflight(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/execution-preflights/{preflight_id}", response_model=ManualEvidenceImportExecutionPreflight)
def analysis_request_execution_preflight_detail(
    request_id: str,
    preflight_id: str,
) -> ManualEvidenceImportExecutionPreflight:
    try:
        return read_manual_evidence_import_execution_preflight(request_id, preflight_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/row-reader-dry-runs", response_model=list[EvidenceRowReaderDryRun])
def analysis_request_row_reader_dry_run_list(request_id: str) -> list[EvidenceRowReaderDryRun]:
    try:
        return list_evidence_row_reader_dry_runs(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/row-reader-dry-runs", response_model=EvidenceRowReaderDryRun)
def analysis_request_row_reader_dry_run_create(
    request_id: str,
    payload: EvidenceRowReaderDryRunCreate | None = None,
) -> EvidenceRowReaderDryRun:
    try:
        return create_evidence_row_reader_dry_run(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/row-reader-dry-runs/{dry_run_id}", response_model=EvidenceRowReaderDryRun)
def analysis_request_row_reader_dry_run_detail(
    request_id: str,
    dry_run_id: str,
) -> EvidenceRowReaderDryRun:
    try:
        return read_evidence_row_reader_dry_run(request_id, dry_run_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}", response_model=AnalysisRequestRecord)
def analysis_request_detail(request_id: str) -> AnalysisRequestRecord:
    try:
        return read_analysis_request(request_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/cancel", response_model=AnalysisRequestCancelResult)
def analysis_request_cancel(request_id: str) -> AnalysisRequestCancelResult:
    try:
        return cancel_analysis_request(request_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
