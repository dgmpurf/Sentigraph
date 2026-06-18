from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.analysis_request import (
    AnalysisRequestCancelResult,
    AnalysisRequestConfig,
    AnalysisRequestCreate,
    AnalysisRequestRecord,
    CaseDraftHandoff,
    EvidenceImportPlan,
)
from app.services.analysis_request_store import (
    AnalysisRequestNotFoundError,
    AnalysisRequestValidationError,
    cancel_analysis_request,
    create_case_draft_handoff,
    create_evidence_import_plan,
    create_analysis_request,
    get_analysis_request_config,
    list_case_draft_handoffs,
    list_evidence_import_plans,
    list_analysis_requests,
    read_case_draft_handoff,
    read_evidence_import_plan,
    read_analysis_request,
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
