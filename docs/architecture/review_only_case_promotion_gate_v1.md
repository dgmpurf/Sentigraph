# Review-Only Case Promotion Gate v1

Status: architecture gate draft

Scope: future promotion gate from review-only case to analysis-ready scope

This document is design-only. It does not implement promotion runtime, review-only case runtime, evidence import, row parsing, Evidence Layer writes, production case creation, review queue creation, dedup, analysis, Sandbox fixture generation, public event page generation, B-end report generation, provider execution, collector jobs, real APIs, URL fetching, scraping, browser automation, or real LLM integration.

## 1. Purpose

The promotion gate is the future human-controlled checkpoint that may move a review-only case into an approved analysis-ready scope.

Promotion must be explicit. A review-only case must never become analysis-ready because rows were imported, previewed, staged, deduped, or reviewed. Promotion requires a recorded human decision and a completed checklist.

## 2. Core Rule

Before promotion:

- `analysis_included = false`
- `public_visible = false`
- `report_allowed = false`
- `sandbox_allowed = false`
- `strategy_lab_allowed = false`

After promotion:

- only the approved evidence scope may become analysis-ready,
- public/report/Sandbox/Strategy Lab generation still requires separate action-specific gates,
- rejected evidence remains excluded,
- weak evidence remains marked,
- coverage limitations remain visible.

## 3. Promotion Requirements

Promotion must require:

- no privacy blockers,
- validation errors equal 0,
- coverage limitations acknowledged,
- dedup completed,
- duplicate amplification blocked,
- review queue completed or minimum review threshold met,
- rejected evidence excluded from analysis,
- weak evidence marked with warning,
- audit timeline present,
- reviewer label present,
- promotion decision recorded,
- analysis inclusion changes only after explicit promotion,
- public/report/Sandbox generation still requires separate action.

## 4. Promotion Blocks

Promotion must be blocked by:

- `privacy_hold`,
- missing coverage note,
- missing validation report,
- missing audit,
- raw author identifiers,
- private or non-public content,
- full-web overclaim,
- full-platform overclaim,
- full-thread overclaim,
- dedup not run,
- duplicate amplification unresolved,
- review queue not initialized,
- all evidence still `review_needed` with no human review,
- no rollback plan,
- stale approval superseded by later hold/reject decision,
- missing reviewer label,
- missing rejected-evidence exclusion,
- missing weak-evidence warning.

## 5. Suggested Promotion Decision Object

```json
{
  "schema": "sentigraph_review_only_case_promotion_decision_v1",
  "decision_id": "promotion_decision_20260619_example",
  "review_case_id": "review_case_20260619_example",
  "reviewer_label": "human_reviewer",
  "decision": "approve_promotion",
  "approved_analysis_scope": "internal_analysis_only",
  "checklist": {
    "privacy_reviewed": true,
    "coverage_acknowledged": true,
    "dedup_completed": true,
    "review_queue_completed": true,
    "weak_evidence_marked": true,
    "rejected_evidence_excluded": true,
    "audit_reviewed": true,
    "not_full_web_acknowledged": true,
    "no_auto_publication_acknowledged": true
  }
}
```

Allowed `decision` values:

- `approve_promotion`
- `reject_promotion`
- `request_more_review`
- `hold_for_privacy`

Allowed `approved_analysis_scope` values:

- `internal_analysis_only`
- `public_sample_demo`
- `b_end_report_candidate`

`public_sample_demo` and `b_end_report_candidate` are not output generation. They only describe the intended later scope. Separate output gates are still required.

## 6. Checklist Semantics

### privacy_reviewed

The reviewer confirms that no privacy blocker remains. This includes confirming that unsafe fields and values are not exposed in analysis-ready evidence.

### coverage_acknowledged

The reviewer confirms that the package is not full-web coverage, not full-platform coverage, and not full-thread coverage unless a separate official contract proves otherwise.

### dedup_completed

Duplicate rows and duplicate URLs must be collapsed or marked so repeated submissions cannot inflate sentiment, risk, or topic counts.

### review_queue_completed

Every included evidence item must be reviewed or meet a documented minimum review threshold. Evidence left in `review_needed` must remain excluded unless the promotion scope explicitly permits a low-trust internal review sample with warnings.

### weak_evidence_marked

Weak or low-trust evidence remains visible as weak. Promotion must not upgrade it to verified evidence.

### rejected_evidence_excluded

Rejected evidence remains outside analysis counts and representative samples.

### audit_reviewed

The reviewer has inspected the audit timeline, import job id, source preview id, package references, and stale-approval status.

### not_full_web_acknowledged

The reviewer confirms that the promoted scope must not be described as full-web, full-platform, or official verification.

### no_auto_publication_acknowledged

The reviewer confirms that promotion does not create a public event page, Sandbox fixture, Summary Report, B-end report, Strategy Lab output, or forecast.

## 7. Stale Approval Rule

A promotion approval is stale if any later event changes:

- privacy status,
- validation report,
- coverage note,
- package reference,
- row staging audit,
- dedup result,
- review queue result,
- reviewer decision,
- rollback status,
- target analysis scope.

Stale approval must block promotion and require a new decision.

## 8. Promotion Output

A successful promotion decision may produce only:

- promotion decision record,
- updated review-only case lifecycle status,
- approved analysis scope marker,
- audit event,
- safe governance summary.

It must not directly produce:

- Summary Report,
- Sandbox fixture,
- public event page,
- B-end report,
- Strategy Lab output,
- forecast,
- real-time monitor,
- official verification claim.

## 9. Current Decision

Decision after this promotion gate design:

- `ready_for_phase_6P_review_only_case_runtime`

Recommended next phase:

- Implement review-only case runtime first, then implement this promotion gate as a later explicit phase.
