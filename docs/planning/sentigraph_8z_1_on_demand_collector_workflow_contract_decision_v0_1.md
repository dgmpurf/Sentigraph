# Sentigraph 8Z-1 On-demand Collector Workflow Contract Decision v0.1

## A. Decision / Status

phase = 8Z-1
decision = ready
privacy_issue_stop = no
docs_only = yes
workflow_contract_only = yes
backend_code_changed = no
tests_changed = no
route_changed = no
frontend_changed = no
runtime_changed = no
collector_job_run = no
provider_job_run = no
private_collector_source_inspected = no
real_exchange_dir_read = no
real_package_dir_read = no
evidence_rows_parsed = no
evidence_layer_write = no
production_evidence_item_created = no
production_case_created = no
production_analysis_run_created = no
actual_analysis_execution_started = no
production_analysis_result_creation_authorized = no
production_analysis_result_created = no
8w69_pause_preserved = yes
8w70_reactivation_selected = no
source11_runtime_called = no
actual_final_summary_report_created = no
b_end_report_runtime_generated = no
sandbox_public_event_runtime_generated = no
export_download_public_delivery_created = no
source_files_created = no
docs_project_sources_created = no
selected_next_boundary_option = ready_for_8Z_2_on_demand_collector_request_result_metadata_contract_docs_only
future_8z2_exact_approval_phrase_required = yes
future_8z2_exact_approval_phrase_active = no
source_update_recommended_after_commit = no
source11_update_recommended = no
recommended_tag = no

## B. Purpose

8Z-1 defines the workflow contract for on-demand collector cooperation with Sentigraph.

It is planning-only. It does not implement a request object, provider result reader change, package resolver change, route/API, frontend, runtime, collector execution, provider job execution, row parsing, Evidence Layer write, production case, production analysis_run, actual analysis execution, production Analysis Result, Source 11 runtime, FinalSummaryReport runtime, report runtime, Sandbox/public event runtime, or delivery runtime.

## C. On-demand Collector Interpretation

The collector project is external to Sentigraph.

The collector is an on-demand task runner, evidence provider, and local package producer that may assist Sentigraph after an explicit operator decision.

The collector is not:

- a periodic crawler
- an embedded Sentigraph crawler
- a Sentigraph-controlled scheduler by default
- a Sentigraph background daemon
- a live crawler runtime inside Sentigraph
- a browser-profile bridge
- a cookie/session/proxy/anti-bot subsystem owned by Sentigraph

Sentigraph does not own collector runtime, browser profiles, cookies, sessions, proxies, anti-bot bypass, platform credentials, hidden APIs, or collector internals.

Sentigraph may consume exported metadata or results only after a collector-side on-demand task is completed outside Sentigraph runtime and a safe handoff artifact exists.

## D. Sentigraph Role

Sentigraph is a safe metadata consumer and governance runner.

Sentigraph may act as:

- safe metadata consumer
- provider_result reader
- package resolver
- review-only staging system
- Route C controlled evidence / case / analysis boundary processor
- governance chain runner

Sentigraph is not:

- a live crawler
- a scraping runtime
- a platform automation system
- a periodic collector scheduler
- a real-time platform fetcher
- an automatic Evidence Layer write system
- an automatic production case / analysis_run / Analysis Result system

## E. Future On-demand Workflow Shape

The future workflow shape is:

1. Sentigraph creates or records a controlled request metadata object.
2. The external collector receives or is manually given that request outside Sentigraph runtime.
3. The external collector executes an explicit on-demand task outside Sentigraph.
4. The collector exports provider_result metadata, package metadata, and/or an exported package.
5. Sentigraph reads only safe provider_result metadata first.
6. Sentigraph resolves package metadata with path guards.
7. Sentigraph enters review-only staging.
8. Future row preview, Evidence, case, and analysis steps remain gated by Route C and exact approval phrases.

8Z-1 does not implement any of these steps.

## F. Real-time Connection Meaning

Allowed interpretation of a future real-time or near-real-time connection:

- explicit on-demand request/result handoff
- operator-triggered handoff
- local exchange or governed metadata exchange
- metadata-first
- review-only before any row preview
- no automatic trust upgrade
- no automatic production object creation

Forbidden interpretation:

- periodic crawler
- continuous polling
- background scheduler
- auto-crawl from Sentigraph
- live HTTP bridge by default
- webhook bridge by default
- Sentigraph-initiated scrape/fetch
- automatic Evidence Layer write
- automatic production EvidenceItem, case, analysis_run, analysis execution, or Analysis Result

## G. Conceptual Contract Objects

8Z-1 introduces conceptual future-only object names. No schema or runtime is implemented now.

Future conceptual objects:

- `sentigraph_on_demand_collection_request_metadata_v0_1`
- `sentigraph_external_collector_provider_result_metadata_v0_1`, or existing `sentigraph_provider_job_result_v0_1` equivalent
- `exported_package_metadata_reference`
- `safe_metadata_handoff_summary`
- `review_only_staging_candidate`
- `route_c_governance_entry_summary`

Existing names should be reused when implementation is later approved. Current relevant existing concepts include `sentigraph_provider_job_result_v0_1`, safe provider handoff summary, package resolution summary, and review-only staging summary.

## H. Request Metadata Allowed Fields

Future request metadata may include:

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

These fields are not authorization for collector execution from Sentigraph runtime.

## I. Request Metadata Forbidden Fields

Future request metadata must not include:

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

## J. Provider Result / Package Metadata Allowed Fields

Future provider result or package metadata may include:

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
- path-safe package reference if an existing resolver supports it

These fields are metadata, not truth, not production evidence, and not official verification.

## K. Provider Result / Package Metadata Forbidden Fields

Future provider result or package metadata must not include:

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

## L. Relationship to Existing Metadata-only Surfaces

Existing metadata-only surfaces already establish useful boundaries:

- `local_exchange_reader.py` reads explicitly configured provider result metadata and blocks forbidden fields.
- `private_collector_provider_result_reader.py` validates provider result metadata and builds a safe handoff summary.
- `private_collector_package_resolver.py` resolves package metadata with path guards and reads only approved metadata files.
- `private_collector_review_only_staging.py` builds review-only staging candidates from safe metadata handoff summaries.

8Z-1 does not call or modify these helpers.

## M. Relationship to 8Y / 8W

8Y Route C remains stage-complete and paused at the controlled analysis result boundary/candidate checkpoint.

8Z workflow planning does not reopen 8W-70.

8Z workflow planning does not authorize production Analysis Result creation.

8Z workflow planning can only define future on-demand collector handoff governance.

8W-69 remains controlling for production Analysis Result authorization.

## N. Future Gates

Recommended future gates:

- 8Z-2 request/result metadata contract docs-only
- 8Z-3 controlled on-demand request metadata fixture smoke, if later approved
- 8Z-4 controlled provider_result metadata handoff smoke, if later approved
- 8Z-5 review-only staging handoff gate, if later approved

Route C gates remain separate for row preview, Evidence, case, and analysis boundaries.

8W authorization remains separate for production Analysis Result.

## O. Future 8Z-2 Phrase Status

Future 8Z-2 exact approval phrase:

```text
APPROVE_8Z_2_ON_DEMAND_COLLECTOR_REQUEST_RESULT_METADATA_CONTRACT_DOCS_ONLY
```

This phrase is inactive in 8Z-1. It must not authorize implementation, collector execution, provider jobs, row parsing, Evidence Layer write, production case, production analysis_run, actual analysis execution, or production Analysis Result.

## P. Relationship to Source 11 / Project Source

Source 11 update is not required unless Analysis Request / Provider / Import Governance runtime behavior changes.

8Z-1 does not change runtime behavior.

8Z-1 must not create Project Source files and must not create `docs/project_sources`.

Source update is not recommended after this single 8Z-1 docs-only contract. A future Source update may be considered only after a larger 8Z batch or on-demand workflow status patch is complete.

## Q. Final Decision

8Z-1 defines the on-demand collector cooperation contract and selects:

`ready_for_8Z_2_on_demand_collector_request_result_metadata_contract_docs_only`

The default next step is docs-only. No collector execution, provider job, runtime, route/API/frontend, Evidence Layer write, production object creation, analysis execution, Source 11 runtime, report runtime, public delivery, or production Analysis Result authorization is approved.
