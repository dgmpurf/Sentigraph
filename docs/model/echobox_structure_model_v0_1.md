# EchoBox Structure Model v0.1

Status: docs-only / design-stage / deterministic heuristic / sample-scoped / uncalibrated.

EchoBox is a sample-scoped anonymous discussion container proxy. It is not a real community map, full social graph, causal propagation chain, or target pool.

Formula metadata:

- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`

## 1. Purpose

Define EchoBox structure proxies:

- saturation
- closure
- bridge capacity
- constructive breakout
- risk breakout
- echo risk

## 2. Core Variables

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

## 3. Stance Entropy

```text
stance_entropy_b = - sum_i(p_i * log(p_i)) / log(k)
```

## 4. Stance Concentration

```text
stance_concentration_b =
  max(p_support_b, p_neutral_b, p_oppose_b, p_mixed_b)
* (1 - p_unknown_b)
```

## 5. Saturation

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

## 6. Closure

```text
closure_b =
  0.30 * (1 - cross_cutting_exposure_b)
+ 0.25 * (1 - cross_box_exposure_b)
+ 0.20 * stance_concentration_b
+ 0.15 * internal_density_b
+ 0.10 * (1 - bridge_capacity_b)
```

## 7. Bridge Capacity

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

## 8. Constructive Breakout

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

## 9. Risk Breakout

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

## 10. Echo Risk

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

## 11. Echo Types

- `sealed_echo_box`
- `saturated_but_bridgeable`
- `bridge_ready_box`
- `risk_breakout_box`
- `fatigue_decay_box`
- `mixed_discussion_box`

## 12. Required Output Object

`EchoBoxWeightV01`:

```json
{
  "schema": "sentigraph_echobox_weight_v0_1",
  "model_status": "design_stage",
  "coefficient_source": "mock_default",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "sample_scope": "selected_sample_only",
  "echo_type": "mixed_discussion_box",
  "scores": {},
  "components": {},
  "explanation": [],
  "boundary_flags": {
    "not_real_community_map": true,
    "not_full_social_graph": true,
    "not_causal_propagation_chain": true,
    "not_target_pool": true
  }
}
```

## 13. Counterexample Matrix

| Counterexample | Expected behavior |
| --- | --- |
| Strong echo but no breakout | High saturation / closure, low breakout. |
| Controversy high but bridge capacity high | Risk may be moderated by bridge capacity. |
| Meme risk breakout with low credibility | Raises risk breakout but not truth. |
| Clear official explanation inside one box | Local de-escalation only, not full-platform effect. |
| Multi-platform parallel boxes | Does not imply mutual influence. |
