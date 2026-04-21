"""
Provider Anthropic (Claude)
============================

Usa a Messages API v1 com header x-api-key.
"""

import json
from typing import List, Optional

from ai.ai_provider import AIProvider, AIResponse, Message
from ai.ai_config import AIProviderConfig


class AnthropicProvider(AIProvider):
    """Provider para Anthropic Messages API."""

    ANTHROPIC_VERSION = "2023-06-01"

    def _build_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": self.ANTHROPIC_VERSION,
        }

    def complete(
        self,
        messages: List[Message],
        max_tokens: int = 2048,
        temperature: Optional[float] = None,
    ) -> AIResponse:
        url = f"{self.config.get_effective_base_url()}/messages"
        temp = temperature if temperature is not None else self.config.temperature

        # Anthropic separa system prompt dos messages
        system_text = ""
        api_messages = []
        for m in messages:
            if m.role == "system":
                system_text += m.content + "\n"
            else:
                api_messages.append({"role": m.role, "content": m.content})

        body_dict = {
            "model": self.config.model,
            "messages": api_messages,
            "max_tokens": max_tokens,
            "temperature": temp,
        }
        if system_text.strip():
            body_dict["system"] = system_text.strip()

        payload = json.dumps(body_dict).encode("utf-8")
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
            content_blocks = data.get("content", [])
            text = "".join(
                blk.get("text", "") for blk in content_blocks if blk.get("type") == "text"
            )
            usage = data.get("usage", {})
            return AIResponse(
                content=text.strip(),
                input_tokens=usage.get("input_tokens", 0),
                output_tokens=usage.get("output_tokens", 0),
                model=data.get("model", self.config.model),
                latency_ms=latency,
                finish_reason=data.get("stop_reason", "end_turn"),
            )
        except (KeyError, json.JSONDecodeError) as exc:
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
