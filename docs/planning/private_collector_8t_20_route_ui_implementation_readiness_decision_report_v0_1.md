# Private Collector 8T-20 Route/UI Implementation Readiness Decision Report v0.1

## A. Decision / Status

```text
phase = 8T-20
task = route_ui_implementation_readiness_decision_docs_only
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
persistent_staging_storage_created = no
route_enabled_by_default = no
enabled_mode_test_only = yes
auth_implemented = no
local_only_runtime_implemented = no
route_methods = GET only
```

Decision fields:

```text
route_implementation_approved_now = no
ui_implementation_approved_now = no
auth_implementation_approved_now = no
storage_implementation_approved_now = no
evidence_row_preview_approved_now = no
production_import_approved_now = no
recommended_next_state = ready_for_8T_21_route_ui_safety_test_plan_docs_only_or_source_patch
```

## B. Inputs from 8T-17

8T-17 established:

- Route skeleton milestone accepted after enabled synthetic fixture smoke.
- Disabled smoke passed.
- Enabled synthetic fixture smoke passed.
- Route still disabled by default.
- Enabled mode still synthetic/test-only.
- No real package reads.
- No evidence row parsing.
- No storage.
- No production import.
- No UI.
- No collector runtime integration.

The route skeleton is accepted as a governance checkpoint, not as implementation approval.

## C. Inputs from 8T-18

8T-18 established:

- Future operator access must be local-only / internal-only.
- No anonymous access.
- No public access.
- No customer access.
- No provider direct access.
- No private collector direct access.
- Auth/local-only is contract-only.
- No auth implementation.
- No local-only runtime implementation.
- Route still disabled by default.

The auth/local-only contract is enough to guide future planning, but it is not a runtime implementation.

## D. Inputs from 8T-19

8T-19 established:

- Future UI must be internal-only / local-only.
- Future UI can only display safe metadata.
- Future UI must not display raw rows, raw comments, raw identifiers, secrets, or absolute paths.
- Future UI must not include active production/public actions.
- No UI implementation yet.

The UI contract is enough to guide future safety test planning, but it is not frontend implementation approval.

## E. Readiness Decision

Current readiness decision:

- Not ready for UI implementation now.
- Not ready for auth/local-only runtime implementation now.
- Not ready for persistent storage now.
- Not ready for evidence row preview now.
- Not ready for production import now.
- Not ready for public / C-end / B-end route now.
- Not ready for collector runtime / API bridge now.

The contracts are now good enough to plan a future implementation slice, but they are not themselves approval to implement.

Any implementation after this point requires a separate explicit user approval and a narrower test/safety plan.

## F. Allowed Next Gates

Allowed next steps:

1. 8T-21 route/UI safety test plan docs-only.
2. 8T-21 first implementation slice design docs-only.
3. ChatGPT-side Source patch for 8T-18 / 8T-19 / 8T-20, likely Source 05 and Source 11 only.

Do not recommend direct implementation yet.

## G. Forbidden Next Steps

Forbidden next steps:

- Direct UI implementation.
- Direct route behavior expansion.
- Route default enabled.
- Auth implementation without test plan.
- Persistent staging storage.
- Evidence row preview.
- Production Evidence import.
- Evidence Layer write.
- Production case.
- `analysis_run`.
- Report runtime.
- Sandbox / public event runtime.
- Public / C-end / B-end / customer route.
- Collector runtime / API bridge.
- Real API / real LLM.
- URL fetch / scrape.

## H. Files Changed

- `docs/planning/private_collector_8t_20_route_ui_implementation_readiness_decision_report_v0_1.md`
- `docs/architecture/internal_operator_route_ui_readiness_matrix_v0_1.md`
- `docs/architecture/internal_operator_future_implementation_slice_options_v0_1.md`

## I. Validation

Run for this docs-only phase:

```text
git diff --check
git status --short
```

Do not run backend tests, frontend build, browser smoke, or collector because this is docs-only unless code is accidentally changed.

## J. Issues

### P0 Privacy / Safety

No P0 issue identified.

The decision explicitly rejects UI/runtime/storage/import/evidence-row-preview implementation in this phase.

### P1 Readiness Blocker

No P1 blocker for a docs-only readiness decision.

There is a blocker for implementation: no route/UI safety test plan exists yet.

### P2 Non-blocking Limitation

- Route safety test plan remains needed.
- Auth/local-only runtime remains not implemented.
- UI remains not implemented.
- Persistent staging storage remains not implemented.
- Evidence row preview and production import remain blocked.

These limitations are intentional and keep the project in a governance-first posture.

### P3 Nice-to-have

- Small Source patch after user approval.
- Future route/UI implementation slice design doc.
- Future frontend safety test checklist if UI is later approved.

## K. Source Update Policy

No immediate Project Source update unless the user requests a small patch.

Do not create Source files in the repository.
Do not create `docs/project_sources`.

## L. Recommended Next Step

Primary recommendation:

Phase 8T-21 route/UI safety test plan docs-only.

Alternative:

ChatGPT-side Source patch for 8T-18 / 8T-19 / 8T-20, likely Source 05 and Source 11 only.

## M. Safety Confirmations

- No backend code changed.
- No frontend code changed.
- No tests changed.
- No runtime code changed.
- No backend route added.
- No frontend UI added.
- No UI implemented.
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
