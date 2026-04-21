"""
Progress — Estatísticas e changelog do treinador
=================================================

Cards de stats horizontais + distribuição por desporto + changelog.
Dados carregados assincronamente com spinner.
"""

import asyncio
import flet as ft
from i18n import t
from flet_app.theme import c, SPORT_COLORS, RADIUS, SPACING, card_shadow
from flet_app.state import app_state
from flet_app.components.adaptive_nav import build_adaptive_layout
from flet_app.components.loading_overlay import build_loading
from flet_app.components.hover_effects import apply_hover_effects_to_card
from training_manager import training_manager


def progress_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de progresso/estatísticas."""

    dark = app_state.dark_mode
    trainer = app_state.trainer_info()

    body = ft.Container(content=build_loading(t("progress_loading"), dark), expand=True, padding=ft.padding.all(16))

    async def _load_data():
        await asyncio.sleep(0.01)

        stats = training_manager.get_statistics(trainer) if trainer else {}
        changelog = training_manager.get_changelog(trainer) if trainer else []

        # Stats cards
        def _stat(icon_name, value, label):
            container = ft.Container(
                content=ft.Column(
                    [ft.Icon(icon_name, size=24, color=c("primary", dark)), ft.Text(value, size=20, weight=ft.FontWeight.BOLD), ft.Text(label, size=11, color=c("text_secondary", dark))],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2,
                ),
                padding=SPACING["md"], border_radius=RADIUS["md"], bgcolor=c("bg_card", dark),
                shadow=card_shadow(dark, "sm"), expand=True,
            )
            return apply_hover_effects_to_card(container, scale_ratio=1.02, shadow_level="lg", dark=dark)

        stats_row = ft.Row(
            [
                _stat(ft.Icons.ASSIGNMENT, str(stats.get("total_plans", 0)), t("progress_plans_label")),
                _stat(ft.Icons.GROUP, str(stats.get("unique_athletes", 0)), t("progress_athletes_label")),
                _stat(ft.Icons.CALENDAR_TODAY, stats.get("latest_plan", "—") or "—", t("progress_latest_label")),
            ],
            spacing=10,
        )

        # Distribuição por desporto
        sport_dist = stats.get("sports_distribution", {})
        total = max(sum(sport_dist.values()), 1)
        sport_bars = []
        for sport, count in sorted(sport_dist.items(), key=lambda x: -x[1]):
            pct = count / total
            color = SPORT_COLORS.get(sport, c("primary", dark))
            sport_bars.append(
                ft.Column([
                    ft.Row([ft.Text(sport, size=13, expand=True), ft.Text(str(count), size=13, weight=ft.FontWeight.BOLD)]),
                    ft.ProgressBar(value=pct, color=color, bgcolor=c("border_light", dark)),
                ], spacing=4)
            )
        if not sport_bars:
            sport_bars.append(ft.Text(t("progress_no_data"), size=13, color=c("text_secondary", dark)))

        # Changelog
        log_items = []
        for entry in changelog[:20]:
            action = entry.action if hasattr(entry, "action") else str(entry)
            ts = entry.timestamp if hasattr(entry, "timestamp") else ""
            detail = entry.details if hasattr(entry, "details") else ""
            log_container = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.EDIT_NOTE, size=16, color=c("primary", dark)),
                    ft.Column([
                        ft.Text(action, size=13, weight=ft.FontWeight.W_500),
                        ft.Text(f"{ts} — {detail}", size=11, color=c("text_secondary", dark)),
                    ], spacing=1, expand=True),
                ], spacing=8),
                padding=8,
                border=ft.border.only(bottom=ft.BorderSide(1, c("border_light", dark))),
            )
            log_items.append(apply_hover_effects_to_card(log_container, scale_ratio=1.02, shadow_level="md", dark=dark))
        if not log_items:
            log_items.append(ft.Text(t("progress_no_log"), size=13, color=c("text_secondary", dark)))

        body.content = ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.INSIGHTS, size=22, color=c("primary", dark)), ft.Text(t("progress_header"), size=20, weight=ft.FontWeight.BOLD)], spacing=SPACING["sm"]),
                stats_row,
                ft.Divider(height=20),
                ft.Text(t("progress_sport_dist"), size=16, weight=ft.FontWeight.W_600),
                *sport_bars,
                ft.Divider(height=20),
                ft.Text(t("progress_changelog_title"), size=16, weight=ft.FontWeight.W_600),
                *log_items,
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        page.update()

    page.run_task(_load_data)

    return build_adaptive_layout(
        page=page,
        selected_index=1,
        body=body,
        dark=dark,
    )
