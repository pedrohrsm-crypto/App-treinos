"""
Provider Google Gemini
=======================

Usa a REST API generateContent do Gemini, autenticada
via query-parameter ?key=... (padrão da AI Studio key).
"""

import json
from typing import List, Optional

from ai.ai_provider import AIProvider, AIResponse, Message
from ai.ai_config import AIProviderConfig


class GoogleProvider(AIProvider):
    """Provider para Google Gemini (generativelanguage API)."""

    def complete(
        self,
        messages: List[Message],
        max_tokens: int = 2048,
        temperature: Optional[float] = None,
    ) -> AIResponse:
        base = self.config.get_effective_base_url()
        model = self.config.model
        url = f"{base}/models/{model}:generateContent?key={self.api_key}"
        temp = temperature if temperature is not None else self.config.temperature

        # Converter mensagens para formato Gemini
        system_text = ""
        contents = []
        for m in messages:
            if m.role == "system":
                system_text += m.content + "\n"
            else:
                role = "model" if m.role == "assistant" else "user"
                contents.append({
                    "role": role,
                    "parts": [{"text": m.content}],
                })

        # Prepend system como primeira mensagem user se existir
        if system_text.strip() and contents:
            first = contents[0]
            if first["role"] == "user":
                first["parts"].insert(
                    0, {"text": f"[Instruções do Sistema]\n{system_text.strip()}\n\n"}
                )

        body_dict = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temp,
            },
        }

        payload = json.dumps(body_dict).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        status, body, latency = self._timed_request(url, payload, headers)

        if status != 200:
            return AIResponse(
                error_message=self._parse_error(body, status),
                latency_ms=latency,
                model=model,
                finish_reason="error",
            )

        try:
            data = json.loads(body)
            candidate = data["candidates"][0]
            parts = candidate.get("content", {}).get("parts", [])
            text = "".join(p.get("text", "") for p in parts)
            usage = data.get("usageMetadata", {})
            return AIResponse(
                content=text.strip(),
                input_tokens=usage.get("promptTokenCount", 0),
                output_tokens=usage.get("candidatesTokenCount", 0),
                model=model,
                latency_ms=latency,
                finish_reason=candidate.get("finishReason", "STOP").lower(),
            )
        except (KeyError, IndexError, json.JSONDecodeError) as exc:
            return AIResponse(
                error_message=f"Resposta inesperada da API: {exc}",
                latency_ms=latency,
                model=model,
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
