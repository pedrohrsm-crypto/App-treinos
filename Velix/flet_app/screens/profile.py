"""
Meu Perfil (My Profile) Screen — Gestão de dados do utilizador
================================================================

Permite visualizar e editar dados pessoais com encriptação de campos sensíveis.
"""

import flet as ft
from datetime import datetime
from i18n import t
from flet_app.theme import c, RADIUS, SPACING, card_shadow
from flet_app.state import app_state
from core.encryption_manager import EncryptionManager


def profile_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de perfil do utilizador."""

    dark = app_state.dark_mode
    edit_mode = [False]  # Toggle para edit mode

    # ── Campos de formulário ─────────────────────────────────────
    nome_field = ft.TextField(label="Nome", read_only=True, border_radius=12, filled=True)
    email_field = ft.TextField(label="Email", read_only=True, border_radius=12, filled=True)
    cref_field = ft.TextField(label="CREF", read_only=True, border_radius=12, filled=True)

    telefone_field = ft.TextField(
        label="Telefone (opcional)",
        prefix_icon=ft.Icons.PHONE,
        border_radius=12,
        filled=True,
        max_length=20,
    )
    data_nasc_field = ft.TextField(
        label="Data de Nascimento (DD/MM/AAAA)",
        prefix_icon=ft.Icons.CALENDAR_TODAY,
        border_radius=12,
        filled=True,
        max_length=10,
    )
    genero_field = ft.Dropdown(
        label="Gênero",
        options=[
            ft.dropdown.Option("Masculino"),
            ft.dropdown.Option("Feminino"),
            ft.dropdown.Option("Outro"),
            ft.dropdown.Option("Prefiro não informar"),
        ],
        border_radius=12,
        filled=True,
    )

    msg_text = ft.Text("", size=13, visible=False)

    # ── Carregar dados do utilizador ─────────────────────────────
    def _load_user_data():
        """Carrega dados do utilizador logado."""
        try:
            if app_state.user and app_state.user.get("id"):
                user_id = app_state.user["id"]
                nome_field.value = app_state.user.get("nome", "")
                email_field.value = app_state.user.get("email", "")
                cref_field.value = app_state.user.get("cref", "")

                # Carregar perfil (com desencriptação se necessário)
                profile = app_state.db.get_user_profile(user_id)
                if profile:
                    # Desencriptar dados sensíveis
                    if app_state.user.get("senha_hash"):
                        master_key = EncryptionManager.derive_master_key(
                            app_state.user["senha_hash"]
                        )
                        try:
                            if profile.get("encrypted_phone"):
                                telefone_field.value = EncryptionManager.decrypt_field(
                                    profile["encrypted_phone"], master_key
                                )
                            if profile.get("encrypted_cpf"):
                                # Mostrar CPF desencriptado apenas se necessário
                                pass
                        except Exception:
                            pass

                    data_nasc_field.value = profile.get("birth_date", "")
                    genero_field.value = profile.get("gender")

        except Exception as e:
            msg_text.value = f"Erro ao carregar perfil: {str(e)[:80]}"
            msg_text.color = c("error", dark)
            msg_text.visible = True

    # ── Toggle edit mode ─────────────────────────────────────────
    def _toggle_edit(_):
        """Alterna entre modo leitura e edição."""
        edit_mode[0] = not edit_mode[0]
        telefone_field.read_only = not edit_mode[0]
        data_nasc_field.read_only = not edit_mode[0]
        genero_field.disabled = not edit_mode[0]

        if edit_mode[0]:
            edit_btn.text = "Cancelar"
            edit_btn.icon = ft.Icons.CLOSE
            save_btn.visible = True
        else:
            edit_btn.text = "Editar"
            edit_btn.icon = ft.Icons.EDIT
            save_btn.visible = False
            # Recarregar dados ao cancelar
            _load_user_data()

        page.update()

    # ── Salvar perfil ────────────────────────────────────────────
    def _save_profile(_):
        """Salva perfil com dados encriptados."""
        msg_text.visible = False
        page.update()

        if not app_state.user or not app_state.user.get("id"):
            msg_text.value = "Erro: Utilizador não identificado"
            msg_text.color = c("error", dark)
            msg_text.visible = True
            page.update()
            return

        try:
            user_id = app_state.user["id"]
            master_key = EncryptionManager.derive_master_key(app_state.user["senha_hash"])

            # Preparar dados para encriptação
            profile_data = {
                "birth_date": data_nasc_field.value or None,
                "gender": genero_field.value or None,
            }

            # Encriptar telefone se fornecido
            if telefone_field.value:
                profile_data["encrypted_phone"] = EncryptionManager.encrypt_field(
                    telefone_field.value, master_key
                )

            # Atualizar perfil
            success, message = app_state.db.update_user_profile(user_id, profile_data)

            if success:
                msg_text.value = "Perfil atualizado com sucesso!"
                msg_text.color = c("success", dark)
                # Sair do modo edição
                edit_mode[0] = False
                edit_btn.text = "Editar"
                edit_btn.icon = ft.Icons.EDIT
                save_btn.visible = False
                telefone_field.read_only = True
                data_nasc_field.read_only = True
                genero_field.disabled = True
            else:
                msg_text.value = message
                msg_text.color = c("error", dark)

            msg_text.visible = True
            page.update()
        except Exception as e:
            msg_text.value = f"Erro ao salvar: {str(e)[:80]}"
            msg_text.color = c("error", dark)
            msg_text.visible = True
            page.update()

    def _go_back(_):
        """Retorna à tela anterior."""
        if edit_mode[0]:
            _toggle_edit(None)
        page.go("/config")

    # ── Botões ───────────────────────────────────────────────────
    edit_btn = ft.ElevatedButton(
        "Editar",
        icon=ft.Icons.EDIT,
        bgcolor=c("primary", dark),
        color=c("text_light", dark),
        on_click=_toggle_edit,
    )

    save_btn = ft.ElevatedButton(
        "Guardar",
        icon=ft.Icons.SAVE,
        bgcolor=c("success", dark),
        color=c("text_light", dark),
        on_click=_save_profile,
        visible=False,
    )

    # Carregar dados ao abrir
    _load_user_data()

    # ── Layout ───────────────────────────────────────────────────
    content = ft.Column(
        [
            # Header
            ft.Row(
                [
                    ft.IconButton(ft.Icons.ARROW_BACK, on_click=_go_back),
                    ft.Text(t("profile_title"), size=22, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    edit_btn,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(height=16, color=ft.Colors.TRANSPARENT),

            # Mensagens
            msg_text,
            ft.Divider(height=8, color=ft.Colors.TRANSPARENT),

            # ── Seção: Conta (read-only) ────────────────────────
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            t("profile_section_account"),
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=c("primary", dark),
                        ),
                        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                        nome_field,
                        email_field,
                        cref_field,
                    ],
                    spacing=10,
                ),
                padding=16,
                bgcolor=c("bg_card", dark),
                border_radius=RADIUS["md"],
                shadow=card_shadow(dark, "sm"),
            ),

            # ── Seção: Dados Pessoais (editáveis) ───────────────
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            t("profile_section_personal"),
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=c("primary", dark),
                        ),
                        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                        telefone_field,
                        data_nasc_field,
                        genero_field,
                    ],
                    spacing=10,
                ),
                padding=16,
                bgcolor=c("bg_card", dark),
                border_radius=RADIUS["md"],
                shadow=card_shadow(dark, "sm"),
            ),

            # ── Seção: Segurança ────────────────────────────────
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            t("profile_section_security"),
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=c("primary", dark),
                        ),
                        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                        ft.Text(
                            t("profile_password_warning"),
                            size=11,
                            color=c("text_secondary", dark),
                        ),
                        ft.ElevatedButton(
                            t("profile_change_password"),
                            icon=ft.Icons.LOCK,
                            on_click=lambda _: _show_password_dialog(),
                        ),
                    ],
                    spacing=10,
                ),
                padding=16,
                bgcolor=c("bg_card", dark),
                border_radius=RADIUS["md"],
                shadow=card_shadow(dark, "sm"),
            ),

            # ── Botão Guardar (visível apenas em modo edição) ────
            ft.Row(
                [save_btn],
                alignment=ft.MainAxisAlignment.END,
                visible=False,
            ),

            ft.Divider(height=16, color=ft.Colors.TRANSPARENT),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    def _show_password_dialog():
        """Mostra diálogo para mudar password."""
        page.open(
            ft.AlertDialog(
                title=ft.Text(t("profile_change_password")),
                content=ft.Text(
                    "Funcionalidade de mudança de password será implementada na próxima versão."
                ),
                actions=[
                    ft.TextButton("OK", on_click=lambda _: _close_dialog()),
                ],
            )
        )

    def _close_dialog():
        """Fecha diálogo."""
        page.close()

    return ft.View(
        route="/profile",
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
