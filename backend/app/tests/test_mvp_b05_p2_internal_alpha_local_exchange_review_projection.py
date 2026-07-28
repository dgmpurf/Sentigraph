from __future__ import annotations

import ast
import importlib
import inspect
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
        enabled=enabled,
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
        "enabled",
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


def test_frontend_api_has_exact_normalizer_and_one_encoded_get_without_fallback() -> None:
    source = FRONTEND_API_PATH.read_text(encoding="utf-8")
    helper = _javascript_function(source, "getInternalAlphaLocalExchangeProjection")
    normalizer = _javascript_function(
        source,
        "normalizeInternalAlphaLocalExchangeProjection",
    )

    safe_handles_start = source.index(
        "export const INTERNAL_ALPHA_LOCAL_EXCHANGE_SAFE_SAMPLE_HANDLES"
    )
    safe_handles_end = source.index("])", safe_handles_start)
    safe_handles_block = source[safe_handles_start:safe_handles_end]
    assert re.findall(r"'([a-z0-9-]+)'", safe_handles_block) == list(
        ORDERED_SAFE_HANDLES
    )
    assert helper.count("apiClient.get(") == 1
    assert "encodeURIComponent(sampleHandle)" in helper
    assert "INTERNAL_ALPHA_LOCAL_EXCHANGE_PROJECTIONS_SEGMENT" in helper
    assert (
        "const INTERNAL_ALPHA_LOCAL_EXCHANGE_PROJECTIONS_SEGMENT = "
        "'local-exchange-projections'"
    ) in source
    assert "normalizeInternalAlphaLocalExchangeProjection" in helper
    assert "?" not in helper
    assert "apiClient.post" not in helper
    assert "apiClient.put" not in helper
    assert "apiClient.patch" not in helper
    assert "apiClient.delete" not in helper
    assert "retry" not in helper.casefold()
    assert "fallback" not in helper.casefold()
    assert "projectionId" not in helper

    assert "Object.keys" in normalizer
    assert "Object.freeze" in normalizer
    assert "frontend_projection_contract_mismatch" in normalizer
    assert len(PROJECTION_FIELDS) == 52
    for field in PROJECTION_FIELDS:
        assert f"'{field}'" in source


def test_frontend_page_keeps_f10_default_and_adds_dual_sample_cached_b05_state_view() -> None:
    source = FRONTEND_PAGE_PATH.read_text(encoding="utf-8")

    assert "getInternalAlphaReviewConsoleProjection" in source
    assert "GOVERNED_REVIEW_CONSOLE_PROJECTION_ID" in source
    assert "internalAlphaLocalExchangeProjectionReview" in source
    assert "selectedLocalExchangeSampleHandle" in source
    assert "localExchangeProjectionStateByHandle" in source
    assert "getInternalAlphaLocalExchangeProjection" in source
    assert source.count("getInternalAlphaLocalExchangeProjection(") == 1
    assert "LOCAL_EXCHANGE_SAMPLE_OPTIONS" in source
    assert "Current curated sample" in source
    assert "Accepted historical sample" in source
    assert 'aria-label="Read-only local-exchange sample"' in source
    local_view_start = source.index(
        "if (selectedReviewView === LOCAL_EXCHANGE_PROJECTION_REVIEW_VIEW)"
    )
    sample_selector_start = source.index(
        'aria-label="Read-only local-exchange sample"'
    )
    assert sample_selector_start > local_view_start
    assert "INTERNAL_ALPHA_LOCAL_EXCHANGE_SAFE_SAMPLE_HANDLES[0]" in source
    assert "value: INTERNAL_ALPHA_LOCAL_EXCHANGE_SAFE_SAMPLE_HANDLES[0]" in source
    assert "value: INTERNAL_ALPHA_LOCAL_EXCHANGE_SAFE_SAMPLE_HANDLES[1]" in source
    assert "requestedLocalExchangeHandles.current.has(selectedLocalExchangeSampleHandle)" in source
    assert "requestedLocalExchangeHandles.current.add(selectedLocalExchangeSampleHandle)" in source
    assert "getInternalAlphaLocalExchangeProjection(selectedLocalExchangeSampleHandle)" in source
    assert "[selectedReviewView, selectedLocalExchangeSampleHandle]" in source
    assert "localExchangeProjectionStateByHandle[selectedLocalExchangeSampleHandle]" in source
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
    assert "retry" not in source.casefold()
    assert "prefetch" not in source.casefold()


def test_frontend_b05_surface_has_no_filename_path_config_or_mutation_controls() -> None:
    api_source = FRONTEND_API_PATH.read_text(encoding="utf-8")
    page_source = FRONTEND_PAGE_PATH.read_text(encoding="utf-8")
    helper = _javascript_function(api_source, "getInternalAlphaLocalExchangeProjection")
    combined = "\n".join([helper, page_source]).casefold()

    for forbidden in (
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
