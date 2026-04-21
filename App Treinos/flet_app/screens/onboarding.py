"""
Onboarding — Carrossel de boas-vindas (primeiro uso)
=====================================================

Exibido apenas na primeira execução ou quando o EULA
ainda não foi aceito. Apresenta as funcionalidades do app
em 4 slides + slide de aceitação de Termos de Uso.
"""

import flet as ft
from i18n import t
from flet_app.theme import c
from flet_app.state import app_state


def onboarding_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de onboarding com 4 slides + EULA."""

    dark = app_state.dark_mode
    current = [0]
    eula_accepted = [False]

    slides = [
        {
            "icon": ft.Icons.DIRECTIONS_RUN,
            "title": t("onboarding_welcome_title"),
            "body": t("onboarding_welcome_body"),
        },
        {
            "icon": ft.Icons.ASSIGNMENT,
            "title": t("onboarding_plans_title"),
            "body": t("onboarding_plans_body"),
        },
        {
            "icon": ft.Icons.INSIGHTS,
            "title": t("onboarding_progress_title"),
            "body": t("onboarding_progress_body"),
        },
        {
            "icon": ft.Icons.WATCH,
            "title": t("onboarding_devices_title"),
            "body": t("onboarding_devices_body"),
        },
        {
            "icon": ft.Icons.GAVEL,
            "title": "Termos de Uso",
            "body": (
                "Ao utilizar o App Treinos, voce concorda com nossos Termos de Uso "
                "e Politica de Privacidade.\n\n"
                "Resumo:\n"
                "- Seus dados sao armazenados localmente no seu computador\n"
                "- Nenhum dado pessoal e enviado a servidores externos\n"
                "- A integracao com IA (opcional) envia dados de treino ao provedor escolhido\n"
                "- O software e uma ferramenta de apoio, nao substitui o julgamento profissional\n\n"
                "Os documentos completos (EULA.md e PRIVACY.md) estao disponiveis "
                "no diretorio de instalacao do software."
            ),
            "is_eula": True,
        },
    ]

    # ── Elementos visuais ────────────────────────────────────────
    icon_display = ft.Icon(slides[0]["icon"], size=72, color=c("primary", dark))
    title_text = ft.Text(
        slides[0]["title"], size=26, weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER, color=c("text_primary", dark),
    )
    body_text = ft.Text(
        slides[0]["body"], size=17, text_align=ft.TextAlign.CENTER,
        color=c("text_secondary", dark),
    )

    # ── Checkbox EULA (visível apenas no slide 5) ──────────────
    eula_checkbox = ft.Checkbox(
        label="Li e aceito os Termos de Uso e a Politica de Privacidade",
        value=False,
        visible=False,
    )

    def _on_eula_change(e):
        eula_accepted[0] = e.control.value
        btn_start.disabled = not eula_accepted[0]
        page.update()

    eula_checkbox.on_change = _on_eula_change

    # ── Indicadores de página (maiores para acessibilidade) ──────
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
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )

    dots_row = _build_dots()

    # ── Navegação ────────────────────────────────────────────────
    btn_back = ft.TextButton(
        t("onboarding_back"),
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda _: _go_back(),
        style=ft.ButtonStyle(color=c("text_secondary", dark)),
        visible=False,
    )
    btn_skip = ft.TextButton(
        t("onboarding_skip"),
        on_click=lambda _: _skip_to_eula(),
        style=ft.ButtonStyle(color=c("text_secondary", dark)),
    )
    btn_next = ft.ElevatedButton(
        t("onboarding_next"),
        icon=ft.Icons.ARROW_FORWARD,
        bgcolor=c("primary", dark),
        color=c("text_light", dark),
        on_click=lambda _: _advance(),
    )
    btn_start = ft.ElevatedButton(
        "Aceitar e Comecar",
        icon=ft.Icons.ROCKET_LAUNCH,
        bgcolor=c("primary", dark),
        color=c("text_light", dark),
        width=240,
        height=48,
        on_click=lambda _: _finish(),
        disabled=True,
    )
    btn_start.visible = False

    def _update_slide():
        slide = slides[current[0]]
        icon_display.name = slide["icon"]
        title_text.value = slide["title"]
        body_text.value = slide["body"]

        is_last = current[0] == len(slides) - 1
        is_first = current[0] == 0
        btn_next.visible = not is_last
        btn_skip.visible = not is_last
        btn_start.visible = is_last
        btn_start.disabled = not eula_accepted[0]
        btn_back.visible = not is_first
        eula_checkbox.visible = is_last

        # Rebuild dots
        nonlocal dots_row
        dots_row.controls.clear()
        for i in range(len(slides)):
            dots_row.controls.append(
                ft.Container(
                    width=28 if i == current[0] else 14,
                    height=14,
                    border_radius=7,
                    bgcolor=c("primary", dark) if i == current[0] else c("text_disabled", dark),
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                )
            )
        page.update()

    def _advance():
        if current[0] < len(slides) - 1:
            current[0] += 1
            _update_slide()

    def _go_back():
        if current[0] > 0:
            current[0] -= 1
            _update_slide()

    def _skip_to_eula():
        current[0] = len(slides) - 1
        _update_slide()

    def _finish():
        if not eula_accepted[0]:
            return
        app_state.set_onboarding_completed()
        app_state.set_eula_accepted()
        page.go("/login")

    # ── Layout ───────────────────────────────────────────────────
    content = ft.Container(
        content=ft.Column(
            [
                ft.Container(expand=1),
                icon_display,
                ft.Container(height=16),
                title_text,
                ft.Container(height=12),
                ft.Container(
                    content=body_text,
                    padding=ft.padding.symmetric(horizontal=32),
                ),
                ft.Container(height=8),
                eula_checkbox,
                ft.Container(expand=1),
                dots_row,
                ft.Container(height=24),
                ft.Row(
                    [btn_back, btn_skip, ft.Container(expand=True), btn_next],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                btn_start,
                ft.Container(height=16),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
        padding=ft.padding.symmetric(horizontal=24, vertical=32),
        expand=True,
        bgcolor=c("bg_secondary", dark),
    )

    return ft.View(
        route="/onboarding",
        controls=[content],
        bgcolor=c("bg_secondary", dark),
    )
