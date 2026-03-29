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
    "login_error_empty": {
        "pt": "Preencha todos os campos.",
        "en": "Please fill in all fields.",
        "es": "Por favor, complete todos los campos.",
    },
    "login_error_invalid": {
        "pt": "Credenciais inválidas.",
        "en": "Invalid credentials.",
        "es": "Credenciales inválidas.",
    },
    "register_link": {
        "pt": "Criar conta",
        "en": "Create account",
        "es": "Crear cuenta",
    },

    # ── Registro ─────────────────────────────────────────────────
    "register_title": {
        "pt": "Criar Conta",
        "en": "Create Account",
        "es": "Crear Cuenta",
    },
    "register_name": {
        "pt": "Nome completo",
        "en": "Full name",
        "es": "Nombre completo",
    },
    "register_cpf": {
        "pt": "CPF",
        "en": "CPF",
        "es": "CPF",
    },
    "register_cref": {
        "pt": "CREF",
        "en": "CREF",
        "es": "CREF",
    },
    "register_email": {
        "pt": "E-mail (opcional)",
        "en": "Email (optional)",
        "es": "Correo (opcional)",
    },
    "register_password": {
        "pt": "Senha",
        "en": "Password",
        "es": "Contraseña",
    },
    "register_confirm": {
        "pt": "Confirmar senha",
        "en": "Confirm password",
        "es": "Confirmar contraseña",
    },
    "register_button": {
        "pt": "Cadastrar",
        "en": "Register",
        "es": "Registrarse",
    },
    "register_error_required": {
        "pt": "Preencha os campos obrigatórios.",
        "en": "Please fill in the required fields.",
        "es": "Por favor, complete los campos obligatorios.",
    },
    "register_error_mismatch": {
        "pt": "As senhas não coincidem.",
        "en": "Passwords do not match.",
        "es": "Las contraseñas no coinciden.",
    },
    "register_error_short": {
        "pt": "A senha deve ter no mínimo 6 caracteres.",
        "en": "Password must be at least 6 characters.",
        "es": "La contraseña debe tener al menos 6 caracteres.",
    },
    "register_success": {
        "pt": "Conta criada! Redirecionando…",
        "en": "Account created! Redirecting…",
        "es": "¡Cuenta creada! Redirigiendo…",
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

    # ── Fitness / Integrações ────────────────────────────────────
    "card_fitness": {
        "pt": "Fitness & Saúde",
        "en": "Fitness & Health",
        "es": "Fitness y Salud",
    },
    "card_fitness_desc": {
        "pt": "Conecte Strava ou Garmin e importe atividades dos seus atletas",
        "en": "Connect Strava or Garmin and import your athletes' activities",
        "es": "Conecta Strava o Garmin e importa actividades de tus atletas",
    },
    "fitness_title": {
        "pt": "Integrações de Fitness",
        "en": "Fitness Integrations",
        "es": "Integraciones de Fitness",
    },
    "fitness_connected": {
        "pt": "Conectado",
        "en": "Connected",
        "es": "Conectado",
    },
    "fitness_not_connected": {
        "pt": "Não conectado",
        "en": "Not connected",
        "es": "No conectado",
    },
    "fitness_strava_desc": {
        "pt": "Importe corridas, pedaladas e natação do Strava. Necessita de um app registado em strava.com/settings/api.",
        "en": "Import runs, rides and swims from Strava. Requires an app registered at strava.com/settings/api.",
        "es": "Importa carreras, pedaleos y natación de Strava. Requiere una app registrada en strava.com/settings/api.",
    },
    "fitness_connect_strava": {
        "pt": "Conectar Strava",
        "en": "Connect Strava",
        "es": "Conectar Strava",
    },
    "fitness_import_activities": {
        "pt": "Importar Atividades",
        "en": "Import Activities",
        "es": "Importar Actividades",
    },
    "fitness_strava_help": {
        "pt": "ℹ️  Como obter Client ID e Secret? Acesse strava.com/settings/api",
        "en": "ℹ️  How to get Client ID and Secret? Visit strava.com/settings/api",
        "es": "ℹ️  ¿Cómo obtener Client ID y Secret? Visita strava.com/settings/api",
    },
    "fitness_garmin_desc": {
        "pt": "Integração com Garmin Connect para importar atividades de relógios Garmin. A API oficial requer parceria comercial — em desenvolvimento.",
        "en": "Garmin Connect integration to import activities from Garmin watches. Official API requires commercial partnership — in development.",
        "es": "Integración con Garmin Connect para importar actividades de relojes Garmin. La API oficial requiere asociación comercial — en desarrollo.",
    },
    "fitness_coming_soon": {
        "pt": "Em breve",
        "en": "Coming soon",
        "es": "Próximamente",
    },
    "fitness_imported_activities": {
        "pt": "Atividades Importadas",
        "en": "Imported Activities",
        "es": "Actividades Importadas",
    },
    "fitness_auth_title": {
        "pt": "Autorização Strava",
        "en": "Strava Authorization",
        "es": "Autorización Strava",
    },
    "fitness_auth_instructions": {
        "pt": "Uma página do Strava foi aberta no navegador. Autorize o acesso e copie o código da URL de retorno (parâmetro 'code').",
        "en": "A Strava page was opened in your browser. Authorize access and copy the code from the return URL ('code' parameter).",
        "es": "Se abrió una página de Strava en el navegador. Autoriza el acceso y copia el código de la URL de retorno (parámetro 'code').",
    },
    "fitness_auth_code_label": {
        "pt": "Código de autorização:",
        "en": "Authorization code:",
        "es": "Código de autorización:",
    },
    "fitness_error_title": {
        "pt": "Erro",
        "en": "Error",
        "es": "Error",
    },
    "fitness_error_credentials": {
        "pt": "Preencha o Client ID e Client Secret do Strava.",
        "en": "Please fill in the Strava Client ID and Client Secret.",
        "es": "Rellena el Client ID y Client Secret de Strava.",
    },
    "fitness_success_title": {
        "pt": "Sucesso",
        "en": "Success",
        "es": "Éxito",
    },
    "fitness_success_connected": {
        "pt": "Strava conectado com sucesso! Agora pode importar atividades.",
        "en": "Strava connected successfully! You can now import activities.",
        "es": "¡Strava conectado con éxito! Ahora puedes importar actividades.",
    },
    "fitness_import_success": {
        "pt": "{count} atividades importadas com sucesso!",
        "en": "{count} activities imported successfully!",
        "es": "¡{count} actividades importadas con éxito!",
    },
    "fitness_no_activities": {
        "pt": "Nenhuma atividade encontrada no Strava.",
        "en": "No activities found on Strava.",
        "es": "No se encontraron actividades en Strava.",
    },

    # ── Calendário ───────────────────────────────────────────────
    "calendar_title": {
        "pt": "Calendário de Treino",
        "en": "Training Calendar",
        "es": "Calendario de Entrenamiento",
    },
    "calendar_today": {
        "pt": "Hoje",
        "en": "Today",
        "es": "Hoy",
    },
    "calendar_sessions": {
        "pt": "{count} sessão(ões)",
        "en": "{count} session(s)",
        "es": "{count} sesión(es)",
    },
    "calendar_no_data": {
        "pt": "Nenhum treino mapeado para este mês.",
        "en": "No training mapped for this month.",
        "es": "Ningún entrenamiento mapeado para este mes.",
    },

    # ── Editor de treino ─────────────────────────────────────────
    "editor_title": {
        "pt": "Editar Treino",
        "en": "Edit Workout",
        "es": "Editar Entrenamiento",
    },
    "editor_save": {
        "pt": "Salvar",
        "en": "Save",
        "es": "Guardar",
    },
    "editor_cancel": {
        "pt": "Cancelar",
        "en": "Cancel",
        "es": "Cancelar",
    },
    "editor_reset": {
        "pt": "Restaurar gerado",
        "en": "Reset to generated",
        "es": "Restaurar generado",
    },
    "editor_copy": {
        "pt": "Copiar para outro dia",
        "en": "Copy to another day",
        "es": "Copiar a otro día",
    },
    "editor_saved": {
        "pt": "Treino atualizado.",
        "en": "Workout updated.",
        "es": "Entrenamiento actualizado.",
    },
    "editor_deleted": {
        "pt": "Sessão removida.",
        "en": "Session removed.",
        "es": "Sesión eliminada.",
    },
    "workout_moved": {
        "pt": "Treino movido.",
        "en": "Workout moved.",
        "es": "Entrenamiento movido.",
    },
    "workout_undo": {
        "pt": "Desfazer",
        "en": "Undo",
        "es": "Deshacer",
    },

    # ── Templates ────────────────────────────────────────────────
    "templates_title": {
        "pt": "Templates de Treino",
        "en": "Workout Templates",
        "es": "Plantillas de Entrenamiento",
    },
    "templates_my": {
        "pt": "Meus Templates",
        "en": "My Templates",
        "es": "Mis Plantillas",
    },
    "templates_system": {
        "pt": "Templates do Sistema",
        "en": "System Templates",
        "es": "Plantillas del Sistema",
    },
    "templates_new": {
        "pt": "Novo Template",
        "en": "New Template",
        "es": "Nueva Plantilla",
    },
    "templates_created": {
        "pt": "Template criado.",
        "en": "Template created.",
        "es": "Plantilla creada.",
    },
    "templates_deleted": {
        "pt": "Template removido.",
        "en": "Template removed.",
        "es": "Plantilla eliminada.",
    },
    "templates_use": {
        "pt": "Usar template",
        "en": "Use template",
        "es": "Usar plantilla",
    },

    # ── Notificações ─────────────────────────────────────────────
    "notifications_title": {
        "pt": "Notificações",
        "en": "Notifications",
        "es": "Notificaciones",
    },
    "notifications_empty": {
        "pt": "Sem notificações pendentes.",
        "en": "No pending notifications.",
        "es": "Sin notificaciones pendientes.",
    },
    "notification_training_today": {
        "pt": "Treino hoje — {athlete}",
        "en": "Training today — {athlete}",
        "es": "Entrenamiento hoy — {athlete}",
    },
    "notification_training_tomorrow": {
        "pt": "Treino amanhã — {athlete}",
        "en": "Training tomorrow — {athlete}",
        "es": "Entrenamiento mañana — {athlete}",
    },
    "notification_deadline": {
        "pt": "Prova próxima — {athlete}",
        "en": "Race approaching — {athlete}",
        "es": "Competencia próxima — {athlete}",
    },
    "notification_inactive": {
        "pt": "Atleta inativo — {athlete}",
        "en": "Inactive athlete — {athlete}",
        "es": "Atleta inactivo — {athlete}",
    },

    # ── Wizard ───────────────────────────────────────────────────
    "wizard_title": {
        "pt": "Novo Plano de Treino",
        "en": "New Training Plan",
        "es": "Nuevo Plan de Entrenamiento",
    },
    "wizard_step_athlete": {
        "pt": "Dados do Atleta",
        "en": "Athlete Data",
        "es": "Datos del Atleta",
    },
    "wizard_step_sport": {
        "pt": "Desporto",
        "en": "Sport",
        "es": "Deporte",
    },
    "wizard_step_period": {
        "pt": "Período",
        "en": "Period",
        "es": "Período",
    },
    "wizard_step_distance": {
        "pt": "Distância",
        "en": "Distance",
        "es": "Distancia",
    },
    "wizard_step_days": {
        "pt": "Dias",
        "en": "Days",
        "es": "Días",
    },
    "wizard_step_review": {
        "pt": "Revisão",
        "en": "Review",
        "es": "Revisión",
    },
    "wizard_generate": {
        "pt": "Gerar Plano",
        "en": "Generate Plan",
        "es": "Generar Plan",
    },
    "wizard_plan_created": {
        "pt": "Plano criado com sucesso! ({count} sessões)",
        "en": "Plan created successfully! ({count} sessions)",
        "es": "¡Plan creado con éxito! ({count} sesiones)",
    },
    "wizard_next": {
        "pt": "Próximo",
        "en": "Next",
        "es": "Siguiente",
    },
    "wizard_back": {
        "pt": "Voltar",
        "en": "Back",
        "es": "Volver",
    },

    # ── Onboarding ───────────────────────────────────────────────
    "onboarding_welcome_title": {
        "pt": "Bem-vindo ao App Treinos",
        "en": "Welcome to Training App",
        "es": "Bienvenido a App Entrenamientos",
    },
    "onboarding_welcome_body": {
        "pt": "Planejamento profissional de treinos esportivos, com periodização automática e monitoramento completo.",
        "en": "Professional sports training planning with automatic periodization and full monitoring.",
        "es": "Planificación profesional de entrenamientos deportivos con periodización automática y monitoreo completo.",
    },
    "onboarding_plans_title": {
        "pt": "Crie Planos Personalizados",
        "en": "Create Custom Plans",
        "es": "Cree Planes Personalizados",
    },
    "onboarding_plans_body": {
        "pt": "Wizard de 6 passos gera planos de treino com periodização científica para Corrida, Ciclismo, Natação e Triathlon.",
        "en": "6-step wizard generates training plans with scientific periodization for Running, Cycling, Swimming and Triathlon.",
        "es": "Asistente de 6 pasos genera planes de entrenamiento con periodización científica para Carrera, Ciclismo, Natación y Triatlón.",
    },
    "onboarding_progress_title": {
        "pt": "Acompanhe o Progresso",
        "en": "Track Progress",
        "es": "Siga el Progreso",
    },
    "onboarding_progress_body": {
        "pt": "Estatísticas detalhadas, distribuição por esporte, calendário de sessões e histórico completo de atividades.",
        "en": "Detailed statistics, sport distribution, session calendar and full activity history.",
        "es": "Estadísticas detalladas, distribución por deporte, calendario de sesiones e historial completo de actividades.",
    },
    "onboarding_devices_title": {
        "pt": "Conecte Seus Dispositivos",
        "en": "Connect Your Devices",
        "es": "Conecte Sus Dispositivos",
    },
    "onboarding_devices_body": {
        "pt": "Integração com Strava para importar suas atividades. Suporte a Garmin em breve.",
        "en": "Strava integration to import your activities. Garmin support coming soon.",
        "es": "Integración con Strava para importar sus actividades. Soporte Garmin próximamente.",
    },
    "onboarding_skip": {
        "pt": "Pular",
        "en": "Skip",
        "es": "Saltar",
    },
    "onboarding_next": {
        "pt": "Próximo",
        "en": "Next",
        "es": "Siguiente",
    },
    "onboarding_start": {
        "pt": "Começar",
        "en": "Get Started",
        "es": "Comenzar",
    },

    # ── Tooltips contextuais ─────────────────────────────────────
    "tooltip_dashboard": {
        "pt": "Toque em um atleta para ver detalhes. Use o botão + para criar um novo plano.",
        "en": "Tap an athlete to see details. Use the + button to create a new plan.",
        "es": "Toque un atleta para ver detalles. Use el botón + para crear un nuevo plan.",
    },
    "tooltip_config": {
        "pt": "Personalize tema e idioma aqui. As configurações são salvas automaticamente.",
        "en": "Customize theme and language here. Settings are saved automatically.",
        "es": "Personalice tema e idioma aquí. Los ajustes se guardan automáticamente.",
    },
    "tooltip_fitness": {
        "pt": "Conecte seu Strava para importar atividades automaticamente.",
        "en": "Connect your Strava to import activities automatically.",
        "es": "Conecte su Strava para importar actividades automáticamente.",
    },
    "tooltip_wizard": {
        "pt": "Preencha os 6 passos para gerar um plano de treino personalizado.",
        "en": "Fill in 6 steps to generate a personalized training plan.",
        "es": "Complete los 6 pasos para generar un plan de entrenamiento personalizado.",
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
