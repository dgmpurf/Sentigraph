# Sentigraph Evidence Layer Import Candidate to Evidence Layer Write Gate Contract v0.1

## A. Contract Purpose

This contract defines the governance boundary between 8W-16 local evidence-layer-import-candidate-shaped boundary objects and any future Evidence Layer Write gate discussion.

This contract is docs-only. It does not implement Evidence Layer write, create EvidenceItems, create production EvidenceItems, write Evidence Layer, create Review Queue Items, create production review queue items, create production cases, create production `analysis_run` records, add route/API/frontend behavior, generate reports, generate Sandbox/public event outputs, or parse additional row files.

## B. Source Object Allowed from 8W-16

The only allowed source for an 8W-17 completion decision is the 8W-16 local evidence layer import candidate set:

`sentigraph_controlled_evidence_layer_import_candidate_set_v0_1`

Required source facts:

- 8W-16 decision is `ready`
- source phase is `8W-16`
- candidate item schema is `sentigraph_controlled_evidence_layer_import_candidate_v0_1`
- candidate set status is `evidence_layer_import_candidate_set_warn_manual_review_required`
- candidate count is `5`
- source review queue candidate count is `5`
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

## C. Evidence Layer Import Candidate Completion Definition

Evidence Layer Import Candidate completion means only:

`complete_local_evidence_layer_import_candidate_boundary_only_with_warning_manual_review_required`

It confirms that 8W-16 produced bounded, redacted, local candidate-shaped boundary objects derived from 8W-13 review queue candidates.

It does not confirm Evidence Layer write readiness, EvidenceItem readiness, production import readiness, production case readiness, production `analysis_run` readiness, analysis readiness, report readiness, Sandbox/public event readiness, public readiness, or customer readiness.

## D. Evidence Layer Write Gate Definition

An Evidence Layer Write gate is a future docs-only checkpoint.

It may decide whether a later backend-only Evidence Layer Write Candidate / Import Runtime implementation can be considered after separate exact approval.

It may define:

- required source object shape
- required warning/manual-review carry-forward
- required redaction and minimization rules
- required blockers
- required no-production-side-effect flags
- required future tests
- exact future implementation approval phrase, if and only if that later gate chooses to define one

It must not create EvidenceItems and must not write Evidence Layer.

## E. Evidence Layer Write Implementation Separation

Evidence Layer Write implementation is a separate future phase, if ever approved.

8W-17 does not approve:

- Evidence Layer Write Candidate creation
- Evidence Layer write helper implementation
- Evidence Layer write runtime
- EvidenceItem creation
- production EvidenceItem creation
- Evidence Layer persistence
- production case creation
- production `analysis_run` creation
- route/API/frontend behavior
- review queue runtime
- B-end report runtime
- Sandbox/public event runtime
- export/download/public/final-delivery runtime

## F. Evidence Layer Import Candidate is not EvidenceItem

An Evidence Layer Import Candidate is not an EvidenceItem.

It must not be interpreted as:

- imported evidence
- production evidence
- verified evidence
- EvidenceItem schema instance
- EvidenceItem id
- analysis-ready evidence
- report-ready evidence

Any EvidenceItem creation requires a later separate gate and explicit implementation approval.

## G. Evidence Layer Import Candidate is not Production EvidenceItem

The 8W-16 candidate object is not a production EvidenceItem.

It must not:

- create production EvidenceItems
- reserve production EvidenceItem ids
- imply production import completion
- imply source verification
- imply trust upgrade
- imply production persistence

Any production EvidenceItem creation requires a later separate gate and explicit implementation approval.

## H. Evidence Layer Import Candidate is not Evidence Layer Write

Evidence Layer Import Candidate completion is not Evidence Layer write.

It must not:

- write Evidence Layer
- mutate Evidence Layer state
- persist production evidence
- set production evidence ids
- mark evidence as imported
- mark evidence as analysis-included
- mark evidence as report-ready

Any Evidence Layer write requires a later separate gate and explicit implementation approval.

## I. Evidence Layer Import Candidate is not Production Case / analysis_run Input

Evidence Layer Import Candidates must not be treated as:

- production case input
- production `analysis_run` input
- analysis-ready evidence
- report-ready evidence
- B-end report runtime input
- Sandbox/public event runtime input
- generated response input
- public/customer-facing output

Any future production case, production `analysis_run`, report, Sandbox, public event, export, download, public access, external delivery, or final delivery transition requires a separate gate.

## J. Evidence Layer Import Candidate is not Analysis-ready Evidence

8W-16 candidate output must preserve:

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

8W-17 does not change these properties.

## K. Warning / Manual-review Handling

The source warning state is part of the contract:

- `warning_count = 1`
- `human_review_required = true`
- `evidence_layer_import_candidate_set_status = evidence_layer_import_candidate_set_warn_manual_review_required`

Future gates must preserve this warning state until a separate human-reviewed process explicitly resolves it.

The warning state must not be cleared by gate language and must not be used as evidence verification, trust upgrade, Evidence Layer write readiness, production readiness, analysis readiness, report readiness, public readiness, or customer readiness.

## L. Allowed Future 8W-18 Docs-only Inputs

Future 8W-18 may inspect:

- 8W-16 health report safe status fields
- 8W-16 service/test safe schema and boundary constants
- 8W-15 and 8W-17 gate docs
- safe aggregate counts and boundary flags

Future 8W-18 must not inspect:

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

## M. Forbidden Current and Future Actions

8W-17 forbids:

- Evidence Layer write
- EvidenceItem creation
- production EvidenceItem creation
- production case creation
- production `analysis_run` creation
- Review Queue Item creation
- production review queue item creation
- review queue runtime
- route/API/frontend behavior
- frontend integration
- B-end report runtime
- Sandbox/public event runtime
- generated response text
- public URL or signed URL generation
- download package runtime
- public access runtime
- external delivery runtime
- final delivery runtime
- additional row parsing
- private collector inspection
- real exchange directory read
- real API / real LLM calls
- provider or collector job execution

Future 8W-18 must remain docs-only and must keep the same prohibitions unless a later user request explicitly defines a new docs-only question.

## N. Future Blocker Categories

Any future Evidence Layer Write gate must block on:

- warning/manual-review state missing
- human review required flag missing
- candidate count mismatch
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
- report/Sandbox/public event request
- download/public access/external/final-delivery request
- real API / real LLM / provider / collector execution request
- full-web, full-platform, official verification, causal proof, or production-readiness overclaim

## O. Future Redaction / Minimization Carry-forward Principles

Future gates must carry forward:

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
- no review action state
- no production ids

Any detection of forbidden fields must block further progression.

## P. Evidence Layer / Production Boundary

Evidence Layer Import Candidate completion remains outside Evidence Layer.

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

## Q. Approval Protocol

8W-17 does not define an active implementation approval phrase.

Any exact approval phrase for a future Evidence Layer Write Candidate / Import Runtime implementation is deferred to a later 8W-18 decision. It is not active in 8W-17 and must not be inferred from this document.

## R. Forbidden Interpretations

This contract must not be interpreted as:

- approval to implement Evidence Layer write
- approval to create Evidence Layer Write Candidates
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

The only approved next boundary is a future docs-only Evidence Layer Write Gate Decision.
