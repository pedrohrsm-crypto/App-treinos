"""
Exportador de treinos para o formato Garmin FIT (.fit).

Utiliza a biblioteca fit-tool para gerar ficheiros FIT do tipo WORKOUT,
compatíveis com dispositivos Garmin e plataformas que aceitem este formato.

Mapeamento de desportos:
  Running=1, Cycling=2, Swimming=5, Multisport=18

Cada WorkoutStep é convertido numa WorkoutStepMessage FIT com:
  - duration_type: TIME (segundos) ou DISTANCE (metros)
  - target_type: HEART_RATE (zona ou custom BPM range)
  - intensity: WARMUP, ACTIVE, COOLDOWN, REST, RECOVERY, INTERVAL
"""
from __future__ import annotations

import datetime
import os
from pathlib import Path
from typing import List, Optional

from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.file_id_message import FileIdMessage
from fit_tool.profile.messages.workout_message import WorkoutMessage as FITWorkoutMessage
from fit_tool.profile.messages.workout_step_message import WorkoutStepMessage
from fit_tool.profile.profile_type import (
    FileType,
    Intensity,
    Manufacturer,
    Sport as FITSport,
    WorkoutStepDuration,
    WorkoutStepTarget,
)

from exporters.workout import Sport, StepType, Workout, WorkoutStep

# ---------------------------------------------------------------------------
# Mapeamentos internos
# ---------------------------------------------------------------------------

_SPORT_TO_FIT: dict[Sport, FITSport] = {
    Sport.RUNNING: FITSport.RUNNING,
    Sport.CYCLING: FITSport.CYCLING,
    Sport.SWIMMING: FITSport.SWIMMING,
    Sport.MULTISPORT: FITSport.MULTISPORT,
}

_STEP_TO_INTENSITY: dict[StepType, Intensity] = {
    StepType.WARMUP: Intensity.WARMUP,
    StepType.ACTIVE: Intensity.ACTIVE,
    StepType.REST: Intensity.REST,
    StepType.COOLDOWN: Intensity.COOLDOWN,
    StepType.INTERVAL: Intensity.INTERVAL,
    StepType.RECOVERY: Intensity.RECOVERY,
}


# ---------------------------------------------------------------------------
# FIT Exporter
# ---------------------------------------------------------------------------

class FITExporter:
    """Exporta objectos Workout para ficheiros .fit (Garmin workout format).

    Args:
        output_dir: Directório de saída para os ficheiros gerados.
    """

    def __init__(self, output_dir: str = "data/exports") -> None:
        self.output_dir = Path(output_dir)

    def export_workout(self, workout: Workout) -> str:
        """Exporta um treino para .fit e devolve o caminho do ficheiro.

        Args:
            workout: Treino estruturado (Workout dataclass).

        Returns:
            Caminho absoluto do ficheiro .fit gerado.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        safe_name = _safe_filename(workout.name)
        filepath = self.output_dir / f"{safe_name}.fit"

        fit_bytes = self._build_fit_bytes(workout)
        filepath.write_bytes(fit_bytes)

        return str(filepath.resolve())

    def export_plan(self, workouts: List[Workout]) -> List[str]:
        """Exporta uma lista de treinos, devolvendo os caminhos gerados."""
        return [self.export_workout(w) for w in workouts]

    def export_workout_bytes(self, workout: Workout) -> bytes:
        """Gera o conteúdo .fit em memória (útil para downloads HTTP)."""
        return self._build_fit_bytes(workout)

    # ------------------------------------------------------------------
    # Construção interna do ficheiro FIT
    # ------------------------------------------------------------------

    def _build_fit_bytes(self, workout: Workout) -> bytes:
        """Constrói o binário FIT completo a partir de um Workout."""

        # 1. File ID
        file_id = FileIdMessage()
        file_id.type = FileType.WORKOUT
        file_id.manufacturer = Manufacturer.DEVELOPMENT.value
        file_id.product = 0
        file_id.serial_number = 0x12345678
        file_id.time_created = round(
            datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000
        )

        # 2. Flatten steps (expand repeats into individual FIT steps)
        flat_steps = _flatten_steps(workout.steps)

        # 3. Workout Step messages
        fit_steps: list[WorkoutStepMessage] = []
        for idx, step in enumerate(flat_steps):
            fit_steps.append(_build_step_message(idx, step))

        # 4. Workout message
        wkt = FITWorkoutMessage()
        wkt.workout_name = workout.name[:40]  # FIT limit ~40 chars
        wkt.sport = _SPORT_TO_FIT.get(workout.sport, FITSport.GENERIC)
        wkt.num_valid_steps = len(fit_steps)

        # 5. Montar FIT file
        builder = FitFileBuilder(auto_define=True, min_string_size=50)
        builder.add(file_id)
        builder.add(wkt)
        builder.add_all(fit_steps)

        fit_file = builder.build()
        return fit_file.to_bytes()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _flatten_steps(steps: List[WorkoutStep]) -> List[WorkoutStep]:
    """Expande steps com repeat_count > 1 em steps individuais.

    O formato FIT não suporta nativamente repeat counts em workout steps
    simples — cada repetição é um step separado (work + recovery).
    """
    flat: list[WorkoutStep] = []
    for step in steps:
        count = max(1, step.repeat_count)
        for _ in range(count):
            flat.append(step)
    return flat


def _build_step_message(index: int, step: WorkoutStep) -> WorkoutStepMessage:
    """Converte um WorkoutStep interno numa WorkoutStepMessage FIT."""
    msg = WorkoutStepMessage()
    msg.message_index = index
    msg.intensity = _STEP_TO_INTENSITY.get(step.step_type, Intensity.ACTIVE)

    # Nome do step (truncado a 40 chars)
    if step.description:
        msg.workout_step_name = step.description[:40]

    # Duração: distância ou tempo
    if step.distance_meters and step.distance_meters > 0:
        msg.duration_type = WorkoutStepDuration.DISTANCE
        msg.duration_distance = float(step.distance_meters)
    elif step.duration_seconds > 0:
        msg.duration_type = WorkoutStepDuration.TIME
        msg.duration_time = float(step.duration_seconds)
    else:
        msg.duration_type = WorkoutStepDuration.OPEN
        msg.duration_value = 0

    # Target: HR zone ou custom BPM range
    if step.target_hr_low and step.target_hr_high:
        msg.target_type = WorkoutStepTarget.HEART_RATE
        msg.custom_target_value_low = step.target_hr_low
        msg.custom_target_value_high = step.target_hr_high
    elif step.target_zone:
        msg.target_type = WorkoutStepTarget.HEART_RATE
        msg.target_hr_zone = step.target_zone
    else:
        msg.target_type = WorkoutStepTarget.OPEN

    return msg


def _safe_filename(name: str) -> str:
    """Remove caracteres inválidos para nomes de ficheiro."""
    safe = name.replace(" ", "_").replace("/", "-")
    return "".join(c for c in safe if c.isalnum() or c in "_-.")
