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


PACKAGE_NAME = "controlled_exported_package_fixture"
SENTINEL_ROW_SECRET = "sentinel-row-token-should-never-appear"
SENTINEL_AUTHOR_VALUE = "sentinel-raw-author-should-never-appear"
PRIVATE_COLLECTOR_PATH_SENTINEL = "G:/private-collector/should-never-appear"


FORBIDDEN_OUTPUT_MARKERS = (
    SENTINEL_ROW_SECRET,
    SENTINEL_AUTHOR_VALUE,
    PRIVATE_COLLECTOR_PATH_SENTINEL,
    "actual-profile-url-should-never-appear",
    "actual-private-message-should-never-appear",
    "actual-cookie-should-never-appear",
    "actual-session-should-never-appear",
    "actual-token-should-never-appear",
    "actual-secret-should-never-appear",
    "actual-browser-profile-should-never-appear",
    "actual-response-text-should-never-appear",
    "actual-generated-public-message-should-never-appear",
    "target-user-list-should-never-appear",
    "persuasion-score-should-never-appear",
    "truth-score-should-never-appear",
    "official-verified-should-never-appear",
    "prediction-probability-should-never-appear",
    "psychological-profile-should-never-appear",
    "personality-diagnosis-should-never-appear",
    "auto-execute-should-never-appear",
    "publish-now-should-never-appear",
    "send-now-should-never-appear",
    "post-now-should-never-appear",
    "execute-now-should-never-appear",
)


def _write_controlled_export_package(export_root: Path, package_name: str = PACKAGE_NAME) -> Path:
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
                        "case_id": "controlled_case_fixture",
                        "case_title": "Controlled exported package metadata smoke",
                        "evidence_count": 12,
                        "source_count": 3,
                        "raw_author_id_exported": False,
                        "raw_author_name_exported": False,
                        "profile_url_exported": False,
                        "raw_author_id_removed": True,
                        "raw_author_name_removed": True,
                        "no_private_messages": True,
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
        elif filename == "validation_report.json":
            path.write_text(
                json.dumps(
                    {
                        "status": "passed",
                        "errors": 0,
                        "warnings": 1,
                        "coverage_note": "metadata-only fixture; not full-web or full-platform coverage",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
        elif filename == "coverage_note.md":
            path.write_text(
                "Selected package metadata fixture only. Not full-web, not full-platform, not official verification.",
                encoding="utf-8",
            )
        elif filename == "validation_report.md":
            path.write_text("status: passed\nwarnings: 1\n", encoding="utf-8")
        elif filename == "README.md":
            path.write_text("Controlled metadata-only package fixture for Sentigraph tests.", encoding="utf-8")
        elif filename == "source_manifest.jsonl":
            path.write_text('{"source_id":"source_fixture","platform":"forum","safe_metadata_only":true}\n', encoding="utf-8")
        elif filename == "collection_log.jsonl":
            path.write_text('{"event":"fixture_created","safe_metadata_only":true}\n', encoding="utf-8")
        elif filename == "evidence_items.jsonl":
            path.write_text(
                "this is deliberately invalid jsonl and must not be parsed "
                f"{SENTINEL_ROW_SECRET} raw_author_id={SENTINEL_AUTHOR_VALUE}\n",
                encoding="utf-8",
            )
        elif filename == "evidence_items.csv":
            path.write_text(
                "this,is,deliberately,not,a,real,evidence,row,"
                f"{SENTINEL_ROW_SECRET},{SENTINEL_AUTHOR_VALUE}\n",
                encoding="utf-8",
            )
        else:
            path.write_text("metadata only", encoding="utf-8")
    return package_dir


def _provider_result_payload(
    *,
    package_name: str = PACKAGE_NAME,
    locator_strategy: str = "package_name_under_configured_export_root",
) -> dict:
    return {
        "schema": "sentigraph_provider_job_result_v0_1",
        "provider_result_id": "provider_result_controlled_metadata_smoke",
        "provider_job_id": "provider_job_controlled_metadata_smoke",
        "request_id": "analysis_request_controlled_metadata_smoke",
        "provider_type": "private_collector_local_file",
        "adapter_id": "private_collector_metadata_only_adapter",
        "contract_version": "0.1",
        "status": "package_ready",
        "package_contract": "sentigraph_evidence_export_v1",
        "package_reference": {
            "package_name": package_name,
            "package_role": "review_ready_candidate",
            "package_index_ref": "package_index.json",
            "package_locator_strategy": locator_strategy,
        },
        "metadata_summary": {
            "evidence_count": 12,
            "source_count": 3,
            "warning_count": 1,
            "error_count": 0,
        },
        "validation_summary": {
            "status": "passed",
            "errors": 0,
            "warnings": 1,
        },
        "coverage_note": "Controlled metadata fixture only; not full-web and not full-platform coverage.",
        "safety_markers": {
            "raw_author_id_exported": False,
            "raw_author_name_exported": False,
            "profile_url_exported": False,
            "raw_author_id_removed": True,
            "raw_author_name_removed": True,
            "no_private_messages": True,
        },
        "created_at": "2026-07-01T00:00:00Z",
    }


def _write_provider_result(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def _serialized_safe_outputs(*values: object) -> str:
    return json.dumps(values, ensure_ascii=False, sort_keys=True, default=str)


def _assert_no_unsafe_output(serialized_output: str, tmp_path: Path) -> None:
    for marker in FORBIDDEN_OUTPUT_MARKERS:
        assert marker not in serialized_output
    assert str(tmp_path) not in serialized_output


def test_controlled_exported_package_metadata_chain_reaches_review_only_staging(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    export_root = tmp_path / "exports"
    _write_controlled_export_package(export_root)
    provider_result_path = _write_provider_result(
        tmp_path / "exchange" / "provider_result.json",
        _provider_result_payload(),
    )

    original_read_text = Path.read_text

    def guarded_read_text(self: Path, *args, **kwargs):
        if self.name in {"evidence_items.jsonl", "evidence_items.csv"}:
            raise AssertionError(f"{self.name} must remain presence-only in metadata smoke")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    reader_result = read_provider_result_metadata(provider_result_path, export_root)
    smoke = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)
    candidate = create_review_only_staging_candidate(smoke.safe_summary, requested_by="controlled_metadata_smoke")
    gate = build_review_only_staging_gate_result(smoke.safe_summary, candidate)
    summary = build_safe_review_only_staging_summary(candidate, gate)

    assert reader_result.status == "accepted_metadata_only"
    assert reader_result.resolver_result is not None
    assert reader_result.resolver_result.status == "accepted_metadata_only"
    assert reader_result.resolver_result.required_files_presence["evidence_items.jsonl"] is True
    assert reader_result.resolver_result.required_files_presence["evidence_items.csv"] is True
    assert reader_result.safe_summary["schema"] == "sentigraph_private_collector_provider_handoff_summary_v0_1"

    assert smoke.smoke_status == "ready_for_metadata_only_handoff"
    assert smoke.safe_summary["metadata_only"] is True
    assert smoke.safe_summary["full_evidence_rows_read"] is False
    assert smoke.safe_summary["evidence_layer_write"] is False
    assert smoke.safe_summary["production_case_created"] is False
    assert smoke.safe_summary["analysis_run_created"] is False

    assert candidate.staging_status == "ready_for_human_review"
    assert candidate.review_status == "ready_for_human_review"
    assert candidate.promotion_status == "promotion_required"
    assert candidate.safety_flags["metadata_only"] is True
    assert candidate.safety_flags["full_evidence_rows_parsed"] is False
    assert candidate.safety_flags["evidence_layer_written"] is False
    assert candidate.safety_flags["production_case_created"] is False
    assert candidate.safety_flags["analysis_run_created"] is False

    assert gate.staging_status == "ready_for_human_review"
    assert gate.evidence_row_boundary_status == "evidence_rows_not_read"
    assert summary["metadata_only"] is True
    assert summary["path_exposed"] is False
    assert summary["gate_result"]["package_resolution_status"] == "accepted_metadata_only"
    assert summary["allowed_actions"] == list(candidate.allowed_actions)
    assert "create_production_case" not in summary["allowed_actions"]
    assert "start_analysis_run" not in summary["allowed_actions"]
    assert "publish" not in summary["allowed_actions"]
    for blocked_action in ("create_production_case", "start_analysis_run", "publish", "send", "post", "execute"):
        assert blocked_action in summary["blocked_actions"]

    serialized_output = _serialized_safe_outputs(reader_result.safe_summary, smoke.safe_summary, summary)
    _assert_no_unsafe_output(serialized_output, tmp_path)

    assert not list(tmp_path.rglob("review_only_staging*.json"))
    assert not list(tmp_path.rglob("staging_candidate*.json"))
    assert not list(tmp_path.rglob("evidence_layer*.json"))
    assert not list(tmp_path.rglob("production_case*.json"))
    assert not list(tmp_path.rglob("analysis_run*.json"))


@pytest.mark.parametrize(
    ("package_reference_update", "expected_status", "expect_staging_block"),
    [
        (
            {
                "package_name": "../escape_package",
                "package_locator_strategy": "package_name_under_configured_export_root",
            },
            "needs_fix_metadata_contract",
            False,
        ),
        (
            {
                "package_name": "escape_package",
                "package_locator_strategy": "package_path_relative_to_export_root",
                "package_path_relative_to_export_root": "../escape_package",
            },
            "blocked_path_escape",
            True,
        ),
    ],
)
def test_controlled_metadata_smoke_blocks_path_traversal(
    tmp_path: Path,
    package_reference_update: dict,
    expected_status: str,
    expect_staging_block: bool,
) -> None:
    export_root = tmp_path / "exports"
    export_root.mkdir()
    payload = _provider_result_payload()
    payload["package_reference"].update(package_reference_update)
    provider_result_path = _write_provider_result(tmp_path / "exchange" / "provider_result.json", payload)

    reader_result = read_provider_result_metadata(provider_result_path, export_root)
    smoke = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)

    assert reader_result.status == expected_status
    assert smoke.smoke_status == expected_status
    if expect_staging_block:
        candidate = create_review_only_staging_candidate(smoke.safe_summary, requested_by="controlled_metadata_smoke")
        assert candidate.staging_status in {expected_status, "blocked_metadata_contract"}
    serialized_output = _serialized_safe_outputs(reader_result.safe_summary, smoke.safe_summary)
    _assert_no_unsafe_output(serialized_output, tmp_path)


def test_controlled_metadata_smoke_blocks_actual_forbidden_metadata_field(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_controlled_export_package(export_root)
    payload = _provider_result_payload()
    payload["token"] = "actual-token-should-never-appear"
    provider_result_path = _write_provider_result(tmp_path / "exchange" / "provider_result.json", payload)

    reader_result = read_provider_result_metadata(provider_result_path, export_root)
    smoke = run_private_collector_local_exchange_metadata_smoke(provider_result_path, export_root)
    candidate = create_review_only_staging_candidate(smoke.safe_summary, requested_by="controlled_metadata_smoke")

    assert reader_result.status == "blocked_privacy_issue"
    assert smoke.smoke_status == "blocked_privacy_issue"
    assert candidate.staging_status == "blocked_privacy_issue"
    assert "token" in reader_result.forbidden_fields
    serialized_output = _serialized_safe_outputs(reader_result.safe_summary, smoke.safe_summary)
    assert "actual-token-should-never-appear" not in serialized_output
    assert str(tmp_path) not in serialized_output
