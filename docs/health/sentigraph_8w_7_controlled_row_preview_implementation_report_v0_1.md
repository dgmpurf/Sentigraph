# Sentigraph 8W-7 Controlled Row Preview Implementation Report v0.1

## A. Decision / Status

decision = ready

privacy_issue_stop = no

backend_only = yes

test_first = yes

row_preview_implementation = yes

metadata_boundary_input = yes

redacted_preview_only = yes

backend_code_changed = yes

frontend_code_changed = no

tests_changed = yes

route_changed = no

api_route_added = no

runtime_changed = local_backend_object_only

source_boundary_schema = sentigraph_metadata_smoke_review_only_staging_boundary_v0_1

output_schema = sentigraph_controlled_row_preview_v0_1

approved_package_name = donglu-sunjihai-youth-football-202606-v2_20260617_121016

approved_package_role = candidate_demo_sample

approved_case_id_hint = donglu_sunjihai_youth_football_202606

approved_row_source = evidence_items.jsonl

evidence_items_jsonl_opened = yes

evidence_items_jsonl_parsed = yes

evidence_items_csv_opened = no

evidence_items_csv_parsed = no

source_manifest_rows_parsed = no

collection_log_rows_parsed = no

original_package_rows_read = no

private_collector_inspected = no

private_collector_source_inspected = no

real_exchange_dir_read = no

max_preview_rows_applied = 5

max_preview_rows_hard_bound = 10

preview_rows_count = 5

rows_inspected_count = 5

row_limit_enforced = yes

text_snippet_max_chars = 160

raw_author_ids_emitted = no

raw_author_names_emitted = no

profile_urls_emitted = no

raw_comments_emitted = no

secrets_emitted = no

absolute_path_exposed = no

package_path_exposed = no

review_queue_item_created = no

production_review_queue_item_created = no

evidence_items_created = no

evidence_layer_write = no

production_case_created = no

production_analysis_run_created = no

b_end_report_runtime_generated = no

sandbox_public_event_generated = no

generated_response_text = no

public_route_created = no

frontend_integration_approved = no

download_package_runtime_used = no

public_access_runtime_used = no

external_delivery_runtime_used = no

final_delivery_runtime_used = no

source_files_created = no

docs_project_sources_created = no

8W-7 is ready as a backend-only, bounded, redacted row preview helper. It produces only an in-memory local preview object for human review and does not create production evidence, cases, analysis runs, routes, frontend integration, reports, public outputs, or delivery artifacts.

## B. Exact Approval and Approved Row Source

Historical exact approval phrase recorded by 8W-7 and superseded by 8Y-3A:

`批准 8W-7 Controlled Row Preview Implementation`

8Y-3A supersedes that phrase with:

`APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION`

The old Chinese phrase and any mojibake variant must be rejected before any row source opens after 8Y-3A. This historical report remains as implementation history and should be read together with the 8Y-3A repair report.

Approved package identity:

- package_name: `donglu-sunjihai-youth-football-202606-v2_20260617_121016`
- package_role: `candidate_demo_sample`
- case_id_hint: `donglu_sunjihai_youth_football_202606`

Approved row source:

`evidence_items.jsonl`

The helper blocks if the exact approval phrase is missing or different. It blocks if callers request CSV, dual-source parsing, source manifest rows, collection log rows, original package rows, private collector raw output, arbitrary paths, or side-effect actions.

## C. Changed Files

- `backend/app/services/controlled_row_preview.py`
- `backend/app/tests/test_controlled_row_preview.py`
- `docs/health/sentigraph_8w_7_controlled_row_preview_implementation_report_v0_1.md`

No frontend, route/API registration, Evidence Layer runtime, production case, production analysis run, review queue runtime, B-end report runtime, Sandbox/public event runtime, export/download/public/final-delivery runtime, private collector, Project Source, or `docs/project_sources/` files were changed.

## D. Controlled Row Preview Helper Summary

Added helper module:

`backend/app/services/controlled_row_preview.py`

Public helper names:

- `build_controlled_row_preview`
- `create_controlled_row_preview`
- `build_safe_controlled_row_preview_summary`

Output schema:

`sentigraph_controlled_row_preview_v0_1`

Summary schema:

`sentigraph_controlled_row_preview_summary_v0_1`

The helper consumes only a dict shaped like the 8W-4 safe local review-only staging boundary marker, the exact 8W-7 approval phrase, optional row source, optional row limit, and optional requested action labels. It does not accept filesystem paths, package roots, env roots, package selectors, external exchange directories, private collector paths, or URLs.

## E. Source Boundary Object and Package Identity

The accepted source boundary must preserve:

- schema: `sentigraph_metadata_smoke_review_only_staging_boundary_v0_1`
- phase: `8W-4`
- boundary_status: `review_only_staging_boundary_ready_for_manual_review`
- approved package name, role, and case id hint
- `metadata_only = true`
- `warning_count = 1`
- `human_review_required = true`
- `warning_manual_review_preserved = true`
- `row_preview_approved = false`
- Evidence Layer write, production case, production analysis run, route, frontend, production, public, and customer readiness false

Wrong schema, wrong phase, wrong identity, dropped warning state, unsafe source flags, or side-effect flags return blocked objects with safe reason codes only.

## F. Row Source Policy and Row Count Enforcement

Allowed row source:

`evidence_items.jsonl`

Forbidden row sources:

- `evidence_items.csv`
- dual-source parsing
- `source_manifest.jsonl`
- `collection_log.jsonl`
- original package rows outside the approved evidence row file
- private collector raw output
- arbitrary user-provided files or paths

Row limits:

- default preview rows: `5`
- hard upper bound: `10`
- `max_preview_rows <= 0` blocks
- `max_preview_rows > 10` blocks
- row limit is enforced before preview output is emitted

Observed ready/warn preview:

- `preview_rows_count = 5`
- `rows_inspected_count = 5`
- `row_limit_enforced = true`

## G. Redaction / Minimization Behavior

Preview rows include only minimized fields:

- preview row id
- bounded row index
- evidence id hash
- evidence type
- platform
- coarse created date
- trust label
- verification status
- review status
- language
- content visibility / access scope
- redacted text snippet capped at 160 characters
- redaction status and warnings
- row boundary flags

Text snippets are capped and redacted for URLs, emails, phone-like strings, handles, secret-like assignments, and long opaque identifiers. The helper falls back from body/comment text to claim summary/title when a candidate text field is unsuitable.

## H. Forbidden Fields and Blocker Behavior

Preview output must not emit:

- raw author ids
- author names, usernames, display names
- profile URLs
- raw profile URLs
- private messages
- emails, phones, addresses, identity fields
- cookies, tokens, sessions, passwords, API keys, secrets, salts
- browser profile paths
- absolute paths
- package paths
- raw collector paths
- unbounded raw comments
- generated response text
- target user lists
- persuasion score, truth score, official verified, prediction probability
- psychological profile or personality diagnosis

Synthetic tests prove forbidden sentinels are redacted, blocked, or absent from serialized output.

## I. No Private Collector / No Arbitrary Path Proof

The helper does not accept a filesystem path parameter and does not scan directories. It uses only the internal approved sample target and approved row source.

Tests monkeypatch `Path.open` and prove:

- only `evidence_items.jsonl` opens
- `evidence_items.csv` does not open
- `source_manifest.jsonl` does not open
- `collection_log.jsonl` does not open
- private collector paths do not open

No private collector project or real exchange directory was inspected.

## J. Output Preview Object

The output includes:

- schema and phase
- preview status
- exact approved target identity
- row source policy
- row count limits and inspected count
- preview row count
- redaction policy version
- warning/manual-review preservation
- preview-only and readiness false flags
- runtime side-effect flags
- safe blockers and warnings
- redacted preview rows

Successful output has:

- `created_local_row_preview = true`
- `parsed_evidence_items_jsonl = true`
- `parsed_evidence_items_csv = false`
- all production/public/frontend/delivery side effects false

Blocked output has:

- `created_local_row_preview = false`
- `preview_rows = []`
- `preview_rows_count = 0`
- safe reason-code blockers only

## K. Relationship to 8W-6 Contract

8W-7 implements the narrow option selected by 8W-6:

`ready_for_8W_7_controlled_row_preview_implementation_after_explicit_approval`

The implementation keeps the 8W-6 boundaries:

- backend-only
- exact approval required
- exact package identity
- JSONL-only first slice
- bounded rows
- redacted preview-only output
- human review required
- no production side effects

## L. Relationship to Source 11 / Evidence Layer

8W-7 does not change Source 11 behavior and does not write Evidence Layer.

It does not create:

- EvidenceItems
- review queue items
- production review queue items
- production case
- production analysis run
- production dedup
- analysis result
- B-end report
- Sandbox fixture
- public event page
- export/download/public/final-delivery object

This preview is a local backend object for human review only. It is not import approval, analysis approval, report approval, public output, customer output, official verification, full-web coverage, full-platform coverage, causal proof, prediction, or production score.

## M. Validation Commands and Results

Preflight:

- `git status --short`: clean before implementation.
- `git branch --show-current`: `main`.
- `git rev-parse HEAD`: `249296cf00618a29265d11e3bcd5f12457e46d23`.
- latest commit message: `Add 8W-6 controlled row preview gate decision`.
- 8W-6 planning and contract docs existed.

TDD red:

- `python -m pytest backend/app/tests/test_controlled_row_preview.py -q`
- failed as expected with `ModuleNotFoundError: No module named 'app.services.controlled_row_preview'`.

Focused:

- `python -m pytest backend/app/tests/test_controlled_row_preview.py -q`
- passed, 48 tests.

Nearby:

- `python -m pytest backend/app/tests/test_controlled_row_preview.py backend/app/tests/test_metadata_smoke_review_only_staging_boundary.py backend/app/tests/test_real_exported_package_metadata_smoke.py backend/app/tests/test_local_exchange_reader.py backend/app/tests/test_analysis_request_golden_contracts.py -q`
- passed, 108 tests.

Compile:

- `python -m py_compile backend/app/services/controlled_row_preview.py backend/app/services/metadata_smoke_review_only_staging_boundary.py backend/app/services/real_exported_package_metadata_smoke.py`
- passed.

Final checks:

- `git diff --check`: passed.
- `git status --short`: only the three allowed 8W-7 files were untracked/changed.
- static safety scan: passed with acceptable matches only in forbidden-field constants, side-effect false flags, test sentinels, and boundary text. No active network, route, frontend, production, delivery, or public output implementation was found.

## N. Not Run and Why

Not run:

- full pytest
- frontend build
- browser smoke
- collector
- real APIs
- real LLMs
- provider jobs
- URL fetch
- scrape
- private collector source inspection
- real exchange directory read
- Evidence Layer write
- production case / production analysis run
- review queue runtime
- B-end report / Sandbox/public event runtime
- report/export/download/public/final-delivery runtime smoke
- route/frontend smoke

Reason:

8W-7 is a backend-only controlled row preview implementation. The task explicitly scopes validation to focused/nearby backend tests, compile, diff/status, and static scan.

## O. Issues P0/P1/P2/P3

- P0: none.
- P1: none.
- P2: future 8W-8 must be docs-only Row Preview Completion / Evidence Candidate Gate Decision. Do not jump to Evidence Layer import.
- P3: consider ChatGPT-side Source 24 patch after commit.

## P. Recommended Next Step

Recommended next task:

Phase 8W-8 Row Preview Completion / Evidence Candidate Gate Decision Docs-only.

Do not proceed directly to Evidence Layer import, production case, production analysis run, review queue runtime, frontend/route, B-end report runtime, Sandbox/public event runtime, public/download/final-delivery runtime, real API, real LLM, provider execution, or collector execution.

## Q. Source Maintenance Recommendation

Recommended after commit:

- consider ChatGPT-side Source 24 or equivalent project-context patch for 8W-7
- do not update Source 11
- do not create Project Source files inside this repository
- do not create `docs/project_sources/`
