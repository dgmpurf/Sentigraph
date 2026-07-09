from __future__ import annotations

import hashlib
import re
from typing import Any


APPROVAL_PHRASE = (
    "APPROVE_9A_4_CONTROLLED_NO_WRITE_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_"
    "AUTHORIZATION_READINESS_CANDIDATE_FIXTURE_SMOKE"
)
INPUT_SCHEMA = "sentigraph_9a_4_no_write_authorization_readiness_input_v0_1"
CANDIDATE_SCHEMA = "sentigraph_actual_evidence_layer_write_authorization_readiness_candidate_v0_1"
SUMMARY_SCHEMA = "sentigraph_actual_evidence_layer_write_authorization_readiness_candidate_summary_v0_1"
CANDIDATE_MODE = "backend_only_local_no_write_authorization_readiness_candidate_fixture"
READY_STATUS = "candidate_ready_for_human_review_no_write"
BLOCKED_STATUS = "candidate_blocked_no_write"

FALSE_FLAGS = [
    "actual_evidence_layer_write_authorized",
    "actual_evidence_layer_write_performed",
    "production_evidenceitem_creation_authorized",
    "production_evidenceitem_created",
    "persisted_evidence_layer_record_created",
    "write_helper_execution_allowed",
    "helper_called",
    "evidenceitem_write_runtime_called",
    "human_authority_validated",
    "final_write_authorization_performed",
    "ready_for_actual_write",
    "write_authorization_object_created_that_permits_write",
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
    "api_key",
    "api_keys",
    "author_id",
    "author_ids",
    "author_name",
    "author_names",
    "collection_log_row_contents",
    "cookie",
    "cookies",
    "display_name",
    "download_id",
    "email",
    "evidence_items_csv_contents",
    "evidence_items_jsonl_contents",
    "export_download_public_final_delivery_payload",
    "finalsummaryreport_payload",
    "generated_public_message",
    "official_verified",
    "package_path",
    "password",
    "passwords",
    "personality_diagnosis",
    "persuasion_score",
    "phone",
    "prediction_probability",
    "private_message",
    "private_messages",
    "production_analysis_result_payload",
    "production_analysis_run_payload",
    "production_case_payload",
    "production_package_rows",
    "profile_url",
    "profile_urls",
    "psychological_profile",
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
    "source_manifest_row_contents",
    "source11_payload",
    "target_user_list",
    "token",
    "tokens",
    "truth_score",
    "url",
    "username",
    "write_execution_payload",
}

STATUS_LABEL_FIELDS = {
    "required_human_authority_status": "not_validated",
    "manual_review_responsibility_status": "requires_human_owner",
    "warning_count_acknowledgment_status": "acknowledgment_required",
    "human_review_required_acknowledgment_status": "acknowledgment_required",
    "no_automatic_trust_upgrade_acknowledgment_status": "acknowledgment_required",
}


def build_no_write_evidence_layer_write_authorization_readiness_candidate(
    fixture: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
) -> dict[str, Any]:
    """Build a local no-write readiness candidate from safe in-memory labels only."""

    _require_exact_approval_phrase(exact_approval_phrase)
    if not isinstance(fixture, dict):
        raise ValueError("blocked_invalid_fixture:not_object")

    _validate_no_forbidden_content(fixture)
    _validate_no_unsafe_true_flags(fixture)

    input_schema = _safe_label(fixture.get("input_schema"))
    if input_schema != INPUT_SCHEMA:
        raise ValueError("blocked_invalid_fixture:input_schema")

    input_source_kind = _required_safe_label(fixture, "input_source_kind")
    source_candidate_ref = _required_safe_label(fixture, "source_candidate_ref")
    input_lineage_summary = _required_safe_text(fixture, "input_lineage_summary")
    warning_count = _safe_non_negative_int(fixture.get("warning_count"), field="warning_count")

    blocker_statuses = _safe_label_collection(fixture.get("blocker_statuses"))
    risk_statuses = _safe_label_collection(fixture.get("risk_statuses"))
    acknowledgments = _safe_mapping(fixture.get("acknowledgment_statuses"))

    candidate: dict[str, Any] = {
        "candidate_id": _candidate_id(source_candidate_ref),
        "candidate_schema": CANDIDATE_SCHEMA,
        "candidate_status": BLOCKED_STATUS if _count_labels(blocker_statuses) else READY_STATUS,
        "candidate_mode": CANDIDATE_MODE,
        "input_source_kind": input_source_kind,
        "input_lineage_summary": input_lineage_summary,
        "required_human_authority_status": _status_label(
            acknowledgments,
            "required_human_authority_status",
        ),
        "manual_review_responsibility_status": _status_label(
            acknowledgments,
            "manual_review_responsibility_status",
        ),
        "warning_count_acknowledgment_status": _status_label(
            acknowledgments,
            "warning_count_acknowledgment_status",
        ),
        "human_review_required_acknowledgment_status": _status_label(
            acknowledgments,
            "human_review_required_acknowledgment_status",
        ),
        "no_automatic_trust_upgrade_acknowledgment_status": _status_label(
            acknowledgments,
            "no_automatic_trust_upgrade_acknowledgment_status",
        ),
        "blocker_statuses": blocker_statuses,
        "risk_statuses": risk_statuses,
        "safe_identity_policy_status": _safe_optional_label(
            fixture.get("safe_identity_policy_status"),
            default="safe_labels_only",
        ),
        "rollback_pause_policy_status": _safe_optional_label(
            fixture.get("rollback_pause_policy_status"),
            default="pause_before_actual_write",
        ),
        "audit_note_status": _safe_optional_label(
            fixture.get("audit_note_status"),
            default="placeholder_only",
        ),
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "warning_count": warning_count,
        "blocker_count": _count_labels(blocker_statuses),
        "risk_count": _count_labels(risk_statuses),
        "next_required_gate_label": "actual_write_requires_separate_future_gate",
        **{flag: False for flag in FALSE_FLAGS},
    }

    _validate_no_forbidden_content(candidate)
    return candidate


def build_safe_no_write_evidence_layer_write_authorization_readiness_candidate_summary(
    fixture: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
) -> dict[str, Any]:
    candidate = build_no_write_evidence_layer_write_authorization_readiness_candidate(
        fixture,
        exact_approval_phrase=exact_approval_phrase,
    )
    return {
        "summary_schema": SUMMARY_SCHEMA,
        "candidate_schema": candidate["candidate_schema"],
        "candidate_status": candidate["candidate_status"],
        "candidate_mode": candidate["candidate_mode"],
        "input_source_kind": candidate["input_source_kind"],
        "warning_count": candidate["warning_count"],
        "blocker_count": candidate["blocker_count"],
        "risk_count": candidate["risk_count"],
        "human_review_required": candidate["human_review_required"],
        "no_automatic_trust_upgrade": candidate["no_automatic_trust_upgrade"],
        "next_required_gate_label": candidate["next_required_gate_label"],
        **{flag: candidate[flag] for flag in FALSE_FLAGS},
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
    lowered = key.strip().lower()
    return lowered in FORBIDDEN_FIELDS


def _looks_forbidden(value: str) -> bool:
    stripped = value.strip()
    lowered = stripped.lower()
    if ":\\" in stripped or ":/" in stripped:
        return True
    if stripped.startswith("../") or stripped.startswith("..\\") or "/../" in stripped or "\\..\\" in stripped:
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


def _safe_mapping(value: Any) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError("blocked_invalid_fixture:acknowledgment_statuses")
    safe: dict[str, str] = {}
    for key, nested in value.items():
        safe_key = _safe_label(key)
        safe_value = _safe_label(nested)
        if safe_key is None or safe_value is None:
            raise ValueError("blocked_invalid_fixture:acknowledgment_statuses")
        safe[safe_key] = safe_value
    return safe


def _safe_label_collection(value: Any) -> dict[str, str] | list[str]:
    if value is None:
        return {}
    if isinstance(value, dict):
        safe: dict[str, str] = {}
        for key, nested in value.items():
            safe_key = _safe_label(key)
            safe_value = _safe_label(nested)
            if safe_key is None or safe_value is None:
                raise ValueError("blocked_invalid_fixture:status_label")
            safe[safe_key] = safe_value
        return safe
    if isinstance(value, list):
        safe_list: list[str] = []
        for item in value:
            safe_item = _safe_label(item)
            if safe_item is None:
                raise ValueError("blocked_invalid_fixture:status_label")
            safe_list.append(safe_item)
        return safe_list
    raise ValueError("blocked_invalid_fixture:status_label")


def _count_labels(value: dict[str, str] | list[str]) -> int:
    return len(value)


def _status_label(acknowledgments: dict[str, str], field: str) -> str:
    return acknowledgments.get(field) or STATUS_LABEL_FIELDS[field]


def _candidate_id(source_candidate_ref: str) -> str:
    digest = hashlib.sha256(source_candidate_ref.encode("utf-8")).hexdigest()[:12]
    return f"no-write-auth-readiness-{digest}"


def _required_safe_label(source: dict[str, Any], field: str) -> str:
    label = _safe_label(source.get(field))
    if label is None:
        raise ValueError(f"blocked_invalid_fixture:{field}")
    return label


def _required_safe_text(source: dict[str, Any], field: str) -> str:
    text = _safe_text(source.get(field))
    if text is None:
        raise ValueError(f"blocked_invalid_fixture:{field}")
    return text


def _safe_optional_label(value: Any, *, default: str) -> str:
    return _safe_label(value) or default


def _safe_non_negative_int(value: Any, *, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"blocked_invalid_fixture:{field}")
    return value


def _safe_label(value: Any) -> str | None:
    text = _safe_text(value)
    if text is None:
        return None
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", text)[:120]


def _safe_text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or _looks_forbidden(stripped):
        return None
    return stripped[:240]

