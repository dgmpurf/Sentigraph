# Simulation Audience Initialization

Status: design only. This document does not implement product code or real-data import. It defines how aggregate public signals should initialize synthetic Simulation Lab audiences.

## Purpose

Audience Initialization converts an Event Frame into a synthetic echo-chamber starting state. It decides how many bubbles/agents represent each aggregate segment, how they are colored, how much attention they carry, and which psychological weights are assumed for each persona cluster.

The layer uses aggregate public behavior only. It must not create individual persuasion profiles, individual targeting lists, or account-level influenceability scores.

## Audience Frame Definition

The simulation box should include these aggregate audience segments:

- `affected_users`: people directly affected by the event, product, service, policy, or incident.
- `core_opposition`: highly negative, highly engaged users already committed to criticism.
- `mild_opposition`: dissatisfied or concerned users who may update with credible remediation.
- `neutral_observers`: undecided viewers who are sensitive to evidence quality, legitimacy, and tone.
- `supporters`: users with positive prior trust, brand affinity, or countervailing evidence.
- `authority_trusting_users`: users more responsive to official, expert, legal, media, or third-party evidence.
- `bridge_nodes`: aggregate cross-community connectors that can carry transparent information across bubbles.
- `external_public_baseline`: a synthetic ordinary-public reference profile, not derived from the narrow observed frame.

Segment names are descriptive simulation cohorts. They do not map to real accounts or targetable people.

## Observed Community Signals

Observed public comments/posts can derive these aggregate inputs:

- `stance_distribution`: oppose, support, neutral, questioning, mixed.
- `sentiment_distribution`: negative, neutral, positive, mixed/ambiguous.
- `topic_distribution`: sub-issue or topic shares.
- `top_risk_topics`: V1.5 top topic risk output.
- `manipulation_signals`: repeated-script density, bot-like concentration, coordination suspicion.
- `influence_distribution`: aggregate reach, engagement, propagation, or bridge exposure proxies.
- `attention_level`: aggregate attention or activity proxy from volume, recency, engagement, monitoring snapshots, or forecast state.
- `action_threshold`: inferred aggregate willingness to comment, share, wait, or stay silent, labeled as an assumption unless directly supported.
- `activity_distribution`: comment/post share by platform or cohort if available.
- `evidence_distribution`: how much discussion references verifiable evidence versus claims or rumors.

These signals should initialize the simulation without storing raw prompts, raw private text, API keys, or personal identifiers.

## Mapping to Bubble and Agent Initialization

Aggregate observed signals map to synthetic visual and model parameters:

| Observed signal | Simulation initialization |
| --- | --- |
| Negative stance share | Red/hostile bubble proportion and negative latent opinion |
| Neutral or questioning share | Gray observer bubble proportion and higher action threshold |
| Supportive share | Green/blue support bubble proportion and positive prior anchor |
| High topic risk | Higher message salience and attention budget |
| Repeated-script signal | Manipulation warning and lower source credibility for suspicious cluster |
| High credible harm | Higher real-crisis message weight and lower public tolerance |
| High influence proxy | Larger bubble size or centrality proxy |
| Cross-community spread | More bridge nodes and higher cross-cutting exposure |
| High attention level | Higher initial attention budget and stronger message visibility |
| High inferred action threshold | More observing/latent agents and slower public expression |
| High fatigue | Lower attention budget and slower expression updates |

Recommended MVP defaults:

- Initialize at least five visible segments even when observed data is thin.
- Preserve external public baseline separately from the observed frame.
- Clamp all model weights to documented ranges.
- Mark inferred values as assumptions.

## Persona Cluster Initialization

Persona clusters are aggregate behavioral priors. They should be created from public historical behavior, synthetic baselines, and current aggregate signals only.

Variables:

- `confirmation_bias`: tendency to accept congenial information.
- `authority_trust`: responsiveness to official, expert, media, or third-party evidence.
- `conformity`: sensitivity to local majority signals.
- `reactance`: resistance when an intervention feels coercive or unfair.
- `negativity_weight`: sensitivity to negative or threat-related information.
- `attention_fatigue`: decline in attention after repeated exposure.
- `identity_attachment`: how strongly the issue relates to a group identity or role.
- `loss_sensitivity`: sensitivity to financial, safety, service, or status loss.
- `moral_outrage_sensitivity`: sensitivity to perceived unfairness, deception, discrimination, or harm.
- `platform_activity`: relative activity or visibility in the observed public frame.

Important boundary: persona clusters are not psychographic targeting profiles. They exist only to initialize aggregate simulation behavior.

## Reference Public Baseline

The `external_public_baseline` should be synthetic/academic, not simply the current comment section. It should encode ordinary-public assumptions:

- expected average reaction to the event category.
- expected loss sensitivity.
- expected authority trust.
- expected reactance.
- expected moral outrage.
- expected safety/legal sensitivity.
- expected trust loss from unclear or delayed response.
- expected tolerance for lawful policy enforcement with transparent explanation.

The baseline should be versioned and labeled as assumed unless calibrated later with reviewed aggregate datasets.

## Schema Proposals

```yaml
AudienceSegment:
  segment_id: string
  label: string
  segment_type: enum # affected_users, core_opposition, mild_opposition, neutral_observers, supporters, authority_trusting_users, bridge_nodes, external_public_baseline
  proportion: number # 0-1
  stance_distribution:
    oppose: number
    support: number
    neutral: number
    questioning: number
    mixed: number
  sentiment_distribution:
    negative: number
    neutral: number
    positive: number
  color_hint: enum # red, gray, green, blue, orange
  average_attention_level: number # 0-1
  opinion_baseline: number # -1 to 1
  action_threshold: number # 0-1
  influence_proxy: number # 0-100
  attention_level_source: enum # observed, inferred, assumed
  action_threshold_source: enum # observed, inferred, assumed
  bridge_score: number # 0-1
  data_origin: enum # observed, baseline_assumption, synthetic_default
  warnings:
    - string
```

```yaml
PersonaCluster:
  cluster_id: string
  segment_id: string
  label: string
  confirmation_bias: number
  authority_trust: number
  conformity: number
  reactance: number
  negativity_weight: number
  attention_fatigue: number
  identity_attachment: number
  loss_sensitivity: number
  moral_outrage_sensitivity: number
  platform_activity: number
  source: enum # aggregate_observed, academic_baseline, synthetic_default
  no_individual_profile: true
```

```yaml
ObservedFrameProfile:
  observed_comment_count: integer
  observed_post_count: integer
  observed_platforms:
    - string
  stance_distribution: object
  sentiment_distribution: object
  topic_distribution: object
  top_risk_topics:
    - string
  manipulation_signal_score: number
  real_crisis_signal_score: number
  influence_distribution_summary:
    low: number
    medium: number
    high: number
  audience_segments:
    - AudienceSegment
  persona_clusters:
    - PersonaCluster
  uncertainty_label: enum # low, medium, high, insufficient_data
```

```yaml
BaselinePublicProfile:
  baseline_id: string
  baseline_version: string
  event_category: string
  expected_average_reaction: number # -1 to 1
  expected_loss_sensitivity: number
  expected_authority_trust: number
  expected_reactance: number
  expected_moral_outrage: number
  expected_safety_legal_sensitivity: number
  expected_policy_enforcement_tolerance: number
  assumed_parameters:
    - string
  limitations:
    - string
```

## Initialization Safeguards

- Never infer hidden traits for named people.
- Never output individual targets, creator targets, or account restriction lists.
- Keep bridge-node modeling aggregate.
- Preserve uncertainty when the observed frame is narrow.
- Do not treat bot/manipulation suspicion as proof without evidence.
- Do not dismiss legitimate complaints just because suspected manipulation exists.

## MVP Implementation Notes

The first code task should create schema placeholders and deterministic fixture mappers only. It should use current V1.5 risk output and synthetic baselines; it should not enable real monitoring-case initialization until privacy, data minimization, and benchmark tests are ready.
