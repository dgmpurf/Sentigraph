# Internal Operator Read-only Staging Route Implementation Guardrails v0.1

## A. Guardrail Purpose

This document defines implementation guardrails for a possible future backend route skeleton.

It does not approve route implementation by itself.

It does not implement code, tests, backend routes, frontend UI, persistent storage, Evidence Layer write, production case creation, `analysis_run`, report runtime, Sandbox/public event runtime, collector integration, or public delivery.

## B. Required Disabled-by-default Behavior

Future route must be disabled by default.

When disabled, the route must return a safe error:

```json
{
  "schema": "internal_operator_review_only_staging_error_v0_1",
  "error_code": "route_disabled",
  "path_exposed": false,
  "raw_metadata_exposed": false
}
```

Disabled behavior must not:

- read package directories
- parse evidence row files
- write persistent storage
- write Evidence Layer
- create cases
- create `analysis_run`
- call collector
- call real APIs
- call real LLMs
- fetch URLs
- scrape pages

## C. Allowed Implementation Mode

Allowed only if the user explicitly approves a future implementation phase:

- backend-only route skeleton.
- GET-only endpoints from 8T-11.
- safe response schema.
- synthetic fixture-only tests.
- no persistent storage.
- no frontend.
- no production import.
- no public route.
- no B-end/C-end customer route.

## D. Safe Fixture Mode, Test-only

If needed for tests, a synthetic in-memory fixture may be used.

The fixture must not:

- read real collector export root.
- read real package directories.
- parse evidence rows.
- include raw identifiers.
- include raw comments.
- include profile URLs as actual values.
- include secrets.
- include absolute private paths.
- include generated public response text.
- include targeting fields.
- include production action payloads.

## E. Forbidden Implementation Behavior

Forbidden:

- `POST`, `PUT`, `PATCH`, or `DELETE`.
- state mutation.
- audit append.
- persistent staging storage.
- production import.
- Evidence Layer write.
- production case creation.
- `analysis_run` creation.
- report generation.
- Sandbox/public event generation.
- public response generation.
- publish/send/post/execute.
- target individuals.
- real collector access.
- private collector project modification.
- real package directory reads.
- real API calls.
- real LLM calls.
- URL fetching.
- scraping.
- live crawl.
- evidence row parsing.
- `evidence_items.jsonl` parsing.
- `evidence_items.csv` parsing.
- raw comment exposure.
- raw author identifier exposure.
- secret exposure.
- absolute path exposure.
- file-byte response.
- download route.
- public URL generation.
- signed URL generation.
- external delivery.

## F. Required Runtime Safety Flags

Future response `safety_flags` must include:

```json
{
  "collector_run": false,
  "live_crawl": false,
  "real_api_called": false,
  "real_llm_called": false,
  "url_fetching": false,
  "scraping": false,
  "full_evidence_rows_parsed": false,
  "evidence_items_jsonl_parsed": false,
  "evidence_items_csv_parsed": false,
  "raw_comments_printed": false,
  "raw_author_identifiers_printed": false,
  "secrets_read": false,
  "evidence_layer_written": false,
  "production_case_created": false,
  "analysis_run_created": false,
  "b_end_report_runtime_generated": false,
  "sandbox_public_event_runtime_generated": false,
  "persistent_staging_storage_created": false
}
```

## G. Required Blocked Actions

Future responses must include these blocked actions:

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

These are blocked behavior labels, not hidden action endpoints.

## H. Failure Behavior

If unsafe input or forbidden fields are detected, the future route must return a safe blocked error without leaking values.

Required behavior:

- return safe error schema.
- include blocker code.
- exclude raw values.
- exclude absolute paths.
- exclude raw metadata dumps.
- exclude raw evidence rows.
- exclude raw identifiers.
- exclude secrets.
- keep production action flags false.
- keep public action flags false.

Unsafe input must never be auto-repaired into a production-ready candidate.
