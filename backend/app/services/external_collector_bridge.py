from __future__ import annotations

import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any

from app.schemas.external_collector_bridge import (
    ExternalCollectorPackageDetail,
    ExternalCollectorPackageSummary,
    ExternalCollectorStatus,
    ExternalCollectorValidationResult,
)


EXPORTS_ENV_VAR = "SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR"
SUGGESTED_LOCAL_PATH = r"G:\AICODING\网页端任务二\exports\sentigraph-evidence-v1"
PACKAGE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")
PACKAGE_INDEX_FILE = "package_index.json"
PACKAGE_ROLE_PRIORITY = {
    "recommended_demo_sample": 0,
    "controlled_public_sample": 1,
    "local_snapshot_test": 2,
    "seed_relevance_test": 3,
    "historical_smoke_test": 4,
    "unknown_historical_export": 5,
}
EXPECTED_FILES = [
    "manifest.json",
    "source_manifest.jsonl",
    "evidence_items.jsonl",
    "coverage_note.md",
    "README.md",
    "validation_report.json",
]
FORBIDDEN_EVIDENCE_KEYS = {
    "raw_author_id",
    "raw_author_name",
    "author_id",
    "author_name",
    "comment_user_id",
    "comment_user_name",
    "profile_url",
    "user_url",
    "homepage_url",
}
SUSPICIOUS_SECRET_KEYS = {
    "api_key",
    "access_token",
    "refresh_token",
    "client_secret",
    "token",
    "cookie",
    "password",
    "session",
    "salt",
}
COVERAGE_PHRASES = [
    "selected public sample",
    "not full-web",
    "not full-platform",
    "not official verification",
    "not causal proof",
]


def get_external_collector_status() -> ExternalCollectorStatus:
    exports_dir = _configured_exports_dir()
    if not exports_dir:
        return ExternalCollectorStatus(
            configured=False,
            exports_dir="",
            exists=False,
            package_count=0,
            message=f"Set {EXPORTS_ENV_VAR} to a local Sentigraph Evidence Export v1 folder.",
            suggested_local_path=SUGGESTED_LOCAL_PATH,
        )

    exists = exports_dir.exists() and exports_dir.is_dir()
    index_entries: dict[str, dict[str, Any]] = {}
    index_available = False
    index_warning = ""
    if exists:
        index_entries, index_available, index_warning = _read_package_index(exports_dir)
    package_count = len(_direct_package_dirs(exports_dir)) if exists else 0
    return ExternalCollectorStatus(
        configured=True,
        exports_dir=str(exports_dir),
        exists=exists,
        package_count=package_count,
        index_available=index_available,
        index_warning=index_warning,
        message="Configured local exports folder is available." if exists else "Configured exports folder does not exist.",
        suggested_local_path=SUGGESTED_LOCAL_PATH,
    )


def list_external_collector_packages() -> list[ExternalCollectorPackageSummary]:
    exports_dir = _configured_exports_dir()
    if not exports_dir or not exports_dir.exists() or not exports_dir.is_dir():
        return []
    index_entries, index_available, index_warning = _read_package_index(exports_dir)
    summaries = [
        _package_summary(
            package_dir,
            index_entry=index_entries.get(package_dir.name),
            index_available=index_available,
            index_warning=index_warning,
        )
        for package_dir in _direct_package_dirs(exports_dir)
    ]
    return sorted(summaries, key=_package_sort_key)


def get_external_collector_package_detail(package_name: str) -> ExternalCollectorPackageDetail:
    package_dir = _resolve_package_dir(package_name)
    index_entries, index_available, index_warning = _read_package_index(package_dir.parent)
    index_entry = index_entries.get(package_dir.name)
    manifest = _read_json(package_dir / "manifest.json")
    validation_report = _read_json(package_dir / "validation_report.json")
    summary = _package_summary(
        package_dir,
        manifest=manifest,
        validation_report=validation_report,
        index_entry=index_entry,
        index_available=index_available,
        index_warning=index_warning,
    )
    validation_summary = _validation_report_summary(validation_report)
    privacy_policy = manifest.get("privacy_policy") if isinstance(manifest.get("privacy_policy"), dict) else {}
    return ExternalCollectorPackageDetail(
        package_name=package_dir.name,
        package_path=str(package_dir),
        manifest_summary=_manifest_summary(manifest),
        validation_report_summary=validation_summary,
        expected_files={file_name: (package_dir / file_name).exists() for file_name in EXPECTED_FILES},
        coverage_note_excerpt=_safe_excerpt(package_dir / "coverage_note.md", 1600),
        readme_excerpt=_safe_excerpt(package_dir / "README.md", 1600),
        privacy_summary={
            "raw_author_id_removed": privacy_policy.get("raw_author_id_removed"),
            "raw_author_name_removed": privacy_policy.get("raw_author_name_removed"),
            "author_hashing": privacy_policy.get("author_hashing"),
            "full_evidence_dump_returned": False,
        },
        package_role=summary.package_role,
        demo_recommendation=summary.demo_recommendation,
        recommended_for_sentigraph_demo=summary.recommended_for_sentigraph_demo,
        sample_quality_label=summary.sample_quality_label,
        index_notes=summary.index_notes,
        index_source="package_index.json" if index_entry else "folder scan fallback",
        index_available=index_available and bool(index_entry),
        index_warning=index_warning,
        recommended_next_action=summary.recommended_next_action,
    )


def validate_external_collector_package(package_name: str) -> ExternalCollectorValidationResult:
    package_dir = _resolve_package_dir(package_name)
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    for file_name in EXPECTED_FILES:
        if not (package_dir / file_name).exists():
            errors.append(_issue("MISSING_EXPECTED_FILE", f"{file_name} is missing", file=file_name))

    manifest = _read_json(package_dir / "manifest.json", errors, "manifest.json")
    validation_report = _read_json(package_dir / "validation_report.json", errors, "validation_report.json")
    evidence_rows = _read_jsonl(package_dir / "evidence_items.jsonl", errors, "evidence_items.jsonl")
    source_rows = _read_jsonl(package_dir / "source_manifest.jsonl", errors, "source_manifest.jsonl")

    if not manifest.get("case_id"):
        errors.append(_issue("MISSING_CASE_ID", "manifest.case_id is required"))
    if not manifest.get("case_title"):
        warnings.append(_issue("MISSING_CASE_TITLE", "manifest.case_title is missing"))
    if not evidence_rows:
        errors.append(_issue("NO_EVIDENCE_ITEMS", "evidence_items.jsonl must contain at least one item"))

    _add_upstream_report_issues(validation_report, warnings, errors)
    _check_evidence_rows(evidence_rows, errors, warnings)

    coverage_text = " ".join(
        [
            str(manifest.get("coverage_note") or ""),
            _safe_excerpt(package_dir / "coverage_note.md", 4000),
            _safe_excerpt(package_dir / "README.md", 4000),
        ]
    ).lower()
    missing_coverage = [phrase for phrase in COVERAGE_PHRASES if phrase not in coverage_text]
    coverage_status = "pass"
    if missing_coverage:
        warnings.append(_issue("COVERAGE_LANGUAGE_INCOMPLETE", "Coverage language is incomplete", missing=missing_coverage))
        coverage_status = "warn"

    privacy_status = "fail" if any(error["code"] in {"FORBIDDEN_EVIDENCE_KEY", "SUSPICIOUS_SECRET_KEY"} for error in errors) else "pass"
    status = "fail" if errors else ("warn" if warnings else "pass")
    return ExternalCollectorValidationResult(
        package_name=package_dir.name,
        status=status,
        errors=errors,
        warnings=warnings,
        counts={
            "evidence_count": len(evidence_rows),
            "source_count": len(source_rows),
            "comment_count": sum(1 for row in evidence_rows if row.get("evidence_type") in {"comment", "reply"}),
            "root_content_count": sum(1 for row in evidence_rows if row.get("is_root_content") is True),
            "errors_count": len(errors),
            "warnings_count": len(warnings),
        },
        privacy_status=privacy_status,
        coverage_status=coverage_status,
        recommended_next_action=_next_action(status, len(warnings)),
    )


def _configured_exports_dir() -> Path | None:
    raw_value = os.environ.get(EXPORTS_ENV_VAR, "").strip()
    if not raw_value:
        return None
    return Path(raw_value).expanduser().resolve()


def _direct_package_dirs(exports_dir: Path) -> list[Path]:
    try:
        return sorted([child for child in exports_dir.iterdir() if child.is_dir()], key=lambda item: item.name.lower())
    except OSError:
        return []


def _read_package_index(exports_dir: Path) -> tuple[dict[str, dict[str, Any]], bool, str]:
    index_path = exports_dir / PACKAGE_INDEX_FILE
    if not index_path.exists():
        return {}, False, ""
    try:
        parsed = json.loads(index_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - malformed local index should not break folder scan.
        return {}, True, f"package_index.json could not be parsed: {type(exc).__name__}"

    if isinstance(parsed, list):
        raw_packages: Any = parsed
    elif isinstance(parsed, dict):
        raw_packages = (
            parsed.get("packages")
            or parsed.get("package_index")
            or parsed.get("export_packages")
            or parsed.get("items")
            or []
        )
    else:
        return {}, True, "package_index.json root must be an object or array."

    if not isinstance(raw_packages, list):
        return {}, True, "package_index.json packages field must be an array."

    entries: dict[str, dict[str, Any]] = {}
    for item in raw_packages:
        if not isinstance(item, dict):
            continue
        package_name = _index_package_name(item)
        if package_name:
            entries[package_name] = item
    return entries, True, ""


def _index_package_name(item: dict[str, Any]) -> str:
    raw_name = str(item.get("package_name") or "").strip()
    if raw_name and PACKAGE_NAME_PATTERN.fullmatch(raw_name) and raw_name not in {".", ".."}:
        return raw_name
    relative_path = str(item.get("package_path_relative") or "").replace("\\", "/").strip("/")
    if not relative_path:
        return ""
    candidate = Path(relative_path).name
    if PACKAGE_NAME_PATTERN.fullmatch(candidate) and candidate not in {".", ".."}:
        return candidate
    return ""


def _resolve_package_dir(package_name: str) -> Path:
    if not PACKAGE_NAME_PATTERN.fullmatch(package_name) or package_name in {".", ".."}:
        raise ValueError("Invalid package name.")
    exports_dir = _configured_exports_dir()
    if not exports_dir:
        raise FileNotFoundError("External collector exports directory is not configured.")
    base_dir = exports_dir.resolve()
    package_dir = (base_dir / package_name).resolve()
    if package_dir.parent != base_dir:
        raise ValueError("Package path must stay inside the configured exports directory.")
    if not package_dir.exists() or not package_dir.is_dir():
        raise FileNotFoundError("Package folder does not exist.")
    return package_dir


def _package_summary(
    package_dir: Path,
    *,
    manifest: dict[str, Any] | None = None,
    validation_report: dict[str, Any] | None = None,
    index_entry: dict[str, Any] | None = None,
    index_available: bool = False,
    index_warning: str = "",
) -> ExternalCollectorPackageSummary:
    index_entry = index_entry if isinstance(index_entry, dict) else {}
    manifest = manifest if manifest is not None else _read_json(package_dir / "manifest.json")
    validation_report = validation_report if validation_report is not None else _read_json(package_dir / "validation_report.json")
    validation_status = str(
        index_entry.get("validation_status")
        or validation_report.get("status")
        or validation_report.get("validation_status")
        or "unknown"
    )
    errors_count = _int_from(index_entry.get("errors_count")) if "errors_count" in index_entry else _issue_count(validation_report, "errors")
    warnings_count = _int_from(index_entry.get("warnings_count")) if "warnings_count" in index_entry else _issue_count(validation_report, "warnings")
    data_scope = manifest.get("data_scope") if isinstance(manifest.get("data_scope"), dict) else {}
    coverage_note = str(manifest.get("coverage_note") or "")
    sample_labels = [label for label in manifest.get("labels", []) if isinstance(label, str)]
    if "selected public sample" in coverage_note.lower() and "selected public sample" not in sample_labels:
        sample_labels.append("selected public sample")
    coverage_warnings = [warning for warning in manifest.get("warnings", []) if isinstance(warning, str)]
    if coverage_note:
        coverage_warnings.append(_truncate(coverage_note, 220))
    status_for_action = "fail" if errors_count else ("warn" if warnings_count else "pass")
    return ExternalCollectorPackageSummary(
        package_name=package_dir.name,
        package_path=str(package_dir),
        manifest_exists=(package_dir / "manifest.json").exists(),
        validation_report_exists=(package_dir / "validation_report.json").exists(),
        case_id=str(index_entry.get("case_id") or manifest.get("case_id") or ""),
        case_title=str(index_entry.get("case_title") or manifest.get("case_title") or ""),
        exported_at=_string_or_none(index_entry.get("exported_at") or manifest.get("exported_at") or manifest.get("generated_at")),
        evidence_count=_int_from(index_entry.get("evidence_count") or data_scope.get("evidence_items_count") or manifest.get("evidence_count")),
        source_count=_int_from(index_entry.get("source_count") or data_scope.get("source_urls_count") or manifest.get("source_count")),
        comment_count=_int_from(index_entry.get("comment_count") or data_scope.get("comment_sample_count")),
        root_count=_int_from(index_entry.get("root_count") or data_scope.get("root_content_count")),
        validation_status=validation_status,
        errors_count=errors_count,
        warnings_count=warnings_count,
        package_role=str(index_entry.get("package_role") or ""),
        demo_recommendation=str(index_entry.get("demo_recommendation") or ""),
        recommended_for_sentigraph_demo=_bool_from(index_entry.get("recommended_for_sentigraph_demo")),
        sample_quality_label=str(index_entry.get("sample_quality_label") or ""),
        index_notes=_truncate(str(index_entry.get("notes") or ""), 500),
        index_available=index_available and bool(index_entry),
        index_warning=index_warning,
        sample_labels=sample_labels,
        coverage_warnings=coverage_warnings[:4],
        recommended_next_action=_next_action(status_for_action, warnings_count),
    )


def _package_sort_key(summary: ExternalCollectorPackageSummary) -> tuple[int, int, int, str, str]:
    recommended_rank = 0 if summary.recommended_for_sentigraph_demo else 1
    demo_rank = 0 if summary.demo_recommendation == "recommended" else 1
    role_rank = PACKAGE_ROLE_PRIORITY.get(summary.package_role, 99)
    exported_desc = _reverse_sort_text(summary.exported_at or "")
    return (recommended_rank, demo_rank, role_rank, exported_desc, summary.package_name.lower())


def _manifest_summary(manifest: dict[str, Any]) -> dict[str, Any]:
    data_scope = manifest.get("data_scope") if isinstance(manifest.get("data_scope"), dict) else {}
    return {
        "package_version": manifest.get("package_version", ""),
        "contract_version": manifest.get("contract_version", ""),
        "case_id": manifest.get("case_id", ""),
        "case_title": manifest.get("case_title", ""),
        "exported_at": manifest.get("exported_at") or manifest.get("generated_at"),
        "evidence_count": data_scope.get("evidence_items_count") or manifest.get("evidence_count", 0),
        "source_count": data_scope.get("source_urls_count") or manifest.get("source_count", 0),
        "comment_sample_count": data_scope.get("comment_sample_count", 0),
        "root_content_count": data_scope.get("root_content_count", 0),
        "coverage_note": _truncate(str(manifest.get("coverage_note") or ""), 500),
    }


def _validation_report_summary(validation_report: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": validation_report.get("status") or validation_report.get("validation_status") or "unknown",
        "errors_count": _issue_count(validation_report, "errors"),
        "warnings_count": _issue_count(validation_report, "warnings"),
        "privacy_status": validation_report.get("privacy_status", "unknown"),
        "coverage_status": validation_report.get("coverage_status", "unknown"),
    }


def _add_upstream_report_issues(
    validation_report: dict[str, Any],
    warnings: list[dict[str, Any]],
    errors: list[dict[str, Any]],
) -> None:
    for item in validation_report.get("errors") or []:
        if isinstance(item, dict):
            errors.append(_issue("UPSTREAM_VALIDATION_ERROR", str(item.get("message") or item.get("code") or "Upstream error")))
    for item in validation_report.get("warnings") or []:
        if isinstance(item, dict):
            warnings.append(_issue("UPSTREAM_VALIDATION_WARNING", str(item.get("message") or item.get("code") or "Upstream warning")))


def _check_evidence_rows(rows: list[dict[str, Any]], errors: list[dict[str, Any]], warnings: list[dict[str, Any]]) -> None:
    evidence_ids: set[str] = set()
    duplicate_groups: Counter[str] = Counter()
    for index, row in enumerate(rows, start=1):
        evidence_id = str(row.get("evidence_id") or "").strip()
        if not evidence_id:
            errors.append(_issue("EMPTY_EVIDENCE_ID", "evidence_id is required", row=index))
        elif evidence_id in evidence_ids:
            errors.append(_issue("DUPLICATE_EVIDENCE_ID", "evidence_id must be unique", row=index))
        evidence_ids.add(evidence_id)

        forbidden_keys = sorted(FORBIDDEN_EVIDENCE_KEYS.intersection(row.keys()))
        if forbidden_keys:
            errors.append(_issue("FORBIDDEN_EVIDENCE_KEY", "Evidence row contains forbidden raw identity keys", row=index, fields=forbidden_keys))

        secret_keys = sorted(key for key in _nested_keys(row) if key.lower() in SUSPICIOUS_SECRET_KEYS)
        if secret_keys:
            errors.append(_issue("SUSPICIOUS_SECRET_KEY", "Evidence row contains suspicious secret/session keys", row=index, fields=secret_keys))

        if row.get("raw_author_id_removed") is False or row.get("raw_author_name_removed") is False:
            errors.append(_issue("RAW_AUTHOR_MARKED_PRESENT", "Raw author fields must be removed before bridge review", row=index))

        if not row.get("coverage_note"):
            warnings.append(_issue("MISSING_ROW_COVERAGE_NOTE", "Evidence row has no coverage_note", row=index))
        if row.get("duplicate_group_id"):
            duplicate_groups[str(row.get("duplicate_group_id"))] += 1

    if duplicate_groups and max(duplicate_groups.values()) > max(5, len(rows) * 0.25):
        warnings.append(_issue("LARGE_DUPLICATE_GROUP", "One duplicate group is unusually large"))


def _read_json(path: Path, errors: list[dict[str, Any]] | None = None, file_name: str | None = None) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        parsed = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - bridge reports local package parse issues.
        if errors is not None:
            errors.append(_issue("JSON_PARSE_FAILED", f"{file_name or path.name} could not be parsed", error_type=type(exc).__name__))
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _read_jsonl(path: Path, errors: list[dict[str, Any]], file_name: str) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    try:
        content = path.read_text(encoding="utf-8-sig")
    except Exception as exc:  # noqa: BLE001
        errors.append(_issue("FILE_READ_FAILED", f"{file_name} could not be read", error_type=type(exc).__name__))
        return rows
    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
        except Exception as exc:  # noqa: BLE001
            errors.append(_issue("JSONL_PARSE_FAILED", f"{file_name}:{line_number} could not be parsed", line=line_number, error_type=type(exc).__name__))
            continue
        if isinstance(parsed, dict):
            rows.append(parsed)
        else:
            errors.append(_issue("JSONL_ROW_NOT_OBJECT", f"{file_name}:{line_number} is not an object", line=line_number))
    return rows


def _safe_excerpt(path: Path, limit: int) -> str:
    if not path.exists() or not path.is_file():
        return ""
    try:
        return _truncate(path.read_text(encoding="utf-8", errors="replace"), limit)
    except OSError:
        return ""


def _nested_keys(value: Any) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.append(str(key))
            keys.extend(_nested_keys(nested))
    elif isinstance(value, list):
        for item in value:
            keys.extend(_nested_keys(item))
    return keys


def _issue(code: str, message: str, **detail: Any) -> dict[str, Any]:
    return {"code": code, "message": message, "detail": detail}


def _issue_count(report: dict[str, Any], key: str) -> int:
    value = report.get(f"{key}_count")
    if value is None:
        value = report.get(key)
    if isinstance(value, list):
        return len(value)
    return _int_from(value)


def _int_from(value: Any) -> int:
    try:
        return max(0, int(float(str(value))))
    except (TypeError, ValueError):
        return 0


def _bool_from(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "recommended"}
    return False


def _string_or_none(value: Any) -> str | None:
    if value is None or value == "":
        return None
    return str(value)


def _truncate(value: str, limit: int) -> str:
    text = value.strip()
    if len(text) <= limit:
        return text
    return f"{text[:limit].rstrip()}..."


def _reverse_sort_text(value: str) -> str:
    return "".join(chr(0x10FFFF - ord(char)) for char in value)


def _next_action(status: str, warnings_count: int) -> str:
    if status == "fail":
        return "fail_validation"
    if warnings_count:
        return "sample_size_warning"
    if status == "pass":
        return "ready_for_sample_review"
    return "needs_manual_review"
