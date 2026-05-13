from fastapi import APIRouter

from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.services.mock_service import generate_mock_recommendation

router = APIRouter()


@router.post("/generate", response_model=RecommendationResponse)
def generate_recommendation(payload: RecommendationRequest) -> RecommendationResponse:
    return generate_mock_recommendation(payload)

