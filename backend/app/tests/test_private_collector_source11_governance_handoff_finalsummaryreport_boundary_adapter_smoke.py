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
from app.services.source11_governance_handoff_finalsummaryreport_adapter import (
    build_source11_governance_handoff_finalsummaryreport_boundary_adapter,
)
from app.services.staging_candidate_generated_run_bridge import build_staging_candidate_generated_run_bridge


ROW_SENTINEL = "ROW_SENTINEL_SHOULD_NOT_BE_READ_OR_EXPOSED_8X16"
RAW_IDENTITY_SENTINEL = "RAW_IDENTITY_SHOULD_NOT_BE_EXPOSED_8X16"
PROFILE_URL_SENTINEL = "PROFILE_URL_SENTINEL_SHOULD_NOT_BE_EXPOSED_8X16"
SECRET_SENTINEL = "SECRET_SENTINEL_SHOULD_NOT_BE_EXPOSED_8X16"
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
    "local_final_summary_report",
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
        "provider_result_id": "provider_result_8x16_boundary_adapter",
        "provider_job_id": "provider_job_8x16_boundary_adapter",
        "request_id": "analysis_request_8x16_boundary_adapter",
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
    candidate = create_review_only_staging_candidate(handoff_summary, requested_by="8x16_boundary_adapter_smoke")
    gate = build_review_only_staging_gate_result(handoff_summary, candidate)
    return build_safe_review_only_staging_summary(candidate, gate)


def _build_chain(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict:
    export_root = tmp_path / "exports"
    _write_synthetic_package(export_root, "synthetic_package")
    provider_result_path = _write_provider_result(
        tmp_path / "exchange" / "provider_result.json",
        _provider_result_payload(),
    )
    original_read_text = Path.read_text

    def guarded_read_text(self: Path, *args, **kwargs):
        if self.name in ROW_LIKE_FILES:
            raise AssertionError(f"{self.name} must not be opened or parsed in 8X-16 boundary adapter smoke")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)
    staging_summary = _build_review_only_staging_summary(provider_result_path, export_root)
    bridge = build_staging_candidate_generated_run_bridge(staging_summary, created_by="8x16_boundary_adapter_smoke")
    bridge["minimum_real_run_input_candidate"]["fixture_metadata"]["stage_id"] = "T0"
    execution = execute_minimum_real_run_from_bridge_candidate(bridge, created_by="8x16_boundary_adapter_smoke")
    integration = integrate_generated_run_with_dense_graph_from_execution(
        execution,
        created_by="8x16_boundary_adapter_smoke",
    )
    report_candidate = build_dense_graph_report_candidate_from_integration(
        integration,
        created_by="8x16_boundary_adapter_smoke",
    )
    boundary = build_report_candidate_final_report_boundary(
        report_candidate,
        created_by="8x16_boundary_adapter_smoke",
    )
    handoff = build_final_report_boundary_source11_governance_handoff(
        boundary,
        created_by="8x16_boundary_adapter_smoke",
    )
    return {
        "staging_summary": staging_summary,
        "bridge": bridge,
        "execution": execution,
        "integration": integration,
        "report_candidate": report_candidate,
        "boundary": boundary,
        "handoff": handoff,
    }


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


def _assert_downstream_false(value: dict) -> None:
    for flag in (
        "source11_runtime_called",
        "source11_final_summary_report_runtime_used",
        "actual_final_summary_report_created",
        "final_summary_report_created",
        "final_report_ready",
        "b_end_report_runtime_generated",
        "sandbox_public_event_generated",
        "sandbox_public_event_runtime_generated",
        "evidence_rows_parsed",
        "evidence_layer_write",
        "production_case_created",
        "production_analysis_run_created",
        "production_evidence_item_created",
        "review_queue_runtime_used",
        "generated_response_text",
        "public_route_created",
        "export_download_public_delivery_created",
        "frontend_ready",
        "route_ready",
        "production_ready",
        "customer_ready",
        "export_ready",
        "public_ready",
    ):
        assert value[flag] is False


def _install_downstream_side_effect_guards(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_downstream(*args, **kwargs):
        raise AssertionError("runtime/export/public delivery must not be called in 8X-16")

    def fail_network(*args, **kwargs):
        raise AssertionError("network access must not occur in 8X-16")

    monkeypatch.setattr(
        source11_governance_handoff_finalsummaryreport_adapter,
        "build_source11_governance_handoff_finalsummaryreport_adapter",
        fail_downstream,
    )
    monkeypatch.setattr(
        source11_governance_handoff_finalsummaryreport_adapter,
        "create_source11_governance_handoff_finalsummaryreport_adapter",
        fail_downstream,
    )
    for module in (
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


def test_source11_handoff_reaches_finalsummaryreport_boundary_adapter_without_runtime_or_export(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_downstream_side_effect_guards(monkeypatch)

    chain = _build_chain(tmp_path, monkeypatch)
    adapter = build_source11_governance_handoff_finalsummaryreport_boundary_adapter(
        chain["handoff"],
        created_by="8x16_boundary_adapter_smoke",
    )
    encoded = _encoded({"chain": chain, "adapter": adapter})

    assert chain["execution"]["generated_run"]["run_schema"] == "sentigraph_opinion_ecosystem_run_v0_1"
    assert chain["execution"]["generated_run"]["run_status"] == "ready"
    assert chain["integration"]["dense_graph_executed"] is True
    assert chain["report_candidate"]["report_candidate_created"] is True
    assert chain["boundary"]["final_report_boundary_created"] is True
    assert chain["handoff"]["source11_governance_handoff_created"] is True

    assert adapter["finalsummaryreport_boundary_adapter_schema"] == (
        "sentigraph_source11_governance_handoff_finalsummaryreport_boundary_adapter_v0_1"
    )
    assert adapter["finalsummaryreport_boundary_adapter_status"] == (
        "boundary_adapter_ready_for_manual_finalsummaryreport_review"
    )
    assert adapter["finalsummaryreport_boundary_adapter_created"] is True
    assert adapter["adapter_mode"] == "backend_only_local_finalsummaryreport_boundary_adapter_smoke"
    assert adapter["input_source_kind"] == "source11_governance_handoff"
    assert adapter["source11_governance_handoff_schema"] == (
        "sentigraph_final_report_boundary_source11_governance_handoff_v0_1"
    )
    assert adapter["source11_governance_handoff_status"] == "handoff_ready_for_manual_source11_governance_review"
    assert adapter["final_report_boundary_schema"] == "sentigraph_report_candidate_final_report_boundary_v0_1"
    assert adapter["report_candidate_schema"] == "sentigraph_dense_graph_report_candidate_v0_1"
    assert adapter["dense_graph_integration_schema"] == "sentigraph_generated_run_dense_graph_bridge_integration_v0_1"
    assert adapter["generated_run_schema"] == "sentigraph_opinion_ecosystem_run_v0_1"
    assert adapter["human_review_required"] is True
    assert adapter["human_review_status"] == "required"
    assert adapter["no_automatic_trust_upgrade"] is True
    assert adapter["coefficient_source"] == "mock_default"
    assert adapter["calibration_status"] == "uncalibrated"
    assert adapter["empirical_validation"] == "not_started"
    assert adapter["blockers"] == []
    _assert_downstream_false(adapter)
    _assert_runtime_side_effects_false(adapter)

    boundary_flags = adapter["boundary_flags"]
    assert boundary_flags["selected_sample_only"] is True
    assert boundary_flags["not_full_web"] is True
    assert boundary_flags["not_full_platform"] is True
    assert boundary_flags["not_official_verification"] is True
    assert boundary_flags["not_causal_proof"] is True
    assert boundary_flags["not_prediction"] is True
    assert boundary_flags["not_production_score"] is True
    assert boundary_flags["human_review_required"] is True
    assert boundary_flags["no_auto_execute"] is True
    assert boundary_flags["no_generated_public_response"] is True
    assert boundary_flags["boundary_adapter_only"] is True
    assert boundary_flags["not_actual_finalsummaryreport_runtime"] is True

    assert adapter["downstream_policy"]["source11_runtime_ready"] is False
    assert adapter["downstream_policy"]["final_summary_report_ready"] is False
    assert adapter["downstream_policy"]["export_ready"] is False
    assert adapter["downstream_policy"]["public_access_ready"] is False
    assert adapter["downstream_policy"]["b_end_ready"] is False
    assert adapter["downstream_policy"]["sandbox_ready"] is False
    assert adapter["downstream_policy"]["frontend_ready"] is False
    assert adapter["downstream_policy"]["route_ready"] is False
    assert adapter["downstream_policy"]["production_ready"] is False
    assert adapter["downstream_policy"]["customer_ready"] is False

    assert not (FORBIDDEN_OUTPUT_KEYS & _walk_keys(adapter))
    assert ROW_SENTINEL not in encoded
    assert RAW_IDENTITY_SENTINEL not in encoded
    assert PROFILE_URL_SENTINEL not in encoded
    assert SECRET_SENTINEL not in encoded
    assert str(tmp_path) not in encoded


def test_wrong_or_missing_source11_handoff_marker_blocks_boundary_adapter(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    handoff = _build_chain(tmp_path, monkeypatch)["handoff"]
    variants = [
        dict(handoff, source11_governance_handoff_schema="unknown"),
        dict(handoff, source11_governance_handoff_status="blocked_metadata_contract"),
        dict(handoff, source11_governance_handoff_created=False),
        dict(handoff, source11_governance_handoff_id=None),
        dict(handoff, source11_governance_review_summary=None),
    ]

    for value in variants:
        adapter = build_source11_governance_handoff_finalsummaryreport_boundary_adapter(value)

        assert adapter["finalsummaryreport_boundary_adapter_status"] == "blocked_metadata_contract"
        assert adapter["finalsummaryreport_boundary_adapter_created"] is False
        _assert_downstream_false(adapter)
        _assert_runtime_side_effects_false(adapter)


def test_runtime_and_readiness_flags_block_boundary_adapter(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base_handoff = _build_chain(tmp_path, monkeypatch)["handoff"]
    for flag in (
        "source11_runtime_called",
        "source11_final_summary_report_runtime_used",
        "actual_final_summary_report_created",
        "final_summary_report_created",
        "final_report_ready",
        "frontend_ready",
        "route_ready",
        "production_ready",
        "customer_ready",
        "export_ready",
        "public_ready",
    ):
        adapter = build_source11_governance_handoff_finalsummaryreport_boundary_adapter(
            dict(base_handoff, **{flag: True})
        )

        assert adapter["finalsummaryreport_boundary_adapter_status"] in {
            "blocked_requested_side_effect",
            "blocked_source11_runtime_side_effect_risk",
        }
        assert adapter["finalsummaryreport_boundary_adapter_created"] is False
        _assert_downstream_false(adapter)
        _assert_runtime_side_effects_false(adapter)


def test_forbidden_fields_block_boundary_adapter_without_exposing_values(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    handoff = _build_chain(tmp_path, monkeypatch)["handoff"]
    handoff.update(
        {
            "raw_author_name": RAW_IDENTITY_SENTINEL,
            "profile_url": PROFILE_URL_SENTINEL,
            "token": SECRET_SENTINEL,
            "full_evidence_rows": [ROW_SENTINEL],
        }
    )

    adapter = build_source11_governance_handoff_finalsummaryreport_boundary_adapter(handoff)
    encoded = _encoded(adapter)

    assert adapter["finalsummaryreport_boundary_adapter_status"] in {"blocked_privacy_issue", "blocked_forbidden_input"}
    assert adapter["finalsummaryreport_boundary_adapter_created"] is False
    assert RAW_IDENTITY_SENTINEL not in encoded
    assert PROFILE_URL_SENTINEL not in encoded
    assert SECRET_SENTINEL not in encoded
    assert ROW_SENTINEL not in encoded
    _assert_downstream_false(adapter)
    _assert_runtime_side_effects_false(adapter)
