# Review-Only Case Lifecycle v1

Status: architecture lifecycle draft

Scope: future review-only case state machine before analysis-ready promotion

This document is design-only. It does not implement review-only case runtime, evidence import, row parsing, Evidence Layer writes, production case creation, review queue creation, dedup, analysis, Sandbox fixture generation, public event page generation, B-end report generation, provider execution, collector jobs, real APIs, URL fetching, scraping, browser automation, or real LLM integration.

## 1. Purpose

The review-only case lifecycle defines how future staged Evidence rows can move through governance without becoming analysis-ready by accident.

The lifecycle is intentionally conservative. Every state keeps analysis, public output, report output, Sandbox output, Strategy Lab output, and forecast output blocked until an explicit promotion gate approves analysis inclusion.

## 2. Lifecycle Overview

States:

- `draft`
- `staging_pending`
- `evidence_staged`
- `governance_in_progress`
- `governance_ready`
- `promotion_requested`
- `promoted_to_analysis_ready`
- `rejected`
- `privacy_hold`
- `archived`
- `rollback_pending`
- `rolled_back`

High-level flow:

```text
draft
-> staging_pending
-> evidence_staged
-> governance_in_progress
-> governance_ready
-> promotion_requested
-> promoted_to_analysis_ready
```

Exception flows:

```text
any state -> privacy_hold
any pre-promotion state -> rejected
staged / ready state -> rollback_pending -> rolled_back
any inactive state -> archived
```

## 3. State Definitions

### draft

Meaning:

- The review-only case shell exists or is being prepared.
- No real Evidence rows are staged.
- Package metadata may be referenced.

Allowed actions:

- inspect package metadata,
- inspect coverage note,
- inspect validation report,
- inspect limited redacted row preview,
- cancel or archive the draft.

Blocked actions:

- stage rows without approved import job,
- run analysis,
- generate reports,
- generate Sandbox or public event output,
- promote.

Required audit:

- creation event,
- source request id,
- package reference if known,
- safe-mode flags.

Transition conditions:

- `draft -> staging_pending` only after an approved import job exists.
- `draft -> rejected` if reviewer rejects the package.
- `draft -> archived` if the reviewer closes it without staging.

### staging_pending

Meaning:

- The review-only case has an approved import job and is waiting for future manual row staging import.

Allowed actions:

- verify import job approval,
- verify execution preflight,
- verify package hashes,
- prepare staging audit,
- cancel before staging.

Blocked actions:

- run analysis,
- create production case,
- create public output,
- skip directly to governance ready,
- promote.

Required audit:

- approved import job id,
- reviewer decision id,
- package reference,
- preflight id,
- stale-approval check.

Transition conditions:

- `staging_pending -> evidence_staged` only after future manual row staging import succeeds.
- `staging_pending -> privacy_hold` if privacy blocker appears.
- `staging_pending -> rollback_pending` if partial staging must be reversed.

### evidence_staged

Meaning:

- Rows have been staged into an internal review-only container in a future implementation.
- Rows remain excluded from analysis.

Allowed actions:

- inspect staged row summaries,
- inspect quarantine / rejection counts,
- initialize review queue,
- prepare dedup run,
- rollback staged import.

Blocked actions:

- run analysis,
- include rows in production case scoring,
- generate reports,
- generate Sandbox/public event output,
- claim verification.

Required audit:

- import audit id,
- row counts,
- privacy summary,
- quarantine/rejection summary,
- rollback pointer.

Transition conditions:

- `evidence_staged -> governance_in_progress` after review queue initialization.
- `evidence_staged -> rollback_pending` before analysis inclusion.
- `evidence_staged -> privacy_hold` if privacy blocker appears.

### governance_in_progress

Meaning:

- Review, dedup, coverage, trust, and audit checks are underway.

Allowed actions:

- approve, reject, mark weak, or request more source for evidence,
- run dedup in a future phase,
- inspect duplicate groups,
- inspect audit timeline,
- update coverage acknowledgement,
- rollback.

Blocked actions:

- promote without completed checks,
- run analysis,
- generate Summary Report,
- generate public event page,
- generate Sandbox fixture,
- generate B-end report.

Required audit:

- review decisions,
- dedup status,
- weak evidence notes,
- rejected evidence exclusion,
- coverage acknowledgement,
- reviewer label.

Transition conditions:

- `governance_in_progress -> governance_ready` only after review/dedup/coverage checks pass.
- `governance_in_progress -> privacy_hold` if privacy blocker appears.
- `governance_in_progress -> rollback_pending` if staged data must be removed.

### governance_ready

Meaning:

- Governance checks are complete enough to request promotion.
- The case is still not analysis-ready.

Allowed actions:

- request promotion,
- inspect governance summary,
- inspect audit timeline,
- rollback before promotion,
- request more review.

Blocked actions:

- run analysis before promotion,
- generate public/report/Sandbox outputs,
- auto-promote.

Required audit:

- governance readiness event,
- dedup completion reference,
- review queue completion or threshold reference,
- coverage limitation acknowledgement,
- rejected evidence exclusion status,
- rollback availability.

Transition conditions:

- `governance_ready -> promotion_requested` requires human decision.
- `governance_ready -> governance_in_progress` if new evidence or new blocker appears.
- `governance_ready -> privacy_hold` if privacy blocker appears.

### promotion_requested

Meaning:

- A reviewer has requested promotion from review-only to analysis-ready.
- Promotion gate checks must run and record a decision.

Allowed actions:

- evaluate promotion checklist,
- approve promotion,
- reject promotion,
- request more review,
- hold for privacy.

Blocked actions:

- analysis before gate approval,
- public/report/Sandbox generation before separate action,
- automatic publication.

Required audit:

- promotion decision id,
- reviewer label,
- checklist snapshot,
- analysis scope requested,
- stale-approval check.

Transition conditions:

- `promotion_requested -> promoted_to_analysis_ready` requires promotion gate approval.
- `promotion_requested -> governance_in_progress` if more review is requested.
- `promotion_requested -> privacy_hold` if privacy hold is requested.
- `promotion_requested -> rejected` if promotion is rejected.

### promoted_to_analysis_ready

Meaning:

- The review-only case has been explicitly promoted for approved analysis scope.
- This still does not automatically generate public pages, Sandbox fixtures, reports, or Strategy Lab outputs.

Allowed actions:

- enable analysis inclusion for approved evidence scope,
- create production / analysis-ready linkage,
- preserve review-only audit references,
- run downstream actions only after separate action-specific gates.

Blocked actions:

- automatic public event publication,
- automatic B-end report generation,
- automatic Sandbox fixture generation,
- automatic Strategy Lab output,
- expansion beyond approved analysis scope.

Required audit:

- promotion decision,
- approved scope,
- reviewer label,
- evidence inclusion summary,
- excluded/rejected/weak evidence summary.

Transition conditions:

- `promoted_to_analysis_ready -> rollback_pending` if promotion must be invalidated.
- `promoted_to_analysis_ready -> archived` after retention policy allows.

### rejected

Meaning:

- The review-only case or promotion request is rejected.

Allowed actions:

- view safe audit summary,
- archive,
- start a new request if needed.

Blocked actions:

- stage new rows under the rejected decision,
- run analysis,
- promote,
- generate outputs.

Required audit:

- rejection decision,
- reviewer label,
- reason code,
- safe package reference.

Transition conditions:

- `rejected -> archived` after review.
- A new attempt must create a new review-only case or append a new explicit decision, not silently reuse the rejected state.

### privacy_hold

Meaning:

- A privacy blocker or severe safety issue has appeared.

Allowed actions:

- inspect safe reason codes,
- perform privacy/security/legal review,
- archive,
- rollback if staged rows exist.

Blocked actions:

- row staging,
- analysis,
- promotion,
- public/report/Sandbox generation,
- printing unsafe content.

Required audit:

- privacy hold event,
- safe reason code,
- package reference,
- affected stage,
- reviewer or system label.

Transition conditions:

- `any state -> privacy_hold` if privacy blocker appears.
- `privacy_hold -> rollback_pending` if staged records must be removed.
- `privacy_hold -> governance_in_progress` only after a new explicit clearance decision.
- `privacy_hold -> rejected` if the package is unsafe.

### archived

Meaning:

- The review-only case is inactive.

Allowed actions:

- inspect safe audit summary,
- retain according to retention policy.

Blocked actions:

- new staging,
- analysis,
- promotion,
- public/report/Sandbox output.

Required audit:

- archive event,
- final status,
- retention note.

Transition conditions:

- terminal unless a future restore workflow explicitly appends a restore event.

### rollback_pending

Meaning:

- A staged or ready review-only case needs rollback before any analysis inclusion.

Allowed actions:

- compute rollback plan,
- mark staged rows inactive in future implementation,
- append rollback audit,
- preserve safe summaries.

Blocked actions:

- analysis inclusion,
- promotion,
- output generation,
- silent deletion of audit.

Required audit:

- rollback request,
- affected import job id,
- affected staged row counts,
- reason code.

Transition conditions:

- `rollback_pending -> rolled_back` after rollback completes.
- `rollback_pending -> privacy_hold` if rollback finds privacy blocker.

### rolled_back

Meaning:

- Staged records have been reversed or marked inactive in a future implementation.

Allowed actions:

- inspect rollback audit,
- archive,
- start a new governed attempt.

Blocked actions:

- analysis inclusion from rolled-back rows,
- promotion of rolled-back case,
- output generation.

Required audit:

- rollback event,
- final counts,
- inactive row references or safe summaries.

Transition conditions:

- `rolled_back -> archived` after review.

## 4. Mandatory Transition Rules

- `draft -> staging_pending` only after approved import job.
- `staging_pending -> evidence_staged` only after future manual row staging import.
- `evidence_staged -> governance_in_progress` after review queue initialization.
- `governance_in_progress -> governance_ready` only after review, dedup, and coverage checks.
- `governance_ready -> promotion_requested` requires human decision.
- `promotion_requested -> promoted_to_analysis_ready` requires promotion gate approval.
- Any state can move to `privacy_hold` if a privacy blocker appears.
- Staged or ready states may move to `rollback_pending` and `rolled_back` before analysis inclusion.

## 5. Current Decision

Decision after this lifecycle design:

- `ready_for_phase_6P_review_only_case_runtime`

Recommended next phase:

- Implement review-only case runtime with append-only lifecycle events and disabled output actions.
