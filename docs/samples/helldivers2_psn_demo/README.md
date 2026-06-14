# Helldivers 2 PSN Evidence Sample

This folder contains a small real public sample package for the Helldivers 2 / PSN account linking controversy.

Package:

- `helldivers2-psn-demo_20260614_055754`

Summary:

- 34 evidence items
- 7 sources
- 28 comment samples
- 6 root / InfluenceCore candidates
- Validation passed with 0 errors
- Validation has 2 expected warnings:
  - one skipped Polygon source from the local environment
  - sample size below the larger target threshold

Scope and limitations:

- Selected public sample only
- Not full-web coverage
- Not full-platform coverage
- Not full-thread coverage
- Not official verification
- Not causal proof
- Not production data

Intended use:

- Sample package intake
- Fixture/reference for future Evidence -> Opinion Ecosystem mapping
- Documentation asset for validating Sentigraph Evidence Export v1 package shape

This sample has not been imported into the backend, mapped into real PeopleCluster/EchoBox objects, or used as production data.

## Local validation

Run the Sentigraph-side offline validator from the repository root:

```powershell
python scripts\validate_external_evidence_package.py docs\samples\helldivers2_psn_demo\helldivers2-psn-demo_20260614_055754 --case-keyword helldivers --case-keyword psn --case-keyword playstation --case-keyword steam
```

The validator is local and read-only. It does not import the package, call APIs, fetch URLs, scrape websites, use browser sessions, or verify the underlying public sources.
