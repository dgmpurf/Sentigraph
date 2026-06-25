# Sentigraph Opinion Ecosystem Weight Model v0.1

Status: docs-only / design-stage / deterministic heuristic / sample-scoped / uncalibrated.

This document describes a future model specification only. It is not implemented in backend, frontend, runtime, report generation, Sandbox generation, or any real analysis execution path.

## 1. Model Identity

- Model name: Sentigraph Opinion Ecosystem Weight Model v0.1
- Model status: deterministic / heuristic / sample-scoped / uncalibrated / design-stage
- `coefficient_source`: `mock_default`
- `calibration_status`: `uncalibrated`
- `empirical_validation`: `not_started`

## 2. Main Chain

```text
EvidenceItem
-> ContentAggregate
-> InfluenceCore
-> EchoBox
-> PeopleCluster
-> T0-T6 state transition
-> Response Strategy comparison
```

## 3. Intended Use

- Describe selected sample discussion structure.
- Explain sample heat, controversy, and risk.
- Explain anonymous PeopleCluster behavior proxies.
- Explain InfluenceCore pull, credibility, and amplification.
- Explain EchoBox saturation, bridge, and breakout proxies.
- Compare transparent response options before human review.
- Support B-end report explanation and Sandbox V2 visual parameters.

## 4. Forbidden Use

- Not real prediction.
- Not causal proof.
- Not official verification.
- Not full-web coverage.
- Not full-platform coverage.
- Not personality diagnosis.
- Not individual persuasion scoring.
- Not public-opinion control.
- Not auto PR decision.
- Not manipulation, astroturfing, fake consensus, harassment, or targeted influence.
- Not a crawler or live monitoring claim.

## 5. Core Boundaries

- PeopleCluster means anonymous aggregate group / behavioral proxy, not a real person.
- InfluenceCore means content / narrative / official / media / KOL / meme core, not people balls.
- EchoBox is a sample-scoped discussion container proxy, not a real community map.
- Provider output and Evidence are evidence, not truth.
- Evidence Scale / Coverage does not mean full-web or full-platform coverage.
- All response strategy outputs require human review.

## 6. Module Outputs

### ContentAggregate

Produces sample-scoped scores:

- `sample_heat_score`
- `sample_controversy_score`
- `discussion_risk_score`
- `review_risk_score`
- `evidence_confidence_score`

### PeopleCluster

Produces anonymous aggregate state transitions:

- stance proxy
- attention proxy
- fatigue proxy
- expression intensity proxy
- exit / cooling / reactivation probabilities

### InfluenceCore

Produces core-level weights:

- factual credibility
- narrative resonance
- exposure
- pull
- amplification
- bridge
- de-escalation
- backlash
- core risk

### EchoBox

Produces discussion-container structure proxies:

- saturation
- closure
- bridge capacity
- constructive breakout
- risk breakout
- echo risk

### ResponseStrategy

Produces human-review candidates only:

- benefit
- cost
- strategy score
- recommendation level
- risk flags

The highest allowed recommendation level is `strong_candidate_for_human_review`. The model must never output `auto_execute`.

## 7. Required Output Metadata

Every future runtime output based on this model must include:

```json
{
  "model_name": "sentigraph_opinion_ecosystem_weight_model_v0_1",
  "model_status": "design_stage",
  "coefficient_source": "mock_default",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "scope_note": "selected_sample_only",
  "not_full_web": true,
  "not_full_platform": true,
  "not_official_verification": true,
  "not_causal_proof": true,
  "not_future_prediction": true,
  "human_review_required": true
}
```

## 8. Integration Position

This v0.1 design should remain behind explicit gates:

1. Evidence governance.
2. Review queue completion.
3. Dedup review completion.
4. Analysis-ready promotion.
5. Human review before response strategy use.

It must not bypass rejected evidence, privacy holds, missing-source blockers, dedup governance, or human review.
