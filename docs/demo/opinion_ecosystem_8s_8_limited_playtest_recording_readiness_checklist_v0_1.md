# Opinion Ecosystem 8S-8 Limited Playtest / Recording Readiness Checklist v0.1

## A. Purpose

This checklist prepares a limited trusted manual playtest or internal recording rehearsal.

It does not execute playtest, does not contact users, does not record video, does not generate media, does not run collector jobs, and does not call real APIs or real LLMs.

## B. Pre-flight Setup

Backend:

```bat
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
.venv\Scripts\activate
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Frontend:

```bat
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"
npm run dev
```

## C. Pre-flight Checks

Check before any playtest or recording rehearsal:

- backend docs page opens at `http://127.0.0.1:8000/docs`
- frontend opens at `http://127.0.0.1:5173`
- `/#/opinion-ecosystem` loads
- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` loads
- generated-run explicit click succeeds
- no visible 500
- no visible `undefined`
- no visible `NaN`
- no visible `[object Object]`
- no console error/warn
- no secrets visible
- no `.env`, API keys, tokens, cookies, sessions, or browser profile paths visible on screen

## D. Recommended 3-Minute Recording Route

Use Dong/Sun as the primary route:

1. `/#/demo`
2. `/#/public-events`
3. `/#/public-events/donglu-sunjihai-youth-football`
4. `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
5. click generated-run panel
6. show boundary labels and module outputs
7. `/#/reports/donglu-sunjihai-youth-football-sample`
8. close with “selected sample / local demo / human review required” boundary

Suggested close:

> 这只是 selected sample 和本地 generated-run 展示，不代表全网全量、官方验证、因果证明或生产分数。所有 ResponseStrategyComparison 都需要人工复核，不生成公开回应，也不会自动执行。

## E. Recommended 8-Minute Recording Route

Include:

- `/#/demo`
- `/#/public-events`
- Dong/Sun detail page
- Dong/Sun Sandbox generated-run
- Dong/Sun B-end report sample
- optional request/support mock page
- optional Helldivers/default comparison
- optional external collector boundary explanation

Optional technical-governance route:

- Use `/#/analysis-requests` only if the backend is running and the page has no visible 500.
- If any visible backend error appears, skip this route and explain that governance route capture is deferred.

## F. Trusted Manual Playtest Instructions

For a trusted tester:

- ask what they think the product does before explaining
- ask whether they think it is live/full-web
- ask whether they understand selected sample only
- ask whether they understand PeopleCluster is not a real person
- ask whether generated run appears more convincing than static explanation
- ask what was confusing
- do not let them enter private or sensitive real data
- do not claim backend is crawling anything
- do not claim request/vote/support numbers are real heat or real demand

Recommended opening:

> 我想先看你自然理解这个 demo 的方式。你可以边点边说：你觉得它在做什么、哪些地方可信、哪些地方让你误解。注意这里不是全网抓取，也不是官方验证；请不要输入任何私人或敏感信息。

## G. Stop Conditions

Stop immediately if:

- user thinks system is crawling live web and cannot be corrected
- user thinks generated run is official truth
- user thinks small balls are real people
- UI shows 500 / ErrorBoundary / `undefined` / `NaN` / `[object Object]`
- publish / send / post / execute CTA appears
- generated response text appears
- raw author identifiers appear
- secrets / `.env` / tokens / cookies are visible
- backend or frontend crashes
- private collector path or browser profile path appears

Also stop if any route appears to expose:

- `response_text`
- `generated_public_message`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`
- `auto_execute`

These may appear only in stop-condition or forbidden-field documentation, not as product behavior.

## H. Post-run Notes Template

```text
tester type:
route used:
confusion points:
boundary misunderstanding:
value perception:
biggest UI blocker:
whether generated-run display helped:
whether B-end report sample was useful:
suggested next fix:
privacy/safety issue yes/no:
```

Use notes only for product feedback. Do not record private account data, platform login state, personal sensitive data, cookies, tokens, sessions, API keys, or secrets.
