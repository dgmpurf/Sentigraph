# Sentigraph On-demand Collector Review-only Staging Handoff Gate Contract v0.1

## A. Contract Purpose

This contract defines the 8Z-6 docs-only gate for considering whether an 8Z-5 request/result correlation summary can become input to a future controlled review-only staging handoff smoke.

It does not implement backend code, tests, routes, frontend, runtime persistence, helper execution, package resolver calls, provider result reader calls, local exchange reader calls, review-only staging candidate creation, Review Queue runtime, collector/provider execution, directory reads, row parsing, Evidence Layer writes, production object creation, analysis execution, report/public output, Project Source files, or GitHub Actions changes.

## B. Current Chain

```text
8Z-1 workflow contract docs-only
-> 8Z-2 request/result metadata contract docs-only
-> 8Z-3 request metadata fixture smoke
-> 8Z-4 provider_result metadata fixture smoke
-> 8Z-5 request/result correlation smoke
-> 8Z-6 review-only staging handoff gate docs-only
```

8Y Route C remains stage-complete and paused. 8W-69 remains the production Analysis Result authorization pause.

## C. 8Z-5 Input Interpretation

The only eligible future source is the 8Z-5 local controlled request/result correlation summary or an equivalent safe fixture.

Required interpretation:

- local controlled backend test path only
- metadata-only
- request ID matched
- provider result ID unique in fixture scope
- package reference opaque and safe
- package resolver not called
- review-only staging not created
- no review-only staging handoff performed
- no real directory reads
- no evidence rows parsed
- no Evidence Layer write
- no production objects
- human review required
- no automatic trust upgrade

## D. Review-only Staging Surface Inventory

| Surface | Surface type | 8Z relation | Side-effect class | 8Z-7 default |
| --- | --- | --- | --- | --- |
| `private_collector_review_only_staging.py` | backend_helper | possible review_only_staging_candidate helper | metadata_only; no_persistence flags | may be considered if safe |
| `test_private_collector_review_only_staging.py` | test_only | helper behavior evidence | test_local_only | reference only |
| `private_collector_provider_result_reader.py` | backend_helper | provider metadata / package handoff reader | may call resolver / package read path | do not call by default |
| `private_collector_package_resolver.py` | backend_helper | package resolution | package_read_possible | do not call by default |
| `local_exchange_reader.py` | runtime_helper | provider result metadata read | metadata read when configured | do not call by default |
| `review_only_staging_import_contract_v0_1.md` | docs_only | staging boundary contract | no runtime | reference only |
| `test_8z_5_controlled_on_demand_collector_request_result_correlation_smoke.py` | test_only | correlated metadata source | test_local_only | allowed source shape |

The existing review-only staging helper has no persistent staging storage flag enabled and records production side effects as false. It still creates a candidate object in memory, so 8Z-6 does not call it. Future 8Z-7 must remain controlled test-path only.

## E. Gate Interpretation

8Z-6 may only select readiness for a future 8Z-7 controlled smoke.

Future 8Z-7 may create a local controlled review-only staging candidate object only inside a backend test path and only if the existing safe helper remains compatible with all constraints.

Future 8Z-7 must not create persistent staging storage, actual Review Queue runtime, production Review Queue item, Evidence Layer write, production EvidenceItem, production case, production analysis_run, actual analysis execution, production Analysis Result, report runtime, public event runtime, delivery runtime, route/API, or frontend.

## F. Future 8Z-7 Input Contract

Allowed future input:

```text
8Z-5 correlation summary
```

Required fields or semantics:

- `request_result_correlation_schema = sentigraph_on_demand_collector_request_result_correlation_v0_1`
- `request_metadata_schema = sentigraph_on_demand_collection_request_metadata_v0_1`
- `provider_result_metadata_schema = sentigraph_on_demand_collector_provider_result_metadata_v0_1`
- `request_id_match = true`
- `provider_result_id_unique_in_fixture_scope = true`
- `package_reference_policy = opaque_safe_identifier_only`
- `metadata_only = true`
- `row_content_included = false`
- `raw_identity_included = false`
- `secrets_included = false`
- `package_resolver_called = false`
- `review_only_staging_created = false`
- `review_only_staging_handoff_performed = false`
- `collector_job_run = false`
- `provider_job_run = false`
- `real_exchange_dir_read = false`
- `real_package_dir_read = false`
- `evidence_rows_parsed = false`
- `evidence_layer_write = false`
- all production object flags false
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

## G. Future 8Z-7 Output Contract

If future 8Z-7 is separately approved, its output constraints are:

- `review_only_staging_candidate_created` may be true only inside controlled backend test path
- candidate schema may use existing safe equivalent or `sentigraph_on_demand_collector_review_only_staging_candidate_v0_1` as local boundary wording only
- `review_only_staging_mode = backend_only_local_review_only_staging_handoff_candidate` or safe equivalent
- `persistent_staging_storage_created = false`
- `actual_review_queue_runtime_used = false`
- `production_review_queue_item_created = false`
- `package_resolver_called = false` by default
- `provider_result_reader_called = false` by default
- `local_exchange_reader_called = false` by default
- `real_exchange_dir_read = false`
- `real_package_dir_read = false`
- `evidence_rows_parsed = false`
- `evidence_layer_write = false`
- production EvidenceItem / case / analysis_run / Analysis Result flags false
- Source 11 / FinalSummaryReport / B-end report / Sandbox/public event / delivery flags false
- route/frontend/customer/public/production-ready flags false
- raw rows/comments/identities/profile URLs/secrets exposed false
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

## H. Hard Stop Rules

Stop future 8Z-7 if it requires:

- no safe review-only staging helper surface found
- package resolver call or real package directory read
- row file parsing
- persistent staging storage
- actual Review Queue runtime
- production Review Queue item
- Evidence Layer write
- production EvidenceItem, case, analysis_run, or Analysis Result
- route/API/frontend
- collector/provider job execution
- scheduler, HTTP bridge, or webhook
- raw rows, comments, identities, or actual profile URLs
- secrets, cookies, sessions, or browser profiles
- real API, LLM, URL fetch, or scraping
- customer/public/production-ready claim

## I. Relationship To Route C

Future 8Z-7 can only produce a local review-only staging candidate.

Route C row preview, Evidence, case, and analysis gates remain separate. 8Z-6 and 8Z-7 do not reopen actual analysis execution and do not authorize production Analysis Result.

## J. Relationship To 8W

8W-69 pause remains preserved.

8W-70 reactivation remains not selected.

Review-only staging handoff cannot satisfy 8W-68 or 8W-69 authorization protocol requirements.

## K. Relationship To Source 11 / Project Source

Source 11 update is not required unless runtime behavior changes.

8Z-6 changes no runtime behavior and must not create Project Source files or `docs/project_sources`.

Future Source update may be considered after a larger 8Z checkpoint, not after this single docs-only gate.

## L. Future Approval Phrase

Future 8Z-7 exact approval phrase:

```text
APPROVE_8Z_7_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_RESULT_CORRELATION_TO_REVIEW_ONLY_STAGING_HANDOFF_SMOKE
```

This phrase is inactive in 8Z-6. It does not authorize implementation, collector execution, provider jobs, request runtime, result reader runtime, package resolver behavior, real exchange/package directory reads, row parsing, persistent staging storage, actual Review Queue runtime, Evidence Layer write, production case, production analysis_run, actual analysis execution, or production Analysis Result.

## M. Contract Decision

The selected next boundary option is:

`ready_for_8Z_7_controlled_on_demand_collector_request_result_correlation_to_review_only_staging_handoff_smoke`

This is only readiness for a future separately approved controlled smoke.
