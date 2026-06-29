# Private Collector 8T-22 First Implementation Slice Design Report v0.1

## A. Decision / Status

```text
phase = 8T-22
task = first_implementation_slice_design_docs_only
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
ui_implemented = no
test_implemented = no
persistent_staging_storage_created = no
route_enabled_by_default = no
enabled_mode_test_only = yes
auth_implemented = no
local_only_runtime_implemented = no
route_methods = GET only
```

Decision fields:

```text
first_implementation_slice_selected = test_only_safety_contract_implementation
test_implementation_approved_now = no
route_implementation_approved_now = no
ui_implementation_approved_now = no
auth_implementation_approved_now = no
storage_implementation_approved_now = no
evidence_row_preview_approved_now = no
production_import_approved_now = no
recommended_next_state = ready_for_8T_23_test_only_safety_contract_implementation_or_source_patch
```

## B. What This Phase Decides

- The safest future first implementation slice is tests-only.
- No route/runtime/UI/auth/storage/import implementation is approved.
- 8T-23 may implement targeted tests only if the user explicitly approves.
- The future tests-only slice must not change backend runtime behavior.
- The future tests-only slice must not change frontend UI.
- The future tests-only slice must not read real package directories, private collector export roots, or evidence row files.

## C. What This Phase Does Not Do

- No test implementation.
- No backend implementation.
- No frontend implementation.
- No route behavior change.
- No auth implementation.
- No authorization implementation.
- No local-only runtime.
- No UI.
- No storage.
- No evidence row preview.
- No production import.
- No Evidence Layer write.
- No production case / `analysis_run`.
- No collector runtime integration.
- No public / C-end / B-end route.

## D. Files Changed

- `docs/architecture/internal_operator_first_implementation_slice_design_v0_1.md`
- `docs/architecture/internal_operator_test_only_first_slice_contract_v0_1.md`
- `docs/planning/private_collector_8t_22_first_implementation_slice_design_report_v0_1.md`

## E. Validation

Run for this docs-only phase:

```text
git diff --check
git status --short
```

Do not run backend tests, frontend build, browser smoke, or collector because this is docs-only unless code is accidentally changed.

## F. Issues

### P0 Privacy / Safety

No P0 issue identified.

The design chooses tests-only as the future first implementation slice and blocks route/UI/auth/storage/import work.

### P1 Slice-design Blocker

No P1 slice-design blocker identified.

The design identifies the safest future first slice and documents prerequisites, stop rules, validation commands, and non-goals.

### P2 Non-blocking Limitation

- Tests are not implemented in this phase.
- Route/UI/auth runtime is not implemented.
- UI remains not implemented.
- Persistent staging storage remains blocked.
- Evidence row preview remains blocked.
- Production import remains blocked.

These limitations are intentional.

### P3 Nice-to-have

- A small Source patch if the user wants current context updated.
- A future exact test implementation prompt for 8T-23.
- A future test fixture naming convention note.

## G. Recommended Next Step

Primary recommendation:

Phase 8T-23 test-only safety contract implementation, only after explicit user approval.

Alternative:

ChatGPT-side Source patch for 8T-18 / 8T-19 / 8T-20 / 8T-21 / 8T-22, likely Source 05 and Source 11 only.

Do not recommend:

- Direct route implementation.
- UI implementation.
- Auth runtime.
- Persistent storage.
- Production import.
- Evidence row preview.
- Evidence Layer write.
- Production case.
- `analysis_run`.
- Report runtime.
- Sandbox / public event runtime.
- Public / C-end / B-end route.
- Collector runtime / API bridge.

## H. Source Update Policy

No immediate Project Source update unless the user requests a small patch.

Do not create Source files in the repository.
Do not create `docs/project_sources`.

## I. Safety Confirmations

- No backend code changed.
- No frontend code changed.
- No tests changed.
- No runtime code changed.
- No backend route added.
- No frontend UI added.
- No UI implemented.
- No test implemented.
- No route behavior changed.
- Route remains disabled by default.
- Enabled mode remains synthetic/test-only.
- Route remains GET-only.
- No auth implementation.
- No authorization implementation.
- No local-only runtime implementation.
- No sessions / tokens / cookies added.
- No persistent staging storage created.
- No Evidence Layer write.
- No production case created.
- No production `analysis_run` created.
- No report runtime generated.
- No Sandbox / public event runtime generated.
- No public event page generated.
- No response text or generated public message generated.
- No publish / send / post / execute behavior implemented.
- No public / C-end / B-end / customer route exposed.
- No collector run.
- No live crawl.
- No real API called.
- No real LLM called.
- No URL fetching.
- No scraping.
- No private collector export root read.
- No real package directories read.
- No `evidence_items.jsonl` parsed or opened.
- No `evidence_items.csv` parsed or opened.
- No evidence row files opened.
- No Project Source modified in repo.
- No Source files created in repo.
- No `docs/project_sources` created.
- No GitHub Actions workflow recreated.
