# Sentigraph On-demand Collector Workflow Contract v0.1

## A. Contract Purpose

This contract defines how an external on-demand collector project may cooperate with Sentigraph without becoming part of Sentigraph runtime.

It is docs-only. It does not implement backend code, tests, route/API behavior, frontend behavior, runtime persistence, collector execution, provider jobs, row parsing, Evidence Layer writes, production object creation, actual analysis execution, production Analysis Result authorization, Source 11 runtime, FinalSummaryReport runtime, report runtime, public event runtime, export/download/public delivery, or Project Source files.

## B. Core Boundary

The collector is external to Sentigraph.

The collector may be treated as an on-demand evidence provider and local package producer. It is not a periodic crawler, embedded Sentigraph crawler, Sentigraph scheduler, Sentigraph background daemon, or live crawler runtime.

Sentigraph must not be represented as:

- embedded crawler product
- periodic collector scheduler
- live scraping runtime
- platform automation product
- cookie/session/browser-profile bridge
- proxy or anti-bot bypass system

Sentigraph consumes exported metadata/results after collector-side task completion. Provider output is evidence, not truth.

## C. Sentigraph Responsibilities

Sentigraph may be responsible for:

- controlled request metadata definition
- safe provider_result metadata reading
- package metadata resolution with path guards
- review-only staging
- Route C gated evidence / case / analysis boundary processing
- governance and audit boundary preservation

Sentigraph is not responsible for:

- collector runtime ownership
- browser profile ownership
- cookie/session/token transfer
- platform credential handling
- proxy or anti-bot bypass handling
- live URL fetching or scraping
- periodic crawling
- automatic Evidence Layer writes
- automatic production case, analysis_run, analysis execution, or Analysis Result creation

## D. Workflow Shape

Future on-demand cooperation should follow this shape:

```text
Sentigraph controlled request metadata
-> external collector receives task outside Sentigraph runtime
-> external collector performs explicit on-demand task outside Sentigraph
-> external collector exports provider_result / package metadata / exported package
-> Sentigraph reads safe provider_result metadata first
-> Sentigraph resolves package metadata with path guards
-> Sentigraph enters review-only staging
-> Route C gated row preview / Evidence / case / analysis boundary chain
```

No step is implemented by 8Z-1.

## E. Real-time Connection Definition

Allowed future meaning of real-time connection:

- explicit on-demand request/result handoff
- operator-triggered exchange
- local exchange or governed metadata exchange
- metadata-first handoff
- review-only before row preview
- no automatic trust upgrade

Forbidden meaning:

- periodic crawler
- continuous polling
- background scheduler
- automatic crawl from Sentigraph
- live HTTP collector bridge by default
- webhook bridge by default
- Sentigraph-initiated scrape/fetch
- automatic Evidence Layer write
- automatic production case / analysis_run / Analysis Result

## F. Future Conceptual Objects

8Z-1 records conceptual future-only objects:

### `sentigraph_on_demand_collection_request_metadata_v0_1`

Purpose: record a safe operator-controlled request intent. It does not execute a collector job.

### `sentigraph_external_collector_provider_result_metadata_v0_1`

Purpose: represent a safe provider result metadata handoff. Existing `sentigraph_provider_job_result_v0_1` should be reused if it remains the best fit.

### `exported_package_metadata_reference`

Purpose: reference a package through safe metadata and path-guarded locator fields.

### `safe_metadata_handoff_summary`

Purpose: summarize provider/package metadata without raw evidence rows, raw comments, raw identities, absolute private paths, or secrets.

### `review_only_staging_candidate`

Purpose: preserve metadata for human review without creating production evidence or a production case.

### `route_c_governance_entry_summary`

Purpose: identify whether a future reviewed handoff can enter Route C gates. It does not bypass Route C exact phrases.

No new schema is implemented in 8Z-1.

## G. Request Metadata Contract

Allowed fields:

- `request_id`
- `case_id_hint`
- `event_slug`
- `requested_platforms` as labels only
- `topic_query` or event summary as safe text only
- `collection_goal`
- `time_window_hint`
- `expected_output_contract`
- `operator_label`
- `created_at`
- `safety_constraints`
- `no_cookie_transfer = true`
- `no_secret_transfer = true`
- `no_browser_profile_transfer = true`
- `no_automatic_execution_by_sentigraph = true`

Forbidden fields:

- platform passwords
- cookies
- sessions
- tokens
- browser profile paths
- proxy credentials
- captcha bypass instructions
- hidden API endpoints
- anti-bot bypass instructions
- `target_user_list`
- `persuasion_score`
- `psychological_profile`
- private messages
- raw identity lists
- secrets
- `.env` values
- direct instruction to scrape/fetch from Sentigraph runtime

## H. Provider Result / Package Metadata Contract

Allowed fields:

- `provider_result_id`
- `provider_job_id`
- `package_name`
- `package_role`
- `validation_status`
- `evidence_count`
- `source_count`
- `warning_count`
- `error_count`
- `coverage_note_summary`
- `validation_summary`
- safety markers
- package file presence map
- export timestamp
- provider attestation summary
- path-safe package reference if supported by existing resolver

Forbidden fields:

- raw evidence row contents
- raw comment dumps
- raw author IDs/names
- profile URLs as actual values
- private messages
- cookies, sessions, or tokens
- passwords or API keys
- absolute private paths exposed to UI/API
- full evidence_items content
- `response_text` or `generated_public_message`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

## I. Metadata-first Gate Rules

Sentigraph must process on-demand collector output in this order:

1. Read safe provider_result metadata.
2. Validate metadata contract and safety markers.
3. Resolve package metadata using path guards.
4. Confirm metadata-only status.
5. Enter review-only staging.
6. Require future explicit gates before row preview.
7. Require Route C gates before Evidence / case / analysis boundary movement.
8. Require 8W authorization before any production Analysis Result creation discussion.

Any metadata object containing actual forbidden values must block or require manual review according to the relevant contract.

## J. Future Gate Plan

Future gates:

- 8Z-2 request/result metadata contract docs-only
- 8Z-3 controlled on-demand request metadata fixture smoke, if later approved
- 8Z-4 controlled provider_result metadata handoff smoke, if later approved
- 8Z-5 review-only staging handoff gate, if later approved

Route C gates remain separate for row preview, Evidence, case, and analysis boundaries.

8W authorization remains separate for production Analysis Result.

## K. Future 8Z-2 Approval Phrase

Future phrase:

```text
APPROVE_8Z_2_ON_DEMAND_COLLECTOR_REQUEST_RESULT_METADATA_CONTRACT_DOCS_ONLY
```

This phrase is inactive in 8Z-1. It does not authorize implementation, collector execution, provider jobs, row parsing, Evidence Layer write, production case, production analysis_run, actual analysis execution, production Analysis Result creation, or any route/API/frontend/runtime expansion.

## L. Relationship to 8Y / 8W / Source 11

8Y Route C remains stage-complete and paused at the controlled backend boundary chain.

8Z planning does not reopen 8W-70.

8Z planning does not authorize production Analysis Result creation.

8W-69 remains controlling for production Analysis Result authorization.

Source 11 update is not required because 8Z-1 changes no Analysis Request / Provider / Import Governance runtime behavior.

8Z-1 must not create Project Source files or repo `docs/project_sources`.

## M. Hard Stop Conditions

Stop future work if it requires:

- backend route/API implementation
- frontend integration
- collector execution from Sentigraph
- provider job execution from Sentigraph
- scheduler, daemon, or periodic polling
- live HTTP bridge or webhook by default
- direct private collector runtime import
- private collector source inspection
- real exchange directory reads
- arbitrary real package directory reads
- evidence row parsing
- `evidence_items.jsonl` or `evidence_items.csv` parsing
- raw comments or raw identities
- actual author names/profile URLs
- cookies, sessions, tokens, secrets, browser profiles, or `.env` values
- real APIs or real LLMs
- URL fetching or scraping
- Evidence Layer write
- production EvidenceItem, case, analysis_run, actual analysis execution, or production Analysis Result
- Source 11 / FinalSummaryReport / B-end / Sandbox / export / public delivery runtime
- customer-ready, public-ready, production-ready, final-ready, export-ready, or Source-11-runtime-ready claim

## N. Contract Decision

The selected next boundary option is:

`ready_for_8Z_2_on_demand_collector_request_result_metadata_contract_docs_only`

8Z-1 defines the on-demand collector cooperation boundary and keeps all runtime, collector, provider, row parsing, production, and public delivery actions unapproved.
