from __future__ import annotations

import hashlib
import json
from typing import Any

import pytest

import app.services.governed_decision_existing_evidence_target_selection_outcome as outcome_module
from app.services.governed_decision_existing_evidence_target_selection_outcome import (
    ACCEPTED_RESULT_BINDING_FIELDS,
    DECISION_REFERENCE_FIELDS,
    MAINLINE_ADJUDICATION_RECEIPT_REFERENCE,
    OUTCOME,
    OUTCOME_RECEIPT_MODE,
    OUTCOME_RECEIPT_SCHEMA,
    OUTCOME_RECEIPT_VERSION,
    OUTPUT_FIELDS,
    POOL_REVIEW_SUMMARY_FIELDS,
    POOL_REVIEW_SUMMARY_MODE,
    POOL_REVIEW_SUMMARY_SCHEMA,
    POOL_REVIEW_SUMMARY_VERSION,
    SELECTION_EXHAUSTION_SCOPE,
    SELECTION_SCOPE,
    GovernedDecisionExistingEvidenceTargetSelectionOutcomeValidationError,
    build_governed_decision_existing_evidence_target_selection_outcome,
)
from app.services.identity_ready_governed_nonproduction_human_review_decision_downstream_handoff import (
    IdentityReadyGovernedNonproductionHumanReviewDecisionDownstreamHandoffValidationError,
)


DECISION_SUFFIX = "0123456789abcdef0123456789abcdef"


def _projection() -> dict[str, Any]:
    return {
        "decision_id": f"irghrd-{DECISION_SUFFIX}",
        "audit_receipt_reference": f"irghrd-receipt-{DECISION_SUFFIX}",
        "sample_handle": "helldivers2-psn-demo",
        "decision_type": "keep_pending_human_review",
        "decision_status": "recorded_append_only_nonproduction_identity_ready",
        "recorded_at": "2026-08-31T12:34:56Z",
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_object_enabled": False,
        "review_queue_runtime_enabled": False,
        "evidence_layer_write_performed": False,
        "provider_or_b05_called": False,
        "analysis_triggered": False,
        "report_triggered": False,
    }


def _binding(
    role: str = "NLO2",
    filename: str = "NLO2_RESULT.json",
) -> dict[str, Any]:
    return {
        "role": role,
        "filename": filename,
        "bytes": 13322,
        "sha256": "d22520249403b4cdcce51134a74b170d8932531946d3cd5bbe1cb5ca62e819f1",
        "terminal_classification": (
            "NO_EXISTING_EXACT_NO_LINK_OUTCOME_SEAM_MINIMAL_"
            "NONAUTHORIZING_IMPLEMENTATION_IDENTIFIED_READY_FOR_MAINLINE"
        ),
        "mainline_accepted": True,
    }


def _summary() -> dict[str, Any]:
    return {
        "schema": POOL_REVIEW_SUMMARY_SCHEMA,
        "version": POOL_REVIEW_SUMMARY_VERSION,
        "mode": POOL_REVIEW_SUMMARY_MODE,
        "mainline_adjudication_receipt_reference": (
            MAINLINE_ADJUDICATION_RECEIPT_REFERENCE
        ),
        "decision_subject": "helldivers2-psn-demo",
        "review_scope": SELECTION_EXHAUSTION_SCOPE,
        "complete_existing_evidence_bearing_case_count": 23,
        "complete_existing_evidenceitem_count": 78,
        "eligible_evidenceitem_count": 57,
        "ineligible_evidenceitem_count": 21,
        "reviewed_existing_evidence_bearing_case_count": 23,
        "reviewed_existing_evidenceitem_count": 78,
        "selectable_existing_target_count": 0,
        "target_pool_complete": True,
        "selection_not_attempted": False,
        "selection_pending": False,
        "selection_exhausted": True,
        "privacy_blocked_unadjudicated_present": True,
        "privacy_blocked_unadjudicated_case_ids": ["case_018"],
        "privacy_blocked_target_match_claimed": False,
        "privacy_blocked_target_mismatch_claimed": False,
        "operational_failure": False,
        "selected_case_id": None,
        "selected_evidence_id": None,
        "selected_evidence_content_hash": None,
        "final_linkage_target_selected": False,
        "accepted_result_bindings": [_binding()],
    }


def _build(
    projection: dict[str, Any] | None = None,
    summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_governed_decision_existing_evidence_target_selection_outcome(
        projection or _projection(),
        summary or _summary(),
    )


def _assert_rejected(summary: dict[str, Any]) -> None:
    with pytest.raises(
        GovernedDecisionExistingEvidenceTargetSelectionOutcomeValidationError
    ):
        _build(summary=summary)


def test_valid_current_shaped_summary_builds_exact_54_field_receipt() -> None:
    receipt = _build()

    assert len(POOL_REVIEW_SUMMARY_FIELDS) == 27
    assert len(OUTPUT_FIELDS) == 54
    assert tuple(receipt) == OUTPUT_FIELDS
    assert receipt["schema"] == OUTCOME_RECEIPT_SCHEMA
    assert receipt["version"] == OUTCOME_RECEIPT_VERSION
    assert receipt["mode"] == OUTCOME_RECEIPT_MODE
    assert receipt["outcome"] == OUTCOME
    assert receipt["selection_scope"] == SELECTION_SCOPE
    assert receipt["selection_exhaustion_scope"] == SELECTION_EXHAUSTION_SCOPE
    assert receipt["complete_existing_evidence_bearing_case_count"] == 23
    assert receipt["complete_existing_evidenceitem_count"] == 78
    assert receipt["eligible_evidenceitem_count"] == 57
    assert receipt["ineligible_evidenceitem_count"] == 21
    assert receipt["reviewed_existing_evidence_bearing_case_count"] == 23
    assert receipt["reviewed_existing_evidenceitem_count"] == 78


def test_decision_projection_is_validated_through_existing_builder_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = (
        outcome_module.build_identity_ready_governed_nonproduction_human_review_decision_downstream_handoff_candidate
    )
    calls = 0

    def counted(projection: dict[str, Any]) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return original(projection)

    monkeypatch.setattr(
        outcome_module,
        "build_identity_ready_governed_nonproduction_human_review_decision_downstream_handoff_candidate",
        counted,
    )

    receipt = _build()

    assert calls == 1
    assert receipt["decision_handoff_validated"] is True
    assert tuple(receipt["decision_reference"]) == DECISION_REFERENCE_FIELDS


def test_invalid_decision_projection_fails_closed() -> None:
    projection = {**_projection(), "production_object_enabled": True}

    with pytest.raises(
        IdentityReadyGovernedNonproductionHumanReviewDecisionDownstreamHandoffValidationError
    ):
        _build(projection=projection)


def test_decision_subject_mismatch_is_rejected() -> None:
    _assert_rejected({**_summary(), "decision_subject": "another-subject"})


@pytest.mark.parametrize("field", POOL_REVIEW_SUMMARY_FIELDS)
def test_each_missing_pool_summary_field_is_rejected(field: str) -> None:
    summary = {key: value for key, value in _summary().items() if key != field}
    _assert_rejected(summary)


def test_extra_pool_summary_field_is_rejected() -> None:
    _assert_rejected({**_summary(), "raw_case_content": "forbidden"})


@pytest.mark.parametrize(
    ("changes", "expected_error"),
    [
        ({"eligible_evidenceitem_count": 56}, "count"),
        ({"reviewed_existing_evidenceitem_count": 77}, "count"),
        ({"reviewed_existing_evidence_bearing_case_count": 22}, "count"),
        ({"target_pool_complete": False}, "state"),
        ({"selection_not_attempted": True}, "state"),
        ({"selection_pending": True}, "state"),
        ({"selection_exhausted": False}, "state"),
        ({"operational_failure": True}, "state"),
        ({"selectable_existing_target_count": 1}, "state"),
        ({"selected_case_id": "case_001"}, "state"),
        ({"selected_evidence_id": "evidence_001"}, "state"),
        ({"selected_evidence_content_hash": "0" * 64}, "state"),
        ({"final_linkage_target_selected": True}, "state"),
    ],
)
def test_incomplete_or_nonexhausted_state_is_rejected(
    changes: dict[str, Any],
    expected_error: str,
) -> None:
    del expected_error
    _assert_rejected({**_summary(), **changes})


@pytest.mark.parametrize(
    "changes",
    [
        {
            "privacy_blocked_unadjudicated_present": False,
            "privacy_blocked_unadjudicated_case_ids": ["case_018"],
        },
        {
            "privacy_blocked_unadjudicated_present": True,
            "privacy_blocked_unadjudicated_case_ids": [],
        },
        {"privacy_blocked_target_match_claimed": True},
        {"privacy_blocked_target_mismatch_claimed": True},
        {
            "privacy_blocked_unadjudicated_case_ids": [
                "case_018",
                "case_018",
            ]
        },
        {
            "privacy_blocked_unadjudicated_case_ids": [
                "case_019",
                "case_018",
            ]
        },
        {"privacy_blocked_unadjudicated_case_ids": ["raw subject text"]},
    ],
)
def test_invalid_privacy_block_contract_is_rejected(
    changes: dict[str, Any],
) -> None:
    _assert_rejected({**_summary(), **changes})


def test_case_018_style_privacy_block_is_preserved_without_semantic_claim() -> None:
    receipt = _build()

    assert receipt["privacy_blocked_unadjudicated_present"] is True
    assert receipt["privacy_blocked_unadjudicated_case_count"] == 1
    assert receipt["privacy_blocked_unadjudicated_case_ids"] == ["case_018"]
    assert receipt["privacy_blocked_target_match_claimed"] is False
    assert receipt["privacy_blocked_target_mismatch_claimed"] is False
    assert "global_absence_of_relevant_evidence_claimed" not in receipt


@pytest.mark.parametrize("field", ACCEPTED_RESULT_BINDING_FIELDS)
def test_each_missing_result_binding_field_is_rejected(field: str) -> None:
    binding = {key: value for key, value in _binding().items() if key != field}
    _assert_rejected({**_summary(), "accepted_result_bindings": [binding]})


def test_extra_result_binding_field_is_rejected() -> None:
    binding = {**_binding(), "raw_result_body": "forbidden"}
    _assert_rejected({**_summary(), "accepted_result_bindings": [binding]})


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("role", "lowercase"),
        ("filename", "../result.json"),
        ("filename", "folder/result.json"),
        ("filename", "result.txt"),
        ("bytes", 0),
        ("bytes", True),
        ("sha256", "A" * 64),
        ("sha256", "0" * 63),
        ("terminal_classification", ""),
        ("terminal_classification", "contains spaces"),
        ("mainline_accepted", False),
    ],
)
def test_unsafe_result_binding_value_is_rejected(
    field: str,
    invalid_value: Any,
) -> None:
    binding = {**_binding(), field: invalid_value}
    _assert_rejected({**_summary(), "accepted_result_bindings": [binding]})


def test_duplicate_or_noncanonical_result_bindings_are_rejected() -> None:
    duplicate_role = [
        _binding("A", "a.json"),
        _binding("A", "b.json"),
    ]
    _assert_rejected(
        {**_summary(), "accepted_result_bindings": duplicate_role}
    )

    duplicate_filename = [
        _binding("A", "same.json"),
        _binding("B", "same.json"),
    ]
    _assert_rejected(
        {**_summary(), "accepted_result_bindings": duplicate_filename}
    )

    noncanonical = [
        _binding("B", "b.json"),
        _binding("A", "a.json"),
    ]
    _assert_rejected(
        {**_summary(), "accepted_result_bindings": noncanonical}
    )


def test_result_binding_list_cap_is_enforced() -> None:
    bindings = [
        _binding(f"R{index:02d}", f"result_{index:02d}.json")
        for index in range(17)
    ]
    _assert_rejected({**_summary(), "accepted_result_bindings": bindings})


def test_fingerprint_and_reference_are_exact_and_deterministic() -> None:
    first = _build()
    second = _build()
    material = {
        key: first[key]
        for key in first
        if key
        not in {"outcome_receipt_reference", "outcome_fingerprint_sha256"}
    }
    canonical = json.dumps(
        material,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    expected = hashlib.sha256(canonical).hexdigest()

    assert first == second
    assert first is not second
    assert first["outcome_fingerprint_sha256"] == expected
    assert first["outcome_receipt_reference"] == f"gdetso-{expected[:32]}"


def test_receipt_is_nonpersistent_and_nonauthorizing() -> None:
    receipt = _build()
    false_fields = (
        "accepted_result_files_verified_by_builder",
        "mainline_authority_validated_by_builder",
        "persisted",
        "truth_support_contradiction_verification_or_trust_claimed",
        "linkage_candidate_created",
        "linkage_write_authorized",
        "review_queue_runtime_enabled",
        "evidence_layer_write_performed",
        "provider_or_b05_called",
        "analysis_triggered",
        "report_triggered",
        "production_object_enabled",
        "public_export_delivery_enabled",
        "new_evidence_acquisition_authorized",
    )

    assert receipt["candidate_only"] is True
    assert receipt["human_review_required"] is True
    assert receipt["no_automatic_trust_upgrade"] is True
    assert all(receipt[field] is False for field in false_fields)


def test_no_raw_content_or_sentinel_identity_is_emitted() -> None:
    receipt = _build()
    prohibited = {
        "raw_case_content",
        "raw_evidence_content",
        "evidence_item",
        "sentinel_evidenceitem",
        "sentinel_link",
        "casestore",
        "decision_ledger",
        "link_ledger",
        "filesystem_path",
        "database_connection",
    }

    assert prohibited.isdisjoint(receipt)
    assert receipt["selected_case_id"] is None
    assert receipt["selected_evidence_id"] is None
    assert receipt["selected_evidence_content_hash"] is None
    assert receipt["final_linkage_target_selected"] is False


def test_inputs_are_not_mutated_and_result_bindings_are_copied() -> None:
    projection = _projection()
    summary = _summary()
    projection_before = {key: value for key, value in projection.items()}
    summary_before = {
        **summary,
        "privacy_blocked_unadjudicated_case_ids": [
            item for item in summary["privacy_blocked_unadjudicated_case_ids"]
        ],
        "accepted_result_bindings": [
            {key: value for key, value in record.items()}
            for record in summary["accepted_result_bindings"]
        ],
    }

    receipt = _build(projection, summary)
    summary["accepted_result_bindings"][0]["role"] = "CHANGED"

    assert projection == projection_before
    assert summary_before["decision_subject"] == summary["decision_subject"]
    assert receipt["accepted_result_bindings"][0]["role"] == "NLO2"
