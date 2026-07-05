from __future__ import annotations

import json
import socket
import urllib.request
from pathlib import Path

import pytest

from app.services import download_public_access_boundary_final_delivery_boundary
from app.services import export_artifact_boundary_download_public_access_boundary
from app.services import export_gate_handoff_export_artifact_boundary
from app.services import finalsummaryreport_boundary_export_gate_handoff
from app.services import source11_governance_handoff_finalsummaryreport_adapter
from app.services.dense_graph_report_candidate_bridge import build_dense_graph_report_candidate_from_integration
from app.services.final_report_boundary_source11_governance_handoff import (
    build_final_report_boundary_source11_governance_handoff,
    build_safe_final_report_boundary_source11_governance_handoff_summary,
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
from app.services.report_candidate_final_report_boundary import build_report_candidate_final_report_boundary
from app.services.staging_candidate_generated_run_bridge import build_staging_candidate_generated_run_bridge


ROW_SENTINEL = "ROW_SENTINEL_SHOULD_NOT_BE_READ_OR_EXPOSED_8X14"
RAW_IDENTITY_SENTINEL = "RAW_IDENTITY_SHOULD_NOT_BE_EXPOSED_8X14"
PROFILE_URL_SENTINEL = "PROFILE_URL_SENTINEL_SHOULD_NOT_BE_EXPOSED_8X14"
SECRET_SENTINEL = "SECRET_SENTINEL_SHOULD_NOT_BE_EXPOSED_8X14"
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
    "source11_final_summary_report_id",
    "final_summary_report_id",
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
        "provider_result_id": "provider_result_8x14_source11_handoff",
        "provider_job_id": "provider_job_8x14_source11_handoff",
        "request_id": "analysis_request_8x14_source11_handoff",
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
    candidate = create_review_only_staging_candidate(handoff_summary, requested_by="8x14_source11_handoff_smoke")
    gate = build_review_only_staging_gate_result(handoff_summary, candidate)
    return build_safe_review_only_staging_summary(candidate, gate)


def _build_finalsummaryreport_boundary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict:
    export_root = tmp_path / "exports"
    _write_synthetic_package(export_root, "synthetic_package")
    provider_result_path = _write_provider_result(
        tmp_path / "exchange" / "provider_result.json",
        _provider_result_payload(),
    )
    original_read_text = Path.read_text

    def guarded_read_text(self: Path, *args, **kwargs):
        if self.name in ROW_LIKE_FILES:
            raise AssertionError(f"{self.name} must not be opened or parsed in 8X-14 Source 11 handoff smoke")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)
    staging_summary = _build_review_only_staging_summary(provider_result_path, export_root)
    bridge = build_staging_candidate_generated_run_bridge(staging_summary, created_by="8x14_source11_handoff_smoke")
    bridge["minimum_real_run_input_candidate"]["fixture_metadata"]["stage_id"] = "T0"
    execution = execute_minimum_real_run_from_bridge_candidate(bridge, created_by="8x14_source11_handoff_smoke")
    integration = integrate_generated_run_with_dense_graph_from_execution(
        execution,
        created_by="8x14_source11_handoff_smoke",
    )
    report_candidate = build_dense_graph_report_candidate_from_integration(
        integration,
        created_by="8x14_source11_handoff_smoke",
    )
    return build_report_candidate_final_report_boundary(
        report_candidate,
        created_by="8x14_source11_handoff_smoke",
    )


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


def _install_downstream_side_effect_guards(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_downstream(*args, **kwargs):
        raise AssertionError("Source 11 runtime/export/public delivery must not be called in 8X-14")

    def fail_network(*args, **kwargs):
        raise AssertionError("network access must not occur in 8X-14")

    for module in (
        source11_governance_handoff_finalsummaryreport_adapter,
        finalsummaryreport_boundary_export_gate_handoff,
        export_gate_handoff_export_artifact_boundary,
        export_artifact_boundary_download_public_access_boundary,
        download_public_access_boundary_final_delivery_boundary,
    ):
        for name in dir(module):
            if name.startswith(("build_", "create_")):
                monkeypatch.setattr(module, name, fail_downstream)

    monkeypatch.setattr(socket, "create_connection", fail_network)
    monkeypatch.setattr(urllib.request, "urlopen", fail_network)


def test_finalsummaryreport_boundary_reaches_source11_handoff_without_runtime_or_export(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_downstream_side_effect_guards(monkeypatch)

    boundary = _build_finalsummaryreport_boundary(tmp_path, monkeypatch)
    handoff = build_final_report_boundary_source11_governance_handoff(
        boundary,
        created_by="8x14_source11_handoff_smoke",
    )
    summary = build_safe_final_report_boundary_source11_governance_handoff_summary(handoff)
    encoded = _encoded({"boundary": boundary, "handoff": handoff, "summary": summary})

    assert boundary["final_report_boundary_schema"] == "sentigraph_report_candidate_final_report_boundary_v0_1"
    assert boundary["final_report_boundary_status"] == "boundary_ready"
    assert boundary["final_report_boundary_created"] is True
    assert boundary["boundary_mode"] == "backend_only_local_final_report_boundary"
    assert boundary["source11_final_summary_report_runtime_used"] is False
    assert boundary["final_summary_report_created"] is False
    assert boundary["final_report_created"] is False
    assert boundary["b_end_report_runtime_generated"] is False
    assert boundary["frontend_ready"] is False
    assert boundary["route_ready"] is False
    assert boundary["production_ready"] is False
    assert boundary["customer_ready"] is False
    assert boundary["export_ready"] is False
    assert boundary["public_ready"] is False
    assert boundary["human_review_required"] is True
    assert boundary["boundary_flags"]["not_full_web"] is True
    assert boundary["boundary_flags"]["not_full_platform"] is True
    assert boundary["boundary_flags"]["not_official_verification"] is True
    assert boundary["boundary_flags"]["not_causal_proof"] is True
    assert boundary["boundary_flags"]["not_prediction"] is True
    assert boundary["boundary_flags"]["not_production_score"] is True
    _assert_runtime_side_effects_false(boundary)

    assert handoff["source11_governance_handoff_schema"] == (
        "sentigraph_final_report_boundary_source11_governance_handoff_v0_1"
    )
    assert handoff["source11_governance_handoff_status"] == "handoff_ready_for_manual_source11_governance_review"
    assert handoff["source11_governance_handoff_created"] is True
    assert handoff["handoff_mode"] == "backend_only_local_source11_governance_handoff"
    assert handoff["input_source_kind"] == "final_report_boundary"
    assert handoff["final_report_boundary_schema"] == "sentigraph_report_candidate_final_report_boundary_v0_1"
    assert handoff["final_report_boundary_status"] == "boundary_ready"
    assert handoff["human_review_required"] is True
    assert handoff["human_review_status"] == "required"
    assert handoff["source11_runtime_called"] is False
    assert handoff["source11_final_summary_report_runtime_used"] is False
    assert handoff["final_summary_report_created"] is False
    assert handoff["final_report_created"] is False
    assert handoff["b_end_report_runtime_generated"] is False
    assert handoff["sandbox_public_event_generated"] is False
    assert handoff["export_artifact_created"] is False
    assert handoff["download_package_created"] is False
    assert handoff["public_access_created"] is False
    assert handoff["external_delivery_performed"] is False
    assert handoff["generated_response_text"] is False
    assert handoff["public_route_created"] is False
    assert handoff["frontend_ready"] is False
    assert handoff["route_ready"] is False
    assert handoff["production_ready"] is False
    assert handoff["customer_ready"] is False
    assert handoff["export_ready"] is False
    assert handoff["public_ready"] is False
    assert handoff["boundary_flags"]["source11_runtime_not_used"] is True
    assert handoff["boundary_flags"]["not_final_summary_report"] is True
    assert handoff["boundary_flags"]["not_export_ready"] is True
    assert handoff["boundary_flags"]["not_public_ready"] is True
    assert handoff["boundary_flags"]["not_customer_ready"] is True
    assert handoff["runtime_side_effects"]["parsed_evidence_items_file"] is False
    assert handoff["runtime_side_effects"]["read_original_package_rows"] is False
    assert handoff["runtime_side_effects"]["wrote_evidence_layer"] is False
    assert handoff["runtime_side_effects"]["created_production_case"] is False
    assert handoff["runtime_side_effects"]["created_production_analysis_run"] is False
    assert handoff["runtime_side_effects"]["used_source11_final_summary_report_runtime"] is False
    assert handoff["runtime_side_effects"]["generated_final_summary_report"] is False
    assert handoff["runtime_side_effects"]["generated_b_end_report_runtime"] is False
    assert handoff["runtime_side_effects"]["generated_sandbox_runtime"] is False
    assert handoff["runtime_side_effects"]["generated_public_event_runtime"] is False
    assert handoff["runtime_side_effects"]["generated_export_artifact"] is False
    assert handoff["runtime_side_effects"]["generated_download_package"] is False
    assert handoff["runtime_side_effects"]["generated_public_access"] is False
    assert handoff["runtime_side_effects"]["performed_external_delivery"] is False
    assert handoff["runtime_side_effects"]["generated_response_text"] is False
    assert handoff["runtime_side_effects"]["created_public_route"] is False
    assert handoff["downstream_policy"]["source11_manual_review_ready"] is True
    assert handoff["downstream_policy"]["source11_runtime_ready"] is False
    assert handoff["downstream_policy"]["final_summary_report_ready"] is False
    assert handoff["downstream_policy"]["export_ready"] is False
    assert handoff["downstream_policy"]["download_ready"] is False
    assert handoff["downstream_policy"]["public_access_ready"] is False
    assert handoff["downstream_policy"]["external_delivery_ready"] is False
    assert summary["source11_governance_handoff_created"] is True
    assert summary["source11_manual_review_ready"] is True
    assert summary["source11_runtime_ready"] is False
    assert summary["final_summary_report_created"] is False
    assert summary["export_ready"] is False
    assert summary["public_ready"] is False
    assert summary["customer_ready"] is False

    assert not (FORBIDDEN_OUTPUT_KEYS & _walk_keys(handoff))
    assert ROW_SENTINEL not in encoded
    assert RAW_IDENTITY_SENTINEL not in encoded
    assert SECRET_SENTINEL not in encoded
    assert str(tmp_path) not in encoded


def test_wrong_or_missing_finalsummaryreport_boundary_blocks_source11_handoff(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    boundary = _build_finalsummaryreport_boundary(tmp_path, monkeypatch)
    variants = [
        dict(boundary, final_report_boundary_schema="unknown"),
        dict(boundary, final_report_boundary_status="blocked_metadata_contract"),
        dict(boundary, final_report_boundary_summary=None),
    ]

    for value in variants:
        handoff = build_final_report_boundary_source11_governance_handoff(value)

        assert handoff["source11_governance_handoff_status"] == "blocked_metadata_contract"
        assert handoff["source11_governance_handoff_created"] is False
        assert handoff["source11_runtime_called"] is False
        assert handoff["source11_final_summary_report_runtime_used"] is False
        assert handoff["final_summary_report_created"] is False
        assert handoff["b_end_report_runtime_generated"] is False
        assert handoff["sandbox_public_event_generated"] is False
        assert handoff["export_artifact_created"] is False
        _assert_runtime_side_effects_false(handoff)


def test_source11_runtime_and_downstream_readiness_flags_block_handoff(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source11_boundary = _build_finalsummaryreport_boundary(tmp_path / "source11", monkeypatch)
    source11_boundary["source11_final_summary_report_runtime_used"] = True

    handoff = build_final_report_boundary_source11_governance_handoff(source11_boundary)

    assert handoff["source11_governance_handoff_status"] == "blocked_source11_runtime_request"
    assert handoff["source11_governance_handoff_created"] is False
    assert handoff["source11_runtime_called"] is False
    assert handoff["source11_final_summary_report_runtime_used"] is False

    for flag in ("frontend_ready", "route_ready", "production_ready", "customer_ready", "export_ready", "public_ready"):
        boundary = _build_finalsummaryreport_boundary(tmp_path / flag, monkeypatch)
        boundary[flag] = True

        blocked = build_final_report_boundary_source11_governance_handoff(boundary)

        assert blocked["source11_governance_handoff_status"] == "blocked_requested_side_effect"
        assert blocked["source11_governance_handoff_created"] is False
        assert blocked["frontend_ready"] is False
        assert blocked["route_ready"] is False
        assert blocked["production_ready"] is False
        assert blocked["customer_ready"] is False
        assert blocked["export_ready"] is False
        assert blocked["public_ready"] is False
        _assert_runtime_side_effects_false(blocked)


def test_forbidden_fields_block_without_exposing_values(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    boundary = _build_finalsummaryreport_boundary(tmp_path, monkeypatch)
    boundary.update(
        {
            "raw_author_name": RAW_IDENTITY_SENTINEL,
            "profile_url": PROFILE_URL_SENTINEL,
            "token": SECRET_SENTINEL,
            "full_evidence_rows": [ROW_SENTINEL],
        }
    )

    handoff = build_final_report_boundary_source11_governance_handoff(boundary)
    encoded = _encoded(handoff)

    assert handoff["source11_governance_handoff_status"] in {"blocked_privacy_issue", "blocked_forbidden_input"}
    assert handoff["source11_governance_handoff_created"] is False
    assert RAW_IDENTITY_SENTINEL not in encoded
    assert PROFILE_URL_SENTINEL not in encoded
    assert SECRET_SENTINEL not in encoded
    assert ROW_SENTINEL not in encoded
    _assert_runtime_side_effects_false(handoff)
