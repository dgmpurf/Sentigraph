# Opinion Ecosystem 8S-10 Internal Recording Rehearsal Dry Run Execution Sheet v0.1

## A. Purpose

This sheet prepares an internal dry run.

It does not execute recording by itself, does not contact users, does not generate media, and does not authorize public launch.

Use this only after the operator explicitly approves Phase 8S-11 dry-run execution.

## B. Operator Preflight

Checklist:

- close unrelated tabs
- hide desktop files
- hide terminals with `.env` / API keys / tokens
- do not show private collector path
- do not use personal browser profile
- do not log into personal accounts
- backend docs page opens
- frontend opens
- Dong/Sun primary route opens
- generated-run click succeeds
- report sample opens
- no visible 500 / ErrorBoundary / `undefined` / `NaN` / `[object Object]`

## C. Primary Dry-run Route

Use:

1. `/#/demo`
2. `/#/public-events`
3. `/#/public-events/donglu-sunjihai-youth-football`
4. `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
5. explicit generated-run click
6. show run metadata / boundary labels / module outputs
7. `/#/reports/donglu-sunjihai-youth-football-sample`
8. close with selected sample / local demo / human review required boundary

Do not include optional routes unless the operator explicitly chooses them during preflight.

## D. Timing Worksheet

| Section | Target duration | Actual duration | Notes | Issue yes/no |
| --- | --- | --- | --- | --- |
| Intro and local-demo boundary | 0:30 |  |  |  |
| Event Plaza | 0:30 |  |  |  |
| Dong/Sun event detail | 0:45 |  |  |  |
| Opinion Ecosystem route open | 0:30 |  |  |  |
| Generated-run click and metadata | 1:00 |  |  |  |
| Boundary labels and modules | 1:00 |  |  |  |
| B-end report sample | 1:00 |  |  |  |
| Closing boundary | 0:30 |  |  |  |
| Total | 5:45 target |  |  |  |

## E. Spoken Boundary Checklist

Say or verify:

- 这是本地 demo
- selected sample only
- 不是全网全量
- 不是全平台全量
- 不是完整讨论线
- 不是官方验证
- 不是因果证明
- 不是预测
- generated run 是本地 fixture 输出
- PeopleCluster 是匿名聚合群体 / 行为代理
- InfluenceCore 是内容 / 叙事 / 官方 / 媒体 / meme 核心，不是人群小球
- ResponseStrategyComparison 只用于人工复核
- 不生成公开回应
- 不自动执行任何平台动作

## F. Dry-run Result Template

```text
date/time:
operator:
backend running yes/no:
frontend running yes/no:
route completed yes/no:
generated-run click success yes/no:
report page success yes/no:
console error/warn yes/no:
visible UI issue yes/no:
stop condition triggered yes/no:
timing issue yes/no:
boundary explanation issue yes/no:
privacy/safety issue yes/no:

recommended next action:
  needs_fix
  repeat_internal_dry_run
  approve_one_trusted_manual_playtest
  approve_recording_capture
  stop

notes:
```

Do not record secrets, raw author identifiers, private account data, tokens, cookies, sessions, browser profile paths, private collector paths, or real exchange dirs in this sheet.

## G. Triage Mapping

If P0:

- stop
- create needs_fix task
- do not run trusted playtest
- do not capture recording

If P1:

- fix copy/UX before any trusted playtest or recording capture
- repeat internal dry run after fix

If only P2/P3:

- allow one more internal rehearsal, or
- ask user to approve one trusted manual playtest
