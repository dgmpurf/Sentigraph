# Opinion Ecosystem 8S-11 Internal Recording Rehearsal Dry Run Report v0.1

## A. Decision / Status

```text
phase = 8S-11
task = internal_recording_rehearsal_dry_run_execution_report
user_approval = yes
recording_capture = not_executed
trusted_manual_playtest = not_executed
public_launch = not_authorized
dry_run_status = passed
next_state_if_passed = ready_for_8S_12_recording_capture_or_one_trusted_manual_playtest_decision
```

The internal operator/browser dry run passed for the primary Dong/Sun route. No video was recorded, no screenshot was captured, no external user was contacted, and no public launch was authorized.

## B. Environment

| Item | Result |
| --- | --- |
| date/time | 2026-06-27 13:57:16 +08:00 |
| OS/shell | Windows NT 10.0.19045.0 / PowerShell 5.1 |
| backend start command used | not used; backend was already listening on `127.0.0.1:8000` |
| frontend start command used | not used; frontend was already listening on `127.0.0.1:5173` |
| backend docs page status | opened; local HTTP status 200 |
| frontend page status | opened; local HTTP status 200 |
| browser/tooling used | Codex in-app browser, local `127.0.0.1` routes only |
| server started by this task | no |
| server stopped by this task | no; no task-owned server process was started |

No secrets, usernames, tokens, cookies, sessions, private paths, browser profile paths, or private collector paths were recorded.

## C. Primary Route Result

| Route | Expected purpose | Opened | Visible issue | Notes |
| --- | --- | --- | --- | --- |
| `/#/demo` | guided demo entry | yes | no | Local demo entry opened. |
| `/#/public-events` | public event plaza | yes | no | Event Plaza opened. |
| `/#/public-events/donglu-sunjihai-youth-football` | Dong/Sun public event detail | yes | no | Dong/Sun detail opened; no Helldivers fallback. |
| `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` | Dong/Sun Opinion Ecosystem query route | yes | no | Dong/Sun sample selected; generated-run panel visible. |
| `/#/reports/donglu-sunjihai-youth-football-sample` | Dong/Sun B-end report sample | yes | no | Report sample opened. |

Optional route checks were also performed after the primary route passed:

| Route | Opened | Visible issue | Notes |
| --- | --- | --- | --- |
| `/#/opinion-ecosystem` | yes | no | Default Helldivers/sample route opened. |
| `/#/public-events/helldivers-psn` | yes | no | Helldivers event detail opened. |
| `/#/reports/helldivers-psn-sample` | yes | no | Helldivers report sample opened. |

## D. Generated-run Check

| Check | Result |
| --- | --- |
| selected sample | `donglu_sunjihai_youth_football` |
| generated-run click explicit | yes |
| request count if observable | not_observable in in-app browser; no generated-run metadata appeared before click, and metadata appeared after the explicit click |
| run status | ready |
| metadata visible | yes |
| boundary labels visible | yes |
| module outputs visible | yes |
| blockers/warnings visible | yes |
| no forbidden CTA | yes |
| no generated public response | yes |

Additional raw-identifier check:

- `author_id`, `author_name`, and `profile_url` values were not exposed as data.
- The page includes boundary text such as “no raw author identifiers” / “不暴露 raw author_id or raw author_name”; this is safety copy, not raw identifier exposure.

## E. Boundary Language Check

| Boundary line | Visible in UI | Spoken/rehearsable | Notes |
| --- | --- | --- | --- |
| 这是本地 demo | yes | yes | Local demo labels visible. |
| selected sample only | yes | yes | Selected-sample labels visible. |
| 不是全网全量 | yes | yes | `not full-web` visible. |
| 不是全平台全量 | yes | yes | `not full-platform` visible. |
| 不是完整讨论线 | yes | yes | `not full-thread` visible. |
| 不是官方验证 | yes | yes | `not official verification` visible. |
| 不是因果证明 | yes | yes | `not causal proof` visible. |
| 不是预测 | yes | yes | `not prediction` visible. |
| generated run 是本地 fixture 输出 | yes | yes | Backend local fixture generated-run copy visible. |
| PeopleCluster 是匿名聚合群体 / 行为代理 | partial | yes | PeopleCluster safety/model-card language visible; operator should still say this line clearly. |
| InfluenceCore 是内容 / 叙事 / 官方 / 媒体 / meme 核心，不是人群小球 | partial | yes | InfluenceCore distinction visible in model/module copy; operator should still say this line clearly. |
| ResponseStrategyComparison 只用于人工复核 | yes | yes | Human-review boundary visible. |
| 不生成公开回应 | yes | yes | `no generated public response` visible. |
| 不自动执行任何平台动作 | yes | yes | `no auto execution` visible. |

## F. Stop-condition Check

| Stop condition | Triggered |
| --- | --- |
| backend/frontend crash | no |
| visible 500 | no |
| ErrorBoundary | no |
| `undefined` / `NaN` / `[object Object]` | no |
| generated-run click fails | no |
| publish / send / post / execute CTA appears | no |
| generated public response text appears | no |
| raw author identifiers appear | no actual identifiers; only safety boundary wording appeared |
| secrets / `.env` / tokens / cookies visible | no |
| private collector path appears | no |
| demo implies live crawling / official truth / production score | no |

Console result:

- Sentigraph app console error/warn count on checked routes: 0

## G. Timing Notes

Exact spoken timing was `not_measured` because this dry run used browser automation for route stability and UI checks rather than live narration.

| Section | Target duration | Actual duration | Notes | Issue |
| --- | --- | --- | --- | --- |
| Intro and local-demo boundary | 0:30 | not_measured | route opened | no |
| Event Plaza | 0:30 | not_measured | route opened | no |
| Dong/Sun event detail | 0:45 | not_measured | route opened | no |
| Opinion Ecosystem route open | 0:30 | not_measured | Dong/Sun query route preserved | no |
| Generated-run click and metadata | 1:00 | not_measured | explicit click succeeded | no |
| Boundary labels and modules | 1:00 | not_measured | labels/modules visible | no |
| B-end report sample | 1:00 | not_measured | route opened | no |
| Closing boundary | 0:30 | not_measured | boundary checklist rehearsable | no |

Recommendation: if 8S-12 chooses recording capture, run a human-timed rehearsal before final capture.

## H. Issues Found

| Severity | Issues |
| --- | --- |
| P0 | none |
| P1 | none |
| P2 | none |
| P3 | none |

No route-blocking, privacy, boundary, generated-run, forbidden CTA, or console issues were found in this dry run.

## I. Recommendation

Recommended next phase:

`Phase 8S-12 recording capture or one trusted manual playtest decision`

Do not automatically start 8S-12. It requires explicit user approval.

If 8S-12 chooses recording capture, do one human-timed rehearsal first because this 8S-11 pass verified route stability and UI boundaries but did not measure spoken pacing.

## J. Safety Confirmations

- no external users contacted
- no video recorded
- no screenshots captured
- no media generated
- no collector/private collector accessed
- no real APIs called
- no real LLM called
- no URL fetching/scraping
- no Evidence Layer write
- no production case / `analysis_run`
- no B-end report runtime
- no Sandbox/public event runtime
- no generated public response
- no publish / send / post / execute
- no secrets read or printed
- no GitHub Actions workflow recreated
