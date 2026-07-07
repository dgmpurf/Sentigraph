from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import app.services.controlled_evidence_candidate as evidence_candidate_module
import app.services.controlled_evidence_layer_import_candidate as import_candidate_module
import app.services.controlled_review_queue_candidate as review_queue_module
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


EIGHT_Y6_APPROVAL_PHRASE = "APPROVE_8Y_6_CONTROLLED_ROW_PREVIEW_TO_EVIDENCE_CANDIDATE_SOURCE_PATH_SMOKE"
OLD_DIRECT_IMPORT_APPROVAL_PHRASE = (
    "APPROVE_8Y_6_CONTROLLED_REDACTED_ROW_PREVIEW_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE"
)
EVIDENCE_CANDIDATE_APPROVAL_PHRASE = "APPROVE_8W_10_CONTROLLED_EVIDENCE_CANDIDATE_IMPLEMENTATION"
OLD_CHINESE_EVIDENCE_CANDIDATE_APPROVAL_PHRASE = (
    "批准 8W-10 Controlled Evidence Candidate Helper Implementation"
)
OLD_MOJIBAKE_EVIDENCE_CANDIDATE_APPROVAL_PHRASE = (
    "鎵瑰噯 8W-10 Controlled Evidence Candidate Helper Implementation"
)
OLD_GARBLED_EVIDENCE_CANDIDATE_APPROVAL_PHRASE = (
    "閹电懓鍣?8W-10 Controlled Evidence Candidate Helper Implementation"
)

SOURCE_PREVIEW_BLOCKED_TRUE_FLAGS = {
    "raw_rows_exposed",
    "raw_comments_exposed",
    "raw_identities_exposed",
    "author_names_or_profile_urls_exposed",
    "evidence_layer_write",
    "production_evidence_item_created",
    "production_case_created",
    "production_analysis_run_created",
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


def _safe_8w4_boundary() -> dict[str, Any]:
    return build_metadata_smoke_review_only_staging_boundary(_safe_8w2_smoke())


def _safe_row_preview() -> dict[str, Any]:
    return build_controlled_row_preview(
        _safe_8w4_boundary(),
        approval_phrase=ROW_PREVIEW_APPROVAL_PHRASE,
        max_preview_rows=5,
        row_source=APPROVED_ROW_SOURCE,
    )


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


def _false_or_absent(value: dict[str, Any], key: str) -> bool:
    return value.get(key) is not True


def _blocked_8y6_output(reason: str) -> dict[str, Any]:
    return {
        "schema": "sentigraph_8y6_row_preview_to_evidence_candidate_source_path_smoke_v0_1",
        "phase": "8Y-6",
        "source_path_step": "row_preview_to_evidence_candidate",
        "smoke_status": "blocked",
        "evidence_candidate_created": False,
        "evidence_candidate_schema": None,
        "evidence_candidate_mode": None,
        "source_preview_schema": None,
        "candidate_count": 0,
        "blockers": [reason],
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "evidence_layer_write": False,
        "production_evidence_item_created": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "review_queue_runtime_used": False,
        "import_candidate_created": False,
        "evidence_layer_import_candidate_created": False,
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
    }


def _source_preview_gate_blockers(source_preview: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    for flag in SOURCE_PREVIEW_BLOCKED_TRUE_FLAGS:
        if source_preview.get(flag) is True:
            blockers.append(f"blocked_source_preview_{flag}")
    runtime_side_effects = source_preview.get("runtime_side_effects")
    if isinstance(runtime_side_effects, dict):
        for flag in (
            "emitted_raw_comments",
            "emitted_raw_identities",
            "emitted_profile_urls",
            "read_original_package_rows",
            "parsed_evidence_items_csv",
            "parsed_source_manifest_jsonl_rows",
            "parsed_collection_log_jsonl_rows",
        ):
            if runtime_side_effects.get(flag) is True:
                blockers.append(f"blocked_source_preview_runtime_{flag}")
    return blockers


def _build_8y6_source_path_smoke(
    *,
    approval_phrase: str | None,
    source_preview: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if approval_phrase != EIGHT_Y6_APPROVAL_PHRASE:
        return _blocked_8y6_output("blocked_missing_exact_8y6_approval")

    preview = source_preview if source_preview is not None else _safe_row_preview()
    preview_blockers = _source_preview_gate_blockers(preview)
    if preview_blockers:
        return _blocked_8y6_output(preview_blockers[0])

    candidate_set = evidence_candidate_module.build_controlled_evidence_candidate_set(
        preview,
        exact_approval_phrase=EVIDENCE_CANDIDATE_APPROVAL_PHRASE,
    )

    return {
        "schema": "sentigraph_8y6_row_preview_to_evidence_candidate_source_path_smoke_v0_1",
        "phase": "8Y-6",
        "source_path_step": "row_preview_to_evidence_candidate",
        "smoke_status": "ready" if candidate_set["evidence_candidate_created"] else "blocked",
        "evidence_candidate_created": candidate_set["evidence_candidate_created"],
        "evidence_candidate_schema": candidate_set["candidate_set_schema"],
        "evidence_candidate_mode": candidate_set["candidate_mode"],
        "source_preview_schema": candidate_set["source_preview_schema"],
        "source_preview_rows_count": candidate_set["source_preview_rows_count"],
        "candidate_count": candidate_set["candidate_count"],
        "candidate_set": candidate_set,
        "blockers": list(candidate_set["blockers"]),
        "warnings": list(candidate_set["warnings"]),
        "human_review_required": candidate_set["human_review_required"],
        "no_automatic_trust_upgrade": True,
        "evidence_layer_write": candidate_set["evidence_layer_write"],
        "production_evidence_item_created": False,
        "production_case_created": candidate_set["production_case_created"],
        "production_analysis_run_created": candidate_set["production_analysis_run_created"],
        "review_queue_runtime_used": False,
        "import_candidate_created": False,
        "evidence_layer_import_candidate_created": False,
        "source11_runtime_called": False,
        "actual_final_summary_report_created": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_runtime_generated": False,
        "export_download_public_delivery_created": False,
        "generated_response_text": False,
        "route_ready": candidate_set["route_ready"],
        "frontend_ready": candidate_set["frontend_ready"],
        "production_ready": candidate_set["production_ready"],
        "customer_ready": candidate_set["customer_ready"],
        "public_ready": candidate_set["public_ready"],
    }


def _assert_no_production_side_effects(smoke: dict[str, Any]) -> None:
    for flag in (
        "evidence_layer_write",
        "production_evidence_item_created",
        "production_case_created",
        "production_analysis_run_created",
        "review_queue_runtime_used",
        "import_candidate_created",
        "evidence_layer_import_candidate_created",
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
    ):
        assert smoke[flag] is False, flag

    candidate_set = smoke.get("candidate_set")
    if isinstance(candidate_set, dict):
        runtime_side_effects = candidate_set["runtime_side_effects"]
        assert isinstance(runtime_side_effects, dict)
        for flag, value in runtime_side_effects.items():
            assert value is False, flag
        assert _false_or_absent(candidate_set, "production_evidence_item_created")
        assert _false_or_absent(candidate_set, "import_candidate_created")
        assert _false_or_absent(candidate_set, "evidence_layer_import_candidate_created")


def _fail_if_called(*args: object, **kwargs: object) -> None:
    raise AssertionError("8Y-6 must not call review queue or import candidate helpers")


def test_8y6_builds_local_evidence_candidate_from_controlled_row_preview(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert ROW_PREVIEW_APPROVAL_PHRASE == "APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION"
    assert evidence_candidate_module.APPROVAL_PHRASE == EVIDENCE_CANDIDATE_APPROVAL_PHRASE
    assert evidence_candidate_module.APPROVAL_PHRASE != OLD_CHINESE_EVIDENCE_CANDIDATE_APPROVAL_PHRASE
    assert evidence_candidate_module.APPROVAL_PHRASE != OLD_MOJIBAKE_EVIDENCE_CANDIDATE_APPROVAL_PHRASE
    assert evidence_candidate_module.APPROVAL_PHRASE != OLD_GARBLED_EVIDENCE_CANDIDATE_APPROVAL_PHRASE

    monkeypatch.setattr(review_queue_module, "build_controlled_review_queue_candidate_set", _fail_if_called)
    monkeypatch.setattr(import_candidate_module, "build_controlled_evidence_layer_import_candidate_set", _fail_if_called)

    smoke = _build_8y6_source_path_smoke(approval_phrase=EIGHT_Y6_APPROVAL_PHRASE)

    assert smoke["smoke_status"] == "ready"
    assert smoke["source_path_step"] == "row_preview_to_evidence_candidate"
    assert smoke["evidence_candidate_created"] is True
    assert smoke["evidence_candidate_schema"] == "sentigraph_controlled_evidence_candidate_set_v0_1"
    assert smoke["evidence_candidate_mode"] == "backend_only_local_preview_derived_evidence_candidate"
    assert smoke["source_preview_schema"] == "sentigraph_controlled_row_preview_v0_1"
    assert smoke["candidate_count"] > 0
    assert smoke["candidate_count"] <= smoke["source_preview_rows_count"] <= 10
    assert smoke["human_review_required"] is True
    assert smoke["no_automatic_trust_upgrade"] is True
    _assert_no_production_side_effects(smoke)
    _assert_no_forbidden_output(smoke)

    candidate_set = smoke["candidate_set"]
    assert candidate_set["candidate_set_status"] == "evidence_candidate_set_warn_manual_review_required"
    assert "manual_review_required" in candidate_set["warnings"]
    for candidate in candidate_set["candidates"]:
        assert candidate["candidate_schema"] == "sentigraph_controlled_evidence_candidate_v0_1"
        assert candidate["human_review_required"] is True
        assert candidate["boundary_flags"]["preview_only"] is True
        assert candidate["boundary_flags"]["not_evidence_item"] is True
        assert candidate["boundary_flags"]["no_evidence_layer_write"] is True


@pytest.mark.parametrize(
    "approval_phrase",
    [None, "", "wrong approval", OLD_DIRECT_IMPORT_APPROVAL_PHRASE],
)
def test_8y6_phrase_required_before_row_open_or_candidate_creation(
    approval_phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_candidate_builder(*args: object, **kwargs: object) -> None:
        raise AssertionError("candidate helper must not be called without 8Y-6 approval")

    def fail_open(*args: object, **kwargs: object) -> None:
        raise AssertionError("row source must not open without 8Y-6 approval")

    monkeypatch.setattr(evidence_candidate_module, "build_controlled_evidence_candidate_set", fail_candidate_builder)
    monkeypatch.setattr(Path, "open", fail_open)
    monkeypatch.setattr(Path, "read_text", fail_open)

    smoke = _build_8y6_source_path_smoke(approval_phrase=approval_phrase)

    assert smoke["smoke_status"] == "blocked"
    assert smoke["evidence_candidate_created"] is False
    assert smoke["candidate_count"] == 0
    assert smoke["blockers"] == ["blocked_missing_exact_8y6_approval"]
    _assert_no_production_side_effects(smoke)
    _assert_no_forbidden_output(smoke)


@pytest.mark.parametrize(
    "helper_phrase",
    [
        None,
        "",
        "wrong helper approval",
        OLD_CHINESE_EVIDENCE_CANDIDATE_APPROVAL_PHRASE,
        OLD_MOJIBAKE_EVIDENCE_CANDIDATE_APPROVAL_PHRASE,
        OLD_GARBLED_EVIDENCE_CANDIDATE_APPROVAL_PHRASE,
    ],
)
def test_old_or_missing_evidence_candidate_helper_phrase_is_rejected(helper_phrase: str | None) -> None:
    candidate_set = evidence_candidate_module.build_controlled_evidence_candidate_set(
        _safe_row_preview(),
        exact_approval_phrase=helper_phrase,
    )

    assert candidate_set["candidate_set_status"].startswith("blocked_")
    assert candidate_set["evidence_candidate_created"] is False
    assert candidate_set["candidate_count"] == 0
    assert candidate_set["blockers"] == ["blocked_missing_exact_approval"]
    _assert_no_forbidden_output(candidate_set)


@pytest.mark.parametrize(
    ("field", "value", "expected_blocker"),
    [
        ("schema", "wrong", "source_preview_schema_wrong"),
        ("raw_rows_exposed", True, "blocked_source_preview_raw_rows_exposed"),
        ("raw_comments_exposed", True, "blocked_source_preview_raw_comments_exposed"),
        ("raw_identities_exposed", True, "blocked_source_preview_raw_identities_exposed"),
        (
            "author_names_or_profile_urls_exposed",
            True,
            "blocked_source_preview_author_names_or_profile_urls_exposed",
        ),
        ("evidence_layer_write", True, "blocked_source_preview_evidence_layer_write"),
        ("production_evidence_item_created", True, "blocked_source_preview_production_evidence_item_created"),
        ("production_case_created", True, "blocked_source_preview_production_case_created"),
        ("production_analysis_run_created", True, "blocked_source_preview_production_analysis_run_created"),
    ],
)
def test_unsafe_source_preview_blocks_before_evidence_candidate_creation(
    field: str,
    value: object,
    expected_blocker: str,
) -> None:
    preview = _safe_row_preview()
    preview[field] = value

    smoke = _build_8y6_source_path_smoke(
        approval_phrase=EIGHT_Y6_APPROVAL_PHRASE,
        source_preview=preview,
    )

    assert smoke["smoke_status"] == "blocked"
    assert smoke["evidence_candidate_created"] is False
    assert smoke["candidate_count"] == 0
    assert expected_blocker in smoke["blockers"]
    _assert_no_production_side_effects(smoke)
    _assert_no_forbidden_output(smoke)


def test_no_automatic_trust_upgrade_false_does_not_clear_manual_review_warning() -> None:
    preview = _safe_row_preview()
    preview["no_automatic_trust_upgrade"] = False

    smoke = _build_8y6_source_path_smoke(
        approval_phrase=EIGHT_Y6_APPROVAL_PHRASE,
        source_preview=preview,
    )

    assert smoke["smoke_status"] == "ready"
    assert smoke["no_automatic_trust_upgrade"] is True
    assert smoke["candidate_set"]["human_review_required"] is True
    assert smoke["candidate_set"]["warning_count"] == 1
    assert "manual_review_required" in smoke["candidate_set"]["warnings"]
    _assert_no_production_side_effects(smoke)
    _assert_no_forbidden_output(smoke)


@pytest.mark.parametrize(
    ("runtime_flag", "expected_blocker"),
    [
        ("emitted_raw_comments", "blocked_source_preview_runtime_emitted_raw_comments"),
        ("emitted_raw_identities", "blocked_source_preview_runtime_emitted_raw_identities"),
        ("emitted_profile_urls", "blocked_source_preview_runtime_emitted_profile_urls"),
        ("read_original_package_rows", "blocked_source_preview_runtime_read_original_package_rows"),
        ("parsed_evidence_items_csv", "blocked_source_preview_runtime_parsed_evidence_items_csv"),
        ("parsed_source_manifest_jsonl_rows", "blocked_source_preview_runtime_parsed_source_manifest_jsonl_rows"),
        ("parsed_collection_log_jsonl_rows", "blocked_source_preview_runtime_parsed_collection_log_jsonl_rows"),
    ],
)
def test_unsafe_source_preview_runtime_flags_block(runtime_flag: str, expected_blocker: str) -> None:
    preview = _safe_row_preview()
    runtime_side_effects = dict(preview["runtime_side_effects"])
    runtime_side_effects[runtime_flag] = True
    preview["runtime_side_effects"] = runtime_side_effects

    smoke = _build_8y6_source_path_smoke(
        approval_phrase=EIGHT_Y6_APPROVAL_PHRASE,
        source_preview=preview,
    )

    assert smoke["smoke_status"] == "blocked"
    assert expected_blocker in smoke["blockers"]
    assert smoke["evidence_candidate_created"] is False
    _assert_no_production_side_effects(smoke)
    _assert_no_forbidden_output(smoke)
