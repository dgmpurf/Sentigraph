# Sentigraph 8W-1 Real Exported Package Metadata Controlled Selection Decision v0.1

## A. Decision / Status

phase = 8W-1

task = real_exported_package_metadata_controlled_selection_decision

decision = ready

selected_next_boundary_option = ready_for_8W_2_controlled_real_exported_package_metadata_smoke_implementation_after_explicit_approval

privacy_issue_stop = no

docs_only = yes

backend_code_changed = no

frontend_code_changed = no

tests_changed = no

route_changed = no

api_route_added = no

runtime_changed = no

collector_run = no

real_api_called = no

real_llm_called = no

url_fetch_or_scrape = no

private_collector_inspected = no

real_exchange_dir_read = no

evidence_rows_parsed = no

original_package_rows_read = no

evidence_layer_write = no

production_case_created = no

production_analysis_run_created = no

selector_implemented = no

package_metadata_smoke_executed = no

download_package_runtime_used = no

public_access_runtime_used = no

external_delivery_runtime_used = no

final_delivery_runtime_used = no

b_end_report_runtime_generated = no

sandbox_public_event_generated = no

generated_response_text = no

public_route_created = no

frontend_integration_approved = no

source_files_created = no

docs_project_sources_created = no

source15_patch_recommended = no

source23_patch_recommended = no

source00_index_patch_recommended = no

source24_new_patch_recommended = consider_after_8W_1_commit

source11_update_recommended = no

Decision:

8W-1 selects Option A:

`ready_for_8W_2_controlled_real_exported_package_metadata_smoke_implementation_after_explicit_approval`

This means a future 8W-2 may, only after the exact approval phrase in Section O, implement a tightly bounded metadata-only smoke against one explicitly selected, already-exported package metadata target. 8W-1 itself does not implement that smoke, does not select by reading any real directory, and does not inspect private collector source.

## B. Current 8V Completion Context

8V is stage-complete only as a local backend metadata/governance boundary chain.

The proven chain is:

1. provider result metadata
2. safe package resolver
3. local exchange metadata smoke
4. review-only staging candidate
5. staging candidate generated-run bridge
6. controlled minimum real-run bridge execution
7. `sentigraph_opinion_ecosystem_run_v0_1` generated run
8. controlled generated-run dense graph bridge integration
9. backend-only dense graph preview
10. `sentigraph_dense_graph_report_candidate_v0_1` local report candidate
11. `sentigraph_report_candidate_final_report_boundary_v0_1` local final-report-boundary object
12. `sentigraph_final_report_boundary_source11_governance_handoff_v0_1` local Source 11 governance handoff marker
13. `sentigraph_source11_governance_handoff_finalsummaryreport_adapter_v0_1` local FinalSummaryReport boundary adapter
14. local in-memory `sentigraph_final_summary_report_v1`-shaped boundary object
15. `sentigraph_finalsummaryreport_boundary_export_gate_handoff_v0_1` local export-gate handoff/readiness marker
16. `sentigraph_export_gate_handoff_export_artifact_boundary_v0_1` local export-artifact boundary/readiness marker
17. `sentigraph_export_artifact_boundary_download_public_access_boundary_v0_1` local download/public-access boundary/readiness marker
18. `sentigraph_download_public_access_boundary_final_delivery_boundary_v0_1` local final-delivery boundary/readiness marker
19. 8V delivery-boundary chain stage-complete decision

8V proved local metadata handoff boundaries only. It did not prove production readiness, customer readiness, public readiness, Evidence Layer import readiness, production case readiness, production `analysis_run` readiness, route/frontend readiness, final delivery readiness, or real package data access readiness.

## C. Real Exported Package Metadata Selection Problem Statement

8W begins a new selection planning phase for real already-exported package metadata.

The 8W-1 problem is to define how a future implementation may identify one safe target for metadata-only smoke without crossing into:

- private collector source inspection
- real exchange directory traversal
- evidence row parsing
- original package row reading
- raw identity exposure
- Evidence Layer write
- production case creation
- production `analysis_run` creation
- report/export/download/public/final-delivery runtime
- route/frontend integration
- real API, real LLM, provider, or collector execution

Provider output remains evidence candidate metadata, not truth, not official verification, not full-web coverage, not full-platform coverage, not causal proof, and not prediction.

## D. Allowed Future Target Definition

A future 8W-2 target may only be a user-approved, already-exported package metadata target.

Allowed target requirements:

- The package was exported before the Sentigraph 8W-2 task starts.
- The target is selected by safe package name or safe metadata identifier, not by an absolute private path.
- The target has metadata-only identity available through an approved metadata record or index entry.
- The target has package index, manifest, validation report, source manifest, and coverage note presence flags, or documented absence/warning states.
- The target has no known privacy blockers.
- The target has no unresolved path traversal, path escape, or absolute private path exposure risk.
- The target can be assessed without reading `evidence_items.jsonl`, `evidence_items.csv`, original package rows, raw comments, raw identities, or profile URL values.
- The target does not require private collector source inspection.
- The target is appropriate for a controlled metadata-only smoke, not a production import.
- The target keeps provider output as evidence candidate, not truth.

Target selection must remain blocked if any required identity is ambiguous and resolving it would require private source inspection, real directory traversal, row parsing, or secret/path exposure.

## E. Allowed Metadata Identity Fields

Future 8W-2 may use only safe conceptual metadata fields such as:

- `package_name`
- `package_role`
- `case_id_hint`
- `provider_result_id`
- `provider_job_id`
- `request_id`
- `validation_status`
- `warning_count`
- `error_count`
- evidence count summary
- source count summary
- coverage note summary
- `privacy_status`
- `path_status`
- `metadata_schema_version`
- `export_package_schema_version`
- package index entry metadata
- manifest presence flag
- validation report presence flag
- source manifest presence flag
- coverage note presence flag

Allowed metadata fields must be treated as selection hints only. They do not upgrade trust, verify authenticity, approve production import, or approve analysis.

## F. Metadata-only Preflight Requirements

Before any future 8W-2 metadata-only smoke, the implementation plan must confirm:

1. The exact 8W-2 approval phrase is present.
2. One package metadata target is explicitly selected by the user or by a safe metadata identifier named by the user.
3. The target is already exported before the task starts.
4. The target can be referenced without emitting absolute private paths.
5. The target can be assessed without private collector source inspection.
6. The target can be assessed without parsing evidence row files or original package rows.
7. The target has no known privacy blocker.
8. The target has no known path traversal or path escape blocker.
9. The target has no secret-like value or raw identity value in allowed metadata.
10. The target's validation status is suitable for metadata-only smoke, or `warn` states are explicitly marked manual-review-required.
11. The target remains selected-sample-only and not full-web, not full-platform, not full-thread, not official verification, not causal proof, not prediction, and not production score.
12. The future helper, if approved, must keep all side effects false except the minimal local metadata-smoke marker allowed by that future task.

## G. Forbidden Inputs / Outputs

Forbidden inputs and outputs include:

- private collector source code
- collector runtime internals
- collector sessions, cookies, tokens, profiles, secrets, salts, passwords, or API keys
- real exchange directory traversal without explicit approval
- `evidence_items.jsonl`
- `evidence_items.csv`
- original package rows
- raw comments
- raw author identifiers
- actual author names
- actual profile URL values
- private messages
- browser profile paths
- proxy or anti-bot details
- absolute private paths
- runtime file paths
- package paths as actual emitted values
- public URLs
- signed URLs
- file-byte routes
- external delivery targets
- object storage targets
- email delivery targets
- portal publication targets
- customer delivery targets
- generated response text
- target user lists
- persuasion scores
- truth scores
- official verification claims
- prediction probabilities
- psychological profiles
- personality diagnoses
- `auto_execute`, `publish`, `send`, `post`, or `execute` behavior

Safe negative boundary language may mention these only as false, forbidden, blocked, deferred, non-approved, or requiring separate later gates.

## H. Blocker Categories

Future 8W-2 must block if:

- there is no explicit user approval for 8W-2 implementation
- no explicit package metadata target is selected
- target identity requires reading a real exchange directory without approval
- target identity requires private collector source inspection
- target identity requires `evidence_items.jsonl` parsing
- target identity requires `evidence_items.csv` parsing
- target identity requires original package row reading
- target uses absolute private path as public output
- metadata contains secret-like values
- metadata contains raw identity values
- metadata contains raw comments or actual profile URL values
- metadata indicates privacy blocker
- metadata indicates path traversal or path escape risk
- metadata indicates validation errors not suitable for smoke
- request asks for Evidence Layer write
- request asks for production case
- request asks for production `analysis_run`
- request asks for B-end report runtime, Sandbox runtime, or public event runtime
- request asks for report/export/download/public/final-delivery runtime
- request asks for route/frontend integration
- request asks for real API, real LLM, provider, or collector execution
- request asks for URL fetch or scrape
- request asks for public or customer output

Any blocker must stop the future phase unless a later user approval explicitly names that exact behavior. Row reads, production writes, public delivery, and private collector source inspection remain separate gates even after 8W-2 approval.

## I. Future 8W-2 Option A: Controlled Metadata-only Smoke

Option A is selected for the future next boundary.

Future 8W-2 may implement, after exact approval only, a controlled metadata-only smoke against one explicitly selected already-exported package metadata target.

The future 8W-2 implementation must remain:

- metadata-only
- no-row-read
- no-private-collector-source-inspection
- no Evidence Layer write
- no production case
- no production `analysis_run`
- no frontend
- no route
- no real API
- no real LLM
- no provider execution
- no collector execution
- no URL fetch
- no scrape
- no B-end report runtime
- no Sandbox/public event runtime
- no report/export/download/public/final-delivery runtime

8W-2 must not infer official verification, truth, causality, prediction, production score, full-web coverage, full-platform coverage, or full-thread coverage.

## J. Future 8W-2 Option B: Inventory/report-only

Option B is not selected now.

Use Option B later if package target selection remains ambiguous because:

- safe package identity fields are unavailable
- export root behavior is unclear
- metadata source is unclear
- env behavior would need to be trusted without review
- package index semantics are inconsistent
- metadata-only smoke would require path traversal or row parsing

If selected later, Option B should remain docs-only or report-only and must not implement a smoke helper.

## K. Future 8W-2 Option C: More Docs-only Inventory

Option C is not selected now.

Use Option C later if the repo lacks enough docs/contracts to safely define:

- allowed target identity fields
- metadata-only preflight requirements
- blocker categories
- private collector separation
- path handling rules
- row-read boundaries
- future exact approval protocol

8W-1 now defines those boundaries sufficiently for a future explicitly approved 8W-2 metadata-only smoke.

## L. Relationship to Private Collector

8W-1 does not change private collector behavior.

Sentigraph must not:

- inspect private collector source
- run collector
- run provider jobs
- access collector sessions, cookies, tokens, profiles, or secrets
- use browser profile state
- read real export folders
- access external collector export roots
- use any real path supplied by env
- run code that opens package directories

Future 8W-2 may only use a user-approved, already-exported package metadata target and must stay metadata-only unless a separate later approval explicitly broadens scope.

## M. Relationship to Source 11 / Evidence Layer

8W-1 does not change Source 11 behavior.

8W-1 does not:

- update Source 11
- change Analysis Request behavior
- change Provider / Import Governance behavior
- change FinalSummaryReport behavior
- write Evidence Layer
- create a production case
- create a production `analysis_run`
- create production review queue items
- run dedup
- run analysis
- generate reports
- generate Sandbox fixtures
- generate public event pages
- create public/customer/delivery outputs

After 8W-1 commit, a Source 24 or equivalent ChatGPT-side project-context patch may be considered if the user wants a new phase marker. Do not create Project Source files inside the repository.

## N. Explicit Non-approvals

8W-1 explicitly does not approve:

- backend runtime implementation
- backend code modification
- tests
- frontend implementation
- route/API addition
- runtime file creation
- selector implementation
- package metadata smoke execution
- real exchange directory read
- private collector source inspection
- evidence row parsing
- original package row reading
- Evidence Layer write
- production case creation
- production `analysis_run` creation
- report/export/download/public/final-delivery runtime
- download package runtime
- public access runtime
- external delivery runtime
- final delivery runtime
- B-end report runtime
- Sandbox/public event runtime
- public URL creation
- signed URL creation
- file-byte route creation
- object storage upload
- email sending
- portal publication
- generated response text
- target user lists
- persuasion scores
- truth scores
- official verification claims
- prediction probabilities
- psychological profiles
- personality diagnoses
- publish, send, post, execute, or auto-execute behavior
- Project Source file creation
- `docs/project_sources/` creation

## O. Required Approval Phrase

Future 8W-2 implementation requires this exact approval phrase:

`批准 8W-2 Controlled Real Exported Package Metadata Smoke implementation`

Without this phrase:

- do not implement selector
- do not read real exchange directories
- do not inspect private collector source
- do not parse rows
- do not create runtime objects
- do not touch Evidence Layer
- do not create production case
- do not create production `analysis_run`
- do not touch frontend/routes
- do not generate B-end, Sandbox, public, export, download, or final-delivery surfaces

Even with this approval, default 8W-2 must remain metadata-only unless the user separately approves row reads or runtime behavior.

## P. Validation / Not Run

Validation for this docs-only phase:

- `git status --short`
- `git branch --show-current`
- `git rev-parse HEAD`
- `git diff --check`
- static safety scan of the two new docs

Backend tests, frontend build, browser smoke, runtime smoke, provider jobs, collector jobs, real API calls, real LLM calls, URL fetching, scraping, private collector inspection, real exchange directory reads, evidence row parsing, original package row reads, local exchange reader runs against real folders, Source file creation, and Project Source updates are intentionally not run because this phase changes only docs.

## Q. Issues P0/P1/P2/P3

- P0: none.
- P1: none.
- P2: future 8W-2 must name exactly one approved package metadata target and prove metadata-only/no-row-read behavior before any smoke is run.
- P3: later Source 24 or project-context patch may summarize 8W-1 after commit, but Source 11 remains unchanged.

## R. Recommended Next Step

Recommended next task:

Phase 8W-2 Controlled Real Exported Package Metadata Smoke implementation, only after the exact approval phrase:

`批准 8W-2 Controlled Real Exported Package Metadata Smoke implementation`

If that approval is not provided, do not proceed to implementation. The safe fallback is an inventory/report-only or docs-only checkpoint.
