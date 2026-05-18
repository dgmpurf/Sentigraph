from __future__ import annotations

from app.services.simulation.schemas import SimulationAgent, SimulationNetworkEdge


def build_homophilous_network(agents: list[SimulationAgent]) -> list[SimulationNetworkEdge]:
    edges: list[SimulationNetworkEdge] = []
    for source in agents:
        for target in agents:
            if source.agent_id == target.agent_id:
                continue
            same_community = source.community_id == target.community_id
            opinion_distance = abs(source.latent_opinion - target.latent_opinion)
            if same_community:
                weight = max(0.22, 0.82 - opinion_distance * 0.25)
                bridge_score = 0.08
            elif opinion_distance <= 0.55:
                weight = max(0.08, 0.28 - opinion_distance * 0.18)
                bridge_score = 0.55
            else:
                continue
            edges.append(
                SimulationNetworkEdge(
                    source_agent_id=source.agent_id,
                    target_agent_id=target.agent_id,
                    weight=round(weight, 4),
                    bridge_score=bridge_score,
                    relationship_type="same_community" if same_community else "bridge",
                )
            )
    return edges


def neighbors_for_agent(
    agent: SimulationAgent,
    agents_by_id: dict[str, SimulationAgent],
    edges: list[SimulationNetworkEdge],
) -> list[tuple[SimulationAgent, float]]:
    neighbors: list[tuple[SimulationAgent, float]] = []
    for edge in edges:
        if edge.target_agent_id != agent.agent_id:
            continue
        neighbor = agents_by_id.get(edge.source_agent_id)
        if neighbor is not None:
            neighbors.append((neighbor, edge.weight))
    return neighbors
