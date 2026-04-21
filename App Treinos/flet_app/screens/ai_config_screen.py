"""
Tela de Configuração de IA
===========================

Permite ao treinador:
- Selecionar e configurar o provider de IA
- Introduzir e testar a API key
- Definir modelo e limites de tokens
- Visualizar consumo mensal
"""

import asyncio
import hashlib
import webbrowser
import flet as ft
from i18n import t
from flet_app.theme import c, SPACING, RADIUS, card_shadow
from flet_app.state import app_state
from flet_app.components.adaptive_nav import build_adaptive_layout
from ai.ai_config import (
    AIProviderConfig,
    SUPPORTED_PROVIDERS,
    load_ai_config,
    save_ai_config,
)
from ai.ai_assistant import AIAssistant


def _password_hash(cref: str) -> str:
    """Hash simples do CREF para derivar chave de cifra."""
    return hashlib.sha256(cref.encode()).hexdigest()


def ai_config_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View de configuração de IA."""

    dark = app_state.dark_mode
    cref = app_state.trainer_cref or ""
    pw_hash = _password_hash(cref)

    config = load_ai_config(cref)
    assistant = AIAssistant(cref, pw_hash)

    # ── Provider dropdown ────────────────────────────────────────

    provider_dd = ft.Dropdown(
        label="Plataforma de IA",
        value=config.provider or None,
        options=[
            ft.dropdown.Option(key=k, text=v["name"])
            for k, v in SUPPORTED_PROVIDERS.items()
        ],
        width=300,
        border_radius=RADIUS["sm"],
    )

    # ── Model dropdown ───────────────────────────────────────────

    def _get_models(provider_key: str):
        info = SUPPORTED_PROVIDERS.get(provider_key, {})
        return info.get("models", [])

    model_dd = ft.Dropdown(
        label="Modelo",
        value=config.model or None,
        options=[ft.dropdown.Option(m) for m in _get_models(config.provider)] if config.provider else [],
        width=300,
        border_radius=RADIUS["sm"],
    )

    # ── API key ──────────────────────────────────────────────────

    api_key_field = ft.TextField(
        label="API Key",
        password=True,
        can_reveal_password=True,
        value="",
        hint_text="Cole a sua API key aqui",
        width=400,
        border_radius=RADIUS["sm"],
    )

    if config.api_key_encrypted:
        api_key_field.hint_text = "••••• (chave já guardada — cole para substituir)"

    # ── Base URL (custom) ────────────────────────────────────────

    base_url_field = ft.TextField(
        label="URL Base (apenas para Custom)",
        value=config.base_url or "",
        hint_text="https://api.exemplo.com/v1",
        width=400,
        visible=config.provider == "custom",
        border_radius=RADIUS["sm"],
    )

    custom_model_field = ft.TextField(
        label="Nome do Modelo (Custom)",
        value=config.model if config.provider == "custom" else "",
        hint_text="nome-do-modelo",
        width=300,
        visible=config.provider == "custom",
        border_radius=RADIUS["sm"],
    )

    # ── Token limit ──────────────────────────────────────────────

    token_limit_field = ft.TextField(
        label="Limite mensal de tokens",
        value=str(config.max_monthly_tokens),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200,
        border_radius=RADIUS["sm"],
    )

    # ── Temperature ──────────────────────────────────────────────

    temp_slider = ft.Slider(
        value=config.temperature,
        min=0.0,
        max=1.0,
        divisions=10,
        label="{value}",
        width=250,
    )
    temp_label = ft.Text(f"Temperatura: {config.temperature:.1f}", size=13)

    def _on_temp_change(e):
        temp_label.value = f"Temperatura: {e.control.value:.1f}"
        page.update()

    temp_slider.on_change = _on_temp_change

    # ── Enabled switch ───────────────────────────────────────────

    enabled_switch = ft.Switch(
        label="IA Ativada",
        value=config.enabled,
    )

    # ── Status / feedback ────────────────────────────────────────

    status_text = ft.Text("", size=13)
    status_bar = ft.ProgressBar(visible=False, width=400)

    # ── Usage info ───────────────────────────────────────────────

    summary = assistant.get_usage_summary()

    usage_progress = ft.ProgressBar(
        value=min(summary["usage_pct"] / 100.0, 1.0),
        width=300,
        color=c("error", dark) if summary["over_limit"] else (
            c("warning", dark) if summary["near_limit"] else c("primary", dark)
        ),
        bgcolor=c("border_light", dark),
    )

    usage_text = ft.Text(
        f"{summary['total_tokens']:,} / {summary['max_monthly']:,} tokens "
        f"({summary['usage_pct']:.1f}%) — US$ {summary['total_cost_usd']:.4f} este mês",
        size=12,
        color=c("text_secondary", dark),
    )

    # Provider-specific API key instructions
    def _open_docs_url(docs_url: str):
        if docs_url:
            webbrowser.open(docs_url)

    docs_url_button = ft.Container(
        visible=False,
        content=ft.Row(
            [
                ft.Icon(ft.Icons.OPEN_IN_NEW, size=14, color=c("info", dark)),
                ft.TextButton(
                    "👉 Clique aqui para obter a API Key",
                    style=ft.ButtonStyle(
                        color=c("info", dark),
                    ),
                ),
            ],
            spacing=4,
            tight=True,
        ),
    )

    # ── Event handlers ───────────────────────────────────────────

    def _on_provider_change(e):
        prov = e.control.value
        models = _get_models(prov)
        model_dd.options = [ft.dropdown.Option(m) for m in models]
        default_model = SUPPORTED_PROVIDERS.get(prov, {}).get("default_model", "")
        model_dd.value = default_model if default_model in models else (models[0] if models else None)

        is_custom = prov == "custom"
        base_url_field.visible = is_custom
        custom_model_field.visible = is_custom
        model_dd.visible = not is_custom

        docs = SUPPORTED_PROVIDERS.get(prov, {}).get("docs_url", "")
        docs_url_button.visible = bool(docs)
        if docs:
            docs_url_button.content.controls[1].on_click = lambda _: _open_docs_url(docs)

        page.update()

    provider_dd.on_change = _on_provider_change

    def _save_config(_):
        prov = provider_dd.value
        if not prov:
            status_text.value = "Selecione uma plataforma."
            status_text.color = c("error", dark)
            page.update()
            return

        new_config = AIProviderConfig(
            provider=prov,
            api_key_encrypted=config.api_key_encrypted,
            model=custom_model_field.value if prov == "custom" else (model_dd.value or ""),
            base_url=base_url_field.value if prov == "custom" else "",
            max_monthly_tokens=int(token_limit_field.value or 500000),
            temperature=round(temp_slider.value, 1),
            enabled=enabled_switch.value,
        )

        new_key = api_key_field.value.strip()
        if new_key:
            new_config.set_api_key(new_key, pw_hash)

        if not new_config.api_key_encrypted:
            status_text.value = "Insira a API key."
            status_text.color = c("error", dark)
            page.update()
            return

        save_ai_config(cref, new_config)
        status_text.value = "Configuração guardada com sucesso!"
        status_text.color = c("success", dark)
        api_key_field.value = ""
        api_key_field.hint_text = "••••• (chave já guardada — cole para substituir)"
        page.update()

    def _test_connection(_):
        status_text.value = "Testando ligação..."
        status_text.color = c("text_secondary", dark)
        status_bar.visible = True
        page.update()

        # Save first if key was entered
        _save_config(None)

        reloaded = load_ai_config(cref)
        test_assistant = AIAssistant(cref, pw_hash)
        test_assistant._config = reloaded

        resp = test_assistant.test_connection()
        status_bar.visible = False

        if resp.is_error:
            status_text.value = f"Erro: {resp.error_message}"
            status_text.color = c("error", dark)
        else:
            status_text.value = (
                f"Ligação OK! Modelo: {resp.model} — "
                f"Latência: {resp.latency_ms}ms"
            )
            status_text.color = c("success", dark)
        page.update()

    # ── Layout ───────────────────────────────────────────────────

    section_title = ft.Row(
        [
            ft.Icon(ft.Icons.SMART_TOY_OUTLINED, size=24, color=c("primary", dark)),
            ft.Text("Configuração de IA", size=24, weight=ft.FontWeight.BOLD),
        ],
        spacing=SPACING["sm"],
    )

    usage_section = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.DATA_USAGE, size=18, color=c("text_secondary", dark)),
                        ft.Text("Consumo Mensal", size=16, weight=ft.FontWeight.W_600),
                    ],
                    spacing=SPACING["xs"],
                ),
                usage_progress,
                usage_text,
            ],
            spacing=SPACING["xs"],
        ),
        bgcolor=c("bg_card", dark),
        border_radius=RADIUS["md"],
        padding=SPACING["md"],
        shadow=card_shadow(dark),
    )

    config_form = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.TUNE, size=18, color=c("text_secondary", dark)),
                        ft.Text("Provider e Credenciais", size=16, weight=ft.FontWeight.W_600),
                    ],
                    spacing=SPACING["xs"],
                ),
                ft.Text(
                    "Escolha a plataforma de IA que prefere usar. Cada uma é gratuita para começar.",
                    size=12,
                    color=c("text_secondary", dark),
                ),
                provider_dd,
                docs_url_button,
                model_dd,
                custom_model_field,
                ft.Text(
                    "Cole a sua API Key aqui. É uma senha única que você consegue na plataforma de IA.",
                    size=12,
                    color=c("text_secondary", dark),
                ),
                api_key_field,
                base_url_field,
                ft.Divider(height=12, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SETTINGS_SUGGEST, size=18, color=c("text_secondary", dark)),
                        ft.Text("Parâmetros", size=16, weight=ft.FontWeight.W_600),
                    ],
                    spacing=SPACING["xs"],
                ),
                token_limit_field,
                temp_label,
                temp_slider,
                enabled_switch,
            ],
            spacing=SPACING["sm"],
        ),
        bgcolor=c("bg_card", dark),
        border_radius=RADIUS["md"],
        padding=SPACING["md"],
        shadow=card_shadow(dark),
    )

    actions_row = ft.Row(
        [
            ft.ElevatedButton(
                "Guardar",
                icon=ft.Icons.SAVE,
                bgcolor=c("primary", dark),
                color=c("text_light", dark),
                on_click=_save_config,
            ),
            ft.OutlinedButton(
                "Testar Ligação",
                icon=ft.Icons.WIFI_TETHERING,
                on_click=_test_connection,
            ),
            ft.TextButton(
                "Voltar",
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: page.go("/config"),
            ),
        ],
        spacing=SPACING["sm"],
    )

    content = ft.Column(
        [
            section_title,
            ft.Divider(),
            usage_section,
            config_form,
            status_bar,
            status_text,
            actions_row,
        ],
        spacing=SPACING["md"],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    return build_adaptive_layout(
        page=page,
        selected_index=4,
        body=ft.Container(
            content=content,
            padding=SPACING["lg"],
            expand=True,
        ),
        dark=dark,
    )
