# Screenshot Capture Report

Status: local browser screenshot QA report only. No backend code, frontend product behavior, collector job, Evidence Layer write, production case, analysis run, report runtime, Sandbox runtime, public URL, signed URL, or external delivery was created.

## Capture Metadata

- Capture date/time: 2026-06-24 23:14:43 +08:00
- Environment: local Windows workspace, Vite frontend dev server
- Frontend URL: `http://127.0.0.1:5173/`
- Screenshot folder: `docs/demo/assets/second_round_playtest_package/`
- Screenshot count: 12 PNG files
- Total PNG size: 2,079,550 bytes
- Video output: not produced; recording remains manual-only

## Validation Summary

- `npm.cmd --prefix frontend run build`: passed
- Browser/local smoke: passed for required routes
- Optional governance route: skipped for screenshot capture because local backend was not running and the page showed a visible 500 marker
- Console errors/warnings on captured routes: none observed
- Visible bad markers on captured routes: no `[object Object]`, no `undefined`, no `NaN`, no visible `Request failed with status code 500`

## Route Results

| Route | Status | Notes |
| --- | --- | --- |
| `/#/demo` | pass | Guided demo page opened; local demo and no-live-fetch context visible. |
| `/#/public-events` | pass | Event Plaza opened; not treated as real hotlist. |
| `/#/public-events/donglu-sunjihai-youth-football` | pass | Dong/Sun event detail opened; sample and boundary sections visible across captures. |
| `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` | pass | Dong/Sun sample selected; V2 ecology view, T0-T6 controls, PeopleCluster / InfluenceCore context visible. |
| `/#/reports/donglu-sunjihai-youth-football-sample` | pass | B-end report sample opened; coverage, response tempo, and boundary sections captured. |
| `/#/analysis-requests` | skipped | Optional technical-governance route showed visible 500 marker without local backend. No screenshot captured. |

## Screenshot Results

| File | Status | QA Notes |
| --- | --- | --- |
| `01_demo_home.png` | captured | Demo guide visible; no bad markers. |
| `02_public_events_plaza.png` | captured | Event Plaza visible; no bad markers. |
| `03_dong_sun_event_detail_top.png` | captured | Dong/Sun detail top visible; no bad markers. |
| `04_dong_sun_evidence_summary.png` | captured | Event detail context captured as full-page support image. |
| `05_dong_sun_sandbox_entry_cta.png` | captured | Event detail CTA context captured as full-page support image. |
| `06_dong_sun_sandbox_v2_overview.png` | captured | V2 ecology view, timeline controls, EchoBox area, and boundary chips visible. |
| `07_dong_sun_t0_t6_controls.png` | captured | T0-T6 controls visible; no bad markers. |
| `08_marker_peoplecluster_boundary.png` | captured | Sandbox marker / aggregate group context visible; no bad markers. |
| `09_dong_sun_b_end_report_hero.png` | captured | B-end report sample hero and boundary chips visible. |
| `10_report_evidence_coverage.png` | captured | Executive summary and coverage area visible. |
| `11_report_response_tempo.png` | captured | Response tempo / event lifecycle context visible. |
| `12_report_boundaries.png` | captured | Report export planning and human review / boundary section visible. |
| `optional_13_analysis_requests_governance_boundary.png` | skipped | Optional route showed visible 500 marker without backend. |

## Boundary Copy Results

Visible or documented in the package:

- not crawler
- not full-web
- not live platform monitor
- not real hotlist
- not official verification
- not causal proof
- no real API / LLM
- no real request / vote / support / sponsorship
- PeopleCluster / InfluenceCore distinction
- Local Exchange Reader is disabled-by-default metadata-only scaffold, not real private collector integration

## Issues / Follow-Up

- `/#/analysis-requests` should only be captured in this package when a safe local backend is running. It was intentionally skipped here to avoid including a visible 500 state in demo assets.
- `04_dong_sun_evidence_summary.png` and `05_dong_sun_sandbox_entry_cta.png` are broad support captures from the same event detail page; for a polished deck, consider manual cropping around the exact evidence summary and CTA blocks.

## Safety Notes

- No private collector directory was touched.
- No collector job was run.
- No real exchange dirs were configured or read.
- No `evidence_items.jsonl` or `evidence_items.csv` files were parsed.
- No Evidence Layer write, production case, analysis run, report runtime, Sandbox runtime, public event runtime, public URL, signed URL, or download route was created.
- No real API, real LLM, external URL fetch, scraping, cookies, sessions, browser profiles, tokens, API keys, or secrets were used.
