"""
Confirm Modal — Diálogo de confirmação antes de ações destrutivas
==================================================================

Usado para deletar, sair sem salvar, etc.

Exemplo:
  from flet_app.components.confirm_modal import show_confirm
  result = await show_confirm(
      page,
      title="Deletar treino?",
      message="Isto não pode ser desfeito.",
      confirm_text="Deletar",
      cancel_text="Cancelar",
  )
  if result:
      # Usuário confirmou
      await delete_training()
"""

import flet as ft
from flet_app.theme import c


async def show_confirm(
    page: ft.Page,
    title: str,
    message: str,
    confirm_text: str = "Confirmar",
    cancel_text: str = "Cancelar",
    danger: bool = True,
) -> bool:
    """
    Exibe modal de confirmação.

    Args:
        page: Página Flet
        title: Título do modal
        message: Mensagem a exibir
        confirm_text: Texto do botão de confirmar
        cancel_text: Texto do botão de cancelar
        danger: Se True, botão é vermelho (ações destrutivas)

    Returns:
        True se usuário clicou em confirmar, False caso contrário
    """

    dark = getattr(page, "_app_dark_mode", False)
    result = [None]

    # Botões
    btn_cancel = ft.TextButton(
        cancel_text,
        on_click=lambda e: _close_dialog(False),
    )

    btn_confirm = ft.TextButton(
        confirm_text,
        style=ft.ButtonStyle(
            color=c("error", dark) if danger else c("primary", dark),
        ),
        on_click=lambda e: _close_dialog(True),
    )

    def _close_dialog(confirmed: bool):
        result[0] = confirmed
        dlg.open = False
        page.update()

    # Modal
    dlg = ft.AlertDialog(
        title=ft.Text(title, size=20, weight="bold", color=c("text_primary", dark)),
        content=ft.Text(message, size=14, color=c("text_secondary", dark)),
        actions=[btn_cancel, btn_confirm],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = dlg
    dlg.open = True
    page.update()

    # Esperar até que usuário clique
    while result[0] is None:
        await ft.asyncio.sleep(0.1)

    return result[0]
