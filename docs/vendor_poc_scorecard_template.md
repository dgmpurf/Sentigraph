# Vendor POC Scorecard Template

Last updated: 2026-05-27

Status: fillable template for evaluating one third-party data vendor. This
template is for CSV/Excel sample POC review only. Do not call vendor APIs,
implement adapters, scrape, integrate MediaCrawler, or store secrets.

## Vendor Summary

| Field | Value |
| --- | --- |
| Vendor name |  |
| Legal entity / jurisdiction |  |
| Website / docs URL |  |
| Primary contact |  |
| Security / compliance contact |  |
| Reviewer |  |
| Review date |  |
| POC keyword / event |  |
| POC time window |  |
| POC platform list |  |
| Sample file name / hash |  |
| Sample received date |  |
| Intended use | Internal POC only |

## Source And Rights Snapshot

| Question | Answer / Evidence |
| --- | --- |
| Data source route |  |
| Official API / licensed feed / partnership / public collection / other |  |
| Platform terms reviewed? |  |
| Commercial analytics allowed? |  |
| Client-facing reports allowed? |  |
| Storage of normalized `EvidenceItem` allowed? |  |
| Retention limit |  |
| Deletion/takedown sync available? |  |
| DPA required or provided? |  |
| Subprocessors disclosed? |  |
| Personal data fields present? |  |

## Sample Import Summary

| Metric | Value |
| --- | ---: |
| Parent contents requested | 50 per platform target |
| Comments requested | 500 per platform target |
| Parent contents received |  |
| Comments received |  |
| Rows imported into preview |  |
| Rows committed |  |
| Rows rejected/skipped |  |
| Duplicate rows |  |
| Review-needed rows |  |
| Secret-like fields found |  |
| Missing source URL rate |  |
| Missing timestamp rate |  |
| Missing text rate |  |
| Freshness range (`created_at` -> `collected_at`) |  |

## Sentigraph Mapping

Use these defaults for accepted POC sample rows:

```text
acquisition_mode=data_vendor
provenance_type=data_vendor
verification_status=vendor_attested
trust_label=medium_low
```

If vendor attestation or source rights are incomplete, change
`verification_status` to `needs_review` and lower trust.

## Risk Flags

Check every applicable flag:

| Risk flag | Applies? | Notes |
| --- | --- | --- |
| `self_crawled_public_web` |  |  |
| `source_unclear` |  |  |
| `deletion_sync_unknown` |  |  |
| `personal_data_unknown` |  |  |
| Secret-like sample values found |  |  |
| Private/login-only data suspected |  |  |
| MediaCrawler/source-code crawler requirement |  |  |
| Captcha/proxy/login-cookie/anti-bot bypass suspected |  |  |
| Full-platform/firehose claim undocumented |  |  |

## Scoring

Use `docs/vendor_scoring_rubric.md` for detailed criteria.

| Category | Max points | Score | Notes |
| --- | ---: | ---: | --- |
| Compliance / contract readiness | 40 |  |  |
| Technical field completeness | 25 |  |  |
| Data quality | 20 |  |  |
| Risk control | 15 |  |  |
| Total | 100 |  |  |

## Classification

Choose one:

- `approved_poc`
- `limited_poc`
- `internal_research_only`
- `reject`

Classification:

```text

```

Rationale:

```text

```

## Recommended Next Action

Choose one:

- Reject vendor.
- Request missing compliance/source documentation.
- Request corrected sample file.
- Run limited internal CSV/Excel POC only.
- Run approved bounded CSV/Excel POC.
- Escalate to legal/security review.
- Consider future Data Vendor Adapter only after POC and compliance gates pass.

Notes:

```text

```

## Adapter Gate Check

Do not start adapter work unless every item is true:

| Gate | Pass? | Notes |
| --- | --- | --- |
| POC complete |  |  |
| Vendor selected |  |  |
| Contract / DPA complete |  |  |
| Retention and deletion/sync complete |  |  |
| Security review complete |  |  |
| API docs and sample payloads available |  |  |
| Mocked fixture tests planned |  |  |
| Credential handling design approved |  |  |
| Rate limits / quota / retry policy documented |  |  |

## Final Sign-Off

| Role | Name | Decision | Date |
| --- | --- | --- | --- |
| Product |  |  |  |
| Engineering |  |  |  |
| Legal / compliance |  |  |  |
| Security |  |  |  |

Final note:

```text
This scorecard does not authorize live vendor API calls, scraping, URL fetching,
MediaCrawler integration, or credential storage. It only records whether a
bounded vendor sample may be imported for Sentigraph POC analysis.
```
