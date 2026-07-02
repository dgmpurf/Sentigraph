from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest

from app.services.controlled_evidence_candidate import (
    APPROVAL_PHRASE,
    build_controlled_evidence_candidate_set,
    build_safe_controlled_evidence_candidate_summary,
)


EXPECTED_APPROVAL_PHRASE = "批准 8W-10 Controlled Evidence Candidate Helper Implementation"
MOJIBAKE_APPROVAL_PHRASE = "鎵瑰噯 8W-10 Controlled Evidence Candidate Helper Implementation"

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
    "actual-email-should-never-appear@example.com",
    "555-123-4567",
    "G:/private-collector/should-never-appear",
    "C:/Users/msjpurf/private-collector/should-never-appear",
    "donglu_sunjihai_youth_football/donglu-sunjihai-youth-football-202606-v2_20260617_121016",
)


def _preview_row(index: int, **overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "preview_row_id": f"preview-row-{index:03d}",
        "row_index": index,
        "evidence_id_hash": f"hash-{index:03d}",
        "evidence_type": "comment",
        "platform": "bilibili",
        "created_at_date": "2026-06-17",
        "trust_label": "medium_low",
        "verification_status": "vendor_attested",
        "review_status": "review_needed",
        "language": "zh",
        "content_visibility": "public",
        "access_scope": "selected_public_sample",
        "text_snippet_redacted": f"redacted snippet {index}",
        "redaction_status": "redacted",
        "redaction_warnings": ["selected_sample_only"],
        "row_boundary_flags": {
            "preview_only": True,
            "human_review_required": True,
            "not_official_verification": True,
            "not_full_web": True,
            "not_full_platform": True,
            "not_causal_proof": True,
        },
    }
    row.update(overrides)
    return row


def _valid_preview(**overrides: object) -> dict[str, object]:
    preview_rows = [_preview_row(index) for index in range(1, 6)]
    preview: dict[str, object] = {
        "schema": "sentigraph_controlled_row_preview_v0_1",
        "phase": "8W-7",
        "preview_status": "row_preview_warn_manual_review_required",
        "created_local_row_preview": True,
        "source_boundary_schema": "sentigraph_metadata_smoke_review_only_staging_boundary_v0_1",
        "source_boundary_phase": "8W-4",
        "row_source": "evidence_items.jsonl",
        "row_source_policy": "single_approved_jsonl_source_only",
        "row_source_path_exposed": False,
        "absolute_path_exposed": False,
        "package_path_exposed": False,
        "max_preview_rows_applied": 5,
        "max_preview_rows_hard_bound": 10,
        "rows_inspected_count": 5,
        "preview_rows_count": 5,
        "row_limit_enforced": True,
        "warning_count": 1,
        "human_review_required": True,
        "warning_manual_review_preserved": True,
        "preview_only": True,
        "production_ready": False,
        "public_ready": False,
        "customer_ready": False,
        "route_ready": False,
        "frontend_ready": False,
        "evidence_layer_ready": False,
        "evidence_layer_write": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "evidence_items_created": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_generated": False,
        "generated_response_text": False,
        "public_route_created": False,
        "download_package_runtime_used": False,
        "public_access_runtime_used": False,
        "external_delivery_runtime_used": False,
        "final_delivery_runtime_used": False,
        "preview_rows": preview_rows,
        "blockers": [],
        "warnings": ["manual_review_required", "selected_sample_only"],
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
            "opened_approved_evidence_items_jsonl": True,
            "parsed_evidence_items_jsonl": True,
            "parsed_evidence_items_csv": False,
            "parsed_source_manifest_jsonl_rows": False,
            "parsed_collection_log_jsonl_rows": False,
            "read_original_package_rows": False,
            "read_private_collector_raw_output": False,
            "emitted_raw_comments": False,
            "emitted_raw_identities": False,
            "emitted_profile_urls": False,
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
    preview.update(overrides)
    return preview


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _assert_safe_output(value: object) -> None:
    serialized = _serialized(value)
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel not in serialized
    assert ":/" not in serialized
    assert ":\\" not in serialized


def _assert_all_disallowed_side_effects_false(candidate_set: dict[str, object]) -> None:
    runtime_side_effects = candidate_set["runtime_side_effects"]
    assert isinstance(runtime_side_effects, dict)
    for flag, value in runtime_side_effects.items():
        assert value is False, flag


def _assert_blocked(candidate_set: dict[str, object], expected_reason: str) -> None:
    assert str(candidate_set["candidate_set_status"]).startswith("blocked_")
    assert candidate_set["evidence_candidate_created"] is False
    assert candidate_set["candidate_count"] == 0
    assert candidate_set["candidates"] == []
    assert expected_reason in candidate_set["blockers"]
    _assert_all_disallowed_side_effects_false(candidate_set)
    _assert_safe_output(candidate_set)


def test_ready_path_builds_local_candidates_without_production_side_effects() -> None:
    assert APPROVAL_PHRASE == EXPECTED_APPROVAL_PHRASE

    candidate_set = build_controlled_evidence_candidate_set(
        _valid_preview(),
        exact_approval_phrase=EXPECTED_APPROVAL_PHRASE,
    )

    assert candidate_set["candidate_set_schema"] == "sentigraph_controlled_evidence_candidate_set_v0_1"
    assert candidate_set["phase"] == "8W-10"
    assert candidate_set["candidate_set_status"] == "evidence_candidate_set_warn_manual_review_required"
    assert candidate_set["input_source_kind"] == "controlled_row_preview"
    assert candidate_set["source_preview_schema"] == "sentigraph_controlled_row_preview_v0_1"
    assert candidate_set["source_preview_phase"] == "8W-7"
    assert candidate_set["candidate_mode"] == "backend_only_local_preview_derived_evidence_candidate"
    assert candidate_set["candidate_count"] == 5
    assert candidate_set["source_preview_rows_count"] == 5
    assert candidate_set["warning_count"] == 1
    assert candidate_set["human_review_required"] is True
    assert candidate_set["preview_only"] is True
    assert candidate_set["evidence_candidate_implementation_approved"] is True
    assert candidate_set["evidence_candidate_created"] is True
    assert candidate_set["evidence_items_created"] is False
    assert candidate_set["evidence_layer_write"] is False
    assert candidate_set["review_queue_item_created"] is False
    assert candidate_set["production_case_created"] is False
    assert candidate_set["production_analysis_run_created"] is False
    assert candidate_set["route_ready"] is False
    assert candidate_set["frontend_ready"] is False

    for candidate in candidate_set["candidates"]:
        assert set(candidate) <= {
            "candidate_schema",
            "candidate_id",
            "source_preview_row_id",
            "source_row_index",
            "source_preview_schema",
            "evidence_id_hash",
            "evidence_type",
            "platform",
            "coarse_created_at",
            "trust_label",
            "verification_status",
            "review_status",
            "language",
            "content_visibility",
            "access_scope",
            "text_snippet_redacted",
            "redaction_status",
            "redaction_warnings",
            "warning_labels",
            "human_review_required",
            "boundary_flags",
        }
        assert candidate["candidate_schema"] == "sentigraph_controlled_evidence_candidate_v0_1"
        assert candidate["human_review_required"] is True
        assert candidate["boundary_flags"]["preview_only"] is True
        assert candidate["boundary_flags"]["not_evidence_item"] is True
        assert candidate["boundary_flags"]["no_evidence_layer_write"] is True
    _assert_all_disallowed_side_effects_false(candidate_set)
    _assert_safe_output(candidate_set)


@pytest.mark.parametrize(
    "phrase",
    [None, "", "wrong approval", MOJIBAKE_APPROVAL_PHRASE],
)
def test_exact_approval_required_before_candidate_creation_and_file_access(
    phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def blocked_open(*args, **kwargs):
        raise AssertionError("8W-10 must not open files")

    monkeypatch.setattr(builtins, "open", blocked_open)
    monkeypatch.setattr(Path, "open", blocked_open)

    candidate_set = build_controlled_evidence_candidate_set(
        _valid_preview(),
        exact_approval_phrase=phrase,
    )

    _assert_blocked(candidate_set, "blocked_missing_exact_approval")


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("schema", "wrong", "source_preview_schema_wrong"),
        ("phase", "wrong", "source_preview_phase_wrong"),
        ("preview_status", "row_preview_ready_for_manual_review", "source_preview_status_not_warn_manual_review"),
        ("created_local_row_preview", False, "source_preview_not_created"),
        ("row_source", "evidence_items.csv", "source_row_source_not_approved_jsonl"),
        ("row_source_policy", "dual_source", "source_row_policy_wrong"),
        ("preview_only", False, "source_preview_only_not_true"),
        ("human_review_required", False, "source_human_review_required_not_true"),
        ("warning_count", 0, "source_warning_count_not_one"),
        ("row_limit_enforced", False, "source_row_limit_not_enforced"),
        ("preview_rows_count", 6, "source_preview_rows_count_inconsistent"),
        ("rows_inspected_count", 4, "source_rows_inspected_less_than_preview_rows"),
        ("absolute_path_exposed", True, "source_absolute_path_exposed"),
        ("package_path_exposed", True, "source_package_path_exposed"),
        ("evidence_layer_write", True, "source_evidence_layer_write_true"),
        ("evidence_items_created", True, "source_evidence_items_created_true"),
        ("review_queue_item_created", True, "source_review_queue_item_created_true"),
        ("production_case_created", True, "source_production_case_created_true"),
        ("production_analysis_run_created", True, "source_production_analysis_run_created_true"),
        ("frontend_ready", True, "source_frontend_ready_true"),
        ("route_ready", True, "source_route_ready_true"),
        ("production_ready", True, "source_production_ready_true"),
    ],
)
def test_source_validation_blocks_unsafe_preview_fields(field: str, value: object, reason: str) -> None:
    candidate_set = build_controlled_evidence_candidate_set(
        _valid_preview(**{field: value}),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(candidate_set, reason)


@pytest.mark.parametrize(
    ("runtime_flag", "reason"),
    [
        ("parsed_evidence_items_csv", "source_runtime_side_effect_true:parsed_evidence_items_csv"),
        ("parsed_source_manifest_jsonl_rows", "source_runtime_side_effect_true:parsed_source_manifest_jsonl_rows"),
        ("parsed_collection_log_jsonl_rows", "source_runtime_side_effect_true:parsed_collection_log_jsonl_rows"),
        ("read_original_package_rows", "source_runtime_side_effect_true:read_original_package_rows"),
        ("accessed_private_collector", "source_runtime_side_effect_true:accessed_private_collector"),
        ("inspected_private_collector_source", "source_runtime_side_effect_true:inspected_private_collector_source"),
        ("read_real_exchange_dir", "source_runtime_side_effect_true:read_real_exchange_dir"),
        ("emitted_raw_comments", "source_runtime_side_effect_true:emitted_raw_comments"),
        ("emitted_raw_identities", "source_runtime_side_effect_true:emitted_raw_identities"),
        ("emitted_profile_urls", "source_runtime_side_effect_true:emitted_profile_urls"),
    ],
)
def test_source_runtime_side_effects_block(runtime_flag: str, reason: str) -> None:
    preview = _valid_preview()
    runtime_side_effects = dict(preview["runtime_side_effects"])
    runtime_side_effects[runtime_flag] = True
    preview["runtime_side_effects"] = runtime_side_effects

    candidate_set = build_controlled_evidence_candidate_set(
        preview,
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(candidate_set, reason)


def test_candidate_limit_cannot_exceed_source_preview_rows_or_hard_bound() -> None:
    exceeds_source = build_controlled_evidence_candidate_set(
        _valid_preview(),
        exact_approval_phrase=APPROVAL_PHRASE,
        candidate_limit=6,
    )
    _assert_blocked(exceeds_source, "blocked_candidate_limit_exceeds_source_preview_rows")

    exceeds_bound = build_controlled_evidence_candidate_set(
        _valid_preview(preview_rows=[_preview_row(index) for index in range(1, 12)], preview_rows_count=11, rows_inspected_count=11),
        exact_approval_phrase=APPROVAL_PHRASE,
        candidate_limit=11,
    )
    _assert_blocked(exceeds_bound, "blocked_candidate_limit_too_high")


def test_preview_rows_absent_or_malformed_block() -> None:
    missing = build_controlled_evidence_candidate_set(
        _valid_preview(preview_rows=[], preview_rows_count=0, rows_inspected_count=0),
        exact_approval_phrase=APPROVAL_PHRASE,
    )
    _assert_blocked(missing, "source_preview_rows_missing")

    malformed = build_controlled_evidence_candidate_set(
        _valid_preview(preview_rows=[{"preview_row_id": "preview-row-001"}], preview_rows_count=1, rows_inspected_count=1),
        exact_approval_phrase=APPROVAL_PHRASE,
    )
    _assert_blocked(malformed, "candidate_row_missing_required_field:evidence_id_hash")


def test_forbidden_fields_in_preview_rows_block_or_never_emit() -> None:
    unsafe_row = _preview_row(
        1,
        raw_author_id="actual-raw-author-should-never-appear",
        author_name="actual-author-name-should-never-appear",
        username="actual-username-should-never-appear",
        display_name="actual-display-name-should-never-appear",
        profile_url="actual-profile-url-should-never-appear",
        raw_comment="actual-raw-comment-should-never-appear",
        token="actual-token-should-never-appear",
        cookie="actual-cookie-should-never-appear",
        api_key="actual-api-key-should-never-appear",
        package_path="G:/private-collector/should-never-appear",
    )
    candidate_set = build_controlled_evidence_candidate_set(
        _valid_preview(preview_rows=[unsafe_row], preview_rows_count=1, rows_inspected_count=1),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(candidate_set, "forbidden_preview_row_field:raw_author_id")


def test_ready_path_never_opens_files(monkeypatch: pytest.MonkeyPatch) -> None:
    def blocked_open(*args, **kwargs):
        raise AssertionError("8W-10 must not open files")

    monkeypatch.setattr(builtins, "open", blocked_open)
    monkeypatch.setattr(Path, "open", blocked_open)

    candidate_set = build_controlled_evidence_candidate_set(
        _valid_preview(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    assert candidate_set["candidate_set_status"] == "evidence_candidate_set_warn_manual_review_required"
    assert candidate_set["candidate_count"] == 5


@pytest.mark.parametrize(
    "requested_action",
    [
        "evidence_layer_write",
        "review_queue_runtime",
        "production_case",
        "production_analysis_run",
        "frontend_route",
        "route_api",
        "b_end_report",
        "sandbox_public_event",
        "real_api",
        "real_llm",
        "provider_job",
        "collector_job",
        "publish",
        "send",
        "post",
        "execute",
        "auto_execute",
    ],
)
def test_requested_side_effects_block_and_keep_flags_false(requested_action: str) -> None:
    candidate_set = build_controlled_evidence_candidate_set(
        _valid_preview(),
        exact_approval_phrase=APPROVAL_PHRASE,
        requested_actions=[requested_action],
    )

    _assert_blocked(candidate_set, f"requested_action_blocked:{requested_action}")


def test_safe_summary_is_counts_and_boundaries_only() -> None:
    summary = build_safe_controlled_evidence_candidate_summary(
        _valid_preview(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    assert summary["summary_schema"] == "sentigraph_controlled_evidence_candidate_summary_v0_1"
    assert summary["phase"] == "8W-10"
    assert summary["candidate_set_schema"] == "sentigraph_controlled_evidence_candidate_set_v0_1"
    assert summary["candidate_set_status"] == "evidence_candidate_set_warn_manual_review_required"
    assert summary["candidate_count"] == 5
    assert summary["source_preview_rows_count"] == 5
    assert summary["warning_count"] == 1
    assert summary["human_review_required"] is True
    assert "candidates" not in summary
    assert "text_snippet_redacted" not in _serialized(summary)
    _assert_safe_output(summary)
