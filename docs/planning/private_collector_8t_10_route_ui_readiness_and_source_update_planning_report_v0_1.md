# Private Collector 8T-10 Route/UI Readiness and Source Update Planning Report v0.1

## A. Decision / Status

```text
phase = 8T-10
task = route_ui_readiness_decision_and_batch_source_update_planning
privacy_issue_stop = no
code_changed = no
docs_only = yes
collector_run = no
live_crawl = no
real_api_called = no
real_llm_called = no
full_evidence_rows_read = no
evidence_layer_write = no
production_case_created = no
analysis_run_created = no
project_source_changed = no
project_source_files_created_in_repo = no
api_route_added = no
frontend_changed = no
persistent_staging_storage_created = no
```

Decision: ready.

Implementation slice: 8T-10 route/UI readiness decision and batch Source update planning.

## B. What 8T-3 Through 8T-9 Established

The 8T chain established a safe metadata-only private collector handoff path:

- 8T-3 metadata package resolution: resolves local package references using safe metadata and required-file presence.
- 8T-4 provider result metadata reading: reads provider result metadata and builds safe handoff summaries.
- 8T-5 local exchange smoke: proves synthetic fixture-level provider result -> package resolution behavior.
- 8T-6 Search-to-Case contract: defines that search/request handoff cannot skip governance gates.
- 8T-7 review-only staging design: defines metadata handoff -> internal review candidate.
- 8T-8 in-memory staging helper: creates review-only staging candidates and gate summaries without persistence.
- 8T-9 integration smoke: proves provider_result JSON fixture -> local exchange smoke -> review-only staging helper -> safe staging candidate summary.

This establishes readiness to design an internal operator route contract.

It does not establish readiness to implement route/UI/runtime integration.

## C. Route Readiness Decision

Decision:

```text
not_ready_for_route_implementation_yet
ready_for_docs_only_internal_operator_read_only_route_contract
```

Reason:

The route would expose an operator surface. It needs a separate route contract, internal operator boundary, disabled-by-default or local-only configuration decision, safe response schema, and audit behavior before implementation.

The future route must remain read-only and metadata-only unless a later phase explicitly approves otherwise.

## D. UI Readiness Decision

Decision:

```text
not_ready_for_ui_implementation_yet
ready_for_docs_only_operator_review_screen_contract_later
```

Reason:

The UI must wait for a safe route contract and response schema. It must display only safe metadata summaries and review-only actions. It must not show raw evidence rows, raw comments, raw identifiers, absolute paths, response text, production actions, or public actions.

## E. Production Readiness Decision

```text
production_import_ready = no
evidence_layer_write_ready = no
production_case_ready = no
analysis_run_ready = no
report_runtime_ready = no
sandbox_public_event_ready = no
```

Production readiness remains blocked until future explicit gates approve:

- evidence preview
- human review
- dedup
- promotion
- production Evidence import
- production case creation
- analysis run
- report/Sandbox/public event generation

## F. Batch Source Update Planning

Do not create Source files in this repo.

Do not modify Project Source from this repo task.

Candidate ChatGPT-side Project Source files likely needing a batch update after commit:

### SENTIGRAPH_PROJECT_SOURCE_00_INDEX_7T_UPDATED.md

Conceptual update:

- add 8T private collector metadata handoff chain to the index.
- mark 8T-10 as route/UI readiness planning only.
- keep route/UI/runtime production import as not implemented.

### SENTIGRAPH_PROJECT_SOURCE_01_CURRENT_STATE.md

Conceptual update:

- record that the 8T chain now includes metadata-only package resolver, provider result reader, local exchange smoke, review-only staging helper, and integration smoke.
- state no production import, Evidence Layer write, production case, `analysis_run`, route, or UI exists yet.

### SENTIGRAPH_PROJECT_SOURCE_02_DATA_AND_EVIDENCE_ARCHITECTURE.md

Conceptual update:

- add metadata-only local package resolver and review-only staging candidate boundary.
- clarify that review-only staging is metadata handoff, not Evidence Layer import.
- preserve no raw evidence rows, no raw identifiers, no absolute private paths, and no production actions.

### SENTIGRAPH_PROJECT_SOURCE_03_SOURCE_VENDOR_COMPLIANCE_STRATEGY.md

Conceptual update:

- add private collector as local metadata handoff / external evidence provider boundary.
- clarify no collector is integrated as a Sentigraph crawler.
- clarify no live crawl, API bridge, cookies, sessions, or hidden scraping are part of Sentigraph.

### SENTIGRAPH_PROJECT_SOURCE_05_ROADMAP_AND_REPLACE_TRIGGERS.md

Conceptual update:

- add route/UI readiness decision outcome.
- next allowed planning step is internal operator read-only staging route contract docs-only.
- production import remains blocked until later explicit gates.

### SENTIGRAPH_PROJECT_SOURCE_11_ANALYSIS_REQUEST_PROVIDER_HANDOFF_AND_IMPORT_GOVERNANCE_STATUS_7T_UPDATED.md

Conceptual update:

- update provider handoff/import governance with 8T metadata-only chain:
  - package resolver
  - provider result reader
  - local exchange smoke
  - Search-to-Case contract
  - review-only staging design/helper/integration smoke
- emphasize boundaries:
  - no production import
  - no Evidence Layer write
  - no production case
  - no `analysis_run`
  - no route/UI yet
  - no collector execution

## G. Recommended Next Step

Recommended next phase:

```text
Phase 8T-11 internal operator read-only staging route contract docs-only
```

Do not recommend route implementation yet.

Do not recommend UI implementation yet.

Do not recommend production import.

Do not recommend Evidence Layer write, production case creation, `analysis_run`, report runtime, Sandbox/public event runtime, public response, publish/send/post/execute behavior, or collector integration.

## H. Safety / Privacy Confirmations

- docs-only
- no code changed
- no collector run
- no live crawl
- no browser automation
- no real API
- no real LLM
- no URL fetch/scrape
- no full evidence rows parsed
- no `evidence_items.jsonl` parsed
- no `evidence_items.csv` parsed
- no raw comments printed
- no raw author ids/names printed
- no cookies/tokens/sessions/profile paths read
- no Evidence Layer write
- no production case / analysis_run
- no B-end report runtime
- no Sandbox/public event runtime
- no frontend/API route added
- no persistent staging storage
- no Project Source files created in repo
- no GitHub Actions workflow recreated

## I. Issues Found

P0 privacy/safety:

- none.

P1 route/UI readiness blocker:

- route implementation is not approved yet.
- UI implementation is not approved yet.

P2 non-blocking limitation:

- current readiness is fixture-chain and docs-only planning readiness.
- route contract, auth/operator boundary, safe response schema, and audit behavior still need design.

P3 nice-to-have:

- after 8T-11, a separate docs-only UI contract may be useful if route contract remains accepted.
