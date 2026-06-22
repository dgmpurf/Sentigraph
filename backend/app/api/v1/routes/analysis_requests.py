from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.analysis_request import (
    AnalysisRequestCancelResult,
    AnalysisRequestConfig,
    AnalysisRequestCreate,
    AnalysisRequestRecord,
    AnalysisReadyPromotionGate,
    AnalysisReadyPromotionGateRequest,
    AnalysisResultBoundaryGate,
    AnalysisResultBoundaryGateAudit,
    AnalysisResultBoundaryGateRequest,
    CaseDraftHandoff,
    DedupPreview,
    DedupGroupReviewActionRequest,
    DedupGroupReviewActionResult,
    DedupGroupReviewAudit,
    DedupPreviewRequest,
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
    ManualAnalysisExecution,
    ManualAnalysisExecutionAudit,
    ManualAnalysisExecutionRequest,
    ManualAnalysisResultCandidate,
    ReportGenerationGate,
    ReportGenerationGateAudit,
    ReportGenerationGateRequest,
    FinalSummaryReport,
    FinalSummaryReportAudit,
    FinalSummaryReportExportArtifact,
    FinalSummaryReportExportArtifactAudit,
    FinalSummaryReportExportArtifactRequest,
    FinalSummaryReportExportGate,
    FinalSummaryReportExportGateAudit,
    FinalSummaryReportExportGateRequest,
    FinalSummaryReportRequest,
    FinalSummaryReportReviewGate,
    FinalSummaryReportReviewGateAudit,
    FinalSummaryReportReviewGateRequest,
    SummaryReportCandidate,
    SummaryReportCandidateAudit,
    SummaryReportCandidateRequest,
    ManualAnalysisTrigger,
    ManualAnalysisTriggerAudit,
    ManualAnalysisTriggerRequest,
    PromotionDecisionAudit,
    RealPackageRowPreview,
    RealPackageRowPreviewCreate,
    ReportExportDownloadPackageGate,
    ReportExportDownloadPackageGateAudit,
    ReportExportDownloadPackageGateRequest,
    ReportExportDownloadPackageArtifact,
    ReportExportDownloadPackageArtifactAudit,
    ReportExportDownloadPackageArtifactRequest,
    ReportExportPublicAccessExternalDeliveryGate,
    ReportExportPublicAccessExternalDeliveryGateAudit,
    ReportExportPublicAccessExternalDeliveryGateRequest,
    ReviewOnlyCase,
    ReviewOnlyCaseCreate,
    ReviewOnlyCaseStagingImport,
    ReviewOnlyCaseStagingImportCreate,
    ReviewQueueActionAudit,
    ReviewQueueActionRequest,
    ReviewQueueActionResult,
    ReviewQueueCompletionGate,
    ReviewQueueCompletionGateRequest,
    ReviewQueueInitialization,
    ReviewQueueInitializationCreate,
    ReviewQueueItemBatch,
    StagedEvidenceCandidateBatch,
)
from app.services.analysis_request_store import (
    AnalysisRequestNotFoundError,
    AnalysisRequestValidationError,
    cancel_analysis_request,
    create_analysis_ready_promotion_gate,
    create_analysis_result_boundary_gate,
    create_case_draft_handoff,
    create_dedup_group_review_action,
    create_dedup_preview,
    create_evidence_import_plan,
    create_evidence_import_preview,
    create_evidence_import_review_decision,
    create_evidence_row_reader_dry_run,
    create_manual_evidence_import_execution_preflight,
    create_manual_analysis_execution,
    create_final_summary_report,
    create_final_summary_report_export_artifact,
    create_final_summary_report_export_gate,
    create_report_export_download_package_gate,
    create_report_export_download_package_artifact,
    create_report_export_public_access_external_delivery_gate,
    create_report_generation_gate,
    create_final_summary_report_review_gate,
    create_summary_report_candidate,
    create_manual_analysis_trigger,
    create_analysis_request,
    create_manual_evidence_import_job,
    create_real_package_row_preview,
    create_review_only_case,
    create_review_only_case_staging_import,
    create_review_queue_completion_gate,
    create_review_queue_item_action,
    create_review_queue_initialization,
    get_analysis_request_config,
    list_all_analysis_ready_promotion_gates,
    list_all_analysis_result_boundary_gate_audits,
    list_all_analysis_result_boundary_gates,
    list_case_draft_handoffs,
    list_all_dedup_group_review_audits,
    list_all_dedup_previews,
    list_all_evidence_row_reader_dry_runs,
    list_all_manual_evidence_import_execution_preflights,
    list_all_manual_evidence_import_jobs,
    list_all_manual_analysis_execution_audits,
    list_all_manual_analysis_executions,
    list_all_manual_analysis_result_candidates,
    list_all_report_generation_gate_audits,
    list_all_report_generation_gates,
    list_all_final_summary_report_audits,
    list_all_final_summary_report_export_artifact_audits,
    list_all_final_summary_report_export_artifacts,
    list_all_final_summary_report_export_gate_audits,
    list_all_final_summary_report_export_gates,
    list_all_final_summary_reports,
    list_all_final_summary_report_review_gate_audits,
    list_all_final_summary_report_review_gates,
    list_all_summary_report_candidate_audits,
    list_all_summary_report_candidates,
    list_all_manual_analysis_trigger_audits,
    list_all_manual_analysis_triggers,
    list_all_promotion_decision_audits,
    list_all_evidence_import_review_decisions,
    list_all_real_package_row_previews,
    list_all_report_export_download_package_gate_audits,
    list_all_report_export_download_package_gates,
    list_all_report_export_download_package_artifact_audits,
    list_all_report_export_download_package_artifacts,
    list_all_report_export_public_access_external_delivery_gate_audits,
    list_all_report_export_public_access_external_delivery_gates,
    list_all_review_only_cases,
    list_all_review_only_case_staging_imports,
    list_all_review_queue_action_audits,
    list_all_review_queue_completion_gates,
    list_all_review_queue_initializations,
    list_evidence_import_plans,
    list_evidence_import_previews,
    list_evidence_import_review_decisions,
    list_evidence_row_reader_dry_runs,
    list_analysis_ready_promotion_gates,
    list_analysis_result_boundary_gate_audits,
    list_analysis_result_boundary_gate_audits_for_gate,
    list_analysis_result_boundary_gates,
    list_dedup_group_review_audits,
    list_dedup_previews,
    list_analysis_requests,
    list_manual_evidence_import_execution_preflights,
    list_manual_evidence_import_jobs,
    list_manual_analysis_execution_audits,
    list_manual_analysis_execution_audits_for_execution,
    list_manual_analysis_executions,
    list_manual_analysis_result_candidates,
    list_report_generation_gate_audits,
    list_report_generation_gate_audits_for_gate,
    list_report_generation_gates,
    list_final_summary_report_audits,
    list_final_summary_report_audits_for_report,
    list_final_summary_report_export_artifact_audits,
    list_final_summary_report_export_artifact_audits_for_artifact,
    list_final_summary_report_export_artifacts,
    list_final_summary_report_export_gate_audits,
    list_final_summary_report_export_gate_audits_for_gate,
    list_final_summary_report_export_gates,
    list_final_summary_reports,
    list_final_summary_report_review_gate_audits,
    list_final_summary_report_review_gate_audits_for_gate,
    list_final_summary_report_review_gates,
    list_summary_report_candidate_audits,
    list_summary_report_candidate_audits_for_candidate,
    list_summary_report_candidates,
    list_manual_analysis_trigger_audits,
    list_manual_analysis_trigger_audits_for_trigger,
    list_manual_analysis_triggers,
    list_promotion_decision_audits,
    list_promotion_decision_audits_for_gate,
    list_real_package_row_previews,
    list_report_export_download_package_gate_audits,
    list_report_export_download_package_gate_audits_for_gate,
    list_report_export_download_package_gates,
    list_report_export_download_package_artifact_audits,
    list_report_export_download_package_artifact_audits_for_artifact,
    list_report_export_download_package_artifacts,
    list_report_export_public_access_external_delivery_gate_audits,
    list_report_export_public_access_external_delivery_gate_audits_for_gate,
    list_report_export_public_access_external_delivery_gates,
    list_review_only_cases,
    list_review_only_case_staging_imports,
    list_review_queue_action_audits,
    list_review_queue_completion_gates,
    list_review_queue_initializations,
    read_case_draft_handoff,
    read_analysis_ready_promotion_gate,
    read_analysis_result_boundary_gate,
    read_dedup_group_review_audits_for_group,
    read_dedup_preview,
    read_evidence_import_plan,
    read_evidence_import_preview,
    read_evidence_import_review_decision,
    read_evidence_row_reader_dry_run,
    read_analysis_request,
    read_manual_evidence_import_execution_preflight,
    read_manual_evidence_import_job,
    read_manual_analysis_execution,
    read_manual_analysis_result_candidate,
    read_final_summary_report,
    read_final_summary_report_export_artifact,
    read_final_summary_report_export_gate,
    read_report_generation_gate,
    read_final_summary_report_review_gate,
    read_summary_report_candidate,
    read_manual_analysis_trigger,
    read_real_package_row_preview,
    read_report_export_download_package_gate,
    read_report_export_download_package_artifact,
    read_report_export_public_access_external_delivery_gate,
    read_review_only_case,
    read_review_only_case_staging_import,
    read_review_queue_action_audits_for_item,
    read_review_queue_completion_gate,
    read_review_queue_initialization,
    read_review_queue_item_batch,
    read_staged_evidence_candidate_batch,
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


@router.get("/real-package-row-previews", response_model=list[RealPackageRowPreview])
def analysis_request_real_package_row_preview_all_list() -> list[RealPackageRowPreview]:
    return list_all_real_package_row_previews()


@router.get("/review-only-cases", response_model=list[ReviewOnlyCase])
def analysis_request_review_only_case_all_list() -> list[ReviewOnlyCase]:
    return list_all_review_only_cases()


@router.get("/staging-imports", response_model=list[ReviewOnlyCaseStagingImport])
def analysis_request_staging_import_all_list() -> list[ReviewOnlyCaseStagingImport]:
    return list_all_review_only_case_staging_imports()


@router.get("/review-queue-initializations", response_model=list[ReviewQueueInitialization])
def analysis_request_review_queue_initialization_all_list() -> list[ReviewQueueInitialization]:
    return list_all_review_queue_initializations()


@router.get("/review-queue-action-audits", response_model=list[ReviewQueueActionAudit])
def analysis_request_review_queue_action_audit_all_list() -> list[ReviewQueueActionAudit]:
    return list_all_review_queue_action_audits()


@router.get("/review-queue-completion-gates", response_model=list[ReviewQueueCompletionGate])
def analysis_request_review_queue_completion_gate_all_list() -> list[ReviewQueueCompletionGate]:
    return list_all_review_queue_completion_gates()


@router.get("/dedup-previews", response_model=list[DedupPreview])
def analysis_request_dedup_preview_all_list() -> list[DedupPreview]:
    return list_all_dedup_previews()


@router.get("/dedup-group-review-audits", response_model=list[DedupGroupReviewAudit])
def analysis_request_dedup_group_review_audit_all_list() -> list[DedupGroupReviewAudit]:
    return list_all_dedup_group_review_audits()


@router.get("/analysis-ready-promotion-gates", response_model=list[AnalysisReadyPromotionGate])
def analysis_request_analysis_ready_promotion_gate_all_list() -> list[AnalysisReadyPromotionGate]:
    return list_all_analysis_ready_promotion_gates()


@router.get("/promotion-decision-audits", response_model=list[PromotionDecisionAudit])
def analysis_request_promotion_decision_audit_all_list() -> list[PromotionDecisionAudit]:
    return list_all_promotion_decision_audits()


@router.get("/manual-analysis-triggers", response_model=list[ManualAnalysisTrigger])
def analysis_request_manual_analysis_trigger_all_list() -> list[ManualAnalysisTrigger]:
    return list_all_manual_analysis_triggers()


@router.get("/manual-analysis-trigger-audits", response_model=list[ManualAnalysisTriggerAudit])
def analysis_request_manual_analysis_trigger_audit_all_list() -> list[ManualAnalysisTriggerAudit]:
    return list_all_manual_analysis_trigger_audits()


@router.get("/analysis-result-boundary-gates", response_model=list[AnalysisResultBoundaryGate])
def analysis_request_analysis_result_boundary_gate_all_list() -> list[AnalysisResultBoundaryGate]:
    return list_all_analysis_result_boundary_gates()


@router.get("/analysis-result-boundary-gate-audits", response_model=list[AnalysisResultBoundaryGateAudit])
def analysis_request_analysis_result_boundary_gate_audit_all_list() -> list[AnalysisResultBoundaryGateAudit]:
    return list_all_analysis_result_boundary_gate_audits()


@router.get("/manual-analysis-executions", response_model=list[ManualAnalysisExecution])
def analysis_request_manual_analysis_execution_all_list() -> list[ManualAnalysisExecution]:
    return list_all_manual_analysis_executions()


@router.get("/manual-analysis-result-candidates", response_model=list[ManualAnalysisResultCandidate])
def analysis_request_manual_analysis_result_candidate_all_list() -> list[ManualAnalysisResultCandidate]:
    return list_all_manual_analysis_result_candidates()


@router.get("/manual-analysis-execution-audits", response_model=list[ManualAnalysisExecutionAudit])
def analysis_request_manual_analysis_execution_audit_all_list() -> list[ManualAnalysisExecutionAudit]:
    return list_all_manual_analysis_execution_audits()


@router.get("/report-generation-gates", response_model=list[ReportGenerationGate])
def analysis_request_report_generation_gate_all_list() -> list[ReportGenerationGate]:
    return list_all_report_generation_gates()


@router.get("/report-generation-gate-audits", response_model=list[ReportGenerationGateAudit])
def analysis_request_report_generation_gate_audit_all_list() -> list[ReportGenerationGateAudit]:
    return list_all_report_generation_gate_audits()


@router.get("/summary-report-candidates", response_model=list[SummaryReportCandidate])
def analysis_request_summary_report_candidate_all_list() -> list[SummaryReportCandidate]:
    return list_all_summary_report_candidates()


@router.get("/summary-report-candidate-audits", response_model=list[SummaryReportCandidateAudit])
def analysis_request_summary_report_candidate_audit_all_list() -> list[SummaryReportCandidateAudit]:
    return list_all_summary_report_candidate_audits()


@router.get("/final-summary-report-review-gates", response_model=list[FinalSummaryReportReviewGate])
def analysis_request_final_summary_report_review_gate_all_list() -> list[FinalSummaryReportReviewGate]:
    return list_all_final_summary_report_review_gates()


@router.get("/final-summary-report-review-gate-audits", response_model=list[FinalSummaryReportReviewGateAudit])
def analysis_request_final_summary_report_review_gate_audit_all_list() -> list[FinalSummaryReportReviewGateAudit]:
    return list_all_final_summary_report_review_gate_audits()


@router.get("/final-summary-reports", response_model=list[FinalSummaryReport])
def analysis_request_final_summary_report_all_list() -> list[FinalSummaryReport]:
    return list_all_final_summary_reports()


@router.get("/final-summary-report-audits", response_model=list[FinalSummaryReportAudit])
def analysis_request_final_summary_report_audit_all_list() -> list[FinalSummaryReportAudit]:
    return list_all_final_summary_report_audits()


@router.get("/final-summary-report-export-gates", response_model=list[FinalSummaryReportExportGate])
def analysis_request_final_summary_report_export_gate_all_list() -> list[FinalSummaryReportExportGate]:
    return list_all_final_summary_report_export_gates()


@router.get("/final-summary-report-export-gate-audits", response_model=list[FinalSummaryReportExportGateAudit])
def analysis_request_final_summary_report_export_gate_audit_all_list() -> list[FinalSummaryReportExportGateAudit]:
    return list_all_final_summary_report_export_gate_audits()


@router.get("/final-summary-report-export-artifacts", response_model=list[FinalSummaryReportExportArtifact])
def analysis_request_final_summary_report_export_artifact_all_list() -> list[FinalSummaryReportExportArtifact]:
    return list_all_final_summary_report_export_artifacts()


@router.get("/final-summary-report-export-artifact-audits", response_model=list[FinalSummaryReportExportArtifactAudit])
def analysis_request_final_summary_report_export_artifact_audit_all_list() -> list[FinalSummaryReportExportArtifactAudit]:
    return list_all_final_summary_report_export_artifact_audits()


@router.get("/report-export-download-package-gates", response_model=list[ReportExportDownloadPackageGate])
def analysis_request_report_export_download_package_gate_all_list() -> list[ReportExportDownloadPackageGate]:
    return list_all_report_export_download_package_gates()


@router.get("/report-export-download-package-gate-audits", response_model=list[ReportExportDownloadPackageGateAudit])
def analysis_request_report_export_download_package_gate_audit_all_list() -> list[ReportExportDownloadPackageGateAudit]:
    return list_all_report_export_download_package_gate_audits()


@router.get("/report-export-download-package-artifacts", response_model=list[ReportExportDownloadPackageArtifact])
def analysis_request_report_export_download_package_artifact_all_list() -> list[ReportExportDownloadPackageArtifact]:
    return list_all_report_export_download_package_artifacts()


@router.get("/report-export-download-package-artifact-audits", response_model=list[ReportExportDownloadPackageArtifactAudit])
def analysis_request_report_export_download_package_artifact_audit_all_list() -> list[ReportExportDownloadPackageArtifactAudit]:
    return list_all_report_export_download_package_artifact_audits()


@router.get("/report-export-public-access-external-delivery-gates", response_model=list[ReportExportPublicAccessExternalDeliveryGate])
def analysis_request_report_export_public_access_external_delivery_gate_all_list() -> list[ReportExportPublicAccessExternalDeliveryGate]:
    return list_all_report_export_public_access_external_delivery_gates()


@router.get(
    "/report-export-public-access-external-delivery-gate-audits",
    response_model=list[ReportExportPublicAccessExternalDeliveryGateAudit],
)
def analysis_request_report_export_public_access_external_delivery_gate_audit_all_list() -> list[ReportExportPublicAccessExternalDeliveryGateAudit]:
    return list_all_report_export_public_access_external_delivery_gate_audits()


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


@router.get("/{request_id}/real-package-row-previews", response_model=list[RealPackageRowPreview])
def analysis_request_real_package_row_preview_list(request_id: str) -> list[RealPackageRowPreview]:
    try:
        return list_real_package_row_previews(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/real-package-row-previews", response_model=RealPackageRowPreview)
def analysis_request_real_package_row_preview_create(
    request_id: str,
    payload: RealPackageRowPreviewCreate | None = None,
) -> RealPackageRowPreview:
    try:
        return create_real_package_row_preview(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/real-package-row-previews/{preview_run_id}", response_model=RealPackageRowPreview)
def analysis_request_real_package_row_preview_detail(
    request_id: str,
    preview_run_id: str,
) -> RealPackageRowPreview:
    try:
        return read_real_package_row_preview(request_id, preview_run_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/review-only-cases", response_model=list[ReviewOnlyCase])
def analysis_request_review_only_case_list(request_id: str) -> list[ReviewOnlyCase]:
    try:
        return list_review_only_cases(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/review-only-cases", response_model=ReviewOnlyCase)
def analysis_request_review_only_case_create(
    request_id: str,
    payload: ReviewOnlyCaseCreate | None = None,
) -> ReviewOnlyCase:
    try:
        return create_review_only_case(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/review-only-cases/{review_case_id}", response_model=ReviewOnlyCase)
def analysis_request_review_only_case_detail(
    request_id: str,
    review_case_id: str,
) -> ReviewOnlyCase:
    try:
        return read_review_only_case(request_id, review_case_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/staging-imports", response_model=list[ReviewOnlyCaseStagingImport])
def analysis_request_staging_import_list(request_id: str) -> list[ReviewOnlyCaseStagingImport]:
    try:
        return list_review_only_case_staging_imports(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/staging-imports", response_model=ReviewOnlyCaseStagingImport)
def analysis_request_staging_import_create(
    request_id: str,
    payload: ReviewOnlyCaseStagingImportCreate | None = None,
) -> ReviewOnlyCaseStagingImport:
    try:
        return create_review_only_case_staging_import(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/staging-imports/{staging_import_id}", response_model=ReviewOnlyCaseStagingImport)
def analysis_request_staging_import_detail(
    request_id: str,
    staging_import_id: str,
) -> ReviewOnlyCaseStagingImport:
    try:
        return read_review_only_case_staging_import(request_id, staging_import_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/staging-imports/{staging_import_id}/candidates",
    response_model=StagedEvidenceCandidateBatch,
)
def analysis_request_staging_import_candidates(
    request_id: str,
    staging_import_id: str,
) -> StagedEvidenceCandidateBatch:
    try:
        return read_staged_evidence_candidate_batch(request_id, staging_import_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/review-queue-initializations", response_model=list[ReviewQueueInitialization])
def analysis_request_review_queue_initialization_list(request_id: str) -> list[ReviewQueueInitialization]:
    try:
        return list_review_queue_initializations(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/review-queue-initializations", response_model=ReviewQueueInitialization)
def analysis_request_review_queue_initialization_create(
    request_id: str,
    payload: ReviewQueueInitializationCreate | None = None,
) -> ReviewQueueInitialization:
    try:
        return create_review_queue_initialization(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/review-queue-initializations/{queue_init_id}", response_model=ReviewQueueInitialization)
def analysis_request_review_queue_initialization_detail(
    request_id: str,
    queue_init_id: str,
) -> ReviewQueueInitialization:
    try:
        return read_review_queue_initialization(request_id, queue_init_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/review-queue-initializations/{queue_init_id}/items",
    response_model=ReviewQueueItemBatch,
)
def analysis_request_review_queue_initialization_items(
    request_id: str,
    queue_init_id: str,
) -> ReviewQueueItemBatch:
    try:
        return read_review_queue_item_batch(request_id, queue_init_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/review-queue-action-audits", response_model=list[ReviewQueueActionAudit])
def analysis_request_review_queue_action_audit_list(request_id: str) -> list[ReviewQueueActionAudit]:
    try:
        return list_review_queue_action_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/review-queue-items/{review_item_id}/actions", response_model=ReviewQueueActionResult)
def analysis_request_review_queue_item_action_create(
    request_id: str,
    review_item_id: str,
    payload: ReviewQueueActionRequest,
) -> ReviewQueueActionResult:
    try:
        return create_review_queue_item_action(request_id, review_item_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/review-queue-items/{review_item_id}/audits", response_model=list[ReviewQueueActionAudit])
def analysis_request_review_queue_item_action_audit_list(
    request_id: str,
    review_item_id: str,
) -> list[ReviewQueueActionAudit]:
    try:
        return read_review_queue_action_audits_for_item(request_id, review_item_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/review-queue-completion-gates", response_model=list[ReviewQueueCompletionGate])
def analysis_request_review_queue_completion_gate_list(request_id: str) -> list[ReviewQueueCompletionGate]:
    try:
        return list_review_queue_completion_gates(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/review-queue-completion-gates", response_model=ReviewQueueCompletionGate)
def analysis_request_review_queue_completion_gate_create(
    request_id: str,
    payload: ReviewQueueCompletionGateRequest,
) -> ReviewQueueCompletionGate:
    try:
        return create_review_queue_completion_gate(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/review-queue-completion-gates/{completion_gate_id}", response_model=ReviewQueueCompletionGate)
def analysis_request_review_queue_completion_gate_detail(
    request_id: str,
    completion_gate_id: str,
) -> ReviewQueueCompletionGate:
    try:
        return read_review_queue_completion_gate(request_id, completion_gate_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/dedup-previews", response_model=list[DedupPreview])
def analysis_request_dedup_preview_list(request_id: str) -> list[DedupPreview]:
    try:
        return list_dedup_previews(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/dedup-previews", response_model=DedupPreview)
def analysis_request_dedup_preview_create(
    request_id: str,
    payload: DedupPreviewRequest,
) -> DedupPreview:
    try:
        return create_dedup_preview(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/dedup-previews/{dedup_preview_id}", response_model=DedupPreview)
def analysis_request_dedup_preview_detail(
    request_id: str,
    dedup_preview_id: str,
) -> DedupPreview:
    try:
        return read_dedup_preview(request_id, dedup_preview_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post(
    "/{request_id}/dedup-previews/{dedup_preview_id}/groups/{group_candidate_id}/actions",
    response_model=DedupGroupReviewActionResult,
)
def analysis_request_dedup_group_review_action_create(
    request_id: str,
    dedup_preview_id: str,
    group_candidate_id: str,
    payload: DedupGroupReviewActionRequest,
) -> DedupGroupReviewActionResult:
    try:
        return create_dedup_group_review_action(request_id, dedup_preview_id, group_candidate_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/dedup-previews/{dedup_preview_id}/groups/{group_candidate_id}/audits",
    response_model=list[DedupGroupReviewAudit],
)
def analysis_request_dedup_group_review_audit_group_list(
    request_id: str,
    dedup_preview_id: str,
    group_candidate_id: str,
) -> list[DedupGroupReviewAudit]:
    try:
        return read_dedup_group_review_audits_for_group(request_id, dedup_preview_id, group_candidate_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/dedup-group-review-audits", response_model=list[DedupGroupReviewAudit])
def analysis_request_dedup_group_review_audit_list(request_id: str) -> list[DedupGroupReviewAudit]:
    try:
        return list_dedup_group_review_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/analysis-ready-promotion-gates", response_model=list[AnalysisReadyPromotionGate])
def analysis_request_analysis_ready_promotion_gate_list(request_id: str) -> list[AnalysisReadyPromotionGate]:
    try:
        return list_analysis_ready_promotion_gates(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/analysis-ready-promotion-gates", response_model=AnalysisReadyPromotionGate)
def analysis_request_analysis_ready_promotion_gate_create(
    request_id: str,
    payload: AnalysisReadyPromotionGateRequest,
) -> AnalysisReadyPromotionGate:
    try:
        return create_analysis_ready_promotion_gate(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/analysis-ready-promotion-gates/{promotion_gate_id}", response_model=AnalysisReadyPromotionGate)
def analysis_request_analysis_ready_promotion_gate_detail(
    request_id: str,
    promotion_gate_id: str,
) -> AnalysisReadyPromotionGate:
    try:
        return read_analysis_ready_promotion_gate(request_id, promotion_gate_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/promotion-decision-audits", response_model=list[PromotionDecisionAudit])
def analysis_request_promotion_decision_audit_list(request_id: str) -> list[PromotionDecisionAudit]:
    try:
        return list_promotion_decision_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/analysis-ready-promotion-gates/{promotion_gate_id}/audits",
    response_model=list[PromotionDecisionAudit],
)
def analysis_request_analysis_ready_promotion_gate_audit_list(
    request_id: str,
    promotion_gate_id: str,
) -> list[PromotionDecisionAudit]:
    try:
        return list_promotion_decision_audits_for_gate(request_id, promotion_gate_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/manual-analysis-triggers", response_model=list[ManualAnalysisTrigger])
def analysis_request_manual_analysis_trigger_list(request_id: str) -> list[ManualAnalysisTrigger]:
    try:
        return list_manual_analysis_triggers(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/manual-analysis-triggers", response_model=ManualAnalysisTrigger)
def analysis_request_manual_analysis_trigger_create(
    request_id: str,
    payload: ManualAnalysisTriggerRequest,
) -> ManualAnalysisTrigger:
    try:
        return create_manual_analysis_trigger(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/manual-analysis-triggers/{manual_trigger_id}", response_model=ManualAnalysisTrigger)
def analysis_request_manual_analysis_trigger_detail(
    request_id: str,
    manual_trigger_id: str,
) -> ManualAnalysisTrigger:
    try:
        return read_manual_analysis_trigger(request_id, manual_trigger_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/manual-analysis-trigger-audits", response_model=list[ManualAnalysisTriggerAudit])
def analysis_request_manual_analysis_trigger_audit_list(request_id: str) -> list[ManualAnalysisTriggerAudit]:
    try:
        return list_manual_analysis_trigger_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/manual-analysis-triggers/{manual_trigger_id}/audits",
    response_model=list[ManualAnalysisTriggerAudit],
)
def analysis_request_manual_analysis_trigger_audit_for_trigger_list(
    request_id: str,
    manual_trigger_id: str,
) -> list[ManualAnalysisTriggerAudit]:
    try:
        return list_manual_analysis_trigger_audits_for_trigger(request_id, manual_trigger_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/analysis-result-boundary-gates", response_model=list[AnalysisResultBoundaryGate])
def analysis_request_analysis_result_boundary_gate_list(request_id: str) -> list[AnalysisResultBoundaryGate]:
    try:
        return list_analysis_result_boundary_gates(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/analysis-result-boundary-gates", response_model=AnalysisResultBoundaryGate)
def analysis_request_analysis_result_boundary_gate_create(
    request_id: str,
    payload: AnalysisResultBoundaryGateRequest,
) -> AnalysisResultBoundaryGate:
    try:
        return create_analysis_result_boundary_gate(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/analysis-result-boundary-gates/{boundary_gate_id}", response_model=AnalysisResultBoundaryGate)
def analysis_request_analysis_result_boundary_gate_detail(
    request_id: str,
    boundary_gate_id: str,
) -> AnalysisResultBoundaryGate:
    try:
        return read_analysis_result_boundary_gate(request_id, boundary_gate_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/analysis-result-boundary-gate-audits", response_model=list[AnalysisResultBoundaryGateAudit])
def analysis_request_analysis_result_boundary_gate_audit_list(request_id: str) -> list[AnalysisResultBoundaryGateAudit]:
    try:
        return list_analysis_result_boundary_gate_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/analysis-result-boundary-gates/{boundary_gate_id}/audits",
    response_model=list[AnalysisResultBoundaryGateAudit],
)
def analysis_request_analysis_result_boundary_gate_audit_for_gate_list(
    request_id: str,
    boundary_gate_id: str,
) -> list[AnalysisResultBoundaryGateAudit]:
    try:
        return list_analysis_result_boundary_gate_audits_for_gate(request_id, boundary_gate_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/manual-analysis-executions", response_model=list[ManualAnalysisExecution])
def analysis_request_manual_analysis_execution_list(request_id: str) -> list[ManualAnalysisExecution]:
    try:
        return list_manual_analysis_executions(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/manual-analysis-executions", response_model=ManualAnalysisExecution)
def analysis_request_manual_analysis_execution_create(
    request_id: str,
    payload: ManualAnalysisExecutionRequest,
) -> ManualAnalysisExecution:
    try:
        return create_manual_analysis_execution(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/manual-analysis-executions/{manual_analysis_execution_id}", response_model=ManualAnalysisExecution)
def analysis_request_manual_analysis_execution_detail(
    request_id: str,
    manual_analysis_execution_id: str,
) -> ManualAnalysisExecution:
    try:
        return read_manual_analysis_execution(request_id, manual_analysis_execution_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/manual-analysis-result-candidates", response_model=list[ManualAnalysisResultCandidate])
def analysis_request_manual_analysis_result_candidate_list(request_id: str) -> list[ManualAnalysisResultCandidate]:
    try:
        return list_manual_analysis_result_candidates(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/manual-analysis-result-candidates/{result_candidate_id}",
    response_model=ManualAnalysisResultCandidate,
)
def analysis_request_manual_analysis_result_candidate_detail(
    request_id: str,
    result_candidate_id: str,
) -> ManualAnalysisResultCandidate:
    try:
        return read_manual_analysis_result_candidate(request_id, result_candidate_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/manual-analysis-execution-audits", response_model=list[ManualAnalysisExecutionAudit])
def analysis_request_manual_analysis_execution_audit_list(request_id: str) -> list[ManualAnalysisExecutionAudit]:
    try:
        return list_manual_analysis_execution_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/manual-analysis-executions/{manual_analysis_execution_id}/audits",
    response_model=list[ManualAnalysisExecutionAudit],
)
def analysis_request_manual_analysis_execution_audit_for_execution_list(
    request_id: str,
    manual_analysis_execution_id: str,
) -> list[ManualAnalysisExecutionAudit]:
    try:
        return list_manual_analysis_execution_audits_for_execution(request_id, manual_analysis_execution_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/report-generation-gates", response_model=list[ReportGenerationGate])
def analysis_request_report_generation_gate_list(request_id: str) -> list[ReportGenerationGate]:
    try:
        return list_report_generation_gates(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/report-generation-gates", response_model=ReportGenerationGate)
def analysis_request_report_generation_gate_create(
    request_id: str,
    payload: ReportGenerationGateRequest,
) -> ReportGenerationGate:
    try:
        return create_report_generation_gate(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/report-generation-gates/{report_gate_id}", response_model=ReportGenerationGate)
def analysis_request_report_generation_gate_detail(
    request_id: str,
    report_gate_id: str,
) -> ReportGenerationGate:
    try:
        return read_report_generation_gate(request_id, report_gate_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/report-generation-gate-audits", response_model=list[ReportGenerationGateAudit])
def analysis_request_report_generation_gate_audit_list(request_id: str) -> list[ReportGenerationGateAudit]:
    try:
        return list_report_generation_gate_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/report-generation-gates/{report_gate_id}/audits",
    response_model=list[ReportGenerationGateAudit],
)
def analysis_request_report_generation_gate_audit_for_gate_list(
    request_id: str,
    report_gate_id: str,
) -> list[ReportGenerationGateAudit]:
    try:
        return list_report_generation_gate_audits_for_gate(request_id, report_gate_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/summary-report-candidates", response_model=list[SummaryReportCandidate])
def analysis_request_summary_report_candidate_list(request_id: str) -> list[SummaryReportCandidate]:
    try:
        return list_summary_report_candidates(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/summary-report-candidates", response_model=SummaryReportCandidate)
def analysis_request_summary_report_candidate_create(
    request_id: str,
    payload: SummaryReportCandidateRequest,
) -> SummaryReportCandidate:
    try:
        return create_summary_report_candidate(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/summary-report-candidates/{summary_report_candidate_id}",
    response_model=SummaryReportCandidate,
)
def analysis_request_summary_report_candidate_detail(
    request_id: str,
    summary_report_candidate_id: str,
) -> SummaryReportCandidate:
    try:
        return read_summary_report_candidate(request_id, summary_report_candidate_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/summary-report-candidate-audits", response_model=list[SummaryReportCandidateAudit])
def analysis_request_summary_report_candidate_audit_list(request_id: str) -> list[SummaryReportCandidateAudit]:
    try:
        return list_summary_report_candidate_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/summary-report-candidates/{summary_report_candidate_id}/audits",
    response_model=list[SummaryReportCandidateAudit],
)
def analysis_request_summary_report_candidate_audit_for_candidate_list(
    request_id: str,
    summary_report_candidate_id: str,
) -> list[SummaryReportCandidateAudit]:
    try:
        return list_summary_report_candidate_audits_for_candidate(request_id, summary_report_candidate_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/final-summary-report-review-gates", response_model=list[FinalSummaryReportReviewGate])
def analysis_request_final_summary_report_review_gate_list(request_id: str) -> list[FinalSummaryReportReviewGate]:
    try:
        return list_final_summary_report_review_gates(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/final-summary-report-review-gates", response_model=FinalSummaryReportReviewGate)
def analysis_request_final_summary_report_review_gate_create(
    request_id: str,
    payload: FinalSummaryReportReviewGateRequest,
) -> FinalSummaryReportReviewGate:
    try:
        return create_final_summary_report_review_gate(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/final-summary-report-review-gates/{final_report_review_gate_id}",
    response_model=FinalSummaryReportReviewGate,
)
def analysis_request_final_summary_report_review_gate_detail(
    request_id: str,
    final_report_review_gate_id: str,
) -> FinalSummaryReportReviewGate:
    try:
        return read_final_summary_report_review_gate(request_id, final_report_review_gate_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/final-summary-report-review-gate-audits", response_model=list[FinalSummaryReportReviewGateAudit])
def analysis_request_final_summary_report_review_gate_audit_list(request_id: str) -> list[FinalSummaryReportReviewGateAudit]:
    try:
        return list_final_summary_report_review_gate_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/final-summary-report-review-gates/{final_report_review_gate_id}/audits",
    response_model=list[FinalSummaryReportReviewGateAudit],
)
def analysis_request_final_summary_report_review_gate_audit_for_gate_list(
    request_id: str,
    final_report_review_gate_id: str,
) -> list[FinalSummaryReportReviewGateAudit]:
    try:
        return list_final_summary_report_review_gate_audits_for_gate(request_id, final_report_review_gate_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/final-summary-reports", response_model=list[FinalSummaryReport])
def analysis_request_final_summary_report_list(request_id: str) -> list[FinalSummaryReport]:
    try:
        return list_final_summary_reports(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/final-summary-reports", response_model=FinalSummaryReport)
def analysis_request_final_summary_report_create(
    request_id: str,
    payload: FinalSummaryReportRequest,
) -> FinalSummaryReport:
    try:
        return create_final_summary_report(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/final-summary-reports/{final_summary_report_id}",
    response_model=FinalSummaryReport,
)
def analysis_request_final_summary_report_detail(
    request_id: str,
    final_summary_report_id: str,
) -> FinalSummaryReport:
    try:
        return read_final_summary_report(request_id, final_summary_report_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/final-summary-report-audits", response_model=list[FinalSummaryReportAudit])
def analysis_request_final_summary_report_audit_list(request_id: str) -> list[FinalSummaryReportAudit]:
    try:
        return list_final_summary_report_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/final-summary-reports/{final_summary_report_id}/audits",
    response_model=list[FinalSummaryReportAudit],
)
def analysis_request_final_summary_report_audit_for_report_list(
    request_id: str,
    final_summary_report_id: str,
) -> list[FinalSummaryReportAudit]:
    try:
        return list_final_summary_report_audits_for_report(request_id, final_summary_report_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/final-summary-report-export-gates", response_model=list[FinalSummaryReportExportGate])
def analysis_request_final_summary_report_export_gate_list(request_id: str) -> list[FinalSummaryReportExportGate]:
    try:
        return list_final_summary_report_export_gates(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/final-summary-report-export-gates", response_model=FinalSummaryReportExportGate)
def analysis_request_final_summary_report_export_gate_create(
    request_id: str,
    payload: FinalSummaryReportExportGateRequest,
) -> FinalSummaryReportExportGate:
    try:
        return create_final_summary_report_export_gate(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/final-summary-report-export-gates/{export_gate_id}",
    response_model=FinalSummaryReportExportGate,
)
def analysis_request_final_summary_report_export_gate_detail(
    request_id: str,
    export_gate_id: str,
) -> FinalSummaryReportExportGate:
    try:
        return read_final_summary_report_export_gate(request_id, export_gate_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/final-summary-report-export-gate-audits", response_model=list[FinalSummaryReportExportGateAudit])
def analysis_request_final_summary_report_export_gate_audit_list(request_id: str) -> list[FinalSummaryReportExportGateAudit]:
    try:
        return list_final_summary_report_export_gate_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/final-summary-report-export-gates/{export_gate_id}/audits",
    response_model=list[FinalSummaryReportExportGateAudit],
)
def analysis_request_final_summary_report_export_gate_audit_for_gate_list(
    request_id: str,
    export_gate_id: str,
) -> list[FinalSummaryReportExportGateAudit]:
    try:
        return list_final_summary_report_export_gate_audits_for_gate(request_id, export_gate_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/final-summary-report-export-artifacts", response_model=list[FinalSummaryReportExportArtifact])
def analysis_request_final_summary_report_export_artifact_list(request_id: str) -> list[FinalSummaryReportExportArtifact]:
    try:
        return list_final_summary_report_export_artifacts(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/final-summary-report-export-artifacts", response_model=FinalSummaryReportExportArtifact)
def analysis_request_final_summary_report_export_artifact_create(
    request_id: str,
    payload: FinalSummaryReportExportArtifactRequest,
) -> FinalSummaryReportExportArtifact:
    try:
        return create_final_summary_report_export_artifact(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/final-summary-report-export-artifacts/{export_artifact_id}",
    response_model=FinalSummaryReportExportArtifact,
)
def analysis_request_final_summary_report_export_artifact_detail(
    request_id: str,
    export_artifact_id: str,
) -> FinalSummaryReportExportArtifact:
    try:
        return read_final_summary_report_export_artifact(request_id, export_artifact_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/final-summary-report-export-artifact-audits", response_model=list[FinalSummaryReportExportArtifactAudit])
def analysis_request_final_summary_report_export_artifact_audit_list(request_id: str) -> list[FinalSummaryReportExportArtifactAudit]:
    try:
        return list_final_summary_report_export_artifact_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/final-summary-report-export-artifacts/{export_artifact_id}/audits",
    response_model=list[FinalSummaryReportExportArtifactAudit],
)
def analysis_request_final_summary_report_export_artifact_audit_for_artifact_list(
    request_id: str,
    export_artifact_id: str,
) -> list[FinalSummaryReportExportArtifactAudit]:
    try:
        return list_final_summary_report_export_artifact_audits_for_artifact(request_id, export_artifact_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/report-export-download-package-gates", response_model=list[ReportExportDownloadPackageGate])
def analysis_request_report_export_download_package_gate_list(request_id: str) -> list[ReportExportDownloadPackageGate]:
    try:
        return list_report_export_download_package_gates(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/report-export-download-package-gates", response_model=ReportExportDownloadPackageGate)
def analysis_request_report_export_download_package_gate_create(
    request_id: str,
    payload: ReportExportDownloadPackageGateRequest,
) -> ReportExportDownloadPackageGate:
    try:
        return create_report_export_download_package_gate(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/report-export-download-package-gates/{download_package_gate_id}",
    response_model=ReportExportDownloadPackageGate,
)
def analysis_request_report_export_download_package_gate_detail(
    request_id: str,
    download_package_gate_id: str,
) -> ReportExportDownloadPackageGate:
    try:
        return read_report_export_download_package_gate(request_id, download_package_gate_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/report-export-download-package-gate-audits", response_model=list[ReportExportDownloadPackageGateAudit])
def analysis_request_report_export_download_package_gate_audit_list(request_id: str) -> list[ReportExportDownloadPackageGateAudit]:
    try:
        return list_report_export_download_package_gate_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/report-export-download-package-gates/{download_package_gate_id}/audits",
    response_model=list[ReportExportDownloadPackageGateAudit],
)
def analysis_request_report_export_download_package_gate_audit_for_gate_list(
    request_id: str,
    download_package_gate_id: str,
) -> list[ReportExportDownloadPackageGateAudit]:
    try:
        return list_report_export_download_package_gate_audits_for_gate(request_id, download_package_gate_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/report-export-download-package-artifacts", response_model=list[ReportExportDownloadPackageArtifact])
def analysis_request_report_export_download_package_artifact_list(request_id: str) -> list[ReportExportDownloadPackageArtifact]:
    try:
        return list_report_export_download_package_artifacts(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{request_id}/report-export-download-package-artifacts", response_model=ReportExportDownloadPackageArtifact)
def analysis_request_report_export_download_package_artifact_create(
    request_id: str,
    payload: ReportExportDownloadPackageArtifactRequest,
) -> ReportExportDownloadPackageArtifact:
    try:
        return create_report_export_download_package_artifact(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/report-export-download-package-artifacts/{package_artifact_id}",
    response_model=ReportExportDownloadPackageArtifact,
)
def analysis_request_report_export_download_package_artifact_detail(
    request_id: str,
    package_artifact_id: str,
) -> ReportExportDownloadPackageArtifact:
    try:
        return read_report_export_download_package_artifact(request_id, package_artifact_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{request_id}/report-export-download-package-artifact-audits", response_model=list[ReportExportDownloadPackageArtifactAudit])
def analysis_request_report_export_download_package_artifact_audit_list(request_id: str) -> list[ReportExportDownloadPackageArtifactAudit]:
    try:
        return list_report_export_download_package_artifact_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/report-export-download-package-artifacts/{package_artifact_id}/audits",
    response_model=list[ReportExportDownloadPackageArtifactAudit],
)
def analysis_request_report_export_download_package_artifact_audit_for_artifact_list(
    request_id: str,
    package_artifact_id: str,
) -> list[ReportExportDownloadPackageArtifactAudit]:
    try:
        return list_report_export_download_package_artifact_audits_for_artifact(request_id, package_artifact_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/report-export-public-access-external-delivery-gates",
    response_model=list[ReportExportPublicAccessExternalDeliveryGate],
)
def analysis_request_report_export_public_access_external_delivery_gate_list(
    request_id: str,
) -> list[ReportExportPublicAccessExternalDeliveryGate]:
    try:
        return list_report_export_public_access_external_delivery_gates(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post(
    "/{request_id}/report-export-public-access-external-delivery-gates",
    response_model=ReportExportPublicAccessExternalDeliveryGate,
)
def analysis_request_report_export_public_access_external_delivery_gate_create(
    request_id: str,
    payload: ReportExportPublicAccessExternalDeliveryGateRequest,
) -> ReportExportPublicAccessExternalDeliveryGate:
    try:
        return create_report_export_public_access_external_delivery_gate(request_id, payload)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/report-export-public-access-external-delivery-gates/{public_access_delivery_gate_id}",
    response_model=ReportExportPublicAccessExternalDeliveryGate,
)
def analysis_request_report_export_public_access_external_delivery_gate_detail(
    request_id: str,
    public_access_delivery_gate_id: str,
) -> ReportExportPublicAccessExternalDeliveryGate:
    try:
        return read_report_export_public_access_external_delivery_gate(request_id, public_access_delivery_gate_id)
    except AnalysisRequestNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/report-export-public-access-external-delivery-gate-audits",
    response_model=list[ReportExportPublicAccessExternalDeliveryGateAudit],
)
def analysis_request_report_export_public_access_external_delivery_gate_audit_list(
    request_id: str,
) -> list[ReportExportPublicAccessExternalDeliveryGateAudit]:
    try:
        return list_report_export_public_access_external_delivery_gate_audits(request_id)
    except AnalysisRequestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{request_id}/report-export-public-access-external-delivery-gates/{public_access_delivery_gate_id}/audits",
    response_model=list[ReportExportPublicAccessExternalDeliveryGateAudit],
)
def analysis_request_report_export_public_access_external_delivery_gate_audit_for_gate_list(
    request_id: str,
    public_access_delivery_gate_id: str,
) -> list[ReportExportPublicAccessExternalDeliveryGateAudit]:
    try:
        return list_report_export_public_access_external_delivery_gate_audits_for_gate(request_id, public_access_delivery_gate_id)
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
