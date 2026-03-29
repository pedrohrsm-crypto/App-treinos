"""
App Treinos — Entry Point Flet
================================

Inicializa a aplicação Flet, configura tema, regista rotas
e arranca com a splash screen.
"""

import flet as ft

from flet_app.theme import build_theme, c
from flet_app.state import app_state
from flet_app.router import Router

# ── Screens ──────────────────────────────────────────────────────
from flet_app.screens.splash import splash_view
from flet_app.screens.login import login_view
from flet_app.screens.register import register_view
from flet_app.screens.dashboard import dashboard_view
from flet_app.screens.athlete_dashboard import athlete_dashboard_view
from flet_app.screens.training_wizard import training_wizard_view
from flet_app.screens.config import config_view
from flet_app.screens.admin import admin_view
from flet_app.screens.progress import progress_view
from flet_app.screens.fitness import fitness_view
from flet_app.screens.templates import templates_view
from flet_app.screens.onboarding import onboarding_view
from flet_app.components.calendar_view import calendar_view_screen


def main(page: ft.Page):
    """Ponto de entrada da aplicação Flet."""

    # ── Configuração da página ───────────────────────────────────
    page.title = "App Treinos v3.0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = build_theme(dark=False)
    page.window.width = 420
    page.window.height = 740
    page.window.min_width = 360
    page.window.min_height = 600

    # ── Router ───────────────────────────────────────────────────
    router = Router(page)

    router.add("/", splash_view)
    router.add("/splash", splash_view)
    router.add("/onboarding", onboarding_view)
    router.add("/login", login_view)
    router.add("/register", register_view)
    router.add("/dashboard", dashboard_view)
    router.add("/athlete", athlete_dashboard_view)
    router.add("/wizard", training_wizard_view)
    router.add("/calendar", calendar_view_screen)
    router.add("/config", config_view)
    router.add("/admin", admin_view)
    router.add("/progress", progress_view)
    router.add("/fitness", fitness_view)
    router.add("/templates", templates_view)

    # ── Arranque ─────────────────────────────────────────────────
    page.go("/splash")


if __name__ == "__main__":
    ft.app(target=main)
