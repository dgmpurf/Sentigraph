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
