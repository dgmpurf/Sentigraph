# Sentigraph Row Preview to Evidence Candidate Gate Contract v0.1

## A. Contract Purpose

This contract defines the governance boundary between the 8W-7 controlled redacted row preview and any future Evidence Candidate gate.

This contract is docs-only. It does not implement Evidence Candidate creation, does not write Evidence Layer, does not create EvidenceItems, does not create review queue items, does not create production case, does not create production `analysis_run`, does not create route/frontend/API, and does not parse additional row files.

## B. 8W-7 Row Preview Object as Source

The only possible future source object for an Evidence Candidate gate discussion is the 8W-7 redacted preview output:

`sentigraph_controlled_row_preview_v0_1`

Verified 8W-7 source status:

- exact approval phrase verified: `yes`
- mojibake phrase present: `no`
- mojibake phrase rejected by test before row file opening: `yes`
- focused tests: `50 passed`
- nearby tests: `110 passed`

Expected 8W-7 summary fields:

- `preview_status = row_preview_warn_manual_review_required`
- `preview_rows_count = 5`
- `rows_inspected_count = 5`
- `row_limit_enforced = true`
- `row_source = evidence_items.jsonl`
- `warning_count = 1`
- `human_review_required = true`
- no raw author identifiers emitted
- no author names emitted
- no profile URLs emitted
- no raw comments emitted
- no secrets emitted
- no absolute path or package path emitted

8W-8 accepts row preview completion only as redacted preview-only / human-review-only.

## C. Row Preview Completion Definition

A completed controlled row preview checkpoint must satisfy all of these:

- exact approval phrase is correct and verified
- source is the 8W-4 review-only staging boundary marker
- target identity is the approved Dong/Sun sample package
- row source is JSONL only
- no additional row sources are parsed
- preview rows are bounded
- preview snippets are redacted and capped
- warning/manual-review state is preserved
- output remains preview-only and human-review-only
- production/public/frontend/delivery side effects are false

8W-7 satisfies these conditions for a preview-only checkpoint, not for production import or analysis readiness.

## D. Evidence Candidate Gate Definition

An Evidence Candidate gate decision is a future docs-only checkpoint. It may define whether a later implementation could transform redacted preview rows into local evidence-candidate-shaped objects.

An Evidence Candidate gate decision may define:

- allowed source object
- candidate schema boundaries
- redaction/minimization carry-forward
- exact future approval phrase
- no-production-write boundary
- blocker categories
- validation scope

It must not create Evidence Candidates.

## E. Evidence Candidate Implementation Separation

Evidence Candidate implementation is a separate future phase, if ever approved.

It may only be considered after:

- 8W-8 ready decision is committed
- a future 8W-9 docs-only gate explicitly allows considering implementation
- a separate exact implementation approval phrase is provided

Future implementation must remain:

- backend-only unless a later separate route/UI gate exists
- test-first
- local-only
- preview-derived only
- bounded
- redacted
- human-review-only

## F. Warning/manual-review Handling

The 8W-7 warning/manual-review state must carry forward:

- `warning_count = 1`
- `human_review_required = true`
- `preview_status = row_preview_warn_manual_review_required`

This warning state must not be interpreted as trust upgrade, verification, production readiness, analysis readiness, report readiness, or public/customer readiness.

## G. Allowed Future 8W-9 Docs-only Inputs

Future 8W-9 may inspect only:

- 8W-7 health report summaries
- 8W-7 helper/test contracts
- 8W-7 preview object schema
- 8W-6/8W-7/8W-8 governance docs
- safe counts and status fields

Future 8W-9 must not inspect:

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

## H. Forbidden Current and Future Actions

Current 8W-8 and future 8W-9 must not:

- implement Evidence Candidate helper logic
- create Evidence Candidates
- create EvidenceItems
- write Evidence Layer
- create review queue runtime
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

## I. Future Evidence Candidate Blocker Categories

Any future Evidence Candidate implementation design must block on:

- missing exact approval phrase
- wrong source schema
- wrong source phase
- wrong approved package identity
- dropped warning/manual-review state
- unbounded row count
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
- production EvidenceItem creation request
- production case request
- production `analysis_run` request
- review queue runtime request
- frontend/route/API request
- B-end report or Sandbox/public event request
- public/customer output request
- generated response text request
- publish/send/post/execute request
- real API/LLM/provider/collector request
- URL fetch or scrape request

## J. Future Redaction/minimization Carry-forward Principles

Future candidate-shaped objects, if ever approved, must carry forward:

- evidence id hash, not raw unsafe identifiers
- bounded row indices
- safe type/platform/status labels
- coarse dates only
- redacted text snippets only
- redaction warnings
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

## K. Evidence Layer / Production Boundary

Evidence Candidate gate and implementation are not Evidence Layer import.

They must not:

- write Evidence Layer
- create production EvidenceItems
- run production dedup
- approve analysis input
- generate analysis results
- generate reports
- generate public/customer outputs

Any Evidence Layer import would require a later separate gate.

## L. Review Queue / Case / Analysis Run Boundary

Evidence Candidate gate and implementation must not create:

- review queue runtime
- review queue items
- production review queue items
- production case
- production `analysis_run`
- manual analysis trigger

Any future review queue or case behavior requires separate governance phases.

## M. Private Collector / Exchange Boundary

Future Evidence Candidate gate work must not:

- inspect private collector source
- modify private collector project
- run collector jobs
- run provider jobs
- access collector sessions, cookies, tokens, profiles, browser state, or secrets
- accept external export roots
- accept env-provided real paths
- traverse real exchange directories
- parse private collector raw output

## N. Approval Protocol

8W-8 does not approve 8W-10.

Future 8W-9 may be a docs-only gate decision. If a future 8W-10 implementation is ever reached, it must require a separate exact approval phrase such as:

`批准 8W-10 Controlled Evidence Candidate Helper Implementation`

This phrase is a placeholder only. It is not current approval.

## O. Forbidden Interpretations

Do not interpret this contract as:

- approval to implement Evidence Candidate logic
- approval to create Evidence Candidates
- approval to create EvidenceItems
- approval to write Evidence Layer
- approval to create review queue runtime
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

The current decision only allows a future 8W-9 docs-only Evidence Candidate gate decision.
