from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.services import dense_graph_report_candidate_bridge as report_candidate_bridge
from app.services import opinion_ecosystem_dense_graph_generated_run_integration as dense_integration
from app.services.minimum_real_run_bridge_execution import (
    build_safe_minimum_real_run_bridge_execution_summary,
    execute_minimum_real_run_from_bridge_candidate,
)
from app.services.private_collector_package_resolver import REQUIRED_PACKAGE_METADATA_FILES
from app.services.private_collector_provider_result_reader import read_provider_result_metadata
from app.services.private_collector_review_only_staging import (
    build_review_only_staging_gate_result,
    build_safe_review_only_staging_summary,
    create_review_only_staging_candidate,
)
from app.services.staging_candidate_generated_run_bridge import build_staging_candidate_generated_run_bridge


ROW_SENTINEL = "ROW_SENTINEL_SHOULD_NOT_BE_READ_OR_EXPOSED_8X4"
RAW_IDENTITY_SENTINEL = "RAW_IDENTITY_SHOULD_NOT_BE_EXPOSED_8X4"
ROW_LIKE_FILES = {
    "evidence_items.jsonl",
    "evidence_items.csv",
    "source_manifest.jsonl",
    "collection_log.jsonl",
}


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
                        "raw_author_id_removed": True,
                        "raw_author_name_removed": True,
                        "profile_url_exported": False,
                    }
                ),
                encoding="utf-8",
            )
        elif filename == "validation_report.json":
            path.write_text(json.dumps({"status": "passed", "errors": 0, "warnings": 0}), encoding="utf-8")
        elif filename in ROW_LIKE_FILES:
            path.write_text(
                f"{ROW_SENTINEL},{RAW_IDENTITY_SENTINEL},not valid row content",
                encoding="utf-8",
            )
        else:
            path.write_text("metadata only; selected sample, not full-web coverage", encoding="utf-8")
    return package_dir


def _provider_result_payload(package_name: str = "synthetic_package") -> dict:
    return {
        "schema": "sentigraph_provider_job_result_v0_1",
        "provider_result_id": "provider_result_8x4_fixture",
        "provider_job_id": "provider_job_8x4_fixture",
        "request_id": "analysis_request_8x4_fixture",
        "provider_type": "private_collector_local_file",
        "adapter_id": "private_collector_metadata_only_adapter",
        "contract_version": "0.1",
        "status": "package_ready",
        "package_contract": "sentigraph_evidence_export_v1",
        "package_reference": {
            "package_name": package_name,
            "package_role": "review_ready_candidate",
            "package_index_ref": "package_index.json",
            "package_locator_strategy": "package_name_under_configured_export_root",
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


def _build_review_only_staging_summary(provider_result_path: Path, export_root: Path) -> dict:
    reader_result = read_provider_result_metadata(provider_result_path, export_root)
    provider_summary = reader_result.safe_summary
    package_summary = provider_summary.get("package_summary")
    validation_summary = provider_summary.get("validation_summary")
    metadata_summary = provider_summary.get("metadata_summary")
    package_summary = package_summary if isinstance(package_summary, dict) else {}
    validation_summary = validation_summary if isinstance(validation_summary, dict) else {}
    metadata_summary = metadata_summary if isinstance(metadata_summary, dict) else {}
    handoff_summary = {
        "schema": "sentigraph_private_collector_provider_handoff_summary_v0_1",
        "smoke_status": "ready_for_metadata_only_handoff",
        "provider_result_status": reader_result.status,
        "package_resolution_status": package_summary.get("status"),
        "provider_result_id": provider_summary.get("provider_result_id"),
        "provider_job_id": provider_summary.get("provider_job_id"),
        "package_name": package_summary.get("package_name"),
        "case_id": provider_summary.get("request_id"),
        "validation_status": validation_summary.get("status"),
        "evidence_count": metadata_summary.get("evidence_count"),
        "source_count": metadata_summary.get("source_count"),
        "warning_count": validation_summary.get("warnings"),
        "error_count": validation_summary.get("errors"),
        "coverage_note": provider_summary.get("coverage_note"),
        "metadata_only": True,
        "full_evidence_rows_read": False,
        "evidence_layer_write": False,
        "production_case_created": False,
        "analysis_run_created": False,
        "forbidden_fields": list(reader_result.forbidden_fields),
        "blockers": list(reader_result.errors),
        "warnings": list(reader_result.warnings),
        "safe_mode": dict(reader_result.safe_mode),
        "path_exposed": False,
        "path_reference": "configured_export_root package",
    }
    candidate = create_review_only_staging_candidate(handoff_summary, requested_by="8x4_wrapper_execution_smoke")
    gate = build_review_only_staging_gate_result(handoff_summary, candidate)
    return build_safe_review_only_staging_summary(candidate, gate)


def test_metadata_bridge_executes_minimum_real_run_wrapper_only_in_controlled_test_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    export_root = tmp_path / "exports"
    _write_synthetic_package(export_root, "synthetic_package")
    provider_result_path = _write_provider_result(tmp_path / "exchange" / "provider_result.json", _provider_result_payload())
    original_read_text = Path.read_text

    def guarded_read_text(self: Path, *args, **kwargs):
        if self.name in ROW_LIKE_FILES:
            raise AssertionError(f"{self.name} must not be opened or parsed in 8X-4 metadata bridge smoke")
        return original_read_text(self, *args, **kwargs)

    def fail_dense_graph(*args, **kwargs):
        raise AssertionError("dense graph must not be called in 8X-4")

    def fail_report_candidate(*args, **kwargs):
        raise AssertionError("report candidate must not be created in 8X-4")

    monkeypatch.setattr(Path, "read_text", guarded_read_text)
    monkeypatch.setattr(dense_integration, "generate_opinion_ecosystem_run_with_dense_graph_attachment", fail_dense_graph)
    monkeypatch.setattr(report_candidate_bridge, "build_dense_graph_report_candidate_from_integration", fail_report_candidate)
    monkeypatch.setattr(report_candidate_bridge, "create_dense_graph_report_candidate_from_integration", fail_report_candidate)

    staging_summary = _build_review_only_staging_summary(provider_result_path, export_root)
    bridge = build_staging_candidate_generated_run_bridge(staging_summary, created_by="8x4_wrapper_execution_smoke")
    execution = execute_minimum_real_run_from_bridge_candidate(bridge, created_by="8x4_wrapper_execution_smoke")
    safe_execution = build_safe_minimum_real_run_bridge_execution_summary(execution)
    generated_run = execution["generated_run"]
    encoded = json.dumps({"staging": staging_summary, "bridge": bridge, "execution": execution}, ensure_ascii=False)

    assert bridge["bridge_status"] == "ready_for_minimum_real_run_input_candidate"
    assert execution["execution_status"] == "executed_local_minimum_real_run"
    assert execution["execution_mode"] == "controlled_backend_only_minimum_real_run"
    assert execution["metadata_only"] is True
    assert execution["minimum_real_run_executed"] is True
    assert execution["dense_graph_called"] is False
    assert execution["evidence_rows_parsed"] is False
    assert generated_run is not None
    assert generated_run["run_schema"] == "sentigraph_opinion_ecosystem_run_v0_1"
    assert generated_run["run_status"] == "blocked"
    assert generated_run["blockers"]
    assert generated_run["blockers"][0]["reason"] == "required_fixture_metadata_missing"
    assert generated_run["human_review_required"] is True
    assert generated_run["coefficient_source"] == "mock_default"
    assert generated_run["calibration_status"] == "uncalibrated"
    assert generated_run["empirical_validation"] == "not_started"
    assert generated_run["boundary_flags"]["not_prediction"] is True
    assert generated_run["boundary_flags"]["not_causal_proof"] is True
    assert generated_run["boundary_flags"]["not_official_verification"] is True
    assert generated_run["boundary_flags"]["not_production_score"] is True
    assert generated_run["boundary_flags"]["human_review_required"] is True
    assert generated_run["boundary_flags"]["no_auto_execute"] is True
    assert generated_run["runtime_side_effects"]["called_real_api"] is False
    assert generated_run["runtime_side_effects"]["called_real_llm"] is False
    assert generated_run["runtime_side_effects"]["parsed_evidence_items_file"] is False
    assert generated_run["runtime_side_effects"]["wrote_evidence_layer"] is False
    assert generated_run["runtime_side_effects"]["created_production_case"] is False
    assert generated_run["runtime_side_effects"]["created_analysis_run"] is False
    assert generated_run["runtime_side_effects"]["generated_response_text"] is False
    assert execution["boundary_flags"]["provider_output_is_evidence_not_truth"] is True
    assert execution["boundary_flags"]["human_review_required"] is True
    assert execution["boundary_flags"]["not_official_verification"] is True
    assert execution["boundary_flags"]["not_causal_proof"] is True
    assert execution["boundary_flags"]["not_prediction"] is True
    assert execution["boundary_flags"]["not_production_score"] is True
    assert all(flag_value is False for flag_value in execution["runtime_side_effects"].values())
    assert "call_dense_graph_directly" in execution["downstream_blocked_actions"]
    assert "generate_report" in execution["downstream_blocked_actions"]
    assert "generate_sandbox_or_public_event" in execution["downstream_blocked_actions"]
    assert safe_execution["minimum_real_run_executed"] is True
    assert safe_execution["dense_graph_called"] is False
    assert safe_execution["evidence_rows_parsed"] is False
    assert safe_execution["path_exposed"] is False
    assert ROW_SENTINEL not in encoded
    assert RAW_IDENTITY_SENTINEL not in encoded
    assert str(tmp_path) not in encoded
