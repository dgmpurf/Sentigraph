from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from app.schemas.local_exchange import (
    LocalExchangeProviderResultMetadata,
    LocalExchangeReaderConfig,
    LocalExchangeReaderResult,
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

    if _contains_unknown_future_platform(payload):
        return _reader_result(
            "manual_review_required",
            warnings=["unknown future platform metadata requires manual review"],
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


def _contains_unknown_future_platform(payload: dict[str, Any]) -> bool:
    for candidate in _walk_values(payload):
        if not isinstance(candidate, dict):
            continue
        platform = str(candidate.get("platform") or candidate.get("platform_hint") or "").strip().lower()
        if platform.startswith("unknown") or "future_platform" in platform:
            return True
    return False


def _walk_values(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for nested_value in value.values():
            values.extend(_walk_values(nested_value))
    elif isinstance(value, list):
        for item in value:
            values.extend(_walk_values(item))
    return values
