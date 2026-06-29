# Internal Operator Future Implementation Slice Options v0.1

## A. Purpose

This is a docs-only options document for future internal operator route/UI work.

It does not approve implementation.
It does not modify route behavior.
It does not approve UI.
It does not approve auth/local-only runtime.
It does not approve storage.
It does not approve evidence row preview.
It does not approve production import.

The goal is to identify safe future gates after the 8T-17 / 8T-18 / 8T-19 contracts without jumping directly into runtime or UI implementation.

## B. Option 1: Safety Test Plan Only

Define a targeted docs-only safety test plan for:

- Disabled route behavior.
- Explicit synthetic fixture enabled mode.
- No forbidden fields.
- GET-only route surface.
- No public alias.
- No C-end alias.
- No B-end alias.
- No `FileResponse`.
- No `StreamingResponse`.
- No ZIP generation.
- No public URL.
- No signed URL.
- No external delivery.
- No evidence row file opening.
- No private collector export root read.
- No real package directory read.
- No storage write.
- No Evidence Layer write.
- No production case.
- No `analysis_run`.

No code implementation.

Recommendation: safest next step.

## C. Option 2: First Implementation Slice Design Only

Define a future minimal implementation slice design, such as:

- Route hardening design around safe denial responses.
- UI placeholder design that remains unimplemented.
- Static safety scan plan for route/UI boundaries.
- Contract-to-test mapping.

Constraints:

- No implementation.
- Must keep route disabled by default.
- Must not add UI without explicit approval.
- Must not add auth runtime without explicit approval.
- Must not add storage.
- Must not preview evidence rows.
- Must not import production Evidence.

Recommendation: acceptable only as docs.

## D. Option 3: Implement Auth / Local-only Runtime

Status:

```text
not_approved_now
```

Requirements before consideration:

- Separate explicit approval.
- Safety test plan.
- Safe response contract.
- No sessions/tokens/cookies unless separately approved.
- No query-string token access.
- No hardcoded tokens.
- No private collector browser/login/profile state.
- No customer/public/provider/private collector direct access.
- Route remains disabled by default unless a separate gate changes exactly that.

Recommendation: do not implement now.

## E. Option 4: Implement Internal Operator UI

Status:

```text
not_approved_now
```

Requirements before consideration:

- Separate explicit approval.
- Frontend safety tests.
- Browser smoke.
- No active production/public actions.
- No public / C-end / B-end alias.
- No raw rows.
- No raw comments.
- No raw identifiers.
- No secrets.
- No absolute paths.
- No evidence row preview.
- No storage.
- No production import.

Recommendation: do not implement now.

## F. Option 5: Persistent Storage / Evidence Row Preview / Production Import

Status:

```text
blocked
```

This is not a near-term option.

Persistent storage, evidence row preview, and production import each require separate architecture, privacy, governance, tests, and explicit user approval. None of these should be bundled into route/UI readiness work.

## G. Recommendation

Recommended path:

1. 8T-21 route/UI safety test plan docs-only first.
2. Optionally perform a ChatGPT-side Source patch if the user wants current context updated.
3. Consider a first implementation-slice design only after the safety test plan exists.

Do not implement runtime, UI, storage, evidence row preview, or production import yet.
