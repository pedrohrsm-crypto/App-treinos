"""
Splash Screen — Inicialização com progresso real
==================================================

Exibe logo, barra de progresso e texto de status enquanto
inicializa DB, carrega preferências e verifica sessão.
"""

import asyncio
import flet as ft
from i18n import t, set_language
from flet_app.theme import c, build_theme


def splash_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de splash com inicialização real."""

    from flet_app.state import app_state
    dark = app_state.dark_mode

    # ── Elementos visuais ────────────────────────────────────────
    logo = ft.Text(
        "🏃", size=80, text_align=ft.TextAlign.CENTER,
        opacity=0, animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
    )
    title = ft.Text(
        t("app_name"), size=40, weight=ft.FontWeight.BOLD,
        color=c("text_light", dark), text_align=ft.TextAlign.CENTER,
        opacity=0, animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_OUT),
    )
    status_text = ft.Text(
        "", size=14, color=c("text_light", dark),
        text_align=ft.TextAlign.CENTER,
        opacity=0, animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
    )
    progress_bar = ft.ProgressBar(
        value=0, width=280, color=c("text_light", dark),
        bgcolor=c("accent_hover", dark),
        opacity=0, animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
    )

    content = ft.Container(
        content=ft.Column(
            [logo, title, ft.Container(height=24), progress_bar, status_text],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True,
        bgcolor=c("bg_primary", dark),
    )

    # ── Helpers de progresso ─────────────────────────────────────
    async def _set_progress(value: float, msg: str):
        progress_bar.value = value
        status_text.value = msg
        page.update()
        await asyncio.sleep(0.15)

    # ── Sequência de inicialização real ──────────────────────────
    async def _init_sequence():
        await asyncio.sleep(0.3)  # aguardar montagem da view

        # Fade in dos elementos
        logo.opacity = 1
        title.opacity = 1
        progress_bar.opacity = 1
        status_text.opacity = 1
        page.update()
        await asyncio.sleep(0.5)

        # Etapa 1: Banco de dados
        await _set_progress(0.15, "Inicializando banco de dados…")
        from core.database import DatabaseManager
        app_state.db = DatabaseManager()
        await _set_progress(0.30, "Banco de dados pronto ✓")

        # Etapa 2: Preferências
        await _set_progress(0.45, "Carregando preferências…")
        session = app_state.load_session()
        await _set_progress(0.55, "Preferências carregadas ✓")

        # Etapa 3: Verificar sessão anterior
        auto_logged = False
        if session:
            await _set_progress(0.65, "Restaurando sessão…")
            # Suporta formato novo (password_hash) e legado (password_raw)
            if "password_hash" in session:
                ok, data = app_state.db.autenticar_por_hash(
                    session["credential"], session["password_hash"]
                )
            elif "password_raw" in session:
                ok, data = app_state.db.autenticar_usuario(
                    session["credential"], session["password_raw"]
                )
                # Migrar sessão legada para formato seguro
                if ok:
                    app_state.save_session(session["credential"], session["password_raw"])
            else:
                ok, data = False, None
            if ok:
                app_state.login(data)
                # Aplicar preferências persistidas
                prefs = app_state.load_preferences()
                if prefs:
                    app_state.dark_mode = prefs.get("dark_mode", False)
                    lang = prefs.get("language", "pt")
                    app_state.language = lang
                    set_language(lang)
                    page.theme_mode = ft.ThemeMode.DARK if app_state.dark_mode else ft.ThemeMode.LIGHT
                    page.theme = build_theme(dark=app_state.dark_mode)
                auto_logged = True
                await _set_progress(0.80, f"Bem-vindo, {app_state.trainer_name} ✓")
            else:
                app_state.clear_session()
                await _set_progress(0.80, "Sessão expirada")
        else:
            await _set_progress(0.80, "Pronto para login")

        # Etapa 4: Finalizar
        await _set_progress(1.0, "Iniciando…")
        await asyncio.sleep(0.4)

        # Navegar
        if auto_logged:
            page.go("/dashboard")
        elif not app_state.is_onboarding_completed():
            page.go("/onboarding")
        else:
            page.go("/login")

    page.run_task(_init_sequence)

    return ft.View(route="/", controls=[content])
