# Sentigraph 8Y-14 Controlled EvidenceItem Write Runtime Smoke After Reroute and Phrase Repair Report v0.1

## A. Decision

phase = 8Y-14

decision = ready

privacy_issue_stop = no

backend_only = yes

test_first = yes

controlled_smoke = yes

source_path_step = production_import_derived_write_candidate_to_controlled_evidenceitem_write_runtime

outer_8y14_phrase = `APPROVE_8Y_14_CONTROLLED_EVIDENCEITEM_WRITE_RUNTIME_SMOKE_AFTER_REROUTE_AND_PHRASE_REPAIR`

repaired_helper_phrase = `APPROVE_8W_28_CONTROLLED_EVIDENCEITEM_EVIDENCE_LAYER_WRITE_RUNTIME_IMPLEMENTATION`

controlled_evidenceitem_write_runtime_called = yes, controlled backend test path only

production_evidenceitem_write_runtime_used = yes, controlled backend test path only

controlled_evidenceitem_write_result_created = yes, controlled backend test path only

evidence_write_result_schema = `sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1`

write_result_schema = `sentigraph_controlled_evidence_layer_write_result_v0_1`

evidence_write_mode = controlled_backend_only_evidence_layer_write_runtime

source_production_import_derived_write_candidate_schema = `sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1`

actual_evidence_layer_write_used = yes, controlled local helper test-path semantics only

evidence_layer_write = yes, controlled local helper test-path semantics only

production_evidence_item_created = no

persisted_evidence_layer_record_created = no

evidence_import_service_called = no

evidence_ingestion_service_called = no

general_production_import_service_called = no

production_case_created = no

production_analysis_run_created = no

production_analysis_result_creation_authorized = no

actual_review_queue_runtime_used = no

production_review_queue_item_created = no

source11_runtime_called = no

actual_final_summary_report_created = no

b_end_report_runtime_generated = no

sandbox_public_event_runtime_generated = no

export_download_public_delivery_created = no

generated_response_text = no

route_changed = no

frontend_changed = no

runtime_changed = controlled_backend_test_path_only

raw_rows_exposed = no

raw_comments_exposed = no

raw_identities_exposed = no

author_names_or_profile_urls_exposed = no

secrets_read = no

human_review_required = yes

no_automatic_trust_upgrade = yes

warning_count = 1

old_8y14_phrase_accepted = no

older_after_reroute_8y14_phrase_accepted = no

repaired_helper_phrase_required = yes

helper_phrase_alone_authorizes_8y14 = no

future_next_boundary_recommendation = production case gate docs-only, not implementation

recommended_tag = no

## B. What Was Implemented

8Y-14 added a focused backend-only test-path smoke in:

`backend/app/tests/test_8y_14_controlled_evidenceitem_write_runtime_smoke_after_reroute_and_phrase_repair.py`

The smoke proves this controlled path:

```text
8Y-13C-equivalent local production-import-derived write candidate
-> existing 8W-28 controlled EvidenceItem write runtime helper
-> local controlled EvidenceItem-shaped runtime result
```

The input is an in-memory 8Y-13C-equivalent fixture with the runtime-expected schema. It does not re-read package rows, `evidence_items.csv`, `evidence_items.jsonl`, `source_manifest`, `collection_log`, private collector output, or real exchange directories.

The only service code change is a safety-only extension to the existing controlled write runtime top-level source blocker table in:

`backend/app/services/controlled_evidenceitem_evidence_layer_write_runtime.py`

The extension blocks unsafe source candidate set flags such as raw exposure, general import/ingestion service usage, Source 11 runtime, FinalSummaryReport runtime, route/frontend/export/public-delivery flags, and related side-effect flags if they are true before the helper proceeds.

## C. Test-first Evidence

The new 8Y-14 test was run before the safety-only service patch.

Initial RED result:

- The first draft showed that blocking all file opening also blocked reused upstream row-preview fixture construction. The test was corrected to use an in-memory 8Y-13C-equivalent source object.
- The corrected RED result showed eight expected helper safety gaps: top-level raw exposure flags, general import/ingestion flags, Source 11 runtime flag, and FinalSummaryReport runtime flag were not yet blocked by the controlled write helper.

Minimal GREEN change:

- Expanded the existing `TOP_LEVEL_FALSE_FIELDS` blocker table in the controlled EvidenceItem write runtime helper.
- No route/API/frontend/runtime persistence was added.
- No broad backend service change was made.

## D. Controlled Runtime Proof

The ready-path smoke asserts:

- outer 8Y-14 phrase is required before any controlled write helper call
- repaired 8W-28 helper phrase is ASCII and required by the helper layer
- controlled EvidenceItem write runtime helper is called only in the backend test path
- runtime schema is `sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1`
- source schema is `sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1`
- controlled EvidenceItem-shaped output is created only as local controlled test-path output
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`
- `warning_count = 1`

## E. Approval Phrase Safety Proof

The smoke asserts:

- missing outer 8Y-14 phrase blocks before controlled write runtime call
- wrong outer 8Y-14 phrase blocks before controlled write runtime call
- old direct 8Y-14 phrase blocks
- older after-reroute 8Y-14 phrase blocks
- 8Y-13C phrase alone blocks
- 8Y-12 / 8Y-10 / 8Y-8 / 8Y-6 phrases alone block
- repaired 8W-28 helper phrase alone blocks as outer 8Y-14 approval
- missing repaired 8W-28 helper phrase blocks at helper layer
- old Chinese and mojibake helper phrases block at helper layer

## F. Production Side-effect Proof

The smoke asserts all of these remain false:

- evidence_import_service_called
- evidence_ingestion_service_called
- general_production_import_service_called
- production_case_created
- production_analysis_run_created
- production_analysis_result_creation_authorized
- actual_review_queue_runtime_used
- production_review_queue_item_created
- source11_runtime_called
- actual_final_summary_report_created
- b_end_report_runtime_generated
- sandbox_public_event_runtime_generated
- export_download_public_delivery_created
- generated_response_text
- route_changed
- frontend_changed
- route_ready
- frontend_ready
- production_ready
- customer_ready
- public_ready
- raw_rows_exposed
- raw_comments_exposed
- raw_identities_exposed
- raw_author_ids_emitted
- raw_author_names_emitted
- profile_urls_emitted
- author_names_or_profile_urls_exposed
- secrets_read

The existing helper's `evidence_layer_write = true` remains qualified as controlled local helper test-path semantics only. It does not mean production storage.

## G. Validation

Focused 8Y-14 smoke:

```text
python -m pytest backend/app/tests/test_8y_14_controlled_evidenceitem_write_runtime_smoke_after_reroute_and_phrase_repair.py -q
```

Result: pass.

Existing controlled EvidenceItem write runtime tests:

```text
python -m pytest backend/app/tests/test_controlled_evidenceitem_evidence_layer_write_runtime.py -q
```

Result: pass.

Upstream reroute / production-import-derived tests:

```text
python -m pytest backend/app/tests/test_8y_13c_controlled_production_import_derived_reroute_smoke.py backend/app/tests/test_controlled_evidence_layer_write_candidate_from_production_import_candidate.py backend/app/tests/test_controlled_production_evidence_import_candidate.py -q
```

Result: pass.

Upstream safety chain:

```text
python -m pytest backend/app/tests/test_8y_12_controlled_evidence_layer_import_candidate_to_write_candidate_smoke.py backend/app/tests/test_controlled_evidence_layer_write_candidate.py backend/app/tests/test_8y_10_controlled_review_queue_candidate_to_evidence_layer_import_candidate_smoke.py backend/app/tests/test_controlled_evidence_layer_import_candidate.py backend/app/tests/test_8y_8_controlled_evidence_candidate_to_review_queue_candidate_smoke.py backend/app/tests/test_controlled_review_queue_candidate.py backend/app/tests/test_8y_6_controlled_row_preview_to_evidence_candidate_source_path_smoke.py backend/app/tests/test_controlled_evidence_candidate.py backend/app/tests/test_controlled_row_preview.py backend/app/tests/test_analysis_request_golden_contracts.py -q
```

Result: pass.

## H. Not Run

Full pytest was not run because 8Y-14 requested focused tests only.

Frontend build was not run because there were no frontend changes.

Browser smoke was not run because there were no route/API/frontend changes.

Collector jobs, real APIs, real LLMs, URL fetching, scraping, private collector inspection, real exchange dir reads, and row parsing were not run.

## I. Safety Confirmations

No route/API added.

No frontend changed.

No general production import service called.

No evidence ingestion service called.

No production case created.

No production analysis_run created.

No production Analysis Result creation authorized.

No Review Queue runtime used.

No Source 11 runtime called.

No actual FinalSummaryReport runtime created.

No B-end report runtime generated.

No Sandbox/public event runtime generated.

No export/download/public/final-delivery runtime created.

No private collector inspected.

No collector job run.

No arbitrary real exchange dir read.

No arbitrary real package dir read.

No `evidence_items.csv` read.

No `evidence_items.jsonl` read by the 8Y-14 smoke.

No `source_manifest` rows parsed.

No `collection_log` rows parsed.

No raw rows/comments/identities exposed.

No actual author names/profile URLs exposed.

No secrets read or printed.

No real APIs called.

No real LLMs called.

No URL fetching.

No scraping.

No Project Source files created.

No `docs/project_sources` files created.

No GitHub Actions modified.

## J. Next Recommendation

Next recommended task:

Production case gate docs-only decision, not implementation.
