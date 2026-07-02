# Sentigraph Review-only Staging Boundary to Row Preview Gate Contract v0.1

## A. Contract Purpose

This contract defines how the 8W-4 metadata-only review-only staging boundary marker may become input to a future docs-only row preview gate decision.

The contract separates:

- completed 8W-4 review-only staging boundary marker
- future 8W-6 row preview gate decision docs
- any later row preview implementation
- any later Evidence Layer, production case, production `analysis_run`, frontend, report, Sandbox/public event, public/download/final-delivery, provider, collector, API, or LLM behavior

This contract is docs-only. It is not row preview, not row parsing, not review queue runtime, not Evidence Layer import, not production staging, not an API route, and not frontend integration.

## B. 8W-4 Boundary Object as Source

The only allowed future 8W-6 source is the safe local 8W-4 review-only staging boundary marker:

- schema: `sentigraph_metadata_smoke_review_only_staging_boundary_v0_1`
- phase: `8W-4`
- boundary_status: `review_only_staging_boundary_ready_for_manual_review`
- created_local_review_only_staging_boundary: `true`
- metadata_only: `true`
- human_review_required: `true`
- warning_count: `1`
- warning_manual_review_preserved: `true`
- review_only_staging_runtime_used: `false`
- review_queue_item_created: `false`
- production_review_queue_item_created: `false`
- row_preview_approved: `false`
- row files parsed: `false`
- original package rows read: `false`
- private collector source inspected: `false`
- real exchange directory read: `false`
- Evidence Layer write: `false`
- production case: `false`
- production `analysis_run`: `false`

The source object is a governance marker only. It is not truth, official verification, full-web coverage, full-platform coverage, causal proof, prediction, or production score.

## C. Review-only Staging Boundary Completion Definition

8W-4 is complete when:

- safe 8W-2 metadata-smoke input was accepted
- exact approved Dong/Sun package identity was preserved
- metadata-only status was preserved
- warning/manual-review state was preserved
- blocked production/public/action labels were preserved
- all runtime side-effect flags remained false
- no file reads were performed by the 8W-4 helper
- no private collector source was inspected
- no real exchange directory was read
- no row preview, Evidence Layer write, production case, or production `analysis_run` occurred

Completion does not mean row preview readiness. Completion only means a docs-only row preview gate decision can be considered.

## D. Row Preview Gate Definition

A row preview gate decision may define:

- whether a future row preview implementation may be considered
- which safe source object could be used
- which package identity restrictions apply
- which row files might later be eligible only after exact approval
- row-count limits
- redaction and minimization requirements
- forbidden fields
- no-production side-effect requirements
- human review requirements
- blocker categories
- tests required for a future implementation

A row preview gate decision must remain documentation only.

It must not:

- open row files
- parse rows
- create preview rows
- expose raw comments
- expose raw identities
- write Evidence Layer
- create production case
- create production `analysis_run`
- create review queue runtime
- add route/frontend/API
- generate report, Sandbox, public event, or delivery output

## E. Row Preview Implementation Separation

Row preview implementation is a separate future phase and is not approved by 8W-5.

Implementation would mean code that:

- opens an explicitly approved row file
- reads a bounded number of rows
- creates redacted row preview records
- validates field-level redaction
- emits preview-only output

Because that is materially more sensitive than a docs-only gate decision, implementation must require a later exact approval phrase after 8W-6. It must not be inferred from this contract.

## F. Warning/manual-review Handling

The 8W-4 warning/manual-review state must carry into any future 8W-6 docs-only gate:

- `warning_count = 1`
- `human_review_required = true`
- `warning_manual_review_preserved = true`
- selected sample only
- not full-web
- not full-platform
- not full-thread
- not official verification
- not causal proof
- not prediction
- not production score

The warning must not be converted into readiness for row preview implementation, import, analysis, reporting, publication, or delivery.

If a future gate cannot preserve the warning/manual-review state, it must stop.

## G. Allowed Future 8W-6 Docs-only Inputs

Future 8W-6 may inspect only safe docs and safe marker records:

- 8W-4 health report
- 8W-4 helper contract and tests as code references
- 8W-4 boundary output schema
- 8W-3 decision and architecture docs
- 8W-2 metadata-smoke report
- safe package identity strings already recorded in repo docs
- warning/manual-review status fields
- false side-effect flags

Future 8W-6 must not inspect:

- private collector project
- private collector source
- external export roots
- real exchange directories
- env-provided real paths
- `evidence_items.jsonl` content
- `evidence_items.csv` content
- `source_manifest.jsonl` rows
- `collection_log.jsonl` rows
- original package rows
- raw comments
- raw identities

## H. Forbidden Current and Future Actions

8W-5 and future 8W-6 do not approve:

- row preview implementation
- row parsing
- opening `evidence_items.jsonl`
- opening `evidence_items.csv`
- source manifest row parsing
- collection log row parsing
- original package row reading
- raw comment reading
- raw identity reading
- private collector source inspection
- real exchange directory read
- review queue runtime
- production review queue item creation
- EvidenceItem creation
- Evidence Layer write
- production case creation
- production `analysis_run` creation
- frontend/route/API
- B-end report runtime
- Sandbox/public event runtime
- report/export/download/public/final-delivery runtime
- public URL creation
- signed URL creation
- file-byte route creation
- object storage upload
- email sending
- portal publication
- generated response text
- publish, send, post, execute, or auto-execute behavior
- real API, real LLM, provider job, or collector job execution
- URL fetch or scrape

## I. Future Row Preview Blocker Categories

A future row preview implementation gate must block if any of these are unresolved:

- missing exact implementation approval phrase
- package identity mismatch
- warning/manual-review state not preserved
- row-count limit not defined
- redaction policy not defined
- raw author ID exposure risk
- raw author name exposure risk
- actual profile URL exposure risk
- raw comment overexposure risk
- private message risk
- cookie/session/token/API key/password/secret risk
- browser profile or collector runtime path risk
- absolute path or package path exposure risk
- private collector source inspection request
- real exchange directory traversal request
- Evidence Layer write request
- production case or production `analysis_run` request
- frontend/route request before a separate UI gate
- B-end report, Sandbox/public event, public/customer output, or delivery request
- generated response text request
- publish/send/post/execute/auto-execute request

Blocked output must use safe reason codes only and must not echo forbidden values.

## J. Future Redaction/minimization Principles

If a future row preview implementation is separately approved, it must follow these principles:

- preview rows are bounded and count-limited
- preview rows are redacted by default
- no raw author IDs
- no raw author names
- no actual profile URL values
- no private messages
- no secrets, cookies, tokens, sessions, passwords, API keys, salts, or browser profile paths
- no absolute filesystem paths
- no package paths in public output
- body/comment text should be minimized and capped
- text snippets should be preview-only and human-review-only
- row preview must not imply Evidence Layer import
- row preview must not imply official verification
- row preview must not imply full-web or full-platform coverage
- row preview must not amplify claims, sentiment, risk, or trust

## K. Evidence Layer / Production Boundary

Row preview gate decision and row preview implementation are not Evidence Layer import.

Future phases must keep these false unless a later separate production gate explicitly changes them:

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

Review-only preview means human inspection support only, not production state.

## L. Private Collector / Exchange Boundary

8W-5 and future 8W-6 must not:

- inspect private collector source
- modify private collector project
- run collector jobs
- run provider jobs
- access collector sessions, cookies, tokens, browser profiles, or secrets
- read real exchange directories
- use env-provided export roots
- traverse external package roots
- parse exported row files

Any future implementation that touches row files must be scoped by a later explicit package/row-preview contract and exact user approval.

## M. Approval Protocol

Future 8W-6 docs-only gate may proceed after an explicit task request for:

Phase 8W-6 Controlled Row Preview Gate Decision Docs-only

Future row preview implementation, if ever reached after 8W-6, must require a separate exact approval phrase such as:

`批准 8W-7 Controlled Row Preview Implementation`

Without that later exact phrase, do not implement helper code, tests, row parsing, preview row output, route/frontend, Evidence Layer writes, production cases, production `analysis_run`, reports, Sandbox/public events, or delivery surfaces.

## N. Forbidden Interpretations

Do not interpret this contract as:

- approval to implement row preview
- approval to parse rows
- approval to open row files
- approval to inspect private collector source
- approval to read real exchange directories
- approval to create preview rows
- approval to write Evidence Layer
- approval to create production case
- approval to create production `analysis_run`
- approval to create review queue runtime
- approval to create frontend routes
- approval to generate B-end report runtime
- approval to generate Sandbox/public event runtime
- approval to generate report/export/download/public/final-delivery runtime
- approval to create public/customer output
- approval to generate response text
- official verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof
- prediction
- production score

The only current decision is that 8W-4 is complete as a metadata-only boundary and may proceed to a future docs-only 8W-6 row preview gate decision.
