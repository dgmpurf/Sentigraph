# LLM Usage Guardrails

Last updated: 2026-05-17

## Purpose

Sentigraph is mock-first today, but future real LLM providers will need usage, cost, and safety controls before any network call is allowed. The current guardrail scaffold records offline mock usage metadata and provides deterministic limit checks that future OpenAI, DeepSeek, and Qwen integrations can call before sending a request.

The scaffold does not call external LLM APIs and does not require API keys.

## Default Configuration

```env
LLM_USAGE_TRACKING_ENABLED=true
LLM_DAILY_CALL_LIMIT=100
LLM_DAILY_TOKEN_LIMIT=100000
LLM_MAX_INPUT_CHARS=20000
LLM_FAIL_CLOSED_ON_LIMIT=true
LLM_COST_GUARDRAIL_MODE=mock
```

These settings are documented in `.env.example`. The local `.env` file must remain uncommitted.

## Current Mock-Only Tracking

The guardrail module lives at:

```text
backend/app/services/llm/usage_guardrails.py
```

Current supported operations:

- `estimate_tokens_from_chars(chars)`
- `check_call_allowed(provider, operation, input_chars)`
- `record_mock_call(provider, operation, input_chars, output_chars)`
- `get_usage_summary()`
- `reset_usage_for_tests()`
- `GET /api/v1/llm/usage` exposes the same metadata-only summary for the local frontend.

`GET /api/v1/llm/status` also includes guardrail limits and tracking status for the read-only `LLM Safety` / `大模型安全状态` page.

`MockProvider` records safe metadata for:

- keyword expansion
- sentiment mock LLM analysis
- topic extraction and cluster summaries
- report and recommendation mock drafts
- selector repair suggestions

## What Is Recorded

Usage records store only safe metadata:

- provider label
- operation label
- input character count
- output character count
- estimated input token count
- estimated output token count
- timestamp
- success flag
- failure category when applicable

Provider and operation labels are sanitized to simple labels before storage.

## What Is Never Recorded

The guardrail scaffold must not store:

- full prompts
- raw user text
- raw comments
- raw HTML
- model responses
- API keys
- access tokens
- cookies
- request headers
- credentials

Current tests assert raw prompt-like text does not appear in usage summaries.

## Future Real-Provider Use

Before a future real provider sends a request, it should call:

```text
check_call_allowed(provider, operation, input_chars)
```

If the decision is blocked and `LLM_FAIL_CLOSED_ON_LIMIT=true`, the provider must not make the external call. Current real provider placeholders remain disabled and return `provider_not_enabled` / `not_configured` behavior without network calls. When a placeholder real provider is explicitly selected with real calls enabled and credentials present, it checks guardrails before returning the current no-call placeholder error, so future HTTP clients can inherit the same fail-closed pattern.

## Future Cost Tracking

This scaffold estimates tokens from characters using a deterministic approximation. Before real calls are enabled, Sentigraph should add:

- provider-specific token accounting
- provider-specific pricing tables
- per-operation budgets
- per-user or per-project budgets after authentication exists
- request throttling
- alerting on quota exhaustion
- durable usage storage if needed

## Checklist Before Enabling Real LLM Calls

- Keep `LLM_ENABLE_REAL_CALLS=false` until implementation review is complete.
- Add mocked HTTP tests for each provider.
- Add timeout, retry, and rate-limit behavior.
- Add strict request and response schemas.
- Add prompt evaluation datasets.
- Add privacy review for text sent to providers.
- Confirm usage summaries still expose no prompts, raw text, keys, cookies, or headers.
- Confirm fallback behavior returns to deterministic rule/template outputs.
