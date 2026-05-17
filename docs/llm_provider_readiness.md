# LLM Provider Readiness

Last updated: 2026-05-17

## Current Status

Sentigraph is still mock-first and offline for LLM-assisted features.

Default configuration:

```env
LLM_PROVIDER=mock
LLM_ENABLE_REAL_CALLS=false
OPENAI_API_KEY=
DEEPSEEK_API_KEY=
QWEN_API_KEY=
```

`MockProvider` is the active default. It returns deterministic local outputs for keyword expansion, sentiment assistance, topic summaries, report/recommendation drafts, and selector repair suggestions. It does not require API keys and does not call external services.

## Provider Architecture

The provider layer lives under:

```text
backend/app/services/llm/
```

Current pieces:

- `BaseLLMProvider`: common interface for future providers.
- `MockProvider`: deterministic offline provider used by the MVP.
- `OpenAIProvider`, `DeepSeekProvider`, `QwenProvider`: placeholders for future real integrations.
- `provider_factory.get_llm_provider()`: selects the configured provider.
- `provider_factory.get_llm_provider_diagnostics()`: returns safe readiness status only.
- `json_guard`: deterministic JSON parsing fallback helpers.
- `redaction`: present/missing-only secret redaction helpers.

## Safety Gates

Real providers remain disabled unless all future gates are intentionally opened:

1. `LLM_PROVIDER` selects a real provider such as `openai`, `deepseek`, or `qwen`.
2. `LLM_ENABLE_REAL_CALLS=true`.
3. The needed API key is configured in the local environment.
4. The provider has an implemented, reviewed HTTP client.
5. Tests cover mocked HTTP behavior, timeouts, retries, output validation, secret redaction, and fallback behavior.

Today, even when a real provider is selected and an API key is present, the placeholder still returns `provider_not_enabled` because no real HTTP integration is implemented.

## Secret Handling

API keys must stay in local environment variables or a local `.env` file that is ignored by git. Never commit keys to the repository.

Safe diagnostics may show:

- `provider_name`
- `real_calls_enabled`
- `api_key_present`
- `provider_status`
- credential presence booleans

Safe diagnostics must never show full or partial API key values. `redact_api_key()` returns only `present` or `missing`, and `redact_config_dict()` redacts secret-like keys recursively.

## Current LLM-Connected Modules

- Keyword expansion routes through the provider factory but only uses `MockProvider` in the current MVP.
- Sentiment analysis defaults to `rule_based`; optional `mock_llm` uses `MockProvider` and falls back to rule-based output.
- Topic cluster summaries default to `template`; optional `mock_llm` uses `MockProvider` and falls back to template output.
- Report generation remains deterministic and template-based in product flows. `MockProvider.generate_report()` exists for future wiring but is not active in the default report builder.
- Selector repair uses sanitized public fixture HTML and deterministic `MockProvider` suggestions only.

## Checklist Before Real Calls

Before enabling any real OpenAI, DeepSeek, or Qwen call:

- Add the provider HTTP client behind `LLM_ENABLE_REAL_CALLS=true`.
- Add request timeouts, retry limits, rate limits, and cost tracking.
- Add strict request and response schemas.
- Add mocked HTTP tests for success, provider errors, malformed responses, timeouts, and rate limits.
- Add prompt evaluation fixtures for keyword expansion, sentiment, topic summaries, report drafts, and selector repair.
- Verify all logs and diagnostics remain present/missing only for secrets.
- Define fallback behavior to current deterministic rule/template outputs.
- Review privacy and data handling for any text sent to providers.

## Known Limitations

- Real OpenAI, DeepSeek, and Qwen integrations are not implemented.
- No provider pricing, token accounting, or rate-limit enforcement is implemented yet.
- No prompt evaluation dataset is in place yet.
- Selector repair suggestions are deterministic mock heuristics and must remain human-reviewed before any profile edit.
