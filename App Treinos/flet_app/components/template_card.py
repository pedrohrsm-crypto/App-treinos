"""
Template Card — Card de template de treino reutilizável
========================================================

Mostra nome, desporto, tipo, duração e zona com botão "Usar".
"""

import flet as ft
from flet_app.theme import c, SPORT_COLORS


ZONE_COLORS = {
    "Z1 - Recuperação": "#68c2a6",
    "Z2 - Aeróbico": "#6885c2",
    "Z3 - Tempo": "#c27968",
    "Z4 - Limiar": "#c26868",
    "Z5 - VO2max": "#7968c2",
}


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

    zone_color = ZONE_COLORS.get(zone, c("primary", dark))
    sport_color = SPORT_COLORS.get(sport, c("primary", dark))

    return ft.Container(
        content=ft.Row(
            [
                # Barra lateral colorida pela zona
                ft.Container(width=4, height=70, bgcolor=zone_color, border_radius=2),
                ft.Column(
                    [
                        ft.Text(name, size=14, weight=ft.FontWeight.W_600),
                        ft.Row([
                            ft.Container(
                                content=ft.Text(sport, size=10, color="#FFF"),
                                bgcolor=sport_color,
                                border_radius=4,
                                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                            ),
                            ft.Text(f"{tipo} · {duration}", size=11, color=c("text_secondary", dark)),
                        ], spacing=6),
                        ft.Text(description, size=11, color=c("text_disabled", dark), max_lines=1),
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
        border_radius=10,
        padding=12,
        shadow=ft.BoxShadow(blur_radius=4, color=c("shadow", dark)),
    )
