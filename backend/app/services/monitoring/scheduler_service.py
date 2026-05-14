from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.repositories.case_repository import CaseRepository
from app.schemas.case import AnalysisCaseDetail
from app.schemas.scheduler import (
    MonitoringJobState,
    MonitoringScheduleConfig,
    SchedulerRunDueResponse,
    SchedulerStatus,
)
from app.services.case_store import get_case_repository, run_monitoring_check


def get_scheduler_status() -> SchedulerStatus:
    repository = get_case_repository()
    now = repository.next_timestamp()
    job_states = _list_job_states(repository, now)
    enabled_jobs = [job for job in job_states if job.enabled]
    due_jobs = [job for job in enabled_jobs if job.is_due]
    future_due_times = [job.next_run_at for job in enabled_jobs if job.next_run_at and not job.is_due]

    return SchedulerStatus(
        background_scheduler_running=False,
        total_cases=len(job_states),
        enabled_cases=len(enabled_jobs),
        due_cases=len(due_jobs),
        next_due_at=min(future_due_times) if future_due_times else None,
        job_states=job_states,
        message="Manual scheduler foundation is configured; no background worker is running.",
    )


def get_case_monitoring_config(case_id: str) -> MonitoringScheduleConfig | None:
    repository = get_case_repository()
    case = repository.get_case(case_id)
    return case.monitoring_config if case else None


def update_case_monitoring_config(
    case_id: str,
    config: MonitoringScheduleConfig,
) -> MonitoringScheduleConfig | None:
    repository = get_case_repository()
    case = repository.get_case(case_id)
    if not case:
        return None

    now = repository.next_timestamp()
    normalized = _normalize_config(config, now=now)
    updated = repository.save_monitoring_config(case_id, normalized, updated_at=now)
    return updated.monitoring_config if updated else None


def enable_case_monitoring(case_id: str) -> MonitoringScheduleConfig | None:
    repository = get_case_repository()
    case = repository.get_case(case_id)
    if not case:
        return None

    now = repository.next_timestamp()
    existing = case.monitoring_config
    config = existing.model_copy(
        update={
            "enabled": True,
            "next_run_at": now,
            "status": "due",
        },
        deep=True,
    )
    updated = repository.save_monitoring_config(case_id, config, updated_at=now)
    return updated.monitoring_config if updated else None


def disable_case_monitoring(case_id: str) -> MonitoringScheduleConfig | None:
    repository = get_case_repository()
    case = repository.get_case(case_id)
    if not case:
        return None

    now = repository.next_timestamp()
    config = case.monitoring_config.model_copy(
        update={
            "enabled": False,
            "next_run_at": None,
            "status": "disabled",
        },
        deep=True,
    )
    updated = repository.save_monitoring_config(case_id, config, updated_at=now)
    return updated.monitoring_config if updated else None


def run_due_monitoring_jobs() -> SchedulerRunDueResponse:
    repository = get_case_repository()
    checked_at = repository.next_timestamp()
    cases = _list_case_details(repository)
    initial_states = _list_job_states(repository, checked_at)
    skipped_count = sum(1 for job in initial_states if job.enabled and not job.is_due)
    due_cases = [
        case
        for case in cases
        if _is_enabled(case.monitoring_config)
        and _is_due(case.monitoring_config, checked_at)
    ]
    monitoring_results = []

    for case in due_cases:
        status = run_monitoring_check(case.case_id, threshold_config=case.monitoring_config.threshold_config)
        if not status:
            continue
        monitoring_results.append(status)
        _mark_case_schedule_ran(repository, case.case_id, case.monitoring_config, status.latest_snapshot.created_at)

    refreshed_states = _list_job_states(repository, checked_at)

    return SchedulerRunDueResponse(
        checked_at=checked_at,
        due_case_count=len(due_cases),
        executed_case_count=len(monitoring_results),
        skipped_case_count=skipped_count,
        monitoring_results=monitoring_results,
        job_states=refreshed_states,
        message=(
            f"Executed {len(monitoring_results)} due monitoring job(s)."
            if monitoring_results
            else "No due monitoring jobs were executed."
        ),
    )


def _mark_case_schedule_ran(
    repository: CaseRepository,
    case_id: str,
    config: MonitoringScheduleConfig,
    last_run_at: datetime,
) -> None:
    next_run_at = _as_utc(last_run_at) + timedelta(minutes=config.interval_minutes)
    updated_config = config.model_copy(
        update={
            "enabled": True,
            "last_run_at": last_run_at,
            "next_run_at": next_run_at,
            "status": "scheduled",
        },
        deep=True,
    )
    repository.save_monitoring_config(case_id, updated_config, updated_at=last_run_at)


def _normalize_config(config: MonitoringScheduleConfig, *, now: datetime) -> MonitoringScheduleConfig:
    if not config.enabled:
        return config.model_copy(update={"enabled": False, "next_run_at": None, "status": "disabled"}, deep=True)

    next_run_at = config.next_run_at or now
    return config.model_copy(
        update={
            "enabled": True,
            "next_run_at": next_run_at,
            "status": "due" if _is_due_time(next_run_at, now) else "scheduled",
        },
        deep=True,
    )


def _list_job_states(repository: CaseRepository, now: datetime) -> list[MonitoringJobState]:
    return [_build_job_state(repository, case, now) for case in _list_case_details(repository)]


def _list_case_details(repository: CaseRepository) -> list[AnalysisCaseDetail]:
    details: list[AnalysisCaseDetail] = []
    for item in repository.list_cases():
        case = repository.get_case(item.case_id)
        if case:
            details.append(case)
    return details


def _build_job_state(repository: CaseRepository, case: AnalysisCaseDetail, now: datetime) -> MonitoringJobState:
    config = case.monitoring_config
    is_due = _is_enabled(config) and _is_due(config, now)
    status = "disabled"
    if config.enabled:
        status = "due" if is_due else "scheduled"

    return MonitoringJobState(
        case_id=case.case_id,
        title=case.title,
        keyword=case.keyword,
        enabled=config.enabled,
        interval_minutes=config.interval_minutes,
        last_run_at=config.last_run_at,
        next_run_at=config.next_run_at,
        status=status,
        is_due=is_due,
        snapshot_count=len(repository.list_analysis_snapshots(case.case_id)),
        alert_count=len(repository.list_case_alerts(case.case_id)),
    )


def _is_enabled(config: MonitoringScheduleConfig) -> bool:
    return bool(config.enabled and config.next_run_at)


def _is_due(config: MonitoringScheduleConfig, now: datetime) -> bool:
    return bool(config.next_run_at and _is_due_time(config.next_run_at, now))


def _is_due_time(next_run_at: datetime, now: datetime) -> bool:
    return _as_utc(next_run_at) <= _as_utc(now)


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
