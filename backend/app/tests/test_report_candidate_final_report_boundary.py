from __future__ import annotations

import builtins
import json
from pathlib import Path

from app.services.dense_graph_report_candidate_bridge import build_dense_graph_report_candidate_from_integration
from app.services.generated_run_dense_graph_bridge_integration import (
    integrate_generated_run_with_dense_graph_from_execution,
)
from app.services.minimum_real_run_bridge_execution import execute_minimum_real_run_from_bridge_candidate
from app.services.report_candidate_final_report_boundary import (
    build_report_candidate_final_report_boundary,
    build_safe_report_candidate_final_report_boundary_summary,
    create_report_candidate_final_report_boundary,
)
from app.services.staging_candidate_generated_run_bridge import build_staging_candidate_generated_run_bridge


SENTINEL_TOKEN = "actual-token-should-never-appear"
SENTINEL_AUTHOR = "actual-author-name-should-never-appear"
SENTINEL_PROFILE = "actual-profile-url-should-never-appear"
SENTINEL_RAW_ROW = "actual-raw-row-should-never-appear"
SENTINEL_PATH = "G:/private-collector/should-never-appear"
SENTINEL_RESPONSE = "actual-response-text-should-never-appear"
SENTINEL_PUBLIC_URL = "https://public-download.example/should-never-appear"
SENTINEL_SIGNED_URL = "https://signed-download.example/should-never-appear"
SENTINEL_EXTERNAL_TARGET = "https://external-delivery.example/should-never-appear"


def _safe_staging_summary(**overrides) -> dict:
    summary = {
        "schema": "sentigraph_review_only_staging_summary_v0_1",
        "staging_candidate_id": "review_staging_candidate_controlled",
        "analysis_request_id": "analysis_request_controlled",
        "provider_result_id": "provider_result_controlled",
        "provider_job_id": "provider_job_controlled",
        "package_name": "controlled_exported_package_fixture",
        "package_role": "review_ready_candidate",
        "case_id_hint": "case_controlled",
        "case_title_hint": "Controlled case",
        "validation_status": "passed",
        "evidence_count": 12,
        "source_count": 3,
        "warning_count": 1,
        "error_count": 0,
        "metadata_summary": {
            "evidence_count": 12,
            "source_count": 3,
            "package_name": "controlled_exported_package_fixture",
        },
        "validation_summary": {"status": "passed", "warnings": 1, "errors": 0},
        "coverage_summary": {
            "coverage_note": "Controlled metadata fixture only; not full-web and not full-platform.",
            "coverage_note_present": True,
            "not_full_web": True,
            "not_full_platform": True,
        },
        "gate_result": {
            "package_resolution_status": "accepted_metadata_only",
            "provider_result_status": "accepted_metadata_only",
            "privacy_status": "clear",
            "path_status": "accepted_metadata_only",
            "metadata_contract_status": "metadata_contract_ok",
            "evidence_row_boundary_status": "evidence_rows_not_read",
        },
        "audit_refs": [{"audit_ref_id": "audit_ref_controlled", "scope": "metadata_only"}],
        "metadata_only": True,
        "path_exposed": False,
        "path_reference": "review_only_metadata_summary",
        "blockers": [],
        "warnings": [],
        "safety_flags": {
            "metadata_only": True,
            "full_evidence_rows_parsed": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "analysis_run_created": False,
        },
    }
    summary.update(overrides)
    return summary


def _safe_report_candidate(**overrides) -> dict:
    bridge = build_staging_candidate_generated_run_bridge(_safe_staging_summary())
    execution = execute_minimum_real_run_from_bridge_candidate(bridge)
    integration = integrate_generated_run_with_dense_graph_from_execution(execution)
    candidate = build_dense_graph_report_candidate_from_integration(integration)
    candidate.update(overrides)
    return candidate


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


def _assert_false_side_effects(value: dict) -> None:
    assert value["runtime_side_effects"]
    assert all(flag_value is False for flag_value in value["runtime_side_effects"].values())


def _assert_output_side_effect_flags_false(value: dict) -> None:
    for flag in (
        "source11_final_summary_report_runtime_used",
        "final_summary_report_created",
        "final_report_created",
        "b_end_report_runtime_generated",
        "sandbox_public_event_generated",
        "export_artifact_created",
        "download_package_created",
        "public_access_created",
        "external_delivery_performed",
        "generated_response_text",
        "public_route_created",
        "frontend_integration_approved",
        "route_ready",
        "frontend_ready",
        "production_ready",
        "export_ready",
        "public_ready",
        "customer_ready",
    ):
        assert value[flag] is False


def _assert_downstream_policy_false(value: dict) -> None:
    policy = value["downstream_policy"]
    for flag in (
        "source11_ready",
        "export_ready",
        "download_ready",
        "public_access_ready",
        "external_delivery_ready",
        "b_end_ready",
        "sandbox_ready",
        "public_event_ready",
        "frontend_ready",
        "route_ready",
        "production_ready",
        "customer_ready",
    ):
        assert policy[flag] is False


def test_ready_report_candidate_creates_local_final_report_boundary_without_downstream_side_effects() -> None:
    boundary = build_report_candidate_final_report_boundary(_safe_report_candidate(), created_by="unit_test")
    alias_boundary = create_report_candidate_final_report_boundary(_safe_report_candidate(), created_by="unit_test")
    summary = build_safe_report_candidate_final_report_boundary_summary(boundary)

    assert boundary["final_report_boundary_schema"] == "sentigraph_report_candidate_final_report_boundary_v0_1"
    assert boundary["final_report_boundary_status"] == "boundary_ready"
    assert boundary["final_report_boundary_created"] is True
    assert boundary["input_source_kind"] == "dense_graph_report_candidate"
    assert boundary["boundary_mode"] == "backend_only_local_final_report_boundary"
    assert boundary["report_candidate_schema"] == "sentigraph_dense_graph_report_candidate_v0_1"
    assert boundary["report_candidate_status"] == "candidate_ready"
    assert boundary["dense_graph_integration_schema"] == "sentigraph_generated_run_dense_graph_bridge_integration_v0_1"
    assert boundary["generated_run_schema"] == "sentigraph_opinion_ecosystem_run_v0_1"
    assert boundary["human_review_required"] is True
    assert boundary["human_review_status"] == "required"
    assert boundary["dense_graph_proxy_summary"]
    assert boundary["report_candidate_summary"]
    assert boundary["candidate_section_outline"]
    assert boundary["coverage_limitations"]
    assert boundary["boundary_flags"]["selected_sample_only"] is True
    assert boundary["boundary_flags"]["not_source11_final_summary_report"] is True
    assert boundary["boundary_flags"]["not_export_ready"] is True
    assert boundary["boundary_flags"]["not_public_ready"] is True
    assert boundary["boundary_flags"]["not_customer_ready"] is True
    assert boundary["boundary_flags"]["not_production_ready"] is True
    _assert_output_side_effect_flags_false(boundary)
    _assert_downstream_policy_false(boundary)
    _assert_false_side_effects(boundary)

    assert alias_boundary["final_report_boundary_status"] == "boundary_ready"
    assert summary["final_report_boundary_status"] == "boundary_ready"
    assert summary["final_report_boundary_created"] is True
    assert summary["source11_final_summary_report_runtime_used"] is False
    assert summary["final_summary_report_created"] is False
    assert summary["export_ready"] is False
    assert summary["public_ready"] is False
    assert summary["customer_ready"] is False


def test_wrong_or_missing_report_candidate_input_blocks_boundary() -> None:
    cases = (
        _safe_report_candidate(report_candidate_schema="unknown"),
        _safe_report_candidate(report_candidate_status="blocked_metadata_contract"),
        _safe_report_candidate(candidate_mode="unknown"),
        _safe_report_candidate(report_candidate_created=False),
        _safe_report_candidate(dense_graph_summary=None),
        _safe_report_candidate(report_candidate_summary=None),
        _safe_report_candidate(boundary_flags=None),
        _safe_report_candidate(runtime_side_effects=None),
    )

    for candidate in cases:
        boundary = build_report_candidate_final_report_boundary(candidate)

        assert boundary["final_report_boundary_status"] == "blocked_metadata_contract"
        assert boundary["final_report_boundary_created"] is False
        _assert_output_side_effect_flags_false(boundary)
        _assert_false_side_effects(boundary)


def test_readiness_true_blocks_boundary_and_output_readiness_remains_false() -> None:
    for flag in ("route_ready", "frontend_ready", "production_ready", "export_ready", "public_ready", "customer_ready"):
        boundary = build_report_candidate_final_report_boundary(_safe_report_candidate(**{flag: True}))

        assert boundary["final_report_boundary_status"] == "blocked_requested_side_effect"
        assert boundary["final_report_boundary_created"] is False
        _assert_output_side_effect_flags_false(boundary)
        _assert_downstream_policy_false(boundary)
        _assert_false_side_effects(boundary)


def test_requested_side_effects_block_boundary_and_remain_false() -> None:
    candidate = _safe_report_candidate(
        source11_final_summary_report_runtime_used=True,
        final_summary_report_created=True,
        final_report_created=True,
        create_final_report=True,
        export_artifact_created=True,
        download_package_created=True,
        public_access_created=True,
        external_delivery_performed=True,
        b_end_report_runtime_generated=True,
        sandbox_public_event_generated=True,
        generated_response_text=True,
        public_route_created=True,
        route_changed=True,
        api_route_added=True,
        frontend_integration_approved=True,
        evidence_layer_write=True,
        production_case_created=True,
        production_analysis_run_created=True,
        evidence_rows_parsed=True,
        called_real_api=True,
        called_real_llm=True,
        ran_collector=True,
        fetched_url=True,
        scraped_page=True,
        auto_execute=True,
        publish_now=True,
        send_now=True,
        post_now=True,
        execute_now=True,
    )

    boundary = build_report_candidate_final_report_boundary(candidate)

    assert boundary["final_report_boundary_status"] == "blocked_requested_side_effect"
    assert boundary["final_report_boundary_created"] is False
    _assert_output_side_effect_flags_false(boundary)
    _assert_false_side_effects(boundary)


def test_forbidden_values_block_or_do_not_leak() -> None:
    candidate = _safe_report_candidate(
        token=SENTINEL_TOKEN,
        raw_author_name=SENTINEL_AUTHOR,
        profile_url=SENTINEL_PROFILE,
        full_evidence_rows=[SENTINEL_RAW_ROW],
        absolute_package_path=SENTINEL_PATH,
        response_text=SENTINEL_RESPONSE,
        public_url=SENTINEL_PUBLIC_URL,
        signed_url=SENTINEL_SIGNED_URL,
        external_delivery_target=SENTINEL_EXTERNAL_TARGET,
    )

    boundary = build_report_candidate_final_report_boundary(candidate)
    encoded = _encoded(boundary)

    assert boundary["final_report_boundary_status"] in {"blocked_privacy_issue", "blocked_forbidden_input"}
    assert boundary["final_report_boundary_created"] is False
    assert SENTINEL_TOKEN not in encoded
    assert SENTINEL_AUTHOR not in encoded
    assert SENTINEL_PROFILE not in encoded
    assert SENTINEL_RAW_ROW not in encoded
    assert SENTINEL_PATH not in encoded
    assert SENTINEL_RESPONSE not in encoded
    assert SENTINEL_PUBLIC_URL not in encoded
    assert SENTINEL_SIGNED_URL not in encoded
    assert SENTINEL_EXTERNAL_TARGET not in encoded
    assert "private-collector" not in encoded
    _assert_output_side_effect_flags_false(boundary)
    _assert_false_side_effects(boundary)


def test_no_package_files_or_evidence_rows_are_accessed(monkeypatch) -> None:
    candidate = _safe_report_candidate()

    def fail_open(*args, **kwargs):
        raise AssertionError("file access is not allowed in 8V-12 final report boundary smoke")

    def fail_read_text(*args, **kwargs):
        raise AssertionError("Path.read_text is not allowed in 8V-12 final report boundary smoke")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "read_text", fail_read_text)

    boundary = build_report_candidate_final_report_boundary(candidate)
    encoded = _encoded(boundary)

    assert boundary["final_report_boundary_status"] == "boundary_ready"
    assert "evidence_items.jsonl" not in encoded
    assert "evidence_items.csv" not in encoded
    assert boundary["runtime_side_effects"]["parsed_evidence_items_file"] is False
    assert boundary["runtime_side_effects"]["read_original_package_rows"] is False


def test_no_source11_export_route_or_public_delivery_fields_are_produced() -> None:
    boundary = build_report_candidate_final_report_boundary(_safe_report_candidate())
    keys = _walk_keys(boundary)

    assert not (
        {
            "response_text",
            "generated_public_message",
            "target_user_list",
            "persuasion_score",
            "truth_score",
            "official_verified",
            "prediction_probability",
            "psychological_profile",
            "personality_diagnosis",
            "pdf_path",
            "markdown_report_path",
            "briefing_deck_path",
            "zip_path",
            "package_path",
            "public_url",
            "signed_url",
            "download_url",
            "file_byte_route",
            "source11_final_summary_report_id",
        }
        & keys
    )
    assert boundary["source11_final_summary_report_runtime_used"] is False
    assert boundary["final_summary_report_created"] is False
    assert boundary["final_report_created"] is False
    assert boundary["export_artifact_created"] is False
    assert boundary["download_package_created"] is False
    assert boundary["public_access_created"] is False
    assert boundary["external_delivery_performed"] is False
    assert boundary["public_route_created"] is False
    assert boundary["frontend_integration_approved"] is False
    assert boundary["route_ready"] is False
    assert boundary["frontend_ready"] is False
    assert boundary["production_ready"] is False
