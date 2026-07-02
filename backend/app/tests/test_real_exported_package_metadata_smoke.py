from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.services.real_exported_package_metadata_smoke import (
    APPROVED_CASE_ID_HINT,
    APPROVED_PACKAGE_NAME,
    APPROVED_PACKAGE_ROLE,
    build_real_exported_package_metadata_smoke,
)


TARGET_PACKAGE_DIR = (
    Path("docs")
    / "samples"
    / "donglu_sunjihai_youth_football"
    / "donglu-sunjihai-youth-football-202606-v2_20260617_121016"
)

FORBIDDEN_SENTINELS = (
    "actual-token-should-never-appear",
    "actual-cookie-should-never-appear",
    "actual-api-key-should-never-appear",
    "actual-raw-author-should-never-appear",
    "actual-author-name-should-never-appear",
    "actual-profile-url-should-never-appear",
    "actual-raw-comment-should-never-appear",
    "G:/private-collector/should-never-appear",
    "donglu_sunjihai_youth_football/donglu-sunjihai-youth-football-202606-v2_20260617_121016",
)


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _assert_safe_output(value: object) -> None:
    serialized = _serialized(value)
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel not in serialized
    assert ":/" not in serialized
    assert ":\\" not in serialized


def _assert_all_runtime_side_effects_false(smoke: dict) -> None:
    runtime_side_effects = smoke["runtime_side_effects"]
    assert runtime_side_effects
    assert all(value is False for value in runtime_side_effects.values())


def test_exact_approved_target_returns_metadata_only_ready_or_warn_object() -> None:
    smoke = build_real_exported_package_metadata_smoke(
        package_name=APPROVED_PACKAGE_NAME,
        package_role=APPROVED_PACKAGE_ROLE,
        case_id_hint=APPROVED_CASE_ID_HINT,
        package_dir=TARGET_PACKAGE_DIR,
        approval_phrase_present=True,
    )

    assert smoke["schema"] == "sentigraph_real_exported_package_metadata_smoke_v0_1"
    assert smoke["phase"] == "8W-2"
    assert smoke["smoke_status"] in {
        "metadata_ready_for_manual_review",
        "metadata_warn_manual_review_required",
    }
    assert smoke["created_local_metadata_smoke"] is True
    assert smoke["target_package_name"] == APPROVED_PACKAGE_NAME
    assert smoke["target_package_role"] == APPROVED_PACKAGE_ROLE
    assert smoke["target_case_id_hint"] == APPROVED_CASE_ID_HINT
    assert smoke["target_provider_result_id"] == "unknown"
    assert smoke["target_provider_job_id"] == "unknown"
    assert smoke["target_request_id"] == "unknown"
    assert smoke["target_identity_method"] == "explicit_user_approved_package_metadata_target"
    assert smoke["target_source_kind"] == "repo_controlled_already_exported_package_metadata"
    assert smoke["metadata_only"] is True
    assert smoke["human_review_required"] is True
    assert smoke["row_files_parsed"] is False
    assert smoke["original_package_rows_read"] is False
    assert smoke["private_collector_source_inspected"] is False
    assert smoke["real_exchange_dir_read"] is False
    assert smoke["absolute_path_exposed"] is False
    assert smoke["package_path_exposed"] is False

    presence = smoke["metadata_files_presence"]
    assert presence["manifest_json_present"] is True
    assert presence["validation_report_json_present"] is True
    assert presence["validation_report_md_present"] is True
    assert presence["source_manifest_jsonl_present"] is True
    assert presence["coverage_note_md_present"] is True
    assert presence["readme_present"] is True
    assert presence["collection_log_jsonl_present"] is True
    assert presence["evidence_items_jsonl_present_presence_only"] is True
    assert presence["evidence_items_csv_present_presence_only"] is True

    safe_summary = smoke["safe_summary"]
    assert safe_summary["validation_status"] in {"passed", "warn", "warning", "unknown"}
    assert isinstance(safe_summary["warning_count"], int)
    assert isinstance(safe_summary["error_count"], int)
    assert safe_summary["privacy_status"] in {"metadata_only_no_known_privacy_blocker", "manual_review_required"}
    assert safe_summary["path_status"] == "repo_controlled_target_path_ok"

    boundary_flags = smoke["boundary_flags"]
    for flag in (
        "selected_sample_only",
        "not_full_web",
        "not_full_platform",
        "not_full_thread",
        "not_official_verification",
        "not_causal_proof",
        "not_prediction",
        "not_production_score",
        "provider_output_is_evidence_candidate_not_truth",
        "human_review_required",
        "metadata_only",
        "no_row_read",
        "no_private_collector_source_inspection",
        "no_evidence_layer_write",
        "no_production_case",
        "no_production_analysis_run",
        "no_frontend_route",
        "no_real_api_llm_provider_collector",
    ):
        assert boundary_flags[flag] is True

    _assert_all_runtime_side_effects_false(smoke)
    _assert_safe_output(smoke)


def test_row_files_are_presence_only_and_not_read(monkeypatch: pytest.MonkeyPatch) -> None:
    original_read_text = Path.read_text

    def guarded_read_text(self: Path, *args, **kwargs):
        if self.name in {"evidence_items.jsonl", "evidence_items.csv", "source_manifest.jsonl", "collection_log.jsonl"}:
            raise AssertionError(f"{self.name} must remain presence-only")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    smoke = build_real_exported_package_metadata_smoke(
        package_name=APPROVED_PACKAGE_NAME,
        package_role=APPROVED_PACKAGE_ROLE,
        case_id_hint=APPROVED_CASE_ID_HINT,
        package_dir=TARGET_PACKAGE_DIR,
        approval_phrase_present=True,
    )

    assert smoke["created_local_metadata_smoke"] is True
    assert smoke["row_files_parsed"] is False
    assert smoke["runtime_side_effects"]["parsed_evidence_items_jsonl"] is False
    assert smoke["runtime_side_effects"]["parsed_evidence_items_csv"] is False
    assert smoke["runtime_side_effects"]["read_original_package_rows"] is False
    _assert_safe_output(smoke)


def test_wrong_missing_or_ambiguous_target_blocks_without_ready_marker() -> None:
    cases = [
        {},
        {
            "package_name": "wrong-package",
            "package_role": APPROVED_PACKAGE_ROLE,
            "case_id_hint": APPROVED_CASE_ID_HINT,
        },
        {
            "package_name": "../donglu-sunjihai-youth-football-202606-v2_20260617_121016",
            "package_role": APPROVED_PACKAGE_ROLE,
            "case_id_hint": APPROVED_CASE_ID_HINT,
        },
        {
            "package_name": APPROVED_PACKAGE_NAME,
            "package_role": "wrong-role",
            "case_id_hint": APPROVED_CASE_ID_HINT,
        },
    ]

    for kwargs in cases:
        smoke = build_real_exported_package_metadata_smoke(
            package_dir=TARGET_PACKAGE_DIR,
            approval_phrase_present=True,
            **kwargs,
        )
        assert smoke["smoke_status"].startswith("blocked_")
        assert smoke["created_local_metadata_smoke"] is False
        assert smoke["selector_implemented"] is False
        _assert_all_runtime_side_effects_false(smoke)
        _assert_safe_output(smoke)


def test_missing_target_path_blocks_without_broadening_or_searching(tmp_path: Path) -> None:
    smoke = build_real_exported_package_metadata_smoke(
        package_name=APPROVED_PACKAGE_NAME,
        package_role=APPROVED_PACKAGE_ROLE,
        case_id_hint=APPROVED_CASE_ID_HINT,
        package_dir=tmp_path / APPROVED_PACKAGE_NAME,
        approval_phrase_present=True,
    )

    assert smoke["smoke_status"] == "blocked_missing_approved_target"
    assert smoke["created_local_metadata_smoke"] is False
    assert smoke["safe_summary"]["path_status"] == "blocked_missing_approved_target"
    _assert_all_runtime_side_effects_false(smoke)
    _assert_safe_output(smoke)


def test_forbidden_metadata_blocks_and_does_not_echo_forbidden_values(tmp_path: Path) -> None:
    package_dir = tmp_path / APPROVED_PACKAGE_NAME
    package_dir.mkdir()
    (package_dir / "manifest.json").write_text(
        json.dumps(
            {
                "package_role": APPROVED_PACKAGE_ROLE,
                "case_id": APPROVED_CASE_ID_HINT,
                "token": "actual-token-should-never-appear",
                "cookie": "actual-cookie-should-never-appear",
                "api_key": "actual-api-key-should-never-appear",
                "raw_author_id": "actual-raw-author-should-never-appear",
                "author_name": "actual-author-name-should-never-appear",
                "profile_url": "actual-profile-url-should-never-appear",
                "raw_comment": "actual-raw-comment-should-never-appear",
                "absolute_path": "G:/private-collector/should-never-appear",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (package_dir / "validation_report.json").write_text('{"status":"passed","errors":0,"warnings":0}', encoding="utf-8")

    smoke = build_real_exported_package_metadata_smoke(
        package_name=APPROVED_PACKAGE_NAME,
        package_role=APPROVED_PACKAGE_ROLE,
        case_id_hint=APPROVED_CASE_ID_HINT,
        package_dir=package_dir,
        approval_phrase_present=True,
    )

    assert smoke["smoke_status"] == "blocked_forbidden_metadata"
    assert smoke["created_local_metadata_smoke"] is False
    assert smoke["safe_summary"]["privacy_status"] == "blocked_forbidden_metadata"
    assert smoke["safe_summary"]["blocker_summary"]
    _assert_all_runtime_side_effects_false(smoke)
    _assert_safe_output(smoke)


def test_side_effect_requests_block_and_keep_side_effect_flags_false() -> None:
    smoke = build_real_exported_package_metadata_smoke(
        package_name=APPROVED_PACKAGE_NAME,
        package_role=APPROVED_PACKAGE_ROLE,
        case_id_hint=APPROVED_CASE_ID_HINT,
        package_dir=TARGET_PACKAGE_DIR,
        approval_phrase_present=True,
        requested_side_effects={
            "evidence_layer_write": True,
            "production_case_created": True,
            "production_analysis_run_created": True,
            "route_changed": True,
            "frontend_integration_approved": True,
            "b_end_report_runtime_generated": True,
            "sandbox_public_event_generated": True,
            "called_real_api": True,
            "called_real_llm": True,
            "ran_collector": True,
            "fetched_url": True,
            "scraped_page": True,
            "public_url_created": True,
            "signed_url_created": True,
            "file_byte_route_created": True,
            "download_package_runtime_used": True,
            "public_access_runtime_used": True,
            "external_delivery_runtime_used": True,
            "final_delivery_runtime_used": True,
            "publish_now": True,
            "send_now": True,
            "post_now": True,
            "execute_now": True,
            "auto_execute": True,
        },
    )

    assert smoke["smoke_status"] == "blocked_requested_side_effect"
    assert smoke["created_local_metadata_smoke"] is False
    assert smoke["safe_summary"]["blocker_summary"]
    _assert_all_runtime_side_effects_false(smoke)
    _assert_safe_output(smoke)
