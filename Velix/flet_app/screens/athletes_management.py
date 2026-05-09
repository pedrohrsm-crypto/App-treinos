"""
Gerenciamento de Atletas — CRUD com banco de dados
===================================================

Tela para criar, editar, visualizar e deletar atletas.
Todos os dados persistem no banco de dados SQLite.
"""

import asyncio
import flet as ft
from i18n import t
from flet_app.theme import c, RADIUS, SPACING
from flet_app.components.adaptive_nav import build_adaptive_layout
from flet_app.state import app_state
from flet_app.components.loading_overlay import build_loading
from flet_app.components.confirm_modal import show_confirm
from flet_app.components.toast import show_toast
from flet_app.components.tour_overlay import create_athletes_tour


def athletes_management_view(page: ft.Page, route: str) -> ft.View:
    """Tela de gerenciamento de atletas com operações CRUD."""

    dark = app_state.dark_mode
    athlete_list_view = None
    create_athlete_view = None

    # ── List View ────────────────────────────────────────────────
    def build_list_view():
        """Constrói lista de atletas."""
        athletes_container = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

        async def load_athletes():
            """Carrega atletas do banco de dados."""
            athletes_container.controls.clear()

            if not app_state.db or not app_state.trainer_cref:
                athletes_container.controls.append(
                    ft.Text("Erro: Sem conexão ao BD ou usuário não autenticado",
                           color=c("warning", dark))
                )
                page.update()
                return

            athletes = app_state.db.get_athletes_by_trainer(app_state.trainer_cref)

            if not athletes:
                athletes_container.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.PERSON_ADD, size=48,
                                   color=c("text_disabled", dark)),
                            ft.Text("Nenhum atleta cadastrado", size=16,
                                   color=c("text_secondary", dark)),
                            ft.TextButton("Criar primeiro atleta +",
                                        on_click=lambda e: _switch_to_create()),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                           spacing=SPACING["md"]),
                        alignment=ft.Alignment.CENTER,
                        expand=True,
                    )
                )
            else:
                for athlete in athletes:
                    card = _build_athlete_card(athlete)
                    athletes_container.controls.append(card)

            page.update()

            # Iniciar tour se for primeira vez
            tour = create_athletes_tour(page)
            tour.start()

        page.run_task(load_athletes)

        return ft.Column([
            # Header
            ft.Container(
                content=ft.Row([
                    ft.Text("Meus Atletas", size=24, weight=ft.FontWeight.BOLD,
                           color=c("text_primary", dark)),
                    ft.IconButton(ft.Icons.ADD,
                                 on_click=lambda e: _switch_to_create(),
                                 icon_color=c("primary", dark)),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=SPACING["lg"],
            ),
            # List
            athletes_container,
        ], expand=True)

    def _build_athlete_card(athlete: dict) -> ft.Container:
        """Constrói card de um atleta."""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(athlete.get("nome", "N/A"), size=16,
                               weight=ft.FontWeight.W_600, color=c("text_primary", dark)),
                        ft.Text(f"CPF: {athlete.get('cpf', 'N/A')}", size=12,
                               color=c("text_secondary", dark)),
                    ], expand=True, spacing=2),
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Editar", icon=ft.Icons.EDIT,
                                           on_click=lambda e, a=athlete: _edit_athlete(a)),
                            ft.PopupMenuItem(text="Deletar", icon=ft.Icons.DELETE,
                                           on_click=lambda e, a=athlete: _delete_athlete(a)),
                        ],
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                ft.Row([
                    ft.Text(f"Esporte: {athlete.get('esporte_principal', 'N/A')}",
                           size=12, color=c("text_secondary", dark)),
                    ft.Text(f"Peso: {athlete.get('peso_atual', 'N/A')} kg",
                           size=12, color=c("text_secondary", dark)),
                ], spacing=SPACING["md"]),
            ], spacing=SPACING["sm"]),
            padding=SPACING["md"],
            margin=ft.margin.symmetric(horizontal=SPACING["md"], vertical=SPACING["sm"]),
            bgcolor=c("bg_tertiary", dark),
            border_radius=RADIUS["md"],
            border=ft.border.all(1, c("border_light", dark)),
        )

    # ── Create/Edit View ─────────────────────────────────────────
    def build_create_view():
        """Constrói formulário de criação/edição de atleta."""

        form_fields = {
            "nome": ft.TextField(label="Nome", required=True),
            "cpf": ft.TextField(label="CPF (11 dígitos)"),
            "email": ft.TextField(label="Email"),
            "genero": ft.Dropdown(
                label="Gênero",
                options=[
                    ft.dropdown.Option("masculino", "Masculino"),
                    ft.dropdown.Option("feminino", "Feminino"),
                    ft.dropdown.Option("outro", "Outro"),
                ],
            ),
            "data_nascimento": ft.TextField(label="Data de Nascimento (YYYY-MM-DD)"),
            "peso_atual": ft.TextField(label="Peso (kg)", keyboard_type=ft.KeyboardType.NUMBER),
            "altura": ft.TextField(label="Altura (cm)", keyboard_type=ft.KeyboardType.NUMBER),
            "esporte_principal": ft.TextField(label="Esporte Principal (ex: corrida)"),
            "vo2_max": ft.TextField(label="VO2 Max (ml/kg/min)", keyboard_type=ft.KeyboardType.NUMBER),
            "frequencia_cardiaca_repouso": ft.TextField(label="FC Repouso (bpm)",
                                                       keyboard_type=ft.KeyboardType.NUMBER),
        }

        def _on_save():
            """Salva atleta no banco de dados."""
            # Validar campos obrigatórios
            if not form_fields["nome"].value.strip():
                show_toast(page, "Nome é obrigatório", dark)
                return

            athlete_data = {
                k: v.value for k, v in form_fields.items()
            }

            try:
                athlete_id = app_state.db.create_athlete(app_state.trainer_cref, athlete_data)
                if athlete_id > 0:
                    show_toast(page, f"Atleta {athlete_data['nome']} criado com sucesso!", dark)
                    _switch_to_list()
                else:
                    show_toast(page, "Erro ao criar atleta", dark)
            except Exception as e:
                show_toast(page, f"Erro: {str(e)}", dark)

        return ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.IconButton(ft.Icons.ARROW_BACK,
                                 on_click=lambda e: _switch_to_list()),
                    ft.Text("Novo Atleta", size=24, weight=ft.FontWeight.BOLD,
                           color=c("text_primary", dark)),
                ], spacing=SPACING["md"]),
                padding=SPACING["lg"],
            ),
            ft.Container(
                content=ft.Column([form_fields[k] for k in form_fields],
                                spacing=SPACING["md"]),
                padding=SPACING["lg"],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            ft.Container(
                content=ft.Row([
                    ft.TextButton("Cancelar", on_click=lambda e: _switch_to_list()),
                    ft.ElevatedButton("Salvar", on_click=lambda e: _on_save(),
                                     bgcolor=c("primary", dark)),
                ], alignment=ft.MainAxisAlignment.END, spacing=SPACING["md"]),
                padding=SPACING["lg"],
            ),
        ], expand=True)

    def _switch_to_list():
        body.content = build_list_view()
        page.update()

    def _switch_to_create():
        body.content = build_create_view()
        page.update()

    def _edit_athlete(athlete: dict):
        show_toast(page, f"Editar {athlete['nome']} - em desenvolvimento", dark)

    def _delete_athlete(athlete: dict):
        def confirm_delete():
            if app_state.db.delete_athlete(athlete["id"]):
                show_toast(page, f"Atleta {athlete['nome']} deletado", dark)
                _switch_to_list()
            else:
                show_toast(page, "Erro ao deletar atleta", dark)

        show_confirm(
            page,
            f"Deletar atleta '{athlete['nome']}'?",
            confirm_delete,
            dark
        )

    # ── Body ─────────────────────────────────────────────────────
    body = ft.Container(expand=True, content=build_list_view())

    return build_adaptive_layout(page, 0, body, dark)
