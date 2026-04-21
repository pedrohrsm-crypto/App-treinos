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
    """Constrói a View de splash com inicialização real e animações profissionais."""

    from flet_app.state import app_state
    dark = app_state.dark_mode

    # ── Elementos visuais ────────────────────────────────────────
    # Logo animado com fade-in e scale
    logo = ft.Icon(
        ft.Icons.DIRECTIONS_RUN, size=60,
        color=c("text_light", dark),
        opacity=0,
        animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_OUT),
        scale=0.8,
        animate_scale=ft.Animation(700, ft.AnimationCurve.EASE_OUT),
    )

    title = ft.Text(
        t("app_name"), size=48, weight=ft.FontWeight.BOLD,
        color=c("text_light", dark), text_align=ft.TextAlign.CENTER,
        opacity=0, animate_opacity=ft.Animation(700, ft.AnimationCurve.EASE_OUT),
    )

    subtitle = ft.Text(
        t("app_subtitle") if hasattr(page, 'locale') else "Treinos Inteligentes em Segundos",
        size=14, color=c("text_secondary", dark), text_align=ft.TextAlign.CENTER,
        opacity=0, animate_opacity=ft.Animation(800, ft.AnimationCurve.EASE_OUT),
    )

    # Barra de progresso melhorada com indicadores de etapas
    progress_bar = ft.ProgressBar(
        value=0, width=300, height=4,
        color=c("primary", dark),
        bgcolor=c("accent_hover", dark),
        opacity=0, animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
    )

    # Labels de progresso por etapa (Database, Session, Preferences, Theme, Done)
    step_labels = ft.Row(
        [
            ft.Column([
                ft.Text("Database", size=10, color=c("text_secondary", dark)),
                ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, size=12,
                       color=c("text_secondary", dark), name="step_1_icon")
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.Text("Session", size=10, color=c("text_secondary", dark)),
                ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, size=12,
                       color=c("text_secondary", dark), name="step_2_icon")
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.Text("Preferences", size=10, color=c("text_secondary", dark)),
                ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, size=12,
                       color=c("text_secondary", dark), name="step_3_icon")
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.Text("Theme", size=10, color=c("text_secondary", dark)),
                ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, size=12,
                       color=c("text_secondary", dark), name="step_4_icon")
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.Text("Ready", size=10, color=c("text_secondary", dark)),
                ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, size=12,
                       color=c("text_secondary", dark), name="step_5_icon")
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ],
        spacing=20, alignment=ft.MainAxisAlignment.CENTER,
        opacity=0, animate_opacity=ft.Animation(800, ft.AnimationCurve.EASE_OUT),
    )

    status_text = ft.Text(
        "", size=13, color=c("text_light", dark),
        text_align=ft.TextAlign.CENTER,
        opacity=0, animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
    )


    content = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=40),  # Top spacing
                logo,
                ft.Container(height=12),
                title,
                ft.Container(height=4),
                subtitle,
                ft.Container(height=48),  # Space before progress
                progress_bar,
                ft.Container(height=24),
                step_labels,
                ft.Container(height=32),
                status_text,
                ft.Container(height=40),  # Bottom spacing
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True,
        bgcolor=c("bg_primary", dark),
    )

    # ── Helpers de progresso ─────────────────────────────────────
    def _mark_step_complete(step_num: int):
        """Marca um passo como completo com checkmark."""
        icon_name = f"step_{step_num}_icon"
        for control in step_labels.controls:
            if hasattr(control, 'controls'):
                for subcontrol in control.controls:
                    if hasattr(subcontrol, 'name') and subcontrol.name == icon_name:
                        subcontrol.name_old = subcontrol.name
                        subcontrol.name = ft.Icons.CHECK_CIRCLE
                        subcontrol.color = c("primary", dark)
                        page.update()

    async def _set_progress(value: float, msg: str, mark_step: int = 0):
        progress_bar.value = min(value, 1.0)
        status_text.value = msg
        if mark_step > 0:
            _mark_step_complete(mark_step)
        page.update()
        await asyncio.sleep(0.1)

    # ── Sequência de inicialização real ──────────────────────────
    async def _init_sequence():
        await asyncio.sleep(0.3)  # aguardar montagem da view

        # Fade in dos elementos com efeito cascata
        logo.opacity = 1
        logo.scale = 1.0
        page.update()
        await asyncio.sleep(0.3)

        title.opacity = 1
        page.update()
        await asyncio.sleep(0.2)

        subtitle.opacity = 1
        progress_bar.opacity = 1
        step_labels.opacity = 1
        status_text.opacity = 1
        page.update()
        await asyncio.sleep(0.3)

        # Etapa 1: Banco de dados
        await _set_progress(0.20, "Inicializando banco de dados…", 1)
        from core.database import DatabaseManager
        app_state.db = DatabaseManager()
        await asyncio.sleep(0.2)

        # Etapa 1.5: Verificar setup inicial
        if app_state.db.needs_initial_setup():
            await _set_progress(1.0, "Configuração inicial necessária…", 5)
            await asyncio.sleep(0.5)
            page.go("/initial-setup")
            return

        # Etapa 2: Preferências
        await _set_progress(0.40, "Carregando preferências…", 2)
        session = app_state.load_session()
        await asyncio.sleep(0.2)

        # Etapa 3: Verificar sessão anterior
        auto_logged = False
        if session:
            await _set_progress(0.60, "Restaurando sessão…", 3)
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
                await _set_progress(0.80, f"Bem-vindo, {app_state.trainer_name}", 4)
            else:
                app_state.clear_session()
                await _set_progress(0.80, "Sessão expirada", 4)
        else:
            await _set_progress(0.80, "Pronto para login", 4)

        await asyncio.sleep(0.2)

        # Etapa 4: Finalizar
        await _set_progress(1.0, "Iniciando…", 5)
        await asyncio.sleep(0.6)  # Delay profissional após 100%

        # Fade out suave antes de navegar
        logo.opacity = 0
        title.opacity = 0
        subtitle.opacity = 0
        progress_bar.opacity = 0
        step_labels.opacity = 0
        status_text.opacity = 0
        page.update()
        await asyncio.sleep(0.3)

        # Navegar
        if auto_logged:
            page.go("/dashboard")
        elif not app_state.is_onboarding_completed() or not app_state.is_eula_accepted():
            page.go("/onboarding")
        else:
            page.go("/login")

    page.run_task(_init_sequence)

    return ft.View(route="/", controls=[content])
