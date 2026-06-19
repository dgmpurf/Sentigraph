# Staged Evidence Governance Defaults v1

Status: architecture policy draft

Scope: future default governance fields for evidence staged inside review-only cases

This document is design-only. It does not implement staging import runtime, backend schemas, frontend UI, row parsing, Evidence Layer writes, production case creation, review queue creation, dedup, analysis, report generation, Sandbox fixture generation, provider execution, live collection, real APIs, URL fetching, scraping, or real LLM integration.

## 1. Purpose

Future staged evidence must enter Sentigraph with conservative governance defaults.

These defaults prevent a staged row from being mistaken for verified, representative, analysis-ready, report-ready, public, or production evidence.

## 2. Required Defaults

Every future staged row should default to:

- `review_status=review_needed`
- `verification_status=source_url_provided_unverified`
- `trust_label=medium_low`
- `analysis_included=false`
- `public_visible=false`
- `report_visible=false`
- `sandbox_visible=false`
- `dedup_required=true`
- `audit_required=true`
- `coverage_warning_required=true`
- `low_trust_warning_required=true`
- `package_name` attached
- `import_job_id` attached
- `review_case_id` attached
- `row_index` or `source_row_id` attached
- `content_hash` generated or preserved
- `duplicate_group_id=pending`

These defaults apply even when the source row looks complete or comes from a well-formed package.

## 3. Trust And Verification Rules

Staging must not upgrade trust automatically.

Official API providers may only upgrade `verification_status` with provider proof and human review. The proof must identify the official source, authorized scope, timestamp, and relevant API response contract without exposing credentials or secrets.

Vendor output, private collector output, local snapshot output, mock output, and user-uploaded data remain `medium_low` by default. They may be useful evidence, but they are not official verification.

Manual promotion can change trust only with an audit reason. The audit reason should explain:

- which source was reviewed,
- what evidence supports the change,
- what coverage limits remain,
- who approved the change,
- when it was approved.

## 4. Review Status Defaults

Staged rows start with `review_needed`.

Later reviewer actions may change review status:

- `approved`
- `rejected`
- `marked_weak`
- `needs_more_source`
- `duplicate_merged`

These statuses should be recorded through a review queue or audit workflow, not by staging import itself.

## 5. Rejected And Weak Evidence

Rejected evidence must remain audit-visible but analysis-excluded.

Weak evidence must remain warning-marked. It may stay visible to reviewers, but analysis and reporting must show low-trust warnings if a later promotion gate allows weak evidence into a constrained analysis scope.

Staging must never hide rejected evidence from audit records, and must never allow rejected evidence to influence sentiment, risk, forecast, reports, Sandbox output, or B-end material.

## 6. Dedup Defaults

Future staged rows should preserve or generate `content_hash`.

Duplicate grouping should default to pending until a dedup phase runs.

Duplicate evidence must not amplify risk or sentiment. Repetition may be retained as a separate signal only after dedup and review explain the difference between unique content count and repetition count.

## 7. Coverage Warning Defaults

Every staged package row must inherit source coverage boundaries from the package and preview chain:

- selected sample,
- not full-web coverage,
- not full-platform coverage,
- not full-thread coverage,
- not official verification,
- not causal proof.

Coverage warnings must remain attached until a later promotion gate explicitly records reviewed scope.

## 8. Forbidden Defaults

Staging must not default any row to:

- `analysis_included=true`,
- `public_visible=true`,
- `report_visible=true`,
- `sandbox_visible=true`,
- `verification_status=verified_by_official_api`,
- `trust_label=high`,
- `review_status=approved`,
- `duplicate_group_id=unique` without dedup,
- production case attachment.

## 9. Future Runtime Checklist

Before a future staging runtime writes any staged row, it should verify:

- the review-only case exists,
- source package references match,
- privacy blockers are absent or safely quarantined,
- governance defaults are attached,
- coverage warnings are attached,
- rollback metadata exists,
- no raw author identifiers, profile URLs, private messages, credentials, emails, or phone numbers are stored.
