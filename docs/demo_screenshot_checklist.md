# Sentigraph v6.27 Demo Screenshot Checklist

Last updated: 2026-05-26

Use this checklist with [demo_asset_package_v6_27.md](demo_asset_package_v6_27.md). Capture the screens manually after running local validation. Do not show secrets, private data, `.env` files, terminal output containing credentials, or browser tabs with private content.

## Required Screenshot Assets

| # | File name | Screen |
| --- | --- | --- |
| 1 | `01_dashboard_overview.png` | Dashboard overview |
| 2 | `02_platform_source_catalog.png` | Source Catalog / Platform Integration Overview |
| 3 | `03_youtube_real_flow_optional.png` | Keyword Search / YouTube real flow, if available |
| 4 | `04_cases_page.png` | Cases page |
| 5 | `05_csv_excel_evidence_import.png` | CSV/Excel Evidence Import |
| 6 | `06_manual_url_evidence.png` | Manual URL Evidence |
| 7 | `07_search_discovery_mock_review.png` | Search Discovery mock candidate review |
| 8 | `08_rss_gdelt_mock_provider_selector.png` | RSS/GDELT mock provider selector |
| 9 | `09_evidence_trust_dedup_fields.png` | Evidence Trust / Dedup fields |
| 10 | `10_evidence_review_queue.png` | Evidence Review Queue |
| 11 | `11_review_audit_timeline.png` | Review Audit Timeline |
| 12 | `12_evidence_scale_coverage.png` | Evidence Scale / Coverage |
| 13 | `13_analysis_result.png` | Analysis Result |
| 14 | `14_summary_report.png` | Summary Report |
| 15 | `15_propagation_graph.png` | Propagation Graph |
| 16 | `16_risk_monitor_forecast.png` | Risk Monitor / Forecast |
| 17 | `17_simulation_lab_initialized.png` | Simulation Lab initialized from case |
| 18 | `18_ab_strategy_comparison.png` | A/B Strategy Comparison |
| 19 | `19_strategy_report_export.png` | Strategy Report Export |
| 20 | `20_benchmarks.png` | Benchmarks |
| 21 | `21_llm_safety.png` | LLM Safety |

## Screenshot Success Signs

- YouTube raw-data screenshots, if captured, show `Data: YouTube Real`, `Analysis: Offline`, and `LLM: Mock`.
- Evidence-only cases do not say YouTube Real.
- CSV/Excel screenshots show user-upload or uploaded-dataset wording.
- Manual URL Evidence screenshots state that the system does not fetch URL content.
- Search Discovery, RSS Mock, and GDELT Mock screenshots show mock/static, metadata-only, no-live-fetch labels.
- Evidence Trust screenshots show provenance, trust label, verification status, duplicate indicator, or risk flags.
- Review Queue screenshots show human-review controls and do not imply AI authenticity verification.
- Audit Timeline screenshots show review history as decision records, not platform verification.
- Evidence Scale / Coverage screenshots include the coverage limitation note.
- Summary/Analysis screenshots show `analysis_input_source` and evidence caveats where relevant.
- Simulation screenshots do not imply real-world execution.
- LLM Safety screenshots show mock provider boundary.

## Pre-Capture Validation

Run from repository root:

```powershell
python -m pytest
python scripts/run_offline_benchmarks.py
npm --prefix frontend run build
```

## Capture Safety Checklist

- Hide `.env`.
- Hide terminal panes with API keys or shell history containing secrets.
- Do not show private user data.
- Use mock/static samples unless intentionally recording the optional YouTube real path.
- If using YouTube real data, show only public comments and avoid sensitive personal information.
- Do not start real RSS/GDELT/search/Douyin/Bilibili providers.
- Do not fetch candidate URLs or scrape websites.
- Do not imply full-web capture, guaranteed predictions, AI authenticity verification, or real-world action execution.
