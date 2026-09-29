from __future__ import annotations

import json
import os
import uuid
from contextlib import contextmanager
from pathlib import Path
from threading import Lock, RLock
from typing import Any, Iterator, Mapping

if os.name == "nt":
    import msvcrt
else:  # pragma: no cover - the current-host concurrency proof is Windows-only.
    import fcntl

from app.schemas.analysis import AnalysisResultResponse
from app.schemas.alert import AlertEvent, AnalysisSnapshot
from app.schemas.case import AnalysisCaseDetail, MarkdownExportResponse
from app.schemas.common import RiskLevel
from app.schemas.notification import NotificationOutboxItem
from app.schemas.report import PublicOpinionReport
from app.schemas.visualization import VisualizationResponse
from app.services.internal_alpha_live_safe_selected_item_lineage_projection import (
    CONTRACT_ERROR,
    SOURCE_FIELDS,
    LiveSafeLineageAmbiguous,
    LiveSafeLineageContractError,
    LiveSafeLineageUnavailable,
    validate_live_safe_selector,
    validate_live_safe_source,
)
from app.services.storage.base_store import (
    CaseRevisionConflict,
    CaseStore,
    validate_case_revision_precondition,
)


PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CASE_STORE_PATH = PROJECT_ROOT / "backend" / "data" / "cases.json"
_PATH_LOCK_REGISTRY: dict[str, RLock] = {}
_PATH_LOCK_REGISTRY_MUTEX = Lock()


def _canonical_store_key(path: Path) -> str:
    return os.path.normcase(str(path.resolve(strict=False)))


def _path_scoped_lock(path: Path) -> RLock:
    key = _canonical_store_key(path)
    with _PATH_LOCK_REGISTRY_MUTEX:
        if key not in _PATH_LOCK_REGISTRY:
            _PATH_LOCK_REGISTRY[key] = RLock()
        return _PATH_LOCK_REGISTRY[key]


def _lock_file_descriptor(fd: int) -> None:
    os.lseek(fd, 0, os.SEEK_SET)
    if os.name == "nt":
        msvcrt.locking(fd, msvcrt.LK_LOCK, 1)
    else:  # pragma: no cover - POSIX fallback has no F1R3 runtime proof.
        fcntl.lockf(fd, fcntl.LOCK_EX, 1, 0, os.SEEK_SET)


def _unlock_file_descriptor(fd: int) -> None:
    os.lseek(fd, 0, os.SEEK_SET)
    if os.name == "nt":
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
    else:  # pragma: no cover - POSIX fallback has no F1R3 runtime proof.
        fcntl.lockf(fd, fcntl.LOCK_UN, 1, 0, os.SEEK_SET)


class LocalJsonCaseStore(CaseStore):
    """Project-local JSON case store for the mock-first MVP."""

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = _resolve_store_path(path or DEFAULT_CASE_STORE_PATH)
        self._lock = _path_scoped_lock(self.path)

    @classmethod
    def from_env(cls) -> "LocalJsonCaseStore":
        return cls(os.getenv("CASE_STORE_PATH") or DEFAULT_CASE_STORE_PATH)

    def create_case(self, case: AnalysisCaseDetail) -> AnalysisCaseDetail:
        saved_case = case.model_copy(update={"case_revision": 0}, deep=True)
        with self._write_transaction():
            data = self._read_data()
            data["cases"][saved_case.case_id] = _case_to_json(saved_case)
            self._write_data(data)
        return saved_case.model_copy(deep=True)

    def list_cases(self) -> list[AnalysisCaseDetail]:
        with self._lock:
            data = self._read_data()
        return [AnalysisCaseDetail.model_validate(item) for item in data["cases"].values()]

    def get_case(self, case_id: str) -> AnalysisCaseDetail | None:
        with self._lock:
            data = self._read_data()
            raw_case = data["cases"].get(case_id)
        return AnalysisCaseDetail.model_validate(raw_case) if raw_case else None

    def read_exact_live_safe_selected_item_lineage(
        self, case_id: str, evidence_id: str
    ) -> Mapping[str, str | bool]:
        """Read only six attestations for one surviving persisted evidence id.

        The existing whole-file JSON parser runs inside this trusted adapter;
        no full case, evidence item or raw_data_safe mapping leaves this method.
        """
        validate_live_safe_selector(case_id, evidence_id)
        with self._lock:
            data = self._read_data()
            raw_case = data["cases"].get(case_id)
            if raw_case is None:
                raise LiveSafeLineageUnavailable("live_safe_lineage_unavailable")
            if type(raw_case) is not dict or raw_case.get("case_id") != case_id:
                raise LiveSafeLineageContractError(CONTRACT_ERROR)
            evidence_items = raw_case.get("evidence_items")
            if type(evidence_items) is not list:
                raise LiveSafeLineageContractError(CONTRACT_ERROR)

            match = None
            match_count = 0
            for item in evidence_items:
                if type(item) is not dict:
                    raise LiveSafeLineageContractError(CONTRACT_ERROR)
                if item.get("evidence_id") == evidence_id:
                    match_count += 1
                    match = item
            if match_count == 0:
                raise LiveSafeLineageUnavailable("live_safe_lineage_unavailable")
            if match_count != 1:
                raise LiveSafeLineageAmbiguous("live_safe_lineage_ambiguous")
            if match.get("case_id") != case_id:
                raise LiveSafeLineageContractError(CONTRACT_ERROR)
            raw_source = match.get("raw_data_safe")
            if type(raw_source) is not dict:
                raise LiveSafeLineageContractError(CONTRACT_ERROR)
            detached = {field: raw_source.get(field) for field in SOURCE_FIELDS}
            return validate_live_safe_source(detached)

    def update_case(self, case: AnalysisCaseDetail) -> AnalysisCaseDetail:
        with self._write_transaction():
            data = self._read_data()
            if case.case_id not in data["cases"]:
                raise KeyError(f"Analysis case '{case.case_id}' does not exist.")
            data["cases"][case.case_id] = _case_to_json(case)
            self._write_data(data)
        return case.model_copy(deep=True)

    def replace_case_if_revision_matches(
        self, case: AnalysisCaseDetail, expected_revision: int
    ) -> AnalysisCaseDetail | None:
        validate_case_revision_precondition(case, expected_revision)
        with self._write_transaction():
            data = self._read_data()
            raw_case = data["cases"].get(case.case_id)
            if raw_case is None:
                return None
            if not isinstance(raw_case, dict) or raw_case.get("case_id") != case.case_id:
                raise ValueError("persisted case_id does not match requested case_id")
            current_revision = raw_case.get("case_revision", 0)
            if type(current_revision) is not int or current_revision < 0:
                raise ValueError("persisted case_revision must be a nonnegative integer")
            if current_revision != expected_revision:
                raise CaseRevisionConflict(case.case_id, expected_revision, current_revision)
            saved_case = case.model_copy(update={"case_revision": expected_revision + 1}, deep=True)
            data["cases"][case.case_id] = _case_to_json(saved_case)
            self._write_data(data)
        return saved_case.model_copy(deep=True)

    def delete_case(self, case_id: str) -> bool:
        with self._write_transaction():
            data = self._read_data()
            if case_id not in data["cases"]:
                return False

            del data["cases"][case_id]
            for collection_name in ("markdown_reports", "snapshots", "alerts"):
                data[collection_name].pop(case_id, None)
            data["notifications"] = {
                notification_id: notification
                for notification_id, notification in data["notifications"].items()
                if not (isinstance(notification, dict) and notification.get("case_id") == case_id)
            }
            self._write_data(data)
        return True

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
        updated_case = case.model_copy(
            update={
                "report": report,
                "markdown_available": markdown_available,
                "risk_score": float(report.overall_risk if report.overall_risk is not None else report.risk_score),
                "risk_level": report.risk_level,
                "risk_model_version": report.risk_model_version,
                "updated_at": updated_at or case.updated_at,
            },
            deep=True,
        )
        return self.update_case(updated_case)

    def save_markdown_report(self, case_id: str, report: MarkdownExportResponse) -> MarkdownExportResponse:
        with self._write_transaction():
            data = self._read_data()
            data["markdown_reports"][case_id] = report.model_dump(mode="json")
            self._write_data(data)
        return report.model_copy(deep=True)

    def get_markdown_report(self, case_id: str) -> MarkdownExportResponse | None:
        with self._lock:
            data = self._read_data()
            raw_report = data["markdown_reports"].get(case_id)
        return MarkdownExportResponse.model_validate(raw_report) if raw_report else None

    def list_markdown_reports(self) -> list[MarkdownExportResponse]:
        with self._lock:
            data = self._read_data()
        return [MarkdownExportResponse.model_validate(item) for item in data["markdown_reports"].values()]

    def save_analysis_snapshot(self, case_id: str, snapshot: AnalysisSnapshot) -> AnalysisSnapshot:
        with self._write_transaction():
            data = self._read_data()
            data["snapshots"].setdefault(case_id, [])
            data["snapshots"][case_id].append(snapshot.model_dump(mode="json"))
            self._write_data(data)
        return snapshot.model_copy(deep=True)

    def list_analysis_snapshots(self, case_id: str) -> list[AnalysisSnapshot]:
        with self._lock:
            data = self._read_data()
            raw_snapshots = data["snapshots"].get(case_id, [])
        snapshots = [AnalysisSnapshot.model_validate(item) for item in raw_snapshots]
        return sorted(snapshots, key=lambda snapshot: snapshot.created_at)

    def save_alert_events(self, case_id: str, alerts: list[AlertEvent]) -> list[AlertEvent]:
        if not alerts:
            return []
        with self._write_transaction():
            data = self._read_data()
            data["alerts"].setdefault(case_id, [])
            data["alerts"][case_id].extend(alert.model_dump(mode="json") for alert in alerts)
            self._write_data(data)
        return [alert.model_copy(deep=True) for alert in alerts]

    def list_case_alerts(self, case_id: str) -> list[AlertEvent]:
        with self._lock:
            data = self._read_data()
            raw_alerts = data["alerts"].get(case_id, [])
        alerts = [AlertEvent.model_validate(item) for item in raw_alerts]
        return sorted(alerts, key=lambda alert: alert.created_at)

    def list_all_alert_events(self) -> list[AlertEvent]:
        with self._lock:
            data = self._read_data()
            raw_alert_groups = data["alerts"].values()
        alerts = [
            AlertEvent.model_validate(item)
            for raw_alerts in raw_alert_groups
            for item in raw_alerts
        ]
        return sorted(alerts, key=lambda alert: alert.created_at, reverse=True)

    def save_notification(self, notification: NotificationOutboxItem) -> NotificationOutboxItem:
        with self._write_transaction():
            data = self._read_data()
            data["notifications"][notification.notification_id] = notification.model_dump(mode="json")
            self._write_data(data)
        return notification.model_copy(deep=True)

    def get_notification(self, notification_id: str) -> NotificationOutboxItem | None:
        with self._lock:
            data = self._read_data()
            raw_notification = data["notifications"].get(notification_id)
        return NotificationOutboxItem.model_validate(raw_notification) if raw_notification else None

    def update_notification(self, notification: NotificationOutboxItem) -> NotificationOutboxItem | None:
        with self._write_transaction():
            data = self._read_data()
            if notification.notification_id not in data["notifications"]:
                return None
            data["notifications"][notification.notification_id] = notification.model_dump(mode="json")
            self._write_data(data)
        return notification.model_copy(deep=True)

    def list_notifications(self) -> list[NotificationOutboxItem]:
        with self._lock:
            data = self._read_data()
            raw_notifications = data["notifications"].values()
        notifications = [NotificationOutboxItem.model_validate(item) for item in raw_notifications]
        return sorted(notifications, key=lambda item: item.created_at, reverse=True)

    def list_case_notifications(self, case_id: str) -> list[NotificationOutboxItem]:
        notifications = [item for item in self.list_notifications() if item.case_id == case_id]
        return sorted(notifications, key=lambda item: item.created_at, reverse=True)

    def reset(self) -> None:
        with self._write_transaction():
            if self.path.exists():
                self.path.unlink()

    @contextmanager
    def _write_transaction(self) -> Iterator[None]:
        """Serialize one complete JSON mutation across local instances/processes."""
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            lock_path = self.path.with_name(self.path.name + ".lock")
            fd = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
            try:
                if os.fstat(fd).st_size < 1:
                    os.lseek(fd, 0, os.SEEK_SET)
                    os.write(fd, b"0")
                    os.fsync(fd)
                _lock_file_descriptor(fd)
                try:
                    yield
                finally:
                    _unlock_file_descriptor(fd)
            finally:
                os.close(fd)

    def _read_data(self) -> dict[str, Any]:
        if not self.path.exists():
            return _empty_data()
        with self.path.open("r", encoding="utf-8") as file:
            raw = json.load(file)
        if not isinstance(raw, dict):
            return _empty_data()
        cases = raw.get("cases")
        markdown_reports = raw.get("markdown_reports")
        snapshots = raw.get("snapshots")
        alerts = raw.get("alerts")
        notifications = raw.get("notifications")
        return {
            "cases": cases if isinstance(cases, dict) else {},
            "markdown_reports": markdown_reports if isinstance(markdown_reports, dict) else {},
            "snapshots": snapshots if isinstance(snapshots, dict) else {},
            "alerts": alerts if isinstance(alerts, dict) else {},
            "notifications": notifications if isinstance(notifications, dict) else {},
        }

    def _write_data(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.path.with_name(f"{self.path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
        try:
            with tmp_path.open("x", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2, sort_keys=True)
                file.write("\n")
                file.flush()
                os.fsync(file.fileno())
            os.replace(tmp_path, self.path)
        finally:
            tmp_path.unlink(missing_ok=True)


def _empty_data() -> dict[str, Any]:
    return {"cases": {}, "markdown_reports": {}, "snapshots": {}, "alerts": {}, "notifications": {}}


def _case_to_json(case: AnalysisCaseDetail) -> dict[str, Any]:
    return case.model_dump(mode="json")


def _resolve_store_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return PROJECT_ROOT / candidate
