from fastapi import APIRouter

from app.schemas.summary import SummaryGenerateRequest, SummaryGenerateResponse
from app.services.mock_service import generate_mock_summary

router = APIRouter()


@router.post("/generate", response_model=SummaryGenerateResponse)
def generate_summary(payload: SummaryGenerateRequest) -> SummaryGenerateResponse:
    return generate_mock_summary(payload)

