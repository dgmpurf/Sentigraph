# Sentigraph 8X-2 Metadata-only Review-only Staging to Generated-run Bridge Handoff Smoke Report v0.1

## Decision

- phase: 8X-2
- decision: ready
- privacy_issue_stop: no
- implementation_type: test-only smoke plus health report
- backend_service_code_changed: no
- backend_route_changed: no
- frontend_changed: no
- runtime_changed: no
- project_source_changed: no

## Scope

This phase strengthens the safe backend mainline from review-only staging to the existing generated-run bridge candidate path:

provider result metadata / controlled local package metadata
-> safe package resolver / provider result reader
-> review-only staging candidate
-> existing staging candidate generated-run bridge
-> metadata-only minimum-real-run input candidate

This phase does not execute the minimum real-run wrapper. It does not create a generated run. It only proves that a safe review-only staging summary can feed the bridge candidate path.

## What Was Proven

- A synthetic provider result metadata file can be read by the metadata-only provider result reader.
- A synthetic exported package directory can be resolved by package name under a configured temporary export root.
- A review-only staging candidate can be created from the provider reader's safe metadata handoff.
- The review-only staging safe summary can be fed into `build_staging_candidate_generated_run_bridge`.
- The bridge returns `ready_for_minimum_real_run_input_candidate`.
- The bridge output remains metadata-only.
- The bridge creates only a `minimum_real_run_input_candidate` object.
- The bridge does not request a generated run.
- The bridge does not execute the minimum real-run wrapper.
- The bridge does not call dense graph generation.
- The bridge does not parse evidence rows.
- The bridge does not write Evidence Layer, create a production case, or create a production analysis run.
- Human review remains required.
- No automatic trust upgrade occurs.

## Evidence Row Boundary

Synthetic row-like files were created only as presence markers:

- `evidence_items.jsonl`
- `evidence_items.csv`
- `source_manifest.jsonl`
- `collection_log.jsonl`

The focused smoke monkeypatches `Path.read_text` to fail if these files are opened. The passing test proves this handoff path did not open or parse them.

## Minimum Real-run / Generated-run Boundary

- minimum_real_run_executed: false
- generated_run_created: false
- generated_run_requested: false
- dense_graph_called: false
- report_candidate_created: false

The smoke monkeypatches minimum real-run and dense graph entrypoints to fail if called. The passing test proves this phase only builds the bridge handoff candidate.

## Safety Boundaries

- collector_run: false
- real_api_called: false
- real_llm_called: false
- url_fetching: false
- scraping: false
- evidence_rows_parsed: false
- evidence_layer_write: false
- production_case_created: false
- production_analysis_run_created: false
- generated_response_text: false
- public_route_created: false
- runtime_side_effects: all false

## Files Added

- `backend/app/tests/test_private_collector_review_only_staging_to_generated_run_bridge_handoff_smoke.py`
- `docs/health/sentigraph_8x_2_metadata_only_review_only_staging_to_generated_run_bridge_handoff_smoke_report_v0_1.md`

## Validation Plan

Required focused validation:

```bash
python -m pytest backend/app/tests/test_private_collector_review_only_staging_to_generated_run_bridge_handoff_smoke.py -q
```

Relevant nearby validation:

```bash
python -m pytest backend/app/tests/test_private_collector_provider_result_to_review_only_staging_handoff_smoke.py backend/app/tests/test_staging_candidate_generated_run_bridge.py -q
python -m pytest backend/app/tests/test_local_exchange_reader.py backend/app/tests/test_analysis_request_golden_contracts.py -q
```

Static validation:

```bash
git diff --check
git status --short
```

## Not Implemented

- No 8W-70 continuation.
- No authorization.
- No production Analysis Result.
- No minimum real-run execution.
- No generated run creation.
- No dense graph call.
- No report candidate creation.
- No External Collector Bridge validate-path integration.
- No backend route.
- No frontend UI.
- No runtime persistence.
- No real exchange directory read.
- No private collector inspection.
- No collector job.
- No real API or LLM.
- No URL fetching or scraping.
- No Evidence Layer write.
- No production case, production EvidenceItem, production analysis run, Review Queue runtime, B-end report, Sandbox/public event, export/download/public/final-delivery runtime.

## Next Recommended Task

Phase 8X-3 should remain conservative. A safe next slice would be a docs-only or tests-only decision for whether this metadata-only bridge candidate may be passed to the existing minimum-real-run wrapper under explicit disabled/default-off boundaries. It should not execute the wrapper unless a later exact approval phrase explicitly authorizes a controlled runtime smoke.
