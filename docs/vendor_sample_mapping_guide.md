# Vendor Sample Mapping Guide

Status: offline mapping and validation guidance only. This guide does not
authorize vendor API calls, live adapters, scraping, URL fetching, cookies,
MediaCrawler, or credential storage.

Use this guide when a vendor sends a bounded CSV or JSON sample for POC
evaluation before any real integration work.

## Mapping Principles

- Do not hardcode `compliance=true`.
- Do not treat vendor samples as official platform API data.
- Do not upgrade vendor evidence to high trust because a vendor name is present.
- Default vendor records to `acquisition_mode=data_vendor`.
- Default vendor provenance to `provenance_type=data_vendor`.
- Use `verification_status=vendor_attested` only when the sample includes a
  written vendor attestation or equivalent documented source/license basis.
- If attestation or source rights are missing, keep
  `verification_status=needs_review`.
- Default POC trust should be `trust_label=medium_low` at most until contract,
  source route, retention, and deletion/sync behavior are verified.
- Preserve unknown vendor fields only in safe metadata after secret-like fields
  are redacted or omitted.

## Required Conservative Flags

Use these `risk_flags` whenever the sample leaves uncertainty:

- `self_crawled_public_web`: the vendor says the sample was self-collected from
  public web pages instead of an official API, platform partnership, licensed
  feed, or user-authorized source.
- `source_unclear`: collection method, upstream provider, platform permission,
  or commercial-use basis is unclear.
- `deletion_sync_unknown`: source deletion, correction, takedown, or
  termination-deletion sync is unknown.
- `personal_data_unknown`: author identifiers, personal-data classification,
  retention, transfer, or data-subject request handling are unclear.

These flags do not automatically reject a POC sample, but they should keep the
sample in human review and prevent overclaiming.

## Offline Utility

`scripts/map_vendor_sample_to_evidence.py` maps local CSV or JSON files into
EvidenceItem-like JSONL or CSV for review.

Example:

```bash
python scripts/map_vendor_sample_to_evidence.py vendor_sample.csv \
  --vendor-name ExampleVendor \
  --platform news_site \
  --query "Tesla recall" \
  --output mapped_vendor_sample.jsonl
```

The utility:

- reads only local files;
- does not call vendor APIs;
- does not fetch URLs;
- does not scrape websites;
- does not execute formulas;
- treats cells starting with `=`, `+`, `-`, or `@` as plain text;
- redacts secret-like text and omits secret-like columns from safe metadata;
- handles ISO timestamps, Unix seconds, and Unix milliseconds;
- emits row-level validation warnings;
- stores vendor/compliance fields in `raw_data_safe` and
  `ingestion_metadata.warnings`.

## Output Semantics

The JSONL output is intended for POC inspection and future import tooling. Each
line contains normalized fields such as:

- `source_provider`
- `platform`
- `source_type`
- `acquisition_mode=data_vendor`
- `provenance_type=data_vendor`
- `verification_status`
- `trust_label`
- `risk_flags`
- `raw_data_safe`
- `ingestion_metadata`

Vendor evidence remains vendor-attested or review-needed, not verified by the
source platform. Imported vendor records should still pass through Evidence
Trust / Provenance / Deduplication and Evidence Review Queue before analysis or
demo use.

## What This Does Not Do

- It does not prove the vendor has lawful rights.
- It does not verify screenshots, article content, comments, or author claims.
- It does not check source URLs by visiting them.
- It does not import private/login-only content.
- It does not enable a recurring data feed.
- It does not approve a future Data Vendor Adapter.

Adapter work remains blocked until the vendor passes the POC, contract/DPA,
retention/deletion, security, quota, mocked-fixture, and credential-handling
gates described in `docs/vendor_poc_plan.md` and
`docs/vendor_scoring_rubric.md`.
