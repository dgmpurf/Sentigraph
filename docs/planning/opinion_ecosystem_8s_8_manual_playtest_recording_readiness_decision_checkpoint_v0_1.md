# Phase 8S-8 Manual Playtest / Recording Readiness Decision Checkpoint v0.1

## A. Decision

```text
phase = 8S-8
decision = manual_playtest_recording_readiness_decision
current_state = ready_for_8S_8_manual_playtest_or_recording_readiness_decision
manual_playtest_readiness = approved_for_limited_trusted_manual_playtest_preparation
recording_readiness = approved_for_internal_recording_rehearsal_preparation
next_state_if_ready = ready_for_8S_9_limited_manual_playtest_and_recording_rehearsal_package
```

8S-8 approves preparation only. It does not execute manual playtest, does not contact external users, does not record video, does not generate media, and does not authorize public launch or production deployment.

The decision is based on the 8S-7 generated-run browser QA, copy polish, and screenshot smoke evidence. The evidence is sufficient for a limited trusted manual playtest preparation path and an internal recording rehearsal preparation path, provided all boundaries below remain visible and respected.

## B. Evidence Reviewed

- 8S-6 added the first frontend generated-run display slice inside the Opinion Ecosystem Sandbox.
- 8S-7 completed browser QA, copy polish, and screenshot smoke for generated-run display.
- Screenshot package route coverage included:
  - `/#/opinion-ecosystem`
  - `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- Generated-run click behavior:
  - before click: `0` generated-run API calls
  - after explicit click: `1` local fixture generated-run call per route
- Visible issue scan:
  - no visible 500
  - no ErrorBoundary
  - no `undefined`
  - no `NaN`
  - no `[object Object]`
  - no publish / send / post / execute CTA
  - no generated public response text
  - no raw author identifiers
- Backend targeted test result from 8S-7: `133 passed`.
- Frontend build result from 8S-7: passed, with only the existing Vite large-chunk warning.
- Screenshot package added six PNG files, README, and screenshot capture report under `docs/demo/assets/opinion_ecosystem_8s_7_generated_run_smoke/`.

## C. What Is Now Allowed If Ready

The next phase may prepare only:

- limited trusted manual playtest with known users
- internal recording rehearsal
- local demo recording preparation
- scripted C-end walkthrough
- scripted B-end reviewer walkthrough
- screenshot-based explanation package refinement

These are preparation activities. They do not mean playtest or recording has happened.

## D. What Is Still Not Allowed

The following remain blocked:

- public launch
- public beta
- production deployment
- external mass user testing
- paid sponsor flow
- real payment
- real user accounts
- real vote/support backend
- real platform API
- real LLM
- private collector integration
- real package row parsing
- `evidence_items.jsonl` / `evidence_items.csv` parsing
- real exchange dir read
- production Evidence write
- production case / `analysis_run`
- B-end report runtime
- Sandbox/public event runtime generation
- generated response text
- Strategy Lab runtime
- publish / send / post / execute behavior
- `auto_execute`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

If any of these appear as an active capability rather than boundary, stop-condition, or forbidden-language text, the next phase must stop.

## E. Approved Demo Route Scope If Ready

Primary C-end route:

1. `/#/demo`
2. `/#/public-events`
3. `/#/public-events/donglu-sunjihai-youth-football`
4. `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
5. explicit generated-run click inside Opinion Ecosystem Sandbox
6. `/#/public-events/request`
7. `/#/reports/donglu-sunjihai-youth-football-sample`

Secondary route:

1. `/#/opinion-ecosystem`
2. explicit generated-run click for Helldivers/default sample
3. `/#/public-events/helldivers-psn`
4. `/#/reports/helldivers-psn-sample`

Optional route:

- `/#/external-collector` only if explaining the local package source boundary.
- `/#/analysis-requests` only if the backend is running and no visible 500 appears. If a visible 500 appears, keep this route out of recording and playtest path.

## F. Required Talking Points

Must say:

- This is a local demo using selected samples.
- It is not full-web coverage.
- It is not full-platform coverage.
- It is not full-thread coverage.
- It is not official verification.
- It is not causal proof.
- It is not prediction.
- It is not a production score.
- The generated run is local fixture only.
- PeopleCluster means anonymous aggregate group / behavioral proxy, not real individual users.
- InfluenceCore means content / narrative / official / media / meme core, not people.
- ResponseStrategyComparison is human-review-only.
- There is no generated public response.
- There is no auto execution.
- There is no publish / send / post / execute action.

Recommended Chinese wording:

> 这是本地 demo 和 selected sample 展示，不代表全网、全平台或完整讨论线。生成运行只是本地 fixture 输出，不是官方验证、因果证明、预测或生产分数。PeopleCluster 是匿名聚合群体/行为代理，不是真实个人；InfluenceCore 是内容、叙事、官方、媒体或 meme 核心，不是人群小球。ResponseStrategyComparison 只用于人工复核前的候选比较，不生成公开回应，也不会自动执行任何动作。

## G. Readiness Risks And Mitigations

| Risk | Mitigation copy |
| --- | --- |
| User may think this is live crawling. | “这里没有实时抓取、没有 crawler job、没有 URL fetch，只展示本地 selected sample 和本地 fixture generated run。” |
| User may think the Dong/Sun sample is full truth. | “Dong/Sun 是受控候选公共样本，不代表全网全量、全平台全量、完整讨论线或官方验证。” |
| User may think generated run is a production score. | “当前分数/模块输出是本地 deterministic demo output，未校准、未做经验验证，human review required。” |
| User may think small balls represent real people. | “PeopleCluster 小球是匿名聚合群体/行为代理，不是个人用户、账号画像或目标用户列表。” |
| User may think suggestions are automatic PR advice. | “ResponseStrategyComparison 是人工复核前的候选比较，不生成回应文案，不发布、不发送、不执行。” |
| User may click routes that need backend and see 500. | “录制前只保留已检查路线；`/#/analysis-requests` 只有在后端运行且没有可见 500 时才展示。” |
| User may ask for “real-time data” or “抓取一下”. | “真实数据接入需要授权、合规和单独 provider gate；当前 demo 不运行抓取、不调用真实 API、不读取私有 collector。” |

## H. Acceptance Criteria For 8S-9

Future 8S-9 can proceed only if:

- repo is clean or the exact intended 8S-8 docs commit is complete
- frontend build passes
- default and Dong/Sun routes still smoke
- generated-run panel still works with explicit click
- no visible 500 / ErrorBoundary / `undefined` / `NaN` / `[object Object]`
- no publish / send / post / execute CTA
- no generated response text
- no raw author identifiers
- user has a script and route checklist
- user explicitly decides to start internal recording rehearsal or limited trusted playtest

## I. Source Recommendation

After the 8S-8 commit:

- update Source 00
- update Source 08
- update Source 09
- update Source 10

Do not update Source 11 unless Analysis Request / Provider / Import Governance behavior changes.
