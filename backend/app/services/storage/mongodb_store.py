from __future__ import annotations

import os
from typing import Any, Protocol

from app.schemas.analysis import AnalysisResultResponse
from app.schemas.alert import AlertEvent, AnalysisSnapshot
from app.schemas.case import AnalysisCaseDetail, MarkdownExportResponse
from app.schemas.common import RiskLevel
from app.schemas.notification import NotificationOutboxItem
from app.schemas.report import PublicOpinionReport
from app.schemas.visualization import VisualizationResponse
from app.services.storage.base_store import CaseStore


DEFAULT_MONGODB_URI = "mongodb://localhost:27017"
DEFAULT_MONGODB_DATABASE = "sentigraph"


class MongoDbStoreConfigError(RuntimeError):
    """Raised when MongoDB store configuration is invalid or unavailable."""


class MongoClientFactory(Protocol):
    def __call__(self, uri: str, **kwargs: Any) -> Any:
        """Create a MongoDB client."""


class MongoDbCaseStore(CaseStore):
    """Optional MongoDB-backed case store.

    The default Sentigraph store remains local JSON. This store is selected only
    when `CASE_STORE_BACKEND=mongodb` and configuration is valid.
    """

    def __init__(
        self,
        *,
        uri: str = DEFAULT_MONGODB_URI,
        database_name: str = DEFAULT_MONGODB_DATABASE,
        client: Any | None = None,
        database: Any | None = None,
        client_factory: MongoClientFactory | None = None,
        verify_connection: bool = True,
    ) -> None:
        if not uri and database is None:
            raise MongoDbStoreConfigError("MONGODB_URI is required when CASE_STORE_BACKEND=mongodb.")
        self.uri = uri
        self.database_name = database_name or DEFAULT_MONGODB_DATABASE
        self._client = client
        self._database = database

        if self._database is None:
            self._client = self._client or _create_mongo_client(uri, client_factory=client_factory)
            if verify_connection:
                try:
                    self._client.admin.command("ping")
                except Exception as exc:  # pragma: no cover - exercised only with real MongoDB connectivity failures.
                    raise MongoDbStoreConfigError(
                        "Unable to connect to MongoDB for CASE_STORE_BACKEND=mongodb. "
                        "Check MONGODB_URI or switch CASE_STORE_BACKEND back to local_json."
                    ) from exc
            self._database = self._client[self.database_name]

        self._cases = self._database["analysis_cases"]
        self._markdown_reports = self._database["markdown_reports"]
        self._snapshots = self._database["analysis_snapshots"]
        self._alerts = self._database["alert_events"]
        self._notifications = self._database["notification_outbox"]
        self._ensure_indexes()

    @classmethod
    def from_env(
        cls,
        *,
        client_factory: MongoClientFactory | None = None,
        verify_connection: bool = True,
    ) -> "MongoDbCaseStore":
        uri = os.getenv("MONGODB_URI", DEFAULT_MONGODB_URI).strip()
        database_name = os.getenv("MONGODB_DATABASE", DEFAULT_MONGODB_DATABASE).strip()
        return cls(
            uri=uri,
            database_name=database_name,
            client_factory=client_factory,
            verify_connection=verify_connection,
        )

    def create_case(self, case: AnalysisCaseDetail) -> AnalysisCaseDetail:
        self._cases.replace_one({"case_id": case.case_id}, _case_to_document(case), upsert=True)
        return case.model_copy(deep=True)

    def list_cases(self) -> list[AnalysisCaseDetail]:
        cases = [AnalysisCaseDetail.model_validate(_strip_mongo_id(item)) for item in self._cases.find({})]
        return sorted(cases, key=lambda item: item.updated_at, reverse=True)

    def get_case(self, case_id: str) -> AnalysisCaseDetail | None:
        raw_case = self._cases.find_one({"case_id": case_id})
        return AnalysisCaseDetail.model_validate(_strip_mongo_id(raw_case)) if raw_case else None

    def update_case(self, case: AnalysisCaseDetail) -> AnalysisCaseDetail:
        if not self.get_case(case.case_id):
            raise KeyError(f"Analysis case '{case.case_id}' does not exist.")
        self._cases.replace_one({"case_id": case.case_id}, _case_to_document(case), upsert=False)
        return case.model_copy(deep=True)

    def save_analysis_result(
        self,
        case_id: str,
        *,
        analysis_result: AnalysisResultResponse,
        visualization_data: VisualizationResponse | None = None,
        risk_score: float | None = None,
        risk_level: RiskLevel | None = None,
        risk_model_version: str | None = None,
        updated_at: Any | None = None,
    ) -> AnalysisCaseDetail | None:
        case = self.get_case(case_id)
        if not case:
            return None
        updated_case = case.model_copy(
            update={
                "analysis_result": analysis_result,
                "visualization_data": visualization_data,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "risk_model_version": risk_model_version,
                "updated_at": updated_at or case.updated_at,
            },
            deep=True,
        )
        return self.update_case(updated_case)

    def save_report(
        self,
        case_id: str,
        *,
        report: PublicOpinionReport,
        updated_at: Any | None = None,
        markdown_available: bool = True,
    ) -> AnalysisCaseDetail | None:
        case = self.get_case(case_id)
        if not case:
            return None
        risk_value = report.overall_risk if report.overall_risk is not None else report.risk_score
        updated_case = case.model_copy(
            update={
                "report": report,
                "markdown_available": markdown_available,
                "risk_score": float(risk_value or 0.0),
                "risk_level": report.risk_level,
                "risk_model_version": report.risk_model_version,
                "updated_at": updated_at or case.updated_at,
            },
            deep=True,
        )
        return self.update_case(updated_case)

    def save_markdown_report(self, case_id: str, report: MarkdownExportResponse) -> MarkdownExportResponse:
        self._markdown_reports.replace_one(
            {"case_id": case_id},
            _safe_document(report.model_dump(mode="json")),
            upsert=True,
        )
        return report.model_copy(deep=True)

    def get_markdown_report(self, case_id: str) -> MarkdownExportResponse | None:
        raw_report = self._markdown_reports.find_one({"case_id": case_id})
        return MarkdownExportResponse.model_validate(_strip_mongo_id(raw_report)) if raw_report else None

    def list_markdown_reports(self) -> list[MarkdownExportResponse]:
        reports = [
            MarkdownExportResponse.model_validate(_strip_mongo_id(item))
            for item in self._markdown_reports.find({})
        ]
        return sorted(reports, key=lambda item: item.generated_at, reverse=True)

    def save_analysis_snapshot(self, case_id: str, snapshot: AnalysisSnapshot) -> AnalysisSnapshot:
        self._snapshots.replace_one(
            {"snapshot_id": snapshot.snapshot_id},
            _safe_document(snapshot.model_dump(mode="json")),
            upsert=True,
        )
        return snapshot.model_copy(deep=True)

    def list_analysis_snapshots(self, case_id: str) -> list[AnalysisSnapshot]:
        snapshots = [
            AnalysisSnapshot.model_validate(_strip_mongo_id(item))
            for item in self._snapshots.find({"case_id": case_id})
        ]
        return sorted(snapshots, key=lambda snapshot: snapshot.created_at)

    def save_alert_events(self, case_id: str, alerts: list[AlertEvent]) -> list[AlertEvent]:
        for alert in alerts:
            self._alerts.replace_one(
                {"alert_id": alert.alert_id},
                _safe_document(alert.model_dump(mode="json")),
                upsert=True,
            )
        return [alert.model_copy(deep=True) for alert in alerts]

    def list_case_alerts(self, case_id: str) -> list[AlertEvent]:
        alerts = [
            AlertEvent.model_validate(_strip_mongo_id(item))
            for item in self._alerts.find({"case_id": case_id})
        ]
        return sorted(alerts, key=lambda alert: alert.created_at)

    def list_all_alert_events(self) -> list[AlertEvent]:
        alerts = [AlertEvent.model_validate(_strip_mongo_id(item)) for item in self._alerts.find({})]
        return sorted(alerts, key=lambda alert: alert.created_at, reverse=True)

    def save_notification(self, notification: NotificationOutboxItem) -> NotificationOutboxItem:
        self._notifications.replace_one(
            {"notification_id": notification.notification_id},
            _safe_document(notification.model_dump(mode="json")),
            upsert=True,
        )
        return notification.model_copy(deep=True)

    def get_notification(self, notification_id: str) -> NotificationOutboxItem | None:
        raw_notification = self._notifications.find_one({"notification_id": notification_id})
        return NotificationOutboxItem.model_validate(_strip_mongo_id(raw_notification)) if raw_notification else None

    def update_notification(self, notification: NotificationOutboxItem) -> NotificationOutboxItem | None:
        if not self.get_notification(notification.notification_id):
            return None
        self._notifications.replace_one(
            {"notification_id": notification.notification_id},
            _safe_document(notification.model_dump(mode="json")),
            upsert=False,
        )
        return notification.model_copy(deep=True)

    def list_notifications(self) -> list[NotificationOutboxItem]:
        notifications = [
            NotificationOutboxItem.model_validate(_strip_mongo_id(item))
            for item in self._notifications.find({})
        ]
        return sorted(notifications, key=lambda item: item.created_at, reverse=True)

    def list_case_notifications(self, case_id: str) -> list[NotificationOutboxItem]:
        notifications = [
            NotificationOutboxItem.model_validate(_strip_mongo_id(item))
            for item in self._notifications.find({"case_id": case_id})
        ]
        return sorted(notifications, key=lambda item: item.created_at, reverse=True)

    def reset(self) -> None:
        for collection in self._collections():
            collection.delete_many({})

    def _collections(self) -> list[Any]:
        return [
            self._cases,
            self._markdown_reports,
            self._snapshots,
            self._alerts,
            self._notifications,
        ]

    def _ensure_indexes(self) -> None:
        self._cases.create_index("case_id", unique=True)
        self._cases.create_index("created_at")
        self._cases.create_index("updated_at")
        self._markdown_reports.create_index("case_id", unique=True)
        self._snapshots.create_index("snapshot_id", unique=True)
        self._snapshots.create_index("case_id")
        self._snapshots.create_index("created_at")
        self._alerts.create_index("alert_id", unique=True)
        self._alerts.create_index("case_id")
        self._alerts.create_index("created_at")
        self._notifications.create_index("notification_id", unique=True)
        self._notifications.create_index("case_id")
        self._notifications.create_index("created_at")
        self._notifications.create_index("status")


def _create_mongo_client(uri: str, *, client_factory: MongoClientFactory | None = None) -> Any:
    if client_factory:
        return client_factory(uri, serverSelectionTimeoutMS=2000)
    try:
        from pymongo import MongoClient
    except ImportError as exc:  # pragma: no cover - depends on optional environment state.
        raise MongoDbStoreConfigError(
            "pymongo is required for CASE_STORE_BACKEND=mongodb. "
            "Install backend requirements or switch CASE_STORE_BACKEND back to local_json."
        ) from exc
    return MongoClient(uri, serverSelectionTimeoutMS=2000)


def _case_to_document(case: AnalysisCaseDetail) -> dict[str, Any]:
    return _safe_document(case.model_dump(mode="json"))


def _safe_document(value: Any) -> Any:
    """Return a MongoDB-safe JSON-like value with string dictionary keys."""

    if isinstance(value, dict):
        return {_safe_key(key): _safe_document(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_safe_document(item) for item in value]
    return value


def _safe_key(key: Any) -> str:
    safe = str(key).replace(".", "_")
    if safe.startswith("$"):
        safe = f"_{safe[1:]}"
    return safe


def _strip_mongo_id(document: dict[str, Any] | None) -> dict[str, Any]:
    if not document:
        return {}
    cleaned = dict(document)
    cleaned.pop("_id", None)
    return cleaned
