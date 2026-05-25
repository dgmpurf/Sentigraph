# Sentigraph Local Demo Checklist

Evidence Review Queue browser-smoke QA result (2026-05-26): open `Cases`, select a case with normalized evidence, and use `Evidence Review / 证据复核` to show low-trust, unverified, screenshot/transcription, missing-source, missing-attestation, duplicate, secret-redacted, and HTML/script-like plain-text evidence. Expected success signs: queue count is nonzero; summary counts show review-needed, low-trust, duplicate groups, approved, rejected, marked weak, and needs more source where applicable; filters for `needs_review`, `low_trust`, `screenshot`, `missing_source`, `duplicates`, `rejected`, and `approved` work; actions `Approve / 通过`, `Reject / 驳回`, `Mark Weak / 标记为弱证据`, `Request Source / 要求补充来源`, `Merge Duplicate / 合并重复`, and `Reset / 重置复核状态` update the queue. Rejected evidence should remain stored but be excluded from default analysis and representative comments; marked-weak evidence remains usable with warnings; duplicate evidence stays collapsed. Analysis Result and Summary Report should warn about low-trust/unverified evidence and rejected-excluded evidence, should not call screenshots/transcriptions verified, should not imply AI verified authenticity, and should not render `[object Object]` or secret markers.

Evidence Review Queue MVP demo note (2026-05-25): in `Cases`, create or open a case with normalized evidence and add examples that should need review: screenshot/transcription evidence, evidence without a source URL, duplicated URL/text evidence, and user-uploaded/manual evidence without attestation. Open `Evidence Review / 证据复核`. Expected signs of success: queue count is nonzero, filters for `needs_review`, `low_trust`, `screenshot`, `missing_source`, `duplicates`, `rejected`, and `approved` work, and each row shows trust label, verification status, provenance type, source URL present/missing, duplicate indicator, risk flags, review status, and action buttons. Use `Approve`, `Reject`, `Mark Weak`, `Request Source`, `Merge Duplicate`, and `Reset` on sample items. Rejected evidence should remain stored but be excluded from default analysis and representative comments; duplicate evidence should stay collapsed; screenshots must not be labeled verified. Safety proof points: AI is not used for authenticity review, URLs are not fetched, no scraping/cookies/real APIs/real LLM APIs are triggered, and MediaCrawler remains not integrated.

Evidence trust/dedup browser-smoke QA result (2026-05-25): local browser smoke verified a case using `analysis_input_source=case_evidence_items` with manual URL evidence, a screenshot-transcription sample, raw HTML/script-like text treated as plain text, and duplicate URL/text evidence. Expected UI proof points: `Data: Evidence`, `Analysis: Offline`, `LLM: Mock`, `provenance_type`, `verification_status`, `trust_label`, `source_url_present`, `attestation_missing`, `review_needed`, readable review flags, and `duplicates collapsed`. Analysis Result should show the same evidence trust/provenance summary, and Summary Report should show `Normalized case evidence report`, a low-trust/unverified evidence warning, and a duplicate-collapse warning. Safety proof points: screenshots/transcriptions are never automatically verified, duplicate submissions do not inflate analysis counts directly, no URL fetching or scraping is triggered, no real APIs or real LLM APIs are called, no cookies or secrets are used, and MediaCrawler remains not integrated.

Evidence trust/dedup demo note (2026-05-25): in `Cases`, attach manual or uploaded evidence with and without the lawful-source attestation checkbox. Expected signs of success: evidence items show `provenance_type`, `verification_status`, `trust_label`, `review_needed`, source URL present/missing status, and duplicate indicators. Add the same URL/text twice to confirm `evidence_count` remains unique while `duplicate_count` / `duplicates collapsed` increases. Add a screenshot-transcription example to confirm it is `screenshot_unverified`; screenshots are never automatically verified. Add raw HTML/script-like text only as a plain text sample and confirm it is flagged, not executed. Summary Report should warn that user-uploaded/manual evidence requires source and human review when trust is low or unverified.

Evidence trust/dedup browser-smoke QA addendum (2026-05-25): create/open a case with no `raw_comments`, attach one manual URL evidence item with attestation, one screenshot/transcription-style item without source URL, and a duplicated URL/text item. Expected browser signs: `Data: Evidence`, `Analysis: Offline`, `LLM: Mock`, `analysis_input_source=case_evidence_items`, trust labels such as `medium` / `unverified`, verification statuses such as `source_url_provided_unverified` / `screenshot_unverified`, `source_url_present: x/y`, `attestation_missing`, `duplicates collapsed`, and readable review flags. Click `添加后运行分析`, then open Analysis Result and Summary Report. Summary Report should show `Normalized case evidence report`, the evidence credibility warning, duplicate-collapse warning, and representative comments from the evidence text. Confirm there is no `[object Object]`, no screenshot is called verified, and no URL fetching or scraping is triggered.

Search Discovery planning/status demo note (2026-05-25): open Platform Integration Overview and find `Search Discovery / URL Candidate Planning`. Expected signs of success: status is `planning_mock_only`, providers include search engine APIs, news discovery APIs, RSS, site-specific public search, user URL lists, data vendors, and mock fixtures; safety tags show no real search API, no URL fetch, and no scraping. This is a planning/status surface only. It does not discover real URLs, fetch pages, scrape websites, or attach candidates automatically. Use Manual URL Evidence or CSV/Excel import for user-reviewed evidence text.

Manual URL Evidence browser-smoke QA addendum (2026-05-25): for a clean demo, create or open a draft case with no attached `raw_comments`, click `打开` on the Cases table if needed, then add five manual evidence examples from `手动添加证据`: article, video, comment, reply, and `interaction_metric`. Expected success signs: the attached evidence preview stays readable, `evidence_items=5`, `acquisition_mode=manual_url`, source/type counts update, no `[object Object]` appears, and no pasted secret-like value is displayed. Click `添加后运行分析`; the Analysis Result should show `Data: Evidence`, `Analysis: Offline`, `LLM: Mock`, and `analysis_input_source=case_evidence_items`. Summary Report and copied Markdown should use the manual evidence text and describe the generation mode as normalized case evidence, not mock fallback or attached raw data. Simulation Lab should initialize from the completed manual-evidence case. Safety proof points for screenshots: no automatic URL fetch, no scraping, no cookies, no credential storage, no real platform API, no real LLM API, and MediaCrawler remains not integrated.

Latest Manual URL Evidence UI: 2026-05-25. In `Cases`, open or create a case with no attached raw comments, use `手动添加证据`, paste a lawful public URL as review context, choose `证据类型` such as `article`, `video`, `comment`, `reply`, or `interaction_metric`, and manually enter at least one of `标题`, `正文 / 摘要`, or `评论内容`. Click `添加到案例`, confirm `evidence_count`, source/type distribution, `acquisition_mode=manual_url`, and the latest evidence preview, then click `添加后运行分析`. Expected signs of success: `analysis_input_source=case_evidence_items`, Summary Report uses the manually entered evidence text, Risk Monitor / Forecast and Simulation Lab can use the completed case, invalid numeric metrics produce warnings instead of crashes, and any pasted secret-like text is redacted. Safety proof points: the UI explains that it does not auto-fetch URL content, does not save credentials/Cookie/key material, and requires the user to ensure the source is lawful; backend tests confirm no URL fetching, no real API calls, no scraping, no real LLM calls, and no MediaCrawler integration.

Latest CSV / Excel Evidence Import browser smoke: 2026-05-25. In `Cases`, open or create a case, use `导入证据数据`, click `下载 CSV 模板`, fill or reuse the safe sample rows, upload the CSV/XLSX file, confirm `字段映射`, click `预览导入结果`, review warnings/duplicates, click `确认导入`, then click `导入后运行分析` or use `Refresh` to rerun the current case. Expected signs of success: the template downloads as `sentigraph_evidence_import_template.csv`, preview parses the template rows, `source_type=uploaded_dataset` or the expected source distribution appears, `acquisition_mode=user_upload`, evidence type counts appear, `evidence_item_count > 0`, `analysis_input_source=case_evidence_items` when no raw comments are attached, and uploaded-file text appears as representative evidence in Cases / Analysis Result / Summary Report. Screenshot targets: the import panel with `导入证据数据` and `下载 CSV 模板`, the preview table with row warnings, the commit result with source/type counts, and the current-case evidence summary showing `Data: Evidence`, `Analysis: Offline`, `LLM: Mock`, `analysis_input_source=case_evidence_items`, and representative imported comments. Safety proof points: formulas are not executed, raw uploaded files are not persisted by default, secret-like fields are redacted or omitted, no crawler starts, no real platform API or real LLM API is called, MediaCrawler is not integrated, and YouTube raw case data still wins when `raw_comments` exist.

CSV / Excel import smoke notes: source mode labels must distinguish uploaded evidence from YouTube real raw data. A case with imported `case_evidence_items` should show `Data: Evidence`; only a YouTube case using attached raw comments should show `Data: YouTube Real`. Evidence-backed propagation graphs should render without ECharts duplicate-node console errors.

Latest Source Catalog / Evidence browser smoke: 2026-05-25. The local UI now has a demo-ready Source Catalog section inside Platform Integration Overview and a compact Evidence summary on case/report pages. Browser smoke verified Dashboard, Platform Integration Overview, Cases, Summary Report, Analysis Result, Risk Monitor, Simulation Lab, Benchmark Dashboard, and LLM Safety with a manually attached evidence case. Expected proof points: Source Catalog shows `12 categories`, `22 sources`, static metadata/no-real-API boundaries, YouTube green/real-capable, Douyin OAuth + `item.comment` pending, Bilibili official-permission pending, Xiaohongshu comment API unknown, Weibo company-age pending, and MediaCrawler not integrated. Evidence proof points: attached article/body evidence, video metadata, comment, reply, and `interaction_metric` records show source distribution, evidence type counts, acquisition mode labels, top titles, representative comments, `analysis_input_source=case_evidence_items`, no raw secrets, and no `[object Object]` rendering.

Latest v6.3 Demo Package Final: 2026-05-20. The final external-presentation package is documented in `docs/demo_package.md`, `docs/demo_recording_script.md`, and `docs/demo_screenshot_checklist.md`. The canonical capture plan now has 14 screens: Dashboard, Keyword Search, Cases, Analysis Result, Summary Report, Propagation Graph, Risk Monitor / Forecast, Simulation Lab initialized from case, Simulation Lab A/B strategy comparison, strategy report export, Benchmark Dashboard, LLM Safety, Platform Integration Overview, and Douyin readiness / platform status if visible. The story must clearly distinguish real YouTube public video/comment data, offline deterministic analysis/risk/report/forecast/Simulation Lab, mock LLM provider, mock/scaffold/pending status for other platforms, and Douyin Web App OAuth / `item.comment` pending status. Do not capture `.env`, API keys, terminal secrets, private data, or any UI implying all platforms are real, real LLM integration is enabled, predictions are guaranteed, Simulation Lab executes real-world actions, content moderation is automatic, individual targeting is supported, or Douyin real API integration is complete.

Latest final YouTube real-data demo UI polish: 2026-05-19. The screenshot target is now uniform across the header and YouTube-only Keyword Search flow: real-data cases should show `Data: YouTube Real`, `Analysis: Offline`, and `LLM: Mock`; mock fallback cases should show `Data: Mock`, `Analysis: Offline`, and `LLM: Mock`. The Summary Report body now distinguishes attached raw-data reports from mock fallback reports, and the sidebar uses the shorter `Simulation / 沙盘` label with a full `Simulation Lab / 舆情预演沙盘` tooltip to avoid awkward truncation in recordings. Data source and analysis mode are separate: YouTube public video/comment data can be real while analysis, reports, forecasts, Simulation Lab, and LLM remain offline/mock. Douyin remains OAuth/scope-pending and is not part of this YouTube real-data demo; real Douyin API calls remain disabled. Frontend validation passed with `npm run build` from `frontend/` (`built in 7.81s`, existing large vendor chunk warning remains). Backend tests and offline benchmarks were not rerun because this pass changed frontend/docs only. Automated validation did not call the real YouTube API, call the real Douyin API, print API keys or `.env` values, scrape, recreate GitHub Actions CI, or call real LLM APIs.

Latest v6.3 screenshot/recording demo package: 2026-05-19. The final presentation package lives in `docs/demo_package.md`, with a dedicated voiceover/page-order script in `docs/demo_recording_script.md` and a capture list now superseded by the 2026-05-20 canonical 14-screen checklist in `docs/demo_screenshot_checklist.md`. The screenshot story should explicitly show `Data: YouTube Real / Analysis: Offline / LLM: Mock` for the optional YouTube real-data case, while keeping the default mock/offline demo available. The updated required capture sequence is Dashboard, Keyword Search, Cases, Analysis Result, Summary Report, Propagation Graph, Risk Monitor / Forecast, Simulation Lab initialized from case, Simulation Lab A/B comparison, strategy report export, Benchmark Dashboard, LLM Safety, Platform Integration Overview, and Douyin readiness / platform status if visible. Validation passed with `python -m pytest` (`544 passed in 6.00s`), `python scripts/run_offline_benchmarks.py` (`522 passed, 0 failed, 0 warnings`, `no_regression`), and `npm --prefix frontend run build` (`built in 8.05s`, existing large vendor chunk warning remains). Do not capture `.env`, API keys, terminal secrets, private data, or any UI implying guaranteed prediction, automatic real-world action execution, automatic content moderation, individual targeting, or completed Douyin real API integration.

Latest v6.2 YouTube real-data demo polish QA: 2026-05-19. Rechecked the final screenshot-ready wording and provenance labels. The app header, Analysis Result, Summary Report, Cases, and Demo Flow surfaces distinguish `Data: YouTube Real`, `Analysis: Offline`, and `LLM: Mock` for YouTube raw-data cases, while mock fallback cases use `Data: Mock`, `Analysis: Offline`, and `LLM: Mock`. Keyword Search still keeps the default mock flow, shows the explicit YouTube real-data crawl/attach/run flow only when YouTube is selected by itself, and shows `For YouTube real-data demo, select YouTube only.` for mixed selections. Representative-comment regression coverage confirms raw YouTube comments remain stored while promo/self-promo comments containing `patreon`, `channel member`, `subscribe`, `referral`, `promo code`, `affiliate`, `join`, `merch`, or `discount code` are down-ranked when substantive alternatives exist. Validation passed with `npm --prefix frontend run build` (`built in 8.08s`, existing large vendor chunk warning remains), `python -m pytest` (`544 passed in 5.99s`), and `python scripts/run_offline_benchmarks.py` (`522 passed, 0 failed, 0 warnings`, `no_regression`). Automated validation did not call the real YouTube API, print API keys, modify `.env`, scrape, recreate GitHub Actions CI, or call real LLM APIs.

Latest final YouTube real-data demo polish validation: 2026-05-19. The app header now uses the same three-badge vocabulary for both real-data and mock cases: YouTube cases with `analysis_input_source=case_raw_data` show `Data: YouTube Real`, `Analysis: Offline`, and `LLM: Mock`; mock-fallback cases show `Data: Mock`, `Analysis: Offline`, and `LLM: Mock`. Cases and Dashboard screens now surface the current case data source more clearly, Markdown exports identify attached case raw data as offline deterministic analysis with no real LLM call, and the Keyword Search mixed-platform warning now reads `For YouTube real-data demo, select YouTube only.` Representative-comment selection still keeps all raw YouTube comments but now also down-ranks `merch` and `discount code` promo/self-promo comments when substantive topic comments exist. Validation passed with `python -m pytest` (`544 passed in 6.40s`), `python scripts/run_offline_benchmarks.py` (`522 passed, 0 failed, 0 warnings`, `no_regression`), and `npm --prefix frontend run build` (`built in 8.57s`, existing large vendor chunk warning remains). Automated validation did not call the real YouTube API, print API keys, modify `.env`, scrape, recreate GitHub Actions CI, or call real LLM APIs.

Latest Keyword Search YouTube real-data frontend QA stabilization: 2026-05-19. The Keyword Search page now keeps the default `Create Case & Run Mock Analysis` path intact and exposes the explicit real-data flow only for YouTube-only selection: `Create YouTube Real Case`, `Crawl YouTube & Attach Raw Data`, and `Run Case Analysis`. After analysis, the page stays on Keyword Search long enough to verify `analysis_input_source=case_raw_data`, raw counts, and YouTube-derived representative comments before using shortcut buttons to open Analysis Result, Summary Report, Risk Monitor, or Simulation Lab. Mixed YouTube plus other-platform selections show `For YouTube real-data demo, select YouTube only.` Frontend validation passed with `npm --prefix frontend run build` (`built in 7.81s`, existing large vendor chunk warning remains). Backend tests and offline benchmarks were not rerun because no backend code changed; automated validation did not call the real YouTube API, print API keys, modify `.env`, scrape, or call real LLM APIs.

Latest YouTube real-data demo UX polish validation: 2026-05-19. The frontend now separates data provenance from execution mode for real-data cases: completed YouTube cases with `analysis_input_source=case_raw_data` show `Data: YouTube Real`, `Analysis: Offline`, `LLM: Mock`, and the raw `analysis_input_source` on the app header, Analysis Result, Summary Report, and Demo Flow surfaces. The Simulation Lab sidebar item is shortened to `Simulation Lab` with a tooltip for `Simulation Lab / 舆情预演沙盘`, reducing awkward truncation in screenshots. Backend report selection keeps all attached raw YouTube comments but down-ranks obvious channel promotion/self-promo comments such as `patreon`, `channel member`, `subscribe`, `referral`, `promo code`, `affiliate`, and `join` when substantive event-relevant alternatives exist. Validation passed with `python -m pytest` (`544 passed in 5.95s`), `python scripts/run_offline_benchmarks.py` (`522 passed, 0 failed, 0 warnings`, `no_regression`), and `npm --prefix frontend run build` (`built in 8.11s`, existing large vendor chunk warning remains). Automated validation did not call the real YouTube API, print API keys, modify `.env`, scrape, or call real LLM APIs.

Latest YouTube real-data browser-smoke documentation QA: 2026-05-19. Rechecked `docs/youtube_real_data_demo.md`, `docs/demo_story.md`, and this checklist against the manual real-data browser-smoke path: start backend, start frontend, run a tiny `platforms=["youtube"]` crawl, confirm `adapter_mode=real`, confirm cache behavior, attach/store YouTube `raw_posts` / `raw_comments` to a case, run case analysis with `analysis_input_source=case_raw_data`, confirm YouTube-derived representative comments, view Chinese Summary Report, export Markdown, open Risk Monitor/Forecast, initialize Simulation Lab, run A/B strategy comparison, export the Simulation Lab strategy report, and open Benchmark Dashboard plus LLM Safety. The concise demo story now explicitly calls out repeating the same tiny crawl inside the cache TTL to verify `cache_hit=true`. Validation passed with `python -m pytest` (`542 passed in 5.18s`), `python scripts/run_offline_benchmarks.py` (`522 passed, 0 failed, 0 warnings`, `no_regression`), and `npm run build` from `frontend/` (`built in 7.59s`, existing large vendor chunk warning remains). Automated validation did not call the real YouTube API, print API keys, scrape, modify `.env`, or call real LLM APIs.

Latest YouTube Real Data Demo Story validation: 2026-05-19. Added `docs/youtube_real_data_demo.md` as the dedicated manual walkthrough for the optional YouTube real-data path. The documented flow starts backend/frontend, verifies safe YouTube real-mode metadata, runs a tiny `Tesla` crawl, attaches the crawl to a case through `POST /api/v1/cases/{case_id}/crawl/start`, runs case analysis with `analysis_input_source=case_raw_data`, checks YouTube-derived representative comments, opens V1.5 topic risk and Chinese Summary Report, exports Markdown, opens Risk Monitor/Forecast, initializes Simulation Lab, runs A/B comparison, exports the strategy report, and finishes with Benchmark Dashboard plus LLM Safety. Expected signs of success remain `adapter_mode=real`, `fallback_used=false`, `credential_present=true`, schema-valid tiny counts, `raw_data_status=attached`, `analysis_input_source=case_raw_data`, and no API-key values in output. Validation passed with `python -m pytest` (`542 passed in 6.32s`), `python scripts/run_offline_benchmarks.py` (`522 passed, 0 failed, 0 warnings`, `no_regression`), and `npm --prefix frontend run build` (`built in 8.26s`, existing large vendor chunk warning remains). Automated validation did not call the real YouTube API.

Latest YouTube cache/guardrail QA validation: 2026-05-18. Cache and quota guardrails were revalidated with mocked YouTube clients only. Focused QA confirmed cache miss/hit/TTL expiry behavior, cache-hit call avoidance, limit clamping, disabled deep replies by default, total-comment caps, comments-disabled partial output, quota-error fallback, API-key redaction, and case raw-data ingestion compatibility. Full validation passed with `python -m pytest` (`542 passed in 5.14s`) and `python scripts/run_offline_benchmarks.py` (`522 passed, 0 failed, 0 warnings`, `no_regression`). Frontend build was not run because no frontend files changed. The manual cache demo remains: run the same tiny YouTube real-mode crawl twice, inspect `platform_metadata[0].cache_hit`, and clear only `backend/data/youtube_cache.json` if a fresh manual crawl is needed.

Latest YouTube Real Data Full Demo QA validation: 2026-05-18. The manual real-data path is now documented end to end: start the backend with a local ignored YouTube key, create a YouTube case, explicitly attach tiny-limit crawl output through `POST /api/v1/cases/{case_id}/crawl/start`, run the case, verify `analysis_result.analysis_input_source=case_raw_data`, view/copy the Markdown report, run monitoring/forecast, initialize Simulation Lab, run deterministic A/B simulation, and export the Simulation Lab strategy report. Automated QA added mocked-real fallback checks for comments-disabled/quota/auth-style failures and network failures; tests never call the real YouTube API. Validation passed with `python -m pytest` (`533 passed in 5.30s`), `python scripts/run_offline_benchmarks.py` (`522 passed, 0 failed, 0 warnings`, `no_regression`), and `npm run build` from `frontend/` (`built in 7.66s`, existing large vendor chunk warning remains).

Latest Case Raw Data Ingestion QA validation: 2026-05-18. `POST /api/v1/cases/{case_id}/crawl/start` can explicitly attach normalized YouTube/future adapter `RawPost` / `RawComment` output to a case. The next `POST /api/v1/cases/{case_id}/run` uses attached raw comments with `analysis_input_source=case_raw_data`; without attached raw comments it falls back to the deterministic mock dataset. QA coverage verifies local JSON reload persistence, MongoDB-shaped persistence through the fake store, YouTube-derived representative comments in Markdown, old mock comments not appearing when raw case comments exist, and no raw-data JSON dump in the user-facing Markdown report. Backend tests passed with `python -m pytest` (`531 passed in 5.22s`) and offline benchmarks passed with `python scripts/run_offline_benchmarks.py` (`522 passed, 0 failed, 0 warnings`, `no_regression`). Frontend build was not run because no frontend files changed. Automated tests use mocked crawl output only and do not call the real YouTube API.

Latest browser smoke and demo story validation: 2026-05-18. Local validation passed with `npm run build` from `frontend` (`built in 8.17s`, existing non-blocking Ant Design/ECharts large vendor chunk warning remains), `python -m pytest` (`511 passed in 5.19s`), and `python scripts/run_offline_benchmarks.py` (`522 passed, 0 failed, 0 warnings`, `no_regression`). `python scripts/api_smoke_check.py --base-url http://127.0.0.1:8000` passed against the local backend (`38 passed, 0 failed`). Browser smoke used an already-running backend on `127.0.0.1:8000` and a clean Vite dev server on an alternate local port because `5173` was occupied by a stale local process. Smoked pages: Demo Flow, Dashboard, Cases, Analysis Result, Summary Report, Risk Monitor, Simulation Lab, Benchmarks, LLM Safety, Platform Integration Overview, Public Parser Status, and Selector Repair Tool. Simulation Lab case initialization, single-scenario run, A/B comparison, content visibility tradeoff panel, strategy report export, and allowed-intervention dropdown were verified. No raw `[object Object]` rendering was observed. Forbidden Simulation Lab tactics were not selectable. A small Ant Design `rowKey` warning on the LLM Safety usage table was fixed. Screenshot/demo story documentation now lives in `docs/demo_story.md`; local smoke screenshots were captured under `.benchmarks/demo_smoke_screenshots/`.

Latest v5.4 demo polish validation: 2026-05-18. Added the `Demo Flow / 演示流程` page for one-page local walkthroughs, extended deterministic demo seeding with forecast and case-to-simulation readiness fields, and extended the local API smoke script to cover forecast plus Simulation Lab demo/run/report export. Backend tests passed with `python -m pytest` (`511 passed in 4.88s`), offline benchmarks passed with `python scripts/run_offline_benchmarks.py` (`522 passed, 0 failed, 0 warnings`; `no_regression`), frontend production build passed with `npm run build` from `frontend` in 8.06s with the existing non-blocking Ant Design/ECharts vendor chunk warning, and local API smoke passed against a temporary backend on port 8010 (`38 passed, 0 failed`). No real APIs, real LLM APIs, live public fetching, real crawlers, real notifications, or manipulation tactics were enabled.

Latest Simulation Lab content visibility intervention QA stabilization: 2026-05-18. Backend tests passed with `python -m pytest` (`488 passed in 4.17s`), offline benchmarks passed with `python scripts/run_offline_benchmarks.py` (`483 passed, 0 failed, 0 warnings`; `simulation_lab: 36 cases`), and frontend production build passed with `npm run build` from `frontend` in 7.90s with the existing non-blocking Ant Design/ECharts vendor chunk warning. Browser smoke against local backend/frontend verified the A/B default `no_response` vs `透明说明后内容移除` flow, the `内容可见性干预` panel labels, human-review copy, no real API/LLM copy, no automatic platform-action execution, and no forbidden tactic values in selectable options. Additional backend coverage now locks down reach sensitivity, reactance sensitivity, score clamping, required aggregate groups, API visibility-result shape, aggregate-only output, and target-list absence.

Latest Simulation Lab content visibility intervention validation: 2026-05-18. Backend tests passed with `python -m pytest` (`482 passed in 4.47s`), offline benchmarks passed with `python scripts/run_offline_benchmarks.py` (`483 passed, 0 failed, 0 warnings`), and frontend production build passed with `npm run build` from `frontend` in 7.67s with the existing non-blocking Ant Design/ECharts vendor chunk warning. Browser smoke against local backend/frontend verified the A/B default `no_response` vs `透明说明后内容移除` flow, the `内容可见性干预` panel labels, and that forbidden tactic values do not appear in selectable options. The Simulation Lab A/B UI now supports safe visibility tradeoff display for `content_removal_with_explanation`, `visibility_reduction`, and `platform_labeling` when exposed by the backend ethics policy; forbidden manipulation and illegal/covert suppression options remain unavailable.

Use this checklist for the current v0.9 case-based, mock-first desktop web MVP demo.

## 0.0 v5.4 One-Click Demo Flow

Use this path when you want a clean end-to-end local demo without jumping manually across many pages first.

1. Reset local runtime data:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\reset_local_data.py --yes
```

2. Seed deterministic demo cases:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\seed_demo_cases.py --reset-first
```

Expected seed output:

- `completed_case_id` is a Tesla demo case using `reddit`, `weibo`, and `bilibili`.
- `forecast_status` is `ready`.
- `simulation_initialization_status` is `initialized`.
- `snapshot_count`, `alert_count`, and `notification_count` are nonzero.
- `mock_only` is `true`.

3. Run offline benchmarks so the Benchmark Dashboard has a fresh result:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\run_offline_benchmarks.py
```

4. Start the backend:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set CASE_STORE_BACKEND=local_json
set PUBLIC_PARSER_LIVE_FETCH_ENABLED=false
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

5. Start the frontend:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"
npm run dev
```

6. Optional smoke check after the backend is running:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\api_smoke_check.py --base-url http://127.0.0.1:8000
```

7. Open `http://127.0.0.1:5173` and click `Demo Flow / 演示流程`.
8. Click `一键准备演示数据` if the Tesla demo case is not already selected.
9. Walk through the cards in order:
   - `创建/加载演示案例`
   - `运行 mock 分析`
   - `查看风险结果`
   - `查看中文报告并导出 Markdown`
   - `初始化沙盘`
   - `A/B 策略对比`
   - `导出策略预演报告`
   - `查看离线评测与安全状态`
10. Confirm the page-level safety note says the demo uses mock/offline data and does not call real platform APIs or real LLM APIs.

Latest Simulation Lab frontend QA stabilization validation: 2026-05-18. Frontend production build passed with `npm run build` from `frontend` in 7.90s with the existing non-blocking Ant Design/ECharts vendor chunk warning. Browser smoke against local `http://127.0.0.1:8000` and `http://127.0.0.1:5173` confirmed the `Simulation Lab / 舆情预演沙盘` route, sidebar navigation, left/center/right/bottom layout, event cards, bubble canvas, aggregate metrics, explanation cards, timeline, `运行模拟`, and `单步推进` flow. Backend tests and offline benchmarks were not rerun because no backend algorithm or benchmark logic changed. No real API, real LLM API, crawler, live public fetch, individual targeting, account-level influenceability scoring, or forbidden manipulation tactic was enabled.

Latest v4.2 benchmark history QA stabilization validation: 2026-05-17. Focused benchmark route/runner tests passed with `14 passed in 0.77s`; full backend tests passed with `423 passed in 3.40s`; offline benchmarks passed with `78 passed, 0 failed, 0 warnings`; frontend production build passed in 7.43s with the existing non-blocking Ant Design/ECharts vendor chunk warning. The `Benchmarks / 离线评测` page now displays latest results, history rows, and regression status with clean Chinese labels. No real LLM API, real platform API, crawler, live public fetch, real notification, API key printing, `.env` value printing, raw prompt logging, or raw user-content logging was introduced.

Latest v3.9 QA stabilization validation: 2026-05-17. Backend tests passed with `409 passed in 3.73s`. Frontend production build passed in 7.84s with the existing non-blocking Ant Design/ECharts vendor chunk warning. The `LLM Safety` / `大模型安全状态` page is read-only and displays MockProvider/default status, disabled real-call status, API key presence booleans only, guardrail limits, and metadata-only usage summaries. Local smoke tooling includes LLM status/usage and public parser preview checks, and demo seeding creates a Hupu fixture-parser demo case. No real LLM API, real platform API, real crawler, live public fetch, real notification, authentication, `.env` modification, API key printing, raw prompt logging, or raw user-content logging is introduced.

Latest pre-v1.0 hardening validation: 2026-05-15. Backend tests passed with `92 passed in 2.82s`. Frontend production build passed in 7.75s with the existing non-blocking Ant Design/ECharts vendor chunk warning. API smoke check passed with `26 passed, 0 failed` against a temporary local backend and temporary project-local JSON store. New local demo utilities are available for safe runtime data reset, deterministic demo seeding, and local API smoke validation. No real email, Slack, webhook, Enterprise WeChat, Feishu, SMS, push, crawler, platform API, Reddit credential, MongoDB, Redis, or external LLM call is made.

Latest optional MongoDB persistence QA validation: 2026-05-15. Focused persistence and case API tests passed with `20 passed in 1.11s`; full backend validation passed with `179 passed in 3.35s`. The default backend remains `CASE_STORE_BACKEND=local_json`; MongoDB is used only when `CASE_STORE_BACKEND=mongodb` is explicitly configured. Fake-backed tests verify MongoDB store selection, unknown-backend errors, safe connection failure errors, index creation, case/report/Markdown/snapshot/alert/notification persistence, reset behavior, and MongoDB-safe document keys without requiring a real MongoDB server.

Latest v0.9 notification QA validation: 2026-05-14. Backend tests passed with `90 passed in 2.34s`. Frontend production build passed in 7.61s with the existing non-blocking Ant Design/ECharts vendor chunk warning. Isolated API smoke checks confirmed alert events create local `in_app` notification outbox items, notifications can be listed by case or globally, `标记已读` sets `read_at`, `模拟发送` sets `simulated_sent_at`, and `模拟发送待处理通知` updates all pending local notifications. No real email, Slack, webhook, Enterprise WeChat, Feishu, SMS, push, crawler, platform API, or external LLM call is made.

Latest v0.8 scheduler QA validation: 2026-05-14. Backend tests passed with `81 passed in 1.76s`. Frontend production build passed in 7.46s with the existing non-blocking Ant Design/ECharts vendor chunk warning. API smoke checks confirmed enabling monitoring, `GET /api/v1/scheduler/status`, `POST /api/v1/scheduler/run-due`, disabled/not-due cases being skipped, case-specific alert thresholds, snapshot/alert persistence, disabling monitoring, and the old `monitor/run` endpoint. The scheduler foundation is manual only; no background worker starts by default.

Latest v0.7 monitoring QA validation: 2026-05-14. Backend tests passed with `68 passed in 1.05s`. Frontend production build passed in 7.45s with the existing non-blocking Ant Design/ECharts vendor chunk warning. API smoke checks confirmed the monitoring flow creates persisted snapshots and alerts, including a deterministic `12.0` latest risk delta after repeated monitor runs. The Risk Monitor page supports persisted snapshots, case alert events, and a `Run Mock Monitoring Check` action. In-app browser automation timed out during this QA pass, so manually click through Risk Monitor before a live demo.

Latest v0.6 persistence validation: 2026-05-14. Backend tests passed with `55 passed in 0.51s`. Case API tests now verify create/list/detail/run, Chinese report attachment, Markdown export, and retrieval after reloading the repository/store from the same local JSON file. Frontend build was not rerun because no frontend files changed.

Latest Hupu public parser QA validation: 2026-05-15. Focused parser/crawl/registry/adapter and old-flow tests passed with `99 passed in 2.52s`; full backend validation passed with `141 passed in 2.78s`. Hupu remains fixture-only and live fetch remains disabled. The smoke command in section 4.6 should return one Hupu `RawPost`, two visible fixture `RawComment` replies, `parser_status=fixture_only`, `live_fetch_enabled=false`, `fallback_reason_category=live_fetch_disabled`, and schema flags set to true.

Latest Tieba public parser validation: 2026-05-15. Focused parser/crawl/registry/adapter tests passed with `58 passed in 0.98s`; full backend validation passed with `148 passed in 2.84s`. Tieba remains fixture-only and live fetch remains disabled, including when the global The Paper live-pilot flag is enabled. The smoke command in section 4.6 should return one Tieba `RawPost`, three visible fixture `RawComment` replies, `parser_status=fixture_only`, `live_fetch_enabled=false`, `fallback_reason_category=live_fetch_disabled`, schema flags set to true, and floor numbers in `raw_data.floor_number`.

Latest NGA public parser QA validation: 2026-05-15. Focused parser/crawl/registry/adapter tests passed with `65 passed in 0.78s`; full backend validation passed with `155 passed in 3.01s`. NGA remains fixture-only and live fetch remains disabled, including when the global The Paper live-pilot flag is enabled. The smoke command in section 4.6 should return one NGA `RawPost`, three visible fixture `RawComment` replies, `parser_status=fixture_only`, `live_fetch_enabled=false`, `fallback_reason_category=live_fetch_disabled`, schema flags set to true, and floor numbers in `raw_data.floor_number`.

Latest public parser status/preview QA validation: 2026-05-15. Focused status/preview tests passed with `12 passed in 1.6s`; full backend validation passed with `167 passed in 3.23s`. `GET /api/v1/public-parsers/status` returns The Paper, Jiemian, Hupu, Maimai, Tieba, and NGA with fixture/profile availability and comment-support flags. `POST /api/v1/public-parsers/preview` returns fixture-first `RawPost` / `RawComment` samples and schema validation flags. Preview does not attempt live fetch unless both the request and global configuration opt in; live public fetching remains disabled by default.

Latest Maimai public parser QA validation: 2026-05-15. Focused parser/crawl/registry/adapter/status tests passed with `86 passed in 0.88s`; full backend validation passed with `176 passed in 3.29s`. Maimai remains fixture-only and live fetch remains disabled, including when the global The Paper live-pilot flag is enabled. The smoke command in section 4.6 should return one Maimai `RawPost`, two visible fixture `RawComment` replies, `parser_status=fixture_only`, `live_fetch_enabled=false`, `fallback_reason_category=live_fetch_disabled`, and schema flags set to true.

Latest Public Parser Status frontend QA validation: 2026-05-15. The `公开页面解析` sidebar page was rechecked for route wiring, parser status loading, fixture preview, empty/error states, and no-live-fetch frontend behavior. The parser table now includes an inline `备注` column so every row shows platform notes. Frontend production build passed in 7.65s with the existing non-blocking Ant Design/ECharts vendor chunk warning. The page loads parser rows dynamically, so Maimai appears through the backend status endpoint without adding a live-fetch control; preview requests from the frontend code always pass `use_live_fetch=false`.

Latest Platform Integration Overview frontend QA validation: 2026-05-16. The `平台接入总览` sidebar page was rechecked against the safe status contract. It loads `GET /api/v1/platforms`, `GET /api/v1/platforms/status`, and `GET /api/v1/public-parsers/status`, shows all eight official API scaffolds, all six public parser platforms, Reddit API-pending status, and future/disabled sources. Public parser preview buttons remain fixed to `use_live_fetch=false`, preview samples render as cards, credential presence is displayed only as booleans, and registry-safe tags now show mock availability, real-mode availability, API approval state, MVP enablement, and mock/real selectability in the public-parser and tile sections. Frontend production build passed in 7.63s with the existing non-blocking Ant Design/ECharts vendor chunk warning. Backend code was not changed. Browser smoke found only the existing shared Ant Design `Spin` tip warning; no real platform API or live public fetch was enabled.

Latest Selector Repair Tool frontend QA validation: 2026-05-17. The `Selector 修复工具` sidebar page was rechecked for route wiring, sidebar navigation, six public parser platform options, safety notice content, selector suggestion flow, preview flow, warning/error/empty states, copy-only draft behavior, and no-live-fetch/no-apply behavior. Browser smoke confirmed fixture HTML suggestions and previews render as cards/tags, `profile_modified=false` remains visible, empty HTML shows a user-facing error, and `复制草稿 JSON` only copies suggestion JSON to the browser clipboard. Frontend production build passed in 7.56s with the existing non-blocking Ant Design/ECharts vendor chunk warning. Backend regression tests passed with `381 passed in 3.63s`. The only observed browser-console issue was the existing shared Ant Design `Spin` tip warning; no real LLM API, live website fetch, active profile modification, real platform API, cookie, login/captcha bypass, proxy rotation, private data access, or Reddit scraping was enabled.

Latest Weibo official API adapter QA validation: 2026-05-16. Focused Weibo/adapter/crawl/registry checks passed with `17 passed in 0.51s`; full backend validation passed with `201 passed in 3.03s`. Weibo remains mock-first through `WEIBO_ADAPTER_MODE=mock`; `WEIBO_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`, returns mock data, and makes no real Weibo API call. The smoke command in section 4.5.1 should return three mock Weibo microblog-style `RawPost` items, three mock visible-comment-style `RawComment` items, `source_type=official_api_adapter_scaffold`, `real_mode_available=false`, `raw_post_schema_valid=true`, and `raw_comment_schema_valid=true`. GitHub Actions CI remains intentionally disabled; use local/Codex validation only.

Latest Bilibili official API adapter QA validation: 2026-05-16. Focused Bilibili/adapter/crawl/registry/regression tests passed with `111 passed in 2.74s`; full backend validation passed with `189 passed in 3.09s`. Bilibili remains mock-first through `BILIBILI_ADAPTER_MODE=mock`; `BILIBILI_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`, returns mock data, and makes no real Bilibili API call. The smoke command in section 4.5.2 should return three mock Bilibili video-style `RawPost` items, three mock visible-comment-style `RawComment` items, `source_type=official_api_adapter_scaffold`, `real_mode_available=false`, and schema flags set to true.

Latest Douyin official API adapter QA validation: 2026-05-16. Focused Douyin/adapter/crawl/registry checks passed with `20 passed in 0.67s`; full backend validation passed with `213 passed in 3.10s`. Douyin remains mock-first through `DOUYIN_ADAPTER_MODE=mock`; `DOUYIN_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`, returns mock data, and makes no real Douyin API call. The smoke command in section 4.5.3 should return three mock Douyin short-video-style `RawPost` items, three mock visible-comment-style `RawComment` items, `source_type=official_api_adapter_scaffold`, `real_mode_available=false`, and schema flags set to true.

Latest Kuaishou official API adapter QA validation: 2026-05-16. Focused Kuaishou/adapter/crawl/registry checks passed with `59 passed in 0.75s`; full backend validation passed with `225 passed in 3.17s`. Kuaishou remains mock-first through `KUAISHOU_ADAPTER_MODE=mock`; `KUAISHOU_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`, returns mock data, and makes no real Kuaishou API call. The smoke command in section 4.5.4 should return three mock Kuaishou short-video/livestream-style `RawPost` items, three mock visible-comment-style `RawComment` items, `source_type=official_api_adapter_scaffold`, `real_mode_available=false`, and schema flags set to true. GitHub Actions CI remains intentionally disabled; use local/Codex validation only.

Latest Xiaohongshu official API adapter QA validation: 2026-05-16. Focused Xiaohongshu/adapter/crawl/registry checks passed with `63 passed in 0.77s`; full backend validation passed with `237 passed in 2.90s`. Xiaohongshu remains mock-first through `XIAOHONGSHU_ADAPTER_MODE=mock`; `XIAOHONGSHU_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`, returns mock data, and makes no real Xiaohongshu API call. The smoke command in section 4.5.5 should return three mock Xiaohongshu lifestyle/community-note-style `RawPost` items, three mock visible-comment-style `RawComment` items, `source_type=official_api_adapter_scaffold`, `real_mode_available=false`, and schema flags set to true. GitHub Actions CI remains intentionally disabled; use local/Codex validation only.

Latest Zhihu official API adapter QA validation: 2026-05-16. Focused Zhihu/adapter/crawl/registry checks passed with `67 passed in 0.80s`; full backend validation passed with `249 passed in 3.04s`. Zhihu remains mock-first through `ZHIHU_ADAPTER_MODE=mock`; `ZHIHU_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`, returns mock data, and makes no real Zhihu API call. The smoke command in section 4.5.6 should return mock Zhihu Q&A/article-style `RawPost` items, visible-comment-style `RawComment` items, `source_type=official_api_adapter_scaffold`, `real_mode_available=false`, and schema flags set to true. GitHub Actions CI remains intentionally disabled; use local/Codex validation only.

Latest Douban official API adapter QA validation: 2026-05-16. Focused Douban/adapter/crawl/registry checks passed with `71 passed in 0.76s`; full backend validation passed with `261 passed in 3.29s`. Douban remains mock-first through `DOUBAN_ADAPTER_MODE=mock`; `DOUBAN_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`, returns mock data, and makes no real Douban API call. The smoke command in section 4.5.7 should return mock Douban review/group/topic-style `RawPost` items, visible-comment-style `RawComment` items, `source_type=official_api_adapter_scaffold`, `real_mode_available=false`, and schema flags set to true. GitHub Actions CI remains intentionally disabled; use local/Codex validation only.

Latest Toutiao official API adapter QA validation: 2026-05-16. Full backend validation passed with `272 passed in 2.75s`. Toutiao remains mock-first through `TOUTIAO_ADAPTER_MODE=mock`; `TOUTIAO_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`, returns mock data, and makes no real Toutiao API call. The smoke command in section 4.5.8 should return mock Toutiao article/micro-headline-style `RawPost` items, visible-comment-style `RawComment` items, `source_type=official_api_adapter_scaffold`, `real_mode_available=false`, and schema flags set to true. GitHub Actions CI remains intentionally disabled; use local/Codex validation only.

Latest v0.4 adapter-foundation validation: 2026-05-14. Backend tests passed with `47 passed in 0.42s`, frontend production build passed in 7.68s, and API smoke checks passed for health, platform registry, crawl start, case create/list/detail/run, Markdown export, visualization, summary, recommendation, analysis result, V1.5 topic-risk fields, and the Reddit mock adapter. The Vite Ant Design/ECharts vendor chunk warning remains non-blocking.

Important constraints:

- Do not enable real crawlers.
- Do not call real platform APIs.
- Do not call OpenAI or external LLM APIs.
- Use the offline mock pipeline only.
- Test on a desktop browser around 1440px width.

## 0.1 v3.9 Exact Local Commands

Backend tests:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python -m pytest
```

Backend server with local JSON persistence:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set CASE_STORE_BACKEND=local_json
set PUBLIC_PARSER_LIVE_FETCH_ENABLED=false
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Frontend dev server:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"
npm run dev
```

Frontend production build:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"
npm run build
```

Reset local runtime JSON data:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\reset_local_data.py --yes
```

Seed deterministic demo cases:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\seed_demo_cases.py --reset-first
```

Run the local API smoke check after starting the backend:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\api_smoke_check.py --base-url http://127.0.0.1:8000
```

LLM Safety page demo:

1. Start the backend with local JSON mode.
2. Start the frontend dev server.
3. Open `http://127.0.0.1:5173`.
4. Click `LLM Safety` / `大模型安全状态` in the sidebar.
5. Confirm real calls are disabled, API key status is boolean-only, usage summaries contain no raw prompts, and there is no API key input or enable-real-calls button.

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

- Creates three deterministic demo cases.
- One case is completed with mock analysis, V1.5 topic risks, Chinese report, Markdown export data, snapshots, alerts, scheduler state, and local in-app notifications.
- One case remains a draft/demo watch case.
- One Hupu public-parser demo case is completed, and the script prints fixture preview post/comment counts without live fetching.

Run the local API smoke check after starting the backend:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\api_smoke_check.py --base-url http://127.0.0.1:8000
```

Expected result:

- Health, platforms, public parser status/preview, LLM status/usage, keyword/crawl/analysis, case run, Markdown export, monitoring, scheduler, alerts, notifications, and report endpoints pass.
- The script prints a clear pass/fail summary and exits nonzero on failure.

## 0.6 LLM Safety Page Check

Open the frontend and choose `LLM Safety` / `大模型安全状态` from the sidebar.

Expected result:

- The page shows `当前 Provider`, `真实调用`, `API Key 状态`, `调用次数`, `Token 估算`, `今日限制`, and `Mock 模式`.
- MockProvider is the active default unless local config was explicitly changed.
- OpenAI, DeepSeek, and Qwen are shown as future/disabled placeholders.
- API key state is displayed as booleans only; no key values or `.env` values are shown.
- The page shows a safety notice that it does not call real LLMs, does not display API keys, and does not record raw prompts.
- There is no button or input that enables real LLM calls, enters API keys, or modifies `.env`.

## 0.5 Optional MongoDB Persistence Check

The default demo still uses local JSON. MongoDB is optional and should only be enabled when a local development MongoDB server is already running.

Start backend with local JSON mode:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set CASE_STORE_BACKEND=local_json
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Start backend with optional MongoDB mode:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set CASE_STORE_BACKEND=mongodb
set MONGODB_URI=mongodb://localhost:27017
set MONGODB_DATABASE=sentigraph
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Expected result:

- MongoDB mode uses the same case/report/monitoring/scheduler/notification APIs.
- If MongoDB is not reachable, the first case-store access reports a configuration error.
- No real crawler, real platform API, external LLM, or real notification delivery is triggered.

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
- Credential-gated YouTube real-mode status

Expected result:

- Reddit, Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, Toutiao, and YouTube are visible as mock-selectable.
- Crawler-later platforms are visible but disabled.
- YouTube real mode is shown as available only when `YOUTUBE_API_KEY` is present; the key value is never displayed.

## 4.4.1 Optional YouTube Real-Data Manual Smoke Check

This check is manual only. It may call the official YouTube Data API v3, so keep it tiny, quota-aware, and key-redacted. Automated tests must continue to use mocked YouTube clients only.

Full manual demo story: `docs/youtube_real_data_demo.md`. Use that document when preparing screenshots because it covers backend/frontend startup, safe real-mode status verification, tiny crawl, case attachment, case analysis, report export, Risk Monitor/Forecast, Simulation Lab initialization, A/B comparison, strategy report export, cache behavior, and troubleshooting.

Frontend Keyword Search real-data flow:

1. Start the backend and frontend locally.
2. Open `Keyword Search`.
3. Select only `YouTube` in the platform selector. If YouTube is selected together with other platforms, use the mock flow or remove the other platforms for the real-data demo.
4. Confirm the explicit YouTube panel shows `Data: YouTube Real`, `Analysis: Offline`, and `LLM: Mock`.
5. Click `Create YouTube Real Case`.
6. Click `Crawl YouTube & Attach Raw Data`.
7. Confirm the panel shows safe crawl metadata: `raw_data_status=attached`, `raw_post_count`, `raw_comment_count`, `adapter_mode`, `fallback_used`, `cache_hit`, and `quota_guardrail_status`.
8. Click `Run Case Analysis`.
9. Confirm the panel shows `analysis_input_source=case_raw_data`, raw counts, and a representative-comments preview derived from attached YouTube comments when comments are available.
10. Use the shortcut buttons to open Analysis Result, Summary Report, Risk Monitor, or Simulation Lab from the completed YouTube case.

Prerequisites:

- The backend is running locally.
- An ignored local `.env` contains `YOUTUBE_ADAPTER_MODE=real` and `YOUTUBE_API_KEY`.
- Do not print `.env` values and do not echo the API key in the terminal.

PowerShell request:

```powershell
$body = @{
  keyword = "Tesla"
  platforms = @("youtube")
  limit = 3
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:8000/api/v1/crawl/start" `
  -ContentType "application/json" `
  -Body $body | ConvertTo-Json -Depth 8
```

Expected result:

- `platform_metadata[0].platform` is `youtube`.
- `platform_metadata[0].adapter_mode` is `real` when local configuration is valid.
- `platform_metadata[0].source_type` is `youtube_data_api_v3`.
- `platform_metadata[0].fallback_used=false`.
- `platform_metadata[0].credential_present=true`, with no key value returned.
- `platform_metadata[0].cache_hit` may be `false` on the first request and `true` on repeated requests within the cache TTL.
- `platform_metadata[0].estimated_quota_units`, `search_call_count`, `videos_call_count`, `comment_threads_call_count`, and `quota_guardrail_status` show safe quota/call diagnostics only.
- `post_count` and `comment_count` are tiny and schema-valid.
- `raw_posts` contain normalized public YouTube video metadata.
- `raw_comments` contain normalized public comment metadata.
- No scraping, cookies, login bypass, captcha bypass, browser profile, private data access, or LLM call occurs.

Cache behavior:

- The default cache path is `backend/data/youtube_cache.json`; it is ignored by git.
- Repeating the same tiny crawl within `YOUTUBE_CACHE_TTL_SECONDS` should avoid another official API call and return `cache_hit=true`.
- The cache stores normalized `RawPost` / `RawComment` data and safe metadata only. It must not store `YOUTUBE_API_KEY`.
- To clear the cache safely on Windows, stop the backend first, then delete only that runtime cache file:

```powershell
Remove-Item -LiteralPath "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\backend\data\youtube_cache.json" -Force -ErrorAction SilentlyContinue
```

Current real-data pipeline status:

- YouTube real crawl output is normalized and returned from `/api/v1/crawl/start`.
- YouTube crawl output can be explicitly attached to a case with `POST /api/v1/cases/{case_id}/crawl/start`.
- `POST /api/v1/cases/{case_id}/run` uses attached case raw comments when available and falls back to mock data when no raw comments are attached.
- Case creation and case run do not automatically call YouTube.

Optional case-ingestion demo path:

```powershell
$caseBody = @{
  keyword = "Tesla"
  platforms = @("youtube")
  title = "YouTube Real Data Case"
} | ConvertTo-Json

$case = Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:8000/api/v1/cases" `
  -ContentType "application/json" `
  -Body $caseBody

$crawlBody = @{
  limit = 3
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/crawl/start" `
  -ContentType "application/json" `
  -Body $crawlBody | ConvertTo-Json -Depth 8

Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/run" | ConvertTo-Json -Depth 8

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/report/markdown" | ConvertTo-Json -Depth 8

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/simulation/initialization-preview" | ConvertTo-Json -Depth 8
```

Expected result:

- The case detail shows `raw_data_status=attached`, `crawl_source_mode=case_crawl_start`, and nonzero `raw_comment_count` if YouTube returned comments.
- The case run shows `analysis_result.analysis_input_source=case_raw_data`.
- Representative comments in the Chinese report can come from attached YouTube comments.
- Analysis Result, Summary Report, Demo Flow, and the app header should show the provenance badges `Data: YouTube Real`, `Analysis: Offline`, and `LLM: Mock`.
- Screenshot target: capture the provenance badge row showing `Data: YouTube Real / Analysis: Offline / LLM: Mock`; this proves real source data and offline deterministic analysis are separate.
- If YouTube comments include low-quality channel promotion/self-promo, the stored raw comments remain attached, but `representative_comments` should prefer substantive event/topic comments when alternatives exist.
- The same completed case can be used by Simulation Lab case initialization; the preview returns only aggregate event-frame, audience, and scenario data.
- API key values are never returned; only boolean credential metadata is shown.

Full YouTube real-data demo API path:

```powershell
$base = "http://127.0.0.1:8000/api/v1"

$caseBody = @{
  keyword = "Tesla"
  platforms = @("youtube")
  title = "YouTube Real Data Case"
  report_language = "zh-CN"
} | ConvertTo-Json

$case = Invoke-RestMethod `
  -Method Post `
  -Uri "$base/cases" `
  -ContentType "application/json" `
  -Body $caseBody

$crawlBody = @{ limit = 3 } | ConvertTo-Json
$attached = Invoke-RestMethod `
  -Method Post `
  -Uri "$base/cases/$($case.case_id)/crawl/start" `
  -ContentType "application/json" `
  -Body $crawlBody

$run = Invoke-RestMethod `
  -Method Post `
  -Uri "$base/cases/$($case.case_id)/run"

$run.analysis_result.analysis_input_source
$run.report.representative_comments | Select-Object -First 3

$markdown = Invoke-RestMethod -Uri "$base/cases/$($case.case_id)/report/markdown"
$monitor = Invoke-RestMethod -Method Post -Uri "$base/cases/$($case.case_id)/monitor/run"
$forecast = Invoke-RestMethod -Method Post -Uri "$base/cases/$($case.case_id)/forecast/run"
$init = Invoke-RestMethod -Method Post -Uri "$base/cases/$($case.case_id)/simulation/initialize"

$scenarioA = $init.simulation_scenario | ConvertTo-Json -Depth 40 | ConvertFrom-Json
$scenarioA.interventions[0].intervention_type = "no_response"
$scenarioA.interventions[0].stance_direction = 0
$scenarioA.interventions[0].evidence_strength = 0
$scenarioA.interventions[0].transparency_level = 0

$scenarioB = $init.simulation_scenario | ConvertTo-Json -Depth 40 | ConvertFrom-Json
$scenarioB.interventions[0].intervention_type = "clarification"
$scenarioB.interventions[0].stance_direction = 0.28
$scenarioB.interventions[0].evidence_strength = 0.68
$scenarioB.interventions[0].transparency_level = 0.72

$resultA = Invoke-RestMethod `
  -Method Post `
  -Uri "$base/simulation/run" `
  -ContentType "application/json" `
  -Body ($scenarioA | ConvertTo-Json -Depth 40)

$resultB = Invoke-RestMethod `
  -Method Post `
  -Uri "$base/simulation/run" `
  -ContentType "application/json" `
  -Body ($scenarioB | ConvertTo-Json -Depth 40)

$strategyReportBody = @{
  simulation_mode = "comparison"
  scenario_name = $init.simulation_scenario.name
  intervention_a = "no_response"
  intervention_b = "clarification"
  result_a = $resultA
  result_b = $resultB
} | ConvertTo-Json -Depth 60

$strategyReport = Invoke-RestMethod `
  -Method Post `
  -Uri "$base/simulation/report/markdown" `
  -ContentType "application/json" `
  -Body $strategyReportBody

$strategyReport.markdown.Substring(0, [Math]::Min(800, $strategyReport.markdown.Length))
```

Expected result:

- `$run.analysis_result.analysis_input_source` is `case_raw_data` when YouTube returns and attaches public comments.
- Representative comments can include YouTube public comments, while API keys and `.env` values never appear.
- Monitoring and forecast endpoints continue to work from the completed case snapshot path.
- Simulation Lab initialization returns aggregate event-frame, audience, persona-cluster, gap-analysis, and synthetic scenario data only.
- The two simulation runs and Markdown strategy report remain deterministic, aggregate-level, and human-review-oriented.
- If YouTube returns no comments or a quota/auth/network error, the adapter should fall back safely; inspect `crawl_metadata` for `fallback_used`, `fallback_reason_category`, and tiny counts.
- If the same crawl is repeated during the cache TTL, inspect `crawl_metadata` for `cache_hit=true`, `estimated_quota_units=0`, and `quota_guardrail_status=cache_hit`.
- For the visual A/B flow, open the frontend Simulation Lab page after this API smoke and load the case with `从案例初始化沙盘`.

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

## 4.5.1 Optional Weibo Mock Adapter Smoke Check

This checks the official API adapter scaffold for Weibo. It should stay offline, should not require Weibo credentials, and should not call real Weibo APIs.

Direct adapter check:

```cmd
cd /d "G:\AICODING\Sentigraph 鑸嗘儏鍥捐氨绯荤粺\Sentigraph"
set PYTHONPATH=backend
python -c "from app.services.crawling.adapter_factory import get_adapter; a=get_adapter('weibo'); posts=a.search_posts('Tesla', limit=3); comments=a.fetch_comments(posts[0].post_id, limit=3); print(a.health_check()); print(len(posts), len(comments), posts[0].platform, comments[0].platform)"
```

Backend `/crawl/start` check:

```powershell
cd /d "G:\AICODING\Sentigraph 鑸嗘儏鍥捐氨绯荤粺\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("weibo"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

Expected result:

- Adapter mode is `mock`.
- `platform_metadata[0].platform` is `weibo`.
- `platform_metadata[0].source_type` is `official_api_adapter_scaffold`.
- `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- `post_count` and `comment_count` are greater than zero and capped by the safe crawl limit.
- `raw_post_schema_valid=true` and `raw_comment_schema_valid=true`.
- Mock `RawPost` items include platform, post id, author id/name, title, content, like/reply/share counts, created time, URL, and raw data.
- Mock `RawComment` items include platform, post id, comment id, parent id when present, author id/name, content, like/reply counts, created time, URL, and raw data.
- No real Weibo API call, Weibo page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call occurs.

## 4.5.2 Optional Bilibili Mock Adapter Smoke Check

This checks the official API adapter scaffold for Bilibili. It should stay offline, should not require Bilibili credentials, and should not call real Bilibili APIs.

Direct adapter check:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set PYTHONPATH=backend
python -c "from app.services.crawling.adapter_factory import get_adapter; a=get_adapter('bilibili'); posts=a.search_posts('Tesla', limit=3); comments=a.fetch_comments(posts[0].post_id, limit=3); print(a.health_check()); print(len(posts), len(comments), posts[0].platform, comments[0].platform)"
```

Backend `/crawl/start` check:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("bilibili"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

Expected result:

- Adapter mode is `mock`.
- `platform_metadata[0].platform` is `bilibili`.
- `platform_metadata[0].source_type` is `official_api_adapter_scaffold`.
- `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- `post_count` and `comment_count` are greater than zero and capped by the safe crawl limit.
- `raw_post_schema_valid=true` and `raw_comment_schema_valid=true`.
- Mock `RawPost` items include platform, post id, author id/name, title, content, like/reply counts, created time, URL, and raw data.
- Mock `RawComment` items include platform, post id, comment id, parent id when present, author id/name, content, like/reply counts, created time, URL, and raw data.
- No real Bilibili API call, Bilibili page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call occurs.

## 4.5.3 Optional Douyin Mock Adapter Smoke Check

This checks the official API adapter scaffold for Douyin. It should stay offline, should not require Douyin credentials, and should not call real Douyin APIs.

Direct adapter check:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set PYTHONPATH=backend
python -c "from app.services.crawling.adapter_factory import get_adapter; a=get_adapter('douyin'); posts=a.search_posts('Tesla', limit=3); comments=a.fetch_comments(posts[0].post_id, limit=3); print(a.health_check()); print(len(posts), len(comments), posts[0].platform, comments[0].platform)"
```

Backend `/crawl/start` check:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("douyin"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

Expected result:

- Adapter mode is `mock`.
- `platform_metadata[0].platform` is `douyin`.
- `platform_metadata[0].source_type` is `official_api_adapter_scaffold`.
- `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- `post_count` and `comment_count` are greater than zero and capped by the safe crawl limit.
- `raw_post_schema_valid=true` and `raw_comment_schema_valid=true`.
- Mock `RawPost` items include platform, post id, creator id/name, title, content, like/reply/share counts, created time, URL, and raw data.
- Mock `RawComment` items include platform, post id, comment id, parent id when present, author id/name, content, like/reply counts, created time, URL, and raw data.
- No real Douyin API call, Douyin page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call occurs.

## 4.5.4 Optional Kuaishou Mock Adapter Smoke Check

This checks the official API adapter scaffold for Kuaishou. It should stay offline, should not require Kuaishou credentials, and should not call real Kuaishou APIs.

Direct adapter check:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set PYTHONPATH=backend
python -c "from app.services.crawling.adapter_factory import get_adapter; a=get_adapter('kuaishou'); posts=a.search_posts('Tesla', limit=3); comments=a.fetch_comments(posts[0].post_id, limit=3); print(a.health_check()); print(len(posts), len(comments), posts[0].platform, comments[0].platform)"
```

Backend `/crawl/start` check:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("kuaishou"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

Expected result:

- Adapter mode is `mock`.
- `platform_metadata[0].platform` is `kuaishou`.
- `platform_metadata[0].source_type` is `official_api_adapter_scaffold`.
- `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- `post_count` and `comment_count` are greater than zero and capped by the safe crawl limit.
- `raw_post_schema_valid=true` and `raw_comment_schema_valid=true`.
- Mock `RawPost` items include platform, post id, creator id/name, title, content, like/reply/share counts, created time, URL, and raw data.
- Mock `RawComment` items include platform, post id, comment id, parent id when present, author id/name, content, like/reply counts, created time, URL, and raw data.
- No real Kuaishou API call, Kuaishou page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call occurs.

## 4.5.5 Optional Xiaohongshu Mock Adapter Smoke Check

This checks the official API adapter scaffold for Xiaohongshu. It should stay offline, should not require Xiaohongshu credentials, and should not call real Xiaohongshu APIs.

Direct adapter check:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set PYTHONPATH=backend
python -c "from app.services.crawling.adapter_factory import get_adapter; a=get_adapter('xiaohongshu'); posts=a.search_posts('Tesla', limit=3); comments=a.fetch_comments(posts[0].post_id, limit=3); print(a.health_check()); print(len(posts), len(comments), posts[0].platform, comments[0].platform)"
```

Backend `/crawl/start` check:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("xiaohongshu"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

Expected result:

- Adapter mode is `mock`.
- `platform_metadata[0].platform` is `xiaohongshu`.
- `platform_metadata[0].source_type` is `official_api_adapter_scaffold`.
- `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- `post_count` and `comment_count` are greater than zero and capped by the safe crawl limit.
- `raw_post_schema_valid=true` and `raw_comment_schema_valid=true`.
- Mock `RawPost` items include platform, post id, creator id/name, title, content, like/reply/share counts, created time, URL, and raw data.
- Mock `RawComment` items include platform, post id, comment id, parent id when present, author id/name, content, like/reply counts, created time, URL, and raw data.
- No real Xiaohongshu API call, Xiaohongshu page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call occurs.

## 4.5.6 Optional Zhihu Mock Adapter Smoke Check

This checks the official API adapter scaffold for Zhihu. It should stay offline, should not require Zhihu credentials, and should not call real Zhihu APIs.

Direct adapter check:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set PYTHONPATH=backend
python -c "from app.services.crawling.adapter_factory import get_adapter; a=get_adapter('zhihu'); posts=a.search_posts('Tesla', limit=3); comments=a.fetch_comments(posts[0].post_id, limit=3); print(a.health_check()); print(len(posts), len(comments), posts[0].platform, comments[0].platform)"
```

Backend `/crawl/start` check:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("zhihu"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

Expected result:

- Adapter mode is `mock`.
- `platform_metadata[0].platform` is `zhihu`.
- `platform_metadata[0].source_type` is `official_api_adapter_scaffold`.
- `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- `post_count` and `comment_count` are greater than zero and capped by the safe crawl limit.
- `raw_post_schema_valid=true` and `raw_comment_schema_valid=true`.
- Mock `RawPost` items include platform, post id, author id/name, title, content, like/reply/share counts, created time, URL, and raw data.
- Mock `RawComment` items include platform, post id, comment id, parent id when present, author id/name, content, like/reply counts, created time, URL, and raw data.
- No real Zhihu API call, Zhihu page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call occurs.

## 4.5.7 Optional Douban Mock Adapter Smoke Check

This checks the official API adapter scaffold for Douban. It should stay offline, should not require Douban credentials, and should not call real Douban APIs.

Direct adapter check:

```cmd
cd /d "G:\AICODING\Sentigraph 鑸嗘儏鍥捐氨绯荤粺\Sentigraph"
set PYTHONPATH=backend
python -c "from app.services.crawling.adapter_factory import get_adapter; a=get_adapter('douban'); posts=a.search_posts('Tesla', limit=3); comments=a.fetch_comments(posts[0].post_id, limit=3); print(a.health_check()); print(len(posts), len(comments), posts[0].platform, comments[0].platform)"
```

Backend `/crawl/start` check:

```powershell
cd /d "G:\AICODING\Sentigraph 鑸嗘儏鍥捐氨绯荤粺\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("douban"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

Expected result:

- Adapter mode is `mock`.
- `platform_metadata[0].platform` is `douban`.
- `platform_metadata[0].source_type` is `official_api_adapter_scaffold`.
- `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- `post_count` and `comment_count` are greater than zero and capped by the safe crawl limit.
- `raw_post_schema_valid=true` and `raw_comment_schema_valid=true`.
- Mock `RawPost` items include platform, post id, author id/name, title, content, like/reply/share counts, created time, URL, and raw data.
- Mock `RawComment` items include platform, post id, comment id, parent id when present, author id/name, content, like/reply counts, created time, URL, and raw data.
- No real Douban API call, Douban page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call occurs.

## 4.5.8 Optional Toutiao Mock Adapter Smoke Check

This checks the official API adapter scaffold for Toutiao. It should stay offline, should not require Toutiao credentials, and should not call real Toutiao APIs.

Direct adapter check:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set PYTHONPATH=backend
python -c "from app.services.crawling.adapter_factory import get_adapter; a=get_adapter('toutiao'); posts=a.search_posts('Tesla', limit=3); comments=a.fetch_comments(posts[0].post_id, limit=3); print(a.health_check()); print(len(posts), len(comments), posts[0].platform, comments[0].platform)"
```

Backend `/crawl/start` check:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("toutiao"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

Expected result:

- Adapter mode is `mock`.
- `platform_metadata[0].platform` is `toutiao`.
- `platform_metadata[0].source_type` is `official_api_adapter_scaffold`.
- `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- `post_count` and `comment_count` are greater than zero and capped by the safe crawl limit.
- `raw_post_schema_valid=true` and `raw_comment_schema_valid=true`.
- Mock `RawPost` items include platform, post id, author id/name, title, content, like/reply/share counts, created time, URL, and raw data.
- Mock `RawComment` items include platform, post id, comment id, parent id when present, author id/name, content, like/reply counts, created time, URL, and raw data.
- No real Toutiao API call, Toutiao page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call occurs.

## 4.6 Optional Public Parser Fixture Smoke Check

This checks the fixture-only public-page parser scaffolds. It must stay offline and must not enable live public fetching.

PowerShell check for The Paper / Pengpai News:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("the_paper"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

PowerShell check for Jiemian News:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("jiemian"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

PowerShell check for Hupu / HuPu:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("hupu"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

PowerShell check for Maimai / 脉脉:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("maimai"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

PowerShell check for Baidu Tieba:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("tieba"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

PowerShell check for NGA:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("nga"); limit = 3 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

Expected result:

- `platform_metadata[0].source_type` is `public_page_parser`.
- `parser_status` is `fixture_only`.
- `live_fetch_enabled` is `false`.
- `fallback_reason_category` is `live_fetch_disabled`.
- `schema_valid`, `raw_post_schema_valid`, and `raw_comment_schema_valid` are `true`.
- The Paper, Jiemian, Hupu, Maimai, Tieba, and NGA return fixture/mock `RawPost` items.
- Jiemian returns no comments; this is documented as `comments_unavailable_without_login_or_dynamic_loading`.
- Hupu returns visible fixture replies as `RawComment` items with author/content/date/light-count fields when present in the fixture.
- Maimai returns visible fixture replies as `RawComment` items with author/content/date/like-count fields when present in the fixture.
- Tieba returns visible fixture replies as `RawComment` items with author/content/date/like-count fields and `raw_data.floor_number` when present in the fixture.
- NGA returns visible fixture replies as `RawComment` items with author/content/date/like-count fields and `raw_data.floor_number` when present in the fixture.
- No real public-page fetch, cookies, login, captcha handling, proxy rotation, private data access, Reddit scraping, platform API call, or external LLM call occurs.

## 4.6.1 Public Parser Status and Preview

This checks the unified public parser diagnostics layer. It remains fixture-first and should not enable live public fetching.

List all parser sources:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/public-parsers/status" | ConvertTo-Json -Depth 8
```

Preview one fixture parser:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ platform = "hupu"; limit = 3; use_live_fetch = $false } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/public-parsers/preview" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

Expected result:

- Status includes `the_paper`, `jiemian`, `hupu`, `maimai`, `tieba`, and `nga`.
- `fixture_available=true` and `profile_available=true` for all six current parser scaffolds.
- Preview returns sample `RawPost` data and visible fixture `RawComment` data where supported.
- `raw_post_schema_valid=true` and `raw_comment_schema_valid=true`.
- `live_fetch_enabled=false` by default.

Frontend page check:

1. Start the backend and frontend.
2. Open `http://127.0.0.1:5173`.
3. Click the sidebar item `公开页面解析`.
4. Confirm the parser table lists `the_paper`, `jiemian`, `hupu`, `maimai`, `tieba`, and `nga`.
5. Confirm every parser row shows platform id, display name, source type, parser status, Fixture/Profile availability, Live Fetch status, comments support, safe limit, request interval, and notes.
6. Click `预览` for `the_paper`, `jiemian`, `hupu`, `maimai`, `tieba`, and `nga`.

Expected frontend result:

- Preview summary shows post count, comment count, fallback reason, schema validation flags, sample posts, sample comments where available, and warnings.
- The frontend request keeps `use_live_fetch=false`; no visible live-fetch enable control is exposed.
- Empty arrays and missing optional preview fields show empty/fallback text instead of crashing.

## 4.6.2 Platform Integration Overview

This checks the unified frontend overview for all platform integration states. It is read-only except for fixture-safe public parser preview buttons.

API checks:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/platforms" | ConvertTo-Json -Depth 8
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/platforms/status" | ConvertTo-Json -Depth 8
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/public-parsers/status" | ConvertTo-Json -Depth 8
```

Frontend page check:

1. Start the backend and frontend.
2. Open `http://127.0.0.1:5173`.
3. Click the sidebar item `平台接入总览`.
4. Confirm the page shows sections for `官方 API 规划平台`, `公开页面解析平台`, `Reddit 状态`, and `暂不启用 / 未来可选`.
5. Confirm official API scaffolds include `bilibili`, `weibo`, `douyin`, `kuaishou`, `xiaohongshu`, `zhihu`, `douban`, and `toutiao`.
6. Confirm public parser platforms include `the_paper`, `jiemian`, `hupu`, `tieba`, `nga`, and `maimai`.
7. Confirm Reddit shows API pending/mock/fallback status and no scraping-bypass language.
8. Confirm credential status is shown only as configured/missing booleans, never credential values.
9. Confirm public parser rows and Reddit/future tiles show registry-safe fields for Mock availability, real-mode availability, API approval, MVP enablement, and mock/real selectability.
10. Click `预览` on public parser rows and confirm sample posts/comments render as cards.

Expected frontend result:

- The overview loads from existing backend status endpoints.
- Public parser preview requests from this page use `use_live_fetch=false`.
- No frontend switch or button can enable live fetch or real adapter mode.
- Missing optional fields, empty arrays, and partial endpoint failures show fallback or warning states instead of crashing.
- React never renders raw JavaScript objects such as `[object Object]` in the visible page.
- No real platform API, public-page fetch, cookie, login, captcha handling, proxy rotation, private data access, Reddit scraping, or external LLM call occurs.

## 4.6.3 Selector Repair Tool

This checks the developer-facing selector repair panel. It uses only caller-provided fixture/sanitized HTML and the existing mock selector repair backend.

Frontend page check:

1. Start the backend and frontend.
2. Open `http://127.0.0.1:5173`.
3. Click the sidebar item `Selector 修复工具`.
4. Confirm the page shows the safety notice: MockProvider mode, no real LLM calls, no live webpage fetch, no automatic parser profile modification, and fixture/sanitized HTML only.
5. Select a public parser platform such as `hupu`, `the_paper`, or `jiemian`.
6. Paste or keep fixture-style HTML in the `Sanitized HTML` text area.
7. Click `生成 Selector 建议`.
8. Confirm candidate selector cards show target field, selector, confidence, rationale, and source.
9. Click `预览建议`.
10. Confirm preview shows extracted title/content samples where matched, matched target tags, warnings, and `profile_modified=false`.
11. Clear the HTML field and confirm the page shows a user-facing error instead of crashing.
12. Click `复制草稿 JSON` after generating a suggestion and confirm only JSON text is copied to the clipboard.
13. If testing error handling, stop the backend or submit an unsupported platform through an API client and confirm the page shows a safe backend error state.

Expected result:

- The frontend calls `POST /api/v1/public-parsers/selector-repair/suggest` and `POST /api/v1/public-parsers/selector-repair/preview`.
- The frontend does not fetch live websites and does not expose a live-fetch toggle.
- The page does not include an apply-to-profile button.
- `复制草稿 JSON` only copies suggestion JSON to the clipboard; it does not write profile files.
- `Schema 校验` displays backend schema status if returned and otherwise shows `未返回` without crashing.
- Empty HTML, malformed HTML, missing optional fields, invalid platform/backend errors, and preview warnings render as UI states rather than raw JavaScript objects.
- No real LLM API, real platform API, browser cookie, login/captcha bypass, proxy rotation, private data access, Reddit scraping, or active profile modification occurs.

## 4.7 Optional The Paper Live Public-Page Fetch Pilot

This is a local-only pilot and is disabled by default. Use it only for one tiny manual check against a public The Paper article page. Do not use accounts, cookies, browser profiles, captcha handling, proxy rotation, or private/authenticated pages.

Latest QA validation: automated tests use mocked network responses only. The tests verify the default disabled fixture/mock path, robots-blocked fallback before page fetch, network-error fallback, selector-error fallback, mocked valid public HTML parsing, and safe request headers without cookies or authorization. Backend validation passed with `136 passed in 2.75s`.

Confirm the default safe mode before enabling the pilot:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set PUBLIC_PARSER_LIVE_FETCH_ENABLED=false
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

In another terminal:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "Tesla"; platforms = @("the_paper"); limit = 1 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

Expected default result: `live_fetch_enabled=false`, `live_fetch_attempted=false`, `fallback_used=true`, `fallback_reason_category=live_fetch_disabled`, `fetch_status=disabled`, and schema flags remain true.

Start the backend with live public parser fetch explicitly enabled:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set PUBLIC_PARSER_LIVE_FETCH_ENABLED=true
set PUBLIC_PARSER_RATE_LIMIT_SECONDS=3
set PUBLIC_PARSER_USER_AGENT=sentigraph-public-parser-dev
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

In a second PowerShell window, run one small request. Replace `<the_paper_article_id>` with the public id from a The Paper URL such as `newsDetail_forward_<the_paper_article_id>`:

```powershell
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
$body = @{ keyword = "<the_paper_article_id>"; platforms = @("the_paper"); limit = 1 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/crawl/start" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 8
```

Expected result:

- `live_fetch_enabled` is `true`.
- `live_fetch_attempted` shows whether the live path was reached.
- `live_fetch_allowed` is `true` only if robots/profile policy allowed the public page fetch.
- `fetch_status` is a safe value such as `ok`, `robots_disallowed`, `robots_unavailable_or_unclear`, `path_not_allowed_by_profile`, `network_error`, `http_error`, or `selector_missing`.
- If anything is blocked, unclear, unavailable, or unparsable, `fallback_used` is `true` and fixture/mock `RawPost` data is returned.
- Comments remain unavailable unless clearly visible in the public page without login.

After the pilot, restart the backend with live fetch disabled:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set PUBLIC_PARSER_LIVE_FETCH_ENABLED=false
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

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

## 8.8 Run Deterministic Risk Forecast

With a completed case selected:

1. Open Risk Monitor.
2. If the case has no snapshots yet, confirm the forecast panel shows `历史不足，需更多监控快照` or the equivalent insufficient-history state.
3. Click `Run Mock Monitoring Check` at least twice, or use the backend monitor command below to create deterministic snapshots.
4. Click `运行风险预测`.
5. Confirm the `风险预测` panel shows `预测风险`, `预测等级`, `趋势方向`, `预测置信度`, `真实危机风险预测`, `操纵传播风险预测`, and `未来高风险话题` when topic data is available.
6. Confirm the `预测解释` area shows the deterministic-MVP disclaimer, `为什么风险上升` / `为什么风险下降` / stable-or-unknown explanation, `主要驱动因素`, `历史数据是否足够`, `置信度说明`, and `建议继续运行监控以积累快照` when history is thin.

Backend smoke commands:

```cmd
powershell -Command "$case = Invoke-RestMethod -Method Post 'http://127.0.0.1:8000/api/v1/cases' -ContentType 'application/json' -Body '{\"keyword\":\"Tesla\",\"platforms\":[\"reddit\",\"weibo\"],\"title\":\"v4.5 Forecast Demo\"}'; Invoke-RestMethod -Method Post \"http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/run\"; Invoke-RestMethod -Method Post \"http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/monitor/run\"; Invoke-RestMethod -Method Post \"http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/monitor/run\"; Invoke-RestMethod -Method Post \"http://127.0.0.1:8000/api/v1/cases/$($case.case_id)/forecast/run\" | ConvertTo-Json -Depth 8"
```

Expected result:

- `GET /api/v1/cases/{case_id}/forecast` and `POST /api/v1/cases/{case_id}/forecast/run` return deterministic offline forecasts from persisted monitoring snapshots.
- Zero snapshots returns `forecast_status=insufficient_history` with a safe recommendation.
- One snapshot returns a conservative low-confidence baseline forecast.
- Multiple snapshots expose latest risk, moving average, slope, acceleration, volatility, trend direction, four horizons, real-crisis forecast, manipulation-risk forecast, and topic forecasts when topic history exists.
- The Risk Monitor frontend explains why the trend is rising, falling, stable, or uncertain without adding a real LLM, real platform call, or machine-learning dependency.
- Predicted scores are clamped to `0-100`, confidence never exceeds `medium`, and no real platform API, real LLM API, crawler, live public fetch, or real notification service is used.

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
- YouTube is mock-selectable and optionally real-capable through the official Data API v3 when configured locally.
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

## 12. Benchmark Dashboard / Evaluation Report

Before opening the page, generate at least one offline benchmark summary. Run it twice if you want to see a previous/latest regression comparison:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\run_offline_benchmarks.py
```

Start the backend and frontend:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"
npm run dev
```

Demo steps:

1. Open `http://127.0.0.1:5173`.
2. Click `Benchmarks / 离线评测` in the sidebar.
3. Confirm the page shows `总通过`, `总失败`, `警告`, `评测套件`, `最近结果`, and `回归风险`.
4. Confirm the suites appear: sentiment, topic_cluster, topic_risk, report_builder, report_quality_rubric, markdown_export, forecasting, selector_repair, public_parser_fixtures, and platform_adapter_mocks.
5. Confirm missing summary state appears clearly if `.benchmarks/offline_benchmark_summary.json` has not been generated.
6. Optionally verify the safe summary endpoint directly:

```cmd
powershell -Command "Invoke-RestMethod http://127.0.0.1:8000/api/v1/benchmarks/latest | ConvertTo-Json -Depth 8"
```

Expected result:

- The frontend only reads `GET /api/v1/benchmarks/latest`, `GET /api/v1/benchmarks/history`, and `GET /api/v1/benchmarks/regression`.
- The backend does not run benchmarks automatically.
- Missing or malformed benchmark summary files return a clear empty/error state and do not expose project-local file paths.
- If the page shows a 404 for `/api/v1/benchmarks/latest`, stop the old backend process and restart uvicorn so the new benchmark route is loaded.
- No real LLM API, real platform API, crawler, live public fetch, real notification, API key value, `.env` value, raw prompt, or raw user content is exposed.

Benchmark history and regression addendum:

1. Run `python scripts\run_offline_benchmarks.py` at least twice to create `.benchmarks/offline_benchmark_summary.json` and `.benchmarks/history/` entries.
2. Refresh the `Benchmarks / 离线评测` page.
3. Confirm the page shows `历史记录`, `回归检测`, `是否退化`, `新增失败`, `警告变化`, and `套件变化`.
4. Confirm regression status is one of `无回归`, `发现回归风险`, or `无历史记录可比较`.
5. Confirm history rows show generated time, pass/fail/warning totals, duration, and whether a regression was detected.
6. Verify the safe endpoints directly if needed:

```cmd
powershell -Command "Invoke-RestMethod http://127.0.0.1:8000/api/v1/benchmarks/history | ConvertTo-Json -Depth 8"
powershell -Command "Invoke-RestMethod http://127.0.0.1:8000/api/v1/benchmarks/regression | ConvertTo-Json -Depth 8"
```

Expected result: the history/regression APIs read only project-local `.benchmarks/` summary files, never run benchmarks automatically, never expose local file paths or case payloads, and never expose raw prompts, raw user content, API keys, `.env` values, or external request bodies.

## 13. Simulation Lab / 舆情预演沙盘

Start the backend and frontend:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"
npm run dev
```

Demo steps:

1. Open `http://127.0.0.1:5173`.
2. Click `Simulation Lab / 舆情预演沙盘` in the sidebar.
3. Confirm the page loads a deterministic demo scenario from `GET /api/v1/simulation/demo-scenario`.
4. Confirm the page shows scenario controls, event/intervention cards, the bubble canvas, aggregate metrics, explanation cards, and a step timeline.
5. Select an allowed intervention such as `事实澄清`, `公开致歉`, `补偿方案`, `FAQ 问答`, `进展更新`, `第三方证据`, `误信息纠正`, or `不回应基线`.
6. Click `运行模拟`, then click `单步推进`.
7. Confirm bubbles change color/opacity/glow, aggregate metrics update, and the timeline highlights the selected step.
8. Confirm the page states that the simulation is deterministic scenario rehearsal and not a guaranteed future prediction.
9. Confirm event cards show `source_type`, `intervention_type`, `source_credibility`, `emotional_intensity`, `evidence_strength`, and `platform_reach`.
10. Confirm the explanation panel shows `为什么风险上升`, `为什么风险下降`, `哪些群体受影响最大`, `哪个干预正在生效`, and the deterministic-MVP disclaimer.
11. Confirm empty/error states are user-facing if the backend is stopped, no scenario is loaded, or the backend rejects an invalid payload.

A/B comparison demo steps:

1. Switch from `单场景模拟` to `A/B 策略对比`.
2. Select `A 方案` as `no_response` and `B 方案` as an allowed transparent intervention such as `clarification`, `apology`, or `content_removal_with_explanation` if the backend ethics policy exposes it.
3. Click `运行 A/B 对比`.
4. Confirm two side-by-side bubble panels appear for `A 方案` and `B 方案`.
5. Confirm `对比结果` shows aggregate deltas for risk change, negative ratio change, polarization change, trust recovery, and backlash risk.
6. Confirm the comparison says `human_review_required` / `人工复核建议` and does not auto-apply any strategy.
7. Click `单步对比` or timeline steps and confirm the A/B timeline updates both sides from the same initial scenario.
8. For QA, exercise these pairs: `no_response` vs `clarification`, `no_response` vs `apology`, `no_response` vs `third_party_evidence`, `clarification` vs `misinformation_correction`, and `no_response` vs `content_removal_with_explanation`.
9. Confirm the comparison summary displays scalar field chips for `better_option`, `risk_delta`, `negative_ratio_delta`, `polarization_delta`, `trust_recovery_delta`, and `ethical_risk_notes` without rendering raw JavaScript objects.

Content visibility intervention demo steps:

1. In `A/B 策略对比`, select `A 方案` as `no_response`.
2. Select `B 方案` as `透明说明后内容移除`, `合规可见性降低`, or `平台标注` if available from `GET /api/v1/simulation/ethics-policy`.
3. Click `运行 A/B 对比`.
4. Confirm the `内容可见性干预` panel appears.
5. Confirm the panel displays `直接曝光降低`, `反弹风险`, `信任损失`, `跨平台外溢`, `中立人群影响`, `强反对群体影响`, `净风险变化`, `删除正当性`, `透明说明质量` where available, and `人工复核建议`.
6. Confirm the safety copy says the module evaluates compliant content-governance risk/reward and does not execute platform actions.
7. Confirm the UI does not expose illegal/covert suppression, fake consensus, bot amplification, fake events, covert influencer seeding, targeted persuasion, or account-level targeting options.

Strategy report export demo steps:

1. In single-scenario mode, run an allowed intervention such as `clarification`.
2. Click `导出策略预演报告`.
3. Confirm the `策略预演报告` card shows a Markdown preview with `# Simulation Lab Strategy Report`, `Scenario Overview`, `Intervention Comparison`, `Key Metrics`, `Audience Impact`, `Ethical Risk Review`, `Recommended Human Review Questions`, and `Limitations`.
4. Click `复制 Markdown` and confirm the copy success state appears.
5. Click `下载 .md` and confirm a local Markdown file is prepared by the browser.
6. Switch to `A/B 策略对比`, run `no_response` vs `content_removal_with_explanation`, and export again.
7. Confirm the report includes `Visibility Intervention Tradeoff` when visibility metrics are available.
8. Confirm A/B reports include risk, negative ratio, polarization, trust recovery, attention level, and backlash-risk comparison fields when available.
9. Confirm the report says real-world actions require human review and policy/legal review.
10. Confirm the report does not show raw JSON, API keys, `.env` values, raw prompts, raw user content, named-user target lists, account-level influenceability scores, or automatic action-execution instructions.

Safety checks:

- Forbidden options must not appear: `fake_consensus`, `bot_amplification`, `fake_event`, `deceptive_distraction`, `covert_influencer_seeding`, `targeted_persuasion`, or `suppression`.
- The page must not include real API toggles, real LLM toggles, API key inputs, live fetch controls, or profile-modification controls.
- The page must not output individual targeting recommendations or account-level influenceability scores.
- The page should use only `GET /api/v1/simulation/ethics-policy`, `GET /api/v1/simulation/demo-scenario`, and `POST /api/v1/simulation/run`.
- The ethics-policy text may mention forbidden categories as policy language; those categories must not appear as selectable intervention options.

Case-to-simulation initialization demo steps:

1. Create and run a case from the `Cases` page, or use the local seed script if demo cases already exist.
2. Open `Simulation Lab / 舆情预演沙盘`.
3. In `从案例初始化沙盘`, select a completed case or enter its `case_id`, for example `case_001`.
4. Click `预览初始化`.
5. Confirm the summary shows `事件框体`, `子议题`, `人群分布`, `普通公众基线`, `回音壁偏差`, `策略提示`, and any `数据不足` warnings.
6. Confirm the safety copy says `仅基于聚合数据，不生成个体操控建议`.
7. Click `从案例初始化沙盘`.
8. Confirm the bubble canvas switches from the generic demo to a case-derived synthetic scenario.
9. Click `运行模拟` or switch to `A/B 策略对比` and compare allowed interventions.
10. Confirm no real API/LLM calls are made, no live fetch is enabled, and no account-level targeting fields appear.

Endpoint checks:

```cmd
powershell -Command "Invoke-RestMethod http://127.0.0.1:8000/api/v1/cases/case_001/simulation/initialization-preview | ConvertTo-Json -Depth 10"
powershell -Command "Invoke-RestMethod -Method Post http://127.0.0.1:8000/api/v1/cases/case_001/simulation/initialize | ConvertTo-Json -Depth 10"
```

Case-to-simulation QA checklist:

- Confirm `sub_issues` include both `topic_risk_score` and `risk_score`.
- Confirm `observed_frame_profile` includes aggregate `harm_salience`, `loss_sensitivity`, `moral_outrage_sensitivity`, and `crisis_legitimacy_pressure`.
- Confirm positive-skewed, polarized, insufficient-data, and manipulation-suspected cases are classified as aggregate frame states, not individual targeting guidance.
- Confirm the response contains no `target_accounts`, `author_id`, `author_name`, `influenceability_score`, or automatic action execution fields.
- Confirm strategy implications remain human-review-oriented and do not expose forbidden manipulation options as case-initialization guidance.
