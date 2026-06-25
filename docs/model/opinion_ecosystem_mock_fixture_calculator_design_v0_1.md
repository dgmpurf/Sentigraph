# Opinion Ecosystem Mock Fixture Calculator Design v0.1

Status: docs-only / design-only / future deterministic local mock calculator. This is not implemented, not runtime, not backend schema, not frontend UI, not real API, not real LLM, not crawler, not full-web, not full-platform, not official verification, not causal proof, not prediction, not personality diagnosis, not individual persuasion scoring, and not auto-executed response strategy.

Scope is selected sample / local fixture / imported evidence only.

Required model metadata:

- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`

## 1. Purpose

This document designs a future deterministic local mock fixture calculator for the Sentigraph Opinion Ecosystem Weight Model v0.1.

The future calculator would read synthetic, safe, local mock fixtures and produce versioned model outputs for:

- ContentAggregateWeightV01
- PeopleClusterStateV01
- InfluenceCoreWeightV01
- EchoBoxWeightV01
- ResponseStrategyComparisonV01
- unified run summary / validation summary

It must not calculate from real collector exports, real platform APIs, live crawler output, real LLM output, private records, cookies, sessions, browser profiles, tokens, API keys, or secrets.

## 2. Why This Phase Is Docs-Only

Phase 8O only defines future behavior. It does not create:

- calculator code
- backend schema
- frontend UI
- tests
- runtime files
- executable fixtures
- product behavior changes

This phase exists to freeze the safety boundary and contract before any future implementation.

## 3. Future Calculator Position

The future calculator may only be considered after governance has already reduced risk:

```text
Evidence governance
-> review / dedup complete
-> selected sample or local fixture
-> mock calculator
-> model card QA
-> human review
-> optional future report/Sandbox explanation gate
```

It must never bypass:

- rejected evidence exclusion
- privacy holds
- missing-source blockers
- dedup governance
- source warnings
- review-needed warnings
- model card boundaries
- human review

## 4. Determinism Requirement

The future calculator must be deterministic:

- same fixture input produces same output
- no network calls
- no real API calls
- no real LLM calls
- no crawler or scraping behavior
- no timestamp-dependent score variation except explicit `generated_at` metadata
- no random sampling unless a fixed fixture seed is documented

## 5. Future Input Class

The calculator should accept only the future mock fixture contract described in:

- `opinion_ecosystem_mock_fixture_contract_v0_1.md`

It should not read:

- real collector directories
- `evidence_items.jsonl`
- `evidence_items.csv`
- Evidence Layer production stores
- browser profiles
- localStorage
- cookies
- tokens
- sessions
- `.env`
- runtime analysis artifacts

## 6. Future Output Class

The calculator should produce the future output contract described in:

- `opinion_ecosystem_mock_calculator_output_contract_v0_1.md`

All outputs must include:

- `model_name`
- `model_version`
- `model_status`
- `coefficient_source`
- `calibration_status`
- `empirical_validation`
- `scope_note`
- `boundary_flags`
- `human_review_required`

## 7. Required Module Outputs

### ContentAggregateWeightV01

The future calculator should map safe fixture evidence and aggregate summaries into sample-scoped heat, controversy, risk, and evidence confidence outputs.

### PeopleClusterStateV01

The future calculator should produce anonymous aggregate group / behavioral proxy states only. PeopleCluster must not represent real individuals.

### InfluenceCoreWeightV01

The future calculator should produce content / narrative / official / media / KOL / meme core weights. InfluenceCore must not be rendered as a person ball.

### EchoBoxWeightV01

The future calculator should produce sample-scoped discussion container proxy scores. EchoBox is not a real community map.

### ResponseStrategyComparisonV01

The future calculator should compare transparent response options for human review. It must never output an executable strategy, public-opinion control plan, or `auto_execute`.

## 8. Boundary Flags

Every output must carry boundary flags:

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

## 9. Future Implementation Rule

If Phase 8P is approved later, implementation must start with tests and local synthetic fixtures. It must not begin by adding UI, backend APIs, production storage, report runtime, Sandbox runtime, public routes, download routes, real providers, or real LLM calls.
