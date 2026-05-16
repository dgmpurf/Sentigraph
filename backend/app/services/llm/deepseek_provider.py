from __future__ import annotations

from app.services.llm.placeholder_provider import PlaceholderLLMProvider


class DeepSeekProvider(PlaceholderLLMProvider):
    provider_id = "deepseek"
    display_name = "DeepSeek Provider"
    required_credentials = ("DEEPSEEK_API_KEY",)
