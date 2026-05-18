# Simulation Lab Validation Plan

Status: validation design plus MVP backend QA checklist. The deterministic backend scaffold is implemented; frontend visualization, empirical calibration, and historical replay remain future work.

Simulation Lab should not be exposed as a decision aid until validation, uncertainty labels, and abuse-resistance checks are in place.

## Validation Goals

The validation plan should establish that the simulator:

- Behaves consistently on simple benchmark cases.
- Produces explainable aggregate metrics.
- Does not overstate certainty.
- Separates estimated and assumed parameters.
- Blocks forbidden manipulation tactics.
- Remains offline and deterministic in MVP mode.
- Can be docked against simpler models.

## ODD Documentation

Every implemented simulator version should have ODD-style documentation:

- Purpose.
- Entities, state variables, and scales.
- Process overview and schedule.
- Design concepts.
- Initialization.
- Inputs.
- Submodels.
- Output metrics.

Decision-related extensions should document:

- Agent decision rules.
- Threshold logic.
- Attention update rules.
- Intervention package effects.
- Assumptions behind source credibility, framing, and fatigue.

ODD documentation should be versioned with the simulator.

## Docking Against Simpler Models

Docking tests compare a richer model against simpler known baselines.

Required MVP docking:

- DeGroot baseline: when `stubbornness=0` and all neighbors are accepted, Friedkin-Johnsen should approach DeGroot-like averaging.
- Friedkin-Johnsen persistence: higher `stubbornness` should preserve initial opinion more strongly.
- Bounded-confidence fragmentation: lower `confidence_radius` should produce more persistent clusters.
- Threshold expression: higher `action_threshold` should reduce public expression.
- Attention decay: without shocks, attention should decline over time.

Docking should be part of offline benchmarks before UI exposure.

## Historical Replay Validation

Historical replay is later-stage work. It should not be part of the MVP unless there is a safe, reviewed, aggregate, and privacy-preserving dataset.

When available, replay should:

- Use time-ordered monitoring snapshots.
- Compare simulated aggregate risk movement to observed aggregate risk movement.
- Avoid account-level matching.
- Report calibration error and uncertainty.
- Keep all raw personal data out of benchmark output.

## Sensitivity Analysis

Sensitivity tests should vary key assumptions:

- Stubbornness.
- Confidence radius.
- Source credibility.
- Evidence strength.
- Attention decay.
- Fatigue.
- Action threshold.
- Cross-cutting exposure rate.
- Homophily.
- Intervention timing.

The UI should surface high-sensitivity parameters as caveats. If an outcome changes direction under small parameter shifts, the scenario should be labeled unstable.

## Ablation Tests

Ablation tests should remove one module at a time:

- No bounded-confidence gate.
- No attention decay.
- No source-credibility weighting.
- No framing effect.
- No threshold expression.
- No cross-cutting exposure.
- No fatigue.

Expected result: ablations should alter interpretable metrics in predictable ways. If not, the model may be too complex or poorly wired.

## Uncertainty Labels

Every simulation result should include an uncertainty label:

- `low`: strong benchmark coverage and stable sensitivity.
- `medium`: reasonable benchmark coverage but assumptions still matter.
- `high`: limited data or sensitive parameters.
- `insufficient_data`: not enough input history or too many assumptions.

MVP should usually default to `medium` or `high`; it should not imply prediction certainty.

## Assumption Logging

Every run should log:

- Model version.
- Scenario name.
- Intervention package.
- Estimated parameters.
- Assumed parameters.
- Synthetic fixture version.
- Random seed, if any.
- Disabled modules.
- Warnings.
- Ethical guardrail checks.

Logs must not include:

- API keys.
- `.env` values.
- Raw private user data.
- Real account identifiers.
- Raw prompts or LLM request bodies.

## Estimated Versus Assumed Parameters

The simulator should separate:

- Estimated parameters: derived from monitoring snapshots or validated aggregate datasets.
- Assumed parameters: default values, user scenario values, or synthetic fixture values.
- Unknown parameters: values that cannot be inferred safely.

Reports should never present assumed parameters as measured facts.

## Benchmark Integration

Offline benchmark suites should be added before the first implementation is considered complete:

- `simulation_fj_docking`
- `simulation_bounded_confidence`
- `simulation_threshold_expression`
- `simulation_attention_decay`
- `simulation_intervention_comparison`
- `simulation_ethics_guardrails`

Each suite should report:

- `case_count`
- `passed`
- `failed`
- `warnings`
- deterministic duration
- safe summary only

Benchmark output must stay summary-only and must not expose raw private content.

Current MVP benchmark coverage is consolidated under the `simulation_lab` offline suite. It covers:

- no-response baseline
- clarification comparison
- apology comparison
- misinformation-correction comparison
- forbidden intervention rejection

The focused backend tests additionally cover:

- deterministic output with and without an explicit seed
- Friedkin-Johnsen prior persistence
- bounded-confidence peer influence
- source credibility effects
- framing effects
- threshold-based expression updates
- attention decay and fatigue bounds
- aggregate-only run result shape
- safe API errors for forbidden interventions

## Safety Validation

Abuse-resistance tests should verify:

- Fake consensus requests are rejected.
- Bot amplification requests are rejected.
- Covert influencer seeding requests are rejected.
- Deceptive attention diversion requests are rejected.
- Vulnerable-group manipulation requests are rejected.
- Individual persuasion targeting requests are rejected.
- Account-level influenceability scoring requests are rejected.
- Suppression or harassment requests are rejected.

## Validation Exit Criteria for MVP

MVP validation is acceptable when:

- All docking tests pass.
- Ethics guardrail tests pass.
- Output schemas are stable.
- Scenario outputs are deterministic.
- Assumption logs are present.
- UI copy clearly says the simulator is scenario rehearsal, not guaranteed prediction.
- No real API, real LLM, live fetch, or crawler path is enabled.
