# Review-Only Case Import Contract v1

Status: architecture contract draft

Scope: future review-only case target for manual evidence import execution

This document is design-only. It does not implement review-only cases, evidence import, case writes, Evidence Layer writes, review queue creation, dedup, analysis, Sandbox fixture generation, public event pages, B-end reports, provider execution, collector jobs, real APIs, URL fetching, scraping, or real LLM.

## 1. Purpose

A review-only case is a future safe target for manual evidence import execution. It lets Sentigraph hold imported evidence candidates for governance before they can affect analysis, reports, public pages, or simulation surfaces.

The goal is to separate:

- package import,
- evidence governance,
- analysis inclusion,
- public or B-end presentation.

## 2. Review-Only Case Concept

A review-only case is a local case-like container with strict defaults:

```json
{
  "case_mode": "review_only",
  "analysis_included": false,
  "review_status": "review_needed",
  "verification_status": "source_url_provided_unverified",
  "trust_label": "medium_low",
  "public_output_allowed": false,
  "report_output_allowed": false,
  "sandbox_output_allowed": false
}
```

It can contain staged evidence candidates, governance metadata, coverage notes, audit timeline entries, and dedup/review status. It must not be presented as a completed production case.

## 3. Difference From Production Case

| Aspect | Review-only case | Production / analysis-ready case |
| --- | --- | --- |
| Purpose | Governance and safe staging | Analysis and reporting after governance |
| Analysis inclusion | `false` by default | Explicitly enabled after checks |
| Evidence status | `review_needed` | Reviewed or explicitly included |
| Verification | `source_url_provided_unverified` by default | May vary by governed evidence |
| Trust | `medium_low` by default for provider package rows | Based on reviewed source provenance |
| Public page | Blocked | Separate explicit action |
| Sandbox | Blocked | Separate explicit action |
| B-end report | Blocked | Separate explicit action |
| Rollback | Required before promotion | Requires invalidation if already analyzed |

## 4. Default Behavior

Review-only imported evidence must default to:

- `analysis_included=false`
- `review_status=review_needed`
- `verification_status=source_url_provided_unverified`
- `trust_label=medium_low`
- `audit_required=true`
- `coverage_warning_required=true`
- `low_trust_warning_required=true`

No public event page, Sandbox fixture, B-end report, strategy lab output, or analysis result should be generated during review-only import.

## 5. Allowed Actions After Import

Allowed actions in a review-only case:

- review evidence,
- inspect package metadata,
- inspect validation and coverage summaries,
- mark weak,
- reject,
- approve for later analysis inclusion,
- request more source,
- dedup,
- coverage review,
- audit review,
- rollback before analysis inclusion.

These actions are governance operations, not public or analytical output generation.

## 6. Blocked Actions Until Governance Complete

The following actions must remain blocked until governance criteria are met:

- analysis,
- Summary Report,
- B-end report,
- public event generation,
- Sandbox fixture generation,
- Strategy Lab / Simulation Lab output,
- automatic forecast,
- automatic recommendation,
- public sharing.

The UI and API should make this explicit. A review-only case is not a completed analysis case.

## 7. Promotion Criteria

Promotion from review-only to analysis-ready should require:

- no privacy blockers,
- validation errors equal 0,
- dedup completed,
- review queue initialized,
- rejected evidence excluded,
- weak evidence marked and warned,
- human review threshold met,
- coverage limitation acknowledged,
- import audit exists,
- rollback or invalidation plan exists,
- reviewer explicitly confirms analysis inclusion.

Suggested minimum threshold for the first MVP:

- all hard privacy checks pass,
- dedup completed for imported rows,
- all rows are either approved, marked weak, rejected, or quarantined,
- coverage limitation banner is attached to the case,
- at least one human reviewer confirms analysis inclusion.

## 8. Existing Case Attachment

Attaching to an existing case is higher risk than creating a new review-only case. It should require:

- explicit `target_case_id`,
- compatibility check with the existing case scope,
- coverage mismatch warning,
- trust mismatch warning,
- no privacy blockers,
- append-only audit entry,
- reviewer confirmation that the case may receive review-only evidence.

Even when attached to an existing case, imported evidence should default to `analysis_included=false`.

## 9. Boundary Language

Use:

- review-only case,
- evidence staging,
- governance before analysis,
- `analysis_included=false`,
- `review_needed`,
- `source_url_provided_unverified`,
- `medium_low`,
- coverage limitation,
- evidence, not truth.

Avoid:

- case completed,
- evidence verified,
- public report generated,
- full-web coverage,
- full-platform coverage,
- live crawl,
- official verification,
- strategy recommendation generated.

## 10. Current Non-Implementation Statement

This contract does not implement:

- review-only case runtime,
- evidence import,
- case writes,
- Evidence Layer writes,
- review queue creation,
- dedup,
- analysis,
- reports,
- Sandbox fixtures,
- public event pages,
- provider execution,
- collector jobs,
- real APIs,
- URL fetching,
- scraping,
- real LLM.
