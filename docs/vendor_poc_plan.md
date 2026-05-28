# Vendor POC Plan

Status: planning guide for evaluating data vendors before adapter work. This
POC uses CSV/Excel import only; it does not call vendor APIs or add a live data
feed.

## Purpose

The vendor POC answers one question: can a third-party provider supply lawful,
usable, and cost-effective public-opinion evidence that improves Sentigraph
analysis without violating the project's no-scraping, no-cookie, no-bypass, and
no-secret boundaries?

## POC Scope

Use the same scope for every vendor so results are comparable:

- Same keyword or event query.
- Same time window.
- Same platform list.
- 500 comments plus 50 parent contents per platform, when the platform/source
  supports that split.
- Import via CSV/Excel using `acquisition_mode=data_vendor`.
- No vendor API integration, no live polling, no URL fetching, no scraping, no
  MediaCrawler, and no secrets.

## Step-by-Step Plan

1. Run the intake checklist in `docs/data_vendor_intake_checklist.md`.
2. Agree on POC keyword, time window, platform list, retention period, and
   permitted use.
3. Ask the vendor for a data dictionary and sample file following
   `docs/vendor_sample_data_schema.md`.
4. Confirm the sample contains no credentials, cookies, private messages, or
   prohibited acquisition artifacts.
5. Import the sample through the existing CSV/Excel Evidence Import flow.
6. Review Evidence Scale / Coverage, trust/provenance, deduplication, review
   queue, and audit behavior.
7. Run deterministic offline analysis only after review gates are clear.
8. Compare quality, coverage, freshness, field completeness, duplication, trust,
   and cost across vendors.
9. Produce a vendor scorecard and one of these recommendations: reject,
   CSV-only, repeat POC, legal/security review, or future adapter candidate.

## Evaluation Criteria

| Area | What to measure |
| --- | --- |
| Coverage | Platforms covered, query relevance, parent/content coverage, comments/replies coverage, language coverage. |
| Duplication | Duplicate rate, duplicate causes, stable IDs, same URL/text repetition. |
| Freshness | Delay between `created_at` and `collected_at`; update frequency if vendor offers recurring data. |
| Field completeness | URL, title/body/comment, parent/root IDs, timestamps, metrics, author labels, language, compliance metadata. |
| Trust and provenance | Collection method, source rights, vendor attestation, deletion/sync support, review-needed rate. |
| Compliance | Commercial-use rights, retention rights, DPA readiness, personal data handling, prohibited-source absence. |
| Cost | Unit economics, minimum commitment, overages, historical backfill, support, and platform-specific pricing. |
| Operational fit | Schema stability, support responsiveness, SLA, incident/deletion notices, and export reliability. |

## Acceptance Gates

A vendor can become a future adapter candidate only if:

- Source rights and commercial-use rights are documented.
- POC sample meets the schema and contains no secrets.
- Contract/DPA needs are clear.
- Retention and deletion/sync behavior are acceptable.
- Sample quality is good enough for the target demo or customer workflow.
- The vendor does not require cookies, login bypass, captcha bypass, proxy
  evasion, hidden APIs, anti-bot bypass, MediaCrawler, or source-code crawler
  integration.
- Pricing and SLA are acceptable for the expected case volume.

## POC Output

Create a short internal scorecard:

- Vendor and sample date.
- POC keyword, time window, and platforms.
- Records imported and rejected.
- Duplicate rate.
- Missing-field rate.
- Review-needed rate.
- Freshness range.
- Trust/provenance summary.
- Compliance concerns.
- Estimated cost.
- Recommendation and next action.

## Adapter Gate

Do not build a Data Vendor Adapter until all are true:

- POC is complete.
- Vendor is selected.
- Contract, DPA, retention, deletion/sync, and security review are complete.
- API documentation and sample payloads are available.
- A mocked test fixture exists.
- Credential handling is designed without exposing secrets.
- Rate limits, quotas, retry behavior, and audit logs are defined.

Until then, vendor data enters Sentigraph only as user-reviewed CSV/Excel sample
evidence with `acquisition_mode=data_vendor`.
