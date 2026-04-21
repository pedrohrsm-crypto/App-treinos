"""
Fitness — Conectores de fitness (Strava, Garmin)
================================================

Ecrã com conexão OAuth via Strava e lista de atividades importadas.
"""

import flet as ft
from flet_app.theme import c, SPACING
from flet_app.state import app_state
from flet_app.components.adaptive_nav import build_adaptive_layout
from flet_app.components.feature_tooltip import build_feature_tooltip
from flet_app.components.hover_effects import apply_hover_effects_to_button, apply_hover_effects_to_card


def fitness_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de integrações fitness."""

    dark = app_state.dark_mode

    # ── Strava connection ────────────────────────────────────────
    connected = [False]
    activities_col = ft.Column(spacing=8)

    def _connect_strava(e):
        try:
            from fitness_connectors import StravaConnector
            connector = StravaConnector(
                client_id="",
                client_secret="",
            )
            url = connector.authorize_url()
            if url:
                page.launch_url(url)
                page.open(ft.SnackBar(
                    ft.Text("Abra o navegador para autorizar o Strava."),
                    bgcolor=c("info", dark),
                ))
        except Exception as ex:
            page.open(ft.SnackBar(
                ft.Text(f"Configuração Strava necessária: {ex}"),
                bgcolor=c("warning", dark),
            ))

    def _load_activities(e):
        # Mostrar spinner enquanto carrega
        activities_col.controls.clear()
        activities_col.controls.append(
            ft.Row(
                [ft.ProgressRing(width=20, height=20, stroke_width=2), ft.Text("Carregando atividades…", size=13)],
                spacing=8, alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        page.update()
        try:
            from fitness_connectors import StravaConnector
            connector = StravaConnector(
                client_id="",
                client_secret="",
            )
            if not connector.is_connected():
                page.open(ft.SnackBar(ft.Text("Conecte o Strava primeiro."), bgcolor=c("warning", dark)))
                return
            acts = connector.get_activities(limit=20)
            activities_col.controls.clear()
            for a in acts:
                activity_card = apply_hover_effects_to_card(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(
                                ft.Icons.DIRECTIONS_RUN if "run" in (a.sport_type or "").lower() else ft.Icons.DIRECTIONS_BIKE if "ride" in (a.sport_type or "").lower() else ft.Icons.POOL,
                                size=20, color=c("primary", dark),
                            ),
                            ft.Column([
                                ft.Text(a.name or "Atividade", size=14, weight=ft.FontWeight.W_600),
                                ft.Text(f"{a.sport_type} · {a.distance_km:.1f} km · {a.duration_min:.0f} min", size=12, color=c("text_secondary", dark)),
                            ], spacing=2, expand=True),
                            ft.Text(a.date[:10] if a.date else "", size=11, color=c("text_disabled", dark)),
                        ], spacing=8),
                        bgcolor=c("bg_card", dark),
                        border_radius=10,
                        padding=12,
                    ),
                    scale_ratio=1.02,
                    shadow_level="md",
                    dark=dark,
                )
                activities_col.controls.append(activity_card)
            if not acts:
                activities_col.controls.append(ft.Text("Nenhuma atividade encontrada.", color=c("text_secondary", dark)))
            page.update()
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor=c("error", dark)))

    # ── UI ───────────────────────────────────────────────────────
    strava_section = apply_hover_effects_to_card(
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/c/cb/Strava_Logo.svg", width=100, height=30, fit=ft.ImageFit.CONTAIN)
                    if False else ft.Row([ft.Icon(ft.Icons.FLASH_ON, size=20, color="#FC4C02"), ft.Text("Strava", size=18, weight=ft.FontWeight.BOLD)], spacing=SPACING["sm"]),
                    apply_hover_effects_to_button(
                        ft.ElevatedButton("Conectar", icon=ft.Icons.LINK, on_click=_connect_strava),
                        scale_ratio=1.05,
                        duration_ms=150,
                        dark=dark,
                    ),
                    apply_hover_effects_to_button(
                        ft.OutlinedButton("Carregar Atividades", icon=ft.Icons.REFRESH, on_click=_load_activities),
                        scale_ratio=1.05,
                        duration_ms=150,
                        dark=dark,
                    ),
                ], spacing=12),
                ft.Text(
                    "Configure client_id e client_secret em fitness_connectors.py para usar a integração Strava.",
                    size=12, color=c("text_secondary", dark),
                ),
            ], spacing=8),
            padding=16,
            bgcolor=c("bg_card", dark),
            border_radius=12,
        ),
        scale_ratio=1.02,
        shadow_level="md",
        dark=dark,
    )

    garmin_section = apply_hover_effects_to_card(
        ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.WATCH, size=20, color=c("primary", dark)), ft.Text("Garmin", size=18, weight=ft.FontWeight.BOLD)], spacing=SPACING["sm"]),
                ft.Text("Integração Garmin Connect em breve.", size=13, color=c("text_secondary", dark)),
            ], spacing=8),
            padding=16,
            bgcolor=c("bg_card", dark),
            border_radius=12,
        ),
        scale_ratio=1.02,
        shadow_level="md",
        dark=dark,
    )

    return build_adaptive_layout(
        page=page,
        selected_index=3,
        body=ft.Container(
            content=ft.Column(
                [
                    ft.Row([ft.Icon(ft.Icons.WATCH, size=22, color=c("primary", dark)), ft.Text("Fitness & Conectores", size=20, weight=ft.FontWeight.BOLD)], spacing=SPACING["sm"]),
                    build_feature_tooltip("fitness", t("tooltip_fitness"), page, dark),
                    strava_section,
                    garmin_section,
                    ft.Divider(height=16),
                    ft.Text("Atividades Importadas", size=16, weight=ft.FontWeight.W_600),
                    activities_col,
                ],
                spacing=SPACING["md"],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=ft.padding.all(SPACING["md"]),
            expand=True,
        ),
        dark=dark,
    )
