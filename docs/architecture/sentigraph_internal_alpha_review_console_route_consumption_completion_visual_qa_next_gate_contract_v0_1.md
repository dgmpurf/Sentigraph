# Sentigraph Internal Alpha Review Console Route-consumption Completion / Visual-QA-or-next-gate Contract v0.1

## Purpose

This contract defines the 8Z-31 boundary after the 8Z-30 disabled backend route consumption smoke. It accepts 8Z-30 only as a narrow route-consumption checkpoint, interprets the smoke-level browser evidence, and selects the next conservative docs-only boundary.

## Contract Status

- phase = 8Z-31
- contract_type = route_consumption_completion_visual_qa_next_gate
- docs_only = yes
- route_consumption_completion_gate_only = yes
- visual_qa_next_gate_decision_only = yes
- implementation_performed = no
- backend_code_changed = no
- tests_changed = no
- frontend_changed = no
- frontend_api_hook_changed = no
- sentigraph_api_hook_changed = no
- backend_route_consumed_now = no
- api_calls_performed_now = no
- backend_route_changed = no
- api_route_added = no
- runtime_changed = no
- helper_called = no
- projection_helper_called = no
- route_called = no
- browser_smoke_run = no
- frontend_build_run = no
- actual_evidence_layer_write = no
- persisted_evidence_layer_record_created = no
- production_evidence_item_created = no
- review_queue_runtime_used = no
- production_review_queue_item_created = no
- production_case_created = no
- production_analysis_run_created = no
- actual_analysis_execution_started = no
- production_analysis_result_authorized = no
- production_analysis_result_created = no
- source11_runtime_called = no
- finalsummaryreport_runtime_called = no
- public_delivery_created = no
- collector_provider_jobs = no
- real_exchange_package_dirs_read = no
- production_package_rows_parsed = no
- raw_rows_comments_identities_exposed = no
- secrets_read = no
- source11_update_recommended = no
- selected_next_boundary = ready_for_8Z_32_internal_alpha_review_console_route_consumption_completion_checkpoint_source_sync_docs_only

## Completion Acceptance Contract

8Z-30 is accepted as route-consumption completion only because it satisfies this narrow contract:

- the frontend shell consumes the existing disabled internal GET projection route in read-only mode
- the route consumed is the 8Z-22 disabled internal route skeleton
- the helper is limited to safe allowlisted projection IDs
- unsupported projection IDs are rejected before request construction
- disabled, unavailable, unsupported, and unexpected responses remain safe
- static fallback remains available
- no backend route/API/service/schema/runtime behavior changed
- no write route, write CTA, operational action path, or production object path was introduced

The accepted completion state is:

`route_consumption_complete_for_disabled_internal_read_only_smoke_only`

It is not an operator runtime, Review Queue runtime, actual write path, production object path, Source 11 runtime, FinalSummaryReport runtime, or public/export/final-delivery path.

## Browser / Visual QA Contract

The 8Z-30 health report records frontend build and browser smoke success. 8Z-31 accepts that result as smoke-level browser evidence only.

The accepted browser evidence means:

- the internal route opened during smoke
- the shell rendered
- static fallback / disabled-not-connected state was visible
- required no-write and no-production boundaries were visible
- no browser console error/warn was reported by the smoke result
- no visible 500, ErrorBoundary, `undefined`, `NaN`, or `[object Object]` was reported

The accepted browser evidence does not mean:

- full visual QA
- design review
- accessibility review
- cross-browser QA
- mobile QA
- screenshot/contact-sheet evidence package
- customer-facing readiness

## Next-boundary Decision Contract

The selected next boundary is:

`ready_for_8Z_32_internal_alpha_review_console_route_consumption_completion_checkpoint_source_sync_docs_only`

This selection is valid only because:

- 8Z-30 is accepted as route-consumption completion for gate purposes
- no privacy issue is identified
- no mandatory visual blocker is identified
- persistent screenshot/contact-sheet evidence is optional rather than mandatory
- the safest next mainline step is a docs-only checkpoint/source-sync recommendation

If visual artifacts become important before source sync, the project may choose a separate visual QA/contact-sheet smoke phase instead. That option is not selected by this contract.

## Non-authorization

This contract does not authorize:

- new implementation
- frontend API changes
- `sentigraphApi` helper expansion
- backend route consumption in this phase
- backend route behavior expansion
- backend route/API implementation
- POST / PUT / PATCH / DELETE routes
- runtime persistence
- Review Queue runtime
- actual Evidence Layer write
- persisted Evidence Layer record creation
- production EvidenceItem creation
- production Review Queue item creation
- production case creation
- production analysis_run creation
- actual analysis execution
- production Analysis Result authorization or creation
- Source 11 runtime
- FinalSummaryReport runtime
- B-end report runtime
- Sandbox/public event runtime
- export/download/public/final-delivery runtime
- collector/provider jobs
- real exchange/package directory reads
- production package-row parsing
- raw rows/comments/identities exposure
- secrets access
- Project Source file creation in repo
- docs/project_sources creation
- GitHub Actions changes

## Safety Invariants

The 8Z-31 decision preserves these invariants:

- internal-only route context
- disabled-by-default backend route posture
- GET-only route-consumption scope from 8Z-30
- read-only safe projection data
- static fallback path
- human review required
- no automatic trust upgrade
- no actual write
- no production object
- no public/customer alias
- no recording/video next step
- 8W-69 pause preserved
- 8W-70 reactivation not selected

## Source Sync Recommendation Contract

If 8Z-31 is committed and accepted as the selected checkpoint:

- ChatGPT-side Source update may be recommended
- Source 11 update remains no unless existing governance runtime behavior changes
- Codex must not create Project Source files in repo
- Codex must not create docs/project_sources files
- no tag is recommended

The source-sync recommendation exists because the disabled internal backend route skeleton and the internal frontend shell are now connected through a narrow read-only route-consumption smoke. It does not imply runtime authorization or production readiness.

## Validation Contract

8Z-31 validation is docs-only:

- `git diff --check`
- trailing whitespace scan on the new docs
- open-marker/mojibake scan on the new docs
- approval phrase scan
- selected future phrase scan
- non-selected future phrase scan if present
- forbidden positive claim scan
- scope scan
- `git status --short`

No backend tests, frontend build, browser smoke, route smoke, helper execution, collector/provider jobs, real API/LLM/network, URL fetch, or scrape is required or allowed for 8Z-31.

## Stop Rules

Stop before completing 8Z-31 if any of the following appears necessary:

- backend code change
- frontend code change
- test change
- runtime change
- route/API behavior change
- helper execution
- projection helper execution
- route call
- browser smoke
- production object creation
- actual Evidence Layer write
- Review Queue runtime
- real exchange/package directory read
- production package-row parsing
- raw/private/secret data access
- Project Source file creation in repo
- GitHub Actions change

## Future Compatibility Rule

Future UI changes must run frontend build and browser smoke when available. Future backend route changes require a separate gate. Future actual write or Review Queue runtime remains a separate high-risk governance path.
