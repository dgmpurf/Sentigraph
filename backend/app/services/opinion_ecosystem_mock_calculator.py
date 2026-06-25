from __future__ import annotations

from collections.abc import Iterable
from typing import Any


SCHEMA = "sentigraph_opinion_ecosystem_mock_calculator_run_v0_1"
MODEL_NAME = "sentigraph_opinion_ecosystem_weight_model"
MODEL_VERSION = "0.1"
MODEL_STATUS = "8P_1_metadata_skeleton"
COEFFICIENT_SOURCE = "mock_default"
CALIBRATION_STATUS = "uncalibrated"
EMPIRICAL_VALIDATION = "not_started"
GENERATED_AT = "not_runtime_generated_in_8P_1"
SCOPE_NOTE = "selected_sample_or_local_fixture_only"
NOT_CALCULATED = "not_calculated_in_8P_1"

REQUIRED_METADATA_FIELDS = (
    "fixture_id",
    "case_id",
    "sample_id",
    "fixture_role",
    "source_mode",
    "stage_id",
    "coverage_note",
)

REQUIRED_TRUE_METADATA_FLAGS = (
    "selected_sample_only",
    "not_full_web",
    "not_full_platform",
)

REQUIRED_BOUNDARY_FLAGS = (
    "not_full_web",
    "not_full_platform",
    "not_official_verification",
    "not_causal_proof",
    "not_prediction",
    "not_personality_diagnosis",
    "not_individual_persuasion_scoring",
    "not_public_opinion_control",
    "not_auto_executed",
    "selected_sample_only",
    "evidence_not_truth",
    "human_review_required",
)

FORBIDDEN_FIELD_KEYS = {
    "raw_author_id",
    "raw_author_name",
    "author_id",
    "author_name",
    "profile_url",
    "private_message",
    "private_messages",
    "dm_content",
    "cookie",
    "cookies",
    "token",
    "tokens",
    "access_token",
    "refresh_token",
    "session",
    "sessions",
    "browser_profile",
    "browser_profile_path",
    "profile_path",
    "localstorage",
    "secret",
    "secrets",
    "api_key",
    "password",
    "raw_author_identifiers",
}

OVERCLAIM_KEYS = {
    "full_web_claim",
    "full_platform_claim",
    "official_verification_claim",
    "causal_proof_claim",
    "prediction_claim",
    "personality_diagnosis_claim",
    "individual_persuasion_scoring_claim",
    "public_opinion_control_claim",
}

PLATFORM_FIELD_KEYS = {
    "platform",
    "platform_hint",
    "source_platform",
    "source_platform_claim",
    "platform_claim",
}

UNKNOWN_PLATFORM_VALUES = {
    "future_forum",
    "unknown_platform",
    "experimental_platform",
    "unsupported_platform",
    "placeholder_platform",
    "unconfigured_platform",
}


def _iter_fields(value: Any, path: str = "") -> Iterable[tuple[str, str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            child_path = f"{path}.{key_text}" if path else key_text
            yield child_path, key_text, child
            yield from _iter_fields(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = f"{path}[{index}]" if path else f"[{index}]"
            yield from _iter_fields(child, child_path)


def _blocker(field: str, path: str, reason: str, category: str) -> dict[str, str]:
    return {
        "field": field,
        "path": path,
        "reason": reason,
        "category": category,
    }


def _warning(field: str, path: str, reason: str, category: str) -> dict[str, str]:
    return {
        "field": field,
        "path": path,
        "reason": reason,
        "category": category,
    }


def _is_truthy_claim(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "claimed", "enabled"}
    if isinstance(value, (int, float)):
        return bool(value)
    return False


def find_forbidden_fixture_fields(fixture: object) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for path, key, _value in _iter_fields(fixture):
        if key.lower() in FORBIDDEN_FIELD_KEYS:
            findings.append(
                _blocker(
                    field=key,
                    path=path,
                    reason="forbidden_identity_or_sensitive_field",
                    category="forbidden_field",
                )
            )
    return findings


def _find_response_strategy_blockers(fixture: object) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    for path, key, value in _iter_fields(fixture):
        key_lower = key.lower()
        value_is_auto = isinstance(value, str) and value.strip().lower() == "auto_execute"
        if key_lower == "auto_execute" or value_is_auto:
            blockers.append(
                _blocker(
                    field=key,
                    path=path,
                    reason="auto_execute_is_forbidden",
                    category="response_strategy_blocker",
                )
            )
    return blockers


def _find_overclaim_blockers(fixture: object) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    for path, key, value in _iter_fields(fixture):
        if key.lower() in OVERCLAIM_KEYS and _is_truthy_claim(value):
            blockers.append(
                _blocker(
                    field=key,
                    path=path,
                    reason="overclaim_flag_is_forbidden",
                    category="overclaim_blocker",
                )
            )
    return blockers


def _find_unknown_platform_warnings(fixture: object) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []
    for path, key, value in _iter_fields(fixture):
        if key.lower() not in PLATFORM_FIELD_KEYS or not isinstance(value, str):
            continue
        if value.strip().lower() in UNKNOWN_PLATFORM_VALUES:
            warnings.append(
                _warning(
                    field=key,
                    path=path,
                    reason="unknown_or_future_platform_requires_manual_review",
                    category="unknown_or_future_platform",
                )
            )
    return warnings


def _validate_required_fixture_shape(fixture: object) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if not isinstance(fixture, dict):
        return [
            _blocker(
                field="fixture",
                path="fixture",
                reason="fixture_must_be_dict",
                category="fixture_contract_blocker",
            )
        ]

    metadata = fixture.get("fixture_metadata")
    if not isinstance(metadata, dict):
        return [
            _blocker(
                field="fixture_metadata",
                path="fixture_metadata",
                reason="fixture_metadata_must_be_dict",
                category="fixture_contract_blocker",
            )
        ]

    for field in REQUIRED_METADATA_FIELDS:
        if metadata.get(field) in (None, ""):
            blockers.append(
                _blocker(
                    field=field,
                    path=f"fixture_metadata.{field}",
                    reason="required_fixture_metadata_missing",
                    category="fixture_contract_blocker",
                )
            )

    for flag in REQUIRED_TRUE_METADATA_FLAGS:
        if metadata.get(flag) is not True:
            blockers.append(
                _blocker(
                    field=flag,
                    path=f"fixture_metadata.{flag}",
                    reason="required_fixture_boundary_flag_missing_or_false",
                    category="fixture_contract_blocker",
                )
            )

    return blockers


def validate_mock_fixture_contract(fixture: dict) -> dict[str, Any]:
    shape_blockers = _validate_required_fixture_shape(fixture)
    forbidden_fields = find_forbidden_fixture_fields(fixture)
    overclaim_blockers = _find_overclaim_blockers(fixture)
    response_strategy_blockers = _find_response_strategy_blockers(fixture)
    unknown_platform_warnings = _find_unknown_platform_warnings(fixture)

    blockers = [
        *shape_blockers,
        *forbidden_fields,
        *overclaim_blockers,
        *response_strategy_blockers,
    ]
    warnings = [*unknown_platform_warnings]

    if blockers:
        status = "blocked"
    elif warnings:
        status = "manual_review_required"
    else:
        status = "metadata_ready"

    return {
        "status": status,
        "compatibility_status": status,
        "human_review_required": True,
        "blockers": blockers,
        "warnings": warnings,
        "forbidden_fields": forbidden_fields,
        "overclaim_blockers": overclaim_blockers,
        "response_strategy_blockers": response_strategy_blockers,
        "unknown_platform_warnings": unknown_platform_warnings,
        "forbidden_field_count": len(forbidden_fields),
        "overclaim_blocker_count": len(overclaim_blockers),
        "response_strategy_blocker_count": len(response_strategy_blockers),
        "unknown_platform_warning_count": len(unknown_platform_warnings),
    }


def _fixture_metadata(fixture: dict) -> dict[str, Any]:
    if isinstance(fixture, dict) and isinstance(fixture.get("fixture_metadata"), dict):
        return fixture["fixture_metadata"]
    return {}


def _fixture_value(fixture: dict, field: str, fallback: str) -> str:
    value = _fixture_metadata(fixture).get(field, fallback)
    if value in (None, ""):
        return fallback
    return str(value)


def _boundary_flags() -> dict[str, bool]:
    return {
        "not_full_web": True,
        "not_full_platform": True,
        "not_official_verification": True,
        "not_causal_proof": True,
        "not_prediction": True,
        "not_personality_diagnosis": True,
        "not_individual_persuasion_scoring": True,
        "not_public_opinion_control": True,
        "not_auto_executed": True,
        "selected_sample_only": True,
        "evidence_not_truth": True,
        "human_review_required": True,
    }


def _runtime_side_effects() -> dict[str, bool]:
    return {
        "real_api_calls": False,
        "real_llm_calls": False,
        "url_fetching": False,
        "scraping": False,
        "collector_jobs_run": False,
        "evidence_items_read": False,
        "evidence_items_parsed": False,
        "evidence_items_imported": False,
        "evidence_layer_written": False,
        "production_case_created": False,
        "analysis_run_created": False,
        "b_end_report_generated": False,
        "sandbox_fixture_generated": False,
        "public_event_page_generated": False,
        "auto_execute": False,
    }


def _module_outputs() -> dict[str, str]:
    return {
        "content_aggregate": NOT_CALCULATED,
        "influence_core": NOT_CALCULATED,
        "echo_box": NOT_CALCULATED,
        "people_cluster": NOT_CALCULATED,
        "response_strategy": NOT_CALCULATED,
    }


def build_mock_calculator_run_metadata(fixture: dict) -> dict[str, Any]:
    validation = validate_mock_fixture_contract(fixture)
    fixture_id = _fixture_value(fixture, "fixture_id", "missing_fixture_id")
    case_id = _fixture_value(fixture, "case_id", "missing_case_id")
    sample_id = _fixture_value(fixture, "sample_id", "missing_sample_id")

    return {
        "schema": SCHEMA,
        "run_id": f"mock_run_{fixture_id}",
        "fixture_id": fixture_id,
        "case_id": case_id,
        "sample_id": sample_id,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "model_status": MODEL_STATUS,
        "coefficient_source": COEFFICIENT_SOURCE,
        "calibration_status": CALIBRATION_STATUS,
        "empirical_validation": EMPIRICAL_VALIDATION,
        "generated_at": GENERATED_AT,
        "scope_note": SCOPE_NOTE,
        "human_review_required": True,
        "boundary_flags": _boundary_flags(),
        "runtime_side_effects": _runtime_side_effects(),
        "validation_summary": {
            "status": validation["status"],
            "blockers": validation["blockers"],
            "warnings": validation["warnings"],
            "forbidden_field_count": validation["forbidden_field_count"],
            "overclaim_blocker_count": validation["overclaim_blocker_count"],
            "response_strategy_blocker_count": validation["response_strategy_blocker_count"],
            "unknown_platform_warning_count": validation["unknown_platform_warning_count"],
        },
        "module_outputs": _module_outputs(),
    }


def validate_output_boundary_flags(run: dict) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    flags = run.get("boundary_flags") if isinstance(run, dict) else None
    side_effects = run.get("runtime_side_effects") if isinstance(run, dict) else None

    if not isinstance(flags, dict):
        blockers.append(
            _blocker(
                field="boundary_flags",
                path="boundary_flags",
                reason="boundary_flags_must_be_dict",
                category="output_boundary_blocker",
            )
        )
    else:
        for flag in REQUIRED_BOUNDARY_FLAGS:
            if flags.get(flag) is not True:
                blockers.append(
                    _blocker(
                        field=flag,
                        path=f"boundary_flags.{flag}",
                        reason="required_boundary_flag_missing_or_false",
                        category="output_boundary_blocker",
                    )
                )

    if not isinstance(side_effects, dict):
        blockers.append(
            _blocker(
                field="runtime_side_effects",
                path="runtime_side_effects",
                reason="runtime_side_effects_must_be_dict",
                category="output_boundary_blocker",
            )
        )
    else:
        for key, value in side_effects.items():
            if value is not False:
                blockers.append(
                    _blocker(
                        field=str(key),
                        path=f"runtime_side_effects.{key}",
                        reason="runtime_side_effect_flag_must_be_false",
                        category="output_boundary_blocker",
                    )
                )

    return {
        "status": "blocked" if blockers else "pass",
        "blockers": blockers,
        "human_review_required": True,
    }


def calculate_opinion_ecosystem_mock_fixture(fixture: dict) -> dict[str, Any]:
    run = build_mock_calculator_run_metadata(fixture)
    boundary_validation = validate_output_boundary_flags(run)
    if boundary_validation["status"] == "blocked":
        run["validation_summary"]["status"] = "blocked"
        run["validation_summary"]["blockers"] = [
            *run["validation_summary"]["blockers"],
            *boundary_validation["blockers"],
        ]
    return run

