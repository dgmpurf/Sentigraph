from __future__ import annotations

import ast
import json
import os
import socket
import sqlite3
import subprocess
import urllib.request
from copy import deepcopy
from pathlib import Path
from typing import Any

import fastapi.routing as fastapi_routing
import pytest
from fastapi.testclient import TestClient

from app.api.v1.routes import internal_operator_review_only_staging as route_module
from app.main import app
from app.services.local_exchange_review_only_projection_bridge import (
    PROJECTION_FIELDS,
    PROJECTION_MODE,
    PROJECTION_SCHEMA,
    PROJECTION_VERSION,
    SOURCE_CHAIN_BOUNDARY,
    build_local_exchange_review_only_projection,
)
from app.services.local_exchange_review_only_staging_bridge import (
    LocalExchangeReviewOnlyStagingBridgeConfig,
)
from app.services.private_collector_package_resolver import (
    READABLE_METADATA_FILES,
    REQUIRED_PACKAGE_METADATA_FILES,
)


client = TestClient(app)

PRIMARY_GATE = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED"
BRIDGE_GATE = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED"
PROJECTION_GATE = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED"
RESULTS_DIR_ENV = "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR"
EXPORT_ROOT_ENV = "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT"
ADAPTER_ID_ENV = "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID"

LIST_ROUTE = "/api/v1/internal/staging/review-only/candidates"
DETAIL_ROUTE_TEMPLATE = f"{LIST_ROUTE}/{{staging_candidate_id}}"
BRIDGE_ROUTE_TEMPLATE = (
    "/api/v1/internal/staging/review-only/local-exchange/candidates/{result_file_name}"
)
PROJECTION_ROUTE_TEMPLATE = (
    "/api/v1/internal/staging/review-only/local-exchange/projections/{result_file_name}"
)
PROJECTION_ROUTE = PROJECTION_ROUTE_TEMPLATE.replace("{result_file_name}", "provider_result.json")

UPSTREAM_SCHEMA = "internal_operator_review_only_staging_local_exchange_response_v0_1"
EXPECTED_PROJECTION_FIELDS = (
    "projection_schema",
    "projection_version",
    "projection_mode",
    "projection_status",
    "projection_error_code",
    "source_chain_boundary",
    "result_file_name",
    "upstream_schema",
    "upstream_status",
    "reader_status",
    "adapter_status",
    "provider_result_status",
    "package_resolution_status",
    "candidate_count",
    "staging_candidate_id",
    "gate_result_id",
    "analysis_request_id",
    "provider_result_id",
    "package_name",
    "case_id_hint",
    "case_title_hint",
    "validation_summary",
    "coverage_summary",
    "review_status",
    "promotion_status",
    "staging_status",
    "gate_summary",
    "warnings",
    "blockers",
    "allowed_actions",
    "blocked_actions",
    "metadata_only",
    "review_only",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "candidate_persistence",
    "persistent_staging_write",
    "review_decision_write",
    "evidence_layer_write",
    "production_evidenceitem_created",
    "production_case_created",
    "analysis_run_created",
    "analysis_result_created",
    "frontend_action_enabled",
    "public_output_enabled",
    "export_delivery_enabled",
    "path_exposed",
    "raw_metadata_exposed",
    "trust_approved",
    "production_ready",
    "promotion_completed",
    "mutable_authority_granted",
)

ROW_LIKE_FILES = {
    "evidence_items.jsonl",
    "evidence_items.csv",
    "source_manifest.jsonl",
    "collection_log.jsonl",
}
ROW_SENTINEL = "B03_ROW_SENTINEL_MUST_NOT_BE_READ"
RAW_SENTINEL = "B03_RAW_IDENTITY_MUST_NOT_CROSS"


def _ready_upstream() -> dict[str, Any]:
    gate_summary = {
        "package_resolution_status": "package_ready",
        "provider_result_status": "accepted_metadata_only",
        "privacy_status": "privacy_clear",
        "path_status": "path_confined",
        "metadata_contract_status": "metadata_contract_valid",
        "evidence_row_boundary_status": "rows_not_read",
        "staging_status": "ready_for_human_review",
    }
    candidate = {
        "staging_candidate_id": "staging_candidate_b03_fixture",
        "gate_result_id": "gate_result_b03_fixture",
        "analysis_request_id": "analysis_request_b03_fixture",
        "provider_result_id": "provider_result_b03_fixture",
        "package_name": "safe_package",
        "case_id_hint": "case_b03_fixture",
        "case_title_hint": "Synthetic review candidate",
        "validation_status": "passed",
        "evidence_count": 34,
        "source_count": 7,
        "comment_count": 28,
        "root_candidate_count": 6,
        "warning_count": 0,
        "error_count": 0,
        "review_status": "ready_for_human_review",
        "promotion_status": "promotion_required",
        "staging_status": "ready_for_human_review",
        "blockers": [],
        "warnings": ["selected_package_coverage_only"],
        "allowed_actions": ["inspect_metadata", "record_human_review_outcome"],
        "blocked_actions": ["automatic_promotion", "production_import"],
        "safety_flags": {"metadata_only": True, "full_evidence_rows_parsed": False},
        "audit_refs": ["synthetic_fixture_only"],
        "gate_result": dict(gate_summary),
        "metadata_only": True,
        "path_exposed": False,
        "path_reference": None,
    }
    return {
        "schema": UPSTREAM_SCHEMA,
        "route_scope": "internal_operator_only",
        "access_scope": "review_only",
        "metadata_only": True,
        "review_only": True,
        "status": "ready_for_human_review",
        "error_code": None,
        "result_file_name": "provider_result.json",
        "reader_status": "metadata_ready",
        "adapter_status": "adapted",
        "provider_result_status": "accepted_metadata_only",
        "package_resolution_status": "package_ready",
        "candidate_count": 1,
        "staging_candidate": candidate,
        "gate_summary": gate_summary,
        "production_import_allowed": False,
        "evidence_layer_write_allowed": False,
        "production_case_creation_allowed": False,
        "analysis_run_allowed": False,
        "public_output_allowed": False,
        "path_exposed": False,
        "raw_metadata_exposed": False,
        "blockers": [],
        "warnings": ["selected_package_coverage_only"],
        "safety_flags": {"review_only_staging_bridge_only": True},
    }


def _manual_upstream() -> dict[str, Any]:
    upstream = _ready_upstream()
    upstream["status"] = "manual_review_required"
    upstream["staging_candidate"]["review_status"] = "manual_review_required"
    upstream["staging_candidate"]["staging_status"] = "manual_review_required"
    upstream["staging_candidate"]["gate_result"]["staging_status"] = "manual_review_required"
    upstream["gate_summary"]["staging_status"] = "manual_review_required"
    return upstream


def _blocked_upstream() -> dict[str, Any]:
    upstream = _ready_upstream()
    upstream.update(
        status="blocked_safety",
        candidate_count=0,
        staging_candidate=None,
        gate_summary=None,
        blockers=["blocked_safety"],
    )
    return upstream


def _set_all_gates(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(PRIMARY_GATE, "true")
    monkeypatch.setenv(BRIDGE_GATE, "true")
    monkeypatch.setenv(PROJECTION_GATE, "true")


def _set_server_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv(RESULTS_DIR_ENV, str(tmp_path / "results"))
    monkeypatch.setenv(EXPORT_ROOT_ENV, str(tmp_path / "exports"))
    monkeypatch.setenv(ADAPTER_ID_ENV, "external_collector_local_file_adapter")


def _effective_app_routes() -> list[Any]:
    iterator = getattr(fastapi_routing, "iter_route_contexts", None)
    if iterator is not None:
        return list(iterator(app.routes))
    immediate = list(app.routes)
    required = ("path", "methods", "matches")
    if all(all(hasattr(route, name) for name in required) for route in immediate):
        return immediate
    raise AssertionError("unsupported_route_inventory_contract")


def _provider_payload() -> dict[str, Any]:
    return {
        "schema": "sentigraph_provider_job_result_v1",
        "request_schema": "sentigraph_analysis_request_v1",
        "contract_version": "1.0",
        "adapter_id": "external_collector_local_file_adapter",
        "compatibility_status": "compatible",
        "status": "package_ready",
        "provider_result_id": "provider_result_b03_fixture",
        "provider_job_id": "provider_job_b03_fixture",
        "sentigraph_request_id": "analysis_request_b03_fixture",
        "provider_type": "private_collector_local_file",
        "package_contract": "sentigraph_evidence_export_v1",
        "package_id": "safe_package",
        "package_role": "review_ready_candidate",
        "package_index_ref": "package_index.json",
        "package_root_ref": "configured_export_root",
        "package_relative_path": "safe_package",
        "summary": {
            "evidence_items": 34,
            "sources": 7,
            "comment_samples": 28,
            "root_candidates": 6,
        },
        "validation_summary": {"status": "passed", "errors": 0, "warnings": 0},
        "coverage_note": "Selected package coverage only; not full-web or full-platform coverage.",
        "safety_markers": {
            "raw_author_id_exported": False,
            "raw_author_name_exported": False,
            "profile_url_exported": False,
            "raw_author_id_removed": True,
            "raw_author_name_removed": True,
            "no_private_messages": True,
        },
        "created_at": "2026-07-16T00:00:00Z",
        "warnings": [],
        "errors": [],
        "nextAction": "review_package_metadata",
    }


def _write_synthetic_fixture(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    results_dir.mkdir(parents=True)
    (results_dir / "provider_result.json").write_text(
        json.dumps(_provider_payload(), ensure_ascii=False), encoding="utf-8"
    )

    package_dir = tmp_path / "exports" / "safe_package"
    package_dir.mkdir(parents=True)
    for filename in REQUIRED_PACKAGE_METADATA_FILES:
        path = package_dir / filename
        if filename == "manifest.json":
            path.write_text(
                json.dumps(
                    {
                        "schema": "sentigraph_evidence_export_manifest_v1",
                        "package_name": "safe_package",
                        "raw_author_id_removed": True,
                        "raw_author_name_removed": True,
                        "profile_url_exported": False,
                    }
                ),
                encoding="utf-8",
            )
        elif filename == "validation_report.json":
            path.write_text(
                json.dumps({"status": "passed", "errors": 0, "warnings": 0}), encoding="utf-8"
            )
        elif filename in ROW_LIKE_FILES:
            path.write_text(f"{ROW_SENTINEL},{RAW_SENTINEL},not valid rows", encoding="utf-8")
        else:
            path.write_text("metadata only", encoding="utf-8")
    (package_dir / "package_index.json").write_text("{}", encoding="utf-8")


def _assert_boundary_flags(projection: dict[str, Any]) -> None:
    assert projection["metadata_only"] is True
    assert projection["review_only"] is True
    assert projection["human_review_required"] is True
    assert projection["no_automatic_trust_upgrade"] is True
    assert projection["candidate_persistence"] == "in_memory_only"
    for field in (
        "persistent_staging_write",
        "review_decision_write",
        "evidence_layer_write",
        "production_evidenceitem_created",
        "production_case_created",
        "analysis_run_created",
        "analysis_result_created",
        "frontend_action_enabled",
        "public_output_enabled",
        "export_delivery_enabled",
        "path_exposed",
        "raw_metadata_exposed",
        "trust_approved",
        "production_ready",
        "promotion_completed",
        "mutable_authority_granted",
    ):
        assert projection[field] is False


def test_projection_contract_has_exact_frozen_field_order() -> None:
    projection = build_local_exchange_review_only_projection("provider_result.json", _ready_upstream())

    assert PROJECTION_FIELDS == EXPECTED_PROJECTION_FIELDS
    assert tuple(projection) == EXPECTED_PROJECTION_FIELDS
    assert len(PROJECTION_FIELDS) == 52


def test_ready_projection_is_deterministic_and_metadata_only() -> None:
    upstream = _ready_upstream()

    first = build_local_exchange_review_only_projection("provider_result.json", deepcopy(upstream))
    second = build_local_exchange_review_only_projection("provider_result.json", deepcopy(upstream))

    assert first == second
    assert first["projection_schema"] == PROJECTION_SCHEMA
    assert first["projection_schema"] == "sentigraph_local_exchange_review_only_candidate_projection_v0_1"
    assert first["projection_version"] == PROJECTION_VERSION == "0.1"
    assert first["projection_mode"] == PROJECTION_MODE == "internal_governed_read_only_review_projection"
    assert first["source_chain_boundary"] == SOURCE_CHAIN_BOUNDARY
    assert first["source_chain_boundary"] == "local_exchange_review_only_staging_candidate_boundary"
    assert first["projection_status"] == "ready_for_human_review"
    assert first["projection_error_code"] is None
    assert first["candidate_count"] == 1
    assert first["package_name"] == "safe_package"
    assert first["validation_summary"] == {
        "validation_status": "passed",
        "warning_count": 0,
        "error_count": 0,
    }
    assert first["coverage_summary"] == {
        "evidence_count": 34,
        "source_count": 7,
        "comment_count": 28,
        "root_candidate_count": 6,
        "coverage_basis": "selected_package_metadata_counts_only",
        "full_web_coverage_claimed": False,
        "full_platform_coverage_claimed": False,
    }
    _assert_boundary_flags(first)


def test_projection_preserves_exact_four_counts_without_changing_top_level_contract() -> None:
    upstream = _ready_upstream()
    upstream["staging_candidate"].update(
        evidence_count=7,
        source_count=3,
        comment_count=4,
        root_candidate_count=2,
    )

    projection = build_local_exchange_review_only_projection("provider_result.json", upstream)

    assert projection["projection_status"] == "ready_for_human_review"
    assert tuple(projection) == EXPECTED_PROJECTION_FIELDS
    assert len(projection) == 52
    assert projection["coverage_summary"] == {
        "evidence_count": 7,
        "source_count": 3,
        "comment_count": 4,
        "root_candidate_count": 2,
        "coverage_basis": "selected_package_metadata_counts_only",
        "full_web_coverage_claimed": False,
        "full_platform_coverage_claimed": False,
    }
    _assert_boundary_flags(projection)


@pytest.mark.parametrize(
    ("upstream", "expected_status", "expected_error"),
    [
        (_manual_upstream(), "manual_review_required", "upstream_manual_review_required"),
        (_blocked_upstream(), "blocked_upstream", "upstream_not_ready"),
    ],
)
def test_manual_or_blocked_upstream_is_fail_closed_without_candidate_upgrade(
    upstream: dict[str, Any], expected_status: str, expected_error: str
) -> None:
    projection = build_local_exchange_review_only_projection("provider_result.json", upstream)

    assert projection["projection_status"] == expected_status
    assert projection["projection_error_code"] == expected_error
    assert projection["projection_status"] != "ready_for_human_review"
    assert projection["candidate_count"] == 0
    assert projection["staging_candidate_id"] is None
    assert projection["production_ready"] is False
    assert projection["promotion_completed"] is False
    _assert_boundary_flags(projection)


@pytest.mark.parametrize(
    "mutator",
    [
        lambda payload: payload.update(schema="unexpected_schema"),
        lambda payload: payload.update(candidate_count=0),
        lambda payload: payload.update(candidate_count=2),
        lambda payload: payload.update(staging_candidate=None),
        lambda payload: payload["staging_candidate"].update(gate_result=None),
        lambda payload: payload.update(gate_summary=None),
    ],
)
def test_wrong_schema_count_or_malformed_candidate_fails_closed(mutator: Any) -> None:
    upstream = _ready_upstream()
    mutator(upstream)

    projection = build_local_exchange_review_only_projection("provider_result.json", upstream)

    assert projection["projection_status"] == "projection_unavailable"
    assert projection["projection_error_code"] is not None
    assert projection["candidate_count"] == 0
    assert projection["staging_candidate_id"] is None
    _assert_boundary_flags(projection)


def test_unknown_benign_fields_do_not_leak_and_unknown_unsafe_fields_fail_closed() -> None:
    benign = _ready_upstream()
    benign["future_bounded_note"] = "ignored"
    benign["staging_candidate"]["future_safe_label"] = "ignored"

    benign_projection = build_local_exchange_review_only_projection("provider_result.json", benign)
    benign_text = json.dumps(benign_projection, sort_keys=True)

    assert benign_projection["projection_status"] == "ready_for_human_review"
    assert "future_bounded_note" not in benign_text
    assert "future_safe_label" not in benign_text

    unsafe = _ready_upstream()
    unsafe["staging_candidate"]["raw_payload"] = "raw-provider-object-must-not-cross"
    unsafe_projection = build_local_exchange_review_only_projection("provider_result.json", unsafe)
    unsafe_text = json.dumps(unsafe_projection, sort_keys=True)

    assert unsafe_projection["projection_status"] == "projection_unavailable"
    assert unsafe_projection["projection_error_code"] == "unsafe_unknown_field"
    assert "raw-provider-object-must-not-cross" not in unsafe_text


def test_f10_persistence_and_reservation_semantics_are_absent() -> None:
    upstream = _ready_upstream()
    upstream["persisted_record_id"] = "persisted_record_must_not_cross"
    upstream["staging_candidate"]["attempt_reservation_id"] = "reservation_must_not_cross"

    projection = build_local_exchange_review_only_projection("provider_result.json", upstream)
    text = json.dumps(projection, sort_keys=True)

    assert projection["projection_status"] == "projection_unavailable"
    for forbidden in (
        "persisted_record_id",
        "attempt_reservation_id",
        "candidate_identity_digest",
        "sqlite",
        "actual_column",
        "exact_target",
        "persisted_record_must_not_cross",
        "reservation_must_not_cross",
    ):
        assert forbidden not in text.lower()


def test_paths_raw_objects_identity_secrets_and_exception_text_do_not_cross() -> None:
    upstream = _ready_upstream()
    upstream["future_bounded_note"] = "ignored"
    upstream["staging_candidate"]["case_title_hint"] = "Synthetic review candidate"

    projection = build_local_exchange_review_only_projection("provider_result.json", upstream)
    text = json.dumps(projection, ensure_ascii=False, sort_keys=True)

    for forbidden in (
        "results_dir",
        "export_root",
        "raw_provider_result",
        "raw_package",
        "raw_author_id",
        "profile_url",
        "actual-token",
        "traceback",
        "g:\\",
        "c:\\",
        "https://",
        "http://",
    ):
        assert forbidden not in text.lower()
    _assert_boundary_flags(projection)


@pytest.mark.parametrize(
    ("disabled_gate", "expected_error"),
    [
        (PRIMARY_GATE, "route_disabled"),
        (BRIDGE_GATE, "local_exchange_route_disabled"),
        (PROJECTION_GATE, "review_projection_route_disabled"),
    ],
)
def test_each_route_gate_fails_closed_before_bridge_or_projection(
    monkeypatch: pytest.MonkeyPatch, disabled_gate: str, expected_error: str
) -> None:
    _set_all_gates(monkeypatch)
    monkeypatch.delenv(disabled_gate, raising=False)

    def fail(*args: object, **kwargs: object) -> dict[str, Any]:
        raise AssertionError("disabled route must not call the B01 bridge or B03 projection builder")

    monkeypatch.setattr(route_module, "build_local_exchange_review_only_staging_response", fail)
    monkeypatch.setattr(route_module, "build_local_exchange_review_only_projection", fail)

    response = client.get(PROJECTION_ROUTE)
    payload = response.json()

    assert response.status_code == 200
    assert payload["projection_status"] == "projection_unavailable"
    assert payload["projection_error_code"] == expected_error
    assert payload["candidate_count"] == 0
    _assert_boundary_flags(payload)


@pytest.mark.parametrize("bad_name", ["provider_result.txt", "..%5Coutside.json"])
def test_route_rejects_invalid_filename_and_traversal_before_local_reader(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, bad_name: str
) -> None:
    _set_all_gates(monkeypatch)
    _set_server_config(monkeypatch, tmp_path)

    def fail_reader(*args: object, **kwargs: object) -> object:
        raise AssertionError("invalid basename must be rejected before the local reader")

    monkeypatch.setattr(
        "app.services.local_exchange_review_only_staging_bridge.read_local_exchange_provider_result_metadata",
        fail_reader,
    )

    payload = client.get(PROJECTION_ROUTE_TEMPLATE.replace("{result_file_name}", bad_name)).json()

    assert payload["projection_status"] == "projection_unavailable"
    assert payload["projection_error_code"] == "invalid_result_file_name"
    assert payload["candidate_count"] == 0


def test_route_uses_server_owned_configuration_and_calls_each_builder_once(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _set_all_gates(monkeypatch)
    _set_server_config(monkeypatch, tmp_path)
    calls: dict[str, Any] = {"bridge": 0, "projection": 0, "config": None}

    def fake_bridge(
        result_file_name: str, config: LocalExchangeReviewOnlyStagingBridgeConfig
    ) -> dict[str, Any]:
        calls["bridge"] += 1
        calls["config"] = config
        assert result_file_name == "provider_result.json"
        return _ready_upstream()

    def fake_projection(result_file_name: str, upstream: dict[str, Any]) -> dict[str, Any]:
        calls["projection"] += 1
        assert result_file_name == "provider_result.json"
        assert upstream == _ready_upstream()
        return build_local_exchange_review_only_projection(result_file_name, upstream)

    monkeypatch.setattr(route_module, "build_local_exchange_review_only_staging_response", fake_bridge)
    monkeypatch.setattr(route_module, "build_local_exchange_review_only_projection", fake_projection)

    response = client.get(
        f"{PROJECTION_ROUTE}?results_dir=client-owned&export_root=client-owned&adapter_id=client-owned"
    )
    payload = response.json()

    assert response.status_code == 200
    assert payload["projection_error_code"] is None
    assert payload["projection_status"] == "ready_for_human_review"
    assert calls["bridge"] == 1
    assert calls["projection"] == 1
    config = calls["config"]
    assert isinstance(config, LocalExchangeReviewOnlyStagingBridgeConfig)
    assert config.results_dir == str(tmp_path / "results")
    assert config.export_root == str(tmp_path / "exports")
    assert config.adapter_id == "external_collector_local_file_adapter"


def test_enabled_synthetic_route_reads_one_result_and_only_fixed_safe_package_metadata(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    import app.services.local_exchange_review_only_staging_bridge as bridge_module

    _write_synthetic_fixture(tmp_path)
    _set_all_gates(monkeypatch)
    _set_server_config(monkeypatch, tmp_path)

    actual_local_reader = bridge_module.read_local_exchange_provider_result_metadata
    actual_provider_reader = bridge_module.read_private_collector_provider_result_metadata
    actual_route_bridge = route_module.build_local_exchange_review_only_staging_response
    original_read_text = Path.read_text
    original_open = Path.open
    calls = {
        "local_reader": 0,
        "provider_reader": 0,
        "row_opens": 0,
        "directory_enumerations": 0,
        "file_writes": 0,
        "decision_writes": 0,
        "external_calls": 0,
    }
    package_reads: list[str] = []
    captured_upstream: dict[str, Any] = {}

    def counting_local_reader(*args: object, **kwargs: object) -> object:
        calls["local_reader"] += 1
        return actual_local_reader(*args, **kwargs)

    def counting_provider_reader(*args: object, **kwargs: object) -> object:
        calls["provider_reader"] += 1
        return actual_provider_reader(*args, **kwargs)

    def capturing_route_bridge(*args: object, **kwargs: object) -> dict[str, Any]:
        response = actual_route_bridge(*args, **kwargs)
        captured_upstream.update(response)
        return response

    def guarded_read_text(self: Path, *args: object, **kwargs: object) -> str:
        if self.name in ROW_LIKE_FILES:
            calls["row_opens"] += 1
            raise AssertionError(f"row-like file must not be read: {self.name}")
        if self.parent.name == "safe_package":
            package_reads.append(self.name)
        return original_read_text(self, *args, **kwargs)

    def guarded_open(self: Path, mode: str = "r", *args: object, **kwargs: object) -> Any:
        if any(marker in mode for marker in ("w", "a", "x", "+")):
            calls["file_writes"] += 1
            raise AssertionError("request path must not write files")
        return original_open(self, mode, *args, **kwargs)

    def fail_iterdir(self: Path) -> Any:
        calls["directory_enumerations"] += 1
        raise AssertionError("request path must not enumerate directories")

    def fail_decision_write(*args: object, **kwargs: object) -> Any:
        calls["decision_writes"] += 1
        raise AssertionError("request path must not open SQLite")

    def fail_external(*args: object, **kwargs: object) -> Any:
        calls["external_calls"] += 1
        raise AssertionError("request path must not make external calls")

    monkeypatch.setattr(bridge_module, "read_local_exchange_provider_result_metadata", counting_local_reader)
    monkeypatch.setattr(bridge_module, "read_private_collector_provider_result_metadata", counting_provider_reader)
    monkeypatch.setattr(route_module, "build_local_exchange_review_only_staging_response", capturing_route_bridge)
    monkeypatch.setattr(Path, "read_text", guarded_read_text)
    monkeypatch.setattr(Path, "open", guarded_open)
    monkeypatch.setattr(Path, "iterdir", fail_iterdir)
    monkeypatch.setattr(sqlite3, "connect", fail_decision_write)
    monkeypatch.setattr(socket, "create_connection", fail_external)
    monkeypatch.setattr(urllib.request, "urlopen", fail_external)
    monkeypatch.setattr(subprocess, "run", fail_external)
    monkeypatch.setattr(subprocess, "Popen", fail_external)

    response = client.get(PROJECTION_ROUTE)
    payload = response.json()
    candidate = captured_upstream.get("staging_candidate") or {}
    diagnostic = {
        "reader_status": captured_upstream.get("reader_status"),
        "adapter_status": captured_upstream.get("adapter_status"),
        "provider_result_status": captured_upstream.get("provider_result_status"),
        "package_resolution_status": captured_upstream.get("package_resolution_status"),
        "review_status": candidate.get("review_status"),
        "promotion_status": candidate.get("promotion_status"),
        "staging_status": candidate.get("staging_status"),
        "metadata_only": candidate.get("metadata_only"),
        "path_exposed": candidate.get("path_exposed"),
        "path_reference": candidate.get("path_reference"),
        "blockers": candidate.get("blockers"),
    }

    assert response.status_code == 200
    assert payload["projection_error_code"] is None, json.dumps(diagnostic, sort_keys=True)
    assert payload["projection_status"] == "ready_for_human_review"
    assert calls == {
        "local_reader": 1,
        "provider_reader": 1,
        "row_opens": 0,
        "directory_enumerations": 0,
        "file_writes": 0,
        "decision_writes": 0,
        "external_calls": 0,
    }
    expected_package_reads = set(READABLE_METADATA_FILES)
    assert package_reads
    assert len(package_reads) == len(expected_package_reads)
    assert set(package_reads) == expected_package_reads
    assert "package_index.json" in package_reads
    assert set(package_reads).isdisjoint(ROW_LIKE_FILES)
    assert ROW_SENTINEL not in json.dumps(payload)
    assert RAW_SENTINEL not in json.dumps(payload)
    _assert_boundary_flags(payload)


def test_existing_b01_route_remains_unchanged_and_never_calls_projection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_all_gates(monkeypatch)
    expected = _ready_upstream()
    calls = {"bridge": 0}

    def fake_bridge(*args: object, **kwargs: object) -> dict[str, Any]:
        calls["bridge"] += 1
        return expected

    def fail_projection(*args: object, **kwargs: object) -> dict[str, Any]:
        raise AssertionError("existing B01 route must not call the B03 projection builder")

    monkeypatch.setattr(route_module, "build_local_exchange_review_only_staging_response", fake_bridge)
    monkeypatch.setattr(route_module, "build_local_exchange_review_only_projection", fail_projection)

    payload = client.get(BRIDGE_ROUTE_TEMPLATE.replace("{result_file_name}", "provider_result.json")).json()

    assert payload == expected
    assert calls["bridge"] == 1


def test_route_family_is_exactly_four_internal_get_only_routes() -> None:
    route_methods = {
        route.path: route.methods
        for route in _effective_app_routes()
        if "staging/review-only" in getattr(route, "path", "")
    }

    assert set(route_methods) == {
        LIST_ROUTE,
        DETAIL_ROUTE_TEMPLATE,
        BRIDGE_ROUTE_TEMPLATE,
        PROJECTION_ROUTE_TEMPLATE,
    }
    for path, methods in route_methods.items():
        assert path.startswith("/api/v1/internal/")
        assert methods == {"GET"}
        assert not {"POST", "PUT", "PATCH", "DELETE"} & methods


def test_projection_service_is_pure_and_has_no_io_environment_database_network_or_f10_imports() -> None:
    service_path = (
        Path(__file__).parents[1]
        / "services"
        / "local_exchange_review_only_projection_bridge.py"
    )
    source = service_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_roots = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_roots.update(
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    )

    assert imported_roots.isdisjoint(
        {
            "app",
            "os",
            "pathlib",
            "sqlite3",
            "socket",
            "subprocess",
            "requests",
            "httpx",
            "urllib",
        }
    )
    lowered = source.lower()
    for forbidden in (
        "persisted_record_id",
        "attempt_reservation_id",
        "candidate_identity_digest",
        "sqlite",
        "actual_column",
        "exact_target",
        "open(",
        "read_text(",
        "write_text(",
        "getenv(",
        "environ",
    ):
        assert forbidden not in lowered
