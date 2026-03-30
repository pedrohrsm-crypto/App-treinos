"""
Athlete Card — Hero card de atleta para o Dashboard
=====================================================

Mostra avatar, nome, desporto, progresso semanal e status.
"""

import flet as ft
from flet_app.theme import c, SPORT_COLORS, SPORT_ICONS, RADIUS, SPACING, card_shadow
from typing import Dict, Callable, Optional


def _initials(name: str) -> str:
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper() if name else "??"


def _sport_icon(sport: str) -> ft.Icon:
    _map = {
        "Corrida": ft.Icons.DIRECTIONS_RUN,
        "Ciclismo": ft.Icons.DIRECTIONS_BIKE,
        "Natação": ft.Icons.POOL,
        "Triathlon": ft.Icons.EMOJI_EVENTS,
        "Duathlon (Natação+Corrida)": ft.Icons.POOL,
        "Duathlon (Ciclismo+Corrida)": ft.Icons.DIRECTIONS_BIKE,
    }
    return ft.Icon(_map.get(sport, ft.Icons.FITNESS_CENTER), size=14)


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
    status_color = c("success", dark) if status == "active" else c("text_disabled", dark)

    avatar = ft.CircleAvatar(
        content=ft.Text(_initials(name), size=18, weight=ft.FontWeight.BOLD, color=c("text_light", dark)),
        bgcolor=sport_color,
        radius=26,
    )

    card_content = ft.Column(
        [
            ft.Row(
                [avatar, ft.Column(
                    [
                        ft.Text(name, size=16, weight=ft.FontWeight.W_600, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Row([_sport_icon(sport), ft.Text(f"{sport} · {distance}", size=12, color=c("text_secondary", dark))], spacing=4),
                    ],
                    spacing=2,
                    expand=True,
                )],
                spacing=SPACING["md"],
            ),
            ft.Divider(height=1, color=c("border_light", dark)),
            ft.Row(
                [
                    ft.Row([
                        ft.Icon(ft.Icons.CIRCLE, size=10, color=status_color),
                        ft.Text(f"S{cur_week}/{total}", size=13, weight=ft.FontWeight.W_500),
                    ], spacing=4),
                    ft.Text(f"{len(summary['plans'])} plano(s)", size=12, color=c("text_secondary", dark)),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.ProgressBar(value=progress, color=sport_color, bgcolor=c("border_light", dark), height=6),
        ],
        spacing=SPACING["sm"],
    )

    shadow_ref = [card_shadow(dark, "md")]

    def _on_hover(e):
        if e.data == "true":
            container.shadow = card_shadow(dark, "lg")
            container.scale = 1.01
        else:
            container.shadow = card_shadow(dark, "md")
            container.scale = 1.0
        container.update()

    container = ft.Container(
        content=card_content,
        padding=SPACING["md"],
        border_radius=RADIUS["lg"],
        bgcolor=c("bg_card", dark),
        shadow=card_shadow(dark, "md"),
        on_click=on_click,
        on_hover=_on_hover,
        ink=True,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        width=360,
    )
    return container
