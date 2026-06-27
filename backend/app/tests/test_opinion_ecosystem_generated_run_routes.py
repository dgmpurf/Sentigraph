from __future__ import annotations

import inspect

from fastapi.testclient import TestClient

from app.api.v1.routes import opinion_ecosystem_generated_runs
from app.main import app


client = TestClient(app)

ROUTE = "/api/v1/opinion-ecosystem/generated-runs/local-fixture"

REQUIRED_BOUNDARY_FLAGS = {
    "selected_sample_only",
    "not_full_web",
    "not_full_platform",
    "not_full_thread",
    "not_official_verification",
    "not_causal_proof",
    "not_prediction",
    "not_production_score",
    "human_review_required",
    "no_auto_execute",
    "no_generated_public_response",
}

REQUIRED_SIDE_EFFECT_FLAGS = {
    "called_real_api",
    "called_real_llm",
    "ran_collector",
    "accessed_private_collector",
    "read_real_exchange_dir",
    "fetched_url",
    "scraped_page",
    "parsed_evidence_items_file",
    "wrote_evidence_layer",
    "created_production_case",
    "created_analysis_run",
    "generated_b_end_report_runtime",
    "generated_sandbox_runtime",
    "generated_public_event_runtime",
    "generated_response_text",
    "published_or_sent",
    "auto_executed",
}

REQUIRED_MODULE_KEYS = {
    "ContentAggregate",
    "InfluenceCore",
    "EchoBox",
    "PeopleCluster",
    "ResponseStrategyComparisonV01",
}

FORBIDDEN_RESPONSE_KEYS = {
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
}


def _walk_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(_walk_keys(child))
    return keys


def test_post_local_fixture_returns_generated_run_contract() -> None:
    response = client.post(
        ROUTE,
        json={"sample_key": "mock_default", "case_id": "case_route_8s4", "sample_id": "sample_route_8s4"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["run_id"].startswith("minimum_real_run_")
    assert body["run_schema"] == "sentigraph_opinion_ecosystem_run_v0_1"
    assert body["run_status"] == "ready"
    assert body["case_id"] == "case_route_8s4"
    assert body["sample_id"] == "sample_route_8s4"
    assert body["input_package_id"] is None
    assert body["input_source_kind"] == "in_memory_safe_fixture"
    assert body["model_version"] == "0.1"
    assert body["coefficient_source"] == "mock_default"
    assert body["calibration_status"] == "uncalibrated"
    assert body["empirical_validation"] == "not_started"
    assert body["human_review_required"] is True


def test_response_includes_required_boundaries_side_effects_and_modules() -> None:
    body = client.post(ROUTE, json={"sample_key": "helldivers_psn"}).json()

    assert REQUIRED_BOUNDARY_FLAGS <= set(body["boundary_flags"])
    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert body["boundary_flags"][flag] is True

    assert REQUIRED_SIDE_EFFECT_FLAGS <= set(body["runtime_side_effects"])
    for flag in REQUIRED_SIDE_EFFECT_FLAGS:
        assert body["runtime_side_effects"][flag] is False

    assert REQUIRED_MODULE_KEYS == set(body["module_outputs"])


def test_unknown_sample_key_returns_safe_4xx_without_fallback() -> None:
    response = client.post(ROUTE, json={"sample_key": "future_live_provider"})

    assert 400 <= response.status_code < 500
    detail = str(response.json().get("detail", "")).lower()
    assert "unsupported" in detail
    assert "provider" not in detail or "unsupported" in detail


def test_forbidden_request_fields_are_rejected() -> None:
    forbidden_payloads = [
        {"sample_key": "mock_default", "exchange_dir": "G:/AICODING/private"},
        {"sample_key": "mock_default", "package_root": "G:/AICODING/private/package"},
        {"sample_key": "mock_default", "evidence_items": "docs/samples/evidence_items.jsonl"},
        {"sample_key": "mock_default", "raw_author_id": "hidden"},
        {"sample_key": "mock_default", "cookie": "hidden"},
        {"sample_key": "mock_default", "token": "hidden"},
        {"sample_key": "mock_default", "session": "hidden"},
        {"sample_key": "mock_default", "browser_profile": "hidden"},
        {"sample_key": "mock_default", "private_message": "hidden"},
        {"sample_key": "mock_default", "raw_evidence_rows": [{"text": "not allowed"}]},
        {"sample_key": "mock_default", "publish_now": True},
        {"sample_key": "mock_default", "send_now": True},
        {"sample_key": "mock_default", "post_now": True},
        {"sample_key": "mock_default", "execute_now": True},
    ]

    for payload in forbidden_payloads:
        response = client.post(ROUTE, json=payload)
        assert 400 <= response.status_code < 500


def test_response_does_not_include_forbidden_output_keys() -> None:
    body = client.post(ROUTE, json={"sample_key": "donglu_sunjihai_youth_football"}).json()

    assert not (FORBIDDEN_RESPONSE_KEYS & _walk_keys(body))


def test_route_source_has_no_file_io_network_or_runtime_tokens() -> None:
    source = inspect.getsource(opinion_ecosystem_generated_runs)
    forbidden_tokens = [
        "op" + "en(",
        "Path(",
        "read" + "_text",
        "write" + "_text",
        "json.load",
        "json.dump",
        "requests.",
        "httpx.",
        "urllib.",
        "fetch(",
        "axios.",
        "FileResponse",
        "StreamingResponse",
        "evidence" + "_items.jsonl",
        "evidence" + "_items.csv",
    ]

    for token in forbidden_tokens:
        assert token not in source
