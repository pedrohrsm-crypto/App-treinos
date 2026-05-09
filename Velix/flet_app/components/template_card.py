"""
Template Card — Card de template de treino reutilizável
========================================================

Mostra nome, desporto, tipo, duração e zona com botão "Usar".
"""

import flet as ft
from flet_app.theme import c, get_zone_color, SPORT_COLORS, RADIUS, SPACING, card_shadow


def build_template_card(
    template: dict,
    on_use=None,
    on_delete=None,
    dark: bool = False,
) -> ft.Container:
    """Constrói um card para um template de treino."""

    name = template.get("name", "Sem nome")
    sport = template.get("sport", "")
    tipo = template.get("type", "")
    zone = template.get("zone", "")
    duration = template.get("duration", "")
    description = template.get("description", "")
    template_id = template.get("id", "")

    zone_bg_color, _ = get_zone_color(zone, dark)
    sport_color = SPORT_COLORS.get(sport, c("primary", dark))

    return ft.Container(
        content=ft.Row(
            [
                # Barra lateral colorida pela zona (WCAG AAA compliant)
                ft.Container(width=4, height=70, bgcolor=zone_bg_color, border_radius=2),
                ft.Column(
                    [
                        ft.Text(name, size=14, weight=ft.FontWeight.W_600),
                        ft.Row([
                            ft.Container(
                                content=ft.Text(sport, size=10, color=c("text_light", dark)),
                                bgcolor=sport_color,
                                border_radius=RADIUS["sm"],
                                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                            ),
                            ft.Text(f"{tipo} · {duration}", size=11, color=c("text_secondary", dark)),
                        ], spacing=6),
                        ft.Text(description, size=11, color=c("text_secondary", dark), max_lines=1),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.Column(
                    [
                        ft.IconButton(
                            ft.Icons.PLAY_ARROW,
                            icon_size=20,
                            tooltip="Usar template",
                            data=template_id,
                            on_click=on_use,
                        ) if on_use else ft.Container(),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            icon_size=16,
                            tooltip="Apagar",
                            data=template_id,
                            on_click=on_delete,
                        ) if on_delete else ft.Container(),
                    ],
                    spacing=0,
                ),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=c("bg_card", dark),
        border_radius=RADIUS["md"],
        padding=SPACING["md"],
        shadow=card_shadow(dark, "sm"),
    )
