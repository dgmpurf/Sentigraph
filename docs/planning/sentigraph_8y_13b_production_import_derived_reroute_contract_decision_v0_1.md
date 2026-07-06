# Sentigraph 8Y-13B Production-import-derived Reroute Contract Decision v0.1

## A. Decision

phase = 8Y-13B

decision = ready

privacy_issue_stop = no

docs_only = yes

contract_only = yes

backend_code_changed = no

tests_changed = no

route_changed = no

frontend_changed = no

runtime_changed = no

adapter_implemented = no

reroute_implemented = no

helper_called = no

production_evidence_import_candidate_created = no

production_import_candidate_created = no

production_import_derived_write_candidate_created = no

controlled_evidenceitem_write_runtime_called = no

actual_evidence_layer_write_used = no

evidence_layer_write = no

persisted_evidence_layer_record_created = no

production_evidence_item_created = no

production_case_created = no

production_analysis_run_created = no

evidence_import_service_called = no

evidence_ingestion_service_called = no

production_evidenceitem_write_runtime_used = no

actual_review_queue_runtime_used = no

production_review_queue_item_created = no

source11_runtime_called = no

actual_final_summary_report_created = no

b_end_report_runtime_generated = no

sandbox_public_event_runtime_generated = no

export_download_public_delivery_created = no

source_files_created = no

docs_project_sources_created = no

selected_compatibility_path = option_B_reroute_through_production_import_derived_path

selected_next_boundary_option = ready_for_8Y_13C_controlled_production_import_derived_reroute_smoke

future_8y13c_exact_approval_phrase_required = yes

future_8y13c_exact_approval_phrase_active = no

old_8y14_phrase_status = inactive_not_selected_pending_compatibility_path

source_update_recommended_after_commit = no

source11_update_recommended = no

recommended_tag = no

## B. 8Y-13A Decision Summary

8Y-13A confirmed the direct schema blocker:

- 8Y-12 direct write-candidate schema: `sentigraph_controlled_evidence_layer_write_candidate_set_v0_1`
- existing controlled EvidenceItem write runtime expected input: `sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1`

8Y-13A selected:

`option_B_reroute_through_production_import_derived_path`

8Y-13A rejected a direct-schema adapter for now because the existing 8W-22 / 8W-25 helper chain already carries a governed path into the runtime-expected schema.

8Y-13A did not implement an adapter, did not implement a reroute, did not call any helper or runtime, did not perform actual Evidence Layer write, and did not create production EvidenceItem, production case, or production `analysis_run`.

The old 8Y-14 phrase remains inactive and not selected pending compatibility path resolution:

`APPROVE_8Y_14_CONTROLLED_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_SMOKE`

## C. Exact Reroute Contract Shape

8Y-13B defines this contract shape only:

```text
8Y-12 direct write candidate
-> controlled production evidence import candidate boundary
-> production-import-derived write-candidate boundary
-> future controlled EvidenceItem write runtime expected input contract
```

Source object:

- source phase: 8Y-12
- source schema: `sentigraph_controlled_evidence_layer_write_candidate_set_v0_1`
- source mode: `backend_only_local_evidence_layer_write_candidate_boundary`
- source status: candidate-only, local-only, human-review-required, no automatic trust upgrade

Step 1:

- direct write candidate -> controlled production evidence import candidate boundary
- possible future helper surface: `backend/app/services/controlled_production_evidence_import_candidate.py`
- expected future output schema: `sentigraph_controlled_production_evidence_import_candidate_set_v0_1`
- expected future mode: `backend_only_local_production_evidence_import_candidate_boundary`
- allowed only if later separately approved

Step 2:

- controlled production evidence import candidate -> production-import-derived write-candidate boundary
- possible future helper surface: `backend/app/services/controlled_evidence_layer_write_candidate_from_production_import_candidate.py`
- expected future output schema: `sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1`
- expected future mode: `backend_only_local_evidence_layer_write_candidate_boundary`
- allowed only if later separately approved

Step 3:

- production-import-derived write candidate -> future controlled EvidenceItem write runtime expected input contract
- possible future runtime surface: `backend/app/services/controlled_evidenceitem_evidence_layer_write_runtime.py`
- runtime execution remains not approved in 8Y-13B

## D. Not Actual Production Import

In this contract, production-import-derived is a schema and governance boundary name only.

It must not be confused with general production import. It must not call `evidence_import.py` or `evidence_ingestion.py`. It must not persist Evidence Layer records. It must not create production EvidenceItem unless a later exact write smoke explicitly approves controlled backend test-path creation.

8Y-13B does not create production evidence import candidates and does not create production-import-derived write candidates.

## E. Allowed Future 8Y-13C Input

Future 8Y-13C may accept only the 8Y-12 local controlled direct write-candidate object or an equivalent safe summary.

Required input constraints:

- schema = `sentigraph_controlled_evidence_layer_write_candidate_set_v0_1` or safe equivalent
- actual_evidence_layer_write_used = false
- evidence_layer_write = false
- persisted_evidence_layer_record_created = false
- production_evidence_item_created = false
- production_case_created = false
- production_analysis_run_created = false
- evidence_import_service_called = false
- evidence_ingestion_service_called = false
- production_evidenceitem_write_runtime_used = false
- actual_review_queue_runtime_used = false
- production_review_queue_item_created = false
- raw_rows_exposed = false
- raw_comments_exposed = false
- raw_identities_exposed = false
- author_names_or_profile_urls_exposed = false
- secrets_read = false
- human_review_required = true
- no_automatic_trust_upgrade = true

## F. Allowed Future 8Y-13C Action

Future 8Y-13C may be:

- backend-only
- test-first
- controlled smoke only
- local-only
- candidate-only
- bounded to the source candidate count
- redacted
- warning-preserving
- human-review-required
- no automatic trust upgrade

Future 8Y-13C may use the existing `controlled_production_evidence_import_candidate` helper if safe and separately approved. It may use the existing `controlled_evidence_layer_write_candidate_from_production_import_candidate` helper if safe and separately approved.

Future 8Y-13C may create a local controlled production evidence import candidate boundary object only inside the controlled backend test path. It may create a local controlled production-import-derived write-candidate boundary object only inside the controlled backend test path.

Future 8Y-13C must not:

- call controlled EvidenceItem write runtime
- perform actual Evidence Layer write
- create a persisted Evidence Layer record
- create production EvidenceItem
- create production case
- create production `analysis_run`
- call `evidence_import.py`
- call `evidence_ingestion.py`
- use route/API/frontend
- call Source 11 runtime
- call actual FinalSummaryReport runtime

## G. Future 8Y-13C Exact Approval Phrase

Inactive future phrase:

`APPROVE_8Y_13C_CONTROLLED_PRODUCTION_IMPORT_DERIVED_REROUTE_SMOKE`

This phrase is inactive in 8Y-13B. It must not authorize implementation in 8Y-13B. It must not authorize actual Evidence Layer write, production EvidenceItem, production case, production `analysis_run`, controlled EvidenceItem write runtime, `evidence_import.py`, `evidence_ingestion.py`, Source 11 runtime, or FinalSummaryReport runtime.

## H. Future 8Y-13C Output Constraints

If later approved, future 8Y-13C may produce output with:

- production_evidence_import_candidate_created = true only inside controlled backend test path
- production_import_candidate_created = true only inside controlled backend test path
- production_import_candidate_schema = `sentigraph_controlled_production_evidence_import_candidate_set_v0_1` or safe equivalent
- production_import_candidate_mode = `backend_only_local_production_evidence_import_candidate_boundary` or safe equivalent
- production_import_derived_write_candidate_created = true only inside controlled backend test path
- production_import_derived_write_candidate_schema = `sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1` or safe equivalent
- write_candidate_from_production_import_candidate_mode = `backend_only_local_evidence_layer_write_candidate_boundary` or safe equivalent

Future 8Y-13C output must keep:

- controlled_evidenceitem_write_runtime_called = false
- production_evidenceitem_write_runtime_used = false
- actual_evidence_layer_write_used = false
- evidence_layer_write = false
- persisted_evidence_layer_record_created = false
- production_evidence_item_created = false
- production_case_created = false
- production_analysis_run_created = false
- evidence_import_service_called = false
- evidence_ingestion_service_called = false
- actual_review_queue_runtime_used = false
- production_review_queue_item_created = false
- source11_runtime_called = false
- actual_final_summary_report_created = false
- b_end_report_runtime_generated = false
- sandbox_public_event_runtime_generated = false
- export_download_public_delivery_created = false
- generated_response_text = false
- route_ready = false
- frontend_ready = false
- production_ready = false
- customer_ready = false
- public_ready = false
- raw_rows_exposed = false
- raw_comments_exposed = false
- raw_identities_exposed = false
- author_names_or_profile_urls_exposed = false
- secrets_read = false
- human_review_required = true
- no_automatic_trust_upgrade = true

## I. Relationship to Old 8Y-14

8Y-13C, if later approved, only resolves schema compatibility by producing the runtime-expected candidate schema.

It still does not call controlled EvidenceItem write runtime. It still does not perform actual write. It does not revive the old 8Y-14 phrase.

After 8Y-13C, a new docs-only gate must decide whether actual controlled EvidenceItem write smoke may be reconsidered.

Old phrase status:

`inactive_not_selected_pending_compatibility_path`

If the project later wants controlled write smoke, use a fresh docs-only gate and either reissue a new phrase or explicitly revalidate the old 8Y-14 phrase.

## J. Hard Blockers for Future 8Y-13C

Future 8Y-13C must stop if any of these are true:

- no safe controlled production evidence import candidate helper surface found
- no safe production-import-derived write candidate helper surface found
- helper approval phrase missing, unsafe, or encoding-invalid
- need actual Evidence Layer write
- need persisted Evidence Layer record
- need production EvidenceItem
- need production case
- need production `analysis_run`
- need controlled EvidenceItem write runtime call
- need `evidence_import.py` or `evidence_ingestion.py` production write service
- need route/API/frontend
- need Source 11 runtime
- need actual FinalSummaryReport runtime
- need B-end/Sandbox/export/public delivery
- need arbitrary real exchange directory
- need arbitrary package directory
- need private collector source inspection
- need collector job execution
- need raw row/comment/identity exposure
- need author names/profile URLs as actual values
- need real API/LLM/network/fetch/scrape
- need automatic trust upgrade
- need customer_ready, public_ready, production_ready, final_ready, export_ready, or source11_runtime_ready claims

## K. Relationship to Route C

8Y-13B keeps Route C alive but inserts a compatibility bridge before any write runtime can be reconsidered.

Actual Evidence Layer write remains a later gate. Production EvidenceItem remains a later gate. Production case remains a later gate. Production `analysis_run` remains a later gate. Production Analysis Result creation remains a later and separate authorization chain. Actual Source 11 / FinalSummaryReport runtime remains Route B and deferred.

## L. Next Recommendation

Next recommended task:

8Y-13C controlled production-import-derived reroute smoke.

That task must be backend-only, test-first, local-only, and controlled. It must not call controlled EvidenceItem write runtime or perform actual Evidence Layer write.
