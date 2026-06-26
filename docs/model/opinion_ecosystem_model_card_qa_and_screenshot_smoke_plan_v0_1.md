# Opinion Ecosystem Model-card QA and Screenshot Smoke Plan v0.1

## A. Purpose

This plan defines the QA pass for the Opinion Ecosystem explanatory UI before any future API integration is considered.

The goal is to verify that the current static/local UI explains the deterministic model slices clearly, without implying production analysis, official verification, full-web coverage, causal proof, or automatic action.

This is a model-card QA and screenshot smoke plan only. It does not implement runtime behavior.

## B. Scope

In scope:

- static/local explanatory UI
- model-card copy
- visual screenshot smoke
- boundary wording
- C-end and B-end demo readability
- ResponseStrategy comparison wording

Out of scope:

- backend API integration
- production calculator route
- analysis_run creation
- Evidence Layer writes
- production report generation
- Sandbox/public event generation
- public publishing
- generated response text
- real LLM calls
- real platform APIs
- live collection
- calibration against reviewed historical outcomes

## C. Model-card Assertions by Module

| Module | What the UI may say | What the UI must not claim |
| --- | --- | --- |
| ContentAggregate | Groups local evidence signals into explanation-ready content aggregates | Not official verification, not truth_score, not full-web coverage |
| InfluenceCore | Shows content / narrative / official / media / meme cores that may shape discussion | Not a real person, not an account graph, not an official cause |
| EchoBox | Shows local amplification or resonance patterns inside the selected sample | Not full-platform spread, not final reach measurement |
| PeopleCluster | Shows anonymous group/cluster behavior in the demo model | Not real individual users, not targeting, not profiling |
| Camp Dynamics | Shows simplified stance movement in the local visualization | Not political/personality classification, not causal proof |
| DeconstructionCore | Shows how a narrative may be reframed or weakened in the local model | Not manipulation guidance, not a guaranteed mitigation |
| ResponseTempo | Shows how timing choices affect the demo state | Not prediction probability, not operational instruction |
| ResponseStrategyComparisonV01 | Compares transparent response candidates for human review | Not generated public copy, not auto_execute, not publish/send/post |
| ReputationMemory | Shows lingering memory in the sample visualization if visible | Not permanent reputation truth, not official record |

## D. Route Smoke Matrix

| Route | Expected sample | Explanation UI visible | Module cards visible | Boundary labels visible | ResponseStrategy human-review-only | T0-T6 visible | Console status | Forbidden UI absence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `/#/opinion-ecosystem` | Helldivers PSN sample or static fixture | Required | Required | Required | Required | Required when Helldivers mode is selected | No Sentigraph error/warn | Required |
| `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` | Dong Lu / Sun Jihai selected public sample; must not fall back to Helldivers | Required | Required | Required | Required | Historical timeline controls if present | No Sentigraph error/warn | Required |
| `/#/public-events/helldivers-psn` | Optional broader route coverage: Helldivers selected public sample | Required if model section is present | Required if model section is present | Required | Required | Required if timeline is shown | No Sentigraph error/warn | Required |
| `/#/public-events/donglu-sunjihai-youth-football` | Optional broader route coverage: Dong Lu / Sun Jihai selected public sample | Required if model section is present | Required if model section is present | Required | Required | Historical timeline controls if present | No Sentigraph error/warn | Required |
| `/#/reports/helldivers-psn-sample` | Optional broader route coverage: Helldivers B-end report sample | Required if model section is present | Required if model section is present | Required | Required | Not required unless report embeds timeline | No Sentigraph error/warn | Required |
| `/#/reports/donglu-sunjihai-youth-football-sample` | Optional broader route coverage: Dong Lu / Sun Jihai B-end report sample | Required if model section is present | Required if model section is present | Required | Required | Not required unless report embeds timeline | No Sentigraph error/warn | Required |
| B-end sample report page | Sample report fixture if route exists | Required if model section is present | Required if model section is present | Required | Required | Not required unless report embeds timeline | No Sentigraph error/warn | Required |

Forbidden UI absence means the route must not show:

- full-web coverage claim
- full-platform coverage claim
- official verification claim
- causal proof claim
- prediction guarantee
- truth_score claim
- target_user_list claim
- persuasion_score claim
- generated public response text
- auto_execute / publish / send / post action
- raw author identifiers

## E. Required Boundary Copy

Every route that shows the explanatory model should keep the boundary understandable:

- 当前为静态/本地解释界面
- 使用的是选定样本或本地 fixture
- 不代表全网覆盖
- 不代表全平台覆盖
- 不代表官方验证
- 不代表因果证明
- 不代表预测保证
- 不调用真实 API 或真实 LLM
- 不执行真实平台动作
- PeopleCluster 小球代表匿名人群簇，不代表真实个人
- InfluenceCore 节点代表内容、叙事、官方、媒体或 meme 核心，不是人物小球
- ResponseStrategy 仅用于人工复核候选比较，不生成可发布回应文案

## F. Screenshot Evidence Plan

Recommended screenshot set:

| Filename | Capture target | QA purpose |
| --- | --- | --- |
| `01_opinion_ecosystem_default_explanation_top.png` | Default Opinion Ecosystem route with explanation top section visible | Prove the default explanatory UI renders |
| `02_opinion_ecosystem_default_module_cards.png` | Default route module cards for ContentAggregate, InfluenceCore, EchoBox, and PeopleCluster | Prove module-level boundaries are visible |
| `03_opinion_ecosystem_default_response_strategy_boundary.png` | Default route ResponseStrategy comparison section | Prove no generated/public action wording |
| `04_dong_sun_query_explanation_top.png` | Dong/Sun query route top section | Prove the canonical query route loads Dong/Sun instead of falling back to Helldivers |
| `05_dong_sun_query_module_cards.png` | Dong/Sun query route module cards | Prove module-card boundaries work for the Chinese-event sample |
| `06_dong_sun_t0_t6_and_boundary_labels.png` | Dong/Sun query route T0-T6 controls and safety labels | Prove timeline and sample boundary labels are visible |
| `07_b_end_report_model_card_boundary.png` | Optional B-end report sample route if included in broader coverage | Prove report-facing wording remains non-operational |
| `08_console_clean_optional.png` | Browser console if capture is practical | Prove no visible runtime errors during smoke |

Screenshots should avoid browser tabs, secrets, profiles, local private paths, and raw author identifiers.

## G. Acceptance Criteria

The model-card QA passes only if:

- all expected routes render without visible error overlays
- no route shows `[object Object]`, `undefined`, or `NaN`
- module cards are readable at desktop demo size
- boundary copy is visible without searching source code
- PeopleCluster and InfluenceCore are not confused in labels
- ResponseStrategy comparison is visibly human-review-only
- no UI text implies full-web, full-platform, official verification, causal proof, prediction guarantee, targeting, or automatic execution
- no clickable control claims to publish, send, post, or execute a response
- no real API or real LLM behavior is implied

If any of these fail, the next task should be copy/UI polish, not API integration.

## H. Source Update Trigger

After model-card QA and screenshot smoke pass:

- update product/source context only after user approval
- Source 00 may need a small current-state note
- Source 08 / 09 / 10 may need demo and model-card notes if they track frontend demo state
- Source 11 should not be updated unless Analysis Request, Provider, or Import Governance behavior changes

No Project Source file should be changed as part of this plan.
