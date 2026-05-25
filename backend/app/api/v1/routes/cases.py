from fastapi import APIRouter, HTTPException

from app.schemas.alert import AlertEvent, AnalysisSnapshot, MonitoringStatus
from app.schemas.case import (
    AnalysisCaseCreateRequest,
    AnalysisCaseDetail,
    AnalysisCaseListItem,
    CaseCrawlStartRequest,
    MarkdownExportResponse,
)
from app.schemas.evidence import (
    EvidenceDeduplicationSummary,
    EvidenceImportCommitRequest,
    EvidenceImportCommitResult,
    EvidenceImportPreviewRequest,
    EvidenceImportPreviewResult,
    EvidenceIngestionBatch,
    EvidenceIngestionResult,
    EvidenceReviewDecisionRequest,
    EvidenceReviewDecisionResult,
    EvidenceReviewSummary,
    EvidenceTrustSummary,
)
from app.services.evidence_import import EvidenceImportError
from app.services.evidence_ingestion import EvidenceValidationError
from app.schemas.forecast import ForecastResult
from app.schemas.notification import NotificationOutboxItem
from app.schemas.scheduler import MonitoringScheduleConfig
from app.services.simulation.case_initializer import (
    CaseAnalysisRequiredError,
    build_case_simulation_initialization,
)
from app.services.simulation.schemas import CaseSimulationInitializationResult
from app.services.case_store import (
    attach_case_evidence,
    commit_case_evidence_import,
    create_case,
    export_case_markdown,
    get_case,
    get_case_evidence_dedup_summary,
    get_case_evidence_review_summary,
    get_case_evidence_trust_summary,
    list_case_evidence,
    list_case_alerts,
    list_case_snapshots,
    list_cases,
    preview_case_evidence_import,
    review_case_evidence_item,
    run_case,
    run_case_crawl,
    run_monitoring_check,
)
from app.services.monitoring.scheduler_service import (
    disable_case_monitoring,
    enable_case_monitoring,
    get_case_monitoring_config,
    update_case_monitoring_config,
)
from app.services.forecasting.forecast_service import get_case_forecast, run_case_forecast
from app.services.notifications.notification_service import list_case_notifications

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


@router.post("/{case_id}/crawl/start", response_model=AnalysisCaseDetail)
def start_case_crawl(case_id: str, payload: CaseCrawlStartRequest | None = None) -> AnalysisCaseDetail:
    case = run_case_crawl(case_id, payload)
    if not case:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return case


@router.get("/{case_id}/evidence", response_model=EvidenceIngestionResult)
def get_case_evidence(case_id: str) -> EvidenceIngestionResult:
    result = list_case_evidence(case_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return result


@router.get("/{case_id}/evidence/trust-summary", response_model=EvidenceTrustSummary)
def get_case_evidence_trust(case_id: str) -> EvidenceTrustSummary:
    result = get_case_evidence_trust_summary(case_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return result


@router.get("/{case_id}/evidence/dedup-summary", response_model=EvidenceDeduplicationSummary)
def get_case_evidence_dedup(case_id: str) -> EvidenceDeduplicationSummary:
    result = get_case_evidence_dedup_summary(case_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return result


@router.get("/{case_id}/evidence/review-queue", response_model=EvidenceReviewSummary)
def get_case_evidence_review_queue(case_id: str) -> EvidenceReviewSummary:
    result = get_case_evidence_review_summary(case_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return result


@router.get("/{case_id}/evidence/review-summary", response_model=EvidenceReviewSummary)
def get_case_evidence_review_summary_route(case_id: str) -> EvidenceReviewSummary:
    result = get_case_evidence_review_summary(case_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return result


@router.post("/{case_id}/evidence/attach", response_model=EvidenceIngestionResult)
def attach_evidence_to_case(case_id: str, payload: EvidenceIngestionBatch) -> EvidenceIngestionResult:
    try:
        result = attach_case_evidence(case_id, payload)
    except EvidenceValidationError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "evidence_attach_rejected",
                "message": str(exc),
                "real_api_calls": False,
                "real_llm_calls": False,
                "url_fetching": False,
            },
        ) from exc
    if not result:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return result


@router.post("/{case_id}/evidence/{evidence_id}/review", response_model=EvidenceReviewDecisionResult)
def review_evidence_for_case(
    case_id: str,
    evidence_id: str,
    payload: EvidenceReviewDecisionRequest,
) -> EvidenceReviewDecisionResult:
    result = review_case_evidence_item(case_id, evidence_id, payload)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis case or evidence item not found.")
    return result


@router.post("/{case_id}/evidence/import/preview", response_model=EvidenceImportPreviewResult)
def preview_evidence_import_for_case(case_id: str, payload: EvidenceImportPreviewRequest) -> EvidenceImportPreviewResult:
    try:
        result = preview_case_evidence_import(case_id, payload)
    except EvidenceImportError as exc:
        raise HTTPException(status_code=400, detail={"error": "evidence_import_rejected", "message": str(exc)}) from exc
    if not result:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return result


@router.post("/{case_id}/evidence/import/commit", response_model=EvidenceImportCommitResult)
def commit_evidence_import_for_case(case_id: str, payload: EvidenceImportCommitRequest) -> EvidenceImportCommitResult:
    try:
        result = commit_case_evidence_import(case_id, payload)
    except EvidenceImportError as exc:
        raise HTTPException(status_code=400, detail={"error": "evidence_import_rejected", "message": str(exc)}) from exc
    if not result:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return result


@router.get("/{case_id}/snapshots", response_model=list[AnalysisSnapshot])
def get_case_snapshots(case_id: str) -> list[AnalysisSnapshot]:
    snapshots = list_case_snapshots(case_id)
    if snapshots is None:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return snapshots


@router.get("/{case_id}/forecast", response_model=ForecastResult)
def get_forecast(case_id: str) -> ForecastResult:
    forecast = get_case_forecast(case_id)
    if not forecast:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return forecast


@router.post("/{case_id}/forecast/run", response_model=ForecastResult)
def run_forecast(case_id: str) -> ForecastResult:
    forecast = run_case_forecast(case_id)
    if not forecast:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return forecast


@router.get("/{case_id}/simulation/initialization-preview", response_model=CaseSimulationInitializationResult)
def preview_case_simulation_initialization(case_id: str) -> CaseSimulationInitializationResult:
    return _case_simulation_initialization(case_id)


@router.post("/{case_id}/simulation/initialize", response_model=CaseSimulationInitializationResult)
def initialize_case_simulation(case_id: str) -> CaseSimulationInitializationResult:
    return _case_simulation_initialization(case_id)


@router.post("/{case_id}/monitor/run", response_model=MonitoringStatus)
def run_case_monitoring(case_id: str) -> MonitoringStatus:
    status = run_monitoring_check(case_id)
    if not status:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return status


@router.get("/{case_id}/monitoring/config", response_model=MonitoringScheduleConfig)
def get_monitoring_config(case_id: str) -> MonitoringScheduleConfig:
    config = get_case_monitoring_config(case_id)
    if not config:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return config


@router.put("/{case_id}/monitoring/config", response_model=MonitoringScheduleConfig)
def update_monitoring_config(case_id: str, payload: MonitoringScheduleConfig) -> MonitoringScheduleConfig:
    config = update_case_monitoring_config(case_id, payload)
    if not config:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return config


@router.post("/{case_id}/monitoring/enable", response_model=MonitoringScheduleConfig)
def enable_monitoring(case_id: str) -> MonitoringScheduleConfig:
    config = enable_case_monitoring(case_id)
    if not config:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return config


@router.post("/{case_id}/monitoring/disable", response_model=MonitoringScheduleConfig)
def disable_monitoring(case_id: str) -> MonitoringScheduleConfig:
    config = disable_case_monitoring(case_id)
    if not config:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return config


@router.get("/{case_id}/alerts", response_model=list[AlertEvent])
def get_case_alerts(case_id: str) -> list[AlertEvent]:
    alerts = list_case_alerts(case_id)
    if alerts is None:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return alerts


@router.get("/{case_id}/notifications", response_model=list[NotificationOutboxItem])
def get_case_notifications(case_id: str) -> list[NotificationOutboxItem]:
    if not get_case(case_id):
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    return list_case_notifications(case_id)


@router.get("/{case_id}/report/markdown", response_model=MarkdownExportResponse)
def get_case_markdown_report(case_id: str) -> MarkdownExportResponse:
    report = export_case_markdown(case_id)
    if not report:
        raise HTTPException(status_code=404, detail="Markdown report is not available for this case.")
    return report


def _case_simulation_initialization(case_id: str) -> CaseSimulationInitializationResult:
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Analysis case not found.")
    snapshots = list_case_snapshots(case_id) or []
    alerts = list_case_alerts(case_id) or []
    forecast = get_case_forecast(case_id)
    try:
        return build_case_simulation_initialization(
            case,
            snapshots=snapshots,
            alerts=alerts,
            forecast=forecast,
        )
    except CaseAnalysisRequiredError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "case_analysis_required",
                "message": "Run case analysis before initializing Simulation Lab from this case.",
                "case_id": case_id,
                "aggregate_level_only": True,
                "real_api_calls": False,
                "real_llm_calls": False,
            },
        ) from exc
