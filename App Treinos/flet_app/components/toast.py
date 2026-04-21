"""
Toast/Snackbar — Feedback visual de ações (sucesso, erro, loading)
===================================================================

Sistema centralizado de notificações que aparecem no rodapé da tela.
Reutilizável em toda a aplicação para confirmar ações.

Exemplo:
  from flet_app.components.toast import show_toast
  show_toast(page, "Treino salvo com sucesso ✓", "success")
  show_toast(page, "Erro ao conectar IA", "error")
  show_toast(page, "Salvando...", "loading")
"""

import flet as ft
import asyncio
from flet_app.theme import c


class Toast:
    """Gerenciador centralizado de toasts."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.active_toasts = []
        self._create_container()

    def _create_container(self):
        """Cria container para toasts no rodapé da página."""
        self.container = ft.Column(
            spacing=8,
            expand=False,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            visible=False,
        )
        # Adiciona ao overlay da página (rodapé)
        if not hasattr(self.page, "_toast_container"):
            self.page._toast_container = self.container

    def _get_colors(self, toast_type: str, dark: bool):
        """Retorna cores baseadas no tipo de toast."""
        colors = {
            "success": {"bg": c("success", dark), "text": "#FFFFFF", "icon": "✓"},
            "error": {"bg": c("error", dark), "text": "#FFFFFF", "icon": "✗"},
            "warning": {"bg": c("warning", dark), "text": "#000000", "icon": "⚠"},
            "loading": {"bg": c("primary", dark), "text": "#FFFFFF", "icon": "⟳"},
            "info": {"bg": c("primary", dark), "text": "#FFFFFF", "icon": "ℹ"},
        }
        return colors.get(toast_type, colors["info"])

    async def show(
        self,
        message: str,
        toast_type: str = "info",
        duration_ms: int = 3000,
        actionable: bool = False,
    ):
        """
        Exibe um toast.

        Args:
            message: Texto a exibir
            toast_type: "success", "error", "warning", "loading", "info"
            duration_ms: Tempo antes de desaparecer (0 = sem timeout)
            actionable: Se True, requer clique para fechar (para errors)
        """
        dark = getattr(self.page, "_app_dark_mode", False)
        colors = self._get_colors(toast_type, dark)

        # Criar toast
        close_btn = ft.IconButton(
            ft.Icons.CLOSE,
            icon_size=16,
            tooltip="Fechar",
        )

        toast_content = ft.Container(
            content=ft.Row(
                [
                    ft.Text(colors["icon"], size=20, color=colors["text"], weight="bold"),
                    ft.Text(
                        message,
                        size=14,
                        color=colors["text"],
                        expand=True,
                        selectable=False,
                    ),
                    close_btn if actionable else ft.Container(width=0),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=14),
            bgcolor=colors["bg"],
            border_radius=8,
            shadow=ft.BoxShadow(blur_radius=4, color="#00000020"),
            min_width=300,
            max_width=500,
        )

        def _remove_toast():
            if toast_content in self.active_toasts:
                self.active_toasts.remove(toast_content)
            self.container.controls.remove(toast_content)
            self.container.visible = len(self.active_toasts) > 0
            self.page.update()

        close_btn.on_click = lambda e: _remove_toast()

        # Adicionar e animar
        self.active_toasts.append(toast_content)
        self.container.controls.append(toast_content)
        self.container.visible = True
        self.page.update()

        # Auto-remover após timeout (a menos que actionable)
        if duration_ms > 0 and not actionable:
            await asyncio.sleep(duration_ms / 1000)
            _remove_toast()


def setup_toasts(page: ft.Page):
    """Inicializa sistema de toasts na página."""
    if not hasattr(page, "_toast_manager"):
        page._toast_manager = Toast(page)
        # Adicionar container ao overlay
        if hasattr(page, "overlay"):
            page.overlay.append(page._toast_manager.container)


async def show_toast(
    page: ft.Page,
    message: str,
    toast_type: str = "info",
    duration_ms: int = 3000,
):
    """
    Função helper para exibir toast.

    Uso:
        await show_toast(page, "Treino salvo ✓", "success")
        await show_toast(page, "Erro ao conectar", "error", 0)  # sem timeout
    """
    if not hasattr(page, "_toast_manager"):
        setup_toasts(page)

    await page._toast_manager.show(message, toast_type, duration_ms)
