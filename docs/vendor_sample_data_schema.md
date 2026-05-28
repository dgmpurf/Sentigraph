# Vendor Sample Data Schema

Status: sample-file schema for vendor POC review. This is not a live vendor API
contract and does not require vendor credentials.

Vendor samples should be delivered as CSV, Excel, or JSON that can be converted
to the same fields. Sentigraph should import the sample through the existing
CSV/Excel Evidence Import flow until a vendor is selected and a separate adapter
is approved.

## Required Sample Fields

| Field | Required | Type | Mapping / Notes |
| --- | --- | --- | --- |
| `source_provider` | yes | string | Vendor or dataset provider name. Store in safe metadata. |
| `platform` | yes | string | Source platform label, for example `youtube`, `weibo`, `news_site`, or vendor-specific platform name. |
| `source_type` | yes | string | Evidence source bucket such as `news_site`, `forum`, `public_web`, `uploaded_dataset`, or a supported platform source type. |
| `acquisition_mode` | yes | string | Must be `data_vendor` for vendor-provided samples. |
| `query` | recommended | string | Keyword/event query used to create the sample. |
| `content_id` | recommended | string | Stable platform/vendor content ID. |
| `parent_id` | optional | string | Parent comment/post/video/article ID. |
| `root_id` | optional | string | Root thread/video/article/post ID. |
| `url` | recommended | string | Public source URL when allowed. Sentigraph must not fetch it during import. |
| `title` | recommended | string | Article/video/post title. |
| `body_text` | conditional | string | Article/post/video description or parent content body. |
| `comment_text` | conditional | string | Comment or reply text. |
| `author_id` | optional | string | Public or pseudonymized author ID. Prefer hashed/pseudonymized IDs. |
| `author_name` | optional | string | Public display label if licensed and allowed. |
| `created_at` | recommended | ISO 8601 string | Time content was published on the source platform. |
| `collected_at` | recommended | ISO 8601 string | Time vendor collected the record. |
| `like_count` | optional | integer | Non-negative interaction metric. |
| `reply_count` | optional | integer | Non-negative interaction metric. |
| `share_count` | optional | integer | Non-negative interaction metric. |
| `view_count` | optional | integer | Non-negative interaction metric. |
| `repost_count` | optional | integer | Non-negative interaction metric; can map to `raw_data_safe.repost_count` if no first-class field exists. |
| `language` | optional | string | Language hint such as `zh-CN`, `en-US`, or `unknown`. |
| `raw_data_safe` | optional | object/string | Sanitized vendor payload subset with no secrets, credentials, cookies, private messages, or hidden account data. |

At least one of `title`, `body_text`, or `comment_text` must be present for each
row. Comment-only rows should include `comment_text`. Parent article/video/post
rows should include `title` and/or `body_text`.

## Compliance Metadata

Vendor sample files should include these columns or an accompanying data
dictionary:

| Field | Purpose |
| --- | --- |
| `collection_method` | Official API, licensed feed, platform partnership, public parser, user panel, or other documented source route. |
| `collection_basis` | Contract, platform agreement, public data terms, user consent, or other basis. |
| `source_terms_url` | URL to platform/vendor terms if available. |
| `vendor_license_id` | Contract, order, or license reference for the sample. |
| `commercial_use_allowed` | Whether commercial analysis/reporting is allowed. |
| `storage_allowed` | Whether Sentigraph may store normalized evidence. |
| `retention_allowed_until` | Retention deadline or policy reference. |
| `deletion_sync_supported` | Whether the vendor can send deletion/takedown updates. |
| `personal_data_classification` | Public, pseudonymized, personal data, sensitive, or vendor-specific classification. |
| `vendor_attestation` | Vendor statement that the sample is lawfully provided for POC analysis. |

These fields should map to `raw_data_safe` or `ingestion_metadata` rather than
becoming visible report text.

## Evidence Mapping

Recommended mapping into `EvidenceItem`:

- `acquisition_mode=data_vendor`
- `provenance_type=data_vendor`
- `verification_status=vendor_attested` only when the vendor attestation and
  contract/license basis are documented; otherwise use `needs_review`.
- `trust_label=medium_low` at most during POC unless official/platform source
  rights are independently verified.
- `source_provider`, `query`, `content_id`, `collected_at`, `repost_count`, and
  compliance fields should remain in safe metadata.
- Duplicates should be deduplicated by content and URL hashes.
- Rejected or low-trust vendor evidence should remain reviewable and excluded
  from default analysis if rejected.

## Forbidden Fields

Vendor samples must not include:

- API keys, OAuth tokens, refresh tokens, client secrets, session IDs, cookies,
  passwords, authorization headers, or `.env` values.
- Private messages, non-public group content, account-private fields, or data
  that requires login unless a reviewed contract explicitly permits it and the
  POC scope allows it.
- Raw browser profiles, crawler configuration, proxy lists, captcha outputs, or
  anti-bot bypass artifacts.
- Executable formulas, macros, scripts, or external-link instructions.

## Minimal CSV Example

```csv
source_provider,platform,source_type,acquisition_mode,query,content_id,parent_id,root_id,url,title,body_text,comment_text,author_id,author_name,created_at,collected_at,like_count,reply_count,share_count,view_count,repost_count,language,collection_method,vendor_attestation
ExampleVendor,news_site,news_site,data_vendor,Tesla recall,article_001,,article_001,https://example.test/news/001,Tesla service update,Public article summary about service response,,author_hash_001,Reporter A,2026-05-20T08:00:00Z,2026-05-20T09:00:00Z,12,3,5,1200,0,en,licensed_feed,true
ExampleVendor,weibo,public_web,data_vendor,Tesla recall,comment_001,post_001,post_001,https://example.test/post/001,,,"Users ask for a clearer repair timeline.",user_hash_001,Public User,2026-05-20T08:10:00Z,2026-05-20T09:01:00Z,8,2,1,0,4,en,licensed_feed,true
```

## JSON Shape Example

```json
{
  "source_provider": "ExampleVendor",
  "platform": "news_site",
  "source_type": "news_site",
  "acquisition_mode": "data_vendor",
  "query": "Tesla recall",
  "content_id": "article_001",
  "root_id": "article_001",
  "url": "https://example.test/news/001",
  "title": "Tesla service update",
  "body_text": "Public article summary about service response",
  "created_at": "2026-05-20T08:00:00Z",
  "collected_at": "2026-05-20T09:00:00Z",
  "language": "en",
  "compliance": {
    "collection_method": "licensed_feed",
    "commercial_use_allowed": true,
    "vendor_attestation": true
  }
}
```

Until JSON import is implemented, convert JSON samples into CSV/Excel using the
same field names before importing into Sentigraph.

## Validation Checks

Before importing a vendor sample:

- Confirm `acquisition_mode=data_vendor`.
- Confirm no secret-like fields or values are present.
- Confirm source/provider/license metadata is present.
- Confirm `created_at` and `collected_at` are parseable.
- Confirm metric fields are non-negative integers.
- Confirm rows have at least one analyzable text field.
- Confirm public source URLs are present where the vendor can legally provide
  them.
- Confirm duplicates are expected and can be evaluated.
- Confirm the sample is covered by the POC and retention terms.
