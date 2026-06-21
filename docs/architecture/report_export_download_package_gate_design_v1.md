# Report Export Download / Package Gate Design v1

## Purpose

Report Export Download / Package Gate is the future governance gate between a local `FinalSummaryReportExportArtifact` record and any future controlled download, local file delivery, ZIP package, or signed delivery runtime.

The gate records whether an existing local export artifact may enter a future controlled delivery runtime. It does not create the delivery runtime and does not expose the artifact to users or networks.

## Core Principle

A local export artifact is not a public download.

The download/package gate only records whether an artifact may be considered by a future controlled delivery runtime. It is still not:

- a download route
- a ZIP or package file
- a public URL
- a signed URL
- a B-end report
- a Sandbox fixture
- a public event page
- an Evidence Layer write
- a production case
- a production review queue
- official verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof

Approval at this gate means only that a later runtime may be considered. It must not be interpreted as public release, customer delivery, file download, package generation, or downstream product generation.

## Required Prior Chain

The future gate can only be considered after all of the following exist and are internally consistent:

- `FinalSummaryReportExportArtifact`
- `FinalSummaryReportExportArtifactAudit`
- `FinalSummaryReportExportGate`
- `FinalSummaryReportExportGate.status == ready_for_future_export_runtime`
- `FinalSummaryReport`
- `FinalSummaryReportAudit`
- `FinalSummaryReportReviewGate`
- `FinalSummaryReportReviewGate.status` is ready for final report runtime
- `SummaryReportCandidate`
- `SummaryReportCandidateAudit`
- `ReportGenerationGate`
- `ReportGenerationGateAudit`
- `ManualAnalysisExecution`
- `ManualAnalysisExecutionAudit`
- `ManualAnalysisResultCandidate`
- `AnalysisResultBoundaryGate`
- `AnalysisResultBoundaryGateAudit`
- required upstream audit references

If any prior object is missing, inconsistent, privacy-held, revision-blocked, or missing required audit references, the download/package gate must return `needs_revision`, `blocked`, or `privacy_hold`.

## Required Preserved Boundaries

The gate must verify that the local export artifact metadata preserves:

- boundary block
- evidence scope
- coverage limitation
- weak evidence warning
- rejected evidence excluded
- duplicate evidence no amplification
- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- audit trace
- source and scope metadata
- local runtime-only artifact status

These boundaries must remain visible to any future download/package runtime. Future packaging, file naming, or download presentation must not hide, remove, weaken, or reword them into stronger claims.

## Allowed Inputs

The gate may inspect only safe local metadata records:

- `FinalSummaryReportExportArtifact`
- `FinalSummaryReportExportArtifactAudit`
- `FinalSummaryReportExportGate`
- `FinalSummaryReportExportGateAudit`
- `FinalSummaryReport`
- `FinalSummaryReportAudit`
- `FinalSummaryReportReviewGate`
- `SummaryReportCandidate`
- `ReportGenerationGate`
- `ManualAnalysisExecution`
- `ManualAnalysisResultCandidate`
- `AnalysisResultBoundaryGate`
- audit references embedded in those records

The gate must not inspect:

- original provider package rows
- `evidence_items.jsonl`
- `evidence_items.csv`
- external collector raw row files
- private collector project files
- browser profile data
- cookies, tokens, sessions, salts, passwords, API key values, or `.env` values
- raw author identifiers
- profile URLs
- private messages
- external URLs through network fetch

## Non-Goals

This design does not implement:

- runtime code
- download routes
- local download files
- ZIP or package files
- public URLs
- signed URLs
- B-end report generation
- Sandbox fixture generation
- public event page generation
- Evidence Layer write
- production case creation
- production review queue creation
- production dedup
- actual analysis engine execution
- real LLM calls
- real platform, search, vendor, provider, or collector API calls
- provider execution
- collector execution
- URL fetching
- scraping
- trust upgrade
- verification upgrade

## Future Runtime Recommendation

Future Phase 7U should implement a local gate writer that:

1. reads one local `FinalSummaryReportExportArtifact` metadata record
2. verifies its `FinalSummaryReportExportArtifactAudit`
3. verifies the upstream export gate, final summary report, final report review gate, summary report candidate, report generation gate, manual analysis execution, and analysis result boundary gate
4. confirms all boundary sections remain present
5. confirms the artifact remains local runtime-only
6. records a human delivery decision
7. writes only a local `sentigraph_report_export_download_package_gate_v1` object and append-only audit
8. keeps all download, package, public URL, signed URL, B-end, Sandbox, public-event, Evidence Layer, production case, and analysis flags false

Future 7U must not:

- create a download route
- create a ZIP or package file
- expose a public URL
- expose a signed URL
- generate a B-end report
- generate a Sandbox fixture
- generate a public event page
- write Evidence Layer
- create a production case
- call real LLMs
- call external APIs
- re-read original package rows
- fetch URLs

## Required Boundary Copy

Any future UI, CLI, or JSON output should include boundary copy equivalent to:

- This is a Report Export Download / Package Gate, not a download or package.
- The input is a local final summary report export artifact.
- The artifact remains local runtime-only.
- Provider output is evidence, not truth.
- The artifact is not official verification.
- The artifact is not full-web, full-platform, or full-thread coverage.
- Weak evidence remains warning-marked.
- Rejected evidence remains excluded.
- Duplicate evidence does not amplify risk, sentiment, coverage, or conclusions.
- Download routes, ZIP packages, signed URLs, public URLs, B-end reports, Sandbox output, and public event output require separate future gates or runtimes.

## Boundary Language

Use:

- Report Export Download / Package Gate
- future controlled delivery runtime
- local export artifact metadata
- local runtime-only artifact
- download/package eligibility gate
- evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- warnings must survive delivery
- downstream gates required

Avoid:

- download generated
- package generated
- ZIP ready
- public URL ready
- signed URL ready
- B-end report ready
- Sandbox ready
- public event ready
- official verified
- full-web coverage
- all-platform coverage
- causal proof
- client delivery complete

