# Sentigraph 8Y-13A Write Path Compatibility Decision v0.1

## A. Decision

phase = 8Y-13A

decision = ready

privacy_issue_stop = no

docs_only = yes

compatibility_decision_only = yes

backend_code_changed = no

tests_changed = no

route_changed = no

frontend_changed = no

runtime_changed = no

adapter_implemented = no

reroute_implemented = no

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

selected_next_boundary_option = ready_for_8Y_13B_production_import_derived_reroute_contract_docs_only

future_exact_approval_phrase_required = yes

future_exact_approval_phrase_active = no

old_8y14_phrase_status = inactive_not_selected_pending_compatibility_path

source_update_recommended_after_commit = no

source11_update_recommended = no

recommended_tag = no

## B. Route C State

8Y-5A selected Route C:

redacted row preview -> controlled evidence candidate -> review-only / review queue candidate -> Evidence Layer import candidate.

The current Route C checkpoints are:

- 8Y-6: controlled row preview -> controlled evidence candidate helper -> local controlled evidence candidate object
- 8Y-8: controlled evidence candidate object -> controlled review queue candidate helper -> local controlled review-only / review queue candidate object
- 8Y-10: controlled review queue candidate object -> controlled Evidence Layer import candidate helper -> local controlled Evidence Layer import candidate object
- 8Y-12: controlled Evidence Layer import candidate -> controlled Evidence Layer write-candidate helper -> local controlled Evidence Layer write-candidate object
- 8Y-13: blocked the actual Evidence Layer write / production EvidenceItem gate because the 8Y-12 direct write-candidate schema does not connect directly to the existing controlled EvidenceItem write runtime helper

8Y-13A is only a compatibility decision. Future write implementation remains inactive. Production case and production `analysis_run` remain separate later gates. Route B actual Source 11 / actual FinalSummaryReport runtime remains deferred.

## C. Compatibility Blocker

Route C 8Y-12 write candidate set schema:

`sentigraph_controlled_evidence_layer_write_candidate_set_v0_1`

Existing controlled EvidenceItem write runtime expected input:

`sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1`

These are not interchangeable. The 8Y-14 phrase carried from 8Y-13 remains inactive and not selected until a compatibility path is resolved:

`APPROVE_8Y_14_CONTROLLED_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_SMOKE`

## D. Relevant Surface Inventory

| Surface | Type | Relation | Side-effect classification | Notes |
| --- | --- | --- | --- | --- |
| `backend/app/services/controlled_evidence_layer_write_candidate.py` | backend_helper | route_c_write_candidate | no_persistence | Produces the direct 8Y-12 style write-candidate set. |
| `backend/app/tests/test_controlled_evidence_layer_write_candidate.py` | test_only | route_c_write_candidate | no_persistence | Verifies direct candidate-only behavior. |
| `backend/app/tests/test_8y_12_controlled_evidence_layer_import_candidate_to_write_candidate_smoke.py` | test_only | route_c_write_candidate | no_persistence | Proves Route C reaches the direct write-candidate object without write side effects. |
| `docs/health/sentigraph_8y_12_controlled_evidence_layer_import_candidate_to_write_candidate_smoke_report_v0_1.md` | docs_only | route_c_write_candidate | no_persistence | Records the 8Y-12 smoke result. |
| `backend/app/services/controlled_production_evidence_import_candidate.py` | backend_helper | production_import_derived_write_candidate upstream | no_persistence | Accepts the direct write-candidate set and creates a controlled production-evidence-import-candidate-shaped object. |
| `backend/app/tests/test_controlled_production_evidence_import_candidate.py` | test_only | production_import_derived_write_candidate upstream | no_persistence | Verifies 8W-22 controlled candidate behavior. |
| `backend/app/services/controlled_evidence_layer_write_candidate_from_production_import_candidate.py` | backend_helper | production_import_derived_write_candidate | no_persistence | Produces the schema expected by the existing controlled EvidenceItem write runtime helper. |
| `backend/app/tests/test_controlled_evidence_layer_write_candidate_from_production_import_candidate.py` | test_only | production_import_derived_write_candidate | no_persistence | Verifies 8W-25 derived write-candidate behavior. |
| `backend/app/services/controlled_evidenceitem_evidence_layer_write_runtime.py` | runtime_helper | controlled_evidenceitem_write_runtime | runtime_local_only | Existing 8W-28 helper expects the 8W-25 derived write-candidate set. |
| `backend/app/tests/test_controlled_evidenceitem_evidence_layer_write_runtime.py` | test_only | controlled_evidenceitem_write_runtime | runtime_local_only | Verifies controlled runtime behavior for the 8W-25 input contract. |
| `backend/app/services/evidence_import.py` | backend_service | actual_production_write_service | actual_Evidence_Layer_write_possible | Must not be called by 8Y-13A or 8Y-13B. |
| `backend/app/services/evidence_ingestion.py` | backend_service | actual_production_write_service | actual_Evidence_Layer_write_possible | Must not be called by 8Y-13A or 8Y-13B. |
| `backend/app/schemas/evidence.py` | backend_schema | unknown | unknown | Contains EvidenceItem and import/ingestion models; schema presence is not write authorization. |
| `backend/app/services/controlled_production_case_candidate.py` | backend_helper | production_case | no_persistence | Downstream and out of scope. |
| `backend/app/services/controlled_production_analysis_run_candidate.py` | backend_helper | production_analysis_run | no_persistence | Downstream and out of scope. |
| `backend/app/services/analysis_request_store.py` | backend_service | production_case / production_analysis_run / report chain | runtime_local_only when called | Downstream runtime store, out of scope. |

## E. Option A: Direct-schema Adapter

Option A would define:

8Y Route C write candidate -> direct compatibility adapter contract -> controlled EvidenceItem write runtime expected input.

Benefits:

- preserves Route C without detouring through production-import-derived naming
- can remain adapter-only and candidate-derived if tightly scoped
- may be easier to explain as a direct continuation of 8Y-12

Risks:

- would create a new adapter shape that duplicates parts of 8W-22 / 8W-25 governance
- could bypass the existing production-import-derived candidate checks unless the adapter reproduces them
- could blur whether the source has passed the same governance expected by the 8W-28 helper
- would need a docs-only adapter contract before any implementation

Option A is not selected because existing code already contains a governed path that converts direct write candidates into the schema expected by the controlled EvidenceItem write runtime helper.

## F. Option B: Reroute Through 8W-25 / Production-import-derived Path

Option B would define:

Route C write candidate -> controlled production evidence import candidate -> production-import-derived write candidate -> existing controlled EvidenceItem write runtime expected input.

Benefits:

- matches the existing controlled EvidenceItem write runtime input contract
- reuses existing 8W-22 and 8W-25 helper boundaries instead of inventing a parallel adapter
- preserves warning/manual-review/no-trust-upgrade fields through existing checks
- keeps any future write runtime discussion aligned with the already documented 8W production evidence write gate chain

Risks:

- introduces production-import-derived semantics earlier in the Route C continuation
- may confuse candidate-shaped governance objects with actual production import if wording is careless
- still requires a docs-only reroute contract before any future write smoke
- still must not call `evidence_import.py`, `evidence_ingestion.py`, or the controlled EvidenceItem write runtime in 8Y-13B

Option B is selected only as a docs-only reroute contract direction. It does not implement rerouting and does not authorize actual Evidence Layer write.

## G. Option C: Continue Pause

Option C would keep Route C paused because compatibility remains unresolved.

Choose Option C if:

- the existing production-import-derived path cannot be safely tied back to Route C
- the reroute would require actual production import services
- a future contract cannot keep all side effects false
- a direct adapter would be safer but not yet designed

Option C is not selected because the existing helper surfaces show a controlled, no-persistence path from the direct write-candidate set into the runtime-expected schema through 8W-22 and 8W-25.

## H. Selected Compatibility Path

selected_compatibility_path = option_B_reroute_through_production_import_derived_path

This selection means the next step should be a docs-only reroute contract that explicitly maps:

1. 8Y-12 direct write-candidate source
2. controlled production evidence import candidate boundary
3. production-import-derived write-candidate boundary
4. future controlled EvidenceItem write runtime input expectations

It must not implement the reroute.

## I. Selected Next Boundary

selected_next_boundary_option = ready_for_8Y_13B_production_import_derived_reroute_contract_docs_only

Future 8Y-13B may only create a docs-only contract. It must not implement an adapter, reroute, write runtime, actual Evidence Layer write, production EvidenceItem, production case, production `analysis_run`, Source 11 runtime, or FinalSummaryReport runtime.

## J. Future Approval Phrase Status

Inactive future phrase for the selected 8Y-13B docs-only contract:

`APPROVE_8Y_13B_PRODUCTION_IMPORT_DERIVED_REROUTE_CONTRACT_DOCS_ONLY`

future_exact_approval_phrase_required = yes

future_exact_approval_phrase_active = no

This phrase is inactive in 8Y-13A. It does not authorize implementation, adapter creation, reroute implementation, actual Evidence Layer write, production EvidenceItem creation, production case creation, production `analysis_run` creation, Source 11 runtime, FinalSummaryReport runtime, B-end/Sandbox/export/public delivery, route/API/frontend behavior, real APIs, real LLMs, provider jobs, collector jobs, URL fetching, or scraping.

Old 8Y-14 phrase status:

old_8y14_phrase_status = inactive_not_selected_pending_compatibility_path

`APPROVE_8Y_14_CONTROLLED_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_SMOKE`

The old phrase must not authorize any work until the compatibility path is resolved by a later docs-only gate.

## K. Hard Blockers for Future Compatibility Work

Future compatibility work must stop if it needs:

- actual Evidence Layer write
- persisted Evidence Layer record
- production EvidenceItem
- production case
- production `analysis_run`
- `evidence_import.py` or `evidence_ingestion.py` production write service
- arbitrary real exchange directory
- arbitrary package directory
- private collector source inspection
- collector job execution
- raw row/comment/identity exposure
- author names/profile URLs as actual values
- route/API/frontend behavior
- Source 11 runtime
- actual FinalSummaryReport runtime
- B-end/Sandbox/export/public delivery
- automatic trust upgrade
- customer_ready, public_ready, production_ready, final_ready, export_ready, or source11_runtime_ready claims

## L. Relationship to Route C

8Y-13A does not end Route C. It chooses the write-path compatibility strategy for the next docs-only boundary.

Actual Evidence Layer write remains a later gate. Production case remains a later gate. Production `analysis_run` remains a later gate. Production Analysis Result creation remains a separate later authorization chain. Source 11 / FinalSummaryReport runtime remains Route B and deferred.

## M. Next Recommendation

Next recommended task:

8Y-13B production-import-derived reroute contract docs-only.

That task should define the allowed source object, transformation sequence, exact schema handoff, stop rules, and validation expectations. It should not implement rerouting or call any runtime helper.
