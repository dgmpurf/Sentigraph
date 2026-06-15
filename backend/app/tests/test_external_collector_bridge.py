from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_external_collector_status_returns_not_configured(monkeypatch) -> None:
    monkeypatch.delenv("SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR", raising=False)

    response = client.get("/api/v1/external-collector/status")

    assert response.status_code == 200
    body = response.json()
    assert body["configured"] is False
    assert body["exists"] is False
    assert body["package_count"] == 0
    assert body["safe_mode"]["collector_jobs_run"] is False
    assert body["safe_mode"]["real_api_calls"] is False
    assert body["safe_mode"]["url_fetching"] is False


def test_external_collector_listing_and_detail_parse_temp_package(tmp_path: Path, monkeypatch) -> None:
    exports_dir = tmp_path / "exports"
    package_dir = exports_dir / "sample_package"
    _write_package(package_dir)
    monkeypatch.setenv("SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR", str(exports_dir))

    status_response = client.get("/api/v1/external-collector/status")
    packages_response = client.get("/api/v1/external-collector/packages")
    detail_response = client.get("/api/v1/external-collector/packages/sample_package")

    assert status_response.status_code == 200
    assert status_response.json()["package_count"] == 1
    assert packages_response.status_code == 200
    package = packages_response.json()[0]
    assert package["package_name"] == "sample_package"
    assert package["case_id"] == "case_bridge_demo"
    assert package["evidence_count"] == 1
    assert package["source_count"] == 1
    assert package["validation_status"] == "pass"
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["manifest_summary"]["case_id"] == "case_bridge_demo"
    assert detail["expected_files"]["manifest.json"] is True
    assert detail["safe_mode"]["full_evidence_dump_returned"] is False
    assert "comment_text" not in detail_response.text


def test_external_collector_package_index_merges_and_sorts_recommended_first(tmp_path: Path, monkeypatch) -> None:
    exports_dir = tmp_path / "exports"
    historical_dir = exports_dir / "historical_package"
    recommended_dir = exports_dir / "helldivers2-psn-demo_20260614_055754"
    _write_package(historical_dir, case_id="case_history", case_title="Historical Test", exported_at="2026-06-15T00:00:00Z")
    _write_package(recommended_dir, case_id="case_helldivers", case_title="Helldivers PSN Demo", exported_at="2026-06-14T05:57:54Z")
    (exports_dir / "package_index.json").write_text(
        json.dumps(
            {
                "packages": [
                    {
                        "package_name": "historical_package",
                        "case_id": "case_history",
                        "case_title": "Historical Test",
                        "exported_at": "2026-06-15T00:00:00Z",
                        "evidence_count": 1200,
                        "source_count": 30,
                        "comment_count": 1000,
                        "root_count": 20,
                        "validation_status": "pass",
                        "package_role": "historical_smoke_test",
                        "demo_recommendation": "not_recommended",
                        "recommended_for_sentigraph_demo": False,
                        "sample_quality_label": "historical smoke",
                        "notes": "Large historical package; not a recommended demo sample.",
                    },
                    {
                        "package_name": "helldivers2-psn-demo_20260614_055754",
                        "case_id": "case_helldivers",
                        "case_title": "Helldivers PSN Demo",
                        "exported_at": "2026-06-14T05:57:54Z",
                        "evidence_count": 34,
                        "source_count": 7,
                        "comment_count": 28,
                        "root_count": 6,
                        "validation_status": "warn",
                        "warnings_count": 2,
                        "errors_count": 0,
                        "package_role": "recommended_demo_sample",
                        "demo_recommendation": "recommended",
                        "recommended_for_sentigraph_demo": True,
                        "sample_quality_label": "selected public sample",
                        "notes": "Recommended Sentigraph demo package.",
                    },
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR", str(exports_dir))

    status_response = client.get("/api/v1/external-collector/status")
    packages_response = client.get("/api/v1/external-collector/packages")
    detail_response = client.get("/api/v1/external-collector/packages/helldivers2-psn-demo_20260614_055754")

    assert status_response.status_code == 200
    assert status_response.json()["index_available"] is True
    assert packages_response.status_code == 200
    packages = packages_response.json()
    assert [item["package_name"] for item in packages] == [
        "helldivers2-psn-demo_20260614_055754",
        "historical_package",
    ]
    recommended = packages[0]
    assert recommended["recommended_for_sentigraph_demo"] is True
    assert recommended["package_role"] == "recommended_demo_sample"
    assert recommended["demo_recommendation"] == "recommended"
    assert recommended["comment_count"] == 28
    assert recommended["root_count"] == 6
    assert "author_name" not in packages_response.text
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["package_role"] == "recommended_demo_sample"
    assert detail["index_source"] == "package_index.json"
    assert detail["index_notes"] == "Recommended Sentigraph demo package."
    assert "comment_text" not in detail_response.text


def test_external_collector_malformed_package_index_falls_back_to_folder_scan(tmp_path: Path, monkeypatch) -> None:
    exports_dir = tmp_path / "exports"
    package_dir = exports_dir / "sample_package"
    _write_package(package_dir)
    (exports_dir / "package_index.json").write_text("{not valid json", encoding="utf-8")
    monkeypatch.setenv("SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR", str(exports_dir))

    status_response = client.get("/api/v1/external-collector/status")
    packages_response = client.get("/api/v1/external-collector/packages")

    assert status_response.status_code == 200
    assert status_response.json()["index_available"] is True
    assert "could not be parsed" in status_response.json()["index_warning"]
    assert packages_response.status_code == 200
    package = packages_response.json()[0]
    assert package["package_name"] == "sample_package"
    assert package["case_id"] == "case_bridge_demo"
    assert package["index_available"] is False
    assert "could not be parsed" in package["index_warning"]


def test_external_collector_validation_rejects_forbidden_identity_keys(tmp_path: Path, monkeypatch) -> None:
    exports_dir = tmp_path / "exports"
    package_dir = exports_dir / "bad_package"
    _write_package(package_dir, forbidden_identity=True)
    monkeypatch.setenv("SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR", str(exports_dir))

    response = client.post("/api/v1/external-collector/packages/bad_package/validate")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "fail"
    assert body["privacy_status"] == "fail"
    assert any(error["code"] == "FORBIDDEN_EVIDENCE_KEY" for error in body["errors"])
    assert body["safe_mode"]["collector_jobs_run"] is False
    assert body["safe_mode"]["url_fetching"] is False
    assert body["safe_mode"]["package_code_executed"] is False


def test_external_collector_blocks_path_traversal(tmp_path: Path, monkeypatch) -> None:
    exports_dir = tmp_path / "exports"
    exports_dir.mkdir()
    monkeypatch.setenv("SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR", str(exports_dir))

    response = client.get("/api/v1/external-collector/packages/..%2Fsecret")

    assert response.status_code in {400, 404}


def _write_package(
    package_dir: Path,
    forbidden_identity: bool = False,
    case_id: str = "case_bridge_demo",
    case_title: str = "Bridge Demo Case",
    exported_at: str = "2026-06-15T00:00:00Z",
) -> None:
    package_dir.mkdir(parents=True)
    coverage = (
        "Selected public sample only; not full-web coverage; not full-platform coverage; "
        "not official verification; not causal proof."
    )
    manifest = {
        "package_version": "sentigraph_external_export_v1",
        "contract_version": "evidence_to_opinion_ecosystem_mapping_contract_v1",
        "case_id": case_id,
        "case_title": case_title,
        "exported_at": exported_at,
        "data_scope": {
            "evidence_items_count": 1,
            "source_urls_count": 1,
            "comment_sample_count": 1,
            "root_content_count": 0,
        },
        "coverage_note": coverage,
        "privacy_policy": {
            "raw_author_id_removed": True,
            "raw_author_name_removed": True,
            "author_hashing": "sha256",
        },
    }
    evidence = {
        "evidence_id": "ev_1",
        "case_id": case_id,
        "platform": "reddit",
        "source_type": "forum",
        "acquisition_mode": "manual_url",
        "provenance_type": "manual_url",
        "verification_status": "source_url_provided_unverified",
        "trust_label": "medium_low",
        "trust_score": 0.45,
        "review_status": "review_needed",
        "evidence_type": "comment",
        "title": "Sample public comment",
        "comment_text": "A safe public sample comment.",
        "language": "en",
        "source_url": "https://example.test/source",
        "url": "https://example.test/source",
        "raw_author_id_removed": True,
        "raw_author_name_removed": True,
        "duplicate_group_id": "dup_1",
        "duplicate_count": 1,
        "coverage_note": coverage,
    }
    if forbidden_identity:
        evidence["author_name"] = "should_not_export"
    source = {
        "source_id": "source_1",
        "platform": "reddit",
        "source_type": "forum",
        "source_url": "https://example.test/source",
        "collection_method": "manual_url",
        "content_visibility": "public",
        "access_scope": "public",
    }

    (package_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (package_dir / "validation_report.json").write_text(json.dumps({"status": "pass", "errors": [], "warnings": []}), encoding="utf-8")
    (package_dir / "evidence_items.jsonl").write_text(json.dumps(evidence) + "\n", encoding="utf-8")
    (package_dir / "source_manifest.jsonl").write_text(json.dumps(source) + "\n", encoding="utf-8")
    (package_dir / "coverage_note.md").write_text(coverage, encoding="utf-8")
    (package_dir / "README.md").write_text("Bridge demo package. " + coverage, encoding="utf-8")
