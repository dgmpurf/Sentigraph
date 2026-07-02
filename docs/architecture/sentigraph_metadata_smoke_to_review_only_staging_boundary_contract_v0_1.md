# Sentigraph Metadata Smoke to Review-only Staging Boundary Contract v0.1

## A. Contract Purpose

This contract defines how the 8W-2 safe metadata-smoke object may, in a future phase, become input to a backend-only review-only staging boundary/readiness marker.

The contract preserves a strict separation between:

- completed 8W-2 metadata-smoke output
- a future 8W-4 metadata-only boundary smoke
- any later row preview, import, Evidence Layer write, production case, production `analysis_run`, frontend, report, Sandbox/public event, public/download/final-delivery, provider, collector, API, or LLM behavior

This contract is docs-only. It is not implementation, not a helper, not a route, not a review queue, not Evidence Layer import, and not production staging.

## B. 8W-2 Metadata-smoke Object as Source

The only allowed future 8W-4 source is the safe local 8W-2 metadata-smoke object:

- schema: `sentigraph_real_exported_package_metadata_smoke_v0_1`
- phase: `8W-2`
- smoke_status: `metadata_warn_manual_review_required`
- target package: `donglu-sunjihai-youth-football-202606-v2_20260617_121016`
- metadata_only: `true`
- human_review_required: `true`
- warning_count: `1`
- row files parsed: `false`
- private collector source inspected: `false`
- real exchange directory read: `false`
- Evidence Layer write: `false`
- production case: `false`
- production `analysis_run`: `false`

The source object must be treated as evidence-candidate metadata, not truth, not official verification, not full-web coverage, not full-platform coverage, not causal proof, not prediction, and not production score.

## C. Metadata-only Review-only Staging Boundary Definition

A future review-only staging boundary marker may be created only after explicit 8W-4 approval.

The marker may represent:

- metadata-only handoff readiness
- manual review required
- warning context carried forward
- safe package identity
- safe validation status
- safe presence flags
- safe blocker/warning summaries
- production and public side effects blocked

The marker must not represent:

- EvidenceItem creation
- production Evidence Layer write
- production review queue item creation
- production case creation
- production `analysis_run` creation
- row preview
- report generation
- Sandbox/public event generation
- frontend/route integration
- public/customer output
- final delivery

## D. Warning Handling Contract

`metadata_warn_manual_review_required` is compatible with a future metadata-only review-only staging boundary only if:

- `warning_count = 1` remains visible
- warning summary is preserved
- `human_review_required = true` remains true
- promotion remains blocked
- row preview remains blocked
- production objects remain blocked
- analysis remains blocked
- public/customer output remains blocked

The warning must not be converted into readiness for import, analysis, reporting, publication, or delivery.

If a later implementation cannot preserve warning/manual-review state, it must block.

## E. Allowed Metadata Fields

Future 8W-4 may consume safe fields from the 8W-2 object such as:

- `schema`
- `phase`
- `smoke_status`
- `target_package_name`
- `target_package_role`
- `target_case_id_hint`
- `target_provider_result_id`
- `target_provider_job_id`
- `target_request_id`
- `target_identity_method`
- `target_source_kind`
- `metadata_only`
- `human_review_required`
- `metadata_files_presence`
- `safe_summary.validation_status`
- `safe_summary.warning_count`
- `safe_summary.error_count`
- `safe_summary.evidence_count_summary`
- `safe_summary.source_count_summary`
- `safe_summary.coverage_note_summary`
- `safe_summary.privacy_status`
- `safe_summary.path_status`
- `safe_summary.blocker_summary`
- `safe_summary.warning_summary`
- `boundary_flags`
- `runtime_side_effects`
- safe `warnings`
- safe `blockers`

Allowed metadata fields may support a boundary/readiness marker only. They must not trigger row reads, import, analysis, report, public event, or delivery.

## F. Forbidden Fields and Actions

Forbidden future inputs:

- `evidence_items.jsonl` content
- `evidence_items.csv` content
- `source_manifest.jsonl` rows
- `collection_log.jsonl` rows
- original package rows
- raw comments
- raw author identifiers
- actual author names
- actual profile URL values
- private messages
- cookies, sessions, tokens, passwords, API keys, salts, or secrets
- browser profile paths
- private collector source
- collector runtime internals
- real exchange directory contents
- absolute paths
- package paths as public output

Forbidden future actions:

- row preview
- row parsing
- Evidence Layer write
- production review queue creation
- production case creation
- production `analysis_run` creation
- B-end report runtime generation
- Sandbox/public event runtime generation
- report/export/download/public/final-delivery runtime
- route/frontend integration
- public URL creation
- signed URL creation
- file-byte route creation
- object storage upload
- email sending
- portal publication
- customer delivery
- generated response text
- publish, send, post, execute, or auto-execute behavior
- real API, real LLM, provider job, or collector job execution
- URL fetch or scrape

## G. Future 8W-4 Blocker Contract

Future 8W-4 must block if:

- exact 8W-4 approval phrase is missing
- input is not the safe 8W-2 metadata-smoke object
- package identity does not match the approved Dong/Sun target
- `smoke_status` is blocked
- `metadata_only` is not true
- `human_review_required` is not true
- warning/manual-review status is dropped
- `row_files_parsed` is true
- any runtime side-effect flag is true
- Evidence Layer write is requested
- production case or production `analysis_run` is requested
- row preview or row parsing is requested
- private collector source inspection is requested
- real exchange directory read is requested
- frontend/route is requested
- B-end report, Sandbox/public event, report/export/download/public/final-delivery runtime is requested
- public/customer output is requested
- generated response text is requested
- publish, send, post, execute, or auto-execute is requested

Blocked output must include only safe reason codes and must not echo forbidden values.

## H. Future Output Contract

Allowed future 8W-4 output:

- schema identifying a local review-only staging boundary/readiness marker
- source schema and source smoke id or safe source label if present
- approved package identity
- metadata-only status
- warning/manual-review status
- human review required
- safe warning and blocker summaries
- allowed review-only actions
- blocked production/public/delivery actions
- runtime side-effect flags all false
- no path exposure

Forbidden future 8W-4 output:

- EvidenceItem rows
- production review queue items
- production Evidence Layer records
- production case
- production `analysis_run`
- row preview
- raw comments
- raw identities
- paths
- URLs
- delivery targets
- report or public event artifacts
- generated response text

## I. No-row-read Proof Expectations

Future 8W-4 tests should prove:

- no `evidence_items.jsonl` content read
- no `evidence_items.csv` content read
- no `source_manifest.jsonl` row parsing
- no `collection_log.jsonl` row parsing
- no original package row reading
- no row preview output

Preferred proof:

- monkeypatch file read helpers to fail on row/log filenames
- assert only the safe 8W-2 object is consumed
- assert all row-read runtime flags remain false

## J. No-private-collector-inspection Expectations

Future 8W-4 must prove:

- private collector project is not modified
- private collector source is not inspected
- collector jobs are not run
- provider jobs are not run
- real exchange directories are not read
- env-provided export roots are not used
- sessions, cookies, tokens, profiles, secrets, and browser state are not accessed

Safe tests should use local fixture objects only unless a future user approval explicitly expands scope.

## K. Evidence Layer / Production Boundary

Future 8W-4 must keep these false:

- Evidence Layer write
- EvidenceItem creation
- production review queue creation
- production case creation
- production `analysis_run` creation
- production dedup
- analysis execution
- report runtime
- Sandbox/public event runtime
- export/download/public/final-delivery runtime

Review-only staging boundary means governance readiness only, not production state.

## L. Approval Protocol

Future 8W-4 implementation requires this exact approval phrase:

`批准 8W-4 Controlled Metadata-Smoke Output to Review-only Staging Boundary Smoke implementation`

Without this phrase, do not implement helper code, tests, runtime objects, review-only staging boundary objects, row reads, private collector inspection, Evidence Layer writes, production cases, production `analysis_run`, frontend/routes, or public/customer output.

## M. Forbidden Interpretations

Do not interpret this contract as:

- approval to implement 8W-4
- approval to create review-only staging boundary object now
- approval to run review-only staging runtime
- approval to parse rows
- approval to preview rows
- approval to write Evidence Layer
- approval to create production case
- approval to create production `analysis_run`
- approval to create production review queue items
- approval to inspect private collector source
- approval to read real exchange directories
- approval to generate B-end report runtime
- approval to generate Sandbox/public event runtime
- approval to generate report/export/download/public/final-delivery runtime
- approval to create frontend routes
- approval to create public/customer output
- official verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof
- prediction
- production score

The only current approval is this docs-only boundary contract and decision checkpoint.
