"""
Core Package - Motor de Treinamento
===================================

Re-exporta classes e funções do módulo canônico training_planner.py.
"""

from .training_engine import (
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
