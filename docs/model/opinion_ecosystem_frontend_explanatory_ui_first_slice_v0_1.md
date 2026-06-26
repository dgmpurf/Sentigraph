# Opinion Ecosystem Frontend Explanatory UI First Slice v0.1

Status: docs-only design / no frontend implementation / no backend implementation / no API route.

## A. Slice Name

Phase 8Q-1 Frontend Explanatory UI First Slice.

## B. Purpose

Future implementation may add explanation-only UI for already implemented backend-only local calculator outputs.

The future UI should not calculate scores in frontend. It should not call a backend calculator API. It should not expose production runtime. It should use static/local demo output snapshots or safe manually curated explanation fixtures for UI explanation only.

The first slice exists to reduce user misunderstanding before any broader score display, API route, report integration, or public event integration is considered.

## C. Future First-Slice UI Components

Design-only component candidates:

- `ModelStatusBadge`: shows `mock_default`, `uncalibrated`, `not_started`, and selected-sample state.
- `SampleScopeNotice`: explains selected sample, not full-web, not full-platform, not full-thread.
- `CalculatorModuleSummaryCard`: one safe card per module.
- `ScoreMeaningTooltip`: short explanation of what a score means and does not mean.
- `WarningAndBlockerPanel`: makes warnings and blockers visible before score interpretation.
- `BoundaryFlagList`: compact list of no-overclaim flags.
- `ModelCardDrawer`: links copy and detail back to the model card.
- `HumanReviewOnlyBanner`: shown when ResponseStrategyComparison is visible.
- `ResponseStrategyComparisonExplanationCard`: compares candidate status without response text or execution CTA.
- `NotCalculatedOrDeferredModuleNotice`: marks deferred modules and nonexistent outputs clearly.

## D. Future First-Slice Data Contract

Safe local UI fixture shape:

```json
{
  "module_name": "ContentAggregate",
  "schema": "sentigraph_content_aggregate_weight_v0_1",
  "model_status": "8P_2_content_aggregate_formula",
  "coefficient_source": "mock_default",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "sample_scope": "selected_sample_or_local_fixture_only",
  "scores_summary": [],
  "warnings_summary": [],
  "blockers_summary": [],
  "boundary_flags": {},
  "human_review_required": true,
  "explanation_copy": [],
  "do_not_claim_copy": []
}
```

Do not include:

- raw author fields
- evidence item content
- full raw JSON dumps
- generated response text
- target user lists
- `auto_execute` or executable commands
- hidden/system/internal warnings that can confuse public demo users

## E. Module Card Requirements

### ContentAggregate

Card title: ContentAggregate / Evidence Heat And Risk Proxy.

Safe summary: sample evidence heat, controversy, evidence confidence, discussion risk, and review risk.

What it means: a bounded local summary of imported or selected evidence.

What it does not mean: real hotlist, official truth, full-web heat, full-platform coverage, or prediction.

Recommended audience: C-end summary, B-end detail, internal QA.

### InfluenceCore

Card title: InfluenceCore / Content And Narrative Core.

Safe summary: content / narrative / official / media / KOL / meme core scoring.

What it means: a selected-sample core-level proxy for credibility, exposure, resonance, bridge potential, amplification, and risk.

What it does not mean: real person, PeopleCluster, fact verifier, causal root proof, or persuasion probability.

Recommended audience: C-end simplified summary, B-end detail, internal QA.

### EchoBox

Card title: EchoBox / Sample Discussion Container.

Safe summary: saturation, closure, bridge capacity, constructive breakout, risk breakout, and echo risk.

What it means: a local sample discussion-structure proxy.

What it does not mean: real community map, full social graph, causal propagation chain, or target pool.

Recommended audience: C-end visual explanation, B-end detail, internal QA.

### PeopleCluster

Card title: PeopleCluster / Anonymous Aggregate Proxy.

Safe summary: aggregate stance, attention, fatigue, expression intensity, exit risk, reactivation proxy, and openness.

What it means: an anonymous group-level behavioral proxy inside the selected sample.

What it does not mean: real person, account identity, psychological profile, personality diagnosis, individual tracking, or belief-change prediction.

Recommended audience: C-end visual explanation with strong labels, B-end detail, internal QA.

### ResponseStrategyComparison

Card title: Response Strategy Comparison / Human-Review Option Comparison.

Safe summary: transparent response candidate comparison with benefits, costs, blockers, warnings, and human-review-only recommendation level.

What it means: a local deterministic comparison of explicitly provided safe response candidates.

What it does not mean: generated response text, Strategy Lab runtime, public posting, automatic PR decision, account operation, public-opinion control, or guaranteed outcome.

Recommended audience: B-end reviewer and internal QA first; C-end only if heavily simplified.

## F. ResponseStrategy UI Requirements

The title should avoid "自动策略". Use:

- "透明回应候选比较"
- "Human-review response option comparison"

The UI must:

- display highest possible level as `strong_candidate_for_human_review`
- show `execution_authorized = false`
- show `public_response_generated = false`
- show `not_auto_executed = true`
- show blockers before score
- never display "best strategy" without a human-review caveat
- never show public response text
- never show publish / send / post / execute CTA

## G. C-End Copy Rules

Use simple language:

- "本地样本"
- "不是全网"
- "不是预测"
- "不是官方验证"
- "小球是匿名人群簇"
- "这些分数用于理解样本结构"

Avoid:

- "实时全网"
- "真实热榜"
- "未来会发生"
- "最优策略"
- "自动建议"
- "说服人群"
- "精准影响"

## H. B-End Copy Rules

B-end copy may include more detail:

- evidence confidence
- review needed
- weak evidence
- rejected excluded
- model-card warnings
- strategy blockers
- human review gate

But still avoid:

- guaranteed outcome
- causal proof
- production report claim
- legal or PR guarantee
- official verification
- automatic action

## I. Design Of Not Calculated / Deferred Notices

Future UI must clearly mark:

- `pull_ik` not implemented
- `stance_effect_ik` not implemented
- effect objects not implemented
- generated response text not implemented
- production calibration not started
- frontend/UI integration is explanatory only
- API route not implemented

Suggested notice:

"This module is deferred. It is not calculated, not exposed in UI, and must not be inferred from current scores."

## J. Accessibility / Readability Expectations

Future UI should follow these readability rules:

- short labels
- no dense formula walls for C-end
- expandable detail for B-end/internal QA
- color should not be the sole indicator
- warning labels should be text-visible
- avoid anxiety-inducing red-only presentation
- use neutral wording for risk
- avoid terms that imply manipulation, control, certainty, or official verification

## K. Future Tests / Smoke List

Future 8Q-1 should plan these checks, but this document does not implement them:

- `test_frontend_build_passes`
- `test_opinion_ecosystem_explanatory_panel_visible`
- `test_dong_sun_sample_shows_explanatory_boundaries`
- `test_response_strategy_card_human_review_only`
- `test_no_generated_response_text_in_ui`
- `test_no_auto_execute_or_publish_cta`
- `test_no_target_user_list_or_persuasion_score_in_ui`
- `test_no_truth_score_or_official_verified_in_ui`
- `test_no_real_community_map_or_full_graph_claim`
- `test_no_raw_author_identifiers`
- `test_no_backend_api_route_added`
- `test_no_collector_or_evidence_items_access`
- browser smoke for `/#/opinion-ecosystem`
- browser smoke for `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- optional browser smoke for `/#/reports/donglu-sunjihai-youth-football-sample`

## L. Not Allowed In Future First UI Implementation

The first frontend explanatory UI slice must not include:

- API route
- backend code
- runtime persistence
- calculator execution from UI
- generated response text
- public posting or action CTA
- Strategy Lab runtime
- B-end report runtime
- public event runtime
- real API / LLM
- collector
- `evidence_items` parsing
- Evidence Layer write
- production case / `analysis_run`
- target user list
- persuasion score
- truth score / official verification / prediction probability
- full-web/full-platform claim
- real identity / psychological profile

## M. Later Slices Only After 8Q-1 Passes

Only after the first explanatory UI and screenshot/model-card QA may future checkpoints consider:

- limited B-end report sample explanation integration
- backend API design for local calculator if still needed
- model-card QA / screenshot smoke
- historical replay comparison
- calibration docs
- production integration design

This document does not pre-authorize those later slices.
