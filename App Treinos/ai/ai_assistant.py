"""
Fachada do Assistente de IA
============================

Ponto de entrada único para todas as funcionalidades de IA.
Orquestra configuração, provider, tokens e prompts.
"""

import asyncio
import logging
from typing import Dict, List, Optional

from ai.ai_config import AIProviderConfig, load_ai_config, save_ai_config
from ai.ai_provider import AIResponse, Message, create_provider
from ai.token_tracker import TokenTracker
from ai import prompt_templates

log = logging.getLogger(__name__)


class AIAssistant:
    """Fachada que simplifica o uso da IA no restante da aplicação."""

    def __init__(self, cref: str, password_hash: str = ""):
        self.cref = cref
        self.password_hash = password_hash
        self._config: Optional[AIProviderConfig] = None
        self._tracker: Optional[TokenTracker] = None

    # ── Lazy-loading ─────────────────────────────────────────────

    @property
    def config(self) -> AIProviderConfig:
        if self._config is None:
            self._config = load_ai_config(self.cref)
        return self._config

    def reload_config(self):
        """Força recarga da configuração."""
        self._config = None

    @property
    def tracker(self) -> TokenTracker:
        if self._tracker is None:
            self._tracker = TokenTracker(self.cref)
        return self._tracker

    # ── Estado ───────────────────────────────────────────────────

    @property
    def is_available(self) -> bool:
        """IA está configurada, ativa e dentro do limite."""
        return (
            self.config.is_configured
            and self.config.enabled
            and not self.tracker.is_over_limit(self.config.max_monthly_tokens)
        )

    @property
    def is_near_limit(self) -> bool:
        return self.tracker.is_near_limit(self.config.max_monthly_tokens)

    @property
    def is_over_limit(self) -> bool:
        return self.tracker.is_over_limit(self.config.max_monthly_tokens)

    def get_usage_summary(self) -> Dict:
        return self.tracker.get_summary(self.config.max_monthly_tokens)

    # ── Chamada genérica ─────────────────────────────────────────

    def _call(
        self,
        system_prompt: str,
        user_prompt: str,
        action: str,
        max_tokens: int = 2048,
    ) -> AIResponse:
        """Executa uma chamada síncrona ao provider."""
        if not self.is_available:
            if self.is_over_limit:
                return AIResponse(
                    error_message="Limite mensal de tokens atingido. "
                    "Ajuste o limite nas configurações de IA ou aguarde o próximo mês.",
                    finish_reason="error",
                )
            return AIResponse(
                error_message="IA não está configurada ou ativada.",
                finish_reason="error",
            )

        api_key = self.config.get_api_key(self.password_hash)
        if not api_key:
            return AIResponse(
                error_message="Não foi possível decifrar a API key.",
                finish_reason="error",
            )

        provider = create_provider(self.config, api_key)
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content=user_prompt),
        ]

        try:
            response = provider.complete(messages, max_tokens=max_tokens)
        except Exception as exc:
            log.exception("Erro ao chamar provider %s", self.config.provider)
            return AIResponse(
                error_message=f"Erro inesperado: {exc}",
                finish_reason="error",
            )

        # Registar tokens (mesmo em erro parcial)
        if response.input_tokens or response.output_tokens:
            self.tracker.record(
                model=response.model or self.config.model,
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                action=action,
            )

        return response

    async def _call_async(
        self,
        system_prompt: str,
        user_prompt: str,
        action: str,
        max_tokens: int = 2048,
    ) -> AIResponse:
        """Wrapper assíncrono (não bloqueia a UI Flet)."""
        return await asyncio.to_thread(
            self._call, system_prompt, user_prompt, action, max_tokens
        )

    # ── Ações especializadas ─────────────────────────────────────

    def optimize_plan(
        self,
        sessions: List[Dict],
        athlete: Dict,
        goal: str = "",
    ) -> AIResponse:
        system, user = prompt_templates.optimize_plan(sessions, athlete, goal)
        return self._call(system, user, action="optimize_plan", max_tokens=3000)

    async def optimize_plan_async(
        self,
        sessions: List[Dict],
        athlete: Dict,
        goal: str = "",
    ) -> AIResponse:
        system, user = prompt_templates.optimize_plan(sessions, athlete, goal)
        return await self._call_async(system, user, action="optimize_plan", max_tokens=3000)

    def suggest_edit(self, session: Dict, context: str = "") -> AIResponse:
        system, user = prompt_templates.suggest_workout_edit(session, context)
        return self._call(system, user, action="suggest_edit", max_tokens=2048)

    async def suggest_edit_async(self, session: Dict, context: str = "") -> AIResponse:
        system, user = prompt_templates.suggest_workout_edit(session, context)
        return await self._call_async(system, user, action="suggest_edit", max_tokens=2048)

    def explain_phase(
        self, phase: str, sport: str = "", weeks: int = 0
    ) -> AIResponse:
        system, user = prompt_templates.explain_periodization(phase, sport, weeks)
        return self._call(system, user, action="explain_phase", max_tokens=2048)

    async def explain_phase_async(
        self, phase: str, sport: str = "", weeks: int = 0
    ) -> AIResponse:
        system, user = prompt_templates.explain_periodization(phase, sport, weeks)
        return await self._call_async(system, user, action="explain_phase", max_tokens=2048)

    def adjust_health(
        self, sessions: List[Dict], condition: str, athlete: Dict
    ) -> AIResponse:
        system, user = prompt_templates.adjust_for_health(sessions, condition, athlete)
        return self._call(system, user, action="adjust_health", max_tokens=2048)

    async def adjust_health_async(
        self, sessions: List[Dict], condition: str, athlete: Dict
    ) -> AIResponse:
        system, user = prompt_templates.adjust_for_health(sessions, condition, athlete)
        return await self._call_async(system, user, action="adjust_health", max_tokens=2048)

    def weekly_analysis(
        self,
        sessions: List[Dict],
        week_number: int,
        phase: str,
        week_type: str,
    ) -> AIResponse:
        system, user = prompt_templates.weekly_analysis(sessions, week_number, phase, week_type)
        return self._call(system, user, action="weekly_analysis", max_tokens=2048)

    async def weekly_analysis_async(
        self,
        sessions: List[Dict],
        week_number: int,
        phase: str,
        week_type: str,
    ) -> AIResponse:
        system, user = prompt_templates.weekly_analysis(sessions, week_number, phase, week_type)
        return await self._call_async(system, user, action="weekly_analysis", max_tokens=2048)

    def race_strategy(
        self,
        race_info: Dict,
        athlete: Dict,
        recent_sessions: List[Dict],
    ) -> AIResponse:
        system, user = prompt_templates.race_strategy(race_info, athlete, recent_sessions)
        return self._call(system, user, action="race_strategy", max_tokens=3000)

    async def race_strategy_async(
        self,
        race_info: Dict,
        athlete: Dict,
        recent_sessions: List[Dict],
    ) -> AIResponse:
        system, user = prompt_templates.race_strategy(race_info, athlete, recent_sessions)
        return await self._call_async(system, user, action="race_strategy", max_tokens=3000)

    # ── Teste de ligação ─────────────────────────────────────────

    def test_connection(self) -> AIResponse:
        """Testa a ligação ao provider configurado."""
        api_key = self.config.get_api_key(self.password_hash)
        if not api_key:
            return AIResponse(
                error_message="API key não configurada ou não foi possível decifrar.",
                finish_reason="error",
            )
        provider = create_provider(self.config, api_key)
        return provider.test_connection()

    async def test_connection_async(self) -> AIResponse:
        return await asyncio.to_thread(self.test_connection)
