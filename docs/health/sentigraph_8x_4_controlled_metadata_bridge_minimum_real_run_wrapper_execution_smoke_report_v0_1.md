# Sentigraph 8X-4 Controlled Metadata Bridge Minimum-real-run Wrapper Execution Smoke Report v0.1

## Decision

- phase: 8X-4
- decision: ready
- privacy_issue_stop: no
- implementation_type: test-only smoke plus health report
- backend_service_code_changed: no
- backend_route_changed: no
- frontend_changed: no
- runtime_changed: no
- project_source_changed: no

## Exact Approval Phrase

The required approval phrase for this controlled smoke was received:

`APPROVE_8X_4_CONTROLLED_METADATA_BRIDGE_MINIMUM_REAL_RUN_WRAPPER_EXECUTION_SMOKE`

This phrase authorizes only the controlled backend test-path wrapper smoke. It does not authorize production Analysis Result creation, production case creation, Evidence Layer write, dense graph, report candidate, route/frontend work, or public delivery.

## Scope

This phase proves the safe metadata bridge can execute the existing minimum-real-run wrapper inside a controlled backend test path:

provider result metadata / controlled local synthetic package metadata
-> safe package resolver / provider result reader
-> review-only staging candidate
-> existing staging candidate generated-run bridge
-> metadata-only minimum-real-run input candidate
-> existing minimum-real-run wrapper
-> local controlled generated-run object

## What Was Proven

- A synthetic provider result metadata file can be read by the metadata-only provider result reader.
- A synthetic package metadata directory can be resolved by package name under a configured temporary export root.
- A review-only staging candidate can be created from safe metadata handoff.
- The staging candidate can feed the generated-run bridge candidate path.
- The generated-run bridge can feed the existing minimum-real-run wrapper.
- The wrapper executes only in the controlled backend test path.
- A local controlled generated-run object is returned.
- The generated-run object remains blocked because the synthetic bridge fixture does not satisfy all minimum-real-run fixture metadata requirements.
- Human review remains required.
- No automatic trust upgrade occurs.

## Generated-run Status

- minimum_real_run_executed: true, only inside controlled backend test path
- generated_run_created: local controlled test-path object only
- generated_run_schema: `sentigraph_opinion_ecosystem_run_v0_1`
- generated_run_status: `blocked`
- blocking reason observed: `required_fixture_metadata_missing`

The blocked run status is intentional and conservative for this phase. 8X-4 proves wrapper compatibility, not analysis readiness or production readiness.

## Evidence Row Boundary

Synthetic row-like files were created only as presence markers:

- `evidence_items.jsonl`
- `evidence_items.csv`
- `source_manifest.jsonl`
- `collection_log.jsonl`

The focused smoke monkeypatches `Path.read_text` to fail if these files are opened. The passing test proves this handoff path did not open or parse them.

## Downstream Boundary

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

## Safety Boundaries

- collector_run: false
- real_api_called: false
- real_llm_called: false
- url_fetching: false
- scraping: false
- private_collector_inspected: false
- real_exchange_dir_read: false
- original_package_rows_read: false
- raw_comments_exposed: false
- raw_identities_exposed: false
- secrets_read: false

## Files Added

- `backend/app/tests/test_private_collector_metadata_bridge_minimum_real_run_wrapper_execution_smoke.py`
- `docs/health/sentigraph_8x_4_controlled_metadata_bridge_minimum_real_run_wrapper_execution_smoke_report_v0_1.md`

## Validation Plan

Required focused validation:

```bash
python -m pytest backend/app/tests/test_private_collector_metadata_bridge_minimum_real_run_wrapper_execution_smoke.py -q
```

Relevant nearby validation:

```bash
python -m pytest backend/app/tests/test_private_collector_review_only_staging_to_generated_run_bridge_handoff_smoke.py backend/app/tests/test_private_collector_provider_result_to_review_only_staging_handoff_smoke.py backend/app/tests/test_minimum_real_run_bridge_execution.py backend/app/tests/test_staging_candidate_generated_run_bridge.py -q
python -m pytest backend/app/tests/test_local_exchange_reader.py backend/app/tests/test_analysis_request_golden_contracts.py -q
```

Static validation:

```bash
git diff --check
git status --short
```

## Not Implemented

- No 8W-70 continuation.
- No production authorization.
- No production Analysis Result.
- No production case.
- No production analysis_run.
- No Evidence Layer write.
- No production EvidenceItem.
- No Review Queue runtime.
- No dense graph call.
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
- No real API or LLM.
- No URL fetching or scraping.

## Next Recommended Task

Phase 8X-5 should remain conservative. A safe next slice would be a docs-only decision about whether to add the missing controlled fixture metadata required for the minimum-real-run wrapper to return a non-blocked local test-path run. It should not call dense graph, create report candidates, write runtime state, or produce production objects.
