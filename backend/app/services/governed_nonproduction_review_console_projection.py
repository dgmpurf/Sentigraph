from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from app.services.governed_nonproduction_exact_target_read_only_audit import (
    RESULT_FIELDS as AUDIT_RESULT_FIELDS,
    RESULT_SCHEMA as AUDIT_RESULT_SCHEMA,
    RESULT_VERSION as AUDIT_RESULT_VERSION,
    TARGET_STATE_OUTCOMES as AUDIT_TARGET_STATE_OUTCOMES,
    audit_governed_nonproduction_exact_target_read_only,
)


PROJECTION_SCHEMA = (
    "sentigraph_internal_alpha_governed_nonproduction_record_review_projection_v0_1"
)
PROJECTION_VERSION = "0.1"
PROJECTION_ID = "governed-nonproduction-record-review-v0-1"
PROJECTION_MODE = "internal_read_only_governed_nonproduction_record_review"
SOURCE_CHAIN_BOUNDARY = "governed_nonproduction_record_review_boundary"
UPSTREAM_SOURCE_CHAIN_BOUNDARY = "evidence_layer_write_candidate_boundary"

PROJECTION_FIELDS = (
    "projection_schema",
    "projection_version",
    "projection_id",
    "projection_status",
    "projection_mode",
    "source_chain_boundary",
    "upstream_source_chain_boundary",
    "review_disposition",
    "target_state_outcome",
    "persisted_record_id",
    "attempt_reservation_id",
    "candidate_identity_digest",
    "input_safe_hash",
    "gate_contract_safe_hash",
    "activation_decision_safe_hash",
    "record_snapshot_digest",
    "reservation_snapshot_digest",
    "record_count_class",
    "reservation_count_class",
    "expected_record_present",
    "expected_reservation_present",
    "unexpected_record_present",
    "unexpected_reservation_present",
    "record_actual_columns_verified",
    "reservation_actual_columns_verified",
    "record_canonical_hash_verified",
    "reservation_canonical_hash_verified",
    "record_exact_binding_verified",
    "reservation_exact_binding_verified",
    "record_reservation_cross_binding_verified",
    "implementation_mutating_attempt_consumed",
    "governed_nonproduction_record_exists",
    "record_status",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "production_evidenceitem_created",
    "production_case_changed",
    "downstream_runtime_called",
    "internal_read_only_projection_ready",
    "operator_runtime_ready",
    "production_ready",
    "public_ready",
    "allowed_actions",
    "blocked_actions",
    "warnings",
    "blockers",
)

READY_ALLOWED_ACTIONS = [
    "inspect_safe_governance_metadata",
    "keep_pending_human_review",
    "request_more_governance_review",
    "prepare_separate_correction_or_revocation_decision",
]
NON_READY_ALLOWED_ACTIONS = ["request_more_governance_review"]
BLOCKED_ACTIONS = [
    "write_again_blocked",
    "second_insert_blocked",
    "automatic_trust_upgrade_blocked",
    "production_promotion_blocked",
    "delete_reset_revoke_without_separate_authorization_blocked",
    "public_delivery_blocked",
]

_OUTCOME_MAP = {
    "exact_expected_reservation_and_record": (
        "governed_record_review_ready",
        "governed_nonproduction_pending_human_review",
        None,
    ),
    "exact_empty": (
        "governed_record_absent",
        "governed_nonproduction_absent",
        "expected_governed_record_not_present",
    ),
    "exact_expected_reservation_only": (
        "governed_record_missing_after_consumed_attempt",
        "governed_nonproduction_record_missing",
        "reservation_present_record_absent",
    ),
    "inconsistent_or_not_safely_classifiable": (
        "governed_record_inconsistent",
        "governed_nonproduction_state_inconsistent",
        "target_state_not_safely_classifiable",
    ),
    "sidecar_present_read_prohibited": (
        "governed_record_read_blocked_sidecar_present",
        "governed_nonproduction_state_unavailable",
        "sidecar_present_read_prohibited",
    ),
    "target_identity_or_metadata_blocked": (
        "governed_record_target_unavailable",
        "governed_nonproduction_state_unavailable",
        "target_identity_or_metadata_blocked",
    ),
    "bounded_read_only_failure": (
        "governed_record_read_only_audit_failed",
        "governed_nonproduction_state_unavailable",
        "bounded_read_only_audit_failure",
    ),
}

_COUNT_CLASSES = {"exact_0", "exact_1", "at_least_2", "not_obtained"}
_AUDIT_BOOLEAN_FIELDS = (
    "audit_task_completed",
    "target_identity_verified",
    "target_metadata_verified",
    "sidecar_preflight_passed",
    "sidecar_postflight_passed",
    "sqlite_opened",
    "sqlite_uri_mode_ro_verified",
    "sqlite_query_only_verified",
    "sqlite_authorizer_verified",
    "schema_contract_verified",
    "expected_record_present",
    "expected_reservation_present",
    "unexpected_record_present",
    "unexpected_reservation_present",
    "record_actual_columns_verified",
    "reservation_actual_columns_verified",
    "record_canonical_hash_verified",
    "reservation_canonical_hash_verified",
    "record_exact_binding_verified",
    "reservation_exact_binding_verified",
    "record_reservation_cross_binding_verified",
    "production_evidenceitem_created",
    "production_case_changed",
    "downstream_runtime_called",
    "writer_invoked",
    "mutation_attempted",
    "runtime_target_classification_performed",
    "physical_path_disclosed",
    "raw_row_disclosed",
    "SQL_text_disclosed",
    "exception_text_disclosed",
    "stack_trace_disclosed",
)
_MUST_REMAIN_FALSE_AUDIT_FIELDS = (
    "production_evidenceitem_created",
    "production_case_changed",
    "downstream_runtime_called",
    "writer_invoked",
    "mutation_attempted",
    "physical_path_disclosed",
    "raw_row_disclosed",
    "SQL_text_disclosed",
    "exception_text_disclosed",
    "stack_trace_disclosed",
)
_YES_NO_UNKNOWN = {"yes", "no", "unknown_not_safely_classified"}
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
TARGET_LOGICAL_LABEL = (
    "runtime/governed_nonproduction_evidence_persistence/"
    "evidence_records_v0_1.sqlite3"
)
DATABASE_PATH = REPOSITORY_ROOT.joinpath(*TARGET_LOGICAL_LABEL.split("/"))

EXPECTED_IDENTITY: dict[str, Any] = {
    "approved_case_id_hint": "donglu_sunjihai_youth_football_202606",
    "approved_package_name": (
        "donglu-sunjihai-youth-football-202606-v2_20260617_121016"
    ),
    "approved_package_role": "candidate_demo_sample",
    "approved_row_source": "evidence_items.jsonl",
    "candidate_lock_status": "locked_for_single_candidate_governance_review_only",
    "final_candidate_id": (
        "evidence-layer-write-candidate-from-production-import-001-0deacf3cded01410"
    ),
    "final_candidate_safe_hash": (
        "2d60536b6afa3324ac5518df545d0826f4109e1580da447d02fee8413e352cb5"
    ),
    "final_candidate_schema": (
        "sentigraph_controlled_evidence_layer_write_candidate_from_"
        "production_import_candidate_set_v0_1"
    ),
    "hash_algorithm": "sha256",
    "hash_input_scope": "versioned_safe_canonical_projection_only",
    "identity_schema": "sentigraph_one_real_source_locked_candidate_identity_v0_1",
    "identity_version": "0.1",
    "selected_preview_row_opaque_id": "preview-row-001",
    "selected_preview_row_safe_hash": (
        "ec06201c92f2fc6c22bca509a285fb02c317bd582460852b82669b79ff711391"
    ),
}
EXPECTED_GATE_CONTRACT_BINDING: dict[str, Any] = {
    "gate_contract_safe_hash": (
        "a3150e96893218a6bd5a25adec1dac38e3b3f2f48bf07dcc72313c05d919fc0a"
    ),
    "gate_contract_schema": (
        "sentigraph_exact_locked_candidate_actual_evidence_layer_write_"
        "execution_gate_contract_v0_1"
    ),
    "gate_contract_version": "0.1",
}
EXPECTED_ACTIVATION_DECISION_BINDING: dict[str, Any] = {
    "activation_decision_id": (
        "sentigraph-mvp13-a03-fresh-exact-nonproduction-persistence-activation-001"
    ),
    "activation_decision_safe_hash": (
        "e1b0fa0b7dbb885962ef5e36f6c87d8c7d0cebd18d2e31e2525fc6bbebe5695d"
    ),
    "activation_decision_schema": (
        "sentigraph_exact_locked_candidate_nonproduction_persistence_"
        "gate_activation_decision_v0_1"
    ),
    "activation_decision_version": "0.1",
    "candidate_identity_digest": (
        "078e2f428e42050eea013c8d2a3ee1ef1c7e341805e7a6fb38aa3cf276622d54"
    ),
    "decision_scope": "exact_locked_candidate_and_selected_nonproduction_target_only",
    "gate_contract_safe_hash": (
        "a3150e96893218a6bd5a25adec1dac38e3b3f2f48bf07dcc72313c05d919fc0a"
    ),
}
EXPECTED_INPUT_SAFE_HASH = (
    "71f39d8067543ae508d1d319e9c950c99030df65aa197d40f82e1f95ea76ebd5"
)
EXPECTED_IDEMPOTENCY_KEY = (
    "c886bd087e84dceff806e748d2f2ceaf11a53929576da0b8d1725c9e34ba8934"
)
EXPECTED_PERSISTED_RECORD_ID = "gnpepr-c886bd087e84dceff806e748d2f2ceaf"
EXPECTED_AUDIT_RECEIPT_REFERENCE = (
    "gnpepr-receipt-c886bd087e84dceff806e748d2f2ceaf"
)
EXPECTED_ATTEMPT_SCOPE_KEY = (
    "c271ee89162b8ad4a88fd2e6f14abce4f440f54f6a0676dd1669be7c59880e9d"
)
EXPECTED_ATTEMPT_RESERVATION_ID = (
    "gnpepr-attempt-34d95623c3678bdd63430d97fdc7d922"
)
EXPECTED_CANDIDATE_IDENTITY_DIGEST = (
    "078e2f428e42050eea013c8d2a3ee1ef1c7e341805e7a6fb38aa3cf276622d54"
)
EXPECTED_GATE_CONTRACT_SAFE_HASH = (
    "a3150e96893218a6bd5a25adec1dac38e3b3f2f48bf07dcc72313c05d919fc0a"
)
EXPECTED_ACTIVATION_DECISION_SAFE_HASH = (
    "e1b0fa0b7dbb885962ef5e36f6c87d8c7d0cebd18d2e31e2525fc6bbebe5695d"
)
EXPECTED_RECORD_SNAPSHOT_DIGEST = (
    "eda50fc437940ac519881638d76fa0443481fc9fda8f50cf62805be0d83baf20"
)
EXPECTED_RESERVATION_SNAPSHOT_DIGEST = (
    "076584df7f9d712b78e9c3e5dee06cc55ff817487084074e34824bd9185f7a6c"
)


def build_governed_nonproduction_review_console_projection() -> dict[str, Any]:
    """Build one bounded request-local projection through the accepted reader."""

    try:
        audit_result = audit_governed_nonproduction_exact_target_read_only(
            authorized_root_path=REPOSITORY_ROOT,
            database_path=DATABASE_PATH,
            target_logical_label=TARGET_LOGICAL_LABEL,
            expected_identity=dict(EXPECTED_IDENTITY),
            expected_gate_contract_binding=dict(EXPECTED_GATE_CONTRACT_BINDING),
            expected_activation_decision_binding=dict(
                EXPECTED_ACTIVATION_DECISION_BINDING
            ),
            expected_input_safe_hash=EXPECTED_INPUT_SAFE_HASH,
            expected_idempotency_key=EXPECTED_IDEMPOTENCY_KEY,
            expected_persisted_record_id=EXPECTED_PERSISTED_RECORD_ID,
            expected_audit_receipt_reference=EXPECTED_AUDIT_RECEIPT_REFERENCE,
            expected_attempt_scope_key=EXPECTED_ATTEMPT_SCOPE_KEY,
            expected_attempt_reservation_id=EXPECTED_ATTEMPT_RESERVATION_ID,
        )
    except Exception:
        audit_result = None
    return _map_audit_result_to_projection(audit_result)


def _map_audit_result_to_projection(
    audit_result: dict[str, Any] | None,
) -> dict[str, Any]:
    source = audit_result if _audit_result_is_structurally_safe(audit_result) else {}
    outcome = source.get("target_state_outcome", "bounded_read_only_failure")
    if (
        outcome == "exact_expected_reservation_and_record"
        and not _audit_result_is_exact_ready(source)
    ):
        outcome = "bounded_read_only_failure"

    projection_status, record_status, blocker = _OUTCOME_MAP[outcome]
    ready = outcome == "exact_expected_reservation_and_record"

    safe_values: dict[str, str | None] = {
        "persisted_record_id": None,
        "attempt_reservation_id": None,
        "candidate_identity_digest": None,
        "input_safe_hash": None,
        "gate_contract_safe_hash": None,
        "activation_decision_safe_hash": None,
        "record_snapshot_digest": None,
        "reservation_snapshot_digest": None,
    }
    if ready:
        safe_values.update(
            {
                "persisted_record_id": EXPECTED_PERSISTED_RECORD_ID,
                "attempt_reservation_id": EXPECTED_ATTEMPT_RESERVATION_ID,
                "candidate_identity_digest": EXPECTED_CANDIDATE_IDENTITY_DIGEST,
                "input_safe_hash": EXPECTED_INPUT_SAFE_HASH,
                "gate_contract_safe_hash": EXPECTED_GATE_CONTRACT_SAFE_HASH,
                "activation_decision_safe_hash": (
                    EXPECTED_ACTIVATION_DECISION_SAFE_HASH
                ),
                "record_snapshot_digest": EXPECTED_RECORD_SNAPSHOT_DIGEST,
                "reservation_snapshot_digest": (
                    EXPECTED_RESERVATION_SNAPSHOT_DIGEST
                ),
            }
        )

    projection = {
        "projection_schema": PROJECTION_SCHEMA,
        "projection_version": PROJECTION_VERSION,
        "projection_id": PROJECTION_ID,
        "projection_status": projection_status,
        "projection_mode": PROJECTION_MODE,
        "source_chain_boundary": SOURCE_CHAIN_BOUNDARY,
        "upstream_source_chain_boundary": UPSTREAM_SOURCE_CHAIN_BOUNDARY,
        "review_disposition": (
            "pending_human_review" if ready else "human_review_blocked"
        ),
        "target_state_outcome": outcome,
        "persisted_record_id": safe_values["persisted_record_id"],
        "attempt_reservation_id": safe_values["attempt_reservation_id"],
        "candidate_identity_digest": safe_values["candidate_identity_digest"],
        "input_safe_hash": safe_values["input_safe_hash"],
        "gate_contract_safe_hash": safe_values["gate_contract_safe_hash"],
        "activation_decision_safe_hash": safe_values[
            "activation_decision_safe_hash"
        ],
        "record_snapshot_digest": safe_values["record_snapshot_digest"],
        "reservation_snapshot_digest": safe_values[
            "reservation_snapshot_digest"
        ],
        "record_count_class": _safe_count_class(source.get("record_count_class")),
        "reservation_count_class": _safe_count_class(
            source.get("reservation_count_class")
        ),
        "expected_record_present": source.get("expected_record_present") is True,
        "expected_reservation_present": (
            source.get("expected_reservation_present") is True
        ),
        "unexpected_record_present": (
            source.get("unexpected_record_present") is True
        ),
        "unexpected_reservation_present": (
            source.get("unexpected_reservation_present") is True
        ),
        "record_actual_columns_verified": (
            source.get("record_actual_columns_verified") is True
        ),
        "reservation_actual_columns_verified": (
            source.get("reservation_actual_columns_verified") is True
        ),
        "record_canonical_hash_verified": (
            source.get("record_canonical_hash_verified") is True
        ),
        "reservation_canonical_hash_verified": (
            source.get("reservation_canonical_hash_verified") is True
        ),
        "record_exact_binding_verified": (
            source.get("record_exact_binding_verified") is True
        ),
        "reservation_exact_binding_verified": (
            source.get("reservation_exact_binding_verified") is True
        ),
        "record_reservation_cross_binding_verified": (
            source.get("record_reservation_cross_binding_verified") is True
        ),
        "implementation_mutating_attempt_consumed": (
            source.get("implementation_mutating_attempt_consumed_actual") == "yes"
        ),
        "governed_nonproduction_record_exists": (
            source.get("governed_nonproduction_record_exists") == "yes"
        ),
        "record_status": record_status,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_evidenceitem_created": False,
        "production_case_changed": False,
        "downstream_runtime_called": False,
        "internal_read_only_projection_ready": ready,
        "operator_runtime_ready": False,
        "production_ready": False,
        "public_ready": False,
        "allowed_actions": (
            list(READY_ALLOWED_ACTIONS)
            if ready
            else list(NON_READY_ALLOWED_ACTIONS)
        ),
        "blocked_actions": list(BLOCKED_ACTIONS),
        "warnings": [],
        "blockers": [] if blocker is None else [blocker],
    }
    if tuple(projection) != PROJECTION_FIELDS:
        raise ValueError("governed_review_projection_contract_invalid")
    return projection


def _audit_result_is_structurally_safe(value: Any) -> bool:
    if not isinstance(value, dict) or tuple(value) != AUDIT_RESULT_FIELDS:
        return False
    if value.get("result_schema") != AUDIT_RESULT_SCHEMA:
        return False
    if value.get("result_version") != AUDIT_RESULT_VERSION:
        return False
    if value.get("target_state_outcome") not in AUDIT_TARGET_STATE_OUTCOMES:
        return False
    if not isinstance(value.get("safe_error_code"), str):
        return False
    if not isinstance(value.get("completed_stage"), str):
        return False
    if any(not isinstance(value.get(field), bool) for field in _AUDIT_BOOLEAN_FIELDS):
        return False
    if value.get("audit_task_completed") is not True:
        return False
    if any(value.get(field) is not False for field in _MUST_REMAIN_FALSE_AUDIT_FIELDS):
        return False
    if value.get("record_count_class") not in _COUNT_CLASSES:
        return False
    if value.get("reservation_count_class") not in _COUNT_CLASSES:
        return False
    if value.get("implementation_mutating_attempt_consumed_actual") not in _YES_NO_UNKNOWN:
        return False
    if value.get("governed_nonproduction_record_exists") not in _YES_NO_UNKNOWN:
        return False
    return all(
        digest is None or _is_sha256(digest)
        for digest in (
            value.get("record_snapshot_digest"),
            value.get("reservation_snapshot_digest"),
        )
    )


def _audit_result_is_exact_ready(value: dict[str, Any]) -> bool:
    expected_true = (
        "target_identity_verified",
        "target_metadata_verified",
        "sidecar_preflight_passed",
        "sidecar_postflight_passed",
        "sqlite_opened",
        "sqlite_uri_mode_ro_verified",
        "sqlite_query_only_verified",
        "sqlite_authorizer_verified",
        "schema_contract_verified",
        "expected_record_present",
        "expected_reservation_present",
        "record_actual_columns_verified",
        "reservation_actual_columns_verified",
        "record_canonical_hash_verified",
        "reservation_canonical_hash_verified",
        "record_exact_binding_verified",
        "reservation_exact_binding_verified",
        "record_reservation_cross_binding_verified",
        "runtime_target_classification_performed",
    )
    return (
        value.get("target_state_outcome")
        == "exact_expected_reservation_and_record"
        and value.get("safe_error_code") == "none"
        and value.get("completed_stage") == "completed"
        and value.get("record_count_class") == "exact_1"
        and value.get("reservation_count_class") == "exact_1"
        and value.get("record_snapshot_digest") == EXPECTED_RECORD_SNAPSHOT_DIGEST
        and value.get("reservation_snapshot_digest")
        == EXPECTED_RESERVATION_SNAPSHOT_DIGEST
        and value.get("unexpected_record_present") is False
        and value.get("unexpected_reservation_present") is False
        and value.get("implementation_mutating_attempt_consumed_actual") == "yes"
        and value.get("governed_nonproduction_record_exists") == "yes"
        and all(value.get(field) is True for field in expected_true)
    )


def _safe_count_class(value: Any) -> str:
    return value if value in _COUNT_CLASSES else "not_obtained"


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and _SHA256_PATTERN.fullmatch(value) is not None
