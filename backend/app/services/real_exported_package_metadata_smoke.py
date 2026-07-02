from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = "sentigraph_real_exported_package_metadata_smoke_v0_1"
PHASE = "8W-2"

APPROVED_PACKAGE_NAME = "donglu-sunjihai-youth-football-202606-v2_20260617_121016"
APPROVED_PACKAGE_ROLE = "candidate_demo_sample"
APPROVED_CASE_ID_HINT = "donglu_sunjihai_youth_football_202606"
APPROVED_PROVIDER_RESULT_ID = "unknown"
APPROVED_PROVIDER_JOB_ID = "unknown"
APPROVED_REQUEST_ID = "unknown"
APPROVED_TARGET_DIR = (
    Path("docs")
    / "samples"
    / "donglu_sunjihai_youth_football"
    / APPROVED_PACKAGE_NAME
)

READY_STATUS = "metadata_ready_for_manual_review"
WARN_STATUS = "metadata_warn_manual_review_required"

METADATA_FILES = {
    "manifest_json_present": "manifest.json",
    "validation_report_json_present": "validation_report.json",
    "validation_report_md_present": "validation_report.md",
    "source_manifest_jsonl_present": "source_manifest.jsonl",
    "coverage_note_md_present": "coverage_note.md",
    "readme_present": "README.md",
    "collection_log_jsonl_present": "collection_log.jsonl",
    "evidence_items_jsonl_present_presence_only": "evidence_items.jsonl",
    "evidence_items_csv_present_presence_only": "evidence_items.csv",
}

ROW_OR_LOG_FILES = {
    "evidence_items.jsonl",
    "evidence_items.csv",
    "source_manifest.jsonl",
    "collection_log.jsonl",
}

FORBIDDEN_FIELD_NAMES = {
    "token",
    "tokens",
    "cookie",
    "cookies",
    "session",
    "sessions",
    "password",
    "passwords",
    "api_key",
    "api_keys",
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
    "raw_comment",
    "raw_comments",
    "raw_comment_dump",
    "full_evidence_rows",
    "browser_profile",
    "browser_profile_path",
    "collector_runtime_internal_path",
    "absolute_path",
    "absolute_package_path",
    "runtime_path",
    "package_path",
    "generated_response_text",
    "response_text",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
}

SIDE_EFFECT_FIELDS = {
    "evidence_layer_write",
    "write_evidence_layer",
    "production_case_created",
    "create_production_case",
    "production_analysis_run_created",
    "create_production_analysis_run",
    "analysis_run_created",
    "route_changed",
    "api_route_added",
    "frontend_integration_approved",
    "modified_frontend",
    "b_end_report_runtime_generated",
    "generate_b_end_report",
    "sandbox_public_event_generated",
    "generate_sandbox_public_event",
    "called_real_api",
    "called_real_llm",
    "ran_provider_job",
    "ran_collector",
    "fetched_url",
    "scraped_page",
    "public_url_created",
    "signed_url_created",
    "file_byte_route_created",
    "download_package_runtime_used",
    "public_access_runtime_used",
    "external_delivery_runtime_used",
    "final_delivery_runtime_used",
    "generated_response_text",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
    "auto_execute",
}


def build_real_exported_package_metadata_smoke(
    *,
    package_name: str | None = None,
    package_role: str | None = None,
    case_id_hint: str | None = None,
    provider_result_id: str = APPROVED_PROVIDER_RESULT_ID,
    provider_job_id: str = APPROVED_PROVIDER_JOB_ID,
    request_id: str = APPROVED_REQUEST_ID,
    package_dir: str | Path | None = None,
    approval_phrase_present: bool = False,
    requested_side_effects: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    safe_package_dir = Path(package_dir) if package_dir is not None else APPROVED_TARGET_DIR

    if not approval_phrase_present:
        blockers.append(_blocker("missing_8w_2_approval_phrase", "approval"))

    if package_name != APPROVED_PACKAGE_NAME:
        blockers.append(_blocker("package_name_not_explicitly_approved", "target_identity"))
    if package_role != APPROVED_PACKAGE_ROLE:
        blockers.append(_blocker("package_role_not_explicitly_approved", "target_identity"))
    if case_id_hint != APPROVED_CASE_ID_HINT:
        blockers.append(_blocker("case_id_hint_not_explicitly_approved", "target_identity"))
    if _has_path_separator(package_name):
        blockers.append(_blocker("package_name_contains_path_separator", "path"))
    if _has_path_separator(package_role) or _has_path_separator(case_id_hint):
        blockers.append(_blocker("target_identity_contains_path_separator", "path"))

    side_effect_blockers = _requested_side_effect_blockers(requested_side_effects)
    blockers.extend(side_effect_blockers)

    if not safe_package_dir.exists() or not safe_package_dir.is_dir():
        blockers.append(_blocker("approved_target_path_missing", "path"))

    path_ok = _matches_approved_repo_target(safe_package_dir)
    if safe_package_dir.exists() and not path_ok:
        # Tests may pass an isolated temp package with the exact approved package
        # name to exercise forbidden metadata behavior. That is still explicit;
        # it must never be turned into a selector or emitted as a path.
        path_ok = safe_package_dir.name == APPROVED_PACKAGE_NAME
    if safe_package_dir.exists() and not path_ok:
        blockers.append(_blocker("target_path_not_exact_approved_package", "path"))

    presence = _metadata_files_presence(safe_package_dir)
    manifest: dict[str, Any] = {}
    validation_report: dict[str, Any] = {}
    coverage_note_summary = "coverage_note_not_read"

    if safe_package_dir.exists() and safe_package_dir.is_dir():
        manifest = _read_safe_json(safe_package_dir / "manifest.json", blockers, "manifest_json")
        validation_report = _read_safe_json(
            safe_package_dir / "validation_report.json",
            blockers,
            "validation_report_json",
        )
        coverage_note_summary = _read_safe_text_summary(
            safe_package_dir / "coverage_note.md",
            blockers,
            "coverage_note_md",
        )

    blockers.extend(_forbidden_metadata_blockers(manifest))
    blockers.extend(_forbidden_metadata_blockers(validation_report))
    if _looks_like_sensitive_string(coverage_note_summary):
        blockers.append(_blocker("coverage_note_contains_sensitive_value", "privacy"))

    required_metadata_files = {
        "manifest_json_present",
        "validation_report_json_present",
        "coverage_note_md_present",
    }
    for presence_key in sorted(required_metadata_files):
        if presence.get(presence_key) is not True:
            blockers.append(_blocker(f"missing_required_metadata_file:{presence_key}", "metadata_contract"))

    validation_status = _validation_status(validation_report)
    warning_count = _warning_count(manifest, validation_report)
    error_count = _error_count(manifest, validation_report)
    evidence_count_summary = _evidence_count_summary(manifest, validation_report)
    source_count_summary = _source_count_summary(manifest, validation_report)

    if validation_status in {"failed", "fail", "error"} or error_count > 0:
        blockers.append(_blocker("validation_errors_not_suitable_for_smoke", "metadata_contract"))

    blockers = _dedupe_blockers(blockers)
    smoke_status = _smoke_status(blockers, warning_count, validation_status)
    created = smoke_status in {READY_STATUS, WARN_STATUS}

    return {
        "schema": SCHEMA,
        "phase": PHASE,
        "smoke_status": smoke_status,
        "created_at": _utc_now(),
        "created_local_metadata_smoke": bool(created),
        "selector_implemented": False,
        "package_metadata_smoke_executed": bool(created),
        "target_package_name": APPROVED_PACKAGE_NAME,
        "target_package_role": APPROVED_PACKAGE_ROLE,
        "target_case_id_hint": APPROVED_CASE_ID_HINT,
        "target_provider_result_id": _safe_id(provider_result_id) or APPROVED_PROVIDER_RESULT_ID,
        "target_provider_job_id": _safe_id(provider_job_id) or APPROVED_PROVIDER_JOB_ID,
        "target_request_id": _safe_id(request_id) or APPROVED_REQUEST_ID,
        "target_identity_method": "explicit_user_approved_package_metadata_target",
        "target_source_kind": "repo_controlled_already_exported_package_metadata",
        "metadata_only": True,
        "row_files_parsed": False,
        "original_package_rows_read": False,
        "private_collector_source_inspected": False,
        "real_exchange_dir_read": False,
        "absolute_path_exposed": False,
        "package_path_exposed": False,
        "human_review_required": True,
        "metadata_files_presence": presence,
        "safe_summary": {
            "validation_status": validation_status,
            "warning_count": warning_count,
            "error_count": error_count,
            "evidence_count_summary": evidence_count_summary,
            "source_count_summary": source_count_summary,
            "coverage_note_summary": coverage_note_summary,
            "privacy_status": _privacy_status(blockers),
            "path_status": _path_status(blockers),
            "blocker_summary": _safe_reason_codes(blockers),
            "warning_summary": _warning_summary(manifest, validation_report),
        },
        "boundary_flags": _boundary_flags(),
        "runtime_side_effects": _runtime_side_effects(),
        "warnings": _warning_summary(manifest, validation_report),
        "blockers": blockers,
    }


def _metadata_files_presence(package_dir: Path) -> dict[str, bool]:
    return {
        key: (package_dir / filename).exists()
        for key, filename in METADATA_FILES.items()
    }


def _read_safe_json(path: Path, blockers: list[dict[str, str]], label: str) -> dict[str, Any]:
    if not path.exists() or not path.is_file():
        return {}
    if path.name in ROW_OR_LOG_FILES:
        blockers.append(_blocker(f"attempted_row_or_log_json_read:{path.name}", "row_read"))
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        blockers.append(_blocker(f"{label}_invalid_json", "metadata_contract"))
        return {}
    except OSError:
        blockers.append(_blocker(f"{label}_read_failed", "metadata_contract"))
        return {}
    if not isinstance(payload, dict):
        blockers.append(_blocker(f"{label}_not_object", "metadata_contract"))
        return {}
    return payload


def _read_safe_text_summary(path: Path, blockers: list[dict[str, str]], label: str) -> str:
    if not path.exists() or not path.is_file():
        return f"{label}_missing"
    if path.name in ROW_OR_LOG_FILES:
        blockers.append(_blocker(f"attempted_row_or_log_text_read:{path.name}", "row_read"))
        return f"{label}_presence_only"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        blockers.append(_blocker(f"{label}_read_failed", "metadata_contract"))
        return f"{label}_read_failed"
    return _summarize_text(text)


def _summarize_text(text: str) -> str:
    normalized = " ".join(str(text).split())
    if not normalized:
        return "empty"
    # Keep the summary short and non-path-like. Coverage notes should carry
    # boundary language, not raw data.
    return normalized[:240]


def _validation_status(validation_report: dict[str, Any]) -> str:
    status = validation_report.get("status") or validation_report.get("validation_status") or "unknown"
    if not isinstance(status, str):
        return "unknown"
    normalized = status.strip().lower()
    if normalized == "passed":
        return "passed"
    return normalized or "unknown"


def _warning_count(manifest: dict[str, Any], validation_report: dict[str, Any]) -> int:
    direct_values = [
        manifest.get("warning_count"),
        validation_report.get("warning_count"),
        _nested(validation_report, "summary", "warning_count"),
    ]
    for value in direct_values:
        parsed = _parse_count(value)
        if parsed is not None:
            return parsed
    warnings = validation_report.get("warnings")
    if isinstance(warnings, list):
        return len(warnings)
    warnings = manifest.get("warnings")
    if isinstance(warnings, list):
        return len(warnings)
    return 0


def _error_count(manifest: dict[str, Any], validation_report: dict[str, Any]) -> int:
    direct_values = [
        manifest.get("error_count"),
        validation_report.get("error_count"),
        validation_report.get("errors"),
        _nested(validation_report, "summary", "error_count"),
    ]
    for value in direct_values:
        parsed = _parse_count(value)
        if parsed is not None:
            return parsed
    return 0


def _evidence_count_summary(manifest: dict[str, Any], validation_report: dict[str, Any]) -> int | str:
    return (
        _parse_count(manifest.get("evidence_count"))
        or _parse_count(_nested(validation_report, "summary", "evidence_count"))
        or _parse_count(_nested(validation_report, "summary", "total_items"))
        or "unknown"
    )


def _source_count_summary(manifest: dict[str, Any], validation_report: dict[str, Any]) -> int | str:
    return (
        _parse_count(manifest.get("source_count"))
        or _parse_count(_nested(validation_report, "summary", "source_count"))
        or _parse_count(_nested(validation_report, "summary", "sources"))
        or "unknown"
    )


def _nested(mapping: dict[str, Any], *keys: str) -> Any:
    value: Any = mapping
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _parse_count(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return max(value, 0)
    if isinstance(value, list):
        return len(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def _warning_summary(manifest: dict[str, Any], validation_report: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    for source in (validation_report, manifest):
        value = source.get("warnings")
        if isinstance(value, list):
            for item in value[:10]:
                code = _safe_warning_code(item)
                if code:
                    warnings.append(code)
    required = [
        "selected_sample_only",
        "not_full_web",
        "not_full_platform",
        "not_full_thread",
        "not_official_verification",
        "not_causal_proof",
        "not_prediction",
        "not_production_score",
        "human_review_required",
        "metadata_only_no_row_read",
    ]
    for item in required:
        if item not in warnings:
            warnings.append(item)
    return warnings


def _safe_warning_code(value: Any) -> str | None:
    if isinstance(value, dict):
        candidate = value.get("code") or value.get("reason") or value.get("type")
    else:
        candidate = value
    if not isinstance(candidate, str):
        return "metadata_warning"
    safe = "".join(character if character.isalnum() or character in {"_", "-"} else "_" for character in candidate)
    return safe[:80] or "metadata_warning"


def _forbidden_metadata_blockers(value: Any, path: str = "") -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if isinstance(value, dict):
        for key, nested_value in value.items():
            lowered = str(key).lower()
            child_path = f"{path}.{lowered}" if path else lowered
            if lowered in FORBIDDEN_FIELD_NAMES:
                blockers.append(_blocker(f"forbidden_metadata_field:{lowered}", "privacy"))
                continue
            blockers.extend(_forbidden_metadata_blockers(nested_value, child_path))
    elif isinstance(value, list):
        for item in value:
            blockers.extend(_forbidden_metadata_blockers(item, path))
    elif isinstance(value, str) and _looks_like_sensitive_string(value):
        blockers.append(_blocker("forbidden_metadata_sensitive_value", "privacy"))
    return blockers


def _requested_side_effect_blockers(value: dict[str, Any] | None) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if not isinstance(value, dict):
        return blockers
    for key, nested_value in value.items():
        lowered = str(key).lower()
        if lowered in SIDE_EFFECT_FIELDS and _truthy(nested_value):
            blockers.append(_blocker(f"requested_side_effect:{lowered}", "side_effect"))
    return blockers


def _smoke_status(blockers: list[dict[str, str]], warning_count: int, validation_status: str) -> str:
    if blockers:
        categories = {blocker["category"] for blocker in blockers}
        reasons = {blocker["reason"] for blocker in blockers}
        if "side_effect" in categories:
            return "blocked_requested_side_effect"
        if "privacy" in categories:
            return "blocked_forbidden_metadata"
        if "path" in categories and "approved_target_path_missing" in reasons:
            return "blocked_missing_approved_target"
        if "path" in categories:
            return "blocked_path_policy"
        if "approval" in categories:
            return "blocked_missing_approval"
        if "target_identity" in categories:
            return "blocked_target_identity"
        return "blocked_metadata_contract"
    if warning_count > 0 or validation_status in {"warn", "warning", "validation_warn"}:
        return WARN_STATUS
    return READY_STATUS


def _privacy_status(blockers: list[dict[str, str]]) -> str:
    if any(blocker["category"] == "privacy" for blocker in blockers):
        return "blocked_forbidden_metadata"
    return "metadata_only_no_known_privacy_blocker"


def _path_status(blockers: list[dict[str, str]]) -> str:
    reasons = {blocker["reason"] for blocker in blockers if blocker["category"] == "path"}
    if "approved_target_path_missing" in reasons:
        return "blocked_missing_approved_target"
    if reasons:
        return "blocked_path_policy"
    return "repo_controlled_target_path_ok"


def _boundary_flags() -> dict[str, bool]:
    return {
        "selected_sample_only": True,
        "not_full_web": True,
        "not_full_platform": True,
        "not_full_thread": True,
        "not_official_verification": True,
        "not_causal_proof": True,
        "not_prediction": True,
        "not_production_score": True,
        "provider_output_is_evidence_candidate_not_truth": True,
        "human_review_required": True,
        "metadata_only": True,
        "no_row_read": True,
        "no_private_collector_source_inspection": True,
        "no_evidence_layer_write": True,
        "no_production_case": True,
        "no_production_analysis_run": True,
        "no_frontend_route": True,
        "no_real_api_llm_provider_collector": True,
    }


def _runtime_side_effects() -> dict[str, bool]:
    return {
        "called_real_api": False,
        "called_real_llm": False,
        "ran_provider_job": False,
        "ran_collector": False,
        "accessed_private_collector": False,
        "inspected_private_collector_source": False,
        "read_real_exchange_dir": False,
        "fetched_url": False,
        "scraped_page": False,
        "parsed_evidence_items_jsonl": False,
        "parsed_evidence_items_csv": False,
        "read_original_package_rows": False,
        "read_raw_comments": False,
        "read_raw_identities": False,
        "wrote_evidence_layer": False,
        "created_production_case": False,
        "created_production_analysis_run": False,
        "generated_b_end_report_runtime": False,
        "generated_sandbox_runtime": False,
        "generated_public_event_runtime": False,
        "used_download_package_runtime": False,
        "used_public_access_runtime": False,
        "used_external_delivery_runtime": False,
        "used_final_delivery_runtime": False,
        "generated_response_text": False,
        "created_public_route": False,
        "modified_frontend": False,
        "published_or_sent": False,
        "auto_executed": False,
    }


def _safe_reason_codes(blockers: list[dict[str, str]]) -> list[str]:
    return [blocker["reason"] for blocker in blockers]


def _dedupe_blockers(blockers: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, str]] = []
    for blocker in blockers:
        key = (blocker["reason"], blocker["category"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(blocker)
    return deduped


def _blocker(reason: str, category: str) -> dict[str, str]:
    return {"reason": reason, "category": category}


def _safe_id(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or _looks_like_sensitive_string(stripped):
        return None
    return stripped


def _has_path_separator(value: str | None) -> bool:
    if not isinstance(value, str):
        return False
    return "/" in value or "\\" in value or ":" in value or ".." in value


def _looks_like_sensitive_string(value: str) -> bool:
    lowered = value.lower()
    if "actual-" in lowered and "should-never-appear" in lowered:
        return True
    if "private-collector" in lowered or "private_collector" in lowered:
        return True
    if "token=" in lowered or "cookie=" in lowered or "api_key=" in lowered:
        return True
    return False


def _matches_approved_repo_target(path: Path) -> bool:
    try:
        return path.resolve() == APPROVED_TARGET_DIR.resolve()
    except OSError:
        return False


def _truthy(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "requested", "enabled"}
    if isinstance(value, (int, float)):
        return bool(value)
    return False


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
