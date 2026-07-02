from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest

from app.services.controlled_review_queue_candidate import (
    APPROVAL_PHRASE,
    build_controlled_review_queue_candidate_set,
    build_safe_controlled_review_queue_candidate_summary,
)


EXPECTED_APPROVAL_PHRASE = "批准 8W-13 Controlled Review Queue Candidate Helper Implementation"
MOJIBAKE_APPROVAL_PHRASE = "鎵瑰噯 8W-13 Controlled Review Queue Candidate Helper Implementation"
ALT_MOJIBAKE_APPROVAL_PHRASE = "閹电懓鍣?8W-13 Controlled Review Queue Candidate Helper Implementation"

FORBIDDEN_SENTINELS = (
    "actual-token-should-never-appear",
    "actual-cookie-should-never-appear",
    "actual-api-key-should-never-appear",
    "actual-secret-should-never-appear",
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


def _evidence_candidate(index: int, **overrides: object) -> dict[str, object]:
    candidate: dict[str, object] = {
        "candidate_schema": "sentigraph_controlled_evidence_candidate_v0_1",
        "candidate_id": f"candidate-{index:03d}-hash-{index:03d}",
        "source_preview_row_id": f"preview-row-{index:03d}",
        "source_row_index": index,
        "source_preview_schema": "sentigraph_controlled_row_preview_v0_1",
        "evidence_id_hash": f"hash-{index:03d}",
        "evidence_type": "comment",
        "platform": "bilibili",
        "coarse_created_at": "2026-06-17",
        "trust_label": "medium_low",
        "verification_status": "vendor_attested",
        "review_status": "review_needed",
        "language": "zh",
        "content_visibility": "public",
        "access_scope": "selected_public_sample",
        "text_snippet_redacted": f"redacted snippet {index}",
        "redaction_status": "redacted",
        "redaction_warnings": ["selected_sample_only"],
        "warning_labels": ["manual_review_required", "selected_sample_only"],
        "human_review_required": True,
        "boundary_flags": {
            "preview_only": True,
            "human_review_required": True,
            "not_evidence_item": True,
            "no_evidence_layer_write": True,
            "no_review_queue_runtime": True,
            "not_production_case": True,
            "not_production_analysis_run": True,
            "not_official_verification": True,
            "not_full_web": True,
            "not_full_platform": True,
            "not_causal_proof": True,
        },
    }
    candidate.update(overrides)
    return candidate


def _valid_candidate_set(**overrides: object) -> dict[str, object]:
    candidates = [_evidence_candidate(index) for index in range(1, 6)]
    candidate_set: dict[str, object] = {
        "candidate_set_schema": "sentigraph_controlled_evidence_candidate_set_v0_1",
        "phase": "8W-10",
        "candidate_set_status": "evidence_candidate_set_warn_manual_review_required",
        "input_source_kind": "controlled_row_preview",
        "source_preview_schema": "sentigraph_controlled_row_preview_v0_1",
        "source_preview_phase": "8W-7",
        "candidate_mode": "backend_only_local_preview_derived_evidence_candidate",
        "candidate_count": 5,
        "source_preview_rows_count": 5,
        "warning_count": 1,
        "human_review_required": True,
        "preview_only": True,
        "evidence_candidate_implementation_approved": True,
        "evidence_candidate_created": True,
        "evidence_items_created": False,
        "evidence_layer_write": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "public_ready": False,
        "customer_ready": False,
        "b_end_ready": False,
        "sandbox_ready": False,
        "public_event_ready": False,
        "candidates": candidates,
        "blockers": [],
        "warnings": ["manual_review_required", "selected_sample_only"],
        "runtime_side_effects": {
            "called_real_api": False,
            "called_real_llm": False,
            "ran_provider_job": False,
            "ran_collector": False,
            "fetched_url": False,
            "scraped_page": False,
            "accessed_private_collector": False,
            "inspected_private_collector_source": False,
            "read_real_exchange_dir": False,
            "parsed_evidence_items_jsonl_again": False,
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
    candidate_set.update(overrides)
    return candidate_set


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
    assert str(candidate_set["review_queue_candidate_set_status"]).startswith("blocked_")
    assert candidate_set["review_queue_candidate_helper_implementation_approved"] is False
    assert candidate_set["review_queue_candidate_created"] is False
    assert candidate_set["review_queue_candidate_count"] == 0
    assert candidate_set["review_queue_candidates"] == []
    assert expected_reason in candidate_set["blockers"]
    _assert_all_disallowed_side_effects_false(candidate_set)
    _assert_safe_output(candidate_set)


def test_ready_path_builds_local_review_queue_candidates_without_production_side_effects() -> None:
    assert APPROVAL_PHRASE == EXPECTED_APPROVAL_PHRASE

    candidate_set = build_controlled_review_queue_candidate_set(
        _valid_candidate_set(),
        exact_approval_phrase=EXPECTED_APPROVAL_PHRASE,
    )

    assert candidate_set["review_queue_candidate_set_schema"] == "sentigraph_controlled_review_queue_candidate_set_v0_1"
    assert candidate_set["phase"] == "8W-13"
    assert candidate_set["review_queue_candidate_set_status"] == "review_queue_candidate_set_warn_manual_review_required"
    assert candidate_set["input_source_kind"] == "controlled_evidence_candidate_set"
    assert candidate_set["source_candidate_set_schema"] == "sentigraph_controlled_evidence_candidate_set_v0_1"
    assert candidate_set["source_candidate_set_status"] == "evidence_candidate_set_warn_manual_review_required"
    assert candidate_set["source_candidate_count"] == 5
    assert candidate_set["review_queue_candidate_mode"] == "backend_only_local_review_queue_candidate_boundary"
    assert candidate_set["review_queue_candidate_count"] == 5
    assert candidate_set["warning_count"] == 1
    assert candidate_set["human_review_required"] is True
    assert candidate_set["preview_only"] is True
    assert candidate_set["queue_candidate_only"] is True
    assert candidate_set["review_queue_candidate_helper_implementation_approved"] is True
    assert candidate_set["review_queue_candidate_created"] is True
    assert candidate_set["review_queue_item_created"] is False
    assert candidate_set["production_review_queue_item_created"] is False
    assert candidate_set["evidence_items_created"] is False
    assert candidate_set["evidence_layer_write"] is False
    assert candidate_set["production_case_created"] is False
    assert candidate_set["production_analysis_run_created"] is False
    assert candidate_set["route_ready"] is False
    assert candidate_set["frontend_ready"] is False

    for candidate in candidate_set["review_queue_candidates"]:
        assert set(candidate) <= {
            "review_queue_candidate_schema",
            "review_queue_candidate_id",
            "source_evidence_candidate_id",
            "source_candidate_set_schema",
            "source_candidate_schema",
            "evidence_id_hash",
            "platform",
            "evidence_type",
            "coarse_created_at",
            "trust_label",
            "verification_status",
            "review_status",
            "text_snippet_redacted",
            "redaction_status",
            "redaction_warnings",
            "warning_labels",
            "blocker_codes",
            "human_review_required",
            "preview_only",
            "queue_candidate_only",
            "boundary_flags",
        }
        assert candidate["review_queue_candidate_schema"] == "sentigraph_controlled_review_queue_candidate_v0_1"
        assert candidate["source_candidate_set_schema"] == "sentigraph_controlled_evidence_candidate_set_v0_1"
        assert candidate["source_candidate_schema"] == "sentigraph_controlled_evidence_candidate_v0_1"
        assert candidate["human_review_required"] is True
        assert candidate["preview_only"] is True
        assert candidate["queue_candidate_only"] is True
        assert candidate["boundary_flags"]["not_review_queue_item"] is True
        assert candidate["boundary_flags"]["not_evidence_item"] is True
        assert candidate["boundary_flags"]["no_evidence_layer_write"] is True
    _assert_all_disallowed_side_effects_false(candidate_set)
    _assert_safe_output(candidate_set)


@pytest.mark.parametrize(
    ("phrase", "expected_reason"),
    [
        (None, "blocked_missing_exact_approval"),
        ("", "blocked_missing_exact_approval"),
        ("wrong approval", "blocked_wrong_exact_approval"),
        (MOJIBAKE_APPROVAL_PHRASE, "blocked_wrong_exact_approval"),
        (ALT_MOJIBAKE_APPROVAL_PHRASE, "blocked_wrong_exact_approval"),
    ],
)
def test_exact_approval_required_before_candidate_creation_and_file_access(
    phrase: str | None,
    expected_reason: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def blocked_open(*args, **kwargs):
        raise AssertionError("8W-13 must not open files")

    monkeypatch.setattr(builtins, "open", blocked_open)
    monkeypatch.setattr(Path, "open", blocked_open)

    candidate_set = build_controlled_review_queue_candidate_set(
        _valid_candidate_set(),
        exact_approval_phrase=phrase,
    )

    _assert_blocked(candidate_set, expected_reason)


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("candidate_set_schema", "wrong", "source_candidate_set_schema_wrong"),
        ("phase", "wrong", "source_candidate_set_phase_wrong"),
        ("candidate_set_status", "evidence_candidate_set_ready_for_manual_review", "source_candidate_set_status_not_warn_manual_review"),
        ("candidate_count", 4, "source_candidate_count_inconsistent"),
        ("source_preview_rows_count", 4, "source_preview_rows_count_less_than_candidate_count"),
        ("warning_count", 0, "source_warning_count_not_one"),
        ("human_review_required", False, "source_human_review_required_not_true"),
        ("preview_only", False, "source_preview_only_not_true"),
        ("evidence_candidate_implementation_approved", False, "source_evidence_candidate_implementation_not_approved"),
        ("evidence_candidate_created", False, "source_evidence_candidate_created_not_true"),
        ("evidence_items_created", True, "source_evidence_items_created_true"),
        ("evidence_layer_write", True, "source_evidence_layer_write_true"),
        ("review_queue_item_created", True, "source_review_queue_item_created_true"),
        ("production_review_queue_item_created", True, "source_production_review_queue_item_created_true"),
        ("production_case_created", True, "source_production_case_created_true"),
        ("production_analysis_run_created", True, "source_production_analysis_run_created_true"),
        ("route_ready", True, "source_route_ready_true"),
        ("frontend_ready", True, "source_frontend_ready_true"),
        ("production_ready", True, "source_production_ready_true"),
        ("public_ready", True, "source_public_ready_true"),
        ("customer_ready", True, "source_customer_ready_true"),
    ],
)
def test_source_validation_blocks_unsafe_candidate_set_fields(field: str, value: object, reason: str) -> None:
    candidate_set = build_controlled_review_queue_candidate_set(
        _valid_candidate_set(**{field: value}),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(candidate_set, reason)


@pytest.mark.parametrize(
    ("runtime_flag", "reason"),
    [
        ("called_real_api", "source_runtime_side_effect_true:called_real_api"),
        ("called_real_llm", "source_runtime_side_effect_true:called_real_llm"),
        ("ran_provider_job", "source_runtime_side_effect_true:ran_provider_job"),
        ("ran_collector", "source_runtime_side_effect_true:ran_collector"),
        ("fetched_url", "source_runtime_side_effect_true:fetched_url"),
        ("scraped_page", "source_runtime_side_effect_true:scraped_page"),
        ("accessed_private_collector", "source_runtime_side_effect_true:accessed_private_collector"),
        ("inspected_private_collector_source", "source_runtime_side_effect_true:inspected_private_collector_source"),
        ("read_real_exchange_dir", "source_runtime_side_effect_true:read_real_exchange_dir"),
        ("parsed_evidence_items_jsonl_again", "source_runtime_side_effect_true:parsed_evidence_items_jsonl_again"),
        ("parsed_evidence_items_csv", "source_runtime_side_effect_true:parsed_evidence_items_csv"),
        ("parsed_source_manifest_jsonl_rows", "source_runtime_side_effect_true:parsed_source_manifest_jsonl_rows"),
        ("parsed_collection_log_jsonl_rows", "source_runtime_side_effect_true:parsed_collection_log_jsonl_rows"),
        ("read_original_package_rows", "source_runtime_side_effect_true:read_original_package_rows"),
        ("read_private_collector_raw_output", "source_runtime_side_effect_true:read_private_collector_raw_output"),
        ("emitted_raw_comments", "source_runtime_side_effect_true:emitted_raw_comments"),
        ("emitted_raw_identities", "source_runtime_side_effect_true:emitted_raw_identities"),
        ("emitted_profile_urls", "source_runtime_side_effect_true:emitted_profile_urls"),
        ("created_review_queue_items", "source_runtime_side_effect_true:created_review_queue_items"),
    ],
)
def test_source_runtime_side_effects_block(runtime_flag: str, reason: str) -> None:
    source = _valid_candidate_set()
    runtime_side_effects = dict(source["runtime_side_effects"])
    runtime_side_effects[runtime_flag] = True
    source["runtime_side_effects"] = runtime_side_effects

    candidate_set = build_controlled_review_queue_candidate_set(
        source,
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(candidate_set, reason)


def test_candidate_limit_cannot_exceed_source_candidate_count_or_hard_bound() -> None:
    exceeds_source = build_controlled_review_queue_candidate_set(
        _valid_candidate_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
        candidate_limit=6,
    )
    _assert_blocked(exceeds_source, "blocked_candidate_limit_exceeds_source_candidate_count")

    many_candidates = [_evidence_candidate(index) for index in range(1, 12)]
    exceeds_bound = build_controlled_review_queue_candidate_set(
        _valid_candidate_set(candidates=many_candidates, candidate_count=11, source_preview_rows_count=11),
        exact_approval_phrase=APPROVAL_PHRASE,
        candidate_limit=11,
    )
    _assert_blocked(exceeds_bound, "blocked_candidate_limit_too_high")


def test_candidates_absent_or_malformed_block() -> None:
    missing = build_controlled_review_queue_candidate_set(
        _valid_candidate_set(candidates=[], candidate_count=0, source_preview_rows_count=0),
        exact_approval_phrase=APPROVAL_PHRASE,
    )
    _assert_blocked(missing, "source_candidates_missing")

    malformed = build_controlled_review_queue_candidate_set(
        _valid_candidate_set(candidates=[{"candidate_id": "candidate-001"}], candidate_count=1, source_preview_rows_count=1),
        exact_approval_phrase=APPROVAL_PHRASE,
    )
    _assert_blocked(malformed, "source_candidate_missing_required_field:evidence_id_hash")


def test_forbidden_fields_in_source_candidates_block_or_never_emit() -> None:
    unsafe_candidate = _evidence_candidate(
        1,
        raw_author_id="actual-raw-author-should-never-appear",
        author_id="actual-raw-author-should-never-appear",
        author_name="actual-author-name-should-never-appear",
        username="actual-username-should-never-appear",
        display_name="actual-display-name-should-never-appear",
        profile_url="actual-profile-url-should-never-appear",
        raw_comment="actual-raw-comment-should-never-appear",
        token="actual-token-should-never-appear",
        cookie="actual-cookie-should-never-appear",
        api_key="actual-api-key-should-never-appear",
        secret="actual-secret-should-never-appear",
        package_path="G:/private-collector/should-never-appear",
        target_user_list=["actual-raw-author-should-never-appear"],
        persuasion_score=0.9,
        truth_score=0.9,
        official_verified=True,
        prediction_probability=0.9,
        psychological_profile="actual-profile-should-never-appear",
        personality_diagnosis="actual-diagnosis-should-never-appear",
        review_action="approve",
        reviewer_assignment="reviewer-1",
        review_decision="approved",
        audit_timeline=["should-never-appear"],
        production_review_queue_item_id="prod-review-001",
        evidence_item_id="evidence-item-001",
    )
    candidate_set = build_controlled_review_queue_candidate_set(
        _valid_candidate_set(candidates=[unsafe_candidate], candidate_count=1, source_preview_rows_count=1),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(candidate_set, "forbidden_source_candidate_field:raw_author_id")


def test_ready_path_never_opens_files(monkeypatch: pytest.MonkeyPatch) -> None:
    def blocked_open(*args, **kwargs):
        raise AssertionError("8W-13 must not open files")

    monkeypatch.setattr(builtins, "open", blocked_open)
    monkeypatch.setattr(Path, "open", blocked_open)

    candidate_set = build_controlled_review_queue_candidate_set(
        _valid_candidate_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    assert candidate_set["review_queue_candidate_set_status"] == "review_queue_candidate_set_warn_manual_review_required"
    assert candidate_set["review_queue_candidate_count"] == 5


@pytest.mark.parametrize(
    "requested_action",
    [
        "review_queue_item_creation",
        "production_review_queue_item_creation",
        "evidence_item_creation",
        "evidence_layer_write",
        "production_case",
        "production_analysis_run",
        "frontend_route",
        "route_api",
        "b_end_report",
        "sandbox_public_event",
        "download_package",
        "public_access",
        "external_delivery",
        "final_delivery",
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
    candidate_set = build_controlled_review_queue_candidate_set(
        _valid_candidate_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
        requested_actions=[requested_action],
    )

    _assert_blocked(candidate_set, f"requested_action_blocked:{requested_action}")


def test_safe_summary_is_counts_and_boundaries_only() -> None:
    summary = build_safe_controlled_review_queue_candidate_summary(
        _valid_candidate_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    assert summary["summary_schema"] == "sentigraph_controlled_review_queue_candidate_summary_v0_1"
    assert summary["phase"] == "8W-13"
    assert summary["review_queue_candidate_set_schema"] == "sentigraph_controlled_review_queue_candidate_set_v0_1"
    assert summary["review_queue_candidate_set_status"] == "review_queue_candidate_set_warn_manual_review_required"
    assert summary["review_queue_candidate_count"] == 5
    assert summary["source_candidate_count"] == 5
    assert summary["warning_count"] == 1
    assert summary["human_review_required"] is True
    assert "review_queue_candidates" not in summary
    assert "text_snippet_redacted" not in _serialized(summary)
    _assert_safe_output(summary)
