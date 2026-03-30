"""
Register Screen — Cadastro de novo treinador
==============================================

Usa DatabaseManager.cadastrar_usuario() para criar conta.
"""

import flet as ft
from i18n import t
from flet_app.theme import c
from flet_app.state import app_state


def register_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de registo."""

    dark = app_state.dark_mode

    nome = ft.TextField(label=t("register_name"), prefix_icon=ft.Icons.PERSON_OUTLINE, border_radius=12, filled=True, autofocus=True, max_length=100)
    cpf = ft.TextField(label=t("register_cpf"), prefix_icon=ft.Icons.BADGE_OUTLINED, border_radius=12, filled=True, max_length=14)
    cref = ft.TextField(label=t("register_cref"), prefix_icon=ft.Icons.VERIFIED_OUTLINED, border_radius=12, filled=True, max_length=20)
    email = ft.TextField(label=t("register_email"), prefix_icon=ft.Icons.EMAIL_OUTLINED, border_radius=12, filled=True, max_length=100)
    senha = ft.TextField(label=t("register_password"), prefix_icon=ft.Icons.LOCK_OUTLINE, password=True, can_reveal_password=True, border_radius=12, filled=True, max_length=128)
    senha2 = ft.TextField(label=t("register_confirm"), prefix_icon=ft.Icons.LOCK_OUTLINE, password=True, can_reveal_password=True, border_radius=12, filled=True, max_length=128)
    msg = ft.Text("", size=13, visible=False)

    register_btn = ft.ElevatedButton(
        t("register_button"),
        icon=ft.Icons.PERSON_ADD,
        bgcolor=c("primary", dark),
        color=c("text_light", dark),
        width=320,
        height=48,
        on_click=lambda _: _do_register(None),
    )

    register_busy = [False]  # debounce guard

    def _do_register(_):
        if register_busy[0]:
            return
        # Validação básica
        if not nome.value or not cpf.value or not cref.value or not senha.value:
            msg.value = t("register_error_required")
            msg.color = c("error", dark)
            msg.visible = True
            page.update()
            return
        if senha.value != senha2.value:
            msg.value = t("register_error_mismatch")
            msg.color = c("error", dark)
            msg.visible = True
            page.update()
            return
        if len(senha.value) < 6:
            msg.value = t("register_error_short")
            msg.color = c("error", dark)
            msg.visible = True
            page.update()
            return

        register_busy[0] = True
        register_btn.disabled = True
        register_btn.text = t("register_processing")
        msg.visible = False
        page.update()

        ok, resp = app_state.db.cadastrar_usuario(
            cpf=cpf.value.strip(),
            cref=cref.value.strip(),
            nome=nome.value.strip(),
            senha=senha.value,
            email=email.value.strip() or None,
        )
        if ok:
            msg.value = t("register_success")
            msg.color = c("success", dark)
            msg.visible = True
            page.update()

            import time, threading
            def _redirect():
                time.sleep(0.8)
                page.go("/login")
            threading.Thread(target=_redirect, daemon=True).start()
        else:
            msg.value = resp
            msg.color = c("error", dark)
            msg.visible = True
            register_btn.disabled = False
            register_btn.text = t("register_button")
            register_busy[0] = False
            page.update()

    def _go_back(_):
        page.go("/login")

    card = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [ft.IconButton(ft.Icons.ARROW_BACK, on_click=_go_back),
                     ft.Text(t("register_title"), size=22, weight=ft.FontWeight.BOLD)],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                nome, cpf, cref, email, senha, senha2,
                msg,
                ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                register_btn,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            width=380,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=32,
        border_radius=20,
        bgcolor=c("bg_card", dark),
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=c("shadow", dark), offset=ft.Offset(0, 4)),
    )

    return ft.View(
        route="/register",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=c("bg_secondary", dark),
        controls=[card],
    )
