# Analysis Requests Backend Golden Contract Inventory v1

Status: test/docs-only inventory. This document does not refactor production code or add runtime behavior.

## Purpose

This inventory records the backend contracts that should remain stable during future Analysis Requests modularization. It is intentionally contract-focused, not a line-by-line snapshot of implementation details.

## Route Families

The Analysis Requests backend currently exposes these route families under `/api/v1/analysis-requests`:

- request core and config
- provider result access through request detail / local result records
- case draft handoffs
- evidence import plans
- metadata-only import previews
- review decisions
- dry-run import jobs
- execution preflights
- synthetic row reader dry-runs
- limited real package row previews
- review-only cases
- review-only staging imports
- review queue initialization
- review action / audit timeline
- review queue completion gates
- dedup previews
- dedup group review audits
- analysis-ready promotion gates
- promotion decision audits
- manual analysis triggers
- manual analysis trigger audits
- analysis result boundary gates
- analysis result boundary gate audits
- manual analysis executions
- manual analysis execution audits
- manual analysis result candidates
- report generation gates
- report generation gate audits
- summary report candidates
- summary report candidate audits
- final summary report review gates
- final summary report review gate audits
- final summary reports
- final summary report audits
- final summary report export gates
- final summary report export gate audits
- final summary report export artifacts
- final summary report export artifact audits
- report export download/package gates
- report export download/package gate audits
- report export download/package artifacts
- report export download/package artifact audits
- report export public access / external delivery gates
- report export public access / external delivery gate audits

Future refactors may move route definitions into submodules, but these URL families must remain compatible unless an explicit migration is approved.

## Schema Family Groups

The schema file currently groups these major contract families:

- request core records and local provider job result records
- case draft and evidence import governance records
- review decision and import job records
- execution preflight and row-reader preview records
- review-only case and staging import records
- review queue initialization, action, audit, and completion records
- dedup preview and dedup group review records
- analysis-ready promotion gate and audit records
- manual analysis trigger, execution, result candidate, and audit records
- analysis result boundary gate and audit records
- report generation gate and audit records
- summary report candidate and audit records
- final summary report review gate, final report, and audit records
- final summary report export gate, artifact, and audit records
- report export download/package gate, artifact, and audit records
- report export public access / external delivery gate and audit records

Latest-chain schemas that must remain present before modularization:

- `ReportExportDownloadPackageArtifact`
- `ReportExportDownloadPackageArtifactAudit`
- `ReportExportPublicAccessExternalDeliveryGate`
- `ReportExportPublicAccessExternalDeliveryGateAudit`

Earlier-family sanity schemas:

- `FinalSummaryReport`
- `FinalSummaryReportExportArtifact`
- `ReportExportDownloadPackageGate`
- `ManualAnalysisExecution`
- `SummaryReportCandidate`

## Store Public Method Families

The current store facade exposes public methods by family:

- `create_*`
- `read_*`
- `list_*`
- `list_all_*`
- audit-specific list/read helpers
- request config and cancellation helpers

During modularization, `analysis_request_store.py` should remain a facade until imports are migrated safely. Public methods used by tests and routes should remain available while internals move.

## Runtime Directory Families

The runtime root remains `runtime/analysis_requests/` unless a separately approved migration is created. Current directory families include request records, provider result records, handoff/import records, review-only records, dedup records, analysis promotion records, manual analysis records, report records, export records, package records, and public-access / external-delivery gate records.

Runtime data must remain ignored by Git. The following must remain ignored:

- `runtime/analysis_requests/`
- `frontend/dist/`
- `.benchmarks/`

## Audit Record Families

Append-only audit families protect each human/governance decision:

- review decision records
- review queue action audits
- dedup group review audits
- promotion decision audits
- manual analysis trigger/execution audits
- analysis result boundary gate audits
- report generation gate audits
- summary report candidate audits
- final summary report review/final report/export audits
- report export download/package gate and artifact audits
- report export public access / external delivery gate audits

Audit records should remain append-only and safe-mode visible.

## Decision and Status Mapping Families

Decision/status mappings are deterministic and conservative. Future refactors should keep names stable unless a migration is explicitly approved:

- request revision -> needs revision
- block -> blocked
- privacy hold -> privacy hold
- approved future gate candidate -> ready for the named future runtime

Status names should not imply that analysis, report generation, public access, delivery, or production writes have already happened.

## No-Side-Effect and Boundary Flag Families

Current gate records and audit records use explicit flags for capabilities that must remain false unless a later approved runtime exists:

- no public download route now
- no file-byte response now
- no ZIP or binary archive now
- no public URL now
- no signed URL now
- no external delivery now
- no email now
- no object storage now
- no portal publication now
- no B-end report now
- no Sandbox or public event now
- no Evidence Layer write now
- no production case / review queue / dedup now
- no real API now
- no real LLM now
- no URL fetch now
- no scrape now
- no original package row re-read now
- no export artifact content read/copy/exposure now

## Public Access / External Delivery Non-Capability Assertions

The latest public-access / external-delivery gate is a governance gate only. It may record future candidate modes, boundary acknowledgements, and audit records. It must not:

- create a public download route
- create a file-byte response route
- generate a public URL
- generate a signed URL
- perform external delivery
- send email
- upload to object storage
- publish to a portal
- generate a ZIP
- expose runtime files
- expose absolute filesystem paths
- read, parse, copy, zip, or expose export artifact content
- read original package rows
- run provider or collector jobs
- call real APIs or LLMs

## Stability Requirements During Future Refactor

Future modularization must preserve:

- route URL families
- schema class names and aliases
- status and decision literal names
- runtime directory labels
- append-only audit behavior
- no-side-effect flags
- safe metadata policy
- no absolute path exposure
- no raw author identifier exposure
- provider output is evidence, not truth
- coverage limitation and human review boundaries

