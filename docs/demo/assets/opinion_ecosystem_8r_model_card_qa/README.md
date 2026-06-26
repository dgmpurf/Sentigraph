# Opinion Ecosystem 8R Model-card QA Screenshot Assets

This folder contains the Phase 8R model-card QA / screenshot smoke assets for the existing static/local Opinion Ecosystem explanatory UI.

Scope:

- QA/assets/report-only.
- Static/local explanatory UI only.
- No frontend product code changes.
- No backend code changes.
- No calculator API integration.
- No Strategy Lab runtime.
- No production runtime.
- No real API, real LLM, URL fetch, scraping, collector access, or Evidence Layer write.

Required route coverage:

- `http://127.0.0.1:5173/#/opinion-ecosystem`
- `http://127.0.0.1:5173/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`

Optional route smoke was also checked:

- `http://127.0.0.1:5173/#/public-events/helldivers-psn`
- `http://127.0.0.1:5173/#/public-events/donglu-sunjihai-youth-football`
- `http://127.0.0.1:5173/#/reports/helldivers-psn-sample`
- `http://127.0.0.1:5173/#/reports/donglu-sunjihai-youth-football-sample`

Screenshots:

- `01_opinion_ecosystem_default_explanation_top.png`
- `02_opinion_ecosystem_default_module_cards.png`
- `03_opinion_ecosystem_default_response_strategy_boundary.png`
- `04_dong_sun_query_explanation_top.png`
- `05_dong_sun_query_module_cards.png`
- `06_dong_sun_t0_t6_and_boundary_labels.png`

Result:

- Required route smoke passed.
- Optional broader route smoke passed.
- Model-card boundary QA passed.
- ResponseStrategyComparisonV01 remains human-review-only.
- No publish/send/post/execute CTA was found.
- No Sentigraph console error or warning was observed during browser smoke.

See `screenshot_capture_report.md` for the detailed QA record.

