# Private Collector 8T-26 Helper Implementation Decision Report v0.1

## A. Decision / Status

```text
phase = 8T-26
task = helper_implementation_decision_docs_only
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
helper_implemented = no
persistent_staging_storage_created = no
route_enabled_by_default = no
enabled_mode_test_only = yes
auth_implemented = no
local_only_runtime_implemented = no
route_methods = GET only
```

Decision fields:

```text
helper_implementation_approved_now = no
broad_helper_implementation_approved_now = no
single_future_helper_candidate_selected = route_enabled_env_gate_helper
single_future_helper_candidate_implementation_approved_now = no
runtime_implementation_approved_now = no
route_runtime_expansion_approved_now = no
ui_implementation_approved_now = no
auth_runtime_approved_now = no
storage_implementation_approved_now = no
evidence_row_preview_approved_now = no
production_import_approved_now = no
collector_bridge_approved_now = no
recommended_next_state = ready_for_8T_27_env_gate_helper_implementation_plan_docs_only_or_pause
```

Decision: ready

## B. Inputs From 8T-23 Through 8T-25

- 8T-23 implemented tests-only safety contract and targeted validations passed.
- 8T-24 decided runtime implementation was not approved and selected no-behavior-change route guard design docs-only.
- 8T-25 created no-behavior-change route guard design and helper contract docs-only.
- 8T-25 did not implement helpers.
- Git was clean after the 8T-25 commit.

## C. Helper Implementation Decision

The project is not approved to implement helper code in 8T-26.

However, if the user wants to keep this route line moving, the safest first future helper candidate is `route_enabled_env_gate_helper`.

This candidate is still not approved for implementation now.

```text
ready_for_helper_implementation_now = no
ready_for_broad_helper_implementation = no
ready_for_single_candidate_planning_docs = yes
ready_for_pause = yes
```

## D. Candidate Comparison

| Candidate | Allowed now? | Implementation approved now? | Docs-only implementation plan allowed? | Risk level | Missing prerequisites | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| Pause | yes | n/a | n/a | lowest | none | Allowed if no immediate route need exists. |
| `route_enabled_env_gate_helper` | yes as future candidate | no | yes | low | 8T-27 docs-only plan, explicit implementation approval, red/green tests, snapshot comparison | Preferred first future implementation candidate. |
| `synthetic_mode_guard` helper | design later | no | yes, later | medium | env gate plan, response snapshot strategy, synthetic fixture boundary proof | Defer until after env gate decision. |
| `safe_error_response` helper | design later | no | yes, later | medium | response-shape sensitivity review, snapshot tests, explicit approval | Useful but should wait because it touches response shape. |
| `safe_metadata_projection` helper | design later | no | yes, later | medium/high | allowed-key contract, response-shape snapshot plan, explicit approval | Useful but should wait because it touches response shape. |
| `forbidden_field_scan` helper | test/support candidate later | no | yes, later | low/medium | test utility boundary, false-positive policy, explicit approval | Keep as test-level/support candidate later. |
| `route_surface_assertion` helper | test/support candidate later | no | yes, later | low/medium | route registry scan plan, explicit approval | Keep as test-level/support candidate later. |
| `no_file_delivery_static_scan` helper | test/support candidate later | no | yes, later | low/medium | static scan ownership, false-positive policy, explicit approval | Keep as test-level/support candidate later. |
| `no_evidence_row_open_guard` helper | test/support candidate later | no | yes, later | medium | path guard scope, no private root access proof, explicit approval | Valuable but should not be first implementation. |
| `no_public_alias_guard` helper | test/support candidate later | no | yes, later | low/medium | route scan scope, future UI coupling rules, explicit approval | Valuable as test/static assertion, not first helper implementation. |

Expected conclusions:

- Pause is allowed.
- `route_enabled_env_gate_helper` is the preferred first future implementation candidate, but only after a separate docs-only implementation plan and explicit user approval.
- `safe_error_response` and `safe_metadata_projection` are useful but should wait because they touch response shape.
- Static scans may remain test-level/support candidates later.
- `no_evidence_row_open_guard` and `no_public_alias_guard` are valuable as tests/static assertions, but not first helper implementation.
- All runtime/UI/auth/storage/import candidates remain blocked.

## E. Why Env Gate Helper Is The Safest First Future Candidate

- It can be a pure deterministic helper.
- It has a small input/output contract.
- It should preserve current accepted values: `1`, `true`, `yes`.
- It should preserve all other values as disabled.
- It must not read secrets.
- It must not support query-param/cookie/token/session enablement.
- It must not introduce production mode.
- Existing tests already cover default/falsey/enabled synthetic behavior.
- Snapshot comparison can prove no behavior change.

## F. Required Prerequisites Before Any Implementation

1. 8T-27 implementation plan docs-only accepted.
2. Explicit user approval for implementation.
3. Red/green targeted tests.
4. Snapshot comparison plan.
5. Existing 8T-23 safety contract tests must pass.
6. Enabled fixture smoke must pass.
7. Disabled smoke must pass.
8. Golden contracts must pass.
9. `py_compile` route module must pass.
10. `git diff --check` must pass.
11. Rollback plan documented.
12. No Source files in repo.

## G. Explicit Non-goals

- no backend implementation now
- no frontend implementation now
- no test implementation now
- no helper implementation now
- no route behavior change
- no route default enablement
- no auth implementation
- no local-only runtime
- no UI
- no storage
- no evidence row preview
- no production import
- no Evidence Layer write
- no production case / analysis_run
- no report runtime
- no Sandbox/public event runtime
- no collector runtime/API bridge

## H. Files Changed

- `docs/planning/private_collector_8t_26_helper_implementation_decision_report_v0_1.md`
- `docs/architecture/internal_operator_helper_implementation_readiness_matrix_v0_1.md`
- `docs/architecture/internal_operator_first_helper_implementation_candidate_v0_1.md`

## I. Validation

Run for this docs-only phase:

```text
git diff --check
git status --short
```

Also run a simple textual scan on the three docs for placeholder markers and trailing whitespace.

Do not run backend tests, frontend build, browser smoke, or collector because this is docs-only unless code was accidentally changed.

Validation result for this phase:

```text
git diff --check = passed
git status --short = three untracked docs-only files
placeholder/trailing whitespace scan = passed
```

## J. Issues

### P0 Privacy / Safety

No P0 issue identified.

Helper implementation remains not approved. Runtime, UI, auth, storage, evidence preview, production import, and collector bridge remain blocked.

### P1 Helper Decision Blocker

No P1 blocker identified.

The decision selects only one future candidate and keeps implementation blocked.

### P2 Non-blocking Limitation

- No helper is implemented.
- No new test is implemented.
- The selected helper candidate still needs a docs-only implementation plan before any code.

These limitations are intentional.

### P3 Nice-to-have

- 8T-27 env gate helper implementation plan docs-only.
- Pause if there is no immediate internal operator route need.

## K. Source Update Policy

No immediate Project Source update unless the user requests a small patch later.

Do not create Source files in repo.
Do not create `docs/project_sources`.

## L. Safety Confirmations

- no backend code changed
- no frontend code changed
- no tests changed
- no runtime code changed
- no helper implemented
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
