"""
Plan Card — Card de plano de treino individual
================================================

Barra lateral colorida por fase de periodização,
sport + distance + semanas + botões de ação.
"""

import flet as ft
from i18n import t
from flet_app.theme import c, PHASE_COLORS, SPORT_COLORS, RADIUS, SPACING, card_shadow
from flet_app.components.hover_effects import apply_hover_effects_to_icon_button
from training_manager import TrainingRecord
from typing import Callable, Optional


def _sport_icon(sport: str) -> ft.Icon:
    _map = {
        "Corrida": ft.Icons.DIRECTIONS_RUN, "Ciclismo": ft.Icons.DIRECTIONS_BIKE,
        "Natação": ft.Icons.POOL, "Triathlon": ft.Icons.EMOJI_EVENTS,
        "Duathlon (Natação+Corrida)": ft.Icons.POOL,
        "Duathlon (Ciclismo+Corrida)": ft.Icons.DIRECTIONS_BIKE,
    }
    return ft.Icon(_map.get(sport, ft.Icons.FITNESS_CENTER), size=16, color=c("primary", dark=False))


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
            ft.Row([
                _sport_icon(plan.sport),
                ft.Text(f"{plan.sport} — {plan.distance}", size=15, weight=ft.FontWeight.W_600),
            ], spacing=SPACING["xs"]),
            ft.Text(t("plan_phase_label", phase=phase, week=current_week, total=plan.weeks), size=12, color=c("text_secondary", dark)),
            ft.Text(t("plan_created_at", date=created), size=11, color=c("text_disabled", dark)),
        ],
        spacing=SPACING["xs"],
        expand=True,
    )

    actions = ft.Row(
        [
            apply_hover_effects_to_icon_button(
                ft.IconButton(ft.Icons.CALENDAR_MONTH, tooltip=t("plan_tooltip_calendar"), icon_color=c("primary", dark), data=plan.id, on_click=on_calendar),
                scale_ratio=1.2,
                dark=dark
            ),
            apply_hover_effects_to_icon_button(
                ft.IconButton(ft.Icons.DOWNLOAD, tooltip=t("plan_tooltip_export"), icon_color=c("info", dark), data=plan.id, on_click=on_export),
                scale_ratio=1.2,
                dark=dark
            ),
            apply_hover_effects_to_icon_button(
                ft.IconButton(ft.Icons.DELETE_OUTLINE, tooltip=t("plan_tooltip_delete"), icon_color=c("error", dark), data=plan.id, on_click=on_delete),
                scale_ratio=1.2,
                dark=dark
            ),
        ],
        spacing=0,
    )

    row = ft.Row([info_col, actions], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def _on_hover(e):
        if e.data == "true":
            container.shadow = card_shadow(dark, "lg")
            container.scale = 1.01
        else:
            container.shadow = card_shadow(dark, "md")
            container.scale = 1.0
        container.update()

    container = ft.Container(
        content=row,
        padding=ft.padding.only(left=0, right=SPACING["md"], top=SPACING["md"], bottom=SPACING["md"]),
        border_radius=RADIUS["lg"],
        bgcolor=c("bg_card", dark),
        border=ft.border.only(left=ft.BorderSide(5, phase_color)),
        shadow=card_shadow(dark, "md"),
        ink=True,
        on_click=on_calendar,
        on_hover=_on_hover,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
    )
    return container
