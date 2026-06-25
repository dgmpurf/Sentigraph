# Opinion Ecosystem 8P Deterministic Local Calculator Decision Checkpoint v0.1

Status: docs-only decision checkpoint. This document does not implement a calculator, backend schema, frontend UI, tests, runtime persistence, product behavior, analysis, report generation, Sandbox generation, public event generation, provider execution, collector execution, real API calls, real LLM calls, or Evidence Layer writes.

## A. Purpose

This checkpoint decides whether Sentigraph should start a future Phase 8P implementation for a deterministic local mock calculator, and if so, what the smallest safe first implementation slice should be.

It exists before any implementation. It is a governance checkpoint, not a runtime checkpoint.

## B. Current State

- Phase 8N-g model formulas are docs-only.
- Phase 8O mock fixture calculator design is docs-only.
- No runtime mock calculator exists.
- No backend schema exists for this calculator.
- No frontend UI exists for this calculator.
- No tests exist yet for calculator implementation.
- No production Evidence import, production case, analysis_run, B-end report runtime, Sandbox runtime, or public event runtime exists for this model.
- The model docs consistently require `coefficient_source = mock_default`, `calibration_status = uncalibrated`, `empirical_validation = not_started`, and `human_review_required = true`.
- Existing model docs define strong boundary flags against full-web claims, full-platform claims, official verification claims, causal proof claims, prediction claims, auto execution, individual profiling, real APIs, real LLMs, crawler behavior, private collector access, and secret exposure.

## C. Decision Question

Should Sentigraph start a very small deterministic local mock calculator implementation?

Decision answer: yes, but only as a future 8P-1 fixture validator and run metadata skeleton. The first implementation slice must not calculate model scores.

## D. Prerequisite Check

The following prerequisites are present in docs and sufficient for a narrow implementation-start decision:

- Model docs exist:
  - `opinion_ecosystem_weight_model_v0_1.md`
  - `content_aggregate_heat_risk_model_v0_1.md`
  - `peoplecluster_transition_model_v0_1.md`
  - `influencecore_weight_model_v0_1.md`
  - `echobox_structure_model_v0_1.md`
  - `response_strategy_comparison_model_v0_1.md`
- Model card and integration plan exist:
  - `opinion_ecosystem_weight_model_card_v0_1.md`
  - `opinion_ecosystem_weight_model_integration_plan_v0_1.md`
- Fixture contract docs exist:
  - `opinion_ecosystem_mock_fixture_calculator_design_v0_1.md`
  - `opinion_ecosystem_mock_fixture_contract_v0_1.md`
- Output contract docs exist:
  - `opinion_ecosystem_mock_calculator_output_contract_v0_1.md`
- Counterexample matrix exists:
  - `opinion_ecosystem_mock_calculator_counterexample_matrix_v0_1.md`
- Validation plan exists:
  - `opinion_ecosystem_mock_calculator_validation_plan_v0_1.md`
- Integration boundary exists:
  - `opinion_ecosystem_mock_calculator_integration_boundary_v0_1.md`
- Source boundaries are consistent: current docs keep the calculator local, deterministic, mock-only, uncalibrated, non-predictive, non-official, and human-review-gated.
- No implementation has started yet for this calculator.

## E. Option Comparison

### Option 1: Fixture Validation And Run Metadata Skeleton Only

Start with pure fixture validation and run metadata skeleton only.

Allowed future scope:

- no formulas yet
- no file reading
- no API routes
- no UI
- no runtime directory writes
- only safe in-memory synthetic dict/object fixtures in future tests
- only validation of fixture contract, forbidden fields, boundary flags, overclaim blockers, and run metadata shape

Risk level: lowest.

Decision: selected as the only approved future first slice.

### Option 2: ContentAggregate Formula Calculator First

Start with the ContentAggregate formula calculator before the validation skeleton.

Risk:

- formulas are new and uncalibrated
- output may be misunderstood as real risk, heat, or empirical score
- boundary enforcement would arrive after scoring instead of before scoring

Decision: defer.

### Option 3: Full Module Calculator

Start with all modules at once: ContentAggregate, PeopleCluster, InfluenceCore, EchoBox, and ResponseStrategy.

Risk:

- too broad for the first implementation
- makes debugging and governance validation harder
- can accidentally imply model maturity

Decision: reject for now.

### Option 4: Frontend UI First

Start with a user-facing calculator or visualization UI before local validator behavior exists.

Risk:

- can make docs-only formulas appear implemented or production-ready
- can overstate a mock local model as real product intelligence
- can hide missing boundary enforcement behind presentation

Decision: reject for now.

### Option 5: Defer Implementation And Keep Docs-Only

Keep the calculator docs-only for another checkpoint.

Risk:

- safest if there is uncertainty
- slows model validation and fixture contract hardening

Decision: allowed fallback, but not selected because Option 1 is narrow enough to start later.

## F. Recommended Decision

Recommended decision: proceed only with Option 1 as future Phase 8P-1.

Selected first implementation slice:

`fixture contract validator + run metadata / boundary flag skeleton`

Required first-slice boundary:

- no formula scoring
- no module outputs beyond empty or explicitly not-calculated placeholders
- no file IO
- no API route
- no frontend UI
- no runtime persistence
- no real package reading
- no private collector access
- no evidence_items parsing
- no Evidence Layer write
- no production case
- no analysis_run
- no B-end report runtime
- no Sandbox or public event runtime

## G. Why First Slice Should Not Calculate Scores Yet

Formula scoring should be deferred because:

- formulas are new and uncalibrated
- first implementation should prove boundary enforcement before scoring
- output metadata validation and forbidden field validation are safer first
- future formula modules can be added one at a time after the validator proves it can block unsafe fixtures and overclaim flags
- early score output may be misread as real heat, truth, risk, prediction, or causal proof

The first implementation should answer: can Sentigraph safely accept a synthetic mock fixture object and return only governance metadata?

It should not answer: what is the event score?

## H. Explicitly Not Included In First Slice

The future 8P-1 slice must not include:

- heat formula calculation
- ContentAggregate scoring
- PeopleCluster transition calculation
- InfluenceCore pull calculation
- EchoBox saturation calculation
- ResponseStrategy scoring
- frontend UI
- API route
- runtime persistence
- real evidence package reading
- `evidence_items.jsonl` parsing
- `evidence_items.csv` parsing
- collector access
- real API calls
- real LLM calls
- Evidence Layer write
- production case creation
- analysis_run creation
- B-end report runtime
- Sandbox runtime
- public event runtime
- public delivery
- auto execution

## I. Future 8P-1 Validation Expectation

Future tests should cover:

- accepted minimal safe fixture returns run metadata
- all required boundary flags are present
- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`
- `human_review_required = true`
- `raw_author_id` blocks
- `author_name` blocks
- `profile_url` blocks
- cookie blocks
- token blocks
- session blocks
- browser profile blocks
- localStorage blocks
- secret-like fields block
- `auto_execute` blocks
- full_web_claim blocks
- full_platform_claim blocks
- official_verification_claim blocks
- causal_proof_claim blocks
- prediction_claim blocks
- future_forum or unknown platform produces `manual_review_required` or an unsupported warning
- no formula outputs are calculated
- no real API, real LLM, crawler, collector, or file IO flags are enabled

## J. Stop Conditions

Stop any future implementation or validation task if it attempts any of the following:

- real API call
- real LLM call
- private collector access
- real exchange directory configuration
- `evidence_items.jsonl` parsing
- `evidence_items.csv` parsing
- Evidence Layer write
- production case creation
- analysis_run creation
- B-end report runtime
- Sandbox runtime
- public event runtime
- public delivery
- public URL or signed URL generation
- file-byte response route
- download route
- browser profile, cookie, token, session, API key, localStorage, .env, salt, or secret access
- raw author identifier exposure
- GitHub Actions workflow recreation

## K. Final Ready State Recommendation

Final recommendation:

`ready_for_8P_1_fixture_validator_skeleton_implementation_prompt`

This means the next implementation prompt may be prepared for a tiny local pure-function validator skeleton, but it must keep formula scoring deferred and keep all runtime, frontend, API, collector, and production-storage boundaries closed.
