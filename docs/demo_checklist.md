# Sentigraph Local Demo Checklist

Use this checklist for the current v0.9 case-based, mock-first desktop web MVP demo.

Latest pre-v1.0 hardening validation: 2026-05-15. Backend tests passed with `92 passed in 2.82s`. Frontend production build passed in 7.75s with the existing non-blocking Ant Design/ECharts vendor chunk warning. API smoke check passed with `26 passed, 0 failed` against a temporary local backend and temporary project-local JSON store. New local demo utilities are available for safe runtime data reset, deterministic demo seeding, and local API smoke validation. No real email, Slack, webhook, Enterprise WeChat, Feishu, SMS, push, crawler, platform API, Reddit credential, MongoDB, Redis, or external LLM call is made.

Latest v0.9 notification QA validation: 2026-05-14. Backend tests passed with `90 passed in 2.34s`. Frontend production build passed in 7.61s with the existing non-blocking Ant Design/ECharts vendor chunk warning. Isolated API smoke checks confirmed alert events create local `in_app` notification outbox items, notifications can be listed by case or globally, `标记已读` sets `read_at`, `模拟发送` sets `simulated_sent_at`, and `模拟发送待处理通知` updates all pending local notifications. No real email, Slack, webhook, Enterprise WeChat, Feishu, SMS, push, crawler, platform API, or external LLM call is made.

Latest v0.8 scheduler QA validation: 2026-05-14. Backend tests passed with `81 passed in 1.76s`. Frontend production build passed in 7.46s with the existing non-blocking Ant Design/ECharts vendor chunk warning. API smoke checks confirmed enabling monitoring, `GET /api/v1/scheduler/status`, `POST /api/v1/scheduler/run-due`, disabled/not-due cases being skipped, case-specific alert thresholds, snapshot/alert persistence, disabling monitoring, and the old `monitor/run` endpoint. The scheduler foundation is manual only; no background worker starts by default.

Latest v0.7 monitoring QA validation: 2026-05-14. Backend tests passed with `68 passed in 1.05s`. Frontend production build passed in 7.45s with the existing non-blocking Ant Design/ECharts vendor chunk warning. API smoke checks confirmed the monitoring flow creates persisted snapshots and alerts, including a deterministic `12.0` latest risk delta after repeated monitor runs. The Risk Monitor page supports persisted snapshots, case alert events, and a `Run Mock Monitoring Check` action. In-app browser automation timed out during this QA pass, so manually click through Risk Monitor before a live demo.

Latest v0.6 persistence validation: 2026-05-14. Backend tests passed with `55 passed in 0.51s`. Case API tests now verify create/list/detail/run, Chinese report attachment, Markdown export, and retrieval after reloading the repository/store from the same local JSON file. Frontend build was not rerun because no frontend files changed.

Latest v0.4 adapter-foundation validation: 2026-05-14. Backend tests passed with `47 passed in 0.42s`, frontend production build passed in 7.68s, and API smoke checks passed for health, platform registry, crawl start, case create/list/detail/run, Markdown export, visualization, summary, recommendation, analysis result, V1.5 topic-risk fields, and the Reddit mock adapter. The Vite Ant Design/ECharts vendor chunk warning remains non-blocking.

Important constraints:

- Do not enable real crawlers.
- Do not call real platform APIs.
- Do not call OpenAI or external LLM APIs.
- Use the offline mock pipeline only.
- Test on a desktop browser around 1440px width.

## 0. Pre-v1.0 Local Demo Data Tools

These helper scripts are safe local-development tools. They only operate inside the repository and do not call external APIs.

Dry-run local runtime data reset:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\reset_local_data.py
```

Actually reset local runtime JSON data:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\reset_local_data.py --yes
```

Expected result:

- Deletes only ignored runtime JSON files under `backend\data\*.json` and `backend\data\*.json.tmp`.
- Preserves `backend\data\.gitkeep`.
- Does not delete source files, docs, schemas, mock fixtures, or `.env`.

Seed deterministic demo cases:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\seed_demo_cases.py --reset-first
```

Expected result:

- Creates two deterministic demo cases.
- One case is completed with mock analysis, V1.5 topic risks, Chinese report, Markdown export data, snapshots, alerts, scheduler state, and local in-app notifications.
- One case remains a draft/demo watch case.

Run the local API smoke check after starting the backend:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\api_smoke_check.py --base-url http://127.0.0.1:8000
```

Expected result:

- Health, platforms, keyword/crawl/analysis, case run, Markdown export, monitoring, scheduler, alerts, notifications, and report endpoints pass.
- The script prints a clear pass/fail summary and exits nonzero on failure.

## 1. Start Backend

Open PowerShell or CMD:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
.venv\Scripts\activate
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Verify:

```text
http://127.0.0.1:8000/api/v1/health
```

Expected result:

```json
{
  "status": "ok",
  "mode": "development",
  "version": "0.1.0"
}
```

## 2. Start Frontend

Open another PowerShell or CMD:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

## 2.5 Create and Run an Analysis Case (v0.3)

Open Cases or Keyword Search.

From Keyword Search:

1. Enter an optional case title, for example `Tesla 舆情案例`.
2. Enter keyword `Tesla`.
3. Select mock-enabled platforms such as Reddit, Weibo, and Bilibili.
4. Click `Create Case & Run Mock Analysis`.

Expected result:

- A new local JSON-backed case is created through `POST /api/v1/cases`.
- The case is run through `POST /api/v1/cases/{case_id}/run`.
- The app returns to Dashboard with the selected case context in the top bar.
- Cases page shows the case title, keyword, platforms, risk score, risk level, updated time, and status.
- No real crawler, real platform API, or external LLM call is triggered.

## 3. Open Dashboard

Check that the first screen shows:

- Risk score
- Risk level
- Current risk model version, expected `v1_5_topic_risk_mvp`
- Top 3 high-risk topics
- Real crisis risk
- Manipulation/spread risk
- Latest public opinion summary
- Sentiment trend
- Risk radar
- Topic clusters
- Bot impact
- Platform heatmap or platform distribution

Expected result:

- Page is not blank.
- No Vite or React error overlay appears.
- Browser console has no relevant app errors.
- Charts render with mock backend data.

## 4. Select Platforms

Open Keyword Search.

Check platform groups:

- MVP mock-selectable platforms
- Official API planned platforms
- Future real adapter candidates
- Crawler-later platforms
- Disabled or optional future platforms

Expected result:

- Reddit, Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, and Toutiao are visible as mock-selectable.
- Crawler-later platforms are visible but disabled.
- YouTube is not active and is marked optional future if shown.

## 4.5 Optional Reddit Mock Adapter Smoke Check

This checks the backend adapter scaffold directly. It should stay offline and should not require Reddit credentials.

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\backend"
..\.venv\Scripts\python.exe -c "from app.services.crawling.adapter_factory import get_adapter; a=get_adapter('reddit'); posts=a.search_posts('Tesla', limit=2); comments=a.fetch_comments(posts[0].post_id, limit=2); print(a.health_check()); print(len(posts), len(comments), posts[0].platform, comments[0].platform)"
```

Expected result:

- Adapter mode is `mock`.
- Health check is OK.
- The command prints at least one normalized Reddit post/comment from local mock data.
- No real Reddit API call is made.

## 5. Run Mock Analysis

In Keyword Search:

1. Enter a keyword, for example `Tesla`.
2. Select one or more mock-selectable platforms.
3. Click `Create Case & Run Mock Analysis`.

Expected result:

- Keyword expansion runs.
- A lightweight local JSON-backed case is created.
- The existing offline V1.5 mock pipeline runs for that case.
- The case detail receives analysis data, visualization data, V1.5 topic risk fields, and a Chinese structured report.
- Dashboard data refreshes from the completed case context.
- No real platform API or crawler is triggered.

## 6. Open SummaryReport

Open Summary Report.

Check that the report displays:

- Risk score
- Risk level label
- Risk model version
- Top V1.5 risk topics
- Topic risk explanations
- Real crisis risk
- Manipulation/repeated-script risk
- Overall summary
- Key findings
- Main risk factors
- Top negative topics
- Representative comments
- Suspected bot/repeated-script signals
- Recommended actions
- Suggested public response

Expected result:

- Report language is `zh-CN`.
- Raw `risk_level` remains an English enum.
- `risk_level_label` displays Chinese labels such as `高风险`.
- `risk_model_version` displays `v1_5_topic_risk_mvp` for the current V1.5 mock pipeline.
- Representative comments stay in their original language.

## 7. Copy Suggested Response

In Summary Report:

1. Find the suggested public response section.
2. Click the copy button.

Expected result:

- A success message appears.
- Clipboard contains the suggested public response text.

## 7.5 Export Markdown Report

In Summary Report for a completed case:

1. Click `复制 Markdown` to copy the Markdown report.
2. Click `下载 .md` to download the Markdown report file.

Expected result:

- Markdown includes title, keyword, selected platforms, risk score, risk level, risk model version, overall summary, key findings, top risk topics, representative comments, suspected bot/repeated-script signals, recommended actions, and suggested public response.
- Export uses `GET /api/v1/cases/{case_id}/report/markdown`.
- Completed case data and generated Markdown metadata are persisted locally in `backend/data/cases.json` by default.
- To reset local demo cases safely, stop the backend and delete only `backend\data\cases.json`.

## 7.6 Persistence QA

After creating and running one case:

1. Confirm the local runtime store exists:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
dir backend\data
```

Expected result:

- `cases.json` exists after a case has been created or run.
- `backend/data/cases.json` is ignored by git and should not be committed.

2. Restart the backend server.
3. Open Cases again or call:

```cmd
powershell -Command "Invoke-RestMethod http://127.0.0.1:8000/api/v1/cases"
```

Expected result:

- Previously created local demo cases still appear.
- Completed cases still expose V1.5 topic risk, Chinese report data, and Markdown export.

Safe reset:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
del backend\data\cases.json
```

Only delete `backend\data\cases.json` when intentionally resetting local demo cases. Keep `backend\data\.gitkeep`.

## 8. Open RiskMonitor

Open Risk Monitor.

Check that the page shows:

- Monitoring status
- Risk trend
- `real_crisis_risk`
- `manipulation_risk`
- Top risk drivers
- Risk factor explanations
- Warning cards
- Trend shift indicator
- Propagation speed indicator
- Controversy indicator
- Current risk model version

Expected result:

- Empty arrays do not crash the page.
- Missing optional fields fall back gracefully.

## 8.5 Run Mock Monitoring Check

With a completed case selected:

1. Open Risk Monitor.
2. Click `Run Mock Monitoring Check`.
3. Confirm a new snapshot appears in the latest snapshot timeline.
4. Confirm the risk delta, latest risk level, top triggered reason, and alert list update.
5. Call the backend endpoints if needed:

```cmd
powershell -Command "Invoke-RestMethod http://127.0.0.1:8000/api/v1/cases/case_001/snapshots"
powershell -Command "Invoke-RestMethod -Method Post http://127.0.0.1:8000/api/v1/cases/case_001/monitor/run"
powershell -Command "Invoke-RestMethod http://127.0.0.1:8000/api/v1/cases/case_001/alerts"
```

Expected result:

- Each monitoring check creates a deterministic local snapshot in `backend/data/cases.json`.
- The first monitoring result can create a baseline event.
- Later monitoring checks may trigger warning/critical alert events when thresholds are crossed.
- Repeated checks should show growing snapshot history; the local QA smoke test created 3 snapshots, 5 alerts, and a `12.0` latest risk delta.
- No real scheduler, real crawler, real platform API, or notification service is used.

## 8.6 Enable Scheduled Monitoring Foundation

With a completed case selected:

1. Open Risk Monitor.
2. Find `监控配置`.
3. Click `启用监控`.
4. Confirm the status changes to `监控已到期` or `监控已启用`.
5. Click `运行到期监控任务`.
6. Confirm a new snapshot appears, alerts update if thresholds are crossed, and `下次检查` advances by the configured interval.
7. Click `暂停监控` if you want to stop future manual run-due checks for this case.

Backend smoke commands:

```cmd
powershell -Command "$case = Invoke-RestMethod -Method Post 'http://127.0.0.1:8000/api/v1/cases' -ContentType 'application/json' -Body '{\"keyword\":\"Tesla\",\"platforms\":[\"reddit\",\"weibo\"],\"title\":\"v0.8 Scheduler Demo\"}'; Invoke-RestMethod -Method Post \"http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/run\"; Invoke-RestMethod -Method Post \"http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/monitoring/enable\"; Invoke-RestMethod 'http://127.0.0.1:8000/api/v1/scheduler/status'; Invoke-RestMethod -Method Post 'http://127.0.0.1:8000/api/v1/scheduler/run-due'; Invoke-RestMethod \"http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/snapshots\""
```

Expected result:

- `GET /api/v1/scheduler/status` shows `background_scheduler_running=false`.
- Enabled due cases are listed in `job_states`.
- `POST /api/v1/scheduler/run-due` runs only due enabled cases.
- Disabled cases are not executed.
- Enabled but not-due cases are skipped and do not create extra snapshots.
- `last_run_at` and `next_run_at` are updated after a due run.
- No real background scheduler, crawler, platform API, external LLM, or notification delivery is started.

## 8.7 Verify Notification Outbox

With a completed case selected:

1. Open Risk Monitor.
2. Click `Run Mock Monitoring Check`, or enable monitoring and click `运行到期监控任务`.
3. Confirm alert events appear.
4. Confirm the `通知中心` card shows notification level, linked case id, message, read/unread state, and simulated send state.
5. Click `标记已读` on one notification.
6. Click `模拟发送` on one notification.
7. Click `模拟发送待处理通知` to update all pending local notifications.

Backend smoke commands:

```cmd
powershell -Command "$case = Invoke-RestMethod -Method Post 'http://127.0.0.1:8000/api/v1/cases' -ContentType 'application/json' -Body '{\"keyword\":\"Tesla\",\"platforms\":[\"reddit\",\"weibo\"],\"title\":\"v0.9 Notification Demo\"}'; Invoke-RestMethod -Method Post \"http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/run\"; Invoke-RestMethod -Method Post \"http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/monitor/run\"; Invoke-RestMethod \"http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/notifications\"; Invoke-RestMethod 'http://127.0.0.1:8000/api/v1/notifications/outbox/status'; Invoke-RestMethod -Method Post 'http://127.0.0.1:8000/api/v1/notifications/simulate-send-pending'"
```

Expected result:

- Monitor-generated alerts create local `in_app` notifications.
- `GET /api/v1/notifications/outbox/status` reports total, unread, pending, and simulated-sent counts.
- Simulated sends only update local JSON state.
- No real email, Slack, webhook, Enterprise WeChat, Feishu, SMS, push service, crawler, platform API, or external LLM is called.

## 9. Open PropagationGraph

Open Propagation Graph.

Check that the page shows:

- Graph nodes
- Graph edges
- Node platform/type/sentiment/influence details
- Graph metrics such as depth, breadth, central node, and propagation speed
- Useful small-graph guidance

Expected result:

- Small mock graph data remains readable.
- Empty graph data would show an empty state instead of a runtime error.

## 10. Browser QA Smoke Result

Latest v0.8 scheduler QA pass: 2026-05-14.

Validated by backend tests, frontend production build, source-level RiskMonitor review, and API smoke checks. The backend and frontend dev servers responded with HTTP 200 at `http://127.0.0.1:8000/api/v1/health` and `http://127.0.0.1:5173`, but the in-app Browser runtime timed out while opening the frontend. Before a public live demo, manually verify:

- Open a completed case.
- Open Risk Monitor.
- Click `启用监控`.
- Click `运行到期监控任务`.
- Confirm a new snapshot appears and `下次检查` advances.
- Click `暂停监控`.
- Run due jobs again and confirm the disabled case does not create another snapshot.

Latest v0.7 monitoring QA pass: 2026-05-14.

Validated by backend tests, frontend production build, source-level RiskMonitor review, and API smoke checks. The frontend dev server responded with HTTP 200 at `http://127.0.0.1:5173`, but in-app browser automation timed out during connection. Before a public live demo, manually verify:

- Open a completed case.
- Open Risk Monitor.
- Click `Run Mock Monitoring Check`.
- Confirm the snapshot timeline increases.
- Confirm risk delta, alert list, alert badges, real-crisis risk, manipulation risk, and top triggered reason are visible.

Previous local browser QA pass: 2026-05-14, final v0.3 case flow.

Validated with a 1440x960 desktop browser viewport through Chrome headless CDP fallback after the in-app Browser connection timed out:

- Dashboard renders V1.5 risk model, top-risk topics, real crisis risk, and manipulation risk.
- Keyword Search shows Reddit, Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, and Toutiao as mock-selectable choices.
- Crawler-later platforms are visible as future integration targets.
- YouTube remains disabled/optional future and is not active in the MVP selector.
- Running a mock analysis returns to Dashboard with refreshed V1.5 mock data.
- Cases page shows the completed case with title, keyword, selected platforms, risk score, risk level, updated time, and status.
- Summary Report can copy the suggested public response, copy the completed case as Markdown, and download a `.md` file.
- Suggested public response copy wrote 111 characters to the browser clipboard.
- Markdown copy wrote 1820 characters to the browser clipboard and included the case title plus `v1_5_topic_risk_mvp`.
- Analysis Result displays topic-risk score, risk explanation, and driver labels.
- Summary Report displays the Chinese structured report and the suggested public response copy button works.
- Risk Monitor displays real-crisis risk, manipulation/repeated-script risk, and top risk drivers.
- Propagation Graph displays graph metrics and an ECharts canvas.
- No relevant browser console errors were observed after adding the local favicon.
- API smoke checks passed for the new case endpoints and the existing platform, visualization, summary, recommendation, and analysis endpoints.

## 11. Final Local Validation Commands

Backend tests:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
.venv\Scripts\activate
python -m pytest
```

Frontend build:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"
npm run build
```

Expected result:

- Backend tests pass.
- Frontend build passes.
- Vite may still report a non-blocking large chunk warning for Ant Design and ECharts unless code splitting has been further optimized.
