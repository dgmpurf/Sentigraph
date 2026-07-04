from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest

from app.services import controlled_production_analysis_result_creation_go_no_go_boundary as module
from app.services.controlled_production_analysis_result_creation_go_no_go_boundary import (
    APPROVAL_PHRASE,
    GO_NO_GO_BLOCKER_CATEGORIES,
    build_controlled_production_analysis_result_creation_go_no_go_boundary,
    build_safe_controlled_production_analysis_result_creation_go_no_go_boundary_summary,
)


EXPECTED_APPROVAL_PHRASE = (
    "APPROVE_8W_65_CONTROLLED_PRODUCTION_ANALYSIS_RESULT_CREATION_GO_NO_GO_BOUNDARY_HELPER_IMPLEMENTATION"
)

EXPECTED_BLOCKERS = {
    "unresolved_warning_or_manual_review_required",
    "missing_human_review_authority",
    "attempted_automatic_trust_upgrade",
    "production_analysis_result_creation_final_authorization_not_performed",
    "production_analysis_result_creation_go_no_go_authorization_not_performed",
    "production_analysis_result_runtime_not_approved",
    "analysis_result_generation_not_approved",
    "actual_analysis_execution_not_approved",
    "production_analysis_run_not_approved",
    "production_case_not_approved",
    "production_evidence_item_creation_not_approved",
    "review_queue_runtime_not_approved",
    "route_api_frontend_not_approved",
    "b_end_report_runtime_not_approved",
    "sandbox_public_event_runtime_not_approved",
    "export_download_public_final_delivery_runtime_not_approved",
    "real_api_llm_provider_collector_not_approved",
    "private_collector_or_real_exchange_dir_access_forbidden",
    "additional_row_parsing_forbidden",
}

FORBIDDEN_SENTINELS = (
    "actual-raw-comment-should-never-appear",
    "actual-raw-identity-should-never-appear",
    "actual-private-path-should-never-appear",
    "actual-token-should-never-appear",
    "actual-secret-should-never-appear",
    "actual-response-text-should-never-appear",
    "actual-public-message-should-never-appear",
    "target-user-should-never-appear",
    "psych-profile-should-never-appear",
)


def _runtime_side_effects(**overrides: bool) -> dict[str, bool]:
    flags = {name: False for name in module.RUNTIME_SIDE_EFFECT_FLAGS}
    flags.update(overrides)
    return flags


def _source_final_authorization_boundary(**overrides: object) -> dict[str, object]:
    boundary: dict[str, object] = {
        "production_analysis_result_creation_final_authorization_boundary_schema": (
            "sentigraph_controlled_production_analysis_result_creation_final_authorization_boundary_v0_1"
        ),
        "production_analysis_result_creation_final_authorization_boundary_id": (
            "controlled-production-analysis-result-creation-final-authorization-boundary-001"
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
        "case_id_hint": "case-donglu-sunjihai-youth-football",
        "case_title_or_label_redacted": "donglu-sunjihai-youth-football-redacted",
        "input_scope_summary_redacted": "safe-final-authorization-boundary-summary-only",
        "warning_count": 1,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "final_authorization_boundary_only": True,
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
            "final_authorization_boundary_only": True,
            "human_review_required": True,
            "warning_preserving": True,
            "not_production_analysis_result": True,
            "not_production_analysis_result_creation_final_authorization": True,
            "not_production_analysis_result_creation_execution": True,
            "not_production_analysis_result_runtime_use": True,
            "not_analysis_result_generation": True,
            "not_actual_analysis_execution": True,
        },
    }
    boundary.update(overrides)
    return boundary


def _valid_final_authorization_boundary_set(**overrides: object) -> dict[str, object]:
    source: dict[str, object] = {
        "production_analysis_result_creation_final_authorization_boundary_set_schema": (
            "sentigraph_controlled_production_analysis_result_creation_final_authorization_boundary_set_v0_1"
        ),
        "phase": "8W-63",
        "production_analysis_result_creation_final_authorization_boundary_set_status": (
            "production_analysis_result_creation_final_authorization_boundary_set_warn_manual_review_required"
        ),
        "input_source_kind": "controlled_production_analysis_result_creation_execution_boundary",
        "source_production_analysis_result_creation_final_authorization_boundary_schema": (
            "sentigraph_controlled_production_analysis_result_creation_final_authorization_boundary_v0_1"
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
            "backend_only_local_production_analysis_result_creation_final_authorization_boundary"
        ),
        "production_analysis_result_creation_final_authorization_boundary_count": 1,
        "warning_count": 1,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_analysis_result_creation_execution_boundary_created_upstream": True,
        "production_analysis_result_creation_final_authorization_boundary_created": True,
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
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_generated": False,
        "generated_response_text": False,
        "public_route_created": False,
        "download_package_runtime_used": False,
        "public_access_runtime_used": False,
        "external_delivery_runtime_used": False,
        "final_delivery_runtime_used": False,
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
        "runtime_side_effects": _runtime_side_effects(),
        "production_analysis_result_creation_final_authorization_boundaries": [
            _source_final_authorization_boundary()
        ],
        "boundary_flags": {
            "backend_only": True,
            "local_only": True,
            "final_authorization_boundary_only": True,
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
    }
    source.update(overrides)
    return source


def _build_ready(source: dict[str, object] | None = None) -> dict[str, object]:
    return build_controlled_production_analysis_result_creation_go_no_go_boundary(
        source or _valid_final_authorization_boundary_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )


def _assert_no_forbidden_payload(payload: object) -> None:
    encoded = json.dumps(payload, sort_keys=True)
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel not in encoded


def test_approval_phrase_constant_is_exact_ascii() -> None:
    assert APPROVAL_PHRASE == EXPECTED_APPROVAL_PHRASE
    assert APPROVAL_PHRASE.isascii()


def test_ready_source_builds_one_warning_preserving_go_no_go_boundary() -> None:
    result = _build_ready()

    assert result["production_analysis_result_creation_go_no_go_boundary_set_schema"] == (
        "sentigraph_controlled_production_analysis_result_creation_go_no_go_boundary_set_v0_1"
    )
    assert result["production_analysis_result_creation_go_no_go_boundary_set_status"] == (
        "production_analysis_result_creation_go_no_go_boundary_set_warn_manual_review_required"
    )
    assert result["input_source_kind"] == (
        "controlled_production_analysis_result_creation_final_authorization_boundary"
    )
    assert result["production_analysis_result_creation_go_no_go_boundary_count"] == 1
    assert result["warning_count"] == 1
    assert result["human_review_required"] is True
    assert result["no_automatic_trust_upgrade"] is True
    assert result["go_no_go_boundary_created"] is True
    assert result["production_analysis_result_creation_go_no_go_authorization_performed"] is False
    assert result["production_analysis_result_creation_final_authorization_performed"] is False
    assert result["production_analysis_result_created"] is False
    assert result["production_analysis_result_creation_executed"] is False
    assert result["production_analysis_result_runtime_used"] is False
    assert result["analysis_result_generation_executed"] is False
    assert result["analysis_result_created"] is False
    assert result["actual_analysis_execution_started"] is False
    assert result["production_analysis_run_created"] is False
    assert result["production_case_created"] is False
    assert result["production_evidence_item_created"] is False
    assert result["review_queue_item_created"] is False
    assert result["production_review_queue_item_created"] is False
    assert result["review_queue_runtime_used"] is False
    assert result["b_end_report_runtime_generated"] is False
    assert result["sandbox_public_event_generated"] is False
    assert result["generated_response_text"] is False
    assert result["public_route_created"] is False
    assert result["download_package_runtime_used"] is False
    assert result["public_access_runtime_used"] is False
    assert result["external_delivery_runtime_used"] is False
    assert result["final_delivery_runtime_used"] is False
    assert result["runtime_side_effects"] == _runtime_side_effects()
    assert set(GO_NO_GO_BLOCKER_CATEGORIES) == EXPECTED_BLOCKERS
    assert EXPECTED_BLOCKERS.issubset(set(result["go_no_go_blocker_categories"]))

    boundaries = result["production_analysis_result_creation_go_no_go_boundaries"]
    assert len(boundaries) == 1
    boundary = boundaries[0]
    assert boundary["production_analysis_result_creation_go_no_go_boundary_schema"] == (
        "sentigraph_controlled_production_analysis_result_creation_go_no_go_boundary_v0_1"
    )
    assert boundary["go_no_go_boundary_only"] is True
    assert boundary["human_review_required"] is True
    assert boundary["no_automatic_trust_upgrade"] is True
    assert boundary["production_analysis_result_creation_go_no_go_authorization_performed"] is False
    assert boundary["production_analysis_result_creation_final_authorization_performed"] is False
    assert boundary["production_analysis_result_created"] is False
    assert boundary["analysis_result_generation_executed"] is False
    assert boundary["actual_analysis_execution_started"] is False
    assert boundary["boundary_flags"]["not_production_analysis_result"] is True
    assert boundary["boundary_flags"]["not_route_api_frontend"] is True
    _assert_no_forbidden_payload(result)


@pytest.mark.parametrize(
    ("phrase", "expected_status"),
    [
        (None, "blocked_missing_exact_approval"),
        ("", "blocked_missing_exact_approval"),
        (
            "APPROVE_8W_65_CONTROLLED_PRODUCTION_ANALYSIS_RESULT_CREATION_GO_NO_GO_BOUNDARY_HELPER_IMPLEMENTATI0N",
            "blocked_wrong_exact_approval",
        ),
        ("\u6279\u51c6 8W-65 Controlled Production Analysis Result Creation Go-No-Go Boundary Helper Implementation", "blocked_non_ascii_approval"),
        ("\u93b5\u7470\u567f 8W-65 Controlled Production Analysis Result Creation Go-No-Go Boundary Helper Implementation", "blocked_non_ascii_approval"),
    ],
)
def test_exact_approval_required_before_go_no_go_boundary_construction(
    phrase: str | None,
    expected_status: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_open(*args: object, **kwargs: object) -> None:
        raise AssertionError("file access is not allowed")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "open", fail_open)

    result = build_controlled_production_analysis_result_creation_go_no_go_boundary(
        _valid_final_authorization_boundary_set(),
        exact_approval_phrase=phrase,
    )

    assert result["production_analysis_result_creation_go_no_go_boundary_set_status"] == expected_status
    assert result["production_analysis_result_creation_go_no_go_boundary_count"] == 0
    assert result["go_no_go_boundary_created"] is False
    assert result["production_analysis_result_creation_go_no_go_boundaries"] == []


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("production_analysis_result_creation_final_authorization_boundary_set_schema", "wrong"),
        ("source_production_analysis_result_creation_final_authorization_boundary_schema", "wrong"),
        ("production_analysis_result_creation_final_authorization_boundary_set_status", "wrong"),
        ("production_analysis_result_creation_final_authorization_boundary_count", 2),
        ("warning_count", 0),
        ("human_review_required", False),
        ("no_automatic_trust_upgrade", False),
        ("production_analysis_result_creation_final_authorization_boundary_created", False),
        ("production_analysis_result_creation_go_no_go_authorization_performed", True),
        ("production_analysis_result_creation_final_authorization_performed", True),
        ("production_analysis_result_created", True),
        ("production_analysis_result_creation_executed", True),
        ("production_analysis_result_runtime_used", True),
        ("analysis_result_generation_executed", True),
        ("analysis_result_created", True),
        ("actual_analysis_execution_started", True),
        ("production_analysis_run_created", True),
        ("production_case_created", True),
        ("production_evidence_item_created", True),
        ("review_queue_item_created", True),
        ("production_review_queue_item_created", True),
        ("review_queue_runtime_used", True),
        ("route_ready", True),
        ("frontend_ready", True),
        ("b_end_report_runtime_generated", True),
        ("sandbox_public_event_generated", True),
        ("download_package_runtime_used", True),
        ("public_access_runtime_used", True),
        ("external_delivery_runtime_used", True),
        ("final_delivery_runtime_used", True),
        ("private_collector_inspected", True),
        ("real_exchange_dir_read", True),
        ("additional_row_parsing_performed", True),
    ],
)
def test_unsafe_upstream_status_blocks_ready_boundary(field: str, value: object) -> None:
    result = _build_ready(_valid_final_authorization_boundary_set(**{field: value}))

    assert result["production_analysis_result_creation_go_no_go_boundary_set_status"].startswith("blocked_")
    assert result["production_analysis_result_creation_go_no_go_boundary_count"] == 0
    assert result["go_no_go_boundary_created"] is False
    assert result["blockers"]


@pytest.mark.parametrize("flag", module.RUNTIME_SIDE_EFFECT_FLAGS)
def test_runtime_side_effect_flags_true_block(flag: str) -> None:
    result = _build_ready(
        _valid_final_authorization_boundary_set(runtime_side_effects=_runtime_side_effects(**{flag: True}))
    )

    assert result["production_analysis_result_creation_go_no_go_boundary_set_status"] == (
        "blocked_source_boundary_violation"
    )
    assert result["go_no_go_boundary_created"] is False
    assert any(flag in blocker for blocker in result["blockers"])


def test_ready_path_does_not_open_files(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_open(*args: object, **kwargs: object) -> None:
        raise AssertionError("file access is not allowed")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "open", fail_open)

    result = _build_ready()

    assert result["production_analysis_result_creation_go_no_go_boundary_count"] == 1


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("raw_comments", ["actual-raw-comment-should-never-appear"]),
        ("raw_identities", ["actual-raw-identity-should-never-appear"]),
        ("package_path", "C:/actual-private-path-should-never-appear"),
        ("token", "actual-token-should-never-appear"),
        ("secret", "actual-secret-should-never-appear"),
        ("generated_response_text", "actual-response-text-should-never-appear"),
        ("generated_public_message", "actual-public-message-should-never-appear"),
        ("target_user_list", ["target-user-should-never-appear"]),
        ("persuasion_score", 0.8),
        ("truth_score", 0.8),
        ("official_verified", True),
        ("prediction_probability", 0.8),
        ("psychological_profile", "psych-profile-should-never-appear"),
        ("personality_diagnosis", "psych-profile-should-never-appear"),
    ],
)
def test_forbidden_source_fields_block_and_are_not_emitted(field: str, value: object) -> None:
    result = _build_ready(_valid_final_authorization_boundary_set(**{field: value}))

    assert result["production_analysis_result_creation_go_no_go_boundary_set_status"] == (
        "blocked_forbidden_field_detected"
    )
    assert result["production_analysis_result_creation_go_no_go_boundary_count"] == 0
    _assert_no_forbidden_payload(result)


def test_safe_summary_is_aggregate_only() -> None:
    summary = build_safe_controlled_production_analysis_result_creation_go_no_go_boundary_summary(
        _valid_final_authorization_boundary_set(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    assert summary["summary_schema"] == (
        "sentigraph_controlled_production_analysis_result_creation_go_no_go_boundary_summary_v0_1"
    )
    assert summary["production_analysis_result_creation_go_no_go_boundary_count"] == 1
    assert summary["warning_count"] == 1
    assert summary["human_review_required"] is True
    assert summary["no_automatic_trust_upgrade"] is True
    assert summary["production_analysis_result_creation_go_no_go_authorization_performed"] is False
    assert summary["production_analysis_result_creation_final_authorization_performed"] is False
    assert summary["production_analysis_result_created"] is False
    assert summary["analysis_result_generation_executed"] is False
    assert summary["actual_analysis_execution_started"] is False
    assert "production_analysis_result_creation_go_no_go_boundaries" not in summary
    _assert_no_forbidden_payload(summary)
