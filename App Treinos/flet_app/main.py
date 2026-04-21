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
from flet_app.screens.onboarding_v2 import onboarding_view_v2 as onboarding_view
from flet_app.screens.initial_setup import initial_setup_view
from flet_app.screens.ai_config_screen import ai_config_view
from flet_app.components.calendar_view import calendar_view_screen
from flet_app.components.toast import setup_toasts


def main(page: ft.Page):
    """Ponto de entrada da aplicação Flet."""

    # ── Configuração da página ───────────────────────────────────
    page.title = "App Treinos v3.1"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = build_theme(dark=False)
    page.window.width = 1024
    page.window.height = 720
    page.window.min_width = 420
    page.window.min_height = 600

    # ── Inicializar sistema de toasts (notificações) ──────────────
    setup_toasts(page)

    # ── Router ───────────────────────────────────────────────────
    router = Router(page)

    router.add("/", splash_view)
    router.add("/splash", splash_view)
    router.add("/onboarding", onboarding_view)
    router.add("/initial-setup", initial_setup_view)
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
    router.add("/ai-config", ai_config_view)

    # ── Arranque ─────────────────────────────────────────────────
    page.go("/splash")


if __name__ == "__main__":
    ft.app(target=main)
