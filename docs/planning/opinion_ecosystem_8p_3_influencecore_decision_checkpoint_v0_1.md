# Opinion Ecosystem 8P-3 InfluenceCore Decision Checkpoint v0.1

Status: docs-only decision checkpoint. This document does not implement formulas, backend code, backend tests, frontend UI, API routes, schemas, runtime persistence, product behavior, analysis, report generation, Sandbox generation, public event generation, provider execution, collector execution, real API calls, real LLM calls, or Evidence Layer writes.

## A. Purpose

This checkpoint decides whether Sentigraph should start a future Phase 8P-3 InfluenceCore formula implementation after the Phase 8P-1 fixture validator and Phase 8P-2 ContentAggregate formula calculator.

It is a planning gate before any InfluenceCore formula code. It is not a runtime artifact, not a model-calculation result, not official verification, not causal proof, and not a strategy auto-execution module.

## B. Current State

- Phase 8N-g formula docs exist and remain the model reference.
- Phase 8O mock calculator design exists and remains the calculator design reference.
- Phase 8P deterministic local calculator decision checkpoint exists.
- Phase 8P-1 backend-only fixture validator and run metadata skeleton exists.
- Phase 8P-1 validates in-memory synthetic fixtures before any scoring.
- Phase 8P-1 blocks forbidden fields, overclaims, `auto_execute`, and unknown or future platform runnable implications.
- Phase 8P-2 ContentAggregate formula calculator exists.
- Phase 8P-2 only calculates `ContentAggregateWeightV01`.
- Phase 8P-2 preserves 8P-1 blockers and runtime side-effect flags.
- No InfluenceCore runtime scoring exists yet.
- No EchoBox, PeopleCluster, or ResponseStrategy runtime scoring exists.
- No frontend UI or API route exists for the mock calculator.

## C. Decision Question

Should Sentigraph start the next formula module implementation for InfluenceCore?

Decision answer: yes, but only as a future Phase 8P-3 InfluenceCore-only standalone local formula calculator after 8P-2 remains green.

## D. Prerequisite Check

Prerequisites are present:

- InfluenceCore formula spec exists: `influencecore_weight_model_v0_1.md`.
- Fixture contract exists: `opinion_ecosystem_mock_fixture_contract_v0_1.md`.
- Output contract exists: `opinion_ecosystem_mock_calculator_output_contract_v0_1.md`.
- Counterexample matrix exists: `opinion_ecosystem_mock_calculator_counterexample_matrix_v0_1.md`.
- Validation plan exists: `opinion_ecosystem_mock_calculator_validation_plan_v0_1.md`.
- Integration boundary exists: `opinion_ecosystem_mock_calculator_integration_boundary_v0_1.md`.
- 8P-1 service exists: `backend/app/services/opinion_ecosystem_mock_calculator.py`.
- 8P-1 targeted tests exist: `backend/app/tests/test_opinion_ecosystem_mock_calculator.py`.
- 8P-2 ContentAggregate tests exist in `backend/app/tests/test_opinion_ecosystem_mock_calculator.py`.
- 8P-1 blocks forbidden fields, overclaims, `auto_execute`, and unknown or future platforms before scoring.
- 8P-2 preserves 8P-1 blockers and adds only ContentAggregate scoring.
- No InfluenceCore formula scoring has started.

## E. Option Comparison

### Option 1: Proceed Later With 8P-3 InfluenceCore-Only Standalone Formula Implementation

Allowed future scope:

- `InfluenceCoreWeightV01` output only
- factual credibility
- narrative resonance
- sample exposure
- bridge potential
- backlash risk
- core strength
- attention amplification
- amplification score
- credibility-adjusted influence score
- de-escalation potential
- core risk
- no per-cluster `pull_ik`
- no PeopleCluster stance effect

Required future boundaries:

- validate with 8P-1 first
- keep ContentAggregate output from 8P-2
- keep all 8P-1 boundary flags
- keep all runtime side-effect flags false
- use local synthetic in-memory fixtures only
- keep EchoBox, PeopleCluster, and ResponseStrategy module outputs as not calculated
- call core-level influence potential what it is: content or narrative influence potential, not persuasion probability and not PeopleCluster stance movement

Risk level: acceptable if narrow.

Decision: selected as the only approved future 8P-3 formula slice.

### Option 2: Proceed Later With InfluenceCore Plus PeopleCluster Effect / Pull Implementation

This option would implement InfluenceCore scoring together with cluster-specific `pull_ik`, `stance_effect_ik`, and `stance_effect_ik_adjusted`.

Risk:

- depends on PeopleCluster state that is not implemented as a stable calculator module
- could be misread as individual persuasion or stance movement
- needs cluster stance, openness, fatigue, exposure, and confidence
- increases model-card QA burden before standalone InfluenceCore behavior is proven

Decision: reject for now.

### Option 3: Proceed With All Remaining Modules At Once

Start InfluenceCore, EchoBox, PeopleCluster, and ResponseStrategy in one implementation pass.

Risk:

- too broad
- hard to validate against counterexamples
- makes score regressions hard to isolate
- increases chance of overclaiming model maturity

Decision: reject for now.

### Option 4: Add Frontend UI First

Add a user-facing InfluenceCore score UI before backend/local formula behavior and model-card QA are stable.

Risk:

- scores can appear production-ready too early
- users may treat sample scores as full-web, full-platform, official verification, or causal proof
- visual presentation may hide uncalibrated assumptions

Decision: reject.

### Option 5: Defer Implementation And Keep 8P-2 Only

Keep the calculator at 8P-2 ContentAggregate stage.

Risk:

- safest fallback
- delays validation of content, narrative, official, media, KOL, meme, and explanation core behavior
- leaves important counterexamples untested in runtime

Decision: allowed fallback if future validation risk rises, but not selected now.

## F. Recommended Decision

Recommended decision: proceed with Option 1 as future Phase 8P-3.

Selected future slice:

`InfluenceCore-only standalone local formula calculator`

This decision is ready only as a future implementation prompt. It does not implement formulas now.

## G. Why InfluenceCore Can Follow ContentAggregate

InfluenceCore can follow ContentAggregate because the previous slice already established the safe scoring pattern:

- ContentAggregate now provides evidence confidence, heat, controversy, review risk, and discussion risk context.
- InfluenceCore can still use safe fixture metadata and associated evidence IDs.
- InfluenceCore is content, narrative, source, official, media, KOL, meme, or explanation identity, not a person.
- The first InfluenceCore slice can calculate core-level credibility, resonance, exposure, amplification, de-escalation, and risk without PeopleCluster.
- It can be validated with local synthetic fixtures and counterexamples.
- It can preserve selected-sample scope and uncalibrated model metadata.
- It can preserve all no-real-API, no-real-LLM, no-collector, no-runtime, and no-production-storage boundaries.

InfluenceCore should help explain why a content or narrative core appears salient in the selected sample. It must not claim truth, official verification, causal proof, prediction, or persuasion probability.

## H. Why PeopleCluster-Specific Pull Is Deferred

PeopleCluster-specific pull is deferred because it depends on PeopleCluster state that is not yet implemented as a stable calculator module.

Deferred formulas include:

- `impact_gate_ik`
- `pull_ik`
- `stance_effect_ik`
- `stance_effect_ik_adjusted`
- `InfluenceCoreToClusterEffectV01`

Reasons for deferral:

- `pull_ik` requires PeopleCluster state.
- `stance_effect_ik` requires cluster stance, openness, fatigue, exposure, and confidence.
- Implementing those formulas before PeopleCluster could imply persuasion or stance movement.
- 8P-3 should only produce `InfluenceCoreWeightV01`.
- `InfluenceCoreToClusterEffectV01` should wait until PeopleCluster and model-card QA are stable.

Any "pull" wording in 8P-3 must be translated into core-level influence potential. It must not be described as persuasion probability, target movement, or PeopleCluster stance movement.

## I. Explicitly Not Included In 8P-3

8P-3 must not include:

- EchoBox scoring
- PeopleCluster transition
- ResponseStrategy scoring
- per-cluster InfluenceCore `pull_ik`
- `stance_effect_ik`
- individual persuasion score
- target user list
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
- official verification claims
- causal proof claims
- prediction claims

## J. Future 8P-3 Validation Expectation

Future 8P-3 tests should cover:

- minimal safe InfluenceCore fixture returns `InfluenceCoreWeightV01`
- all 8P-1 boundary flags remain present
- all runtime side-effect flags remain false
- ContentAggregate output from 8P-2 still works
- forbidden fields still block before scoring
- overclaim fields still block before scoring
- `auto_execute` still blocks before scoring
- unknown or future platform still returns `manual_review_required` or warning
- official_statement credible but low exposure has high credibility and low amplification
- viral_meme low credibility can have high amplification but low factual credibility
- low_trust_claim raises core risk but not truth
- third_party_explanation can have bridge and de-escalation potential when credible
- no EchoBox, PeopleCluster, or ResponseStrategy scores
- no `persuasion_score`, `prediction_probability`, `truth_score`, or `official_verified` output
- no per-cluster `pull_ik` or `stance_effect_ik` output

## K. Stop Conditions

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
- target user list generation
- official verification claims
- causal proof claims
- prediction claims
- raw author identifier exposure
- cookie, token, session, browser profile, API key, localStorage, .env, salt, or secret access
- GitHub Actions workflow recreation

## L. Final Ready State Recommendation

Final recommendation:

`ready_for_8P_3_influencecore_formula_implementation_prompt`

This means a later implementation prompt may add InfluenceCore-only local formula behavior, but it must keep 8P-1 validation first, preserve 8P-2 ContentAggregate behavior, keep all runtime side-effect flags false, defer PeopleCluster-specific pull/effects, defer EchoBox, PeopleCluster, and ResponseStrategy, and avoid UI/API/runtime/storage changes.
