"""
Templates de Prompts para Treino Desportivo
=============================================

Cada função devolve (system_prompt, user_prompt) prontos
para enviar ao LLM. Textos em Português (Brasil) com
fallback contextual.
"""

from typing import Dict, List, Tuple


# ── System Prompt base ───────────────────────────────────────────

SYSTEM_PROMPT = """Você é um assistente de IA especializado em planejamento de treino desportivo.
Você auxilia profissionais de Educação Física (CREF) na criação e ajuste de planos de treino.

Regras:
1. Baseie-se em evidência científica (ACSM, NSCA, literatura peer-reviewed).
2. Respeite as variáveis de treino informadas pelo treinador.
3. Considere periodização, zonas de treino e saúde do atleta.
4. Responda de forma objetiva e profissional.
5. Use terminologia técnica correta em Português do Brasil.
6. Nunca substitua o julgamento clínico do profissional.
7. Se não tiver informação suficiente, peça esclarecimento.
"""


def _format_sessions(sessions: List[Dict]) -> str:
    """Formata sessões de treino para o prompt."""
    if not sessions:
        return "(nenhuma sessão fornecida)"
    lines = []
    for i, s in enumerate(sessions, 1):
        parts = [
            f"  Dia: {s.get('dia', '?')}",
            f"  Modalidade: {s.get('modalidade', '?')}",
            f"  Duração: {s.get('duracao', '?')} min",
            f"  Tipo: {s.get('tipo', '?')}",
            f"  Zona: {s.get('zona', '?')}",
            f"  Fase: {s.get('fase', '?')}",
            f"  Semana: {s.get('semana', '?')} ({s.get('tipo_semana', '?')})",
        ]
        desc = s.get("descricao", "")
        if desc:
            parts.append(f"  Descrição: {desc}")
        lines.append(f"Sessão {i}:\n" + "\n".join(parts))
    return "\n\n".join(lines)


def _format_athlete_info(athlete: Dict) -> str:
    """Formata dados do atleta para o prompt."""
    if not athlete:
        return "(dados do atleta não informados)"
    parts = []
    if athlete.get("nome"):
        parts.append(f"Nome: {athlete['nome']}")
    if athlete.get("idade"):
        parts.append(f"Idade: {athlete['idade']} anos")
    if athlete.get("sexo"):
        parts.append(f"Sexo: {athlete['sexo']}")
    if athlete.get("nivel"):
        parts.append(f"Nível: {athlete['nivel']}")
    if athlete.get("objetivo"):
        parts.append(f"Objetivo: {athlete['objetivo']}")
    if athlete.get("restricoes"):
        parts.append(f"Restrições de saúde: {athlete['restricoes']}")
    if athlete.get("modalidade"):
        parts.append(f"Modalidade principal: {athlete['modalidade']}")
    return "\n".join(parts) if parts else "(dados do atleta não informados)"


# ── Templates ────────────────────────────────────────────────────

def optimize_plan(
    sessions: List[Dict],
    athlete: Dict,
    goal: str = "",
) -> Tuple[str, str]:
    """Prompt para otimizar um plano de treino completo."""
    user = f"""Analise e otimize o seguinte plano de treino:

## Dados do Atleta
{_format_athlete_info(athlete)}

## Objetivo adicional
{goal or '(nenhum objetivo adicional)'}

## Sessões do Plano
{_format_sessions(sessions)}

Por favor:
1. Avalie a distribuição de carga e recuperação.
2. Identifique pontos de melhoria na periodização.
3. Sugira ajustes concretos com justificativa.
4. Mantenha o volume total compatível com o nível do atleta.

Responda de forma estruturada com seções claras."""

    return SYSTEM_PROMPT, user


def suggest_workout_edit(
    session: Dict,
    context: str = "",
) -> Tuple[str, str]:
    """Prompt para sugerir edição numa sessão específica."""
    user = f"""Sugira melhorias para esta sessão de treino:

## Sessão
{_format_sessions([session])}

## Contexto do treinador
{context or '(sem contexto adicional)'}

Por favor:
1. Proponha 2-3 variações da sessão.
2. Justifique cada alteração.
3. Indique a intensidade relativa (RPE ou % FC máx).

Responda de forma concisa e prática."""

    return SYSTEM_PROMPT, user


def explain_periodization(
    phase: str,
    sport: str = "",
    weeks: int = 0,
) -> Tuple[str, str]:
    """Prompt para explicar uma fase da periodização."""
    user = f"""Explique a fase de periodização:

Fase: {phase}
Modalidade: {sport or '(geral)'}
Duração: {weeks or '?'} semanas

Por favor:
1. Descreva os objetivos fisiológicos desta fase.
2. Indique a distribuição ideal de volume e intensidade.
3. Dê exemplos de sessões-tipo.
4. Explique a transição para a fase seguinte.

Use linguagem técnica acessível."""

    return SYSTEM_PROMPT, user


def adjust_for_health(
    sessions: List[Dict],
    condition: str,
    athlete: Dict,
) -> Tuple[str, str]:
    """Prompt para ajustar treino a condições de saúde."""
    user = f"""Ajuste o plano de treino para a seguinte condição de saúde:

## Condição
{condition}

## Dados do Atleta
{_format_athlete_info(athlete)}

## Sessões atuais
{_format_sessions(sessions)}

Por favor:
1. Identifique exercícios contraindicados.
2. Sugira substituições seguras.
3. Ajuste volume e intensidade conforme necessário.
4. Indique sinais de alerta a monitorizar.

IMPORTANTE: Esta é uma assistência ao profissional de saúde, não substitui avaliação médica."""

    return SYSTEM_PROMPT, user


def weekly_analysis(
    sessions: List[Dict],
    week_number: int,
    phase: str,
    week_type: str,
) -> Tuple[str, str]:
    """Prompt para análise de uma semana de treino."""
    user = f"""Analise a semana de treino:

## Contexto
Semana: {week_number}
Fase: {phase}
Tipo de semana: {week_type}

## Sessões da semana
{_format_sessions(sessions)}

Por favor:
1. Avalie a distribuição de carga ao longo da semana.
2. Verifique se os dias de descanso são adequados.
3. Analise a progressão de intensidade.
4. Dê uma nota de 1-10 e justifique.

Responda de forma objetiva e prática."""

    return SYSTEM_PROMPT, user


def race_strategy(
    race_info: Dict,
    athlete: Dict,
    recent_sessions: List[Dict],
) -> Tuple[str, str]:
    """Prompt para estratégia de prova/competição."""
    race_parts = []
    if race_info.get("nome"):
        race_parts.append(f"Prova: {race_info['nome']}")
    if race_info.get("distancia"):
        race_parts.append(f"Distância: {race_info['distancia']}")
    if race_info.get("data"):
        race_parts.append(f"Data: {race_info['data']}")
    if race_info.get("tipo"):
        race_parts.append(f"Tipo: {race_info['tipo']}")
    race_text = "\n".join(race_parts) if race_parts else "(detalhes da prova não informados)"

    user = f"""Desenvolva uma estratégia para a prova:

## Prova
{race_text}

## Atleta
{_format_athlete_info(athlete)}

## Treinos recentes
{_format_sessions(recent_sessions)}

Por favor:
1. Sugira uma estratégia de ritmo (pacing).
2. Defina zonas de intensidade para cada trecho.
3. Indique precauções (nutrição, hidratação, clima).
4. Proponha um plano de tapering pré-prova.

Responda de forma prática e aplicável."""

    return SYSTEM_PROMPT, user
