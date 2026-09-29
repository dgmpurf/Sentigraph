"""Offline proof of analysis-bound auxiliary history and guarded actions."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.case_repository import CaseRepository, analysis_invalidation_update
from app.schemas.case import AnalysisCaseCreateRequest
from app.services.case_store import configure_case_repository, run_monitoring_check
from app.services.monitoring.analysis_lineage_currentness import (
    AuxiliaryGuardUnavailable,
    AuxiliaryIdentityConflict,
    AuxiliaryLineageStale,
    classify_alert,
    classify_notification,
    classify_snapshot,
    classify_source_pair,
)
from app.services.storage.local_json_store import LocalJsonCaseStore
from app.services.storage.mongodb_store import MongoDbCaseStore
from app.tests.test_mongodb_case_store import FakeMongoClient


client = TestClient(app)


@pytest.fixture(autouse=True)
def isolated_store(tmp_path):
    repository = CaseRepository(LocalJsonCaseStore(tmp_path / "cases.json"))
    configure_case_repository(repository)
    return repository


def _run_case(repository: CaseRepository):
    case = repository.create_case(AnalysisCaseCreateRequest(keyword="Synthetic lineage fixture", platforms=["reddit"]))
    response = client.post(f"/api/v1/cases/{case.case_id}/run")
    assert response.status_code == 200
    return repository.get_case(case.case_id)


def _invalidate(repository: CaseRepository, case_id: str):
    case = repository.get_case(case_id)
    return repository.replace_case_if_revision_matches(
        case.model_copy(update=analysis_invalidation_update(), deep=True), case.case_revision
    )


def _mongo_repository() -> CaseRepository:
    fake_client = FakeMongoClient()
    database = fake_client["sentigraph_test"]
    return CaseRepository(MongoDbCaseStore(client=fake_client, database=database))


def test_direct_tristate_and_case_revision_only_bump(isolated_store) -> None:
    repository = isolated_store
    case = _run_case(repository)
    snapshot = repository.list_analysis_snapshots(case.case_id)[0]
    assert classify_snapshot(case, snapshot) == "CURRENT"
    assert classify_source_pair(case, None, None) == "UNBOUND_LEGACY"
    assert classify_source_pair(case, case.analysis_revision - 1, "old_run") == "HISTORICAL"

    bumped = repository.replace_case_if_revision_matches(case, case.case_revision)
    assert bumped.case_revision > case.case_revision
    assert classify_snapshot(bumped, snapshot) == "CURRENT"

    _invalidate(repository, case.case_id)
    assert classify_snapshot(repository.get_case(case.case_id), snapshot) == "HISTORICAL"


def test_markdown_current_rebuild_and_old_slot_guard(isolated_store) -> None:
    repository = isolated_store
    case = _run_case(repository)
    current = repository.get_markdown_report(case.case_id)
    response = client.get(f"/api/v1/cases/{case.case_id}/report/markdown")
    assert response.status_code == 200
    assert response.json()["source_analysis_run_id"] == case.analysis_run_id
    assert current.source_analysis_revision == case.analysis_revision
    with pytest.raises(AuxiliaryIdentityConflict):
        repository.save_markdown_report(
            case.case_id, current.model_copy(update={"source_analysis_run_id": None})
        )

    higher = current.model_copy(update={
        "source_analysis_revision": current.source_analysis_revision + 9,
        "source_analysis_run_id": "higher_run",
    })
    repository.save_markdown_report(case.case_id, higher)
    with pytest.raises(AuxiliaryIdentityConflict):
        repository.save_markdown_report(case.case_id, current)
    assert repository.get_markdown_report(case.case_id).source_analysis_run_id == "higher_run"


def test_markdown_guard_mongo_fake_matches_local(isolated_store) -> None:
    local = isolated_store
    case = _run_case(local)
    report = local.get_markdown_report(case.case_id)
    mongo = _mongo_repository()
    mongo.save_markdown_report(case.case_id, report)
    with pytest.raises(AuxiliaryIdentityConflict):
        mongo.save_markdown_report(
            case.case_id, report.model_copy(update={"source_analysis_revision": None})
        )
    higher = report.model_copy(update={
        "source_analysis_revision": report.source_analysis_revision + 1,
        "source_analysis_run_id": "newer",
    })
    mongo.save_markdown_report(case.case_id, higher)
    with pytest.raises(AuxiliaryIdentityConflict):
        mongo.save_markdown_report(case.case_id, report)
    assert mongo.get_markdown_report(case.case_id).source_analysis_run_id == "newer"


def test_markdown_invalidation_and_legacy_slot_rebuild(isolated_store) -> None:
    repository = isolated_store
    case = _run_case(repository)
    original = repository.get_markdown_report(case.case_id)
    _invalidate(repository, case.case_id)
    assert client.get(f"/api/v1/cases/{case.case_id}/report/markdown").status_code == 404
    assert repository.get_markdown_report(case.case_id) == original

    assert client.post(f"/api/v1/cases/{case.case_id}/run").status_code == 200
    fresh_case = repository.get_case(case.case_id)
    fresh = client.get(f"/api/v1/cases/{case.case_id}/report/markdown").json()
    assert fresh["source_analysis_run_id"] == fresh_case.analysis_run_id
    assert fresh["source_analysis_run_id"] != original.source_analysis_run_id

    store = repository.store
    with store._write_transaction():
        data = store._read_data()
        data["markdown_reports"][case.case_id].pop("source_analysis_revision")
        data["markdown_reports"][case.case_id].pop("source_analysis_run_id")
        store._write_data(data)
    rebuilt = client.get(f"/api/v1/cases/{case.case_id}/report/markdown")
    assert rebuilt.status_code == 200
    assert rebuilt.json()["source_analysis_run_id"] == fresh_case.analysis_run_id


def test_monitor_concurrent_unique_snapshots_and_history_views(isolated_store) -> None:
    repository = isolated_store
    case = _run_case(repository)
    with ThreadPoolExecutor(max_workers=2) as pool:
        statuses = list(pool.map(lambda _: run_monitoring_check(case.case_id), range(2)))
    assert all(status is not None for status in statuses)
    snapshots = repository.list_analysis_snapshots(case.case_id)
    assert len({snapshot.snapshot_id for snapshot in snapshots}) == 3
    assert all(snapshot.source_analysis_run_id == case.analysis_run_id for snapshot in snapshots)
    with pytest.raises(AuxiliaryIdentityConflict):
        repository.save_analysis_snapshot(case.case_id, snapshots[0])

    before = client.get(f"/api/v1/cases/{case.case_id}/snapshots").json()
    assert {item["lineage_status"] for item in before} == {"CURRENT"}
    _invalidate(repository, case.case_id)
    after = client.get(f"/api/v1/cases/{case.case_id}/snapshots").json()
    assert {item["lineage_status"] for item in after} == {"HISTORICAL"}


def test_alert_notification_parent_chain_and_stale_actions(isolated_store) -> None:
    repository = isolated_store
    case = _run_case(repository)
    status = run_monitoring_check(case.case_id)
    assert status.alerts
    alert = status.alerts[0]
    notification = repository.list_case_notifications(case.case_id)[0]
    snapshot = repository.get_analysis_snapshot(alert.snapshot_id)
    assert classify_alert(case, alert, snapshot) == "CURRENT"
    assert classify_notification(case, notification, alert, snapshot) == "CURRENT"
    assert classify_notification(case, notification, None, snapshot) == "UNBOUND_LEGACY"
    assert client.get(f"/api/v1/cases/{case.case_id}/notifications").json()[0]["lineage_status"] == "CURRENT"
    orphan = notification.model_copy(update={
        "notification_id": "orphan_notification",
        "alert_id": "missing_alert",
        "metadata": {"snapshot_id": snapshot.snapshot_id},
    }, deep=True)
    repository.save_notification(orphan)
    assert repository.classify_notification_item(orphan) == "UNBOUND_LEGACY"
    assert client.post(f"/api/v1/notifications/{orphan.notification_id}/read").status_code == 409
    assert repository.get_notification(orphan.notification_id).read_at is None

    _invalidate(repository, case.case_id)
    for suffix in ("read", "simulate-send"):
        response = client.post(f"/api/v1/notifications/{notification.notification_id}/{suffix}")
        assert response.status_code == 409
        assert response.json()["detail"]["error"] == "case_auxiliary_lineage_stale"
    assert repository.get_notification(notification.notification_id).read_at is None
    assert repository.get_notification(notification.notification_id).status == "pending"
    outbox = client.get("/api/v1/notifications/outbox/status").json()
    assert outbox["pending"] >= 1
    assert outbox["current_pending"] == 0
    assert outbox["historical_or_unbound_total"] >= 1
    assert outbox["total"] == outbox["current_total"] + outbox["historical_or_unbound_total"]
    assert {item["lineage_status"] for item in client.get(f"/api/v1/cases/{case.case_id}/alerts").json()} == {"HISTORICAL"}
    assert client.post("/api/v1/notifications/simulate-send-pending").json() == []


def test_mongo_transaction_guard_current_stale_and_unavailable(isolated_store) -> None:
    local = isolated_store
    case = _run_case(local)
    status = run_monitoring_check(case.case_id)
    alert = status.alerts[0]
    notification = local.list_case_notifications(case.case_id)[0]

    mongo = _mongo_repository()
    mongo.store.create_case(case)
    mongo.save_analysis_snapshot(case.case_id, local.get_analysis_snapshot(alert.snapshot_id))
    mongo.save_alert_events(case.case_id, [alert])
    mongo.save_notification(notification)
    with pytest.raises(AuxiliaryIdentityConflict):
        mongo.save_analysis_snapshot(case.case_id, local.get_analysis_snapshot(alert.snapshot_id))
    changed = mongo.mutate_notification_if_current(notification.notification_id, "mark_read", mongo.next_timestamp())
    assert changed.read_at is not None
    assert mongo.store._cases.find_one({"case_id": case.case_id})["auxiliary_action_guard_counter"] == 1
    orphan = notification.model_copy(update={
        "notification_id": "mongo_orphan_notification",
        "alert_id": "missing_alert",
        "metadata": {"snapshot_id": alert.snapshot_id},
    }, deep=True)
    mongo.save_notification(orphan)
    with pytest.raises(AuxiliaryLineageStale):
        mongo.mutate_notification_if_current(orphan.notification_id, "mark_read", mongo.next_timestamp())
    assert mongo.get_notification(orphan.notification_id).read_at is None
    assert mongo.store._cases.find_one({"case_id": case.case_id})["auxiliary_action_guard_counter"] == 1

    _invalidate(mongo, case.case_id)
    with pytest.raises(AuxiliaryLineageStale):
        mongo.mutate_notification_if_current(notification.notification_id, "simulate_send", mongo.next_timestamp())
    assert mongo.get_notification(notification.notification_id).status == "pending"

    no_session = MongoDbCaseStore(database=mongo.store._database)
    with pytest.raises(AuxiliaryGuardUnavailable):
        no_session.mutate_notification_if_current(notification.notification_id, "simulate_send", mongo.next_timestamp())


def test_forecast_and_simulation_use_new_pair_only(isolated_store) -> None:
    repository = isolated_store
    case = _run_case(repository)
    run_monitoring_check(case.case_id)
    old = repository.list_analysis_snapshots(case.case_id)
    _invalidate(repository, case.case_id)
    assert client.post(f"/api/v1/cases/{case.case_id}/run").status_code == 200
    current = repository.get_case(case.case_id)
    forecast = client.get(f"/api/v1/cases/{case.case_id}/forecast")
    assert forecast.status_code == 200
    assert forecast.json()["snapshot_count"] == 1
    assert forecast.json()["source_analysis_run_id"] == current.analysis_run_id
    assert all(item["source_analysis_run_id"] == current.analysis_run_id for item in forecast.json()["input_snapshots"])
    assert all(classify_snapshot(current, snapshot) == "HISTORICAL" for snapshot in old)

    simulation = client.get(f"/api/v1/cases/{case.case_id}/simulation/initialization-preview")
    assert simulation.status_code == 200
    assert simulation.json()["event_frame"]["observed_frame_profile"]["snapshot_count"] == 1


def test_legacy_unbound_snapshot_loads_but_never_current(isolated_store) -> None:
    repository = isolated_store
    case = _run_case(repository)
    current = repository.list_analysis_snapshots(case.case_id)[0]
    legacy = current.model_copy(update={
        "snapshot_id": "legacy_snapshot",
        "source_analysis_revision": None,
        "source_analysis_run_id": None,
    })
    repository.save_analysis_snapshot(case.case_id, legacy)
    assert classify_snapshot(case, legacy) == "UNBOUND_LEGACY"
    views = client.get(f"/api/v1/cases/{case.case_id}/snapshots").json()
    assert any(item["snapshot_id"] == "legacy_snapshot" and item["lineage_status"] == "UNBOUND_LEGACY" for item in views)
    forecast = client.get(f"/api/v1/cases/{case.case_id}/forecast").json()
    assert forecast["snapshot_count"] == 1


def test_monitor_invalidation_after_snapshot_stops_alert_and_notification(isolated_store, monkeypatch) -> None:
    repository = isolated_store
    case = _run_case(repository)
    original_save = repository.save_analysis_snapshot
    before_alerts = repository.list_case_alerts(case.case_id)
    before_notifications = repository.list_case_notifications(case.case_id)

    def save_then_invalidate(case_id, snapshot):
        saved = original_save(case_id, snapshot)
        _invalidate(repository, case_id)
        return saved

    monkeypatch.setattr(repository, "save_analysis_snapshot", save_then_invalidate)
    with pytest.raises(AuxiliaryLineageStale):
        run_monitoring_check(case.case_id)
    assert repository.list_case_alerts(case.case_id) == before_alerts
    assert repository.list_case_notifications(case.case_id) == before_notifications
    assert all(
        classify_snapshot(repository.get_case(case.case_id), snapshot) == "HISTORICAL"
        for snapshot in repository.list_analysis_snapshots(case.case_id)
    )


def test_forecast_and_simulation_revalidate_during_assembly(isolated_store, monkeypatch) -> None:
    repository = isolated_store
    case = _run_case(repository)
    from app.services.forecasting import forecast_service

    original_compute = forecast_service.compute_forecast_from_snapshots

    def compute_then_invalidate(*args, **kwargs):
        result = original_compute(*args, **kwargs)
        _invalidate(repository, case.case_id)
        return result

    with monkeypatch.context() as patch:
        patch.setattr(forecast_service, "compute_forecast_from_snapshots", compute_then_invalidate)
        forecast = client.get(f"/api/v1/cases/{case.case_id}/forecast")
    assert forecast.status_code == 409
    assert forecast.json()["detail"]["error"] == "case_auxiliary_lineage_stale"

    assert client.post(f"/api/v1/cases/{case.case_id}/run").status_code == 200
    from app.api.v1.routes import cases as case_routes

    original_build = case_routes.build_case_simulation_initialization

    def build_then_invalidate(*args, **kwargs):
        result = original_build(*args, **kwargs)
        _invalidate(repository, case.case_id)
        return result

    with monkeypatch.context() as patch:
        patch.setattr(case_routes, "build_case_simulation_initialization", build_then_invalidate)
        simulation = client.get(f"/api/v1/cases/{case.case_id}/simulation/initialization-preview")
    assert simulation.status_code == 409
    assert simulation.json()["detail"]["error"] == "case_auxiliary_lineage_stale"
