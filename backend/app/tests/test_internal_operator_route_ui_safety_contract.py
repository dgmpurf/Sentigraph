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
SYNTHETIC_CANDIDATE_ID = "synthetic_review_staging_candidate"
LIST_ROUTE = "/api/v1/internal/staging/review-only/candidates"
DETAIL_ROUTE = f"{LIST_ROUTE}/{SYNTHETIC_CANDIDATE_ID}"
UNKNOWN_ROUTE = f"{LIST_ROUTE}/unknown_candidate"
ROUTE_MODULE = Path("backend/app/api/v1/routes/internal_operator_review_only_staging.py")

DISABLED_VALUES = [None, "", "false", "0", "unknown"]
ENABLED_VALUES = ["1", "true", "yes"]

REQUIRED_FALSE_SAFETY_FLAGS = {
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
}

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

FORBIDDEN_ACTIVE_KEYS = {
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
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
    "cookie",
    "session",
    "token",
    "password",
    "api_key",
    "browser_profile_path",
    "absolute_private_path",
    "package_path",
}

FORBIDDEN_ACTIVE_VALUE_MARKERS = [
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "raw_evidence_rows",
    "raw_comment_dump",
    "raw_author_id",
    "raw_author_name",
    "author_id",
    "author_name",
    "profile_url",
    "private_message",
    "api_key",
    "token",
    "cookie",
    "session",
    "password",
    "browser_profile",
    "evidence_items.jsonl",
    "evidence_items.csv",
]

STATIC_FORBIDDEN_IMPLEMENTATION_TERMS = [
    "FileResponse",
    "StreamingResponse",
    "ZipFile",
    "zipfile",
    "public_url",
    "signed_url",
    "external_delivery",
    "send_email",
    "object_storage",
    "portal_publication",
    "file_byte",
    "file-bytes",
    "archive creation",
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


def _json_text(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True).lower()


def _json_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        keys = {str(key) for key in value}
        for nested_value in value.values():
            keys.update(_json_keys(nested_value))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_json_keys(item))
        return keys
    return set()


def _strip_allowed_boundary_metadata(text: str) -> str:
    allowed_boundary_names = [
        "raw_metadata_exposed",
        "raw_author_identifiers_printed",
        "raw_comments_printed",
        "secrets_read",
        "evidence_items_jsonl_parsed",
        "evidence_items_csv_parsed",
        "path_exposed",
    ]
    for name in allowed_boundary_names:
        text = text.replace(name, "")
    for action in BLOCKED_ACTIONS:
        text = text.replace(action, "")
    return text


def _assert_safe_disabled_error(payload: dict[str, Any], error_code: str) -> None:
    assert payload["schema"] == "internal_operator_review_only_staging_error_v0_1"
    assert payload["route_scope"] == "internal_operator"
    assert payload["access_scope"] == "local_or_disabled_by_default"
    assert payload["metadata_only"] is True
    assert payload["review_only"] is True
    assert payload["error_code"] == error_code
    assert error_code in payload["blockers"]
    assert payload["path_exposed"] is False
    assert payload["raw_metadata_exposed"] is False


def _assert_safe_payload(payload: dict[str, Any], tmp_path: Path) -> None:
    keys = _json_keys(payload)
    text = _strip_allowed_boundary_metadata(_json_text(payload))

    assert str(tmp_path).lower() not in text
    assert "g:\\" not in text
    assert "c:\\users" not in text
    for forbidden_key in FORBIDDEN_ACTIVE_KEYS:
        assert forbidden_key not in keys
    for marker in FORBIDDEN_ACTIVE_VALUE_MARKERS:
        assert marker not in text


def _assert_base_enabled_envelope(payload: dict[str, Any], schema: str) -> None:
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
    assert set(payload["allowed_actions"]) == ALLOWED_ACTIONS
    assert BLOCKED_ACTIONS.issubset(set(payload["blocked_actions"]))
    for flag in REQUIRED_FALSE_SAFETY_FLAGS:
        assert payload["safety_flags"][flag] is False


@pytest.mark.parametrize("env_value", DISABLED_VALUES)
@pytest.mark.parametrize("route", [LIST_ROUTE, DETAIL_ROUTE])
def test_disabled_and_falsey_env_values_return_safe_route_disabled(
    monkeypatch: pytest.MonkeyPatch,
    env_value: str | None,
    route: str,
    tmp_path: Path,
) -> None:
    _set_env(monkeypatch, env_value)

    response = client.get(route)
    payload = response.json()

    assert response.status_code == 200
    _assert_safe_disabled_error(payload, "route_disabled")
    _assert_safe_payload(payload, tmp_path)


@pytest.mark.parametrize("env_value", ENABLED_VALUES)
def test_enabled_values_return_synthetic_fixture_list_only(
    monkeypatch: pytest.MonkeyPatch,
    env_value: str,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(ENV_FLAG, env_value)

    response = client.get(LIST_ROUTE)
    payload = response.json()

    assert response.status_code == 200
    _assert_base_enabled_envelope(
        payload,
        "internal_operator_review_only_staging_response_list_v0_1",
    )
    assert payload["count"] == 1
    assert len(payload["candidates"]) == 1
    assert payload["candidates"][0]["staging_candidate_id"] == SYNTHETIC_CANDIDATE_ID
    assert payload["candidates"][0]["package_name"] == "synthetic_package"
    assert payload["candidates"][0]["review_status"] == "ready_for_human_review"
    _assert_safe_payload(payload, tmp_path)


@pytest.mark.parametrize("env_value", ENABLED_VALUES)
def test_enabled_values_return_synthetic_fixture_detail_only(
    monkeypatch: pytest.MonkeyPatch,
    env_value: str,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(ENV_FLAG, env_value)

    response = client.get(DETAIL_ROUTE)
    payload = response.json()

    assert response.status_code == 200
    _assert_base_enabled_envelope(payload, "internal_operator_review_only_staging_response_v0_1")
    assert payload["staging_candidate_id"] == SYNTHETIC_CANDIDATE_ID
    assert payload["staging_candidate"]["staging_candidate_id"] == SYNTHETIC_CANDIDATE_ID
    assert payload["staging_candidate"]["package_name"] == "synthetic_package"
    assert payload["gate_summary"]["evidence_row_boundary_status"] == "evidence_rows_not_read"
    assert payload["gate_summary"]["staging_status"] == "ready_for_human_review"
    _assert_safe_payload(payload, tmp_path)


def test_unknown_enabled_candidate_returns_safe_not_found(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(ENV_FLAG, "true")

    response = client.get(UNKNOWN_ROUTE)
    payload = response.json()

    assert response.status_code == 200
    _assert_safe_disabled_error(payload, "not_found")
    _assert_safe_payload(payload, tmp_path)


def test_internal_operator_route_family_is_get_only_and_has_no_public_aliases() -> None:
    route_methods = {
        route.path: route.methods
        for route in app.routes
        if "staging/review-only/candidates" in getattr(route, "path", "")
    }

    assert set(route_methods) == {LIST_ROUTE, f"{LIST_ROUTE}/{{staging_candidate_id}}"}
    for path, methods in route_methods.items():
        assert path.startswith("/api/v1/internal/")
        assert methods == {"GET"}

    aliases = [
        route.path
        for route in app.routes
        if "staging/review-only/candidates" in getattr(route, "path", "")
        and not getattr(route, "path", "").startswith("/api/v1/internal/")
    ]
    assert aliases == []


def test_no_provider_private_collector_or_customer_callback_route_exists() -> None:
    unsafe_route_fragments = [
        "/provider",
        "/callback",
        "/collector",
        "/public",
        "/customer",
        "/b-end",
        "/c-end",
    ]

    route_paths = [
        route.path
        for route in app.routes
        if "staging/review-only/candidates" in getattr(route, "path", "")
    ]

    assert route_paths
    for path in route_paths:
        for fragment in unsafe_route_fragments:
            assert fragment not in path


def test_route_module_static_scan_has_no_delivery_file_response_or_output_generation() -> None:
    text = ROUTE_MODULE.read_text(encoding="utf-8")

    for forbidden in STATIC_FORBIDDEN_IMPLEMENTATION_TERMS:
        assert forbidden not in text


def test_enabled_fixture_route_does_not_open_evidence_rows_or_private_collector_paths(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_FLAG, "true")
    original_path_open = Path.open
    original_builtin_open = builtins.open
    forbidden_fragments = [
        "evidence_items.jsonl",
        "evidence_items.csv",
        "sentigraph-evidence-v1",
        "private_collector",
        "\u7f51\u9875\u7aef\u4efb\u52a1\u4e8c",
        "exports",
    ]

    def _assert_safe_path(path: object) -> None:
        normalized = str(path).lower()
        if any(fragment.lower() in normalized for fragment in forbidden_fragments):
            raise AssertionError(f"synthetic fixture route must not open real package path: {path}")

    def guarded_path_open(self: Path, *args: Any, **kwargs: Any):
        _assert_safe_path(self)
        return original_path_open(self, *args, **kwargs)

    def guarded_builtin_open(file: object, *args: Any, **kwargs: Any):
        _assert_safe_path(file)
        return original_builtin_open(file, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_path_open)
    monkeypatch.setattr(builtins, "open", guarded_builtin_open)

    assert client.get(LIST_ROUTE).json()["count"] == 1
    assert client.get(DETAIL_ROUTE).json()["staging_candidate_id"] == SYNTHETIC_CANDIDATE_ID


def test_route_smoke_creates_no_persistent_runtime_or_production_side_effect_files(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv(ENV_FLAG, "true")

    client.get(LIST_ROUTE)
    client.get(DETAIL_ROUTE)
    client.get(UNKNOWN_ROUTE)

    unexpected_patterns = [
        "review_only_staging*.json",
        "staging_candidate*.json",
        "review_queue*.json",
        "audit*.json",
        "evidence_layer*.json",
        "production_case*.json",
        "analysis_run*.json",
        "b_end_report*.json",
        "sandbox*.json",
        "public_event*.json",
        "*.sqlite",
        "*.db",
    ]
    for pattern in unexpected_patterns:
        assert list(tmp_path.rglob(pattern)) == []


def test_frontend_has_no_internal_operator_ui_or_public_alias_for_this_phase() -> None:
    frontend_files = list(Path("frontend/src").rglob("*.jsx")) + list(Path("frontend/src").rglob("*.js"))
    assert frontend_files

    joined = "\n".join(path.read_text(encoding="utf-8") for path in frontend_files)

    assert "/api/v1/internal/staging/review-only/candidates" not in joined
    assert "internal/staging/review-only/candidates" not in joined
    assert "synthetic_review_staging_candidate" not in joined
    assert "internal_operator_review_only_staging" not in joined
