# Sentigraph 8X-8 Controlled Ready Generated-run Dense Graph Bridge Smoke Report v0.1

## Decision

- phase: 8X-8
- decision: ready
- privacy_issue_stop: no
- implementation_type: focused backend test plus health report
- backend_service_code_changed: no
- backend_route_changed: no
- frontend_changed: no
- runtime_changed: no
- project_source_changed: no

## Exact Approval Phrase

The required approval phrase for this controlled smoke was received:

`APPROVE_8X_8_CONTROLLED_READY_GENERATED_RUN_DENSE_GRAPH_BRIDGE_SMOKE`

This phrase authorizes only the controlled backend test-path dense graph bridge smoke. It does not authorize production Analysis Result creation, production case creation, production analysis_run creation, Evidence Layer write, report candidate creation, route/frontend work, runtime persistence, or public delivery.

## Scope

This phase proves the safe 8X metadata bridge chain can reach the existing dense graph bridge only inside a controlled backend test path:

provider result metadata / controlled local synthetic package metadata
-> safe package resolver / provider result reader
-> review-only staging candidate
-> staging generated-run bridge
-> metadata-only minimum-real-run input candidate
-> completed synthetic minimum-real-run fixture metadata
-> existing minimum-real-run wrapper
-> local controlled ready generated-run object
-> existing generated-run to dense graph bridge
-> local controlled backend dense graph preview

## What Changed

No service code was changed.

The phase added one focused smoke test that drives the full synthetic metadata path into the existing generated-run dense graph bridge and asserts that the output remains local, anonymous aggregate/proxy, selected-sample-only, uncalibrated, and human-review-required.

## What Was Proven

- A synthetic provider result metadata file can be read by the metadata-only provider result reader.
- A synthetic package metadata directory can be resolved by package name under a configured temporary export root.
- A review-only staging candidate can be created from safe metadata handoff.
- The staging candidate can feed the generated-run bridge candidate path.
- The generated-run bridge can feed the existing minimum-real-run wrapper.
- Synthetic `stage_id` fixture metadata clears the previous `required_fixture_metadata_missing` blocker.
- A local controlled ready generated-run object is returned.
- The local controlled ready generated-run object can enter the existing dense graph bridge.
- Dense graph execution occurs exactly inside the controlled backend test path.
- The dense graph preview remains a local controlled test-path object.
- Human review remains required.
- No automatic trust upgrade occurs.

## Generated-run Status

- minimum_real_run_executed: true, only inside controlled backend test path
- generated_run_created: local controlled test-path object only
- generated_run_schema: `sentigraph_opinion_ecosystem_run_v0_1`
- generated_run_status: `ready`
- coefficient_source: `mock_default`
- calibration_status: `uncalibrated`
- empirical_validation: `not_started`
- human_review_required: true

The ready status is local and controlled. It does not mean production readiness, production Analysis Result creation, official verification, causal proof, prediction, or production score.

## Dense Graph Status

- dense_graph_called: true, only inside controlled backend test path
- dense_graph_preview_present: true
- dense_graph_preview_scope: local controlled backend preview only
- dense_graph_preview_type: anonymous aggregate/proxy
- frontend_ready: false
- route_ready: false
- production_ready: false

The dense graph preview does not authorize a report candidate, frontend integration, route integration, public event generation, public delivery, or customer-ready output.

## Evidence Row Boundary

Synthetic row-like files were created only as presence markers:

- `evidence_items.jsonl`
- `evidence_items.csv`
- `source_manifest.jsonl`
- `collection_log.jsonl`

The focused smoke monkeypatches `Path.read_text` to fail if these files are opened. The passing test proves this handoff path did not open or parse them.

## Downstream Boundary

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

## Safety Boundaries

- collector_run: false
- real_api_called: false
- real_llm_called: false
- network_access: false
- url_fetching: false
- scraping: false
- private_collector_inspected: false
- real_exchange_dir_read: false
- real_package_dir_read: false
- original_package_rows_read: false
- raw_comments_exposed: false
- raw_identities_exposed: false
- author_names_or_profile_urls_exposed: false
- secrets_read: false
- automatic_trust_upgrade: false

## Negative Coverage

The focused smoke also proves:

- blocked generated-run objects do not call dense graph
- missing generated-run objects do not call dense graph
- missing generated-run boundary flags block before dense graph
- forbidden active fields block without exposing sentinel values
- report candidate bridge entrypoints are monkeypatched to fail if called
- row-like file reads are monkeypatched to fail if opened

## Files Added

- `backend/app/tests/test_private_collector_ready_generated_run_dense_graph_bridge_smoke.py`
- `docs/health/sentigraph_8x_8_controlled_ready_generated_run_dense_graph_bridge_smoke_report_v0_1.md`

## Validation Results

Focused validation:

```bash
python -m pytest backend/app/tests/test_private_collector_ready_generated_run_dense_graph_bridge_smoke.py -q
```

Result: pass, 4 passed.

Relevant nearby validation:

```bash
python -m pytest backend/app/tests/test_private_collector_metadata_bridge_minimum_real_run_fixture_metadata_completion_smoke.py backend/app/tests/test_private_collector_metadata_bridge_minimum_real_run_wrapper_execution_smoke.py backend/app/tests/test_generated_run_dense_graph_bridge_integration.py backend/app/tests/test_staging_candidate_generated_run_bridge.py -q
```

Result: pass, 17 passed.

Nearby safety validation:

```bash
python -m pytest backend/app/tests/test_local_exchange_reader.py backend/app/tests/test_analysis_request_golden_contracts.py -q
```

Result: pass, 16 passed.

Static validation:

```bash
git diff --check
git status --short
```

Result: run after this report was added; see final task summary.

## Not Implemented

- No 8W-70 continuation.
- No production authorization.
- No production Analysis Result.
- No production case.
- No production analysis_run.
- No Evidence Layer write.
- No production EvidenceItem.
- No Review Queue runtime.
- No report candidate.
- No B-end report runtime.
- No Sandbox/public event runtime.
- No generated response text.
- No backend route/API.
- No frontend.
- No runtime persistence.
- No export/download/public/final-delivery runtime.
- No External Collector Bridge validate-path integration.
- No private collector inspection.
- No collector job.
- No real exchange directory read.
- No real package directory read outside synthetic temporary fixtures.
- No real API or LLM.
- No URL fetching or scraping.

## Next Recommended Task

Phase 8X-9 should remain conservative. A safe next slice would be a docs-only gate decision about whether the local controlled dense graph preview may be considered for a future report-candidate gate smoke. It should not create a report candidate without a new exact approval phrase and should not add routes, frontend, runtime state, Evidence Layer writes, production objects, export/download/public delivery, or trust upgrades.
