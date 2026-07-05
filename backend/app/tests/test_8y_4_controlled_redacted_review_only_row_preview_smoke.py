from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from app.services.controlled_row_preview import (
    APPROVAL_PHRASE,
    APPROVED_ROW_SOURCE,
    HARD_ROW_BOUND,
    REDACTION_POLICY_VERSION,
    build_controlled_row_preview,
)
from app.services.metadata_smoke_review_only_staging_boundary import (
    build_metadata_smoke_review_only_staging_boundary,
)
from app.services.real_exported_package_metadata_smoke import (
    APPROVED_CASE_ID_HINT,
    APPROVED_PACKAGE_NAME,
    APPROVED_PACKAGE_ROLE,
)


CANONICAL_8W7_APPROVAL_PHRASE = "APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION"
OLD_CHINESE_APPROVAL_PHRASE = "批准 8W-7 Controlled Row Preview Implementation"
OLD_MOJIBAKE_APPROVAL_PHRASE = "\u93b5\u7470\u566f 8W-7 Controlled Row Preview Implementation"

FORBIDDEN_KEYS = {
    "raw_rows",
    "raw_row",
    "raw_comment",
    "raw_comments",
    "raw_author_id",
    "raw_author_ids",
    "raw_author_name",
    "raw_author_names",
    "author_id",
    "author_ids",
    "author_name",
    "author_names",
    "username",
    "display_name",
    "profile_url",
    "profile_urls",
    "private_message",
    "private_messages",
    "email",
    "phone",
    "token",
    "cookie",
    "session",
    "password",
    "api_key",
    "secret",
    "browser_profile",
    "browser_profile_path",
    "absolute_path",
    "package_path",
    "source_url",
    "response_text",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
}

FORBIDDEN_TEXT_SENTINELS = (
    "actual-token-should-never-appear",
    "actual-cookie-should-never-appear",
    "actual-api-key-should-never-appear",
    "actual-raw-author-should-never-appear",
    "actual-author-name-should-never-appear",
    "actual-profile-url-should-never-appear",
    "actual-raw-comment-should-never-appear",
)


def _safe_8w2_smoke(**overrides: object) -> dict[str, object]:
    smoke: dict[str, object] = {
        "schema": "sentigraph_real_exported_package_metadata_smoke_v0_1",
        "phase": "8W-2",
        "smoke_status": "metadata_warn_manual_review_required",
        "target_package_name": APPROVED_PACKAGE_NAME,
        "target_package_role": APPROVED_PACKAGE_ROLE,
        "target_case_id_hint": APPROVED_CASE_ID_HINT,
        "metadata_only": True,
        "human_review_required": True,
        "warning_count": 1,
        "error_count": 0,
        "row_files_parsed": False,
        "evidence_items_jsonl_parsed": False,
        "evidence_items_csv_parsed": False,
        "original_package_rows_read": False,
        "private_collector_source_inspected": False,
        "real_exchange_dir_read": False,
        "safe_summary": {
            "validation_status": "passed",
            "warning_count": 1,
            "error_count": 0,
            "coverage_note_summary": "Selected public sample only; not full-web coverage.",
            "privacy_status": "metadata_only_no_known_privacy_blocker",
            "path_status": "repo_controlled_target_path_ok",
            "warning_summary": ["sample_size_below_target"],
            "blocker_summary": [],
        },
        "runtime_side_effects": {
            "called_real_api": False,
            "called_real_llm": False,
            "ran_provider_job": False,
            "ran_collector": False,
            "accessed_private_collector": False,
            "inspected_private_collector_source": False,
            "read_real_exchange_dir": False,
            "fetched_url": False,
            "scraped_page": False,
            "parsed_evidence_items_jsonl": False,
            "parsed_evidence_items_csv": False,
            "parsed_source_manifest_jsonl_rows": False,
            "parsed_collection_log_jsonl_rows": False,
            "read_original_package_rows": False,
            "read_raw_comments": False,
            "read_raw_identities": False,
            "wrote_evidence_layer": False,
            "created_evidence_items": False,
            "created_review_queue_items": False,
            "created_production_review_queue_items": False,
            "created_production_case": False,
            "created_production_analysis_run": False,
            "generated_b_end_report_runtime": False,
            "generated_sandbox_runtime": False,
            "generated_public_event_runtime": False,
            "used_report_export_runtime": False,
            "used_download_package_runtime": False,
            "used_public_access_runtime": False,
            "used_external_delivery_runtime": False,
            "used_final_delivery_runtime": False,
            "generated_response_text": False,
            "created_public_route": False,
            "modified_frontend": False,
            "published_or_sent": False,
            "auto_executed": False,
        },
    }
    smoke.update(overrides)
    return smoke


def _safe_8w4_boundary() -> dict[str, Any]:
    return build_metadata_smoke_review_only_staging_boundary(_safe_8w2_smoke())


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _json_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        keys = {str(key) for key in value}
        for nested_value in value.values():
            keys.update(_json_keys(nested_value))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_json_keys(item))
        return keys
    return set()


def _assert_no_forbidden_keys_or_sentinels(value: object) -> None:
    keys = {key.lower() for key in _json_keys(value)}
    serialized = _serialized(value).lower()
    assert not (keys & FORBIDDEN_KEYS)
    for sentinel in FORBIDDEN_TEXT_SENTINELS:
        assert sentinel not in serialized
    assert "g:\\" not in serialized
    assert "c:\\users" not in serialized


def _assert_runtime_flag_false(preview: dict[str, Any], flag: str) -> None:
    assert preview["runtime_side_effects"].get(flag) is False, flag


def test_8y4_controlled_smoke_creates_bounded_redacted_review_only_preview() -> None:
    preview = build_controlled_row_preview(
        _safe_8w4_boundary(),
        approval_phrase=CANONICAL_8W7_APPROVAL_PHRASE,
        max_preview_rows=5,
        row_source=APPROVED_ROW_SOURCE,
    )

    assert APPROVAL_PHRASE == CANONICAL_8W7_APPROVAL_PHRASE
    assert APPROVAL_PHRASE.isascii()
    assert preview["schema"] == "sentigraph_controlled_row_preview_v0_1"
    assert preview["created_local_row_preview"] is True
    assert preview["preview_only"] is True
    assert preview["row_source"] == "evidence_items.jsonl"
    assert preview["row_source_policy"] == "single_approved_jsonl_source_only"
    assert preview["runtime_side_effects"]["opened_approved_evidence_items_jsonl"] is True
    assert preview["runtime_side_effects"]["parsed_evidence_items_jsonl"] is True
    assert preview["runtime_side_effects"]["parsed_evidence_items_csv"] is False
    assert preview["runtime_side_effects"]["parsed_source_manifest_jsonl_rows"] is False
    assert preview["runtime_side_effects"]["parsed_collection_log_jsonl_rows"] is False
    assert preview["runtime_side_effects"]["read_original_package_rows"] is False
    assert preview["runtime_side_effects"]["read_real_exchange_dir"] is False
    assert preview["runtime_side_effects"]["accessed_private_collector"] is False
    assert preview["runtime_side_effects"]["inspected_private_collector_source"] is False
    assert preview["max_preview_rows_applied"] == 5
    assert preview["max_preview_rows_hard_bound"] == HARD_ROW_BOUND == 10
    assert preview["preview_rows_count"] <= preview["max_preview_rows_applied"]
    assert preview["rows_inspected_count"] <= preview["max_preview_rows_hard_bound"]
    assert preview["row_limit_enforced"] is True
    assert preview["redaction_policy_version"] == REDACTION_POLICY_VERSION
    assert preview["human_review_required"] is True
    assert preview["warning_manual_review_preserved"] is True
    assert "manual_review_required" in preview["warnings"]
    assert preview["absolute_path_exposed"] is False
    assert preview["package_path_exposed"] is False
    assert preview["row_source_path_exposed"] is False
    assert preview["evidence_layer_write"] is False
    assert preview["evidence_items_created"] is False
    assert preview["production_case_created"] is False
    assert preview["production_analysis_run_created"] is False
    assert preview["review_queue_item_created"] is False
    assert preview["production_review_queue_item_created"] is False
    assert preview["generated_response_text"] is False
    assert preview["b_end_report_runtime_generated"] is False
    assert preview["sandbox_public_event_generated"] is False
    assert preview["download_package_runtime_used"] is False
    assert preview["public_access_runtime_used"] is False
    assert preview["external_delivery_runtime_used"] is False
    assert preview["final_delivery_runtime_used"] is False
    assert preview["route_ready"] is False
    assert preview["frontend_ready"] is False
    assert preview["production_ready"] is False
    assert preview["customer_ready"] is False
    assert preview["public_ready"] is False

    for flag in (
        "wrote_evidence_layer",
        "created_evidence_items",
        "created_review_queue_items",
        "created_production_review_queue_items",
        "created_production_case",
        "created_production_analysis_run",
        "generated_b_end_report_runtime",
        "generated_sandbox_runtime",
        "generated_public_event_runtime",
        "used_report_export_runtime",
        "used_download_package_runtime",
        "used_public_access_runtime",
        "used_external_delivery_runtime",
        "used_final_delivery_runtime",
        "generated_response_text",
        "created_public_route",
        "modified_frontend",
        "called_real_api",
        "called_real_llm",
        "ran_provider_job",
        "ran_collector",
        "fetched_url",
        "scraped_page",
        "published_or_sent",
        "auto_executed",
    ):
        _assert_runtime_flag_false(preview, flag)

    assert preview["preview_rows"]
    for row in preview["preview_rows"]:
        assert set(row) <= {
            "preview_row_id",
            "row_index",
            "evidence_id_hash",
            "evidence_type",
            "platform",
            "created_at_date",
            "trust_label",
            "verification_status",
            "review_status",
            "language",
            "content_visibility",
            "access_scope",
            "text_snippet_redacted",
            "redaction_status",
            "redaction_warnings",
            "row_boundary_flags",
        }
        assert row["redaction_status"] == "redacted"
        assert len(row["text_snippet_redacted"]) <= 160
        assert row["row_boundary_flags"]["preview_only"] is True
        assert row["row_boundary_flags"]["human_review_required"] is True

    _assert_no_forbidden_keys_or_sentinels(preview)


@pytest.mark.parametrize(
    "approval_phrase",
    [None, "", "wrong approval", OLD_CHINESE_APPROVAL_PHRASE, OLD_MOJIBAKE_APPROVAL_PHRASE],
)
def test_8y4_wrong_missing_or_old_phrase_blocks_before_row_source_open(
    approval_phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    boundary = _safe_8w4_boundary()

    def blocked_open(*args: object, **kwargs: object) -> None:
        raise AssertionError("row source must not open before exact approval")

    monkeypatch.setattr(Path, "open", blocked_open)
    monkeypatch.setattr(Path, "read_text", blocked_open)

    preview = build_controlled_row_preview(boundary, approval_phrase=approval_phrase)

    assert preview["created_local_row_preview"] is False
    assert preview["preview_rows"] == []
    assert preview["preview_rows_count"] == 0
    assert "blocked_missing_exact_approval" in preview["blockers"]
    assert preview["runtime_side_effects"]["opened_approved_evidence_items_jsonl"] is False
    assert preview["runtime_side_effects"]["parsed_evidence_items_jsonl"] is False
    assert preview["runtime_side_effects"]["parsed_evidence_items_csv"] is False
    assert preview["evidence_layer_write"] is False
    assert preview["evidence_items_created"] is False
    assert preview["production_case_created"] is False
    assert preview["production_analysis_run_created"] is False
    assert preview["review_queue_item_created"] is False
    assert preview["production_review_queue_item_created"] is False
    _assert_no_forbidden_keys_or_sentinels(preview)
