# Sentigraph Controlled Evidence Candidate Gate Contract v0.1

## A. Contract Purpose

This contract defines the governance boundary for any future Evidence Candidate helper that might derive local candidate-shaped objects from the 8W-7 controlled redacted row preview.

This contract is docs-only. It does not implement Evidence Candidate creation, does not write Evidence Layer, does not create EvidenceItems, does not create review queue runtime, does not create production case, does not create production `analysis_run`, does not create route/frontend/API, and does not parse additional row files.

## B. Source Object Allowed from 8W-7 / 8W-8

The only allowed future source object is the 8W-7 redacted preview output already accepted by 8W-8:

`sentigraph_controlled_row_preview_v0_1`

Required source state:

- 8W-8 decision is `ready`
- 8W-8 selected `ready_for_8W_9_controlled_evidence_candidate_gate_decision_docs_only`
- source schema is `sentigraph_controlled_row_preview_v0_1`
- source phase is `8W-7`
- `preview_status = row_preview_warn_manual_review_required`
- `preview_rows_count = 5`
- `rows_inspected_count = 5`
- `row_limit_enforced = true`
- `row_source = evidence_items.jsonl`
- `warning_count = 1`
- `human_review_required = true`
- exact approval phrase is verified
- no raw author identifiers emitted
- no author names emitted
- no profile URLs emitted
- no raw comments emitted
- no secrets emitted
- no absolute path or package path emitted

No other package row file, collector output, exchange directory, or frontend state is an approved source for this gate.

## C. Future Local Evidence-candidate-shaped Object Definition

A future local evidence-candidate-shaped object, if separately approved, would be an intermediate backend-only governance object derived from safe preview rows.

It may include only safe candidate fields such as:

- candidate schema
- candidate id
- source preview row id
- source preview schema
- evidence id hash
- platform label
- evidence type label
- coarse created date
- trust label
- verification status
- review status
- redacted snippet
- warning labels
- human-review-required flag
- boundary flags
- safe blocker or warning codes

It must remain preview-derived, bounded, redacted, and human-review-only.

## D. Candidate Is Not EvidenceItem

An Evidence Candidate is not an EvidenceItem.

It must not:

- use the production EvidenceItem schema as if it were imported evidence
- create EvidenceItems
- write Evidence Layer
- count as analysis input
- be treated as verified
- upgrade trust labels
- remove warning/manual-review state
- become public/customer output

Any EvidenceItem creation requires a later separate gate.

## E. Candidate Is Not Evidence Layer Import

Evidence Candidate gate and future helper implementation are not Evidence Layer import.

They must not:

- write Evidence Layer
- create production EvidenceItems
- run production dedup
- approve analysis input
- generate analysis results
- generate reports
- generate public/customer outputs

Any Evidence Layer import requires a later separate import gate.

## F. Candidate Is Not Review Queue Runtime

Evidence Candidate gate and future helper implementation must not create:

- review queue runtime
- review queue items
- production review queue items
- review actions
- review audit timeline

Human-review-required labels in candidate-shaped objects are boundary metadata only. They do not create review queue state.

## G. Candidate Is Not Production Case / Production Analysis Run

Evidence Candidate gate and future helper implementation must not create:

- production case
- production `analysis_run`
- manual analysis trigger
- analysis result
- report candidate
- final report
- Sandbox fixture
- public event page

Any transition to production case or production analysis run requires a later separate governance phase.

## H. Redaction/minimization Carry-forward

Future candidate-shaped objects, if ever approved, must carry forward:

- safe evidence id hash, not raw identifiers
- bounded preview row id
- bounded row index if needed
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
- cookies, tokens, sessions, passwords, API keys, secrets, or salts
- absolute paths
- package paths
- raw collector paths
- generated response text
- target user lists
- persuasion score
- truth score
- official verified fields
- prediction probability
- psychological profile
- personality diagnosis

## I. Future Blocker Categories

Any future Evidence Candidate helper implementation must block on:

- missing exact approval phrase
- wrong source schema
- wrong source phase
- wrong 8W-8 decision
- wrong approved package identity
- dropped warning/manual-review state
- unbounded candidate count
- raw author identifier exposure
- author name exposure
- profile URL exposure
- raw comment exposure
- secret/cookie/token/session/password/API key/salt exposure
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

## J. Future Test Expectations

Future 8W-10 tests, if approved, should prove:

- exact future approval phrase is required
- wrong phrase blocks before candidate creation
- candidate output uses the correct schema
- candidate output is derived only from approved preview rows
- warning/manual-review state is preserved
- candidate count is bounded by source preview count
- raw identifiers are not emitted
- author names are not emitted
- profile URLs are not emitted
- raw comments are not emitted
- secrets are not emitted
- absolute paths and package paths are not emitted
- EvidenceItems are not created
- Evidence Layer is not written
- review queue runtime is not created
- production case is not created
- production `analysis_run` is not created
- frontend/route/API is not added
- no private collector source is inspected
- no real exchange directory is read
- no additional row files are parsed
- no real API, real LLM, provider job, collector job, URL fetch, or scrape occurs

## K. Approval Protocol

8W-9 does not approve 8W-10.

If future 8W-10 implementation is ever reached, it must require the exact approval phrase:

`批准 8W-10 Controlled Evidence Candidate Helper Implementation`

This phrase is a placeholder only. It is not current approval.

Future approval must be explicit in a later user task and must not be inferred from this contract.

## L. Forbidden Interpretations

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
- approval to generate report/export/download/public/final-delivery runtime
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

The current decision only allows a future 8W-10 implementation task to be considered after exact explicit approval.
