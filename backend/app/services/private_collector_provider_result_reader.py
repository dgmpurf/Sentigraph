from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.services.private_collector_package_resolver import (
    PrivateCollectorPackageResolutionResult,
    build_safe_package_summary,
    resolve_private_collector_package,
)


PROVIDER_RESULT_SCHEMA = "sentigraph_provider_job_result_v0_1"

REQUIRED_PROVIDER_RESULT_FIELDS = (
    "schema",
    "provider_result_id",
    "provider_job_id",
    "request_id",
    "provider_type",
    "adapter_id",
    "contract_version",
    "status",
    "package_contract",
    "package_reference",
    "metadata_summary",
    "validation_summary",
    "coverage_note",
    "safety_markers",
    "created_at",
)

REQUIRED_PACKAGE_REFERENCE_FIELDS = (
    "package_name",
    "package_role",
    "package_index_ref",
    "package_locator_strategy",
)

ALLOWED_PACKAGE_LOCATOR_STRATEGIES = {
    "package_name_under_configured_export_root",
    "package_path_relative_to_export_root",
    "manual_review_required_legacy_path",
}

READY_PROVIDER_STATUSES = {
    "accepted_metadata_only",
    "package_ready",
    "validation_passed",
}

MANUAL_REVIEW_PROVIDER_STATUSES = {
    "validation_warn",
    "manual_review_required",
    "adapter_required",
    "field_quality_weak",
    "unsupported_platform",
}

BLOCKED_PROVIDER_STATUSES = {
    "blocked_safety",
    "blocked_path_escape",
    "blocked_missing_package",
    "blocked_privacy_issue",
    "live_collection_not_authorized",
    "needs_fix_metadata_contract",
}

FORBIDDEN_PROVIDER_FIELDS = {
    "cookie",
    "token",
    "session",
    "password",
    "api_key",
    "browser_profile",
    "profile_path",
    "raw_author_id",
    "raw_author_name",
    "profile_url",
    "private_message",
    "raw_comment_dump",
    "full_evidence_rows",
    "absolute_media_path",
    "collector_runtime_internal_path",
    "generated_public_response_text",
    "generated_public_message",
    "response_text",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
}

ALLOWED_SAFETY_MARKERS = {
    "raw_author_id_exported": False,
    "raw_author_name_exported": False,
    "profile_url_exported": False,
    "raw_author_id_removed": True,
    "raw_author_name_removed": True,
    "no_private_messages": True,
}


@dataclass(slots=True)
class PrivateCollectorProviderResultReaderResult:
    status: str
    provider_status: str | None = None
    provider_result_id: str | None = None
    resolver_result: PrivateCollectorPackageResolutionResult | None = None
    safe_summary: dict[str, Any] = field(default_factory=dict)
    forbidden_fields: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    safe_mode: dict[str, bool] = field(default_factory=dict)


def read_provider_result_metadata(
    provider_result: dict[str, Any] | str | Path,
    export_root: str | Path,
    *,
    metadata_read_profile: str | None = None,
) -> PrivateCollectorProviderResultReaderResult:
    """Read a metadata-only provider result and resolve its package reference."""

    payload_result = _load_provider_result(provider_result)
    if payload_result.status != "loaded":
        return payload_result
    payload = payload_result.safe_summary["provider_result_payload"]

    validation = validate_provider_result_metadata(payload)
    if validation.status != "valid":
        return validation

    provider_status = str(payload["status"])
    provider_result_id = str(payload["provider_result_id"])
    if provider_status in BLOCKED_PROVIDER_STATUSES:
        return _reader_result(
            provider_status,
            provider_status=provider_status,
            provider_result_id=provider_result_id,
            warnings=[f"provider result status is blocked: {provider_status}"],
            safe_summary=build_provider_handoff_summary(payload, None, status=provider_status),
        )

    strategy = payload["package_reference"]["package_locator_strategy"]
    if strategy == "manual_review_required_legacy_path":
        return _reader_result(
            "manual_review_required",
            provider_status=provider_status,
            provider_result_id=provider_result_id,
            warnings=["legacy package path requires manual review and is not silently accepted"],
            safe_summary=build_provider_handoff_summary(payload, None, status="manual_review_required"),
        )

    if metadata_read_profile is None:
        resolver_result = resolve_provider_result_package(payload, export_root)
    else:
        resolver_result = resolve_provider_result_package(
            payload,
            export_root,
            metadata_read_profile=metadata_read_profile,
        )
    final_status = _status_from_provider_and_resolver(provider_status, resolver_result.status)
    warnings = list(resolver_result.warnings)
    if provider_status in MANUAL_REVIEW_PROVIDER_STATUSES:
        warnings.append(f"provider result status requires manual review: {provider_status}")
    safe_summary = build_provider_handoff_summary(payload, resolver_result, status=final_status)
    return _reader_result(
        final_status,
        provider_status=provider_status,
        provider_result_id=provider_result_id,
        resolver_result=resolver_result,
        forbidden_fields=list(resolver_result.forbidden_fields),
        warnings=warnings,
        errors=list(resolver_result.errors),
        safe_summary=safe_summary,
    )


def validate_provider_result_metadata(provider_result: dict[str, Any]) -> PrivateCollectorProviderResultReaderResult:
    if not isinstance(provider_result, dict):
        return _reader_result("needs_fix_metadata_contract", errors=["provider result metadata must be a JSON object"])

    forbidden_fields = sorted(_find_forbidden_fields(provider_result))
    if forbidden_fields:
        return _reader_result(
            "blocked_privacy_issue",
            forbidden_fields=forbidden_fields,
            warnings=["provider result metadata contains forbidden actual fields"],
        )

    missing = [field_name for field_name in REQUIRED_PROVIDER_RESULT_FIELDS if field_name not in provider_result]
    if missing:
        return _reader_result(
            "needs_fix_metadata_contract",
            errors=[f"missing required provider result field: {field_name}" for field_name in missing],
        )

    if provider_result.get("schema") != PROVIDER_RESULT_SCHEMA:
        return _reader_result(
            "needs_fix_metadata_contract",
            errors=[f"unsupported schema: {provider_result.get('schema')!r}"],
        )

    provider_status = str(provider_result.get("status"))
    if provider_status not in READY_PROVIDER_STATUSES | MANUAL_REVIEW_PROVIDER_STATUSES | BLOCKED_PROVIDER_STATUSES:
        return _reader_result(
            "needs_fix_metadata_contract",
            errors=[f"unsupported provider result status: {provider_status!r}"],
        )

    package_reference = provider_result.get("package_reference")
    if not isinstance(package_reference, dict):
        return _reader_result("needs_fix_metadata_contract", errors=["package_reference must be a JSON object"])

    missing_reference = [field_name for field_name in REQUIRED_PACKAGE_REFERENCE_FIELDS if field_name not in package_reference]
    if missing_reference:
        return _reader_result(
            "needs_fix_metadata_contract",
            errors=[f"missing required package_reference field: {field_name}" for field_name in missing_reference],
        )

    locator_strategy = package_reference.get("package_locator_strategy")
    if locator_strategy not in ALLOWED_PACKAGE_LOCATOR_STRATEGIES:
        return _reader_result(
            "needs_fix_metadata_contract",
            errors=[f"unsupported package_locator_strategy: {locator_strategy!r}"],
        )

    safety_marker_status = _validate_safety_markers(provider_result.get("safety_markers"))
    if safety_marker_status is not None:
        return safety_marker_status

    return _reader_result(
        "valid",
        provider_status=provider_status,
        provider_result_id=str(provider_result.get("provider_result_id")),
    )


def resolve_provider_result_package(
    provider_result: dict[str, Any],
    export_root: str | Path,
    *,
    metadata_read_profile: str | None = None,
) -> PrivateCollectorPackageResolutionResult:
    package_reference = provider_result["package_reference"]
    strategy = package_reference["package_locator_strategy"]
    if strategy == "package_name_under_configured_export_root":
        package_entry = {"package_name": package_reference.get("package_name")}
    elif strategy == "package_path_relative_to_export_root":
        package_entry = {
            "package_path_relative_to_export_root": package_reference.get("package_path_relative_to_export_root")
            or package_reference.get("package_name")
        }
    else:
        package_entry = {
            "package_path_relative": package_reference.get("package_path_relative"),
        }
    if metadata_read_profile is None:
        return resolve_private_collector_package(export_root, package_entry)
    return resolve_private_collector_package(
        export_root,
        package_entry,
        metadata_read_profile=metadata_read_profile,
    )


def build_provider_handoff_summary(
    provider_result: dict[str, Any],
    resolver_result: PrivateCollectorPackageResolutionResult | None,
    *,
    status: str | None = None,
) -> dict[str, Any]:
    provider_status = str(provider_result.get("status", "unknown"))
    final_status = status or (resolver_result.status if resolver_result is not None else provider_status)
    package_summary = (
        build_safe_package_summary(resolver_result)
        if resolver_result is not None
        else {
            "status": final_status,
            "package_name": _safe_package_name(provider_result),
            "path_exposed": False,
            "path_reference": "configured_export_root package",
        }
    )
    return {
        "schema": "sentigraph_private_collector_provider_handoff_summary_v0_1",
        "status": final_status,
        "provider_result_id": provider_result.get("provider_result_id"),
        "provider_job_id": provider_result.get("provider_job_id"),
        "request_id": provider_result.get("request_id"),
        "provider_type": provider_result.get("provider_type"),
        "adapter_id": provider_result.get("adapter_id"),
        "provider_status": provider_status,
        "package_contract": provider_result.get("package_contract"),
        "package_reference": {
            "package_name": _safe_package_name(provider_result),
            "package_role": _package_reference(provider_result).get("package_role"),
            "package_index_ref": _package_reference(provider_result).get("package_index_ref"),
            "package_locator_strategy": _package_reference(provider_result).get("package_locator_strategy"),
        },
        "metadata_summary": provider_result.get("metadata_summary", {}),
        "validation_summary": provider_result.get("validation_summary", {}),
        "coverage_note": provider_result.get("coverage_note"),
        "package_summary": package_summary,
        "safe_mode": _safe_mode(),
        "path_exposed": False,
        "path_reference": "configured_export_root package",
    }


def _load_provider_result(provider_result: dict[str, Any] | str | Path) -> PrivateCollectorProviderResultReaderResult:
    if isinstance(provider_result, dict):
        return _reader_result("loaded", safe_summary={"provider_result_payload": provider_result})

    path = Path(provider_result)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return _reader_result("needs_fix_metadata_contract", errors=[f"provider result JSON is invalid: {exc.msg}"])
    except OSError as exc:
        return _reader_result("needs_fix_metadata_contract", errors=[f"provider result could not be read: {type(exc).__name__}"])
    if not isinstance(payload, dict):
        return _reader_result("needs_fix_metadata_contract", errors=["provider result metadata must be a JSON object"])
    return _reader_result("loaded", safe_summary={"provider_result_payload": payload})


def _reader_result(
    status: str,
    *,
    provider_status: str | None = None,
    provider_result_id: str | None = None,
    resolver_result: PrivateCollectorPackageResolutionResult | None = None,
    safe_summary: dict[str, Any] | None = None,
    forbidden_fields: list[str] | None = None,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> PrivateCollectorProviderResultReaderResult:
    return PrivateCollectorProviderResultReaderResult(
        status=status,
        provider_status=provider_status,
        provider_result_id=provider_result_id,
        resolver_result=resolver_result,
        safe_summary=safe_summary or {},
        forbidden_fields=forbidden_fields or [],
        warnings=warnings or [],
        errors=errors or [],
        safe_mode=_safe_mode(),
    )


def _status_from_provider_and_resolver(provider_status: str, resolver_status: str) -> str:
    if resolver_status != "accepted_metadata_only":
        return resolver_status
    if provider_status == "package_ready":
        return "accepted_metadata_only"
    if provider_status == "validation_passed":
        return "validation_passed"
    if provider_status in MANUAL_REVIEW_PROVIDER_STATUSES:
        return provider_status
    return provider_status


def _validate_safety_markers(value: Any) -> PrivateCollectorProviderResultReaderResult | None:
    if not isinstance(value, dict):
        return _reader_result("needs_fix_metadata_contract", errors=["safety_markers must be a JSON object"])
    warnings = []
    for marker, expected_value in ALLOWED_SAFETY_MARKERS.items():
        if marker in value and value[marker] is not expected_value:
            warnings.append(f"safety marker does not preserve boundary: {marker}")
    if warnings:
        return _reader_result("blocked_safety", warnings=warnings)
    return None


def _find_forbidden_fields(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            key_text = str(key)
            lowered_key = key_text.lower()
            if lowered_key in ALLOWED_SAFETY_MARKERS and nested_value is ALLOWED_SAFETY_MARKERS[lowered_key]:
                continue
            if lowered_key in FORBIDDEN_PROVIDER_FIELDS:
                found.add(key_text)
            found.update(_find_forbidden_fields(nested_value))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_forbidden_fields(item))
    return found


def _package_reference(provider_result: dict[str, Any]) -> dict[str, Any]:
    package_reference = provider_result.get("package_reference")
    return package_reference if isinstance(package_reference, dict) else {}


def _safe_package_name(provider_result: dict[str, Any]) -> str | None:
    package_name = _package_reference(provider_result).get("package_name")
    return package_name if isinstance(package_name, str) else None


def _safe_mode() -> dict[str, bool]:
    return {
        "metadata_only": True,
        "provider_result_reader_only": True,
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
