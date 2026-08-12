from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from app.schemas.local_exchange import (
    LocalExchangeProviderResultMetadata,
    LocalExchangeProviderResultContentIdentity,
    LocalExchangeReaderConfig,
    LocalExchangeReaderResult,
    LocalExchangeVersionedReaderResult,
)
from app.services.b05_review_subject_identity import (
    build_provider_result_content_identity,
    text_from_same_read_raw_bytes,
)


ACCEPTED_PROVIDER_STATUSES = {
    "package_ready",
    "needs_manual_snapshot",
    "blocked",
    "invalid_schema",
    "unsupported_contract",
    "failed",
    "manual_review_required",
}
METADATA_READY_PROVIDER_STATUSES = {"package_ready", "needs_manual_snapshot"}

COMPATIBLE_STATUSES = {"compatible", "deprecated_compatible"}
MANUAL_REVIEW_COMPATIBILITY_STATUSES = {"manual_review_required"}
INVALID_COMPATIBILITY_STATUSES = {"invalid_schema"}
UNSUPPORTED_COMPATIBILITY_STATUSES = {"unsupported_contract"}

FORBIDDEN_FIELD_NAMES = {
    "cookie",
    "cookies",
    "token",
    "tokens",
    "session",
    "sessions",
    "browser_profile_path",
    "browser_profile_paths",
    "localstorage",
    "local_storage",
    "password",
    "passwords",
    "qr_payload",
    "qr_payloads",
    "raw_author_id",
    "raw_author_ids",
    "raw_author_identifier",
    "raw_author_identifiers",
    "raw_author_name",
    "raw_author_names",
    "author_id",
    "author_ids",
    "author_name",
    "author_names",
    "profile_url",
    "profile_urls",
    "private_message",
    "private_messages",
    "raw_evidence_rows",
    "evidence_item_content",
    "evidence_items_content",
    "evidence_items_jsonl",
    "evidence_items_csv",
    "collector_internals",
    "proxy_pool",
    "proxy_details",
    "evasion_details",
    "bypass_details",
    "captcha_bypass",
    "anti_bot_bypass",
}

FORBIDDEN_VALUE_MARKERS = {
    "evidence_items.jsonl",
    "evidence_items.csv",
}

PLATFORM_LIST_FIELDS = {
    "platforms",
    "source_platforms",
}
PLATFORM_SUMMARY_FIELDS = {
    "platform_summary",
    "source_summaries",
}
UNKNOWN_FUTURE_PLATFORM_MARKERS = {
    "future",
    "unknown",
    "unsupported",
    "unconfigured",
    "placeholder",
    "experimental",
}


def read_provider_result_metadata(
    config: LocalExchangeReaderConfig,
    result_file: str | Path | None = None,
) -> LocalExchangeReaderResult:
    """Read one explicitly configured provider result metadata file.

    This function is intentionally metadata-only. It does not read package
    indexes, evidence rows, collector state, environment variables, or URLs.
    """

    if not config.exchange_enabled:
        return _reader_result(
            "disabled",
            warnings=["local exchange reader disabled by default"],
        )

    if result_file is None:
        return _reader_result(
            "blocked",
            warnings=["result_file is required when local exchange reader is enabled"],
        )

    if not config.resultsDir.strip():
        return _reader_result(
            "blocked",
            warnings=["resultsDir must be explicitly configured before reading metadata"],
        )

    path = Path(result_file)
    results_dir = Path(config.resultsDir)
    if not _is_path_within(path, results_dir):
        return _reader_result(
            "blocked",
            warnings=["result_file must stay inside configured resultsDir"],
        )

    if not path.exists() or not path.is_file():
        return _reader_result(
            "not_found",
            warnings=["provider result metadata file not found"],
            file_read_attempted=False,
            result_file_exists=False,
        )

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return _reader_result(
            "invalid_schema",
            errors=[f"provider result metadata is not valid JSON: {exc.msg}"],
            file_read_attempted=True,
            result_file_exists=True,
        )
    except OSError as exc:
        return _reader_result(
            "failed",
            errors=[f"provider result metadata could not be read: {type(exc).__name__}"],
            file_read_attempted=True,
            result_file_exists=True,
        )

    if not isinstance(payload, dict):
        return _reader_result(
            "invalid_schema",
            errors=["provider result metadata must be a JSON object"],
            file_read_attempted=True,
            result_file_exists=True,
        )

    forbidden_fields = sorted(_find_forbidden_fields(payload))
    if forbidden_fields:
        return _reader_result(
            "blocked",
            warnings=["provider result metadata contains forbidden fields"],
            forbidden_fields=forbidden_fields,
            file_read_attempted=True,
            result_file_exists=True,
        )

    contract_status = _validate_contract(payload, config)
    if contract_status is not None:
        status, warnings = contract_status
        return _reader_result(
            status,
            warnings=warnings,
            file_read_attempted=True,
            result_file_exists=True,
        )

    unknown_platforms = _unknown_future_platform_values(payload)
    if unknown_platforms:
        platform_summary = ", ".join(unknown_platforms[:5])
        return _reader_result(
            "manual_review_required",
            warnings=[
                f"unknown future platform or unsupported platform metadata requires manual review: {platform_summary}"
            ],
            file_read_attempted=True,
            result_file_exists=True,
        )

    try:
        metadata = LocalExchangeProviderResultMetadata.model_validate(payload)
    except ValidationError as exc:
        return _reader_result(
            "invalid_schema",
            errors=[str(exc)],
            file_read_attempted=True,
            result_file_exists=True,
        )

    return _reader_result(
        "metadata_ready",
        metadata=metadata,
        file_read_attempted=True,
        result_file_exists=True,
    )


def read_provider_result_metadata_with_content_identity(
    config: LocalExchangeReaderConfig,
    result_file: str | Path | None = None,
) -> LocalExchangeVersionedReaderResult:
    """Read and identify one provider result from one immutable raw buffer."""

    if not config.exchange_enabled:
        return _versioned_reader_result(
            "disabled",
            "unavailable_identity_material",
            warnings=["local exchange reader disabled by default"],
        )
    if result_file is None:
        return _versioned_reader_result(
            "blocked",
            "unavailable_identity_material",
            warnings=["result_file is required when local exchange reader is enabled"],
        )
    if not config.resultsDir.strip():
        return _versioned_reader_result(
            "blocked",
            "unavailable_identity_material",
            warnings=["resultsDir must be explicitly configured before reading metadata"],
        )

    path = Path(result_file)
    results_dir = Path(config.resultsDir)
    if not _is_path_within(path, results_dir):
        return _versioned_reader_result(
            "blocked",
            "unavailable_identity_material",
            warnings=["result_file must stay inside configured resultsDir"],
        )
    if not path.exists() or not path.is_file():
        return _versioned_reader_result(
            "not_found",
            "unavailable_identity_material",
            warnings=["provider result metadata file not found"],
            result_file_exists=False,
        )

    try:
        raw_bytes = path.read_bytes()
        safe_identity = build_provider_result_content_identity(path.name, raw_bytes)
        text = text_from_same_read_raw_bytes(raw_bytes)
    except (OSError, UnicodeDecodeError, TypeError, ValueError):
        return _versioned_reader_result(
            "failed",
            "blocked_provider_result_read_or_decode",
            errors=["provider result metadata could not be read or decoded"],
            file_read_attempted=True,
            result_file_exists=True,
        )

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return _versioned_reader_result(
            "invalid_schema",
            "blocked_provider_result_parse",
            errors=["provider result metadata is not valid JSON"],
            file_read_attempted=True,
            result_file_exists=True,
        )
    if not isinstance(payload, dict):
        return _versioned_reader_result(
            "invalid_schema",
            "blocked_provider_result_parse",
            errors=["provider result metadata must be a JSON object"],
            file_read_attempted=True,
            result_file_exists=True,
        )

    forbidden_fields = sorted(_find_forbidden_fields(payload))
    if forbidden_fields:
        return _versioned_reader_result(
            "blocked",
            "unavailable_identity_material",
            warnings=["provider result metadata contains forbidden fields"],
            forbidden_fields=forbidden_fields,
            file_read_attempted=True,
            result_file_exists=True,
        )
    contract_status = _validate_contract(payload, config)
    if contract_status is not None:
        status, warnings = contract_status
        return _versioned_reader_result(
            status,
            "unavailable_identity_material",
            warnings=warnings,
            file_read_attempted=True,
            result_file_exists=True,
        )
    unknown_platforms = _unknown_future_platform_values(payload)
    if unknown_platforms:
        return _versioned_reader_result(
            "manual_review_required",
            "unavailable_identity_material",
            warnings=["unknown future or unsupported platform metadata requires manual review"],
            file_read_attempted=True,
            result_file_exists=True,
        )
    try:
        metadata = LocalExchangeProviderResultMetadata.model_validate(payload)
        content_identity = LocalExchangeProviderResultContentIdentity.model_validate(safe_identity)
    except ValidationError:
        return _versioned_reader_result(
            "invalid_schema",
            "blocked_provider_result_parse",
            errors=["provider result metadata failed schema validation"],
            file_read_attempted=True,
            result_file_exists=True,
        )
    return _versioned_reader_result(
        "metadata_ready",
        "ready",
        metadata=metadata,
        provider_result_content_identity=content_identity,
        file_read_attempted=True,
        result_file_exists=True,
    )


def _versioned_reader_result(
    status: str,
    identity_status: str,
    *,
    metadata: LocalExchangeProviderResultMetadata | None = None,
    provider_result_content_identity: LocalExchangeProviderResultContentIdentity | None = None,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
    forbidden_fields: list[str] | None = None,
    file_read_attempted: bool = False,
    result_file_exists: bool = False,
) -> LocalExchangeVersionedReaderResult:
    result = LocalExchangeVersionedReaderResult(
        status=status,  # type: ignore[arg-type]
        identity_status=identity_status,  # type: ignore[arg-type]
        metadata=metadata,
        provider_result_content_identity=provider_result_content_identity,
        warnings=warnings or [],
        errors=errors or [],
        forbidden_fields=forbidden_fields or [],
        file_read_attempted=file_read_attempted,
        result_file_exists=result_file_exists,
    )
    result.safe_mode["file_read_attempted"] = file_read_attempted
    return result


def _reader_result(
    status: str,
    *,
    metadata: LocalExchangeProviderResultMetadata | None = None,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
    forbidden_fields: list[str] | None = None,
    file_read_attempted: bool = False,
    result_file_exists: bool = False,
) -> LocalExchangeReaderResult:
    result = LocalExchangeReaderResult(
        status=status,  # type: ignore[arg-type]
        metadata=metadata,
        warnings=warnings or [],
        errors=errors or [],
        forbidden_fields=forbidden_fields or [],
        file_read_attempted=file_read_attempted,
        result_file_exists=result_file_exists,
    )
    result.safe_mode["file_read_attempted"] = file_read_attempted
    return result


def _is_path_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _find_forbidden_fields(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            lowered_key = str(key).lower()
            if lowered_key in FORBIDDEN_FIELD_NAMES:
                found.add(str(key))
            found.update(_find_forbidden_fields(nested_value))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_forbidden_fields(item))
    elif isinstance(value, str):
        lowered_value = value.lower()
        for marker in FORBIDDEN_VALUE_MARKERS:
            if marker in lowered_value:
                found.add(marker)
    return found


def _validate_contract(payload: dict[str, Any], config: LocalExchangeReaderConfig) -> tuple[str, list[str]] | None:
    result_schema = payload.get("result_schema") or payload.get("schema")
    if result_schema != config.result_schema:
        return "unsupported_contract", [f"unsupported result_schema: {result_schema!r}"]

    request_schema = payload.get("request_schema")
    if request_schema is not None and request_schema != config.request_schema:
        return "unsupported_contract", [f"unsupported request_schema: {request_schema!r}"]

    contract_version = payload.get("contract_version")
    if contract_version != config.contract_version:
        return "unsupported_contract", [f"unsupported contract_version: {contract_version!r}"]

    configured_adapter = config.adapter_id.strip()
    if configured_adapter and payload.get("adapter_id") != configured_adapter:
        return "manual_review_required", ["adapter_id does not match configured adapter"]

    compatibility_status = str(payload.get("compatibility_status", "")).strip()
    if compatibility_status in COMPATIBLE_STATUSES:
        compatibility_warning = (
            ["provider result uses deprecated_compatible compatibility_status"]
            if compatibility_status == "deprecated_compatible"
            else []
        )
    elif compatibility_status in UNSUPPORTED_COMPATIBILITY_STATUSES:
        return "unsupported_contract", ["provider result compatibility_status is unsupported_contract"]
    elif compatibility_status in INVALID_COMPATIBILITY_STATUSES:
        return "invalid_schema", ["provider result compatibility_status is invalid_schema"]
    elif compatibility_status in MANUAL_REVIEW_COMPATIBILITY_STATUSES:
        return "manual_review_required", ["provider result compatibility_status requires manual review"]
    else:
        return "blocked", [f"unknown compatibility_status: {compatibility_status!r}"]

    provider_status = str(payload.get("status", "")).strip()
    if provider_status not in ACCEPTED_PROVIDER_STATUSES:
        return "manual_review_required", [f"unknown provider result status: {provider_status!r}"]
    if provider_status == "unsupported_contract":
        return "unsupported_contract", ["provider result status is unsupported_contract"]
    if provider_status == "invalid_schema":
        return "invalid_schema", ["provider result status is invalid_schema"]
    if provider_status == "manual_review_required":
        return "manual_review_required", ["provider result status requires manual review"]
    if provider_status == "blocked":
        return "blocked", ["provider result status is blocked"]
    if provider_status == "failed":
        return "failed", ["provider result status is failed"]
    if provider_status not in METADATA_READY_PROVIDER_STATUSES:
        return "manual_review_required", [f"provider result status is not metadata-ready: {provider_status!r}"]

    if compatibility_warning:
        payload.setdefault("warnings", [])
        if isinstance(payload["warnings"], list):
            payload["warnings"].extend(compatibility_warning)
    return None


def _unknown_future_platform_values(payload: dict[str, Any]) -> list[str]:
    unknown_platforms: set[str] = set()
    for candidate in _walk_values(payload):
        if not isinstance(candidate, dict):
            continue
        for key in ("platform", "platform_hint"):
            value = candidate.get(key)
            if _is_unknown_future_platform(value):
                unknown_platforms.add(str(value).strip())
        for key in PLATFORM_LIST_FIELDS:
            for value in _flatten_platform_metadata(candidate.get(key), include_keys=False):
                if _is_unknown_future_platform(value):
                    unknown_platforms.add(value)
        for key in PLATFORM_SUMMARY_FIELDS:
            for value in _flatten_platform_metadata(candidate.get(key), include_keys=True):
                if _is_unknown_future_platform(value):
                    unknown_platforms.add(value)
        package_summary = candidate.get("package_summary")
        if isinstance(package_summary, dict):
            for value in _flatten_platform_metadata(package_summary.get("platforms"), include_keys=False):
                if _is_unknown_future_platform(value):
                    unknown_platforms.add(value)
    return sorted(unknown_platforms)


def _flatten_platform_metadata(value: Any, *, include_keys: bool) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, (int, float, bool)):
        return []
    if isinstance(value, list):
        flattened: list[str] = []
        for item in value:
            flattened.extend(_flatten_platform_metadata(item, include_keys=include_keys))
        return flattened
    if isinstance(value, dict):
        flattened = []
        for key, nested_value in value.items():
            if include_keys and str(key).strip():
                flattened.append(str(key).strip())
            flattened.extend(_flatten_platform_metadata(nested_value, include_keys=include_keys))
        return flattened
    return []


def _is_unknown_future_platform(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.strip().lower().replace("-", "_")
    if not normalized:
        return False
    tokens = {token for token in normalized.split("_") if token}
    return bool(tokens & UNKNOWN_FUTURE_PLATFORM_MARKERS)


def _walk_values(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for nested_value in value.values():
            values.extend(_walk_values(nested_value))
    elif isinstance(value, list):
        for item in value:
            values.extend(_walk_values(item))
    return values
