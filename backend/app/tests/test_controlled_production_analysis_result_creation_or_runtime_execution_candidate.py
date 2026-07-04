from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest

from app.services import controlled_production_analysis_result_creation_or_runtime_execution_candidate as module
from app.services.controlled_production_analysis_result_creation_or_runtime_execution_candidate import (
    APPROVAL_PHRASE,
    build_controlled_production_analysis_result_creation_or_runtime_execution_candidate_set,
    build_safe_controlled_production_analysis_result_creation_or_runtime_execution_candidate_summary,
)


EXPECTED_APPROVAL_PHRASE = (
    "APPROVE_8W_52_CONTROLLED_PRODUCTION_ANALYSIS_RESULT_CREATION_OR_RUNTIME_EXECUTION_CANDIDATE_HELPER_IMPLEMENTATION"
)
NON_ASCII_APPROVAL_PHRASE = (
    "\u6279\u51c6 8W-52 Controlled Production Analysis Result Creation Runtime Execution Candidate Helper Implementation"
)
MOJIBAKE_APPROVAL_PHRASE = (
    "\u9395\u7470\u567f 8W-52 Controlled Production Analysis Result Creation Runtime Execution Candidate Helper Implementation"
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
    flags = {name: False for name in module.RUNTIME_SIDE_EFFECT_FLAGS}
    flags.update(overrides)
    return flags


def _source_runtime_boundary(**overrides: object) -> dict[str, object]:
    boundary: dict[str, object] = {
        "production_analysis_result_runtime_boundary_schema": (
            "sentigraph_controlled_production_analysis_result_runtime_boundary_v0_1"
        ),
        "production_analysis_result_runtime_boundary_id": (
            "controlled-production-analysis-result-runtime-boundary-001-hash-001"
        ),
        "source_production_analysis_result_boundary_id": (
            "controlled-production-analysis-result-boundary-001-hash-001"
        ),
        "source_production_analysis_result_boundary_ids": [
            "controlled-production-analysis-result-boundary-001-hash-001"
        ],
        "source_production_analysis_result_runtime_boundary_count": 1,
        "source_production_analysis_result_boundary_count": 1,
        "source_production_analysis_result_candidate_count": 1,
        "source_analysis_result_candidate_count": 1,
        "source_actual_analysis_execution_candidate_count": 1,
        "source_production_analysis_run_candidate_count": 1,
        "source_production_case_candidate_count": 1,
        "source_controlled_evidence_item_count": 5,
        "case_id_hint": "case-donglu-sunjihai-youth-football",
        "case_title_or_label_redacted": "donglu-sunjihai-youth-football-redacted",
        "input_scope_summary_redacted": "controlled_local_production_analysis_result_runtime_boundary_summary_only",
        "intended_runtime_boundary_labels": [
            "runtime_boundary_only",
            "selected_sample_only",
            "human_review_required",
            "no_automatic_trust_upgrade",
        ],
        "intended_module_scope_labels": [
            "production_analysis_result_runtime_boundary",
            "no_production_analysis_result",
            "no_production_analysis_result_runtime_use",
            "no_analysis_result_generation",
        ],
        "runtime_gate_labels": [
            "runtime_gate_only",
            "manual_review_required",
            "not_runtime_execution",
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
        "production_analysis_result_runtime_readiness_blockers": [
            "production_analysis_result_runtime_not_approved",
            "human_review_required",
        ],
        "production_analysis_result_creation_readiness_blockers": [
            "production_analysis_result_creation_not_approved",
            "human_review_required",
        ],
        "production_runtime_blockers": [
            "production_analysis_result_runtime_not_approved",
            "human_review_required",
        ],
        "report_readiness_blockers": [
            "analysis_result_not_created",
            "report_generation_not_approved",
            "human_review_required",
        ],
        "production_record_creation_blockers": [
            "production_analysis_run_creation_not_approved",
            "production_case_creation_not_approved",
            "production_evidence_item_creation_not_approved",
        ],
        "runtime_boundary_only": True,
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
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "review_queue_runtime_used": False,
        "report_ready": False,
        "boundary_flags": {
            "runtime_boundary_only": True,
            "human_review_required": True,
            "warning_preserving": True,
            "not_production_analysis_result": True,
            "not_production_analysis_result_runtime_use": True,
            "not_analysis_result_generation": True,
            "not_actual_analysis_execution": True,
            "not_production_analysis_run": True,
            "not_production_case": True,
            "not_production_evidence_item": True,
            "not_review_queue_item": True,
            "not_production_review_queue_item": True,
            "no_generated_response_text": True,
        },
    }
    boundary.update(overrides)
    return boundary


def _valid_runtime_boundary_set(**overrides: object) -> dict[str, object]:
    source: dict[str, object] = {
        "production_analysis_result_runtime_boundary_set_schema": (
            "sentigraph_controlled_production_analysis_result_runtime_boundary_set_v0_1"
        ),
        "phase": "8W-49",
        "production_analysis_result_runtime_boundary_set_status": (
            "production_analysis_result_runtime_boundary_set_warn_manual_review_required"
        ),
        "input_source_kind": "controlled_production_analysis_result_boundary",
        "source_production_analysis_result_boundary_set_schema": (
            "sentigraph_controlled_production_analysis_result_boundary_set_v0_1"
        ),
        "source_production_analysis_result_boundary_schema": (
            "sentigraph_controlled_production_analysis_result_boundary_v0_1"
        ),
        "source_production_analysis_result_boundary_count": 1,
        "source_production_analysis_result_candidate_count": 1,
        "source_analysis_result_candidate_count": 1,
        "source_actual_analysis_execution_candidate_count": 1,
        "source_production_analysis_run_candidate_count": 1,
        "source_production_case_candidate_count": 1,
        "source_controlled_evidence_item_count": 5,
        "runtime_boundary_mode": "backend_only_local_production_analysis_result_runtime_boundary",
        "production_analysis_result_runtime_boundary_count": 1,
        "warning_count": 1,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_analysis_result_boundary_created_upstream": True,
        "production_analysis_result_runtime_boundary_created": True,
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
        "8w50_decision": "ready",
        "8w51_decision": "ready",
        "8w51_selected_next_boundary_option": (
            "ready_for_8W_52_controlled_production_analysis_result_creation_or_runtime_execution_candidate_helper_implementation_after_explicit_approval"
        ),
        "runtime_side_effects": _runtime_side_effects(),
        "production_analysis_result_runtime_boundaries": [_source_runtime_boundary()],
        "boundary_flags": {
            "backend_only": True,
            "local_only": True,
            "runtime_boundary_only": True,
            "human_review_required": True,
            "warning_preserving": True,
            "not_production_analysis_result": True,
            "not_production_analysis_result_runtime_use": True,
            "not_analysis_result_generation": True,
            "not_actual_analysis_execution": True,
        },
        "warnings": ["manual_review_required", "selected_sample_only"],
        "blockers": [],
        "audit_summary": {
            "analysis_effect": "none",
            "production_analysis_result_effect": "none",
            "production_analysis_result_runtime_effect": "none",
        },
    }
    source.update(overrides)
    return source


def _assert_no_forbidden_payload(payload: object) -> None:
    encoded = json.dumps(payload, sort_keys=True)
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel not in encoded


def _build_ready(source: dict[str, object] | None = None) -> dict[str, object]:
    return build_controlled_production_analysis_result_creation_or_runtime_execution_candidate_set(
        source or _valid_runtime_boundary_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )


def test_approval_phrase_constant_is_exact_ascii() -> None:
    assert APPROVAL_PHRASE == EXPECTED_APPROVAL_PHRASE
    assert APPROVAL_PHRASE.isascii()


def test_ready_path_builds_one_warning_preserving_candidate() -> None:
    result = _build_ready()

    assert result["production_analysis_result_creation_or_runtime_execution_candidate_set_schema"] == (
        "sentigraph_controlled_production_analysis_result_creation_or_runtime_execution_candidate_set_v0_1"
    )
    assert result["production_analysis_result_creation_or_runtime_execution_candidate_set_status"] == (
        "production_analysis_result_creation_or_runtime_execution_candidate_set_warn_manual_review_required"
    )
    assert result["production_analysis_result_creation_or_runtime_execution_candidate_count"] == 1
    assert result["source_production_analysis_result_runtime_boundary_set_schema"] == (
        "sentigraph_controlled_production_analysis_result_runtime_boundary_set_v0_1"
    )
    assert result["source_production_analysis_result_runtime_boundary_schema"] == (
        "sentigraph_controlled_production_analysis_result_runtime_boundary_v0_1"
    )
    assert result["source_production_analysis_result_runtime_boundary_count"] == 1
    assert result["source_production_analysis_result_boundary_count"] == 1
    assert result["source_production_analysis_result_candidate_count"] == 1
    assert result["source_analysis_result_candidate_count"] == 1
    assert result["source_actual_analysis_execution_candidate_count"] == 1
    assert result["source_production_analysis_run_candidate_count"] == 1
    assert result["source_production_case_candidate_count"] == 1
    assert result["source_controlled_evidence_item_count"] == 5
    assert result["warning_count"] == 1
    assert result["human_review_required"] is True
    assert result["no_automatic_trust_upgrade"] is True
    assert result["production_analysis_result_creation_or_runtime_execution_candidate_created"] is True
    assert result["production_analysis_result_created"] is False
    assert result["production_analysis_result_runtime_used"] is False
    assert result["analysis_result_generation_executed"] is False
    assert result["analysis_result_created"] is False
    assert result["actual_analysis_execution_started"] is False
    assert result["analysis_execution_started"] is False
    assert result["production_analysis_run_created"] is False
    assert result["production_case_created"] is False
    assert result["production_evidence_item_created"] is False
    assert result["review_queue_item_created"] is False
    assert result["production_review_queue_item_created"] is False
    assert result["review_queue_runtime_used"] is False
    assert result["route_ready"] is False
    assert result["frontend_ready"] is False
    assert result["runtime_side_effects"] == _runtime_side_effects()
    assert result["blockers"] == []

    candidates = result["production_analysis_result_creation_or_runtime_execution_candidates"]
    assert len(candidates) == 1
    candidate = candidates[0]
    assert candidate["production_analysis_result_creation_or_runtime_execution_candidate_schema"] == (
        "sentigraph_controlled_production_analysis_result_creation_or_runtime_execution_candidate_v0_1"
    )
    assert candidate["candidate_only"] is True
    assert candidate["human_review_required"] is True
    assert candidate["production_analysis_result_created"] is False
    assert candidate["production_analysis_result_runtime_used"] is False
    assert candidate["analysis_result_generation_executed"] is False
    assert candidate["actual_analysis_execution_started"] is False
    assert candidate["review_queue_runtime_used"] is False
    assert candidate["boundary_flags"]["not_production_analysis_result"] is True
    _assert_no_forbidden_payload(result)


@pytest.mark.parametrize(
    ("phrase", "expected_status"),
    [
        (None, "blocked_missing_exact_approval"),
        ("", "blocked_missing_exact_approval"),
        ("APPROVE_8W_52_CONTROLLED_PRODUCTION_ANALYSIS_RESULT_CREATION_OR_RUNTIME_EXECUTION_CANDIDATE_HELPER_IMPLEMENTATI0N", "blocked_wrong_exact_approval"),
        (NON_ASCII_APPROVAL_PHRASE, "blocked_non_ascii_approval"),
        (MOJIBAKE_APPROVAL_PHRASE, "blocked_non_ascii_approval"),
    ],
)
def test_exact_approval_phrase_required_before_candidate_construction(
    phrase: str | None,
    expected_status: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_open(*args: object, **kwargs: object) -> None:
        raise AssertionError("file access is not allowed")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "open", fail_open)

    result = build_controlled_production_analysis_result_creation_or_runtime_execution_candidate_set(
        _valid_runtime_boundary_set(),
        exact_approval_phrase=phrase,
    )

    assert result["production_analysis_result_creation_or_runtime_execution_candidate_set_status"] == expected_status
    assert result["production_analysis_result_creation_or_runtime_execution_candidate_count"] == 0
    assert result["production_analysis_result_creation_or_runtime_execution_candidate_created"] is False
    assert result["production_analysis_result_creation_or_runtime_execution_candidates"] == []


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("production_analysis_result_runtime_boundary_set_schema", "wrong"),
        ("production_analysis_result_runtime_boundary_set_status", "wrong"),
        ("production_analysis_result_runtime_boundary_count", 2),
        ("source_production_analysis_result_boundary_count", 2),
        ("source_production_analysis_result_candidate_count", 2),
        ("source_analysis_result_candidate_count", 2),
        ("source_actual_analysis_execution_candidate_count", 2),
        ("source_production_analysis_run_candidate_count", 2),
        ("source_production_case_candidate_count", 2),
        ("source_controlled_evidence_item_count", 6),
        ("warning_count", 0),
        ("human_review_required", False),
        ("no_automatic_trust_upgrade", False),
        ("8w50_decision", "needs_fix"),
        ("8w51_decision", "needs_fix"),
        ("8w51_selected_next_boundary_option", "pause"),
        ("production_analysis_result_created", True),
        ("production_analysis_result_runtime_used", True),
        ("analysis_result_generation_executed", True),
        ("analysis_result_created", True),
        ("actual_analysis_execution_started", True),
        ("analysis_execution_started", True),
        ("production_analysis_run_created", True),
        ("production_case_created", True),
        ("production_evidence_item_created", True),
        ("review_queue_item_created", True),
        ("production_review_queue_item_created", True),
        ("review_queue_runtime_used", True),
        ("route_ready", True),
        ("frontend_ready", True),
    ],
)
def test_source_boundary_validation_blocks_unsafe_inputs(field: str, value: object) -> None:
    result = _build_ready(_valid_runtime_boundary_set(**{field: value}))

    assert result["production_analysis_result_creation_or_runtime_execution_candidate_set_status"] != (
        "production_analysis_result_creation_or_runtime_execution_candidate_set_warn_manual_review_required"
    )
    assert result["production_analysis_result_creation_or_runtime_execution_candidate_count"] == 0
    assert result["production_analysis_result_creation_or_runtime_execution_candidate_created"] is False
    assert result["blockers"]


@pytest.mark.parametrize(
    "flag",
    [
        "called_real_api",
        "called_real_llm",
        "ran_provider_job",
        "ran_collector",
        "fetched_url",
        "scraped_page",
        "accessed_private_collector",
        "inspected_private_collector_source",
        "read_real_exchange_dir",
        "parsed_evidence_items_jsonl_again",
        "parsed_evidence_items_csv",
        "created_production_evidence_items",
        "created_review_queue_items",
        "created_production_review_queue_items",
        "created_production_case",
        "created_production_analysis_run",
        "started_actual_analysis_execution",
        "started_analysis_execution",
        "created_analysis_result",
        "created_production_analysis_result",
        "used_production_analysis_result_runtime",
        "generated_b_end_report_runtime",
        "generated_sandbox_runtime",
        "generated_public_event_runtime",
        "used_download_package_runtime",
        "used_public_access_runtime",
        "used_external_delivery_runtime",
        "used_final_delivery_runtime",
        "generated_response_text",
        "created_public_route",
        "modified_frontend",
    ],
)
def test_runtime_side_effect_flags_true_block(flag: str) -> None:
    result = _build_ready(_valid_runtime_boundary_set(runtime_side_effects=_runtime_side_effects(**{flag: True})))

    assert result["production_analysis_result_creation_or_runtime_execution_candidate_set_status"] == (
        "blocked_source_boundary_violation"
    )
    assert result["production_analysis_result_creation_or_runtime_execution_candidate_created"] is False
    assert any(flag in blocker for blocker in result["blockers"])


@pytest.mark.parametrize(
    "requested_action",
    [
        "production_analysis_result",
        "production_analysis_result_runtime",
        "analysis_result_generation",
        "actual_analysis_execution",
        "production_analysis_run",
        "production_case",
        "production_evidence_item",
        "review_queue_runtime",
        "route_api",
        "frontend_route",
        "b_end_report",
        "sandbox_public_event",
        "download_package",
        "public_access",
        "external_delivery",
        "final_delivery",
        "real_api",
        "real_llm",
        "collector_job",
        "private_collector",
        "real_exchange",
    ],
)
def test_requested_side_effect_actions_block(requested_action: str) -> None:
    result = build_controlled_production_analysis_result_creation_or_runtime_execution_candidate_set(
        _valid_runtime_boundary_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
        requested_actions=[requested_action],
    )

    assert result["production_analysis_result_creation_or_runtime_execution_candidate_set_status"].startswith(
        "blocked_"
    )
    assert result["production_analysis_result_creation_or_runtime_execution_candidate_count"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("raw_author_id", "actual-raw-author-should-never-appear"),
        ("author_name", "actual-author-name-should-never-appear"),
        ("profile_url", "actual-profile-url-should-never-appear"),
        ("raw_comments", ["actual-raw-comment-should-never-appear"]),
        ("token", "actual-token-should-never-appear"),
        ("absolute_path", "G:/private-collector/should-never-appear"),
        ("production_analysis_result_id", "production-analysis-result-id-should-never-appear"),
        ("analysis_result_id", "analysis-result-id-should-never-appear"),
        ("actual_analysis_execution_id", "actual-analysis-execution-id-should-never-appear"),
        ("production_analysis_run_id", "production-analysis-run-id-should-never-appear"),
        ("production_case_id", "production-case-id-should-never-appear"),
        ("production_evidence_item_id", "production-evidence-item-id-should-never-appear"),
        ("target_user_list", ["target-user-should-never-appear"]),
        ("persuasion_score", 0.9),
        ("truth_score", 0.9),
        ("official_verified", True),
        ("prediction_probability", 0.9),
        ("psychological_profile", "profile-should-never-appear"),
        ("personality_diagnosis", "diagnosis-should-never-appear"),
        ("sentiment_score", 0.8),
        ("risk_score", 0.8),
        ("forecast", "actual-forecast-should-never-appear"),
        ("narrative", "actual-narrative-should-never-appear"),
        ("recommendation", "actual-recommendation-should-never-appear"),
        ("strategy", "actual-strategy-should-never-appear"),
    ],
)
def test_forbidden_fields_block_and_are_not_emitted(field: str, value: object) -> None:
    source = _valid_runtime_boundary_set(**{field: value})

    result = _build_ready(source)

    assert result["production_analysis_result_creation_or_runtime_execution_candidate_set_status"] == (
        "blocked_forbidden_field_detected"
    )
    assert result["production_analysis_result_creation_or_runtime_execution_candidate_count"] == 0
    _assert_no_forbidden_payload(result)


def test_ready_path_does_not_open_files(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_open(*args: object, **kwargs: object) -> None:
        raise AssertionError("file access is not allowed")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "open", fail_open)

    result = _build_ready()

    assert result["production_analysis_result_creation_or_runtime_execution_candidate_count"] == 1
    assert result["production_analysis_result_creation_or_runtime_execution_candidate_created"] is True


def test_missing_source_runtime_boundary_blocks() -> None:
    result = _build_ready(_valid_runtime_boundary_set(production_analysis_result_runtime_boundaries=[]))

    assert result["production_analysis_result_creation_or_runtime_execution_candidate_set_status"] == (
        "blocked_invalid_source_production_analysis_result_runtime_boundary"
    )
    assert result["production_analysis_result_creation_or_runtime_execution_candidate_count"] == 0


def test_multiple_candidate_request_blocks() -> None:
    result = build_controlled_production_analysis_result_creation_or_runtime_execution_candidate_set(
        _valid_runtime_boundary_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
        candidate_count=2,
    )

    assert result["production_analysis_result_creation_or_runtime_execution_candidate_set_status"] == (
        "blocked_candidate_boundary_limit_violation"
    )
    assert result["production_analysis_result_creation_or_runtime_execution_candidate_count"] == 0


def test_safe_summary_is_aggregate_only() -> None:
    summary = build_safe_controlled_production_analysis_result_creation_or_runtime_execution_candidate_summary(
        _valid_runtime_boundary_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    assert summary["summary_schema"] == (
        "sentigraph_controlled_production_analysis_result_creation_or_runtime_execution_candidate_summary_v0_1"
    )
    assert summary["production_analysis_result_creation_or_runtime_execution_candidate_count"] == 1
    assert summary["production_analysis_result_created"] is False
    assert summary["production_analysis_result_runtime_used"] is False
    assert summary["analysis_result_generation_executed"] is False
    assert summary["actual_analysis_execution_started"] is False
    assert "production_analysis_result_creation_or_runtime_execution_candidates" not in summary
    _assert_no_forbidden_payload(summary)
