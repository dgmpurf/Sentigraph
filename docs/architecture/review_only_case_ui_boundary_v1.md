# Review-Only Case UI Boundary v1

Status: architecture UI boundary draft

Scope: future UI copy and blocked-action rules for review-only cases

This document is design-only. It does not implement UI, review-only case runtime, evidence import, row parsing, Evidence Layer writes, production case creation, review queue creation, dedup, analysis, Sandbox fixture generation, public event page generation, B-end report generation, provider execution, collector jobs, real APIs, URL fetching, scraping, browser automation, or real LLM integration.

## 1. Purpose

The review-only case UI must prevent reviewers and demo viewers from mistaking staged evidence for production analysis.

The UI should make the case status obvious: internal review only, not analysis-ready, not public, not full-web coverage, not official verification, and not allowed to generate analysis or output until promotion.

## 2. Required UI Boundary Copy

Future UI must say:

- Review-only case is not a production case.
- Evidence is staged for governance only.
- Not analysis-ready.
- Not public.
- Not full-web coverage.
- Not full-platform coverage.
- Not full-thread coverage.
- Not official verification.
- Analysis, Sandbox and reports are disabled until promotion.
- Provider output is evidence, not truth.
- Imported rows default to `review_needed` / `source_url_provided_unverified` / `medium_low`.
- Rejected evidence is excluded by default.
- Weak evidence remains marked with warning.
- Public/report/Sandbox generation still requires a separate action after promotion.

## 3. UI Must Not Say

Future UI must not say:

- case 已完成,
- evidence 已验证,
- 全网分析完成,
- 官方验证,
- 可直接生成报告,
- 自动进入 Sandbox,
- 风险分数已更新,
- 真实监控已开始,
- official verification completed,
- full-web coverage completed,
- production case created,
- analysis ready by default,
- report ready by default.

## 4. UI Sections

### Review-only case identity

Show:

- review case id,
- linked request id,
- source import job id,
- source preview run id,
- status,
- visibility: `internal_review_only`,
- analysis included: false,
- public visible: false.

Primary copy:

> This is a review-only case. It is a governance container, not a production case.

### Package source and coverage

Show:

- package name,
- package role,
- package path label or safe local reference,
- coverage level,
- not full-web,
- not full-platform,
- not full-thread,
- validation report status,
- coverage note status.

Primary copy:

> Package validation confirms structure and safety metadata. It does not prove official verification or complete coverage.

### Governance status

Show:

- review status,
- verification status,
- trust label,
- low-trust warning,
- coverage warning,
- privacy status,
- promotion readiness.

Primary copy:

> Provider output is evidence, not truth. Governance must be completed before analysis inclusion.

### Evidence review status

Show:

- reviewed count,
- approved count,
- weak count,
- rejected count,
- needs more source count,
- still review_needed count.

Primary copy:

> Evidence left in review_needed is not analysis-ready. Rejected evidence is excluded by default.

### Dedup status

Show:

- dedup required,
- dedup completed,
- duplicate group count,
- duplicate amplification blocked,
- unresolved duplicate warning.

Primary copy:

> Duplicate evidence must not inflate sentiment, risk, or topic counts.

### Audit status

Show:

- audit timeline present,
- latest audit event,
- reviewer label present,
- rollback plan present,
- stale approval status.

Primary copy:

> Promotion requires an audit trail and a current human decision.

### Promotion readiness

Show:

- ready / not ready,
- blocking reasons,
- missing checklist items,
- requested analysis scope if any.

Primary copy:

> Promotion changes only analysis inclusion for an approved scope. Public pages, reports and Sandbox output require separate action.

### Blocked actions

Show disabled actions with reasons:

- Run analysis: disabled until promotion.
- Generate Summary Report: disabled until promotion and report gate.
- Generate Sandbox fixture: disabled until promotion and Sandbox gate.
- Generate public event page: disabled until promotion and public-page gate.
- Generate B-end report: disabled until promotion and report gate.
- Run Strategy Lab: disabled until promotion and strategy gate.

### Next manual steps

Show:

- complete privacy review,
- complete evidence review,
- run dedup,
- acknowledge coverage limitations,
- review audit timeline,
- resolve weak/rejected evidence,
- request promotion,
- rollback staged import if needed.

## 5. Status Labels

Recommended labels:

| Internal value | UI label | Meaning |
| --- | --- | --- |
| `draft` | Draft review-only case | Metadata only, no staged rows |
| `staging_pending` | Waiting for staging | Approved import job exists, rows not staged |
| `evidence_staged` | Evidence staged for review | Staged rows are still excluded from analysis |
| `governance_in_progress` | Governance in progress | Review, dedup, coverage, audit checks running |
| `governance_ready` | Ready to request promotion | Still not analysis-ready |
| `promotion_requested` | Promotion requested | Waiting for promotion gate |
| `promoted_to_analysis_ready` | Promoted for approved analysis scope | Output generation still requires separate action |
| `rejected` | Rejected | Cannot be promoted under this decision |
| `privacy_hold` | Privacy hold | Hard stop until privacy review |
| `rollback_pending` | Rollback pending | Analysis blocked |
| `rolled_back` | Rolled back | Staged rows inactive |
| `archived` | Archived | Inactive review record |

## 6. Warning Banner Examples

### Default review-only banner

> Review-only case: evidence is staged for governance only. It is not a production case, not analysis-ready, not public, not full-web coverage, and not official verification.

### Coverage banner

> This package is a selected sample. Coverage limitations must remain visible in any later analysis or report.

### Trust banner

> Imported rows default to `review_needed`, `source_url_provided_unverified`, and `medium_low`. Human review and dedup are required before analysis inclusion.

### Output blocked banner

> Analysis, Sandbox, public event pages, B-end reports, Strategy Lab output, and forecasts are disabled until explicit promotion and separate output gates.

### Privacy hold banner

> Privacy hold: promotion and output are blocked. Inspect safe reason codes only; do not print unsafe row content or raw identity fields.

## 7. Interaction Rules

Future UI should:

- keep blocked buttons visible but disabled with reason text,
- require explicit acknowledgement before promotion request,
- show coverage limitations near every action that might lead to analysis,
- show low-trust warning near evidence summaries,
- show rejected evidence exclusion status,
- show duplicate amplification status,
- show latest audit event,
- never auto-click or auto-run downstream actions.

Future UI should not:

- hide review-only status after promotion request,
- use success styling that implies production completion,
- display unsafe raw row payloads,
- display raw identity fields,
- display private messages,
- render generated reports from review-only data,
- route review-only cases into public pages.

## 8. Current Decision

Decision after this UI boundary design:

- `ready_for_phase_6P_review_only_case_runtime`

Recommended next phase:

- Add review-only case runtime with UI disabled-state contracts, but no evidence analysis or public output generation.
