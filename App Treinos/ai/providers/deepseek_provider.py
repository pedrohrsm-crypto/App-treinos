"""
Provider DeepSeek
==================

A API DeepSeek é OpenAI-compatível, pelo que reutilizamos
o OpenAIProvider com URL e modelo diferentes.
"""

from ai.providers.openai_provider import OpenAIProvider


class DeepSeekProvider(OpenAIProvider):
    """Provider DeepSeek — herda de OpenAIProvider (API compatível)."""
    pass
