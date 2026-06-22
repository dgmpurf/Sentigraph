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
    create_real_package_row_preview,
    create_review_only_case,
    create_review_only_case_staging_import,
    create_review_queue_initialization,
    create_review_queue_completion_gate,
    create_dedup_preview,
    create_dedup_group_review_action,
    create_analysis_ready_promotion_gate,
    create_analysis_result_boundary_gate,
    create_report_generation_gate,
    create_summary_report_candidate,
    create_final_summary_report_review_gate,
    create_final_summary_report,
    create_final_summary_report_export_gate,
    create_manual_analysis_execution,
    create_manual_analysis_trigger,
    create_report_export_public_access_external_delivery_gate,
    create_review_queue_item_action,
    create_analysis_request,
    get_analysis_request_config,
    list_evidence_import_plans,
    list_evidence_import_previews,
    list_evidence_import_review_decisions,
    list_manual_evidence_import_execution_preflights,
    list_manual_evidence_import_jobs,
    list_evidence_row_reader_dry_runs,
    list_real_package_row_previews,
    list_review_only_cases,
    list_review_only_case_staging_imports,
    list_review_queue_action_audits,
    list_review_queue_completion_gates,
    list_dedup_previews,
    list_dedup_group_review_audits,
    list_analysis_ready_promotion_gates,
    list_analysis_result_boundary_gate_audits,
    list_analysis_result_boundary_gates,
    list_report_generation_gate_audits,
    list_report_generation_gates,
    list_summary_report_candidate_audits,
    list_summary_report_candidates,
    list_final_summary_report_review_gate_audits,
    list_final_summary_report_review_gates,
    list_final_summary_report_audits,
    list_final_summary_reports,
    list_final_summary_report_export_gate_audits,
    list_final_summary_report_export_gates,
    list_report_export_public_access_external_delivery_gate_audits,
    list_report_export_public_access_external_delivery_gates,
    list_manual_analysis_execution_audits,
    list_manual_analysis_executions,
    list_manual_analysis_result_candidates,
    list_manual_analysis_trigger_audits,
    list_manual_analysis_triggers,
    list_promotion_decision_audits,
    list_review_queue_initializations,
    list_analysis_requests,
    read_evidence_row_reader_dry_run,
    read_real_package_row_preview,
    read_review_only_case,
    read_review_only_case_staging_import,
    read_review_queue_action_audits_for_item,
    read_review_queue_completion_gate,
    read_dedup_preview,
    read_dedup_group_review_audits_for_group,
    read_analysis_ready_promotion_gate,
    read_analysis_result_boundary_gate,
    read_report_generation_gate,
    read_summary_report_candidate,
    read_final_summary_report_review_gate,
    read_final_summary_report,
    read_final_summary_report_export_gate,
    read_report_export_public_access_external_delivery_gate,
    read_manual_analysis_execution,
    read_manual_analysis_result_candidate,
    read_manual_analysis_trigger,
    read_review_queue_initialization,
    read_review_queue_item_batch,
    read_staged_evidence_candidate_batch,
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


def create_real_preview_package(tmp_path: Path, *, mixed: bool = False, include_rows: bool = True) -> Path:
    package_dir = tmp_path / ("mixed_real_preview_package" if mixed else "safe_real_preview_package")
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "manifest.json").write_text(
        json.dumps({"package_name": package_dir.name, "package_role": "selected_public_sample"}),
        encoding="utf-8",
    )
    (package_dir / "validation_report.json").write_text(
        json.dumps({"validation": {"errors": 0, "warnings": 0}, "errors": 0, "coverage": {"not_full_web": True}}),
        encoding="utf-8",
    )
    (package_dir / "coverage_note.md").write_text(
        "selected public sample only; not full-web, not full-platform, not full-thread",
        encoding="utf-8",
    )
    (package_dir / "README.md").write_text("local real package preview fixture", encoding="utf-8")
    if include_rows:
        if mixed:
            rows = [
                {
                    "platform": "synthetic_forum",
                    "evidence_type": "comment",
                    "source_url": "https://example.invalid/real-preview/accepted",
                    "title": "Accepted future preview row",
                    "body_text": "Safe future preview text.",
                    "created_at": "2026-06-18T01:00:00Z",
                    "language": "en",
                    "like_count": 3,
                },
                {
                    "platform": "synthetic_forum",
                    "evidence_type": "comment",
                    "source_url": "https://example.invalid/real-preview/quarantine",
                    "title": "Forbidden identity row",
                    "body_text": "This row should be quarantined.",
                    "raw_author_id": "real-preview-user-should-not-return",
                    "raw_author_name": "Real Preview Name Should Not Return",
                    "profile_url": "https://example.test/profile/real-preview",
                },
                "{bad json",
                {
                    "platform": "synthetic_forum",
                    "evidence_type": "comment",
                    "source_url": "https://example.invalid/real-preview/privacy-stop",
                    "title": "Private message row",
                    "body_text": "This row should trigger privacy stop.",
                    "private_message": "Real preview private message should not return.",
                },
            ]
        else:
            rows = [
                {
                    "platform": "synthetic_forum",
                    "evidence_type": "comment",
                    "source_url": "https://example.invalid/real-preview/1",
                    "title": "Safe local package row",
                    "body_text": "Safe local package row preview body. " * 12,
                    "created_at": "2026-06-18T01:00:00Z",
                    "language": "en",
                    "like_count": 9,
                    "reply_count": 2,
                },
                {
                    "platform": "synthetic_news",
                    "evidence_type": "article",
                    "source_url": "https://example.invalid/real-preview/2",
                    "title": "Second safe local package row",
                    "body_text": "Second safe preview row.",
                    "created_at": "2026-06-18T02:00:00Z",
                    "language": "en",
                },
            ]
        lines = [json.dumps(row, ensure_ascii=False) if isinstance(row, dict) else row for row in rows]
        (package_dir / "evidence_items.jsonl").write_text("\n".join(lines), encoding="utf-8")
    return package_dir


def create_many_row_preview_package(tmp_path: Path, *, row_count: int = 4) -> Path:
    package_dir = tmp_path / "many_safe_real_preview_package"
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "manifest.json").write_text(
        json.dumps({"package_name": package_dir.name, "package_role": "selected_public_sample"}),
        encoding="utf-8",
    )
    (package_dir / "validation_report.json").write_text(json.dumps({"errors": 0, "warnings": 0}), encoding="utf-8")
    (package_dir / "coverage_note.md").write_text(
        "selected public sample only; not full-web, not full-platform, not full-thread",
        encoding="utf-8",
    )
    (package_dir / "README.md").write_text("local many-row preview fixture", encoding="utf-8")
    rows = [
        {
            "platform": "synthetic_forum",
            "evidence_type": "comment",
            "source_url": f"https://example.invalid/real-preview/many/{index}",
            "title": f"Safe local package row {index}",
            "body_text": f"Safe local package row preview body {index}.",
            "created_at": "2026-06-18T01:00:00Z",
            "language": "en",
            "like_count": index,
        }
        for index in range(1, row_count + 1)
    ]
    (package_dir / "evidence_items.jsonl").write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows),
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


def real_preview_ack_payload(**overrides: object) -> dict:
    payload = {
        "acknowledge_real_package_preview": True,
        "acknowledge_no_import": True,
        "acknowledge_preview_not_representative": True,
        "acknowledge_privacy_stop": True,
    }
    payload.update(overrides)
    return payload


def staging_import_ack_payload(**overrides: object) -> dict:
    payload = {
        "acknowledge_review_only_staging": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_no_analysis": True,
        "acknowledge_no_report": True,
    }
    payload.update(overrides)
    return payload


def review_queue_init_ack_payload(**overrides: object) -> dict:
    payload = {
        "acknowledge_review_only_queue": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_no_dedup": True,
        "acknowledge_no_analysis": True,
        "acknowledge_no_report": True,
    }
    payload.update(overrides)
    return payload


def review_queue_action_payload(action: str = "approve", **overrides: object) -> dict:
    payload = {
        "action": action,
        "reviewer_label": "local_reviewer",
        "note": f"Local review-only action: {action}.",
        "acknowledge_review_only_action": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_no_dedup": True,
        "acknowledge_no_analysis": True,
        "acknowledge_no_report": True,
    }
    payload.update(overrides)
    return payload


def review_queue_completion_gate_payload(**overrides: object) -> dict:
    payload = {
        "minimum_reviewed_ratio": 1.0,
        "allow_deferred_items": False,
        "acknowledge_completion_is_not_dedup": True,
        "acknowledge_completion_is_not_analysis": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_no_report": True,
    }
    payload.update(overrides)
    return payload


def dedup_preview_payload(**overrides: object) -> dict:
    payload = {
        "include_marked_weak": True,
        "include_duplicate_merged": True,
        "acknowledge_dedup_preview_only": True,
        "acknowledge_no_production_dedup": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_analysis": True,
        "acknowledge_no_report": True,
    }
    payload.update(overrides)
    return payload


def dedup_group_review_action_payload(action: str = "confirm_group", **overrides: object) -> dict:
    payload = {
        "action": action,
        "reviewer_label": "dedup_reviewer",
        "note": f"Review-only dedup group action: {action}.",
        "acknowledge_review_only_group_action": True,
        "acknowledge_no_production_dedup": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_analysis": True,
        "acknowledge_no_report": True,
    }
    payload.update(overrides)
    return payload


def promotion_gate_payload(decision: str = "approve_for_future_manual_analysis_trigger", **overrides: object) -> dict:
    payload = {
        "promotion_decision": decision,
        "reviewer_label": "promotion_reviewer",
        "note": f"Local promotion decision: {decision}.",
        "coverage_limitations_acknowledged": True,
        "privacy_acknowledged": True,
        "weak_evidence_warning_acknowledged": True,
        "dedup_preview_warning_acknowledged": True,
        "provider_output_is_evidence_not_truth_acknowledged": True,
        "acknowledge_promotion_is_not_analysis": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_no_production_dedup": True,
        "acknowledge_no_report": True,
    }
    payload.update(overrides)
    return payload


def manual_analysis_trigger_payload(decision: str = "trigger_analysis", **overrides: object) -> dict:
    payload = {
        "promotion_gate_id": "",
        "review_case_id": "",
        "trigger_decision": decision,
        "reviewer_label": "manual_trigger_reviewer",
        "note": f"Local manual analysis trigger decision: {decision}.",
        "analysis_scope_mode": "promotion_set_preview",
        "coverage_acknowledged": True,
        "privacy_acknowledged": True,
        "weak_warning_acknowledged": True,
        "dedup_warning_acknowledged": True,
        "provider_output_is_evidence_not_truth_acknowledged": True,
        "not_official_verification_acknowledged": True,
        "not_full_web_coverage_acknowledged": True,
        "acknowledge_trigger_record_only": True,
        "acknowledge_no_analysis_run": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_no_report": True,
        "acknowledge_no_sandbox_or_public_event": True,
    }
    payload.update(overrides)
    return payload


def analysis_result_boundary_gate_payload(**overrides: object) -> dict:
    payload = {
        "manual_trigger_id": "",
        "promotion_gate_id": "",
        "review_case_id": "",
        "reviewer_label": "boundary_gate_reviewer",
        "note": "Local Analysis Result Boundary Gate readiness review.",
        "coverage_limitation_acknowledged": True,
        "weak_evidence_warning_acknowledged": True,
        "rejected_evidence_exclusion_acknowledged": True,
        "dedup_warning_acknowledged": True,
        "provider_output_is_evidence_not_truth_acknowledged": True,
        "not_official_verification_acknowledged": True,
        "not_full_web_coverage_acknowledged": True,
        "audit_trace_acknowledged": True,
        "acknowledge_boundary_gate_only": True,
        "acknowledge_no_analysis_run": True,
        "acknowledge_no_analysis_result_generation": True,
        "acknowledge_no_report_generation": True,
        "acknowledge_no_sandbox_or_public_event": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
    }
    payload.update(overrides)
    return payload


def manual_analysis_execution_payload(**overrides: object) -> dict:
    payload = {
        "manual_trigger_id": "",
        "boundary_gate_id": "",
        "promotion_gate_id": "",
        "review_case_id": "",
        "reviewer_label": "manual_analysis_execution_reviewer",
        "note": "Create local review-only analysis result candidate.",
        "analysis_execution_mode": "local_review_only_candidate",
        "acknowledge_local_candidate_only": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_no_report_generation": True,
        "acknowledge_no_sandbox_or_public_event": True,
        "acknowledge_provider_output_is_evidence_not_truth": True,
        "acknowledge_not_official_verification": True,
        "acknowledge_not_full_web_coverage": True,
        "acknowledge_weak_evidence_warning": True,
        "acknowledge_rejected_exclusion": True,
        "acknowledge_dedup_no_risk_amplification": True,
    }
    payload.update(overrides)
    return payload


def report_generation_gate_payload(**overrides: object) -> dict:
    payload = {
        "manual_analysis_execution_id": "",
        "result_candidate_id": "",
        "boundary_gate_id": "",
        "review_case_id": "",
        "reviewer_label": "report_gate_reviewer",
        "note": "Create a local report generation gate record only.",
        "requested_future_output": "summary_report_candidate",
        "acknowledge_gate_only": True,
        "acknowledge_no_summary_report_generation": True,
        "acknowledge_no_b_end_report_generation": True,
        "acknowledge_no_export_generation": True,
        "acknowledge_no_sandbox_or_public_event": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_provider_output_is_evidence_not_truth": True,
        "acknowledge_not_official_verification": True,
        "acknowledge_not_full_web_coverage": True,
        "acknowledge_weak_evidence_warning": True,
        "acknowledge_rejected_exclusion": True,
        "acknowledge_dedup_no_risk_amplification": True,
        "acknowledge_audit_trace_required": True,
    }
    payload.update(overrides)
    return payload


def summary_report_candidate_payload(**overrides: object) -> dict:
    payload = {
        "report_gate_id": "",
        "result_candidate_id": "",
        "manual_analysis_execution_id": "",
        "boundary_gate_id": "",
        "review_case_id": "",
        "reviewer_label": "summary_candidate_reviewer",
        "note": "Create local Summary Report Candidate only.",
        "candidate_mode": "local_summary_report_candidate",
        "acknowledge_candidate_only": True,
        "acknowledge_not_final_summary_report": True,
        "acknowledge_no_b_end_report": True,
        "acknowledge_no_export_generation": True,
        "acknowledge_no_sandbox_or_public_event": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_provider_output_is_evidence_not_truth": True,
        "acknowledge_not_official_verification": True,
        "acknowledge_not_full_web_coverage": True,
        "acknowledge_weak_evidence_warning": True,
        "acknowledge_rejected_exclusion": True,
        "acknowledge_dedup_no_risk_amplification": True,
        "acknowledge_audit_trace_required": True,
    }
    payload.update(overrides)
    return payload


def final_summary_report_review_gate_payload(**overrides: object) -> dict:
    payload = {
        "summary_report_candidate_id": "",
        "report_gate_id": "",
        "result_candidate_id": "",
        "manual_analysis_execution_id": "",
        "boundary_gate_id": "",
        "review_case_id": "",
        "reviewer_label": "final_summary_reviewer",
        "note": "Review Summary Report Candidate for future final runtime only.",
        "review_decision": "approve_for_future_final_runtime",
        "required_revisions": [],
        "acknowledge_review_gate_only": True,
        "acknowledge_no_final_summary_report_generation": True,
        "acknowledge_no_b_end_report_generation": True,
        "acknowledge_no_export_generation": True,
        "acknowledge_no_sandbox_or_public_event": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_provider_output_is_evidence_not_truth": True,
        "acknowledge_not_official_verification": True,
        "acknowledge_not_full_web_coverage": True,
        "acknowledge_weak_evidence_warning": True,
        "acknowledge_rejected_exclusion": True,
        "acknowledge_dedup_no_risk_amplification": True,
        "acknowledge_audit_trace_required": True,
    }
    payload.update(overrides)
    return payload


def final_summary_report_payload(**overrides: object) -> dict:
    payload = {
        "summary_report_candidate_id": "",
        "final_report_review_gate_id": "",
        "report_gate_id": "",
        "result_candidate_id": "",
        "manual_analysis_execution_id": "",
        "boundary_gate_id": "",
        "review_case_id": "",
        "reviewer_label": "final_summary_report_reviewer",
        "note": "Create local Final Summary Report object only.",
        "acknowledge_local_final_summary_report_only": True,
        "acknowledge_no_pdf_export": True,
        "acknowledge_no_markdown_export": True,
        "acknowledge_no_deck_export": True,
        "acknowledge_no_b_end_report": True,
        "acknowledge_no_sandbox_or_public_event": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_provider_output_is_evidence_not_truth": True,
        "acknowledge_not_official_verification": True,
        "acknowledge_not_full_web_coverage": True,
        "acknowledge_weak_evidence_warning": True,
        "acknowledge_rejected_exclusion": True,
        "acknowledge_dedup_no_risk_amplification": True,
        "acknowledge_audit_trace_required": True,
    }
    payload.update(overrides)
    return payload


def final_summary_report_export_gate_payload(**overrides: object) -> dict:
    payload = {
        "final_summary_report_id": "",
        "final_summary_report_audit_id": "",
        "summary_report_candidate_id": "",
        "final_report_review_gate_id": "",
        "report_gate_id": "",
        "result_candidate_id": "",
        "manual_analysis_execution_id": "",
        "boundary_gate_id": "",
        "review_case_id": "",
        "reviewer_label": "final_summary_report_export_reviewer",
        "note": "Local Final Summary Report Export Gate only.",
        "export_decision": "approve_for_future_export_runtime",
        "required_revisions": [],
        "acknowledge_export_gate_only": True,
        "acknowledge_no_markdown_file_now": True,
        "acknowledge_no_pdf_file_now": True,
        "acknowledge_no_pptx_file_now": True,
        "acknowledge_no_b_end_report_generation": True,
        "acknowledge_no_sandbox_or_public_event": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_provider_output_is_evidence_not_truth": True,
        "acknowledge_not_official_verification": True,
        "acknowledge_not_full_web_coverage": True,
        "acknowledge_weak_evidence_warning": True,
        "acknowledge_rejected_exclusion": True,
        "acknowledge_dedup_no_risk_amplification": True,
        "acknowledge_audit_trace_required": True,
    }
    payload.update(overrides)
    return payload


def final_summary_report_export_artifact_payload(**overrides: object) -> dict:
    payload = {
        "final_summary_report_id": "",
        "export_gate_id": "",
        "export_gate_audit_id": "",
        "review_case_id": "",
        "artifact_type": "analyst_markdown",
        "reviewer_label": "final_summary_report_export_artifact_reviewer",
        "note": "Create local Final Summary Report export artifact only.",
        "acknowledge_export_artifact_only": True,
        "acknowledge_no_b_end_report": True,
        "acknowledge_no_sandbox_or_public_event": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_provider_output_is_evidence_not_truth": True,
        "acknowledge_not_official_verification": True,
        "acknowledge_not_full_web_coverage": True,
        "acknowledge_weak_evidence_warning": True,
        "acknowledge_rejected_exclusion": True,
        "acknowledge_dedup_no_risk_amplification": True,
        "acknowledge_audit_trace_required": True,
    }
    payload.update(overrides)
    return payload


def report_export_download_package_gate_payload(**overrides: object) -> dict:
    payload = {
        "export_artifact_id": "",
        "export_artifact_audit_id": "",
        "final_summary_report_id": "",
        "export_gate_id": "",
        "review_case_id": "",
        "reviewer_label": "report_export_download_package_reviewer",
        "note": "Record local download/package gate only.",
        "delivery_decision": "approve_for_future_download_package_runtime",
        "required_revisions": [],
        "acknowledge_download_package_gate_only": True,
        "acknowledge_no_download_route_now": True,
        "acknowledge_no_package_or_zip_now": True,
        "acknowledge_no_public_or_signed_url_now": True,
        "acknowledge_no_b_end_report": True,
        "acknowledge_no_sandbox_or_public_event": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_provider_output_is_evidence_not_truth": True,
        "acknowledge_not_official_verification": True,
        "acknowledge_not_full_web_coverage": True,
        "acknowledge_weak_evidence_warning": True,
        "acknowledge_rejected_exclusion": True,
        "acknowledge_dedup_no_risk_amplification": True,
        "acknowledge_audit_trace_required": True,
    }
    payload.update(overrides)
    return payload


def report_export_download_package_artifact_payload(**overrides: object) -> dict:
    payload = {
        "download_package_gate_id": "",
        "review_case_id": "",
        "package_mode": "local_manifest_only",
        "operator_label": "download_package_artifact_reviewer",
        "note": "Create a local manifest-only report export package artifact.",
        "acknowledge_local_manifest_only": True,
        "acknowledge_no_download_route": True,
        "acknowledge_no_file_bytes": True,
        "acknowledge_no_zip": True,
        "acknowledge_no_public_or_signed_url": True,
        "acknowledge_no_runtime_file_exposure": True,
        "acknowledge_no_artifact_content_read": True,
        "acknowledge_no_b_end_report": True,
        "acknowledge_no_sandbox_or_public_event": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_provider_output_is_evidence_not_truth": True,
        "acknowledge_not_official_verification": True,
        "acknowledge_not_full_web_coverage": True,
        "acknowledge_weak_evidence_warning": True,
        "acknowledge_rejected_exclusion": True,
        "acknowledge_dedup_no_risk_amplification": True,
        "acknowledge_audit_trace_required": True,
    }
    payload.update(overrides)
    return payload


def report_export_public_access_external_delivery_gate_payload(**overrides: object) -> dict:
    payload = {
        "package_artifact_id": "",
        "download_package_gate_id": "",
        "final_summary_report_id": "",
        "review_case_id": "",
        "reviewer_label": "public_access_delivery_reviewer",
        "note": "Create public access / external delivery gate record only.",
        "access_delivery_decision": "approve_for_future_public_access_external_delivery_runtime",
        "requested_future_access_modes": ["internal_handoff_future_candidate"],
        "requested_future_delivery_modes": ["internal_handoff_future_candidate"],
        "required_revisions": [],
        "acknowledge_gate_only": True,
        "acknowledge_no_public_download_route": True,
        "acknowledge_no_file_byte_response": True,
        "acknowledge_no_zip": True,
        "acknowledge_no_public_or_signed_url": True,
        "acknowledge_no_external_delivery": True,
        "acknowledge_no_email": True,
        "acknowledge_no_object_storage": True,
        "acknowledge_no_portal_publication": True,
        "acknowledge_no_runtime_file_exposure": True,
        "acknowledge_no_manifest_content_exposure": True,
        "acknowledge_no_export_artifact_content_read": True,
        "acknowledge_no_b_end_report": True,
        "acknowledge_no_sandbox_or_public_event": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_provider_output_is_evidence_not_truth": True,
        "acknowledge_not_official_verification": True,
        "acknowledge_not_full_web_coverage": True,
        "acknowledge_downstream_gates_required": True,
    }
    payload.update(overrides)
    return payload


def create_review_queue_ready_chain(tmp_path: Path, request_id: str, *, package_dir: Path | None = None):
    if package_dir is None:
        package_dir = create_real_preview_package(tmp_path)
    create_real_preview_ready_chain(tmp_path, request_id, package_dir)
    preview = create_real_package_row_preview(request_id, real_preview_ack_payload())
    review_case = create_review_only_case(request_id)
    staging_import = create_review_only_case_staging_import(
        request_id,
        staging_import_ack_payload(review_case_id=review_case.review_case_id, preview_run_id=preview.preview_run_id),
    )
    queue_init = create_review_queue_initialization(
        request_id,
        review_queue_init_ack_payload(
            review_case_id=review_case.review_case_id,
            staging_import_id=staging_import.staging_import_id,
        ),
    )
    item_batch = read_review_queue_item_batch(request_id, queue_init.queue_init_id)
    return review_case, staging_import, queue_init, item_batch


def create_dedup_preview_ready_chain(tmp_path: Path, request_id: str):
    package_dir = create_many_row_preview_package(tmp_path)
    review_case, staging_import, queue_init, item_batch = create_review_queue_ready_chain(tmp_path, request_id, package_dir=package_dir)
    item_ids = [item.review_item_id for item in item_batch.items]
    for item_id in item_ids:
        create_review_queue_item_action(request_id, item_id, review_queue_action_payload("approve"))
    batch_path = tmp_path / "review_queue_items" / f"{request_id}_{queue_init.queue_init_id}.json"
    batch_payload = json.loads(batch_path.read_text(encoding="utf-8"))
    batch_payload["items"][0]["evidence_candidate"]["source_url"] = "https://example.com/dedup?id=1&utm_source=demo"
    batch_payload["items"][0]["evidence_candidate"]["title_preview"] = "Duplicate candidate alpha"
    batch_payload["items"][0]["evidence_candidate"]["body_text_preview"] = "Same preview text."
    batch_payload["items"][1]["evidence_candidate"]["source_url"] = "https://example.com/dedup?id=1"
    batch_payload["items"][1]["evidence_candidate"]["title_preview"] = "Duplicate candidate alpha"
    batch_payload["items"][1]["evidence_candidate"]["body_text_preview"] = "Same preview text."
    batch_path.write_text(json.dumps(batch_payload), encoding="utf-8")
    gate = create_review_queue_completion_gate(
        request_id,
        review_queue_completion_gate_payload(queue_init_id=queue_init.queue_init_id, review_case_id=queue_init.review_case_id),
    )
    preview = create_dedup_preview(
        request_id,
        dedup_preview_payload(
            review_case_id=queue_init.review_case_id,
            queue_init_id=queue_init.queue_init_id,
            completion_gate_id=gate.completion_gate_id,
        ),
    )
    assert preview.groups
    return review_case, staging_import, queue_init, item_batch, gate, preview, preview.groups[0]


def create_real_preview_ready_chain(tmp_path: Path, request_id: str, package_dir: Path) -> dict:
    preflight_payload = create_execution_preflight(tmp_path, request_id, package_dir=package_dir)
    create_evidence_row_reader_dry_run(
        request_id,
        {"preflight_id": preflight_payload["preflight_id"], "fixture_name": "safe_evidence_items", "max_rows": 20},
    )
    return preflight_payload


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


def test_real_package_row_preview_reads_limited_local_package_with_redaction_only(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Real package preview safe"))
    )
    package_dir = create_real_preview_package(tmp_path)
    preflight_payload = create_real_preview_ready_chain(tmp_path, record.request_id, package_dir)

    preview = create_real_package_row_preview(record.request_id, real_preview_ack_payload())
    second_preview = create_real_package_row_preview(record.request_id, real_preview_ack_payload(max_rows=1))
    preview_files = sorted((tmp_path / "real_package_row_previews").glob(f"{record.request_id}_*.json"))
    read_back = read_real_package_row_preview(record.request_id, preview.preview_run_id)

    assert preview.schema_ == "sentigraph_real_package_row_preview_v1"
    assert preview.preflight_id == preflight_payload["preflight_id"]
    assert preview.execution_mode == "real_package_row_preview_only"
    assert preview.status == "passed"
    assert preview.package_reference.package_name == package_dir.name
    assert preview.package_reference.package_role == "selected_public_sample"
    assert preview.limits.max_rows == 10
    assert preview.limits.hard_max_rows == 20
    assert preview.limits.full_scan is False
    assert preview.limits.import_rows is False
    assert preview.rows.rows_seen == 2
    assert preview.rows.accepted_for_preview == 2
    assert preview.rows.quarantined == 0
    assert preview.rows.rejected == 0
    assert len(preview.redacted_preview_rows) == 2
    assert len(preview.redacted_preview_rows[0].evidence_candidate.body_text_preview) <= 160
    assert preview.now_flags.import_evidence_rows_now is False
    assert preview.now_flags.write_evidence_layer_now is False
    assert preview.now_flags.create_case_now is False
    assert preview.now_flags.run_analysis_now is False
    assert preview.readiness.can_import_now is False
    assert second_preview.preview_run_id != preview.preview_run_id
    assert second_preview.rows.rows_seen == 1
    assert len(preview_files) == 2
    assert len(list_real_package_row_previews(record.request_id)) == 2
    assert read_back.preview_run_id == preview.preview_run_id
    assert not (tmp_path / "cases").exists()


def test_real_package_row_preview_quarantines_rejects_and_privacy_stops_without_raw_values(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Real package preview mixed"))
    )
    package_dir = create_real_preview_package(tmp_path, mixed=True)
    create_real_preview_ready_chain(tmp_path, record.request_id, package_dir)

    preview = create_real_package_row_preview(record.request_id, real_preview_ack_payload(max_rows=10))
    text = json.dumps(preview.model_dump(mode="json", by_alias=True), ensure_ascii=False)

    assert preview.status == "privacy_stop"
    assert preview.rows.rows_seen == 4
    assert preview.rows.accepted_for_preview == 1
    assert preview.rows.quarantined == 1
    assert preview.rows.rejected == 1
    assert preview.rows.privacy_stop_at_row == 4
    assert preview.privacy_scan.raw_author_id_detected == 1
    assert preview.privacy_scan.raw_author_name_detected == 1
    assert preview.privacy_scan.profile_url_detected == 1
    assert preview.privacy_scan.private_message_detected == 1
    assert preview.privacy_scan.privacy_stop_triggered is True
    assert preview.readiness.state == "privacy_stop"
    assert "real-preview-user-should-not-return" not in text
    assert "Real Preview Name Should Not Return" not in text
    assert "example.test/profile/real-preview" not in text
    assert "Real preview private message should not return" not in text


def test_real_package_row_preview_blocks_unsafe_inputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Real package preview blocks"))
    )
    package_dir = create_real_preview_package(tmp_path)
    preflight_payload = create_execution_preflight(tmp_path, record.request_id, package_dir=package_dir)

    cases = [
        ("No synthetic dry-run", real_preview_ack_payload(), "synthetic row reader"),
        ("Too many rows", real_preview_ack_payload(max_rows=21), "max_rows"),
        ("Missing acknowledgement", real_preview_ack_payload(acknowledge_no_import=False), "acknowledgement"),
    ]
    for _title, payload, expected_message in cases:
        try:
            create_real_package_row_preview(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{_title} should block real package row preview")

    create_evidence_row_reader_dry_run(
        record.request_id,
        {"preflight_id": preflight_payload["preflight_id"], "fixture_name": "safe_evidence_items", "max_rows": 20},
    )
    reject_decision = create_evidence_import_review_decision(
        record.request_id,
        review_payload("reject_import", notes="Supersede approve before preview."),
    )
    assert reject_decision.decision == "reject_import"
    try:
        create_real_package_row_preview(record.request_id, real_preview_ack_payload())
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "approve_import" in str(exc)
    else:
        raise AssertionError("Latest non-approve review decision should block real package row preview")


def test_real_package_row_preview_blocks_missing_or_unsafe_package_files(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Real package preview missing files"))
    )
    package_dir = create_real_preview_package(tmp_path, include_rows=False)
    create_real_preview_ready_chain(tmp_path, record.request_id, package_dir)

    try:
        create_real_package_row_preview(record.request_id, real_preview_ack_payload())
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "evidence_items.jsonl" in str(exc)
    else:
        raise AssertionError("Missing evidence_items.jsonl should block real package row preview")


def test_review_only_case_creates_internal_container_after_safe_preview(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Review-only case safe"))
    )
    package_dir = create_real_preview_package(tmp_path)
    create_real_preview_ready_chain(tmp_path, record.request_id, package_dir)
    preview = create_real_package_row_preview(record.request_id, real_preview_ack_payload())

    review_case = create_review_only_case(
        record.request_id,
        {"source_preview_run_id": preview.preview_run_id, "target_case_mode": "new_review_case"},
    )
    read_back = read_review_only_case(record.request_id, review_case.review_case_id)
    cases = list_review_only_cases(record.request_id)
    payload_text = json.dumps(review_case.model_dump(mode="json", by_alias=True), ensure_ascii=False)

    assert review_case.schema_ == "sentigraph_review_only_case_v1"
    assert review_case.request_id == record.request_id
    assert review_case.source_preview_run_id == preview.preview_run_id
    assert review_case.source_import_job_id == preview.import_job_id
    assert review_case.source_preflight_id == preview.preflight_id
    assert review_case.status == "staging_pending"
    assert review_case.visibility == "internal_review_only"
    assert review_case.analysis_included is False
    assert review_case.public_visible is False
    assert review_case.report_allowed is False
    assert review_case.sandbox_allowed is False
    assert review_case.strategy_lab_allowed is False
    assert review_case.production_case_created is False
    assert review_case.evidence_rows_imported is False
    assert review_case.evidence_layer_written is False
    assert review_case.review_queue_created is False
    assert review_case.dedup_run is False
    assert review_case.analysis_run is False
    assert review_case.package_reference.package_name == package_dir.name
    assert review_case.source_preview_summary.accepted_for_preview == 2
    assert review_case.source_preview_summary.privacy_stop_triggered is False
    assert review_case.coverage.not_full_web is True
    assert review_case.coverage.not_full_platform is True
    assert review_case.coverage.not_full_thread is True
    assert review_case.governance_defaults.review_status == "review_needed"
    assert review_case.governance_defaults.verification_status == "source_url_provided_unverified"
    assert review_case.governance_defaults.trust_label == "medium_low"
    assert review_case.governance_defaults.analysis_included is False
    assert review_case.target_case_reference.mode == "new_review_case"
    assert review_case.target_case_reference.attach_to_production_case_now is False
    assert review_case.readiness.can_import_rows_now is False
    assert review_case.readiness.can_run_analysis_now is False
    assert review_case.readiness.can_generate_report_now is False
    assert review_case.readiness.requires_future_staging_import_phase is True
    assert "run analysis now" in review_case.blocked_actions
    assert "future staging import completed" in review_case.promotion_requirements
    assert "provider output is evidence, not truth" in " ".join(review_case.boundary_notes).lower()
    assert read_back.review_case_id == review_case.review_case_id
    assert len(cases) == 1
    assert not (tmp_path / "cases").exists()
    assert "real-preview-user-should-not-return" not in payload_text


def test_review_only_case_blocks_privacy_stop_and_latest_non_approve_decision(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Review-only case blocked"))
    )
    package_dir = create_real_preview_package(tmp_path, mixed=True)
    create_real_preview_ready_chain(tmp_path, record.request_id, package_dir)
    preview = create_real_package_row_preview(record.request_id, real_preview_ack_payload())

    try:
        create_review_only_case(record.request_id, {"source_preview_run_id": preview.preview_run_id})
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "privacy_stop" in str(exc)
    else:
        raise AssertionError("privacy_stop preview should block review-only case creation")

    safe_record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Review-only case stale decision"))
    )
    safe_package_dir = create_real_preview_package(tmp_path / "safe")
    create_real_preview_ready_chain(tmp_path, safe_record.request_id, safe_package_dir)
    safe_preview = create_real_package_row_preview(safe_record.request_id, real_preview_ack_payload())
    create_evidence_import_review_decision(
        safe_record.request_id,
        review_payload("request_more_source", notes="Supersede approve before review-only case."),
    )

    try:
        create_review_only_case(safe_record.request_id, {"source_preview_run_id": safe_preview.preview_run_id})
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "approve_import" in str(exc)
    else:
        raise AssertionError("latest non-approve decision should block review-only case creation")


def test_review_only_case_blocks_invalid_target_and_requested_side_effects(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Review-only target blocks"))
    )
    package_dir = create_real_preview_package(tmp_path)
    create_real_preview_ready_chain(tmp_path, record.request_id, package_dir)
    preview = create_real_package_row_preview(record.request_id, real_preview_ack_payload())

    cases = [
        ({"source_preview_run_id": preview.preview_run_id, "target_case_mode": "production_case"}, "target_case_mode"),
        ({"source_preview_run_id": preview.preview_run_id, "target_case_mode": "existing_case_review_wrapper"}, "target_case_id"),
        ({"source_preview_run_id": preview.preview_run_id, "analysis_included": True}, "analysis_included"),
        ({"source_preview_run_id": preview.preview_run_id, "production_case_created": True}, "production_case_created"),
        ({"source_preview_run_id": preview.preview_run_id, "evidence_rows_imported": True}, "evidence_rows_imported"),
    ]
    for payload, expected_message in cases:
        try:
            create_review_only_case(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{expected_message} should block review-only case creation")

    wrapper = create_review_only_case(
        record.request_id,
        {
            "source_preview_run_id": preview.preview_run_id,
            "target_case_mode": "existing_case_review_wrapper",
            "target_case_id": "case_existing_review_target",
        },
    )
    assert wrapper.target_case_reference.mode == "existing_case_review_wrapper"
    assert wrapper.target_case_reference.target_case_id == "case_existing_review_target"
    assert wrapper.production_case_created is False
    assert wrapper.evidence_rows_imported is False


def test_review_only_staging_import_creates_candidates_from_redacted_preview_only(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Review-only staging safe"))
    )
    package_dir = create_real_preview_package(tmp_path)
    create_real_preview_ready_chain(tmp_path, record.request_id, package_dir)
    preview = create_real_package_row_preview(record.request_id, real_preview_ack_payload())
    (package_dir / "evidence_items.jsonl").write_text(
        '{"raw_author_id":"must_not_be_opened_after_preview","body_text":"unsafe raw package row"}\n',
        encoding="utf-8",
    )
    review_case = create_review_only_case(
        record.request_id,
        {"source_preview_run_id": preview.preview_run_id, "target_case_mode": "new_review_case"},
    )

    staging_import = create_review_only_case_staging_import(
        record.request_id,
        staging_import_ack_payload(
            review_case_id=review_case.review_case_id,
            preview_run_id=preview.preview_run_id,
        ),
    )
    read_back = read_review_only_case_staging_import(record.request_id, staging_import.staging_import_id)
    imports = list_review_only_case_staging_imports(record.request_id)
    batch = read_staged_evidence_candidate_batch(record.request_id, staging_import.staging_import_id)
    payload_text = json.dumps(batch.model_dump(mode="json", by_alias=True), ensure_ascii=False)

    assert staging_import.schema_ == "sentigraph_review_only_case_staging_import_v1"
    assert staging_import.execution_mode == "review_only_redacted_preview_staging"
    assert staging_import.status == "completed"
    assert staging_import.review_case_id == review_case.review_case_id
    assert staging_import.source_preview_run_id == preview.preview_run_id
    assert staging_import.source_import_job_id == preview.import_job_id
    assert staging_import.limits.source == "limited_real_package_row_preview"
    assert staging_import.limits.max_rows_from_preview == 20
    assert staging_import.limits.full_scan is False
    assert staging_import.limits.read_package_rows_now is False
    assert staging_import.limits.analysis_inclusion is False
    assert staging_import.limits.public_visibility is False
    assert staging_import.counts.preview_rows_seen == 2
    assert staging_import.counts.accepted_for_staging == 2
    assert staging_import.counts.quarantined_from_staging == 0
    assert staging_import.counts.rejected_from_staging == 0
    assert staging_import.counts.privacy_stop is False
    assert staging_import.default_governance.review_status == "review_needed"
    assert staging_import.default_governance.verification_status == "source_url_provided_unverified"
    assert staging_import.default_governance.trust_label == "medium_low"
    assert staging_import.default_governance.analysis_included is False
    assert staging_import.default_governance.public_visible is False
    assert staging_import.default_governance.report_visible is False
    assert staging_import.default_governance.sandbox_visible is False
    assert staging_import.target.production_case_id is None
    assert staging_import.target.production_case_created is False
    assert staging_import.target.evidence_layer_written is False
    assert staging_import.rollback.rollback_available is True
    assert staging_import.readiness.state == "staged_for_review_only"
    assert staging_import.readiness.can_run_analysis_now is False
    assert staging_import.readiness.can_generate_report_now is False
    assert staging_import.readiness.requires_review_queue_phase is True
    assert read_back.staging_import_id == staging_import.staging_import_id
    assert [item.staging_import_id for item in imports] == [staging_import.staging_import_id]

    assert batch.schema_ == "sentigraph_staged_evidence_candidate_batch_v1"
    assert batch.staging_import_id == staging_import.staging_import_id
    assert len(batch.candidates) == 2
    assert batch.candidates[0].schema_ == "sentigraph_staged_evidence_candidate_v1"
    assert batch.candidates[0].source_preview_row_index == preview.redacted_preview_rows[0].row_index
    assert batch.candidates[0].evidence_candidate.title_preview == "Safe local package row"
    assert batch.candidates[0].governance.review_status == "review_needed"
    assert batch.candidates[0].governance.verification_status == "source_url_provided_unverified"
    assert batch.candidates[0].governance.trust_label == "medium_low"
    assert batch.candidates[0].governance.analysis_included is False
    assert batch.candidates[0].governance.public_visible is False
    assert batch.candidates[0].governance.report_visible is False
    assert batch.candidates[0].governance.sandbox_visible is False
    assert batch.candidates[0].privacy.from_redacted_preview is True
    assert batch.candidates[0].privacy.raw_author_id_present is False
    assert batch.candidates[0].privacy.raw_author_name_present is False
    assert batch.candidates[0].privacy.profile_url_present is False
    assert batch.candidates[0].privacy.private_message_present is False
    assert batch.candidates[0].privacy.passed is True
    assert batch.candidates[0].dedup.computed_now is False
    assert batch.candidates[0].dedup.required_before_analysis is True
    assert batch.candidates[0].dedup.content_hash is None
    assert "must_not_be_opened_after_preview" not in payload_text
    assert "real-preview-user-should-not-return" not in payload_text
    assert "Real Preview Name Should Not Return" not in payload_text
    assert "example.test/profile/real-preview" not in payload_text
    assert "Real preview private message should not return" not in payload_text
    assert not (tmp_path / "cases").exists()


def test_review_only_staging_import_blocks_unsafe_inputs_and_duplicate_import(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Review-only staging blocks"))
    )
    package_dir = create_real_preview_package(tmp_path)
    create_real_preview_ready_chain(tmp_path, record.request_id, package_dir)
    preview = create_real_package_row_preview(record.request_id, real_preview_ack_payload())
    review_case = create_review_only_case(record.request_id, {"source_preview_run_id": preview.preview_run_id})

    cases = [
        (staging_import_ack_payload(acknowledge_no_analysis=False), "acknowledgement"),
        (staging_import_ack_payload(package_path=str(package_dir / "evidence_items.jsonl")), "package_path"),
        (staging_import_ack_payload(write_evidence_layer_now=True), "side effect"),
        (staging_import_ack_payload(target_production_case_id="case_prod_unsafe"), "production_case_id"),
        (
            staging_import_ack_payload(
                review_case_id=review_case.review_case_id,
                preview_run_id="real_package_row_preview_missing",
            ),
            "row preview",
        ),
    ]
    for payload, expected_message in cases:
        try:
            create_review_only_case_staging_import(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{expected_message} should block staging import")

    first = create_review_only_case_staging_import(
        record.request_id,
        staging_import_ack_payload(review_case_id=review_case.review_case_id),
    )
    try:
        create_review_only_case_staging_import(
            record.request_id,
            staging_import_ack_payload(review_case_id=review_case.review_case_id),
        )
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "already has staging import" in str(exc)
    else:
        raise AssertionError("Duplicate staging import should be blocked")
    assert len(list_review_only_case_staging_imports(record.request_id)) == 1
    assert first.staging_import_id


def test_review_only_staging_import_blocks_privacy_stop_and_latest_non_approve_decision(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Staging latest decision blocks"))
    )
    package_dir = create_real_preview_package(tmp_path)
    create_real_preview_ready_chain(tmp_path, record.request_id, package_dir)
    preview = create_real_package_row_preview(record.request_id, real_preview_ack_payload())
    review_case = create_review_only_case(record.request_id, {"source_preview_run_id": preview.preview_run_id})
    create_evidence_import_review_decision(
        record.request_id,
        review_payload("hold_for_privacy_review", notes="Supersede approve before staging."),
    )

    try:
        create_review_only_case_staging_import(
            record.request_id,
            staging_import_ack_payload(review_case_id=review_case.review_case_id),
        )
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "approve_import" in str(exc)
    else:
        raise AssertionError("Latest non-approve review decision should block staging import")

    privacy_record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Staging privacy stop blocks"))
    )
    privacy_package = create_real_preview_package(tmp_path / "privacy", mixed=True)
    create_real_preview_ready_chain(tmp_path, privacy_record.request_id, privacy_package)
    privacy_preview = create_real_package_row_preview(privacy_record.request_id, real_preview_ack_payload())
    assert privacy_preview.status == "privacy_stop"
    unsafe_case_path = tmp_path / "review_only_cases" / f"{privacy_record.request_id}_review_only_case_unsafe.json"
    unsafe_case_path.write_text(
        json.dumps(
            {
                "schema": "sentigraph_review_only_case_v1",
                "review_case_id": "review_only_case_unsafe",
                "request_id": privacy_record.request_id,
                "source_import_job_id": privacy_preview.import_job_id,
                "source_preview_run_id": privacy_preview.preview_run_id,
                "source_preflight_id": privacy_preview.preflight_id,
                "status": "staging_pending",
            }
        ),
        encoding="utf-8",
    )
    try:
        create_review_only_case_staging_import(
            privacy_record.request_id,
            staging_import_ack_payload(review_case_id="review_only_case_unsafe"),
        )
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "privacy_stop" in str(exc)
    else:
        raise AssertionError("privacy_stop preview should block staging import")


def test_review_queue_initialization_creates_items_from_staged_candidates_only(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Review queue init safe"))
    )
    package_dir = create_real_preview_package(tmp_path)
    create_real_preview_ready_chain(tmp_path, record.request_id, package_dir)
    preview = create_real_package_row_preview(record.request_id, real_preview_ack_payload())
    (package_dir / "evidence_items.jsonl").write_text(
        '{"raw_author_id":"must_not_be_opened_for_queue","body_text":"unsafe raw package row"}\n',
        encoding="utf-8",
    )
    review_case = create_review_only_case(record.request_id, {"source_preview_run_id": preview.preview_run_id})
    staging_import = create_review_only_case_staging_import(
        record.request_id,
        staging_import_ack_payload(review_case_id=review_case.review_case_id),
    )

    queue_init = create_review_queue_initialization(
        record.request_id,
        review_queue_init_ack_payload(
            review_case_id=review_case.review_case_id,
            staging_import_id=staging_import.staging_import_id,
        ),
    )
    read_back = read_review_queue_initialization(record.request_id, queue_init.queue_init_id)
    inits = list_review_queue_initializations(record.request_id)
    item_batch = read_review_queue_item_batch(record.request_id, queue_init.queue_init_id)
    payload_text = json.dumps(item_batch.model_dump(mode="json", by_alias=True), ensure_ascii=False)

    assert queue_init.schema_ == "sentigraph_review_queue_initialization_v1"
    assert queue_init.execution_mode == "review_only_queue_initialization"
    assert queue_init.status == "completed"
    assert queue_init.review_case_id == review_case.review_case_id
    assert queue_init.staging_import_id == staging_import.staging_import_id
    assert queue_init.source.source_type == "staged_evidence_candidates"
    assert queue_init.source.candidate_batch_schema == "sentigraph_staged_evidence_candidate_batch_v1"
    assert queue_init.counts.staged_candidates_seen == 2
    assert queue_init.counts.queue_items_created == 2
    assert queue_init.counts.excluded_candidates == 0
    assert queue_init.counts.privacy_hold_items == 0
    assert queue_init.defaults.queue_status == "review_needed"
    assert queue_init.defaults.review_status == "review_needed"
    assert queue_init.defaults.verification_status == "source_url_provided_unverified"
    assert queue_init.defaults.trust_label == "medium_low"
    assert queue_init.defaults.analysis_included is False
    assert queue_init.defaults.public_visible is False
    assert queue_init.defaults.report_visible is False
    assert queue_init.defaults.sandbox_visible is False
    assert queue_init.defaults.dedup_required is True
    assert queue_init.target.production_case_id is None
    assert queue_init.target.production_case_created is False
    assert queue_init.target.evidence_layer_written is False
    assert queue_init.target.production_review_queue_created is False
    assert queue_init.readiness.state == "review_queue_initialized"
    assert queue_init.readiness.can_run_analysis_now is False
    assert queue_init.readiness.can_generate_report_now is False
    assert queue_init.readiness.requires_review_actions_phase is True
    assert queue_init.readiness.requires_dedup_phase is True
    assert read_back.queue_init_id == queue_init.queue_init_id
    assert [item.queue_init_id for item in inits] == [queue_init.queue_init_id]

    assert item_batch.schema_ == "sentigraph_review_queue_item_batch_v1"
    assert item_batch.queue_init_id == queue_init.queue_init_id
    assert len(item_batch.items) == 2
    first_item = item_batch.items[0]
    assert first_item.schema_ == "sentigraph_review_queue_item_v1"
    assert first_item.queue_init_id == queue_init.queue_init_id
    assert first_item.staging_id
    assert first_item.queue_status == "review_needed"
    assert first_item.evidence_candidate.title_preview == "Safe local package row"
    assert first_item.governance.review_status == "review_needed"
    assert first_item.governance.verification_status == "source_url_provided_unverified"
    assert first_item.governance.trust_label == "medium_low"
    assert first_item.governance.analysis_included is False
    assert first_item.governance.public_visible is False
    assert first_item.governance.report_visible is False
    assert first_item.governance.sandbox_visible is False
    assert first_item.privacy.raw_author_id_present is False
    assert first_item.privacy.raw_author_name_present is False
    assert first_item.privacy.profile_url_present is False
    assert first_item.privacy.private_message_present is False
    assert first_item.privacy.passed is True
    assert first_item.dedup.dedup_status == "not_run"
    assert first_item.dedup.duplicate_group_id is None
    assert first_item.dedup.duplicate_count == 1
    assert first_item.dedup.may_amplify_risk is False
    assert first_item.audit.source == "review_queue_initialization"
    assert "must_not_be_opened_for_queue" not in payload_text
    assert "real-preview-user-should-not-return" not in payload_text
    assert "Real Preview Name Should Not Return" not in payload_text
    assert "example.test/profile/real-preview" not in payload_text
    assert "Real preview private message should not return" not in payload_text
    assert not (tmp_path / "cases").exists()


def test_review_queue_initialization_blocks_unsafe_inputs_and_duplicate_init(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Review queue init blocks"))
    )
    package_dir = create_real_preview_package(tmp_path)
    create_real_preview_ready_chain(tmp_path, record.request_id, package_dir)
    preview = create_real_package_row_preview(record.request_id, real_preview_ack_payload())
    review_case = create_review_only_case(record.request_id, {"source_preview_run_id": preview.preview_run_id})
    staging_import = create_review_only_case_staging_import(
        record.request_id,
        staging_import_ack_payload(review_case_id=review_case.review_case_id),
    )

    cases = [
        (review_queue_init_ack_payload(acknowledge_no_dedup=False), "acknowledgement"),
        (review_queue_init_ack_payload(package_path=str(package_dir / "evidence_items.jsonl")), "package_path"),
        (review_queue_init_ack_payload(target_production_case_id="case_prod_unsafe"), "production_case_id"),
        (review_queue_init_ack_payload(analysis_included=True), "side effect"),
        (review_queue_init_ack_payload(dedup_run=True), "side effect"),
        (
            review_queue_init_ack_payload(
                review_case_id=review_case.review_case_id,
                staging_import_id="review_only_staging_import_missing",
            ),
            "staging import",
        ),
    ]
    for payload, expected_message in cases:
        try:
            create_review_queue_initialization(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected_message in str(exc)
        else:
            raise AssertionError(f"{expected_message} should block queue initialization")

    first = create_review_queue_initialization(
        record.request_id,
        review_queue_init_ack_payload(
            review_case_id=review_case.review_case_id,
            staging_import_id=staging_import.staging_import_id,
        ),
    )
    try:
        create_review_queue_initialization(
            record.request_id,
            review_queue_init_ack_payload(
                review_case_id=review_case.review_case_id,
                staging_import_id=staging_import.staging_import_id,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "already has review queue initialization" in str(exc)
    else:
        raise AssertionError("Duplicate review queue initialization should be blocked")
    assert len(list_review_queue_initializations(record.request_id)) == 1
    assert first.queue_init_id


def test_review_queue_initialization_blocks_non_approve_decision_and_forbidden_candidate(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Review queue decision blocks"))
    )
    package_dir = create_real_preview_package(tmp_path)
    create_real_preview_ready_chain(tmp_path, record.request_id, package_dir)
    preview = create_real_package_row_preview(record.request_id, real_preview_ack_payload())
    review_case = create_review_only_case(record.request_id, {"source_preview_run_id": preview.preview_run_id})
    staging_import = create_review_only_case_staging_import(
        record.request_id,
        staging_import_ack_payload(review_case_id=review_case.review_case_id),
    )
    create_evidence_import_review_decision(
        record.request_id,
        review_payload("request_more_source", notes="Supersede approve before queue init."),
    )

    try:
        create_review_queue_initialization(
            record.request_id,
            review_queue_init_ack_payload(
                review_case_id=review_case.review_case_id,
                staging_import_id=staging_import.staging_import_id,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "approve_import" in str(exc)
    else:
        raise AssertionError("Latest non-approve review decision should block queue initialization")

    unsafe_record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Review queue forbidden candidate blocks"))
    )
    unsafe_package = create_real_preview_package(tmp_path / "unsafe_queue")
    create_real_preview_ready_chain(tmp_path, unsafe_record.request_id, unsafe_package)
    unsafe_preview = create_real_package_row_preview(unsafe_record.request_id, real_preview_ack_payload())
    unsafe_case = create_review_only_case(unsafe_record.request_id, {"source_preview_run_id": unsafe_preview.preview_run_id})
    unsafe_staging = create_review_only_case_staging_import(
        unsafe_record.request_id,
        staging_import_ack_payload(review_case_id=unsafe_case.review_case_id),
    )
    batch_path = tmp_path / "staged_evidence_candidates" / f"{unsafe_record.request_id}_{unsafe_staging.staging_import_id}.json"
    batch_payload = json.loads(batch_path.read_text(encoding="utf-8"))
    batch_payload["candidates"][0]["privacy"]["raw_author_id_present"] = True
    batch_path.write_text(json.dumps(batch_payload), encoding="utf-8")

    try:
        create_review_queue_initialization(
            unsafe_record.request_id,
            review_queue_init_ack_payload(
                review_case_id=unsafe_case.review_case_id,
                staging_import_id=unsafe_staging.staging_import_id,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "forbidden" in str(exc) or "raw_author" in str(exc)
    else:
        raise AssertionError("Forbidden candidate privacy flag should block queue initialization")


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


def test_review_queue_action_approve_updates_local_item_and_appends_audit(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Review queue action approve")))
    _review_case, _staging_import, queue_init, item_batch = create_review_queue_ready_chain(tmp_path, record.request_id)
    review_item_id = item_batch.items[0].review_item_id

    result = create_review_queue_item_action(record.request_id, review_item_id, review_queue_action_payload("approve"))
    updated_batch = read_review_queue_item_batch(record.request_id, queue_init.queue_init_id)
    updated_item = [item for item in updated_batch.items if item.review_item_id == review_item_id][0]
    audits = read_review_queue_action_audits_for_item(record.request_id, review_item_id)

    assert result.schema_ == "sentigraph_review_queue_action_result_v1"
    assert result.action == "approve"
    assert result.previous_status == "review_needed"
    assert result.new_status == "approved"
    assert updated_item.queue_status == "approved"
    assert updated_item.governance.review_status == "approved"
    assert updated_item.governance.analysis_included is False
    assert updated_item.governance.public_visible is False
    assert updated_item.governance.report_visible is False
    assert updated_item.governance.sandbox_visible is False
    assert updated_item.governance.trust_label == "medium_low"
    assert updated_item.dedup.dedup_status == "not_run"
    assert updated_item.dedup.may_amplify_risk is False
    assert result.now_flags["run_analysis_now"] is False
    assert result.now_flags["run_dedup_now"] is False
    assert result.readiness["can_run_analysis_now"] is False
    assert len(audits) == 1
    assert audits[0].analysis_effect == "eligible_for_future_dedup"
    assert audits[0].safe_mode["no_url_fetch"] is True
    assert audits[0].safe_mode["no_secret_exposed"] is True


def test_review_queue_actions_append_audit_and_preserve_exclusion(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Review queue action statuses")))
    _review_case, _staging_import, queue_init, item_batch = create_review_queue_ready_chain(tmp_path, record.request_id)
    first_item_id = item_batch.items[0].review_item_id
    second_item_id = item_batch.items[1].review_item_id

    reject_result = create_review_queue_item_action(record.request_id, first_item_id, review_queue_action_payload("reject", note="Reject this weak source."))
    reset_result = create_review_queue_item_action(record.request_id, first_item_id, review_queue_action_payload("reset_review", note="Reset for second pass."))
    weak_result = create_review_queue_item_action(record.request_id, first_item_id, review_queue_action_payload("mark_weak", note="Keep as weak evidence."))
    source_result = create_review_queue_item_action(record.request_id, first_item_id, review_queue_action_payload("request_more_source", note="Need source context."))
    hold_result = create_review_queue_item_action(record.request_id, first_item_id, review_queue_action_payload("hold_for_privacy_review", note="Privacy hold until reviewer checks."))
    duplicate_result = create_review_queue_item_action(
        record.request_id,
        second_item_id,
        review_queue_action_payload(
            "merge_duplicate",
            note="Likely duplicate cluster.",
            duplicate_group_id="dup_group_demo",
            duplicate_of_review_item_id=first_item_id,
        ),
    )

    updated_batch = read_review_queue_item_batch(record.request_id, queue_init.queue_init_id)
    item_map = {item.review_item_id: item for item in updated_batch.items}
    first_audits = read_review_queue_action_audits_for_item(record.request_id, first_item_id)
    all_audits = list_review_queue_action_audits(record.request_id)

    assert reject_result.new_status == "rejected"
    assert reset_result.previous_status == "rejected"
    assert reset_result.new_status == "review_needed"
    assert weak_result.new_status == "marked_weak"
    assert source_result.new_status == "needs_more_source"
    assert hold_result.new_status == "privacy_hold"
    assert duplicate_result.new_status == "duplicate_merged"
    assert item_map[first_item_id].queue_status == "privacy_hold"
    assert item_map[first_item_id].governance.analysis_included is False
    assert item_map[first_item_id].governance.trust_label == "medium_low"
    assert item_map[second_item_id].queue_status == "duplicate_merged"
    assert item_map[second_item_id].dedup.dedup_status == "duplicate_candidate_marked"
    assert item_map[second_item_id].dedup.duplicate_group_id == "dup_group_demo"
    assert item_map[second_item_id].dedup.may_amplify_risk is False
    assert [audit.action for audit in first_audits] == [
        "reject",
        "reset_review",
        "mark_weak",
        "request_more_source",
        "hold_for_privacy_review",
    ]
    assert len(all_audits) == 6


def test_review_queue_action_blocks_unsafe_payloads_and_transitions(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Review queue action blocks")))
    _review_case, _staging_import, queue_init, item_batch = create_review_queue_ready_chain(tmp_path, record.request_id)
    review_item_id = item_batch.items[0].review_item_id

    unsafe_cases = [
        (review_queue_action_payload("approve", reviewer_label=""), "reviewer_label"),
        (review_queue_action_payload("approve", acknowledge_no_analysis=False), "acknowledgement"),
        (review_queue_action_payload("approve", analysis_included=True), "side effect"),
        (review_queue_action_payload("approve", trust_label="high"), "trust_label"),
        (review_queue_action_payload("approve", verification_status="verified_by_official_api"), "verification"),
        (review_queue_action_payload("approve", production_case_id="case_prod_unsafe"), "production_case_id"),
        (review_queue_action_payload("reset_review"), "transition"),
    ]
    for payload, expected in unsafe_cases:
        try:
            create_review_queue_item_action(record.request_id, review_item_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected in str(exc)
        else:
            raise AssertionError(f"{expected} should block review queue action")

    create_review_queue_item_action(record.request_id, review_item_id, review_queue_action_payload("hold_for_privacy_review", note="hold"))
    try:
        create_review_queue_item_action(record.request_id, review_item_id, review_queue_action_payload("approve"))
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "transition" in str(exc)
    else:
        raise AssertionError("approval from privacy_hold should be blocked")

    batch_path = tmp_path / "review_queue_items" / f"{record.request_id}_{queue_init.queue_init_id}.json"
    batch_payload = json.loads(batch_path.read_text(encoding="utf-8"))
    batch_payload["items"][0]["privacy"]["raw_author_id_present"] = True
    batch_path.write_text(json.dumps(batch_payload), encoding="utf-8")
    try:
        create_review_queue_item_action(
            record.request_id,
            review_item_id,
            review_queue_action_payload("reset_review", note="reset unsafe item"),
        )
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "forbidden" in str(exc) or "raw_author" in str(exc)
    else:
        raise AssertionError("raw author flag should block review action")


def test_review_queue_completion_gate_passes_complete_mixed_reviewed_queue(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Completion gate complete")))
    package_dir = create_many_row_preview_package(tmp_path)
    _review_case, _staging_import, queue_init, item_batch = create_review_queue_ready_chain(tmp_path, record.request_id, package_dir=package_dir)
    item_ids = [item.review_item_id for item in item_batch.items]

    create_review_queue_item_action(record.request_id, item_ids[0], review_queue_action_payload("approve"))
    create_review_queue_item_action(record.request_id, item_ids[1], review_queue_action_payload("reject", note="Reject weak source."))
    create_review_queue_item_action(record.request_id, item_ids[2], review_queue_action_payload("mark_weak", note="Keep weak with warning."))
    create_review_queue_item_action(
        record.request_id,
        item_ids[3],
        review_queue_action_payload("merge_duplicate", note="Merge duplicate candidate.", duplicate_group_id="dup_completion_gate"),
    )

    gate = create_review_queue_completion_gate(
        record.request_id,
        review_queue_completion_gate_payload(queue_init_id=queue_init.queue_init_id, review_case_id=queue_init.review_case_id),
    )
    gates = list_review_queue_completion_gates(record.request_id)
    read_back = read_review_queue_completion_gate(record.request_id, gate.completion_gate_id)
    updated_batch = read_review_queue_item_batch(record.request_id, queue_init.queue_init_id)
    item_map = {item.review_item_id: item for item in updated_batch.items}

    assert gate.schema_ == "sentigraph_review_queue_completion_gate_v1"
    assert gate.status == "complete_enough_for_future_dedup_preview"
    assert gate.counts.total_items == 4
    assert gate.counts.approved == 1
    assert gate.counts.rejected == 1
    assert gate.counts.marked_weak == 1
    assert gate.counts.duplicate_merged == 1
    assert gate.counts.reviewed_ratio == 1.0
    assert gate.audit_summary.items_with_audit == 4
    assert gate.audit_summary.items_missing_audit == 0
    assert gate.downstream_eligibility.eligible_for_future_dedup_preview is True
    assert gate.downstream_eligibility.can_run_dedup_now is False
    assert gate.downstream_eligibility.can_run_analysis_now is False
    assert gate.now_flags["run_dedup_now"] is False
    assert gate.now_flags["run_analysis_now"] is False
    assert item_map[item_ids[0]].governance.analysis_included is False
    assert item_map[item_ids[1]].governance.analysis_included is False
    assert item_map[item_ids[2]].governance.analysis_included is False
    assert item_map[item_ids[2]].queue_status == "marked_weak"
    assert item_map[item_ids[3]].dedup.may_amplify_risk is False
    assert gates[0].completion_gate_id == gate.completion_gate_id
    assert read_back.completion_gate_id == gate.completion_gate_id


def test_review_queue_completion_gate_reports_incomplete_privacy_and_deferred_states(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))

    incomplete_record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Completion incomplete")))
    _case, _staging, incomplete_queue, _items = create_review_queue_ready_chain(tmp_path, incomplete_record.request_id)
    incomplete_gate = create_review_queue_completion_gate(
        incomplete_record.request_id,
        review_queue_completion_gate_payload(queue_init_id=incomplete_queue.queue_init_id, review_case_id=incomplete_queue.review_case_id),
    )
    assert incomplete_gate.status == "incomplete"
    assert incomplete_gate.counts.review_needed == 2
    assert "reviewed_ratio_below_minimum" in incomplete_gate.blocked_reasons

    privacy_record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Completion privacy hold")))
    _case, _staging, privacy_queue, privacy_items = create_review_queue_ready_chain(tmp_path, privacy_record.request_id)
    create_review_queue_item_action(
        privacy_record.request_id,
        privacy_items.items[0].review_item_id,
        review_queue_action_payload("hold_for_privacy_review", note="Hold for privacy."),
    )
    privacy_gate = create_review_queue_completion_gate(
        privacy_record.request_id,
        review_queue_completion_gate_payload(queue_init_id=privacy_queue.queue_init_id, review_case_id=privacy_queue.review_case_id),
    )
    assert privacy_gate.status == "privacy_hold"
    assert "privacy_hold_items_present" in privacy_gate.blocked_reasons

    deferred_record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Completion deferred")))
    _case, _staging, deferred_queue, deferred_items = create_review_queue_ready_chain(tmp_path, deferred_record.request_id)
    for item in deferred_items.items:
        create_review_queue_item_action(
            deferred_record.request_id,
            item.review_item_id,
            review_queue_action_payload("request_more_source", note="Defer pending source follow-up."),
        )
    blocked_deferred_gate = create_review_queue_completion_gate(
        deferred_record.request_id,
        review_queue_completion_gate_payload(queue_init_id=deferred_queue.queue_init_id, review_case_id=deferred_queue.review_case_id),
    )
    allowed_deferred_gate = create_review_queue_completion_gate(
        deferred_record.request_id,
        review_queue_completion_gate_payload(
            queue_init_id=deferred_queue.queue_init_id,
            review_case_id=deferred_queue.review_case_id,
            allow_deferred_items=True,
        ),
    )
    assert blocked_deferred_gate.status == "incomplete"
    assert "needs_more_source_items_present" in blocked_deferred_gate.blocked_reasons
    assert allowed_deferred_gate.status == "complete_enough_for_future_dedup_preview"
    assert any("deferred" in warning for warning in allowed_deferred_gate.warnings)


def test_review_queue_completion_gate_blocks_unsafe_items_and_payloads(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Completion gate blocks")))
    _review_case, _staging_import, queue_init, item_batch = create_review_queue_ready_chain(tmp_path, record.request_id)
    first_item_id = item_batch.items[0].review_item_id

    unsafe_payloads = [
        (review_queue_completion_gate_payload(queue_init_id=queue_init.queue_init_id, acknowledge_no_report=False), "acknowledgement"),
        (review_queue_completion_gate_payload(queue_init_id=queue_init.queue_init_id, run_analysis_now=True), "side effect"),
        (review_queue_completion_gate_payload(queue_init_id=queue_init.queue_init_id, dedup_run=True), "side effect"),
    ]
    for payload, expected in unsafe_payloads:
        try:
            create_review_queue_completion_gate(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert expected in str(exc)
        else:
            raise AssertionError(f"{expected} should block completion gate request")

    create_review_queue_item_action(record.request_id, first_item_id, review_queue_action_payload("approve"))
    batch_path = tmp_path / "review_queue_items" / f"{record.request_id}_{queue_init.queue_init_id}.json"
    batch_payload = json.loads(batch_path.read_text(encoding="utf-8"))
    batch_payload["items"][0]["queue_status"] = "duplicate_merged"
    batch_payload["items"][0]["governance"]["review_status"] = "duplicate_merged"
    batch_payload["items"][0]["dedup"]["dedup_status"] = "duplicate_candidate_marked"
    batch_payload["items"][0]["dedup"]["may_amplify_risk"] = True
    batch_payload["items"][1]["queue_status"] = "approved"
    batch_payload["items"][1]["governance"]["review_status"] = "approved"
    batch_payload["items"][1]["privacy"]["raw_author_id_present"] = True
    batch_path.write_text(json.dumps(batch_payload), encoding="utf-8")

    gate = create_review_queue_completion_gate(
        record.request_id,
        review_queue_completion_gate_payload(queue_init_id=queue_init.queue_init_id, review_case_id=queue_init.review_case_id),
    )

    assert gate.status == "blocked"
    assert "duplicate_may_amplify_risk" in gate.blocked_reasons
    assert "raw_forbidden_field_risk" in gate.blocked_reasons
    assert "missing_action_audit_for_reviewed_item" in gate.blocked_reasons
    assert gate.downstream_eligibility.eligible_for_future_dedup_preview is False


def test_review_queue_completion_gate_records_are_append_only(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Completion append-only")))
    _review_case, _staging_import, queue_init, item_batch = create_review_queue_ready_chain(tmp_path, record.request_id)
    for item in item_batch.items:
        create_review_queue_item_action(record.request_id, item.review_item_id, review_queue_action_payload("approve"))

    first_gate = create_review_queue_completion_gate(
        record.request_id,
        review_queue_completion_gate_payload(queue_init_id=queue_init.queue_init_id, review_case_id=queue_init.review_case_id),
    )
    second_gate = create_review_queue_completion_gate(
        record.request_id,
        review_queue_completion_gate_payload(queue_init_id=queue_init.queue_init_id, review_case_id=queue_init.review_case_id),
    )
    gates = list_review_queue_completion_gates(record.request_id)

    assert first_gate.completion_gate_id != second_gate.completion_gate_id
    assert {gate.completion_gate_id for gate in gates} >= {first_gate.completion_gate_id, second_gate.completion_gate_id}
    assert len(gates) == 2


def test_dedup_preview_groups_review_only_items_without_reading_package_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Dedup preview signals")))
    package_dir = create_many_row_preview_package(tmp_path)
    _review_case, _staging_import, queue_init, item_batch = create_review_queue_ready_chain(tmp_path, record.request_id, package_dir=package_dir)
    forbidden_row_file = package_dir / "evidence_items.jsonl"
    forbidden_row_file.write_text('{"raw_author_id":"must_not_be_read","source_url":"https://unsafe.example"}\n', encoding="utf-8")
    item_ids = [item.review_item_id for item in item_batch.items]

    create_review_queue_item_action(record.request_id, item_ids[0], review_queue_action_payload("approve"))
    create_review_queue_item_action(record.request_id, item_ids[1], review_queue_action_payload("mark_weak", note="Keep with warning."))
    create_review_queue_item_action(
        record.request_id,
        item_ids[2],
        review_queue_action_payload("merge_duplicate", note="Reviewer merge hint.", duplicate_group_id="manual_hint_a"),
    )
    create_review_queue_item_action(
        record.request_id,
        item_ids[3],
        review_queue_action_payload("merge_duplicate", note="Reviewer merge hint.", duplicate_group_id="manual_hint_a"),
    )

    batch_path = tmp_path / "review_queue_items" / f"{record.request_id}_{queue_init.queue_init_id}.json"
    batch_payload = json.loads(batch_path.read_text(encoding="utf-8"))
    batch_payload["items"][0]["evidence_candidate"]["source_url"] = "https://Example.com/story?utm_source=news&id=42"
    batch_payload["items"][0]["evidence_candidate"]["title_preview"] = "Helldivers PSN rollback"
    batch_payload["items"][0]["evidence_candidate"]["body_text_preview"] = "Same community concern."
    batch_payload["items"][1]["evidence_candidate"]["source_url"] = "https://example.com/story?id=42"
    batch_payload["items"][1]["evidence_candidate"]["title_preview"] = "helldivers psn rollback"
    batch_payload["items"][1]["evidence_candidate"]["body_text_preview"] = "Same   community concern."
    batch_payload["items"][2]["evidence_candidate"]["source_url"] = "https://forum.example/a"
    batch_payload["items"][3]["evidence_candidate"]["source_url"] = "https://forum.example/b"
    batch_path.write_text(json.dumps(batch_payload), encoding="utf-8")

    gate = create_review_queue_completion_gate(
        record.request_id,
        review_queue_completion_gate_payload(queue_init_id=queue_init.queue_init_id, review_case_id=queue_init.review_case_id),
    )
    preview = create_dedup_preview(
        record.request_id,
        dedup_preview_payload(
            review_case_id=queue_init.review_case_id,
            queue_init_id=queue_init.queue_init_id,
            completion_gate_id=gate.completion_gate_id,
        ),
    )
    previews = list_dedup_previews(record.request_id)
    read_back = read_dedup_preview(record.request_id, preview.dedup_preview_id)
    updated_batch = read_review_queue_item_batch(record.request_id, queue_init.queue_init_id)

    assert preview.schema_ == "sentigraph_dedup_preview_v1"
    assert preview.status == "preview_ready"
    assert preview.counts.items_seen == 4
    assert preview.counts.items_eligible_for_preview == 4
    assert preview.counts.duplicate_group_candidates >= 2
    assert preview.readiness.can_run_dedup_now is False
    assert preview.readiness.can_run_analysis_now is False
    assert all(group.may_amplify_risk is False for group in preview.groups)
    assert all(group.analysis_effect == "preview_only_no_analysis_effect" for group in preview.groups)
    assert any(group.reason == "mixed" and set(item_ids[:2]).issubset(set(group.item_ids)) for group in preview.groups)
    assert any(group.reason in {"reviewer_merge_hint", "mixed"} and set(item_ids[2:4]).issubset(set(group.item_ids)) for group in preview.groups)
    assert read_back.dedup_preview_id == preview.dedup_preview_id
    assert previews[0].dedup_preview_id == preview.dedup_preview_id
    assert all(item.governance.analysis_included is False for item in updated_batch.items)
    assert all(item.dedup.may_amplify_risk is False for item in updated_batch.items)
    assert "must_not_be_read" not in json.dumps(preview.model_dump(mode="json"), ensure_ascii=False)


def test_dedup_preview_excludes_ineligible_items_and_honors_include_flags(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Dedup preview exclusions")))
    package_dir = create_many_row_preview_package(tmp_path)
    _review_case, _staging_import, queue_init, item_batch = create_review_queue_ready_chain(tmp_path, record.request_id, package_dir=package_dir)
    item_ids = [item.review_item_id for item in item_batch.items]

    create_review_queue_item_action(record.request_id, item_ids[0], review_queue_action_payload("approve"))
    create_review_queue_item_action(record.request_id, item_ids[1], review_queue_action_payload("reject"))
    create_review_queue_item_action(record.request_id, item_ids[2], review_queue_action_payload("mark_weak"))
    create_review_queue_item_action(
        record.request_id,
        item_ids[3],
        review_queue_action_payload("merge_duplicate", duplicate_group_id="dup_include_flag"),
    )
    gate = create_review_queue_completion_gate(
        record.request_id,
        review_queue_completion_gate_payload(queue_init_id=queue_init.queue_init_id, review_case_id=queue_init.review_case_id),
    )

    preview = create_dedup_preview(
        record.request_id,
        dedup_preview_payload(
            queue_init_id=queue_init.queue_init_id,
            review_case_id=queue_init.review_case_id,
            completion_gate_id=gate.completion_gate_id,
            include_marked_weak=False,
            include_duplicate_merged=False,
        ),
    )

    excluded = {item.review_item_id: item.reason for item in preview.excluded_items}
    assert preview.counts.items_eligible_for_preview == 1
    assert item_ids[1] in excluded and excluded[item_ids[1]] == "status_rejected"
    assert item_ids[2] in excluded and excluded[item_ids[2]] == "marked_weak_not_included"
    assert item_ids[3] in excluded and excluded[item_ids[3]] == "duplicate_merged_not_included"
    assert preview.counts.duplicate_group_candidates == 0
    assert preview.counts.unique_candidate_count == 1


def test_dedup_preview_blocks_unsafe_or_incomplete_creation(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Dedup preview blocks")))
    _review_case, _staging_import, queue_init, item_batch = create_review_queue_ready_chain(tmp_path, record.request_id)
    item_id = item_batch.items[0].review_item_id

    incomplete_gate = create_review_queue_completion_gate(
        record.request_id,
        review_queue_completion_gate_payload(queue_init_id=queue_init.queue_init_id, review_case_id=queue_init.review_case_id),
    )
    assert incomplete_gate.status == "incomplete"

    unsafe_payloads = [
        dedup_preview_payload(queue_init_id=queue_init.queue_init_id, completion_gate_id=incomplete_gate.completion_gate_id),
        dedup_preview_payload(queue_init_id=queue_init.queue_init_id, completion_gate_id="missing_gate"),
        dedup_preview_payload(queue_init_id=queue_init.queue_init_id, completion_gate_id=incomplete_gate.completion_gate_id, acknowledge_no_analysis=False),
        dedup_preview_payload(queue_init_id=queue_init.queue_init_id, completion_gate_id=incomplete_gate.completion_gate_id, run_analysis_now=True),
        dedup_preview_payload(queue_init_id=queue_init.queue_init_id, completion_gate_id=incomplete_gate.completion_gate_id, production_case_id="case_prod_unsafe"),
    ]
    for payload in unsafe_payloads:
        try:
            create_dedup_preview(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert any(text in str(exc) for text in ("completion gate", "acknowledgement", "side effect", "production_case"))
        else:
            raise AssertionError("unsafe dedup preview payload should fail")

    create_review_queue_item_action(record.request_id, item_id, review_queue_action_payload("approve"))
    batch_path = tmp_path / "review_queue_items" / f"{record.request_id}_{queue_init.queue_init_id}.json"
    batch_payload = json.loads(batch_path.read_text(encoding="utf-8"))
    batch_payload["items"][0]["privacy"]["raw_author_id_present"] = True
    batch_path.write_text(json.dumps(batch_payload), encoding="utf-8")
    blocked_gate = create_review_queue_completion_gate(
        record.request_id,
        review_queue_completion_gate_payload(queue_init_id=queue_init.queue_init_id, review_case_id=queue_init.review_case_id),
    )
    assert blocked_gate.status == "blocked"
    try:
        create_dedup_preview(record.request_id, dedup_preview_payload(queue_init_id=queue_init.queue_init_id, completion_gate_id=blocked_gate.completion_gate_id))
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "completion gate" in str(exc)
    else:
        raise AssertionError("blocked completion gate should fail dedup preview")


def test_dedup_preview_records_are_append_only(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Dedup preview append-only")))
    _review_case, _staging_import, queue_init, item_batch = create_review_queue_ready_chain(tmp_path, record.request_id)
    for item in item_batch.items:
        create_review_queue_item_action(record.request_id, item.review_item_id, review_queue_action_payload("approve"))
    gate = create_review_queue_completion_gate(
        record.request_id,
        review_queue_completion_gate_payload(queue_init_id=queue_init.queue_init_id, review_case_id=queue_init.review_case_id),
    )

    first_preview = create_dedup_preview(record.request_id, dedup_preview_payload(queue_init_id=queue_init.queue_init_id, completion_gate_id=gate.completion_gate_id))
    second_preview = create_dedup_preview(record.request_id, dedup_preview_payload(queue_init_id=queue_init.queue_init_id, completion_gate_id=gate.completion_gate_id))
    previews = list_dedup_previews(record.request_id)

    assert first_preview.dedup_preview_id != second_preview.dedup_preview_id
    assert {preview.dedup_preview_id for preview in previews} >= {first_preview.dedup_preview_id, second_preview.dedup_preview_id}
    assert len(previews) == 2


def test_dedup_group_review_confirm_updates_preview_and_appends_audit(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Dedup group confirm")))
    _case, _staging, queue_init, _batch, _gate, preview, group = create_dedup_preview_ready_chain(tmp_path, record.request_id)

    result = create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("confirm_group"),
    )
    updated_preview = read_dedup_preview(record.request_id, preview.dedup_preview_id)
    updated_group = next(item for item in updated_preview.groups if item.group_candidate_id == group.group_candidate_id)
    audits = read_dedup_group_review_audits_for_group(record.request_id, preview.dedup_preview_id, group.group_candidate_id)
    item_batch = read_review_queue_item_batch(record.request_id, queue_init.queue_init_id)

    assert result.schema_ == "sentigraph_dedup_group_review_action_result_v1"
    assert result.previous_group_status == "review_needed"
    assert result.new_group_status == "confirmed"
    assert result.updated_group.group_status == "confirmed"
    assert result.updated_group.human_confirmation_required is False
    assert result.updated_group.may_amplify_risk is False
    assert result.updated_group.analysis_effect == "eligible_for_future_promotion_gate"
    assert result.readiness["can_run_production_dedup_now"] is False
    assert result.readiness["can_run_analysis_now"] is False
    assert result.audit_record.analysis_effect == "eligible_for_future_promotion_gate"
    assert result.audit_record.dedup_effect == "review_only_group_confirmed"
    assert result.audit_record.now_flags["run_production_dedup_now"] is False
    assert updated_group.group_status == "confirmed"
    assert updated_group.human_confirmation_required is False
    assert len(audits) == 1
    assert audits[0].audit_id == result.audit_id
    assert all(item.governance.analysis_included is False for item in item_batch.items)
    assert all(item.dedup.may_amplify_risk is False for item in item_batch.items)


def test_dedup_group_review_actions_are_review_only_and_append_audits(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Dedup group actions")))
    _case, _staging, _queue_init, _batch, _gate, preview, group = create_dedup_preview_ready_chain(tmp_path, record.request_id)
    second_item_id = group.item_ids[1]

    change = create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("change_representative", representative_item_id=second_item_id),
    )
    weak = create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("mark_group_weak"),
    )
    reset = create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("reset_group_review"),
    )
    split = create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("split_group", split_item_ids=[second_item_id]),
    )
    reset_after_split = create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("reset_group_review"),
    )
    reject = create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("reject_group"),
    )
    reset_after_reject = create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("reset_group_review"),
    )
    needs_source = create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("request_more_source"),
    )
    reset_after_source = create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("reset_group_review"),
    )
    privacy = create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("hold_group_for_privacy"),
    )

    request_audits = list_dedup_group_review_audits(record.request_id)
    updated_preview = read_dedup_preview(record.request_id, preview.dedup_preview_id)
    updated_group = next(item for item in updated_preview.groups if item.group_candidate_id == group.group_candidate_id)

    assert change.new_group_status == "representative_changed"
    assert change.updated_group.representative_item_id == second_item_id
    assert weak.new_group_status == "marked_weak"
    assert weak.audit_record.trust_label_effect == "weak_warning"
    assert reset.new_group_status == "review_needed"
    assert split.new_group_status == "split"
    assert split.updated_group.split_item_ids == [second_item_id]
    assert reject.audit_record.analysis_effect == "blocked"
    assert needs_source.audit_record.analysis_effect == "blocked"
    assert privacy.new_group_status == "privacy_hold"
    assert privacy.audit_record.analysis_effect == "blocked"
    assert updated_group.group_status == "privacy_hold"
    assert updated_group.may_amplify_risk is False
    assert len(request_audits) == 10
    assert {audit.audit_id for audit in request_audits} >= {
        change.audit_id,
        weak.audit_id,
        reset.audit_id,
        split.audit_id,
        reset_after_split.audit_id,
        reject.audit_id,
        reset_after_reject.audit_id,
        needs_source.audit_id,
        reset_after_source.audit_id,
        privacy.audit_id,
    }


def test_dedup_group_review_blocks_unsafe_actions(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Dedup group blocks")))
    _case, _staging, queue_init, _batch, _gate, preview, group = create_dedup_preview_ready_chain(tmp_path, record.request_id)

    unsafe_payloads = [
        dedup_group_review_action_payload("confirm_group", reviewer_label=""),
        dedup_group_review_action_payload("confirm_group", acknowledge_no_analysis=False),
        dedup_group_review_action_payload("confirm_group", run_production_dedup_now=True),
        dedup_group_review_action_payload("confirm_group", production_case_id="case_prod_unsafe"),
        dedup_group_review_action_payload("change_representative", representative_item_id="outside_group"),
        dedup_group_review_action_payload("split_group", split_item_ids=[]),
        dedup_group_review_action_payload("split_group", split_item_ids=["outside_group"]),
        dedup_group_review_action_payload("mark_group_weak", note=""),
        dedup_group_review_action_payload("confirm_group", trust_label="high"),
    ]
    for payload in unsafe_payloads:
        try:
            create_dedup_group_review_action(record.request_id, preview.dedup_preview_id, group.group_candidate_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert any(
                text in str(exc)
                for text in ("reviewer", "acknowledgement", "side effect", "production_case", "representative", "split", "note", "trust")
            )
        else:
            raise AssertionError("unsafe dedup group action should fail")

    create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("reject_group"),
    )
    try:
        create_dedup_group_review_action(
            record.request_id,
            preview.dedup_preview_id,
            group.group_candidate_id,
            dedup_group_review_action_payload("confirm_group"),
        )
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "transition" in str(exc)
    else:
        raise AssertionError("invalid transition from rejected should fail")

    create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("reset_group_review"),
    )
    batch_path = tmp_path / "review_queue_items" / f"{record.request_id}_{queue_init.queue_init_id}.json"
    batch_payload = json.loads(batch_path.read_text(encoding="utf-8"))
    batch_payload["items"][0]["privacy"]["raw_author_id_present"] = True
    batch_path.write_text(json.dumps(batch_payload), encoding="utf-8")
    try:
        create_dedup_group_review_action(
            record.request_id,
            preview.dedup_preview_id,
            group.group_candidate_id,
            dedup_group_review_action_payload("confirm_group"),
        )
    except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
        assert "forbidden" in str(exc) or "raw" in str(exc)
    else:
        raise AssertionError("raw/private queue item should block dedup group action")


def test_analysis_ready_promotion_gate_creates_eligible_record_and_audit(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Promotion gate eligible")))
    _case, _staging, queue_init, item_batch, gate, preview, group = create_dedup_preview_ready_chain(tmp_path, record.request_id)
    create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("confirm_group"),
    )

    result = create_analysis_ready_promotion_gate(
        record.request_id,
        promotion_gate_payload(
            review_case_id=queue_init.review_case_id,
            queue_init_id=queue_init.queue_init_id,
            completion_gate_id=gate.completion_gate_id,
            dedup_preview_id=preview.dedup_preview_id,
        ),
    )
    gates = list_analysis_ready_promotion_gates(record.request_id)
    audits = list_promotion_decision_audits(record.request_id)
    read_back = read_analysis_ready_promotion_gate(record.request_id, result.promotion_gate_id)
    refreshed_items = read_review_queue_item_batch(record.request_id, queue_init.queue_init_id).items

    assert result.schema_ == "sentigraph_analysis_ready_promotion_gate_v1"
    assert result.status == "eligible_for_future_manual_analysis_trigger"
    assert result.readiness.eligible_for_future_manual_analysis_trigger is True
    assert result.readiness.can_run_analysis_now is False
    assert result.readiness.can_generate_report_now is False
    assert result.now_flags["run_analysis_now"] is False
    assert result.now_flags["write_evidence_layer_now"] is False
    assert result.input_scope.analysis_included is False
    assert result.input_scope.provider_output_is_truth is False
    assert result.input_scope.official_verification is False
    assert set(result.promotion_set_preview.item_ids) == {item.review_item_id for item in item_batch.items}
    assert group.group_candidate_id in result.promotion_set_preview.group_ids
    assert result.promotion_decision.analysis_effect == "eligible_for_manual_trigger_only"
    assert read_back.promotion_gate_id == result.promotion_gate_id
    assert gates[0].promotion_gate_id == result.promotion_gate_id
    assert audits[0].promotion_gate_id == result.promotion_gate_id
    assert audits[0].analysis_effect == "eligible_for_manual_trigger_only"
    assert audits[0].now_flags["run_analysis_now"] is False
    assert all(item.governance.analysis_included is False for item in refreshed_items)


def test_analysis_ready_promotion_gate_hold_and_reject_are_not_eligible(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Promotion gate human decisions")))
    _case, _staging, queue_init, _batch, gate, preview, group = create_dedup_preview_ready_chain(tmp_path, record.request_id)
    create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("confirm_group"),
    )

    hold = create_analysis_ready_promotion_gate(
        record.request_id,
        promotion_gate_payload(
            "hold_for_more_review",
            review_case_id=queue_init.review_case_id,
            queue_init_id=queue_init.queue_init_id,
            completion_gate_id=gate.completion_gate_id,
            dedup_preview_id=preview.dedup_preview_id,
        ),
    )
    rejected = create_analysis_ready_promotion_gate(
        record.request_id,
        promotion_gate_payload(
            "reject_promotion",
            review_case_id=queue_init.review_case_id,
            queue_init_id=queue_init.queue_init_id,
            completion_gate_id=gate.completion_gate_id,
            dedup_preview_id=preview.dedup_preview_id,
        ),
    )
    audits = list_promotion_decision_audits(record.request_id)

    assert hold.status == "held_by_human"
    assert hold.readiness.eligible_for_future_manual_analysis_trigger is False
    assert hold.promotion_decision.analysis_effect == "held"
    assert rejected.status == "rejected_by_human"
    assert rejected.readiness.eligible_for_future_manual_analysis_trigger is False
    assert rejected.promotion_decision.analysis_effect == "rejected"
    assert len(audits) == 2
    assert {audit.decision for audit in audits} == {"hold_for_more_review", "reject_promotion"}


def test_analysis_ready_promotion_gate_blocks_unresolved_or_unsafe_inputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Promotion gate blockers")))
    _case, _staging, queue_init, _batch, gate, preview, group = create_dedup_preview_ready_chain(tmp_path, record.request_id)
    base_payload = promotion_gate_payload(
        review_case_id=queue_init.review_case_id,
        queue_init_id=queue_init.queue_init_id,
        completion_gate_id=gate.completion_gate_id,
        dedup_preview_id=preview.dedup_preview_id,
    )

    blocked_payloads = [
        {**base_payload, "reviewer_label": ""},
        {**base_payload, "promotion_decision": ""},
        {**base_payload, "coverage_limitations_acknowledged": False},
        {**base_payload, "provider_output_is_evidence_not_truth_acknowledged": False},
        {**base_payload, "run_analysis_now": True},
        {**base_payload, "production_case_id": "case_prod_unsafe"},
        {**base_payload, "trust_label": "high"},
    ]
    for payload in blocked_payloads:
        try:
            create_analysis_ready_promotion_gate(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert validation failure text.
            assert any(text in str(exc) for text in ("reviewer", "decision", "acknowledgement", "side effect", "production_case", "trust"))
        else:
            raise AssertionError("unsafe promotion payload should fail")

    try:
        create_analysis_ready_promotion_gate(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - unresolved group should block.
        assert "group" in str(exc) or "incomplete" in str(exc)
    else:
        raise AssertionError("unreviewed dedup group should block promotion")

    create_dedup_group_review_action(
        record.request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("confirm_group"),
    )
    updated_preview_path = tmp_path / "dedup_previews" / f"{record.request_id}_{preview.dedup_preview_id}.json"
    preview_payload = json.loads(updated_preview_path.read_text(encoding="utf-8"))
    preview_payload["groups"][0]["may_amplify_risk"] = True
    updated_preview_path.write_text(json.dumps(preview_payload), encoding="utf-8")
    try:
        create_analysis_ready_promotion_gate(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - risk amplification should block.
        assert "amplify" in str(exc) or "risk" in str(exc)
    else:
        raise AssertionError("may_amplify_risk group should block promotion")

    preview_payload["groups"][0]["may_amplify_risk"] = False
    updated_preview_path.write_text(json.dumps(preview_payload), encoding="utf-8")
    batch_path = tmp_path / "review_queue_items" / f"{record.request_id}_{queue_init.queue_init_id}.json"
    batch_payload = json.loads(batch_path.read_text(encoding="utf-8"))
    batch_payload["items"][0]["privacy"]["raw_author_id_present"] = True
    batch_path.write_text(json.dumps(batch_payload), encoding="utf-8")
    try:
        create_analysis_ready_promotion_gate(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - raw/private field should block.
        assert "privacy" in str(exc) or "raw" in str(exc) or "forbidden" in str(exc)
    else:
        raise AssertionError("raw/private item should block promotion")

    forbidden_row_file = tmp_path / "many_safe_real_preview_package" / "evidence_items.jsonl"
    if forbidden_row_file.exists():
        forbidden_row_file.write_text('{"raw_author_id":"must_not_be_read_by_promotion","body_text":"unsafe raw package row"}\n', encoding="utf-8")
    batch_payload["items"][0]["privacy"]["raw_author_id_present"] = False
    batch_path.write_text(json.dumps(batch_payload), encoding="utf-8")
    result = create_analysis_ready_promotion_gate(record.request_id, base_payload)
    assert result.status == "eligible_for_future_manual_analysis_trigger"


def create_manual_trigger_ready_chain(tmp_path: Path, request_id: str):
    _case, _staging, queue_init, item_batch, gate, preview, group = create_dedup_preview_ready_chain(tmp_path, request_id)
    create_dedup_group_review_action(
        request_id,
        preview.dedup_preview_id,
        group.group_candidate_id,
        dedup_group_review_action_payload("confirm_group"),
    )
    promotion_gate = create_analysis_ready_promotion_gate(
        request_id,
        promotion_gate_payload(
            review_case_id=queue_init.review_case_id,
            queue_init_id=queue_init.queue_init_id,
            completion_gate_id=gate.completion_gate_id,
            dedup_preview_id=preview.dedup_preview_id,
        ),
    )
    return queue_init, item_batch, promotion_gate


def test_manual_analysis_trigger_records_ready_object_and_audit_without_running_analysis(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Manual trigger ready")))
    queue_init, item_batch, promotion_gate = create_manual_trigger_ready_chain(tmp_path, record.request_id)

    result = create_manual_analysis_trigger(
        record.request_id,
        manual_analysis_trigger_payload(
            promotion_gate_id=promotion_gate.promotion_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    read_back = read_manual_analysis_trigger(record.request_id, result.manual_trigger_id)
    triggers = list_manual_analysis_triggers(record.request_id)
    audits = list_manual_analysis_trigger_audits(record.request_id)
    refreshed_items = read_review_queue_item_batch(record.request_id, queue_init.queue_init_id).items

    assert result.schema_ == "sentigraph_manual_analysis_trigger_v1"
    assert result.status == "trigger_recorded_ready_for_future_analysis_runtime"
    assert result.trigger_decision == "trigger_analysis"
    assert result.analysis_scope.source == "review_only_promoted_set"
    assert set(result.analysis_scope.include_item_ids) == {item.review_item_id for item in item_batch.items}
    assert result.analysis_scope.include_group_ids == promotion_gate.promotion_set_preview.group_ids
    assert result.analysis_scope.exclude_item_ids == promotion_gate.promotion_set_preview.excluded_item_ids
    assert result.analysis_scope.weak_warning_item_ids == promotion_gate.promotion_set_preview.weak_item_ids
    assert result.required_warnings.provider_output_is_evidence_not_truth is True
    assert result.required_warnings.not_official_verification is True
    assert result.required_warnings.not_full_web_coverage is True
    assert result.now_flags["run_analysis_now"] is False
    assert result.now_flags["generate_analysis_result_now"] is False
    assert result.now_flags["write_evidence_layer_now"] is False
    assert result.now_flags["create_production_case_now"] is False
    assert result.readiness.can_run_analysis_now is False
    assert result.readiness.analysis_runtime_not_implemented_here is True
    assert "Analysis Result Boundary Gate" in " ".join(result.recommended_next_steps)
    assert read_back.manual_trigger_id == result.manual_trigger_id
    assert triggers[0].manual_trigger_id == result.manual_trigger_id
    assert len(audits) == 1
    assert audits[0].manual_trigger_id == result.manual_trigger_id
    assert audits[0].analysis_effect == "trigger_record_only_no_analysis_run"
    assert audits[0].now_flags["run_analysis_now"] is False
    assert all(item.governance.analysis_included is False for item in refreshed_items)


def test_manual_analysis_trigger_hold_and_cancel_append_audits_without_analysis(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Manual trigger hold cancel")))
    queue_init, _item_batch, promotion_gate = create_manual_trigger_ready_chain(tmp_path, record.request_id)

    hold = create_manual_analysis_trigger(
        record.request_id,
        manual_analysis_trigger_payload(
            "hold",
            promotion_gate_id=promotion_gate.promotion_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    cancel = create_manual_analysis_trigger(
        record.request_id,
        manual_analysis_trigger_payload(
            "cancel",
            promotion_gate_id=promotion_gate.promotion_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    audits = list_manual_analysis_trigger_audits(record.request_id)

    assert hold.status == "held"
    assert hold.now_flags["run_analysis_now"] is False
    assert cancel.status == "cancelled"
    assert cancel.now_flags["generate_analysis_result_now"] is False
    assert len(audits) == 2
    assert {audit.decision for audit in audits} == {"hold", "cancel"}
    assert all(audit.analysis_effect == "trigger_record_only_no_analysis_run" for audit in audits)


def test_manual_analysis_trigger_blocks_unsafe_or_incomplete_payloads(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Manual trigger blockers")))
    queue_init, _item_batch, promotion_gate = create_manual_trigger_ready_chain(tmp_path, record.request_id)
    base_payload = manual_analysis_trigger_payload(
        promotion_gate_id=promotion_gate.promotion_gate_id,
        review_case_id=queue_init.review_case_id,
    )
    unsafe_payloads = [
        {**base_payload, "promotion_gate_id": ""},
        {**base_payload, "reviewer_label": ""},
        {**base_payload, "note": ""},
        {**base_payload, "coverage_acknowledged": False},
        {**base_payload, "provider_output_is_evidence_not_truth_acknowledged": False},
        {**base_payload, "acknowledge_no_analysis_run": False},
        {**base_payload, "run_analysis_now": True},
        {**base_payload, "generate_analysis_result_now": True},
        {**base_payload, "write_evidence_layer_now": True},
        {**base_payload, "create_production_case_now": True},
        {**base_payload, "generate_report_now": True},
        {**base_payload, "generate_sandbox_now": True},
        {**base_payload, "generate_public_event_now": True},
        {**base_payload, "trust_label": "high"},
        {**base_payload, "verification_status": "verified_by_official_api"},
    ]
    for payload in unsafe_payloads:
        try:
            create_manual_analysis_trigger(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert any(
                text in str(exc)
                for text in ("promotion_gate", "reviewer", "note", "acknowledgement", "side effect", "trust", "verification")
            )
        else:
            raise AssertionError("unsafe manual trigger payload should fail")

    noneligible = create_analysis_ready_promotion_gate(
        record.request_id,
        promotion_gate_payload(
            "hold_for_more_review",
            review_case_id=queue_init.review_case_id,
            queue_init_id=promotion_gate.queue_init_id,
            completion_gate_id=promotion_gate.completion_gate_id,
            dedup_preview_id=promotion_gate.dedup_preview_id,
        ),
    )
    try:
        create_manual_analysis_trigger(
            record.request_id,
            manual_analysis_trigger_payload(
                promotion_gate_id=noneligible.promotion_gate_id,
                review_case_id=queue_init.review_case_id,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - non-eligible gate should block.
        assert "eligible" in str(exc) or "promotion" in str(exc)
    else:
        raise AssertionError("non-eligible promotion gate should block manual trigger")


def test_manual_analysis_trigger_does_not_parse_real_package_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Manual trigger no package parse")))
    queue_init, _item_batch, promotion_gate = create_manual_trigger_ready_chain(tmp_path, record.request_id)
    forbidden_row_file = tmp_path / "many_safe_real_preview_package" / "evidence_items.jsonl"
    assert forbidden_row_file.exists()
    forbidden_row_file.write_text(
        '{"raw_author_id":"must_not_be_read_by_manual_trigger","body_text":"unsafe row"}\n{broken',
        encoding="utf-8",
    )

    result = create_manual_analysis_trigger(
        record.request_id,
        manual_analysis_trigger_payload(
            promotion_gate_id=promotion_gate.promotion_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )

    assert result.status == "trigger_recorded_ready_for_future_analysis_runtime"
    assert "must_not_be_read_by_manual_trigger" not in json.dumps(result.model_dump(mode="json"), ensure_ascii=False)


def create_analysis_result_boundary_ready_chain(tmp_path: Path, request_id: str):
    queue_init, item_batch, promotion_gate = create_manual_trigger_ready_chain(tmp_path, request_id)
    manual_trigger = create_manual_analysis_trigger(
        request_id,
        manual_analysis_trigger_payload(
            promotion_gate_id=promotion_gate.promotion_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    return queue_init, item_batch, promotion_gate, manual_trigger


def test_analysis_result_boundary_gate_creates_ready_record_and_audit_without_analysis(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Analysis boundary ready")))
    queue_init, item_batch, promotion_gate, manual_trigger = create_analysis_result_boundary_ready_chain(tmp_path, record.request_id)

    result = create_analysis_result_boundary_gate(
        record.request_id,
        analysis_result_boundary_gate_payload(
            manual_trigger_id=manual_trigger.manual_trigger_id,
            promotion_gate_id=promotion_gate.promotion_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    read_back = read_analysis_result_boundary_gate(record.request_id, result.boundary_gate_id)
    gates = list_analysis_result_boundary_gates(record.request_id)
    audits = list_analysis_result_boundary_gate_audits(record.request_id)
    refreshed_items = read_review_queue_item_batch(record.request_id, queue_init.queue_init_id).items

    assert result.schema_ == "sentigraph_analysis_result_boundary_gate_v1"
    assert result.status == "boundary_ready_for_future_analysis_result_runtime"
    assert result.analysis_input_boundary.source == "review_only_promoted_candidates"
    assert result.analysis_input_boundary.provider_output_is_truth is False
    assert result.analysis_input_boundary.official_verification is False
    assert result.analysis_input_boundary.full_web_coverage is False
    assert result.analysis_input_boundary.analysis_includes_rejected is False
    assert result.analysis_input_boundary.duplicates_amplify_risk is False
    assert all(result.required_boundary_sections.model_dump().values())
    assert result.counts.included_item_count == len(manual_trigger.analysis_scope.include_item_ids)
    assert result.counts.excluded_rejected_count == len(manual_trigger.analysis_scope.exclude_item_ids)
    assert result.counts.weak_warning_count == len(manual_trigger.analysis_scope.weak_warning_item_ids)
    assert result.counts.duplicate_group_count == len(manual_trigger.analysis_scope.include_group_ids)
    assert result.now_flags["run_analysis_now"] is False
    assert result.now_flags["generate_analysis_result_now"] is False
    assert result.now_flags["generate_report_now"] is False
    assert result.now_flags["write_evidence_layer_now"] is False
    assert result.readiness.can_present_analysis_result_now is False
    assert result.readiness.requires_future_analysis_execution is True
    assert result.readiness.requires_boundary_runtime is False
    assert "Coverage is limited" in " ".join(result.warnings + result.boundary_notes)
    assert "Weak evidence" in " ".join(result.warnings + result.boundary_notes)
    assert "Rejected evidence" in " ".join(result.warnings + result.boundary_notes)
    assert "Duplicate evidence must not amplify risk" in " ".join(result.warnings + result.boundary_notes)
    assert "Provider output is evidence, not truth" in " ".join(result.warnings + result.boundary_notes)
    assert read_back.boundary_gate_id == result.boundary_gate_id
    assert gates[0].boundary_gate_id == result.boundary_gate_id
    assert len(audits) == 1
    assert audits[0].boundary_gate_id == result.boundary_gate_id
    assert audits[0].analysis_effect == "boundary_gate_record_only_no_analysis_run"
    assert audits[0].now_flags["run_analysis_now"] is False
    assert audits[0].now_flags["generate_analysis_result_now"] is False
    assert all(item.governance.analysis_included is False for item in refreshed_items)
    assert all(item.governance.report_visible is False for item in refreshed_items)


def test_analysis_result_boundary_gate_blocks_unsafe_or_incomplete_payloads(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Analysis boundary blockers")))
    queue_init, _item_batch, promotion_gate, manual_trigger = create_analysis_result_boundary_ready_chain(tmp_path, record.request_id)
    base_payload = analysis_result_boundary_gate_payload(
        manual_trigger_id=manual_trigger.manual_trigger_id,
        promotion_gate_id=promotion_gate.promotion_gate_id,
        review_case_id=queue_init.review_case_id,
    )

    unsafe_payloads = [
        {**base_payload, "manual_trigger_id": ""},
        {**base_payload, "promotion_gate_id": ""},
        {**base_payload, "reviewer_label": ""},
        {**base_payload, "note": ""},
        {**base_payload, "coverage_limitation_acknowledged": False},
        {**base_payload, "weak_evidence_warning_acknowledged": False},
        {**base_payload, "rejected_evidence_exclusion_acknowledged": False},
        {**base_payload, "dedup_warning_acknowledged": False},
        {**base_payload, "provider_output_is_evidence_not_truth_acknowledged": False},
        {**base_payload, "not_official_verification_acknowledged": False},
        {**base_payload, "not_full_web_coverage_acknowledged": False},
        {**base_payload, "audit_trace_acknowledged": False},
        {**base_payload, "acknowledge_no_analysis_run": False},
        {**base_payload, "run_analysis_now": True},
        {**base_payload, "generate_analysis_result_now": True},
        {**base_payload, "generate_report_now": True},
        {**base_payload, "generate_sandbox_now": True},
        {**base_payload, "generate_public_event_now": True},
        {**base_payload, "write_evidence_layer_now": True},
        {**base_payload, "create_production_case_now": True},
        {**base_payload, "provider_output_is_truth": True},
        {**base_payload, "official_verification": True},
        {**base_payload, "full_web_coverage": True},
        {**base_payload, "duplicates_amplify_risk": True},
        {**base_payload, "analysis_includes_rejected": True},
    ]
    for payload in unsafe_payloads:
        try:
            create_analysis_result_boundary_gate(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - tests assert local validation failure text.
            assert any(
                text in str(exc)
                for text in ("manual_trigger", "promotion_gate", "reviewer", "note", "acknowledgement", "side effect", "truth", "verification", "coverage", "duplicate", "rejected")
            )
        else:
            raise AssertionError("unsafe boundary gate payload should fail")

    held_trigger = create_manual_analysis_trigger(
        record.request_id,
        manual_analysis_trigger_payload(
            "hold",
            promotion_gate_id=promotion_gate.promotion_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    try:
        create_analysis_result_boundary_gate(
            record.request_id,
            analysis_result_boundary_gate_payload(
                manual_trigger_id=held_trigger.manual_trigger_id,
                promotion_gate_id=promotion_gate.promotion_gate_id,
                review_case_id=queue_init.review_case_id,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - non-ready trigger should block.
        assert "manual trigger" in str(exc).lower() or "ready" in str(exc).lower()
    else:
        raise AssertionError("non-ready manual trigger should block boundary gate")

    audit_path = next((tmp_path / "manual_analysis_trigger_audits").glob(f"{record.request_id}_{manual_trigger.manual_trigger_id}_*.json"))
    audit_path.unlink()
    try:
        create_analysis_result_boundary_gate(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - missing manual trigger audit should block.
        assert "audit" in str(exc).lower()
    else:
        raise AssertionError("missing manual trigger audit should block boundary gate")


def test_analysis_result_boundary_gate_does_not_parse_real_package_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Analysis boundary no package parse")))
    queue_init, _item_batch, promotion_gate, manual_trigger = create_analysis_result_boundary_ready_chain(tmp_path, record.request_id)
    forbidden_row_file = tmp_path / "many_safe_real_preview_package" / "evidence_items.jsonl"
    assert forbidden_row_file.exists()
    forbidden_row_file.write_text(
        '{"raw_author_id":"must_not_be_read_by_boundary_gate","profile_url":"https://forbidden.example/profile","body_text":"unsafe row"}\n{broken',
        encoding="utf-8",
    )

    result = create_analysis_result_boundary_gate(
        record.request_id,
        analysis_result_boundary_gate_payload(
            manual_trigger_id=manual_trigger.manual_trigger_id,
            promotion_gate_id=promotion_gate.promotion_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )

    serialized = json.dumps(result.model_dump(mode="json"), ensure_ascii=False)
    assert result.status == "boundary_ready_for_future_analysis_result_runtime"
    assert "must_not_be_read_by_boundary_gate" not in serialized
    assert "forbidden.example" not in serialized


def create_manual_analysis_execution_ready_chain(tmp_path: Path, request_id: str):
    queue_init, item_batch, promotion_gate, manual_trigger = create_analysis_result_boundary_ready_chain(tmp_path, request_id)
    boundary_gate = create_analysis_result_boundary_gate(
        request_id,
        analysis_result_boundary_gate_payload(
            manual_trigger_id=manual_trigger.manual_trigger_id,
            promotion_gate_id=promotion_gate.promotion_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    return queue_init, item_batch, promotion_gate, manual_trigger, boundary_gate


def test_manual_analysis_execution_creates_candidate_and_audit_without_downstream_outputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Manual execution ready")))
    queue_init, item_batch, promotion_gate, manual_trigger, boundary_gate = create_manual_analysis_execution_ready_chain(
        tmp_path,
        record.request_id,
    )

    result = create_manual_analysis_execution(
        record.request_id,
        manual_analysis_execution_payload(
            manual_trigger_id=manual_trigger.manual_trigger_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            promotion_gate_id=promotion_gate.promotion_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    read_back = read_manual_analysis_execution(record.request_id, result.manual_analysis_execution_id)
    candidate = read_manual_analysis_result_candidate(record.request_id, result.result_candidate_id)
    executions = list_manual_analysis_executions(record.request_id)
    candidates = list_manual_analysis_result_candidates(record.request_id)
    audits = list_manual_analysis_execution_audits(record.request_id)

    assert result.schema_ == "sentigraph_manual_analysis_execution_v1"
    assert result.status == "analysis_result_candidate_created"
    assert result.execution_mode == "local_review_only_candidate"
    assert result.input_scope.analysis_input_source == "manual_trigger_scope"
    assert result.input_scope.original_package_rows_read is False
    assert set(result.input_scope.included_item_ids) == set(manual_trigger.analysis_scope.include_item_ids)
    assert set(result.input_scope.excluded_item_ids) == set(manual_trigger.analysis_scope.exclude_item_ids)
    assert set(result.input_scope.weak_warning_item_ids) == set(manual_trigger.analysis_scope.weak_warning_item_ids)
    assert result.boundary_block.coverage_limitation is True
    assert result.boundary_block.weak_evidence_warning is True
    assert result.boundary_block.rejected_evidence_exclusion_note is True
    assert result.boundary_block.dedup_warning is True
    assert result.boundary_block.provider_output_evidence_not_truth_note is True
    assert result.boundary_block.not_official_verification_note is True
    assert result.boundary_block.not_full_web_coverage_note is True
    assert result.boundary_block.audit_trace_note is True
    assert all(value is False for value in result.now_flags.values())
    assert result.readiness.analysis_result_candidate_created is True
    assert result.readiness.can_generate_report_now is False
    assert result.readiness.can_generate_sandbox_now is False
    assert result.readiness.can_generate_public_event_now is False
    assert result.readiness.requires_result_review_or_report_gate is True
    assert read_back.manual_analysis_execution_id == result.manual_analysis_execution_id
    assert executions[0].manual_analysis_execution_id == result.manual_analysis_execution_id

    assert candidate.schema_ == "sentigraph_manual_analysis_result_candidate_v1"
    assert candidate.analysis_input_source == "manual_trigger_scope"
    assert candidate.source_scope_summary.included_item_count == len(manual_trigger.analysis_scope.include_item_ids)
    assert candidate.source_scope_summary.excluded_rejected_count == len(manual_trigger.analysis_scope.exclude_item_ids)
    assert candidate.source_scope_summary.weak_warning_count == len(manual_trigger.analysis_scope.weak_warning_item_ids)
    assert candidate.source_scope_summary.duplicate_group_count == len(manual_trigger.analysis_scope.include_group_ids)
    assert candidate.downstream_flags["summary_report_ready"] is False
    assert candidate.downstream_flags["sandbox_ready"] is False
    assert candidate.downstream_flags["public_event_ready"] is False
    assert candidate.downstream_flags["b_end_report_ready"] is False
    assert candidate.audit_refs["promotion_gate_id"] == promotion_gate.promotion_gate_id
    assert candidate.audit_refs["manual_trigger_id"] == manual_trigger.manual_trigger_id
    assert candidate.audit_refs["boundary_gate_id"] == boundary_gate.boundary_gate_id
    assert candidates[0].result_candidate_id == candidate.result_candidate_id
    assert len(candidate.analysis_summary["representative_evidence"]) > 0
    serialized_candidate = json.dumps(candidate.model_dump(mode="json"), ensure_ascii=False)
    assert "Provider output is evidence, not truth" in serialized_candidate
    assert "not official verification" in serialized_candidate.lower()
    assert "full-web" in serialized_candidate
    assert "raw_author_id" not in serialized_candidate
    assert "profile_url" not in serialized_candidate
    assert "must_not_be_read" not in serialized_candidate

    assert len(audits) == 1
    assert audits[0].manual_analysis_execution_id == result.manual_analysis_execution_id
    assert audits[0].result_candidate_id == candidate.result_candidate_id
    assert audits[0].analysis_effect == "local_result_candidate_created"
    assert all(value is False for value in audits[0].now_flags.values())
    assert all(item.governance.analysis_included is False for item in item_batch.items)


def test_manual_analysis_execution_blocks_unsafe_or_incomplete_payloads(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Manual execution blockers")))
    queue_init, _item_batch, promotion_gate, manual_trigger, boundary_gate = create_manual_analysis_execution_ready_chain(
        tmp_path,
        record.request_id,
    )
    base_payload = manual_analysis_execution_payload(
        manual_trigger_id=manual_trigger.manual_trigger_id,
        boundary_gate_id=boundary_gate.boundary_gate_id,
        promotion_gate_id=promotion_gate.promotion_gate_id,
        review_case_id=queue_init.review_case_id,
    )
    unsafe_payloads = [
        {**base_payload, "manual_trigger_id": ""},
        {**base_payload, "boundary_gate_id": ""},
        {**base_payload, "reviewer_label": ""},
        {**base_payload, "note": ""},
        {**base_payload, "analysis_execution_mode": "production_analysis"},
        {**base_payload, "acknowledge_local_candidate_only": False},
        {**base_payload, "acknowledge_no_evidence_layer_write": False},
        {**base_payload, "acknowledge_provider_output_is_evidence_not_truth": False},
        {**base_payload, "run_analysis_now": True},
        {**base_payload, "generate_summary_report_now": True},
        {**base_payload, "write_evidence_layer_now": True},
        {**base_payload, "include_rejected_evidence": True},
        {**base_payload, "remove_weak_warnings": True},
        {**base_payload, "duplicates_amplify_risk": True},
        {**base_payload, "official_verification": True},
        {**base_payload, "full_web_coverage": True},
    ]
    for payload in unsafe_payloads:
        try:
            create_manual_analysis_execution(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - each unsafe payload should block.
            assert "manual analysis execution" in str(exc).lower() or "analysis execution" in str(exc).lower()
        else:
            raise AssertionError(f"unsafe payload should block: {payload}")

    held_trigger = create_manual_analysis_trigger(
        record.request_id,
        manual_analysis_trigger_payload(
            "hold",
            promotion_gate_id=promotion_gate.promotion_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    try:
        create_manual_analysis_execution(
            record.request_id,
            manual_analysis_execution_payload(
                manual_trigger_id=held_trigger.manual_trigger_id,
                boundary_gate_id=boundary_gate.boundary_gate_id,
                promotion_gate_id=promotion_gate.promotion_gate_id,
                review_case_id=queue_init.review_case_id,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - non-ready trigger should block.
        assert "manual trigger" in str(exc).lower() or "ready" in str(exc).lower()
    else:
        raise AssertionError("non-ready manual trigger should block execution")

    audit_path = next((tmp_path / "analysis_result_boundary_gate_audits").glob(f"{record.request_id}_{boundary_gate.boundary_gate_id}_*.json"))
    audit_path.unlink()
    try:
        create_manual_analysis_execution(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - missing boundary audit should block.
        assert "audit" in str(exc).lower()
    else:
        raise AssertionError("missing boundary gate audit should block execution")


def test_manual_analysis_execution_does_not_parse_real_package_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Manual execution no package parse")))
    queue_init, _item_batch, promotion_gate, manual_trigger, boundary_gate = create_manual_analysis_execution_ready_chain(
        tmp_path,
        record.request_id,
    )
    forbidden_row_file = tmp_path / "many_safe_real_preview_package" / "evidence_items.jsonl"
    assert forbidden_row_file.exists()
    forbidden_row_file.write_text(
        '{"raw_author_id":"must_not_be_read_by_manual_execution","profile_url":"https://forbidden.example/profile","body_text":"unsafe row"}\n{broken',
        encoding="utf-8",
    )

    result = create_manual_analysis_execution(
        record.request_id,
        manual_analysis_execution_payload(
            manual_trigger_id=manual_trigger.manual_trigger_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            promotion_gate_id=promotion_gate.promotion_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    candidate = read_manual_analysis_result_candidate(record.request_id, result.result_candidate_id)

    serialized = json.dumps(
        {
            "execution": result.model_dump(mode="json"),
            "candidate": candidate.model_dump(mode="json"),
        },
        ensure_ascii=False,
    )
    assert result.status == "analysis_result_candidate_created"
    assert result.input_scope.original_package_rows_read is False
    assert "must_not_be_read_by_manual_execution" not in serialized
    assert "forbidden.example" not in serialized


def create_report_generation_gate_ready_chain(tmp_path: Path, request_id: str):
    queue_init, item_batch, promotion_gate, manual_trigger, boundary_gate = create_manual_analysis_execution_ready_chain(
        tmp_path,
        request_id,
    )
    execution = create_manual_analysis_execution(
        request_id,
        manual_analysis_execution_payload(
            manual_trigger_id=manual_trigger.manual_trigger_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            promotion_gate_id=promotion_gate.promotion_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    candidate = read_manual_analysis_result_candidate(request_id, execution.result_candidate_id)
    return queue_init, item_batch, promotion_gate, manual_trigger, boundary_gate, execution, candidate


def test_report_generation_gate_creates_ready_record_and_audit_without_outputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Report gate ready")))
    queue_init, _item_batch, _promotion_gate, _manual_trigger, boundary_gate, execution, candidate = (
        create_report_generation_gate_ready_chain(tmp_path, record.request_id)
    )

    result = create_report_generation_gate(
        record.request_id,
        report_generation_gate_payload(
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            result_candidate_id=candidate.result_candidate_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    read_back = read_report_generation_gate(record.request_id, result.report_gate_id)
    gates = list_report_generation_gates(record.request_id)
    audits = list_report_generation_gate_audits(record.request_id)

    assert result.schema_ == "sentigraph_report_generation_gate_v1"
    assert result.status == "report_gate_ready_for_future_runtime"
    assert result.allowed_future_outputs.summary_report_candidate is True
    assert result.allowed_future_outputs.b_end_report_candidate is False
    assert result.allowed_future_outputs.pdf_export is False
    assert result.allowed_future_outputs.markdown_export is False
    assert result.allowed_future_outputs.briefing_deck_export is False
    assert result.allowed_future_outputs.sandbox is False
    assert result.allowed_future_outputs.public_event is False
    assert all(result.required_report_sections.model_dump().values())
    assert result.input_boundary.source == "manual_analysis_result_candidate"
    assert result.input_boundary.write_evidence_layer_now is False
    assert result.input_boundary.create_production_case_now is False
    assert result.input_boundary.read_original_package_rows_now is False
    assert result.input_boundary.call_llm_now is False
    assert result.input_boundary.call_external_api_now is False
    assert result.readiness.can_generate_summary_report_candidate_in_future is True
    assert result.readiness.can_generate_summary_report_now is False
    assert result.readiness.can_generate_b_end_report_now is False
    assert result.readiness.can_export_now is False
    assert result.readiness.can_generate_sandbox_now is False
    assert result.readiness.can_generate_public_event_now is False
    assert "Provider output is evidence, not truth" in " ".join(result.warnings + result.boundary_notes)
    assert "Future Phase 7J" in " ".join(result.recommended_next_steps)
    assert read_back.report_gate_id == result.report_gate_id
    assert gates[0].report_gate_id == result.report_gate_id
    assert len(audits) == 1
    assert audits[0].report_gate_id == result.report_gate_id
    assert audits[0].analysis_effect == "report_generation_gate_record_only_no_report_generated"
    assert audits[0].now_flags["generate_summary_report_now"] is False
    assert audits[0].now_flags["generate_b_end_report_now"] is False
    assert audits[0].now_flags["export_now"] is False
    assert audits[0].now_flags["generate_sandbox_now"] is False
    assert audits[0].now_flags["generate_public_event_now"] is False
    assert not (tmp_path / "reports").exists()


def test_report_generation_gate_blocks_unsafe_or_incomplete_payloads(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Report gate blockers")))
    queue_init, _item_batch, _promotion_gate, _manual_trigger, boundary_gate, execution, candidate = (
        create_report_generation_gate_ready_chain(tmp_path, record.request_id)
    )
    base_payload = report_generation_gate_payload(
        manual_analysis_execution_id=execution.manual_analysis_execution_id,
        result_candidate_id=candidate.result_candidate_id,
        boundary_gate_id=boundary_gate.boundary_gate_id,
        review_case_id=queue_init.review_case_id,
    )

    unsafe_payloads = [
        {**base_payload, "manual_analysis_execution_id": ""},
        {**base_payload, "result_candidate_id": ""},
        {**base_payload, "boundary_gate_id": ""},
        {**base_payload, "reviewer_label": ""},
        {**base_payload, "note": ""},
        {**base_payload, "requested_future_output": "b_end_report_candidate"},
        {**base_payload, "acknowledge_gate_only": False},
        {**base_payload, "acknowledge_no_summary_report_generation": False},
        {**base_payload, "acknowledge_no_export_generation": False},
        {**base_payload, "acknowledge_audit_trace_required": False},
        {**base_payload, "generate_summary_report_now": True},
        {**base_payload, "export_now": True},
        {**base_payload, "generate_sandbox_now": True},
        {**base_payload, "generate_public_event_now": True},
        {**base_payload, "write_evidence_layer_now": True},
        {**base_payload, "create_production_case_now": True},
        {**base_payload, "read_original_package_rows_now": True},
        {**base_payload, "call_llm_now": True},
        {**base_payload, "call_external_api_now": True},
        {**base_payload, "include_rejected_evidence": True},
        {**base_payload, "remove_weak_warnings": True},
        {**base_payload, "duplicates_amplify_risk": True},
        {**base_payload, "official_verification": True},
        {**base_payload, "full_web_coverage": True},
    ]
    for payload in unsafe_payloads:
        try:
            create_report_generation_gate(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - local validation should reject each unsafe payload.
            assert "report generation gate" in str(exc).lower() or "report gate" in str(exc).lower()
        else:
            raise AssertionError(f"unsafe report gate payload should block: {payload}")

    candidate_path = tmp_path / "manual_analysis_result_candidates" / f"{record.request_id}_{candidate.result_candidate_id}.json"
    candidate_payload = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate_payload.pop("boundary_block", None)
    candidate_path.write_text(json.dumps(candidate_payload), encoding="utf-8")
    try:
        create_report_generation_gate(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - missing boundary block should block.
        assert "boundary" in str(exc).lower()
    else:
        raise AssertionError("missing candidate boundary block should block report gate")


def test_report_generation_gate_does_not_parse_real_package_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Report gate no package parse")))
    queue_init, _item_batch, _promotion_gate, _manual_trigger, boundary_gate, execution, candidate = (
        create_report_generation_gate_ready_chain(tmp_path, record.request_id)
    )
    forbidden_row_file = tmp_path / "many_safe_real_preview_package" / "evidence_items.jsonl"
    assert forbidden_row_file.exists()
    forbidden_row_file.write_text(
        '{"raw_author_id":"must_not_be_read_by_report_gate","profile_url":"https://forbidden.example/profile","body_text":"unsafe row"}\n{broken',
        encoding="utf-8",
    )

    result = create_report_generation_gate(
        record.request_id,
        report_generation_gate_payload(
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            result_candidate_id=candidate.result_candidate_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )

    serialized = json.dumps(result.model_dump(mode="json"), ensure_ascii=False)
    assert result.status == "report_gate_ready_for_future_runtime"
    assert "must_not_be_read_by_report_gate" not in serialized
    assert "forbidden.example" not in serialized


def create_summary_report_candidate_ready_chain(tmp_path: Path, request_id: str):
    queue_init, item_batch, promotion_gate, manual_trigger, boundary_gate, execution, candidate = (
        create_report_generation_gate_ready_chain(tmp_path, request_id)
    )
    report_gate = create_report_generation_gate(
        request_id,
        report_generation_gate_payload(
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            result_candidate_id=candidate.result_candidate_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    return queue_init, item_batch, promotion_gate, manual_trigger, boundary_gate, execution, candidate, report_gate


def test_summary_report_candidate_creates_local_candidate_and_audit_without_downstream_outputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Summary candidate ready")))
    queue_init, item_batch, _promotion_gate, _manual_trigger, boundary_gate, execution, candidate, report_gate = (
        create_summary_report_candidate_ready_chain(tmp_path, record.request_id)
    )

    result = create_summary_report_candidate(
        record.request_id,
        summary_report_candidate_payload(
            report_gate_id=report_gate.report_gate_id,
            result_candidate_id=candidate.result_candidate_id,
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    read_back = read_summary_report_candidate(record.request_id, result.summary_report_candidate_id)
    candidates = list_summary_report_candidates(record.request_id)
    audits = list_summary_report_candidate_audits(record.request_id)

    assert result.schema_ == "sentigraph_summary_report_candidate_v1"
    assert result.status == "summary_report_candidate_created"
    assert result.summary_report_candidate_id
    assert result.input_refs.manual_analysis_execution_id == execution.manual_analysis_execution_id
    assert result.input_refs.result_candidate_id == candidate.result_candidate_id
    assert result.input_refs.boundary_gate_id == boundary_gate.boundary_gate_id
    assert result.input_refs.report_gate_id == report_gate.report_gate_id
    assert result.input_refs.manual_analysis_execution_audit_ids
    assert result.input_refs.report_generation_gate_audit_ids
    assert result.executive_summary_candidate.title
    assert "candidate" in result.executive_summary_candidate.candidate_only_note.lower()
    assert "evidence, not truth" in result.executive_summary_candidate.confidence_note.lower()
    assert result.evidence_scope_section.source_scope_summary["included_item_count"] == candidate.source_scope_summary.included_item_count
    assert "not full-web" in result.evidence_scope_section.not_full_web_coverage_note.lower()
    assert "not official verification" in result.evidence_scope_section.not_official_verification_note.lower()
    assert result.analysis_summary_section.analysis_summary
    assert result.risk_and_topic_section.risk_caveats
    assert result.representative_evidence_section.items
    assert "raw author identifiers" in result.representative_evidence_section.redaction_note.lower()
    assert "rejected evidence remains excluded" in result.representative_evidence_section.rejected_exclusion_note.lower()
    assert "weak evidence" in result.representative_evidence_section.weak_evidence_note.lower()
    assert "duplicate evidence" in result.representative_evidence_section.duplicate_no_amplification_note.lower()
    assert result.boundary_block.coverage_limitation
    assert result.boundary_block.weak_evidence_warning
    assert result.boundary_block.rejected_evidence_exclusion_note
    assert result.boundary_block.dedup_warning
    assert result.boundary_block.provider_output_evidence_not_truth_note
    assert result.boundary_block.not_official_verification_note
    assert result.boundary_block.not_full_web_coverage_note
    assert result.boundary_block.candidate_only_note
    assert result.boundary_block.audit_trace_note
    assert all(value is False for value in result.downstream_flags.values())
    assert "not final Summary Report" in " ".join(result.warnings + result.limitations)
    assert result.audit_trace.manual_analysis_execution_id == execution.manual_analysis_execution_id
    assert result.audit_trace.result_candidate_id == candidate.result_candidate_id
    assert result.audit_trace.boundary_gate_id == boundary_gate.boundary_gate_id
    assert result.audit_trace.report_gate_id == report_gate.report_gate_id
    assert result.audit_trace.audit_ids
    assert read_back.summary_report_candidate_id == result.summary_report_candidate_id
    assert candidates[0].summary_report_candidate_id == result.summary_report_candidate_id

    serialized = json.dumps(result.model_dump(mode="json"), ensure_ascii=False)
    assert "Provider output is evidence, not truth" in serialized
    assert "official verification" in serialized
    assert "full-web" in serialized
    assert "full-platform" in serialized
    assert "full-thread" in serialized
    assert '"raw_author_id"' not in serialized
    assert '"raw_author_name"' not in serialized
    assert '"profile_url"' not in serialized
    assert "must_not_be_read" not in serialized
    assert all(item.governance.analysis_included is False for item in item_batch.items)

    assert len(audits) == 1
    assert audits[0].summary_report_candidate_id == result.summary_report_candidate_id
    assert audits[0].analysis_effect == "summary_report_candidate_created_no_final_report_generated"
    assert audits[0].now_flags["final_summary_report_now"] is False
    assert audits[0].now_flags["b_end_report_now"] is False
    assert audits[0].now_flags["export_now"] is False
    assert audits[0].now_flags["generate_sandbox_now"] is False
    assert audits[0].now_flags["generate_public_event_now"] is False
    assert not (tmp_path / "summary_reports").exists()
    assert not (tmp_path / "exports").exists()


def test_summary_report_candidate_blocks_unsafe_or_incomplete_payloads(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Summary candidate blockers")))
    queue_init, _item_batch, _promotion_gate, _manual_trigger, boundary_gate, execution, candidate, report_gate = (
        create_summary_report_candidate_ready_chain(tmp_path, record.request_id)
    )
    base_payload = summary_report_candidate_payload(
        report_gate_id=report_gate.report_gate_id,
        result_candidate_id=candidate.result_candidate_id,
        manual_analysis_execution_id=execution.manual_analysis_execution_id,
        boundary_gate_id=boundary_gate.boundary_gate_id,
        review_case_id=queue_init.review_case_id,
    )

    unsafe_payloads = [
        {**base_payload, "report_gate_id": ""},
        {**base_payload, "result_candidate_id": ""},
        {**base_payload, "manual_analysis_execution_id": ""},
        {**base_payload, "boundary_gate_id": ""},
        {**base_payload, "reviewer_label": ""},
        {**base_payload, "note": ""},
        {**base_payload, "candidate_mode": "final_summary_report"},
        {**base_payload, "acknowledge_candidate_only": False},
        {**base_payload, "acknowledge_not_final_summary_report": False},
        {**base_payload, "acknowledge_no_export_generation": False},
        {**base_payload, "acknowledge_audit_trace_required": False},
        {**base_payload, "final_report_now": True},
        {**base_payload, "b_end_report_now": True},
        {**base_payload, "export_now": True},
        {**base_payload, "sandbox_now": True},
        {**base_payload, "public_event_now": True},
        {**base_payload, "write_evidence_layer_now": True},
        {**base_payload, "create_production_case_now": True},
        {**base_payload, "read_original_package_rows_now": True},
        {**base_payload, "call_llm_now": True},
        {**base_payload, "call_external_api_now": True},
        {**base_payload, "include_rejected_evidence": True},
        {**base_payload, "remove_weak_warnings": True},
        {**base_payload, "duplicates_amplify_risk": True},
        {**base_payload, "official_verification": True},
        {**base_payload, "full_web_coverage": True},
        {**base_payload, "raw_author_id": "unsafe"},
    ]
    for payload in unsafe_payloads:
        try:
            create_summary_report_candidate(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - each unsafe payload should block.
            assert "summary report candidate" in str(exc).lower() or "summary candidate" in str(exc).lower()
        else:
            raise AssertionError(f"unsafe summary report candidate payload should block: {payload}")

    audit_path = next((tmp_path / "report_generation_gate_audits").glob(f"{record.request_id}_{report_gate.report_gate_id}_*.json"))
    audit_path.unlink()
    try:
        create_summary_report_candidate(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - missing report gate audit should block.
        assert "audit" in str(exc).lower()
    else:
        raise AssertionError("missing report generation gate audit should block summary candidate")


def test_summary_report_candidate_does_not_parse_original_package_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Summary candidate no row parse")))
    queue_init, _item_batch, _promotion_gate, _manual_trigger, boundary_gate, execution, candidate, report_gate = (
        create_summary_report_candidate_ready_chain(tmp_path, record.request_id)
    )
    forbidden_row_file = tmp_path / "many_safe_real_preview_package" / "evidence_items.jsonl"
    assert forbidden_row_file.exists()
    forbidden_row_file.write_text(
        '{"raw_author_id":"must_not_be_read_by_summary_candidate","profile_url":"https://forbidden.example/profile","body_text":"unsafe row"}\n{broken',
        encoding="utf-8",
    )

    result = create_summary_report_candidate(
        record.request_id,
        summary_report_candidate_payload(
            report_gate_id=report_gate.report_gate_id,
            result_candidate_id=candidate.result_candidate_id,
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )

    serialized = json.dumps(result.model_dump(mode="json"), ensure_ascii=False)
    assert result.status == "summary_report_candidate_created"
    assert "must_not_be_read_by_summary_candidate" not in serialized
    assert "forbidden.example" not in serialized


def create_final_summary_report_review_gate_ready_chain(tmp_path: Path, request_id: str):
    queue_init, item_batch, promotion_gate, manual_trigger, boundary_gate, execution, candidate, report_gate = (
        create_summary_report_candidate_ready_chain(tmp_path, request_id)
    )
    summary_candidate = create_summary_report_candidate(
        request_id,
        summary_report_candidate_payload(
            report_gate_id=report_gate.report_gate_id,
            result_candidate_id=candidate.result_candidate_id,
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    return queue_init, item_batch, promotion_gate, manual_trigger, boundary_gate, execution, candidate, report_gate, summary_candidate


def test_final_summary_report_review_gate_approves_candidate_without_downstream_outputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Final review gate ready")))
    queue_init, item_batch, _promotion_gate, _manual_trigger, boundary_gate, execution, candidate, report_gate, summary_candidate = (
        create_final_summary_report_review_gate_ready_chain(tmp_path, record.request_id)
    )

    result = create_final_summary_report_review_gate(
        record.request_id,
        final_summary_report_review_gate_payload(
            summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
            report_gate_id=report_gate.report_gate_id,
            result_candidate_id=candidate.result_candidate_id,
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    read_back = read_final_summary_report_review_gate(record.request_id, result.final_report_review_gate_id)
    gates = list_final_summary_report_review_gates(record.request_id)
    audits = list_final_summary_report_review_gate_audits(record.request_id)

    assert result.schema_ == "sentigraph_final_summary_report_review_gate_v1"
    assert result.status == "ready_for_future_final_summary_report_runtime"
    assert result.review_decision == "approve_for_future_final_runtime"
    assert result.summary_report_candidate_id == summary_candidate.summary_report_candidate_id
    assert result.report_gate_id == report_gate.report_gate_id
    assert result.result_candidate_id == candidate.result_candidate_id
    assert result.manual_analysis_execution_id == execution.manual_analysis_execution_id
    assert result.boundary_gate_id == boundary_gate.boundary_gate_id
    assert all(result.required_final_report_sections.model_dump().values())
    assert result.input_boundary.source == "summary_report_candidate"
    assert result.input_boundary.read_original_package_rows_now is False
    assert result.input_boundary.call_llm_now is False
    assert result.input_boundary.call_external_api_now is False
    assert result.input_boundary.write_evidence_layer_now is False
    assert result.input_boundary.create_production_case_now is False
    assert result.downstream_readiness.can_run_future_final_summary_report_runtime is True
    assert result.downstream_readiness.can_generate_final_summary_report_now is False
    assert result.downstream_readiness.can_export_now is False
    assert result.downstream_readiness.can_generate_b_end_report_now is False
    assert result.downstream_readiness.can_generate_sandbox_now is False
    assert result.downstream_readiness.can_generate_public_event_now is False
    assert result.downstream_readiness.requires_export_gate is True
    assert result.downstream_readiness.requires_b_end_report_gate is True
    assert result.downstream_readiness.requires_sandbox_gate is True
    assert result.downstream_readiness.requires_public_event_gate is True
    assert "Provider output is evidence, not truth" in " ".join(result.warnings + result.boundary_notes)
    assert "not official verification" in " ".join(result.boundary_notes).lower()
    assert "not full-web" in " ".join(result.boundary_notes).lower()
    assert "not full-platform" in " ".join(result.boundary_notes).lower()
    assert "not full-thread" in " ".join(result.boundary_notes).lower()
    assert "Weak evidence" in " ".join(result.boundary_notes)
    assert "Rejected evidence" in " ".join(result.boundary_notes)
    assert "Duplicate evidence" in " ".join(result.boundary_notes)
    assert result.audit_refs["summary_report_candidate_audit_ids"]
    assert result.audit_refs["report_generation_gate_audit_ids"]
    assert result.audit_refs["manual_analysis_execution_audit_ids"]
    assert result.audit_refs["boundary_gate_audit_ids"]
    assert read_back.final_report_review_gate_id == result.final_report_review_gate_id
    assert gates[0].final_report_review_gate_id == result.final_report_review_gate_id
    assert all(item.governance.analysis_included is False for item in item_batch.items)

    serialized = json.dumps(result.model_dump(mode="json"), ensure_ascii=False)
    assert "Provider output is evidence, not truth" in serialized
    assert "official verification" in serialized
    assert "full-web" in serialized
    assert "full-platform" in serialized
    assert "full-thread" in serialized
    assert '"raw_author_id"' not in serialized
    assert '"raw_author_name"' not in serialized
    assert '"profile_url"' not in serialized

    assert len(audits) == 1
    assert audits[0].final_report_review_gate_id == result.final_report_review_gate_id
    assert audits[0].summary_report_candidate_id == summary_candidate.summary_report_candidate_id
    assert audits[0].analysis_effect == "final_summary_report_review_gate_record_only_no_final_report_generated"
    assert audits[0].now_flags["final_summary_report_now"] is False
    assert audits[0].now_flags["b_end_report_now"] is False
    assert audits[0].now_flags["export_now"] is False
    assert audits[0].now_flags["generate_sandbox_now"] is False
    assert audits[0].now_flags["generate_public_event_now"] is False
    assert audits[0].now_flags["write_evidence_layer_now"] is False
    assert audits[0].now_flags["create_production_case_now"] is False
    assert not (tmp_path / "summary_reports").exists()
    assert not (tmp_path / "exports").exists()
    assert not (tmp_path / "b_end_reports").exists()
    assert not (tmp_path / "sandbox_fixtures").exists()
    assert not (tmp_path / "public_events").exists()


def test_final_summary_report_review_gate_decision_status_mapping(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Final review decisions")))
    queue_init, _item_batch, _promotion_gate, _manual_trigger, boundary_gate, execution, candidate, report_gate, summary_candidate = (
        create_final_summary_report_review_gate_ready_chain(tmp_path, record.request_id)
    )
    base_payload = final_summary_report_review_gate_payload(
        summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
        report_gate_id=report_gate.report_gate_id,
        result_candidate_id=candidate.result_candidate_id,
        manual_analysis_execution_id=execution.manual_analysis_execution_id,
        boundary_gate_id=boundary_gate.boundary_gate_id,
        review_case_id=queue_init.review_case_id,
    )

    revision = create_final_summary_report_review_gate(
        record.request_id,
        {
            **base_payload,
            "review_decision": "request_revision",
            "required_revisions": ["Clarify evidence scope wording before future final runtime."],
        },
    )
    blocked = create_final_summary_report_review_gate(record.request_id, {**base_payload, "review_decision": "block"})
    privacy = create_final_summary_report_review_gate(record.request_id, {**base_payload, "review_decision": "privacy_hold"})

    assert revision.status == "needs_revision"
    assert revision.required_revisions
    assert revision.downstream_readiness.can_run_future_final_summary_report_runtime is False
    assert blocked.status == "blocked"
    assert blocked.downstream_readiness.can_run_future_final_summary_report_runtime is False
    assert privacy.status == "privacy_hold"
    assert privacy.downstream_readiness.can_run_future_final_summary_report_runtime is False

    try:
        create_final_summary_report_review_gate(record.request_id, {**base_payload, "review_decision": "request_revision", "required_revisions": []})
    except Exception as exc:  # noqa: BLE001 - revision decisions require explicit revision notes.
        assert "revision" in str(exc).lower()
    else:
        raise AssertionError("request_revision without required revisions should block")


def test_final_summary_report_review_gate_blocks_unsafe_or_incomplete_payloads(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Final review blockers")))
    queue_init, _item_batch, _promotion_gate, _manual_trigger, boundary_gate, execution, candidate, report_gate, summary_candidate = (
        create_final_summary_report_review_gate_ready_chain(tmp_path, record.request_id)
    )
    base_payload = final_summary_report_review_gate_payload(
        summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
        report_gate_id=report_gate.report_gate_id,
        result_candidate_id=candidate.result_candidate_id,
        manual_analysis_execution_id=execution.manual_analysis_execution_id,
        boundary_gate_id=boundary_gate.boundary_gate_id,
        review_case_id=queue_init.review_case_id,
    )

    unsafe_payloads = [
        {**base_payload, "summary_report_candidate_id": ""},
        {**base_payload, "report_gate_id": ""},
        {**base_payload, "result_candidate_id": ""},
        {**base_payload, "manual_analysis_execution_id": ""},
        {**base_payload, "boundary_gate_id": ""},
        {**base_payload, "reviewer_label": ""},
        {**base_payload, "note": ""},
        {**base_payload, "review_decision": "publish_final_report"},
        {**base_payload, "acknowledge_review_gate_only": False},
        {**base_payload, "acknowledge_no_final_summary_report_generation": False},
        {**base_payload, "acknowledge_no_export_generation": False},
        {**base_payload, "acknowledge_audit_trace_required": False},
        {**base_payload, "final_report_now": True},
        {**base_payload, "final_summary_report_now": True},
        {**base_payload, "b_end_report_now": True},
        {**base_payload, "export_now": True},
        {**base_payload, "sandbox_now": True},
        {**base_payload, "public_event_now": True},
        {**base_payload, "write_evidence_layer_now": True},
        {**base_payload, "create_production_case_now": True},
        {**base_payload, "read_original_package_rows_now": True},
        {**base_payload, "call_llm_now": True},
        {**base_payload, "call_external_api_now": True},
        {**base_payload, "include_rejected_evidence": True},
        {**base_payload, "remove_weak_warnings": True},
        {**base_payload, "duplicates_amplify_risk": True},
        {**base_payload, "official_verification": True},
        {**base_payload, "full_web_coverage": True},
        {**base_payload, "raw_author_id": "unsafe"},
    ]
    for payload in unsafe_payloads:
        try:
            create_final_summary_report_review_gate(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - each unsafe payload should block.
            assert "final summary report review gate" in str(exc).lower() or "final review gate" in str(exc).lower()
        else:
            raise AssertionError(f"unsafe final summary report review payload should block: {payload}")

    audit_path = next((tmp_path / "summary_report_candidate_audits").glob(f"{record.request_id}_{summary_candidate.summary_report_candidate_id}_*.json"))
    audit_path.unlink()
    try:
        create_final_summary_report_review_gate(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - missing summary candidate audit should block.
        assert "audit" in str(exc).lower()
    else:
        raise AssertionError("missing summary report candidate audit should block final review gate")


def test_final_summary_report_review_gate_does_not_parse_original_package_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Final review no row parse")))
    queue_init, _item_batch, _promotion_gate, _manual_trigger, boundary_gate, execution, candidate, report_gate, summary_candidate = (
        create_final_summary_report_review_gate_ready_chain(tmp_path, record.request_id)
    )
    forbidden_row_file = tmp_path / "many_safe_real_preview_package" / "evidence_items.jsonl"
    assert forbidden_row_file.exists()
    forbidden_row_file.write_text(
        '{"raw_author_id":"must_not_be_read_by_final_review_gate","profile_url":"https://forbidden.example/profile","body_text":"unsafe row"}\n{broken',
        encoding="utf-8",
    )

    result = create_final_summary_report_review_gate(
        record.request_id,
        final_summary_report_review_gate_payload(
            summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
            report_gate_id=report_gate.report_gate_id,
            result_candidate_id=candidate.result_candidate_id,
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )

    serialized = json.dumps(result.model_dump(mode="json"), ensure_ascii=False)
    assert result.status == "ready_for_future_final_summary_report_runtime"
    assert "must_not_be_read_by_final_review_gate" not in serialized
    assert "forbidden.example" not in serialized


def create_final_summary_report_ready_chain(tmp_path: Path, request_id: str):
    queue_init, item_batch, promotion_gate, manual_trigger, boundary_gate, execution, candidate, report_gate, summary_candidate = (
        create_final_summary_report_review_gate_ready_chain(tmp_path, request_id)
    )
    final_review_gate = create_final_summary_report_review_gate(
        request_id,
        final_summary_report_review_gate_payload(
            summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
            report_gate_id=report_gate.report_gate_id,
            result_candidate_id=candidate.result_candidate_id,
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    return (
        queue_init,
        item_batch,
        promotion_gate,
        manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
    )


def test_final_summary_report_creates_local_report_and_audit_without_downstream_outputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Final summary report ready")))
    (
        queue_init,
        item_batch,
        _promotion_gate,
        _manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
    ) = create_final_summary_report_ready_chain(tmp_path, record.request_id)

    result = create_final_summary_report(
        record.request_id,
        final_summary_report_payload(
            summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
            final_report_review_gate_id=final_review_gate.final_report_review_gate_id,
            report_gate_id=report_gate.report_gate_id,
            result_candidate_id=candidate.result_candidate_id,
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    read_back = read_final_summary_report(record.request_id, result.final_summary_report_id)
    reports = list_final_summary_reports(record.request_id)
    audits = list_final_summary_report_audits(record.request_id)

    assert result.schema_ == "sentigraph_final_summary_report_v1"
    assert result.status == "final_summary_report_created"
    assert result.review_case_id == queue_init.review_case_id
    assert result.summary_report_candidate_id == summary_candidate.summary_report_candidate_id
    assert result.final_report_review_gate_id == final_review_gate.final_report_review_gate_id
    assert result.report_gate_id == report_gate.report_gate_id
    assert result.result_candidate_id == candidate.result_candidate_id
    assert result.manual_analysis_execution_id == execution.manual_analysis_execution_id
    assert result.boundary_gate_id == boundary_gate.boundary_gate_id
    assert result.report_sections["executive_summary"]["one_sentence_summary"]
    assert result.report_sections["evidence_scope"]["not_full_web_coverage_note"]
    assert result.report_sections["analysis_summary"]["analysis_summary"]
    assert result.report_sections["risk_and_topic"]["risk_caveats"]
    assert result.report_sections["representative_evidence"]["items"]
    assert result.report_sections["limitations"]
    assert result.report_sections["warnings"]
    assert result.report_sections["boundary_block"]["provider_output_evidence_not_truth_note"]
    assert result.report_sections["audit_trace"]["summary_report_candidate_audit_ids"]
    assert result.report_sections["audit_trace"]["final_summary_report_review_gate_audit_ids"]
    assert result.report_sections["audit_trace"]["report_generation_gate_audit_ids"]
    assert result.report_sections["audit_trace"]["manual_analysis_execution_audit_ids"]
    assert result.report_sections["audit_trace"]["boundary_gate_audit_ids"]
    assert result.source_and_scope["source"] == "summary_report_candidate"
    assert result.source_and_scope["provider_output_evidence_not_truth"] is True
    assert result.source_and_scope["not_official_verification"] is True
    assert result.source_and_scope["not_full_web_coverage"] is True
    assert result.source_and_scope["not_full_platform_coverage"] is True
    assert result.source_and_scope["not_full_thread_coverage"] is True
    assert all(value is False for value in result.downstream_flags.values())
    assert all(value is True for value in result.required_next_gates.values())
    assert "Weak evidence" in " ".join(result.warnings + result.boundary_notes)
    assert "Rejected evidence" in " ".join(result.warnings + result.boundary_notes)
    assert "Duplicate evidence" in " ".join(result.warnings + result.boundary_notes)
    assert "Provider output is evidence, not truth" in " ".join(result.warnings + result.boundary_notes)
    assert read_back.final_summary_report_id == result.final_summary_report_id
    assert reports[0].final_summary_report_id == result.final_summary_report_id
    assert all(item.governance.analysis_included is False for item in item_batch.items)

    serialized = json.dumps(result.model_dump(mode="json"), ensure_ascii=False)
    assert "official verification" in serialized
    assert "full-web" in serialized
    assert "full-platform" in serialized
    assert "full-thread" in serialized
    assert '"raw_author_id"' not in serialized
    assert '"raw_author_name"' not in serialized
    assert '"profile_url"' not in serialized

    assert len(audits) == 1
    assert audits[0].final_summary_report_id == result.final_summary_report_id
    assert audits[0].summary_report_candidate_id == summary_candidate.summary_report_candidate_id
    assert audits[0].final_report_review_gate_id == final_review_gate.final_report_review_gate_id
    assert audits[0].analysis_effect == "local_final_summary_report_created_no_export_no_b_end_no_sandbox_no_public_event"
    assert audits[0].now_flags["pdf_export_now"] is False
    assert audits[0].now_flags["markdown_export_now"] is False
    assert audits[0].now_flags["deck_export_now"] is False
    assert audits[0].now_flags["b_end_report_now"] is False
    assert audits[0].now_flags["generate_sandbox_now"] is False
    assert audits[0].now_flags["generate_public_event_now"] is False
    assert audits[0].now_flags["write_evidence_layer_now"] is False
    assert audits[0].now_flags["create_production_case_now"] is False
    assert not (tmp_path / "exports").exists()
    assert not (tmp_path / "b_end_reports").exists()
    assert not (tmp_path / "sandbox_fixtures").exists()
    assert not (tmp_path / "public_events").exists()
    assert not (tmp_path / "production_cases").exists()


def test_final_summary_report_blocks_unsafe_or_incomplete_payloads(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Final report blockers")))
    queue_init, _item_batch, _promotion_gate, _manual_trigger, boundary_gate, execution, candidate, report_gate, summary_candidate, final_review_gate = (
        create_final_summary_report_ready_chain(tmp_path, record.request_id)
    )
    base_payload = final_summary_report_payload(
        summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
        final_report_review_gate_id=final_review_gate.final_report_review_gate_id,
        report_gate_id=report_gate.report_gate_id,
        result_candidate_id=candidate.result_candidate_id,
        manual_analysis_execution_id=execution.manual_analysis_execution_id,
        boundary_gate_id=boundary_gate.boundary_gate_id,
        review_case_id=queue_init.review_case_id,
    )

    unsafe_payloads = [
        {**base_payload, "summary_report_candidate_id": ""},
        {**base_payload, "final_report_review_gate_id": ""},
        {**base_payload, "report_gate_id": ""},
        {**base_payload, "result_candidate_id": ""},
        {**base_payload, "manual_analysis_execution_id": ""},
        {**base_payload, "boundary_gate_id": ""},
        {**base_payload, "reviewer_label": ""},
        {**base_payload, "note": ""},
        {**base_payload, "acknowledge_local_final_summary_report_only": False},
        {**base_payload, "acknowledge_no_pdf_export": False},
        {**base_payload, "acknowledge_no_markdown_export": False},
        {**base_payload, "acknowledge_no_deck_export": False},
        {**base_payload, "acknowledge_no_b_end_report": False},
        {**base_payload, "acknowledge_no_sandbox_or_public_event": False},
        {**base_payload, "acknowledge_no_evidence_layer_write": False},
        {**base_payload, "acknowledge_no_production_case": False},
        {**base_payload, "acknowledge_provider_output_is_evidence_not_truth": False},
        {**base_payload, "acknowledge_not_official_verification": False},
        {**base_payload, "acknowledge_not_full_web_coverage": False},
        {**base_payload, "acknowledge_weak_evidence_warning": False},
        {**base_payload, "acknowledge_rejected_exclusion": False},
        {**base_payload, "acknowledge_dedup_no_risk_amplification": False},
        {**base_payload, "acknowledge_audit_trace_required": False},
        {**base_payload, "pdf_export_now": True},
        {**base_payload, "markdown_export_now": True},
        {**base_payload, "deck_export_now": True},
        {**base_payload, "b_end_report_now": True},
        {**base_payload, "sandbox_now": True},
        {**base_payload, "public_event_now": True},
        {**base_payload, "write_evidence_layer_now": True},
        {**base_payload, "create_production_case_now": True},
        {**base_payload, "read_original_package_rows_now": True},
        {**base_payload, "call_llm_now": True},
        {**base_payload, "call_external_api_now": True},
        {**base_payload, "include_rejected_evidence": True},
        {**base_payload, "remove_weak_warnings": True},
        {**base_payload, "duplicates_amplify_risk": True},
        {**base_payload, "official_verification": True},
        {**base_payload, "full_web_coverage": True},
        {**base_payload, "raw_author_id": "unsafe"},
    ]
    for payload in unsafe_payloads:
        try:
            create_final_summary_report(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - each unsafe payload should block.
            assert "final summary report" in str(exc).lower()
        else:
            raise AssertionError(f"unsafe final summary report payload should block: {payload}")

    audit_path = next((tmp_path / "final_summary_report_review_gate_audits").glob(f"{record.request_id}_{final_review_gate.final_report_review_gate_id}_*.json"))
    audit_path.unlink()
    try:
        create_final_summary_report(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - missing final review audit should block.
        assert "audit" in str(exc).lower()
    else:
        raise AssertionError("missing final review gate audit should block final summary report")


def test_final_summary_report_requires_ready_review_gate(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Final report requires gate")))
    queue_init, _item_batch, _promotion_gate, _manual_trigger, boundary_gate, execution, candidate, report_gate, summary_candidate = (
        create_final_summary_report_review_gate_ready_chain(tmp_path, record.request_id)
    )
    revision_gate = create_final_summary_report_review_gate(
        record.request_id,
        final_summary_report_review_gate_payload(
            summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
            report_gate_id=report_gate.report_gate_id,
            result_candidate_id=candidate.result_candidate_id,
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
            review_decision="request_revision",
            required_revisions=["Clarify report scope before final runtime."],
        ),
    )

    try:
        create_final_summary_report(
            record.request_id,
            final_summary_report_payload(
                summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
                final_report_review_gate_id=revision_gate.final_report_review_gate_id,
                report_gate_id=report_gate.report_gate_id,
                result_candidate_id=candidate.result_candidate_id,
                manual_analysis_execution_id=execution.manual_analysis_execution_id,
                boundary_gate_id=boundary_gate.boundary_gate_id,
                review_case_id=queue_init.review_case_id,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - non-ready final gate should block.
        assert "not ready" in str(exc).lower() or "ready" in str(exc).lower()
    else:
        raise AssertionError("non-ready final review gate should block final summary report")


def test_final_summary_report_does_not_parse_original_package_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Final report no row parse")))
    queue_init, _item_batch, _promotion_gate, _manual_trigger, boundary_gate, execution, candidate, report_gate, summary_candidate, final_review_gate = (
        create_final_summary_report_ready_chain(tmp_path, record.request_id)
    )
    forbidden_row_file = tmp_path / "many_safe_real_preview_package" / "evidence_items.jsonl"
    assert forbidden_row_file.exists()
    forbidden_row_file.write_text(
        '{"raw_author_id":"must_not_be_read_by_final_report","profile_url":"https://forbidden.example/profile","body_text":"unsafe row"}\n{broken',
        encoding="utf-8",
    )

    result = create_final_summary_report(
        record.request_id,
        final_summary_report_payload(
            summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
            final_report_review_gate_id=final_review_gate.final_report_review_gate_id,
            report_gate_id=report_gate.report_gate_id,
            result_candidate_id=candidate.result_candidate_id,
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )

    serialized = json.dumps(result.model_dump(mode="json"), ensure_ascii=False)
    assert result.status == "final_summary_report_created"
    assert "must_not_be_read_by_final_report" not in serialized
    assert "forbidden.example" not in serialized


def create_final_summary_report_export_gate_ready_chain(tmp_path: Path, request_id: str):
    queue_init, item_batch, promotion_gate, manual_trigger, boundary_gate, execution, candidate, report_gate, summary_candidate, final_review_gate = (
        create_final_summary_report_ready_chain(tmp_path, request_id)
    )
    final_report = create_final_summary_report(
        request_id,
        final_summary_report_payload(
            summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
            final_report_review_gate_id=final_review_gate.final_report_review_gate_id,
            report_gate_id=report_gate.report_gate_id,
            result_candidate_id=candidate.result_candidate_id,
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    final_report_audit = list_final_summary_report_audits(request_id)[0]
    return (
        queue_init,
        item_batch,
        promotion_gate,
        manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
        final_report,
        final_report_audit,
    )


def test_final_summary_report_export_gate_approves_future_export_without_generating_files(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Export gate ready")))
    (
        queue_init,
        item_batch,
        _promotion_gate,
        _manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
        final_report,
        final_report_audit,
    ) = create_final_summary_report_export_gate_ready_chain(tmp_path, record.request_id)
    fake_exports = [
        tmp_path / "exports" / "final-summary.md",
        tmp_path / "exports" / "final-summary.pdf",
        tmp_path / "exports" / "final-summary.pptx",
    ]

    result = create_final_summary_report_export_gate(
        record.request_id,
        final_summary_report_export_gate_payload(
            final_summary_report_id=final_report.final_summary_report_id,
            final_summary_report_audit_id=final_report_audit.final_summary_report_audit_id,
            summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
            final_report_review_gate_id=final_review_gate.final_report_review_gate_id,
            report_gate_id=report_gate.report_gate_id,
            result_candidate_id=candidate.result_candidate_id,
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    read_back = read_final_summary_report_export_gate(record.request_id, result.export_gate_id)
    gates = list_final_summary_report_export_gates(record.request_id)
    audits = list_final_summary_report_export_gate_audits(record.request_id)

    assert result.schema_ == "sentigraph_final_summary_report_export_gate_v1"
    assert result.status == "ready_for_future_export_runtime"
    assert result.export_decision == "approve_for_future_export_runtime"
    assert result.final_summary_report_id == final_report.final_summary_report_id
    assert result.final_summary_report_audit_id == final_report_audit.final_summary_report_audit_id
    assert result.summary_report_candidate_id == summary_candidate.summary_report_candidate_id
    assert result.final_report_review_gate_id == final_review_gate.final_report_review_gate_id
    assert result.report_gate_id == report_gate.report_gate_id
    assert result.result_candidate_id == candidate.result_candidate_id
    assert result.manual_analysis_execution_id == execution.manual_analysis_execution_id
    assert result.boundary_gate_id == boundary_gate.boundary_gate_id
    assert result.allowed_future_exports["markdown_export_candidate"] is True
    assert result.allowed_future_exports["pdf_export_candidate"] is True
    assert result.allowed_future_exports["briefing_deck_outline_candidate"] is True
    assert result.not_allowed_now["markdown_file_now"] is True
    assert result.not_allowed_now["pdf_file_now"] is True
    assert result.not_allowed_now["pptx_file_now"] is True
    assert result.not_allowed_now["b_end_report_now"] is True
    assert result.not_allowed_now["sandbox_now"] is True
    assert result.not_allowed_now["public_event_now"] is True
    assert result.input_boundary["source"] == "final_summary_report"
    assert result.input_boundary["read_original_package_rows_now"] is False
    assert result.input_boundary["call_llm_now"] is False
    assert result.input_boundary["call_external_api_now"] is False
    assert result.input_boundary["write_evidence_layer_now"] is False
    assert result.input_boundary["create_production_case_now"] is False
    assert all(result.required_export_sections.values())
    assert result.downstream_readiness["can_run_future_markdown_export_runtime"] is True
    assert result.downstream_readiness["can_generate_export_now"] is False
    assert result.downstream_readiness["can_generate_b_end_report_now"] is False
    assert result.downstream_readiness["can_generate_sandbox_now"] is False
    assert result.downstream_readiness["can_generate_public_event_now"] is False
    assert result.downstream_readiness["requires_b_end_report_gate"] is True
    assert result.downstream_readiness["requires_sandbox_gate"] is True
    assert result.downstream_readiness["requires_public_event_gate"] is True
    assert result.audit_refs["final_summary_report_audit_ids"] == [final_report_audit.final_summary_report_audit_id]
    assert result.audit_refs["final_summary_report_review_gate_audit_ids"]
    assert result.audit_refs["summary_report_candidate_audit_ids"]
    assert result.audit_refs["report_generation_gate_audit_ids"]
    assert result.audit_refs["manual_analysis_execution_audit_ids"]
    assert result.audit_refs["boundary_gate_audit_ids"]
    assert read_back.export_gate_id == result.export_gate_id
    assert gates[0].export_gate_id == result.export_gate_id
    assert all(item.governance.analysis_included is False for item in item_batch.items)

    serialized = json.dumps(result.model_dump(mode="json"), ensure_ascii=False)
    assert "Provider output is evidence, not truth" in serialized
    assert "official verification" in serialized
    assert "full-web" in serialized
    assert "full-platform" in serialized
    assert "full-thread" in serialized
    assert '"raw_author_id"' not in serialized
    assert '"raw_author_name"' not in serialized
    assert '"profile_url"' not in serialized

    assert len(audits) == 1
    assert audits[0].schema_ == "sentigraph_final_summary_report_export_gate_audit_v1"
    assert audits[0].export_gate_id == result.export_gate_id
    assert audits[0].final_summary_report_id == final_report.final_summary_report_id
    assert audits[0].final_summary_report_audit_id == final_report_audit.final_summary_report_audit_id
    assert audits[0].analysis_effect == "final_summary_report_export_gate_record_only_no_export_generated"
    assert audits[0].now_flags["markdown_file_now"] is False
    assert audits[0].now_flags["pdf_file_now"] is False
    assert audits[0].now_flags["pptx_file_now"] is False
    assert audits[0].now_flags["b_end_report_now"] is False
    assert audits[0].now_flags["generate_sandbox_now"] is False
    assert audits[0].now_flags["generate_public_event_now"] is False
    assert audits[0].now_flags["write_evidence_layer_now"] is False
    assert audits[0].now_flags["create_production_case_now"] is False
    assert all(not path.exists() for path in fake_exports)
    assert not (tmp_path / "b_end_reports").exists()
    assert not (tmp_path / "sandbox_fixtures").exists()
    assert not (tmp_path / "public_events").exists()
    assert not (tmp_path / "production_cases").exists()


def test_final_summary_report_export_gate_decision_status_mapping(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Export gate decisions")))
    (
        queue_init,
        _item_batch,
        _promotion_gate,
        _manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
        final_report,
        final_report_audit,
    ) = create_final_summary_report_export_gate_ready_chain(tmp_path, record.request_id)
    base_payload = final_summary_report_export_gate_payload(
        final_summary_report_id=final_report.final_summary_report_id,
        final_summary_report_audit_id=final_report_audit.final_summary_report_audit_id,
        summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
        final_report_review_gate_id=final_review_gate.final_report_review_gate_id,
        report_gate_id=report_gate.report_gate_id,
        result_candidate_id=candidate.result_candidate_id,
        manual_analysis_execution_id=execution.manual_analysis_execution_id,
        boundary_gate_id=boundary_gate.boundary_gate_id,
        review_case_id=queue_init.review_case_id,
    )

    revision = create_final_summary_report_export_gate(
        record.request_id,
        {
            **base_payload,
            "export_decision": "request_revision",
            "required_revisions": ["Restore visible export boundary block before future export runtime."],
        },
    )
    blocked = create_final_summary_report_export_gate(record.request_id, {**base_payload, "export_decision": "block"})
    privacy = create_final_summary_report_export_gate(record.request_id, {**base_payload, "export_decision": "privacy_hold"})

    assert revision.status == "needs_revision"
    assert revision.required_revisions
    assert revision.downstream_readiness["can_run_future_markdown_export_runtime"] is False
    assert blocked.status == "blocked"
    assert blocked.downstream_readiness["can_run_future_markdown_export_runtime"] is False
    assert privacy.status == "privacy_hold"
    assert privacy.downstream_readiness["can_run_future_markdown_export_runtime"] is False

    try:
        create_final_summary_report_export_gate(
            record.request_id,
            {**base_payload, "export_decision": "request_revision", "required_revisions": []},
        )
    except Exception as exc:  # noqa: BLE001 - revision decisions require explicit revision notes.
        assert "revision" in str(exc).lower()
    else:
        raise AssertionError("request_revision without required revisions should block")


def test_final_summary_report_export_gate_blocks_unsafe_or_incomplete_payloads(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Export gate blockers")))
    (
        queue_init,
        _item_batch,
        _promotion_gate,
        _manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
        final_report,
        final_report_audit,
    ) = create_final_summary_report_export_gate_ready_chain(tmp_path, record.request_id)
    base_payload = final_summary_report_export_gate_payload(
        final_summary_report_id=final_report.final_summary_report_id,
        final_summary_report_audit_id=final_report_audit.final_summary_report_audit_id,
        summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
        final_report_review_gate_id=final_review_gate.final_report_review_gate_id,
        report_gate_id=report_gate.report_gate_id,
        result_candidate_id=candidate.result_candidate_id,
        manual_analysis_execution_id=execution.manual_analysis_execution_id,
        boundary_gate_id=boundary_gate.boundary_gate_id,
        review_case_id=queue_init.review_case_id,
    )

    unsafe_payloads = [
        {**base_payload, "final_summary_report_id": ""},
        {**base_payload, "final_summary_report_audit_id": ""},
        {**base_payload, "summary_report_candidate_id": ""},
        {**base_payload, "final_report_review_gate_id": ""},
        {**base_payload, "report_gate_id": ""},
        {**base_payload, "result_candidate_id": ""},
        {**base_payload, "manual_analysis_execution_id": ""},
        {**base_payload, "boundary_gate_id": ""},
        {**base_payload, "reviewer_label": ""},
        {**base_payload, "note": ""},
        {**base_payload, "export_decision": "generate_pdf_now"},
        {**base_payload, "acknowledge_export_gate_only": False},
        {**base_payload, "acknowledge_no_markdown_file_now": False},
        {**base_payload, "acknowledge_no_pdf_file_now": False},
        {**base_payload, "acknowledge_no_pptx_file_now": False},
        {**base_payload, "acknowledge_no_b_end_report_generation": False},
        {**base_payload, "acknowledge_no_sandbox_or_public_event": False},
        {**base_payload, "acknowledge_no_evidence_layer_write": False},
        {**base_payload, "acknowledge_no_production_case": False},
        {**base_payload, "acknowledge_provider_output_is_evidence_not_truth": False},
        {**base_payload, "acknowledge_not_official_verification": False},
        {**base_payload, "acknowledge_not_full_web_coverage": False},
        {**base_payload, "acknowledge_weak_evidence_warning": False},
        {**base_payload, "acknowledge_rejected_exclusion": False},
        {**base_payload, "acknowledge_dedup_no_risk_amplification": False},
        {**base_payload, "acknowledge_audit_trace_required": False},
        {**base_payload, "markdown_file_now": True},
        {**base_payload, "pdf_file_now": True},
        {**base_payload, "pptx_file_now": True},
        {**base_payload, "b_end_report_now": True},
        {**base_payload, "sandbox_now": True},
        {**base_payload, "public_event_now": True},
        {**base_payload, "write_evidence_layer_now": True},
        {**base_payload, "create_production_case_now": True},
        {**base_payload, "read_original_package_rows_now": True},
        {**base_payload, "call_llm_now": True},
        {**base_payload, "call_external_api_now": True},
        {**base_payload, "provider_execution_requested": True},
        {**base_payload, "collector_job_requested": True},
        {**base_payload, "include_rejected_evidence": True},
        {**base_payload, "remove_weak_warnings": True},
        {**base_payload, "duplicates_amplify_risk": True},
        {**base_payload, "provider_output_is_truth": True},
        {**base_payload, "official_verification": True},
        {**base_payload, "full_web_coverage": True},
        {**base_payload, "raw_author_id": "unsafe"},
    ]
    for payload in unsafe_payloads:
        try:
            create_final_summary_report_export_gate(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - each unsafe payload should block.
            assert "export gate" in str(exc).lower() or "export" in str(exc).lower()
        else:
            raise AssertionError(f"unsafe final summary report export gate payload should block: {payload}")

    audit_path = next((tmp_path / "final_summary_report_audits").glob(f"{record.request_id}_{final_report.final_summary_report_id}_*.json"))
    audit_path.unlink()
    try:
        create_final_summary_report_export_gate(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - missing final summary report audit should block.
        assert "audit" in str(exc).lower()
    else:
        raise AssertionError("missing final summary report audit should block export gate")


def test_final_summary_report_export_gate_requires_report_boundaries(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Export gate boundaries")))
    (
        queue_init,
        _item_batch,
        _promotion_gate,
        _manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
        final_report,
        final_report_audit,
    ) = create_final_summary_report_export_gate_ready_chain(tmp_path, record.request_id)
    report_path = next((tmp_path / "final_summary_reports").glob(f"{record.request_id}_{final_report.final_summary_report_id}.json"))
    report_data = json.loads(report_path.read_text(encoding="utf-8"))
    report_data["report_sections"].pop("boundary_block")
    report_path.write_text(json.dumps(report_data), encoding="utf-8")

    try:
        create_final_summary_report_export_gate(
            record.request_id,
            final_summary_report_export_gate_payload(
                final_summary_report_id=final_report.final_summary_report_id,
                final_summary_report_audit_id=final_report_audit.final_summary_report_audit_id,
                summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
                final_report_review_gate_id=final_review_gate.final_report_review_gate_id,
                report_gate_id=report_gate.report_gate_id,
                result_candidate_id=candidate.result_candidate_id,
                manual_analysis_execution_id=execution.manual_analysis_execution_id,
                boundary_gate_id=boundary_gate.boundary_gate_id,
                review_case_id=queue_init.review_case_id,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - missing required boundary section should block.
        assert "boundary" in str(exc).lower() or "section" in str(exc).lower()
    else:
        raise AssertionError("missing final report boundary block should block export gate")


def test_final_summary_report_export_gate_does_not_parse_original_package_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Export gate no row parse")))
    (
        queue_init,
        _item_batch,
        _promotion_gate,
        _manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
        final_report,
        final_report_audit,
    ) = create_final_summary_report_export_gate_ready_chain(tmp_path, record.request_id)
    forbidden_row_file = tmp_path / "many_safe_real_preview_package" / "evidence_items.jsonl"
    assert forbidden_row_file.exists()
    forbidden_row_file.write_text(
        '{"raw_author_id":"must_not_be_read_by_export_gate","profile_url":"https://forbidden.example/profile","body_text":"unsafe row"}\n{broken',
        encoding="utf-8",
    )

    result = create_final_summary_report_export_gate(
        record.request_id,
        final_summary_report_export_gate_payload(
            final_summary_report_id=final_report.final_summary_report_id,
            final_summary_report_audit_id=final_report_audit.final_summary_report_audit_id,
            summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
            final_report_review_gate_id=final_review_gate.final_report_review_gate_id,
            report_gate_id=report_gate.report_gate_id,
            result_candidate_id=candidate.result_candidate_id,
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )

    serialized = json.dumps(result.model_dump(mode="json"), ensure_ascii=False)
    assert result.status == "ready_for_future_export_runtime"
    assert "must_not_be_read_by_export_gate" not in serialized
    assert "forbidden.example" not in serialized


def create_final_summary_report_export_artifact_ready_chain(tmp_path: Path, request_id: str):
    (
        queue_init,
        item_batch,
        promotion_gate,
        manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
        final_report,
        final_report_audit,
    ) = create_final_summary_report_export_gate_ready_chain(tmp_path, request_id)
    export_gate = create_final_summary_report_export_gate(
        request_id,
        final_summary_report_export_gate_payload(
            final_summary_report_id=final_report.final_summary_report_id,
            final_summary_report_audit_id=final_report_audit.final_summary_report_audit_id,
            summary_report_candidate_id=summary_candidate.summary_report_candidate_id,
            final_report_review_gate_id=final_review_gate.final_report_review_gate_id,
            report_gate_id=report_gate.report_gate_id,
            result_candidate_id=candidate.result_candidate_id,
            manual_analysis_execution_id=execution.manual_analysis_execution_id,
            boundary_gate_id=boundary_gate.boundary_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    export_gate_audit = list_final_summary_report_export_gate_audits(request_id)[0]
    return (
        queue_init,
        item_batch,
        promotion_gate,
        manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
        final_report,
        final_report_audit,
        export_gate,
        export_gate_audit,
    )


def test_final_summary_report_export_runtime_creates_allowed_local_artifacts(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Export artifact runtime")))
    (
        queue_init,
        item_batch,
        _promotion_gate,
        _manual_trigger,
        _boundary_gate,
        _execution,
        _candidate,
        _report_gate,
        _summary_candidate,
        _final_review_gate,
        final_report,
        _final_report_audit,
        export_gate,
        export_gate_audit,
    ) = create_final_summary_report_export_artifact_ready_chain(tmp_path, record.request_id)

    expected_formats = {
        "analyst_markdown": ("md", ".md"),
        "briefing_deck_outline": ("pptx_outline", ".json"),
        "evidence_appendix_package": ("json_bundle", ".json"),
    }
    created = []
    for artifact_type, (expected_format, expected_suffix) in expected_formats.items():
        artifact = analysis_request_store.create_final_summary_report_export_artifact(
            record.request_id,
            final_summary_report_export_artifact_payload(
                final_summary_report_id=final_report.final_summary_report_id,
                export_gate_id=export_gate.export_gate_id,
                export_gate_audit_id=export_gate_audit.export_gate_audit_id,
                review_case_id=queue_init.review_case_id,
                artifact_type=artifact_type,
            ),
        )
        created.append(artifact)
        local_path = artifact.artifact_paths["local_runtime_path"]
        artifact_file = tmp_path / Path(local_path).relative_to("runtime/analysis_requests")

        assert artifact.schema_ == "sentigraph_final_summary_report_export_artifact_v1"
        assert artifact.status == "export_artifact_created"
        assert artifact.artifact_type == artifact_type
        assert artifact.artifact_format == expected_format
        assert local_path.startswith(f"runtime/analysis_requests/final_summary_report_exports/{record.request_id}/")
        assert local_path.endswith(expected_suffix)
        assert artifact_file.exists()
        assert artifact_file.resolve().is_relative_to((tmp_path / "final_summary_report_exports").resolve())
        assert artifact.artifact_scope["is_b_end_report"] is False
        assert artifact.artifact_scope["is_public_event"] is False
        assert artifact.artifact_scope["is_sandbox"] is False
        assert artifact.artifact_scope["is_production_case"] is False
        assert artifact.artifact_paths["public_url"] is None
        assert all(artifact.export_sections.values())
        assert artifact.source_and_scope["provider_output_evidence_not_truth"] is True
        assert artifact.source_and_scope["not_official_verification"] is True
        assert artifact.source_and_scope["not_full_web_coverage"] is True
        assert artifact.source_and_scope["not_full_platform_coverage"] is True
        assert artifact.source_and_scope["not_full_thread_coverage"] is True
        assert artifact.downstream_flags["b_end_report_ready"] is False
        assert artifact.downstream_flags["sandbox_ready"] is False
        assert artifact.downstream_flags["public_event_ready"] is False
        assert artifact.required_next_gates["b_end_report_gate"] is True
        assert artifact.required_next_gates["sandbox_generation_gate"] is True
        assert artifact.required_next_gates["public_event_generation_gate"] is True
        assert artifact.audit_refs["export_gate_audit_ids"] == [export_gate_audit.export_gate_audit_id]
        assert artifact.audit_refs["final_summary_report_audit_ids"]
        assert all(item.governance.analysis_included is False for item in item_batch.items)

        serialized = json.dumps(artifact.model_dump(mode="json"), ensure_ascii=False)
        assert "Provider output is evidence, not truth" in serialized
        assert "official verification" in serialized
        assert "full-web" in serialized
        assert "full-platform" in serialized
        assert "full-thread" in serialized
        assert "Weak evidence remains warning-marked" in serialized
        assert "Rejected evidence remains excluded" in serialized
        assert "Duplicate evidence" in serialized
        assert '"raw_author_id"' not in serialized
        assert '"raw_author_name"' not in serialized
        assert '"profile_url"' not in serialized

    listed = analysis_request_store.list_final_summary_report_export_artifacts(record.request_id)
    audits = analysis_request_store.list_final_summary_report_export_artifact_audits(record.request_id)
    assert {item.export_artifact_id for item in listed} == {item.export_artifact_id for item in created}
    assert len(audits) == 3
    assert {audit.export_artifact_id for audit in audits} == {item.export_artifact_id for item in created}
    assert all(audit.analysis_effect == "local_export_artifact_created_no_b_end_no_sandbox_no_public_event" for audit in audits)
    assert all(audit.now_flags["b_end_report_now"] is False for audit in audits)
    assert all(audit.now_flags["generate_sandbox_now"] is False for audit in audits)
    assert all(audit.now_flags["generate_public_event_now"] is False for audit in audits)
    assert all(audit.now_flags["write_evidence_layer_now"] is False for audit in audits)
    assert all(audit.now_flags["create_production_case_now"] is False for audit in audits)
    assert all(audit.now_flags["call_llm_now"] is False for audit in audits)
    assert all(audit.now_flags["fetch_url_now"] is False for audit in audits)
    assert all(audit.now_flags["read_original_rows_now"] is False for audit in audits)
    assert not list(tmp_path.rglob("*.pdf"))
    assert not list(tmp_path.rglob("*.pptx"))
    assert not (tmp_path / "b_end_reports").exists()
    assert not (tmp_path / "sandbox_fixtures").exists()
    assert not (tmp_path / "public_events").exists()
    assert not (tmp_path / "production_cases").exists()


def test_final_summary_report_export_runtime_blocks_unsafe_requests(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Export artifact blockers")))
    (
        queue_init,
        _item_batch,
        _promotion_gate,
        _manual_trigger,
        _boundary_gate,
        _execution,
        _candidate,
        _report_gate,
        _summary_candidate,
        _final_review_gate,
        final_report,
        _final_report_audit,
        export_gate,
        export_gate_audit,
    ) = create_final_summary_report_export_artifact_ready_chain(tmp_path, record.request_id)
    base_payload = final_summary_report_export_artifact_payload(
        final_summary_report_id=final_report.final_summary_report_id,
        export_gate_id=export_gate.export_gate_id,
        export_gate_audit_id=export_gate_audit.export_gate_audit_id,
        review_case_id=queue_init.review_case_id,
    )

    unsafe_payloads = [
        {**base_payload, "final_summary_report_id": ""},
        {**base_payload, "export_gate_id": ""},
        {**base_payload, "export_gate_audit_id": ""},
        {**base_payload, "reviewer_label": ""},
        {**base_payload, "note": ""},
        {**base_payload, "artifact_type": "executive_pdf"},
        {**base_payload, "artifact_format": "pptx"},
        {**base_payload, "local_runtime_path": "../escape.md"},
        {**base_payload, "acknowledge_export_artifact_only": False},
        {**base_payload, "acknowledge_no_b_end_report": False},
        {**base_payload, "acknowledge_no_sandbox_or_public_event": False},
        {**base_payload, "acknowledge_no_evidence_layer_write": False},
        {**base_payload, "acknowledge_no_production_case": False},
        {**base_payload, "acknowledge_provider_output_is_evidence_not_truth": False},
        {**base_payload, "acknowledge_not_official_verification": False},
        {**base_payload, "acknowledge_not_full_web_coverage": False},
        {**base_payload, "acknowledge_weak_evidence_warning": False},
        {**base_payload, "acknowledge_rejected_exclusion": False},
        {**base_payload, "acknowledge_dedup_no_risk_amplification": False},
        {**base_payload, "acknowledge_audit_trace_required": False},
        {**base_payload, "b_end_report_now": True},
        {**base_payload, "sandbox_now": True},
        {**base_payload, "public_event_now": True},
        {**base_payload, "write_evidence_layer_now": True},
        {**base_payload, "create_production_case_now": True},
        {**base_payload, "read_original_rows_now": True},
        {**base_payload, "fetch_url_now": True},
        {**base_payload, "call_llm_now": True},
        {**base_payload, "include_rejected_evidence": True},
        {**base_payload, "remove_weak_warnings": True},
        {**base_payload, "duplicates_amplify_risk": True},
        {**base_payload, "provider_output_is_truth": True},
        {**base_payload, "official_verification": True},
        {**base_payload, "full_web_coverage": True},
        {**base_payload, "raw_author_id": "unsafe"},
    ]
    for payload in unsafe_payloads:
        try:
            analysis_request_store.create_final_summary_report_export_artifact(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - each unsafe payload should block.
            assert "export artifact" in str(exc).lower() or "export" in str(exc).lower()
        else:
            raise AssertionError(f"unsafe final summary report export artifact payload should block: {payload}")

    gate_path = tmp_path / "final_summary_report_export_gates" / f"{record.request_id}_{export_gate.export_gate_id}.json"
    gate_data = json.loads(gate_path.read_text(encoding="utf-8"))
    gate_data["status"] = "blocked"
    gate_path.write_text(json.dumps(gate_data), encoding="utf-8")
    try:
        analysis_request_store.create_final_summary_report_export_artifact(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - non-ready export gate should block.
        assert "export gate" in str(exc).lower() and "ready" in str(exc).lower()
    else:
        raise AssertionError("non-ready final summary report export gate should block artifact runtime")


def test_final_summary_report_export_runtime_does_not_parse_original_package_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Export artifact no row parse")))
    (
        queue_init,
        _item_batch,
        _promotion_gate,
        _manual_trigger,
        _boundary_gate,
        _execution,
        _candidate,
        _report_gate,
        _summary_candidate,
        _final_review_gate,
        final_report,
        _final_report_audit,
        export_gate,
        export_gate_audit,
    ) = create_final_summary_report_export_artifact_ready_chain(tmp_path, record.request_id)
    forbidden_row_file = tmp_path / "many_safe_real_preview_package" / "evidence_items.jsonl"
    assert forbidden_row_file.exists()
    forbidden_row_file.write_text(
        '{"raw_author_id":"must_not_be_read_by_export_runtime","profile_url":"https://forbidden.example/profile","body_text":"unsafe row"}\n{broken',
        encoding="utf-8",
    )

    artifact = analysis_request_store.create_final_summary_report_export_artifact(
        record.request_id,
        final_summary_report_export_artifact_payload(
            final_summary_report_id=final_report.final_summary_report_id,
            export_gate_id=export_gate.export_gate_id,
            export_gate_audit_id=export_gate_audit.export_gate_audit_id,
            review_case_id=queue_init.review_case_id,
            artifact_type="evidence_appendix_package",
        ),
    )
    local_path = artifact.artifact_paths["local_runtime_path"]
    artifact_file = tmp_path / Path(local_path).relative_to("runtime/analysis_requests")
    artifact_text = artifact_file.read_text(encoding="utf-8")
    serialized = json.dumps(artifact.model_dump(mode="json"), ensure_ascii=False) + artifact_text

    assert artifact.status == "export_artifact_created"
    assert "must_not_be_read_by_export_runtime" not in serialized
    assert "forbidden.example" not in serialized


def create_report_export_download_package_gate_ready_chain(tmp_path: Path, request_id: str):
    (
        queue_init,
        item_batch,
        promotion_gate,
        manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
        final_report,
        final_report_audit,
        export_gate,
        export_gate_audit,
    ) = create_final_summary_report_export_artifact_ready_chain(tmp_path, request_id)
    artifact = analysis_request_store.create_final_summary_report_export_artifact(
        request_id,
        final_summary_report_export_artifact_payload(
            final_summary_report_id=final_report.final_summary_report_id,
            export_gate_id=export_gate.export_gate_id,
            export_gate_audit_id=export_gate_audit.export_gate_audit_id,
            review_case_id=queue_init.review_case_id,
            artifact_type="analyst_markdown",
        ),
    )
    artifact_audit = analysis_request_store.list_final_summary_report_export_artifact_audits(request_id)[0]
    return (
        queue_init,
        item_batch,
        promotion_gate,
        manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
        final_report,
        final_report_audit,
        export_gate,
        export_gate_audit,
        artifact,
        artifact_audit,
    )


def test_report_export_download_package_gate_runtime_creates_gate_and_audit(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Download package gate runtime")))
    (
        queue_init,
        _item_batch,
        _promotion_gate,
        _manual_trigger,
        _boundary_gate,
        _execution,
        _candidate,
        _report_gate,
        _summary_candidate,
        _final_review_gate,
        final_report,
        _final_report_audit,
        export_gate,
        _export_gate_audit,
        artifact,
        artifact_audit,
    ) = create_report_export_download_package_gate_ready_chain(tmp_path, record.request_id)

    expected_statuses = {
        "approve_for_future_download_package_runtime": "ready_for_future_download_package_runtime",
        "request_revision": "needs_revision",
        "block": "blocked",
        "privacy_hold": "privacy_hold",
    }
    created = []
    for decision, expected_status in expected_statuses.items():
        gate = analysis_request_store.create_report_export_download_package_gate(
            record.request_id,
            report_export_download_package_gate_payload(
                export_artifact_id=artifact.export_artifact_id,
                export_artifact_audit_id=artifact_audit.export_artifact_audit_id,
                final_summary_report_id=final_report.final_summary_report_id,
                export_gate_id=export_gate.export_gate_id,
                review_case_id=queue_init.review_case_id,
                delivery_decision=decision,
                required_revisions=["Clarify delivery boundary."] if decision == "request_revision" else [],
            ),
        )
        created.append(gate)

        assert gate.schema_ == "sentigraph_report_export_download_package_gate_v1"
        assert gate.status == expected_status
        assert gate.delivery_decision == decision
        assert gate.allowed_future_delivery["local_metadata_download_candidate"] is True
        assert gate.allowed_future_delivery["local_file_download_candidate"] is True
        assert gate.allowed_future_delivery["zip_package_candidate"] is True
        assert gate.allowed_future_delivery["signed_url_candidate"] is False
        assert gate.allowed_future_delivery["public_url_candidate"] is False
        assert gate.not_allowed_now["download_route_now"] is True
        assert gate.not_allowed_now["zip_package_now"] is True
        assert gate.not_allowed_now["public_url_now"] is True
        assert gate.not_allowed_now["signed_url_now"] is True
        assert gate.not_allowed_now["b_end_report_now"] is True
        assert gate.not_allowed_now["sandbox_now"] is True
        assert gate.not_allowed_now["public_event_now"] is True
        assert gate.input_boundary["source"] == "final_summary_report_export_artifact"
        assert gate.input_boundary["read_runtime_file_content_now"] is False
        assert gate.input_boundary["read_original_package_rows_now"] is False
        assert gate.input_boundary["call_llm_now"] is False
        assert gate.input_boundary["call_external_api_now"] is False
        assert gate.input_boundary["write_evidence_layer_now"] is False
        assert gate.input_boundary["create_production_case_now"] is False
        assert gate.delivery_boundary["runtime_path_only"] is True
        assert gate.delivery_boundary["public_url"] is False
        assert gate.delivery_boundary["download_requires_future_runtime"] is True
        assert gate.delivery_boundary["package_requires_future_runtime"] is True
        assert gate.delivery_boundary["human_review_required"] is True
        assert gate.downstream_readiness["can_run_future_download_package_runtime"] is (
            decision == "approve_for_future_download_package_runtime"
        )
        assert gate.downstream_readiness["can_generate_download_now"] is False
        assert gate.downstream_readiness["can_generate_package_now"] is False
        assert gate.downstream_readiness["can_generate_b_end_report_now"] is False
        assert gate.downstream_readiness["can_generate_sandbox_now"] is False
        assert gate.downstream_readiness["can_generate_public_event_now"] is False
        assert gate.downstream_readiness["requires_b_end_report_gate"] is True
        assert gate.downstream_readiness["requires_sandbox_gate"] is True
        assert gate.downstream_readiness["requires_public_event_gate"] is True
        assert gate.audit_refs["export_artifact_audit_ids"] == [artifact_audit.export_artifact_audit_id]
        assert gate.audit_refs["export_gate_ids"] == [export_gate.export_gate_id]
        assert "Provider output is evidence, not truth" in json.dumps(gate.model_dump(mode="json"), ensure_ascii=False)
        assert "official verification" in json.dumps(gate.model_dump(mode="json"), ensure_ascii=False)
        assert "full-web" in json.dumps(gate.model_dump(mode="json"), ensure_ascii=False)
        assert "Weak evidence remains warning-marked" in json.dumps(gate.model_dump(mode="json"), ensure_ascii=False)
        assert "Rejected evidence remains excluded" in json.dumps(gate.model_dump(mode="json"), ensure_ascii=False)
        assert "Duplicate evidence" in json.dumps(gate.model_dump(mode="json"), ensure_ascii=False)

    listed = analysis_request_store.list_report_export_download_package_gates(record.request_id)
    audits = analysis_request_store.list_report_export_download_package_gate_audits(record.request_id)
    assert {gate.download_package_gate_id for gate in listed} == {gate.download_package_gate_id for gate in created}
    assert len(audits) == 4
    assert {audit.download_package_gate_id for audit in audits} == {gate.download_package_gate_id for gate in created}
    assert all(audit.analysis_effect == "report_export_download_package_gate_record_only_no_download_or_package_generated" for audit in audits)
    assert all(audit.now_flags["download_route_now"] is False for audit in audits)
    assert all(audit.now_flags["zip_package_now"] is False for audit in audits)
    assert all(audit.now_flags["public_url_now"] is False for audit in audits)
    assert all(audit.now_flags["signed_url_now"] is False for audit in audits)
    assert all(audit.now_flags["b_end_report_now"] is False for audit in audits)
    assert all(audit.now_flags["generate_sandbox_now"] is False for audit in audits)
    assert all(audit.now_flags["generate_public_event_now"] is False for audit in audits)
    assert all(audit.now_flags["write_evidence_layer_now"] is False for audit in audits)
    assert all(audit.now_flags["create_production_case_now"] is False for audit in audits)
    assert all(audit.now_flags["read_runtime_file_content_now"] is False for audit in audits)
    assert all(audit.now_flags["read_original_rows_now"] is False for audit in audits)
    assert all(audit.now_flags["call_llm_now"] is False for audit in audits)
    assert all(audit.now_flags["fetch_url_now"] is False for audit in audits)
    assert not list(tmp_path.rglob("*.zip"))
    assert not (tmp_path / "download_routes").exists()
    assert not (tmp_path / "report_export_download_packages").exists()
    assert not (tmp_path / "b_end_reports").exists()
    assert not (tmp_path / "sandbox_fixtures").exists()
    assert not (tmp_path / "public_events").exists()
    assert not (tmp_path / "production_cases").exists()


def test_report_export_download_package_gate_blocks_unsafe_requests_and_metadata(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Download package blockers")))
    (
        queue_init,
        _item_batch,
        _promotion_gate,
        _manual_trigger,
        _boundary_gate,
        _execution,
        _candidate,
        _report_gate,
        _summary_candidate,
        _final_review_gate,
        final_report,
        _final_report_audit,
        export_gate,
        _export_gate_audit,
        artifact,
        artifact_audit,
    ) = create_report_export_download_package_gate_ready_chain(tmp_path, record.request_id)
    base_payload = report_export_download_package_gate_payload(
        export_artifact_id=artifact.export_artifact_id,
        export_artifact_audit_id=artifact_audit.export_artifact_audit_id,
        final_summary_report_id=final_report.final_summary_report_id,
        export_gate_id=export_gate.export_gate_id,
        review_case_id=queue_init.review_case_id,
    )

    unsafe_payloads = [
        {**base_payload, "export_artifact_id": ""},
        {**base_payload, "export_artifact_audit_id": ""},
        {**base_payload, "final_summary_report_id": ""},
        {**base_payload, "export_gate_id": ""},
        {**base_payload, "review_case_id": ""},
        {**base_payload, "reviewer_label": ""},
        {**base_payload, "note": ""},
        {**base_payload, "delivery_decision": "request_revision", "required_revisions": []},
        {**base_payload, "acknowledge_download_package_gate_only": False},
        {**base_payload, "acknowledge_no_download_route_now": False},
        {**base_payload, "acknowledge_no_package_or_zip_now": False},
        {**base_payload, "acknowledge_no_public_or_signed_url_now": False},
        {**base_payload, "acknowledge_no_b_end_report": False},
        {**base_payload, "acknowledge_no_sandbox_or_public_event": False},
        {**base_payload, "acknowledge_no_evidence_layer_write": False},
        {**base_payload, "acknowledge_no_production_case": False},
        {**base_payload, "acknowledge_provider_output_is_evidence_not_truth": False},
        {**base_payload, "acknowledge_not_official_verification": False},
        {**base_payload, "acknowledge_not_full_web_coverage": False},
        {**base_payload, "acknowledge_weak_evidence_warning": False},
        {**base_payload, "acknowledge_rejected_exclusion": False},
        {**base_payload, "acknowledge_dedup_no_risk_amplification": False},
        {**base_payload, "acknowledge_audit_trace_required": False},
        {**base_payload, "download_route_now": True},
        {**base_payload, "zip_package_now": True},
        {**base_payload, "package_now": True},
        {**base_payload, "public_url_now": True},
        {**base_payload, "signed_url_now": True},
        {**base_payload, "b_end_report_now": True},
        {**base_payload, "sandbox_now": True},
        {**base_payload, "public_event_now": True},
        {**base_payload, "write_evidence_layer_now": True},
        {**base_payload, "create_production_case_now": True},
        {**base_payload, "read_runtime_file_content_now": True},
        {**base_payload, "read_original_rows_now": True},
        {**base_payload, "fetch_url_now": True},
        {**base_payload, "call_llm_now": True},
        {**base_payload, "provider_execution_requested": True},
        {**base_payload, "collector_job_requested": True},
        {**base_payload, "remove_weak_warnings": True},
        {**base_payload, "include_rejected_evidence": True},
        {**base_payload, "duplicates_amplify_risk": True},
        {**base_payload, "provider_output_is_truth": True},
        {**base_payload, "official_verification": True},
        {**base_payload, "full_web_coverage": True},
        {**base_payload, "raw_author_id": "unsafe"},
    ]
    for payload in unsafe_payloads:
        try:
            analysis_request_store.create_report_export_download_package_gate(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - each unsafe payload should block.
            assert "download/package" in str(exc).lower() or "download package" in str(exc).lower() or "export artifact" in str(exc).lower()
        else:
            raise AssertionError(f"unsafe report export download/package payload should block: {payload}")

    artifact_path = tmp_path / "final_summary_report_export_artifacts" / f"{record.request_id}_{artifact.export_artifact_id}.json"
    artifact_data = json.loads(artifact_path.read_text(encoding="utf-8"))
    metadata_mutations = [
        ("status", "blocked"),
        ("artifact_paths", {"local_runtime_path": "../escape.md", "public_url": None}),
        ("artifact_paths", {"local_runtime_path": artifact.artifact_paths["local_runtime_path"], "public_url": "https://public.example/report"}),
        ("artifact_scope", {**artifact.artifact_scope, "is_b_end_report": True}),
        ("export_sections", {**artifact.export_sections, "boundary_block": False}),
        ("source_and_scope", {**artifact.source_and_scope, "not_official_verification": False}),
        ("downstream_flags", {**artifact.downstream_flags, "b_end_report_ready": True}),
        ("warnings", []),
        ("boundary_notes", ["Provider output is truth. Official verification. Full-web coverage."]),
        ("raw_author_id", "unsafe"),
    ]
    for key, value in metadata_mutations:
        mutated = dict(artifact_data)
        mutated[key] = value
        artifact_path.write_text(json.dumps(mutated), encoding="utf-8")
        try:
            analysis_request_store.create_report_export_download_package_gate(record.request_id, base_payload)
        except Exception as exc:  # noqa: BLE001 - unsafe artifact metadata should block.
            assert "export artifact" in str(exc).lower() or "download/package" in str(exc).lower()
        else:
            raise AssertionError(f"unsafe export artifact metadata should block: {key}={value}")
    artifact_path.write_text(json.dumps(artifact_data), encoding="utf-8")

    audit_path = tmp_path / "final_summary_report_export_artifact_audits" / (
        f"{record.request_id}_{artifact.export_artifact_id}_{artifact_audit.export_artifact_audit_id}.json"
    )
    audit_backup = audit_path.read_text(encoding="utf-8")
    audit_path.unlink()
    try:
        analysis_request_store.create_report_export_download_package_gate(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - missing audit should block.
        assert "artifact audit" in str(exc).lower()
    else:
        raise AssertionError("missing export artifact audit should block download/package gate")
    audit_path.write_text(audit_backup, encoding="utf-8")

    export_gate_path = tmp_path / "final_summary_report_export_gates" / f"{record.request_id}_{export_gate.export_gate_id}.json"
    export_gate_data = json.loads(export_gate_path.read_text(encoding="utf-8"))
    export_gate_data["status"] = "blocked"
    export_gate_path.write_text(json.dumps(export_gate_data), encoding="utf-8")
    try:
        analysis_request_store.create_report_export_download_package_gate(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - non-ready export gate should block.
        assert "export gate" in str(exc).lower() and "ready" in str(exc).lower()
    else:
        raise AssertionError("non-ready export gate should block download/package gate")


def test_report_export_download_package_gate_does_not_read_artifact_file_content(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Download package no file read")))
    (
        queue_init,
        _item_batch,
        _promotion_gate,
        _manual_trigger,
        _boundary_gate,
        _execution,
        _candidate,
        _report_gate,
        _summary_candidate,
        _final_review_gate,
        final_report,
        _final_report_audit,
        export_gate,
        _export_gate_audit,
        artifact,
        artifact_audit,
    ) = create_report_export_download_package_gate_ready_chain(tmp_path, record.request_id)
    artifact_file = tmp_path / Path(artifact.artifact_paths["local_runtime_path"]).relative_to("runtime/analysis_requests")
    artifact_file.write_text(
        "raw_author_id=must_not_be_read_by_download_gate\nprofile_url=https://forbidden.example/profile\n{broken",
        encoding="utf-8",
    )

    gate = analysis_request_store.create_report_export_download_package_gate(
        record.request_id,
        report_export_download_package_gate_payload(
            export_artifact_id=artifact.export_artifact_id,
            export_artifact_audit_id=artifact_audit.export_artifact_audit_id,
            final_summary_report_id=final_report.final_summary_report_id,
            export_gate_id=export_gate.export_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    audits = analysis_request_store.list_report_export_download_package_gate_audits(record.request_id)
    serialized = json.dumps(gate.model_dump(mode="json"), ensure_ascii=False)
    serialized += json.dumps([audit.model_dump(mode="json") for audit in audits], ensure_ascii=False)

    assert gate.status == "ready_for_future_download_package_runtime"
    assert "must_not_be_read_by_download_gate" not in serialized
    assert "forbidden.example" not in serialized
    assert not list(tmp_path.rglob("*.zip"))
    assert not (tmp_path / "report_export_download_packages").exists()


def create_report_export_download_package_artifact_ready_chain(tmp_path: Path, request_id: str):
    (
        queue_init,
        item_batch,
        promotion_gate,
        manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
        final_report,
        final_report_audit,
        export_gate,
        export_gate_audit,
        artifact,
        artifact_audit,
    ) = create_report_export_download_package_gate_ready_chain(tmp_path, request_id)
    gate = analysis_request_store.create_report_export_download_package_gate(
        request_id,
        report_export_download_package_gate_payload(
            export_artifact_id=artifact.export_artifact_id,
            export_artifact_audit_id=artifact_audit.export_artifact_audit_id,
            final_summary_report_id=final_report.final_summary_report_id,
            export_gate_id=export_gate.export_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    gate_audit = analysis_request_store.list_report_export_download_package_gate_audits_for_gate(
        request_id,
        gate.download_package_gate_id,
    )[0]
    return (
        queue_init,
        item_batch,
        promotion_gate,
        manual_trigger,
        boundary_gate,
        execution,
        candidate,
        report_gate,
        summary_candidate,
        final_review_gate,
        final_report,
        final_report_audit,
        export_gate,
        export_gate_audit,
        artifact,
        artifact_audit,
        gate,
        gate_audit,
    )


def test_report_export_download_package_runtime_creates_manifest_artifact_and_audit(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Download package artifact runtime")))
    (
        queue_init,
        item_batch,
        _promotion_gate,
        _manual_trigger,
        _boundary_gate,
        _execution,
        _candidate,
        _report_gate,
        _summary_candidate,
        _final_review_gate,
        final_report,
        _final_report_audit,
        export_gate,
        _export_gate_audit,
        artifact,
        _artifact_audit,
        gate,
        gate_audit,
    ) = create_report_export_download_package_artifact_ready_chain(tmp_path, record.request_id)

    package_artifact = analysis_request_store.create_report_export_download_package_artifact(
        record.request_id,
        report_export_download_package_artifact_payload(
            download_package_gate_id=gate.download_package_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )

    manifest_ref = package_artifact.manifest_runtime_ref
    manifest_file = tmp_path / Path(manifest_ref).relative_to("runtime/analysis_requests")
    boundary_file = manifest_file.parent / "boundary.json"
    readme_file = manifest_file.parent / "README.md"
    manifest_payload = json.loads(manifest_file.read_text(encoding="utf-8"))
    serialized = json.dumps(package_artifact.model_dump(mode="json"), ensure_ascii=False)
    serialized += json.dumps(manifest_payload, ensure_ascii=False)

    assert package_artifact.schema_ == "sentigraph_report_export_download_package_artifact_v1"
    assert package_artifact.package_status == "local_manifest_ready"
    assert package_artifact.package_type == "report_export_download_package_artifact"
    assert package_artifact.package_version == "sentigraph_report_export_download_package_artifact_v1"
    assert package_artifact.package_mode == "local_manifest_only"
    assert package_artifact.download_package_gate_id == gate.download_package_gate_id
    assert package_artifact.final_summary_report_export_artifact_ids == [artifact.export_artifact_id]
    assert package_artifact.final_summary_report_id == final_report.final_summary_report_id
    assert package_artifact.final_summary_report_export_gate_id == export_gate.export_gate_id
    assert manifest_ref.startswith(f"runtime/analysis_requests/report_export_download_packages/{record.request_id}/")
    assert manifest_ref.endswith("/manifest.json")
    assert not Path(manifest_ref).is_absolute()
    assert len(manifest_ref) < 260 or ":" not in manifest_ref[:3]
    assert manifest_file.exists()
    assert boundary_file.exists()
    assert readme_file.exists()
    assert manifest_file.resolve().is_relative_to((tmp_path / "report_export_download_packages").resolve())
    assert package_artifact.manifest_summary["artifact_count"] == 1
    assert package_artifact.manifest_summary["contains_public_url"] is False
    assert package_artifact.manifest_summary["contains_signed_url"] is False
    assert package_artifact.manifest_summary["contains_download_route"] is False
    assert package_artifact.manifest_summary["contains_raw_author_identifier"] is False
    assert package_artifact.manifest_summary["contains_secret_like_value"] is False
    assert package_artifact.file_inventory_summary["absolute_paths_exposed"] is False
    assert package_artifact.file_inventory_summary["file_bytes_exposed"] is False
    assert package_artifact.boundary_block["creates_download_route_now"] is False
    assert package_artifact.boundary_block["returns_file_bytes_now"] is False
    assert package_artifact.boundary_block["generates_public_url_now"] is False
    assert package_artifact.boundary_block["generates_signed_url_now"] is False
    assert package_artifact.boundary_block["generates_zip_now"] is False
    assert package_artifact.boundary_block["generates_binary_archive_now"] is False
    assert package_artifact.boundary_block["exposes_runtime_file_now"] is False
    assert package_artifact.boundary_block["exposes_absolute_path_now"] is False
    assert package_artifact.boundary_block["copies_artifact_file_content_now"] is False
    assert package_artifact.boundary_block["reads_artifact_file_content_now"] is False
    assert package_artifact.boundary_block["parses_artifact_file_content_now"] is False
    assert package_artifact.boundary_block["generates_local_manifest_package_now"] is True
    assert package_artifact.boundary_block["generates_b_end_report_now"] is False
    assert package_artifact.boundary_block["generates_sandbox_now"] is False
    assert package_artifact.boundary_block["generates_public_event_now"] is False
    assert package_artifact.boundary_block["writes_evidence_layer_now"] is False
    assert package_artifact.boundary_block["creates_production_case_now"] is False
    assert package_artifact.boundary_block["calls_real_api_now"] is False
    assert package_artifact.boundary_block["calls_real_llm_now"] is False
    assert package_artifact.boundary_block["fetches_url_now"] is False
    assert package_artifact.boundary_block["scrapes_now"] is False
    assert package_artifact.boundary_block["reads_original_package_rows_now"] is False
    assert "local_zip_candidate" in package_artifact.unsupported_modes
    assert "public_download_route" in package_artifact.unsupported_modes
    assert package_artifact.audit_trace["download_package_gate_audit_ids"] == [gate_audit.download_package_gate_audit_id]
    assert package_artifact.source_export_artifact_refs == [
        {
            "export_artifact_id": artifact.export_artifact_id,
            "artifact_type": artifact.artifact_type,
            "artifact_format": artifact.artifact_format,
            "status": artifact.status,
        }
    ]
    assert all(item.governance.analysis_included is False for item in item_batch.items)
    assert "Provider output is evidence, not truth" in serialized
    assert "official verification" in serialized
    assert "full-web" in serialized
    assert "Weak evidence remains warning-marked" in serialized
    assert "Rejected evidence remains excluded" in serialized
    assert "Duplicate evidence" in serialized
    assert '"raw_author_id"' not in serialized
    assert '"raw_author_name"' not in serialized
    assert '"profile_url"' not in serialized
    assert '"file_bytes"' not in serialized
    assert "signed-url-value" not in serialized

    listed = analysis_request_store.list_report_export_download_package_artifacts(record.request_id)
    all_artifacts = analysis_request_store.list_all_report_export_download_package_artifacts()
    audits = analysis_request_store.list_report_export_download_package_artifact_audits(record.request_id)
    artifact_audits = analysis_request_store.list_report_export_download_package_artifact_audits_for_artifact(
        record.request_id,
        package_artifact.package_artifact_id,
    )
    assert listed[0].package_artifact_id == package_artifact.package_artifact_id
    assert all_artifacts[0].package_artifact_id == package_artifact.package_artifact_id
    assert audits[0].package_artifact_id == package_artifact.package_artifact_id
    assert artifact_audits[0].package_artifact_id == package_artifact.package_artifact_id
    assert artifact_audits[0].analysis_effect == "local_manifest_package_created_no_download_no_zip_no_public_delivery"
    assert artifact_audits[0].now_flags["download_route_now"] is False
    assert artifact_audits[0].now_flags["return_file_bytes_now"] is False
    assert artifact_audits[0].now_flags["zip_now"] is False
    assert artifact_audits[0].now_flags["public_url_now"] is False
    assert artifact_audits[0].now_flags["signed_url_now"] is False
    assert artifact_audits[0].now_flags["read_artifact_file_content_now"] is False
    assert artifact_audits[0].now_flags["generate_b_end_report_now"] is False
    assert artifact_audits[0].now_flags["generate_sandbox_now"] is False
    assert artifact_audits[0].now_flags["generate_public_event_now"] is False
    assert artifact_audits[0].now_flags["write_evidence_layer_now"] is False
    assert artifact_audits[0].now_flags["create_production_case_now"] is False
    assert artifact_audits[0].now_flags["call_llm_now"] is False
    assert artifact_audits[0].now_flags["fetch_url_now"] is False
    assert artifact_audits[0].now_flags["read_original_rows_now"] is False
    assert not list(tmp_path.rglob("*.zip"))
    assert not (tmp_path / "download_routes").exists()
    assert not (tmp_path / "b_end_reports").exists()
    assert not (tmp_path / "sandbox_fixtures").exists()
    assert not (tmp_path / "public_events").exists()
    assert not (tmp_path / "production_cases").exists()


def test_report_export_download_package_runtime_blocks_unsafe_payloads_and_non_ready_gate(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Download package artifact blockers")))
    (
        queue_init,
        _item_batch,
        _promotion_gate,
        _manual_trigger,
        _boundary_gate,
        _execution,
        _candidate,
        _report_gate,
        _summary_candidate,
        _final_review_gate,
        final_report,
        _final_report_audit,
        export_gate,
        _export_gate_audit,
        artifact,
        artifact_audit,
        gate,
        _gate_audit,
    ) = create_report_export_download_package_artifact_ready_chain(tmp_path, record.request_id)
    base_payload = report_export_download_package_artifact_payload(
        download_package_gate_id=gate.download_package_gate_id,
        review_case_id=queue_init.review_case_id,
    )

    unsafe_payloads = [
        {**base_payload, "download_package_gate_id": ""},
        {**base_payload, "review_case_id": ""},
        {**base_payload, "operator_label": ""},
        {**base_payload, "note": ""},
        {**base_payload, "package_mode": "local_zip_candidate"},
        {**base_payload, "acknowledge_local_manifest_only": False},
        {**base_payload, "acknowledge_no_download_route": False},
        {**base_payload, "acknowledge_no_file_bytes": False},
        {**base_payload, "acknowledge_no_zip": False},
        {**base_payload, "acknowledge_no_public_or_signed_url": False},
        {**base_payload, "acknowledge_no_runtime_file_exposure": False},
        {**base_payload, "acknowledge_no_artifact_content_read": False},
        {**base_payload, "acknowledge_no_b_end_report": False},
        {**base_payload, "acknowledge_no_sandbox_or_public_event": False},
        {**base_payload, "acknowledge_no_evidence_layer_write": False},
        {**base_payload, "acknowledge_no_production_case": False},
        {**base_payload, "acknowledge_provider_output_is_evidence_not_truth": False},
        {**base_payload, "acknowledge_not_official_verification": False},
        {**base_payload, "acknowledge_not_full_web_coverage": False},
        {**base_payload, "acknowledge_weak_evidence_warning": False},
        {**base_payload, "acknowledge_rejected_exclusion": False},
        {**base_payload, "acknowledge_dedup_no_risk_amplification": False},
        {**base_payload, "acknowledge_audit_trace_required": False},
        {**base_payload, "create_download_route_now": True},
        {**base_payload, "return_file_bytes_now": True},
        {**base_payload, "generate_public_url_now": True},
        {**base_payload, "generate_signed_url_now": True},
        {**base_payload, "generate_zip_now": True},
        {**base_payload, "generate_binary_archive_now": True},
        {**base_payload, "expose_runtime_file_now": True},
        {**base_payload, "expose_absolute_path_now": True},
        {**base_payload, "copy_artifact_file_content_now": True},
        {**base_payload, "read_artifact_file_content_now": True},
        {**base_payload, "parse_artifact_file_content_now": True},
        {**base_payload, "generate_b_end_report_now": True},
        {**base_payload, "generate_sandbox_now": True},
        {**base_payload, "generate_public_event_now": True},
        {**base_payload, "write_evidence_layer_now": True},
        {**base_payload, "create_production_case_now": True},
        {**base_payload, "call_real_api_now": True},
        {**base_payload, "call_real_llm_now": True},
        {**base_payload, "fetch_url_now": True},
        {**base_payload, "scrape_now": True},
        {**base_payload, "read_original_package_rows_now": True},
        {**base_payload, "public_url": "https://public.example/report"},
        {**base_payload, "signed_url": "signed-url-value"},
        {**base_payload, "download_url": "https://download.example/report"},
        {**base_payload, "external_delivery_url": "https://delivery.example/report"},
        {**base_payload, "zip_path": "../escape.zip"},
        {**base_payload, "package_path": "C:\\unsafe\\package"},
        {**base_payload, "manifest_runtime_ref": "../escape/manifest.json"},
        {**base_payload, "file_bytes": "unsafe"},
        {**base_payload, "raw_artifact_content": "unsafe"},
        {**base_payload, "raw_author_id": "unsafe"},
        {**base_payload, "token": "unsafe"},
        {**base_payload, "cookie": "unsafe"},
    ]
    for payload in unsafe_payloads:
        try:
            analysis_request_store.create_report_export_download_package_artifact(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - each unsafe payload should block.
            assert "download/package" in str(exc).lower() or "package artifact" in str(exc).lower()
        else:
            raise AssertionError(f"unsafe report export download/package artifact payload should block: {payload}")

    revision_gate = analysis_request_store.create_report_export_download_package_gate(
        record.request_id,
        report_export_download_package_gate_payload(
            export_artifact_id=artifact.export_artifact_id,
            export_artifact_audit_id=artifact_audit.export_artifact_audit_id,
            final_summary_report_id=final_report.final_summary_report_id,
            export_gate_id=export_gate.export_gate_id,
            review_case_id=queue_init.review_case_id,
            delivery_decision="request_revision",
            required_revisions=["Clarify local package boundary."],
        ),
    )
    try:
        analysis_request_store.create_report_export_download_package_artifact(
            record.request_id,
            report_export_download_package_artifact_payload(
                download_package_gate_id=revision_gate.download_package_gate_id,
                review_case_id=queue_init.review_case_id,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - non-ready gate should block.
        assert "download/package gate" in str(exc).lower() and "ready" in str(exc).lower()
    else:
        raise AssertionError("non-ready download/package gate should block package artifact runtime")

    gate_audit_path = next((tmp_path / "report_export_download_package_gate_audits").glob(f"{record.request_id}_{gate.download_package_gate_id}_*.json"))
    gate_audit_backup = gate_audit_path.read_text(encoding="utf-8")
    gate_audit_path.unlink()
    try:
        analysis_request_store.create_report_export_download_package_artifact(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - missing gate audit should block.
        assert "gate audit" in str(exc).lower()
    else:
        raise AssertionError("missing download/package gate audit should block package artifact runtime")
    gate_audit_path.write_text(gate_audit_backup, encoding="utf-8")


def test_report_export_download_package_runtime_does_not_read_export_artifact_file_content(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Download package artifact no content read")))
    (
        queue_init,
        _item_batch,
        _promotion_gate,
        _manual_trigger,
        _boundary_gate,
        _execution,
        _candidate,
        _report_gate,
        _summary_candidate,
        _final_review_gate,
        _final_report,
        _final_report_audit,
        _export_gate,
        _export_gate_audit,
        artifact,
        _artifact_audit,
        gate,
        _gate_audit,
    ) = create_report_export_download_package_artifact_ready_chain(tmp_path, record.request_id)
    artifact_file = tmp_path / Path(artifact.artifact_paths["local_runtime_path"]).relative_to("runtime/analysis_requests")
    artifact_file.write_text(
        "raw_artifact_content_should_not_be_read\nraw_author_id=unsafe\nprofile_url=https://forbidden.example/profile\n{broken",
        encoding="utf-8",
    )

    package_artifact = analysis_request_store.create_report_export_download_package_artifact(
        record.request_id,
        report_export_download_package_artifact_payload(
            download_package_gate_id=gate.download_package_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    manifest_file = tmp_path / Path(package_artifact.manifest_runtime_ref).relative_to("runtime/analysis_requests")
    serialized = json.dumps(package_artifact.model_dump(mode="json"), ensure_ascii=False)
    serialized += manifest_file.read_text(encoding="utf-8")

    assert package_artifact.package_status == "local_manifest_ready"
    assert "raw_artifact_content_should_not_be_read" not in serialized
    assert "forbidden.example" not in serialized
    assert not list(tmp_path.rglob("*.zip"))


def test_report_export_public_access_external_delivery_gate_creates_record_and_audit(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Public access external delivery gate"))
    )
    (
        queue_init,
        _item_batch,
        _promotion_gate,
        _manual_trigger,
        _boundary_gate,
        _execution,
        _candidate,
        _report_gate,
        _summary_candidate,
        _final_review_gate,
        final_report,
        _final_report_audit,
        _export_gate,
        _export_gate_audit,
        _artifact,
        _artifact_audit,
        package_gate,
        _package_gate_audit,
    ) = create_report_export_download_package_artifact_ready_chain(tmp_path, record.request_id)
    package_artifact = analysis_request_store.create_report_export_download_package_artifact(
        record.request_id,
        report_export_download_package_artifact_payload(
            download_package_gate_id=package_gate.download_package_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )

    gate = create_report_export_public_access_external_delivery_gate(
        record.request_id,
        report_export_public_access_external_delivery_gate_payload(
            package_artifact_id=package_artifact.package_artifact_id,
            download_package_gate_id=package_gate.download_package_gate_id,
            final_summary_report_id=final_report.final_summary_report_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    audits = list_report_export_public_access_external_delivery_gate_audits(record.request_id)
    gate_audits = analysis_request_store.list_report_export_public_access_external_delivery_gate_audits_for_gate(
        record.request_id,
        gate.public_access_delivery_gate_id,
    )
    serialized = json.dumps(gate.model_dump(mode="json"), ensure_ascii=False)

    assert gate.schema_ == "sentigraph_report_export_public_access_external_delivery_gate_v1"
    assert gate.gate_status == "ready_for_future_public_access_external_delivery_runtime"
    assert gate.access_delivery_decision == "approve_for_future_public_access_external_delivery_runtime"
    assert gate.package_artifact_id == package_artifact.package_artifact_id
    assert gate.upstream_package_artifact_status == "local_manifest_ready"
    assert gate.eligibility_summary["safe_metadata_only"] is True
    assert gate.eligibility_summary["upstream_audit_exists"] is True
    assert gate.eligibility_summary["no_public_url"] is True
    assert gate.eligibility_summary["no_signed_url"] is True
    assert gate.eligibility_summary["no_download_url"] is True
    assert gate.eligibility_summary["no_zip_or_binary_archive"] is True
    assert gate.boundary_block["creates_public_download_route_now"] is False
    assert gate.boundary_block["creates_file_byte_response_now"] is False
    assert gate.boundary_block["generates_public_url_now"] is False
    assert gate.boundary_block["generates_signed_url_now"] is False
    assert gate.boundary_block["performs_external_delivery_now"] is False
    assert gate.boundary_block["sends_email_now"] is False
    assert gate.boundary_block["uploads_to_object_storage_now"] is False
    assert gate.boundary_block["publishes_to_portal_now"] is False
    assert gate.boundary_block["exposes_runtime_file_now"] is False
    assert gate.boundary_block["exposes_absolute_path_now"] is False
    assert gate.boundary_block["exposes_manifest_file_content_now"] is False
    assert gate.boundary_block["exposes_export_artifact_content_now"] is False
    assert gate.boundary_block["reads_export_artifact_file_content_now"] is False
    assert gate.boundary_block["copies_export_artifact_content_now"] is False
    assert gate.boundary_block["generates_zip_now"] is False
    assert gate.boundary_block["generates_binary_archive_now"] is False
    assert gate.boundary_block["generates_b_end_report_now"] is False
    assert gate.boundary_block["generates_sandbox_now"] is False
    assert gate.boundary_block["generates_public_event_now"] is False
    assert gate.boundary_block["writes_evidence_layer_now"] is False
    assert gate.boundary_block["creates_production_case_now"] is False
    assert gate.boundary_block["calls_real_api_now"] is False
    assert gate.boundary_block["calls_real_llm_now"] is False
    assert gate.boundary_block["fetches_url_now"] is False
    assert gate.boundary_block["scrapes_now"] is False
    assert gate.boundary_block["reads_original_package_rows_now"] is False
    assert gate.downstream_gate_policy["requires_public_access_runtime_gate"] is True
    assert gate.downstream_gate_policy["requires_external_delivery_runtime_gate"] is True
    assert gate.downstream_gate_policy["requires_b_end_report_gate"] is True
    assert gate.downstream_gate_policy["requires_sandbox_generation_gate"] is True
    assert gate.downstream_gate_policy["requires_public_event_generation_gate"] is True
    assert "No public download route" in " ".join(gate.boundary_notes)
    assert "Provider output is evidence, not truth" in serialized
    assert "full-web" in serialized
    assert "official verification" in serialized
    assert '"raw_author_id"' not in serialized
    assert '"raw_author_name"' not in serialized
    assert '"profile_url"' not in serialized
    assert '"file_bytes"' not in serialized
    assert '"public_url": "http' not in serialized
    assert '"signed_url": "http' not in serialized
    assert audits[0].public_access_delivery_gate_id == gate.public_access_delivery_gate_id
    assert gate_audits[0].analysis_effect == "public_access_external_delivery_gate_record_only_no_public_access_or_delivery_generated"
    assert gate_audits[0].now_flags["public_download_route_now"] is False
    assert gate_audits[0].now_flags["file_byte_response_now"] is False
    assert gate_audits[0].now_flags["public_url_now"] is False
    assert gate_audits[0].now_flags["signed_url_now"] is False
    assert gate_audits[0].now_flags["external_delivery_now"] is False
    assert gate_audits[0].now_flags["email_now"] is False
    assert gate_audits[0].now_flags["object_storage_upload_now"] is False
    assert gate_audits[0].now_flags["portal_publication_now"] is False
    assert gate_audits[0].now_flags["read_export_artifact_file_content_now"] is False
    assert gate_audits[0].now_flags["generate_b_end_report_now"] is False
    assert gate_audits[0].now_flags["generate_sandbox_now"] is False
    assert gate_audits[0].now_flags["generate_public_event_now"] is False
    assert gate_audits[0].now_flags["write_evidence_layer_now"] is False
    assert gate_audits[0].now_flags["create_production_case_now"] is False
    assert read_report_export_public_access_external_delivery_gate(record.request_id, gate.public_access_delivery_gate_id).public_access_delivery_gate_id == gate.public_access_delivery_gate_id
    assert list_report_export_public_access_external_delivery_gates(record.request_id)[0].public_access_delivery_gate_id == gate.public_access_delivery_gate_id
    assert not list(tmp_path.rglob("*.zip"))
    assert not (tmp_path / "public_download_routes").exists()
    assert not (tmp_path / "file_byte_responses").exists()
    assert not (tmp_path / "external_deliveries").exists()
    assert not (tmp_path / "object_storage").exists()
    assert not (tmp_path / "portal_publications").exists()
    assert not (tmp_path / "b_end_reports").exists()
    assert not (tmp_path / "sandbox_fixtures").exists()
    assert not (tmp_path / "public_events").exists()


def test_report_export_public_access_external_delivery_gate_status_mapping_and_blockers(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    record = create_analysis_request(
        AnalysisRequestCreate(case_seed=AnalysisRequestCaseSeed(title="Public access external delivery blockers"))
    )
    (
        queue_init,
        _item_batch,
        _promotion_gate,
        _manual_trigger,
        _boundary_gate,
        _execution,
        _candidate,
        _report_gate,
        _summary_candidate,
        _final_review_gate,
        final_report,
        _final_report_audit,
        _export_gate,
        _export_gate_audit,
        _artifact,
        _artifact_audit,
        package_gate,
        _package_gate_audit,
    ) = create_report_export_download_package_artifact_ready_chain(tmp_path, record.request_id)
    package_artifact = analysis_request_store.create_report_export_download_package_artifact(
        record.request_id,
        report_export_download_package_artifact_payload(
            download_package_gate_id=package_gate.download_package_gate_id,
            review_case_id=queue_init.review_case_id,
        ),
    )
    base_payload = report_export_public_access_external_delivery_gate_payload(
        package_artifact_id=package_artifact.package_artifact_id,
        download_package_gate_id=package_gate.download_package_gate_id,
        final_summary_report_id=final_report.final_summary_report_id,
        review_case_id=queue_init.review_case_id,
    )

    revision_gate = create_report_export_public_access_external_delivery_gate(
        record.request_id,
        {**base_payload, "access_delivery_decision": "request_revision", "required_revisions": ["Clarify delivery audience."]},
    )
    blocked_gate = create_report_export_public_access_external_delivery_gate(
        record.request_id,
        {**base_payload, "access_delivery_decision": "block"},
    )
    privacy_gate = create_report_export_public_access_external_delivery_gate(
        record.request_id,
        {**base_payload, "access_delivery_decision": "privacy_hold"},
    )
    assert revision_gate.gate_status == "needs_revision"
    assert blocked_gate.gate_status == "blocked"
    assert privacy_gate.gate_status == "privacy_hold"

    unsafe_payloads = [
        {**base_payload, "package_artifact_id": ""},
        {**base_payload, "download_package_gate_id": ""},
        {**base_payload, "reviewer_label": ""},
        {**base_payload, "note": ""},
        {**base_payload, "access_delivery_decision": "request_revision", "required_revisions": []},
        {**base_payload, "acknowledge_gate_only": False},
        {**base_payload, "acknowledge_no_public_download_route": False},
        {**base_payload, "acknowledge_no_file_byte_response": False},
        {**base_payload, "acknowledge_no_zip": False},
        {**base_payload, "acknowledge_no_public_or_signed_url": False},
        {**base_payload, "acknowledge_no_external_delivery": False},
        {**base_payload, "acknowledge_no_email": False},
        {**base_payload, "acknowledge_no_object_storage": False},
        {**base_payload, "acknowledge_no_portal_publication": False},
        {**base_payload, "acknowledge_no_runtime_file_exposure": False},
        {**base_payload, "acknowledge_no_manifest_content_exposure": False},
        {**base_payload, "acknowledge_no_export_artifact_content_read": False},
        {**base_payload, "acknowledge_no_b_end_report": False},
        {**base_payload, "acknowledge_no_sandbox_or_public_event": False},
        {**base_payload, "acknowledge_no_evidence_layer_write": False},
        {**base_payload, "acknowledge_no_production_case": False},
        {**base_payload, "acknowledge_provider_output_is_evidence_not_truth": False},
        {**base_payload, "acknowledge_not_official_verification": False},
        {**base_payload, "acknowledge_not_full_web_coverage": False},
        {**base_payload, "acknowledge_downstream_gates_required": False},
        {**base_payload, "creates_public_download_route_now": True},
        {**base_payload, "creates_file_byte_response_now": True},
        {**base_payload, "generates_public_url_now": True},
        {**base_payload, "generates_signed_url_now": True},
        {**base_payload, "performs_external_delivery_now": True},
        {**base_payload, "sends_email_now": True},
        {**base_payload, "uploads_to_object_storage_now": True},
        {**base_payload, "publishes_to_portal_now": True},
        {**base_payload, "exposes_runtime_file_now": True},
        {**base_payload, "exposes_absolute_path_now": True},
        {**base_payload, "exposes_manifest_file_content_now": True},
        {**base_payload, "exposes_export_artifact_content_now": True},
        {**base_payload, "reads_export_artifact_file_content_now": True},
        {**base_payload, "copies_export_artifact_content_now": True},
        {**base_payload, "generates_zip_now": True},
        {**base_payload, "generates_binary_archive_now": True},
        {**base_payload, "generates_b_end_report_now": True},
        {**base_payload, "generates_sandbox_now": True},
        {**base_payload, "generates_public_event_now": True},
        {**base_payload, "writes_evidence_layer_now": True},
        {**base_payload, "creates_production_case_now": True},
        {**base_payload, "calls_real_api_now": True},
        {**base_payload, "calls_real_llm_now": True},
        {**base_payload, "fetches_url_now": True},
        {**base_payload, "scrapes_now": True},
        {**base_payload, "reads_original_package_rows_now": True},
        {**base_payload, "public_url": "https://public.example/report"},
        {**base_payload, "signed_url": "https://signed.example/report"},
        {**base_payload, "download_url": "https://download.example/report"},
        {**base_payload, "external_delivery_url": "https://delivery.example/report"},
        {**base_payload, "object_storage_url": "s3://unsafe/report"},
        {**base_payload, "portal_url": "https://portal.example/report"},
        {**base_payload, "file_bytes": "unsafe"},
        {**base_payload, "zip_path": "../escape.zip"},
        {**base_payload, "absolute_path": "C:\\unsafe\\report"},
        {**base_payload, "manifest_file_content": "{}"},
        {**base_payload, "raw_artifact_content": "unsafe"},
        {**base_payload, "raw_author_id": "unsafe"},
        {**base_payload, "token": "unsafe"},
        {**base_payload, "cookie": "unsafe"},
        {**base_payload, "session": "unsafe"},
    ]
    for payload in unsafe_payloads:
        try:
            create_report_export_public_access_external_delivery_gate(record.request_id, payload)
        except Exception as exc:  # noqa: BLE001 - every unsafe payload should block.
            assert "public access" in str(exc).lower() or "external delivery" in str(exc).lower()
        else:
            raise AssertionError(f"unsafe public access / external delivery payload should block: {payload}")

    package_artifact_path = tmp_path / "report_export_download_package_artifacts" / f"{record.request_id}_{package_artifact.package_artifact_id}.json"
    artifact_payload = json.loads(package_artifact_path.read_text(encoding="utf-8"))
    artifact_payload["package_status"] = "blocked"
    package_artifact_path.write_text(json.dumps(artifact_payload), encoding="utf-8")
    try:
        create_report_export_public_access_external_delivery_gate(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - non-ready package artifact should block.
        assert "package artifact" in str(exc).lower() and "ready" in str(exc).lower()
    else:
        raise AssertionError("non-ready package artifact should block public access / external delivery gate")
    artifact_payload["package_status"] = "local_manifest_ready"
    package_artifact_path.write_text(json.dumps(artifact_payload), encoding="utf-8")

    package_audit_path = next((tmp_path / "report_export_download_package_artifact_audits").glob(f"{record.request_id}_{package_artifact.package_artifact_id}_*.json"))
    package_audit_backup = package_audit_path.read_text(encoding="utf-8")
    package_audit_path.unlink()
    try:
        create_report_export_public_access_external_delivery_gate(record.request_id, base_payload)
    except Exception as exc:  # noqa: BLE001 - missing package artifact audit should block.
        assert "package artifact audit" in str(exc).lower()
    else:
        raise AssertionError("missing package artifact audit should block public access / external delivery gate")
    package_audit_path.write_text(package_audit_backup, encoding="utf-8")


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
