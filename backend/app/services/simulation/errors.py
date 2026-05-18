from __future__ import annotations


class SimulationEthicsError(ValueError):
    """Raised when a simulation request violates the ethics policy."""

    def __init__(
        self,
        message: str,
        *,
        blocked_categories: list[str] | None = None,
        intervention_type: str | None = None,
    ) -> None:
        super().__init__(message)
        self.blocked_categories = blocked_categories or []
        self.intervention_type = intervention_type
