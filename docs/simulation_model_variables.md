# Simulation Lab Model Variables

Status: schema design only. These variables describe a future deterministic, ethical Simulation Lab module. They are not product code and do not enable real API, crawler, or LLM behavior.

All schemas are conceptual and should be converted into backend Pydantic models only in a later implementation task.

## Agent Schema

Synthetic agents represent aggregate personas or cohort-level simulation particles. They must not represent real accounts or identifiable users.

```yaml
SimulationAgent:
  agent_id: string
  cohort_label: string
  latent_opinion: number        # -1.0 to 1.0, private stance
  expressed_opinion: number     # -1.0 to 1.0, public stance
  initial_opinion: number       # -1.0 to 1.0
  stubbornness: number          # 0.0 to 1.0, Friedkin-Johnsen persistence
  confirmation_bias: number     # 0.0 to 1.0
  motivated_reasoning: number   # 0.0 to 1.0
  negativity_weight: number     # 0.0 to 2.0
  reactance: number             # 0.0 to 1.0
  authority_trust:
    official: number            # 0.0 to 1.0
    media: number               # 0.0 to 1.0
    third_party: number         # 0.0 to 1.0
    peer: number                # 0.0 to 1.0
  conformity: number            # 0.0 to 1.0
  identity_vector: number[]     # low-dimensional synthetic identity coordinates
  attention_budget: number      # 0.0 to 1.0
  fatigue: number               # 0.0 to 1.0
  action_threshold: number      # 0.0 to 1.0
  confidence_radius: number     # 0.0 to 2.0 on opinion-distance scale
  public_commitment: number     # 0.0 to 1.0
  activity_intensity: number    # 0.0 to 1.0
  narrative_affinity:
    quality_issue: number
    safety_issue: number
    price_issue: number
    apology_acceptance: number
    correction_acceptance: number
  safety_flags:
    synthetic_only: true
    no_real_account_mapping: true
```

Required MVP fields:

- `latent_opinion`
- `expressed_opinion`
- `stubbornness`
- `confidence_radius`
- `action_threshold`
- `attention_budget`
- `fatigue`
- `authority_trust`

V2 fields:

- `public_commitment`
- `narrative_affinity`
- richer `identity_vector`

Forbidden field use:

- Do not store real user identifiers.
- Do not attach real account URLs.
- Do not calculate individual influenceability.

## Message Schema

Messages represent public claims or transparent response events. They may be generated from a scenario template or entered by a user as a reviewed intervention package.

```yaml
SimulationMessage:
  message_id: string
  source_type: enum            # official, media, third_party, peer, rumor, unknown
  source_credibility: number   # 0.0 to 1.0
  evidence_strength: number    # 0.0 to 1.0
  framing: enum                # clarification, apology, compensation, faq, progress_update, third_party_evidence, correction, prebunking, neutral
  stance_direction: number     # -1.0 to 1.0
  specificity: number          # 0.0 to 1.0
  emotional_valence: number    # -1.0 to 1.0
  identity_affirmation: number # 0.0 to 1.0
  autonomy_threat: number      # 0.0 to 1.0
  novelty: number              # 0.0 to 1.0
  repetition_signature: string # safe aggregate repetition label, not bot instruction
  platform_affordance:
    comment_visibility: number
    share_friction: number
    quote_context: number
    correction_visibility: number
  visibility_seed: number      # 0.0 to 1.0
  created_at_step: integer
  transparency_label: string
```

Safety notes:

- `repetition_signature` exists to detect or model observed repetition, not to create repeated scripts.
- `framing` must stay within transparent response categories.
- `source_type` must not be fabricated to impersonate real third parties.

## Network Schema

The network is synthetic and aggregate. It should describe exposure patterns, not real social graphs.

```yaml
SimulationNetwork:
  network_id: string
  nodes:
    - agent_id: string
      cohort_label: string
      bridge_score: number                 # 0.0 to 1.0
      local_cluster_id: string
      cross_cutting_exposure_rate: number  # 0.0 to 1.0
  edges:
    - source_agent_id: string
      target_agent_id: string
      tie_strength: number                 # 0.0 to 1.0
      trust_weight: number                 # 0.0 to 1.0
      conflict_weight: number              # 0.0 to 1.0
      homophily_score: number              # 0.0 to 1.0
      exposure_probability: number         # 0.0 to 1.0
  global_metrics:
    modularity: number
    polarization: number
    opinion_entropy: number
    average_cross_cutting_exposure_rate: number
```

MVP network:

- Static.
- Homophilous.
- Small enough to explain and benchmark.
- No real account import.

V2 network:

- Optional dynamic rewiring after validation.
- Optional cross-platform layer after real data permissions and privacy review.

## Intervention Schema

Interventions are transparent crisis-response packages.

```yaml
SimulationIntervention:
  intervention_id: string
  intervention_type: enum       # clarification, apology, compensation, faq, progress_update, third_party_evidence, correction, prebunking
  responsible_party: string
  transparency_label: string
  publication_step: integer
  publication_cadence: enum     # one_time, scheduled_updates, event_triggered
  target_scope: enum            # all_public, topic_segment, platform_segment
  evidence_strength: number     # 0.0 to 1.0
  empathy_level: number         # 0.0 to 1.0
  responsibility_admission: number # 0.0 to 1.0
  compensation_offer:
    present: boolean
    specificity: number
  corrective_action:
    present: boolean
    specificity: number
  third_party_verification:
    present: boolean
    source_credibility: number
  warnings:
    - string
```

Rules:

- `target_scope` must remain aggregate.
- No field may specify account lists, vulnerable groups, or individual targets.
- Interventions must be reviewable and truthful.

## FeedPolicy Schema

Feed policies describe aggregate visibility assumptions for a platform-like environment.

```yaml
SimulationFeedPolicy:
  policy_id: string
  platform_label: string
  ranking_bias:
    recency: number
    engagement: number
    credibility: number
    controversy: number
    correction_boost: number
    misinformation_penalty: number
  decay:
    attention_half_life_steps: number
    novelty_decay: number
  interaction_affordances:
    reply_visibility: number
    quote_visibility: number
    reshare_visibility: number
    correction_visibility: number
  cross_cutting_exposure_rate: number
  safety_notes:
    live_fetch_enabled: false
    real_platform_calibration: false
```

MVP feed policies should be synthetic profiles such as `generic_news`, `generic_forum`, and `generic_short_video`. Platform-specific calibration is future work.

## Simulation Output Schema

Outputs must be aggregate, uncertainty-labeled, and safe to display.

```yaml
SimulationOutput:
  simulation_id: string
  scenario_name: string
  generated_at: string
  status: enum                  # complete, warning, insufficient_assumptions, failed_safe
  model_version: string
  assumptions:
    estimated_parameters:
      - string
    assumed_parameters:
      - string
    data_sources:
      - string
  intervention_summary:
    intervention_id: string
    intervention_type: string
    transparency_label: string
  aggregate_metrics:
    predicted_risk_score: number
    predicted_risk_level: enum  # low, medium, high, critical
    real_crisis_risk: number
    manipulation_risk: number
    polarization: number
    opinion_entropy: number
    narrative_dominance: number
    correction_uptake: number
    trust_recovery: number
    attention_half_life: number
    cross_cutting_exposure_rate: number
    ethical_risk_score: number
  topic_metrics:
    - topic_id: string
      topic: string
      current_risk: number
      simulated_risk: number
      trend_direction: enum     # rising, falling, stable, unknown
      explanation: string
  comparison:
    baseline_delta: number
    alternative_rank: integer
    uncertainty_label: enum     # low, medium, high, insufficient_data
  warnings:
    - string
  forbidden_outputs_absent:
    account_targets: true
    persuasion_scores: true
    bot_instructions: true
    covert_seeding_plan: true
```

## Parameter Governance

Every simulation run should separate:

- Estimated parameters: derived from monitoring snapshots, aggregate risk output, or validated fixtures.
- Assumed parameters: chosen defaults or scenario values.
- User-provided scenario parameters: transparent and auditable.

The UI should show assumption labels before any scenario result is interpreted.
