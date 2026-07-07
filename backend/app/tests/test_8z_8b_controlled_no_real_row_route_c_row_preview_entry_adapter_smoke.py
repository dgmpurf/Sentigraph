from __future__ import annotations

import builtins
import importlib
import json
import sys
from pathlib import Path

import pytest


APPROVAL_PHRASE = "APPROVE_8Z_8B_CONTROLLED_NO_REAL_ROW_ROUTE_C_ROW_PREVIEW_ENTRY_ADAPTER_SMOKE"
FUTURE_8Z8C_PHRASE = "APPROVE_8Z_8C_NO_REAL_ROW_ADAPTER_COMPLETION_ROUTE_C_ROW_PREVIEW_REGATE_DECISION_DOCS_ONLY"
INACTIVE_8Z9_PHRASE = "APPROVE_8Z_9_CONTROLLED_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ROW_PREVIEW_SMOKE"
INNER_8W7_PHRASE = "APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION"

ADAPTER_SCHEMA = "sentigraph_on_demand_collector_no_real_row_route_c_row_preview_entry_adapter_v0_1"
ADAPTER_MODE = "backend_only_local_no_real_row_route_c_row_preview_entry_adapter"
STAGING_SCHEMA = "sentigraph_on_demand_collector_review_only_staging_candidate_v0_1"
STAGING_MODE = "backend_only_local_review_only_staging_handoff_candidate"
CORRELATION_SCHEMA = "sentigraph_on_demand_collector_request_result_correlation_v0_1"

DISALLOWED_IMPORT_PREFIXES = (
    "app.services.controlled_row_preview",
    "app.services.private_collector_package_resolver",
    "app.services.private_collector_provider_result_reader",
    "app.services.local_exchange_reader",
    "app.services.private_collector_review_only_staging",
    "app.services.controlled_evidence_candidate",
    "app.services.controlled_review_queue_candidate",
    "app.services.controlled_evidence_layer_import_candidate",
    "app.services.controlled_evidence_layer_write_candidate",
    "app.services.controlled_evidenceitem_evidence_layer_write_runtime",
)

FALSE_SIDE_EFFECTS = {
    "row_preview_executed": False,
    "controlled_row_preview_helper_called": False,
    "redacted_review_only_row_preview_created": False,
    "row_preview_rows_created": False,
    "synthetic_evidence_rows_created": False,
    "fake_evidence_rows_created": False,
    "evidence_rows_created": False,
    "row_source_path_present": False,
    "row_source_file_opened": False,
    "file_read_performed": False,
    "evidence_items_jsonl_parsed": False,
    "evidence_items_csv_parsed": False,
    "source_manifest_rows_parsed": False,
    "collection_log_rows_parsed": False,
    "package_resolver_called": False,
    "provider_result_reader_called": False,
    "local_exchange_reader_called": False,
    "review_only_staging_helper_called": False,
    "persistent_staging_storage_created": False,
    "actual_review_queue_runtime_used": False,
    "production_review_queue_item_created": False,
    "collector_job_run": False,
    "provider_job_run": False,
    "scheduler_created": False,
    "http_bridge_created": False,
    "webhook_created": False,
    "private_collector_source_inspected": False,
    "real_exchange_dir_read": False,
    "real_package_dir_read": False,
    "evidence_rows_parsed": False,
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
    "route_ready": False,
    "frontend_ready": False,
    "production_ready": False,
    "customer_ready": False,
    "public_ready": False,
    "raw_rows_exposed": False,
    "raw_comments_exposed": False,
    "raw_identities_exposed": False,
    "author_names_or_profile_urls_exposed": False,
    "secrets_read": False,
}

FORBIDDEN_FIELDS = {
    "row_source_path",
    "source_url",
    "raw_row",
    "raw_rows",
    "row_body",
    "row_bodies",
    "row_snippet",
    "row_snippets",
    "raw_comment",
    "raw_comments",
    "raw_identity",
    "raw_identities",
    "raw_author_id",
    "raw_author_ids",
    "author_id",
    "author_ids",
    "raw_author_name",
    "raw_author_names",
    "author_name",
    "author_names",
    "profile_url",
    "profile_urls",
    "full_evidence_items_content",
    "source_manifest_rows",
    "collection_log_rows",
    "cookie",
    "cookies",
    "session",
    "sessions",
    "token",
    "tokens",
    "browser_profile",
    "browser_profile_path",
    "secret",
    "secrets",
    ".env",
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "pred" + "iction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "auto_execute",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
}

FORBIDDEN_TEXT_MARKERS = (
    "production" + "-ready",
    "customer" + "-ready",
    "public" + "-ready",
    "export" + "-ready",
    "final" + "-ready",
    "source-11" + "-runtime-ready",
)


def build_safe_8z7_review_only_staging_candidate_fixture(**overrides: object) -> dict[str, object]:
    fixture: dict[str, object] = {
        "review_only_staging_candidate_schema": STAGING_SCHEMA,
        "review_only_staging_mode": STAGING_MODE,
        "source_request_result_correlation_schema": CORRELATION_SCHEMA,
        "package_reference_policy": "opaque_safe_identifier_only",
        "metadata_only": True,
        "entry_source_kind": "8z7_review_only_staging_candidate",
        "candidate_id": "review_staging_candidate_label_only",
        "request_id": "request_8z8b_fixture_001",
        "provider_result_id": "provider_result_8z8b_fixture_001",
        "package_name": "safe_selected_sample_package",
        "safe_counts": {"evidence_count": 12, "source_count": 4, "warning_count": 1, "error_count": 0},
        "row_content_included": False,
        "raw_identity_included": False,
        "secrets_included": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "blockers": [],
        "warnings": ["manual_review_required", "no_real_row_entry_candidate_only"],
        **FALSE_SIDE_EFFECTS,
    }
    fixture.update(overrides)
    return fixture


def build_no_real_row_route_c_row_preview_entry_adapter(
    source_candidate: dict[str, object] | None,
    *,
    approval_phrase: str | None,
    output_overrides: dict[str, object] | None = None,
) -> dict[str, object]:
    if approval_phrase != APPROVAL_PHRASE:
        return _blocked_adapter("missing_or_wrong_8z8b_approval_phrase", adapter_created=False)

    blockers = validate_no_real_row_route_c_row_preview_entry_adapter_source(source_candidate)
    if blockers:
        return _blocked_adapter(*blockers, adapter_created=False)

    adapter: dict[str, object] = {
        "status": "route_c_row_preview_entry_candidate_ready_for_regate",
        "no_real_row_route_c_row_preview_entry_adapter_created": True,
        "adapter_schema": ADAPTER_SCHEMA,
        "adapter_mode": ADAPTER_MODE,
        "route_c_row_preview_entry_candidate_created": True,
        "entry_candidate_only": True,
        "metadata_only": True,
        "source_review_only_staging_candidate_schema": source_candidate["review_only_staging_candidate_schema"],
        "source_review_only_staging_mode": source_candidate["review_only_staging_mode"],
        "source_request_result_correlation_schema": source_candidate["source_request_result_correlation_schema"],
        "package_reference_policy": "opaque_safe_identifier_only",
        "row_content_included": False,
        "raw_identity_included": False,
        "secrets_included": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "next_gate": "separate_docs_only_re_gate_required_before_8z9",
        "8z9_phrase_status": "inactive_not_ready_pending_8Z_8C_re_gate",
        "not_row_preview": True,
        "not_redacted_row_preview": True,
        "not_synthetic_evidence": True,
        "not_fake_evidence_rows": True,
        "not_evidence_candidate": True,
        "future_route_c_row_preview_may_be_regated_later": True,
        "blockers": [],
        "warnings": ["manual_review_required", "adapter_candidate_only_no_real_rows"],
        **FALSE_SIDE_EFFECTS,
    }
    if output_overrides:
        adapter.update(output_overrides)
    output_blockers = _adapter_output_blockers(adapter)
    if output_blockers:
        return _blocked_adapter(*output_blockers, adapter_created=False)
    return adapter


def validate_no_real_row_route_c_row_preview_entry_adapter(adapter: dict[str, object]) -> list[str]:
    blockers: list[str] = []
    if adapter.get("adapter_schema") != ADAPTER_SCHEMA:
        blockers.append("adapter_schema_mismatch")
    if adapter.get("adapter_mode") != ADAPTER_MODE:
        blockers.append("adapter_mode_mismatch")
    blockers.extend(_adapter_output_blockers(adapter))
    return blockers


def validate_no_real_row_route_c_row_preview_entry_adapter_source(source_candidate: object) -> list[str]:
    if not isinstance(source_candidate, dict):
        return ["source_candidate_must_be_dict"]

    blockers: list[str] = []
    blockers.extend(_forbidden_content_blockers(source_candidate))
    required_values = {
        "review_only_staging_candidate_schema": STAGING_SCHEMA,
        "review_only_staging_mode": STAGING_MODE,
        "source_request_result_correlation_schema": CORRELATION_SCHEMA,
        "package_reference_policy": "opaque_safe_identifier_only",
        "metadata_only": True,
        "row_content_included": False,
        "raw_identity_included": False,
        "secrets_included": False,
        "package_resolver_called": False,
        "provider_result_reader_called": False,
        "local_exchange_reader_called": False,
        "review_only_staging_helper_called": False,
        "persistent_staging_storage_created": False,
        "actual_review_queue_runtime_used": False,
        "production_review_queue_item_created": False,
        "collector_job_run": False,
        "provider_job_run": False,
        "real_exchange_dir_read": False,
        "real_package_dir_read": False,
        "evidence_rows_parsed": False,
        "evidence_layer_write": False,
        "production_evidence_item_created": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "actual_analysis_execution_started": False,
        "production_analysis_result_creation_authorized": False,
        "production_analysis_result_created": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
    }
    for field_name, expected in required_values.items():
        actual = source_candidate.get(field_name)
        if isinstance(expected, bool):
            if actual is not expected:
                blockers.append(f"{field_name}_must_be_{str(expected).lower()}")
            continue
        if actual != expected:
            blockers.append(f"{field_name}_must_be_{expected}")
    return blockers


def _adapter_output_blockers(adapter: dict[str, object]) -> list[str]:
    blockers: list[str] = []
    blockers.extend(_forbidden_content_blockers(adapter))
    required_values = {
        "metadata_only": True,
        "entry_candidate_only": True,
        "route_c_row_preview_entry_candidate_created": True,
        "row_preview_executed": False,
        "controlled_row_preview_helper_called": False,
        "redacted_review_only_row_preview_created": False,
        "row_preview_rows_created": False,
        "synthetic_evidence_rows_created": False,
        "fake_evidence_rows_created": False,
        "evidence_rows_created": False,
        "row_source_path_present": False,
        "row_source_file_opened": False,
        "file_read_performed": False,
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
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "customer_ready": False,
        "public_ready": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
    }
    for field_name, expected in required_values.items():
        actual = adapter.get(field_name)
        if isinstance(expected, bool):
            if actual is not expected:
                blockers.append(f"{field_name}_must_be_{str(expected).lower()}")
            continue
        if actual != expected:
            blockers.append(f"{field_name}_must_be_{expected}")
    for field_name, expected in FALSE_SIDE_EFFECTS.items():
        actual = adapter.get(field_name)
        if isinstance(expected, bool) and actual is not expected:
            blockers.append(f"{field_name}_must_be_{str(expected).lower()}")
    return blockers


def _blocked_adapter(*blockers: str, adapter_created: bool) -> dict[str, object]:
    return {
        "status": "blocked",
        "no_real_row_route_c_row_preview_entry_adapter_created": adapter_created,
        "adapter_schema": ADAPTER_SCHEMA,
        "adapter_mode": ADAPTER_MODE,
        "route_c_row_preview_entry_candidate_created": False,
        "entry_candidate_only": True,
        "metadata_only": True,
        "row_content_included": False,
        "raw_identity_included": False,
        "secrets_included": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "next_gate": "separate_docs_only_re_gate_required_before_8z9",
        "8z9_phrase_status": "inactive_not_ready_pending_8Z_8C_re_gate",
        "blockers": list(blockers),
        **FALSE_SIDE_EFFECTS,
    }


def _forbidden_content_blockers(value: object, prefix: str = "") -> list[str]:
    blockers: list[str] = []
    if isinstance(value, dict):
        for key, nested_value in value.items():
            key_text = str(key)
            lowered_key = key_text.lower()
            if lowered_key in FORBIDDEN_FIELDS:
                blockers.append(f"forbidden_field:{prefix}{key_text}")
            blockers.extend(_forbidden_content_blockers(nested_value, f"{prefix}{key_text}."))
        return blockers
    if isinstance(value, list):
        for index, nested_value in enumerate(value):
            blockers.extend(_forbidden_content_blockers(nested_value, f"{prefix}{index}."))
        return blockers
    if isinstance(value, str):
        lowered_value = value.lower()
        blockers.extend(
            f"forbidden_ready_claim:{marker}" for marker in FORBIDDEN_TEXT_MARKERS if marker in lowered_value
        )
    return blockers


def _json_text(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def test_8z8b_exact_phrase_creates_no_real_row_entry_adapter_candidate() -> None:
    adapter = build_no_real_row_route_c_row_preview_entry_adapter(
        build_safe_8z7_review_only_staging_candidate_fixture(),
        approval_phrase=APPROVAL_PHRASE,
    )

    assert adapter["no_real_row_route_c_row_preview_entry_adapter_created"] is True
    assert adapter["adapter_schema"] == ADAPTER_SCHEMA
    assert adapter["adapter_mode"] == ADAPTER_MODE
    assert adapter["route_c_row_preview_entry_candidate_created"] is True
    assert adapter["entry_candidate_only"] is True
    assert adapter["metadata_only"] is True
    assert adapter["source_review_only_staging_candidate_schema"] == STAGING_SCHEMA
    assert adapter["source_review_only_staging_mode"] == STAGING_MODE
    assert adapter["source_request_result_correlation_schema"] == CORRELATION_SCHEMA
    assert adapter["package_reference_policy"] == "opaque_safe_identifier_only"
    assert adapter["next_gate"] == "separate_docs_only_re_gate_required_before_8z9"
    assert adapter["8z9_phrase_status"] == "inactive_not_ready_pending_8Z_8C_re_gate"
    assert adapter["human_review_required"] is True
    assert adapter["no_automatic_trust_upgrade"] is True
    assert validate_no_real_row_route_c_row_preview_entry_adapter(adapter) == []


def test_adapter_is_metadata_entry_candidate_not_preview_or_evidence_candidate() -> None:
    adapter = build_no_real_row_route_c_row_preview_entry_adapter(
        build_safe_8z7_review_only_staging_candidate_fixture(),
        approval_phrase=APPROVAL_PHRASE,
    )

    assert adapter["not_row_preview"] is True
    assert adapter["not_redacted_row_preview"] is True
    assert adapter["not_synthetic_evidence"] is True
    assert adapter["not_fake_evidence_rows"] is True
    assert adapter["not_evidence_candidate"] is True
    assert adapter["future_route_c_row_preview_may_be_regated_later"] is True
    assert "preview_rows" not in adapter
    assert "evidence_rows" not in adapter
    assert "row_source_path" not in adapter


@pytest.mark.parametrize(
    "wrong_phrase",
    [
        None,
        "",
        "wrong phrase",
        "APPROVE_8Z_8A_NO_REAL_ROW_ROUTE_C_ROW_PREVIEW_ENTRY_COMPATIBILITY_DESIGN_DOCS_ONLY",
        INACTIVE_8Z9_PHRASE,
        INNER_8W7_PHRASE,
        "APPROVE_8Z_8_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ENTRY_GATE_DECISION_DOCS_ONLY",
        "APPROVE_8Z_7_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_RESULT_CORRELATION_TO_REVIEW_ONLY_STAGING_HANDOFF_SMOKE",
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
def test_missing_wrong_neighbor_or_inner_helper_phrase_blocks_before_adapter_creation(
    wrong_phrase: str | None,
) -> None:
    adapter = build_no_real_row_route_c_row_preview_entry_adapter(
        build_safe_8z7_review_only_staging_candidate_fixture(),
        approval_phrase=wrong_phrase,
    )

    assert adapter["status"] == "blocked"
    assert adapter["no_real_row_route_c_row_preview_entry_adapter_created"] is False
    assert adapter["route_c_row_preview_entry_candidate_created"] is False
    assert adapter["blockers"] == ["missing_or_wrong_8z8b_approval_phrase"]


@pytest.mark.parametrize(
    ("field_name", "value", "blocker"),
    [
        ("review_only_staging_candidate_schema", "wrong", "review_only_staging_candidate_schema_must_be_"),
        ("source_request_result_correlation_schema", "wrong", "source_request_result_correlation_schema_must_be_"),
        ("package_reference_policy", "resolved_path", "package_reference_policy_must_be_opaque_safe_identifier_only"),
        ("metadata_only", False, "metadata_only_must_be_true"),
        ("row_content_included", True, "row_content_included_must_be_false"),
        ("raw_identity_included", True, "raw_identity_included_must_be_false"),
        ("secrets_included", True, "secrets_included_must_be_false"),
        ("package_resolver_called", True, "package_resolver_called_must_be_false"),
        ("provider_result_reader_called", True, "provider_result_reader_called_must_be_false"),
        ("local_exchange_reader_called", True, "local_exchange_reader_called_must_be_false"),
        ("review_only_staging_helper_called", True, "review_only_staging_helper_called_must_be_false"),
        ("persistent_staging_storage_created", True, "persistent_staging_storage_created_must_be_false"),
        ("actual_review_queue_runtime_used", True, "actual_review_queue_runtime_used_must_be_false"),
        ("production_review_queue_item_created", True, "production_review_queue_item_created_must_be_false"),
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
        ("human_review_required", False, "human_review_required_must_be_true"),
        ("no_automatic_trust_upgrade", False, "no_automatic_trust_upgrade_must_be_true"),
    ],
)
def test_unsafe_source_candidate_blocks_before_adapter_creation(
    field_name: str,
    value: object,
    blocker: str,
) -> None:
    adapter = build_no_real_row_route_c_row_preview_entry_adapter(
        build_safe_8z7_review_only_staging_candidate_fixture(**{field_name: value}),
        approval_phrase=APPROVAL_PHRASE,
    )

    assert adapter["status"] == "blocked"
    assert adapter["no_real_row_route_c_row_preview_entry_adapter_created"] is False
    assert any(actual.startswith(blocker) for actual in adapter["blockers"])


@pytest.mark.parametrize(
    "field_name",
    [
        "row_source_path",
        "row_body",
        "row_snippet",
        "raw_comment",
        "raw_author_id",
        "raw_author_name",
        "profile_url",
        "cookie",
        "session",
        "token",
        "browser_profile_path",
        "secret",
        ".env",
        "full_evidence_items_content",
        "source_manifest_rows",
        "collection_log_rows",
        "response_text",
        "generated_public_message",
        "target_user_list",
        "persuasion_score",
        "truth_score",
        "official_verified",
        "pred" + "iction_probability",
        "psychological_profile",
        "personality_diagnosis",
        "auto_execute",
        "publish_now",
        "send_now",
        "post_now",
        "execute_now",
    ],
)
def test_forbidden_source_fields_block_before_adapter_creation(field_name: str) -> None:
    adapter = build_no_real_row_route_c_row_preview_entry_adapter(
        build_safe_8z7_review_only_staging_candidate_fixture(**{field_name: "forbidden actual value"}),
        approval_phrase=APPROVAL_PHRASE,
    )

    assert adapter["status"] == "blocked"
    assert any(field_name in blocker for blocker in adapter["blockers"])


@pytest.mark.parametrize(
    ("field_name", "value", "blocker"),
    [
        ("row_source_path_present", True, "row_source_path_present_must_be_false"),
        ("row_preview_executed", True, "row_preview_executed_must_be_false"),
        ("controlled_row_preview_helper_called", True, "controlled_row_preview_helper_called_must_be_false"),
        ("redacted_review_only_row_preview_created", True, "redacted_review_only_row_preview_created_must_be_false"),
        ("row_preview_rows_created", True, "row_preview_rows_created_must_be_false"),
        ("synthetic_evidence_rows_created", True, "synthetic_evidence_rows_created_must_be_false"),
        ("fake_evidence_rows_created", True, "fake_evidence_rows_created_must_be_false"),
        ("evidence_rows_created", True, "evidence_rows_created_must_be_false"),
        ("evidence_layer_write", True, "evidence_layer_write_must_be_false"),
        ("production_case_created", True, "production_case_created_must_be_false"),
        ("route_ready", True, "route_ready_must_be_false"),
        ("frontend_ready", True, "frontend_ready_must_be_false"),
        ("public_ready", True, "public_ready_must_be_false"),
    ],
)
def test_unsafe_adapter_output_flags_block(
    field_name: str,
    value: object,
    blocker: str,
) -> None:
    adapter = build_no_real_row_route_c_row_preview_entry_adapter(
        build_safe_8z7_review_only_staging_candidate_fixture(),
        approval_phrase=APPROVAL_PHRASE,
        output_overrides={field_name: value},
    )

    assert adapter["status"] == "blocked"
    assert any(actual.startswith(blocker) for actual in adapter["blockers"])


def test_forbidden_adapter_output_fields_and_ready_claims_block() -> None:
    forbidden_field = build_no_real_row_route_c_row_preview_entry_adapter(
        build_safe_8z7_review_only_staging_candidate_fixture(),
        approval_phrase=APPROVAL_PHRASE,
        output_overrides={"raw_rows": ["forbidden"]},
    )
    ready_claim = build_no_real_row_route_c_row_preview_entry_adapter(
        build_safe_8z7_review_only_staging_candidate_fixture(),
        approval_phrase=APPROVAL_PHRASE,
        output_overrides={"operator_claim": "production" + "-ready Source-11" + "-runtime-ready"},
    )

    assert "forbidden_field:raw_rows" in forbidden_field["blockers"]
    assert "forbidden_ready_claim:" + "production" + "-ready" in ready_claim["blockers"]
    assert "forbidden_ready_claim:" + "source-11" + "-runtime-ready" in ready_claim["blockers"]


def test_no_file_read_or_disallowed_helper_import_occurs(monkeypatch: pytest.MonkeyPatch) -> None:
    attempted_reads: list[str] = []
    attempted_imports: list[str] = []
    before_modules = set(sys.modules)

    def fail_read(self: Path, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        attempted_reads.append(str(self))
        raise AssertionError(f"unexpected file read: {self}")

    original_import = builtins.__import__
    original_import_module = importlib.import_module

    def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):  # noqa: ANN001, ANN002, ANN003
        if name.startswith(DISALLOWED_IMPORT_PREFIXES):
            attempted_imports.append(name)
            raise AssertionError(f"unexpected helper import: {name}")
        return original_import(name, globals, locals, fromlist, level)

    def guarded_import_module(name: str, package: str | None = None):  # noqa: ANN001
        if name.startswith(DISALLOWED_IMPORT_PREFIXES):
            attempted_imports.append(name)
            raise AssertionError(f"unexpected helper import: {name}")
        return original_import_module(name, package)

    monkeypatch.setattr(Path, "read_text", fail_read)
    monkeypatch.setattr(Path, "read_bytes", fail_read)
    monkeypatch.setattr(Path, "open", fail_read)
    monkeypatch.setattr(builtins, "__import__", guarded_import)
    monkeypatch.setattr(importlib, "import_module", guarded_import_module)

    adapter = build_no_real_row_route_c_row_preview_entry_adapter(
        build_safe_8z7_review_only_staging_candidate_fixture(),
        approval_phrase=APPROVAL_PHRASE,
    )

    assert adapter["status"] == "route_c_row_preview_entry_candidate_ready_for_regate"
    assert attempted_reads == []
    assert attempted_imports == []
    new_modules = set(sys.modules) - before_modules
    assert not {
        module_name
        for module_name in new_modules
        if module_name.startswith(DISALLOWED_IMPORT_PREFIXES)
    }
    for flag_name in (
        "controlled_row_preview_helper_called",
        "package_resolver_called",
        "provider_result_reader_called",
        "local_exchange_reader_called",
        "review_only_staging_helper_called",
        "evidence_layer_write",
        "actual_review_queue_runtime_used",
        "production_review_queue_item_created",
    ):
        assert adapter[flag_name] is False


def test_adapter_has_no_runtime_or_production_side_effects() -> None:
    adapter = build_no_real_row_route_c_row_preview_entry_adapter(
        build_safe_8z7_review_only_staging_candidate_fixture(),
        approval_phrase=APPROVAL_PHRASE,
    )

    for flag_name, expected_value in FALSE_SIDE_EFFECTS.items():
        assert adapter[flag_name] is expected_value
    serialized = _json_text(adapter).lower()
    assert "evidence_items.jsonl" not in serialized
    assert "evidence_items.csv" not in serialized
    assert ":/" not in serialized
    assert ":\\" not in serialized
