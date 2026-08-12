from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any

from app.schemas.local_exchange import LocalExchangeReaderConfig
from app.services.local_exchange_reader import (
    read_provider_result_metadata as read_local_exchange_provider_result_metadata,
    read_provider_result_metadata_with_content_identity,
)
from app.services.private_collector_package_resolver import (
    GOVERNED_B05_METADATA_READ_PROFILE as _RESOLVER_GOVERNED_B05_METADATA_READ_PROFILE,
)
from app.services.private_collector_provider_result_reader import (
    PrivateCollectorProviderResultReaderResult,
    read_provider_result_metadata as read_private_collector_provider_result_metadata,
    read_provider_result_metadata_with_identity,
)
from app.services.private_collector_review_only_staging import (
    build_review_only_staging_gate_result,
    build_safe_review_only_staging_summary,
    create_review_only_staging_candidate,
)


GOVERNED_B05_STAGING_METADATA_READ_PROFILE = (
    _RESOLVER_GOVERNED_B05_METADATA_READ_PROFILE
)

RESPONSE_SCHEMA = "internal_operator_review_only_staging_local_exchange_response_v0_1"
VERSIONED_RESPONSE_SCHEMA = "internal_operator_review_only_staging_local_exchange_response_v0_2"
OUTPUT_PROVIDER_RESULT_SCHEMA = "sentigraph_provider_job_result_v0_1"
OUTPUT_PROVIDER_RESULT_CONTRACT_VERSION = "0.1"
MAX_RESULT_FILE_NAME_LENGTH = 160
MAX_SAFE_TEXT_LENGTH = 2_000

_RESULT_FILE_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*\.json$")
_PLAIN_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_SAFE_IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,191}$")

_SOURCE_STATUS_MAP = {
    "package_ready": "package_ready",
    "needs_manual_snapshot": "manual_review_required",
    "blocked": "blocked_safety",
    "invalid_schema": "needs_fix_metadata_contract",
    "unsupported_contract": "needs_fix_metadata_contract",
    "failed": "blocked_safety",
    "manual_review_required": "manual_review_required",
}

_READER_STATUS_MAP = {
    "disabled": "blocked_configuration",
    "blocked": "blocked_safety",
    "invalid_schema": "needs_fix_metadata_contract",
    "unsupported_contract": "needs_fix_metadata_contract",
    "manual_review_required": "manual_review_required",
    "not_found": "not_found",
    "failed": "blocked_safety",
}

_READY_PROVIDER_READER_STATUSES = {
    "accepted_metadata_only",
    "validation_passed",
}

_MANUAL_PROVIDER_READER_STATUSES = {
    "validation_warn",
    "manual_review_required",
    "adapter_required",
    "field_quality_weak",
    "unsupported_platform",
}

_EXPECTED_SAFETY_MARKERS = {
    "raw_author_id_exported": False,
    "raw_author_name_exported": False,
    "profile_url_exported": False,
    "raw_author_id_removed": True,
    "raw_author_name_removed": True,
    "no_private_messages": True,
}


@dataclass(frozen=True, slots=True)
class LocalExchangeReviewOnlyStagingBridgeConfig:
    results_dir: str = ""
    export_root: str = ""
    adapter_id: str = ""
    metadata_read_profile: str | None = None


@dataclass(slots=True)
class LocalExchangeProviderResultAdapterResult:
    status: str
    provider_result: dict[str, Any] | None = None
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def adapt_local_exchange_metadata_to_provider_result(
    metadata: dict[str, Any],
) -> LocalExchangeProviderResultAdapterResult:
    """Purely adapt validated v1 metadata into the existing v0.1 reader contract."""

    if not isinstance(metadata, dict):
        return _adapter_stop("needs_fix_metadata_contract", "metadata_not_object")

    required_identifiers = (
        "provider_result_id",
        "provider_job_id",
        "sentigraph_request_id",
        "provider_type",
        "adapter_id",
        "package_contract",
    )
    normalized_identifiers: dict[str, str] = {}
    for field_name in required_identifiers:
        value = metadata.get(field_name)
        if not _is_safe_identifier(value):
            return _adapter_stop("manual_review_required", f"missing_or_unsafe_actual_field:{field_name}")
        normalized_identifiers[field_name] = str(value)

    source_status = metadata.get("status")
    if not isinstance(source_status, str) or source_status not in _SOURCE_STATUS_MAP:
        return _adapter_stop("manual_review_required", "unknown_source_status")
    output_status = _SOURCE_STATUS_MAP[source_status]

    package_name = metadata.get("package_id")
    package_role = metadata.get("package_role")
    package_index_ref = metadata.get("package_index_ref")
    package_root_ref = metadata.get("package_root_ref")
    package_relative_path = metadata.get("package_relative_path")
    if not _is_plain_name(package_name):
        return _adapter_stop("blocked_path_escape", "unsafe_package_identity")
    if not _is_safe_identifier(package_role):
        return _adapter_stop("manual_review_required", "missing_or_unsafe_actual_field:package_role")
    if not _is_plain_json_name(package_index_ref):
        return _adapter_stop("manual_review_required", "unsafe_package_index_reference")
    if package_root_ref != "configured_export_root":
        return _adapter_stop("manual_review_required", "ambiguous_package_root_reference")
    if not _is_unambiguous_package_relative_path(package_relative_path, str(package_name)):
        return _adapter_stop("blocked_path_escape", "unsafe_or_ambiguous_package_relative_path")

    summary = metadata.get("summary")
    if not isinstance(summary, dict):
        return _adapter_stop("manual_review_required", "missing_actual_metadata_summary")
    evidence_count = _nonnegative_int(summary.get("evidence_count", summary.get("evidence_items")))
    source_count = _nonnegative_int(summary.get("source_count", summary.get("sources")))
    comment_count = _nonnegative_int(summary.get("comment_count", summary.get("comment_samples")))
    root_candidate_count = _nonnegative_int(
        summary.get("root_candidate_count", summary.get("root_candidates"))
    )
    if (
        evidence_count is None
        or source_count is None
        or comment_count is None
        or root_candidate_count is None
    ):
        return _adapter_stop("manual_review_required", "incomplete_actual_metadata_summary")

    validation_summary = metadata.get("validation_summary")
    if not isinstance(validation_summary, dict):
        return _adapter_stop("manual_review_required", "missing_actual_validation_summary")
    validation_status = validation_summary.get("status")
    validation_errors = _nonnegative_int(validation_summary.get("errors"))
    validation_warnings = _nonnegative_int(validation_summary.get("warnings"))
    if (
        not _is_safe_identifier(validation_status)
        or validation_errors is None
        or validation_warnings is None
    ):
        return _adapter_stop("manual_review_required", "incomplete_actual_validation_summary")

    coverage_note = metadata.get("coverage_note")
    created_at = metadata.get("created_at")
    if not _is_safe_text(coverage_note):
        return _adapter_stop("manual_review_required", "missing_or_unsafe_actual_field:coverage_note")
    if not _is_safe_text(created_at, max_length=128):
        return _adapter_stop("manual_review_required", "missing_or_unsafe_actual_field:created_at")

    safety_markers = metadata.get("safety_markers")
    if not isinstance(safety_markers, dict):
        return _adapter_stop("manual_review_required", "missing_actual_safety_markers")
    missing_safety_markers = sorted(set(_EXPECTED_SAFETY_MARKERS) - set(safety_markers))
    if missing_safety_markers:
        return _adapter_stop("manual_review_required", "incomplete_actual_safety_markers")
    if set(safety_markers) != set(_EXPECTED_SAFETY_MARKERS):
        return _adapter_stop("blocked_safety", "unexpected_actual_safety_markers")
    if any(safety_markers[key] is not expected for key, expected in _EXPECTED_SAFETY_MARKERS.items()):
        return _adapter_stop("blocked_safety", "unsafe_actual_safety_markers")

    provider_result = {
        "schema": OUTPUT_PROVIDER_RESULT_SCHEMA,
        "provider_result_id": normalized_identifiers["provider_result_id"],
        "provider_job_id": normalized_identifiers["provider_job_id"],
        "request_id": normalized_identifiers["sentigraph_request_id"],
        "provider_type": normalized_identifiers["provider_type"],
        "adapter_id": normalized_identifiers["adapter_id"],
        "contract_version": OUTPUT_PROVIDER_RESULT_CONTRACT_VERSION,
        "status": output_status,
        "package_contract": normalized_identifiers["package_contract"],
        "package_reference": {
            "package_name": str(package_name),
            "package_role": str(package_role),
            "package_index_ref": str(package_index_ref),
            "package_locator_strategy": "package_name_under_configured_export_root",
        },
        "metadata_summary": {
            "evidence_count": evidence_count,
            "source_count": source_count,
            "comment_count": comment_count,
            "root_candidate_count": root_candidate_count,
        },
        "validation_summary": {
            "status": str(validation_status),
            "errors": validation_errors,
            "warnings": validation_warnings,
        },
        "coverage_note": str(coverage_note),
        "safety_markers": {key: safety_markers[key] for key in _EXPECTED_SAFETY_MARKERS},
        "created_at": str(created_at),
    }
    return LocalExchangeProviderResultAdapterResult(status="adapted", provider_result=provider_result)


def build_local_exchange_review_only_staging_response(
    result_file_name: str,
    config: LocalExchangeReviewOnlyStagingBridgeConfig,
) -> dict[str, Any]:
    """Read one configured result and build one nonpersistent review-only candidate."""

    if not _is_valid_result_file_name(result_file_name):
        return _terminal_response(
            "invalid_result_file_name",
            blockers=["invalid_result_file_name"],
        )

    response = _base_response(result_file_name)
    if not config.results_dir.strip() or not config.export_root.strip() or not config.adapter_id.strip():
        response.update(
            status="blocked_configuration",
            blockers=["missing_server_owned_configuration"],
        )
        return response

    local_reader_config = LocalExchangeReaderConfig(
        exchange_enabled=True,
        resultsDir=config.results_dir,
        result_schema="sentigraph_provider_job_result_v1",
        contract_version="1.0",
        adapter_id=config.adapter_id,
    )
    result_path = Path(config.results_dir) / result_file_name
    local_reader_result = read_local_exchange_provider_result_metadata(local_reader_config, result_path)
    response["reader_status"] = local_reader_result.status
    if local_reader_result.status != "metadata_ready" or local_reader_result.metadata is None:
        response["status"] = _READER_STATUS_MAP.get(local_reader_result.status, "manual_review_required")
        response["blockers"] = [response["status"]]
        return response

    adapter_result = adapt_local_exchange_metadata_to_provider_result(
        local_reader_result.metadata.model_dump(mode="python")
    )
    response["adapter_status"] = adapter_result.status
    if adapter_result.status != "adapted" or adapter_result.provider_result is None:
        response["status"] = adapter_result.status
        response["blockers"] = list(adapter_result.blockers)
        response["warnings"] = list(adapter_result.warnings)
        return response

    if config.metadata_read_profile is None:
        provider_reader_result = read_private_collector_provider_result_metadata(
            adapter_result.provider_result,
            config.export_root,
        )
    else:
        provider_reader_result = read_private_collector_provider_result_metadata(
            adapter_result.provider_result,
            config.export_root,
            metadata_read_profile=config.metadata_read_profile,
        )
    response["provider_result_status"] = provider_reader_result.status
    response["package_resolution_status"] = (
        provider_reader_result.resolver_result.status
        if provider_reader_result.resolver_result is not None
        else None
    )

    handoff_summary = _build_staging_handoff(provider_reader_result)
    candidate = create_review_only_staging_candidate(
        handoff_summary,
        requested_by="mvp_b01_local_exchange_bridge",
    )
    gate = build_review_only_staging_gate_result(handoff_summary, candidate)
    staging_summary = build_safe_review_only_staging_summary(candidate, gate)

    response["status"] = _bridge_status(provider_reader_result.status, staging_summary)
    response["candidate_count"] = 1
    response["staging_candidate"] = staging_summary
    response["gate_summary"] = dict(staging_summary["gate_result"])
    response["blockers"] = list(staging_summary["blockers"])
    response["warnings"] = list(staging_summary["warnings"])
    return response


def build_identity_ready_local_exchange_review_only_staging_response(
    result_file_name: str,
    config: LocalExchangeReviewOnlyStagingBridgeConfig,
) -> dict[str, Any]:
    """Build the parallel identity-ready handoff without changing B01 v0.1."""

    response = _base_versioned_response(result_file_name if _is_valid_result_file_name(result_file_name) else None)
    if not _is_valid_result_file_name(result_file_name):
        response.update(
            status="invalid_result_file_name",
            error_code="invalid_result_file_name",
            blockers=["invalid_result_file_name"],
        )
        return response
    if not config.results_dir.strip() or not config.export_root.strip() or not config.adapter_id.strip():
        response.update(
            status="blocked_configuration",
            blockers=["missing_server_owned_configuration"],
        )
        return response

    local_reader_config = LocalExchangeReaderConfig(
        exchange_enabled=True,
        resultsDir=config.results_dir,
        result_schema="sentigraph_provider_job_result_v1",
        contract_version="1.0",
        adapter_id=config.adapter_id,
    )
    result_path = Path(config.results_dir) / result_file_name
    local_reader_result = read_provider_result_metadata_with_content_identity(
        local_reader_config,
        result_path,
    )
    response["reader_status"] = local_reader_result.status
    if (
        local_reader_result.status != "metadata_ready"
        or local_reader_result.identity_status != "ready"
        or local_reader_result.metadata is None
        or local_reader_result.provider_result_content_identity is None
    ):
        response["status"] = local_reader_result.identity_status
        response["blockers"] = [local_reader_result.identity_status]
        response["review_subject_identity_material"] = _unavailable_identity_material(
            local_reader_result.identity_status,
            result_file_name=result_file_name,
        )
        return response

    adapter_result = adapt_local_exchange_metadata_to_provider_result(
        local_reader_result.metadata.model_dump(mode="python")
    )
    response["adapter_status"] = adapter_result.status
    if adapter_result.status != "adapted" or adapter_result.provider_result is None:
        response["status"] = "unavailable_identity_material"
        response["blockers"] = list(adapter_result.blockers) or ["unavailable_identity_material"]
        response["warnings"] = list(adapter_result.warnings)
        return response

    content_identity = local_reader_result.provider_result_content_identity.model_dump(mode="python")
    provider_reader_result = read_provider_result_metadata_with_identity(
        adapter_result.provider_result,
        config.export_root,
        provider_result_content_identity=content_identity,
        metadata_read_profile=config.metadata_read_profile or GOVERNED_B05_STAGING_METADATA_READ_PROFILE,
    )
    response["provider_result_status"] = provider_reader_result.status
    response["package_resolution_status"] = (
        provider_reader_result.resolver_result.status
        if provider_reader_result.resolver_result is not None
        else None
    )
    if provider_reader_result.identity_status != "ready":
        response["status"] = provider_reader_result.identity_status
        response["blockers"] = [provider_reader_result.identity_status]
        response["review_subject_identity_material"] = _unavailable_identity_material(
            provider_reader_result.identity_status,
            result_file_name=result_file_name,
            package_name=(
                provider_reader_result.resolver_result.package_name
                if provider_reader_result.resolver_result is not None
                else None
            ),
        )
        return response

    handoff_summary = _build_staging_handoff(provider_reader_result)  # type: ignore[arg-type]
    handoff_summary["review_subject_content_identity"] = dict(
        provider_reader_result.safe_identity_material
    )
    candidate = create_review_only_staging_candidate(
        handoff_summary,
        requested_by="post_p04_b05_identity_ready_bridge",
    )
    gate = build_review_only_staging_gate_result(handoff_summary, candidate)
    staging_summary = build_safe_review_only_staging_summary(candidate, gate)

    response["status"] = _bridge_status(provider_reader_result.status, staging_summary)
    response["candidate_count"] = 1
    response["staging_candidate"] = staging_summary
    response["gate_summary"] = dict(staging_summary["gate_result"])
    response["blockers"] = list(staging_summary["blockers"])
    response["warnings"] = list(staging_summary["warnings"])
    response["review_subject_identity_material"] = dict(
        provider_reader_result.safe_identity_material
    )
    return response


def build_disabled_local_exchange_response(error_code: str) -> dict[str, Any]:
    response = _base_response(None)
    response.update(
        status=error_code,
        error_code=error_code,
        blockers=[error_code],
    )
    return response


def _build_staging_handoff(
    provider_reader_result: PrivateCollectorProviderResultReaderResult,
) -> dict[str, Any]:
    provider_summary = provider_reader_result.safe_summary
    package_summary = (
        provider_summary.get("package_summary")
        if isinstance(provider_summary.get("package_summary"), dict)
        else {}
    )
    metadata_summary = (
        provider_summary.get("metadata_summary")
        if isinstance(provider_summary.get("metadata_summary"), dict)
        else {}
    )
    validation_summary = (
        provider_summary.get("validation_summary")
        if isinstance(provider_summary.get("validation_summary"), dict)
        else {}
    )
    if provider_reader_result.status in _READY_PROVIDER_READER_STATUSES:
        smoke_status = "ready_for_metadata_only_handoff"
    elif provider_reader_result.status in _MANUAL_PROVIDER_READER_STATUSES:
        smoke_status = "manual_review_required"
    else:
        smoke_status = provider_reader_result.status

    blockers = list(provider_reader_result.errors)
    if provider_reader_result.status not in _READY_PROVIDER_READER_STATUSES | _MANUAL_PROVIDER_READER_STATUSES:
        blockers.extend(provider_reader_result.warnings)
    return {
        "schema": "sentigraph_private_collector_local_exchange_smoke_summary_v0_1",
        "smoke_status": smoke_status,
        "provider_result_status": provider_reader_result.status,
        "provider_result_id": provider_summary.get("provider_result_id"),
        "package_resolution_status": package_summary.get("status"),
        "package_name": package_summary.get("package_name"),
        "case_id": provider_summary.get("request_id"),
        "validation_status": validation_summary.get("status"),
        "evidence_count": metadata_summary.get("evidence_count"),
        "source_count": metadata_summary.get("source_count"),
        "comment_count": metadata_summary.get("comment_count"),
        "root_candidate_count": metadata_summary.get("root_candidate_count"),
        "warning_count": validation_summary.get("warnings"),
        "error_count": validation_summary.get("errors"),
        "coverage_note": provider_summary.get("coverage_note"),
        "metadata_only": True,
        "full_evidence_rows_read": False,
        "evidence_layer_write": False,
        "production_case_created": False,
        "analysis_run_created": False,
        "forbidden_fields": list(provider_reader_result.forbidden_fields),
        "blockers": blockers,
        "warnings": list(provider_reader_result.warnings),
        "safe_mode": _safety_flags(),
        "path_exposed": False,
        "path_reference": "configured_local_exchange_result_and_export_root_package",
    }


def _bridge_status(provider_reader_status: str, staging_summary: dict[str, Any]) -> str:
    if provider_reader_status in _MANUAL_PROVIDER_READER_STATUSES:
        return "manual_review_required"
    if provider_reader_status not in _READY_PROVIDER_READER_STATUSES:
        return provider_reader_status
    staging_status = staging_summary.get("staging_status")
    return str(staging_status) if isinstance(staging_status, str) else "manual_review_required"


def _base_response(result_file_name: str | None) -> dict[str, Any]:
    return {
        "schema": RESPONSE_SCHEMA,
        "route_scope": "internal_operator",
        "access_scope": "local_or_disabled_by_default",
        "metadata_only": True,
        "review_only": True,
        "status": "not_started",
        "error_code": None,
        "result_file_name": result_file_name,
        "reader_status": "not_called",
        "adapter_status": "not_called",
        "provider_result_status": None,
        "package_resolution_status": None,
        "candidate_count": 0,
        "staging_candidate": None,
        "gate_summary": None,
        "production_import_allowed": False,
        "evidence_layer_write_allowed": False,
        "production_case_creation_allowed": False,
        "analysis_run_allowed": False,
        "public_output_allowed": False,
        "path_exposed": False,
        "raw_metadata_exposed": False,
        "blockers": [],
        "warnings": [],
        "safety_flags": _safety_flags(),
    }


def _base_versioned_response(result_file_name: str | None) -> dict[str, Any]:
    response = _base_response(result_file_name)
    response["schema"] = VERSIONED_RESPONSE_SCHEMA
    response["review_subject_identity_material"] = _unavailable_identity_material(
        "unavailable_identity_material",
        result_file_name=result_file_name,
    )
    return response


def _unavailable_identity_material(
    identity_status: str,
    *,
    result_file_name: str | None,
    package_name: str | None = None,
) -> dict[str, Any]:
    return {
        "identity_status": identity_status,
        "result_file_name": result_file_name,
        "package_name": package_name,
        "provider_result_content_bytes": None,
        "provider_result_content_sha256": None,
        "metadata_profile": None,
        "metadata_entry_count": 0,
        "safe_metadata_bundle_sha256": None,
        "review_subject_content_safe_hash": None,
    }


def _terminal_response(
    status: str,
    *,
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    response = _base_response(None)
    response.update(
        status=status,
        blockers=list(blockers or []),
        warnings=list(warnings or []),
    )
    return response


def _adapter_stop(status: str, blocker: str) -> LocalExchangeProviderResultAdapterResult:
    return LocalExchangeProviderResultAdapterResult(status=status, blockers=[blocker])


def _is_valid_result_file_name(value: Any) -> bool:
    if not isinstance(value, str) or not value or len(value) > MAX_RESULT_FILE_NAME_LENGTH:
        return False
    if value in {".", ".."} or any(ord(character) < 32 or ord(character) == 127 for character in value):
        return False
    if any(marker in value for marker in ("/", "\\", ":", "\x00")):
        return False
    return _RESULT_FILE_NAME_RE.fullmatch(value) is not None


def _is_plain_name(value: Any) -> bool:
    return (
        isinstance(value, str)
        and value not in {"", ".", ".."}
        and _PLAIN_NAME_RE.fullmatch(value) is not None
    )


def _is_plain_json_name(value: Any) -> bool:
    return _is_plain_name(value) and str(value).endswith(".json")


def _is_safe_identifier(value: Any) -> bool:
    return isinstance(value, str) and _SAFE_IDENTIFIER_RE.fullmatch(value) is not None


def _is_unambiguous_package_relative_path(value: Any, package_name: str) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        return False
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return False
    return len(path.parts) == 1 and path.parts[0] == package_name


def _is_safe_text(value: Any, *, max_length: int = MAX_SAFE_TEXT_LENGTH) -> bool:
    if not isinstance(value, str) or not value.strip() or len(value) > max_length:
        return False
    return not any(ord(character) < 32 and character not in {"\t", "\n", "\r"} for character in value)


def _nonnegative_int(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _safety_flags() -> dict[str, bool]:
    return {
        "metadata_only": True,
        "review_only_staging_bridge_only": True,
        "runtime_file_written": False,
        "persistent_staging_storage_created": False,
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
        "public_output_generated": False,
        "external_delivery_performed": False,
    }
