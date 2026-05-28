# Vendor POC Scoring Rubric

Last updated: 2026-05-27

Status: docs-only rubric for evaluating third-party data vendors before any
API integration. Sentigraph does not call vendor APIs, implement adapters,
scrape websites, integrate MediaCrawler, or store vendor secrets during this
process.

## Purpose

Use this rubric after the vendor intake checklist and before deciding whether a
vendor sample can enter a bounded Sentigraph POC. The score measures vendor
readiness for compliant sample import through CSV/Excel, not readiness for a
live adapter.

Total score: 100 points.

## Hard Blockers

Any hard blocker overrides the numeric score and produces `reject` unless legal
and security reviewers explicitly decide otherwise:

- Vendor requires cookies, passwords, OAuth tokens, API keys, client secrets, or
  browser profiles from Sentigraph.
- Vendor uses or asks Sentigraph to use captcha bypass, proxy evasion,
  anti-bot bypass, hidden APIs, login-cookie crawling, or private-data access.
- Vendor requires MediaCrawler or source-code crawler integration as the product
  path.
- Vendor cannot identify data source rights or commercial-use rights.
- Vendor sample includes credentials, cookies, authorization headers, private
  messages, non-public account data, or `.env`-like fields.
- Vendor refuses deletion/retention discussion for data that may contain
  personal data.
- Vendor claims full-platform or firehose access without documentation.

## Scoring Categories

### 1. Compliance / Contract Readiness - 40 pts

| Criterion | Points | Evidence expected |
| --- | ---: | --- |
| Vendor identity and legal entity are verified | 5 | Registered entity, jurisdiction, website, contacts. |
| Data source route is documented | 8 | Official API, licensed feed, platform partnership, user panel, or other lawful basis. |
| Commercial-use rights are clear | 6 | Internal analytics, client reports, screenshots, derived aggregates, redistribution limits. |
| Storage and retention rights are clear | 5 | Retention period, backup policy, raw-file vs normalized-evidence rights. |
| Deletion/takedown sync policy is documented | 5 | Source deletion handling, corrections, sync cadence, termination deletion. |
| Personal data handling is documented | 5 | Author IDs/names, pseudonymization, sensitive data, DSR handling, cross-border transfer. |
| Contract/DPA path is realistic | 4 | MSA/order form, DPA, subprocessors, breach notice, security schedule. |
| Platform terms and prohibited collection methods are addressed | 2 | Explicit no-cookie/no-bypass/no-private-data statement. |

### 2. Technical Field Completeness - 25 pts

| Criterion | Points | Evidence expected |
| --- | ---: | --- |
| Required schema fields are present | 5 | `source_provider`, `platform`, `source_type`, `acquisition_mode=data_vendor`. |
| Stable IDs and hierarchy fields are present | 4 | `content_id`, `parent_id`, `root_id`, platform/vendor IDs. |
| Text fields are usable | 4 | At least one of `title`, `body_text`, `comment_text`; reply/comment split is clear. |
| Timestamps are complete and parseable | 3 | `created_at`, `collected_at`, timezone behavior. |
| Source URL fields are present when legally allowed | 3 | Public URL or source reference for review. |
| Interaction metrics are present and typed | 2 | Like/reply/share/view/repost counts as non-negative integers. |
| Language and platform/source metadata are present | 2 | Language hints, source names, source type buckets. |
| Safe raw/compliance metadata is structured | 2 | `raw_data_safe` excludes secrets and contains collection/compliance metadata. |

### 3. Data Quality - 20 pts

| Criterion | Points | Evidence expected |
| --- | ---: | --- |
| Sample matches POC scope | 4 | Same keyword, time window, platform list, 500 comments + 50 parent contents per platform when feasible. |
| Coverage is relevant and explainable | 4 | Query relevance, platform coverage, parent/comment balance, language coverage. |
| Freshness is acceptable | 3 | Reasonable `created_at` to `collected_at` delay and update expectations. |
| Duplication rate is acceptable and explainable | 3 | Duplicate rows, URL/text repetition, stable IDs. |
| Field completeness is high in practice | 3 | Low missing-rate for source URLs, timestamps, title/body/comment fields. |
| Import/review behavior is clean | 3 | CSV/Excel import warnings are manageable; review-needed rate is explainable. |

### 4. Risk Control - 15 pts

| Criterion | Points | Evidence expected |
| --- | ---: | --- |
| Secret and credential controls are clean | 4 | No API keys, cookies, tokens, passwords, authorization headers, or `.env` values. |
| Prohibited acquisition methods are absent | 4 | No scraping bypass, MediaCrawler requirement, hidden APIs, captcha/proxy/login-cookie path. |
| Review and trust labeling are conservative | 3 | Vendor evidence remains reviewable; unverified data is not overstated. |
| Personal-data risk is bounded | 2 | Pseudonymization or documented public-author handling. |
| Operational risk is bounded | 2 | SLA, schema-change notice, incident/deletion handling, support path. |

## Vendor Classification

| Classification | Typical score | Required conditions | Meaning |
| --- | ---: | --- | --- |
| `approved_poc` | 80-100 | No hard blockers; compliance score at least 30; risk-control score at least 12 | Proceed with bounded CSV/Excel POC using vendor sample data. |
| `limited_poc` | 60-79 | No hard blockers; source route is plausible; missing items are documented | Allow a smaller sample POC with review warnings and no customer-facing claims. |
| `internal_research_only` | 40-59 | No secret exposure; no direct adapter; material uncertainty remains | Use only for internal schema/quality research on static samples, not demos or client deliverables. |
| `reject` | 0-39 or any hard blocker | Rights, source, safety, or data handling are not acceptable | Do not import sample into Sentigraph except possibly as a quarantined legal/security artifact outside product flow. |

Classification can only improve after written evidence changes. A high data
quality score cannot compensate for unclear rights, prohibited collection
methods, or secret exposure.

## Sentigraph Evidence Mapping

Vendor POC records should map conservatively:

```text
acquisition_mode=data_vendor
provenance_type=data_vendor
verification_status=vendor_attested
trust_label=medium_low
```

Use `verification_status=vendor_attested` only when the vendor provides a
documented attestation and source/license basis. If not, use `needs_review` and
lower trust.

Default `trust_label=medium_low` means the vendor path is documented enough for
POC review, not that the content claims are true. Official platform confirmation
or a reviewed official API path may justify higher trust later. If vendor
attestation, source route, commercial-use rights, or deletion/sync behavior are
missing, keep the evidence at `needs_review` or `unverified`.

## Standard Vendor Risk Flags

Add these risk flags when applicable:

- `self_crawled_public_web`: vendor states that data was self-collected from
  public web pages rather than official/licensed channels. This is not
  automatically disqualifying, but it requires platform-terms and collection
  method review.
- `source_unclear`: vendor cannot clearly explain source route, upstream
  provider, platform permission, or license basis.
- `deletion_sync_unknown`: vendor cannot explain source deletion, correction,
  takedown, or contract-termination sync behavior.
- `personal_data_unknown`: author IDs/names, sensitive fields, retention,
  transfer, or data-subject handling are unclear.

Risk flags should appear in the scorecard, vendor notes, and imported
`EvidenceItem` metadata if a POC sample is accepted.

## Adapter Decision Boundary

This rubric does not approve a live adapter. A Data Vendor Adapter is future-only
until a vendor is selected and the POC, contract/DPA, retention/deletion,
security, quota, mocked-fixture, and credential-handling gates are complete.
