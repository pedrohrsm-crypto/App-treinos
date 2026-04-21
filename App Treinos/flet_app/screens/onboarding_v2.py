"""
Onboarding Expandido v3 — 6 slides com LGPD obrigatória
==========================================================

Novo fluxo:
1. Bem-vindo (valor prop)
2. Organize seus atletas (feature)
3. Gere treinos com IA (feature)
4. Acompanhe o progresso (feature)
5. Conformidade LGPD (legal - MANDATORY)
6. Vamos começar! (CTA)

Nota: Slide 5 tem checkbox obrigatório do LGPD que bloqueia progresso para slide 6.
Confirmação persiste em preferences.json.
"""

import flet as ft
from i18n import t
from flet_app.theme import c, SPACING
from flet_app.state import app_state


def onboarding_view_v2(page: ft.Page, route: str) -> ft.View:
    """Onboarding expandido com LGPD obrigatória como slide 5."""

    dark = app_state.dark_mode
    current = [0]
    lgpd_accepted = [False]

    slides = [
        {
            "icon": ft.Icons.DIRECTIONS_RUN,
            "icon_color": c("primary", dark),
            "title": "Bem-vindo ao App Treinos",
            "subtitle": "Software para Personal Trainers Profissionais",
            "body": (
                "Organize seus atletas, crie planos de treino "
                "personalizados e acompanhe o progresso com "
                "inteligência artificial opcional.\n\n"
                "Todos os seus dados ficam em seu computador."
            ),
            "highlight": None,
        },
        {
            "icon": ft.Icons.PEOPLE,
            "icon_color": c("success", dark),
            "title": "Organize seus atletas",
            "subtitle": "Gestão centralizada",
            "body": (
                "Crie um perfil completo para cada atleta:\n\n"
                "• Dados pessoais e parâmetros fisiológicos\n"
                "• Histórico de métricas (peso, VO2 max, etc)\n"
                "• Limitações de saúde e ciclo menstrual\n"
                "• Disponibilidade e preferências"
            ),
            "highlight": "NOVO",
        },
        {
            "icon": ft.Icons.SMART_TOY,
            "icon_color": c("primary", dark),
            "title": "Gere treinos com IA",
            "subtitle": "Automatização inteligente",
            "body": (
                "Configure múltiplos provedores de IA:\n\n"
                "• OpenAI (ChatGPT, GPT-4)\n"
                "• Anthropic (Claude)\n"
                "• Google (Gemini)\n"
                "• DeepSeek ou API personalizadas\n\n"
                "A IA sugere exercícios e periodização automática."
            ),
            "highlight": None,
        },
        {
            "icon": ft.Icons.SHOW_CHART,
            "icon_color": c("success", dark),
            "title": "Acompanhe o progresso",
            "subtitle": "Métricas em tempo real",
            "body": (
                "Visualize o desenvolvimento dos seus atletas:\n\n"
                "• Histórico de treinos realizados\n"
                "• Evolução de métricas fisiológicas\n"
                "• Gráficos de tendências\n"
                "• Exportar dados para análise\n"
                "• Conformidade com LGPD brasileira"
            ),
            "highlight": None,
        },
        {
            "icon": ft.Icons.LOCK,
            "icon_color": c("warning", dark),
            "title": "Proteção de Dados (LGPD)",
            "subtitle": "Conformidade brasileira obrigatória",
            "body": (
                "CONFORMIDADE LGPD:\n\n"
                "✓ Todos os dados são armazenados localmente NO SEU COMPUTADOR\n"
                "✓ Nenhuma informação pessoal de atletas é enviada a servidores externos\n"
                "✓ IA externa (opcional) receberá apenas dados anônimos de treino\n"
                "✓ Você controla total acesso e pode deletar dados de atletas\n\n"
                "Clique para ler: PRIVACY.md (política completa)"
            ),
            "is_lgpd": True,
            "show_checkbox": True,
        },
        {
            "icon": ft.Icons.CHECK_CIRCLE,
            "icon_color": c("success", dark),
            "title": "Vamos começar!",
            "subtitle": "Sistema pronto para uso",
            "body": (
                "Configuração concluída com sucesso!\n\n"
                "Na próxima tela você acessa o painel principal.\n\n"
                "Use o botão '+' para criar seu primeiro atleta "
                "e comece a gerar treinos imediatamente.\n\n"
                "Dúvidas? Veja o menu 'Ajuda' em qualquer momento."
            ),
            "highlight": "PRONTO",
            "is_final": True,
        },
    ]

    # ── Elementos visuais ────────────────────────────────────────
    icon_display = ft.Icon(
        slides[0]["icon"], size=100, color=slides[0].get("icon_color", c("primary", dark))
    )
    title_text = ft.Text(
        slides[0]["title"],
        size=28,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        color=c("text_primary", dark),
    )
    subtitle_text = ft.Text(
        slides[0]["subtitle"],
        size=14,
        text_align=ft.TextAlign.CENTER,
        color=c("primary", dark),
        weight=ft.FontWeight.W_500,
    )
    body_text = ft.Text(
        slides[0]["body"],
        size=14,
        text_align=ft.TextAlign.LEFT,
        color=c("text_secondary", dark),
        min_lines=5,
    )

    # Badge de destaque
    highlight_badge = ft.Container(
        visible=False,
        content=ft.Text(
            "", size=12, weight="bold", color="white",
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=c("success", dark),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=16,
    )

    # ── Checkbox LGPD (visível apenas no slide 5) ─────────────────
    lgpd_checkbox = ft.Checkbox(
        label="Entendo e confirmo que li a política de LGPD",
        value=False,
        visible=False,
    )

    def _on_lgpd_change(e):
        lgpd_accepted[0] = e.control.value
        btn_next.disabled = not lgpd_accepted[0]
        page.update()

    lgpd_checkbox.on_change = _on_lgpd_change

    # ── Link para ler PRIVACY.md
    privacy_link = ft.TextButton(
        "Ler política de privacidade completa (PRIVACY.md)",
        visible=False,
        on_click=lambda e: _open_privacy_doc()
    )

    def _open_privacy_doc():
        # Placeholder para abrir documento
        # Em produção, isso abrira usando webbrowser ou system open
        pass

    # ── Indicadores de página (dots) ──────
    def _build_dots():
        return ft.Row(
            [
                ft.Container(
                    width=14 if i != current[0] else 28,
                    height=14,
                    border_radius=7,
                    bgcolor=c("primary", dark) if i == current[0] else c("text_disabled", dark),
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                    animate_size=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                )
                for i in range(len(slides))
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    # ── Navegação ────────────────────────────────────────────────
    def _on_next():
        current[0] = min(current[0] + 1, len(slides) - 1)
        _update_slide()

    def _on_prev():
        current[0] = max(current[0] - 1, 0)
        _update_slide()

    def _update_slide():
        slide = slides[current[0]]
        icon_display.name = slide["icon"]
        icon_display.color = slide.get("icon_color", c("primary", dark))
        title_text.value = slide["title"]
        subtitle_text.value = slide.get("subtitle", "")
        body_text.value = slide["body"]

        # Highlight badge
        if slide.get("highlight"):
            highlight_badge.visible = True
            highlight_badge.content.value = slide["highlight"]
        else:
            highlight_badge.visible = False

        # LGPD checkbox e link
        lgpd_checkbox.visible = slide.get("show_checkbox", False)
        privacy_link.visible = slide.get("is_lgpd", False)

        # Botão "Próximo" desativado até aceitar LGPD
        if slide.get("is_lgpd", False):
            btn_next.disabled = not lgpd_accepted[0]
            btn_next.text = "Confirmar e Continuar ➜"
        else:
            btn_next.disabled = False
            btn_next.text = "Iniciar ➜" if current[0] == len(slides) - 1 else "Seguinte ➜"

        dots.controls = _build_dots().controls

        page.update()

    def _on_start():
        # Marcar onboarding como concluído
        app_state.mark_onboarding_complete()

        # Marcar LGPD como aceito (se aplicável)
        if lgpd_accepted[0]:
            app_state.mark_lgpd_confirmed()

        page.go("/dashboard")

    # ── Botões ───────────────────────────────────────────────────
    btn_prev = ft.TextButton("← Anterior", on_click=lambda e: _on_prev())
    btn_next = ft.TextButton("Seguinte ➜", on_click=lambda e: _on_next())

    def _wrap_button(btn):
        btn.on_click = lambda e: _on_start() if current[0] == len(slides) - 1 else (
            _on_next() if btn == btn_next else _on_prev()
        )
        return btn

    btn_next = _wrap_button(btn_next)

    dots = ft.Row(controls=_build_dots().controls, alignment=ft.MainAxisAlignment.CENTER)

    # ── Layout ────────────────────────────────────────────────────
    content = ft.Container(
        content=ft.Column(
            [
                # Conteúdo
                ft.Container(expand=True),
                icon_display,
                ft.Container(height=16),
                title_text,
                subtitle_text,
                ft.Container(height=20),
                body_text,
                ft.Container(height=20),
                highlight_badge,
                ft.Container(expand=True),

                # Privacy link (LGPD slide)
                privacy_link,

                # Dots
                dots,
                ft.Container(height=20),

                # LGPD checkbox
                lgpd_checkbox,
                ft.Container(height=12),

                # Navigation
                ft.Row(
                    [btn_prev, ft.Container(expand=True), btn_next],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        ),
        padding=ft.padding.symmetric(horizontal=32, vertical=40),
        expand=True,
        bgcolor=c("bg_primary", dark),
    )

    return ft.View(route=route, controls=[content], vertical_alignment=ft.MainAxisAlignment.START)
