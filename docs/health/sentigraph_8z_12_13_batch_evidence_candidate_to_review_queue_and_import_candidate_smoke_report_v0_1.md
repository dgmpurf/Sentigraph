# Sentigraph 8Z-12/13 Batch Evidence Candidate to Review Queue and Import Candidate Smoke Report v0.1

## Decision

- phase = 8Z-12/13
- decision = ready
- privacy_issue_stop = no
- batch_prompt = yes
- batch_phrase = APPROVE_8Z_12_13_BATCH_EVIDENCE_CANDIDATE_TO_REVIEW_QUEUE_AND_IMPORT_CANDIDATE_SMOKE
- review_queue_helper_phrase_repair_needed = yes
- review_queue_helper_phrase_repair_performed = yes
- review_queue_helper_phrase = APPROVE_8W_13_CONTROLLED_REVIEW_QUEUE_CANDIDATE_IMPLEMENTATION
- evidence_layer_import_helper_phrase_repair_needed = yes
- evidence_layer_import_helper_phrase_repair_performed = yes
- evidence_layer_import_helper_phrase = APPROVE_8W_16_CONTROLLED_EVIDENCE_LAYER_IMPORT_CANDIDATE_IMPLEMENTATION
- old_chinese_or_mojibake_helper_phrases_rejected = yes

## Scope

This batch is backend-only, local-only, candidate-only, test-path-only controlled smoke work.

It verifies the narrow candidate transition:

1. controlled Evidence candidate
2. controlled Review Queue candidate helper
3. controlled Evidence Layer import candidate helper

It does not authorize or perform Review Queue runtime, Evidence Layer write, production EvidenceItem creation, production case creation, production analysis_run creation, actual analysis execution, production Analysis Result creation, route/API/frontend work, collector/provider work, Source 11 runtime, FinalSummaryReport runtime, B-end/Sandbox/public-event generation, export/download/public delivery, or real package-row access.

## Helper Phrase Audit

The active helper phrases in:

- backend/app/services/controlled_review_queue_candidate.py
- backend/app/services/controlled_evidence_layer_import_candidate.py

were repaired from encoding-unsafe non-ASCII approval phrases to ASCII canonical helper phrases.

Focused helper tests now prove:

- canonical ASCII helper phrase is accepted.
- missing helper phrase is rejected.
- wrong helper phrase is rejected.
- old Chinese helper phrase is rejected.
- old mojibake/garbled helper phrase is rejected.
- rejected phrase blocks before candidate creation and file access.

## 8Z-12 Review Queue Candidate Smoke

- 8z12_review_queue_candidate_smoke_executed = yes
- controlled_review_queue_candidate_created = yes
- review_queue_candidate_schema = sentigraph_controlled_review_queue_candidate_v0_1
- review_queue_candidate_mode = backend_only_local_review_queue_candidate_boundary
- review_queue_helper_inner_phrase_required = yes
- helper_inner_phrase_alone_authorizes_batch = no
- actual_review_queue_runtime_used = no
- production_review_queue_item_created = no

## 8Z-13 Evidence Layer Import Candidate Smoke

- 8z13_evidence_layer_import_candidate_smoke_executed = yes
- controlled_evidence_layer_import_candidate_created = yes
- evidence_layer_import_candidate_schema = sentigraph_controlled_evidence_layer_import_candidate_v0_1
- evidence_layer_import_candidate_mode = backend_only_local_evidence_layer_import_candidate_boundary
- evidence_layer_import_helper_inner_phrase_required = yes
- evidence_layer_write = no
- evidence_layer_write_candidate_created = no
- production_evidence_item_created = no

## Required False Side Effects

- actual_review_queue_runtime_used = no
- production_review_queue_item_created = no
- evidence_layer_write = no
- evidence_layer_write_candidate_created = no
- production_evidence_item_created = no
- production_case_created = no
- production_analysis_run_created = no
- actual_analysis_execution_started = no
- production_analysis_result_creation_authorized = no
- production_analysis_result_created = no
- downstream_route_c_auto_run = no
- package_resolver_called = no
- provider_result_reader_called = no
- local_exchange_reader_called = no
- review_only_staging_helper_called = no
- collector_job_run = no
- provider_job_run = no
- scheduler_created = no
- http_bridge_created = no
- webhook_created = no
- private_collector_source_inspected = no
- real_exchange_dir_read = no
- real_package_dir_read = no
- production_package_rows_parsed = no
- original_package_rows_read = no
- raw_rows_exposed = no
- raw_comments_exposed = no
- raw_identities_exposed = no
- author_names_or_profile_urls_exposed = no
- secrets_read = no
- source11_runtime_called = no
- actual_final_summary_report_created = no
- b_end_report_runtime_generated = no
- sandbox_public_event_runtime_generated = no
- export_download_public_delivery_created = no
- route_changed = no
- frontend_changed = no
- runtime_changed = no
- route_ready = no
- frontend_ready = no
- production_ready = no
- customer_ready = no
- public_ready = no
- human_review_required = yes
- no_automatic_trust_upgrade = yes

## Validation Evidence

The following focused validation commands are required for this batch:

- python -m pytest backend/app/tests/test_controlled_review_queue_candidate.py backend/app/tests/test_controlled_evidence_layer_import_candidate.py -q
- python -m pytest backend/app/tests/test_8z_12_13_batch_evidence_candidate_to_review_queue_and_import_candidate_smoke.py -q
- python -m pytest backend/app/tests/test_8z_11_controlled_on_demand_collector_route_c_row_preview_to_evidence_candidate_smoke.py backend/app/tests/test_controlled_evidence_candidate.py -q
- python -m pytest backend/app/tests/test_8y_8_controlled_evidence_candidate_to_review_queue_candidate_smoke.py backend/app/tests/test_8y_10_controlled_review_queue_candidate_to_evidence_layer_import_candidate_smoke.py -q
- python -m pytest backend/app/tests/test_8z_9_controlled_on_demand_collector_review_only_staging_to_route_c_row_preview_smoke.py backend/app/tests/test_8z_8b_controlled_no_real_row_route_c_row_preview_entry_adapter_smoke.py -q
- python -m pytest backend/app/tests/test_local_exchange_reader.py backend/app/tests/test_analysis_request_golden_contracts.py -q
- python -m py_compile backend/app/services/controlled_review_queue_candidate.py backend/app/services/controlled_evidence_layer_import_candidate.py
- git diff --check

## Next Boundary Recommendation

future_next_boundary_recommendation = batch docs/smoke for Evidence Layer import candidate to write-candidate boundary, still not actual Evidence Layer write.

Inactive future batch idea only:

- APPROVE_8Z_14_15_BATCH_IMPORT_CANDIDATE_TO_WRITE_CANDIDATE_BOUNDARY_SMOKE

This future phrase is inactive and does not authorize anything in 8Z-12/13.
