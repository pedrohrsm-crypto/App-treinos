"""
Loading Overlay — Componente reutilizável de carregamento
=========================================================

ProgressRing com texto de status, usado como placeholder
enquanto dados assíncronos carregam.
"""

import flet as ft
from flet_app.theme import c


def build_loading(message: str = "Carregando…", dark: bool = False) -> ft.Container:
    """Retorna um Container centralizado com spinner + mensagem."""
    return ft.Container(
        content=ft.Column(
            [
                ft.ProgressRing(width=40, height=40, stroke_width=3, color=c("primary", dark)),
                ft.Text(message, size=14, color=c("text_secondary", dark)),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True,
    )
