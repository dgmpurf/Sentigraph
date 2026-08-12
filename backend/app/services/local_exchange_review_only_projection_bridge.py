from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any, Final

PROJECTION_SCHEMA: Final = "sentigraph_local_exchange_review_only_candidate_projection_v0_1"
PROJECTION_VERSION: Final = "0.1"
VERSIONED_PROJECTION_SCHEMA: Final = "sentigraph_local_exchange_review_only_candidate_projection_v0_2"
VERSIONED_PROJECTION_VERSION: Final = "0.2"
PROJECTION_MODE: Final = "internal_governed_read_only_review_projection"
SOURCE_CHAIN_BOUNDARY: Final = "local_exchange_review_only_staging_candidate_boundary"
UPSTREAM_SCHEMA: Final = "internal_operator_review_only_staging_local_exchange_response_v0_1"

PROJECTION_FIELDS: Final = (
    "projection_schema",
    "projection_version",
    "projection_mode",
    "projection_status",
    "projection_error_code",
    "source_chain_boundary",
    "result_file_name",
    "upstream_schema",
    "upstream_status",
    "reader_status",
    "adapter_status",
    "provider_result_status",
    "package_resolution_status",
    "candidate_count",
    "staging_candidate_id",
    "gate_result_id",
    "analysis_request_id",
    "provider_result_id",
    "package_name",
    "case_id_hint",
    "case_title_hint",
    "validation_summary",
    "coverage_summary",
    "review_status",
    "promotion_status",
    "staging_status",
    "gate_summary",
    "warnings",
    "blockers",
    "allowed_actions",
    "blocked_actions",
    "metadata_only",
    "review_only",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "candidate_persistence",
    "persistent_staging_write",
    "review_decision_write",
    "evidence_layer_write",
    "production_evidenceitem_created",
    "production_case_created",
    "analysis_run_created",
    "analysis_result_created",
    "frontend_action_enabled",
    "public_output_enabled",
    "export_delivery_enabled",
    "path_exposed",
    "raw_metadata_exposed",
    "trust_approved",
    "production_ready",
    "promotion_completed",
    "mutable_authority_granted",
)
VERSIONED_PROJECTION_FIELDS: Final = (*PROJECTION_FIELDS, "review_subject_identity")
VERSIONED_UPSTREAM_SCHEMA: Final = "internal_operator_review_only_staging_local_exchange_response_v0_2"
REVIEW_SUBJECT_IDENTITY_FIELDS: Final = (
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

_REVIEW_SUBJECT_IDENTITY_SCHEMA: Final = "sentigraph_b05_review_subject_identity_v0_1"
_REVIEW_SUBJECT_IDENTITY_VERSION: Final = "0.1"
_GOVERNED_B05_METADATA_PROFILE: Final = "governed_b05_five_file"
_GOVERNED_B05_METADATA_ENTRY_COUNT: Final = 5
_BLOCKED_IDENTITY_STATUSES: Final = frozenset(
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

_RESULT_BASENAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\.json")
_SAFE_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_LOWER_HEX_64 = re.compile(r"[0-9a-f]{64}")
_READY_STATUS = "ready_for_human_review"
_MANUAL_STATUS = "manual_review_required"
_READY_PACKAGE_STATUSES = frozenset({"accepted_metadata_only", "package_ready"})
_SAFE_PATH_REFERENCES = frozenset({None, "review_only_metadata_summary"})

_TOP_LEVEL_FIELDS = frozenset(
    {
        "schema",
        "route_scope",
        "access_scope",
        "metadata_only",
        "review_only",
        "status",
        "error_code",
        "result_file_name",
        "reader_status",
        "adapter_status",
        "provider_result_status",
        "package_resolution_status",
        "candidate_count",
        "staging_candidate",
        "gate_summary",
        "production_import_allowed",
        "evidence_layer_write_allowed",
        "production_case_creation_allowed",
        "analysis_run_allowed",
        "public_output_allowed",
        "path_exposed",
        "raw_metadata_exposed",
        "blockers",
        "warnings",
        "safety_flags",
    }
)
_CANDIDATE_FIELDS = frozenset(
    {
        "staging_candidate_id",
        "gate_result_id",
        "analysis_request_id",
        "provider_result_id",
        "package_name",
        "case_id_hint",
        "case_title_hint",
        "validation_status",
        "evidence_count",
        "source_count",
        "comment_count",
        "root_candidate_count",
        "warning_count",
        "error_count",
        "review_status",
        "promotion_status",
        "staging_status",
        "blockers",
        "warnings",
        "allowed_actions",
        "blocked_actions",
        "safety_flags",
        "audit_refs",
        "gate_result",
        "metadata_only",
        "path_exposed",
        "path_reference",
    }
)
_GATE_FIELDS = frozenset(
    {
        "gate_result_id",
        "package_resolution_status",
        "provider_result_status",
        "privacy_status",
        "path_status",
        "metadata_contract_status",
        "evidence_row_boundary_status",
        "staging_status",
        "blockers",
        "warnings",
        "allowed_actions",
        "blocked_actions",
        "safety_flags",
    }
)
_UNSAFE_UNKNOWN_KEY_FRAGMENTS = (
    "persisted_",
    "reservation_",
    "identity_digest",
    "raw_payload",
    "raw_provider",
    "raw_package",
    "raw_author",
    "author_id",
    "author_name",
    "profile_url",
    "secret",
    "password",
    "token",
    "results_dir",
    "export_root",
    "absolute_path",
    "evidence_items",
    "source_manifest",
    "collection_log",
    "exception",
    "traceback",
    "database_",
    "table_",
    "column_",
    "target_",
)


def build_local_exchange_review_only_projection(
    result_file_name: str,
    upstream_response: Mapping[str, Any] | object,
) -> dict[str, Any]:
    """Build one bounded, side-effect-free review projection from the B01 response."""

    if not _is_result_basename(result_file_name):
        return _terminal_projection("projection_unavailable", "invalid_result_file_name")
    if not isinstance(upstream_response, Mapping):
        return _terminal_projection(
            "projection_unavailable",
            "invalid_upstream_response",
            result_file_name=result_file_name,
        )
    if _has_unsafe_unknown_keys(upstream_response, _TOP_LEVEL_FIELDS):
        return _terminal_projection(
            "projection_unavailable",
            "unsafe_unknown_field",
            result_file_name=result_file_name,
        )

    upstream_schema = upstream_response.get("schema")
    upstream_status = _bounded_token(upstream_response.get("status"))
    if upstream_schema != UPSTREAM_SCHEMA:
        return _terminal_projection(
            "projection_unavailable",
            "unexpected_upstream_schema",
            result_file_name=result_file_name,
            upstream_status=upstream_status,
        )

    base = _base_projection(
        result_file_name=result_file_name,
        upstream_schema=UPSTREAM_SCHEMA,
        upstream_status=upstream_status,
    )
    if (
        upstream_response.get("result_file_name") != result_file_name
        or upstream_response.get("metadata_only") is not True
        or upstream_response.get("review_only") is not True
        or upstream_response.get("path_exposed") is not False
        or upstream_response.get("raw_metadata_exposed") is not False
    ):
        return _with_terminal_state(base, "projection_unavailable", "invalid_upstream_boundary")

    if upstream_status == _MANUAL_STATUS:
        return _with_terminal_state(base, _MANUAL_STATUS, "upstream_manual_review_required")
    if upstream_status != _READY_STATUS:
        return _with_terminal_state(base, "blocked_upstream", "upstream_not_ready")

    candidate_count = _nonnegative_int(upstream_response.get("candidate_count"))
    if candidate_count != 1:
        return _with_terminal_state(base, "projection_unavailable", "candidate_count_not_one")

    candidate = upstream_response.get("staging_candidate")
    top_gate = upstream_response.get("gate_summary")
    if not isinstance(candidate, Mapping) or not isinstance(top_gate, Mapping):
        return _with_terminal_state(base, "projection_unavailable", "malformed_candidate_or_gate")
    if _has_unsafe_unknown_keys(candidate, _CANDIDATE_FIELDS) or _has_unsafe_unknown_keys(
        top_gate, _GATE_FIELDS
    ):
        return _with_terminal_state(base, "projection_unavailable", "unsafe_unknown_field")

    candidate_gate = candidate.get("gate_result")
    if not isinstance(candidate_gate, Mapping):
        return _with_terminal_state(base, "projection_unavailable", "malformed_candidate_or_gate")
    if _has_unsafe_unknown_keys(candidate_gate, _GATE_FIELDS):
        return _with_terminal_state(base, "projection_unavailable", "unsafe_unknown_field")

    identifiers = _candidate_identifiers(candidate)
    counts = _candidate_counts(candidate)
    gate_summary = _bounded_gate_summary(candidate_gate)
    top_gate_summary = _bounded_gate_summary(top_gate)
    warnings = _bounded_text_list(candidate.get("warnings"))
    blockers = _bounded_text_list(candidate.get("blockers"))
    allowed_actions = _bounded_text_list(candidate.get("allowed_actions"))
    blocked_actions = _bounded_text_list(candidate.get("blocked_actions"))
    if (
        identifiers is None
        or counts is None
        or gate_summary is None
        or top_gate_summary is None
        or gate_summary != top_gate_summary
        or warnings is None
        or blockers is None
        or allowed_actions is None
        or blocked_actions is None
    ):
        return _with_terminal_state(base, "projection_unavailable", "malformed_candidate_or_gate")

    reader_status = _bounded_token(upstream_response.get("reader_status"))
    adapter_status = _bounded_token(upstream_response.get("adapter_status"))
    provider_status = _bounded_token(upstream_response.get("provider_result_status"))
    package_status = _bounded_token(upstream_response.get("package_resolution_status"))
    review_status = _bounded_token(candidate.get("review_status"))
    promotion_status = _bounded_token(candidate.get("promotion_status"))
    staging_status = _bounded_token(candidate.get("staging_status"))
    if (
        reader_status != "metadata_ready"
        or adapter_status != "adapted"
        or provider_status != "accepted_metadata_only"
        or package_status not in _READY_PACKAGE_STATUSES
        or review_status != _READY_STATUS
        or promotion_status != "promotion_required"
        or staging_status != _READY_STATUS
        or gate_summary["staging_status"] != _READY_STATUS
        or candidate.get("metadata_only") is not True
        or candidate.get("path_exposed") is not False
        or candidate.get("path_reference") not in _SAFE_PATH_REFERENCES
        or blockers
    ):
        return _with_terminal_state(base, "projection_unavailable", "candidate_not_projection_ready")

    base.update(
        projection_status=_READY_STATUS,
        projection_error_code=None,
        reader_status=reader_status,
        adapter_status=adapter_status,
        provider_result_status=provider_status,
        package_resolution_status=package_status,
        candidate_count=1,
        staging_candidate_id=identifiers["staging_candidate_id"],
        gate_result_id=identifiers["gate_result_id"],
        analysis_request_id=identifiers["analysis_request_id"],
        provider_result_id=identifiers["provider_result_id"],
        package_name=identifiers["package_name"],
        case_id_hint=identifiers["case_id_hint"],
        case_title_hint=identifiers["case_title_hint"],
        validation_summary={
            "validation_status": identifiers["validation_status"],
            "warning_count": counts["warning_count"],
            "error_count": counts["error_count"],
        },
        coverage_summary={
            "evidence_count": counts["evidence_count"],
            "source_count": counts["source_count"],
            "comment_count": counts["comment_count"],
            "root_candidate_count": counts["root_candidate_count"],
            "coverage_basis": "selected_package_metadata_counts_only",
            "full_web_coverage_claimed": False,
            "full_platform_coverage_claimed": False,
        },
        review_status=review_status,
        promotion_status=promotion_status,
        staging_status=staging_status,
        gate_summary=gate_summary,
        warnings=warnings,
        blockers=blockers,
        allowed_actions=allowed_actions,
        blocked_actions=blocked_actions,
    )
    return base


def build_identity_ready_local_exchange_review_only_projection(
    sample_handle: str,
    result_file_name: str,
    upstream_response: Mapping[str, Any] | object,
    review_subject_identity: Mapping[str, Any] | object,
) -> dict[str, Any]:
    """Append one prebuilt bounded identity to the parallel 53-field projection."""

    if not isinstance(upstream_response, Mapping):
        return build_disabled_identity_ready_local_exchange_review_only_projection(
            "invalid_upstream_response",
            review_subject_identity=review_subject_identity,
            sample_handle=sample_handle,
            result_file_name=result_file_name,
        )
    legacy_upstream = dict(upstream_response)
    if legacy_upstream.get("schema") == VERSIONED_UPSTREAM_SCHEMA:
        legacy_upstream["schema"] = UPSTREAM_SCHEMA
    legacy_projection = build_local_exchange_review_only_projection(
        result_file_name,
        legacy_upstream,
    )
    legacy_projection["projection_schema"] = VERSIONED_PROJECTION_SCHEMA
    legacy_projection["projection_version"] = VERSIONED_PROJECTION_VERSION

    identity_package_name = legacy_projection.get("package_name")
    if (
        isinstance(review_subject_identity, Mapping)
        and review_subject_identity.get("identity_status") == "ready"
        and not (
            isinstance(identity_package_name, str)
            and _SAFE_TOKEN.fullmatch(identity_package_name) is not None
        )
    ):
        staging_candidate = upstream_response.get("staging_candidate")
        staging_package_name = (
            staging_candidate.get("package_name")
            if isinstance(staging_candidate, Mapping)
            else None
        )
        identity_package_name = (
            staging_package_name
            if isinstance(staging_package_name, str)
            and _SAFE_TOKEN.fullmatch(staging_package_name) is not None
            else None
        )

    identity = _validated_review_subject_identity(
        review_subject_identity,
        sample_handle=sample_handle,
        result_file_name=result_file_name,
        package_name=identity_package_name,
    )
    if identity is None:
        return legacy_projection
    identity_status = identity["identity_status"]
    if identity_status != "ready":
        return _with_versioned_identity_failure(
            legacy_projection,
            identity_status,
            review_subject_identity=identity,
        )
    legacy_projection["review_subject_identity"] = identity
    return legacy_projection


def build_disabled_identity_ready_local_exchange_review_only_projection(
    error_code: str,
    *,
    review_subject_identity: Mapping[str, Any] | object,
    sample_handle: str | None = None,
    result_file_name: str | None = None,
) -> dict[str, Any]:
    projection = build_disabled_local_exchange_review_only_projection(
        error_code,
        result_file_name=result_file_name,
    )
    projection["projection_schema"] = VERSIONED_PROJECTION_SCHEMA
    projection["projection_version"] = VERSIONED_PROJECTION_VERSION
    identity = _validated_review_subject_identity(
        review_subject_identity,
        sample_handle=sample_handle,
        result_file_name=result_file_name,
        package_name=None,
    )
    if identity is not None and identity["identity_status"] != "ready":
        projection["review_subject_identity"] = identity
    return projection


def _with_versioned_identity_failure(
    projection: dict[str, Any],
    identity_status: str,
    *,
    review_subject_identity: Mapping[str, Any],
) -> dict[str, Any]:
    safe_status = identity_status if isinstance(identity_status, str) else "unavailable_identity_material"
    projection["projection_status"] = "projection_unavailable"
    projection["projection_error_code"] = safe_status
    projection["blockers"] = [safe_status]
    projection["review_subject_identity"] = dict(review_subject_identity)
    return projection


def _validated_review_subject_identity(
    value: Mapping[str, Any] | object,
    *,
    sample_handle: str | None,
    result_file_name: str | None,
    package_name: object,
) -> dict[str, Any] | None:
    if not isinstance(value, Mapping) or tuple(value) != REVIEW_SUBJECT_IDENTITY_FIELDS:
        return None
    identity = dict(value)
    if (
        identity.get("identity_schema") != _REVIEW_SUBJECT_IDENTITY_SCHEMA
        or identity.get("identity_version") != _REVIEW_SUBJECT_IDENTITY_VERSION
        or identity.get("sample_handle") != sample_handle
        or identity.get("result_file_name") != result_file_name
    ):
        return None
    identity_status = identity.get("identity_status")
    identity_package_name = identity.get("package_name")
    if identity_status == "ready":
        if (
            not isinstance(sample_handle, str)
            or not sample_handle
            or not isinstance(result_file_name, str)
            or not _is_result_basename(result_file_name)
            or not isinstance(identity_package_name, str)
            or identity_package_name != package_name
            or not _SAFE_TOKEN.fullmatch(identity_package_name)
            or not isinstance(identity.get("provider_result_content_bytes"), int)
            or isinstance(identity.get("provider_result_content_bytes"), bool)
            or identity["provider_result_content_bytes"] < 0
            or identity.get("metadata_profile") != _GOVERNED_B05_METADATA_PROFILE
            or identity.get("metadata_entry_count") != _GOVERNED_B05_METADATA_ENTRY_COUNT
        ):
            return None
        for field in (
            "provider_result_content_sha256",
            "safe_metadata_bundle_sha256",
            "review_subject_content_safe_hash",
            "review_subject_binding_safe_hash",
        ):
            if not isinstance(identity.get(field), str) or _LOWER_HEX_64.fullmatch(identity[field]) is None:
                return None
        return identity
    if identity_status not in _BLOCKED_IDENTITY_STATUSES:
        return None
    if identity_package_name is not None and (
        not isinstance(identity_package_name, str)
        or _SAFE_TOKEN.fullmatch(identity_package_name) is None
    ):
        return None
    if package_name is not None and identity_package_name != package_name:
        return None
    if (
        identity.get("provider_result_content_bytes") is not None
        or identity.get("provider_result_content_sha256") is not None
        or identity.get("metadata_profile") is not None
        or identity.get("metadata_entry_count") != 0
        or identity.get("safe_metadata_bundle_sha256") is not None
        or identity.get("review_subject_content_safe_hash") is not None
        or identity.get("review_subject_binding_safe_hash") is not None
    ):
        return None
    return identity


def build_disabled_local_exchange_review_only_projection(
    error_code: str,
    result_file_name: str | None = None,
) -> dict[str, Any]:
    safe_name = result_file_name if _is_result_basename(result_file_name) else None
    safe_error = _bounded_token(error_code) or "route_disabled"
    return _terminal_projection(
        "projection_unavailable",
        safe_error,
        result_file_name=safe_name,
    )


def _base_projection(
    *,
    result_file_name: str | None,
    upstream_schema: str | None = None,
    upstream_status: str | None = None,
) -> dict[str, Any]:
    return {
        "projection_schema": PROJECTION_SCHEMA,
        "projection_version": PROJECTION_VERSION,
        "projection_mode": PROJECTION_MODE,
        "projection_status": "projection_unavailable",
        "projection_error_code": None,
        "source_chain_boundary": SOURCE_CHAIN_BOUNDARY,
        "result_file_name": result_file_name,
        "upstream_schema": upstream_schema,
        "upstream_status": upstream_status,
        "reader_status": None,
        "adapter_status": None,
        "provider_result_status": None,
        "package_resolution_status": None,
        "candidate_count": 0,
        "staging_candidate_id": None,
        "gate_result_id": None,
        "analysis_request_id": None,
        "provider_result_id": None,
        "package_name": None,
        "case_id_hint": None,
        "case_title_hint": None,
        "validation_summary": None,
        "coverage_summary": None,
        "review_status": None,
        "promotion_status": None,
        "staging_status": None,
        "gate_summary": None,
        "warnings": [],
        "blockers": [],
        "allowed_actions": [],
        "blocked_actions": [],
        "metadata_only": True,
        "review_only": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "candidate_persistence": "in_memory_only",
        "persistent_staging_write": False,
        "review_decision_write": False,
        "evidence_layer_write": False,
        "production_evidenceitem_created": False,
        "production_case_created": False,
        "analysis_run_created": False,
        "analysis_result_created": False,
        "frontend_action_enabled": False,
        "public_output_enabled": False,
        "export_delivery_enabled": False,
        "path_exposed": False,
        "raw_metadata_exposed": False,
        "trust_approved": False,
        "production_ready": False,
        "promotion_completed": False,
        "mutable_authority_granted": False,
    }


def _terminal_projection(
    status: str,
    error_code: str,
    *,
    result_file_name: str | None = None,
    upstream_status: str | None = None,
) -> dict[str, Any]:
    projection = _base_projection(
        result_file_name=result_file_name,
        upstream_status=upstream_status,
    )
    return _with_terminal_state(projection, status, error_code)


def _with_terminal_state(
    projection: dict[str, Any],
    status: str,
    error_code: str,
) -> dict[str, Any]:
    projection["projection_status"] = status
    projection["projection_error_code"] = error_code
    projection["blockers"] = [error_code]
    return projection


def _candidate_identifiers(candidate: Mapping[str, Any]) -> dict[str, str | None] | None:
    required_fields = (
        "staging_candidate_id",
        "gate_result_id",
        "analysis_request_id",
        "provider_result_id",
        "package_name",
        "validation_status",
    )
    normalized: dict[str, str | None] = {}
    for field in required_fields:
        value = _bounded_token(candidate.get(field))
        if value is None:
            return None
        normalized[field] = value
    for field in ("case_id_hint", "case_title_hint"):
        value = candidate.get(field)
        if value is not None and not _is_bounded_text(value, limit=200):
            return None
        normalized[field] = value
    return normalized


def _candidate_counts(candidate: Mapping[str, Any]) -> dict[str, int] | None:
    counts: dict[str, int] = {}
    for field in (
        "evidence_count",
        "source_count",
        "comment_count",
        "root_candidate_count",
        "warning_count",
        "error_count",
    ):
        value = _nonnegative_int(candidate.get(field))
        if value is None:
            return None
        counts[field] = value
    return counts


def _bounded_gate_summary(gate: Mapping[str, Any]) -> dict[str, str] | None:
    normalized: dict[str, str] = {}
    for field in (
        "package_resolution_status",
        "provider_result_status",
        "privacy_status",
        "path_status",
        "metadata_contract_status",
        "evidence_row_boundary_status",
        "staging_status",
    ):
        value = _bounded_token(gate.get(field))
        if value is None:
            return None
        normalized[field] = value
    return normalized


def _bounded_text_list(value: object) -> list[str] | None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) > 16:
        return None
    normalized: list[str] = []
    for item in value:
        if not _is_bounded_text(item, limit=160):
            return None
        normalized.append(item)
    return normalized


def _has_unsafe_unknown_keys(mapping: Mapping[str, Any], allowed: frozenset[str]) -> bool:
    for key in mapping:
        if not isinstance(key, str):
            return True
        lowered = key.lower()
        if key not in allowed and any(fragment in lowered for fragment in _UNSAFE_UNKNOWN_KEY_FRAGMENTS):
            return True
    return False


def _is_result_basename(value: object) -> bool:
    return (
        isinstance(value, str)
        and 0 < len(value) <= 160
        and _RESULT_BASENAME.fullmatch(value) is not None
        and "/" not in value
        and "\\" not in value
    )


def _bounded_token(value: object) -> str | None:
    if not isinstance(value, str) or not 0 < len(value) <= 160:
        return None
    return value if _SAFE_TOKEN.fullmatch(value) is not None else None


def _is_bounded_text(value: object, *, limit: int) -> bool:
    if not isinstance(value, str) or not 0 < len(value) <= limit or not value.isprintable():
        return False
    lowered = value.lower()
    return (
        "/" not in value
        and "\\" not in value
        and "://" not in value
        and "secret" not in lowered
        and "password" not in lowered
        and "token=" not in lowered
    )


def _nonnegative_int(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None
