# Internal Operator Read-only Staging Route Test Plan v0.1

## A. Test Plan Purpose

This document defines future route tests before implementation.

It is docs-only. It does not create tests, routes, frontend UI, persistent storage, Evidence Layer writes, production cases, `analysis_run`, report runtime, Sandbox/public event runtime, collector integration, or public delivery.

## B. Disabled-by-default Tests

Future route implementation must include tests proving:

- route returns `route_disabled` by default.
- `route_disabled` response follows `internal_operator_review_only_staging_error_v0_1`.
- `route_disabled` response exposes no absolute path.
- `route_disabled` response exposes no raw metadata.
- disabled route does not read package directories.
- disabled route does not parse evidence row files.
- disabled route does not mutate state.

## C. Safe Ready Fixture Tests

Future route implementation must include tests proving:

- synthetic fixture returns `internal_operator_review_only_staging_response_v0_1`.
- `metadata_only = true`.
- `review_only = true`.
- `production_import_allowed = false`.
- `evidence_layer_write_allowed = false`.
- `production_case_creation_allowed = false`.
- `analysis_run_allowed = false`.
- `public_output_allowed = false`.
- allowed actions are labels only.
- blocked actions include production/public/action/targeting behaviors.
- response includes safe `staging_candidate`.
- response includes safe `gate_summary`.
- response includes safe `safety_flags`.

## D. Forbidden Field Tests

Future route implementation must block or exclude:

- raw evidence rows
- raw comments
- raw author ids
- raw author names
- profile URLs as actual values
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

Forbidden-field tests must verify values are not leaked in response bodies.

## E. Evidence Row Boundary Tests

Future route implementation must include tests proving:

- `evidence_items.jsonl` is not opened.
- `evidence_items.csv` is not opened.
- no full evidence rows are parsed.
- no raw comments are printed.
- no raw identifiers are printed.
- no evidence row preview is returned.

Recommended approach: monkeypatch file read helpers so attempts to open `evidence_items.jsonl` or `evidence_items.csv` fail the test.

## F. Production Boundary Tests

Future route implementation must include tests proving:

- no Evidence Layer write.
- no production case.
- no `analysis_run`.
- no report runtime.
- no Sandbox/public event runtime.
- no publish/send/post/execute behavior.
- no persistent staging storage.
- no collector execution.
- no real API calls.
- no real LLM calls.
- no URL fetching.
- no scraping.

## G. Route Surface Tests

Future route implementation must include tests proving:

- only `GET` endpoints exist for this route family.
- no `POST`, `PUT`, `PATCH`, or `DELETE`.
- no `FileResponse`.
- no `StreamingResponse`.
- no ZIP generation.
- no public URL.
- no signed URL.
- no file-byte route.
- no external delivery.
- no frontend route.
- no C-end route.
- no B-end customer route.

## H. Recommended Validation Commands for Future Implementation

Future implementation validation commands:

```text
python -m pytest backend/app/tests/test_internal_operator_review_only_staging_routes.py
python -m pytest backend/app/tests/test_private_collector_review_only_staging.py
python -m pytest backend/app/tests/test_private_collector_review_only_staging_integration_smoke.py
python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
git diff --check
git status --short
```

If future implementation touches route registration or app startup, also run targeted route/app import validation before claiming readiness.

Do not require frontend build unless frontend changes are explicitly approved.
