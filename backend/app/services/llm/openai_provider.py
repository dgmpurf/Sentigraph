from __future__ import annotations

from app.services.llm.placeholder_provider import PlaceholderLLMProvider


class OpenAIProvider(PlaceholderLLMProvider):
    provider_id = "openai"
    display_name = "OpenAI Provider"
    required_credentials = ("OPENAI_API_KEY",)
