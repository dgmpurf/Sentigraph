# Opinion Ecosystem ResponseStrategy First Comparison Slice v0.1

Status: docs-only first comparison slice plan. This document does not implement formulas, backend code, backend tests, frontend UI, API routes, schemas, runtime persistence, file IO, product behavior, analysis, report generation, Sandbox generation, public event generation, provider execution, collector execution, real API calls, real LLM calls, Evidence Layer writes, public posting, or generated public response text.

## A. Slice Name

Phase 8P-6 ResponseStrategy Comparison Calculator.

## B. Purpose

A future implementation may calculate only `ResponseStrategyComparisonV01` from local synthetic in-memory fixture metadata and already calculated 8P-2 through 8P-5 outputs.

It compares explicit strategy candidates for human review only.

It is:

- deterministic
- local
- selected-sample-only
- mock-default
- uncalibrated
- non-causal
- non-predictive
- non-executable
- human-review-only

It is not:

- an auto-execution engine
- an automated PR decision
- a guarantee of public reaction
- a causal-effect predictor
- a public-opinion control tool
- a covert influence optimizer
- a persuasion system
- an individual-targeting system
- a fake-consensus or astroturfing system
- a content-posting or account-operation system

## C. Expected Future Code Scope

Likely future update scope:

- `backend/app/services/opinion_ecosystem_mock_calculator.py`
- `backend/app/tests/test_opinion_ecosystem_mock_calculator.py`

Do not add:

- API routes
- frontend UI
- runtime persistence
- backend schemas unless absolutely necessary
- response generation modules
- posting / execution modules
- package files

## D. Future Pure Function Candidates

Future implementation may add small pure functions:

- `get_response_strategy_candidate(candidate)`
- `validate_response_strategy_candidate(candidate)`
- `calculate_strategy_evidence_fit(candidate, upstream_outputs)`
- `calculate_strategy_timing_fit(candidate, upstream_outputs)`
- `calculate_strategy_clarity_gain(candidate, upstream_outputs)`
- `calculate_strategy_confusion_reduction(candidate, upstream_outputs)`
- `calculate_strategy_emotion_deescalation(candidate, upstream_outputs)`
- `calculate_strategy_bridge_opening(candidate, upstream_outputs)`
- `calculate_strategy_trust_repair_potential(candidate, upstream_outputs)`
- `calculate_strategy_fatigue_relief(candidate, upstream_outputs)`
- `calculate_strategy_reactivation_risk_reduction(candidate, upstream_outputs)`
- `calculate_strategy_amplification_risk(candidate, upstream_outputs)`
- `calculate_strategy_backlash_risk(candidate, upstream_outputs)`
- `calculate_strategy_privacy_risk(candidate)`
- `calculate_strategy_overclaim_risk(candidate)`
- `calculate_strategy_implementation_risk(candidate)`
- `calculate_strategy_benefit(candidate, components)`
- `calculate_strategy_cost(candidate, components)`
- `calculate_strategy_score(candidate, benefit, cost)`
- `determine_strategy_recommendation_level(candidate, scores, blockers)`
- `calculate_response_strategy_comparison(candidate, upstream_outputs)`
- `calculate_all_response_strategy_comparisons(fixture, upstream_outputs)`

All future helpers must be deterministic and pure. They must not read files, call networks, call real LLMs, write runtime files, or execute platform actions.

## E. Safe Inputs

Allow only safe fixture metadata:

- `fixture_metadata`
- `response_strategy_candidates`
- `ContentAggregateWeightV01` outputs
- `InfluenceCoreWeightV01` outputs
- `EchoBoxWeightV01` outputs
- `PeopleClusterStateV01` outputs

Optionally allow safe evidence-confidence summaries already present in upstream outputs.

Do not require:

- full text
- raw evidence rows
- raw identities
- external API data
- real collector directories
- `evidence_items.jsonl`
- `evidence_items.csv`

Allowed strategy-candidate fields may include only safe, explicit metadata already defined or compatible with the source model:

- `candidate_id`
- `strategy_id`
- `strategy_type`
- `strategy_status_hint`
- `stage_id`
- `claim_intensity`
- `stage_fit`
- `response_gap_fit`
- `heat_fit`
- `fatigue_fit`
- `strategy_clarity_base`
- `strategy_deescalation_base`
- `strategy_bridge_base`
- `transparency_level`
- `accountability_level`
- `consistency_with_prior_record`
- `resolution_signal`
- `low_amplification_level`
- `constructive_new_info`
- `unresolved_grievance_reduction`
- `low_identity_threat_language`
- `exposure_level`
- `novelty`
- `media_relay_probability`
- `mismatch_with_cluster_concerns`
- `perceived_defensiveness`
- `timing_lag`
- `low_empathy_language`
- `contradiction_with_prior_record`
- `identity_threat_risk`
- `ambiguity`
- `use_of_personal_story`
- `minor_or_family_sensitivity`
- `raw_identity_exposure`
- `consent_uncertainty`
- `doxxing_or_harassment_risk`
- `causal_language`
- `full_web_claim`
- `official_verification_claim`
- `prediction_language`
- `uncalibrated_score_without_boundary`
- `requires_new_runtime`
- `requires_real_API_or_LLM`
- `requires_unreviewed_data`
- `requires_external_actor_coordination`
- `requires_legal_review`
- `requires_sensitive_material`
- `voluntary`
- `informed_consent`
- `redacted`
- `minor_protected`
- `context_verifiable`
- `no_private_detail_exposure`
- `human_review_approved`
- `risk_flags`

No raw author ID.
No author name.
No profile URL.
No private message.
No cookie, token, session, profile path, localStorage, API key, salt, or secret.
No target-user fields.

## F. Formula Scope

Future 8P-6 must use `docs/model/response_strategy_comparison_model_v0_1.md` as the formula source of truth.

Do not invent formulas.
Do not change coefficients.
Do not silently rename formula components.
Do not invent recommendation levels.
Do not invent strategy IDs.

If source fields are missing from the fixture or upstream outputs, future implementation must mark the affected component as low confidence or blocked according to the missing-data policy. It must not create favorable evidence by default.

### F.1 Evidence Fit

```text
evidence_fit_r =
  1 - claim_intensity_r * (1 - Q)
```

### F.2 Timing Fit

```text
timing_fit_r =
  0.35 * stage_fit_r
+ 0.25 * response_gap_fit_r
+ 0.20 * heat_fit_r
+ 0.20 * fatigue_fit_r
```

### F.3 Benefit Components

Clarity gain:

```text
clarity_gain_r =
  strategy_clarity_base_r
* evidence_fit_r
* (0.60 + 0.40 * factual_credibility_mean)
```

Confusion reduction:

```text
confusion_reduction_r =
  clarity_gain_r
* narrative_fragmentation
* (0.50 + 0.50 * bridge_capacity)
```

Emotion de-escalation:

```text
emotion_deescalation_r =
  strategy_deescalation_base_r
* (0.50 + 0.50 * deescalation_potential_mean)
* (1 - backlash_risk_r)
```

Bridge opening:

```text
bridge_opening_r =
  strategy_bridge_base_r
* bridge_capacity
* (0.50 + 0.50 * cross_cutting_exposure)
* (1 - identity_threat_risk_r)
```

Trust repair:

```text
trust_repair_potential_r =
  0.35 * evidence_fit_r
+ 0.25 * transparency_level_r
+ 0.20 * accountability_level_r
+ 0.20 * consistency_with_prior_record_r
```

Fatigue relief:

```text
fatigue_relief_r =
  0.30 * resolution_signal_r
+ 0.20 * clarity_gain_r
+ 0.20 * low_amplification_level_r
+ 0.15 * constructive_new_info_r
+ 0.15 * bridge_opening_r
```

Reactivation risk reduction:

```text
reactivation_risk_reduction_r =
  0.30 * trust_repair_potential_r
+ 0.25 * confusion_reduction_r
+ 0.20 * unresolved_grievance_reduction_r
+ 0.15 * fatigue_relief_r
+ 0.10 * low_identity_threat_language_r
```

### F.4 Risk Components

Amplification risk:

```text
amplification_risk_r =
  0.30 * exposure_level_r
+ 0.20 * risk_breakout
+ 0.15 * observed_amplification_mean
+ 0.15 * controversy
+ 0.10 * novelty_r
+ 0.10 * media_relay_probability_r
```

Backlash risk:

```text
backlash_risk_r =
  0.25 * mismatch_with_cluster_concerns_r
+ 0.20 * perceived_defensiveness_r
+ 0.15 * timing_lag
+ 0.15 * low_empathy_language_r
+ 0.10 * contradiction_with_prior_record_r
+ 0.10 * identity_threat_risk_r
+ 0.05 * ambiguity_r
```

Privacy risk:

```text
privacy_risk_r =
  0.35 * use_of_personal_story_r
+ 0.25 * minor_or_family_sensitivity
+ 0.15 * raw_identity_exposure_r
+ 0.15 * consent_uncertainty_r
+ 0.10 * doxxing_or_harassment_risk
```

Overclaim risk:

```text
overclaim_risk_r =
  0.30 * causal_language_r
+ 0.25 * full_web_claim_r
+ 0.20 * official_verification_claim_r
+ 0.15 * prediction_language_r
+ 0.10 * uncalibrated_score_without_boundary_r
```

Implementation risk:

```text
implementation_risk_r =
  0.25 * requires_new_runtime
+ 0.20 * requires_real_API_or_LLM
+ 0.20 * requires_unreviewed_data
+ 0.15 * requires_external_actor_coordination
+ 0.10 * requires_legal_review
+ 0.10 * requires_sensitive_material
```

### F.5 Benefit, Cost, Score

```text
benefit_r =
  0.18 * clarity_gain_r
+ 0.16 * confusion_reduction_r
+ 0.15 * emotion_deescalation_r
+ 0.14 * bridge_opening_r
+ 0.13 * trust_repair_potential_r
+ 0.12 * fatigue_relief_r
+ 0.12 * reactivation_risk_reduction_r
```

```text
cost_r =
  0.26 * amplification_risk_r
+ 0.24 * backlash_risk_r
+ 0.20 * privacy_risk_r
+ 0.16 * overclaim_risk_r
+ 0.14 * implementation_risk_r
```

```text
strategy_score_r =
  clamp(0.50 + 0.50 * (benefit_r - cost_r), 0, 1)
```

### F.6 Recommendation Levels

Exact levels from the source model:

- `forbidden`
- `blocked_pending_review`
- `private_review_only`
- `strong_candidate_for_human_review`
- `candidate_for_human_review`
- `prepare_materials_first`
- `not_recommended_now`
- `monitor_only`

Highest allowed level:

```text
strong_candidate_for_human_review
```

Never output:

```text
auto_execute
```

### F.7 Deferred Source-Model Objects

The source model lists additional objects:

- `ResponseToPeopleClusterEffectV01`
- `ResponseToEchoBoxEffectV01`
- `GeneratedInfluenceCoreCandidateV01`

They are not included in the first 8P-6 slice. They remain deferred because the first implementation is comparison-only and must not imply causal effects, persuasion estimates, guaranteed community change, or generated public narrative creation.

## G. Gate And Blocker Policy

Future behavior must apply blockers before scores:

1. Forbidden strategy behavior -> `forbidden`
2. Privacy / consent / minor-safety blocker -> `blocked_pending_review` or `private_review_only`
3. Evidence insufficiency / trust blocker -> `prepare_materials_first` or `private_review_only`
4. Legal or sensitive-material review blocker -> `blocked_pending_review` or `private_review_only`
5. Overclaim blocker -> blocked or downgraded
6. Implementation-risk blocker -> blocked, downgraded, or warning
7. Score-based recommendation level

Specific gate rules:

- `auto_execute` -> forbidden
- fake consensus -> forbidden
- astroturfing -> forbidden
- bots, sockpuppets, or water-army behavior -> forbidden
- covert seeding -> forbidden
- undisclosed paid advocacy -> forbidden
- fabricated third-party endorsement -> forbidden
- manufactured grassroots activity -> forbidden
- harassment -> forbidden
- brigading -> forbidden
- coordinated reporting -> forbidden
- suppression of criticism -> forbidden
- individual targeting -> forbidden
- target-user lists -> forbidden
- ranking people by persuadability -> forbidden
- exploiting fear, identity threat, isolation, or vulnerability -> forbidden
- hiding material facts to improve sentiment -> forbidden
- false claims -> forbidden
- real API / LLM requirement -> implementation-risk warning or block
- sensitive-material requirement -> legal / privacy review
- overclaim language -> block or downgrade
- unknown strategy ID -> blocked or manual review

A score cannot override blockers.

## H. Missing-Data Policy

Deterministic handling:

- missing evidence confidence -> low-confidence warning
- missing stage -> timing-fit warning
- missing PeopleCluster output -> compare without cluster interpretation and warn
- missing EchoBox output -> compare without structural bridge / closure interpretation and warn
- missing InfluenceCore output -> credibility / de-escalation components downgrade and warn
- missing ContentAggregate output -> heat / controversy / review context unavailable; no strong recommendation
- missing consent fields for sensitive material -> block
- no candidate list -> `insufficient_data`
- unknown strategy ID -> manual review
- no upstream evidence -> no `strong_candidate_for_human_review`

Missing data must not become favorable evidence by default.

If a formula component cannot be mapped without inventing a coefficient, future implementation must use:

```text
implementation_requires_formula_confirmation_from_response_strategy_comparison_model_v0_1
```

## I. First-Slice Output Shape

Future `ResponseStrategyComparisonV01` output shape:

```text
schema = sentigraph_response_strategy_comparison_v0_1
comparison_id
candidate_id
strategy_id
strategy_type
model_status = 8P_6_response_strategy_comparison
coefficient_source = mock_default
calibration_status = uncalibrated
empirical_validation = not_started
sample_scope = selected_sample_or_local_fixture_only
```

Strategy status:

- `allowed`
- `allowed_with_review`
- `prepare_only`
- `blocked`
- `forbidden`

Scores:

- `evidence_fit`
- `timing_fit`
- `clarity_gain`
- `confusion_reduction`
- `emotion_deescalation`
- `bridge_opening`
- `trust_repair_potential`
- `fatigue_relief`
- `reactivation_risk_reduction`
- `amplification_risk`
- `backlash_risk`
- `privacy_risk`
- `overclaim_risk`
- `implementation_risk`
- `benefit_score`
- `cost_score`
- `strategy_score`

Recommendation:

- `recommendation_level`
- `eligible_for_human_review`
- `human_review_required = true`
- `not_auto_executed = true`
- `execution_authorized = false`
- `public_response_generated = false`
- `guaranteed_outcome = false`

Components:

- `benefit_components`
- `cost_components`
- `timing_components`
- `evidence_components`
- `privacy_components`
- `implementation_components`
- `associated_aggregate_ids_used`
- `associated_influence_core_ids_used`
- `associated_echo_box_ids_used`
- `associated_people_cluster_ids_used`

Blockers:

- `forbidden_behavior_blockers`
- `privacy_blockers`
- `consent_blockers`
- `evidence_blockers`
- `overclaim_blockers`
- `implementation_blockers`
- `legal_review_blockers`

Warnings:

- `low_confidence_warnings`
- `missing_component_warnings`
- `sensitive_material_warnings`
- `timing_warnings`
- `amplification_warnings`
- `backlash_warnings`
- `model_card_warnings`

Quality flags:

- `selected_sample_only`
- `uncalibrated`
- `mock_default_coefficients`
- `evidence_not_truth`
- `human_review_only`
- `not_auto_executed`
- `not_public_opinion_control`
- `not_individual_targeting`
- `not_guaranteed_outcome`

Explanation:

- short deterministic explanation
- describe benefits and costs separately
- never promise an outcome
- never instruct execution

Boundary flags:

```text
human_review_required = true
not_auto_executed = true
not_public_opinion_control = true
not_individual_targeting = true
not_target_user_list = true
not_causal_proof = true
not_prediction = true
not_guaranteed_outcome = true
not_official_verification = true
evidence_not_truth = true
selected_sample_only = true
no_publication_action = true
```

Do not include:

- `auto_execute`
- `execute_now`
- `publish_now`
- `send_now`
- `post_now`
- `response_text`
- `generated_public_message`
- `guaranteed_success`
- `guaranteed_calming`
- `predicted_support_gain`
- `predicted_opposition_drop`
- `persuasion_score`
- `prediction_probability`
- `target_user_list`
- `raw_author_identifiers`
- `real_account_id`
- `psychological_profile`
- `ResponseToPeopleClusterEffectV01`
- `ResponseToEchoBoxEffectV01`
- `GeneratedInfluenceCoreCandidateV01`
- `pull_ik`
- `stance_effect_ik`
- `InfluenceCoreToClusterEffectV01`

## J. Integration With Existing Run Object

Future `calculate_opinion_ecosystem_mock_fixture` should:

- run 8P-1 validation first
- if blocked, calculate nothing
- if manual-review-required due unknown / future platform, do not calculate ResponseStrategy
- if metadata-ready, preserve:
  - `ContentAggregateWeightV01`
  - `InfluenceCoreWeightV01`
  - `EchoBoxWeightV01`
  - `PeopleClusterStateV01`
- calculate `ResponseStrategyComparisonV01` only from explicit safe candidates
- preserve all boundary flags
- preserve all runtime side-effect flags as false
- never create execution side effects

Future `module_outputs`:

- `content_aggregate`: list of `ContentAggregateWeightV01`
- `influence_core`: list of `InfluenceCoreWeightV01`
- `echo_box`: list of `EchoBoxWeightV01`
- `people_cluster`: list of `PeopleClusterStateV01`
- `response_strategy`: list of `ResponseStrategyComparisonV01`

No effect objects in the first slice.

## K. Future Tests

Future 8P-6 tests should include:

- `test_response_strategy_minimal_fixture_calculates_comparison_v0_1`
- `test_response_strategy_preserves_all_upstream_outputs`
- `test_response_strategy_highest_level_is_human_review_candidate`
- `test_response_strategy_auto_execute_is_forbidden`
- `test_response_strategy_forbidden_behavior_is_blocked`
- `test_response_strategy_unknown_id_requires_manual_review`
- `test_response_strategy_insufficient_evidence_is_not_strong_candidate`
- `test_t4_long_faq_can_have_clarity_benefit_and_backlash_risk`
- `test_no_guaranteed_calming_claim`
- `test_low_credibility_claim_not_treated_as_fact`
- `test_no_response_is_baseline_not_automatic_recommendation`
- `test_third_party_explanation_requires_disclosure_and_review`
- `test_fabricated_third_party_endorsement_is_forbidden`
- `test_minors_or_family_material_without_consent_is_blocked`
- `test_privacy_blocker_overrides_high_benefit`
- `test_community_deconstruction_support_not_covert_seeding`
- `test_correction_or_apology_requires_applicability_evidence`
- `test_no_generated_response_text_in_8P_6`
- `test_no_peoplecluster_or_echobox_effect_objects_in_8P_6`
- `test_no_pull_or_stance_effect_in_8P_6`
- `test_no_target_user_list_or_persuasion_score`
- `test_no_forbidden_output_fields_after_response_strategy_scoring`
- `test_deterministic_same_fixture_same_response_strategy_output`
- `test_no_real_io_or_runtime_side_effects_by_design`

## L. Not Allowed In Future First Implementation

Future 8P-6 first implementation must not include:

- frontend Strategy Lab
- API route
- runtime persistence
- generated response text
- posting or publishing
- account action
- response effect objects
- causal claims
- guaranteed outcomes
- real API / LLM
- collector
- `evidence_items` file parsing
- Evidence Layer write
- production case / `analysis_run`
- B-end report / Sandbox / public event runtime
- individual targeting
- target-user list
- psychological profiling
- fake consensus
- covert manipulation
- bots / sockpuppets
- harassment
- `auto_execute`

## M. Later Slices

Only after the first `ResponseStrategyComparisonV01` slice passes targeted validation and model-card QA may separate future checkpoints consider:

- effect-object design, if still justified
- frontend explanatory UI
- B-end report explanation integration
- model-card QA and screenshot smoke
- historical replay comparison
- human-review comparison and calibration

This document does not pre-authorize those later slices.
