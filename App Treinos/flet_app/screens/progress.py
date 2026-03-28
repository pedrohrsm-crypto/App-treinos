"""
Progress — Estatísticas e changelog do treinador
=================================================

Cards de stats horizontais + distribuição por desporto + changelog.
"""

import flet as ft
from i18n import t
from flet_app.theme import c, SPORT_COLORS
from flet_app.state import app_state
from flet_app.components.nav_bar import build_nav_bar
from training_manager import training_manager


def progress_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de progresso/estatísticas."""

    dark = app_state.dark_mode
    trainer = app_state.trainer_info()

    stats = training_manager.get_statistics(trainer) if trainer else {}
    changelog = training_manager.get_changelog(trainer) if trainer else []

    # ── Stats cards ──────────────────────────────────────────────
    def _stat(icon: str, value: str, label: str) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [ft.Text(icon, size=24), ft.Text(value, size=20, weight=ft.FontWeight.BOLD), ft.Text(label, size=11, color=c("text_secondary", dark))],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
            padding=16,
            border_radius=12,
            bgcolor=c("bg_card", dark),
            shadow=ft.BoxShadow(blur_radius=4, color=c("shadow", dark)),
            expand=True,
        )

    stats_row = ft.Row(
        [
            _stat("📋", str(stats.get("total_plans", 0)), "Planos"),
            _stat("👥", str(stats.get("unique_athletes", 0)), "Atletas"),
            _stat("📅", stats.get("latest_plan", "—") or "—", "Último"),
        ],
        spacing=10,
    )

    # ── Distribuição por desporto ────────────────────────────────
    sport_dist = stats.get("sports_distribution", {})
    total = max(sum(sport_dist.values()), 1)

    sport_bars = []
    for sport, count in sorted(sport_dist.items(), key=lambda x: -x[1]):
        pct = count / total
        color = SPORT_COLORS.get(sport, c("primary", dark))
        sport_bars.append(
            ft.Column([
                ft.Row([
                    ft.Text(sport, size=13, expand=True),
                    ft.Text(str(count), size=13, weight=ft.FontWeight.BOLD),
                ]),
                ft.ProgressBar(value=pct, color=color, bgcolor=c("border_light", dark)),
            ], spacing=4)
        )

    if not sport_bars:
        sport_bars.append(ft.Text("Sem dados.", size=13, color=c("text_secondary", dark)))

    # ── Changelog ────────────────────────────────────────────────
    log_items = []
    for entry in changelog[:20]:
        action = entry.action if hasattr(entry, "action") else str(entry)
        ts = entry.timestamp if hasattr(entry, "timestamp") else ""
        detail = entry.details if hasattr(entry, "details") else ""
        log_items.append(
            ft.Container(
                content=ft.Row([
                    ft.Text("📝", size=16),
                    ft.Column([
                        ft.Text(action, size=13, weight=ft.FontWeight.W_500),
                        ft.Text(f"{ts} — {detail}", size=11, color=c("text_secondary", dark)),
                    ], spacing=1, expand=True),
                ], spacing=8),
                padding=8,
                border=ft.border.only(bottom=ft.BorderSide(1, c("border_light", dark))),
            )
        )

    if not log_items:
        log_items.append(ft.Text("Sem registos.", size=13, color=c("text_secondary", dark)))

    return ft.View(
        route="/progress",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("📊 Progresso", size=20, weight=ft.FontWeight.BOLD),
                        stats_row,
                        ft.Divider(height=20),
                        ft.Text("Distribuição por Desporto", size=16, weight=ft.FontWeight.W_600),
                        *sport_bars,
                        ft.Divider(height=20),
                        ft.Text("Changelog", size=16, weight=ft.FontWeight.W_600),
                        *log_items,
                    ],
                    spacing=12,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                padding=ft.padding.all(16),
                expand=True,
            )
        ],
        navigation_bar=build_nav_bar(page, selected_index=1),
        bgcolor=c("bg_secondary", dark),
    )
