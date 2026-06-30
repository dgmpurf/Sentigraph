from __future__ import annotations

import pytest

from app.api.v1.routes.internal_operator_review_only_staging import (
    _resolve_internal_operator_route_enabled_mode,
)


@pytest.mark.parametrize(
    "raw_env_value",
    [None, "", "false", "0", "unknown", "TRUE-ish", "enabled"],
)
def test_env_gate_helper_disables_default_falsey_and_unknown_values(
    raw_env_value: str | None,
) -> None:
    decision = _resolve_internal_operator_route_enabled_mode(raw_env_value)

    assert decision.enabled is False
    assert decision.mode == "disabled"
    assert decision.disabled_reason == "route_disabled"


@pytest.mark.parametrize("raw_env_value", ["1", "true", "yes"])
def test_env_gate_helper_enables_only_existing_normalized_values(raw_env_value: str) -> None:
    decision = _resolve_internal_operator_route_enabled_mode(raw_env_value)

    assert decision.enabled is True
    assert decision.mode == "synthetic_fixture_only"
    assert decision.disabled_reason is None


@pytest.mark.parametrize("raw_env_value", [" TRUE ", " Yes ", " 1 "])
def test_env_gate_helper_preserves_existing_strip_and_lower_normalization(
    raw_env_value: str,
) -> None:
    decision = _resolve_internal_operator_route_enabled_mode(raw_env_value)

    assert decision.enabled is True
    assert decision.mode == "synthetic_fixture_only"
    assert decision.disabled_reason is None
