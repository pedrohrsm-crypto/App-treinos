"""
Admin Panel — Gestão de utilizadores
======================================

DataTable com CRUD de utilizadores (listar, editar, desativar).
Dados carregados assincronamente com spinner.
"""

import asyncio
import flet as ft
from flet_app.theme import c
from flet_app.state import app_state
from flet_app.components.loading_overlay import build_loading


def admin_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de administração."""

    dark = app_state.dark_mode

    if not app_state.is_admin:
        return ft.View(route="/admin", controls=[ft.Text("Acesso negado.")])

    body = ft.Container(content=build_loading("Carregando utilizadores…", dark), expand=True)

    def _go_back(_):
        page.go("/config")

    def _deactivate(e):
        uid = e.control.data
        if uid:
            app_state.db.deletar_usuario(uid)
            page.go("/admin")  # reload

    async def _load_data():
        await asyncio.sleep(0.01)

        users = app_state.db.listar_usuarios()
        rows = []
        for u in users:
            status = "Ativo" if u.get("ativo", 1) else "Inativo"
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(u.get("id", "")))),
                        ft.DataCell(ft.Text(u.get("nome", ""))),
                        ft.DataCell(ft.Text(u.get("cpf", ""))),
                        ft.DataCell(ft.Text(u.get("cref", ""))),
                        ft.DataCell(ft.Text(u.get("email", "") or "—")),
                        ft.DataCell(ft.Text(status)),
                        ft.DataCell(
                            ft.IconButton(
                                ft.Icons.BLOCK, tooltip="Desativar",
                                icon_color=c("error", dark), data=u.get("id"),
                                on_click=_deactivate,
                            )
                        ),
                    ],
                )
            )

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("CPF")),
                ft.DataColumn(ft.Text("CREF")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Ação")),
            ],
            rows=rows,
        )

        body.content = ft.Column(
            [
                ft.Row(
                    [ft.IconButton(ft.Icons.ARROW_BACK, on_click=_go_back),
                     ft.Row([ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, size=22, color=c("primary", dark)), ft.Text("Painel de Administração", size=22, weight=ft.FontWeight.BOLD)], spacing=8)],
                ),
                ft.Divider(),
                ft.Container(content=table, expand=True),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
        page.update()

    page.run_task(_load_data)

    return ft.View(
        route="/admin",
        controls=[ft.Container(content=body, padding=20, expand=True)],
    )
