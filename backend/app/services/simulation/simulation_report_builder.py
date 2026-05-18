from __future__ import annotations

from datetime import datetime, timezone

from app.services.simulation.errors import SimulationEthicsError
from app.services.simulation.schemas import (
    SimulationMetricSummary,
    SimulationRunResult,
    SimulationStrategyComparisonSummary,
    SimulationStrategyReport,
    SimulationStrategyReportRequest,
    SimulationStrategyReportResponse,
    VisibilityInterventionResult,
)
from app.services.simulation.intervention_library import FORBIDDEN_INTERVENTION_TYPES


HUMAN_REVIEW_QUESTIONS = [
    "Is the intervention lawful/platform-authorized?",
    "Is the explanation transparent?",
    "Does the strategy increase neutral-audience backlash?",
    "Does it risk cross-platform spillover?",
    "Are the findings based on aggregate simulation only?",
    "Is additional real-world evidence required?",
]

LIMITATIONS = [
    "This is a deterministic scenario simulation.",
    "It is not a guarantee of real-world outcomes.",
    "It is for aggregate crisis-response comparison only.",
    "Real-world actions require human review and policy/legal review.",
]


def build_simulation_strategy_report(
    request: SimulationStrategyReportRequest,
) -> SimulationStrategyReportResponse:
    """Build a safe Markdown report from existing aggregate simulation results."""

    _validate_report_request(request)
    generated_at = datetime.now(timezone.utc)
    scenario_name = _scenario_name(request)
    intervention_a = _intervention_a(request)
    intervention_b = request.intervention_b if request.simulation_mode == "comparison" else None
    ethical_flags = _collect_ethical_flags(request)
    summary = _summary_sentence(request)
    report = SimulationStrategyReport(
        generated_at=generated_at,
        scenario_name=scenario_name,
        simulation_mode=request.simulation_mode,
        intervention_a=intervention_a,
        intervention_b=intervention_b,
        summary=summary,
        ethical_risk_flags=ethical_flags,
        limitations=LIMITATIONS,
    )
    markdown = _build_markdown(report, request)
    return SimulationStrategyReportResponse(report=report, markdown=markdown)


def _validate_report_request(request: SimulationStrategyReportRequest) -> None:
    intervention_values = [
        value.strip().lower()
        for value in (request.intervention_a, request.intervention_b)
        if isinstance(value, str) and value.strip()
    ]
    blocked = sorted({value for value in intervention_values if value in FORBIDDEN_INTERVENTION_TYPES})
    if blocked:
        raise SimulationEthicsError(
            "Simulation strategy report rejected a forbidden intervention type.",
            blocked_categories=blocked,
            intervention_type=", ".join(blocked),
        )
    if request.simulation_mode == "single":
        if request.run_result is None:
            raise ValueError("single scenario report requires run_result")
    elif request.simulation_mode == "comparison":
        if request.result_a is None or request.result_b is None:
            raise ValueError("A/B comparison report requires result_a and result_b")
        if not request.intervention_a or not request.intervention_b:
            raise ValueError("A/B comparison report requires intervention_a and intervention_b")
    else:
        raise ValueError("unsupported simulation report mode")


def _scenario_name(request: SimulationStrategyReportRequest) -> str:
    if request.scenario_name:
        return _safe_inline(request.scenario_name)
    if request.run_result:
        return _safe_inline(request.run_result.scenario_name)
    if request.result_a:
        return _safe_inline(request.result_a.scenario_name)
    return "Simulation Scenario"


def _intervention_a(request: SimulationStrategyReportRequest) -> str:
    if request.intervention_a:
        return _safe_inline(request.intervention_a)
    if request.run_result:
        return _active_intervention(request.run_result)
    return "not_available"


def _summary_sentence(request: SimulationStrategyReportRequest) -> str:
    if request.simulation_mode == "single":
        risk = _risk_proxy(request.run_result.final_metrics if request.run_result else None)
        return (
            "Single-scenario deterministic simulation completed with final aggregate "
            f"risk proxy {risk:.1f}/100."
        )
    summary = request.comparison_summary or _derive_comparison_summary(
        request.result_a,
        request.result_b,
    )
    better = summary.better_option if summary else "inconclusive"
    return (
        "A/B deterministic comparison completed. "
        f"Lower aggregate risk option: {better}. Human review is required before any real-world action."
    )


def _collect_ethical_flags(request: SimulationStrategyReportRequest) -> list[str]:
    flags: list[str] = []
    results = [result for result in (request.run_result, request.result_a, request.result_b) if result is not None]
    for result in results:
        flags.extend(result.final_metrics.ethical_risk_flags)
        if result.visibility_intervention_result:
            flags.extend(result.visibility_intervention_result.warnings)
    if request.comparison_summary:
        flags.extend(request.comparison_summary.ethical_risk_notes)
    return _unique_safe_lines(flags) or ["No additional aggregate ethical risk flags were returned."]


def _build_markdown(report: SimulationStrategyReport, request: SimulationStrategyReportRequest) -> str:
    lines: list[str] = [
        "# Simulation Lab Strategy Report",
        "",
        f"- Generated at: {_format_datetime(report.generated_at)}",
        f"- Scenario: {report.scenario_name}",
        f"- Simulation mode: {report.simulation_mode}",
        "- Safety posture: aggregate crisis-response comparison only; human review required.",
        "",
        "## Scenario Overview",
        "",
        report.summary,
        "",
    ]
    if request.simulation_mode == "comparison":
        lines.extend(_comparison_sections(request))
    else:
        lines.extend(_single_sections(request))
    lines.extend(
        [
            "## Ethical Risk Review",
            "",
            "- Human review required: yes",
            "- Real API calls: no",
            "- Real LLM calls: no",
            "- Live public fetching: no",
            "- Automatic real-world execution: no",
        ]
    )
    for flag in report.ethical_risk_flags:
        lines.append(f"- Aggregate risk note: {_safe_line(flag)}")
    lines.extend(["", "## Recommended Human Review Questions", ""])
    lines.extend(f"- {question}" for question in HUMAN_REVIEW_QUESTIONS)
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in report.limitations)
    lines.append("")
    return "\n".join(lines)


def _single_sections(request: SimulationStrategyReportRequest) -> list[str]:
    result = request.run_result
    metrics = result.final_metrics if result else None
    visibility = result.visibility_intervention_result if result else None
    lines = [
        "## Intervention Comparison",
        "",
        f"- Intervention A: {_safe_inline(_intervention_a(request))}",
        "- Comparison mode: single scenario; no B option was supplied.",
        "",
        "## Key Metrics",
        "",
        _metric_table_header(),
        _metric_table_row("Final", metrics, _risk_proxy(metrics)),
        "",
        "## Audience Impact",
        "",
        _audience_impact(metrics),
        "",
    ]
    lines.extend(_visibility_section(visibility))
    return lines


def _comparison_sections(request: SimulationStrategyReportRequest) -> list[str]:
    result_a = request.result_a
    result_b = request.result_b
    metrics_a = result_a.final_metrics if result_a else None
    metrics_b = result_b.final_metrics if result_b else None
    summary = request.comparison_summary or _derive_comparison_summary(result_a, result_b)
    lines = [
        "## Intervention Comparison",
        "",
        f"- Intervention A: {_safe_inline(request.intervention_a)}",
        f"- Intervention B: {_safe_inline(request.intervention_b)}",
        f"- Lower aggregate risk option: {_safe_inline(summary.better_option)}",
        "- Recommendation: human review required; do not auto-execute strategy.",
        "",
        "## Key Metrics",
        "",
        _metric_table_header(),
        _metric_table_row("A", metrics_a, summary.risk_a),
        _metric_table_row("B", metrics_b, summary.risk_b),
        _delta_table(summary),
        *_backlash_summary_lines(summary),
        "",
        "## Audience Impact",
        "",
        _audience_impact(metrics_a, "A"),
        _audience_impact(metrics_b, "B"),
        "",
    ]
    lines.extend(_visibility_section(result_a.visibility_intervention_result if result_a else None, "A"))
    lines.extend(_visibility_section(result_b.visibility_intervention_result if result_b else None, "B"))
    return lines


def _metric_table_header() -> str:
    return (
        "| Option | Risk proxy | Negative ratio | Polarization | Trust recovery | Attention level |\n"
        "| --- | ---: | ---: | ---: | ---: | ---: |"
    )


def _metric_table_row(label: str, metrics: SimulationMetricSummary | None, risk: float | None) -> str:
    if metrics is None:
        return f"| {label} | n/a | n/a | n/a | n/a | n/a |"
    return (
        f"| {label} | {_number(risk)}/100 | {_percent(metrics.negative_ratio)} | "
        f"{_number(metrics.polarization_index)} | {_percent(metrics.trust_recovery_proxy)} | "
        f"{_percent(metrics.attention_level)} |"
    )


def _delta_table(summary: SimulationStrategyComparisonSummary) -> str:
    return (
        "| Delta B-A | "
        f"{_signed(summary.risk_delta)} | "
        f"{_signed_percent(summary.negative_ratio_delta)} | "
        f"{_signed(summary.polarization_delta)} | "
        f"{_signed_percent(summary.trust_recovery_delta)} | "
        f"{_signed_percent(summary.attention_level_delta)} |"
    )


def _backlash_summary_lines(summary: SimulationStrategyComparisonSummary) -> list[str]:
    if (
        summary.backlash_risk_a is None
        and summary.backlash_risk_b is None
        and summary.backlash_risk_delta is None
    ):
        return []
    return [
        "",
        f"- Backlash risk A: {_percent(summary.backlash_risk_a)}",
        f"- Backlash risk B: {_percent(summary.backlash_risk_b)}",
        f"- Backlash risk delta B-A: {_signed_percent(summary.backlash_risk_delta)}",
    ]


def _audience_impact(metrics: SimulationMetricSummary | None, label: str = "Final") -> str:
    if metrics is None:
        return f"- {label}: no aggregate metrics available."
    if metrics.negative_ratio >= 0.55:
        direction = "negative audience share remains elevated."
    elif metrics.trust_recovery_proxy >= 0.58:
        direction = "trust recovery proxy is comparatively stronger."
    else:
        direction = "audience impact is mixed and should be reviewed with context."
    return (
        f"- {label}: {direction} Positive share {_percent(metrics.positive_ratio)}, "
        f"neutral share {_percent(metrics.neutral_ratio)}, negative share {_percent(metrics.negative_ratio)}."
    )


def _visibility_section(
    visibility: VisibilityInterventionResult | None,
    label: str | None = None,
) -> list[str]:
    if visibility is None:
        return []
    prefix = f"{label} " if label else ""
    return [
        "## Visibility Intervention Tradeoff",
        "",
        f"- {prefix}Intervention type: {_safe_inline(visibility.intervention_type)}",
        f"- Exposure reduction: {_number(visibility.exposure_reduction)}/100",
        f"- Backlash risk: {_number(visibility.backlash_cost)}/100",
        f"- Trust loss: {_number(visibility.trust_loss)}/100",
        f"- Cross-platform spillover risk: {_number(visibility.spillover_risk)}/100",
        f"- Neutral audience impact: {_number(visibility.neutral_audience_impact)}/100",
        f"- Opposition group impact: {_number(visibility.opposition_group_impact)}/100",
        f"- Net risk change: {_number(visibility.net_risk_change)}/100",
        f"- Removal legitimacy score: {_number(visibility.removal_legitimacy_score)}/100",
        f"- Recommendation: {_safe_inline(visibility.recommendation)}",
        f"- Explanation: {_safe_line(visibility.explanation)}",
        "",
    ]


def _derive_comparison_summary(
    result_a: SimulationRunResult | None,
    result_b: SimulationRunResult | None,
) -> SimulationStrategyComparisonSummary:
    metrics_a = result_a.final_metrics if result_a else None
    metrics_b = result_b.final_metrics if result_b else None
    risk_a = _risk_proxy(metrics_a)
    risk_b = _risk_proxy(metrics_b)
    risk_delta = None if risk_a is None or risk_b is None else risk_b - risk_a
    better = "inconclusive"
    if risk_delta is not None:
        if abs(risk_delta) < 0.5:
            better = "tie"
        else:
            better = "B" if risk_delta < 0 else "A"
    return SimulationStrategyComparisonSummary(
        better_option=better,
        risk_a=risk_a,
        risk_b=risk_b,
        risk_delta=risk_delta,
        negative_ratio_delta=_metric_delta(metrics_a, metrics_b, "negative_ratio"),
        polarization_delta=_metric_delta(metrics_a, metrics_b, "polarization_index"),
        trust_recovery_delta=_metric_delta(metrics_a, metrics_b, "trust_recovery_proxy"),
        attention_level_delta=_metric_delta(metrics_a, metrics_b, "attention_level"),
        ethical_risk_notes=["No additional aggregate ethical risk flags were returned."],
    )


def _risk_proxy(metrics: SimulationMetricSummary | None) -> float | None:
    if metrics is None:
        return None
    score = (
        metrics.negative_ratio * 52
        + metrics.polarization_index * 28
        + metrics.attention_level * 12
        - metrics.trust_recovery_proxy * 14
    )
    return _clamp(score, 0.0, 100.0)


def _metric_delta(
    metrics_a: SimulationMetricSummary | None,
    metrics_b: SimulationMetricSummary | None,
    field: str,
) -> float | None:
    if metrics_a is None or metrics_b is None:
        return None
    return getattr(metrics_b, field) - getattr(metrics_a, field)


def _active_intervention(result: SimulationRunResult) -> str:
    if result.step_results:
        return _safe_inline(result.step_results[0].active_intervention_type)
    return "not_available"


def _format_datetime(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _number(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.2f}"


def _signed(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:+.2f}"


def _percent(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.0f}%"


def _signed_percent(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:+.0f}%"


def _safe_inline(value: object) -> str:
    text = str(value or "not_available")
    return _safe_line(text).replace("|", "/")


def _safe_line(value: object) -> str:
    text = str(value or "").replace("\r", " ").replace("\n", " ").strip()
    text = text.replace("{", "(").replace("}", ")")
    return text[:500] if text else "not_available"


def _unique_safe_lines(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        safe_value = _safe_line(value)
        if safe_value and safe_value not in seen:
            seen.add(safe_value)
            result.append(safe_value)
    return result


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return min(maximum, max(minimum, value))
