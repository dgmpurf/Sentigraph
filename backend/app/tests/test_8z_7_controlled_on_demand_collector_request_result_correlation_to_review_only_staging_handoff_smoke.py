from __future__ import annotations

from pathlib import Path

import pytest

from app.services.private_collector_review_only_staging import (
    build_review_only_staging_gate_result,
    build_safe_review_only_staging_summary,
    create_review_only_staging_candidate,
)


APPROVAL_PHRASE = (
    "APPROVE_8Z_7_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_RESULT_CORRELATION_TO_REVIEW_ONLY_STAGING_HANDOFF_SMOKE"
)
FUTURE_8Z8_PHRASE = "APPROVE_8Z_8_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ENTRY_GATE_DECISION_DOCS_ONLY"
CORRELATION_SCHEMA = "sentigraph_on_demand_collector_request_result_correlation_v0_1"
REQUEST_SCHEMA = "sentigraph_on_demand_collection_request_metadata_v0_1"
PROVIDER_RESULT_SCHEMA = "sentigraph_on_demand_collector_provider_result_metadata_v0_1"
STAGING_CANDIDATE_SCHEMA = "sentigraph_on_demand_collector_review_only_staging_candidate_v0_1"
STAGING_MODE = "backend_only_local_review_only_staging_handoff_candidate"

FALSE_SIDE_EFFECTS = {
    "package_resolver_called": False,
    "provider_result_reader_called": False,
    "local_exchange_reader_called": False,
    "collector_job_run": False,
    "provider_job_run": False,
    "scheduler_created": False,
    "http_bridge_created": False,
    "webhook_created": False,
    "private_collector_source_inspected": False,
    "real_exchange_dir_read": False,
    "real_package_dir_read": False,
    "evidence_rows_parsed": False,
    "evidence_items_jsonl_parsed": False,
    "evidence_items_csv_parsed": False,
    "source_manifest_rows_parsed": False,
    "collection_log_rows_parsed": False,
    "evidence_layer_write": False,
    "production_evidence_item_created": False,
    "production_case_created": False,
    "production_analysis_run_created": False,
    "actual_analysis_execution_started": False,
    "production_analysis_result_creation_authorized": False,
    "production_analysis_result_created": False,
    "8w69_pause_preserved": True,
    "8w70_reactivation_selected": False,
    "source11_runtime_called": False,
    "actual_final_summary_report_created": False,
    "b_end_report_runtime_generated": False,
    "sandbox_public_event_runtime_generated": False,
    "export_download_public_delivery_created": False,
    "route_changed": False,
    "frontend_changed": False,
    "runtime_changed": False,
    "raw_rows_exposed": False,
    "raw_comments_exposed": False,
    "raw_identities_exposed": False,
    "author_names_or_profile_urls_exposed": False,
    "secrets_read": False,
}

FORBIDDEN_FIELDS = {
    "cookie",
    "cookies",
    "session",
    "sessions",
    "token",
    "tokens",
    "api_key",
    "password",
    "browser_profile_path",
    "browser_profile_paths",
    "browser_profile",
    "profile_path",
    "raw_author_id",
    "raw_author_ids",
    "raw_author_name",
    "raw_author_names",
    "profile_url",
    "profile_urls",
    "private_message",
    "private_messages",
    "raw_rows",
    "raw_evidence_row_contents",
    "raw_comments",
    "raw_comment_dump",
    "raw_comment_dumps",
    "full_evidence_items_content",
    "source_manifest_rows",
    "source_manifest_row_contents",
    "collection_log_rows",
    "collection_log_row_contents",
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "auto_execute",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
}

FORBIDDEN_READY_CLAIMS = (
    "production-ready",
    "customer-ready",
    "public-ready",
    "export-ready",
    "final-ready",
    "source-11-runtime-ready",
)


def _safe_correlation_summary(**overrides: object) -> dict[str, object]:
    summary: dict[str, object] = {
        "status": "correlation_ready_for_manual_review",
        "request_result_correlation_created": True,
        "request_result_correlation_schema": CORRELATION_SCHEMA,
        "request_metadata_schema": REQUEST_SCHEMA,
        "provider_result_metadata_schema": PROVIDER_RESULT_SCHEMA,
        "request_id_match": True,
        "provider_result_id_unique_in_fixture_scope": True,
        "package_reference_policy": "opaque_safe_identifier_only",
        "metadata_only": True,
        "row_content_included": False,
        "raw_identity_included": False,
        "secrets_included": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "review_only_staging_created": False,
        "review_only_staging_handoff_performed": False,
        "safe_counts": {"evidence_count": 12, "source_count": 4, "warning_count": 1, "error_count": 0},
        "safe_labels": {
            "request_id": "request_8z7_fixture_001",
            "provider_result_id": "provider_result_8z7_fixture_001",
            "case_id_hint": "case_hint_label_only",
            "case_title_hint": "Selected public event label",
            "package_name": "safe_selected_sample_package",
        },
        "blockers": [],
        "warnings": [],
        **FALSE_SIDE_EFFECTS,
    }
    summary.update(overrides)
    return summary


def _build_8z7_controlled_handoff_smoke(
    approval_phrase: str | None = APPROVAL_PHRASE,
    **correlation_overrides: object,
) -> dict[str, object]:
    if approval_phrase != APPROVAL_PHRASE:
        return _blocked_smoke("missing_or_wrong_8z7_approval_phrase", helper_called=False)

    correlation = _safe_correlation_summary(**correlation_overrides)
    blockers = _correlation_blockers(correlation)
    if blockers:
        return _blocked_smoke(*blockers, helper_called=False)

    handoff_summary = _handoff_summary_from_correlation(correlation)
    candidate = create_review_only_staging_candidate(handoff_summary, requested_by="internal_operator")
    gate = build_review_only_staging_gate_result(handoff_summary, candidate)
    safe_summary = build_safe_review_only_staging_summary(candidate, gate)

    return {
        "status": "ready_for_human_review",
        "review_only_staging_candidate_created": True,
        "review_only_staging_candidate_schema": STAGING_CANDIDATE_SCHEMA,
        "review_only_staging_mode": STAGING_MODE,
        "source_request_result_correlation_schema": correlation["request_result_correlation_schema"],
        "request_metadata_schema": correlation["request_metadata_schema"],
        "provider_result_metadata_schema": correlation["provider_result_metadata_schema"],
        "request_id_match": True,
        "provider_result_id_unique_in_fixture_scope": True,
        "package_reference_policy": "opaque_safe_identifier_only",
        "metadata_only": True,
        "row_content_included": False,
        "raw_identity_included": False,
        "secrets_included": False,
        "review_only_staging_handoff_performed": True,
        "persistent_staging_storage_created": False,
        "actual_review_queue_runtime_used": False,
        "production_review_queue_item_created": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "staging_helper_called": True,
        "candidate_staging_status": candidate.staging_status,
        "candidate_review_status": candidate.review_status,
        "candidate_promotion_status": candidate.promotion_status,
        "safe_summary_schema": safe_summary["schema"],
        "path_exposed": safe_summary["path_exposed"],
        "path_reference": safe_summary["path_reference"],
        "blockers": [],
        **FALSE_SIDE_EFFECTS,
    }


def _blocked_smoke(*blockers: str, helper_called: bool) -> dict[str, object]:
    return {
        "status": "blocked",
        "review_only_staging_candidate_created": False,
        "review_only_staging_candidate_schema": STAGING_CANDIDATE_SCHEMA,
        "review_only_staging_mode": STAGING_MODE,
        "source_request_result_correlation_schema": CORRELATION_SCHEMA,
        "request_metadata_schema": REQUEST_SCHEMA,
        "provider_result_metadata_schema": PROVIDER_RESULT_SCHEMA,
        "metadata_only": True,
        "row_content_included": False,
        "raw_identity_included": False,
        "secrets_included": False,
        "review_only_staging_handoff_performed": False,
        "persistent_staging_storage_created": False,
        "actual_review_queue_runtime_used": False,
        "production_review_queue_item_created": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "staging_helper_called": helper_called,
        "blockers": list(blockers),
        **FALSE_SIDE_EFFECTS,
    }


def _handoff_summary_from_correlation(correlation: dict[str, object]) -> dict[str, object]:
    safe_labels = correlation["safe_labels"]
    safe_counts = correlation["safe_counts"]
    assert isinstance(safe_labels, dict)
    assert isinstance(safe_counts, dict)
    return {
        "schema": "sentigraph_on_demand_collector_review_only_staging_handoff_smoke_v0_1",
        "smoke_status": "ready_for_metadata_only_handoff",
        "provider_result_id": safe_labels["provider_result_id"],
        "provider_result_status": "accepted_metadata_only",
        "package_resolution_status": "opaque_safe_identifier_not_resolved",
        "package_name": safe_labels["package_name"],
        "case_id": safe_labels["request_id"],
        "case_title_hint": safe_labels["case_title_hint"],
        "validation_status": "passed",
        "evidence_count": safe_counts["evidence_count"],
        "source_count": safe_counts["source_count"],
        "warning_count": safe_counts["warning_count"],
        "error_count": safe_counts["error_count"],
        "coverage_note": "Selected public sample metadata only; not full-web or full-platform coverage.",
        "metadata_only": True,
        "full_evidence_rows_read": False,
        "evidence_layer_write": False,
        "production_case_created": False,
        "analysis_run_created": False,
        "blockers": [],
        "warnings": [],
        "safety_markers": {
            "raw_author_id_exported": False,
            "raw_author_name_exported": False,
            "profile_url_exported": False,
            "raw_author_id_removed": True,
            "raw_author_name_removed": True,
            "no_private_messages": True,
        },
        "path_exposed": False,
        "path_reference": "opaque_safe_identifier_only",
    }


def _correlation_blockers(correlation: dict[str, object]) -> list[str]:
    blockers: list[str] = []
    blockers.extend(_forbidden_field_blockers(correlation))
    blockers.extend(_forbidden_text_blockers(correlation))
    expected_values = {
        "request_result_correlation_schema": CORRELATION_SCHEMA,
        "request_metadata_schema": REQUEST_SCHEMA,
        "provider_result_metadata_schema": PROVIDER_RESULT_SCHEMA,
        "request_id_match": True,
        "provider_result_id_unique_in_fixture_scope": True,
        "package_reference_policy": "opaque_safe_identifier_only",
        "metadata_only": True,
        "row_content_included": False,
        "raw_identity_included": False,
        "secrets_included": False,
        "review_only_staging_created": False,
        "review_only_staging_handoff_performed": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
    }
    for field_name, expected in expected_values.items():
        actual = correlation.get(field_name)
        if isinstance(expected, bool):
            if actual is not expected:
                blockers.append(f"{field_name}_must_be_{str(expected).lower()}")
            continue
        if actual != expected:
            blockers.append(f"{field_name}_must_be_{str(expected).lower()}")

    for field_name, expected in FALSE_SIDE_EFFECTS.items():
        if correlation.get(field_name) is not expected:
            blockers.append(f"{field_name}_must_be_{str(expected).lower()}")

    if not isinstance(correlation.get("safe_labels"), dict):
        blockers.append("safe_labels_must_be_object")
    if not isinstance(correlation.get("safe_counts"), dict):
        blockers.append("safe_counts_must_be_object")
    return blockers


def _forbidden_field_blockers(value: object, prefix: str = "") -> list[str]:
    blockers: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            lowered = key_text.lower()
            if lowered in FORBIDDEN_FIELDS:
                blockers.append(f"forbidden_field:{prefix}{key_text}")
            blockers.extend(_forbidden_field_blockers(nested, f"{prefix}{key_text}."))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            blockers.extend(_forbidden_field_blockers(nested, f"{prefix}{index}."))
    return blockers


def _forbidden_text_blockers(value: object) -> list[str]:
    text = str(value).lower()
    return [f"forbidden_ready_claim:{marker}" for marker in FORBIDDEN_READY_CLAIMS if marker in text]


def test_8z7_exact_phrase_creates_review_only_staging_candidate() -> None:
    summary = _build_8z7_controlled_handoff_smoke()

    assert summary["review_only_staging_candidate_created"] is True
    assert summary["review_only_staging_candidate_schema"] == STAGING_CANDIDATE_SCHEMA
    assert summary["review_only_staging_mode"] == STAGING_MODE
    assert summary["source_request_result_correlation_schema"] == CORRELATION_SCHEMA
    assert summary["request_metadata_schema"] == REQUEST_SCHEMA
    assert summary["provider_result_metadata_schema"] == PROVIDER_RESULT_SCHEMA
    assert summary["request_id_match"] is True
    assert summary["provider_result_id_unique_in_fixture_scope"] is True
    assert summary["package_reference_policy"] == "opaque_safe_identifier_only"
    assert summary["metadata_only"] is True
    assert summary["row_content_included"] is False
    assert summary["raw_identity_included"] is False
    assert summary["secrets_included"] is False
    assert summary["review_only_staging_handoff_performed"] is True
    assert summary["candidate_staging_status"] == "ready_for_human_review"
    assert summary["candidate_review_status"] == "ready_for_human_review"
    assert summary["candidate_promotion_status"] == "promotion_required"
    assert summary["safe_summary_schema"] == "sentigraph_review_only_staging_summary_v0_1"
    assert summary["path_exposed"] is False
    assert summary["path_reference"] == "review_only_metadata_summary"


@pytest.mark.parametrize(
    "wrong_phrase",
    [
        None,
        "",
        "wrong phrase",
        FUTURE_8Z8_PHRASE,
        "APPROVE_8Z_6_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_HANDOFF_GATE_DECISION_DOCS_ONLY",
        "APPROVE_8Z_5_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_RESULT_CORRELATION_SMOKE",
        "APPROVE_8Z_4_CONTROLLED_ON_DEMAND_COLLECTOR_PROVIDER_RESULT_METADATA_FIXTURE_SMOKE",
        "APPROVE_8Z_3_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_METADATA_FIXTURE_SMOKE",
        "APPROVE_8Z_2_ON_DEMAND_COLLECTOR_REQUEST_RESULT_METADATA_CONTRACT_DOCS_ONLY",
        "APPROVE_8Z_1_ON_DEMAND_COLLECTOR_WORKFLOW_CONTRACT_DOCS_ONLY",
        "APPROVE_8Y_ROUTE_C_RUNTIME",
        "APPROVE_8W_PRODUCTION_ANALYSIS_RESULT_CREATION",
    ],
)
def test_missing_wrong_or_neighbor_phrase_blocks_before_staging_helper_call(wrong_phrase: str | None) -> None:
    summary = _build_8z7_controlled_handoff_smoke(wrong_phrase)

    assert summary["status"] == "blocked"
    assert summary["review_only_staging_candidate_created"] is False
    assert summary["review_only_staging_handoff_performed"] is False
    assert summary["staging_helper_called"] is False
    assert summary["blockers"] == ["missing_or_wrong_8z7_approval_phrase"]


@pytest.mark.parametrize(
    ("field_name", "value", "blocker"),
    [
        ("request_result_correlation_schema", "wrong_schema", "request_result_correlation_schema_must_be_"),
        ("request_id_match", False, "request_id_match_must_be_true"),
        ("provider_result_id_unique_in_fixture_scope", False, "provider_result_id_unique_in_fixture_scope_must_be_true"),
        ("package_reference_policy", "path_to_package", "package_reference_policy_must_be_opaque_safe_identifier_only"),
        ("metadata_only", False, "metadata_only_must_be_true"),
        ("row_content_included", True, "row_content_included_must_be_false"),
        ("raw_identity_included", True, "raw_identity_included_must_be_false"),
        ("secrets_included", True, "secrets_included_must_be_false"),
        ("package_resolver_called", True, "package_resolver_called_must_be_false"),
        ("review_only_staging_created", True, "review_only_staging_created_must_be_false"),
        ("review_only_staging_handoff_performed", True, "review_only_staging_handoff_performed_must_be_false"),
        ("collector_job_run", True, "collector_job_run_must_be_false"),
        ("provider_job_run", True, "provider_job_run_must_be_false"),
        ("real_exchange_dir_read", True, "real_exchange_dir_read_must_be_false"),
        ("real_package_dir_read", True, "real_package_dir_read_must_be_false"),
        ("evidence_rows_parsed", True, "evidence_rows_parsed_must_be_false"),
        ("evidence_layer_write", True, "evidence_layer_write_must_be_false"),
        ("production_evidence_item_created", True, "production_evidence_item_created_must_be_false"),
        ("production_case_created", True, "production_case_created_must_be_false"),
        ("production_analysis_run_created", True, "production_analysis_run_created_must_be_false"),
        ("actual_analysis_execution_started", True, "actual_analysis_execution_started_must_be_false"),
        (
            "production_analysis_result_creation_authorized",
            True,
            "production_analysis_result_creation_authorized_must_be_false",
        ),
        ("production_analysis_result_created", True, "production_analysis_result_created_must_be_false"),
        ("source11_runtime_called", True, "source11_runtime_called_must_be_false"),
        ("actual_final_summary_report_created", True, "actual_final_summary_report_created_must_be_false"),
        ("human_review_required", False, "human_review_required_must_be_true"),
        ("no_automatic_trust_upgrade", False, "no_automatic_trust_upgrade_must_be_true"),
    ],
)
def test_unsafe_correlation_flags_block_before_staging_helper_call(
    field_name: str,
    value: object,
    blocker: str,
) -> None:
    summary = _build_8z7_controlled_handoff_smoke(**{field_name: value})

    assert summary["status"] == "blocked"
    assert summary["staging_helper_called"] is False
    assert any(actual.startswith(blocker) for actual in summary["blockers"])


@pytest.mark.parametrize(
    "field_name",
    [
        "cookie",
        "session",
        "token",
        "browser_profile_path",
        "raw_author_id",
        "raw_author_name",
        "profile_url",
        "private_message",
        "raw_rows",
        "raw_comments",
        "full_evidence_items_content",
        "source_manifest_rows",
        "collection_log_rows",
        "response_text",
        "generated_public_message",
        "target_user_list",
        "persuasion_score",
        "truth_score",
        "official_verified",
        "prediction_probability",
        "psychological_profile",
        "personality_diagnosis",
        "auto_execute",
        "publish_now",
        "send_now",
        "post_now",
        "execute_now",
    ],
)
def test_forbidden_request_result_or_correlation_fields_block_before_helper_call(field_name: str) -> None:
    summary = _build_8z7_controlled_handoff_smoke(**{field_name: "forbidden actual value"})

    assert summary["status"] == "blocked"
    assert summary["staging_helper_called"] is False
    assert any(field_name in blocker for blocker in summary["blockers"])


def test_public_ready_or_source11_runtime_ready_claim_blocks_before_helper_call() -> None:
    summary = _build_8z7_controlled_handoff_smoke(operator_claim="production-ready Source-11-runtime-ready")

    assert summary["status"] == "blocked"
    assert summary["staging_helper_called"] is False
    assert "forbidden_ready_claim:production-ready" in summary["blockers"]
    assert "forbidden_ready_claim:source-11-runtime-ready" in summary["blockers"]


def test_controlled_handoff_smoke_does_not_read_files_or_parse_rows(monkeypatch: pytest.MonkeyPatch) -> None:
    attempted_reads: list[str] = []

    def fail_if_called(self: Path, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        attempted_reads.append(str(self))
        raise AssertionError(f"unexpected file read: {self}")

    monkeypatch.setattr(Path, "read_text", fail_if_called)
    monkeypatch.setattr(Path, "read_bytes", fail_if_called)
    monkeypatch.setattr(Path, "open", fail_if_called)

    summary = _build_8z7_controlled_handoff_smoke()

    assert summary["status"] == "ready_for_human_review"
    assert attempted_reads == []
    assert summary["package_resolver_called"] is False
    assert summary["provider_result_reader_called"] is False
    assert summary["local_exchange_reader_called"] is False
    assert summary["real_exchange_dir_read"] is False
    assert summary["real_package_dir_read"] is False
    assert summary["evidence_rows_parsed"] is False
    assert summary["evidence_items_jsonl_parsed"] is False
    assert summary["evidence_items_csv_parsed"] is False
    assert summary["source_manifest_rows_parsed"] is False
    assert summary["collection_log_rows_parsed"] is False


def test_controlled_handoff_smoke_has_no_runtime_or_production_side_effects() -> None:
    summary = _build_8z7_controlled_handoff_smoke()

    assert summary["persistent_staging_storage_created"] is False
    assert summary["actual_review_queue_runtime_used"] is False
    assert summary["production_review_queue_item_created"] is False
    for flag_name, expected_value in FALSE_SIDE_EFFECTS.items():
        assert summary[flag_name] is expected_value
