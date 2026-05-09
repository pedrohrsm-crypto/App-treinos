"""
NavBar — Barra de navegação inferior
======================================

4 destinos: Dashboard | Progresso | Fitness | Config.
"""

import flet as ft
from i18n import t


def build_nav_bar(page: ft.Page, selected_index: int = 0) -> ft.NavigationBar:
    """Constrói NavigationBar universal."""

    def _on_change(e):
        idx = e.control.selected_index
        routes = ["/dashboard", "/progress", "/fitness", "/config"]
        page.go(routes[idx])

    return ft.NavigationBar(
        selected_index=selected_index,
        on_change=_on_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Dashboard"),
            ft.NavigationBarDestination(icon=ft.Icons.BAR_CHART_OUTLINED, selected_icon=ft.Icons.BAR_CHART, label=t("card_progress") if t("card_progress") != "card_progress" else "Progresso"),
            ft.NavigationBarDestination(icon=ft.Icons.WATCH_OUTLINED, selected_icon=ft.Icons.WATCH, label="Fitness"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label="Config"),
        ],
    )
