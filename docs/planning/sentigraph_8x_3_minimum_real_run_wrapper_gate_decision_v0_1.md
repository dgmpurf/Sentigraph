# Sentigraph 8X-3 Minimum-real-run Wrapper Gate Decision v0.1

## Decision

- phase: 8X-3
- decision: ready
- privacy_issue_stop: no
- docs_only: yes
- backend_code_changed: no
- tests_changed: no
- route_changed: no
- frontend_changed: no
- runtime_changed: no
- minimum_real_run_executed: no
- generated_run_created: no
- dense_graph_called: no
- report_candidate_created: no
- evidence_rows_parsed: no
- evidence_layer_write: no
- production_case_created: no
- production_analysis_run_created: no
- human_review_required: yes
- no_automatic_trust_upgrade: yes
- future_8x4_exact_approval_phrase_required: yes
- future_8x4_exact_approval_phrase_active: no
- selected_next_boundary_option: ready_for_8X_4_controlled_metadata_bridge_minimum_real_run_wrapper_execution_smoke

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

## Purpose

8X-3 is a docs-only gate decision. It decides whether the 8X metadata-only bridge candidate may later be passed to the existing minimum-real-run wrapper in a future controlled backend-only smoke.

8X-3 does not authorize production Analysis Result creation. It does not authorize final production execution. It does not execute any wrapper or generate any runtime object.

## Allowed Future 8X-4 Input

Future 8X-4 may consider only this input:

- a metadata-only minimum-real-run input candidate created through the 8X-2 bridge path
- safe provider metadata
- safe review-only staging metadata
- synthetic/temp fixture package metadata unless a later prompt explicitly narrows and approves a different local input
- no evidence rows
- no raw comments
- no raw identities
- no author names or profile URLs as actual values
- no cookies, sessions, tokens, browser profiles, secrets, or private paths

Any input that requires row parsing, private collector inspection, or real exchange directory access must stop before 8X-4 execution.

## Allowed Future 8X-4 Action

Future 8X-4 may be considered only as:

- backend-only
- test-first
- controlled smoke only
- synthetic/temp fixture only unless explicitly approved otherwise
- execute the existing minimum-real-run wrapper only from the safe metadata bridge candidate
- no dense graph
- no report candidate
- no route or frontend
- no runtime persistence
- no production Evidence Layer write
- no production case
- no production analysis_run
- no generated response text
- no public output

The future smoke may prove wrapper compatibility with a safe candidate, but it must not claim production readiness or public truth.

## Hard Blockers

Pause or block before any future 8X-4 execution if any of these are needed:

- parse `evidence_items.jsonl`
- parse `evidence_items.csv`
- parse `source_manifest.jsonl`
- parse `collection_log.jsonl`
- read original package rows
- read a real exchange directory
- inspect private collector source
- run a collector job
- call a real API
- call a real LLM
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
- call dense graph
- create a report candidate
- generate B-end report runtime
- generate Sandbox/public event runtime
- create export/download/public/final-delivery runtime
- add a backend route/API
- add frontend UI
- modify Project Source files
- continue 8W-70

## Required Future 8X-4 Output Constraints

If a future 8X-4 controlled smoke is explicitly approved, its output must preserve:

- minimum_real_run_executed: true only inside the controlled backend test path
- generated_run may be present only as a local controlled test-path object
- dense_graph_called: false
- report_candidate_created: false
- evidence_rows_parsed: false
- evidence_layer_write: false
- production_case_created: false
- production_analysis_run_created: false
- production_evidence_item_created: false
- review_queue_runtime_used: false
- b_end_report_runtime_generated: false
- sandbox_public_event_runtime_generated: false
- generated_response_text: false
- public_route_created: false
- export_download_public_delivery_created: false
- human_review_required: true
- no_automatic_trust_upgrade: true

The future smoke must not turn provider output into truth, official verification, causal proof, prediction, or production score.

## Future Approval Phrase

Future 8X-4 requires this exact approval phrase:

`APPROVE_8X_4_CONTROLLED_METADATA_BRIDGE_MINIMUM_REAL_RUN_WRAPPER_EXECUTION_SMOKE`

This phrase is inactive in 8X-3. Its presence in this document is a future gate definition only. It is not authorization for 8X-4 execution, not authorization for production Analysis Result creation, and not final authorization for any production runtime.

## Stop Rule

If any 8X-4 prompt omits the exact phrase, changes its spelling, adds production authorization language, expands scope to real package rows, or requests dense graph/report/public delivery, the correct next state is:

pause_or_blocked_before_minimum_real_run_wrapper_execution

## Source Recommendation

After commit, Source updates are optional and should be limited to high-level project-state summaries if needed. Do not update Source 11 unless existing Analysis Request / Provider / Import Governance runtime behavior changes.
