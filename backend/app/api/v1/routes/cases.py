from fastapi import APIRouter, HTTPException

from app.schemas.alert import AlertEvent, AnalysisSnapshot, MonitoringStatus
from app.schemas.case import (
    AnalysisCaseCreateRequest,
    AnalysisCaseDetail,
    AnalysisCaseListItem,
    MarkdownExportResponse,
)
from app.services.case_store import (
    create_case,
    export_case_markdown,
    get_case,
    list_case_alerts,
    list_case_snapshots,
    list_cases,
    run_case,
    run_monitoring_check,
)

router = APIRouter()


@router.get("", response_model=list[AnalysisCaseListItem])
def get_cases() -> list[AnalysisCaseListItem]:
    return list_cases()


@router.post("", response_model=AnalysisCaseDetail)
def create_analysis_case(payload: AnalysisCaseCreateRequest) -> AnalysisCaseDetail:
    return create_case(payload)


@router.get("/{case_id}", response_model=AnalysisCaseDetail)
def get_analysis_case(case_id: str) -> AnalysisCaseDetail:
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return case


@router.post("/{case_id}/run", response_model=AnalysisCaseDetail)
def run_analysis_case(case_id: str) -> AnalysisCaseDetail:
    case = run_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return case


@router.get("/{case_id}/snapshots", response_model=list[AnalysisSnapshot])
def get_case_snapshots(case_id: str) -> list[AnalysisSnapshot]:
    snapshots = list_case_snapshots(case_id)
    if snapshots is None:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return snapshots


@router.post("/{case_id}/monitor/run", response_model=MonitoringStatus)
def run_case_monitoring(case_id: str) -> MonitoringStatus:
    status = run_monitoring_check(case_id)
    if not status:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return status


@router.get("/{case_id}/alerts", response_model=list[AlertEvent])
def get_case_alerts(case_id: str) -> list[AlertEvent]:
    alerts = list_case_alerts(case_id)
    if alerts is None:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return alerts


@router.get("/{case_id}/report/markdown", response_model=MarkdownExportResponse)
def get_case_markdown_report(case_id: str) -> MarkdownExportResponse:
    report = export_case_markdown(case_id)
    if not report:
        raise HTTPException(status_code=404, detail="Markdown report is not available for this case.")
    return report
