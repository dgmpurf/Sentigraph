# OpenClaw / 龙虾 Usage Policy

Status: policy note only. OpenClaw is not integrated into Sentigraph.

This note defines how OpenClaw / 龙虾 may be used around Sentigraph without
turning it into a product crawler, production data source, or ingestion
pipeline dependency.

## Product Boundary

OpenClaw is not a core crawler, adapter, scheduler, connector, parser, or
production data source for Sentigraph.

Do not integrate OpenClaw into:

- `backend/app/services/crawling`
- `backend/app/services/evidence_ingestion.py`
- Search Discovery providers
- CSV/Excel import internals
- case run or monitoring pipelines
- background jobs, recurring fetch jobs, or production ingestion flows

There should be no OpenClaw API route, adapter factory entry, platform registry
entry, automated job, bundled skill execution path, or hidden fetch path inside
Sentigraph unless a future task explicitly reopens this policy with legal,
security, and product review.

## Allowed External Assistance

OpenClaw may be used only as external operator assistance outside the
Sentigraph ingestion pipeline:

- low-volume public evidence collection performed by a human operator;
- candidate URL/title/snippet organization;
- vendor documentation review and checklist preparation;
- local demo automation over Sentigraph's own local UI, using safe mock or
  non-secret sample data.

OpenClaw-assisted output must be reviewed by a human before it enters
Sentigraph. It should be treated as user-provided evidence, not official
platform data and not automatically verified evidence.

## Forbidden Uses

Do not use OpenClaw for:

- high-frequency scraping;
- login or cookie crawling;
- captcha bypass;
- anti-bot bypass;
- proxy evasion;
- hidden API access;
- private, paywalled, deleted, login-only, or restricted data collection;
- source-code crawler integration;
- recurring platform monitoring jobs;
- collecting credentials, tokens, cookies, `.env` values, private messages, or
  account-only data;
- automatically fetching or enriching URLs accepted in Sentigraph;
- claiming that screenshots, transcriptions, or user-submitted text were
  verified by Sentigraph or by a platform.

These boundaries are the same safety boundaries used for MediaCrawler-style
packages, unofficial scrape APIs, and scraping-as-a-service feeds.

## Allowed Entry Paths Into Sentigraph

Any OpenClaw-assisted material must enter Sentigraph through one of the existing
human-reviewed routes:

- Manual URL Evidence
- CSV/Excel Evidence Import
- Search Discovery candidate review

The operator must provide or confirm the public source context and lawful-use
basis. Sentigraph should store only normalized `EvidenceItem` records and safe
metadata, not OpenClaw runtime state, cookies, browser sessions, credentials, or
raw secret-bearing exports.

## Default Trust Mapping

OpenClaw-assisted evidence should use conservative trust/provenance labels:

- `provenance_type=manual_text` today, or `external_agent_assisted` if a future
  schema explicitly adds that value;
- `source_capture_method=external_agent_assisted` when available;
- `verification_status=user_attested_unverified`;
- `trust_label=low` or `medium_low`;
- `review_status=needs_review`;
- `user_attestation_required=true`.

Suggested `risk_flags`:

- `external_agent_assisted`
- `third_party_skill_risk`
- `source_unclear`
- `source_url_missing`
- `possible_secret_redacted`
- `needs_manual_review`

Official API evidence, platform-authorized OAuth evidence, reviewed public
parser evidence, and licensed vendor evidence must remain separate provenance
classes. OpenClaw-assisted evidence must not be upgraded to official API trust.

## Security Notes

Third-party skills, browser assistants, and local automation tools can expose
risk if they are run near secrets or private data. Do not run untrusted skills
or external assistants in a workspace, terminal, browser profile, or document
set that contains:

- `.env` files or copied environment values;
- API keys, OAuth tokens, cookies, client secrets, or vendor credentials;
- logged-in platform sessions;
- private client documents;
- private user data or restricted vendor samples.

For demos, use a clean browser context and safe local fixtures. Hide terminals
that might contain secrets. Review any generated CSV/Excel/JSON output before
importing it into Sentigraph.

## Vendor And Demo Use

OpenClaw may help organize vendor documentation, summarize non-confidential
terms, or prepare local demo artifacts. It does not replace vendor intake,
contract/DPA review, source-rights confirmation, deletion/sync review,
retention review, security review, or POC scoring.

For local demos, OpenClaw can help click through Sentigraph's own UI or prepare
non-secret sample files. It must not click through logged-in third-party
platforms to collect data, harvest cookies, or run hidden collection workflows.

## Review Requirement

OpenClaw-assisted evidence remains unverified until a human reviews source,
rights, trust, duplicates, and safety flags. Screenshots and transcriptions are
not automatically verified. Repeated submissions should be deduplicated and
treated as repetition signals, not as raw sentiment/risk amplification.

This policy keeps OpenClaw as optional external operator assistance while
preserving Sentigraph's core boundary: no scraping bypass, no hidden collection,
no credential exposure, no production crawler integration, and no automatic
truth guarantee.
