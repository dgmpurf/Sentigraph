from __future__ import annotations

from app.services.simulation.schemas import SimulationAgent, SimulationConfig


def update_attention(
    agent: SimulationAgent,
    *,
    message_pressure: float,
    config: SimulationConfig,
) -> tuple[float, float, str]:
    pressure = min(1.0, abs(message_pressure))
    new_fatigue = _clamp01(agent.fatigue + config.fatigue_increase * (0.45 + pressure))
    replenishment = pressure * 0.12
    fatigue_drag = new_fatigue * 0.045
    new_attention = _clamp01(agent.attention_budget * (1.0 - config.attention_decay) + replenishment - fatigue_drag)
    status = "fatigued" if new_fatigue >= 0.85 or new_attention <= 0.08 else agent.status
    if new_attention <= 0.02:
        status = "inactive"
    return new_attention, new_fatigue, status


def _clamp01(value: float) -> float:
    return min(1.0, max(0.0, value))
