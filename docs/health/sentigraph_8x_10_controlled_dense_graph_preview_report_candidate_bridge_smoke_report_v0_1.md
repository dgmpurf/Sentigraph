# Sentigraph 8X-10 Controlled Dense Graph Preview Report Candidate Bridge Smoke Report v0.1

## Decision

- phase: 8X-10
- decision: ready
- privacy_issue_stop: no
- implementation_type: focused backend test plus tiny safety compatibility fix plus health report
- backend_service_code_changed: yes, minimal no-behavior-expansion readiness guard
- backend_route_changed: no
- frontend_changed: no
- runtime_changed: no
- project_source_changed: no

## Exact Approval Phrase

The required approval phrase for this controlled smoke was received:

`APPROVE_8X_10_CONTROLLED_DENSE_GRAPH_PREVIEW_REPORT_CANDIDATE_BRIDGE_SMOKE`

This phrase authorizes only the controlled backend test-path report candidate bridge smoke. It does not authorize production Analysis Result creation, FinalSummaryReport creation, B-end report runtime, Sandbox/public event runtime, production case creation, production analysis_run creation, Evidence Layer write, route/frontend work, runtime persistence, export/download/public delivery, or trust upgrade.

## Scope

This phase proves the safe 8X metadata bridge chain can reach the existing dense graph report candidate bridge only inside a controlled backend test path:

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
-> existing dense graph report candidate bridge
-> local controlled backend report-candidate object

## What Changed

The phase added one focused smoke test that drives the full synthetic metadata path into the existing dense graph report candidate bridge and asserts that the output remains local, controlled, selected-sample-only, human-review-required, and disconnected from final report/export/public surfaces.

A tiny compatibility fix was added to `dense_graph_report_candidate_bridge.py`:

- `customer_ready` is treated as an optional false-only readiness flag.
- If `customer_ready` is absent, existing safe inputs continue normally.
- If `customer_ready = true` appears in a dense graph preview or integration object, candidate creation is blocked as a requested side effect.
- Local report candidate output explicitly keeps `customer_ready = false`.

No route, frontend, runtime persistence, production object, export, or public delivery behavior was added.

## What Was Proven

- A synthetic provider result metadata file can be read by the metadata-only provider result reader.
- A synthetic package metadata directory can be resolved by package name under a configured temporary export root.
- A review-only staging candidate can be created from safe metadata handoff.
- The staging candidate can feed the generated-run bridge candidate path.
- The generated-run bridge can feed the existing minimum-real-run wrapper.
- Synthetic `stage_id` fixture metadata clears the previous `required_fixture_metadata_missing` blocker.
- A local controlled ready generated-run object is returned.
- The local controlled ready generated-run object can enter the existing dense graph bridge.
- A local controlled backend dense graph preview is returned.
- The dense graph preview can enter the existing report candidate bridge.
- A local controlled backend report-candidate object is returned.
- Human review remains required.
- No automatic trust upgrade occurs.

## Dense Graph Preview Status

- dense_graph_preview_present: true
- dense_graph_preview_scope: local controlled backend preview only
- dense_graph_preview_type: anonymous aggregate/proxy
- frontend_ready: false
- route_ready: false
- production_ready: false

## Report Candidate Status

- report_candidate_created: true, only inside controlled backend test path
- report_candidate_status: `candidate_ready`
- report_candidate_schema: `sentigraph_dense_graph_report_candidate_v0_1`
- report_candidate_mode: `backend_only_local_report_candidate`
- report_candidate_scope: `selected_sample_only_dense_graph_preview`
- customer_ready: false
- frontend_ready: false
- route_ready: false
- production_ready: false
- export_ready: false
- public_ready: false
- final_report_ready: false

The candidate-ready status is local and controlled. It does not mean final report readiness, B-end report readiness, customer readiness, public readiness, export readiness, production readiness, official verification, causal proof, prediction, or production score.

## Evidence Row Boundary

Synthetic row-like files were created only as presence markers:

- `evidence_items.jsonl`
- `evidence_items.csv`
- `source_manifest.jsonl`
- `collection_log.jsonl`

The focused smoke monkeypatches `Path.read_text` to fail if these files are opened. The passing test proves this handoff path did not open or parse them.

## Downstream Boundary

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

- wrong or missing dense graph preview does not create a report candidate
- missing dense graph summary blocks candidate creation
- `frontend_ready = true` blocks candidate creation
- `route_ready = true` blocks candidate creation
- `production_ready = true` blocks candidate creation
- `customer_ready = true` blocks candidate creation
- forbidden active fields block without exposing sentinel values
- FinalSummaryReport entrypoints are monkeypatched to fail if called
- row-like file reads are monkeypatched to fail if opened

## Files Added or Updated

- `backend/app/tests/test_private_collector_dense_graph_preview_report_candidate_bridge_smoke.py`
- `backend/app/services/dense_graph_report_candidate_bridge.py`
- `docs/health/sentigraph_8x_10_controlled_dense_graph_preview_report_candidate_bridge_smoke_report_v0_1.md`

## Validation Results

Focused validation:

```bash
python -m pytest backend/app/tests/test_private_collector_dense_graph_preview_report_candidate_bridge_smoke.py -q
```

Result: pass, 5 passed.

Relevant nearby validation:

```bash
python -m pytest backend/app/tests/test_private_collector_ready_generated_run_dense_graph_bridge_smoke.py backend/app/tests/test_generated_run_dense_graph_bridge_integration.py backend/app/tests/test_dense_graph_report_candidate_bridge.py -q
```

Result: pass, 19 passed.

Upstream metadata chain validation:

```bash
python -m pytest backend/app/tests/test_private_collector_metadata_bridge_minimum_real_run_fixture_metadata_completion_smoke.py backend/app/tests/test_private_collector_metadata_bridge_minimum_real_run_wrapper_execution_smoke.py backend/app/tests/test_staging_candidate_generated_run_bridge.py -q
```

Result: pass, 9 passed.

Nearby safety validation:

```bash
python -m pytest backend/app/tests/test_local_exchange_reader.py backend/app/tests/test_analysis_request_golden_contracts.py -q
```

Result: pass, 16 passed.

Static validation:

```bash
python -m py_compile backend/app/services/private_collector_package_resolver.py backend/app/services/private_collector_provider_result_reader.py backend/app/services/private_collector_review_only_staging.py backend/app/services/staging_candidate_generated_run_bridge.py backend/app/services/minimum_real_run_bridge_execution.py backend/app/services/generated_run_dense_graph_bridge_integration.py backend/app/services/dense_graph_report_candidate_bridge.py
git diff --check
git status --short
```

Result: run after this report was added; see final task summary.

## Not Implemented

- No 8W-70 continuation.
- No production authorization.
- No production Analysis Result.
- No FinalSummaryReport.
- No B-end report runtime.
- No Sandbox/public event runtime.
- No production case.
- No production analysis_run.
- No Evidence Layer write.
- No production EvidenceItem.
- No Review Queue runtime.
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
- No customer-ready, public-ready, production-ready, final-ready, or export-ready output.

## Next Recommended Task

Phase 8X-11 should remain conservative. A safe next slice would be a docs-only gate decision about whether the local controlled report candidate may be considered for a future FinalSummaryReport boundary decision. It should not create FinalSummaryReport without a new exact approval phrase and should not add routes, frontend, runtime state, Evidence Layer writes, production objects, export/download/public delivery, or trust upgrades.
