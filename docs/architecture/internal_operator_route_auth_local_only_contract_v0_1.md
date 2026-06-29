# Internal Operator Route Auth and Local-only Contract v0.1

## A. Purpose

This document defines a docs-only contract for future internal operator access to the review-only staging route.

It is not auth implementation.
It is not authorization implementation.
It is not route expansion.
It is not UI approval.
It is not persistent storage approval.
It is not evidence row preview approval.
It is not production import approval.

The purpose is to define the minimum access, denial, and audit boundaries that must be accepted before any future runtime implementation is considered.

## B. Current Route State

Existing route family:

```text
GET /api/v1/internal/staging/review-only/candidates
GET /api/v1/internal/staging/review-only/candidates/{staging_candidate_id}
```

Current route state:

- Route remains disabled by default.
- Enabled mode is synthetic/test-only.
- Route is metadata-only and review-only.
- Route exposes safe metadata only.
- No evidence row preview.
- No persistent storage.
- No production import.
- No Evidence Layer write.
- No production case.
- No `analysis_run`.
- No public / C-end / B-end customer route.

## C. Actor Definitions

### internal_operator

An internal Sentigraph operator role label for future local-only review-only staging work. This actor may be considered for future local-only access only after a separate approved implementation gate.

### local_developer_operator

A local developer/operator role label for local development and smoke checks. This actor may be considered for future local-only access only after a separate approved implementation gate.

### security_reviewer

A reviewer role label for checking privacy, path exposure, raw identifier exposure, and route boundary behavior. This actor may be considered for future docs-only or local-only review contexts, but no runtime access is implemented in this phase.

### customer_user

A customer-facing user. This actor must not access the internal operator route.

### public_user

A public internet user. This actor must not access the internal operator route.

### c_end_user

A C-end product user. This actor must not access the internal operator route.

### b_end_customer_user

A B-end customer user. This actor must not access the internal operator route.

### provider_system

An external or internal provider system. This actor must not access the internal operator route directly.

### private_collector

The private collector project or process. It must not access the internal operator route directly and must not be integrated as a Sentigraph internal crawler or HTTP/API bridge by this contract.

Only `internal_operator` and `local_developer_operator` may be considered for future local-only access. `security_reviewer` may be considered for future review-only checks. `customer_user`, `public_user`, `c_end_user`, `b_end_customer_user`, `provider_system`, and `private_collector` must not access this route.

## D. Local-only Boundary

Future local-only requirement:

- Route must remain disabled by default.
- Future enabled access must require explicit local operator gate.
- Future access must be local-only / internal-only.
- No public internet exposure.
- No customer-facing route.
- No C-end / B-end alias.
- No external provider callback.
- No HTTP/API bridge to private collector.
- No browser profile / cookie / session transfer.
- No absolute filesystem path exposure.

This is a contract only, not implementation.

## E. Future Auth / Authorization Contract

Future minimum policy:

- No anonymous access.
- No query-string token access.
- No hardcoded token in docs/code.
- No cookie/session-based collector credentials.
- No reuse of private collector browser/login/profile state.
- Access must be operator-role gated before any real metadata route expansion.
- Synthetic fixture mode may remain test-only but must not imply production access.
- Failed auth/locality checks must return safe error response.

Future implementation must not introduce sessions, cookies, tokens, accounts, browser profile transfer, or private collector credentials without a separate explicit approval gate.

## F. Safe Denial Response Contract

Future safe errors:

- `route_disabled`
- `operator_auth_required`
- `operator_role_required`
- `local_only_required`
- `synthetic_mode_only`
- `not_found`
- `privacy_hold`

For all denial responses:

- `schema = internal_operator_review_only_staging_error_v0_1` or future compatible safe error schema.
- `metadata_only = true`.
- `review_only = true`.
- `path_exposed = false`.
- `raw_metadata_exposed = false`.
- No absolute paths.
- No raw comments.
- No raw author identifiers.
- No evidence rows.
- No secrets.
- No `response_text`.
- No `generated_public_message`.
- No `target_user_list`.
- No `persuasion_score`.
- No `truth_score`.
- No `official_verified`.
- No `prediction_probability`.
- No `psychological_profile`.
- No `personality_diagnosis`.

Denial responses must explain the boundary code without leaking paths, private collector internals, package content, credentials, or raw evidence values.

## G. Audit / Logging Contract

Docs-only design:

- Future auth/local-only decisions may need append-only audit records.
- Current phase does not implement audit.
- Future audit must not include secrets, cookies, tokens, raw identifiers, absolute paths, raw evidence rows, or private collector profile data.
- Audit must log only safe metadata such as decision code, route family, operator role label, timestamp, blockers, warnings, and boundary flags.

Audit records must be governance evidence, not a second channel for leaking forbidden data.

## H. Explicit Non-goals

- No auth implementation now.
- No authorization implementation now.
- No UI implementation now.
- No persistent storage now.
- No production import now.
- No evidence row preview now.
- No Evidence Layer write now.
- No production case / `analysis_run` now.
- No B-end report runtime.
- No Sandbox / public event runtime.
- No public / C-end / B-end route.
- No collector runtime integration.
- No HTTP/API bridge to collector.
- No real API / real LLM.
- No URL fetch / scrape.
- No publish / send / post / execute behavior.

## I. Approval Gates Before Future Implementation

Future gates before any implementation:

1. Auth/local-only contract docs accepted.
2. Safe error contract accepted.
3. Operator role wording accepted.
4. Route remains disabled by default.
5. Separate explicit user approval before any implementation.
6. Targeted tests before any runtime behavior expansion.

If any future implementation proposes UI, storage, evidence row preview, production import, public customer exposure, collector runtime integration, HTTP/API bridge behavior, or real package reads, stop and require a separate explicit user approval.
