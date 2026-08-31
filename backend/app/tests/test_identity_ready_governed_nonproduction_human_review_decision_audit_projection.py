from __future__ import annotations

import ast
import inspect
import json
import sqlite3
from pathlib import Path

import pytest

from app.api.v1.routes import internal_alpha_governed_review_decisions as route_module
from app.services import (
    identity_ready_governed_nonproduction_human_review_decision_audit_projection as service,
)
from app.services import (
    identity_ready_governed_nonproduction_human_review_decision_ledger as writer_contract,
)


SAFE_BINDING_HASH = "a" * 64
DECISION_ID = "irghrd-1660440e30c13429998b8c5b6ae14052"


def _request(
    *,
    safe_binding_hash: str = SAFE_BINDING_HASH,
    decision_type: str = "keep_pending_human_review",
) -> dict[str, object]:
    return {
        "request_schema": writer_contract.REQUEST_SCHEMA,
        "request_version": writer_contract.REQUEST_VERSION,
        "candidate": {
            "schema": writer_contract.CANDIDATE_SCHEMA,
            "mode": writer_contract.CANDIDATE_MODE,
            "identity_schema": writer_contract.IDENTITY_SCHEMA,
            "identity_version": writer_contract.IDENTITY_VERSION,
            "identity_status": writer_contract.IDENTITY_STATUS,
            "sample_handle": writer_contract.SERVER_SAMPLE_HANDLE,
            "review_subject_binding_safe_hash": safe_binding_hash,
            "decision_type": decision_type,
            "candidate_only": True,
            "persisted": False,
            "trust_upgraded": False,
            "production_object": False,
            "human_review_required": True,
            "no_automatic_trust_upgrade": True,
        },
    }


def _valid_decision() -> dict[str, object]:
    validated = writer_contract.validate_identity_ready_governed_review_decision_request(
        _request(),
        server_binding_safe_hash=SAFE_BINDING_HASH,
    )
    identity = writer_contract._identity_for(validated)
    assert identity["decision_id"] == DECISION_ID
    return writer_contract._build_decision(identity, "2026-08-27T00:00:00Z")


def _decision_for(
    safe_binding_hash: str,
    decision_type: str,
    recorded_at: str,
) -> dict[str, object]:
    validated = writer_contract.validate_identity_ready_governed_review_decision_request(
        _request(
            safe_binding_hash=safe_binding_hash,
            decision_type=decision_type,
        ),
        server_binding_safe_hash=safe_binding_hash,
    )
    return writer_contract._build_decision(
        writer_contract._identity_for(validated),
        recorded_at,
    )


def _target(root: Path) -> Path:
    return root.joinpath(*writer_contract.LOGICAL_TARGET_LABEL.split("/"))


def _write_fixture(
    root: Path,
    *,
    decision: dict[str, object] | None = None,
    decisions: list[dict[str, object]] | None = None,
    wrong_schema: bool = False,
) -> Path:
    database = _target(root)
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as connection:
        if wrong_schema:
            connection.execute(
                f"CREATE TABLE {writer_contract.PRIMARY_TABLE} (decision_id TEXT PRIMARY KEY)"
            )
        else:
            connection.execute(writer_contract.CREATE_TABLE_STATEMENT)
            rows = decisions if decisions is not None else ([decision] if decision else [])
            for item in rows:
                connection.execute(
                    f"""
                    INSERT INTO {writer_contract.PRIMARY_TABLE} (
                        decision_id,
                        idempotency_key,
                        audit_receipt_reference,
                        sample_handle,
                        review_subject_binding_safe_hash,
                        decision_type,
                        decision_canonical_hash,
                        decision_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """.strip(),
                    (
                        item["decision_id"],
                        item["idempotency_key"],
                        item["audit_receipt_reference"],
                        item["sample_handle"],
                        item["review_subject_binding_safe_hash"],
                        item["decision_type"],
                        item["decision_canonical_hash"],
                        json.dumps(
                            item,
                            ensure_ascii=False,
                            allow_nan=False,
                            separators=(",", ":"),
                        ),
                    ),
                )
        connection.commit()
    return database


def _project(root: Path, decision_id: str = DECISION_ID) -> dict[str, object]:
    return service.project_identity_ready_governed_nonproduction_human_review_decision_audit(
        authorized_root_path=root,
        database_path=_target(root),
        target_logical_label=writer_contract.LOGICAL_TARGET_LABEL,
        decision_id=decision_id,
    )


def _history(root: Path, limit: int = 20) -> dict[str, object]:
    return service.list_identity_ready_governed_nonproduction_human_review_decision_audit_projections(
        authorized_root_path=root,
        database_path=_target(root),
        target_logical_label=writer_contract.LOGICAL_TARGET_LABEL,
        limit=limit,
    )


def test_missing_parent_and_missing_database_are_bounded_404_states(tmp_path: Path) -> None:
    root = tmp_path / "repository"
    root.mkdir()

    assert _project(root) == service._bounded_result("audit_target_absent")

    _target(root).parent.mkdir(parents=True)
    assert _project(root) == service._bounded_result("audit_target_absent")


def test_wrong_schema_and_absent_exact_id_are_distinct_bounded_states(
    tmp_path: Path,
) -> None:
    wrong_schema_root = tmp_path / "wrong-schema"
    wrong_schema_root.mkdir()
    _write_fixture(wrong_schema_root, wrong_schema=True)
    assert _project(wrong_schema_root)["readback_status"] == "audit_schema_inconsistent"

    absent_id_root = tmp_path / "absent-id"
    absent_id_root.mkdir()
    _write_fixture(absent_id_root)
    assert _project(absent_id_root)["readback_status"] == "decision_not_found"


def test_one_valid_row_returns_only_the_exact_safe_projection_without_changing_bytes(
    tmp_path: Path,
) -> None:
    root = tmp_path / "valid"
    root.mkdir()
    database = _write_fixture(root, decision=_valid_decision())
    before = database.read_bytes()

    result = _project(root)

    assert tuple(result) == service.SUCCESS_FIELDS
    assert result == {
        "response_schema": service.RESPONSE_SCHEMA,
        "response_version": "0.1",
        "route_mode": service.ROUTE_MODE,
        "readback_status": "decision_audit_ready",
        "decision_id": DECISION_ID,
        "audit_receipt_reference": (
            "irghrd-receipt-1660440e30c13429998b8c5b6ae14052"
        ),
        "sample_handle": "helldivers2-psn-demo",
        "decision_type": "keep_pending_human_review",
        "decision_status": "recorded_append_only_nonproduction_identity_ready",
        "recorded_at": "2026-08-27T00:00:00Z",
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_object_enabled": False,
        "review_queue_runtime_enabled": False,
        "evidence_layer_write_performed": False,
        "provider_or_b05_called": False,
        "analysis_triggered": False,
        "report_triggered": False,
    }
    assert database.read_bytes() == before


@pytest.mark.parametrize("failure_kind", ["canonical_hash", "false_flag"])
def test_hash_and_false_flag_mismatches_fail_closed(
    tmp_path: Path,
    failure_kind: str,
) -> None:
    decision = _valid_decision()
    if failure_kind == "canonical_hash":
        decision["decision_canonical_hash"] = "f" * 64
    else:
        decision["analysis_triggered"] = True
        material = {
            field: decision[field]
            for field in writer_contract.DECISION_FIELDS
            if field != "decision_canonical_hash"
        }
        decision["decision_canonical_hash"] = writer_contract._canonical_sha256(material)
    root = tmp_path / failure_kind
    root.mkdir()
    _write_fixture(root, decision=decision)

    assert _project(root)["readback_status"] == "decision_integrity_mismatch"


def test_sidecar_preflight_blocks_before_sqlite_open(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "sidecar"
    root.mkdir()
    database = _write_fixture(root, decision=_valid_decision())
    Path(f"{database}-wal").write_bytes(b"synthetic-sidecar")
    open_calls = 0

    def fail_connect(*_args, **_kwargs):
        nonlocal open_calls
        open_calls += 1
        raise AssertionError("sqlite must not open while a sidecar exists")

    monkeypatch.setattr(service.sqlite3, "connect", fail_connect)
    assert _project(root)["readback_status"] == "sidecar_present_read_prohibited"
    assert open_calls == 0


def test_reparse_metadata_blocks_before_sqlite_open(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "reparse"
    root.mkdir()
    database = _write_fixture(root, decision=_valid_decision())
    original_metadata = service._path_metadata
    open_calls = 0

    def synthetic_metadata(path: Path):
        value = original_metadata(path)
        if path == database:
            return service._PathMetadata(True, True, False, False, True)
        return value

    def fail_connect(*_args, **_kwargs):
        nonlocal open_calls
        open_calls += 1
        raise AssertionError("sqlite must not open through reparse metadata")

    monkeypatch.setattr(service, "_path_metadata", synthetic_metadata)
    monkeypatch.setattr(service.sqlite3, "connect", fail_connect)
    assert _project(root)["readback_status"] == "target_identity_or_metadata_blocked"
    assert open_calls == 0


def test_locked_open_is_bounded_503(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "locked"
    root.mkdir()
    _write_fixture(root, decision=_valid_decision())

    def locked_connect(*_args, **_kwargs):
        raise sqlite3.OperationalError("synthetic locked fixture")

    monkeypatch.setattr(service.sqlite3, "connect", locked_connect)
    assert _project(root)["readback_status"] == "bounded_read_only_unavailable"


def test_route_is_disabled_by_default_and_maps_one_safe_projection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(route_module.IDENTITY_READY_AUDIT_PROJECTION_GATE, raising=False)
    calls = 0

    def fail_projection(**_kwargs):
        nonlocal calls
        calls += 1
        raise AssertionError("disabled route must not inspect the target")

    monkeypatch.setattr(
        route_module,
        "project_identity_ready_governed_nonproduction_human_review_decision_audit",
        fail_projection,
    )
    disabled = route_module.get_identity_ready_decision_audit_projection(DECISION_ID)
    disabled_payload = json.loads(disabled.body)
    assert disabled.status_code == 404
    assert tuple(disabled_payload) == service.ERROR_FIELDS
    assert disabled_payload["readback_status"] == "audit_target_absent"
    assert calls == 0

    monkeypatch.setenv(route_module.IDENTITY_READY_AUDIT_PROJECTION_GATE, "1")
    expected = service._success_result(_valid_decision())
    monkeypatch.setattr(
        route_module,
        "project_identity_ready_governed_nonproduction_human_review_decision_audit",
        lambda **_kwargs: expected,
    )
    response = route_module.get_identity_ready_decision_audit_projection(DECISION_ID)
    assert response.status_code == 200
    assert json.loads(response.body) == expected


def test_invalid_decision_id_never_calls_the_projection_service(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(route_module.IDENTITY_READY_AUDIT_PROJECTION_GATE, "1")
    calls = 0

    def fail_projection(**_kwargs):
        nonlocal calls
        calls += 1
        raise AssertionError("invalid identifier must not inspect the target")

    monkeypatch.setattr(
        route_module,
        "project_identity_ready_governed_nonproduction_human_review_decision_audit",
        fail_projection,
    )
    response = route_module.get_identity_ready_decision_audit_projection("not-an-id")
    payload = json.loads(response.body)
    assert response.status_code == 404
    assert payload["readback_status"] == "decision_not_found"
    assert calls == 0


def test_reader_source_has_no_writer_factory_mutation_or_network_surface() -> None:
    source = inspect.getsource(service)
    parsed = ast.parse(source)
    imported_or_called_names = {
        node.id for node in ast.walk(parsed) if isinstance(node, ast.Name)
    }
    attribute_calls = {
        node.func.attr
        for node in ast.walk(parsed)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }

    assert "IdentityReadyGovernedNonproductionHumanReviewDecisionLedger" not in source
    assert "record_identity_ready_governed_nonproduction_human_review_decision" not in source
    assert "immutable=1" not in source
    assert not {"subprocess", "socket", "httpx", "requests"}.intersection(
        imported_or_called_names
    )
    assert not {"mkdir", "write_text", "write_bytes", "unlink", "rename"}.intersection(
        attribute_calls
    )
    upper_source = source.upper()
    for forbidden_sql in ("INSERT ", "UPDATE ", "DELETE ", "REPLACE ", "CREATE TABLE"):
        assert forbidden_sql not in upper_source


def test_history_limit_is_validated_before_sqlite_open(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "limit"
    root.mkdir()
    open_calls = 0

    def fail_connect(*_args, **_kwargs):
        nonlocal open_calls
        open_calls += 1
        raise AssertionError("invalid limit must not open sqlite")

    monkeypatch.setattr(service.sqlite3, "connect", fail_connect)
    assert _history(root, 0) == service._history_bounded_result(
        "history_limit_invalid"
    )
    assert _history(root, 21) == service._history_bounded_result(
        "history_limit_invalid"
    )
    assert open_calls == 0


def test_history_returns_empty_and_one_safe_row_without_changing_bytes(
    tmp_path: Path,
) -> None:
    empty_root = tmp_path / "empty"
    empty_root.mkdir()
    empty_database = _write_fixture(empty_root)
    empty_before = empty_database.read_bytes()
    assert _history(empty_root, 1) == service._history_success_result(
        [],
        requested_limit=1,
    )
    assert empty_database.read_bytes() == empty_before

    one_root = tmp_path / "one"
    one_root.mkdir()
    one_database = _write_fixture(one_root, decision=_valid_decision())
    one_before = one_database.read_bytes()
    result = _history(one_root, 20)
    assert tuple(result) == service.HISTORY_SUCCESS_FIELDS
    assert result["history_status"] == "decision_history_ready"
    assert result["requested_limit"] == 20
    assert result["returned_count"] == 1
    assert result["ordering"] == "recorded_at_desc_decision_id_desc"
    assert tuple(result["decisions"][0]) == service.HISTORY_ROW_FIELDS
    assert result["decisions"][0]["decision_id"] == DECISION_ID
    assert not {
        "review_subject_binding_safe_hash",
        "decision_canonical_hash",
        "input_safe_hash",
        "decision_json",
    }.intersection(result["decisions"][0])
    assert result["decisions"][0]["provider_or_b05_called"] is False
    assert result["decisions"][0]["human_review_required"] is True
    assert result["decisions"][0]["no_automatic_trust_upgrade"] is True
    assert one_database.read_bytes() == one_before


def test_history_is_deterministically_ordered_and_bounded_by_requested_limit(
    tmp_path: Path,
) -> None:
    decisions = [
        _decision_for("b" * 64, "keep_pending_human_review", "2026-08-27T00:00:00Z"),
        _decision_for("c" * 64, "request_more_governance_review", "2026-08-28T00:00:00Z"),
        _decision_for("d" * 64, "keep_pending_human_review", "2026-08-28T00:00:00Z"),
    ]
    root = tmp_path / "ordered"
    root.mkdir()
    _write_fixture(root, decisions=decisions)

    result = _history(root, 2)
    expected = sorted(
        decisions,
        key=lambda item: (item["recorded_at"], item["decision_id"]),
        reverse=True,
    )[:2]
    assert result["returned_count"] == 2
    assert [item["decision_id"] for item in result["decisions"]] == [
        item["decision_id"] for item in expected
    ]


def test_history_route_reuses_gate_and_rejects_invalid_limit_without_reader_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[int] = []

    def history_reader(**kwargs):
        calls.append(kwargs["limit"])
        return service._history_success_result([], requested_limit=kwargs["limit"])

    monkeypatch.setattr(
        route_module,
        "list_identity_ready_governed_nonproduction_human_review_decision_audit_projections",
        history_reader,
    )
    monkeypatch.delenv(route_module.IDENTITY_READY_AUDIT_PROJECTION_GATE, raising=False)
    disabled = route_module.get_identity_ready_decision_audit_history(20)
    assert disabled.status_code == 404
    assert calls == []

    monkeypatch.setenv(route_module.IDENTITY_READY_AUDIT_PROJECTION_GATE, "1")
    for invalid in (0, 21, True):
        response = route_module.get_identity_ready_decision_audit_history(invalid)
        assert response.status_code == 422
    assert calls == []

    for allowed in (1, 20):
        response = route_module.get_identity_ready_decision_audit_history(allowed)
        assert response.status_code == 200
    assert calls == [1, 20]


def test_history_source_preserves_read_only_ordering_and_bounded_query_contract() -> None:
    source = inspect.getsource(
        service.list_identity_ready_governed_nonproduction_human_review_decision_audit_projections
    )
    assert "?mode=ro" in source
    assert "PRAGMA query_only = ON" in source
    assert "json_extract(decision_json, '$.recorded_at') DESC" in source
    assert "decision_id DESC LIMIT ?" in source
    assert "COUNT(*)" not in source
    assert "OFFSET" not in source.upper()
