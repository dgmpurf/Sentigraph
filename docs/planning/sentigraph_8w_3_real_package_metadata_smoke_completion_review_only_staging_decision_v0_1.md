# Sentigraph 8W-3 Real Package Metadata Smoke Completion / Review-only Staging Decision v0.1

## A. Decision / Status

phase = 8W-3

task = real_package_metadata_smoke_completion_review_only_staging_decision

decision = ready

selected_next_boundary_option = ready_for_8W_4_controlled_metadata_smoke_output_to_review_only_staging_boundary_smoke_after_explicit_approval

privacy_issue_stop = no

docs_only = yes

backend_code_changed = no

frontend_code_changed = no

tests_changed = no

route_changed = no

api_route_added = no

runtime_changed = no

selector_implemented = no

review_only_staging_boundary_created = no

review_only_staging_runtime_used = no

row_preview_approved = no

evidence_items_jsonl_parsed = no

evidence_items_csv_parsed = no

original_package_rows_read = no

private_collector_inspected = no

private_collector_source_inspected = no

real_exchange_dir_read = no

evidence_layer_write = no

production_case_created = no

production_analysis_run_created = no

b_end_report_runtime_generated = no

sandbox_public_event_generated = no

generated_response_text = no

public_route_created = no

frontend_integration_approved = no

download_package_runtime_used = no

public_access_runtime_used = no

external_delivery_runtime_used = no

final_delivery_runtime_used = no

source_files_created = no

docs_project_sources_created = no

8w2_smoke_status = metadata_warn_manual_review_required

8w2_warning_count = 1

human_review_required = yes

source24_patch_recommended = consider_after_8W_3_commit

source11_update_recommended = no

Decision:

8W-2 is complete enough as a metadata-only checkpoint with warning/manual-review status.

Completion assessment:

`complete_with_warning_manual_review_required`

The warning is non-blocking for a future backend-only metadata-smoke-output to review-only staging boundary smoke, because the future 8W-4 scope is only a boundary/readiness marker and must preserve `human_review_required = true`. 8W-3 does not approve row preview, Evidence Layer import, production case, production `analysis_run`, frontend/route, B-end report runtime, Sandbox/public event runtime, report/export/download/public/final-delivery runtime, real API/LLM/provider/collector, or private collector inspection.

## B. 8W-2 Metadata Smoke Result Summary

8W-2 completed a backend-only controlled metadata-only smoke for exactly one approved package metadata target:

- package_name: `donglu-sunjihai-youth-football-202606-v2_20260617_121016`
- package_role: `candidate_demo_sample`
- case_id_hint: `donglu_sunjihai_youth_football_202606`
- smoke_status: `metadata_warn_manual_review_required`
- warning_count: `1`
- error_count: `0`
- human_review_required: `true`
- selector_implemented: `no`
- row files parsed: `no`
- original package rows read: `no`
- private collector source inspected: `no`
- real exchange directory read: `no`
- Evidence Layer write: `no`
- production case: `no`
- production `analysis_run`: `no`
- frontend/route: `no`

8W-2 produced a safe local metadata-smoke object only. It did not produce review queue items, EvidenceItems, production cases, production analysis runs, public/customer output, or delivery artifacts.

## C. Meaning of `metadata_warn_manual_review_required`

`metadata_warn_manual_review_required` means:

- the metadata smoke completed safely
- the package target identity matched the explicitly approved target
- safe metadata was read only from allowed metadata files
- row files remained presence-only
- no privacy blocker was reported
- no path blocker was reported
- warning_count = 1 must remain visible and acknowledged in human review
- future review-only staging can only be a metadata-only boundary if separately approved

It does not mean:

- evidence rows are safe to parse
- package rows can be previewed
- Evidence Layer import is approved
- production case creation is approved
- production `analysis_run` creation is approved
- B-end report, Sandbox, or public event generation is approved
- frontend/route integration is approved
- final delivery, public access, download package, or external delivery is approved
- official verification is complete
- full-web, full-platform, or full-thread coverage is achieved
- causal proof, prediction, or production score is available

## D. Completion Assessment

8W-2 is complete enough as a metadata-only checkpoint because:

- the approved package target was exact and repo-controlled
- the smoke did not implement selector behavior
- the smoke did not read real exchange directories
- the smoke did not inspect private collector source
- row/log files remained presence-only
- the output carried selected-sample and not-full-coverage boundaries
- all production, public, frontend, route, delivery, collector, API, LLM, row-read, and Evidence Layer side-effect flags remained false

This assessment is limited to metadata-smoke completion. It is not a production readiness or import readiness assessment.

## E. Warning Handling Decision

warning_handling_decision = non_blocking_for_future_metadata_only_review_only_staging_boundary

The warning remains meaningful and must be carried forward as manual-review context. It must not be suppressed, treated as evidence verification, or converted into analysis readiness.

Future 8W-4, if approved, must preserve:

- `human_review_required = true`
- `warning_count = 1`
- warning summary
- selected sample boundary
- no row-read boundary
- no production object boundary

If a later task tries to convert warning/manual-review status into row preview, production import, analysis, report generation, or public/customer output, it must be blocked.

## F. Review-only Staging Boundary Question

The review-only staging boundary question is:

Can the 8W-2 safe metadata-smoke object become input to a future backend-only local review-only staging boundary/readiness marker?

Answer:

Yes, after explicit 8W-4 approval, but only as metadata-only safe input and only to create a local boundary/readiness marker. It must not create EvidenceItems, production review queue items, Evidence Layer rows, production case, production `analysis_run`, row preview, B-end report, Sandbox/public event, frontend route, public output, customer output, or delivery artifact.

## G. Selected Next Boundary Option

Selected option:

`ready_for_8W_4_controlled_metadata_smoke_output_to_review_only_staging_boundary_smoke_after_explicit_approval`

Rationale:

8W-2 warning/manual-review status is compatible with a future metadata-only review-only staging boundary because the staging boundary can preserve manual review and blocked production actions. The future 8W-4 must be backend-only, no-row-read, local, and test-first. It must require exact user approval before implementation.

## H. Future 8W-4 Allowed Input Contract

Allowed future 8W-4 input:

- the 8W-2 safe local metadata-smoke object only
- exact approved package identity only
- safe metadata fields only
- smoke status
- warning count
- error count
- safe warning summary
- safe blocker summary
- metadata file presence flags
- selected sample / not full coverage boundary flags
- runtime side-effect false flags

Allowed fields may include:

- `schema`
- `phase`
- `smoke_status`
- `target_package_name`
- `target_package_role`
- `target_case_id_hint`
- `target_provider_result_id`
- `target_provider_job_id`
- `target_request_id`
- `metadata_only`
- `human_review_required`
- `metadata_files_presence`
- `safe_summary`
- `boundary_flags`
- `runtime_side_effects`
- `warnings`
- `blockers`

The future input must not require reading package rows or package files beyond the already-created safe metadata-smoke object.

## I. Future 8W-4 Forbidden Input/output

Forbidden future 8W-4 input:

- `evidence_items.jsonl` content
- `evidence_items.csv` content
- `source_manifest.jsonl` rows
- `collection_log.jsonl` rows
- original package rows
- raw comments
- raw author identifiers
- actual author names
- actual profile URL values
- absolute paths
- package paths as public output
- private collector source
- real exchange directories
- cookies, tokens, sessions, API keys, passwords, salts, secrets, browser profiles, or collector internals

Allowed future 8W-4 output:

- backend-only local review-only staging boundary/readiness marker
- metadata-only safe summary
- `human_review_required = true`
- warning/manual-review context
- no production object

Forbidden future 8W-4 output:

- EvidenceItem rows
- production review queue items
- production Evidence Layer
- production case
- production `analysis_run`
- row preview
- B-end report runtime
- Sandbox/public event runtime
- frontend route
- public/customer output
- generated response text
- report/export/download/public/final-delivery runtime
- download package
- public URL
- signed URL
- file-byte route
- object storage upload
- email
- portal publication
- publish, send, post, execute, or auto-execute behavior

## J. Future 8W-4 Exact Approval Phrase

Future 8W-4 implementation requires this exact approval phrase:

`批准 8W-4 Controlled Metadata-Smoke Output to Review-only Staging Boundary Smoke implementation`

Without this exact phrase:

- do not implement backend helper
- do not create tests
- do not create review-only staging boundary object
- do not read rows
- do not inspect private collector source
- do not write Evidence Layer
- do not create production case
- do not create production `analysis_run`
- do not touch frontend/routes
- do not generate B-end report, Sandbox/public event, public/customer output, or final-delivery surfaces

## K. Explicit Non-approvals

8W-3 explicitly does not approve:

- backend runtime implementation
- backend code changes
- test changes
- frontend code changes
- route/API additions
- runtime helper creation
- runtime file creation
- selector implementation
- review-only staging boundary creation
- review-only staging runtime
- row preview
- `evidence_items.jsonl` parsing
- `evidence_items.csv` parsing
- source manifest row parsing
- collection log row parsing
- original package row reading
- raw comment reading
- raw identity reading
- private collector source inspection
- real exchange directory read
- Evidence Layer write
- production case creation
- production `analysis_run` creation
- B-end report runtime
- Sandbox/public event runtime
- report/export/download/public/final-delivery runtime
- public route creation
- frontend integration
- real API calls
- real LLM calls
- provider jobs
- collector jobs
- URL fetch
- scrape
- generated response text
- public/customer output
- publish, send, post, execute, or auto-execute behavior
- Project Source file creation
- `docs/project_sources/` creation

## L. Relationship to Source 11 / Evidence Layer

8W-3 does not change Source 11 behavior.

8W-3 does not write Evidence Layer, create EvidenceItems, create production review queue items, create a production case, create a production `analysis_run`, run production dedup, run analysis, generate reports, generate Sandbox fixtures, or generate public event pages.

Source 11 should remain unchanged because Analysis Request / Provider / Import Governance behavior did not change in this docs-only checkpoint.

## M. Relationship to Private Collector

8W-3 does not change private collector behavior.

Sentigraph must not:

- inspect private collector source
- run collector jobs
- run provider jobs
- access collector sessions, cookies, tokens, profiles, browser state, or secrets
- read real exchange directories
- access external collector export roots
- parse exported row files
- use env-provided real paths

Future 8W-4 may only consume the safe 8W-2 metadata-smoke object after explicit approval.

## N. Validation / Not Run

Validation for this docs-only phase:

- `git status --short`
- `git branch --show-current`
- `git rev-parse HEAD`
- `git diff --check`
- static safety scan of the two new docs

Not run:

- pytest
- frontend build
- browser smoke
- collector
- real APIs
- real LLMs
- provider jobs
- URL fetch
- scrape
- private collector source inspection
- real exchange directory read
- evidence row parsing
- row preview
- Evidence Layer write
- production case / production `analysis_run`
- B-end report / Sandbox/public event / report/export/download/public/final-delivery runtime smoke
- route/frontend smoke

Reason:

8W-3 is docs-only and explicitly forbids runtime behavior.

## O. Issues P0/P1/P2/P3

- P0: none.
- P1: none.
- P2: future 8W-4 must preserve `metadata_warn_manual_review_required`, `warning_count = 1`, and `human_review_required = true`; do not convert the warning into row preview, production import, analysis, report, or public output readiness.
- P3: consider ChatGPT-side Source 24 patch after commit.

## P. Recommended Next Step

Recommended next task:

Phase 8W-4 Controlled Metadata-Smoke Output to Review-only Staging Boundary Smoke implementation, only after this exact approval phrase:

`批准 8W-4 Controlled Metadata-Smoke Output to Review-only Staging Boundary Smoke implementation`

If the phrase is not provided, keep the project at the 8W-3 docs-only checkpoint.

## Q. Source Maintenance Recommendation

After commit:

- consider ChatGPT-side Source 24 or equivalent project-context patch for 8W-3
- do not update Source 11
- do not create Project Source files inside this repository
- do not create `docs/project_sources/`
