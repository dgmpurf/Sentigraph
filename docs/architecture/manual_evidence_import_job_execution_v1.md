# Manual Evidence Import Job Execution v1

Status: architecture design draft

Scope: future manual execution step after a Phase 6I dry-run import job

This document is design-only. It does not implement evidence import, row reading, row parsing, Evidence Layer writes, production case creation, review queue creation, dedup, analysis, Sandbox fixture generation, public event page generation, B-end report generation, provider execution, collector execution, real API calls, URL fetching, scraping, browser automation, official platform adapters, vendor adapters, MediaCrawler integration, OpenClaw production ingestion, or real LLM integration.

## 1. Purpose

The future manual import execution step is the controlled step after a reviewer has approved an Evidence Import Preview and Sentigraph has created a dry-run Manual Evidence Import Job.

The purpose is to specify how a later Phase 6K or beyond may safely read evidence rows from an approved local Evidence Export package and move them into a review-only evidence staging area or review-only case.

The execution step must preserve these principles:

- Provider output is evidence, not truth.
- Reviewer approval allows a future import path; it does not mean evidence is imported.
- Imported rows must start as `review_needed`.
- Imported rows must not enter analysis by default.
- Coverage limitations remain visible.
- Trust and verification remain conservative.
- Audit and rollback must exist before analysis inclusion.

## 2. Non-Goals

Manual import execution must not mean:

- automatic import without a human decision,
- live collection,
- provider execution,
- collector execution,
- automatic analysis,
- automatic Sandbox fixture generation,
- automatic B-end report generation,
- automatic public event page generation,
- trust upgrade to official verification,
- full-web coverage,
- full-platform coverage,
- full-thread coverage,
- prediction guarantee,
- crawler integration,
- real-world platform action.

## 3. Future Execution Chain

```text
Approved Review Decision
-> Dry-run Import Job
-> Execution Preflight
-> Row Reader
-> Evidence Row Sanitizer
-> Evidence Staging Area
-> Dedup Preview / Dedup Job
-> Review Queue Initialization
-> Audit Timeline
-> Optional manual promotion into case analysis
-> Later explicit Analysis/Sandbox/Report action
```

Every arrow is a gate. A later stage must not silently happen because an earlier stage exists.

| Stage | Meaning | Must not imply |
| --- | --- | --- |
| Approved Review Decision | Human reviewer approved future import under conservative defaults | Rows were imported |
| Dry-run Import Job | Phase 6I local job draft exists | Execution has started |
| Execution Preflight | Re-check current decision, preview, package, privacy, and rollback readiness | Rows are valid |
| Row Reader | Stream package rows under strict limits | Unbounded read or row logging |
| Evidence Row Sanitizer | Remove or block unsafe fields | Truth verification |
| Evidence Staging Area | Store safe candidates for review | Analysis inclusion |
| Dedup Preview / Dedup Job | Collapse duplicate influence before analysis | Final topic/risk calculation |
| Review Queue Initialization | Human governance begins | Automatic approval |
| Audit Timeline | Record execution facts | Immutable truth of source claims |
| Manual promotion | A later explicit step may include reviewed evidence in analysis | Automatic report/public output |

## 4. Execution Preconditions

Manual import execution can proceed only if all of these are true:

- Dry-run job exists.
- Dry-run job `readiness.state` is `ready_for_future_manual_import_execution`.
- The approved import decision exists.
- The approved decision is still the selected active decision.
- The latest decision is not `reject_import`, `request_more_source`, `hold_for_privacy_review`, or another superseding block.
- Package reference exists.
- Package manifest exists.
- Validation report exists.
- `validation.errors = 0`.
- Validation status is `passed` or `warn`.
- Coverage limitations are present.
- Privacy flags are present.
- Reviewer explicitly accepts selected or controlled sample limitations.
- Target case mode is a review-only case or an existing case with explicit id.
- Import mode is manual and audited.
- Runtime confirms no raw author identifiers are imported.
- Rollback and audit plan exists before row writes.

Manual import execution must block if any of these are true:

- Any privacy blocker exists.
- Missing validation report.
- Missing coverage note.
- Missing package manifest.
- Full-web, full-platform, or full-thread overclaim.
- Raw author id detected.
- Raw author name detected.
- Profile URL detected.
- Private message detected.
- Non-public content detected.
- Decision is not `approve_import`.
- Reviewer approval is stale or superseded.
- Dry-run job has any `*_now` execution flags set incorrectly.
- Target case is missing.
- Target case mode is invalid.
- Rollback plan is missing.

## 5. Row Reading Rules

Future implementation may read:

- `evidence_items.jsonl`
- optionally `evidence_items.csv` only as a fallback

Future implementation must not read or import:

- cookies,
- tokens,
- sessions,
- browser profile paths,
- private messages,
- raw author ids,
- raw author names,
- profile URLs,
- non-public content,
- account-only content,
- credential files,
- `.env` values,
- salts or local security material.

The row reader must:

- stream rows instead of loading unbounded large files,
- limit the first MVP to a configurable max row count,
- validate each row against Evidence Export v1,
- quarantine invalid rows,
- never print full row content to logs,
- never print author-like fields,
- preserve original row hashes for audit without exposing raw identifiers,
- fail closed on privacy violations,
- stop on hard privacy blockers before writing analysis-includable evidence.

## 6. Default Import Mapping

Future imported EvidenceItem candidates should default to:

```json
{
  "review_status": "review_needed",
  "verification_status": "source_url_provided_unverified",
  "trust_label": "medium_low",
  "analysis_included": false,
  "audit_required": true,
  "low_trust_warning_required": true,
  "coverage_warning_required": true
}
```

Additional mapping rules:

- `provenance_type = external_provider_package` unless the original package provenance is safer and more specific.
- `acquisition_mode = external_provider_package` unless the original acquisition mode is safe and reviewed.
- `source_url_present` is preserved from package metadata.
- `duplicate_count` is preserved if available.
- `duplicate_group_id` may be preserved only if safe, otherwise generated.
- `content_hash` is preserved or generated.
- `package_id` or `package_name` is attached.
- `import_job_id` is attached.
- `coverage_note` is attached.
- `validation_report` reference is attached.

Official API exception:

Only a future official API provider with verifiable proof and human review may upgrade `verification_status`. Vendor output remains `vendor_attested` / `medium_low` unless a later human review upgrades it with a documented reason. A higher source provenance label still does not prove that every claim in the content is true.

## 7. Staging-First Rule

Do not import directly into the final analysis pool.

The first MVP should import into one of these:

- review-only case,
- evidence staging area,
- `case_evidence_items` with `review_status=review_needed` and `analysis_included=false`.

Analysis inclusion should require a later explicit action after governance checks.

## 8. Dedup and Review Queue

Dedup must run before analysis.

Review queue must be initialized before analysis.

Rejected, weak, duplicate, or low-trust evidence must not amplify risk. Duplicate volume may remain as a repetition signal, but unique evidence should be the default basis for sentiment/topic/risk counts unless a later report explicitly explains how repetition is used.

Dedup results must be auditable:

- content hash method,
- duplicate group id,
- duplicate count,
- collapsed item count,
- rejected or merged item ids,
- reviewer-visible reason.

## 9. Audit and Rollback

Every import execution must record:

- who approved,
- when executed,
- package hash or manifest hash,
- validation report reference,
- import job id,
- row count attempted,
- row count accepted,
- row count quarantined,
- row count rejected,
- privacy checks,
- dedup status,
- review queue status,
- rollback file or rollback operation id.

Rollback must be possible before analysis inclusion. If analysis inclusion has already happened in a future phase, rollback should require a separate analysis invalidation or regeneration plan.

## 10. Recommended Implementation Phases

Recommended future sequence:

- 6K: metadata-only execution preflight runtime.
- 6L: row reader dry-run with synthetic fixture only.
- 6M: staging import with tiny local fixture.
- 6N: review queue initialization.
- 6O: dedup before analysis.
- 6P: manual analysis trigger after governance.
- 6Q: package import for Dong/Sun selected sample with explicit controlled-sample banner.

## 11. Boundary Language

Use:

- manual import execution,
- evidence staging,
- review-only case,
- `analysis_included=false`,
- `review_needed`,
- `source_url_provided_unverified`,
- `medium_low`,
- coverage limitation,
- selected / controlled public sample,
- evidence, not truth,
- audit and rollback,
- privacy stop.

Avoid:

- automatic import completed,
- full-web coverage,
- official verified,
- live crawl,
- crawler integration,
- prediction guarantee,
- public report generated,
- case completed,
- strategy recommendation generated.

## 12. Current Non-Implementation Statement

This document does not implement:

- evidence row import,
- evidence row parsing,
- Evidence Layer writes,
- production case creation,
- review queue creation,
- dedup,
- analysis generation,
- Sandbox fixture generation,
- public event page generation,
- B-end report generation,
- provider execution,
- collector jobs,
- real API calls,
- URL fetching,
- scraping,
- browser automation,
- official API provider,
- vendor API provider,
- real LLM.
