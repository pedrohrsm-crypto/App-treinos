"""
Athlete Card — Hero card de atleta para o Dashboard
=====================================================

Mostra avatar, nome, desporto, progresso semanal e status.
"""

import flet as ft
from flet_app.theme import c, SPORT_COLORS
from typing import Dict, Callable, Optional


def _initials(name: str) -> str:
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper() if name else "??"


def _sport_emoji(sport: str) -> str:
    _map = {
        "Corrida": "🏃",
        "Ciclismo": "🚴",
        "Natação": "🏊",
        "Triathlon": "🏅",
        "Duathlon (Natação+Corrida)": "🏊🏃",
        "Duathlon (Ciclismo+Corrida)": "🚴🏃",
    }
    return _map.get(sport, "🏋️")


def build_athlete_card(
    summary: Dict,
    on_click: Optional[Callable] = None,
    dark: bool = False,
) -> ft.Container:
    """
    Constrói hero card para um atleta.

    Args:
        summary: dict de get_athletes_summary() com keys:
            athlete_name, athlete_data, latest_sport, total_weeks,
            current_week, status, plans
        on_click: callback ao clicar no card
        dark: modo escuro ativo
    """
    name = summary["athlete_name"]
    sport = summary["latest_sport"]
    distance = summary["plans"][0].distance if summary["plans"] else ""
    status = summary["status"]
    cur_week = summary["current_week"]
    total = summary["plans"][0].weeks if summary["plans"] else 1
    progress = min(cur_week / max(total, 1), 1.0)

    sport_color = SPORT_COLORS.get(sport, c("primary", dark))
    status_icon = "🟢" if status == "active" else "⚪"

    avatar = ft.CircleAvatar(
        content=ft.Text(_initials(name), size=18, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
        bgcolor=sport_color,
        radius=26,
    )

    card_content = ft.Column(
        [
            ft.Row(
                [avatar, ft.Column(
                    [
                        ft.Text(name, size=16, weight=ft.FontWeight.W_600, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text(f"{_sport_emoji(sport)} {sport} · {distance}", size=12, color=c("text_secondary", dark)),
                    ],
                    spacing=2,
                    expand=True,
                )],
                spacing=12,
            ),
            ft.Divider(height=1, color=c("border_light", dark)),
            ft.Row(
                [
                    ft.Text(f"{status_icon} S{cur_week}/{total}", size=13, weight=ft.FontWeight.W_500),
                    ft.Text(f"{len(summary['plans'])} plano(s)", size=12, color=c("text_secondary", dark)),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.ProgressBar(value=progress, color=sport_color, bgcolor=c("border_light", dark), height=6),
        ],
        spacing=8,
    )

    return ft.Container(
        content=card_content,
        padding=16,
        border_radius=16,
        bgcolor=c("bg_card", dark),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=c("shadow", dark), offset=ft.Offset(0, 2)),
        on_click=on_click,
        ink=True,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        width=320,
    )
