from fastapi import APIRouter

from app.schemas.alert import AlertsResponse
from app.services.mock_service import get_mock_alerts

router = APIRouter()


@router.get("/{project_id}", response_model=AlertsResponse)
def get_alerts(project_id: str) -> AlertsResponse:
    return get_mock_alerts(project_id)

