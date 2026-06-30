# Private Collector 8T-27 Env Gate Helper Implementation Plan Report v0.1

## A. Decision / Status

```text
phase = 8T-27
task = env_gate_helper_implementation_plan_docs_only
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
implementation_plan_created = yes
helper_implementation_approved_now = no
env_gate_helper_implementation_approved_now = no
runtime_implementation_approved_now = no
route_runtime_expansion_approved_now = no
ui_implementation_approved_now = no
auth_runtime_approved_now = no
storage_implementation_approved_now = no
evidence_row_preview_approved_now = no
production_import_approved_now = no
collector_bridge_approved_now = no
recommended_next_state = ready_for_8T_28_env_gate_helper_implementation_approval_decision_or_pause
```

Decision: ready

## B. Inputs From 8T-23 Through 8T-26

- 8T-23 implemented tests-only safety contract and targeted validations passed.
- 8T-24 decided runtime implementation was not approved and selected no-behavior-change route guard design docs-only.
- 8T-25 created no-behavior-change route guard design and helper contract docs-only.
- 8T-26 selected `route_enabled_env_gate_helper` as the single future first helper candidate, but did not approve implementation.
- Git was clean after the 8T-26 commit.

## C. What This Phase Plans

8T-27 only plans a future implementation.

It defines future allowed files, tests, snapshot comparisons, rollback, and stop rules. It does not implement helper code. It does not approve helper code.

## D. Future Helper Contract Recap

Future `route_enabled_env_gate_helper` contract:

Input:

- environment variable string value or `None`

Output:

- enabled boolean
- mode label: `disabled` or `synthetic_fixture_only`
- safe reason code if disabled

Accepted enabled values:

- `1`
- `true`
- `yes`

All other values:

- disabled

Current-code inspection note:

- The current route uses `strip().lower()`, so surrounding whitespace and case variants such as `TRUE` and `Yes` currently resolve the same as `true` and `yes`. Future implementation must preserve this exact current behavior; it must not invent a broader set of enabled values.

Forbidden:

- default enabled
- production mode
- query-param enablement
- token/cookie/session enablement
- reading files
- reading `.env` directly if current code does not do so
- calling APIs
- changing route response schema
- changing route URL or method
- changing enabled fixture behavior

## E. Future Implementation Scope

A future implementation phase, if explicitly approved later, should keep the allowed file scope minimal.

Allowed future implementation files:

- `backend/app/api/v1/routes/internal_operator_review_only_staging.py`
- `backend/app/tests/test_internal_operator_review_only_staging_disabled_smoke.py`
- `backend/app/tests/test_internal_operator_review_only_staging_enabled_fixture_smoke.py`
- `backend/app/tests/test_internal_operator_route_ui_safety_contract.py`

Optional only if justified:

- `backend/app/services/internal_operator_route_guard.py`
- `backend/app/tests/test_internal_operator_route_env_gate_helper.py`

Do not create or modify these files in 8T-27.

The future implementation must be no-behavior-change:

- current route URL unchanged
- current method unchanged
- current default disabled behavior unchanged
- current falsey env behavior unchanged
- current `1` / `true` / `yes` behavior unchanged
- current case/whitespace normalization unchanged
- current response shapes unchanged
- current no-file-read / no-storage / no-production side-effect behavior unchanged

## F. Future Red/Green Test Plan

Design tests only. Do not implement tests.

Future test plan should include:

1. Unit test for helper:
   - `None` -> disabled
   - empty string -> disabled
   - `false` -> disabled
   - `0` -> disabled
   - unknown -> disabled
   - `1` -> enabled synthetic_fixture_only
   - `true` -> enabled synthetic_fixture_only
   - `yes` -> enabled synthetic_fixture_only
   - `TRUE` -> enabled synthetic_fixture_only because current route lowercases
   - `Yes` -> enabled synthetic_fixture_only because current route lowercases
   - whitespace around enabled values -> current-code inspection confirms `strip()` behavior must be preserved
2. Route snapshot tests:
   - unset env disabled response unchanged.
   - falsey env disabled response unchanged.
   - enabled synthetic fixture list response unchanged.
   - enabled synthetic fixture detail response unchanged.
   - unknown candidate not_found response unchanged.
3. Existing safety tests:
   - route/UI safety contract tests.
   - enabled fixture smoke.
   - disabled smoke.
   - analysis request golden contracts.
4. Static safety:
   - no `FileResponse` / `StreamingResponse` / ZIP / public URL / signed URL / external delivery.
   - no public/C-end/B-end/customer alias.
   - no `evidence_items` opening.
   - no private collector root read.
5. Compile / hygiene:
   - `py_compile` route module.
   - `git diff --check`.
   - `git status --short`.

## G. Snapshot Comparison Plan

Future implementation must compare these snapshot groups:

- `disabled_default_snapshot`
- `falsey_env_snapshot`
- `enabled_list_snapshot`
- `enabled_detail_snapshot`
- `enabled_unknown_candidate_snapshot`
- `route_methods_snapshot`
- `forbidden_fields_scan_snapshot`
- `side_effects_snapshot`

The future implementation must prove pre/post snapshots are identical or intentionally equivalent with a documented no-behavior-change reason.

## H. Rollback Plan

Future implementation must be revertible by:

- reverting helper extraction commit.
- restoring direct current env gate logic.
- rerunning 8T-23 safety contract tests.
- rerunning enabled and disabled smoke.
- rerunning golden contracts.
- checking git diff and status.

## I. Stop Rules

Stop immediately if:

- route becomes enabled by default.
- any currently disabled env value becomes enabled.
- any currently enabled value becomes disabled.
- production mode appears.
- route methods change.
- public/C-end/B-end/customer alias appears.
- response schema changes.
- `FileResponse` / `StreamingResponse` / ZIP / public URL / signed URL / external delivery appears.
- `evidence_items` file opens.
- private collector root is read.
- storage / Evidence Layer write / production case / analysis_run appears.
- auth/session/token/cookie behavior appears.
- `response_text` / `generated_public_message` / `target_user_list` / `persuasion_score` / `truth_score` / `official_verified` / `prediction_probability` / `psychological_profile` / `personality_diagnosis` appears.

## J. Explicit Non-goals

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

## K. Files Changed

- `docs/planning/private_collector_8t_27_env_gate_helper_implementation_plan_report_v0_1.md`
- `docs/architecture/internal_operator_env_gate_helper_implementation_plan_v0_1.md`
- `docs/architecture/internal_operator_env_gate_helper_test_snapshot_and_rollback_plan_v0_1.md`

## L. Validation

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

## M. Issues

### P0 Privacy / Safety

No P0 issue identified.

Helper implementation remains not approved. Runtime, UI, auth, storage, evidence preview, production import, and collector bridge remain blocked.

### P1 Implementation Plan Blocker

No P1 blocker identified.

The plan defines future file scope, test groups, snapshot comparison, rollback, and stop rules without implementing code.

### P2 Non-blocking Limitation

- No helper is implemented.
- No new test is implemented.
- The future implementation still requires explicit approval.

These limitations are intentional.

### P3 Nice-to-have

- 8T-28 env gate helper implementation approval decision.
- Pause if there is no immediate internal operator route need.

## N. Source Update Policy

No immediate Project Source update unless the user requests a small patch later.

Do not create Source files in repo.
Do not create `docs/project_sources`.

## O. Safety Confirmations

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
