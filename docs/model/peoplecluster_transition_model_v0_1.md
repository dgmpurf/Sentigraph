# PeopleCluster State Transition Model v0.1

Status: docs-only / design-stage / deterministic heuristic / sample-scoped / uncalibrated.

PeopleCluster means anonymous aggregate group / behavioral proxy. It is not a real person, account, psychological profile, personality diagnosis, or persuasion target.

Formula metadata:

- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`

## 1. Purpose

Define anonymous aggregate PeopleCluster state transition across T0-T6 for Sandbox V2 and B-end explanation.

This is not future prediction and not causal proof.

## 2. State Vector

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

## 3. Evidence Confidence Damping

```text
D_Q = 0.40 + 0.60 * Q
```

`Q` comes from ContentAggregate evidence confidence. Low confidence dampens stance movement.

## 4. Bounded Confidence

```text
epsilon_i = epsilon_min + (epsilon_max - epsilon_min) * o_i
epsilon_min = 0.25
epsilon_max = 0.85
```

```text
gate_ij = 1 if |s_i - s_j| <= epsilon_i, otherwise bridge_leak_ij
bridge_leak_ij = 0.10 * bridge_exposure_ij
```

## 5. Peer Field

```text
P_i =
  sum_j(edge_ij * gate_ij * a_j * e_j * u_j * s_j)
  /
  (sum_j(edge_ij * gate_ij * a_j * e_j * u_j) + epsilon)
```

## 6. InfluenceCore Field

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

## 7. Resistance And Learning Rate

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

## 8. Stance Update

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

## 9. Confidence Update

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

## 10. Attention Update

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

## 11. Fatigue Update

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

## 12. Expression Intensity

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

## 13. Exit And Reactivation Proxies

Fatigue exit:

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

Cooling exit:

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

Reactivation:

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

## 14. Camp Labels

- `support`
- `neutral_or_uncertain`
- `oppose`
- `mixed`
- `exited_or_fatigued`

## 15. Required Output Object

`PeopleClusterStateV01`:

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

Possible flags:

- `low_confidence`
- `high_fatigue`
- `high_reactivation_risk`

## 16. Counterexample Matrix

| Counterexample | Expected behavior |
| --- | --- |
| Low-trust emotional screenshot | Does not force massive stance change. |
| One-sided heat | Does not invent opposition cluster. |
| Official clarification | Can reduce fatigue but not instantly flip opposition. |
| Repeated meme | Can increase fatigue without infinite confidence increase. |
| T6 new trigger | Raises reactivation proxy but is not prediction. |
