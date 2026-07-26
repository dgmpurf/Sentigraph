from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import external_collector_bridge as bridge


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

    assert response.status_code == 400
    assert response.json() == {"detail": "blocked_path_escape"}
    assert str(tmp_path) not in response.text


@pytest.mark.parametrize(
    "unsafe_name",
    [
        "../secret",
        r"..\secret",
        "nested/../../secret",
        r"nested\../..\secret",
        "/absolute/secret",
        r"C:\private\secret",
        r"\\server\share\secret",
        r"\leading\secret",
        ".",
        "..",
        "...",
        "nested/package",
    ],
)
def test_external_collector_path_like_names_receive_bounded_containment_status(
    tmp_path: Path,
    monkeypatch,
    unsafe_name: str,
) -> None:
    exports_dir = tmp_path / "exports"
    exports_dir.mkdir()
    monkeypatch.setenv("SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR", str(exports_dir))

    encoded_name = {
        ".": "%2E",
        "..": "%2E%2E",
        "...": "%2E%2E%2E",
    }.get(unsafe_name, quote(unsafe_name, safe=""))
    response = client.get(f"/api/v1/external-collector/packages/{encoded_name}")

    assert response.status_code == 400
    assert response.json() == {"detail": "blocked_path_escape"}
    assert str(tmp_path) not in response.text
    assert unsafe_name not in response.text


def test_external_collector_invalid_non_path_name_has_distinct_safe_status(tmp_path: Path, monkeypatch) -> None:
    exports_dir = tmp_path / "exports"
    exports_dir.mkdir()
    monkeypatch.setenv("SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR", str(exports_dir))

    response = client.get("/api/v1/external-collector/packages/bad%20package")

    assert response.status_code == 400
    assert response.json() == {"detail": "external_collector_invalid_package_name"}
    assert str(tmp_path) not in response.text


def test_external_collector_lookup_statuses_distinguish_configuration_and_missing_package(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.delenv("SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR", raising=False)
    not_configured = client.get("/api/v1/external-collector/packages/safe_package")

    missing_root = tmp_path / "missing_exports"
    monkeypatch.setenv("SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR", str(missing_root))
    configured_root_missing = client.get("/api/v1/external-collector/packages/safe_package")

    exports_dir = tmp_path / "exports"
    exports_dir.mkdir()
    monkeypatch.setenv("SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR", str(exports_dir))
    package_missing = client.get("/api/v1/external-collector/packages/safe_package")

    assert not_configured.status_code == 404
    assert not_configured.json() == {"detail": "external_collector_bridge_not_configured"}
    assert configured_root_missing.status_code == 404
    assert configured_root_missing.json() == {"detail": "external_collector_configured_root_missing"}
    assert package_missing.status_code == 404
    assert package_missing.json() == {"detail": "external_collector_package_not_found"}
    assert str(tmp_path) not in configured_root_missing.text
    assert str(tmp_path) not in package_missing.text


def test_external_collector_rejected_path_does_not_open_or_enumerate_package_content(
    tmp_path: Path,
    monkeypatch,
) -> None:
    exports_dir = tmp_path / "exports"
    exports_dir.mkdir()
    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()
    (outside_dir / "manifest.json").write_text('{"private": "must-not-be-read"}', encoding="utf-8")
    monkeypatch.setenv("SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR", str(exports_dir))
    read_calls: list[Path] = []
    enumeration_calls: list[Path] = []
    original_read_text = Path.read_text
    original_iterdir = Path.iterdir

    def tracked_read_text(path: Path, *args, **kwargs):
        read_calls.append(path)
        return original_read_text(path, *args, **kwargs)

    def tracked_iterdir(path: Path):
        enumeration_calls.append(path)
        return original_iterdir(path)

    monkeypatch.setattr(Path, "read_text", tracked_read_text)
    monkeypatch.setattr(Path, "iterdir", tracked_iterdir)

    response = client.get("/api/v1/external-collector/packages/..%2Foutside")

    assert response.status_code == 400
    assert response.json() == {"detail": "blocked_path_escape"}
    assert read_calls == []
    assert enumeration_calls == []
    assert str(outside_dir) not in response.text
    assert "must-not-be-read" not in response.text


def test_external_collector_canonical_sibling_prefix_escape_is_rejected(
    tmp_path: Path,
    monkeypatch,
) -> None:
    exports_dir = tmp_path / "safe"
    exports_dir.mkdir()
    sibling_dir = tmp_path / "safe-evil"
    sibling_dir.mkdir()
    candidate = exports_dir / "linked_package"
    original_resolve = Path.resolve

    def redirected_resolve(path: Path, *args, **kwargs):
        if path == exports_dir:
            return exports_dir
        if path == candidate:
            return sibling_dir
        return original_resolve(path, *args, **kwargs)

    monkeypatch.setattr(bridge, "_configured_exports_dir", lambda: exports_dir)
    monkeypatch.setattr(Path, "resolve", redirected_resolve)

    response = client.get("/api/v1/external-collector/packages/linked_package")

    assert response.status_code == 400
    assert response.json() == {"detail": "blocked_path_escape"}
    assert str(exports_dir) not in response.text
    assert str(sibling_dir) not in response.text


def test_external_collector_listing_skips_canonical_outside_root_directory(
    tmp_path: Path,
    monkeypatch,
) -> None:
    exports_dir = tmp_path / "exports"
    linked_package = exports_dir / "linked_package"
    linked_package.mkdir(parents=True)
    outside_package = tmp_path / "outside" / "linked_package"
    outside_package.mkdir(parents=True)
    original_resolve = Path.resolve

    def redirected_resolve(path: Path, *args, **kwargs):
        if path == exports_dir:
            return exports_dir
        if path == linked_package:
            return outside_package
        return original_resolve(path, *args, **kwargs)

    def unexpected_summary(*args, **kwargs):
        pytest.fail("outside-root directory must not reach package summary parsing")

    monkeypatch.setattr(bridge, "_configured_exports_dir", lambda: exports_dir)
    monkeypatch.setattr(Path, "resolve", redirected_resolve)
    monkeypatch.setattr(bridge, "_package_summary", unexpected_summary)

    assert bridge.list_external_collector_packages() == []


def test_external_collector_validation_route_rejects_encoded_traversal(tmp_path: Path, monkeypatch) -> None:
    exports_dir = tmp_path / "exports"
    exports_dir.mkdir()
    monkeypatch.setenv("SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR", str(exports_dir))

    response = client.post("/api/v1/external-collector/packages/..%2Fsecret/validate")

    assert response.status_code == 400
    assert response.json() == {"detail": "blocked_path_escape"}
    assert str(tmp_path) not in response.text


def test_external_collector_internal_path_failure_is_bounded(monkeypatch) -> None:
    def fail_configuration_lookup() -> Path:
        raise OSError(r"C:\private\collector\must-not-leak")

    monkeypatch.setattr(bridge, "_configured_exports_dir", fail_configuration_lookup)

    response = client.get("/api/v1/external-collector/packages/safe_package")

    assert response.status_code == 500
    assert response.json() == {"detail": "external_collector_internal_failure"}
    assert "must-not-leak" not in response.text
    assert "C:" not in response.text


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
