# ContentAggregate Heat / Controversy / Risk Model v0.1

Status: docs-only / design-stage / deterministic heuristic / sample-scoped / uncalibrated.

This model is not implemented. It is not a real hotlist, not official verification, not causal proof, and not full-web or full-platform coverage.

## 1. Purpose

Define sample-scoped ContentAggregate scores:

- `sample_heat_score`
- `sample_controversy_score`
- `discussion_risk_score`
- `review_risk_score`
- `evidence_confidence_score`

Formula metadata:

- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`

## 2. Evidence Base Weight

```text
w_e = trust_weight * review_weight * dedup_weight * relevance_weight * recency_weight
```

### Trust Weight Defaults

| Source / provenance | trust_weight |
| --- | ---: |
| official_api_public | 1.00 |
| official_api_oauth | 0.95 |
| reviewed_public_parser | 0.80 |
| manual_url_with_attestation | 0.65 |
| data_vendor_attested | 0.55 |
| user_upload_with_source | 0.50 |
| search_discovery_candidate | 0.40 |
| manual_text_without_source | 0.30 |
| screenshot_transcription | 0.30 |
| mock_fixture | 0.25 |
| unknown_or_unclear_source | 0.20 |

### Review Weight Defaults

| review_status | review_weight |
| --- | ---: |
| approved | 1.00 |
| not_reviewed | 0.70 |
| review_needed | 0.70 |
| needs_more_source | 0.55 |
| marked_weak | 0.45 |
| rejected | 0.00 |
| human_rejected | 0.00 |

### Dedup Weight

```text
dedup_weight_e = 1 / sqrt(duplicate_group_size)
```

If no duplicate group exists:

```text
dedup_weight_e = 1
```

Repetition signal:

```text
repetition_signal_g = log(1 + duplicate_group_size) / log(1 + duplicate_cap)
```

Duplicate evidence must not infinitely amplify heat, sentiment, risk, coverage, or report conclusions.

### Relevance Weight

| relevance | relevance_weight |
| --- | ---: |
| strong_case_match | 1.00 |
| partial_case_match | 0.60 |
| weak_case_match | 0.30 |
| off_topic | 0.00 |

### Recency Weight For Historical Replay

| recency | recency_weight |
| --- | ---: |
| inside_stage_window | 1.00 |
| near_stage_window | 0.70 |
| outside_but_relevant | 0.40 |
| unknown_time | 0.60 |

## 3. Utility Function

```text
log_norm(x, cap) = clamp(log(1 + x) / log(1 + cap), 0, 1)
```

## 4. Heat Components

- `V_A = volume_score`
- `I_A = interaction_score`
- `G_A = growth_score`
- `E_A = emotion_intensity`
- `S_A = spread_score`
- `R_A = repetition_signal`

Observed sample heat:

```text
H_observed_A =
  0.30 * V_A
+ 0.20 * I_A
+ 0.15 * G_A
+ 0.15 * E_A
+ 0.10 * S_A
+ 0.10 * R_A
```

If components are missing, re-normalize over available components.

Confidence-adjusted heat:

```text
H_conf_A = H_observed_A * (0.60 + 0.40 * Q_A)
```

## 5. Evidence Confidence

```text
Q_A = weighted_mean(trust_weight_e * review_weight_e, dedup_adjusted_weight_e)
```

Coverage quality:

```text
coverage_quality_A =
  0.35 * source_url_present_share
+ 0.25 * reviewed_or_approved_share
+ 0.20 * non_low_trust_share
+ 0.20 * non_unknown_stance_share
```

Evidence confidence:

```text
evidence_confidence_A =
  0.65 * Q_A
+ 0.35 * coverage_quality_A
```

Low evidence confidence means conclusions must be downgraded. It does not mean evidence is false.

## 6. Polarization And Controversy

```text
conflict_mass = p_support + p_oppose
balance = 1 - abs(p_support - p_oppose) / (p_support + p_oppose + epsilon)
known_ratio = 1 - p_unknown
P_A = conflict_mass * balance * sqrt(known_ratio)
```

Controversy:

```text
C_A =
  0.30 * P_A
+ 0.20 * E_A
+ 0.15 * X_A
+ 0.15 * D_A
+ 0.10 * R_A
+ 0.10 * L_A
```

Where:

- `X_A = cross-stance interaction or heuristic proxy`
- `D_A = narrative divergence`
- `L_A = low_trust_share_A * P_A`

## 7. Discussion Risk

```text
DR_A =
  0.25 * H_observed_A
+ 0.25 * C_A
+ 0.15 * E_A
+ 0.15 * S_A
+ 0.10 * issue_sensitivity_A
+ 0.10 * response_gap_A
```

Discussion risk is not legal risk and must not be treated as a final fact judgment.

## 8. Review Risk

```text
RR_A =
  0.30 * (1 - evidence_confidence_A)
+ 0.25 * low_trust_share_A
+ 0.20 * review_needed_share_A
+ 0.15 * missing_source_url_share_A
+ 0.10 * sensitive_privacy_flag_share_A
```

Overall risk:

```text
R_A = 0.70 * DR_A + 0.30 * RR_A
```

## 9. Required Output Object

`ContentAggregateWeightV01`:

```json
{
  "schema": "sentigraph_content_aggregate_weight_v0_1",
  "sample_scope": "selected_sample_only",
  "model_status": "design_stage",
  "coefficient_source": "mock_default",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "evidence_mass": {},
  "scores": {},
  "components": {},
  "quality_flags": [],
  "explanation": [],
  "boundary_flags": {
    "not_real_hotlist": true,
    "not_full_web": true,
    "not_full_platform": true,
    "not_official_verification": true,
    "not_causal_proof": true
  }
}
```

## 10. Anti-Overclaim Rules

- `sample_heat_score` is not a real hotlist.
- `sample_controversy_score` is not fact judgment.
- `discussion_risk_score` is not legal risk.
- Low evidence confidence means downgrade conclusions.
- Low-trust screenshot evidence can raise review risk but should lower confidence.

## 11. Counterexample Matrix

| Counterexample | Expected behavior |
| --- | --- |
| Duplicate comments | Increase repetition signal but do not infinitely amplify heat. |
| Low-trust screenshot | May raise review risk but lowers confidence. |
| One-sided high heat | Does not imply high controversy. |
| Multi-platform low-emotion discussion | Should not inflate risk automatically. |
| Small trusted source sample | May have high confidence but low heat. |
