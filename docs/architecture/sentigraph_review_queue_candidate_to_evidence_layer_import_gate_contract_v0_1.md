# Sentigraph Review Queue Candidate to Evidence Layer Import Gate Contract v0.1

## A. Contract Purpose

This contract defines the governance boundary between the 8W-13 local review-queue-candidate-shaped boundary objects and any future Evidence Layer Import gate.

This contract is docs-only. It does not implement Evidence Layer import helper logic, does not create Evidence Layer Import Candidates, does not create EvidenceItems, does not write Evidence Layer, does not create Review Queue Items, does not create production review queue items, does not create production case, does not create production `analysis_run`, does not create route/frontend/API, and does not parse additional row files.

## B. Source Object Allowed from 8W-13

The only possible future source object for an Evidence Layer Import gate discussion is the 8W-13 local review queue candidate set output:

`sentigraph_controlled_review_queue_candidate_set_v0_1`

Required source state:

- 8W-13 decision is `ready`
- review queue candidate set status is `review_queue_candidate_set_warn_manual_review_required`
- review queue candidate item schema is `sentigraph_controlled_review_queue_candidate_v0_1`
- review queue candidate count is `5`
- source evidence candidate count is `5`
- warning count is `1`
- human review required is `true`
- preview only is `true`
- queue candidate only is `true`
- candidates are redacted and evidence-candidate-derived
- Review Queue Items created is `false`
- production review queue items created is `false`
- EvidenceItems created is `false`
- Evidence Layer write is `false`
- production case created is `false`
- production `analysis_run` created is `false`
- frontend/route/API changed is `false`

No original row file, collector output, exchange directory, Evidence Layer record, production review queue state, frontend state, route state, or customer-facing output is an approved source for this gate.

## C. Review Queue Candidate Completion Definition

A completed review-queue-candidate-shaped checkpoint must satisfy all of these:

- exact 8W-13 approval was used in the prior implementation phase
- input source was an already-existing 8W-10 evidence candidate set object
- no additional evidence rows were parsed
- review queue candidate set schema is correct
- candidate count is bounded
- candidates are redacted
- warning/manual-review state is preserved
- output remains local-only and human-review-only
- output remains queue-candidate-only
- production/public/frontend/delivery side effects are false

8W-13 satisfies these conditions for a local boundary checkpoint, not for Evidence Layer import readiness or production import readiness.

## D. Evidence Layer Import Gate Definition

An Evidence Layer Import gate decision is a future docs-only checkpoint. It may define whether a later implementation could transform local review-queue-candidate-shaped boundary objects into evidence-layer-import-candidate-shaped boundary objects.

An Evidence Layer Import gate decision may define:

- allowed source object
- evidence-layer-import-candidate schema boundaries
- warning/manual-review carry-forward
- no-production-write boundary
- blocker categories
- validation scope
- future exact approval protocol

It must not create EvidenceItems and must not write Evidence Layer.

## E. Evidence Layer Import Implementation Separation

Evidence Layer Import implementation is a separate future phase, if ever approved.

It may only be considered after:

- 8W-14 ready decision is committed
- a future 8W-15 docs-only gate explicitly allows considering implementation
- a separate exact implementation approval phrase is provided in that future phase

Future implementation must remain:

- backend-only unless a later separate route/UI gate exists
- test-first
- local-only
- review-queue-candidate-derived only
- bounded
- redacted
- human-review-only
- no automatic trust upgrade
- no production case creation
- no production `analysis_run` creation

## F. Review Queue Candidate is not EvidenceItem

A Review Queue Candidate is not an EvidenceItem.

It must not:

- use production EvidenceItem schema as if it were imported evidence
- create EvidenceItems
- write Evidence Layer
- count as analysis input
- be treated as verified
- upgrade trust labels
- remove warning/manual-review state
- become public/customer output

Any EvidenceItem creation requires a later separate import gate and explicit implementation approval.

## G. Review Queue Candidate is not Evidence Layer Import

Review Queue Candidate completion and Evidence Layer Import gate are not Evidence Layer import.

They must not:

- write Evidence Layer
- create production EvidenceItems
- run production dedup
- approve analysis input
- generate analysis results
- generate reports
- generate public/customer outputs

Any Evidence Layer import requires a later separate implementation gate.

## H. Review Queue Candidate is not Production Review Queue Item

Review Queue Candidate completion and Evidence Layer Import gate must not create:

- review queue runtime
- Review Queue Items
- production review queue items
- review actions
- reviewer assignments
- review decisions
- review audit timelines

Human-review-required labels are boundary metadata only. They do not create review queue state.

## I. Review Queue Candidate is not Production Case / analysis_run Input

A Review Queue Candidate must not be treated as:

- production case data
- production `analysis_run` input
- analysis-ready evidence
- report-ready evidence
- public event evidence
- B-end report evidence
- Sandbox runtime evidence

Any future production case, `analysis_run`, report, Sandbox, or public event transition requires separate governance gates.

## J. Warning/manual-review Handling

The 8W-13 warning/manual-review state must carry forward:

- `warning_count = 1`
- `human_review_required = true`
- `review_queue_candidate_set_status = review_queue_candidate_set_warn_manual_review_required`

This warning state must not be interpreted as trust upgrade, verification, Evidence Layer readiness, production readiness, analysis readiness, report readiness, or public/customer readiness.

## K. Allowed Future 8W-15 Docs-only Inputs

Future 8W-15 may inspect only:

- 8W-13 health report summaries
- 8W-13 helper/test contracts
- 8W-13 review queue candidate set schema
- 8W-12/8W-13/8W-14 governance docs
- safe counts and status fields

Future 8W-15 must not inspect:

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

## L. Forbidden Current and Future Actions

Current 8W-14 and future 8W-15 must not:

- implement Evidence Layer Import helper logic
- create Evidence Layer Import Candidates
- create EvidenceItems
- write Evidence Layer
- create Review Queue Items
- create production review queue items
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

## M. Future Blocker Categories

Any future Evidence Layer Import Candidate helper design must block on:

- missing exact approval phrase
- wrong source schema
- wrong source phase
- wrong source status
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
- EvidenceItem creation request without explicit implementation approval
- Evidence Layer write request without explicit implementation approval
- Review Queue Item creation request
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

## N. Future Redaction/minimization Carry-forward Principles

Future evidence-layer-import-candidate-shaped objects, if ever approved, must carry forward:

- safe candidate id
- source review queue candidate schema and id
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
- review action state
- production review queue item ids
- production EvidenceItem ids

## O. Evidence Layer / Production Boundary

Review Queue Candidate completion and Evidence Layer Import gate are not Evidence Layer import.

They must not:

- write Evidence Layer
- create production EvidenceItems
- run production dedup
- approve analysis input
- generate analysis results
- generate reports
- generate public/customer outputs

Any Evidence Layer import would require a later separate gate and implementation approval.

## P. Approval Protocol

8W-14 does not approve 8W-15 implementation work.

Future 8W-15 may be a docs-only Evidence Layer Import gate decision. If a future implementation is ever reached, its exact approval phrase must be defined by that later gate and must not be inferred from 8W-14.

This contract contains no active implementation approval phrase.

## Q. Forbidden Interpretations

Do not interpret this contract as:

- approval to implement Evidence Layer Import logic
- approval to create Evidence Layer Import Candidates
- approval to create EvidenceItems
- approval to write Evidence Layer
- approval to create Review Queue Items
- approval to create production review queue items
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

The current decision only allows a future 8W-15 docs-only Evidence Layer Import gate decision.
