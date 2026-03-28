"""
Templates — Biblioteca de templates de treino
==============================================

Grid de templates (do sistema + do treinador) com criação e uso.
"""

import flet as ft
from flet_app.theme import c, SPORT_COLORS
from flet_app.state import app_state
from flet_app.components.template_card import build_template_card
from flet_app.components.nav_bar import build_nav_bar
from training_manager import training_manager


# Templates de sistema pré-definidos
SYSTEM_TEMPLATES = [
    {"id": "sys_rec", "name": "Recuperação Ativa", "sport": "Corrida", "type": "Recuperação", "zone": "Z1 - Recuperação", "duration": "30 min", "modality": "Corrida", "description": "Corrida leve contínua para recuperação."},
    {"id": "sys_base", "name": "Base Aeróbica", "sport": "Corrida", "type": "Base", "zone": "Z2 - Aeróbico", "duration": "50 min", "modality": "Corrida", "description": "Corrida em ritmo constante Z2."},
    {"id": "sys_int", "name": "Intervalado 800m", "sport": "Corrida", "type": "Intervalado", "zone": "Z4 - Limiar", "duration": "45 min", "modality": "Corrida", "description": "15min aquec + 6x800m (rec 2min) + 10min desaq."},
    {"id": "sys_longo", "name": "Longão Semanal", "sport": "Corrida", "type": "Longo", "zone": "Z2 - Aeróbico", "duration": "90 min", "modality": "Corrida", "description": "Corrida longa a ritmo confortável."},
    {"id": "sys_nat_tec", "name": "Técnica Natação", "sport": "Natação", "type": "Técnica", "zone": "Z2 - Aeróbico", "duration": "60 min", "modality": "Natação", "description": "1000m aquec + drills técnicos + 500m desaq."},
    {"id": "sys_bike", "name": "Pedal Base", "sport": "Ciclismo", "type": "Base", "zone": "Z2 - Aeróbico", "duration": "90 min", "modality": "Ciclismo", "description": "Pedal constante em terreno plano."},
    {"id": "sys_fartlek", "name": "Fartlek", "sport": "Corrida", "type": "Fartlek", "zone": "Z3 - Tempo", "duration": "40 min", "modality": "Corrida", "description": "Alternância livre de ritmos."},
    {"id": "sys_brick", "name": "Brick Bike+Run", "sport": "Triathlon", "type": "Combinado", "zone": "Z3 - Tempo", "duration": "90 min", "modality": "Brick", "description": "60min bike Z2 + 30min corrida Z3."},
]


def templates_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View da biblioteca de templates."""

    dark = app_state.dark_mode
    trainer = app_state.trainer_info()

    # ── Carregar templates do treinador ──────────────────────────
    user_templates = training_manager.get_templates(trainer) if trainer else []

    # ── Listas ───────────────────────────────────────────────────
    user_list = ft.Column(spacing=8)
    system_list = ft.Column(spacing=8)

    def _refresh():
        nonlocal user_templates
        user_templates = training_manager.get_templates(trainer) if trainer else []
        _populate()
        page.update()

    def _populate():
        # User templates
        user_list.controls.clear()
        if not user_templates:
            user_list.controls.append(
                ft.Text("Nenhum template criado. Use 'Novo' para criar.", size=13, color=c("text_secondary", dark))
            )
        for tmpl in user_templates:
            card = build_template_card(tmpl, on_use=_use_template, on_delete=_delete_template, dark=dark)
            user_list.controls.append(card)

        # System templates
        system_list.controls.clear()
        for tmpl in SYSTEM_TEMPLATES:
            card = build_template_card(tmpl, on_use=_use_template, dark=dark)
            system_list.controls.append(card)

    def _use_template(e):
        tmpl_id = e.control.data
        # Find template
        tmpl = None
        for t in user_templates + SYSTEM_TEMPLATES:
            if t.get("id") == tmpl_id:
                tmpl = t
                break
        if tmpl:
            page.open(ft.SnackBar(
                ft.Text(f"📋 Template '{tmpl['name']}' disponível para uso no editor de treino."),
                bgcolor=c("info", dark),
            ))

    def _delete_template(e):
        tmpl_id = e.control.data
        ok = training_manager.delete_template(trainer, tmpl_id)
        if ok:
            page.open(ft.SnackBar(ft.Text("🗑️ Template removido."), bgcolor=c("warning", dark)))
            _refresh()

    # ── Criar novo template ──────────────────────────────────────
    def _open_create_dialog(_):
        name_f = ft.TextField(label="Nome", autofocus=True, expand=True)
        sport_f = ft.Dropdown(
            label="Desporto", width=160,
            options=[ft.dropdown.Option(s) for s in SPORT_COLORS.keys()],
        )
        type_f = ft.Dropdown(
            label="Tipo", width=140,
            options=[ft.dropdown.Option(t) for t in ["Recuperação", "Base", "Tempo", "Intervalado", "Longo", "Técnica", "Fartlek", "Sprint", "Combinado"]],
        )
        zone_f = ft.Dropdown(
            label="Zona", width=180,
            options=[ft.dropdown.Option(z) for z in ["Z1 - Recuperação", "Z2 - Aeróbico", "Z3 - Tempo", "Z4 - Limiar", "Z5 - VO2max"]],
        )
        dur_f = ft.TextField(label="Duração", hint_text="Ex: 45 min", width=120)
        desc_f = ft.TextField(label="Descrição", multiline=True, min_lines=2, max_lines=3)

        def _save(e):
            if not name_f.value or not sport_f.value:
                return
            tmpl = {
                "name": name_f.value,
                "sport": sport_f.value,
                "type": type_f.value or "",
                "zone": zone_f.value or "",
                "duration": dur_f.value or "",
                "modality": sport_f.value,
                "description": desc_f.value or "",
            }
            ok = training_manager.save_template(trainer, tmpl)
            if ok:
                page.close(dialog)
                page.open(ft.SnackBar(ft.Text("✅ Template criado."), bgcolor=c("success", dark)))
                _refresh()

        dialog = ft.AlertDialog(
            title=ft.Text("📋 Novo Template"),
            content=ft.Container(
                content=ft.Column([
                    name_f,
                    ft.Row([sport_f, type_f], spacing=8),
                    ft.Row([zone_f, dur_f], spacing=8),
                    desc_f,
                ], spacing=10),
                width=420, height=280,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog)),
                ft.ElevatedButton("Salvar", on_click=_save, bgcolor=c("primary", dark), color=c("text_light", dark)),
            ],
        )
        page.open(dialog)

    _populate()

    # ── FAB ──────────────────────────────────────────────────────
    fab = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        text="Novo",
        bgcolor=c("primary", dark),
        foreground_color=c("text_light", dark),
        on_click=_open_create_dialog,
    )

    return ft.View(
        route="/templates",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("📋 Meus Templates", size=18, weight=ft.FontWeight.BOLD),
                        user_list,
                        ft.Divider(height=20),
                        ft.Text("📦 Templates do Sistema", size=18, weight=ft.FontWeight.BOLD),
                        system_list,
                    ],
                    spacing=12,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                padding=ft.padding.all(16),
                expand=True,
            )
        ],
        navigation_bar=build_nav_bar(page, selected_index=0),
        floating_action_button=fab,
        bgcolor=c("bg_secondary", dark),
    )
