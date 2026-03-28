"""
Splash Screen — Animação de abertura
=====================================

Exibe logo + nome da app por 2 s e redireciona para /login.
"""

import flet as ft
from i18n import t
from flet_app.theme import c
from flet_app.state import app_state


def splash_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de splash."""

    dark = app_state.dark_mode

    logo = ft.Text(
        "🏃",
        size=80,
        text_align=ft.TextAlign.CENTER,
        opacity=0,
        animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_OUT),
    )
    title = ft.Text(
        t("app_name"),
        size=40,
        weight=ft.FontWeight.BOLD,
        color=c("text_light", dark),
        text_align=ft.TextAlign.CENTER,
        opacity=0,
        animate_opacity=ft.Animation(800, ft.AnimationCurve.EASE_OUT),
    )
    subtitle = ft.Text(
        t("splash_subtitle"),
        size=16,
        color=c("text_light", dark),
        text_align=ft.TextAlign.CENTER,
        opacity=0,
        animate_opacity=ft.Animation(1000, ft.AnimationCurve.EASE_OUT),
    )

    content = ft.Container(
        content=ft.Column(
            [logo, title, subtitle],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True,
        bgcolor=c("bg_primary", dark),
    )

    def _animate_and_redirect(_):
        logo.opacity = 1
        title.opacity = 1
        subtitle.opacity = 1
        page.update()

        import time
        time.sleep(2)
        page.go("/login")

    page.on_connect = None  # reset
    content.on_click = None  # no interaction needed

    # Trigger animation after view is mounted
    def _on_view(_):
        import threading
        threading.Thread(target=_animate_and_redirect, args=(None,), daemon=True).start()

    page.on_connect = _on_view
    # Also schedule directly for desktop (no on_connect event)
    import threading
    threading.Timer(0.3, _animate_and_redirect, args=(None,)).start()

    return ft.View(route="/", controls=[content])
