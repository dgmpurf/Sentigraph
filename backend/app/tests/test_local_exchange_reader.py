from __future__ import annotations

import json
from pathlib import Path

from app.schemas.local_exchange import LocalExchangeReaderConfig
from app.services.local_exchange_reader import read_provider_result_metadata


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def _safe_provider_result_payload() -> dict:
    return {
        "schema": "sentigraph_provider_job_result_v1",
        "request_schema": "sentigraph_analysis_request_v1",
        "contract_version": "1.0",
        "adapter_id": "external_collector_local_file_adapter",
        "compatibility_status": "compatible",
        "status": "package_ready",
        "provider_result_id": "provider_result_fixture",
        "provider_job_id": "provider_job_fixture",
        "sentigraph_request_id": "request_fixture",
        "package_contract": "sentigraph_evidence_export_v1",
        "package_id": "package_fixture",
        "package_role": "review_ready_candidate",
        "package_index_ref": "package_index.json",
        "package_root_ref": "configured_package_root",
        "package_relative_path": "packages/package_fixture",
        "summary": {
            "evidence_items": 34,
            "sources": 7,
            "comment_samples": 28,
            "root_candidates": 6,
        },
        "validation_summary": {
            "status": "warn",
            "errors": 0,
            "warnings": 2,
        },
        "coverage_note": "Selected package coverage only; not full-web or full-platform coverage.",
        "warnings": ["sample_size_below_target"],
        "errors": [],
        "nextAction": "review_package_metadata",
    }


REQUIRED_FALSE_SAFE_FLAGS = [
    "evidence_items_read",
    "evidence_items_parsed",
    "evidence_items_imported",
    "evidence_layer_written",
    "production_case_created",
    "analysis_run_created",
    "b_end_report_generated",
    "sandbox_fixture_generated",
    "public_event_page_generated",
    "provider_execution",
    "collector_jobs_run",
    "http_provider_integration",
    "real_api_calls",
    "real_llm_calls",
    "url_fetching",
    "scraping",
    "secrets_exposed",
    "raw_author_identifiers_exposed",
]


def _assert_safe_invariants(result) -> None:
    assert result.safe_mode["metadata_only"] is True
    for flag in REQUIRED_FALSE_SAFE_FLAGS:
        assert result.safe_mode[flag] is False


def test_local_exchange_reader_disabled_by_default_does_not_read_files(tmp_path: Path) -> None:
    missing_result = tmp_path / "results" / "provider_result.json"
    config = LocalExchangeReaderConfig(resultsDir=str(tmp_path / "results"))

    result = read_provider_result_metadata(config, missing_result)

    assert result.status == "disabled"
    assert result.file_read_attempted is False
    assert result.result_file_exists is False
    assert result.metadata is None
    assert result.safe_mode["file_read_attempted"] is False
    _assert_safe_invariants(result)


def test_local_exchange_reader_accepts_metadata_only_compatible_provider_result(tmp_path: Path) -> None:
    result_file = _write_json(tmp_path / "results" / "provider_result.json", _safe_provider_result_payload())
    config = LocalExchangeReaderConfig(exchange_enabled=True, resultsDir=str(tmp_path / "results"))

    result = read_provider_result_metadata(config, result_file)

    assert result.status == "metadata_ready"
    assert result.file_read_attempted is True
    assert result.result_file_exists is True
    assert result.metadata is not None
    assert result.metadata.result_schema == "sentigraph_provider_job_result_v1"
    assert result.metadata.request_schema == "sentigraph_analysis_request_v1"
    assert result.metadata.status == "package_ready"
    assert result.metadata.package_id == "package_fixture"
    assert result.metadata.summary["evidence_items"] == 34
    _assert_safe_invariants(result)


def test_local_exchange_reader_rejects_forbidden_nested_fields(tmp_path: Path) -> None:
    payload = _safe_provider_result_payload()
    payload["privacy_leak"] = {"raw_author_id": "should_not_cross_boundary"}
    result_file = _write_json(tmp_path / "results" / "provider_result.json", payload)
    config = LocalExchangeReaderConfig(exchange_enabled=True, resultsDir=str(tmp_path / "results"))

    result = read_provider_result_metadata(config, result_file)

    assert result.status == "blocked"
    assert "raw_author_id" in result.forbidden_fields
    assert result.metadata is None
    _assert_safe_invariants(result)


def test_local_exchange_reader_rejects_unknown_schema_or_version(tmp_path: Path) -> None:
    config = LocalExchangeReaderConfig(exchange_enabled=True, resultsDir=str(tmp_path / "results"))

    payload = _safe_provider_result_payload()
    payload["schema"] = "sentigraph_provider_job_result_v2"
    result_file = _write_json(tmp_path / "results" / "provider_result_v2.json", payload)
    result = read_provider_result_metadata(config, result_file)

    assert result.status == "unsupported_contract"
    assert result.metadata is None
    assert any("result_schema" in warning for warning in result.warnings)
    _assert_safe_invariants(result)

    payload = _safe_provider_result_payload()
    payload["contract_version"] = "2.0"
    result_file = _write_json(tmp_path / "results" / "provider_result_version_2.json", payload)
    result = read_provider_result_metadata(config, result_file)

    assert result.status == "unsupported_contract"
    assert result.metadata is None
    assert any("contract_version" in warning for warning in result.warnings)
    _assert_safe_invariants(result)


def test_local_exchange_reader_unknown_compatibility_status_becomes_blocked(tmp_path: Path) -> None:
    payload = _safe_provider_result_payload()
    payload["compatibility_status"] = "future_live_provider_ready"
    result_file = _write_json(tmp_path / "results" / "provider_result.json", payload)
    config = LocalExchangeReaderConfig(exchange_enabled=True, resultsDir=str(tmp_path / "results"))

    result = read_provider_result_metadata(config, result_file)

    assert result.status == "blocked"
    assert result.metadata is None
    assert any("compatibility_status" in warning for warning in result.warnings)
    _assert_safe_invariants(result)


def test_local_exchange_reader_unknown_provider_status_becomes_manual_review(tmp_path: Path) -> None:
    payload = _safe_provider_result_payload()
    payload["status"] = "future_runnable_status"
    result_file = _write_json(tmp_path / "results" / "provider_result.json", payload)
    config = LocalExchangeReaderConfig(exchange_enabled=True, resultsDir=str(tmp_path / "results"))

    result = read_provider_result_metadata(config, result_file)

    assert result.status == "manual_review_required"
    assert result.metadata is None
    assert any("provider result status" in warning for warning in result.warnings)
    _assert_safe_invariants(result)


def test_local_exchange_reader_unknown_future_platform_requires_manual_review(tmp_path: Path) -> None:
    payload = _safe_provider_result_payload()
    payload["platforms"] = [{"platform": "unknown_future_platform", "queue_status": "runnable_safe"}]
    result_file = _write_json(tmp_path / "results" / "unknown_platform.json", payload)
    config = LocalExchangeReaderConfig(exchange_enabled=True, resultsDir=str(tmp_path / "results"))

    result = read_provider_result_metadata(config, result_file)

    assert result.status == "manual_review_required"
    assert result.metadata is None
    assert any("unknown future platform" in warning for warning in result.warnings)
    _assert_safe_invariants(result)


def test_local_exchange_reader_future_forum_platform_requires_manual_review(tmp_path: Path) -> None:
    payload = _safe_provider_result_payload()
    payload["platforms"] = [{"platform": "future_forum", "queue_status": "runnable_safe"}]
    result_file = _write_json(tmp_path / "results" / "future_forum_platform.json", payload)
    config = LocalExchangeReaderConfig(exchange_enabled=True, resultsDir=str(tmp_path / "results"))

    result = read_provider_result_metadata(config, result_file)

    assert result.status in {"manual_review_required", "blocked"}
    assert result.metadata is None
    assert any("future_forum" in warning for warning in result.warnings)
    assert any("unknown" in warning or "unsupported" in warning for warning in result.warnings)
    _assert_safe_invariants(result)


def test_local_exchange_reader_does_not_parse_evidence_item_files(tmp_path: Path) -> None:
    payload = _safe_provider_result_payload()
    result_file = _write_json(tmp_path / "results" / "provider_result.json", payload)
    package_dir = tmp_path / "packages" / "package_fixture"
    package_dir.mkdir(parents=True)
    (package_dir / "evidence_items.jsonl").write_text("{this is intentionally not parsed", encoding="utf-8")
    config = LocalExchangeReaderConfig(
        exchange_enabled=True,
        resultsDir=str(tmp_path / "results"),
        packageRoot=str(tmp_path / "packages"),
    )

    result = read_provider_result_metadata(config, result_file)

    assert result.status == "metadata_ready"
    _assert_safe_invariants(result)
