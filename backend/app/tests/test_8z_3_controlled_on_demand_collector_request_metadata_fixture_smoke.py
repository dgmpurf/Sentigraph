from __future__ import annotations

from pathlib import Path

APPROVAL_PHRASE = "APPROVE_8Z_3_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_METADATA_FIXTURE_SMOKE"
REQUEST_SCHEMA = "sentigraph_on_demand_collection_request_metadata_v0_1"
REQUEST_MODE = "backend_only_local_on_demand_request_metadata_fixture"

ALLOWED_FIELDS = {
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

ALLOWED_STATES = {
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
    "secrets",
    ".env",
    "auto_execute",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
}

REQUIRED_TRUE_FLAGS = [
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
        "request_id": "request_8z3_fixture_001",
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
        "expected_output_contract": "sentigraph_on_demand_collector_provider_result_metadata_v0_1",
        "expected_package_role": "review_only_metadata_candidate",
        "operator_label": "local_operator_label",
        "request_created_at": "2026-07-06T00:00:00Z",
        "request_created_by_label": "sentigraph_local_test",
        "safety_constraints": [
            "no collector execution",
            "no provider job",
            "no secrets",
            "no cookies or browser profiles",
            "no Sentigraph live fetch",
            "no URL scraping",
            "human review required",
        ],
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


def _build_request_metadata_fixture(
    approval_phrase: str | None = APPROVAL_PHRASE,
    *,
    metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    if approval_phrase != APPROVAL_PHRASE:
        return _blocked_summary("missing_or_wrong_8z3_approval_phrase", fixture_created=False)

    request_metadata = metadata if metadata is not None else _safe_request_metadata()
    blockers = _request_metadata_blockers(request_metadata)
    if blockers:
        return _blocked_summary(*blockers, fixture_created=False)

    return {
        "status": "fixture_ready",
        "request_metadata_fixture_created": True,
        "request_metadata_schema": REQUEST_SCHEMA,
        "request_metadata_mode": REQUEST_MODE,
        "metadata_only": True,
        "request_metadata": request_metadata,
        "blockers": [],
        **FALSE_SIDE_EFFECTS,
    }


def _blocked_summary(*blockers: str, fixture_created: bool) -> dict[str, object]:
    return {
        "status": "blocked",
        "request_metadata_fixture_created": fixture_created,
        "request_metadata_schema": REQUEST_SCHEMA,
        "request_metadata_mode": REQUEST_MODE,
        "metadata_only": True,
        "request_metadata": None,
        "blockers": list(blockers),
        **FALSE_SIDE_EFFECTS,
    }


def _request_metadata_blockers(metadata: dict[str, object]) -> list[str]:
    blockers: list[str] = []
    fields = set(metadata)
    unexpected_fields = fields - ALLOWED_FIELDS
    forbidden_fields = {field for field in fields if field.lower() in FORBIDDEN_FIELDS}

    if unexpected_fields:
        blockers.extend(f"unexpected_field:{field}" for field in sorted(unexpected_fields))
    if forbidden_fields:
        blockers.extend(f"forbidden_field:{field}" for field in sorted(forbidden_fields))
    if not metadata.get("request_id"):
        blockers.append("missing_request_id")
    if _looks_path_like(str(metadata.get("request_id", ""))):
        blockers.append("path_like_request_id")
    if metadata.get("request_schema") != REQUEST_SCHEMA:
        blockers.append("unsupported_request_schema")
    if metadata.get("request_state") not in ALLOWED_STATES:
        blockers.append("unsupported_request_state")
    for flag in REQUIRED_TRUE_FLAGS:
        if metadata.get(flag) is not True:
            blockers.append(f"{flag}_must_be_true")
    topic_query = str(metadata.get("topic_query_safe_text", "")).lower()
    if "sentigraph" in topic_query and any(term in topic_query for term in ("fetch", "scrape", "crawl")):
        blockers.append("topic_query_directs_sentigraph_live_fetch_or_scrape")
    if "public route" in str(metadata.get("event_slug", "")).lower():
        blockers.append("event_slug_must_remain_label_only")
    if "create production case" in str(metadata.get("case_id_hint", "")).lower():
        blockers.append("case_id_hint_must_remain_hint_only")
    safety_constraints = metadata.get("safety_constraints")
    safety_text = " ".join(str(item).lower() for item in safety_constraints) if isinstance(safety_constraints, list) else ""
    for required_text in ("no collector execution", "no secrets", "no sentigraph live fetch"):
        if required_text not in safety_text:
            blockers.append(f"missing_safety_constraint:{required_text}")
    return blockers


def _looks_path_like(value: str) -> bool:
    return any(part in value for part in ("/", "\\", ":", ".."))


def test_8z3_exact_phrase_creates_safe_metadata_fixture() -> None:
    summary = _build_request_metadata_fixture()

    assert summary["status"] == "fixture_ready"
    assert summary["request_metadata_fixture_created"] is True
    assert summary["request_metadata_schema"] == REQUEST_SCHEMA
    assert summary["request_metadata_mode"] == REQUEST_MODE
    assert summary["metadata_only"] is True
    metadata = summary["request_metadata"]
    assert isinstance(metadata, dict)
    assert metadata["request_state"] in ALLOWED_STATES
    assert metadata["request_id"] == "request_8z3_fixture_001"
    assert metadata["case_id_hint"] == "case_hint_label_only"
    assert metadata["event_slug"] == "event-slug-label-only"
    assert "Sentigraph live fetch" not in metadata["topic_query_safe_text"]
    assert metadata["requested_platform_labels"] == ["public_forum_label", "news_label"]
    for flag in REQUIRED_TRUE_FLAGS:
        assert metadata[flag] is True
    for field in metadata:
        assert field in ALLOWED_FIELDS
    for flag, expected_value in FALSE_SIDE_EFFECTS.items():
        assert summary[flag] is expected_value


def test_missing_or_wrong_phrase_blocks_before_fixture_creation() -> None:
    for phrase in (
        None,
        "",
        "wrong phrase",
        "APPROVE_8Z_2_ON_DEMAND_COLLECTOR_REQUEST_RESULT_METADATA_CONTRACT_DOCS_ONLY",
        "APPROVE_8Z_1_ON_DEMAND_COLLECTOR_WORKFLOW_CONTRACT_DOCS_ONLY",
        "APPROVE_8W_70_REACTIVATION",
        "APPROVE_8Y_ROUTE_C_RUNTIME",
    ):
        summary = _build_request_metadata_fixture(phrase)

        assert summary["status"] == "blocked"
        assert summary["request_metadata_fixture_created"] is False
        assert summary["request_metadata"] is None
        assert summary["blockers"] == ["missing_or_wrong_8z3_approval_phrase"]


def test_forbidden_metadata_field_blocks_fixture_creation() -> None:
    for field_name in FORBIDDEN_FIELDS:
        if field_name == ".env":
            continue
        metadata = _safe_request_metadata(**{field_name: "forbidden"})
        summary = _build_request_metadata_fixture(metadata=metadata)

        assert summary["status"] == "blocked"
        assert summary["request_metadata_fixture_created"] is False
        assert any(field_name in blocker for blocker in summary["blockers"])


def test_required_true_safety_flags_must_remain_true() -> None:
    for flag in REQUIRED_TRUE_FLAGS:
        metadata = _safe_request_metadata(**{flag: False})
        summary = _build_request_metadata_fixture(metadata=metadata)

        assert summary["status"] == "blocked"
        assert summary["request_metadata_fixture_created"] is False
        assert f"{flag}_must_be_true" in summary["blockers"]


def test_request_metadata_blocks_live_fetch_or_scrape_semantics() -> None:
    metadata = _safe_request_metadata(topic_query_safe_text="Tell Sentigraph to fetch and scrape this URL now.")

    summary = _build_request_metadata_fixture(metadata=metadata)

    assert summary["status"] == "blocked"
    assert summary["request_metadata_fixture_created"] is False
    assert "topic_query_directs_sentigraph_live_fetch_or_scrape" in summary["blockers"]


def test_event_slug_and_case_hint_remain_labels_only() -> None:
    event_slug_summary = _build_request_metadata_fixture(
        metadata=_safe_request_metadata(event_slug="create public route for this event")
    )
    case_hint_summary = _build_request_metadata_fixture(
        metadata=_safe_request_metadata(case_id_hint="create production case from this hint")
    )

    assert event_slug_summary["status"] == "blocked"
    assert "event_slug_must_remain_label_only" in event_slug_summary["blockers"]
    assert case_hint_summary["status"] == "blocked"
    assert "case_id_hint_must_remain_hint_only" in case_hint_summary["blockers"]


def test_unsupported_state_and_bad_request_id_block_fixture_creation() -> None:
    unsupported_state = _build_request_metadata_fixture(metadata=_safe_request_metadata(request_state="runtime_ready"))
    missing_request_id = _build_request_metadata_fixture(metadata=_safe_request_metadata(request_id=""))
    path_like_request_id = _build_request_metadata_fixture(metadata=_safe_request_metadata(request_id="../package/path"))

    assert unsupported_state["status"] == "blocked"
    assert "unsupported_request_state" in unsupported_state["blockers"]
    assert missing_request_id["status"] == "blocked"
    assert "missing_request_id" in missing_request_id["blockers"]
    assert path_like_request_id["status"] == "blocked"
    assert "path_like_request_id" in path_like_request_id["blockers"]


def test_fixture_smoke_does_not_read_row_or_secret_files(monkeypatch) -> None:
    attempted_reads: list[str] = []

    def fail_if_called(self, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003
        attempted_reads.append(str(self))
        raise AssertionError(f"unexpected file read: {self}")

    monkeypatch.setattr(Path, "read_text", fail_if_called)
    monkeypatch.setattr(Path, "read_bytes", fail_if_called)
    monkeypatch.setattr(Path, "open", fail_if_called)

    summary = _build_request_metadata_fixture()

    assert summary["status"] == "fixture_ready"
    assert attempted_reads == []
    assert summary["real_exchange_dir_read"] is False
    assert summary["real_package_dir_read"] is False
    assert summary["evidence_items_jsonl_parsed"] is False
    assert summary["evidence_items_csv_parsed"] is False
    assert summary["source_manifest_rows_parsed"] is False
    assert summary["collection_log_rows_parsed"] is False
    assert summary["secrets_read"] is False
