from __future__ import annotations

from app.services.llm.placeholder_provider import PlaceholderLLMProvider


class QwenProvider(PlaceholderLLMProvider):
    provider_id = "qwen"
    display_name = "Qwen Provider"
    required_credentials = ("QWEN_API_KEY",)
