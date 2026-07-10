from __future__ import annotations

import inspect
import json
from importlib import import_module
from pathlib import Path
from typing import Any

import pytest


APPROVAL_PHRASE = "APPROVE_9A_15_CONTROLLED_CANDIDATE_SPECIFIC_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_PRE_WRITE_REVIEW_AUDIT_NO_WRITE"
AUDIT_SCHEMA = "sentigraph_controlled_candidate_specific_evidence_layer_pre_write_review_audit_v0_1"
AUDIT_MODE = "backend_only_local_candidate_specific_pre_write_review_no_write"
DIRECT_WRITE_SCHEMA = "sentigraph_controlled_evidence_layer_write_candidate_set_v0_1"
PRODUCTION_IMPORT_SCHEMA = "sentigraph_controlled_production_evidence_import_candidate_set_v0_1"
DERIVED_WRITE_SCHEMA = (
    "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1"
)

NEIGHBOR_PHRASES = [
    "APPROVE_9A_14_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_HUMAN_PROVIDED_AUTHORITY_MANUAL_REVIEW_RESPONSIBILITY_DECLARATION_RECOGNITION_SAFETY_CONTRACT_TESTS_ONLY",
    "APPROVE_9A_13_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_HUMAN_PROVIDED_AUTHORITY_MANUAL_REVIEW_RESPONSIBILITY_DECLARATION_GATE_DOCS_ONLY",
    "APPROVE_9A_11_CONTROLLED_NON_AUTHORIZING_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_HUMAN_AUTHORITY_DECLARATION_FIXTURE_SMOKE",
    "APPROVE_9A_4_CONTROLLED_NO_WRITE_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_AUTHORIZATION_READINESS_CANDIDATE_FIXTURE_SMOKE",
    "APPROVE_8Y_13C_CONTROLLED_PRODUCTION_IMPORT_DERIVED_REROUTE_SMOKE",
    "APPROVE_8Y_14_CONTROLLED_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_SMOKE",
    "APPROVE_8W_28_CONTROLLED_EVIDENCEITEM_EVIDENCE_LAYER_WRITE_RUNTIME_IMPLEMENTATION",
    "APPROVE_GENERIC_PRE_WRITE_REVIEW",
]

FALSE_FLAGS = [
    "actual_write_authorized",
    "actual_evidence_layer_write_approved",
    "actual_evidence_layer_write_performed",
    "persisted_evidence_layer_record_created",
    "production_evidenceitem_creation_authorized",
    "production_evidenceitem_created",
    "write_helper_execution_allowed",
    "write_authorization_object_created_that_permits_write",
    "evidenceitem_write_runtime_called",
    "human_authority_validated",
    "manual_review_responsibility_accepted",
    "final_write_authorization_performed",
    "ready_for_actual_write",
    "review_queue_runtime_used",
    "production_case_created",
    "production_analysis_run_created",
    "actual_analysis_execution_started",
    "production_analysis_result_authorized",
    "production_analysis_result_created",
    "source11_runtime_called",
    "finalsummaryreport_runtime_called",
    "public_delivery_created",
    "provider_called",
    "collector_called",
    "private_collector_inspected",
    "real_exchange_dir_read",
    "production_package_rows_parsed",
]

RISK_CATEGORIES = [
    "production_data_integrity_risk",
    "privacy_raw_identity_risk",
    "irreversible_write_risk",
    "authorization_confusion_risk",
    "trust_inflation_risk",
    "provider_vendor_output_mistaken_as_truth_risk",
    "duplicate_amplification_risk",
    "weak_rejected_evidence_inclusion_risk",
    "route_api_frontend_accidental_write_exposure_risk",
    "downstream_production_escalation_risk",
    "source11_finalsummaryreport_escalation_risk",
    "public_customer_readiness_overclaim_risk",
]

ALLOWED_RISK_LABELS = {
    "mitigated_for_controlled_fixture",
    "open",
    "unknown",
    "not_applicable_to_no_write_fixture",
    "blocked",
}

FORBIDDEN_IMPORT_TOKENS = [
    "controlled_evidenceitem_evidence_layer_write_runtime",
    "evidence_import",
    "evidence_ingestion",
    "review_queue",
    "production_case",
    "production_analysis_run",
    "analysis_result",
    "source11",
    "finalsummaryreport",
]


def _service():
    return import_module("app.services.evidence_layer_write_candidate_pre_write_review_audit")


def _safe_candidate(**overrides: object) -> dict[str, Any]:
    candidate: dict[str, Any] = {
        "candidate_id": "candidate_fixture_9a15_001",
        "selected_candidate_schema": DERIVED_WRITE_SCHEMA,
        "candidate_origin": "controlled_8y13c_equivalent_in_memory_fixture",
        "real_production_candidate": False,
        "real_package_rows_used": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "warning_count": 1,
        "warnings": ["manual_review_required"],
        "warning_acknowledgment_present": True,
        "lineage": [
            {
                "stage": "direct_write_candidate",
                "schema": DIRECT_WRITE_SCHEMA,
                "candidate_ref": "direct_fixture_9a15_001",
            },
            {
                "stage": "controlled_production_evidence_import_candidate",
                "schema": PRODUCTION_IMPORT_SCHEMA,
                "candidate_ref": "production_import_fixture_9a15_001",
                "source_candidate_ref": "direct_fixture_9a15_001",
            },
            {
                "stage": "production_import_derived_write_candidate",
                "schema": DERIVED_WRITE_SCHEMA,
                "candidate_ref": "candidate_fixture_9a15_001",
                "source_candidate_ref": "production_import_fixture_9a15_001",
            },
        ],
        "boundary_flags": {flag: False for flag in FALSE_FLAGS},
    }
    candidate.update(overrides)
    return candidate


def _safe_candidate_fixture(*candidates: dict[str, Any]) -> dict[str, Any]:
    selected = list(candidates) if candidates else [_safe_candidate()]
    return {
        "source_direct_write_candidate_schema": DIRECT_WRITE_SCHEMA,
        "production_import_candidate_schema": PRODUCTION_IMPORT_SCHEMA,
        "selected_candidate_schema": DERIVED_WRITE_SCHEMA,
        "candidate_origin": "controlled_8y13c_equivalent_in_memory_fixture",
        "candidates": selected,
    }


def _safe_declaration_context(**overrides: object) -> dict[str, object]:
    context: dict[str, object] = {
        "declaration_source_kind": "explicit_human_message_later",
        "recognition_outcome": "declaration_present_for_docs_only_review",
        "declared_authority_role_label": "self_declared_project_owner_role",
        "authority_basis_label": "authority_basis_not_independently_validated",
        "manual_review_responsibility_statement_present": True,
        "warning_count_acknowledgment_present": True,
        "human_review_required_acknowledgment_present": True,
        "no_automatic_trust_upgrade_acknowledgment_present": True,
        "blocker_review_status_before_9a15": "not_reviewed_yet",
        "risk_review_status_before_9a15": "not_reviewed_yet",
        "lineage_review_status_before_9a15": "not_reviewed_yet",
        "raw_private_secret_absence_acknowledgment_before_9a15": "not_reviewed_yet",
        "rollback_pause_revocation_responsibility_label": "self_declared_project_owner_role",
        "human_authority_validated": False,
        "manual_review_responsibility_accepted": False,
        "final_write_authorization_performed": False,
        "actual_write_authorized": False,
        "production_evidenceitem_creation_authorized": False,
        "ready_for_actual_write": False,
    }
    context.update(overrides)
    return context


def _safe_rollback_plan(**overrides: object) -> dict[str, object]:
    plan: dict[str, object] = {
        "pause_on_any_blocker": True,
        "revocation_target_kind": "controlled_candidate_fixture",
        "revocation_target_ref": "candidate_fixture_9a15_001",
        "rollback_action": "discard_in_memory_candidate_and_audit",
        "persistence_rollback_required": False,
        "no_persistence": True,
        "final_write_authorization_still_required": True,
    }
    plan.update(overrides)
    return plan


def _build(
    candidate_fixture: dict[str, Any] | None = None,
    declaration_context: dict[str, object] | None = None,
    rollback_plan: dict[str, object] | None = None,
    *,
    phrase: str | None = APPROVAL_PHRASE,
) -> dict[str, Any]:
    return _service().audit_candidate_specific_pre_write_review(
        candidate_fixture or _safe_candidate_fixture(),
        declaration_context=declaration_context or _safe_declaration_context(),
        rollback_plan=rollback_plan or _safe_rollback_plan(),
        exact_approval_phrase=phrase,
    )


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def test_exact_9a15_phrase_is_required_before_audit_input_is_inspected() -> None:
    service = _service()
    assert service.APPROVAL_PHRASE == APPROVAL_PHRASE

    class ExplodingMapping(dict[str, object]):
        def get(self, key: str, default: object = None) -> object:
            raise AssertionError("candidate input inspected before approval phrase validation")

    for phrase in [None, "", "APPROVE_WRONG", *NEIGHBOR_PHRASES]:
        with pytest.raises(ValueError, match="blocked_(missing|wrong)_exact_9a15_approval"):
            service.audit_candidate_specific_pre_write_review(
                ExplodingMapping(),
                declaration_context=ExplodingMapping(),
                rollback_plan=ExplodingMapping(),
                exact_approval_phrase=phrase,
            )


def test_safe_in_memory_8y13c_equivalent_candidate_is_audited_no_write() -> None:
    audit = _build()

    assert audit["audit_schema"] == AUDIT_SCHEMA
    assert audit["phase"] == "9A-15"
    assert audit["audit_mode"] == AUDIT_MODE
    assert audit["audit_status"] == "candidate_review_complete_no_write"
    assert audit["selected_candidate_count"] == 1
    assert audit["selected_candidate_id"] == "candidate_fixture_9a15_001"
    assert audit["selected_candidate_schema"] == DERIVED_WRITE_SCHEMA
    assert audit["selected_candidate_origin"] == "controlled_8y13c_equivalent_in_memory_fixture"
    assert audit["candidate_specific_review_complete"] is True
    assert audit["candidate_specific_blockers_clear"] is True
    assert audit["blockers"] == []


@pytest.mark.parametrize(
    ("fixture", "expected_blocker"),
    [
        (_safe_candidate_fixture(_safe_candidate(selected_candidate_schema="wrong")), "selected_candidate_schema_wrong"),
        (_safe_candidate_fixture(), "candidate_count_not_exactly_one"),
        (
            _safe_candidate_fixture(_safe_candidate(), _safe_candidate(candidate_id="candidate_fixture_9a15_002")),
            "candidate_count_not_exactly_one",
        ),
        (_safe_candidate_fixture(_safe_candidate(candidate_id="G:/candidate.json")), "candidate_id_not_safe_opaque_id"),
        (_safe_candidate_fixture(_safe_candidate(candidate_id="https://example.invalid/candidate")), "candidate_id_not_safe_opaque_id"),
    ],
)
def test_schema_count_and_opaque_candidate_id_are_required(
    fixture: dict[str, Any], expected_blocker: str
) -> None:
    if fixture["candidates"] == [_safe_candidate()]:
        fixture = {**fixture, "candidates": []}
    audit = _build(fixture)
    assert audit["audit_status"] == "candidate_review_blocked_no_write"
    assert expected_blocker in audit["blockers"]
    assert audit["candidate_specific_review_complete"] is False
    assert audit["ready_for_actual_write"] is False


def test_required_three_stage_lineage_is_ordered_and_continuous() -> None:
    audit = _build()
    lineage = audit["lineage_review"]

    assert lineage["status"] == "reviewed"
    assert lineage["stage_order"] == [
        "direct_write_candidate",
        "controlled_production_evidence_import_candidate",
        "production_import_derived_write_candidate",
    ]
    assert lineage["schema_transitions_match"] is True
    assert lineage["candidate_reference_continuity"] is True
    assert lineage["no_lineage_gap"] is True
    assert lineage["no_arbitrary_source_substitution"] is True
    assert lineage["no_original_row_or_real_package_dependency"] is True


@pytest.mark.parametrize(
    "lineage_mutator",
    [
        lambda lineage: lineage[:2],
        lambda lineage: list(reversed(lineage)),
        lambda lineage: [*lineage[:1], {**lineage[1], "schema": "wrong"}, *lineage[2:]],
        lambda lineage: [*lineage[:2], {**lineage[2], "source_candidate_ref": "substituted_ref"}],
    ],
)
def test_missing_inconsistent_or_substituted_lineage_blocks(lineage_mutator) -> None:
    candidate = _safe_candidate()
    candidate["lineage"] = lineage_mutator(candidate["lineage"])
    audit = _build(_safe_candidate_fixture(candidate))

    assert audit["audit_status"] == "candidate_review_blocked_no_write"
    assert audit["lineage_review"]["status"] == "blocked"
    assert audit["candidate_specific_blockers_clear"] is False


@pytest.mark.parametrize(
    ("overrides", "expected_blocker"),
    [
        ({"human_review_required": False}, "human_review_required_not_true"),
        ({"no_automatic_trust_upgrade": False}, "no_automatic_trust_upgrade_not_true"),
        ({"warning_count": 0}, "warning_count_not_one"),
        ({"warnings": []}, "manual_review_required_warning_missing"),
        ({"warning_acknowledgment_present": False}, "warning_acknowledgment_missing"),
    ],
)
def test_human_review_no_upgrade_and_warning_acknowledgment_are_required(
    overrides: dict[str, object], expected_blocker: str
) -> None:
    audit = _build(_safe_candidate_fixture(_safe_candidate(**overrides)))
    assert audit["audit_status"] == "candidate_review_blocked_no_write"
    assert expected_blocker in audit["blockers"]


def test_candidate_blocker_and_all_risk_categories_are_reviewed_conservatively() -> None:
    audit = _build()
    blocker_review = audit["candidate_blocker_review"]
    risk_review = audit["risk_review"]

    assert blocker_review["status"] == "reviewed"
    assert all(blocker_review["checks"].values())
    assert risk_review["status"] == "reviewed"
    assert set(risk_review["classifications"]) == set(RISK_CATEGORIES)
    assert set(risk_review["classifications"].values()) <= ALLOWED_RISK_LABELS
    assert "production safe" not in _serialized(risk_review).lower()
    assert "write approved" not in _serialized(risk_review).lower()


@pytest.mark.parametrize(
    ("unsafe_key", "unsafe_value"),
    [
        ("raw_rows", [{"body": "forbidden-test-value"}]),
        ("raw_comment", "forbidden-test-value"),
        ("raw_author_id", "forbidden-test-value"),
        ("raw_author_name", "forbidden-test-value"),
        ("profile_url", "https://example.invalid/profile"),
        ("private_message", "forbidden-test-value"),
        ("token", "forbidden-test-value"),
        ("cookie", "forbidden-test-value"),
        ("session", "forbidden-test-value"),
        ("salt", "forbidden-test-value"),
        ("password", "forbidden-test-value"),
        (".env", "forbidden-test-value"),
        ("production_package_rows", [{"row": 1}]),
        ("evidence_items_jsonl_contents", "forbidden-test-value"),
        ("source_manifest_row_contents", "forbidden-test-value"),
        ("response_text", "forbidden-test-value"),
        ("target_user_list", ["forbidden-test-value"]),
        ("truth_score", 1.0),
        ("official_verified", True),
        ("psychological_profile", "forbidden-test-value"),
        ("real_person_pii", "forbidden-test-value"),
    ],
)
def test_recursive_raw_private_secret_scan_stops_without_echoing_unsafe_data(
    unsafe_key: str, unsafe_value: object
) -> None:
    candidate = _safe_candidate()
    candidate["nested_test_payload"] = {"deeper": {unsafe_key: unsafe_value}}
    audit = _build(_safe_candidate_fixture(candidate))

    assert audit["audit_status"] == "privacy_issue_stop"
    assert audit["raw_private_secret_review"]["status"] == "blocked"
    assert "privacy_or_forbidden_field_detected" in audit["blockers"]
    serialized = _serialized(audit)
    assert "forbidden-test-value" not in serialized
    assert "example.invalid" not in serialized


@pytest.mark.parametrize(
    "unsafe_value",
    [
        "G:/real/package/path",
        "C:\\private\\package.json",
        "https://example.invalid/package",
        "file:///private/package.json",
    ],
)
def test_arbitrary_path_url_or_real_package_reference_blocks(unsafe_value: str) -> None:
    candidate = _safe_candidate()
    candidate["safe_note"] = unsafe_value
    audit = _build(_safe_candidate_fixture(candidate))
    assert audit["audit_status"] == "privacy_issue_stop"
    assert audit["real_package_or_rows_reviewed"] is False


@pytest.mark.parametrize(
    ("overrides", "expected_blocker"),
    [
        ({"pause_on_any_blocker": False}, "rollback_pause_revocation_plan_invalid"),
        ({"revocation_target_kind": "production_record"}, "rollback_pause_revocation_plan_invalid"),
        ({"revocation_target_ref": "wrong_ref"}, "rollback_pause_revocation_plan_invalid"),
        ({"rollback_action": "persist_then_delete"}, "rollback_pause_revocation_plan_invalid"),
        ({"persistence_rollback_required": True}, "rollback_pause_revocation_plan_invalid"),
        ({"no_persistence": False}, "rollback_pause_revocation_plan_invalid"),
        ({"final_write_authorization_still_required": False}, "rollback_pause_revocation_plan_invalid"),
    ],
)
def test_safe_rollback_pause_revocation_plan_is_required(
    overrides: dict[str, object], expected_blocker: str
) -> None:
    audit = _build(rollback_plan=_safe_rollback_plan(**overrides))
    assert audit["audit_status"] == "candidate_review_blocked_no_write"
    assert audit["rollback_pause_revocation_review"]["status"] == "blocked"
    assert expected_blocker in audit["blockers"]


def test_human_declaration_safe_context_is_preserved_but_never_validated_or_accepted() -> None:
    source = _safe_declaration_context()
    audit = _build(declaration_context=source)
    preserved = audit["human_declaration_context_review"]

    for key, value in source.items():
        assert preserved["preserved_context"][key] == value
    assert preserved["status"] == "reviewed_non_authorizing"
    assert preserved["declaration_structurally_present_for_docs_only_review"] is True
    assert audit["human_authority_validated"] is False
    assert audit["manual_review_responsibility_accepted"] is False
    assert audit["final_write_authorization_performed"] is False


@pytest.mark.parametrize("flag", FALSE_FLAGS)
def test_any_unsafe_true_flag_blocks(flag: str) -> None:
    candidate = _safe_candidate()
    candidate["boundary_flags"][flag] = True
    audit = _build(_safe_candidate_fixture(candidate))

    assert audit["audit_status"] == "candidate_review_blocked_no_write"
    assert f"unsafe_true_flag:{flag}" in audit["blockers"]
    assert audit["ready_for_actual_write"] is False


def test_success_output_keeps_authorization_blockers_and_pauses_actual_write() -> None:
    audit = _build()

    assert audit["candidate_specific_review_complete"] is True
    assert audit["real_production_candidate_reviewed"] is False
    assert audit["real_package_or_rows_reviewed"] is False
    assert audit["candidate_specific_blockers_clear"] is True
    assert audit["authorization_blockers_remaining"] is True
    assert audit["overall_write_disposition"] == "pause"
    assert audit["ready_for_actual_write"] is False
    assert audit["final_write_authorization_still_required"] is True
    for flag in FALSE_FLAGS:
        assert audit[flag] is False, flag

    serialized = _serialized(audit).lower()
    for forbidden_claim in [
        "candidate is approved for production write",
        "human authority is validated",
        "final authorization is complete",
        "production evidenceitem is authorized",
        "production-ready",
        "write-approved",
        "final-authorized",
    ]:
        assert forbidden_claim not in serialized


def test_no_file_reads_occur_during_candidate_audit(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_file_read(*args: object, **kwargs: object) -> None:
        raise AssertionError("9A-15 candidate audit must not read files")

    monkeypatch.setattr(Path, "read_text", fail_file_read)
    monkeypatch.setattr(Path, "read_bytes", fail_file_read)
    monkeypatch.setattr(Path, "open", fail_file_read)

    audit = _build()
    assert audit["audit_status"] == "candidate_review_complete_no_write"


def test_new_service_has_no_forbidden_runtime_or_production_imports() -> None:
    source = inspect.getsource(_service()).lower()
    import_lines = "\n".join(
        line.strip()
        for line in source.splitlines()
        if line.strip().startswith("import ") or line.strip().startswith("from ")
    )
    for token in FORBIDDEN_IMPORT_TOKENS:
        assert token not in import_lines, token
    assert "path(" not in source
    assert ".open(" not in source
    assert ".read_text(" not in source
    assert ".read_bytes(" not in source


def test_safe_summary_is_no_write_and_does_not_echo_candidate_payload() -> None:
    service = _service()
    summary = service.build_candidate_specific_pre_write_review_summary(_build())

    assert summary["audit_schema"] == AUDIT_SCHEMA
    assert summary["audit_status"] == "candidate_review_complete_no_write"
    assert summary["candidate_specific_review_complete"] is True
    assert summary["authorization_blockers_remaining"] is True
    assert summary["overall_write_disposition"] == "pause"
    assert summary["ready_for_actual_write"] is False
    assert "candidates" not in summary
    assert "lineage" not in summary
