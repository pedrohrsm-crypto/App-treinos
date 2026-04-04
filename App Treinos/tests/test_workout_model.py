"""
Testes para o modelo de treinos (exporters/workout.py) e parser (description_parser.py).

Valida a conversão de dicts do TrainingPlanGenerator para Workout
e o parsing de todas as variações de descrições encontradas no training_planner.py.

Desportos cobertos: Corrida, Ciclismo, Natação, Triathlon,
  Duathlon (Natação+Corrida), Duathlon (Ciclismo+Corrida).
"""
import pytest
from datetime import date

from exporters.workout import (
    Sport, StepType, Workout, WorkoutStep,
    WORKOUT_TYPES, MODALITIES, PHASES, RACE_DISTANCES, ZONE_PERCENTAGES,
    from_plan_dict, parse_duration, parse_zone_string,
    compute_zone_config, map_sport,
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
# Constantes do projecto
# ---------------------------------------------------------------------------

class TestConstants:
    def test_workout_types_complete(self):
        """Todos os tipos de treino do training_planner estão listados."""
        expected = {
            "Recuperação", "Base", "Técnica", "Técnica + Estímulos",
            "Fartlek Leve", "Fartlek", "Intervalado", "Tempo Run",
            "Progressivo", "Long Run", "Long Ride", "Sweet Spot",
            "VO2max", "Velocidade", "Aeróbico", "Volume",
            "Combinado", "Shakeout", "DIA DA PROVA",
        }
        assert set(WORKOUT_TYPES) == expected

    def test_modalities_complete(self):
        expected = {"Corrida", "Ciclismo", "Natação", "Brick", "Multisport"}
        assert set(MODALITIES) == expected

    def test_phases_complete(self):
        expected = {"base", "resistencia", "velocidade", "potencia", "polimento"}
        assert set(PHASES) == expected

    def test_race_distances_per_sport(self):
        assert "Corrida" in RACE_DISTANCES
        assert "Maratona" in RACE_DISTANCES["Corrida"]
        assert "Ciclismo" in RACE_DISTANCES
        assert "160K" in RACE_DISTANCES["Ciclismo"]
        assert "Natação" in RACE_DISTANCES
        assert "Triathlon" in RACE_DISTANCES
        assert "Ironman" in RACE_DISTANCES["Triathlon"]
        assert "Duathlon (Natação+Corrida)" in RACE_DISTANCES
        assert "Duathlon (Ciclismo+Corrida)" in RACE_DISTANCES

    def test_zone_percentages(self):
        assert len(ZONE_PERCENTAGES) == 5
        assert ZONE_PERCENTAGES[1] == (0.50, 0.65)
        assert ZONE_PERCENTAGES[5] == (1.00, 1.10)


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

    def test_large_duration_triathlon(self):
        """Ironman pode ter treinos de 180 min."""
        assert parse_duration("180 min") == 10800


# ---------------------------------------------------------------------------
# parse_zone_string
# ---------------------------------------------------------------------------

class TestParseZoneString:
    def test_full_name(self):
        assert parse_zone_string("Z1 - Recuperação") == 1
        assert parse_zone_string("Z5 - VO2max") == 5

    def test_short(self):
        assert parse_zone_string("Z3") == 3

    def test_zone_range(self):
        """Z2-Z3 deve retornar a zona mais baixa."""
        assert parse_zone_string("Z2-Z3") == 2
        assert parse_zone_string("Z4-Z5") == 4

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

    def test_different_threshold(self):
        """Atleta com limiar 180 BPM."""
        config = compute_zone_config(180.0)
        assert config[1] == (90, 117)
        assert config[5] == (180, 198)


# ---------------------------------------------------------------------------
# map_sport — Todos os desportos do projecto
# ---------------------------------------------------------------------------

class TestMapSport:
    def test_corrida(self):
        assert map_sport("Corrida") == Sport.RUNNING

    def test_ciclismo(self):
        assert map_sport("Ciclismo") == Sport.CYCLING

    def test_natacao_com_acento(self):
        assert map_sport("Natação") == Sport.SWIMMING

    def test_natacao_sem_acento(self):
        assert map_sport("Natacao") == Sport.SWIMMING

    def test_brick(self):
        assert map_sport("Brick") == Sport.MULTISPORT

    def test_multisport(self):
        assert map_sport("Multisport") == Sport.MULTISPORT

    def test_triathlon(self):
        assert map_sport("Triathlon") == Sport.MULTISPORT

    def test_duathlon_generico(self):
        assert map_sport("Duathlon") == Sport.MULTISPORT

    def test_duathlon_natacao_corrida_parenteses(self):
        """Nome exacto do SPORT_COLORS."""
        assert map_sport("Duathlon (Natação+Corrida)") == Sport.MULTISPORT

    def test_duathlon_ciclismo_corrida_parenteses(self):
        """Nome exacto do SPORT_COLORS."""
        assert map_sport("Duathlon (Ciclismo+Corrida)") == Sport.MULTISPORT

    def test_duathlon_natacao_corrida_texto(self):
        """Nome usado no training_planner aliases."""
        assert map_sport("Duathlon Natação e Corrida") == Sport.MULTISPORT

    def test_duathlon_ciclismo_corrida_texto(self):
        assert map_sport("Duathlon Ciclismo e Corrida") == Sport.MULTISPORT

    def test_aquathlon(self):
        assert map_sport("Aquathlon") == Sport.MULTISPORT

    def test_case_insensitive(self):
        assert map_sport("corrida") == Sport.RUNNING
        assert map_sport("CICLISMO") == Sport.CYCLING

    def test_unknown_defaults_running(self):
        assert map_sport("Desconhecido") == Sport.RUNNING


# ---------------------------------------------------------------------------
# parse_description — Intervalado (Corrida, Ciclismo, Natação)
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
        assert steps[0].step_type == StepType.WARMUP
        assert steps[0].duration_seconds == 900
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
        assert intervals[0].duration_seconds == 300
        assert steps[-1].step_type == StepType.COOLDOWN
        assert steps[-1].duration_seconds == 900

    def test_cycling_sweet_spot(self, zone_config):
        """20min aquec + 3x15min no limiar (rec 5min) + 15min desaq"""
        steps = parse_description(
            "20min aquec + 3x15min no limiar (rec 5min) + 15min desaq",
            total_duration_seconds=5400,
            default_zone=4,
            zone_config=zone_config,
        )
        assert steps[0].step_type == StepType.WARMUP
        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 3
        assert intervals[0].duration_seconds == 900  # 15min
        recoveries = [s for s in steps if s.step_type == StepType.RECOVERY]
        assert len(recoveries) == 3
        assert recoveries[0].duration_seconds == 300  # 5min

    def test_swim_interval_with_recovery(self, zone_config):
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

    def test_swim_short_recovery(self, zone_config):
        """1000m aquec + 20x100m (rec 15s) + 500m desaq"""
        steps = parse_description(
            "1000m aquec + 20x100m (rec 15s) + 500m desaq",
            total_duration_seconds=3600,
            default_zone=4,
            zone_config=zone_config,
        )
        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 20
        recoveries = [s for s in steps if s.step_type == StepType.RECOVERY]
        assert recoveries[0].duration_seconds == 15

    def test_running_1km_interval(self, zone_config):
        """15min aquec + 6x1km Z4 (rec 2min) + 10min desaq"""
        steps = parse_description(
            "15min aquec + 6x1km Z4 (rec 2min) + 10min desaq",
            total_duration_seconds=3600,
            default_zone=4,
            zone_config=zone_config,
        )
        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 6
        assert intervals[0].distance_meters == 1000.0

    def test_cycling_interval_4x10min(self, zone_config):
        """20min aquec + 4x10min alta intensidade (rec 4min) + 15min desaq"""
        steps = parse_description(
            "20min aquec + 4x10min alta intensidade (rec 4min) + 15min desaq",
            total_duration_seconds=5400,
            default_zone=4,
            zone_config=zone_config,
        )
        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 4
        assert intervals[0].duration_seconds == 600


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
        assert len(intervals) == 14  # 6 drills + 8 technique

    def test_swim_smaller_warmup(self, zone_config):
        """700m aquecimento + 4x100m técnica + 300m volta à calma"""
        steps = parse_description(
            "700m aquecimento + 4x100m técnica + 300m volta à calma",
            total_duration_seconds=2700,
            default_zone=2,
            zone_config=zone_config,
        )
        assert steps[0].distance_meters == 700.0
        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 4


# ---------------------------------------------------------------------------
# parse_description — Brick/Multisport (Triathlon, Duathlon)
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

    def test_brick_zone_range(self, zone_config):
        """60min bike Z2-Z3 + transição + 30min corrida Z3"""
        steps = parse_description(
            "60min bike Z2-Z3 + transição + 30min corrida Z3",
            total_duration_seconds=5400,
            default_zone=3,
            zone_config=zone_config,
        )
        active_steps = [s for s in steps if s.step_type == StepType.ACTIVE]
        assert len(active_steps) == 2
        assert active_steps[0].target_zone == 2  # Z2 (mais baixa do range)

    def test_duathlon_bike_run(self, zone_config):
        """70min bike Z2 + transição + 30min corrida Z2-Z3"""
        steps = parse_description(
            "70min bike Z2 + transição + 30min corrida Z2-Z3",
            total_duration_seconds=6000,
            default_zone=2,
            zone_config=zone_config,
        )
        active_steps = [s for s in steps if s.step_type == StepType.ACTIVE]
        assert len(active_steps) == 2
        assert active_steps[0].duration_seconds == 4200  # 70min

    def test_aquathlon_swim_run(self, zone_config):
        """30min natação Z2 + transição + 35min corrida Z2"""
        steps = parse_description(
            "30min natação Z2 + transição + 35min corrida Z2",
            total_duration_seconds=3900,
            default_zone=2,
            zone_config=zone_config,
        )
        active_steps = [s for s in steps if s.step_type == StepType.ACTIVE]
        assert len(active_steps) == 2
        rest_steps = [s for s in steps if s.step_type == StepType.REST]
        assert len(rest_steps) == 1


# ---------------------------------------------------------------------------
# parse_description — Fartlek (3 variantes)
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

    def test_fartlek_with_rec(self, zone_config):
        """15min aquec + 5x(4min Z5 + 3min rec) + 10min desaq"""
        steps = parse_description(
            "15min aquec + 5x(4min Z5 + 3min rec) + 10min desaq",
            total_duration_seconds=3600,
            default_zone=5,
            zone_config=zone_config,
        )
        assert steps[0].step_type == StepType.WARMUP
        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 5
        assert intervals[0].duration_seconds == 240  # 4min
        assert intervals[0].target_zone == 5
        recoveries = [s for s in steps if s.step_type == StepType.RECOVERY]
        assert len(recoveries) == 5
        assert recoveries[0].duration_seconds == 180  # 3min
        assert recoveries[0].target_zone == 1  # rec → Z1

    def test_fartlek_taper(self, zone_config):
        """15min aquec + 4x(2min Z4 + 3min rec) + 10min desaq (polimento)"""
        steps = parse_description(
            "15min aquec + 4x(2min Z4 + 3min rec) + 10min desaq",
            total_duration_seconds=2400,
            default_zone=3,
            zone_config=zone_config,
        )
        intervals = [s for s in steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 4

    def test_fartlek_continuous(self, zone_config):
        """10min aquec + 30min fartlek Z2-Z3 + 10min desaq"""
        steps = parse_description(
            "10min aquec + 30min fartlek Z2-Z3 + 10min desaq",
            total_duration_seconds=3000,
            default_zone=2,
            zone_config=zone_config,
        )
        assert len(steps) == 3
        assert steps[0].step_type == StepType.WARMUP
        assert steps[0].duration_seconds == 600
        assert steps[1].step_type == StepType.ACTIVE
        assert steps[1].duration_seconds == 1800
        assert "Fartlek" in steps[1].description
        assert steps[2].step_type == StepType.COOLDOWN
        assert steps[2].duration_seconds == 600


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

    def test_threshold_run(self, zone_config):
        """15min aquec + 20min Z4 + 15min desaq"""
        steps = parse_description(
            "15min aquec + 20min Z4 + 15min desaq",
            total_duration_seconds=3000,
            default_zone=4,
            zone_config=zone_config,
        )
        assert len(steps) == 3
        assert steps[1].target_zone == 4
        assert steps[1].duration_seconds == 1200


# ---------------------------------------------------------------------------
# parse_description — Contínuo, especiais e fallback
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

    def test_continuous_cycling(self, zone_config):
        """Ritmo constante em terreno plano"""
        steps = parse_description(
            "Ritmo constante em terreno plano",
            total_duration_seconds=5400,
            default_zone=2,
            zone_config=zone_config,
        )
        assert len(steps) == 1
        assert steps[0].step_type == StepType.ACTIVE
        assert steps[0].duration_seconds == 5400

    def test_continuous_cycling_varied(self, zone_config):
        """Ritmo constante em terreno variado"""
        steps = parse_description(
            "Ritmo constante em terreno variado",
            total_duration_seconds=4500,
            default_zone=2,
            zone_config=zone_config,
        )
        assert len(steps) == 1

    def test_recovery_run(self, zone_config):
        """Corrida regenerativa"""
        steps = parse_description(
            "Corrida regenerativa",
            total_duration_seconds=2400,
            default_zone=1,
            zone_config=zone_config,
        )
        assert len(steps) == 1
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

    def test_continuous_distance_2500(self, zone_config):
        """2500m contínuo moderado"""
        steps = parse_description(
            "2500m contínuo moderado",
            total_duration_seconds=3300,
            default_zone=2,
            zone_config=zone_config,
        )
        assert len(steps) == 1
        assert steps[0].distance_meters == 2500.0

    def test_continuous_distance_1800(self, zone_config):
        """1800m contínuo suave"""
        steps = parse_description(
            "1800m contínuo suave",
            total_duration_seconds=2400,
            default_zone=1,
            zone_config=zone_config,
        )
        assert len(steps) == 1
        assert steps[0].distance_meters == 1800.0

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

    def test_long_ride_simulation(self, zone_config):
        """Pedal longo com simulação de prova"""
        steps = parse_description(
            "Pedal longo com simulação de prova",
            total_duration_seconds=10800,  # 180min
            default_zone=2,
            zone_config=zone_config,
        )
        assert len(steps) == 1
        assert steps[0].duration_seconds == 10800

    def test_run_with_stretching(self, zone_config):
        """Corrida leve + alongamentos"""
        steps = parse_description(
            "Corrida leve + alongamentos",
            total_duration_seconds=1800,
            default_zone=1,
            zone_config=zone_config,
        )
        assert len(steps) == 1
        assert steps[0].step_type == StepType.ACTIVE

    def test_shakeout(self, zone_config):
        """Corrida muito leve (shakeout/polimento)"""
        steps = parse_description(
            "Corrida muito leve",
            total_duration_seconds=1800,
            default_zone=1,
            zone_config=zone_config,
        )
        assert len(steps) == 1

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

    def test_menstrual_adjusted_suffix(self, zone_config):
        """Descrição com sufixo de ajuste menstrual."""
        steps = parse_description(
            "Corrida contínua confortável | 🌸 AJUSTADO: Intensidade reduzida (fase menstrual)",
            total_duration_seconds=2400,
            default_zone=2,
            zone_config=zone_config,
        )
        assert len(steps) == 1
        assert "🌸" not in steps[0].description

    def test_race_day(self, zone_config):
        """🏁 DIA DA MARATONA - Boa sorte!"""
        steps = parse_description(
            "🏁 DIA DA MARATONA - Boa sorte!",
            total_duration_seconds=0,
            default_zone=4,
            zone_config=zone_config,
        )
        assert len(steps) == 1
        assert steps[0].step_type == StepType.ACTIVE
        assert "DIA DA MARATONA" in steps[0].description

    def test_race_day_no_emoji(self, zone_config):
        """DIA DA PROVA sem emoji."""
        steps = parse_description(
            "DIA DA PROVA - Boa sorte!",
            total_duration_seconds=0,
            default_zone=4,
            zone_config=zone_config,
        )
        assert len(steps) == 1

    def test_empty_description(self, zone_config):
        """Descrição vazia gera step ACTIVE."""
        steps = parse_description("", 2400, 2, zone_config)
        assert len(steps) == 1
        assert steps[0].step_type == StepType.ACTIVE


# ---------------------------------------------------------------------------
# from_plan_dict — Integração com todos os desportos
# ---------------------------------------------------------------------------

class TestFromPlanDict:
    def test_running_base(self):
        d = {
            'dia': 'Terça', 'modalidade': 'Corrida', 'duracao': '50 min',
            'tipo': 'Base', 'zona': 'Z2 - Aeróbico',
            'descricao': 'Corrida contínua confortável',
            'semana': 1, 'fase': 'base', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR, athlete_name="João")
        assert w.sport == Sport.RUNNING
        assert w.total_duration_seconds == 3000
        assert w.name == "Corrida Base S1"
        assert w.athlete_name == "João"
        assert w.phase == "base"
        assert w.workout_type == "Base"
        assert w.week_type == "normal"
        assert w.modality == "Corrida"
        assert len(w.steps) >= 1
        assert len(w.zone_config) == 5
        assert w.zone_config[2] == (104, 128)

    def test_cycling_interval(self):
        d = {
            'dia': 'Terça', 'modalidade': 'Ciclismo', 'duracao': '90 min',
            'tipo': 'Intervalado', 'zona': 'Z5 - VO2max',
            'descricao': '20min aquec + 6x5min alta intensidade (rec 3min) + 15min desaq',
            'semana': 2, 'fase': 'velocidade', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.sport == Sport.CYCLING
        assert w.workout_type == "Intervalado"
        intervals = [s for s in w.steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 6

    def test_cycling_sweet_spot(self):
        d = {
            'dia': 'Quinta', 'modalidade': 'Ciclismo', 'duracao': '90 min',
            'tipo': 'Sweet Spot', 'zona': 'Z4 - Limiar',
            'descricao': '20min aquec + 3x15min no limiar (rec 5min) + 15min desaq',
            'semana': 2, 'fase': 'resistencia', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.sport == Sport.CYCLING
        assert w.workout_type == "Sweet Spot"
        intervals = [s for s in w.steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 3

    def test_cycling_long_ride(self):
        d = {
            'dia': 'Domingo', 'modalidade': 'Ciclismo', 'duracao': '180 min',
            'tipo': 'Long Ride', 'zona': 'Z2 - Aeróbico',
            'descricao': 'Pedal longo com simulação de prova',
            'semana': 3, 'fase': 'base', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.sport == Sport.CYCLING
        assert w.total_duration_seconds == 10800
        assert w.workout_type == "Long Ride"

    def test_triathlon_brick(self):
        d = {
            'dia': 'Domingo', 'modalidade': 'Brick', 'duracao': '90 min',
            'tipo': 'Combinado', 'zona': 'Z3 - Tempo',
            'descricao': '60min bike Z2 + 30min corrida Z3',
            'semana': 3, 'fase': 'resistencia', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.sport == Sport.MULTISPORT
        assert w.workout_type == "Combinado"
        active = [s for s in w.steps if s.step_type == StepType.ACTIVE]
        assert len(active) == 2

    def test_triathlon_brick_with_transition(self):
        d = {
            'dia': 'Domingo', 'modalidade': 'Brick', 'duracao': '75 min',
            'tipo': 'Combinado', 'zona': 'Z3 - Tempo',
            'descricao': '35min natação Z2 + transição + 40min corrida Z3',
            'semana': 4, 'fase': 'base', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.sport == Sport.MULTISPORT
        rest = [s for s in w.steps if s.step_type == StepType.REST]
        assert len(rest) == 1  # transição

    def test_swim_technique(self):
        d = {
            'dia': 'Segunda', 'modalidade': 'Natação', 'duracao': '60 min',
            'tipo': 'Técnica', 'zona': 'Z2 - Aeróbico',
            'descricao': '1000m aquecimento + 8x100m técnica + 500m volta à calma',
            'semana': 1, 'fase': 'base', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.sport == Sport.SWIMMING
        assert w.workout_type == "Técnica"
        assert w.steps[0].step_type == StepType.WARMUP
        assert w.steps[0].distance_meters == 1000.0

    def test_swim_volume(self):
        d = {
            'dia': 'Sábado', 'modalidade': 'Natação', 'duracao': '60 min',
            'tipo': 'Volume', 'zona': 'Z2 - Aeróbico',
            'descricao': '3000m contínuo com foco na técnica',
            'semana': 1, 'fase': 'base', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.sport == Sport.SWIMMING
        assert w.workout_type == "Volume"
        assert w.steps[0].distance_meters == 3000.0

    def test_running_recovery(self):
        d = {
            'dia': 'Segunda', 'modalidade': 'Corrida', 'duracao': '40 min',
            'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação',
            'descricao': 'Corrida leve e regenerativa',
            'semana': 1, 'fase': 'base', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.workout_type == "Recuperação"
        assert w.steps[0].target_zone == 1

    def test_running_long_run(self):
        d = {
            'dia': 'Domingo', 'modalidade': 'Corrida', 'duracao': '100 min',
            'tipo': 'Long Run', 'zona': 'Z2 - Aeróbico',
            'descricao': 'Corrida longa com 20min finais Z3',
            'semana': 2, 'fase': 'resistencia', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.workout_type == "Long Run"
        assert len(w.steps) == 2
        assert w.steps[1].target_zone == 3

    def test_vo2max_interval(self):
        d = {
            'dia': 'Terça', 'modalidade': 'Corrida', 'duracao': '60 min',
            'tipo': 'VO2max', 'zona': 'Z5 - VO2max',
            'descricao': '15min aquec + 5x(4min Z5 + 3min rec) + 10min desaq',
            'semana': 4, 'fase': 'velocidade', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.sport == Sport.RUNNING
        assert w.workout_type == "VO2max"
        intervals = [s for s in w.steps if s.step_type == StepType.INTERVAL]
        assert len(intervals) == 5

    def test_with_date(self):
        d = {
            'modalidade': 'Corrida', 'duracao': '45 min', 'tipo': 'Base',
            'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida contínua',
            'semana': 1, 'fase': 'base', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR,
                           workout_date=date(2026, 4, 1))
        assert w.date == date(2026, 4, 1)

    def test_race_day(self):
        d = {
            'dia': 'Domingo', 'modalidade': 'Corrida', 'duracao': '0 min',
            'tipo': 'DIA DA PROVA', 'zona': 'Z4 - Limiar',
            'descricao': '🏁 DIA DA MARATONA - Boa sorte!',
            'semana': 18, 'fase': 'polimento', 'tipo_semana': 'polimento',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.workout_type == "DIA DA PROVA"
        assert w.phase == "polimento"
        assert w.week_type == "polimento"

    def test_fartlek_leve(self):
        d = {
            'dia': 'Quinta', 'modalidade': 'Corrida', 'duracao': '50 min',
            'tipo': 'Fartlek Leve', 'zona': 'Z2 - Aeróbico',
            'descricao': '10min aquec + 30min fartlek Z2-Z3 + 10min desaq',
            'semana': 1, 'fase': 'base', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.workout_type == "Fartlek Leve"
        assert len(w.steps) == 3
        assert w.steps[0].step_type == StepType.WARMUP
        assert w.steps[1].step_type == StepType.ACTIVE

    def test_duathlon_brick(self):
        d = {
            'dia': 'Domingo', 'modalidade': 'Brick', 'duracao': '90 min',
            'tipo': 'Combinado', 'zona': 'Z3 - Tempo',
            'descricao': '60min bike Z2-Z3 + transição + 30min corrida Z3',
            'semana': 3, 'fase': 'resistencia', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        assert w.sport == Sport.MULTISPORT
        active = [s for s in w.steps if s.step_type == StepType.ACTIVE]
        assert len(active) == 2


# ---------------------------------------------------------------------------
# HR Zones — verificação de BPM nos steps
# ---------------------------------------------------------------------------

class TestHRZonesInSteps:
    def test_interval_hr_values(self):
        """Steps de intervalo devem ter HR preenchido em BPM."""
        d = {
            'modalidade': 'Corrida', 'duracao': '60 min',
            'tipo': 'Intervalado', 'zona': 'Z4 - Limiar',
            'descricao': '15min aquec + 6x800m (rec 2min) + 10min desaq',
            'semana': 1, 'fase': 'base', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        intervals = [s for s in w.steps if s.step_type == StepType.INTERVAL]
        assert intervals[0].target_hr_low is not None
        assert intervals[0].target_hr_high is not None
        # Z4: 90-100% of 160 = 144-160
        assert intervals[0].target_hr_low == 144
        assert intervals[0].target_hr_high == 160

    def test_recovery_hr_z1(self):
        """Steps de recuperação devem ter HR de Z1."""
        d = {
            'modalidade': 'Corrida', 'duracao': '60 min',
            'tipo': 'Intervalado', 'zona': 'Z4 - Limiar',
            'descricao': '15min aquec + 6x800m (rec 2min) + 10min desaq',
            'semana': 1, 'fase': 'base', 'tipo_semana': 'normal',
        }
        w = from_plan_dict(d, limiar_lactato=LIMIAR)
        recoveries = [s for s in w.steps if s.step_type == StepType.RECOVERY]
        assert recoveries[0].target_zone == 1
        assert recoveries[0].target_hr_low == 80   # 50% of 160
        assert recoveries[0].target_hr_high == 104  # 65% of 160
