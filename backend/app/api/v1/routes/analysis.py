from fastapi import APIRouter

from app.schemas.analysis import AnalysisResultResponse, AnalysisRunRequest, AnalysisRunResponse
from app.services.mock_service import get_mock_analysis_result, run_mock_analysis

router = APIRouter()


@router.post("/run", response_model=AnalysisRunResponse)
def run_analysis(payload: AnalysisRunRequest) -> AnalysisRunResponse:
    return run_mock_analysis(payload)


@router.get("/{project_id}", response_model=AnalysisResultResponse)
def get_analysis(project_id: str) -> AnalysisResultResponse:
    return get_mock_analysis_result(project_id)

