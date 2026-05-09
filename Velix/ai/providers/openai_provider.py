"""
Provider OpenAI (e OpenAI-compatíveis)
========================================

Suporta qualquer endpoint compatível com a API Chat Completions:
OpenAI, Azure OpenAI, Groq, Ollama, LM Studio, etc.
"""

import json
from typing import List, Optional

from ai.ai_provider import AIProvider, AIResponse, Message
from ai.ai_config import AIProviderConfig


class OpenAIProvider(AIProvider):
    """Provider para OpenAI Chat Completions API."""

    def _build_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def complete(
        self,
        messages: List[Message],
        max_tokens: int = 2048,
        temperature: Optional[float] = None,
    ) -> AIResponse:
        url = f"{self.config.get_effective_base_url()}/chat/completions"
        temp = temperature if temperature is not None else self.config.temperature

        payload = json.dumps({
            "model": self.config.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "max_tokens": max_tokens,
            "temperature": temp,
        }).encode("utf-8")

        headers = self._build_headers()
        status, body, latency = self._timed_request(url, payload, headers)

        if status != 200:
            return AIResponse(
                error_message=self._parse_error(body, status),
                latency_ms=latency,
                model=self.config.model,
                finish_reason="error",
            )

        try:
            data = json.loads(body)
            choice = data["choices"][0]
            usage = data.get("usage", {})
            return AIResponse(
                content=choice["message"]["content"].strip(),
                input_tokens=usage.get("prompt_tokens", 0),
                output_tokens=usage.get("completion_tokens", 0),
                model=data.get("model", self.config.model),
                latency_ms=latency,
                finish_reason=choice.get("finish_reason", "stop"),
            )
        except (KeyError, IndexError, json.JSONDecodeError) as exc:
            return AIResponse(
                error_message=f"Resposta inesperada da API: {exc}",
                latency_ms=latency,
                model=self.config.model,
                finish_reason="error",
            )

    @staticmethod
    def _parse_error(body: bytes, status: int) -> str:
        try:
            data = json.loads(body)
            msg = data.get("error", {}).get("message", "")
            if msg:
                return f"[{status}] {msg}"
        except (json.JSONDecodeError, AttributeError):
            pass
        return f"[{status}] {body[:200].decode(errors='replace')}"
