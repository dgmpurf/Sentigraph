# Opinion Ecosystem 8Q Frontend Explanatory UI Decision Checkpoint v0.1

Status: docs-only decision checkpoint / no frontend implementation / no backend implementation / no API exposure.

This checkpoint decides whether Sentigraph should start a future frontend explanatory UI slice for already implemented backend-only local calculator outputs. It does not authorize frontend code, API routes, production runtime, B-end report runtime integration, Sandbox runtime integration, public event generation, public posting, generated response text, or automatic strategy execution.

## A. Purpose

This is a docs-only decision checkpoint before any frontend explanatory UI implementation.

It decides whether Sentigraph should begin a future 8Q frontend explanatory UI slice for the already implemented local deterministic calculator outputs:

- `ContentAggregateWeightV01`
- `InfluenceCoreWeightV01`
- `EchoBoxWeightV01`
- `PeopleClusterStateV01`
- `ResponseStrategyComparisonV01`

This document does not authorize:

- frontend code
- backend code
- API routes
- production runtime
- B-end report runtime integration
- Sandbox runtime integration
- public event runtime generation
- generated public communication
- automatic strategy execution
- Evidence Layer writes
- production case or analysis run creation

## B. Current State

Current implemented calculator state:

- 8P-1 validator and run metadata skeleton exists.
- 8P-2 `ContentAggregateWeightV01` exists.
- 8P-3 `InfluenceCoreWeightV01` exists.
- 8P-4 `EchoBoxWeightV01` exists.
- 8P-5 `PeopleClusterStateV01` exists.
- 8P-6 `ResponseStrategyComparisonV01` exists.
- All 8P modules are backend-only, pure-local, deterministic, selected-sample, mock-default, and uncalibrated.
- 8P-1 forbidden-field, overclaim, `auto_execute`, and unknown/future platform guards remain present.
- Runtime side-effect flags remain false.
- No frontend explanatory UI has been implemented for these runtime outputs.
- No API route exposes the calculator.
- No C-end public page or B-end report sample uses backend calculator runtime scores yet.
- No Response Strategy Lab runtime exists.
- No generated response text exists.
- No public posting or execution exists.
- `pull_ik`, `stance_effect_ik`, `stance_effect_ik_adjusted`, effect objects, generated InfluenceCore candidates, and production simulation remain unimplemented.

The current frontend surfaces are still demo/sample-oriented. They can explain local samples, but they do not consume backend calculator runtime scores.

## C. Decision Question

Should Sentigraph begin a future 8Q frontend explanatory UI implementation?

Decision answer: yes, but only as a future frontend-only explanatory UI / model-card explanation slice that uses local static demo output fixtures or manually curated snapshots. It must not expose a calculator API route, execute the backend calculator from the UI, generate response text, publish anything, or imply production monitoring.

## D. Prerequisite Check

Prerequisite state:

- Backend calculator modules exist through 8P-6.
- Output contracts exist.
- Model card exists.
- Counterexample matrix exists.
- Integration boundary exists.
- Targeted tests exist for calculator behavior and safety boundaries.
- No API route exists for calculator exposure.
- No frontend runtime integration exists.
- No model-card QA or screenshot smoke has been run for a score UI yet.
- No historical replay calibration exists.
- No production Evidence to Opinion Ecosystem import exists.
- No B-end report runtime integration exists.
- No public event or Sandbox runtime generation exists.

This is adequate for a future explanation-only frontend slice because the main risk is interpretation and labeling, not formula availability.

## E. Option Comparison

### Option 1: Future Frontend-Only Explanatory UI First Slice

Proceed later with a frontend-only explanatory UI first slice using local/static explanatory fixtures or manually embedded mock calculator output snapshots.

Allowed:

- explanation panels
- model-status badges
- selected-sample / mock-default / uncalibrated labels
- score meaning cards
- warnings and blocker explanations
- human-review-only banner
- safe per-module summary cards
- links to model-card docs
- no API route
- no live backend calculator call
- no production runtime
- no response generation
- no `auto_execute`

Decision: selected as the future first implementation slice.

### Option 2: Expose Backend Calculator Through A New API Route First

Rejected for now.

Reason: the project has not created backend schema/API governance for calculator exposure. API exposure can make local mock scoring look production-ready, especially to users who do not distinguish local deterministic heuristics from production analysis.

### Option 3: Show All Raw Backend Calculator JSON In C-End Public Pages

Rejected for now.

Reason: raw outputs contain too much model detail and could be misread as official truth, prediction, full-platform measurement, or production monitoring.

### Option 4: Integrate Scores Into B-End Report Sample Pages As Live Runtime Metrics

Rejected for now.

Reason: current B-end pages are fixed frontend-only samples. Report runtime integration has separate governance and must not be implied by an explanatory UI slice.

### Option 5: Build Response Strategy Lab UI Now

Rejected for now.

Reason: `ResponseStrategyComparisonV01` is human-review-only comparison, not a strategy execution lab, not a response text generator, and not a production decision engine.

### Option 6: Defer UI And Do Model-Card QA / Screenshot Smoke First

Allowed fallback if explanatory UI proves too easy to misread.

This option remains available if first-slice copy or visual framing cannot clearly show selected-sample, mock-default, uncalibrated, and human-review-only boundaries.

## F. Recommended Decision

Recommended decision: proceed later with Option 1 as future 8Q-1.

Future 8Q-1 should be:

`frontend-only explanatory UI / model-card explanation slice`

Ready state recommendation:

`ready_for_8Q_frontend_explanatory_ui_first_slice_prompt`

## G. Why Frontend Explanatory UI Can Follow 8P-6

Frontend explanatory UI can follow 8P-6 because:

- backend now has ContentAggregate, InfluenceCore, EchoBox, PeopleCluster, and ResponseStrategyComparison outputs
- the main risk is user interpretation, not formula availability
- C-end and B-end users need clear labels before any score UI appears
- the first UI slice can be explanation-only and static/local
- screenshot smoke and boundary-wording checks can validate it before any API integration

The UI should explain score meaning and limitations. It should not turn scores into product claims.

## H. Why API Route / Production Integration Remain Deferred

API route and production integration remain deferred because:

- API exposure can imply production runtime readiness.
- Backend schema and governance have not been designed for calculator exposure.
- C-end and B-end pages currently remain frontend-only/local demo/sample pages.
- Production Evidence import and `analysis_run` integration remain absent.
- B-end report runtime remains absent.
- Sandbox/public event runtime generation remains absent.

The first explanatory UI should therefore avoid live backend calls and use local static snapshots or curated explanation fixtures.

## I. UI Audience Segmentation

### 1. C-End Public Event User

C-end users need simplified explanations, not raw model details.

They should see:

- selected sample only
- not full-web
- not full-platform
- not full-thread
- not prediction
- not official verification
- not causal proof
- no automatic action

### 2. B-End Reviewer / Professional User

B-end reviewers can see more detailed module-level components, warnings, blockers, and human-review status.

They must still see:

- uncalibrated
- mock-default
- model-card boundaries
- evidence is not truth
- rejected evidence excluded
- weak evidence warning-marked
- human review required

### 3. Internal QA / Model-Review User

Internal QA may inspect raw-ish module outputs and model-card warnings in controlled dev/demo context only.

This must not become a production analytics UI or public score feed.

## J. Score Exposure Tiers

### Tier A: Safe Summary Explanation

Can be shown broadly with strong labels:

- evidence confidence
- sample heat
- controversy
- discussion/review risk
- InfluenceCore credibility/resonance/exposure as content-core metrics
- EchoBox saturation/closure/bridge capacity as sample discussion-structure proxy
- PeopleCluster aggregate attention/fatigue/stance as anonymous aggregate proxy
- ResponseStrategy recommendation level as human-review-only candidate status

### Tier B: B-End / Reviewer-Only With Model-Card Warnings

Can be shown only with stronger caveats:

- `credibility_adjusted_influence_score`
- `transition_pressure`
- `state_delta`
- reactivation potential
- risk breakout
- `strategy_score`
- `benefit_score`
- `cost_score`
- privacy risk
- overclaim risk
- implementation risk

### Tier C: Not For First UI Slice

Do not show in the first explanatory UI slice:

- raw formulas
- all raw components
- raw JSON dumps
- developer-only warnings that may confuse users
- any field whose wording could imply prediction, persuasion, truth, full-web coverage, real identity tracking, or automatic strategy execution

### Tier D: Forbidden / Nonexistent Outputs

Must never appear as UI features or claims:

- `pull_ik`
- `stance_effect_ik`
- `ResponseToPeopleClusterEffectV01`
- `ResponseToEchoBoxEffectV01`
- `GeneratedInfluenceCoreCandidateV01`
- `response_text`
- `generated_public_message`
- `auto_execute`
- `publish_now`
- `execute_now`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `guaranteed_success`
- real community map
- full graph
- psychological profile
- personality diagnosis

## K. Module-Specific Explanation Rules

### ContentAggregate

Explain as evidence-level / aggregate-level heat and risk proxy.

It is not full-web heat and not official truth. Duplicate evidence is folded. Rejected evidence is excluded. Evidence confidence affects score interpretation.

### InfluenceCore

Explain as content/narrative/source core scoring.

InfluenceCore is not PeopleCluster and not a real person. `factual_credibility` is not `truth_score`. Credibility-adjusted influence is not persuasion probability. No `pull_ik` or stance effect is exposed.

### EchoBox

Explain as sample-scoped discussion container proxy.

EchoBox is not a real community map and not a full social graph. Bridge and breakout are potential structure indicators, not causal propagation proof.

### PeopleCluster

Explain as anonymous aggregate behavioral proxy.

PeopleCluster is not a real person, not account identity, and not a psychological profile. `transition_pressure` and `state_delta` are aggregate proxies, not prediction of real people's belief change.

### ResponseStrategyComparison

Explain as transparent response candidate comparison for human review.

It is not response text generation, not Strategy Lab runtime, not public posting, and not `auto_execute`. The highest level is `strong_candidate_for_human_review`. High score cannot override blockers.

## L. Required UI Boundary Copy

Short copy snippets for future UI:

- "Selected sample only. This is not full-web, full-platform, or full-thread coverage."
- "Mock-default coefficients. The model is uncalibrated and not empirically validated."
- "Evidence is not truth. Scores summarize available evidence, not official verification."
- "Not causal proof and not prediction. The UI explains sample structure only."
- "No automatic action. Human review is required before any interpretation or response."
- "PeopleCluster means anonymous aggregate proxy, not real individual users."
- "InfluenceCore means content / narrative / official / media / meme core, not a person ball."
- "EchoBox means sample discussion container proxy, not a real community map."
- "ResponseStrategy is a human-review-only comparison. It does not generate response text."

Chinese short copy for future C-end UI:

- "仅代表已选样本，不代表全网、全平台或完整讨论串。"
- "模型系数为 mock-default，当前未校准。"
- "证据不是事实本身，分数不是官方验证。"
- "这不是因果证明，也不是预测。"
- "不执行自动动作，所有解释都需要人工复核。"
- "PeopleCluster 是匿名人群簇代理，不是真实个人。"
- "InfluenceCore 是内容、叙事、官方、媒体或梗化核心，不是人群小球。"
- "EchoBox 是样本讨论容器代理，不是真实社群地图。"
- "ResponseStrategy 只比较供人工复核的回应候选，不生成公开回应文本。"

## M. Future First UI Slice Proposal

Future 8Q-1:

`frontend-only explanatory score cards / model-card drawer using local static demo output fixtures`

Likely future changed files if approved later:

- `frontend/src/components/opinion/OpinionEcosystemModelExplanation.jsx`
- `frontend/src/data/opinionEcosystemCalculatorOutputFixture.js`
- `frontend/src/pages/OpinionEcosystemSandbox.jsx`
- `frontend/src/styles/global.css`
- optional `docs/model/opinion_ecosystem_frontend_explanatory_ui_model_card_v0_1.md`

Do not implement those files in this checkpoint.

## N. Future Route / Page Scope

Future first UI slice should be limited to one or two demo surfaces:

- Opinion Ecosystem Sandbox explanatory panel
- optional B-end report sample "model explanation / planned runtime boundary" panel

Do not expose as:

- production dashboard
- public ranking
- Strategy Lab runtime
- API-driven live metrics
- report export output
- public event score feed

## O. Future Validation Expectations

Future 8Q-1 should validate:

- frontend build passes
- route smoke for `/#/opinion-ecosystem`
- route smoke for `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- optional report sample smoke
- no console errors
- no `[object Object]`
- no `undefined` / `NaN`
- no visible 500
- boundary copy visible
- labels show selected-sample / mock-default / uncalibrated
- ResponseStrategy card says human-review-only
- no `response_text`
- no `auto_execute`
- no `publish_now` / `execute_now`
- no `target_user_list`
- no `truth_score` / `official_verified`
- no `prediction_probability` / `persuasion_score`
- no real community map or full graph claim
- no raw author identifiers
- no API call added
- no backend route added
- no collector touched
- no `evidence_items` parsed

## P. Stop Conditions

Stop future implementation if it attempts:

- API route for calculator
- production runtime integration
- B-end report runtime integration
- Sandbox/public event runtime generation
- generated response text
- Strategy Lab runtime
- `auto_execute`
- public posting
- target user list
- individual persuasion score
- real identity matching
- psychological profiling
- official verification claims
- prediction or guarantee claims
- full-web/full-platform claims
- real API / LLM
- collector access
- `evidence_items` parsing
- Evidence Layer write
- production case / `analysis_run`

## Q. Final Ready State

Decision: ready.

Recommended next ready state:

`ready_for_8Q_frontend_explanatory_ui_first_slice_prompt`

This means a later implementation prompt may add a frontend-only explanatory UI / model-card explanation slice using static/local fixtures, while keeping API exposure, production runtime, Strategy Lab runtime, B-end report runtime integration, Sandbox/public event runtime generation, generated response text, and any public action deferred.
