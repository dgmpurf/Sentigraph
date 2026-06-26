# Phase 8R Model-card QA / Screenshot Smoke Report

## Decision

Decision: ready.

Privacy issue stop: no.

Code changed: no.

Docs or assets changed: yes.

Implementation slice: 8R model-card QA / screenshot smoke.

## Environment

- Frontend URL: `http://127.0.0.1:5173`
- Browser path: in-app browser automation
- Dev server: local Vite dev server
- Build command: `npm.cmd --prefix frontend run build`
- Screenshot folder: `docs/demo/assets/opinion_ecosystem_8r_model_card_qa/`

## Screenshot Results

| File | What it proves |
| --- | --- |
| `01_opinion_ecosystem_default_explanation_top.png` | Default Opinion Ecosystem route loads with visible safety boundary and local/static demo framing. |
| `02_opinion_ecosystem_default_module_cards.png` | Default route model explanation section and module-card boundaries are visible. |
| `03_opinion_ecosystem_default_response_strategy_boundary.png` | ResponseStrategyComparisonV01 is human-review-only, not response text generation or execution. |
| `04_dong_sun_query_explanation_top.png` | Canonical Dong/Sun query route loads and selects the Dong/Sun sample instead of falling back to Helldivers. |
| `05_dong_sun_query_module_cards.png` | Dong/Sun query route shows the same model-card explanation and module-card boundaries. |
| `06_dong_sun_t0_t6_and_boundary_labels.png` | Dong/Sun T0-T6 controls and sample boundary labels are visible. |

## Required Route QA

| Check | `/#/opinion-ecosystem` | `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` |
| --- | --- | --- |
| Page loads | pass | pass |
| Expected sample | Helldivers PSN sample / static default | Dong/Sun selected public sample; no Helldivers fallback |
| Explanation UI visible | pass | pass |
| Module cards visible | pass | pass |
| ContentAggregate visible | pass | pass |
| InfluenceCore visible | pass | pass |
| EchoBox visible | pass | pass |
| PeopleCluster visible | pass | pass |
| ResponseStrategyComparisonV01 visible | pass | pass |
| Selected-sample / mock-default / uncalibrated labels | pass | pass |
| Evidence-not-truth / not-prediction / not-causal-proof / not-official-verification copy | pass | pass |
| ResponseStrategy human-review-only | pass | pass |
| T0-T6 controls visible | pass | pass |
| Console error/warn from Sentigraph app | none observed | none observed |
| Visible 500 / ErrorBoundary / undefined / NaN / `[object Object]` | none observed | none observed |
| Publish/send/post/execute CTA | none observed | none observed |

Notes:

- The phrase family around generated response text appears only in deferred/negative boundary copy, such as "generated response text not implemented" or "Public response generated false". No active response generation UI or CTA was observed.
- The UI remains static/local and explanatory. It does not connect to a backend calculator API.

## Optional Broader Route Smoke

| Route | Result |
| --- | --- |
| `/#/public-events/helldivers-psn` | pass: page loaded, boundary copy visible, no console error/warn, no visible 500/undefined/NaN/`[object Object]`, no publish/send/post/execute CTA |
| `/#/public-events/donglu-sunjihai-youth-football` | pass: page loaded, boundary copy visible, no console error/warn, no visible 500/undefined/NaN/`[object Object]`, no publish/send/post/execute CTA |
| `/#/reports/helldivers-psn-sample` | pass: page loaded, boundary copy visible, no console error/warn, no visible 500/undefined/NaN/`[object Object]`, no publish/send/post/execute CTA |
| `/#/reports/donglu-sunjihai-youth-football-sample` | pass: page loaded, boundary copy visible, no console error/warn, no visible 500/undefined/NaN/`[object Object]`, no publish/send/post/execute CTA |

## Model-card QA Result

| Module | Result |
| --- | --- |
| ContentAggregate | pass: framed as local evidence/content aggregate, not official verification, not truth_score, not full-web coverage |
| InfluenceCore | pass: framed as content / narrative / official / media / meme core, not a real person, not an account graph, not an official cause |
| EchoBox | pass: framed as selected-sample discussion container proxy, not full-platform spread, not final reach measurement, not real community map/full graph |
| PeopleCluster | pass: framed as anonymous aggregate proxy, not real individual users, not targeting, not profiling, not psychological/personality diagnosis |
| ResponseStrategyComparisonV01 | pass: framed as transparent response candidate comparison for human review only, not generated public copy, not response text generation, not auto_execute, not publish/send/post/execute |

C-end readability: pass.

B-end / reviewer wording risk: pass.

## Validation Results

- Frontend build: passed with existing Vite chunk-size warnings only.
- Browser screenshot smoke: passed for required routes.
- Optional broader route smoke: passed.
- Console health: no Sentigraph app error/warn observed during smoke.
- Static/local boundary: passed.

Post-capture validation commands to run:

- `git diff --check`
- `git status --short`
- static safety scan over changed files and relevant 8Q frontend files

## Not Run

- Backend tests: not run because this task changed only docs/assets and no backend files.
- Full pytest: not run because this task changed only docs/assets and no backend files.
- Collector: not run by design.
- Private collector project: not accessed.

## Safety Confirmations

- No backend code changed.
- No frontend product code changed.
- No API routes changed.
- No backend schemas changed.
- No backend tests changed.
- No runtime files changed.
- No package files changed.
- No Project Source files changed.
- No collector touched.
- No collector run.
- No real exchange dirs accessed.
- No `evidence_items.jsonl` or `evidence_items.csv` parsed.
- No Evidence Layer write.
- No production case.
- No analysis_run.
- No B-end report runtime.
- No Sandbox/public event runtime.
- No real API or LLM.
- No URL fetch or scraping.
- No secrets, cookies, sessions, or browser profiles read.
- No GitHub Actions workflow recreated.
- No generated public communication.
- No response text generation.
- No auto_execute / publish / send / post CTA.
- No target-user or identity output.
- No persuasion score.
- No manipulative UI design.

