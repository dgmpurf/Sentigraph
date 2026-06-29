from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.services.private_collector_local_exchange_smoke import (
    run_private_collector_local_exchange_metadata_smoke,
)
from app.services.private_collector_package_resolver import REQUIRED_PACKAGE_METADATA_FILES


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


def test_valid_local_exchange_fixture_returns_ready_for_metadata_only_handoff(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "helldivers_package")
    provider_result_path = _write_provider_result(tmp_path / "exchange" / "provider_result.json", _provider_result_payload())

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    assert result.smoke_status == "ready_for_metadata_only_handoff"
    assert result.provider_result_status == "accepted_metadata_only"
    assert result.package_resolution_status == "accepted_metadata_only"
    assert result.package_name == "helldivers_package"
    assert result.case_id == "analysis_request_fixture"
    assert result.metadata_only is True
    assert result.full_evidence_rows_read is False


def test_missing_provider_result_json_returns_blocked_missing_provider_result(tmp_path: Path) -> None:
    result = run_private_collector_local_exchange_metadata_smoke(
        tmp_path / "missing" / "provider_result.json",
        tmp_path / "exports",
    )

    assert result.smoke_status == "blocked_missing_provider_result"
    assert any("provider_result JSON file not found" in blocker for blocker in result.blockers)


def test_invalid_provider_result_schema_returns_needs_fix_metadata_contract(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "bad_schema_package")
    payload = _provider_result_payload(package_name="bad_schema_package")
    payload["schema"] = "sentigraph_provider_job_result_v9"
    provider_result_path = _write_provider_result(tmp_path / "provider_result.json", payload)

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    assert result.smoke_status == "needs_fix_metadata_contract"
    assert any("unsupported schema" in blocker for blocker in result.blockers)


def test_package_ready_with_safe_package_returns_metadata_only_ready_status(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "ready_package")
    provider_result_path = _write_provider_result(
        tmp_path / "provider_result.json",
        _provider_result_payload(package_name="ready_package", status="package_ready"),
    )

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    assert result.smoke_status == "ready_for_metadata_only_handoff"
    assert result.provider_result_status == "accepted_metadata_only"


def test_validation_warn_remains_manual_review_or_warning_oriented(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "warn_package")
    payload = _provider_result_payload(package_name="warn_package", status="validation_warn")
    payload["validation_summary"] = {"status": "warn", "errors": 0, "warnings": 2}
    provider_result_path = _write_provider_result(tmp_path / "provider_result.json", payload)

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    assert result.smoke_status == "manual_review_required"
    assert result.validation_status == "warn"
    assert any("manual review" in warning for warning in result.warnings)


def test_live_collection_not_authorized_remains_blocked(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "blocked_package")
    provider_result_path = _write_provider_result(
        tmp_path / "provider_result.json",
        _provider_result_payload(package_name="blocked_package", status="live_collection_not_authorized"),
    )

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    assert result.smoke_status == "live_collection_not_authorized"
    assert any("live_collection_not_authorized" in blocker for blocker in result.blockers)


def test_blocked_missing_package_propagates_safely(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    export_root.mkdir()
    provider_result_path = _write_provider_result(
        tmp_path / "provider_result.json",
        _provider_result_payload(package_name="missing_package"),
    )

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    assert result.smoke_status == "blocked_missing_package"
    assert result.package_resolution_status == "blocked_missing_package"


def test_blocked_path_escape_propagates_safely(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    export_root.mkdir()
    payload = _provider_result_payload(
        package_name="escape_package",
        locator_strategy="package_path_relative_to_export_root",
    )
    payload["package_reference"]["package_path_relative_to_export_root"] = "../escape_package"
    provider_result_path = _write_provider_result(tmp_path / "provider_result.json", payload)

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    assert result.smoke_status == "blocked_path_escape"
    assert result.package_resolution_status == "blocked_path_escape"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("token", "actual-token"),
        ("raw_author_id", "actual-id"),
    ],
)
def test_forbidden_provider_metadata_returns_blocked_privacy_issue(tmp_path: Path, field: str, value: str) -> None:
    payload = _provider_result_payload()
    payload[field] = value
    provider_result_path = _write_provider_result(tmp_path / "provider_result.json", payload)

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, tmp_path / "exports")

    assert result.smoke_status == "blocked_privacy_issue"
    assert field in result.safe_summary["forbidden_fields"]


def test_safety_marker_fields_are_allowed(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "marker_package")
    payload = _provider_result_payload(package_name="marker_package")
    payload["safety_markers"]["raw_author_id_exported"] = False
    payload["safety_markers"]["raw_author_id_removed"] = True
    provider_result_path = _write_provider_result(tmp_path / "provider_result.json", payload)

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    assert result.smoke_status == "ready_for_metadata_only_handoff"
    assert result.safe_summary["forbidden_fields"] == []


def test_safe_smoke_summary_does_not_include_absolute_filesystem_paths(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "safe_package")
    provider_result_path = _write_provider_result(
        tmp_path / "provider_result.json",
        _provider_result_payload(package_name="safe_package"),
    )

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)
    summary_text = json.dumps(result.safe_summary, ensure_ascii=False)

    assert str(tmp_path) not in summary_text
    assert str(export_root) not in summary_text
    assert result.safe_summary["path_exposed"] is False


def test_evidence_item_files_are_not_opened_or_parsed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "safe_package")
    provider_result_path = _write_provider_result(
        tmp_path / "provider_result.json",
        _provider_result_payload(package_name="safe_package"),
    )
    original_read_text = Path.read_text

    def guarded_read_text(self: Path, *args, **kwargs):
        if self.name in {"evidence_items.jsonl", "evidence_items.csv"}:
            raise AssertionError(f"{self.name} must not be parsed")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    assert result.smoke_status == "ready_for_metadata_only_handoff"


def test_smoke_helper_has_no_runtime_or_production_side_effects(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "safe_package")
    provider_result_path = _write_provider_result(
        tmp_path / "provider_result.json",
        _provider_result_payload(package_name="safe_package"),
    )

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    assert result.evidence_layer_write is False
    assert result.production_case_created is False
    assert result.analysis_run_created is False
    for flag in [
        "runtime_file_written",
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
        assert result.safe_summary["safe_mode"][flag] is False


def test_smoke_helper_uses_tmp_fixture_without_real_collector_export_root(tmp_path: Path) -> None:
    export_root = tmp_path / "synthetic_exports"
    _write_package(export_root, "synthetic_package")
    provider_result_path = _write_provider_result(
        tmp_path / "synthetic_exchange" / "provider_result.json",
        _provider_result_payload(package_name="synthetic_package"),
    )

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    assert result.smoke_status == "ready_for_metadata_only_handoff"
    assert result.package_name == "synthetic_package"


def test_smoke_helper_produces_concise_safe_summary_counts(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "count_package")
    payload = _provider_result_payload(package_name="count_package")
    payload["metadata_summary"] = {"evidence_count": 34, "source_count": 7}
    payload["validation_summary"] = {"status": "passed", "errors": 0, "warnings": 2}
    provider_result_path = _write_provider_result(tmp_path / "provider_result.json", payload)

    result = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    assert result.safe_summary["package_name"] == "count_package"
    assert result.safe_summary["case_id"] == "analysis_request_fixture"
    assert result.safe_summary["validation_status"] == "passed"
    assert result.safe_summary["evidence_count"] == 34
    assert result.safe_summary["source_count"] == 7
    assert result.safe_summary["warning_count"] == 2
    assert result.safe_summary["error_count"] == 0
