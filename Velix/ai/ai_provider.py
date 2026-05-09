"""
Interface Abstrata para Providers de IA
========================================

Define o contrato que todos os providers concretos implementam
e a factory function para instanciação.
"""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

from ai.ai_config import AIProviderConfig


@dataclass
class AIResponse:
    """Resultado normalizado de um pedido ao LLM."""

    content: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    model: str = ""
    latency_ms: int = 0
    finish_reason: str = ""        # "stop", "length", "error"
    error_message: str = ""

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def is_error(self) -> bool:
        return bool(self.error_message)


@dataclass
class Message:
    """Mensagem no formato role/content."""

    role: str    # "system" | "user" | "assistant"
    content: str


class AIProvider(ABC):
    """Contrato para cada provider de IA suportado."""

    def __init__(self, config: AIProviderConfig, api_key: str):
        self.config = config
        self.api_key = api_key

    @abstractmethod
    def complete(
        self,
        messages: List[Message],
        max_tokens: int = 2048,
        temperature: Optional[float] = None,
    ) -> AIResponse:
        """Envia mensagens ao LLM e retorna a resposta normalizada."""
        ...

    def test_connection(self) -> AIResponse:
        """Teste rápido de conectividade com mensagem trivial."""
        return self.complete(
            messages=[
                Message(role="system", content="Responde com OK."),
                Message(role="user", content="Teste"),
            ],
            max_tokens=8,
        )

    @staticmethod
    def count_tokens_estimate(text: str) -> int:
        """Estimativa grosseira: ~4 caracteres por token."""
        return max(1, len(text) // 4)

    def _build_headers(self) -> dict:
        """Headers base — cada provider pode sobrepor."""
        return {
            "Content-Type": "application/json",
        }

    def _timed_request(self, url: str, payload: bytes, headers: dict, timeout: int = 30) -> tuple:
        """
        Faz o pedido HTTP via urllib e devolve (status, body_bytes, latency_ms).
        """
        import urllib.request
        import urllib.error

        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                latency = int((time.perf_counter() - t0) * 1000)
                return resp.status, body, latency
        except urllib.error.HTTPError as exc:
            body = exc.read() if exc.fp else b""
            latency = int((time.perf_counter() - t0) * 1000)
            return exc.code, body, latency
        except urllib.error.URLError as exc:
            latency = int((time.perf_counter() - t0) * 1000)
            return 0, str(exc.reason).encode(), latency


# ── Factory ──────────────────────────────────────────────────────

def create_provider(config: AIProviderConfig, api_key: str) -> AIProvider:
    """Cria o provider correto com base na configuração."""
    provider_name = config.provider.lower()

    if provider_name == "openai":
        from ai.providers.openai_provider import OpenAIProvider
        return OpenAIProvider(config, api_key)

    if provider_name == "anthropic":
        from ai.providers.anthropic_provider import AnthropicProvider
        return AnthropicProvider(config, api_key)

    if provider_name == "google":
        from ai.providers.google_provider import GoogleProvider
        return GoogleProvider(config, api_key)

    if provider_name == "deepseek":
        from ai.providers.deepseek_provider import DeepSeekProvider
        return DeepSeekProvider(config, api_key)

    if provider_name == "custom":
        # Custom usa o formato OpenAI-compatible
        from ai.providers.openai_provider import OpenAIProvider
        return OpenAIProvider(config, api_key)

    raise ValueError(f"Provider desconhecido: {provider_name}")
