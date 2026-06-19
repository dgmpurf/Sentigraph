# Review Queue Item Contract v1

## Purpose

This document defines the future `sentigraph_review_queue_item_v1` object shape for review-only case queues.

A review queue item is a human-review object created from a staged evidence candidate. It is not a production `EvidenceItem`, not analysis input, not public material, and not verified truth.

## Object Shape

```json
{
  "schema": "sentigraph_review_queue_item_v1",
  "review_item_id": "review_item_...",
  "review_case_id": "review_case_...",
  "staging_import_id": "staging_import_...",
  "staging_id": "staging_...",
  "request_id": "analysis_request_...",
  "package_name": "package-name",
  "created_at": "2026-06-19T00:00:00Z",
  "created_by": "local_reviewer",
  "queue_status": "review_needed",
  "evidence_candidate": {
    "evidence_type": "comment",
    "platform": "unknown",
    "source_url": "https://example.invalid/public-source",
    "title_preview": "Safe title preview",
    "body_text_preview": "Safe redacted body/comment preview",
    "created_at": "2026-06-19T00:00:00Z",
    "language": "zh",
    "safe_counts": {}
  },
  "governance": {
    "review_status": "review_needed",
    "verification_status": "source_url_provided_unverified",
    "trust_label": "medium_low",
    "analysis_included": false,
    "public_visible": false,
    "report_visible": false,
    "sandbox_visible": false,
    "dedup_required": true,
    "audit_required": true
  },
  "privacy": {
    "raw_author_id_present": false,
    "raw_author_name_present": false,
    "profile_url_present": false,
    "private_message_present": false,
    "passed": true
  },
  "dedup": {
    "dedup_status": "not_run",
    "duplicate_group_id": null,
    "duplicate_count": 1,
    "may_amplify_risk": false
  },
  "audit": {
    "source": "review_queue_initialization",
    "created_at": "2026-06-19T00:00:00Z"
  }
}
```

## Status Values

`queue_status` may be:

- `review_needed`
- `approved`
- `rejected`
- `marked_weak`
- `needs_more_source`
- `duplicate_merged`
- `privacy_hold`

Initialization should create queue items with `review_needed` only.

## Evidence Candidate Fields

The `evidence_candidate` object may contain only safe preview fields:

- `evidence_type`
- `platform`
- `source_url`
- `title_preview`
- `body_text_preview`
- `created_at`
- `language`
- `safe_counts`

The queue item carries redacted preview text only unless a future staging phase safely stores additional sanitized content.

## Governance Defaults

New queue items must keep conservative governance:

- `review_status=review_needed`
- `verification_status=source_url_provided_unverified`
- `trust_label=medium_low`
- `analysis_included=false`
- `public_visible=false`
- `report_visible=false`
- `sandbox_visible=false`
- `dedup_required=true`
- `audit_required=true`

Approval in the review queue must not automatically change `analysis_included` to true. A later promotion or analysis-readiness gate must decide that separately.

## Privacy Rules

Queue items must never include:

- raw author identifiers
- raw author names
- profile URLs
- private messages
- cookies
- tokens
- API keys
- passwords
- emails
- phone numbers
- browser session data
- raw package rows

If any forbidden value is detected, the item must not be initialized and the case should move to a privacy or safety review state.

## Dedup Fields

Queue initialization does not run deduplication.

The initial dedup state should be:

- `dedup_status=not_run`
- `duplicate_group_id=null`
- `duplicate_count=1`
- `may_amplify_risk=false`

Duplicate group assignment belongs to a later dedup preview/runtime phase.

## Contract Boundaries

A review queue item is:

- audit-visible
- review-only
- derived from a staged evidence candidate
- excluded from analysis by default
- excluded from public display by default
- excluded from report and Sandbox output by default

A review queue item is not:

- a production `EvidenceItem`
- an analysis input
- a public event source
- a report source
- official verification
- a full-web or full-platform sample
- proof of causal influence

