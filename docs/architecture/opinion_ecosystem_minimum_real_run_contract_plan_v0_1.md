# Opinion Ecosystem Minimum Real-run Contract Plan v0.1

## A. Purpose

This plan defines the future contract for a minimum real-run from a safe local package or sample source to an Opinion Ecosystem deterministic calculator output.

The goal is to bridge the gap between static explanatory UI and a bounded generated run, while preserving strict safety boundaries:

- no live collection
- no real API
- no real LLM
- no collector run
- no production Evidence write
- no production case
- no production `analysis_run`
- no report runtime
- no generated response text
- no public action

## B. Candidate Input Sources

| Candidate input source | Usefulness | Risk | Notes |
| --- | --- | --- | --- |
| Curated local static calculator fixture | Very safe for first contract tests | Too close to current static demo | Useful for schema and UI skeleton verification only |
| Existing Helldivers selected public sample package | Good known demo sample | Smaller sample size and public-event limitations | Useful for continuity with existing screenshots |
| Existing Dong/Sun controlled candidate package | Larger sample and Chinese-event relevance | Still selected sample, not official verification | Strong first real-run candidate if kept local and bounded |
| Future local exchange provider result metadata | Aligns with provider boundary work | Must avoid real exchange dirs without explicit approval | Design-only until approved |
| Future reviewed Evidence package | Best long-term input | Requires review, dedup, privacy, and import gates | Later-stage input after governance gates |

## C. Recommended First Input

Use an existing local selected sample fixture or package path first, not live collector output.

Recommended first candidate:

- Dong/Sun controlled candidate sample, if the next contract task confirms a safe local source path and input schema.

Reason:

- it has a larger sample size than the small Helldivers fixture
- it exercises Chinese C-end and B-end demo language
- it already carries selected-sample and review-needed framing
- it remains safe as long as it is local, bounded, and does not read live exchange directories or call external services

Important boundary:

Dong/Sun remains selected sample only. It is not full-web coverage, not full-platform coverage, not official verification, not causal proof, and not prediction.

## D. Future Run Contract Fields

A future minimum real-run output should include:

```json
{
  "run_id": "opinion_run_...",
  "run_schema": "sentigraph_opinion_ecosystem_run_v0_1",
  "case_id": "case_or_null",
  "sample_id": "sample_or_null",
  "input_package_id": "local_sample_or_package_id",
  "input_scope_note": "selected local sample only",
  "generated_at": "ISO-8601 timestamp",
  "model_version": "opinion_ecosystem_v0_1",
  "coefficient_source": "mock_default_or_documented_local",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "human_review_required": true,
  "boundary_flags": [
    "selected_sample_only",
    "not_full_web",
    "not_full_platform",
    "not_full_thread",
    "not_official_verification",
    "not_causal_proof",
    "not_prediction",
    "not_production_score",
    "human_review_required"
  ],
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
    "fetched_url": false,
    "scraped_page": false,
    "wrote_evidence_layer": false,
    "created_production_case": false,
    "created_analysis_run": false,
    "generated_report_runtime": false,
    "generated_response_text": false,
    "published_or_sent": false,
    "auto_executed": false
  }
}
```

Field requirements:

- `run_id` must be unique for the generated run.
- `run_schema` must version the contract.
- `case_id` or `sample_id` must identify the local bounded input context.
- `input_package_id` must not expose absolute private paths.
- `input_scope_note` must explain selected-sample limitations.
- `generated_at` must record when the local run output was generated.
- `model_version` must identify the deterministic calculator version.
- `coefficient_source` must not imply calibrated production weights unless calibration is actually complete.
- `calibration_status` must remain explicit.
- `empirical_validation` must remain explicit.
- `human_review_required` must remain true for this stage.
- `boundary_flags` must be visible to frontend and reports.
- `warnings` and `blockers` must be shown before score interpretation.
- `module_outputs` must be versioned or internally self-describing in later design.
- `runtime_side_effects` must be all false for minimum real-run.

## E. Frontend Display Requirements

Every generated run display must show:

- generated from selected local sample or package
- not full-web
- not full-platform
- not full-thread
- not official verification
- not causal proof
- not prediction
- not production score
- human review required
- no automatic execution

ResponseStrategyComparisonV01 display must remain:

- human-review-only
- no generated public copy
- no response text generation
- no publish / send / post / execute CTA
- blockers before score

PeopleCluster display must state:

- anonymous aggregate proxy
- not real individual users
- not targeting
- not profiling
- not psychological profile
- not personality diagnosis

InfluenceCore display must state:

- content / narrative / official / media / meme core
- not a person ball
- not an account graph
- not an official cause

## F. Acceptance Criteria Before Manual Playtest

Manual playtest is allowed only if:

- backend can generate a run output on demand
- frontend displays that generated run output
- run output includes model metadata and boundary flags
- default Opinion Ecosystem route smoke passes
- Dong/Sun route smoke passes
- no response text generation exists
- no publish / send / post / execute CTA exists
- no real API, real LLM, or collector side effects occur
- no production Evidence write occurs
- no production case or `analysis_run` is created
- no visible `undefined`
- no visible `NaN`
- no visible `[object Object]`
- no visible 500 or ErrorBoundary

If these criteria are not met, external manual playtest and recording remain deferred.

## G. Explicitly Deferred

The following remain deferred after this contract plan:

- Strategy Lab runtime
- B-end report runtime
- production import
- real collector integration
- calibration
- public deployment
- external delivery
- generated public response text
- publishing, sending, posting, or executing any response

Deferred means not implemented, not implied, and not demoed as available.

