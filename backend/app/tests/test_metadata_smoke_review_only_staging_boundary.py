from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest

from app.services.real_exported_package_metadata_smoke import (
    APPROVED_CASE_ID_HINT,
    APPROVED_PACKAGE_NAME,
    APPROVED_PACKAGE_ROLE,
)
from app.services.metadata_smoke_review_only_staging_boundary import (
    build_metadata_smoke_review_only_staging_boundary,
)


FORBIDDEN_SENTINELS = (
    "actual-token-should-never-appear",
    "actual-cookie-should-never-appear",
    "actual-api-key-should-never-appear",
    "actual-raw-author-should-never-appear",
    "actual-author-name-should-never-appear",
    "actual-profile-url-should-never-appear",
    "actual-raw-comment-should-never-appear",
    "G:/private-collector/should-never-appear",
    "C:/Users/msjpurf/private-collector/should-never-appear",
    "donglu_sunjihai_youth_football/donglu-sunjihai-youth-football-202606-v2_20260617_121016",
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
            "evidence_count_summary": "unknown",
            "source_count_summary": "unknown",
            "coverage_note_summary": "Selected public sample only; not full-web coverage.",
            "privacy_status": "metadata_only_no_known_privacy_blocker",
            "path_status": "repo_controlled_target_path_ok",
            "warning_summary": ["sample_size_below_target"],
            "blocker_summary": [],
        },
        "boundary_flags": {
            "metadata_only": True,
            "selected_sample_only": True,
            "not_full_web": True,
            "not_full_platform": True,
            "not_full_thread": True,
            "not_official_verification": True,
            "not_causal_proof": True,
            "not_prediction": True,
            "not_production_score": True,
            "provider_output_is_evidence_candidate_not_truth": True,
            "no_row_read": True,
            "no_private_collector_source_inspection": True,
            "no_evidence_layer_write": True,
            "no_production_case": True,
            "no_production_analysis_run": True,
            "no_frontend_route": True,
            "no_real_api_llm_provider_collector": True,
            "human_review_required": True,
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
        "warnings": ["sample_size_below_target"],
        "blockers": [],
    }
    smoke.update(overrides)
    return smoke


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _assert_safe_output(value: object) -> None:
    serialized = _serialized(value)
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel not in serialized
    assert ":/" not in serialized
    assert ":\\" not in serialized


def _assert_all_side_effects_false(boundary: dict[str, object]) -> None:
    runtime_side_effects = boundary["runtime_side_effects"]
    assert isinstance(runtime_side_effects, dict)
    assert runtime_side_effects
    assert all(value is False for value in runtime_side_effects.values())


def _assert_blocked(boundary: dict[str, object], expected_reason: str | None = None) -> None:
    assert str(boundary["boundary_status"]).startswith("blocked_")
    assert boundary["created_local_review_only_staging_boundary"] is False
    assert boundary["review_only_staging_boundary_created"] is False
    assert boundary["review_only_staging_runtime_used"] is False
    assert boundary["review_queue_item_created"] is False
    assert boundary["production_review_queue_item_created"] is False
    assert boundary["evidence_items_created"] is False
    assert boundary["row_preview_approved"] is False
    assert boundary["evidence_layer_write"] is False
    assert boundary["production_case_created"] is False
    assert boundary["production_analysis_run_created"] is False
    _assert_all_side_effects_false(boundary)
    if expected_reason:
        assert expected_reason in boundary["blocker_codes"]
    _assert_safe_output(boundary)


def test_ready_warn_boundary_from_safe_8w2_metadata_smoke() -> None:
    boundary = build_metadata_smoke_review_only_staging_boundary(_safe_8w2_smoke())

    assert boundary["schema"] == "sentigraph_metadata_smoke_review_only_staging_boundary_v0_1"
    assert boundary["phase"] == "8W-4"
    assert boundary["boundary_status"] == "review_only_staging_boundary_ready_for_manual_review"
    assert boundary["created_local_review_only_staging_boundary"] is True
    assert boundary["input_source_kind"] == "real_exported_package_metadata_smoke"
    assert boundary["input_schema"] == "sentigraph_real_exported_package_metadata_smoke_v0_1"
    assert boundary["input_phase"] == "8W-2"
    assert boundary["input_smoke_status"] == "metadata_warn_manual_review_required"
    assert boundary["approved_target_package_name"] == APPROVED_PACKAGE_NAME
    assert boundary["approved_target_package_role"] == APPROVED_PACKAGE_ROLE
    assert boundary["approved_target_case_id_hint"] == APPROVED_CASE_ID_HINT
    assert boundary["metadata_only"] is True
    assert boundary["human_review_required"] is True
    assert boundary["warning_count"] == 1
    assert boundary["warning_manual_review_preserved"] is True
    assert boundary["review_only_staging_boundary_created"] is True
    assert boundary["review_only_staging_runtime_used"] is False
    assert boundary["review_queue_item_created"] is False
    assert boundary["production_review_queue_item_created"] is False
    assert boundary["evidence_items_created"] is False
    assert boundary["row_preview_approved"] is False
    assert boundary["evidence_layer_write"] is False
    assert boundary["production_case_created"] is False
    assert boundary["production_analysis_run_created"] is False
    assert boundary["frontend_ready"] is False
    assert boundary["route_ready"] is False
    assert boundary["production_ready"] is False
    assert boundary["public_ready"] is False
    assert boundary["customer_ready"] is False
    assert boundary["b_end_ready"] is False
    assert boundary["sandbox_ready"] is False
    assert boundary["public_event_ready"] is False

    safe_summary = boundary["safe_source_summary"]
    assert safe_summary["target_package_name"] == APPROVED_PACKAGE_NAME
    assert safe_summary["target_package_role"] == APPROVED_PACKAGE_ROLE
    assert safe_summary["target_case_id_hint"] == APPROVED_CASE_ID_HINT
    assert safe_summary["input_smoke_status"] == "metadata_warn_manual_review_required"
    assert safe_summary["warning_count"] == 1
    assert safe_summary["error_count"] == 0
    assert safe_summary["validation_status"] == "passed"
    assert safe_summary["coverage_note_summary"] == "Selected public sample only; not full-web coverage."
    assert safe_summary["privacy_status"] == "metadata_only_no_known_privacy_blocker"
    assert safe_summary["path_status"] == "repo_controlled_target_path_ok"
    assert safe_summary["warning_summary"] == ["sample_size_below_target"]
    assert safe_summary["blocker_summary"] == []

    for flag in (
        "metadata_only",
        "selected_sample_only",
        "not_full_web",
        "not_full_platform",
        "not_full_thread",
        "not_official_verification",
        "not_causal_proof",
        "not_prediction",
        "not_production_score",
        "provider_output_is_evidence_candidate_not_truth",
        "no_row_read",
        "no_private_collector_source_inspection",
        "no_evidence_layer_write",
        "no_production_case",
        "no_production_analysis_run",
        "no_frontend_route",
        "no_real_api_llm_provider_collector",
        "human_review_required",
        "warning_manual_review_preserved",
    ):
        assert boundary["boundary_flags"][flag] is True

    _assert_all_side_effects_false(boundary)
    _assert_safe_output(boundary)


def test_warning_manual_review_state_must_be_preserved() -> None:
    boundary = build_metadata_smoke_review_only_staging_boundary(_safe_8w2_smoke())
    assert boundary["warning_count"] == 1
    assert boundary["human_review_required"] is True
    assert boundary["warning_manual_review_preserved"] is True

    missing_warning = _safe_8w2_smoke()
    missing_warning.pop("warning_count")
    blocked = build_metadata_smoke_review_only_staging_boundary(missing_warning)

    _assert_blocked(blocked, "warning_count_missing_or_invalid")


@pytest.mark.parametrize(
    ("field", "value", "expected_reason"),
    [
        ("target_package_name", "wrong-package", "package_name_not_approved"),
        ("target_package_role", "wrong-role", "package_role_not_approved"),
        ("target_case_id_hint", "wrong_case", "case_id_hint_not_approved"),
    ],
)
def test_wrong_package_identity_blocks(field: str, value: str, expected_reason: str) -> None:
    smoke = _safe_8w2_smoke(**{field: value})

    boundary = build_metadata_smoke_review_only_staging_boundary(smoke)

    _assert_blocked(boundary, expected_reason)


@pytest.mark.parametrize(
    ("field", "value", "expected_reason"),
    [
        ("metadata_only", False, "metadata_only_not_true"),
        ("row_files_parsed", True, "row_files_parsed_true"),
        ("evidence_items_jsonl_parsed", True, "evidence_items_jsonl_parsed_true"),
        ("evidence_items_csv_parsed", True, "evidence_items_csv_parsed_true"),
        ("original_package_rows_read", True, "original_package_rows_read_true"),
        ("private_collector_source_inspected", True, "private_collector_source_inspected_true"),
        ("real_exchange_dir_read", True, "real_exchange_dir_read_true"),
    ],
)
def test_unsafe_source_flags_block(field: str, value: object, expected_reason: str) -> None:
    boundary = build_metadata_smoke_review_only_staging_boundary(_safe_8w2_smoke(**{field: value}))

    _assert_blocked(boundary, expected_reason)


def test_any_runtime_side_effect_true_blocks() -> None:
    smoke = _safe_8w2_smoke()
    runtime_side_effects = dict(smoke["runtime_side_effects"])
    runtime_side_effects["called_real_api"] = True
    smoke["runtime_side_effects"] = runtime_side_effects

    boundary = build_metadata_smoke_review_only_staging_boundary(smoke)

    _assert_blocked(boundary, "runtime_side_effect_true:called_real_api")


@pytest.mark.parametrize(
    ("field", "value", "expected_reason"),
    [
        ("raw_author_id", "actual-raw-author-should-never-appear", "forbidden_input_field:raw_author_id"),
        ("author_name", "actual-author-name-should-never-appear", "forbidden_input_field:author_name"),
        ("profile_url", "actual-profile-url-should-never-appear", "forbidden_input_field:profile_url"),
        ("raw_comment", "actual-raw-comment-should-never-appear", "forbidden_input_field:raw_comment"),
        ("token", "actual-token-should-never-appear", "forbidden_input_field:token"),
        ("cookie", "actual-cookie-should-never-appear", "forbidden_input_field:cookie"),
        ("api_key", "actual-api-key-should-never-appear", "forbidden_input_field:api_key"),
        ("absolute_path", "G:/private-collector/should-never-appear", "forbidden_input_field:absolute_path"),
    ],
)
def test_forbidden_values_block_and_are_not_echoed(field: str, value: str, expected_reason: str) -> None:
    smoke = _safe_8w2_smoke()
    smoke["safe_summary"] = dict(smoke["safe_summary"])
    smoke["safe_summary"][field] = value

    boundary = build_metadata_smoke_review_only_staging_boundary(smoke)

    _assert_blocked(boundary, expected_reason)


def test_helper_does_not_read_files(monkeypatch: pytest.MonkeyPatch) -> None:
    def blocked_open(*args, **kwargs):
        raise AssertionError("8W-4 helper must not open files")

    def blocked_read_text(*args, **kwargs):
        raise AssertionError("8W-4 helper must not read files")

    monkeypatch.setattr(builtins, "open", blocked_open)
    monkeypatch.setattr(Path, "read_text", blocked_read_text)

    boundary = build_metadata_smoke_review_only_staging_boundary(_safe_8w2_smoke())

    assert boundary["boundary_status"] == "review_only_staging_boundary_ready_for_manual_review"
    assert boundary["created_local_review_only_staging_boundary"] is True


@pytest.mark.parametrize(
    "requested_action",
    [
        "row_preview",
        "evidence_layer_write",
        "production_case",
        "production_analysis_run",
        "frontend_route",
        "b_end_report",
        "sandbox_public_event",
        "public_url",
        "signed_url",
        "download_package",
        "final_delivery",
        "publish",
        "send",
        "post",
        "execute",
    ],
)
def test_side_effect_requests_block_and_keep_flags_false(requested_action: str) -> None:
    smoke = _safe_8w2_smoke(requested_actions=[requested_action])

    boundary = build_metadata_smoke_review_only_staging_boundary(smoke)

    _assert_blocked(boundary, f"requested_action_blocked:{requested_action}")


def test_allowed_and_blocked_actions_are_labels_only() -> None:
    boundary = build_metadata_smoke_review_only_staging_boundary(_safe_8w2_smoke())

    assert boundary["allowed_actions"] == [
        "manual_review_warning_acknowledgement_required",
        "keep_as_metadata_checkpoint",
        "future_review_only_staging_boundary_review",
        "future_row_preview_gate_decision_required",
    ]
    for action in (
        "row_preview",
        "evidence_layer_write",
        "production_case_creation",
        "production_analysis_run_creation",
        "production_review_queue_creation",
        "b_end_report_runtime",
        "sandbox_public_event_runtime",
        "frontend_route",
        "report_export_download_public_final_delivery_runtime",
        "real_api_llm_provider_collector",
        "publish_send_post_execute",
    ):
        assert action in boundary["blocked_actions"]
    _assert_safe_output(boundary)
