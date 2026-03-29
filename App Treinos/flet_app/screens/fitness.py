"""
Fitness — Conectores de fitness (Strava, Garmin)
================================================

Ecrã com conexão OAuth via Strava e lista de atividades importadas.
"""

import flet as ft
from flet_app.theme import c
from flet_app.state import app_state
from flet_app.components.nav_bar import build_nav_bar
from flet_app.components.feature_tooltip import build_feature_tooltip


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
                    ft.Text("🔗 Abra o navegador para autorizar o Strava."),
                    bgcolor=c("info", dark),
                ))
        except Exception as ex:
            page.open(ft.SnackBar(
                ft.Text(f"⚠️ Configuração Strava necessária: {ex}"),
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
                activities_col.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text("🏃" if "run" in (a.sport_type or "").lower() else "🚴" if "ride" in (a.sport_type or "").lower() else "🏊", size=20),
                            ft.Column([
                                ft.Text(a.name or "Atividade", size=14, weight=ft.FontWeight.W_600),
                                ft.Text(f"{a.sport_type} · {a.distance_km:.1f} km · {a.duration_min:.0f} min", size=12, color=c("text_secondary", dark)),
                            ], spacing=2, expand=True),
                            ft.Text(a.date[:10] if a.date else "", size=11, color=c("text_disabled", dark)),
                        ], spacing=8),
                        bgcolor=c("bg_card", dark),
                        border_radius=10,
                        padding=12,
                    )
                )
            if not acts:
                activities_col.controls.append(ft.Text("Nenhuma atividade encontrada.", color=c("text_secondary", dark)))
            page.update()
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor=c("error", dark)))

    # ── UI ───────────────────────────────────────────────────────
    strava_section = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/c/cb/Strava_Logo.svg", width=100, height=30, fit=ft.ImageFit.CONTAIN)
                if False else ft.Text("🔶 Strava", size=18, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Conectar", icon=ft.Icons.LINK, on_click=_connect_strava),
                ft.OutlinedButton("Carregar Atividades", icon=ft.Icons.REFRESH, on_click=_load_activities),
            ], spacing=12),
            ft.Text(
                "Configure client_id e client_secret em fitness_connectors.py para usar a integração Strava.",
                size=12, color=c("text_secondary", dark),
            ),
        ], spacing=8),
        padding=16,
        bgcolor=c("bg_card", dark),
        border_radius=12,
    )

    garmin_section = ft.Container(
        content=ft.Column([
            ft.Text("⌚ Garmin", size=18, weight=ft.FontWeight.BOLD),
            ft.Text("Integração Garmin Connect em breve.", size=13, color=c("text_secondary", dark)),
        ], spacing=8),
        padding=16,
        bgcolor=c("bg_card", dark),
        border_radius=12,
    )

    return ft.View(
        route="/fitness",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("⌚ Fitness & Conectores", size=20, weight=ft.FontWeight.BOLD),
                        build_feature_tooltip("fitness", t("tooltip_fitness"), page, dark),
                        strava_section,
                        garmin_section,
                        ft.Divider(height=16),
                        ft.Text("Atividades Importadas", size=16, weight=ft.FontWeight.W_600),
                        activities_col,
                    ],
                    spacing=12,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                padding=ft.padding.all(16),
                expand=True,
            )
        ],
        navigation_bar=build_nav_bar(page, selected_index=2),
        bgcolor=c("bg_secondary", dark),
    )
