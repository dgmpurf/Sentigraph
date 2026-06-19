# Staging Import To Review Queue Gate v1

Status: architecture gate draft

Scope: future gate between review-only case staging import and review queue initialization

This document is design-only. It does not implement review queue runtime, staging import runtime, row parsing, Evidence Layer writes, production case creation, dedup, analysis, Summary Report generation, Sandbox fixture generation, B-end report generation, public event page generation, provider execution, collector jobs, real APIs, URL fetching, scraping, browser automation, or real LLM integration.

## 1. Purpose

This gate defines what must happen after staging import and before any staged evidence can enter an Evidence Review Queue.

Staging import completion does not create review queue items automatically unless a future phase explicitly implements and gates that behavior.

## 2. Core Rules

Review queue initialization requires a separate gate.

Dedup should run before analysis.

Review queue items should start with `review_needed`.

No Summary Report, Sandbox fixture, B-end report, public event page, Strategy Lab output, forecast output, or analysis result may be generated before governance is complete.

## 3. Required Inputs

Future review queue initialization should require:

- review-only case exists,
- staging import exists,
- staging import status is safe for review queue consideration,
- `privacy_stop=false`,
- rollback metadata exists,
- quarantine/rejection summaries are safe,
- default governance fields are present,
- coverage limitations are attached,
- latest human decision allows review queue initialization,
- no production case creation happened,
- no analysis inclusion happened.

## 4. Reviewer Actions

Review queue items should support:

- `approve`
- `reject`
- `mark_weak`
- `request_more_source`
- `merge_duplicate`

These actions should be human review records. They must not claim AI verified authenticity, official platform verification, full-web coverage, or causal proof.

## 5. Decision Effects

Rejected evidence stays audit-visible but excluded from analysis.

Weak evidence stays warning-marked.

Duplicate evidence must not amplify risk.

`approve` means the evidence may move to the next governance step. It does not by itself mean analysis inclusion, report generation, public display, Sandbox generation, or official verification.

`request_more_source` keeps the item in review status and should preserve source limitation warnings.

`merge_duplicate` should preserve duplicate history and prevent duplicate amplification.

## 6. Dedup Before Analysis

Dedup should run before any analysis-ready promotion.

The system should distinguish:

- unique evidence count,
- duplicate evidence count,
- duplicate group size,
- repetition signal if explicitly reviewed,
- rejected evidence count,
- weak evidence count.

Repeated submissions or repeated package rows must not inflate sentiment, risk, forecast, report, or Sandbox outputs.

## 7. Blocked Outputs

Before review queue, dedup, audit, and promotion are complete, the system must block:

- Summary Report,
- B-end report,
- Sandbox fixture,
- public event page,
- Strategy Lab output,
- Simulation Lab output,
- forecast output,
- risk score update,
- sentiment score update,
- production case update.

## 8. Future Phase Plan

Suggested future phases:

- 6R: Staging Import Runtime with tiny local fixture or controlled package.
- 6S: Review Queue Initialization Design.
- 6T: Review Queue Initialization Runtime.
- 6U: Dedup Preview before Analysis.
- 6V: Analysis-ready Promotion Gate.
- 6W: Manual analysis trigger from review-only case.

Each phase should preserve the same safety boundary: provider output is evidence, not truth.

## 9. Boundary Copy

Recommended UI text:

> Staged evidence is waiting for human review. It is not production evidence, not official verification, not full-web coverage, and not analysis-ready. Rejected evidence remains audit-visible but excluded. Weak evidence remains warning-marked. Duplicate evidence is collapsed before any analysis-ready promotion.

## 10. Non-Goals

This gate does not implement:

- automatic review queue creation,
- AI authenticity review,
- official API verification,
- production case promotion,
- dedup runtime,
- analysis runtime,
- report generation,
- Sandbox generation,
- public event generation,
- live crawling or URL fetching.
