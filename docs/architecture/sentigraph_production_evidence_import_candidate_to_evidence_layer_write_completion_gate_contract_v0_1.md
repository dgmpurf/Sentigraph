# Sentigraph Production Evidence Import Candidate to Evidence Layer Write Completion Gate Contract v0.1

## A. Contract Purpose

This contract defines the governance boundary between the completed 8W-22 local production-evidence-import-candidate-shaped boundary objects and a possible future docs-only Evidence Layer Write Gate Decision.

This contract is docs-only.

It does not implement Evidence Layer write, create EvidenceItems, create production EvidenceItems, create Review Queue Items, create production review queue items, create production cases, create production `analysis_run` records, add route/API/frontend behavior, generate reports, generate Sandbox/public event outputs, or parse additional row files.

## B. Source Object Allowed from 8W-22

The only allowed source for the 8W-23 completion and future gate discussion is the already-established 8W-22 local production evidence import candidate set:

`sentigraph_controlled_production_evidence_import_candidate_set_v0_1`

Required source facts:

- 8W-22 decision is `ready`
- 8W-22 source object kind is the in-memory controlled Evidence Layer Write Candidate set from 8W-19
- 8W-22 set schema is `sentigraph_controlled_production_evidence_import_candidate_set_v0_1`
- 8W-22 item schema is `sentigraph_controlled_production_evidence_import_candidate_v0_1`
- candidate set status is `production_evidence_import_candidate_set_warn_manual_review_required`
- production evidence import candidate count is `5`
- source evidence layer write candidate count is `5`
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

## C. Production Evidence Import Candidate Completion Definition

Production Evidence Import Candidate completion means:

- the 8W-22 helper produced local candidate-shaped boundary objects
- the objects are bounded to the accepted source candidate count
- warning/manual-review state remains active
- redacted snippets and safe lineage fields are preserved
- no production write occurred
- no trust upgrade occurred
- no analysis-ready or report-ready state was created
- no additional rows were parsed

Completion does not mean Evidence Layer Write completion.

Completion does not mean imported evidence.

Completion does not mean production evidence.

## D. Evidence Layer Write Gate Definition

The Evidence Layer Write gate is a future governance decision point that may ask whether a later backend-only Evidence Layer Write Candidate / EvidenceItem Write Runtime implementation can be considered after separate exact approval.

A future gate may define:

- allowed source object
- required blocker checks
- warning/manual-review carry-forward
- redaction/minimization carry-forward
- production boundary checks
- required tests
- future implementation approval protocol

A future gate must not perform Evidence Layer write.

## E. Evidence Layer Write Implementation Separation

Evidence Layer Write implementation is separate from:

- 8W-22 production evidence import candidate creation
- 8W-23 completion and gate decision
- future 8W-24 docs-only gate decision

Any Evidence Layer write implementation requires:

- a later separate task
- an exact approval phrase
- test-first implementation
- explicit blocker tests
- proof that missing, wrong, or garbled approval phrases block before side effects
- no file or row parsing unless separately approved

## F. Production Evidence Import Candidate is not EvidenceItem

A Production Evidence Import Candidate is not an EvidenceItem.

It must not:

- use production EvidenceItem schema as if imported
- create EvidenceItems
- reserve EvidenceItem ids
- imply Evidence Layer readiness
- imply analysis readiness
- imply report readiness

Any EvidenceItem creation requires a later separate gate and explicit implementation approval.

## G. Production Evidence Import Candidate is not Production EvidenceItem

A Production Evidence Import Candidate is not a production EvidenceItem.

It remains:

- local
- bounded
- redacted
- candidate-shaped
- warning-preserving
- human-review-required
- non-production

It must not be interpreted as production evidence, production import output, production review state, production case state, or production `analysis_run` input.

## H. Production Evidence Import Candidate is not Evidence Layer Write

Production Evidence Import Candidate creation is not Evidence Layer write.

It must not:

- write Evidence Layer
- mutate Evidence Layer state
- persist production evidence
- set production EvidenceItem ids
- mark evidence as imported
- mark evidence as analysis-included
- mark evidence as report-ready

Any Evidence Layer write requires a later separate gate and explicit implementation approval after candidate-shaped boundary work.

## I. Production Evidence Import Candidate is not Production Case / analysis_run Input

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

## J. Production Evidence Import Candidate is not Analysis-ready Evidence

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

## K. Production Evidence Import Candidate is not Report-ready Evidence

Production Evidence Import Candidate status must not be treated as report-ready.

It must not:

- generate B-end report sections
- generate public event summaries
- generate Sandbox fixtures
- generate response text
- supply customer-facing claims
- supply public-facing claims

Report readiness requires later gates after Evidence Layer write, production case governance, analysis governance, report candidate governance, final report review governance, export governance, and delivery governance.

## L. Warning / Manual-review Handling

The warning state is part of the contract:

- `warning_count = 1`
- `human_review_required = true`
- `production_evidence_import_candidate_set_status = production_evidence_import_candidate_set_warn_manual_review_required`

8W-23 treats this warning state as acceptable for a future docs-only gate discussion only because no write behavior is approved.

The warning state must not be cleared by transformation and must not be used as evidence verification, trust upgrade, EvidenceItem readiness, Evidence Layer write readiness, production readiness, analysis readiness, report readiness, public readiness, or customer readiness.

## M. Allowed Future 8W-24 Docs-only Inputs

Future 8W-24 may inspect only safe metadata already represented in:

- 8W-22 health report
- 8W-22 service/test contract
- 8W-23 planning decision
- this architecture contract

Future 8W-24 must not inspect:

- `evidence_items.jsonl`
- `evidence_items.csv`
- `source_manifest.jsonl`
- `collection_log.jsonl`
- original package rows
- raw comments
- raw identities
- private collector source
- private collector project
- real exchange directories
- env-provided real paths

## N. Forbidden Current and Future Actions

8W-23 and future 8W-24 must not perform:

- Evidence Layer write implementation
- EvidenceItem creation
- production EvidenceItem creation
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

## O. Future Blocker Categories

A future Evidence Layer Write gate must block on:

- unresolved warning/manual-review state
- missing human review acknowledgement
- missing exact approval protocol
- source schema mismatch
- source status mismatch
- candidate count mismatch
- any EvidenceItem flag already true
- any production EvidenceItem flag already true
- any Evidence Layer write flag already true
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

## P. Future Redaction / Minimization Carry-forward Principles

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

## Q. Evidence Layer / Production Boundary

Production Evidence Import Candidate completion remains outside Evidence Layer.

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

## R. Approval Protocol

8W-23 has no active implementation approval phrase.

Future 8W-24 is docs-only and must not activate an implementation phrase.

Any later implementation phase after 8W-24 must define and require a separate exact approval phrase. That future phrase must be tested so that missing, wrong, or garbled variants block before any side effect.

8W-23 does not approve Evidence Layer Write implementation.

8W-23 does not approve EvidenceItem creation.

8W-23 does not approve production EvidenceItem creation.

8W-23 does not approve Evidence Layer write, Review Queue Item creation, production case creation, production `analysis_run` creation, route/API/frontend behavior, reports, Sandbox/public events, or delivery runtime.

## S. Forbidden Interpretations

This contract must not be interpreted as:

- approval to implement Evidence Layer write
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

The only selected next boundary is future 8W-24 Evidence Layer Write Gate Decision Docs-only.
