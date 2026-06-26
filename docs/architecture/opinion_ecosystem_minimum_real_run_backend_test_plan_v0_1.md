# Opinion Ecosystem Minimum Real-run Backend Test Plan v0.1

## A. Purpose

This document defines tests for the future first backend code slice that generates a local Opinion Ecosystem run object.

The tests should prove that the run object is deterministic, boundary-preserving, backend-only, local-only, and safe to inspect before any API, frontend, runtime persistence, or production analysis work begins.

## B. Required Future Tests

The future implementation should include tests that prove:

- generated run contains `run_id` and `run_schema`
- generated run has `run_schema = sentigraph_opinion_ecosystem_run_v0_1`
- generated run includes model metadata
- generated run includes all required boundary flags
- generated run has `runtime_side_effects` with every required flag set to false
- generated run includes `ContentAggregate`, `InfluenceCore`, `EchoBox`, `PeopleCluster`, and `ResponseStrategyComparisonV01` outputs when calculator input is valid
- blocked fixture does not produce a normal ready run
- forbidden fields remain blocked
- `auto_execute` remains blocked
- unknown or future platform remains `manual_review_required`
- `response_text` is not produced
- `generated_public_message` is not produced
- `target_user_list` is not produced
- `persuasion_score` is not produced
- `truth_score` is not produced
- `official_verified` is not produced
- `prediction_probability` is not produced
- no file IO is required for the first implementation slice
- no API route is added
- no frontend changes are required
- no runtime persistence is created
- no Evidence Layer write occurs
- no production case is created
- no production `analysis_run` is created
- no collector access occurs
- no real API is called
- no real LLM is called
- no URL fetch occurs
- no scraping occurs

Concrete expected assertions for the first slice:

```text
run["run_schema"] == "sentigraph_opinion_ecosystem_run_v0_1"
run["human_review_required"] is True
run["boundary_flags"]["not_full_web"] is True
run["boundary_flags"]["not_official_verification"] is True
run["boundary_flags"]["no_generated_public_response"] is True
all(value is False for value in run["runtime_side_effects"].values())
"response_text" not in serialized_run
"generated_public_message" not in serialized_run
"target_user_list" not in serialized_run
"persuasion_score" not in serialized_run
"truth_score" not in serialized_run
"official_verified" not in serialized_run
"prediction_probability" not in serialized_run
```

## C. Candidate Test Files For Future Implementation

Preferred future test file:

```text
backend/app/tests/test_opinion_ecosystem_minimum_real_run.py
```

Lower-risk alternative after inspection:

```text
backend/app/tests/test_opinion_ecosystem_mock_calculator.py
```

The preferred path is a new focused test file because the generated-run wrapper contract is distinct from the existing mock calculator formulas. Extending the existing calculator test file is acceptable only if inspection shows the wrapper is small and directly coupled to the current fixture helpers.

No test file should be created during this docs-only 8S-1 phase.

## D. Validation Command For Future Implementation

For the future backend-only implementation slice, recommended validation is:

```powershell
python -m pytest backend/app/tests/test_opinion_ecosystem_minimum_real_run.py -q
python -m pytest backend/app/tests/test_opinion_ecosystem_mock_calculator.py -q
python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py -q
python -m pytest backend/app/tests/test_external_collector_bridge.py -q
python -m pytest backend/app/tests/test_local_exchange_reader.py -q
python -m py_compile backend/app/services/<touched-service-file>.py
git diff --check
```

The first tiny slice should not require full `python -m pytest` unless code touch expands beyond the expected wrapper and focused tests.

## E. Stop Conditions

Stop the future implementation and return for approval if it tries to add or perform any of these:

- API route
- frontend integration
- runtime persistence
- reading real exchange dirs
- parsing `evidence_items.jsonl`
- parsing `evidence_items.csv`
- production Evidence write
- production case creation
- production `analysis_run`
- B-end report runtime
- Sandbox runtime
- public event runtime
- real API call
- real LLM call
- collector access
- generated response text
- `auto_execute`
- publish / send / post behavior
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

These stop conditions are contract boundaries, not missing work.
