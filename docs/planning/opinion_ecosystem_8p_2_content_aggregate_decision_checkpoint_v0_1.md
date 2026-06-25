# Opinion Ecosystem 8P-2 ContentAggregate Decision Checkpoint v0.1

Status: docs-only decision checkpoint. This document does not implement formulas, backend code, backend tests, frontend UI, API routes, schemas, runtime persistence, product behavior, analysis, report generation, Sandbox generation, public event generation, provider execution, collector execution, real API calls, real LLM calls, or Evidence Layer writes.

## A. Purpose

This checkpoint decides whether Sentigraph should start a future Phase 8P-2 ContentAggregate formula implementation after the Phase 8P-1 fixture validator and metadata skeleton.

It is a planning gate before any formula code. It is not a runtime artifact and not a model-calculation result.

## B. Current State

- Phase 8N-g formula docs exist and remain docs-only.
- Phase 8O mock calculator design exists and remains docs-only.
- Phase 8P deterministic local calculator decision checkpoint exists.
- Phase 8P-1 backend-only validator skeleton exists.
- Phase 8P-1 validates in-memory synthetic fixtures and outputs metadata only.
- Phase 8P-1 blocks forbidden fields, overclaims, `auto_execute`, and unknown/future platform runnable implications.
- Phase 8P-1 does not calculate formulas.
- No ContentAggregate runtime scoring exists yet.
- No InfluenceCore, EchoBox, PeopleCluster, or ResponseStrategy runtime scoring exists.
- No frontend UI or API route exists for the mock calculator.
- Current runtime side-effect flags remain false by design.

## C. Decision Question

Should Sentigraph start the first formula module implementation for ContentAggregate?

Decision answer: yes, but only as a future 8P-2 ContentAggregate-only local formula calculator after 8P-1 remains green.

## D. Prerequisite Check

Prerequisites are present:

- ContentAggregate formula spec exists: `content_aggregate_heat_risk_model_v0_1.md`.
- Fixture contract exists: `opinion_ecosystem_mock_fixture_contract_v0_1.md`.
- Output contract exists: `opinion_ecosystem_mock_calculator_output_contract_v0_1.md`.
- Counterexample matrix exists: `opinion_ecosystem_mock_calculator_counterexample_matrix_v0_1.md`.
- Validation plan exists: `opinion_ecosystem_mock_calculator_validation_plan_v0_1.md`.
- Integration boundary exists: `opinion_ecosystem_mock_calculator_integration_boundary_v0_1.md`.
- 8P-1 service exists: `backend/app/services/opinion_ecosystem_mock_calculator.py`.
- 8P-1 targeted tests exist: `backend/app/tests/test_opinion_ecosystem_mock_calculator.py`.
- 8P-1 blocks forbidden fields, overclaims, `auto_execute`, and unknown/future platforms.
- No formula scoring has started.

## E. Option Comparison

### Option 1: Proceed With 8P-2 ContentAggregate-Only Formula Implementation

Allowed future scope:

- evidence base weight
- evidence confidence
- sample_heat_score
- sample_controversy_score
- discussion_risk_score
- review_risk_score
- overall_risk_score
- `ContentAggregateWeightV01` output only

Required future boundaries:

- validate with 8P-1 first
- keep all 8P-1 boundary flags
- keep all runtime side-effect flags false
- use in-memory synthetic fixtures only
- keep other module outputs as not calculated

Risk level: acceptable if narrow.

Decision: selected as the only approved future first formula slice.

### Option 2: Evidence Confidence And Review Risk Only

Allowed future scope would calculate only evidence confidence and review risk while deferring heat, controversy, and discussion risk.

Risk:

- lower formula risk
- but creates too many micro phases and delays testing the core ContentAggregate contract
- still needs most of the same weighting and missing-data policy

Decision: not selected.

### Option 3: All Formula Modules At Once

Start ContentAggregate, InfluenceCore, EchoBox, PeopleCluster, and ResponseStrategy in one implementation pass.

Risk:

- too broad
- hard to validate against counterexamples
- increases chance of overclaiming model maturity
- makes it harder to isolate score regressions

Decision: reject for now.

### Option 4: Frontend UI First

Add a user-facing score UI before backend/local formula behavior and model-card QA are stable.

Risk:

- scores can appear production-ready too early
- users may treat sample scores as full-web or official truth
- visual presentation may hide uncalibrated assumptions

Decision: reject.

### Option 5: Defer Implementation And Keep 8P-1 Only

Keep the calculator at validator/metadata skeleton stage.

Risk:

- safest fallback
- delays formula validation and counterexample hardening

Decision: allowed fallback if future validation risk rises, but not selected now.

## F. Recommended Decision

Recommended decision: proceed with Option 1 as future Phase 8P-2.

Selected future slice:

`ContentAggregate-only local formula calculator`

This decision is ready only as a future implementation prompt. It does not implement formulas now.

## G. Why 8P-2 Can Calculate ContentAggregate But Not Other Modules

ContentAggregate is the safest first formula module because it uses evidence metadata and aggregate summaries that are already part of the safe fixture contract:

- trust labels and trust_score
- review_status
- duplicate_group_id and duplicate_count
- relevance_label
- recency_label
- stance_hint
- emotion_intensity_hint
- source_url_present
- safe aggregate summaries

ContentAggregate does not require:

- PeopleCluster behavioral transition
- InfluenceCore pull / amplification / de-escalation
- EchoBox structure graph or bridge/breakout structure
- ResponseStrategy benefit, cost, or strategy score

It can be validated with local synthetic fixtures and counterexamples:

- duplicate evidence folded, not infinitely amplified
- low-trust emotional screenshot lowers confidence and raises review risk
- one-sided high heat does not imply high controversy
- rejected evidence excluded before analysis-ready scoring

## H. Explicitly Not Included In 8P-2

8P-2 must not include:

- InfluenceCore scoring
- EchoBox scoring
- PeopleCluster transition
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
- production Evidence Layer write
- production case creation
- analysis_run creation
- B-end report runtime
- Sandbox runtime
- public event runtime
- public delivery
- auto execution
- individual persuasion scoring

## I. Future 8P-2 Validation Expectation

Future 8P-2 tests should cover:

- minimal safe ContentAggregate fixture returns `ContentAggregateWeightV01`
- all 8P-1 boundary flags remain present
- all runtime side-effect flags remain false
- forbidden fields still block
- overclaim fields still block
- `auto_execute` still blocks
- unknown/future platform still returns `manual_review_required`
- rejected evidence excluded from analysis-ready scoring
- duplicate evidence folded and not infinitely amplified
- low-trust emotional screenshot lowers confidence and raises review risk
- one-sided high heat does not imply high controversy
- missing optional components re-normalize safely
- no InfluenceCore, EchoBox, PeopleCluster, or ResponseStrategy scores
- no `prediction_probability`, `persuasion_score`, `truth_score`, or `official_verified` output

## J. Stop Conditions

Stop any future task if it attempts:

- real API calls
- real LLM calls
- collector access
- real exchange directory configuration
- `evidence_items.jsonl` parsing
- `evidence_items.csv` parsing
- Evidence Layer write
- production case creation
- analysis_run creation
- B-end report runtime
- Sandbox runtime
- public event runtime
- frontend score UI before model-card QA
- public delivery
- auto execution
- individual persuasion scoring
- raw author identifier exposure
- cookie, token, session, browser profile, API key, localStorage, .env, salt, or secret access
- GitHub Actions workflow recreation

## K. Final Ready State Recommendation

Final recommendation:

`ready_for_8P_2_content_aggregate_formula_implementation_prompt`

This means a later implementation prompt may add ContentAggregate-only local formula behavior, but it must keep 8P-1 validation first, keep all runtime side-effect flags false, defer all other modules, and avoid UI/API/runtime/storage changes.
