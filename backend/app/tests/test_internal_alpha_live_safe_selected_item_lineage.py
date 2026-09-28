"""Synthetic/temp-file contract tests; no real LocalJson business data is read."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

import app.api.v1.routes.internal_alpha_review_console as route_module
from app.repositories.case_repository import CaseRepository
from app.services.internal_alpha_live_safe_selected_item_lineage_projection import (
    SOURCE_FIELDS,
    LiveSafeLineageAmbiguous,
    LiveSafeLineageContractError,
    LiveSafeLineageUnavailable,
    build_live_safe_selected_item_lineage_projection,
)
from app.services.storage.local_json_store import LocalJsonCaseStore


CASE_ID = "case_001"
EVIDENCE_ID = "evidence_youtube_official_api_video_comment"
PREFIX = "/api/v1/internal/alpha/review-console"
LIVE_PATH = f"{PREFIX}/v0.1/live-selected-item-lineage/{CASE_ID}/{EVIDENCE_ID}"
RESPONSE_FIELDS = (
    "response_schema", "route_mode", "status", "projection", "safe_metadata_only",
    "human_review_required", "no_automatic_trust_upgrade", "synthetic_fixture_only",
    "live_persisted_record_connected", "actual_write_enabled", "production_object_enabled",
    "review_queue_runtime_enabled", "public_ready", "production_ready",
)
PROJECTION_FIELDS = (
    "projection_schema", "projection_mode", "binding_mode", "reviewed_batch_safe_hash",
    "fresh_batch_safe_hash", "persisted_selected_safe_hash", "selected_binding_evidence_present",
    "reply_content_acquired", "author_identity_omitted_at_production",
    "transport_source_provenance_only", "human_review_required",
    "no_automatic_trust_upgrade", "synthetic_fixture_only", "live_persisted_record_connected",
)

app = FastAPI()
app.include_router(route_module.router, prefix=PREFIX)
client = TestClient(app)


def safe_source() -> dict[str, object]:
    return {
        "review_binding_mode": "selected_item_v1",
        "reviewed_batch_safe_hash": "1" * 64,
        "fresh_batch_safe_hash": "2" * 64,
        "selected_discussion_safe_hash": "3" * 64,
        "reply_content_acquired": False,
        "author_identity_omitted": True,
    }


def evidence_item(*, evidence_id: str = EVIDENCE_ID, source: object = None) -> dict[str, object]:
    return {
        "case_id": CASE_ID,
        "evidence_id": evidence_id,
        "comment_text": "PRIVATE_BODY_POISON",
        "author_name": "PRIVATE_AUTHOR_POISON",
        "raw_data_safe": {
            **(safe_source() if source is None else source),
            "comment_id": "PRIVATE_COMMENT_ID_POISON",
            "source_url": "PRIVATE_URL_POISON",
        },
    }


def store_with_items(tmp_path: Path, items: list[object]) -> LocalJsonCaseStore:
    store_path = tmp_path / "synthetic_cases.json"
    store_path.write_text(json.dumps({
        "cases": {
            CASE_ID: {"case_id": CASE_ID, "evidence_items": items},
            "another_case": {"case_id": "another_case", "evidence_items": "POISON_OTHER_CASE"},
        },
    }), encoding="utf-8")
    return LocalJsonCaseStore(store_path)


def set_gates(monkeypatch: pytest.MonkeyPatch, parent: str | None, dedicated: str | None) -> None:
    for flag, value in (
        (route_module.ENV_FLAG, parent),
        (route_module.LIVE_SAFE_SELECTED_ITEM_LINEAGE_ENV_FLAG, dedicated),
    ):
        if value is None:
            monkeypatch.delenv(flag, raising=False)
        else:
            monkeypatch.setenv(flag, value)


def assert_no_private_content(payload: object) -> None:
    text = json.dumps(payload, sort_keys=True)
    for poison in (
        "PRIVATE_BODY_POISON", "PRIVATE_AUTHOR_POISON", "PRIVATE_COMMENT_ID_POISON",
        "PRIVATE_URL_POISON", CASE_ID, EVIDENCE_ID, "raw_data_safe", "evidence_items",
    ):
        assert poison not in text


def test_exact_one_store_reader_detaches_only_six_scalars_without_full_case_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = store_with_items(tmp_path, [
        evidence_item(evidence_id="other_evidence"), evidence_item(),
    ])

    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("full-case, list, write or provider fallback called")

    for method in ("get_case", "list_cases", "update_case", "create_case", "_write_data"):
        monkeypatch.setattr(store, method, forbidden)
    source = store.read_exact_live_safe_selected_item_lineage(CASE_ID, EVIDENCE_ID)
    assert tuple(source) == SOURCE_FIELDS
    assert dict(source) == safe_source()
    with pytest.raises(TypeError):
        source["reply_content_acquired"] = True  # type: ignore[index]
    projection = build_live_safe_selected_item_lineage_projection(source)
    assert tuple(projection) == PROJECTION_FIELDS
    assert projection["synthetic_fixture_only"] is False
    assert projection["live_persisted_record_connected"] is True
    assert projection["transport_source_provenance_only"] is True
    assert_no_private_content(dict(projection))


@pytest.mark.parametrize("items,error", [
    ([], LiveSafeLineageUnavailable),
    ([evidence_item(evidence_id="other_evidence")], LiveSafeLineageUnavailable),
    ([evidence_item(), evidence_item()], LiveSafeLineageAmbiguous),
])
def test_zero_and_multiple_exact_matches_fail_closed(
    tmp_path: Path, items: list[object], error: type[Exception]
) -> None:
    store = store_with_items(tmp_path, items)
    with pytest.raises(error) as caught:
        store.read_exact_live_safe_selected_item_lineage(CASE_ID, EVIDENCE_ID)
    assert_no_private_content(str(caught.value))


@pytest.mark.parametrize("field,invalid", [
    ("review_binding_mode", "batch_v1"),
    ("reviewed_batch_safe_hash", "A" * 64),
    ("fresh_batch_safe_hash", "3" * 63),
    ("selected_discussion_safe_hash", "g" * 64),
    ("reply_content_acquired", True),
    ("reply_content_acquired", 0),
    ("author_identity_omitted", False),
    ("author_identity_omitted", 1),
])
def test_malformed_or_privacy_unsafe_attestations_fail_before_repository_boundary(
    tmp_path: Path, field: str, invalid: object
) -> None:
    source = safe_source()
    source[field] = invalid
    store = store_with_items(tmp_path, [evidence_item(source=source)])
    with pytest.raises(LiveSafeLineageContractError) as caught:
        CaseRepository(store).read_exact_live_safe_selected_item_lineage(CASE_ID, EVIDENCE_ID)
    assert_no_private_content(str(caught.value))


@pytest.mark.parametrize("field", SOURCE_FIELDS)
def test_missing_attestation_never_gets_default(tmp_path: Path, field: str) -> None:
    source = safe_source()
    del source[field]
    store = store_with_items(tmp_path, [evidence_item(source=source)])
    with pytest.raises(LiveSafeLineageContractError):
        store.read_exact_live_safe_selected_item_lineage(CASE_ID, EVIDENCE_ID)


def test_invalid_selector_and_other_backend_fail_before_full_case_access(tmp_path: Path) -> None:
    store = store_with_items(tmp_path, [evidence_item()])
    for selector in ("bad space", "../private", "x" * 257):
        with pytest.raises(LiveSafeLineageContractError):
            store.read_exact_live_safe_selected_item_lineage(CASE_ID, selector)

    class OtherBackend:
        def get_case(self, case_id: str) -> None:
            raise AssertionError("full-case fallback called")

    with pytest.raises(LiveSafeLineageUnavailable):
        CaseRepository(OtherBackend()).read_exact_live_safe_selected_item_lineage(  # type: ignore[arg-type]
            CASE_ID, EVIDENCE_ID
        )


@pytest.mark.parametrize("parent,dedicated", [
    (None, None), ("1", None), (None, "1"), ("false", "true"), ("yes", "false"),
])
def test_disabled_route_never_initializes_or_reads_store(
    monkeypatch: pytest.MonkeyPatch, parent: str | None, dedicated: str | None
) -> None:
    set_gates(monkeypatch, parent, dedicated)

    def forbidden() -> None:
        raise AssertionError("disabled route initialized repository")

    monkeypatch.setattr(route_module, "get_case_repository", forbidden)
    payload = client.get(LIVE_PATH).json()
    assert tuple(payload) == RESPONSE_FIELDS
    assert payload["status"] == "disabled"
    assert payload["projection"] is None
    assert payload["live_persisted_record_connected"] is False
    assert_no_private_content(payload)


def test_enabled_route_has_fixed_safe_allowlist_and_no_selector_echo(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    set_gates(monkeypatch, "1", "yes")
    repository = CaseRepository(store_with_items(tmp_path, [evidence_item()]))
    monkeypatch.setattr(route_module, "get_case_repository", lambda: repository)
    response = client.get(LIVE_PATH)
    assert response.status_code == 200
    payload = response.json()
    assert tuple(payload) == RESPONSE_FIELDS
    assert payload["status"] == "available"
    assert tuple(payload["projection"]) == PROJECTION_FIELDS
    assert payload["projection"]["persisted_selected_safe_hash"] == "3" * 64
    assert payload["live_persisted_record_connected"] is True
    assert payload["synthetic_fixture_only"] is False
    assert payload["actual_write_enabled"] is False
    assert payload["production_ready"] is False
    assert_no_private_content(payload)


@pytest.mark.parametrize("items,status", [
    ([], "unavailable"),
    ([evidence_item(), evidence_item()], "ambiguous"),
    ([evidence_item(source={"review_binding_mode": "batch_v1"})], "contract_mismatch"),
])
def test_enabled_route_failures_expose_only_static_status(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, items: list[object], status: str
) -> None:
    set_gates(monkeypatch, "1", "1")
    repository = CaseRepository(store_with_items(tmp_path, items))
    monkeypatch.setattr(route_module, "get_case_repository", lambda: repository)
    payload = client.get(LIVE_PATH).json()
    assert tuple(payload) == RESPONSE_FIELDS
    assert payload["status"] == status
    assert payload["projection"] is None
    assert_no_private_content(payload)


def test_enabled_route_unexpected_error_is_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    set_gates(monkeypatch, "1", "1")

    def failed() -> None:
        raise RuntimeError("PRIVATE_BODY_POISON")

    monkeypatch.setattr(route_module, "get_case_repository", failed)
    payload = client.get(LIVE_PATH).json()
    assert payload["status"] == "unavailable"
    assert_no_private_content(payload)


def test_new_route_is_separate_get_only_and_synthetic_fixture_is_unchanged() -> None:
    routes = {route.path: route.methods for route in route_module.router.routes}
    assert "/v0.1/live-selected-item-lineage/{case_id}/{evidence_id}" in routes
    assert routes["/v0.1/live-selected-item-lineage/{case_id}/{evidence_id}"] == {"GET"}
    assert routes["/selected-item-lineage-fixture"] == {"GET"}
