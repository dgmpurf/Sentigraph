# Sentigraph 8X-5 Minimum-real-run Fixture Metadata Completion Gate Decision v0.1

## Decision

- phase: 8X-5
- decision: ready
- privacy_issue_stop: no
- docs_only: yes
- backend_code_changed: no
- tests_changed: no
- route_changed: no
- frontend_changed: no
- runtime_changed: no
- fixture_metadata_completed: no
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
- future_8x6_exact_approval_phrase_required: yes
- future_8x6_exact_approval_phrase_active: no
- selected_next_boundary_option: ready_for_8X_6_controlled_metadata_bridge_minimum_real_run_fixture_metadata_completion_smoke

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

## 8X-4 Blocked Result Interpretation

The 8X-4 blocked generated-run status is a safe conservative outcome, not a failure. It proves the wrapper can be reached through the metadata bridge while preserving strict boundaries.

The current blocker is:

- required_fixture_metadata_missing

8X-5 does not complete fixture metadata. It only defines the future gate for deciding whether 8X-6 may complete the minimum fixture metadata needed by the existing wrapper.

## Purpose

8X-5 is a docs-only gate decision. It defines whether a future 8X-6 may complete minimum-real-run fixture metadata for the synthetic metadata bridge candidate and rerun the existing minimum-real-run wrapper in a controlled backend test path.

8X-5 does not execute the wrapper, create a generated run, modify code, add tests, or create runtime state.

## Allowed Future 8X-6 Input

Future 8X-6 may consider only this input:

- metadata-only minimum-real-run input candidate created through the 8X-2 and 8X-4 bridge path
- synthetic/temp fixture metadata only
- only the minimum fixture metadata required by the existing minimum-real-run wrapper
- no evidence rows
- no raw comments
- no raw identities
- no author names or profile URLs as actual values
- no real package directory
- no private collector source
- no cookies, sessions, tokens, browser profiles, secrets, or private paths

Any input that requires row parsing, real package access, private collector inspection, or real exchange directory access must stop before 8X-6 execution.

## Allowed Future 8X-6 Action

Future 8X-6 may be considered only as:

- backend-only
- test-first
- controlled smoke only
- synthetic/temp fixture only
- complete the minimum fixture metadata required by the existing minimum-real-run wrapper
- rerun the existing minimum-real-run wrapper from a safe metadata bridge candidate
- produce a local controlled generated-run object only
- clear the `required_fixture_metadata_missing` blocker only if the existing wrapper contract supports it
- no dense graph
- no report candidate
- no route or frontend
- no runtime persistence
- no Evidence Layer write
- no production case
- no production analysis_run
- no production EvidenceItem

Future 8X-6 may prove fixture metadata compatibility. It must not claim production readiness, official verification, causal proof, prediction, or customer-ready reporting.

## Hard Blockers

Pause or block before any future 8X-6 execution if any of these are needed:

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
- add runtime persistence
- make broad service behavior changes
- perform any automatic trust upgrade
- modify Project Source files
- continue 8W-70

## Required Future 8X-6 Output Constraints

If a future 8X-6 controlled smoke is explicitly approved, its output must preserve:

- minimum_real_run_executed: true only inside controlled backend test path
- generated_run may be present only as a local controlled test-path object
- generated_run_status may become non-blocked only if the existing wrapper contract permits it
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
- coefficient_source: `mock_default` or existing safe local equivalent
- calibration_status: `uncalibrated` or existing safe local equivalent
- empirical_validation: `not_started` or existing safe local equivalent

The future smoke must not turn provider output into truth, official verification, causal proof, prediction, production score, or production Analysis Result.

## Future Approval Phrase

Future 8X-6 requires this exact approval phrase:

`APPROVE_8X_6_CONTROLLED_METADATA_BRIDGE_MINIMUM_REAL_RUN_FIXTURE_METADATA_COMPLETION_SMOKE`

This phrase is inactive in 8X-5. Its presence in this document is a future gate definition only. It is not authorization for 8X-6 execution, production Analysis Result creation, production case creation, Evidence Layer write, report generation, or public delivery.

## Stop Rule

If any 8X-6 prompt omits the exact phrase, changes its spelling, adds production authorization language, expands scope to real package rows, requests dense graph/report/public delivery, or requests broad service behavior changes, the correct next state is:

pause_or_blocked_before_fixture_metadata_completion

## Source Recommendation

After commit, Source updates are optional and should be limited to high-level project-state summaries if needed. Do not update Source 11 unless existing Analysis Request / Provider / Import Governance runtime behavior changes.
