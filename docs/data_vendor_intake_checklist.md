# Data Vendor Intake Checklist

Status: planning and compliance checklist only. Sentigraph does not currently
call vendor APIs, store vendor credentials, or ship a real data-vendor adapter.

Use this checklist before accepting a third-party public-opinion dataset, sample
file, or API proposal. A vendor can move into a Sentigraph proof of concept only
after the source, rights, retention, and data-handling boundaries are clear.

## Intake Decision

Record one decision for each vendor review:

- `reject`: source or rights are unclear, or the vendor requires prohibited
  collection methods.
- `request_more_information`: vendor claims are plausible but not documented.
- `csv_poc_only`: approved only for a bounded CSV/Excel sample import.
- `legal_security_review`: commercial, privacy, or security review is required.
- `future_adapter_candidate`: consider API work only after POC, contract, DPA,
  quota, deletion, and security gates pass.

Do not implement a live adapter before the POC and compliance review are
complete.

## Vendor Identity

- Legal company name and registered jurisdiction.
- Website and product documentation.
- Primary contact, security contact, and legal/compliance contact.
- Business registration or equivalent proof when needed.
- Role: data controller, data processor, reseller, broker, or platform partner.
- Subprocessors or upstream data providers.
- References, customer examples, or platform partnership proof.
- Security posture: SOC 2, ISO 27001, penetration testing, incident response,
  or equivalent evidence if available.

## Supported Platforms

For each platform, record:

- Platform name and region.
- Data source route: official API, licensed firehose, platform partnership,
  reviewed public data, user panel, data vendor upstream, or other.
- Whether comments, replies, posts, videos, articles, metrics, and timestamps are
  supported.
- Whether deleted, private, paywalled, login-only, or age-restricted content is
  excluded.
- Coverage limits: keyword, account, geography, language, historical range, and
  update frequency.
- Whether the vendor can provide source URLs and stable platform content IDs.

## Data Fields

Ask for a data dictionary and sample file that identifies:

- Parent/root/content IDs and URL fields.
- Title, body text, comment text, and reply text fields.
- Public author labels and whether author IDs are hashed or raw.
- Created time, collected time, and timezone behavior.
- Like, reply, share, repost, view, and other interaction metrics.
- Language, source platform, query, collection method, and freshness fields.
- Deletion/takedown status, if available.
- Safe raw payload subset in `raw_data_safe`, with secrets and credentials
  excluded.

## Pricing Model

- Pricing unit: seats, API calls, records, monthly volume, platform, historical
  backfill, dashboard access, or support tier.
- Minimum commitment and cancellation terms.
- Overage pricing and rate-limit handling.
- Trial or POC pricing.
- Whether derived reports, screenshots, or client deliverables require an
  additional license.

## SLA And Operations

- Availability target.
- Freshness and ingestion latency.
- Historical backfill latency.
- Support hours and escalation path.
- Incident notification timing.
- Data correction and deletion propagation timing.
- Quota, throttling, and retry behavior.
- Change notification for schemas, fields, and upstream provider changes.

## Sample Data Requirements

A POC sample should:

- Use the same keyword, time window, and platform list agreed for the POC.
- Include 500 comments and 50 parent contents per platform when feasible.
- Use `acquisition_mode=data_vendor`.
- Include a clear data dictionary and collection-method statement.
- Include no credentials, cookies, API keys, tokens, session IDs, passwords, or
  private messages.
- Prefer public or legally licensed content with source URLs.
- Use stable IDs and timestamps.
- Include deletion/sync metadata if the vendor supports it.

## Compliance Questions

Ask the vendor to answer in writing:

- What is the lawful source of each platform dataset?
- Is the source official API, licensed data, platform partnership, public parser,
  user panel, or another method?
- Does collection comply with the source platform terms?
- Does collection use cookies, login sessions, captcha solving, proxy evasion,
  hidden APIs, or anti-bot bypass?
- Are private messages, private groups, paywalled content, or non-public account
  data excluded?
- Are minors, sensitive personal data, precise location, or government IDs
  collected?
- Which jurisdictions apply to collection, storage, and transfer?
- Can the vendor support deletion requests, takedowns, or source-content removal
  sync?
- Can the vendor provide a DPA and list subprocessors?

## Commercial Use Rights

Confirm whether Sentigraph and its users may:

- Store normalized `EvidenceItem` records.
- Run internal analytics and deterministic reports.
- Produce client-facing summaries and screenshots.
- Export derived aggregate reports.
- Keep derived aggregates after raw-data deletion, if allowed.
- Redistribute raw records or snippets, if allowed.
- Use data for model training or evaluation. Default should be no unless
  explicitly licensed and reviewed.

## Storage And Retention Rights

Record:

- Allowed retention period for raw vendor files and normalized evidence.
- Whether Sentigraph may keep only normalized evidence and safe metadata.
- Backup and archival rules.
- Deletion deadlines after contract termination.
- Whether derived aggregates can be retained.
- Whether public author names or IDs must be hashed.

## Deletion And Sync Policy

The vendor should explain:

- How deleted source content is represented.
- Whether takedown sync is available.
- Whether corrections and edits are delivered.
- How often sync events are sent.
- How Sentigraph should handle deletion in normalized evidence, reports, and
  audit logs.

## Personal Data Handling

Clarify:

- Public author IDs, usernames, display names, avatars, bios, and profile URLs.
- Whether fields are raw, hashed, pseudonymized, or aggregated.
- Sensitive-category handling.
- User deletion request handling.
- Cross-border transfer controls.
- Whether individual targeting, influenceability scoring, or persuasion
  profiling is prohibited. Sentigraph must not create those profiles.

## Contract And DPA Requirements

Before any real adapter or recurring data feed:

- Master service agreement or order form.
- Data processing agreement when personal data may be processed.
- Subprocessor list.
- Security schedule.
- Breach notification clause.
- Confidentiality clause.
- Audit rights or compliance evidence.
- Indemnity or warranty language for data rights.
- Termination and deletion language.

## Red Flags

Reject or escalate if a vendor:

- Markets "unlimited scraping" or "bypass" collection.
- Requires Sentigraph to provide cookies, account passwords, access tokens, or
  client secrets.
- Uses captcha bypass, proxy evasion, login-cookie crawling, hidden APIs, or
  anti-bot bypass without clear official permission.
- Cannot explain data source rights.
- Claims full-platform firehose access without documentation.
- Includes private messages, private groups, paywalled content, or login-only
  content without explicit rights.
- Refuses to provide a sample schema or data dictionary.
- Cannot support deletion/takedown obligations.
- Refuses DPA or subprocessor disclosure when personal data is involved.
- Includes credentials, cookies, API keys, tokens, or `.env`-like fields in
  sample data.
- Requires MediaCrawler or source-code crawler integration as the product path.

## Sentigraph Boundary

- Use vendor samples through CSV/Excel import for POC.
- Store normalized `EvidenceItem` records and safe metadata only.
- Keep `provenance_type=data_vendor` and verification conservative unless the
  contract and source route justify stronger labeling.
- Do not call vendor APIs, fetch URLs, scrape pages, use cookies, or integrate
  MediaCrawler during intake.
