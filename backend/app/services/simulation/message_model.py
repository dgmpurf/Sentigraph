from __future__ import annotations

from app.services.simulation.schemas import SimulationAgent, SimulationIntervention, SimulationMessage


FRAMING_MULTIPLIERS = {
    "neutral": 1.0,
    "safety": 1.12,
    "accountability": 1.08,
    "clarifying": 0.92,
    "apology": 1.0,
    "compensation": 1.06,
    "faq": 0.78,
    "progress": 0.88,
    "third_party_evidence": 1.14,
    "misinformation_correction": 1.18,
    "no_response": 0.0,
}


def intervention_to_message(intervention: SimulationIntervention, step: int) -> SimulationMessage:
    intervention_type = intervention.intervention_type.strip().lower()
    stance_direction = intervention.stance_direction
    evidence_strength = intervention.evidence_strength
    source_credibility = intervention.source_credibility
    emotional_intensity = intervention.emotional_intensity
    framing = intervention.framing
    if intervention_type == "clarification":
        stance_direction = max(stance_direction, 0.28)
        framing = "clarifying"
    elif intervention_type == "apology":
        stance_direction = max(stance_direction, 0.34 + intervention.responsibility_acknowledgement * 0.16)
        framing = "apology"
    elif intervention_type == "compensation":
        stance_direction = max(stance_direction, 0.44)
        framing = "compensation"
    elif intervention_type == "faq":
        stance_direction = max(stance_direction, 0.2)
        framing = "faq"
    elif intervention_type == "progress_update":
        stance_direction = max(stance_direction, 0.26)
        framing = "progress"
    elif intervention_type == "third_party_evidence":
        stance_direction = max(stance_direction, 0.36)
        source_credibility = max(source_credibility, 0.86)
        framing = "third_party_evidence"
    elif intervention_type == "misinformation_correction":
        stance_direction = max(stance_direction, 0.42)
        evidence_strength = max(evidence_strength, 0.78)
        framing = "misinformation_correction"
    elif intervention_type == "no_response":
        stance_direction = 0.0
        evidence_strength = 0.0
        source_credibility = 0.0
        emotional_intensity = 0.0
        framing = "no_response"

    return SimulationMessage(
        message_id=f"{intervention.intervention_id}_message_step_{step}",
        topic=intervention.topic,
        source_type=intervention.source_type,
        source_credibility=source_credibility,
        stance_direction=stance_direction,
        emotional_intensity=emotional_intensity,
        evidence_strength=evidence_strength,
        framing=framing,
        novelty=max(0.15, 0.85 - step * 0.08) if intervention_type != "no_response" else 0.0,
        repetition=min(1.0, step * 0.08),
        platform_reach=0.62 * intervention.intensity,
    )


def message_effect_for_agent(agent: SimulationAgent, messages: list[SimulationMessage]) -> float:
    total = 0.0
    for message in messages:
        multiplier = FRAMING_MULTIPLIERS.get(message.framing, 1.0)
        evidence = 0.35 + message.evidence_strength * 0.65
        emotion = 0.45 + message.emotional_intensity * 0.55
        reach = 0.35 + message.platform_reach * 0.65
        novelty = 0.6 + message.novelty * 0.4 - message.repetition * 0.12
        raw_effect = (
            message.stance_direction
            * message.source_credibility
            * evidence
            * emotion
            * reach
            * novelty
            * multiplier
        )

        if raw_effect < 0:
            raw_effect *= max(0.25, agent.negativity_weight)
        elif raw_effect > 0:
            raw_effect *= 0.55 + agent.authority_trust * 0.45
            raw_effect *= max(0.25, 1.0 - agent.reactance * 0.35)

        if raw_effect * agent.latent_opinion < 0:
            raw_effect *= max(0.2, 1.0 - agent.confirmation_bias * 0.55)
        total += raw_effect
    return total
