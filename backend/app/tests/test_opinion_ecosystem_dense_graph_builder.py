from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.services import opinion_ecosystem_dense_graph_builder as dense_builder


REQUIRED_BOUNDARY_FLAGS = {
    "selected_sample_only",
    "not_full_web",
    "not_full_platform",
    "not_full_thread",
    "not_official_verification",
    "not_causal_proof",
    "not_prediction",
    "not_production_score",
    "no_auto_execute",
    "no_generated_public_response",
    "anonymous_aggregate_only",
}

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

FORBIDDEN_OUTPUT_KEYS = {
    "raw_author_id",
    "author_id",
    "author_name",
    "profile_url",
    "private_message",
    "cookie",
    "session",
    "token",
    "password",
    "api_key",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "response_text",
    "generated_public_message",
    "auto_execute",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
}


def _evidence(index: int, **overrides: object) -> dict:
    platforms = ["bilibili", "weibo", "news", "forum"]
    stances = ["support", "neutral", "oppose", "mixed"]
    item = {
        "evidence_id": f"evidence_{index:03d}",
        "platform": platforms[index % len(platforms)],
        "source_type": "comment" if index % 3 else "post",
        "source_name": f"source_{index % 5}",
        "source_url": f"https://example.test/thread/{index % 7}",
        "title": f"Safe title {index % 4}",
        "body_text": f"safe public sample text bucket {index % 9}",
        "created_at": f"2026-06-{(index % 7) + 1:02d}T12:00:00Z",
        "stance_hint": stances[index % len(stances)],
        "emotion_intensity_hint": (index % 10) / 10,
        "attention_hint": ((index + 3) % 10) / 10,
        "trust_label": "medium",
        "review_status": "approved",
        "duplicate_group_id": f"dup_{index}",
        "duplicate_count": 1,
    }
    item.update(overrides)
    return item


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


def _walk_values(value: object) -> list[object]:
    values: list[object] = []
    if isinstance(value, dict):
        for child in value.values():
            values.extend(_walk_values(child))
    elif isinstance(value, list):
        for child in value:
            values.extend(_walk_values(child))
    else:
        values.append(value)
    return values


def _people_nodes(run: dict) -> list[dict]:
    return [node for node in run["graph"]["nodes"] if node["node_type"] == "people_cluster_proxy"]


def test_builds_dense_graph_from_small_synthetic_evidence_list() -> None:
    run = dense_builder.build_dense_opinion_graph_from_evidence_items(
        [_evidence(index) for index in range(8)],
        sample_id="unit_small",
        max_people_clusters=60,
        max_edges=160,
    )

    assert run["run_schema"] == "sentigraph_opinion_ecosystem_dense_graph_run_v0_1"
    assert run["run_status"] == "generated_local_dense_graph"
    assert run["sample_id"] == "unit_small"
    assert run["coefficient_source"] == "mock_default"
    assert run["calibration_status"] == "uncalibrated"
    assert run["empirical_validation"] == "not_started"
    assert run["human_review_required"] is True
    assert REQUIRED_BOUNDARY_FLAGS <= set(run["boundary_flags"])
    assert all(run["boundary_flags"][flag] is True for flag in REQUIRED_BOUNDARY_FLAGS)
    assert REQUIRED_SIDE_EFFECT_FLAGS <= set(run["runtime_side_effects"])
    assert all(run["runtime_side_effects"][flag] is False for flag in REQUIRED_SIDE_EFFECT_FLAGS)
    assert _people_nodes(run)
    assert run["graph"]["timeline_buckets"]
    assert run["graph"]["graph_summary"]["people_cluster_proxy_count"] == len(_people_nodes(run))


def test_produces_many_anonymous_people_cluster_nodes_from_larger_sample() -> None:
    evidence_items = [_evidence(index) for index in range(48)]

    run = dense_builder.build_dense_opinion_graph_from_evidence_items(
        evidence_items,
        sample_id="unit_dense",
        max_people_clusters=180,
        max_edges=500,
    )
    people_nodes = _people_nodes(run)

    assert len(people_nodes) >= 96
    assert len(people_nodes) <= 180
    assert len(run["graph"]["edges"]) <= 500
    assert {node["node_id"] for node in people_nodes} == {f"pc_{index:04d}" for index in range(1, len(people_nodes) + 1)}
    assert all(node["boundary_note"] == "anonymous_aggregate_proxy_not_real_person" for node in people_nodes)


def test_does_not_expose_raw_author_identifiers_or_identity_values() -> None:
    evidence_items = [
        _evidence(
            1,
            raw_author_id="raw-person-1",
            author_name="Real Name",
            profile_url="https://example.test/profile/person",
        )
    ]

    run = dense_builder.build_dense_opinion_graph_from_evidence_items(evidence_items, sample_id="identity_blocked")
    text = json.dumps(run, ensure_ascii=False)

    assert run["run_status"] == "blocked"
    assert "raw-person-1" not in text
    assert "Real Name" not in text
    assert "profile/person" not in text
    assert not (FORBIDDEN_OUTPUT_KEYS & _walk_keys(run))
    assert run["privacy_scan"]["raw_identifier_found"] is True


def test_forbidden_fields_are_blocked_without_exposing_values() -> None:
    evidence_items = [
        _evidence(
            2,
            token="secret-token-value",
            response_text="draft public response",
            publish_now=True,
            psychological_profile={"x": "do not expose"},
        )
    ]

    run = dense_builder.build_dense_opinion_graph_from_evidence_items(evidence_items, sample_id="forbidden_blocked")
    text = json.dumps(run, ensure_ascii=False)

    assert run["run_status"] == "blocked"
    assert run["blockers"]
    assert "secret-token-value" not in text
    assert "draft public response" not in text
    assert "do not expose" not in text
    assert not (FORBIDDEN_OUTPUT_KEYS & _walk_keys(run))


def test_rejected_evidence_does_not_amplify_people_nodes() -> None:
    base = [_evidence(index) for index in range(10)]
    with_rejected = [*base, *[_evidence(100 + index, review_status="rejected") for index in range(40)]]

    base_run = dense_builder.build_dense_opinion_graph_from_evidence_items(base, sample_id="base", max_people_clusters=120)
    rejected_run = dense_builder.build_dense_opinion_graph_from_evidence_items(
        with_rejected,
        sample_id="with_rejected",
        max_people_clusters=120,
    )

    assert len(_people_nodes(rejected_run)) == len(_people_nodes(base_run))
    assert rejected_run["graph"]["graph_summary"]["rejected_excluded_count"] == 40


def test_duplicates_do_not_over_amplify_nodes() -> None:
    unique = [_evidence(index, duplicate_group_id=f"dup_{index}") for index in range(12)]
    duplicated = [
        *unique,
        *[_evidence(200 + index, duplicate_group_id="same_dup", duplicate_count=40) for index in range(60)],
    ]

    unique_run = dense_builder.build_dense_opinion_graph_from_evidence_items(unique, sample_id="unique", max_people_clusters=160)
    duplicate_run = dense_builder.build_dense_opinion_graph_from_evidence_items(
        duplicated,
        sample_id="duplicated",
        max_people_clusters=160,
    )

    assert len(_people_nodes(duplicate_run)) <= len(_people_nodes(unique_run)) + 8
    assert duplicate_run["graph"]["graph_summary"]["duplicate_folded_count"] >= 60


def test_output_is_json_serializable() -> None:
    run = dense_builder.build_dense_opinion_graph_from_evidence_items(
        [_evidence(index) for index in range(16)],
        sample_id="json_serializable",
    )

    encoded = json.dumps(run, ensure_ascii=False, sort_keys=True)
    assert "sentigraph_opinion_ecosystem_dense_graph_run_v0_1" in encoded


def test_controlled_repo_sample_loader_rejects_absolute_path() -> None:
    with pytest.raises(ValueError, match="repo_relative_path_required"):
        dense_builder.load_controlled_repo_sample_evidence_items(Path("C:/outside/evidence_items.jsonl"))


def test_controlled_repo_sample_loader_rejects_path_traversal() -> None:
    with pytest.raises(ValueError, match="docs_samples_only"):
        dense_builder.load_controlled_repo_sample_evidence_items("../docs/samples/demo/evidence_items.jsonl")


def test_controlled_repo_sample_loader_reads_jsonl_under_docs_samples(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    sample_dir = tmp_path / "docs" / "samples" / "unit"
    sample_dir.mkdir(parents=True)
    sample_file = sample_dir / "evidence_items.jsonl"
    sample_file.write_text(
        json.dumps(_evidence(1), ensure_ascii=False) + "\n" + json.dumps(_evidence(2), ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(dense_builder, "REPO_ROOT", tmp_path)

    items = dense_builder.load_controlled_repo_sample_evidence_items("docs/samples/unit/evidence_items.jsonl")

    assert [item["evidence_id"] for item in items] == ["evidence_001", "evidence_002"]


def test_controlled_repo_sample_loader_rejects_non_jsonl_under_docs_samples(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    sample_dir = tmp_path / "docs" / "samples" / "unit"
    sample_dir.mkdir(parents=True)
    sample_file = sample_dir / "evidence_items.csv"
    sample_file.write_text("evidence_id\n1\n", encoding="utf-8")
    monkeypatch.setattr(dense_builder, "REPO_ROOT", tmp_path)

    with pytest.raises(ValueError, match="jsonl_only"):
        dense_builder.load_controlled_repo_sample_evidence_items("docs/samples/unit/evidence_items.csv")
