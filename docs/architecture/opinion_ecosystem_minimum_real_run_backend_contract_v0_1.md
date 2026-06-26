# Opinion Ecosystem Minimum Real-run Backend Contract v0.1

## A. Purpose

This document defines the backend-only contract for the first generated Opinion Ecosystem run output.

The contract is intended to give the next code slice a narrow, testable target: produce one safe local generated-run object from a bounded fixture-style input, while preserving the current Sentigraph governance boundaries.

## B. Scope

The first backend implementation slice should only create a generated local run output from safe local fixture or sample input.

The first slice must not:

- expose an API route
- integrate with frontend UI
- read real exchange dirs
- access the private collector project
- parse `evidence_items.jsonl`
- parse `evidence_items.csv`
- read original package rows
- write runtime persistence
- write the production Evidence Layer
- create a production case
- create a production `analysis_run`
- generate a B-end report runtime
- generate a Sandbox runtime
- generate a public event runtime

Parsing package evidence files may be considered only after a later bounded input-source design checkpoint explicitly allows it.

## C. Proposed Contract Name

Use:

```text
sentigraph_opinion_ecosystem_run_v0_1
```

## D. Proposed Output Object

The generated run object should be JSON-serializable and deterministic for the same safe input.

Required top-level fields:

- `run_id`
- `run_schema`
- `run_status`
- `case_id`
- `sample_id`
- `input_package_id`
- `input_source_kind`
- `input_scope_note`
- `generated_at`
- `model_version`
- `coefficient_source`
- `calibration_status`
- `empirical_validation`
- `human_review_required`
- `boundary_flags`
- `warnings`
- `blockers`
- `module_outputs`
- `runtime_side_effects`

Required `module_outputs` keys:

- `ContentAggregate`
- `InfluenceCore`
- `EchoBox`
- `PeopleCluster`
- `ResponseStrategyComparisonV01`

Proposed shape:

```json
{
  "run_id": "oe-run-local-fixture-001",
  "run_schema": "sentigraph_opinion_ecosystem_run_v0_1",
  "run_status": "generated_local_fixture_only",
  "case_id": "local-fixture-case",
  "sample_id": "local-fixture-sample",
  "input_package_id": null,
  "input_source_kind": "in_memory_safe_fixture",
  "input_scope_note": "selected_sample_or_local_fixture_only",
  "generated_at": "2026-06-26T00:00:00Z",
  "model_version": "0.1",
  "coefficient_source": "mock_default",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "human_review_required": true,
  "boundary_flags": {
    "selected_sample_only": true,
    "not_full_web": true,
    "not_full_platform": true,
    "not_full_thread": true,
    "not_official_verification": true,
    "not_causal_proof": true,
    "not_prediction": true,
    "not_production_score": true,
    "human_review_required": true,
    "no_auto_execute": true,
    "no_generated_public_response": true
  },
  "warnings": [],
  "blockers": [],
  "module_outputs": {
    "ContentAggregate": {},
    "InfluenceCore": {},
    "EchoBox": {},
    "PeopleCluster": {},
    "ResponseStrategyComparisonV01": {}
  },
  "runtime_side_effects": {
    "called_real_api": false,
    "called_real_llm": false,
    "ran_collector": false,
    "accessed_private_collector": false,
    "read_real_exchange_dir": false,
    "fetched_url": false,
    "scraped_page": false,
    "parsed_evidence_items_file": false,
    "wrote_evidence_layer": false,
    "created_production_case": false,
    "created_analysis_run": false,
    "generated_b_end_report_runtime": false,
    "generated_sandbox_runtime": false,
    "generated_public_event_runtime": false,
    "generated_response_text": false,
    "published_or_sent": false,
    "auto_executed": false
  }
}
```

Field notes:

- `run_id`: local deterministic or generated identifier for this backend-only run object.
- `run_schema`: must equal `sentigraph_opinion_ecosystem_run_v0_1`.
- `run_status`: should distinguish normal local generation from blocked or invalid input states.
- `case_id`: local fixture case identifier; it does not imply production case creation.
- `sample_id`: safe fixture or selected sample identifier.
- `input_package_id`: optional metadata only; null is acceptable for the first in-memory fixture slice.
- `input_source_kind`: expected first value is `in_memory_safe_fixture`.
- `input_scope_note`: must preserve selected-sample boundaries.
- `generated_at`: timestamp for run object creation.
- `model_version`: Opinion Ecosystem model version used by the local calculator.
- `coefficient_source`: source of coefficient values, such as `mock_default`.
- `calibration_status`: must not imply empirical calibration.
- `empirical_validation`: must not imply completed real-world validation.
- `human_review_required`: must remain true.
- `boundary_flags`: reader-facing safety and scope flags.
- `warnings`: non-blocking caveats.
- `blockers`: blocking validation reasons when a normal ready run cannot be produced.
- `module_outputs`: canonical generated module output envelope.
- `runtime_side_effects`: explicit false flags proving the slice did not perform disallowed runtime actions.

## E. Required Boundary Flags

The first generated run must include these boundary flags:

- `selected_sample_only`
- `not_full_web`
- `not_full_platform`
- `not_full_thread`
- `not_official_verification`
- `not_causal_proof`
- `not_prediction`
- `not_production_score`
- `human_review_required`
- `no_auto_execute`
- `no_generated_public_response`

Expected values are `true` for all required boundary flags.

## F. Required Runtime Side-effect Flags

All required runtime side-effect flags must be present and false:

- `called_real_api`
- `called_real_llm`
- `ran_collector`
- `accessed_private_collector`
- `read_real_exchange_dir`
- `fetched_url`
- `scraped_page`
- `parsed_evidence_items_file`
- `wrote_evidence_layer`
- `created_production_case`
- `created_analysis_run`
- `generated_b_end_report_runtime`
- `generated_sandbox_runtime`
- `generated_public_event_runtime`
- `generated_response_text`
- `published_or_sent`
- `auto_executed`

These flags are part of the contract. A successful first slice must prove that it generated only a local run object and did not perform external, production, or publication side effects.

## G. Allowed First Implementation Input

The safest first implementation input is an in-memory safe fixture or an existing local calculator fixture snapshot.

The Dong Lu / Sun Jihai package may be a later candidate only after a separate bounded input-source design checkpoint defines exactly which fields may be read and how package rows remain privacy-safe.

The first implementation slice should not read `docs/samples` package `evidence_items` files unless a later checkpoint explicitly allows package evidence parsing.

## H. Relationship to Existing Calculator

The future implementation should reuse or wrap the existing backend-only pure-local Opinion Ecosystem mock calculator.

Observed existing service file:

```text
backend/app/services/opinion_ecosystem_mock_calculator.py
```

Observed current calculator entrypoint during design review:

```text
calculate_opinion_ecosystem_mock_fixture(fixture)
```

Observed helper names during design review include:

```text
build_mock_calculator_run_metadata(fixture)
validate_output_boundary_flags(run)
```

Codex must inspect actual function names again before implementation. This document defines the desired contract, not an import guarantee.

The future wrapper should preserve the existing 8P-1 through 8P-6 boundaries. If the existing calculator returns lower-case module keys such as `content_aggregate`, `influence_core`, `echo_box`, `people_cluster`, or `response_strategy`, the wrapper may map them into the canonical contract keys:

- `ContentAggregate`
- `InfluenceCore`
- `EchoBox`
- `PeopleCluster`
- `ResponseStrategyComparisonV01`

That mapping must not upgrade trust, infer official verification, produce public response text, or create production analysis state.

## I. What This Contract Is Not

This contract is not:

- an API route
- a frontend integration
- a production calculator
- an Evidence Layer import
- a production case
- a production `analysis_run`
- a B-end report runtime
- a Sandbox runtime
- a public event runtime
- a Strategy Lab runtime
- generated response text
- a real API integration
- a real LLM integration
- a collector integration
- official verification
- causal proof
- prediction
