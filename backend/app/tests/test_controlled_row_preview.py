from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.services.metadata_smoke_review_only_staging_boundary import (
    build_metadata_smoke_review_only_staging_boundary,
)
from app.services.real_exported_package_metadata_smoke import (
    APPROVED_CASE_ID_HINT,
    APPROVED_PACKAGE_NAME,
    APPROVED_PACKAGE_ROLE,
)
from app.services.controlled_row_preview import (
    APPROVAL_PHRASE,
    APPROVED_ROW_SOURCE,
    build_controlled_row_preview,
    build_safe_controlled_row_preview_summary,
)


EXPECTED_APPROVAL_PHRASE = "APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION"
OLD_CHINESE_APPROVAL_PHRASE = "批准 8W-7 Controlled Row Preview Implementation"
MOJIBAKE_APPROVAL_PHRASE = "\u93b5\u7470\u566f 8W-7 Controlled Row Preview Implementation"

FORBIDDEN_SENTINELS = (
    "actual-token-should-never-appear",
    "actual-cookie-should-never-appear",
    "actual-api-key-should-never-appear",
    "actual-raw-author-should-never-appear",
    "actual-author-name-should-never-appear",
    "actual-username-should-never-appear",
    "actual-display-name-should-never-appear",
    "actual-profile-url-should-never-appear",
    "actual-raw-comment-should-never-appear",
    "actual-email-should-never-appear@example.com",
    "555-123-4567",
    "G:/private-collector/should-never-appear",
    "C:/Users/msjpurf/private-collector/should-never-appear",
    "donglu_sunjihai_youth_football/donglu-sunjihai-youth-football-202606-v2_20260617_121016",
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


def _safe_8w4_boundary(**overrides: object) -> dict[str, object]:
    boundary = build_metadata_smoke_review_only_staging_boundary(_safe_8w2_smoke())
    boundary.update(overrides)
    return boundary


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _assert_safe_output(value: object) -> None:
    serialized = _serialized(value)
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel not in serialized
    assert ":/" not in serialized
    assert ":\\" not in serialized


def _assert_all_disallowed_side_effects_false(preview: dict[str, object]) -> None:
    runtime_side_effects = preview["runtime_side_effects"]
    assert isinstance(runtime_side_effects, dict)
    for flag, value in runtime_side_effects.items():
        if flag in {"opened_approved_evidence_items_jsonl", "parsed_evidence_items_jsonl"}:
            continue
        assert value is False, flag


def _assert_blocked(preview: dict[str, object], expected_reason: str) -> None:
    assert str(preview["preview_status"]).startswith("blocked_")
    assert preview["created_local_row_preview"] is False
    assert preview["preview_rows_count"] == 0
    assert preview["preview_rows"] == []
    assert expected_reason in preview["blockers"]
    _assert_all_disallowed_side_effects_false(preview)
    _assert_safe_output(preview)


def test_exact_approval_phrase_is_canonical_ascii_text() -> None:
    assert APPROVAL_PHRASE == EXPECTED_APPROVAL_PHRASE
    assert APPROVAL_PHRASE.isascii()

    preview = build_controlled_row_preview(
        _safe_8w4_boundary(),
        approval_phrase=EXPECTED_APPROVAL_PHRASE,
    )

    assert preview["created_local_row_preview"] is True
    assert preview["preview_status"] in {
        "row_preview_ready_for_manual_review",
        "row_preview_warn_manual_review_required",
    }


def test_ready_warn_path_from_safe_8w4_boundary() -> None:
    preview = build_controlled_row_preview(_safe_8w4_boundary(), approval_phrase=APPROVAL_PHRASE)

    assert preview["schema"] == "sentigraph_controlled_row_preview_v0_1"
    assert preview["phase"] == "8W-7"
    assert preview["preview_status"] in {
        "row_preview_ready_for_manual_review",
        "row_preview_warn_manual_review_required",
    }
    assert preview["created_local_row_preview"] is True
    assert preview["source_boundary_schema"] == "sentigraph_metadata_smoke_review_only_staging_boundary_v0_1"
    assert preview["source_boundary_phase"] == "8W-4"
    assert preview["approved_target_package_name"] == APPROVED_PACKAGE_NAME
    assert preview["approved_target_package_role"] == APPROVED_PACKAGE_ROLE
    assert preview["approved_target_case_id_hint"] == APPROVED_CASE_ID_HINT
    assert preview["row_source"] == APPROVED_ROW_SOURCE
    assert preview["row_source_policy"] == "single_approved_jsonl_source_only"
    assert preview["row_source_path_exposed"] is False
    assert preview["absolute_path_exposed"] is False
    assert preview["package_path_exposed"] is False
    assert preview["warning_count"] == 1
    assert preview["human_review_required"] is True
    assert preview["warning_manual_review_preserved"] is True
    assert preview["preview_only"] is True
    assert preview["production_ready"] is False
    assert preview["public_ready"] is False
    assert preview["customer_ready"] is False
    assert preview["route_ready"] is False
    assert preview["frontend_ready"] is False
    assert preview["evidence_layer_ready"] is False
    assert preview["max_preview_rows_requested"] == 5
    assert preview["max_preview_rows_applied"] == 5
    assert preview["max_preview_rows_hard_bound"] == 10
    assert preview["preview_rows_count"] <= 5
    assert preview["rows_inspected_count"] <= 10
    assert preview["row_limit_enforced"] is True
    assert preview["runtime_side_effects"]["parsed_evidence_items_jsonl"] is True
    assert preview["runtime_side_effects"]["parsed_evidence_items_csv"] is False
    assert preview["evidence_layer_write"] is False
    assert preview["production_case_created"] is False
    assert preview["production_analysis_run_created"] is False
    assert preview["route_changed"] is False
    assert preview["frontend_code_changed"] is False

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
        assert len(row["text_snippet_redacted"]) <= 160
        assert row["row_boundary_flags"]["preview_only"] is True
        assert row["row_boundary_flags"]["human_review_required"] is True
    _assert_all_disallowed_side_effects_false(preview)
    _assert_safe_output(preview)


@pytest.mark.parametrize(
    "approval_phrase",
    [None, "", "wrong approval", OLD_CHINESE_APPROVAL_PHRASE, MOJIBAKE_APPROVAL_PHRASE],
)
def test_exact_approval_required_before_opening_rows(
    approval_phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def blocked_open(*args, **kwargs):
        raise AssertionError("row source must not open without exact approval")

    monkeypatch.setattr(Path, "open", blocked_open)
    monkeypatch.setattr(Path, "read_text", blocked_open)

    preview = build_controlled_row_preview(_safe_8w4_boundary(), approval_phrase=approval_phrase)

    _assert_blocked(preview, "blocked_missing_exact_approval")
    assert preview["runtime_side_effects"]["parsed_evidence_items_jsonl"] is False
    assert preview["runtime_side_effects"]["opened_approved_evidence_items_jsonl"] is False


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("schema", "wrong", "source_boundary_schema_wrong"),
        ("phase", "wrong", "source_boundary_phase_wrong"),
        ("approved_target_package_name", "wrong", "source_package_name_mismatch"),
        ("approved_target_package_role", "wrong", "source_package_role_mismatch"),
        ("approved_target_case_id_hint", "wrong", "source_case_id_hint_mismatch"),
        ("metadata_only", False, "metadata_only_not_true"),
        ("human_review_required", False, "human_review_required_not_true"),
        ("warning_count", 0, "warning_count_not_one"),
        ("warning_manual_review_preserved", False, "warning_manual_review_not_preserved"),
        ("row_preview_approved", True, "row_preview_already_approved_in_source"),
        ("evidence_layer_write", True, "source_evidence_layer_write_true"),
        ("production_case_created", True, "source_production_case_created_true"),
        ("production_analysis_run_created", True, "source_production_analysis_run_created_true"),
        ("frontend_ready", True, "source_frontend_ready_true"),
        ("route_ready", True, "source_route_ready_true"),
        ("production_ready", True, "source_production_ready_true"),
    ],
)
def test_wrong_source_boundary_blocks(field: str, value: object, reason: str) -> None:
    preview = build_controlled_row_preview(
        _safe_8w4_boundary(**{field: value}),
        approval_phrase=APPROVAL_PHRASE,
    )

    _assert_blocked(preview, reason)


@pytest.mark.parametrize(
    ("row_source", "reason"),
    [
        ("evidence_items.csv", "blocked_unapproved_row_source"),
        ("evidence_items.jsonl,evidence_items.csv", "blocked_unapproved_row_source"),
        ("source_manifest.jsonl", "blocked_unapproved_row_source"),
        ("collection_log.jsonl", "blocked_unapproved_row_source"),
        ("original_package_rows", "blocked_unapproved_row_source"),
        ("private_collector_raw_output", "blocked_unapproved_row_source"),
    ],
)
def test_row_source_policy_blocks_unapproved_sources(row_source: str, reason: str) -> None:
    preview = build_controlled_row_preview(
        _safe_8w4_boundary(),
        approval_phrase=APPROVAL_PHRASE,
        row_source=row_source,
    )

    _assert_blocked(preview, reason)
    assert preview["runtime_side_effects"]["parsed_evidence_items_jsonl"] is False
    assert preview["runtime_side_effects"]["parsed_evidence_items_csv"] is False


@pytest.mark.parametrize(
    ("max_preview_rows", "expected_status"),
    [
        (10, "allowed"),
        (11, "blocked_requested_row_limit_too_high"),
        (0, "blocked_requested_row_limit_not_positive"),
    ],
)
def test_row_count_limit(max_preview_rows: int, expected_status: str) -> None:
    preview = build_controlled_row_preview(
        _safe_8w4_boundary(),
        approval_phrase=APPROVAL_PHRASE,
        max_preview_rows=max_preview_rows,
    )

    if expected_status == "allowed":
        assert preview["created_local_row_preview"] is True
        assert preview["preview_rows_count"] <= 10
        assert preview["rows_inspected_count"] <= 10
        assert preview["row_limit_enforced"] is True
    else:
        _assert_blocked(preview, expected_status)


def test_file_access_limited_to_approved_jsonl(monkeypatch: pytest.MonkeyPatch) -> None:
    opened: list[str] = []
    original_open = Path.open

    def guarded_open(self: Path, *args, **kwargs):
        opened.append(self.name)
        if self.name in {"evidence_items.csv", "source_manifest.jsonl", "collection_log.jsonl"}:
            raise AssertionError(f"{self.name} must not open")
        if "private" in str(self).lower() or "collector" in str(self).lower():
            raise AssertionError("private collector path must not open")
        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_open)

    preview = build_controlled_row_preview(_safe_8w4_boundary(), approval_phrase=APPROVAL_PHRASE)

    assert preview["created_local_row_preview"] is True
    assert opened == ["evidence_items.jsonl"]
    _assert_safe_output(preview)


def test_redaction_blocks_or_removes_forbidden_sentinels(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    row_file = tmp_path / "evidence_items.jsonl"
    row_file.write_text(
        json.dumps(
            {
                "evidence_id": "safe-evidence-id",
                "evidence_type": "comment",
                "platform": "unknown_future_platform",
                "created_at": "2026-06-17T12:10:16Z",
                "trust_label": "medium_low",
                "verification_status": "vendor_attested",
                "review_status": "review_needed",
                "language": "zh",
                "body_text": (
                    "实际正文包含 https://example.com/path "
                    "actual-email-should-never-appear@example.com 555-123-4567 "
                    "@actual-username-should-never-appear token=actual-token-should-never-appear"
                ),
                "author_id": "actual-raw-author-should-never-appear",
                "author_name": "actual-author-name-should-never-appear",
                "username": "actual-username-should-never-appear",
                "display_name": "actual-display-name-should-never-appear",
                "profile_url": "actual-profile-url-should-never-appear",
                "api_key": "actual-api-key-should-never-appear",
                "cookie": "actual-cookie-should-never-appear",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    import app.services.controlled_row_preview as module

    monkeypatch.setattr(module, "APPROVED_ROW_FILE", row_file)
    preview = build_controlled_row_preview(_safe_8w4_boundary(), approval_phrase=APPROVAL_PHRASE)

    assert preview["created_local_row_preview"] is True
    assert preview["preview_rows_count"] == 1
    row = preview["preview_rows"][0]
    assert len(row["text_snippet_redacted"]) <= 160
    assert "redacted_sensitive_text" in row["redaction_warnings"]
    _assert_safe_output(preview)


@pytest.mark.parametrize(
    "requested_action",
    [
        "evidence_layer_write",
        "production_case",
        "production_analysis_run",
        "review_queue_runtime",
        "frontend_route",
        "b_end_report",
        "sandbox_public_event",
        "public_url",
        "signed_url",
        "download_package",
        "final_delivery",
        "publish",
        "send",
        "post",
        "execute",
        "auto_execute",
    ],
)
def test_side_effect_requests_block_and_keep_flags_false(requested_action: str) -> None:
    preview = build_controlled_row_preview(
        _safe_8w4_boundary(),
        approval_phrase=APPROVAL_PHRASE,
        requested_actions=[requested_action],
    )

    _assert_blocked(preview, f"requested_action_blocked:{requested_action}")


def test_health_summary_is_safe_counts_only() -> None:
    summary = build_safe_controlled_row_preview_summary(
        _safe_8w4_boundary(),
        approval_phrase=APPROVAL_PHRASE,
    )

    assert summary["schema"] == "sentigraph_controlled_row_preview_summary_v0_1"
    assert summary["phase"] == "8W-7"
    assert summary["preview_status"] in {
        "row_preview_ready_for_manual_review",
        "row_preview_warn_manual_review_required",
    }
    assert summary["preview_rows_count"] <= 5
    assert summary["rows_inspected_count"] <= 10
    assert "preview_rows" not in summary
    assert "approved_target_package_name" in summary
    _assert_safe_output(summary)
