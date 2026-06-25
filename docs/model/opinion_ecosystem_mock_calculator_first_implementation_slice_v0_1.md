# Opinion Ecosystem Mock Calculator First Implementation Slice v0.1

Status: docs-only first-slice design. This document does not implement a calculator, backend schema, frontend UI, tests, runtime persistence, file IO, API routes, product behavior, formula scoring, analysis, report generation, Sandbox generation, public event generation, provider execution, collector execution, real API calls, real LLM calls, or Evidence Layer writes.

## A. First Slice Name

Phase 8P-1 Fixture Validator and Run Metadata Skeleton.

## B. Purpose

The future 8P-1 implementation should only validate a synthetic in-memory mock fixture contract and produce a safe mock run metadata object.

It should prove that Sentigraph can enforce model boundaries before it calculates any heat, risk, transition, influence, echo, or response strategy scores.

## C. Expected Future Code Scope If Approved Later

Likely future files only:

- `backend/app/services/opinion_ecosystem_mock_calculator.py`
- `backend/app/tests/test_opinion_ecosystem_mock_calculator.py`

Optional only if necessary in a later implementation:

- `backend/app/schemas/opinion_ecosystem_mock_calculator.py`

Do not create these files as part of this docs-only checkpoint.

## D. Future Pure Function Candidates

Possible future pure functions:

- `validate_mock_fixture_contract(fixture)`
- `find_forbidden_fixture_fields(fixture)`
- `build_mock_calculator_run_metadata(fixture)`
- `validate_output_boundary_flags(run)`
- `calculate_opinion_ecosystem_mock_fixture(fixture)`

For 8P-1, `calculate_opinion_ecosystem_mock_fixture(fixture)` should only call the validator and metadata builder. It must not calculate module scores yet.

## E. Future Fixture Input

Future 8P-1 input should be only an in-memory synthetic fixture object in tests.

It must not read:

- filesystem package files
- real evidence packages
- private collector directories
- local exchange directories
- `evidence_items.jsonl`
- `evidence_items.csv`
- browser profiles
- cookies
- tokens
- sessions
- API keys
- .env values
- salts
- secrets

It must not call:

- real APIs
- real LLMs
- search providers
- platform providers
- vendor providers
- crawler code

## F. Future Minimal Output

Illustrative output shape:

```json
{
  "schema": "sentigraph_opinion_ecosystem_mock_calculator_run_v0_1",
  "run_id": "mock_run_example",
  "fixture_id": "synthetic_fixture_example",
  "model_name": "sentigraph_opinion_ecosystem_mock_calculator",
  "model_version": "0.1",
  "model_status": "mock_local_uncalibrated",
  "coefficient_source": "mock_default",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "scope_note": "Synthetic local mock fixture validation only; not full-web, not full-platform, not official verification, not causal proof, not prediction.",
  "boundary_flags": {
    "not_full_web": true,
    "not_full_platform": true,
    "not_official_verification": true,
    "not_causal_proof": true,
    "not_prediction": true,
    "not_real_api": true,
    "not_real_llm": true,
    "not_crawler": true,
    "not_collector_runtime": true,
    "not_auto_executed": true,
    "human_review_required": true
  },
  "validation_summary": {
    "fixture_contract_validation": "pass_or_fail",
    "forbidden_fields_validation": "pass_or_fail",
    "boundary_and_overclaim_validation": "pass_or_fail",
    "output_boundary_validation": "pass_or_fail"
  },
  "warnings": [],
  "blockers": [],
  "human_review_required": true,
  "module_outputs": {
    "status": "not_calculated_in_8P_1",
    "content_aggregate": null,
    "peoplecluster": null,
    "influencecore": null,
    "echobox": null,
    "response_strategy": null
  }
}
```

8P-1 may also return `module_outputs = {}` if the implementation keeps a clearer metadata-only shape. In either case, the response must state that module scores are not calculated in 8P-1.

## G. Future Forbidden Outputs

Future 8P-1 output must never include:

- `real_hotlist_score`
- `truth_score`
- `official_verified`
- `causal_chain_confirmed`
- `prediction_probability`
- `persuasion_score`
- `auto_execute`
- `target_user_list`
- `raw_author_identifiers`
- production Evidence IDs
- production case IDs
- public download URLs
- signed URLs
- file-byte response paths
- absolute filesystem paths

## H. Future Test List

Future 8P-1 tests should include:

- `test_disabled_from_real_io_by_design`
- `test_minimal_safe_fixture_returns_metadata_only`
- `test_boundary_flags_are_always_present`
- `test_forbidden_identity_fields_block_fixture`
- `test_forbidden_secret_fields_block_fixture`
- `test_auto_execute_blocks_fixture`
- `test_overclaim_flags_block_fixture`
- `test_future_unknown_platform_manual_review`
- `test_no_module_scores_are_calculated_in_first_slice`
- `test_no_real_api_llm_collector_flags`

These tests should use only in-memory synthetic fixtures. They should not read package files, real evidence rows, collector output, or runtime directories.

## I. Not Allowed In First Implementation Slice

The future 8P-1 implementation must not include:

- formula scoring
- heat formula calculation
- PeopleCluster transition calculation
- InfluenceCore pull calculation
- EchoBox saturation calculation
- ResponseStrategy scoring
- frontend UI
- API route
- runtime persistence
- backend storage mutation
- Evidence Layer write
- production case creation
- analysis_run creation
- B-end report runtime
- Sandbox runtime
- public event runtime
- real evidence package reading
- `evidence_items.jsonl` parsing
- `evidence_items.csv` parsing
- private collector access
- real exchange directory configuration
- collector jobs
- provider jobs
- real API calls
- real LLM calls
- external URL fetching
- scraping
- browser automation
- cookie, token, session, browser profile, localStorage, API key, .env, salt, or secret access
- raw author identifier exposure
- auto execution
- public URL generation
- signed URL generation
- file-byte response route
- download route
- ZIP generation
- GitHub Actions workflow recreation

## J. Next Slices Only After 8P-1 Passes

Only after 8P-1 passes validation should later slices be considered:

- 8P-2 ContentAggregate formula only
- 8P-3 InfluenceCore formula only
- 8P-4 EchoBox formula only
- 8P-5 PeopleCluster transition only
- 8P-6 ResponseStrategy comparison only
- 8Q frontend explanatory UI only after backend/local calculator and model card QA are stable

Each later slice must preserve:

- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`
- `human_review_required = true`
- no real API or real LLM
- no collector access
- no evidence_items parsing unless a later explicit gate permits a safe, reviewed, local-only reader
- no Evidence Layer write
- no production case creation
- no analysis_run creation
- no automatic action or strategy execution
