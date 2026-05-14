from fastapi import APIRouter

from app.schemas.scheduler import SchedulerRunDueResponse, SchedulerStatus
from app.services.monitoring.scheduler_service import get_scheduler_status, run_due_monitoring_jobs

router = APIRouter()


@router.get("/status", response_model=SchedulerStatus)
def get_status() -> SchedulerStatus:
    return get_scheduler_status()


@router.post("/run-due", response_model=SchedulerRunDueResponse)
def run_due() -> SchedulerRunDueResponse:
    return run_due_monitoring_jobs()
