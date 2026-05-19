# YouTube Real Data Demo

Last updated: 2026-05-19

This walkthrough shows how a tiny, quota-aware YouTube Data API v3 sample can flow through Sentigraph from official API crawl to case analysis, Chinese report, monitoring/forecasting, Simulation Lab initialization, A/B strategy rehearsal, and strategy report export.

This is a manual local demo path only. Automated tests and offline benchmarks must continue to use mocked YouTube clients and must not call the real YouTube API.

## Prerequisites

- Run from the repository root: `G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph`
- Backend dependencies are installed.
- Frontend dependencies are installed under `frontend/`.
- The local ignored `.env` file is configured for YouTube real mode:

```text
YOUTUBE_ADAPTER_MODE=real
YOUTUBE_API_KEY=<local key>
```

Do not commit, paste, echo, print, screenshot, or log the API key. The backend should expose only `credential_present=true/false` and never the key value.

Recommended guardrails in `.env.example`:

```text
YOUTUBE_CACHE_ENABLED=true
YOUTUBE_CACHE_TTL_SECONDS=3600
YOUTUBE_MAX_SEARCH_RESULTS=5
YOUTUBE_MAX_COMMENTS_PER_VIDEO=20
YOUTUBE_MAX_REPLIES_PER_COMMENT=5
YOUTUBE_MAX_TOTAL_COMMENTS=50
YOUTUBE_ENABLE_DEEP_REPLIES=false
```

## Validation Commands

These commands are local/offline validation. They should not call the real YouTube API.

```powershell
cd "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python -m pytest
python scripts/run_offline_benchmarks.py
npm --prefix frontend run build
```

## Start Servers

Start the backend:

```powershell
cd "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$env:CASE_STORE_BACKEND = "local_json"
$env:PUBLIC_PARSER_LIVE_FETCH_ENABLED = "false"
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Start the frontend in a separate PowerShell window:

```powershell
cd "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
npm --prefix frontend run dev
```

Open the Vite URL, usually `http://127.0.0.1:5173`.

## Verify YouTube Real Mode Is Configured

This command reads safe platform metadata only. It must not print `.env` values.

```powershell
$base = "http://127.0.0.1:8000/api/v1"
$status = Invoke-RestMethod -Uri "$base/platforms/status"
$status.platforms |
  Where-Object { $_.platform_id -eq "youtube" } |
  Select-Object platform_id, source_type, real_mode_available, selectable_for_real, credentials_present |
  ConvertTo-Json -Depth 6
```

Expected signs:

- `platform_id` is `youtube`.
- `source_type` is `youtube_data_api_v3`.
- `credentials_present.YOUTUBE_API_KEY` is `true` when local `.env` is configured.
- No API key value appears.

## Run Tiny YouTube Real Crawl

This manual command may call the official YouTube Data API v3 if real mode and the key are configured. Keep `limit=3` for demos.

```powershell
$base = "http://127.0.0.1:8000/api/v1"
$crawlBody = @{
  keyword = "Tesla"
  platforms = @("youtube")
  limit = 3
} | ConvertTo-Json

$crawl = Invoke-RestMethod `
  -Method Post `
  -Uri "$base/crawl/start" `
  -ContentType "application/json" `
  -Body $crawlBody

$crawl.platform_metadata[0] | ConvertTo-Json -Depth 8
```

Expected signs:

- `adapter_mode=real`
- `source_type=youtube_data_api_v3`
- `fallback_used=false`
- `credential_present=true`
- `post_count` and `comment_count` are tiny.
- `raw_post_schema_valid=true`
- `raw_comment_schema_valid=true`
- `cache_hit=false` on a fresh request or `cache_hit=true` on a repeat inside the TTL.

If YouTube quota/auth/network/comment availability fails, inspect `fallback_used`, `fallback_reason_category`, and `quota_guardrail_status`. The adapter should fall back safely without exposing credentials.

## Create Case And Attach YouTube Data

Case creation does not automatically call YouTube. The real crawl is explicit through the case-specific crawl endpoint.

```powershell
$base = "http://127.0.0.1:8000/api/v1"
$caseBody = @{
  title = "YouTube Real Data Demo Case"
  keyword = "Tesla"
  platforms = @("youtube")
  report_language = "zh-CN"
} | ConvertTo-Json

$case = Invoke-RestMethod `
  -Method Post `
  -Uri "$base/cases" `
  -ContentType "application/json" `
  -Body $caseBody

$attachBody = @{ limit = 3 } | ConvertTo-Json
$attached = Invoke-RestMethod `
  -Method Post `
  -Uri "$base/cases/$($case.case_id)/crawl/start" `
  -ContentType "application/json" `
  -Body $attachBody

$attached | Select-Object case_id, raw_data_status, crawl_source_mode, raw_post_count, raw_comment_count, crawl_attached_at | ConvertTo-Json -Depth 6
$attached.crawl_metadata[0] | ConvertTo-Json -Depth 8
```

Expected signs:

- `raw_data_status=attached` when posts or comments are stored.
- `crawl_source_mode=case_crawl_start`
- `raw_post_count` and/or `raw_comment_count` are nonzero when YouTube returns data.
- Crawl metadata contains booleans and counts only, never credentials.

## Run Case Analysis From Attached Raw Data

```powershell
$run = Invoke-RestMethod `
  -Method Post `
  -Uri "$base/cases/$($case.case_id)/run"

$run | Select-Object case_id, status, analysis_input_source, raw_post_count, raw_comment_count, risk_score, risk_level | ConvertTo-Json -Depth 6
$run.analysis_result.analysis_input_source
$run.report.representative_comments | Select-Object -First 3
```

Expected signs:

- `status=completed`
- `analysis_input_source=case_raw_data`
- `raw_comment_count` reflects attached YouTube comments when available.
- Representative comments can come from public YouTube comments.
- The run does not fall back to old mock comments when attached raw comments exist.

If no raw comments were attached, the case run should fall back safely with `analysis_input_source=mock_data_fallback`.

## View And Export Chinese Report

Frontend path:

1. Open `Cases`.
2. Open the YouTube case.
3. Open `Summary Report`.
4. Use `复制 Markdown` or the Markdown download action.

API check:

```powershell
$markdown = Invoke-RestMethod -Uri "$base/cases/$($case.case_id)/report/markdown"
$markdown.filename
$markdown.markdown.Substring(0, [Math]::Min(1000, $markdown.markdown.Length))
```

Expected signs:

- Markdown contains the case title, risk model version, high-risk topics, representative comments, and recommended response sections.
- It should not contain raw JSON dumps, API keys, `.env` values, or credentials.

## Risk Monitor And Forecast

```powershell
$monitor = Invoke-RestMethod -Method Post -Uri "$base/cases/$($case.case_id)/monitor/run"
$forecast = Invoke-RestMethod -Method Post -Uri "$base/cases/$($case.case_id)/forecast/run"

$monitor | Select-Object status, snapshot_count, latest_risk_level | ConvertTo-Json -Depth 6
$forecast | Select-Object forecast_status, snapshot_count, trend_direction, forecast_confidence, predicted_risk_score, predicted_risk_level | ConvertTo-Json -Depth 6
```

Frontend path:

1. Open `Risk Monitor`.
2. Select the YouTube-based case.
3. Run monitoring if needed.
4. Run risk forecast.

## Initialize Simulation Lab From The Case

```powershell
$preview = Invoke-RestMethod -Uri "$base/cases/$($case.case_id)/simulation/initialization-preview"
$init = Invoke-RestMethod -Method Post -Uri "$base/cases/$($case.case_id)/simulation/initialize"

$init | Select-Object case_id, status, model_version | ConvertTo-Json -Depth 6
$init.event_frame | Select-Object event_title, uncertainty_label | ConvertTo-Json -Depth 6
$init.frame_gap_analysis | Select-Object primary_classification, uncertainty_label | ConvertTo-Json -Depth 6
```

Expected signs:

- Initialization returns aggregate event-frame, audience-segment, persona-cluster, frame-gap, and synthetic scenario data.
- No named-user targeting, account-level influenceability scores, or automatic action execution appears.

Frontend path:

1. Open `Simulation Lab / 舆情预演沙盘`.
2. Use `从案例初始化沙盘`.
3. Select or enter the YouTube case id.
4. Preview initialization.
5. Initialize and load the scenario into the bubble view.

## Run Simulation And Export Strategy Report

Single-scenario API path:

```powershell
$scenario = $init.simulation_scenario
$simulationRun = Invoke-RestMethod `
  -Method Post `
  -Uri "$base/simulation/run" `
  -ContentType "application/json" `
  -Body ($scenario | ConvertTo-Json -Depth 40)

$strategyReportBody = @{
  simulation_mode = "single"
  scenario_name = $simulationRun.scenario_name
  intervention_a = $scenario.interventions[0].intervention_type
  run_result = $simulationRun
  generated_from = "youtube_real_data_demo_manual"
} | ConvertTo-Json -Depth 60

$strategyReport = Invoke-RestMethod `
  -Method Post `
  -Uri "$base/simulation/report/markdown" `
  -ContentType "application/json" `
  -Body $strategyReportBody

$strategyReport.markdown.Substring(0, [Math]::Min(1000, $strategyReport.markdown.Length))
```

Visual A/B frontend path:

1. Open `Simulation Lab / 舆情预演沙盘`.
2. Switch to `A/B 策略对比`.
3. Compare safe transparent options, for example `no_response` vs `clarification`, or `no_response` vs `content_removal_with_explanation` if allowed by the ethics policy.
4. Review the bubble panels, delta badges, visibility tradeoff panel, and human-review recommendation.
5. Click `导出策略预演报告`.
6. Click `复制 Markdown`.

The strategy report is deterministic, aggregate-level, and human-review-oriented. It must not recommend automatic real-world action execution.

## Benchmarks And LLM Safety

Frontend proof points:

1. Open `Benchmarks / 离线评测`.
2. Confirm the latest offline benchmark summary is available and has no failures.
3. Open `LLM Safety / 大模型安全状态`.
4. Confirm `MockProvider` is active and real LLM calls are disabled.
5. Open `Platform Integration Overview`.
6. Confirm YouTube is the only real-capable adapter when configured; other platforms remain mock/scaffold unless separately approved later.

## Cache Notes

- Cache file: `backend/data/youtube_cache.json`
- The cache file is ignored by git.
- Cache entries store normalized posts/comments plus safe metadata only.
- The API key is not stored in cache keys or cache payloads.
- Repeating the same tiny crawl within `YOUTUBE_CACHE_TTL_SECONDS` should show `cache_hit=true`.

To clear the cache manually, stop the backend and delete only the runtime cache file:

```powershell
Remove-Item -LiteralPath "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\backend\data\youtube_cache.json" -Force -ErrorAction SilentlyContinue
```

No cache status or cache clear API endpoint is currently required for the demo.

## Screenshot Checklist

Recommended screenshot sequence:

1. YouTube platform status showing credential presence as a boolean only.
2. Tiny `/crawl/start` metadata showing `adapter_mode=real`, `fallback_used=false`, schema-valid counts, and quota/cache metadata.
3. Case detail after `POST /cases/{case_id}/crawl/start`, showing `raw_data_status=attached`.
4. Case run result showing `analysis_input_source=case_raw_data`.
5. Analysis Result page with V1.5 topic risk.
6. Chinese Summary Report with representative comments.
7. Markdown report export preview.
8. Risk Monitor / Forecast.
9. Simulation Lab initialized from the YouTube case.
10. Simulation Lab single run.
11. Simulation Lab A/B strategy comparison.
12. Content visibility tradeoff panel if using a visibility intervention.
13. Simulation Lab strategy report export.
14. Benchmark Dashboard.
15. LLM Safety page.
16. Platform Integration Overview.

## Troubleshooting

- `adapter_mode=mock`: verify `.env` has `YOUTUBE_ADAPTER_MODE=real`, restart the backend, and do not print the key.
- `credential_present=false`: verify the local ignored `.env` contains `YOUTUBE_API_KEY=<local key>`, then restart the backend.
- `fallback_used=true`: inspect `fallback_reason_category` and `quota_guardrail_status`. Config, quota, auth, network, or comments-disabled cases should fail safely.
- `cache_hit=false` on first run: expected. Repeat the same tiny request within the TTL to test cache hit behavior.
- Mojibake in PowerShell output: prefer checking the frontend or a UTF-8-aware terminal before assuming backend decoding is wrong.
- `analysis_input_source=mock_data_fallback`: verify the case-specific crawl attach step produced nonempty `raw_comments` before running the case.
- Simulation initialization returns `case_analysis_required`: run `POST /api/v1/cases/{case_id}/run` first.

## Safety Boundary

- Use only official YouTube Data API v3.
- Do not scrape YouTube pages.
- Do not use browser cookies, login sessions, captcha bypass, anti-bot evasion, proxy rotation, OAuth-only private data, or private account data.
- Do not call real LLM APIs.
- Keep limits tiny and cache enabled.
- Keep real YouTube calls manual/local only.
- Keep outputs aggregate-level and human-review-oriented.
