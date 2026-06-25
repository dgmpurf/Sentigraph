# Opinion Ecosystem 8P-4 EchoBox Decision Checkpoint v0.1

Status: docs-only decision checkpoint. This document does not implement formulas, backend code, backend tests, frontend UI, API routes, schemas, runtime persistence, product behavior, analysis, report generation, Sandbox generation, public event generation, provider execution, collector execution, real API calls, real LLM calls, graph extraction, or Evidence Layer writes.

## A. Purpose

This checkpoint decides whether Sentigraph should start a future Phase 8P-4 EchoBox formula implementation after the Phase 8P-1 fixture validator, Phase 8P-2 ContentAggregate formula calculator, and Phase 8P-3 InfluenceCore formula calculator.

It is a planning gate before any EchoBox formula code. It is not a runtime artifact, not a model-calculation result, not a real community map, not a full graph, not official verification, not causal proof, and not prediction.

## B. Current State

- Phase 8N-g formula docs exist and remain the model reference.
- Phase 8O mock calculator design exists and remains the calculator design reference.
- Phase 8P deterministic local calculator decision checkpoint exists.
- Phase 8P-1 backend-only fixture validator and run metadata skeleton exists.
- Phase 8P-2 ContentAggregate formula calculator exists.
- Phase 8P-3 InfluenceCore formula calculator exists.
- Phase 8P-2 only calculates `ContentAggregateWeightV01`.
- Phase 8P-3 only calculates standalone `InfluenceCoreWeightV01`.
- No EchoBox runtime scoring exists yet.
- No PeopleCluster or ResponseStrategy runtime scoring exists.
- No `pull_ik` or `stance_effect_ik` exists.
- No frontend UI or API route exists for the mock calculator.

## C. Decision Question

Should Sentigraph start the next formula module implementation for EchoBox?

Decision answer: yes, but only as a future Phase 8P-4 EchoBox-only standalone local formula calculator after 8P-3 remains green.

## D. Prerequisite Check

Prerequisites are present:

- EchoBox formula spec exists: `echobox_structure_model_v0_1.md`.
- Fixture contract exists: `opinion_ecosystem_mock_fixture_contract_v0_1.md`.
- Output contract exists: `opinion_ecosystem_mock_calculator_output_contract_v0_1.md`.
- Counterexample matrix exists: `opinion_ecosystem_mock_calculator_counterexample_matrix_v0_1.md`.
- Validation plan exists: `opinion_ecosystem_mock_calculator_validation_plan_v0_1.md`.
- Integration boundary exists: `opinion_ecosystem_mock_calculator_integration_boundary_v0_1.md`.
- 8P-1 service exists: `backend/app/services/opinion_ecosystem_mock_calculator.py`.
- 8P-1 targeted tests exist: `backend/app/tests/test_opinion_ecosystem_mock_calculator.py`.
- 8P-2 ContentAggregate tests exist.
- 8P-3 InfluenceCore tests exist.
- 8P-1 blocks forbidden fields, overclaims, `auto_execute`, and unknown or future platforms before scoring.
- 8P-2 preserves 8P-1 blockers and adds only ContentAggregate scoring.
- 8P-3 preserves 8P-1/8P-2 behavior and adds only standalone InfluenceCore scoring.
- No EchoBox formula scoring has started.

## E. Option Comparison

### Option 1: Proceed Later With 8P-4 EchoBox-Only Standalone Formula Implementation

Allowed future scope:

- `EchoBoxWeightV01` output only
- saturation
- closure
- bridge capacity
- constructive breakout
- risk breakout
- echo risk
- no PeopleCluster transition
- no ResponseStrategy scoring
- no real graph extraction
- no real community map

Required future boundaries:

- validate with 8P-1 first
- keep ContentAggregate output from 8P-2
- keep InfluenceCore output from 8P-3
- keep all 8P-1 boundary flags
- keep all runtime side-effect flags false
- use local synthetic in-memory fixtures only
- keep PeopleCluster and ResponseStrategy module outputs as not calculated
- describe bridge and breakout as sample-scoped discussion-structure potential, not causal proof, prediction, persuasion probability, or real-world propagation certainty

Risk level: acceptable if narrow.

Decision: selected as the only approved future 8P-4 formula slice.

### Option 2: Proceed Later With EchoBox Plus PeopleCluster Interaction Together

This option would implement EchoBox and PeopleCluster state/transition behavior together.

Risk:

- PeopleCluster state and transitions require separate boundary and tests
- combining the two could make EchoBox look like real community manipulation or individual tracking
- increases model-card QA burden before standalone EchoBox behavior is proven

Decision: reject for now.

### Option 3: Proceed Later With EchoBox Plus ResponseStrategy Together

This option would implement discussion-structure scoring and strategy comparison in one pass.

Risk:

- strategy scoring requires human-review and no-auto-execution boundaries
- strategy candidate output could be misread as operational instruction
- response strategy should not be mixed with discussion-structure scoring

Decision: reject for now.

### Option 4: Proceed With All Remaining Modules At Once

Start EchoBox, PeopleCluster, and ResponseStrategy in one implementation pass.

Risk:

- too broad
- hard to validate against counterexamples
- too easy to weaken boundaries
- makes score regressions hard to isolate

Decision: reject for now.

### Option 5: Add Frontend UI First

Add a user-facing EchoBox score UI before backend/local formula behavior and model-card QA are stable.

Risk:

- scores can appear production-ready too early
- users may treat sample structure scores as full-platform graph truth
- visual presentation may hide uncalibrated assumptions

Decision: reject.

### Option 6: Defer Implementation And Keep 8P-3 Only

Keep the calculator at 8P-3 ContentAggregate plus InfluenceCore stage.

Risk:

- safest fallback
- delays validation of discussion-container saturation, closure, bridge, breakout, and echo risk behavior

Decision: allowed fallback if future validation risk rises, but not selected now.

## F. Recommended Decision

Recommended decision: proceed with Option 1 as future Phase 8P-4.

Selected future slice:

`EchoBox-only standalone local formula calculator`

This decision is ready only as a future implementation prompt. It does not implement formulas now.

## G. Why EchoBox Can Follow InfluenceCore

EchoBox can follow InfluenceCore because the previous slices established safe scoring inputs and boundaries:

- ContentAggregate now provides evidence confidence, heat, controversy, and risk context.
- InfluenceCore now provides content, narrative, and source core-level scoring.
- EchoBox can use safe fixture metadata, content aggregate refs, influence core refs, stance distributions, cross-cutting proxy summaries, and platform/source spread hints.
- EchoBox is a discussion-container proxy, not a real community map.
- The first EchoBox slice can calculate saturation, closure, bridge, breakout, and echo risk without PeopleCluster transitions.
- It can be validated with local synthetic fixtures and counterexamples.

EchoBox should help explain selected-sample discussion structure. It must not claim real community topology, full graph truth, official verification, causal proof, prediction, hidden targeting, or persuasion probability.

## H. Why PeopleCluster / ResponseStrategy Remain Deferred

PeopleCluster and ResponseStrategy remain deferred because they require different state, review, and safety boundaries:

- PeopleCluster transition requires stance, attention, fatigue, openness, expression, exit/reactivation, and cluster confidence.
- ResponseStrategy comparison requires human-review strategy candidate boundaries and no `auto_execute`.
- EchoBox must not imply individual persuasion, target user lists, or real social graph control.
- 8P-4 should only produce `EchoBoxWeightV01`.
- EchoBox-to-PeopleCluster effects should wait until PeopleCluster and model-card QA are stable.

Any bridge or breakout wording in 8P-4 must be described as sample-scoped discussion-structure potential, not causal proof, prediction, persuasion probability, or real-world propagation certainty.

## I. Explicitly Not Included In 8P-4

8P-4 must not include:

- PeopleCluster transition
- ResponseStrategy scoring
- InfluenceCore-to-cluster `pull_ik`
- `stance_effect_ik`
- individual persuasion score
- target user list
- real community map
- real full graph
- full-platform graph extraction
- frontend UI
- API route
- runtime persistence
- real evidence package reading
- `evidence_items` parsing
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
- official verification claims
- causal proof claims
- prediction claims

## J. Future 8P-4 Validation Expectation

Future 8P-4 tests should cover:

- minimal safe EchoBox fixture returns `EchoBoxWeightV01`
- all 8P-1 boundary flags remain present
- all runtime side-effect flags remain false
- ContentAggregate output from 8P-2 still works
- InfluenceCore output from 8P-3 still works
- forbidden fields still block before scoring
- overclaim fields still block before scoring
- `auto_execute` still blocks before scoring
- unknown or future platform still returns `manual_review_required` or warning
- strong echo no breakout case: high saturation/closure but low breakout
- bridgeable controversy case: high controversy but bridge capacity nonzero/high
- sealed echo case: high closure and low bridge capacity
- low confidence / low trust evidence lowers EchoBox confidence
- duplicate evidence does not artificially increase saturation without folded warning
- one-sided high heat does not automatically mean high closure or full echo chamber
- no PeopleCluster or ResponseStrategy scores
- no `pull_ik` or `stance_effect_ik` output
- no real community map, full graph, or target user list
- no `persuasion_score`, `prediction_probability`, `truth_score`, or `official_verified` output

## K. Stop Conditions

Stop any future task if it attempts:

- real API calls
- real LLM calls
- collector access
- real exchange directory configuration
- `evidence_items` parsing
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
- target user list generation
- real community map
- full graph extraction
- official verification claims
- causal proof claims
- prediction claims
- raw author identifier exposure
- cookie, token, session, browser profile, API key, localStorage, .env, salt, or secret access
- GitHub Actions workflow recreation

## L. Final Ready State Recommendation

Final recommendation:

`ready_for_8P_4_echobox_formula_implementation_prompt`

This means a later implementation prompt may add EchoBox-only local formula behavior, but it must keep 8P-1 validation first, preserve 8P-2 ContentAggregate behavior, preserve 8P-3 InfluenceCore behavior, keep all runtime side-effect flags false, defer PeopleCluster and ResponseStrategy, avoid real graph/community-map claims, and avoid UI/API/runtime/storage changes.
