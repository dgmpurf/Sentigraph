# Sentigraph Platform Sources

Sentigraph now prioritizes Chinese public opinion platforms for future source integration while keeping Reddit visible in the project as a future real adapter candidate.

The current MVP remains mock-first. No real crawler, real third-party API call, API key, login bypass, captcha bypass, anti-bot evasion, paywall bypass, or private data collection is implemented in this phase.

## MVP mock-selectable platforms

MVP selections are limited to platforms that can run with local mock data. Selecting these platforms only changes the offline mock workflow; it does not call real third-party APIs or real crawlers.

| platform_id | display_name | category | source_type | selectable_for_mock |
| --- | --- | --- | --- | --- |
| `reddit` | Reddit | `future_real_adapter_candidate` | `mock_data_future_adapter_placeholder` | true |
| `weibo` | Weibo | `official_api_planned` | `mock_data_official_api_placeholder` | true |
| `bilibili` | Bilibili | `official_api_planned` | `mock_data_official_api_placeholder` | true |
| `douyin` | Douyin | `official_api_planned` | `mock_data_official_api_placeholder` | true |
| `kuaishou` | Kuaishou | `official_api_planned` | `mock_data_official_api_placeholder` | true |
| `xiaohongshu` | Xiaohongshu | `official_api_planned` | `mock_data_official_api_placeholder` | true |
| `zhihu` | Zhihu | `official_api_planned` | `mock_data_official_api_placeholder` | true |
| `douban` | Douban | `official_api_planned` | `mock_data_official_api_placeholder` | true |
| `toutiao` | Toutiao | `official_api_planned` | `mock_data_official_api_placeholder` | true |

## official_api_planned

These platforms should be integrated through official API programs when credentials, permissions, usage limits, and compliance requirements are available. They may be selectable for mock analysis in the MVP, but they must not trigger real API calls yet.

| platform_id | display_name | official_platform_url | MVP status |
| --- | --- | --- | --- |
| `weibo` | Weibo | https://open.weibo.com | mock-selectable placeholder |
| `bilibili` | Bilibili | https://openhome.bilibili.com | mock-selectable placeholder |
| `douyin` | Douyin | https://developer.open-douyin.com | mock-selectable placeholder |
| `kuaishou` | Kuaishou | https://open.kuaishou.com | mock-selectable placeholder |
| `xiaohongshu` | Xiaohongshu | https://open.xiaohongshu.com | mock-selectable placeholder |
| `zhihu` | Zhihu | https://open.zhihu.com | mock-selectable placeholder |
| `douban` | Douban | https://developers.douban.com | mock-selectable placeholder |
| `toutiao` | Toutiao | https://open.toutiao.com | mock-selectable placeholder |

## future_real_adapter_candidate

| platform_id | display_name | MVP status | notes |
| --- | --- | --- | --- |
| `reddit` | Reddit | mock-selectable placeholder | Reddit stays visible and selectable for mock analysis. A real adapter may be planned later after compliance and API design review. |

## crawler_later

These platforms are not selectable for real crawling in the MVP. They are visible as future candidates for public-page parsers and selector profiles, only for publicly available pages.

| platform_id | display_name | future source approach |
| --- | --- | --- |
| `hupu` | Hupu | public-page parser later |
| `baidu_tieba` | Baidu Tieba | public-page parser later |
| `tianya` | Tianya | public-page parser later |
| `nga` | NGA | public-page parser later |
| `maimai` | Maimai | public-page parser later |
| `the_paper` | The Paper / Pengpai News | public-page parser later |
| `jiemian` | Jiemian News | public-page parser later |

Crawler-later work should be handled in a future phase using public-page parsers and selector profiles. Each parser must normalize public posts/comments into the common Sentigraph schema and must include tests with sanitized fixture HTML.

## disabled_or_optional_future

| platform_id | display_name | status | notes |
| --- | --- | --- | --- |
| `youtube` | YouTube | optional future | Removed from active MVP platform choices. Keep only as an optional future source. |

## Future Crawler Maintenance Note

If a public webpage structure changes, Sentigraph may use an LLM to analyze sanitized public HTML fixtures and suggest selector updates. This maintenance workflow must never be used to bypass login, captcha, paywalls, anti-bot systems, rate limits, or private data access.

Selectors should be reviewed manually before use, versioned in the repository, and covered by tests against sanitized public-page fixtures.
