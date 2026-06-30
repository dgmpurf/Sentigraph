# Internal Operator Env Gate Helper Implementation Plan v0.1

## A. Purpose

This is a docs-only implementation plan for future `route_enabled_env_gate_helper`.

It does not implement helper code. It does not approve implementation. It does not approve runtime expansion.

## B. Candidate Helper Name

Canonical proposed helper name:

`route_enabled_env_gate_helper`

Final naming can be adjusted during future implementation if the current route module structure strongly favors a private local function name. Any naming adjustment must preserve the same contract and no-behavior-change proof requirements.

## C. Future Helper Interface

Proposed deterministic interface:

Input:

- `raw_env_value: str | None`

Output:

- `enabled: bool`
- `mode: disabled | synthetic_fixture_only`
- `disabled_reason: route_disabled | None`

No filesystem input.
No request object.
No cookies.
No sessions.
No tokens.
No query params.
No role/account auth.
No production mode.

## D. Behavior Table

| raw_env_value | expected enabled | expected mode | expected reason |
| --- | --- | --- | --- |
| `None` | false | `disabled` | `route_disabled` |
| empty string | false | `disabled` | `route_disabled` |
| `false` | false | `disabled` | `route_disabled` |
| `0` | false | `disabled` | `route_disabled` |
| `unknown` | false | `disabled` | `route_disabled` |
| `1` | true | `synthetic_fixture_only` | `None` |
| `true` | true | `synthetic_fixture_only` | `None` |
| `yes` | true | `synthetic_fixture_only` | `None` |
| `TRUE` | true | `synthetic_fixture_only` | `None` |
| `Yes` | true | `synthetic_fixture_only` | `None` |
| ` true ` | true | `synthetic_fixture_only` | `None` |

Current-code inspection note:

- Current route logic uses `strip().lower()`, so the future helper must preserve case-insensitive and surrounding-whitespace behavior for the same accepted values.
- Do not introduce new accepted values beyond the current accepted set after normalization.

## E. Future Code Movement Plan

Option A:

Extract existing env decision logic inside the current route module into a local private helper in the same module.

This has the lowest surface area.

Option B:

Extract to `backend/app/services/internal_operator_route_guard.py`.

This is more reusable but has larger surface area.

Recommendation:

Option A first, unless current code structure strongly favors service extraction during the future implementation phase.

## F. Allowed Future Changed Files If Implementation Is Approved Later

Allowed:

- `backend/app/api/v1/routes/internal_operator_review_only_staging.py`
- `backend/app/tests/test_internal_operator_review_only_staging_disabled_smoke.py`
- `backend/app/tests/test_internal_operator_review_only_staging_enabled_fixture_smoke.py`
- `backend/app/tests/test_internal_operator_route_ui_safety_contract.py`

Optional only if justified:

- `backend/app/services/internal_operator_route_guard.py`
- `backend/app/tests/test_internal_operator_route_env_gate_helper.py`

Not allowed:

- frontend files
- Source files
- GitHub Actions
- runtime storage files
- private collector project files

## G. Future Validation Command Plan

Required later if implementation is approved:

```text
python -m pytest backend/app/tests/test_internal_operator_route_ui_safety_contract.py
python -m pytest backend/app/tests/test_internal_operator_review_only_staging_enabled_fixture_smoke.py
python -m pytest backend/app/tests/test_internal_operator_review_only_staging_disabled_smoke.py
python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
python -m py_compile backend/app/api/v1/routes/internal_operator_review_only_staging.py
git diff --check
git status --short
```

Optional:

- full backend pytest only if the route helper extraction touches shared backend behavior.

## H. Future Implementation Approval Requirement

Even after 8T-27, implementation requires explicit user approval.

Approval phrase should be something like:

`批准 8T-28 env gate helper implementation`

Without that approval, do not implement.
