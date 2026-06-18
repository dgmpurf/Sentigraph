from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def route_provider_result(request_id: str, *, status: str = "validation_warn", errors: int = 0) -> dict:
    return {
        "schema": "sentigraph_provider_job_result_v1",
        "request_id": request_id,
        "provider_job_id": "provider_job_route_001",
        "provider_type": "private_collector",
        "status": status,
        "safety_status": "safe",
        "package_path": "exports/sentigraph-evidence-v1/route_package",
        "package_name": "route_package",
        "package_role": "selected_public_sample",
        "package_index_path": "exports/sentigraph-evidence-v1/package_index.json",
        "counts": {"evidence": 581, "comments": 546, "sources": 37, "roots": 35},
        "validation": {"status": "warn" if errors == 0 else "failed", "errors": errors, "warnings": 1},
        "coverage": {"coverage_level": "selected_public_sample", "not_full_web": True, "not_full_platform": True, "not_full_thread": True},
        "privacy": {"raw_author_ids_removed": True, "raw_author_names_removed": True, "profile_urls_removed": True, "private_messages_excluded": True},
    }


def route_full_review_checklist() -> dict:
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


def route_review_payload(decision: str = "approve_import", **overrides: object) -> dict:
    payload = {
        "reviewer_label": "route_reviewer",
        "decision": decision,
        "target_case_mode": "new_review_case" if decision != "reject_import" else "reject_no_case",
        "target_case_id": None,
        "notes": "Route review decision.",
        "checklist": route_full_review_checklist(),
    }
    payload.update(overrides)
    return payload


def create_route_import_preview(tmp_path: Path, title: str = "Review decision route") -> str:
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": title}},
    )
    request_id = create_response.json()["request_id"]
    result_path = tmp_path / "results" / f"{request_id}.json"
    result_path.write_text(json.dumps(route_provider_result(request_id)), encoding="utf-8")
    assert client.post(f"/api/v1/analysis-requests/{request_id}/case-draft").status_code == 200
    assert client.post(f"/api/v1/analysis-requests/{request_id}/import-plan").status_code == 200
    assert client.post(f"/api/v1/analysis-requests/{request_id}/import-preview").status_code == 200
    return request_id


def create_route_approve_decision(tmp_path: Path, title: str = "Import job route") -> str:
    request_id = create_route_import_preview(tmp_path, title)
    response = client.post(
        f"/api/v1/analysis-requests/{request_id}/review-decisions",
        json=route_review_payload("approve_import"),
    )
    assert response.status_code == 200
    return request_id


def test_analysis_request_routes_create_list_read_cancel(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))

    config_response = client.get("/api/v1/analysis-requests/config")
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={
            "case_seed": {
                "title": "Helldivers PSN request",
                "description": "Local request only.",
                "keywords": ["helldivers", "psn"],
                "negative_keywords": ["unrelated"],
                "language": ["en"],
                "event_type": "game_community_event",
                "sensitive_flags": [],
            },
            "sampling_plan": {
                "platforms": ["reddit", "steam"],
                "target_comment_count": 500,
                "target_source_count": 30,
                "max_runtime_minutes": 60,
                "sample_strategy": "stratified_public_sample",
            },
        },
    )

    assert config_response.status_code == 200
    assert config_response.json()["safe_mode"]["collector_jobs_run"] is False
    assert create_response.status_code == 200
    created = create_response.json()
    request_id = created["request_id"]
    assert created["request"]["schema"] == "sentigraph_analysis_request_v1"
    assert created["request"]["safety_policy"]["allow_live_collection"] is False
    assert created["request"]["privacy_policy"]["remove_raw_author_id"] is True

    list_response = client.get("/api/v1/analysis-requests")
    detail_response = client.get(f"/api/v1/analysis-requests/{request_id}")
    cancel_response = client.post(f"/api/v1/analysis-requests/{request_id}/cancel")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert detail_response.status_code == 200
    assert detail_response.json()["request_id"] == request_id
    assert cancel_response.status_code == 200
    assert cancel_response.json()["status"] == "canceled"
    assert cancel_response.json()["safe_mode"]["provider_cancel_called"] is False


def test_analysis_request_route_reads_manual_provider_result(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": "Provider result request"}},
    )
    request_id = create_response.json()["request_id"]
    result_path = tmp_path / "results" / f"{request_id}.json"
    result_path.write_text(
        json.dumps(
            {
                "schema": "sentigraph_provider_job_result_v1",
                "request_id": request_id,
                "provider_job_id": "provider_job_001",
                "provider_type": "private_collector",
                "status": "validation_warn",
                "safety_status": "medium",
                "package_name": "sample_package",
                "counts": {"evidence": 581, "comments": 546, "sources": 37, "roots": 35},
                "validation": {"status": "warn", "errors": 0, "warnings": 2},
            }
        ),
        encoding="utf-8",
    )

    response = client.get(f"/api/v1/analysis-requests/{request_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["provider_status"] == "validation_warn"
    assert body["safety_status"] == "medium"
    assert body["package_name"] == "sample_package"
    assert body["provider_result"]["counts"]["evidence"] == 581
    assert "raw_author_value" not in response.text


def test_analysis_request_routes_read_default_result_from_list_and_detail(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": "Default provider result route"}},
    )
    request_id = create_response.json()["request_id"]
    result_path = tmp_path / "results" / f"{request_id}.json"
    result_path.write_text(
        json.dumps(
            {
                "schema": "sentigraph_provider_job_result_v1",
                "request_id": request_id,
                "provider_job_id": "local_default_route",
                "provider_type": "private_collector",
                "status": "needs_manual_snapshot",
                "safety_status": "safe",
                "counts": {"evidence": 0, "comments": 0, "sources": 0, "roots": 0},
                "validation": {"status": "not_run", "errors": 0, "warnings": 0},
            }
        ),
        encoding="utf-8",
    )

    list_response = client.get("/api/v1/analysis-requests")
    detail_response = client.get(f"/api/v1/analysis-requests/{request_id}")

    assert list_response.status_code == 200
    assert list_response.json()[0]["provider_status"] == "needs_manual_snapshot"
    assert list_response.json()[0]["safety_status"] == "safe"
    assert detail_response.status_code == 200
    body = detail_response.json()
    assert body["result_warning"] is None
    assert body["provider_result"]["validation"]["status"] == "not_run"
    assert body["provider_result"]["counts"]["evidence"] == 0
    assert body["provider_result"]["counts"]["roots"] == 0


def test_analysis_request_route_reads_legacy_provider_result_aliases(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": "Legacy provider result route"}},
    )
    request_id = create_response.json()["request_id"]
    result_path = tmp_path / "results" / f"{request_id}.json"
    result_path.write_text(
        json.dumps(
            {
                "schema": "sentigraph_provider_job_result_v1",
                "request_id": request_id,
                "provider_job_id": "local_legacy_route",
                "provider_type": "private_collector",
                "status": "validation_warn",
                "safety_status": "safe",
                "package_name": "legacy_package",
                "counts": {"evidence_items": 581, "comments": 546, "sources": 37, "root_content": 35},
                "validation": {"status": "warn", "errors_count": 0, "warnings_count": 1},
            }
        ),
        encoding="utf-8",
    )

    response = client.get(f"/api/v1/analysis-requests/{request_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["result_warning"] is None
    assert body["provider_result"]["counts"]["evidence"] == 581
    assert body["provider_result"]["counts"]["comments"] == 546
    assert body["provider_result"]["counts"]["sources"] == 37
    assert body["provider_result"]["counts"]["roots"] == 35
    assert body["provider_result"]["validation"]["warnings"] == 1


def test_analysis_request_case_draft_routes_create_read_and_list(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": "Case draft route"}},
    )
    request_id = create_response.json()["request_id"]
    result_path = tmp_path / "results" / f"{request_id}.json"
    result_path.write_text(json.dumps(route_provider_result(request_id)), encoding="utf-8")

    post_response = client.post(f"/api/v1/analysis-requests/{request_id}/case-draft")
    get_response = client.get(f"/api/v1/analysis-requests/{request_id}/case-draft")
    list_response = client.get("/api/v1/analysis-requests/case-drafts")

    assert post_response.status_code == 200
    body = post_response.json()
    assert body["schema"] == "sentigraph_case_draft_handoff_v1"
    assert body["draft_id"] == f"draft_{request_id}"
    assert body["provider_summary"]["status"] == "validation_warn"
    assert body["package_reference"]["package_name"] == "route_package"
    assert body["counts"]["evidence"] == 581
    assert body["counts"]["roots"] == 35
    assert body["validation"]["warnings"] == 1
    assert body["readiness"]["can_import_evidence"] is False
    assert body["safe_mode"]["evidence_rows_imported"] is False
    assert get_response.status_code == 200
    assert get_response.json()["draft_id"] == body["draft_id"]
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert "raw_author_value" not in post_response.text


def test_analysis_request_case_draft_route_blocks_ineligible_result(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": "Blocked draft route"}},
    )
    request_id = create_response.json()["request_id"]
    result_path = tmp_path / "results" / f"{request_id}.json"
    result_path.write_text(json.dumps(route_provider_result(request_id, status="validation_failed", errors=2)), encoding="utf-8")

    response = client.post(f"/api/v1/analysis-requests/{request_id}/case-draft")

    assert response.status_code == 400
    assert "not eligible" in response.text


def test_analysis_request_import_plan_routes_create_read_and_list(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": "Import plan route"}},
    )
    request_id = create_response.json()["request_id"]
    result_path = tmp_path / "results" / f"{request_id}.json"
    result_path.write_text(json.dumps(route_provider_result(request_id)), encoding="utf-8")
    draft_response = client.post(f"/api/v1/analysis-requests/{request_id}/case-draft")

    post_response = client.post(f"/api/v1/analysis-requests/{request_id}/import-plan")
    get_response = client.get(f"/api/v1/analysis-requests/{request_id}/import-plan")
    list_response = client.get("/api/v1/analysis-requests/import-plans")

    assert draft_response.status_code == 200
    assert post_response.status_code == 200
    body = post_response.json()
    assert body["schema"] == "sentigraph_evidence_import_plan_v1"
    assert body["plan_id"] == f"import_plan_{request_id}"
    assert body["draft_id"] == f"draft_{request_id}"
    assert body["package_reference"]["package_name"] == "route_package"
    assert body["counts"]["evidence"] == 581
    assert body["proposed_import"]["import_evidence_rows_now"] is False
    assert body["proposed_import"]["create_case_now"] is False
    assert body["proposed_import"]["run_analysis_now"] is False
    assert body["proposed_import"]["generate_sandbox_now"] is False
    assert body["proposed_import"]["generate_report_now"] is False
    assert body["default_evidence_policy"]["review_status"] == "review_needed"
    assert body["default_evidence_policy"]["trust_label"] == "medium_low"
    assert body["readiness"]["can_import_now"] is False
    assert body["safe_mode"]["evidence_rows_imported"] is False
    assert body["safe_mode"]["production_case_created"] is False
    assert get_response.status_code == 200
    assert get_response.json()["plan_id"] == body["plan_id"]
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert "raw_author_value" not in post_response.text


def test_analysis_request_import_plan_route_blocks_without_case_draft(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": "Blocked import plan route"}},
    )
    request_id = create_response.json()["request_id"]
    result_path = tmp_path / "results" / f"{request_id}.json"
    result_path.write_text(json.dumps(route_provider_result(request_id)), encoding="utf-8")

    response = client.post(f"/api/v1/analysis-requests/{request_id}/import-plan")

    assert response.status_code == 404
    assert "case draft handoff" in response.text.lower()


def test_analysis_request_import_plan_route_blocks_bad_draft(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": "Bad import draft route"}},
    )
    request_id = create_response.json()["request_id"]
    result_path = tmp_path / "results" / f"{request_id}.json"
    result_path.write_text(json.dumps(route_provider_result(request_id)), encoding="utf-8")
    assert client.post(f"/api/v1/analysis-requests/{request_id}/case-draft").status_code == 200
    draft_path = tmp_path / "case_drafts" / f"{request_id}.json"
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    draft["validation"]["errors"] = 2
    draft_path.write_text(json.dumps(draft), encoding="utf-8")

    response = client.post(f"/api/v1/analysis-requests/{request_id}/import-plan")

    assert response.status_code == 400
    assert "validation errors" in response.text


def test_analysis_request_import_preview_routes_create_read_and_list(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": "Import preview route"}},
    )
    request_id = create_response.json()["request_id"]
    result_path = tmp_path / "results" / f"{request_id}.json"
    result_path.write_text(json.dumps(route_provider_result(request_id)), encoding="utf-8")
    assert client.post(f"/api/v1/analysis-requests/{request_id}/case-draft").status_code == 200
    assert client.post(f"/api/v1/analysis-requests/{request_id}/import-plan").status_code == 200

    post_response = client.post(f"/api/v1/analysis-requests/{request_id}/import-preview")
    get_response = client.get(f"/api/v1/analysis-requests/{request_id}/import-preview")
    list_response = client.get("/api/v1/analysis-requests/import-previews")

    assert post_response.status_code == 200
    body = post_response.json()
    assert body["schema"] == "sentigraph_evidence_import_preview_v1"
    assert body["preview_id"] == f"import_preview_{request_id}"
    assert body["plan_id"] == f"import_plan_{request_id}"
    assert body["draft_id"] == f"draft_{request_id}"
    assert body["package_reference"]["package_name"] == "route_package"
    assert body["metadata_summary"]["evidence"] == 581
    assert body["validation_summary"]["errors"] == 0
    assert body["proposed_evidence_defaults"]["review_status"] == "review_needed"
    assert body["proposed_evidence_defaults"]["verification_status"] == "source_url_provided_unverified"
    assert body["proposed_evidence_defaults"]["trust_label"] == "medium_low"
    assert body["dedup_preview"]["required"] is True
    assert body["dedup_preview"]["computed_now"] is False
    assert body["sample_preview_policy"]["read_rows_now"] is False
    assert body["readiness"]["can_import_now"] is False
    assert body["safe_mode"]["metadata_only_preview"] is True
    assert body["safe_mode"]["evidence_rows_read"] is False
    assert body["safe_mode"]["evidence_rows_parsed"] is False
    assert body["safe_mode"]["evidence_rows_imported"] is False
    assert body["safe_mode"]["production_case_created"] is False
    assert get_response.status_code == 200
    assert get_response.json()["preview_id"] == body["preview_id"]
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert "raw_author_value" not in post_response.text


def test_analysis_request_import_preview_route_blocks_without_import_plan(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": "Blocked import preview route"}},
    )
    request_id = create_response.json()["request_id"]
    result_path = tmp_path / "results" / f"{request_id}.json"
    result_path.write_text(json.dumps(route_provider_result(request_id)), encoding="utf-8")
    assert client.post(f"/api/v1/analysis-requests/{request_id}/case-draft").status_code == 200

    response = client.post(f"/api/v1/analysis-requests/{request_id}/import-preview")

    assert response.status_code == 404
    assert "evidence import plan" in response.text.lower()


def test_analysis_request_import_preview_route_blocks_bad_plan(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": "Bad import preview plan route"}},
    )
    request_id = create_response.json()["request_id"]
    result_path = tmp_path / "results" / f"{request_id}.json"
    result_path.write_text(json.dumps(route_provider_result(request_id)), encoding="utf-8")
    assert client.post(f"/api/v1/analysis-requests/{request_id}/case-draft").status_code == 200
    assert client.post(f"/api/v1/analysis-requests/{request_id}/import-plan").status_code == 200
    plan_path = tmp_path / "import_plans" / f"{request_id}.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan["proposed_import"]["import_evidence_rows_now"] = True
    plan_path.write_text(json.dumps(plan), encoding="utf-8")

    response = client.post(f"/api/v1/analysis-requests/{request_id}/import-preview")

    assert response.status_code == 400
    assert "immediate execution" in response.text


def test_analysis_request_review_decision_routes_create_read_and_list(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id = create_route_import_preview(tmp_path)

    approve_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/review-decisions",
        json=route_review_payload("approve_import"),
    )
    second_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/review-decisions",
        json=route_review_payload("request_more_source", notes="Need more source context."),
    )
    list_response = client.get(f"/api/v1/analysis-requests/{request_id}/review-decisions")
    all_response = client.get("/api/v1/analysis-requests/review-decisions")

    assert approve_response.status_code == 200
    body = approve_response.json()
    assert body["schema"] == "sentigraph_evidence_import_review_decision_v1"
    assert body["preview_id"] == f"import_preview_{request_id}"
    assert body["plan_id"] == f"import_plan_{request_id}"
    assert body["draft_id"] == f"draft_{request_id}"
    assert body["reviewer_label"] == "route_reviewer"
    assert body["decision"] == "approve_import"
    assert body["readiness"]["state"] == "approved_for_future_manual_import"
    assert body["readiness"]["can_create_import_job_now"] is False
    assert body["approved_defaults"]["review_status"] == "review_needed"
    assert body["approved_defaults"]["verification_status"] == "source_url_provided_unverified"
    assert body["approved_defaults"]["trust_label"] == "medium_low"
    assert body["safe_mode"]["evidence_rows_imported"] is False
    assert body["safe_mode"]["production_case_created"] is False
    assert body["safe_mode"]["analysis_generated"] is False
    assert second_response.status_code == 200
    assert second_response.json()["decision_id"] != body["decision_id"]
    assert list_response.status_code == 200
    assert len(list_response.json()) == 2
    assert all_response.status_code == 200
    assert len(all_response.json()) == 2
    read_response = client.get(f"/api/v1/analysis-requests/{request_id}/review-decisions/{body['decision_id']}")
    assert read_response.status_code == 200
    assert read_response.json()["decision_id"] == body["decision_id"]
    assert "raw_author_value" not in approve_response.text


def test_analysis_request_review_decision_route_blocks_without_preview(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": "Blocked review decision route"}},
    )
    request_id = create_response.json()["request_id"]

    response = client.post(
        f"/api/v1/analysis-requests/{request_id}/review-decisions",
        json=route_review_payload("reject_import"),
    )

    assert response.status_code == 404
    assert "import preview" in response.text.lower()


def test_analysis_request_review_decision_route_blocks_missing_approve_ack(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id = create_route_import_preview(tmp_path, "Missing approve ack route")
    checklist = route_full_review_checklist()
    checklist["no_auto_report_acknowledged"] = False

    response = client.post(
        f"/api/v1/analysis-requests/{request_id}/review-decisions",
        json=route_review_payload("approve_import", checklist=checklist),
    )

    assert response.status_code == 400
    assert "acknowledgements" in response.text


def test_analysis_request_review_decision_route_blocks_bad_preview(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id = create_route_import_preview(tmp_path, "Bad review preview route")
    preview_path = tmp_path / "import_previews" / f"{request_id}.json"
    preview = json.loads(preview_path.read_text(encoding="utf-8"))
    preview["coverage_summary"]["not_full_web"] = False
    preview_path.write_text(json.dumps(preview), encoding="utf-8")

    response = client.post(
        f"/api/v1/analysis-requests/{request_id}/review-decisions",
        json=route_review_payload("reject_import"),
    )

    assert response.status_code == 400
    assert "coverage" in response.text


def test_analysis_request_import_job_routes_create_read_and_list(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id = create_route_approve_decision(tmp_path)

    post_response = client.post(f"/api/v1/analysis-requests/{request_id}/import-jobs")
    second_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/import-jobs",
        json={"target_case_mode": "existing_case", "target_case_id": "case_route_existing"},
    )
    list_response = client.get(f"/api/v1/analysis-requests/{request_id}/import-jobs")
    all_response = client.get("/api/v1/analysis-requests/import-jobs")

    assert post_response.status_code == 200
    body = post_response.json()
    assert body["schema"] == "sentigraph_manual_evidence_import_job_v1"
    assert body["job_type"] == "manual_evidence_import"
    assert body["execution_mode"] == "dry_run_gate"
    assert body["status"] == "draft_not_executed"
    assert body["source"] == "human_review_decision"
    assert body["target_case"]["mode"] == "new_review_case"
    assert body["target_case"]["create_case_now"] is False
    assert body["package_reference"]["package_name"] == "route_package"
    assert body["metadata_summary"]["evidence"] == 581
    assert body["approved_defaults"]["review_status"] == "review_needed"
    assert body["approved_defaults"]["verification_status"] == "source_url_provided_unverified"
    assert body["approved_defaults"]["trust_label"] == "medium_low"
    assert body["dry_run_result"]["would_import_evidence_rows"] is True
    assert body["dry_run_result"]["import_evidence_rows_now"] is False
    assert body["dry_run_result"]["create_case_now"] is False
    assert body["dry_run_result"]["run_analysis_now"] is False
    assert body["dry_run_result"]["generate_report_now"] is False
    assert body["preflight_checks"]["approved_import_decision_present"] is True
    assert body["readiness"]["state"] == "ready_for_future_manual_import_execution"
    assert body["readiness"]["can_execute_now"] is False
    assert body["safe_mode"]["evidence_rows_read"] is False
    assert body["safe_mode"]["evidence_rows_parsed"] is False
    assert body["safe_mode"]["evidence_rows_imported"] is False
    assert body["safe_mode"]["production_case_created"] is False
    assert body["safe_mode"]["analysis_generated"] is False
    assert second_response.status_code == 200
    assert second_response.json()["job_id"] != body["job_id"]
    assert second_response.json()["target_case"]["mode"] == "existing_case"
    assert list_response.status_code == 200
    assert len(list_response.json()) == 2
    assert all_response.status_code == 200
    assert len(all_response.json()) == 2
    read_response = client.get(f"/api/v1/analysis-requests/{request_id}/import-jobs/{body['job_id']}")
    assert read_response.status_code == 200
    assert read_response.json()["job_id"] == body["job_id"]
    assert "raw_author_value" not in post_response.text


def test_analysis_request_import_job_route_blocks_without_approve_decision(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id = create_route_import_preview(tmp_path, "Job blocked no decision")

    response = client.post(f"/api/v1/analysis-requests/{request_id}/import-jobs")

    assert response.status_code == 404
    assert "review decision" in response.text.lower()


def test_analysis_request_import_job_route_blocks_non_approve_latest_decision(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id = create_route_import_preview(tmp_path, "Job blocked non approve")
    reject_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/review-decisions",
        json=route_review_payload("reject_import", notes="Reject package."),
    )
    assert reject_response.status_code == 200

    response = client.post(f"/api/v1/analysis-requests/{request_id}/import-jobs")

    assert response.status_code == 400
    assert "approve_import" in response.text


def test_analysis_request_import_job_route_blocks_existing_case_without_id(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id = create_route_approve_decision(tmp_path, "Job blocked target id")

    response = client.post(
        f"/api/v1/analysis-requests/{request_id}/import-jobs",
        json={"target_case_mode": "existing_case"},
    )

    assert response.status_code == 400
    assert "target_case_id" in response.text


def test_analysis_request_import_job_route_blocks_bad_preview(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id = create_route_approve_decision(tmp_path, "Job blocked bad preview")
    preview_path = tmp_path / "import_previews" / f"{request_id}.json"
    preview = json.loads(preview_path.read_text(encoding="utf-8"))
    preview["validation_summary"]["errors"] = 2
    preview_path.write_text(json.dumps(preview), encoding="utf-8")

    response = client.post(f"/api/v1/analysis-requests/{request_id}/import-jobs")

    assert response.status_code == 400
    assert "validation errors" in response.text


def test_analysis_request_route_invalid_result_returns_warning(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    create_response = client.post(
        "/api/v1/analysis-requests",
        json={"case_seed": {"title": "Invalid provider result"}},
    )
    request_id = create_response.json()["request_id"]
    (tmp_path / "results" / f"{request_id}.json").write_text("{broken", encoding="utf-8")

    response = client.get(f"/api/v1/analysis-requests/{request_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["provider_result"] is None
    assert body["result_warning"]
    assert body["safe_mode"]["real_api_calls"] is False
    assert body["safe_mode"]["url_fetching"] is False


def test_analysis_request_route_blocks_bad_request_id(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))

    response = client.get("/api/v1/analysis-requests/..%2Fsecret")

    assert response.status_code in {400, 404}
