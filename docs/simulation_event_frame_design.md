# Simulation Event Frame Design

Status: design only. This document does not implement product code, real API calls, real LLM calls, live public fetching, crawler behavior, or manipulation tactics.

## Purpose

The Event Frame layer converts an observed public-opinion event into a structured initial frame for Simulation Lab. It answers:

- What is the event actually about?
- Which sub-issues are driving risk?
- Which parts are measured from current aggregate Sentigraph output?
- Which parts are assumed, synthetic, or uncertain?
- What should the simulator initialize before any ethical intervention comparison?

The Event Frame must remain aggregate-level. It must not create individual persuasion profiles, identify accounts for targeting, rank people by influenceability, or produce operational instructions for manipulation.

## Position in Sentigraph

The Event Frame sits between current analysis outputs and the Simulation Lab scenario builder.

```text
case data / monitoring snapshots
  -> sentiment, topics, V1.5 risk, manipulation signals, reports
  -> EventFrame builder
  -> Audience initialization
  -> baseline gap analysis
  -> SimulationScenario
  -> Simulation Lab run / A-B comparison
```

Input sources should be limited to safe aggregate artifacts:

- Topic clusters and topic risk scores.
- Sentiment distribution.
- Representative comments only as reviewed examples, not raw payload dumps.
- Manipulation or repeated-script signals.
- Propagation and influence proxies when available.
- Monitoring snapshots and forecast state.
- Synthetic or academic public baseline assumptions.

## Relationship to Existing Sentigraph Modules

The Event Frame should reuse current Sentigraph outputs instead of inventing a parallel analysis stack:

- V1.5 topic risk supplies `top_risk_topics`, topic-level risk scores, real-crisis risk, manipulation risk, and risk explanations.
- Monitoring supplies time-ordered aggregate snapshots, alert history, and observed risk movement.
- Forecasting supplies deterministic trend context such as rising, falling, stable, or insufficient-history states.
- Simulation Lab consumes the Event Frame as an initialization contract for aggregate agents, message/event cards, audience segments, and A/B intervention comparison.
- Reports can later summarize Event Frame assumptions, baseline gaps, and safe strategy comparisons for human review.

The Event Frame should not replace these modules. It should preserve their outputs as estimated parameters and clearly label synthetic baseline assumptions.

## Event Decomposition

One event should be decomposed into sub-issues so the simulator can avoid treating a crisis as one undifferentiated negative blob.

Supported sub-issue categories:

- `product_quality`: defects, reliability complaints, performance degradation, service quality.
- `official_response_delay`: delayed explanation, silence, unclear timeline, perceived avoidance.
- `pricing_dispute`: price fairness, refunds, discounts, hidden fees, unequal treatment.
- `safety_legal_issue`: safety, legality, compliance, discrimination, fraud, public harm, regulatory exposure.
- `brand_trust`: perceived credibility, sincerity, history of similar issues, broken promises.
- `suspected_manipulation`: repeated scripts, suspicious coordination, bot-like activity, low-credibility amplification.
- `public_figure_controversy`: celebrity, executive, employee, influencer, or spokesperson controversy.
- `workplace_company_issue`: labor dispute, workplace complaint, management conduct, layoffs, internal culture.

Sub-issue detection should be conservative. If the current rule/template logic cannot classify an issue confidently, mark it as `unknown` or add an uncertainty warning rather than forcing a category.

## Sub-Issue Severity

Each sub-issue should carry:

- `observed_volume`: aggregate volume share in the current frame.
- `negative_ratio`: negative sentiment share.
- `severity_hint`: low, medium, high, or critical.
- `topic_risk_score`: V1.5 topic risk when available.
- `real_crisis_signal`: credible harm, safety, legal, service-impact, or trust damage signal.
- `manipulation_signal`: repeated-script or coordination signal.
- `evidence_quality`: how much of the issue is supported by observable public evidence.
- `uncertainty`: low, medium, high, or insufficient_data.

Sub-issue severity should prioritize safety/legal and credible real-crisis signals over raw volume. A small but high-severity topic should not be diluted by many low-risk neutral topics.

## Event Frame Workflow

1. Collect safe aggregate inputs from the existing case result, monitoring snapshots, or benchmark fixture.
2. Normalize topics into sub-issue categories.
3. Attach observed sentiment, stance, manipulation, and influence distributions.
4. Separate estimated values from assumed defaults.
5. Create an observed frame profile.
6. Compare it with an external public baseline.
7. Emit strategy implications and Simulation Lab initialization parameters.

The workflow should fail safely:

- If there are no comments or no snapshots, return `insufficient_data`.
- If topics exist but categories are ambiguous, preserve raw topic labels and mark uncertainty.
- If manipulation signals are high but real-crisis signal is also high, do not dismiss the event as fake; track both.
- If the observed frame is narrow, require a broader observation warning before strategy interpretation.

## Output Schema Proposal

```yaml
EventFrame:
  event_frame_id: string
  case_id: string | null
  event_title: string
  event_summary: string
  generated_at: string
  source_mode: enum # synthetic_fixture, aggregate_case_output, monitoring_snapshot, manual_review
  data_safety:
    aggregate_only: true
    no_real_account_targets: true
    no_private_data: true
    raw_payload_retained: false
  sub_issues:
    - SubIssue
  observed_frame_profile: ObservedFrameProfile
  baseline_public_profile: BaselinePublicProfile
  frame_gap_analysis: FrameGapAnalysis
  strategy_implications:
    - StrategyImplication
  initialization_hints:
    audience_segments:
      - string
    persona_clusters:
      - string
    suggested_simulation_steps: integer
    recommended_intervention_candidates:
      - string
  uncertainty:
    label: enum # low, medium, high, insufficient_data
    reasons:
      - string
  assumption_log:
    estimated_parameters:
      - string
    assumed_parameters:
      - string
    unknown_parameters:
      - string
```

```yaml
SubIssue:
  sub_issue_id: string
  category: enum
  label: string
  summary: string
  observed_volume: number          # 0-1
  negative_ratio: number           # 0-1
  neutral_ratio: number            # 0-1
  positive_ratio: number           # 0-1
  topic_risk_score: number         # 0-100
  severity_hint: enum              # low, medium, high, critical
  real_crisis_signal: number       # 0-100
  manipulation_signal: number      # 0-100
  influence_proxy: number          # 0-100
  evidence_quality: enum           # weak, mixed, moderate, strong
  representative_comment_refs:
    - string                       # safe internal ids or redacted refs only
  uncertainty_reasons:
    - string
```

## Relationship to Simulation Scenario

The Event Frame does not run the simulator by itself. It creates a safe initialization contract:

- Sub-issues become scenario topics and message/event cards.
- Audience frame proportions become synthetic agent communities.
- Sentiment and stance distributions become initial opinion distributions.
- Top-risk topics become higher-attention messages.
- Observed attention, activity, and influence proxies become aggregate attention budgets, bubble sizes, and bridge exposure assumptions.
- Neutral/questioning shares, fatigue, and prior engagement become conservative aggregate action-threshold assumptions.
- Manipulation signals become aggregate warnings and model variables, not tactics.
- Baseline gaps become strategy caveats.
- Content visibility tradeoffs become optional lawful/platform-authorized comparison inputs.

## Safety Boundaries

The Event Frame must not:

- Fetch live pages.
- Call real platform APIs.
- Call real LLM APIs.
- Create fake events.
- Recommend fake consensus, bot amplification, covert seeding, deceptive diversion, or individual targeting.
- Use real account handles, cookies, private messages, credentials, or hidden data.
- Present observed community behavior as representative of the whole public without a gap warning.

## MVP Implementation Notes

The first implementation should be schema-first and fixture-first:

- Build from existing aggregate case outputs and synthetic benchmark fixtures.
- Use deterministic category mapping and conservative fallback labels.
- Store only summary fields, counts, ratios, and safe references.
- Add offline benchmark cases for aligned, more-negative, more-positive, polarized, manipulation-suspected, and insufficient-data frames.
