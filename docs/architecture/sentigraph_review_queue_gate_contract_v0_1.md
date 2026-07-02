# Sentigraph Review Queue Gate Contract v0.1

## A. Contract Purpose

This contract defines the governance boundary between the 8W-10 local evidence-candidate-shaped boundary objects, the 8W-11 completion decision, and any future review-queue-candidate-shaped local boundary object.

This contract is docs-only. It does not implement a Review Queue Candidate helper, does not create Review Queue Candidates, does not create Review Queue Items, does not write Evidence Layer, does not create EvidenceItems, does not create production case, does not create production `analysis_run`, does not add route/frontend/API, and does not parse additional row files.

## B. Source Object Allowed from 8W-10 / 8W-11

The only allowed future source object for a Review Queue Candidate gate is the 8W-10 local candidate set output accepted by 8W-11:

`sentigraph_controlled_evidence_candidate_set_v0_1`

Required source state:

- 8W-11 decision is `ready`.
- 8W-11 selected next boundary is `ready_for_8W_12_review_queue_gate_decision_docs_only`.
- 8W-10 candidate set status is `evidence_candidate_set_warn_manual_review_required`.
- candidate item schema is `sentigraph_controlled_evidence_candidate_v0_1`.
- candidate count is `5`.
- source preview rows count is `5`.
- warning count is `1`.
- human review required is `true`.
- preview-only is `true`.
- candidates are bounded, redacted, and preview-derived.
- EvidenceItems created is `false`.
- Evidence Layer write is `false`.
- Review Queue Item created is `false`.
- production review queue item created is `false`.
- production case created is `false`.
- production `analysis_run` created is `false`.
- frontend/route/API changed is `false`.

No original row file, collector output, exchange directory, Evidence Layer record, frontend state, runtime review queue state, public route, or customer-facing output is an approved source for this gate.

## C. Future Local Review-queue-candidate-shaped Object Definition

A future review-queue-candidate-shaped object, if ever approved, may be a local backend boundary object derived only from an eligible 8W-10 evidence candidate.

Suggested future schema name:

`sentigraph_controlled_review_queue_candidate_v0_1`

Suggested future candidate set schema name:

`sentigraph_controlled_review_queue_candidate_set_v0_1`

Allowed future fields may include:

- schema.
- phase.
- local review queue candidate id.
- source evidence candidate id.
- source candidate set schema.
- source evidence id hash.
- platform label.
- evidence type label.
- coarse created date.
- trust label.
- verification status.
- review status.
- redacted snippet.
- warning labels.
- blocker codes.
- human review required flag.
- preview-only flag.
- queue-candidate-only boundary flag.
- runtime side-effect flags, all false.

The future object must preserve human-review-only and warning/manual-review state. It must not be promoted into runtime review queue state by construction.

## D. Review Queue Candidate is not Review Queue Item

A Review Queue Candidate is not a Review Queue Item.

Review Queue Candidate means:

- local backend boundary object.
- candidate-shaped only.
- evidence-candidate-derived only.
- human-review-only.
- no runtime queue state.
- no review action state.
- no audit timeline state.

Review Queue Item means:

- runtime review workflow state.
- not approved by 8W-12.
- not created by a candidate helper.
- requires a later separate Review Queue runtime gate if ever considered.

The future candidate helper, if ever approved, must not create Review Queue Items or production review queue items.

## E. Review Queue Candidate is not EvidenceItem

A Review Queue Candidate is not an EvidenceItem.

It must not:

- use production EvidenceItem schema as if imported.
- create EvidenceItems.
- write Evidence Layer.
- count as analysis input.
- be treated as verified.
- upgrade trust labels.
- remove warning/manual-review state.
- become public/customer output.

Any EvidenceItem creation requires a later separate Evidence Layer import gate.

## F. Review Queue Candidate is not Evidence Layer Import

Review Queue Candidate creation, if ever approved, is not Evidence Layer import.

It must not:

- write Evidence Layer.
- create production EvidenceItems.
- run production dedup.
- approve analysis input.
- generate analysis results.
- generate reports.
- generate public/customer outputs.

Any Evidence Layer import requires a later separate import gate.

## G. Review Queue Candidate is not Production Review Queue Item

Review Queue Candidate creation, if ever approved, must remain outside production review queue runtime.

It must not create:

- production review queue items.
- review action records.
- review audit timeline records.
- reviewer assignment records.
- approval or rejection decisions.
- queue completion gates.

Human-review-required labels are boundary metadata only. They do not create review queue state.

## H. Redaction/minimization Carry-forward

Future review-queue-candidate-shaped objects must carry forward only safe minimized fields from 8W-10 evidence candidates.

Allowed carry-forward categories:

- safe ids and hashes.
- source schema/status labels.
- platform and evidence type labels.
- coarse dates.
- trust, verification, and review status labels.
- redacted snippets.
- warning labels and blocker codes.
- human-review-only and preview-only flags.

Forbidden carry-forward categories:

- raw author IDs.
- raw author names.
- usernames, display names, or profile URLs.
- raw comments.
- private messages.
- email, phone, address, or identity fields.
- cookies, tokens, sessions, passwords, API keys, secrets, or salts.
- browser profile paths.
- absolute paths or package paths.
- raw collector paths.
- real exchange paths.
- generated response text.
- target user lists.
- persuasion score.
- truth score.
- official verified fields.
- prediction probability.
- psychological profile.
- personality diagnosis.

## I. Warning/manual-review Carry-forward

The 8W-10 warning/manual-review state must carry forward into any future review-queue-candidate-shaped object:

- `warning_count = 1`.
- `human_review_required = true`.
- `candidate_set_status = evidence_candidate_set_warn_manual_review_required`.

The future object must not downgrade, hide, or remove warning/manual-review state. A warning state must not be interpreted as trust upgrade, verification, review completion, production readiness, analysis readiness, report readiness, or public/customer readiness.

## J. Future Blocker Categories

Any future Review Queue Candidate helper design or implementation must block on:

- missing exact approval phrase.
- wrong source schema.
- wrong source phase.
- wrong source status.
- dropped warning/manual-review state.
- unbounded candidate count.
- raw author identifier exposure.
- author name exposure.
- profile URL exposure.
- raw comment exposure.
- secret, cookie, token, session, password, API key, or salt exposure.
- absolute path or package path exposure.
- private collector source request.
- real exchange directory request.
- arbitrary file path request.
- new row parsing request outside the approved input contract.
- Evidence Layer write request.
- EvidenceItem creation request.
- Review Queue Item creation request.
- production review queue item creation request.
- production case request.
- production `analysis_run` request.
- route/frontend/API request.
- B-end report or Sandbox/public event request.
- public/customer output request.
- generated response text request.
- publish/send/post/execute request.
- real API, real LLM, provider job, or collector job request.
- URL fetch or scrape request.

Blocked outputs must remain safe summaries with all runtime side-effect flags false.

## K. Future Test Expectations

Future 8W-13 tests, if ever approved, should prove:

- exact approval phrase is required.
- missing/wrong/mojibake approval phrase blocks before any candidate conversion.
- source schema must be `sentigraph_controlled_evidence_candidate_set_v0_1`.
- source status must preserve `evidence_candidate_set_warn_manual_review_required`.
- candidate count remains bounded.
- warning count and human review required are preserved.
- only redacted snippets and safe labels are emitted.
- forbidden identity, secret, path, and raw text fields are blocked or omitted.
- no file opening occurs.
- no additional row parsing occurs.
- no `evidence_items.jsonl` or CSV parsing occurs.
- no source manifest or collection log rows are parsed.
- no private collector source is inspected.
- no real exchange directory is read.
- no EvidenceItems are created.
- no Evidence Layer write occurs.
- no Review Queue Items are created.
- no production case or production `analysis_run` is created.
- no route/API/frontend behavior is added.
- no report, Sandbox, public event, download, public access, external delivery, or final delivery behavior is triggered.
- runtime side-effect flags remain false.

## L. Approval Protocol

8W-12 does not approve 8W-13.

If a future 8W-13 implementation task is proposed, it must require this exact approval phrase:

`批准 8W-13 Controlled Review Queue Candidate Helper Implementation`

This phrase is a future placeholder only. It is not current approval.

The future implementation must be a separate task and must remain backend-only, test-first, local-only, evidence-candidate-derived only, bounded, redacted, and human-review-only.

## M. Evidence Layer / Production Boundary

Review Queue Candidate gate and any future Review Queue Candidate helper are not Evidence Layer import.

They must not:

- write Evidence Layer.
- create production EvidenceItems.
- run production dedup.
- approve analysis input.
- create production case.
- create production `analysis_run`.
- generate analysis results.
- generate reports.
- generate Sandbox/public event outputs.
- create public/customer outputs.
- create public URLs, signed URLs, downloads, public access, external delivery, or final delivery.

Any production transition requires a later separate gate and exact approval.

## N. Forbidden Interpretations

Do not interpret this contract as:

- approval to implement Review Queue Candidate helper logic.
- approval to create Review Queue Candidates.
- approval to create Review Queue Items.
- approval to create production review queue items.
- approval to create EvidenceItems.
- approval to write Evidence Layer.
- approval to create production case.
- approval to create production `analysis_run`.
- approval to add route/frontend/API.
- approval to generate B-end report runtime.
- approval to generate Sandbox/public event runtime.
- approval to generate public/customer output.
- approval to parse more rows.
- approval to inspect private collector source.
- approval to read real exchange directories.
- official verification.
- full-web coverage.
- full-platform coverage.
- full-thread coverage.
- causal proof.
- prediction.
- production score.

The current decision only allows a future 8W-13 implementation task to be considered after separate exact approval.
