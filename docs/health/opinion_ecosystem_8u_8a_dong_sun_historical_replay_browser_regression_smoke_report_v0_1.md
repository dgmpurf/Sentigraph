# Opinion Ecosystem 8U-8A Dong/Sun Historical Replay Browser Regression Smoke Report v0.1

## A. Decision / Status

phase = 8U-8A

task = dong_sun_historical_replay_browser_regression_smoke

decision = partial

privacy_issue_stop = no

browser_smoke = yes

backend_code_changed = no

frontend_code_changed = no

route_changed = no

api_route_added = no

dense_graph_frontend_implementation = no

real_api_called = no

real_llm_called = no

collector_run = no

url_fetch_or_scrape = no

Summary:

- Required Dong/Sun navigation routes opened successfully.
- Dong/Sun event detail CTAs preserved `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`.
- Direct Dong/Sun query route selected the Dong/Sun youth football sample and showed Dong/Sun T0-T6 timeline content.
- Default `/#/opinion-ecosystem` still selected the Helldivers sample and did not regress to Dong/Sun by default.
- No P0 or P1 regression was found.
- One P2 visual clarity note remains: Dong/Sun PeopleCluster balls are visible, but relatively small and sparse compared with InfluenceCore nodes.

## B. Routes Tested

- `/#/public-events`
- `/#/public-events/donglu-sunjihai-youth-football`
- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- `/#/reports/donglu-sunjihai-youth-football-sample`
- Control route: `/#/opinion-ecosystem`

## C. Interaction Results

| Source page | CTA label / location | Resulting URL | Active sample | Timeline shown | Result |
| --- | --- | --- | --- | --- | --- |
| `/#/public-events` | `查看受控样本详情` on Dong/Sun event card | `/#/public-events/donglu-sunjihai-youth-football` | Dong/Sun event detail | Not applicable | Pass |
| `/#/public-events/donglu-sunjihai-youth-football` | `查看本地历史复盘沙盒` | `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` | Dong/Sun youth football sample mode | Dong/Sun T0-T6 | Pass |
| `/#/public-events/donglu-sunjihai-youth-football` | `查看 T0-T6 本地历史复盘` | `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` | Dong/Sun youth football sample mode | Dong/Sun T0-T6 | Pass |

Dong/Sun T0-T6 phase controls were clickable and showed these local historical replay stages:

- T0: 争议背景进入公众视野
- T1: 社区讨论扩散
- T2: 阵营化与青训路线分歧
- T3: 媒体转述与二次解释
- T4: 情绪高峰与极端表达隔离
- T5: 舆论疲劳与普通用户退出
- T6: 声誉记忆与长期议题沉淀

Helldivers / PSN text appeared on the Sandbox page only as a data-source option, not as the active Dong/Sun sample.

## D. Direct Route Result

Direct route tested:

`/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`

Result:

- Dong/Sun sample selected on initial load: pass.
- Dong/Sun evidence summary visible: pass.
- Sample summary visible: `581 evidence`, `37 sources`, `546 comments`, `35 roots`: pass.
- T0-T6 quick controls near the canvas: pass.
- Marker / PeopleCluster proxy explanation visible: pass.
- Boundary labels visible: pass.

Visible boundary labels included:

- selected sample / selected public sample where applicable
- not full-web
- not full-platform
- not official verification
- not causal proof
- not prediction
- no real API / LLM
- PeopleCluster anonymous aggregate proxy

## E. Helldivers Default Control

Control route tested:

`/#/opinion-ecosystem`

Result:

- Default route still selected Helldivers sample behavior: pass.
- Default route did not select Dong/Sun unless the query string requested Dong/Sun: pass.
- T0-T6 controls still rendered: pass.
- No visible 500, ErrorBoundary, `[object Object]`, `undefined`, or `NaN`: pass.

## F. Visual Clarity Notes

balls_visible = yes

sparse_or_unclear = yes, P2

spinner_or_rotating_marker_confusing = no blocking spinner found

marker_explanation_visible = yes

peoplecluster_proxy_copy_visible = yes

Notes:

- EchoBox rendered clearly as a strong container.
- InfluenceCore nodes were visually distinct from PeopleCluster balls.
- Dong/Sun PeopleCluster balls were visible as small points around the EchoBox, but they were less prominent than InfluenceCore nodes and may feel sparse or easy to miss during a friend/customer demo.
- No indefinite loading spinner was observed. A small animated/highlight marker may be read as a local animation cue, but it did not block understanding or appear to be a loading state.

## G. Safety Checks

- no raw author/profile values: pass.
- no profile URL exposure: pass.
- no secrets: pass.
- no publish / send / post / execute CTA: pass.
- no real API / real LLM / collector run: pass.
- no `[object Object]`: pass.
- no `undefined` / `NaN`: pass.
- no visible 500 / ErrorBoundary: pass.

Clarification:

- `author_id` and `author_name` appeared only inside validator/boundary text saying raw identifiers are not exposed. No raw author values or profile URLs were visible.
- `发布`, `发送`, `post`, and `execute` appeared only in negative boundary language such as not publishing, sending, executing, or performing account actions. No actionable publish/send/post/execute CTA was visible.

## H. Screenshots

Screenshots were captured under:

`docs/demo/assets/donglu_sunjihai_historical_replay_regression_smoke/`

Files:

- `01_public_events_dong_sun_card.png`
- `02_dong_sun_detail_cta_area.png`
- `03_dong_sun_sandbox_after_cta_top.png`
- `04_dong_sun_sandbox_timeline_controls.png`
- `05_dong_sun_peoplecluster_marker_area.png`
- `06_dong_sun_report_route.png`

## I. Issues P0/P1/P2/P3

P0:

- None found.

P1:

- None found.
- Dong/Sun CTAs did not open Helldivers / PSN as the active sample.
- Dong/Sun query route did not fall back to Helldivers.
- Dong/Sun timeline matched the youth-football replay stages.
- No visible ErrorBoundary or 500 appeared.
- No infinite spinner blocked understanding.

P2:

- Dong/Sun PeopleCluster balls are visible but visually small/sparse relative to InfluenceCore nodes.
- The page is demo-usable, but a small frontend polish decision would improve first-time user readability before dense graph frontend/API integration.

P3:

- None requiring immediate action in this smoke.

## J. Recommendation

Recommended next action:

- Because no P0/P1 issue was found but one P2 visual clarity issue remains, run a small frontend polish decision before dense graph frontend/API integration.
- After that, proceed to 8U-8B dense graph frontend/API contract refinement or pause for product review.

Recommended commit message:

`Add Dong/Sun historical replay browser regression smoke report`

Recommended tag:

No tag needed.

Source recommendation:

No immediate Source update. Do not create Source files in repo.

## Validation

Commands run:

- `git status --short`: initial clean working tree before screenshots/report.
- `git branch --show-current`: `main`
- `git rev-parse HEAD`: `c654fffbcb5466449e7a177016b61e07aa8e8cda`
- `git log --oneline -8`:
  - `c654fff Add 8U-7 dense graph frontend integration decision`
  - `561d843 Add 8U-6 dense graph route validation report`
  - `dcda98e Implement 8U-5 dense graph internal route`
  - `b998212 Add 8U-4 dense graph route contract`
  - `a94517f Implement 8U-3 dense graph generated-run integration`
  - `a73d17d Implement 8U-2 dense graph generated-run attachment`
  - `c7b689a Implement 8U-1 dense opinion graph builder`
  - `19fdc91 Add 8S-16-NR no-recording path decision`
- `npm --prefix frontend run build`: pass.
  - Vite emitted existing large chunk warnings only.
- `git diff --check`: pass before report creation.

Backend tests were not run because this was browser QA / report-only and the required routes rendered through the existing frontend without needing backend validation.
