# Simulation Baseline Gap Analysis

Status: design only. This document defines the comparison between an observed event frame and an external public baseline. It does not implement code or real data access.

## Purpose

Baseline Gap Analysis explains whether the observed discussion frame is likely representative of broader public reaction or whether it is unusually negative, unusually positive, polarized, manipulation-suspected, or too thin to interpret.

This is a caution layer. It prevents Simulation Lab from overfitting to one comment area, one platform, one fan community, or one coordinated discussion pocket.

## Baseline Profiles

Sentigraph should maintain synthetic/academic ordinary-public baselines by event category. These are assumptions, not measured facts, until calibrated later.

Baseline dimensions:

- `expected_average_reaction`: ordinary-public stance estimate from -1 to 1.
- `expected_loss_sensitivity`: sensitivity to money, time, safety, service, or status loss.
- `expected_authority_trust`: tendency to accept official, expert, or third-party evidence.
- `expected_reactance`: expected backlash when response feels coercive or unfair.
- `expected_moral_outrage`: response to deception, discrimination, harm, or unfairness.
- `expected_safety_legal_sensitivity`: sensitivity to safety, legal, compliance, or public-harm issues.
- `expected_policy_enforcement_tolerance`: tolerance for lawful/platform-authorized moderation when explanation and policy clarity are high.

Recommended starting baselines:

- product/service complaint.
- safety/legal concern.
- pricing dispute.
- public figure controversy.
- workplace/company issue.
- suspected misinformation/manipulation.
- content visibility intervention.

## Gap Inputs

The gap analyzer compares:

- External public baseline.
- Observed frame stance distribution.
- Observed frame sentiment distribution.
- Top sub-issues and topic risks.
- Real-crisis and manipulation signals.
- Polarization level.
- Neutral-observer share.
- Supporter/opposition share.
- Platform/frame breadth.
- Evidence quality and uncertainty.

## Gap Classifications

### `aligned_public_and_frame`

The observed frame resembles the external public baseline within tolerance.

Implication: the event likely reflects a broader public issue. Strategy should focus on remediation, clarification, apology, compensation, transparent updates, third-party evidence, and lawful content governance if needed.

### `frame_more_negative_than_public`

The observed frame is more negative than the expected ordinary-public baseline.

Implication: the current frame may be an activated pocket, opposition-heavy area, or narrow platform sample. Broaden observation before interpreting it as broad public sentiment. Test whether transparent external evidence can cross bubbles. Evaluate whether visibility intervention could create neutral-audience backlash.

### `frame_more_positive_than_public`

The observed frame is more positive than the expected ordinary-public baseline.

Implication: the case may be observed inside a friendly echo chamber. Do not overstate safety. Broader exposure may increase risk if neutral audiences are less forgiving.

### `polarized_frame`

The observed frame contains strong support and strong opposition with high conflict or topic disagreement.

Implication: intervention should avoid triumphal tone, accusatory language, or one-sided framing. Compare clarification, third-party evidence, and progress updates. Monitor bridge-node exposure and neutral observer movement.

### `manipulation_suspected_frame`

Repeated scripts, suspicious coordination, low-credibility concentration, or bot-like behavior is elevated.

Implication: keep manipulation risk separate from real-crisis risk. Do not dismiss legitimate harm. Compare factual correction, platform labeling, evidence transparency, and monitoring; do not respond with fake consensus or covert amplification.

### `insufficient_data`

There are too few safe aggregate observations, too little topic evidence, or too much uncertainty.

Implication: do not run strategy interpretation as if it were measured. Recommend additional monitoring snapshots, broader source coverage, or synthetic-only scenario rehearsal.

## Coarse Decision Rules

The first implementation can use deterministic thresholds:

- If observed count is below minimum or all key distributions are missing: `insufficient_data`.
- If manipulation signal is high and repeated-script density is material: include `manipulation_suspected_frame`.
- If positive and negative shares are both high: include `polarized_frame`.
- If observed average stance is more than a configured delta below baseline: `frame_more_negative_than_public`.
- If observed average stance is more than a configured delta above baseline: `frame_more_positive_than_public`.
- Otherwise: `aligned_public_and_frame`.

Multiple labels may be present. For example, a frame can be both `frame_more_negative_than_public` and `manipulation_suspected_frame`.

## Schema Proposal

```yaml
FrameGapAnalysis:
  analysis_id: string
  event_frame_id: string
  primary_classification: enum
  secondary_classifications:
    - enum
  baseline_profile_id: string
  observed_frame_id: string
  gap_scores:
    average_reaction_gap: number       # observed - baseline, -2 to 2
    negativity_gap: number             # -1 to 1
    positivity_gap: number             # -1 to 1
    polarization_score: number         # 0-100
    manipulation_suspected_score: number # 0-100
    evidence_quality_score: number     # 0-100
    representativeness_score: number   # 0-100
  interpretation:
    summary: string
    strategy_cautions:
      - string
    monitoring_recommendations:
      - string
  uncertainty:
    label: enum # low, medium, high, insufficient_data
    reasons:
      - string
  safety_flags:
    aggregate_only: true
    no_individual_targeting: true
    no_manipulation_tactics: true
```

## Strategy Implications

When public baseline and frame are aligned:

- Prioritize remediation.
- Clarify facts and timeline.
- Apologize when responsibility is credible.
- Offer compensation when affected users need concrete remedy.
- Publish transparent progress updates.
- Use third-party evidence where appropriate.
- Model lawful content governance only if policy basis is clear.

When the frame is more negative than baseline:

- Broaden the observation frame before overreacting.
- Test cross-community exposure and external evidence.
- Use transparent experts or disclosed creators only.
- Avoid covert manipulation, fake support, or bot-like activity.
- Evaluate whether high-reach content moderation could shift neutral observers negatively.

When the frame is more positive than baseline:

- Warn that friendly-community feedback can understate risk.
- Test broader public exposure assumptions.
- Avoid overconfident messaging.
- Prepare neutral-audience explanations before the issue spreads.

When polarized:

- Avoid escalatory language.
- Use evidence-first, empathy-forward messages.
- Track bridge-node and neutral-observer metrics.
- Treat trust recovery and polarization reduction as separate goals.

When manipulation is suspected:

- Separate manipulation risk from legitimate crisis risk.
- Use correction, labeling, and monitoring.
- Do not manufacture counter-consensus.
- Consider lawful platform governance only with clear policy basis and transparent explanation.

## Validation Plan

Benchmarks should cover:

- aligned public and observed frame.
- observed frame more negative than public baseline.
- observed frame more positive than public baseline.
- polarized frame.
- manipulation-suspected frame.
- insufficient data.
- high real-crisis risk plus high manipulation signal.

The output should be coarse and stable; it should not claim the true public opinion of a population.

