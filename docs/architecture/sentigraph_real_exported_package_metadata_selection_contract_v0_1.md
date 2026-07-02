# Sentigraph Real Exported Package Metadata Selection Contract v0.1

## A. Contract Purpose

This contract defines the safe selection boundary for a future controlled metadata-only smoke against one real already-exported package metadata target.

The contract exists because 8V completed a local metadata/governance boundary chain, but 8V did not read real exported package data. 8W starts a separate selection planning phase that must keep private collector, real exchange directory, evidence row, Evidence Layer, production case, production `analysis_run`, frontend, route, export/download/public, final-delivery, and customer-output boundaries intact.

This contract is not runtime implementation. It is not a selector. It is not a package metadata smoke. It is not private collector access. It is not real exchange directory access. It is not row parsing. It is not Evidence Layer import. It is not production case or production `analysis_run` creation.

## B. Package Metadata Target Definition

A future package metadata target is allowed only when all of the following are true:

- The package has already been exported before the Sentigraph task starts.
- The target is selected by the user or by a user-approved safe metadata identifier.
- The target can be identified through metadata-only fields.
- The target can be referenced without emitting absolute private paths.
- The target does not require private collector source inspection.
- The target does not require row parsing.
- The target does not require original package row reading.
- The target does not require URL fetch, scrape, real API, real LLM, provider job, or collector job.
- The target has no known privacy blocker.
- The target has no known path traversal or path escape blocker.
- The target is suitable for metadata-only smoke, not production import.

An allowed target is a candidate for future manual metadata validation only. It is not truth, not official verification, not a production record, not a final report, and not public/customer delivery.

## C. Allowed Metadata Fields

Allowed safe metadata identity fields include:

- `package_name`
- `package_role`
- `case_id_hint`
- `provider_result_id`
- `provider_job_id`
- `request_id`
- `sentigraph_request_id`
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
- `package_index_ref`
- package index entry metadata
- manifest presence flag
- validation report presence flag
- source manifest presence flag
- coverage note presence flag
- `package_contract`
- `package_id`
- `package_root_ref` only as a configured-root label, not an actual absolute path
- `package_relative_path` only as safe metadata subject to path policy and never as public output
- `summary`
- `validation_summary`
- `coverage_note`
- `warnings`
- `errors`
- `nextAction`

Count summaries and presence flags may support target selection. They must not amplify truth, trust, sentiment, risk, coverage, report conclusions, or production score.

## D. Forbidden Metadata Fields and Values

Forbidden actual metadata fields and values include:

- private collector source code
- collector runtime internals
- collector sessions
- cookies
- tokens
- salts
- passwords
- API keys
- browser profile paths
- proxy credentials
- crawler internals
- anti-bot or captcha bypass details
- real exchange directory contents unless separately approved
- `evidence_items.jsonl`
- `evidence_items.csv`
- original package rows
- raw comments
- raw author identifiers
- actual author names
- actual profile URL values
- private messages
- absolute private paths
- runtime file paths
- package paths as emitted values
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

Safety marker fields are allowed only when they express non-export, removal, or false side-effect states, for example `raw_author_id_exported=false` or `no_private_messages=true`. Actual raw identifiers or secret-like values are never allowed.

## E. Selector Non-implementation Boundary

8W-1 does not implement a selector.

The following remain non-approved:

- selecting by scanning real export roots
- opening real package folders
- reading package indexes from real folders
- reading manifests from real folders
- reading validation reports from real folders
- parsing row files
- reading original package rows
- inspecting private collector source
- using env-provided real paths
- creating runtime objects
- changing backend code
- changing tests
- changing frontend code
- adding routes

Future 8W-2 must be separately approved before any helper, test, fixture, or metadata smoke is implemented.

## F. Future Metadata-only Smoke Contract

If 8W-2 is explicitly approved, the future smoke should:

- accept one explicit package metadata target
- operate on safe metadata only
- report metadata readiness, warning, or blocked status
- preserve selected-sample-only limitations
- preserve not-full-web, not-full-platform, and not-full-thread limitations
- preserve not-official-verification, not-causal-proof, not-prediction, and not-production-score limitations
- keep provider output as evidence candidate, not truth
- keep human review required
- keep all production, public, download, delivery, route, frontend, report, Sandbox, and Evidence Layer side effects false
- avoid emitting absolute private paths
- avoid emitting package paths as public values
- avoid reading row content
- avoid touching private collector source

Even with 8W-2 approval, row reads, production import, final delivery, public access, download generation, route/frontend integration, and customer output require separate later approvals.

## G. Blocker Contract

The future metadata-only smoke must block if any of these conditions appear:

- missing exact user approval for 8W-2 implementation
- missing explicit package metadata target
- target identity is ambiguous
- target requires private collector source inspection
- target requires real exchange directory traversal without approval
- target requires `evidence_items.jsonl` parsing
- target requires `evidence_items.csv` parsing
- target requires original package row reading
- target requires raw comment reading
- target requires raw identity reading
- target exposes actual profile URL values
- target exposes secret-like values
- target exposes absolute private paths
- target exposes runtime or package paths as output
- target has privacy blocker
- target has path traversal or path escape blocker
- target has validation errors unsuitable for smoke
- target asks for Evidence Layer write
- target asks for production case
- target asks for production `analysis_run`
- target asks for B-end report runtime
- target asks for Sandbox/public event runtime
- target asks for report/export/download/public/final-delivery runtime
- target asks for public URL, signed URL, file-byte route, object storage upload, email, portal publication, or customer delivery
- target asks for route/frontend integration
- target asks for provider or collector execution
- target asks for real API, real LLM, URL fetch, or scrape
- target asks for publish, send, post, execute, or auto-execute behavior

Blocked output must include only safe reason codes and must not echo forbidden values.

## H. Audit / Traceability Fields

Future 8W-2 metadata-only smoke may use safe traceability fields such as:

- `selection_decision_id`
- `selected_package_name`
- `selected_package_role`
- `selected_provider_result_id`
- `selected_provider_job_id`
- `selected_request_id`
- `selected_case_id_hint`
- `metadata_schema_version`
- `export_package_schema_version`
- `selection_method`
- `selected_by`
- `selected_at`
- `preflight_status`
- `privacy_status`
- `path_status`
- `validation_status`
- `warning_count`
- `error_count`
- `evidence_count_summary`
- `source_count_summary`
- `coverage_note_summary`
- `blockers`
- `warnings`
- `safe_mode`

Traceability must not contain absolute paths, raw identities, raw comments, package rows, row file contents, secret-like values, public URLs, signed URLs, delivery targets, or runtime file paths.

## I. Future Validation Plan

Future 8W-2 implementation should validate:

- exact approval phrase was present
- one metadata target is explicitly selected
- target identity uses allowed fields only
- row files are not parsed
- original package rows are not read
- private collector source is not inspected
- real exchange directories are not read unless the future task explicitly approves that exact action
- forbidden fields are blocked
- secret-like values are blocked
- raw identity values are blocked
- profile URL values are blocked
- absolute private paths are blocked
- path traversal and path escape are blocked
- Evidence Layer is not written
- production case is not created
- production `analysis_run` is not created
- report/export/download/public/final-delivery runtime is not used
- public URL, signed URL, file-byte route, object storage upload, email, portal publication, and customer delivery are not created
- B-end report runtime and Sandbox/public event runtime are not generated
- route/frontend is not changed
- provider/collector jobs are not run
- real APIs and real LLMs are not called
- URLs are not fetched and pages are not scraped

8W-1 docs-only validation remains limited to status checks, `git diff --check`, and static safety scans.

## J. Relationship to Local Exchange Reader / Package Resolver

The existing local exchange reader is disabled by default and metadata-only. It validates provider result metadata and keeps safe-mode flags false for row parsing, Evidence Layer writes, production case creation, production `analysis_run` creation, B-end report generation, Sandbox fixture generation, public event generation, provider execution, collector jobs, real APIs, real LLMs, URL fetching, scraping, secrets exposure, raw author identifier exposure, public download routes, file-byte responses, ZIP generation, public URLs, signed URLs, and external delivery.

8W-1 does not run the local exchange reader against real folders.

Future 8W-2 may reuse or wrap existing local metadata reader/resolver concepts only after exact approval, and only for metadata-only smoke. Codex must inspect actual current function names before implementation and must not invent runtime functions from this document.

If a package resolver exists or is added later, it must preserve:

- disabled-by-default behavior
- explicit user-approved target
- no private collector source inspection
- no row parsing
- no absolute private path exposure
- no Evidence Layer write
- no production case or production `analysis_run`
- no route/frontend/public/customer output

## K. Relationship to Private Collector

Private collector remains outside Sentigraph production ingestion.

This contract does not allow:

- modifying the private collector project
- reading private collector source
- running collector jobs
- inspecting collector sessions, cookies, tokens, profiles, or secrets
- using browser profile state
- using proxy or anti-bot internals
- reading real export folders
- accessing external collector export roots
- trusting env-supplied real paths without a separate explicit gate
- importing collector code into Sentigraph

Only already-exported package metadata may become a future target, and only after the user approves the exact future metadata-only smoke.

## L. Forbidden Interpretations

Do not interpret this contract as:

- approval to implement 8W-2
- approval to implement a selector
- approval to read real exchange directories
- approval to inspect private collector source
- approval to parse `evidence_items.jsonl`
- approval to parse `evidence_items.csv`
- approval to read original package rows
- approval to read raw comments
- approval to expose raw identities
- approval to write Evidence Layer
- approval to create production case
- approval to create production `analysis_run`
- approval to generate report/export/download/public/final-delivery runtime
- approval to create download package
- approval to create public URL
- approval to create signed URL
- approval to create file-byte route
- approval to upload object storage
- approval to send email
- approval to publish portal
- approval to create customer delivery
- approval to modify frontend or routes
- approval to generate B-end report runtime
- approval to generate Sandbox/public event runtime
- approval to call real APIs
- approval to call real LLMs
- approval to run provider or collector jobs
- approval to fetch URLs or scrape
- approval for production readiness
- approval for public readiness
- approval for customer readiness
- official verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof
- prediction
- production score

The only approved current outcome is a docs-only selection decision. The future 8W-2 implementation requires the exact approval phrase:

`批准 8W-2 Controlled Real Exported Package Metadata Smoke implementation`
