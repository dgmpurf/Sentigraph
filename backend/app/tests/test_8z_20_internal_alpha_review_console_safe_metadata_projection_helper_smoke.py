from __future__ import annotations

import builtins
import inspect
import json
from pathlib import Path
from typing import Any

import pytest

import app.services.internal_alpha_review_console_safe_metadata_projection as projection_module
from app.services.internal_alpha_review_console_safe_metadata_projection import (
    APPROVAL_PHRASE,
    build_internal_alpha_review_console_safe_metadata_projection,
    build_safe_internal_alpha_review_console_projection_summary,
)


EXPECTED_APPROVAL_PHRASE = "APPROVE_8Z_20_INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_METADATA_PROJECTION_HELPER_SMOKE"
OLD_8Z19_PHRASE = "APPROVE_8Z_19_INTERNAL_ALPHA_REVIEW_CONSOLE_IMPLEMENTATION_READINESS_DECISION_DOCS_ONLY"
OLD_8Z18_PHRASE = "APPROVE_8Z_18_INTERNAL_ALPHA_REVIEW_CONSOLE_SAFETY_CONTRACT_TESTS_ONLY"
OLD_8Z17_PHRASE = "APPROVE_8Z_17_INTERNAL_ALPHA_REVIEW_CONSOLE_AND_OPERATOR_WORKFLOW_PLANNING_DOCS_ONLY"
OLD_8Y_PHRASE = "APPROVE_8Y_20_CONTROLLED_ANALYSIS_RUN_CANDIDATE_TO_ANALYSIS_RESULT_BOUNDARY_SMOKE"
OLD_8W_PHRASE = "APPROVE_8W_19_CONTROLLED_EVIDENCE_LAYER_WRITE_CANDIDATE_IMPLEMENTATION"

FORBIDDEN_SENTINELS = (
    "actual-token-should-never-appear",
    "actual-cookie-should-never-appear",
    "actual-api-key-should-never-appear",
    "actual-raw-author-should-never-appear",
    "actual-author-name-should-never-appear",
    "actual-profile-url-should-never-appear",
    "actual-raw-comment-should-never-appear",
    "actual-private-message-should-never-appear",
    "G:/private-collector/should-never-appear",
    "C:/Users/msjpurf/private-collector/should-never-appear",
    "https://example.invalid/profile/should-never-appear",
)

FALSE_SOURCE_FLAGS = {
    "actual_evidence_layer_write_used": "source_actual_evidence_layer_write_used_true",
    "evidence_layer_write": "source_evidence_layer_write_true",
    "persisted_evidence_layer_record_created": "source_persisted_evidence_layer_record_created_true",
    "production_evidence_item_created": "source_production_evidence_item_created_true",
    "review_queue_runtime_used": "source_review_queue_runtime_used_true",
    "production_review_queue_item_created": "source_production_review_queue_item_created_true",
    "production_case_created": "source_production_case_created_true",
    "production_analysis_run_created": "source_production_analysis_run_created_true",
    "actual_analysis_execution_started": "source_actual_analysis_execution_started_true",
    "production_analysis_result_authorized": "source_production_analysis_result_authorized_true",
    "production_analysis_result_created": "source_production_analysis_result_created_true",
    "source11_runtime_called": "source_source11_runtime_called_true",
    "finalsummaryreport_runtime_called": "source_finalsummaryreport_runtime_called_true",
    "public_delivery_created": "source_public_delivery_created_true",
    "export_download_public_delivery_created": "source_export_download_public_delivery_created_true",
    "collector_job_run": "source_collector_job_run_true",
    "provider_job_run": "source_provider_job_run_true",
    "real_exchange_dir_read": "source_real_exchange_dir_read_true",
    "real_package_dir_read": "source_real_package_dir_read_true",
    "production_package_rows_parsed": "source_production_package_rows_parsed_true",
    "raw_rows_exposed": "source_raw_rows_exposed_true",
    "raw_comments_exposed": "source_raw_comments_exposed_true",
    "raw_identities_exposed": "source_raw_identities_exposed_true",
    "secrets_read": "source_secrets_read_true",
    "route_changed": "source_route_changed_true",
    "api_route_added": "source_api_route_added_true",
    "frontend_changed": "source_frontend_changed_true",
    "runtime_changed": "source_runtime_changed_true",
}

READINESS_TRUE_FLAGS = {
    "route_ready": "source_route_ready_true",
    "frontend_ready": "source_frontend_ready_true",
    "runtime_ready": "source_runtime_ready_true",
    "public_ready": "source_public_ready_true",
    "production_ready": "source_production_ready_true",
    "actual_write_enabled": "source_actual_write_enabled_true",
    "production_object_enabled": "source_production_object_enabled_true",
    "review_queue_runtime_enabled": "source_review_queue_runtime_enabled_true",
    "source11_runtime_enabled": "source_source11_runtime_enabled_true",
    "finalsummaryreport_runtime_enabled": "source_finalsummaryreport_runtime_enabled_true",
}

DISALLOWED_SERVICE_IMPORTS = (
    "app.services.controlled_row_preview",
    "app.services.controlled_evidence_candidate",
    "app.services.controlled_review_queue_candidate",
    "app.services.controlled_evidence_layer_import_candidate",
    "app.services.controlled_evidence_layer_write_candidate",
    "app.services.controlled_evidenceitem_evidence_layer_write_runtime",
    "app.services.evidence_import",
    "app.services.evidence_ingestion",
    "app.services.private_collector_package_resolver",
    "app.services.private_collector_provider_result_reader",
    "app.services.local_exchange_reader",
    "app.services.private_collector_review_only_staging",
)


def _safe_source(**overrides: object) -> dict[str, object]:
    source: dict[str, object] = {
        "source_summary_schema": "sentigraph_internal_alpha_no_write_governance_chain_summary_v0_1",
        "request_id": "req_8z20_safe_fixture",
        "provider_result_id": "provider_result_8z20_safe_fixture",
        "package_reference": "opaque_package_ref_8z20_safe_fixture",
        "stage_id": "stage_8z16_safe_fixture",
        "stage_schema": "sentigraph_internal_alpha_stage_summary_v0_1",
        "stage_status": "warn_manual_review_required",
        "stage_mode": "backend_only_local_no_write_governance_chain",
        "candidate_id": "evidence_layer_write_candidate_boundary_8z20_fixture",
        "boundary_id": "boundary_8z20_evidence_layer_write_candidate",
        "source_chain_boundary": "evidence_layer_write_candidate_boundary",
        "evidence_count": 3,
        "source_count": 2,
        "warning_count": 1,
        "blocker_count": 0,
        "coverage_note_summary": "selected public sample only; not full-web coverage",
        "validation_summary": "local backend-only governance chain summary",
        "safety_flags": {
            "safe_metadata_only": True,
            "raw_identity_exposed": False,
            "secrets_read": False,
        },
        "boundary_flags": {
            "selected_sample_only": True,
            "not_full_web": True,
            "not_full_platform": True,
            "not_official_verification": True,
            "not_causal_proof": True,
            "no_actual_write": True,
        },
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "audit_refs": ["audit_ref_8z20_safe_fixture"],
        "health_report_refs": ["health_report_8z16_safe_fixture"],
        "allowed_actions": [
            "keep_paused",
            "needs_more_review",
            "blocked_privacy_or_raw_identity_risk",
            "blocked_missing_authority",
            "candidate_ready_for_future_docs_only_write_gate_discussion",
        ],
        "blocked_actions": [
            "actual_write_blocked",
            "route_api_blocked",
            "frontend_blocked",
            "runtime_blocked",
        ],
        "next_gate_inactive_phrase_labels": [
            "inactive_future_docs_only_write_gate_discussion_phrase_required",
        ],
    }
    source.update({flag: False for flag in FALSE_SOURCE_FLAGS})
    source.update({flag: False for flag in READINESS_TRUE_FLAGS})
    source.update(overrides)
    return source


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _assert_no_forbidden_sentinels(value: object) -> None:
    serialized = _serialized(value)
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel not in serialized
    assert ":/" not in serialized
    assert ":\\" not in serialized


def _assert_projection_safe_flags(projection: dict[str, object]) -> None:
    false_fields = [
        "route_ready",
        "frontend_ready",
        "runtime_ready",
        "public_ready",
        "production_ready",
        "actual_write_enabled",
        "production_object_enabled",
        "review_queue_runtime_enabled",
        "source11_runtime_enabled",
        "finalsummaryreport_runtime_enabled",
        "actual_evidence_layer_write",
        "persisted_evidence_layer_record_created",
        "production_evidence_item_created",
        "review_queue_runtime_used",
        "production_review_queue_item_created",
        "production_case_created",
        "production_analysis_run_created",
        "actual_analysis_execution_started",
        "production_analysis_result_authorized",
        "production_analysis_result_created",
        "source11_runtime_called",
        "finalsummaryreport_runtime_called",
        "public_delivery_created",
        "collector_provider_jobs",
        "real_exchange_package_dirs_read",
        "production_package_rows_parsed",
        "raw_rows_comments_identities_exposed",
        "secrets_read",
    ]
    for field in false_fields:
        assert projection[field] is False, field
    runtime_side_effects = projection["runtime_side_effects"]
    assert isinstance(runtime_side_effects, dict)
    for flag, value in runtime_side_effects.items():
        assert value is False, flag


def _assert_blocked(projection: dict[str, object], expected_blocker: str) -> None:
    assert str(projection["projection_status"]).startswith("blocked_")
    assert projection["projection_created"] is False
    assert expected_blocker in projection["blockers"]
    _assert_projection_safe_flags(projection)
    _assert_no_forbidden_sentinels(projection)


def test_positive_smoke_builds_safe_metadata_projection_without_side_effects() -> None:
    assert APPROVAL_PHRASE == EXPECTED_APPROVAL_PHRASE

    projection = build_internal_alpha_review_console_safe_metadata_projection(
        _safe_source(),
        exact_approval_phrase=EXPECTED_APPROVAL_PHRASE,
    )

    assert projection["projection_schema"] == "sentigraph_internal_alpha_review_console_safe_metadata_projection_v0_1"
    assert projection["phase"] == "8Z-20"
    assert projection["projection_status"] == "safe_metadata_projection_ready_for_internal_alpha_review"
    assert projection["projection_created"] is True
    assert projection["projection_mode"] == "backend_only_local_safe_metadata_projection"
    assert projection["source_chain_boundary"] == "evidence_layer_write_candidate_boundary"
    assert projection["safe_metadata_only"] is True
    assert projection["label_only_operator_outcomes"] is True
    assert projection["warning_count"] == 1
    assert projection["blocker_count"] == 0
    assert projection["human_review_required"] is True
    assert projection["no_automatic_trust_upgrade"] is True
    assert projection["request_id"] == "req_8z20_safe_fixture"
    assert projection["provider_result_id"] == "provider_result_8z20_safe_fixture"
    assert projection["package_reference"] == "opaque_package_ref_8z20_safe_fixture"
    assert projection["allowed_actions"] == [
        "keep_paused",
        "needs_more_review",
        "blocked_privacy_or_raw_identity_risk",
        "blocked_missing_authority",
        "candidate_ready_for_future_docs_only_write_gate_discussion",
    ]
    _assert_projection_safe_flags(projection)
    _assert_no_forbidden_sentinels(projection)


@pytest.mark.parametrize(
    "phrase",
    [
        None,
        "",
        "wrong approval",
        OLD_8Z19_PHRASE,
        OLD_8Z18_PHRASE,
        OLD_8Z17_PHRASE,
        OLD_8Y_PHRASE,
        OLD_8W_PHRASE,
    ],
)
def test_exact_8z20_phrase_is_required_before_projection_creation_and_file_access(
    phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def blocked_file_access(*args: object, **kwargs: object) -> None:
        raise AssertionError("8Z-20 projection helper must not open files")

    monkeypatch.setattr(builtins, "open", blocked_file_access)
    monkeypatch.setattr(Path, "open", blocked_file_access)
    monkeypatch.setattr(Path, "read_text", blocked_file_access)
    monkeypatch.setattr(Path, "read_bytes", blocked_file_access)

    projection = build_internal_alpha_review_console_safe_metadata_projection(
        _safe_source(),
        exact_approval_phrase=phrase,
    )

    expected_blocker = "blocked_missing_exact_8z20_approval" if phrase in {None, ""} else "blocked_wrong_exact_8z20_approval"
    _assert_blocked(projection, expected_blocker)


@pytest.mark.parametrize(
    ("field", "value", "expected_blocker"),
    [
        ("source_summary_schema", "wrong", "source_schema_wrong"),
        ("source_chain_boundary", "wrong_boundary", "source_chain_boundary_wrong"),
        ("human_review_required", False, "source_human_review_required_not_true"),
        ("no_automatic_trust_upgrade", False, "source_no_automatic_trust_upgrade_not_true"),
        ("request_id", "", "source_required_safe_id_missing:request_id"),
        ("provider_result_id", "", "source_required_safe_id_missing:provider_result_id"),
        ("stage_id", "", "source_required_safe_id_missing:stage_id"),
        ("candidate_id", "", "source_required_safe_id_missing:candidate_id"),
        ("boundary_id", "", "source_required_safe_id_missing:boundary_id"),
        ("package_reference", "G:/private-collector/should-never-appear", "source_package_reference_path_like"),
        ("coverage_note_summary", "https://example.invalid/profile/should-never-appear", "source_forbidden_value:coverage_note_summary"),
    ],
)
def test_source_schema_boundary_review_and_safe_id_requirements_block(
    field: str,
    value: object,
    expected_blocker: str,
) -> None:
    projection = build_internal_alpha_review_console_safe_metadata_projection(
        _safe_source(**{field: value}),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(projection, expected_blocker)


@pytest.mark.parametrize(("flag", "expected_blocker"), [*FALSE_SOURCE_FLAGS.items(), *READINESS_TRUE_FLAGS.items()])
def test_false_source_side_effect_or_readiness_flags_true_block(flag: str, expected_blocker: str) -> None:
    projection = build_internal_alpha_review_console_safe_metadata_projection(
        _safe_source(**{flag: True}),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(projection, expected_blocker)


@pytest.mark.parametrize(
    ("field", "value", "expected_blocker"),
    [
        ("raw_author_id", "actual-raw-author-should-never-appear", "source_forbidden_field:raw_author_id"),
        ("raw_author_name", "actual-author-name-should-never-appear", "source_forbidden_field:raw_author_name"),
        ("profile_url", "https://example.invalid/profile/should-never-appear", "source_forbidden_field:profile_url"),
        ("raw_comments", ["actual-raw-comment-should-never-appear"], "source_forbidden_field:raw_comments"),
        ("private_message", "actual-private-message-should-never-appear", "source_forbidden_field:private_message"),
        ("token", "actual-token-should-never-appear", "source_forbidden_field:token"),
        ("api_key", "actual-api-key-should-never-appear", "source_forbidden_field:api_key"),
        ("evidence_items_jsonl_contents", "raw row body", "source_forbidden_field:evidence_items_jsonl_contents"),
        ("target_user_list", ["audience"], "source_forbidden_field:target_user_list"),
        ("persuasion_score", 0.7, "source_forbidden_field:persuasion_score"),
    ],
)
def test_raw_or_forbidden_fields_block_without_echoing_values(field: str, value: object, expected_blocker: str) -> None:
    projection = build_internal_alpha_review_console_safe_metadata_projection(
        _safe_source(**{field: value}),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(projection, expected_blocker)


@pytest.mark.parametrize(
    "action",
    [
        "approve actual Evidence Layer write",
        "perform actual Evidence Layer write",
        "create production EvidenceItem",
        "use Review Queue runtime",
        "create production case",
        "start actual analysis execution",
        "authorize production Analysis Result",
        "call Source 11 runtime",
        "run collector/provider job",
        "read real exchange/package dir",
        "publish/send/post/execute platform action",
    ],
)
def test_forbidden_active_actions_block(action: str) -> None:
    projection = build_internal_alpha_review_console_safe_metadata_projection(
        _safe_source(allowed_actions=["keep_paused", action]),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(projection, f"source_forbidden_active_action:{action}")


def test_helper_never_imports_or_calls_disallowed_chain_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    source_text = inspect.getsource(projection_module)
    for module_name in DISALLOWED_SERVICE_IMPORTS:
        assert module_name not in source_text
        assert module_name.rsplit(".", 1)[-1] not in source_text

    original_import = builtins.__import__

    def blocked_import(name: str, *args: object, **kwargs: object) -> object:
        if name in DISALLOWED_SERVICE_IMPORTS:
            raise AssertionError(f"8Z-20 must not import {name}")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)

    projection = build_internal_alpha_review_console_safe_metadata_projection(
        _safe_source(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    assert projection["projection_created"] is True


def test_helper_never_uses_file_network_or_subprocess_primitives(monkeypatch: pytest.MonkeyPatch) -> None:
    source_text = inspect.getsource(projection_module)
    forbidden_source_terms = [
        "import requests",
        "import httpx",
        "import socket",
        "import subprocess",
        "import urllib",
        "Path(",
        "open(",
        "read_text",
        "read_bytes",
    ]
    for term in forbidden_source_terms:
        assert term not in source_text

    def blocked_file_access(*args: object, **kwargs: object) -> None:
        raise AssertionError("8Z-20 projection helper must not use file IO")

    monkeypatch.setattr(builtins, "open", blocked_file_access)
    monkeypatch.setattr(Path, "open", blocked_file_access)
    monkeypatch.setattr(Path, "read_text", blocked_file_access)
    monkeypatch.setattr(Path, "read_bytes", blocked_file_access)

    projection = build_internal_alpha_review_console_safe_metadata_projection(
        _safe_source(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    assert projection["projection_created"] is True


def test_safe_projection_summary_is_counts_and_boundary_only() -> None:
    summary = build_safe_internal_alpha_review_console_projection_summary(
        _safe_source(),
        exact_approval_phrase=APPROVAL_PHRASE,
    )

    assert summary["summary_schema"] == "sentigraph_internal_alpha_review_console_safe_metadata_projection_summary_v0_1"
    assert summary["phase"] == "8Z-20"
    assert summary["projection_schema"] == "sentigraph_internal_alpha_review_console_safe_metadata_projection_v0_1"
    assert summary["projection_created"] is True
    assert summary["source_chain_boundary"] == "evidence_layer_write_candidate_boundary"
    assert summary["warning_count"] == 1
    assert summary["human_review_required"] is True
    assert summary["no_automatic_trust_upgrade"] is True
    assert "allowed_actions" not in summary
    assert "blocked_actions" not in summary
    _assert_projection_safe_flags(summary)
    _assert_no_forbidden_sentinels(summary)
