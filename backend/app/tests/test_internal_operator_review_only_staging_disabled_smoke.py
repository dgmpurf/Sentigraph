from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

ENV_FLAG = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED"
BRIDGE_ENV_FLAG = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED"
LIST_ROUTE = "/api/v1/internal/staging/review-only/candidates"
DETAIL_ROUTE = "/api/v1/internal/staging/review-only/candidates/synthetic_review_staging_candidate"
BRIDGE_ROUTE = "/api/v1/internal/staging/review-only/local-exchange/candidates/provider_result.json"
BRIDGE_ROUTE_TEMPLATE = "/api/v1/internal/staging/review-only/local-exchange/candidates/{result_file_name}"

DISABLED_VALUES = [None, "", "false", "0", "random", "TRUE-ish", "enabled"]

FORBIDDEN_DISABLED_RESPONSE_TERMS = [
    "raw_author_id",
    "raw_author_name",
    "raw_comment_dump",
    "token",
    "cookie",
    "session",
    "password",
    "api_key",
    "secret",
    "evidence_items.jsonl",
    "evidence_items.csv",
    "profile_url",
    "response_text",
    "generated_public_message",
]

STATIC_FORBIDDEN_ROUTE_TERMS = [
    "FileResponse",
    "StreamingResponse",
    "zipfile",
    "public_url",
    "signed_url",
    "external_delivery",
    "send_email",
    "object_storage",
    "portal_publication",
    "evidence_items.jsonl",
    "evidence_items.csv",
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
]


def _set_env(monkeypatch: pytest.MonkeyPatch, value: str | None) -> None:
    if value is None:
        monkeypatch.delenv(ENV_FLAG, raising=False)
    else:
        monkeypatch.setenv(ENV_FLAG, value)


def _payload_text(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False).lower()


def _assert_disabled_response(payload: dict) -> None:
    assert payload["schema"] == "internal_operator_review_only_staging_error_v0_1"
    assert payload["route_scope"] == "internal_operator"
    assert payload["access_scope"] == "local_or_disabled_by_default"
    assert payload["metadata_only"] is True
    assert payload["review_only"] is True
    assert payload["error_code"] == "route_disabled"
    assert "route_disabled" in payload["blockers"]
    assert payload["path_exposed"] is False
    assert payload["raw_metadata_exposed"] is False


@pytest.mark.parametrize("env_value", DISABLED_VALUES)
@pytest.mark.parametrize("route", [LIST_ROUTE, DETAIL_ROUTE])
def test_internal_operator_routes_return_route_disabled_for_default_and_falsey_env_values(
    monkeypatch: pytest.MonkeyPatch,
    env_value: str | None,
    route: str,
) -> None:
    _set_env(monkeypatch, env_value)

    response = client.get(route)
    payload = response.json()

    assert response.status_code == 200
    _assert_disabled_response(payload)


@pytest.mark.parametrize("route", [LIST_ROUTE, DETAIL_ROUTE])
def test_disabled_response_has_no_paths_raw_metadata_or_secret_markers(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    route: str,
) -> None:
    monkeypatch.delenv(ENV_FLAG, raising=False)

    payload = client.get(route).json()
    text = _payload_text(payload)

    assert str(tmp_path).lower() not in text
    assert "g:\\" not in text
    assert "c:\\users" not in text
    assert "raw_metadata" not in text.replace("raw_metadata_exposed", "")
    for forbidden in FORBIDDEN_DISABLED_RESPONSE_TERMS:
        assert forbidden not in text


def test_primary_disabled_gate_blocks_local_exchange_bridge_before_file_access(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.delenv(ENV_FLAG, raising=False)
    monkeypatch.setenv(BRIDGE_ENV_FLAG, "true")

    payload = client.get(BRIDGE_ROUTE).json()
    text = _payload_text(payload)

    assert payload["schema"] == "internal_operator_review_only_staging_local_exchange_response_v0_1"
    assert payload["error_code"] == "route_disabled"
    assert payload["reader_status"] == "not_called"
    assert payload["candidate_count"] == 0
    assert str(tmp_path).lower() not in text


def test_disabled_routes_do_not_open_evidence_item_files_with_path_or_builtin_open(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(ENV_FLAG, raising=False)
    original_path_open = Path.open
    original_builtin_open = builtins.open

    def guarded_path_open(self: Path, *args, **kwargs):
        if self.name in {"evidence_items.jsonl", "evidence_items.csv"}:
            raise AssertionError(f"{self.name} must not be opened")
        return original_path_open(self, *args, **kwargs)

    def guarded_builtin_open(file, *args, **kwargs):
        if Path(str(file)).name in {"evidence_items.jsonl", "evidence_items.csv"}:
            raise AssertionError(f"{file} must not be opened")
        return original_builtin_open(file, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_path_open)
    monkeypatch.setattr(builtins, "open", guarded_builtin_open)

    assert client.get(LIST_ROUTE).json()["error_code"] == "route_disabled"
    assert client.get(DETAIL_ROUTE).json()["error_code"] == "route_disabled"


def test_route_family_is_get_only_and_internal_only() -> None:
    route_methods = {
        route.path: route.methods
        for route in app.routes
        if "staging/review-only" in getattr(route, "path", "")
    }

    assert set(route_methods) == {
        LIST_ROUTE,
        DETAIL_ROUTE.replace("synthetic_review_staging_candidate", "{staging_candidate_id}"),
        BRIDGE_ROUTE_TEMPLATE,
    }
    for path, methods in route_methods.items():
        assert path.startswith("/api/v1/internal/")
        assert "GET" in methods
        assert "POST" not in methods
        assert "PUT" not in methods
        assert "PATCH" not in methods
        assert "DELETE" not in methods


def test_no_public_c_end_or_b_end_alias_routes_exist_for_staging_family() -> None:
    aliases = [
        route.path
        for route in app.routes
        if "staging/review-only" in getattr(route, "path", "")
        and not getattr(route, "path", "").startswith("/api/v1/internal/")
    ]

    assert aliases == []


def test_route_module_static_scan_has_no_delivery_file_response_or_forbidden_behavior() -> None:
    route_module = Path("backend/app/api/v1/routes/internal_operator_review_only_staging.py")
    text = route_module.read_text(encoding="utf-8")

    for forbidden in STATIC_FORBIDDEN_ROUTE_TERMS:
        assert forbidden not in text


def test_disabled_smoke_creates_no_runtime_or_staging_files(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv(ENV_FLAG, raising=False)

    client.get(LIST_ROUTE)
    client.get(DETAIL_ROUTE)
    client.get(BRIDGE_ROUTE)

    assert not list(tmp_path.rglob("review_only_staging*.json"))
    assert not list(tmp_path.rglob("staging_candidate*.json"))
    assert not list(tmp_path.rglob("review_queue*.json"))
    assert not list(tmp_path.rglob("analysis_run*.json"))
    assert not list(tmp_path.rglob("*.sqlite"))
    assert not list(tmp_path.rglob("*.db"))
