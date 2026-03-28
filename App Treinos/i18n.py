"""
Sistema de Internacionalização (i18n)
=====================================

Fornece tradução de strings para PT-BR, EN e ES.
Uso: from i18n import t, set_language, get_language
     label.config(text=t('app_name'))
"""

from typing import Dict

_current_language = "pt"

_translations: Dict[str, Dict[str, str]] = {
    # ── Geral ────────────────────────────────────────────────────
    "app_name": {
        "pt": "App Treinos",
        "en": "Training App",
        "es": "App Entrenamientos",
    },
    "app_subtitle": {
        "pt": "Sistema Profissional de Planejamento Esportivo",
        "en": "Professional Sports Planning System",
        "es": "Sistema Profesional de Planificación Deportiva",
    },

    # ── Splash ───────────────────────────────────────────────────
    "splash_subtitle": {
        "pt": "Sistema Profissional de Planejamento Esportivo",
        "en": "Professional Sports Planning System",
        "es": "Sistema Profesional de Planificación Deportiva",
    },

    # ── Login ────────────────────────────────────────────────────
    "login_title": {
        "pt": "Acesso Profissional",
        "en": "Professional Access",
        "es": "Acceso Profesional",
    },
    "login_cpf_cref": {
        "pt": "CPF ou CREF",
        "en": "CPF or CREF",
        "es": "CPF o CREF",
    },
    "login_password": {
        "pt": "Senha",
        "en": "Password",
        "es": "Contraseña",
    },
    "login_button": {
        "pt": "Entrar",
        "en": "Sign In",
        "es": "Iniciar Sesión",
    },
    "login_create_account": {
        "pt": "Criar Nova Conta",
        "en": "Create New Account",
        "es": "Crear Nueva Cuenta",
    },
    "login_admin": {
        "pt": "Acesso Administrativo",
        "en": "Admin Access",
        "es": "Acceso Administrativo",
    },

    # ── Dashboard ────────────────────────────────────────────────
    "dashboard_greeting": {
        "pt": "Olá, {name}! O que você deseja fazer hoje?",
        "en": "Hello, {name}! What would you like to do today?",
        "es": "¡Hola, {name}! ¿Qué deseas hacer hoy?",
    },
    "dashboard_choose": {
        "pt": "Escolha uma opção abaixo para começar",
        "en": "Choose an option below to get started",
        "es": "Elige una opción para comenzar",
    },
    "card_new_plan": {
        "pt": "Novo Plano",
        "en": "New Plan",
        "es": "Nuevo Plan",
    },
    "card_new_plan_desc": {
        "pt": "Crie um novo plano de treinamento personalizado para seu atleta",
        "en": "Create a personalized training plan for your athlete",
        "es": "Crea un plan de entrenamiento personalizado para tu atleta",
    },
    "card_edit_plan": {
        "pt": "Editar Plano",
        "en": "Edit Plan",
        "es": "Editar Plan",
    },
    "card_edit_plan_desc": {
        "pt": "Visualize, edite ou exporte planos de treinamento já criados",
        "en": "View, edit or export previously created training plans",
        "es": "Visualiza, edita o exporta planes ya creados",
    },
    "card_export_pdf": {
        "pt": "Exportar PDF",
        "en": "Export PDF",
        "es": "Exportar PDF",
    },
    "card_export_pdf_desc": {
        "pt": "Exporte planos de treinamento em formato PDF profissional",
        "en": "Export training plans in professional PDF format",
        "es": "Exporta planes de entrenamiento en formato PDF profesional",
    },
    "card_progress": {
        "pt": "Meu Progresso",
        "en": "My Progress",
        "es": "Mi Progreso",
    },
    "card_progress_desc": {
        "pt": "Visualize estatísticas e histórico dos seus treinamentos",
        "en": "View statistics and history of your training plans",
        "es": "Visualiza estadísticas e historial de tus entrenamientos",
    },
    "card_click_hint": {
        "pt": "Clique para começar →",
        "en": "Click to start →",
        "es": "Haz clic para empezar →",
    },

    # ── Progresso ────────────────────────────────────────────────
    "progress_title": {
        "pt": "Dashboard de Progresso",
        "en": "Progress Dashboard",
        "es": "Panel de Progreso",
    },
    "progress_plans_created": {
        "pt": "Planos Criados",
        "en": "Plans Created",
        "es": "Planes Creados",
    },
    "progress_unique_athletes": {
        "pt": "Atletas Únicos",
        "en": "Unique Athletes",
        "es": "Atletas Únicos",
    },
    "progress_sports": {
        "pt": "Modalidades",
        "en": "Sports",
        "es": "Modalidades",
    },
    "progress_latest": {
        "pt": "Último Plano",
        "en": "Latest Plan",
        "es": "Último Plan",
    },
    "progress_distribution": {
        "pt": "Distribuição por Modalidade",
        "en": "Distribution by Sport",
        "es": "Distribución por Modalidad",
    },
    "progress_recent": {
        "pt": "Planos Recentes",
        "en": "Recent Plans",
        "es": "Planes Recientes",
    },
    "progress_changelog": {
        "pt": "Histórico de Alterações",
        "en": "Change History",
        "es": "Historial de Cambios",
    },
    "progress_empty": {
        "pt": "Nenhum treino criado ainda",
        "en": "No training plans created yet",
        "es": "Aún no se crearon entrenamientos",
    },
    "progress_empty_hint": {
        "pt": "Crie seu primeiro plano de treino para ver estatísticas aqui!",
        "en": "Create your first training plan to see statistics here!",
        "es": "¡Crea tu primer plan de entrenamiento para ver estadísticas aquí!",
    },

    # ── Wizard ───────────────────────────────────────────────────
    "wizard_step": {
        "pt": "Etapa {current} de {total}",
        "en": "Step {current} of {total}",
        "es": "Paso {current} de {total}",
    },
    "wizard_next": {
        "pt": "Próximo →",
        "en": "Next →",
        "es": "Siguiente →",
    },
    "wizard_prev": {
        "pt": "← Anterior",
        "en": "← Previous",
        "es": "← Anterior",
    },
    "wizard_generate": {
        "pt": "Gerar Plano ✓",
        "en": "Generate Plan ✓",
        "es": "Generar Plan ✓",
    },

    # ── Esportes ─────────────────────────────────────────────────
    "sport_running": {
        "pt": "Corrida",
        "en": "Running",
        "es": "Carrera",
    },
    "sport_cycling": {
        "pt": "Ciclismo",
        "en": "Cycling",
        "es": "Ciclismo",
    },
    "sport_swimming": {
        "pt": "Natação",
        "en": "Swimming",
        "es": "Natación",
    },
    "sport_triathlon": {
        "pt": "Triathlon",
        "en": "Triathlon",
        "es": "Triatlón",
    },

    # ── Botões comuns ────────────────────────────────────────────
    "btn_back": {
        "pt": "← Voltar",
        "en": "← Back",
        "es": "← Volver",
    },
    "btn_logout": {
        "pt": "🚪  Sair",
        "en": "🚪  Logout",
        "es": "🚪  Salir",
    },
    "btn_cancel": {
        "pt": "Cancelar",
        "en": "Cancel",
        "es": "Cancelar",
    },
    "btn_confirm": {
        "pt": "Confirmar",
        "en": "Confirm",
        "es": "Confirmar",
    },
    "btn_delete": {
        "pt": "Excluir",
        "en": "Delete",
        "es": "Eliminar",
    },

    # ── Mensagens ────────────────────────────────────────────────
    "confirm_logout": {
        "pt": "Tem certeza que deseja sair?\n\nVocê será redirecionado para a tela de login.",
        "en": "Are you sure you want to log out?\n\nYou will be redirected to the login screen.",
        "es": "¿Seguro que deseas salir?\n\nSerás redirigido a la pantalla de inicio de sesión.",
    },
    "confirm_logout_title": {
        "pt": "Confirmar Logout",
        "en": "Confirm Logout",
        "es": "Confirmar Cierre de Sesión",
    },
    "weeks_label": {
        "pt": "semanas",
        "en": "weeks",
        "es": "semanas",
    },
}

SUPPORTED_LANGUAGES = ("pt", "en", "es")


def set_language(lang: str):
    """Define o idioma ativo. Aceita: 'pt', 'en', 'es'."""
    global _current_language
    if lang in SUPPORTED_LANGUAGES:
        _current_language = lang


def get_language() -> str:
    """Retorna o código do idioma ativo."""
    return _current_language


def t(key: str, **kwargs) -> str:
    """
    Traduz uma chave para o idioma ativo.

    Aceita placeholders: t('dashboard_greeting', name='João')
    Retorna a chave em si se não encontrada.
    """
    entry = _translations.get(key)
    if entry is None:
        return key
    text = entry.get(_current_language, entry.get("pt", key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text
