"""Pure analysis-lineage classification for persisted auxiliary artifacts."""

from __future__ import annotations

from app.schemas.alert import AlertEvent, AnalysisSnapshot, AuxiliaryLineageStatus
from app.schemas.case import AnalysisCaseDetail
from app.schemas.notification import NotificationOutboxItem


class AuxiliaryLineageStale(RuntimeError):
    """A known artifact cannot be used as a current-analysis operation."""

    def __init__(self, case_id: str, artifact_type: str, artifact_id: str | None = None) -> None:
        self.case_id = case_id
        self.artifact_type = artifact_type
        self.artifact_id = artifact_id
        super().__init__("case_auxiliary_lineage_stale")


class AuxiliaryGuardUnavailable(RuntimeError):
    """The store cannot atomically guard an auxiliary action."""


class AuxiliaryIdentityConflict(RuntimeError):
    """An immutable auxiliary ID or monotonic publication guard conflicted."""

    def __init__(self, case_id: str, artifact_type: str, artifact_id: str | None = None) -> None:
        self.case_id = case_id
        self.artifact_type = artifact_type
        self.artifact_id = artifact_id
        super().__init__("case_auxiliary_identity_conflict")


def current_case_pair(case: AnalysisCaseDetail | None) -> tuple[int, str] | None:
    """Return the completed case's analysis pair, never its case-CAS revision."""
    if case is None or case.status != "completed":
        return None
    if case.analysis_revision is None or case.analysis_run_id is None:
        return None
    return case.analysis_revision, case.analysis_run_id


def classify_source_pair(
    case: AnalysisCaseDetail | None,
    source_analysis_revision: int | None,
    source_analysis_run_id: str | None,
) -> AuxiliaryLineageStatus:
    if case is None or source_analysis_revision is None or source_analysis_run_id is None:
        return "UNBOUND_LEGACY"
    return (
        "CURRENT"
        if current_case_pair(case) == (source_analysis_revision, source_analysis_run_id)
        else "HISTORICAL"
    )


def classify_snapshot(
    case: AnalysisCaseDetail | None, snapshot: AnalysisSnapshot | None
) -> AuxiliaryLineageStatus:
    if case is None or snapshot is None or snapshot.case_id != case.case_id:
        return "UNBOUND_LEGACY"
    return classify_source_pair(case, snapshot.source_analysis_revision, snapshot.source_analysis_run_id)


def classify_alert(
    case: AnalysisCaseDetail | None, alert: AlertEvent | None, snapshot: AnalysisSnapshot | None
) -> AuxiliaryLineageStatus:
    if (
        case is None or alert is None or snapshot is None
        or alert.case_id != case.case_id or snapshot.case_id != alert.case_id
        or alert.snapshot_id != snapshot.snapshot_id
    ):
        return "UNBOUND_LEGACY"
    return classify_snapshot(case, snapshot)


def classify_notification(
    case: AnalysisCaseDetail | None,
    notification: NotificationOutboxItem | None,
    alert: AlertEvent | None,
    snapshot: AnalysisSnapshot | None,
) -> AuxiliaryLineageStatus:
    if (
        case is None or notification is None or alert is None
        or notification.case_id != case.case_id or notification.alert_id != alert.alert_id
        or alert.case_id != notification.case_id
    ):
        return "UNBOUND_LEGACY"
    return classify_alert(case, alert, snapshot)
