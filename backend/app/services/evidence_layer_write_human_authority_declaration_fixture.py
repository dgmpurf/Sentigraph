from __future__ import annotations

import hashlib
import re
from typing import Any


APPROVAL_PHRASE = (
    "APPROVE_9A_11_CONTROLLED_NON_AUTHORIZING_EVIDENCE_LAYER_WRITE_PRODUCTION_"
    "EVIDENCEITEM_HUMAN_AUTHORITY_DECLARATION_FIXTURE_SMOKE"
)
DECLARATION_SCHEMA = "sentigraph_actual_evidence_layer_write_human_authority_declaration_v0_1"
SUMMARY_SCHEMA = "sentigraph_actual_evidence_layer_write_human_authority_declaration_summary_v0_1"
DECLARATION_SCOPE = "local_non_authorizing_fixture"
DECLARATION_MODE = "backend_only_local_non_authorizing_human_authority_declaration_fixture"
READY_STATUS = "declaration_fixture_ready_for_human_review_non_authorizing"
BLOCKED_STATUS = "declaration_fixture_blocked"
PRIVACY_STATUS = "privacy_issue_stop"
PAUSED_STATUS = "paused"

SAFE_INPUT_FIELDS = [
    "human_authority_identity_label",
    "authority_basis",
    "manual_review_responsibility_label",
    "warning_count_acknowledgment",
    "human_review_required_acknowledgment",
    "no_automatic_trust_upgrade_acknowledgment",
    "blocker_review_status",
    "risk_review_status",
    "lineage_review_status",
    "raw_private_secret_absence_acknowledgment",
    "rollback_pause_responsibility",
]

FALSE_FLAGS = [
    "actual_write_authorized",
    "production_evidenceitem_creation_authorized",
    "ready_for_actual_write",
    "human_authority_validated",
    "manual_review_responsibility_accepted",
    "final_write_authorization_performed",
    "actual_evidence_layer_write_approved",
    "actual_evidence_layer_write_performed",
    "persisted_evidence_layer_record_created",
    "production_evidenceitem_created",
    "write_authorization_object_created_that_permits_write",
    "runtime_human_authority_validation_performed",
    "runtime_manual_review_responsibility_acceptance_performed",
    "evidenceitem_write_runtime_called",
    "review_queue_runtime_used",
    "production_case_created",
    "production_analysis_run_created",
    "actual_analysis_execution_started",
    "production_analysis_result_authorized",
    "production_analysis_result_created",
    "source11_runtime_called",
    "finalsummaryreport_runtime_called",
    "public_delivery_created",
]

FORBIDDEN_FIELDS = {
    ".env",
    "absolute_path",
    "author_id",
    "author_ids",
    "author_name",
    "author_names",
    "collection_log_row_contents",
    "cookie",
    "cookies",
    "credential token",
    "evidence_items_csv_contents",
    "evidence_items_jsonl_contents",
    "export_download_public_final_delivery_payload",
    "finalsummaryreport_payload",
    "generated_public_message",
    "government id",
    "legal name",
    "official_verified",
    "package_path",
    "password",
    "passwords",
    "personal address",
    "personal email",
    "personality_diagnosis",
    "persuasion_score",
    "phone number",
    "prediction_probability",
    "private proof files",
    "private_message",
    "private_messages",
    "production_analysis_result_payload",
    "production_analysis_run_payload",
    "production_case_payload",
    "production_package_rows",
    "profile_url",
    "profile_urls",
    "psychological_profile",
    "raw author ids",
    "raw author names",
    "raw comments",
    "raw pii",
    "raw rows",
    "raw_author_id",
    "raw_author_ids",
    "raw_author_name",
    "raw_author_names",
    "raw_comment",
    "raw_comments",
    "raw_rows",
    "response_text",
    "route_api_frontend_trigger_payload",
    "salt",
    "salts",
    "secret",
    "secrets",
    "session",
    "sessions",
    "signature image",
    "source_manifest_row_contents",
    "source11_payload",
    "target_user_list",
    "token",
    "tokens",
    "truth_score",
    "write_execution_payload",
}


def build_non_authorizing_human_authority_declaration_fixture(
    fixture: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
) -> dict[str, Any]:
    """Build a local non-authorizing human-authority declaration fixture."""

    _require_exact_approval_phrase(exact_approval_phrase)
    if not isinstance(fixture, dict):
        raise ValueError("blocked_invalid_fixture:not_object")

    _validate_no_forbidden_content(fixture)
    _validate_no_unsafe_true_flags(fixture)

    safe_values = {
        field: _required_safe_label(fixture, field)
        for field in SAFE_INPUT_FIELDS
    }
    declaration = {
        "declaration_id": _declaration_id(safe_values),
        "declaration_schema": DECLARATION_SCHEMA,
        "declaration_status": _declaration_status(safe_values),
        "declaration_mode": DECLARATION_MODE,
        "declaration_scope": DECLARATION_SCOPE,
        **safe_values,
        "final_write_authorization_still_required": True,
        **{flag: False for flag in FALSE_FLAGS},
    }

    _validate_no_forbidden_content(declaration)
    return declaration


def build_non_authorizing_human_authority_declaration_fixture_summary(
    fixture: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
) -> dict[str, Any]:
    declaration = build_non_authorizing_human_authority_declaration_fixture(
        fixture,
        exact_approval_phrase=exact_approval_phrase,
    )
    return {
        "summary_schema": SUMMARY_SCHEMA,
        "declaration_schema": declaration["declaration_schema"],
        "declaration_status": declaration["declaration_status"],
        "declaration_mode": declaration["declaration_mode"],
        "declaration_scope": declaration["declaration_scope"],
        "final_write_authorization_still_required": declaration[
            "final_write_authorization_still_required"
        ],
        **{flag: declaration[flag] for flag in FALSE_FLAGS},
    }


def _require_exact_approval_phrase(exact_approval_phrase: str | None) -> None:
    if exact_approval_phrase is None or exact_approval_phrase == "":
        raise ValueError("blocked_missing_exact_approval")
    if exact_approval_phrase != APPROVAL_PHRASE:
        raise ValueError("blocked_wrong_exact_approval")


def _validate_no_forbidden_content(value: Any, *, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            if _is_forbidden_field(key_text):
                raise ValueError(f"blocked_forbidden_field:{'.'.join((*path, key_text))}")
            _validate_no_forbidden_content(nested, path=(*path, key_text))
        return
    if isinstance(value, list):
        for index, nested in enumerate(value):
            _validate_no_forbidden_content(nested, path=(*path, str(index)))
        return
    if isinstance(value, str) and _looks_forbidden(value):
        raise ValueError(f"blocked_forbidden_value:{'.'.join(path) or 'value'}")


def _validate_no_unsafe_true_flags(value: Any, *, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            if key_text in FALSE_FLAGS and nested is True:
                raise ValueError(f"blocked_unsafe_true_flag:{'.'.join((*path, key_text))}")
            _validate_no_unsafe_true_flags(nested, path=(*path, key_text))
        return
    if isinstance(value, list):
        for index, nested in enumerate(value):
            _validate_no_unsafe_true_flags(nested, path=(*path, str(index)))


def _is_forbidden_field(key: str) -> bool:
    return key.strip().lower() in FORBIDDEN_FIELDS


def _looks_forbidden(value: str) -> bool:
    stripped = value.strip()
    lowered = stripped.lower()
    if ":\\" in stripped or ":/" in stripped:
        return True
    if stripped.startswith("../") or stripped.startswith("..\\"):
        return True
    if "/../" in stripped or "\\..\\" in stripped:
        return True
    if lowered.startswith("http://") or lowered.startswith("https://"):
        return True
    if ".env" in lowered:
        return True
    forbidden_fragments = [
        "actual-token-should-never-appear",
        "actual-cookie-should-never-appear",
        "actual-secret-should-never-appear",
        "actual-raw-author-should-never-appear",
        "actual-author-name-should-never-appear",
        "actual-profile-url-should-never-appear",
        "actual-raw-comment-should-never-appear",
        "private-collector",
        "private_collector",
        "evidence_items.jsonl",
        "evidence_items.csv",
        "source_manifest",
        "collection_log",
        "donglu_sunjihai_youth_football/",
        "donglu_sunjihai_youth_football\\",
    ]
    return any(fragment in lowered for fragment in forbidden_fragments)


def _required_safe_label(source: dict[str, Any], field: str) -> str:
    label = _safe_label(source.get(field))
    if label is None:
        raise ValueError(f"blocked_invalid_fixture:{field}")
    return label


def _safe_label(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or _looks_forbidden(stripped):
        return None
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", stripped)[:120]


def _declaration_status(safe_values: dict[str, str]) -> str:
    status_labels = " ".join(safe_values[field] for field in SAFE_INPUT_FIELDS).lower()
    if "privacy_issue_stop" in status_labels:
        return PRIVACY_STATUS
    if "paused" in status_labels:
        return PAUSED_STATUS
    if safe_values["blocker_review_status"] in {
        "no_blockers_in_fixture",
        "cleared_for_non_authorizing_fixture_review",
    }:
        return READY_STATUS
    return BLOCKED_STATUS


def _declaration_id(safe_values: dict[str, str]) -> str:
    identity = "|".join(safe_values[field] for field in SAFE_INPUT_FIELDS)
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:12]
    return f"non-authorizing-human-authority-declaration-{digest}"
