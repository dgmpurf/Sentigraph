# Sentigraph v6.3 Demo Package

Status: screenshot/recording-ready local demo package.

This package explains how to present Sentigraph to collaborators, reviewers, or future users using the already working local demo path. The key framing is:

> Real: YouTube public video/comment data. Offline deterministic: analysis, V1.5 risk model, forecast, reports, and Simulation Lab. Mock: LLM provider. Scaffold/mock: other platform APIs.

The default demo can still run fully mock/offline. The optional YouTube real-data demo requires a local ignored `.env` key and must remain manual/local only.

## Product Summary

Sentigraph is a desktop public-opinion intelligence dashboard. It turns a keyword-driven case into normalized public data, deterministic offline analysis, V1.5 topic-risk scoring, Chinese reports, Markdown export, monitoring and forecasting, ethical Simulation Lab rehearsal, benchmark status, and LLM/platform safety diagnostics.

For v6.3, the demo can show an end-to-end YouTube public-data path:

1. Create or load a YouTube case.
2. Crawl a tiny YouTube sample through the official Data API when locally configured.
3. Attach public video/comment data to the case.
4. Run offline deterministic analysis from attached raw data.
5. View V1.5 topic risk and Chinese reports.
6. Initialize Simulation Lab from aggregate case analysis.
7. Compare transparent A/B response strategies.
8. Export a Simulation Lab strategy report.
9. Verify offline benchmarks, mock LLM status, and platform integration boundaries.

## Demo Story

The short story to tell:

"Sentigraph can ingest real public YouTube video/comment data when configured locally, but it keeps analysis offline and deterministic. Reports, forecasts, and Simulation Lab are review aids, not guaranteed predictions or automatic actions. The LLM layer is mock for this demo, and all other platform APIs remain mock or scaffold unless future official permissions are added."

Use `docs/demo_recording_script.md` for the 3-minute and 8-minute voiceover scripts.

## Screenshot List

Use `docs/demo_screenshot_checklist.md` as the canonical screenshot checklist.

Required sequence:

1. Dashboard showing YouTube real case.
2. Keyword Search with YouTube real-data flow.
3. Cases page showing completed YouTube case.
4. Analysis Result showing `analysis_input_source=case_raw_data`.
5. Summary Report showing YouTube-derived comments.
6. Propagation Graph showing YouTube nodes.
7. Risk Monitor / Forecast.
8. Simulation Lab initialized from case.
9. Simulation Lab A/B strategy comparison.
10. Strategy report export.
11. Benchmark Dashboard.
12. LLM Safety.
13. Platform Integration Overview.

Store local screenshots in an ignored folder such as `.benchmarks/demo_smoke_screenshots/`. Do not capture `.env`, API keys, private data, browser cookies, or raw credential settings.

## Local Run Commands

Run from the repository root.

Offline validation:

```cmd
python -m pytest
python scripts\run_offline_benchmarks.py
npm --prefix frontend run build
```

Default mock/offline demo prep:

```cmd
python scripts\reset_local_data.py --yes
python scripts\seed_demo_cases.py --reset-first
python scripts\run_offline_benchmarks.py
```

Start backend:

```cmd
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Start frontend in a second terminal:

```cmd
npm --prefix frontend run dev
```

Open:

```text
http://127.0.0.1:5173
```

Optional API smoke while backend is running:

```cmd
python scripts\api_smoke_check.py --base-url http://127.0.0.1:8000
```

## YouTube Real-Data Caveats

The optional YouTube demo requires a local ignored `.env` file:

```text
YOUTUBE_ADAPTER_MODE=real
YOUTUBE_API_KEY=<local key>
```

Rules:

- Never commit, print, paste, screenshot, or log the API key.
- Automated tests and offline benchmarks must not call the real YouTube API.
- Real YouTube calls are manual/local only.
- The adapter uses the official YouTube Data API v3 only.
- No scraping, browser cookies, login bypass, captcha bypass, anti-bot evasion, or private/OAuth-only data is used.
- Keep limits tiny and cache enabled.
- If the API key is missing or a quota/auth/network error occurs, the adapter falls back safely and reports sanitized metadata only.

See `docs/youtube_real_data_demo.md` for the exact manual PowerShell path.

## What Is Real vs Mock

| Area | v6.3 Demo Status |
| --- | --- |
| YouTube data | Real public video/comment data only when local `.env` is configured and the real-data flow is manually run. |
| Analysis pipeline | Offline deterministic analysis from attached case raw data, or mock-data fallback when no raw data is attached. |
| V1.5 topic risk | Offline deterministic. |
| Chinese report and Markdown export | Offline deterministic report builder. |
| Monitoring and forecast | Offline deterministic from local snapshots; not a guaranteed prediction. |
| Simulation Lab | Offline deterministic aggregate scenario rehearsal; no real-world action execution. |
| LLM provider | Mock. No real LLM calls. |
| Other platform APIs | Mock/scaffold unless future official permissioned integrations are implemented. |

## What Each Screen Proves

| Screen | What it proves |
| --- | --- |
| Dashboard | A completed case can be reviewed from a compact operations view with clear data/analysis/LLM status. |
| Keyword Search | YouTube real-data flow is explicit and separate from the default mock path. |
| Cases | Local case state persists and can show raw-data attachment context. |
| Analysis Result | `analysis_input_source=case_raw_data` proves attached raw data entered analysis. |
| Summary Report | YouTube-derived representative comments can appear in a Chinese analyst report and Markdown export. |
| Propagation Graph | Visualization remains connected for YouTube-based cases. |
| Risk Monitor / Forecast | Monitoring and trend signals work offline from local snapshots. |
| Simulation Lab | Aggregate scenario initialization and A/B comparison work from case analysis. |
| Strategy Report Export | Human-review-oriented Markdown strategy reports are available. |
| Benchmarks | Local regression checks run without credentials or external services. |
| LLM Safety | Real LLM calls are disabled and provider status is mock. |
| Platform Integration Overview | YouTube is the only current real-capable official adapter; other platforms remain mock/scaffold. |

## Current Limitations

- This is not a production release.
- Real YouTube mode requires local configuration and is manual-only.
- Other platform APIs are not real integrations yet.
- Real LLM calls are not integrated.
- Live public fetching and real crawlers remain disabled.
- Forecasts are deterministic review signals, not guaranteed predictions.
- Simulation Lab is deterministic and aggregate-level; it does not execute real-world actions, content moderation, or platform operations.
- Content visibility modeling is only a lawful/platform-authorized tradeoff simulation for human review.
- The system does not output individual targeting, account-level influenceability scoring, fake consensus, bot amplification, fake events, covert seeding, deceptive diversion, harassment, or suppression tactics.
- Vite may report a non-blocking large vendor chunk warning for Ant Design and ECharts.

## Safety and Ethics Boundaries

- No API keys or `.env` values should be printed or captured.
- No real LLM APIs are called.
- No scraping is implemented.
- No private data collection is implemented.
- No bypass of login, captcha, paywalls, cookies, or anti-bot systems is implemented.
- Real-world actions require external human, policy, and legal review.
- Simulation Lab output is aggregate scenario rehearsal and must not be treated as automatic strategy execution.
