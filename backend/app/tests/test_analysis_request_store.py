from __future__ import annotations

import json
from pathlib import Path

from app.schemas.analysis_request import AnalysisRequestCaseSeed, AnalysisRequestCreate
from app.services import analysis_request_store
from app.services.analysis_request_store import (
    cancel_analysis_request,
    create_case_draft_handoff,
    create_evidence_import_plan,
    create_evidence_import_preview,
    create_analysis_request,
    get_analysis_request_config,
    list_evidence_import_plans,
    list_evidence_import_previews,
    list_analysis_requests,
    read_analysis_request,
)


def provider_result_payload(
    request_id: str,
    *,
    status: str = "validation_warn",
    safety_status: str = "safe",
    validation_errors: int = 0,
    package_name: str = "sample_package",
    evidence: int = 581,
    privacy: dict | None = None,
    coverage: dict | None = None,
) -> dict:
    return {
        "schema": "sentigraph_provider_job_result_v1",
        "request_id": request_id,
        "provider_job_id": "provider_job_local_001",
        "provider_type": "private_collector",
        "status": status,
        "safety_status": safety_status,
        "package_path": "exports/sentigraph-evidence-v1/sample_package",
        "package_name": package_name,
        "package_role": "selected_public_sample",
        "package_index_path": "exports/sentigraph-evidence-v1/package_index.json",
        "counts": {"evidence": evidence, "comments": 546, "sources": 37, "roots": 35},
        "validation": {"status": "warn" if validation_errors == 0 else "failed", "errors": validation_errors, "warnings": 1},
        "coverage": coverage
        if coverage is not None
        else {"coverage_level": "selected_public_sample", "not_full_web": True, "not_full_platform": True, "not_full_thread": True},
        "privacy": privacy
        if privacy is not None
        else {"raw_author_ids_removed": True, "raw_author_names_removed": True, "profile_urls_removed": True, "private_messages_excluded": True},
        "skipped": [],
        "notes": ["Local package result only."],
    }


def write_provider_result(tmp_path: Path, request_id: str, payload: dict) -> None:
    result_path = tmp_path / "results" / f"{request_id}.json"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(payload), encoding="utf-8")


def create_valid_case_draft(tmp_path: Path, request_id: str) -> dict:
    write_provider_result(tmp_path, request_id, provider_result_payload(request_id))
    draft = create_case_draft_handoff(request_id)
    draft_path = tmp_path / "case_drafts" / f"{request_id}.json"
    return json.loads(draft_path.read_text(encoding="utf-8"))


def overwrite_case_draft(tmp_path: Path, request_id: str, draft_payload: dict) -> None:
    draft_path = tmp_path / "case_drafts" / f"{request_id}.json"
    draft_path.write_text(json.dumps(draft_payload), encoding="utf-8")


def create_valid_import_plan(tmp_path: Path, request_id: str) -> dict:
    create_valid_case_draft(tmp_path, request_id)
    plan = create_evidence_import_plan(request_id)
    plan_path = tmp_path / "import_plans" / f"{request_id}.json"
    return json.loads(plan_path.read_text(encoding="utf-8"))


def overwrite_import_plan(tmp_path: Path, request_id: str, plan_payload: dict) -> None:
    plan_path = tmp_path / "import_plans" / f"{request_id}.json"
    plan_path.write_text(json.dumps(plan_payload), encoding="utf-8")


def test_create_request_writes_json_with_conservative_defaults(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))

    record = create_analysis_request(
        AnalysisRequestCreate(
            case_seed=AnalysisRequestCaseSeed(
                title="Helldivers PSN follow-up",
                description="Local file-based request only.",
                keywords=["helldivers", "psn"],
                negative_keywords=["unrelated"],
            )
        )
    )

    request_path = tmp_path / "requests" / f"{record.request_id}.json"
    assert request_path.exists()
    parsed = json.loads(request_path.read_text(encoding="utf-8"))
    assert parsed["schema"] == "sentigraph_analysis_request_v1"
    assert parsed["safety_policy"]["allow_live_collection"] is False
    assert parsed["safety_policy"]["allow_saved_profile"] is False
    assert parsed["safety_policy"]["allow_manual_snapshot"] is True
    assert parsed["safety_policy"]["forbid_proxy_pool"] is True
    assert parsed["safety_policy"]["forbid_captcha_bypass"] is True
    assert parsed["privacy_policy"]["remove_raw_author_id"] is True
    assert parsed["privacy_policy"]["remove_raw_author_name"] is True
    assert record.safe_mode["provider_execution"] is False


def test_list_and_read_requests_with_provider_result(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Dong Lu public event sample"))
    )
    result = {
        "schema": "sentigraph_provider_job_result_v1",
        "request_id": record.request_id,
        "provider_job_id": "provider_job_local_001",
        "provider_type": "private_collector",
        "status": "package_ready",
        "safety_status": "safe",
        "package_path": "exports/sentigraph-evidence-v1/sample_package",
        "package_name": "sample_package",
        "package_role": "selected_public_sample",
        "package_index_path": "exports/sentigraph-evidence-v1/package_index.json",
        "counts": {"evidence": 34, "comments": 28, "sources": 7, "roots": 6},
        "validation": {"status": "warn", "errors": 0, "warnings": 2},
        "coverage": {"coverage_level": "selected_public_sample", "not_full_web": True, "not_full_platform": True, "not_full_thread": True},
        "privacy": {"raw_author_ids_removed": True, "raw_author_names_removed": True, "profile_urls_removed": True, "private_messages_excluded": True},
        "skipped": [],
        "notes": ["Local package result only."],
    }
    result_path = tmp_path / "results" / f"{record.request_id}.json"
    result_path.write_text(json.dumps(result), encoding="utf-8")

    items = list_analysis_requests()
    detail = read_analysis_request(record.request_id)

    assert len(items) == 1
    assert items[0].provider_status == "package_ready"
    assert items[0].package_name == "sample_package"
    assert detail.provider_result is not None
    assert detail.provider_result.counts.evidence == 34
    assert detail.provider_result.coverage.not_full_web is True


def test_provider_result_with_canonical_not_run_parses(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Default provider result"))
    )
    result_path = tmp_path / "results" / f"{record.request_id}.json"
    result_path.write_text(
        json.dumps(
            {
                "schema": "sentigraph_provider_job_result_v1",
                "request_id": record.request_id,
                "provider_job_id": "local_default",
                "provider_type": "private_collector",
                "status": "needs_manual_snapshot",
                "safety_status": "safe",
                "counts": {"evidence": 0, "comments": 0, "sources": 0, "roots": 0},
                "validation": {"status": "not_run", "errors": 0, "warnings": 0},
            }
        ),
        encoding="utf-8",
    )

    detail = read_analysis_request(record.request_id)

    assert detail.result_warning is None
    assert detail.provider_status == "needs_manual_snapshot"
    assert detail.safety_status == "safe"
    assert detail.provider_result is not None
    assert detail.provider_result.validation.status == "not_run"
    assert detail.provider_result.counts.evidence == 0
    assert detail.provider_result.counts.roots == 0


def test_provider_result_legacy_aliases_parse_and_normalize(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Legacy provider result"))
    )
    result_path = tmp_path / "results" / f"{record.request_id}.json"
    result_path.write_text(
        json.dumps(
            {
                "schema": "sentigraph_provider_job_result_v1",
                "request_id": record.request_id,
                "provider_job_id": "local_legacy",
                "provider_type": "private_collector",
                "status": "validation_warn",
                "safety_status": "safe",
                "counts": {"evidence_items": 581, "comments": 546, "sources": 37, "root_content": 35},
                "validation": {"status": "warn", "errors_count": 0, "warnings_count": 1},
            }
        ),
        encoding="utf-8",
    )

    detail = read_analysis_request(record.request_id)

    assert detail.result_warning is None
    assert detail.provider_result is not None
    assert detail.provider_result.counts.evidence == 581
    assert detail.provider_result.counts.comments == 546
    assert detail.provider_result.counts.sources == 37
    assert detail.provider_result.counts.roots == 35
    assert detail.provider_result.validation.errors == 0
    assert detail.provider_result.validation.warnings == 1


def test_provider_result_canonical_fields_win_over_legacy_aliases(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Canonical provider result"))
    )
    result_path = tmp_path / "results" / f"{record.request_id}.json"
    result_path.write_text(
        json.dumps(
            {
                "schema": "sentigraph_provider_job_result_v1",
                "request_id": record.request_id,
                "status": "package_ready",
                "safety_status": "safe",
                "counts": {
                    "evidence": 34,
                    "evidence_items": 999,
                    "comments": 28,
                    "sources": 7,
                    "roots": 6,
                    "root_content": 999,
                },
                "validation": {
                    "status": "passed",
                    "errors": 0,
                    "errors_count": 999,
                    "warnings": 0,
                    "warnings_count": 999,
                },
            }
        ),
        encoding="utf-8",
    )

    detail = read_analysis_request(record.request_id)

    assert detail.provider_result is not None
    assert detail.provider_result.counts.evidence == 34
    assert detail.provider_result.counts.roots == 6
    assert detail.provider_result.validation.errors == 0
    assert detail.provider_result.validation.warnings == 0


def test_eligible_validation_warn_result_creates_case_draft(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(
            case_seed=AnalysisRequestCaseSeed(
                title="Dong Sun draft handoff",
                description="Local handoff only.",
                keywords=["donglu", "sunjihai"],
            )
        )
    )
    write_provider_result(tmp_path, record.request_id, provider_result_payload(record.request_id))

    draft = create_case_draft_handoff(record.request_id)
    draft_again = create_case_draft_handoff(record.request_id)
    draft_text = (tmp_path / "case_drafts" / f"{record.request_id}.json").read_text(encoding="utf-8")

    assert draft.schema_ == "sentigraph_case_draft_handoff_v1"
    assert draft.draft_id == f"draft_{record.request_id}"
    assert draft_again.draft_id == draft.draft_id
    assert draft.provider_summary.status == "validation_warn"
    assert draft.package_reference.package_name == "sample_package"
    assert draft.counts.evidence == 581
    assert draft.counts.roots == 35
    assert draft.validation.warnings == 1
    assert draft.coverage.not_full_web is True
    assert draft.privacy.raw_author_ids_removed is True
    assert draft.readiness.can_import_evidence is False
    assert draft.safe_mode["evidence_rows_imported"] is False
    assert "raw_author_value" not in draft_text


def test_eligible_package_ready_result_creates_case_draft(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Package ready handoff"))
    )
    result = provider_result_payload(record.request_id, status="package_ready")
    result["validation"] = {"status": "passed", "errors": 0, "warnings": 0}
    write_provider_result(tmp_path, record.request_id, result)

    draft = create_case_draft_handoff(record.request_id)

    assert draft.provider_summary.status == "package_ready"
    assert draft.validation.status == "passed"


def test_legacy_alias_result_can_create_case_draft_after_normalization(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Legacy handoff"))
    )
    result = provider_result_payload(record.request_id)
    result["counts"] = {"evidence_items": 581, "comments": 546, "sources": 37, "root_content": 35}
    result["validation"] = {"status": "warn", "errors_count": 0, "warnings_count": 1}
    write_provider_result(tmp_path, record.request_id, result)

    draft = create_case_draft_handoff(record.request_id)

    assert draft.counts.evidence == 581
    assert draft.counts.roots == 35
    assert draft.validation.warnings == 1


def test_case_draft_blocks_ineligible_provider_results(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))

    cases = [
        ("No provider result", None, "provider result is missing"),
        ("Needs manual snapshot", provider_result_payload("placeholder", status="needs_manual_snapshot", evidence=0, package_name=""), "not eligible"),
        ("Validation failed", provider_result_payload("placeholder", status="validation_failed"), "not eligible"),
        ("Validation errors", provider_result_payload("placeholder", status="validation_warn", validation_errors=2), "validation errors"),
        ("Missing package", provider_result_payload("placeholder", package_name=""), "package_name is missing"),
        ("Unsafe safety", provider_result_payload("placeholder", safety_status="blocked"), "safety status"),
        (
            "Missing privacy",
            provider_result_payload("placeholder", privacy={"raw_author_ids_removed": True}),
            "privacy fields missing",
        ),
        (
            "Claims full web",
            provider_result_payload("placeholder", coverage={"coverage_level": "full_web", "not_full_web": False, "not_full_platform": True, "not_full_thread": True}),
            "coverage",
        ),
    ]

    for title, result, expected_message in cases:
        record = create_analysis_request(
            AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title=title))
        )
        if result is not None:
            result["request_id"] = record.request_id
            write_provider_result(tmp_path, record.request_id, result)

        try:
            create_case_draft_handoff(record.request_id)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{title} should not create a case draft")


def test_eligible_case_draft_creates_evidence_import_plan(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Import plan handoff"))
    )
    create_valid_case_draft(tmp_path, record.request_id)

    plan = create_evidence_import_plan(record.request_id)
    plan_again = create_evidence_import_plan(record.request_id)
    plan_text = (tmp_path / "import_plans" / f"{record.request_id}.json").read_text(encoding="utf-8")

    assert plan.schema_ == "sentigraph_evidence_import_plan_v1"
    assert plan.plan_id == f"import_plan_{record.request_id}"
    assert plan_again.plan_id == plan.plan_id
    assert plan.source == "case_draft_handoff"
    assert plan.package_reference.package_name == "sample_package"
    assert plan.counts.evidence == 581
    assert plan.validation.errors == 0
    assert plan.coverage.not_full_web is True
    assert plan.privacy.raw_author_ids_removed is True
    assert plan.proposed_import.import_evidence_rows_now is False
    assert plan.proposed_import.create_case_now is False
    assert plan.proposed_import.run_analysis_now is False
    assert plan.proposed_import.generate_sandbox_now is False
    assert plan.proposed_import.generate_report_now is False
    assert plan.default_evidence_policy.review_status == "review_needed"
    assert plan.default_evidence_policy.verification_status == "source_url_provided_unverified"
    assert plan.default_evidence_policy.trust_label == "medium_low"
    assert plan.default_evidence_policy.dedup_required is True
    assert plan.default_evidence_policy.audit_required is True
    assert plan.readiness.can_import_now is False
    assert plan.safe_mode["evidence_rows_imported"] is False
    assert plan.safe_mode["production_case_created"] is False
    assert len(plan.manual_review_checklist) >= 8
    assert len(list_evidence_import_plans()) == 1
    assert "raw_author_value" not in plan_text


def test_import_plan_requires_existing_case_draft(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="No draft import plan"))
    )
    write_provider_result(tmp_path, record.request_id, provider_result_payload(record.request_id))

    try:
        create_evidence_import_plan(record.request_id)
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "case draft handoff" in str(exc).lower()
    else:
        raise AssertionError("Missing case draft should block import plan")


def test_import_plan_blocks_ineligible_case_drafts(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))

    cases = [
        ("Missing package", lambda draft: draft["package_reference"].update({"package_name": ""}), "package_name is missing"),
        ("Validation failed", lambda draft: draft["validation"].update({"status": "failed"}), "validation status"),
        ("Validation errors", lambda draft: draft["validation"].update({"errors": 2}), "validation errors"),
        ("Unsafe safety", lambda draft: draft["provider_summary"].update({"safety_status": "blocked"}), "safety status"),
        ("No evidence", lambda draft: draft["counts"].update({"evidence": 0}), "counts.evidence"),
        ("Missing privacy", lambda draft: draft["privacy"].update({"raw_author_ids_removed": False}), "privacy flags"),
        ("Claims full web", lambda draft: draft["coverage"].update({"coverage_level": "full_web", "not_full_web": False}), "coverage"),
        ("Not ready", lambda draft: draft["readiness"].update({"state": "blocked"}), "readiness"),
    ]

    for title, mutate, expected_message in cases:
        record = create_analysis_request(
            AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title=title))
        )
        draft_payload = create_valid_case_draft(tmp_path, record.request_id)
        mutate(draft_payload)
        overwrite_case_draft(tmp_path, record.request_id, draft_payload)

        try:
            create_evidence_import_plan(record.request_id)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{title} should not create an import plan")


def test_import_plan_does_not_import_rows_or_create_case_outputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Plan only safety"))
    )
    create_valid_case_draft(tmp_path, record.request_id)

    plan = create_evidence_import_plan(record.request_id)

    assert plan.safe_mode["local_planning_only"] is True
    assert plan.safe_mode["evidence_rows_imported"] is False
    assert plan.safe_mode["production_case_created"] is False
    assert plan.safe_mode["analysis_generated"] is False
    assert plan.safe_mode["sandbox_fixture_generated"] is False
    assert plan.safe_mode["public_event_page_generated"] is False
    assert plan.safe_mode["report_generated"] is False
    assert plan.safe_mode["provider_execution"] is False
    assert plan.safe_mode["collector_jobs_run"] is False
    assert not (tmp_path / "evidence_items.jsonl").exists()
    assert not (tmp_path / "cases").exists()


def test_eligible_import_plan_creates_metadata_only_preview(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Preview from import plan"))
    )
    create_valid_import_plan(tmp_path, record.request_id)

    preview = create_evidence_import_preview(record.request_id)
    preview_again = create_evidence_import_preview(record.request_id)
    preview_text = (tmp_path / "import_previews" / f"{record.request_id}.json").read_text(encoding="utf-8")

    assert preview.schema_ == "sentigraph_evidence_import_preview_v1"
    assert preview.preview_id == f"import_preview_{record.request_id}"
    assert preview_again.preview_id == preview.preview_id
    assert preview.source == "evidence_import_plan"
    assert preview.plan_id == f"import_plan_{record.request_id}"
    assert preview.draft_id == f"draft_{record.request_id}"
    assert preview.package_reference.package_name == "sample_package"
    assert preview.metadata_summary.evidence == 581
    assert preview.validation_summary.errors == 0
    assert preview.coverage_summary.not_full_web is True
    assert preview.privacy_summary.raw_author_ids_removed is True
    assert preview.proposed_evidence_defaults.review_status == "review_needed"
    assert preview.proposed_evidence_defaults.verification_status == "source_url_provided_unverified"
    assert preview.proposed_evidence_defaults.trust_label == "medium_low"
    assert preview.dedup_preview.required is True
    assert preview.dedup_preview.computed_now is False
    assert preview.sample_preview_policy.read_rows_now is False
    assert preview.sample_preview_policy.max_safe_sample_rows_future == 20
    assert preview.sample_preview_policy.redact_author_fields is True
    assert preview.readiness.can_import_now is False
    assert preview.safe_mode["metadata_only_preview"] is True
    assert preview.safe_mode["evidence_rows_read"] is False
    assert preview.safe_mode["evidence_rows_parsed"] is False
    assert preview.safe_mode["evidence_rows_imported"] is False
    assert preview.safe_mode["production_case_created"] is False
    assert preview.safe_mode["analysis_generated"] is False
    assert len(preview.recommended_next_steps) >= 4
    assert len(list_evidence_import_previews()) == 1
    assert "raw_author_value" not in preview_text


def test_import_preview_requires_existing_import_plan(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="No import plan preview"))
    )
    create_valid_case_draft(tmp_path, record.request_id)

    try:
        create_evidence_import_preview(record.request_id)
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "evidence import plan" in str(exc).lower()
    else:
        raise AssertionError("Missing import plan should block preview")


def test_import_preview_blocks_ineligible_import_plans(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))

    cases = [
        ("Missing package", lambda plan: plan["package_reference"].update({"package_name": ""}), "package_name is missing"),
        ("Validation failed", lambda plan: plan["validation"].update({"status": "failed"}), "validation status"),
        ("Validation not run", lambda plan: plan["validation"].update({"status": "not_run"}), "validation status"),
        ("Validation errors", lambda plan: plan["validation"].update({"errors": 2}), "validation errors"),
        ("No evidence", lambda plan: plan["counts"].update({"evidence": 0}), "counts.evidence"),
        ("Missing privacy", lambda plan: plan["privacy"].update({"raw_author_ids_removed": False}), "privacy flags"),
        ("Claims full web", lambda plan: plan["coverage"].update({"coverage_level": "full_web", "not_full_web": False}), "coverage"),
        ("Immediate import", lambda plan: plan["proposed_import"].update({"import_evidence_rows_now": True}), "immediate execution"),
        ("Immediate case", lambda plan: plan["proposed_import"].update({"create_case_now": True}), "immediate execution"),
        ("Immediate analysis", lambda plan: plan["proposed_import"].update({"run_analysis_now": True}), "immediate execution"),
        ("Immediate sandbox", lambda plan: plan["proposed_import"].update({"generate_sandbox_now": True}), "immediate execution"),
        ("Immediate report", lambda plan: plan["proposed_import"].update({"generate_report_now": True}), "immediate execution"),
        ("Not ready", lambda plan: plan["readiness"].update({"state": "blocked"}), "readiness"),
    ]

    for title, mutate, expected_message in cases:
        record = create_analysis_request(
            AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title=title))
        )
        plan_payload = create_valid_import_plan(tmp_path, record.request_id)
        mutate(plan_payload)
        overwrite_import_plan(tmp_path, record.request_id, plan_payload)

        try:
            create_evidence_import_preview(record.request_id)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{title} should not create an import preview")


def test_import_preview_does_not_parse_invalid_evidence_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Invalid rows ignored by preview"))
    )
    plan_payload = create_valid_import_plan(tmp_path, record.request_id)
    package_dir = tmp_path / "external_package"
    package_dir.mkdir()
    (package_dir / "manifest.json").write_text(json.dumps({"package_name": "external_package"}), encoding="utf-8")
    (package_dir / "validation_report.json").write_text(json.dumps({"status": "warn", "errors": 0}), encoding="utf-8")
    (package_dir / "evidence_items.jsonl").write_text("{this is not valid jsonl and must not be parsed", encoding="utf-8")
    plan_payload["package_reference"]["package_name"] = "external_package"
    plan_payload["package_reference"]["package_path"] = str(package_dir)
    overwrite_import_plan(tmp_path, record.request_id, plan_payload)

    preview = create_evidence_import_preview(record.request_id)

    assert preview.package_reference.package_name == "external_package"
    assert preview.metadata_summary.evidence == 581
    assert preview.sample_preview_policy.read_rows_now is False
    assert preview.safe_mode["evidence_rows_read"] is False
    assert preview.safe_mode["evidence_rows_parsed"] is False
    assert not (tmp_path / "cases").exists()


def test_invalid_result_json_sets_warning_without_crash(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Invalid result demo"))
    )
    (tmp_path / "results" / f"{record.request_id}.json").write_text("{not valid json", encoding="utf-8")

    detail = read_analysis_request(record.request_id)

    assert detail.provider_result is None
    assert detail.result_warning
    assert "invalid" in detail.result_warning.lower()


def test_cancel_writes_local_canceled_state(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Cancel local request"))
    )

    result = cancel_analysis_request(record.request_id)
    detail = read_analysis_request(record.request_id)

    assert result.status == "canceled"
    assert detail.request_status == "canceled"
    assert detail.request.sentigraph_metadata["provider_cancel_called"] is False
    assert result.safe_mode["provider_cancel_called"] is False


def test_cancel_does_not_change_package_ready_result(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Package ready request"))
    )
    result_path = tmp_path / "results" / f"{record.request_id}.json"
    result_path.write_text(
        json.dumps(
            {
                "schema": "sentigraph_provider_job_result_v1",
                "request_id": record.request_id,
                "status": "package_ready",
                "safety_status": "safe",
            }
        ),
        encoding="utf-8",
    )

    result = cancel_analysis_request(record.request_id)
    detail = read_analysis_request(record.request_id)

    assert result.warning
    assert result.safe_mode["provider_cancel_called"] is False
    assert detail.request_status == "draft"


def test_config_uses_default_runtime_label_without_absolute_path(monkeypatch) -> None:
    monkeypatch.delenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", raising=False)

    config = get_analysis_request_config()

    assert config.root_label == "runtime/analysis_requests"
    assert "\\" not in config.root_label


def test_store_does_not_use_subprocess_or_network_symbols() -> None:
    source = Path(analysis_request_store.__file__).read_text(encoding="utf-8")

    assert "subprocess" not in source
    assert "requests." not in source
    assert "httpx" not in source
    assert "urllib" not in source
