from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.alert import AlertThresholdConfig, MonitoringStatus


MonitoringScheduleStatus = Literal["disabled", "scheduled", "due"]


class MonitoringScheduleConfig(BaseModel):
    enabled: bool = False
    interval_minutes: int = Field(default=60, ge=5, le=1440)
    last_run_at: datetime | None = None
    next_run_at: datetime | None = None
    threshold_config: AlertThresholdConfig = Field(default_factory=AlertThresholdConfig)
    status: MonitoringScheduleStatus = "disabled"


class MonitoringJobState(BaseModel):
    case_id: str
    title: str
    keyword: str
    enabled: bool
    interval_minutes: int
    last_run_at: datetime | None = None
    next_run_at: datetime | None = None
    status: MonitoringScheduleStatus
    is_due: bool
    snapshot_count: int = 0
    alert_count: int = 0


class SchedulerStatus(BaseModel):
    background_scheduler_running: bool = False
    total_cases: int = 0
    enabled_cases: int = 0
    due_cases: int = 0
    next_due_at: datetime | None = None
    job_states: list[MonitoringJobState] = Field(default_factory=list)
    message: str


class SchedulerRunDueResponse(BaseModel):
    checked_at: datetime
    due_case_count: int
    executed_case_count: int
    skipped_case_count: int
    monitoring_results: list[MonitoringStatus] = Field(default_factory=list)
    job_states: list[MonitoringJobState] = Field(default_factory=list)
    message: str
