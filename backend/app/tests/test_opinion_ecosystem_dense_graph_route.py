from __future__ import annotations

import json

from fastapi.testclient import TestClient

from app.api.v1.routes import opinion_ecosystem_dense_graph
from app.main import app


client = TestClient(app)

ROUTE = "/api/v1/internal/opinion-ecosystem/dense-graph/generated-runs"
ENV_FLAG = "SENTIGRAPH_OPINION_ECOSYSTEM_DENSE_GRAPH_ROUTE_ENABLED"

REQUIRED_SIDE_EFFECT_FLAGS = {
    "called_real_api",
    "called_real_llm",
    "ran_collector",
    "accessed_private_collector",
    "read_real_exchange_dir",
    "fetched_url",
    "scraped_page",
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

FORBIDDEN_RESPONSE_KEYS = {
    "raw_author_id",
    "author_name",
    "raw_author_name",
    "profile_url",
    "username",
    "account_id",
    "cookie",
    "cookies",
    "session",
    "sessions",
    "token",
    "tokens",
    "browser_profile_path",
    "private_message",
    "private_messages",
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "auto_execute",
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


def test_route_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv(ENV_FLAG, raising=False)

    response = client.get(f"{ROUTE}/donglu-sunjihai-youth-football")

    assert response.status_code == 200
    body = response.json()
    assert body["error_schema"] == "sentigraph_opinion_ecosystem_dense_graph_route_error_v0_1"
    assert body["route_status"] == "disabled"
    assert body["error_code"] == "route_disabled"
    assert body["path_exposed"] is False
    assert body["raw_metadata_exposed"] is False
    assert body["private_collector_path_exposed"] is False
    assert body["evidence_rows_exposed"] is False


def test_falsey_and_unknown_env_values_disable_route(monkeypatch) -> None:
    for value in ("0", "false", "no", "enabled", "random"):
        monkeypatch.setenv(ENV_FLAG, value)
        body = client.get(f"{ROUTE}/donglu-sunjihai-youth-football").json()
        assert body["route_status"] == "disabled"
        assert body["error_code"] == "route_disabled"


def test_enabled_values_allow_known_sample(monkeypatch) -> None:
    for value in ("1", "true", "yes"):
        monkeypatch.setenv(ENV_FLAG, value)
        response = client.get(f"{ROUTE}/helldivers-psn")
        body = response.json()
        assert response.status_code == 200
        assert body["response_schema"] == "sentigraph_opinion_ecosystem_dense_graph_route_response_v0_1"
        assert body["route_status"] in {"ready", "degraded", "blocked"}
        assert body["sample_id"] == "helldivers-psn"


def test_disabled_route_does_not_call_dense_graph_service(monkeypatch) -> None:
    monkeypatch.delenv(ENV_FLAG, raising=False)

    def fail_if_called(*args, **kwargs):
        raise AssertionError("dense graph service must not be called when route is disabled")

    monkeypatch.setattr(
        opinion_ecosystem_dense_graph.integration,
        "generate_opinion_ecosystem_run_with_dense_graph_attachment",
        fail_if_called,
    )

    body = client.get(f"{ROUTE}/donglu-sunjihai-youth-football").json()

    assert body["route_status"] == "disabled"


def test_get_only_route_surface(monkeypatch) -> None:
    monkeypatch.setenv(ENV_FLAG, "1")

    response = client.post(f"{ROUTE}/donglu-sunjihai-youth-football")

    assert response.status_code == 405


def test_known_dong_sun_sample_returns_safe_dense_graph_response(monkeypatch) -> None:
    monkeypatch.setenv(ENV_FLAG, "1")

    response = client.get(f"{ROUTE}/donglu-sunjihai-youth-football")
    body = response.json()

    assert response.status_code == 200
    assert body["route_status"] == "ready"
    assert body["sample_id"] == "donglu-sunjihai-youth-football"
    assert body["generated_run_integration"]["integration_schema"] == (
        "sentigraph_opinion_ecosystem_generated_run_dense_graph_integration_v0_1"
    )
    assert body["graph_summary"]["people_cluster_proxy_count"] > 0
    assert body["graph_summary"]["edge_count"] > 0
    assert body["graph_summary"]["timeline_bucket_count"] > 0
    assert body["generated_run_integration"]["integration_summary"]["frontend_ready"] is False
    assert body["generated_run_integration"]["integration_summary"]["production_ready"] is False


def test_known_sample_response_includes_preview_policy_and_bounded_limits(monkeypatch) -> None:
    monkeypatch.setenv(ENV_FLAG, "yes")

    body = client.get(
        f"{ROUTE}/donglu-sunjihai-youth-football",
        params={"node_limit": 9999, "edge_limit": 9999, "include_previews": "true"},
    ).json()

    assert body["preview_limits"] == {"node_limit": 240, "edge_limit": 800, "include_previews": True}
    attachment = body["generated_run_integration"]["dense_graph_attachment"]
    assert len(attachment["nodes_preview"]) <= 240
    assert len(attachment["edges_preview"]) <= 800
    assert body["graph_summary"]["recommended_visualization_mode"] == "dense_sandbox_proxy_graph"


def test_lower_bound_limits_are_clamped(monkeypatch) -> None:
    monkeypatch.setenv(ENV_FLAG, "1")

    body = client.get(
        f"{ROUTE}/helldivers-psn",
        params={"node_limit": 1, "edge_limit": 1, "include_previews": "false"},
    ).json()

    assert body["preview_limits"] == {"node_limit": 20, "edge_limit": 50, "include_previews": False}
    attachment = body["generated_run_integration"]["dense_graph_attachment"]
    assert attachment["nodes_preview"] == []
    assert attachment["edges_preview"] == []


def test_unknown_sample_returns_safe_unsupported_sample_without_fallback(monkeypatch) -> None:
    monkeypatch.setenv(ENV_FLAG, "true")

    body = client.get(f"{ROUTE}/future-live-provider").json()

    assert body["route_status"] == "unsupported_sample"
    assert body["error_code"] == "unsupported_sample"
    assert body["sample_id"] == "future-live-provider"
    assert body["path_exposed"] is False
    assert body["evidence_rows_exposed"] is False


def test_path_traversal_sample_is_rejected_safely(monkeypatch) -> None:
    monkeypatch.setenv(ENV_FLAG, "1")

    body = client.get(f"{ROUTE}/..%2Fdocs%2Fsamples%2Fsecret").json()

    assert body["route_status"] == "unsupported_sample"
    assert body["error_code"] == "unsupported_sample"
    assert body["path_exposed"] is False


def test_response_does_not_include_forbidden_fields(monkeypatch) -> None:
    monkeypatch.setenv(ENV_FLAG, "1")

    body = client.get(f"{ROUTE}/donglu-sunjihai-youth-football").json()
    encoded = json.dumps(body, ensure_ascii=False)

    assert not (FORBIDDEN_RESPONSE_KEYS & _walk_keys(body))
    assert "G:\\AICODING\\网页端任务二" not in encoded
    assert "private collector" not in encoded.lower()


def test_runtime_side_effect_flags_false_and_no_production_side_effects(monkeypatch) -> None:
    monkeypatch.setenv(ENV_FLAG, "1")

    body = client.get(f"{ROUTE}/donglu-sunjihai-youth-football").json()

    assert REQUIRED_SIDE_EFFECT_FLAGS <= set(body["runtime_side_effects"])
    assert all(body["runtime_side_effects"][flag] is False for flag in REQUIRED_SIDE_EFFECT_FLAGS)
    assert body["generated_run_integration"]["integration_summary"]["route_ready"] is False
    assert body["generated_run_integration"]["integration_summary"]["production_ready"] is False


def test_no_frontend_files_or_route_for_arbitrary_path_parameter(monkeypatch) -> None:
    monkeypatch.setenv(ENV_FLAG, "1")

    body = client.get(
        f"{ROUTE}/donglu-sunjihai-youth-football",
        params={"package_path": "G:/AICODING/private/evidence_items.jsonl"},
    ).json()

    assert body["route_status"] == "unsupported_sample"
    assert body["error_code"] == "unsupported_query_parameter"
    assert body["path_exposed"] is False
