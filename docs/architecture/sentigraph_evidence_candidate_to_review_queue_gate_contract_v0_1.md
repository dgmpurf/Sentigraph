# Sentigraph Evidence Candidate to Review Queue Gate Contract v0.1

## A. Contract Purpose

This contract defines the governance boundary between the 8W-10 local evidence-candidate-shaped boundary objects and any future Review Queue gate.

This contract is docs-only. It does not implement Review Queue helper logic, does not create review queue items, does not write Evidence Layer, does not create EvidenceItems, does not create production case, does not create production `analysis_run`, does not create route/frontend/API, and does not parse additional row files.

## B. Source Object Allowed from 8W-10

The only possible future source object for a Review Queue gate discussion is the 8W-10 local candidate set output:

`sentigraph_controlled_evidence_candidate_set_v0_1`

Required source state:

- 8W-10 decision is `ready`
- candidate set status is `evidence_candidate_set_warn_manual_review_required`
- candidate item schema is `sentigraph_controlled_evidence_candidate_v0_1`
- candidate count is `5`
- source preview rows count is `5`
- warning count is `1`
- human review required is `true`
- preview only is `true`
- candidates are redacted and preview-derived
- EvidenceItems created is `false`
- Evidence Layer write is `false`
- review queue item created is `false`
- production review queue item created is `false`
- production case created is `false`
- production `analysis_run` created is `false`
- frontend/route/API changed is `false`

No original row file, collector output, exchange directory, Evidence Layer record, frontend state, or runtime review queue state is an approved source for this gate.

## C. Evidence Candidate Completion Definition

A completed evidence-candidate-shaped checkpoint must satisfy all of these:

- exact 8W-10 approval was used in the prior implementation phase
- input source was an already-existing 8W-7 preview object
- no additional evidence rows were parsed
- candidate set schema is correct
- candidate count is bounded
- candidates are redacted
- warning/manual-review state is preserved
- output remains local-only and human-review-only
- production/public/frontend/delivery side effects are false

8W-10 satisfies these conditions for a local boundary checkpoint, not for review queue runtime or production import readiness.

## D. Review Queue Gate Definition

A Review Queue gate decision is a future docs-only checkpoint. It may define whether a later implementation could transform local evidence-candidate-shaped boundary objects into review-queue-candidate-shaped boundary objects.

A Review Queue gate decision may define:

- allowed source object
- review-queue-candidate schema boundaries
- warning/manual-review carry-forward
- exact future approval phrase
- no-production-write boundary
- blocker categories
- validation scope

It must not create review queue items.

## E. Review Queue Implementation Separation

Review Queue implementation is a separate future phase, if ever approved.

It may only be considered after:

- 8W-11 ready decision is committed
- a future 8W-12 docs-only gate explicitly allows considering implementation
- a separate exact implementation approval phrase is provided

Future implementation must remain:

- backend-only unless a later separate route/UI gate exists
- test-first
- local-only
- candidate-derived only
- bounded
- redacted
- human-review-only
- no Evidence Layer write
- no production review queue item creation

## F. Evidence Candidate Is Not EvidenceItem

An Evidence Candidate is not an EvidenceItem.

It must not:

- use production EvidenceItem schema as if it were imported evidence
- create EvidenceItems
- write Evidence Layer
- count as analysis input
- be treated as verified
- upgrade trust labels
- remove warning/manual-review state
- become public/customer output

Any EvidenceItem creation requires a later separate gate.

## G. Evidence Candidate Is Not Evidence Layer Import

Evidence Candidate completion and Review Queue gate are not Evidence Layer import.

They must not:

- write Evidence Layer
- create production EvidenceItems
- run production dedup
- approve analysis input
- generate analysis results
- generate reports
- generate public/customer outputs

Any Evidence Layer import requires a later separate import gate.

## H. Evidence Candidate Is Not Review Queue Runtime

Evidence Candidate completion and Review Queue gate must not create:

- review queue runtime
- review queue items
- production review queue items
- review actions
- review audit timeline

Human-review-required labels are boundary metadata only. They do not create review queue state.

## I. Warning/manual-review Handling

The 8W-10 warning/manual-review state must carry forward:

- `warning_count = 1`
- `human_review_required = true`
- `candidate_set_status = evidence_candidate_set_warn_manual_review_required`

This warning state must not be interpreted as trust upgrade, verification, review queue readiness, production readiness, analysis readiness, report readiness, or public/customer readiness.

## J. Allowed Future 8W-12 Docs-only Inputs

Future 8W-12 may inspect only:

- 8W-10 health report summaries
- 8W-10 helper/test contracts
- 8W-10 candidate set schema
- 8W-9/8W-10/8W-11 governance docs
- safe counts and status fields

Future 8W-12 must not inspect:

- `evidence_items.jsonl` content again
- `evidence_items.csv`
- source manifest rows
- collection log rows
- original package rows
- raw comments
- raw identities
- private collector source
- private collector project
- real exchange directories
- env-provided real paths

## K. Forbidden Current and Future Actions

Current 8W-11 and future 8W-12 must not:

- implement Review Queue helper logic
- create review queue items
- create production review queue items
- create EvidenceItems
- write Evidence Layer
- create production case
- create production `analysis_run`
- add frontend/route/API
- generate B-end report runtime
- generate Sandbox/public event runtime
- generate report/export/download/public/final-delivery runtime
- create public URL or signed URL
- create file-byte route
- generate response text
- publish, send, post, execute, or auto-execute
- call real APIs
- call real LLMs
- run provider or collector jobs
- fetch URLs
- scrape
- inspect private collector source
- read real exchange directories
- parse additional row files

## L. Future Blocker Categories

Any future Review Queue helper implementation design must block on:

- missing exact approval phrase
- wrong source schema
- wrong source phase
- wrong approved candidate set identity
- dropped warning/manual-review state
- unbounded candidate count
- raw author identifier exposure
- author name exposure
- profile URL exposure
- raw comment exposure
- secret/cookie/token/session/password/API key exposure
- absolute path or package path exposure
- private collector source request
- real exchange directory request
- arbitrary file path request
- new row parsing request outside the approved input contract
- Evidence Layer write request
- EvidenceItem creation request
- review queue item creation request outside the approved future helper boundary
- production review queue item creation request
- production case request
- production `analysis_run` request
- frontend/route/API request
- B-end report or Sandbox/public event request
- public/customer output request
- generated response text request
- publish/send/post/execute request
- real API/LLM/provider/collector request
- URL fetch or scrape request

## M. Future Redaction/minimization Carry-forward Principles

Future review-queue-candidate-shaped objects, if ever approved, must carry forward:

- safe candidate id
- source candidate schema and id
- evidence id hash, not raw unsafe identifiers
- safe type/platform/status labels
- coarse dates only
- redacted snippets only
- redaction warnings
- warning/manual-review state
- preview-only/human-review-only boundary flags

They must not carry forward:

- raw author IDs
- author names/usernames/display names
- profile URLs
- raw comments
- private messages
- email, phone, address, or identity fields
- cookies, tokens, sessions, passwords, API keys, secrets
- absolute paths
- package paths
- raw collector paths
- generated response text
- persuasion score
- truth score
- official verified fields
- prediction probability
- psychological profile
- personality diagnosis

## N. Evidence Layer / Production Boundary

Evidence Candidate completion and Review Queue gate are not Evidence Layer import.

They must not:

- write Evidence Layer
- create production EvidenceItems
- run production dedup
- approve analysis input
- generate analysis results
- generate reports
- generate public/customer outputs

Any Evidence Layer import would require a later separate gate.

## O. Review Queue / Case / Analysis Run Boundary

Evidence Candidate completion and Review Queue gate must not create:

- review queue runtime
- review queue items
- production review queue items
- production case
- production `analysis_run`
- manual analysis trigger

Any future review queue behavior requires separate governance phases.

## P. Approval Protocol

8W-11 does not approve 8W-13.

Future 8W-12 may be a docs-only gate decision. If a future 8W-13 implementation is ever reached, it must require a separate exact approval phrase such as:

`批准 8W-13 Controlled Review Queue Candidate Helper Implementation`

This phrase is a placeholder only. It is not current approval.

## Q. Forbidden Interpretations

Do not interpret this contract as:

- approval to implement Review Queue logic
- approval to create review queue items
- approval to create production review queue items
- approval to create EvidenceItems
- approval to write Evidence Layer
- approval to create production case
- approval to create production `analysis_run`
- approval to add route/frontend/API
- approval to generate B-end report runtime
- approval to generate Sandbox/public event runtime
- approval to generate public/customer output
- approval to parse more rows
- approval to inspect private collector source
- approval to read real exchange directories
- official verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof
- prediction
- production score

The current decision only allows a future 8W-12 docs-only Review Queue gate decision.
