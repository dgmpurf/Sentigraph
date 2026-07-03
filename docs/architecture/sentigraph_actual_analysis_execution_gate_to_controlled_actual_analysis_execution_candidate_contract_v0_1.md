# Sentigraph Actual Analysis Execution Gate to Controlled Actual Analysis Execution Candidate Contract v0.1

## A. Contract Purpose

This contract defines the boundary between the 8W-36 Actual Analysis Execution Gate Decision and a possible future backend-only Controlled Actual Analysis Execution Candidate helper implementation.

The contract prevents the future candidate-helper discussion from being mistaken for actual analysis execution, production analysis_run creation, analysis result generation, production case creation, production EvidenceItem creation, Review Queue runtime, route/API/frontend behavior, B-end report runtime, Sandbox/public event runtime, export/download/public access/external delivery/final delivery runtime, provider/collector execution, real API calls, real LLM calls, URL fetching, scraping, private collector inspection, real exchange directory reads, or additional row parsing.

## B. Source Object Allowed from 8W-35 / 8W-34

The only allowed source object for a future 8W-37 candidate helper discussion is the controlled local production analysis run candidate set accepted by 8W-35 and produced by 8W-34:

`sentigraph_controlled_production_analysis_run_candidate_set_v0_1`

Required source facts:

- candidate schema: `sentigraph_controlled_production_analysis_run_candidate_v0_1`
- candidate set status: `production_analysis_run_candidate_set_warn_manual_review_required`
- candidate count: `1`
- source production case candidate count: `1`
- source controlled evidence item count: `5`
- warning count: `1`
- human review required: `yes`
- production analysis run candidate created: `true`, controlled local only
- production analysis_run created: `false`
- actual analysis execution started: `false`
- analysis result created: `false`
- production case created: `false`
- production EvidenceItem created: `false`
- Review Queue item created: `false`
- production Review Queue item created: `false`
- Review Queue runtime used: `false`
- route/API/frontend changed: `false`
- private collector inspected: `false`
- real exchange directory read: `false`

No original package row, collector raw output, exchange directory, production Evidence Layer record, production review queue state, production case state, production analysis_run state, frontend state, route state, public URL, signed URL, download package, external delivery, final delivery, or customer-facing output is an approved source for this contract.

## C. Actual Analysis Execution Gate Definition

The Actual Analysis Execution Gate is a governance decision point. It determines whether a later backend-only Controlled Actual Analysis Execution Candidate helper implementation may be considered after separate exact approval.

The gate must define:

- source object scope
- warning/manual-review carry-forward
- production analysis run candidate versus production analysis_run separation
- production analysis run candidate versus actual analysis execution separation
- controlled actual analysis execution candidate versus actual analysis execution separation
- actual analysis execution versus analysis result generation separation
- future exact approval protocol
- blockers and non-approvals

The gate must not execute analysis, create production analysis_run records, generate analysis results, create production cases, create production EvidenceItems, write Evidence Layer, create Review Queue Items, add route/API/frontend behavior, generate B-end reports, generate Sandbox/public event outputs, generate response text, generate downloads, enable public access, perform external delivery, perform final delivery, execute providers or collectors, call real APIs, call real LLMs, inspect private collector source, read real exchange directories, or parse additional row files.

## D. Future Controlled Actual Analysis Execution Candidate Helper Definition

A future Controlled Actual Analysis Execution Candidate helper, if separately approved in 8W-37, may be considered only as a backend-only local transformation from the accepted 8W-34 controlled production analysis run candidate set summary toward a tightly bounded actual-analysis-execution-candidate-shaped output.

It may only be:

- backend-only
- test-first
- local-only
- controlled production-analysis-run-candidate-derived only
- bounded to the existing candidate count
- warning-preserving
- human-review-only
- no automatic trust upgrade
- candidate-shaped only

It must still preserve:

- no actual analysis execution
- no analysis result generation
- no production analysis_run creation
- no production case creation
- no production EvidenceItem creation
- no Review Queue Item creation
- no production Review Queue Item creation
- no Review Queue runtime
- no frontend/route/API behavior
- no B-end report runtime
- no Sandbox/public event runtime
- no public/customer output
- no export/download/public access/external delivery/final delivery runtime
- no real API/LLM/provider/collector
- no additional row parsing unless separately approved
- no private collector inspection
- no real exchange directory read

## E. Implementation Separation

8W-36 is not 8W-37.

8W-36 is docs-only. It does not approve implementation.

Any future 8W-37 implementation must be a separate user-approved task with the exact ASCII-only approval phrase. It must include tests proving missing, wrong, non-ASCII, or garbled approval phrases block before any candidate construction, file open, row parsing, actual analysis execution, analysis result generation, production analysis_run creation, production case creation, production EvidenceItem creation, Review Queue Item creation, route/API/frontend behavior, report generation, Sandbox/public event generation, delivery runtime, provider execution, collector execution, real API call, or real LLM call.

## F. Controlled Production Analysis Run Candidate Is Not Production analysis_run

A controlled production analysis run candidate is not a production analysis_run.

It must not:

- create production analysis_run records
- persist production analysis_run state
- appear in route/API/frontend as production analysis_run
- count as executed analysis history
- create report candidates
- create analysis results
- imply production readiness

## G. Controlled Production Analysis Run Candidate Is Not Actual Analysis Execution

A controlled production analysis run candidate is not actual analysis execution.

It must not:

- run analysis
- call an execution engine
- create findings
- create scores
- create conclusions
- create report-ready material
- feed Sandbox/public event output
- generate response text

Actual analysis execution requires a later separate gate and explicit approval.

## H. Controlled Actual Analysis Execution Candidate Is Not Actual Analysis Execution

A future controlled actual-analysis-execution-candidate object, if ever implemented, would still not be actual analysis execution.

It would only be a governance candidate object that describes whether a later actual execution phase could be considered.

It must not:

- execute the analysis
- generate analysis results
- create production analysis_run records
- update production state
- create report or public output
- publish, send, post, or deliver anything

## I. Actual Analysis Execution Is Not Analysis Result Generation Unless Separately Approved

Actual analysis execution and analysis result generation are distinct boundaries.

Any future actual analysis execution approval must not automatically approve:

- Analysis Result record creation
- report candidate generation
- final summary report generation
- export artifact generation
- public URL or signed URL generation
- external delivery
- public/customer display

Analysis result generation requires a later separate gate and explicit approval.

## J. Actual Analysis Execution Is Not B-end Report Runtime

Actual analysis execution is not B-end report runtime.

It must not generate:

- report candidates
- final summary reports
- strategy reports
- customer-facing report text
- export packages
- downloadable files
- delivery artifacts

B-end report runtime requires a later separate gate and explicit approval.

## K. Actual Analysis Execution Is Not Sandbox / Public Event Runtime

Actual analysis execution is not Sandbox or public event runtime.

It must not generate:

- Sandbox fixtures
- public event pages
- public event routes
- Event Plaza entries
- public status cards
- response copy
- C-end public claims

Sandbox/public event runtime requires a later separate gate and explicit approval.

## L. Actual Analysis Execution Is Not Review Queue Runtime

Actual analysis execution governance is not Review Queue runtime.

It must not create:

- Review Queue Items
- production Review Queue Items
- review action records
- review audit timeline events

Human-review-required state remains visible metadata, but it is not a review queue record.

## M. Warning / Manual-review Carry-forward

The warning state is part of the contract:

- `8w34_warning_count = 1`
- `human_review_required = yes`
- `8w34_production_analysis_run_candidate_set_status = production_analysis_run_candidate_set_warn_manual_review_required`

Future 8W-37 must preserve this warning state unless a separate human-reviewed process explicitly resolves it.

The warning state must not be cleared by transformation and must not be used as evidence verification, trust upgrade, production analysis_run readiness, actual analysis execution readiness, analysis result readiness, report readiness, public readiness, or customer readiness.

## N. Redaction / Minimization Carry-forward

Future 8W-37 must keep the source scope minimized to controlled candidate-set metadata.

It must not inspect:

- raw comments
- raw identities
- raw author identifiers
- private collector source
- real exchange directories
- env-provided real paths
- original package rows
- `evidence_items.jsonl`
- `evidence_items.csv`
- `source_manifest.jsonl`
- `collection_log.jsonl`
- secrets, tokens, cookies, sessions, salts, credentials, or environment values

Any detection of forbidden fields must block further progression.

## O. Future Blocker Categories

A future Controlled Actual Analysis Execution Candidate helper must block on:

- missing exact approval phrase
- wrong exact approval phrase
- non-ASCII approval phrase
- garbled approval phrase
- wrong source candidate set schema
- wrong source candidate schema
- wrong source candidate set status
- candidate count mismatch
- source count mismatch
- warning count mismatch
- missing human-review-required state
- any production analysis_run flag already true
- any actual analysis execution flag already true
- any analysis result flag already true
- any production case flag already true
- any production EvidenceItem flag already true
- any Review Queue Item flag already true
- any production Review Queue item flag already true
- route/API/frontend request
- B-end report request
- Sandbox/public event request
- export/download/public access/external delivery/final delivery request
- provider or collector execution request
- private collector source request
- real exchange directory request
- original row parsing request
- real API or real LLM request
- generated response text request
- publish, send, post, or delivery request

## P. Future Exact Approval Protocol, ASCII-only

Future 8W-37, if requested, must require this exact ASCII-only approval phrase:

`APPROVE_8W_37_CONTROLLED_ACTUAL_ANALYSIS_EXECUTION_CANDIDATE_HELPER_IMPLEMENTATION`

This phrase is not active implementation approval in 8W-36.

8W-36 does not approve Controlled Actual Analysis Execution Candidate helper implementation.

8W-36 does not approve actual analysis execution.

8W-36 does not approve analysis result generation.

8W-36 does not approve production analysis_run creation.

No Chinese approval phrase is defined for future 8W-37.

## Q. Forbidden Current Actions

8W-36 forbids:

- Controlled Actual Analysis Execution Candidate helper implementation
- actual analysis execution
- analysis execution
- analysis result generation
- production analysis_run creation
- production case creation
- production EvidenceItem creation
- Evidence Layer write
- Review Queue Item creation
- production Review Queue Item creation
- Review Queue runtime
- route/API/frontend behavior
- frontend integration
- private collector inspection
- real exchange directory reads
- original row parsing
- public route creation
- B-end report runtime
- Sandbox/public event runtime
- generated response text
- export/download/public access/external delivery/final delivery runtime
- provider execution
- collector execution
- real API calls
- real LLM calls
- URL fetching or scraping
- Project Source changes

## R. Forbidden Future Interpretations

This contract must not be interpreted as:

- approval to implement Controlled Actual Analysis Execution Candidate helper
- approval to create production analysis_run records
- approval to start actual analysis execution
- approval to generate analysis results
- approval to create production cases
- approval to create production EvidenceItems
- approval to write production Evidence Layer
- approval to create Review Queue Items
- approval to create production Review Queue Items
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

The only selected next boundary is future 8W-37 consideration after separate exact ASCII-only approval.
