"""
Adaptive Navigation — Sidebar (desktop) / Bottom Nav (mobile)
==============================================================

Sidebar persistente em larguras ≥ 768px, NavigationBar inferior
para janelas menores. Transição automática ao redimensionar.
"""

import flet as ft
from i18n import t
from flet_app.theme import c, RADIUS, SPACING


# ── Destinos de navegação ─────────────────────────────────────

NAV_ITEMS = [
    {"route": "/dashboard", "icon": ft.Icons.HOME_OUTLINED, "icon_selected": ft.Icons.HOME, "label_key": "nav_dashboard"},
    {"route": "/progress", "icon": ft.Icons.INSIGHTS_OUTLINED, "icon_selected": ft.Icons.INSIGHTS, "label_key": "nav_stats"},
    {"route": "/templates", "icon": ft.Icons.LIBRARY_BOOKS_OUTLINED, "icon_selected": ft.Icons.LIBRARY_BOOKS, "label_key": "nav_templates"},
    {"route": "/fitness", "icon": ft.Icons.WATCH_OUTLINED, "icon_selected": ft.Icons.WATCH, "label_key": "nav_fitness"},
    {"route": "/config", "icon": ft.Icons.SETTINGS_OUTLINED, "icon_selected": ft.Icons.SETTINGS, "label_key": "nav_config"},
    {"route": "/help", "icon": ft.Icons.HELP_OUTLINE, "icon_selected": ft.Icons.HELP, "label_key": "nav_help"},
]

DESKTOP_BREAKPOINT = 768


def _build_sidebar(page: ft.Page, selected_index: int, dark: bool) -> ft.Container:
    """Sidebar lateral para desktop (≥ 768px)."""

    def _go(route):
        def handler(_):
            page.go(route)
        return handler

    nav_items = []
    for i, item in enumerate(NAV_ITEMS):
        is_selected = i == selected_index
        icon = item["icon_selected"] if is_selected else item["icon"]
        icon_color = c("primary", dark) if is_selected else c("text_secondary", dark)
        text_color = c("primary", dark) if is_selected else c("text_secondary", dark)
        bg = c("bg_tertiary", dark) if is_selected else None

        nav_items.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(icon, size=22, color=icon_color),
                        ft.Text(t(item["label_key"]), size=14, weight=ft.FontWeight.W_500 if is_selected else ft.FontWeight.NORMAL, color=text_color),
                    ],
                    spacing=SPACING["md"],
                ),
                padding=ft.padding.symmetric(horizontal=SPACING["md"], vertical=SPACING["sm"] + 2),
                border_radius=RADIUS["md"],
                bgcolor=bg,
                on_click=_go(item["route"]),
                ink=True,
                animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            )
        )

    # Logo / brand
    brand = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.DIRECTIONS_RUN, size=28, color=c("primary", dark)),
                ft.Text("Velix", size=18, weight=ft.FontWeight.BOLD, color=c("text_primary", dark)),
            ],
            spacing=SPACING["sm"],
        ),
        padding=ft.padding.only(left=SPACING["md"], top=SPACING["lg"], bottom=SPACING["xl"]),
    )

    sidebar = ft.Container(
        content=ft.Column(
            [brand] + nav_items,
            spacing=SPACING["xs"],
        ),
        width=220,
        bgcolor=c("bg_card", dark),
        border=ft.border.only(right=ft.BorderSide(1, c("border_light", dark))),
        padding=ft.padding.only(left=SPACING["sm"], right=SPACING["sm"], top=0, bottom=SPACING["md"]),
        expand=True,
    )
    return sidebar


def _build_bottom_nav(page: ft.Page, selected_index: int) -> ft.NavigationBar:
    """Bottom NavigationBar para mobile (< 768px)."""

    def _on_change(e):
        idx = e.control.selected_index
        page.go(NAV_ITEMS[idx]["route"])

    return ft.NavigationBar(
        selected_index=selected_index,
        on_change=_on_change,
        destinations=[
            ft.NavigationBarDestination(
                icon=item["icon"],
                selected_icon=item["icon_selected"],
                label=t(item["label_key"]),
            )
            for item in NAV_ITEMS
        ],
    )


def build_adaptive_layout(
    page: ft.Page,
    selected_index: int,
    body: ft.Control,
    dark: bool,
    fab: ft.FloatingActionButton = None,
    appbar: ft.AppBar = None,
) -> ft.View:
    """
    Constrói View com navegação adaptativa.

    Em desktop (≥ 768px): sidebar esquerda + conteúdo à direita.
    Em mobile (< 768px): conteúdo + bottom navigation bar.
    """
    route = NAV_ITEMS[selected_index]["route"]
    page_width = page.window.width or 800

    if page_width >= DESKTOP_BREAKPOINT:
        sidebar = _build_sidebar(page, selected_index, dark)
        layout = ft.Row(
            [sidebar, ft.VerticalDivider(width=0), ft.Container(content=body, expand=True)],
            spacing=0,
            expand=True,
        )
        return ft.View(
            route=route,
            controls=[layout],
            floating_action_button=fab,
            appbar=appbar,
            bgcolor=c("bg_secondary", dark),
            padding=0,
        )
    else:
        return ft.View(
            route=route,
            controls=[body] if not appbar else [body],
            navigation_bar=_build_bottom_nav(page, selected_index),
            floating_action_button=fab,
            appbar=appbar,
            bgcolor=c("bg_secondary", dark),
        )
