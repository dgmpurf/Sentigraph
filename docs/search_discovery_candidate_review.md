# Search Discovery Candidate Review

Status: mock-only UX scaffold implemented.

This workflow lets a user review deterministic mock Search Discovery candidates and attach accepted candidates to a case as normalized `EvidenceItem` records. It is a safe product rehearsal for future search providers. It is not live search.

## What It Does

1. User enters a keyword/event query in the Search Discovery page.
2. Sentigraph calls the local mock endpoint:
   `GET /api/v1/search-discovery/mock-candidates?query=Tesla`
3. The UI shows candidate URL/title/snippet metadata.
4. User marks candidates as accepted or rejected.
5. Accepted candidates can be attached to a selected case through:
   `POST /api/v1/cases/{case_id}/search-discovery/candidates/attach`
6. Attached candidates become `EvidenceItem` records with:
   - `acquisition_mode=search_discovery`
   - `provenance_type=search_discovery_candidate`
   - `verification_status=source_url_provided_unverified`
   - conservative low trust
   - review-needed behavior

## What It Does Not Do

- It does not call real search APIs.
- It does not fetch candidate URLs.
- It does not scrape websites.
- It does not use cookies, sessions, proxies, captcha handling, or anti-bot bypasses.
- It does not call real YouTube, Douyin, Bilibili, website, or LLM APIs.
- It does not claim candidate snippets are full source content.
- It does not verify screenshots, candidate URLs, or source authenticity.

## Evidence Behavior

Accepted candidates save metadata only:

- title
- snippet as `body_text`
- URL
- source name
- platform/content hints
- safe mock provider metadata

Rejected candidates are not converted to evidence. Candidate URL content remains unfetched. Users must later supplement full article/comment text manually, import a lawful dataset, or route a source through a reviewed public parser if one is allowed.

## Review And Trust

Search Discovery candidate evidence is intentionally conservative. A URL improves context but is not verification. Candidate evidence appears in the Evidence Review Queue so a human can approve, reject, mark weak, request more source, or merge duplicates.

## Future Provider Plan

Future real provider support should stay behind:

- provider terms/quota review
- mocked contract fixtures
- no-fetch tests by default
- credential-present booleans only
- user review before attach
- no automatic scraping or full-content extraction
