from __future__ import annotations

import math
import re
from typing import Any, Final


SCAN_SCHEMA: Final = "sentigraph_protected_value_boundary_scan_v0_1"
SCAN_VERSION: Final = "0.1"
SAFE_PAYLOAD_PROFILE: Final = "safe_payload_v0_1"
SAFE_CAPTURE_RECEIPT_PROFILE: Final = "safe_capture_receipt_v1_0"

_SUPPORTED_PROFILES: Final = frozenset(
    {SAFE_PAYLOAD_PROFILE, SAFE_CAPTURE_RECEIPT_PROFILE}
)
_SAFE_REDACTION_MARKER: Final = "[redacted selected source content]"
_MAX_SCAN_DEPTH: Final = 64
_SAFE_SHA256_RE: Final = re.compile(r"^[a-f0-9]{64}$")

_RECEIPT_NEGATIVE_PROOF_KEYS: Final = frozenset(
    {
        "raw_row_retained",
        "raw_author_identity_retained",
        "absolute_path_recorded",
        "production_object_created",
        "database_accessed",
        "network_called",
        "gate_activated",
        "persistence_mutation_performed",
        "directory_enumeration_performed",
        "alternate_source_used",
    }
)

_FORBIDDEN_KEYS: Final = frozenset(
    {
        "raw_row",
        "raw_rows",
        "raw_row_text",
        "raw_source_text",
        "raw_content",
        "raw_comment",
        "raw_comments",
        "raw_author_id",
        "raw_author_ids",
        "raw_author_name",
        "raw_author_names",
        "author_id",
        "author_name",
        "account_id",
        "account_name",
        "profile_url",
        "profile_data",
        "private_message",
        "private_messages",
        "source_url",
        "url",
        "absolute_path",
        "physical_path",
        "filesystem_path",
        "file_path",
        "source_path",
        "package_path",
        "cookie",
        "cookies",
        "session",
        "sessions",
        "token",
        "tokens",
        "password",
        "passwords",
        "api_key",
        "api_keys",
        "credential",
        "credentials",
        "environment_value",
        "env_value",
        "secret",
        "secrets",
        "unrelated_rows",
        "production_package_rows",
        "evidence_items_jsonl_contents",
        "evidence_items_csv_contents",
        "source_manifest_row_contents",
        "collection_log_row_contents",
        "response_text",
        "generated_public_message",
        "target_user_list",
        "persuasion_score",
        "psychological_profile",
        "personality_diagnosis",
        "official_verified",
        "truth_score",
        "prediction_probability",
        "real_person_pii",
    }
)

_URL_RE: Final = re.compile(r"(?:\bhttps?://|\bwww\.)", re.IGNORECASE)
_WINDOWS_ABSOLUTE_PATH_RE: Final = re.compile(
    r"(?:^|[\s=\"'])[A-Za-z]:[\\/]"
)
_UNC_ABSOLUTE_PATH_RE: Final = re.compile(r"^(?:\\\\|//)[^\\/\s]+[\\/]")
_POSIX_ABSOLUTE_PATH_RE: Final = re.compile(r"(?:^|[\s=\"'])/(?!/)[^\s]")
_TRAVERSAL_RE: Final = re.compile(r"(?:^|[\\/])\.\.(?:[\\/]|$)")
_EMAIL_RE: Final = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)
_PHONE_RE: Final = re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)")
_SECRET_RE: Final = re.compile(
    r"(?:"
    r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}"
    r"|\bsk-[A-Za-z0-9_-]{8,}"
    r"|\bxox[baprs]-[A-Za-z0-9-]+"
    r"|\bAKIA[0-9A-Z]{16}\b"
    r"|\bAIza[0-9A-Za-z_-]{20,}\b"
    r"|\bghp_[0-9A-Za-z]{20,}\b"
    r"|\bgithub_pat_[0-9A-Za-z_]{20,}\b"
    r"|\b(?:sk|pk)_live_[0-9A-Za-z]{8,}\b"
    r"|-----BEGIN(?: [A-Z]+)? PRIVATE KEY-----"
    r"|\b(?:api[_ -]?key|access[_ -]?token|refresh[_ -]?token|token|cookie|password|secret)"
    r"\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{4,}"
    r"|(?:^|[\\/])\.env(?:$|[\\/\s])"
    r")",
    re.IGNORECASE,
)
_RAW_CONTENT_RE: Final = re.compile(
    r"\b(?:raw[_ -]?(?:row|rows|comment|comments|author(?:[_ -]?(?:id|name))?|identity)"
    r"|private[_ -]?message|profile[_ -]?url)\b\s*[:=]",
    re.IGNORECASE,
)


def scan_protected_value_boundary(
    value: Any,
    *,
    profile: str,
) -> dict[str, Any]:
    """Scan a payload or receipt without IO or unsafe finding disclosure."""

    if not isinstance(profile, str) or profile not in _SUPPORTED_PROFILES:
        return _build_result(
            profile="invalid",
            finding_location_class="unknown",
            findings=["invalid_scan_profile"],
        )

    location = "payload" if profile == SAFE_PAYLOAD_PROFILE else "receipt"
    if not isinstance(value, dict):
        return _build_result(
            profile=profile,
            finding_location_class=location,
            findings=["invalid_scan_input"],
        )

    findings: list[str] = []
    _scan_value(
        value,
        profile=profile,
        depth=0,
        active_container_ids=set(),
        findings=findings,
    )
    return _build_result(
        profile=profile,
        finding_location_class=location,
        findings=findings,
    )


def _scan_value(
    value: Any,
    *,
    profile: str,
    depth: int,
    active_container_ids: set[int],
    findings: list[str],
) -> None:
    if depth > _MAX_SCAN_DEPTH:
        findings.append("invalid_scan_input")
        return

    if isinstance(value, dict):
        container_id = id(value)
        if container_id in active_container_ids:
            findings.append("invalid_scan_input")
            return
        active_container_ids.add(container_id)
        try:
            if any(not isinstance(key, str) for key in value):
                findings.append("invalid_scan_input")
                return
            for key in sorted(value):
                nested = value[key]
                normalized_key = key.casefold()
                _scan_key(
                    normalized_key,
                    nested,
                    profile=profile,
                    depth=depth,
                    findings=findings,
                )
                _scan_value(
                    nested,
                    profile=profile,
                    depth=depth + 1,
                    active_container_ids=active_container_ids,
                    findings=findings,
                )
        finally:
            active_container_ids.remove(container_id)
        return

    if isinstance(value, list):
        container_id = id(value)
        if container_id in active_container_ids:
            findings.append("invalid_scan_input")
            return
        active_container_ids.add(container_id)
        try:
            for item in value:
                _scan_value(
                    item,
                    profile=profile,
                    depth=depth + 1,
                    active_container_ids=active_container_ids,
                    findings=findings,
                )
        finally:
            active_container_ids.remove(container_id)
        return

    if isinstance(value, str):
        _scan_string(value, findings)
        return

    if value is None or isinstance(value, (bool, int)):
        return
    if isinstance(value, float) and math.isfinite(value):
        return
    findings.append("invalid_scan_input")


def _scan_key(
    normalized_key: str,
    nested: Any,
    *,
    profile: str,
    depth: int,
    findings: list[str],
) -> None:
    if normalized_key in _RECEIPT_NEGATIVE_PROOF_KEYS:
        if profile == SAFE_CAPTURE_RECEIPT_PROFILE:
            if depth != 0 or nested is not False:
                findings.append("negative_proof_state_violation")
        else:
            findings.append("forbidden_key_present")
        return
    if normalized_key in _FORBIDDEN_KEYS:
        findings.append("forbidden_key_present")


def _scan_string(value: str, findings: list[str]) -> None:
    if value == _SAFE_REDACTION_MARKER or _SAFE_SHA256_RE.fullmatch(value):
        return
    if _URL_RE.search(value):
        findings.append("unsafe_URL_pattern")
    if (
        _WINDOWS_ABSOLUTE_PATH_RE.search(value)
        or _UNC_ABSOLUTE_PATH_RE.search(value)
        or _POSIX_ABSOLUTE_PATH_RE.search(value)
        or _TRAVERSAL_RE.search(value)
    ):
        findings.append("unsafe_absolute_path_pattern")
    if _EMAIL_RE.search(value):
        findings.append("unsafe_email_pattern")
    if _PHONE_RE.search(value):
        findings.append("unsafe_phone_pattern")
    if _SECRET_RE.search(value):
        findings.append("unsafe_secret_pattern")
    if _RAW_CONTENT_RE.search(value):
        findings.append("unsafe_raw_content_pattern")


def _build_result(
    *,
    profile: str,
    finding_location_class: str,
    findings: list[str],
) -> dict[str, Any]:
    categories = list(dict.fromkeys(findings))
    return {
        "scan_schema": SCAN_SCHEMA,
        "scan_version": SCAN_VERSION,
        "profile": profile,
        "passed": not findings,
        "finding_count": len(findings),
        "finding_categories": categories,
        "first_finding_code": findings[0] if findings else None,
        "finding_location_class": finding_location_class,
        "protected_value_exposed": False,
        "raw_key_echoed": False,
        "raw_value_echoed": False,
    }
