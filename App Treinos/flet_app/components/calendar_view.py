"""
Calendar View — Calendário Mensal Interativo
=============================================

Grid 7×6 mostrando treinos mapeados por dia.
Chips coloridos por zona, navegação por mês, click para editar.
Alternativa por botão ao drag & drop para acessibilidade motora.
"""

import flet as ft
from datetime import date, timedelta, datetime as dt
import calendar as cal
from i18n import t
from flet_app.theme import c, PHASE_COLORS, RADIUS
from flet_app.state import app_state
from training_manager import training_manager


# Mapa zona → cor (simplificado)
ZONE_COLORS = {
    "Z1 - Recuperação": "#68c2a6",
    "Z2 - Aeróbico": "#6885c2",
    "Z3 - Tempo": "#c27968",
    "Z4 - Limiar": "#c26868",
    "Z5 - VO2max": "#7968c2",
}

SPORT_ICON_SHORT = {
    "Corrida": ft.Icons.DIRECTIONS_RUN,
    "Ciclismo": ft.Icons.DIRECTIONS_BIKE,
    "Natação": ft.Icons.POOL,
    "Brick": ft.Icons.SYNC,
    "Multisport": ft.Icons.EMOJI_EVENTS,
}

_DAY_KEYS = [
    "calendar_day_mon", "calendar_day_tue", "calendar_day_wed",
    "calendar_day_thu", "calendar_day_fri", "calendar_day_sat", "calendar_day_sun",
]


def calendar_view_screen(page: ft.Page, route: str) -> ft.View:
    """Constrói a View do calendário mensal de um plano."""

    dark = app_state.dark_mode
    plan_id = app_state.selected_plan_id or route.rstrip("/").rsplit("/", 1)[-1]
    trainer = app_state.trainer_info()

    # Estado de navegação: ano e mês visualizados
    today = date.today()
    view_year = [today.year]
    view_month = [today.month]

    # Carregar calendário completo do plano
    calendar_data = training_manager.get_calendar(trainer, plan_id) if trainer else {}

    # ── Header do mês ────────────────────────────────────────────
    month_label = ft.Text("", size=18, weight=ft.FontWeight.BOLD, expand=True, text_align=ft.TextAlign.CENTER)

    def _update_month_label():
        month_key = f"calendar_month_{view_month[0]}"
        month_label.value = f"{t(month_key)} {view_year[0]}"

    def _prev_month(_):
        if view_month[0] == 1:
            view_month[0] = 12
            view_year[0] -= 1
        else:
            view_month[0] -= 1
        _rebuild_grid()
        page.update()

    def _next_month(_):
        if view_month[0] == 12:
            view_month[0] = 1
            view_year[0] += 1
        else:
            view_month[0] += 1
        _rebuild_grid()
        page.update()

    def _go_today(_):
        view_year[0] = today.year
        view_month[0] = today.month
        _rebuild_grid()
        page.update()

    month_nav = ft.Row(
        [
            ft.IconButton(ft.Icons.CHEVRON_LEFT, on_click=_prev_month),
            month_label,
            ft.IconButton(ft.Icons.CHEVRON_RIGHT, on_click=_next_month),
            ft.TextButton(t("calendar_btn_today"), on_click=_go_today),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # ── Grid do calendário ───────────────────────────────────────
    grid_column = ft.Column(spacing=2)

    def _rebuild_grid():
        _update_month_label()
        grid_column.controls.clear()

        # Header dos dias da semana
        header_row = ft.Row(
            [ft.Container(ft.Text(t(dk), size=12, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER, color=c("text_secondary", dark)), width=90, alignment=ft.Alignment.CENTER) for dk in _DAY_KEYS],
            spacing=2,
        )
        grid_column.controls.append(header_row)

        # Calcular semanas do mês
        first_day = date(view_year[0], view_month[0], 1)
        # weekday(): Monday=0
        start_weekday = first_day.weekday()
        days_in_month = cal.monthrange(view_year[0], view_month[0])[1]

        # Preencher a partir da segunda anterior ao dia 1
        current = first_day - timedelta(days=start_weekday)

        for _ in range(6):  # máximo 6 semanas
            row_controls = []
            week_has_current_month = False
            for _ in range(7):
                is_current_month = current.month == view_month[0] and current.year == view_year[0]
                if is_current_month:
                    week_has_current_month = True
                cell = _build_day_cell(current, is_current_month)
                row_controls.append(cell)
                current += timedelta(days=1)

            if not week_has_current_month:
                break
            grid_column.controls.append(ft.Row(row_controls, spacing=2))

    # ── Drag & Drop state ───────────────────────────────────────
    undo_state = {"from": None, "to": None, "index": None}

    def _do_move(from_date: str, session_index: int, to_date: str):
        """Executa a movimentação (usada por drag&drop e pelo botão mover)."""
        if from_date == to_date:
            return
        ok = training_manager.move_workout(
            trainer, plan_id,
            from_date=from_date,
            session_index=session_index,
            to_date=to_date,
        )
        if ok:
            undo_state["from"] = from_date
            undo_state["to"] = to_date
            undo_state["index"] = session_index
            _refresh_calendar()

            def _undo(e):
                target_sessions = calendar_data.get(undo_state["to"], [])
                if target_sessions:
                    training_manager.move_workout(
                        trainer, plan_id,
                        from_date=undo_state["to"],
                        session_index=len(target_sessions) - 1,
                        to_date=undo_state["from"],
                    )
                    _refresh_calendar()

            page.open(ft.SnackBar(
                ft.Text(t("calendar_moved")),
                action=t("calendar_undo"),
                on_action=_undo,
                duration=5000,
                bgcolor=c("info", dark),
            ))
            page.update()

    def _on_drag_accept(e):
        """Callback quando um chip é dropado numa célula destino."""
        src = page.get_control(e.src_id)
        if not src or not hasattr(src, "data"):
            return
        drag_data = src.data  # {"date": str, "session_index": int}
        target_date = e.control.data  # date_key da célula destino

        if not drag_data or not target_date:
            return
        _do_move(drag_data["date"], drag_data["session_index"], target_date)

    def _build_day_cell(d: date, is_current_month: bool) -> ft.Container:
        key = d.isoformat()
        sessions = calendar_data.get(key, [])
        is_today = d == today

        # Cor do número do dia
        if not is_current_month:
            day_color = c("text_disabled", dark)
            bg = c("bg_secondary", dark)
        elif is_today:
            day_color = c("text_light", dark)
            bg = c("primary", dark)
        elif sessions:
            day_color = c("text_primary", dark)
            bg = c("bg_card", dark)
        else:
            day_color = c("text_secondary", dark)
            bg = c("bg_tertiary", dark)

        # Mini chips para sessões (máx 3 visíveis) — wrapped in Draggable
        chips = []
        for i, s in enumerate(sessions[:3]):
            zona = s.get("zona", "")
            zone_color = ZONE_COLORS.get(zona, c("primary", dark))
            modalidade = s.get("modalidade", "")
            icon_name = SPORT_ICON_SHORT.get(modalidade, ft.Icons.ASSIGNMENT)
            tipo_short = s.get("tipo", "")[:4]

            # Chip com tamanho acessível (mín ~36px de altura)
            chip_content = ft.Container(
                content=ft.Row([ft.Icon(icon_name, size=11, color=c("text_light")), ft.Text(tipo_short, size=10, color=c("text_light"))], spacing=2, tight=True),
                bgcolor=zone_color,
                border_radius=4,
                padding=ft.padding.symmetric(horizontal=4, vertical=3),
            )

            if is_current_month:
                # Wrap in Draggable for drag & drop
                draggable = ft.Draggable(
                    content=chip_content,
                    content_feedback=ft.Container(
                        content=ft.Row([ft.Icon(icon_name, size=13, color=c("text_light")), ft.Text(tipo_short, size=12, color=c("text_light"))], spacing=2, tight=True),
                        bgcolor=zone_color,
                        border_radius=6,
                        padding=ft.padding.symmetric(horizontal=6, vertical=4),
                        opacity=0.8,
                    ),
                    data={"date": key, "session_index": i},
                )
                chips.append(draggable)
            else:
                chips.append(chip_content)

        if len(sessions) > 3:
            chips.append(ft.Text(f"+{len(sessions) - 3}", size=10, color=c("text_secondary", dark)))

        cell_content = ft.Column(
            [
                ft.Text(str(d.day), size=12, weight=ft.FontWeight.BOLD if is_today else ft.FontWeight.NORMAL, color=day_color),
                *chips,
            ],
            spacing=1,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        def _on_cell_click(e, date_key=key, sess=sessions):
            if sess and is_current_month:
                _open_day_detail(date_key, sess)

        # Wrap cell in DragTarget for drop reception
        if is_current_month:
            cell_container = ft.DragTarget(
                content=ft.Container(
                    content=cell_content,
                    width=90,
                    height=80,
                    alignment=ft.Alignment.TOP_CENTER,
                    border_radius=8,
                    bgcolor=bg,
                    border=ft.border.all(2, c("primary", dark)) if is_today else ft.border.all(1, c("border_light", dark)),
                    padding=ft.padding.only(top=4),
                    on_click=_on_cell_click if sessions else None,
                    ink=bool(sessions),
                ),
                data=key,
                on_accept=_on_drag_accept,
            )
        else:
            cell_container = ft.Container(
                content=cell_content,
                width=90,
                height=80,
                alignment=ft.Alignment.TOP_CENTER,
                border_radius=8,
                bgcolor=bg,
                padding=ft.padding.only(top=4),
            )

        return cell_container

    # ── Detalhe do dia (BottomSheet) ─────────────────────────────
    def _open_day_detail(date_key: str, sessions: list):
        """Abre painel inferior com sessões do dia."""
        # Carregar com overrides aplicados
        full_sessions = training_manager.get_workout_for_date(trainer, plan_id, date_key) if trainer else sessions

        session_cards = []
        for i, s in enumerate(full_sessions):
            zona = s.get("zona", "")
            zone_color = ZONE_COLORS.get(zona, c("primary", dark))
            modalidade = s.get("modalidade", "")
            icon_name = SPORT_ICON_SHORT.get(modalidade, ft.Icons.ASSIGNMENT)

            # Botão "Mover para…" (alternativa acessível a drag & drop)
            def _show_move_dialog(e, src_date=date_key, src_index=i):
                move_date_field = ft.TextField(
                    label=t("calendar_move_date_label"),
                    hint_text="YYYY-MM-DD",
                    width=220,
                )
                status_text = ft.Text("", size=12)

                def _do_move_btn(e2):
                    target = move_date_field.value.strip()
                    if not target:
                        return
                    try:
                        dt.strptime(target, "%Y-%m-%d")
                    except ValueError:
                        status_text.value = t("editor_copy_invalid_date")
                        status_text.color = c("error", dark)
                        page.update()
                        return
                    page.close(move_dlg)
                    _do_move(src_date, src_index, target)

                def _cancel_move(e2):
                    page.close(move_dlg)

                move_dlg = ft.AlertDialog(
                    title=ft.Text(t("calendar_move_btn")),
                    content=ft.Column([move_date_field, status_text], spacing=8, tight=True),
                    actions=[
                        ft.TextButton(t("btn_cancel"), on_click=_cancel_move),
                        ft.ElevatedButton(t("btn_confirm"), on_click=_do_move_btn, bgcolor=c("primary", dark), color=c("text_light", dark)),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                page.open(move_dlg)
                page.update()

            card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(width=4, height=40, bgcolor=zone_color, border_radius=2),
                        ft.Column([
                            ft.Row([ft.Icon(icon_name, size=14, color=zone_color), ft.Text(f"{s.get('tipo', '')} — {s.get('duracao', '')}", size=14, weight=ft.FontWeight.W_600)], spacing=4),
                            ft.Text(zona, size=12, color=c("text_secondary", dark)),
                            ft.Text(s.get("descricao", ""), size=12, color=c("text_secondary", dark), max_lines=2),
                        ], spacing=2, expand=True),
                        ft.Column([
                            ft.IconButton(
                                ft.Icons.EDIT,
                                icon_size=22,
                                tooltip=t("editor_title"),
                                data={"date": date_key, "index": i},
                                on_click=lambda e: _open_editor(e.control.data["date"], e.control.data["index"]),
                            ),
                            ft.IconButton(
                                ft.Icons.SWAP_HORIZ,
                                icon_size=22,
                                tooltip=t("calendar_move_btn"),
                                on_click=_show_move_dialog,
                            ),
                        ], spacing=0),
                    ], spacing=8),
                ]),
                bgcolor=c("bg_card", dark),
                border_radius=RADIUS["md"],
                padding=10,
                margin=ft.margin.only(bottom=6),
            )
            session_cards.append(card)

        sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column(
                    [
                    ft.Row([ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=c("primary", dark)), ft.Text(date_key, size=16, weight=ft.FontWeight.BOLD)], spacing=8),
                        ft.Text(t("calendar_sessions", count=len(full_sessions)), size=13, color=c("text_secondary", dark)),
                        ft.Divider(),
                        *session_cards,
                    ],
                    spacing=8,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=20,
                width=page.width or 400,
            ),
        )
        page.open(sheet)
        page.update()

    def _open_editor(date_key: str, session_index: int):
        """Navega para o editor inline (reutiliza workout_editor via dialog)."""
        from flet_app.components.workout_editor import open_workout_editor
        open_workout_editor(
            page=page,
            trainer=trainer,
            plan_id=plan_id,
            date_key=date_key,
            session_index=session_index,
            dark=dark,
            on_save=lambda: _refresh_calendar(),
        )

    def _refresh_calendar():
        nonlocal calendar_data
        calendar_data = training_manager.get_calendar(trainer, plan_id) if trainer else {}
        _rebuild_grid()
        page.update()

    # ── Legenda ──────────────────────────────────────────────────
    legend_row = ft.Row(
        [
            ft.Row([ft.Container(width=12, height=12, bgcolor=color, border_radius=3), ft.Text(name, size=11)], spacing=4)
            for name, color in ZONE_COLORS.items()
        ],
        spacing=12,
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # ── Build inicial ────────────────────────────────────────────
    _rebuild_grid()

    return ft.View(
        route=f"/calendar/{plan_id}",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go(f"/athlete/{app_state.selected_athlete or ''}")),
                            ft.Text(t("calendar_header"), size=18, weight=ft.FontWeight.BOLD, expand=True),
                        ]),
                        month_nav,
                        grid_column,
                        ft.Divider(),
                        legend_row,
                    ],
                    spacing=8,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                padding=ft.padding.all(12),
                expand=True,
            )
        ],
        padding=0,
        bgcolor=c("bg_secondary", dark),
    )
