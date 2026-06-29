from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

LIST_ROUTE = "/api/v1/internal/staging/review-only/candidates"
DETAIL_ROUTE = "/api/v1/internal/staging/review-only/candidates/synthetic_review_staging_candidate"
UNKNOWN_ROUTE = "/api/v1/internal/staging/review-only/candidates/unknown_candidate"
ENV_FLAG = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED"

FORBIDDEN_RESPONSE_TERMS = [
    "raw_evidence_rows",
    "raw_comment_dump",
    "raw_author_id",
    "raw_author_name",
    "profile_url",
    "private_message",
    "cookie",
    "session",
    "token",
    "password",
    "api_key",
    "browser_profile",
    "absolute_private_path",
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


def _response_text(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False).lower()


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


def _assert_safe_disabled_response(payload: dict) -> None:
    assert payload["schema"] == "internal_operator_review_only_staging_error_v0_1"
    assert payload["route_scope"] == "internal_operator"
    assert payload["access_scope"] == "local_or_disabled_by_default"
    assert payload["metadata_only"] is True
    assert payload["review_only"] is True
    assert payload["error_code"] == "route_disabled"
    assert payload["message"] == "Review-only staging route is disabled."
    assert "route_disabled" in payload["blockers"]
    assert payload["warnings"] == []
    assert payload["path_exposed"] is False
    assert payload["raw_metadata_exposed"] is False


def test_list_route_is_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv(ENV_FLAG, raising=False)

    response = client.get(LIST_ROUTE)
    payload = response.json()

    assert response.status_code == 200
    _assert_safe_disabled_response(payload)


def test_detail_route_is_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv(ENV_FLAG, raising=False)

    response = client.get(DETAIL_ROUTE)
    payload = response.json()

    assert response.status_code == 200
    _assert_safe_disabled_response(payload)


def test_disabled_response_exposes_no_absolute_paths_or_raw_metadata(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv(ENV_FLAG, raising=False)

    payload = client.get(DETAIL_ROUTE).json()
    text = _response_text(payload)

    assert str(tmp_path).lower() not in text
    assert "raw_metadata" not in text.replace("raw_metadata_exposed", "")
    assert "evidence_items.jsonl" not in text
    assert "evidence_items.csv" not in text


def test_disabled_routes_do_not_open_evidence_item_files(monkeypatch) -> None:
    monkeypatch.delenv(ENV_FLAG, raising=False)
    original_open = Path.open

    def guarded_open(self: Path, *args, **kwargs):
        if self.name in {"evidence_items.jsonl", "evidence_items.csv"}:
            raise AssertionError(f"{self.name} must not be opened")
        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_open)

    assert client.get(LIST_ROUTE).json()["error_code"] == "route_disabled"
    assert client.get(DETAIL_ROUTE).json()["error_code"] == "route_disabled"


def test_enabled_list_route_returns_safe_fixture_envelope(monkeypatch) -> None:
    monkeypatch.setenv(ENV_FLAG, "true")

    response = client.get(LIST_ROUTE)
    payload = response.json()

    assert response.status_code == 200
    assert payload["schema"] == "internal_operator_review_only_staging_response_list_v0_1"
    assert payload["route_scope"] == "internal_operator"
    assert payload["access_scope"] == "local_or_disabled_by_default"
    assert payload["metadata_only"] is True
    assert payload["review_only"] is True
    assert payload["production_import_allowed"] is False
    assert payload["evidence_layer_write_allowed"] is False
    assert payload["production_case_creation_allowed"] is False
    assert payload["analysis_run_allowed"] is False
    assert payload["public_output_allowed"] is False
    assert len(payload["candidates"]) == 1
    assert payload["candidates"][0]["staging_candidate_id"] == "synthetic_review_staging_candidate"


def test_enabled_detail_route_returns_safe_fixture_response(monkeypatch) -> None:
    monkeypatch.setenv(ENV_FLAG, "1")

    response = client.get(DETAIL_ROUTE)
    payload = response.json()

    assert response.status_code == 200
    assert payload["schema"] == "internal_operator_review_only_staging_response_v0_1"
    assert payload["staging_candidate_id"] == "synthetic_review_staging_candidate"
    assert payload["route_scope"] == "internal_operator"
    assert payload["access_scope"] == "local_or_disabled_by_default"
    assert payload["metadata_only"] is True
    assert payload["review_only"] is True
    assert payload["production_import_allowed"] is False
    assert payload["evidence_layer_write_allowed"] is False
    assert payload["production_case_creation_allowed"] is False
    assert payload["analysis_run_allowed"] is False
    assert payload["public_output_allowed"] is False
    assert payload["staging_candidate"]["package_name"] == "synthetic_package"
    assert payload["gate_summary"]["evidence_row_boundary_status"] == "evidence_rows_not_read"


def test_enabled_detail_route_has_required_false_safety_flags(monkeypatch) -> None:
    monkeypatch.setenv(ENV_FLAG, "yes")

    payload = client.get(DETAIL_ROUTE).json()

    for flag in REQUIRED_FALSE_SAFETY_FLAGS:
        assert payload["safety_flags"][flag] is False


def test_enabled_detail_route_has_review_only_labels_and_blocked_production_actions(monkeypatch) -> None:
    monkeypatch.setenv(ENV_FLAG, "true")

    payload = client.get(DETAIL_ROUTE).json()

    assert set(payload["allowed_actions"]) == {
        "continue_review",
        "request_more_metadata",
        "mark_manual_review_required",
        "reject_package",
        "block_privacy_issue",
        "request_future_evidence_preview_gate",
        "request_future_dedup_gate",
        "request_future_promotion_gate",
    }
    for blocked_action in [
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
    ]:
        assert blocked_action in payload["blocked_actions"]


def test_enabled_detail_route_contains_no_forbidden_fields_or_absolute_private_paths(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv(ENV_FLAG, "true")

    payload = client.get(DETAIL_ROUTE).json()
    text = _response_text(payload)
    keys = _json_keys(payload)

    for forbidden in FORBIDDEN_RESPONSE_TERMS:
        assert forbidden not in keys
    assert str(tmp_path).lower() not in text
    assert "g:\\" not in text
    assert "c:\\users" not in text


def test_unknown_synthetic_candidate_returns_safe_not_found_error(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv(ENV_FLAG, "true")

    response = client.get(UNKNOWN_ROUTE)
    payload = response.json()
    text = _response_text(payload)

    assert response.status_code == 200
    assert payload["schema"] == "internal_operator_review_only_staging_error_v0_1"
    assert payload["error_code"] == "not_found"
    assert payload["path_exposed"] is False
    assert payload["raw_metadata_exposed"] is False
    assert str(tmp_path).lower() not in text


def test_route_family_exposes_get_only_methods() -> None:
    route_methods = {
        route.path: route.methods
        for route in app.routes
        if getattr(route, "path", "").startswith("/api/v1/internal/staging/review-only/candidates")
    }

    assert route_methods
    for methods in route_methods.values():
        assert "GET" in methods
        assert "POST" not in methods
        assert "PUT" not in methods
        assert "PATCH" not in methods
        assert "DELETE" not in methods


def test_route_module_has_no_file_stream_zip_or_external_delivery_behavior() -> None:
    route_module = Path("backend/app/api/v1/routes/internal_operator_review_only_staging.py")
    text = route_module.read_text(encoding="utf-8")

    forbidden_terms = [
        "FileResponse",
        "StreamingResponse",
        "zipfile",
        "public_url",
        "signed_url",
        "send_email",
        "object_storage",
        "external_delivery",
        "portal_publication",
    ]
    for term in forbidden_terms:
        assert term not in text
