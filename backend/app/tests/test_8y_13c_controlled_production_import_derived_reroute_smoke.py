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
import app.services.evidence_import as evidence_import_module
import app.services.evidence_ingestion as evidence_ingestion_module
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


EIGHT_Y13C_APPROVAL_PHRASE = "APPROVE_8Y_13C_CONTROLLED_PRODUCTION_IMPORT_DERIVED_REROUTE_SMOKE"
EIGHT_Y12_APPROVAL_PHRASE = "APPROVE_8Y_12_CONTROLLED_EVIDENCE_LAYER_IMPORT_CANDIDATE_TO_WRITE_CANDIDATE_SMOKE"
EIGHT_Y10_APPROVAL_PHRASE = (
    "APPROVE_8Y_10_CONTROLLED_REVIEW_QUEUE_CANDIDATE_TO_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE"
)
EIGHT_Y8_APPROVAL_PHRASE = "APPROVE_8Y_8_CONTROLLED_EVIDENCE_CANDIDATE_TO_REVIEW_QUEUE_CANDIDATE_SMOKE"
EIGHT_Y6_APPROVAL_PHRASE = "APPROVE_8Y_6_CONTROLLED_ROW_PREVIEW_TO_EVIDENCE_CANDIDATE_SOURCE_PATH_SMOKE"
OLD_DIRECT_IMPORT_APPROVAL_PHRASE = (
    "APPROVE_8Y_6_CONTROLLED_REDACTED_ROW_PREVIEW_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE"
)
OLD_EIGHT_Y14_APPROVAL_PHRASE = "APPROVE_8Y_14_CONTROLLED_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_SMOKE"

SOURCE_WRITE_BLOCKED_TRUE_FLAGS = {
    "actual_evidence_layer_write_used",
    "evidence_layer_write",
    "persisted_evidence_layer_record_created",
    "production_evidence_item_created",
    "production_case_created",
    "production_analysis_run_created",
    "evidence_import_service_called",
    "evidence_ingestion_service_called",
    "production_evidenceitem_write_runtime_used",
    "actual_review_queue_runtime_used",
    "production_review_queue_item_created",
    "raw_rows_exposed",
    "raw_comments_exposed",
    "raw_identities_exposed",
    "raw_author_ids_emitted",
    "raw_author_names_emitted",
    "profile_urls_emitted",
    "author_names_or_profile_urls_exposed",
    "secrets_read",
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
    "psychological_profile",
    "personality_diagnosis",
}

FALSE_SIDE_EFFECT_FLAGS = (
    "controlled_evidenceitem_write_runtime_called",
    "production_evidenceitem_write_runtime_used",
    "actual_evidence_layer_write_used",
    "evidence_layer_write",
    "persisted_evidence_layer_record_created",
    "production_evidence_item_created",
    "production_case_created",
    "production_analysis_run_created",
    "production_analysis_result_creation_authorized",
    "evidence_import_service_called",
    "evidence_ingestion_service_called",
    "actual_review_queue_runtime_used",
    "production_review_queue_item_created",
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
    "raw_author_ids_emitted",
    "raw_author_names_emitted",
    "profile_urls_emitted",
    "author_names_or_profile_urls_exposed",
    "secrets_read",
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
    candidate_set = review_queue_module.build_controlled_review_queue_candidate_set(
        _safe_evidence_candidate_set(),
        exact_approval_phrase=review_queue_module.APPROVAL_PHRASE,
    )
    candidate_set["no_automatic_trust_upgrade"] = True
    candidate_set["actual_review_queue_runtime_used"] = False
    candidate_set["actual_evidence_layer_write_used"] = False
    candidate_set["raw_rows_exposed"] = False
    candidate_set["raw_comments_exposed"] = False
    candidate_set["raw_identities_exposed"] = False
    candidate_set["author_names_or_profile_urls_exposed"] = False
    candidate_set["secrets_read"] = False
    return candidate_set


def _safe_import_candidate_set() -> dict[str, Any]:
    candidate_set = import_candidate_module.build_controlled_evidence_layer_import_candidate_set(
        _safe_review_queue_candidate_set(),
        exact_approval_phrase=import_candidate_module.APPROVAL_PHRASE,
    )
    candidate_set["no_automatic_trust_upgrade"] = True
    candidate_set["actual_evidence_layer_write_used"] = False
    candidate_set["persisted_evidence_layer_record_created"] = False
    candidate_set["actual_review_queue_runtime_used"] = False
    candidate_set["raw_rows_exposed"] = False
    candidate_set["raw_comments_exposed"] = False
    candidate_set["raw_identities_exposed"] = False
    candidate_set["raw_author_ids_emitted"] = False
    candidate_set["raw_author_names_emitted"] = False
    candidate_set["profile_urls_emitted"] = False
    candidate_set["author_names_or_profile_urls_exposed"] = False
    candidate_set["secrets_read"] = False
    return candidate_set


def _safe_direct_write_candidate_set() -> dict[str, Any]:
    candidate_set = write_candidate_module.build_controlled_evidence_layer_write_candidate_set(
        _safe_import_candidate_set(),
        exact_approval_phrase=write_candidate_module.APPROVAL_PHRASE,
    )
    candidate_set["no_automatic_trust_upgrade"] = True
    candidate_set["actual_evidence_layer_write_used"] = False
    candidate_set["persisted_evidence_layer_record_created"] = False
    candidate_set["evidence_import_service_called"] = False
    candidate_set["evidence_ingestion_service_called"] = False
    candidate_set["production_evidenceitem_write_runtime_used"] = False
    candidate_set["actual_review_queue_runtime_used"] = False
    candidate_set["raw_rows_exposed"] = False
    candidate_set["raw_comments_exposed"] = False
    candidate_set["raw_identities_exposed"] = False
    candidate_set["raw_author_ids_emitted"] = False
    candidate_set["raw_author_names_emitted"] = False
    candidate_set["profile_urls_emitted"] = False
    candidate_set["author_names_or_profile_urls_exposed"] = False
    candidate_set["secrets_read"] = False
    return candidate_set


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
    assert "g:\\" not in serialized
    assert "c:\\users" not in serialized
    assert ":/" not in serialized


def _blocked_8y13c_output(reason: str) -> dict[str, Any]:
    blocked = {
        "schema": "sentigraph_8y13c_controlled_production_import_derived_reroute_smoke_v0_1",
        "phase": "8Y-13C",
        "source_path_step": "direct_write_candidate_to_production_import_derived_write_candidate",
        "smoke_status": "blocked",
        "production_evidence_import_candidate_created": False,
        "production_import_candidate_created": False,
        "production_import_candidate_schema": None,
        "production_import_candidate_mode": None,
        "production_import_derived_write_candidate_created": False,
        "production_import_derived_write_candidate_schema": None,
        "write_candidate_from_production_import_candidate_mode": None,
        "source_direct_write_candidate_schema": None,
        "source_direct_write_candidate_count": 0,
        "production_import_candidate_count": 0,
        "production_import_derived_write_candidate_count": 0,
        "blockers": [reason],
        "warnings": [],
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
    }
    blocked.update({flag: False for flag in FALSE_SIDE_EFFECT_FLAGS})
    return blocked


def _source_direct_write_candidate_blockers(source_candidate_set: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if (
        source_candidate_set.get("evidence_layer_write_candidate_set_schema")
        != "sentigraph_controlled_evidence_layer_write_candidate_set_v0_1"
    ):
        blockers.append("source_direct_write_candidate_schema_wrong")
    if source_candidate_set.get("no_automatic_trust_upgrade") is not True:
        blockers.append("source_no_automatic_trust_upgrade_not_true")
    for flag in SOURCE_WRITE_BLOCKED_TRUE_FLAGS:
        if source_candidate_set.get(flag) is True:
            blockers.append(f"blocked_source_direct_write_candidate_{flag}")
    return blockers


def _build_8y13c_reroute_smoke(
    *,
    approval_phrase: str | None,
    source_direct_write_candidate_set: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if approval_phrase != EIGHT_Y13C_APPROVAL_PHRASE:
        return _blocked_8y13c_output("blocked_missing_exact_8y13c_approval")

    source_candidate_set = source_direct_write_candidate_set or _safe_direct_write_candidate_set()
    source_blockers = _source_direct_write_candidate_blockers(source_candidate_set)
    if source_blockers:
        return _blocked_8y13c_output(source_blockers[0])

    production_import_candidate_set = production_import_module.build_controlled_production_evidence_import_candidate_set(
        source_candidate_set,
        exact_approval_phrase=production_import_module.APPROVAL_PHRASE,
    )
    if not production_import_candidate_set.get("production_evidence_import_candidate_created"):
        return _blocked_8y13c_output("production_import_candidate_not_created")

    derived_write_candidate_set = (
        write_from_production_import_module
        .build_controlled_evidence_layer_write_candidate_from_production_import_candidate_set(
            production_import_candidate_set,
            exact_approval_phrase=write_from_production_import_module.APPROVAL_PHRASE,
        )
    )
    if not derived_write_candidate_set.get("evidence_layer_write_candidate_created"):
        return _blocked_8y13c_output("production_import_derived_write_candidate_not_created")

    return {
        "schema": "sentigraph_8y13c_controlled_production_import_derived_reroute_smoke_v0_1",
        "phase": "8Y-13C",
        "source_path_step": "direct_write_candidate_to_production_import_derived_write_candidate",
        "smoke_status": "ready",
        "production_evidence_import_candidate_created": True,
        "production_import_candidate_created": True,
        "production_import_candidate_schema": production_import_candidate_set[
            "production_evidence_import_candidate_set_schema"
        ],
        "production_import_candidate_mode": production_import_candidate_set[
            "production_evidence_import_candidate_mode"
        ],
        "production_import_candidate_count": production_import_candidate_set[
            "production_evidence_import_candidate_count"
        ],
        "production_import_derived_write_candidate_created": True,
        "production_import_derived_write_candidate_schema": derived_write_candidate_set[
            "evidence_layer_write_candidate_set_schema"
        ],
        "write_candidate_from_production_import_candidate_mode": derived_write_candidate_set[
            "evidence_layer_write_candidate_mode"
        ],
        "production_import_derived_write_candidate_count": derived_write_candidate_set[
            "evidence_layer_write_candidate_count"
        ],
        "source_direct_write_candidate_schema": source_candidate_set["evidence_layer_write_candidate_set_schema"],
        "source_direct_write_candidate_count": source_candidate_set["evidence_layer_write_candidate_count"],
        "production_import_candidate_set": production_import_candidate_set,
        "production_import_derived_write_candidate_set": derived_write_candidate_set,
        "blockers": [],
        "warnings": list(derived_write_candidate_set["warnings"]),
        "human_review_required": derived_write_candidate_set["human_review_required"],
        "no_automatic_trust_upgrade": True,
        **{flag: False for flag in FALSE_SIDE_EFFECT_FLAGS},
    }


def _assert_no_production_side_effects(smoke: dict[str, Any]) -> None:
    for flag in FALSE_SIDE_EFFECT_FLAGS:
        assert smoke[flag] is False, flag

    for key in ("production_import_candidate_set", "production_import_derived_write_candidate_set"):
        candidate_set = smoke.get(key)
        if isinstance(candidate_set, dict):
            runtime_side_effects = candidate_set["runtime_side_effects"]
            assert isinstance(runtime_side_effects, dict)
            for flag, value in runtime_side_effects.items():
                assert value is False, f"{key}:{flag}"


def _fail_if_called(*args: object, **kwargs: object) -> None:
    raise AssertionError("8Y-13C must not call write runtime, production services, route, frontend, or delivery helpers")


def _patch_optional(monkeypatch: pytest.MonkeyPatch, module: object, name: str) -> None:
    if hasattr(module, name):
        monkeypatch.setattr(module, name, _fail_if_called)


def _patch_forbidden_entrypoints(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "build_imported_evidence_items",
        "build_evidence_import_commit_result",
        "preview_evidence_import",
    ):
        _patch_optional(monkeypatch, evidence_import_module, name)
    for name in (
        "build_evidence_items_from_raw_data",
        "raw_post_to_evidence_item",
        "raw_comment_to_evidence_item",
        "normalize_manual_evidence_batch",
        "build_evidence_ingestion_result",
        "enrich_and_deduplicate_evidence_items",
        "merge_evidence_items",
        "build_review_summary",
        "apply_review_decision",
    ):
        _patch_optional(monkeypatch, evidence_ingestion_module, name)
    for name in (
        "build_controlled_evidenceitem_evidence_layer_write_runtime",
        "create_controlled_evidenceitem_evidence_layer_write_runtime",
        "build_safe_controlled_evidenceitem_evidence_layer_write_runtime_summary",
    ):
        _patch_optional(monkeypatch, evidenceitem_write_module, name)
    for name in ("build_controlled_production_case_candidate_set",):
        _patch_optional(monkeypatch, production_case_module, name)
    for name in ("build_controlled_production_analysis_run_candidate_set",):
        _patch_optional(monkeypatch, production_analysis_run_module, name)
    for name in (
        "create_review_queue_initialization",
        "create_review_queue_item_action",
        "create_review_queue_completion_gate",
        "create_final_summary_report",
        "create_report_export_download_package_artifact",
        "create_report_export_public_access_external_delivery_gate",
    ):
        _patch_optional(monkeypatch, analysis_request_store, name)


def test_8y13c_builds_production_import_derived_write_candidate_without_write_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert ROW_PREVIEW_APPROVAL_PHRASE == "APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION"
    assert [hex(ord(ch)) for ch in production_import_module.APPROVAL_PHRASE[:2]] == ["0x6279", "0x51c6"]
    assert [hex(ord(ch)) for ch in write_from_production_import_module.APPROVAL_PHRASE[:2]] == [
        "0x6279",
        "0x51c6",
    ]
    _patch_forbidden_entrypoints(monkeypatch)

    smoke = _build_8y13c_reroute_smoke(approval_phrase=EIGHT_Y13C_APPROVAL_PHRASE)

    assert smoke["smoke_status"] == "ready"
    assert smoke["source_path_step"] == "direct_write_candidate_to_production_import_derived_write_candidate"
    assert smoke["source_direct_write_candidate_schema"] == (
        "sentigraph_controlled_evidence_layer_write_candidate_set_v0_1"
    )
    assert smoke["production_evidence_import_candidate_created"] is True
    assert smoke["production_import_candidate_created"] is True
    assert smoke["production_import_candidate_schema"] == (
        "sentigraph_controlled_production_evidence_import_candidate_set_v0_1"
    )
    assert smoke["production_import_candidate_mode"] == (
        "backend_only_local_production_evidence_import_candidate_boundary"
    )
    assert smoke["production_import_derived_write_candidate_created"] is True
    assert smoke["production_import_derived_write_candidate_schema"] == (
        "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1"
    )
    assert smoke["write_candidate_from_production_import_candidate_mode"] == (
        "backend_only_local_evidence_layer_write_candidate_boundary"
    )
    assert 0 < smoke["production_import_candidate_count"] <= smoke["source_direct_write_candidate_count"] <= 10
    assert (
        smoke["production_import_derived_write_candidate_count"]
        <= smoke["production_import_candidate_count"]
        <= smoke["source_direct_write_candidate_count"]
    )
    assert smoke["human_review_required"] is True
    assert smoke["no_automatic_trust_upgrade"] is True
    assert "manual_review_required" in smoke["warnings"]
    _assert_no_production_side_effects(smoke)
    _assert_no_forbidden_output(smoke)

    production_import_candidates = smoke["production_import_candidate_set"]["production_evidence_import_candidates"]
    derived_write_candidates = smoke["production_import_derived_write_candidate_set"]["evidence_layer_write_candidates"]
    assert len(production_import_candidates) == len(derived_write_candidates)

    for candidate in production_import_candidates:
        assert candidate["production_evidence_import_candidate_schema"] == (
            "sentigraph_controlled_production_evidence_import_candidate_v0_1"
        )
        assert candidate["human_review_required"] is True
        assert candidate["production_import_candidate_only"] is True
        assert candidate["boundary_flags"]["not_production_evidence_item"] is True
        assert candidate["boundary_flags"]["no_evidence_layer_write"] is True
        assert candidate["boundary_flags"]["not_production_case"] is True
        assert candidate["boundary_flags"]["not_production_analysis_run"] is True

    for candidate in derived_write_candidates:
        assert candidate["evidence_layer_write_candidate_schema"] == (
            "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_v0_1"
        )
        assert candidate["human_review_required"] is True
        assert candidate["production_import_candidate_only"] is True
        assert candidate["evidence_layer_write_candidate_only"] is True
        assert candidate["boundary_flags"]["not_production_evidence_item"] is True
        assert candidate["boundary_flags"]["no_evidence_layer_write"] is True
        assert candidate["boundary_flags"]["not_production_case"] is True
        assert candidate["boundary_flags"]["not_production_analysis_run"] is True


@pytest.mark.parametrize(
    "approval_phrase",
    [
        None,
        "",
        "wrong approval",
        EIGHT_Y12_APPROVAL_PHRASE,
        EIGHT_Y10_APPROVAL_PHRASE,
        EIGHT_Y8_APPROVAL_PHRASE,
        EIGHT_Y6_APPROVAL_PHRASE,
        OLD_DIRECT_IMPORT_APPROVAL_PHRASE,
        OLD_EIGHT_Y14_APPROVAL_PHRASE,
    ],
)
def test_8y13c_phrase_required_before_reroute_candidate_creation(
    approval_phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        production_import_module,
        "build_controlled_production_evidence_import_candidate_set",
        _fail_if_called,
    )
    monkeypatch.setattr(
        write_from_production_import_module,
        "build_controlled_evidence_layer_write_candidate_from_production_import_candidate_set",
        _fail_if_called,
    )
    _patch_forbidden_entrypoints(monkeypatch)

    smoke = _build_8y13c_reroute_smoke(approval_phrase=approval_phrase)

    assert smoke["smoke_status"] == "blocked"
    assert smoke["production_evidence_import_candidate_created"] is False
    assert smoke["production_import_candidate_created"] is False
    assert smoke["production_import_derived_write_candidate_created"] is False
    assert smoke["blockers"] == ["blocked_missing_exact_8y13c_approval"]
    _assert_no_production_side_effects(smoke)
    _assert_no_forbidden_output(smoke)


@pytest.mark.parametrize(
    ("field", "value", "expected_blocker"),
    [
        ("evidence_layer_write_candidate_set_schema", "wrong", "source_direct_write_candidate_schema_wrong"),
        ("actual_evidence_layer_write_used", True, "blocked_source_direct_write_candidate_actual_evidence_layer_write_used"),
        ("evidence_layer_write", True, "blocked_source_direct_write_candidate_evidence_layer_write"),
        (
            "persisted_evidence_layer_record_created",
            True,
            "blocked_source_direct_write_candidate_persisted_evidence_layer_record_created",
        ),
        ("production_evidence_item_created", True, "blocked_source_direct_write_candidate_production_evidence_item_created"),
        ("production_case_created", True, "blocked_source_direct_write_candidate_production_case_created"),
        ("production_analysis_run_created", True, "blocked_source_direct_write_candidate_production_analysis_run_created"),
        ("evidence_import_service_called", True, "blocked_source_direct_write_candidate_evidence_import_service_called"),
        ("evidence_ingestion_service_called", True, "blocked_source_direct_write_candidate_evidence_ingestion_service_called"),
        (
            "production_evidenceitem_write_runtime_used",
            True,
            "blocked_source_direct_write_candidate_production_evidenceitem_write_runtime_used",
        ),
        ("raw_rows_exposed", True, "blocked_source_direct_write_candidate_raw_rows_exposed"),
        ("raw_comments_exposed", True, "blocked_source_direct_write_candidate_raw_comments_exposed"),
        ("raw_identities_exposed", True, "blocked_source_direct_write_candidate_raw_identities_exposed"),
        (
            "author_names_or_profile_urls_exposed",
            True,
            "blocked_source_direct_write_candidate_author_names_or_profile_urls_exposed",
        ),
        ("no_automatic_trust_upgrade", False, "source_no_automatic_trust_upgrade_not_true"),
    ],
)
def test_8y13c_blocks_unsafe_direct_write_candidate_source_before_reroute(
    field: str,
    value: object,
    expected_blocker: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = _safe_direct_write_candidate_set()
    source[field] = value
    monkeypatch.setattr(
        production_import_module,
        "build_controlled_production_evidence_import_candidate_set",
        _fail_if_called,
    )
    monkeypatch.setattr(
        write_from_production_import_module,
        "build_controlled_evidence_layer_write_candidate_from_production_import_candidate_set",
        _fail_if_called,
    )
    _patch_forbidden_entrypoints(monkeypatch)

    smoke = _build_8y13c_reroute_smoke(
        approval_phrase=EIGHT_Y13C_APPROVAL_PHRASE,
        source_direct_write_candidate_set=source,
    )

    assert smoke["smoke_status"] == "blocked"
    assert smoke["production_import_candidate_created"] is False
    assert smoke["production_import_derived_write_candidate_created"] is False
    assert smoke["blockers"] == [expected_blocker]
    _assert_no_production_side_effects(smoke)
    _assert_no_forbidden_output(smoke)
