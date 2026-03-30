"""
Config Screen — Preferências e administração
==============================================

Toggle dark mode, seletor de idioma, logout, acesso admin.
"""

import flet as ft
from i18n import t, set_language, get_language, SUPPORTED_LANGUAGES
from flet_app.theme import c, build_theme, SPACING
from flet_app.state import app_state
from flet_app.components.adaptive_nav import build_adaptive_layout
from flet_app.components.feature_tooltip import build_feature_tooltip


_LANG_LABELS = {"pt": "Português", "en": "English", "es": "Español"}


def config_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de configurações."""

    dark = app_state.dark_mode

    # ── Dark mode ────────────────────────────────────────────────
    def _toggle_dark(e):
        app_state.dark_mode = e.control.value
        page.theme_mode = ft.ThemeMode.DARK if app_state.dark_mode else ft.ThemeMode.LIGHT
        page.theme = build_theme(dark=app_state.dark_mode)
        app_state.save_preferences()
        page.go("/config")  # reload view

    dark_switch = ft.Switch(
        label=t("config_dark_mode"),
        value=app_state.dark_mode,
        on_change=_toggle_dark,
    )

    # ── Idioma ───────────────────────────────────────────────────
    def _change_lang(e):
        code = e.control.data
        set_language(code)
        app_state.language = code
        app_state.save_preferences()
        page.go("/config")  # reload view com novo idioma

    lang_chips = ft.Row(
        [
            ft.ElevatedButton(
                label,
                data=code,
                bgcolor=c("primary", dark) if get_language() == code else c("bg_card", dark),
                color=c("text_light", dark) if get_language() == code else c("text_primary", dark),
                on_click=_change_lang,
            )
            for code, label in _LANG_LABELS.items()
        ],
        spacing=8,
    )

    # ── Logout ───────────────────────────────────────────────────
    def _logout(_):
        app_state.logout()
        page.go("/login")

    # ── Admin ────────────────────────────────────────────────────
    admin_btn = ft.ElevatedButton(
        t("config_admin"),
        icon=ft.Icons.ADMIN_PANEL_SETTINGS,
        bgcolor=c("triadic_1", dark),
        color=c("text_light", dark),
        on_click=lambda _: page.go("/admin"),
        visible=app_state.is_admin,
    )

    # ── Layout ───────────────────────────────────────────────────
    tooltip = build_feature_tooltip(
        "config",
        t("tooltip_config"),
        page, dark,
    )
    content = ft.Column(
        [
            ft.Row([ft.Icon(ft.Icons.SETTINGS, size=24, color=c("primary", dark)), ft.Text(t("config_title"), size=24, weight=ft.FontWeight.BOLD)], spacing=SPACING["sm"]),
            ft.Divider(),
            ft.Text(t("config_theme"), size=16, weight=ft.FontWeight.W_600),
            dark_switch,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Text(t("config_language"), size=16, weight=ft.FontWeight.W_600),
            lang_chips,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            admin_btn,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Text(t("config_session", name=app_state.trainer_name or "—"), size=13, color=c("text_secondary", dark)),
            ft.OutlinedButton(t("config_logout"), icon=ft.Icons.LOGOUT, on_click=_logout),
        ],
        spacing=8,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    return build_adaptive_layout(
        page=page,
        selected_index=4,
        body=ft.Container(content=ft.Column([tooltip, content], spacing=SPACING["sm"]), padding=SPACING["lg"], expand=True),
        dark=dark,
    )
