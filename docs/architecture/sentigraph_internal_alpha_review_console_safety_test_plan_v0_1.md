# Sentigraph Internal Alpha Review Console Safety Test Plan v0.1

## Purpose

This document defines a future safety-test-only slice for an Internal Alpha review console. It does not approve route/API/frontend implementation.

The future test-only slice is intended to prevent ambiguity before any read-only internal review console work is considered.

## Inactive Future Phrase

Future phrase, inactive in 8Z-17:

`APPROVE_8Z_18_INTERNAL_ALPHA_REVIEW_CONSOLE_SAFETY_CONTRACT_TESTS_ONLY`

This phrase is recorded only as an inactive future planning label. It does not authorize anything in 8Z-17. It does not authorize route/API/frontend implementation, actual Evidence Layer write, production EvidenceItem creation, Review Queue runtime, production case, production analysis_run, actual analysis execution, production Analysis Result, Source 11 runtime, FinalSummaryReport runtime, collector/provider jobs, real package reads, or public/export delivery.

## Test-only Next Slice Rationale

The next safe step, if any, should be tests-only because:

- 8Z-16 reached only a no-write boundary.
- human review is still required.
- no automatic trust upgrade remains required.
- actual write and production object creation remain higher-risk separate gates.
- route/API/frontend exposure could accidentally imply readiness if not guarded by tests first.
- a console could expose raw rows or identities unless projection is specified and tested.

## Expected Test Categories

Future 8Z-18 tests should cover:

- route disabled by default if a route is later introduced
- no public aliases
- no C-end aliases
- no B-end/customer aliases
- safe metadata projection only
- forbidden field scan
- forbidden value scan
- no raw rows
- no raw comments
- no raw author IDs
- no raw author names
- no profile URLs
- no cookies/sessions/tokens/passwords/API keys
- no absolute private paths
- no `.env` values
- no `evidence_items.jsonl` contents
- no `evidence_items.csv` contents
- no source_manifest row contents
- no collection_log row contents
- no original package row contents
- no response_text or generated_public_message
- no target_user_list / persuasion_score / truth_score / official_verified / prediction_probability
- no psychological_profile / personality_diagnosis
- no file read
- no row read
- no helper call
- no Evidence Layer write
- no production EvidenceItem
- no Review Queue runtime
- no production Review Queue item
- no production case
- no production analysis_run
- no actual analysis execution
- no production Analysis Result
- no Source 11 runtime
- no FinalSummaryReport runtime
- no export/public delivery runtime
- no forbidden CTA

## Codex Self-validation First

Codex should validate future safety tests before asking the user to playtest. A future console task must not rely on the user as a routine tester for defects that Codex can catch with local tests, static scans, or browser smoke.

## Browser Smoke Rule

Browser smoke is required only if UI/frontend changes are later explicitly approved and browser capability is available without installing new tooling.

If browser smoke is used, it must verify:

- the surface is internal-only and local-only
- no public/customer labels
- no raw fields
- no forbidden CTA
- boundary copy is visible
- no console error/warn
- no `[object Object]`
- no `undefined`
- no `NaN`
- no visible 500/ErrorBoundary

8Z-17 does not run browser smoke because it is docs-only planning.

## Draft Validation Bundle for Future 8Z-18

Future 8Z-18 may require:

- focused safety contract test file only
- static scan of route/UI files if touched
- forbidden field/key/value scan
- no file-read monkeypatch coverage
- no helper-call monkeypatch coverage
- no downstream runtime monkeypatch coverage
- `git diff --check`
- `git status --short`

Future 8Z-18 should not run full pytest unless touched files or failures require it. It should not run frontend build or browser smoke unless route/UI implementation is explicitly in scope later.

## Stop / Report Conditions

Stop and report if a future task requires:

- service code implementation
- route/API implementation
- frontend implementation
- runtime persistence
- helper execution
- row preview execution
- Evidence candidate creation
- Review Queue candidate creation
- Evidence Layer import candidate creation
- Evidence Layer write-candidate creation
- actual Evidence Layer write
- production EvidenceItem creation
- Review Queue runtime
- production case
- production analysis_run
- actual analysis execution
- production Analysis Result
- Source 11 runtime
- FinalSummaryReport runtime
- B-end report runtime
- Sandbox/public event runtime
- export/download/public/final delivery runtime
- collector/provider jobs
- real API / real LLM
- URL fetch / scraping
- private collector inspection
- real exchange/package directory read
- production package row parsing
- raw rows/comments/identities exposure
- secrets access

## Future Commit / Tag / Source Rules

Future tests should not commit, tag, or update Project Source files unless the user explicitly asks.

For 8Z-17:

- no commit performed
- no tag performed
- no Project Source files created
- Source 11 update recommended = no

## Future Outcome Labels

Future 8Z-18 may return:

- ready_for_review_console_contract_after_tests
- needs_fix_before_review_console_contract
- privacy_issue_stop
- pause_before_route_ui_discussion

None of these labels approve actual write, production objects, Review Queue runtime, Source 11 runtime, FinalSummaryReport runtime, public/export delivery, or route/API/frontend implementation.
