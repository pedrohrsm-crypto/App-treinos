"""
Workout Editor — Modal de edição inline de treino
==================================================

AlertDialog com campos editáveis para tipo, zona, duração,
modalidade e descrição. Suporta salvar override, copiar para
outro dia, apagar sessão e reset ao treino gerado.
"""

import flet as ft
from datetime import datetime
from i18n import t
from flet_app.theme import c, RADIUS
from flet_app.state import app_state
from training_manager import training_manager


WORKOUT_TYPES = [
    "Recuperação", "Base", "Tempo", "Intervalado", "Longo",
    "Técnica", "Fartlek", "Sprint", "Long Ride", "Combinado", "Brick",
]

ZONES = ["Z1 - Recuperação", "Z2 - Aeróbico", "Z3 - Tempo", "Z4 - Limiar", "Z5 - VO2max"]

MODALITIES = ["Corrida", "Ciclismo", "Natação", "Brick", "Multisport"]


def open_workout_editor(
    page: ft.Page,
    trainer,
    plan_id: str,
    date_key: str,
    session_index: int,
    dark: bool,
    on_save=None,
):
    """
    Abre um AlertDialog para editar uma sessão de treino.

    Args:
        trainer: dict com 'cref'
        plan_id: ID do plano
        date_key: data ISO (YYYY-MM-DD)
        session_index: índice da sessão nesse dia
        dark: modo escuro
        on_save: callback chamado após salvar/reset
    """
    sessions = training_manager.get_workout_for_date(trainer, plan_id, date_key) if trainer else []
    if session_index < 0 or session_index >= len(sessions):
        page.open(ft.SnackBar(ft.Text(t("editor_session_not_found")), bgcolor=c("error", dark)))
        return

    session = sessions[session_index]

    # ── Campos editáveis ─────────────────────────────────────────
    tipo_dd = ft.Dropdown(
        label=t("editor_type_label"),
        value=session.get("tipo", ""),
        options=[ft.dropdown.Option(tp) for tp in WORKOUT_TYPES],
        expand=True,
    )
    zona_dd = ft.Dropdown(
        label=t("editor_zone_label"),
        value=session.get("zona", ""),
        options=[ft.dropdown.Option(z) for z in ZONES],
        expand=True,
    )
    duracao_field = ft.TextField(
        label=t("editor_duration_label"),
        value=session.get("duracao", ""),
        hint_text=t("editor_duration_hint"),
        expand=True,
        max_length=50,
    )
    modalidade_dd = ft.Dropdown(
        label=t("editor_modality_label"),
        value=session.get("modalidade", ""),
        options=[ft.dropdown.Option(m) for m in MODALITIES],
        expand=True,
    )
    descricao_field = ft.TextField(
        label=t("editor_notes_label"),
        value=session.get("descricao", ""),
        multiline=True,
        min_lines=2,
        max_lines=4,
        max_length=500,
    )

    status_text = ft.Text("", size=12)

    # ── Acções ───────────────────────────────────────────────────
    def _get_override_data():
        return {
            "tipo": tipo_dd.value or session.get("tipo", ""),
            "zona": zona_dd.value or session.get("zona", ""),
            "duracao": duracao_field.value or session.get("duracao", ""),
            "modalidade": modalidade_dd.value or session.get("modalidade", ""),
            "descricao": descricao_field.value or session.get("descricao", ""),
        }

    def _save(e):
        ok = training_manager.save_workout_override(
            trainer, plan_id, date_key, session_index, _get_override_data()
        )
        if ok:
            page.close(dialog)
            page.open(ft.SnackBar(ft.Text(t("editor_saved")), bgcolor=c("success", dark)))
            if on_save:
                on_save()
        else:
            status_text.value = t("editor_save_error")
            status_text.color = c("error", dark)
            page.update()

    def _reset(e):
        ok = training_manager.reset_workout_override(
            trainer, plan_id, date_key, session_index
        )
        if ok:
            page.close(dialog)
            page.open(ft.SnackBar(ft.Text(t("editor_reset_msg")), bgcolor=c("info", dark)))
            if on_save:
                on_save()
        else:
            status_text.value = t("editor_reset_error")
            status_text.color = c("error", dark)
            page.update()

    def _delete(e):
        # Confirmação antes de apagar (P5-7)
        def _confirm_del(_):
            page.close(confirm_dlg)
            ok = training_manager.save_workout_override(
                trainer, plan_id, date_key, session_index,
                {"tipo": "—REMOVIDO—", "zona": "", "duracao": "0 min", "descricao": "Sessão removida pelo treinador.", "modalidade": ""},
            )
            if ok:
                page.close(dialog)
                page.open(ft.SnackBar(ft.Text(t("editor_deleted_msg")), bgcolor=c("warning", dark)))
                if on_save:
                    on_save()

        def _cancel_del(_):
            page.close(confirm_dlg)

        confirm_dlg = ft.AlertDialog(
            title=ft.Text(t("confirm_delete_session_title")),
            content=ft.Text(t("confirm_delete_session_body")),
            actions=[
                ft.TextButton(t("btn_cancel"), on_click=_cancel_del),
                ft.ElevatedButton(t("btn_delete"), icon=ft.Icons.DELETE, bgcolor=c("error", dark), color=c("text_light", dark), on_click=_confirm_del),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(confirm_dlg)
        page.update()

    def _cancel(e):
        page.close(dialog)

    # ── Copiar para outro dia ────────────────────────────────────
    copy_date_field = ft.TextField(label=t("editor_copy_label"), width=220, visible=False)
    copy_status = ft.Text("", size=12, visible=False)
    copy_btn_confirm = ft.TextButton(t("editor_copy_confirm"), visible=False, on_click=lambda e: _do_copy())
    copy_row = ft.Row([copy_date_field, copy_btn_confirm], spacing=8)

    def _show_copy(e):
        copy_date_field.visible = True
        copy_btn_confirm.visible = True
        copy_status.visible = True
        page.update()

    def _do_copy():
        target = copy_date_field.value.strip()
        if not target:
            return
        # Validação do formato de data (P6-4)
        try:
            datetime.strptime(target, "%Y-%m-%d")
        except ValueError:
            copy_status.value = t("editor_copy_invalid_date")
            copy_status.color = c("error", dark)
            page.update()
            return

        # Find next available index on target day
        target_sessions = training_manager.get_workout_for_date(trainer, plan_id, target)
        new_index = len(target_sessions)
        ok = training_manager.save_workout_override(trainer, plan_id, target, new_index, _get_override_data())
        if ok:
            page.close(dialog)
            page.open(ft.SnackBar(ft.Text(t("editor_copied_msg", date=target)), bgcolor=c("success", dark)))
            if on_save:
                on_save()

    # ── Preview badge ────────────────────────────────────────────
    zone_colors = {
        "Z1 - Recuperação": "#68c2a6",
        "Z2 - Aeróbico": "#6885c2",
        "Z3 - Tempo": "#c27968",
        "Z4 - Limiar": "#c26868",
        "Z5 - VO2max": "#7968c2",
    }

    preview_badge = ft.Container(
        content=ft.Text("Preview", size=11, color=c("text_light")),
        bgcolor=zone_colors.get(session.get("zona", ""), c("primary", dark)),
        border_radius=6,
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )

    def _update_preview(e=None):
        zona_val = zona_dd.value or ""
        preview_badge.bgcolor = zone_colors.get(zona_val, c("primary", dark))
        tipo_val = tipo_dd.value or ""
        preview_badge.content = ft.Text(f"{tipo_val[:3]} — {zona_val}", size=11, color=c("text_light"))
        page.update()

    tipo_dd.on_change = _update_preview
    zona_dd.on_change = _update_preview

    # ── Dialog ───────────────────────────────────────────────────
    dialog = ft.AlertDialog(
        title=ft.Row([ft.Icon(ft.Icons.EDIT, size=20), ft.Text(t("editor_header", date=date_key))], spacing=8),
        content=ft.Container(
            content=ft.Column(
                [
                    preview_badge,
                    ft.Row([tipo_dd, zona_dd], spacing=8),
                    ft.Row([duracao_field, modalidade_dd], spacing=8),
                    descricao_field,
                    copy_row,
                    copy_status,
                    status_text,
                ],
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
            ),
            width=480,
            height=400,
        ),
        actions=[
            ft.TextButton(t("btn_cancel"), on_click=_cancel),
            ft.TextButton(t("editor_copy_btn"), icon=ft.Icons.CONTENT_COPY, on_click=_show_copy),
            ft.TextButton(t("editor_reset_btn"), icon=ft.Icons.RESTART_ALT, on_click=_reset),
            ft.TextButton(t("editor_delete_btn"), icon=ft.Icons.DELETE_OUTLINE, on_click=_delete),
            ft.ElevatedButton(t("editor_save"), icon=ft.Icons.SAVE, on_click=_save, bgcolor=c("primary", dark), color=c("text_light", dark)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.open(dialog)
    page.update()
