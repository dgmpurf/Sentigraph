# Private Collector 8T-24 Runtime Slice Decision Report v0.1

## A. Decision / Status

```text
phase = 8T-24
task = runtime_slice_decision_docs_only
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
runtime_implementation_approved_now = no
route_runtime_expansion_approved_now = no
ui_implementation_approved_now = no
auth_runtime_approved_now = no
storage_implementation_approved_now = no
evidence_row_preview_approved_now = no
production_import_approved_now = no
collector_bridge_approved_now = no
future_runtime_candidate_selected = no_behavior_change_route_guard_design_docs_only
recommended_next_state = ready_for_8T_25_no_behavior_change_route_guard_design_docs_only_or_pause
```

Decision: ready

## B. Inputs From 8T-18 Through 8T-23

- 8T-18 accepted auth/local-only contract docs-only.
- 8T-19 accepted internal operator UI contract docs-only.
- 8T-20 rejected direct route/UI/auth/storage/import implementation.
- 8T-21 created route/UI safety test plan docs-only.
- 8T-22 selected tests-only safety contract as first implementation slice.
- 8T-23 implemented tests-only safety contract and targeted validation passed.
- Source 05 / 11 have been patched on the ChatGPT side.

8T-23 validation inputs:

- route/UI safety contract test: 23 passed
- enabled fixture smoke: 13 passed
- disabled smoke: 21 passed
- analysis request golden contracts: 7 passed
- route module py_compile: passed
- git diff --check: passed

## C. Runtime Readiness Decision

The project is not ready to implement runtime expansion in 8T-24.

8T-23 tests increased confidence in the route skeleton boundary, but tests passing is not approval to expand runtime behavior. The route remains disabled by default, enabled mode remains synthetic/test-only, and the current safe next step is either pause or a docs-only guard-design checkpoint.

```text
ready_for_route_runtime_implementation = no
ready_for_ui_implementation = no
ready_for_auth_runtime = no
ready_for_storage = no
ready_for_evidence_row_preview = no
ready_for_production_import = no
ready_for_collector_bridge = no
ready_for_no_behavior_change_design_docs = yes
ready_for_pause = yes
```

## D. Candidate Next Steps

| Candidate | Allowed now? | Docs-only allowed? | Implementation allowed now? | Risk level | Missing prerequisites | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| Pause after 8T-23 safety tests | yes | n/a | n/a | low | none | Allowed. Use if there is no immediate operator-route need. |
| 8T-25 no-behavior-change route guard design docs-only | yes | yes | no | low | none beyond this decision | Recommended if continuing. |
| 8T-25 auth/local-only runtime design docs-only | not preferred now | yes, later | no | medium | accepted guard design, explicit auth design scope | Defer; not the immediate next step. |
| 8T-25 internal operator UI implementation | no | design only later | no | medium/high | explicit UI approval, frontend safety plan, browser smoke plan | Not allowed. |
| 8T-25 route runtime expansion | no | design only later | no | high | accepted no-behavior-change design, explicit runtime approval, test-first plan | Not allowed. |
| 8T-25 persistent staging storage | no | design only later | no | high | storage threat model, retention policy, privacy gate, rollback plan | Blocked. |
| 8T-25 evidence row preview | no | design only later | no | high | row redaction policy, privacy scan, bounded reader design, explicit approval | Blocked. |
| 8T-25 production import | no | design only later | no | very high | Evidence Layer promotion gate, human approval, dedup/review completion, audit policy | Blocked. |
| 8T-25 collector runtime/API bridge | no | design only later | no | very high | provider boundary, auth model, no live collection proof, private collector contract | Blocked. |

Expected conclusions:

- Pause is allowed.
- No-behavior-change route guard design docs-only is allowed and recommended if continuing.
- Auth runtime design may be docs-only later but is not the preferred immediate next step.
- UI implementation is not allowed.
- Route runtime expansion is not allowed.
- Storage, evidence preview, import, and collector bridge remain blocked.

## E. Recommended Path

Primary recommendation:

Phase 8T-25 no-behavior-change route guard design docs-only.

Alternative:

Pause after 8T-23 and avoid further internal operator route work until a real operator need appears.

Do not recommend:

- direct route runtime expansion
- UI implementation
- auth runtime implementation
- persistent storage
- evidence row preview
- production import
- collector runtime/API bridge

## F. What 8T-25 May Design, If Chosen

8T-25 may design only:

- no-behavior-change route guard hardening concept
- route guard helper / safe error helper design
- env gate helper design
- response serialization safety design
- static scan maintenance design
- no public alias regression mapping

8T-25 must not implement those helpers.

## G. Explicit Non-goals

- no backend implementation now
- no frontend implementation now
- no test implementation now
- no route behavior change now
- no auth implementation now
- no local-only runtime now
- no UI now
- no storage now
- no evidence row preview now
- no production import now
- no Evidence Layer write now
- no production case / analysis_run now
- no report runtime
- no Sandbox/public event runtime
- no collector runtime/API bridge

## H. Files Changed

- `docs/planning/private_collector_8t_24_runtime_slice_decision_report_v0_1.md`
- `docs/architecture/internal_operator_runtime_slice_readiness_matrix_v0_1.md`
- `docs/architecture/internal_operator_future_runtime_slice_candidates_v0_1.md`

## I. Validation

Run for this docs-only phase:

```text
git diff --check
git status --short
```

Do not run backend tests, frontend build, browser smoke, or collector because this is docs-only unless code was accidentally changed.

Validation result for this phase:

```text
git diff --check = passed
git status --short = three untracked docs-only files
```

## J. Issues

### P0 Privacy / Safety

No P0 issue identified.

### P1 Runtime Decision Blocker

No P1 blocker identified.

Runtime implementation remains explicitly not approved. The recommended path is docs-only guard design or pause.

### P2 Non-blocking Limitation

- No runtime helper design is created beyond the candidate-level 8T-24 decision.
- No implementation is approved.
- No new tests are added in this phase.

These limitations are intentional.

### P3 Nice-to-have

- A future 8T-25 no-behavior-change guard design.
- A future small Source patch only if the user explicitly requests it.

## K. Source Update Policy

No immediate Project Source update unless the user requests another small patch later.

Do not create Source files in repo.
Do not create `docs/project_sources`.

## L. Safety Confirmations

- no backend code changed
- no frontend code changed
- no tests changed
- no runtime code changed
- no backend route added
- no frontend UI added
- no UI implemented
- no test implemented
- no route behavior changed
- route remains disabled by default
- enabled mode remains synthetic/test-only
- route remains GET-only
- no auth implementation
- no authorization implementation
- no local-only runtime implementation
- no sessions / tokens / cookies added
- no persistent staging storage created
- no Evidence Layer write
- no production case created
- no production analysis_run created
- no report runtime generated
- no Sandbox / public event runtime generated
- no public event page generated
- no response_text or generated_public_message generated
- no publish / send / post / execute behavior implemented
- no public / C-end / B-end / customer route exposed
- no collector run
- no live crawl
- no real API called
- no real LLM called
- no URL fetching
- no scraping
- no private collector export root read
- no real package directories read
- no `evidence_items.jsonl` parsed or opened
- no `evidence_items.csv` parsed or opened
- no evidence row files opened
- no Project Source modified in repo
- no Source files created in repo
- no `docs/project_sources` created
- no GitHub Actions workflow recreated
