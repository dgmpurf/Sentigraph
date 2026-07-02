# Sentigraph Production Evidence Import Gate Contract v0.1

## A. Contract Purpose

This contract defines the governance boundary for moving from 8W-19 local evidence-layer-write-candidate-shaped boundary objects toward a possible future Controlled Production Evidence Import Candidate helper.

This contract is docs-only.

It does not implement Production Evidence Import Candidate helper logic, create Production Evidence Import Candidates, create EvidenceItems, create production EvidenceItems, write Evidence Layer, create Review Queue Items, create production review queue items, create production cases, create production `analysis_run` records, add route/API/frontend behavior, generate reports, generate Sandbox/public event outputs, or parse additional row files.

## B. Source Object Allowed from 8W-19 / 8W-20

The only allowed source for a future Production Evidence Import Candidate discussion is the already-established 8W-19 local evidence layer write candidate set accepted by 8W-20:

`sentigraph_controlled_evidence_layer_write_candidate_set_v0_1`

Required source facts:

- 8W-20 decision is `ready`
- 8W-20 selected next boundary is `ready_for_8W_21_production_evidence_import_gate_decision_docs_only`
- 8W-19 candidate set schema is `sentigraph_controlled_evidence_layer_write_candidate_set_v0_1`
- 8W-19 candidate item schema is `sentigraph_controlled_evidence_layer_write_candidate_v0_1`
- candidate set status is `evidence_layer_write_candidate_set_warn_manual_review_required`
- candidate count is `5`
- source evidence layer import candidate count is `5`
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

## C. Future Local Production-evidence-import-candidate-shaped Object Definition

A future 8W-22 helper, if separately approved, may define local production-evidence-import-candidate-shaped objects.

Suggested future conceptual set fields:

- production evidence import candidate set schema
- production evidence import candidate set status
- source evidence layer write candidate set schema
- source evidence layer write candidate set status
- source evidence layer write candidate count
- warning count
- human review required
- boundary flags
- runtime side-effect flags
- candidates

Suggested future conceptual candidate fields:

- production evidence import candidate schema
- production evidence import candidate id
- source evidence layer write candidate id
- source evidence layer import candidate lineage id, if already present
- platform label
- evidence type label
- redacted title preview
- redacted body preview
- verification status
- review status
- trust label
- warning flags
- blocker flags
- human review required
- no-production-side-effect flags

These fields are design guidance only. They do not authorize implementation in 8W-21.

## D. Production Evidence Import Candidate is not EvidenceItem

A Production Evidence Import Candidate is not an EvidenceItem.

It must not:

- use the production EvidenceItem schema as if imported
- create EvidenceItems
- create production EvidenceItems
- reserve EvidenceItem ids
- imply Evidence Layer readiness
- imply analysis readiness
- imply report readiness

Any EvidenceItem creation requires a later separate gate and explicit implementation approval.

## E. Production Evidence Import Candidate is not Production EvidenceItem

A Production Evidence Import Candidate is not a production EvidenceItem.

It must remain:

- local
- bounded
- redacted
- candidate-shaped
- warning-preserving
- human-review-required
- non-production

It must not be interpreted as production evidence, production import output, production review state, production case state, or production `analysis_run` input.

## F. Production Evidence Import Candidate is not Evidence Layer Write

Production Evidence Import Candidate creation, if ever approved, is still not Evidence Layer write.

It must not:

- write Evidence Layer
- mutate Evidence Layer state
- persist production evidence
- set production EvidenceItem ids
- mark evidence as imported
- mark evidence as analysis-included
- mark evidence as report-ready

Any Evidence Layer write requires a later separate gate and explicit implementation approval after candidate-shaped boundary work.

## G. Production Evidence Import Candidate is not Production Case / analysis_run Input

Production Evidence Import Candidates must not be treated as:

- production case input
- production `analysis_run` input
- analysis-ready evidence
- report-ready evidence
- B-end report runtime input
- Sandbox/public event runtime input
- generated response input
- public/customer-facing output

Any future production case, production `analysis_run`, report, Sandbox, public event, export, download, public access, external delivery, or final delivery transition requires a separate gate.

## H. Production Evidence Import Candidate is not Analysis-ready Evidence

Production Evidence Import Candidate status must preserve:

- `human_review_required = true`
- warning/manual-review state
- selected sample limitation
- no official verification
- no causal proof
- no full-web coverage
- no full-platform coverage
- no full-thread coverage
- no automatic trust upgrade
- no automatic inclusion in analysis

It must not be used as analysis-ready evidence.

## I. Production Evidence Import Candidate is not Report-ready Evidence

Production Evidence Import Candidate status must not be treated as report-ready.

It must not:

- generate B-end report sections
- generate public event summaries
- generate Sandbox fixtures
- generate response text
- supply customer-facing claims
- supply public-facing claims

Report readiness requires later gates after Evidence Layer write, production case governance, analysis governance, report candidate governance, final report review governance, export governance, and delivery governance.

## J. Redaction / Minimization Carry-forward

Future 8W-22 must carry forward:

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
- no production ids

Any detection of forbidden fields must block further progression.

## K. Warning / Manual-review Carry-forward

The warning state is part of the contract:

- `warning_count = 1`
- `human_review_required = true`
- `evidence_layer_write_candidate_set_status = evidence_layer_write_candidate_set_warn_manual_review_required`

Future 8W-22 must preserve this warning state until a separate human-reviewed process explicitly resolves it.

The warning state must not be cleared by transformation and must not be used as evidence verification, trust upgrade, EvidenceItem readiness, Evidence Layer write readiness, production readiness, analysis readiness, report readiness, public readiness, or customer readiness.

## L. Future Blocker Categories

Any future Production Evidence Import Candidate helper must block on:

- missing exact approval phrase
- wrong exact approval phrase
- garbled approval phrase
- source schema mismatch
- source status mismatch
- candidate count mismatch
- missing warning/manual-review state
- missing human review required state
- source object already marked as EvidenceItem
- source object already marked as production EvidenceItem
- source object already marked as Evidence Layer write
- source object already marked as Review Queue Item
- source object already marked as production case
- source object already marked as production `analysis_run`
- raw identity exposure
- secret-like value exposure
- private collector source request
- real exchange directory request
- additional row parsing request
- route/API/frontend request
- review queue runtime request
- report/Sandbox/public event request
- download/public access/external/final-delivery request
- real API / real LLM / provider / collector execution request
- full-web, full-platform, official verification, causal proof, or production-readiness overclaim

## M. Future Test Expectations

If 8W-22 is explicitly approved, tests should prove:

- exact approval phrase is required before candidate creation
- exact phrase `批准 8W-22 Controlled Production Evidence Import Candidate Helper Implementation` is accepted
- garbled approval phrases are rejected
- missing approval phrase is rejected
- wrong approval phrase is rejected
- source schema mismatch blocks
- source status mismatch blocks
- warning count mismatch blocks
- missing human review required state blocks
- any EvidenceItem flag set to true blocks
- any production EvidenceItem flag set to true blocks
- any Evidence Layer write flag set to true blocks
- any Review Queue Item flag set to true blocks
- any production case flag set to true blocks
- any production `analysis_run` flag set to true blocks
- candidate output remains bounded
- candidate output remains redacted
- EvidenceItem fields are not produced
- Evidence Layer write flags remain false
- production side-effect flags remain false
- no file paths are accepted
- no package rows are parsed
- no route/API/frontend behavior is added

## N. Approval Protocol

Future 8W-22, if requested, must require this exact approval phrase:

`批准 8W-22 Controlled Production Evidence Import Candidate Helper Implementation`

This phrase is not active implementation approval in 8W-21.

8W-21 does not approve Controlled Production Evidence Import Candidate helper implementation.

8W-21 does not approve Production Evidence Import Candidate creation.

8W-21 does not approve EvidenceItem creation, production EvidenceItem creation, Evidence Layer write, Review Queue Item creation, production case creation, production `analysis_run` creation, route/API/frontend behavior, reports, Sandbox/public events, or delivery runtime.

## O. Evidence Layer / Production Boundary

Production Evidence Import Candidate planning remains outside Evidence Layer.

It must not:

- create EvidenceItems
- create production EvidenceItems
- write Evidence Layer
- create production cases
- create production `analysis_run` records
- create Review Queue Items
- create production review queue items
- run review queue runtime
- run analysis
- generate report
- generate Sandbox/public event
- generate public URL
- generate signed URL
- generate download package
- perform external delivery
- perform final delivery

Any progression beyond candidate-shaped objects requires a later separate gate and explicit approval.

## P. Forbidden Interpretations

This contract must not be interpreted as:

- approval to implement Controlled Production Evidence Import Candidate helper logic
- approval to create Production Evidence Import Candidates
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

The only selected next boundary is future 8W-22 consideration after separate exact approval.
