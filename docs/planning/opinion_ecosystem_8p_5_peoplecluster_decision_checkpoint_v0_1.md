# Opinion Ecosystem 8P-5 PeopleCluster Decision Checkpoint v0.1

Status: docs-only / planning checkpoint / no runtime implementation.

This checkpoint decides whether Sentigraph should start a future Phase 8P-5 PeopleCluster transition implementation after the Phase 8P-1 fixture validator, Phase 8P-2 ContentAggregate calculator, Phase 8P-3 InfluenceCore calculator, and Phase 8P-4 EchoBox calculator.

It is not a runtime artifact, not an analysis result, not a production Evidence Layer write, not official verification, not causal proof, and not prediction.

## A. Purpose

This document is a docs-only decision checkpoint before any PeopleCluster transition implementation.

Its purpose is to decide the next safe implementation slice and preserve the existing Sentigraph boundaries:

- PeopleCluster means anonymous aggregate group / behavioral proxy.
- PeopleCluster is not a real person.
- PeopleCluster is not a real account.
- PeopleCluster is not a psychological profile.
- PeopleCluster is not personality diagnosis.
- PeopleCluster is not individual tracking.
- PeopleCluster is not an individual persuasion target.
- PeopleCluster is not a target user list.
- PeopleCluster is not prediction.
- PeopleCluster is not causal proof.
- PeopleCluster is not official verification.
- PeopleCluster is not an auto-executed response strategy.

## B. Current State

Current completed context:

- 8N-g formula docs exist.
- 8O mock calculator design exists.
- 8P decision checkpoint exists.
- 8P-1 backend-only validator skeleton exists.
- 8P-2 ContentAggregate formula calculator exists.
- 8P-3 InfluenceCore formula calculator exists.
- 8P-4 EchoBox formula calculator exists.
- 8P-2 only calculates `ContentAggregateWeightV01`.
- 8P-3 only calculates standalone `InfluenceCoreWeightV01`.
- 8P-4 only calculates standalone `EchoBoxWeightV01`.
- No PeopleCluster runtime scoring exists yet.
- No ResponseStrategy runtime scoring exists.
- No `pull_ik` exists.
- No `stance_effect_ik` exists.
- No frontend UI or API route exists for the mock calculator.

The current calculator chain is therefore:

```text
8P-1 fixture validation
-> 8P-2 ContentAggregateWeightV01
-> 8P-3 InfluenceCoreWeightV01
-> 8P-4 EchoBoxWeightV01
-> PeopleCluster not calculated
-> ResponseStrategy not calculated
```

## C. Decision Question

Should Sentigraph start the next formula / transition module implementation for PeopleCluster?

Decision answer: yes, but only as a future Phase 8P-5 PeopleCluster-only anonymous aggregate transition calculator.

## D. Prerequisite Check

Prerequisites now available:

- PeopleCluster transition formula spec exists: `docs/model/peoplecluster_transition_model_v0_1.md`.
- Fixture contract exists.
- Output contract exists.
- Counterexample matrix exists.
- Validation plan exists.
- Integration boundary exists.
- 8P-1 service exists.
- 8P-1 targeted tests exist.
- 8P-2 ContentAggregate tests exist.
- 8P-3 InfluenceCore tests exist.
- 8P-4 EchoBox tests exist.
- 8P-1 blocks forbidden fields, overclaims, `auto_execute`, and unknown future platforms.
- 8P-2 preserves 8P-1 blockers and adds only ContentAggregate scoring.
- 8P-3 preserves 8P-1 / 8P-2 behavior and adds only standalone InfluenceCore scoring.
- 8P-4 preserves 8P-1 / 8P-2 / 8P-3 behavior and adds only standalone EchoBox scoring.
- No PeopleCluster transition scoring has started.

The prerequisite state is adequate for a future PeopleCluster-only implementation slice, as long as it remains local, deterministic, anonymous, aggregate, and non-predictive.

## E. Option Comparison

### Option 1: Proceed Later With 8P-5 PeopleCluster-Only Standalone Aggregate Transition Implementation

Allowed scope:

- `PeopleClusterStateV01` output only
- aggregate stance state / stance distribution proxy
- stance confidence
- attention level
- fatigue level
- expression intensity / expression tendency
- exit risk / withdrawal tendency
- reactivation potential
- openness / confidence radius proxy where existing docs define it
- aggregate transition pressure / `state_delta` only where existing docs define it
- no individual identity
- no target user list
- no persuasion probability
- no `pull_ik`
- no `stance_effect_ik`
- no ResponseStrategy scoring

This is the only recommended next slice because it follows the established ordering: content, core, discussion structure, then anonymous aggregate group state.

Decision: selected as the future 8P-5 slice.

### Option 2: Proceed Later With PeopleCluster Plus InfluenceCore-To-Cluster `pull_ik` / `stance_effect_ik`

This option would implement PeopleCluster state together with per-cluster InfluenceCore pull and stance-effect fields.

Rejected for now because:

- `pull_ik` and `stance_effect_ik` can be misread as individual persuasion or causal stance movement.
- Those formulas require stricter model-card QA and interpretation rules.
- They should wait until standalone `PeopleClusterStateV01` is stable.
- `InfluenceCoreToClusterEffectV01` must remain deferred.

### Option 3: Proceed Later With PeopleCluster Plus ResponseStrategy Together

This option would implement PeopleCluster state and strategy comparison in the same pass.

Rejected for now because:

- ResponseStrategy comparison requires strategy candidates, benefit / cost scoring, recommendation level, and human review.
- Strategy outputs can be misread as automated public-opinion control if implemented too early.
- ResponseStrategy must preserve `no auto_execute`.
- ResponseStrategy should remain a separate later slice.

### Option 4: Proceed With All Remaining Modules At Once

This option would implement PeopleCluster, InfluenceCore-to-cluster effects, ResponseStrategy, and any remaining outputs in one pass.

Rejected for now because:

- The scope is too broad.
- It weakens reviewability.
- It makes boundary regressions harder to isolate.
- It increases risk of accidental UI / API / runtime / storage expansion.

### Option 5: Add Frontend UI First

This option would add user-facing PeopleCluster score UI before backend/model-card QA.

Rejected because:

- PeopleCluster transitions could appear production-ready.
- PeopleCluster could be misread as real-person profiling.
- PeopleCluster could be misread as targetable audience segmentation.
- The backend/local calculator and model-card QA should come first.

### Option 6: Defer Implementation And Keep 8P-4 Only

This fallback is allowed if future safety review finds the PeopleCluster transition language too risky.

If selected later, Sentigraph should stay at:

```text
ContentAggregate + InfluenceCore + EchoBox only
```

and keep PeopleCluster and ResponseStrategy as not calculated.

## F. Recommended Decision

Recommended decision: proceed with Option 1 as future Phase 8P-5.

Selected future implementation slice:

```text
PeopleCluster-only anonymous aggregate transition calculator
```

Decision state:

```text
ready_for_8P_5_peoplecluster_transition_implementation_prompt
```

This does not authorize runtime implementation in this docs-only task. It only prepares the next prompt boundary.

## G. Why PeopleCluster Can Follow EchoBox

PeopleCluster can follow EchoBox because the previous slices now provide safer upstream context:

- ContentAggregate provides evidence confidence, heat, controversy, risk, trust, review, and duplication context.
- InfluenceCore provides content / narrative / official / media / meme / explanation core-level scoring.
- EchoBox provides discussion-structure context: saturation, closure, bridge, breakout, and echo risk.
- PeopleCluster can use safe fixture metadata and upstream aggregate outputs to compute anonymous aggregate state proxies.
- PeopleCluster is not a person and not a psychological diagnosis.
- The first PeopleCluster slice can calculate aggregate state, fatigue, attention, expression, exit risk, and reactivation potential without ResponseStrategy.
- The first PeopleCluster slice can avoid individual targeting.
- The first PeopleCluster slice can be validated with local synthetic fixtures and counterexamples.

The first implementation must describe transition wording as sample-scoped aggregate behavior. It must not describe private belief, individual mental change, persuasion probability, official verification, causal proof, or future prediction.

## H. Why `pull_ik` / `stance_effect_ik` Remain Deferred

`pull_ik` and `stance_effect_ik` remain deferred because:

- They can be interpreted as persuasion.
- They can be interpreted as causal stance movement.
- They require careful interpretation across InfluenceCore, EchoBox, and PeopleCluster.
- They should not appear before `PeopleClusterStateV01` and model-card QA are stable.
- 8P-5 should only produce `PeopleClusterStateV01`.
- `InfluenceCoreToClusterEffectV01` should remain deferred.

Any future wording around pull or stance effect must be framed as sample-scoped explanatory proxy, not individual persuasion, not causal proof, and not prediction.

## I. Why ResponseStrategy Remains Deferred

ResponseStrategy remains deferred because:

- ResponseStrategy comparison requires explicit strategy candidates.
- ResponseStrategy comparison requires benefit / cost scoring.
- ResponseStrategy comparison requires recommendation level boundaries.
- ResponseStrategy comparison requires human review.
- It can be misread as automated public-opinion control if implemented too early.
- It must preserve no `auto_execute`.
- It should remain a later 8P-6 slice.

PeopleCluster 8P-5 may prepare anonymous aggregate state, but it must not recommend an action, execute an action, or claim a strategy will cause a result.

## J. Explicitly Not Included In 8P-5

8P-5 must not include:

- ResponseStrategy scoring
- `pull_ik`
- `stance_effect_ik`
- `stance_effect_ik_adjusted`
- `InfluenceCoreToClusterEffectV01`
- individual persuasion score
- target user list
- real user / account identity
- cross-platform person matching
- psychological profiling
- personality diagnosis
- frontend UI
- API route
- runtime persistence
- real evidence package reading
- `evidence_items` parsing
- collector access
- real API
- real LLM
- production Evidence Layer write
- production case
- `analysis_run`
- B-end report runtime
- Sandbox / public event runtime

The only acceptable 8P-5 output is a local deterministic `PeopleClusterStateV01` object derived from already safe in-memory fixture metadata and upstream local calculator outputs.

## K. Future 8P-5 Validation Expectation

Future 8P-5 tests should cover:

- minimal safe PeopleCluster fixture returns `PeopleClusterStateV01`
- all 8P-1 boundary flags remain present
- all runtime side-effect flags remain false
- ContentAggregate output from 8P-2 still works
- InfluenceCore output from 8P-3 still works
- EchoBox output from 8P-4 still works
- forbidden fields still block before PeopleCluster scoring
- overclaim fields still block before PeopleCluster scoring
- `auto_execute` still blocks before PeopleCluster scoring
- unknown / future platform still returns manual-review-required or warning behavior
- PeopleCluster output never exposes raw author IDs, author names, or profile URLs
- PeopleCluster output never includes `target_user_list`
- high heat does not imply all people changed stance
- high EchoBox closure can raise aggregate fatigue / exit risk only as sample-scoped proxy
- bridgeable mixed cluster can have nonzero openness / reactivation potential without persuasion claims
- missing previous state yields current-state-only or insufficient-data warning
- rejected evidence is excluded from aggregate transition scoring
- low trust evidence lowers confidence and raises warning
- duplicate evidence is folded; `duplicate_count` can contribute only as bounded repetition / activity signal
- no ResponseStrategy scores
- no `pull_ik` / `stance_effect_ik` output
- no `persuasion_score`, `prediction_probability`, `truth_score`, or `official_verified` output
- deterministic same fixture returns same output

## L. Stop Conditions

Stop any future 8P-5 implementation attempt if it introduces:

- real API
- real LLM
- collector access
- `evidence_items` parsing
- Evidence Layer write
- production case
- `analysis_run`
- B-end report runtime
- Sandbox / public event runtime
- frontend score UI before model-card QA
- public delivery
- `auto_execute`
- individual persuasion scoring
- target user list
- real user / account matching
- psychological profiling
- personality diagnosis
- official verification claims
- causal proof claims
- prediction claims

If any stop condition appears, the correct decision is `needs_fix` or `privacy_issue_stop`, not implementation.

## M. Final Ready State Recommendation

Final recommendation:

```text
ready_for_8P_5_peoplecluster_transition_implementation_prompt
```

This means a later implementation prompt may add PeopleCluster-only local deterministic transition behavior, but it must keep 8P-1 validation first, preserve 8P-2 ContentAggregate behavior, preserve 8P-3 InfluenceCore behavior, preserve 8P-4 EchoBox behavior, keep all runtime side-effect flags false, defer `pull_ik`, defer `stance_effect_ik`, defer ResponseStrategy, avoid real-person claims, and avoid UI / API / runtime / storage changes.
