from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED_PACKAGE_FILES = [
    "manifest.json",
    "source_manifest.jsonl",
    "evidence_items.jsonl",
    "evidence_items.csv",
    "collection_log.jsonl",
    "coverage_note.md",
    "README.md",
    "validation_report.json",
    "validation_report.md",
]

EVIDENCE_REQUIRED_KEYS = [
    "evidence_id",
    "case_id",
    "platform",
    "source_type",
    "acquisition_mode",
    "provenance_type",
    "verification_status",
    "trust_label",
    "trust_score",
    "review_status",
    "evidence_type",
    "title",
    "body_text",
    "comment_text",
    "language",
    "source_url",
    "url",
    "root_id",
    "parent_id",
    "created_at",
    "collected_at",
    "author_platform_hash",
    "author_hash_method",
    "author_identity_confidence",
    "raw_author_id_removed",
    "raw_author_name_removed",
    "like_count",
    "reply_count",
    "share_count",
    "view_count",
    "content_hash",
    "normalized_content_hash",
    "canonical_url_hash",
    "duplicate_group_id",
    "duplicate_count",
    "risk_flags",
    "content_visibility",
    "access_scope",
    "source_capture_method",
    "coverage_note",
    "raw_data_safe",
    "ingestion_metadata",
]

OPTIONAL_HINT_KEYS = [
    "stance_hint",
    "camp_state_hint",
    "emotion_hint",
    "topic_hint",
    "people_cluster_hint",
    "influence_core_candidate",
    "influence_core_type",
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
    "token",
    "cookie",
    "password",
    "session",
    "storagestate",
    "profilepath",
    "sessdata",
    "bili_jct",
}

COVERAGE_PHRASES = {
    "selected_public_sample": ["selected public sample", "selected sample"],
    "not_full_web": ["not full-web", "not full web"],
    "not_full_platform": ["not full-platform", "not full platform"],
    "not_full_thread": ["not full-thread", "not full thread"],
    "not_official_verification": ["not official verification"],
    "not_causal_proof": ["not causal proof"],
}


def issue(code: str, message: str, *, detail: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"code": code, "message": message, "detail": detail or {}}


def read_json(path: Path, errors: list[dict[str, Any]]) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - CLI validator should report parse failures.
        errors.append(issue("JSON_PARSE_FAILED", f"Could not parse {path.name}", detail={"file": path.name, "error_type": type(exc).__name__}))
        return {}


def read_jsonl(path: Path, errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        content = path.read_text(encoding="utf-8-sig")
    except Exception as exc:  # noqa: BLE001
        errors.append(issue("FILE_READ_FAILED", f"Could not read {path.name}", detail={"file": path.name, "error_type": type(exc).__name__}))
        return rows
    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
        except Exception as exc:  # noqa: BLE001
            errors.append(issue("JSONL_PARSE_FAILED", f"Could not parse {path.name}:{line_number}", detail={"file": path.name, "line": line_number, "error_type": type(exc).__name__}))
            continue
        if not isinstance(parsed, dict):
            errors.append(issue("JSONL_ROW_NOT_OBJECT", f"{path.name}:{line_number} is not a JSON object", detail={"file": path.name, "line": line_number}))
            continue
        rows.append(parsed)
    return rows


def nested_keys(value: Any) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.append(str(key))
            keys.extend(nested_keys(nested))
    elif isinstance(value, list):
        for item in value:
            keys.extend(nested_keys(item))
    return keys


def count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(key) or "(empty)") for row in rows).items()))


def numeric(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str) and value.strip():
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "used", "enabled"}
    return bool(value)


def add_validation_report_issues(validation_report: dict[str, Any], warnings: list[dict[str, Any]], errors: list[dict[str, Any]]) -> None:
    for item in validation_report.get("errors") or []:
        errors.append(issue("UPSTREAM_VALIDATION_ERROR", str(item.get("message") or item.get("code") or "Upstream validation error"), detail={"code": item.get("code")}))
    for item in validation_report.get("warnings") or []:
        warnings.append(issue("UPSTREAM_VALIDATION_WARNING", str(item.get("message") or item.get("code") or "Upstream validation warning"), detail={"code": item.get("code")}))


def check_manifest(manifest: dict[str, Any], warnings: list[dict[str, Any]], errors: list[dict[str, Any]]) -> None:
    if manifest.get("package_version") != "sentigraph_external_export_v1":
        errors.append(issue("INVALID_PACKAGE_VERSION", "manifest.package_version must be sentigraph_external_export_v1"))
    for key in ["contract_version", "case_id", "case_title", "data_scope", "coverage_note"]:
        if key not in manifest or manifest.get(key) in (None, "", {}):
            errors.append(issue("MISSING_MANIFEST_FIELD", f"manifest.{key} is required", detail={"field": key}))
    if "privacy_policy" not in manifest:
        warnings.append(issue("MISSING_PRIVACY_POLICY", "manifest.privacy_policy is absent"))


def check_counts(manifest: dict[str, Any], sources: list[dict[str, Any]], evidence: list[dict[str, Any]], warnings: list[dict[str, Any]]) -> None:
    data_scope = manifest.get("data_scope") if isinstance(manifest.get("data_scope"), dict) else {}
    expected_actual = {
        "evidence_items_count": len(evidence),
        "source_urls_count": len(sources),
        "comment_sample_count": sum(1 for row in evidence if row.get("evidence_type") in {"comment", "reply"}),
        "root_content_count": sum(1 for row in evidence if row.get("is_root_content") is True),
    }
    for field, actual in expected_actual.items():
        expected = data_scope.get(field)
        if expected is None:
            warnings.append(issue("MISSING_DATA_SCOPE_COUNT", f"manifest.data_scope.{field} is absent", detail={"field": field, "actual": actual}))
            continue
        if numeric(expected) != float(actual):
            warnings.append(issue("DATA_SCOPE_COUNT_MISMATCH", f"manifest.data_scope.{field} does not match parsed records", detail={"field": field, "manifest": expected, "actual": actual}))


def check_evidence_items(evidence: list[dict[str, Any]], warnings: list[dict[str, Any]], errors: list[dict[str, Any]]) -> None:
    ids: set[str] = set()
    duplicate_counts: list[float] = []
    duplicate_groups: Counter[str] = Counter()
    for index, row in enumerate(evidence, start=1):
        evidence_id = str(row.get("evidence_id") or "").strip()
        if not evidence_id:
            errors.append(issue("EMPTY_EVIDENCE_ID", "evidence_id must not be empty", detail={"row": index}))
        elif evidence_id in ids:
            errors.append(issue("DUPLICATE_EVIDENCE_ID", "evidence_id must be unique", detail={"row": index}))
        ids.add(evidence_id)

        missing = [key for key in EVIDENCE_REQUIRED_KEYS if key not in row]
        if missing:
            errors.append(issue("MISSING_EVIDENCE_KEYS", "Evidence item is missing required keys", detail={"row": index, "missing_keys": missing}))

        missing_hints = [key for key in OPTIONAL_HINT_KEYS if key not in row]
        if missing_hints:
            warnings.append(issue("MISSING_OPTIONAL_HINT_KEYS", "Evidence item is missing optional hint keys", detail={"row": index, "missing_keys": missing_hints}))

        trust_score = numeric(row.get("trust_score"))
        if trust_score is None or trust_score < 0 or trust_score > 1:
            errors.append(issue("INVALID_TRUST_SCORE", "trust_score must be numeric within 0..1", detail={"row": index}))
        if not row.get("trust_label"):
            errors.append(issue("MISSING_TRUST_LABEL", "trust_label is required", detail={"row": index}))
        if not row.get("review_status"):
            errors.append(issue("MISSING_REVIEW_STATUS", "review_status is required", detail={"row": index}))

        forbidden = sorted(FORBIDDEN_EVIDENCE_KEYS.intersection(row.keys()))
        if forbidden:
            errors.append(issue("FORBIDDEN_EVIDENCE_KEY", "Evidence item contains forbidden raw identity field names", detail={"row": index, "fields": forbidden}))

        secret_like = sorted(key for key in nested_keys(row) if key.lower() in SUSPICIOUS_SECRET_KEYS)
        if secret_like:
            errors.append(issue("SUSPICIOUS_SECRET_KEY", "Evidence item contains suspicious secret/session field names", detail={"row": index, "fields": secret_like}))

        if row.get("raw_author_id_removed") is not True:
            errors.append(issue("RAW_AUTHOR_ID_NOT_MARKED_REMOVED", "raw_author_id_removed must be true", detail={"row": index}))
        if row.get("raw_author_name_removed") is not True:
            errors.append(issue("RAW_AUTHOR_NAME_NOT_MARKED_REMOVED", "raw_author_name_removed must be true", detail={"row": index}))

        author_hash = str(row.get("author_platform_hash") or "").strip()
        if author_hash and (author_hash.startswith(("http://", "https://")) or (" " not in author_hash and not author_hash.startswith("sha256:") and len(author_hash) < 32)):
            warnings.append(issue("AUTHOR_HASH_LOOKS_RAW", "author_platform_hash may not be a hash-like anonymized value", detail={"row": index}))
        display_label = str(row.get("author_display_label") or "").strip().lower()
        if display_label and not (display_label.startswith("anonymous") or display_label.startswith("synthetic") or display_label in {"unknown", "redacted"}):
            warnings.append(issue("AUTHOR_DISPLAY_LABEL_NEEDS_REVIEW", "author_display_label should be synthetic or redacted", detail={"row": index}))

        duplicate_count = numeric(row.get("duplicate_count"))
        if duplicate_count is None:
            errors.append(issue("INVALID_DUPLICATE_COUNT", "duplicate_count must be numeric", detail={"row": index}))
        else:
            duplicate_counts.append(duplicate_count)
            if duplicate_count < 0:
                errors.append(issue("NEGATIVE_DUPLICATE_COUNT", "duplicate_count must not be negative", detail={"row": index}))
        duplicate_group_id = str(row.get("duplicate_group_id") or "").strip()
        if not duplicate_group_id:
            errors.append(issue("MISSING_DUPLICATE_GROUP_ID", "duplicate_group_id is required", detail={"row": index}))
        else:
            duplicate_groups[duplicate_group_id] += 1

        if str(row.get("review_status") or "").lower() == "rejected" and str(row.get("trust_label") or "").lower() != "rejected" and not row.get("excluded_from_active_evidence"):
            warnings.append(issue("REJECTED_EVIDENCE_ACTIVE_WEIGHT_UNCLEAR", "Rejected evidence should be excluded or labeled rejected", detail={"row": index}))

    if evidence and duplicate_groups:
        largest_group = max(duplicate_groups.values())
        if largest_group > max(5, len(evidence) * 0.25):
            warnings.append(issue("LARGE_DUPLICATE_GROUP", "Many rows share the same duplicate_group_id", detail={"largest_group_size": largest_group}))


def check_coverage(package_dir: Path, manifest: dict[str, Any], warnings: list[dict[str, Any]], errors: list[dict[str, Any]]) -> str:
    parts = [str(manifest.get("coverage_note") or "")]
    coverage_path = package_dir / "coverage_note.md"
    if coverage_path.exists():
        parts.append(coverage_path.read_text(encoding="utf-8", errors="replace"))
    coverage_text = "\n".join(parts).lower()
    missing: list[str] = []
    for key, variants in COVERAGE_PHRASES.items():
        if not any(variant in coverage_text for variant in variants):
            missing.append(key)
    if missing:
        warnings.append(issue("COVERAGE_LANGUAGE_MISSING", "Coverage language is incomplete", detail={"missing": missing}))
        return "warn"
    return "pass"


def check_sources(sources: list[dict[str, Any]], warnings: list[dict[str, Any]], errors: list[dict[str, Any]]) -> None:
    for index, row in enumerate(sources, start=1):
        for key in ["source_id", "platform", "source_type", "collection_method"]:
            if not row.get(key):
                errors.append(issue("MISSING_SOURCE_FIELD", f"source_manifest row requires {key}", detail={"row": index, "field": key}))
        if not row.get("source_url") and not (row.get("skipped") or row.get("coverage_note") or row.get("skip_reason")):
            errors.append(issue("SOURCE_URL_OR_LIMITATION_REQUIRED", "source_url is required unless skipped/limited source is documented", detail={"row": index}))
        for key in ["content_visibility", "access_scope"]:
            value = str(row.get(key) or "").lower()
            if value and value != "public" and not (row.get("coverage_note") or row.get("skip_reason")):
                warnings.append(issue("SOURCE_ACCESS_LIMITATION_REVIEW", f"source_manifest {key} is not public", detail={"row": index, "field": key}))
        for key in ["cookie_used", "captcha_bypass_used", "anti_bot_bypass_used", "login_required"]:
            if truthy(row.get(key)):
                errors.append(issue("FORBIDDEN_SOURCE_METHOD", f"source_manifest should not indicate {key}", detail={"row": index, "field": key}))


def check_case_relevance(evidence: list[dict[str, Any]], case_keywords: list[str], warnings: list[dict[str, Any]]) -> dict[str, Any]:
    if not case_keywords:
        return {"status": "not_run", "match_rate": None, "unrelated_item_count": None}
    lowered_keywords = [keyword.lower() for keyword in case_keywords if keyword.strip()]
    roots = [row for row in evidence if row.get("is_root_content") is True or row.get("influence_core_candidate") is True]
    if not roots:
        warnings.append(issue("CASE_RELEVANCE_NO_ROOTS", "No root / InfluenceCore candidate rows were available for case relevance checks"))
        return {"status": "warn", "match_rate": 0.0, "unrelated_item_count": 0}
    matched = 0
    for row in roots:
        haystack = " ".join(str(row.get(key) or "") for key in ["title", "body_text", "source_url", "claim_summary"]).lower()
        if any(keyword in haystack for keyword in lowered_keywords):
            matched += 1
    match_rate = matched / len(roots)
    unrelated = len(roots) - matched
    if match_rate < 0.5:
        warnings.append(issue("CASE_RELEVANCE_LOW", "Root case relevance match rate is low", detail={"match_rate": match_rate, "unrelated_root_count": unrelated}))
        status = "warn"
    else:
        status = "pass"
    return {"status": status, "match_rate": match_rate, "unrelated_item_count": unrelated, "root_count": len(roots)}


def validate_package(package_path: str | Path, case_keywords: list[str] | None = None, strict: bool = False) -> dict[str, Any]:
    package_dir = Path(package_path)
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    if not package_dir.exists() or not package_dir.is_dir():
        errors.append(issue("PACKAGE_FOLDER_NOT_FOUND", "Package folder does not exist", detail={"path": str(package_dir)}))

    missing_files = [file_name for file_name in REQUIRED_PACKAGE_FILES if not (package_dir / file_name).exists()]
    for file_name in missing_files:
        errors.append(issue("MISSING_REQUIRED_FILE", "Required package file is missing", detail={"file": file_name}))

    manifest = read_json(package_dir / "manifest.json", errors) if (package_dir / "manifest.json").exists() else {}
    validation_report = read_json(package_dir / "validation_report.json", errors) if (package_dir / "validation_report.json").exists() else {}
    sources = read_jsonl(package_dir / "source_manifest.jsonl", errors) if (package_dir / "source_manifest.jsonl").exists() else []
    evidence = read_jsonl(package_dir / "evidence_items.jsonl", errors) if (package_dir / "evidence_items.jsonl").exists() else []
    collection_log = read_jsonl(package_dir / "collection_log.jsonl", errors) if (package_dir / "collection_log.jsonl").exists() else []

    add_validation_report_issues(validation_report, warnings, errors)
    if manifest:
        check_manifest(manifest, warnings, errors)
        check_counts(manifest, sources, evidence, warnings)
    check_evidence_items(evidence, warnings, errors)
    coverage_status = check_coverage(package_dir, manifest, warnings, errors) if package_dir.exists() else "fail"
    check_sources(sources, warnings, errors)
    case_relevance = check_case_relevance(evidence, case_keywords or [], warnings)

    duplicate_group_counter = Counter(str(row.get("duplicate_group_id") or "") for row in evidence if row.get("duplicate_group_id"))
    duplicate_counts = [numeric(row.get("duplicate_count")) or 0 for row in evidence]
    privacy_status = "fail" if any(error["code"] in {"FORBIDDEN_EVIDENCE_KEY", "SUSPICIOUS_SECRET_KEY", "RAW_AUTHOR_ID_NOT_MARKED_REMOVED", "RAW_AUTHOR_NAME_NOT_MARKED_REMOVED"} for error in errors) else "pass"

    status = "fail" if errors or (strict and warnings) else ("warn" if warnings else "pass")
    return {
        "package_path": str(package_dir),
        "case_id": manifest.get("case_id", ""),
        "case_title": manifest.get("case_title", ""),
        "status": status,
        "errors_count": len(errors),
        "warnings_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "evidence_count": len(evidence),
        "source_count": len(sources),
        "root_content_count": sum(1 for row in evidence if row.get("is_root_content") is True),
        "comment_count": sum(1 for row in evidence if row.get("evidence_type") in {"comment", "reply"}),
        "collection_log_count": len(collection_log),
        "distribution": {
            "platform": count_by(evidence, "platform"),
            "evidence_type": count_by(evidence, "evidence_type"),
            "trust_label": count_by(evidence, "trust_label"),
            "review_status": count_by(evidence, "review_status"),
        },
        "privacy_status": privacy_status,
        "coverage_status": coverage_status,
        "case_relevance": case_relevance,
        "deduplication": {
            "duplicate_group_count": len(duplicate_group_counter),
            "max_duplicate_count": max(duplicate_counts) if duplicate_counts else 0,
            "largest_duplicate_group_size": max(duplicate_group_counter.values()) if duplicate_group_counter else 0,
        },
        "low_trust": {
            "medium_low": sum(1 for row in evidence if row.get("trust_label") == "medium_low"),
            "low": sum(1 for row in evidence if row.get("trust_label") == "low"),
            "rejected": sum(1 for row in evidence if row.get("review_status") == "rejected" or row.get("trust_label") == "rejected"),
            "review_needed": sum(1 for row in evidence if row.get("review_status") == "review_needed"),
        },
    }


def print_text_summary(result: dict[str, Any]) -> None:
    print(f"Package: {result['package_path']}")
    print(f"Case: {result.get('case_id')} - {result.get('case_title')}")
    print(f"Validation status: {result['status']}")
    print(f"Errors: {result['errors_count']}")
    print(f"Warnings: {result['warnings_count']}")
    print(f"Evidence: {result['evidence_count']}")
    print(f"Sources: {result['source_count']}")
    print(f"Roots: {result['root_content_count']}")
    print(f"Comments: {result['comment_count']}")
    print(f"Privacy status: {result['privacy_status']}")
    print(f"Coverage status: {result['coverage_status']}")
    case_status = result.get("case_relevance", {}).get("status")
    if case_status and case_status != "not_run":
        match_rate = result["case_relevance"].get("match_rate")
        print(f"Case relevance: {case_status} ({match_rate:.0%} root match rate)")
    print("Distribution by platform:")
    for key, value in result["distribution"]["platform"].items():
        print(f"  {key}: {value}")
    print("Distribution by evidence_type:")
    for key, value in result["distribution"]["evidence_type"].items():
        print(f"  {key}: {value}")
    print("Distribution by trust_label:")
    for key, value in result["distribution"]["trust_label"].items():
        print(f"  {key}: {value}")
    print("Distribution by review_status:")
    for key, value in result["distribution"]["review_status"].items():
        print(f"  {key}: {value}")
    if result["errors"]:
        print("Errors:")
        for item in result["errors"]:
            print(f"  - {item['code']}: {item['message']}")
    if result["warnings"]:
        print("Warnings:")
        for item in result["warnings"]:
            print(f"  - {item['code']}: {item['message']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a local Sentigraph Evidence Export v1 package without importing it.")
    parser.add_argument("package_folder", help="External evidence package folder to validate.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary to stdout.")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero when warnings are present.")
    parser.add_argument("--case-keyword", action="append", default=[], help="Case keyword for root evidence relevance checks. Can be repeated.")
    args = parser.parse_args(argv)

    result = validate_package(args.package_folder, case_keywords=args.case_keyword, strict=args.strict)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text_summary(result)
    return 1 if result["status"] == "fail" or (args.strict and result["warnings_count"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
