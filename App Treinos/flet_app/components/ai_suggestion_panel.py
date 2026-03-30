"""
Painel de Sugestões de IA
==========================

Componente reutilizável que pode ser adicionado a qualquer tela.
Exibe um banner colapsável com ações de IA contextuais
(otimizar plano, sugerir edição, explicar fase, etc.).
"""

import asyncio
import hashlib
import flet as ft
from flet_app.theme import c, SPACING, RADIUS, card_shadow
from flet_app.state import app_state
from ai.ai_assistant import AIAssistant
from ai.ai_provider import AIResponse


def _password_hash(cref: str) -> str:
    return hashlib.sha256(cref.encode()).hexdigest()


def build_ai_suggestion_panel(
    page: ft.Page,
    dark: bool,
    action_type: str = "optimize_plan",
    action_kwargs: dict = None,
) -> ft.Container:
    """
    Constrói um painel de sugestão IA colapsável.

    Parâmetros
    ----------
    page : ft.Page
    dark : bool
    action_type : str
        Uma das ações do AIAssistant: optimize_plan, suggest_edit,
        explain_phase, weekly_analysis, adjust_health, race_strategy.
    action_kwargs : dict
        Argumentos a passar ao método do assistant (ex.: sessions, athlete, etc.).
    """
    cref = app_state.trainer_cref or ""
    pw_hash = _password_hash(cref)
    assistant = AIAssistant(cref, pw_hash)

    if not assistant.config.is_configured or not assistant.config.enabled:
        return ft.Container()

    # ── Estado interno ───────────────────────────────────────────

    is_expanded = False
    result_text = ft.Markdown(
        "",
        selectable=True,
        extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
    )
    loading = ft.ProgressRing(visible=False, width=20, height=20, stroke_width=2)
    status_text = ft.Text("", size=12, color=c("text_secondary", dark))
    content_col = ft.Column(
        [result_text, status_text],
        spacing=SPACING["xs"],
        visible=False,
    )

    # ── Ações ────────────────────────────────────────────────────

    ACTION_LABELS = {
        "optimize_plan": ("Otimizar Plano", ft.Icons.AUTO_AWESOME),
        "suggest_edit": ("Sugerir Edição", ft.Icons.EDIT_NOTE),
        "explain_phase": ("Explicar Fase", ft.Icons.SCHOOL),
        "weekly_analysis": ("Analisar Semana", ft.Icons.ANALYTICS),
        "adjust_health": ("Ajustar Saúde", ft.Icons.HEALTH_AND_SAFETY),
        "race_strategy": ("Estratégia de Prova", ft.Icons.EMOJI_EVENTS),
    }

    label, icon = ACTION_LABELS.get(action_type, ("IA", ft.Icons.SMART_TOY))

    def _toggle_expand(_):
        nonlocal is_expanded
        is_expanded = not is_expanded
        content_col.visible = is_expanded
        toggle_btn.icon = ft.Icons.EXPAND_LESS if is_expanded else ft.Icons.EXPAND_MORE
        page.update()

    def _run_ai(_):
        if assistant.is_over_limit:
            status_text.value = "Limite mensal de tokens atingido."
            status_text.color = c("error", dark)
            page.update()
            return

        loading.visible = True
        status_text.value = "Consultando IA..."
        status_text.color = c("text_secondary", dark)
        result_text.value = ""
        content_col.visible = True
        page.update()

        kwargs = action_kwargs or {}
        method = getattr(assistant, action_type, None)
        if method is None:
            status_text.value = f"Ação '{action_type}' não encontrada."
            status_text.color = c("error", dark)
            loading.visible = False
            page.update()
            return

        try:
            response: AIResponse = method(**kwargs)
        except Exception as exc:
            response = AIResponse(
                error_message=f"Erro inesperado: {exc}",
                finish_reason="error",
            )

        loading.visible = False
        if response.is_error:
            status_text.value = f"Erro: {response.error_message}"
            status_text.color = c("error", dark)
            result_text.value = ""
        else:
            result_text.value = response.content
            usage = assistant.get_usage_summary()
            status_text.value = (
                f"Tokens: {response.total_tokens:,} | "
                f"Latência: {response.latency_ms}ms | "
                f"Mês: {usage['usage_pct']:.1f}%"
            )
            status_text.color = (
                c("warning", dark) if usage["near_limit"] else c("text_secondary", dark)
            )
        page.update()

    # ── Construção ───────────────────────────────────────────────

    toggle_btn = ft.IconButton(
        icon=ft.Icons.EXPAND_MORE,
        icon_size=20,
        on_click=_toggle_expand,
        tooltip="Expandir/Recolher",
    )

    header = ft.Row(
        [
            ft.Icon(ft.Icons.SMART_TOY, size=18, color=c("primary", dark)),
            ft.Text("Assistente IA", size=14, weight=ft.FontWeight.W_600),
            ft.Container(expand=True),
            loading,
            ft.FilledTonalButton(
                label,
                icon=icon,
                on_click=_run_ai,
            ),
            toggle_btn,
        ],
        spacing=SPACING["xs"],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Warning banner for near-limit
    warning_banner = ft.Container(visible=False)
    if assistant.is_near_limit:
        summary = assistant.get_usage_summary()
        warning_banner = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.WARNING_AMBER, size=16, color=c("warning", dark)),
                    ft.Text(
                        f"Atenção: {summary['usage_pct']:.0f}% do limite mensal utilizado.",
                        size=12,
                        color=c("warning", dark),
                    ),
                ],
                spacing=SPACING["xs"],
            ),
            visible=True,
        )

    panel = ft.Container(
        content=ft.Column(
            [header, warning_banner, content_col],
            spacing=SPACING["xs"],
        ),
        bgcolor=c("bg_card", dark),
        border_radius=RADIUS["md"],
        padding=ft.padding.symmetric(horizontal=SPACING["md"], vertical=SPACING["sm"]),
        shadow=card_shadow(dark, "sm"),
        border=ft.border.all(1, c("border_light", dark)),
    )

    return panel
