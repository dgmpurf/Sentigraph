from __future__ import annotations

from abc import ABC, abstractmethod
from app.schemas.alert import AlertEvent, AnalysisSnapshot
from app.schemas.case import AnalysisCaseDetail, MarkdownExportResponse
from app.schemas.notification import NotificationOutboxItem


class CaseRevisionConflict(RuntimeError):
    """A persisted case no longer matches a caller's expected revision."""

    def __init__(self, case_id: str, expected_revision: int, current_revision: int | None = None) -> None:
        self.case_id = case_id
        self.expected_revision = expected_revision
        self.current_revision = current_revision
        super().__init__("case_revision_conflict")


def validate_case_revision_precondition(case: AnalysisCaseDetail, expected_revision: int) -> None:
    """Reject malformed CAS requests before either storage backend writes."""
    if type(expected_revision) is not int or expected_revision < 0:
        raise ValueError("expected_revision must be a nonnegative integer")
    if case.case_revision != expected_revision:
        raise ValueError("case.case_revision must equal expected_revision")


class CaseStore(ABC):
    """Persistence interface for Sentigraph analysis cases.

    Local JSON remains the default MVP backend. Optional MongoDB persistence
    must stay behind this same interface and be enabled only by configuration.
    """

    @abstractmethod
    def create_case(self, case: AnalysisCaseDetail) -> AnalysisCaseDetail:
        """Persist a newly-created case."""

    @abstractmethod
    def list_cases(self) -> list[AnalysisCaseDetail]:
        """Return all persisted case details."""

    @abstractmethod
    def get_case(self, case_id: str) -> AnalysisCaseDetail | None:
        """Return one case detail, if it exists."""

    @abstractmethod
    def update_case(self, case: AnalysisCaseDetail) -> AnalysisCaseDetail:
        """Legacy test/administrative replacement; never use for business writes."""

    @abstractmethod
    def replace_case_if_revision_matches(
        self, case: AnalysisCaseDetail, expected_revision: int
    ) -> AnalysisCaseDetail | None:
        """Atomically replace an existing case only at its expected revision."""

    @abstractmethod
    def delete_case(self, case_id: str) -> bool:
        """Delete one case and its store-owned auxiliary records."""

    @abstractmethod
    def save_markdown_report(self, case_id: str, report: MarkdownExportResponse) -> MarkdownExportResponse:
        """Persist a rendered Markdown report."""

    @abstractmethod
    def get_markdown_report(self, case_id: str) -> MarkdownExportResponse | None:
        """Return a persisted Markdown report, if available."""

    @abstractmethod
    def list_markdown_reports(self) -> list[MarkdownExportResponse]:
        """Return all persisted Markdown reports."""

    @abstractmethod
    def save_analysis_snapshot(self, case_id: str, snapshot: AnalysisSnapshot) -> AnalysisSnapshot:
        """Persist one monitoring snapshot for a case."""

    @abstractmethod
    def list_analysis_snapshots(self, case_id: str) -> list[AnalysisSnapshot]:
        """Return persisted monitoring snapshots for a case."""

    @abstractmethod
    def save_alert_events(self, case_id: str, alerts: list[AlertEvent]) -> list[AlertEvent]:
        """Persist alert events for a case."""

    @abstractmethod
    def list_case_alerts(self, case_id: str) -> list[AlertEvent]:
        """Return persisted alert events for a case."""

    @abstractmethod
    def list_all_alert_events(self) -> list[AlertEvent]:
        """Return all persisted alert events."""

    @abstractmethod
    def save_notification(self, notification: NotificationOutboxItem) -> NotificationOutboxItem:
        """Persist one notification outbox item."""

    @abstractmethod
    def get_notification(self, notification_id: str) -> NotificationOutboxItem | None:
        """Return one notification outbox item, if available."""

    @abstractmethod
    def update_notification(self, notification: NotificationOutboxItem) -> NotificationOutboxItem | None:
        """Replace an existing notification outbox item."""

    @abstractmethod
    def list_notifications(self) -> list[NotificationOutboxItem]:
        """Return all notification outbox items."""

    @abstractmethod
    def list_case_notifications(self, case_id: str) -> list[NotificationOutboxItem]:
        """Return notification outbox items for one case."""

    @abstractmethod
    def reset(self) -> None:
        """Clear persisted cases for tests or explicit local reset."""
