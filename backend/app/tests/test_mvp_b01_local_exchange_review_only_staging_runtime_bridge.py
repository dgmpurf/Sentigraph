from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import fastapi.routing as fastapi_routing
import pytest
from fastapi.testclient import TestClient

from app.api.v1.routes import internal_operator_review_only_staging as route_module
from app.main import app
from app.services.local_exchange_review_only_staging_bridge import (
    LocalExchangeReviewOnlyStagingBridgeConfig,
    adapt_local_exchange_metadata_to_provider_result,
    build_local_exchange_review_only_staging_response,
)
from app.services.private_collector_package_resolver import REQUIRED_PACKAGE_METADATA_FILES


client = TestClient(app)

PRIMARY_GATE = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED"
BRIDGE_GATE = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED"
RESULTS_DIR_ENV = "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR"
EXPORT_ROOT_ENV = "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT"
ADAPTER_ID_ENV = "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID"
BRIDGE_ROUTE = "/api/v1/internal/staging/review-only/local-exchange/candidates/provider_result.json"
LIST_ROUTE = "/api/v1/internal/staging/review-only/candidates"
DETAIL_ROUTE = f"{LIST_ROUTE}/synthetic_review_staging_candidate"
ROW_SENTINEL = "B01_ROW_SENTINEL_MUST_NOT_BE_READ"
RAW_SENTINEL = "B01_RAW_IDENTITY_MUST_NOT_BE_EXPOSED"
ROW_LIKE_FILES = {
    "evidence_items.jsonl",
    "evidence_items.csv",
    "source_manifest.jsonl",
    "collection_log.jsonl",
}


def _effective_app_routes() -> list[Any]:
    iterator = getattr(fastapi_routing, "iter_route_contexts", None)
    if iterator is not None:
        return list(iterator(app.routes))
    immediate = list(app.routes)
    required = ("path", "methods", "matches")
    if all(all(hasattr(route, name) for name in required) for route in immediate):
        return immediate
    raise AssertionError("unsupported_route_inventory_contract")


def _config(tmp_path: Path, **overrides: str) -> LocalExchangeReviewOnlyStagingBridgeConfig:
    values = {
        "results_dir": str(tmp_path / "results"),
        "export_root": str(tmp_path / "exports"),
        "adapter_id": "external_collector_local_file_adapter",
    }
    values.update(overrides)
    return LocalExchangeReviewOnlyStagingBridgeConfig(**values)


def _v1_payload(
    *,
    package_name: str = "safe_package",
    status: str = "package_ready",
    compatibility_status: str = "compatible",
) -> dict[str, Any]:
    return {
        "schema": "sentigraph_provider_job_result_v1",
        "request_schema": "sentigraph_analysis_request_v1",
        "contract_version": "1.0",
        "adapter_id": "external_collector_local_file_adapter",
        "compatibility_status": compatibility_status,
        "status": status,
        "provider_result_id": "provider_result_b01_fixture",
        "provider_job_id": "provider_job_b01_fixture",
        "sentigraph_request_id": "analysis_request_b01_fixture",
        "provider_type": "private_collector_local_file",
        "package_contract": "sentigraph_evidence_export_v1",
        "package_id": package_name,
        "package_role": "review_ready_candidate",
        "package_index_ref": "package_index.json",
        "package_root_ref": "configured_export_root",
        "package_relative_path": package_name,
        "summary": {
            "evidence_items": 34,
            "sources": 7,
            "comment_samples": 28,
            "root_candidates": 6,
        },
        "validation_summary": {
            "status": "passed",
            "errors": 0,
            "warnings": 0,
        },
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


def _write_result(results_dir: Path, payload: dict[str, Any], name: str = "provider_result.json") -> Path:
    results_dir.mkdir(parents=True, exist_ok=True)
    path = results_dir / name
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def _write_package(export_root: Path, package_name: str, *, forbidden_metadata: bool = False) -> Path:
    package_dir = export_root / package_name
    package_dir.mkdir(parents=True)
    for filename in REQUIRED_PACKAGE_METADATA_FILES:
        path = package_dir / filename
        if filename == "manifest.json":
            payload: dict[str, Any] = {
                "schema": "sentigraph_evidence_export_manifest_v1",
                "package_name": package_name,
                "raw_author_id_removed": True,
                "raw_author_name_removed": True,
                "profile_url_exported": False,
            }
            if forbidden_metadata:
                payload["token"] = "actual-token-must-not-cross-response"
            path.write_text(json.dumps(payload), encoding="utf-8")
        elif filename == "validation_report.json":
            path.write_text(json.dumps({"status": "passed", "errors": 0, "warnings": 0}), encoding="utf-8")
        elif filename in ROW_LIKE_FILES:
            path.write_text(f"{ROW_SENTINEL},{RAW_SENTINEL},not valid rows", encoding="utf-8")
        else:
            path.write_text("metadata only", encoding="utf-8")
    return package_dir


def _ready_bridge(tmp_path: Path) -> dict[str, Any]:
    config = _config(tmp_path)
    _write_result(Path(config.results_dir), _v1_payload())
    _write_package(Path(config.export_root), "safe_package")
    return build_local_exchange_review_only_staging_response("provider_result.json", config)


def _enable_route(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv(PRIMARY_GATE, "true")
    monkeypatch.setenv(BRIDGE_GATE, "true")
    monkeypatch.setenv(RESULTS_DIR_ENV, str(tmp_path / "results"))
    monkeypatch.setenv(EXPORT_ROOT_ENV, str(tmp_path / "exports"))
    monkeypatch.setenv(ADAPTER_ID_ENV, "external_collector_local_file_adapter")


def _assert_safe_response(payload: dict[str, Any], tmp_path: Path) -> None:
    text = json.dumps(payload, ensure_ascii=False).lower()
    assert payload["schema"] == "internal_operator_review_only_staging_local_exchange_response_v0_1"
    assert payload["metadata_only"] is True
    assert payload["review_only"] is True
    assert payload["path_exposed"] is False
    assert payload["raw_metadata_exposed"] is False
    assert str(tmp_path).lower() not in text
    assert "g:\\" not in text
    assert "c:\\users" not in text
    assert ROW_SENTINEL.lower() not in text
    assert RAW_SENTINEL.lower() not in text
    assert "actual-token-must-not-cross-response" not in text


def test_primary_route_gate_disabled_returns_route_disabled_without_bridge_or_file_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(PRIMARY_GATE, raising=False)
    monkeypatch.setenv(BRIDGE_GATE, "true")

    def fail_bridge(*args: object, **kwargs: object) -> dict[str, Any]:
        raise AssertionError("bridge must not execute while the primary route gate is disabled")

    monkeypatch.setattr(route_module, "build_local_exchange_review_only_staging_response", fail_bridge)
    payload = client.get(BRIDGE_ROUTE).json()

    assert payload["error_code"] == "route_disabled"
    assert payload["candidate_count"] == 0


def test_local_exchange_bridge_gate_is_disabled_by_default_without_bridge_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(PRIMARY_GATE, "true")
    monkeypatch.delenv(BRIDGE_GATE, raising=False)

    def fail_bridge(*args: object, **kwargs: object) -> dict[str, Any]:
        raise AssertionError("bridge must not execute while its gate is disabled")

    monkeypatch.setattr(route_module, "build_local_exchange_review_only_staging_response", fail_bridge)
    payload = client.get(BRIDGE_ROUTE).json()

    assert payload["error_code"] == "local_exchange_route_disabled"
    assert payload["candidate_count"] == 0


@pytest.mark.parametrize("missing_env", [RESULTS_DIR_ENV, EXPORT_ROOT_ENV, ADAPTER_ID_ENV])
def test_missing_server_owned_configuration_blocks_safely(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    missing_env: str,
) -> None:
    _enable_route(monkeypatch, tmp_path)
    monkeypatch.delenv(missing_env, raising=False)

    payload = client.get(BRIDGE_ROUTE).json()

    assert payload["status"] == "blocked_configuration"
    assert payload["candidate_count"] == 0
    _assert_safe_response(payload, tmp_path)


@pytest.mark.parametrize(
    "bad_name",
    [
        "",
        ".",
        "..",
        "../provider_result.json",
        "nested/provider_result.json",
        "nested\\provider_result.json",
        "C:provider_result.json",
        "https:%2F%2Fexample.test%2Fprovider_result.json",
        "provider result.json",
        "provider_result.txt",
        "provider_result.json%00",
        "a" * 250 + ".json",
    ],
)
def test_invalid_result_basename_is_rejected_before_local_reader(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    bad_name: str,
) -> None:
    def fail_reader(*args: object, **kwargs: object) -> object:
        raise AssertionError("invalid basename must be rejected before any reader call")

    monkeypatch.setattr(
        "app.services.local_exchange_review_only_staging_bridge.read_local_exchange_provider_result_metadata",
        fail_reader,
    )

    payload = build_local_exchange_review_only_staging_response(bad_name, _config(tmp_path))

    assert payload["status"] == "invalid_result_file_name"
    assert payload["candidate_count"] == 0


def test_result_path_cannot_escape_configured_results_directory(tmp_path: Path) -> None:
    outside = tmp_path / "outside.json"
    outside.write_text(json.dumps(_v1_payload()), encoding="utf-8")

    payload = build_local_exchange_review_only_staging_response("../outside.json", _config(tmp_path))

    assert payload["status"] == "invalid_result_file_name"
    assert payload["reader_status"] == "not_called"


def test_absent_safe_basename_returns_not_found_without_candidate(tmp_path: Path) -> None:
    config = _config(tmp_path)
    Path(config.results_dir).mkdir(parents=True)

    payload = build_local_exchange_review_only_staging_response("missing.json", config)

    assert payload["status"] == "not_found"
    assert payload["candidate_count"] == 0
    assert payload["reader_status"] == "not_found"


@pytest.mark.parametrize("content", ["{invalid", "[]"])
def test_invalid_json_or_non_object_schema_is_safe(tmp_path: Path, content: str) -> None:
    config = _config(tmp_path)
    results_dir = Path(config.results_dir)
    results_dir.mkdir(parents=True)
    (results_dir / "provider_result.json").write_text(content, encoding="utf-8")

    payload = build_local_exchange_review_only_staging_response("provider_result.json", config)

    assert payload["status"] == "needs_fix_metadata_contract"
    assert payload["candidate_count"] == 0
    _assert_safe_response(payload, tmp_path)


def test_unsupported_v1_contract_maps_to_needs_fix_without_package_resolution(tmp_path: Path) -> None:
    config = _config(tmp_path)
    source = _v1_payload()
    source["contract_version"] = "2.0"
    _write_result(Path(config.results_dir), source)

    payload = build_local_exchange_review_only_staging_response("provider_result.json", config)

    assert payload["status"] == "needs_fix_metadata_contract"
    assert payload["reader_status"] == "unsupported_contract"
    assert payload["candidate_count"] == 0


def test_unknown_future_platform_is_manual_and_never_ready(tmp_path: Path) -> None:
    config = _config(tmp_path)
    source = _v1_payload()
    source["platforms"] = [{"platform": "unknown_future_platform"}]
    _write_result(Path(config.results_dir), source)

    payload = build_local_exchange_review_only_staging_response("provider_result.json", config)

    assert payload["status"] == "manual_review_required"
    assert payload["status"] != "ready_for_human_review"
    assert payload["candidate_count"] == 0


def test_pure_v1_to_v0_1_adapter_is_exact_and_deterministic() -> None:
    source = _v1_payload()

    first = adapt_local_exchange_metadata_to_provider_result(source)
    second = adapt_local_exchange_metadata_to_provider_result(dict(source))

    assert first.status == "adapted"
    assert first.provider_result == second.provider_result
    assert first.provider_result == {
        "schema": "sentigraph_provider_job_result_v0_1",
        "provider_result_id": "provider_result_b01_fixture",
        "provider_job_id": "provider_job_b01_fixture",
        "request_id": "analysis_request_b01_fixture",
        "provider_type": "private_collector_local_file",
        "adapter_id": "external_collector_local_file_adapter",
        "contract_version": "0.1",
        "status": "package_ready",
        "package_contract": "sentigraph_evidence_export_v1",
        "package_reference": {
            "package_name": "safe_package",
            "package_role": "review_ready_candidate",
            "package_index_ref": "package_index.json",
            "package_locator_strategy": "package_name_under_configured_export_root",
        },
        "metadata_summary": {
            "evidence_count": 34,
            "source_count": 7,
            "comment_count": 28,
            "root_candidate_count": 6,
        },
        "validation_summary": {"status": "passed", "errors": 0, "warnings": 0},
        "coverage_note": "Selected package coverage only; not full-web or full-platform coverage.",
        "safety_markers": source["safety_markers"],
        "created_at": "2026-07-16T00:00:00Z",
    }


def test_safe_package_creates_exactly_one_in_memory_candidate_and_gate(tmp_path: Path) -> None:
    payload = _ready_bridge(tmp_path)

    assert payload["status"] == "ready_for_human_review"
    assert payload["candidate_count"] == 1
    assert payload["staging_candidate"]["package_name"] == "safe_package"
    assert payload["staging_candidate"]["analysis_request_id"] == "analysis_request_b01_fixture"
    assert payload["staging_candidate"]["evidence_count"] == 34
    assert payload["staging_candidate"]["source_count"] == 7
    assert payload["staging_candidate"]["comment_count"] == 28
    assert payload["staging_candidate"]["root_candidate_count"] == 6
    assert payload["gate_summary"]["staging_status"] == "ready_for_human_review"
    assert payload["production_import_allowed"] is False
    _assert_safe_response(payload, tmp_path)


def test_exact_four_v1_counts_survive_adapter_and_b01_staging(tmp_path: Path) -> None:
    source = _v1_payload()
    source["summary"] = {
        "evidence_items": 7,
        "sources": 3,
        "comment_samples": 4,
        "root_candidates": 2,
    }

    adapter = adapt_local_exchange_metadata_to_provider_result(source)
    assert adapter.status == "adapted"
    assert adapter.provider_result is not None
    assert adapter.provider_result["metadata_summary"] == {
        "evidence_count": 7,
        "source_count": 3,
        "comment_count": 4,
        "root_candidate_count": 2,
    }

    config = _config(tmp_path)
    _write_result(Path(config.results_dir), source)
    _write_package(Path(config.export_root), "safe_package")
    payload = build_local_exchange_review_only_staging_response("provider_result.json", config)

    assert payload["status"] == "ready_for_human_review"
    assert payload["candidate_count"] == 1
    assert {
        key: payload["staging_candidate"][key]
        for key in ("evidence_count", "source_count", "comment_count", "root_candidate_count")
    } == {
        "evidence_count": 7,
        "source_count": 3,
        "comment_count": 4,
        "root_candidate_count": 2,
    }


def test_needs_manual_snapshot_remains_manual_and_never_ready(tmp_path: Path) -> None:
    config = _config(tmp_path)
    _write_result(Path(config.results_dir), _v1_payload(status="needs_manual_snapshot"))
    _write_package(Path(config.export_root), "safe_package")

    payload = build_local_exchange_review_only_staging_response("provider_result.json", config)

    assert payload["status"] == "manual_review_required"
    assert payload["staging_candidate"]["review_status"] == "manual_review_required"
    assert payload["status"] != "ready_for_human_review"


@pytest.mark.parametrize("missing_field", ["provider_type", "safety_markers", "created_at"])
def test_missing_actual_provenance_or_safety_never_resolves_package(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    missing_field: str,
) -> None:
    config = _config(tmp_path)
    source = _v1_payload()
    source.pop(missing_field)
    _write_result(Path(config.results_dir), source)

    def fail_provider_reader(*args: object, **kwargs: object) -> object:
        raise AssertionError("missing actual provenance/safety must stop before package resolution")

    monkeypatch.setattr(
        "app.services.local_exchange_review_only_staging_bridge.read_private_collector_provider_result_metadata",
        fail_provider_reader,
    )

    payload = build_local_exchange_review_only_staging_response("provider_result.json", config)

    assert payload["status"] == "manual_review_required"
    assert payload["candidate_count"] == 0


@pytest.mark.parametrize(
    ("package_id", "relative_path"),
    [
        ("../escape", "../escape"),
        ("safe_package", "../safe_package"),
        ("safe_package", "other_package"),
        ("safe/package", "safe/package"),
    ],
)
def test_unsafe_or_ambiguous_package_reference_never_becomes_ready(
    tmp_path: Path,
    package_id: str,
    relative_path: str,
) -> None:
    config = _config(tmp_path)
    source = _v1_payload(package_name="safe_package")
    source["package_id"] = package_id
    source["package_relative_path"] = relative_path
    _write_result(Path(config.results_dir), source)

    payload = build_local_exchange_review_only_staging_response("provider_result.json", config)

    assert payload["status"] in {"manual_review_required", "blocked_path_escape"}
    assert payload["status"] != "ready_for_human_review"
    assert payload["candidate_count"] == 0


def test_forbidden_provider_metadata_blocks_before_package_resolution(tmp_path: Path) -> None:
    config = _config(tmp_path)
    source = _v1_payload()
    source["raw_author_id"] = "raw-id-must-not-cross"
    _write_result(Path(config.results_dir), source)

    payload = build_local_exchange_review_only_staging_response("provider_result.json", config)
    text = json.dumps(payload)

    assert payload["status"] == "blocked_safety"
    assert payload["candidate_count"] == 0
    assert "raw-id-must-not-cross" not in text


def test_forbidden_safe_package_metadata_blocks_privacy_without_raw_value(tmp_path: Path) -> None:
    config = _config(tmp_path)
    _write_result(Path(config.results_dir), _v1_payload(package_name="unsafe_package"))
    _write_package(Path(config.export_root), "unsafe_package", forbidden_metadata=True)

    payload = build_local_exchange_review_only_staging_response("provider_result.json", config)
    text = json.dumps(payload)

    assert payload["status"] == "blocked_privacy_issue"
    assert payload["candidate_count"] == 1
    assert "actual-token-must-not-cross-response" not in text


def test_no_evidence_or_row_like_file_is_opened_or_parsed(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config = _config(tmp_path)
    _write_result(Path(config.results_dir), _v1_payload())
    _write_package(Path(config.export_root), "safe_package")
    original_read_text = Path.read_text

    def guarded_read_text(self: Path, *args: object, **kwargs: object) -> str:
        if self.name in ROW_LIKE_FILES:
            raise AssertionError(f"row-like file must not be read: {self.name}")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    payload = build_local_exchange_review_only_staging_response("provider_result.json", config)

    assert payload["status"] == "ready_for_human_review"
    assert payload["safety_flags"]["full_evidence_rows_parsed"] is False


def test_bridge_is_nonpersistent_and_creates_no_runtime_state_files(tmp_path: Path) -> None:
    config = _config(tmp_path)
    _write_result(Path(config.results_dir), _v1_payload())
    _write_package(Path(config.export_root), "safe_package")
    before = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*") if path.is_file())

    payload = build_local_exchange_review_only_staging_response("provider_result.json", config)
    after = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*") if path.is_file())

    assert payload["candidate_count"] == 1
    assert after == before
    assert not list(tmp_path.rglob("*.sqlite"))
    assert not list(tmp_path.rglob("*.db"))


def test_response_contains_no_absolute_path_raw_payload_or_server_configuration(tmp_path: Path) -> None:
    payload = _ready_bridge(tmp_path)
    text = json.dumps(payload, ensure_ascii=False)

    _assert_safe_response(payload, tmp_path)
    assert "results_dir" not in text
    assert "export_root" not in text
    assert "provider_result_payload" not in text
    assert "package_relative_path" not in text


def test_existing_synthetic_list_and_exact_detail_endpoints_are_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(PRIMARY_GATE, "true")
    monkeypatch.delenv(BRIDGE_GATE, raising=False)

    list_payload = client.get(LIST_ROUTE).json()
    detail_payload = client.get(DETAIL_ROUTE).json()

    assert list_payload["schema"] == "internal_operator_review_only_staging_response_list_v0_1"
    assert list_payload["count"] == 1
    assert detail_payload["schema"] == "internal_operator_review_only_staging_response_v0_1"
    assert detail_payload["staging_candidate_id"] == "synthetic_review_staging_candidate"


def test_bridge_endpoint_is_get_only_internal_and_default_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(PRIMARY_GATE, raising=False)
    monkeypatch.delenv(BRIDGE_GATE, raising=False)
    route_path = "/api/v1/internal/staging/review-only/local-exchange/candidates/{result_file_name}"
    methods = {
        route.path: route.methods
        for route in _effective_app_routes()
        if route.path == route_path
    }

    assert set(methods) == {route_path}
    assert methods[route_path] == {"GET"}
    assert client.get(BRIDGE_ROUTE).json()["error_code"] == "route_disabled"
    assert client.post(BRIDGE_ROUTE).status_code == 405


def test_safe_response_declares_no_product_or_network_side_effects(tmp_path: Path) -> None:
    payload = _ready_bridge(tmp_path)

    assert payload["safety_flags"]["metadata_only"] is True
    for flag in [
        "persistent_staging_storage_created",
        "collector_run",
        "live_crawl",
        "browser_automation",
        "real_api_called",
        "real_llm_called",
        "url_fetching",
        "scraping",
        "full_evidence_rows_parsed",
        "evidence_layer_written",
        "production_case_created",
        "analysis_run_created",
        "public_output_generated",
        "external_delivery_performed",
    ]:
        assert payload["safety_flags"][flag] is False


def test_local_reader_runs_once_and_provider_reader_receives_in_memory_dict(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    import app.services.local_exchange_review_only_staging_bridge as bridge_module

    config = _config(tmp_path)
    _write_result(Path(config.results_dir), _v1_payload())
    _write_package(Path(config.export_root), "safe_package")
    actual_local_reader = bridge_module.read_local_exchange_provider_result_metadata
    actual_provider_reader = bridge_module.read_private_collector_provider_result_metadata
    calls = {"local": 0, "provider": 0}

    def counting_local_reader(*args: object, **kwargs: object) -> object:
        calls["local"] += 1
        return actual_local_reader(*args, **kwargs)

    def counting_provider_reader(provider_result: object, export_root: object) -> object:
        calls["provider"] += 1
        assert isinstance(provider_result, dict)
        return actual_provider_reader(provider_result, export_root)

    monkeypatch.setattr(bridge_module, "read_local_exchange_provider_result_metadata", counting_local_reader)
    monkeypatch.setattr(bridge_module, "read_private_collector_provider_result_metadata", counting_provider_reader)

    payload = build_local_exchange_review_only_staging_response("provider_result.json", config)

    assert payload["status"] == "ready_for_human_review"
    assert calls == {"local": 1, "provider": 1}


@pytest.mark.parametrize(
    ("source_status", "expected_status"),
    [
        ("blocked", "blocked_safety"),
        ("invalid_schema", "needs_fix_metadata_contract"),
        ("unsupported_contract", "needs_fix_metadata_contract"),
        ("failed", "blocked_safety"),
        ("manual_review_required", "manual_review_required"),
    ],
)
def test_nonready_source_statuses_never_upgrade_to_ready(
    tmp_path: Path,
    source_status: str,
    expected_status: str,
) -> None:
    config = _config(tmp_path)
    _write_result(Path(config.results_dir), _v1_payload(status=source_status))

    payload = build_local_exchange_review_only_staging_response("provider_result.json", config)

    assert payload["status"] == expected_status
    assert payload["status"] != "ready_for_human_review"
    assert payload["candidate_count"] == 0


def test_bridge_module_static_boundary_has_no_discovery_network_writer_or_database_code() -> None:
    module_path = Path("backend/app/services/local_exchange_review_only_staging_bridge.py")
    text = module_path.read_text(encoding="utf-8")

    for forbidden in [
        ".glob(",
        ".rglob(",
        ".iterdir(",
        "os.walk",
        "requests.",
        "httpx.",
        "sqlite",
        "FileResponse",
        "StreamingResponse",
        "subprocess",
    ]:
        assert forbidden not in text
