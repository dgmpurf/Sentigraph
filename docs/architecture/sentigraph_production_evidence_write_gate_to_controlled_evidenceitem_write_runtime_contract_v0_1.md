# Sentigraph Production Evidence Write Gate to Controlled EvidenceItem Write Runtime Contract v0.1

## A. Contract Purpose

This contract defines the governance boundary between the 8W-27 Production Evidence Write gate decision and a possible future backend-only Controlled EvidenceItem / Evidence Layer Write Runtime implementation.

This contract is docs-only.

It does not implement Controlled EvidenceItem creation, create EvidenceItems, create production EvidenceItems, write Evidence Layer, create Review Queue Items, create production review queue items, create production cases, create production `analysis_run` records, add route/API/frontend behavior, generate reports, generate Sandbox/public event outputs, generate response text, generate downloads, enable public access, perform external delivery, perform final delivery, execute providers or collectors, call real APIs, call real LLMs, inspect private collector source, read real exchange directories, or parse additional row files.

## B. Source Object Allowed from 8W-25 / 8W-26

The only allowed source for a future Controlled EvidenceItem / Evidence Layer Write Runtime discussion is the already-established 8W-25 local evidence layer write candidate set accepted by 8W-26:

`sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1`

Required source facts:

- 8W-26 decision is `ready`
- 8W-26 selected next boundary is `ready_for_8W_27_production_evidence_write_gate_decision_docs_only`
- 8W-25 candidate set schema is `sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1`
- 8W-25 candidate item schema is `sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_v0_1`
- candidate set status is `evidence_layer_write_candidate_set_warn_manual_review_required`
- evidence layer write candidate count is `5`
- source production evidence import candidate count is `5`
- warning count is `1`
- human review required is `yes`
- EvidenceItem created is `false`
- production EvidenceItem created is `false`
- Evidence Layer write is `false`
- Review Queue Item created is `false`
- production review queue item created is `false`
- production case created is `false`
- production `analysis_run` created is `false`
- route/API/frontend behavior added is `false`
- additional row parsing performed is `false`
- private collector inspected is `false`
- real exchange directory read is `false`

No original row file, collector raw output, exchange directory, Evidence Layer record, production review queue state, production case state, production `analysis_run` state, frontend state, route state, public URL, signed URL, download package, external delivery, final delivery, or customer-facing output is an approved source for this contract.

## C. Production Evidence Write Gate Definition

The Production Evidence Write gate is a governance decision point. It determines whether a later backend-only Controlled EvidenceItem / Evidence Layer Write Runtime implementation may be considered after separate exact approval.

The gate may define:

- allowed source object
- blocker categories
- warning/manual-review carry-forward
- redaction/minimization carry-forward
- production boundary checks
- future test expectations
- future exact approval protocol

The gate must not perform Controlled EvidenceItem creation, EvidenceItem creation, production EvidenceItem creation, Evidence Layer write, production case creation, production `analysis_run` creation, Review Queue Item creation, route/API/frontend behavior, report generation, Sandbox/public event generation, delivery runtime, provider execution, collector execution, real API calls, or real LLM calls.

## D. Future Controlled EvidenceItem / Evidence Layer Write Runtime Definition

A future 8W-28 Controlled EvidenceItem / Evidence Layer Write Runtime, if separately approved, may be considered only as a backend-only local transformation from the accepted 8W-25 evidence layer write candidate set toward a tightly bounded EvidenceItem-shaped output.

It must remain:

- backend-only
- test-first
- local-only
- evidence-layer-write-candidate-derived only
- bounded to the existing candidate count
- redacted
- warning-preserving
- human-review-only
- no automatic trust upgrade
- no production case creation
- no production `analysis_run` creation
- no Review Queue Item creation
- no production review queue item creation
- no review queue runtime
- no frontend/route/API behavior
- no B-end report runtime
- no Sandbox/public event runtime
- no public/customer output
- no real API/LLM/provider/collector execution
- no additional row parsing unless separately approved
- no private collector inspection
- no real exchange directory read

## E. Implementation Separation

Future 8W-28 implementation is separate from:

- 8W-25 evidence layer write candidate creation
- 8W-26 candidate completion and gate decision
- 8W-27 Production Evidence Write gate decision
- production case creation
- production `analysis_run` creation
- review queue runtime
- route/API/frontend integration
- report generation
- export/download/public access/external/final delivery runtime

Any future implementation must require:

- a separate user task
- exact approval phrase
- tests proving missing, wrong, or garbled approval phrases block before side effects
- tests proving source schema/status/count/warning boundaries are preserved
- tests proving forbidden production and delivery side-effect flags remain false
- tests proving no row files are opened unless a later separate checkpoint approves that source

## F. Evidence Layer Write Candidate is not EvidenceItem

An Evidence Layer Write Candidate is not an EvidenceItem.

It must not:

- use production EvidenceItem schema as if imported
- create EvidenceItems
- reserve EvidenceItem ids
- imply Evidence Layer readiness
- imply analysis readiness
- imply report readiness
- imply public readiness
- imply customer readiness

Any EvidenceItem creation requires a later separate implementation task and exact approval phrase.

## G. Evidence Layer Write Candidate is not Production EvidenceItem

An Evidence Layer Write Candidate is not a production EvidenceItem.

It remains:

- local
- bounded
- redacted
- candidate-shaped
- warning-preserving
- human-review-required
- non-production

It must not be interpreted as production evidence, production import output, production review state, production case state, or production `analysis_run` input.

## H. EvidenceItem is not Production Case

Even if a future 8W-28 creates a Controlled EvidenceItem-shaped object after exact approval, that object must not be interpreted as a production case.

An EvidenceItem does not:

- create or mutate a production case
- establish case completeness
- establish case readiness for analysis
- create customer-facing claims
- create public-facing claims
- create report-ready state

Production case creation requires a separate future gate.

## I. EvidenceItem is not Production analysis_run

An EvidenceItem is not a production `analysis_run`.

An EvidenceItem does not:

- run analysis
- create analysis results
- generate risk scores
- generate forecasts
- generate report candidates
- generate final reports
- generate Sandbox/public event outputs
- generate response text

Production `analysis_run` creation requires a separate future gate after Evidence Layer and case governance.

## J. Evidence Layer Write is not Review Queue Runtime

Evidence Layer write is not review queue runtime.

Future 8W-28 must not create:

- Review Queue Items
- production review queue items
- reviewer assignments
- review decisions
- review action audit entries
- audit timeline mutations

Human-review-required state must remain visible. Any review queue transition requires a separate future gate.

## K. Warning / Manual-review Carry-forward

The warning state is part of the contract:

- `warning_count = 1`
- `human_review_required = true`
- `evidence_layer_write_candidate_set_status = evidence_layer_write_candidate_set_warn_manual_review_required`

Future 8W-28 must preserve this warning state unless a separate human-reviewed process explicitly resolves it.

The warning state must not be cleared by transformation and must not be used as evidence verification, trust upgrade, EvidenceItem readiness, Evidence Layer write readiness, production readiness, analysis readiness, report readiness, public readiness, or customer readiness.

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

A future Controlled EvidenceItem / Evidence Layer Write Runtime must block on:

- missing exact approval phrase
- wrong exact approval phrase
- garbled approval phrase
- source schema mismatch
- source status mismatch
- candidate count mismatch
- warning count mismatch
- missing human-review-required state
- any EvidenceItem flag already true before the controlled runtime
- any production EvidenceItem flag already true
- any Evidence Layer write flag already true before the controlled runtime
- any Review Queue Item flag already true
- any production case flag already true
- any production `analysis_run` flag already true
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

## N. Future Exact Approval Protocol

Future 8W-28, if requested, must require this exact approval phrase:

`批准 8W-28 Controlled EvidenceItem Evidence Layer Write Runtime Implementation`

This phrase is not active implementation approval in 8W-27.

8W-27 does not approve Controlled EvidenceItem / Evidence Layer Write Runtime implementation.

8W-27 does not approve EvidenceItem creation.

8W-27 does not approve production EvidenceItem creation.

8W-27 does not approve Evidence Layer write.

Future 8W-28 tests must prove that missing, wrong, or garbled variants block before any EvidenceItem construction, Evidence Layer write, file open, row parsing, production case creation, production `analysis_run` creation, Review Queue Item creation, route/API/frontend behavior, report generation, Sandbox/public event generation, delivery runtime, provider execution, collector execution, real API call, or real LLM call.

## O. Forbidden Current Actions

8W-27 must not perform:

- Controlled EvidenceItem / Evidence Layer Write Runtime implementation
- EvidenceItem creation
- production EvidenceItem creation
- Evidence Layer write
- Review Queue Item creation
- production review queue item creation
- review queue runtime
- production case creation
- production `analysis_run` creation
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
- provider or collector execution
- real API or real LLM calls
- publish, send, post, execute, or auto-execute behavior

## P. Forbidden Future Interpretations

This contract must not be interpreted as:

- approval to implement Controlled EvidenceItem / Evidence Layer Write Runtime
- approval to create EvidenceItems
- approval to create production EvidenceItems
- approval to write Evidence Layer
- approval to create Review Queue Items
- approval to create production review queue items
- approval to create production cases
- approval to create production `analysis_run` records
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

The only selected next boundary is future 8W-28 consideration after separate exact approval.
