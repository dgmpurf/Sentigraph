from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

ENV_FLAG = "SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED"
ROUTE_PREFIX = "/api/v1/internal/alpha/review-console"
ALLOWED_PROJECTION_ID = "internal-alpha-safe-projection-fixture"
ALLOWED_ALT_PROJECTION_ID = "8z16-no-write-alpha-fixture"
DETAIL_ROUTE = f"{ROUTE_PREFIX}/projections/{ALLOWED_PROJECTION_ID}"
ALT_DETAIL_ROUTE = f"{ROUTE_PREFIX}/projections/{ALLOWED_ALT_PROJECTION_ID}"
UNKNOWN_DETAIL_ROUTE = f"{ROUTE_PREFIX}/projections/unknown-projection-id"

APPROVAL_PHRASE_8Z22 = "APPROVE_8Z_22_INTERNAL_ALPHA_REVIEW_CONSOLE_DISABLED_BACKEND_ROUTE_SKELETON_SMOKE"
APPROVAL_PHRASE_8Z21 = (
    "APPROVE_8Z_21_INTERNAL_ALPHA_REVIEW_CONSOLE_PROJECTION_COMPLETION_ROUTE_READINESS_GATE_DECISION_DOCS_ONLY"
)
APPROVAL_PHRASE_8Z20 = "APPROVE_8Z_20_INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_METADATA_PROJECTION_HELPER_SMOKE"

FALSEY_ENV_VALUES = [None, "", "false", "0", "no", "unknown"]
ENABLED_ENV_VALUES = ["1", "true", "yes"]

FORBIDDEN_RESPONSE_TERMS = [
    "raw_author_id",
    "raw_author_name",
    "raw evidence rows",
    "raw comments",
    "raw_comment",
    "profile_url",
    "private_message",
    "cookie",
    "session",
    "token",
    "password",
    "api_key",
    "browser_profile",
    ".env",
    "evidence_items.jsonl",
    "evidence_items.csv",
    "source_manifest",
    "collection_log",
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "actual-raw-author-should-never-appear",
    "actual-profile-url-should-never-appear",
    "actual-token-should-never-appear",
    "g:/private-collector",
    "c:/users",
]

STATIC_FORBIDDEN_ROUTE_TERMS = [
    "FileResponse",
    "StreamingResponse",
    "zipfile",
    "public_url",
    "signed_url",
    "file_bytes",
    "file bytes",
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

DISALLOWED_SERVICE_IMPORTS = [
    "controlled_row_preview",
    "controlled_evidence_candidate",
    "controlled_review_queue_candidate",
    "controlled_evidence_layer_import_candidate",
    "controlled_evidence_layer_write_candidate",
    "controlled_evidenceitem_evidence_layer_write_runtime",
    "evidence_import",
    "evidence_ingestion",
    "private_collector_package_resolver",
    "private_collector_provider_result_reader",
    "local_exchange_reader",
    "private_collector_review_only_staging",
]

PUBLIC_ALIASES = [
    "/public/review-console",
    "/public-events/review-console",
    "/reports/review-console",
    "/customer/review-console",
    "/b-end/review-console",
    "/c-end/review-console",
    "/api/v1/public/review-console",
    "/api/v1/review-console/public",
]


def _set_env(monkeypatch: pytest.MonkeyPatch, value: str | None) -> None:
    if value is None:
        monkeypatch.delenv(ENV_FLAG, raising=False)
    else:
        monkeypatch.setenv(ENV_FLAG, value)


def _payload_text(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).casefold()


def _assert_no_forbidden_response_terms(payload: object) -> None:
    text = _payload_text(payload)
    for term in FORBIDDEN_RESPONSE_TERMS:
        assert term.casefold() not in text, term
    assert ":\\" not in text


def _assert_disabled_response(payload: dict[str, object]) -> None:
    assert payload["response_schema"] == "sentigraph_internal_alpha_review_console_route_error_v0_1"
    assert payload["error"] == "route_disabled"
    assert payload["path_exposed"] is False
    assert payload["raw_metadata_exposed"] is False
    assert payload["raw_rows_exposed"] is False
    assert payload["secrets_exposed"] is False
    assert payload["route_ready"] is False
    assert payload["frontend_ready"] is False
    assert payload["production_ready"] is False
    assert payload["public_ready"] is False
    _assert_no_forbidden_response_terms(payload)


def _assert_safe_success_response(payload: dict[str, object], projection_id: str) -> None:
    assert payload["response_schema"] == "sentigraph_internal_alpha_review_console_route_response_v0_1"
    assert payload["route_mode"] == "disabled_by_default_internal_safe_projection_route_skeleton"
    assert payload["projection_id"] == projection_id
    assert payload["route_ready"] == "skeleton_only"
    assert payload["frontend_ready"] is False
    assert payload["runtime_ready"] is False
    assert payload["public_ready"] is False
    assert payload["production_ready"] is False
    assert payload["actual_write_enabled"] is False
    assert payload["production_object_enabled"] is False
    assert payload["review_queue_runtime_enabled"] is False
    assert payload["source11_runtime_enabled"] is False
    assert payload["finalsummaryreport_runtime_enabled"] is False

    projection = payload["projection"]
    assert isinstance(projection, dict)
    assert projection["projection_schema"] == "sentigraph_internal_alpha_review_console_safe_metadata_projection_v0_1"
    assert projection["projection_mode"] == "backend_only_local_safe_metadata_projection"
    assert projection["source_chain_boundary"] == "evidence_layer_write_candidate_boundary"
    assert projection["safe_metadata_only"] is True
    assert projection["label_only_operator_outcomes"] is True
    assert projection["human_review_required"] is True
    assert projection["no_automatic_trust_upgrade"] is True
    assert projection["route_ready"] is False
    assert projection["frontend_ready"] is False
    assert projection["runtime_ready"] is False
    assert projection["public_ready"] is False
    assert projection["production_ready"] is False
    assert projection["actual_write_enabled"] is False
    assert projection["production_object_enabled"] is False
    assert projection["review_queue_runtime_enabled"] is False
    assert projection["source11_runtime_enabled"] is False
    assert projection["finalsummaryreport_runtime_enabled"] is False
    _assert_no_forbidden_response_terms(payload)


@pytest.mark.parametrize("env_value", FALSEY_ENV_VALUES)
def test_route_is_disabled_by_default_and_falsey_env_values_do_not_call_projection_helper(
    monkeypatch: pytest.MonkeyPatch,
    env_value: str | None,
) -> None:
    import app.api.v1.routes.internal_alpha_review_console as route_module

    _set_env(monkeypatch, env_value)

    def fail_if_called(*args: object, **kwargs: object) -> None:
        raise AssertionError("projection helper must not run while route is disabled")

    monkeypatch.setattr(route_module, "build_internal_alpha_review_console_safe_metadata_projection", fail_if_called)

    response = client.get(DETAIL_ROUTE)
    payload = response.json()

    assert response.status_code == 200
    _assert_disabled_response(payload)


@pytest.mark.parametrize("env_value", ENABLED_ENV_VALUES)
def test_enabled_values_return_only_safe_synthetic_projection_response(
    monkeypatch: pytest.MonkeyPatch,
    env_value: str,
) -> None:
    _set_env(monkeypatch, env_value)

    response = client.get(DETAIL_ROUTE)
    payload = response.json()

    assert response.status_code == 200
    _assert_safe_success_response(payload, ALLOWED_PROJECTION_ID)


def test_alternate_allowed_projection_id_returns_safe_projection(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_env(monkeypatch, "yes")

    payload = client.get(ALT_DETAIL_ROUTE).json()

    _assert_safe_success_response(payload, ALLOWED_ALT_PROJECTION_ID)


def test_unknown_projection_id_is_safe_not_found_without_default_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_env(monkeypatch, "true")

    payload = client.get(UNKNOWN_DETAIL_ROUTE).json()

    assert payload["response_schema"] == "sentigraph_internal_alpha_review_console_route_error_v0_1"
    assert payload["error"] == "unsupported_projection"
    assert payload["projection_id"] == "unsupported"
    assert payload["path_exposed"] is False
    assert payload["raw_metadata_exposed"] is False
    assert payload["raw_rows_exposed"] is False
    assert payload["secrets_exposed"] is False
    assert "projection" not in payload
    _assert_no_forbidden_response_terms(payload)


def test_route_family_is_get_only_and_internal_only() -> None:
    route_methods = {
        route.path: route.methods
        for route in app.routes
        if "internal/alpha/review-console" in getattr(route, "path", "")
    }

    assert set(route_methods) == {f"{ROUTE_PREFIX}/projections/{{projection_id}}"}
    for path, methods in route_methods.items():
        assert path.startswith("/api/v1/internal/")
        assert "GET" in methods
        assert "POST" not in methods
        assert "PUT" not in methods
        assert "PATCH" not in methods
        assert "DELETE" not in methods


def test_no_public_customer_b_end_or_c_end_alias_routes_exist() -> None:
    active_paths = [getattr(route, "path", "") for route in app.routes]
    for alias in PUBLIC_ALIASES:
        assert alias not in active_paths
    assert [
        path
        for path in active_paths
        if "review-console" in path and not path.startswith("/api/v1/internal/alpha/review-console")
    ] == []


def test_route_source_has_no_file_delivery_package_delivery_or_forbidden_helpers() -> None:
    route_module = Path("backend/app/api/v1/routes/internal_alpha_review_console.py")
    text = route_module.read_text(encoding="utf-8")

    for forbidden in STATIC_FORBIDDEN_ROUTE_TERMS:
        assert forbidden not in text
    for forbidden_import in DISALLOWED_SERVICE_IMPORTS:
        assert forbidden_import not in text
    assert "internal_alpha_review_console_safe_metadata_projection" in text


def test_enabled_route_does_not_read_files(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_env(monkeypatch, "1")

    def blocked_file_access(*args: object, **kwargs: object) -> None:
        raise AssertionError("8Z-22 route skeleton must not read files")

    monkeypatch.setattr(builtins, "open", blocked_file_access)
    monkeypatch.setattr(Path, "open", blocked_file_access)
    monkeypatch.setattr(Path, "read_text", blocked_file_access)
    monkeypatch.setattr(Path, "read_bytes", blocked_file_access)

    payload = client.get(DETAIL_ROUTE).json()

    _assert_safe_success_response(payload, ALLOWED_PROJECTION_ID)


def test_no_frontend_hook_was_added() -> None:
    frontend_root = Path("frontend/src")
    frontend_files = [
        path
        for path in frontend_root.rglob("*")
        if path.is_file() and path.suffix in {".js", ".jsx", ".ts", ".tsx"}
    ]
    joined = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in frontend_files)

    assert "internal_alpha_review_console" not in joined
    assert "internal-alpha-review-console" not in joined
    assert "review-console/projections" not in joined


def test_approval_phrases_are_not_user_input_or_write_authorization() -> None:
    route_module = Path("backend/app/api/v1/routes/internal_alpha_review_console.py")
    text = route_module.read_text(encoding="utf-8")

    assert APPROVAL_PHRASE_8Z22 not in text
    assert APPROVAL_PHRASE_8Z21 not in text
    assert '"approval_phrase"' not in text
    assert "approval_phrase: str" not in text
    assert "exact_approval_phrase=PROJECTION_APPROVAL_PHRASE" in text
    assert APPROVAL_PHRASE_8Z20 not in text
    assert "actual Evidence Layer write approved" not in text
    assert "production EvidenceItem approved" not in text
