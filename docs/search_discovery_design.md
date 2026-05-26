# Search Discovery Design

Status: planning and static mock status only.

Search Discovery is the planned layer for finding candidate public-opinion evidence locations before any content extraction happens. It can return candidate URLs, titles, snippets, source names, and timestamps from approved discovery providers, RSS feeds, data vendors, user-provided URL lists, or mock fixtures.

Search Discovery is not crawling. It must not automatically fetch candidate URLs, scrape pages, bypass login, bypass captcha, evade anti-bot controls, use cookies, call real LLMs, or treat discovery metadata as full evidence text.

## What It Does

- Helps a user discover possible evidence sources for an event or keyword.
- Returns URL/title/snippet metadata only.
- Marks candidates as `pending_review`.
- Requires a user to accept or reject candidates before they can affect a case.
- Routes accepted candidates into Manual URL Evidence, CSV/Excel import, or a separately reviewed public parser path.

## What It Does Not Do

- It does not fetch URLs.
- It does not scrape websites.
- It does not use cookies, browser sessions, proxies, captcha handling, or anti-bot bypasses.
- It does not collect private, login-only, paywalled, or hidden data.
- It does not call real YouTube, Douyin, Bilibili, search, website, or LLM APIs in the current implementation.
- It does not automatically attach candidates to a case.

## Relationship To Evidence Layer

Search Discovery emits `SearchDiscoveryCandidate` metadata. A candidate is not an `EvidenceItem` until a human reviews it and provides or authorizes usable text.

Accepted candidates should retain conservative provenance until stronger source
evidence exists. A candidate URL improves review context but is not verification.
If a user manually attaches copied text from a candidate URL, trust remains
conservative and duplicate text/URL submissions are collapsed by the Evidence
Layer.

Recommended flow:

```text
keyword/event query
  -> discovery provider or mock fixture returns URL/title/snippet candidates
  -> user reviews candidate list
  -> accepted candidates become manual_url evidence or wait for parser review
  -> EvidenceItem normalization
  -> deterministic offline case analysis
```

## Review Flow

1. User enters a keyword or event label.
2. A configured provider or mock fixture returns candidate URLs, titles, and snippets.
3. User reviews relevance, source lawfulness, and whether content should be used.
4. User accepts or rejects each candidate.
5. Accepted candidates can be:
   - manually attached with title/body/comment text through Manual URL Evidence
   - included in CSV/Excel evidence import
   - routed to a reviewed public parser only when source rules allow it
6. No page fetching occurs unless a later source-specific parser is explicitly reviewed, fixture-tested, and configured.

## Current Static API

```http
GET /api/v1/search-discovery/status
GET /api/v1/search-discovery/mock-candidates?query=Tesla
POST /api/v1/cases/{case_id}/search-discovery/candidates/attach
```

The status and candidate endpoints return static/mock metadata only. The attach endpoint accepts user-reviewed mock/static candidates and saves accepted candidates as conservative `EvidenceItem` records. These endpoints do not call real search APIs, fetch URLs, read credentials, expose secrets, or start crawlers.

## Candidate Schema Summary

`SearchDiscoveryCandidate` fields:

- `candidate_id`
- `query`
- `provider`
- `platform_hint`
- `title`
- `snippet`
- `url`
- `published_at`
- `source_name`
- `content_type_hint`
- `confidence`
- `acquisition_mode=search_discovery`
- `status=pending_review|accepted|rejected|attached`
- `safety_notes`

Accepted candidate evidence uses `acquisition_mode=search_discovery`, `provenance_type=search_discovery_candidate`, URL/title/snippet metadata only, conservative trust, and review-needed behavior. Rejected candidates are not attached.

## Safety Boundary

- Default status is `planning_mock_only`.
- Current mock endpoint uses `example.test` URLs.
- Provider credential presence is represented only as booleans.
- MediaCrawler is not integrated.
- Full content extraction remains out of scope for Search Discovery itself.
- Search discovery candidates must remain aggregate evidence leads, not targeting instructions.

## Future Work

- Mock Search Discovery UI for candidate review is implemented.
- Provider adapter design with strict no-fetch tests by default.
- RSS discovery pilot using fixture data first.
- GDELT/news discovery research.
- User-reviewed candidate attach workflow.
- Source-specific public parser routing only after compliance review.
