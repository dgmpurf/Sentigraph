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
    create_evidence_import_review_decision,
    create_manual_evidence_import_execution_preflight,
    create_manual_evidence_import_job,
    create_evidence_row_reader_dry_run,
    create_analysis_request,
    get_analysis_request_config,
    list_evidence_import_plans,
    list_evidence_import_previews,
    list_evidence_import_review_decisions,
    list_manual_evidence_import_execution_preflights,
    list_manual_evidence_import_jobs,
    list_evidence_row_reader_dry_runs,
    list_analysis_requests,
    read_evidence_row_reader_dry_run,
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


def create_valid_import_preview(tmp_path: Path, request_id: str) -> dict:
    create_valid_import_plan(tmp_path, request_id)
    preview = create_evidence_import_preview(request_id)
    preview_path = tmp_path / "import_previews" / f"{request_id}.json"
    return json.loads(preview_path.read_text(encoding="utf-8"))


def overwrite_import_preview(tmp_path: Path, request_id: str, preview_payload: dict) -> None:
    preview_path = tmp_path / "import_previews" / f"{request_id}.json"
    preview_path.write_text(json.dumps(preview_payload), encoding="utf-8")


def full_review_checklist() -> dict:
    return {
        "coverage_reviewed": True,
        "validation_reviewed": True,
        "privacy_reviewed": True,
        "no_raw_author_identifiers": True,
        "not_full_web_acknowledged": True,
        "not_full_platform_acknowledged": True,
        "not_full_thread_acknowledged": True,
        "review_needed_default_acknowledged": True,
        "trust_label_default_acknowledged": True,
        "dedup_required_acknowledged": True,
        "no_auto_analysis_acknowledged": True,
        "no_auto_report_acknowledged": True,
    }


def review_payload(decision: str = "approve_import", **overrides: object) -> dict:
    payload = {
        "reviewer_label": "local_reviewer",
        "decision": decision,
        "target_case_mode": "new_review_case" if decision != "reject_import" else "reject_no_case",
        "target_case_id": None,
        "notes": "Reviewed local metadata-only import preview.",
        "checklist": full_review_checklist(),
    }
    payload.update(overrides)
    return payload


def create_approved_review_decision(tmp_path: Path, request_id: str) -> dict:
    create_valid_import_preview(tmp_path, request_id)
    decision = create_evidence_import_review_decision(request_id, review_payload("approve_import"))
    decision_path = tmp_path / "review_decisions" / f"{request_id}_{decision.decision_id}.json"
    return json.loads(decision_path.read_text(encoding="utf-8"))


def create_package_dir(tmp_path: Path, *, include_required: bool = True) -> Path:
    package_dir = tmp_path / "external_package"
    package_dir.mkdir(parents=True, exist_ok=True)
    if include_required:
        (package_dir / "manifest.json").write_text("{}", encoding="utf-8")
        (package_dir / "validation_report.json").write_text('{"errors":0}', encoding="utf-8")
        (package_dir / "coverage_note.md").write_text("selected public sample only", encoding="utf-8")
        (package_dir / "README.md").write_text("local package fixture", encoding="utf-8")
        (package_dir / "evidence_items.jsonl").write_text(
            '{"raw_author_id":"must_not_be_parsed","comment_text":"forbidden-looking row"}\n{broken',
            encoding="utf-8",
        )
    return package_dir


def create_manual_import_job(tmp_path: Path, request_id: str, *, package_dir: Path | None = None) -> dict:
    create_approved_review_decision(tmp_path, request_id)
    if package_dir is not None:
        preview_path = tmp_path / "import_previews" / f"{request_id}.json"
        preview = json.loads(preview_path.read_text(encoding="utf-8"))
        preview["package_reference"]["package_path"] = str(package_dir)
        preview_path.write_text(json.dumps(preview), encoding="utf-8")
    job = create_manual_evidence_import_job(request_id)
    job_path = tmp_path / "import_jobs" / f"{request_id}_{job.job_id}.json"
    return json.loads(job_path.read_text(encoding="utf-8"))


def create_execution_preflight(tmp_path: Path, request_id: str, *, package_dir: Path | None = None) -> dict:
    create_manual_import_job(tmp_path, request_id, package_dir=package_dir)
    preflight = create_manual_evidence_import_execution_preflight(request_id)
    preflight_path = tmp_path / "execution_preflights" / f"{request_id}_{preflight.preflight_id}.json"
    return json.loads(preflight_path.read_text(encoding="utf-8"))


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


def test_approve_import_creates_append_only_review_decision(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Approve future import"))
    )
    create_valid_import_preview(tmp_path, record.request_id)

    decision = create_evidence_import_review_decision(record.request_id, review_payload("approve_import"))
    decision_again = create_evidence_import_review_decision(
        record.request_id,
        review_payload("request_more_source", notes="Ask provider for broader source notes."),
    )
    decision_files = sorted((tmp_path / "review_decisions").glob(f"{record.request_id}_*.json"))
    decision_text = "\n".join(path.read_text(encoding="utf-8") for path in decision_files)

    assert decision.schema_ == "sentigraph_evidence_import_review_decision_v1"
    assert decision.preview_id == f"import_preview_{record.request_id}"
    assert decision.plan_id == f"import_plan_{record.request_id}"
    assert decision.draft_id == f"draft_{record.request_id}"
    assert decision.request_id == record.request_id
    assert decision.reviewer_label == "local_reviewer"
    assert decision.decision == "approve_import"
    assert decision.readiness.state == "approved_for_future_manual_import"
    assert decision.readiness.can_create_import_job_now is False
    assert decision.readiness.requires_future_manual_import_phase is True
    assert decision.approved_defaults.review_status == "review_needed"
    assert decision.approved_defaults.verification_status == "source_url_provided_unverified"
    assert decision.approved_defaults.trust_label == "medium_low"
    assert decision.audit.source == "manual_review"
    assert decision.safe_mode["evidence_rows_imported"] is False
    assert decision.safe_mode["production_case_created"] is False
    assert decision.safe_mode["analysis_generated"] is False
    assert decision.safe_mode["report_generated"] is False
    assert decision_again.decision_id != decision.decision_id
    assert len(decision_files) == 2
    assert len(list_evidence_import_review_decisions(record.request_id)) == 2
    assert "raw_author_value" not in decision_text


def test_approve_import_blocks_when_checklist_missing(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Approve missing checklist"))
    )
    create_valid_import_preview(tmp_path, record.request_id)
    checklist = full_review_checklist()
    checklist["privacy_reviewed"] = False

    try:
        create_evidence_import_review_decision(record.request_id, review_payload("approve_import", checklist=checklist))
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "acknowledgements" in str(exc)
    else:
        raise AssertionError("approve_import should require all checklist acknowledgements")


def test_non_approve_review_decisions_are_allowed_with_notes(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    expected_states = {
        "reject_import": "rejected",
        "request_more_source": "needs_more_source",
        "mark_limited_sample": "limited_sample_only",
        "hold_for_privacy_review": "held_for_privacy_review",
    }

    for decision_value, expected_state in expected_states.items():
        record = create_analysis_request(
            AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title=f"{decision_value} decision"))
        )
        create_valid_import_preview(tmp_path, record.request_id)
        checklist = full_review_checklist()
        checklist["coverage_reviewed"] = False

        decision = create_evidence_import_review_decision(
            record.request_id,
            review_payload(decision_value, checklist=checklist, notes=f"{decision_value} recorded with notes."),
        )

        assert decision.decision == decision_value
        assert decision.readiness.state == expected_state
        assert decision.readiness.can_create_import_job_now is False
        assert decision.safe_mode["evidence_rows_imported"] is False


def test_review_decision_blocks_missing_preview_and_invalid_payloads(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Missing preview decision"))
    )

    cases = [
        ("Missing preview", record.request_id, review_payload("reject_import"), "import preview"),
    ]

    valid_record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Invalid decision payloads"))
    )
    create_valid_import_preview(tmp_path, valid_record.request_id)
    cases.extend(
        [
            ("Missing reviewer", valid_record.request_id, review_payload("reject_import", reviewer_label=""), "reviewer_label"),
            ("Unknown decision", valid_record.request_id, review_payload("unknown_decision"), "decision"),
            ("Missing notes", valid_record.request_id, review_payload("request_more_source", notes=""), "notes"),
        ]
    )

    for title, request_id, payload, expected_message in cases:
        try:
            create_evidence_import_review_decision(request_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{title} should block review decision")


def test_review_decision_blocks_unsafe_preview(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))

    cases = [
        ("Validation errors", lambda preview: preview["validation_summary"].update({"errors": 2}), "validation errors"),
        ("Missing privacy", lambda preview: preview["privacy_summary"].update({"raw_author_ids_removed": False}), "privacy flags"),
        ("Claims full web", lambda preview: preview["coverage_summary"].update({"coverage_level": "full_web", "not_full_web": False}), "coverage"),
        ("Wrong review default", lambda preview: preview["proposed_evidence_defaults"].update({"review_status": "approved"}), "review_status"),
        ("Wrong verification default", lambda preview: preview["proposed_evidence_defaults"].update({"verification_status": "verified"}), "verification_status"),
        ("Wrong trust default", lambda preview: preview["proposed_evidence_defaults"].update({"trust_label": "high"}), "trust_label"),
        ("Reads rows", lambda preview: preview["sample_preview_policy"].update({"read_rows_now": True}), "read_rows_now"),
        ("Not ready", lambda preview: preview["readiness"].update({"state": "blocked"}), "readiness"),
    ]

    for title, mutate, expected_message in cases:
        record = create_analysis_request(
            AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title=title))
        )
        preview_payload = create_valid_import_preview(tmp_path, record.request_id)
        mutate(preview_payload)
        overwrite_import_preview(tmp_path, record.request_id, preview_payload)

        try:
            create_evidence_import_review_decision(record.request_id, review_payload("reject_import", notes=title))
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{title} should block review decision")


def test_review_decision_does_not_import_rows_or_create_outputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Decision only safety"))
    )
    preview_payload = create_valid_import_preview(tmp_path, record.request_id)
    package_dir = tmp_path / "external_package"
    package_dir.mkdir()
    (package_dir / "evidence_items.jsonl").write_text("{invalid rows should not be parsed", encoding="utf-8")
    preview_payload["package_reference"]["package_path"] = str(package_dir)
    overwrite_import_preview(tmp_path, record.request_id, preview_payload)

    decision = create_evidence_import_review_decision(record.request_id, review_payload("approve_import"))

    assert decision.safe_mode["evidence_rows_read"] is False
    assert decision.safe_mode["evidence_rows_parsed"] is False
    assert decision.safe_mode["evidence_rows_imported"] is False
    assert decision.safe_mode["production_case_created"] is False
    assert decision.safe_mode["analysis_generated"] is False
    assert not (tmp_path / "cases").exists()


def test_approved_review_decision_creates_manual_import_job_dry_run(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Manual import job dry run"))
    )
    decision_payload = create_approved_review_decision(tmp_path, record.request_id)

    job = create_manual_evidence_import_job(record.request_id)
    second_job = create_manual_evidence_import_job(
        record.request_id,
        {"decision_id": decision_payload["decision_id"], "target_case_mode": "new_review_case"},
    )
    job_files = sorted((tmp_path / "import_jobs").glob(f"{record.request_id}_*.json"))
    job_text = "\n".join(path.read_text(encoding="utf-8") for path in job_files)

    assert job.schema_ == "sentigraph_manual_evidence_import_job_v1"
    assert job.decision_id == decision_payload["decision_id"]
    assert job.preview_id == f"import_preview_{record.request_id}"
    assert job.plan_id == f"import_plan_{record.request_id}"
    assert job.draft_id == f"draft_{record.request_id}"
    assert job.request_id == record.request_id
    assert job.job_type == "manual_evidence_import"
    assert job.execution_mode == "dry_run_gate"
    assert job.status == "draft_not_executed"
    assert job.target_case.mode == "new_review_case"
    assert job.target_case.create_case_now is False
    assert job.package_reference.package_name == "sample_package"
    assert job.metadata_summary.evidence == 581
    assert job.approved_defaults.review_status == "review_needed"
    assert job.approved_defaults.verification_status == "source_url_provided_unverified"
    assert job.approved_defaults.trust_label == "medium_low"
    assert job.dry_run_result.would_import_evidence_rows is True
    assert job.dry_run_result.import_evidence_rows_now is False
    assert job.dry_run_result.would_create_or_attach_case is True
    assert job.dry_run_result.create_case_now is False
    assert job.dry_run_result.would_run_dedup is True
    assert job.dry_run_result.run_dedup_now is False
    assert job.dry_run_result.would_create_review_queue_items is True
    assert job.dry_run_result.create_review_queue_now is False
    assert job.dry_run_result.would_run_analysis is False
    assert job.dry_run_result.run_analysis_now is False
    assert job.dry_run_result.generate_report_now is False
    assert job.preflight_checks.approved_import_decision_present is True
    assert job.preflight_checks.coverage_acknowledged is True
    assert job.preflight_checks.no_raw_author_identifiers_acknowledged is True
    assert job.readiness.state == "ready_for_future_manual_import_execution"
    assert job.readiness.can_execute_now is False
    assert job.readiness.requires_separate_import_phase is True
    assert job.safe_mode["evidence_rows_read"] is False
    assert job.safe_mode["evidence_rows_parsed"] is False
    assert job.safe_mode["evidence_rows_imported"] is False
    assert job.safe_mode["production_case_created"] is False
    assert job.safe_mode["analysis_generated"] is False
    assert second_job.job_id != job.job_id
    assert len(job_files) == 2
    assert len(list_manual_evidence_import_jobs(record.request_id)) == 2
    assert "raw_author_value" not in job_text


def test_manual_import_job_blocks_non_approve_latest_decisions(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    blocked_decisions = [
        "reject_import",
        "request_more_source",
        "mark_limited_sample",
        "hold_for_privacy_review",
    ]

    for decision_value in blocked_decisions:
        record = create_analysis_request(
            AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title=f"{decision_value} job block"))
        )
        create_valid_import_preview(tmp_path, record.request_id)
        create_evidence_import_review_decision(
            record.request_id,
            review_payload(decision_value, notes=f"{decision_value} should block job."),
        )

        try:
            create_manual_evidence_import_job(record.request_id)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert "approve_import" in str(exc)
        else:
            raise AssertionError(f"{decision_value} should block manual import job draft")


def test_manual_import_job_blocks_missing_decision_and_bad_target(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    missing_record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Missing decision job"))
    )
    create_valid_import_preview(tmp_path, missing_record.request_id)
    approved_record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Bad target job"))
    )
    create_approved_review_decision(tmp_path, approved_record.request_id)

    cases = [
        ("Missing decision", missing_record.request_id, {}, "review decision"),
        ("Existing case without id", approved_record.request_id, {"target_case_mode": "existing_case"}, "target_case_id"),
        ("Invalid target", approved_record.request_id, {"target_case_mode": "reject_no_case"}, "target_case_mode"),
    ]

    for title, request_id, payload, expected_message in cases:
        try:
            create_manual_evidence_import_job(request_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{title} should block manual import job")


def test_manual_import_job_blocks_unsafe_decision_and_preview(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))

    cases = [
        ("Checklist missing", "decision", lambda decision: decision["checklist"].update({"privacy_reviewed": False}), "acknowledgements"),
        ("Validation errors", "preview", lambda preview: preview["validation_summary"].update({"errors": 2}), "validation errors"),
        ("No evidence", "preview", lambda preview: preview["metadata_summary"].update({"evidence": 0}), "metadata_summary.evidence"),
        ("Missing package", "preview", lambda preview: preview["package_reference"].update({"package_name": ""}), "package_name"),
        ("Privacy missing", "preview", lambda preview: preview["privacy_summary"].update({"raw_author_ids_removed": False}), "privacy flags"),
        ("Full web claim", "preview", lambda preview: preview["coverage_summary"].update({"not_full_web": False}), "coverage"),
        ("Reads rows", "preview", lambda preview: preview["sample_preview_policy"].update({"read_rows_now": True}), "read_rows_now"),
    ]

    for title, target, mutate, expected_message in cases:
        record = create_analysis_request(
            AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title=title))
        )
        decision_payload = create_approved_review_decision(tmp_path, record.request_id)
        if target == "decision":
            decision_path = tmp_path / "review_decisions" / f"{record.request_id}_{decision_payload['decision_id']}.json"
            decision = json.loads(decision_path.read_text(encoding="utf-8"))
            mutate(decision)
            decision_path.write_text(json.dumps(decision), encoding="utf-8")
        else:
            preview_path = tmp_path / "import_previews" / f"{record.request_id}.json"
            preview = json.loads(preview_path.read_text(encoding="utf-8"))
            mutate(preview)
            preview_path.write_text(json.dumps(preview), encoding="utf-8")

        try:
            create_manual_evidence_import_job(record.request_id)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{title} should block manual import job")


def test_manual_import_job_existing_case_requires_target_id_and_remains_dry_run(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Existing case dry run"))
    )
    create_approved_review_decision(tmp_path, record.request_id)

    job = create_manual_evidence_import_job(
        record.request_id,
        {"target_case_mode": "existing_case", "target_case_id": "case_existing_review_only"},
    )

    assert job.target_case.mode == "existing_case"
    assert job.target_case.target_case_id == "case_existing_review_only"
    assert job.target_case.create_case_now is False
    assert job.dry_run_result.create_case_now is False
    assert job.readiness.can_execute_now is False


def test_manual_import_job_does_not_parse_invalid_evidence_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Dry run ignores rows"))
    )
    create_approved_review_decision(tmp_path, record.request_id)
    package_dir = tmp_path / "external_package"
    package_dir.mkdir()
    (package_dir / "evidence_items.jsonl").write_text("{invalid rows must not be parsed", encoding="utf-8")
    preview_path = tmp_path / "import_previews" / f"{record.request_id}.json"
    preview = json.loads(preview_path.read_text(encoding="utf-8"))
    preview["package_reference"]["package_path"] = str(package_dir)
    preview_path.write_text(json.dumps(preview), encoding="utf-8")

    job = create_manual_evidence_import_job(record.request_id)

    assert job.safe_mode["evidence_rows_read"] is False
    assert job.safe_mode["evidence_rows_parsed"] is False
    assert job.safe_mode["evidence_rows_imported"] is False
    assert not (tmp_path / "cases").exists()


def test_manual_import_execution_preflight_checks_job_and_package_without_opening_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Execution preflight happy path"))
    )
    package_dir = create_package_dir(tmp_path)
    job_payload = create_manual_import_job(tmp_path, record.request_id, package_dir=package_dir)

    preflight = create_manual_evidence_import_execution_preflight(record.request_id)
    second_preflight = create_manual_evidence_import_execution_preflight(
        record.request_id,
        {"job_id": job_payload["job_id"], "created_by": "second_reviewer"},
    )
    preflight_files = sorted((tmp_path / "execution_preflights").glob(f"{record.request_id}_*.json"))
    preflight_text = "\n".join(path.read_text(encoding="utf-8") for path in preflight_files)

    assert preflight.schema_ == "sentigraph_manual_evidence_import_execution_preflight_v1"
    assert preflight.job_id == job_payload["job_id"]
    assert preflight.decision_id == job_payload["decision_id"]
    assert preflight.preview_id == job_payload["preview_id"]
    assert preflight.plan_id == job_payload["plan_id"]
    assert preflight.draft_id == job_payload["draft_id"]
    assert preflight.request_id == record.request_id
    assert preflight.source == "manual_evidence_import_job_dry_run"
    assert preflight.execution_mode == "preflight_only"
    assert preflight.status == "preflight_passed"
    assert preflight.package_reference.package_name == "sample_package"
    assert preflight.package_file_checks.manifest_present is True
    assert preflight.package_file_checks.validation_report_present is True
    assert preflight.package_file_checks.coverage_note_present is True
    assert preflight.package_file_checks.readme_present is True
    assert preflight.package_file_checks.evidence_items_jsonl_present is True
    assert preflight.package_file_checks.evidence_items_csv_present is False
    assert preflight.package_file_checks.row_files_opened is False
    assert preflight.package_file_checks.row_files_parsed is False
    assert preflight.metadata_summary.evidence == 581
    assert preflight.validation_summary.errors == 0
    assert preflight.coverage_summary.not_full_web is True
    assert preflight.privacy_summary.raw_author_ids_removed is True
    assert preflight.target_case_preflight.mode == "new_review_case"
    assert preflight.target_case_preflight.create_case_now is False
    assert preflight.target_case_preflight.review_only_required is True
    assert preflight.target_case_preflight.analysis_included_default is False
    assert preflight.future_row_reader_plan.would_read_rows_in_future_phase is True
    assert preflight.future_row_reader_plan.read_rows_now is False
    assert preflight.future_row_reader_plan.streaming_required is True
    assert preflight.future_row_reader_plan.fail_closed_on_privacy_violation is True
    assert preflight.future_staging_plan.stage_rows_now is False
    assert preflight.future_staging_plan.default_review_status == "review_needed"
    assert preflight.future_staging_plan.default_verification_status == "source_url_provided_unverified"
    assert preflight.future_staging_plan.default_trust_label == "medium_low"
    assert preflight.future_staging_plan.analysis_included is False
    assert preflight.future_governance_plan.dedup_required is True
    assert preflight.future_governance_plan.dedup_run_now is False
    assert preflight.future_governance_plan.review_queue_created_now is False
    assert preflight.readiness.state == "ready_for_future_manual_import_execution"
    assert preflight.readiness.can_execute_now is False
    assert preflight.readiness.requires_separate_execution_phase is True
    assert preflight.safe_mode["evidence_rows_opened"] is False
    assert preflight.safe_mode["evidence_rows_parsed"] is False
    assert preflight.safe_mode["evidence_rows_imported"] is False
    assert preflight.safe_mode["production_case_created"] is False
    assert preflight.safe_mode["analysis_generated"] is False
    assert second_preflight.preflight_id != preflight.preflight_id
    assert len(preflight_files) == 2
    assert len(list_manual_evidence_import_execution_preflights(record.request_id)) == 2
    assert "must_not_be_parsed" not in preflight_text
    assert "forbidden-looking row" not in preflight_text
    assert not (tmp_path / "cases").exists()


def test_manual_import_execution_preflight_blocks_missing_or_unsafe_job(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    missing_record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Missing job preflight"))
    )
    create_approved_review_decision(tmp_path, missing_record.request_id)
    unsafe_record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Unsafe job preflight"))
    )
    create_manual_import_job(tmp_path, unsafe_record.request_id)
    job_path = next((tmp_path / "import_jobs").glob(f"{unsafe_record.request_id}_*.json"))
    job = json.loads(job_path.read_text(encoding="utf-8"))
    job["dry_run_result"]["import_evidence_rows_now"] = True
    job_path.write_text(json.dumps(job), encoding="utf-8")

    cases = [
        ("Missing job", missing_record.request_id, "manual import job"),
        ("Unsafe now flag", unsafe_record.request_id, "import_evidence_rows_now"),
    ]
    for title, request_id, expected_message in cases:
        try:
            create_manual_evidence_import_execution_preflight(request_id)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{title} should block execution preflight")


def test_manual_import_execution_preflight_blocks_superseded_decision_and_bad_preview(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    cases = [
        ("Superseded decision", "decision", lambda record_id: create_evidence_import_review_decision(record_id, review_payload("reject_import", notes="Reject later.")), "approve_import"),
        ("Validation errors", "preview", lambda preview: preview["validation_summary"].update({"errors": 1}), "validation errors"),
        ("No evidence", "preview", lambda preview: preview["metadata_summary"].update({"evidence": 0}), "metadata_summary.evidence"),
        ("Missing package", "preview", lambda preview: preview["package_reference"].update({"package_name": ""}), "package_name"),
        ("Privacy missing", "preview", lambda preview: preview["privacy_summary"].update({"raw_author_ids_removed": False}), "privacy flags"),
        ("Full web claim", "preview", lambda preview: preview["coverage_summary"].update({"not_full_web": False}), "coverage"),
    ]

    for title, target, mutate, expected_message in cases:
        record = create_analysis_request(
            AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title=title))
        )
        create_manual_import_job(tmp_path, record.request_id)
        if target == "decision":
            mutate(record.request_id)
        else:
            preview_path = tmp_path / "import_previews" / f"{record.request_id}.json"
            preview = json.loads(preview_path.read_text(encoding="utf-8"))
            mutate(preview)
            preview_path.write_text(json.dumps(preview), encoding="utf-8")

        try:
            create_manual_evidence_import_execution_preflight(record.request_id)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{title} should block execution preflight")


def test_manual_import_execution_preflight_warns_when_package_path_unavailable_and_blocks_missing_required_files(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    warn_record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Preflight package path warn"))
    )
    create_manual_import_job(tmp_path, warn_record.request_id)
    warned = create_manual_evidence_import_execution_preflight(warn_record.request_id)
    assert warned.status == "preflight_warn"
    assert warned.package_file_checks.package_path_checked is False
    assert warned.package_file_checks.row_files_opened is False

    blocked_record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Preflight missing manifest"))
    )
    package_dir = create_package_dir(tmp_path / "missing_required_case", include_required=False)
    (package_dir / "validation_report.json").write_text("{}", encoding="utf-8")
    (package_dir / "coverage_note.md").write_text("coverage", encoding="utf-8")
    create_manual_import_job(tmp_path, blocked_record.request_id, package_dir=package_dir)

    try:
        create_manual_evidence_import_execution_preflight(blocked_record.request_id)
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "manifest" in str(exc)
    else:
        raise AssertionError("Missing manifest should block execution preflight when package path is readable")


def test_manual_import_execution_preflight_existing_case_requires_target_id(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Preflight existing case"))
    )
    create_approved_review_decision(tmp_path, record.request_id)
    job = create_manual_evidence_import_job(
        record.request_id,
        {"target_case_mode": "existing_case", "target_case_id": "case_review_only_existing"},
    )

    preflight = create_manual_evidence_import_execution_preflight(record.request_id, {"job_id": job.job_id})

    assert preflight.target_case_preflight.mode == "existing_case"
    assert preflight.target_case_preflight.target_case_id == "case_review_only_existing"
    assert preflight.target_case_preflight.create_case_now is False
    assert preflight.target_case_preflight.analysis_included_default is False


def test_evidence_row_reader_dry_run_reads_safe_synthetic_fixture_only(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Safe fixture row reader"))
    )
    preflight_payload = create_execution_preflight(tmp_path, record.request_id, package_dir=create_package_dir(tmp_path))

    dry_run = create_evidence_row_reader_dry_run(
        record.request_id,
        {"preflight_id": preflight_payload["preflight_id"], "fixture_name": "safe_evidence_items", "max_rows": 20},
    )
    second_dry_run = create_evidence_row_reader_dry_run(
        record.request_id,
        {"preflight_id": preflight_payload["preflight_id"], "fixture_name": "safe_evidence_items", "max_rows": 1},
    )
    dry_run_files = sorted((tmp_path / "row_reader_dry_runs").glob(f"{record.request_id}_*.json"))
    dry_run_text = "\n".join(path.read_text(encoding="utf-8") for path in dry_run_files)
    read_back = read_evidence_row_reader_dry_run(record.request_id, dry_run.dry_run_id)

    assert dry_run.schema_ == "sentigraph_evidence_row_reader_dry_run_v1"
    assert dry_run.preflight_id == preflight_payload["preflight_id"]
    assert dry_run.job_id == preflight_payload["job_id"]
    assert dry_run.source == "execution_preflight"
    assert dry_run.execution_mode == "synthetic_fixture_row_reader_dry_run"
    assert dry_run.status == "passed"
    assert dry_run.fixture_policy.synthetic_fixture_only is True
    assert dry_run.fixture_policy.real_provider_package_allowed is False
    assert dry_run.fixture_policy.external_collector_package_allowed is False
    assert dry_run.fixture_policy.max_rows == 20
    assert dry_run.row_source.source_type == "synthetic_fixture"
    assert dry_run.row_source.real_package_path_used is False
    assert dry_run.counts.rows_seen == 2
    assert dry_run.counts.accepted_for_preview == 2
    assert dry_run.counts.quarantined == 0
    assert dry_run.counts.rejected == 0
    assert dry_run.privacy_scan.privacy_stop_triggered is False
    assert len(dry_run.redacted_preview_rows) == 2
    assert dry_run.redacted_preview_rows[0].evidence_candidate.body_text_preview
    assert dry_run.redacted_preview_rows[0].governance_defaults.review_status == "review_needed"
    assert dry_run.redacted_preview_rows[0].governance_defaults.analysis_included is False
    assert dry_run.now_flags.import_evidence_rows_now is False
    assert dry_run.now_flags.write_evidence_layer_now is False
    assert dry_run.now_flags.create_case_now is False
    assert dry_run.now_flags.create_review_queue_now is False
    assert dry_run.now_flags.run_dedup_now is False
    assert dry_run.now_flags.run_analysis_now is False
    assert dry_run.now_flags.generate_sandbox_now is False
    assert dry_run.now_flags.generate_report_now is False
    assert dry_run.readiness.can_import_now is False
    assert dry_run.readiness.requires_future_phase is True
    assert second_dry_run.dry_run_id != dry_run.dry_run_id
    assert second_dry_run.counts.rows_seen == 1
    assert len(dry_run_files) == 2
    assert len(list_evidence_row_reader_dry_runs(record.request_id)) == 2
    assert read_back.dry_run_id == dry_run.dry_run_id
    assert "synthetic-user-123" not in dry_run_text
    assert "Synthetic Name" not in dry_run_text
    assert "Synthetic private message" not in dry_run_text
    assert not (tmp_path / "cases").exists()


def test_evidence_row_reader_dry_run_quarantines_forbidden_fields_and_rejects_invalid_json(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Mixed fixture row reader"))
    )
    preflight_payload = create_execution_preflight(tmp_path, record.request_id, package_dir=create_package_dir(tmp_path))

    dry_run = create_evidence_row_reader_dry_run(
        record.request_id,
        {"preflight_id": preflight_payload["preflight_id"], "fixture_name": "mixed_evidence_items", "max_rows": 20},
    )
    text = json.dumps(dry_run.model_dump(mode="json", by_alias=True), ensure_ascii=False)

    assert dry_run.status == "warn"
    assert dry_run.counts.rows_seen == 4
    assert dry_run.counts.accepted_for_preview == 1
    assert dry_run.counts.quarantined == 2
    assert dry_run.counts.rejected == 1
    assert dry_run.privacy_scan.raw_author_id_detected == 1
    assert dry_run.privacy_scan.raw_author_name_detected == 1
    assert dry_run.privacy_scan.profile_url_detected == 1
    assert dry_run.privacy_scan.private_message_detected == 1
    assert dry_run.privacy_scan.privacy_stop_triggered is True
    assert len(dry_run.quarantine_summary) == 2
    assert len(dry_run.rejection_summary) == 1
    assert "forbidden_fields_detected" in text
    assert "synthetic-user-123" not in text
    assert "Synthetic Name" not in text
    assert "example.test/profile/synthetic" not in text
    assert "Synthetic private message" not in text


def test_evidence_row_reader_dry_run_blocks_unsafe_inputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Blocked row reader"))
    )
    preflight_payload = create_execution_preflight(tmp_path, record.request_id, package_dir=create_package_dir(tmp_path))
    preflight_id = preflight_payload["preflight_id"]
    preflight_path = tmp_path / "execution_preflights" / f"{record.request_id}_{preflight_id}.json"
    blocked_preflight = dict(preflight_payload)
    blocked_preflight["status"] = "preflight_blocked"
    preflight_path.write_text(json.dumps(blocked_preflight), encoding="utf-8")

    cases = [
        ("Missing preflight", "missing_preflight", {"preflight_id": "manual_import_preflight_missing"}, "execution preflight"),
        ("Blocked preflight", record.request_id, {"preflight_id": preflight_id}, "preflight_blocked"),
        ("Too many rows", record.request_id, {"preflight_id": preflight_id, "max_rows": 21}, "max_rows"),
        ("Path traversal", record.request_id, {"preflight_id": preflight_id, "fixture_name": "../safe_evidence_items"}, "fixture"),
        ("Real package path", record.request_id, {"preflight_id": preflight_id, "fixture_name": "safe_evidence_items", "row_source_path": str(create_package_dir(tmp_path) / "evidence_items.jsonl")}, "synthetic fixture"),
        ("Now flag", record.request_id, {"preflight_id": preflight_id, "fixture_name": "safe_evidence_items", "now_flags": {"run_analysis_now": True}}, "now flags"),
    ]
    for title, request_id, payload, expected_message in cases:
        preflight_path.write_text(
            json.dumps(blocked_preflight if title == "Blocked preflight" else preflight_payload),
            encoding="utf-8",
        )
        try:
            create_evidence_row_reader_dry_run(request_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{title} should block row reader dry-run")


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
