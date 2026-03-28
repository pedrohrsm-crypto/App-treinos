"""
Testes — Métodos de Backend para Flet v3.0.0
=============================================

Cobre:
  • get_athletes_summary: agrupamento, status, ordenação
  • map_sessions_to_calendar: mapeamento datas, persistência
  • get_calendar: leitura, ficheiro inexistente
  • save_workout_override / get_workout_for_date: edição inline
  • reset_workout_override: reverter para original
  • move_workout: drag & drop entre datas
  • Templates CRUD: save, get, delete
  • Notification Engine: cenários de notificação

Executar:  pytest tests/test_flet_backend.py -v
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime, date, timedelta
from unittest.mock import patch

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from training_planner import TrainerInfo, Athlete
from training_manager import TrainingManager, TrainingRecord


# ═══════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════

@pytest.fixture
def trainer():
    return TrainerInfo(
        nome_completo="Dr. Test Runner",
        cpf="12345678909",
        cref="654321-G/RJ",
    )

@pytest.fixture
def trainer2():
    return TrainerInfo(
        nome_completo="Prof. Segundo Treinador",
        cpf="12345678909",
        cref="111222-G/SP",
    )

@pytest.fixture
def atleta_corrida(trainer):
    return Athlete(
        nome="Ana Paula", idade=28, peso=60, altura=165,
        genero="Feminino", esporte="Corrida",
        distancia_prova="10K", limiar_lactato=160,
        vo2_max=46, dias_semana=4, semanas_ate_prova=12,
        trainer=trainer,
    )

@pytest.fixture
def atleta_ciclismo(trainer):
    return Athlete(
        nome="Bruno Oliveira", idade=34, peso=78, altura=180,
        genero="Masculino", esporte="Ciclismo",
        distancia_prova="100K", limiar_lactato=170,
        vo2_max=52, dias_semana=5, semanas_ate_prova=16,
        trainer=trainer,
    )

@pytest.fixture
def manager(tmp_path):
    return TrainingManager(base_dir=str(tmp_path / "trainers"))


def _register_and_get_id(manager, trainer, atleta) -> str:
    """Helper: regista um plano e devolve o ID."""
    record = manager.register_training(trainer, atleta)
    return record.id


# ═══════════════════════════════════════════════════════════════════
# 1. GET_ATHLETES_SUMMARY
# ═══════════════════════════════════════════════════════════════════

class TestAthletesSummary:

    def test_summary_vazio_sem_planos(self, manager, trainer):
        result = manager.get_athletes_summary(trainer)
        assert result == []

    def test_summary_um_atleta(self, manager, trainer, atleta_corrida):
        manager.register_training(trainer, atleta_corrida)
        result = manager.get_athletes_summary(trainer)

        assert len(result) == 1
        summary = result[0]
        assert summary['athlete_name'] == "Ana Paula"
        assert summary['latest_sport'] == "Corrida"
        assert summary['total_weeks'] == 12
        assert summary['current_week'] >= 1
        assert summary['status'] in ('active', 'completed')
        assert len(summary['plans']) == 1

    def test_summary_multiplos_atletas(self, manager, trainer, atleta_corrida, atleta_ciclismo):
        manager.register_training(trainer, atleta_corrida)
        time.sleep(1.1)
        manager.register_training(trainer, atleta_ciclismo)

        result = manager.get_athletes_summary(trainer)
        assert len(result) == 2
        nomes = {s['athlete_name'] for s in result}
        assert nomes == {"Ana Paula", "Bruno Oliveira"}

    def test_summary_dois_planos_mesmo_atleta(self, manager, trainer, atleta_corrida):
        manager.register_training(trainer, atleta_corrida)
        time.sleep(1.1)
        manager.register_training(trainer, atleta_corrida)

        result = manager.get_athletes_summary(trainer)
        assert len(result) == 1
        assert len(result[0]['plans']) == 2
        assert result[0]['total_weeks'] == 24  # 12 + 12

    def test_summary_athlete_data_presente(self, manager, trainer, atleta_corrida):
        manager.register_training(trainer, atleta_corrida)
        result = manager.get_athletes_summary(trainer)

        data = result[0]['athlete_data']
        assert data['nome'] == "Ana Paula"
        assert data['peso'] == 60

    def test_summary_isolamento_treinadores(self, manager, trainer, trainer2, atleta_corrida, atleta_ciclismo):
        manager.register_training(trainer, atleta_corrida)
        # Criar atleta para trainer2
        from dataclasses import replace
        atleta_t2 = replace(atleta_ciclismo, trainer=trainer2)
        manager.register_training(trainer2, atleta_t2)

        result_t1 = manager.get_athletes_summary(trainer)
        result_t2 = manager.get_athletes_summary(trainer2)
        assert len(result_t1) == 1
        assert result_t1[0]['athlete_name'] == "Ana Paula"
        assert len(result_t2) == 1
        assert result_t2[0]['athlete_name'] == "Bruno Oliveira"


# ═══════════════════════════════════════════════════════════════════
# 2. CALENDÁRIO (map, get, movimentação)
# ═══════════════════════════════════════════════════════════════════

class TestCalendar:

    def _sample_sessions(self):
        """Sessões de exemplo para testes de calendário."""
        return [
            {"dia": "Segunda", "modalidade": "Corrida", "duracao": "45min",
             "tipo": "Base", "zona": "Z2", "descricao": "Corrida base",
             "semana": 1, "fase": "Base"},
            {"dia": "Quarta", "modalidade": "Corrida", "duracao": "60min",
             "tipo": "Intervalado", "zona": "Z4", "descricao": "Intervalos 800m",
             "semana": 1, "fase": "Base"},
            {"dia": "Sexta", "modalidade": "Corrida", "duracao": "30min",
             "tipo": "Recuperação", "zona": "Z1", "descricao": "Trote leve",
             "semana": 1, "fase": "Base"},
            {"dia": "Segunda", "modalidade": "Corrida", "duracao": "50min",
             "tipo": "Tempo", "zona": "Z3", "descricao": "Corrida tempo",
             "semana": 2, "fase": "Build"},
        ]

    def test_map_sessions_cria_calendario(self, manager, trainer, atleta_corrida):
        pid = _register_and_get_id(manager, trainer, atleta_corrida)
        sessions = self._sample_sessions()
        cal = manager.map_sessions_to_calendar(trainer, pid, sessions, "2025-01-06")  # Monday

        assert isinstance(cal, dict)
        assert len(cal) > 0
        # Semana 1: Seg 6/Jan, Qua 8/Jan, Sex 10/Jan
        assert "2025-01-06" in cal
        assert "2025-01-08" in cal
        assert "2025-01-10" in cal
        # Semana 2: Seg 13/Jan
        assert "2025-01-13" in cal
        assert len(cal["2025-01-06"]) == 1
        assert cal["2025-01-06"][0]["tipo"] == "Base"

    def test_map_sessions_persiste_ficheiro(self, manager, trainer, atleta_corrida):
        pid = _register_and_get_id(manager, trainer, atleta_corrida)
        sessions = self._sample_sessions()[:1]
        manager.map_sessions_to_calendar(trainer, pid, sessions, "2025-01-06")

        cal_path = manager._get_calendar_path(trainer, pid)
        assert cal_path.exists()
        with open(cal_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert "2025-01-06" in data

    def test_get_calendar_vazio_por_omissao(self, manager, trainer, atleta_corrida):
        pid = _register_and_get_id(manager, trainer, atleta_corrida)
        cal = manager.get_calendar(trainer, pid)
        assert cal == {}

    def test_get_calendar_apos_mapeamento(self, manager, trainer, atleta_corrida):
        pid = _register_and_get_id(manager, trainer, atleta_corrida)
        sessions = self._sample_sessions()[:2]
        manager.map_sessions_to_calendar(trainer, pid, sessions, "2025-01-06")

        cal = manager.get_calendar(trainer, pid)
        assert len(cal) == 2
        assert "2025-01-06" in cal
        assert "2025-01-08" in cal

    def test_move_workout_sucesso(self, manager, trainer, atleta_corrida):
        pid = _register_and_get_id(manager, trainer, atleta_corrida)
        sessions = self._sample_sessions()[:2]
        manager.map_sessions_to_calendar(trainer, pid, sessions, "2025-01-06")

        # Mover sessão de Seg para Sáb
        ok = manager.move_workout(trainer, pid, "2025-01-06", 0, "2025-01-11")
        assert ok is True

        cal = manager.get_calendar(trainer, pid)
        assert "2025-01-06" not in cal or len(cal.get("2025-01-06", [])) == 0
        assert "2025-01-11" in cal
        assert cal["2025-01-11"][0]["tipo"] == "Base"

    def test_move_workout_indice_invalido(self, manager, trainer, atleta_corrida):
        pid = _register_and_get_id(manager, trainer, atleta_corrida)
        sessions = self._sample_sessions()[:1]
        manager.map_sessions_to_calendar(trainer, pid, sessions, "2025-01-06")

        ok = manager.move_workout(trainer, pid, "2025-01-06", 5, "2025-01-11")
        assert ok is False

    def test_move_workout_data_inexistente(self, manager, trainer, atleta_corrida):
        pid = _register_and_get_id(manager, trainer, atleta_corrida)
        sessions = self._sample_sessions()[:1]
        manager.map_sessions_to_calendar(trainer, pid, sessions, "2025-01-06")

        ok = manager.move_workout(trainer, pid, "2025-12-31", 0, "2025-01-11")
        assert ok is False


# ═══════════════════════════════════════════════════════════════════
# 3. WORKOUT OVERRIDES (edição inline)
# ═══════════════════════════════════════════════════════════════════

class TestWorkoutOverrides:

    def _setup_calendar(self, manager, trainer, atleta_corrida):
        pid = _register_and_get_id(manager, trainer, atleta_corrida)
        sessions = [
            {"dia": "Segunda", "modalidade": "Corrida", "duracao": "45min",
             "tipo": "Base", "zona": "Z2", "descricao": "Corrida base",
             "semana": 1, "fase": "Base"},
            {"dia": "Segunda", "modalidade": "Corrida", "duracao": "30min",
             "tipo": "Recuperação", "zona": "Z1", "descricao": "Trote",
             "semana": 1, "fase": "Base"},
        ]
        manager.map_sessions_to_calendar(trainer, pid, sessions, "2025-01-06")
        return pid

    def test_save_e_get_override(self, manager, trainer, atleta_corrida):
        pid = self._setup_calendar(manager, trainer, atleta_corrida)

        override = {"tipo": "Fartlek", "zona": "Z3", "duracao": "50min"}
        ok = manager.save_workout_override(trainer, pid, "2025-01-06", 0, override)
        assert ok is True

        workouts = manager.get_workout_for_date(trainer, pid, "2025-01-06")
        assert len(workouts) == 2
        assert workouts[0]["tipo"] == "Fartlek"
        assert workouts[0]["zona"] == "Z3"
        assert workouts[0]["duracao"] == "50min"
        # Segundo treino inalterado
        assert workouts[1]["tipo"] == "Recuperação"

    def test_get_workout_sem_override(self, manager, trainer, atleta_corrida):
        pid = self._setup_calendar(manager, trainer, atleta_corrida)
        workouts = manager.get_workout_for_date(trainer, pid, "2025-01-06")
        assert len(workouts) == 2
        assert workouts[0]["tipo"] == "Base"

    def test_get_workout_data_vazia(self, manager, trainer, atleta_corrida):
        pid = self._setup_calendar(manager, trainer, atleta_corrida)
        workouts = manager.get_workout_for_date(trainer, pid, "2025-12-25")
        assert workouts == []

    def test_reset_override_especifico(self, manager, trainer, atleta_corrida):
        pid = self._setup_calendar(manager, trainer, atleta_corrida)

        manager.save_workout_override(trainer, pid, "2025-01-06", 0, {"tipo": "X"})
        manager.save_workout_override(trainer, pid, "2025-01-06", 1, {"tipo": "Y"})

        # Reset apenas o primeiro
        ok = manager.reset_workout_override(trainer, pid, "2025-01-06", session_index=0)
        assert ok is True

        workouts = manager.get_workout_for_date(trainer, pid, "2025-01-06")
        assert workouts[0]["tipo"] == "Base"  # voltou ao original
        assert workouts[1]["tipo"] == "Y"     # manteve override

    def test_reset_todos_overrides_do_dia(self, manager, trainer, atleta_corrida):
        pid = self._setup_calendar(manager, trainer, atleta_corrida)

        manager.save_workout_override(trainer, pid, "2025-01-06", 0, {"tipo": "X"})
        manager.save_workout_override(trainer, pid, "2025-01-06", 1, {"tipo": "Y"})

        ok = manager.reset_workout_override(trainer, pid, "2025-01-06", session_index=None)
        assert ok is True

        workouts = manager.get_workout_for_date(trainer, pid, "2025-01-06")
        assert workouts[0]["tipo"] == "Base"
        assert workouts[1]["tipo"] == "Recuperação"

    def test_reset_sem_overrides_existentes(self, manager, trainer, atleta_corrida):
        pid = self._setup_calendar(manager, trainer, atleta_corrida)
        ok = manager.reset_workout_override(trainer, pid, "2025-01-06", session_index=0)
        assert ok is True

    def test_multiple_overrides_dias_diferentes(self, manager, trainer, atleta_corrida):
        pid = _register_and_get_id(manager, trainer, atleta_corrida)
        sessions = [
            {"dia": "Segunda", "modalidade": "Corrida", "duracao": "45min",
             "tipo": "Base", "zona": "Z2", "descricao": "", "semana": 1, "fase": "Base"},
            {"dia": "Quarta", "modalidade": "Corrida", "duracao": "60min",
             "tipo": "Intervalado", "zona": "Z4", "descricao": "", "semana": 1, "fase": "Base"},
        ]
        manager.map_sessions_to_calendar(trainer, pid, sessions, "2025-01-06")

        manager.save_workout_override(trainer, pid, "2025-01-06", 0, {"tipo": "Fartlek"})
        manager.save_workout_override(trainer, pid, "2025-01-08", 0, {"tipo": "Tempo"})

        w1 = manager.get_workout_for_date(trainer, pid, "2025-01-06")
        w2 = manager.get_workout_for_date(trainer, pid, "2025-01-08")
        assert w1[0]["tipo"] == "Fartlek"
        assert w2[0]["tipo"] == "Tempo"


# ═══════════════════════════════════════════════════════════════════
# 4. TEMPLATES CRUD
# ═══════════════════════════════════════════════════════════════════

class TestTemplates:

    def _sample_template(self):
        return {
            "name": "Intervalado 800m",
            "sport": "Corrida",
            "type": "Intervalado",
            "zone": "Z4",
            "duration": "50min",
            "modality": "Corrida",
            "description": "8x800m com recuperação 2min"
        }

    def test_templates_vazio(self, manager, trainer):
        result = manager.get_templates(trainer)
        assert result == []

    def test_save_template(self, manager, trainer):
        tmpl = self._sample_template()
        ok = manager.save_template(trainer, tmpl)
        assert ok is True

        templates = manager.get_templates(trainer)
        assert len(templates) == 1
        assert templates[0]["name"] == "Intervalado 800m"
        assert "id" in templates[0]
        assert templates[0]["id"].startswith("tmpl_")
        assert "created_at" in templates[0]

    def test_save_multiplos_templates(self, manager, trainer):
        t1 = self._sample_template()
        t2 = {"name": "Base Aeróbica", "sport": "Corrida", "type": "Base",
               "zone": "Z2", "duration": "60min", "modality": "Corrida",
               "description": "Corrida longa em Z2"}
        time.sleep(1.1)  # Evitar colisão de IDs
        manager.save_template(trainer, t1)
        time.sleep(1.1)
        manager.save_template(trainer, t2)

        templates = manager.get_templates(trainer)
        assert len(templates) == 2
        nomes = {t["name"] for t in templates}
        assert nomes == {"Intervalado 800m", "Base Aeróbica"}

    def test_delete_template(self, manager, trainer):
        tmpl = self._sample_template()
        manager.save_template(trainer, tmpl)

        templates = manager.get_templates(trainer)
        tid = templates[0]["id"]

        ok = manager.delete_template(trainer, tid)
        assert ok is True

        templates_after = manager.get_templates(trainer)
        assert len(templates_after) == 0

    def test_delete_template_id_inexistente(self, manager, trainer):
        tmpl = self._sample_template()
        manager.save_template(trainer, tmpl)

        ok = manager.delete_template(trainer, "tmpl_nao_existe")
        assert ok is True  # não falha, simplesmente não encontra

        templates = manager.get_templates(trainer)
        assert len(templates) == 1  # mantém o existente

    def test_templates_isolamento_treinadores(self, manager, trainer, trainer2):
        t1 = self._sample_template()
        manager.save_template(trainer, t1)

        assert len(manager.get_templates(trainer)) == 1
        assert len(manager.get_templates(trainer2)) == 0


# ═══════════════════════════════════════════════════════════════════
# 5. NOTIFICATION ENGINE
# ═══════════════════════════════════════════════════════════════════

class TestNotificationEngine:

    def test_notificacoes_sem_treinador(self):
        from flet_app.services.notification_engine import get_pending_notifications
        result = get_pending_notifications(None)
        assert result == []

    def test_notificacoes_sem_planos(self, manager, trainer):
        """Usa um manager com base_dir temporário — trainer sem planos."""
        from flet_app.services import notification_engine

        # Substituir a instância global temporariamente
        original_tm = notification_engine.training_manager
        notification_engine.training_manager = manager

        try:
            result = notification_engine.get_pending_notifications(trainer)
            assert result == []
        finally:
            notification_engine.training_manager = original_tm

    def test_notificacao_plano_sem_calendario(self, manager, trainer, atleta_corrida):
        """Cria plano antigo sem calendário → deve gerar notificação 'info'."""
        from flet_app.services import notification_engine

        record = manager.register_training(trainer, atleta_corrida)

        # Simular plano criado há 20 dias
        plans = manager.get_trainer_plans(trainer)
        plan_data = plans[0]
        old_date = (datetime.now() - timedelta(days=20)).isoformat()
        plan_data_dict = {
            "id": plan_data.id,
            "athlete_name": plan_data.athlete_name,
            "sport": plan_data.sport,
            "distance": plan_data.distance,
            "weeks": plan_data.weeks,
            "created_at": old_date,
            "athlete_data": plan_data.athlete_data,
        }
        # Reescrever metadata.json com o plano antigo
        metadata_path = manager._get_metadata_path(trainer)
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump({"plans": [plan_data_dict]}, f, ensure_ascii=False)

        original_tm = notification_engine.training_manager
        notification_engine.training_manager = manager

        try:
            notifications = notification_engine.get_pending_notifications(trainer)
            info_notifs = [n for n in notifications if n["type"] == "info"]
            assert len(info_notifs) >= 1
            assert "calendário" in info_notifs[0]["title"].lower() or "calendário" in info_notifs[0]["detail"].lower()
        finally:
            notification_engine.training_manager = original_tm

    def test_notificacao_treino_hoje(self, manager, trainer, atleta_corrida):
        """Cria calendário com sessão hoje → deve gerar notificação 'training'."""
        from flet_app.services import notification_engine

        pid = _register_and_get_id(manager, trainer, atleta_corrida)
        today_key = date.today().isoformat()
        cal = {today_key: [{"tipo": "Base", "zona": "Z2", "duracao": "45min"}]}
        cal_path = manager._get_calendar_path(trainer, pid)
        cal_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cal_path, 'w', encoding='utf-8') as f:
            json.dump(cal, f, ensure_ascii=False)

        original_tm = notification_engine.training_manager
        notification_engine.training_manager = manager

        try:
            notifications = notification_engine.get_pending_notifications(trainer)
            training_notifs = [n for n in notifications if n["type"] == "training"]
            assert len(training_notifs) >= 1
            assert "hoje" in training_notifs[0]["title"].lower()
            assert training_notifs[0]["priority"] == 1
        finally:
            notification_engine.training_manager = original_tm

    def test_notificacoes_ordenadas_por_prioridade(self, manager, trainer, atleta_corrida):
        """Verifica que as notificações vêm ordenadas por prioridade."""
        from flet_app.services import notification_engine

        pid = _register_and_get_id(manager, trainer, atleta_corrida)

        today_key = date.today().isoformat()
        tomorrow_key = (date.today() + timedelta(days=1)).isoformat()
        cal = {
            today_key: [{"tipo": "Intervalado", "zona": "Z4", "duracao": "50min"}],
            tomorrow_key: [{"tipo": "Base", "zona": "Z2", "duracao": "45min"}],
        }
        cal_path = manager._get_calendar_path(trainer, pid)
        cal_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cal_path, 'w', encoding='utf-8') as f:
            json.dump(cal, f, ensure_ascii=False)

        original_tm = notification_engine.training_manager
        notification_engine.training_manager = manager

        try:
            notifications = notification_engine.get_pending_notifications(trainer)
            if len(notifications) >= 2:
                for i in range(len(notifications) - 1):
                    assert notifications[i]["priority"] <= notifications[i+1]["priority"]
        finally:
            notification_engine.training_manager = original_tm
