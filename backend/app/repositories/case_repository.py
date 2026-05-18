from __future__ import annotations

from datetime import datetime, timedelta, timezone
import re

from app.schemas.analysis import AnalysisResultResponse
from app.schemas.alert import AlertEvent, AnalysisSnapshot
from app.schemas.case import (
    AnalysisCaseCreateRequest,
    AnalysisCaseDetail,
    AnalysisCaseListItem,
    MarkdownExportResponse,
)
from app.schemas.comment import RawComment, RawPost
from app.schemas.common import RiskLevel
from app.schemas.crawl import PlatformCrawlMetadata
from app.schemas.notification import NotificationOutboxItem
from app.schemas.report import PublicOpinionReport
from app.schemas.scheduler import MonitoringScheduleConfig
from app.schemas.visualization import VisualizationResponse
from app.services.storage.base_store import CaseStore


BASE_TIME = datetime(2026, 5, 14, 9, 0, 0, tzinfo=timezone.utc)


class CaseRepository:
    """Repository facade for analysis case persistence."""

    def __init__(self, store: CaseStore) -> None:
        self.store = store

    def create_case(self, payload: AnalysisCaseCreateRequest) -> AnalysisCaseDetail:
        case_number = self._next_case_number()
        case_id = f"case_{case_number:03d}"
        project_id = f"project_{case_number:03d}"
        timestamp = self.next_timestamp()
        keyword = payload.keyword.strip()
        title = (payload.title or f"{keyword} \u8206\u60c5\u5206\u6790").strip()

        detail = AnalysisCaseDetail(
            case_id=case_id,
            project_id=project_id,
            title=title,
            keyword=keyword,
            platforms=_normalize_platforms(payload.platforms),
            status="draft",
            created_at=timestamp,
            updated_at=timestamp,
            report_language=payload.report_language,
        )
        return self.store.create_case(detail)

    def list_cases(self) -> list[AnalysisCaseListItem]:
        cases = sorted(self.store.list_cases(), key=lambda item: item.updated_at, reverse=True)
        return [_to_list_item(case) for case in cases]

    def get_case(self, case_id: str) -> AnalysisCaseDetail | None:
        return self.store.get_case(case_id)

    def update_case(self, case: AnalysisCaseDetail) -> AnalysisCaseDetail:
        return self.store.update_case(case)

    def save_case_raw_data(
        self,
        case_id: str,
        *,
        raw_posts: list[RawPost],
        raw_comments: list[RawComment],
        crawl_metadata: list[PlatformCrawlMetadata],
        crawl_source_mode: str,
        raw_data_status: str,
        attached_at: datetime | None = None,
    ) -> AnalysisCaseDetail | None:
        case = self.get_case(case_id)
        if not case:
            return None
        timestamp = attached_at or self.next_timestamp()
        updated_case = case.model_copy(
            update={
                "raw_posts": raw_posts,
                "raw_comments": raw_comments,
                "crawl_metadata": crawl_metadata,
                "crawl_source_mode": crawl_source_mode,
                "crawl_attached_at": timestamp,
                "raw_data_status": raw_data_status,
                "raw_post_count": len(raw_posts),
                "raw_comment_count": len(raw_comments),
                "updated_at": timestamp,
            },
            deep=True,
        )
        return self.update_case(updated_case)

    def get_monitoring_config(self, case_id: str) -> MonitoringScheduleConfig | None:
        case = self.get_case(case_id)
        return case.monitoring_config if case else None

    def save_monitoring_config(
        self,
        case_id: str,
        config: MonitoringScheduleConfig,
        *,
        updated_at: datetime | None = None,
    ) -> AnalysisCaseDetail | None:
        case = self.get_case(case_id)
        if not case:
            return None
        updated_case = case.model_copy(
            update={
                "monitoring_config": config,
                "updated_at": updated_at or self.next_timestamp(),
            },
            deep=True,
        )
        return self.update_case(updated_case)

    def save_analysis_result(
        self,
        case_id: str,
        *,
        analysis_result: AnalysisResultResponse,
        visualization_data: VisualizationResponse | None = None,
        risk_score: float | None = None,
        risk_level: RiskLevel | None = None,
        risk_model_version: str | None = None,
        updated_at: datetime | None = None,
    ) -> AnalysisCaseDetail | None:
        return self.store.save_analysis_result(
            case_id,
            analysis_result=analysis_result,
            visualization_data=visualization_data,
            risk_score=risk_score,
            risk_level=risk_level,
            risk_model_version=risk_model_version,
            updated_at=updated_at or self.next_timestamp(),
        )

    def save_report(
        self,
        case_id: str,
        *,
        report: PublicOpinionReport,
        updated_at: datetime | None = None,
        markdown_available: bool = True,
    ) -> AnalysisCaseDetail | None:
        return self.store.save_report(
            case_id,
            report=report,
            updated_at=updated_at or self.next_timestamp(),
            markdown_available=markdown_available,
        )

    def save_markdown_report(self, case_id: str, report: MarkdownExportResponse) -> MarkdownExportResponse:
        return self.store.save_markdown_report(case_id, report)

    def get_markdown_report(self, case_id: str) -> MarkdownExportResponse | None:
        return self.store.get_markdown_report(case_id)

    def save_analysis_snapshot(self, case_id: str, snapshot: AnalysisSnapshot) -> AnalysisSnapshot:
        return self.store.save_analysis_snapshot(case_id, snapshot)

    def list_analysis_snapshots(self, case_id: str) -> list[AnalysisSnapshot]:
        return self.store.list_analysis_snapshots(case_id)

    def save_alert_events(self, case_id: str, alerts: list[AlertEvent]) -> list[AlertEvent]:
        return self.store.save_alert_events(case_id, alerts)

    def list_case_alerts(self, case_id: str) -> list[AlertEvent]:
        return self.store.list_case_alerts(case_id)

    def list_all_alert_events(self) -> list[AlertEvent]:
        return self.store.list_all_alert_events()

    def save_notification(self, notification: NotificationOutboxItem) -> NotificationOutboxItem:
        return self.store.save_notification(notification)

    def get_notification(self, notification_id: str) -> NotificationOutboxItem | None:
        return self.store.get_notification(notification_id)

    def update_notification(self, notification: NotificationOutboxItem) -> NotificationOutboxItem | None:
        return self.store.update_notification(notification)

    def list_notifications(self) -> list[NotificationOutboxItem]:
        return self.store.list_notifications()

    def list_case_notifications(self, case_id: str) -> list[NotificationOutboxItem]:
        return self.store.list_case_notifications(case_id)

    def reset(self) -> None:
        self.store.reset()

    def next_timestamp(self) -> datetime:
        timestamps = [BASE_TIME - timedelta(minutes=1)]
        for case in self.store.list_cases():
            timestamps.extend([case.created_at, case.updated_at])
        for markdown_report in self.store.list_markdown_reports():
            timestamps.append(markdown_report.generated_at)
        for case in self.store.list_cases():
            for snapshot in self.store.list_analysis_snapshots(case.case_id):
                timestamps.append(snapshot.created_at)
            for alert in self.store.list_case_alerts(case.case_id):
                timestamps.append(alert.created_at)
        for notification in self.store.list_notifications():
            timestamps.append(notification.created_at)
            if notification.read_at:
                timestamps.append(notification.read_at)
            if notification.simulated_sent_at:
                timestamps.append(notification.simulated_sent_at)
        latest = max(_ensure_aware(timestamp) for timestamp in timestamps)
        return latest + timedelta(minutes=1)

    def next_snapshot_number(self, case_id: str) -> int:
        max_number = 0
        for snapshot in self.store.list_analysis_snapshots(case_id):
            match = re.fullmatch(rf"{re.escape(case_id)}_snapshot_(\d+)", snapshot.snapshot_id)
            if match:
                max_number = max(max_number, int(match.group(1)))
        return max_number + 1

    def _next_case_number(self) -> int:
        max_number = 0
        for case in self.store.list_cases():
            match = re.fullmatch(r"case_(\d+)", case.case_id)
            if match:
                max_number = max(max_number, int(match.group(1)))
        return max_number + 1


def _to_list_item(case: AnalysisCaseDetail) -> AnalysisCaseListItem:
    return AnalysisCaseListItem(
        case_id=case.case_id,
        project_id=case.project_id,
        title=case.title,
        keyword=case.keyword,
        platforms=case.platforms,
        status=case.status,
        created_at=case.created_at,
        updated_at=case.updated_at,
        risk_score=case.risk_score,
        risk_level=case.risk_level,
        risk_model_version=case.risk_model_version,
        report_language=case.report_language,
        monitoring_config=case.monitoring_config,
    )


def _normalize_platforms(platforms: list[str]) -> list[str]:
    return list(dict.fromkeys(platform.strip().lower() for platform in platforms if platform.strip()))


def _ensure_aware(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
