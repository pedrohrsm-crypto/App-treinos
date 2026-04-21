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
    "register_returning": {
        "pt": "Retornando à tela inicial.",
        "en": "Returning to home screen.",
        "es": "Volviendo a la pantalla inicial.",
    },
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

    # ── Smartwatch / Wearables ────────────────────────────────────
    "smartwatch_title": {
        "pt": "Conectar Smartwatch",
        "en": "Connect Smartwatch",
        "es": "Conectar Smartwatch",
    },
    "smartwatch_subtitle": {
        "pt": "Emparelhe seus relógios e pulseiras de fitness para sincronizar atividades automaticamente.",
        "en": "Pair your smartwatches and fitness bands to automatically sync activities.",
        "es": "Empareja tus smartwatches y bandas de fitness para sincronizar actividades automáticamente.",
    },
    "smartwatch_recent_activities": {
        "pt": "Atividades Sincronizadas Recentemente",
        "en": "Recently Synced Activities",
        "es": "Actividades Sincronizadas Recientemente",
    },
    "smartwatch_garmin": {
        "pt": "Garmin Watch / Edge",
        "en": "Garmin Watch / Edge",
        "es": "Garmin Watch / Edge",
    },
    "smartwatch_apple": {
        "pt": "Apple Watch",
        "en": "Apple Watch",
        "es": "Apple Watch",
    },
    "smartwatch_fitbit": {
        "pt": "Fitbit",
        "en": "Fitbit",
        "es": "Fitbit",
    },
    "smartwatch_samsung": {
        "pt": "Samsung Galaxy Watch",
        "en": "Samsung Galaxy Watch",
        "es": "Samsung Galaxy Watch",
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

    # ── Dashboard (hardcoded → i18n) ────────────────────────────
    "dashboard_search": {
        "pt": "Pesquisar atleta…",
        "en": "Search athlete…",
        "es": "Buscar atleta…",
    },
    "dashboard_no_athlete": {
        "pt": "Nenhum atleta encontrado",
        "en": "No athlete found",
        "es": "Ningún atleta encontrado",
    },
    "dashboard_no_athlete_hint": {
        "pt": "Crie um plano de treino para começar.",
        "en": "Create a training plan to get started.",
        "es": "Cree un plan de entrenamiento para comenzar.",
    },
    "dashboard_loading": {
        "pt": "Carregando atletas…",
        "en": "Loading athletes…",
        "es": "Cargando atletas…",
    },
    "dashboard_new_plan": {
        "pt": "Novo Plano",
        "en": "New Plan",
        "es": "Nuevo Plan",
    },

    # ── Wizard (hardcoded → i18n) ────────────────────────────────
    "wizard_header": {
        "pt": "Novo Plano de Treino",
        "en": "New Training Plan",
        "es": "Nuevo Plan de Entrenamiento",
    },
    "wizard_athlete_title": {
        "pt": "Dados do Atleta",
        "en": "Athlete Data",
        "es": "Datos del Atleta",
    },
    "wizard_name": {
        "pt": "Nome completo",
        "en": "Full name",
        "es": "Nombre completo",
    },
    "wizard_age": {
        "pt": "Idade",
        "en": "Age",
        "es": "Edad",
    },
    "wizard_weight": {
        "pt": "Peso (kg)",
        "en": "Weight (kg)",
        "es": "Peso (kg)",
    },
    "wizard_height": {
        "pt": "Altura (cm)",
        "en": "Height (cm)",
        "es": "Altura (cm)",
    },
    "wizard_gender": {
        "pt": "Género",
        "en": "Gender",
        "es": "Género",
    },
    "wizard_gender_male": {
        "pt": "Masculino",
        "en": "Male",
        "es": "Masculino",
    },
    "wizard_gender_female": {
        "pt": "Feminino",
        "en": "Female",
        "es": "Femenino",
    },
    "wizard_cycle_label": {
        "pt": "Fase do ciclo menstrual (opcional)",
        "en": "Menstrual cycle phase (optional)",
        "es": "Fase del ciclo menstrual (opcional)",
    },
    "wizard_cycle_none": {
        "pt": "Não informar",
        "en": "Not specified",
        "es": "No informar",
    },
    "wizard_cycle_menstrual": {
        "pt": "Menstrual",
        "en": "Menstrual",
        "es": "Menstrual",
    },
    "wizard_cycle_follicular": {
        "pt": "Folicular",
        "en": "Follicular",
        "es": "Folicular",
    },
    "wizard_cycle_ovulatory": {
        "pt": "Ovulatória",
        "en": "Ovulatory",
        "es": "Ovulatoria",
    },
    "wizard_cycle_luteal": {
        "pt": "Lútea",
        "en": "Luteal",
        "es": "Lútea",
    },
    "wizard_sport_title": {
        "pt": "Selecione o Desporto",
        "en": "Select a Sport",
        "es": "Seleccione el Deporte",
    },
    "wizard_period_title": {
        "pt": "Período de Treinamento",
        "en": "Training Period",
        "es": "Período de Entrenamiento",
    },
    "wizard_period_hint": {
        "pt": "Informe a data da prova para cálculo automático das semanas.",
        "en": "Enter the race date for automatic week calculation.",
        "es": "Ingrese la fecha de la prueba para cálculo automático de semanas.",
    },
    "wizard_date_label": {
        "pt": "Data da prova (DD/MM/AAAA)",
        "en": "Race date (DD/MM/YYYY)",
        "es": "Fecha de la prueba (DD/MM/AAAA)",
    },
    "wizard_date_hint": {
        "pt": "Ex: 15/08/2026",
        "en": "E.g.: 15/08/2026",
        "es": "Ej: 15/08/2026",
    },
    "wizard_weeks_result": {
        "pt": "{weeks} semanas de treinamento",
        "en": "{weeks} weeks of training",
        "es": "{weeks} semanas de entrenamiento",
    },
    "wizard_weeks_capped": {
        "pt": "{weeks} semanas — será ajustado ao máximo de 52.",
        "en": "{weeks} weeks — will be capped at 52.",
        "es": "{weeks} semanas — se ajustará al máximo de 52.",
    },
    "wizard_dist_title": {
        "pt": "Distância & Fisiologia",
        "en": "Distance & Physiology",
        "es": "Distancia y Fisiología",
    },
    "wizard_dist_label": {
        "pt": "Distância da prova",
        "en": "Race distance",
        "es": "Distancia de la prueba",
    },
    "wizard_lactate": {
        "pt": "Limiar de lactato (bpm)",
        "en": "Lactate threshold (bpm)",
        "es": "Umbral de lactato (bpm)",
    },
    "wizard_vo2": {
        "pt": "VO2 Max (ml/kg/min)",
        "en": "VO2 Max (ml/kg/min)",
        "es": "VO2 Max (ml/kg/min)",
    },
    "wizard_health_toggle": {
        "pt": "Adicionar problemas de saúde",
        "en": "Add health issues",
        "es": "Agregar problemas de salud",
    },
    "wizard_health_type": {
        "pt": "Tipo",
        "en": "Type",
        "es": "Tipo",
    },
    "wizard_health_desc": {
        "pt": "Descrição",
        "en": "Description",
        "es": "Descripción",
    },
    "wizard_health_member": {
        "pt": "Membro afetado (opcional)",
        "en": "Affected limb (optional)",
        "es": "Miembro afectado (opcional)",
    },
    "wizard_health_add": {
        "pt": "Adicionar",
        "en": "Add",
        "es": "Agregar",
    },
    "wizard_days_title": {
        "pt": "Disponibilidade Semanal",
        "en": "Weekly Availability",
        "es": "Disponibilidad Semanal",
    },
    "wizard_days_hint": {
        "pt": "Quantos dias por semana o atleta pode treinar?",
        "en": "How many days per week can the athlete train?",
        "es": "¿Cuántos días por semana puede entrenar el atleta?",
    },
    "wizard_days_label": {
        "pt": "Dias por semana: {days}",
        "en": "Days per week: {days}",
        "es": "Días por semana: {days}",
    },
    "wizard_review_title": {
        "pt": "Revisão do Plano",
        "en": "Plan Review",
        "es": "Revisión del Plan",
    },
    "wizard_review_hint": {
        "pt": "Confirme os dados antes de gerar o plano.",
        "en": "Confirm the data before generating the plan.",
        "es": "Confirme los datos antes de generar el plan.",
    },
    "wizard_review_name": {
        "pt": "Nome",
        "en": "Name",
        "es": "Nombre",
    },
    "wizard_review_age_weight": {
        "pt": "Idade/Peso/Altura",
        "en": "Age/Weight/Height",
        "es": "Edad/Peso/Altura",
    },
    "wizard_review_gender": {
        "pt": "Género",
        "en": "Gender",
        "es": "Género",
    },
    "wizard_review_sport": {
        "pt": "Desporto",
        "en": "Sport",
        "es": "Deporte",
    },
    "wizard_review_distance": {
        "pt": "Distância",
        "en": "Distance",
        "es": "Distancia",
    },
    "wizard_review_weeks": {
        "pt": "Semanas",
        "en": "Weeks",
        "es": "Semanas",
    },
    "wizard_review_lactate_vo2": {
        "pt": "Limiar / VO2",
        "en": "Threshold / VO2",
        "es": "Umbral / VO2",
    },
    "wizard_review_days": {
        "pt": "Dias/semana",
        "en": "Days/week",
        "es": "Días/semana",
    },
    "wizard_review_cycle": {
        "pt": "Ciclo",
        "en": "Cycle",
        "es": "Ciclo",
    },
    "wizard_review_health": {
        "pt": "Saúde",
        "en": "Health",
        "es": "Salud",
    },
    "wizard_btn_back": {
        "pt": "Voltar",
        "en": "Back",
        "es": "Volver",
    },
    "wizard_btn_next": {
        "pt": "Próximo",
        "en": "Next",
        "es": "Siguiente",
    },
    "wizard_btn_generate": {
        "pt": "Gerar Plano",
        "en": "Generate Plan",
        "es": "Generar Plan",
    },
    "wizard_loading": {
        "pt": "Gerando plano de treino…",
        "en": "Generating training plan…",
        "es": "Generando plan de entrenamiento…",
    },
    "wizard_step_athlete_label": {
        "pt": "Atleta",
        "en": "Athlete",
        "es": "Atleta",
    },
    "wizard_step_sport_label": {
        "pt": "Desporto",
        "en": "Sport",
        "es": "Deporte",
    },
    "wizard_step_period_label": {
        "pt": "Período",
        "en": "Period",
        "es": "Período",
    },
    "wizard_step_dist_label": {
        "pt": "Distância",
        "en": "Distance",
        "es": "Distancia",
    },
    "wizard_step_days_label": {
        "pt": "Dias",
        "en": "Days",
        "es": "Días",
    },
    "wizard_step_review_label": {
        "pt": "Revisão",
        "en": "Review",
        "es": "Revisión",
    },

    # ── Validação do Wizard ──────────────────────────────────────
    "wizard_err_name": {
        "pt": "Nome é obrigatório (mínimo 2 caracteres).",
        "en": "Name is required (minimum 2 characters).",
        "es": "El nombre es obligatorio (mínimo 2 caracteres).",
    },
    "wizard_err_age_range": {
        "pt": "Idade deve ser entre 10 e 100.",
        "en": "Age must be between 10 and 100.",
        "es": "La edad debe estar entre 10 y 100.",
    },
    "wizard_err_age_invalid": {
        "pt": "Idade inválida (use um número inteiro).",
        "en": "Invalid age (use a whole number).",
        "es": "Edad inválida (use un número entero).",
    },
    "wizard_err_weight_range": {
        "pt": "Peso deve ser entre 30 e 250 kg.",
        "en": "Weight must be between 30 and 250 kg.",
        "es": "El peso debe estar entre 30 y 250 kg.",
    },
    "wizard_err_weight_invalid": {
        "pt": "Peso inválido.",
        "en": "Invalid weight.",
        "es": "Peso inválido.",
    },
    "wizard_err_height_range": {
        "pt": "Altura deve ser entre 100 e 250 cm.",
        "en": "Height must be between 100 and 250 cm.",
        "es": "La altura debe estar entre 100 y 250 cm.",
    },
    "wizard_err_height_invalid": {
        "pt": "Altura inválida.",
        "en": "Invalid height.",
        "es": "Altura inválida.",
    },
    "wizard_err_sport": {
        "pt": "Selecione um desporto.",
        "en": "Select a sport.",
        "es": "Seleccione un deporte.",
    },
    "wizard_err_date": {
        "pt": "Informe a data da prova.",
        "en": "Enter the race date.",
        "es": "Ingrese la fecha de la prueba.",
    },
    "wizard_err_weeks": {
        "pt": "Semanas devem ser ≥ 1.",
        "en": "Weeks must be ≥ 1.",
        "es": "Las semanas deben ser ≥ 1.",
    },
    "wizard_err_weeks_invalid": {
        "pt": "Número de semanas inválido.",
        "en": "Invalid number of weeks.",
        "es": "Número de semanas inválido.",
    },
    "wizard_err_distance": {
        "pt": "Selecione uma distância.",
        "en": "Select a distance.",
        "es": "Seleccione una distancia.",
    },
    "wizard_err_lactate_range": {
        "pt": "Limiar de lactato deve ser entre 100 e 220 bpm.",
        "en": "Lactate threshold must be between 100 and 220 bpm.",
        "es": "El umbral de lactato debe estar entre 100 y 220 bpm.",
    },
    "wizard_err_lactate_invalid": {
        "pt": "Limiar de lactato inválido.",
        "en": "Invalid lactate threshold.",
        "es": "Umbral de lactato inválido.",
    },
    "wizard_err_vo2_range": {
        "pt": "VO2 Max deve ser entre 20 e 90.",
        "en": "VO2 Max must be between 20 and 90.",
        "es": "VO2 Max debe estar entre 20 y 90.",
    },
    "wizard_err_vo2_invalid": {
        "pt": "VO2 Max inválido.",
        "en": "Invalid VO2 Max.",
        "es": "VO2 Max inválido.",
    },
    "wizard_health_ortho": {
        "pt": "Ortopédico",
        "en": "Orthopedic",
        "es": "Ortopédico",
    },
    "wizard_health_asthma": {
        "pt": "Asma / Respiratório",
        "en": "Asthma / Respiratory",
        "es": "Asma / Respiratorio",
    },
    "wizard_health_diabetes": {
        "pt": "Diabetes",
        "en": "Diabetes",
        "es": "Diabetes",
    },
    "wizard_health_hypertension": {
        "pt": "Hipertensão",
        "en": "Hypertension",
        "es": "Hipertensión",
    },
    "wizard_health_other": {
        "pt": "Outro",
        "en": "Other",
        "es": "Otro",
    },
    "wizard_health_limit": {
        "pt": "Máximo de 10 problemas de saúde.",
        "en": "Maximum 10 health issues.",
        "es": "Máximo 10 problemas de salud.",
    },

    # ── Config (hardcoded → i18n) ────────────────────────────────
    "config_title": {
        "pt": "Configurações",
        "en": "Settings",
        "es": "Configuración",
    },
    "config_theme": {
        "pt": "Tema",
        "en": "Theme",
        "es": "Tema",
    },
    "config_dark_mode": {
        "pt": "Modo escuro",
        "en": "Dark mode",
        "es": "Modo oscuro",
    },
    "config_language": {
        "pt": "Idioma",
        "en": "Language",
        "es": "Idioma",
    },
    "config_session": {
        "pt": "Sessão: {name}",
        "en": "Session: {name}",
        "es": "Sesión: {name}",
    },
    "config_logout": {
        "pt": "Logout",
        "en": "Logout",
        "es": "Cerrar sesión",
    },
    "config_admin": {
        "pt": "Painel Admin",
        "en": "Admin Panel",
        "es": "Panel Admin",
    },

    # ── Progress (hardcoded → i18n) ──────────────────────────────
    "progress_plans_label": {
        "pt": "Planos",
        "en": "Plans",
        "es": "Planes",
    },
    "progress_athletes_label": {
        "pt": "Atletas",
        "en": "Athletes",
        "es": "Atletas",
    },
    "progress_latest_label": {
        "pt": "Último",
        "en": "Latest",
        "es": "Último",
    },
    "progress_sport_dist": {
        "pt": "Distribuição por Desporto",
        "en": "Distribution by Sport",
        "es": "Distribución por Deporte",
    },
    "progress_no_data": {
        "pt": "Sem dados.",
        "en": "No data.",
        "es": "Sin datos.",
    },
    "progress_changelog_title": {
        "pt": "Changelog",
        "en": "Changelog",
        "es": "Historial",
    },
    "progress_no_log": {
        "pt": "Sem registos.",
        "en": "No records.",
        "es": "Sin registros.",
    },
    "progress_header": {
        "pt": "Progresso",
        "en": "Progress",
        "es": "Progreso",
    },
    "progress_loading": {
        "pt": "Carregando estatísticas…",
        "en": "Loading statistics…",
        "es": "Cargando estadísticas…",
    },

    # ── Athlete Dashboard (hardcoded → i18n) ─────────────────────
    "athlete_loading": {
        "pt": "Carregando dados…",
        "en": "Loading data…",
        "es": "Cargando datos…",
    },
    "athlete_loading_plans": {
        "pt": "Carregando planos…",
        "en": "Loading plans…",
        "es": "Cargando planes…",
    },
    "athlete_stats_plans": {
        "pt": "Planos",
        "en": "Plans",
        "es": "Planes",
    },
    "athlete_stats_weeks": {
        "pt": "Semanas",
        "en": "Weeks",
        "es": "Semanas",
    },
    "athlete_stats_sport": {
        "pt": "Desporto",
        "en": "Sport",
        "es": "Deporte",
    },
    "athlete_stats_bmi": {
        "pt": "IMC",
        "en": "BMI",
        "es": "IMC",
    },
    "athlete_plans_title": {
        "pt": "Planos de Treino",
        "en": "Training Plans",
        "es": "Planes de Entrenamiento",
    },
    "athlete_no_plans": {
        "pt": "Nenhum plano criado para este atleta.",
        "en": "No plans created for this athlete.",
        "es": "Ningún plan creado para este atleta.",
    },
    "athlete_export_msg": {
        "pt": "Exportação disponível via wizard.",
        "en": "Export available via wizard.",
        "es": "Exportación disponible via wizard.",
    },

    # ── Confirmações de exclusão ─────────────────────────────────
    "confirm_delete_plan_title": {
        "pt": "Confirmar exclusão",
        "en": "Confirm deletion",
        "es": "Confirmar eliminación",
    },
    "confirm_delete_plan_body": {
        "pt": "Tem certeza que deseja excluir este plano? Esta ação não pode ser desfeita.",
        "en": "Are you sure you want to delete this plan? This action cannot be undone.",
        "es": "¿Está seguro de que desea eliminar este plan? Esta acción no se puede deshacer.",
    },
    "confirm_delete_session_title": {
        "pt": "Confirmar remoção",
        "en": "Confirm removal",
        "es": "Confirmar eliminación",
    },
    "confirm_delete_session_body": {
        "pt": "Tem certeza que deseja remover esta sessão de treino?",
        "en": "Are you sure you want to remove this training session?",
        "es": "¿Está seguro de que desea eliminar esta sesión de entrenamiento?",
    },

    # ── Calendário (hardcoded → i18n) ────────────────────────────
    "calendar_header": {
        "pt": "Calendário de Treino",
        "en": "Training Calendar",
        "es": "Calendario de Entrenamiento",
    },
    "calendar_btn_today": {
        "pt": "Hoje",
        "en": "Today",
        "es": "Hoy",
    },
    "calendar_moved": {
        "pt": "Treino movido.",
        "en": "Workout moved.",
        "es": "Entrenamiento movido.",
    },
    "calendar_undo": {
        "pt": "Desfazer",
        "en": "Undo",
        "es": "Deshacer",
    },
    "calendar_day_mon": {"pt": "Seg", "en": "Mon", "es": "Lun"},
    "calendar_day_tue": {"pt": "Ter", "en": "Tue", "es": "Mar"},
    "calendar_day_wed": {"pt": "Qua", "en": "Wed", "es": "Mié"},
    "calendar_day_thu": {"pt": "Qui", "en": "Thu", "es": "Jue"},
    "calendar_day_fri": {"pt": "Sex", "en": "Fri", "es": "Vie"},
    "calendar_day_sat": {"pt": "Sáb", "en": "Sat", "es": "Sáb"},
    "calendar_day_sun": {"pt": "Dom", "en": "Sun", "es": "Dom"},
    "calendar_month_1": {"pt": "Janeiro", "en": "January", "es": "Enero"},
    "calendar_month_2": {"pt": "Fevereiro", "en": "February", "es": "Febrero"},
    "calendar_month_3": {"pt": "Março", "en": "March", "es": "Marzo"},
    "calendar_month_4": {"pt": "Abril", "en": "April", "es": "Abril"},
    "calendar_month_5": {"pt": "Maio", "en": "May", "es": "Mayo"},
    "calendar_month_6": {"pt": "Junho", "en": "June", "es": "Junio"},
    "calendar_month_7": {"pt": "Julho", "en": "July", "es": "Julio"},
    "calendar_month_8": {"pt": "Agosto", "en": "August", "es": "Agosto"},
    "calendar_month_9": {"pt": "Setembro", "en": "September", "es": "Septiembre"},
    "calendar_month_10": {"pt": "Outubro", "en": "October", "es": "Octubre"},
    "calendar_month_11": {"pt": "Novembro", "en": "November", "es": "Noviembre"},
    "calendar_month_12": {"pt": "Dezembro", "en": "December", "es": "Diciembre"},
    "calendar_move_btn": {
        "pt": "Mover para…",
        "en": "Move to…",
        "es": "Mover a…",
    },
    "calendar_move_date_label": {
        "pt": "Data destino (AAAA-MM-DD)",
        "en": "Target date (YYYY-MM-DD)",
        "es": "Fecha destino (AAAA-MM-DD)",
    },

    # ── Workout Editor (hardcoded → i18n) ────────────────────────
    "editor_type_label": {
        "pt": "Tipo de treino",
        "en": "Workout type",
        "es": "Tipo de entrenamiento",
    },
    "editor_zone_label": {
        "pt": "Zona de FC",
        "en": "HR Zone",
        "es": "Zona de FC",
    },
    "editor_duration_label": {
        "pt": "Duração",
        "en": "Duration",
        "es": "Duración",
    },
    "editor_duration_hint": {
        "pt": "Ex: 45 min",
        "en": "E.g.: 45 min",
        "es": "Ej: 45 min",
    },
    "editor_modality_label": {
        "pt": "Modalidade",
        "en": "Modality",
        "es": "Modalidad",
    },
    "editor_notes_label": {
        "pt": "Descrição / Notas",
        "en": "Description / Notes",
        "es": "Descripción / Notas",
    },
    "editor_header": {
        "pt": "Editar Treino — {date}",
        "en": "Edit Workout — {date}",
        "es": "Editar Entrenamiento — {date}",
    },
    "editor_copy_label": {
        "pt": "Copiar para data (AAAA-MM-DD)",
        "en": "Copy to date (YYYY-MM-DD)",
        "es": "Copiar a fecha (AAAA-MM-DD)",
    },
    "editor_copy_confirm": {
        "pt": "Confirmar cópia",
        "en": "Confirm copy",
        "es": "Confirmar copia",
    },
    "editor_copy_btn": {
        "pt": "Copiar",
        "en": "Copy",
        "es": "Copiar",
    },
    "editor_reset_btn": {
        "pt": "Reset",
        "en": "Reset",
        "es": "Reset",
    },
    "editor_delete_btn": {
        "pt": "Apagar",
        "en": "Delete",
        "es": "Eliminar",
    },
    "editor_session_not_found": {
        "pt": "Sessão não encontrada.",
        "en": "Session not found.",
        "es": "Sesión no encontrada.",
    },
    "editor_save_error": {
        "pt": "Erro ao salvar.",
        "en": "Error saving.",
        "es": "Error al guardar.",
    },
    "editor_reset_msg": {
        "pt": "Treino restaurado ao gerado.",
        "en": "Workout reset to generated.",
        "es": "Entrenamiento restaurado al generado.",
    },
    "editor_reset_error": {
        "pt": "Erro ao restaurar.",
        "en": "Error resetting.",
        "es": "Error al restaurar.",
    },
    "editor_deleted_msg": {
        "pt": "Sessão removida.",
        "en": "Session removed.",
        "es": "Sesión eliminada.",
    },
    "editor_copied_msg": {
        "pt": "Copiado para {date}.",
        "en": "Copied to {date}.",
        "es": "Copiado a {date}.",
    },
    "editor_copy_invalid_date": {
        "pt": "Data inválida. Use o formato AAAA-MM-DD.",
        "en": "Invalid date. Use the format YYYY-MM-DD.",
        "es": "Fecha inválida. Use el formato AAAA-MM-DD.",
    },

    # ── Plan Card (hardcoded → i18n) ─────────────────────────────
    "plan_phase_base": {"pt": "Base", "en": "Base", "es": "Base"},
    "plan_phase_resistance": {"pt": "Resistência", "en": "Endurance", "es": "Resistencia"},
    "plan_phase_speed": {"pt": "Velocidade", "en": "Speed", "es": "Velocidad"},
    "plan_phase_power": {"pt": "Potência", "en": "Power", "es": "Potencia"},
    "plan_phase_taper": {"pt": "Polimento", "en": "Taper", "es": "Afinación"},
    "plan_phase_label": {
        "pt": "Fase: {phase} · S{week}/{total}",
        "en": "Phase: {phase} · W{week}/{total}",
        "es": "Fase: {phase} · S{week}/{total}",
    },
    "plan_created_at": {
        "pt": "Criado em {date}",
        "en": "Created on {date}",
        "es": "Creado el {date}",
    },
    "plan_tooltip_calendar": {
        "pt": "Calendário",
        "en": "Calendar",
        "es": "Calendario",
    },
    "plan_tooltip_export": {
        "pt": "Exportar",
        "en": "Export",
        "es": "Exportar",
    },
    "plan_tooltip_delete": {
        "pt": "Apagar",
        "en": "Delete",
        "es": "Eliminar",
    },

    # ── Nav Bar (hardcoded → i18n) ───────────────────────────────
    "nav_dashboard": {
        "pt": "Dashboard",
        "en": "Dashboard",
        "es": "Panel",
    },
    "nav_stats": {
        "pt": "Estatísticas",
        "en": "Statistics",
        "es": "Estadísticas",
    },
    "nav_templates": {
        "pt": "Modelos",
        "en": "Templates",
        "es": "Plantillas",
    },
    "nav_fitness": {
        "pt": "Fitness",
        "en": "Fitness",
        "es": "Fitness",
    },
    "nav_config": {
        "pt": "Config",
        "en": "Settings",
        "es": "Ajustes",
    },
    "nav_help": {
        "pt": "Ajuda",
        "en": "Help",
        "es": "Ayuda",
    },

    # ── Onboarding extras ────────────────────────────────────────
    "onboarding_back": {
        "pt": "Voltar",
        "en": "Back",
        "es": "Volver",
    },

    # ── Debounce / login ─────────────────────────────────────────
    "login_processing": {
        "pt": "Entrando…",
        "en": "Signing in…",
        "es": "Iniciando sesión…",
    },
    "register_processing": {
        "pt": "Criando conta…",
        "en": "Creating account…",
        "es": "Creando cuenta…",
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
