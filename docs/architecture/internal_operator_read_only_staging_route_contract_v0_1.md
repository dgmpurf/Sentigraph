# Internal Operator Read-only Staging Route Contract v0.1

## A. Purpose

This document defines a future internal operator route contract for review-only staging candidates.

The future route is:

- internal operator only
- read-only
- metadata-only
- disabled by default or local-only until a later explicit implementation gate
- safe-summary only

The future route is not production import, not Evidence Layer write, not production case creation, not `analysis_run`, not report generation, not Sandbox/public event generation, and not public delivery.

This document is design only. It does not implement a backend route, frontend UI, router change, API bridge, persistent staging storage, collector integration, or production behavior.

## B. Route Candidate

Design-only candidate routes:

```text
GET /api/v1/internal/staging/review-only/candidates/{staging_candidate_id}
GET /api/v1/internal/staging/review-only/candidates
```

Only `GET` routes are in scope for this contract.

No `POST`, `PUT`, `PATCH`, or `DELETE` route is in scope.

No route implementation is approved by this document.

No state-changing operator decision is approved by this document.

## C. Allowed Response Fields

The future route may expose only safe metadata fields:

- `staging_candidate_id`
- `analysis_request_id`
- `provider_result_id`
- `package_name`
- `case_id_hint`
- `case_title_hint`
- `validation_status`
- `evidence_count`
- `source_count`
- `warning_count`
- `error_count`
- `metadata_summary`
- `validation_summary`
- `coverage_summary`
- `review_status`
- `promotion_status`
- `blockers`
- `warnings`
- `allowed_actions`
- `blocked_actions`
- `safety_flags`
- `audit_refs`
- `created_at`

Counts and summaries are governance metadata only. They are not evidence truth, official verification, full-platform coverage, or causal proof.

## D. Forbidden Response Fields

The future route must not expose:

- raw evidence rows
- raw comments
- raw author ids
- raw author names
- profile URLs as actual values
- private messages
- cookies
- sessions
- tokens
- passwords
- API keys
- browser profile paths
- absolute private paths
- `response_text`
- `generated_public_message`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

If any forbidden field is present in an upstream metadata object as an actual value, the future route must return a safe blocked response without leaking that value.

## E. Operator Access Boundary

The route is internal-only.

The route should be disabled by default or limited to local-only operator mode until a later explicit implementation gate approves otherwise.

The route must not provide:

- public user access
- C-end access
- B-end customer access
- external delivery
- public URL
- signed URL
- file-byte response
- download route
- object storage upload
- portal publication
- email delivery

The route must not be treated as a data collection mechanism or crawler.

## F. Allowed Actions Exposed as Labels Only

Allowed labels:

- `continue_review`
- `request_more_metadata`
- `mark_manual_review_required`
- `reject_package`
- `block_privacy_issue`
- `request_future_evidence_preview_gate`
- `request_future_dedup_gate`
- `request_future_promotion_gate`

These are labels only.

They are not executable actions.

The future route must not mutate state when returning these labels.

## G. Blocked Actions

The response must always include these blocked actions:

- `approve_production_evidence`
- `create_production_case`
- `start_analysis_run`
- `generate_report`
- `generate_public_event`
- `generate_public_response`
- `publish`
- `send`
- `post`
- `execute`
- `target_individuals`

These blocked actions communicate that the route cannot perform production import, analysis, report generation, public output, external delivery, or targeting behavior.

## H. Audit Behavior, Future Design Only

The future route may read safe audit refs.

The route must not append audit records.

The route must not mutate state.

The route must not create persistent staging storage.

State-changing operator decisions require a separate future design and explicit approval.

Future audit refs must not expose:

- raw evidence rows
- raw comments
- raw identifiers
- secrets
- absolute private paths
- response text
- production action payloads

## I. Preconditions Before Implementation

Before route implementation, Sentigraph needs:

- safe response schema
- operator auth or local-only access boundary
- disabled-by-default setting
- route tests proving safe fields only
- route tests proving no forbidden fields
- route tests proving no production actions
- route tests proving no persistent staging storage
- route tests proving no evidence row parsing
- route tests proving no collector execution
- route tests proving no URL fetch or scraping
- route tests proving no real API or real LLM calls
- audit strategy for read-only route access
- explicit approval for any implementation work

Until these preconditions are reviewed, the correct state is:

```text
ready_for_route_contract_review
not_ready_for_route_implementation
```
