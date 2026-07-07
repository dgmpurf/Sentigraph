from __future__ import annotations

import json
from typing import Any

import pytest

import app.services.analysis_request_store as analysis_request_store
import app.services.controlled_evidence_layer_import_candidate as import_candidate_module
import app.services.controlled_evidence_layer_write_candidate as write_candidate_module
import app.services.controlled_evidence_layer_write_candidate_from_production_import_candidate as write_from_production_import_module
import app.services.controlled_evidenceitem_evidence_layer_write_runtime as evidenceitem_write_module
import app.services.controlled_production_analysis_run_candidate as production_analysis_run_module
import app.services.controlled_production_case_candidate as production_case_module
import app.services.controlled_production_evidence_import_candidate as production_import_module
import app.services.controlled_review_queue_candidate as review_queue_module
from app.services.controlled_evidence_candidate import (
    APPROVAL_PHRASE as EVIDENCE_CANDIDATE_APPROVAL_PHRASE,
    build_controlled_evidence_candidate_set,
)
from app.services.controlled_row_preview import (
    APPROVAL_PHRASE as ROW_PREVIEW_APPROVAL_PHRASE,
    APPROVED_ROW_SOURCE,
    build_controlled_row_preview,
)
from app.services.metadata_smoke_review_only_staging_boundary import (
    build_metadata_smoke_review_only_staging_boundary,
)
from app.services.real_exported_package_metadata_smoke import (
    APPROVED_CASE_ID_HINT,
    APPROVED_PACKAGE_NAME,
    APPROVED_PACKAGE_ROLE,
)


EIGHT_Y10_APPROVAL_PHRASE = (
    "APPROVE_8Y_10_CONTROLLED_REVIEW_QUEUE_CANDIDATE_TO_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE"
)
EIGHT_Y8_APPROVAL_PHRASE = "APPROVE_8Y_8_CONTROLLED_EVIDENCE_CANDIDATE_TO_REVIEW_QUEUE_CANDIDATE_SMOKE"
EIGHT_Y6_APPROVAL_PHRASE = "APPROVE_8Y_6_CONTROLLED_ROW_PREVIEW_TO_EVIDENCE_CANDIDATE_SOURCE_PATH_SMOKE"
OLD_DIRECT_IMPORT_APPROVAL_PHRASE = (
    "APPROVE_8Y_6_CONTROLLED_REDACTED_ROW_PREVIEW_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE"
)

SOURCE_REVIEW_QUEUE_BLOCKED_TRUE_FLAGS = {
    "raw_rows_exposed",
    "raw_comments_exposed",
    "raw_identities_exposed",
    "author_names_or_profile_urls_exposed",
    "evidence_layer_write",
    "production_evidence_item_created",
    "production_case_created",
    "production_analysis_run_created",
    "actual_review_queue_runtime_used",
    "production_review_queue_item_created",
    "review_queue_item_created",
    "actual_evidence_layer_write_used",
}

SOURCE_RUNTIME_BLOCKED_TRUE_FLAGS = {
    "emitted_raw_comments",
    "emitted_raw_identities",
    "emitted_profile_urls",
    "created_review_queue_items",
    "created_production_review_queue_items",
    "wrote_evidence_layer",
    "created_evidence_items",
    "created_production_case",
    "created_production_analysis_run",
    "read_original_package_rows",
    "parsed_evidence_items_csv",
    "parsed_source_manifest_jsonl_rows",
    "parsed_collection_log_jsonl_rows",
}

FORBIDDEN_KEYS = {
    "raw_rows",
    "raw_row",
    "raw_comment",
    "raw_comments",
    "raw_author_id",
    "raw_author_ids",
    "raw_author_name",
    "raw_author_names",
    "author_id",
    "author_ids",
    "author_name",
    "author_names",
    "username",
    "display_name",
    "profile_url",
    "profile_urls",
    "source_url",
    "private_message",
    "private_messages",
    "email",
    "phone",
    "token",
    "cookie",
    "session",
    "password",
    "api_key",
    "secret",
    "browser_profile",
    "browser_profile_path",
    "absolute_path",
    "package_path",
    "response_text",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
}

FORBIDDEN_SENTINELS = (
    "actual-token-should-never-appear",
    "actual-cookie-should-never-appear",
    "actual-api-key-should-never-appear",
    "actual-raw-author-should-never-appear",
    "actual-author-name-should-never-appear",
    "actual-username-should-never-appear",
    "actual-display-name-should-never-appear",
    "actual-profile-url-should-never-appear",
    "actual-raw-comment-should-never-appear",
    "G:/private-collector/should-never-appear",
    "C:/Users/msjpurf/private-collector/should-never-appear",
)


def _safe_8w2_smoke(**overrides: object) -> dict[str, object]:
    smoke: dict[str, object] = {
        "schema": "sentigraph_real_exported_package_metadata_smoke_v0_1",
        "phase": "8W-2",
        "smoke_status": "metadata_warn_manual_review_required",
        "target_package_name": APPROVED_PACKAGE_NAME,
        "target_package_role": APPROVED_PACKAGE_ROLE,
        "target_case_id_hint": APPROVED_CASE_ID_HINT,
        "metadata_only": True,
        "human_review_required": True,
        "warning_count": 1,
        "error_count": 0,
        "row_files_parsed": False,
        "evidence_items_jsonl_parsed": False,
        "evidence_items_csv_parsed": False,
        "original_package_rows_read": False,
        "private_collector_source_inspected": False,
        "real_exchange_dir_read": False,
        "safe_summary": {
            "validation_status": "passed",
            "warning_count": 1,
            "error_count": 0,
            "coverage_note_summary": "Selected public sample only; not full-web coverage.",
            "privacy_status": "metadata_only_no_known_privacy_blocker",
            "path_status": "repo_controlled_target_path_ok",
            "warning_summary": ["sample_size_below_target"],
            "blocker_summary": [],
        },
        "runtime_side_effects": {
            "called_real_api": False,
            "called_real_llm": False,
            "ran_provider_job": False,
            "ran_collector": False,
            "accessed_private_collector": False,
            "inspected_private_collector_source": False,
            "read_real_exchange_dir": False,
            "fetched_url": False,
            "scraped_page": False,
            "parsed_evidence_items_jsonl": False,
            "parsed_evidence_items_csv": False,
            "parsed_source_manifest_jsonl_rows": False,
            "parsed_collection_log_jsonl_rows": False,
            "read_original_package_rows": False,
            "read_raw_comments": False,
            "read_raw_identities": False,
            "wrote_evidence_layer": False,
            "created_evidence_items": False,
            "created_review_queue_items": False,
            "created_production_review_queue_items": False,
            "created_production_case": False,
            "created_production_analysis_run": False,
            "generated_b_end_report_runtime": False,
            "generated_sandbox_runtime": False,
            "generated_public_event_runtime": False,
            "used_report_export_runtime": False,
            "used_download_package_runtime": False,
            "used_public_access_runtime": False,
            "used_external_delivery_runtime": False,
            "used_final_delivery_runtime": False,
            "generated_response_text": False,
            "created_public_route": False,
            "modified_frontend": False,
            "published_or_sent": False,
            "auto_executed": False,
        },
    }
    smoke.update(overrides)
    return smoke


def _safe_row_preview() -> dict[str, Any]:
    return build_controlled_row_preview(
        build_metadata_smoke_review_only_staging_boundary(_safe_8w2_smoke()),
        approval_phrase=ROW_PREVIEW_APPROVAL_PHRASE,
        max_preview_rows=5,
        row_source=APPROVED_ROW_SOURCE,
    )


def _safe_evidence_candidate_set() -> dict[str, Any]:
    candidate_set = build_controlled_evidence_candidate_set(
        _safe_row_preview(),
        exact_approval_phrase=EVIDENCE_CANDIDATE_APPROVAL_PHRASE,
    )
    candidate_set["no_automatic_trust_upgrade"] = True
    return candidate_set


def _safe_review_queue_candidate_set() -> dict[str, Any]:
    review_queue_candidate_set = review_queue_module.build_controlled_review_queue_candidate_set(
        _safe_evidence_candidate_set(),
        exact_approval_phrase=review_queue_module.APPROVAL_PHRASE,
    )
    review_queue_candidate_set["no_automatic_trust_upgrade"] = True
    review_queue_candidate_set["actual_review_queue_runtime_used"] = False
    review_queue_candidate_set["actual_evidence_layer_write_used"] = False
    review_queue_candidate_set["raw_rows_exposed"] = False
    review_queue_candidate_set["raw_comments_exposed"] = False
    review_queue_candidate_set["raw_identities_exposed"] = False
    review_queue_candidate_set["author_names_or_profile_urls_exposed"] = False
    review_queue_candidate_set["secrets_read"] = False
    return review_queue_candidate_set


def _json_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        keys = {str(key) for key in value}
        for nested in value.values():
            keys.update(_json_keys(nested))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_json_keys(item))
        return keys
    return set()


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _assert_no_forbidden_output(value: object) -> None:
    keys = {key.lower() for key in _json_keys(value)}
    serialized = _serialized(value).lower()
    assert not (keys & FORBIDDEN_KEYS)
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel.lower() not in serialized
    assert "g:\\" not in serialized
    assert "c:\\users" not in serialized
    assert ":/" not in serialized


def _blocked_8y10_output(reason: str) -> dict[str, Any]:
    return {
        "schema": "sentigraph_8y10_review_queue_candidate_to_evidence_layer_import_candidate_smoke_v0_1",
        "phase": "8Y-10",
        "source_path_step": "review_queue_candidate_to_evidence_layer_import_candidate",
        "smoke_status": "blocked",
        "evidence_layer_import_candidate_created": False,
        "import_candidate_created": False,
        "import_candidate_schema": None,
        "import_candidate_mode": None,
        "source_review_queue_candidate_set_schema": None,
        "source_review_queue_candidate_schema": None,
        "source_review_queue_candidate_count": 0,
        "evidence_layer_import_candidate_count": 0,
        "blockers": [reason],
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "actual_evidence_layer_write_used": False,
        "evidence_layer_write": False,
        "production_evidence_item_created": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "actual_review_queue_runtime_used": False,
        "production_review_queue_item_created": False,
        "review_queue_item_created": False,
        "source11_runtime_called": False,
        "actual_final_summary_report_created": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_runtime_generated": False,
        "export_download_public_delivery_created": False,
        "generated_response_text": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "customer_ready": False,
        "public_ready": False,
        "raw_rows_exposed": False,
        "raw_comments_exposed": False,
        "raw_identities_exposed": False,
        "author_names_or_profile_urls_exposed": False,
        "secrets_read": False,
    }


def _source_review_queue_gate_blockers(source_candidate_set: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if (
        source_candidate_set.get("review_queue_candidate_set_schema")
        != "sentigraph_controlled_review_queue_candidate_set_v0_1"
    ):
        blockers.append("source_review_queue_candidate_set_schema_wrong")
    if source_candidate_set.get("no_automatic_trust_upgrade") is not True:
        blockers.append("source_no_automatic_trust_upgrade_not_true")
    for flag in SOURCE_REVIEW_QUEUE_BLOCKED_TRUE_FLAGS:
        if source_candidate_set.get(flag) is True:
            blockers.append(f"blocked_source_review_queue_candidate_{flag}")

    runtime_side_effects = source_candidate_set.get("runtime_side_effects")
    if isinstance(runtime_side_effects, dict):
        for flag in SOURCE_RUNTIME_BLOCKED_TRUE_FLAGS:
            if runtime_side_effects.get(flag) is True:
                blockers.append(f"blocked_source_review_queue_candidate_runtime_{flag}")
    return blockers


def _build_8y10_source_path_smoke(
    *,
    approval_phrase: str | None,
    source_review_queue_candidate_set: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if approval_phrase != EIGHT_Y10_APPROVAL_PHRASE:
        return _blocked_8y10_output("blocked_missing_exact_8y10_approval")

    candidate_source = source_review_queue_candidate_set or _safe_review_queue_candidate_set()
    source_blockers = _source_review_queue_gate_blockers(candidate_source)
    if source_blockers:
        return _blocked_8y10_output(source_blockers[0])

    import_candidate_set = import_candidate_module.build_controlled_evidence_layer_import_candidate_set(
        candidate_source,
        exact_approval_phrase=import_candidate_module.APPROVAL_PHRASE,
    )

    created = import_candidate_set["evidence_layer_import_candidate_created"]
    return {
        "schema": "sentigraph_8y10_review_queue_candidate_to_evidence_layer_import_candidate_smoke_v0_1",
        "phase": "8Y-10",
        "source_path_step": "review_queue_candidate_to_evidence_layer_import_candidate",
        "smoke_status": "ready" if created else "blocked",
        "evidence_layer_import_candidate_created": created,
        "import_candidate_created": created,
        "import_candidate_schema": import_candidate_set["evidence_layer_import_candidate_set_schema"],
        "import_candidate_mode": import_candidate_set["evidence_layer_import_candidate_mode"],
        "source_review_queue_candidate_set_schema": import_candidate_set[
            "source_review_queue_candidate_set_schema"
        ],
        "source_review_queue_candidate_schema": "sentigraph_controlled_review_queue_candidate_v0_1",
        "source_review_queue_candidate_count": import_candidate_set["source_review_queue_candidate_count"],
        "evidence_layer_import_candidate_count": import_candidate_set["evidence_layer_import_candidate_count"],
        "evidence_layer_import_candidate_set": import_candidate_set,
        "blockers": list(import_candidate_set["blockers"]),
        "warnings": list(import_candidate_set["warnings"]),
        "human_review_required": import_candidate_set["human_review_required"],
        "no_automatic_trust_upgrade": True,
        "actual_evidence_layer_write_used": False,
        "evidence_layer_write": import_candidate_set["evidence_layer_write"],
        "production_evidence_item_created": import_candidate_set["production_evidence_item_created"],
        "production_case_created": import_candidate_set["production_case_created"],
        "production_analysis_run_created": import_candidate_set["production_analysis_run_created"],
        "actual_review_queue_runtime_used": False,
        "production_review_queue_item_created": import_candidate_set["production_review_queue_item_created"],
        "review_queue_item_created": import_candidate_set["review_queue_item_created"],
        "source11_runtime_called": False,
        "actual_final_summary_report_created": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_runtime_generated": False,
        "export_download_public_delivery_created": False,
        "generated_response_text": False,
        "route_ready": import_candidate_set["route_ready"],
        "frontend_ready": import_candidate_set["frontend_ready"],
        "production_ready": import_candidate_set["production_ready"],
        "customer_ready": import_candidate_set["customer_ready"],
        "public_ready": import_candidate_set["public_ready"],
        "raw_rows_exposed": False,
        "raw_comments_exposed": False,
        "raw_identities_exposed": False,
        "author_names_or_profile_urls_exposed": False,
        "secrets_read": False,
    }


def _assert_no_production_side_effects(smoke: dict[str, Any]) -> None:
    for flag in (
        "actual_evidence_layer_write_used",
        "evidence_layer_write",
        "production_evidence_item_created",
        "production_case_created",
        "production_analysis_run_created",
        "actual_review_queue_runtime_used",
        "production_review_queue_item_created",
        "review_queue_item_created",
        "source11_runtime_called",
        "actual_final_summary_report_created",
        "b_end_report_runtime_generated",
        "sandbox_public_event_runtime_generated",
        "export_download_public_delivery_created",
        "generated_response_text",
        "route_ready",
        "frontend_ready",
        "production_ready",
        "customer_ready",
        "public_ready",
        "raw_rows_exposed",
        "raw_comments_exposed",
        "raw_identities_exposed",
        "author_names_or_profile_urls_exposed",
        "secrets_read",
    ):
        assert smoke[flag] is False, flag

    candidate_set = smoke.get("evidence_layer_import_candidate_set")
    if isinstance(candidate_set, dict):
        runtime_side_effects = candidate_set["runtime_side_effects"]
        assert isinstance(runtime_side_effects, dict)
        for flag, value in runtime_side_effects.items():
            assert value is False, flag


def _fail_if_called(*args: object, **kwargs: object) -> None:
    raise AssertionError("8Y-10 must not call write, production, route, frontend, or delivery helpers")


def _patch_optional(monkeypatch: pytest.MonkeyPatch, module: object, name: str) -> None:
    if hasattr(module, name):
        monkeypatch.setattr(module, name, _fail_if_called)


def _patch_forbidden_entrypoints(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "create_review_queue_initialization",
        "create_review_queue_item_action",
        "create_review_queue_completion_gate",
        "create_final_summary_report",
        "create_report_export_download_package_artifact",
        "create_report_export_public_access_external_delivery_gate",
    ):
        _patch_optional(monkeypatch, analysis_request_store, name)
    _patch_optional(monkeypatch, write_candidate_module, "build_controlled_evidence_layer_write_candidate_set")
    _patch_optional(
        monkeypatch,
        write_from_production_import_module,
        "build_controlled_evidence_layer_write_candidate_from_production_import_candidate_set",
    )
    _patch_optional(
        monkeypatch,
        evidenceitem_write_module,
        "build_controlled_evidenceitem_evidence_layer_write_runtime",
    )
    _patch_optional(monkeypatch, production_import_module, "build_controlled_production_evidence_import_candidate_set")
    _patch_optional(monkeypatch, production_case_module, "build_controlled_production_case_candidate_set")
    _patch_optional(
        monkeypatch,
        production_analysis_run_module,
        "build_controlled_production_analysis_run_candidate_set",
    )


def test_8y10_builds_local_import_candidate_from_controlled_review_queue_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert ROW_PREVIEW_APPROVAL_PHRASE == "APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION"
    assert import_candidate_module.APPROVAL_PHRASE == (
        "APPROVE_8W_16_CONTROLLED_EVIDENCE_LAYER_IMPORT_CANDIDATE_IMPLEMENTATION"
    )
    _patch_forbidden_entrypoints(monkeypatch)

    smoke = _build_8y10_source_path_smoke(approval_phrase=EIGHT_Y10_APPROVAL_PHRASE)

    assert smoke["smoke_status"] == "ready"
    assert smoke["source_path_step"] == "review_queue_candidate_to_evidence_layer_import_candidate"
    assert smoke["evidence_layer_import_candidate_created"] is True
    assert smoke["import_candidate_created"] is True
    assert smoke["import_candidate_schema"] == "sentigraph_controlled_evidence_layer_import_candidate_set_v0_1"
    assert smoke["import_candidate_mode"] == "backend_only_local_evidence_layer_import_candidate_boundary"
    assert smoke["source_review_queue_candidate_set_schema"] == "sentigraph_controlled_review_queue_candidate_set_v0_1"
    assert smoke["source_review_queue_candidate_schema"] == "sentigraph_controlled_review_queue_candidate_v0_1"
    assert smoke["evidence_layer_import_candidate_count"] > 0
    assert smoke["evidence_layer_import_candidate_count"] <= smoke["source_review_queue_candidate_count"] <= 10
    assert smoke["human_review_required"] is True
    assert smoke["no_automatic_trust_upgrade"] is True
    _assert_no_production_side_effects(smoke)
    _assert_no_forbidden_output(smoke)

    candidate_set = smoke["evidence_layer_import_candidate_set"]
    assert candidate_set["evidence_layer_import_candidate_set_status"] == (
        "evidence_layer_import_candidate_set_warn_manual_review_required"
    )
    assert "manual_review_required" in candidate_set["warnings"]
    for candidate in candidate_set["evidence_layer_import_candidates"]:
        assert candidate["evidence_layer_import_candidate_schema"] == (
            "sentigraph_controlled_evidence_layer_import_candidate_v0_1"
        )
        assert candidate["source_review_queue_candidate_set_schema"] == (
            "sentigraph_controlled_review_queue_candidate_set_v0_1"
        )
        assert candidate["source_review_queue_candidate_schema"] == (
            "sentigraph_controlled_review_queue_candidate_v0_1"
        )
        assert candidate["human_review_required"] is True
        assert candidate["preview_only"] is True
        assert candidate["import_candidate_only"] is True
        assert candidate["boundary_flags"]["not_evidence_item"] is True
        assert candidate["boundary_flags"]["no_evidence_layer_write"] is True
        assert candidate["boundary_flags"]["not_production_case"] is True
        assert candidate["boundary_flags"]["not_production_analysis_run"] is True


@pytest.mark.parametrize(
    "approval_phrase",
    [
        None,
        "",
        "wrong approval",
        EIGHT_Y8_APPROVAL_PHRASE,
        EIGHT_Y6_APPROVAL_PHRASE,
        OLD_DIRECT_IMPORT_APPROVAL_PHRASE,
    ],
)
def test_8y10_phrase_required_before_import_candidate_creation(
    approval_phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_import_builder(*args: object, **kwargs: object) -> None:
        raise AssertionError("import candidate helper must not be called without 8Y-10 approval")

    monkeypatch.setattr(import_candidate_module, "build_controlled_evidence_layer_import_candidate_set", fail_import_builder)
    _patch_forbidden_entrypoints(monkeypatch)

    smoke = _build_8y10_source_path_smoke(approval_phrase=approval_phrase)

    assert smoke["smoke_status"] == "blocked"
    assert smoke["evidence_layer_import_candidate_created"] is False
    assert smoke["import_candidate_created"] is False
    assert smoke["evidence_layer_import_candidate_count"] == 0
    assert smoke["blockers"] == ["blocked_missing_exact_8y10_approval"]
    _assert_no_production_side_effects(smoke)
    _assert_no_forbidden_output(smoke)


@pytest.mark.parametrize(
    ("field", "value", "expected_blocker"),
    [
        ("review_queue_candidate_set_schema", "wrong", "source_review_queue_candidate_set_schema_wrong"),
        ("raw_rows_exposed", True, "blocked_source_review_queue_candidate_raw_rows_exposed"),
        ("raw_comments_exposed", True, "blocked_source_review_queue_candidate_raw_comments_exposed"),
        ("raw_identities_exposed", True, "blocked_source_review_queue_candidate_raw_identities_exposed"),
        (
            "author_names_or_profile_urls_exposed",
            True,
            "blocked_source_review_queue_candidate_author_names_or_profile_urls_exposed",
        ),
        ("evidence_layer_write", True, "blocked_source_review_queue_candidate_evidence_layer_write"),
        (
            "production_evidence_item_created",
            True,
            "blocked_source_review_queue_candidate_production_evidence_item_created",
        ),
        ("production_case_created", True, "blocked_source_review_queue_candidate_production_case_created"),
        (
            "production_analysis_run_created",
            True,
            "blocked_source_review_queue_candidate_production_analysis_run_created",
        ),
        (
            "actual_review_queue_runtime_used",
            True,
            "blocked_source_review_queue_candidate_actual_review_queue_runtime_used",
        ),
        (
            "production_review_queue_item_created",
            True,
            "blocked_source_review_queue_candidate_production_review_queue_item_created",
        ),
        ("review_queue_item_created", True, "blocked_source_review_queue_candidate_review_queue_item_created"),
        ("no_automatic_trust_upgrade", False, "source_no_automatic_trust_upgrade_not_true"),
    ],
)
def test_unsafe_source_review_queue_candidate_blocks_before_import_candidate_creation(
    field: str,
    value: object,
    expected_blocker: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_import_builder(*args: object, **kwargs: object) -> None:
        raise AssertionError("import candidate helper must not be called for unsafe review queue candidate source")

    source_candidate_set = _safe_review_queue_candidate_set()
    source_candidate_set[field] = value
    monkeypatch.setattr(import_candidate_module, "build_controlled_evidence_layer_import_candidate_set", fail_import_builder)
    _patch_forbidden_entrypoints(monkeypatch)

    smoke = _build_8y10_source_path_smoke(
        approval_phrase=EIGHT_Y10_APPROVAL_PHRASE,
        source_review_queue_candidate_set=source_candidate_set,
    )

    assert smoke["smoke_status"] == "blocked"
    assert smoke["evidence_layer_import_candidate_created"] is False
    assert smoke["import_candidate_created"] is False
    assert smoke["evidence_layer_import_candidate_count"] == 0
    assert expected_blocker in smoke["blockers"]
    _assert_no_production_side_effects(smoke)
    _assert_no_forbidden_output(smoke)


@pytest.mark.parametrize(
    ("runtime_flag", "expected_blocker"),
    [
        ("emitted_raw_comments", "blocked_source_review_queue_candidate_runtime_emitted_raw_comments"),
        ("emitted_raw_identities", "blocked_source_review_queue_candidate_runtime_emitted_raw_identities"),
        ("emitted_profile_urls", "blocked_source_review_queue_candidate_runtime_emitted_profile_urls"),
        ("created_review_queue_items", "blocked_source_review_queue_candidate_runtime_created_review_queue_items"),
        (
            "created_production_review_queue_items",
            "blocked_source_review_queue_candidate_runtime_created_production_review_queue_items",
        ),
        ("wrote_evidence_layer", "blocked_source_review_queue_candidate_runtime_wrote_evidence_layer"),
        ("created_evidence_items", "blocked_source_review_queue_candidate_runtime_created_evidence_items"),
        ("read_original_package_rows", "blocked_source_review_queue_candidate_runtime_read_original_package_rows"),
        ("parsed_evidence_items_csv", "blocked_source_review_queue_candidate_runtime_parsed_evidence_items_csv"),
    ],
)
def test_unsafe_source_review_queue_candidate_runtime_flags_block(
    runtime_flag: str,
    expected_blocker: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_import_builder(*args: object, **kwargs: object) -> None:
        raise AssertionError("import candidate helper must not be called for unsafe runtime flags")

    source_candidate_set = _safe_review_queue_candidate_set()
    runtime_side_effects = dict(source_candidate_set["runtime_side_effects"])
    runtime_side_effects[runtime_flag] = True
    source_candidate_set["runtime_side_effects"] = runtime_side_effects
    monkeypatch.setattr(import_candidate_module, "build_controlled_evidence_layer_import_candidate_set", fail_import_builder)
    _patch_forbidden_entrypoints(monkeypatch)

    smoke = _build_8y10_source_path_smoke(
        approval_phrase=EIGHT_Y10_APPROVAL_PHRASE,
        source_review_queue_candidate_set=source_candidate_set,
    )

    assert smoke["smoke_status"] == "blocked"
    assert expected_blocker in smoke["blockers"]
    assert smoke["evidence_layer_import_candidate_created"] is False
    assert smoke["import_candidate_created"] is False
    _assert_no_production_side_effects(smoke)
    _assert_no_forbidden_output(smoke)
