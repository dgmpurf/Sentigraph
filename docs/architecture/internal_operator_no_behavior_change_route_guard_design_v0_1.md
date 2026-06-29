# Internal Operator No-behavior-change Route Guard Design v0.1

## A. Purpose

This is a docs-only design for future no-behavior-change guard hardening around the internal operator review-only staging route.

This document does not implement code. It does not modify route behavior. It does not approve runtime expansion. It does not approve auth, UI, storage, evidence preview, production import, collector bridge, or public exposure.

The design exists only to define what a future guard/helper extraction would need to preserve if the user explicitly approves implementation later.

## B. Current Accepted Foundation

- 8T-17 route skeleton accepted after disabled and enabled synthetic fixture smoke.
- 8T-18 auth/local-only contract accepted docs-only.
- 8T-19 UI contract accepted docs-only.
- 8T-20 readiness decision rejected direct implementation.
- 8T-21 safety test plan created.
- 8T-22 selected tests-only as first implementation slice.
- 8T-23 tests-only safety contract implemented and passed.
- 8T-24 selected no-behavior-change route guard design as the only recommended continuation.

## C. Design Principle

The future guard design must preserve exact current behavior.

It may only centralize or make explicit existing safety checks. It must not broaden access. It must not enable production mode. It must not add data reads. It must not add UI. It must not change response schema unless separately approved.

No future helper is allowed to convert the current synthetic/test-only route into runtime import, evidence preview, production staging, public output, or collector bridge behavior.

## D. Future Guard / Helper Candidates

### 1. `route_enabled_env_gate` Helper

Purpose:

- Centralize disabled-by-default route gating.

What it would centralize:

- Accepted true values: `1`, `true`, `yes`.
- Disabled behavior for unset, empty, falsey, and unknown env values.

Current behavior it must preserve:

- Unset env disables the route.
- Empty string, `false`, `0`, and unknown values disable the route.
- No query parameter, token, cookie, session, header, or account state enables the route.

Forbidden changes:

- No default-enabled mode.
- No production mode.
- No session/token/cookie-based enablement.
- No query-param enablement.

Future test requirement:

- Disabled/default env tests.
- Falsey env tests.
- Explicit true-value tests.

Implementation approval status:

- not approved now

### 2. `synthetic_mode_guard` Helper

Purpose:

- Make synthetic/test-only mode explicit.

What it would centralize:

- Synthetic candidate id checks.
- Synthetic fixture-only response rule.
- Unknown candidate safe `not_found`.

Current behavior it must preserve:

- Enabled mode returns only synthetic metadata.
- Unknown candidate returns safe `not_found`.
- No real package path, private collector root, or evidence row file is read.

Forbidden changes:

- No real package resolution.
- No private collector root probing.
- No evidence row preview.
- No production staging.

Future test requirement:

- Candidate list response snapshot.
- Candidate detail response snapshot.
- Unknown candidate safe error snapshot.
- File-open guard for `evidence_items.jsonl` and `evidence_items.csv`.

Implementation approval status:

- not approved now

### 3. `safe_error_response` Helper

Purpose:

- Centralize safe denial/error response shape.

What it would centralize:

- Error schema.
- `metadata_only = true`.
- `review_only = true`.
- `path_exposed = false`.
- `raw_metadata_exposed = false`.

Current behavior it must preserve:

- Safe `route_disabled` response.
- Safe `not_found` response.
- No raw metadata, paths, secrets, raw rows, author identifiers, or generated messages.

Forbidden changes:

- No absolute path exposure.
- No raw row exposure.
- No secret-like field exposure.
- No public/generated response text.

Future test requirement:

- Recursive key/value forbidden-field scan.
- Snapshot comparison against current disabled and not_found responses.

Implementation approval status:

- not approved now

### 4. `safe_metadata_projection` Helper

Purpose:

- Centralize the safe metadata-only projection for synthetic staging candidates.

What it would centralize:

- Allowed metadata fields.
- Coverage summary fields.
- Validation summary fields.
- Allowed and blocked action labels.
- Required safety flags.

Current behavior it must preserve:

- No raw rows.
- No raw comments.
- No actual author identifiers.
- No profile URLs.
- No absolute private paths.
- No evidence file contents.

Forbidden changes:

- No row preview.
- No raw package content.
- No production Evidence write.
- No production case creation.
- No analysis run creation.

Future test requirement:

- Allowed-key assertion.
- Forbidden-key assertion.
- Required false safety flags assertion.

Implementation approval status:

- not approved now

### 5. `forbidden_field_scan` Helper

Purpose:

- Centralize response scan logic for unsafe active output fields.

What it would centralize:

- Response JSON key scan.
- Serialized text marker scan.
- Boundary-label false-positive handling.

Current behavior it must preserve:

- Safety flag names and blocked-action labels may appear only as boundary metadata.
- Active forbidden payload fields must not appear.

Forbidden changes:

- No active `response_text`.
- No `generated_public_message`.
- No targeting, persuasion, truth, prediction, personality, or official verification outputs.

Future test requirement:

- Explicit false-positive tests for safety flag names.
- Explicit failure fixtures for active forbidden fields.

Implementation approval status:

- not approved now

### 6. `route_surface_assertion` Helper

Purpose:

- Centralize route-surface checks.

What it would centralize:

- GET-only assertion.
- Internal path prefix assertion.
- No public/C-end/B-end/customer/provider/collector aliases.

Current behavior it must preserve:

- Route family remains internal-only and GET-only.

Forbidden changes:

- No POST/PUT/PATCH/DELETE.
- No callback route.
- No public route.
- No customer/B-end/C-end alias.

Future test requirement:

- Route registry scan.
- Exact route-family path assertion.

Implementation approval status:

- not approved now

### 7. `no_file_delivery_static_scan` Helper

Purpose:

- Centralize static checks against file delivery implementation.

What it would centralize:

- `FileResponse` scan.
- `StreamingResponse` scan.
- ZIP/archive scan.
- Public/signed URL scan.
- Object storage, portal publication, and email delivery scan.

Current behavior it must preserve:

- No file-byte route.
- No ZIP/archive.
- No public URL.
- No signed URL.
- No external delivery.

Forbidden changes:

- No download endpoint.
- No file-byte response.
- No object storage upload.
- No portal publication.
- No email/send/publish behavior.

Future test requirement:

- Static source scan for route module and future helper modules.

Implementation approval status:

- not approved now

### 8. `no_evidence_row_open_guard` Helper

Purpose:

- Centralize monkeypatch/file-open guard patterns for tests.

What it would centralize:

- Guard against opening `evidence_items.jsonl`.
- Guard against opening `evidence_items.csv`.
- Guard against reading private collector roots or real package export paths.

Current behavior it must preserve:

- Synthetic route calls do not open evidence row files.
- Synthetic route calls do not probe private collector paths.

Forbidden changes:

- No evidence row parsing.
- No real package row reading.
- No private collector root reading.

Future test requirement:

- Scoped `Path.open` / `builtins.open` guard.
- Optional path-probe guard.

Implementation approval status:

- not approved now

### 9. `no_public_alias_guard` Helper

Purpose:

- Centralize no-public-alias regression checks.

What it would centralize:

- Public route exclusion.
- C-end/B-end/customer alias exclusion.
- Provider/collector callback exclusion.

Current behavior it must preserve:

- Internal operator route remains internal-only.

Forbidden changes:

- No public exposure.
- No customer-facing route.
- No platform/provider callback.
- No collector runtime/API bridge.

Future test requirement:

- Route registry scan.
- Frontend route/API string scan only if UI files are touched in a separately approved phase.

Implementation approval status:

- not approved now

## E. Non-behavior-change Proof Requirements

Future implementation, if ever approved, must prove:

- same disabled default behavior.
- same falsey env behavior.
- same explicit synthetic fixture enabled behavior.
- same GET-only route surface.
- same safe list/detail/not_found response shape.
- same no-public-alias behavior.
- same no `evidence_items` opening behavior.
- same no storage / no Evidence Layer / no production case / no analysis_run behavior.
- no new frontend/UI route.
- no new auth/session/token/cookie behavior.

## F. Future Red/Green TDD Approach

Design only:

- First add failing tests only if the helper does not exist.
- Implement the smallest helper extraction later only after explicit approval.
- Compare pre/post response snapshots.
- Run existing 8T-23 safety contract tests.
- Run enabled fixture smoke.
- Run disabled smoke.
- Run golden contracts.
- Run `py_compile`.
- Run `git diff --check`.

Do not implement these tests now.

## G. Rollback and Stop Rules

Future implementation must stop if:

- route behavior changes.
- route becomes enabled by default.
- any POST/PUT/PATCH/DELETE appears.
- any UI appears.
- any `evidence_items` file opens.
- any private collector root is read.
- any `FileResponse` / `StreamingResponse` / ZIP / public URL / signed URL / external delivery appears.
- any Evidence Layer write / production case / analysis_run appears.
- any `response_text` / `generated_public_message` / targeting / persuasion / truth / prediction / personality output appears.

## H. Explicit Non-goals

- no backend implementation now
- no frontend implementation now
- no test implementation now
- no helper implementation now
- no route behavior change
- no auth implementation
- no local-only runtime
- no UI
- no storage
- no evidence row preview
- no production import
- no Evidence Layer write
- no production case / analysis_run
- no report runtime
- no Sandbox/public event runtime
- no collector runtime/API bridge
