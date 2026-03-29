"""
Login Screen — Autenticação do treinador
==========================================

Usa DatabaseManager.autenticar_usuario() para validar CPF/CREF + senha.
"""

import flet as ft
from i18n import t
from flet_app.theme import c
from flet_app.state import app_state


def login_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de login."""

    dark = app_state.dark_mode

    # ── Campos ───────────────────────────────────────────────────
    credential = ft.TextField(
        label=t("login_cpf_cref"),
        prefix_icon=ft.Icons.BADGE_OUTLINED,
        border_radius=12,
        filled=True,
        autofocus=True,
    )
    password = ft.TextField(
        label=t("login_password"),
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        border_radius=12,
        filled=True,
        on_submit=lambda _: _do_login(None),
    )
    error_text = ft.Text("", color=c("error", dark), size=13, visible=False)

    # ── Acções ───────────────────────────────────────────────────
    def _do_login(_):
        cred = credential.value.strip()
        pwd = password.value.strip()
        if not cred or not pwd:
            error_text.value = t("login_error_empty")
            error_text.visible = True
            page.update()
            return

        ok, data = app_state.db.autenticar_usuario(cred, pwd)
        if ok:
            app_state.login(data)
            app_state.save_session(cred, pwd)
            page.go("/dashboard")
        else:
            error_text.value = t("login_error_invalid")
            error_text.visible = True
            page.update()

    def _go_register(_):
        page.go("/register")

    # ── Layout ───────────────────────────────────────────────────
    card = ft.Container(
        content=ft.Column(
            [
                ft.Text("🏃", size=50, text_align=ft.TextAlign.CENTER),
                ft.Text(
                    t("app_name"),
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    t("login_title"),
                    size=14,
                    color=c("text_secondary", dark),
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                credential,
                password,
                error_text,
                ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                ft.ElevatedButton(
                    t("login_button"),
                    icon=ft.Icons.LOGIN,
                    bgcolor=c("primary", dark),
                    color=c("text_light", dark),
                    width=320,
                    height=48,
                    on_click=_do_login,
                ),
                ft.TextButton(
                    t("register_link"),
                    on_click=_go_register,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            width=360,
        ),
        padding=40,
        border_radius=20,
        bgcolor=c("bg_card", dark),
        shadow=ft.BoxShadow(
            spread_radius=1, blur_radius=15,
            color=c("shadow", dark), offset=ft.Offset(0, 4),
        ),
    )

    return ft.View(
        route="/login",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=c("bg_secondary", dark),
        controls=[card],
    )
