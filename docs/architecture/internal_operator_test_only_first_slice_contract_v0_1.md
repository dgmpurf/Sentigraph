# Internal Operator Test-only First Slice Contract v0.1

## A. Purpose

This document defines the future 8T-23 test-only implementation contract.

This phase does not implement it.
It does not create tests.
It does not modify backend route code.
It does not modify frontend code.
It does not approve runtime changes.

The future 8T-23 slice, if explicitly approved by the user, should add tests only.

## B. Allowed Future Files for 8T-23

Possible future test files only:

- `backend/app/tests/test_internal_operator_route_ui_safety_contract.py`

Alternative if lower risk after inspection:

- Extend an existing internal operator route smoke test file only if the added scope remains test-only and does not blur phase history.

Do not create these files in 8T-22.

## C. Future 8T-23 Allowed Implementation Scope

Allowed:

- Tests only.
- Test fixtures only if synthetic and in-memory / `tmp_path`.
- Monkeypatch guards for file open / path reads if safe.
- Static scans of existing route module.
- Route registry checks.
- Serialized response scans.
- Side-effect checks for no storage/runtime files.

Not allowed:

- Backend route code changes.
- Frontend code changes.
- Auth implementation.
- UI implementation.
- Route behavior change.
- Persistent storage.
- Evidence row preview.
- Production import.
- Evidence Layer write.
- Production case.
- `analysis_run`.
- Collector runtime / API bridge.
- Real API / real LLM.
- URL fetch / scrape.

## D. Future 8T-23 Minimum Test Cases

Proposed tests:

1. Disabled by default returns safe `route_disabled`.
2. Falsey env values remain disabled.
3. Explicit `1` / `true` / `yes` enables synthetic fixture only.
4. Unknown candidate returns safe `not_found`.
5. Route methods remain GET-only.
6. No public / C-end / B-end / customer alias.
7. Safe responses contain no forbidden keys/values.
8. Required false safety flag names are allowed only as boundary flags.
9. No `FileResponse` / `StreamingResponse` / ZIP / public URL / signed URL / external delivery in route module.
10. No `evidence_items.jsonl` / `evidence_items.csv` open in synthetic fixture mode.
11. No private collector export root or real package read.
12. No storage / Evidence Layer / production case / `analysis_run` side effects.
13. No `response_text` / `generated_public_message` / `target_user_list` / persuasion / truth / official / prediction / personality fields.

Tests must be written so that any accidental file read, path probe, public alias, state mutation, or forbidden field exposure fails loudly.

## E. Future Validation Command Plan

Future 8T-23, if approved, should run:

```text
python -m pytest backend/app/tests/test_internal_operator_route_ui_safety_contract.py
python -m pytest backend/app/tests/test_internal_operator_review_only_staging_enabled_fixture_smoke.py
python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
python -m py_compile backend/app/api/v1/routes/internal_operator_review_only_staging.py
git diff --check
git status --short
```

If the actual route module path changes before 8T-23, inspect the repository and use the actual route module path instead of guessing.

Do not run frontend build unless frontend changes accidentally occur.
Do not run collector.
Do not run browser smoke unless a later UI phase explicitly approves browser validation.

## F. Future 8T-23 Output Requirements

Future 8T-23 output should include:

- Decision.
- `privacy_issue_stop`.
- `tests_changed`.
- `runtime_code_changed`.
- Test files changed.
- Tests passed.
- Route behavior changed yes/no.
- Forbidden field scan result.
- File open/path guard result.
- Side-effect result.
- Recommended commit.
- Recommended tag: no.

It must also confirm no backend runtime code changed, no frontend code changed, no collector run, no real APIs, no URL fetch/scrape, no evidence row parsing, and no production side effects.

## G. Explicit Non-goals

- No route runtime.
- No UI.
- No auth runtime.
- No storage.
- No evidence preview.
- No production import.
- No collector bridge.
- No real API.
- No real LLM.
- No URL fetch / scrape.
- No public / C-end / B-end / customer route.
