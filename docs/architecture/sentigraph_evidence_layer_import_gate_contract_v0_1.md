# Sentigraph Evidence Layer Import Gate Contract v0.1

## A. Contract Purpose

This contract defines the 8W-15 docs-only boundary for considering a future Evidence Layer Import Candidate helper.

It does not implement helper logic, create Evidence Layer Import Candidates, create EvidenceItems, write Evidence Layer, create production cases, create production `analysis_run` records, create Review Queue Items, create production review queue items, add route/API/frontend behavior, generate reports, generate Sandbox/public event outputs, or parse additional row files.

The contract exists to prevent local review-queue-candidate-shaped boundary objects from being misread as production evidence.

## B. Source Object Allowed from 8W-13 / 8W-14

The only allowed source for a future Evidence Layer Import Candidate helper discussion is the 8W-13 local review queue candidate set already accepted by 8W-14:

`sentigraph_controlled_review_queue_candidate_set_v0_1`

Required source facts:

- 8W-13 decision is `ready`
- 8W-14 decision is `ready`
- 8W-14 selected `ready_for_8W_15_evidence_layer_import_gate_decision_docs_only`
- review queue candidate set status is `review_queue_candidate_set_warn_manual_review_required`
- review queue candidate item schema is `sentigraph_controlled_review_queue_candidate_v0_1`
- review queue candidate count is `5`
- source evidence candidate count is `5`
- warning count is `1`
- human review required is `yes`
- EvidenceItems created is `false`
- Evidence Layer write is `false`
- Review Queue Items created is `false`
- production review queue items created is `false`
- production cases created is `false`
- production `analysis_run` records created is `false`
- route/API/frontend behavior added is `false`
- additional row parsing performed is `false`

No original row file, collector raw output, exchange directory, Evidence Layer record, production review queue state, frontend state, route state, public URL, signed URL, download package, external delivery, final delivery, or customer-facing output is an approved source for this gate.

## C. Future Local Evidence-layer-import-candidate-shaped Object Definition

A future Evidence Layer Import Candidate helper, if explicitly approved, may create local evidence-layer-import-candidate-shaped boundary objects with a schema similar to:

`sentigraph_controlled_evidence_layer_import_candidate_set_v0_1`

Candidate set fields should include only safe, minimized metadata:

- candidate set schema
- candidate set id
- source review queue candidate set schema
- source review queue candidate set status
- evidence layer import candidate count
- source review queue candidate count
- warning count
- human review required
- selected sample boundary
- import blocker list
- safety flags
- production side-effect flags
- candidate item summaries

Candidate item fields should be derived only from safe review-queue-candidate fields:

- candidate schema
- candidate id
- source review queue candidate id
- source evidence candidate id
- preview hash
- source URL presence flag or already-safe source URL field if present in the source candidate
- title or label preview if already redacted and safe
- redacted text snippet if already present in the source candidate
- redaction status
- warning labels
- human review required flag
- trust boundary label
- import readiness blocker list
- no-production-side-effect flags

The helper must not inspect or reconstruct raw comments, raw identities, private collector rows, real exchange directory content, original package rows, `evidence_items.jsonl`, `evidence_items.csv`, `source_manifest.jsonl`, or `collection_log.jsonl`.

## D. Evidence Layer Import Candidate is not EvidenceItem

An Evidence Layer Import Candidate is not an EvidenceItem.

It must not:

- use the production EvidenceItem schema as if imported
- create EvidenceItems
- create production EvidenceItems
- obtain EvidenceItem ids
- imply source verification
- imply trust upgrade
- imply Evidence Layer readiness
- imply analysis readiness

Any EvidenceItem creation requires a later separate gate and explicit implementation approval.

## E. Evidence Layer Import Candidate is not Evidence Layer Write

Evidence Layer Import Candidate creation, if ever approved, is still not Evidence Layer write.

It must not:

- write Evidence Layer
- mutate Evidence Layer state
- persist production evidence
- set production evidence ids
- mark evidence as imported
- mark evidence as analysis-included
- mark evidence as report-ready

Any Evidence Layer write requires a later separate gate and explicit implementation approval.

## F. Evidence Layer Import Candidate is not Production EvidenceItem

The candidate object must remain local, bounded, and non-production.

It is not a production EvidenceItem, not a production import, not a production review artifact, not a production case artifact, and not production `analysis_run` input.

If a future helper emits ids, those ids must be candidate ids only. They must not be EvidenceItem ids, production review queue item ids, production case ids, production `analysis_run` ids, report ids, Sandbox ids, public event ids, download ids, public access ids, or delivery ids.

## G. Evidence Layer Import Candidate is not Production Case / analysis_run Input

Evidence Layer Import Candidates must not be treated as:

- production case input
- production `analysis_run` input
- analysis-ready evidence
- report-ready evidence
- B-end report runtime input
- Sandbox/public event runtime input
- generated response input
- customer-facing output

Any future production case, production `analysis_run`, report, Sandbox, public event, export, download, public access, external delivery, or final delivery transition requires a separate gate.

## H. Evidence Layer Import Candidate is not Analysis-ready Evidence

Candidate creation must not produce analysis readiness.

The future helper must preserve:

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

## I. Redaction / Minimization Carry-forward

Future candidate objects must carry forward the same minimization posture as 8W-10 and 8W-13.

Allowed safe fields are only those already present in the local review queue candidate object and already redacted or minimized.

Forbidden fields include:

- raw author id
- raw author name
- profile URL
- private message
- email
- phone
- token
- cookie
- session
- password-like value
- API key
- raw comment body beyond existing redacted preview
- original package row content
- collector raw row content

Any detection of forbidden fields must block candidate creation.

## J. Warning / Manual-review Carry-forward

The source warning state is part of the contract:

- `warning_count = 1`
- `human_review_required = true`
- `review_queue_candidate_set_status = review_queue_candidate_set_warn_manual_review_required`

A future helper must preserve this warning state and surface it in the candidate set.

The warning state must not be cleared by transformation and must not be used as evidence verification, trust upgrade, Evidence Layer readiness, production readiness, analysis readiness, report readiness, public readiness, or customer readiness.

## K. Future Blocker Categories

Any future helper must block on:

- missing exact approval phrase
- wrong exact approval phrase
- mojibake approval phrase
- source schema mismatch
- source status mismatch
- warning/manual-review state missing
- human review required flag missing
- candidate count mismatch
- forbidden raw identity field
- forbidden secret-like field
- source object already marked as EvidenceItem
- source object already marked as Evidence Layer write
- source object already marked as production case
- source object already marked as production `analysis_run`
- request to parse `evidence_items.jsonl`
- request to parse `evidence_items.csv`
- request to parse `source_manifest.jsonl`
- request to parse `collection_log.jsonl`
- request to inspect private collector source
- request to read real exchange directory
- request to fetch URL or scrape page
- request to call real API or real LLM
- request to create route/API/frontend behavior
- request to generate B-end report, Sandbox/public event, download package, public access, external delivery, or final delivery

## L. Future Test Expectations

If 8W-16 is explicitly approved, tests should prove:

- exact approval phrase is required before candidate creation
- mojibake approval phrase is rejected
- missing approval phrase is rejected
- wrong approval phrase is rejected
- source schema mismatch blocks
- source status mismatch blocks
- warning count must remain `1`
- human review required must remain true
- candidate count must match source count
- forbidden raw identity fields block
- forbidden secret-like fields block
- EvidenceItem fields are not produced
- Evidence Layer write flags remain false
- production case flags remain false
- production `analysis_run` flags remain false
- Review Queue Item flags remain false
- route/API/frontend flags remain false
- B-end report, Sandbox/public event, download, public access, external delivery, and final delivery flags remain false
- no additional row parsing is performed
- no private collector source is inspected
- no real exchange directory is read
- no real API or real LLM is called
- safe summary excludes redacted snippet bodies unless explicitly allowed by the safe summary contract

## M. Approval Protocol

Future 8W-16, if requested, must require this exact approval phrase:

`批准 8W-16 Controlled Evidence Layer Import Candidate Helper Implementation`

This phrase is not active implementation approval in 8W-15.

8W-15 only defines the future approval phrase and the boundaries a future implementation must preserve.

## N. Evidence Layer / Production Boundary

Evidence Layer Import Candidate creation is still outside Evidence Layer.

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

The first future helper may only create local candidate-shaped boundary objects if explicitly approved.

## O. Forbidden Interpretations

This contract must not be interpreted as:

- approval to implement Evidence Layer Import logic now
- approval to create Evidence Layer Import Candidates now
- approval to create EvidenceItems
- approval to write Evidence Layer
- approval to create production EvidenceItems
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

The only approved next boundary is a future explicitly approved, backend-only, local-only, test-first Evidence Layer Import Candidate helper consideration.
