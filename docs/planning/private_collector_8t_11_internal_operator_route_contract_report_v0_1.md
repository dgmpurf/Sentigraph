# Private Collector 8T-11 Internal Operator Route Contract Report v0.1

## A. Decision / Status

```text
phase = 8T-11
task = internal_operator_read_only_staging_route_contract_docs_only
privacy_issue_stop = no
code_changed = no
docs_only = yes
collector_run = no
live_crawl = no
real_api_called = no
real_llm_called = no
full_evidence_rows_read = no
evidence_layer_write = no
production_case_created = no
analysis_run_created = no
project_source_changed = no
project_source_files_created_in_repo = no
api_route_added = no
frontend_changed = no
persistent_staging_storage_created = no
```

Decision: ready.

Implementation slice: 8T-11 internal operator read-only staging route contract docs-only.

## B. What 8T-10 Decided

8T-10 decided:

- route implementation is not ready.
- route contract docs are ready to create.
- UI implementation is not ready.
- production import is blocked.
- Evidence Layer write is blocked.
- production case creation is blocked.
- `analysis_run` creation is blocked.
- report/Sandbox/public event generation is blocked.

8T-10 also recommended a future ChatGPT-side Project Source batch update after the user approves. No Source files should be created in the repo.

## C. Route Contract Summary

The future route contract is internal operator, read-only, metadata-only, and disabled-by-default or local-only until later explicit approval.

Design-only route candidates:

```text
GET /api/v1/internal/staging/review-only/candidates/{staging_candidate_id}
GET /api/v1/internal/staging/review-only/candidates
```

Only `GET` is included.

No `POST`, `PUT`, `PATCH`, or `DELETE` is included.

The contract allows safe metadata fields such as candidate IDs, package name, case hints, validation status, counts, safe summaries, review status, promotion status, blockers, warnings, allowed action labels, blocked action labels, safety flags, audit refs, and created time.

The contract forbids raw evidence rows, raw comments, raw author ids/names, profile URLs as actual values, secrets, absolute private paths, generated response text, targeting fields, persuasion/truth scores, official verification claims, prediction probabilities, psychological profiles, and personality diagnosis.

## D. Safe Response Schema Summary

The safe response schema is:

```text
internal_operator_review_only_staging_response_v0_1
```

Required boundary fields include:

- `metadata_only = true`
- `review_only = true`
- `production_import_allowed = false`
- `evidence_layer_write_allowed = false`
- `production_case_creation_allowed = false`
- `analysis_run_allowed = false`
- `public_output_allowed = false`

The schema includes:

- safe `staging_candidate`
- safe `gate_summary`
- allowed action labels
- blocked action labels
- safety flags
- warnings
- blockers
- audit refs

The schema also defines safe error responses for:

- `not_found`
- `manual_review_required`
- `blocked_privacy_issue`
- `blocked_metadata_contract`
- `blocked_path_escape`
- `route_disabled`
- `operator_auth_required`

Error responses must not leak absolute paths, raw metadata, raw evidence rows, raw identifiers, secrets, profile URLs, generated response text, or production action payloads.

## E. Operator Boundary

The future route is:

- internal-only
- read-only
- metadata-only
- disabled-by-default or local-only until implementation gate approval
- not public
- not C-end
- not B-end customer-facing
- not external delivery
- not a download route
- not a file-byte route
- not a public URL or signed URL generator
- not an object storage uploader
- not an email sender
- not a portal publisher

Allowed actions are labels only. They are not executable actions.

Blocked actions must always include production import, production case creation, analysis run, report generation, public event generation, generated public response, publish, send, post, execute, and target-individual behavior.

## F. Implementation Readiness Decision

```text
ready_for_route_implementation = no
ready_for_route_contract_review = yes
ready_for_ui_implementation = no
ready_for_production_import = no
```

Route implementation still requires:

- explicit user approval
- route tests
- safe response schema enforcement
- operator auth or local-only boundary
- disabled-by-default setting
- no evidence row parsing tests
- no forbidden field exposure tests
- no production action tests
- no persistent staging storage tests
- audit strategy review

## G. Recommended Next Step

Recommended:

```text
Phase 8T-12 internal operator read-only staging route implementation decision checkpoint
```

Do not recommend implementation unless explicitly approved by the user.

Do not recommend UI implementation.

Do not recommend production import.

Do not recommend Evidence Layer write, production case creation, `analysis_run`, report runtime, Sandbox/public event runtime, generated public response, publish/send/post/execute behavior, collector integration, real API calls, or real LLM calls.

## H. Source Update Policy

No immediate Project Source update.

Batch later after route contract review or route implementation decision milestone.

Do not create `docs/project_sources`.

Do not create Source update files in the repo.

Do not modify Project Source files from this repo task.

## I. Safety Confirmations

- docs-only
- no code changed
- no tests changed
- no collector run
- no live crawl
- no browser automation
- no real API
- no real LLM
- no URL fetch/scrape
- no full evidence rows parsed
- no `evidence_items.jsonl` parsed
- no `evidence_items.csv` parsed
- no raw comments printed
- no raw author ids/names printed
- no cookies/tokens/sessions/profile paths read
- no Evidence Layer write
- no production case / analysis_run
- no B-end report runtime
- no Sandbox/public event runtime
- no frontend/API route added
- no persistent staging storage
- no Project Source files created in repo
- no GitHub Actions workflow recreated

## J. Issues Found

P0 privacy/safety:

- none.

P1 implementation blocker:

- route implementation is still not approved.
- UI implementation is still not approved.
- production import remains blocked.

P2 non-blocking limitation:

- this phase is route contract and safe response schema only.
- implementation tests are intentionally deferred until a route implementation decision checkpoint approves implementation.

P3 nice-to-have:

- a future UI contract can build from this safe response schema after route implementation is approved and verified.
