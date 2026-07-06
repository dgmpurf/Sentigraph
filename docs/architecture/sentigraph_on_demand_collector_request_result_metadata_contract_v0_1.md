# Sentigraph On-demand Collector Request / Result Metadata Contract v0.1

## A. Contract Purpose

This contract defines the metadata-only request/result handoff between Sentigraph and an external on-demand collector.

It is docs-only. It does not implement backend code, tests, route/API behavior, frontend behavior, runtime persistence, collector execution, provider execution, scheduler behavior, HTTP bridge behavior, webhook behavior, package resolver behavior, staging behavior, row parsing, Evidence Layer write, production EvidenceItem, production case, production analysis_run, actual analysis execution, production Analysis Result authorization, production Analysis Result creation, Source 11 runtime, FinalSummaryReport runtime, B-end report runtime, Sandbox/public event runtime, export/download/public/final-delivery runtime, Project Source files, or GitHub Actions changes.

## B. 8Z-1 Workflow Anchor

8Z-1 defined this conceptual workflow:

```text
Sentigraph controlled request metadata
-> external collector runs explicit on-demand task outside Sentigraph
-> collector exports provider_result / package metadata
-> Sentigraph reads safe metadata first
-> package resolver / review-only staging
-> Route C gated governance chain
```

8Z-2 defines the request/result metadata contract for that workflow. It does not implement the workflow.

The collector remains external, on-demand, and outside Sentigraph runtime. Sentigraph remains a safe metadata consumer and governance runner.

## C. Request Metadata Object

Future docs-only schema name:

`sentigraph_on_demand_collection_request_metadata_v0_1`

Purpose: describe a safe operator-controlled collection request for an external collector. It is not a command for Sentigraph to scrape, fetch, schedule, execute a provider job, or run collector code.

Allowed fields:

| Field | Meaning |
| --- | --- |
| `request_id` | Stable request identifier for correlation. |
| `request_schema` | Expected schema label, such as `sentigraph_on_demand_collection_request_metadata_v0_1`. |
| `request_version` | Contract version label. |
| `case_id_hint` | Optional case hint only; not production case creation. |
| `event_slug` | Safe event label only; not route/public event creation. |
| `event_title` | Safe display title. |
| `event_summary_safe_text` | Safe event summary with no secrets, raw identities, or private content. |
| `topic_query_safe_text` | Safe topic text; not a Sentigraph live search instruction. |
| `requested_platform_labels` | Platform labels only. |
| `collection_goal` | Human-readable goal for external operator review. |
| `collection_scope_note` | Scope/coverage limitation note. |
| `time_window_hint` | Optional time-window hint. |
| `expected_output_contract` | Expected provider result/package metadata contract label. |
| `expected_package_role` | Expected package role, such as selected sample or review input. |
| `operator_label` | Non-secret operator label. |
| `request_created_at` | Request metadata timestamp. |
| `request_created_by_label` | Non-secret creator label. |
| `safety_constraints` | Boundary text and explicit stop conditions. |
| `review_required` | Must be true for handoff governance. |
| `no_cookie_transfer` | Must be true. |
| `no_secret_transfer` | Must be true. |
| `no_browser_profile_transfer` | Must be true. |
| `no_automatic_execution_by_sentigraph` | Must be true. |
| `no_sentigraph_scheduler` | Must be true. |
| `no_sentigraph_live_fetch` | Must be true. |
| `no_automatic_trust_upgrade` | Must be true. |
| `human_review_required` | Must be true. |

Forbidden request fields:

- platform passwords
- cookies
- sessions
- tokens
- browser profile paths
- proxy credentials
- captcha bypass instructions
- anti-bot bypass instructions
- hidden API endpoint instructions
- login instructions
- raw identity lists
- `target_user_list`
- `persuasion_score`
- `psychological_profile`
- `personality_diagnosis`
- private messages
- raw author IDs
- raw author names
- profile URLs as actual values
- secrets
- `.env` values
- instruction for Sentigraph to scrape/fetch
- instruction for Sentigraph to run collector
- `auto_execute`
- `publish_now`
- `send_now`
- `post_now`
- `execute_now`

## D. Request State Labels

Future request labels:

- `draft`
- `pending_operator_review`
- `ready_for_external_collector_task`
- `handed_to_external_collector`
- `external_collection_in_progress_external_only`
- `external_collection_completed`
- `provider_result_metadata_available`
- `package_metadata_available`
- `review_only_staging_candidate_ready`
- `blocked_by_safety_policy`
- `rejected_by_operator`
- `expired`
- `cancelled`

These labels are metadata-only vocabulary. They are not a runtime state machine in 8Z-2.

## E. Provider Result / Result Metadata Object

Future docs-only schema name:

`sentigraph_on_demand_collector_provider_result_metadata_v0_1`

Existing runtime anchor:

`sentigraph_provider_job_result_v0_1`

If implementation is later approved, the existing provider result contract should be reused when it remains sufficient. A new runtime schema should not be created merely because 8Z-2 named a docs-only conceptual shape.

Allowed result metadata fields:

| Field | Meaning |
| --- | --- |
| `provider_result_id` | Unique metadata result identifier. |
| `provider_result_schema` | Schema label or equivalent `schema` field. |
| `request_id` | Correlates to request metadata. |
| `provider_job_id` | External collector/provider job label. |
| `external_collector_label` | Non-secret collector label. |
| `collector_project_label` | Non-secret project label. |
| `package_name` | Opaque safe package identifier. |
| `package_role` | Package role label. |
| `package_schema_version` | Package contract version. |
| `package_reference_kind` | Safe reference kind. |
| `package_reference_safe_id` | Opaque safe package reference. |
| `validation_status` | Metadata/package validation status. |
| `validation_summary` | Safe validation summary only. |
| `evidence_count` | Count metadata only. |
| `source_count` | Count metadata only. |
| `warning_count` | Count metadata only. |
| `error_count` | Count metadata only. |
| `coverage_note_summary` | Coverage limitation summary. |
| `platform_label_summary` | Safe platform-label summary. |
| `source_type_summary` | Safe source-type summary. |
| `package_file_presence_map` | Boolean file presence map only. |
| `manifest_present` | Boolean only. |
| `validation_report_present` | Boolean only. |
| `coverage_note_present` | Boolean only. |
| `evidence_items_jsonl_present` | Boolean only. |
| `evidence_items_csv_present` | Boolean only. |
| `source_manifest_present` | Boolean only. |
| `collection_log_present` | Boolean only. |
| `export_timestamp` | Export metadata timestamp. |
| `provider_attestation_summary` | Safe provider attestation summary. |
| `safety_markers` | Explicit safety booleans and limitations. |
| `metadata_only` | Must be true. |
| `row_content_included` | Must be false. |
| `raw_identity_included` | Must be false. |
| `secrets_included` | Must be false. |
| `human_review_required` | Must be true. |
| `no_automatic_trust_upgrade` | Must be true. |

Forbidden result metadata fields:

- raw evidence row contents
- raw comment dumps
- full `evidence_items` content
- raw author IDs
- raw author names
- profile URLs as actual values
- private messages
- cookies
- sessions
- tokens
- passwords
- API keys
- browser profile paths
- proxy credentials
- absolute private paths exposed to UI/API
- `source_manifest` row contents
- `collection_log` row contents
- `response_text`
- `generated_public_message`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`
- production-ready, customer-ready, public-ready, export-ready, final-ready, or Source-11-runtime-ready claims

## F. Result State Labels

Future result labels:

- `metadata_received`
- `metadata_schema_valid`
- `metadata_schema_invalid`
- `package_reference_valid`
- `package_reference_blocked`
- `package_metadata_ready`
- `validation_pass`
- `validation_warn`
- `validation_error`
- `review_only_ready`
- `blocked_pending_manual_review`
- `blocked_for_forbidden_metadata`
- `blocked_for_path_policy`
- `blocked_for_row_content_presence`
- `blocked_for_secret_or_identity_exposure`

These labels are metadata-only vocabulary. They are not result reader runtime in 8Z-2.

## G. Correlation Rules

Correlation rules:

- `request_id` must match or be linked by explicit correlation metadata.
- missing `request_id` correlation requires manual review.
- mismatched `request_id` blocks automatic handoff.
- `provider_result_id` must be unique within the result metadata scope.
- duplicate `provider_result_id` requires manual review.
- `package_name` is an opaque safe identifier, not an executable path.
- `case_id_hint` is a hint only and cannot create a production case.
- `event_slug` is a label only and cannot create a route or public event.
- result metadata cannot auto-upgrade trust.
- result metadata cannot create Evidence Layer records.
- result metadata cannot create production case, production analysis_run, actual analysis execution, or production Analysis Result.

## H. Package Reference Policy

Package reference rules:

- use `package_name` or a safe package reference only.
- do not treat package names as executable paths.
- forbid path traversal.
- do not expose absolute private paths in UI/API.
- do not read arbitrary package directories in 8Z-2.
- do not read real exchange directories in 8Z-2.
- do not read row files in 8Z-2.
- future path resolution must remain separate and gated by the existing safe resolver or a future explicit smoke.
- `evidence_items.jsonl` / `evidence_items.csv` presence may be recorded only as booleans.
- `source_manifest` / `collection_log` presence may be recorded only as booleans.

## I. Metadata-first Gate Order

The metadata-first order is:

1. request metadata contract.
2. provider_result metadata contract.
3. safe result/package reference validation.
4. package metadata presence check.
5. review-only staging candidate.
6. future controlled row preview only with separate approval.
7. Route C gates for row preview / Evidence / case / analysis boundaries.
8. 8W authorization for any production Analysis Result discussion.

8Z-2 stops at steps 1 and 2 as documentation.

## J. Relationship to Existing Surfaces

Current relevant surfaces include:

- `local_exchange_reader.py`, which reads explicitly configured provider result metadata and blocks forbidden fields.
- `private_collector_provider_result_reader.py`, which validates `sentigraph_provider_job_result_v0_1` and builds a safe handoff summary.
- `private_collector_package_resolver.py`, which resolves safe package metadata with path guards.
- `private_collector_review_only_staging.py`, which can build review-only staging summaries from safe handoff metadata.

8Z-2 does not call, modify, or expand these helpers.

## K. Relationship to Route C

8Z request/result metadata can only feed review-only staging or Route C entry after future gates.

Route C is stage-complete and paused under the 8Y-21 reconciliation. 8Z-2 does not reopen actual analysis execution, does not authorize production Analysis Result, and does not change the Route C pause.

## L. Relationship to 8W

8W-69 pause remains preserved.

8W-70 reactivation remains not selected.

8Z request/result metadata cannot authorize production Analysis Result creation and cannot satisfy 8W-68 or 8W-69 authorization protocol requirements.

## M. Relationship to Source 11

Source 11 update is not required unless existing Analysis Request / Provider / Import Governance runtime behavior changes.

8Z-2 does not change runtime behavior and must not create Project Source files or `docs/project_sources`.

## N. Stop Rules

Stop future work if it asks 8Z request/result metadata to perform or imply:

- backend route/API implementation
- frontend implementation
- request runtime
- result reader runtime
- runtime persistence
- collector job execution
- provider job execution
- scheduler, daemon, or periodic polling
- HTTP bridge or webhook implementation
- live crawl
- private collector source inspection
- MediaCrawler / OpenClaw production integration
- real exchange directory read
- arbitrary real package directory read
- row file read
- `evidence_items.jsonl` parsing
- `evidence_items.csv` parsing
- `source_manifest` row parsing
- `collection_log` row parsing
- original package row reading
- raw comments
- raw identities
- actual author names/profile URLs
- cookies, sessions, tokens, browser profiles, secrets, private paths, or `.env` values
- real APIs
- real LLMs
- URL fetching or scraping
- Evidence Layer write
- production EvidenceItem
- production case
- production analysis_run
- actual analysis execution
- production Analysis Result authorization
- production Analysis Result creation
- 8W-70 reactivation
- Review Queue runtime
- Source 11 runtime
- FinalSummaryReport runtime
- B-end report runtime
- Sandbox/public event runtime
- export/download/public/final-delivery runtime
- customer-ready, public-ready, production-ready, final-ready, export-ready, or Source-11-runtime-ready claim
- official verification
- causal proof
- prediction
- production score

## O. Future Gate Plan

Future gates may be proposed only by separate approval:

- 8Z-3 controlled on-demand collector request metadata fixture smoke.
- 8Z-4 controlled provider_result metadata fixture smoke.
- 8Z-5 controlled request/result correlation smoke.
- 8Z-6 review-only staging handoff gate.

Future 8Z-3 exact approval phrase:

```text
APPROVE_8Z_3_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_METADATA_FIXTURE_SMOKE
```

This phrase is inactive in 8Z-2. It does not authorize implementation, collector execution, provider jobs, HTTP bridge, webhook, scheduler, real exchange directory reads, row parsing, Evidence Layer write, production case, production analysis_run, actual analysis execution, or production Analysis Result.

## P. Contract Decision

8Z-2 selects:

`ready_for_8Z_3_controlled_on_demand_collector_request_metadata_fixture_smoke`

This means the metadata contract is coherent enough for a future controlled request metadata fixture smoke discussion. It does not authorize that smoke, and it does not authorize any runtime, collector, provider, row parsing, production, report, public delivery, or Source 11 action.
