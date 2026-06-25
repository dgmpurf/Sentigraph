# InfluenceCore Weight Model v0.1

Status: docs-only / design-stage / deterministic heuristic / sample-scoped / uncalibrated.

InfluenceCore means content / narrative / official / media / KOL / meme / explanation core. It is not PeopleCluster, not a person ball, not a fact verifier, not causal root proof, and not a persuasion target.

Formula metadata:

- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`

## 1. Purpose

Define InfluenceCore weights:

- factual credibility
- narrative resonance
- sample exposure
- pull
- amplification
- bridge
- de-escalation
- backlash
- core risk

## 2. Core Variables

```text
d_k  = frame_direction [-1, 1]
fc_k = factual_credibility
nr_k = narrative_resonance
ex_k = sample_exposure
cl_k = clarity_score
nv_k = novelty_score
em_k = emotional_charge
br_k = bridge_potential
rp_k = repetition_signal
rs_k = resolution_signal
bk_k = backlash_risk
```

## 3. Core Types

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

## 4. Factual Credibility

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

Default source identity weights:

| Source identity | weight |
| --- | ---: |
| official_statement | 0.95 |
| recognized_media_report | 0.78 |
| expert_explanation | 0.72 |
| known_org_or_institution | 0.70 |
| kol_creator_content | 0.58 |
| ordinary_viral_content | 0.45 |
| forum_thread | 0.42 |
| community_comment_cluster | 0.38 |
| meme_deconstruction | 0.30 |
| unknown_source_core | 0.25 |
| low_trust_claim | 0.15 |

Factual credibility is sample evidence credibility, not official verification.

## 5. Narrative Resonance

```text
nr_k =
  0.22 * clarity_score
+ 0.20 * emotional_charge
+ 0.18 * repetition_signal
+ 0.15 * novelty_score
+ 0.15 * identity_or_group_relevance_proxy
+ 0.10 * meme_or_symbolic_density
```

## 6. Sample Exposure

```text
ex_k =
  0.35 * log_norm(weighted_mentions_k, mention_cap)
+ 0.20 * log_norm(weighted_replies_k, reply_cap)
+ 0.15 * log_norm(weighted_shares_or_reposts_k, share_cap)
+ 0.15 * platform_spread_k
+ 0.15 * source_spread_k
```

Sample exposure is not full-platform coverage.

## 7. Bridge Potential

```text
br_k =
  0.25 * cross_platform_presence
+ 0.20 * neutral_or_explanatory_frame
+ 0.20 * source_credibility_across_camps
+ 0.15 * low_identity_threat_language
+ 0.10 * shared_value_language
+ 0.10 * media_or_third_party_relay
```

## 8. Backlash Risk

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

## 9. Impact Gate

```text
fit_ik = exp(- |s_i - d_k| / tau_fit)
tau_fit = 0.70
```

```text
challenge_ik =
  o_i * fc_k * br_k * exp(- |s_i - d_k| / tau_challenge)
tau_challenge = 1.20
```

```text
impact_gate_ik =
  0.70 * fit_ik
+ 0.30 * challenge_ik
```

## 10. Core Strength And Pull

```text
core_strength_k =
  0.24 * fc_k
+ 0.22 * nr_k
+ 0.18 * ex_k
+ 0.14 * cl_k
+ 0.12 * nv_k
+ 0.10 * br_k
```

```text
pull_ik =
  exposure_ik
* core_strength_k
* impact_gate_ik
* (1 - f_i)
* D_Q
```

Directional stance effect:

```text
stance_effect_ik = pull_ik * (d_k - s_i)
stance_effect_ik_adjusted = stance_effect_ik * (0.40 + 0.60 * fc_k)
```

## 11. Amplification

Attention amplification:

```text
attention_amplification_k =
  0.24 * ex_k
+ 0.20 * nr_k
+ 0.18 * em_k
+ 0.16 * nv_k
+ 0.12 * rp_k
+ 0.10 * br_k
```

Amplification:

```text
amp_k =
  0.25 * attention_amplification_k
+ 0.20 * ex_k
+ 0.18 * rp_k
+ 0.15 * br_k
+ 0.12 * nv_k
+ 0.10 * em_k
```

Credibility-adjusted influence score:

```text
credibility_adjusted_influence_score =
  amp_k * (0.55 + 0.45 * fc_k)
```

## 12. De-Escalation

```text
deescalation_potential_k =
  0.24 * fc_k
+ 0.22 * cl_k
+ 0.20 * rs_k
+ 0.16 * br_k
+ 0.10 * empathy_or_context_k
+ 0.08 * low_identity_threat_language
- 0.20 * bk_k
```

## 13. Core Risk

```text
core_risk_k =
  0.20 * amp_k
+ 0.18 * bk_k
+ 0.16 * em_k
+ 0.14 * low_trust_conflict_k
+ 0.12 * privacy_or_sensitivity_risk_k
+ 0.10 * contradiction_risk_k
+ 0.10 * unresolved_grievance_k
```

## 14. Required Output Objects

`InfluenceCoreWeightV01`:

```json
{
  "schema": "sentigraph_influencecore_weight_v0_1",
  "model_status": "design_stage",
  "coefficient_source": "mock_default",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "core_type": "unknown_source_core",
  "scores": {},
  "components": {},
  "explanation": [],
  "boundary_flags": {
    "not_person_ball": true,
    "not_fact_verifier": true,
    "not_causal_root_proof": true
  }
}
```

`InfluenceCoreToClusterEffectV01`:

```json
{
  "schema": "sentigraph_influencecore_to_cluster_effect_v0_1",
  "cluster_id": "",
  "core_id": "",
  "pull": 0,
  "stance_effect": 0,
  "stance_effect_adjusted": 0,
  "human_review_required": true
}
```

## 15. Counterexample Matrix

| Counterexample | Expected behavior |
| --- | --- |
| Official statement credible but low exposure | High credibility, limited sample pull. |
| Viral meme high amplification but low credibility | High amplification risk, low factual credibility. |
| KOL cross-community relay | Affects open clusters more than closed clusters. |
| Third-party explanation | May have high de-escalation without high heat. |
| Low-trust claim | Raises risk but must not be treated as fact. |
