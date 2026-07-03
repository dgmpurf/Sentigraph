# Sentigraph Production Analysis Run Gate to Controlled Production Analysis Run Candidate Contract v0.1

## A. Contract purpose

This contract defines the governance boundary between the 8W-33 Production Analysis Run gate decision and a possible future backend-only Controlled Production Analysis Run Candidate helper implementation.

This contract is docs-only.

It does not implement Controlled Production Analysis Run Candidate creation, create production `analysis_run` records, start analysis execution, create production cases, create production EvidenceItems, write production Evidence Layer, create Review Queue Items, create production review queue items, add route/API/frontend behavior, generate B-end reports, generate Sandbox/public event outputs, generate response text, generate downloads, enable public access, perform external delivery, perform final delivery, execute providers or collectors, call real APIs, call real LLMs, inspect private collector source, read real exchange directories, or parse additional row files.

## B. Source object allowed from 8W-32 / 8W-31

The only allowed source for a future Controlled Production Analysis Run Candidate helper discussion is the already-established 8W-31 controlled local production case candidate set summary accepted by 8W-32:

`sentigraph_controlled_production_case_candidate_set_v0_1`

Required source facts:

- 8W-32 decision is `ready`
- 8W-32 selected next boundary is `ready_for_8W_33_production_analysis_run_gate_decision_docs_only`
- production case candidate set schema is `sentigraph_controlled_production_case_candidate_set_v0_1`
- production case candidate schema is `sentigraph_controlled_production_case_candidate_v0_1`
- production case candidate set status is `production_case_candidate_set_warn_manual_review_required`
- production case candidate count is `1`
- source controlled evidence item count is `5`
- warning count is `1`
- human review required is `yes`
- production case candidate created is `true`, controlled local only
- production case created is `false`
- production `analysis_run` created is `false`
- analysis execution started is `false`
- production EvidenceItem created is `false`
- Review Queue Item created is `false`
- production review queue item created is `false`
- Review Queue runtime used is `false`
- route/API/frontend behavior added is `false`
- additional row parsing performed is `false`
- private collector inspected is `false`
- real exchange directory read is `false`

No original row file, collector raw output, exchange directory, production Evidence Layer record, production review queue state, production case state, production `analysis_run` state, frontend state, route state, public URL, signed URL, download package, external delivery, final delivery, or customer-facing output is an approved source for this contract.

## C. Production Analysis Run gate definition

The Production Analysis Run gate is a governance decision point. It determines whether a later backend-only Controlled Production Analysis Run Candidate helper implementation may be considered after separate exact approval.

The gate may define:

- allowed source object
- blocker categories
- warning/manual-review carry-forward
- redaction/minimization carry-forward
- production case candidate versus production case versus production `analysis_run` separation
- production `analysis_run` versus analysis execution separation
- future test expectations
- future exact approval protocol

The gate must not perform Controlled Production Analysis Run Candidate creation, production `analysis_run` creation, analysis execution, production case creation, production EvidenceItem creation, production Evidence Layer write, Review Queue Item creation, route/API/frontend behavior, report generation, Sandbox/public event generation, delivery runtime, provider execution, collector execution, real API calls, or real LLM calls.

## D. Future Controlled Production Analysis Run Candidate helper definition

A future 8W-34 Controlled Production Analysis Run Candidate helper, if separately approved, may be considered only as a backend-only local transformation from the accepted 8W-31 controlled local production case candidate set summary toward a tightly bounded production-analysis-run-candidate-shaped output.

It must remain:

- backend-only
- test-first
- local-only
- controlled production-case-candidate-derived only
- bounded to the existing production case candidate count
- bounded to the existing source controlled evidence item count
- redacted
- warning-preserving
- human-review-only
- no automatic trust upgrade
- no production `analysis_run` creation
- no analysis execution
- no production case creation
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

## E. Implementation separation

Future 8W-34 implementation is separate from:

- 8W-31 controlled production case candidate creation
- 8W-32 completion and gate decision
- 8W-33 Production Analysis Run gate decision
- production `analysis_run` creation
- analysis execution
- production case creation
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
- tests proving warning/manual-review state remains active
- tests proving forbidden production and delivery side-effect flags remain false
- tests proving no row files are opened unless a later separate checkpoint approves that source

## F. Controlled production case candidate is not production case

A controlled production case candidate is not a production case.

It must not:

- create or reserve a production case id
- persist a production case
- attach production EvidenceItems
- establish case completeness
- establish production readiness
- establish analysis readiness
- create customer-facing claims
- create public-facing claims

Any production case creation requires a later separate implementation task and exact approval phrase.

## G. Controlled production case candidate is not production analysis_run

A controlled production case candidate is not a production `analysis_run`.

It must not:

- create or reserve a production `analysis_run` id
- schedule analysis
- run analysis
- create analysis results
- create risk, sentiment, coverage, narrative, forecast, or strategy outputs
- create report candidates
- create final reports
- create Sandbox/public event outputs
- create generated response text

Production `analysis_run` creation requires a separate future gate after production case governance.

## H. Controlled Production Analysis Run Candidate is not analysis execution

A future Controlled Production Analysis Run Candidate, if separately approved, would still not be analysis execution.

It must not:

- run analysis
- calculate production scores
- produce analysis results
- produce recommendations
- produce report-ready claims
- produce public-facing conclusions
- produce customer-facing conclusions
- publish, send, post, execute, or auto-execute actions

Analysis execution requires a later separate gate and explicit approval.

## I. Production analysis_run is not B-end report runtime

Production `analysis_run` governance is not B-end report runtime.

Future phases must not infer:

- report candidate generation
- final report generation
- report export generation
- report download generation
- B-end customer report readiness
- sales or customer-facing deliverable readiness

B-end report runtime requires a later separate gate and explicit approval.

## J. Production analysis_run is not Sandbox/public event runtime

Production `analysis_run` governance is not Sandbox or public event runtime.

Future phases must not infer:

- Sandbox fixture generation
- public event page generation
- public event route creation
- public event narrative generation
- public visualization publication
- public/customer-facing output

Sandbox/public event runtime requires a later separate gate and explicit approval.

## K. Production analysis_run is not Review Queue runtime

Production `analysis_run` governance is not Review Queue runtime.

Future phases must not infer:

- Review Queue Items
- production review queue items
- reviewer assignments
- review actions
- review decisions
- review action audit entries
- audit timeline mutations

Human-review-required state remains visible, but it is not a review queue record.

## L. Warning/manual-review carry-forward

The warning state is part of the contract:

- `8w31_warning_count = 1`
- `human_review_required = yes`
- `8w31_production_case_candidate_set_status = production_case_candidate_set_warn_manual_review_required`

Future 8W-34 must preserve this warning state unless a separate human-reviewed process explicitly resolves it.

The warning state must not be cleared by transformation and must not be used as evidence verification, trust upgrade, production case readiness, production `analysis_run` readiness, analysis execution readiness, report readiness, public readiness, or customer readiness.

## M. Redaction/minimization carry-forward

Future phases must carry forward:

- redacted snippets only
- safe aggregate metadata only
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

## N. Future blocker categories

A future Controlled Production Analysis Run Candidate helper must block on:

- missing exact approval phrase
- wrong exact approval phrase
- non-ASCII approval phrase
- garbled approval phrase
- source schema mismatch
- source status mismatch
- production case candidate count mismatch
- source controlled evidence item count mismatch
- warning count mismatch
- missing human-review-required state
- any production case flag already true
- any production `analysis_run` flag already true
- any analysis execution flag already true
- any production EvidenceItem flag already true
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
- full-web, full-platform, official verification, causal proof, production-readiness, analysis-readiness, or customer-readiness overclaim

## O. Future exact approval protocol, ASCII-only

Future 8W-34, if requested, must require this exact ASCII-only approval phrase:

`APPROVE_8W_34_CONTROLLED_PRODUCTION_ANALYSIS_RUN_CANDIDATE_HELPER_IMPLEMENTATION`

This phrase is not active implementation approval in 8W-33.

8W-33 does not approve Controlled Production Analysis Run Candidate helper implementation.

8W-33 does not approve production `analysis_run` creation.

8W-33 does not approve analysis execution.

8W-33 does not approve production case creation.

8W-33 does not approve production EvidenceItem creation.

Future 8W-34 tests must prove that missing, wrong, non-ASCII, or garbled variants block before any controlled production analysis run candidate construction, production `analysis_run` creation, analysis execution, production case creation, production EvidenceItem creation, Evidence Layer write, file open, row parsing, Review Queue Item creation, route/API/frontend behavior, report generation, Sandbox/public event generation, delivery runtime, provider execution, collector execution, real API call, or real LLM call.

No Chinese approval phrase is defined for future 8W-34.

## P. Forbidden current actions

8W-33 must not perform:

- Controlled Production Analysis Run Candidate helper implementation
- production `analysis_run` creation
- analysis execution
- production case creation
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

## Q. Forbidden future interpretations

This contract must not be interpreted as:

- approval to implement Controlled Production Analysis Run Candidate helper
- approval to create production `analysis_run` records
- approval to start analysis execution
- approval to create production cases
- approval to create production EvidenceItems
- approval to write production Evidence Layer
- approval to create Review Queue Items
- approval to create production review queue items
- approval to add route/API/frontend behavior
- approval to integrate frontend
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

The only selected next boundary is future 8W-34 consideration after separate exact ASCII-only approval.
