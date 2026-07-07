# Sentigraph 8Z-10A/8Z-11 Batch Controlled Evidence Candidate Phrase Repair and Smoke Report v0.1

phase = 8Z-10A/8Z-11
decision = ready
privacy_issue_stop = no
batch_prompt = yes
batch_phrase = APPROVE_8Z_10A_11_BATCH_REPAIR_CONTROLLED_EVIDENCE_CANDIDATE_HELPER_PHRASE_REGATE_AND_SMOKE
repair_completion_phrase = APPROVE_8Z_10A_11_REPAIR_8Y6_HELPER_PHRASE_EXPECTATION_AND_COMPLETE_BATCH_VALIDATION
helper_phrase_repair_performed = yes
helper_phrase_repair_needed = yes
repaired_helper_phrase = APPROVE_8W_10_CONTROLLED_EVIDENCE_CANDIDATE_IMPLEMENTATION
old_chinese_helper_phrase_rejected = yes
old_mojibake_helper_phrase_rejected = yes
old_garbled_helper_phrase_rejected = yes
8y6_helper_phrase_expectation_repaired = yes
8z9_combined_suite_import_isolation_repaired = yes
8z10_blocker_repaired_for_gate_purposes = yes
8z11_smoke_executed = yes
controlled_evidence_candidate_created = yes, controlled backend test path only
evidence_candidate_schema = sentigraph_controlled_evidence_candidate_v0_1
evidence_candidate_mode = backend_only_local_controlled_evidence_candidate
evidence_layer_write = no
production_evidence_item_created = no
actual_review_queue_runtime_used = no
production_review_queue_item_created = no
review_queue_candidate_created = no
evidence_layer_import_candidate_created = no
production_case_created = no
production_analysis_run_created = no
actual_analysis_execution_started = no
production_analysis_result_creation_authorized = no
production_analysis_result_created = no
downstream_route_c_auto_run = no
real_exchange_dir_read = no
real_package_dir_read = no
production_package_rows_parsed = no
collector_job_run = no
provider_job_run = no
source11_runtime_called = no
actual_final_summary_report_created = no
b_end_report_runtime_generated = no
sandbox_public_event_runtime_generated = no
export_download_public_delivery_created = no
route_changed = no
frontend_changed = no
runtime_changed = no
human_review_required = yes
no_automatic_trust_upgrade = yes
repaired_8z9_combined_suite_import_isolation_assertion = yes
repair_type = order_independent_no_new_import_or_call_guard
future_next_boundary_recommendation = batch docs/smoke for Evidence candidate -> Review Queue candidate -> Evidence Layer import candidate, candidate-only, not Evidence Layer write

## Summary

This batch repaired the controlled Evidence candidate helper phrase from the encoding-unsafe helper phrase to the canonical ASCII helper phrase:

`APPROVE_8W_10_CONTROLLED_EVIDENCE_CANDIDATE_IMPLEMENTATION`

The repair is limited to helper phrase authorization and focused backend tests. It does not add service behavior beyond the phrase repair, does not add a route/API/frontend, does not persist runtime state, and does not cross the Evidence Layer or production object boundary.

8Z-11 proves only that an 8Z-9-equivalent safe row-preview fixture plus the accepted batch phrase and repaired helper phrase can create a local controlled Evidence candidate object in a backend test path. It does not create Evidence Layer records, Review Queue candidates, production EvidenceItems, production cases, production analysis runs, actual analysis execution, production Analysis Results, Source 11 runtime, reports, Sandbox/public event runtime, export/download/public delivery runtime, collector jobs, provider jobs, schedulers, HTTP bridges, or webhooks.

## Repairs

- Repaired `backend/app/services/controlled_evidence_candidate.py` helper phrase to ASCII.
- Updated `backend/app/tests/test_controlled_evidence_candidate.py` so only the ASCII helper phrase is accepted.
- Added `backend/app/tests/test_8z_11_controlled_on_demand_collector_route_c_row_preview_to_evidence_candidate_smoke.py` for the controlled 8Z-11 smoke.
- Repaired the 8Z-9 combined-suite import-isolation assertion to snapshot `sys.modules`, guard `builtins.__import__` and `importlib.import_module`, and assert no new disallowed modules are imported during the 8Z-9 smoke operation.
- Updated `backend/app/tests/test_8y_6_controlled_row_preview_to_evidence_candidate_source_path_smoke.py` so 8Y-6 uses the repaired helper phrase and keeps old helper phrases as rejected negative-test inputs.

## 8Z-9 Isolation Repair Proof

The old global `sys.modules` absence assertion was order-dependent in combined pytest runs. The repaired test no longer requires already-imported modules to be absent. It proves that the 8Z-9 operation itself does not newly import disallowed helper modules and that false side-effect flags remain false.

No modules are removed from `sys.modules`, no cleanup hack was added, and no downstream Route C helper is called.

## Helper Phrase Repair Proof

The focused helper test proves:

- repaired ASCII helper phrase is accepted;
- missing helper phrase is rejected;
- wrong helper phrase is rejected;
- batch phrase alone is rejected at helper layer;
- old Chinese helper phrase is rejected;
- old mojibake helper phrase is rejected;
- old garbled helper phrase is rejected;
- rejected phrases block before Evidence candidate creation and file access.

## 8Y-6 Compatibility Proof

8Y-6 now uses the repaired helper phrase when it routes a controlled row preview into the controlled Evidence candidate helper. It also directly tests that missing, wrong, old Chinese, old mojibake, and old garbled helper phrases are rejected by the helper.

8Y-6 still preserves:

- no Evidence Layer write;
- no production EvidenceItem;
- no Review Queue runtime;
- no production case;
- no production analysis run;
- no actual analysis execution;
- no production Analysis Result;
- no route/API/frontend;
- no real exchange or package directory read;
- no production package row parsing;
- no raw rows, comments, identities, author names, or profile URLs.

## 8Z-11 Smoke Proof

The 8Z-11 focused smoke proves:

- batch outer phrase is required before helper call;
- repaired helper inner phrase is required at helper layer;
- helper inner phrase alone does not authorize the batch;
- old standalone 8Z-11 wording remains inactive;
- controlled Evidence candidate is created only inside controlled backend test path;
- candidate output remains local, candidate-only, review-only, and human-review-required;
- no downstream Route C auto-run occurs;
- all Evidence Layer, Review Queue, production object, report, Sandbox/public event, export/download/public delivery, collector/provider, Source 11, route/frontend/runtime, raw exposure, and readiness flags remain false.

## Validation

Helper repair tests:

`python -m pytest backend/app/tests/test_controlled_evidence_candidate.py -q`

Result: pass.

New 8Z-11 focused smoke:

`python -m pytest backend/app/tests/test_8z_11_controlled_on_demand_collector_route_c_row_preview_to_evidence_candidate_smoke.py -q`

Result: pass.

Upstream 8Z row-preview chain:

`python -m pytest backend/app/tests/test_8z_9_controlled_on_demand_collector_review_only_staging_to_route_c_row_preview_smoke.py backend/app/tests/test_8z_8b_controlled_no_real_row_route_c_row_preview_entry_adapter_smoke.py backend/app/tests/test_8z_7_controlled_on_demand_collector_request_result_correlation_to_review_only_staging_handoff_smoke.py -q`

Result: pass.

Existing Route C row-preview to Evidence candidate safety:

`python -m pytest backend/app/tests/test_8y_6_controlled_row_preview_to_evidence_candidate_source_path_smoke.py backend/app/tests/test_controlled_row_preview.py -q`

Result: pass.

Local/golden safety:

`python -m pytest backend/app/tests/test_local_exchange_reader.py backend/app/tests/test_analysis_request_golden_contracts.py -q`

Result: pass.

Touched service compile:

`python -m py_compile backend/app/services/controlled_evidence_candidate.py`

Result: pass.

## Boundary

This batch is not an Evidence Layer write, not a Review Queue candidate gate, not an Evidence Layer import candidate gate, not production EvidenceItem creation, not production case creation, not production analysis run creation, not actual analysis execution, not production Analysis Result creation, not Source 11 runtime, not FinalSummaryReport runtime, not B-end report runtime, not Sandbox/public event runtime, not export/download/public delivery runtime, not collector/provider execution, not a route/API/frontend change, and not a runtime persistence change.

Provider output and preview-derived candidates remain evidence inputs, not truth, not official verification, not causal proof, not prediction, and not a production score.
