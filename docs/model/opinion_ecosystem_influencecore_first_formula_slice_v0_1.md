# Opinion Ecosystem InfluenceCore First Formula Slice v0.1

Status: docs-only first formula slice plan. This document does not implement formulas, backend code, backend tests, frontend UI, API routes, schemas, runtime persistence, file IO, product behavior, analysis, report generation, Sandbox generation, public event generation, provider execution, collector execution, real API calls, real LLM calls, or Evidence Layer writes.

## A. First Formula Slice Name

Phase 8P-3 InfluenceCore Formula Calculator.

## B. Purpose

Future 8P-3 implementation should calculate only `InfluenceCoreWeightV01` using local synthetic in-memory fixtures that already passed 8P-1 validation and can coexist with 8P-2 ContentAggregate outputs.

The goal is to add the smallest standalone InfluenceCore formula module while preserving all 8P-1 governance boundaries and all 8P-2 ContentAggregate behavior.

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

- `get_source_identity_weight(core)`
- `calculate_factual_credibility(core, evidence_items)`
- `calculate_narrative_resonance(core, evidence_items)`
- `calculate_sample_exposure(core, evidence_items)`
- `calculate_bridge_potential(core, evidence_items)`
- `calculate_backlash_risk(core, evidence_items)`
- `calculate_core_strength(core, evidence_items)`
- `calculate_attention_amplification(core, evidence_items)`
- `calculate_influencecore_weight(core, evidence_items)`
- `calculate_all_influencecore_weights(fixture)`

All functions should remain deterministic and should operate only on in-memory synthetic fixture dicts.

## E. Input Assumptions

Future 8P-3 may use only safe metadata from:

- `evidence_items_safe`
- `influence_cores`
- `fixture_metadata`
- optionally ContentAggregate output context from 8P-2, but the first implementation should not require it

Allowed InfluenceCore fields:

- `core_id`
- `core_type`
- `frame_direction`
- `associated_evidence_ids`
- `source_identity_hint`
- `clarity_hint`
- `novelty_hint`
- `bridge_hint`
- `backlash_hint`
- `emotional_charge_hint`
- `repetition_hint`
- `resolution_signal_hint`
- `source_transparency_hint`
- `cross_source_consistency_hint`
- `privacy_safety_pass`
- `risk_flags`

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

## F. Formula Scope

Future 8P-3 should implement the following 8N-g formulas only where they are standalone and do not require PeopleCluster.

### Core Types

Allowed core types:

- `official_statement`
- `media_report`
- `expert_explanation`
- `kol_creator_content`
- `ordinary_viral_content`
- `forum_thread`
- `community_comment_cluster`
- `meme_deconstruction`
- `faq_or_longform_explanation`
- `correction_or_apology`
- `progress_update`
- `third_party_context`
- `low_trust_claim`
- `unknown_source_core`

Implementation may also map these aliases:

- `recognized_media_report` -> `media_report`
- `known_org_or_institution` -> `expert_explanation` or a documented source identity weight of 0.70

### Default Source Identity Weight

| Source identity | weight |
| --- | ---: |
| official_statement | 0.95 |
| recognized_media_report | 0.78 |
| media_report | 0.78 |
| expert_explanation | 0.72 |
| known_org_or_institution | 0.70 |
| kol_creator_content | 0.58 |
| ordinary_viral_content | 0.45 |
| forum_thread | 0.42 |
| community_comment_cluster | 0.38 |
| meme_deconstruction | 0.30 |
| unknown_source_core | 0.25 |
| low_trust_claim | 0.15 |

### Factual Credibility

```text
fc_k =
  0.28 * source_identity_weight
+ 0.24 * evidence_trust_mean
+ 0.18 * review_quality
+ 0.14 * source_transparency
+ 0.10 * cross_source_consistency
+ 0.06 * privacy_safety_pass
- penalty_k
```

Factual credibility is selected-sample evidence credibility. It is not official verification, not truth, and not causal proof.

### Narrative Resonance

```text
nr_k =
  0.22 * clarity_score
+ 0.20 * emotional_charge
+ 0.18 * repetition_signal
+ 0.15 * novelty_score
+ 0.15 * identity_or_group_relevance_proxy
+ 0.10 * meme_or_symbolic_density
```

### Sample Exposure

```text
ex_k =
  0.35 * log_norm(weighted_mentions_k, mention_cap)
+ 0.20 * log_norm(weighted_replies_k, reply_cap)
+ 0.15 * log_norm(weighted_shares_or_reposts_k, share_cap)
+ 0.15 * platform_spread_k
+ 0.15 * source_spread_k
```

Sample exposure is selected-sample exposure. It is not full-web coverage and not full-platform coverage.

### Bridge Potential

```text
br_k =
  0.25 * cross_platform_presence
+ 0.20 * neutral_or_explanatory_frame
+ 0.20 * source_credibility_across_camps
+ 0.15 * low_identity_threat_language
+ 0.10 * shared_value_language
+ 0.10 * media_or_third_party_relay
```

### Backlash Risk

```text
bk_k =
  0.22 * mismatch_with_cluster_concerns
+ 0.18 * perceived_defensiveness
+ 0.16 * timing_lag
+ 0.14 * low_empathy_language
+ 0.12 * contradiction_with_prior_record
+ 0.10 * high_identity_threat
+ 0.08 * ambiguity_or_missing_detail
```

### Core Strength

```text
core_strength_k =
  0.24 * fc_k
+ 0.22 * nr_k
+ 0.18 * ex_k
+ 0.14 * clarity_score
+ 0.12 * novelty_score
+ 0.10 * br_k
```

### Attention Amplification

```text
attention_amplification_k =
  0.24 * ex_k
+ 0.20 * nr_k
+ 0.18 * emotional_charge
+ 0.16 * novelty_score
+ 0.12 * repetition_signal
+ 0.10 * br_k
```

### Amplification

```text
amp_k =
  0.25 * attention_amplification_k
+ 0.20 * ex_k
+ 0.18 * repetition_signal
+ 0.15 * br_k
+ 0.12 * novelty_score
+ 0.10 * emotional_charge
```

### Credibility-Adjusted Influence

```text
credibility_adjusted_influence_score =
  amp_k * (0.55 + 0.45 * fc_k)
```

This score should be described as core-level influence potential in a selected sample. It is not persuasion probability and not PeopleCluster stance movement.

### De-Escalation

```text
deescalation_potential_k =
  0.24 * fc_k
+ 0.22 * clarity_score
+ 0.20 * resolution_signal
+ 0.16 * br_k
+ 0.10 * empathy_or_context
+ 0.08 * low_identity_threat_language
- 0.20 * bk_k
```

### Core Risk

```text
core_risk_k =
  0.20 * amp_k
+ 0.18 * bk_k
+ 0.16 * emotional_charge
+ 0.14 * low_trust_conflict
+ 0.12 * privacy_or_sensitivity_risk
+ 0.10 * contradiction_risk
+ 0.10 * unresolved_grievance
```

### Deferred Formulas

Do not implement in 8P-3:

- `impact_gate_ik`
- `pull_ik`
- `stance_effect_ik`
- `stance_effect_ik_adjusted`
- `InfluenceCoreToClusterEffectV01`

These require PeopleCluster and should be deferred.

## G. Missing Data Policy

Future 8P-3 should use this missing-data policy:

- missing `clarity_hint`: use a neutral documented default or mark `missing_component` warning
- missing `novelty_hint`: mark unavailable or use neutral only if explicitly documented
- missing `bridge_hint`: mark unavailable or use safe default with warning
- missing `backlash_hint`: mark unavailable or use safe default with warning
- missing associated evidence: add `insufficient_data` warning and do not emit a strong score
- low trust evidence: lower factual credibility and raise core risk
- rejected evidence: exclude from analysis-ready scoring and count in warning
- unknown `core_type`: use `unknown_source_core` and add warning
- `low_trust_claim`: use low source identity weight and never treat it as truth or official verification
- official_statement with low exposure: high credibility can coexist with low amplification

Missing data must not become zero by accident unless a formula explicitly documents zero as the conservative value.

## H. Future Minimal Output

Future `InfluenceCoreWeightV01` output shape:

```json
{
  "schema": "sentigraph_influencecore_weight_v0_1",
  "core_id": "core_example",
  "core_type": "unknown_source_core",
  "model_status": "8P_3_influencecore_local_formula",
  "coefficient_source": "mock_default",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "sample_scope": "selected_sample_only",
  "evidence_mass": {},
  "scores": {
    "factual_credibility": 0.0,
    "narrative_resonance": 0.0,
    "sample_exposure": 0.0,
    "bridge_potential": 0.0,
    "backlash_risk": 0.0,
    "core_strength": 0.0,
    "attention_amplification": 0.0,
    "amplification_score": 0.0,
    "credibility_adjusted_influence_score": 0.0,
    "deescalation_potential": 0.0,
    "core_risk": 0.0
  },
  "components": {},
  "quality_flags": [],
  "warnings": [],
  "explanation": [],
  "boundary_flags": {
    "not_official_verification": true,
    "not_truth_score": true,
    "not_causal_proof": true,
    "not_prediction": true,
    "not_persuasion_probability": true,
    "not_people_cluster": true,
    "not_real_person": true,
    "evidence_not_truth": true,
    "human_review_required": true
  }
}
```

This is a future output contract only. It is not implemented by this document.

## I. Integration With 8P-1 / 8P-2 Run Object

Future `calculate_opinion_ecosystem_mock_fixture` should:

- validate fixture with the existing 8P-1 validator first
- if blocked, not calculate InfluenceCore
- if `manual_review_required` due unknown or future platform, either not calculate or calculate only with warning
- never imply any provider is runnable
- if `metadata_ready`, calculate ContentAggregate and InfluenceCore
- preserve all 8P-1 boundary flags
- preserve runtime side-effect flags all false
- keep ContentAggregate output from 8P-2
- set module outputs:
  - `content_aggregate`: list of `ContentAggregateWeightV01` outputs
  - `influence_core`: list of `InfluenceCoreWeightV01` outputs
  - `echo_box`: `not_calculated_in_8P_3`
  - `people_cluster`: `not_calculated_in_8P_3`
  - `response_strategy`: `not_calculated_in_8P_3`

Do not add API routes.
Do not add frontend UI.
Do not write runtime files.

## J. Future Tests List

Future 8P-3 tests should include:

- `test_influencecore_minimal_fixture_calculates_weight_v0_1`
- `test_official_statement_credible_but_low_exposure`
- `test_viral_meme_low_credibility_high_amplification_warning`
- `test_low_trust_claim_raises_core_risk_but_not_truth`
- `test_third_party_explanation_can_have_bridge_and_deescalation_potential`
- `test_unknown_core_type_uses_unknown_source_core_warning`
- `test_rejected_evidence_excluded_from_influencecore_scores`
- `test_missing_associated_evidence_yields_insufficient_data_warning`
- `test_forbidden_fields_still_block_before_influencecore_scoring`
- `test_overclaim_fields_still_block_before_influencecore_scoring`
- `test_auto_execute_still_blocks_before_influencecore_scoring`
- `test_future_unknown_platform_does_not_imply_provider_runnable`
- `test_no_echobox_peoplecluster_response_strategy_scores_in_8P_3`
- `test_no_peoplecluster_pull_or_stance_effect_in_8P_3`
- `test_no_forbidden_output_fields_after_influencecore_scoring`
- `test_deterministic_same_fixture_same_output_after_influencecore_scoring`
- `test_no_real_io_or_runtime_side_effects_by_design`

Do not implement these tests in this docs-only phase.

## K. Not Allowed In 8P-3 Implementation

Future 8P-3 implementation must not include:

- EchoBox scoring
- PeopleCluster transition
- ResponseStrategy scoring
- per-cluster InfluenceCore pull
- stance effect
- frontend UI
- API route
- backend schema unless absolutely necessary
- runtime persistence
- filesystem read/write except optional safe source scan inside tests if needed
- collector access
- `evidence_items.jsonl` parsing
- `evidence_items.csv` parsing
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

## L. Next Slices Only After 8P-3 Passes

Only after 8P-3 passes targeted validation should later slices be considered:

- 8P-4 EchoBox formula only
- 8P-5 PeopleCluster transition only
- 8P-6 ResponseStrategy comparison only
- 8Q frontend explanatory UI only after backend/local calculator and model-card QA are stable
- 8R model card QA / screenshot smoke
- later calibration after historical replay dataset and human review comparison

Each later slice must preserve selected-sample scope, uncalibrated metadata, human review, and all no-real-API/no-real-LLM/no-collector/no-public-action boundaries.
