from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REQUIRED_PACKAGE_METADATA_FILES = (
    "manifest.json",
    "source_manifest.jsonl",
    "evidence_items.jsonl",
    "evidence_items.csv",
    "collection_log.jsonl",
    "coverage_note.md",
    "README.md",
    "validation_report.json",
    "validation_report.md",
)

READABLE_METADATA_FILES = {
    "manifest.json",
    "validation_report.json",
    "coverage_note.md",
    "README.md",
    "validation_report.md",
    "package_index.json",
}

GENERIC_METADATA_READ_PROFILE = "generic_six_file"
GOVERNED_B05_METADATA_READ_PROFILE = "governed_b05_five_file"
GOVERNED_B05_READABLE_METADATA_FILES = (
    "README.md",
    "coverage_note.md",
    "manifest.json",
    "validation_report.json",
    "validation_report.md",
)

FORBIDDEN_METADATA_FIELDS = {
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
}

ALLOWED_PRIVACY_MARKERS = {
    "raw_author_id_exported": False,
    "raw_author_name_exported": False,
    "profile_url_exported": False,
    "raw_author_id_removed": True,
    "raw_author_name_removed": True,
    "no_private_messages": True,
}

TERMINAL_BLOCK_STATUSES = {
    "blocked_path_escape",
    "blocked_missing_package",
    "blocked_privacy_issue",
    "needs_fix_metadata_contract",
    "manual_review_required",
}


@dataclass(slots=True)
class PrivateCollectorPackageResolutionResult:
    status: str
    package_name: str | None = None
    locator_strategy: str | None = None
    resolved_package_path: Path | None = None
    required_files_presence: dict[str, bool] = field(default_factory=dict)
    missing_required_files: list[str] = field(default_factory=list)
    forbidden_fields: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    safe_mode: dict[str, bool] = field(default_factory=dict)


@dataclass(slots=True)
class PrivateCollectorPackageMetadataSummary:
    status: str
    package_name: str | None
    required_files_presence: dict[str, bool]
    missing_required_files: list[str]
    forbidden_fields: list[str]
    warnings: list[str]
    safe_summary: dict[str, Any]


def resolve_private_collector_package(
    export_root: str | Path,
    package_entry: dict[str, Any],
    *,
    metadata_read_profile: str = GENERIC_METADATA_READ_PROFILE,
) -> PrivateCollectorPackageResolutionResult:
    """Resolve a private collector package for metadata-only handoff.

    This helper intentionally does not parse evidence row files, run collector
    jobs, write Evidence Layer records, create cases, or expose absolute paths
    in its safe summary output.
    """

    safe_mode = _safe_mode()
    readable_metadata_files = _readable_metadata_files_for_profile(metadata_read_profile)
    if readable_metadata_files is None:
        return _result(
            "needs_fix_metadata_contract",
            errors=["unsupported metadata_read_profile"],
            safe_mode=safe_mode,
        )
    root = Path(export_root)
    try:
        resolved_root = root.resolve(strict=False)
    except OSError as exc:
        return _result(
            "blocked_missing_package",
            errors=[f"configured_export_root could not be resolved: {type(exc).__name__}"],
            safe_mode=safe_mode,
        )

    if not resolved_root.exists() or not resolved_root.is_dir():
        return _result(
            "blocked_missing_package",
            errors=["configured_export_root does not exist or is not a directory"],
            safe_mode=safe_mode,
        )

    package_name = _clean_text(package_entry.get("package_name"))
    legacy_path = _clean_text(package_entry.get("package_path_relative"))
    explicit_relative_path = _clean_text(package_entry.get("package_path_relative_to_export_root"))

    warnings: list[str] = []
    if package_name is not None:
        package_name_error = _validate_package_name(package_name)
        if package_name_error is not None:
            return _result(
                package_name_error,
                package_name=package_name,
                warnings=["package_name must be a plain directory name"],
                safe_mode=safe_mode,
            )

        candidate = resolved_root / package_name
        if _is_path_within_root(candidate, resolved_root):
            try:
                resolved_candidate = candidate.resolve(strict=False)
            except OSError:
                return _result(
                    "blocked_path_escape",
                    package_name=package_name,
                    errors=["package_name path could not be safely resolved"],
                    safe_mode=safe_mode,
                )
            if resolved_candidate.exists() and resolved_candidate.is_dir():
                if legacy_path is not None:
                    warnings.append("legacy package_path_relative ignored because package_name resolved safely")
                return _resolve_existing_package(
                    resolved_candidate,
                    package_name,
                    "package_name_under_configured_export_root",
                    warnings=warnings,
                    safe_mode=safe_mode,
                    readable_metadata_files=readable_metadata_files,
                )
        else:
            return _result(
                "blocked_path_escape",
                package_name=package_name,
                warnings=["package_name resolved outside configured_export_root"],
                safe_mode=safe_mode,
            )

    if explicit_relative_path is not None:
        relative_status = _validate_relative_path(explicit_relative_path)
        if relative_status is not None:
            return _result(
                relative_status,
                warnings=["package_path_relative_to_export_root must stay inside configured_export_root"],
                safe_mode=safe_mode,
            )
        candidate = resolved_root / explicit_relative_path
        if not _is_path_within_root(candidate, resolved_root):
            return _result(
                "blocked_path_escape",
                warnings=["package_path_relative_to_export_root resolved outside configured_export_root"],
                safe_mode=safe_mode,
            )
        resolved_candidate = candidate.resolve(strict=False)
        if not resolved_candidate.exists() or not resolved_candidate.is_dir():
            return _result(
                "blocked_missing_package",
                package_name=resolved_candidate.name,
                locator_strategy="package_path_relative_to_export_root",
                warnings=["package_path_relative_to_export_root package directory not found"],
                safe_mode=safe_mode,
            )
        return _resolve_existing_package(
            resolved_candidate,
            resolved_candidate.name,
            "package_path_relative_to_export_root",
            warnings=warnings,
            safe_mode=safe_mode,
            readable_metadata_files=readable_metadata_files,
        )

    if package_name is not None:
        return _result(
            "blocked_missing_package",
            package_name=package_name,
            warnings=["package_name package directory not found under configured_export_root"],
            safe_mode=safe_mode,
        )

    if legacy_path is not None:
        return _result(
            "manual_review_required",
            warnings=["legacy package_path_relative is ambiguous without an explicit export-root base"],
            safe_mode=safe_mode,
        )

    return _result(
        "needs_fix_metadata_contract",
        warnings=["package metadata must include package_name or package_path_relative_to_export_root"],
        safe_mode=safe_mode,
    )


def summarize_private_collector_package_metadata(
    resolved_package: PrivateCollectorPackageResolutionResult,
) -> PrivateCollectorPackageMetadataSummary:
    return PrivateCollectorPackageMetadataSummary(
        status=resolved_package.status,
        package_name=resolved_package.package_name,
        required_files_presence=dict(resolved_package.required_files_presence),
        missing_required_files=list(resolved_package.missing_required_files),
        forbidden_fields=list(resolved_package.forbidden_fields),
        warnings=list(resolved_package.warnings),
        safe_summary=build_safe_package_summary(resolved_package),
    )


def build_safe_package_summary(resolution_result: PrivateCollectorPackageResolutionResult) -> dict[str, Any]:
    return {
        "schema": "sentigraph_private_collector_package_resolution_summary_v0_1",
        "status": resolution_result.status,
        "package_name": resolution_result.package_name,
        "locator_strategy": resolution_result.locator_strategy,
        "required_files_presence": dict(resolution_result.required_files_presence),
        "missing_required_files": list(resolution_result.missing_required_files),
        "forbidden_fields": list(resolution_result.forbidden_fields),
        "warnings": list(resolution_result.warnings),
        "safe_mode": dict(resolution_result.safe_mode),
        "path_exposed": False,
        "path_reference": "configured_export_root package",
    }


def _resolve_existing_package(
    package_dir: Path,
    package_name: str,
    locator_strategy: str,
    *,
    warnings: list[str],
    safe_mode: dict[str, bool],
    readable_metadata_files: set[str] | tuple[str, ...],
) -> PrivateCollectorPackageResolutionResult:
    required_files_presence = {filename: (package_dir / filename).exists() for filename in REQUIRED_PACKAGE_METADATA_FILES}
    missing_required_files = [filename for filename, exists in required_files_presence.items() if not exists]
    forbidden_fields = sorted(
        _scan_metadata_files_for_forbidden_fields(
            package_dir,
            readable_metadata_files,
        )
    )
    if forbidden_fields:
        return _result(
            "blocked_privacy_issue",
            package_name=package_name,
            locator_strategy=locator_strategy,
            resolved_package_path=package_dir,
            required_files_presence=required_files_presence,
            missing_required_files=missing_required_files,
            forbidden_fields=forbidden_fields,
            warnings=warnings + ["safe metadata files contain forbidden fields"],
            safe_mode=safe_mode,
        )

    return _result(
        "accepted_metadata_only",
        package_name=package_name,
        locator_strategy=locator_strategy,
        resolved_package_path=package_dir,
        required_files_presence=required_files_presence,
        missing_required_files=missing_required_files,
        warnings=warnings,
        safe_mode=safe_mode,
    )


def _result(
    status: str,
    *,
    package_name: str | None = None,
    locator_strategy: str | None = None,
    resolved_package_path: Path | None = None,
    required_files_presence: dict[str, bool] | None = None,
    missing_required_files: list[str] | None = None,
    forbidden_fields: list[str] | None = None,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
    safe_mode: dict[str, bool] | None = None,
) -> PrivateCollectorPackageResolutionResult:
    return PrivateCollectorPackageResolutionResult(
        status=status,
        package_name=package_name,
        locator_strategy=locator_strategy,
        resolved_package_path=resolved_package_path,
        required_files_presence=required_files_presence or {},
        missing_required_files=missing_required_files or [],
        forbidden_fields=forbidden_fields or [],
        warnings=warnings or [],
        errors=errors or [],
        safe_mode=safe_mode or _safe_mode(),
    )


def _safe_mode() -> dict[str, bool]:
    return {
        "metadata_only": True,
        "package_path_resolver_only": True,
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


def _validate_package_name(package_name: str) -> str | None:
    if package_name in {"", ".", ".."}:
        return "needs_fix_metadata_contract"
    if "/" in package_name or "\\" in package_name:
        return "needs_fix_metadata_contract"
    return None


def _validate_relative_path(relative_path: str) -> str | None:
    path = Path(relative_path)
    if path.is_absolute():
        return "blocked_path_escape"
    if any(part in {"", ".", ".."} for part in path.parts):
        return "blocked_path_escape"
    return None


def _is_path_within_root(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
    except ValueError:
        return False
    return True


def _readable_metadata_files_for_profile(
    metadata_read_profile: object,
) -> set[str] | tuple[str, ...] | None:
    if metadata_read_profile == GENERIC_METADATA_READ_PROFILE:
        return READABLE_METADATA_FILES
    if metadata_read_profile == GOVERNED_B05_METADATA_READ_PROFILE:
        return GOVERNED_B05_READABLE_METADATA_FILES
    return None


def _scan_metadata_files_for_forbidden_fields(
    package_dir: Path,
    readable_metadata_files: set[str] | tuple[str, ...],
) -> set[str]:
    forbidden_fields: set[str] = set()
    for filename in readable_metadata_files:
        path = package_dir / filename
        if not path.exists() or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            forbidden_fields.add(f"{filename}:unreadable_text")
            continue
        except OSError:
            forbidden_fields.add(f"{filename}:read_error")
            continue
        if filename.endswith(".json"):
            try:
                payload = json.loads(text) if text.strip() else {}
            except json.JSONDecodeError:
                forbidden_fields.add(f"{filename}:invalid_json")
                continue
            forbidden_fields.update(_find_forbidden_json_fields(payload))
        else:
            forbidden_fields.update(_find_forbidden_text_fields(text))
    return forbidden_fields


def _find_forbidden_json_fields(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            key_text = str(key)
            lowered_key = key_text.lower()
            if lowered_key in ALLOWED_PRIVACY_MARKERS and nested_value is ALLOWED_PRIVACY_MARKERS[lowered_key]:
                continue
            if lowered_key in FORBIDDEN_METADATA_FIELDS:
                found.add(key_text)
            found.update(_find_forbidden_json_fields(nested_value))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_forbidden_json_fields(item))
    return found


def _find_forbidden_text_fields(text: str) -> set[str]:
    found: set[str] = set()
    field_pattern = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*[:=]", re.MULTILINE)
    for match in field_pattern.finditer(text):
        key = match.group(1).lower()
        if key in ALLOWED_PRIVACY_MARKERS:
            continue
        if key in FORBIDDEN_METADATA_FIELDS:
            found.add(match.group(1))
    return found


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        return None
    return value.strip()
