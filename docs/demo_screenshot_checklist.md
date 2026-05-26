# Sentigraph v6.26 Demo Screenshot Checklist

Last updated: 2026-05-26

Use this list for the final screenshot package. Capture evidence boundaries clearly: optional real YouTube data, offline deterministic analysis, mock/static Search Discovery and RSS/GDELT providers, mock LLM, and pending real platform integrations.

## Required Sequence

1. Dashboard showing current case status and navigation.
2. Keyword Search showing the explicit YouTube real-data flow.
3. Keyword Search warning for non-YouTube multi-platform mock mode, if useful.
4. Cases page showing a completed YouTube real-data case, if local YouTube key is configured.
5. Cases page showing CSV/Excel Evidence Import and template download.
6. CSV/Excel preview showing normalized evidence rows.
7. CSV/Excel import result showing `evidence_count > 0` and `acquisition_mode=user_upload`.
8. Manual URL Evidence form showing no-fetch/no-scrape safety text.
9. Manual evidence result showing latest attached evidence and `acquisition_mode=manual_url`.
10. Evidence Trust / Provenance section showing trust label, verification status, and risk flags.
11. Evidence Review Queue showing low/unverified evidence.
12. Evidence Review Audit Timeline showing a decision history event.
13. Evidence Scale / Coverage showing total, unique, duplicate, distributions, latest jobs, and coverage note.
14. Search Discovery page with provider selector set to Mock Static.
15. Search Discovery page with provider selector set to RSS Mock.
16. Search Discovery page with provider selector set to GDELT Mock.
17. Search Discovery candidate attachment result showing review-needed warning.
18. Analysis Result showing `analysis_input_source` and low-trust/unverified evidence caveat.
19. Summary Report showing representative evidence and Markdown export control.
20. Propagation Graph, if included in the recording path.
21. Risk Monitor / Forecast showing offline deterministic forecast.
22. Simulation Lab initialized from a case.
23. Simulation Lab A/B strategy comparison.
24. Strategy report export screen or result.
25. Benchmark Dashboard.
26. LLM Safety showing mock provider boundary.
27. Platform Integration Overview showing YouTube real-capable and Douyin/Bilibili pending.
28. Source Catalog / Feasibility Matrix view, if exposed in the UI.

## Success Signs

- YouTube real-data screenshots show `Data: YouTube Real`, `Analysis: Offline`, and `LLM: Mock` only for raw YouTube cases.
- Evidence-based cases do not claim YouTube Real unless raw YouTube data was used.
- Search Discovery and RSS/GDELT providers are labeled mock/static and metadata-only.
- Evidence Scale / Coverage says coverage is imported/available evidence, not full-platform capture.
- Review UI makes it clear that screenshots and transcriptions are not automatically verified.
- Rejected evidence is shown as excluded from analysis by default.
- No API keys, tokens, cookies, `.env` values, or raw secret fields appear.

## Pre-Capture Validation

Run from repository root:

```powershell
python -m pytest
python scripts/run_offline_benchmarks.py
npm --prefix frontend run build
```

Do not start real RSS/GDELT/search/Douyin/Bilibili integrations for the screenshot package. The optional YouTube real-data path may be recorded only from a locally configured environment and should not be exercised by automated tests.
