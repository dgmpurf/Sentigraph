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
)


def _write_synthetic_package(export_root: Path, package_name: str) -> Path:
    package_dir = export_root / package_name
    package_dir.mkdir(parents=True)
    for filename in REQUIRED_PACKAGE_METADATA_FILES:
        path = package_dir / filename
        if filename == "manifest.json":
            path.write_text(
                json.dumps(
                    {
                        "schema": "sentigraph_evidence_export_manifest_v1",
                        "package_name": package_name,
                    }
                ),
                encoding="utf-8",
            )
        elif filename == "validation_report.json":
            path.write_text(
                json.dumps({"status": "passed", "errors": 0, "warnings": 0}),
                encoding="utf-8",
            )
        elif filename in {"evidence_items.jsonl", "evidence_items.csv"}:
            path.write_text("", encoding="utf-8")
        else:
            path.write_text("metadata only", encoding="utf-8")
    return package_dir


def _provider_result_payload(
    *,
    package_name: str = "helldivers_package",
    status: str = "package_ready",
    locator_strategy: str = "package_name_under_configured_export_root",
) -> dict:
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
            "package_locator_strategy": locator_strategy,
        },
        "metadata_summary": {
            "evidence_count": 34,
            "source_count": 7,
            "comment_count": 28,
        },
        "validation_summary": {
            "status": "passed",
            "errors": 0,
            "warnings": 0,
        },
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


def _run_staging_chain(tmp_path: Path, payload: dict | None = None, *, write_package: bool = True) -> dict:
    package_name = (payload or {}).get("package_reference", {}).get("package_name", "helldivers_package")
    export_root = tmp_path / "exports"
    if write_package:
        _write_synthetic_package(export_root, package_name)
    else:
        export_root.mkdir(parents=True)
    provider_result_path = _write_provider_result(
        tmp_path / "exchange" / "provider_result.json",
        payload or _provider_result_payload(package_name=package_name),
    )

    smoke = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)
    candidate = create_review_only_staging_candidate(smoke.safe_summary, requested_by="integration_smoke")
    gate = build_review_only_staging_gate_result(smoke.safe_summary, candidate)
    summary = build_safe_review_only_staging_summary(candidate, gate)
    return {"smoke": smoke, "candidate": candidate, "gate": gate, "summary": summary}


def test_valid_synthetic_chain_reaches_ready_for_human_review(tmp_path: Path) -> None:
    result = _run_staging_chain(tmp_path)

    assert result["smoke"].smoke_status == "ready_for_metadata_only_handoff"
    assert result["candidate"].staging_status == "ready_for_human_review"
    assert result["candidate"].review_status == "ready_for_human_review"
    assert result["gate"].staging_status == "ready_for_human_review"
    assert result["summary"]["staging_status"] == "ready_for_human_review"


def test_valid_chain_returns_required_safe_summary_fields(tmp_path: Path) -> None:
    summary = _run_staging_chain(tmp_path)["summary"]

    assert summary["package_name"] == "helldivers_package"
    assert summary["case_id_hint"] == "analysis_request_fixture"
    assert summary["validation_status"] == "passed"
    assert summary["evidence_count"] == 34
    assert summary["source_count"] == 7
    assert summary["warning_count"] == 0
    assert summary["error_count"] == 0


def test_safe_staging_summary_does_not_include_absolute_filesystem_paths(tmp_path: Path) -> None:
    summary = _run_staging_chain(tmp_path)["summary"]
    summary_text = json.dumps(summary, ensure_ascii=False)

    assert str(tmp_path) not in summary_text
    assert summary["path_exposed"] is False


def test_evidence_item_files_are_not_opened_or_parsed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    original_read_text = Path.read_text

    def guarded_read_text(self: Path, *args, **kwargs):
        if self.name in {"evidence_items.jsonl", "evidence_items.csv"}:
            raise AssertionError(f"{self.name} must not be opened or parsed")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    result = _run_staging_chain(tmp_path)

    assert result["summary"]["staging_status"] == "ready_for_human_review"


def test_allowed_actions_contain_only_review_only_actions(tmp_path: Path) -> None:
    candidate = _run_staging_chain(tmp_path)["candidate"]

    assert set(candidate.allowed_actions) == set(ALLOWED_REVIEW_ONLY_ACTIONS)
    assert "create_production_case" not in candidate.allowed_actions
    assert "start_analysis_run" not in candidate.allowed_actions
    assert "publish" not in candidate.allowed_actions


def test_blocked_actions_include_production_import_report_public_and_execute_actions(tmp_path: Path) -> None:
    candidate = _run_staging_chain(tmp_path)["candidate"]

    for action in BLOCKED_PRODUCTION_ACTIONS:
        assert action in candidate.blocked_actions
    for action in ["create_production_case", "start_analysis_run", "generate_report", "generate_public_event"]:
        assert action in candidate.blocked_actions
    for action in ["publish", "send", "post", "execute"]:
        assert action in candidate.blocked_actions


def test_validation_warn_stays_metadata_validation_warn_not_production_ready(tmp_path: Path) -> None:
    payload = _provider_result_payload(status="validation_warn")
    payload["validation_summary"] = {"status": "warn", "errors": 0, "warnings": 2}
    result = _run_staging_chain(tmp_path, payload)

    assert result["smoke"].smoke_status == "manual_review_required"
    assert result["candidate"].staging_status == "metadata_validation_warn"
    assert result["candidate"].review_status == "manual_review_required"
    assert result["summary"]["promotion_status"] == "promotion_required"


def test_live_collection_not_authorized_remains_blocked(tmp_path: Path) -> None:
    result = _run_staging_chain(tmp_path, _provider_result_payload(status="live_collection_not_authorized"))

    assert result["smoke"].smoke_status == "live_collection_not_authorized"
    assert result["candidate"].staging_status == "live_collection_not_authorized"
    assert result["summary"]["staging_status"] == "live_collection_not_authorized"


def test_blocked_missing_package_propagates_safely(tmp_path: Path) -> None:
    result = _run_staging_chain(tmp_path, write_package=False)

    assert result["smoke"].smoke_status == "blocked_missing_package"
    assert result["candidate"].staging_status == "blocked_missing_package"
    assert result["summary"]["gate_result"]["package_resolution_status"] == "blocked_missing_package"


def test_blocked_path_escape_propagates_safely(tmp_path: Path) -> None:
    payload = _provider_result_payload(
        package_name="escape_package",
        locator_strategy="package_path_relative_to_export_root",
    )
    payload["package_reference"]["package_path_relative_to_export_root"] = "../escape_package"
    result = _run_staging_chain(tmp_path, payload, write_package=False)

    assert result["smoke"].smoke_status == "blocked_path_escape"
    assert result["candidate"].staging_status == "blocked_path_escape"
    assert result["summary"]["gate_result"]["package_resolution_status"] == "blocked_path_escape"


def test_blocked_privacy_issue_propagates_safely(tmp_path: Path) -> None:
    payload = _provider_result_payload()
    payload["raw_author_id"] = "actual-id"
    result = _run_staging_chain(tmp_path, payload)

    assert result["smoke"].smoke_status == "blocked_privacy_issue"
    assert result["candidate"].staging_status == "blocked_privacy_issue"
    assert result["summary"]["gate_result"]["privacy_status"] == "blocked_privacy_issue"


@pytest.mark.parametrize("field", ["token", "raw_author_id"])
def test_provider_metadata_with_actual_forbidden_fields_blocks_privacy_issue(tmp_path: Path, field: str) -> None:
    payload = _provider_result_payload()
    payload[field] = "actual-value"
    result = _run_staging_chain(tmp_path, payload)

    assert result["smoke"].smoke_status == "blocked_privacy_issue"
    assert result["candidate"].staging_status == "blocked_privacy_issue"
    assert field in result["smoke"].safe_summary["forbidden_fields"]


def test_safe_privacy_marker_fields_are_allowed(tmp_path: Path) -> None:
    payload = _provider_result_payload()
    payload["safety_markers"]["raw_author_id_exported"] = False
    payload["safety_markers"]["raw_author_id_removed"] = True
    result = _run_staging_chain(tmp_path, payload)

    assert result["smoke"].smoke_status == "ready_for_metadata_only_handoff"
    assert result["candidate"].staging_status == "ready_for_human_review"
    assert result["summary"]["blockers"] == []


@pytest.mark.parametrize(
    ("flag", "expected_status"),
    [
        ("full_evidence_rows_read", "blocked_evidence_rows_in_metadata_stage"),
        ("evidence_layer_write", "production_import_blocked"),
        ("production_case_created", "production_import_blocked"),
        ("analysis_run_created", "production_import_blocked"),
    ],
)
def test_dangerous_true_handoff_flags_block_staging(tmp_path: Path, flag: str, expected_status: str) -> None:
    result = _run_staging_chain(tmp_path)
    handoff = dict(result["smoke"].safe_summary)
    handoff[flag] = True

    candidate = create_review_only_staging_candidate(handoff)
    gate = build_review_only_staging_gate_result(handoff, candidate)
    summary = build_safe_review_only_staging_summary(candidate, gate)

    assert summary["staging_status"] == expected_status
    assert any(flag in blocker for blocker in summary["blockers"])


def test_no_persistent_staging_storage_is_created(tmp_path: Path) -> None:
    _run_staging_chain(tmp_path)

    assert not list(tmp_path.rglob("review_only_staging*.json"))
    assert not list(tmp_path.rglob("staging_candidate*.json"))
    assert not list(tmp_path.rglob("*.sqlite"))
    assert not list(tmp_path.rglob("*.db"))


def test_no_route_ui_or_project_source_integration_exists() -> None:
    repo_root = Path(__file__).resolve().parents[3]

    assert not (repo_root / "frontend" / "src" / "pages" / "PrivateCollectorReviewOnlyStaging.jsx").exists()
    assert not (repo_root / "backend" / "app" / "api" / "v1" / "routes" / "private_collector_staging.py").exists()
    assert not (repo_root / "docs" / "project_sources").exists()
