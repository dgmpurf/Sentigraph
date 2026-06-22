# Report Export Public Access / External Delivery Policy v1

## Purpose

This policy defines future eligibility, warning, limitation, and separation rules for a Report Export Public Access / External Delivery Gate.

The policy is docs-only. It does not implement a public access runtime, external delivery runtime, download route, file-byte response, public URL, signed URL, object storage publication, portal access, B-end report, Sandbox, public event, Evidence Layer write, production case, real API call, real LLM call, URL fetch, or scraping.

## Eligibility Policy

A future gate may be considered only when all of the following are true:

- upstream `ReportExportDownloadPackageArtifact` exists
- upstream package artifact status is `local_manifest_ready` or equivalent
- upstream package artifact has append-only audit
- upstream package artifact is local manifest-only or otherwise explicitly allowed by a later policy
- package manifest summary contains only safe metadata
- no public URL is present
- no signed URL is present
- no download URL is present
- no public download route exists
- no file-byte response exists
- no ZIP exists
- no binary archive exists
- no absolute filesystem path is exposed
- no raw author identifiers are present
- no secrets, tokens, cookies, sessions, salts, passwords, API key values, authorization headers, or `.env` values are present
- no runtime file is exposed
- no file bytes are exposed
- no manifest file content is exposed through API/UI
- no export artifact content is exposed through API/UI
- no export artifact file content is read, parsed, or copied
- no original package rows are read
- all boundary flags remain false
- downstream B-end, Sandbox, public event, public access runtime, and external delivery runtime remain separate

If any requirement fails, status must be `blocked` or `privacy_hold`.

## Requested Mode Policy

Requested future access/delivery modes must be labels only. They must not trigger side effects.

Allowed future labels:

- `public_download_route_future_candidate`
- `file_byte_response_future_candidate`
- `signed_url_future_candidate`
- `public_url_future_candidate`
- `restricted_portal_access_future_candidate`
- `object_storage_publication_future_candidate`
- `external_delivery_future_candidate`
- `internal_handoff_future_candidate`

Unsupported or ambiguous labels must be blocked by policy.

## Required Warning Language

Future gate output should preserve warnings equivalent to:

- Provider output is evidence, not truth.
- This package is not official verification.
- This package is not full-web coverage.
- This package is not full-platform coverage.
- This package is not full-thread coverage.
- Evidence scope remains limited to imported or available evidence.
- Low-trust and weak-evidence warnings remain visible.
- Rejected evidence exclusion is preserved.
- Duplicate evidence no-amplification is preserved.
- A manifest-only package does not equal a public download.
- Public access and external delivery are future gated steps.
- B-end report generation requires a separate gate.
- Sandbox generation requires a separate gate.
- Public event generation requires a separate gate.

## Blockers

The future gate must block readiness for:

- privacy hold
- missing upstream package artifact
- missing upstream package artifact audit
- missing upstream download/package gate
- missing final summary report export artifact
- missing final report lineage
- unsafe requested mode
- public URL already present
- signed URL already present
- download URL already present
- ZIP or binary archive already present
- absolute path exposure
- runtime file exposure
- manifest file content exposure
- export artifact content exposure
- export artifact content read/parse/copy request
- raw author identifier exposure
- secret-like value exposure
- original package row read request
- URL fetch request
- scraping request
- real API request
- real LLM request
- B-end, Sandbox, or public event generation attempt
- Evidence Layer write attempt
- production case, review queue, or dedup creation attempt

## Public Access / External Delivery Separation

The following are separate future layers:

- local package artifact generation
- public access gate
- public access runtime
- external delivery gate
- external delivery runtime
- B-end report gate/runtime
- Sandbox generation gate/runtime
- public event generation gate/runtime

Gate readiness is not a replacement for any runtime.

## Public Access Runtime Policy Placeholder

A future public access runtime, if separately approved, would need its own design for:

- allowed artifact classes
- redaction review
- expiration policy
- revocation policy
- access logging policy
- absolute path suppression
- content exposure controls
- route authorization
- operator audit
- abuse handling

Those concerns are intentionally not implemented in Phase 7X.

## External Delivery Runtime Policy Placeholder

A future external delivery runtime, if separately approved, would need its own design for:

- recipient scope
- delivery method
- delivery authorization
- delivery audit
- retraction policy
- redaction confirmation
- sensitive data checks
- no-secret transmission checks
- rate and abuse controls

Those concerns are intentionally not implemented in Phase 7X.

## Non-Overclaim Policy

The future gate must not be described as:

- public access completed
- external delivery completed
- customer delivery completed
- B-end report generated
- Sandbox generated
- public event generated
- official verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof
- production case promotion
- Evidence Layer publication
- trading, moderation, or real-world execution

