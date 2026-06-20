# Summary Report Candidate Runtime Design v1

## Purpose

Summary Report Candidate Runtime is the future local runtime that may create a `SummaryReportCandidate` after a `ReportGenerationGate` is ready.

The runtime should transform an already bounded `ManualAnalysisResultCandidate` into a reader-oriented local report candidate while preserving every governance boundary from review, dedup, promotion, analysis, boundary, and report-gate stages.

This document is design-only. It does not implement runtime and does not generate any report candidate.

## Core Principle

A `SummaryReportCandidate` is a local draft candidate, not a final report.

It is not:

- a final Summary Report
- a B-end report
- a PDF export
- a Markdown export
- a briefing deck
- a Sandbox fixture
- a public event page
- official verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof
- legal, PR, or business guarantee

The candidate may organize bounded analysis for human review, but it must not upgrade evidence trust, verification status, coverage scope, or downstream readiness.

## Required Prior Chain

The future runtime can only be considered after:

- `ManualAnalysisExecution` exists.
- `ManualAnalysisResultCandidate` exists.
- `ManualAnalysisExecutionAudit` exists.
- `AnalysisResultBoundaryGate` exists.
- `ReportGenerationGate` exists.
- `ReportGenerationGateAudit` exists.
- `ReportGenerationGate.status` is `report_gate_ready_for_future_runtime`.
- The result candidate boundary block is present and complete.
- Rejected evidence is excluded.
- Weak evidence remains warning-marked.
- Duplicate evidence does not amplify risk, sentiment, coverage, or conclusions.
- Provider output is evidence, not truth.
- The candidate does not claim official verification.
- The candidate does not claim full-web, full-platform, or full-thread coverage.
- No privacy blocker exists.
- No unresolved needs-more-source blocker exists.

If any prior record is missing, unsafe, incomplete, privacy-held, or inconsistent, the future runtime must return `incomplete`, `blocked`, or `privacy_hold`.

## Allowed Inputs

The future runtime may read only safe local records:

- `ReportGenerationGate`
- `ReportGenerationGateAudit`
- `ManualAnalysisResultCandidate`
- `ManualAnalysisExecution`
- `ManualAnalysisExecutionAudit`
- `AnalysisResultBoundaryGate`
- `AnalysisResultBoundaryGateAudit`

It must not read:

- original provider package rows
- `evidence_items.jsonl`
- `evidence_items.csv`
- external collector output rows
- private collector project files
- browser profile data
- cookies, tokens, sessions, salts, passwords, API key values, or `.env` values
- raw author identifiers
- private messages
- URLs through network fetch

## Non-Goals

This phase does not design or implement:

- final Summary Report generation
- B-end report generation
- PDF export
- Markdown export
- briefing deck generation
- Sandbox fixture generation
- public event page generation
- Evidence Layer write
- production case creation
- production review queue creation
- production dedup
- actual analysis engine execution
- real LLM calls
- real platform, search, vendor, or provider API calls
- provider execution
- collector execution
- URL fetching
- scraping
- trust upgrade
- official verification upgrade

## Future Runtime Behavior

Future 7K should:

- verify the report gate is ready
- verify the report gate has an audit
- verify the manual analysis execution has an audit
- verify the result candidate boundary block is complete
- build a local `SummaryReportCandidate`
- preserve all boundary and warning sections
- preserve audit references
- keep downstream flags false
- keep export readiness false
- keep Sandbox and public event readiness false
- write only the local candidate object and candidate audit if that audit is separately designed

Future 7K must not:

- generate a final report
- generate PDF, Markdown, or deck files
- generate B-end report files
- generate Sandbox fixtures
- generate public event pages
- write Evidence Layer
- create production case
- call a real LLM
- call external APIs
- re-read original rows
- fetch URLs

## Candidate-Only Boundary Copy

Any future UI or JSON output should include boundary copy equivalent to:

- This is a local Summary Report Candidate.
- It is based on reviewed local evidence scope.
- It is not a final report.
- It is not official verification.
- It is not full-web, full-platform, or full-thread coverage.
- Provider output is evidence, not truth.
- Weak evidence remains warning-marked.
- Rejected evidence is excluded.
- Duplicate evidence does not amplify risk, sentiment, coverage, or conclusions.
- Export, B-end report, Sandbox, and public-event output require separate future gates.

## First Runtime Recommendation

Future 7K should implement a local candidate writer behind the existing `ReportGenerationGate`.

It should create `sentigraph_summary_report_candidate_v1` only when:

- the gate status is `report_gate_ready_for_future_runtime`
- report gate audit exists
- manual execution audit exists
- boundary gate audit exists
- all required sections can be populated from safe candidate/gate/audit records
- all downstream flags remain false

## Boundary Language

Use:

- Summary Report Candidate
- local draft candidate
- report candidate only
- bounded evidence scope
- candidate-only status
- evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- weak evidence warning
- rejected evidence excluded
- duplicate evidence does not amplify risk
- downstream export gate required

Avoid:

- report generated
- final report
- PDF ready
- Markdown ready
- deck ready
- B-end report ready
- public event ready
- Sandbox ready
- official verified
- full-web coverage
- all-platform coverage
- complete public opinion
- causal proof
- legal guarantee
- PR guarantee
