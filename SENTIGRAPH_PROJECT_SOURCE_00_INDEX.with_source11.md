# Sentigraph Project Source 00 Index with Source 11

Update date: 2026-06-18

Nature: Index copy that adds Source 11. This file does not replace any existing Source 00-10 files.

## Current Baseline

Sentigraph is a public-opinion evidence analysis system with a conservative, evidence-first architecture. The current local repository includes a mock/offline-first product surface, optional YouTube public-data demo path, CSV/Excel/manual evidence flows, source catalog and feasibility docs, trust/dedup/review/audit governance, C-end public event demos, B-end report samples, and Phase 6 file-based Analysis Request / Provider Handoff / Import Governance status.

The project must keep these boundaries explicit:

- Sentigraph is not a full-web crawler.
- Sentigraph does not perform unauthorized scraping.
- Sentigraph does not use cookies, login sessions, captcha bypass, anti-bot bypass, proxy evasion, or private data collection.
- Search Discovery, RSS, and GDELT are mock/static unless a future source says otherwise.
- Vendor POC is offline sample mapping unless a future source says otherwise.
- Provider output is evidence, not official truth.
- Evidence Scale / Coverage is imported/available evidence coverage, not full-web or full-platform coverage.
- MediaCrawler is not integrated.
- OpenClaw is external manual assistance only, not production ingestion.
- The LLM provider remains mock unless a future source says otherwise.

## Source List

1. `SENTIGRAPH_PROJECT_SOURCE_00_INDEX.md`  
   Baseline index and source map, if present in the project source bundle.

2. `SENTIGRAPH_PROJECT_SOURCE_01_FOUNDATION.md`  
   Product foundation, project purpose, and core boundaries, if present in the project source bundle.

3. `SENTIGRAPH_PROJECT_SOURCE_02_BACKEND_AND_ANALYSIS.md`  
   Backend and deterministic analysis state, if present in the project source bundle.

4. `SENTIGRAPH_PROJECT_SOURCE_03_FRONTEND_AND_DEMO.md`  
   Frontend pages, demo flows, and UI status, if present in the project source bundle.

5. `SENTIGRAPH_PROJECT_SOURCE_04_EVIDENCE_LAYER.md`  
   Evidence ingestion, trust, review, and import state, if present in the project source bundle.

6. `SENTIGRAPH_PROJECT_SOURCE_05_SOURCE_CATALOG_AND_SEARCH_DISCOVERY.md`  
   Source catalog, feasibility matrix, search discovery, RSS/GDELT mock provider status, if present in the project source bundle.

7. `SENTIGRAPH_PROJECT_SOURCE_06_VENDOR_AND_WEBSITE.md`  
   Vendor POC, website, policy, and operation guide status, if present in the project source bundle.

8. `SENTIGRAPH_PROJECT_SOURCE_07_OPINION_ECOSYSTEM_RESEARCH.md`  
   Opinion ecosystem research, mapping, and sandbox-facing research state, if present in the project source bundle.

9. `SENTIGRAPH_PROJECT_SOURCE_08_OPINION_ECOSYSTEM_SANDBOX_AND_PUBLIC_EVENT.md`  
   Opinion Ecosystem Sandbox, public event, and related demo state, if present in the project source bundle.

10. `SENTIGRAPH_PROJECT_SOURCE_09_C_END_PUBLIC_EVENT_PLATFORM.md`  
    C-end public event platform planning or implementation state, if present in the project source bundle.

11. `SENTIGRAPH_PROJECT_SOURCE_10_C_END_B_END_DEMO_AND_REPORT_STATUS.md`  
    C-end public event platform, Helldivers / Dong-Sun demos, Sandbox V2, B-end report samples, LLM semantic annotation docs, professional mock/source labeling, and B-end report export docs, if present in the project source bundle.

12. `SENTIGRAPH_PROJECT_SOURCE_11_ANALYSIS_REQUEST_PROVIDER_HANDOFF_AND_IMPORT_GOVERNANCE_STATUS.md`  
    Phase 6 Analysis Request, Provider Handoff, Import Governance, manual review gates, dry-run import job, execution preflight, and synthetic row-reader dry-run status patch.

## Source 11 Addition Summary

Source 11 records Phase 6A-L status:

- Analysis Request file-based MVP.
- Private collector file adapter boundary.
- Cross-project file handshake and schema compatibility fix.
- Case Draft Handoff.
- Evidence Import Plan.
- Metadata-only Import Preview.
- Human Review Decision Record.
- Dry-run Import Job Gate.
- Execution Preflight.
- Synthetic Fixture Row Reader Dry-Run.

Source 11 also records that the Phase 6 chain still does not:

- run collectors
- call real APIs
- fetch URLs
- scrape websites
- read real package evidence rows
- import evidence rows
- write the Evidence Layer
- create production cases
- create review queue items
- run dedup
- generate analysis
- generate Sandbox fixtures
- generate reports

## Current Implementation State Update

Current implementation state now includes the Phase 6 local file handoff chain:

Analysis Request -> Provider Result -> Case Draft Handoff -> Evidence Import Plan -> Import Preview -> Human Review Decision -> Dry-run Import Job -> Execution Preflight -> Synthetic Row Reader Dry-Run.

This is a governance and preflight subsystem. It is not a live provider, not an import runtime, and not a production evidence ingestion adapter.

## Current Ready State

Decision:

- `ready_for_phase_6M_real_package_row_preview_design`

Recommended next step:

- Design Phase 6M real package row preview first, before any runtime that reads real package rows.

Phase 6M design should require:

- explicit human opt-in
- tiny redacted sample only
- `max_rows=20`
- read-only behavior
- privacy stop
- quarantine
- no import
- no Evidence Layer write
- no case creation
- no analysis

## Commit Guidance

Recommended commit message:

- `Add Source 11 analysis request provider handoff status`

Recommended tag:

- No tag needed.
