from app.schemas.common import RiskLevel
from pydantic import BaseModel


class AlertItem(BaseModel):
    alert_id: str
    level: RiskLevel
    message: str
    created_at: str
    resolved: bool


class AlertsResponse(BaseModel):
    project_id: str
    alerts: list[AlertItem]

