from __future__ import annotations

from statistics import mean

from app.services.simulation.schemas import SimulationAgent, SimulationMetricSummary


def calculate_metrics(
    agents: list[SimulationAgent],
    *,
    baseline: SimulationMetricSummary | None = None,
    ethical_flags: list[str] | None = None,
) -> SimulationMetricSummary:
    if not agents:
        return SimulationMetricSummary(
            average_latent_opinion=0.0,
            average_expressed_opinion=0.0,
            negative_ratio=0.0,
            neutral_ratio=1.0,
            positive_ratio=0.0,
            polarization_index=0.0,
            attention_level=0.0,
            trust_recovery_proxy=0.0,
            intervention_effect_score=0.0,
            false_belief_proxy=0.0,
            min_latent_opinion=0.0,
            max_latent_opinion=0.0,
            min_expressed_opinion=0.0,
            max_expressed_opinion=0.0,
            ethical_risk_flags=ethical_flags or [],
        )

    latent = [agent.latent_opinion for agent in agents]
    expressed = [agent.expressed_opinion for agent in agents]
    avg_latent = mean(latent)
    avg_expressed = mean(expressed)
    negative_ratio = sum(1 for value in expressed if value < -0.15) / len(expressed)
    positive_ratio = sum(1 for value in expressed if value > 0.15) / len(expressed)
    neutral_ratio = max(0.0, 1.0 - negative_ratio - positive_ratio)
    polarization_index = min(1.0, mean(abs(value - avg_expressed) for value in expressed))
    attention_level = mean(agent.attention_budget for agent in agents)

    if baseline is None:
        trust_recovery_proxy = _clamp01((avg_latent + 1.0) / 2.0)
        intervention_effect_score = 0.0
    else:
        latent_improvement = avg_latent - baseline.average_latent_opinion
        negative_reduction = baseline.negative_ratio - negative_ratio
        trust_recovery_proxy = _clamp01(0.5 + latent_improvement / 2.0)
        intervention_effect_score = _clamp_score(negative_reduction * 72.0 + max(0.0, latent_improvement) * 42.0)

    false_belief_proxy = _clamp01(max(0.0, -avg_latent) * (0.55 + attention_level * 0.45))
    return SimulationMetricSummary(
        average_latent_opinion=round(avg_latent, 4),
        average_expressed_opinion=round(avg_expressed, 4),
        negative_ratio=round(negative_ratio, 4),
        neutral_ratio=round(neutral_ratio, 4),
        positive_ratio=round(positive_ratio, 4),
        polarization_index=round(polarization_index, 4),
        attention_level=round(attention_level, 4),
        trust_recovery_proxy=round(trust_recovery_proxy, 4),
        intervention_effect_score=round(intervention_effect_score, 4),
        false_belief_proxy=round(false_belief_proxy, 4),
        min_latent_opinion=round(min(latent), 4),
        max_latent_opinion=round(max(latent), 4),
        min_expressed_opinion=round(min(expressed), 4),
        max_expressed_opinion=round(max(expressed), 4),
        ethical_risk_flags=ethical_flags or [],
    )


def calculate_community_metrics(
    agents: list[SimulationAgent],
    *,
    baseline: SimulationMetricSummary | None = None,
    ethical_flags: list[str] | None = None,
) -> dict[str, SimulationMetricSummary]:
    communities: dict[str, list[SimulationAgent]] = {}
    for agent in agents:
        communities.setdefault(agent.community_id, []).append(agent)
    return {
        community_id: calculate_metrics(community_agents, baseline=baseline, ethical_flags=ethical_flags)
        for community_id, community_agents in sorted(communities.items())
    }


def _clamp01(value: float) -> float:
    return min(1.0, max(0.0, value))


def _clamp_score(value: float) -> float:
    return min(100.0, max(0.0, value))
