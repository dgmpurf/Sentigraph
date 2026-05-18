from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.services.simulation.errors import SimulationEthicsError
from app.services.simulation.schemas import (
    SimulationEthicsPolicyResponse,
    SimulationRunResult,
    SimulationScenario,
)
from app.services.simulation.simulation_engine import (
    create_default_echo_chamber_scenario,
    ethics_policy_dict,
    run_simulation,
)


router = APIRouter()


@router.post("/run", response_model=SimulationRunResult)
def run_simulation_scenario(scenario: SimulationScenario) -> SimulationRunResult:
    """Run the deterministic, aggregate-level Simulation Lab MVP model."""

    try:
        return run_simulation(scenario)
    except SimulationEthicsError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "simulation_intervention_rejected",
                "message": str(exc),
                "blocked_categories": exc.blocked_categories,
                "intervention_type": exc.intervention_type,
                "aggregate_level_only": True,
            },
        ) from exc


@router.get("/demo-scenario", response_model=SimulationScenario)
def get_demo_scenario() -> SimulationScenario:
    """Return a deterministic synthetic demo scenario with no external data."""

    return create_default_echo_chamber_scenario()


@router.get("/ethics-policy", response_model=SimulationEthicsPolicyResponse)
def get_ethics_policy() -> SimulationEthicsPolicyResponse:
    """Return allowed and forbidden Simulation Lab intervention types."""

    return SimulationEthicsPolicyResponse.model_validate(ethics_policy_dict())
