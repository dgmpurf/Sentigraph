from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.services.simulation.schemas import (
    SimulationStrategyComparisonSummary,
    SimulationStrategyReportRequest,
)
from app.services.simulation.simulation_engine import (
    create_brand_crisis_scenario,
    create_high_reach_negative_video_scenario,
    run_simulation,
)
from app.services.simulation.simulation_report_builder import build_simulation_strategy_report


client = TestClient(app)


REQUIRED_MARKDOWN_SECTIONS = [
    "# Simulation Lab Strategy Report",
    "## Scenario Overview",
    "## Intervention Comparison",
    "## Key Metrics",
    "## Audience Impact",
    "## Ethical Risk Review",
    "## Recommended Human Review Questions",
    "## Limitations",
]


def test_single_scenario_markdown_report_generated() -> None:
    result = run_simulation(create_brand_crisis_scenario(intervention_type="clarification"))
    response = build_simulation_strategy_report(
        SimulationStrategyReportRequest(
            simulation_mode="single",
            scenario_name=result.scenario_name,
            intervention_a="clarification",
            run_result=result,
        )
    )

    assert response.report.simulation_mode == "single"
    assert response.report.human_review_required is True
    assert all(section in response.markdown for section in REQUIRED_MARKDOWN_SECTIONS)
    assert "Intervention A: clarification" in response.markdown
    assert "Real API calls: no" in response.markdown
    assert "Real LLM calls: no" in response.markdown


def test_ab_comparison_markdown_report_generated() -> None:
    result_a = run_simulation(create_brand_crisis_scenario(intervention_type="no_response"))
    result_b = run_simulation(create_brand_crisis_scenario(intervention_type="apology"))
    response = build_simulation_strategy_report(
        SimulationStrategyReportRequest(
            simulation_mode="comparison",
            scenario_name="Synthetic brand crisis",
            intervention_a="no_response",
            intervention_b="apology",
            result_a=result_a,
            result_b=result_b,
        )
    )

    markdown = response.markdown
    assert response.report.simulation_mode == "comparison"
    assert "Intervention A: no_response" in markdown
    assert "Intervention B: apology" in markdown
    assert "Delta B-A" in markdown
    assert "human review required" in markdown.lower()


def test_ab_comparison_markdown_includes_supplied_backlash_and_attention_fields() -> None:
    result_a = run_simulation(create_brand_crisis_scenario(intervention_type="no_response"))
    result_b = run_simulation(create_brand_crisis_scenario(intervention_type="clarification"))
    response = build_simulation_strategy_report(
        SimulationStrategyReportRequest(
            simulation_mode="comparison",
            scenario_name="Synthetic brand crisis",
            intervention_a="no_response",
            intervention_b="clarification",
            result_a=result_a,
            result_b=result_b,
            comparison_summary=SimulationStrategyComparisonSummary(
                better_option="B",
                risk_a=42.0,
                risk_b=36.0,
                risk_delta=-6.0,
                negative_ratio_delta=-0.08,
                polarization_delta=-0.03,
                trust_recovery_delta=0.09,
                attention_level_delta=-0.02,
                backlash_risk_a=0.21,
                backlash_risk_b=0.12,
                backlash_risk_delta=-0.09,
                ethical_risk_notes=["No additional aggregate ethical risk flags were returned."],
            ),
        )
    )

    markdown = response.markdown
    assert "Backlash risk A: 21%" in markdown
    assert "Backlash risk B: 12%" in markdown
    assert "Backlash risk delta B-A: -9%" in markdown
    assert "| Delta B-A | -6.00 | -8% | -0.03 | +9% | -2% |" in markdown


def test_visibility_tradeoff_section_appears_when_data_exists() -> None:
    result_a = run_simulation(create_high_reach_negative_video_scenario(intervention_type="no_response"))
    result_b = run_simulation(
        create_high_reach_negative_video_scenario(intervention_type="content_removal_with_explanation")
    )
    response = build_simulation_strategy_report(
        SimulationStrategyReportRequest(
            simulation_mode="comparison",
            scenario_name="High reach negative video",
            intervention_a="no_response",
            intervention_b="content_removal_with_explanation",
            result_a=result_a,
            result_b=result_b,
        )
    )

    assert "## Visibility Intervention Tradeoff" in response.markdown
    assert "Exposure reduction" in response.markdown
    assert "Cross-platform spillover risk" in response.markdown
    assert "content_removal_with_explanation" in response.markdown


def test_markdown_report_avoids_raw_json_and_targeting_language() -> None:
    result = run_simulation(create_brand_crisis_scenario(intervention_type="third_party_evidence"))
    markdown = build_simulation_strategy_report(
        SimulationStrategyReportRequest(
            simulation_mode="single",
            intervention_a="third_party_evidence",
            run_result=result,
        )
    ).markdown.lower()

    unsafe_terms = [
        "{",
        "}",
        "api_key",
        "openai_api_key",
        ".env",
        "target_accounts",
        "author_id",
        "author_name",
        "influenceability_score",
        "fake_consensus",
        "bot_amplification",
        "targeted_persuasion",
        "covert manipulation",
        "harassment",
        "suppression tactics",
    ]
    assert all(term not in markdown for term in unsafe_terms)


def test_human_review_questions_are_present() -> None:
    result = run_simulation(create_brand_crisis_scenario(intervention_type="clarification"))
    markdown = build_simulation_strategy_report(
        SimulationStrategyReportRequest(
            simulation_mode="single",
            intervention_a="clarification",
            run_result=result,
        )
    ).markdown

    assert "Is the intervention lawful/platform-authorized?" in markdown
    assert "Is the explanation transparent?" in markdown
    assert "Does it risk cross-platform spillover?" in markdown
    assert "Is additional real-world evidence required?" in markdown


def test_simulation_report_endpoint_works() -> None:
    result = run_simulation(create_brand_crisis_scenario(intervention_type="clarification"))
    payload = SimulationStrategyReportRequest(
        simulation_mode="single",
        intervention_a="clarification",
        run_result=result,
    ).model_dump(mode="json")

    response = client.post("/api/v1/simulation/report/markdown", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["safe_mode"]["real_api_calls"] is False
    assert body["safe_mode"]["real_llm_calls"] is False
    assert "# Simulation Lab Strategy Report" in body["markdown"]


def test_simulation_report_endpoint_rejects_forbidden_intervention() -> None:
    result = run_simulation(create_brand_crisis_scenario(intervention_type="clarification"))
    payload = SimulationStrategyReportRequest(
        simulation_mode="single",
        intervention_a="fake_consensus",
        run_result=result,
    ).model_dump(mode="json")

    response = client.post("/api/v1/simulation/report/markdown", json=payload)

    assert response.status_code == 400
    body = response.json()["detail"]
    assert body["error"] == "simulation_report_intervention_rejected"
    assert body["aggregate_level_only"] is True


def test_old_simulation_endpoints_still_work() -> None:
    scenario_response = client.get("/api/v1/simulation/demo-scenario")
    policy_response = client.get("/api/v1/simulation/ethics-policy")

    assert scenario_response.status_code == 200
    assert policy_response.status_code == 200
    assert scenario_response.json()["agents"]
    assert policy_response.json()["aggregate_level_only"] is True
