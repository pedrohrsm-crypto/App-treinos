"""
Notification Engine — Motor de notificações
============================================

Calcula notificações pendentes com base nos planos e calendários
existentes: próximo treino, semana de prova, atleta inativo, etc.
"""

from datetime import datetime, date, timedelta
from typing import List, Dict
from training_manager import training_manager


def get_pending_notifications(trainer_info) -> List[Dict]:
    """
    Gera lista de notificações pendentes para o treinador.

    Returns:
        List[Dict]: cada notificação tem:
            type: 'training' | 'deadline' | 'inactive' | 'info'
            icon: emoji
            title: str
            detail: str
            priority: int (1=alta, 3=baixa)
    """
    if not trainer_info:
        return []

    notifications = []
    today = date.today()
    now = datetime.now()

    plans = training_manager.get_trainer_plans(trainer_info)

    # Agrupar por atleta
    athletes: Dict[str, list] = {}
    for p in plans:
        athletes.setdefault(p.athlete_name, []).append(p)

    for athlete_name, athlete_plans in athletes.items():
        for plan in athlete_plans:
            try:
                created = datetime.fromisoformat(plan.created_at)
            except (ValueError, TypeError):
                created = now

            elapsed_weeks = max((now - created).days // 7, 0)
            total_weeks = plan.weeks or 1

            # ── Treino de hoje/amanhã ────────────────────────────
            calendar = training_manager.get_calendar(trainer_info, plan.id)
            today_key = today.isoformat()
            tomorrow_key = (today + timedelta(days=1)).isoformat()

            today_sessions = calendar.get(today_key, [])
            tomorrow_sessions = calendar.get(tomorrow_key, [])

            if today_sessions:
                tipos = ", ".join(s.get("tipo", "?") for s in today_sessions[:3])
                notifications.append({
                    "type": "training",
                    "icon": "alarm",
                    "title": f"Treino hoje — {athlete_name}",
                    "detail": f"{len(today_sessions)} sessão(ões): {tipos}",
                    "priority": 1,
                })

            if tomorrow_sessions:
                tipos = ", ".join(s.get("tipo", "?") for s in tomorrow_sessions[:3])
                notifications.append({
                    "type": "training",
                    "icon": "calendar_today",
                    "title": f"Treino amanhã — {athlete_name}",
                    "detail": f"{len(tomorrow_sessions)} sessão(ões): {tipos}",
                    "priority": 2,
                })

            # ── Semana de prova se aproximando ───────────────────
            remaining_weeks = total_weeks - elapsed_weeks
            if 0 < remaining_weeks <= 2:
                notifications.append({
                    "type": "deadline",
                    "icon": "flag",
                    "title": f"Prova próxima — {athlete_name}",
                    "detail": f"Faltam {remaining_weeks} semana(s) para a prova ({plan.sport} {plan.distance}).",
                    "priority": 1,
                })

            # ── Plano sem edição há muito tempo ──────────────────
            days_since = (now - created).days
            if days_since > 14 and not calendar:
                notifications.append({
                    "type": "info",
                    "icon": "assignment",
                    "title": f"Plano sem calendário — {athlete_name}",
                    "detail": f"Plano criado há {days_since} dias sem mapeamento de calendário.",
                    "priority": 3,
                })

            # ── Atleta sem treino há 3+ dias ─────────────────────
            if calendar:
                recent_dates = sorted(calendar.keys(), reverse=True)
                last_training_date = None
                for dk in recent_dates:
                    try:
                        d = date.fromisoformat(dk)
                        if d <= today:
                            last_training_date = d
                            break
                    except ValueError:
                        continue
                if last_training_date and (today - last_training_date).days > 3:
                    notifications.append({
                        "type": "inactive",
                        "icon": "warning",
                        "title": f"Atleta inativo — {athlete_name}",
                        "detail": f"Último treino agendado: {last_training_date.isoformat()} ({(today - last_training_date).days} dias atrás).",
                        "priority": 2,
                    })

    # Ordenar por prioridade
    notifications.sort(key=lambda n: n["priority"])
    return notifications
