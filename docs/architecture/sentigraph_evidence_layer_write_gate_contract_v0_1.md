# Sentigraph Evidence Layer Write Gate Contract v0.1

## A. Purpose

This contract defines the 8Y-11 governance boundary between the completed 8Y-10 local controlled Evidence Layer import candidate smoke and any future controlled Evidence Layer write-candidate smoke.

It is docs-only and gate-only. It does not implement a helper, route, API, frontend view, runtime persistence, write-candidate creation, Evidence Layer write, persisted Evidence Layer record creation, production EvidenceItem creation, production case creation, production `analysis_run` creation, actual Review Queue runtime, production Review Queue item creation, Source 11 runtime, actual FinalSummaryReport runtime, B-end report runtime, Sandbox/public event runtime, export/download/public/final-delivery runtime, provider job, collector job, real API call, real LLM call, URL fetch, or scrape.

## B. Source Path Contract

Selected Route C path:

```text
redacted row preview
-> controlled evidence candidate
-> review-only / review queue candidate
-> Evidence Layer import candidate
-> Evidence Layer write candidate
```

8Y-10 completed only the helper hop from controlled review queue candidate to controlled Evidence Layer import candidate.

8Y-11 decides that the next candidate boundary may be considered because an existing safe backend helper surface is present:

```text
backend/app/services/controlled_evidence_layer_write_candidate.py
```

This is not actual Evidence Layer write. It is a local Evidence-Layer-write-candidate-shaped boundary helper.

## C. Accepted Source Object

Future 8Y-12, if separately approved, may only accept:

```text
evidence_layer_import_candidate_set_schema = sentigraph_controlled_evidence_layer_import_candidate_set_v0_1
evidence_layer_import_candidate_set_status = evidence_layer_import_candidate_set_warn_manual_review_required
evidence_layer_import_candidate_mode = backend_only_local_evidence_layer_import_candidate_boundary
source_review_queue_candidate_set_schema = sentigraph_controlled_review_queue_candidate_set_v0_1
human_review_required = true
preview_only = true
import_candidate_only = true
evidence_layer_import_candidate_created = true
evidence_item_created = false
evidence_items_created = false
production_evidence_item_created = false
evidence_layer_write = false
review_queue_item_created = false
production_review_queue_item_created = false
production_case_created = false
production_analysis_run_created = false
```

Equivalent safe summaries may be accepted only if they preserve the same false side-effect flags and do not contain raw rows, raw comments, raw identities, author names, profile URLs, private paths, cookies, sessions, tokens, API keys, browser profiles, or secrets.

## D. Existing Evidence Layer Write Candidate Helper Surface

Observed existing helper:

```text
service = backend/app/services/controlled_evidence_layer_write_candidate.py
phase = 8W-19
evidence_layer_write_candidate_set_schema = sentigraph_controlled_evidence_layer_write_candidate_set_v0_1
evidence_layer_write_candidate_schema = sentigraph_controlled_evidence_layer_write_candidate_v0_1
source_evidence_layer_import_candidate_set_schema = sentigraph_controlled_evidence_layer_import_candidate_set_v0_1
source_evidence_layer_import_candidate_schema = sentigraph_controlled_evidence_layer_import_candidate_v0_1
evidence_layer_write_candidate_mode = backend_only_local_evidence_layer_write_candidate_boundary
```

Observed helper boundaries:

```text
human_review_required = true
preview_only = true
evidence_layer_write_candidate_only = true
evidence_layer_write_candidate_created = true only when called with exact helper approval
evidence_item_created = false
evidence_items_created = false
production_evidence_item_created = false
evidence_layer_write = false
review_queue_item_created = false
production_review_queue_item_created = false
production_case_created = false
production_analysis_run_created = false
route_ready = false
frontend_ready = false
production_ready = false
public_ready = false
customer_ready = false
```

The helper reports runtime side-effect flags as false, including provider/collector jobs, real API/LLM calls, URL fetch, scraping, private collector access, real exchange directory reads, original package row reads, raw identity emission, Evidence Layer writes, Review Queue item creation, production case creation, production analysis run creation, report/runtime generation, frontend modification, publish/send/post, and auto-execution.

## E. Surface Classification Matrix

| Surface | Classification | Relation | Side-effect classification |
| --- | --- | --- | --- |
| `controlled_evidence_layer_import_candidate.py` | backend_helper | import_candidate_source | no_persistence |
| `test_controlled_evidence_layer_import_candidate.py` | test_only | import_candidate_source | no_persistence |
| `test_8y_10_controlled_review_queue_candidate_to_evidence_layer_import_candidate_smoke.py` | test_only | import_candidate_source | no_persistence |
| `sentigraph_8y_10_controlled_review_queue_candidate_to_evidence_layer_import_candidate_smoke_report_v0_1.md` | docs_only | import_candidate_source | no_persistence |
| `controlled_evidence_layer_write_candidate.py` | backend_helper | evidence_layer_write_candidate | no_persistence |
| `test_controlled_evidence_layer_write_candidate.py` | test_only | evidence_layer_write_candidate | no_persistence |
| `controlled_evidence_layer_write_candidate_from_production_import_candidate.py` | backend_helper | evidence_layer_write_candidate | no_persistence |
| `controlled_evidenceitem_evidence_layer_write_runtime.py` | backend_helper / runtime_helper | production_evidence_write | runtime_local_only in controlled test path |
| `test_controlled_evidenceitem_evidence_layer_write_runtime.py` | test_only | production_evidence_write | runtime_local_only in controlled test path |
| `controlled_production_evidence_import_candidate.py` | backend_helper | production_evidence_import | no_persistence |
| `controlled_production_case_candidate.py` | backend_helper | production_case | no_persistence |
| `controlled_production_analysis_run_candidate.py` | backend_helper | production_analysis_run | no_persistence |
| `evidence_import.py` | backend_service | production_import | actual_Evidence_Layer_write_possible if called |
| `evidence_ingestion.py` | backend_service | production_import | actual_Evidence_Layer_write_possible if called |
| `backend/app/schemas/evidence.py` | backend_schema | production_import | unknown unless instantiated |
| `analysis_request_store.py` downstream functions | backend_service | production_case / production_analysis_run / report chain | runtime_local_only when called |
| `sentigraph_evidence_layer_import_candidate_gate_contract_v0_1.md` | docs_only | import_candidate_source | no_persistence |
| `sentigraph_8y_9_evidence_layer_import_candidate_gate_decision_v0_1.md` | docs_only | import_candidate_source | no_persistence |

## F. Future 8Y-12 Output Contract

If future 8Y-12 is separately approved, it may produce only a local controlled Evidence Layer write-candidate object.

Minimum expected output constraints:

```text
evidence_layer_write_candidate_created = true only inside controlled backend test path
write_candidate_created = true only inside controlled backend test path
write_candidate_mode = backend_only_local_evidence_layer_write_candidate_boundary or safe equivalent
actual_evidence_layer_write_used = false
evidence_layer_write = false
persisted_evidence_layer_record_created = false
production_evidence_item_created = false
production_case_created = false
production_analysis_run_created = false
evidence_import_service_called = false
evidence_ingestion_service_called = false
production_evidenceitem_write_runtime_used = false
actual_review_queue_runtime_used = false
production_review_queue_item_created = false
source11_runtime_called = false
actual_final_summary_report_created = false
b_end_report_runtime_generated = false
sandbox_public_event_runtime_generated = false
export_download_public_delivery_created = false
generated_response_text = false
route_ready = false
frontend_ready = false
production_ready = false
customer_ready = false
public_ready = false
raw_rows_exposed = false
raw_comments_exposed = false
raw_identities_exposed = false
author_names_or_profile_urls_exposed = false
secrets_read = false
human_review_required = true
no_automatic_trust_upgrade = true
```

## G. Future 8Y-12 Approval Phrase

Future 8Y-12 exact approval phrase:

```text
APPROVE_8Y_12_CONTROLLED_EVIDENCE_LAYER_IMPORT_CANDIDATE_TO_WRITE_CANDIDATE_SMOKE
```

This phrase is inactive in 8Y-11. It is a future placeholder only. It does not authorize implementation, write-candidate creation in 8Y-11, actual Evidence Layer write, persisted Evidence Layer record creation, production EvidenceItem creation, production case creation, production `analysis_run` creation, actual Review Queue runtime, production Review Queue item creation, Source 11 runtime, actual FinalSummaryReport runtime, route/API/frontend behavior, delivery runtime, provider/collector execution, real API calls, real LLM calls, URL fetching, or scraping.

## H. Related Phrase Status

The 8Y-10 smoke phrase remains limited to 8Y-10:

```text
APPROVE_8Y_10_CONTROLLED_REVIEW_QUEUE_CANDIDATE_TO_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE
```

The 8Y-8 smoke phrase remains limited to 8Y-8:

```text
APPROVE_8Y_8_CONTROLLED_EVIDENCE_CANDIDATE_TO_REVIEW_QUEUE_CANDIDATE_SMOKE
```

The previous direct import phrase remains inactive and not selected:

```text
APPROVE_8Y_6_CONTROLLED_REDACTED_ROW_PREVIEW_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE
```

None of these phrases may authorize 8Y-12 work.

## I. Required Stop Rules

Future 8Y-12 must stop if any request requires:

- actual Evidence Layer write
- persisted Evidence Layer record
- production EvidenceItem
- production case
- production `analysis_run`
- `evidence_import.py` / `evidence_ingestion.py` production write service
- production EvidenceItem write/runtime helper
- actual Review Queue runtime
- production Review Queue item
- Source 11 runtime
- actual FinalSummaryReport runtime
- route/API/frontend
- B-end/Sandbox/export/public delivery
- provider or collector execution
- private collector source inspection
- arbitrary real exchange directory
- arbitrary package directory
- additional row parsing
- evidence_items.csv parsing
- source_manifest row parsing
- collection_log row parsing
- original package row reading
- raw comments
- raw identities
- author names/profile URLs as actual values
- cookies, sessions, tokens, browser profiles, secrets, private paths, or `.env` values
- real API/LLM/network/fetch/scrape
- automatic trust upgrade
- customer/public/production readiness claim

## J. Relationship to Write, Production, and Runtime Gates

Evidence Layer write candidate is not actual Evidence Layer write.

Actual Evidence Layer write, production EvidenceItem, production case, production `analysis_run`, actual analysis execution, production Analysis Result, Source 11 runtime, actual FinalSummaryReport runtime, report generation, export/download/public access, and final delivery each remain separate gates.

## K. Selected Next Boundary Option

Because a safe backend helper surface exists and it is separate from actual Evidence Layer write and production EvidenceItem creation, 8Y-11 selects:

```text
ready_for_8Y_12_controlled_evidence_layer_import_candidate_to_write_candidate_smoke
```

This is only a planning state. Future 8Y-12 still requires a new task with the exact inactive phrase promoted by the user. No implementation is approved by this contract.
