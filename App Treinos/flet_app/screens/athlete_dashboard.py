"""
Athlete Dashboard — Dashboard individual do atleta
====================================================

Header com info pessoal + stats + hero cards de planos.
Dados carregados assincronamente com spinner.
"""

import asyncio
import flet as ft
from datetime import datetime
from i18n import t
from flet_app.theme import c, SPORT_COLORS
from flet_app.state import app_state
from flet_app.components.plan_card import build_plan_card
from flet_app.components.loading_overlay import build_loading
from training_manager import training_manager


def athlete_dashboard_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View do dashboard de um atleta específico."""

    dark = app_state.dark_mode
    athlete_name = app_state.selected_athlete or route.rstrip("/").rsplit("/", 1)[-1]
    trainer = app_state.trainer_info()

    # ── Header (estático, mostra imediatamente) ──────────────────
    initials = "".join(w[0] for w in athlete_name.split()[:2]).upper()
    avatar = ft.CircleAvatar(
        content=ft.Text(initials, size=24, weight=ft.FontWeight.BOLD, color="#FFF"),
        bgcolor=c("primary", dark), radius=32,
    )

    header = ft.Container(
        content=ft.Row(
            [
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/dashboard")),
                avatar,
                ft.Column(
                    [
                        ft.Text(athlete_name, size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("Carregando dados…", size=13, color=c("text_secondary", dark)),
                    ],
                    spacing=2,
                ),
            ],
            spacing=12,
        ),
        padding=ft.padding.only(left=8, right=16, top=12, bottom=8),
    )

    # Placeholder que será substituído com dados reais
    body = ft.Container(content=build_loading("Carregando planos…", dark), expand=True)

    # ── FAB novo plano ───────────────────────────────────────────
    fab = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        tooltip="Novo Plano",
        bgcolor=c("primary", dark),
        foreground_color=c("text_light", dark),
        on_click=lambda _: page.go("/wizard"),
    )

    # ── Carregamento assíncrono ──────────────────────────────────
    async def _load_data():
        await asyncio.sleep(0.01)

        plans = training_manager.get_trainer_plans(trainer) if trainer else []
        athlete_plans = [p for p in plans if p.athlete_name == athlete_name]
        latest = athlete_plans[0] if athlete_plans else None
        data = latest.athlete_data if latest else {}

        now = datetime.now()
        def _current_week(plan):
            try:
                created = datetime.fromisoformat(plan.created_at)
                elapsed = (now - created).days
                return min(max(elapsed // 7 + 1, 1), plan.weeks)
            except (ValueError, TypeError):
                return 1

        total_plans = len(athlete_plans)
        total_weeks = sum(p.weeks for p in athlete_plans)
        latest_sport = latest.sport if latest else "—"
        sport_color = SPORT_COLORS.get(latest_sport, c("primary", dark))

        # Atualizar avatar com cor do desporto
        avatar.bgcolor = sport_color

        # Atualizar subtítulo do header
        header.content.controls[2].controls[1] = ft.Text(
            f"{data.get('idade', '?')} anos · {data.get('peso', '?')} kg · {data.get('altura', '?')} cm",
            size=13, color=c("text_secondary", dark),
        )

        # Stats
        def _stat(icon, value, label):
            return ft.Container(
                content=ft.Column(
                    [ft.Text(icon, size=22), ft.Text(value, size=18, weight=ft.FontWeight.BOLD), ft.Text(label, size=11, color=c("text_secondary", dark))],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2,
                ),
                padding=12, border_radius=12, bgcolor=c("bg_card", dark),
                shadow=ft.BoxShadow(blur_radius=4, color=c("shadow", dark)),
                expand=True,
            )

        stats_row = ft.Row(
            [
                _stat("📋", str(total_plans), "Planos"),
                _stat("📅", str(total_weeks), "Semanas"),
                _stat(_sport_emoji(latest_sport), latest_sport, "Desporto"),
                _stat("⚖️", f"{data.get('imc', '—')}", "IMC"),
            ],
            spacing=10,
        )

        # Acções nos cards de plano
        def _go_calendar(e):
            plan_id = e.control.data
            app_state.selected_plan_id = plan_id
            page.go(f"/calendar/{plan_id}")

        def _delete_plan(e):
            plan_id = e.control.data
            ok, msg = training_manager.delete_plan(trainer, plan_id)
            if ok:
                page.go(f"/athlete/{athlete_name}")
            else:
                page.open(ft.SnackBar(ft.Text(msg), bgcolor=c("error", dark)))

        def _export_plan(e):
            page.open(ft.SnackBar(ft.Text("Exportação disponível via wizard."), bgcolor=c("info", dark)))

        plan_cards = []
        for p in athlete_plans:
            cw = _current_week(p)
            card = build_plan_card(p, current_week=cw, on_calendar=_go_calendar, on_delete=_delete_plan, on_export=_export_plan, dark=dark)
            plan_cards.append(card)

        if not plan_cards:
            plan_cards.append(
                ft.Container(ft.Text("Nenhum plano criado para este atleta.", color=c("text_secondary", dark)), padding=20)
            )

        content = ft.Column(
            [stats_row, ft.Divider(height=16, color=ft.Colors.TRANSPARENT),
             ft.Text("  Planos de Treino", size=16, weight=ft.FontWeight.W_600),
             *plan_cards],
            spacing=8,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        body.content = content
        page.update()

    page.run_task(_load_data)

    return ft.View(
        route=f"/athlete/{athlete_name}",
        controls=[header, ft.Container(content=body, padding=ft.padding.symmetric(horizontal=8), expand=True)],
        floating_action_button=fab,
    )


def _sport_emoji(sport: str) -> str:
    _map = {"Corrida": "🏃", "Ciclismo": "🚴", "Natação": "🏊", "Triathlon": "🏅"}
    return _map.get(sport, "🏋️")
