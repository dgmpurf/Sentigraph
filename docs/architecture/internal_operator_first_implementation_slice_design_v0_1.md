# Internal Operator First Implementation Slice Design v0.1

## A. Purpose

This is a docs-only design for the future first implementation slice after the internal operator route/UI contracts.

It does not implement tests.
It does not implement route code.
It does not implement UI.
It does not implement auth.
It does not approve runtime expansion.
It does not approve storage, evidence row preview, production import, or collector runtime integration.

The purpose is to choose the safest future implementation slice and make explicit that implementation still requires separate user approval.

## B. Input Milestones

- 8T-17 route skeleton accepted after disabled + enabled synthetic fixture smoke.
- 8T-18 auth/local-only contract accepted.
- 8T-19 UI contract accepted.
- 8T-20 route/UI implementation readiness decision rejected direct implementation.
- 8T-21 route/UI safety test plan created.

These inputs establish a governance-first path. They do not approve runtime route expansion, frontend UI, auth runtime, persistent storage, evidence row preview, or production import.

## C. Candidate Implementation Slices

| Candidate | Description | Risk level | Implementation approval now? | Why / why not | Required prerequisites | Recommended order |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Test-only safety contract implementation | Add targeted backend tests and static scans for route/UI safety contracts. | Low | No, requires explicit user approval | Safest first implementation because it does not change route/UI behavior. | User approval, test-only scope, no runtime changes. | First future slice. |
| 2. Route hardening implementation | Change route runtime or safe response logic. | Medium | No | Runtime changes can affect behavior and need tests first. | Test-only slice, explicit approval, narrow bug/safety objective. | After test-only slice if needed. |
| 3. Auth/local-only runtime implementation | Add auth/locality checks. | High | No | Requires auth design, denial tests, and careful no-token/no-cookie boundaries. | Auth test plan, explicit approval, no sessions/tokens/cookies unless separately approved. | Not first. |
| 4. Internal operator UI implementation | Add frontend UI for safe metadata. | High | No | UI can accidentally expose data, overstate actions, or create customer-facing surfaces. | UI safety tests, browser smoke plan, explicit approval. | Not first. |
| 5. Persistent staging storage | Persist staging candidates or audits. | High | No | Storage introduces retention, privacy, audit, and cleanup requirements. | Storage/privacy design, tests, explicit approval. | Blocked. |
| 6. Evidence row preview | Preview row contents. | Very high | No | Raw rows/comments/identifiers may leak. | Redaction/privacy design, approval, tests. | Blocked. |
| 7. Production import | Write Evidence Layer / production case / `analysis_run`. | Very high | No | Production side effects are outside route skeleton milestone. | Separate import governance gate. | Blocked. |

Expected conclusion:

```text
Candidate 1 is the only acceptable future first implementation slice.
Candidates 2-7 are not approved now.
```

## D. Recommended First Implementation Slice

Recommended future slice:

```text
8T-23 test-only safety contract implementation
```

Scope:

- Add targeted tests only.
- No backend runtime behavior change.
- No frontend UI.
- No route behavior change.
- No auth runtime.
- No storage.
- No evidence row preview.
- No production import.
- No collector runtime / API bridge.

Possible future test focus:

- Disabled/default route behavior.
- Falsey env route disabled.
- Explicit synthetic fixture enabled mode.
- GET-only route surface.
- No public / C-end / B-end alias.
- No forbidden fields in serialized responses.
- No `FileResponse` / `StreamingResponse` / ZIP / public URL / signed URL / external delivery.
- No `evidence_items.jsonl` / `evidence_items.csv` opening.
- No real package / private collector root read.
- No storage / Evidence Layer / production case / `analysis_run` side effects.

## E. Not Recommended as First Slice

Not recommended as first slice:

- Route runtime expansion: behavior changes should follow tests, not precede them.
- UI implementation: frontend exposure needs safety tests and browser smoke planning first.
- Auth implementation: auth/locality runtime needs denial-response and no-token/no-cookie tests first.
- Local-only runtime: locality enforcement needs a narrow contract-to-test implementation plan first.
- Storage: persistence changes need retention/privacy/audit design.
- Evidence row preview: raw rows/comments/identifiers remain blocked.
- Production import: Evidence Layer writes and production case creation remain blocked.
- Public / C-end / B-end exposure: internal route must not become customer-facing.
- Collector runtime / API bridge: private collector must not become an internal crawler or runtime bridge.

## F. Approval Requirement

Even the test-only implementation slice requires separate explicit user approval before Codex modifies tests.

This phase only designs the slice.

Approval for a test-only slice must not be interpreted as approval for route runtime changes, frontend UI, auth runtime, storage, evidence row preview, production import, or collector runtime/API bridge.

## G. Stop Rules

If a future task asks to implement route/UI/auth/storage/evidence preview/import before the test-only slice is approved, stop and request explicit approval.

If a future task asks to read real package directories, read private collector export roots, open `evidence_items.jsonl`, open `evidence_items.csv`, write Evidence Layer, create production case, create `analysis_run`, generate reports, generate public events, publish/send/post/execute, or connect collector runtime/API bridge, stop and require a separate explicit gate.
