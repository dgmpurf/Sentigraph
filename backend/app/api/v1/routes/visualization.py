from fastapi import APIRouter

from app.schemas.visualization import VisualizationDataRequest, VisualizationResponse
from app.services.mock_service import get_mock_visualization

router = APIRouter()


@router.post("/data", response_model=VisualizationResponse)
def get_visualization_data(payload: VisualizationDataRequest) -> VisualizationResponse:
    return get_mock_visualization(payload)

