# Internal Operator Route Access Policy Matrix v0.1

## A. Policy Matrix

| Route / capability | Current status | Allowed now? | Allowed only as docs? | Requires separate approval? | Forbidden fields / side effects | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Route disabled default | Current yes | Yes | No | No | No state mutation, no evidence rows, no production import | Route must remain disabled by default. |
| Enabled synthetic fixture test mode | Current yes | Only for tests/readiness smoke | No | Already limited to explicit env test mode | No real package reads, no private collector export root reads, no evidence rows, no storage | Enabled values are explicit `1` / `true` / `yes`; mode remains synthetic/test-only. |
| Future local operator mode | Candidate only | No | Yes | Yes | No anonymous/public/customer/provider access, no absolute paths, no raw identifiers, no evidence rows | Requires auth/local-only implementation approval and targeted tests. |
| Future operator UI | Candidate only | No | Yes | Yes | No runtime file exposure, no public route, no production actions | UI contract docs may be considered before implementation. |
| Future persistent staging storage | Not implemented | No | Yes, design only | Yes | No storage write, no audit append, no review queue creation now | Storage requires a separate persistence/privacy design. |
| Future evidence row preview | Blocked | No | Yes, design only | Yes | Raw rows, raw comments, raw author IDs/names, profile URLs, private messages | Evidence row preview remains blocked until a separate gate. |
| Future production import | Blocked | No | Yes, design only | Yes | Evidence Layer write, production case, `analysis_run`, review queue creation | Production import is not part of this route skeleton. |
| Future public / C-end / B-end exposure | Blocked | No | No, except boundary warning docs | Yes | Public customer route, public URL, signed URL, external delivery | Internal route must not become customer-facing. |
| Future collector runtime bridge | Blocked | No | No, except boundary warning docs | Yes | HTTP/API bridge, collector as crawler, live crawl, cookies/sessions/profile transfer | Private collector direct access remains blocked. |

## B. Route Method Matrix

Existing route family remains GET-only:

```text
GET /api/v1/internal/staging/review-only/candidates
GET /api/v1/internal/staging/review-only/candidates/{staging_candidate_id}
```

Not approved:

- POST.
- PUT.
- PATCH.
- DELETE.
- State mutation.
- Audit append in current route skeleton.
- Review queue creation.
- Storage write.
- Evidence Layer write.
- Production case creation.
- `analysis_run` creation.

The current route skeleton is read-only and metadata-only. Future method expansion requires separate explicit approval.

## C. User / Access Matrix

| Actor | Current access | Future possible access | Notes |
| --- | --- | --- | --- |
| internal_operator | None by default; disabled route only unless explicitly synthetic/test-enabled | Docs-only candidate for future local-only access | Must be role-gated and local-only before any real metadata expansion. |
| local_developer_operator | None by default; may use explicit synthetic/test mode for local readiness | Docs-only candidate for future local-only access | Test-only synthetic mode does not imply production access. |
| security_reviewer | None by default | Docs-only candidate for future review-only checks | Future access, if any, must not expose raw paths, raw identifiers, rows, or secrets. |
| customer_user | Blocked | Blocked | Must not access internal operator route. |
| public_user | Blocked | Blocked | No public internet exposure. |
| c_end_user | Blocked | Blocked | No C-end alias. |
| b_end_customer_user | Blocked | Blocked | No B-end/customer alias. |
| provider_system | Blocked | Blocked | No provider callback or direct provider access. |
| private_collector | Blocked | Blocked | No direct route access, no HTTP/API bridge, no crawler integration. |

Only `internal_operator`, `local_developer_operator`, and `security_reviewer` may be future docs-only candidates. All customer/public/provider/private collector direct access remains blocked.

## D. Data Exposure Matrix

Allowed safe metadata:

| Field / category | Allowed? | Notes |
| --- | --- | --- |
| `staging_candidate_id` | Yes | Safe synthetic or metadata-only identifier. |
| `provider_result_id` | Yes | Safe metadata identifier only. |
| `package_name` | Yes | Safe package label only; no absolute path. |
| `case_id_hint` | Yes | Hint only; no production case creation. |
| `validation_status` | Yes | Metadata-only validation summary. |
| `evidence_count` | Yes | Count only, not row content. |
| `source_count` | Yes | Count only, not row content. |
| `warning_count` | Yes | Count only. |
| `error_count` | Yes | Count only. |
| Safe coverage summary | Yes | Limitation metadata only. |
| Blockers / warnings | Yes | Safe codes and labels only. |
| `allowed_actions` labels | Yes | Labels only; no state-changing endpoint implied. |
| `blocked_actions` labels | Yes | Boundary labels only. |
| `safety_flags` | Yes | Boolean boundary flags only. |

Forbidden data:

| Field / category | Allowed? | Notes |
| --- | --- | --- |
| Raw evidence rows | No | No row preview in this phase. |
| Raw comments | No | No comment content exposure. |
| Raw author IDs/names | No | No raw identity exposure. |
| Profile URL actual values | No | No profile URL values. |
| Cookies / sessions / tokens / passwords / API keys | No | No secret or credential exposure. |
| Browser profile paths | No | No browser profile transfer. |
| Absolute private paths | No | No absolute filesystem path exposure. |
| Private messages | No | No private content. |
| `response_text` | No | No generated response text. |
| `generated_public_message` | No | No public message generation. |
| `target_user_list` | No | No targeting. |
| `persuasion_score` | No | No persuasion scoring. |
| `truth_score` | No | No truth scoring. |
| `official_verified` | No | No official verification claim. |
| `prediction_probability` | No | No prediction probability. |
| `psychological_profile` | No | No personality profiling. |
| `personality_diagnosis` | No | No personality diagnosis. |

## E. Implementation Stop Rule

If any future implementation proposes UI, storage, evidence row preview, production import, public route, collector runtime bridge, API bridge, or real package reads, stop and require a separate explicit user approval.

This route must remain a disabled-by-default, local/internal, metadata-only governance surface until a later approved phase changes exactly one boundary with targeted tests and a matching safety report.
