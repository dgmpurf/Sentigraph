# Sentigraph Production Case Gate to Controlled Production Case Candidate Contract v0.1

## A. Contract Purpose

This contract defines the governance boundary between the 8W-30 Production Case gate decision and a possible future backend-only Controlled Production Case Candidate helper implementation.

This contract is docs-only.

It does not implement Controlled Production Case Candidate creation, create production cases, create production `analysis_run` records, create production EvidenceItems, write production Evidence Layer, create Review Queue Items, create production review queue items, add route/API/frontend behavior, generate B-end reports, generate Sandbox/public event outputs, generate response text, generate downloads, enable public access, perform external delivery, perform final delivery, execute providers or collectors, call real APIs, call real LLMs, inspect private collector source, read real exchange directories, or parse additional row files.

## B. Source Object Allowed from 8W-29 / 8W-28

The only allowed source for a future Controlled Production Case Candidate helper discussion is the already-established 8W-28 controlled local runtime output summary accepted by 8W-29:

`sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1`

Required source facts:

- 8W-29 decision is `ready`
- 8W-29 selected next boundary is `ready_for_8W_30_production_case_gate_decision_docs_only`
- 8W-28 runtime schema is `sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1`
- 8W-28 write result schema is `sentigraph_controlled_evidence_layer_write_result_v0_1`
- 8W-28 controlled evidence item schema is `sentigraph_controlled_evidence_item_v0_1`
- 8W-28 write runtime status is `evidence_layer_write_runtime_warn_manual_review_required`
- controlled evidence item count is `5`
- source Evidence Layer Write Candidate count is `5`
- warning count is `1`
- human review required is `yes`
- EvidenceItem created is `true`, controlled local only
- Evidence Layer write is `true`, controlled local helper/test path only
- production EvidenceItem created is `false`
- production case created is `false`
- production `analysis_run` created is `false`
- Review Queue Item created is `false`
- production review queue item created is `false`
- Review Queue runtime used is `false`
- route/API/frontend behavior added is `false`
- additional row parsing performed is `false`
- private collector inspected is `false`
- real exchange directory read is `false`

No original row file, collector raw output, exchange directory, production Evidence Layer record, production review queue state, production case state, production `analysis_run` state, frontend state, route state, public URL, signed URL, download package, external delivery, final delivery, or customer-facing output is an approved source for this contract.

## C. Production Case Gate Definition

The Production Case gate is a governance decision point. It determines whether a later backend-only Controlled Production Case Candidate helper implementation may be considered after separate exact approval.

The gate may define:

- allowed source object
- blocker categories
- warning/manual-review carry-forward
- redaction/minimization carry-forward
- production case versus production `analysis_run` separation
- future test expectations
- future exact approval protocol

The gate must not perform Controlled Production Case Candidate creation, production case creation, production `analysis_run` creation, production EvidenceItem creation, production Evidence Layer write, Review Queue Item creation, route/API/frontend behavior, report generation, Sandbox/public event generation, delivery runtime, provider execution, collector execution, real API calls, or real LLM calls.

## D. Future Controlled Production Case Candidate Helper Definition

A future 8W-31 Controlled Production Case Candidate helper, if separately approved, may be considered only as a backend-only local transformation from the accepted 8W-28 controlled local output summary toward a tightly bounded production-case-candidate-shaped output.

It must remain:

- backend-only
- test-first
- local-only
- controlled Evidence Layer write completion derived only
- bounded to the existing controlled item count
- redacted
- warning-preserving
- human-review-only
- no automatic trust upgrade
- no production case creation
- no production `analysis_run` creation
- no production EvidenceItem creation
- no Review Queue Item creation
- no production review queue item creation
- no Review Queue runtime
- no frontend/route/API behavior
- no B-end report runtime
- no Sandbox/public event runtime
- no public/customer output
- no export/download/public/final-delivery runtime
- no real API/LLM/provider/collector execution
- no additional row parsing unless separately approved
- no private collector inspection
- no real exchange directory read

## E. Implementation Separation

Future 8W-31 implementation is separate from:

- 8W-28 controlled EvidenceItem-shaped object creation
- 8W-28 controlled local Evidence Layer write result creation
- 8W-29 completion and gate decision
- 8W-30 Production Case gate decision
- production case creation
- production `analysis_run` creation
- production EvidenceItem creation
- Review Queue runtime
- route/API/frontend integration
- report generation
- export/download/public access/external/final delivery runtime

Any future implementation must require:

- a separate user task
- exact ASCII-only approval phrase
- tests proving missing, wrong, non-ASCII, or garbled approval phrases block before side effects
- tests proving source schema/status/count/warning boundaries are preserved
- tests proving forbidden production and delivery side-effect flags remain false
- tests proving no row files are opened unless a later separate checkpoint approves that source

## F. Controlled EvidenceItem is Not Production EvidenceItem

A controlled EvidenceItem-shaped object is not a production EvidenceItem.

It must not:

- use production EvidenceItem schema as if imported
- reserve production EvidenceItem ids
- imply production Evidence Layer persistence
- imply production case readiness
- imply analysis readiness
- imply report readiness
- imply public readiness
- imply customer readiness

Any production EvidenceItem creation requires a later separate implementation task and exact approval phrase.

## G. Controlled Evidence Layer Write Result is Not Production Case

A controlled local Evidence Layer write result is not a production case.

It does not:

- create a production case id
- reserve a production case id
- attach evidence to a production case
- establish case completeness
- establish analysis readiness
- create customer-facing claims
- create public-facing claims

## H. Controlled Production Case Candidate is Not Production analysis_run

A future Controlled Production Case Candidate would not be a production `analysis_run`.

It must not:

- run analysis
- create analysis results
- generate risk scores
- generate forecasts
- generate report candidates
- generate final reports
- generate Sandbox/public event outputs
- generate response text

Production `analysis_run` creation requires a separate future gate after production case governance.

## I. Production Case is Not Analysis Execution

Production case state, even if later separately approved, is not analysis execution.

It must not:

- mark evidence as analysis-ready by itself
- produce analysis results
- multiply sentiment, risk, or coverage conclusions
- produce report-ready claims
- produce public-facing conclusions
- create automatic recommendations

Analysis execution requires a separate future gate.

## J. Production Case is Not Review Queue Runtime

Production case governance is not Review Queue runtime.

Future 8W-31 must not create:

- Review Queue Items
- production review queue items
- reviewer assignments
- review decisions
- review action audit entries
- audit timeline mutations

Human-review-required state remains visible, but it is not a review queue record.

## K. Warning / Manual-review Carry-forward

The warning state is part of the contract:

- `8w28_warning_count = 1`
- `human_review_required = yes`
- `8w28_write_runtime_status = evidence_layer_write_runtime_warn_manual_review_required`

Future 8W-31 must preserve this warning state unless a separate human-reviewed process explicitly resolves it.

The warning state must not be cleared by transformation and must not be used as evidence verification, trust upgrade, production EvidenceItem readiness, production case readiness, production `analysis_run` readiness, analysis readiness, report readiness, public readiness, or customer readiness.

## L. Redaction / Minimization Carry-forward

Future phases must carry forward:

- redacted snippets only
- no raw comments
- no raw identities
- no profile URLs
- no private messages
- no emails or phones
- no cookies, tokens, sessions, passwords, API keys, salts, or secrets
- no absolute filesystem paths
- no package paths
- no collector raw paths
- no generated response text
- no psychological profiles or persuasion scores
- no review action runtime state
- no production ids unless a later gate explicitly approves them

Any detection of forbidden fields must block further progression.

## M. Future Blocker Categories

A future Controlled Production Case Candidate helper must block on:

- missing exact approval phrase
- wrong exact approval phrase
- non-ASCII approval phrase
- garbled approval phrase
- source schema mismatch
- source status mismatch
- controlled evidence item count mismatch
- warning count mismatch
- missing human-review-required state
- any production EvidenceItem flag already true
- any production case flag already true
- any production `analysis_run` flag already true
- any Review Queue Item flag already true
- any production review queue item flag already true
- raw identity exposure
- secret-like value exposure
- private collector source request
- real exchange directory request
- additional row parsing request
- route/API/frontend request
- report/Sandbox/public event request
- download/public access/external/final-delivery request
- real API / real LLM / provider / collector execution request
- full-web, full-platform, official verification, causal proof, or production-readiness overclaim

## N. Future Exact Approval Protocol, ASCII-only

Future 8W-31, if requested, must require this exact ASCII-only approval phrase:

`APPROVE_8W_31_CONTROLLED_PRODUCTION_CASE_CANDIDATE_HELPER_IMPLEMENTATION`

This phrase is not active implementation approval in 8W-30.

8W-30 does not approve Controlled Production Case Candidate helper implementation.

8W-30 does not approve production case creation.

8W-30 does not approve production `analysis_run` creation.

8W-30 does not approve production EvidenceItem creation.

Future 8W-31 tests must prove that missing, wrong, non-ASCII, or garbled variants block before any controlled production case candidate construction, production case creation, production `analysis_run` creation, production EvidenceItem creation, Evidence Layer write, file open, row parsing, Review Queue Item creation, route/API/frontend behavior, report generation, Sandbox/public event generation, delivery runtime, provider execution, collector execution, real API call, or real LLM call.

## O. Forbidden Current Actions

8W-30 must not perform:

- Controlled Production Case Candidate helper implementation
- production case creation
- production `analysis_run` creation
- production EvidenceItem creation
- production Evidence Layer persistence
- Review Queue Item creation
- production review queue item creation
- Review Queue runtime
- route/API/frontend behavior
- frontend integration
- additional row parsing
- private collector inspection
- real exchange directory reads
- B-end report runtime
- Sandbox/public event runtime
- generated response text
- public route creation
- public URL generation
- signed URL generation
- download package runtime
- public access runtime
- external delivery runtime
- final delivery runtime
- provider execution
- collector execution
- real API calls
- real LLM calls
- URL fetches
- scraping
- publish, send, post, execute, or auto-execute behavior

## P. Forbidden Future Interpretations

This contract must not be interpreted as:

- approval to implement Controlled Production Case Candidate helper
- approval to create production cases
- approval to create production `analysis_run` records
- approval to create production EvidenceItems
- approval to write production Evidence Layer
- approval to create Review Queue Items
- approval to create production review queue items
- approval to add route/API/frontend behavior
- approval to integrate frontend
- approval to run analysis
- approval to generate B-end reports
- approval to generate Sandbox/public event runtime
- approval to generate response text
- approval to create public URLs or signed URLs
- approval to generate download packages
- approval to perform public access, external delivery, or final delivery
- approval to parse more row files
- approval to inspect private collector source
- approval to read real exchange directories
- approval to call real APIs or real LLMs
- approval to execute provider or collector jobs

The only selected next boundary is future 8W-31 consideration after separate exact ASCII-only approval.
