# Opinion Ecosystem 8S-13 Full-stack Runtime Readiness Gate Report v0.1

## A. Decision / Status

phase = 8S-13
task = full_stack_runtime_readiness_gate
selected_path = full_stack_runtime_readiness_gate_first
recording_capture = deferred
trusted_manual_playtest = deferred
frontend_polish = deferred

full_stack_readiness_status = passed
next_state_if_passed = ready_for_8S_14_recording_scope_or_trusted_playtest_decision_after_full_stack_gate

## B. Environment

| Item | Result |
| --- | --- |
| date/time | 2026-06-27 18:59:28 +08:00 |
| OS | Microsoft Windows NT 10.0.19045.0 |
| shell | Windows PowerShell 5.1.19041.6456 |
| Python | Python 3.10.11 |
| pytest | pytest 9.0.3 |
| backend already running | yes |
| frontend already running | yes |
| backend start command used | not used |
| frontend start command used | not used |
| servers stopped by this task | no |
| browser/tooling used | Codex in-app browser against local `127.0.0.1` routes |

No secrets, `.env` values, tokens, cookies, sessions, browser profile paths, private collector paths, or personal data were recorded.

## C. Test Results

| Command | Result | Passed count | Warnings | Notes |
| --- | --- | ---: | --- | --- |
| `git status --short` | passed | n/a | none | Clean before starting. |
| `git diff --check` | passed | n/a | none | No whitespace errors. |
| `python -m pytest backend/app/tests/test_opinion_ecosystem_generated_run_routes.py` | passed | 6 | none observed | Generated-run route tests passed. |
| `python -m pytest backend/app/tests/test_opinion_ecosystem_minimum_real_run.py` | passed | 8 | none observed | Minimum real-run contract tests passed. |
| `python -m pytest backend/app/tests/test_opinion_ecosystem_mock_calculator.py` | passed | 112 | none observed | Pure local calculator chain tests passed. |
| `python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py` | passed | 7 | none observed | Governance golden contract tests passed. |
| `python -m pytest backend/app/tests/test_external_collector_bridge.py` | passed | 6 | none observed | External collector bridge boundary tests passed. |
| `python -m pytest backend/app/tests/test_local_exchange_reader.py` | passed | 9 | none observed | Local exchange reader tests passed. |
| `npm.cmd --prefix frontend run build` | passed | n/a | Vite chunk size warning | Build completed successfully; chunk warning is non-blocking. |

## D. Backend Runtime Smoke Results

| Endpoint / action | Expected | Actual | Pass/fail | Notes |
| --- | --- | --- | --- | --- |
| `GET /docs` | 200 OK | 200 OK | pass | Local backend docs page opened. |
| `GET /openapi.json` | 200 OK | 200 OK | pass | Local OpenAPI document returned. |
| `POST /api/v1/opinion-ecosystem/generated-runs/local-fixture` with `sample_key=donglu_sunjihai_youth_football` | 200 / ready | 200 / ready | pass | `run_schema=sentigraph_opinion_ecosystem_run_v0_1`; required boundaries and modules present. |
| `POST /api/v1/opinion-ecosystem/generated-runs/local-fixture` with `sample_key=helldivers_psn` | 200 / ready | 200 / ready | pass | `run_schema=sentigraph_opinion_ecosystem_run_v0_1`; required boundaries and modules present. |
| `POST /api/v1/opinion-ecosystem/generated-runs/local-fixture` with unknown sample key | safe 4xx | 400 | pass | Returned `unsupported_sample_key`; no unsafe fallback observed. |

## E. Frontend / Browser Full-stack Route Results

| Route | Expected purpose | Opened | Backend-dependent behavior verified | Visible issue | Console issue | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `/#/demo` | Guided demo entry | yes | n/a | no | no | Local demo/sample boundary wording was visible or reachable. |
| `/#/public-events` | Event plaza | yes | n/a | no | no | Dong/Sun and Helldivers event cards were visible. |
| `/#/public-events/donglu-sunjihai-youth-football` | Dong/Sun public event detail | yes | n/a | no | no | Dong/Sun context retained; no fallback to Helldivers. |
| `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` | Dong/Sun Opinion Ecosystem sandbox | yes | yes | no | no | Generated-run control visible before click; run metadata visible after explicit click. |
| `/#/reports/donglu-sunjihai-youth-football-sample` | Dong/Sun B-end report sample | yes | n/a | no | no | Report boundary visible; no generated production report claim observed. |
| `/#/analysis-requests` | Governance / Analysis Requests route | yes | yes | no | no | Governance sections rendered without visible 500; no active public download or signed URL capability observed. |

Optional routes were also checked after required routes passed:

| Route | Result | Notes |
| --- | --- | --- |
| `/#/opinion-ecosystem` | opened | Default sandbox route rendered. |
| `/#/public-events/helldivers-psn` | opened | Helldivers event route rendered. |
| `/#/reports/helldivers-psn-sample` | opened | Helldivers report sample route rendered. |

CTA route checks on the Dong/Sun detail page:

| CTA | Result |
| --- | --- |
| `查看本地历史复盘沙盒` | navigated to `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` |
| `查看 B端报告样例` | navigated to `/#/reports/donglu-sunjihai-youth-football-sample` |

## F. Generated-run UI Contract Check

| Check | Result | Notes |
| --- | --- | --- |
| explicit click | yes | Clicked the unique `Load backend local generated run` button once. |
| backend request success | yes | Success inferred from generated-run metadata and `run_schema` appearing after the explicit click. |
| selected sample retained | yes | Route remained `sample=donglu-sunjihai-youth-football`; Dong/Sun context remained visible. |
| run metadata visible | yes | `sentigraph_opinion_ecosystem_run_v0_1` appeared after click. |
| boundary labels visible | yes | Not full-web/platform/thread, not official verification, not causal proof, not prediction/production score boundaries were visible. |
| module outputs visible | yes | ContentAggregate, InfluenceCore, EchoBox, PeopleCluster, and ResponseStrategyComparisonV01 signals were visible. |
| forbidden fields absent | yes | No `response_text`, `generated_public_message`, target-user, persuasion/truth/official/prediction, or psychological profiling fields observed. |
| no public action CTA | yes | No publish/send/post/execute CTA observed. |

## G. Analysis Requests Route Check

| Check | Result | Notes |
| --- | --- | --- |
| route opened | yes | `/#/analysis-requests` opened with backend running. |
| backend required | yes | Route depends on backend governance data. |
| no visible 500 | yes | No visible 500 prompt observed. |
| no ErrorBoundary / undefined / NaN / `[object Object]` | yes | None observed. |
| no public download / signed URL / external delivery active capability | yes | Boundary/gate sections visible; no active unsafe delivery control observed. |

## H. Issues Found

P0: none

P1: none

P2: none

P3: none

## I. Recommendation

Phase 8S-13 full-stack runtime readiness gate passed. The next phase should be:

Phase 8S-14 recording scope or trusted playtest decision after full-stack gate.

Do not automatically start recording or trusted playtest. 8S-14 requires explicit user approval.

## J. Safety Confirmations

- no recording captured
- no screenshots captured
- no trusted manual playtest executed
- no frontend behavior changed
- no backend code changed
- no tests changed
- no Project Source changed
- no collector/private collector accessed
- no real APIs called
- no real LLM called
- no URL fetching/scraping
- no Evidence Layer write
- no production case / analysis_run
- no B-end report runtime
- no Sandbox/public event runtime
- no generated public response
- no publish/send/post/execute
- no secrets read or printed
- no GitHub Actions workflow recreated

