from __future__ import annotations

import json
import socket
import urllib.request
from pathlib import Path

import pytest

from app.services import report_candidate_final_report_boundary
from app.services import source11_governance_handoff_finalsummaryreport_adapter
from app.services.dense_graph_report_candidate_bridge import (
    build_dense_graph_report_candidate_from_integration,
    build_safe_dense_graph_report_candidate_summary,
)
from app.services.generated_run_dense_graph_bridge_integration import (
    integrate_generated_run_with_dense_graph_from_execution,
)
from app.services.minimum_real_run_bridge_execution import execute_minimum_real_run_from_bridge_candidate
from app.services.private_collector_package_resolver import REQUIRED_PACKAGE_METADATA_FILES
from app.services.private_collector_provider_result_reader import read_provider_result_metadata
from app.services.private_collector_review_only_staging import (
    build_review_only_staging_gate_result,
    build_safe_review_only_staging_summary,
    create_review_only_staging_candidate,
)
from app.services.staging_candidate_generated_run_bridge import build_staging_candidate_generated_run_bridge


ROW_SENTINEL = "ROW_SENTINEL_SHOULD_NOT_BE_READ_OR_EXPOSED_8X10"
RAW_IDENTITY_SENTINEL = "RAW_IDENTITY_SHOULD_NOT_BE_EXPOSED_8X10"
PROFILE_URL_SENTINEL = "PROFILE_URL_SENTINEL_SHOULD_NOT_BE_EXPOSED_8X10"
SECRET_SENTINEL = "SECRET_SENTINEL_SHOULD_NOT_BE_EXPOSED_8X10"
ROW_LIKE_FILES = {
    "evidence_items.jsonl",
    "evidence_items.csv",
    "source_manifest.jsonl",
    "collection_log.jsonl",
}
FORBIDDEN_OUTPUT_KEYS = {
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "public_url",
    "signed_url",
    "download_url",
    "file_byte_route",
    "pdf_path",
    "markdown_report_path",
    "briefing_deck_path",
    "zip_path",
    "package_path",
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
                f"{ROW_SENTINEL},{RAW_IDENTITY_SENTINEL},{SECRET_SENTINEL},not valid row content",
                encoding="utf-8",
            )
        else:
            path.write_text("metadata only; selected sample, not full-web coverage", encoding="utf-8")
    return package_dir


def _provider_result_payload(package_name: str = "synthetic_package") -> dict:
    return {
        "schema": "sentigraph_provider_job_result_v0_1",
        "provider_result_id": "provider_result_8x10_report_candidate",
        "provider_job_id": "provider_job_8x10_report_candidate",
        "request_id": "analysis_request_8x10_report_candidate",
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
    candidate = create_review_only_staging_candidate(handoff_summary, requested_by="8x10_report_candidate_smoke")
    gate = build_review_only_staging_gate_result(handoff_summary, candidate)
    return build_safe_review_only_staging_summary(candidate, gate)


def _build_dense_graph_integration(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict:
    export_root = tmp_path / "exports"
    _write_synthetic_package(export_root, "synthetic_package")
    provider_result_path = _write_provider_result(
        tmp_path / "exchange" / "provider_result.json",
        _provider_result_payload(),
    )
    original_read_text = Path.read_text

    def guarded_read_text(self: Path, *args, **kwargs):
        if self.name in ROW_LIKE_FILES:
            raise AssertionError(f"{self.name} must not be opened or parsed in 8X-10 report candidate smoke")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)
    staging_summary = _build_review_only_staging_summary(provider_result_path, export_root)
    bridge = build_staging_candidate_generated_run_bridge(staging_summary, created_by="8x10_report_candidate_smoke")
    bridge["minimum_real_run_input_candidate"]["fixture_metadata"]["stage_id"] = "T0"
    execution = execute_minimum_real_run_from_bridge_candidate(bridge, created_by="8x10_report_candidate_smoke")
    return integrate_generated_run_with_dense_graph_from_execution(execution, created_by="8x10_report_candidate_smoke")


def _encoded(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _walk_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(_walk_keys(child))
    return keys


def _assert_runtime_side_effects_false(value: dict) -> None:
    runtime_side_effects = value.get("runtime_side_effects")
    assert isinstance(runtime_side_effects, dict)
    assert all(flag_value is False for flag_value in runtime_side_effects.values())


def _blocker_reasons(value: dict) -> set[str]:
    blockers = value.get("blockers")
    if not isinstance(blockers, list):
        return set()
    return {str(blocker.get("reason")) for blocker in blockers if isinstance(blocker, dict)}


def _install_external_side_effect_guards(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_final_report(*args, **kwargs):
        raise AssertionError("FinalSummaryReport boundary/runtime must not be called in 8X-10")

    def fail_network(*args, **kwargs):
        raise AssertionError("network access must not occur in 8X-10")

    monkeypatch.setattr(
        report_candidate_final_report_boundary,
        "build_report_candidate_final_report_boundary",
        fail_final_report,
    )
    monkeypatch.setattr(
        report_candidate_final_report_boundary,
        "create_report_candidate_final_report_boundary",
        fail_final_report,
    )
    monkeypatch.setattr(
        source11_governance_handoff_finalsummaryreport_adapter,
        "build_source11_governance_handoff_finalsummaryreport_adapter",
        fail_final_report,
    )
    monkeypatch.setattr(
        source11_governance_handoff_finalsummaryreport_adapter,
        "create_source11_governance_handoff_finalsummaryreport_adapter",
        fail_final_report,
    )
    monkeypatch.setattr(socket, "create_connection", fail_network)
    monkeypatch.setattr(urllib.request, "urlopen", fail_network)


def test_dense_graph_preview_reaches_local_report_candidate_without_final_report_or_export(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_external_side_effect_guards(monkeypatch)

    integration = _build_dense_graph_integration(tmp_path, monkeypatch)
    candidate = build_dense_graph_report_candidate_from_integration(integration, created_by="8x10_report_candidate_smoke")
    summary = build_safe_dense_graph_report_candidate_summary(candidate)
    report_summary = candidate["report_candidate_summary"]
    encoded = _encoded({"integration": integration, "candidate": candidate, "summary": summary})

    assert integration["integration_status"] == "integrated_backend_dense_graph_preview"
    assert integration["dense_graph_executed"] is True
    assert integration["dense_graph_summary"]["dense_graph_attached"] is True
    assert integration["dense_graph_summary"]["frontend_ready"] is False
    assert integration["dense_graph_summary"]["route_ready"] is False
    assert integration["dense_graph_summary"]["production_ready"] is False
    assert integration["boundary_flags"]["anonymous_aggregate_only"] is True
    assert integration["boundary_flags"]["not_full_web"] is True
    assert integration["boundary_flags"]["not_full_platform"] is True
    assert integration["boundary_flags"]["not_full_thread"] is True
    assert integration["boundary_flags"]["not_official_verification"] is True
    assert integration["boundary_flags"]["not_causal_proof"] is True
    assert integration["boundary_flags"]["not_prediction"] is True
    assert integration["boundary_flags"]["not_production_score"] is True
    assert integration["boundary_flags"]["human_review_required"] is True
    _assert_runtime_side_effects_false(integration)

    assert candidate["report_candidate_schema"] == "sentigraph_dense_graph_report_candidate_v0_1"
    assert candidate["report_candidate_status"] == "candidate_ready"
    assert candidate["input_source_kind"] == "generated_run_dense_graph_bridge_integration"
    assert candidate["candidate_mode"] == "backend_only_local_report_candidate"
    assert candidate["report_candidate_created"] is True
    assert candidate["dense_graph_integration_schema"] == "sentigraph_generated_run_dense_graph_bridge_integration_v0_1"
    assert candidate["dense_graph_summary"]["dense_graph_attached"] is True
    assert report_summary["candidate_scope"] == "selected_sample_only_dense_graph_preview"
    assert report_summary["human_review_required"] is True
    assert report_summary["final_report_ready"] is False
    assert report_summary["export_ready"] is False
    assert report_summary["public_ready"] is False
    assert report_summary["b_end_runtime_ready"] is False
    assert report_summary["sandbox_public_event_ready"] is False
    assert candidate["final_report_created"] is False
    assert candidate["b_end_report_runtime_generated"] is False
    assert candidate["sandbox_public_event_generated"] is False
    assert candidate["export_artifact_created"] is False
    assert candidate["generated_response_text"] is False
    assert candidate["public_route_created"] is False
    assert candidate["frontend_integration_approved"] is False
    assert candidate["frontend_ready"] is False
    assert candidate["route_ready"] is False
    assert candidate["production_ready"] is False
    assert bool(candidate.get("customer_ready", False)) is False
    assert candidate["boundary_flags"]["human_review_required"] is True
    assert candidate["boundary_flags"]["not_final_report"] is True
    assert candidate["boundary_flags"]["not_b_end_report_runtime"] is True
    assert candidate["boundary_flags"]["not_sandbox_public_event_runtime"] is True
    assert candidate["boundary_flags"]["not_export_artifact"] is True
    assert candidate["boundary_flags"]["not_official_verification"] is True
    assert candidate["boundary_flags"]["not_causal_proof"] is True
    assert candidate["boundary_flags"]["not_prediction"] is True
    assert candidate["boundary_flags"]["not_production_score"] is True
    _assert_runtime_side_effects_false(candidate)
    assert candidate["runtime_side_effects"]["parsed_evidence_items_file"] is False
    assert candidate["runtime_side_effects"]["read_original_package_rows"] is False
    assert candidate["runtime_side_effects"]["wrote_evidence_layer"] is False
    assert candidate["runtime_side_effects"]["created_production_case"] is False
    assert candidate["runtime_side_effects"]["created_analysis_run"] is False
    assert candidate["runtime_side_effects"]["created_final_report"] is False
    assert candidate["runtime_side_effects"]["generated_b_end_report_runtime"] is False
    assert candidate["runtime_side_effects"]["generated_sandbox_runtime"] is False
    assert candidate["runtime_side_effects"]["generated_public_event_runtime"] is False
    assert candidate["runtime_side_effects"]["created_export_artifact"] is False
    assert candidate["runtime_side_effects"]["created_download_package"] is False
    assert candidate["runtime_side_effects"]["performed_external_delivery"] is False
    assert summary["report_candidate_created"] is True
    assert summary["final_report_ready"] is False
    assert summary["export_ready"] is False
    assert summary["public_ready"] is False
    assert summary["b_end_runtime_ready"] is False
    assert summary["sandbox_public_event_ready"] is False
    assert not (FORBIDDEN_OUTPUT_KEYS & _walk_keys(candidate))
    assert ROW_SENTINEL not in encoded
    assert RAW_IDENTITY_SENTINEL not in encoded
    assert SECRET_SENTINEL not in encoded
    assert str(tmp_path) not in encoded


def test_wrong_or_missing_dense_graph_preview_blocks_report_candidate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    integration = _build_dense_graph_integration(tmp_path, monkeypatch)
    variants = [
        dict(integration, integration_status="blocked_metadata_contract"),
        dict(integration, dense_graph_executed=False),
        dict(integration, dense_graph_integration=None),
        dict(integration, dense_graph_summary=None),
    ]

    for value in variants:
        candidate = build_dense_graph_report_candidate_from_integration(value)

        assert candidate["report_candidate_status"] == "blocked_metadata_contract"
        assert candidate["report_candidate_created"] is False
        assert candidate["final_report_created"] is False
        assert candidate["export_artifact_created"] is False
        assert candidate["public_route_created"] is False
        _assert_runtime_side_effects_false(candidate)


def test_readiness_flags_block_report_candidate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for flag in ("frontend_ready", "route_ready", "production_ready"):
        integration = _build_dense_graph_integration(tmp_path / flag, monkeypatch)
        integration["dense_graph_summary"][flag] = True

        candidate = build_dense_graph_report_candidate_from_integration(integration)

        assert candidate["report_candidate_status"] == "blocked_requested_side_effect"
        assert candidate["report_candidate_created"] is False
        assert candidate["frontend_ready"] is False
        assert candidate["route_ready"] is False
        assert candidate["production_ready"] is False
        _assert_runtime_side_effects_false(candidate)


def test_customer_ready_flag_blocks_report_candidate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    integration = _build_dense_graph_integration(tmp_path, monkeypatch)
    integration["customer_ready"] = True

    candidate = build_dense_graph_report_candidate_from_integration(integration)

    assert candidate["report_candidate_status"] == "blocked_requested_side_effect"
    assert candidate["report_candidate_created"] is False
    assert bool(candidate.get("customer_ready", False)) is False
    _assert_runtime_side_effects_false(candidate)


def test_forbidden_fields_block_without_exposing_values(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    integration = _build_dense_graph_integration(tmp_path, monkeypatch)
    integration.update(
        {
            "raw_author_name": RAW_IDENTITY_SENTINEL,
            "profile_url": PROFILE_URL_SENTINEL,
            "token": SECRET_SENTINEL,
            "full_evidence_rows": [ROW_SENTINEL],
        }
    )

    candidate = build_dense_graph_report_candidate_from_integration(integration)
    encoded = _encoded(candidate)

    assert candidate["report_candidate_status"] in {"blocked_privacy_issue", "blocked_forbidden_input"}
    assert candidate["report_candidate_created"] is False
    assert RAW_IDENTITY_SENTINEL not in encoded
    assert PROFILE_URL_SENTINEL not in encoded
    assert SECRET_SENTINEL not in encoded
    assert ROW_SENTINEL not in encoded
