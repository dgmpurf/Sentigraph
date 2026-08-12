from __future__ import annotations

import hashlib
import io
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any, Final


PROVIDER_RESULT_CONTENT_IDENTITY_SCHEMA: Final = (
    "sentigraph_b05_provider_result_content_identity_v0_1"
)
METADATA_FILE_CONTENT_IDENTITY_SCHEMA: Final = (
    "sentigraph_b05_governed_metadata_file_content_identity_v0_1"
)
METADATA_IDENTITY_BUNDLE_SCHEMA: Final = (
    "sentigraph_b05_governed_metadata_identity_bundle_v0_1"
)
REVIEW_SUBJECT_CONTENT_IDENTITY_SCHEMA: Final = (
    "sentigraph_b05_review_subject_content_identity_v0_1"
)
REVIEW_SUBJECT_BINDING_SCHEMA: Final = "sentigraph_b05_review_subject_binding_v0_1"
REVIEW_SUBJECT_IDENTITY_SCHEMA: Final = "sentigraph_b05_review_subject_identity_v0_1"
IDENTITY_VERSION: Final = "0.1"

GOVERNED_B05_IDENTITY_METADATA_FILES: Final = (
    "README.md",
    "coverage_note.md",
    "manifest.json",
    "validation_report.json",
    "validation_report.md",
)

PROVIDER_RESULT_CONTENT_IDENTITY_FIELDS: Final = (
    "identity_schema",
    "identity_version",
    "result_file_name",
    "content_bytes",
    "content_sha256",
)
METADATA_FILE_CONTENT_IDENTITY_FIELDS: Final = (
    "name",
    "content_bytes",
    "content_sha256",
)
METADATA_IDENTITY_BUNDLE_FIELDS: Final = (
    "bundle_schema",
    "bundle_version",
    "profile",
    "entry_count",
    "entries",
)
REVIEW_SUBJECT_CONTENT_IDENTITY_FIELDS: Final = (
    "subject_schema",
    "subject_version",
    "provider_result_identity",
    "metadata_profile",
    "safe_metadata_bundle_sha256",
)
REVIEW_SUBJECT_BINDING_FIELDS: Final = (
    "binding_schema",
    "binding_version",
    "sample_handle",
    "result_file_name",
    "package_name",
    "review_subject_content_safe_hash",
)
B05_REVIEW_SUBJECT_IDENTITY_FIELDS: Final = (
    "identity_schema",
    "identity_version",
    "identity_status",
    "sample_handle",
    "result_file_name",
    "package_name",
    "provider_result_content_bytes",
    "provider_result_content_sha256",
    "metadata_profile",
    "metadata_entry_count",
    "safe_metadata_bundle_sha256",
    "review_subject_content_safe_hash",
    "review_subject_binding_safe_hash",
)

READY_IDENTITY_STATUS: Final = "ready"
BLOCKED_IDENTITY_STATUSES: Final = frozenset(
    {
        "blocked_provider_result_read_or_decode",
        "blocked_provider_result_parse",
        "blocked_metadata_member_missing_or_nonfile",
        "blocked_metadata_read_or_decode",
        "blocked_metadata_profile_or_order_mismatch",
        "blocked_package_name_provenance_mismatch",
        "blocked_sample_registry_binding_mismatch",
        "blocked_digest_construction_mismatch",
        "unavailable_identity_material",
    }
)

_LOWER_HEX_64 = re.compile(r"^[0-9a-f]{64}$")


def text_from_same_read_raw_bytes(raw_bytes: bytes) -> str:
    """Reconstruct text exactly like Path.read_text(encoding='utf-8')."""

    if not isinstance(raw_bytes, bytes):
        raise TypeError("raw_bytes_must_be_bytes")
    with io.TextIOWrapper(
        io.BytesIO(raw_bytes),
        encoding="utf-8",
        errors="strict",
        newline=None,
    ) as stream:
        return stream.read()


def canonical_safe_object_sha256(value: Mapping[str, Any]) -> str:
    """Hash one bounded JSON-safe identity object without exposing its preimage."""

    _validate_canonical_safe_value(value)
    encoded = json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_provider_result_content_identity(
    result_file_name: str,
    raw_bytes: bytes,
) -> dict[str, Any]:
    return {
        "identity_schema": PROVIDER_RESULT_CONTENT_IDENTITY_SCHEMA,
        "identity_version": IDENTITY_VERSION,
        "result_file_name": result_file_name,
        "content_bytes": len(raw_bytes),
        "content_sha256": hashlib.sha256(raw_bytes).hexdigest(),
    }


def build_metadata_file_content_identity(name: str, raw_bytes: bytes) -> dict[str, Any]:
    return {
        "name": name,
        "content_bytes": len(raw_bytes),
        "content_sha256": hashlib.sha256(raw_bytes).hexdigest(),
    }


def build_metadata_identity_bundle(
    profile: str,
    entries: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, Any], str]:
    safe_entries = [dict(entry) for entry in entries]
    names = tuple(entry.get("name") for entry in safe_entries)
    if names != GOVERNED_B05_IDENTITY_METADATA_FILES:
        raise ValueError("metadata_profile_or_order_mismatch")
    if any(tuple(entry) != METADATA_FILE_CONTENT_IDENTITY_FIELDS for entry in safe_entries):
        raise ValueError("metadata_identity_field_order_mismatch")
    if any(
        not isinstance(entry.get("content_bytes"), int)
        or isinstance(entry.get("content_bytes"), bool)
        or entry["content_bytes"] < 0
        or not is_lower_hex_sha256(entry.get("content_sha256"))
        for entry in safe_entries
    ):
        raise ValueError("metadata_identity_value_mismatch")
    bundle = {
        "bundle_schema": METADATA_IDENTITY_BUNDLE_SCHEMA,
        "bundle_version": IDENTITY_VERSION,
        "profile": profile,
        "entry_count": len(safe_entries),
        "entries": safe_entries,
    }
    return bundle, canonical_safe_object_sha256(bundle)


def build_review_subject_content_safe_hash(
    provider_result_identity: Mapping[str, Any],
    metadata_profile: str,
    safe_metadata_bundle_sha256: str,
) -> str:
    if tuple(provider_result_identity) != PROVIDER_RESULT_CONTENT_IDENTITY_FIELDS:
        raise ValueError("provider_result_identity_field_order_mismatch")
    if not is_lower_hex_sha256(provider_result_identity.get("content_sha256")):
        raise ValueError("provider_result_identity_digest_mismatch")
    if not is_lower_hex_sha256(safe_metadata_bundle_sha256):
        raise ValueError("metadata_bundle_digest_mismatch")
    subject = {
        "subject_schema": REVIEW_SUBJECT_CONTENT_IDENTITY_SCHEMA,
        "subject_version": IDENTITY_VERSION,
        "provider_result_identity": dict(provider_result_identity),
        "metadata_profile": metadata_profile,
        "safe_metadata_bundle_sha256": safe_metadata_bundle_sha256,
    }
    return canonical_safe_object_sha256(subject)


def build_ready_review_subject_identity(
    *,
    sample_handle: str,
    result_file_name: str,
    package_name: str,
    provider_result_identity: Mapping[str, Any],
    metadata_profile: str,
    metadata_entry_count: int,
    safe_metadata_bundle_sha256: str,
    review_subject_content_safe_hash: str,
) -> dict[str, Any]:
    if provider_result_identity.get("result_file_name") != result_file_name:
        raise ValueError("provider_result_name_binding_mismatch")
    if metadata_entry_count != len(GOVERNED_B05_IDENTITY_METADATA_FILES):
        raise ValueError("metadata_entry_count_mismatch")
    for digest in (
        provider_result_identity.get("content_sha256"),
        safe_metadata_bundle_sha256,
        review_subject_content_safe_hash,
    ):
        if not is_lower_hex_sha256(digest):
            raise ValueError("identity_digest_mismatch")
    binding = {
        "binding_schema": REVIEW_SUBJECT_BINDING_SCHEMA,
        "binding_version": IDENTITY_VERSION,
        "sample_handle": sample_handle,
        "result_file_name": result_file_name,
        "package_name": package_name,
        "review_subject_content_safe_hash": review_subject_content_safe_hash,
    }
    binding_hash = canonical_safe_object_sha256(binding)
    return {
        "identity_schema": REVIEW_SUBJECT_IDENTITY_SCHEMA,
        "identity_version": IDENTITY_VERSION,
        "identity_status": READY_IDENTITY_STATUS,
        "sample_handle": sample_handle,
        "result_file_name": result_file_name,
        "package_name": package_name,
        "provider_result_content_bytes": provider_result_identity.get("content_bytes"),
        "provider_result_content_sha256": provider_result_identity.get("content_sha256"),
        "metadata_profile": metadata_profile,
        "metadata_entry_count": metadata_entry_count,
        "safe_metadata_bundle_sha256": safe_metadata_bundle_sha256,
        "review_subject_content_safe_hash": review_subject_content_safe_hash,
        "review_subject_binding_safe_hash": binding_hash,
    }


def build_unavailable_review_subject_identity(
    identity_status: str,
    *,
    sample_handle: str | None = None,
    result_file_name: str | None = None,
    package_name: str | None = None,
) -> dict[str, Any]:
    safe_status = identity_status if identity_status in BLOCKED_IDENTITY_STATUSES else "unavailable_identity_material"
    return {
        "identity_schema": REVIEW_SUBJECT_IDENTITY_SCHEMA,
        "identity_version": IDENTITY_VERSION,
        "identity_status": safe_status,
        "sample_handle": sample_handle,
        "result_file_name": result_file_name,
        "package_name": package_name,
        "provider_result_content_bytes": None,
        "provider_result_content_sha256": None,
        "metadata_profile": None,
        "metadata_entry_count": 0,
        "safe_metadata_bundle_sha256": None,
        "review_subject_content_safe_hash": None,
        "review_subject_binding_safe_hash": None,
    }


def is_lower_hex_sha256(value: object) -> bool:
    return isinstance(value, str) and _LOWER_HEX_64.fullmatch(value) is not None


def _validate_canonical_safe_value(value: object) -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, list):
        for item in value:
            _validate_canonical_safe_value(item)
        return
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if not isinstance(key, str):
                raise ValueError("canonical_identity_key_must_be_string")
            _validate_canonical_safe_value(nested)
        return
    raise ValueError("canonical_identity_value_not_json_safe")
