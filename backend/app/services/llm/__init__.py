"""Mock-first LLM provider scaffold for Sentigraph.

The default provider is deterministic and offline. Placeholder real providers
intentionally do not call external APIs until future explicit integration work.
"""

from app.services.llm.mock_provider import MockProvider
from app.services.llm.provider_factory import get_llm_provider, get_llm_provider_diagnostics
from app.services.llm.redaction import redact_api_key, redact_config_dict

__all__ = [
    "MockProvider",
    "get_llm_provider",
    "get_llm_provider_diagnostics",
    "redact_api_key",
    "redact_config_dict",
]
