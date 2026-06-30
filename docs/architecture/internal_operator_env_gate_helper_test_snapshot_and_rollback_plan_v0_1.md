# Internal Operator Env Gate Helper Test, Snapshot, and Rollback Plan v0.1

## A. Purpose

This is a docs-only plan for future tests, snapshots, and rollback.

No tests are implemented now. No helper code is implemented now. No route behavior is changed now.

## B. Test Groups

1. Helper unit behavior tests
   - Verify `None`, empty string, `false`, `0`, and unknown values remain disabled.
   - Verify `1`, `true`, and `yes` remain enabled as synthetic fixture only.
   - Verify case and whitespace behavior preserves current `strip().lower()` route behavior.
2. Route disabled smoke tests
   - Verify unset env remains disabled.
   - Verify falsey env values remain disabled.
   - Verify disabled response shape stays safe.
3. Route enabled synthetic fixture tests
   - Verify list response stays synthetic fixture only.
   - Verify detail response stays synthetic fixture only.
   - Verify unknown candidate stays safe `not_found`.
4. Route/UI safety contract tests
   - Verify no public aliases.
   - Verify no active forbidden fields.
   - Verify no evidence row file opens.
   - Verify no side-effect files.
5. Golden contract tests
   - Verify analysis request golden contracts remain passing.
6. Static safety scans
   - Verify no `FileResponse`.
   - Verify no `StreamingResponse`.
   - Verify no ZIP/archive.
   - Verify no public/signed URL.
   - Verify no external delivery.
7. Side-effect checks
   - Verify no storage.
   - Verify no Evidence Layer write.
   - Verify no production case.
   - Verify no analysis_run.
8. py_compile / git hygiene
   - Compile touched backend route module.
   - Run `git diff --check`.
   - Run `git status --short`.

## C. Snapshot Inventory

- `disabled_default_response`
- `false_env_response`
- `zero_env_response`
- `unknown_env_response`
- `enabled_1_list_response`
- `enabled_true_list_response`
- `enabled_yes_list_response`
- `enabled_detail_response`
- `unknown_candidate_not_found_response`
- `route_methods_snapshot`
- `route_alias_snapshot`
- `static_forbidden_implementation_scan`

## D. Snapshot Comparison Rule

Allowed:

- ordering-insensitive comparison for JSON object keys.
- explicit safe timestamp/ID normalization if present.
- documented equivalence for non-semantic ordering.

Forbidden:

- changing field names.
- changing route status semantics.
- adding production/runtime fields.
- adding raw metadata/row fields.
- adding public URL/download fields.

## E. Rollback Checklist

If future implementation fails:

1. Revert helper extraction change.
2. Rerun targeted route tests.
3. Rerun 8T-23 safety contract tests.
4. Verify route disabled default.
5. Verify enabled synthetic fixture mode.
6. Verify no source files / runtime files / frontend files added.
7. Restore git clean state.

## F. Stop Rules

Stop immediately if:

- route becomes enabled by default.
- any currently disabled env value becomes enabled.
- any currently enabled value becomes disabled.
- production mode appears.
- route methods change.
- public/C-end/B-end/customer alias appears.
- response schema changes.
- `FileResponse` / `StreamingResponse` / ZIP / public URL / signed URL / external delivery appears.
- `evidence_items` file opens.
- private collector root is read.
- storage / Evidence Layer write / production case / analysis_run appears.
- auth/session/token/cookie behavior appears.
- `response_text` / `generated_public_message` / `target_user_list` / `persuasion_score` / `truth_score` / `official_verified` / `prediction_probability` / `psychological_profile` / `personality_diagnosis` appears.
