# Internal Operator Route Guard Helper Contract v0.1

## A. Purpose

This document defines a future helper contract only.

It does not implement helper code. It does not approve runtime expansion, route behavior changes, UI, auth runtime, storage, evidence row preview, production import, collector bridge, or public exposure.

## B. Future Helper Family Overview

| Helper family | Future purpose | Input allowed | Output allowed | Forbidden behavior | Implementation approved now? |
| --- | --- | --- | --- | --- | --- |
| env gate helper | Centralize disabled-by-default env gate | Env flag string only | Boolean enabled/disabled decision | Query-param enablement, token/cookie/session enablement, default enabled, production mode | no |
| synthetic fixture mode helper | Keep enabled mode synthetic/test-only | Candidate id and static synthetic fixture metadata | Safe fixture metadata or safe not_found | Real package reads, private collector reads, evidence row preview, production staging | no |
| safe error response helper | Centralize safe denial response | Error code and safe message | Safe error envelope | Paths, raw metadata, raw rows, secrets, identifiers, generated messages | no |
| safe metadata projection helper | Project safe staging metadata only | Already-safe synthetic metadata | Safe metadata envelope | Raw comments, author identifiers, profile URLs, absolute paths, evidence file contents | no |
| forbidden field scan helper | Centralize active forbidden-field checks | Response JSON / serialized response text | Pass/fail test signal | Treating forbidden active fields as allowed output | no |
| no public alias guard | Prevent public/customer/provider aliases | FastAPI route registry | Pass/fail test signal | Public, C-end, B-end, customer, provider callback, collector callback route | no |
| no file-byte delivery guard | Prevent file delivery implementation | Route/helper source text | Pass/fail static scan signal | FileResponse, StreamingResponse, zip/archive, public URL, signed URL, external delivery | no |
| no evidence row open guard | Prevent evidence row file opening | Scoped test monkeypatch | Assertion failure on forbidden open | Opening evidence_items files, private collector roots, real export paths | no |
| no production side-effect guard | Prevent persistence and production state changes | Response/static/tmp-path observations | Pass/fail test signal | Evidence Layer writes, production case, analysis_run, review queue, report/Sandbox/public event runtime | no |

## C. Env Gate Helper Contract

Future accepted true values:

- `1`
- `true`
- `yes`

All other values must be disabled, including:

- unset
- empty string
- `false`
- `0`
- unknown strings

Requirements:

- no default enabled
- no secrets
- no query-param enablement
- no token/cookie/session enablement
- no production mode enablement
- no account/login/profile-state enablement

## D. Safe Error Response Helper Contract

Allowed future denial codes:

- `route_disabled`
- `operator_auth_required`
- `operator_role_required`
- `local_only_required`
- `synthetic_mode_only`
- `not_found`
- `privacy_hold`

Required safe fields:

- `metadata_only = true`
- `review_only = true`
- `path_exposed = false`
- `raw_metadata_exposed = false`

Forbidden:

- absolute paths
- raw comments
- raw author identifiers
- evidence rows
- secrets
- `response_text`
- `generated_public_message`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

## E. Safe Metadata Projection Contract

Allowed:

- `staging_candidate_id`
- `provider_result_id`
- `package_name`
- `package_role`
- `case_id_hint`
- `validation_status`
- `evidence_count`
- `source_count`
- `warning_count`
- `error_count`
- coverage summary
- blockers/warnings
- allowed_actions labels
- blocked_actions labels
- safety_flags

Forbidden:

- raw row content
- raw comments
- actual author identifiers
- actual profile URLs
- absolute paths
- private messages
- cookies/sessions/tokens/API keys
- evidence_items file contents

## F. Static Guard Contract

Future static checks must continue to guard against:

- `FileResponse`
- `StreamingResponse`
- zip/archive
- `public_url`
- `signed_url`
- `external_delivery`
- email delivery
- object storage upload
- portal publication
- public/C-end/B-end/customer alias routes
- collector callback/API bridge

Boundary wording and blocked-action labels may appear in docs or safe metadata, but active implementation must not appear without a separately approved runtime phase.

## G. Future Implementation Prerequisites

Before implementing any helper:

1. This contract accepted.
2. Explicit user approval.
3. Red/green targeted tests.
4. No-behavior-change snapshot comparison.
5. Existing safety contract tests remain passing.
6. Rollback plan.
7. No Source files in repo.

Implementation remains not approved now.
