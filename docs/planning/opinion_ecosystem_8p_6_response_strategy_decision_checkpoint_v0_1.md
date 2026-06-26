# Opinion Ecosystem 8P-6 ResponseStrategy Decision Checkpoint v0.1

Status: docs-only / planning checkpoint / no runtime implementation.

This checkpoint decides whether Sentigraph should start a future Phase 8P-6 ResponseStrategy comparison implementation after the Phase 8P-1 fixture validator, Phase 8P-2 ContentAggregate calculator, Phase 8P-3 InfluenceCore calculator, Phase 8P-4 EchoBox calculator, and Phase 8P-5 PeopleCluster transition calculator.

It is not a runtime artifact, not an analysis result, not a response generator, not an execution system, not official verification, not causal proof, and not prediction.

## A. Purpose

This document is a docs-only decision checkpoint before any ResponseStrategy implementation.

It decides whether the deterministic local mock calculator should add a first ResponseStrategy comparison slice.

It does not authorize:

- scoring implementation in this task
- frontend Strategy Lab
- public message generation
- public posting
- production runtime
- automatic action
- API routes
- runtime persistence
- report integration

ResponseStrategy means deterministic, sample-scoped comparison of transparent communication options for human review. It does not mean automated public-opinion control, public posting, generated public response text, or platform account operation.

## B. Current State

Current completed context:

- 8N-g model docs exist.
- 8O calculator design exists.
- 8P deterministic local calculator decision checkpoint exists.
- 8P-1 validator / run metadata skeleton exists.
- 8P-2 `ContentAggregateWeightV01` exists.
- 8P-3 `InfluenceCoreWeightV01` exists.
- 8P-4 `EchoBoxWeightV01` exists.
- 8P-5 `PeopleClusterStateV01` exists.
- All four upstream modules are backend-only, pure-local, deterministic, selected-sample, and uncalibrated.
- 8P-1 forbidden-field, overclaim, `auto_execute`, and future-platform guards remain present.
- Runtime side-effect flags remain false.
- No ResponseStrategy scoring exists.
- No `ResponseStrategyComparisonV01` exists.
- No frontend Strategy Lab runtime exists.
- No generated response text exists.
- No posting or execution exists.
- `pull_ik`, `stance_effect_ik`, `stance_effect_ik_adjusted`, and `InfluenceCoreToClusterEffectV01` remain unimplemented.

The current calculator chain is therefore:

```text
8P-1 fixture validation
-> 8P-2 ContentAggregateWeightV01
-> 8P-3 InfluenceCoreWeightV01
-> 8P-4 EchoBoxWeightV01
-> 8P-5 PeopleClusterStateV01
-> ResponseStrategy not calculated
```

## C. Decision Question

Should Sentigraph begin a future 8P-6 ResponseStrategy implementation?

Decision answer: yes, but only as a future `ResponseStrategyComparisonV01`-only deterministic local comparison calculator for explicit safe strategy candidates.

## D. Prerequisite Check

Prerequisites now available:

- Response strategy formula spec exists: `docs/model/response_strategy_comparison_model_v0_1.md`.
- Fixture contract exists.
- Output contract exists.
- Counterexample matrix exists.
- Validation plan exists.
- Integration boundary exists.
- ContentAggregate output exists.
- InfluenceCore output exists.
- EchoBox output exists.
- PeopleCluster output exists.
- 8P-1 blocker behavior exists.
- Upstream targeted tests exist.
- No ResponseStrategy implementation has started.
- No UI, API, persistence, or product runtime integration exists.
- No real API, real LLM, or collector dependency is required.

The prerequisite state is adequate for a future ResponseStrategy comparison-only implementation slice if it stays local, deterministic, selected-sample, uncalibrated, non-causal, non-predictive, non-executable, and human-review-only.

## E. Option Comparison

### Option 1: Future ResponseStrategyComparisonV01-Only Implementation

Allowed scope:

- compare explicit safe response strategy candidates
- `evidence_fit`
- `timing_fit`
- `clarity_gain`
- `confusion_reduction`
- `emotion_deescalation`
- `bridge_opening`
- `trust_repair_potential`
- `fatigue_relief`
- `reactivation_risk_reduction`
- `amplification_risk`
- `backlash_risk`
- `privacy_risk`
- `overclaim_risk`
- `implementation_risk`
- `benefit_score`
- `cost_score`
- `strategy_score`
- `recommendation_level`
- blockers
- warnings
- human-review candidate output only

Not allowed:

- response text generation
- publication
- execution
- `ResponseToPeopleClusterEffectV01`
- `ResponseToEchoBoxEffectV01`
- `GeneratedInfluenceCoreCandidateV01`
- causal outcome prediction
- guaranteed effect

Decision: selected as the future first implementation slice.

### Option 2: ResponseStrategyComparisonV01 Plus ResponseToPeopleClusterEffectV01

Rejected for the first slice because:

- it can be misread as persuasion or causal stance change
- it can reintroduce `stance_effect` semantics
- it requires stricter model-card review
- PeopleCluster must remain anonymous aggregate, not a target segment

### Option 3: ResponseStrategyComparisonV01 Plus ResponseToEchoBoxEffectV01

Rejected for the first slice because:

- it can be misread as guaranteed breakout, closure reduction, or community control
- EchoBox is only a sample-scoped discussion-structure proxy
- causal effect estimation is not calibrated

### Option 4: ResponseStrategyComparisonV01 Plus GeneratedInfluenceCoreCandidateV01 Or Generated Public-Response Text

Rejected for the first slice because:

- it changes comparison into content generation
- it risks automatic publication or synthetic influence creation
- it needs separate content, legal, privacy, review, disclosure, and publication gates

### Option 5: Add Frontend Response Strategy Lab First

Rejected because:

- the UI could appear production-ready
- users could mistake comparison scores for proven outcomes
- backend/model-card QA must happen first
- the current report page marks Response Strategy Lab as planned-only

### Option 6: Implement Full Strategy Runtime, API Route, Persistence, Report Integration, And Public Action Flow Together

Rejected because:

- scope is too broad
- it weakens auditability
- it increases the risk of accidental auto-execution or overclaim
- it violates the staged implementation plan

### Option 7: Defer ResponseStrategy And Keep The Calculator At 8P-5

Allowed as fallback if the safety boundary cannot be made sufficiently explicit.

Decision: not selected because Option 1 can be separated from effect objects, response generation, UI, and execution.

## F. Recommended Decision

Recommended decision: proceed later with Option 1 only.

Selected future implementation slice:

```text
ResponseStrategyComparisonV01-only deterministic local comparison calculator
```

Decision state:

```text
ready_for_8P_6_responsestrategy_comparison_implementation_prompt
```

This does not implement anything in this docs-only task. It only prepares the next implementation prompt boundary.

## G. Why ResponseStrategy Can Follow PeopleCluster

ResponseStrategy can follow PeopleCluster because the previous slices provide safe aggregate context:

- ContentAggregate provides evidence confidence, heat, controversy, and risk context.
- InfluenceCore provides credibility, exposure, amplification, bridge, backlash, and de-escalation context.
- EchoBox provides saturation, closure, bridge capacity, breakout, and echo-risk context.
- PeopleCluster provides anonymous aggregate stance, confidence, attention, fatigue, expression, exit, reactivation, and openness proxies.

These upstream outputs are enough to compare transparent communication candidates without calculating individual targeting or guaranteed effects.

The first slice can remain deterministic, synthetic-fixture-only, local, uncalibrated, and human-review-only.

## H. Why Effect Objects Remain Deferred

The following remain deferred:

- `ResponseToPeopleClusterEffectV01`
- `ResponseToEchoBoxEffectV01`
- `GeneratedInfluenceCoreCandidateV01`
- `pull_ik`
- `stance_effect_ik`
- `stance_effect_ik_adjusted`
- `InfluenceCoreToClusterEffectV01`

Effect objects could be interpreted as:

- causal claims
- persuasion estimates
- community control
- guaranteed strategy outcomes
- synthetic narrative generation

Future consideration would require a separate checkpoint and stronger model-card QA.

## I. Human-Review-Only Rule

Every strategy output requires human review.

Highest allowed recommendation level:

```text
strong_candidate_for_human_review
```

Never output:

```text
auto_execute
```

Rules:

- Strategy score cannot authorize execution.
- A high strategy score cannot override a privacy blocker.
- A high strategy score cannot override missing evidence.
- A high strategy score cannot override forbidden behavior.
- No output may claim a strategy will cause a specific public reaction.
- No output may claim guaranteed calming, support growth, opposition decline, or reputation repair.

## J. Allowed Strategy IDs

The allowed IDs from the source model are exactly:

- `S0 no_response_baseline`
- `S1 observe_and_prepare`
- `S2 low_amplification_hold`
- `S3 factual_clarification`
- `S4 FAQ_or_longform_explanation`
- `S5 evidence_supported_context`
- `S6 third_party_explanation`
- `S7 correction_or_apology_if_applicable`
- `S8 progress_update`
- `S9 community_deconstruction_support`
- `S10 fatigue_period_reputation_repair`
- `S11 private_review_before_public_response`

Interpretation safeguards:

- `S0` is a comparison baseline, not an instruction to ignore an issue.
- `S6` requires disclosed, non-fabricated, independently reviewable third-party participation.
- `S7` applies only when evidence supports correction or accountability.
- `S9` means transparent support for existing community clarification or de-escalation. It must not mean covert seeding, fake grassroots behavior, bots, sockpuppets, water-army behavior, or coordinated influence.
- `S11` means no public action until private human review completes.

Unknown strategy IDs must be blocked or routed to manual review.

## K. Recommendation Levels

The exact existing levels are:

- `forbidden`
- `blocked_pending_review`
- `private_review_only`
- `strong_candidate_for_human_review`
- `candidate_for_human_review`
- `prepare_materials_first`
- `not_recommended_now`
- `monitor_only`

Do not invent:

- `approved_for_execution`
- `auto_execute`
- `guaranteed_success`
- `publish_now`
- `deploy`
- `send`
- `post`
- `target_now`

## L. Blocker Precedence

Future 8P-6 should use this precedence:

1. Forbidden-behavior blocker
2. Privacy / consent / minor-safety blocker
3. Evidence insufficiency / trust blocker
4. Legal or sensitive-material review blocker
5. Overclaim blocker
6. Implementation-risk blocker
7. Score-based recommendation level

A score must never override a higher-priority blocker.

## M. Third-Party / Beneficiary / Parent / Adult-Student Material

All of these must be true:

- `voluntary = true`
- `informed_consent = true`
- `redacted = true`
- `minor_protected = true`
- `context_verifiable = true`
- `no_private_detail_exposure = true`
- `human_review_approved = true`

If any condition is missing, the output must be:

- `blocked_pending_review`
- or `private_review_only`

No public-use candidate may be produced.

Additional rules:

- no minor should be placed at the center of controversy
- no family or beneficiary material may be used as emotional leverage
- no fabricated testimony
- no undisclosed sponsorship
- no raw identity exposure

## N. Explicitly Not Included In 8P-6 First Implementation Slice

The first 8P-6 slice must not include:

- public response text generation
- response drafting
- automatic posting
- account operation
- moderation action
- report runtime integration
- Sandbox runtime integration
- C-end public event integration
- frontend UI
- API route
- runtime persistence
- `ResponseToPeopleClusterEffectV01`
- `ResponseToEchoBoxEffectV01`
- `GeneratedInfluenceCoreCandidateV01`
- `pull_ik`
- `stance_effect_ik`
- `InfluenceCoreToClusterEffectV01`
- real API / LLM
- collector
- `evidence_items` parsing
- Evidence Layer write
- production case
- `analysis_run`
- B-end report runtime
- public delivery
- `target_user_list`
- individual persuasion score
- real identity matching
- psychological profiling
- personality diagnosis
- guaranteed outcome
- `auto_execute`

## O. Future Validation Expectations

Future tests should cover:

- minimal safe strategy candidate produces `ResponseStrategyComparisonV01`
- multiple candidates can be compared deterministically
- 8P-1 blockers remain present
- ContentAggregate output remains present
- InfluenceCore output remains present
- EchoBox output remains present
- PeopleCluster output remains present
- runtime side-effect flags remain false
- `human_review_required` remains true
- highest recommendation is `strong_candidate_for_human_review`
- `auto_execute` input is blocked
- forbidden behavior is blocked
- unknown strategy ID is blocked or manual review
- insufficient evidence yields `prepare_materials_first` or `private_review_only`
- T4 FAQ can show clarity benefit and high backlash / amplification risk simultaneously
- no guaranteed calming claim
- low-credibility viral claim is not treated as fact
- no-response is treated as baseline, not automatic recommendation
- high benefit cannot override privacy risk
- minors / family material without consent is blocked
- disclosed third-party explanation differs from fabricated endorsement
- community deconstruction support cannot become covert seeding
- same fixture gives exactly the same output
- no effect-object outputs
- no generated response text
- no real IO / network / runtime side effects

## P. Stop Conditions

Stop any future implementation attempt if it introduces:

- `auto_execute`
- public posting
- generated public response text
- account control
- hidden promotion
- fake consensus
- astroturfing
- bots or sockpuppets
- water-army behavior
- individual targeting
- target user list
- persuasion scoring
- real-person profiling
- psychological profiling
- harassment
- brigading
- coordinated reporting
- suppression of criticism
- fabricated endorsement
- raw identity exposure
- minors / family material without required consent and protection
- causal outcome claims
- guaranteed effect claims
- real API / LLM
- collector access
- `evidence_items` parsing
- Evidence Layer write
- production case
- `analysis_run`
- B-end report runtime
- Sandbox / public event runtime
- frontend Strategy Lab before model-card QA

If any stop condition appears, the correct decision is `needs_fix` or `privacy_issue_stop`, not implementation.

## Q. Final Ready State Recommendation

Final recommendation:

```text
ready_for_8P_6_responsestrategy_comparison_implementation_prompt
```

This means a later implementation prompt may add ResponseStrategyComparisonV01-only local deterministic comparison behavior, but it must keep 8P-1 validation first, preserve 8P-2 ContentAggregate behavior, preserve 8P-3 InfluenceCore behavior, preserve 8P-4 EchoBox behavior, preserve 8P-5 PeopleCluster behavior, keep all runtime side-effect flags false, defer effect objects, defer generated response text, defer frontend Strategy Lab, and avoid UI / API / runtime / storage changes.
