# Opinion Ecosystem 8S-15 Internal QA Capture Execution Report v0.1

## A. Decision / Status

phase = 8S-15
task = internal_qa_capture_execution
operator_approval = yes
capture_scope = internal_qa_only
trusted_manual_playtest = not_executed
public_recording = blocked
external_distribution = blocked
media_committed = no
source_update_after_commit = no_batch_later

recording_capture = not_executed_tooling_unavailable
internal_qa_capture_status = needs_operator_manual_capture_or_capture_tool_setup
next_state_if_blocked = needs_manual_capture_execution_or_tooling_setup

## B. Environment

| Item | Result |
| --- | --- |
| date/time | 2026-06-27 19:49:45 +08:00 |
| OS | Microsoft Windows NT 10.0.19045.0 |
| shell | Windows PowerShell 5.1.19041.6456 |
| backend already running | yes |
| frontend already running | yes |
| backend start command used | not used |
| frontend start command used | not used |
| recording capability available | no |
| browser/tooling used | Codex in-app browser against local `127.0.0.1` routes |
| servers stopped by this task | no |

No secrets, `.env` values, tokens, cookies, sessions, browser profile paths, private collector paths, personal data, or absolute media file paths were recorded.

## C. Capture-safe Checklist Result

| Checklist item | Result | Notes |
| --- | --- | --- |
| browser has no devtools open | not observable | The local browser route rehearsal did not open devtools. |
| no terminal showing `.env`, API keys, tokens, cookies, sessions, or secret-bearing commands | not observable | No terminal contents were captured or recorded. |
| no file explorer / panel showing private collector path | not observable | No file explorer panels were opened or captured. |
| no personal documents visible | not observable | The rehearsal used a controlled local browser test tab only. |
| no browser profile/cookie/session pages visible | pass | No browser profile, cookie, or session pages were opened. |
| no raw author identifiers visible | pass | Required routes showed no actual raw author identifiers. Optional Analysis Requests route showed only privacy-policy field names in boundary text. |
| page zoom and window size set before recording | not applicable | No recording was executed. |
| only local `127.0.0.1` routes are used | pass | All route checks used local backend/frontend. |
| no external browser tabs are visible | not observable | Other user tabs were not inspected. A controlled local test tab was used. |
| no recorder overlay exposes sensitive paths | not applicable | No recorder was started. |

## D. Route Execution / Capture Results

| Route / step | Expected | Observed | Pass/fail | Captured in recording | Notes |
| --- | --- | --- | --- | --- | --- |
| `/#/demo` | Demo entry visible; local/demo boundary visible or reachable | Opened; local demo/sample boundary visible or reachable | pass | not applicable | No visible 500, ErrorBoundary, `undefined`, `NaN`, or `[object Object]`. |
| `/#/public-events` | Dong/Sun and Helldivers cards visible | Opened; both event cards visible | pass | not applicable | No stop condition observed. |
| `/#/public-events/donglu-sunjihai-youth-football` | Dong/Sun context retained; no fallback to Helldivers; sample/evidence context visible; sandbox/report CTAs visible or reachable | Opened; Dong/Sun context retained; sample/evidence context visible; sandbox and report CTA text present | pass | not applicable | Page text may include broader app references, but route context remained Dong/Sun. |
| `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` | Selected sample remains Dong/Sun; boundary labels visible; generated-run control visible | Opened; Dong/Sun route retained; boundary labels and generated-run control visible | pass | not applicable | Generated-run button count was 1 before click. |
| Explicit click `Load backend local generated run` once | Generated-run metadata appears | Clicked once; generated-run metadata appeared | pass | not applicable | `sentigraph_opinion_ecosystem_run_v0_1` appeared after click. |
| `/#/reports/donglu-sunjihai-youth-football-sample` | B-end report sample visible; report boundary visible; no production report/export claim | Opened; report sample and boundary visible; no production report/export claim observed | pass | not applicable | No stop condition observed. |
| Optional `/#/analysis-requests` | No visible 500; governance sections render; no active public download / signed URL / external delivery capability | Opened; governance sections rendered; public delivery/download gates appeared as boundary-only or disabled controls | pass | not applicable | Privacy-policy field names appeared only in boundary text; no actual raw identifiers were visible. |

## E. Generated-run Check

| Check | Result | Notes |
| --- | --- | --- |
| explicit click | yes | Clicked the unique `Load backend local generated run` control exactly once. |
| selected sample retained | yes | Route remained `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`. |
| generated-run metadata visible | yes | Generated-run metadata appeared after click. |
| run_schema visible | yes | `sentigraph_opinion_ecosystem_run_v0_1` was visible after click. |
| boundary labels visible | yes | Not full-web/platform/thread, not official verification, not causal proof, not prediction/production score boundary labels were visible. |
| module outputs visible | yes | ContentAggregate, InfluenceCore, EchoBox, PeopleCluster, and ResponseStrategyComparisonV01 signals were visible. |
| forbidden fields absent | yes | No generated public response, target-user, persuasion/truth/official/prediction, or psychological profiling output was observed. |
| no public action CTA | yes | No publish/send/post/execute CTA was observed. |

## F. Recording Metadata

recording_status = not_executed
reason = Codex local environment did not provide a safe video recording capability for this task.

recommended_operator_action:

1. Perform a local-only manual recording with a trusted local screen recorder.
2. Store media outside tracked repo paths.
3. Do not commit media.
4. Do not print or share absolute media paths.
5. Keep external distribution blocked until the capture is reviewed.

media_committed = no
external_distribution = no
public_recording = blocked
screenshots_captured = no
absolute_media_path = not_recorded_in_report
review_status = not_started

## G. Issues Found

P0: none

P1: none

P2: none

P3: none

Notes:

- Optional Analysis Requests route displayed privacy-policy field names such as raw author removal rules only as boundary/governance text. No actual raw author identifiers were observed.
- Optional Analysis Requests route displayed public access / external delivery / download language only as boundary/gate text. Public delivery controls observed in the route were disabled or non-active.

## H. Recommendation

Recording was not executed due tooling limitation. The next recommended step is:

Manual capture execution or capture tooling setup for internal QA only.

After a local internal capture is completed and reviewed, the next phase can become:

Phase 8S-16 internal QA capture review or trusted playtest decision.

Do not automatically start a trusted manual playtest.

## I. Source Update Policy

Project Source update = no immediate update

Reason:
8S-15 is internal QA capture/report only, and the capture itself was not executed in this environment.

Batch Source update later only after actual reviewed capture, trusted manual playtest, public/external demo package, code/runtime/API/schema/safety boundary change, or Project Source/repo divergence.

## J. Safety Confirmations

- no trusted manual playtest executed
- no public/external recording produced
- no media committed
- no screenshots captured
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

