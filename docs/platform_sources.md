# Sentigraph Platform Sources

Sentigraph now prioritizes Chinese public opinion platforms for future source integration while keeping Reddit visible in the project as a future real adapter candidate.

The current MVP product flow remains mock-first. No real crawler, login bypass, captcha bypass, anti-bot evasion, paywall bypass, proxy rotation, browser-cookie use, or private data collection is implemented in this phase. Reddit API access is now marked `api_pending`: mock mode is available, but real Reddit API mode is disabled until API approval is granted. Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, and Toutiao now have official API adapter scaffolds with mock data only; real API mode remains disabled until credentials, approval, permission scopes, and implementation are added. Douyin and Xiaohongshu developer access is recorded as obtained by the user, but their comment/note-comment API permissions are not yet verified. `POST /api/v1/crawl/start` routes Reddit, Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, and Toutiao requests through the adapter layer and returns normalized mock data with safe status metadata.

Cross-platform adapter QA is now stabilized with a parametrized local test matrix. The matrix verifies factory registration, mock-only official adapter behavior, safe blocked real-mode metadata, credential redaction, `/crawl/start` metadata, public parser fixture preview, and schema-valid `RawPost` / `RawComment` output without making real platform API calls.

## Data-source readiness layer

Sentigraph exposes platform readiness through `GET /api/v1/platforms/status`. The status layer is safe for frontend display and contains only non-secret metadata:

- `mock_available`
- `real_mode_available`
- `api_approval_required`
- `api_approval_status`
- `developer_access_status`
- `comment_api_status`
- `real_mode_blocker`
- `credentials_required`
- `credentials_present` as present/missing booleans only
- `enabled_in_mvp`
- `selectable_for_mock`
- `selectable_for_real`

Current global status:

- Reddit: `api_pending`; mock mode available; real API mode disabled until Reddit approval is granted.
- Reddit scraping: not implemented and not used to bypass API approval.
- Official API planned platforms: Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, Toutiao.
- Weibo: official API adapter scaffold available in mock mode; real API mode disabled and not called.
- Bilibili: official API adapter scaffold available in mock mode; real API mode disabled and not called.
- Douyin: official API adapter scaffold available in mock mode; developer access obtained; comment permission not verified; real API mode disabled and not called.
- Kuaishou: official API adapter scaffold available in mock mode; real API mode disabled and not called.
- Xiaohongshu: official API adapter scaffold available in mock mode; developer access obtained; note/comment API availability not verified; real API mode disabled and not called.
- Zhihu: official API adapter scaffold available in mock mode; real API mode disabled and not called.
- Douban: official API adapter scaffold available in mock mode; real API mode disabled and not called.
- Toutiao: official API adapter scaffold available in mock mode; real API mode disabled and not called.
- Crawler-later platforms: Hupu, Baidu Tieba, Tianya, NGA, Maimai, The Paper / Pengpai News, Jiemian News.
- YouTube: `disabled_or_optional_future`.

## MVP mock-selectable platforms

MVP selections are limited to platforms that can run with local mock data. Selecting these platforms only changes the offline mock workflow; it does not call real third-party APIs or real crawlers.

| platform_id | display_name | category | source_type | selectable_for_mock |
| --- | --- | --- | --- | --- |
| `reddit` | Reddit | `future_real_adapter_candidate` | `mock_data_future_adapter_placeholder` | true |
| `weibo` | Weibo | `official_api_planned` | `official_api_adapter_scaffold` | true |
| `bilibili` | Bilibili | `official_api_planned` | `official_api_adapter_scaffold` | true |
| `douyin` | Douyin | `official_api_planned` | `official_api_adapter_scaffold` | true |
| `kuaishou` | Kuaishou | `official_api_planned` | `official_api_adapter_scaffold` | true |
| `xiaohongshu` | Xiaohongshu | `official_api_planned` | `official_api_adapter_scaffold` | true |
| `zhihu` | Zhihu | `official_api_planned` | `official_api_adapter_scaffold` | true |
| `douban` | Douban | `official_api_planned` | `official_api_adapter_scaffold` | true |
| `toutiao` | Toutiao | `official_api_planned` | `official_api_adapter_scaffold` | true |

## official_api_planned

These platforms should be integrated through official API programs when credentials, permissions, usage limits, and compliance requirements are available. They may be selectable for mock analysis in the MVP, but they must not trigger real API calls yet.

| platform_id | display_name | official_platform_url | MVP status |
| --- | --- | --- | --- |
| `weibo` | Weibo | https://open.weibo.com | mock adapter scaffold; real API pending credentials/approval |
| `bilibili` | Bilibili | https://openhome.bilibili.com | mock adapter scaffold; real API pending credentials/approval |
| `douyin` | Douyin | https://developer.open-douyin.com | mock adapter scaffold; developer access obtained; comment permission not verified |
| `kuaishou` | Kuaishou | https://open.kuaishou.com | mock adapter scaffold; real API pending credentials/approval |
| `xiaohongshu` | Xiaohongshu | https://open.xiaohongshu.com | mock adapter scaffold; developer access obtained; note/comment API not verified |
| `zhihu` | Zhihu | https://open.zhihu.com | mock adapter scaffold; real API pending credentials/approval |
| `douban` | Douban | https://developers.douban.com | mock adapter scaffold; real API pending credentials/approval |
| `toutiao` | Toutiao | https://open.toutiao.com | mock adapter scaffold; real API pending credentials/approval |

## future_real_adapter_candidate

| platform_id | display_name | MVP status | notes |
| --- | --- | --- | --- |
| `reddit` | Reddit | `api_pending`; mock-selectable | Reddit stays visible and selectable for mock analysis. The adapter defaults to local mock data and does not require credentials. Real API mode is disabled until Reddit approval is granted. |

### Reddit adapter scaffold

The first real-data preparation step is a shared platform adapter interface plus a Reddit adapter scaffold.

Current behavior:

- Default mode is `mock` through `REDDIT_ADAPTER_MODE=mock`.
- If Reddit credentials are missing, the adapter falls back to local mock data from `mock_data/raw_comments.json`.
- Mock mode normalizes local Reddit-like comments into the same `RawPost` and `RawComment` schemas used by the rest of Sentigraph.
- Real API mode is disabled while Reddit API approval is pending, even if `REDDIT_ADAPTER_MODE=real` and credentials are present.
- Passing a code-level `mode="real"` request is not enough by itself; the approval gate, environment gate, and credentials must all allow real mode before any real API client can be initialized.
- PRAW remains the planned official Reddit API dependency for later approved real mode, but the current adapter must not call Reddit while status is `api_pending`.
- Public-page scraping is not implemented and must not be used to bypass Reddit API approval.
- Adapter status is visible through `health_check()` and `get_status_metadata()`, including environment mode, requested mode, active mode, credential presence, fallback reason, `mock_available`, `api_pending`, and `real_mode_disabled`.
- `POST /api/v1/crawl/start` uses `adapter_factory.get_adapter("reddit")` when Reddit is selected and returns safe adapter metadata plus normalized `RawPost` / `RawComment` mock fallback data. Safe diagnostics include only real-mode reached status, dependency availability, exception class name, sanitized error category, and approval/fallback flags.
- The current case flow and mock dashboard remain mock-first and do not require real Reddit credentials.

Future real Reddit mode credentials after approval:

```text
REDDIT_CLIENT_ID
REDDIT_CLIENT_SECRET
REDDIT_USER_AGENT
REDDIT_ADAPTER_MODE=real
```

Adapter contract:

- `search_posts(keyword, limit, sort, date_range)`
- `fetch_comments(post_id, limit)`
- `normalize_post(raw)`
- `normalize_comment(raw)`
- `health_check()`
- `supports_real_mode()`
- `get_required_credentials()`

Factory behavior:

- `get_adapter("reddit")` and `get_platform_adapter("reddit")` return the Reddit adapter.
- Unknown platforms return a safe adapter registration error.
- Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, and Toutiao have mock-only official API adapter scaffolds. Douyin and Xiaohongshu now record developer access obtained but keep comment/note-comment permission as unverified. Other official API planned platforms remain registry entries only until credentials, permissions, and product behavior are reviewed.
- Crawler-later platforms remain inactive for real collection.

Safety constraints:

- Use the official Reddit API path only after approval is granted.
- Do not use public-page scraping to bypass API approval.
- Do not implement login bypass, captcha bypass, anti-bot evasion, or private data collection.
- Do not store Reddit credentials in the repository.
- Add fixture-first tests before expanding real-mode behavior.
- Rate-limit and retry handling should stay conservative and transparent.

### Weibo official API adapter scaffold

Weibo is now an official-API-planned Chinese platform with a concrete adapter scaffold. It is intentionally mock-first and does not call the real Weibo API.

Current behavior:

- Default mode is `mock` through `WEIBO_ADAPTER_MODE=mock`.
- `get_adapter("weibo")` returns the Weibo adapter.
- `POST /api/v1/crawl/start` uses the adapter when `platforms` contains `weibo`.
- Mock mode returns deterministic Weibo-style microblog posts and visible public-comment mock data normalized as `RawPost` and `RawComment`.
- If `WEIBO_ADAPTER_MODE=real`, the adapter stays in mock mode and reports safe `api_pending` or `config_error` metadata. No network call is made.
- Safe status metadata includes `source_type="official_api_adapter_scaffold"`, `mock_available=true`, `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- No Weibo page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call is implemented.
- Latest QA revalidation confirmed the adapter interface, mock output schema fields, platform registry status, `/crawl/start` metadata, and safe real-mode blocking; full local backend validation passed with `201 passed in 3.03s`.

Future Weibo credentials after approval:

```text
WEIBO_ADAPTER_MODE=real
WEIBO_CLIENT_ID
WEIBO_CLIENT_SECRET
WEIBO_ACCESS_TOKEN
```

Remaining before real Weibo integration:

- official application/approval and permission-scope review
- rate-limit and usage policy documentation
- a reviewed official API client implementation
- mocked response fixtures that match approved API payloads
- compliance review before any live request

### Bilibili official API adapter scaffold

Bilibili is the first official-API-planned Chinese platform with a concrete adapter scaffold. It is intentionally mock-first and does not call the real Bilibili API.

Current behavior:

- Default mode is `mock` through `BILIBILI_ADAPTER_MODE=mock`.
- `get_adapter("bilibili")` returns the Bilibili adapter.
- `POST /api/v1/crawl/start` uses the adapter when `platforms` contains `bilibili`.
- Mock mode returns deterministic Bilibili-style video posts and visible public-comment mock data normalized as `RawPost` and `RawComment`.
- If `BILIBILI_ADAPTER_MODE=real`, the adapter stays in mock mode and reports safe `api_pending` or `config_error` metadata. No network call is made.
- Safe status metadata includes `source_type="official_api_adapter_scaffold"`, `mock_available=true`, `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- Latest QA status: focused Bilibili/adapter/crawl/registry/regression validation passed, direct local smoke returned schema-valid mock posts/comments, and full backend validation passed. No real Bilibili API call or Bilibili page scraping was made.

Future Bilibili credentials after approval:

```text
BILIBILI_ADAPTER_MODE=real
BILIBILI_CLIENT_ID
BILIBILI_CLIENT_SECRET
BILIBILI_ACCESS_TOKEN
```

Remaining before real Bilibili integration:

- official application/approval and permission-scope review
- rate-limit and usage policy documentation
- a reviewed official API client implementation
- mocked response fixtures that match approved API payloads
- compliance review before any live request

### Douyin official API adapter scaffold

Douyin is now an official-API-planned Chinese short-video platform with a concrete adapter scaffold. It is intentionally mock-first and does not call the real Douyin API.

Current behavior:

- Default mode is `mock` through `DOUYIN_ADAPTER_MODE=mock`.
- `get_adapter("douyin")` returns the Douyin adapter.
- `POST /api/v1/crawl/start` uses the adapter when `platforms` contains `douyin`.
- Mock mode returns deterministic Douyin-style short-video posts and visible public-comment mock data normalized as `RawPost` and `RawComment`.
- Developer access has been obtained by the user, but exact comment permissions are unknown.
- If `DOUYIN_ADAPTER_MODE=real`, the adapter stays in mock mode and reports safe `api_pending:permission_not_verified` when credentials are present or safe `config_error` metadata when credentials are missing. No network call is made.
- Safe status metadata includes `source_type="official_api_adapter_scaffold"`, `mock_available=true`, `real_mode_available=false`, `api_pending=true`, `real_mode_disabled=true`, `developer_access_status="obtained"`, `comment_api_status="unknown_or_permission_required"`, and `real_mode_blocker="permission_not_verified"`.
- No Douyin page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call is implemented.
- Latest QA status: focused Douyin/adapter/crawl/registry validation passed with `20 passed in 0.67s`; full local backend validation passed with `213 passed in 3.10s`. The pass confirmed the adapter interface, mock output schema fields, platform registry status, `/crawl/start` metadata, and safe real-mode blocking.

Future Douyin credentials after approval:

```text
DOUYIN_ADAPTER_MODE=real
DOUYIN_CLIENT_KEY
DOUYIN_CLIENT_SECRET
DOUYIN_ACCESS_TOKEN
```

Remaining before real Douyin integration:

- verify in the Douyin developer console that interaction/comment management or the current equivalent product is enabled
- verify `item.comment` or the current official equivalent comment scope
- verify whether keyword video comment management is available and applicable
- verify user authorization requirements and whether access is limited to authorized or owned items
- official application/approval and permission-scope review
- rate-limit and usage policy documentation
- a reviewed official API client implementation
- mocked response fixtures that match approved API payloads
- compliance review before any live request

### Kuaishou official API adapter scaffold

Kuaishou is now an official-API-planned Chinese short-video and livestream platform with a concrete adapter scaffold. It is intentionally mock-first and does not call the real Kuaishou API.

Current behavior:

- Default mode is `mock` through `KUAISHOU_ADAPTER_MODE=mock`.
- `get_adapter("kuaishou")` returns the Kuaishou adapter.
- `POST /api/v1/crawl/start` uses the adapter when `platforms` contains `kuaishou`.
- Mock mode returns deterministic Kuaishou-style short-video/livestream posts and visible public-comment mock data normalized as `RawPost` and `RawComment`.
- If `KUAISHOU_ADAPTER_MODE=real`, the adapter stays in mock mode and reports safe `api_pending` or `config_error` metadata. No network call is made.
- Safe status metadata includes `source_type="official_api_adapter_scaffold"`, `mock_available=true`, `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- No Kuaishou page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call is implemented.

Future Kuaishou credentials after approval:

```text
KUAISHOU_ADAPTER_MODE=real
KUAISHOU_CLIENT_ID
KUAISHOU_CLIENT_SECRET
KUAISHOU_ACCESS_TOKEN
```

Remaining before real Kuaishou integration:

- official application/approval and permission-scope review
- rate-limit and usage policy documentation
- a reviewed official API client implementation
- mocked response fixtures that match approved API payloads
- compliance review before any live request

### Xiaohongshu official API adapter scaffold

Xiaohongshu is now an official-API-planned Chinese lifestyle/community note platform with a concrete adapter scaffold. It is intentionally mock-first and does not call the real Xiaohongshu API.

Current behavior:

- Default mode is `mock` through `XIAOHONGSHU_ADAPTER_MODE=mock`.
- `get_adapter("xiaohongshu")` returns the Xiaohongshu adapter.
- `POST /api/v1/crawl/start` uses the adapter when `platforms` contains `xiaohongshu`.
- Mock mode returns deterministic Xiaohongshu-style note posts and visible public-comment mock data normalized as `RawPost` and `RawComment`.
- Developer access has been obtained by the user, but the exact note/comment API product and scope are unknown. Current public official materials may be commerce/Ark oriented.
- If `XIAOHONGSHU_ADAPTER_MODE=real`, the adapter stays in mock mode and reports safe `api_pending:permission_not_verified` when credentials are present or safe `config_error` metadata when credentials are missing. No network call is made.
- Safe status metadata includes `source_type="official_api_adapter_scaffold"`, `mock_available=true`, `real_mode_available=false`, `api_pending=true`, `real_mode_disabled=true`, `developer_access_status="obtained"`, `comment_api_status="unknown_or_not_confirmed"`, and `real_mode_blocker="permission_not_verified"`.
- No Xiaohongshu page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call is implemented.

Future Xiaohongshu credentials after approval:

```text
XIAOHONGSHU_ADAPTER_MODE=real
XIAOHONGSHU_CLIENT_ID
XIAOHONGSHU_CLIENT_SECRET
XIAOHONGSHU_ACCESS_TOKEN
```

Remaining before real Xiaohongshu integration:

- verify in the Xiaohongshu developer console whether note/content/comment/interaction data APIs exist for the approved product
- verify whether comments are available through official APIs
- verify whether access is limited to own account, merchant, Ark, ad, or approved creator content
- map app-key/app-secret terminology to the existing `XIAOHONGSHU_CLIENT_ID` / `XIAOHONGSHU_CLIENT_SECRET` placeholders if needed
- official application/approval and permission-scope review
- rate-limit and usage policy documentation
- a reviewed official API client implementation
- mocked response fixtures that match approved API payloads
- compliance review before any live request

### Zhihu official API adapter scaffold

Zhihu is now an official-API-planned Chinese Q&A/article platform with a concrete adapter scaffold. It is intentionally mock-first and does not call the real Zhihu API.

Current behavior:

- Default mode is `mock` through `ZHIHU_ADAPTER_MODE=mock`.
- `get_adapter("zhihu")` returns the Zhihu adapter.
- `POST /api/v1/crawl/start` uses the adapter when `platforms` contains `zhihu`.
- Mock mode returns deterministic Zhihu-style Q&A/article posts and visible public-comment mock data normalized as `RawPost` and `RawComment`.
- If `ZHIHU_ADAPTER_MODE=real`, the adapter stays in mock mode and reports safe `api_pending` or `config_error` metadata. No network call is made.
- Safe status metadata includes `source_type="official_api_adapter_scaffold"`, `mock_available=true`, `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- No Zhihu page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call is implemented.

Future Zhihu credentials after approval:

```text
ZHIHU_ADAPTER_MODE=real
ZHIHU_CLIENT_ID
ZHIHU_CLIENT_SECRET
ZHIHU_ACCESS_TOKEN
```

Remaining before real Zhihu integration:

- official application/approval and permission-scope review
- rate-limit and usage policy documentation
- a reviewed official API client implementation
- mocked response fixtures that match approved API payloads
- compliance review before any live request

### Douban official API adapter scaffold

Douban is now an official-API-planned Chinese review/group/topic discussion platform with a concrete adapter scaffold. It is intentionally mock-first and does not call the real Douban API.

Current behavior:

- Default mode is `mock` through `DOUBAN_ADAPTER_MODE=mock`.
- `get_adapter("douban")` returns the Douban adapter.
- `POST /api/v1/crawl/start` uses the adapter when `platforms` contains `douban`.
- Mock mode returns deterministic Douban-style review, group topic, and visible public-comment mock data normalized as `RawPost` and `RawComment`.
- If `DOUBAN_ADAPTER_MODE=real`, the adapter stays in mock mode and reports safe `api_pending` or `config_error` metadata. No network call is made.
- Safe status metadata includes `source_type="official_api_adapter_scaffold"`, `mock_available=true`, `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- No Douban page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call is implemented.

Future Douban credentials after approval:

```text
DOUBAN_ADAPTER_MODE=real
DOUBAN_CLIENT_ID
DOUBAN_CLIENT_SECRET
DOUBAN_ACCESS_TOKEN
```

Remaining before real Douban integration:

- official application/approval and permission-scope review
- rate-limit and usage policy documentation
- a reviewed official API client implementation
- mocked response fixtures that match approved API payloads
- compliance review before any live request

### Toutiao official API adapter scaffold

Toutiao is now an official-API-planned Chinese news and micro-headline platform with a concrete adapter scaffold. It is intentionally mock-first and does not call the real Toutiao API.

Current behavior:

- Default mode is `mock` through `TOUTIAO_ADAPTER_MODE=mock`.
- `get_adapter("toutiao")` returns the Toutiao adapter.
- `POST /api/v1/crawl/start` uses the adapter when `platforms` contains `toutiao`.
- Mock mode returns deterministic Toutiao-style article, micro-headline, and visible public-comment mock data normalized as `RawPost` and `RawComment`.
- If `TOUTIAO_ADAPTER_MODE=real`, the adapter stays in mock mode and reports safe `api_pending` or `config_error` metadata. No network call is made.
- Safe status metadata includes `source_type="official_api_adapter_scaffold"`, `mock_available=true`, `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`.
- No Toutiao page scraping, login, captcha handling, cookies, proxy rotation, private data access, or external LLM call is implemented.

Future Toutiao credentials after approval:

```text
TOUTIAO_ADAPTER_MODE=real
TOUTIAO_CLIENT_ID
TOUTIAO_CLIENT_SECRET
TOUTIAO_ACCESS_TOKEN
```

Remaining before real Toutiao integration:

- official application/approval and permission-scope review
- rate-limit and usage policy documentation
- a reviewed official API client implementation
- mocked response fixtures that match approved API payloads
- compliance review before any live request

## Compliant Public-Source Parser Framework

Some crawler-later platforms may eventually require public-page parsers for publicly available pages. The framework foundation is now scaffolded under `backend/app/services/crawling/public_parser/`, with The Paper / Pengpai News (`the_paper`), Jiemian News / 界面新闻 (`jiemian`), Hupu / HuPu (`hupu`), Maimai / 脉脉 (`maimai`), Baidu Tieba / 百度贴吧 (`tieba`), and NGA (`nga`) as fixture-only parser scaffolds.

Hupu / HuPu (`hupu`) is now included as a fixture-only forum-style public parser scaffold.
Maimai / 脉脉 (`maimai`) is now included as a fixture-only workplace and industry discussion public parser scaffold.
Baidu Tieba / 百度贴吧 (`tieba`) is now included as a fixture-only forum-style public parser scaffold.
NGA (`nga`) is now included as a fixture-only forum-style public parser scaffold.

Current status:

- Public parser framework: scaffolded.
- Fixture profiles: `the_paper`, `jiemian`, `hupu`, `maimai`, `tieba`, `nga`.
- Parser mode: `fixture_only`.
- Live public fetch: disabled by default through `PUBLIC_PARSER_LIVE_FETCH_ENABLED=false`.
- Unified status endpoint: `GET /api/v1/public-parsers/status` reports parser status, fixture/profile availability, comment support, safe limits, and effective live-fetch status for `the_paper`, `jiemian`, `hupu`, `maimai`, `tieba`, and `nga`.
- Fixture preview endpoint: `POST /api/v1/public-parsers/preview` parses deterministic fixture data and returns sample `RawPost` / `RawComment` items with schema validation flags and safe warnings.
- The Paper / Pengpai News has an optional local live public-page fetch pilot. It is used only when `PUBLIC_PARSER_LIVE_FETCH_ENABLED=true`; otherwise fixture/mock fallback remains the default.
- The Paper live pilot uses the public parser fetcher, robots/profile checks, low request rate, timeout, no cookies, no login, no captcha handling, no proxy rotation, and safe fixture fallback on unclear/blocked/network/selector failures.
- The Paper live pilot expects a public The Paper article id as the `keyword` so the profile can build a public article URL. It is not a general search crawler.
- The Paper live pilot QA is fixture/mocked-network based. Automated tests verify disabled default behavior, robots-blocked fallback before page fetch, network-error fallback, selector-error fallback, mocked valid HTML parsing, and safe headers without cookies or authorization.
- `/api/v1/crawl/start` may return fixture/mock public parser data for `the_paper`, `jiemian`, `hupu`, `maimai`, `tieba`, or `nga` when explicitly requested, with safe parser metadata.
- `/api/v1/public-parsers/preview` is intended for developer inspection and QA; it is fixture-first and safe for local offline demos.
- Fixture QA status: all six parser profiles load, fixture extraction validates against `RawPost`, missing selectors fail safely, and `/api/v1/crawl/start` returns safe parser metadata for each scaffolded platform.
- Status/preview QA status: all six parser profiles are visible through `GET /api/v1/public-parsers/status`; preview works for all six sources, unknown platforms fail safely, fixture-only platforms stay live-disabled, and preview does not use live fetch unless explicitly requested and globally enabled.
- Jiemian fixture extraction currently covers article title, content, source/author label, created time, and permalink. Comments are not parsed because the fixture does not expose public comments without login or dynamic loading: `comments_unavailable_without_login_or_dynamic_loading`.
- Hupu fixture extraction currently covers thread title, main post content, author/source, created time, permalink, light/upvote count, reply count, and visible fixture replies normalized as `RawComment`. Hupu live fetch remains disabled.
- Latest Hupu QA confirms `platforms=["hupu"]` returns fixture-only public parser metadata, one normalized thread `RawPost`, two visible fixture reply `RawComment` items, and valid schema flags without any live public fetch.
- Maimai fixture extraction currently covers post title, main post content, source/author, created time, permalink, interaction count, reply count, and visible fixture replies normalized as `RawComment`. Maimai live fetch remains disabled.
- Latest Maimai QA confirms `platforms=["maimai"]` returns fixture-only public parser metadata, one normalized workplace/industry discussion `RawPost`, two visible fixture reply `RawComment` items, and valid schema flags without any live public fetch. Maimai remains fixture-only even when the global The Paper live-pilot flag is enabled.
- Tieba fixture extraction currently covers thread title, main post content, author/source, created time, permalink, like/upvote count, reply count, and visible fixture replies normalized as `RawComment`; floor numbers are stored in `RawComment.raw_data.floor_number`. Tieba live fetch remains disabled.
- Latest Tieba QA confirms `platforms=["tieba"]` returns fixture-only public parser metadata, one normalized thread `RawPost`, three visible fixture reply `RawComment` items, floor numbers in `raw_data.floor_number`, and valid schema flags. Tieba remains fixture-only even when the global The Paper live-pilot flag is enabled.
- NGA fixture extraction currently covers thread title, main post content, author/source, created time, permalink, like/upvote count, reply count, and visible fixture replies normalized as `RawComment`; floor numbers are stored in `RawComment.raw_data.floor_number`. NGA live fetch remains disabled.
- Latest NGA QA confirms `platforms=["nga"]` returns fixture-only public parser metadata, one normalized thread `RawPost`, three visible fixture reply `RawComment` items, floor numbers in `raw_data.floor_number`, and valid schema flags. NGA remains fixture-only even when the global The Paper live-pilot flag is enabled.
- Frontend active MVP selectors should still keep crawler-later platforms disabled unless a later task explicitly promotes one.

Framework constraints:

- Parse only publicly available pages that do not require login, cookies, paywall access, captcha bypass, or anti-bot evasion.
- Use sanitized public HTML fixtures for selector development and tests.
- Keep selector profiles versioned, reviewed, and covered by deterministic tests.
- Do not use proxy rotation, private data collection, browser profiles, tokens, cookies, hidden APIs, or scraped private messages.
- Use LLM assistance only for analyzing sanitized public fixtures and suggesting selector updates, never for bypassing access controls or platform approval.
- Keep each platform behind an explicit compliance review before activation.

## crawler_later

These platforms are not selectable for real crawling in the MVP. They are visible as future candidates for public-page parsers and selector profiles, only for publicly available pages.

| platform_id | display_name | future source approach |
| --- | --- | --- |
| `hupu` | Hupu / HuPu | `fixture_only` public-page parser scaffold; `comments=fixture_public_only` |
| `tieba` | Baidu Tieba / 百度贴吧 | `fixture_only` public-page parser scaffold; `comments=fixture_public_only`; floor number stored in `RawComment.raw_data.floor_number` |
| `tianya` | Tianya | public-page parser later |
| `nga` | NGA | `fixture_only` public-page parser scaffold; `comments=fixture_public_only`; floor number stored in `RawComment.raw_data.floor_number` |
| `maimai` | Maimai / 脉脉 | `fixture_only` public-page parser scaffold; `comments=fixture_public_only`; workplace/industry discussion fixture |
| `the_paper` | The Paper / Pengpai News | `fixture_only` public-page parser scaffold |
| `jiemian` | Jiemian News / 界面新闻 | `fixture_only` public-page parser scaffold; `comments_unavailable_without_login_or_dynamic_loading` |

Crawler-later work should be handled in a future phase using public-page parsers and selector profiles. Each parser must normalize public posts/comments into the common Sentigraph schema and must include tests with sanitized fixture HTML.

## disabled_or_optional_future

| platform_id | display_name | status | notes |
| --- | --- | --- | --- |
| `youtube` | YouTube | optional future | Removed from active MVP platform choices. Keep only as an optional future source. |

## Future Crawler Maintenance Note

If a public webpage structure changes, Sentigraph may use an LLM to analyze sanitized public HTML fixtures and suggest selector updates. This maintenance workflow must never be used to bypass login, captcha, paywalls, anti-bot systems, rate limits, or private data access.

Selectors should be reviewed manually before use, versioned in the repository, and covered by tests against sanitized public-page fixtures.
