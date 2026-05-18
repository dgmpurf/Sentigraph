# Simulation Strategy Policy

Status: design only. This document defines ethical strategy implications for Event Frame and Audience Initialization. It does not implement product code, real API calls, real LLM calls, platform actions, or manipulation tactics.

## Purpose

The Strategy Policy layer converts Event Frame, Audience Initialization, and Baseline Gap Analysis into safe simulation options. It is not an execution system. It can recommend what to compare in Simulation Lab, but any real-world response remains outside the simulator and requires human review.

## Policy Principles

- Transparent crisis response only.
- Aggregate-level scenario comparison only.
- Human review required.
- No automatic public action execution.
- No covert influence, fake consensus, bot amplification, fake events, deceptive distraction, or individual targeting.
- Lawful/platform-authorized visibility actions may be modeled only as tradeoffs with policy basis and transparent explanation.

## Strategy Implications by Gap Class

### Public Baseline and Frame Are Aligned

Recommended simulation options:

- remediation plan.
- clarification.
- apology when responsibility is credible.
- compensation when direct harm or loss exists.
- transparent progress updates.
- third-party evidence.
- lawful content governance if policy basis is clear.

Risk posture: treat the event as potentially broader than one community. Optimize for repair, evidence, and trust recovery rather than message volume.

### Frame More Negative Than Public Baseline

Recommended simulation options:

- broaden observation frame.
- compare clarification vs third-party evidence.
- test cross-community exposure with aggregate bridge-node assumptions.
- use disclosed experts or creators to explain evidence when appropriate.
- evaluate whether removal or visibility reduction may create neutral-audience backlash.

Do not:

- assume the current frame represents all publics.
- create covert praise.
- seed fake grassroots reactions.
- hide criticism merely because it is negative.

### Frame More Positive Than Public Baseline

Recommended simulation options:

- run a wider-public baseline stress test.
- compare no-response vs clarification for neutral observers.
- prepare factual FAQ and progress updates before broader spread.
- warn that friendly echo chambers can understate risk.

Do not:

- treat supportive comments as proof of low risk.
- amplify friendly reactions as fake consensus.
- ignore safety/legal or workplace issues because current fans are positive.

### Polarized Frame

Recommended simulation options:

- clarification plus empathy.
- third-party evidence.
- progress update cadence.
- bridge-node exposure assumptions.
- neutral-observer reaction to tone and evidence.

Do not:

- use accusatory language.
- frame critics as enemies.
- optimize only for core supporters.

### Manipulation-Suspected Frame

Recommended simulation options:

- misinformation correction.
- platform labeling where appropriate.
- third-party evidence.
- monitoring and repeated-script analysis.
- lawful content governance only with explicit policy basis.

Do not:

- respond with fake consensus or bot amplification.
- dismiss all criticism as coordinated.
- publish unsupported claims of fraud or manipulation.

### Insufficient Data

Recommended simulation options:

- synthetic-only rehearsal.
- additional monitoring snapshots.
- broader platform/source review.
- manual expert review before operational interpretation.

Do not:

- recommend a high-confidence strategy.
- present simulation output as forecast certainty.

## Content Visibility Intervention Policy

Simulation Lab may model the following lawful/platform-authorized actions:

- deletion/removal.
- visibility reduction.
- comment closure.
- account restriction, aggregate only.
- platform labeling.
- policy enforcement notice.
- transparent explanation.

Each visibility simulation must evaluate these input assumptions:

- `target_message_reach`.
- `residual_copies`.
- `screenshot_probability`.
- `repost_migration_probability`.
- `perceived_suppression`.
- `policy_violation_clarity`.
- `legitimacy_of_removal`.
- `public_explanation_quality`.
- `reactance_amplification`.
- `martyr_effect`.
- `cross_platform_spillover`.
- `neutral_audience_negative_shift`.
- `hard_opposition_negative_shift`.

Each visibility simulation must emit these output metrics:

- `exposure_reduction`.
- `backlash_risk`.
- `neutral_audience_negative_shift`.
- `hard_opposition_reaction`.
- `cross_platform_spillover`.
- `trust_loss`.
- `net_risk_change`.
- `removal_legitimacy_score`.

Safe interpretation:

- High exposure reduction can still be harmful if neutral-audience trust loss is high.
- Labeling or clarification may be preferable when policy clarity is weak.
- Removal plus transparent explanation should be compared against no response, labeling, and clarification.
- Hard-opposition backlash alone is less concerning than shifting neutral observers negatively, but it still belongs in the tradeoff report.

Visibility modeling must not produce:

- target-account lists.
- instructions to evade platform rules.
- illegal suppression plans.
- covert censorship plans.
- harassment or retaliation recommendations.

## Creator and Influencer Communication Modeling

Simulation Lab may compare disclosed, truthful, transparent communication paths.

Allowed:

- disclosed creator education.
- expert explanation.
- third-party evidence interpretation.
- FAQ amplification.
- transparent creator collaboration.
- real user support-channel explanation.
- public correction by accountable parties.

Forbidden:

- covert paid praise.
- fake grassroots.
- undisclosed paid defense.
- false testimonials.
- harassment campaigns.
- fake consensus.
- bot amplification.
- covert influencer seeding.
- creator targeting based on hidden influenceability.

Creator/expert communication modeling should remain aggregate:

- creator/expert channel type.
- disclosure quality.
- credibility.
- evidence clarity.
- audience overlap.
- likely neutral-observer effect.

It should not identify specific people to pressure, recruit covertly, silence, or manipulate.

## Schema Proposals

```yaml
StrategyImplication:
  implication_id: string
  frame_gap_classification: string
  recommended_simulation_options:
    - string
  discouraged_options:
    - string
  rationale: string
  human_review_required: true
  confidence_label: enum # low, medium, high, insufficient_data
  safety_warnings:
    - string
```

```yaml
ContentVisibilityTradeoff:
  tradeoff_id: string
  intervention_type: enum # content_removal, visibility_reduction, comment_closure, account_restriction, platform_labeling, policy_enforcement_notice, content_removal_with_explanation
  policy_basis: string
  authorization_source: string
  transparent_explanation_required: boolean
  target_message_reach: number
  residual_copies: number
  screenshot_probability: number
  repost_migration_probability: number
  perceived_suppression: number
  policy_violation_clarity: number
  legitimacy_of_removal: number
  public_explanation_quality: number
  reactance_amplification: number
  martyr_effect: number
  cross_platform_spillover_input: number
  exposure_reduction: number
  backlash_risk: number
  neutral_audience_negative_shift: number
  hard_opposition_reaction: number
  cross_platform_spillover: number
  trust_loss: number
  net_risk_change: number
  removal_legitimacy_score: number
  recommendation: enum # not_recommended, conditional_human_review, allowed_with_transparent_explanation, prefer_labeling_or_clarification
  explanation: string
  aggregate_level_only: true
  automatic_execution_supported: false
```

```yaml
CreatorCommunicationPlan:
  plan_id: string
  communication_type: enum # disclosed_creator_education, expert_explanation, third_party_evidence_interpretation, faq_amplification, transparent_creator_collaboration, support_channel_explanation
  disclosure_required: true
  evidence_required: true
  source_credibility: number
  public_explanation_quality: number
  expected_neutral_audience_effect: number
  expected_trust_recovery_effect: number
  risks:
    - string
  forbidden_absent:
    covert_payment: true
    fake_grassroots: true
    false_testimonials: true
    bot_amplification: true
    individual_targeting: true
```

## Implementation Boundary

The next implementation should only build schema placeholders and deterministic strategy-option generation from aggregate Event Frame outputs. It should not run real APIs, call real LLMs, execute platform actions, generate specific outreach lists, or recommend covert operations.
