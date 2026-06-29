from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.services.private_collector_provider_result_reader import (
    PrivateCollectorProviderResultReaderResult,
    read_provider_result_metadata,
)


READY_READER_STATUSES = {
    "accepted_metadata_only",
    "validation_passed",
}

MANUAL_REVIEW_READER_STATUSES = {
    "validation_warn",
    "manual_review_required",
    "adapter_required",
    "field_quality_weak",
    "unsupported_platform",
}

BLOCKED_READER_STATUSES = {
    "blocked_safety",
    "blocked_path_escape",
    "blocked_missing_package",
    "blocked_privacy_issue",
    "live_collection_not_authorized",
    "needs_fix_metadata_contract",
}


@dataclass(slots=True)
class PrivateCollectorLocalExchangeSmokeResult:
    smoke_status: str
    provider_result_status: str | None = None
    package_resolution_status: str | None = None
    package_name: str | None = None
    case_id: str | None = None
    validation_status: str | None = None
    metadata_only: bool = True
    full_evidence_rows_read: bool = False
    evidence_layer_write: bool = False
    production_case_created: bool = False
    analysis_run_created: bool = False
    safe_summary: dict[str, Any] = field(default_factory=dict)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def run_private_collector_local_exchange_metadata_smoke(
    provider_result_path: str | Path,
    export_root: str | Path,
) -> PrivateCollectorLocalExchangeSmokeResult:
    """Run a local metadata-only exchange smoke against a synthetic fixture path."""

    path = Path(provider_result_path)
    if not path.exists() or not path.is_file():
        return _smoke_result(
            "blocked_missing_provider_result",
            blockers=["provider_result JSON file not found"],
        )

    reader_result = read_provider_result_metadata(path, export_root)
    smoke_status = _smoke_status_from_reader(reader_result.status)
    provider_summary = reader_result.safe_summary
    package_summary = provider_summary.get("package_summary") if isinstance(provider_summary.get("package_summary"), dict) else {}
    validation_summary = provider_summary.get("validation_summary") if isinstance(provider_summary.get("validation_summary"), dict) else {}
    metadata_summary = provider_summary.get("metadata_summary") if isinstance(provider_summary.get("metadata_summary"), dict) else {}

    blockers = list(reader_result.errors)
    if smoke_status in BLOCKED_READER_STATUSES or smoke_status in {"blocked_missing_provider_result", "needs_fix_metadata_contract"}:
        blockers.extend(reader_result.warnings)
    warnings = list(reader_result.warnings)
    safe_summary = _build_safe_smoke_summary(
        smoke_status=smoke_status,
        reader_result=reader_result,
        package_summary=package_summary,
        validation_summary=validation_summary,
        metadata_summary=metadata_summary,
        blockers=blockers,
        warnings=warnings,
    )
    return _smoke_result(
        smoke_status,
        provider_result_status=reader_result.status,
        package_resolution_status=package_summary.get("status"),
        package_name=package_summary.get("package_name"),
        case_id=provider_summary.get("request_id"),
        validation_status=validation_summary.get("status"),
        safe_summary=safe_summary,
        blockers=blockers,
        warnings=warnings,
    )


def _smoke_status_from_reader(reader_status: str) -> str:
    if reader_status in READY_READER_STATUSES:
        return "ready_for_metadata_only_handoff"
    if reader_status in MANUAL_REVIEW_READER_STATUSES:
        return "manual_review_required"
    if reader_status in BLOCKED_READER_STATUSES:
        return reader_status
    return "needs_fix_metadata_contract"


def _build_safe_smoke_summary(
    *,
    smoke_status: str,
    reader_result: PrivateCollectorProviderResultReaderResult,
    package_summary: dict[str, Any],
    validation_summary: dict[str, Any],
    metadata_summary: dict[str, Any],
    blockers: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "schema": "sentigraph_private_collector_local_exchange_smoke_summary_v0_1",
        "smoke_status": smoke_status,
        "provider_result_status": reader_result.status,
        "package_resolution_status": package_summary.get("status"),
        "package_name": package_summary.get("package_name"),
        "case_id": reader_result.safe_summary.get("request_id"),
        "validation_status": validation_summary.get("status"),
        "evidence_count": metadata_summary.get("evidence_count"),
        "source_count": metadata_summary.get("source_count"),
        "warning_count": validation_summary.get("warnings"),
        "error_count": validation_summary.get("errors"),
        "metadata_only": True,
        "full_evidence_rows_read": False,
        "evidence_layer_write": False,
        "production_case_created": False,
        "analysis_run_created": False,
        "forbidden_fields": list(reader_result.forbidden_fields),
        "blockers": list(blockers),
        "warnings": list(warnings),
        "safe_mode": _safe_mode(),
        "path_exposed": False,
        "path_reference": "configured_exchange_provider_result and configured_export_root package",
    }


def _smoke_result(
    smoke_status: str,
    *,
    provider_result_status: str | None = None,
    package_resolution_status: str | None = None,
    package_name: str | None = None,
    case_id: str | None = None,
    validation_status: str | None = None,
    safe_summary: dict[str, Any] | None = None,
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
) -> PrivateCollectorLocalExchangeSmokeResult:
    return PrivateCollectorLocalExchangeSmokeResult(
        smoke_status=smoke_status,
        provider_result_status=provider_result_status,
        package_resolution_status=package_resolution_status,
        package_name=package_name,
        case_id=case_id,
        validation_status=validation_status,
        metadata_only=True,
        full_evidence_rows_read=False,
        evidence_layer_write=False,
        production_case_created=False,
        analysis_run_created=False,
        safe_summary=safe_summary or {
            "schema": "sentigraph_private_collector_local_exchange_smoke_summary_v0_1",
            "smoke_status": smoke_status,
            "metadata_only": True,
            "full_evidence_rows_read": False,
            "evidence_layer_write": False,
            "production_case_created": False,
            "analysis_run_created": False,
            "path_exposed": False,
            "path_reference": "configured_exchange_provider_result and configured_export_root package",
            "safe_mode": _safe_mode(),
        },
        blockers=blockers or [],
        warnings=warnings or [],
    )


def _safe_mode() -> dict[str, bool]:
    return {
        "metadata_only": True,
        "local_exchange_smoke_only": True,
        "runtime_file_written": False,
        "collector_run": False,
        "live_crawl": False,
        "browser_automation": False,
        "real_api_called": False,
        "real_llm_called": False,
        "url_fetching": False,
        "scraping": False,
        "full_evidence_rows_parsed": False,
        "evidence_items_jsonl_parsed": False,
        "evidence_items_csv_parsed": False,
        "raw_comments_printed": False,
        "raw_author_identifiers_printed": False,
        "secrets_read": False,
        "evidence_layer_written": False,
        "production_case_created": False,
        "analysis_run_created": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_runtime_generated": False,
        "frontend_api_route_added": False,
        "project_source_changed": False,
        "github_actions_recreated": False,
    }
