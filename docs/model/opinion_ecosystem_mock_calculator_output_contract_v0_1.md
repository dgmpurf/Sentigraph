# Opinion Ecosystem Mock Calculator Output Contract v0.1

Status: docs-only / design-only / future deterministic local mock calculator output contract. This is not implemented, not runtime, not backend schema, not frontend UI, not real API, not real LLM, not crawler, not full-web, not full-platform, not official verification, not causal proof, not prediction, not personality diagnosis, not individual persuasion scoring, and not auto-executed response strategy.

Scope is selected sample / local fixture / imported evidence only.

Required model metadata:

- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`

## 1. Purpose

This document designs the future output contract for a local deterministic mock calculator. It defines the run summary, module output references, required warnings, and forbidden output fields.

## 2. OpinionEcosystemMockCalculatorRunV01

Illustrative Markdown-only shape:

```json
{
  "schema": "sentigraph_opinion_ecosystem_mock_calculator_run_v0_1",
  "run_id": "mock_run_001",
  "fixture_id": "fixture_001",
  "model_name": "sentigraph_opinion_ecosystem_weight_model",
  "model_version": "0.1",
  "model_status": "design_stage_or_mock_runtime",
  "coefficient_source": "mock_default",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "generated_at": "2026-01-01T00:00:00Z",
  "scope_note": "selected_sample_only",
  "boundary_flags": {},
  "input_summary": {},
  "output_refs": {},
  "validation_summary": {},
  "human_review_required": true
}
```

This is not an executable fixture or runtime output in this phase.

## 3. Module Outputs

Future output refs may include:

- `ContentAggregateWeightV01`
- `PeopleClusterStateV01`
- `InfluenceCoreWeightV01`
- `InfluenceCoreToClusterEffectV01`
- `EchoBoxWeightV01`
- `ResponseStrategyComparisonV01`
- `ResponseToPeopleClusterEffectV01`
- `ResponseToEchoBoxEffectV01`
- `GeneratedInfluenceCoreCandidateV01`

## 4. Required Boundary Flags

Every run and module output must include:

```json
{
  "not_full_web": true,
  "not_full_platform": true,
  "not_official_verification": true,
  "not_causal_proof": true,
  "not_prediction": true,
  "not_personality_diagnosis": true,
  "not_individual_persuasion_scoring": true,
  "not_public_opinion_control": true,
  "not_auto_executed": true,
  "selected_sample_only": true,
  "evidence_not_truth": true,
  "human_review_required": true
}
```

## 5. Required Warning Fields

Future run output must include these warning arrays or counters:

- `low_confidence_warnings`
- `low_trust_warnings`
- `review_needed_warnings`
- `duplicate_folded_warnings`
- `rejected_excluded_warnings`
- `privacy_blockers`
- `overclaim_blockers`
- `response_strategy_blockers`
- `model_card_warnings`

Warnings must be visible to future UI/report layers and must not be silently dropped.

## 6. Forbidden Outputs

The future calculator must never output:

- `real_hotlist_score`
- `truth_score`
- `official_verified = true` unless a future real official input path explicitly supports it and the output is separately gated
- `causal_chain_confirmed`
- `prediction_probability`
- `persuasion_score`
- `auto_execute`
- `target_user_list`
- `raw_author_identifiers`

## 7. Module Output Notes

### ContentAggregateWeightV01

Must include selected sample scope, evidence confidence, heat / controversy / risk scores, and warnings that sample heat is not a real hotlist.

### PeopleClusterStateV01

Must include `not_real_person = true` and `aggregate_behavioral_proxy = true`.

### InfluenceCoreWeightV01

Must include `not_person_ball = true` and `evidence_not_truth = true`.

### EchoBoxWeightV01

Must include `not_real_community_map = true` and `not_full_social_graph = true`.

### ResponseStrategyComparisonV01

Must include:

- `human_review_required = true`
- `not_auto_executed = true`
- strategy recommendation level no higher than `strong_candidate_for_human_review`

## 8. Validation Summary Requirements

Future `validation_summary` should include:

- fixture schema validation status
- forbidden field validation status
- model metadata validation status
- boundary flag validation status
- counterexample validation status
- human review requirement validation status
- no real API / real LLM / crawler validation status

It must not include absolute local paths, secrets, browser profile paths, tokens, cookies, sessions, or raw author identifiers.
