from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.services.evidence_layer_write_authorization_readiness_candidate import (
    APPROVAL_PHRASE,
    CANDIDATE_MODE,
    CANDIDATE_SCHEMA,
    build_no_write_evidence_layer_write_authorization_readiness_candidate,
    build_safe_no_write_evidence_layer_write_authorization_readiness_candidate_summary,
)


REPO_ROOT = Path(__file__).resolve().parents[3]

EXPECTED_APPROVAL_PHRASE = (
    "APPROVE_9A_4_CONTROLLED_NO_WRITE_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_"
    "AUTHORIZATION_READINESS_CANDIDATE_FIXTURE_SMOKE"
)
NEIGHBOR_PHRASES = [
    "APPROVE_9A_1_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_GO_NO_GO_GATE_DECISION_DOCS_ONLY",
    "APPROVE_9A_2_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_AUTHORIZATION_PROTOCOL_TESTS_ONLY",
    "APPROVE_9A_3_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_AUTHORIZATION_PROTOCOL_COMPLETION_WRITE_AUTHORIZATION_READINESS_GATE_DECISION_DOCS_ONLY",
    "APPROVE_8W_28_CONTROLLED_EVIDENCEITEM_EVIDENCE_LAYER_WRITE_RUNTIME_IMPLEMENTATION",
    "APPROVE_8W_70_PRODUCTION_ANALYSIS_RESULT_CREATION_CHAIN_REACTIVATION_DECISION_DOCS_ONLY",
    "APPROVE_GENERIC_WRITE_AUTHORIZATION",
]

FALSE_FLAGS = [
    "actual_evidence_layer_write_authorized",
    "actual_evidence_layer_write_performed",
    "production_evidenceitem_creation_authorized",
    "production_evidenceitem_created",
    "persisted_evidence_layer_record_created",
    "write_helper_execution_allowed",
    "helper_called",
    "evidenceitem_write_runtime_called",
    "human_authority_validated",
    "final_write_authorization_performed",
    "ready_for_actual_write",
    "write_authorization_object_created_that_permits_write",
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
    "secret",
    "token",
    "cookie",
    "session",
    "salt",
    "password",
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


def _safe_fixture(**overrides: object) -> dict[str, object]:
    fixture: dict[str, object] = {
        "input_schema": "sentigraph_9a_4_no_write_authorization_readiness_input_v0_1",
        "input_source_kind": "controlled_production_import_derived_write_candidate_summary",
        "source_candidate_ref": "opaque-write-candidate-summary-001",
        "input_lineage_summary": "safe Route C candidate summary labels only",
        "warning_count": 1,
        "blocker_statuses": {
            "human_review_required": "present",
            "final_write_authorization": "not_performed",
        },
        "risk_statuses": {
            "actual_write_boundary": "blocked",
            "production_evidenceitem_boundary": "blocked",
        },
        "acknowledgment_statuses": {
            "required_human_authority_status": "not_validated",
            "manual_review_responsibility_status": "requires_human_owner",
            "warning_count_acknowledgment_status": "acknowledged_as_unresolved",
            "human_review_required_acknowledgment_status": "acknowledged_required",
            "no_automatic_trust_upgrade_acknowledgment_status": "acknowledged_no_upgrade",
        },
        "safe_identity_policy_status": "safe_labels_only_no_raw_identity",
        "rollback_pause_policy_status": "pause_before_actual_write",
        "audit_note_status": "placeholder_only_no_runtime_audit",
    }
    fixture.update(overrides)
    return fixture


def _build(fixture: dict[str, object] | None = None) -> dict[str, object]:
    return build_no_write_evidence_layer_write_authorization_readiness_candidate(
        fixture or _safe_fixture(),
        exact_approval_phrase=EXPECTED_APPROVAL_PHRASE,
    )


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _assert_safe_serialized(value: object) -> None:
    serialized = _serialized(value)
    for forbidden_field in FORBIDDEN_FIELDS:
        assert forbidden_field not in serialized
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel not in serialized
    assert ":/" not in serialized
    assert ":\\" not in serialized


def test_exact_9a4_phrase_is_required() -> None:
    assert APPROVAL_PHRASE == EXPECTED_APPROVAL_PHRASE

    with pytest.raises(ValueError, match="blocked_missing_exact_approval"):
        build_no_write_evidence_layer_write_authorization_readiness_candidate(
            _safe_fixture(),
            exact_approval_phrase=None,
        )

    with pytest.raises(ValueError, match="blocked_wrong_exact_approval"):
        build_no_write_evidence_layer_write_authorization_readiness_candidate(
            _safe_fixture(),
            exact_approval_phrase="APPROVE_WRONG_NO_WRITE_PHRASE",
        )

    for phrase in NEIGHBOR_PHRASES:
        with pytest.raises(ValueError, match="blocked_wrong_exact_approval"):
            build_no_write_evidence_layer_write_authorization_readiness_candidate(
                _safe_fixture(),
                exact_approval_phrase=phrase,
            )


def test_safe_in_memory_fixture_builds_versioned_no_write_candidate() -> None:
    candidate = _build()

    assert candidate["candidate_schema"] == CANDIDATE_SCHEMA
    assert candidate["candidate_schema"] == "sentigraph_actual_evidence_layer_write_authorization_readiness_candidate_v0_1"
    assert candidate["candidate_mode"] == CANDIDATE_MODE
    assert candidate["candidate_mode"] == "backend_only_local_no_write_authorization_readiness_candidate_fixture"
    assert candidate["candidate_status"] == "candidate_blocked_no_write"
    assert candidate["candidate_id"].startswith("no-write-auth-readiness-")
    assert candidate["input_source_kind"] == "controlled_production_import_derived_write_candidate_summary"
    assert candidate["input_lineage_summary"] == "safe Route C candidate summary labels only"
    assert candidate["human_review_required"] is True
    assert candidate["no_automatic_trust_upgrade"] is True
    assert candidate["warning_count"] == 1
    assert candidate["blocker_count"] == 2
    assert candidate["risk_count"] == 2
    assert candidate["next_required_gate_label"] == "actual_write_requires_separate_future_gate"
    assert candidate["required_human_authority_status"] == "not_validated"
    assert candidate["manual_review_responsibility_status"] == "requires_human_owner"
    assert candidate["warning_count_acknowledgment_status"] == "acknowledged_as_unresolved"
    assert candidate["human_review_required_acknowledgment_status"] == "acknowledged_required"
    assert candidate["no_automatic_trust_upgrade_acknowledgment_status"] == "acknowledged_no_upgrade"
    assert candidate["safe_identity_policy_status"] == "safe_labels_only_no_raw_identity"
    assert candidate["rollback_pause_policy_status"] == "pause_before_actual_write"
    assert candidate["audit_note_status"] == "placeholder_only_no_runtime_audit"
    assert candidate["blocker_statuses"] == {
        "human_review_required": "present",
        "final_write_authorization": "not_performed",
    }
    assert candidate["risk_statuses"] == {
        "actual_write_boundary": "blocked",
        "production_evidenceitem_boundary": "blocked",
    }
    _assert_safe_serialized(candidate)


def test_candidate_status_without_blockers_still_does_not_imply_actual_write_readiness() -> None:
    candidate = _build(_safe_fixture(blocker_statuses=[]))

    assert candidate["candidate_status"] == "candidate_ready_for_human_review_no_write"
    assert candidate["ready_for_actual_write"] is False
    assert candidate["actual_evidence_layer_write_authorized"] is False
    assert candidate["production_evidenceitem_creation_authorized"] is False


def test_all_actual_write_production_runtime_source11_and_public_delivery_flags_are_false() -> None:
    candidate = _build()

    for flag in FALSE_FLAGS:
        assert candidate[flag] is False, flag

    assert candidate["human_review_required"] is True
    assert candidate["no_automatic_trust_upgrade"] is True
    assert candidate["human_authority_validated"] is False
    assert candidate["final_write_authorization_performed"] is False


@pytest.mark.parametrize("field_name", FORBIDDEN_FIELDS)
def test_recursive_forbidden_field_scanner_blocks_raw_private_secret_path_and_production_payload_fields(
    field_name: str,
) -> None:
    fixture = _safe_fixture(nested={"safe_container": {field_name: "actual-secret-should-never-appear"}})

    with pytest.raises(ValueError, match="blocked_forbidden_field"):
        _build(fixture)


@pytest.mark.parametrize("flag_name", FALSE_FLAGS)
def test_unsafe_true_flags_are_blocked(flag_name: str) -> None:
    fixture = _safe_fixture(nested={"unsafe_flags": {flag_name: True}})

    with pytest.raises(ValueError, match="blocked_unsafe_true_flag"):
        _build(fixture)


@pytest.mark.parametrize(
    "unsafe_ref",
    [
        "G:/AICODING/private/path",
        "C:/Users/msjpurf/private/path",
        r"C:\\Users\\msjpurf\\private\\path",
        "../runtime/analysis_requests/private",
        "donglu_sunjihai_youth_football/donglu-sunjihai-youth-football-202606-v2_20260617_121016",
    ],
)
def test_path_like_ids_and_arbitrary_paths_are_blocked(unsafe_ref: str) -> None:
    fixture = _safe_fixture(source_candidate_ref=unsafe_ref)

    with pytest.raises(ValueError, match="blocked_forbidden_value"):
        _build(fixture)


def test_candidate_never_contains_forbidden_response_public_persuasion_truth_or_profile_fields() -> None:
    candidate = _build()
    serialized = _serialized(candidate)

    for token in [
        "response_text",
        "generated_public_message",
        "target_user_list",
        "persuasion_score",
        "prediction_probability",
        "truth_score",
        "official_verified",
        "psychological_profile",
        "personality_diagnosis",
    ]:
        assert token not in serialized


def test_candidate_creation_performs_no_file_reads(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_file_read(*args: object, **kwargs: object) -> None:
        raise AssertionError("candidate creation must not read files")

    monkeypatch.setattr(Path, "read_text", fail_file_read)
    monkeypatch.setattr(Path, "read_bytes", fail_file_read)
    monkeypatch.setattr(Path, "open", fail_file_read)

    candidate = _build()

    assert candidate["candidate_schema"] == CANDIDATE_SCHEMA
    assert candidate["actual_evidence_layer_write_performed"] is False


def test_service_does_not_import_or_call_forbidden_write_runtime_helpers() -> None:
    service_path = REPO_ROOT / "backend" / "app" / "services" / "evidence_layer_write_authorization_readiness_candidate.py"
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


def test_safe_summary_preserves_no_write_no_production_boundary() -> None:
    summary = build_safe_no_write_evidence_layer_write_authorization_readiness_candidate_summary(
        _safe_fixture(),
        exact_approval_phrase=EXPECTED_APPROVAL_PHRASE,
    )

    assert summary["summary_schema"] == "sentigraph_actual_evidence_layer_write_authorization_readiness_candidate_summary_v0_1"
    assert summary["candidate_schema"] == CANDIDATE_SCHEMA
    assert summary["candidate_status"] == "candidate_blocked_no_write"
    assert summary["warning_count"] == 1
    assert summary["blocker_count"] == 2
    assert summary["risk_count"] == 2
    for flag in FALSE_FLAGS:
        assert summary[flag] is False, flag
    assert summary["human_review_required"] is True
    assert summary["no_automatic_trust_upgrade"] is True
    _assert_safe_serialized(summary)
