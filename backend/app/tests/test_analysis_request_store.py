from __future__ import annotations

import json
from pathlib import Path

from app.schemas.analysis_request import AnalysisRequestCaseSeed, AnalysisRequestCreate
from app.services import analysis_request_store
from app.services.analysis_request_store import (
    cancel_analysis_request,
    create_analysis_request,
    get_analysis_request_config,
    list_analysis_requests,
    read_analysis_request,
)


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
