from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Protocol

from pymongo.errors import DuplicateKeyError

from app.schemas.alert import AlertEvent, AnalysisSnapshot
from app.schemas.case import AnalysisCaseDetail, MarkdownExportResponse
from app.schemas.notification import NotificationOutboxItem
from app.services.monitoring.analysis_lineage_currentness import (
    AuxiliaryGuardUnavailable,
    AuxiliaryIdentityConflict,
    AuxiliaryLineageStale,
    classify_notification,
)
from app.services.storage.base_store import (
    CaseRevisionConflict,
    CaseStore,
    validate_case_revision_precondition,
)


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
        saved_case = case.model_copy(update={"case_revision": 0}, deep=True)
        self._cases.replace_one({"case_id": saved_case.case_id}, _case_to_document(saved_case), upsert=True)
        return saved_case.model_copy(deep=True)

    def list_cases(self) -> list[AnalysisCaseDetail]:
        cases = [AnalysisCaseDetail.model_validate(_strip_mongo_id(item)) for item in self._cases.find({})]
        return sorted(cases, key=lambda item: item.updated_at, reverse=True)

    def get_case(self, case_id: str) -> AnalysisCaseDetail | None:
        raw_case = self._cases.find_one({"case_id": case_id})
        return AnalysisCaseDetail.model_validate(_strip_mongo_id(raw_case)) if raw_case else None

    def update_case(self, case: AnalysisCaseDetail) -> AnalysisCaseDetail:
        """Legacy test/administrative replacement; business writers use CAS."""
        if not self.get_case(case.case_id):
            raise KeyError(f"Analysis case '{case.case_id}' does not exist.")
        self._cases.replace_one({"case_id": case.case_id}, _case_to_document(case), upsert=False)
        return case.model_copy(deep=True)

    def replace_case_if_revision_matches(
        self, case: AnalysisCaseDetail, expected_revision: int
    ) -> AnalysisCaseDetail | None:
        validate_case_revision_precondition(case, expected_revision)
        revision_filter: dict[str, Any]
        if expected_revision == 0:
            revision_filter = {
                "case_id": case.case_id,
                "$or": [
                    {"case_revision": {"$exists": False}},
                    {"case_revision": 0},
                ],
            }
        else:
            revision_filter = {"case_id": case.case_id, "case_revision": expected_revision}
        saved_case = case.model_copy(update={"case_revision": expected_revision + 1}, deep=True)
        result = self._cases.replace_one(revision_filter, _case_to_document(saved_case), upsert=False)
        if result.matched_count == 1:
            return saved_case.model_copy(deep=True)
        if result.matched_count != 0:
            raise RuntimeError("case_revision_cas_unexpected_match_count")
        # This read classifies a failed conditional write; it never authorizes replay.
        persisted = self._cases.find_one({"case_id": case.case_id})
        if persisted is None:
            return None
        current_revision = persisted.get("case_revision", 0)
        if type(current_revision) is not int or current_revision < 0:
            current_revision = None
        raise CaseRevisionConflict(case.case_id, expected_revision, current_revision)

    def delete_case(self, case_id: str) -> bool:
        if not self.get_case(case_id):
            return False
        for collection in (
            self._cases,
            self._markdown_reports,
            self._snapshots,
            self._alerts,
            self._notifications,
        ):
            collection.delete_many({"case_id": case_id})
        return True

    def save_markdown_report(self, case_id: str, report: MarkdownExportResponse) -> MarkdownExportResponse:
        if report.case_id != case_id:
            raise AuxiliaryIdentityConflict(case_id, "markdown")
        if (report.source_analysis_revision is None) != (report.source_analysis_run_id is None):
            raise AuxiliaryIdentityConflict(case_id, "markdown")
        incoming = _safe_document(report.model_dump(mode="json"))
        existing = self._markdown_reports.find_one({"case_id": case_id})
        if existing is None:
            try:
                self._markdown_reports.insert_one(incoming)
            except DuplicateKeyError as exc:
                raise AuxiliaryIdentityConflict(case_id, "markdown") from exc
            return report.model_copy(deep=True)
        persisted = MarkdownExportResponse.model_validate(_strip_mongo_id(existing))
        old_revision = persisted.source_analysis_revision
        new_revision = report.source_analysis_revision
        if old_revision is not None:
            if new_revision is None or new_revision < old_revision:
                raise AuxiliaryIdentityConflict(case_id, "markdown")
            if new_revision == old_revision:
                if persisted.source_analysis_run_id != report.source_analysis_run_id:
                    raise AuxiliaryIdentityConflict(case_id, "markdown")
                return persisted
        guard: dict[str, Any] = {"case_id": case_id}
        for field in ("source_analysis_revision", "source_analysis_run_id"):
            guard[field] = existing[field] if field in existing else {"$exists": False}
        replaced = self._markdown_reports.replace_one(guard, incoming, upsert=False)
        if replaced.matched_count != 1:
            raise AuxiliaryIdentityConflict(case_id, "markdown")
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
        if snapshot.case_id != case_id:
            raise AuxiliaryIdentityConflict(case_id, "snapshot", snapshot.snapshot_id)
        try:
            self._snapshots.insert_one(_safe_document(snapshot.model_dump(mode="json")))
        except DuplicateKeyError as exc:
            raise AuxiliaryIdentityConflict(case_id, "snapshot", snapshot.snapshot_id) from exc
        return snapshot.model_copy(deep=True)

    def list_analysis_snapshots(self, case_id: str) -> list[AnalysisSnapshot]:
        snapshots = [
            AnalysisSnapshot.model_validate(_strip_mongo_id(item))
            for item in self._snapshots.find({"case_id": case_id})
        ]
        return sorted(snapshots, key=lambda snapshot: snapshot.created_at)

    def get_analysis_snapshot(self, snapshot_id: str) -> AnalysisSnapshot | None:
        raw = self._snapshots.find_one({"snapshot_id": snapshot_id})
        return AnalysisSnapshot.model_validate(_strip_mongo_id(raw)) if raw else None

    def save_alert_events(self, case_id: str, alerts: list[AlertEvent]) -> list[AlertEvent]:
        for alert in alerts:
            if alert.case_id != case_id:
                raise AuxiliaryIdentityConflict(case_id, "alert", alert.alert_id)
            raw = _safe_document(alert.model_dump(mode="json"))
            existing = self._alerts.find_one({"alert_id": alert.alert_id})
            if existing is not None:
                if _strip_mongo_id(existing) != raw:
                    raise AuxiliaryIdentityConflict(case_id, "alert", alert.alert_id)
                continue
            try:
                self._alerts.insert_one(raw)
            except DuplicateKeyError as exc:
                raise AuxiliaryIdentityConflict(case_id, "alert", alert.alert_id) from exc
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

    def get_alert_event(self, alert_id: str) -> AlertEvent | None:
        raw = self._alerts.find_one({"alert_id": alert_id})
        return AlertEvent.model_validate(_strip_mongo_id(raw)) if raw else None

    def save_notification(self, notification: NotificationOutboxItem) -> NotificationOutboxItem:
        raw = _safe_document(notification.model_dump(mode="json"))
        existing = self._notifications.find_one({"notification_id": notification.notification_id})
        if existing is not None:
            if _strip_mongo_id(existing) != raw:
                raise AuxiliaryIdentityConflict(
                    notification.case_id, "notification", notification.notification_id
                )
            return NotificationOutboxItem.model_validate(_strip_mongo_id(existing))
        try:
            self._notifications.insert_one(raw)
        except DuplicateKeyError as exc:
            raise AuxiliaryIdentityConflict(
                notification.case_id, "notification", notification.notification_id
            ) from exc
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

    def mutate_notification_if_current(
        self, notification_id: str, action: str, at: datetime
    ) -> NotificationOutboxItem | None:
        if action not in {"mark_read", "simulate_send"}:
            raise ValueError("Unsupported notification action")
        if self._client is None or not callable(getattr(self._client, "start_session", None)):
            raise AuxiliaryGuardUnavailable("case_auxiliary_guard_unavailable")
        try:
            with self._client.start_session() as session:
                with session.start_transaction():
                    raw = self._notifications.find_one({"notification_id": notification_id}, session=session)
                    if raw is None:
                        return None
                    notification = NotificationOutboxItem.model_validate(_strip_mongo_id(raw))
                    raw_alert = self._alerts.find_one({"alert_id": notification.alert_id}, session=session)
                    alert = AlertEvent.model_validate(_strip_mongo_id(raw_alert)) if raw_alert else None
                    raw_snapshot = (
                        self._snapshots.find_one({"snapshot_id": alert.snapshot_id}, session=session)
                        if alert else None
                    )
                    snapshot = AnalysisSnapshot.model_validate(_strip_mongo_id(raw_snapshot)) if raw_snapshot else None
                    raw_case = self._cases.find_one({"case_id": notification.case_id}, session=session)
                    case = AnalysisCaseDetail.model_validate(_strip_mongo_id(raw_case)) if raw_case else None
                    if classify_notification(case, notification, alert, snapshot) != "CURRENT":
                        raise AuxiliaryLineageStale(notification.case_id, "notification", notification_id)
                    if action == "mark_read" and notification.read_at is None:
                        updated = notification.model_copy(update={"read_at": at}, deep=True)
                    elif action == "simulate_send" and notification.status != "simulated_sent":
                        updated = notification.model_copy(
                            update={"status": "simulated_sent", "simulated_sent_at": at}, deep=True
                        )
                    else:
                        return notification
                    # Touch the case in the same transaction to force a write conflict
                    # with any concurrent case invalidation; a read alone permits write skew.
                    fenced = self._cases.update_one(
                        {
                            "case_id": notification.case_id,
                            "status": "completed",
                            "case_revision": case.case_revision,
                            "analysis_revision": case.analysis_revision,
                            "analysis_run_id": case.analysis_run_id,
                        },
                        {"$inc": {"auxiliary_action_guard_counter": 1}},
                        session=session,
                    )
                    if fenced.matched_count != 1:
                        raise AuxiliaryLineageStale(notification.case_id, "notification", notification_id)
                    replaced = self._notifications.replace_one(
                        {"notification_id": notification_id},
                        _safe_document(updated.model_dump(mode="json")),
                        upsert=False,
                        session=session,
                    )
                    if replaced.matched_count != 1:
                        raise AuxiliaryIdentityConflict(notification.case_id, "notification", notification_id)
                    return updated
        except (AuxiliaryLineageStale, AuxiliaryIdentityConflict):
            raise
        except Exception as exc:
            raise AuxiliaryGuardUnavailable("case_auxiliary_guard_unavailable") from exc

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
