"""
Modelo interno de treinos estruturados para exportação FIT/TCX.

Converte os dicts gerados pelo TrainingPlanGenerator em dataclasses
tipadas, prontas para serialização nos formatos Garmin FIT e TCX.

Desportos suportados: Corrida, Ciclismo, Natação, Triathlon,
  Duathlon (Natação+Corrida), Duathlon (Ciclismo+Corrida).

Fases de periodização: base, resistencia, velocidade, potencia, polimento.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Sport(Enum):
    """Desportos suportados pelo App Treinos.

    Mapeamento FIT: Running=1, Cycling=2, Swimming=5, Multisport=3.
    """
    RUNNING = "running"
    CYCLING = "cycling"
    SWIMMING = "swimming"
    MULTISPORT = "multisport"


class StepType(Enum):
    WARMUP = "warmup"
    ACTIVE = "active"
    REST = "rest"
    COOLDOWN = "cooldown"
    INTERVAL = "interval"
    RECOVERY = "recovery"


# ---------------------------------------------------------------------------
# Tipos de treino reconhecidos pelo training_planner.py
# ---------------------------------------------------------------------------

WORKOUT_TYPES = [
    "Recuperação", "Base", "Técnica", "Técnica + Estímulos",
    "Fartlek Leve", "Fartlek", "Intervalado", "Tempo Run",
    "Progressivo", "Long Run", "Long Ride", "Sweet Spot",
    "VO2max", "Velocidade", "Aeróbico", "Volume",
    "Combinado", "Shakeout", "DIA DA PROVA",
]

# Modalidades usadas nas sessões individuais (campo 'modalidade')
MODALITIES = ["Corrida", "Ciclismo", "Natação", "Brick", "Multisport"]

# Fases de periodização
PHASES = ["base", "resistencia", "velocidade", "potencia", "polimento"]


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class WorkoutStep:
    """Um passo individual dentro de um treino estruturado."""
    step_type: StepType
    duration_seconds: int = 0
    target_zone: Optional[int] = None          # 1-5
    target_hr_low: Optional[int] = None        # BPM
    target_hr_high: Optional[int] = None       # BPM
    repeat_count: int = 1
    distance_meters: Optional[float] = None
    description: str = ""


@dataclass
class Workout:
    """Treino completamente estruturado, pronto para exportação FIT/TCX."""
    name: str
    sport: Sport
    total_duration_seconds: int
    workout_type: str = ""                      # Base, Intervalado, Long Run, etc.
    steps: List[WorkoutStep] = field(default_factory=list)
    zone_config: Dict[int, Tuple[int, int]] = field(default_factory=dict)
    date: Optional[date] = None
    description: str = ""
    athlete_name: str = ""
    week_number: int = 0
    phase: str = ""                             # base, resistencia, velocidade, etc.
    week_type: str = ""                         # normal, recuperacao, polimento
    modality: str = ""                          # Modalidade original em PT


# ---------------------------------------------------------------------------
# Mapeamento modalidade → Sport
# ---------------------------------------------------------------------------

_SPORT_MAP: Dict[str, Sport] = {
    # Modalidades de sessão (campo 'modalidade')
    "corrida": Sport.RUNNING,
    "ciclismo": Sport.CYCLING,
    "natação": Sport.SWIMMING,
    "natacao": Sport.SWIMMING,
    "brick": Sport.MULTISPORT,
    "multisport": Sport.MULTISPORT,

    # Desportos principais (campo 'esporte' do Athlete)
    "triathlon": Sport.MULTISPORT,
    "duathlon": Sport.MULTISPORT,

    # Nomes exactos do SPORT_COLORS / training_wizard.py
    "duathlon (natação+corrida)": Sport.MULTISPORT,
    "duathlon (ciclismo+corrida)": Sport.MULTISPORT,

    # Variantes sem parênteses (usadas no training_planner aliases)
    "duathlon natação e corrida": Sport.MULTISPORT,
    "duathlon ciclismo e corrida": Sport.MULTISPORT,

    # Aliases adicionais
    "aquathlon": Sport.MULTISPORT,
}

# Mapeamento zona string → número (1-5)
_ZONE_MAP: Dict[str, int] = {
    "Z1 - Recuperação": 1,
    "Z2 - Aeróbico": 2,
    "Z3 - Tempo": 3,
    "Z4 - Limiar": 4,
    "Z5 - VO2max": 5,
}

# Percentagens de cada zona em relação ao limiar lactato
ZONE_PERCENTAGES: Dict[int, Tuple[float, float]] = {
    1: (0.50, 0.65),
    2: (0.65, 0.80),
    3: (0.80, 0.90),
    4: (0.90, 1.00),
    5: (1.00, 1.10),
}

# Distâncias de prova suportadas por desporto
RACE_DISTANCES: Dict[str, List[str]] = {
    "Corrida": ["5K", "10K", "Meia Maratona", "Maratona"],
    "Ciclismo": ["40K", "80K", "160K"],
    "Natação": ["1500m", "3000m", "5000m"],
    "Triathlon": ["Sprint", "Olímpico", "Meio Ironman", "Ironman"],
    "Duathlon (Natação+Corrida)": ["Aquathlon Sprint", "Aquathlon Olímpico", "Aquathlon Longo"],
    "Duathlon (Ciclismo+Corrida)": ["Duathlon Sprint", "Duathlon Olímpico", "Duathlon Longo", "Duathlon Ironman"],
}


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def parse_duration(duracao: str) -> int:
    """Converte string de duração para segundos.

    Aceita formatos: "45 min", "90 min", "1h30", "1:30:00".
    """
    duracao = duracao.strip().lower()

    # "45 min" ou "45min"
    m = re.match(r"^(\d+)\s*min", duracao)
    if m:
        return int(m.group(1)) * 60

    # "1h30" ou "1h"
    m = re.match(r"^(\d+)h\s*(\d+)?", duracao)
    if m:
        hours = int(m.group(1))
        mins = int(m.group(2)) if m.group(2) else 0
        return hours * 3600 + mins * 60

    # "1:30:00" ou "90:00"
    parts = duracao.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])

    # Fallback: tenta interpretar como minutos
    try:
        return int(float(duracao)) * 60
    except ValueError:
        return 0


def parse_zone_string(zona: str) -> Optional[int]:
    """Extrai o número da zona (1-5) de uma string como 'Z2 - Aeróbico'.

    Também suporta ranges como 'Z2-Z3' (retorna a zona mais baixa).
    """
    if zona in _ZONE_MAP:
        return _ZONE_MAP[zona]
    # "Z2-Z3" → retorna 2 (zona mais baixa do range)
    m = re.match(r"Z(\d)(?:\s*-\s*Z(\d))?", zona)
    if m:
        return int(m.group(1))
    return None


def compute_zone_config(limiar_lactato: float) -> Dict[int, Tuple[int, int]]:
    """Calcula os limites de HR (BPM) para cada zona com base no limiar."""
    config: Dict[int, Tuple[int, int]] = {}
    for zone_num, (pct_min, pct_max) in ZONE_PERCENTAGES.items():
        hr_low = round(limiar_lactato * pct_min)
        hr_high = round(limiar_lactato * pct_max)
        config[zone_num] = (hr_low, hr_high)
    return config


def map_sport(modalidade: str) -> Sport:
    """Mapeia nome da modalidade em português para o enum Sport."""
    key = modalidade.strip().lower()
    return _SPORT_MAP.get(key, Sport.RUNNING)


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def from_plan_dict(
    d: dict,
    limiar_lactato: float,
    athlete_name: str = "",
    workout_date: Optional[date] = None,
) -> Workout:
    """Converte um dict do TrainingPlanGenerator num Workout estruturado.

    Args:
        d: Dict com keys: modalidade, duracao, tipo, zona, descricao,
           semana, fase, tipo_semana.
        limiar_lactato: Limiar lactato do atleta em BPM (para cálculo de zonas).
        athlete_name: Nome do atleta (opcional).
        workout_date: Data do treino (opcional).

    Returns:
        Workout pronto para exportação.
    """
    from exporters.description_parser import parse_description

    modalidade = d.get("modalidade", "Corrida")
    sport = map_sport(modalidade)
    total_seconds = parse_duration(d.get("duracao", "0 min"))
    zone_num = parse_zone_string(d.get("zona", ""))
    zone_config = compute_zone_config(limiar_lactato)

    # Gerar nome descritivo
    tipo = d.get("tipo", "Treino")
    semana = d.get("semana", 0)
    name = f"{modalidade} {tipo} S{semana}" if semana else f"{modalidade} {tipo}"

    # Parsear descrição em steps estruturados
    steps = parse_description(
        descricao=d.get("descricao", ""),
        total_duration_seconds=total_seconds,
        default_zone=zone_num,
        zone_config=zone_config,
    )

    return Workout(
        name=name,
        sport=sport,
        total_duration_seconds=total_seconds,
        workout_type=tipo,
        steps=steps,
        zone_config=zone_config,
        date=workout_date,
        description=d.get("descricao", ""),
        athlete_name=athlete_name,
        week_number=semana,
        phase=d.get("fase", ""),
        week_type=d.get("tipo_semana", ""),
        modality=modalidade,
    )
