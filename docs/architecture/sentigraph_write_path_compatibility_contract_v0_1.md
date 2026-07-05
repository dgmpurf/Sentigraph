# Sentigraph Write Path Compatibility Contract v0.1

## A. Purpose

This contract records the 8Y-13A compatibility decision after 8Y-13 blocked the direct actual Evidence Layer write / production EvidenceItem gate.

8Y-13A is docs-only, planning-only, and compatibility-decision-only. It does not implement an adapter, does not implement a reroute, and does not call the controlled EvidenceItem write runtime.

## B. Compatibility Problem

8Y-12 produced the direct Route C write-candidate set:

```text
sentigraph_controlled_evidence_layer_write_candidate_set_v0_1
```

The existing controlled EvidenceItem write runtime helper expects:

```text
sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1
```

The schemas are not interchangeable. A compatibility strategy is required before any future controlled write smoke can be reconsidered.

## C. Selected Path

```json
{
  "phase": "8Y-13A",
  "decision": "ready",
  "docs_only": true,
  "compatibility_decision_only": true,
  "selected_compatibility_path": "option_B_reroute_through_production_import_derived_path",
  "selected_next_boundary_option": "ready_for_8Y_13B_production_import_derived_reroute_contract_docs_only",
  "adapter_implemented": false,
  "reroute_implemented": false,
  "actual_evidence_layer_write_used": false,
  "evidence_layer_write": false,
  "persisted_evidence_layer_record_created": false,
  "production_evidence_item_created": false,
  "production_case_created": false,
  "production_analysis_run_created": false,
  "production_evidenceitem_write_runtime_used": false
}
```

## D. Selected Path Shape

The selected direction is:

```text
8Y-12 direct write candidate
-> controlled production evidence import candidate boundary
-> production-import-derived write candidate boundary
-> future controlled EvidenceItem write runtime input expectations
```

This path is selected because the existing helper chain already supports the schema expected by the controlled EvidenceItem write runtime:

- `controlled_production_evidence_import_candidate.py` accepts `sentigraph_controlled_evidence_layer_write_candidate_set_v0_1`
- `controlled_evidence_layer_write_candidate_from_production_import_candidate.py` produces `sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1`
- `controlled_evidenceitem_evidence_layer_write_runtime.py` expects `sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1`

## E. Option A Status

Option A, a direct-schema adapter, is not selected now.

It would preserve the Route C line more directly, but it would also create a new adapter shape that risks duplicating or skipping existing 8W-22 / 8W-25 governance. If Option A is ever reconsidered, it needs a separate docs-only contract before implementation.

## F. Option B Status

Option B is selected only as a docs-only reroute contract direction.

It may be considered because it reuses existing governed helper boundaries and matches the runtime helper input contract. It must be described carefully so production-import-derived candidate language is not mistaken for actual production import, Evidence Layer write, or production EvidenceItem creation.

8Y-13A does not approve invoking any helper at runtime.

## G. Option C Status

Option C, continued pause, is not selected because enough existing surfaces exist to justify a docs-only reroute contract. If 8Y-13B cannot keep side effects false or cannot preserve Route C lineage, the chain must pause again.

## H. Future 8Y-13B Contract Requirements

Future 8Y-13B must define:

- allowed source: the 8Y-12 direct write-candidate object or a safe summary
- allowed intermediate: controlled production evidence import candidate boundary
- allowed derived target: production-import-derived write-candidate boundary
- exact schema handoff into future controlled EvidenceItem write runtime input expectations
- warning_count carry-forward
- human_review_required carry-forward
- no_automatic_trust_upgrade carry-forward
- redaction/minimization carry-forward
- no side-effect flags
- hard stop rules
- tests expected for a later implementation phase, without creating tests in 8Y-13B

Future 8Y-13B must not implement anything.

## I. Future Approval Phrase

Inactive future phrase for 8Y-13B:

```text
APPROVE_8Y_13B_PRODUCTION_IMPORT_DERIVED_REROUTE_CONTRACT_DOCS_ONLY
```

This phrase is not active in 8Y-13A. It does not authorize implementation, adapter creation, reroute implementation, actual Evidence Layer write, persisted record creation, production EvidenceItem creation, production case creation, production `analysis_run` creation, Review Queue runtime, Source 11 runtime, FinalSummaryReport runtime, B-end report output, Sandbox/public-event output, export/download/public delivery, route/API/frontend behavior, provider/collector jobs, real APIs, real LLMs, URL fetching, or scraping.

## J. Old 8Y-14 Phrase Status

Old phrase:

```text
APPROVE_8Y_14_CONTROLLED_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_SMOKE
```

Status:

```text
inactive_not_selected_pending_compatibility_path
```

It must not authorize any work until the selected compatibility path is resolved by later docs-only gate work.

## K. Hard Blockers

Stop future compatibility work if it needs:

- adapter implementation
- reroute implementation
- actual Evidence Layer write
- persisted Evidence Layer record
- production EvidenceItem
- production case
- production `analysis_run`
- `evidence_import.py` / `evidence_ingestion.py` production write service
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
- customer_ready, public_ready, production_ready, final_ready, export_ready, or source11_runtime_ready claim

## L. Route Separation

8Y-13A keeps Route C alive as a governance path but redirects the next compatibility discussion through the production-import-derived controlled helper chain. It does not activate actual write. It does not activate production case, production `analysis_run`, production Analysis Result creation, Source 11, FinalSummaryReport, or delivery runtime.

## M. Next Boundary

Next boundary:

`ready_for_8Y_13B_production_import_derived_reroute_contract_docs_only`

The next boundary should remain docs-only and should not call any helper or runtime.
