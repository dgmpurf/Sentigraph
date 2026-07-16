from __future__ import annotations

import builtins
import json
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

ENV_FLAG = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED"
BRIDGE_ENV_FLAG = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED"
SYNTHETIC_CANDIDATE_ID = "synthetic_review_staging_candidate"
LIST_ROUTE = "/api/v1/internal/staging/review-only/candidates"
DETAIL_ROUTE = f"{LIST_ROUTE}/{SYNTHETIC_CANDIDATE_ID}"
UNKNOWN_ROUTE = f"{LIST_ROUTE}/unknown_candidate"
BRIDGE_ROUTE = "/api/v1/internal/staging/review-only/local-exchange/candidates/provider_result.json"
BRIDGE_ROUTE_TEMPLATE = "/api/v1/internal/staging/review-only/local-exchange/candidates/{result_file_name}"
PROJECTION_ROUTE_TEMPLATE = "/api/v1/internal/staging/review-only/local-exchange/projections/{result_file_name}"

ENABLED_VALUES = ["1", "true", "yes"]

ALLOWED_ACTIONS = {
    "continue_review",
    "request_more_metadata",
    "mark_manual_review_required",
    "reject_package",
    "block_privacy_issue",
    "request_future_evidence_preview_gate",
    "request_future_dedup_gate",
    "request_future_promotion_gate",
}

BLOCKED_ACTIONS = {
    "approve_production_evidence",
    "create_production_case",
    "start_analysis_run",
    "generate_report",
    "generate_public_event",
    "generate_public_response",
    "publish",
    "send",
    "post",
    "execute",
    "target_individuals",
}

REQUIRED_FALSE_SAFETY_FLAGS = [
    "collector_run",
    "live_crawl",
    "real_api_called",
    "real_llm_called",
    "url_fetching",
    "scraping",
    "full_evidence_rows_parsed",
    "evidence_items_jsonl_parsed",
    "evidence_items_csv_parsed",
    "raw_comments_printed",
    "raw_author_identifiers_printed",
    "secrets_read",
    "evidence_layer_written",
    "production_case_created",
    "analysis_run_created",
    "b_end_report_runtime_generated",
    "sandbox_public_event_runtime_generated",
    "persistent_staging_storage_created",
]

FORBIDDEN_KEYS = {
    "raw_evidence_rows",
    "raw_comments",
    "raw_comment_dump",
    "raw_author_id",
    "raw_author_ids",
    "raw_author_name",
    "raw_author_names",
    "author_id",
    "author_name",
    "profile_url",
    "private_message",
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
}

FORBIDDEN_RESPONSE_MARKERS = [
    "raw_evidence_rows",
    "raw_comment_dump",
    "raw_author_id",
    "raw_author_name",
    "author_id",
    "author_name",
    "profile_url",
    "private_message",
    "api_key",
    "secret",
    "token",
    "cookie",
    "session",
    "password",
    "browser_profile",
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


def _payload_text(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False).lower()


def _payload_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        keys = {str(key) for key in value}
        for nested_value in value.values():
            keys.update(_payload_keys(nested_value))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_payload_keys(item))
        return keys
    return set()


def _assert_enabled_base_envelope(payload: dict[str, Any], schema: str) -> None:
    assert payload["schema"] == schema
    assert payload["route_scope"] == "internal_operator"
    assert payload["access_scope"] == "local_or_disabled_by_default"
    assert payload["metadata_only"] is True
    assert payload["review_only"] is True
    assert payload["production_import_allowed"] is False
    assert payload["evidence_layer_write_allowed"] is False
    assert payload["production_case_creation_allowed"] is False
    assert payload["analysis_run_allowed"] is False
    assert payload["public_output_allowed"] is False


def _assert_no_forbidden_payload_content(payload: dict[str, Any], tmp_path: Path) -> None:
    text = _payload_text(payload)
    # These false-valued safety flag names are required boundary metadata, not leaked raw values.
    text = text.replace('"raw_author_identifiers_printed": false', "")
    text = text.replace('"secrets_read": false', "")
    keys = _payload_keys(payload)

    assert str(tmp_path).lower() not in text
    assert "g:\\" not in text
    assert "c:\\users" not in text
    assert "raw_metadata" not in text.replace("raw_metadata_exposed", "")
    for forbidden in FORBIDDEN_KEYS:
        assert forbidden not in keys
    for forbidden in FORBIDDEN_RESPONSE_MARKERS:
        assert forbidden not in text


def _assert_required_false_safety_flags(payload: dict[str, Any]) -> None:
    safety_flags = payload["safety_flags"]
    for flag in REQUIRED_FALSE_SAFETY_FLAGS:
        assert safety_flags[flag] is False


@pytest.mark.parametrize("env_value", ENABLED_VALUES)
def test_explicit_enabled_env_values_return_synthetic_fixture_list(
    monkeypatch: pytest.MonkeyPatch,
    env_value: str,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(ENV_FLAG, env_value)

    response = client.get(LIST_ROUTE)
    payload = response.json()

    assert response.status_code == 200
    _assert_enabled_base_envelope(payload, "internal_operator_review_only_staging_response_list_v0_1")
    assert payload["count"] == 1
    assert len(payload["candidates"]) == 1
    assert payload["candidates"][0]["staging_candidate_id"] == SYNTHETIC_CANDIDATE_ID
    assert payload["candidates"][0]["package_name"] == "synthetic_package"
    assert payload["candidates"][0]["review_status"] == "ready_for_human_review"
    _assert_required_false_safety_flags(payload)
    _assert_no_forbidden_payload_content(payload, tmp_path)


@pytest.mark.parametrize("env_value", ENABLED_VALUES)
def test_explicit_enabled_env_values_return_synthetic_fixture_detail(
    monkeypatch: pytest.MonkeyPatch,
    env_value: str,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(ENV_FLAG, env_value)

    response = client.get(DETAIL_ROUTE)
    payload = response.json()

    assert response.status_code == 200
    _assert_enabled_base_envelope(payload, "internal_operator_review_only_staging_response_v0_1")
    assert payload["staging_candidate_id"] == SYNTHETIC_CANDIDATE_ID
    assert payload["staging_candidate"]["staging_candidate_id"] == SYNTHETIC_CANDIDATE_ID
    assert payload["staging_candidate"]["package_name"] == "synthetic_package"
    assert payload["gate_summary"]["evidence_row_boundary_status"] == "evidence_rows_not_read"
    assert payload["gate_summary"]["staging_status"] == "ready_for_human_review"
    assert set(payload["allowed_actions"]) == ALLOWED_ACTIONS
    assert BLOCKED_ACTIONS.issubset(set(payload["blocked_actions"]))
    _assert_required_false_safety_flags(payload)
    _assert_no_forbidden_payload_content(payload, tmp_path)


def test_allowed_actions_are_review_labels_only_and_do_not_create_state_changing_routes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_FLAG, "true")

    payload = client.get(DETAIL_ROUTE).json()
    route_methods = {
        route.path: route.methods
        for route in app.routes
        if "staging/review-only" in getattr(route, "path", "")
    }

    assert set(payload["allowed_actions"]) == ALLOWED_ACTIONS
    assert set(route_methods) == {
        LIST_ROUTE,
        f"{LIST_ROUTE}/{{staging_candidate_id}}",
        BRIDGE_ROUTE_TEMPLATE,
        PROJECTION_ROUTE_TEMPLATE,
    }
    for path, methods in route_methods.items():
        assert path.startswith("/api/v1/internal/")
        assert "GET" in methods
        assert "POST" not in methods
        assert "PUT" not in methods
        assert "PATCH" not in methods
        assert "DELETE" not in methods


def test_enabled_mode_unknown_candidate_returns_safe_not_found_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(ENV_FLAG, "yes")

    response = client.get(UNKNOWN_ROUTE)
    payload = response.json()

    assert response.status_code == 200
    assert payload["schema"] == "internal_operator_review_only_staging_error_v0_1"
    assert payload["route_scope"] == "internal_operator"
    assert payload["access_scope"] == "local_or_disabled_by_default"
    assert payload["metadata_only"] is True
    assert payload["review_only"] is True
    assert payload["error_code"] == "not_found"
    assert "not_found" in payload["blockers"]
    assert payload["path_exposed"] is False
    assert payload["raw_metadata_exposed"] is False
    _assert_no_forbidden_payload_content(payload, tmp_path)


def test_enabled_synthetic_routes_do_not_open_evidence_item_files(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_FLAG, "true")
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

    assert client.get(LIST_ROUTE).json()["schema"] == "internal_operator_review_only_staging_response_list_v0_1"
    assert client.get(DETAIL_ROUTE).json()["schema"] == "internal_operator_review_only_staging_response_v0_1"


def test_bridge_remains_independently_disabled_while_synthetic_fixture_routes_are_enabled(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(ENV_FLAG, "true")
    monkeypatch.delenv(BRIDGE_ENV_FLAG, raising=False)

    payload = client.get(BRIDGE_ROUTE).json()

    assert payload["schema"] == "internal_operator_review_only_staging_local_exchange_response_v0_1"
    assert payload["error_code"] == "local_exchange_route_disabled"
    assert payload["reader_status"] == "not_called"
    assert payload["candidate_count"] == 0
    _assert_no_forbidden_payload_content(payload, tmp_path)


def test_enabled_synthetic_routes_do_not_probe_real_package_or_private_collector_paths(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_FLAG, "true")
    original_exists = Path.exists
    original_iterdir = Path.iterdir
    forbidden_fragments = [
        "网页端任务二",
        "private_collector",
        "exports",
        "sentigraph-evidence-v1",
        "runtime",
    ]

    def assert_safe_path(path: Path) -> None:
        normalized = str(path).lower()
        if any(fragment.lower() in normalized for fragment in forbidden_fragments):
            raise AssertionError(f"enabled fixture smoke must not probe real path: {path}")

    def guarded_exists(self: Path) -> bool:
        assert_safe_path(self)
        return original_exists(self)

    def guarded_iterdir(self: Path):
        assert_safe_path(self)
        return original_iterdir(self)

    monkeypatch.setattr(Path, "exists", guarded_exists)
    monkeypatch.setattr(Path, "iterdir", guarded_iterdir)

    assert client.get(LIST_ROUTE).json()["count"] == 1
    assert client.get(DETAIL_ROUTE).json()["staging_candidate_id"] == SYNTHETIC_CANDIDATE_ID


def test_no_public_c_end_or_b_end_alias_routes_exist_for_enabled_fixture_family() -> None:
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


def test_enabled_synthetic_smoke_creates_no_storage_or_side_effect_files(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(ENV_FLAG, "true")

    client.get(LIST_ROUTE)
    client.get(DETAIL_ROUTE)
    client.get(BRIDGE_ROUTE)

    assert not list(tmp_path.rglob("review_only_staging*.json"))
    assert not list(tmp_path.rglob("staging_candidate*.json"))
    assert not list(tmp_path.rglob("review_queue*.json"))
    assert not list(tmp_path.rglob("audit*.json"))
    assert not list(tmp_path.rglob("evidence_layer*.json"))
    assert not list(tmp_path.rglob("production_case*.json"))
    assert not list(tmp_path.rglob("analysis_run*.json"))
    assert not list(tmp_path.rglob("*.sqlite"))
    assert not list(tmp_path.rglob("*.db"))
