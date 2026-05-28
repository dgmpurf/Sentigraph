# Source Feasibility Matrix

Last updated: 2026-05-28

This matrix reframes Sentigraph ingestion around event-centered evidence rather
than platform-specific crawling. A source is usable only through a compliant
acquisition mode: official API, OAuth-authorized account data, fixture-backed
public parser, search-discovery metadata, user upload, manual URL entry, future
data vendor integration, or mock fixture.

The broader source catalog is documented in `docs/source_catalog.md`. This
matrix is the operational green/yellow/red layer for deciding whether a source
can be used now, needs approval/review, or must remain blocked.

Sentigraph must not integrate MediaCrawler as a core data source. MediaCrawler
or similar third-party crawler output may only be considered indirectly when a
user supplies an exported dataset and attests that the source, permissions, and
collection method were lawful. Sentigraph itself must not perform login-cookie
crawling, captcha bypass, proxy evasion, anti-bot bypass, hidden API access, or
private data collection.

OpenClaw / 龙虾 follows the same non-integration boundary. It may be used only
as external operator assistance for low-volume public evidence organization,
vendor documentation review, candidate URL/title/snippet organization, or local
demo automation. It must not become a Sentigraph crawler, adapter, scheduler, or
production ingestion source. Any OpenClaw-assisted material must enter through
Manual URL Evidence, CSV/Excel import, or Search Discovery candidate review with
low or medium-low trust and human review required. See
`docs/openclaw_usage_policy.md`.

Manual/user-uploaded/screenshot evidence is not automatically verified. Source
URLs, capture method, user attestation, trust label, verification status, and
duplicate counts must be carried as evidence provenance metadata.

Data vendors are a separate path from crawling. Contracted vendor sample files
can be green for bounded CSV/Excel POC import when rights, retention, deletion,
and personal-data handling are documented. Prospective vendors remain yellow
until intake and POC gates pass. Unofficial scrape APIs, scraping-as-a-service
feeds, and source-code crawler solutions remain red unless the user supplies an
exported dataset with lawful-source attestation and Sentigraph treats it only as
user-uploaded evidence.

## Status Legend

| Color | Meaning |
| --- | --- |
| green | Usable now through current Sentigraph code or safe manual/user-provided evidence attachment. |
| yellow | Possible later with official API approval, OAuth verification, compliant public parser review, or user-provided exports. |
| red | Do not crawl or fetch directly without official permission, OAuth authorization, or user-provided lawful data. |

## Green Sources

| Source | Allowed acquisition modes | Forbidden acquisition modes | Can collect now | Cannot currently collect | Current Sentigraph status | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| YouTube | `official_api_public`, `mock_fixture`, `user_upload` | Scraping, cookies, login bypass, captcha bypass, private/OAuth-only data | Public video metadata and public comments through official YouTube Data API v3 when locally configured; mocked fixtures in tests | Exhaustive comments, private/account-only data, broad production crawl, unbounded replies | Real-capable with cache/quota guardrails; mock default; case raw data and `EvidenceItem` normalization working | Keep tiny limits and cache; add broader quota strategy only after demo needs grow |
| user-uploaded CSV/Excel | `user_upload`, `mock_fixture` | Hidden source collection, credential-bearing files, private data without permission | User-provided article/comment/post rows normalized as `EvidenceItem` through CSV/Excel preview/commit | Live source collection, hidden-source discovery, credential-bearing files | CSV/Excel import is implemented with safe normalization, deduplication, trust/review labels, and no raw-file persistence by default | Keep import template and validation current |
| contracted data vendor sample/import | `data_vendor`, `user_upload` for exported files covered by contract/POC | Live vendor API before approval, unlicensed resale, secret-bearing files, private data outside contract | Bounded vendor sample files imported through CSV/Excel as normalized `EvidenceItem` records | Live vendor adapter, recurring feed, platform-wide capture, or unbounded backfill | Intake checklist, sample schema, and POC plan are documented; no adapter exists | Run vendor intake, contract/DPA review, and CSV/Excel POC before adapter design |
| manual URL import | `manual_url`, `user_upload` | Automatic live fetching without review, login/captcha bypass | User-entered title/body/comment/url metadata as manual evidence | Automatic URL page fetch, dynamic comments, private content | Manual Evidence UI can store safe URL/title/body/comment fields without fetching URLs | Keep review/attestation wording visible |
| mock fixtures | `mock_fixture` | Treating mock data as real platform data | Deterministic posts/comments for tests and demos | Real platform state | Default safe mode across adapters and tests | Keep as regression baseline |
| RSS public feeds | `public_parser`, `manual_url`, `user_upload`, `mock_fixture` | Private feeds, paywalled content, subscriber-only metadata | Public feed metadata when terms permit it | Hidden comments or full articles outside feed permission | Catalog/planning source; no connector yet | Add fixture/import pilot only if needed |

## Yellow Sources

| Source | Allowed acquisition modes | Forbidden acquisition modes | Can collect now | Cannot currently collect | Current Sentigraph status | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| Douyin | `official_api_oauth` after Web App OAuth and `item.comment` verification; `user_upload`; `mock_fixture` | Scraping, cookies, captcha bypass, login bypass, anti-bot evasion, unauthorized `item_id` discovery | Mock Douyin-style data; future user-provided lawful exports | Real comments, keyword discovery, unauthorized videos/comments | Web App developer access recorded; OAuth, redirect URI, whitelist, token flow, `item.comment`, and lawful `item_id` source pending | Verify console gates before any real call |
| Bilibili | Official API after approval; `user_upload`; `mock_fixture` | Page scraping, cookies, private/member-only data, hidden APIs | Mock Bilibili-style data; future user-provided exports | Real comments/danmu via official API | Adapter scaffold, approval pending | Confirm official API permission and capture sanitized fixtures |
| Xiaohongshu | Official API after comment/note permission confirmation; `user_upload`; `mock_fixture` | Scraping, login-cookie collection, anti-bot bypass | Mock note/comment data; future user-provided exports | Real note/comment data | Developer access recorded, comment API unknown/not confirmed | Verify console product and note/comment scope |
| Weibo | Official API after approval and company-age gate; `user_upload`; `mock_fixture` | Scraping, cookies, login bypass, private messages | Mock Weibo-style microblog/comment data | Real public comments via official API | Company-age requirement pending | Recheck official API eligibility |
| Reddit | Official API after approval; `user_upload`; `mock_fixture` | Public-page scraping as API-approval bypass | Mock Reddit-style data | Real Reddit posts/comments | API approval pending | Wait for approval; use PRAW only after approval |
| Toutiao | Official API after approval; reviewed public-parser fixture only; `user_upload`; `mock_fixture` | Scraping without permission, dynamic hidden endpoints | Mock Toutiao-style data; future fixture records | Real comments/articles through official route | Adapter scaffold, permission pending | Verify official API or compliant public parser route |
| The Paper | Reviewed public parser fixture, optional compliant public-page pilot when explicitly enabled; `user_upload`; `mock_fixture` | Login/captcha/paywall/private data, broad crawler behavior | Fixture article data; optional low-rate public article pilot already guarded | Dynamic comments requiring login or scripts | Public parser scaffold with fixture-first behavior | Keep fixture-first; live fetch only after explicit review |
| Jiemian | Reviewed public parser fixture; `user_upload`; `mock_fixture` | Login/captcha/dynamic private comment collection | Fixture article data | Comments not exposed in fixture without login/dynamic loading | Public parser scaffold, fixture-only | Keep fixture-first; review compliant public page access before live work |
| Hupu | Reviewed public parser fixture; `user_upload`; `mock_fixture` | Login/captcha/anti-bot bypass, cookies | Fixture thread and visible replies | Broad live crawling and authenticated content | Public parser scaffold, fixture-only | Keep fixture regression coverage |
| Tieba | Reviewed public parser fixture; `user_upload`; `mock_fixture` | Login/captcha/anti-bot bypass, cookies | Fixture thread and visible replies | Broad live crawling and authenticated content | Public parser scaffold, fixture-only | Keep fixture regression coverage |
| NGA | Reviewed public parser fixture; `user_upload`; `mock_fixture` | Login/captcha/anti-bot bypass, cookies | Fixture thread and visible replies | Broad live crawling and authenticated content | Public parser scaffold, fixture-only | Keep fixture regression coverage |
| Maimai | Reviewed public parser fixture; `user_upload`; `mock_fixture` | Login/captcha/anti-bot bypass, cookies, private workplace data | Fixture workplace/industry discussion and visible replies | Live authenticated content, private identity/workplace data | Public parser scaffold, fixture-only | Keep fixture-only unless a compliant public source is verified |
| search discovery | `search_discovery` metadata from approved provider/mock fixture/user-provided URL list; `manual_url` after review | Search scraping, SERP scraping without permission, URL auto-fetching, full-content extraction without approved route, anti-bot bypass | Static/mock URL-title-snippet candidates, mock candidate attach, and user-reviewed URL lists | Automatic all-web search ingestion, automatic page content extraction | Static status/mock candidate endpoints and mock-only candidate attach are available; no real provider configured | Keep mock candidate-review QA stable; research RSS/GDELT/news APIs with fixtures first |
| RSS/GDELT mock providers | `search_discovery` from local fixtures only | Live RSS polling, real GDELT calls, URL fetching, scraping, automatic full-content extraction | Local `rss_mock` and `gdelt_mock` URL/title/snippet candidates with review-needed attach behavior | Real feed/API data, full article text, automatic enrichment | Provider taxonomy and mock fixture outputs implemented; no live provider configured | Use for demos/tests; real RSS/GDELT remains future terms/quota/no-fetch work |
| prospective data vendors | `data_vendor` after intake, contract, DPA, sample review, and POC; CSV/Excel sample import only before adapter | Live API integration before vendor selection, unlicensed samples, credentials in sample files, scraping-as-a-service without documented rights | Reviewed sample files only if lawful source and retention terms are documented | Recurring feed, live API calls, or production adapter | Planning path documented in `docs/data_vendor_intake_checklist.md`, `docs/vendor_sample_data_schema.md`, and `docs/vendor_poc_plan.md` | Compare vendors through bounded POC before any adapter work |
| general news/media sites | `public_parser`, `manual_url`, `search_discovery`, `user_upload`, `data_vendor` | Paywall bypass, login-only comments, copyright bulk copying | Public article/title/body metadata through reviewed feeds/parsers or user-provided evidence | Broad live crawling and restricted comments | Catalog entries include 36Kr, Huxiu, Sina, NetEase, Tencent News, Xinhua, People, Reuters, BBC, The Guardian | Add source-specific fixtures only after review |
| Q&A sites | `official_api_public`, `official_api_oauth`, `public_parser`, `manual_url`, `user_upload` | Login-only/private answer/comment data, hidden APIs | Public Q&A evidence if official/API/parser path is approved | Private profiles/messages | Catalog entries include Zhihu, Stack Exchange, Quora | Verify source-specific API and terms |
| complaint/review sites | `official_api_public`, `public_parser`, `manual_url`, `user_upload`, `data_vendor` | Private order/support data, identity enrichment, login-only reviews | Public complaints/reviews through approved APIs/feeds or user upload | Private support tickets and account data | Catalog entries include Black Cat Complaint, App Store, Google Play, Steam, Trustpilot | Design redaction/import checks before use |
| finance/investor forums | `official_api_public`, `public_parser`, `manual_url`, `user_upload`, `data_vendor` | Trading-advice profiling, private account data, scraping bypass | Public investor discussion evidence with compliance review | Account-level financial profiling | Catalog entries include Xueqiu, Eastmoney Guba, StockTwits | Review licensing and financial disclaimers |
| global social platforms | `official_api_public`, `official_api_oauth`, `manual_url`, `user_upload`, `data_vendor` | Private messages, cookies, scraping bypass, anti-bot evasion | Public social evidence through official/vendor/user-provided routes | Broad unapproved scraping | Catalog entries include X/Twitter, Bluesky, Mastodon | Research API terms source by source |

## Red Sources

| Source | Allowed acquisition modes | Forbidden acquisition modes | Can collect now | Cannot currently collect | Current Sentigraph status | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| Kuaishou | Official API only after permission; user-provided lawful exports; mock fixture | Direct crawl, cookies, captcha bypass, anti-bot bypass, unauthorized livestream/comment access | Mock Kuaishou-style data only | Real posts/comments/livestream comments | Adapter scaffold, real mode disabled | Verify official API and permission scope before any real work |
| Zhihu | Official API only after permission; user-provided lawful exports; mock fixture | Scraping, cookies, login bypass, private answer/comment data | Mock Zhihu-style data only | Real Q&A/article/comment data | Adapter scaffold, real mode disabled | Verify official API access and limits |
| Douban | Official API only after permission; user-provided lawful exports; mock fixture | Scraping, cookies, private group data, login bypass | Mock Douban-style data only | Real review/group/topic/comment data | Adapter scaffold, real mode disabled | Verify official API access and public data scope |
| unofficial scrape APIs / scraping-as-a-service | None as a core source; user-upload only after lawful-source attestation and compliance review | Cookies, hidden APIs, captcha/anti-bot bypass, proxy evasion, private data, unlicensed resale, platform-term bypass | Nothing directly through Sentigraph | Live collection, direct adapter, recurring feed, or automatic import | Not integrated; internal research only when legal/compliance review allows review of static samples | Reject by default; use official APIs, licensed vendors, reviewed public parsers, or user-provided lawful data instead |
| source-code crawler solutions / MediaCrawler-style packages | None as a core source; exported datasets only as user-uploaded evidence with lawful-source attestation | Integrating crawler code, login-cookie crawling, captcha bypass, proxy evasion, anti-bot bypass, private-data collection | Nothing directly through Sentigraph | Product crawler integration or automatic platform collection | Explicitly not integrated | Keep out of product; evaluate only lawful exported sample files, never crawler runtime integration |
| OpenClaw / 龙虾 runtime integration | None as a core source; external operator output may enter only through `manual_url`, `user_upload`, or `search_discovery` review with attestation | Product adapter integration, high-frequency scraping, login-cookie crawling, captcha bypass, anti-bot bypass, proxy evasion, private data, credential collection, automated URL fetching | Nothing directly through Sentigraph; only human-reviewed URL/title/snippet/text artifacts can be imported | Core crawler role, production data feed, hidden fetch path, recurring platform collection, or official-trust upgrade | Not integrated; policy note only | Keep outside the product pipeline; use `docs/openclaw_usage_policy.md` and mark assisted evidence low/medium-low trust with `needs_review` |

## Evidence Mapping

All allowed or user-provided records should normalize into `EvidenceItem` before
downstream analysis. Typical mappings:

- Video or post metadata: `evidence_type=video` or `post`, title/body text,
  public URL, interaction metrics, and safe metadata.
- Article pages: `evidence_type=article`, title, body text, public URL, and
  public source metadata.
- Comments and replies: `evidence_type=comment` or `reply`, `root_id`,
  `parent_id`, comment text, public URL, and interaction counts.
- Interaction counts: `evidence_type=interaction_metric` only when the record is
  a standalone metric artifact; otherwise counts stay on the video/post/comment
  evidence item.

Evidence ingestion is normalization, not collection. It must not call real APIs,
real LLM APIs, live public fetching, crawlers, or scraping bypasses. It must not
store or return API keys, `.env` values, cookies, OAuth tokens, authorization
headers, client secrets, private messages, or hidden account data.

Search Discovery is green only for URL/title/snippet metadata, mock fixtures,
RSS/feed metadata after review, and user-reviewed URL lists. Candidate URLs do
not authorize Sentigraph to fetch page content. Full content extraction requires
an official API, a reviewed public parser, licensed vendor data, or text supplied
by the user through Manual URL Evidence or CSV/Excel import.

The current `rss_mock` and `gdelt_mock` providers are local fixtures only. They
prepare the review UX for future all-web discovery but do not call RSS feeds,
GDELT, search APIs, websites, or platform APIs.
