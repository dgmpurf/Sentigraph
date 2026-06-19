# Review-Only Case Staging Import Contract v1

Status: architecture contract draft

Scope: future staging import object for review-only cases

This document is design-only. It does not implement runtime code, row parsing, evidence import, Evidence Layer writes, production case creation, review queue creation, dedup, analysis, Sandbox fixture generation, public event page generation, B-end report generation, provider execution, collector jobs, real API calls, URL fetching, scraping, browser automation, or real LLM integration.

## 1. Contract Purpose

This contract defines a future object that records a manual staging import attempt into a review-only case.

The object must preserve governance, privacy, rollback, and audit state without authorizing analysis, report generation, public display, or production case creation.

## 2. Suggested Object Shape

```json
{
  "schema": "sentigraph_review_only_case_staging_import_v1",
  "staging_import_id": "...",
  "review_case_id": "...",
  "request_id": "...",
  "package_name": "...",
  "source_preview_run_id": "...",
  "source_import_job_id": "...",
  "created_at": "...",
  "created_by": "...",
  "execution_mode": "manual_staging_import",
  "status": "draft|preflight_passed|staging_started|partial|completed|blocked|privacy_stop|rolled_back",
  "limits": {
    "max_rows": 100,
    "full_scan": false,
    "analysis_inclusion": false,
    "public_visibility": false
  },
  "counts": {
    "rows_seen": 0,
    "accepted_for_review": 0,
    "quarantined": 0,
    "rejected": 0,
    "privacy_stop_at_row": null
  },
  "default_governance": {
    "review_status": "review_needed",
    "verification_status": "source_url_provided_unverified",
    "trust_label": "medium_low",
    "analysis_included": false,
    "dedup_required": true,
    "audit_required": true
  },
  "target": {
    "target_type": "review_only_case_staging",
    "review_case_id": "...",
    "production_case_id": null,
    "production_case_created": false
  },
  "rollback": {
    "rollback_available": true,
    "rollback_id": "...",
    "rollback_required_before_analysis": true
  },
  "readiness": {
    "state": "staged_for_review_only|blocked|privacy_stop",
    "can_run_analysis_now": false,
    "can_generate_report_now": false,
    "requires_review_queue_phase": true
  }
}
```

## 3. Field Explanations

| Field | Meaning |
| --- | --- |
| `schema` | Contract identifier. Must be `sentigraph_review_only_case_staging_import_v1`. |
| `staging_import_id` | Unique id for this staging import attempt. Must not be reused for a different attempt. |
| `review_case_id` | Review-only case receiving staged rows. |
| `request_id` | Analysis Request that produced the governed provider package chain. |
| `package_name` | Local package name from the approved package reference. |
| `source_preview_run_id` | Limited Real Package Row Preview used as source readiness evidence. |
| `source_import_job_id` | Dry-run import job or governed import job id that preceded staging. |
| `created_at` | Timestamp for the staging import record. |
| `created_by` | Reviewer or local actor label. It must not contain secrets or private identity data. |
| `execution_mode` | Must be `manual_staging_import`; not provider execution, crawling, or live collection. |
| `status` | Current staging import state. |
| `limits` | Runtime safety limits. `full_scan`, `analysis_inclusion`, and `public_visibility` must remain false for MVP. |
| `counts` | Safe row counts only. No raw row content or forbidden values. |
| `default_governance` | Defaults applied to every staged row. They do not prove source truth. |
| `target` | Confirms staging is limited to review-only case storage and does not create production cases. |
| `rollback` | Rollback availability and id. Rollback must be available before any future analysis inclusion. |
| `readiness` | Downstream readiness. Staging completion still requires review queue, dedup, audit, and promotion phases. |

## 4. Status Values

| Status | Meaning |
| --- | --- |
| `draft` | Object prepared but not executed. |
| `preflight_passed` | Required prior checks passed for a future manual staging run. |
| `staging_started` | Runtime began reading controlled rows in a future phase. |
| `partial` | Some rows staged; others quarantined/rejected or execution stopped safely. |
| `completed` | Controlled staging finished. This does not mean analysis-ready. |
| `blocked` | Gate failed before staging or during safe checks. |
| `privacy_stop` | A privacy blocker stopped staging. |
| `rolled_back` | Staged records were rolled back or marked inactive. |

## 5. Required Invariants

The object must always satisfy:

- `execution_mode=manual_staging_import`.
- `limits.full_scan=false`.
- `limits.analysis_inclusion=false`.
- `limits.public_visibility=false`.
- `default_governance.analysis_included=false`.
- `target.production_case_id=null`.
- `target.production_case_created=false`.
- `readiness.can_run_analysis_now=false`.
- `readiness.can_generate_report_now=false`.
- `readiness.requires_review_queue_phase=true`.
- rollback metadata is present.
- no raw forbidden values are logged or returned.

## 6. Forbidden Side Effects

Creating this object must not:

- write analysis-ready Evidence Layer rows,
- create production case records,
- create review queue items automatically,
- run dedup,
- run analysis,
- generate reports,
- generate Sandbox fixtures,
- generate public event pages,
- execute provider or collector jobs,
- fetch URLs,
- call real APIs,
- call real LLMs.

## 7. Readiness Semantics

`state=staged_for_review_only` means only that candidate rows are staged for future governance. It does not mean:

- official verification,
- full coverage,
- production readiness,
- report readiness,
- Sandbox readiness,
- risk score readiness,
- public display readiness.
