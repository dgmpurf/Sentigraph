# Sentigraph Review-only / Review Queue Candidate Gate Contract v0.1

## A. Purpose

This contract defines the 8Y-7 governance boundary between the completed 8Y-6 local controlled evidence candidate source-path smoke and any future controlled review-only / review queue candidate smoke.

It is docs-only and gate-only. It does not implement a helper, route, API, frontend view, runtime persistence, import candidate, Evidence Layer write, production EvidenceItem, production case, production `analysis_run`, Source 11 runtime, actual FinalSummaryReport runtime, report, Sandbox/public event, export/download/public/final-delivery runtime, provider job, collector job, real API call, real LLM call, URL fetch, or scrape.

## B. Source Path Contract

Selected Route C path:

```text
redacted row preview
-> controlled evidence candidate
-> review-only / review queue candidate
-> Evidence Layer import candidate
```

8Y-6 completed only the first helper hop from controlled row preview to controlled evidence candidate.

8Y-7 decides that the next candidate boundary may be considered because an existing safe backend helper surface is present:

```text
backend/app/services/controlled_review_queue_candidate.py
```

This is not actual Review Queue runtime. It is a local review-queue-candidate-shaped boundary helper.

## C. Accepted Source Object

Future 8Y-8, if separately approved, may only accept:

```text
candidate_set_schema = sentigraph_controlled_evidence_candidate_set_v0_1
candidate_set_status = evidence_candidate_set_warn_manual_review_required
candidate_mode = backend_only_local_preview_derived_evidence_candidate
source_preview_schema = sentigraph_controlled_row_preview_v0_1
human_review_required = true
preview_only = true
evidence_candidate_created = true
evidence_layer_write = false
review_queue_item_created = false
production_review_queue_item_created = false
production_case_created = false
production_analysis_run_created = false
```

Equivalent safe summaries may be accepted only if they preserve the same false side-effect flags and do not contain raw rows, raw comments, raw identities, author names, profile URLs, private paths, cookies, sessions, tokens, API keys, browser profiles, or secrets.

## D. Existing Review Queue Candidate Helper Surface

Observed existing helper:

```text
service = backend/app/services/controlled_review_queue_candidate.py
phase = 8W-13
review_queue_candidate_set_schema = sentigraph_controlled_review_queue_candidate_set_v0_1
review_queue_candidate_schema = sentigraph_controlled_review_queue_candidate_v0_1
source_candidate_set_schema = sentigraph_controlled_evidence_candidate_set_v0_1
source_candidate_schema = sentigraph_controlled_evidence_candidate_v0_1
review_queue_candidate_mode = backend_only_local_review_queue_candidate_boundary
```

Observed helper boundaries:

```text
human_review_required = true
preview_only = true
queue_candidate_only = true
review_queue_item_created = false
production_review_queue_item_created = false
evidence_items_created = false
evidence_layer_write = false
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
| `controlled_evidence_candidate.py` | backend_helper | evidence_candidate_source | no_persistence |
| `controlled_review_queue_candidate.py` | backend_helper | review_queue_candidate | no_persistence |
| `controlled_evidence_layer_import_candidate.py` | backend_helper | import_candidate | no_persistence |
| `analysis_request_store.py` review-only case / staging / review queue functions | backend_service | actual_review_queue_runtime | runtime_local_only when called |
| `backend/app/schemas` ReviewQueue models | backend_schema | actual_review_queue_runtime | unknown unless called |
| `test_controlled_review_queue_candidate.py` | test_only | review_queue_candidate | no_persistence |
| `sentigraph_evidence_candidate_to_review_queue_gate_contract_v0_1.md` | docs_only | review_queue_candidate | no_persistence |
| `sentigraph_review_queue_candidate_to_evidence_layer_import_gate_contract_v0_1.md` | docs_only | import_candidate | no_persistence |

## F. Future 8Y-8 Output Contract

If future 8Y-8 is separately approved, it may produce only a local controlled review-only / review queue candidate object.

Minimum expected output constraints:

```text
review_queue_candidate_created = true only inside controlled backend test path
review_queue_candidate_mode = backend_only_local_review_queue_candidate_boundary or safe equivalent
actual_review_queue_runtime_used = false
production_review_queue_item_created = false
evidence_layer_import_candidate_created = false
import_candidate_created = false
evidence_layer_write = false
production_evidence_item_created = false
production_case_created = false
production_analysis_run_created = false
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

## G. Future 8Y-8 Approval Phrase

Future 8Y-8 exact approval phrase:

```text
APPROVE_8Y_8_CONTROLLED_EVIDENCE_CANDIDATE_TO_REVIEW_QUEUE_CANDIDATE_SMOKE
```

This phrase is inactive in 8Y-7. It is a future placeholder only. It does not authorize implementation, actual Review Queue runtime, production Review Queue item creation, Evidence Layer import candidate creation, Evidence Layer write, production EvidenceItem creation, production case creation, production `analysis_run` creation, Source 11 runtime, actual FinalSummaryReport runtime, route/API/frontend behavior, delivery runtime, provider/collector execution, real API calls, real LLM calls, URL fetching, or scraping.

## H. Required Stop Rules

Future 8Y-8 must stop if any request requires:

- actual Review Queue runtime
- production Review Queue item
- Evidence Layer import candidate
- Evidence Layer write
- production EvidenceItem
- production case
- production `analysis_run`
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

## I. Relationship to Import Candidate and Later Gates

Review queue candidate completion is not Evidence Layer import.

Evidence Layer import candidate remains a later gate and must not be created by 8Y-8. Evidence Layer write, production EvidenceItem, production case, production `analysis_run`, actual analysis execution, production Analysis Result, Source 11 runtime, actual FinalSummaryReport runtime, report generation, export/download/public access, and final delivery each remain separate gates.

## J. Selected Next Boundary Option

Because a safe backend helper surface exists and it is separate from actual Review Queue runtime, 8Y-7 selects:

```text
ready_for_8Y_8_controlled_evidence_candidate_to_review_queue_candidate_smoke
```

This is only a planning state. Future 8Y-8 still requires a new task with the exact inactive phrase promoted by the user. No implementation is approved by this contract.
