from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest

from app.services import controlled_production_analysis_result_candidate as module
from app.services.controlled_production_analysis_result_candidate import (
    APPROVAL_PHRASE,
    build_controlled_production_analysis_result_candidate_set,
    build_safe_controlled_production_analysis_result_candidate_summary,
)


EXPECTED_APPROVAL_PHRASE = (
    "APPROVE_8W_43_CONTROLLED_PRODUCTION_ANALYSIS_RESULT_CANDIDATE_HELPER_IMPLEMENTATION"
)
NON_ASCII_APPROVAL_PHRASE = (
    "\u6279\u51c6 8W-43 Controlled Production Analysis Result Candidate Helper Implementation"
)
MOJIBAKE_APPROVAL_PHRASE = (
    "\u9395\u7470\u567f 8W-43 Controlled Production Analysis Result Candidate Helper Implementation"
)

FORBIDDEN_SENTINELS = (
    "production-analysis-result-id-should-never-appear",
    "analysis-result-id-should-never-appear",
    "actual-analysis-execution-id-should-never-appear",
    "analysis-execution-id-should-never-appear",
    "production-analysis-run-id-should-never-appear",
    "production-case-id-should-never-appear",
    "production-evidence-item-id-should-never-appear",
    "review-queue-item-id-should-never-appear",
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
    "actual-sentiment-should-never-appear",
    "actual-risk-should-never-appear",
    "actual-forecast-should-never-appear",
    "actual-narrative-should-never-appear",
    "actual-recommendation-should-never-appear",
    "actual-strategy-should-never-appear",
    "actual-public-conclusion-should-never-appear",
    "actual-customer-conclusion-should-never-appear",
)


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
        "created_production_evidence_items": False,
        "created_review_queue_items": False,
        "created_production_review_queue_items": False,
        "created_production_case": False,
        "created_production_analysis_run": False,
        "started_actual_analysis_execution": False,
        "started_analysis_execution": False,
        "created_analysis_result": False,
        "created_production_analysis_result": False,
        "created_report_candidate": False,
        "created_final_report": False,
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


def _source_analysis_result_candidate(**overrides: object) -> dict[str, object]:
    candidate: dict[str, object] = {
        "analysis_result_candidate_schema": "sentigraph_controlled_analysis_result_candidate_v0_1",
        "analysis_result_candidate_id": "controlled-analysis-result-candidate-001-hash-001",
        "source_actual_analysis_execution_candidate_id": (
            "controlled-actual-analysis-execution-candidate-001-hash-001"
        ),
        "source_actual_analysis_execution_candidate_ids": [
            "controlled-actual-analysis-execution-candidate-001-hash-001"
        ],
        "source_actual_analysis_execution_candidate_count": 1,
        "source_production_analysis_run_candidate_count": 1,
        "source_production_case_candidate_count": 1,
        "source_controlled_evidence_item_count": 5,
        "case_id_hint": "case-donglu-sunjihai-youth-football",
        "case_title_or_label_redacted": "donglu-sunjihai-youth-football-redacted",
        "input_scope_summary_redacted": "controlled_local_analysis_result_candidate_summary_only",
        "intended_result_scope_labels": [
            "candidate_only",
            "selected_sample_only",
            "human_review_required",
            "no_automatic_trust_upgrade",
        ],
        "intended_module_scope_labels": [
            "analysis_result_candidate_boundary",
            "no_production_analysis_result",
            "no_analysis_result_generation",
            "no_report_generation",
        ],
        "warning_count": 1,
        "human_review_required": True,
        "review_status": "human_review_required",
        "trust_boundary_label": "no_automatic_trust_upgrade",
        "verification_status_summary": "needs_review",
        "redaction_status": "redacted",
        "redaction_warnings": ["manual_review_required", "selected_sample_only"],
        "warning_labels": ["manual_review_required", "selected_sample_only"],
        "blocker_codes": [],
        "analysis_result_generation_readiness_blockers": [
            "analysis_result_generation_not_approved",
            "actual_analysis_execution_not_started",
            "human_review_required",
        ],
        "production_analysis_result_readiness_blockers": [
            "production_analysis_result_not_approved",
            "analysis_result_not_created",
            "human_review_required",
        ],
        "report_readiness_blockers": [
            "analysis_result_not_created",
            "report_generation_not_approved",
            "human_review_required",
        ],
        "analysis_result_candidate_only": True,
        "no_automatic_trust_upgrade": True,
        "production_analysis_result_created": False,
        "production_analysis_result_runtime_used": False,
        "analysis_result_generation_executed": False,
        "analysis_result_created": False,
        "actual_analysis_execution_started": False,
        "analysis_execution_started": False,
        "production_analysis_run_created": False,
        "production_case_created": False,
        "production_evidence_item_created": False,
        "report_ready": False,
        "boundary_flags": {
            "analysis_result_candidate_only": True,
            "controlled_actual_analysis_execution_candidate_derived_only": True,
            "human_review_required": True,
            "warning_preserving": True,
            "no_automatic_trust_upgrade": True,
            "not_analysis_result_generation": True,
            "not_analysis_result": True,
            "not_production_analysis_result": True,
            "not_actual_analysis_execution": True,
            "not_production_analysis_run": True,
            "not_production_case": True,
            "not_production_evidence_item": True,
            "not_review_queue_item": True,
            "not_report_ready": True,
            "not_frontend_ready": True,
            "not_route_ready": True,
            "not_public_ready": True,
            "not_customer_ready": True,
            "no_generated_response_text": True,
        },
    }
    candidate.update(overrides)
    return candidate


def _valid_source_analysis_result_candidate_set(**overrides: object) -> dict[str, object]:
    source: dict[str, object] = {
        "analysis_result_candidate_set_schema": "sentigraph_controlled_analysis_result_candidate_set_v0_1",
        "phase": "8W-40",
        "analysis_result_candidate_set_status": "analysis_result_candidate_set_warn_manual_review_required",
        "input_source_kind": "controlled_actual_analysis_execution_candidate",
        "source_actual_analysis_execution_candidate_set_schema": (
            "sentigraph_controlled_actual_analysis_execution_candidate_set_v0_1"
        ),
        "source_actual_analysis_execution_candidate_schema": (
            "sentigraph_controlled_actual_analysis_execution_candidate_v0_1"
        ),
        "source_actual_analysis_execution_candidate_count": 1,
        "source_production_analysis_run_candidate_count": 1,
        "source_production_case_candidate_count": 1,
        "source_controlled_evidence_item_count": 5,
        "analysis_result_candidate_mode": "backend_only_local_analysis_result_candidate_boundary",
        "analysis_result_candidate_count": 1,
        "warning_count": 1,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "actual_analysis_execution_candidate_created_upstream": True,
        "analysis_result_candidate_created": True,
        "analysis_result_candidate_only": True,
        "production_analysis_result_created": False,
        "production_analysis_result_runtime_used": False,
        "analysis_result_generation_executed": False,
        "analysis_result_created": False,
        "actual_analysis_execution_started": False,
        "analysis_execution_started": False,
        "production_analysis_run_created": False,
        "production_case_created": False,
        "production_evidence_item_created": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "review_queue_runtime_used": False,
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
        "boundary_flags": {
            "backend_only": True,
            "local_only": True,
            "analysis_result_candidate_only": True,
            "controlled_actual_analysis_execution_candidate_derived_only": True,
            "human_review_required": True,
            "warning_preserving": True,
            "no_automatic_trust_upgrade": True,
            "not_analysis_result_generation": True,
            "not_analysis_result": True,
            "not_production_analysis_result": True,
            "not_actual_analysis_execution": True,
            "not_production_analysis_run": True,
            "not_production_case": True,
            "not_production_evidence_item": True,
            "not_review_queue_item": True,
            "not_production_review_queue_item": True,
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
        "runtime_side_effects": _runtime_side_effects(),
        "warnings": ["manual_review_required", "selected_sample_only", "analysis_result_candidate_only"],
        "blockers": [],
        "audit_summary": {
            "audit_schema": "sentigraph_controlled_analysis_result_candidate_audit_summary_v0_1",
            "phase": "8W-40",
            "analysis_effect": "none",
            "analysis_result_effect": "none",
            "production_analysis_result_effect": "none",
            "actual_analysis_execution_effect": "none",
            "production_side_effect": "none",
            "human_review_required": True,
            "warning_count": 1,
            "analysis_result_candidate_count": 1,
            "review_queue_effect": "none",
            "route_api_frontend_effect": "none",
            "report_effect": "none",
            "delivery_effect": "none",
        },
        "analysis_result_candidates": [_source_analysis_result_candidate()],
    }
    source.update(overrides)
    return source


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
    assert str(candidate_set["production_analysis_result_candidate_set_status"]).startswith("blocked_")
    assert expected_reason in candidate_set["blockers"]
    assert candidate_set["production_analysis_result_candidate_created"] is False
    assert candidate_set["production_analysis_result_candidate_count"] == 0
    assert candidate_set["production_analysis_result_candidates"] == []
    assert candidate_set["production_analysis_result_created"] is False
    assert candidate_set["production_analysis_result_runtime_used"] is False
    assert candidate_set["analysis_result_generation_executed"] is False
    assert candidate_set["analysis_result_created"] is False
    assert candidate_set["actual_analysis_execution_started"] is False
    assert candidate_set["analysis_execution_started"] is False
    assert candidate_set["production_analysis_run_created"] is False
    assert candidate_set["production_case_created"] is False
    assert candidate_set["production_evidence_item_created"] is False
    assert candidate_set["review_queue_item_created"] is False
    assert candidate_set["production_review_queue_item_created"] is False
    assert candidate_set["review_queue_runtime_used"] is False
    _assert_all_side_effects_false(candidate_set)
    _assert_safe_output(candidate_set)


def test_ready_path_builds_one_controlled_production_analysis_result_candidate() -> None:
    assert APPROVAL_PHRASE == EXPECTED_APPROVAL_PHRASE
    assert APPROVAL_PHRASE.isascii()

    candidate_set = build_controlled_production_analysis_result_candidate_set(
        _valid_source_analysis_result_candidate_set(),
        exact_approval_phrase=EXPECTED_APPROVAL_PHRASE,
    )

    assert candidate_set["production_analysis_result_candidate_set_schema"] == (
        "sentigraph_controlled_production_analysis_result_candidate_set_v0_1"
    )
    assert candidate_set["phase"] == "8W-43"
    assert candidate_set["production_analysis_result_candidate_set_status"] == (
        "production_analysis_result_candidate_set_warn_manual_review_required"
    )
    assert candidate_set["input_source_kind"] == "controlled_analysis_result_candidate"
    assert candidate_set["source_analysis_result_candidate_set_schema"] == (
        "sentigraph_controlled_analysis_result_candidate_set_v0_1"
    )
    assert candidate_set["source_analysis_result_candidate_schema"] == (
        "sentigraph_controlled_analysis_result_candidate_v0_1"
    )
    assert candidate_set["source_analysis_result_candidate_count"] == 1
    assert candidate_set["source_actual_analysis_execution_candidate_count"] == 1
    assert candidate_set["source_production_analysis_run_candidate_count"] == 1
    assert candidate_set["source_production_case_candidate_count"] == 1
    assert candidate_set["source_controlled_evidence_item_count"] == 5
    assert candidate_set["production_analysis_result_candidate_mode"] == (
        "backend_only_local_production_analysis_result_candidate_boundary"
    )
    assert candidate_set["production_analysis_result_candidate_count"] == 1
    assert candidate_set["warning_count"] == 1
    assert candidate_set["human_review_required"] is True
    assert candidate_set["no_automatic_trust_upgrade"] is True
    assert candidate_set["analysis_result_candidate_created_upstream"] is True
    assert candidate_set["production_analysis_result_candidate_created"] is True
    assert candidate_set["production_analysis_result_created"] is False
    assert candidate_set["production_analysis_result_runtime_used"] is False
    assert candidate_set["analysis_result_generation_executed"] is False
    assert candidate_set["analysis_result_created"] is False
    assert candidate_set["actual_analysis_execution_started"] is False
    assert candidate_set["analysis_execution_started"] is False
    assert candidate_set["production_analysis_run_created"] is False
    assert candidate_set["production_case_created"] is False
    assert candidate_set["production_evidence_item_created"] is False
    assert candidate_set["review_queue_item_created"] is False
    assert candidate_set["production_review_queue_item_created"] is False
    assert candidate_set["review_queue_runtime_used"] is False
    assert candidate_set["route_ready"] is False
    assert candidate_set["frontend_ready"] is False
    assert candidate_set["blockers"] == []

    candidates = candidate_set["production_analysis_result_candidates"]
    assert isinstance(candidates, list)
    assert len(candidates) == 1
    candidate = candidates[0]
    allowed_fields = {
        "production_analysis_result_candidate_schema",
        "production_analysis_result_candidate_id",
        "source_analysis_result_candidate_id",
        "source_analysis_result_candidate_ids",
        "source_analysis_result_candidate_count",
        "source_actual_analysis_execution_candidate_count",
        "source_production_analysis_run_candidate_count",
        "source_production_case_candidate_count",
        "source_controlled_evidence_item_count",
        "case_id_hint",
        "case_title_or_label_redacted",
        "input_scope_summary_redacted",
        "intended_result_boundary_labels",
        "intended_module_scope_labels",
        "warning_count",
        "human_review_required",
        "review_status",
        "trust_boundary_label",
        "verification_status_summary",
        "redaction_status",
        "redaction_warnings",
        "warning_labels",
        "blocker_codes",
        "production_analysis_result_readiness_blockers",
        "report_readiness_blockers",
        "production_record_creation_blockers",
        "production_analysis_result_candidate_only",
        "no_automatic_trust_upgrade",
        "production_analysis_result_created",
        "production_analysis_result_runtime_used",
        "analysis_result_generation_executed",
        "analysis_result_created",
        "actual_analysis_execution_started",
        "analysis_execution_started",
        "production_analysis_run_created",
        "production_case_created",
        "production_evidence_item_created",
        "report_ready",
        "boundary_flags",
    }
    assert set(candidate) <= allowed_fields
    assert candidate["production_analysis_result_candidate_schema"] == (
        "sentigraph_controlled_production_analysis_result_candidate_v0_1"
    )
    assert candidate["source_analysis_result_candidate_count"] == 1
    assert candidate["source_actual_analysis_execution_candidate_count"] == 1
    assert candidate["source_production_analysis_run_candidate_count"] == 1
    assert candidate["source_production_case_candidate_count"] == 1
    assert candidate["source_controlled_evidence_item_count"] == 5
    assert candidate["review_status"] == "human_review_required"
    assert candidate["trust_boundary_label"] == "no_automatic_trust_upgrade"
    assert candidate["verification_status_summary"] == "needs_review"
    assert candidate["human_review_required"] is True
    assert candidate["production_analysis_result_candidate_only"] is True
    assert candidate["no_automatic_trust_upgrade"] is True
    assert candidate["production_analysis_result_created"] is False
    assert candidate["production_analysis_result_runtime_used"] is False
    assert candidate["analysis_result_generation_executed"] is False
    assert candidate["analysis_result_created"] is False
    assert candidate["actual_analysis_execution_started"] is False
    assert candidate["analysis_execution_started"] is False
    assert candidate["production_analysis_run_created"] is False
    assert candidate["production_case_created"] is False
    assert candidate["production_evidence_item_created"] is False
    assert candidate["report_ready"] is False
    assert "manual_review_required" in candidate["warning_labels"]
    assert "production_analysis_result_not_approved" in candidate[
        "production_analysis_result_readiness_blockers"
    ]
    assert "analysis_result_not_created" in candidate["report_readiness_blockers"]
    assert "production_analysis_run_creation_not_approved" in candidate[
        "production_record_creation_blockers"
    ]
    assert candidate["boundary_flags"]["production_analysis_result_candidate_only"] is True
    assert candidate["boundary_flags"]["not_production_analysis_result"] is True
    assert candidate["boundary_flags"]["not_analysis_result_generation"] is True
    assert candidate["boundary_flags"]["not_report_ready"] is True
    _assert_all_side_effects_false(candidate_set)
    _assert_safe_output(candidate_set)


@pytest.mark.parametrize(
    ("phrase", "expected_reason"),
    [
        (None, "blocked_missing_exact_approval"),
        ("", "blocked_missing_exact_approval"),
        ("wrong approval", "blocked_wrong_exact_approval"),
        (
            "APPROVE_8W_43_CONTROLLED_PRODUCTION_ANALYSIS_RESULT_CANDIDATE_HELPER_IMPLEMENTATI0N",
            "blocked_wrong_exact_approval",
        ),
        (NON_ASCII_APPROVAL_PHRASE, "blocked_non_ascii_approval"),
        (MOJIBAKE_APPROVAL_PHRASE, "blocked_non_ascii_approval"),
    ],
)
def test_exact_ascii_approval_required_before_candidate_construction_and_file_access(
    phrase: str | None,
    expected_reason: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def blocked_open(*args, **kwargs):
        raise AssertionError("8W-43 must not open files")

    def blocked_candidate(*args, **kwargs):
        raise AssertionError("8W-43 must not construct candidates on wrong approval")

    monkeypatch.setattr(builtins, "open", blocked_open)
    monkeypatch.setattr(Path, "open", blocked_open)
    monkeypatch.setattr(module, "_candidate_from_source", blocked_candidate)

    candidate_set = build_controlled_production_analysis_result_candidate_set(
        _valid_source_analysis_result_candidate_set(),
        exact_approval_phrase=phrase,
    )

    _assert_blocked(candidate_set, expected_reason)


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("analysis_result_candidate_set_schema", "wrong", "source_analysis_result_candidate_set_schema_wrong"),
        (
            "analysis_result_candidate_set_status",
            "analysis_result_candidate_set_ready",
            "source_analysis_result_candidate_set_status_not_warn_manual_review",
        ),
        ("analysis_result_candidate_count", 2, "source_analysis_result_candidate_count_not_one"),
        (
            "source_actual_analysis_execution_candidate_count",
            2,
            "source_actual_analysis_execution_candidate_count_not_one",
        ),
        (
            "source_production_analysis_run_candidate_count",
            2,
            "source_production_analysis_run_candidate_count_not_one",
        ),
        ("source_production_case_candidate_count", 2, "source_production_case_candidate_count_not_one"),
        ("source_controlled_evidence_item_count", 4, "source_controlled_evidence_item_count_not_five"),
        ("warning_count", 0, "source_warning_count_not_one"),
        ("human_review_required", False, "source_human_review_required_not_true"),
        ("no_automatic_trust_upgrade", False, "source_no_automatic_trust_upgrade_not_true"),
        ("analysis_result_candidate_created", False, "source_analysis_result_candidate_created_not_true"),
        ("production_analysis_result_created", True, "source_production_analysis_result_created_true"),
        ("analysis_result_generation_executed", True, "source_analysis_result_generation_executed_true"),
        ("analysis_result_created", True, "source_analysis_result_created_true"),
        ("actual_analysis_execution_started", True, "source_actual_analysis_execution_started_true"),
        ("analysis_execution_started", True, "source_analysis_execution_started_true"),
        ("production_analysis_run_created", True, "source_production_analysis_run_created_true"),
        ("production_case_created", True, "source_production_case_created_true"),
        ("production_evidence_item_created", True, "source_production_evidence_item_created_true"),
        ("review_queue_item_created", True, "source_review_queue_item_created_true"),
        ("production_review_queue_item_created", True, "source_production_review_queue_item_created_true"),
        ("review_queue_runtime_used", True, "source_review_queue_runtime_used_true"),
        ("route_ready", True, "source_route_ready_true"),
        ("frontend_ready", True, "source_frontend_ready_true"),
        ("private_collector_inspected", True, "source_private_collector_inspected_true"),
        ("real_exchange_dir_read", True, "source_real_exchange_dir_read_true"),
    ],
)
def test_source_validation_blocks_unsafe_candidate_set_fields(field: str, value: object, reason: str) -> None:
    candidate_set = build_controlled_production_analysis_result_candidate_set(
        _valid_source_analysis_result_candidate_set(**{field: value}),
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
        (
            "created_production_review_queue_items",
            "source_runtime_side_effect_true:created_production_review_queue_items",
        ),
        ("created_production_case", "source_runtime_side_effect_true:created_production_case"),
        ("created_production_analysis_run", "source_runtime_side_effect_true:created_production_analysis_run"),
        ("started_actual_analysis_execution", "source_runtime_side_effect_true:started_actual_analysis_execution"),
        ("started_analysis_execution", "source_runtime_side_effect_true:started_analysis_execution"),
        ("created_analysis_result", "source_runtime_side_effect_true:created_analysis_result"),
        ("created_production_analysis_result", "source_runtime_side_effect_true:created_production_analysis_result"),
        ("created_report_candidate", "source_runtime_side_effect_true:created_report_candidate"),
        ("created_final_report", "source_runtime_side_effect_true:created_final_report"),
        ("generated_b_end_report_runtime", "source_runtime_side_effect_true:generated_b_end_report_runtime"),
        ("generated_sandbox_runtime", "source_runtime_side_effect_true:generated_sandbox_runtime"),
        ("generated_public_event_runtime", "source_runtime_side_effect_true:generated_public_event_runtime"),
        ("used_download_package_runtime", "source_runtime_side_effect_true:used_download_package_runtime"),
        ("generated_response_text", "source_runtime_side_effect_true:generated_response_text"),
        ("created_public_route", "source_runtime_side_effect_true:created_public_route"),
        ("modified_frontend", "source_runtime_side_effect_true:modified_frontend"),
        ("published_or_sent", "source_runtime_side_effect_true:published_or_sent"),
        ("auto_executed", "source_runtime_side_effect_true:auto_executed"),
    ],
)
def test_source_runtime_side_effects_block(runtime_flag: str, reason: str) -> None:
    source = _valid_source_analysis_result_candidate_set()
    source["runtime_side_effects"] = _runtime_side_effects(**{runtime_flag: True})

    candidate_set = build_controlled_production_analysis_result_candidate_set(
        source,
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(candidate_set, reason)


def test_candidate_count_blocks_when_source_candidates_absent_or_malformed() -> None:
    absent = build_controlled_production_analysis_result_candidate_set(
        _valid_source_analysis_result_candidate_set(analysis_result_candidates=[]),
        exact_approval_phrase=APPROVAL_PHRASE,
    )
    _assert_blocked(absent, "source_analysis_result_candidates_count_not_one")

    malformed = build_controlled_production_analysis_result_candidate_set(
        _valid_source_analysis_result_candidate_set(analysis_result_candidates=[{"wrong": "shape"}]),
        exact_approval_phrase=APPROVAL_PHRASE,
    )
    _assert_blocked(malformed, "source_analysis_result_candidate_schema_wrong")


def test_forbidden_fields_in_source_candidate_block_or_never_emit() -> None:
    unsafe_candidate = _source_analysis_result_candidate(
        production_analysis_result_id="production-analysis-result-id-should-never-appear",
        analysis_result_id="analysis-result-id-should-never-appear",
        actual_analysis_execution_id="actual-analysis-execution-id-should-never-appear",
        analysis_execution_id="analysis-execution-id-should-never-appear",
        production_analysis_run_id="production-analysis-run-id-should-never-appear",
        analysis_run_id="production-analysis-run-id-should-never-appear",
        production_case_id="production-case-id-should-never-appear",
        production_evidence_item_id="production-evidence-item-id-should-never-appear",
        review_queue_item_id="review-queue-item-id-should-never-appear",
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
        sentiment_score=0.9,
        risk_score=0.9,
        forecast="actual-forecast-should-never-appear",
        narrative="actual-narrative-should-never-appear",
        recommendation="actual-recommendation-should-never-appear",
        strategy="actual-strategy-should-never-appear",
        review_action="approve",
        reviewer_assignment="reviewer-1",
        review_decision="approved",
        audit_timeline=["should-never-appear"],
    )

    candidate_set = build_controlled_production_analysis_result_candidate_set(
        _valid_source_analysis_result_candidate_set(analysis_result_candidates=[unsafe_candidate]),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(candidate_set, "forbidden_source_analysis_result_candidate_field:production_analysis_result_id")


def test_ready_path_never_opens_files(monkeypatch: pytest.MonkeyPatch) -> None:
    def blocked_open(*args, **kwargs):
        raise AssertionError("8W-43 must not open files")

    monkeypatch.setattr(builtins, "open", blocked_open)
    monkeypatch.setattr(Path, "open", blocked_open)

    candidate_set = build_controlled_production_analysis_result_candidate_set(
        _valid_source_analysis_result_candidate_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    assert candidate_set["production_analysis_result_candidate_set_status"] == (
        "production_analysis_result_candidate_set_warn_manual_review_required"
    )
    assert candidate_set["production_analysis_result_candidate_count"] == 1


@pytest.mark.parametrize(
    "requested_action",
    [
        "production_analysis_result",
        "analysis_result_generation",
        "actual_analysis_execution",
        "analysis_execution",
        "production_analysis_run",
        "production_case",
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
    candidate_set = build_controlled_production_analysis_result_candidate_set(
        _valid_source_analysis_result_candidate_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
        requested_actions=[requested_action],
    )

    assert candidate_set["production_analysis_result_candidate_set_status"].startswith("blocked_")
    assert f"requested_action_blocked:{requested_action}" in candidate_set["blockers"]
    assert candidate_set["production_analysis_result_created"] is False
    assert candidate_set["production_analysis_result_runtime_used"] is False
    assert candidate_set["analysis_result_generation_executed"] is False
    assert candidate_set["analysis_result_created"] is False
    assert candidate_set["actual_analysis_execution_started"] is False
    assert candidate_set["analysis_execution_started"] is False
    assert candidate_set["production_analysis_run_created"] is False
    assert candidate_set["production_case_created"] is False
    assert candidate_set["production_evidence_item_created"] is False
    assert candidate_set["route_ready"] is False
    assert candidate_set["frontend_ready"] is False
    _assert_all_side_effects_false(candidate_set)
    _assert_safe_output(candidate_set)


def test_safe_summary_is_counts_and_boundaries_only() -> None:
    summary = build_safe_controlled_production_analysis_result_candidate_summary(
        _valid_source_analysis_result_candidate_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    assert summary["summary_schema"] == (
        "sentigraph_controlled_production_analysis_result_candidate_summary_v0_1"
    )
    assert summary["phase"] == "8W-43"
    assert summary["production_analysis_result_candidate_set_schema"] == (
        "sentigraph_controlled_production_analysis_result_candidate_set_v0_1"
    )
    assert summary["production_analysis_result_candidate_set_status"] == (
        "production_analysis_result_candidate_set_warn_manual_review_required"
    )
    assert summary["production_analysis_result_candidate_count"] == 1
    assert summary["source_analysis_result_candidate_count"] == 1
    assert summary["source_actual_analysis_execution_candidate_count"] == 1
    assert summary["source_production_analysis_run_candidate_count"] == 1
    assert summary["source_production_case_candidate_count"] == 1
    assert summary["source_controlled_evidence_item_count"] == 5
    assert summary["warning_count"] == 1
    assert summary["human_review_required"] is True
    assert summary["production_analysis_result_candidate_created"] is True
    assert summary["production_analysis_result_created"] is False
    assert summary["production_analysis_result_runtime_used"] is False
    assert summary["analysis_result_generation_executed"] is False
    assert summary["analysis_result_created"] is False
    assert summary["actual_analysis_execution_started"] is False
    assert summary["analysis_execution_started"] is False
    assert summary["production_analysis_run_created"] is False
    assert summary["production_case_created"] is False
    assert summary["production_evidence_item_created"] is False
    assert "production_analysis_result_candidates" not in summary
    assert "source_analysis_result_candidate_id" not in _serialized(summary)
    assert "production_analysis_result_id" not in _serialized(summary)
    assert "analysis_result_id" not in _serialized(summary)
    assert "actual_analysis_execution_id" not in _serialized(summary)
    assert "generated_response_text" not in _serialized(summary)
    _assert_safe_output(summary)
