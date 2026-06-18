# Evidence Import Audit and Rollback v1

Status: architecture contract draft

Scope: future audit and rollback model for manual evidence import execution

This document is design-only. It does not implement audit storage, rollback execution, evidence import, Evidence Layer writes, case writes, row parsing, review queue creation, dedup, analysis, Sandbox fixture generation, public event pages, B-end reports, provider execution, collector jobs, real APIs, URL fetching, scraping, or real LLM.

## 1. Purpose

Manual evidence import execution must be auditable and reversible before analysis inclusion. The audit layer records what was approved, what package was used, what rows were attempted, what was accepted or blocked, and how rollback can be performed.

Audit records are governance evidence. They are not proof that package content is true, complete, or officially verified.

## 2. Suggested Audit Object

```json
{
  "schema": "sentigraph_evidence_import_audit_v1",
  "audit_id": "audit_20260618_example",
  "import_job_id": "manual_import_job_20260618_example",
  "decision_id": "review_decision_20260618_example",
  "package_name": "example-package",
  "started_at": "2026-06-18T00:00:00Z",
  "finished_at": "2026-06-18T00:00:10Z",
  "status": "completed",
  "counts": {
    "rows_seen": 0,
    "accepted_for_review": 0,
    "quarantined": 0,
    "rejected": 0
  },
  "privacy": {
    "privacy_stop_triggered": false,
    "reason": null
  },
  "rollback": {
    "rollback_available": true,
    "rollback_id": "rollback_20260618_example",
    "analysis_inclusion_blocked_until_review": true
  }
}
```

## 3. Status Values

| Status | Meaning |
| --- | --- |
| `completed` | Import execution finished with no hard stop |
| `partial` | Some rows were accepted and some quarantined or rejected |
| `failed` | Execution failed before a safe result was created |
| `rolled_back` | Previously written staging records were rolled back |
| `privacy_stop` | Execution stopped because of privacy or forbidden-field violation |

`completed` does not mean analysis-ready. It only means the execution stage finished.

## 4. Row-Level Audit Summary

The audit should include row-level summaries without printing row content:

- row index,
- source row id or row hash,
- staging id if created,
- row status,
- reason codes,
- privacy check result,
- validation check result,
- content hash prefix,
- dedup requirement.

The audit must not include full title/body/comment text, raw author values, private messages, credentials, cookies, tokens, sessions, or browser profile paths.

## 5. Package-Level Audit Summary

Package-level audit should include:

- package name,
- package role,
- package path label or safe local reference,
- manifest hash,
- validation report hash or reference,
- coverage note hash or reference,
- import job id,
- review decision id,
- reviewer label,
- execution timestamp,
- row count attempted,
- row count accepted for review,
- row count quarantined,
- row count rejected,
- privacy stop status,
- rollback id.

Package audit should preserve enough information to reproduce governance decisions without exposing unsafe content.

## 6. Rollback Requirements

Rollback must be available before analysis inclusion.

Rollback should be able to:

- remove or mark inactive staged evidence rows from a specific import job,
- reverse review-only case attachments for that import job,
- preserve audit trail,
- preserve rejected/quarantined evidence summaries for review,
- block analysis until rollback state is resolved,
- report rollback counts.

Rollback must not silently delete audit records. It should append a rollback event.

## 7. Immutable Decision Chain

The decision chain should be append-only:

```text
Import Preview
-> Human Review Decision
-> Dry-run Import Job
-> Execution Preflight
-> Import Audit
-> Rollback Audit if needed
```

Do not overwrite old review decisions. If a reviewer changes their mind, append a new decision and mark earlier decisions as superseded by reference.

## 8. Stale Approval Detection

Execution must detect stale approval.

An approval is stale if:

- a newer decision exists for the same request,
- package manifest hash changed,
- validation report changed,
- coverage note changed,
- privacy summary changed,
- target case changed without explicit confirmation,
- dry-run job safe mode changed,
- reviewer checklist is no longer complete.

Stale approval should block execution and require a new review decision.

## 9. Superseded Decision Behavior

If a later decision is:

- `reject_import`,
- `request_more_source`,
- `hold_for_privacy_review`,
- another policy-defined block,

then previous `approve_import` decisions must not be executable unless a reviewer explicitly selects and re-approves a safe decision under the current package state.

The audit should record the superseding decision id.

## 10. Privacy Stop Behavior

Privacy stop is a hard gate.

When privacy stop is triggered:

- stop row processing,
- do not import additional rows,
- do not create analysis-includable evidence,
- record safe reason code,
- avoid printing row content,
- avoid printing author-like fields,
- keep package in review/hold state,
- require privacy/legal/security review before retry.

Examples:

- raw author id detected,
- raw author name detected,
- profile URL detected,
- private message detected,
- credential-like field detected,
- cookie-like field detected,
- token-like field detected,
- session-like field detected,
- browser profile path detected.

## 11. Recovery After Partial Import

If partial import happens in a future implementation:

- keep accepted rows in review-only state,
- keep quarantined rows excluded from analysis,
- keep rejected rows visible only in audit,
- block analysis until reviewer resolves partial state,
- allow rollback of all rows from the import job,
- allow retry only with a new audit entry.

Partial import must not silently become analysis-ready.

## 12. Rejected Evidence Audit

Rejected evidence should remain visible for audit but excluded from analysis.

Recommended storage:

- safe row hash,
- reason code,
- row index,
- package name,
- import job id,
- rejected timestamp,
- reviewer or system reason.

Do not store unsafe raw row payloads just to preserve rejected evidence.

## 13. Current Non-Implementation Statement

This contract does not implement:

- audit storage,
- rollback operation,
- row reading,
- row parsing,
- Evidence Layer writes,
- case writes,
- review queue creation,
- dedup,
- analysis,
- report generation,
- Sandbox fixture generation,
- public event pages,
- provider execution,
- collector jobs,
- real APIs,
- URL fetching,
- scraping,
- browser automation,
- real LLM.
