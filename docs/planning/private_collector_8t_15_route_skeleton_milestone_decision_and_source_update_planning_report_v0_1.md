# Private Collector 8T-15 Route Skeleton Milestone Decision and Source Update Planning Report v0.1

## A. Decision / Status

```text
phase = 8T-15
task = route_skeleton_milestone_decision_and_source_update_planning
privacy_issue_stop = no
docs_only = yes
code_changed = no
tests_changed = no
runtime_code_changed = no
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
route_enabled_by_default = no
route_methods = GET only
```

Decision:

```text
route_skeleton_milestone_status = accepted
ready_for_source_update_planning = yes
ready_for_enabled_fixture_smoke = yes, but only as test/readiness checkpoint
ready_for_ui_implementation = no
ready_for_persistent_storage = no
ready_for_production_import = no
ready_for_evidence_row_preview = no
```

## B. What 8T-13 Established

Phase 8T-13 established the first tiny internal operator route skeleton:

- Backend-only route skeleton.
- GET-only route surface.
- Disabled by default.
- Safe `route_disabled` response when disabled.
- Synthetic fixture-only enabled mode.
- No UI.
- No persistent staging storage.
- No production import.
- No Evidence Layer write.
- No production case.
- No `analysis_run`.

The route skeleton is an internal operator readiness surface, not a collector integration and not an ingestion product feature.

## C. What 8T-14 Established

Phase 8T-14 established disabled-mode smoke coverage:

- Disabled default smoke passed.
- Falsey environment value smoke passed.
- No `evidence_items.jsonl` opening.
- No `evidence_items.csv` opening.
- Safe error body.
- GET-only route surface.
- No public / C-end / B-end alias.
- No `FileResponse`.
- No `StreamingResponse`.
- No ZIP generation.
- No public URL generation.
- No signed URL generation.
- No external delivery.

8T-14 confirmed that the route remains safe while disabled and that it does not expose raw file paths, raw metadata, evidence row content, or private collector internals.

## D. Milestone Decision

The 8T-13 / 8T-14 route skeleton milestone is accepted as a completed route skeleton checkpoint.

```text
route_skeleton_milestone_status = accepted
ready_for_source_update_planning = yes
ready_for_enabled_fixture_smoke = yes, but only as test/readiness checkpoint
ready_for_ui_implementation = no
ready_for_persistent_storage = no
ready_for_production_import = no
ready_for_evidence_row_preview = no
```

This acceptance means only that the disabled-by-default backend route skeleton and its disabled-mode smoke are now stable enough to document in project context. It does not approve UI, persistent storage, production import, real package row preview, Evidence Layer write, production case creation, analysis run creation, report runtime, Sandbox runtime, public event runtime, or external delivery.

## E. Source Update Planning

Do not create Source files in the repository.
Do not modify Project Source in the repository.

Candidate ChatGPT-side Source update list:

- `SENTIGRAPH_PROJECT_SOURCE_00_INDEX_8T_10_UPDATED.md`
- `SENTIGRAPH_PROJECT_SOURCE_01_CURRENT_STATE_8T_10_UPDATED.md`
- `SENTIGRAPH_PROJECT_SOURCE_02_DATA_AND_EVIDENCE_ARCHITECTURE_8T_10_UPDATED.md`
- `SENTIGRAPH_PROJECT_SOURCE_03_SOURCE_VENDOR_COMPLIANCE_STRATEGY_8T_10_UPDATED.md`
- `SENTIGRAPH_PROJECT_SOURCE_05_ROADMAP_AND_REPLACE_TRIGGERS_8T_10_UPDATED.md`
- `SENTIGRAPH_PROJECT_SOURCE_11_ANALYSIS_REQUEST_PROVIDER_HANDOFF_AND_IMPORT_GOVERNANCE_STATUS_8T_10_UPDATED.md`

Conceptual Source update notes for each candidate:

### SENTIGRAPH_PROJECT_SOURCE_00_INDEX_8T_10_UPDATED.md

- Add 8T-13 / 8T-14 / 8T-15 as the current internal operator route skeleton milestone.
- Note that the route skeleton exists.
- Note that disabled-mode smoke passed.
- Note that the route remains disabled by default and GET-only.
- Note that the enabled mode is synthetic / test-only.
- Note that there is no UI, no persistent storage, no Evidence Layer write, no production case, no `analysis_run`, no production import, no evidence row parsing, and no public / C-end / B-end route.

### SENTIGRAPH_PROJECT_SOURCE_01_CURRENT_STATE_8T_10_UPDATED.md

- Update current state to include the internal operator read-only staging route skeleton.
- Make clear that the route is disabled by default.
- Make clear that the route is GET-only.
- Make clear that the route is not an ingestion feature yet.
- Preserve the current boundary that production import and evidence row preview remain blocked.

### SENTIGRAPH_PROJECT_SOURCE_02_DATA_AND_EVIDENCE_ARCHITECTURE_8T_10_UPDATED.md

- Add the internal operator route skeleton as a pre-ingestion governance checkpoint.
- State that it does not write Evidence Layer records.
- State that it does not create a production case, review queue, dedup run, analysis run, report, Sandbox fixture, or public event page.
- State that no evidence row parsing is approved by this milestone.

### SENTIGRAPH_PROJECT_SOURCE_03_SOURCE_VENDOR_COMPLIANCE_STRATEGY_8T_10_UPDATED.md

- Clarify that private collector handoff remains local and metadata-governed.
- Clarify that the route skeleton does not make the private collector a Sentigraph internal crawler.
- Clarify that real collector execution, live crawl, real API calls, cookie/session use, and source bypass remain outside Sentigraph product ingestion.

### SENTIGRAPH_PROJECT_SOURCE_05_ROADMAP_AND_REPLACE_TRIGGERS_8T_10_UPDATED.md

- Mark route skeleton milestone as accepted.
- Keep next steps gated:
  - ChatGPT-side Source update.
  - Enabled synthetic fixture smoke / readiness checkpoint.
  - Operator route auth / local-only contract docs.
- Do not schedule UI, persistent storage, production import, or evidence row preview as automatic next steps.

### SENTIGRAPH_PROJECT_SOURCE_11_ANALYSIS_REQUEST_PROVIDER_HANDOFF_AND_IMPORT_GOVERNANCE_STATUS_8T_10_UPDATED.md

- Add route skeleton status under provider handoff / import governance context.
- State that 8T-13 route skeleton now exists.
- State that 8T-14 disabled-mode smoke passed.
- State that the route remains disabled by default and GET-only.
- State that enabled fixture mode is synthetic / test-only.
- State that there is no UI, no persistent staging storage, no Evidence Layer write, no production case, no `analysis_run`, no production import, no evidence row parsing, and no public / C-end / B-end route.

## F. Recommended Next Step

Primary recommendation:

After commit, ask the user whether to perform a ChatGPT-side batch Project Source update for the 8T-13 / 8T-14 / 8T-15 milestone.

Secondary recommendation if no Source update:

Phase 8T-16 enabled synthetic fixture route smoke / readiness checkpoint, test-only, no UI, no persistent storage, no production import.

Do not recommend:

- UI implementation.
- Persistent storage.
- Production import.
- Evidence row preview.
- Evidence Layer write.
- Production case.
- `analysis_run`.
- Report runtime.
- Sandbox / public event runtime.
- Public / C-end / B-end route.

## G. Issues

### P0 Privacy / Safety

No P0 issue identified.

The milestone remains disabled by default, GET-only, local governance oriented, and does not read full evidence rows or expose private collector internals.

### P1 Milestone Blocker

No P1 milestone blocker identified.

8T-13 created the skeleton and 8T-14 verified disabled-mode safety. 8T-15 can accept the milestone as documentation/planning state.

### P2 Non-blocking Limitation

- No enabled synthetic fixture smoke milestone has been completed yet.
- No auth / local-only operator contract has been finalized beyond current disabled-route behavior.
- No UI contract exists for the internal operator route.

These are expected limitations, not blockers.

### P3 Nice-to-have

- A compact Source update diff plan after user approval.
- A later operator route boundary diagram.
- A later local-only auth / operator role wording note.

## H. Safety Confirmations

- No backend code changed.
- No frontend code changed.
- No tests changed.
- No runtime code changed.
- No backend route added.
- No route behavior changed.
- Route remains disabled by default.
- Route remains GET-only.
- No persistent staging storage created.
- No Evidence Layer write.
- No production case created.
- No production `analysis_run` created.
- No report runtime generated.
- No Sandbox / public event runtime generated.
- No response text or generated public message generated.
- No publish / send / post / execute behavior implemented.
- No collector run.
- No live crawl.
- No real API called.
- No real LLM called.
- No URL fetching.
- No scraping.
- No private collector export root read.
- No real package directories read.
- No `evidence_items.jsonl` parsed.
- No `evidence_items.csv` parsed.
- No evidence row files opened.
- No Project Source modified.
- No Source update files created in repo.
- No GitHub Actions workflow recreated.
