# Opinion Ecosystem EchoBox First Formula Slice v0.1

Status: docs-only first formula slice plan. This document does not implement formulas, backend code, backend tests, frontend UI, API routes, schemas, runtime persistence, file IO, product behavior, graph extraction, analysis, report generation, Sandbox generation, public event generation, provider execution, collector execution, real API calls, real LLM calls, or Evidence Layer writes.

## A. First Formula Slice Name

Phase 8P-4 EchoBox Formula Calculator.

## B. Purpose

Future 8P-4 implementation should calculate only `EchoBoxWeightV01` using local synthetic in-memory fixtures that already passed 8P-1 validation and can coexist with 8P-2 ContentAggregate outputs and 8P-3 InfluenceCore outputs.

The goal is to add the smallest standalone EchoBox formula module while preserving all 8P-1 governance boundaries, all 8P-2 ContentAggregate behavior, and all 8P-3 InfluenceCore behavior.

## C. Expected Future Code Scope If Approved Later

Likely update only:

- `backend/app/services/opinion_ecosystem_mock_calculator.py`
- `backend/app/tests/test_opinion_ecosystem_mock_calculator.py`

Do not add:

- API routes
- frontend UI
- runtime persistence
- package files
- schema files, unless a later implementation proves plain dict contracts are insufficient

## D. Future Pure Function Candidates

Future pure function candidates:

- `get_echobox_associated_evidence(echo_box, evidence_items)`
- `get_echobox_content_aggregate_refs(echo_box, content_aggregate_outputs)`
- `get_echobox_influence_core_refs(echo_box, influence_core_outputs)`
- `calculate_echobox_saturation(echo_box, evidence_items, content_aggregates)`
- `calculate_echobox_closure(echo_box, evidence_items, content_aggregates, influence_cores)`
- `calculate_echobox_bridge_capacity(echo_box, evidence_items, content_aggregates, influence_cores)`
- `calculate_echobox_constructive_breakout(echo_box, evidence_items, content_aggregates, influence_cores)`
- `calculate_echobox_risk_breakout(echo_box, evidence_items, content_aggregates, influence_cores)`
- `calculate_echobox_risk(echo_box, evidence_items, content_aggregates, influence_cores)`
- `calculate_echobox_weight(echo_box, evidence_items, content_aggregate_outputs, influence_core_outputs)`
- `calculate_all_echobox_weights(fixture, content_aggregate_outputs, influence_core_outputs)`

All functions should remain deterministic and should operate only on in-memory synthetic fixture dicts.

## E. Input Assumptions

Future 8P-4 may use only safe metadata from:

- `fixture_metadata`
- `evidence_items_safe`
- `content_aggregates`
- `influence_cores`
- `echo_boxes`
- `ContentAggregateWeightV01` output from 8P-2 if already available
- `InfluenceCoreWeightV01` output from 8P-3 if already available

Allowed EchoBox fields:

- `echo_box_id`
- `echo_box_role`
- `platform_refs`
- `aggregate_ids`
- `influence_core_ids`
- `people_cluster_ids` as opaque anonymous aggregate IDs only, not as cluster state
- `stance_distribution`
- `interaction_proxy_summary`
- `cross_cutting_proxy_summary`
- `platform_spread_hint`
- `source_spread_hint`
- `saturation_hint`
- `closure_hint`
- `bridge_hint`
- `cross_box_exposure_hint`
- `neutral_or_explanatory_frame_hint`
- `shared_value_language_hint`
- `moderation_context_hint`
- `sealed_discussion_hint`
- `constructive_breakout_hint`
- `risk_breakout_hint`
- `attention_concentration_hint`
- `repetition_hint`
- `low_trust_share_hint`
- `review_needed_share_hint`
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
- `echo_box_refs` if present
- `created_at_bucket`
- `relative_stage_bucket`

No full text is required.

Not required and not allowed:

- raw author fields
- profile URLs
- private messages
- cookies
- tokens
- sessions
- browser profile data
- localStorage
- secrets
- real package rows
- collector output
- real community graph
- real account graph
- target user list

## F. Formula Scope

Future 8P-4 should use `docs/model/echobox_structure_model_v0_1.md` as the formula source of truth.

The first implementation slice must be standalone `EchoBoxWeightV01` only.

### Core Variables

The source EchoBox structure model defines these variables:

- `stance_concentration`
- `stance_entropy`
- `internal_density`
- `cross_cutting_exposure`
- `cross_box_exposure`
- `repetition`
- `emotion`
- `core_dominance`
- `bridge_capacity`
- `saturation`
- `closure`
- `constructive_breakout`
- `risk_breakout`
- `echo_risk`

### Stance Entropy

```text
stance_entropy_b = - sum_i(p_i * log(p_i)) / log(k)
```

The source model defines this formula, but the first 8P-4 score output list does not require a standalone `stance_entropy` score. If a future implementation uses it as a component, it must preserve this exact definition.

### Stance Concentration

```text
stance_concentration_b =
  max(p_support_b, p_neutral_b, p_oppose_b, p_mixed_b)
* (1 - p_unknown_b)
```

### Saturation

```text
saturation_b =
  0.24 * stance_concentration_b
+ 0.20 * repetition_b
+ 0.18 * internal_density_b
+ 0.16 * core_dominance_b
+ 0.12 * emotion_b
+ 0.10 * (1 - cross_cutting_exposure_b)
```

Confidence-adjusted saturation:

```text
saturation_conf_adjusted_b =
  saturation_b * (0.65 + 0.35 * Q_b)
```

`Q_b` must be derived from already-safe evidence confidence context or an explicitly documented safe proxy. If no safe confidence source exists, future implementation must mark `implementation_requires_formula_confirmation_from_echobox_structure_model_v0_1` rather than inventing a new confidence formula.

### Closure

```text
closure_b =
  0.30 * (1 - cross_cutting_exposure_b)
+ 0.25 * (1 - cross_box_exposure_b)
+ 0.20 * stance_concentration_b
+ 0.15 * internal_density_b
+ 0.10 * (1 - bridge_capacity_b)
```

### Bridge Capacity

```text
bridge_capacity_b =
  0.22 * bridge_cluster_share_b
+ 0.20 * bridge_core_share_b
+ 0.16 * neutral_or_mixed_cluster_share_b
+ 0.14 * explanatory_core_share_b
+ 0.12 * cross_cutting_exposure_b
+ 0.10 * low_identity_threat_language_b
+ 0.06 * evidence_confidence_b
```

`bridge_cluster_share_b` and `neutral_or_mixed_cluster_share_b` reference cluster-level concepts. In 8P-4 they may be used only if the fixture provides safe aggregate hints. They must not trigger PeopleCluster transition scoring. If safe hints do not exist, future implementation must warn or mark `implementation_requires_formula_confirmation_from_echobox_structure_model_v0_1`.

### Constructive Breakout

```text
constructive_breakout_b =
  0.24 * bridge_capacity_b
+ 0.20 * deescalation_core_share_b
+ 0.16 * evidence_confidence_b
+ 0.14 * clarity_mean_b
+ 0.12 * cross_box_exposure_b
+ 0.08 * media_or_third_party_relay_b
+ 0.06 * novelty_constructive_b
```

### Risk Breakout

```text
risk_breakout_b =
  0.22 * emotion_b
+ 0.20 * controversy_b
+ 0.16 * observed_amplification_mean_b
+ 0.14 * backlash_risk_mean_b
+ 0.12 * low_trust_conflict_b
+ 0.10 * platform_spread_b
+ 0.06 * repetition_b
```

### Echo Risk

```text
echo_risk_b =
  0.20 * saturation_b
+ 0.18 * closure_b
+ 0.16 * risk_breakout_b
+ 0.14 * controversy_b
+ 0.12 * emotion_b
+ 0.10 * low_trust_conflict_b
+ 0.10 * review_risk_b
```

### Deferred Formulas And Outputs

Do not implement in 8P-4:

- PeopleCluster transition formulas
- ResponseStrategy formulas
- `pull_ik`
- `stance_effect_ik`
- `stance_effect_ik_adjusted`
- `InfluenceCoreToClusterEffectV01`
- `PeopleClusterStateV01`
- `ResponseStrategyComparisonV01`

## G. Missing Data Policy

Future 8P-4 should use this missing-data policy:

- missing `echo_box_refs`: allow `aggregate_ids` / `platform_refs` fallback if safe; add warning
- missing `aggregate_ids`: add `insufficient_data` warning and do not emit a strong score
- missing `influence_core_ids`: allow EchoBox scoring from aggregate/evidence only with warning
- missing `stance_distribution`: closure and bridge outputs should downgrade or warn
- missing `cross_cutting_proxy_summary`: bridge capacity should not be invented; warn or use safe neutral default
- missing platform/source spread: use safe evidence-derived proxy if available; otherwise warn
- rejected evidence: exclude from analysis-ready scoring and count in warning
- low-trust evidence: lower confidence and can raise echo risk
- duplicate evidence: fold duplicates; `duplicate_count` may contribute only bounded repetition signal
- unknown `echo_box_role`: use `unknown_echo_box` and add warning
- strong one-sided heat: does not automatically mean echo chamber
- no evidence for echo box: add `insufficient_data` warning and do not emit a strong score

Missing data must not become strong evidence by accident. If the EchoBox source model lacks enough detail for a component derivation, future implementation must mark `implementation_requires_formula_confirmation_from_echobox_structure_model_v0_1`.

## H. Future Minimal Output

Future `EchoBoxWeightV01` output shape:

```json
{
  "schema": "sentigraph_echo_box_weight_v0_1",
  "echo_box_id": "echo_box_example",
  "echo_box_role": "mixed_discussion_box",
  "model_status": "8P_4_echobox_formula",
  "coefficient_source": "mock_default",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "sample_scope": "selected_sample_or_local_fixture_only",
  "evidence_mass": {
    "evidence_count": 0,
    "analysis_ready_evidence_count": 0,
    "rejected_excluded_count": 0,
    "duplicate_group_count": 0,
    "low_trust_count": 0,
    "review_needed_count": 0,
    "associated_aggregate_count": 0,
    "associated_influence_core_count": 0
  },
  "scores": {
    "saturation_score": 0.0,
    "closure_score": 0.0,
    "bridge_capacity_score": 0.0,
    "constructive_breakout_score": 0.0,
    "risk_breakout_score": 0.0,
    "echo_risk_score": 0.0
  },
  "components": {
    "saturation_components": {},
    "closure_components": {},
    "bridge_capacity_components": {},
    "constructive_breakout_components": {},
    "risk_breakout_components": {},
    "echo_risk_components": {},
    "stance_distribution": {},
    "platform_spread": 0.0,
    "source_spread": 0.0,
    "cross_cutting_proxy_summary": {},
    "associated_aggregate_ids_used": [],
    "associated_influence_core_ids_used": []
  },
  "quality_flags": [
    "selected_sample_only",
    "uncalibrated",
    "mock_default_coefficients",
    "evidence_not_truth",
    "not_real_community_map",
    "not_full_graph",
    "not_full_platform"
  ],
  "warnings": {
    "low_confidence_warnings": [],
    "low_trust_warnings": [],
    "review_needed_warnings": [],
    "duplicate_folded_warnings": [],
    "rejected_excluded_warnings": [],
    "missing_component_warnings": [],
    "insufficient_data_warnings": [],
    "unknown_echo_box_role_warnings": [],
    "model_card_warnings": [],
    "overclaim_warnings": []
  },
  "explanation": [],
  "boundary_flags": {
    "not_real_community_map": true,
    "not_full_graph": true,
    "not_full_platform": true,
    "not_official_verification": true,
    "not_causal_proof": true,
    "not_prediction": true,
    "not_individual_tracking": true,
    "not_target_user_list": true,
    "evidence_not_truth": true,
    "human_review_required": true
  }
}
```

This is a future output contract only. It is not implemented by this document.

Forbidden output fields:

- `real_hotlist_score`
- `truth_score`
- `official_verified`
- `causal_chain_confirmed`
- `prediction_probability`
- `persuasion_score`
- `target_user_list`
- `raw_author_identifiers`
- `real_community_map`
- `full_social_graph`
- `pull_ik`
- `stance_effect_ik`
- `stance_effect_ik_adjusted`
- `InfluenceCoreToClusterEffectV01`
- `PeopleClusterStateV01`
- `ResponseStrategyComparisonV01`

## I. Integration With 8P-1 / 8P-2 / 8P-3 Run Object

Future `calculate_opinion_ecosystem_mock_fixture` should:

- validate fixture with the existing 8P-1 validator first
- if blocked, not calculate ContentAggregate, InfluenceCore, or EchoBox
- if `manual_review_required` due unknown or future platform, either not calculate or calculate only with explicit warning
- never imply any provider is runnable
- if `metadata_ready`, calculate ContentAggregate, InfluenceCore, and EchoBox
- preserve all 8P-1 boundary flags
- preserve runtime side-effect flags all false
- keep ContentAggregate output from 8P-2
- keep InfluenceCore output from 8P-3
- set module outputs:
  - `content_aggregate`: list of `ContentAggregateWeightV01` outputs
  - `influence_core`: list of `InfluenceCoreWeightV01` outputs
  - `echo_box`: list of `EchoBoxWeightV01` outputs
  - `people_cluster`: `not_calculated_in_8P_4`
  - `response_strategy`: `not_calculated_in_8P_4`

Do not add API routes.
Do not add frontend UI.
Do not write runtime files.

## J. Future Tests List

Future 8P-4 tests should include:

- `test_echobox_minimal_fixture_calculates_weight_v0_1`
- `test_strong_echo_no_breakout_high_closure_low_breakout`
- `test_bridgeable_controversy_has_bridge_capacity`
- `test_sealed_echo_box_has_high_closure_low_bridge_capacity`
- `test_low_trust_evidence_lowers_echobox_confidence_and_raises_warning`
- `test_duplicate_evidence_folded_not_linear_saturation`
- `test_one_sided_high_heat_does_not_automatically_mean_echo_chamber`
- `test_unknown_echobox_role_uses_unknown_warning`
- `test_missing_aggregate_or_evidence_yields_insufficient_data_warning`
- `test_rejected_evidence_excluded_from_echobox_scores`
- `test_forbidden_fields_still_block_before_echobox_scoring`
- `test_overclaim_fields_still_block_before_echobox_scoring`
- `test_auto_execute_still_blocks_before_echobox_scoring`
- `test_future_unknown_platform_does_not_imply_provider_runnable`
- `test_contentaggregate_and_influencecore_outputs_preserved_in_8P_4`
- `test_no_peoplecluster_response_strategy_scores_in_8P_4`
- `test_no_pull_or_stance_effect_in_8P_4`
- `test_no_real_community_map_or_full_graph_output`
- `test_no_forbidden_output_fields_after_echobox_scoring`
- `test_deterministic_same_fixture_same_output_after_echobox_scoring`
- `test_no_real_io_or_runtime_side_effects_by_design`

Do not implement these tests in this docs-only phase.

## K. Not Allowed In 8P-4 Implementation

Future 8P-4 implementation must not include:

- PeopleCluster transition
- ResponseStrategy scoring
- per-cluster InfluenceCore pull
- stance effect
- real community graph extraction
- real full graph
- target user list
- frontend UI
- API route
- backend schema unless absolutely necessary
- runtime persistence
- filesystem read/write except optional safe source scan inside tests if needed
- collector access
- `evidence_items` parsing
- Evidence Layer write
- production case creation
- analysis_run creation
- B-end report runtime
- Sandbox runtime
- public event runtime
- real API calls
- real LLM calls
- auto execution
- `persuasion_score`
- `prediction_probability`
- `truth_score`
- `official_verified` output

## L. Next Slices Only After 8P-4 Passes

Only after 8P-4 passes targeted validation should later slices be considered:

- 8P-5 PeopleCluster transition only
- 8P-6 ResponseStrategy comparison only
- 8Q frontend explanatory UI only after backend/local calculator and model-card QA are stable
- 8R model card QA / screenshot smoke
- later calibration after historical replay dataset and human review comparison

Each later slice must preserve selected-sample scope, uncalibrated metadata, human review, and all no-real-API/no-real-LLM/no-collector/no-public-action boundaries.
