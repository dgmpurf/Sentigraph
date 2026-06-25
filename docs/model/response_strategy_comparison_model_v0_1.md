# Response Strategy Comparison Model v0.1

Status: docs-only / design-stage / deterministic heuristic / sample-scoped / uncalibrated.

This model compares transparent response options. It never auto-executes a response strategy. All outputs require human review.

Formula metadata:

- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`

## 1. Purpose

Compare response options for human review:

- clarity gain
- confusion reduction
- emotion de-escalation
- bridge opening
- trust repair potential
- fatigue relief
- reactivation risk reduction
- amplification risk
- backlash risk
- privacy risk
- overclaim risk
- implementation risk

## 2. Allowed Strategy IDs

- `S0 no_response_baseline`
- `S1 observe_and_prepare`
- `S2 low_amplification_hold`
- `S3 factual_clarification`
- `S4 FAQ_or_longform_explanation`
- `S5 evidence_supported_context`
- `S6 third_party_explanation`
- `S7 correction_or_apology_if_applicable`
- `S8 progress_update`
- `S9 community_deconstruction_support`
- `S10 fatigue_period_reputation_repair`
- `S11 private_review_before_public_response`

Strategy status:

- `allowed`
- `allowed_with_review`
- `prepare_only`
- `blocked`
- `forbidden`

## 3. Forbidden Strategy Behaviors

- fake consensus
- covert manipulation
- sockpuppet / bot / 水军
- individual targeting
- harassment
- fabricated third-party endorsement
- using minors without strict protection

## 4. Evidence Fit

```text
evidence_fit_r =
  1 - claim_intensity_r * (1 - Q)
```

## 5. Timing Fit

```text
timing_fit_r =
  0.35 * stage_fit_r
+ 0.25 * response_gap_fit_r
+ 0.20 * heat_fit_r
+ 0.20 * fatigue_fit_r
```

## 6. Benefit Components

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

## 7. Risk Components

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

## 8. Benefit, Cost, Score

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

## 9. Recommendation Levels

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

## 10. Special Rule For Third-Party / Beneficiary / Parent / Adult Student Material

All must be true:

```text
voluntary = true
informed_consent = true
redacted = true
minor_protected = true
context_verifiable = true
no_private_detail_exposure = true
human_review_approved = true
```

If any condition is missing, the strategy must be `blocked_pending_review` or `private_review_only`.

## 11. Required Output Objects

- `ResponseStrategyComparisonV01`
- `ResponseToPeopleClusterEffectV01`
- `ResponseToEchoBoxEffectV01`
- `GeneratedInfluenceCoreCandidateV01`

All objects must include:

- `human_review_required = true`
- `not_auto_executed = true`
- `not_public_opinion_control = true`
- `model_status = design_stage`
- `calibration_status = uncalibrated`

## 12. Counterexample Matrix

| Counterexample | Expected behavior |
| --- | --- |
| Evidence insufficient but quick clarification requested | Prepare materials or private review first. |
| T4 emotional peak with long FAQ | Higher amplification / backlash risk. |
| Low credibility viral claim | Avoid treating claim as fact. |
| Community already naturally deconstructing | Consider observe / support deconstruction carefully. |
| Minors/family material without consent | Block pending review. |
| Official source credible but opposition distrusts official source | Bridge may require third-party explanation or context. |
