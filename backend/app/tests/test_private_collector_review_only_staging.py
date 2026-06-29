from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.services.private_collector_local_exchange_smoke import (
    run_private_collector_local_exchange_metadata_smoke,
)
from app.services.private_collector_package_resolver import REQUIRED_PACKAGE_METADATA_FILES
from app.services.private_collector_review_only_staging import (
    ALLOWED_REVIEW_ONLY_ACTIONS,
    BLOCKED_PRODUCTION_ACTIONS,
    build_review_only_staging_gate_result,
    build_safe_review_only_staging_summary,
    create_review_only_staging_candidate,
    validate_review_only_staging_input,
)


def _safe_handoff_summary(
    *,
    smoke_status: str = "ready_for_metadata_only_handoff",
    validation_status: str = "passed",
    package_resolution_status: str = "accepted_metadata_only",
    provider_result_status: str = "accepted_metadata_only",
) -> dict:
    return {
        "schema": "sentigraph_private_collector_local_exchange_smoke_summary_v0_1",
        "smoke_status": smoke_status,
        "provider_result_status": provider_result_status,
        "package_resolution_status": package_resolution_status,
        "package_name": "helldivers_package",
        "case_id": "analysis_request_fixture",
        "validation_status": validation_status,
        "evidence_count": 34,
        "source_count": 7,
        "warning_count": 0,
        "error_count": 0,
        "metadata_only": True,
        "full_evidence_rows_read": False,
        "evidence_layer_write": False,
        "production_case_created": False,
        "analysis_run_created": False,
        "forbidden_fields": [],
        "blockers": [],
        "warnings": [],
        "safe_mode": {
            "metadata_only": True,
            "runtime_file_written": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "analysis_run_created": False,
            "collector_run": False,
            "real_api_called": False,
            "real_llm_called": False,
            "url_fetching": False,
            "scraping": False,
            "evidence_items_jsonl_parsed": False,
            "evidence_items_csv_parsed": False,
        },
        "path_exposed": False,
        "path_reference": "configured_exchange_provider_result and configured_export_root package",
    }


def _write_package(root: Path, package_name: str) -> Path:
    package_dir = root / package_name
    package_dir.mkdir(parents=True)
    for filename in REQUIRED_PACKAGE_METADATA_FILES:
        target = package_dir / filename
        if filename.endswith(".json"):
            target.write_text("{}", encoding="utf-8")
        else:
            target.write_text("metadata only", encoding="utf-8")
    return package_dir


def _provider_result_payload(package_name: str = "helldivers_package", status: str = "package_ready") -> dict:
    return {
        "schema": "sentigraph_provider_job_result_v0_1",
        "provider_result_id": "provider_result_fixture",
        "provider_job_id": "provider_job_fixture",
        "request_id": "analysis_request_fixture",
        "provider_type": "private_collector_local_file",
        "adapter_id": "private_collector_metadata_only_adapter",
        "contract_version": "0.1",
        "status": status,
        "package_contract": "sentigraph_evidence_export_v1",
        "package_reference": {
            "package_name": package_name,
            "package_role": "review_ready_candidate",
            "package_index_ref": "package_index.json",
            "package_locator_strategy": "package_name_under_configured_export_root",
        },
        "metadata_summary": {"evidence_count": 34, "source_count": 7},
        "validation_summary": {"status": "passed", "errors": 0, "warnings": 0},
        "coverage_note": "Selected package coverage only; not full-web or full-platform coverage.",
        "safety_markers": {
            "raw_author_id_exported": False,
            "raw_author_name_exported": False,
            "profile_url_exported": False,
            "raw_author_id_removed": True,
            "raw_author_name_removed": True,
            "no_private_messages": True,
        },
        "created_at": "2026-06-29T00:00:00Z",
    }


def _write_provider_result(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_valid_safe_metadata_handoff_creates_ready_for_human_review_candidate() -> None:
    candidate = create_review_only_staging_candidate(_safe_handoff_summary(), requested_by="internal_operator")
    gate = build_review_only_staging_gate_result(_safe_handoff_summary(), candidate)

    assert candidate.staging_status == "ready_for_human_review"
    assert candidate.review_status == "ready_for_human_review"
    assert candidate.promotion_status == "promotion_required"
    assert candidate.package_name == "helldivers_package"
    assert candidate.analysis_request_id == "analysis_request_fixture"
    assert gate.staging_status == "ready_for_human_review"


def test_safe_8t5_smoke_result_can_create_staging_candidate(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "helldivers_package")
    provider_result_path = _write_provider_result(tmp_path / "provider_result.json", _provider_result_payload())
    smoke = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    candidate = create_review_only_staging_candidate(smoke.safe_summary, requested_by="internal_operator")

    assert candidate.staging_status == "ready_for_human_review"
    assert candidate.package_name == "helldivers_package"
    assert candidate.evidence_count == 34
    assert candidate.source_count == 7


def test_validation_warn_remains_manual_review_or_metadata_validation_warn() -> None:
    handoff = _safe_handoff_summary(smoke_status="manual_review_required", validation_status="warn")
    handoff["warnings"] = ["provider result status requires manual review: validation_warn"]
    handoff["warning_count"] = 2

    candidate = create_review_only_staging_candidate(handoff)
    gate = build_review_only_staging_gate_result(handoff, candidate)

    assert candidate.staging_status == "metadata_validation_warn"
    assert candidate.review_status == "manual_review_required"
    assert gate.staging_status == "metadata_validation_warn"


@pytest.mark.parametrize(
    "smoke_status",
    [
        "live_collection_not_authorized",
        "blocked_missing_package",
        "blocked_path_escape",
        "blocked_privacy_issue",
    ],
)
def test_blocked_smoke_statuses_propagate_safely(smoke_status: str) -> None:
    handoff = _safe_handoff_summary(smoke_status=smoke_status)
    handoff["blockers"] = [smoke_status]

    candidate = create_review_only_staging_candidate(handoff)
    gate = build_review_only_staging_gate_result(handoff, candidate)

    assert candidate.staging_status == smoke_status
    assert smoke_status in candidate.blockers
    assert gate.staging_status == smoke_status


@pytest.mark.parametrize("missing_field", ["package_name", "case_id", "validation_status"])
def test_missing_required_package_or_provider_fields_returns_blocked_metadata_contract(missing_field: str) -> None:
    handoff = _safe_handoff_summary()
    handoff.pop(missing_field)

    result = validate_review_only_staging_input(handoff)

    assert result.status == "blocked_metadata_contract"
    assert any(missing_field in blocker for blocker in result.blockers)


@pytest.mark.parametrize(
    "flag_name",
    [
        "full_evidence_rows_read",
        "evidence_layer_write",
        "production_case_created",
        "analysis_run_created",
    ],
)
def test_dangerous_true_flags_block_staging(flag_name: str) -> None:
    handoff = _safe_handoff_summary()
    handoff[flag_name] = True

    candidate = create_review_only_staging_candidate(handoff)

    if flag_name == "full_evidence_rows_read":
        assert candidate.staging_status == "blocked_evidence_rows_in_metadata_stage"
    else:
        assert candidate.staging_status == "production_import_blocked"
    assert any(flag_name in blocker for blocker in candidate.blockers)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("token", "actual-token"),
        ("raw_author_id", "actual-id"),
    ],
)
def test_actual_forbidden_fields_return_blocked_privacy_issue(field: str, value: str) -> None:
    handoff = _safe_handoff_summary()
    handoff[field] = value

    candidate = create_review_only_staging_candidate(handoff)

    assert candidate.staging_status == "blocked_privacy_issue"
    assert field in candidate.blockers[0]


def test_safe_privacy_marker_fields_are_allowed() -> None:
    handoff = _safe_handoff_summary()
    handoff["safety_markers"] = {
        "raw_author_id_exported": False,
        "raw_author_name_exported": False,
        "profile_url_exported": False,
        "raw_author_id_removed": True,
        "raw_author_name_removed": True,
        "no_private_messages": True,
    }

    candidate = create_review_only_staging_candidate(handoff)

    assert candidate.staging_status == "ready_for_human_review"
    assert candidate.blockers == []


def test_safe_staging_summary_does_not_include_absolute_filesystem_paths(tmp_path: Path) -> None:
    handoff = _safe_handoff_summary()
    handoff["operator_note"] = "safe text"
    candidate = create_review_only_staging_candidate(handoff)
    gate = build_review_only_staging_gate_result(handoff, candidate)

    summary = build_safe_review_only_staging_summary(candidate, gate)
    summary_text = json.dumps(summary, ensure_ascii=False)

    assert str(tmp_path) not in summary_text
    assert summary["path_exposed"] is False


def test_allowed_actions_are_review_only_and_blocked_actions_include_production_actions() -> None:
    candidate = create_review_only_staging_candidate(_safe_handoff_summary())

    assert set(candidate.allowed_actions) == set(ALLOWED_REVIEW_ONLY_ACTIONS)
    assert "create_production_case" not in candidate.allowed_actions
    assert "start_analysis_run" not in candidate.allowed_actions
    for action in BLOCKED_PRODUCTION_ACTIONS:
        assert action in candidate.blocked_actions


def test_helper_has_no_runtime_or_production_side_effects() -> None:
    candidate = create_review_only_staging_candidate(_safe_handoff_summary())

    assert candidate.safety_flags["metadata_only"] is True
    for flag in [
        "runtime_file_written",
        "persistent_staging_storage_created",
        "evidence_layer_written",
        "production_case_created",
        "analysis_run_created",
        "collector_run",
        "real_api_called",
        "real_llm_called",
        "url_fetching",
        "scraping",
        "evidence_items_jsonl_parsed",
        "evidence_items_csv_parsed",
    ]:
        assert candidate.safety_flags[flag] is False


def test_helper_does_not_open_or_parse_evidence_item_files(monkeypatch: pytest.MonkeyPatch) -> None:
    original_read_text = Path.read_text

    def guarded_read_text(self: Path, *args, **kwargs):
        if self.name in {"evidence_items.jsonl", "evidence_items.csv"}:
            raise AssertionError(f"{self.name} must not be parsed")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    candidate = create_review_only_staging_candidate(_safe_handoff_summary())

    assert candidate.staging_status == "ready_for_human_review"


def test_audit_refs_are_safe_and_do_not_expose_rows_or_absolute_paths(tmp_path: Path) -> None:
    candidate = create_review_only_staging_candidate(_safe_handoff_summary(), requested_by="internal_operator")
    gate = build_review_only_staging_gate_result(_safe_handoff_summary(), candidate)
    summary = build_safe_review_only_staging_summary(candidate, gate)
    summary_text = json.dumps(summary, ensure_ascii=False)

    assert summary["audit_refs"] == candidate.audit_refs
    assert str(tmp_path) not in summary_text
    assert "evidence_items.jsonl" not in summary_text
    assert "evidence_items.csv" not in summary_text
