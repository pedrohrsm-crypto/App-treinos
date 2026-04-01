"""
Parser de descrições de treino em português para WorkoutSteps estruturados.

Padrões suportados (todos extraídos do training_planner.py):

 1. Intervalado  — "15min aquec + 6x800m (rec 2min) + 10min desaq"
                   "20min aquec + 6x5min alta intensidade (rec 3min) + 15min desaq"
                   "20min aquec + 3x15min no limiar (rec 5min) + 15min desaq"
 2. Natação      — "1000m aquecimento + 8x100m técnica + 500m volta à calma"
                   "800m aquec + 6x50m drill + 8x100m técnica + 300m desaq"
 3. Brick        — "60min bike Z2 + 30min corrida Z3"
                   "35min natação Z2 + transição + 40min corrida Z3"
                   "60min bike Z2-Z3 + transição + 30min corrida Z3"
 4. Progressivo  — "15min Z2 + 25min Z3 + 15min Z2"
                   "15min aquec + 30min Z3 + 15min desaq"
                   "15min aquec + 20min Z4 + 15min desaq"
 5. Fartlek      — "15min aquec + 8x(2min Z4 + 2min Z2) + 10min desaq"
                   "15min aquec + 5x(4min Z5 + 3min rec) + 10min desaq"
                   "10min aquec + 30min fartlek Z2-Z3 + 10min desaq"
 6. Contínuo     — "Corrida leve e contínua" / "Ritmo constante em terreno plano"
                   "3000m contínuo com foco na técnica" / "2500m contínuo suave"
 7. Final forte  — "Corrida longa com 20min finais Z3"
 8. Dia de prova — "🏁 DIA DA MARATONA - Boa sorte!"

Fallback: se nenhum padrão é reconhecido, gera um único step ACTIVE.
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from exporters.workout import StepType, WorkoutStep


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _hr_for_zone(
    zone_num: Optional[int],
    zone_config: Dict[int, Tuple[int, int]],
) -> Tuple[Optional[int], Optional[int]]:
    """Retorna (hr_low, hr_high) para uma zona, ou (None, None)."""
    if zone_num and zone_num in zone_config:
        return zone_config[zone_num]
    return (None, None)


def _make_step(
    step_type: StepType,
    duration_seconds: int = 0,
    zone_num: Optional[int] = None,
    zone_config: Optional[Dict[int, Tuple[int, int]]] = None,
    distance_meters: Optional[float] = None,
    repeat_count: int = 1,
    description: str = "",
) -> WorkoutStep:
    """Cria um WorkoutStep com HR preenchido a partir da zona."""
    hr_low, hr_high = _hr_for_zone(zone_num, zone_config or {})
    return WorkoutStep(
        step_type=step_type,
        duration_seconds=duration_seconds,
        target_zone=zone_num,
        target_hr_low=hr_low,
        target_hr_high=hr_high,
        repeat_count=repeat_count,
        distance_meters=distance_meters,
        description=description,
    )


def _extract_zone_from_text(text: str) -> Optional[int]:
    """Extrai número de zona (1-5) de fragmentos como 'Z2', 'Z2-Z3', etc.

    Para ranges (Z2-Z3), retorna a zona mais baixa.
    """
    m = re.search(r"Z(\d)", text)
    return int(m.group(1)) if m else None


def _parse_duration_fragment(text: str) -> int:
    """Parseia fragmentos como '15min', '2min', '30s' em segundos."""
    text = text.strip().lower()

    m = re.match(r"(\d+)\s*min", text)
    if m:
        return int(m.group(1)) * 60

    m = re.match(r"(\d+)\s*s$", text)
    if m:
        return int(m.group(1))

    m = re.match(r"(\d+)\s*h", text)
    if m:
        return int(m.group(1)) * 3600

    try:
        return int(text) * 60  # assume minutos
    except ValueError:
        return 0


def _parse_distance_fragment(text: str) -> float:
    """Parseia fragmentos como '800m', '1km', '1000m' em metros."""
    text = text.strip().lower()

    m = re.match(r"(\d+(?:\.\d+)?)\s*km", text)
    if m:
        return float(m.group(1)) * 1000

    m = re.match(r"(\d+(?:\.\d+)?)\s*m", text)
    if m:
        return float(m.group(1))

    return 0.0


# ---------------------------------------------------------------------------
# Detectores de padrão
# ---------------------------------------------------------------------------

# Padrão 1: Intervalado com aquecimento/desaquecimento
# "15min aquec + 6x800m (rec 2min) + 10min desaq"
# "20min aquec + 6x5min alta intensidade (rec 3min) + 15min desaq"
# "20min aquec + 3x15min no limiar (rec 5min) + 15min desaq"
# "500m aquec + 10x200m (rec 30s) + 300m desaq"
# "1000m aquec + 20x100m (rec 15s) + 500m desaq"
_RE_INTERVAL_FULL = re.compile(
    r"(\d+\s*(?:min|m|km))\s*(?:aquec(?:imento)?)\s*\+"
    r"\s*(\d+)\s*x\s*(\d+\s*(?:min|m|km|s))\b"
    r"(?:\s+[^\(]*)?"  # texto opcional (ex: "alta intensidade", "técnica", "no limiar")
    r"\s*(?:\(\s*rec\s*(\d+\s*(?:min|s))\s*\))?"
    r"(?:\s*\+\s*(\d+\s*(?:min|m|km))\s*(?:desaq(?:uecimento)?|volta\s*[àa]\s*calma))?"
    , re.IGNORECASE
)

# Padrão 2: Brick / Multisport (com zona simples ou range)
# "60min bike Z2 + 30min corrida Z3"
# "35min natação Z2 + transição + 40min corrida Z3"
# "60min bike Z2-Z3 + transição + 30min corrida Z3"
# "90min bike Z2 + 30min corrida Z2"
_RE_BRICK = re.compile(
    r"(\d+\s*min)\s+\w+\s+(Z\d)(?:-Z\d)?"
    r"(?:\s*\+\s*(?:transição\s*\+\s*)?)"
    r"(\d+\s*min)\s+\w+\s+(Z\d)(?:-Z\d)?"
    , re.IGNORECASE
)

# Padrão 3: Fartlek com blocos zona
# "15min aquec + 8x(2min Z4 + 2min Z2) + 10min desaq"
_RE_FARTLEK = re.compile(
    r"(\d+\s*min)\s*aquec\s*\+"
    r"\s*(\d+)\s*x\s*\(\s*(\d+\s*min)\s*(Z\d)\s*\+\s*(\d+\s*min)\s*(Z\d)\s*\)"
    r"\s*\+\s*(\d+\s*min)\s*desaq"
    , re.IGNORECASE
)

# Padrão 3b: Fartlek com "rec" em vez de zona
# "15min aquec + 5x(4min Z5 + 3min rec) + 10min desaq"
# "15min aquec + 4x(2min Z4 + 3min rec) + 10min desaq"
_RE_FARTLEK_REC = re.compile(
    r"(\d+\s*min)\s*aquec\s*\+"
    r"\s*(\d+)\s*x\s*\(\s*(\d+\s*min)\s*(Z\d)\s*\+\s*(\d+\s*min)\s*rec\s*\)"
    r"\s*\+\s*(\d+\s*min)\s*desaq"
    , re.IGNORECASE
)

# Padrão 3c: Fartlek contínuo sem blocos repetidos
# "10min aquec + 30min fartlek Z2-Z3 + 10min desaq"
_RE_FARTLEK_CONTINUOUS = re.compile(
    r"(\d+\s*min)\s*aquec\s*\+"
    r"\s*(\d+\s*min)\s*fartlek\s*(Z\d)(?:-(Z\d))?"
    r"\s*\+\s*(\d+\s*min)\s*desaq"
    , re.IGNORECASE
)

# Padrão 4: Contínuo com distância (natação)
# "3000m contínuo com foco na técnica"
# "2500m contínuo moderado"
# "1800m contínuo suave"
# "2000m contínuo suave"
# "2500m contínuo em ritmo confortável"
_RE_CONTINUOUS_DIST = re.compile(
    r"^(\d+)\s*m\s+cont[ií]nuo",
    re.IGNORECASE
)

# Padrão 5: Dia de prova
# "🏁 DIA DA MARATONA - Boa sorte!"
# "🏁 DIA DA PROVA - Boa sorte!"
_RE_RACE_DAY = re.compile(
    r"(?:🏁|DIA\s+D[AO])",
    re.IGNORECASE
)


# ---------------------------------------------------------------------------
# Parser principal
# ---------------------------------------------------------------------------

def parse_description(
    descricao: str,
    total_duration_seconds: int,
    default_zone: Optional[int] = None,
    zone_config: Optional[Dict[int, Tuple[int, int]]] = None,
) -> List[WorkoutStep]:
    """Parseia uma descrição de treino em português para steps estruturados.

    Args:
        descricao: Texto descritivo do treino (ex: "15min aquec + 6x800m ...").
        total_duration_seconds: Duração total do treino em segundos.
        default_zone: Zona de HR padrão (1-5) do treino.
        zone_config: Mapa zona→(hr_low, hr_high) em BPM.

    Returns:
        Lista de WorkoutStep. Nunca retorna lista vazia.
    """
    zc = zone_config or {}

    # Remover sufixos de ajuste (health/menstrual)
    clean = re.split(r"\s*\|\s*[⚕🌸]", descricao)[0].strip()

    if not clean:
        return [_make_step(StepType.ACTIVE, total_duration_seconds,
                           default_zone, zc)]

    # --- Dia de prova: step único especial ---
    if _RE_RACE_DAY.search(clean):
        return [_make_step(StepType.ACTIVE, total_duration_seconds,
                           default_zone, zc, description=clean)]

    # --- Tentar Fartlek com blocos zona ---
    m = _RE_FARTLEK.search(clean)
    if m:
        return _parse_fartlek(m, default_zone, zc)

    # --- Tentar Fartlek com "rec" em vez de zona ---
    m = _RE_FARTLEK_REC.search(clean)
    if m:
        return _parse_fartlek_rec(m, default_zone, zc)

    # --- Tentar Fartlek contínuo (sem blocos) ---
    m = _RE_FARTLEK_CONTINUOUS.search(clean)
    if m:
        return _parse_fartlek_continuous(m, zc)

    # --- Tentar Brick/Multisport ---
    m = _RE_BRICK.search(clean)
    if m:
        return _parse_brick(m, zc)

    # --- Tentar natação estruturada (warmup + reps + cooldown) ---
    # Deve vir ANTES do intervalado para capturar "volta à calma"
    steps = _try_parse_swim_structured(clean, default_zone, zc)
    if steps:
        return steps

    # --- Tentar Intervalado completo ---
    m = _RE_INTERVAL_FULL.search(clean)
    if m:
        return _parse_interval(m, default_zone, zc)

    # --- Tentar segmentos progressivos ---
    steps = _try_parse_segments(clean, zc, total_duration_seconds)
    if steps:
        return steps

    # --- Contínuo com distância (natação) ---
    m = _RE_CONTINUOUS_DIST.search(clean)
    if m:
        meters = float(m.group(1))
        return [_make_step(StepType.ACTIVE, total_duration_seconds,
                           default_zone, zc, distance_meters=meters,
                           description=clean)]

    # --- Treino com final especial: "Corrida longa com 20min finais Z3" ---
    m = re.search(r"(\d+)\s*min\s*finais?\s*(Z\d)", clean, re.IGNORECASE)
    if m and total_duration_seconds > 0:
        final_secs = int(m.group(1)) * 60
        final_zone = int(m.group(2)[1])
        main_secs = max(total_duration_seconds - final_secs, 0)
        steps_list = []
        if main_secs > 0:
            steps_list.append(_make_step(StepType.ACTIVE, main_secs,
                                         default_zone, zc))
        steps_list.append(_make_step(StepType.ACTIVE, final_secs,
                                     final_zone, zc, description="Finais"))
        return steps_list

    # --- Fallback: step único ACTIVE ---
    return [_make_step(StepType.ACTIVE, total_duration_seconds,
                       default_zone, zc, description=clean)]


# ---------------------------------------------------------------------------
# Parsers específicos
# ---------------------------------------------------------------------------

def _parse_interval(
    m: re.Match,
    default_zone: Optional[int],
    zc: Dict[int, Tuple[int, int]],
) -> List[WorkoutStep]:
    """Parseia intervalado: aquec + NxDist (rec X) + desaq."""
    steps: List[WorkoutStep] = []

    warmup_raw = m.group(1)
    reps = int(m.group(2))
    interval_raw = m.group(3)
    recovery_raw = m.group(4)
    cooldown_raw = m.group(5)

    # Warmup — pode ser em metros (natação) ou minutos (corrida/ciclismo)
    warmup_dist = _parse_distance_fragment(warmup_raw)
    warmup_zone = default_zone if default_zone and default_zone <= 2 else 2
    if warmup_dist > 0 and "m" in warmup_raw.lower() and "min" not in warmup_raw.lower():
        steps.append(_make_step(StepType.WARMUP, 0, warmup_zone, zc,
                                distance_meters=warmup_dist))
    else:
        warmup_secs = _parse_duration_fragment(warmup_raw)
        steps.append(_make_step(StepType.WARMUP, warmup_secs, warmup_zone, zc))

    # Intervalo — pode ser distância ou duração
    interval_dist = _parse_distance_fragment(interval_raw)
    interval_secs = _parse_duration_fragment(interval_raw)

    # Recovery
    recovery_secs = _parse_duration_fragment(recovery_raw) if recovery_raw else 0

    # Zona do intervalo: geralmente mais alta que o default
    interval_zone = default_zone if default_zone and default_zone >= 3 else (default_zone or 4)
    recovery_zone = 1  # recuperação sempre Z1

    for _ in range(reps):
        if interval_dist > 0 and "m" in interval_raw.lower() and "min" not in interval_raw.lower():
            steps.append(_make_step(StepType.INTERVAL, interval_secs,
                                    interval_zone, zc,
                                    distance_meters=interval_dist))
        else:
            steps.append(_make_step(StepType.INTERVAL, interval_secs,
                                    interval_zone, zc))

        if recovery_secs > 0:
            steps.append(_make_step(StepType.RECOVERY, recovery_secs,
                                    recovery_zone, zc))

    # Cooldown
    if cooldown_raw:
        cooldown_dist = _parse_distance_fragment(cooldown_raw)
        if cooldown_dist > 0 and "m" in cooldown_raw.lower() and "min" not in cooldown_raw.lower():
            steps.append(_make_step(StepType.COOLDOWN, 0, warmup_zone, zc,
                                    distance_meters=cooldown_dist))
        else:
            cooldown_secs = _parse_duration_fragment(cooldown_raw)
            steps.append(_make_step(StepType.COOLDOWN, cooldown_secs,
                                    warmup_zone, zc))

    return steps


def _parse_fartlek(
    m: re.Match,
    default_zone: Optional[int],
    zc: Dict[int, Tuple[int, int]],
) -> List[WorkoutStep]:
    """Parseia fartlek: aquec + Nx(Xmin ZN + Xmin ZN) + desaq."""
    warmup_secs = _parse_duration_fragment(m.group(1))
    reps = int(m.group(2))
    on_secs = _parse_duration_fragment(m.group(3))
    on_zone = int(m.group(4)[1])
    off_secs = _parse_duration_fragment(m.group(5))
    off_zone = int(m.group(6)[1])
    cooldown_secs = _parse_duration_fragment(m.group(7))

    steps: List[WorkoutStep] = []
    steps.append(_make_step(StepType.WARMUP, warmup_secs, 2, zc))

    for _ in range(reps):
        steps.append(_make_step(StepType.INTERVAL, on_secs, on_zone, zc))
        steps.append(_make_step(StepType.RECOVERY, off_secs, off_zone, zc))

    steps.append(_make_step(StepType.COOLDOWN, cooldown_secs, 2, zc))
    return steps


def _parse_fartlek_rec(
    m: re.Match,
    default_zone: Optional[int],
    zc: Dict[int, Tuple[int, int]],
) -> List[WorkoutStep]:
    """Parseia fartlek com 'rec': aquec + Nx(Xmin ZN + Xmin rec) + desaq."""
    warmup_secs = _parse_duration_fragment(m.group(1))
    reps = int(m.group(2))
    on_secs = _parse_duration_fragment(m.group(3))
    on_zone = int(m.group(4)[1])
    off_secs = _parse_duration_fragment(m.group(5))
    cooldown_secs = _parse_duration_fragment(m.group(6))

    steps: List[WorkoutStep] = []
    steps.append(_make_step(StepType.WARMUP, warmup_secs, 2, zc))

    for _ in range(reps):
        steps.append(_make_step(StepType.INTERVAL, on_secs, on_zone, zc))
        steps.append(_make_step(StepType.RECOVERY, off_secs, 1, zc))

    steps.append(_make_step(StepType.COOLDOWN, cooldown_secs, 2, zc))
    return steps


def _parse_fartlek_continuous(
    m: re.Match,
    zc: Dict[int, Tuple[int, int]],
) -> List[WorkoutStep]:
    """Parseia fartlek contínuo: aquec + Xmin fartlek ZN(-ZN) + desaq.

    Ex: "10min aquec + 30min fartlek Z2-Z3 + 10min desaq"
    """
    warmup_secs = _parse_duration_fragment(m.group(1))
    main_secs = _parse_duration_fragment(m.group(2))
    zone_low = int(m.group(3)[1])
    zone_high = int(m.group(4)[1]) if m.group(4) else zone_low
    cooldown_secs = _parse_duration_fragment(m.group(5))

    return [
        _make_step(StepType.WARMUP, warmup_secs, 2, zc),
        _make_step(StepType.ACTIVE, main_secs, zone_low, zc,
                   description=f"Fartlek Z{zone_low}-Z{zone_high}"),
        _make_step(StepType.COOLDOWN, cooldown_secs, 2, zc),
    ]


def _parse_brick(
    m: re.Match,
    zc: Dict[int, Tuple[int, int]],
) -> List[WorkoutStep]:
    """Parseia brick: Xmin sport Z + (transição +) Xmin sport Z."""
    seg1_secs = _parse_duration_fragment(m.group(1))
    seg1_zone = int(m.group(2)[1])
    seg2_secs = _parse_duration_fragment(m.group(3))
    seg2_zone = int(m.group(4)[1])

    return [
        _make_step(StepType.ACTIVE, seg1_secs, seg1_zone, zc,
                   description="Segmento 1"),
        _make_step(StepType.REST, 120, 1, zc, description="Transição"),
        _make_step(StepType.ACTIVE, seg2_secs, seg2_zone, zc,
                   description="Segmento 2"),
    ]


def _try_parse_swim_structured(
    text: str,
    default_zone: Optional[int],
    zc: Dict[int, Tuple[int, int]],
) -> Optional[List[WorkoutStep]]:
    """Tenta parsear estrutura de natação com aquecimento + séries + volta à calma.

    Exemplos:
      "800m aquec + 6x50m drill + 8x100m técnica + 300m desaq"
      "1000m aquecimento + 8x100m técnica + 500m volta à calma"
      "1000m aquecimento + 6x100m técnica + 400m volta à calma"
    """
    # Se tem "(rec" é intervalado com recovery, não natação pura
    if "(rec" in text.lower() or "( rec" in text.lower():
        return None

    # Procurar por aquecimento em metros
    warmup_match = re.match(r"(\d+)\s*m\s*(?:aquec(?:imento)?)", text, re.IGNORECASE)
    if not warmup_match:
        return None

    warmup_meters = float(warmup_match.group(1))

    # Procurar cooldown (volta à calma / desaq)
    cooldown_match = re.search(
        r"(\d+)\s*m\s*(?:volta\s*[àa]\s*calma|desaq(?:uecimento)?)\s*$",
        text, re.IGNORECASE
    )

    # Extrair todas as séries NxMm
    series = re.findall(r"(\d+)\s*x\s*(\d+)\s*m\b", text)

    if not series:
        return None

    steps: List[WorkoutStep] = []
    warmup_zone = default_zone if default_zone and default_zone <= 2 else 2

    steps.append(_make_step(StepType.WARMUP, 0, warmup_zone, zc,
                            distance_meters=warmup_meters))

    for reps_str, dist_str in series:
        reps = int(reps_str)
        dist = float(dist_str)
        for _ in range(reps):
            steps.append(_make_step(StepType.INTERVAL, 0, default_zone, zc,
                                    distance_meters=dist))

    if cooldown_match:
        cooldown_meters = float(cooldown_match.group(1))
        steps.append(_make_step(StepType.COOLDOWN, 0, warmup_zone, zc,
                                distance_meters=cooldown_meters))

    return steps


def _try_parse_segments(
    text: str,
    zc: Dict[int, Tuple[int, int]],
    total_duration_seconds: int,
) -> Optional[List[WorkoutStep]]:
    """Parseia segmentos com zonas: "15min Z2 + 25min Z3 + 15min Z2".

    Também captura:
      "15min aquec + 30min Z3 + 15min desaq"
      "15min aquec + 20min Z4 + 15min desaq"
    """
    # Encontrar todos os fragmentos "Xmin ZN" ou "Xmin aquec/desaq"
    pattern = r"(\d+)\s*min\s+(?:(Z\d)(?:-Z\d)?|aquec(?:imento)?|desaq(?:uecimento)?)"
    matches = list(re.finditer(pattern, text, re.IGNORECASE))

    if len(matches) < 2:
        return None

    steps: List[WorkoutStep] = []

    for i, match in enumerate(matches):
        secs = int(match.group(1)) * 60
        zone_str = match.group(2)
        zone_num = int(zone_str[1]) if zone_str else 2

        # Determinar tipo do step
        full_match = match.group(0).lower()
        if "aquec" in full_match or (i == 0 and "aquec" in text[:match.end()].lower()):
            step_type = StepType.WARMUP
        elif "desaq" in full_match or (i == len(matches) - 1 and "desaq" in text[match.start():].lower()):
            step_type = StepType.COOLDOWN
        else:
            step_type = StepType.ACTIVE

        steps.append(_make_step(step_type, secs, zone_num, zc))

    return steps if steps else None
