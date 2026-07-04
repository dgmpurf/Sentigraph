from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest

from app.services import controlled_production_analysis_result_creation_final_authorization_boundary as module
from app.services.controlled_production_analysis_result_creation_final_authorization_boundary import (
    APPROVAL_PHRASE,
    build_controlled_production_analysis_result_creation_final_authorization_boundary_set,
    build_safe_controlled_production_analysis_result_creation_final_authorization_boundary_summary,
)


EXPECTED_APPROVAL_PHRASE = (
    "APPROVE_8W_63_CONTROLLED_PRODUCTION_ANALYSIS_RESULT_CREATION_FINAL_AUTHORIZATION_BOUNDARY_HELPER_IMPLEMENTATION"
)
NON_ASCII_APPROVAL_PHRASE = (
    "\u6279\u51c6 8W-63 Controlled Production Analysis Result Creation Final Authorization Boundary Helper Implementation"
)
MOJIBAKE_APPROVAL_PHRASE = (
    "\u93b5\u7470\u567f 8W-63 Controlled Production Analysis Result Creation Final Authorization Boundary Helper Implementation"
)

EXPECTED_8W62_DECISION = "ready"
EXPECTED_8W62_NEXT = (
    "ready_for_8W_63_controlled_production_analysis_result_creation_final_authorization_boundary_helper_implementation_after_explicit_approval"
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


def _source_execution_boundary(**overrides: object) -> dict[str, object]:
    boundary: dict[str, object] = {
        "production_analysis_result_creation_execution_boundary_schema": (
            "sentigraph_controlled_production_analysis_result_creation_execution_boundary_v0_1"
        ),
        "production_analysis_result_creation_execution_boundary_id": (
            "controlled-production-analysis-result-creation-execution-boundary-001-hash-001"
        ),
        "source_production_analysis_result_creation_runtime_boundary_count": 1,
        "source_production_analysis_result_creation_candidate_count": 1,
        "source_production_analysis_result_creation_boundary_count": 1,
        "source_production_analysis_result_creation_or_runtime_execution_candidate_count": 1,
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
        "input_scope_summary_redacted": (
            "controlled_local_production_analysis_result_creation_execution_boundary_summary_only"
        ),
        "intended_creation_execution_boundary_labels": [
            "creation_execution_boundary_only",
            "selected_sample_only",
            "human_review_required",
            "no_automatic_trust_upgrade",
        ],
        "intended_module_scope_labels": [
            "production_analysis_result_creation_execution_boundary",
            "no_production_analysis_result",
            "no_production_analysis_result_creation_final_authorization",
            "no_production_analysis_result_runtime_use",
            "no_analysis_result_generation",
        ],
        "creation_execution_gate_labels": [
            "execution_boundary_gate_only",
            "manual_review_required",
            "not_final_authorization",
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
        "production_analysis_result_creation_final_authorization_readiness_blockers": [
            "production_analysis_result_creation_final_authorization_not_approved",
            "human_review_required",
        ],
        "production_analysis_result_creation_readiness_blockers": [
            "production_analysis_result_creation_not_approved",
            "human_review_required",
        ],
        "production_analysis_result_creation_execution_readiness_blockers": [
            "production_analysis_result_creation_execution_not_approved",
            "human_review_required",
        ],
        "production_analysis_result_runtime_readiness_blockers": [
            "production_analysis_result_runtime_not_approved",
            "human_review_required",
        ],
        "analysis_result_generation_readiness_blockers": [
            "analysis_result_generation_not_approved",
            "human_review_required",
        ],
        "actual_analysis_execution_readiness_blockers": [
            "actual_analysis_execution_not_approved",
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
        "creation_execution_boundary_only": True,
        "no_automatic_trust_upgrade": True,
        "production_analysis_result_creation_final_authorization_performed": False,
        "production_analysis_result_created": False,
        "production_analysis_result_creation_executed": False,
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
            "creation_execution_boundary_only": True,
            "human_review_required": True,
            "warning_preserving": True,
            "not_production_analysis_result": True,
            "not_production_analysis_result_creation_final_authorization": True,
            "not_production_analysis_result_creation_execution": True,
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


def _valid_execution_boundary_set(**overrides: object) -> dict[str, object]:
    source: dict[str, object] = {
        "production_analysis_result_creation_execution_boundary_set_schema": (
            "sentigraph_controlled_production_analysis_result_creation_execution_boundary_set_v0_1"
        ),
        "phase": "8W-61",
        "production_analysis_result_creation_execution_boundary_set_status": (
            "production_analysis_result_creation_execution_boundary_set_warn_manual_review_required"
        ),
        "input_source_kind": "controlled_production_analysis_result_creation_runtime_boundary",
        "source_production_analysis_result_creation_execution_boundary_schema": (
            "sentigraph_controlled_production_analysis_result_creation_execution_boundary_v0_1"
        ),
        "source_production_analysis_result_creation_execution_boundary_count": 1,
        "source_production_analysis_result_creation_runtime_boundary_count": 1,
        "source_production_analysis_result_creation_candidate_count": 1,
        "source_production_analysis_result_creation_boundary_count": 1,
        "source_production_analysis_result_creation_or_runtime_execution_candidate_count": 1,
        "source_production_analysis_result_runtime_boundary_count": 1,
        "source_production_analysis_result_boundary_count": 1,
        "source_production_analysis_result_candidate_count": 1,
        "source_analysis_result_candidate_count": 1,
        "source_actual_analysis_execution_candidate_count": 1,
        "source_production_analysis_run_candidate_count": 1,
        "source_production_case_candidate_count": 1,
        "source_controlled_evidence_item_count": 5,
        "final_authorization_boundary_mode": (
            "backend_only_local_production_analysis_result_creation_execution_boundary"
        ),
        "production_analysis_result_creation_execution_boundary_count": 1,
        "warning_count": 1,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_analysis_result_creation_runtime_boundary_created_upstream": True,
        "production_analysis_result_creation_runtime_boundary_created": True,
        "production_analysis_result_creation_execution_boundary_created": True,
        "production_analysis_result_creation_final_authorization_performed": False,
        "production_analysis_result_created": False,
        "production_analysis_result_creation_executed": False,
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
        "runtime_side_effects": _runtime_side_effects(),
        "production_analysis_result_creation_execution_boundaries": [_source_execution_boundary()],
        "boundary_flags": {
            "backend_only": True,
            "local_only": True,
            "creation_execution_boundary_only": True,
            "human_review_required": True,
            "warning_preserving": True,
            "not_production_analysis_result": True,
            "not_production_analysis_result_creation_final_authorization": True,
            "not_production_analysis_result_creation_execution": True,
            "not_production_analysis_result_runtime_use": True,
            "not_analysis_result_generation": True,
        },
        "warnings": ["manual_review_required", "selected_sample_only"],
        "blockers": [],
        "audit_summary": {
            "analysis_effect": "none",
            "production_analysis_result_effect": "none",
            "production_analysis_result_creation_final_authorization_effect": "none",
            "production_analysis_result_creation_effect": "none",
            "production_analysis_result_creation_execution_effect": "none",
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
    return build_controlled_production_analysis_result_creation_final_authorization_boundary_set(
        source or _valid_execution_boundary_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
        decision_8w62=EXPECTED_8W62_DECISION,
        selected_next_boundary_option_8w62=EXPECTED_8W62_NEXT,
    )


def test_approval_phrase_constant_is_exact_ascii() -> None:
    assert APPROVAL_PHRASE == EXPECTED_APPROVAL_PHRASE
    assert APPROVAL_PHRASE.isascii()


def test_ready_path_builds_one_warning_preserving_final_authorization_boundary() -> None:
    result = _build_ready()

    assert result["production_analysis_result_creation_final_authorization_boundary_set_schema"] == (
        "sentigraph_controlled_production_analysis_result_creation_final_authorization_boundary_set_v0_1"
    )
    assert result["production_analysis_result_creation_final_authorization_boundary_set_status"] == (
        "production_analysis_result_creation_final_authorization_boundary_set_warn_manual_review_required"
    )
    assert result["input_source_kind"] == "controlled_production_analysis_result_creation_execution_boundary"
    assert result["final_authorization_boundary_mode"] == (
        "backend_only_local_production_analysis_result_creation_final_authorization_boundary"
    )
    assert result["production_analysis_result_creation_final_authorization_boundary_count"] == 1
    assert result["source_production_analysis_result_creation_execution_boundary_set_schema"] == (
        "sentigraph_controlled_production_analysis_result_creation_execution_boundary_set_v0_1"
    )
    assert result["source_production_analysis_result_creation_execution_boundary_schema"] == (
        "sentigraph_controlled_production_analysis_result_creation_execution_boundary_v0_1"
    )
    assert result["source_production_analysis_result_creation_execution_boundary_count"] == 1
    assert result["source_production_analysis_result_creation_runtime_boundary_count"] == 1
    assert result["source_production_analysis_result_creation_candidate_count"] == 1
    assert result["source_production_analysis_result_creation_boundary_count"] == 1
    assert result["source_production_analysis_result_creation_or_runtime_execution_candidate_count"] == 1
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
    assert result["production_analysis_result_creation_execution_boundary_created_upstream"] is True
    assert result["production_analysis_result_creation_final_authorization_boundary_created"] is True
    assert result["production_analysis_result_creation_final_authorization_performed"] is False
    assert result["production_analysis_result_created"] is False
    assert result["production_analysis_result_creation_executed"] is False
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

    boundaries = result["production_analysis_result_creation_final_authorization_boundaries"]
    assert len(boundaries) == 1
    boundary = boundaries[0]
    assert boundary["production_analysis_result_creation_final_authorization_boundary_schema"] == (
        "sentigraph_controlled_production_analysis_result_creation_final_authorization_boundary_v0_1"
    )
    assert boundary["final_authorization_boundary_only"] is True
    assert boundary["human_review_required"] is True
    assert boundary["production_analysis_result_creation_final_authorization_performed"] is False
    assert boundary["production_analysis_result_created"] is False
    assert boundary["production_analysis_result_creation_executed"] is False
    assert boundary["production_analysis_result_runtime_used"] is False
    assert boundary["analysis_result_generation_executed"] is False
    assert boundary["actual_analysis_execution_started"] is False
    assert boundary["review_queue_runtime_used"] is False
    assert boundary["boundary_flags"]["not_production_analysis_result"] is True
    assert boundary["boundary_flags"]["not_production_analysis_result_creation_final_authorization"] is True
    assert boundary["boundary_flags"]["not_production_analysis_result_runtime_use"] is True
    _assert_no_forbidden_payload(result)


def test_safe_summary_without_execution_boundary_list_builds_one_final_authorization_boundary() -> None:
    source = _valid_execution_boundary_set()
    source.pop("production_analysis_result_creation_execution_boundaries")

    result = _build_ready(source)

    assert result["production_analysis_result_creation_final_authorization_boundary_set_status"] == (
        "production_analysis_result_creation_final_authorization_boundary_set_warn_manual_review_required"
    )
    assert result["production_analysis_result_creation_final_authorization_boundary_count"] == 1
    assert result["production_analysis_result_creation_final_authorization_boundary_created"] is True
    assert result["production_analysis_result_creation_final_authorization_boundaries"][0][
        "source_production_analysis_result_creation_execution_boundary_count"
    ] == 1
    _assert_no_forbidden_payload(result)


@pytest.mark.parametrize(
    ("phrase", "expected_status"),
    [
        (None, "blocked_missing_exact_approval"),
        ("", "blocked_missing_exact_approval"),
        (
            "APPROVE_8W_63_CONTROLLED_PRODUCTION_ANALYSIS_RESULT_CREATION_FINAL_AUTHORIZATION_BOUNDARY_HELPER_IMPLEMENTATI0N",
            "blocked_wrong_exact_approval",
        ),
        (NON_ASCII_APPROVAL_PHRASE, "blocked_non_ascii_approval"),
        (MOJIBAKE_APPROVAL_PHRASE, "blocked_non_ascii_approval"),
    ],
)
def test_exact_approval_phrase_required_before_final_authorization_boundary_construction(
    phrase: str | None,
    expected_status: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_open(*args: object, **kwargs: object) -> None:
        raise AssertionError("file access is not allowed")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "open", fail_open)

    result = build_controlled_production_analysis_result_creation_final_authorization_boundary_set(
        _valid_execution_boundary_set(),
        exact_approval_phrase=phrase,
        decision_8w62=EXPECTED_8W62_DECISION,
        selected_next_boundary_option_8w62=EXPECTED_8W62_NEXT,
    )

    assert result["production_analysis_result_creation_final_authorization_boundary_set_status"] == expected_status
    assert result["production_analysis_result_creation_final_authorization_boundary_count"] == 0
    assert result["production_analysis_result_creation_final_authorization_boundary_created"] is False
    assert result["production_analysis_result_creation_final_authorization_boundaries"] == []


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("production_analysis_result_creation_execution_boundary_set_schema", "wrong"),
        ("source_production_analysis_result_creation_execution_boundary_schema", "wrong"),
        ("production_analysis_result_creation_execution_boundary_set_status", "wrong"),
        ("source_production_analysis_result_creation_execution_boundary_count", 2),
        ("production_analysis_result_creation_execution_boundary_count", 2),
        ("source_production_analysis_result_creation_runtime_boundary_count", 2),
        ("source_production_analysis_result_creation_candidate_count", 2),
        ("source_production_analysis_result_creation_boundary_count", 2),
        ("source_production_analysis_result_creation_or_runtime_execution_candidate_count", 2),
        ("source_production_analysis_result_runtime_boundary_count", 2),
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
        ("production_analysis_result_creation_execution_boundary_created", False),
        ("production_analysis_result_creation_runtime_boundary_created", False),
        ("production_analysis_result_creation_final_authorization_performed", True),
        ("production_analysis_result_created", True),
        ("production_analysis_result_creation_executed", True),
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
def test_source_execution_boundary_validation_blocks_unsafe_inputs(field: str, value: object) -> None:
    result = _build_ready(_valid_execution_boundary_set(**{field: value}))

    assert result["production_analysis_result_creation_final_authorization_boundary_set_status"] != (
        "production_analysis_result_creation_final_authorization_boundary_set_warn_manual_review_required"
    )
    assert result["production_analysis_result_creation_final_authorization_boundary_count"] == 0
    assert result["production_analysis_result_creation_final_authorization_boundary_created"] is False
    assert result["blockers"]


@pytest.mark.parametrize(
    ("decision", "selected_next"),
    [
        (None, EXPECTED_8W62_NEXT),
        ("needs_fix", EXPECTED_8W62_NEXT),
        (EXPECTED_8W62_DECISION, None),
        (EXPECTED_8W62_DECISION, "pause"),
    ],
)
def test_missing_or_wrong_8w62_gate_status_blocks(decision: str | None, selected_next: str | None) -> None:
    result = build_controlled_production_analysis_result_creation_final_authorization_boundary_set(
        _valid_execution_boundary_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
        decision_8w62=decision,
        selected_next_boundary_option_8w62=selected_next,
    )

    assert result["production_analysis_result_creation_final_authorization_boundary_set_status"] == (
        "blocked_invalid_source_production_analysis_result_creation_execution_boundary"
    )
    assert result["production_analysis_result_creation_final_authorization_boundary_count"] == 0


@pytest.mark.parametrize("flag", module.RUNTIME_SIDE_EFFECT_FLAGS)
def test_runtime_side_effect_flags_true_block(flag: str) -> None:
    result = _build_ready(_valid_execution_boundary_set(runtime_side_effects=_runtime_side_effects(**{flag: True})))

    assert result["production_analysis_result_creation_final_authorization_boundary_set_status"] == (
        "blocked_source_boundary_violation"
    )
    assert result["production_analysis_result_creation_final_authorization_boundary_created"] is False
    assert any(flag in blocker for blocker in result["blockers"])


@pytest.mark.parametrize(
    "requested_action",
    [
        "production_analysis_result_creation_final_authorization",
        "production_analysis_result",
        "production_analysis_result_creation",
        "production_analysis_result_creation_execution",
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
        "row_parsing",
    ],
)
def test_requested_side_effect_actions_block(requested_action: str) -> None:
    result = build_controlled_production_analysis_result_creation_final_authorization_boundary_set(
        _valid_execution_boundary_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
        decision_8w62=EXPECTED_8W62_DECISION,
        selected_next_boundary_option_8w62=EXPECTED_8W62_NEXT,
        requested_actions=[requested_action],
    )

    assert result["production_analysis_result_creation_final_authorization_boundary_set_status"].startswith(
        "blocked_"
    )
    assert result["production_analysis_result_creation_final_authorization_boundary_count"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("raw_author_id", "actual-raw-author-should-never-appear"),
        ("author_id", "actual-raw-author-should-never-appear"),
        ("author_name", "actual-author-name-should-never-appear"),
        ("username", "actual-username-should-never-appear"),
        ("display_name", "actual-display-name-should-never-appear"),
        ("profile_url", "actual-profile-url-should-never-appear"),
        ("raw_comments", ["actual-raw-comment-should-never-appear"]),
        ("token", "actual-token-should-never-appear"),
        ("cookie", "actual-cookie-should-never-appear"),
        ("api_key", "actual-api-key-should-never-appear"),
        ("secret", "actual-secret-should-never-appear"),
        ("salt", "actual-salt-should-never-appear"),
        ("absolute_path", "G:/private-collector/should-never-appear"),
        ("package_path", "C:/Users/msjpurf/private-collector/should-never-appear"),
        ("production_analysis_result_id", "production-analysis-result-id-should-never-appear"),
        ("analysis_result_id", "analysis-result-id-should-never-appear"),
        ("actual_analysis_execution_id", "actual-analysis-execution-id-should-never-appear"),
        ("analysis_execution_id", "analysis-execution-id-should-never-appear"),
        ("production_analysis_run_id", "production-analysis-run-id-should-never-appear"),
        ("analysis_run_id", "production-analysis-run-id-should-never-appear"),
        ("production_case_id", "production-case-id-should-never-appear"),
        ("production_evidence_item_id", "production-evidence-item-id-should-never-appear"),
        ("review_queue_item_id", "review-queue-item-id-should-never-appear"),
        ("production_review_queue_item_id", "review-queue-item-id-should-never-appear"),
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
    source = _valid_execution_boundary_set(**{field: value})

    result = _build_ready(source)

    assert result["production_analysis_result_creation_final_authorization_boundary_set_status"] == (
        "blocked_forbidden_field_detected"
    )
    assert result["production_analysis_result_creation_final_authorization_boundary_count"] == 0
    _assert_no_forbidden_payload(result)


def test_ready_path_does_not_open_files(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_open(*args: object, **kwargs: object) -> None:
        raise AssertionError("file access is not allowed")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "open", fail_open)

    result = _build_ready()

    assert result["production_analysis_result_creation_final_authorization_boundary_count"] == 1
    assert result["production_analysis_result_creation_final_authorization_boundary_created"] is True


def test_missing_source_creation_execution_boundary_blocks() -> None:
    result = _build_ready(_valid_execution_boundary_set(production_analysis_result_creation_execution_boundaries=[]))

    assert result["production_analysis_result_creation_final_authorization_boundary_set_status"] == (
        "blocked_invalid_source_production_analysis_result_creation_execution_boundary"
    )
    assert result["production_analysis_result_creation_final_authorization_boundary_count"] == 0


def test_multiple_final_authorization_boundary_request_blocks() -> None:
    result = build_controlled_production_analysis_result_creation_final_authorization_boundary_set(
        _valid_execution_boundary_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
        decision_8w62=EXPECTED_8W62_DECISION,
        selected_next_boundary_option_8w62=EXPECTED_8W62_NEXT,
        final_authorization_boundary_count=2,
    )

    assert result["production_analysis_result_creation_final_authorization_boundary_set_status"] == (
        "blocked_final_authorization_boundary_limit_violation"
    )
    assert result["production_analysis_result_creation_final_authorization_boundary_count"] == 0


def test_safe_summary_is_aggregate_only() -> None:
    summary = build_safe_controlled_production_analysis_result_creation_final_authorization_boundary_summary(
        _valid_execution_boundary_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
        decision_8w62=EXPECTED_8W62_DECISION,
        selected_next_boundary_option_8w62=EXPECTED_8W62_NEXT,
    )

    assert summary["summary_schema"] == (
        "sentigraph_controlled_production_analysis_result_creation_final_authorization_boundary_summary_v0_1"
    )
    assert summary["production_analysis_result_creation_final_authorization_boundary_count"] == 1
    assert summary["production_analysis_result_creation_final_authorization_performed"] is False
    assert summary["production_analysis_result_created"] is False
    assert summary["production_analysis_result_creation_executed"] is False
    assert summary["production_analysis_result_runtime_used"] is False
    assert summary["analysis_result_generation_executed"] is False
    assert summary["actual_analysis_execution_started"] is False
    assert "production_analysis_result_creation_final_authorization_boundaries" not in summary
    _assert_no_forbidden_payload(summary)
