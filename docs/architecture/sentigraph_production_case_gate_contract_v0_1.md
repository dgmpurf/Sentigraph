# Sentigraph Production Case Gate Contract v0.1

## Purpose

This contract defines the 8Y-15 production case gate boundary between a local controlled EvidenceItem write runtime result and a future controlled production case candidate smoke.

The contract is docs-only. It does not create a production case candidate, actual production case, production analysis_run, production Analysis Result, Source 11 output, FinalSummaryReport output, route/API/frontend, or delivery runtime.

## Gate Object

```json
{
  "schema": "sentigraph_production_case_gate_decision_v0_1",
  "phase": "8Y-15",
  "decision": "ready",
  "docs_only": true,
  "gate_only": true,
  "selected_next_boundary_option": "ready_for_8Y_16_controlled_evidenceitem_write_result_to_production_case_candidate_smoke",
  "source": {
    "source_phase": "8Y-14",
    "source_runtime_schema": "sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1",
    "source_candidate_set_schema": "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1",
    "source_scope": "controlled_backend_test_path_only",
    "human_review_required": true,
    "no_automatic_trust_upgrade": true,
    "warning_count": 1
  },
  "now_flags": {
    "helper_called": false,
    "production_case_candidate_created": false,
    "actual_production_case_created": false,
    "production_case_created": false,
    "production_analysis_run_created": false,
    "production_analysis_result_creation_authorized": false,
    "new_evidence_layer_write_performed": false,
    "evidence_import_service_called": false,
    "evidence_ingestion_service_called": false,
    "actual_review_queue_runtime_used": false,
    "production_review_queue_item_created": false,
    "source11_runtime_called": false,
    "actual_final_summary_report_created": false,
    "b_end_report_runtime_generated": false,
    "sandbox_public_event_runtime_generated": false,
    "export_download_public_delivery_created": false,
    "source_files_created": false,
    "docs_project_sources_created": false
  },
  "future_8y16": {
    "exact_approval_phrase_required": true,
    "exact_approval_phrase_active": false,
    "exact_approval_phrase": "APPROVE_8Y_16_CONTROLLED_EVIDENCEITEM_WRITE_RESULT_TO_PRODUCTION_CASE_CANDIDATE_SMOKE",
    "allowed_mode": "backend_only_local_controlled_candidate_smoke",
    "candidate_only": true
  }
}
```

## Field Meaning

- `schema`: Identifies this docs-only gate decision contract.
- `phase`: The current docs-only phase.
- `decision`: `ready` means a future controlled candidate smoke may be considered; it does not authorize execution now.
- `docs_only`: Must remain true for 8Y-15.
- `gate_only`: Must remain true for 8Y-15.
- `selected_next_boundary_option`: Names the next inactive boundary selected by this gate.
- `source`: Safe summary of the 8Y-14 controlled backend test-path source.
- `now_flags`: All side-effect flags for 8Y-15; every value must remain false.
- `future_8y16`: Inactive description of the future exact approval phrase and scope.

## Production Case Surface Classification

| Surface | Class | Relation | Side effects | Allowed in 8Y-15 |
| --- | --- | --- | --- | --- |
| `controlled_production_case_candidate.py` | backend_helper | production_case_candidate | no_persistence | inspect only |
| `test_controlled_production_case_candidate.py` | test_only | production_case_candidate | no_persistence | inspect only |
| `controlled_production_analysis_run_candidate.py` | backend_helper | production_analysis_run | no_persistence | inspect only |
| `test_controlled_production_analysis_run_candidate.py` | test_only | production_analysis_run | no_persistence | inspect only |
| `analysis_request_store.py` | backend_service | review_queue / analysis / report / delivery runtime | runtime_local_only or broader depending endpoint | inspect only |
| `evidence_import.py` | backend_service | Evidence import | unknown | inspect only |
| `evidence_ingestion.py` | backend_service | EvidenceItem / Review Queue normalization | unknown | inspect only |
| `schemas/evidence.py` | schema | EvidenceItem / Review Queue | no_persistence | inspect only |
| Production case / analysis / report / delivery architecture docs | docs_only | mixed | no_persistence | inspect only |

8Y-15 does not call any of these surfaces.

## Future 8Y-16 Input Contract

Future 8Y-16 may use only safe source summary values equivalent to:

- source_runtime_schema = sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1
- source_production_import_derived_write_candidate_schema = sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1
- controlled_evidenceitem_write_runtime_called = true in prior controlled backend test path only
- controlled_evidenceitem_write_result_created = true in prior controlled backend test path only
- production_case_created = false
- production_analysis_run_created = false
- production_analysis_result_creation_authorized = false
- evidence_import_service_called = false
- evidence_ingestion_service_called = false
- actual_review_queue_runtime_used = false
- production_review_queue_item_created = false
- source11_runtime_called = false
- actual_final_summary_report_created = false
- b_end_report_runtime_generated = false
- sandbox_public_event_runtime_generated = false
- export_download_public_delivery_created = false
- raw_rows_exposed = false
- raw_comments_exposed = false
- raw_identities_exposed = false
- author_names_or_profile_urls_exposed = false
- secrets_read = false
- human_review_required = true
- no_automatic_trust_upgrade = true
- warning_count = 1

## Future 8Y-16 Output Contract

Future 8Y-16 may output a candidate-only object inside a controlled backend test path if separately approved. Its output must preserve:

- production_case_candidate_created may be true only inside the controlled backend test path
- production_case_candidate_schema = sentigraph_controlled_production_case_candidate_v0_1 or safe equivalent
- production_case_candidate_only = true
- actual_production_case_created = false
- production_case_created = false unless the helper uses that field for local candidate semantics and the report qualifies it as not store/runtime
- production_analysis_run_created = false
- production_analysis_result_creation_authorized = false
- new_evidence_layer_write_performed = false
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

## Future 8Y-16 Inactive Approval Phrase

The inactive future phrase is:

`APPROVE_8Y_16_CONTROLLED_EVIDENCEITEM_WRITE_RESULT_TO_PRODUCTION_CASE_CANDIDATE_SMOKE`

It is recorded here only as a future requirement. It is not active in 8Y-15 and does not grant implementation authority.

## Stop Rules

Stop before future 8Y-16 if any of these are required:

- actual production case runtime/store creation
- production analysis_run
- production Analysis Result creation authorization
- Source 11 runtime
- actual FinalSummaryReport runtime
- route/API/frontend
- B-end/Sandbox/export/public/final-delivery runtime
- evidence_import.py / evidence_ingestion.py general production write service
- new Evidence Layer write beyond the 8Y-14 source object
- actual Review Queue runtime
- production Review Queue item
- raw row/comment/identity exposure
- author names/profile URLs as actual values
- arbitrary real exchange dir
- arbitrary package dir
- private collector source inspection
- collector job execution
- real API/LLM/network/fetch/scrape
- automatic trust upgrade
- customer/public/production readiness claims
- missing, unsafe, garbled, or non-explicit helper approval phrase

## Relationship To Later Gates

8Y-16, if separately approved, can only be a local controlled production case candidate smoke. Actual production case creation remains a later gate. Production analysis_run remains a later gate. Production Analysis Result creation remains a later and separate authorization chain. Route B Source 11 / FinalSummaryReport runtime remains deferred. Export/download/public/final-delivery remains deferred.

## Phrase Non-Transfer Rule

The 8Y-14 phrase, 8W-28 helper phrase, 8Y-13C phrase, 8Y-12 phrase, 8Y-10 phrase, 8Y-8 phrase, and 8Y-6 phrase do not authorize future 8Y-16 work.

Only the future 8Y-16 exact phrase can be considered for future 8Y-16, and this document records it as inactive only.
