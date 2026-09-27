from __future__ import annotations

import ast
import builtins
from pathlib import Path
import socket

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

import app.api.v1.routes.internal_alpha_review_console as route_module
from app.services.internal_alpha_selected_item_lineage_projection import PROJECTION_FIELDS


PREFIX = "/api/v1/internal/alpha/review-console"
ENDPOINT = f"{PREFIX}/selected-item-lineage-fixture"
RESPONSE_FIELDS = (
    "response_schema", "route_mode", "projection", "safe_metadata_only",
    "human_review_required", "no_automatic_trust_upgrade", "synthetic_fixture_only",
    "live_persisted_record_connected", "actual_write_enabled", "production_object_enabled",
    "review_queue_runtime_enabled", "public_ready", "production_ready",
)
test_app = FastAPI()
test_app.include_router(route_module.router, prefix=PREFIX)
client = TestClient(test_app)


def set_gates(monkeypatch: pytest.MonkeyPatch, parent: str | None, dedicated: str | None) -> None:
    for flag, value in ((route_module.ENV_FLAG, parent), (route_module.SELECTED_ITEM_LINEAGE_FIXTURE_ENV_FLAG, dedicated)):
        if value is None:
            monkeypatch.delenv(flag, raising=False)
        else:
            monkeypatch.setenv(flag, value)


def assert_wrapper(payload: dict[str, object]) -> None:
    assert tuple(payload) == RESPONSE_FIELDS
    assert payload["response_schema"] == "sentigraph_internal_alpha_selected_item_lineage_fixture_response_v0_1"
    assert payload["route_mode"] == "disabled_by_default_internal_synthetic_fixture_only"
    for field in ("safe_metadata_only", "human_review_required", "no_automatic_trust_upgrade", "synthetic_fixture_only"):
        assert payload[field] is True
    for field in ("live_persisted_record_connected", "actual_write_enabled", "production_object_enabled", "review_queue_runtime_enabled", "public_ready", "production_ready"):
        assert payload[field] is False


@pytest.mark.parametrize("parent,dedicated", [
    (None, None), ("1", None), (None, "1"), ("true", "false"), ("false", "true"),
    ("1", "unknown"), ("unknown", "1"), ("0", "yes"), ("yes", "unexpected"),
])
def test_both_gates_are_required_before_fixture_or_builder(
    monkeypatch: pytest.MonkeyPatch, parent: str | None, dedicated: str | None,
) -> None:
    set_gates(monkeypatch, parent, dedicated)

    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("disabled gate reached fixture or builder")

    monkeypatch.setattr(route_module, "_selected_item_lineage_safe_fixture", forbidden)
    monkeypatch.setattr(route_module, "build_internal_alpha_selected_item_lineage_projection", forbidden)
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert_wrapper(response.json())
    assert response.json()["projection"] is None


@pytest.mark.parametrize("parent,dedicated", [("1", "1"), ("true", "yes"), ("yes", "true")])
def test_enabled_route_returns_only_exact_synthetic_scalars(
    monkeypatch: pytest.MonkeyPatch, parent: str, dedicated: str,
) -> None:
    set_gates(monkeypatch, parent, dedicated)
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    payload = response.json()
    assert_wrapper(payload)
    assert tuple(payload["projection"]) == PROJECTION_FIELDS
    assert payload["projection"]["persisted_selected_safe_hash"] == "3" * 64
    assert payload["projection"]["reviewed_batch_safe_hash"] == "1" * 64
    assert payload["projection"]["fresh_batch_safe_hash"] == "2" * 64
    assert all(type(value) in (str, bool) for value in payload["projection"].values())


def test_builder_error_is_bounded_and_does_not_leak_detail(monkeypatch: pytest.MonkeyPatch) -> None:
    set_gates(monkeypatch, "1", "1")

    def rejected(*args: object) -> None:
        raise ValueError("synthetic_forbidden_private_detail")

    monkeypatch.setattr(route_module, "build_internal_alpha_selected_item_lineage_projection", rejected)
    payload = client.get(ENDPOINT).json()
    assert_wrapper(payload)
    assert payload["projection"] is None
    assert "synthetic_forbidden_private_detail" not in str(payload)


def test_enabled_handler_performs_no_file_or_outbound_network_io(monkeypatch: pytest.MonkeyPatch) -> None:
    set_gates(monkeypatch, "1", "1")

    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("synthetic handler attempted I/O")

    monkeypatch.setattr(builtins, "open", forbidden)
    monkeypatch.setattr(Path, "open", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    payload = route_module.get_internal_alpha_selected_item_lineage_fixture()
    assert_wrapper(payload)
    assert payload["projection"] is not None


def test_route_handler_has_only_bounded_gate_fixture_builder_calls() -> None:
    tree = ast.parse(Path(route_module.__file__).read_text(encoding="utf-8"))
    handler = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "get_internal_alpha_selected_item_lineage_fixture")
    assert len(handler.decorator_list) == 1
    decorator = handler.decorator_list[0]
    assert isinstance(decorator, ast.Call)
    assert isinstance(decorator.func, ast.Attribute)
    assert isinstance(decorator.func.value, ast.Name)
    assert decorator.func.value.id == "router"
    assert decorator.func.attr == "get"
    assert len(decorator.args) == 1
    assert isinstance(decorator.args[0], ast.Constant)
    assert decorator.args[0].value == "/selected-item-lineage-fixture"
    assert decorator.keywords == []

    body = ast.Module(body=handler.body, type_ignores=[])
    calls = {node.func.id for node in ast.walk(body) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    assert calls == {"_route_enabled", "_selected_item_lineage_fixture_enabled", "dict", "build_internal_alpha_selected_item_lineage_projection", "_selected_item_lineage_safe_fixture"}
    assert not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) for node in ast.walk(body))


def test_router_is_get_only_internal_and_existing_projection_remains_separate(monkeypatch: pytest.MonkeyPatch) -> None:
    routes = {route.path: route.methods for route in route_module.router.routes}
    assert "/selected-item-lineage-fixture" in routes
    assert all(methods == {"GET"} for methods in routes.values())
    assert all(f"{PREFIX}{path}".startswith(f"{PREFIX}/") for path in routes)
    set_gates(monkeypatch, None, "1")
    old_payload = client.get(f"{PREFIX}/projections/internal-alpha-safe-projection-fixture").json()
    assert old_payload["error"] == "route_disabled"
    assert "persisted_selected_safe_hash" not in old_payload
