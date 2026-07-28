from __future__ import annotations

import ast
import importlib
from collections import OrderedDict
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
from typing import Any

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
CATALOG_SERVICE_PATH = REPO_ROOT / "backend/app/services/internal_alpha_local_exchange_sample_catalog.py"
ROUTE_PATH = REPO_ROOT / "backend/app/api/v1/routes/internal_alpha_review_console.py"
FRONTEND_API_PATH = REPO_ROOT / "frontend/src/api/sentigraphApi.js"
FRONTEND_PAGE_PATH = REPO_ROOT / "frontend/src/pages/InternalAlphaReviewConsole.jsx"

REGISTRY_MODULE = "app.services.internal_alpha_local_exchange_review_projection"
CATALOG_MODULE = "app.services.internal_alpha_local_exchange_sample_catalog"
ROUTE_MODULE = "app.api.v1.routes.internal_alpha_review_console"
CATALOG_ROUTE = "/local-exchange-samples"
CATALOG_SCHEMA = "sentigraph_internal_alpha_local_exchange_sample_catalog_v0_1"
CATALOG_MODE = "internal_alpha_read_only_local_exchange_sample_catalog"
CATALOG_FIELDS = (
    "schema", "version", "mode", "status", "sample_count",
    "default_sample_handle", "samples", "read_only",
    "human_review_required", "production_ready", "mutable_authority_granted",
)
SAMPLE_FIELDS = (
    "sample_handle", "display_label", "sample_role",
    "is_default", "enabled", "catalog_order",
)
EXPECTED_SAMPLES = (
    ("helldivers2-psn-demo", "Current curated sample", "current_curated", True, True, 0),
    ("helldivers2-psn-demo-20260614", "Accepted historical sample", "accepted_historical", False, True, 1),
)
PRIVATE_TERMS = (
    "result_file_name", "package_name", "results_dir", "export_root",
    "adapter_id", "receipt", "raw_metadata", "evidence_items",
    "source_manifest", "collection_log",
)


def _registry_service() -> Any:
    return importlib.import_module(REGISTRY_MODULE)


def _catalog_service() -> Any:
    return importlib.import_module(CATALOG_MODULE)


def _route() -> Any:
    return importlib.import_module(ROUTE_MODULE)


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


def test_default_registry_owns_exact_safe_catalog_metadata() -> None:
    service = _registry_service()
    entries = tuple(service.DEFAULT_SAMPLE_REGISTRY.values())
    assert isinstance(service.DEFAULT_SAMPLE_REGISTRY, MappingProxyType)
    assert tuple(
        (entry.sample_handle, entry.display_label, entry.sample_role,
         entry.is_default, entry.enabled, entry.catalog_order)
        for entry in entries
    ) == EXPECTED_SAMPLES


def test_catalog_is_deterministic_safe_and_registry_derived() -> None:
    service = _catalog_service()
    catalog = service.build_internal_alpha_local_exchange_sample_catalog()
    assert tuple(catalog) == CATALOG_FIELDS
    assert catalog["schema"] == CATALOG_SCHEMA
    assert catalog["version"] == "0.1"
    assert catalog["mode"] == CATALOG_MODE
    assert catalog["status"] == "ready"
    assert catalog["sample_count"] == 2
    assert catalog["default_sample_handle"] == EXPECTED_SAMPLES[0][0]
    assert catalog["read_only"] is True
    assert catalog["human_review_required"] is True
    assert catalog["production_ready"] is False
    assert catalog["mutable_authority_granted"] is False
    assert tuple(tuple(sample) for sample in catalog["samples"]) == (SAMPLE_FIELDS, SAMPLE_FIELDS)
    assert tuple(
        tuple(sample[field] for field in SAMPLE_FIELDS) for sample in catalog["samples"]
    ) == EXPECTED_SAMPLES
    assert catalog == service.build_internal_alpha_local_exchange_sample_catalog()
    serialized = repr(catalog).casefold()
    for private_term in PRIVATE_TERMS:
        assert private_term not in serialized


def test_catalog_does_not_invoke_artifact_builders(monkeypatch: pytest.MonkeyPatch) -> None:
    registry_service = _registry_service()
    catalog_service = _catalog_service()

    def forbidden(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("artifact_builder_invoked")

    monkeypatch.setattr(registry_service, "build_local_exchange_review_only_staging_response", forbidden)
    monkeypatch.setattr(registry_service, "build_local_exchange_review_only_projection", forbidden)
    assert catalog_service.build_internal_alpha_local_exchange_sample_catalog()["status"] == "ready"


def _invalid_registry(
    first: dict[str, object],
    second: dict[str, object],
    keys: tuple[str, str] | None = None,
) -> OrderedDict[str, Any]:
    entries = tuple(_registry_service().DEFAULT_SAMPLE_REGISTRY.values())
    changed = (replace(entries[0], **first), replace(entries[1], **second))
    mapping_keys = keys or (changed[0].sample_handle, changed[1].sample_handle)
    return OrderedDict(zip(mapping_keys, changed, strict=True))


@pytest.mark.parametrize(
    "registry",
    (
        _invalid_registry({"sample_handle": "duplicate"}, {"sample_handle": "duplicate"}, ("first", "second")),
        _invalid_registry({"display_label": "../unsafe"}, {}),
        _invalid_registry({"sample_role": "Unsafe Role"}, {}),
        _invalid_registry({"is_default": False}, {"is_default": False}),
        _invalid_registry({"is_default": True}, {"is_default": True}),
        _invalid_registry({"enabled": False}, {}),
        _invalid_registry({"catalog_order": 1}, {"catalog_order": 0}),
    ),
)
def test_invalid_registry_invariants_fail_closed(registry: OrderedDict[str, Any]) -> None:
    with pytest.raises(ValueError, match="invalid_sample_catalog"):
        _catalog_service().build_internal_alpha_local_exchange_sample_catalog(registry)


def test_catalog_route_reuses_internal_gate_and_stays_get_only(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    route = _route()
    catalog_service = _catalog_service()
    source = ROUTE_PATH.read_text(encoding="utf-8")
    assert f'@router.get("{CATALOG_ROUTE}")' in source
    assert source.count(f'"{CATALOG_ROUTE}"') == 1
    for method in ("post", "put", "patch", "delete"):
        assert f'@router.{method}("{CATALOG_ROUTE}")' not in source

    monkeypatch.setattr(route, "_route_enabled", lambda: False)
    disabled = route.get_internal_alpha_local_exchange_sample_catalog()
    assert tuple(disabled) == CATALOG_FIELDS
    assert disabled["status"] == "unavailable"
    assert disabled["sample_count"] == 0
    assert disabled["samples"] == []
    assert disabled["read_only"] is True
    assert disabled["production_ready"] is False

    monkeypatch.setattr(route, "_route_enabled", lambda: True)
    ready = route.get_internal_alpha_local_exchange_sample_catalog()
    assert ready == catalog_service.build_internal_alpha_local_exchange_sample_catalog()


def test_in_process_catalog_route_is_gated_and_never_reads_artifacts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from fastapi.testclient import TestClient

    from app.main import app

    registry_service = _registry_service()

    def forbidden(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("artifact_builder_invoked")

    monkeypatch.setattr(registry_service, "build_local_exchange_review_only_staging_response", forbidden)
    monkeypatch.setattr(registry_service, "build_local_exchange_review_only_projection", forbidden)
    client = TestClient(app)
    path = "/api/v1/internal/alpha/review-console/local-exchange-samples"

    monkeypatch.delenv("SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED", raising=False)
    disabled = client.get(path)
    assert disabled.status_code == 200
    assert disabled.json()["status"] == "unavailable"

    monkeypatch.setenv("SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED", "true")
    ready = client.get(path)
    assert ready.status_code == 200
    assert ready.json()["status"] == "ready"
    assert ready.json()["sample_count"] == 2


def test_catalog_service_has_no_io_network_or_mutation_dependencies() -> None:
    source = CATALOG_SERVICE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    for forbidden in (
        "pathlib", "os", "sqlite", "database", "persistence", "requests",
        "httpx", "urllib", "socket", "subprocess", "provider", "collector",
    ):
        assert all(forbidden not in module.casefold() for module in modules)
    lowered = source.casefold()
    for forbidden_call in (
        "open(", "read_text(", "read_bytes(", "write_text(", "write_bytes(",
        "glob(", "rglob(", "listdir(", "scandir(",
    ):
        assert forbidden_call not in lowered


def test_frontend_catalog_helper_is_strict_single_get_without_fallback_catalog() -> None:
    source = FRONTEND_API_PATH.read_text(encoding="utf-8")
    helper = _javascript_function(source, "getInternalAlphaLocalExchangeSampleCatalog")
    normalizer = _javascript_function(source, "normalizeInternalAlphaLocalExchangeSampleCatalog")
    assert helper.count("apiClient.get(") == 1
    assert "INTERNAL_ALPHA_LOCAL_EXCHANGE_SAMPLES_SEGMENT" in helper
    assert "normalizeInternalAlphaLocalExchangeSampleCatalog(data)" in helper
    assert not any(method in helper for method in ("apiClient.post", "apiClient.put", "apiClient.patch", "apiClient.delete"))
    assert "retry" not in helper.casefold()
    assert "fallback" not in helper.casefold()
    assert "Object.keys" in normalizer
    assert "Object.freeze" in normalizer
    assert "frontend_sample_catalog_contract_mismatch" in normalizer
    assert CATALOG_SCHEMA in normalizer
    assert CATALOG_MODE in normalizer
    for field in CATALOG_FIELDS + SAMPLE_FIELDS:
        assert f"'{field}'" in source
    assert "INTERNAL_ALPHA_LOCAL_EXCHANGE_SAFE_SAMPLE_HANDLES" not in source
    for handle, label, *_rest in EXPECTED_SAMPLES:
        assert handle not in source
        assert label not in source


def test_frontend_page_consumes_catalog_as_single_runtime_source() -> None:
    source = FRONTEND_PAGE_PATH.read_text(encoding="utf-8")
    assert "getInternalAlphaLocalExchangeSampleCatalog" in source
    assert source.count("getInternalAlphaLocalExchangeSampleCatalog(") == 1
    for marker in (
        "localExchangeCatalogRequestStarted", "localExchangeCatalogState",
        "localExchangeCatalog.samples.map", "sample.display_label", "sample.sample_handle",
        "sample.enabled", "sample.is_default", "selectedLocalExchangeSample?.enabled",
        "catalogPhase !== 'loaded'",
    ):
        assert marker in source
    assert "LOCAL_EXCHANGE_SAMPLE_OPTIONS" not in source
    assert "INTERNAL_ALPHA_LOCAL_EXCHANGE_SAFE_SAMPLE_HANDLES" not in source
    for handle, label, *_rest in EXPECTED_SAMPLES:
        assert handle not in source
        assert label not in source
    assert "requestedLocalExchangeHandles.current.has(selectedLocalExchangeSampleHandle)" in source
    assert "requestedLocalExchangeHandles.current.add(selectedLocalExchangeSampleHandle)" in source
    assert "getInternalAlphaLocalExchangeProjection(selectedLocalExchangeSampleHandle)" in source
    assert "localExchangeProjectionStateByHandle[selectedLocalExchangeSampleHandle]" in source
    for forbidden in ("localStorage", "sessionStorage", "retry", "prefetch", "polling"):
        assert forbidden.casefold() not in source.casefold()
