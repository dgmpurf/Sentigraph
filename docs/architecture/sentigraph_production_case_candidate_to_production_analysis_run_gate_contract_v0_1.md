# Sentigraph Production Case Candidate to Production Analysis Run Gate Contract v0.1

## A. Contract Purpose

This contract defines the governance boundary between the 8W-31 controlled production case candidate helper checkpoint and a possible future docs-only Production Analysis Run gate decision.

This contract is docs-only.

It does not implement production `analysis_run` creation, production case creation, production EvidenceItem creation, production Evidence Layer write, Review Queue Item creation, production review queue item creation, Review Queue runtime, route/API/frontend behavior, B-end report runtime, Sandbox/public event runtime, generated response text, export/download/public access/external delivery/final delivery runtime, provider execution, collector execution, real API calls, real LLM calls, URL fetching, scraping, private collector inspection, real exchange directory reads, or additional evidence row parsing.

## B. Source Object Allowed from 8W-31

The only allowed source for a future 8W-33 docs-only Production Analysis Run gate discussion is the accepted 8W-31 controlled local production case candidate output summary:

`sentigraph_controlled_production_case_candidate_set_v0_1`

Required source facts:

- 8W-31 decision is `ready`
- production case candidate set schema is `sentigraph_controlled_production_case_candidate_set_v0_1`
- production case candidate schema is `sentigraph_controlled_production_case_candidate_v0_1`
- production case candidate set status is `production_case_candidate_set_warn_manual_review_required`
- production case candidate count is `1`
- source controlled evidence item count is `5`
- warning count is `1`
- human review required is `yes`
- production case candidate created is `yes`, controlled local only
- production case created is `false`
- production `analysis_run` created is `false`
- production EvidenceItem created is `false`
- Review Queue Item created is `false`
- production review queue item created is `false`
- Review Queue runtime used is `false`
- route/API/frontend changed is `false`
- additional row parsing performed is `false`
- private collector inspected is `false`
- real exchange directory read is `false`
- real API / real LLM / provider / collector execution is `false`

No original row file, collector raw output, exchange directory, production Evidence Layer record, production review queue state, production case state, production `analysis_run` state, frontend state, route state, public URL, signed URL, download package, external delivery, final delivery, or customer-facing output is an approved source for this contract.

## C. Production Case Candidate Completion Definition

Production Case Candidate completion means the 8W-31 helper/test-path output is complete only as a controlled local candidate-shaped object.

Completion requires:

- exactly one case-level candidate
- source controlled evidence item count remains five
- warning count remains one
- human-review-required state remains active
- redaction and minimization remain active
- no production ids are emitted
- no raw author identifiers, raw comments, profile URLs, secrets, paths, or generated response text are emitted
- production case, production `analysis_run`, production EvidenceItem, Review Queue, route/API/frontend, report, Sandbox/public event, and delivery flags remain false

Completion does not mean production case readiness, production `analysis_run` readiness, analysis execution readiness, report readiness, public readiness, or customer readiness.

## D. Production Analysis Run Gate Definition

The Production Analysis Run gate is a future docs-only governance decision point.

It may define:

- allowed source objects from 8W-31
- blocker categories
- warning/manual-review carry-forward
- redaction/minimization carry-forward
- production case candidate versus production case versus production `analysis_run` separation
- production `analysis_run` versus analysis execution separation
- future exact approval protocol
- future implementation stop conditions

It must not create production `analysis_run` records, production cases, production EvidenceItems, Review Queue Items, routes, API endpoints, frontend UI, analysis results, reports, Sandbox/public event output, generated response text, downloads, public access, external delivery, final delivery, provider jobs, collector jobs, real API calls, real LLM calls, URL fetches, scraping behavior, private collector inspection, real exchange directory reads, or additional row parsing.

## E. Production Analysis Run Implementation Separation

A future Production Analysis Run gate decision is separate from any implementation.

Implementation would require:

- a later separate implementation task
- an exact ASCII-only approval phrase marked active only in that later task
- tests proving missing, wrong, non-ASCII, and garbled approval phrases block before side effects
- tests proving source schema/status/count/warning boundaries are preserved
- tests proving production case candidate is not treated as production case
- tests proving production `analysis_run` creation does not run analysis unless separately approved
- tests proving no route/API/frontend, report, Sandbox/public event, delivery, provider, collector, real API, real LLM, URL fetch, scraping, private collector, real exchange, or additional row parsing behavior is introduced

## F. Controlled Production Case Candidate is Not Production Case

A controlled production case candidate is not a production case.

It must not:

- create or reserve a production case id
- persist a production case
- attach production EvidenceItems
- mark evidence as case-complete
- mark case state as production-ready
- mark the case as analysis-ready
- imply any public or customer-facing case record

## G. Controlled Production Case Candidate is Not Production analysis_run

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

## H. Production analysis_run is Not Analysis Execution Unless Separately Approved

Even a future production `analysis_run` record would not automatically mean analysis execution.

A production `analysis_run` gate must preserve the separation between:

- analysis run metadata
- analysis execution
- analysis result generation
- report generation
- Sandbox/public event generation
- public/customer output
- publish/send/post/execute actions

Analysis execution requires a later separate gate and explicit approval.

## I. Production analysis_run is Not Review Queue Runtime

Production `analysis_run` governance is not Review Queue runtime.

Future phases must not infer:

- Review Queue Items
- production review queue items
- reviewer assignments
- review actions
- review decisions
- review audit timeline mutations

Human-review-required state remains visible, but it is not a production review queue record.

## J. Warning / Manual-review Carry-forward

The warning/manual-review state is part of the source contract:

- `8w31_warning_count = 1`
- `human_review_required = yes`
- `8w31_production_case_candidate_set_status = production_case_candidate_set_warn_manual_review_required`

Future 8W-33 must carry this state forward and must not treat it as official verification, trust upgrade, production case readiness, production `analysis_run` readiness, analysis readiness, report readiness, public readiness, or customer readiness.

## K. Allowed Future 8W-33 Docs-only Inputs

Future 8W-33 may inspect only safe committed metadata from:

- 8W-31 health report
- 8W-31 helper contract shape and tests
- 8W-30 Production Case gate decision
- 8W-29 Evidence Layer Write completion decision
- 8W-28 controlled EvidenceItem / Evidence Layer write runtime report

Future 8W-33 must not inspect original package rows, raw comments, raw identities, private collector source, real exchange directories, env-provided real paths, or additional evidence row files.

## L. Forbidden Current and Future Actions

This contract does not approve:

- production `analysis_run` creation
- production case creation
- production EvidenceItem creation
- production Evidence Layer write
- Review Queue Item creation
- production review queue item creation
- Review Queue runtime
- route/API/frontend behavior
- frontend integration
- analysis execution
- B-end report runtime
- Sandbox/public event runtime
- generated response text
- public route creation
- public URL generation
- signed URL generation
- FileResponse or StreamingResponse download behavior
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
- private collector inspection
- real exchange directory reads
- additional row parsing
- publish, send, post, execute, or auto-execute behavior

## M. Future Blocker Categories

Future 8W-33 and any later implementation must block on:

- source schema mismatch
- source status mismatch
- production case candidate count mismatch
- source controlled evidence item count mismatch
- warning count mismatch
- missing human-review-required state
- any production case flag already true
- any production `analysis_run` flag already true
- any production EvidenceItem flag already true
- any Review Queue Item flag already true
- any production review queue item flag already true
- any route/API/frontend flag already true
- any report, Sandbox/public event, delivery, provider, collector, real API, real LLM, URL fetch, scraping, private collector, real exchange, or additional row parsing flag already true
- raw identity exposure
- raw comment exposure
- secret-like value exposure
- absolute path or package path exposure
- generated response text exposure
- full-web, full-platform, official verification, causal proof, production readiness, or customer readiness overclaim

## N. Future Redaction / Minimization Carry-forward Principles

Future phases must carry forward:

- safe aggregate metadata only
- redacted labels and snippets only
- safe controlled ids and hashes only
- no raw author identifiers
- no author names, usernames, display names, or profile URLs
- no raw comments
- no private messages
- no email, phone, or address fields
- no cookies, tokens, sessions, passwords, API keys, secrets, salts, or browser profile paths
- no absolute filesystem paths, package paths, or raw collector paths
- no generated response text
- no target user lists, persuasion scores, truth scores, official verification flags, prediction probabilities, psychological profiles, or personality diagnoses
- no review action, reviewer assignment, review decision, or audit timeline mutation state

## O. Approval Protocol

8W-32 does not activate an implementation approval phrase.

Future 8W-33 may define only a docs-only gate and may defer any future implementation phrase. If a later implementation is ever considered, the approval phrase must be ASCII-only and tested so that missing, wrong, non-ASCII, or garbled variants block before production `analysis_run` creation, production case creation, production EvidenceItem creation, Review Queue Item creation, route/API/frontend behavior, file opening, row parsing, report generation, Sandbox/public event generation, delivery runtime, provider execution, collector execution, real API calls, or real LLM calls.

## P. Forbidden Interpretations

This contract must not be interpreted as:

- approval to implement production `analysis_run`
- approval to implement production case creation
- approval to implement production EvidenceItem creation
- approval to run analysis
- approval to generate analysis results
- approval to generate B-end reports
- approval to generate Sandbox/public events
- approval to create public routes
- approval to generate downloads or public/signed URLs
- approval to perform public access, external delivery, or final delivery
- approval to create Review Queue Items or production review queue items
- approval to add route/API/frontend behavior
- approval to parse more row files
- approval to inspect private collector source
- approval to read real exchange directories
- approval to call real APIs or real LLMs
- approval to execute provider or collector jobs
- approval to publish, send, post, execute, or auto-execute anything

The only selected next boundary is future 8W-33 docs-only Production Analysis Run Gate Decision consideration.
