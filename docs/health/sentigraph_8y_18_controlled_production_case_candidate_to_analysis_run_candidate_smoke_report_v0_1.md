# Sentigraph 8Y-18 Controlled Production Case Candidate to Analysis Run Candidate Smoke Report v0.1

## Status Fields

- phase = 8Y-18
- decision = ready
- privacy_issue_stop = no
- backend_only = yes
- test_first = yes
- controlled_smoke = yes
- source_path_step = production_case_candidate_to_production_analysis_run_candidate
- outer_8y18_phrase = APPROVE_8Y_18_CONTROLLED_PRODUCTION_CASE_CANDIDATE_TO_ANALYSIS_RUN_CANDIDATE_SMOKE
- production_analysis_run_candidate_created = yes, controlled backend test path only
- production_analysis_run_candidate_schema = sentigraph_controlled_production_analysis_run_candidate_v0_1
- production_analysis_run_candidate_mode = backend_only_local_production_analysis_run_candidate_boundary
- source_production_case_candidate_schema = sentigraph_controlled_production_case_candidate_v0_1
- source_evidence_write_result_schema = sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1
- actual_production_analysis_run_created = no
- production_analysis_run_runtime_used = no
- production_analysis_run_store_record_created = no
- production_analysis_run_created = no
- actual_analysis_execution_started = no
- analysis_execution_started = no
- production_analysis_result_creation_authorized = no
- production_analysis_result_created = no
- actual_production_case_created = no
- production_case_runtime_used = no
- production_case_store_record_created = no
- new_evidence_layer_write_performed = no
- evidence_import_service_called = no
- evidence_ingestion_service_called = no
- actual_review_queue_runtime_used = no
- production_review_queue_item_created = no
- source11_runtime_called = no
- actual_final_summary_report_created = no
- b_end_report_runtime_generated = no
- sandbox_public_event_runtime_generated = no
- export_download_public_delivery_created = no
- generated_response_text = no
- route_changed = no
- frontend_changed = no
- runtime_changed = no except controlled backend test path candidate object
- raw_rows_exposed = no
- raw_comments_exposed = no
- raw_identities_exposed = no
- author_names_or_profile_urls_exposed = no
- secrets_read = no
- human_review_required = yes
- no_automatic_trust_upgrade = yes
- warning_count = 1
- future_next_boundary_recommendation = production Analysis Result / actual analysis execution gate docs-only, not implementation

## What Was Proven

The focused 8Y-18 smoke created a local controlled production analysis_run candidate object inside the backend test path only:

1. Build a safe 8Y-16-equivalent controlled production case candidate smoke source.
2. Require the exact 8Y-18 outer phrase before any analysis-run-candidate helper call.
3. Normalize only missing false boundary flags required by the existing helper contract.
4. Feed the safe production case candidate set to the existing controlled production analysis_run candidate helper.
5. Confirm the output is candidate-only, local-only, backend-only, warning-preserving, and human-review-required.

The existing helper phrase remains the 8W-34 helper phrase and was used only inside the controlled backend test path. It was not broadened, weakened, or replaced.

## Approval Phrase Safety Proof

The new smoke test proves:

- missing 8Y-18 phrase blocks before production analysis_run candidate helper call
- wrong 8Y-18 phrase blocks before production analysis_run candidate helper call
- 8Y-16 phrase alone blocks
- 8Y-14 phrase alone blocks
- 8W-28 helper phrase alone blocks
- 8Y-13C / 8Y-12 / 8Y-10 / 8Y-8 / 8Y-6 phrases alone block
- row preview helper phrase alone blocks
- existing production analysis_run candidate helper phrase is ASCII
- mojibake production analysis_run candidate helper phrase is rejected by the existing helper

## Source Safety Proof

The smoke test blocks unsafe source mutations before production analysis_run candidate helper call, including:

- wrong source production case candidate schema
- actual production case flags
- production case runtime/store flags
- actual production analysis_run flags
- production analysis_run flag
- actual analysis execution flag
- production Analysis Result authorization flag
- production Analysis Result creation flag
- evidence import / evidence ingestion service flags
- Review Queue runtime / production Review Queue item flags
- Source 11 / FinalSummaryReport flags
- B-end report / Sandbox public event / export download public delivery flags
- raw rows/comments/identities flags
- author-name/profile-url exposure flag
- no_automatic_trust_upgrade = false

## No-Call Boundary

The smoke test monkeypatches identifiable forbidden entrypoints so the test fails if it calls:

- evidence import helpers
- evidence ingestion helpers
- production case candidate helper after the safe 8Y-16 source object has already been obtained
- Review Queue creation / action / completion store helpers
- manual analysis execution / result candidate store helpers
- analysis result boundary store helper
- summary report / FinalSummaryReport store helpers
- export / download / public delivery store helpers
- file open operations

The allowed production analysis_run candidate helper is the only analysis-run-candidate surface used, and it is used only in the controlled backend test path.

## Validation

- `python -m pytest backend/app/tests/test_8y_18_controlled_production_case_candidate_to_analysis_run_candidate_smoke.py -q` = pass
- `python -m pytest backend/app/tests/test_controlled_production_analysis_run_candidate.py -q` = pass
- `python -m pytest backend/app/tests/test_8y_16_controlled_evidenceitem_write_result_to_production_case_candidate_smoke.py backend/app/tests/test_controlled_production_case_candidate.py backend/app/tests/test_8y_14_controlled_evidenceitem_write_runtime_smoke_after_reroute_and_phrase_repair.py backend/app/tests/test_controlled_evidenceitem_evidence_layer_write_runtime.py -q` = pass
- `python -m pytest backend/app/tests/test_8y_13c_controlled_production_import_derived_reroute_smoke.py backend/app/tests/test_controlled_evidence_layer_write_candidate_from_production_import_candidate.py backend/app/tests/test_controlled_production_evidence_import_candidate.py backend/app/tests/test_analysis_request_golden_contracts.py -q` = pass

No service file was changed, so touched-service py_compile was not required.

## Not Run

- full pytest: not required for this focused controlled smoke
- frontend build: no frontend changes
- browser smoke: no route/API/frontend changes
- collector jobs: forbidden
- real API / real LLM / network / URL fetch / scraping: forbidden

## Safety Confirmations

- no actual production analysis_run runtime/store record created
- no actual analysis execution started
- no production Analysis Result creation authorized
- no production Analysis Result created
- no actual production case runtime/store record created
- no actual Review Queue runtime used
- no production Review Queue item created
- no Source 11 runtime called
- no actual FinalSummaryReport runtime output created
- no B-end report runtime created
- no Sandbox/public event runtime created
- no export/download/public/final-delivery runtime created
- no backend route/API added
- no frontend added
- no runtime persistence added outside controlled test path object
- no evidence_import.py or evidence_ingestion.py general production write service called
- no private collector source inspected
- no collector jobs run
- no arbitrary real exchange directories read
- no arbitrary real package directories read
- no evidence_items.csv read
- no evidence_items.jsonl parsed anew
- no source_manifest rows parsed
- no collection_log rows parsed
- no raw rows/comments/identities exposed
- no actual author names/profile URLs exposed
- no cookies, sessions, tokens, browser profiles, secrets, private paths, or .env values read or printed
- no real APIs called
- no real LLMs called
- no URL fetching
- no scraping
- no Project Source files created
- no docs/project_sources created
- no GitHub Actions changes
