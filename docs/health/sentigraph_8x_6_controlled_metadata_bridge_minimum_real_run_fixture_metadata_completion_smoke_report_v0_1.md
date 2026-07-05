# Sentigraph 8X-6 Controlled Metadata Bridge Minimum-real-run Fixture Metadata Completion Smoke Report v0.1

## Decision

- phase: 8X-6
- decision: ready
- privacy_issue_stop: no
- implementation_type: focused backend test plus tiny compatibility fix plus health report
- backend_service_code_changed: yes, minimal compatibility fix
- backend_route_changed: no
- frontend_changed: no
- runtime_changed: no
- project_source_changed: no

## Exact Approval Phrase

The required approval phrase for this controlled smoke was received:

`APPROVE_8X_6_CONTROLLED_METADATA_BRIDGE_MINIMUM_REAL_RUN_FIXTURE_METADATA_COMPLETION_SMOKE`

This phrase authorizes only the controlled backend test-path fixture metadata completion smoke. It does not authorize production Analysis Result creation, production case creation, Evidence Layer write, dense graph, report candidate, route/frontend work, runtime persistence, or public delivery.

## Scope

This phase proves the safe metadata bridge can complete the minimum synthetic fixture metadata required by the existing minimum-real-run wrapper:

provider result metadata / controlled local synthetic package metadata
-> safe package resolver / provider result reader
-> review-only staging candidate
-> existing staging candidate generated-run bridge
-> metadata-only minimum-real-run input candidate
-> completed synthetic minimum-real-run fixture metadata
-> existing minimum-real-run wrapper
-> local controlled generated-run object

## What Changed

The focused smoke adds `stage_id` to the synthetic `minimum_real_run_input_candidate.fixture_metadata`.

A tiny compatibility fix preserves that safe `stage_id` when `minimum_real_run_bridge_execution` builds the local mock fixture for the existing minimum-real-run wrapper.

No other service behavior was expanded.

## What Was Proven

- A synthetic provider result metadata file can be read by the metadata-only provider result reader.
- A synthetic package metadata directory can be resolved by package name under a configured temporary export root.
- A review-only staging candidate can be created from safe metadata handoff.
- The staging candidate can feed the generated-run bridge candidate path.
- The generated-run bridge can feed the existing minimum-real-run wrapper.
- The synthetic `stage_id` fixture metadata clears the previous `required_fixture_metadata_missing` blocker.
- The wrapper executes only in the controlled backend test path.
- A local controlled generated-run object is returned.
- Human review remains required.
- No automatic trust upgrade occurs.

## Generated-run Status

- minimum_real_run_executed: true, only inside controlled backend test path
- generated_run_created: local controlled test-path object only
- generated_run_schema: `sentigraph_opinion_ecosystem_run_v0_1`
- generated_run_status: `ready`
- previous blocker cleared: `required_fixture_metadata_missing`

The ready status is local and controlled. It does not mean production readiness, production Analysis Result creation, official verification, causal proof, prediction, or production score.

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
- automatic_trust_upgrade: false

## Files Added or Updated

- `backend/app/tests/test_private_collector_metadata_bridge_minimum_real_run_fixture_metadata_completion_smoke.py`
- `backend/app/services/minimum_real_run_bridge_execution.py`
- `docs/health/sentigraph_8x_6_controlled_metadata_bridge_minimum_real_run_fixture_metadata_completion_smoke_report_v0_1.md`

## Validation Plan

Required focused validation:

```bash
python -m pytest backend/app/tests/test_private_collector_metadata_bridge_minimum_real_run_fixture_metadata_completion_smoke.py -q
```

Relevant nearby validation:

```bash
python -m pytest backend/app/tests/test_private_collector_metadata_bridge_minimum_real_run_wrapper_execution_smoke.py backend/app/tests/test_private_collector_review_only_staging_to_generated_run_bridge_handoff_smoke.py backend/app/tests/test_private_collector_provider_result_to_review_only_staging_handoff_smoke.py backend/app/tests/test_minimum_real_run_bridge_execution.py backend/app/tests/test_staging_candidate_generated_run_bridge.py -q
python -m pytest backend/app/tests/test_local_exchange_reader.py backend/app/tests/test_analysis_request_golden_contracts.py -q
```

Static validation:

```bash
python -m py_compile backend/app/services/minimum_real_run_bridge_execution.py
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

Phase 8X-7 should remain conservative. A safe next slice would be a docs-only decision about whether this local controlled ready generated-run object may be handed to the existing dense graph gate in a future controlled test-path smoke. It should not call dense graph without a new exact approval phrase and should not create report candidates, routes, frontend, runtime state, or production objects.
