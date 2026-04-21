"""
Testes Avançados — Inserção de Dados, Dashboards e Novas Funcionalidades
=========================================================================

Cobre:
  • TrainingManager: inserção, listagem, estatísticas, changelog, remoção
  • Navegação: alternância de dashboards (Progress, Fitness)
  • i18n: traduções nos 3 idiomas
  • Modo Escuro: toggle e persistência de cores
  • Fitness Connectors: modelos, normalização de desportos, registo
  • Versionamento semântico

Executar:  pytest tests/test_funcionalidades.py -v
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import asdict

import pytest

# Garantir path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from training_planner import TrainerInfo, Athlete
from training_manager import TrainingManager, TrainingRecord, ChangeLogEntry
from i18n import t, set_language, get_language, SUPPORTED_LANGUAGES
from fitness_connectors import (
    ActivitySummary,
    StravaConnector,
    GarminConnector,
    FitnessConnector,
    CONNECTORS,
    _STRAVA_SPORT_MAP,
)
from app_treinos.version import __version__


# ═══════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════

@pytest.fixture
def trainer():
    return TrainerInfo(
        nome_completo="Dr. Mariana Costa Lima",
        cpf="12345678909",
        cref="654321-G/RJ",
    )


@pytest.fixture
def trainer2():
    """Segundo treinador para testar isolamento."""
    return TrainerInfo(
        nome_completo="Prof. Roberto Almeida Souza",
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
def atleta_natacao(trainer):
    return Athlete(
        nome="Carolina Dias", idade=22, peso=58, altura=168,
        genero="Feminino", esporte="Natação",
        distancia_prova="1500m", limiar_lactato=155,
        vo2_max=44, dias_semana=5, semanas_ate_prova=10,
        trainer=trainer,
    )


@pytest.fixture
def manager(tmp_path):
    """TrainingManager com diretório temporário isolado."""
    return TrainingManager(base_dir=str(tmp_path / "trainers"))


@pytest.fixture(autouse=True)
def reset_language():
    """Restaura idioma para PT-BR antes de cada teste."""
    set_language("pt")
    yield
    set_language("pt")


# ═══════════════════════════════════════════════════════════════════
# 1. INSERÇÃO DE DADOS — TrainingManager
# ═══════════════════════════════════════════════════════════════════

class TestInsercaoDados:
    """Regista treinos e verifica persistência."""

    def test_registar_treino_corrida(self, manager, trainer, atleta_corrida):
        record = manager.register_training(trainer, atleta_corrida)
        assert isinstance(record, TrainingRecord)
        assert record.athlete_name == "Ana Paula"
        assert record.sport == "Corrida"
        assert record.distance == "10K"
        assert record.weeks == 12

    def test_registar_treino_ciclismo(self, manager, trainer, atleta_ciclismo):
        record = manager.register_training(trainer, atleta_ciclismo)
        assert record.sport == "Ciclismo"
        assert record.distance == "100K"

    def test_registar_treino_natacao(self, manager, trainer, atleta_natacao):
        record = manager.register_training(trainer, atleta_natacao)
        assert record.sport == "Natação"
        assert record.distance == "1500m"

    def test_multiplos_registos_mesmo_treinador(self, manager, trainer, atleta_corrida, atleta_ciclismo):
        r1 = manager.register_training(trainer, atleta_corrida)
        time.sleep(1.1)  # IDs têm granularidade de segundo (%Y%m%d_%H%M%S)
        r2 = manager.register_training(trainer, atleta_ciclismo)
        assert r1.id != r2.id
        plans = manager.get_trainer_plans(trainer)
        assert len(plans) == 2

    def test_dados_atleta_persistidos_em_json(self, manager, trainer, atleta_corrida):
        record = manager.register_training(trainer, atleta_corrida)
        assert record.athlete_data['nome'] == "Ana Paula"
        assert record.athlete_data['peso'] == 60
        assert record.athlete_data['altura'] == 165
        assert 'imc' in record.athlete_data

    def test_registro_com_caminhos_de_ficheiros(self, manager, trainer, atleta_corrida, tmp_path):
        xlsx = str(tmp_path / "treino.xlsx")
        pdf = str(tmp_path / "treino.pdf")
        record = manager.register_training(trainer, atleta_corrida, excel_path=xlsx, pdf_path=pdf)
        assert record.excel_path == xlsx
        assert record.pdf_path == pdf

    def test_metadados_salvos_no_disco(self, manager, trainer, atleta_corrida):
        manager.register_training(trainer, atleta_corrida)
        meta_path = manager._get_metadata_path(trainer)
        assert meta_path.exists()
        with open(meta_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data['plans']) == 1
        assert data['plans'][0]['athlete_name'] == "Ana Paula"


# ═══════════════════════════════════════════════════════════════════
# 2. ISOLAMENTO POR TREINADOR
# ═══════════════════════════════════════════════════════════════════

class TestIsolamentoTreinadores:
    """Cada treinador só vê os próprios planos."""

    def test_treinadores_diferentes_nao_se_veem(self, manager, trainer, trainer2, atleta_corrida):
        manager.register_training(trainer, atleta_corrida)
        plans_t1 = manager.get_trainer_plans(trainer)
        plans_t2 = manager.get_trainer_plans(trainer2)
        assert len(plans_t1) == 1
        assert len(plans_t2) == 0

    def test_treinador_nao_pode_apagar_plano_alheio(self, manager, trainer, trainer2, atleta_corrida):
        record = manager.register_training(trainer, atleta_corrida)
        success, msg = manager.delete_plan(trainer2, record.id)
        assert success is False
        # Plano original permanece
        assert manager.get_plan_by_id(trainer, record.id) is not None

    def test_verificar_propriedade(self, manager, trainer, trainer2, atleta_corrida):
        record = manager.register_training(trainer, atleta_corrida)
        assert manager.verify_ownership(trainer, record.id) is True
        assert manager.verify_ownership(trainer2, record.id) is False


# ═══════════════════════════════════════════════════════════════════
# 3. REMOÇÃO DE PLANOS
# ═══════════════════════════════════════════════════════════════════

class TestRemocaoPlanos:
    """Apagar planos e verificar consistência."""

    def test_apagar_plano_existente(self, manager, trainer, atleta_corrida):
        record = manager.register_training(trainer, atleta_corrida)
        success, msg = manager.delete_plan(trainer, record.id)
        assert success is True
        assert manager.get_plan_by_id(trainer, record.id) is None

    def test_apagar_plano_inexistente(self, manager, trainer):
        success, msg = manager.delete_plan(trainer, "plano_fantasma_9999")
        assert success is False

    def test_contagem_apos_remocao(self, manager, trainer, atleta_corrida, atleta_ciclismo):
        r1 = manager.register_training(trainer, atleta_corrida)
        time.sleep(0.01)
        r2 = manager.register_training(trainer, atleta_ciclismo)
        manager.delete_plan(trainer, r1.id)
        plans = manager.get_trainer_plans(trainer)
        assert len(plans) == 1
        assert plans[0].id == r2.id


# ═══════════════════════════════════════════════════════════════════
# 4. ESTATÍSTICAS — DASHBOARD DE PROGRESSO
# ═══════════════════════════════════════════════════════════════════

class TestEstatisticas:
    """Dados que alimentam o ProgressDashboard."""

    def test_estatisticas_vazio(self, manager, trainer):
        stats = manager.get_statistics(trainer)
        assert stats['total_plans'] == 0
        assert stats['unique_athletes'] == 0
        assert stats['sports_distribution'] == {}
        assert stats['latest_plan'] is None

    def test_estatisticas_com_planos(self, manager, trainer, atleta_corrida, atleta_ciclismo, atleta_natacao):
        manager.register_training(trainer, atleta_corrida)
        time.sleep(0.01)
        manager.register_training(trainer, atleta_ciclismo)
        time.sleep(0.01)
        manager.register_training(trainer, atleta_natacao)

        stats = manager.get_statistics(trainer)
        assert stats['total_plans'] == 3
        assert stats['unique_athletes'] == 3
        assert stats['sports_distribution'] == {'Corrida': 1, 'Ciclismo': 1, 'Natação': 1}
        assert stats['latest_plan'] is not None

    def test_atletas_duplicados_contam_uma_vez(self, manager, trainer, atleta_corrida):
        manager.register_training(trainer, atleta_corrida)
        time.sleep(0.01)
        manager.register_training(trainer, atleta_corrida)
        stats = manager.get_statistics(trainer)
        assert stats['total_plans'] == 2
        assert stats['unique_athletes'] == 1

    def test_distribuicao_atualiza_apos_remocao(self, manager, trainer, atleta_corrida, atleta_ciclismo):
        r1 = manager.register_training(trainer, atleta_corrida)
        time.sleep(0.01)
        manager.register_training(trainer, atleta_ciclismo)
        manager.delete_plan(trainer, r1.id)
        stats = manager.get_statistics(trainer)
        assert stats['sports_distribution'] == {'Ciclismo': 1}
        assert stats['total_plans'] == 1


# ═══════════════════════════════════════════════════════════════════
# 5. HISTÓRICO DE ALTERAÇÕES (CHANGELOG)
# ═══════════════════════════════════════════════════════════════════

class TestChangelog:
    """Verifica que o changelog regista ações correctamente."""

    def test_changelog_vazio_inicialmente(self, manager, trainer):
        entries = manager.get_changelog(trainer)
        assert entries == []

    def test_criacao_gera_entrada(self, manager, trainer, atleta_corrida):
        manager.register_training(trainer, atleta_corrida)
        entries = manager.get_changelog(trainer)
        assert len(entries) == 1
        assert entries[0].action == 'created'
        assert 'Ana Paula' in entries[0].details

    def test_remocao_gera_entrada(self, manager, trainer, atleta_corrida):
        record = manager.register_training(trainer, atleta_corrida)
        manager.delete_plan(trainer, record.id)
        entries = manager.get_changelog(trainer)
        assert len(entries) == 2
        actions = {e.action for e in entries}
        assert 'created' in actions
        assert 'deleted' in actions

    def test_exportacao_gera_entrada(self, manager, trainer, atleta_corrida, tmp_path):
        record = manager.register_training(trainer, atleta_corrida)
        manager.update_plan_paths(trainer, record.id, excel_path=str(tmp_path / "out.xlsx"))
        entries = manager.get_changelog(trainer)
        assert any(e.action == 'exported' for e in entries)

    def test_changelog_ordenado_mais_recente_primeiro(self, manager, trainer, atleta_corrida, atleta_ciclismo):
        manager.register_training(trainer, atleta_corrida)
        time.sleep(0.01)
        manager.register_training(trainer, atleta_ciclismo)
        entries = manager.get_changelog(trainer)
        assert entries[0].timestamp >= entries[1].timestamp

    def test_changelog_limit(self, manager, trainer, atleta_corrida):
        for _ in range(5):
            manager.register_training(trainer, atleta_corrida)
            time.sleep(0.01)
        entries = manager.get_changelog(trainer, limit=3)
        assert len(entries) == 3

    def test_changelog_persistido_no_disco(self, manager, trainer, atleta_corrida):
        manager.register_training(trainer, atleta_corrida)
        path = manager._get_changelog_path(trainer)
        assert path.exists()
        with open(path, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        assert len(raw) == 1
        assert raw[0]['action'] == 'created'


# ═══════════════════════════════════════════════════════════════════
# 6. INTERNACIONALIZAÇÃO (i18n)
# ═══════════════════════════════════════════════════════════════════

class TestI18n:
    """Traduções nos 3 idiomas suportados."""

    def test_idiomas_suportados(self):
        assert SUPPORTED_LANGUAGES == ("pt", "en", "es")

    def test_idioma_padrao_portugues(self):
        assert get_language() == "pt"

    def test_alternar_para_ingles(self):
        set_language("en")
        assert get_language() == "en"
        assert t('app_name') == "Training App"

    def test_alternar_para_espanhol(self):
        set_language("es")
        assert get_language() == "es"
        assert t('app_name') == "App Entrenamientos"

    def test_idioma_invalido_ignorado(self):
        set_language("fr")
        assert get_language() == "pt"

    def test_placeholder_substituido(self):
        result = t('dashboard_greeting', name='João')
        assert 'João' in result

    def test_placeholder_em_ingles(self):
        set_language("en")
        result = t('dashboard_greeting', name='John')
        assert 'John' in result

    def test_chave_inexistente_retorna_chave(self):
        assert t('chave_que_nao_existe') == 'chave_que_nao_existe'

    # ── Chaves dos hero cards ────────────────────────────────────

    @pytest.mark.parametrize("key", [
        'card_new_plan', 'card_edit_plan', 'card_export_pdf',
        'card_progress', 'card_fitness',
    ])
    def test_todos_cards_tem_traducao_3_idiomas(self, key):
        for lang in SUPPORTED_LANGUAGES:
            set_language(lang)
            val = t(key)
            assert val != key, f"Chave '{key}' sem tradução em '{lang}'"

    # ── Chaves de fitness ────────────────────────────────────────

    @pytest.mark.parametrize("key", [
        'fitness_title', 'fitness_connected', 'fitness_not_connected',
        'fitness_strava_desc', 'fitness_connect_strava',
        'fitness_import_activities', 'fitness_garmin_desc',
        'fitness_coming_soon', 'fitness_imported_activities',
    ])
    def test_chaves_fitness_existem(self, key):
        for lang in SUPPORTED_LANGUAGES:
            set_language(lang)
            assert t(key) != key, f"'{key}' em '{lang}'"

    # ── Chaves de progresso ──────────────────────────────────────

    @pytest.mark.parametrize("key", [
        'progress_title', 'progress_plans_created', 'progress_unique_athletes',
        'progress_sports', 'progress_latest', 'progress_distribution',
        'progress_recent', 'progress_changelog', 'progress_empty',
    ])
    def test_chaves_progresso_existem(self, key):
        for lang in SUPPORTED_LANGUAGES:
            set_language(lang)
            assert t(key) != key


# ═══════════════════════════════════════════════════════════════════
# 7. MODO ESCURO
# ═══════════════════════════════════════════════════════════════════

class TestModoEscuro:
    """Toggle de tema e persistência de cores (Flet theme dicts)."""

    @pytest.fixture(autouse=True)
    def load_palettes(self):
        """Carrega paletas LIGHT e DARK do tema Flet."""
        from flet_app.theme import LIGHT, DARK, c, build_theme
        self.light = LIGHT
        self.dark = DARK
        self.c = c
        self.build_theme = build_theme
        yield

    def test_paleta_light_tem_chaves_essenciais(self):
        for key in ['primary', 'bg_primary', 'text_primary', 'bg_secondary']:
            assert key in self.light, f"Chave '{key}' ausente em LIGHT"

    def test_paleta_dark_tem_chaves_essenciais(self):
        for key in ['primary', 'bg_primary', 'text_primary', 'bg_secondary']:
            assert key in self.dark, f"Chave '{key}' ausente em DARK"

    def test_light_dark_mesmas_chaves(self):
        assert set(self.light.keys()) == set(self.dark.keys())

    def test_dark_bg_primary_correto(self):
        assert self.dark['bg_primary'] == '#1e2a30'

    def test_light_bg_primary_diferente_dark(self):
        assert self.light['bg_primary'] != self.dark['bg_primary']

    def test_cores_escuras_tem_contraste_minimo(self):
        """Cores de texto no modo escuro devem ter contraste suficiente contra bg."""
        bg = self.dark['bg_secondary']
        fg = self.dark['text_primary']
        bg_r = int(bg[1:3], 16)
        fg_r = int(fg[1:3], 16)
        assert abs(fg_r - bg_r) > 100, "Contraste insuficiente no modo escuro"

    def test_funcao_c_retorna_cor_light(self):
        assert self.c('primary', dark=False) == self.light['primary']

    def test_funcao_c_retorna_cor_dark(self):
        assert self.c('primary', dark=True) == self.dark['primary']

    def test_build_theme_retorna_ft_theme(self):
        import flet as ft
        theme = self.build_theme(dark=False)
        assert isinstance(theme, ft.Theme)


# ═══════════════════════════════════════════════════════════════════
# 8. FITNESS CONNECTORS
# ═══════════════════════════════════════════════════════════════════

class TestFitnessConnectors:
    """Testa modelos de dados e normalização de desportos."""

    def test_activity_summary_criacao(self):
        act = ActivitySummary(
            source='strava', external_id='123', name='Morning Run',
            sport='Corrida', date='2026-03-15',
            distance_km=10.5, duration_minutes=55.2,
        )
        assert act.sport == 'Corrida'
        assert act.distance_km == 10.5

    def test_activity_summary_to_dict(self):
        act = ActivitySummary(
            source='manual', external_id='1', name='Treino',
            sport='Natação', date='2026-01-01',
            distance_km=1.5, duration_minutes=30,
        )
        d = act.to_dict()
        assert isinstance(d, dict)
        assert d['source'] == 'manual'
        assert d['sport'] == 'Natação'

    def test_activity_campos_opcionais(self):
        act = ActivitySummary(
            source='strava', external_id='999', name='Test',
            sport='Ciclismo', date='2026-06-01',
            distance_km=50, duration_minutes=120,
            avg_heart_rate=145, max_heart_rate=175,
            elevation_gain_m=800, calories=1200,
        )
        assert act.avg_heart_rate == 145
        assert act.calories == 1200

    def test_strava_sport_map_corrida(self):
        assert _STRAVA_SPORT_MAP['Run'] == 'Corrida'
        assert _STRAVA_SPORT_MAP['TrailRun'] == 'Corrida'
        assert _STRAVA_SPORT_MAP['VirtualRun'] == 'Corrida'

    def test_strava_sport_map_ciclismo(self):
        assert _STRAVA_SPORT_MAP['Ride'] == 'Ciclismo'
        assert _STRAVA_SPORT_MAP['VirtualRide'] == 'Ciclismo'

    def test_strava_sport_map_natacao(self):
        assert _STRAVA_SPORT_MAP['Swim'] == 'Natação'

    def test_connectors_registry(self):
        assert 'strava' in CONNECTORS
        assert 'garmin' in CONNECTORS
        assert CONNECTORS['strava'] is StravaConnector
        assert CONNECTORS['garmin'] is GarminConnector

    def test_garmin_nao_conectado(self):
        garmin = GarminConnector()
        assert garmin.is_connected() is False
        assert garmin.get_activities() == []

    def test_strava_parse_activity(self):
        """Testa parsing de uma atividade raw Strava."""
        connector = StravaConnector("fake_id", "fake_secret")
        raw = {
            'id': 12345,
            'name': 'Corrida matinal',
            'type': 'Run',
            'distance': 10500,       # metros
            'moving_time': 3300,     # segundos
            'start_date_local': '2026-03-15T07:00:00',
            'average_heartrate': 148.5,
            'max_heartrate': 172,
            'total_elevation_gain': 120.5,
        }
        act = connector._parse_activity(raw)
        assert act.source == 'strava'
        assert act.sport == 'Corrida'
        assert act.distance_km == 10.5
        assert abs(act.duration_minutes - 55) < 0.5
        assert act.avg_heart_rate == 148.5
        assert act.elevation_gain_m == 120.5

    def test_strava_parse_sem_heartrate(self):
        connector = StravaConnector("x", "y")
        raw = {
            'id': 999, 'name': 'Pedal', 'type': 'Ride',
            'distance': 50000, 'moving_time': 7200,
            'start_date_local': '2026-01-01T10:00:00',
        }
        act = connector._parse_activity(raw)
        assert act.avg_heart_rate is None
        assert act.sport == 'Ciclismo'

    def test_strava_parse_pace(self):
        connector = StravaConnector("x", "y")
        raw = {
            'id': 1, 'name': 'Run', 'type': 'Run',
            'distance': 5000, 'moving_time': 1500,  # 25 min / 5 km = 5:00/km
            'start_date_local': '2026-06-01T08:00:00',
        }
        act = connector._parse_activity(raw)
        assert act.avg_pace_min_km == 5.0


# ═══════════════════════════════════════════════════════════════════
# 9. ALTERNÂNCIA DE DASHBOARDS (lógica de navegação)
# ═══════════════════════════════════════════════════════════════════

class TestNavegacaoDashboards:
    """Verifica que dados necessários para cada dashboard estão disponíveis."""

    def test_progress_dashboard_dados_disponiveis(self, manager, trainer, atleta_corrida):
        """Dados que o ProgressDashboard usa existem e são válidos."""
        manager.register_training(trainer, atleta_corrida)
        plans = manager.get_trainer_plans(trainer)
        stats = manager.get_statistics(trainer)
        changelog = manager.get_changelog(trainer)

        assert len(plans) > 0
        assert stats['total_plans'] == 1
        assert len(changelog) > 0
        # Campos necessários para o dashboard
        assert plans[0].athlete_name
        assert plans[0].sport
        assert plans[0].distance
        assert plans[0].weeks > 0

    def test_fitness_screen_puede_usar_strava_connector(self):
        """FitnessScreen importa e instancia StravaConnector sem erros."""
        connector = StravaConnector("test_id", "test_secret")
        assert connector.name == "strava"
        assert not connector.is_connected()

    def test_navegacao_ida_e_volta_preserva_dados(self, manager, trainer, atleta_corrida):
        """Simula navegar Progress → voltar → verificar dados intactos."""
        manager.register_training(trainer, atleta_corrida)
        # "Navegar" para Progress: buscar dados
        stats_before = manager.get_statistics(trainer)
        # "Voltar" para Dashboard: buscar novamente
        stats_after = manager.get_statistics(trainer)
        assert stats_before == stats_after

    def test_dados_consistentes_entre_dashboards(self, manager, trainer, atleta_corrida, atleta_ciclismo):
        """Estadísticas devem ser consistentes com lista de planos."""
        manager.register_training(trainer, atleta_corrida)
        time.sleep(0.01)
        manager.register_training(trainer, atleta_ciclismo)
        plans = manager.get_trainer_plans(trainer)
        stats = manager.get_statistics(trainer)
        # total_plans deve igualar len(plans)
        assert stats['total_plans'] == len(plans)
        # athletes deve igualar set de nomes
        unique = {p.athlete_name for p in plans}
        assert stats['unique_athletes'] == len(unique)


# ═══════════════════════════════════════════════════════════════════
# 10. VERSIONAMENTO
# ═══════════════════════════════════════════════════════════════════

class TestVersionamento:
    """Verifica versão semântica."""

    def test_versao_formato_semver(self):
        parts = __version__.split('.')
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

    def test_versao_atual(self):
        assert __version__ == "3.1.0"


# ═══════════════════════════════════════════════════════════════════
# 11. UPDATE DE PATHS E FLUXO COMPLETO
# ═══════════════════════════════════════════════════════════════════

class TestFluxoCompleto:
    """Simula fluxo real: criar → exportar → atualizar → listar → apagar."""

    def test_fluxo_completo_crud(self, manager, trainer, atleta_corrida, tmp_path):
        # CREATE
        record = manager.register_training(trainer, atleta_corrida)
        assert record.id
        assert record.excel_path is None

        # UPDATE (exportar)
        xlsx = str(tmp_path / "plano.xlsx")
        ok = manager.update_plan_paths(trainer, record.id, excel_path=xlsx)
        assert ok is True

        # READ
        plan = manager.get_plan_by_id(trainer, record.id)
        assert plan.excel_path == xlsx
        assert plan.last_modified is not None

        # LIST
        plans = manager.get_trainer_plans(trainer)
        assert len(plans) == 1

        # DELETE
        success, msg = manager.delete_plan(trainer, record.id)
        assert success is True
        assert manager.get_plan_by_id(trainer, record.id) is None

        # CHANGELOG tem todas as ações
        entries = manager.get_changelog(trainer)
        actions = [e.action for e in entries]
        assert 'created' in actions
        assert 'exported' in actions
        assert 'deleted' in actions


# ═══════════════════════════════════════════════════════════════════
# 12. EDGE CASES
# ═══════════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Casos extremos e validações de segurança."""

    def test_trainer_none_levanta_erro(self, manager):
        with pytest.raises(ValueError, match="None"):
            manager._get_trainer_id(None)

    def test_cref_vazio_levanta_erro(self, manager):
        with pytest.raises(ValueError, match="vazio"):
            manager._get_trainer_id({'cref': ''})

    def test_activity_distancia_zero(self):
        connector = StravaConnector("x", "y")
        raw = {
            'id': 1, 'name': 'Stretching', 'type': 'Run',
            'distance': 0, 'moving_time': 300,
            'start_date_local': '2026-01-01T00:00:00',
        }
        act = connector._parse_activity(raw)
        assert act.distance_km == 0
        assert act.avg_pace_min_km is None  # Não divide por zero

    def test_changelog_limite_zero(self, manager, trainer, atleta_corrida):
        manager.register_training(trainer, atleta_corrida)
        entries = manager.get_changelog(trainer, limit=0)
        assert entries == []
