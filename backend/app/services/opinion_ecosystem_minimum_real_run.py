from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.services import opinion_ecosystem_mock_calculator as calculator


RUN_SCHEMA = "sentigraph_opinion_ecosystem_run_v0_1"
INPUT_SOURCE_KIND = "in_memory_safe_fixture"

MODULE_OUTPUT_MAP = {
    "content_aggregate": "ContentAggregate",
    "influence_core": "InfluenceCore",
    "echo_box": "EchoBox",
    "people_cluster": "PeopleCluster",
    "response_strategy": "ResponseStrategyComparisonV01",
}


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _fixture_metadata(fixture: dict[str, Any]) -> dict[str, Any]:
    metadata = fixture.get("fixture_metadata")
    return metadata if isinstance(metadata, dict) else {}


def _metadata_value(metadata: dict[str, Any], key: str, fallback: str) -> str:
    value = metadata.get(key)
    if value in (None, ""):
        return fallback
    return str(value)


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
        "human_review_required": True,
        "no_auto_execute": True,
        "no_generated_public_response": True,
    }


def _runtime_side_effects() -> dict[str, bool]:
    return {
        "called_real_api": False,
        "called_real_llm": False,
        "ran_collector": False,
        "accessed_private_collector": False,
        "read_real_exchange_dir": False,
        "fetched_url": False,
        "scraped_page": False,
        "parsed_evidence_items_file": False,
        "wrote_evidence_layer": False,
        "created_production_case": False,
        "created_analysis_run": False,
        "generated_b_end_report_runtime": False,
        "generated_sandbox_runtime": False,
        "generated_public_event_runtime": False,
        "generated_response_text": False,
        "published_or_sent": False,
        "auto_executed": False,
    }


def _response_strategy_blockers(calculator_run: dict[str, Any]) -> list[dict[str, str]]:
    source_outputs = calculator_run.get("module_outputs")
    if not isinstance(source_outputs, dict):
        return []
    outputs = source_outputs.get("response_strategy")
    if not isinstance(outputs, list):
        return []

    blockers: list[dict[str, str]] = []
    for index, output in enumerate(outputs):
        if not isinstance(output, dict):
            continue
        recommendation = output.get("recommendation")
        recommendation_level = recommendation.get("recommendation_level") if isinstance(recommendation, dict) else None
        if output.get("strategy_status") == "forbidden" or recommendation_level == "forbidden":
            blockers.append(
                {
                    "field": "response_strategy",
                    "path": f"module_outputs.response_strategy[{index}]",
                    "reason": "response_strategy_forbidden_by_calculator",
                    "category": "minimum_real_run_blocker",
                }
            )
    return blockers


def _all_blockers(calculator_run: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        *_validation_items(calculator_run, "blockers"),
        *_response_strategy_blockers(calculator_run),
    ]


def _run_status(calculator_run: dict[str, Any]) -> str:
    if _all_blockers(calculator_run):
        return "blocked"
    validation = calculator_run.get("validation_summary")
    if not isinstance(validation, dict):
        return "blocked"
    status = validation.get("status")
    if status == "metadata_ready":
        return "ready"
    if status == "manual_review_required":
        return "manual_review_required"
    return "blocked"


def _validation_items(calculator_run: dict[str, Any], key: str) -> list[dict[str, Any]]:
    validation = calculator_run.get("validation_summary")
    if not isinstance(validation, dict):
        return []
    value = validation.get(key)
    return value if isinstance(value, list) else []


def _module_outputs(calculator_run: dict[str, Any]) -> dict[str, Any]:
    source_outputs = calculator_run.get("module_outputs")
    if not isinstance(source_outputs, dict):
        source_outputs = {}
    return {
        contract_key: source_outputs.get(calculator_key, [])
        for calculator_key, contract_key in MODULE_OUTPUT_MAP.items()
    }


def generate_opinion_ecosystem_minimum_real_run(fixture: dict[str, Any]) -> dict[str, Any]:
    calculator_run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)
    metadata = _fixture_metadata(fixture)

    return {
        "run_id": f"minimum_real_run_{calculator_run.get('run_id', 'unknown')}",
        "run_schema": RUN_SCHEMA,
        "run_status": _run_status(calculator_run),
        "case_id": str(calculator_run.get("case_id") or _metadata_value(metadata, "case_id", "missing_case_id")),
        "sample_id": str(calculator_run.get("sample_id") or _metadata_value(metadata, "sample_id", "missing_sample_id")),
        "input_package_id": None,
        "input_source_kind": INPUT_SOURCE_KIND,
        "input_scope_note": str(calculator_run.get("scope_note") or "selected_sample_or_local_fixture_only"),
        "generated_at": _utc_timestamp(),
        "model_version": str(calculator_run.get("model_version") or calculator.MODEL_VERSION),
        "coefficient_source": str(calculator_run.get("coefficient_source") or calculator.COEFFICIENT_SOURCE),
        "calibration_status": str(calculator_run.get("calibration_status") or calculator.CALIBRATION_STATUS),
        "empirical_validation": str(calculator_run.get("empirical_validation") or calculator.EMPIRICAL_VALIDATION),
        "human_review_required": True,
        "boundary_flags": _boundary_flags(),
        "warnings": _validation_items(calculator_run, "warnings"),
        "blockers": _all_blockers(calculator_run),
        "module_outputs": _module_outputs(calculator_run),
        "runtime_side_effects": _runtime_side_effects(),
    }
