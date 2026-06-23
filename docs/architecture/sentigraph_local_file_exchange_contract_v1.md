# Sentigraph Local File Exchange Contract v1

Status: architecture design only. No runtime is implemented by this document.

## 1. Purpose

This contract defines a future local-file bridge between Sentigraph and an independent private collector project. The projects remain independent:

- Sentigraph does not import collector code.
- The collector does not import Sentigraph code.
- They do not share runtime.
- They do not communicate through HTTP/HTTPS for the MVP.
- They exchange explicitly versioned local files through configured directories.

Provider output is evidence, not truth. Package metadata can become review-ready input later, but it is not production evidence, not official verification, and not a report.

## 2. No HTTP / No HTTPS

The MVP exchange model is local files only.

Forbidden in this contract:

- HTTP provider API.
- HTTPS provider API.
- Webhook.
- Local server callback.
- Direct process invocation.
- Browser profile bridge.
- Cookies, tokens, sessions, browser state, proxy details, anti-bot details, or hidden platform APIs.

## 3. Config Fields

Future Sentigraph configuration should be explicit and disabled by default:

```json
{
  "exchange_enabled": false,
  "requestsDir": "runtime/analysis_requests/local_exchange/requests",
  "resultsDir": "runtime/analysis_requests/local_exchange/results",
  "packageIndexPath": "",
  "packageRoot": "",
  "exchangeLogPath": "runtime/analysis_requests/local_exchange/logs",
  "request_schema": "sentigraph_analysis_request_v1",
  "result_schema": "sentigraph_provider_job_result_v1",
  "contract_version": "1.0",
  "adapter_id": "configured_external_provider"
}
```

The example paths are future-gated local runtime paths. They must remain ignored runtime paths and must not be treated as mandatory private collector locations.

## 4. Request File Contract

Sentigraph may later write a `sentigraph_analysis_request_v1` JSON file to `requestsDir`.

Example safe fields:

```json
{
  "request_id": "req_...",
  "request_schema": "sentigraph_analysis_request_v1",
  "contract_version": "1.0",
  "created_at": "2026-06-23T00:00:00Z",
  "query": "event keyword",
  "event_hint": {
    "title": "optional event title",
    "language": "zh-CN"
  },
  "platforms": ["public_web"],
  "time_window": {
    "start": "2026-06-01T00:00:00Z",
    "end": "2026-06-23T00:00:00Z"
  },
  "max_items": 500,
  "safety_mode": "metadata_and_public_sample_only",
  "output_contract": "sentigraph_evidence_export_v1",
  "allow_live_collection": false,
  "privacy": {
    "redact_author_identifiers": true,
    "no_cookies": true,
    "no_tokens": true,
    "no_sessions": true
  },
  "requested_package_role": "review_ready_candidate",
  "callback_mode": "local_file_exchange"
}
```

Default `allow_live_collection` is false. If a future request tries to require cookies, tokens, sessions, browser profiles, crawler internals, or anti-bot bypass, the collector should block it or require manual review.

## 5. Result File Contract

The private collector may later write a `sentigraph_provider_job_result_v1` JSON file to `resultsDir`.

Example safe fields:

```json
{
  "provider_result_id": "result_...",
  "provider_job_id": "job_...",
  "sentigraph_request_id": "req_...",
  "result_schema": "sentigraph_provider_job_result_v1",
  "contract_version": "1.0",
  "adapter_id": "external_collector_local_file_adapter",
  "compatibility_status": "compatible",
  "status": "package_ready",
  "package_contract": "sentigraph_evidence_export_v1",
  "package_id": "package_...",
  "package_role": "review_ready_candidate",
  "package_index_ref": "package_index.json",
  "package_root_ref": "configured_package_root",
  "package_relative_path": "packages/package_...",
  "summary": {
    "evidence_items": 0,
    "sources": 0,
    "comment_samples": 0,
    "root_candidates": 0
  },
  "validation_summary": {
    "status": "pass|warn|fail",
    "errors": 0,
    "warnings": 0
  },
  "coverage_note": "Selected package coverage only; not full-web or full-platform coverage.",
  "warnings": [],
  "errors": [],
  "nextAction": "review_package_metadata"
}
```

Allowed result statuses:

- `package_ready`
- `needs_manual_snapshot`
- `blocked`
- `invalid_schema`
- `unsupported_contract`
- `failed`

The result file must not include full evidence content. It should reference package metadata and safe counts only.

## 6. Package Index

Use the existing Sentigraph Evidence Export v1 `package_index.json` and package folders as metadata sources.

Rules:

- Do not copy full `evidence_items.jsonl` content into the provider result.
- Do not copy raw rows into Sentigraph.
- Do not include raw author IDs, raw author names, profile URLs, private messages, cookies, tokens, sessions, secrets, browser state, proxy details, anti-bot details, or collector internals.
- Sentigraph may later read safe package metadata before any review-only import.

## 7. Atomic File Behavior

Future writers should:

- Write a temporary file first.
- Flush/fsync if available and safe.
- Rename to final `.json`.
- Never read partial files.
- Include `processed_at` and `result_written_at`.
- Use idempotency by `request_id` and `provider_job_id`.
- Keep append-only exchange logs where practical.

## 8. Compatibility Handling

Every file should include:

- `request_schema`
- `result_schema`
- `contract_version`
- `adapter_id`
- `compatibility_status`

If the contract is unsupported, return `unsupported_contract`.
If required fields are missing or invalid, return `invalid_schema`.
If safety boundaries are violated, return `blocked` with safe warning codes.

## 9. Safety Rules

Sentigraph must not ask for:

- Cookies, tokens, sessions, salts, or API keys.
- Browser profiles or login state.
- Captcha bypass or anti-bot bypass.
- Proxy evasion details.
- Raw author identifiers.
- Private messages.
- Crawler internals.

Provider result must not expose:

- raw author IDs
- raw author names
- profile URLs
- email / phone / password-like values
- cookies / tokens / sessions
- secrets
- private messages
- browser profile paths
- collector internals

## 10. Relationship To Sentigraph State

This is a future contract design. It does not:

- Write the production Evidence Layer.
- Create a production case.
- Create a production review queue.
- Run production dedup.
- Run analysis.
- Generate a B-end report runtime.
- Generate a Sandbox fixture.
- Generate a public event page.
- Execute provider or collector jobs.
- Call real APIs.
- Fetch URLs or scrape websites.
