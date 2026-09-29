from fastapi import APIRouter

from app.schemas.alert import AlertEventView, AlertsResponse
from app.services.case_store import get_case_repository, list_all_case_alerts
from app.services.mock_service import get_mock_alerts

router = APIRouter()


@router.get("", response_model=list[AlertEventView])
def get_all_alerts() -> list[AlertEventView]:
    repository = get_case_repository()
    return [repository.alert_view(alert) for alert in list_all_case_alerts()]


@router.get("/{project_id}", response_model=AlertsResponse)
def get_alerts(project_id: str) -> AlertsResponse:
    return get_mock_alerts(project_id)
