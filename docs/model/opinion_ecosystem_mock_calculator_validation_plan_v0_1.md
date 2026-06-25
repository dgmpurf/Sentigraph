# Opinion Ecosystem Mock Calculator Validation Plan v0.1

Status: docs-only / design-only / future deterministic local mock calculator validation plan. This is not implemented, not runtime, not backend schema, not frontend UI, not tests, not real API, not real LLM, not crawler, not full-web, not full-platform, not official verification, not causal proof, not prediction, not personality diagnosis, not individual persuasion scoring, and not auto-executed response strategy.

Scope is selected sample / local fixture / imported evidence only.

Required model metadata:

- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`

## 1. Purpose

This document defines a future validation plan for a deterministic local mock calculator. It does not add tests in this phase.

## 2. Validation Layers

### Docs Review Validation

Confirm that future implementation traces back to:

- `opinion_ecosystem_weight_model_v0_1.md`
- `content_aggregate_heat_risk_model_v0_1.md`
- `peoplecluster_transition_model_v0_1.md`
- `influencecore_weight_model_v0_1.md`
- `echobox_structure_model_v0_1.md`
- `response_strategy_comparison_model_v0_1.md`
- `opinion_ecosystem_weight_model_card_v0_1.md`

### Fixture Contract Validation

Validate:

- required fixture groups exist
- required metadata exists
- selected sample boundary flags exist
- forbidden fields are absent
- response strategy does not contain `auto_execute`
- no full-web / full-platform / official verification / causal proof / prediction claims

### Output Boundary Validation

Validate every output includes:

- `model_status`
- `coefficient_source`
- `calibration_status`
- `empirical_validation`
- `scope_note`
- boundary flags
- warning fields
- human review requirement

### Counterexample Validation

Run future tests based on `opinion_ecosystem_mock_calculator_counterexample_matrix_v0_1.md`.

### Model Card QA Validation

Validate:

- model card warnings are propagated
- red-flag phrases are blocked or translated into safe replacements
- no output implies truth, causality, prediction, personality diagnosis, or individual persuasion scoring

### Snapshot Stability Validation

For the same fixture:

- output should be deterministic
- score ordering should be stable
- warnings should be stable
- only `generated_at` may vary if not fixture-fixed

### Sensitivity Smoke

Design-only future sensitivity checks:

- increasing duplicate count should increase repetition signal sublinearly
- lowering trust should lower confidence
- rejecting evidence should exclude it
- increasing bridge capacity should change EchoBox classification
- setting `auto_execute` should fail validation

No empirical calibration is included in this phase.

## 3. Future Targeted Test Groups

- `fixture_schema_validation`
- `evidence_weighting_validation`
- `content_aggregate_formula_validation`
- `peoplecluster_transition_validation`
- `influencecore_formula_validation`
- `echobox_formula_validation`
- `response_strategy_validation`
- `boundary_and_overclaim_validation`
- `forbidden_fields_validation`

## 4. Required Future Validation Invariants

- low trust dampens conclusions
- rejected evidence excluded
- duplicates folded
- PeopleCluster has no raw author IDs
- InfluenceCore is not a person ball
- EchoBox is not a real community map
- ResponseStrategy has no `auto_execute`
- all strategy outputs include `human_review_required`
- all outputs include `model_status`, `calibration_status`, and `scope_note`
- no real API / real LLM / crawler flags
- no full-web, full-platform, official-verification, causal-proof, or prediction claims

## 5. Forbidden Field Validation

Future validation must block:

- `raw_author_id`
- `raw_author_name`
- `author_name`
- `profile_url`
- private message content
- cookie
- token
- session
- browser profile
- localStorage
- secret

Mentions of these terms in validation rules are allowed only as negative boundary text.

## 6. Future Validation Output

Future validation summaries should include:

```json
{
  "fixture_schema_validation": "pass_or_fail",
  "forbidden_fields_validation": "pass_or_fail",
  "boundary_and_overclaim_validation": "pass_or_fail",
  "counterexample_validation": "pass_or_fail",
  "model_card_validation": "pass_or_fail",
  "human_review_required": true
}
```

## 7. Stop Conditions

Stop future implementation or validation if:

- any fixture reads real collector dirs
- any fixture parses real `evidence_items.jsonl` or `evidence_items.csv`
- any code calls real API or real LLM
- any code fetches URLs or scrapes
- any output exposes raw author identifiers
- any response strategy is auto-executed
- any output claims full-web, full-platform, official verification, causal proof, or prediction
