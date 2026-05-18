from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.case_repository import CaseRepository
from app.schemas.analysis import SentimentSummary
from app.schemas.case import AnalysisCaseDetail
from app.services.case_store import configure_case_repository, reset_case_store
from app.services.simulation.case_initializer import (
    CaseAnalysisRequiredError,
    build_case_simulation_initialization,
)
from app.services.simulation.simulation_engine import run_simulation
from app.services.storage.local_json_store import LocalJsonCaseStore


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_cases(case_store_path) -> None:
    configure_case_repository(CaseRepository(LocalJsonCaseStore(case_store_path)))
    reset_case_store()


@pytest.fixture
def case_store_path(tmp_path):
    return tmp_path / "cases.json"


def test_initialized_scenario_from_completed_case() -> None:
    case = _completed_case()

    result = build_case_simulation_initialization(case)

    assert result.status in {"initialized", "partial"}
    assert result.event_frame.case_id == case.case_id
    assert result.event_frame.sub_issues
    assert result.audience_segments
    assert result.persona_clusters
    assert result.simulation_scenario.agents
    assert result.simulation_scenario.metadata["aggregate_only"] is True
    assert result.safe_mode["individual_targeting"] is False


def test_case_without_analysis_returns_case_analysis_required() -> None:
    response = client.post(
        "/api/v1/cases",
        json={"keyword": "Demo", "platforms": ["reddit"], "title": "Draft case"},
    )
    assert response.status_code == 200
    case_id = response.json()["case_id"]

    api_response = client.post(f"/api/v1/cases/{case_id}/simulation/initialize")

    assert api_response.status_code == 400
    assert api_response.json()["detail"]["error"] == "case_analysis_required"

    with pytest.raises(CaseAnalysisRequiredError):
        build_case_simulation_initialization(AnalysisCaseDetail.model_validate(response.json()))


def test_missing_sentiment_distribution_falls_back_safely() -> None:
    case = _completed_case()
    assert case.analysis_result is not None
    patched_analysis = case.analysis_result.model_copy(update={"sentiment": None})
    patched_case = case.model_copy(update={"analysis_result": patched_analysis})

    result = build_case_simulation_initialization(patched_case)

    assert "missing_sentiment_distribution_used_safe_default" in result.warnings
    assert result.audience_segments
    observed = result.event_frame.observed_frame_profile
    assert observed.sentiment_distribution["negative"] == 0.45


def test_topic_risks_become_sub_issues() -> None:
    case = _completed_case()

    result = build_case_simulation_initialization(case)

    analysis_topics = {topic.topic for topic in case.analysis_result.topic_risks}  # type: ignore[union-attr]
    sub_issue_titles = {issue.title for issue in result.event_frame.sub_issues}
    assert analysis_topics & sub_issue_titles
    assert all(0 <= issue.topic_risk_score <= 100 for issue in result.event_frame.sub_issues)
    assert all(issue.risk_score == issue.topic_risk_score for issue in result.event_frame.sub_issues)


def test_sentiment_distribution_becomes_audience_segments() -> None:
    case = _completed_case()

    result = build_case_simulation_initialization(case)

    segment_ids = {segment.segment_id for segment in result.audience_segments}
    assert {"core_opposition", "mild_opposition", "neutral_observers", "supporters"}.issubset(segment_ids)
    assert 0.98 <= sum(segment.proportion for segment in result.audience_segments) <= 1.02


def test_manipulation_risk_creates_warnings() -> None:
    case = _completed_case()
    assert case.analysis_result is not None
    patched_case = case.model_copy(
        update={"analysis_result": case.analysis_result.model_copy(update={"manipulation_risk": 88.0})}
    )

    result = build_case_simulation_initialization(patched_case)

    assert "aggregate_repeated_script_or_manipulation_signal_detected" in result.warnings
    assert result.frame_gap_analysis.primary_classification == "manipulation_suspected_frame"


def test_real_crisis_risk_maps_to_aggregate_frame_factors() -> None:
    case = _completed_case()
    assert case.analysis_result is not None
    patched_case = case.model_copy(
        update={"analysis_result": case.analysis_result.model_copy(update={"real_crisis_risk": 86.0})}
    )

    result = build_case_simulation_initialization(patched_case)
    observed = result.event_frame.observed_frame_profile

    assert observed.harm_salience >= 0.8
    assert observed.loss_sensitivity >= 0.7
    assert observed.moral_outrage_sensitivity >= 0.68
    assert observed.crisis_legitimacy_pressure >= 0.75
    assert all(cluster.no_individual_profile for cluster in result.persona_clusters)
    assert all(cluster.harm_salience >= 0.8 for cluster in result.persona_clusters)


def test_frame_gap_classification_more_negative_than_public() -> None:
    case = _completed_case()
    assert case.analysis_result is not None
    patched_analysis = case.analysis_result.model_copy(
        update={
            "sentiment": SentimentSummary(
                positive_ratio=0.04,
                neutral_ratio=0.16,
                negative_ratio=0.80,
                average_sentiment_score=-0.74,
            ),
            "manipulation_risk": 12.0,
        }
    )
    patched_case = case.model_copy(update={"analysis_result": patched_analysis})

    result = build_case_simulation_initialization(patched_case)

    assert result.frame_gap_analysis.primary_classification == "frame_more_negative_than_public"


def test_frame_gap_classification_more_positive_than_public() -> None:
    case = _completed_case()
    assert case.analysis_result is not None
    patched_analysis = case.analysis_result.model_copy(
        update={
            "sentiment": SentimentSummary(
                positive_ratio=0.78,
                neutral_ratio=0.18,
                negative_ratio=0.04,
                average_sentiment_score=0.72,
            ),
            "manipulation_risk": 12.0,
        }
    )
    patched_case = case.model_copy(update={"analysis_result": patched_analysis})

    result = build_case_simulation_initialization(patched_case)

    assert result.frame_gap_analysis.primary_classification == "frame_more_positive_than_public"


def test_frame_gap_classification_polarized_frame() -> None:
    case = _completed_case()
    assert case.analysis_result is not None
    patched_analysis = case.analysis_result.model_copy(
        update={
            "sentiment": SentimentSummary(
                positive_ratio=0.30,
                neutral_ratio=0.24,
                negative_ratio=0.46,
                average_sentiment_score=-0.14,
            ),
            "manipulation_risk": 12.0,
        }
    )
    patched_case = case.model_copy(update={"analysis_result": patched_analysis})

    result = build_case_simulation_initialization(patched_case)

    assert result.frame_gap_analysis.primary_classification == "polarized_frame"


def test_frame_gap_classification_insufficient_data() -> None:
    case = _completed_case()
    assert case.analysis_result is not None
    patched_analysis = case.analysis_result.model_copy(
        update={
            "topic_risks": [
                topic.model_copy(update={"comment_count": 0})
                for topic in case.analysis_result.topic_risks
            ],
            "topics": [
                topic.model_copy(update={"comment_count": 0})
                for topic in case.analysis_result.topics
            ],
            "manipulation_risk": 12.0,
        }
    )
    patched_case = case.model_copy(update={"analysis_result": patched_analysis})

    result = build_case_simulation_initialization(patched_case)

    assert result.frame_gap_analysis.primary_classification == "insufficient_data"
    assert "insufficient_observed_comment_count" in result.warnings


def test_initializer_output_has_no_named_user_targeting() -> None:
    result = build_case_simulation_initialization(_completed_case())
    payload = result.model_dump_json()

    assert "target_accounts" not in payload
    assert "author_id" not in payload
    assert "author_name" not in payload
    assert "influenceability_score" not in payload
    assert "targeted_persuasion" not in payload
    assert "covert_suppression" not in payload
    assert "fake_consensus" not in payload
    assert "bot_amplification" not in payload
    assert all(agent.agent_id.startswith("synthetic_") for agent in result.simulation_scenario.agents)


def test_generated_scenario_is_accepted_by_simulation_engine() -> None:
    result = build_case_simulation_initialization(_completed_case())

    simulation_result = run_simulation(result.simulation_scenario)

    assert simulation_result.simulation_status == "completed"
    assert simulation_result.safe_mode["aggregate_level_only"] is True


def test_case_simulation_endpoints_work_for_completed_case() -> None:
    case = _completed_case()

    preview = client.get(f"/api/v1/cases/{case.case_id}/simulation/initialization-preview")
    initialize = client.post(f"/api/v1/cases/{case.case_id}/simulation/initialize")

    assert preview.status_code == 200
    assert initialize.status_code == 200
    body = initialize.json()
    assert body["case_id"] == case.case_id
    assert body["event_frame"]["data_safety"]["aggregate_only"] is True
    assert body["simulation_scenario"]["metadata"]["no_individual_targeting"] is True


def _completed_case() -> AnalysisCaseDetail:
    create_response = client.post(
        "/api/v1/cases",
        json={
            "keyword": "Acme battery safety",
            "platforms": ["reddit", "weibo", "bilibili"],
            "title": "Acme battery safety case",
        },
    )
    assert create_response.status_code == 200
    case_id = create_response.json()["case_id"]
    run_response = client.post(f"/api/v1/cases/{case_id}/run")
    assert run_response.status_code == 200
    return AnalysisCaseDetail.model_validate(run_response.json())
