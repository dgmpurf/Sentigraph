from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
import sys


def _load_mapper():
    repo_root = Path(__file__).resolve().parents[3]
    module_path = repo_root / "scripts" / "map_vendor_sample_to_evidence.py"
    spec = importlib.util.spec_from_file_location("vendor_sample_mapper", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _fixture_path(name: str) -> Path:
    return Path(__file__).parent / "fixtures" / "evidence" / name


def test_vendor_csv_maps_to_evidence_like_rows_and_redacts_secrets(monkeypatch) -> None:
    mapper = _load_mapper()
    network_attempted = False

    def fail_network(*_args, **_kwargs):
        nonlocal network_attempted
        network_attempted = True
        raise AssertionError("vendor sample mapper must not call network")

    monkeypatch.setattr("socket.create_connection", fail_network)

    result = mapper.map_vendor_sample_file(
        _fixture_path("vendor_sample_minimal.csv"),
        vendor_name="ExampleVendor",
        platform="news_site",
        query="Tesla QA",
    )

    assert len(result.evidence_items) == 2
    first = result.evidence_items[0]
    assert first["acquisition_mode"] == "data_vendor"
    assert first["provenance_type"] == "data_vendor"
    assert first["verification_status"] == "vendor_attested"
    assert first["trust_label"] == "medium_low"
    assert first["source_capture_method"] == "vendor_sample_file"
    assert first["raw_data_safe"]["no_network_calls"] is True
    assert first["raw_data_safe"]["no_url_fetching"] is True
    assert first["raw_data_safe"]["no_scraping"] is True
    assert "password=[REDACTED]" in first["comment_text"]
    assert first["author_id"] == "user_123"
    assert first["created_at"].endswith("Z")
    assert "secret-marker" not in json.dumps(result.evidence_items, ensure_ascii=False)
    assert network_attempted is False


def test_missing_compliance_fields_remain_unverified_and_flagged() -> None:
    mapper = _load_mapper()
    result = mapper.map_vendor_sample_file(
        _fixture_path("vendor_sample_minimal.csv"),
        vendor_name="ExampleVendor",
        platform="news_site",
        query="Tesla QA",
    )

    second = result.evidence_items[1]
    assert second["platform"] == "unknown_network"
    assert second["verification_status"] == "needs_review"
    assert second["trust_label"] == "unverified"
    assert second["raw_data_safe"]["compliance_metadata"]["vendor_attestation"] == "unknown"
    assert "source_unclear" in second["risk_flags"]
    assert "deletion_sync_unknown" in second["risk_flags"]
    assert "personal_data_unknown" in second["risk_flags"]
    assert "unsupported_platform_claim" in second["risk_flags"]
    assert "formula_like_text_plain" in second["risk_flags"]
    assert "possible_secret_redacted" in second["risk_flags"]
    assert second["like_count"] == 0
    assert any(warning["code"] == "invalid_number" for warning in second["validation_warnings"])


def test_timestamp_parser_handles_seconds_milliseconds_and_iso() -> None:
    mapper = _load_mapper()
    warnings: list[object] = []

    seconds = mapper.parse_vendor_timestamp("1716211200", row_number=1, field="created_at", warnings=warnings)
    milliseconds = mapper.parse_vendor_timestamp("1716214800000", row_number=1, field="collected_at", warnings=warnings)
    iso = mapper.parse_vendor_timestamp("2026-05-20T08:00:00Z", row_number=1, field="created_at", warnings=warnings)

    assert seconds == "2024-05-20T13:20:00Z"
    assert milliseconds == "2024-05-20T14:20:00Z"
    assert iso == "2026-05-20T08:00:00Z"
    assert warnings == []


def test_json_input_unknown_platform_does_not_crash_and_author_ids_are_safe(tmp_path) -> None:
    mapper = _load_mapper()
    sample_path = tmp_path / "vendor_sample.json"
    sample_path.write_text(
        json.dumps(
            {
                "records": [
                    {
                        "provider": "JsonVendor",
                        "platform": "new_platform",
                        "content_id": "json_001",
                        "comment": "Vendor JSON public comment with api_key=secret-value",
                        "author_id": "author-safe-1",
                        "source_url": "https://example.test/json/1",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = mapper.map_vendor_sample_file(sample_path, vendor_name="JsonVendor", platform="news_site", query="Tesla QA")

    assert len(result.evidence_items) == 1
    item = result.evidence_items[0]
    assert item["platform"] == "new_platform"
    assert item["source_type"] == "public_web"
    assert item["author_id"] == "author-safe-1"
    assert "unsupported_platform_claim" in item["risk_flags"]
    assert "api_key=[REDACTED]" in item["comment_text"]
    assert "secret-value" not in json.dumps(item, ensure_ascii=False)


def test_cli_can_write_jsonl_and_csv_without_secret_values(tmp_path) -> None:
    mapper = _load_mapper()
    result = mapper.map_vendor_sample_file(
        _fixture_path("vendor_sample_minimal.csv"),
        vendor_name="ExampleVendor",
        platform="news_site",
        query="Tesla QA",
    )
    jsonl_path = tmp_path / "mapped.jsonl"
    csv_path = tmp_path / "mapped.csv"

    with jsonl_path.open("w", encoding="utf-8", newline="") as handle:
        mapper.write_jsonl(result.evidence_items, handle)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        mapper.write_csv(result.evidence_items, handle)

    assert len(jsonl_path.read_text(encoding="utf-8").splitlines()) == 2
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 2
    assert "secret-marker" not in jsonl_path.read_text(encoding="utf-8")
    assert "secret-marker" not in csv_path.read_text(encoding="utf-8")
