from __future__ import annotations

import json
from importlib import import_module
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]

EXPECTED_APPROVAL_PHRASE = (
    "APPROVE_9A_11_CONTROLLED_NON_AUTHORIZING_EVIDENCE_LAYER_WRITE_PRODUCTION_"
    "EVIDENCEITEM_HUMAN_AUTHORITY_DECLARATION_FIXTURE_SMOKE"
)
DECLARATION_SCHEMA = "sentigraph_actual_evidence_layer_write_human_authority_declaration_v0_1"
DECLARATION_SCOPE = "local_non_authorizing_fixture"
DECLARATION_MODE = "backend_only_local_non_authorizing_human_authority_declaration_fixture"
READY_STATUS = "declaration_fixture_ready_for_human_review_non_authorizing"
BLOCKED_STATUS = "declaration_fixture_blocked"

NEIGHBOR_PHRASES = [
    "APPROVE_9A_8_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_HUMAN_AUTHORITY_MANUAL_REVIEW_RESPONSIBILITY_DECLARATION_GATE_DOCS_ONLY",
    "APPROVE_9A_9_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_HUMAN_AUTHORITY_DECLARATION_SAFETY_CONTRACT_TESTS_ONLY",
    "APPROVE_9A_10_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_DECLARATION_SAFETY_COMPLETION_ACTUAL_WRITE_AUTHORIZATION_READINESS_GATE_DECISION_DOCS_ONLY",
    "APPROVE_9A_6_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_HUMAN_AUTHORITY_FINAL_AUTHORIZATION_PROTOCOL_TESTS_ONLY",
    "APPROVE_8W_28_CONTROLLED_EVIDENCEITEM_EVIDENCE_LAYER_WRITE_RUNTIME_IMPLEMENTATION",
    "APPROVE_GENERIC_WRITE_AUTHORIZATION",
]

FALSE_FLAGS = [
    "actual_write_authorized",
    "production_evidenceitem_creation_authorized",
    "ready_for_actual_write",
    "human_authority_validated",
    "manual_review_responsibility_accepted",
    "final_write_authorization_performed",
    "actual_evidence_layer_write_approved",
    "actual_evidence_layer_write_performed",
    "persisted_evidence_layer_record_created",
    "production_evidenceitem_created",
    "write_authorization_object_created_that_permits_write",
    "runtime_human_authority_validation_performed",
    "runtime_manual_review_responsibility_acceptance_performed",
    "evidenceitem_write_runtime_called",
    "review_queue_runtime_used",
    "production_case_created",
    "production_analysis_run_created",
    "actual_analysis_execution_started",
    "production_analysis_result_authorized",
    "production_analysis_result_created",
    "source11_runtime_called",
    "finalsummaryreport_runtime_called",
    "public_delivery_created",
]

FORBIDDEN_FIELDS = [
    "raw_rows",
    "raw_comments",
    "raw_author_id",
    "raw_author_ids",
    "raw_author_name",
    "raw_author_names",
    "author_id",
    "author_name",
    "profile_url",
    "private_message",
    "private_messages",
    "secret",
    "secrets",
    "token",
    "tokens",
    "cookie",
    "cookies",
    "session",
    "sessions",
    "salt",
    "salts",
    "password",
    "passwords",
    ".env",
    "absolute_path",
    "package_path",
    "production_package_rows",
    "evidence_items_jsonl_contents",
    "evidence_items_csv_contents",
    "source_manifest_row_contents",
    "collection_log_row_contents",
    "write_execution_payload",
    "route_api_frontend_trigger_payload",
    "production_case_payload",
    "production_analysis_run_payload",
    "production_analysis_result_payload",
    "source11_payload",
    "finalsummaryreport_payload",
    "export_download_public_final_delivery_payload",
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
]

UNSAFE_IDENTITY_FIELDS = [
    "legal name",
    "personal address",
    "phone number",
    "personal email",
    "government ID",
    "credential token",
    "signature image",
    "private proof files",
    "raw PII",
]

FORBIDDEN_SENTINELS = [
    "actual-token-should-never-appear",
    "actual-cookie-should-never-appear",
    "actual-secret-should-never-appear",
    "actual-raw-author-should-never-appear",
    "actual-author-name-should-never-appear",
    "actual-profile-url-should-never-appear",
    "actual-raw-comment-should-never-appear",
    "G:/private-collector/should-never-appear",
    "C:/Users/msjpurf/private-collector/should-never-appear",
    "donglu_sunjihai_youth_football/donglu-sunjihai-youth-football-202606-v2_20260617_121016",
]

FORBIDDEN_OUTPUT_TOKENS = [
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "write_execution_payload",
    "production_case_payload",
    "production_analysis_run_payload",
    "production_analysis_result_payload",
    "source11_payload",
    "finalsummaryreport_payload",
]

FORBIDDEN_SERVICE_IMPORTS = [
    "controlled_evidenceitem_evidence_layer_write_runtime",
    "evidence_import",
    "evidence_ingestion",
    "review_queue",
    "production_case",
    "production_analysis_run",
    "source11",
    "finalsummaryreport",
]


def _service_module():
    return import_module("app.services.evidence_layer_write_human_authority_declaration_fixture")


def _safe_fixture(**overrides: object) -> dict[str, object]:
    fixture: dict[str, object] = {
        "human_authority_identity_label": "not_validated_by_codex",
        "authority_basis": "not_validated_by_codex",
        "manual_review_responsibility_label": "not_accepted_by_codex",
        "warning_count_acknowledgment": "required_later",
        "human_review_required_acknowledgment": "required_later",
        "no_automatic_trust_upgrade_acknowledgment": "required_later",
        "blocker_review_status": "blocked_until_separate_final_authorization",
        "risk_review_status": "human_required_later",
        "lineage_review_status": "safe_label_lineage_only",
        "raw_private_secret_absence_acknowledgment": "required_later",
        "rollback_pause_responsibility": "required_later",
    }
    fixture.update(overrides)
    return fixture


def _build(fixture: dict[str, object] | None = None) -> dict[str, object]:
    return _service_module().build_non_authorizing_human_authority_declaration_fixture(
        fixture or _safe_fixture(),
        exact_approval_phrase=EXPECTED_APPROVAL_PHRASE,
    )


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _assert_safe_serialized(value: object) -> None:
    serialized = _serialized(value)
    for token in FORBIDDEN_OUTPUT_TOKENS:
        assert token not in serialized
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel not in serialized
    assert ":/" not in serialized
    assert ":\\" not in serialized


def test_exact_9a11_phrase_is_required_and_neighbor_phrases_are_rejected() -> None:
    service = _service_module()
    assert service.APPROVAL_PHRASE == EXPECTED_APPROVAL_PHRASE

    with pytest.raises(ValueError, match="blocked_missing_exact_approval"):
        service.build_non_authorizing_human_authority_declaration_fixture(
            _safe_fixture(),
            exact_approval_phrase=None,
        )

    for phrase in ["APPROVE_WRONG_NON_AUTHORIZING_DECLARATION", *NEIGHBOR_PHRASES]:
        with pytest.raises(ValueError, match="blocked_wrong_exact_approval"):
            service.build_non_authorizing_human_authority_declaration_fixture(
                _safe_fixture(),
                exact_approval_phrase=phrase,
            )


def test_safe_in_memory_input_builds_versioned_non_authorizing_declaration_fixture() -> None:
    declaration = _build()

    assert declaration["declaration_schema"] == DECLARATION_SCHEMA
    assert declaration["declaration_scope"] == DECLARATION_SCOPE
    assert declaration["declaration_mode"] == DECLARATION_MODE
    assert declaration["declaration_status"] == BLOCKED_STATUS
    assert declaration["declaration_id"].startswith("non-authorizing-human-authority-declaration-")
    assert declaration["human_authority_identity_label"] == "not_validated_by_codex"
    assert declaration["authority_basis"] == "not_validated_by_codex"
    assert declaration["manual_review_responsibility_label"] == "not_accepted_by_codex"
    assert declaration["warning_count_acknowledgment"] == "required_later"
    assert declaration["human_review_required_acknowledgment"] == "required_later"
    assert declaration["no_automatic_trust_upgrade_acknowledgment"] == "required_later"
    assert declaration["blocker_review_status"] == "blocked_until_separate_final_authorization"
    assert declaration["risk_review_status"] == "human_required_later"
    assert declaration["lineage_review_status"] == "safe_label_lineage_only"
    assert declaration["raw_private_secret_absence_acknowledgment"] == "required_later"
    assert declaration["rollback_pause_responsibility"] == "required_later"
    _assert_safe_serialized(declaration)


def test_status_is_non_authorizing_and_all_write_production_runtime_flags_are_false() -> None:
    declaration = _build(_safe_fixture(blocker_review_status="no_blockers_in_fixture"))

    assert declaration["declaration_status"] == READY_STATUS
    assert declaration["final_write_authorization_still_required"] is True
    for flag in FALSE_FLAGS:
        assert declaration[flag] is False, flag


@pytest.mark.parametrize("field_name", [*FORBIDDEN_FIELDS, *UNSAFE_IDENTITY_FIELDS])
def test_recursive_forbidden_field_scanner_blocks_raw_private_secret_path_pii_and_payload_fields(
    field_name: str,
) -> None:
    fixture = _safe_fixture(nested={"safe_container": {field_name: "actual-secret-should-never-appear"}})

    with pytest.raises(ValueError, match="blocked_forbidden_field"):
        _build(fixture)


@pytest.mark.parametrize("flag_name", FALSE_FLAGS)
def test_unsafe_true_flags_are_blocked_recursively(flag_name: str) -> None:
    fixture = _safe_fixture(nested={"unsafe_flags": {flag_name: True}})

    with pytest.raises(ValueError, match="blocked_unsafe_true_flag"):
        _build(fixture)


@pytest.mark.parametrize(
    "unsafe_value",
    [
        "G:/AICODING/private/path",
        "C:/Users/msjpurf/private/path",
        r"C:\\Users\\msjpurf\\private\\path",
        "../runtime/analysis_requests/private",
        "https://example.invalid/should-not-fetch",
        "donglu_sunjihai_youth_football/donglu-sunjihai-youth-football-202606-v2_20260617_121016",
    ],
)
def test_path_like_ids_and_arbitrary_paths_are_blocked(unsafe_value: str) -> None:
    fixture = _safe_fixture(lineage_review_status=unsafe_value)

    with pytest.raises(ValueError, match="blocked_forbidden_value"):
        _build(fixture)


def test_fixture_output_does_not_contain_public_message_scores_verification_claims_or_production_payloads() -> None:
    declaration = _build()
    serialized = _serialized(declaration)

    for token in FORBIDDEN_OUTPUT_TOKENS:
        assert token not in serialized


def test_fixture_creation_performs_no_file_reads(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_file_read(*args: object, **kwargs: object) -> None:
        raise AssertionError("declaration fixture creation must not read files")

    monkeypatch.setattr(Path, "read_text", fail_file_read)
    monkeypatch.setattr(Path, "read_bytes", fail_file_read)
    monkeypatch.setattr(Path, "open", fail_file_read)

    declaration = _build()

    assert declaration["declaration_schema"] == DECLARATION_SCHEMA
    assert declaration["actual_evidence_layer_write_performed"] is False


def test_service_does_not_import_forbidden_write_runtime_helpers_or_file_io_modules() -> None:
    service_path = (
        REPO_ROOT
        / "backend"
        / "app"
        / "services"
        / "evidence_layer_write_human_authority_declaration_fixture.py"
    )
    service_source = service_path.read_text(encoding="utf-8")
    import_lines = [
        line.strip()
        for line in service_source.splitlines()
        if line.startswith("import ") or line.startswith("from ")
    ]

    for forbidden_import in FORBIDDEN_SERVICE_IMPORTS:
        assert all(forbidden_import not in line for line in import_lines), forbidden_import

    assert "Path(" not in service_source
    assert ".open(" not in service_source
    assert ".read_text(" not in service_source
    assert ".read_bytes(" not in service_source
    assert "subprocess" not in service_source


def test_safe_summary_preserves_non_authorizing_no_write_boundary() -> None:
    service = _service_module()
    summary = service.build_non_authorizing_human_authority_declaration_fixture_summary(
        _safe_fixture(),
        exact_approval_phrase=EXPECTED_APPROVAL_PHRASE,
    )

    assert summary["summary_schema"] == "sentigraph_actual_evidence_layer_write_human_authority_declaration_summary_v0_1"
    assert summary["declaration_schema"] == DECLARATION_SCHEMA
    assert summary["declaration_status"] == BLOCKED_STATUS
    assert summary["declaration_scope"] == DECLARATION_SCOPE
    assert summary["declaration_mode"] == DECLARATION_MODE
    assert summary["final_write_authorization_still_required"] is True
    for flag in FALSE_FLAGS:
        assert summary[flag] is False, flag
    _assert_safe_serialized(summary)
