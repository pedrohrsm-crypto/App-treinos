"""
Help Screen — Central Hub de Documentação e Suporte
===================================================

Oferece:
1. Como Usar (How-To)
2. Configurações (Settings)
3. Sobre (About)
4. Suporte (Support)
"""

import flet as ft
from i18n import t
from flet_app.theme import c, RADIUS, SPACING
from flet_app.components.adaptive_nav import build_adaptive_layout
from flet_app.state import app_state
from flet_app.components.tour_overlay import create_help_tour


def help_view(page: ft.Page, route: str) -> ft.View:
    """Tela de Ajuda e Documentação."""

    dark = app_state.dark_mode

    # ── Expandible sections ──────────────────────────────────────

    # Section 1: Como Usar
    section_howtouse = ft.ExpansionTile(
        title=ft.Text("Como Usar", size=16, weight=ft.FontWeight.W_600,
                     color=c("text_primary", dark)),
        icon_color=c("primary", dark),
        collapsed_icon_color=c("text_secondary", dark),
        content=ft.Container(
            content=ft.Column([
                ft.Text("Guia Rápido de Início:", size=14, weight=ft.FontWeight.W_500,
                       color=c("text_primary", dark)),
                ft.Text("1. Crie um perfil de atleta com dados pessoais e fisiológicos",
                       size=13, color=c("text_secondary", dark)),
                ft.Text("2. Use o Assistente de Treino para criar planos personalizados",
                       size=13, color=c("text_secondary", dark)),
                ft.Text("3. Configure IA opcional para sugestões automáticas",
                       size=13, color=c("text_secondary", dark)),
                ft.Text("4. Acompanhe progresso no Dashboard com métricas",
                       size=13, color=c("text_secondary", dark)),
                ft.Divider(height=16),
                ft.ElevatedButton(
                    text="Refazer Tour Interativo",
                    icon=ft.Icons.PLAY_ARROW,
                    on_click=lambda e: _restart_tour()
                ),
            ], spacing=SPACING["sm"]),
            padding=SPACING["md"]
        )
    )

    # Section 2: Configurações
    section_config = ft.ExpansionTile(
        title=ft.Text("Configurações", size=16, weight=ft.FontWeight.W_600,
                     color=c("text_primary", dark)),
        icon_color=c("primary", dark),
        collapsed_icon_color=c("text_secondary", dark),
        content=ft.Container(
            content=ft.Column([
                ft.TextButton(
                    "🌓 Modo Escuro/Claro",
                    on_click=lambda e: page.go("/config")
                ),
                ft.TextButton(
                    "🌐 Idioma (PT/EN/ES)",
                    on_click=lambda e: page.go("/config")
                ),
                ft.TextButton(
                    "🤖 Configuração de IA",
                    on_click=lambda e: page.go("/ai-config")
                ),
                ft.TextButton(
                    "👤 Gerenciar Atletas",
                    on_click=lambda e: page.go("/dashboard")
                ),
            ], spacing=SPACING["sm"]),
            padding=SPACING["md"]
        )
    )

    # Section 3: Sobre
    section_about = ft.ExpansionTile(
        title=ft.Text("Sobre", size=16, weight=ft.FontWeight.W_600,
                     color=c("text_primary", dark)),
        icon_color=c("primary", dark),
        collapsed_icon_color=c("text_secondary", dark),
        content=ft.Container(
            content=ft.Column([
                _build_about_row("Versão", "v3.1.0"),
                _build_about_row("Data", "21/04/2026"),
                _build_about_row("Desenvolvedor", "App Treinos by PT Team"),
                ft.Divider(height=12),
                ft.TextButton("📄 Ler EULA (Termos de Uso)"),
                ft.TextButton("🔒 Política de Privacidade (LGPD)"),
                ft.TextButton("📃 Licença (LICENSE)"),
            ], spacing=SPACING["sm"]),
            padding=SPACING["md"]
        )
    )

    # Section 4: Suporte
    section_support = ft.ExpansionTile(
        title=ft.Text("Suporte", size=16, weight=ft.FontWeight.W_600,
                     color=c("text_primary", dark)),
        icon_color=c("primary", dark),
        collapsed_icon_color=c("text_secondary", dark),
        content=ft.Container(
            content=ft.Column([
                ft.Text("Email de Suporte:", size=13, weight=ft.FontWeight.W_500,
                       color=c("text_primary", dark)),
                ft.Text("support@apptreinos.com.br", size=12,
                       color=c("primary", dark)),
                ft.Divider(height=16),
                ft.Text("Perguntas Frequentes:", size=13, weight=ft.FontWeight.W_500,
                       color=c("text_primary", dark)),
                _build_faq_item("Como resetar minha senha?",
                              "Acesse o ecrã de login e clique em 'Esqueceu a senha?'"),
                _build_faq_item("Onde ficam meus dados?",
                              "Todos os dados são armazenados localmente no seu computador. Zero servidores externos (exceto IA opcional)."),
                _build_faq_item("Como exportar dados de atletas?",
                              "Use a opção 'Exportar' no Dashboard para cada atleta. Formatos: CSV, PDF, Excel."),
                _build_faq_item("O app funciona offline?",
                              "Sim! Apenas a IA (se configurada) requer internet. Resto funciona 100% offline."),
            ], spacing=SPACING["sm"]),
            padding=SPACING["md"]
        )
    )

    # ── Body content ─────────────────────────────────────────────
    body = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.HELP_OUTLINE, size=32, color=c("primary", dark)),
                        ft.Text("Ajuda & Documentação", size=28, weight=ft.FontWeight.BOLD,
                               color=c("text_primary", dark)),
                    ], spacing=SPACING["md"]),
                    padding=SPACING["lg"]
                ),
                ft.Container(
                    content=ft.Column([
                        section_howtouse,
                        section_config,
                        section_about,
                        section_support,
                    ], spacing=SPACING["md"]),
                    padding=ft.padding.symmetric(horizontal=SPACING["lg"], vertical=SPACING["md"])
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=0
        ),
        expand=True,
        bgcolor=c("bg_secondary", dark),
    )

    def _restart_tour():
        """Marca todos os tours como não vistos (para restart)."""
        app_state.seen_tours = {}  # Reseta tours
        page.snack_bar = ft.SnackBar(ft.Text("Tour será exibido na próxima tela!"))
        page.snack_bar.open = True
        page.update()

    # Iniciar tour se for primeira vez
    tour = create_help_tour(page)
    tour.start()

    return build_adaptive_layout(page, 5, body, dark)  # Index 5 = Help


def _build_about_row(label: str, value: str) -> ft.Container:
    """Helper para linha de informação About."""
    return ft.Container(
        content=ft.Row([
            ft.Text(f"{label}:", size=13, weight=ft.FontWeight.W_500,
                   color=ft.colors.GREY_700),
            ft.Text(value, size=13, color=ft.colors.BLUE_600),
        ], spacing=SPACING["md"]),
    )


def _build_faq_item(question: str, answer: str) -> ft.Container:
    """Helper para item de FAQ."""
    return ft.Container(
        content=ft.Column([
            ft.Text(f"• {question}", size=12, weight=ft.FontWeight.W_500,
                   color=ft.colors.GREY_900),
            ft.Text(f"  {answer}", size=11, color=ft.colors.GREY_700,
                   italic=True),
        ], spacing=4),
        padding=ft.padding.symmetric(vertical=SPACING["xs"])
    )
