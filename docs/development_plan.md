# Sentigraph Development Plan

## Core Principle

Do not build everything at once.

Build the system in small, testable MVP phases.

The first goal is not perfect analysis accuracy. The first goal is a running full-stack prototype:

```text
keyword input → mock analysis → dashboard visualization
```

## MVP 0: Repository Skeleton

Goal:

Create the project structure and make sure backend and frontend can run.

Tasks:

1. Create backend FastAPI project structure.
2. Create frontend React + Vite project structure.
3. Create docs and mock_data folders.
4. Add initial Pydantic schemas.
5. Add mock JSON data.
6. Add basic routes that return mock data.
7. Add README run instructions.

Do not implement:

- real crawlers
- real OpenAI calls
- real database logic
- complex ML models

## MVP 1: Mock Dashboard

Goal:

Build a visible demo dashboard using mock data.

Tasks:

1. Create Dashboard page.
2. Create KeywordSearch page.
3. Create AnalysisResult page.
4. Create PropagationGraph page.
5. Create RiskMonitor page.
6. Create SummaryReport page.
7. Add ECharts charts:
   - sentiment trend line
   - risk radar chart
   - topic cluster chart
   - bot impact chart
   - propagation network graph
   - platform heatmap
8. Connect frontend to backend mock APIs.
9. Add loading, error, and empty states.

Success criteria:

- User can input keyword.
- Backend returns mock data.
- Frontend displays charts.
- No React object rendering error.

## MVP 2: Preprocessing and Deduplication

Goal:

Implement text cleaning, normalization, user aggregation, and duplicate detection.

Tasks:

1. Implement `text_cleaner.py`.
2. Implement `language_detector.py`.
3. Implement `content_normalizer.py`.
4. Implement `duplicate_detector.py`.
5. Implement `user_aggregator.py`.
6. Preserve duplicate statistics.
7. Add tests.

Important:

Duplicate content should not be simply deleted. It should be grouped and counted.

## MVP 3: Sentiment and Topic Analysis

Goal:

Implement basic analysis services.

Tasks:

1. Implement `sentiment_analyzer.py`.
2. Implement `stance_analyzer.py`.
3. Implement `topic_clusterer.py`.
4. Implement `opinion_extractor.py`.
5. Implement `conflict_detector.py`.
6. Add strict JSON guard for LLM responses.
7. Add tests.

Start with mock mode first.

Then add optional LLM mode.

## MVP 4: Bot and Repeated-Script Detection

Goal:

Detect suspicious repeated scripts and possible bot-like behavior.

Tasks:

1. Implement `behavior_features.py`.
2. Implement `repeated_script_detector.py`.
3. Implement `account_pattern_detector.py`.
4. Implement `bot_score_service.py`.
5. Add bot impact chart data.
6. Add tests.

Rule-based detection is enough for the first version.

## MVP 5: Propagation Graph

Goal:

Build public opinion propagation graph.

Tasks:

1. Implement `propagation_builder.py`.
2. Implement `graph_metrics.py`.
3. Implement `depth_analyzer.py`.
4. Implement `influence_calculator.py`.
5. Add frontend graph visualization.
6. Add tests.

Use NetworkX on backend.

Use ECharts Graph on frontend.

## MVP 6: Risk Scoring and Recommendation

Goal:

Calculate risk score and generate response suggestions.

Tasks:

1. Implement `sentiment_score.py`.
2. Implement `bot_impact_score.py`.
3. Implement `controversy_score.py`.
4. Implement `trend_shift_detector.py`.
5. Implement `risk_score.py`.
6. Implement `recommendation_generator.py`.
7. Implement `crisis_strategy.py`.
8. Implement `response_template_generator.py`.
9. Add summary and recommendation frontend display.

Risk model versioning:

- Current active backend model: `v1_static_mvp`.
- Maintain `docs/algorithm_design.md` for the public opinion risk algorithm design.
- Maintain `docs/risk_model_roadmap.md` for V1/V2 migration planning.
- V2 topic-cluster dynamic risk is planned, but not implemented yet.
- Do not change active scoring behavior without an explicit migration task and tests.

## MVP 7: Platform Source Integration Roadmap

Goal:

Prepare official API integrations and future public-page parser work while keeping the MVP mock-first.

Tasks:

1. Maintain `docs/platform_sources.md`.
2. Maintain the backend platform registry exposed by `GET /api/v1/platforms`.
3. Keep active MVP platform choices limited to mock-capable sources.
4. Keep Reddit visible and mock-selectable as a future real adapter candidate.
5. Prioritize Chinese public opinion platforms for official API planning.
6. Plan official API integrations for Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, and Toutiao.
7. Plan crawler-later public-page parsers for Hupu, Baidu Tieba, Tianya, NGA, Maimai, The Paper / Pengpai News, and Jiemian News.
8. Keep YouTube disabled or optional future, not active in the MVP.

Do not implement:

- real third-party API calls
- real crawlers
- API key requirements
- login bypass
- captcha bypass
- private data scraping
- anti-bot evasion

Crawler maintenance note:

If a public webpage structure changes, an LLM may be used in a future phase to analyze sanitized public HTML fixtures and suggest selector updates. This must never be used to bypass login, captcha, paywalls, anti-bot systems, rate limits, or private data access.

## MVP 8: Incremental Monitoring and Alerts

Goal:

Add hourly monitoring and alerting.

Tasks:

1. Implement hourly incremental crawl.
2. Store last crawl cursor/time.
3. Compare new sentiment trend with previous trend.
4. Calculate slope and curvature shift.
5. Trigger alert when threshold is exceeded.
6. Add alert API.
7. Add alert frontend cards.
8. Add tests.

Alert logic:

```text
if trend_shift > threshold:
    create alert

if two consecutive shifts exceed threshold:
    escalate alert level
```

## MVP 9: Multi-Platform Adapters

Goal:

Add real platform adapters after the registry, compliance model, and mock pipeline are stable.

Suggested order:

1. Weibo
2. Bilibili
3. Douyin
4. Kuaishou
5. Xiaohongshu
6. Zhihu
7. Douban
8. Toutiao

Reddit remains a visible future real adapter candidate and can be reviewed in parallel after the shared adapter interface and compliance checklist are stable.

Each adapter must normalize output into the same RawPost and RawComment schema.

YouTube remains optional future and is not part of active MVP platform selection.

## Recommended First Codex Task

```text
Read AGENTS.md, README.md, and all files under docs/ first.

Create the initial Sentigraph repository skeleton.

Tasks:
1. Create backend FastAPI project structure under backend/app.
2. Create frontend React + Vite structure under frontend/src.
3. Add Pydantic schemas for keyword, crawl, comment, analysis, visualization, propagation, recommendation, and alert.
4. Add mock_data JSON files for raw_comments, cleaned_comments, analysis_result, visualization_response, and propagation_graph.
5. Add FastAPI routes:
   - POST /api/v1/keywords/expand
   - POST /api/v1/crawl/start
   - POST /api/v1/analysis/run
   - POST /api/v1/visualization/data
   - POST /api/v1/summary/generate
   - POST /api/v1/recommendation/generate
6. All routes can return mock data for now.
7. Create frontend pages:
   - Dashboard
   - KeywordSearch
   - AnalysisResult
   - PropagationGraph
   - RiskMonitor
   - SummaryReport
8. Connect frontend to mock backend APIs.
9. Use dark sci-fi dashboard style with Ant Design, ECharts, and Framer Motion.
10. Add README.md with run instructions.

Do not implement real crawlers yet.
Do not implement real OpenAI calls yet.
Focus only on project skeleton, mock data, API contract, and frontend-backend connection.
```

## Development Rules for Codex

1. Make small changes.
2. Run tests after backend changes.
3. Keep API schema stable.
4. Update docs if schema changes.
5. Never hardcode secrets.
6. Never implement login/captcha bypass.
7. Use mock mode if real services are unavailable.
8. Prefer readable modular code.
