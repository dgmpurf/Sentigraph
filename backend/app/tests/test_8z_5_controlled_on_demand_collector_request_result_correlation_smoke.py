from __future__ import annotations

from pathlib import Path

APPROVAL_PHRASE = "APPROVE_8Z_5_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_RESULT_CORRELATION_SMOKE"
CORRELATION_SCHEMA = "sentigraph_on_demand_collector_request_result_correlation_v0_1"
CORRELATION_MODE = "backend_only_local_on_demand_request_result_correlation_fixture"
REQUEST_SCHEMA = "sentigraph_on_demand_collection_request_metadata_v0_1"
PROVIDER_RESULT_SCHEMA = "sentigraph_on_demand_collector_provider_result_metadata_v0_1"

REQUEST_ALLOWED_FIELDS = {
    "request_id",
    "request_schema",
    "request_version",
    "case_id_hint",
    "event_slug",
    "event_title",
    "event_summary_safe_text",
    "topic_query_safe_text",
    "requested_platform_labels",
    "collection_goal",
    "collection_scope_note",
    "time_window_hint",
    "expected_output_contract",
    "expected_package_role",
    "operator_label",
    "request_created_at",
    "request_created_by_label",
    "safety_constraints",
    "review_required",
    "no_cookie_transfer",
    "no_secret_transfer",
    "no_browser_profile_transfer",
    "no_automatic_execution_by_sentigraph",
    "no_sentigraph_scheduler",
    "no_sentigraph_live_fetch",
    "no_automatic_trust_upgrade",
    "human_review_required",
    "request_state",
}

RESULT_ALLOWED_FIELDS = {
    "provider_result_id",
    "provider_result_schema",
    "request_id",
    "provider_job_id",
    "external_collector_label",
    "collector_project_label",
    "package_name",
    "package_role",
    "package_schema_version",
    "package_reference_kind",
    "package_reference_safe_id",
    "validation_status",
    "validation_summary",
    "evidence_count",
    "source_count",
    "warning_count",
    "error_count",
    "coverage_note_summary",
    "platform_label_summary",
    "source_type_summary",
    "package_file_presence_map",
    "manifest_present",
    "validation_report_present",
    "coverage_note_present",
    "evidence_items_jsonl_present",
    "evidence_items_csv_present",
    "source_manifest_present",
    "collection_log_present",
    "export_timestamp",
    "provider_attestation_summary",
    "safety_markers",
    "metadata_only",
    "row_content_included",
    "raw_identity_included",
    "secrets_included",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "result_state",
}

REQUEST_STATES = {
    "draft",
    "pending_operator_review",
    "ready_for_external_collector_task",
    "handed_to_external_collector",
    "external_collection_in_progress_external_only",
    "external_collection_completed",
    "provider_result_metadata_available",
    "package_metadata_available",
    "review_only_staging_candidate_ready",
    "blocked_by_safety_policy",
    "rejected_by_operator",
    "expired",
    "cancelled",
}

RESULT_STATES = {
    "metadata_received",
    "metadata_schema_valid",
    "metadata_schema_invalid",
    "package_reference_valid",
    "package_reference_blocked",
    "package_metadata_ready",
    "validation_pass",
    "validation_warn",
    "validation_error",
    "review_only_ready",
    "blocked_pending_manual_review",
    "blocked_for_forbidden_metadata",
    "blocked_for_path_policy",
    "blocked_for_row_content_presence",
    "blocked_for_secret_or_identity_exposure",
}

FORBIDDEN_FIELDS = {
    "platform_password",
    "platform_passwords",
    "cookie",
    "cookies",
    "session",
    "sessions",
    "token",
    "tokens",
    "browser_profile_path",
    "browser_profile_paths",
    "proxy_credentials",
    "captcha_bypass_instructions",
    "anti_bot_bypass_instructions",
    "hidden_api_endpoint_instructions",
    "login_instructions",
    "raw_identity_lists",
    "target_user_list",
    "persuasion_score",
    "psychological_profile",
    "personality_diagnosis",
    "private_messages",
    "raw_author_id",
    "raw_author_ids",
    "raw_author_name",
    "raw_author_names",
    "profile_url",
    "profile_urls",
    "raw_evidence_row_contents",
    "raw_comment_dumps",
    "full_evidence_items_content",
    "source_manifest_row_contents",
    "collection_log_row_contents",
    "response_text",
    "generated_public_message",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "secrets",
    ".env",
    "auto_execute",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
}

FORBIDDEN_TEXT_MARKERS = (
    "raw row",
    "raw rows",
    "raw comment",
    "raw comments",
    "raw identity",
    "raw identities",
    "raw_author_id",
    "raw_author_name",
    "profile_url",
    "cookie",
    "session",
    "token",
    "secret",
    "api key",
    "password",
)

REQUEST_REQUIRED_TRUE_FLAGS = [
    "review_required",
    "no_cookie_transfer",
    "no_secret_transfer",
    "no_browser_profile_transfer",
    "no_automatic_execution_by_sentigraph",
    "no_sentigraph_scheduler",
    "no_sentigraph_live_fetch",
    "no_automatic_trust_upgrade",
    "human_review_required",
]

FALSE_SIDE_EFFECTS = {
    "collector_job_run": False,
    "provider_job_run": False,
    "scheduler_created": False,
    "http_bridge_created": False,
    "webhook_created": False,
    "private_collector_source_inspected": False,
    "real_exchange_dir_read": False,
    "real_package_dir_read": False,
    "package_resolver_called": False,
    "review_only_staging_created": False,
    "review_only_staging_handoff_performed": False,
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


def _safe_request_metadata(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "request_id": "request_8z5_fixture_001",
        "request_schema": REQUEST_SCHEMA,
        "request_version": "0.1",
        "case_id_hint": "case_hint_label_only",
        "event_slug": "event-slug-label-only",
        "event_title": "Selected public event label",
        "event_summary_safe_text": "Safe selected public sample context for operator review.",
        "topic_query_safe_text": "Safe topic text for external on-demand collector planning.",
        "requested_platform_labels": ["public_forum_label", "news_label"],
        "collection_goal": "Prepare metadata-only external collector request fixture.",
        "collection_scope_note": "Selected sample planning only; not full-web or full-platform coverage.",
        "time_window_hint": "operator_selected_window_label",
        "expected_output_contract": PROVIDER_RESULT_SCHEMA,
        "expected_package_role": "review_only_metadata_candidate",
        "operator_label": "local_operator_label",
        "request_created_at": "2026-07-06T00:00:00Z",
        "request_created_by_label": "sentigraph_local_test",
        "safety_constraints": ["no collector execution", "no secrets", "no Sentigraph live fetch"],
        "review_required": True,
        "no_cookie_transfer": True,
        "no_secret_transfer": True,
        "no_browser_profile_transfer": True,
        "no_automatic_execution_by_sentigraph": True,
        "no_sentigraph_scheduler": True,
        "no_sentigraph_live_fetch": True,
        "no_automatic_trust_upgrade": True,
        "human_review_required": True,
        "request_state": "pending_operator_review",
    }
    payload.update(overrides)
    return payload


def _safe_provider_result_metadata(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "provider_result_id": "provider_result_8z5_fixture_001",
        "provider_result_schema": PROVIDER_RESULT_SCHEMA,
        "request_id": "request_8z5_fixture_001",
        "provider_job_id": "external_job_label_only",
        "external_collector_label": "external_collector_label_only",
        "collector_project_label": "collector_project_label_only",
        "package_name": "safe_selected_sample_package",
        "package_role": "review_only_metadata_candidate",
        "package_schema_version": "0.1",
        "package_reference_kind": "opaque_safe_identifier_only",
        "package_reference_safe_id": "package_ref_8z5_fixture_001",
        "validation_status": "validation_warn",
        "validation_summary": "Safe metadata summary only; content rows are not included.",
        "evidence_count": 12,
        "source_count": 4,
        "warning_count": 1,
        "error_count": 0,
        "coverage_note_summary": "Selected public sample metadata only; not full-web or full-platform coverage.",
        "platform_label_summary": ["public_forum_label", "news_label"],
        "source_type_summary": ["public_post_label", "public_article_label"],
        "package_file_presence_map": {
            "manifest": True,
            "validation_report": True,
            "coverage_note": True,
            "evidence_items_jsonl": True,
            "evidence_items_csv": False,
            "source_manifest": True,
            "collection_log": True,
        },
        "manifest_present": True,
        "validation_report_present": True,
        "coverage_note_present": True,
        "evidence_items_jsonl_present": True,
        "evidence_items_csv_present": False,
        "source_manifest_present": True,
        "collection_log_present": True,
        "export_timestamp": "2026-07-06T00:00:00Z",
        "provider_attestation_summary": "Metadata-only package handoff; human review remains required.",
        "safety_markers": {
            "metadata_only": True,
            "row_content_included": False,
            "raw_identity_included": False,
            "secrets_included": False,
            "human_review_required": True,
            "no_automatic_trust_upgrade": True,
        },
        "metadata_only": True,
        "row_content_included": False,
        "raw_identity_included": False,
        "secrets_included": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "result_state": "metadata_schema_valid",
    }
    payload.update(overrides)
    return payload


def _build_correlation_summary(
    approval_phrase: str | None = APPROVAL_PHRASE,
    *,
    request_metadata: dict[str, object] | None = None,
    provider_result_metadata: dict[str, object] | None = None,
    existing_provider_result_ids: set[str] | None = None,
    output_overrides: dict[str, object] | None = None,
) -> dict[str, object]:
    if approval_phrase != APPROVAL_PHRASE:
        return _blocked_summary("missing_or_wrong_8z5_approval_phrase", correlation_created=False)

    request = request_metadata if request_metadata is not None else _safe_request_metadata()
    result = provider_result_metadata if provider_result_metadata is not None else _safe_provider_result_metadata()
    blockers = _request_blockers(request)
    blockers.extend(_provider_result_blockers(result))

    request_id = str(request.get("request_id", ""))
    result_request_id = str(result.get("request_id", ""))
    provider_result_id = str(result.get("provider_result_id", ""))
    existing_ids = existing_provider_result_ids or set()

    if request_id and result_request_id and request_id != result_request_id:
        blockers.append("request_id_mismatch")
    if provider_result_id and provider_result_id in existing_ids:
        blockers.append("duplicate_provider_result_id")

    if blockers:
        return _blocked_summary(*blockers, correlation_created=False)

    summary = {
        "status": "correlation_ready_for_manual_review",
        "correlation_status": "correlation_ready_for_manual_review",
        "request_result_correlation_created": True,
        "request_result_correlation_schema": CORRELATION_SCHEMA,
        "request_result_correlation_mode": CORRELATION_MODE,
        "request_metadata_schema": REQUEST_SCHEMA,
        "provider_result_metadata_schema": PROVIDER_RESULT_SCHEMA,
        "request_id_match": True,
        "request_id_present_in_request": True,
        "request_id_present_in_result": True,
        "provider_result_id_present": True,
        "provider_result_id_unique_in_fixture_scope": True,
        "package_name_present": True,
        "package_name_treated_as_opaque_identifier": True,
        "package_reference_policy": "opaque_safe_identifier_only",
        "metadata_only": True,
        "row_content_included": False,
        "raw_identity_included": False,
        "secrets_included": False,
        "request_result_correlation_performed": True,
        "correlation_does_not_create_case": True,
        "correlation_does_not_create_public_event": True,
        "correlation_does_not_create_evidence_layer_record": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "safe_counts": {
            "evidence_count": result["evidence_count"],
            "source_count": result["source_count"],
            "warning_count": result["warning_count"],
            "error_count": result["error_count"],
        },
        "safe_labels": {
            "request_id": request_id,
            "provider_result_id": provider_result_id,
            "case_id_hint": request["case_id_hint"],
            "event_slug": request["event_slug"],
            "package_name": result["package_name"],
        },
        "blockers": [],
        **FALSE_SIDE_EFFECTS,
    }
    if output_overrides:
        summary.update(output_overrides)
    output_blockers = _correlation_output_blockers(summary)
    if output_blockers:
        return _blocked_summary(*output_blockers, correlation_created=False)
    return summary


def _blocked_summary(*blockers: str, correlation_created: bool) -> dict[str, object]:
    return {
        "status": "blocked",
        "correlation_status": "blocked",
        "request_result_correlation_created": correlation_created,
        "request_result_correlation_schema": CORRELATION_SCHEMA,
        "request_result_correlation_mode": CORRELATION_MODE,
        "request_metadata_schema": REQUEST_SCHEMA,
        "provider_result_metadata_schema": PROVIDER_RESULT_SCHEMA,
        "request_id_match": False,
        "request_id_present_in_request": False,
        "request_id_present_in_result": False,
        "provider_result_id_present": False,
        "provider_result_id_unique_in_fixture_scope": False,
        "package_name_present": False,
        "package_name_treated_as_opaque_identifier": True,
        "package_reference_policy": "opaque_safe_identifier_only",
        "metadata_only": True,
        "row_content_included": False,
        "raw_identity_included": False,
        "secrets_included": False,
        "request_result_correlation_performed": False,
        "correlation_does_not_create_case": True,
        "correlation_does_not_create_public_event": True,
        "correlation_does_not_create_evidence_layer_record": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "blockers": list(blockers),
        **FALSE_SIDE_EFFECTS,
    }


def _request_blockers(request: dict[str, object]) -> list[str]:
    blockers: list[str] = []
    blockers.extend(_field_blockers(request, REQUEST_ALLOWED_FIELDS, "request"))
    if request.get("request_schema") != REQUEST_SCHEMA:
        blockers.append("unsupported_request_schema")
    request_id = str(request.get("request_id", ""))
    if not request_id:
        blockers.append("missing_request_id_in_request")
    elif _looks_path_like(request_id):
        blockers.append("path_like_request_id")
    if request.get("request_state") not in REQUEST_STATES:
        blockers.append("unsupported_request_state")
    for flag in REQUEST_REQUIRED_TRUE_FLAGS:
        if request.get(flag) is not True:
            blockers.append(f"request_{flag}_must_be_true")
    if "create production case" in str(request.get("case_id_hint", "")).lower():
        blockers.append("case_id_hint_must_remain_hint_only")
    if "public route" in str(request.get("event_slug", "")).lower():
        blockers.append("event_slug_must_remain_label_only")
    return blockers


def _provider_result_blockers(result: dict[str, object]) -> list[str]:
    blockers: list[str] = []
    blockers.extend(_field_blockers(result, RESULT_ALLOWED_FIELDS, "provider_result"))
    if result.get("provider_result_schema") != PROVIDER_RESULT_SCHEMA:
        blockers.append("unsupported_provider_result_schema")
    provider_result_id = str(result.get("provider_result_id", ""))
    if not provider_result_id:
        blockers.append("missing_provider_result_id")
    elif _looks_path_like(provider_result_id):
        blockers.append("path_like_provider_result_id")
    request_id = str(result.get("request_id", ""))
    if not request_id:
        blockers.append("missing_request_id_in_provider_result")
    elif _looks_path_like(request_id):
        blockers.append("path_like_request_id")
    for field_name in ("package_name", "package_reference_safe_id"):
        value = str(result.get(field_name, ""))
        if not value:
            blockers.append(f"missing_{field_name}")
        elif _looks_path_like(value):
            blockers.append(f"path_like_{field_name}")
    if result.get("package_reference_kind") != "opaque_safe_identifier_only":
        blockers.append("unsupported_package_reference_kind")
    if result.get("metadata_only") is not True:
        blockers.append("provider_result_metadata_only_must_be_true")
    for field_name in ("row_content_included", "raw_identity_included", "secrets_included"):
        if result.get(field_name) is not False:
            blockers.append(f"provider_result_{field_name}_must_be_false")
    for field_name in ("human_review_required", "no_automatic_trust_upgrade"):
        if result.get(field_name) is not True:
            blockers.append(f"provider_result_{field_name}_must_be_true")
    for field_name in (
        "evidence_items_jsonl_present",
        "evidence_items_csv_present",
        "source_manifest_present",
        "collection_log_present",
    ):
        if not isinstance(result.get(field_name), bool):
            blockers.append(f"{field_name}_must_be_boolean")
    presence_map = result.get("package_file_presence_map")
    if not isinstance(presence_map, dict):
        blockers.append("package_file_presence_map_must_be_object")
    else:
        for key, value in presence_map.items():
            if not isinstance(key, str) or not isinstance(value, bool):
                blockers.append(f"package_file_presence_map_entry_must_be_boolean:{key}")
    for field_name in ("validation_summary", "coverage_note_summary", "provider_attestation_summary"):
        if _contains_forbidden_text(str(result.get(field_name, ""))):
            blockers.append(f"{field_name}_contains_forbidden_content")
    if result.get("result_state") not in RESULT_STATES:
        blockers.append("unsupported_result_state")
    return blockers


def _field_blockers(payload: dict[str, object], allowed_fields: set[str], label: str) -> list[str]:
    blockers: list[str] = []
    for field_name in sorted(set(payload) - allowed_fields):
        blockers.append(f"{label}_unexpected_field:{field_name}")
    for field_name in sorted(field for field in payload if field.lower() in FORBIDDEN_FIELDS):
        blockers.append(f"{label}_forbidden_field:{field_name}")
    return blockers


def _correlation_output_blockers(summary: dict[str, object]) -> list[str]:
    blockers = [
        f"correlation_forbidden_field:{field_name}"
        for field_name in sorted(field for field in summary if field.lower() in FORBIDDEN_FIELDS)
    ]
    if summary.get("package_resolver_called") is not False:
        blockers.append("package_resolver_call_attempted")
    if summary.get("review_only_staging_created") is not False:
        blockers.append("review_only_staging_creation_attempted")
    if summary.get("review_only_staging_handoff_performed") is not False:
        blockers.append("review_only_staging_handoff_attempted")
    return blockers


def _contains_forbidden_text(value: str) -> bool:
    lowered = value.lower()
    return any(marker in lowered for marker in FORBIDDEN_TEXT_MARKERS)


def _looks_path_like(value: str) -> bool:
    return any(part in value for part in ("/", "\\", ":", ".."))


def test_8z5_exact_phrase_creates_safe_request_result_correlation_summary() -> None:
    summary = _build_correlation_summary()

    assert summary["status"] == "correlation_ready_for_manual_review"
    assert summary["request_result_correlation_created"] is True
    assert summary["request_result_correlation_schema"] == CORRELATION_SCHEMA
    assert summary["request_result_correlation_mode"] == CORRELATION_MODE
    assert summary["request_metadata_schema"] == REQUEST_SCHEMA
    assert summary["provider_result_metadata_schema"] == PROVIDER_RESULT_SCHEMA
    assert summary["request_id_match"] is True
    assert summary["request_id_present_in_request"] is True
    assert summary["request_id_present_in_result"] is True
    assert summary["provider_result_id_present"] is True
    assert summary["provider_result_id_unique_in_fixture_scope"] is True
    assert summary["package_name_present"] is True
    assert summary["package_name_treated_as_opaque_identifier"] is True
    assert summary["package_reference_policy"] == "opaque_safe_identifier_only"
    assert summary["metadata_only"] is True
    assert summary["row_content_included"] is False
    assert summary["raw_identity_included"] is False
    assert summary["secrets_included"] is False
    assert summary["request_result_correlation_performed"] is True
    assert summary["correlation_does_not_create_case"] is True
    assert summary["correlation_does_not_create_public_event"] is True
    assert summary["correlation_does_not_create_evidence_layer_record"] is True
    assert summary["human_review_required"] is True
    assert summary["no_automatic_trust_upgrade"] is True
    assert summary["safe_counts"] == {"evidence_count": 12, "source_count": 4, "warning_count": 1, "error_count": 0}
    assert summary["safe_labels"]["request_id"] == "request_8z5_fixture_001"
    assert summary["safe_labels"]["provider_result_id"] == "provider_result_8z5_fixture_001"
    for flag, expected_value in FALSE_SIDE_EFFECTS.items():
        assert summary[flag] is expected_value


def test_missing_or_wrong_phrase_blocks_before_correlation_creation() -> None:
    for phrase in (
        None,
        "",
        "wrong phrase",
        "APPROVE_8Z_4_CONTROLLED_ON_DEMAND_COLLECTOR_PROVIDER_RESULT_METADATA_FIXTURE_SMOKE",
        "APPROVE_8Z_3_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_METADATA_FIXTURE_SMOKE",
        "APPROVE_8Z_2_ON_DEMAND_COLLECTOR_REQUEST_RESULT_METADATA_CONTRACT_DOCS_ONLY",
        "APPROVE_8Z_1_ON_DEMAND_COLLECTOR_WORKFLOW_CONTRACT_DOCS_ONLY",
        "APPROVE_8W_70_REACTIVATION",
        "APPROVE_8Y_ROUTE_C_RUNTIME",
    ):
        summary = _build_correlation_summary(phrase)

        assert summary["status"] == "blocked"
        assert summary["request_result_correlation_created"] is False
        assert summary["request_result_correlation_performed"] is False
        assert summary["blockers"] == ["missing_or_wrong_8z5_approval_phrase"]


def test_request_id_must_be_present_and_match_exactly() -> None:
    missing_request = _build_correlation_summary(request_metadata=_safe_request_metadata(request_id=""))
    missing_result = _build_correlation_summary(provider_result_metadata=_safe_provider_result_metadata(request_id=""))
    mismatch = _build_correlation_summary(provider_result_metadata=_safe_provider_result_metadata(request_id="other"))

    assert "missing_request_id_in_request" in missing_request["blockers"]
    assert "missing_request_id_in_provider_result" in missing_result["blockers"]
    assert "request_id_mismatch" in mismatch["blockers"]


def test_duplicate_provider_result_id_blocks_automatic_correlation() -> None:
    summary = _build_correlation_summary(existing_provider_result_ids={"provider_result_8z5_fixture_001"})

    assert summary["status"] == "blocked"
    assert summary["request_result_correlation_created"] is False
    assert "duplicate_provider_result_id" in summary["blockers"]


def test_request_and_provider_result_forbidden_fields_block_correlation() -> None:
    for field_name in FORBIDDEN_FIELDS:
        if field_name == ".env":
            continue
        request_summary = _build_correlation_summary(request_metadata=_safe_request_metadata(**{field_name: "forbidden"}))
        result_summary = _build_correlation_summary(
            provider_result_metadata=_safe_provider_result_metadata(**{field_name: "forbidden"})
        )

        assert request_summary["status"] == "blocked"
        assert any(field_name in blocker for blocker in request_summary["blockers"])
        assert result_summary["status"] == "blocked"
        assert any(field_name in blocker for blocker in result_summary["blockers"])


def test_correlation_output_forbidden_field_blocks() -> None:
    summary = _build_correlation_summary(output_overrides={"target_user_list": ["forbidden"]})

    assert summary["status"] == "blocked"
    assert summary["request_result_correlation_created"] is False
    assert "correlation_forbidden_field:target_user_list" in summary["blockers"]


def test_request_safety_flags_must_remain_true() -> None:
    for field_name in REQUEST_REQUIRED_TRUE_FLAGS:
        summary = _build_correlation_summary(request_metadata=_safe_request_metadata(**{field_name: False}))

        assert summary["status"] == "blocked"
        assert f"request_{field_name}_must_be_true" in summary["blockers"]


def test_provider_result_safety_flags_must_remain_safe() -> None:
    cases = [
        ("metadata_only", False, "provider_result_metadata_only_must_be_true"),
        ("row_content_included", True, "provider_result_row_content_included_must_be_false"),
        ("raw_identity_included", True, "provider_result_raw_identity_included_must_be_false"),
        ("secrets_included", True, "provider_result_secrets_included_must_be_false"),
        ("human_review_required", False, "provider_result_human_review_required_must_be_true"),
        ("no_automatic_trust_upgrade", False, "provider_result_no_automatic_trust_upgrade_must_be_true"),
    ]

    for field_name, value, blocker in cases:
        summary = _build_correlation_summary(provider_result_metadata=_safe_provider_result_metadata(**{field_name: value}))

        assert summary["status"] == "blocked"
        assert blocker in summary["blockers"]


def test_identifiers_and_package_reference_must_not_be_paths() -> None:
    cases = [
        ("request", "request_id", "../request"),
        ("result", "request_id", "../request"),
        ("result", "provider_result_id", "../provider"),
        ("result", "package_name", "../package"),
        ("result", "package_reference_safe_id", "C:/private/package"),
    ]

    for payload_kind, field_name, value in cases:
        if payload_kind == "request":
            summary = _build_correlation_summary(request_metadata=_safe_request_metadata(**{field_name: value}))
        else:
            summary = _build_correlation_summary(provider_result_metadata=_safe_provider_result_metadata(**{field_name: value}))

        assert summary["status"] == "blocked"
        assert any(field_name in blocker for blocker in summary["blockers"])


def test_case_id_hint_and_event_slug_remain_non_production_labels() -> None:
    case_summary = _build_correlation_summary(
        request_metadata=_safe_request_metadata(case_id_hint="create production case")
    )
    event_summary = _build_correlation_summary(request_metadata=_safe_request_metadata(event_slug="create public route"))

    assert "case_id_hint_must_remain_hint_only" in case_summary["blockers"]
    assert "event_slug_must_remain_label_only" in event_summary["blockers"]


def test_presence_fields_and_summaries_remain_safe_metadata_only() -> None:
    non_boolean = _build_correlation_summary(
        provider_result_metadata=_safe_provider_result_metadata(evidence_items_jsonl_present="yes")
    )
    map_content = _build_correlation_summary(
        provider_result_metadata=_safe_provider_result_metadata(
            package_file_presence_map={"evidence_items_jsonl": "row content"}
        )
    )
    unsafe_summary = _build_correlation_summary(
        provider_result_metadata=_safe_provider_result_metadata(validation_summary="contains raw_author_id and secret")
    )

    assert "evidence_items_jsonl_present_must_be_boolean" in non_boolean["blockers"]
    assert "package_file_presence_map_entry_must_be_boolean:evidence_items_jsonl" in map_content["blockers"]
    assert "validation_summary_contains_forbidden_content" in unsafe_summary["blockers"]


def test_unsupported_request_or_result_state_blocks() -> None:
    request_state = _build_correlation_summary(request_metadata=_safe_request_metadata(request_state="runtime_ready"))
    result_state = _build_correlation_summary(provider_result_metadata=_safe_provider_result_metadata(result_state="runtime_ready"))

    assert "unsupported_request_state" in request_state["blockers"]
    assert "unsupported_result_state" in result_state["blockers"]


def test_package_resolver_and_staging_attempts_block() -> None:
    resolver_summary = _build_correlation_summary(output_overrides={"package_resolver_called": True})
    staging_summary = _build_correlation_summary(output_overrides={"review_only_staging_created": True})
    handoff_summary = _build_correlation_summary(output_overrides={"review_only_staging_handoff_performed": True})

    assert "package_resolver_call_attempted" in resolver_summary["blockers"]
    assert "review_only_staging_creation_attempted" in staging_summary["blockers"]
    assert "review_only_staging_handoff_attempted" in handoff_summary["blockers"]


def test_correlation_smoke_does_not_read_files(monkeypatch) -> None:
    attempted_reads: list[str] = []

    def fail_if_called(self, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        attempted_reads.append(str(self))
        raise AssertionError(f"unexpected file read: {self}")

    monkeypatch.setattr(Path, "read_text", fail_if_called)
    monkeypatch.setattr(Path, "read_bytes", fail_if_called)
    monkeypatch.setattr(Path, "open", fail_if_called)

    summary = _build_correlation_summary()

    assert summary["status"] == "correlation_ready_for_manual_review"
    assert attempted_reads == []
    assert summary["real_exchange_dir_read"] is False
    assert summary["real_package_dir_read"] is False
    assert summary["package_resolver_called"] is False
    assert summary["review_only_staging_created"] is False
    assert summary["review_only_staging_handoff_performed"] is False
    assert summary["evidence_items_jsonl_parsed"] is False
    assert summary["evidence_items_csv_parsed"] is False
    assert summary["source_manifest_rows_parsed"] is False
    assert summary["collection_log_rows_parsed"] is False
    assert summary["secrets_read"] is False
