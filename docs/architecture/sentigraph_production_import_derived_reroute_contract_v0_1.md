# Sentigraph Production-import-derived Reroute Contract v0.1

## A. Purpose

This contract defines the selected 8Y-13B production-import-derived reroute path from the 8Y-12 direct write-candidate object toward the schema expected by the controlled EvidenceItem write runtime helper.

This is contract-only. It does not implement the reroute, call helpers, create candidates, call runtime, or write Evidence Layer records.

## B. Source and Target Schemas

Source schema from 8Y-12:

```text
sentigraph_controlled_evidence_layer_write_candidate_set_v0_1
```

Intermediate schema from the controlled production evidence import candidate boundary:

```text
sentigraph_controlled_production_evidence_import_candidate_set_v0_1
```

Target candidate schema expected by the controlled EvidenceItem write runtime helper:

```text
sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1
```

The contract resolves the 8Y-13 direct schema mismatch by requiring a governed intermediate path before any later write runtime discussion.

## C. Reroute Contract Object

```json
{
  "phase": "8Y-13B",
  "decision": "ready",
  "docs_only": true,
  "contract_only": true,
  "selected_compatibility_path": "option_B_reroute_through_production_import_derived_path",
  "selected_next_boundary_option": "ready_for_8Y_13C_controlled_production_import_derived_reroute_smoke",
  "source_schema": "sentigraph_controlled_evidence_layer_write_candidate_set_v0_1",
  "intermediate_schema": "sentigraph_controlled_production_evidence_import_candidate_set_v0_1",
  "target_runtime_input_schema": "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1",
  "helper_called": false,
  "reroute_implemented": false,
  "controlled_evidenceitem_write_runtime_called": false,
  "actual_evidence_layer_write_used": false,
  "production_evidence_item_created": false,
  "production_case_created": false,
  "production_analysis_run_created": false
}
```

## D. Contract Steps

Step 1 contract:

- input: 8Y-12 direct write-candidate set
- helper surface if later approved: `controlled_production_evidence_import_candidate`
- output schema if later approved: `sentigraph_controlled_production_evidence_import_candidate_set_v0_1`
- output mode if later approved: `backend_only_local_production_evidence_import_candidate_boundary`
- side effect expectation: no persistence, no Evidence Layer write, no production EvidenceItem

Step 2 contract:

- input: controlled production evidence import candidate set
- helper surface if later approved: `controlled_evidence_layer_write_candidate_from_production_import_candidate`
- output schema if later approved: `sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1`
- output mode if later approved: `backend_only_local_evidence_layer_write_candidate_boundary`
- side effect expectation: no persistence, no Evidence Layer write, no production EvidenceItem

Step 3 contract:

- input: production-import-derived write-candidate set
- future runtime surface: `controlled_evidenceitem_evidence_layer_write_runtime`
- 8Y-13B approval: none
- future runtime call: not approved

## E. Not Actual Production Import

Production-import-derived is a controlled schema lineage label in this context. It is not general production import.

This contract does not allow:

- `evidence_import.py` calls
- `evidence_ingestion.py` calls
- persisted Evidence Layer record creation
- production EvidenceItem creation
- production case creation
- production `analysis_run` creation
- route/API/frontend behavior
- Source 11 runtime
- actual FinalSummaryReport runtime
- B-end/Sandbox/export/public delivery
- real API or real LLM use
- provider or collector job execution
- URL fetching or scraping

## F. Future 8Y-13C Input Contract

Future 8Y-13C may accept only:

```json
{
  "schema": "sentigraph_controlled_evidence_layer_write_candidate_set_v0_1",
  "actual_evidence_layer_write_used": false,
  "evidence_layer_write": false,
  "persisted_evidence_layer_record_created": false,
  "production_evidence_item_created": false,
  "production_case_created": false,
  "production_analysis_run_created": false,
  "evidence_import_service_called": false,
  "evidence_ingestion_service_called": false,
  "production_evidenceitem_write_runtime_used": false,
  "actual_review_queue_runtime_used": false,
  "production_review_queue_item_created": false,
  "raw_rows_exposed": false,
  "raw_comments_exposed": false,
  "raw_identities_exposed": false,
  "author_names_or_profile_urls_exposed": false,
  "secrets_read": false,
  "human_review_required": true,
  "no_automatic_trust_upgrade": true
}
```

Equivalent safe summaries may be accepted only if they preserve the same side-effect false flags and human-review/no-trust-upgrade boundaries.

## G. Future 8Y-13C Output Contract

Future 8Y-13C may produce, only inside controlled backend test path:

```json
{
  "production_evidence_import_candidate_created": true,
  "production_import_candidate_created": true,
  "production_import_candidate_schema": "sentigraph_controlled_production_evidence_import_candidate_set_v0_1",
  "production_import_candidate_mode": "backend_only_local_production_evidence_import_candidate_boundary",
  "production_import_derived_write_candidate_created": true,
  "production_import_derived_write_candidate_schema": "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1",
  "write_candidate_from_production_import_candidate_mode": "backend_only_local_evidence_layer_write_candidate_boundary",
  "controlled_evidenceitem_write_runtime_called": false,
  "production_evidenceitem_write_runtime_used": false,
  "actual_evidence_layer_write_used": false,
  "evidence_layer_write": false,
  "persisted_evidence_layer_record_created": false,
  "production_evidence_item_created": false,
  "production_case_created": false,
  "production_analysis_run_created": false,
  "human_review_required": true,
  "no_automatic_trust_upgrade": true
}
```

The output must not include raw row values, raw comments, raw identities, author names, profile URLs, secrets, absolute private paths, route state, frontend state, public output, delivery output, Source 11 output, or FinalSummaryReport output.

## H. Future 8Y-13C Approval Phrase

Inactive future phrase:

```text
APPROVE_8Y_13C_CONTROLLED_PRODUCTION_IMPORT_DERIVED_REROUTE_SMOKE
```

This phrase is not active in 8Y-13B. It does not authorize implementation in 8Y-13B, actual Evidence Layer write, persisted record creation, production EvidenceItem creation, production case creation, production `analysis_run` creation, controlled EvidenceItem write runtime calls, `evidence_import.py`, `evidence_ingestion.py`, Source 11 runtime, FinalSummaryReport runtime, route/API/frontend behavior, B-end/Sandbox/export/public delivery, real APIs, real LLMs, provider jobs, collector jobs, URL fetching, or scraping.

## I. Old 8Y-14 Phrase Status

```text
APPROVE_8Y_14_CONTROLLED_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_SMOKE
```

Status:

```text
inactive_not_selected_pending_compatibility_path
```

8Y-13C, if later approved, only produces the runtime-expected candidate schema. It does not call the runtime and does not revive the old phrase.

After 8Y-13C, a fresh docs-only gate must decide whether any controlled EvidenceItem write smoke may be reconsidered.

## J. Hard Stop Conditions

Stop future 8Y-13C if any task needs:

- unsafe or missing controlled production evidence import candidate helper surface
- unsafe or missing production-import-derived write candidate helper surface
- helper approval phrase missing, unsafe, or encoding-invalid
- actual Evidence Layer write
- persisted Evidence Layer record
- production EvidenceItem
- production case
- production `analysis_run`
- controlled EvidenceItem write runtime call
- `evidence_import.py` or `evidence_ingestion.py` production write service
- route/API/frontend behavior
- Source 11 runtime
- actual FinalSummaryReport runtime
- B-end/Sandbox/export/public delivery
- arbitrary real exchange directory
- arbitrary package directory
- private collector source inspection
- collector job execution
- raw row/comment/identity exposure
- author names/profile URLs as actual values
- real API, real LLM, network fetch, or scraping
- automatic trust upgrade
- customer_ready, public_ready, production_ready, final_ready, export_ready, or source11_runtime_ready claim

## K. Route C Relationship

The reroute keeps Route C active but inserts an explicit compatibility bridge before any write runtime can be reconsidered.

Later gates remain separate:

- actual Evidence Layer write gate
- production EvidenceItem gate
- production case gate
- production `analysis_run` gate
- Production Analysis Result authorization chain
- Source 11 / FinalSummaryReport Route B runtime gates
- B-end/Sandbox/export/public/final-delivery gates

## L. Next Boundary

Selected next boundary:

```text
ready_for_8Y_13C_controlled_production_import_derived_reroute_smoke
```

The next boundary may implement only the controlled reroute smoke if separately approved. It must not call controlled EvidenceItem write runtime or perform actual Evidence Layer write.
