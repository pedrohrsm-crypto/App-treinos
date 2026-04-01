"""
Testes para o modelo de treinos (exporters/workout.py) e parser (description_parser.py).

Valida a conversão de dicts do TrainingPlanGenerator para Workout
e o parsing de todas as variações de descrições encontradas no training_planner.py.
"""
import pytest
from datetime import date

from exporters.workout import (
    Sport, StepType, Workout, WorkoutStep,
    from_plan_dict, parse_duration, parse_zone_string,
    compute_zone_config, map_sport, ZONE_PERCENTAGES,
)
from exporters.description_parser import parse_description


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

LIMIAR = 160.0  # BPM típico


@pytest.fixture
def zone_config():
    return compute_zone_config(LIMIAR)


# ---------------------------------------------------------------------------
# parse_duration
# ---------------------------------------------------------------------------

class TestParseDuration:
    def test_minutes(self):
        assert parse_duration("45 min") == 2700
        assert parse_duration("90 min") == 5400

    def test_minutes_no_space(self):
        assert parse_duration("45min") == 2700

    def test_hours(self):
        assert parse_duration("1h30") == 5400
        assert parse_duration("2h") == 7200

    def test_colon_format(self):
        assert parse_duration("1:30:00") == 5400
        assert parse_duration("90:00") == 5400

    def test_empty(self):
        assert parse_duration("") == 0


# ---------------------------------------------------------------------------
# parse_zone_string
# ---------------------------------------------------------------------------

class TestParseZoneString:
    def test_full_name(self):
        assert parse_zone_string("Z1 - Recuperação") == 1
        assert parse_zone_string("Z5 - VO2max") == 5

    def test_short(self):
        assert parse_zone_string("Z3") == 3

    def test_unknown(self):
        assert parse_zone_string("") is None


# ---------------------------------------------------------------------------
# compute_zone_config
# ---------------------------------------------------------------------------

class TestComputeZoneConfig:
    def test_zone_boundaries(self):
        config = compute_zone_config(LIMIAR)
        assert len(config) == 5
        # Z1: 50-65% of 160 = 80-104
        assert config[1] == (80, 104)
        # Z4: 90-100% of 160 = 144-160
        assert config[4] == (144, 160)
        # Z5: 100-110% of 160 = 160-176
        assert config[5] == (160, 176)


# ---------------------------------------------------------------------------
# map_sport
# ---------------------------------------------------------------------------

class TestMapSport:
    def test_corrida(self):
        assert map_sport("Corrida") == Sport.RUNNING

    def test_ciclismo(self):
        assert map_sport("Ciclismo") == Sport.CYCLING

    def test_natacao(self):
        assert map_sport("Natação") == Sport.SWIMMING

    def test_brick(self):
        assert map_sport("Brick") == Sport.MULTISPORT

    def test_triathlon(self):
        assert map_sport("Triathlon") == Sport.MULTISPORT

    def test_duathlon(self):
        assert map_sport("Duathlon Natação e Corrida") == Sport.MULTISPORT


# ---------------------------------------------------------------------------
# parse_description — Intervalado
# ---------------------------------------------------------------------------

class TestParseInterval:
    def test_running_interval(self, zone_config):
        """15min aquec + 6x800m (rec 2min) + 10min desaq"""
        steps = parse_description(
            "15min aquec + 6x800m (rec 2min) + 10min desaq",
            total_duration_seconds=2700,
            default_zone=4,
            zone_config=zone_config,
        )
        # warmup + 6*(interval + recovery) + cooldown = 1 + 12 + 1 = 14
        assert steps[0].step_type == StepType.WARMUP
        assert steps[0].duration_seconds == 900  # 15min
        assert steps[-1].step_type == StepType.COOLDOWN

        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 6
        assert intervals[0].distance_meters == 800.0

        recoveries = [s for s in steps if s.step_type == StepType.RECOVERY]
        assert len(recoveries) == 6
        assert recoveries[0].duration_seconds == 120

    def test_cycling_interval_duration_based(self, zone_config):
        """20min aquec + 6x5min alta intensidade (rec 3min) + 15min desaq"""
        steps = parse_description(
            "20min aquec + 6x5min alta intensidade (rec 3min) + 15min desaq",
            total_duration_seconds=5400,
            default_zone=5,
            zone_config=zone_config,
        )
        assert steps[0].step_type == StepType.WARMUP
        assert steps[0].duration_seconds == 1200
        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 6
        assert intervals[0].duration_seconds == 300  # 5min
        assert steps[-1].step_type == StepType.COOLDOWN
        assert steps[-1].duration_seconds == 900

    def test_swim_interval(self, zone_config):
        """500m aquec + 10x200m (rec 30s) + 300m desaq"""
        steps = parse_description(
            "500m aquec + 10x200m (rec 30s) + 300m desaq",
            total_duration_seconds=3600,
            default_zone=3,
            zone_config=zone_config,
        )
        assert steps[0].step_type == StepType.WARMUP
        assert steps[0].distance_meters == 500.0
        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 10
        assert intervals[0].distance_meters == 200.0
        recoveries = [s for s in steps if s.step_type == StepType.RECOVERY]
        assert recoveries[0].duration_seconds == 30

    def test_no_recovery(self, zone_config):
        """600m aquec + 8x200m + 400m desaq (sem rec explícito)"""
        steps = parse_description(
            "600m aquec + 8x200m (rec 30s) + 400m desaq",
            total_duration_seconds=3600,
            default_zone=4,
            zone_config=zone_config,
        )
        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 8


# ---------------------------------------------------------------------------
# parse_description — Natação estruturada
# ---------------------------------------------------------------------------

class TestParseSwimStructured:
    def test_swim_technique(self, zone_config):
        """1000m aquecimento + 8x100m técnica + 500m volta à calma"""
        steps = parse_description(
            "1000m aquecimento + 8x100m técnica + 500m volta à calma",
            total_duration_seconds=3600,
            default_zone=2,
            zone_config=zone_config,
        )
        assert steps[0].step_type == StepType.WARMUP
        assert steps[0].distance_meters == 1000.0
        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 8
        assert intervals[0].distance_meters == 100.0
        assert steps[-1].step_type == StepType.COOLDOWN
        assert steps[-1].distance_meters == 500.0

    def test_swim_multi_series(self, zone_config):
        """800m aquec + 6x50m drill + 8x100m técnica + 300m desaq"""
        steps = parse_description(
            "800m aquec + 6x50m drill + 8x100m técnica + 300m desaq",
            total_duration_seconds=3600,
            default_zone=2,
            zone_config=zone_config,
        )
        assert steps[0].step_type == StepType.WARMUP
        assert steps[0].distance_meters == 800.0
        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        # 6 drills + 8 technique = 14
        assert len(intervals) == 14


# ---------------------------------------------------------------------------
# parse_description — Brick/Multisport
# ---------------------------------------------------------------------------

class TestParseBrick:
    def test_bike_run(self, zone_config):
        """60min bike Z2 + 30min corrida Z3"""
        steps = parse_description(
            "60min bike Z2 + 30min corrida Z3",
            total_duration_seconds=5400,
            default_zone=3,
            zone_config=zone_config,
        )
        active_steps = [s for s in steps if s.step_type == StepType.ACTIVE]
        assert len(active_steps) == 2
        assert active_steps[0].duration_seconds == 3600
        assert active_steps[0].target_zone == 2
        assert active_steps[1].duration_seconds == 1800
        assert active_steps[1].target_zone == 3

    def test_brick_with_transition(self, zone_config):
        """35min natação Z2 + transição + 40min corrida Z3"""
        steps = parse_description(
            "35min natação Z2 + transição + 40min corrida Z3",
            total_duration_seconds=4500,
            default_zone=3,
            zone_config=zone_config,
        )
        active_steps = [s for s in steps if s.step_type == StepType.ACTIVE]
        assert len(active_steps) == 2
        rest_steps = [s for s in steps if s.step_type == StepType.REST]
        assert len(rest_steps) == 1  # transição


# ---------------------------------------------------------------------------
# parse_description — Fartlek
# ---------------------------------------------------------------------------

class TestParseFartlek:
    def test_fartlek_blocks(self, zone_config):
        """15min aquec + 8x(2min Z4 + 2min Z2) + 10min desaq"""
        steps = parse_description(
            "15min aquec + 8x(2min Z4 + 2min Z2) + 10min desaq",
            total_duration_seconds=3300,
            default_zone=3,
            zone_config=zone_config,
        )
        assert steps[0].step_type == StepType.WARMUP
        assert steps[0].duration_seconds == 900
        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 8
        assert intervals[0].duration_seconds == 120
        assert intervals[0].target_zone == 4
        recoveries = [s for s in steps if s.step_type == StepType.RECOVERY]
        assert len(recoveries) == 8
        assert recoveries[0].target_zone == 2
        assert steps[-1].step_type == StepType.COOLDOWN


# ---------------------------------------------------------------------------
# parse_description — Progressivo/Segmentado
# ---------------------------------------------------------------------------

class TestParseSegments:
    def test_three_segments(self, zone_config):
        """15min Z2 + 25min Z3 + 15min Z2"""
        steps = parse_description(
            "15min Z2 + 25min Z3 + 15min Z2",
            total_duration_seconds=3300,
            default_zone=2,
            zone_config=zone_config,
        )
        assert len(steps) == 3
        assert steps[0].duration_seconds == 900
        assert steps[0].target_zone == 2
        assert steps[1].duration_seconds == 1500
        assert steps[1].target_zone == 3
        assert steps[2].duration_seconds == 900
        assert steps[2].target_zone == 2

    def test_tempo_run(self, zone_config):
        """15min aquec + 30min Z3 + 15min desaq"""
        steps = parse_description(
            "15min aquec + 30min Z3 + 15min desaq",
            total_duration_seconds=3600,
            default_zone=3,
            zone_config=zone_config,
        )
        assert len(steps) == 3
        assert steps[0].step_type == StepType.WARMUP
        assert steps[1].step_type == StepType.ACTIVE
        assert steps[1].target_zone == 3
        assert steps[2].step_type == StepType.COOLDOWN


# ---------------------------------------------------------------------------
# parse_description — Contínuo e fallback
# ---------------------------------------------------------------------------

class TestParseContinuous:
    def test_continuous_text(self, zone_config):
        """Corrida leve e contínua — fallback a step único"""
        steps = parse_description(
            "Corrida leve e contínua",
            total_duration_seconds=2400,
            default_zone=1,
            zone_config=zone_config,
        )
        assert len(steps) == 1
        assert steps[0].step_type == StepType.ACTIVE
        assert steps[0].duration_seconds == 2400
        assert steps[0].target_zone == 1

    def test_continuous_distance_swim(self, zone_config):
        """3000m contínuo com foco na técnica"""
        steps = parse_description(
            "3000m contínuo com foco na técnica",
            total_duration_seconds=3600,
            default_zone=2,
            zone_config=zone_config,
        )
        assert len(steps) == 1
        assert steps[0].distance_meters == 3000.0
        assert steps[0].step_type == StepType.ACTIVE

    def test_long_run_final_zone(self, zone_config):
        """Corrida longa com 20min finais Z3"""
        steps = parse_description(
            "Corrida longa com 20min finais Z3",
            total_duration_seconds=6000,
            default_zone=2,
            zone_config=zone_config,
        )
        assert len(steps) == 2
        assert steps[0].duration_seconds == 4800  # 80min
        assert steps[0].target_zone == 2
        assert steps[1].duration_seconds == 1200  # 20min
        assert steps[1].target_zone == 3

    def test_health_adjusted_suffix(self, zone_config):
        """Descrição com sufixo de ajuste de saúde deve ser ignorada."""
        steps = parse_description(
            "Corrida contínua | ⚕️ AJUSTADO: Volume reduzido",
            total_duration_seconds=2400,
            default_zone=2,
            zone_config=zone_config,
        )
        assert len(steps) == 1
        assert steps[0].description == "Corrida contínua"


# ---------------------------------------------------------------------------
# from_plan_dict — Integração completa
# ---------------------------------------------------------------------------

class TestFromPlanDict:
    def test_running_base(self):
        d = {
            'dia': 'Terça',
            'modalidade': 'Corrida',
            'duracao': '50 min',
            'tipo': 'Base',
            'zona': 'Z2 - Aeróbico',
            'descricao': 'Corrida contínua confortável',
            'semana': 1,
            'fase': 'base',
            'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR, athlete_name="João")
        assert w.sport == Sport.RUNNING
        assert w.total_duration_seconds == 3000
        assert w.name == "Corrida Base S1"
        assert w.athlete_name == "João"
        assert w.phase == "base"
        assert len(w.steps) >= 1
        assert len(w.zone_config) == 5
        assert w.zone_config[2] == (104, 128)

    def test_triathlon_brick(self):
        d = {
            'dia': 'Domingo',
            'modalidade': 'Brick',
            'duracao': '90 min',
            'tipo': 'Combinado',
            'zona': 'Z3 - Tempo',
            'descricao': '60min bike Z2 + 30min corrida Z3',
            'semana': 3,
            'fase': 'resistencia',
            'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.sport == Sport.MULTISPORT
        assert w.total_duration_seconds == 5400
        active = [s for s in w.steps if s.step_type == StepType.ACTIVE]
        assert len(active) == 2

    def test_swim_interval(self):
        d = {
            'dia': 'Segunda',
            'modalidade': 'Natação',
            'duracao': '60 min',
            'tipo': 'Técnica',
            'zona': 'Z2 - Aeróbico',
            'descricao': '1000m aquecimento + 8x100m técnica + 500m volta à calma',
            'semana': 1,
            'fase': 'base',
            'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.sport == Sport.SWIMMING
        assert w.steps[0].step_type == StepType.WARMUP
        assert w.steps[0].distance_meters == 1000.0

    def test_with_date(self):
        d = {
            'modalidade': 'Corrida',
            'duracao': '45 min',
            'tipo': 'Base',
            'zona': 'Z2 - Aeróbico',
            'descricao': 'Corrida contínua',
            'semana': 1,
            'fase': 'base',
            'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR,
                           workout_date=date(2026, 4, 1))
        assert w.date == date(2026, 4, 1)

    def test_vo2max_interval(self):
        d = {
            'dia': 'Terça',
            'modalidade': 'Corrida',
            'duracao': '60 min',
            'tipo': 'VO2max',
            'zona': 'Z5 - VO2max',
            'descricao': '15min aquec + 5x(4min Z5 + 3min rec) + 10min desaq',
            'semana': 4,
            'fase': 'velocidade',
            'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.sport == Sport.RUNNING
        intervals = [s for s in w.steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) >= 1
