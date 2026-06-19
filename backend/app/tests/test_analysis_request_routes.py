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


def create_route_import_job(tmp_path: Path, title: str = "Execution preflight route") -> tuple[str, str]:
    request_id = create_route_approve_decision(tmp_path, title)
    response = client.post(f"/api/v1/analysis-requests/{request_id}/import-jobs")
    assert response.status_code == 200
    return request_id, response.json()["job_id"]


def create_route_execution_preflight(tmp_path: Path, title: str = "Row reader dry-run route") -> tuple[str, str]:
    request_id, _job_id = create_route_import_job(tmp_path, title)
    response = client.post(f"/api/v1/analysis-requests/{request_id}/execution-preflights")
    assert response.status_code == 200
    return request_id, response.json()["preflight_id"]


def create_route_real_preview_package(tmp_path: Path, *, include_rows: bool = True) -> Path:
    package_dir = tmp_path / "route_real_preview_package"
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "manifest.json").write_text(
        json.dumps({"package_name": "route_real_preview_package", "package_role": "selected_public_sample"}),
        encoding="utf-8",
    )
    (package_dir / "validation_report.json").write_text(json.dumps({"errors": 0, "warnings": 0}), encoding="utf-8")
    (package_dir / "coverage_note.md").write_text("selected sample only; not full web", encoding="utf-8")
    (package_dir / "README.md").write_text("route preview package", encoding="utf-8")
    if include_rows:
        (package_dir / "evidence_items.jsonl").write_text(
            "\n".join(
                [
                    json.dumps(
                        {
                            "platform": "synthetic_forum",
                            "evidence_type": "comment",
                            "source_url": "https://example.invalid/route-preview/1",
                            "title": "Route preview row",
                            "body_text": "Route preview body.",
                            "created_at": "2026-06-18T01:00:00Z",
                            "language": "en",
                        }
                    ),
                    json.dumps(
                        {
                            "platform": "synthetic_forum",
                            "evidence_type": "comment",
                            "source_url": "https://example.invalid/route-preview/2",
                            "title": "Forbidden route row",
                            "body_text": "Route row should be quarantined.",
                            "raw_author_id": "route-raw-author-not-returned",
                        }
                    ),
                ]
            ),
            encoding="utf-8",
        )
    return package_dir


def create_route_real_preview_chain(tmp_path: Path) -> tuple[str, str]:
    request_id = create_route_approve_decision(tmp_path, "Real package row preview route")
    package_dir = create_route_real_preview_package(tmp_path)
    preview_path = tmp_path / "import_previews" / f"{request_id}.json"
    preview = json.loads(preview_path.read_text(encoding="utf-8"))
    preview["package_reference"]["package_path"] = str(package_dir)
    preview["package_reference"]["package_name"] = package_dir.name
    preview["package_reference"]["package_role"] = "selected_public_sample"
    preview_path.write_text(json.dumps(preview), encoding="utf-8")
    job_response = client.post(f"/api/v1/analysis-requests/{request_id}/import-jobs")
    assert job_response.status_code == 200
    preflight_response = client.post(f"/api/v1/analysis-requests/{request_id}/execution-preflights")
    assert preflight_response.status_code == 200
    preflight_id = preflight_response.json()["preflight_id"]
    dry_run_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/row-reader-dry-runs",
        json={"preflight_id": preflight_id, "fixture_name": "safe_evidence_items", "max_rows": 20},
    )
    assert dry_run_response.status_code == 200
    return request_id, preflight_id


def route_real_preview_ack_payload(**overrides: object) -> dict:
    payload = {
        "acknowledge_real_package_preview": True,
        "acknowledge_no_import": True,
        "acknowledge_preview_not_representative": True,
        "acknowledge_privacy_stop": True,
    }
    payload.update(overrides)
    return payload


def route_staging_import_ack_payload(**overrides: object) -> dict:
    payload = {
        "acknowledge_review_only_staging": True,
        "acknowledge_no_evidence_layer_write": True,
        "acknowledge_no_production_case": True,
        "acknowledge_no_analysis": True,
        "acknowledge_no_report": True,
    }
    payload.update(overrides)
    return payload


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


def test_analysis_request_execution_preflight_routes_create_read_and_list(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id, job_id = create_route_import_job(tmp_path)

    post_response = client.post(f"/api/v1/analysis-requests/{request_id}/execution-preflights")
    second_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/execution-preflights",
        json={"job_id": job_id, "created_by": "second_route_reviewer"},
    )
    list_response = client.get(f"/api/v1/analysis-requests/{request_id}/execution-preflights")
    all_response = client.get("/api/v1/analysis-requests/execution-preflights")

    assert post_response.status_code == 200
    body = post_response.json()
    assert body["schema"] == "sentigraph_manual_evidence_import_execution_preflight_v1"
    assert body["job_id"] == job_id
    assert body["source"] == "manual_evidence_import_job_dry_run"
    assert body["execution_mode"] == "preflight_only"
    assert body["status"] in {"preflight_passed", "preflight_warn"}
    assert body["package_file_checks"]["row_files_opened"] is False
    assert body["package_file_checks"]["row_files_parsed"] is False
    assert body["metadata_summary"]["evidence"] == 581
    assert body["validation_summary"]["errors"] == 0
    assert body["coverage_summary"]["not_full_web"] is True
    assert body["privacy_summary"]["raw_author_ids_removed"] is True
    assert body["target_case_preflight"]["create_case_now"] is False
    assert body["target_case_preflight"]["analysis_included_default"] is False
    assert body["future_row_reader_plan"]["read_rows_now"] is False
    assert body["future_staging_plan"]["stage_rows_now"] is False
    assert body["future_staging_plan"]["analysis_included"] is False
    assert body["future_governance_plan"]["dedup_run_now"] is False
    assert body["future_governance_plan"]["review_queue_created_now"] is False
    assert body["readiness"]["can_execute_now"] is False
    assert body["safe_mode"]["evidence_rows_opened"] is False
    assert body["safe_mode"]["evidence_rows_parsed"] is False
    assert body["safe_mode"]["evidence_rows_imported"] is False
    assert body["safe_mode"]["production_case_created"] is False
    assert body["safe_mode"]["analysis_generated"] is False
    assert second_response.status_code == 200
    assert second_response.json()["preflight_id"] != body["preflight_id"]
    assert list_response.status_code == 200
    assert len(list_response.json()) == 2
    assert all_response.status_code == 200
    assert len(all_response.json()) == 2
    read_response = client.get(f"/api/v1/analysis-requests/{request_id}/execution-preflights/{body['preflight_id']}")
    assert read_response.status_code == 200
    assert read_response.json()["preflight_id"] == body["preflight_id"]
    assert "raw_author_value" not in post_response.text


def test_analysis_request_execution_preflight_route_blocks_missing_job(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id = create_route_approve_decision(tmp_path, "Preflight missing job route")

    response = client.post(f"/api/v1/analysis-requests/{request_id}/execution-preflights")

    assert response.status_code == 404
    assert "manual import job" in response.text.lower()


def test_analysis_request_execution_preflight_route_blocks_non_approve_latest_decision(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id, _job_id = create_route_import_job(tmp_path, "Preflight superseded route")
    reject_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/review-decisions",
        json=route_review_payload("reject_import", notes="Reject after job."),
    )
    assert reject_response.status_code == 200

    response = client.post(f"/api/v1/analysis-requests/{request_id}/execution-preflights")

    assert response.status_code == 400
    assert "approve_import" in response.text


def test_analysis_request_execution_preflight_route_blocks_bad_preview(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id, _job_id = create_route_import_job(tmp_path, "Preflight bad preview route")
    preview_path = tmp_path / "import_previews" / f"{request_id}.json"
    preview = json.loads(preview_path.read_text(encoding="utf-8"))
    preview["validation_summary"]["errors"] = 1
    preview_path.write_text(json.dumps(preview), encoding="utf-8")

    response = client.post(f"/api/v1/analysis-requests/{request_id}/execution-preflights")

    assert response.status_code == 400
    assert "validation errors" in response.text


def test_analysis_request_row_reader_dry_run_routes_create_read_and_list(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id, preflight_id = create_route_execution_preflight(tmp_path)

    safe_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/row-reader-dry-runs",
        json={"preflight_id": preflight_id, "fixture_name": "safe_evidence_items", "max_rows": 20},
    )
    mixed_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/row-reader-dry-runs",
        json={"preflight_id": preflight_id, "fixture_name": "mixed_evidence_items", "max_rows": 20},
    )
    list_response = client.get(f"/api/v1/analysis-requests/{request_id}/row-reader-dry-runs")
    all_response = client.get("/api/v1/analysis-requests/row-reader-dry-runs")

    assert safe_response.status_code == 200
    safe_body = safe_response.json()
    assert safe_body["schema"] == "sentigraph_evidence_row_reader_dry_run_v1"
    assert safe_body["preflight_id"] == preflight_id
    assert safe_body["execution_mode"] == "synthetic_fixture_row_reader_dry_run"
    assert safe_body["fixture_policy"]["synthetic_fixture_only"] is True
    assert safe_body["fixture_policy"]["real_provider_package_allowed"] is False
    assert safe_body["row_source"]["source_type"] == "synthetic_fixture"
    assert safe_body["row_source"]["real_package_path_used"] is False
    assert safe_body["counts"]["accepted_for_preview"] == 2
    assert safe_body["counts"]["quarantined"] == 0
    assert safe_body["counts"]["rejected"] == 0
    assert safe_body["now_flags"]["import_evidence_rows_now"] is False
    assert safe_body["now_flags"]["write_evidence_layer_now"] is False
    assert safe_body["now_flags"]["create_case_now"] is False
    assert safe_body["now_flags"]["run_analysis_now"] is False
    assert safe_body["readiness"]["can_import_now"] is False
    assert "synthetic-user-123" not in safe_response.text
    assert "Synthetic Name" not in safe_response.text
    assert "Synthetic private message" not in safe_response.text

    assert mixed_response.status_code == 200
    mixed_body = mixed_response.json()
    assert mixed_body["status"] == "warn"
    assert mixed_body["counts"]["accepted_for_preview"] == 1
    assert mixed_body["counts"]["quarantined"] == 2
    assert mixed_body["counts"]["rejected"] == 1
    assert mixed_body["privacy_scan"]["raw_author_id_detected"] == 1
    assert mixed_body["privacy_scan"]["private_message_detected"] == 1
    assert "synthetic-user-123" not in mixed_response.text
    assert "Synthetic Name" not in mixed_response.text
    assert "Synthetic private message" not in mixed_response.text

    assert list_response.status_code == 200
    assert len(list_response.json()) == 2
    assert all_response.status_code == 200
    assert len(all_response.json()) == 2
    read_response = client.get(f"/api/v1/analysis-requests/{request_id}/row-reader-dry-runs/{safe_body['dry_run_id']}")
    assert read_response.status_code == 200
    assert read_response.json()["dry_run_id"] == safe_body["dry_run_id"]


def test_analysis_request_row_reader_dry_run_route_blocks_unsafe_inputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id, preflight_id = create_route_execution_preflight(tmp_path, "Row reader route blocks")

    cases = [
        ({"preflight_id": preflight_id, "max_rows": 21}, "max_rows"),
        ({"preflight_id": preflight_id, "fixture_name": "../safe_evidence_items"}, "fixture"),
        ({"preflight_id": preflight_id, "fixture_name": "safe_evidence_items", "row_source_path": str(tmp_path / "evidence_items.jsonl")}, "synthetic fixture"),
        ({"preflight_id": preflight_id, "fixture_name": "safe_evidence_items", "now_flags": {"run_analysis_now": True}}, "now flags"),
    ]
    for payload, expected_message in cases:
        response = client.post(f"/api/v1/analysis-requests/{request_id}/row-reader-dry-runs", json=payload)
        assert response.status_code == 400
        assert expected_message in response.text

    missing_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/row-reader-dry-runs",
        json={"preflight_id": "manual_import_preflight_missing"},
    )
    assert missing_response.status_code == 404
    assert "execution preflight" in missing_response.text.lower()


def test_analysis_request_real_package_row_preview_routes_create_read_and_list(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id, preflight_id = create_route_real_preview_chain(tmp_path)

    first_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/real-package-row-previews",
        json=route_real_preview_ack_payload(max_rows=10),
    )
    second_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/real-package-row-previews",
        json=route_real_preview_ack_payload(max_rows=1),
    )
    list_response = client.get(f"/api/v1/analysis-requests/{request_id}/real-package-row-previews")
    all_response = client.get("/api/v1/analysis-requests/real-package-row-previews")

    assert first_response.status_code == 200
    body = first_response.json()
    assert body["schema"] == "sentigraph_real_package_row_preview_v1"
    assert body["preflight_id"] == preflight_id
    assert body["execution_mode"] == "real_package_row_preview_only"
    assert body["status"] == "warn"
    assert body["package_reference"]["package_name"] == "route_real_preview_package"
    assert body["limits"]["max_rows"] == 10
    assert body["limits"]["hard_max_rows"] == 20
    assert body["limits"]["full_scan"] is False
    assert body["limits"]["import_rows"] is False
    assert body["rows"]["accepted_for_preview"] == 1
    assert body["rows"]["quarantined"] == 1
    assert body["now_flags"]["import_evidence_rows_now"] is False
    assert body["now_flags"]["write_evidence_layer_now"] is False
    assert body["readiness"]["can_import_now"] is False
    assert "route-raw-author-not-returned" not in first_response.text

    assert second_response.status_code == 200
    assert second_response.json()["preview_run_id"] != body["preview_run_id"]
    assert second_response.json()["rows"]["rows_seen"] == 1
    assert list_response.status_code == 200
    assert len(list_response.json()) == 2
    assert all_response.status_code == 200
    assert len(all_response.json()) == 2
    read_response = client.get(
        f"/api/v1/analysis-requests/{request_id}/real-package-row-previews/{body['preview_run_id']}"
    )
    assert read_response.status_code == 200
    assert read_response.json()["preview_run_id"] == body["preview_run_id"]


def test_analysis_request_real_package_row_preview_route_blocks_unsafe_inputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id, _preflight_id = create_route_real_preview_chain(tmp_path)

    cases = [
        (route_real_preview_ack_payload(max_rows=21), "max_rows"),
        (route_real_preview_ack_payload(acknowledge_privacy_stop=False), "acknowledgement"),
        (route_real_preview_ack_payload(now_flags={"run_analysis_now": True}), "now flags"),
    ]
    for payload, expected_message in cases:
        response = client.post(f"/api/v1/analysis-requests/{request_id}/real-package-row-previews", json=payload)
        assert response.status_code == 400
        assert expected_message in response.text


def test_analysis_request_review_only_case_routes_create_read_and_list(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id, _preflight_id = create_route_real_preview_chain(tmp_path)
    preview_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/real-package-row-previews",
        json=route_real_preview_ack_payload(max_rows=1),
    )
    assert preview_response.status_code == 200
    preview_run_id = preview_response.json()["preview_run_id"]

    create_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/review-only-cases",
        json={"source_preview_run_id": preview_run_id, "target_case_mode": "new_review_case"},
    )
    list_response = client.get(f"/api/v1/analysis-requests/{request_id}/review-only-cases")
    all_response = client.get("/api/v1/analysis-requests/review-only-cases")

    assert create_response.status_code == 200
    body = create_response.json()
    assert body["schema"] == "sentigraph_review_only_case_v1"
    assert body["request_id"] == request_id
    assert body["source_preview_run_id"] == preview_run_id
    assert body["status"] == "staging_pending"
    assert body["visibility"] == "internal_review_only"
    assert body["analysis_included"] is False
    assert body["public_visible"] is False
    assert body["report_allowed"] is False
    assert body["sandbox_allowed"] is False
    assert body["strategy_lab_allowed"] is False
    assert body["production_case_created"] is False
    assert body["evidence_rows_imported"] is False
    assert body["evidence_layer_written"] is False
    assert body["review_queue_created"] is False
    assert body["dedup_run"] is False
    assert body["analysis_run"] is False
    assert body["governance_defaults"]["review_status"] == "review_needed"
    assert body["governance_defaults"]["verification_status"] == "source_url_provided_unverified"
    assert body["governance_defaults"]["trust_label"] == "medium_low"
    assert body["readiness"]["can_import_rows_now"] is False
    assert body["readiness"]["can_run_analysis_now"] is False
    assert body["readiness"]["can_generate_report_now"] is False
    assert body["target_case_reference"]["attach_to_production_case_now"] is False
    assert "route-raw-author-not-returned" not in create_response.text

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert all_response.status_code == 200
    assert len(all_response.json()) == 1
    read_response = client.get(f"/api/v1/analysis-requests/{request_id}/review-only-cases/{body['review_case_id']}")
    assert read_response.status_code == 200
    assert read_response.json()["review_case_id"] == body["review_case_id"]


def test_analysis_request_review_only_case_route_blocks_unsafe_inputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id, _preflight_id = create_route_real_preview_chain(tmp_path)
    preview_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/real-package-row-previews",
        json=route_real_preview_ack_payload(max_rows=1),
    )
    assert preview_response.status_code == 200
    preview_run_id = preview_response.json()["preview_run_id"]

    cases = [
        ({"source_preview_run_id": preview_run_id, "target_case_mode": "production_case"}, "target_case_mode"),
        ({"source_preview_run_id": preview_run_id, "target_case_mode": "existing_case_review_wrapper"}, "target_case_id"),
        ({"source_preview_run_id": preview_run_id, "analysis_included": True}, "analysis_included"),
        ({"source_preview_run_id": preview_run_id, "production_case_created": True}, "production_case_created"),
        ({"source_preview_run_id": preview_run_id, "evidence_rows_imported": True}, "evidence_rows_imported"),
    ]
    for payload, expected_message in cases:
        response = client.post(f"/api/v1/analysis-requests/{request_id}/review-only-cases", json=payload)
        assert response.status_code == 400
        assert expected_message in response.text

    missing_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/review-only-cases",
        json={"source_preview_run_id": "real_package_row_preview_missing"},
    )
    assert missing_response.status_code == 404
    assert "row preview" in missing_response.text.lower()


def test_analysis_request_review_only_staging_import_routes_create_read_and_list(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id, _preflight_id = create_route_real_preview_chain(tmp_path)
    preview_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/real-package-row-previews",
        json=route_real_preview_ack_payload(max_rows=1),
    )
    assert preview_response.status_code == 200
    preview_run_id = preview_response.json()["preview_run_id"]
    review_case_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/review-only-cases",
        json={"source_preview_run_id": preview_run_id, "target_case_mode": "new_review_case"},
    )
    assert review_case_response.status_code == 200
    review_case_id = review_case_response.json()["review_case_id"]

    create_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/staging-imports",
        json=route_staging_import_ack_payload(review_case_id=review_case_id, preview_run_id=preview_run_id),
    )
    list_response = client.get(f"/api/v1/analysis-requests/{request_id}/staging-imports")
    all_response = client.get("/api/v1/analysis-requests/staging-imports")

    assert create_response.status_code == 200
    body = create_response.json()
    assert body["schema"] == "sentigraph_review_only_case_staging_import_v1"
    assert body["request_id"] == request_id
    assert body["review_case_id"] == review_case_id
    assert body["source_preview_run_id"] == preview_run_id
    assert body["execution_mode"] == "review_only_redacted_preview_staging"
    assert body["status"] == "completed"
    assert body["limits"]["read_package_rows_now"] is False
    assert body["limits"]["analysis_inclusion"] is False
    assert body["target"]["production_case_created"] is False
    assert body["target"]["evidence_layer_written"] is False
    assert body["readiness"]["can_run_analysis_now"] is False
    assert body["readiness"]["requires_review_queue_phase"] is True
    assert body["counts"]["accepted_for_staging"] == 1

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert all_response.status_code == 200
    assert len(all_response.json()) == 1
    read_response = client.get(
        f"/api/v1/analysis-requests/{request_id}/staging-imports/{body['staging_import_id']}"
    )
    candidates_response = client.get(
        f"/api/v1/analysis-requests/{request_id}/staging-imports/{body['staging_import_id']}/candidates"
    )
    assert read_response.status_code == 200
    assert read_response.json()["staging_import_id"] == body["staging_import_id"]
    assert candidates_response.status_code == 200
    candidates_body = candidates_response.json()
    assert candidates_body["schema"] == "sentigraph_staged_evidence_candidate_batch_v1"
    assert len(candidates_body["candidates"]) == 1
    candidate_text = json.dumps(candidates_body, ensure_ascii=False)
    assert candidates_body["candidates"][0]["governance"]["review_status"] == "review_needed"
    assert candidates_body["candidates"][0]["governance"]["verification_status"] == "source_url_provided_unverified"
    assert candidates_body["candidates"][0]["governance"]["analysis_included"] is False
    assert candidates_body["candidates"][0]["privacy"]["from_redacted_preview"] is True
    assert "route-raw-author-not-returned" not in candidate_text


def test_analysis_request_review_only_staging_import_route_blocks_unsafe_inputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SENTIGRAPH_ANALYSIS_REQUESTS_DIR", str(tmp_path))
    request_id, _preflight_id = create_route_real_preview_chain(tmp_path)
    preview_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/real-package-row-previews",
        json=route_real_preview_ack_payload(max_rows=1),
    )
    assert preview_response.status_code == 200
    preview_run_id = preview_response.json()["preview_run_id"]
    review_case_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/review-only-cases",
        json={"source_preview_run_id": preview_run_id, "target_case_mode": "new_review_case"},
    )
    assert review_case_response.status_code == 200
    review_case_id = review_case_response.json()["review_case_id"]

    cases = [
        (route_staging_import_ack_payload(acknowledge_no_report=False), "acknowledgement", 400),
        (route_staging_import_ack_payload(package_path="runtime/private/evidence_items.jsonl"), "package_path", 400),
        (route_staging_import_ack_payload(run_analysis_now=True), "side effect", 400),
        (route_staging_import_ack_payload(target_production_case_id="case_prod_unsafe"), "production_case_id", 400),
        (
            route_staging_import_ack_payload(
                review_case_id=review_case_id,
                preview_run_id="real_package_row_preview_missing",
            ),
            "row preview",
            404,
        ),
    ]
    for payload, expected_message, expected_status in cases:
        response = client.post(f"/api/v1/analysis-requests/{request_id}/staging-imports", json=payload)
        assert response.status_code == expected_status
        assert expected_message in response.text

    first_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/staging-imports",
        json=route_staging_import_ack_payload(review_case_id=review_case_id),
    )
    duplicate_response = client.post(
        f"/api/v1/analysis-requests/{request_id}/staging-imports",
        json=route_staging_import_ack_payload(review_case_id=review_case_id),
    )
    assert first_response.status_code == 200
    assert duplicate_response.status_code == 400
    assert "already has staging import" in duplicate_response.text


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
