# Selector Repair Design

Last updated: 2026-05-17

## Purpose

Selector repair is a mock-first maintenance scaffold for Sentigraph public-page parser profiles. It helps developers inspect what might need to change when a fixture parser stops matching title, content, author, date, or comment selectors.

The current implementation only works from caller-provided public fixture HTML. It does not fetch live pages, does not call real platform APIs, and does not call real LLM APIs.

## Safety Policy

- Use sanitized public HTML fixtures only.
- Do not include private pages, authenticated pages, cookies, authorization headers, access tokens, API keys, or user account data.
- Do not bypass login, captcha, paywalls, rate limits, robots policy, or anti-bot controls.
- Do not use browser cookies or proxy rotation.
- Do not scrape Reddit or official API scaffold platforms.
- Do not automatically apply suggested selectors to active parser profiles.

## Sanitization

`html_sanitizer.sanitize_html()` removes:

- `<script>` tags
- `<style>` tags
- inline event handlers such as `onclick`
- obvious token/cookie/authorization/client-secret/password pairs
- bearer-style authorization values
- obvious token/cookie/CSRF metadata

The sanitized HTML is capped by `SELECTOR_REPAIR_MAX_HTML_CHARS`, defaulting to `20000`, so repair requests stay bounded.

## Workflow

1. A parser fixture or manual QA run detects selector drift.
2. A developer submits public fixture HTML, the current selector profile, extraction targets, and an error summary.
3. The backend builds a `SelectorRepairRequest` using sanitized HTML only.
4. `MockProvider.suggest_selector_repair()` returns deterministic `SelectorRepairSuggestion` candidates.
5. A developer previews candidates against fixture HTML.
6. The preview returns matched targets, sample values, warnings, and `profile_modified=false`.
7. A human reviews the suggestion before any later profile edit.

## API

Current endpoints:

- `POST /api/v1/public-parsers/selector-repair/suggest`
- `POST /api/v1/public-parsers/selector-repair/preview`

Both endpoints are fixture-only and deterministic. They never fetch live pages and never modify active profile files.

Invalid platforms, missing selector profiles, malformed suggestions, and unmatched preview selectors fail safely with structured errors or preview warnings. These failures do not write to parser profile files.

## Configuration

```env
SELECTOR_REPAIR_MODE=mock
SELECTOR_REPAIR_ENABLE_REAL_LLM=false
SELECTOR_REPAIR_MAX_HTML_CHARS=20000
```

`future_real_llm` mode is intentionally disabled and returns safe provider-disabled behavior. Real LLM selector repair requires a future task with explicit approval, prompt/schema review, mocked HTTP coverage, key redaction tests, timeout/rate-limit handling, and human review gates.

## Current Limitations

- Mock suggestions are deterministic heuristics, not intelligent selector discovery.
- The preview validates whether candidates match fixture HTML, but it cannot prove selectors are stable on real pages.
- Active parser profiles are never edited automatically.
- Draft saving currently returns an in-memory draft marker; durable draft storage and review UI remain future work.
