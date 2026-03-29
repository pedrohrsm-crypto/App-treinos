"""
Onboarding — Carrossel de boas-vindas (primeiro uso)
=====================================================

Exibido apenas na primeira execução. Apresenta as
funcionalidades do app em 4 slides com navegação por
botões e indicadores de página.
"""

import flet as ft
from i18n import t
from flet_app.theme import c
from flet_app.state import app_state


def onboarding_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de onboarding com 4 slides."""

    dark = app_state.dark_mode
    current = [0]

    slides = [
        {
            "emoji": "🏃",
            "title": t("onboarding_welcome_title"),
            "body": t("onboarding_welcome_body"),
        },
        {
            "emoji": "📋",
            "title": t("onboarding_plans_title"),
            "body": t("onboarding_plans_body"),
        },
        {
            "emoji": "📊",
            "title": t("onboarding_progress_title"),
            "body": t("onboarding_progress_body"),
        },
        {
            "emoji": "⌚",
            "title": t("onboarding_devices_title"),
            "body": t("onboarding_devices_body"),
        },
    ]

    # ── Elementos visuais ────────────────────────────────────────
    emoji_text = ft.Text(slides[0]["emoji"], size=72, text_align=ft.TextAlign.CENTER)
    title_text = ft.Text(
        slides[0]["title"], size=26, weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER, color=c("text_primary", dark),
    )
    body_text = ft.Text(
        slides[0]["body"], size=15, text_align=ft.TextAlign.CENTER,
        color=c("text_secondary", dark),
    )

    # ── Indicadores de página ────────────────────────────────────
    def _build_dots():
        return ft.Row(
            [
                ft.Container(
                    width=10 if i != current[0] else 24,
                    height=10,
                    border_radius=5,
                    bgcolor=c("primary", dark) if i == current[0] else c("text_disabled", dark),
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                    animate_size=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                )
                for i in range(len(slides))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        )

    dots_row = _build_dots()

    # ── Navegação ────────────────────────────────────────────────
    btn_skip = ft.TextButton(
        t("onboarding_skip"),
        on_click=lambda _: _finish(),
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
        t("onboarding_start"),
        icon=ft.Icons.ROCKET_LAUNCH,
        bgcolor=c("primary", dark),
        color=c("text_light", dark),
        width=200,
        height=48,
        on_click=lambda _: _finish(),
    )
    btn_start.visible = False

    def _update_slide():
        slide = slides[current[0]]
        emoji_text.value = slide["emoji"]
        title_text.value = slide["title"]
        body_text.value = slide["body"]

        is_last = current[0] == len(slides) - 1
        btn_next.visible = not is_last
        btn_skip.visible = not is_last
        btn_start.visible = is_last

        # Rebuild dots
        nonlocal dots_row
        dots_row.controls.clear()
        for i in range(len(slides)):
            dots_row.controls.append(
                ft.Container(
                    width=24 if i == current[0] else 10,
                    height=10,
                    border_radius=5,
                    bgcolor=c("primary", dark) if i == current[0] else c("text_disabled", dark),
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                )
            )
        page.update()

    def _advance():
        if current[0] < len(slides) - 1:
            current[0] += 1
            _update_slide()

    def _finish():
        app_state.set_onboarding_completed()
        page.go("/login")

    # ── Layout ───────────────────────────────────────────────────
    content = ft.Container(
        content=ft.Column(
            [
                ft.Container(expand=1),
                emoji_text,
                ft.Container(height=16),
                title_text,
                ft.Container(height=12),
                ft.Container(
                    content=body_text,
                    padding=ft.padding.symmetric(horizontal=32),
                ),
                ft.Container(expand=1),
                dots_row,
                ft.Container(height=24),
                ft.Row(
                    [btn_skip, btn_next],
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
