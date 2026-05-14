from fastapi import APIRouter, HTTPException

from app.schemas.case import (
    AnalysisCaseCreateRequest,
    AnalysisCaseDetail,
    AnalysisCaseListItem,
    MarkdownExportResponse,
)
from app.services.case_store import create_case, export_case_markdown, get_case, list_cases, run_case

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


@router.get("/{case_id}/report/markdown", response_model=MarkdownExportResponse)
def get_case_markdown_report(case_id: str) -> MarkdownExportResponse:
    report = export_case_markdown(case_id)
    if not report:
        raise HTTPException(status_code=404, detail="Markdown report is not available for this case.")
    return report
