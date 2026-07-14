from __future__ import annotations

import ast
import importlib
import inspect
from pathlib import Path
from typing import Any

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
SERVICE_PATH = (
    REPO_ROOT
    / "backend/app/services/governed_nonproduction_review_console_projection.py"
)
ROUTE_PATH = REPO_ROOT / "backend/app/api/v1/routes/internal_alpha_review_console.py"

GLOBAL_GATE = "SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED"
GOVERNED_GATE = "SENTIGRAPH_INTERNAL_ALPHA_GOVERNED_RECORD_REVIEW_ENABLED"
GOVERNED_PROJECTION_ID = "governed-nonproduction-record-review-v0-1"
SYNTHETIC_PROJECTION_IDS = (
    "internal-alpha-safe-projection-fixture",
    "8z16-no-write-alpha-fixture",
)

PROJECTION_SCHEMA = (
    "sentigraph_internal_alpha_governed_nonproduction_record_review_projection_v0_1"
)
OUTER_RESPONSE_SCHEMA = (
    "sentigraph_internal_alpha_review_console_governed_record_route_response_v0_1"
)

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

SAFE_READY_FIELDS = (
    "persisted_record_id",
    "attempt_reservation_id",
    "candidate_identity_digest",
    "input_safe_hash",
    "gate_contract_safe_hash",
    "activation_decision_safe_hash",
    "record_snapshot_digest",
    "reservation_snapshot_digest",
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

EXPECTED_SAFE_READY_VALUES = {
    "persisted_record_id": "gnpepr-c886bd087e84dceff806e748d2f2ceaf",
    "attempt_reservation_id": "gnpepr-attempt-34d95623c3678bdd63430d97fdc7d922",
    "candidate_identity_digest": (
        "078e2f428e42050eea013c8d2a3ee1ef1c7e341805e7a6fb38aa3cf276622d54"
    ),
    "input_safe_hash": (
        "71f39d8067543ae508d1d319e9c950c99030df65aa197d40f82e1f95ea76ebd5"
    ),
    "gate_contract_safe_hash": (
        "a3150e96893218a6bd5a25adec1dac38e3b3f2f48bf07dcc72313c05d919fc0a"
    ),
    "activation_decision_safe_hash": (
        "e1b0fa0b7dbb885962ef5e36f6c87d8c7d0cebd18d2e31e2525fc6bbebe5695d"
    ),
    "record_snapshot_digest": (
        "eda50fc437940ac519881638d76fa0443481fc9fda8f50cf62805be0d83baf20"
    ),
    "reservation_snapshot_digest": (
        "076584df7f9d712b78e9c3e5dee06cc55ff817487084074e34824bd9185f7a6c"
    ),
}

OUTCOME_MAP = {
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

OUTER_RESPONSE_FIELDS = (
    "response_schema",
    "route_mode",
    "projection_id",
    "projection",
    "projection_schema",
    "projection_status",
    "source_chain_boundary",
    "safe_metadata_only",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "actual_write_enabled",
    "production_object_enabled",
    "review_queue_runtime_enabled",
    "operator_runtime_ready",
    "public_ready",
    "production_ready",
)


def _adapter_module():
    return importlib.import_module(
        "app.services.governed_nonproduction_review_console_projection"
    )


def _reader_module():
    return importlib.import_module(
        "app.services.governed_nonproduction_exact_target_read_only_audit"
    )


def _route_module():
    return importlib.import_module(
        "app.api.v1.routes.internal_alpha_review_console"
    )


def _audit_result(
    outcome: str = "exact_expected_reservation_and_record",
) -> dict[str, Any]:
    reader = _reader_module()
    result: dict[str, Any] = {
        "result_schema": reader.RESULT_SCHEMA,
        "result_version": reader.RESULT_VERSION,
        "audit_task_completed": True,
        "target_state_outcome": outcome,
        "safe_error_code": "none",
        "completed_stage": "classification",
        "target_identity_verified": False,
        "target_metadata_verified": False,
        "sidecar_preflight_passed": False,
        "sidecar_postflight_passed": False,
        "sqlite_opened": False,
        "sqlite_uri_mode_ro_verified": False,
        "sqlite_query_only_verified": False,
        "sqlite_authorizer_verified": False,
        "schema_contract_verified": False,
        "record_count_class": "not_obtained",
        "reservation_count_class": "not_obtained",
        "record_snapshot_digest": None,
        "reservation_snapshot_digest": None,
        "expected_record_present": False,
        "expected_reservation_present": False,
        "unexpected_record_present": False,
        "unexpected_reservation_present": False,
        "record_actual_columns_verified": False,
        "reservation_actual_columns_verified": False,
        "record_canonical_hash_verified": False,
        "reservation_canonical_hash_verified": False,
        "record_exact_binding_verified": False,
        "reservation_exact_binding_verified": False,
        "record_reservation_cross_binding_verified": False,
        "implementation_mutating_attempt_consumed_actual": (
            "unknown_not_safely_classified"
        ),
        "governed_nonproduction_record_exists": "unknown_not_safely_classified",
        "production_evidenceitem_created": False,
        "production_case_changed": False,
        "downstream_runtime_called": False,
        "writer_invoked": False,
        "mutation_attempted": False,
        "runtime_target_classification_performed": False,
        "physical_path_disclosed": False,
        "raw_row_disclosed": False,
        "SQL_text_disclosed": False,
        "exception_text_disclosed": False,
        "stack_trace_disclosed": False,
    }

    if outcome == "exact_expected_reservation_and_record":
        result.update(
            {
                "completed_stage": "completed",
                "target_identity_verified": True,
                "target_metadata_verified": True,
                "sidecar_preflight_passed": True,
                "sidecar_postflight_passed": True,
                "sqlite_opened": True,
                "sqlite_uri_mode_ro_verified": True,
                "sqlite_query_only_verified": True,
                "sqlite_authorizer_verified": True,
                "schema_contract_verified": True,
                "record_count_class": "exact_1",
                "reservation_count_class": "exact_1",
                "record_snapshot_digest": EXPECTED_SAFE_READY_VALUES[
                    "record_snapshot_digest"
                ],
                "reservation_snapshot_digest": EXPECTED_SAFE_READY_VALUES[
                    "reservation_snapshot_digest"
                ],
                "expected_record_present": True,
                "expected_reservation_present": True,
                "record_actual_columns_verified": True,
                "reservation_actual_columns_verified": True,
                "record_canonical_hash_verified": True,
                "reservation_canonical_hash_verified": True,
                "record_exact_binding_verified": True,
                "reservation_exact_binding_verified": True,
                "record_reservation_cross_binding_verified": True,
                "implementation_mutating_attempt_consumed_actual": "yes",
                "governed_nonproduction_record_exists": "yes",
                "runtime_target_classification_performed": True,
            }
        )
    elif outcome == "exact_empty":
        result.update(
            {
                "record_count_class": "exact_0",
                "reservation_count_class": "exact_0",
                "runtime_target_classification_performed": True,
            }
        )
    elif outcome == "exact_expected_reservation_only":
        result.update(
            {
                "record_count_class": "exact_0",
                "reservation_count_class": "exact_1",
                "expected_reservation_present": True,
                "implementation_mutating_attempt_consumed_actual": "yes",
                "runtime_target_classification_performed": True,
            }
        )

    assert tuple(result) == reader.RESULT_FIELDS
    return result


def test_adapter_module_exposes_exact_projection_contract() -> None:
    module = _adapter_module()

    assert SERVICE_PATH.is_file()
    assert callable(module.build_governed_nonproduction_review_console_projection)
    assert module.PROJECTION_FIELDS == PROJECTION_FIELDS
    assert len(module.PROJECTION_FIELDS) == 46
    assert len(set(module.PROJECTION_FIELDS)) == 46


def test_ready_projection_has_exact_fields_order_values_and_labels() -> None:
    module = _adapter_module()

    projection = module._map_audit_result_to_projection(_audit_result())

    assert tuple(projection) == PROJECTION_FIELDS
    assert projection["projection_schema"] == PROJECTION_SCHEMA
    assert projection["projection_status"] == "governed_record_review_ready"
    assert projection["review_disposition"] == "pending_human_review"
    assert projection["target_state_outcome"] == (
        "exact_expected_reservation_and_record"
    )
    for field, value in EXPECTED_SAFE_READY_VALUES.items():
        assert projection[field] == value
    assert projection["record_count_class"] == "exact_1"
    assert projection["reservation_count_class"] == "exact_1"
    assert projection["implementation_mutating_attempt_consumed"] is True
    assert projection["governed_nonproduction_record_exists"] is True
    assert projection["human_review_required"] is True
    assert projection["no_automatic_trust_upgrade"] is True
    assert projection["production_evidenceitem_created"] is False
    assert projection["production_case_changed"] is False
    assert projection["downstream_runtime_called"] is False
    assert projection["internal_read_only_projection_ready"] is True
    assert projection["operator_runtime_ready"] is False
    assert projection["production_ready"] is False
    assert projection["public_ready"] is False
    assert projection["allowed_actions"] == READY_ALLOWED_ACTIONS
    assert projection["blocked_actions"] == BLOCKED_ACTIONS
    assert projection["warnings"] == []
    assert projection["blockers"] == []


@pytest.mark.parametrize(
    ("outcome", "expected_status", "expected_record_status", "expected_blocker"),
    [
        (outcome, *mapping)
        for outcome, mapping in OUTCOME_MAP.items()
    ],
)
def test_all_seven_outcomes_map_to_one_exact_safe_shape(
    outcome: str,
    expected_status: str,
    expected_record_status: str,
    expected_blocker: str | None,
) -> None:
    module = _adapter_module()

    projection = module._map_audit_result_to_projection(_audit_result(outcome))

    assert tuple(projection) == PROJECTION_FIELDS
    assert projection["projection_status"] == expected_status
    assert projection["record_status"] == expected_record_status
    if expected_blocker is None:
        assert projection["blockers"] == []
        assert projection["allowed_actions"] == READY_ALLOWED_ACTIONS
        assert projection["internal_read_only_projection_ready"] is True
    else:
        assert projection["blockers"] == [expected_blocker]
        assert projection["allowed_actions"] == NON_READY_ALLOWED_ACTIONS
        assert projection["internal_read_only_projection_ready"] is False
        for field in SAFE_READY_FIELDS:
            assert projection[field] is None
    assert projection["blocked_actions"] == BLOCKED_ACTIONS
    assert projection["operator_runtime_ready"] is False
    assert projection["production_ready"] is False
    assert projection["public_ready"] is False


def test_malformed_or_unsafe_helper_results_fail_closed() -> None:
    module = _adapter_module()
    malformed = _audit_result()
    malformed.pop("record_count_class")
    unsafe = _audit_result()
    unsafe["production_evidenceitem_created"] = True

    for result in (malformed, unsafe, None, {"target_state_outcome": "unknown"}):
        projection = module._map_audit_result_to_projection(result)
        assert tuple(projection) == PROJECTION_FIELDS
        assert projection["target_state_outcome"] == "bounded_read_only_failure"
        assert projection["projection_status"] == (
            "governed_record_read_only_audit_failed"
        )
        assert projection["blockers"] == ["bounded_read_only_audit_failure"]
        assert projection["internal_read_only_projection_ready"] is False
        for field in SAFE_READY_FIELDS:
            assert projection[field] is None


def test_public_adapter_calls_accepted_reader_exactly_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _adapter_module()
    calls = 0

    def fake_reader(**kwargs: Any) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        assert set(kwargs) == {
            "authorized_root_path",
            "database_path",
            "target_logical_label",
            "expected_identity",
            "expected_gate_contract_binding",
            "expected_activation_decision_binding",
            "expected_input_safe_hash",
            "expected_idempotency_key",
            "expected_persisted_record_id",
            "expected_audit_receipt_reference",
            "expected_attempt_scope_key",
            "expected_attempt_reservation_id",
        }
        return _audit_result()

    monkeypatch.setattr(
        module,
        "audit_governed_nonproduction_exact_target_read_only",
        fake_reader,
    )

    projection = module.build_governed_nonproduction_review_console_projection()

    assert calls == 1
    assert projection["projection_status"] == "governed_record_review_ready"


def test_public_adapter_does_not_retry_reader_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _adapter_module()
    calls = 0

    def failing_reader(**kwargs: Any) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        raise RuntimeError("synthetic reader failure")

    monkeypatch.setattr(
        module,
        "audit_governed_nonproduction_exact_target_read_only",
        failing_reader,
    )

    projection = module.build_governed_nonproduction_review_console_projection()

    assert calls == 1
    assert projection["projection_status"] == (
        "governed_record_read_only_audit_failed"
    )
    assert projection["blockers"] == ["bounded_read_only_audit_failure"]


def test_service_source_has_no_direct_sqlite_writer_discovery_or_retry() -> None:
    source = SERVICE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_from = {
        node.module or ""
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    accepted_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "audit_governed_nonproduction_exact_target_read_only"
    ]

    assert "sqlite3" not in imported_modules
    assert all("persistence" not in module for module in imported_from)
    assert (
        "app.services.governed_nonproduction_evidence_persistence"
        not in source
    )
    assert "glob(" not in source
    assert "rglob(" not in source
    assert "os.walk" not in source
    assert "listdir" not in source
    assert "retry" not in source.casefold()
    assert len(accepted_calls) == 1


def test_dual_gates_and_unsupported_id_never_call_adapter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    route = _route_module()

    def fail_if_called() -> dict[str, Any]:
        raise AssertionError("adapter must not run for a disabled gate or unsupported ID")

    monkeypatch.setattr(
        route,
        "build_governed_nonproduction_review_console_projection",
        fail_if_called,
    )

    monkeypatch.delenv(GLOBAL_GATE, raising=False)
    monkeypatch.delenv(GOVERNED_GATE, raising=False)
    assert route.get_internal_alpha_review_console_projection(
        GOVERNED_PROJECTION_ID
    )["error"] == "route_disabled"

    monkeypatch.setenv(GLOBAL_GATE, "1")
    assert route.get_internal_alpha_review_console_projection(
        GOVERNED_PROJECTION_ID
    )["error"] == "governed_record_projection_disabled"

    monkeypatch.setenv(GOVERNED_GATE, "1")
    assert route.get_internal_alpha_review_console_projection(
        "unsupported-projection-id"
    )["error"] == "unsupported_projection"


def test_exact_governed_id_and_both_gates_call_adapter_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    route = _route_module()
    module = _adapter_module()
    calls = 0

    def fake_adapter() -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return module._map_audit_result_to_projection(_audit_result())

    monkeypatch.setenv(GLOBAL_GATE, "1")
    monkeypatch.setenv(GOVERNED_GATE, "1")
    monkeypatch.setattr(
        route,
        "build_governed_nonproduction_review_console_projection",
        fake_adapter,
    )

    payload = route.get_internal_alpha_review_console_projection(
        GOVERNED_PROJECTION_ID
    )

    assert calls == 1
    assert tuple(payload) == OUTER_RESPONSE_FIELDS
    assert payload["response_schema"] == OUTER_RESPONSE_SCHEMA
    assert payload["projection_id"] == GOVERNED_PROJECTION_ID
    assert payload["projection_schema"] == PROJECTION_SCHEMA
    assert payload["projection_status"] == "governed_record_review_ready"
    assert payload["safe_metadata_only"] is True
    assert payload["human_review_required"] is True
    assert payload["no_automatic_trust_upgrade"] is True
    assert payload["actual_write_enabled"] is False
    assert payload["production_object_enabled"] is False
    assert payload["review_queue_runtime_enabled"] is False
    assert payload["operator_runtime_ready"] is False
    assert payload["public_ready"] is False
    assert payload["production_ready"] is False


def test_existing_synthetic_ids_ignore_governed_gate_and_preserve_semantics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    route = _route_module()

    def fail_if_called() -> dict[str, Any]:
        raise AssertionError("governed adapter must not run for synthetic IDs")

    monkeypatch.setenv(GLOBAL_GATE, "1")
    monkeypatch.delenv(GOVERNED_GATE, raising=False)
    monkeypatch.setattr(
        route,
        "build_governed_nonproduction_review_console_projection",
        fail_if_called,
    )

    for projection_id in SYNTHETIC_PROJECTION_IDS:
        payload = route.get_internal_alpha_review_console_projection(projection_id)
        assert payload["response_schema"] == (
            "sentigraph_internal_alpha_review_console_route_response_v0_1"
        )
        assert payload["projection_id"] == projection_id
        assert payload["projection"]["projection_schema"] == (
            "sentigraph_internal_alpha_review_console_safe_metadata_projection_v0_1"
        )
        assert payload["actual_write_enabled"] is False
        assert payload["production_ready"] is False
        assert payload["public_ready"] is False


def test_route_source_remains_internal_get_only_without_delivery_or_mutation() -> None:
    source = ROUTE_PATH.read_text(encoding="utf-8")

    assert '@router.get("/projections/{projection_id}")' in source
    for forbidden in (
        "@router.post",
        "@router.put",
        "@router.patch",
        "@router.delete",
        "FileResponse",
        "StreamingResponse",
        "sqlite3",
        "public/",
        "customer/",
    ):
        assert forbidden not in source
