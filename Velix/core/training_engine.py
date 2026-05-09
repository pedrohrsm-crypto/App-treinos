"""
Core Training Engine — Re-exporta do módulo canônico training_planner.py
=========================================================================

Este módulo existia como cópia independente do training_planner.py.
Foi unificado em 28/03/2026 para eliminar duplicação de código (96.5% idêntico).

Todas as classes e funções agora são importadas de training_planner.py,
que é o módulo canônico mantido na raiz do projeto.
"""

import sys
from pathlib import Path

# Garantir que o diretório raiz do projeto está no path
_project_root = str(Path(__file__).parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from training_planner import (
    calcular_semanas_ate_prova,
    HealthIssue,
    TrainerInfo,
    Athlete,
    HealthAdvisor,
    PeriodizationPlanner,
    TrainingZones,
    TrainingPlanGenerator,
    ExcelExporter,
)

__all__ = [
    "calcular_semanas_ate_prova",
    "HealthIssue",
    "TrainerInfo",
    "Athlete",
    "HealthAdvisor",
    "PeriodizationPlanner",
    "TrainingZones",
    "TrainingPlanGenerator",
    "ExcelExporter",
]
