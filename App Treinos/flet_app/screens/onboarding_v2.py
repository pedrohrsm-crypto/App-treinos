"""
Onboarding Melhorado v2 — 5 slides com foco em ação
====================================================

Novo fluxo:
1. Bem-vindo (valor prop)
2. Crie treino em 2 min (benefit)
3. Conecte IA (setup opcional)
4. Vamos começar! (CTA)
5. Termos de Uso (legal)

Plus: Opção de criar primeiro treino guiado após onboarding.
"""

import flet as ft
from i18n import t
from flet_app.theme import c, SPACING
from flet_app.state import app_state


def onboarding_view_v2(page: ft.Page, route: str) -> ft.View:
    """Onboarding melhorado com foco em ação rápida."""

    dark = app_state.dark_mode
    current = [0]
    eula_accepted = [False]

    slides = [
        {
            "icon": ft.Icons.DIRECTIONS_RUN,
            "icon_color": c("primary", dark),
            "title": "Bem-vindo ao App Treinos",
            "subtitle": "Crie planos de treino em minutos",
            "body": (
                "Organize seus atletas, personalize treinos "
                "e acompanhe progresso com inteligência artificial opcional."
            ),
            "highlight": None,
        },
        {
            "icon": ft.Icons.FLASH_ON,
            "icon_color": c("success", dark),
            "title": "Crie um treino em 2 minutos",
            "subtitle": "Processo guiado",
            "body": (
                "1. Escolha o atleta\n"
                "2. Selecione modalidade (corrida, musculação, etc)\n"
                "3. Aproveite templates pré-feitos\n"
                "4. Ajuste e pronto!"
            ),
            "highlight": "RÁPIDO",
        },
        {
            "icon": ft.Icons.SMART_TOY,
            "icon_color": c("primary", dark),
            "title": "Potencialize com IA (opcional)",
            "subtitle": "Sugestões inteligentes",
            "body": (
                "Conecte OpenAI, Anthropic ou outro provedor.\n\n"
                "A IA sugere exercícios, periodização e adaptações "
                "conforme o progresso do atleta.\n\n"
                "Pode deixar para depois."
            ),
            "highlight": None,
        },
        {
            "icon": ft.Icons.CHECK_CIRCLE,
            "icon_color": c("success", dark),
            "title": "Vamos começar!",
            "subtitle": "Estamos prontos",
            "body": (
                "Na próxima tela você verá seu painel.\n\n"
                "Use o botão '+' para criar seu primeiro atleta e treino.\n\n"
                "Qualquer dúvida? Veja a documentação em Configurações."
            ),
            "highlight": "PRÓXIMO",
        },
        {
            "icon": ft.Icons.GAVEL,
            "icon_color": c("warning", dark),
            "title": "Termos de Uso & Privacidade",
            "subtitle": "Importante",
            "body": (
                "✓ Seus dados estão SEMPRE locais (no seu computador)\n"
                "✓ Nenhum dado pessoal é enviado a servers externos\n"
                "✓ IA (opcional) pode compartilhar vossos treinos com o provedor escolhido\n"
                "✓ O app é uma ferramenta de apoio, não substitui avaliação profissional\n\n"
                "Documentos completos: EULA.md e PRIVACY.md na pasta de instalação"
            ),
            "is_eula": True,
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
        size=15,
        text_align=ft.TextAlign.CENTER,
        color=c("text_secondary", dark),
        min_lines=4,
    )

    # Badge de "RÁPIDO" ou "PRÓXIMO" se existir
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

    # ── Checkbox EULA (visível apenas no slide 5) ──────────────
    eula_checkbox = ft.Checkbox(
        label="Li e aceito Termos de Uso e Privacidade",
        value=False,
        visible=False,
    )

    def _on_eula_change(e):
        eula_accepted[0] = e.control.value
        btn_next.disabled = not eula_accepted[0]
        page.update()

    eula_checkbox.on_change = _on_eula_change

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

        # EULA
        eula_checkbox.visible = slide.get("is_eula", False)
        btn_next.disabled = slide.get("is_eula", False) and not eula_accepted[0]
        btn_next.text = "Iniciar ➜" if current[0] == len(slides) - 1 else "Seguinte ➜"
        dots.controls = _build_dots().controls

        page.update()

    def _on_start():
        # Marcar onboarding como concluído
        app_state.db.mark_onboarding_complete()
        app_state.db.mark_eula_accepted()
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
                ft.Container(height=24),
                body_text,
                ft.Container(height=24),
                highlight_badge,
                ft.Container(expand=True),

                # Dots
                dots,
                ft.Container(height=24),

                # EULA checkbox
                eula_checkbox,

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
