# Sentigraph Controlled Row Preview Gate Contract v0.1

## A. Contract Purpose

This contract defines the future implementation boundary for a controlled row preview helper that may be considered after 8W-6.

This contract is docs-only. It does not implement row preview, does not open row files, does not parse `evidence_items.jsonl` or `evidence_items.csv`, does not read original package rows, does not write Evidence Layer, does not create production case, does not create production `analysis_run`, does not create route/frontend, and does not touch private collector or real exchange directories.

## B. Approved Package and Source Marker

The only future eligible package identity is:

- package_name: `donglu-sunjihai-youth-football-202606-v2_20260617_121016`
- package_role: `candidate_demo_sample`
- case_id_hint: `donglu_sunjihai_youth_football_202606`

The only future eligible source marker is the 8W-4 safe local review-only staging boundary marker:

- schema: `sentigraph_metadata_smoke_review_only_staging_boundary_v0_1`
- phase: `8W-4`
- boundary_status: `review_only_staging_boundary_ready_for_manual_review`
- metadata_only: `true`
- warning_count: `1`
- human_review_required: `true`
- warning_manual_review_preserved: `true`
- row_preview_approved: `false` before implementation starts
- Evidence Layer write: `false`
- production case: `false`
- production `analysis_run`: `false`

Future implementation must not accept arbitrary package names, paths, directories, URLs, env roots, collector output roots, or user-provided filesystem paths.

## C. Row Preview Implementation Separation

8W-6 is only a gate decision.

Row preview implementation is a separate later phase. It would mean code that:

- opens one explicitly approved row source
- reads only a bounded number of rows
- emits redacted preview-only rows
- preserves warning/manual-review state
- keeps all production side effects false

This contract does not approve that implementation now.

## D. Future Approval Protocol

Future implementation requires this exact approval phrase:

`批准 8W-7 Controlled Row Preview Implementation`

Without this exact phrase:

- do not create tests
- do not create backend helper
- do not open row files
- do not parse rows
- do not create preview rows
- do not write Evidence Layer
- do not create production case
- do not create production `analysis_run`
- do not add route/frontend/API
- do not generate report, Sandbox, public event, public/customer output, or delivery output

## E. Future Allowed Row Source

Recommended first-slice source:

`evidence_items.jsonl`

Alternative source:

`evidence_items.csv`, only if the future approval explicitly names CSV.

Future 8W-7 must parse only one source. It must not parse both JSONL and CSV unless a later gate explicitly approves dual-source comparison.

Future 8W-7 must not parse:

- `source_manifest.jsonl` rows
- `collection_log.jsonl` rows
- original package rows outside the approved evidence row file
- private collector raw output
- raw crawler output
- arbitrary user-provided files

## F. Future Row Minimization Policy

Future row preview must be minimized:

- default `max_preview_rows = 5`
- hard upper bound `max_preview_rows <= 10`
- row limit enforced before emitting preview output
- output preview-only and human-review-only
- no production scoring
- no public output
- no B-end report runtime use
- no Sandbox/public event runtime use
- no trust upgrade
- no official verification claim
- no full-web or full-platform claim

If a future helper cannot prove row-count enforcement, it must block.

## G. Future Redaction Policy

Future preview output must be redacted by default.

Required redaction behavior:

- raw author identifiers removed
- author names/usernames/display names removed
- actual profile URL values removed
- private messages skipped or blocked
- secrets/cookies/tokens/sessions/passwords/API keys blocked
- browser profile paths blocked
- absolute filesystem paths blocked
- package paths blocked
- raw collector paths blocked
- text snippets capped and redacted
- rows with doxxing, harassment, minors/family sensitive personal details, or private-message risk skipped or blocked

Blocked output must use safe reason codes only and must not echo forbidden values.

## H. Future Allowed Preview Fields

Future redacted preview rows may include only:

- `preview_row_id`
- `row_index`
- `evidence_id` or `evidence_id_hash` if safe
- `evidence_type`
- `platform`
- `created_at_date` or coarse `created_at` if safe
- `trust_label`
- `verification_status`
- `review_status`
- `language`
- `content_visibility` or `access_scope` if safe
- `text_snippet_redacted`
- `redaction_status`
- `redaction_warnings`
- `row_boundary_flags`

All fields must be preview-only and human-review-only.

## I. Future Forbidden Fields

Future preview rows must not include:

- `raw_author_id`
- `author_id`
- `author_name`
- `username`
- `display_name`
- actual `profile_url`
- raw profile URL
- private messages
- email
- phone
- address
- identity fields
- cookies
- tokens
- sessions
- passwords
- API keys
- secrets
- salts
- browser profile paths
- absolute filesystem paths
- package paths
- raw collector paths
- unbounded raw comments
- generated response text
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

The presence of these fields in a candidate output must block or redact the row before emission.

## J. Future Blocker Contract

Future 8W-7 must block if:

- exact approval phrase is missing
- package identity mismatches
- row source is not explicitly approved
- row file is missing
- row file path would require directory traversal
- parse scope exceeds `max_preview_rows`
- redaction policy is missing
- raw author ID exposure risk exists
- author name exposure risk exists
- actual profile URL exposure risk exists
- raw comment overexposure risk exists
- private message risk exists
- minors/family sensitive personal detail risk exists
- cookie/session/token/API key/password/secret risk exists
- browser profile path risk exists
- absolute path or package path exposure risk exists
- private collector source inspection is requested
- real exchange directory traversal is requested
- Evidence Layer write is requested
- production case or production `analysis_run` is requested
- review queue runtime is requested
- frontend/route/API is requested
- B-end report or Sandbox/public event is requested
- report/export/download/public/final-delivery runtime is requested
- public/customer output is requested
- generated response text is requested
- publish/send/post/execute/auto-execute is requested
- real API, real LLM, provider, or collector execution is requested
- URL fetch or scrape is requested

Blocked output must not echo raw values, paths, tokens, identities, snippets beyond redaction limits, or private details.

## K. Future No-production Side-effect Contract

Future row preview must keep all production/public side effects false:

- Evidence Layer write
- EvidenceItem creation
- review queue runtime
- production review queue item creation
- production case creation
- production `analysis_run` creation
- production dedup
- analysis execution
- report runtime
- B-end report runtime
- Sandbox/public event runtime
- export/download/public/final-delivery runtime
- public route creation
- signed URL creation
- public URL creation
- file-byte route creation
- object storage upload
- email sending
- portal publication
- generated response text
- publish/send/post/execute/auto-execute

Preview rows are human-review-only artifacts and must not be treated as production evidence.

## L. Future Test Contract

Future 8W-7 tests must prove:

- exact package identity accepted
- wrong package blocks
- missing exact approval phrase blocks
- row file opening limited to explicitly approved source
- `max_preview_rows` enforced
- `evidence_items.csv` not opened when JSONL is selected
- `source_manifest.jsonl` not parsed
- `collection_log.jsonl` not parsed
- private collector source not accessed
- real exchange directory not traversed
- raw author ID/name/profile URL sentinels redacted or blocked
- secret/token/cookie sentinels blocked
- absolute path/package path not emitted
- text snippets capped
- no Evidence Layer write
- no production case
- no production `analysis_run`
- no route/frontend
- no B-end report/Sandbox/public output
- no generated response text
- all runtime side-effect flags false

Tests should use local fixtures and monkeypatch forbidden file reads to prove non-selected files are not opened.

## M. Private Collector / Exchange Boundary

Future row preview must not:

- inspect private collector source
- modify private collector project
- run collector jobs
- run provider jobs
- access collector sessions, cookies, tokens, browser profiles, or secrets
- accept external export roots
- accept env-provided real paths
- traverse real exchange directories
- parse private collector raw output

Only the explicitly approved repo-controlled package target and explicitly approved row source may be considered after exact approval.

## N. Evidence Layer / Production Boundary

Future row preview is not Evidence Layer import.

It must not:

- write Evidence Layer
- create EvidenceItems
- create production review queue items
- create production case
- create production `analysis_run`
- run production dedup
- run analysis
- generate report
- generate Sandbox fixture
- generate public event
- generate export/download/public/final-delivery artifact

Any later production promotion must require a separate gate.

## O. Forbidden Interpretations

Do not interpret this contract as:

- approval to implement row preview now
- approval to create tests now
- approval to create backend helper now
- approval to open `evidence_items.jsonl` now
- approval to open `evidence_items.csv` now
- approval to parse rows now
- approval to preview raw comments
- approval to expose raw identities
- approval to inspect private collector source
- approval to read real exchange directories
- approval to write Evidence Layer
- approval to create production case
- approval to create production `analysis_run`
- approval to create review queue runtime
- approval to create frontend routes
- approval to generate B-end report runtime
- approval to generate Sandbox/public event runtime
- approval to generate report/export/download/public/final-delivery runtime
- approval to create public/customer output
- approval to generate response text
- official verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof
- prediction
- production score

The only current decision is that a future 8W-7 controlled row preview implementation may be considered after exact approval and under this contract.
