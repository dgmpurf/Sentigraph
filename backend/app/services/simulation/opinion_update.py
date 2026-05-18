from __future__ import annotations

from app.services.simulation.attention_model import update_attention
from app.services.simulation.message_model import message_effect_for_agent
from app.services.simulation.network_builder import neighbors_for_agent
from app.services.simulation.schemas import (
    SimulationAgent,
    SimulationConfig,
    SimulationMessage,
    SimulationNetworkEdge,
)


def update_agents_for_step(
    agents: list[SimulationAgent],
    edges: list[SimulationNetworkEdge],
    messages: list[SimulationMessage],
    config: SimulationConfig,
) -> list[SimulationAgent]:
    agents_by_id = {agent.agent_id: agent for agent in agents}
    community_average = _community_expressed_average(agents)
    return [
        _update_agent(
            agent,
            agents_by_id,
            edges,
            messages,
            config,
            community_average.get(agent.community_id, agent.expressed_opinion),
        )
        for agent in agents
    ]


def _update_agent(
    agent: SimulationAgent,
    agents_by_id: dict[str, SimulationAgent],
    edges: list[SimulationNetworkEdge],
    messages: list[SimulationMessage],
    config: SimulationConfig,
    community_average: float,
) -> SimulationAgent:
    peer_average = _bounded_peer_average(agent, agents_by_id, edges)
    peer_delta = 0.0 if peer_average is None else peer_average - agent.latent_opinion
    raw_message_effect = message_effect_for_agent(agent, messages)
    attended_message_effect = raw_message_effect * agent.attention_budget

    social_component = agent.latent_opinion + config.peer_influence_weight * agent.conformity * peer_delta
    message_component = config.message_influence_weight * attended_message_effect
    prior_component = config.prior_persistence_weight * agent.stubbornness * agent.prior_anchor
    adaptive_component = (1.0 - config.prior_persistence_weight * agent.stubbornness) * (
        social_component + message_component
    )
    new_latent = _clamp_opinion(prior_component + adaptive_component)

    if abs(new_latent) >= agent.action_threshold:
        conformity_pull = agent.conformity * 0.08 * (community_average - agent.expressed_opinion)
        new_expressed = _clamp_opinion(agent.expressed_opinion * 0.62 + new_latent * 0.38 + conformity_pull)
    else:
        new_expressed = _clamp_opinion(agent.expressed_opinion * 0.88 + new_latent * 0.12)

    attention, fatigue, status = update_attention(
        agent,
        message_pressure=attended_message_effect,
        config=config,
    )
    return agent.model_copy(
        update={
            "latent_opinion": round(new_latent, 4),
            "expressed_opinion": round(new_expressed, 4),
            "attention_budget": round(attention, 4),
            "fatigue": round(fatigue, 4),
            "status": status,
        }
    )


def _bounded_peer_average(
    agent: SimulationAgent,
    agents_by_id: dict[str, SimulationAgent],
    edges: list[SimulationNetworkEdge],
) -> float | None:
    weighted_sum = 0.0
    total_weight = 0.0
    for neighbor, weight in neighbors_for_agent(agent, agents_by_id, edges):
        if abs(neighbor.latent_opinion - agent.latent_opinion) > agent.confidence_radius:
            continue
        weighted_sum += neighbor.latent_opinion * weight
        total_weight += weight
    if total_weight <= 0:
        return None
    return weighted_sum / total_weight


def _community_expressed_average(agents: list[SimulationAgent]) -> dict[str, float]:
    values: dict[str, list[float]] = {}
    for agent in agents:
        values.setdefault(agent.community_id, []).append(agent.expressed_opinion)
    return {
        community_id: sum(opinions) / len(opinions)
        for community_id, opinions in values.items()
        if opinions
    }


def _clamp_opinion(value: float) -> float:
    return min(1.0, max(-1.0, value))
