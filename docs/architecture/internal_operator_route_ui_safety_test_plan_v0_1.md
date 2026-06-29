# Internal Operator Route/UI Safety Test Plan v0.1

## A. Purpose

This is a docs-only safety test plan for future internal operator route/UI implementation.

It does not implement tests.
It does not approve implementation.
It does not modify runtime behavior.
It does not modify backend code.
It does not modify frontend code.
It does not enable the route.

The purpose is to define the test families that must exist before any future route/UI implementation slice is approved.

## B. Test Families Overview

Future test families:

1. Disabled route behavior tests.
2. Falsey env route-disabled tests.
3. Enabled synthetic fixture tests.
4. GET-only route surface tests.
5. No public / C-end / B-end / customer alias tests.
6. Safe denial response tests.
7. Forbidden field absence tests.
8. No file-byte / no ZIP / no URL / no external delivery tests.
9. No evidence row opening tests.
10. No private collector / real package read tests.
11. No storage / no Evidence Layer write tests.
12. No production case / `analysis_run` tests.
13. Future UI safe display tests.
14. Future UI forbidden active action tests.
15. Static safety scans.

These test families are future requirements only. This phase does not create test files.

## C. Route Safety Test Plan

Future route tests must cover:

- Route disabled by default.
- Unset env disabled.
- `false` / `0` / unknown env disabled.
- Explicit `1` / `true` / `yes` only enters synthetic fixture mode.
- Enabled mode remains synthetic/test-only.
- Unknown candidate returns safe `not_found`.
- Existing route family remains GET-only.
- POST / PUT / PATCH / DELETE not approved.
- No public / C-end / B-end / customer alias.
- No provider callback route.
- No private collector callback route.

Expected assertions:

- Disabled responses use safe error envelope.
- Enabled synthetic responses remain metadata-only and review-only.
- Route registry contains only internal GET routes for this route family.
- No state-changing method exists for this route family.

## D. Safe Response Test Plan

Future tests must assert:

- `metadata_only = true`.
- `review_only = true`.
- `path_exposed = false`.
- `raw_metadata_exposed = false`.
- No absolute paths.
- No raw comments.
- No raw author identifiers.
- No evidence rows.
- No secrets.
- No `response_text`.
- No `generated_public_message`.
- No `target_user_list`.
- No `persuasion_score`.
- No `truth_score`.
- No `official_verified`.
- No `prediction_probability`.
- No `psychological_profile`.
- No `personality_diagnosis`.

Safe response tests must check both keys and serialized values. Required false-valued safety flag names may appear only as boundary metadata.

## E. File / Delivery Safety Test Plan

Future tests must assert no:

- `FileResponse`.
- `StreamingResponse`.
- ZIP generation.
- Archive generation.
- Public URL.
- Signed URL.
- External delivery.
- Email delivery.
- Object storage upload.
- Portal publication.
- File-byte response.

These checks should include route module static scans and route behavior checks where relevant.

## F. Evidence / Collector Safety Test Plan

Future tests must assert no:

- `evidence_items.jsonl` opening.
- `evidence_items.csv` opening.
- Full evidence row parsing.
- Raw row preview.
- Real package directory read.
- Private collector export root read.
- Private collector runtime access.
- Collector job run.
- HTTP/API bridge to collector.
- URL fetch.
- Scraping.
- Real API.
- Real LLM.

Tests may use guarded file-open monkeypatches and path-probe guards to prove synthetic fixture routes do not touch evidence row files or private collector roots.

## G. Storage / Production Side-effect Test Plan

Future tests must assert no:

- Persistent staging storage.
- Audit append unless separately approved.
- Review queue creation.
- Evidence Layer write.
- Production case creation.
- `analysis_run` creation.
- B-end report runtime.
- Sandbox / public event runtime.
- Public response generation.
- Publish / send / post / execute behavior.

Tests should also confirm no runtime files, database files, or production records are created by route/UI smoke checks.

## H. Future UI Safety Test Plan

Future UI tests must cover:

- UI not implemented until separately approved.
- If future UI exists, it must display only safe metadata.
- No raw rows / comments / identifiers / secrets / absolute paths visible.
- No `[object Object]`, `undefined`, `NaN`, or visible 500.
- No active production/public CTA.
- No download / export / open raw file / refresh live collector / fetch / scrape CTA.
- No public / C-end / B-end / customer route.
- Internal-only / local-only boundary copy visible.
- Metadata-only / review-only boundary copy visible.
- Not production import / no Evidence Layer / no production case / no `analysis_run` copy visible.

Browser smoke, if later approved, must remain local and must not call real APIs, fetch URLs, scrape pages, or touch private collector runtime.

## I. Static Scan Plan

Future static scans should search touched route/UI files for:

- `FileResponse`
- `StreamingResponse`
- `zip`
- `public_url`
- `signed_url`
- `external_delivery`
- `response_text`
- `generated_public_message`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`
- `evidence_items.jsonl`
- `evidence_items.csv`
- Collector runtime bridge language.
- Public / C-end / B-end alias route strings.

Matches are acceptable only in tests, docs, or explicit forbidden-boundary language.

## J. Required Pre-implementation Gate

Before any route/UI implementation:

1. This safety test plan must be accepted.
2. A first implementation slice design must be accepted.
3. User must explicitly approve implementation.
4. Targeted tests must be written before implementation.
5. Route must remain disabled by default unless a later explicit gate changes exactly that.

Any proposal to implement UI, auth runtime, route expansion, storage, evidence row preview, production import, public exposure, or collector runtime bridge must stop until a specific approval gate exists.

## K. Explicit Non-goals

- No tests implemented now.
- No backend code now.
- No frontend code now.
- No route behavior change now.
- No auth implementation now.
- No authorization implementation now.
- No UI implementation now.
- No storage now.
- No evidence row preview now.
- No production import now.
- No Evidence Layer write now.
- No production case / `analysis_run` now.
- No report runtime.
- No Sandbox / public event runtime.
- No collector runtime / API bridge.
