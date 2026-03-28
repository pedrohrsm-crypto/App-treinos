"""
Training Wizard — Criação de plano passo a passo
=================================================

Stepper de 6 etapas: Atleta → Desporto → Período → Distância/Fisio
→ Disponibilidade → Revisão + Gerar plano.
"""

import flet as ft
from datetime import datetime
import math
from i18n import t
from flet_app.theme import c, SPORT_COLORS
from flet_app.state import app_state
from training_planner import Athlete, TrainerInfo, TrainingPlanGenerator, calcular_semanas_ate_prova
from training_manager import training_manager


# Distâncias por desporto (espelho de training_planner.py L1527)
DISTANCES = {
    "Corrida": ["5K", "10K", "Meia Maratona", "Maratona"],
    "Ciclismo": ["40K", "80K", "160K"],
    "Natação": ["1500m", "3000m", "5000m"],
    "Triathlon": ["Sprint", "Olímpico", "Meio Ironman", "Ironman"],
    "Duathlon (Natação+Corrida)": ["Aquathlon Sprint", "Aquathlon Olímpico", "Aquathlon Longo"],
    "Duathlon (Ciclismo+Corrida)": ["Duathlon Sprint", "Duathlon Olímpico", "Duathlon Longo", "Duathlon Ironman"],
}

SPORT_EMOJIS = {
    "Corrida": "🏃",
    "Ciclismo": "🚴",
    "Natação": "🏊",
    "Triathlon": "🏅",
    "Duathlon (Natação+Corrida)": "🏊🏃",
    "Duathlon (Ciclismo+Corrida)": "🚴🏃",
}

HEALTH_TYPES = {
    1: "Ortopédico",
    2: "Asma / Respiratório",
    3: "Diabetes",
    4: "Hipertensão",
    5: "Outro",
}


def training_wizard_view(page: ft.Page, route: str) -> ft.View:
    """Constrói a View do wizard de criação de treino."""

    dark = app_state.dark_mode
    current_step = [0]  # mutable ref

    # ── Estado do formulário ─────────────────────────────────────
    form = {
        "nome": app_state.selected_athlete or "",
        "idade": "",
        "peso": "",
        "altura": "",
        "genero": "masculino",
        "esporte": "",
        "distancia": "",
        "limiar_lactato": "",
        "vo2_max": "",
        "dias_semana": 5,
        "semanas_ate_prova": "",
        "data_prova": "",
        "fase_menstrual": None,
        "problemas_saude": [],
    }

    error_text = ft.Text("", color=c("error", dark), size=13)

    # ═══════════════════════════════════════════════════════════════
    # STEP 1 — Dados do Atleta
    # ═══════════════════════════════════════════════════════════════
    nome_field = ft.TextField(label="Nome completo", value=form["nome"], autofocus=True)
    idade_field = ft.TextField(label="Idade", keyboard_type=ft.KeyboardType.NUMBER, width=100)
    peso_field = ft.TextField(label="Peso (kg)", keyboard_type=ft.KeyboardType.NUMBER, width=120)
    altura_field = ft.TextField(label="Altura (cm)", keyboard_type=ft.KeyboardType.NUMBER, width=120)
    genero_dd = ft.Dropdown(
        label="Género",
        width=160,
        value="masculino",
        options=[ft.dropdown.Option("masculino", "Masculino"), ft.dropdown.Option("feminino", "Feminino")],
    )

    # Ciclo menstrual (visível apenas se feminino)
    fase_dd = ft.Dropdown(
        label="Fase do ciclo menstrual (opcional)",
        width=280,
        options=[
            ft.dropdown.Option("", "Não informar"),
            ft.dropdown.Option("menstrual", "Menstrual"),
            ft.dropdown.Option("folicular", "Folicular"),
            ft.dropdown.Option("ovulatoria", "Ovulatória"),
            ft.dropdown.Option("lutea", "Lútea"),
        ],
        visible=False,
    )

    def _on_genero_change(e):
        fase_dd.visible = genero_dd.value == "feminino"
        page.update()

    genero_dd.on_change = _on_genero_change

    step1_content = ft.Column(
        [
            ft.Text("👤 Dados do Atleta", size=18, weight=ft.FontWeight.BOLD),
            nome_field,
            ft.Row([idade_field, peso_field, altura_field], spacing=12),
            ft.Row([genero_dd, fase_dd], spacing=12),
        ],
        spacing=12,
    )

    # ═══════════════════════════════════════════════════════════════
    # STEP 2 — Seleção de Desporto
    # ═══════════════════════════════════════════════════════════════
    sport_selection = [None]

    def _sport_cards():
        cards = []
        for sport, emoji in SPORT_EMOJIS.items():
            color = SPORT_COLORS.get(sport, c("primary", dark))

            def _select(e, s=sport):
                sport_selection[0] = s
                form["esporte"] = s
                # Atualizar visual de seleção
                for ctrl in sport_grid.controls:
                    ctrl.border = None
                e.control.border = ft.border.all(3, c("primary", dark))
                # Atualizar distâncias
                _update_distance_options(s)
                page.update()

            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(emoji, size=36),
                        ft.Text(sport, size=13, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                ),
                width=130,
                height=100,
                alignment=ft.alignment.center,
                border_radius=12,
                bgcolor=color + "18",
                on_click=_select,
                ink=True,
            )
            cards.append(card)
        return cards

    sport_grid = ft.GridView(runs_count=3, max_extent=150, spacing=10, run_spacing=10, child_aspect_ratio=1.3)
    sport_grid.controls = _sport_cards()

    step2_content = ft.Column(
        [
            ft.Text("🏆 Selecione o Desporto", size=18, weight=ft.FontWeight.BOLD),
            sport_grid,
        ],
        spacing=12,
    )

    # ═══════════════════════════════════════════════════════════════
    # STEP 3 — Período / Data da Prova
    # ═══════════════════════════════════════════════════════════════
    data_prova_field = ft.TextField(label="Data da prova (DD/MM/AAAA)", hint_text="Ex: 15/08/2026", width=220)
    semanas_result = ft.Text("", size=14, color=c("success", dark))

    def _calc_weeks(e):
        val = data_prova_field.value.strip()
        if not val:
            semanas_result.value = ""
            page.update()
            return
        try:
            weeks = calcular_semanas_ate_prova(val)
            if weeks > 52:
                semanas_result.value = f"⚠️ {weeks} semanas (máx 52). Será ajustado automaticamente."
                semanas_result.color = c("warning", dark)
                form["semanas_ate_prova"] = 52
            else:
                semanas_result.value = f"✅ {weeks} semanas de treinamento"
                semanas_result.color = c("success", dark)
                form["semanas_ate_prova"] = weeks
            form["data_prova"] = val
        except ValueError as ex:
            semanas_result.value = f"❌ {ex}"
            semanas_result.color = c("error", dark)
        page.update()

    data_prova_field.on_blur = _calc_weeks
    data_prova_field.on_submit = _calc_weeks

    step3_content = ft.Column(
        [
            ft.Text("📅 Período de Treinamento", size=18, weight=ft.FontWeight.BOLD),
            ft.Text("Informe a data da prova para cálculo automático das semanas.", size=13, color=c("text_secondary", dark)),
            data_prova_field,
            semanas_result,
        ],
        spacing=12,
    )

    # ═══════════════════════════════════════════════════════════════
    # STEP 4 — Distância + Fisiologia
    # ═══════════════════════════════════════════════════════════════
    dist_dd = ft.Dropdown(label="Distância da prova", width=260)
    limiar_field = ft.TextField(label="Limiar de lactato (bpm)", hint_text="100-220", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    vo2_field = ft.TextField(label="VO2 Max (ml/kg/min)", hint_text="20-90", keyboard_type=ft.KeyboardType.NUMBER, width=200)

    def _update_distance_options(sport: str):
        dists = DISTANCES.get(sport, [])
        dist_dd.options = [ft.dropdown.Option(d, d) for d in dists]
        if dists:
            dist_dd.value = dists[0]
            form["distancia"] = dists[0]

    def _on_dist_change(e):
        form["distancia"] = dist_dd.value

    dist_dd.on_change = _on_dist_change

    # Saúde
    health_section_visible = [False]
    health_list_col = ft.Column(spacing=8)

    def _toggle_health(e):
        health_section_visible[0] = not health_section_visible[0]
        health_container.visible = health_section_visible[0]
        page.update()

    health_type_dd = ft.Dropdown(
        label="Tipo",
        width=180,
        options=[ft.dropdown.Option(str(k), v) for k, v in HEALTH_TYPES.items()],
    )
    health_desc_field = ft.TextField(label="Descrição", expand=True)
    health_member_field = ft.TextField(label="Membro afetado (opcional)", width=180)

    def _add_health(e):
        if not health_type_dd.value or not health_desc_field.value:
            return
        issue = {
            "tipo": HEALTH_TYPES.get(int(health_type_dd.value), "Outro"),
            "descricao": health_desc_field.value,
            "membro_afetado": health_member_field.value or None,
        }
        form["problemas_saude"].append(issue)
        _refresh_health_list()
        health_desc_field.value = ""
        health_member_field.value = ""
        page.update()

    def _remove_health(idx):
        if 0 <= idx < len(form["problemas_saude"]):
            form["problemas_saude"].pop(idx)
            _refresh_health_list()
            page.update()

    def _refresh_health_list():
        health_list_col.controls.clear()
        for i, h in enumerate(form["problemas_saude"]):
            health_list_col.controls.append(
                ft.Row([
                    ft.Text(f"• {h['tipo']}: {h['descricao']}", expand=True, size=13),
                    ft.IconButton(ft.Icons.DELETE, icon_size=16, on_click=lambda _, idx=i: _remove_health(idx)),
                ])
            )

    health_container = ft.Container(
        content=ft.Column([
            ft.Row([health_type_dd, health_desc_field], spacing=8),
            ft.Row([health_member_field, ft.ElevatedButton("Adicionar", on_click=_add_health)], spacing=8),
            health_list_col,
        ], spacing=8),
        visible=False,
        padding=ft.padding.only(top=8),
    )

    step4_content = ft.Column(
        [
            ft.Text("🎯 Distância & Fisiologia", size=18, weight=ft.FontWeight.BOLD),
            dist_dd,
            ft.Row([limiar_field, vo2_field], spacing=12),
            ft.TextButton("🏥 Adicionar problemas de saúde", on_click=_toggle_health),
            health_container,
        ],
        spacing=12,
    )

    # ═══════════════════════════════════════════════════════════════
    # STEP 5 — Disponibilidade Semanal
    # ═══════════════════════════════════════════════════════════════
    dias_label = ft.Text(f"Dias por semana: 5", size=16, weight=ft.FontWeight.W_500)

    def _on_slider(e):
        val = int(e.control.value)
        form["dias_semana"] = val
        dias_label.value = f"Dias por semana: {val}"
        page.update()

    dias_slider = ft.Slider(min=1, max=7, divisions=6, value=5, label="{value}", on_change=_on_slider, expand=True)

    step5_content = ft.Column(
        [
            ft.Text("📆 Disponibilidade Semanal", size=18, weight=ft.FontWeight.BOLD),
            ft.Text("Quantos dias por semana o atleta pode treinar?", size=13, color=c("text_secondary", dark)),
            dias_label,
            dias_slider,
        ],
        spacing=12,
    )

    # ═══════════════════════════════════════════════════════════════
    # STEP 6 — Revisão + Gerar
    # ═══════════════════════════════════════════════════════════════
    review_col = ft.Column(spacing=8)

    def _build_review():
        review_col.controls.clear()
        items = [
            ("👤 Nome", form.get("nome", "—")),
            ("📏 Idade/Peso/Altura", f"{form.get('idade', '?')} anos · {form.get('peso', '?')} kg · {form.get('altura', '?')} cm"),
            ("⚧ Género", form.get("genero", "—")),
            ("🏆 Desporto", form.get("esporte", "—")),
            ("🎯 Distância", form.get("distancia", "—")),
            ("📅 Semanas", str(form.get("semanas_ate_prova", "—"))),
            ("💓 Limiar / VO2", f"{form.get('limiar_lactato', '?')} bpm / {form.get('vo2_max', '?')} ml/kg/min"),
            ("📆 Dias/semana", str(form.get("dias_semana", "?"))),
        ]
        if form.get("fase_menstrual"):
            items.append(("🌙 Ciclo", form["fase_menstrual"]))
        if form.get("problemas_saude"):
            saude = ", ".join(h["tipo"] for h in form["problemas_saude"])
            items.append(("🏥 Saúde", saude))

        for label, value in items:
            review_col.controls.append(
                ft.Row([
                    ft.Text(label, size=13, weight=ft.FontWeight.W_600, width=160),
                    ft.Text(value, size=13),
                ])
            )

    step6_content = ft.Column(
        [
            ft.Text("📝 Revisão do Plano", size=18, weight=ft.FontWeight.BOLD),
            ft.Text("Confirme os dados antes de gerar o plano.", size=13, color=c("text_secondary", dark)),
            ft.Divider(),
            review_col,
        ],
        spacing=12,
    )

    # ═══════════════════════════════════════════════════════════════
    # STEPPER
    # ═══════════════════════════════════════════════════════════════
    steps_content = [step1_content, step2_content, step3_content, step4_content, step5_content, step6_content]
    step_titles = ["Atleta", "Desporto", "Período", "Distância", "Dias", "Revisão"]
    step_container = ft.Container(expand=True, padding=ft.padding.all(16))
    step_container.content = steps_content[0]

    # Progress indicator
    progress_row = ft.Row(spacing=4, alignment=ft.MainAxisAlignment.CENTER)

    def _build_progress():
        progress_row.controls.clear()
        for i, title in enumerate(step_titles):
            is_active = i == current_step[0]
            is_done = i < current_step[0]
            color = c("primary", dark) if is_active else (c("success", dark) if is_done else c("text_disabled", dark))
            progress_row.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.CircleAvatar(
                            content=ft.Text("✓" if is_done else str(i + 1), size=12, color="#FFF"),
                            bgcolor=color, radius=14,
                        ),
                        ft.Text(title, size=10, color=color, text_align=ft.TextAlign.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    width=60,
                    on_click=lambda _, idx=i: _go_step(idx) if idx <= current_step[0] else None,
                )
            )

    def _go_step(idx):
        current_step[0] = idx
        step_container.content = steps_content[idx]
        if idx == 5:
            _collect_form_values()
            _build_review()
        _build_progress()
        _update_buttons()
        page.update()

    def _collect_form_values():
        form["nome"] = nome_field.value or ""
        form["idade"] = idade_field.value or ""
        form["peso"] = peso_field.value or ""
        form["altura"] = altura_field.value or ""
        form["genero"] = genero_dd.value or "masculino"
        form["limiar_lactato"] = limiar_field.value or ""
        form["vo2_max"] = vo2_field.value or ""
        if genero_dd.value == "feminino" and fase_dd.value:
            form["fase_menstrual"] = fase_dd.value

    # ── Validação por step ───────────────────────────────────────
    def _validate_step(step: int) -> str | None:
        """Retorna mensagem de erro ou None se ok."""
        if step == 0:
            _collect_form_values()
            if not form["nome"] or len(form["nome"].strip()) < 2:
                return "Nome é obrigatório (mínimo 2 caracteres)."
            try:
                age = int(form["idade"])
                if not (10 <= age <= 100):
                    return "Idade deve ser entre 10 e 100."
            except (ValueError, TypeError):
                return "Idade inválida."
            try:
                w = float(form["peso"])
                if not (30 <= w <= 250):
                    return "Peso deve ser entre 30 e 250 kg."
            except (ValueError, TypeError):
                return "Peso inválido."
            try:
                h = float(form["altura"])
                if not (100 <= h <= 250):
                    return "Altura deve ser entre 100 e 250 cm."
            except (ValueError, TypeError):
                return "Altura inválida."
        elif step == 1:
            if not form["esporte"]:
                return "Selecione um desporto."
        elif step == 2:
            if not form.get("semanas_ate_prova"):
                return "Informe a data da prova."
            try:
                weeks = int(form["semanas_ate_prova"])
                if weeks < 1:
                    return "Semanas devem ser ≥ 1."
            except (ValueError, TypeError):
                return "Número de semanas inválido."
        elif step == 3:
            if not form.get("distancia"):
                return "Selecione uma distância."
            try:
                lt = float(form["limiar_lactato"])
                if not (100 <= lt <= 220):
                    return "Limiar de lactato deve ser entre 100 e 220 bpm."
            except (ValueError, TypeError):
                return "Limiar de lactato inválido."
            try:
                vo2 = float(form["vo2_max"])
                if not (20 <= vo2 <= 90):
                    return "VO2 Max deve ser entre 20 e 90."
            except (ValueError, TypeError):
                return "VO2 Max inválido."
        return None

    # ── Navegação ────────────────────────────────────────────────
    btn_back = ft.OutlinedButton("Voltar", icon=ft.Icons.ARROW_BACK, on_click=lambda _: _prev())
    btn_next = ft.ElevatedButton("Próximo", icon=ft.Icons.ARROW_FORWARD, on_click=lambda _: _next())
    btn_generate = ft.ElevatedButton(
        "🚀 Gerar Plano",
        bgcolor=c("success", dark),
        color=c("text_light", dark),
        on_click=lambda _: _generate(),
    )

    bottom_row = ft.Row(
        [btn_back, error_text, btn_next, btn_generate],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    def _update_buttons():
        btn_back.visible = current_step[0] > 0
        btn_next.visible = current_step[0] < 5
        btn_generate.visible = current_step[0] == 5
        error_text.value = ""

    def _prev():
        if current_step[0] > 0:
            _go_step(current_step[0] - 1)

    def _next():
        err = _validate_step(current_step[0])
        if err:
            error_text.value = err
            page.update()
            return
        if current_step[0] < 5:
            _go_step(current_step[0] + 1)

    def _generate():
        _collect_form_values()
        error_text.value = ""
        try:
            # Build TrainerInfo
            trainer_info = TrainerInfo(
                nome_completo=app_state.trainer_name or "Treinador",
                cpf=app_state.user.get("cpf", "") if app_state.user else "",
                cref=app_state.trainer_cref or "",
            )

            # Build health issues
            from training_planner import HealthIssue
            health_issues = []
            for h in form["problemas_saude"]:
                health_issues.append(HealthIssue(
                    tipo=h["tipo"],
                    descricao=h["descricao"],
                    membro_afetado=h.get("membro_afetado"),
                ))

            # Build Athlete
            athlete = Athlete(
                nome=form["nome"].strip(),
                idade=int(form["idade"]),
                peso=float(form["peso"]),
                altura=float(form["altura"]),
                esporte=form["esporte"],
                dias_semana=form["dias_semana"],
                distancia_prova=form["distancia"],
                limiar_lactato=float(form["limiar_lactato"]),
                vo2_max=float(form["vo2_max"]),
                genero=form["genero"],
                trainer=trainer_info,
                semanas_ate_prova=int(form["semanas_ate_prova"]),
                problemas_saude=health_issues,
                fase_menstrual=form.get("fase_menstrual") or None,
            )

            # Generate plan
            generator = TrainingPlanGenerator(athlete)
            full_plan = generator.get_full_training_plan()

            # Register via training_manager
            record = training_manager.register_training(trainer_info, athlete)

            # Map to calendar
            training_manager.map_sessions_to_calendar(
                trainer_info, record.id, full_plan,
                datetime.now().strftime("%Y-%m-%d"),
            )

            page.open(ft.SnackBar(
                ft.Text(f"✅ Plano criado com sucesso! ({len(full_plan)} sessões)"),
                bgcolor=c("success", dark),
            ))
            # Navigate to athlete dashboard
            app_state.selected_athlete = athlete.nome
            page.go(f"/athlete/{athlete.nome}")

        except Exception as ex:
            error_text.value = f"Erro: {ex}"
            page.update()

    # ── Init ─────────────────────────────────────────────────────
    _build_progress()
    _update_buttons()

    # Pre-fill athlete name if coming from athlete dashboard
    if app_state.selected_athlete:
        nome_field.value = app_state.selected_athlete
        # Try to pre-fill from existing data
        trainer = app_state.trainer_info()
        if trainer:
            plans = training_manager.get_trainer_plans(trainer)
            for p in plans:
                if p.athlete_name == app_state.selected_athlete:
                    data = p.athlete_data or {}
                    if data.get("idade"):
                        idade_field.value = str(data["idade"])
                    if data.get("peso"):
                        peso_field.value = str(data["peso"])
                    if data.get("altura"):
                        altura_field.value = str(data["altura"])
                    if data.get("genero"):
                        genero_dd.value = data["genero"]
                        fase_dd.visible = data["genero"] == "feminino"
                    break

    return ft.View(
        route="/wizard",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        # Top bar
                        ft.Row(
                            [
                                ft.IconButton(ft.Icons.CLOSE, on_click=lambda _: page.go("/dashboard")),
                                ft.Text("Novo Plano de Treino", size=18, weight=ft.FontWeight.BOLD, expand=True),
                            ],
                        ),
                        progress_row,
                        ft.Divider(),
                        step_container,
                        ft.Divider(),
                        bottom_row,
                    ],
                    spacing=8,
                    expand=True,
                ),
                padding=ft.padding.all(16),
                expand=True,
            )
        ],
        padding=0,
        bgcolor=c("bg_secondary", dark),
    )
