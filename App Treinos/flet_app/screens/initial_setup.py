"""
Ecrã de Configuração Inicial
==============================

Exibido no primeiro arranque quando não existem utilizadores na BD.
Solicita ao profissional que crie a conta de administrador.
"""

import flet as ft
from i18n import t
from flet_app.theme import c


def initial_setup_view(page: ft.Page, route: str) -> ft.View:
    """View para criação do administrador inicial."""

    from flet_app.state import app_state
    dark = app_state.dark_mode

    error_text = ft.Text("", color=ft.Colors.RED_400, size=13)
    success_text = ft.Text("", color=ft.Colors.GREEN_400, size=13)

    cpf_field = ft.TextField(
        label="CPF (11 dígitos)", max_length=11, width=320,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    cref_field = ft.TextField(
        label="CREF", max_length=20, width=320,
    )
    nome_field = ft.TextField(
        label="Nome completo", width=320,
    )
    email_field = ft.TextField(
        label="Email (opcional)", width=320,
        keyboard_type=ft.KeyboardType.EMAIL,
    )
    senha_field = ft.TextField(
        label="Senha (mínimo 6 caracteres)", width=320,
        password=True, can_reveal_password=True,
    )
    senha_confirm_field = ft.TextField(
        label="Confirmar senha", width=320,
        password=True, can_reveal_password=True,
    )

    def _criar_admin(e):
        error_text.value = ""
        success_text.value = ""

        cpf = cpf_field.value.strip() if cpf_field.value else ""
        cref = cref_field.value.strip() if cref_field.value else ""
        nome = nome_field.value.strip() if nome_field.value else ""
        email = email_field.value.strip() if email_field.value else ""
        senha = senha_field.value or ""
        senha_confirm = senha_confirm_field.value or ""

        if len(cpf) != 11 or not cpf.isdigit():
            error_text.value = "CPF deve conter exatamente 11 dígitos."
            page.update()
            return
        if not cref:
            error_text.value = "CREF é obrigatório."
            page.update()
            return
        if len(nome) < 2:
            error_text.value = "Nome deve ter no mínimo 2 caracteres."
            page.update()
            return
        if len(senha) < 6:
            error_text.value = "Senha deve ter no mínimo 6 caracteres."
            page.update()
            return
        if senha != senha_confirm:
            error_text.value = "As senhas não coincidem."
            page.update()
            return

        ok, msg = app_state.db.criar_admin_inicial(cpf, cref, nome, senha, email)
        if ok:
            success_text.value = "Administrador criado com sucesso!"
            page.update()
            page.go("/login")
        else:
            error_text.value = msg
            page.update()

    btn_criar = ft.ElevatedButton(
        "Criar Administrador",
        icon=ft.Icons.ADMIN_PANEL_SETTINGS,
        on_click=_criar_admin,
        width=320,
        height=48,
    )

    content = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.SETTINGS_SUGGEST, size=60, color=c("accent", dark)),
                ft.Text(
                    "Configuração Inicial",
                    size=28, weight=ft.FontWeight.BOLD,
                    color=c("text", dark),
                ),
                ft.Text(
                    "Crie a conta de administrador para começar a usar o App Treinos.",
                    size=14, color=c("text_secondary", dark),
                    text_align=ft.TextAlign.CENTER, width=340,
                ),
                ft.Container(height=8),
                cpf_field,
                cref_field,
                nome_field,
                email_field,
                senha_field,
                senha_confirm_field,
                ft.Container(height=4),
                error_text,
                success_text,
                btn_criar,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True,
        bgcolor=c("bg_primary", dark),
        padding=32,
    )

    return ft.View(route="/initial-setup", controls=[content])
