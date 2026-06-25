# Opinion Ecosystem PeopleCluster First Transition Slice v0.1

Status: docs-only / future implementation plan / no runtime implementation.

This document defines the first acceptable future implementation slice for PeopleCluster in the deterministic local mock calculator. It uses `docs/model/peoplecluster_transition_model_v0_1.md` as the source of truth and does not invent new formulas.

## A. First Transition Slice Name

Phase 8P-5 PeopleCluster Transition Calculator.

## B. Purpose

Future implementation should calculate only `PeopleClusterStateV01` using local synthetic in-memory fixtures that already passed 8P-1 validation and can coexist with:

- 8P-2 `ContentAggregateWeightV01`
- 8P-3 `InfluenceCoreWeightV01`
- 8P-4 `EchoBoxWeightV01`

The first slice must stay anonymous, aggregate, sample-scoped, deterministic, uncalibrated, and non-predictive.

It must not calculate ResponseStrategy outputs, `pull_ik`, `stance_effect_ik`, individual persuasion probability, real user identities, or target user lists.

## C. Expected Future Code Scope If Approved Later

Likely future update scope:

- `backend/app/services/opinion_ecosystem_mock_calculator.py`
- `backend/app/tests/test_opinion_ecosystem_mock_calculator.py`

Do not add:

- API routes
- frontend UI
- runtime persistence
- schema files unless a future implementation proves they are absolutely necessary

## D. Future Pure Function Candidates

Future implementation may add small pure functions similar to the existing ContentAggregate, InfluenceCore, and EchoBox slices:

- `get_peoplecluster_associated_evidence(cluster, evidence_items)`
- `get_peoplecluster_content_aggregate_refs(cluster, content_aggregate_outputs)`
- `get_peoplecluster_influence_core_refs(cluster, influence_core_outputs)`
- `get_peoplecluster_echobox_refs(cluster, echo_box_outputs)`
- `calculate_peoplecluster_stance_state(cluster, evidence_items, upstream_outputs)`
- `calculate_peoplecluster_stance_confidence(cluster, evidence_items, upstream_outputs)`
- `calculate_peoplecluster_attention_level(cluster, evidence_items, upstream_outputs)`
- `calculate_peoplecluster_fatigue_level(cluster, evidence_items, upstream_outputs)`
- `calculate_peoplecluster_expression_intensity(cluster, evidence_items, upstream_outputs)`
- `calculate_peoplecluster_exit_risk(cluster, evidence_items, upstream_outputs)`
- `calculate_peoplecluster_reactivation_potential(cluster, evidence_items, upstream_outputs)`
- `calculate_peoplecluster_state(cluster, evidence_items, content_aggregate_outputs, influence_core_outputs, echo_box_outputs)`
- `calculate_all_peoplecluster_states(fixture, content_aggregate_outputs, influence_core_outputs, echo_box_outputs)`

These are design candidates only. This docs-only task does not implement them.

## E. Input Assumptions

Future 8P-5 may use only safe metadata from fixture objects and existing local calculator outputs.

Allowed fixture-level inputs:

- `fixture_metadata`
- `evidence_items_safe`
- `content_aggregates`
- `influence_cores`
- `echo_boxes`
- `people_clusters`
- `ContentAggregateWeightV01` output from 8P-2 if already available
- `InfluenceCoreWeightV01` output from 8P-3 if already available
- `EchoBoxWeightV01` output from 8P-4 if already available

Allowed PeopleCluster fields:

- `cluster_id`
- `cluster_role`
- `cluster_type`
- `sample_share_hint`
- `stance_distribution`
- `stance_hint`
- `stance_strength_hint`
- `stance_confidence_hint`
- `attention_hint`
- `fatigue_hint`
- `expression_hint`
- `exit_hint`
- `reactivation_hint`
- `openness_hint`
- `confidence_radius_hint`
- `issue_salience_hint`
- `exposure_hint`
- `bridge_exposure_hint`
- `echo_box_ids`
- `aggregate_ids`
- `influence_core_ids`
- `previous_state`
- `stage_id`
- `time_bucket`
- `risk_flags`

Allowed evidence fields:

- `evidence_id`
- `platform`
- `evidence_type`
- `acquisition_mode`
- `provenance_type`
- `verification_status`
- `trust_label`
- `trust_score`
- `review_status`
- `duplicate_group_id`
- `duplicate_count`
- `relevance_label`
- `recency_label`
- `stance_hint`
- `emotion_intensity_hint`
- `narrative_frame_hint`
- `source_url_present`
- `aggregate_ref`
- `influence_core_refs`
- `echo_box_refs`
- `people_cluster_refs` if present
- `created_at_bucket`
- `relative_stage_bucket`

No full text is required.

Forbidden input categories:

- raw author fields
- author names
- profile URLs
- private messages
- cookies
- tokens
- sessions
- browser profile data
- real account graph
- target user list
- individual-level user rows

## F. Formula Scope

Future 8P-5 must use `docs/model/peoplecluster_transition_model_v0_1.md` as the formula source of truth.

If a component is not explicitly defined there, future implementation must not invent a coefficient. It must mark the component as:

```text
implementation_requires_formula_confirmation_from_peoplecluster_transition_model_v0_1
```

The first implementation slice must be standalone `PeopleClusterStateV01` only.

Do not include:

- ResponseStrategy formulas
- `pull_ik`
- `stance_effect_ik`
- `InfluenceCoreToClusterEffectV01`
- individual persuasion probability
- target user lists

### F.1 PeopleClusterStateV01 Source Object

The source model defines `PeopleClusterStateV01` as:

```json
{
  "schema": "sentigraph_peoplecluster_state_v0_1",
  "model_status": "design_stage",
  "coefficient_source": "mock_default",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "state": {},
  "transition": {},
  "probabilities": {},
  "labels": [],
  "explanation": [],
  "flags": [
    "selected_sample_only",
    "not_real_person",
    "aggregate_behavioral_proxy"
  ]
}
```

Future implementation must keep the same source meaning. If schema naming differs between contracts, the implementation must resolve the mismatch explicitly before coding instead of silently adding a new schema name.

### F.2 State Vector

The source model defines the PeopleCluster state vector:

```text
s_i     = expressed_stance in [-1, 1]
k_i     = stance_confidence in [0, 1]
a_i     = attention_budget in [0, 1]
f_i     = fatigue in [0, 1]
e_i     = expression_intensity in [0, 1]
o_i     = openness in [0, 1]
u_i     = visibility_weight in [0, 1]
theta_i = action_threshold in [0, 1]
m_i     = reputation_memory_sensitivity in [0, 1]
```

Future implementation may map fixture hints into these fields only as anonymous aggregate proxies.

### F.3 Evidence Confidence Damping

The source model defines:

```text
D_Q = 0.40 + 0.60 * Q
```

`Q` comes from ContentAggregate evidence confidence. Low confidence dampens stance movement.

### F.4 Bounded Confidence / Openness Radius

The source model defines:

```text
epsilon_i = epsilon_min + (epsilon_max - epsilon_min) * o_i
epsilon_min = 0.25
epsilon_max = 0.85
```

```text
gate_ij = 1 if |s_i - s_j| <= epsilon_i, otherwise bridge_leak_ij
bridge_leak_ij = 0.10 * bridge_exposure_ij
```

This may support an openness / confidence-radius proxy only as aggregate sample behavior. It must not be described as individual openness or persuasion receptivity.

### F.5 Peer Field

The source model defines:

```text
P_i =
  sum_j(edge_ij * gate_ij * a_j * e_j * u_j * s_j)
  /
  (sum_j(edge_ij * gate_ij * a_j * e_j * u_j) + epsilon)
```

If future fixture fields do not safely provide `edge_ij`, `a_j`, `e_j`, `u_j`, or `s_j`, future implementation must either use already reviewed safe aggregate hints or emit `implementation_requires_formula_confirmation_from_peoplecluster_transition_model_v0_1`.

### F.6 InfluenceCore Field

The source model defines:

```text
core_gate_ik = o_i * q_k * exp(- |s_i - d_k| / tau_core)
tau_core = 0.75
```

```text
IC_i =
  sum_k(exposure_ik * core_gate_ik * p_k * d_k)
  /
  (sum_k(exposure_ik * core_gate_ik * p_k) + epsilon)
```

This is not `pull_ik` and not `stance_effect_ik`. It can only be used inside anonymous aggregate PeopleCluster state estimation if safe source fields exist.

### F.7 Resistance And Learning Rate

The source model defines:

```text
resistance_i =
  0.55 * k_i
+ 0.25 * (1 - o_i)
+ 0.20 * f_i
```

```text
eta_i =
  eta_base * a_i * (1 - f_i) * (1 - resistance_i) * D_Q
eta_base = 0.20
```

This is an aggregate transition dampening proxy. It must not be described as private belief resistance or individual learning.

### F.8 Stance State / Transition Pressure

The source model defines:

```text
s_i(t+1) =
clamp(
  s_i(t)
  + eta_i * [
      0.45 * (P_i - s_i(t))
    + 0.40 * (IC_i - s_i(t))
    + 0.15 * (RS_i - s_i(t))
  ],
  -1,
  1
)
```

`RS_i` is a response-strategy field if a reviewed strategy candidate exists. No strategy is auto-executed.

8P-5 must not implement ResponseStrategy. Therefore:

- If `RS_i` is unavailable, future implementation must not invent a strategy field.
- If the stance update cannot be safely calculated without `RS_i`, mark the component as `implementation_requires_formula_confirmation_from_peoplecluster_transition_model_v0_1`.
- If a neutral reviewed strategy proxy is used in a future implementation, it must be explicitly documented before coding.

### F.9 Stance Confidence

The source model defines:

```text
k_i(t+1) =
clamp(
  k_i(t)
  + 0.08 * aligned_i * repetition_signal
  + 0.06 * aligned_i * evidence_confidence
  - 0.07 * cross_i * o_i
  - 0.05 * uncertainty
  - 0.04 * fatigue_i,
  0,
  1
)
```

This is confidence in the aggregate state proxy, not confidence about truth and not confidence about a real person's belief.

### F.10 Attention Level

The source model defines:

```text
a_i(t+1) =
clamp(
  (1 - decay_a) * a_i(t)
  + 0.22 * H
  + 0.14 * C
  + 0.12 * novelty_signal
  + 0.08 * personal_relevance_proxy
  + 0.08 * reactivation_trigger
  - 0.18 * f_i(t)
  - 0.10 * resolution_signal,
  0,
  1
)
decay_a = 0.08
```

`personal_relevance_proxy` is an aggregate fixture proxy only. It must not imply personal data, individual identity, or psychological profiling.

### F.11 Fatigue Level

The source model defines:

```text
f_i(t+1) =
clamp(
  (1 - decay_f) * f_i(t)
  + 0.22 * H
  + 0.18 * C
  + 0.14 * repetition_signal
  + 0.10 * unresolved_grievance
  - 0.18 * resolution_signal
  - 0.12 * constructive_new_info
  - 0.08 * bridge_understanding,
  0,
  1
)
decay_f = 0.04
```

High closure, repetition, or heat can raise fatigue only as a selected-sample aggregate proxy.

### F.12 Expression Intensity / Expression Tendency

The source model defines:

```text
raw_expression_i =
  1.80 * a_i
+ 1.25 * C
+ 1.10 * emotion_intensity
+ 0.80 * |s_i| * k_i
+ 0.50 * social_norm_pressure
- 1.40 * f_i
- 1.20 * theta_i

e_i(t+1) = sigmoid(raw_expression_i)
```

Expression intensity is not a prediction that real people will post or act. It is only a selected-sample aggregate tendency proxy.

### F.13 Exit Risk / Withdrawal Tendency

The source model defines fatigue exit:

```text
Pr_fatigue_exit_i =
sigmoid(
  -1.60
  + 2.20 * f_i
  + 0.90 * repetition_signal
  + 0.70 * unresolved_grievance
  - 0.80 * new_information_signal
)
```

The source model defines cooling exit:

```text
Pr_cooling_exit_i =
sigmoid(
  -1.40
  + 1.50 * resolution_signal
  + 0.90 * fatigue_i
  - 0.80 * controversy
  - 0.60 * new_trigger
)
```

These are exit / withdrawal proxies for a cluster state. They are not individual churn predictions.

### F.14 Reactivation Potential

The source model defines:

```text
Pr_reactivate_i =
sigmoid(
  -2.00
  + 1.40 * reputation_memory
  + 1.20 * new_trigger
  + 1.00 * unresolved_grievance
  + 0.60 * identity_relevance_proxy
  - 1.10 * fatigue_i
  - 0.70 * resolution_signal
)
```

Reactivation is a historical replay proxy, not prediction.

`identity_relevance_proxy` is an aggregate narrative relevance proxy only. It must not use real identity matching.

### F.15 Camp Labels

The source model defines:

- `support`
- `neutral_or_uncertain`
- `oppose`
- `mixed`
- `exited_or_fatigued`

Future implementation may emit these labels only as aggregate state labels.

## G. Missing Data Policy

Future 8P-5 should use this missing-data policy:

- missing `people_cluster_refs`: allow `aggregate_ids` / `echo_box_ids` fallback if safe; add warning
- missing `aggregate_ids`: allow evidence / echo box association fallback if safe; warn
- missing `echo_box_ids`: allow PeopleCluster scoring from evidence / aggregate only with warning
- missing `previous_state`: output current-state-only or `transition_low_confidence` warning
- missing `stance_distribution`: derive from associated safe evidence `stance_hint` if possible; otherwise emit insufficient-data warning
- missing `stance_confidence`: use low confidence default or warning
- missing attention / fatigue / expression hints: use safe deterministic neutral policy or re-normalize with warning
- rejected evidence: exclude from analysis-ready scoring and count in warning
- low-trust evidence: lower confidence and raise review / uncertainty warnings
- duplicate evidence: fold; `duplicate_count` may contribute only bounded repetition / activity signal
- unknown `cluster_role` / `cluster_type`: use `unknown_people_cluster` and add warning
- high heat alone: does not imply stance change
- high closure alone: does not imply private belief or permanent polarization
- no evidence for cluster: insufficient-data warning and no strong transition

Missing data must never become strong evidence by accident.

## H. Future Minimal Output

Future `PeopleClusterStateV01` output shape:

```text
schema = sentigraph_people_cluster_state_v0_1
cluster_id
cluster_role
cluster_type
model_status = 8P_5_peoplecluster_transition
coefficient_source = mock_default
calibration_status = uncalibrated
empirical_validation = not_started
sample_scope = selected_sample_or_local_fixture_only
```

Evidence mass:

- `evidence_count`
- `analysis_ready_evidence_count`
- `rejected_excluded_count`
- `duplicate_group_count`
- `low_trust_count`
- `review_needed_count`
- `associated_aggregate_count`
- `associated_influence_core_count`
- `associated_echo_box_count`

State:

- `stance_score`
- `stance_label`
- `stance_distribution`
- `stance_confidence`
- `attention_level`
- `fatigue_level`
- `expression_intensity`
- `exit_risk`
- `reactivation_potential`
- `openness_score` if defined by existing model doc
- `transition_pressure` if defined by existing model doc

Components:

- `stance_components`
- `confidence_components`
- `attention_components`
- `fatigue_components`
- `expression_components`
- `exit_risk_components`
- `reactivation_components`
- `associated_aggregate_ids_used`
- `associated_influence_core_ids_used`
- `associated_echo_box_ids_used`
- `associated_evidence_ids_used`

Quality flags:

- `selected_sample_only`
- `uncalibrated`
- `mock_default_coefficients`
- `evidence_not_truth`
- `anonymous_aggregate_only`
- `not_real_person`
- `not_psychological_profile`
- `not_individual_tracking`

Warnings:

- `low_confidence_warnings`
- `low_trust_warnings`
- `review_needed_warnings`
- `duplicate_folded_warnings`
- `rejected_excluded_warnings`
- `missing_component_warnings`
- `insufficient_data_warnings`
- `unknown_people_cluster_warnings`
- `model_card_warnings`
- `overclaim_warnings`

Explanation:

- short deterministic human-readable explanation strings

Boundary flags:

```text
anonymous_aggregate_only = true
not_real_person = true
not_real_account = true
not_psychological_profile = true
not_personality_diagnosis = true
not_individual_tracking = true
not_target_user_list = true
not_persuasion_probability = true
not_causal_proof = true
not_prediction = true
evidence_not_truth = true
human_review_required = true
```

Do not include:

- `real_hotlist_score`
- `truth_score`
- `official_verified`
- `causal_chain_confirmed`
- `prediction_probability`
- `persuasion_score`
- `target_user_list`
- `raw_author_identifiers`
- `raw_author_id`
- `author_id`
- `author_name`
- `profile_url`
- `real_account_id`
- `cross_platform_identity`
- `psychological_profile`
- `personality_diagnosis`
- `pull_ik`
- `stance_effect_ik`
- `stance_effect_ik_adjusted`
- `InfluenceCoreToClusterEffectV01`
- `ResponseStrategyComparisonV01`

## I. Integration With 8P-1 / 8P-2 / 8P-3 / 8P-4 Run Object

Future `calculate_opinion_ecosystem_mock_fixture` should:

- validate fixture with existing 8P-1 validator first
- if blocked: do not calculate ContentAggregate, InfluenceCore, EchoBox, or PeopleCluster
- if manual-review-required due unknown future platform: either do not calculate or calculate only with explicit warning; never imply provider runnable
- if metadata-ready: calculate ContentAggregate, InfluenceCore, EchoBox, and PeopleCluster
- preserve all 8P-1 boundary flags
- preserve runtime side-effect flags all false
- keep ContentAggregate output from 8P-2
- keep InfluenceCore output from 8P-3
- keep EchoBox output from 8P-4
- set `module_outputs.content_aggregate` to a list of `ContentAggregateWeightV01` outputs
- set `module_outputs.influence_core` to a list of `InfluenceCoreWeightV01` outputs
- set `module_outputs.echo_box` to a list of `EchoBoxWeightV01` outputs
- set `module_outputs.people_cluster` to a list of `PeopleClusterStateV01` outputs
- set `module_outputs.response_strategy` to `not_calculated_in_8P_5`

Do not add API routes.
Do not add frontend UI.
Do not write runtime files.

## J. Future Tests List

Future 8P-5 tests should include:

- `test_peoplecluster_minimal_fixture_calculates_state_v0_1`
- `test_peoplecluster_output_is_anonymous_aggregate_only`
- `test_high_heat_does_not_imply_all_people_changed_stance`
- `test_high_echobox_closure_can_raise_fatigue_without_personal_claim`
- `test_bridgeable_mixed_cluster_has_reactivation_or_openness_potential_without_persuasion_claim`
- `test_missing_previous_state_yields_current_state_only_warning`
- `test_low_trust_evidence_lowers_peoplecluster_confidence`
- `test_rejected_evidence_excluded_from_peoplecluster_scores`
- `test_duplicate_evidence_folded_not_linear_attention`
- `test_unknown_peoplecluster_role_uses_unknown_warning`
- `test_forbidden_fields_still_block_before_peoplecluster_scoring`
- `test_overclaim_fields_still_block_before_peoplecluster_scoring`
- `test_auto_execute_still_blocks_before_peoplecluster_scoring`
- `test_future_unknown_platform_does_not_imply_provider_runnable`
- `test_contentaggregate_influencecore_echobox_outputs_preserved_in_8P_5`
- `test_no_response_strategy_scores_in_8P_5`
- `test_no_pull_or_stance_effect_in_8P_5`
- `test_no_target_user_list_or_real_identity_output`
- `test_no_psychological_profile_or_personality_diagnosis_output`
- `test_no_forbidden_output_fields_after_peoplecluster_scoring`
- `test_deterministic_same_fixture_same_output_after_peoplecluster_scoring`
- `test_no_real_io_or_runtime_side_effects_by_design`

## K. Not Allowed In 8P-5 Implementation

Future 8P-5 implementation must not include:

- ResponseStrategy scoring
- per-cluster InfluenceCore pull
- `pull_ik`
- `stance_effect_ik`
- `stance_effect_ik_adjusted`
- `InfluenceCoreToClusterEffectV01`
- individual persuasion score
- target user list
- real user / account identity
- cross-platform person matching
- psychological profiling
- personality diagnosis
- frontend UI
- API route
- backend schema unless absolutely necessary
- runtime persistence
- filesystem read / write except optional safe source scan inside tests if needed
- collector
- `evidence_items` parsing
- Evidence Layer write
- production case
- `analysis_run`
- B-end report runtime
- Sandbox / public event runtime
- real API
- real LLM
- `auto_execute`
- `persuasion_score`
- `prediction_probability`
- `truth_score`
- `official_verified` output

## L. Next Slices Only After 8P-5 Passes

Only after 8P-5 passes targeted validation should later slices be considered:

- 8P-6 ResponseStrategy comparison only
- 8Q frontend explanatory UI only after backend/local calculator and model-card QA are stable
- 8R model-card QA / screenshot smoke
- later calibration after historical replay dataset and human review comparison

Those later slices must continue to preserve selected-sample boundaries, evidence-not-truth boundaries, no real API / LLM behavior, no collector access, no Evidence Layer write, no production case, and no individual targeting.
