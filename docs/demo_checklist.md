# Sentigraph Local Demo Checklist

Use this checklist for the current v0.6 case-based, mock-first desktop web MVP demo.

Latest v0.6 persistence validation: 2026-05-14. Backend tests passed with `55 passed in 0.51s`. Case API tests now verify create/list/detail/run, Chinese report attachment, Markdown export, and retrieval after reloading the repository/store from the same local JSON file. Frontend build was not rerun because no frontend files changed.

Latest v0.4 adapter-foundation validation: 2026-05-14. Backend tests passed with `47 passed in 0.42s`, frontend production build passed in 7.68s, and API smoke checks passed for health, platform registry, crawl start, case create/list/detail/run, Markdown export, visualization, summary, recommendation, analysis result, V1.5 topic-risk fields, and the Reddit mock adapter. The Vite Ant Design/ECharts vendor chunk warning remains non-blocking.

Important constraints:

- Do not enable real crawlers.
- Do not call real platform APIs.
- Do not call OpenAI or external LLM APIs.
- Use the offline mock pipeline only.
- Test on a desktop browser around 1440px width.

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
cd /d "G:\AICODING\Sentigraph 鑸嗘儏鍥捐氨绯荤粺\Sentigraph\backend"
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

Latest local browser QA pass: 2026-05-14, final v0.3 case flow.

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
