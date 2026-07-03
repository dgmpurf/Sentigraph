from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest

from app.services.controlled_production_case_candidate import (
    APPROVAL_PHRASE,
    build_controlled_production_case_candidate_set,
    build_safe_controlled_production_case_candidate_summary,
)


EXPECTED_APPROVAL_PHRASE = "APPROVE_8W_31_CONTROLLED_PRODUCTION_CASE_CANDIDATE_HELPER_IMPLEMENTATION"
NON_ASCII_APPROVAL_PHRASE = "\u6279\u51c6 8W-31 Controlled Production Case Candidate Helper Implementation"
MOJIBAKE_APPROVAL_PHRASE = "\u9395\u7470\u567f 8W-31 Controlled Production Case Candidate Helper Implementation"

FORBIDDEN_SENTINELS = (
    "actual-token-should-never-appear",
    "actual-cookie-should-never-appear",
    "actual-api-key-should-never-appear",
    "actual-secret-should-never-appear",
    "actual-salt-should-never-appear",
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


def _controlled_evidence_item(index: int, **overrides: object) -> dict[str, object]:
    item: dict[str, object] = {
        "controlled_evidence_item_schema": "sentigraph_controlled_evidence_item_v0_1",
        "controlled_evidence_item_id": f"controlled-evidence-item-{index:03d}-hash-{index:03d}",
        "source_evidence_layer_write_candidate_id": (
            f"evidence-layer-write-candidate-from-production-import-{index:03d}-hash-{index:03d}"
        ),
        "source_production_evidence_import_candidate_id": (
            f"production-evidence-import-candidate-{index:03d}-hash-{index:03d}"
        ),
        "source_evidence_layer_import_candidate_id": (
            f"evidence-layer-import-candidate-{index:03d}-hash-{index:03d}"
        ),
        "source_review_queue_candidate_id": f"review-queue-candidate-{index:03d}-hash-{index:03d}",
        "source_evidence_candidate_id": f"candidate-{index:03d}-hash-{index:03d}",
        "evidence_id_hash": f"hash-{index:03d}",
        "controlled_content_hash": f"hash-{index:03d}",
        "preview_hash": f"preview-hash-{index:03d}",
        "case_id_hint": "case-donglu-sunjihai-youth-football",
        "platform": "bilibili",
        "evidence_type": "comment",
        "coarse_created_at": "2026-06-17",
        "source_url_present": False,
        "acquisition_mode": "controlled_local_import",
        "provenance_type": "evidence_layer_write_candidate",
        "verification_status": "vendor_attested",
        "trust_label": "medium_low",
        "review_status": "review_needed",
        "title_or_label_redacted": f"redacted label {index}",
        "text_snippet_redacted": f"redacted snippet {index}",
        "redaction_status": "redacted",
        "redaction_warnings": ["selected_sample_only"],
        "warning_labels": ["manual_review_required", "selected_sample_only"],
        "blocker_codes": [],
        "human_review_required": True,
        "preview_only": True,
        "import_candidate_only": True,
        "evidence_layer_write_runtime_controlled_only": True,
        "analysis_ready": False,
        "report_ready": False,
        "production_case_ready": False,
        "production_analysis_run_ready": False,
        "boundary_flags": {
            "controlled_local_evidence_item_only": True,
            "controlled_local_evidence_layer_write_only": True,
            "human_review_required": True,
            "preview_only": True,
            "import_candidate_only": True,
            "no_automatic_trust_upgrade": True,
            "not_production_evidence_item": True,
            "not_review_queue_item": True,
            "not_production_review_queue_item": True,
            "not_production_case": True,
            "not_production_analysis_run": True,
            "not_analysis_ready": True,
            "not_report_ready": True,
            "not_frontend_ready": True,
            "not_route_ready": True,
            "not_public_ready": True,
            "not_customer_ready": True,
            "not_official_verification": True,
            "not_full_web": True,
            "not_full_platform": True,
            "not_causal_proof": True,
            "no_generated_response_text": True,
        },
    }
    item.update(overrides)
    return item


def _runtime_side_effects(**overrides: bool) -> dict[str, bool]:
    flags = {
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
        "created_evidence_item": False,
        "created_production_evidence_items": False,
        "created_review_queue_items": False,
        "created_production_review_queue_items": False,
        "created_production_case": False,
        "created_production_analysis_run": False,
        "created_review_action_records": False,
        "created_review_audit_timeline_records": False,
        "created_reviewer_assignment_records": False,
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
    }
    flags.update(overrides)
    return flags


def _valid_evidenceitem_runtime(**overrides: object) -> dict[str, object]:
    items = [_controlled_evidence_item(index) for index in range(1, 6)]
    runtime: dict[str, object] = {
        "runtime_schema": "sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1",
        "phase": "8W-28",
        "write_runtime_status": "evidence_layer_write_runtime_warn_manual_review_required",
        "input_source_kind": "controlled_evidence_layer_write_candidate_set",
        "source_candidate_count": 5,
        "source_evidence_layer_write_candidate_count": 5,
        "source_candidate_set_schema": (
            "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1"
        ),
        "controlled_evidence_item_schema": "sentigraph_controlled_evidence_item_v0_1",
        "controlled_evidence_item_count": 5,
        "write_result_schema": "sentigraph_controlled_evidence_layer_write_result_v0_1",
        "controlled_evidence_layer_write_result_created": True,
        "controlled_evidenceitem_created": True,
        "evidence_item_created": True,
        "evidence_items_created": True,
        "evidence_layer_write": True,
        "evidence_layer_write_scope": "controlled_local_helper_test_path_only",
        "production_evidence_item_created": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "review_queue_runtime_used": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "analysis_ready": False,
        "report_ready": False,
        "b_end_ready": False,
        "sandbox_ready": False,
        "public_event_ready": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "public_ready": False,
        "customer_ready": False,
        "additional_row_parsing_performed": False,
        "evidence_items_jsonl_parsed_again": False,
        "evidence_items_csv_parsed": False,
        "source_manifest_rows_parsed": False,
        "collection_log_rows_parsed": False,
        "original_package_rows_read": False,
        "raw_comments_read": False,
        "raw_identities_read": False,
        "private_collector_inspected": False,
        "private_collector_source_inspected": False,
        "real_exchange_dir_read": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_generated": False,
        "generated_response_text": False,
        "public_route_created": False,
        "frontend_integration_approved": False,
        "download_package_runtime_used": False,
        "public_access_runtime_used": False,
        "external_delivery_runtime_used": False,
        "final_delivery_runtime_used": False,
        "warning_count": 1,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "controlled_evidence_items": items,
        "controlled_evidence_layer_write_result": {
            "write_result_schema": "sentigraph_controlled_evidence_layer_write_result_v0_1",
            "controlled_evidence_layer_write_result_created": True,
            "controlled_evidence_item_count": 5,
            "evidence_layer_write_scope": "controlled_local_helper_test_path_only",
            "production_evidence_item_created": False,
            "production_case_created": False,
            "production_analysis_run_created": False,
            "review_queue_item_created": False,
            "production_review_queue_item_created": False,
            "analysis_ready": False,
            "report_ready": False,
            "human_review_required": True,
            "no_automatic_trust_upgrade": True,
        },
        "runtime_side_effects": _runtime_side_effects(),
        "warnings": ["manual_review_required", "selected_sample_only"],
        "blockers": [],
    }
    runtime.update(overrides)
    return runtime


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _assert_safe_output(value: object) -> None:
    serialized = _serialized(value)
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel not in serialized
    assert ":/" not in serialized
    assert ":\\" not in serialized


def _assert_all_side_effects_false(candidate_set: dict[str, object]) -> None:
    runtime_side_effects = candidate_set["runtime_side_effects"]
    assert isinstance(runtime_side_effects, dict)
    for flag, value in runtime_side_effects.items():
        assert value is False, flag


def _assert_blocked(candidate_set: dict[str, object], expected_reason: str) -> None:
    assert str(candidate_set["production_case_candidate_set_status"]).startswith("blocked_")
    assert expected_reason in candidate_set["blockers"]
    assert candidate_set["production_case_candidate_created"] is False
    assert candidate_set["production_case_candidate_count"] == 0
    assert candidate_set["production_case_candidates"] == []
    assert candidate_set["production_case_created"] is False
    assert candidate_set["production_analysis_run_created"] is False
    assert candidate_set["production_evidence_item_created"] is False
    assert candidate_set["review_queue_item_created"] is False
    assert candidate_set["production_review_queue_item_created"] is False
    assert candidate_set["review_queue_runtime_used"] is False
    _assert_all_side_effects_false(candidate_set)
    _assert_safe_output(candidate_set)


def test_ready_path_builds_one_controlled_production_case_candidate() -> None:
    assert APPROVAL_PHRASE == EXPECTED_APPROVAL_PHRASE
    assert APPROVAL_PHRASE.isascii()

    candidate_set = build_controlled_production_case_candidate_set(
        _valid_evidenceitem_runtime(),
        exact_approval_phrase=EXPECTED_APPROVAL_PHRASE,
    )

    assert candidate_set["production_case_candidate_set_schema"] == (
        "sentigraph_controlled_production_case_candidate_set_v0_1"
    )
    assert candidate_set["phase"] == "8W-31"
    assert candidate_set["production_case_candidate_set_status"] == (
        "production_case_candidate_set_warn_manual_review_required"
    )
    assert candidate_set["source_runtime_schema"] == (
        "sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1"
    )
    assert candidate_set["source_write_result_schema"] == "sentigraph_controlled_evidence_layer_write_result_v0_1"
    assert candidate_set["source_controlled_evidence_item_count"] == 5
    assert candidate_set["warning_count"] == 1
    assert candidate_set["human_review_required"] is True
    assert candidate_set["production_case_candidate_count"] == 1
    assert candidate_set["production_case_candidate_created"] is True
    assert candidate_set["production_case_candidate_only"] is True
    assert candidate_set["production_case_created"] is False
    assert candidate_set["production_analysis_run_created"] is False
    assert candidate_set["production_evidence_item_created"] is False
    assert candidate_set["review_queue_item_created"] is False
    assert candidate_set["production_review_queue_item_created"] is False
    assert candidate_set["review_queue_runtime_used"] is False
    assert candidate_set["analysis_ready"] is False
    assert candidate_set["report_ready"] is False
    assert candidate_set["b_end_ready"] is False
    assert candidate_set["sandbox_ready"] is False
    assert candidate_set["public_event_ready"] is False
    assert candidate_set["route_ready"] is False
    assert candidate_set["frontend_ready"] is False
    assert candidate_set["production_ready"] is False
    assert candidate_set["public_ready"] is False
    assert candidate_set["customer_ready"] is False
    assert candidate_set["no_automatic_trust_upgrade"] is True
    assert candidate_set["blockers"] == []
    assert "manual_review_required" in candidate_set["warnings"]
    assert candidate_set["audit_summary"]["analysis_effect"] == "none"
    assert candidate_set["audit_summary"]["production_side_effect"] == "none"

    candidates = candidate_set["production_case_candidates"]
    assert isinstance(candidates, list)
    assert len(candidates) == 1
    candidate = candidates[0]
    allowed_fields = {
        "production_case_candidate_schema",
        "production_case_candidate_id",
        "source_runtime_schema",
        "source_write_result_schema",
        "source_controlled_evidence_item_count",
        "source_controlled_evidence_item_refs",
        "case_id_hint",
        "package_role",
        "sample_role",
        "candidate_scope",
        "review_status",
        "verification_status",
        "trust_label",
        "warning_count",
        "warning_labels",
        "human_review_required",
        "no_automatic_trust_upgrade",
        "production_case_candidate_only",
        "redaction_status",
        "blocker_codes",
        "boundary_flags",
        "production_case_ready",
        "production_analysis_run_ready",
        "analysis_ready",
        "report_ready",
        "b_end_ready",
        "sandbox_ready",
        "route_ready",
        "frontend_ready",
        "public_ready",
        "customer_ready",
    }
    assert set(candidate) <= allowed_fields
    assert candidate["production_case_candidate_schema"] == "sentigraph_controlled_production_case_candidate_v0_1"
    assert candidate["source_controlled_evidence_item_count"] == 5
    assert len(candidate["source_controlled_evidence_item_refs"]) == 5
    assert candidate["candidate_scope"] == "controlled_local_helper_only"
    assert candidate["review_status"] == "review_needed"
    assert candidate["verification_status"] == "needs_review"
    assert candidate["trust_label"] == "medium_low"
    assert candidate["human_review_required"] is True
    assert candidate["no_automatic_trust_upgrade"] is True
    assert candidate["production_case_candidate_only"] is True
    assert candidate["production_case_ready"] is False
    assert candidate["production_analysis_run_ready"] is False
    assert candidate["analysis_ready"] is False
    assert candidate["report_ready"] is False
    assert candidate["b_end_ready"] is False
    assert candidate["sandbox_ready"] is False
    assert candidate["route_ready"] is False
    assert candidate["frontend_ready"] is False
    assert candidate["public_ready"] is False
    assert candidate["customer_ready"] is False
    assert candidate["boundary_flags"]["production_case_candidate_only"] is True
    assert candidate["boundary_flags"]["not_production_case"] is True
    assert candidate["boundary_flags"]["not_production_analysis_run"] is True
    assert candidate["boundary_flags"]["not_production_evidence_item"] is True
    assert candidate["boundary_flags"]["not_review_queue_item"] is True
    _assert_all_side_effects_false(candidate_set)
    _assert_safe_output(candidate_set)


@pytest.mark.parametrize(
    ("phrase", "expected_reason"),
    [
        (None, "blocked_missing_exact_approval"),
        ("", "blocked_missing_exact_approval"),
        ("wrong approval", "blocked_wrong_exact_approval"),
        (NON_ASCII_APPROVAL_PHRASE, "blocked_non_ascii_approval"),
        (MOJIBAKE_APPROVAL_PHRASE, "blocked_non_ascii_approval"),
        ("APPROVE_8W_31_CONTROLLED_PRODUCTION_CASE_CANDIDATE_HELPER_IMPLEMENTATI0N", "blocked_wrong_exact_approval"),
    ],
)
def test_exact_ascii_approval_required_before_candidate_construction_and_file_access(
    phrase: str | None,
    expected_reason: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def blocked_open(*args, **kwargs):
        raise AssertionError("8W-31 must not open files")

    monkeypatch.setattr(builtins, "open", blocked_open)
    monkeypatch.setattr(Path, "open", blocked_open)

    candidate_set = build_controlled_production_case_candidate_set(
        _valid_evidenceitem_runtime(),
        exact_approval_phrase=phrase,
    )

    _assert_blocked(candidate_set, expected_reason)


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("runtime_schema", "wrong", "source_runtime_schema_wrong"),
        ("write_result_schema", "wrong", "source_write_result_schema_wrong"),
        (
            "write_runtime_status",
            "evidence_layer_write_runtime_ready",
            "source_write_runtime_status_not_warn_manual_review",
        ),
        ("controlled_evidence_item_schema", "wrong", "source_controlled_evidence_item_schema_wrong"),
        ("controlled_evidence_item_count", 4, "source_controlled_evidence_item_count_not_five"),
        ("source_evidence_layer_write_candidate_count", 4, "source_evidence_layer_write_candidate_count_not_five"),
        ("warning_count", 0, "source_warning_count_not_one"),
        ("human_review_required", False, "source_human_review_required_not_true"),
        ("controlled_evidenceitem_created", False, "source_controlled_evidenceitem_created_not_true"),
        (
            "controlled_evidence_layer_write_result_created",
            False,
            "source_controlled_evidence_layer_write_result_created_not_true",
        ),
        ("evidence_item_created", False, "source_evidence_item_created_not_true"),
        ("evidence_items_created", False, "source_evidence_items_created_not_true"),
        ("evidence_layer_write", False, "source_evidence_layer_write_not_true"),
        ("production_evidence_item_created", True, "source_production_evidence_item_created_true"),
        ("production_case_created", True, "source_production_case_created_true"),
        ("production_analysis_run_created", True, "source_production_analysis_run_created_true"),
        ("review_queue_item_created", True, "source_review_queue_item_created_true"),
        ("production_review_queue_item_created", True, "source_production_review_queue_item_created_true"),
        ("review_queue_runtime_used", True, "source_review_queue_runtime_used_true"),
        ("route_ready", True, "source_route_ready_true"),
        ("frontend_ready", True, "source_frontend_ready_true"),
        ("public_ready", True, "source_public_ready_true"),
        ("customer_ready", True, "source_customer_ready_true"),
        ("private_collector_inspected", True, "source_private_collector_inspected_true"),
        ("real_exchange_dir_read", True, "source_real_exchange_dir_read_true"),
    ],
)
def test_source_validation_blocks_unsafe_runtime_fields(field: str, value: object, reason: str) -> None:
    candidate_set = build_controlled_production_case_candidate_set(
        _valid_evidenceitem_runtime(**{field: value}),
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
        ("created_production_evidence_items", "source_runtime_side_effect_true:created_production_evidence_items"),
        ("created_review_queue_items", "source_runtime_side_effect_true:created_review_queue_items"),
        ("created_production_review_queue_items", "source_runtime_side_effect_true:created_production_review_queue_items"),
        ("created_production_case", "source_runtime_side_effect_true:created_production_case"),
        ("created_production_analysis_run", "source_runtime_side_effect_true:created_production_analysis_run"),
        ("generated_b_end_report_runtime", "source_runtime_side_effect_true:generated_b_end_report_runtime"),
        ("generated_sandbox_runtime", "source_runtime_side_effect_true:generated_sandbox_runtime"),
        ("used_download_package_runtime", "source_runtime_side_effect_true:used_download_package_runtime"),
        ("generated_response_text", "source_runtime_side_effect_true:generated_response_text"),
        ("created_public_route", "source_runtime_side_effect_true:created_public_route"),
        ("modified_frontend", "source_runtime_side_effect_true:modified_frontend"),
        ("published_or_sent", "source_runtime_side_effect_true:published_or_sent"),
        ("auto_executed", "source_runtime_side_effect_true:auto_executed"),
    ],
)
def test_source_runtime_side_effects_block(runtime_flag: str, reason: str) -> None:
    source = _valid_evidenceitem_runtime()
    source["runtime_side_effects"] = _runtime_side_effects(**{runtime_flag: True})

    candidate_set = build_controlled_production_case_candidate_set(
        source,
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(candidate_set, reason)


def test_count_shape_blocks_when_items_do_not_match_expected_case_level_shape() -> None:
    too_few_items = [_controlled_evidence_item(index) for index in range(1, 5)]
    candidate_set = build_controlled_production_case_candidate_set(
        _valid_evidenceitem_runtime(
            controlled_evidence_items=too_few_items,
            controlled_evidence_item_count=4,
            source_evidence_layer_write_candidate_count=4,
        ),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(candidate_set, "source_controlled_evidence_item_count_not_five")


def test_forbidden_fields_in_source_items_block_or_never_emit() -> None:
    unsafe_item = _controlled_evidence_item(
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
        salt="actual-salt-should-never-appear",
        absolute_path="G:/private-collector/should-never-appear",
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
        production_case_id="production-case-001",
        production_analysis_run_id="production-analysis-run-001",
        production_evidence_item_id="production-evidence-item-001",
        review_queue_item_id="review-queue-item-001",
    )

    candidate_set = build_controlled_production_case_candidate_set(
        _valid_evidenceitem_runtime(
            controlled_evidence_items=[unsafe_item, *[_controlled_evidence_item(index) for index in range(2, 6)]],
            controlled_evidence_item_count=5,
            source_evidence_layer_write_candidate_count=5,
        ),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(candidate_set, "forbidden_source_controlled_evidence_item_field:raw_author_id")


def test_ready_path_never_opens_files(monkeypatch: pytest.MonkeyPatch) -> None:
    def blocked_open(*args, **kwargs):
        raise AssertionError("8W-31 must not open files")

    monkeypatch.setattr(builtins, "open", blocked_open)
    monkeypatch.setattr(Path, "open", blocked_open)

    candidate_set = build_controlled_production_case_candidate_set(
        _valid_evidenceitem_runtime(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    assert candidate_set["production_case_candidate_set_status"] == (
        "production_case_candidate_set_warn_manual_review_required"
    )
    assert candidate_set["production_case_candidate_count"] == 1


@pytest.mark.parametrize(
    "requested_action",
    [
        "production_case",
        "production_analysis_run",
        "production_evidence_item",
        "review_queue_item_creation",
        "production_review_queue_item_creation",
        "review_queue_runtime",
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
        "row_parsing",
        "private_collector",
        "real_exchange",
        "publish",
        "send",
        "post",
        "execute",
        "auto_execute",
    ],
)
def test_requested_side_effects_block_and_keep_flags_false(requested_action: str) -> None:
    candidate_set = build_controlled_production_case_candidate_set(
        _valid_evidenceitem_runtime(),
        exact_approval_phrase=APPROVAL_PHRASE,
        requested_actions=[requested_action],
    )

    assert candidate_set["production_case_candidate_set_status"].startswith("blocked_")
    assert f"requested_action_blocked:{requested_action}" in candidate_set["blockers"]
    assert candidate_set["production_case_created"] is False
    assert candidate_set["production_analysis_run_created"] is False
    assert candidate_set["production_evidence_item_created"] is False
    assert candidate_set["route_ready"] is False
    assert candidate_set["frontend_ready"] is False
    _assert_all_side_effects_false(candidate_set)
    _assert_safe_output(candidate_set)


def test_safe_summary_is_counts_and_boundaries_only() -> None:
    summary = build_safe_controlled_production_case_candidate_summary(
        _valid_evidenceitem_runtime(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    assert summary["summary_schema"] == "sentigraph_controlled_production_case_candidate_summary_v0_1"
    assert summary["phase"] == "8W-31"
    assert summary["production_case_candidate_set_schema"] == (
        "sentigraph_controlled_production_case_candidate_set_v0_1"
    )
    assert summary["production_case_candidate_set_status"] == "production_case_candidate_set_warn_manual_review_required"
    assert summary["production_case_candidate_count"] == 1
    assert summary["source_controlled_evidence_item_count"] == 5
    assert summary["warning_count"] == 1
    assert summary["human_review_required"] is True
    assert summary["production_case_candidate_created"] is True
    assert summary["production_case_created"] is False
    assert summary["production_analysis_run_created"] is False
    assert summary["production_evidence_item_created"] is False
    assert "production_case_candidates" not in summary
    assert "source_controlled_evidence_item_refs" not in _serialized(summary)
    assert "text_snippet_redacted" not in _serialized(summary)
    assert "production_case_id" not in _serialized(summary)
    assert "production_analysis_run_id" not in _serialized(summary)
    assert "review_action" not in _serialized(summary)
    assert "generated_response_text" not in _serialized(summary)
    _assert_safe_output(summary)
