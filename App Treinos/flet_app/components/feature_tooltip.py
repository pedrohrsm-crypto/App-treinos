"""
Feature Tooltip — Dica contextual de primeiro uso
===================================================

Balão informativo exibido apenas na primeira visita
a cada tela. Dispensado com toque, registra em preferências
para não reaparecer.
"""

import flet as ft
from flet_app.theme import c
from flet_app.state import app_state


def build_feature_tooltip(
    screen_key: str,
    message: str,
    page: ft.Page,
    dark: bool = False,
) -> ft.Container:
    """
    Retorna um Container com dica contextual.
    Se o tooltip para *screen_key* já foi visto, retorna Container vazio.

    Parâmetros:
        screen_key: Identificador único da tela (ex: "dashboard").
        message: Texto da dica.
        page: Instância da página Flet para atualizar UI.
        dark: Modo escuro ativo.
    """
    # Verificar se já foi visto
    data = app_state._read_prefs_file()
    seen = data.get("_seen_tooltips", [])
    if screen_key in seen:
        return ft.Container(visible=False)

    tooltip_container = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color=c("primary", dark), size=20),
                ft.Text(message, size=13, color=c("text_primary", dark), expand=True),
                ft.IconButton(
                    ft.Icons.CLOSE, icon_size=22,
                    icon_color=c("text_secondary", dark),
                    on_click=lambda _: _dismiss(),
                ),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        border_radius=10,
        bgcolor=c("bg_tertiary", dark),
        border=ft.border.all(1, c("primary", dark)),
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
    )

    def _dismiss():
        # Marcar como visto
        file_data = app_state._read_prefs_file()
        seen_list = file_data.get("_seen_tooltips", [])
        if screen_key not in seen_list:
            seen_list.append(screen_key)
        file_data["_seen_tooltips"] = seen_list
        app_state._write_prefs_file(file_data)

        # Animar saída
        tooltip_container.opacity = 0
        page.update()

    return tooltip_container
