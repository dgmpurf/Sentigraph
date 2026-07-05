# Sentigraph 8X-9 Dense Graph Preview to Report Candidate Gate Decision v0.1

## Decision

- phase: 8X-9
- decision: ready
- privacy_issue_stop: no
- docs_only: yes
- backend_code_changed: no
- tests_changed: no
- route_changed: no
- frontend_changed: no
- runtime_changed: no
- dense_graph_called: no
- report_candidate_created: no
- final_summary_report_created: no
- b_end_report_runtime_generated: no
- evidence_rows_parsed: no
- evidence_layer_write: no
- production_case_created: no
- production_analysis_run_created: no
- human_review_required: yes
- no_automatic_trust_upgrade: yes
- future_8x10_exact_approval_phrase_required: yes
- future_8x10_exact_approval_phrase_active: no
- selected_next_boundary_option: ready_for_8X_10_controlled_dense_graph_preview_report_candidate_bridge_smoke

## Current Anchor

8W-69 is complete and selected the pause boundary. Sentigraph must not continue to 8W-70 from this decision.

8X-1 proved this metadata-only path:

provider result metadata / synthetic package metadata
-> safe package resolver / provider result reader
-> review-only staging candidate

8X-1 did not use the External Collector Bridge validate path as the mainline and proved row-like files were not opened or parsed.

8X-2 proved this metadata-only path:

review-only staging candidate
-> existing staging candidate generated-run bridge
-> metadata-only minimum-real-run input candidate

8X-2 did not execute the minimum-real-run wrapper, did not create a generated run, did not call dense graph, and did not parse evidence rows.

8X-3 created a docs-only gate for a controlled 8X-4 minimum-real-run wrapper smoke.

8X-4 executed the existing minimum-real-run wrapper only inside a controlled backend test path and created a local controlled generated-run object. The generated run remained blocked because required fixture metadata was missing.

8X-5 created a docs-only gate for minimum fixture metadata completion.

8X-6 completed synthetic minimum-real-run fixture metadata and produced a local controlled generated-run object:

- generated_run_schema: `sentigraph_opinion_ecosystem_run_v0_1`
- generated_run_status: `ready`
- previous blocker cleared: `required_fixture_metadata_missing`

8X-7 created a docs-only gate for a controlled 8X-8 ready generated-run dense graph bridge smoke.

8X-8 proved this controlled backend test-path chain:

local controlled ready generated-run object
-> existing generated-run dense graph bridge
-> local controlled backend dense graph preview

8X-8 did not create a report candidate, write Evidence Layer records, create production case, create production analysis_run, add route/frontend/runtime persistence, or perform public/export delivery.

## Purpose

8X-9 is a docs-only gate decision. It defines whether a future 8X-10 may hand the 8X-8 local controlled backend dense graph preview to the existing dense graph report candidate bridge in a future controlled backend test-path smoke.

8X-9 does not call dense graph. It does not create a report candidate. It does not modify backend code, tests, routes, frontend code, runtime state, or Project Source files.

## 8X-8 Dense Graph Preview Interpretation

The 8X-8 dense graph preview is local controlled test-path preview only. It is not production-ready, customer-ready, frontend-ready, route-ready, official verification, causal proof, prediction, production scoring, FinalSummaryReport creation, B-end report runtime, or public event output.

The 8X-8 preview may be treated only as a safe local handoff candidate for a future controlled report candidate bridge smoke if all 8X-10 gate conditions remain satisfied.

## Allowed Future 8X-10 Input

Future 8X-10 may accept only this input:

- the local controlled backend dense graph preview created through the 8X-8 path
- dense_graph_preview scope is local controlled backend preview only
- anonymous aggregate/proxy boundary preserved
- frontend_ready: false
- route_ready: false
- production_ready: false
- customer_ready: false if present
- human_review_required: true
- no_automatic_trust_upgrade: true
- coefficient source remains `mock_default` or an existing safe local equivalent
- calibration status remains `uncalibrated` or an existing safe local equivalent
- empirical validation remains `not_started` or an existing safe local equivalent
- not_full_web semantics remain present
- not_full_platform semantics remain present
- not_full_thread semantics remain present
- not_official_verification semantics remain present
- not_causal_proof semantics remain present
- not_prediction semantics remain present
- not_production_score semantics remain present
- no evidence rows
- no raw comments or identities
- no author names or profile URLs as actual values
- no real package directory
- no private collector source
- no cookies, sessions, tokens, browser profiles, secrets, or private paths

Any input requiring row parsing, real package access, private collector inspection, real exchange directory reads, raw data exposure, route/frontend readiness, or production readiness must stop before 8X-10.

## Allowed Future 8X-10 Action

Future 8X-10 may be considered only as:

- backend-only
- test-first
- controlled smoke only
- synthetic/temp fixture only
- use the existing dense graph preview to report candidate bridge only from the safe 8X-8 local dense graph preview
- may produce a local backend report-candidate object only
- no FinalSummaryReport
- no B-end report runtime
- no Sandbox/public event runtime
- no route or frontend
- no runtime persistence
- no Evidence Layer write
- no production case
- no production analysis_run
- no production EvidenceItem
- no Review Queue runtime
- no export/download/public/final-delivery runtime
- no generated response text
- no public output or delivery

Future 8X-10 may prove only that the existing report candidate bridge can accept a safe local controlled dense graph preview under a backend test path. It must not claim final report readiness, public truth, official verification, causal proof, prediction, customer reporting, frontend readiness, route readiness, or production readiness.

## Hard Blockers

Pause or block before any future 8X-10 execution if any of these are needed or requested:

- parse `evidence_items.jsonl`
- parse `evidence_items.csv`
- parse `source_manifest.jsonl`
- parse `collection_log.jsonl`
- read original package rows
- read a real exchange directory
- read a real package directory
- inspect private collector source
- run a collector job
- call a real API
- call a real LLM
- use network access
- fetch a URL
- scrape a website
- write Evidence Layer records
- create a production case
- create a production analysis_run
- create a production EvidenceItem
- use Review Queue runtime
- expose raw comments or raw identities
- expose author names or profile URLs as actual values
- read or expose cookies, sessions, tokens, browser profiles, secrets, or private paths
- generate response text
- generate FinalSummaryReport
- generate B-end report runtime
- generate Sandbox/public event runtime
- create export/download/public/final-delivery runtime
- add a backend route/API
- add frontend UI
- add runtime persistence
- make broad service behavior changes
- perform any automatic trust upgrade
- use customer-ready or public-ready language
- modify Project Source files
- continue 8W-70

## Required Future 8X-10 Output Constraints

If a future 8X-10 controlled smoke is explicitly approved, its output must preserve:

- report_candidate_created: true only inside controlled backend test path
- report_candidate: present only as a local controlled backend object
- final_summary_report_created: false
- b_end_report_runtime_generated: false
- sandbox_public_event_runtime_generated: false
- evidence_rows_parsed: false
- evidence_layer_write: false
- production_case_created: false
- production_analysis_run_created: false
- production_evidence_item_created: false
- review_queue_runtime_used: false
- generated_response_text: false
- public_route_created: false
- export_download_public_delivery_created: false
- frontend_ready: false
- route_ready: false
- production_ready: false
- customer_ready: false
- human_review_required: true
- no_automatic_trust_upgrade: true
- coefficient_source: `mock_default` or existing safe local equivalent
- calibration_status: `uncalibrated` or existing safe local equivalent
- empirical_validation: `not_started` or existing safe local equivalent
- not_full_web semantics remain present
- not_full_platform semantics remain present
- not_official_verification semantics remain present
- not_causal_proof semantics remain present
- not_prediction semantics remain present
- not_production_score semantics remain present

The report candidate, if produced in a future phase, must remain a local internal candidate derived from dense graph preview metadata. It must not become a final report, B-end report runtime, export artifact, public event, public URL, signed URL, download package, or production object.

## Future Approval Phrase

Future 8X-10 requires this exact approval phrase:

`APPROVE_8X_10_CONTROLLED_DENSE_GRAPH_PREVIEW_REPORT_CANDIDATE_BRIDGE_SMOKE`

This phrase is inactive in 8X-9. Its presence in this document is a future gate definition only. It is not authorization for 8X-10 execution, not authorization for production Analysis Result creation, not final authorization, and not authorization for report candidate creation outside a controlled backend test path.

## Stop Rule

If any 8X-10 prompt omits the exact phrase, changes its spelling, adds production authorization language, expands scope to real package rows, requests FinalSummaryReport/B-end report/Sandbox/public event/export/public delivery, requests route/frontend/runtime persistence, requests customer-ready or public-ready output, requests broad service behavior changes, or requests trust upgrade, the correct next state is:

pause_or_blocked_before_report_candidate_bridge_smoke

## Source Recommendation

After commit, Source updates are optional and should be limited to high-level project-state summaries if needed. Do not update Source 11 unless existing Analysis Request / Provider / Import Governance runtime behavior changes.
