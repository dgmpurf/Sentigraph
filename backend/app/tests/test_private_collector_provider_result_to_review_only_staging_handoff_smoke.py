from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.services.private_collector_local_exchange_smoke import (
    run_private_collector_local_exchange_metadata_smoke,
)
from app.services.private_collector_package_resolver import REQUIRED_PACKAGE_METADATA_FILES
from app.services.private_collector_provider_result_reader import read_provider_result_metadata
from app.services.private_collector_review_only_staging import (
    build_review_only_staging_gate_result,
    build_safe_review_only_staging_summary,
    create_review_only_staging_candidate,
)


ROW_SENTINEL = "ROW_SENTINEL_SHOULD_NOT_BE_READ_OR_EXPOSED"
RAW_IDENTITY_SENTINEL = "RAW_IDENTITY_SHOULD_NOT_BE_EXPOSED"
ROW_LIKE_FILES = {
    "evidence_items.jsonl",
    "evidence_items.csv",
    "source_manifest.jsonl",
    "collection_log.jsonl",
}


def _write_synthetic_package(export_root: Path, package_name: str, *, forbidden_metadata: bool = False) -> Path:
    package_dir = export_root / package_name
    package_dir.mkdir(parents=True)
    for filename in REQUIRED_PACKAGE_METADATA_FILES:
        path = package_dir / filename
        if filename == "manifest.json":
            manifest = {
                "schema": "sentigraph_evidence_export_manifest_v1",
                "package_name": package_name,
                "raw_author_id_removed": True,
                "raw_author_name_removed": True,
                "profile_url_exported": False,
            }
            if forbidden_metadata:
                manifest["token"] = "actual-token-should-block"
            path.write_text(json.dumps(manifest), encoding="utf-8")
        elif filename == "validation_report.json":
            path.write_text(json.dumps({"status": "passed", "errors": 0, "warnings": 0}), encoding="utf-8")
        elif filename in ROW_LIKE_FILES:
            path.write_text(
                f"{ROW_SENTINEL},{RAW_IDENTITY_SENTINEL},not valid json or csv rows",
                encoding="utf-8",
            )
        else:
            path.write_text("metadata only; selected sample, not full-web coverage", encoding="utf-8")
    return package_dir


def _provider_result_payload(
    *,
    package_name: str = "synthetic_package",
    status: str = "package_ready",
    locator_strategy: str = "package_name_under_configured_export_root",
) -> dict:
    return {
        "schema": "sentigraph_provider_job_result_v0_1",
        "provider_result_id": "provider_result_8x1_fixture",
        "provider_job_id": "provider_job_8x1_fixture",
        "request_id": "analysis_request_8x1_fixture",
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


def _build_staging_summary_from_provider_result(provider_result_path: Path, export_root: Path) -> dict:
    smoke = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)
    candidate = create_review_only_staging_candidate(smoke.safe_summary, requested_by="8x1_handoff_smoke")
    gate = build_review_only_staging_gate_result(smoke.safe_summary, candidate)
    return build_safe_review_only_staging_summary(candidate, gate)


def test_provider_result_metadata_reader_to_review_only_staging_is_metadata_only(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    export_root = tmp_path / "exports"
    _write_synthetic_package(export_root, "synthetic_package")
    provider_result_path = _write_provider_result(tmp_path / "exchange" / "provider_result.json", _provider_result_payload())
    original_read_text = Path.read_text

    def guarded_read_text(self: Path, *args, **kwargs):
        if self.name in ROW_LIKE_FILES:
            raise AssertionError(f"{self.name} must not be opened or parsed in metadata-only handoff")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    reader_result = read_provider_result_metadata(provider_result_path, export_root)
    staging_summary = _build_staging_summary_from_provider_result(provider_result_path, export_root)
    summary_text = json.dumps(staging_summary, ensure_ascii=False)

    assert reader_result.status == "accepted_metadata_only"
    assert reader_result.resolver_result is not None
    assert reader_result.resolver_result.status == "accepted_metadata_only"
    assert reader_result.safe_mode["metadata_only"] is True
    assert reader_result.safe_mode["evidence_items_jsonl_parsed"] is False
    assert reader_result.safe_mode["evidence_items_csv_parsed"] is False
    assert staging_summary["staging_status"] == "ready_for_human_review"
    assert staging_summary["review_status"] == "ready_for_human_review"
    assert staging_summary["metadata_only"] is True
    assert staging_summary["safety_flags"]["metadata_only"] is True
    assert staging_summary["safety_flags"]["evidence_items_jsonl_parsed"] is False
    assert staging_summary["safety_flags"]["evidence_items_csv_parsed"] is False
    assert staging_summary["safety_flags"]["evidence_layer_written"] is False
    assert staging_summary["safety_flags"]["production_case_created"] is False
    assert staging_summary["safety_flags"]["analysis_run_created"] is False
    assert ROW_SENTINEL not in summary_text
    assert RAW_IDENTITY_SENTINEL not in summary_text
    assert str(tmp_path) not in summary_text


def test_path_escape_blocks_before_review_only_staging_can_be_ready(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    export_root.mkdir()
    payload = _provider_result_payload(
        package_name="escape_package",
        locator_strategy="package_path_relative_to_export_root",
    )
    payload["package_reference"]["package_path_relative_to_export_root"] = "../escape_package"
    provider_result_path = _write_provider_result(tmp_path / "exchange" / "provider_result.json", payload)

    reader_result = read_provider_result_metadata(provider_result_path, export_root)
    staging_summary = _build_staging_summary_from_provider_result(provider_result_path, export_root)

    assert reader_result.status == "blocked_path_escape"
    assert staging_summary["staging_status"] == "blocked_path_escape"
    assert staging_summary["gate_result"]["package_resolution_status"] == "blocked_path_escape"
    assert staging_summary["safety_flags"]["evidence_layer_written"] is False
    assert staging_summary["safety_flags"]["production_case_created"] is False
    assert staging_summary["safety_flags"]["analysis_run_created"] is False


def test_forbidden_package_metadata_blocks_privacy_issue_without_exposing_raw_values(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_synthetic_package(export_root, "unsafe_package", forbidden_metadata=True)
    provider_result_path = _write_provider_result(
        tmp_path / "exchange" / "provider_result.json",
        _provider_result_payload(package_name="unsafe_package"),
    )

    reader_result = read_provider_result_metadata(provider_result_path, export_root)
    staging_summary = _build_staging_summary_from_provider_result(provider_result_path, export_root)
    summary_text = json.dumps(staging_summary, ensure_ascii=False)

    assert reader_result.status == "blocked_privacy_issue"
    assert "token" in reader_result.forbidden_fields
    assert staging_summary["staging_status"] == "blocked_privacy_issue"
    assert staging_summary["gate_result"]["privacy_status"] == "blocked_privacy_issue"
    assert "actual-token-should-block" not in summary_text
    assert ROW_SENTINEL not in summary_text
    assert RAW_IDENTITY_SENTINEL not in summary_text


def test_provider_metadata_with_forbidden_actual_identity_blocks_before_staging_ready(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_synthetic_package(export_root, "synthetic_package")
    payload = _provider_result_payload()
    payload["raw_author_id"] = "raw-author-id-should-block"
    provider_result_path = _write_provider_result(tmp_path / "exchange" / "provider_result.json", payload)

    reader_result = read_provider_result_metadata(provider_result_path, export_root)
    staging_summary = _build_staging_summary_from_provider_result(provider_result_path, export_root)
    summary_text = json.dumps(staging_summary, ensure_ascii=False)

    assert reader_result.status == "blocked_privacy_issue"
    assert "raw_author_id" in reader_result.forbidden_fields
    assert staging_summary["staging_status"] == "blocked_privacy_issue"
    assert "raw-author-id-should-block" not in summary_text
