from __future__ import annotations

import ast
import importlib
import inspect
import json
import re
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Any

import pytest

from app.services.local_exchange_review_only_projection_bridge import (
    PROJECTION_FIELDS,
    build_disabled_local_exchange_review_only_projection,
    build_local_exchange_review_only_projection,
)
from app.services.private_collector_package_resolver import (
    GOVERNED_B05_METADATA_READ_PROFILE,
    GOVERNED_B05_READABLE_METADATA_FILES,
    REQUIRED_PACKAGE_METADATA_FILES,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
SERVICE_PATH = (
    REPO_ROOT
    / "backend/app/services/internal_alpha_local_exchange_review_projection.py"
)
ROUTE_PATH = REPO_ROOT / "backend/app/api/v1/routes/internal_alpha_review_console.py"
FRONTEND_API_PATH = REPO_ROOT / "frontend/src/api/sentigraphApi.js"
FRONTEND_PAGE_PATH = REPO_ROOT / "frontend/src/pages/InternalAlphaReviewConsole.jsx"

SERVICE_MODULE = "app.services.internal_alpha_local_exchange_review_projection"
ROUTE_MODULE = "app.api.v1.routes.internal_alpha_review_console"
SAFE_HANDLE = "helldivers2-psn-demo"
HISTORICAL_HANDLE = "helldivers2-psn-demo-20260614"
ORDERED_SAFE_HANDLES = (SAFE_HANDLE, HISTORICAL_HANDLE)
SYNTHETIC_RESULT_NAME = "synthetic-result.json"
HISTORICAL_RESULT_NAME = "provider_result_helldivers2-psn-demo_20260614_055754.json"
REAL_RESULT_NAME = "provider_result_helldivers2-psn-demo_20260720_123627.json"
ORDERED_DEFAULT_MAPPINGS = (
    (SAFE_HANDLE, REAL_RESULT_NAME),
    (HISTORICAL_HANDLE, HISTORICAL_RESULT_NAME),
)
ROUTE_PATH_TEMPLATE = (
    "/api/v1/internal/alpha/review-console/"
    "local-exchange-projections/{sample_handle}"
)

REGISTRY_SCHEMA = "sentigraph_internal_alpha_local_exchange_sample_registry_v0_1"
ROUTE_MODE = "internal_alpha_read_only_local_exchange_projection_operator"
CAPABILITY_LABEL = "b05_local_exchange_projection_read_only"
B05_GATE = "SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED"
SHARED_GATE = "SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED"
B01_ROUTE_GATE = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED"
B01_EXCHANGE_GATE = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED"
B03_PROJECTION_GATE = (
    "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED"
)
RESULTS_DIR_ENV = "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR"
EXPORT_ROOT_ENV = "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT"
ADAPTER_ID_ENV = "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID"

ALL_GATES = (
    SHARED_GATE,
    B05_GATE,
    B01_ROUTE_GATE,
    B01_EXCHANGE_GATE,
    B03_PROJECTION_GATE,
)
CONFIG_ENVS = (RESULTS_DIR_ENV, EXPORT_ROOT_ENV, ADAPTER_ID_ENV)
PREBUILDER_ERRORS = (
    "invalid_sample_handle",
    "b05_operator_surface_disabled",
    "unknown_sample_handle",
    "invalid_server_owned_configuration",
    "registry_route_mismatch",
)

EXPECTED_TRUE_FLAGS = (
    "metadata_only",
    "review_only",
    "human_review_required",
    "no_automatic_trust_upgrade",
)
EXPECTED_FALSE_FLAGS = (
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
EXPECTED_NULL_FIELDS = (
    "result_file_name",
    "upstream_schema",
    "upstream_status",
    "reader_status",
    "adapter_status",
    "provider_result_status",
    "package_resolution_status",
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
)

APP_MAIN_IMPORTS = 0
TEST_CLIENT_CREATIONS = 0


def _service() -> Any:
    return importlib.import_module(SERVICE_MODULE)


def _route_client() -> tuple[Any, Any]:
    global APP_MAIN_IMPORTS, TEST_CLIENT_CREATIONS

    from fastapi.testclient import TestClient

    APP_MAIN_IMPORTS += 1
    from app.main import app

    client = TestClient(app)
    TEST_CLIENT_CREATIONS += 1
    return importlib.import_module(ROUTE_MODULE), client


def _enabled_environment() -> dict[str, str]:
    environment = {gate: "true" for gate in ALL_GATES}
    environment.update(
        {
            RESULTS_DIR_ENV: "synthetic-results-root",
            EXPORT_ROOT_ENV: "synthetic-export-root",
            ADAPTER_ID_ENV: "synthetic_local_exchange_adapter",
        }
    )
    return environment


def _entry(
    service: Any,
    *,
    enabled: bool = True,
    route_mode: str = ROUTE_MODE,
    capability_label: str = CAPABILITY_LABEL,
) -> Any:
    return service.InternalAlphaLocalExchangeSampleRegistryEntry(
        sample_handle=SAFE_HANDLE,
        result_file_name=SYNTHETIC_RESULT_NAME,
        display_label="Synthetic sample",
        sample_role="synthetic_sample",
        is_default=True,
        enabled=enabled,
        catalog_order=0,
        route_mode=route_mode,
        capability_label=capability_label,
    )


def _registry(service: Any, **entry_overrides: object) -> Mapping[str, Any]:
    return service.build_internal_alpha_local_exchange_sample_registry(
        [_entry(service, **entry_overrides)]
    )


def _empty_registry(service: Any) -> Mapping[str, Any]:
    return service.build_internal_alpha_local_exchange_sample_registry()


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
        "staging_candidate_id": "synthetic_staging_candidate",
        "gate_result_id": "synthetic_gate_result",
        "analysis_request_id": "synthetic_analysis_request",
        "provider_result_id": "synthetic_provider_result",
        "package_name": "synthetic_package",
        "case_id_hint": "synthetic_case",
        "case_title_hint": "Synthetic review candidate",
        "validation_status": "passed",
        "evidence_count": 3,
        "source_count": 2,
        "comment_count": 4,
        "root_candidate_count": 1,
        "warning_count": 0,
        "error_count": 0,
        "review_status": "ready_for_human_review",
        "promotion_status": "promotion_required",
        "staging_status": "ready_for_human_review",
        "blockers": [],
        "warnings": ["selected_package_coverage_only"],
        "allowed_actions": ["inspect_metadata", "record_human_review_outcome"],
        "blocked_actions": ["automatic_promotion", "production_import"],
        "safety_flags": {
            "metadata_only": True,
            "full_evidence_rows_parsed": False,
        },
        "audit_refs": ["synthetic_fixture_only"],
        "gate_result": dict(gate_summary),
        "metadata_only": True,
        "path_exposed": False,
        "path_reference": None,
    }
    return {
        "schema": "internal_operator_review_only_staging_local_exchange_response_v0_1",
        "route_scope": "internal_operator_only",
        "access_scope": "review_only",
        "metadata_only": True,
        "review_only": True,
        "status": "ready_for_human_review",
        "error_code": None,
        "result_file_name": SYNTHETIC_RESULT_NAME,
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
        "warnings": [],
        "safety_flags": {
            "metadata_only": True,
            "review_only": True,
            "full_evidence_rows_read": False,
        },
    }


def _write_governed_b05_fixture(tmp_path: Path) -> dict[str, str]:
    results_dir = tmp_path / "results"
    results_dir.mkdir(parents=True)
    provider_result = {
        "schema": "sentigraph_provider_job_result_v1",
        "request_schema": "sentigraph_analysis_request_v1",
        "contract_version": "1.0",
        "adapter_id": "synthetic_local_exchange_adapter",
        "compatibility_status": "compatible",
        "status": "package_ready",
        "provider_result_id": "synthetic_provider_result",
        "provider_job_id": "synthetic_provider_job",
        "sentigraph_request_id": "synthetic_analysis_request",
        "provider_type": "private_collector_local_file",
        "package_contract": "sentigraph_evidence_export_v1",
        "package_id": "synthetic_package",
        "package_role": "review_ready_candidate",
        "package_index_ref": "package_index.json",
        "package_root_ref": "configured_export_root",
        "package_relative_path": "synthetic_package",
        "summary": {
            "evidence_items": 7,
            "sources": 3,
            "comment_samples": 4,
            "root_candidates": 3,
        },
        "validation_summary": {"status": "passed", "errors": 0, "warnings": 0},
        "coverage_note": "Selected package metadata counts only.",
        "safety_markers": {
            "raw_author_id_exported": False,
            "raw_author_name_exported": False,
            "profile_url_exported": False,
            "raw_author_id_removed": True,
            "raw_author_name_removed": True,
            "no_private_messages": True,
        },
        "created_at": "2026-08-07T00:00:00Z",
        "warnings": [],
        "errors": [],
        "nextAction": "review_package_metadata",
    }
    (results_dir / SYNTHETIC_RESULT_NAME).write_text(
        json.dumps(provider_result),
        encoding="utf-8",
    )

    export_root = tmp_path / "exports"
    package_dir = export_root / "synthetic_package"
    package_dir.mkdir(parents=True)
    for filename in REQUIRED_PACKAGE_METADATA_FILES:
        target = package_dir / filename
        if filename == "manifest.json":
            target.write_text(
                json.dumps(
                    {
                        "schema": "sentigraph_evidence_export_manifest_v1",
                        "package_name": "synthetic_package",
                        "raw_author_id_removed": True,
                        "raw_author_name_removed": True,
                        "profile_url_exported": False,
                    }
                ),
                encoding="utf-8",
            )
        elif filename == "validation_report.json":
            target.write_text(
                json.dumps({"status": "passed", "errors": 0, "warnings": 0}),
                encoding="utf-8",
            )
        elif filename.endswith(".json"):
            target.write_text("{}", encoding="utf-8")
        else:
            target.write_text("synthetic metadata only", encoding="utf-8")
    (package_dir / "package_index.json").write_text(
        json.dumps({"token": "package-index-body-must-not-be-opened"}),
        encoding="utf-8",
    )

    environment = {gate: "true" for gate in ALL_GATES}
    environment.update(
        {
            RESULTS_DIR_ENV: str(results_dir),
            EXPORT_ROOT_ENV: str(export_root),
            ADAPTER_ID_ENV: "synthetic_local_exchange_adapter",
        }
    )
    return environment


def _assert_exact_sentinel(payload: dict[str, Any], error_code: str) -> None:
    assert tuple(payload) == PROJECTION_FIELDS
    assert len(payload) == 52
    assert payload == build_disabled_local_exchange_review_only_projection(
        error_code,
        result_file_name=None,
    )
    assert payload["projection_schema"] == (
        "sentigraph_local_exchange_review_only_candidate_projection_v0_1"
    )
    assert payload["projection_version"] == "0.1"
    assert payload["projection_mode"] == "internal_governed_read_only_review_projection"
    assert payload["projection_status"] == "projection_unavailable"
    assert payload["projection_error_code"] == error_code
    assert payload["source_chain_boundary"] == (
        "local_exchange_review_only_staging_candidate_boundary"
    )
    assert payload["candidate_count"] == 0
    assert payload["warnings"] == []
    assert payload["blockers"] == [error_code]
    assert payload["allowed_actions"] == []
    assert payload["blocked_actions"] == []
    assert payload["candidate_persistence"] == "in_memory_only"
    for field in EXPECTED_NULL_FIELDS:
        assert payload[field] is None, field
    for field in EXPECTED_TRUE_FLAGS:
        assert payload[field] is True, field
    for field in EXPECTED_FALSE_FLAGS:
        assert payload[field] is False, field


class _ExplodingRegistry(Mapping[str, Any]):
    def __getitem__(self, key: str) -> Any:
        raise AssertionError(f"registry lookup forbidden for malformed handle: {key}")

    def __iter__(self) -> Any:
        raise AssertionError("registry iteration forbidden")

    def __len__(self) -> int:
        raise AssertionError("registry length lookup forbidden")

    def get(self, key: str, default: Any = None) -> Any:
        raise AssertionError(f"registry lookup forbidden for malformed handle: {key}")


def test_constants_default_registry_and_exact_b03_contract_are_frozen() -> None:
    service = _service()

    assert service.REGISTRY_SCHEMA == REGISTRY_SCHEMA
    assert service.ROUTE_MODE == ROUTE_MODE
    assert service.CAPABILITY_LABEL == CAPABILITY_LABEL
    assert service.B05_GATE_ENV == B05_GATE
    assert service.SAFE_SAMPLE_HANDLE_MAX_LENGTH == 64
    assert service.SAFE_SAMPLE_HANDLE_PATTERN == (
        r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$"
    )
    assert service.PROJECTION_FIELDS is PROJECTION_FIELDS
    assert len(PROJECTION_FIELDS) == 52
    service_source = SERVICE_PATH.read_text(encoding="utf-8")
    assert service_source.count(REAL_RESULT_NAME) == 1
    assert service_source.count(HISTORICAL_RESULT_NAME) == 1
    assert isinstance(service.DEFAULT_SAMPLE_REGISTRY, MappingProxyType)
    assert len(service.DEFAULT_SAMPLE_REGISTRY) == 2
    assert tuple(service.DEFAULT_SAMPLE_REGISTRY) == ORDERED_SAFE_HANDLES
    assert tuple(service.InternalAlphaLocalExchangeSampleRegistryEntry.__dataclass_fields__) == (
        "sample_handle",
        "result_file_name",
        "display_label",
        "sample_role",
        "is_default",
        "enabled",
        "catalog_order",
        "route_mode",
        "capability_label",
    )
    for sample_handle, result_file_name in ORDERED_DEFAULT_MAPPINGS:
        entry = service.DEFAULT_SAMPLE_REGISTRY[sample_handle]
        assert isinstance(
            entry,
            service.InternalAlphaLocalExchangeSampleRegistryEntry,
        )
        assert (
            entry.sample_handle,
            entry.result_file_name,
            entry.enabled,
            entry.route_mode,
            entry.capability_label,
        ) == (
            sample_handle,
            result_file_name,
            True,
            ROUTE_MODE,
            CAPABILITY_LABEL,
        )
    with pytest.raises(TypeError):
        service.DEFAULT_SAMPLE_REGISTRY[SAFE_HANDLE] = object()
    entry = service.DEFAULT_SAMPLE_REGISTRY[SAFE_HANDLE]
    with pytest.raises(ValueError, match="duplicate_sample_handle"):
        service.build_internal_alpha_local_exchange_sample_registry([entry, entry])


@pytest.mark.parametrize(
    "value",
    [
        "",
        "Uppercase",
        "-leading",
        "trailing-",
        "under_score",
        "period.value",
        "forward/slash",
        r"back\slash",
        "drive:value",
        "percent%2fvalue",
        "query?value",
        "fragment#value",
        "white space",
        "https://example.invalid",
        "..",
        "a" * 65,
        None,
        7,
    ],
)
def test_malformed_handle_matrix_is_rejected(value: object) -> None:
    service = _service()
    assert service.validate_internal_alpha_local_exchange_sample_handle(value) is False


def test_valid_handle_is_accepted_and_malformed_handle_never_looks_up_registry() -> None:
    service = _service()
    calls = {"staging": 0, "projection": 0}

    def fail_staging(*args: object, **kwargs: object) -> dict[str, Any]:
        calls["staging"] += 1
        raise AssertionError("B01 must not run")

    def fail_projection(*args: object, **kwargs: object) -> dict[str, Any]:
        calls["projection"] += 1
        raise AssertionError("B03 must not run")

    assert all(
        service.validate_internal_alpha_local_exchange_sample_handle(handle) is True
        for handle in ORDERED_SAFE_HANDLES
    )
    payload = service.build_internal_alpha_local_exchange_review_projection(
        "../invalid",
        registry=_ExplodingRegistry(),
        environment=_enabled_environment(),
        staging_builder=fail_staging,
        projection_builder=fail_projection,
    )

    _assert_exact_sentinel(payload, "invalid_sample_handle")
    assert calls == {"staging": 0, "projection": 0}


def test_registry_is_immutable_and_rejects_duplicates() -> None:
    service = _service()
    entry = _entry(service)
    registry = service.build_internal_alpha_local_exchange_sample_registry([entry])

    assert isinstance(registry, MappingProxyType)
    assert tuple(registry) == (SAFE_HANDLE,)
    assert registry[SAFE_HANDLE] is entry
    with pytest.raises(TypeError):
        registry[SAFE_HANDLE] = entry
    with pytest.raises(ValueError, match="duplicate_sample_handle"):
        service.build_internal_alpha_local_exchange_sample_registry([entry, entry])
    assert SYNTHETIC_RESULT_NAME not in SERVICE_PATH.read_text(encoding="utf-8")


@pytest.mark.parametrize("entry_enabled", [None, False])
def test_unknown_and_disabled_entries_are_indistinguishable(entry_enabled: bool | None) -> None:
    service = _service()
    registry = (
        _empty_registry(service)
        if entry_enabled is None
        else _registry(service, enabled=False)
    )

    payload = service.build_internal_alpha_local_exchange_review_projection(
        SAFE_HANDLE,
        registry=registry,
        environment=_enabled_environment(),
    )

    _assert_exact_sentinel(payload, "unknown_sample_handle")


@pytest.mark.parametrize(
    "overrides",
    [
        {"route_mode": "synthetic_wrong_route_mode"},
        {"capability_label": "synthetic_wrong_capability"},
    ],
)
def test_route_mode_or_capability_mismatch_fails_closed(overrides: dict[str, object]) -> None:
    service = _service()
    payload = service.build_internal_alpha_local_exchange_review_projection(
        SAFE_HANDLE,
        registry=_registry(service, **overrides),
        environment=_enabled_environment(),
    )
    _assert_exact_sentinel(payload, "registry_route_mismatch")


@pytest.mark.parametrize("disabled_gate", ALL_GATES)
def test_each_disabled_gate_stops_before_registry_or_builders(disabled_gate: str) -> None:
    service = _service()
    environment = _enabled_environment()
    environment.pop(disabled_gate)
    calls = {"staging": 0, "projection": 0}

    def fail_staging(*args: object, **kwargs: object) -> dict[str, Any]:
        calls["staging"] += 1
        raise AssertionError("B01 must not run while a gate is disabled")

    def fail_projection(*args: object, **kwargs: object) -> dict[str, Any]:
        calls["projection"] += 1
        raise AssertionError("B03 must not run while a gate is disabled")

    payload = service.build_internal_alpha_local_exchange_review_projection(
        SAFE_HANDLE,
        registry=_registry(service),
        environment=environment,
        staging_builder=fail_staging,
        projection_builder=fail_projection,
    )

    _assert_exact_sentinel(payload, "b05_operator_surface_disabled")
    assert calls == {"staging": 0, "projection": 0}


@pytest.mark.parametrize("config_env", CONFIG_ENVS)
@pytest.mark.parametrize("bad_value", ["", "   ", "x" * 2049])
def test_missing_blank_or_unbounded_server_configuration_stops_builders(
    config_env: str,
    bad_value: str,
) -> None:
    service = _service()
    environment = _enabled_environment()
    environment[config_env] = bad_value
    calls = {"staging": 0, "projection": 0}

    def fail_staging(*args: object, **kwargs: object) -> dict[str, Any]:
        calls["staging"] += 1
        raise AssertionError("B01 must not run with invalid server configuration")

    def fail_projection(*args: object, **kwargs: object) -> dict[str, Any]:
        calls["projection"] += 1
        raise AssertionError("B03 must not run with invalid server configuration")

    payload = service.build_internal_alpha_local_exchange_review_projection(
        SAFE_HANDLE,
        registry=_registry(service),
        environment=environment,
        staging_builder=fail_staging,
        projection_builder=fail_projection,
    )

    _assert_exact_sentinel(payload, "invalid_server_owned_configuration")
    assert calls == {"staging": 0, "projection": 0}


def test_every_prebuilder_failure_uses_the_existing_b03_disabled_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = _service()
    factory_calls: list[tuple[str, object]] = []

    def recording_factory(
        error_code: str,
        result_file_name: str | None = None,
    ) -> dict[str, Any]:
        factory_calls.append((error_code, result_file_name))
        return build_disabled_local_exchange_review_only_projection(
            error_code,
            result_file_name=result_file_name,
        )

    monkeypatch.setattr(
        service,
        "build_disabled_local_exchange_review_only_projection",
        recording_factory,
    )

    empty_registry = _empty_registry(service)
    scenarios = [
        ("invalid/handle", empty_registry, _enabled_environment()),
        (SAFE_HANDLE, empty_registry, {}),
        (SAFE_HANDLE, empty_registry, _enabled_environment()),
        (
            SAFE_HANDLE,
            _registry(service),
            {**_enabled_environment(), RESULTS_DIR_ENV: ""},
        ),
        (
            SAFE_HANDLE,
            _registry(service, route_mode="synthetic_wrong_route_mode"),
            _enabled_environment(),
        ),
    ]
    for handle, registry, environment in scenarios:
        service.build_internal_alpha_local_exchange_review_projection(
            handle,
            registry=registry,
            environment=environment,
        )

    assert factory_calls == [(error_code, None) for error_code in PREBUILDER_ERRORS]


def test_synthetic_ready_path_calls_b01_and_b03_once_and_returns_same_direct_object() -> None:
    service = _service()
    calls: dict[str, Any] = {
        "staging": 0,
        "projection": 0,
        "result_names": [],
        "config": None,
    }
    upstream = _ready_upstream()
    expected_projection = build_local_exchange_review_only_projection(
        SYNTHETIC_RESULT_NAME,
        upstream,
    )

    def fake_staging(result_file_name: str, config: Any) -> dict[str, Any]:
        calls["staging"] += 1
        calls["result_names"].append(result_file_name)
        calls["config"] = config
        return upstream

    def fake_projection(
        result_file_name: str,
        received_upstream: dict[str, Any],
    ) -> dict[str, Any]:
        calls["projection"] += 1
        calls["result_names"].append(result_file_name)
        assert received_upstream is upstream
        return expected_projection

    payload = service.build_internal_alpha_local_exchange_review_projection(
        SAFE_HANDLE,
        registry=_registry(service),
        environment=_enabled_environment(),
        staging_builder=fake_staging,
        projection_builder=fake_projection,
    )

    assert payload is expected_projection
    assert tuple(payload) == PROJECTION_FIELDS
    assert len(payload) == 52
    assert payload["projection_status"] == "ready_for_human_review"
    assert payload["projection_error_code"] is None
    assert calls["staging"] == 1
    assert calls["projection"] == 1
    assert calls["result_names"] == [SYNTHETIC_RESULT_NAME, SYNTHETIC_RESULT_NAME]
    assert calls["config"].results_dir == "synthetic-results-root"
    assert calls["config"].export_root == "synthetic-export-root"
    assert calls["config"].adapter_id == "synthetic_local_exchange_adapter"
    assert calls["config"].metadata_read_profile == GOVERNED_B05_METADATA_READ_PROFILE


def test_governed_b05_profile_opens_exact_five_metadata_files_and_returns_ready_projection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = _service()
    environment = _write_governed_b05_fixture(tmp_path)
    package_dir = tmp_path / "exports" / "synthetic_package"
    original_read_text = Path.read_text
    package_reads: list[str] = []

    def guarded_read_text(self: Path, *args: object, **kwargs: object) -> str:
        if self.parent == package_dir:
            if self.name == "package_index.json":
                raise AssertionError("governed B05 path must not open package_index.json")
            package_reads.append(self.name)
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    payload = service.build_internal_alpha_local_exchange_review_projection(
        SAFE_HANDLE,
        registry=_registry(service),
        environment=environment,
    )

    assert tuple(payload) == PROJECTION_FIELDS
    assert len(payload) == 52
    assert payload["projection_status"] == "ready_for_human_review"
    assert payload["projection_error_code"] is None
    assert payload["coverage_summary"] == {
        "evidence_count": 7,
        "source_count": 3,
        "comment_count": 4,
        "root_candidate_count": 3,
        "coverage_basis": "selected_package_metadata_counts_only",
        "full_web_coverage_claimed": False,
        "full_platform_coverage_claimed": False,
    }
    assert tuple(package_reads) == GOVERNED_B05_READABLE_METADATA_FILES


@pytest.mark.parametrize(
    ("sample_handle", "expected_result_name"),
    ORDERED_DEFAULT_MAPPINGS,
)
def test_each_default_registry_handle_uses_only_its_exact_basename_with_injected_fake_builders(
    sample_handle: str,
    expected_result_name: str,
) -> None:
    service = _service()
    calls: dict[str, Any] = {
        "staging": 0,
        "projection": 0,
        "result_names": [],
    }
    upstream = _ready_upstream()
    upstream["result_file_name"] = expected_result_name
    expected_projection = build_local_exchange_review_only_projection(
        expected_result_name,
        upstream,
    )

    def fake_staging(result_file_name: str, config: Any) -> dict[str, Any]:
        calls["staging"] += 1
        calls["result_names"].append(result_file_name)
        assert config.results_dir == "synthetic-results-root"
        assert config.export_root == "synthetic-export-root"
        assert config.adapter_id == "synthetic_local_exchange_adapter"
        return upstream

    def fake_projection(
        result_file_name: str,
        received_upstream: dict[str, Any],
    ) -> dict[str, Any]:
        calls["projection"] += 1
        calls["result_names"].append(result_file_name)
        assert received_upstream is upstream
        return expected_projection

    payload = service.build_internal_alpha_local_exchange_review_projection(
        sample_handle,
        environment=_enabled_environment(),
        staging_builder=fake_staging,
        projection_builder=fake_projection,
    )

    assert payload is expected_projection
    assert calls == {
        "staging": 1,
        "projection": 1,
        "result_names": [expected_result_name, expected_result_name],
    }


@pytest.mark.parametrize(
    "projection_case",
    ("reordered_complete", "missing_mutable_authority_granted"),
)
def test_reordered_or_incomplete_injected_projection_fails_closed(
    projection_case: str,
) -> None:
    service = _service()
    environment = _enabled_environment()
    upstream_path_marker = "synthetic/private/upstream/path"
    invalid_projection_marker = "invalid_projection_content_must_not_escape"
    upstream = _ready_upstream()
    upstream["synthetic_private_marker"] = upstream_path_marker
    calls: dict[str, Any] = {
        "staging": 0,
        "projection": 0,
        "result_names": [],
    }

    def fake_staging(result_file_name: str, config: Any) -> dict[str, Any]:
        calls["staging"] += 1
        calls["result_names"].append(result_file_name)
        assert result_file_name == REAL_RESULT_NAME
        assert config.results_dir == "synthetic-results-root"
        assert config.export_root == "synthetic-export-root"
        assert config.adapter_id == "synthetic_local_exchange_adapter"
        return upstream

    def fake_projection(
        result_file_name: str,
        received_upstream: dict[str, Any],
    ) -> dict[str, Any]:
        calls["projection"] += 1
        calls["result_names"].append(result_file_name)
        assert result_file_name == REAL_RESULT_NAME
        assert received_upstream is upstream

        ordered_items = [
            (field, invalid_projection_marker)
            for field in PROJECTION_FIELDS
        ]
        if projection_case == "reordered_complete":
            invalid_projection = dict(ordered_items[1:] + ordered_items[:1])
            assert len(invalid_projection) == 52
            assert set(invalid_projection) == set(PROJECTION_FIELDS)
            assert tuple(invalid_projection) != PROJECTION_FIELDS
            return invalid_projection

        missing_field = "mutable_authority_granted"
        invalid_projection = dict(
            (field, value)
            for field, value in ordered_items
            if field != missing_field
        )
        assert len(invalid_projection) == 51
        assert missing_field not in invalid_projection
        assert tuple(invalid_projection) == tuple(
            field for field in PROJECTION_FIELDS if field != missing_field
        )
        return invalid_projection

    payload = service.build_internal_alpha_local_exchange_review_projection(
        SAFE_HANDLE,
        environment=environment,
        staging_builder=fake_staging,
        projection_builder=fake_projection,
    )

    _assert_exact_sentinel(payload, "b05_projection_contract_mismatch")
    assert calls == {
        "staging": 1,
        "projection": 1,
        "result_names": [REAL_RESULT_NAME, REAL_RESULT_NAME],
    }
    rendered = repr(payload)
    for config_name in CONFIG_ENVS:
        assert environment[config_name] not in rendered
    assert upstream_path_marker not in rendered
    assert invalid_projection_marker not in rendered


def test_direct_b03_response_has_no_envelope_or_f10_persisted_record_fields() -> None:
    service = _service()
    payload = service.build_internal_alpha_local_exchange_review_projection(
        SAFE_HANDLE,
        registry=_registry(service),
        environment=_enabled_environment(),
        staging_builder=lambda *_: _ready_upstream(),
        projection_builder=build_local_exchange_review_only_projection,
    )

    assert tuple(payload) == PROJECTION_FIELDS
    for forbidden in (
        "response_schema",
        "projection",
        "sample_handle",
        "persisted_record_id",
        "attempt_reservation_id",
        "candidate_identity_digest",
        "input_safe_hash",
        "record_snapshot_digest",
    ):
        assert forbidden not in payload


def test_responses_never_expose_server_configuration_or_paths() -> None:
    service = _service()
    environment = _enabled_environment()
    payload = service.build_internal_alpha_local_exchange_review_projection(
        SAFE_HANDLE,
        registry=_empty_registry(service),
        environment=environment,
    )
    rendered = repr(payload)

    for value in environment.values():
        if value != "true":
            assert value not in rendered
    for field in (RESULTS_DIR_ENV, EXPORT_ROOT_ENV, ADAPTER_ID_ENV):
        assert field not in rendered
    assert payload["path_exposed"] is False
    assert payload["raw_metadata_exposed"] is False


def test_route_runtime_dependencies_remain_lazy_for_selected_service_tests() -> None:
    assert APP_MAIN_IMPORTS == 0
    assert TEST_CLIENT_CREATIONS == 0


def test_route_is_one_path_parameter_get_only_and_preserves_http_200_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    route, client = _route_client()
    signature = inspect.signature(
        route.get_internal_alpha_local_exchange_review_projection
    )
    assert tuple(signature.parameters) == ("sample_handle",)

    for gate in ALL_GATES:
        monkeypatch.delenv(gate, raising=False)
    response = client.get(ROUTE_PATH_TEMPLATE.format(sample_handle=SAFE_HANDLE))

    assert response.status_code == 200
    _assert_exact_sentinel(response.json(), "b05_operator_surface_disabled")


def test_route_returns_ready_projection_directly_with_http_200(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    route, client = _route_client()
    ready = build_local_exchange_review_only_projection(
        SYNTHETIC_RESULT_NAME,
        _ready_upstream(),
    )
    calls = 0

    def fake_service(sample_handle: object) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        assert sample_handle == SAFE_HANDLE
        return ready

    monkeypatch.setattr(
        route,
        "build_internal_alpha_local_exchange_review_projection",
        fake_service,
    )
    response = client.get(ROUTE_PATH_TEMPLATE.format(sample_handle=SAFE_HANDLE))

    assert response.status_code == 200
    assert response.json() == ready
    assert calls == 1


def test_route_source_has_exact_get_inventory_and_no_mutation_sibling() -> None:
    source = ROUTE_PATH.read_text(encoding="utf-8")
    assert '@router.get("/projections/{projection_id}")' in source
    assert '@router.get("/local-exchange-projections/{sample_handle}")' in source
    assert source.count('"/local-exchange-projections/{sample_handle}"') == 1
    for method in ("post", "put", "patch", "delete"):
        assert f'@router.{method}("/local-exchange-projections/' not in source


def test_service_static_boundary_has_no_side_effect_or_f10_dependencies() -> None:
    source = SERVICE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module)

    forbidden_import_fragments = (
        "sqlite",
        "database",
        "persistence",
        "requests",
        "httpx",
        "urllib",
        "socket",
        "provider",
        "collector",
        "openai",
        "llm",
        "subprocess",
        "playwright",
        "selenium",
        "governed_nonproduction",
        "f10",
    )
    assert all(
        fragment not in module.casefold()
        for module in imported_modules
        for fragment in forbidden_import_fragments
    )

    lowered = source.casefold()
    for forbidden_call in (
        "glob(",
        "rglob(",
        "os.walk",
        "listdir(",
        "scandir(",
        "open(",
        "latest",
        "fallback",
        "retry",
    ):
        assert forbidden_call not in lowered


def _javascript_function(source: str, function_name: str) -> str:
    marker = f"function {function_name}"
    start = source.index(marker)
    opening = source.index("{", start)
    depth = 0
    for index in range(opening, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]
    raise AssertionError(f"unterminated function: {function_name}")


def _local_exchange_page_branch(source: str) -> str:
    start_marker = "if (selectedReviewView === LOCAL_EXCHANGE_PROJECTION_REVIEW_VIEW)"
    end_marker = "const projection = routeState.projection"
    assert source.count(start_marker) == 1
    assert source.count(end_marker) == 1
    start = source.index(start_marker)
    end = source.index(end_marker, start)
    return source[start:end]


def test_frontend_api_has_exact_normalizers_and_one_get_per_helper_without_fallback() -> None:
    source = FRONTEND_API_PATH.read_text(encoding="utf-8")
    projection_helper = _javascript_function(source, "getInternalAlphaLocalExchangeProjection")
    projection_normalizer = _javascript_function(
        source,
        "normalizeInternalAlphaLocalExchangeProjection",
    )
    catalog_helper = _javascript_function(
        source,
        "getInternalAlphaLocalExchangeSampleCatalog",
    )
    catalog_normalizer = _javascript_function(
        source,
        "normalizeInternalAlphaLocalExchangeSampleCatalog",
    )

    assert projection_helper.count("apiClient.get(") == 1
    assert "encodeURIComponent(sampleHandle)" in projection_helper
    assert "INTERNAL_ALPHA_LOCAL_EXCHANGE_PROJECTIONS_SEGMENT" in projection_helper
    assert "normalizeInternalAlphaLocalExchangeProjection" in projection_helper
    assert catalog_helper.count("apiClient.get(") == 1
    assert "INTERNAL_ALPHA_LOCAL_EXCHANGE_SAMPLES_SEGMENT" in catalog_helper
    assert "normalizeInternalAlphaLocalExchangeSampleCatalog" in catalog_helper
    assert "INTERNAL_ALPHA_LOCAL_EXCHANGE_SAFE_SAMPLE_HANDLES" not in source
    for handle in ORDERED_SAFE_HANDLES:
        assert handle not in source
    for label in ("Current curated sample", "Accepted historical sample"):
        assert label not in source

    for helper in (projection_helper, catalog_helper):
        assert "apiClient.post" not in helper
        assert "apiClient.put" not in helper
        assert "apiClient.patch" not in helper
        assert "apiClient.delete" not in helper
        assert "retry" not in helper.casefold()
        assert "fallback" not in helper.casefold()

    assert "Object.keys" in projection_normalizer
    assert "Object.freeze" in projection_normalizer
    assert "frontend_projection_contract_mismatch" in projection_normalizer
    assert "Object.keys" in catalog_normalizer
    assert "Object.freeze" in catalog_normalizer
    assert "frontend_sample_catalog_contract_mismatch" in catalog_normalizer
    assert len(PROJECTION_FIELDS) == 52
    for field in PROJECTION_FIELDS:
        assert f"'{field}'" in source


def test_frontend_page_keeps_f10_default_and_uses_backend_catalog_for_cached_b05_state() -> None:
    source = FRONTEND_PAGE_PATH.read_text(encoding="utf-8")
    local_exchange_branch = _local_exchange_page_branch(source)

    assert "getInternalAlphaReviewConsoleProjection" in source
    assert "GOVERNED_REVIEW_CONSOLE_PROJECTION_ID" in source
    assert "internalAlphaLocalExchangeProjectionReview" in source
    assert "getInternalAlphaLocalExchangeSampleCatalog" in source
    assert source.count("getInternalAlphaLocalExchangeSampleCatalog(") == 1
    assert "localExchangeCatalogRequestStarted" in source
    assert "localExchangeCatalogState" in source
    assert "localExchangeCatalog.samples.map" in source
    assert "sample.sample_handle" in source
    assert "sample.display_label" in source
    assert "sample.sample_role" in source
    assert "sample.is_default" in source
    assert "sample.enabled" in source
    assert "LOCAL_EXCHANGE_SAMPLE_OPTIONS" not in source
    assert "INTERNAL_ALPHA_LOCAL_EXCHANGE_SAFE_SAMPLE_HANDLES" not in source
    for handle in ORDERED_SAFE_HANDLES:
        assert handle not in source
    for label in ("Current curated sample", "Accepted historical sample"):
        assert label not in source

    assert "selectedLocalExchangeSampleHandle" in source
    assert "localExchangeProjectionStateByHandle" in source
    assert "getInternalAlphaLocalExchangeProjection" in source
    assert source.count("getInternalAlphaLocalExchangeProjection(") == 1
    assert 'aria-label="Read-only local-exchange sample"' in source
    assert "requestedLocalExchangeHandles.current.has(selectedLocalExchangeSampleHandle)" in source
    assert "requestedLocalExchangeHandles.current.add(selectedLocalExchangeSampleHandle)" in source
    assert "getInternalAlphaLocalExchangeProjection(selectedLocalExchangeSampleHandle)" in source
    assert "localExchangeProjectionStateByHandle[selectedLocalExchangeSampleHandle]" in source
    assert "catalogPhase !== 'loaded'" in source
    assert "selectedLocalExchangeSample?.enabled" in source
    for request_phase in ("idle", "loading", "loaded", "unavailable", "bounded_error"):
        assert request_phase in source
    for projection_phase in (
        "manual_review_required",
        "blocked_upstream",
        "projection_unavailable",
        "ready_for_human_review",
    ):
        assert projection_phase in source
    for copy_line in (
        "Real metadata compatibility demonstrated for one approved sample.",
        "Read-only and human-review-only.",
        "Not a persisted governed record.",
        "Not trust approval.",
        "Not production readiness.",
        "Not full-web or full-platform coverage.",
    ):
        assert copy_line in source
    assert "result_file_name" not in source
    assert "localStorage" not in source
    assert "sessionStorage" not in source
    assert "console.log" not in source
    assert "retry" not in local_exchange_branch.casefold()
    assert "prefetch" not in local_exchange_branch.casefold()

def test_frontend_b05_surface_has_no_filename_path_config_or_mutation_controls() -> None:
    api_source = FRONTEND_API_PATH.read_text(encoding="utf-8")
    page_source = FRONTEND_PAGE_PATH.read_text(encoding="utf-8")
    helper = _javascript_function(api_source, "getInternalAlphaLocalExchangeProjection")
    local_exchange_branch = _local_exchange_page_branch(page_source)
    combined = "\n".join([helper, local_exchange_branch]).casefold()

    for forbidden in (
        "retry",
        "polling",
        "prefetch",
        "filenameinput",
        "pathinput",
        "rootinput",
        "adapterinput",
        "configinput",
        "<button",
        "<form",
        "approvewrite",
        "rejectprojection",
        "persistprojection",
        "promoteprojection",
        "publishprojection",
        "exportprojection",
        "decision-ledger",
    ):
        assert forbidden not in combined
