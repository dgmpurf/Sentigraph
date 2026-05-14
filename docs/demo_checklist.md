# Sentigraph Local Demo Checklist

Use this checklist for the current mock-first desktop web MVP demo.

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

## 5. Run Mock Analysis

In Keyword Search:

1. Enter a keyword, for example `Tesla`.
2. Select one or more mock-selectable platforms.
3. Click the analysis/start button.

Expected result:

- Keyword expansion runs.
- Mock crawl task runs.
- Mock analysis task runs.
- Dashboard data refreshes from backend mock APIs.
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

Latest local browser QA pass: 2026-05-14.

Validated with a 1440x900 desktop browser viewport:

- Dashboard renders V1.5 risk model, top-risk topics, real crisis risk, and manipulation risk.
- Keyword Search shows Reddit, Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, and Toutiao as mock-selectable choices.
- Crawler-later platforms are visible as future integration targets.
- YouTube remains disabled/optional future and is not active in the MVP selector.
- Running a mock analysis returns to Dashboard with refreshed V1.5 mock data.
- Analysis Result displays topic-risk score, risk explanation, and driver labels.
- Summary Report displays the Chinese structured report and the suggested public response copy button works.
- Risk Monitor displays real-crisis risk, manipulation/repeated-script risk, and top risk drivers.
- Propagation Graph displays graph metrics and an ECharts canvas.
- No relevant browser console errors were observed after adding the local favicon.

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
