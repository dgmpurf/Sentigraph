# Opinion Ecosystem 8R Model-card QA / Static-vs-API Decision Checkpoint v0.1

## A. Purpose

This checkpoint decides whether Sentigraph should keep the current Opinion Ecosystem explanatory UI as a static/local demo surface, or proceed toward frontend API integration for the deterministic calculator outputs.

Decision scope:

- evaluate the current Phase 8P / 8Q state
- identify model-card QA work needed before any API integration
- keep product claims conservative for C-end and B-end demos
- prevent a premature move from explanation-only UI into runtime analysis, generated response, or public action features

This document is planning-only. It does not authorize implementation.

## B. Current State

Current implemented state, based on the Phase 8P and 8Q sequence:

- Phase 8P calculator work introduced deterministic, local formula slices for ContentAggregate, InfluenceCore, EchoBox, PeopleCluster transitions, and ResponseStrategy comparison.
- Phase 8Q added a frontend explanatory UI slice that reads local/static fixture data and presents model-card style explanations.
- The current UI is explanation-only and demo-oriented.
- There is no production calculator API route.
- There is no production analysis runtime connected to these model-card explanations.
- There is no report runtime connected to these model-card explanations.
- There is no Sandbox/public event generation runtime created by these model-card explanations.
- There is no generated response text.
- There is no auto_execute, publish, send, post, or platform action.
- There is no calibration claim against reviewed historical outcomes.

The current safe default is: static/local explanation UI.

## C. Decision Question

Should Sentigraph proceed directly from the Phase 8Q explanatory UI to frontend API integration?

Answer: no.

The next step should be model-card QA, screenshot smoke, and boundary-copy review. API integration should remain a separate future gated design checkpoint.

## D. Recommended Decision

Recommended state:

- Keep the static/local explanatory UI as the demo default.
- Do not proceed directly to frontend API integration.
- Do a model-card QA and screenshot smoke pass first.
- Keep calculator outputs framed as deterministic demo/model-card explanations, not production truth, not prediction, and not official verification.
- Defer Strategy Lab, B-end report runtime integration, and calibration until their own gates exist.

Decision label:

`static_ui_remains_demo_default_api_integration_not_approved_now`

## E. Option Comparison

| Option | What it means | Benefit | Risk | Decision |
| --- | --- | --- | --- | --- |
| Keep static/local UI | Continue showing explanation cards from local fixture data | Safe for demo, easy to QA, no runtime overclaim | Less dynamic than a full runtime | Approved for now |
| Add frontend API integration now | Connect UI to backend calculator-style route | More realistic architecture | Premature capability signal, larger QA surface, higher risk of overclaim | Not approved now |
| Add Strategy Lab now | Let users compare response plans in a more productized flow | Strong demo value | Could be misunderstood as generated response or action recommendation | Deferred |
| Add B-end report runtime now | Push model-card outputs into report generation | Useful later | Report gates and legal language must stay separate | Deferred |
| Add calibration now | Compare model outputs to historical reviewed results | Improves credibility | Requires reviewed replay dataset and acceptance criteria | Deferred |

## F. Required Model-card QA Before API

Before any API integration, the static UI needs a model-card QA pass:

- verify every module card has a plain-language purpose
- verify every module card identifies its input scope
- verify every module card states what it does not claim
- verify visual labels do not imply truth_score, official verification, or prediction probability
- verify ResponseStrategy comparison remains human-review-only
- verify Strategy wording uses transparent communication terms, not manipulation wording
- verify PeopleCluster wording says anonymous groups/clusters, not real individuals
- verify InfluenceCore wording says content / narrative / official / media / meme cores, not people balls
- verify model-card copy says the output is local/static explanation, not production analysis
- verify selected sample limitations are visible when sample data is shown

## G. Future API Integration Prerequisites

API integration can be reconsidered only after a separate docs-only checkpoint defines:

- exact route contract
- schema versioning
- fixture parity tests
- no network and no real LLM boundary
- no production Evidence Layer write
- no analysis_run creation
- no report generation side effect
- no Sandbox/public event generation side effect
- no generated response text
- no auto_execute / publish / send / post action
- no exposure of raw author identifiers
- no public/signed URL behavior
- no calibration claim unless a reviewed historical replay dataset exists

The future route, if approved, must return explanation-ready deterministic objects only. It must not produce executable strategy text or platform actions.

## H. Stop Conditions

Stop before API integration if any of these are true:

- UI copy implies full-web coverage
- UI copy implies full-platform coverage
- UI copy implies causal proof
- UI copy implies official verification
- UI copy implies prediction probability
- UI copy implies truth_score or authoritative correctness
- UI copy implies generated response text is ready to publish
- UI copy implies automatic targeting, persuasion, sending, posting, or execution
- module cards are unclear to a non-technical user
- Strategy comparison appears to recommend manipulating users
- PeopleCluster can be mistaken for real individual users
- InfluenceCore can be mistaken for a person node
- boundary copy is missing from C-end or B-end demo routes

## I. Screenshot / Browser Smoke Requirement

The immediate next task should be visual/browser QA, not API work.

Minimum smoke coverage:

- `/#/opinion-ecosystem`
- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`

Optional broader route coverage may include:

- `/#/public-events/helldivers-psn`
- `/#/public-events/donglu-sunjihai-youth-football`
- `/#/reports/helldivers-psn-sample`
- `/#/reports/donglu-sunjihai-youth-football-sample`

For each route, verify:

- model-card section renders
- module cards are visible
- selected sample boundary is visible where sample data appears
- ResponseStrategy comparison is clearly human-review-only
- no `undefined`
- no `NaN`
- no `[object Object]`
- no visible 500 prompt
- no copy saying full-web, full-platform, official verified, causal proof, or prediction guarantee

## J. Boundary Copy Checklist

The UI should keep these ideas visible in short, human-readable form:

- 本地解释快照
- 不是生产分数
- 不是全网
- 不是全平台
- 不是预测
- 不是官方验证
- 不代表因果证明
- 不自动执行
- 需要人工复核
- 小球是匿名人群簇
- InfluenceCore 是内容、叙事、官方、媒体或 meme 核心，不是人物小球
- 透明回应候选比较
- 不生成公开回应文案
- 不发布、不发送、不自动执行任何平台动作

## K. Final Decision State

Decision:

`static_ui_remains_demo_default_api_integration_not_approved_now`

Ready state after this checkpoint:

`ready_for_phase_8r_model_card_qa_and_screenshot_smoke`

Recommended next task:

Run model-card QA and screenshot smoke for the static/local explanatory UI. Do not start API integration until a later docs-only API contract checkpoint is approved.
