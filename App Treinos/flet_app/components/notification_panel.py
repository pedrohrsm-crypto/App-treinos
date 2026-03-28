"""
Notification Panel — Painel de notificações (overlay)
=====================================================

Dropdown/overlay com lista de notificações pendentes,
ícone 🔔 com badge contador integrado ao nav_bar.
"""

import flet as ft
from flet_app.theme import c
from flet_app.state import app_state
from flet_app.services.notification_engine import get_pending_notifications


PRIORITY_COLORS = {
    1: "#c26868",  # alta → vermelho
    2: "#c27968",  # média → laranja
    3: "#6885c2",  # baixa → azul
}


def build_notification_icon(page: ft.Page, dark: bool = False) -> ft.Container:
    """
    Constrói ícone de sino com badge e abre painel ao clicar.

    Retorna um Container que pode ser adicionado ao header.
    """
    trainer = app_state.trainer_info()
    notifications = get_pending_notifications(trainer)
    count = len(notifications)

    badge_text = ft.Text(str(count) if count <= 9 else "9+", size=9, color="#FFF", weight=ft.FontWeight.BOLD)
    badge = ft.Container(
        content=badge_text,
        bgcolor=c("error", dark) if count > 0 else c("text_disabled", dark),
        border_radius=8,
        width=16,
        height=16,
        alignment=ft.Alignment.CENTER,
        visible=count > 0,
    )

    def _open_panel(e):
        _show_notification_panel(page, notifications, dark)

    icon_stack = ft.Stack(
        [
            ft.IconButton(ft.Icons.NOTIFICATIONS_OUTLINED, icon_size=24, on_click=_open_panel),
            ft.Container(badge, top=4, right=4),
        ],
        width=40,
        height=40,
    )

    return ft.Container(content=icon_stack)


def _show_notification_panel(page: ft.Page, notifications: list, dark: bool):
    """Abre BottomSheet com lista de notificações."""

    if not notifications:
        page.open(ft.SnackBar(ft.Text("🔔 Sem notificações pendentes."), bgcolor=c("info", dark)))
        return

    cards = []
    for n in notifications:
        pcolor = PRIORITY_COLORS.get(n.get("priority", 3), c("primary", dark))
        cards.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(width=4, height=50, bgcolor=pcolor, border_radius=2),
                        ft.Text(n.get("icon", "🔔"), size=24),
                        ft.Column(
                            [
                                ft.Text(n.get("title", ""), size=14, weight=ft.FontWeight.W_600),
                                ft.Text(n.get("detail", ""), size=12, color=c("text_secondary", dark)),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=c("bg_card", dark),
                border_radius=10,
                padding=10,
                margin=ft.margin.only(bottom=6),
            )
        )

    sheet = ft.BottomSheet(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row([
                        ft.Text("🔔 Notificações", size=16, weight=ft.FontWeight.BOLD, expand=True),
                        ft.Text(f"{len(notifications)} pendente(s)", size=13, color=c("text_secondary", dark)),
                    ]),
                    ft.Divider(),
                    *cards,
                ],
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            width=page.width or 400,
        ),
    )
    page.open(sheet)
    page.update()
