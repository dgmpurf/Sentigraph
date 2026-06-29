# Internal Operator UI Contract v0.1

## A. Purpose

This document defines a docs-only contract for a future internal operator UI for the review-only staging route.

It is not UI implementation.
It is not route implementation.
It is not auth implementation.
It is not authorization implementation.
It is not storage approval.
It is not evidence row preview approval.
It is not production import approval.

The contract defines what a future UI may display, must not display, and must not do before any frontend code is considered.

## B. Current Prerequisite State

- 8T-17 route skeleton milestone accepted after enabled fixture smoke.
- 8T-18 auth/local-only contract accepted.
- Route remains disabled by default.
- Enabled route mode remains synthetic/test-only.
- Future real metadata access requires separate explicit approval.
- No UI currently exists.
- No persistent staging storage exists.
- No evidence row preview is approved.
- No production import is approved.

## C. Intended Future UI User

Allowed future UI users:

- `internal_operator`
- `local_developer_operator`
- `security_reviewer`

Blocked users:

- `customer_user`
- `public_user`
- `c_end_user`
- `b_end_customer_user`
- `provider_system`
- `private_collector`

The UI must never be customer-facing or public-facing. The UI must not expose a C-end route, B-end route, provider callback route, private collector callback, or public customer page.

## D. Future UI Purpose

Future internal operator UI may only help inspect safe review-only staging metadata, such as:

- Staging candidate summary.
- Provider result metadata summary.
- Package label.
- `case_id_hint`.
- Validation status.
- Evidence/source counts.
- Warning/error counts.
- Safe coverage summary.
- Blockers/warnings.
- `allowed_actions` labels.
- `blocked_actions` labels.
- `safety_flags`.

It must not imply import, approval, production case creation, analysis run, report generation, Sandbox/public event generation, public output, or collector runtime integration.

## E. UI Display Contract

### Route Disabled / Setup Status

Allowed fields:

- Route status.
- Disabled reason.
- Synthetic mode label.
- Local-only/internal-only boundary label.
- Metadata-only/review-only boundary label.

Forbidden fields:

- Absolute filesystem paths.
- Tokens, cookies, sessions, passwords, API keys.
- Browser profile paths.
- Private collector export roots.

### Candidate List Metadata-only Table

Allowed fields:

- `staging_candidate_id`.
- `provider_result_id`.
- `package_name`.
- `package_role`.
- `case_id_hint`.
- `validation_status`.
- `evidence_count`.
- `source_count`.
- `warning_count`.
- `error_count`.
- Safe coverage summary.

Forbidden fields:

- Raw evidence rows.
- Raw comments.
- Raw author IDs/names.
- Profile URL actual values.
- Private messages.
- Evidence file contents.
- Absolute private paths.

### Candidate Detail Metadata-only Panel

Allowed fields:

- Safe candidate metadata.
- Provider result metadata summary.
- Validation summary.
- Coverage summary.
- Review-only status.
- Promotion boundary labels.

Forbidden fields:

- `evidence_items.jsonl` contents.
- `evidence_items.csv` contents.
- Raw row values.
- Raw comment text.
- Raw author identifiers.
- Secret-like values.

### Gate Summary Panel

Allowed fields:

- Package resolution status.
- Provider result status.
- Privacy status.
- Path status as safe code only.
- Metadata contract status.
- Evidence row boundary status.
- Staging status.

Forbidden fields:

- Absolute path values.
- Raw package paths.
- Private collector root values.
- Raw metadata dumps.

### Blockers / Warnings Panel

Allowed fields:

- Safe blocker codes.
- Safe warning codes.
- Human-readable safe boundary explanations.

Forbidden fields:

- Raw evidence snippets.
- Raw source file content.
- Private collector internals.

### Allowed Actions Labels Panel

Allowed labels:

- `continue_review`
- `request_more_metadata`
- `mark_manual_review_required`
- `reject_package`
- `block_privacy_issue`
- `request_future_evidence_preview_gate`
- `request_future_dedup_gate`
- `request_future_promotion_gate`

These are labels only. This phase does not approve active buttons or mutations.

### Blocked Actions Labels Panel

Allowed blocked labels:

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

These labels explain what the UI must not do.

### Safety Flags Panel

Allowed fields:

- Boolean safety flags such as `collector_run = false`, `real_api_called = false`, `real_llm_called = false`, `evidence_layer_written = false`, and `production_case_created = false`.

Forbidden fields:

- Any credential, raw identity value, raw row content, or absolute path value.

### Boundary Explanation Panel

Allowed content:

- Internal-only.
- Local-only candidate.
- Disabled by default.
- Synthetic/test-only if in fixture mode.
- Metadata-only.
- Review-only.
- Not production import.
- No Evidence Layer write.
- No production case.
- No `analysis_run`.
- No report runtime.
- No Sandbox/public event runtime.
- No public route.
- No collector runtime integration.

### Audit Readiness Placeholder

Allowed:

- Docs-only placeholder stating that future audit must be append-only and safe-metadata-only.

Forbidden:

- Actual audit append.
- Review queue creation.
- Storage write.
- Raw data capture.

## F. Forbidden UI Display

The future UI must not display:

- Raw evidence rows.
- Raw comments.
- Raw author IDs/names.
- Profile URL actual values.
- Private messages.
- Cookies / sessions / tokens / passwords / API keys.
- Browser profile paths.
- Absolute private paths.
- `evidence_items.jsonl` / `evidence_items.csv` contents.
- `response_text`.
- `generated_public_message`.
- `target_user_list`.
- `persuasion_score`.
- `truth_score`.
- `official_verified`.
- `prediction_probability`.
- `psychological_profile`.
- `personality_diagnosis`.

## G. Forbidden UI Actions

The future UI must not include buttons or CTAs for:

- Approve production evidence.
- Create production case.
- Start `analysis_run`.
- Generate report.
- Generate public event.
- Generate public response.
- Publish.
- Send.
- Post.
- Execute.
- Target individuals.
- Download package.
- Export data.
- Open raw file.
- Open private collector.
- Refresh live collector.
- Fetch URL.
- Scrape page.

Allowed future UI labels may include only non-mutating or future-gate labels:

- `continue_review`
- `request_more_metadata`
- `mark_manual_review_required`
- `reject_package`
- `block_privacy_issue`
- `request_future_evidence_preview_gate`
- `request_future_dedup_gate`
- `request_future_promotion_gate`

This phase must not implement any action.

## H. UI State and Wording Contract

Future UI must clearly label:

- Internal-only.
- Local-only candidate.
- Disabled by default.
- Synthetic/test-only if in fixture mode.
- Metadata-only.
- Review-only.
- Not production import.
- No Evidence Layer write.
- No production case.
- No `analysis_run`.
- No report runtime.
- No Sandbox/public event runtime.
- No public route.
- No collector runtime integration.

The UI wording must not imply that a package has been imported, verified, approved, analyzed, reported, published, sent, or made public.

## I. Empty / Denied / Disabled States

Safe UI empty states:

- Route disabled.
- Operator auth required.
- Operator role required.
- Local-only required.
- Synthetic mode only.
- Candidate not found.
- Privacy hold.
- No candidates available.

All states must avoid leaking paths, raw metadata values, row content, secrets, or collector internals.

## J. Implementation Prerequisites

Before any UI implementation:

1. UI contract accepted.
2. Auth/local-only contract accepted.
3. Route remains disabled by default.
4. Safe backend response schema stable.
5. Separate explicit user approval.
6. Targeted frontend safety tests.
7. Browser smoke.
8. No public / C-end / B-end alias.

Any UI implementation request must be treated as a new phase, not as approval embedded in this contract.

## K. Explicit Non-goals

- No UI implementation now.
- No frontend code now.
- No backend code now.
- No auth implementation now.
- No authorization implementation now.
- No storage now.
- No evidence row preview now.
- No production import now.
- No Evidence Layer write now.
- No production case / `analysis_run` now.
- No report runtime.
- No Sandbox / public event runtime.
- No collector runtime integration.
- No public / C-end / B-end route.
