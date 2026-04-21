"""
Smartwatch Connection Screen — Conectar dispositivos wearables
===============================================================

Permite conexão com smartwatches e smartbands (Garmin, Apple Watch, Fitbit, Samsung).
"""

import flet as ft
from i18n import t
from flet_app.theme import c, RADIUS, SPACING, card_shadow
from flet_app.state import app_state


def smartwatch_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de conexão com smartwatch."""

    dark = app_state.dark_mode

    # ── Estado ───────────────────────────────────────────────────
    devices_status = {
        "garmin_watch": {"connected": False, "model": ""},
        "apple_watch": {"connected": False, "model": ""},
        "fitbit": {"connected": False, "model": ""},
        "samsung": {"connected": False, "model": ""},
    }

    def build_device_card(device_type: str, device_name: str, icon: str) -> ft.Container:
        """Constrói um card para um tipo de dispositivo."""
        is_connected = devices_status[device_type]["connected"]
        status_color = c("success", dark) if is_connected else c("text_secondary", dark)
        status_text = "Conectado" if is_connected else "Não conectado"

        return ft.Container(
            content=ft.Column(
                [
                    # Ícone + Nome do dispositivo
                    ft.Row(
                        [
                            ft.Icon(icon, size=40, color=c("primary", dark)),
                            ft.Column(
                                [
                                    ft.Text(device_name, size=16, weight=ft.FontWeight.W_600),
                                    ft.Text(
                                        status_text,
                                        size=12,
                                        color=status_color,
                                    ),
                                ],
                                spacing=0,
                            ),
                        ],
                        spacing=12,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Divider(height=12, color=ft.Colors.TRANSPARENT),

                    # Botões de ação
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Conectar" if not is_connected else "Desconectar",
                                icon=ft.Icons.LINK if not is_connected else ft.Icons.LINK_OFF,
                                on_click=lambda e, dt=device_type: _toggle_connection(e, dt),
                                bgcolor=c("primary", dark) if not is_connected else c("error", dark),
                                color=c("text_light", dark),
                                width=150,
                            ),
                            ft.IconButton(
                                ft.Icons.SYNC,
                                tooltip="Sincronizar agora",
                                on_click=lambda e, dt=device_type: _sync_device(e, dt),
                                disabled=not is_connected,
                            ),
                        ],
                        spacing=8,
                        expand=True,
                    ),
                ],
                spacing=8,
            ),
            padding=16,
            bgcolor=c("bg_card", dark),
            border_radius=RADIUS["md"],
            shadow=card_shadow(dark, "sm"),
        )

    def _toggle_connection(e, device_type: str):
        """Alterna conexão com o dispositivo."""
        status = devices_status[device_type]
        status["connected"] = not status["connected"]

        if status["connected"]:
            snack_msg = f"{_get_device_name(device_type)} conectado com sucesso!"
            snack_color = c("success", dark)
        else:
            snack_msg = f"{_get_device_name(device_type)} desconectado"
            snack_color = c("warning", dark)

        page.open(
            ft.SnackBar(
                ft.Text(snack_msg),
                bgcolor=snack_color,
            )
        )
        page.update()

    def _sync_device(e, device_type: str):
        """Sincroniza atividades do dispositivo."""
        device_name = _get_device_name(device_type)
        page.open(
            ft.SnackBar(
                ft.Text(f"Sincronizando {device_name}..."),
                bgcolor=c("info", dark),
            )
        )
        # Simular sincronização
        # TODO: Integrar com fitness_connectors para sincronização real
        import threading
        import time

        def _sync():
            time.sleep(2)
            page.open(
                ft.SnackBar(
                    ft.Text(f"{device_name} sincronizado! 5 atividades importadas."),
                    bgcolor=c("success", dark),
                )
            )
            page.update()

        threading.Thread(target=_sync, daemon=True).start()

    def _get_device_name(device_type: str) -> str:
        """Retorna nome amigável do dispositivo."""
        names = {
            "garmin_watch": "Garmin Watch/Edge",
            "apple_watch": "Apple Watch",
            "fitbit": "Fitbit",
            "samsung": "Samsung Galaxy Watch",
        }
        return names.get(device_type, device_type)

    def _go_back(_):
        """Retorna à tela anterior."""
        page.go("/fitness")

    # ── Layout principal ─────────────────────────────────────────
    content = ft.Column(
        [
            # ── Header ──────────────────────────────────────────
            ft.Row(
                [
                    ft.IconButton(ft.Icons.ARROW_BACK, on_click=_go_back),
                    ft.Text(t("smartwatch_title"), size=22, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Text(
                t("smartwatch_subtitle"),
                size=13,
                color=c("text_secondary", dark),
            ),
            ft.Divider(height=16, color=ft.Colors.TRANSPARENT),

            # ── Cartões de dispositivos ─────────────────────────
            build_device_card("garmin_watch", "Garmin Watch / Edge", ft.Icons.DEVICES),
            build_device_card("apple_watch", "Apple Watch", ft.Icons.WATCH),
            build_device_card("fitbit", "Fitbit", ft.Icons.FITNESS_CENTER),
            build_device_card("samsung", "Samsung Galaxy Watch", ft.Icons.DEVICES),

            ft.Divider(height=16, color=ft.Colors.TRANSPARENT),

            # ── Seção de atividades sincronizadas ────────────────
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            t("smartwatch_recent_activities"),
                            size=14,
                            weight=ft.FontWeight.W_600,
                        ),
                        ft.Text(
                            "Nenhuma atividade sincronizada ainda.",
                            size=12,
                            color=c("text_secondary", dark),
                        ),
                    ],
                    spacing=8,
                ),
                padding=16,
                bgcolor=c("bg_card", dark),
                border_radius=RADIUS["md"],
                shadow=card_shadow(dark, "sm"),
            ),

            ft.Divider(height=8, color=ft.Colors.TRANSPARENT),

            # ── Informações de ajuda ────────────────────────────
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "💡 Dica",
                            size=12,
                            weight=ft.FontWeight.W_600,
                            color=c("info", dark),
                        ),
                        ft.Text(
                            "Depois de conectar um dispositivo, suas atividades serão sincronizadas automaticamente quando você abrir o App Treinos.",
                            size=11,
                            color=c("text_secondary", dark),
                            max_lines=3,
                        ),
                    ],
                    spacing=4,
                ),
                padding=12,
                bgcolor=c("bg_tertiary", dark),
                border_radius=RADIUS["sm"],
            ),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.View(
        route="/smartwatch",
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=c("bg_secondary", dark),
        padding=16,
        controls=[
            ft.Container(
                content=content,
                padding=0,
                expand=True,
            )
        ],
    )
