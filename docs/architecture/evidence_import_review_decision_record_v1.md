# Evidence Import Review Decision Record v1

Status: architecture contract draft

Scope: future human review decision after Evidence Import Preview and before Manual Evidence Import Job

This document is design-only. It does not implement review decision storage, UI, evidence import, backend routes, frontend code, provider execution, collector execution, API calls, URL fetching, scraping, analysis generation, Sandbox fixture generation, public event page generation, or report generation.

## 1. Purpose

Evidence Import Review Decision is the auditable human decision that allows or blocks a future manual import job.

Approval allows a future import job. It does not automatically import evidence rows, create a production case, run analysis, generate a Sandbox fixture, generate a public event page, or generate a B-end report.

Rejected or held packages should remain visible in audit records but must not be imported.

## 2. Suggested Object Shape

```json
{
  "schema": "sentigraph_evidence_import_review_decision_v1",
  "decision_id": "decision_req_20260618_example",
  "preview_id": "preview_req_20260618_example",
  "plan_id": "import_plan_req_20260618_example",
  "request_id": "req_20260618_example",
  "reviewer_label": "local_reviewer",
  "reviewed_at": "2026-06-18T00:00:00Z",
  "decision": "approve_import",
  "target_case_mode": "new_review_case",
  "target_case_id": null,
  "notes": "Package is suitable for review-only import. Coverage limits must remain visible.",
  "checklist": {
    "coverage_reviewed": true,
    "validation_reviewed": true,
    "privacy_reviewed": true,
    "no_raw_author_identifiers": true,
    "not_full_web_acknowledged": true,
    "review_needed_default_acknowledged": true,
    "trust_label_default_acknowledged": true,
    "dedup_required_acknowledged": true,
    "no_auto_analysis_acknowledged": true
  },
  "approved_defaults": {
    "review_status": "review_needed",
    "verification_status": "source_url_provided_unverified",
    "trust_label": "medium_low",
    "dedup_required": true,
    "audit_required": true
  },
  "audit": {
    "created_by": "local_reviewer",
    "created_at": "2026-06-18T00:00:00Z",
    "source": "manual_review"
  }
}
```

## 3. Decision Values

Allowed future decisions:

| Decision | Meaning | Import job allowed |
| --- | --- | --- |
| `approve_import` | Reviewer approves future manual import under selected defaults | Yes, later explicit job only |
| `reject_import` | Reviewer rejects package for import | No |
| `request_more_source` | Reviewer needs more coverage/source/validation information | No |
| `mark_limited_sample` | Reviewer allows limited-sample handling but keeps warnings prominent | Maybe, only if paired with explicit approval in future policy |
| `hold_for_privacy_review` | Reviewer blocks until privacy/legal/security review | No |

The MVP should treat only `approve_import` as eligible for a future import job.

## 4. Target Case Modes

| Target mode | Meaning | Recommended handling |
| --- | --- | --- |
| `new_review_case` | Create a new review-only case in a future import job | Recommended MVP |
| `existing_case` | Attach to an existing case selected by reviewer | Require explicit `target_case_id` |
| `reject_no_case` | Do not create or select a case | Use for reject/hold decisions |

Approval should not create the case immediately. It only authorizes a future Manual Evidence Import Job to create or select the case under audit.

## 5. Required Checklist

Future review UI should require the reviewer to acknowledge:

- coverage reviewed,
- validation reviewed,
- privacy reviewed,
- no raw author identifiers,
- not full-web coverage acknowledged,
- review-needed default acknowledged,
- trust-label default acknowledged,
- dedup required acknowledged,
- no automatic analysis acknowledged.

If any required checklist item is false, import approval should be blocked.

## 6. Approved Defaults

Approved defaults should remain conservative:

```json
{
  "review_status": "review_needed",
  "verification_status": "source_url_provided_unverified",
  "trust_label": "medium_low",
  "dedup_required": true,
  "audit_required": true
}
```

Reviewer approval must not automatically upgrade trust or verification. If a future official API source exists, higher verification status may require provider-specific proof plus human review.

## 7. Audit Requirements

Decision records should be immutable or append-only in future implementation.

Recommended audit behavior:

- never overwrite a previous decision silently,
- append a new decision event for changes,
- store reviewer label only, not credentials,
- store timestamps,
- store target-case intent,
- preserve rejected and held decisions,
- link decision to preview, import plan, and analysis request,
- keep no secret values in notes.

## 8. Privacy Blocker Policy

Reviewer cannot override privacy blockers without a future legal/security process.

Hard blockers should include:

- raw author identifiers present,
- raw author names present when not explicitly approved by future policy,
- profile URLs present,
- private messages present,
- non-public content present,
- cookies/sessions/profile paths present,
- missing privacy flags,
- minor-sensitive policy violation.

If a privacy blocker is found, the decision should be `hold_for_privacy_review` or `reject_import`.

## 9. Boundary Language

Use these terms:

- manual import,
- import preview,
- review decision,
- Evidence governance,
- `review_needed`,
- `source_url_provided_unverified`,
- `medium_low`,
- coverage limitation,
- selected / controlled public sample,
- evidence, not truth,
- provider output.

Avoid these terms:

- automatic full import,
- full-web coverage,
- official verified,
- real-time crawl,
- crawler integration,
- prediction guarantee,
- public report generated,
- case completed.

## 10. Current Non-Implementation Statement

This contract does not implement:

- review decision UI,
- review decision storage,
- manual evidence import job,
- evidence row import,
- production case creation,
- analysis generation,
- Sandbox fixture generation,
- public event page generation,
- B-end report generation,
- provider execution,
- collector jobs,
- real API calls,
- URL fetching,
- scraping,
- real LLM.

