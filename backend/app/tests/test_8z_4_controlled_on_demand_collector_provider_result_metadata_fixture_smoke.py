from __future__ import annotations

from pathlib import Path

APPROVAL_PHRASE = "APPROVE_8Z_4_CONTROLLED_ON_DEMAND_COLLECTOR_PROVIDER_RESULT_METADATA_FIXTURE_SMOKE"
PROVIDER_RESULT_SCHEMA = "sentigraph_on_demand_collector_provider_result_metadata_v0_1"
PROVIDER_RESULT_MODE = "backend_only_local_on_demand_provider_result_metadata_fixture"

ALLOWED_FIELDS = {
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

ALLOWED_STATES = {
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
    "raw_evidence_row_contents",
    "raw_comment_dumps",
    "full_evidence_items_content",
    "raw_author_id",
    "raw_author_ids",
    "raw_author_name",
    "raw_author_names",
    "profile_url",
    "profile_urls",
    "private_messages",
    "cookie",
    "cookies",
    "session",
    "sessions",
    "token",
    "tokens",
    "password",
    "passwords",
    "api_key",
    "api_keys",
    "browser_profile_path",
    "browser_profile_paths",
    "proxy_credentials",
    "absolute_private_paths",
    "source_manifest_row_contents",
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

REQUIRED_FALSE_FLAGS = {
    "row_content_included": False,
    "raw_identity_included": False,
    "secrets_included": False,
}

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
    "request_result_correlation_performed": False,
    "request_result_correlation_deferred_to_8z5": True,
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


def _safe_provider_result_metadata(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "provider_result_id": "provider_result_8z4_fixture_001",
        "provider_result_schema": PROVIDER_RESULT_SCHEMA,
        "request_id": "request_8z3_fixture_001",
        "provider_job_id": "external_job_label_only",
        "external_collector_label": "external_collector_label_only",
        "collector_project_label": "collector_project_label_only",
        "package_name": "safe_selected_sample_package",
        "package_role": "review_only_metadata_candidate",
        "package_schema_version": "0.1",
        "package_reference_kind": "opaque_safe_identifier_only",
        "package_reference_safe_id": "package_ref_8z4_fixture_001",
        "validation_status": "validation_warn",
        "validation_summary": "Safe metadata summary only; row content is not included.",
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


def _build_provider_result_metadata_fixture(
    approval_phrase: str | None = APPROVAL_PHRASE,
    *,
    metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    if approval_phrase != APPROVAL_PHRASE:
        return _blocked_summary("missing_or_wrong_8z4_approval_phrase", fixture_created=False)

    provider_result_metadata = metadata if metadata is not None else _safe_provider_result_metadata()
    blockers = _provider_result_metadata_blockers(provider_result_metadata)
    if blockers:
        return _blocked_summary(*blockers, fixture_created=False)

    return {
        "status": "fixture_ready",
        "provider_result_metadata_fixture_created": True,
        "provider_result_metadata_schema": PROVIDER_RESULT_SCHEMA,
        "provider_result_metadata_mode": PROVIDER_RESULT_MODE,
        "metadata_only": True,
        "provider_result_metadata": provider_result_metadata,
        "request_id_present": True,
        "package_reference_policy": "opaque_safe_identifier_only",
        "package_file_presence_map_mode": "boolean_presence_only",
        "blockers": [],
        **FALSE_SIDE_EFFECTS,
    }


def _blocked_summary(*blockers: str, fixture_created: bool) -> dict[str, object]:
    return {
        "status": "blocked",
        "provider_result_metadata_fixture_created": fixture_created,
        "provider_result_metadata_schema": PROVIDER_RESULT_SCHEMA,
        "provider_result_metadata_mode": PROVIDER_RESULT_MODE,
        "metadata_only": True,
        "provider_result_metadata": None,
        "request_id_present": False,
        "package_reference_policy": "opaque_safe_identifier_only",
        "package_file_presence_map_mode": "boolean_presence_only",
        "blockers": list(blockers),
        **FALSE_SIDE_EFFECTS,
    }


def _provider_result_metadata_blockers(metadata: dict[str, object]) -> list[str]:
    blockers: list[str] = []
    fields = set(metadata)
    unexpected_fields = fields - ALLOWED_FIELDS
    forbidden_fields = {field for field in fields if field.lower() in FORBIDDEN_FIELDS}

    if unexpected_fields:
        blockers.extend(f"unexpected_field:{field}" for field in sorted(unexpected_fields))
    if forbidden_fields:
        blockers.extend(f"forbidden_field:{field}" for field in sorted(forbidden_fields))
    if not metadata.get("provider_result_id"):
        blockers.append("missing_provider_result_id")
    if _looks_path_like(str(metadata.get("provider_result_id", ""))):
        blockers.append("path_like_provider_result_id")
    if not metadata.get("request_id"):
        blockers.append("missing_request_id")
    if metadata.get("provider_result_schema") != PROVIDER_RESULT_SCHEMA:
        blockers.append("unsupported_provider_result_schema")
    if metadata.get("result_state") not in ALLOWED_STATES:
        blockers.append("unsupported_result_state")
    if metadata.get("metadata_only") is not True:
        blockers.append("metadata_only_must_be_true")
    for field_name, expected_value in REQUIRED_FALSE_FLAGS.items():
        if metadata.get(field_name) is not expected_value:
            blockers.append(f"{field_name}_must_be_false")
    for field_name in ("human_review_required", "no_automatic_trust_upgrade"):
        if metadata.get(field_name) is not True:
            blockers.append(f"{field_name}_must_be_true")
    for field_name in ("package_name", "package_reference_safe_id"):
        value = str(metadata.get(field_name, ""))
        if not value:
            blockers.append(f"missing_{field_name}")
        elif _looks_path_like(value):
            blockers.append(f"path_like_{field_name}")
    if metadata.get("package_reference_kind") != "opaque_safe_identifier_only":
        blockers.append("unsupported_package_reference_kind")
    for field_name in (
        "evidence_items_jsonl_present",
        "evidence_items_csv_present",
        "source_manifest_present",
        "collection_log_present",
        "manifest_present",
        "validation_report_present",
        "coverage_note_present",
    ):
        if not isinstance(metadata.get(field_name), bool):
            blockers.append(f"{field_name}_must_be_boolean")
    blockers.extend(_presence_map_blockers(metadata.get("package_file_presence_map")))
    for field_name in ("validation_summary", "coverage_note_summary", "provider_attestation_summary"):
        text = str(metadata.get(field_name, "")).lower()
        if any(marker in text for marker in FORBIDDEN_TEXT_MARKERS):
            blockers.append(f"{field_name}_contains_forbidden_content")
    blockers.extend(_safety_marker_blockers(metadata.get("safety_markers")))
    return blockers


def _presence_map_blockers(value: object) -> list[str]:
    if not isinstance(value, dict):
        return ["package_file_presence_map_must_be_object"]
    blockers: list[str] = []
    for key, entry in value.items():
        if not isinstance(key, str):
            blockers.append("package_file_presence_map_key_must_be_string")
        if not isinstance(entry, bool):
            blockers.append(f"package_file_presence_map_value_must_be_boolean:{key}")
    return blockers


def _safety_marker_blockers(value: object) -> list[str]:
    if not isinstance(value, dict):
        return ["safety_markers_must_be_object"]
    expected_markers = {
        "metadata_only": True,
        "row_content_included": False,
        "raw_identity_included": False,
        "secrets_included": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
    }
    return [
        f"safety_marker_{field_name}_mismatch"
        for field_name, expected_value in expected_markers.items()
        if value.get(field_name) is not expected_value
    ]


def _looks_path_like(value: str) -> bool:
    return any(part in value for part in ("/", "\\", ":", ".."))


def test_8z4_exact_phrase_creates_safe_provider_result_metadata_fixture() -> None:
    summary = _build_provider_result_metadata_fixture()

    assert summary["status"] == "fixture_ready"
    assert summary["provider_result_metadata_fixture_created"] is True
    assert summary["provider_result_metadata_schema"] == PROVIDER_RESULT_SCHEMA
    assert summary["provider_result_metadata_mode"] == PROVIDER_RESULT_MODE
    assert summary["metadata_only"] is True
    assert summary["request_id_present"] is True
    assert summary["request_result_correlation_performed"] is False
    assert summary["request_result_correlation_deferred_to_8z5"] is True
    assert summary["package_reference_policy"] == "opaque_safe_identifier_only"
    assert summary["package_file_presence_map_mode"] == "boolean_presence_only"
    metadata = summary["provider_result_metadata"]
    assert isinstance(metadata, dict)
    assert metadata["provider_result_id"] == "provider_result_8z4_fixture_001"
    assert metadata["request_id"] == "request_8z3_fixture_001"
    assert metadata["package_name"] == "safe_selected_sample_package"
    assert metadata["package_reference_kind"] == "opaque_safe_identifier_only"
    assert metadata["package_reference_safe_id"] == "package_ref_8z4_fixture_001"
    assert metadata["validation_status"] == "validation_warn"
    assert metadata["result_state"] in ALLOWED_STATES
    assert isinstance(metadata["package_file_presence_map"], dict)
    assert all(isinstance(value, bool) for value in metadata["package_file_presence_map"].values())
    for field_name in (
        "evidence_items_jsonl_present",
        "evidence_items_csv_present",
        "source_manifest_present",
        "collection_log_present",
    ):
        assert isinstance(metadata[field_name], bool)
    assert metadata["safety_markers"]["metadata_only"] is True
    assert metadata["safety_markers"]["row_content_included"] is False
    assert metadata["safety_markers"]["raw_identity_included"] is False
    assert metadata["safety_markers"]["secrets_included"] is False
    assert metadata["safety_markers"]["human_review_required"] is True
    assert metadata["safety_markers"]["no_automatic_trust_upgrade"] is True
    for field in metadata:
        assert field in ALLOWED_FIELDS
    for flag, expected_value in FALSE_SIDE_EFFECTS.items():
        assert summary[flag] is expected_value


def test_missing_or_wrong_phrase_blocks_before_fixture_creation() -> None:
    for phrase in (
        None,
        "",
        "wrong phrase",
        "APPROVE_8Z_3_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_METADATA_FIXTURE_SMOKE",
        "APPROVE_8Z_2_ON_DEMAND_COLLECTOR_REQUEST_RESULT_METADATA_CONTRACT_DOCS_ONLY",
        "APPROVE_8Z_1_ON_DEMAND_COLLECTOR_WORKFLOW_CONTRACT_DOCS_ONLY",
        "APPROVE_8W_70_REACTIVATION",
        "APPROVE_8Y_ROUTE_C_RUNTIME",
    ):
        summary = _build_provider_result_metadata_fixture(phrase)

        assert summary["status"] == "blocked"
        assert summary["provider_result_metadata_fixture_created"] is False
        assert summary["provider_result_metadata"] is None
        assert summary["blockers"] == ["missing_or_wrong_8z4_approval_phrase"]


def test_forbidden_metadata_fields_block_fixture_creation() -> None:
    for field_name in FORBIDDEN_FIELDS:
        metadata = _safe_provider_result_metadata(**{field_name: "forbidden"})
        summary = _build_provider_result_metadata_fixture(metadata=metadata)

        assert summary["status"] == "blocked"
        assert summary["provider_result_metadata_fixture_created"] is False
        assert any(field_name in blocker for blocker in summary["blockers"])


def test_required_metadata_and_safety_flags_are_enforced() -> None:
    cases = [
        ("metadata_only", False, "metadata_only_must_be_true"),
        ("row_content_included", True, "row_content_included_must_be_false"),
        ("raw_identity_included", True, "raw_identity_included_must_be_false"),
        ("secrets_included", True, "secrets_included_must_be_false"),
        ("human_review_required", False, "human_review_required_must_be_true"),
        ("no_automatic_trust_upgrade", False, "no_automatic_trust_upgrade_must_be_true"),
    ]

    for field_name, value, blocker in cases:
        summary = _build_provider_result_metadata_fixture(metadata=_safe_provider_result_metadata(**{field_name: value}))

        assert summary["status"] == "blocked"
        assert summary["provider_result_metadata_fixture_created"] is False
        assert blocker in summary["blockers"]


def test_package_identifiers_must_remain_opaque_safe_identifiers() -> None:
    cases = [
        ("package_name", "../package"),
        ("package_name", "C:/private/package"),
        ("package_reference_safe_id", "../package"),
        ("package_reference_safe_id", "C:/private/package"),
        ("provider_result_id", "../provider-result"),
    ]

    for field_name, value in cases:
        summary = _build_provider_result_metadata_fixture(metadata=_safe_provider_result_metadata(**{field_name: value}))

        assert summary["status"] == "blocked"
        assert any(field_name in blocker for blocker in summary["blockers"])


def test_presence_fields_and_package_file_presence_map_are_boolean_only() -> None:
    for field_name in (
        "evidence_items_jsonl_present",
        "evidence_items_csv_present",
        "source_manifest_present",
        "collection_log_present",
    ):
        summary = _build_provider_result_metadata_fixture(metadata=_safe_provider_result_metadata(**{field_name: "yes"}))

        assert summary["status"] == "blocked"
        assert f"{field_name}_must_be_boolean" in summary["blockers"]

    map_summary = _build_provider_result_metadata_fixture(
        metadata=_safe_provider_result_metadata(package_file_presence_map={"evidence_items_jsonl": "raw row content"})
    )

    assert map_summary["status"] == "blocked"
    assert "package_file_presence_map_value_must_be_boolean:evidence_items_jsonl" in map_summary["blockers"]


def test_summary_text_blocks_raw_rows_identities_and_secrets() -> None:
    for field_name in ("validation_summary", "coverage_note_summary", "provider_attestation_summary"):
        summary = _build_provider_result_metadata_fixture(
            metadata=_safe_provider_result_metadata(**{field_name: "contains raw_author_id and secret"})
        )

        assert summary["status"] == "blocked"
        assert f"{field_name}_contains_forbidden_content" in summary["blockers"]


def test_unsupported_state_and_missing_identifiers_block_fixture_creation() -> None:
    unsupported_state = _build_provider_result_metadata_fixture(
        metadata=_safe_provider_result_metadata(result_state="runtime_ready")
    )
    missing_provider_result_id = _build_provider_result_metadata_fixture(
        metadata=_safe_provider_result_metadata(provider_result_id="")
    )
    missing_request_id = _build_provider_result_metadata_fixture(metadata=_safe_provider_result_metadata(request_id=""))

    assert unsupported_state["status"] == "blocked"
    assert "unsupported_result_state" in unsupported_state["blockers"]
    assert missing_provider_result_id["status"] == "blocked"
    assert "missing_provider_result_id" in missing_provider_result_id["blockers"]
    assert missing_request_id["status"] == "blocked"
    assert "missing_request_id" in missing_request_id["blockers"]


def test_request_result_correlation_is_deferred_to_8z5() -> None:
    summary = _build_provider_result_metadata_fixture(
        metadata=_safe_provider_result_metadata(request_id="opaque_request_id_not_compared_here")
    )

    assert summary["status"] == "fixture_ready"
    assert summary["request_result_correlation_performed"] is False
    assert summary["request_result_correlation_deferred_to_8z5"] is True


def test_fixture_smoke_does_not_read_package_rows_or_secret_files(monkeypatch) -> None:
    attempted_reads: list[str] = []

    def fail_if_called(self, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        attempted_reads.append(str(self))
        raise AssertionError(f"unexpected file read: {self}")

    monkeypatch.setattr(Path, "read_text", fail_if_called)
    monkeypatch.setattr(Path, "read_bytes", fail_if_called)
    monkeypatch.setattr(Path, "open", fail_if_called)

    summary = _build_provider_result_metadata_fixture()

    assert summary["status"] == "fixture_ready"
    assert attempted_reads == []
    assert summary["real_exchange_dir_read"] is False
    assert summary["real_package_dir_read"] is False
    assert summary["package_resolver_called"] is False
    assert summary["review_only_staging_created"] is False
    assert summary["evidence_items_jsonl_parsed"] is False
    assert summary["evidence_items_csv_parsed"] is False
    assert summary["source_manifest_rows_parsed"] is False
    assert summary["collection_log_rows_parsed"] is False
    assert summary["secrets_read"] is False
