"""
Dashboard — Grid de Hero Cards de Atletas
===========================================

Tela principal pós-login. Mostra saudação, barra de pesquisa,
grid responsivo de athlete cards e FAB para criar novo plano.
"""

import flet as ft
from i18n import t
from flet_app.theme import c
from flet_app.state import app_state
from flet_app.components.nav_bar import build_nav_bar
from flet_app.components.athlete_card import build_athlete_card
from training_manager import training_manager


def dashboard_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View do dashboard de atletas."""

    dark = app_state.dark_mode
    trainer = app_state.trainer_info()

    # ── Dados ────────────────────────────────────────────────────
    athletes = training_manager.get_athletes_summary(trainer) if trainer else []

    # ── Pesquisa ─────────────────────────────────────────────────
    search_field = ft.TextField(
        hint_text="Pesquisar atleta…",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=24,
        filled=True,
        height=44,
        expand=True,
        on_change=lambda e: _filter(e.control.value),
    )

    # ── Grid de cards ────────────────────────────────────────────
    grid = ft.GridView(
        runs_count=2,
        max_extent=360,
        child_aspect_ratio=1.7,
        spacing=16,
        run_spacing=16,
        padding=ft.padding.symmetric(horizontal=16),
        expand=True,
    )

    def _populate(filter_text: str = ""):
        grid.controls.clear()
        ft_lower = filter_text.lower()
        for summary in athletes:
            name = summary["athlete_name"]
            sport = summary["latest_sport"]
            if ft_lower and ft_lower not in name.lower() and ft_lower not in sport.lower():
                continue
            card = build_athlete_card(
                summary,
                on_click=lambda _, n=name: _go_athlete(n),
                dark=dark,
            )
            grid.controls.append(card)

        if not grid.controls:
            grid.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("📭", size=48),
                            ft.Text("Nenhum atleta encontrado", size=16, color=c("text_secondary", dark)),
                            ft.Text("Crie um plano de treino para começar.", size=13, color=c("text_disabled", dark)),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            )

    def _filter(text: str):
        _populate(text)
        page.update()

    def _go_athlete(name: str):
        app_state.selected_athlete = name
        page.go(f"/athlete/{name}")

    def _go_wizard(_):
        page.go("/wizard")

    _populate()

    # ── Header ───────────────────────────────────────────────────
    greeting = t("dashboard_greeting", name=app_state.trainer_name or "")
    header = ft.Container(
        content=ft.Column(
            [
                ft.Text(greeting, size=22, weight=ft.FontWeight.BOLD),
                ft.Row([search_field], spacing=8),
            ],
            spacing=8,
        ),
        padding=ft.padding.only(left=16, right=16, top=12, bottom=4),
    )

    # ── FAB ──────────────────────────────────────────────────────
    fab = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        text="Novo Plano",
        bgcolor=c("primary", dark),
        foreground_color=c("text_light", dark),
        on_click=_go_wizard,
    )

    return ft.View(
        route="/dashboard",
        controls=[header, grid],
        navigation_bar=build_nav_bar(page, selected_index=0),
        floating_action_button=fab,
    )
