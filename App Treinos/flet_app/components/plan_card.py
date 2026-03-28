"""
Plan Card — Card de plano de treino individual
================================================

Barra lateral colorida por fase de periodização,
sport + distance + semanas + botões de ação.
"""

import flet as ft
from flet_app.theme import c, PHASE_COLORS, SPORT_COLORS
from training_manager import TrainingRecord
from typing import Callable, Optional


def _sport_emoji(sport: str) -> str:
    _map = {
        "Corrida": "🏃", "Ciclismo": "🚴", "Natação": "🏊",
        "Triathlon": "🏅", "Duathlon (Natação+Corrida)": "🏊🏃",
        "Duathlon (Ciclismo+Corrida)": "🚴🏃",
    }
    return _map.get(sport, "🏋️")


def _phase_for_week(current_week: int, total_weeks: int) -> str:
    """Estima a fase de periodização com base na semana atual."""
    ratio = current_week / max(total_weeks, 1)
    if ratio < 0.35:
        return "Base"
    elif ratio < 0.55:
        return "Resistencia"
    elif ratio < 0.75:
        return "Velocidade"
    elif ratio < 0.90:
        return "Potencia"
    return "Polimento"


def build_plan_card(
    plan: TrainingRecord,
    current_week: int,
    on_calendar: Optional[Callable] = None,
    on_delete: Optional[Callable] = None,
    on_export: Optional[Callable] = None,
    dark: bool = False,
) -> ft.Container:
    """Constrói card de plano de treino."""

    phase = _phase_for_week(current_week, plan.weeks)
    phase_color = PHASE_COLORS.get(phase, c("primary", dark))

    created = plan.created_at[:10] if plan.created_at else "—"

    info_col = ft.Column(
        [
            ft.Text(
                f"{_sport_emoji(plan.sport)} {plan.sport} — {plan.distance}",
                size=15, weight=ft.FontWeight.W_600,
            ),
            ft.Text(f"Fase: {phase} · S{current_week}/{plan.weeks}", size=12, color=c("text_secondary", dark)),
            ft.Text(f"Criado em {created}", size=11, color=c("text_disabled", dark)),
        ],
        spacing=4,
        expand=True,
    )

    actions = ft.Row(
        [
            ft.IconButton(ft.Icons.CALENDAR_MONTH, tooltip="Calendário", icon_color=c("primary", dark), data=plan.id, on_click=on_calendar),
            ft.IconButton(ft.Icons.DOWNLOAD, tooltip="Exportar", icon_color=c("info", dark), data=plan.id, on_click=on_export),
            ft.IconButton(ft.Icons.DELETE_OUTLINE, tooltip="Apagar", icon_color=c("error", dark), data=plan.id, on_click=on_delete),
        ],
        spacing=0,
    )

    row = ft.Row([info_col, actions], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    return ft.Container(
        content=row,
        padding=ft.padding.only(left=0, right=12, top=12, bottom=12),
        border_radius=14,
        bgcolor=c("bg_card", dark),
        border=ft.border.only(left=ft.BorderSide(5, phase_color)),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=c("shadow", dark), offset=ft.Offset(0, 2)),
        ink=True,
        on_click=on_calendar,
    )
