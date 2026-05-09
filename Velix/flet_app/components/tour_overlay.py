"""
Tour Overlay — Sistema de Tour Interativo First-Use
====================================================

Cria overlay com backdrop escuro, elemento destacado, e tooltip
para guiar usuários em primeiro uso das telas.

Features:
- Highlight dinâmico de elementos
- Backdrop com efeito de "dimming"
- Tooltip com Next/Skip buttons
- Persistência de tours vistos
- Integração com AppState
"""

import flet as ft
from typing import Optional, Dict, Callable
from flet_app.theme import c, RADIUS, SPACING
from flet_app.state import app_state


class TourStep:
    """Define um passo do tour."""

    def __init__(
        self,
        title: str,
        description: str,
        target_control: Optional[ft.Control] = None,
        position: str = "bottom",  # 'top', 'bottom', 'left', 'right'
        max_width: int = 300,
    ):
        """
        Args:
            title: Título do passo
            description: Descrição detalhada
            target_control: Controle a destacar (None = mostrar só tooltip)
            position: Posição do tooltip relativo ao elemento
            max_width: Largura máxima do tooltip
        """
        self.title = title
        self.description = description
        self.target_control = target_control
        self.position = position
        self.max_width = max_width


class TourOverlay:
    """Gerenciador de tour interativo."""

    def __init__(
        self,
        page: ft.Page,
        tour_id: str,
        steps: list,
        on_complete: Optional[Callable] = None,
        dark: bool = False,
    ):
        """
        Args:
            page: Página Flet
            tour_id: ID único do tour (ex: 'dashboard_tour')
            steps: Lista de TourStep
            on_complete: Callback ao concluir tour
            dark: Modo escuro
        """
        self.page = page
        self.tour_id = tour_id
        self.steps = steps
        self.on_complete = on_complete
        self.dark = dark
        self.current_step = 0

        # Elementos de UI
        self.backdrop = None
        self.highlight = None
        self.tooltip = None
        self.tour_container = None

    def start(self):
        """Inicia o tour."""
        if self._should_skip_tour():
            return

        self._build_ui()
        self._show_step(0)

    def skip(self):
        """Pula o tour."""
        self._mark_tour_as_seen()
        self._cleanup()
        if self.on_complete:
            self.on_complete()

    def next_step(self):
        """Vai para próximo passo."""
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self._mark_tour_as_seen()
            self._cleanup()
            if self.on_complete:
                self.on_complete()
        else:
            self._show_step(self.current_step)

    def _should_skip_tour(self) -> bool:
        """Verifica se tour já foi visto."""
        seen = app_state._read_prefs_file().get("_seen_tours", {})
        return seen.get(self.tour_id, False)

    def _mark_tour_as_seen(self):
        """Marca tour como visto."""
        prefs = app_state._read_prefs_file()
        if "_seen_tours" not in prefs:
            prefs["_seen_tours"] = {}
        prefs["_seen_tours"][self.tour_id] = True
        app_state._write_prefs_file(prefs)

    def _build_ui(self):
        """Constrói elementos do overlay."""
        # Backdrop (fundo escuro)
        self.backdrop = ft.Container(
            width=self.page.window.width,
            height=self.page.window.height,
            bgcolor="rgba(0,0,0,0.7)",
            on_click=lambda e: self.next_step(),
        )

        # Container para controlar z-index
        self.tour_container = ft.Stack(
            [self.backdrop],
            expand=True,
        )

        # Adicionar ao overlay da página
        if not hasattr(self.page, '_tour_overlay'):
            self.page.overlay.append(self.tour_container)

    def _show_step(self, step_index: int):
        """Exibe um passo específico."""
        if step_index >= len(self.steps):
            return

        step = self.steps[step_index]

        # Atualizar highlight se houver target
        if step.target_control:
            self._update_highlight(step)

        # Atualizar tooltip
        self._update_tooltip(step)
        self.page.update()

    def _update_highlight(self, step: TourStep):
        """Atualiza o elemento destacado."""
        # Nota: Em Flet, não há forma nativa de obter coordenadas exatas
        # Então criamos um efeito visual usando borders/opacity
        if hasattr(step.target_control, 'border'):
            step.target_control.border = ft.border.all(
                3, c("warning", self.dark)
            )
            step.target_control.shadow = ft.BoxShadow(
                blur_radius=20,
                spread_radius=5,
                color=c("warning", self.dark),
                offset=ft.Offset(0, 0),
            )

            # Animated scale
            if hasattr(step.target_control, 'scale'):
                step.target_control.scale = 1.05
                step.target_control.animate_scale = ft.Animation(
                    300, ft.AnimationCurve.EASE_OUT
                )

    def _update_tooltip(self, step: TourStep):
        """Atualiza o tooltip com título e descrição."""
        progress = f"{self.current_step + 1}/{len(self.steps)}"

        tooltip_content = ft.Column([
            # Header
            ft.Row([
                ft.Text(progress, size=11, color=c("text_secondary", self.dark)),
                ft.IconButton(
                    ft.Icons.CLOSE,
                    icon_size=18,
                    on_click=lambda e: self.skip(),
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            # Título
            ft.Text(
                step.title,
                size=16,
                weight=ft.FontWeight.BOLD,
                color=c("text_primary", self.dark),
            ),

            # Descrição
            ft.Text(
                step.description,
                size=13,
                color=c("text_secondary", self.dark),
                max_lines=5,
            ),

            # Botões
            ft.Row([
                ft.TextButton(
                    "Pular",
                    on_click=lambda e: self.skip(),
                ),
                ft.ElevatedButton(
                    "Próximo ➜" if self.current_step < len(self.steps) - 1 else "Concluir",
                    on_click=lambda e: self.next_step(),
                    bgcolor=c("primary", self.dark),
                ),
            ], spacing=SPACING["sm"]),
        ], spacing=SPACING["md"])

        self.tooltip = ft.Container(
            content=tooltip_content,
            padding=SPACING["lg"],
            bgcolor=c("bg_card", self.dark),
            border_radius=RADIUS["lg"],
            border=ft.border.all(1, c("border_light", self.dark)),
            width=step.max_width,
            shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=2,
                color=ft.colors.BLACK26,
            ),
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            opacity=0,
        )

        # Posicionar tooltip dinamicamente
        tooltip_wrapper = ft.Container(
            content=self.tooltip,
            alignment=ft.Alignment.CENTER,
            expand=True,
        )

        # Remover tooltip anterior se existir
        if len(self.tour_container.controls) > 1:
            self.tour_container.controls.pop()

        self.tour_container.controls.append(tooltip_wrapper)

        # Animar entrada do tooltip
        self.tooltip.opacity = 1

    def _cleanup(self):
        """Remove overlay do tour."""
        if self.tour_container in self.page.overlay:
            self.page.overlay.remove(self.tour_container)
            self.page.update()


# ── Factory functions ────────────────────────────────────────

def create_dashboard_tour(page: ft.Page, on_complete=None) -> TourOverlay:
    """Cria tour para tela do Dashboard."""

    steps = [
        TourStep(
            title="Bem-vindo ao Dashboard",
            description="Este é seu painel principal. Aqui você vê todos os seus atletas cadastrados.",
            position="top",
        ),
        TourStep(
            title="Pesquise Atletas",
            description="Use a barra de pesquisa para filtrar atletas por nome ou modalidade esportiva.",
            position="bottom",
        ),
        TourStep(
            title="Crie Novos Planos",
            description="Clique no botão '+' para criar um novo treino para qualquer atleta.",
            position="left",
        ),
        TourStep(
            title="Menu de Ajuda",
            description="Acesse 'Ajuda' no menu lateral para documentação, FAQs e suporte.",
            position="left",
        ),
    ]

    return TourOverlay(page, "dashboard_tour", steps, on_complete, dark=False)


def create_athletes_tour(page: ft.Page, on_complete=None) -> TourOverlay:
    """Cria tour para tela de Gerenciamento de Atletas."""

    steps = [
        TourStep(
            title="Seus Atletas",
            description="Visualize todos os atletas cadastrados. Cada card mostra nome, CPF e esporte.",
            position="top",
        ),
        TourStep(
            title="Adicione Atleta",
            description="Clique em '+' para registrar um novo atleta com dados completos (fisiológicos, saúde, etc).",
            position="top",
        ),
        TourStep(
            title="Menu de Ações",
            description="Clique no '⋮' para editar ou deletar o atleta (soft delete, dados preservados).",
            position="left",
        ),
        TourStep(
            title="Dados Rastreados",
            description="Sistema armazena: peso, altura, VO2 Max, FC repouso, limiar lactato, ciclo menstrual.",
            position="top",
        ),
    ]

    return TourOverlay(page, "athletes_tour", steps, on_complete, dark=False)


def create_help_tour(page: ft.Page, on_complete=None) -> TourOverlay:
    """Cria tour para tela de Ajuda."""

    steps = [
        TourStep(
            title="Centro de Ajuda",
            description="4 seções expandíveis: Como Usar, Configurações, Sobre e Suporte.",
            position="top",
        ),
        TourStep(
            title="Como Usar",
            description="Guia rápido de 4 passos e botão para refazer este tour em qualquer momento.",
            position="bottom",
        ),
        TourStep(
            title="Configurações",
            description="Acesse tema escuro/claro, idioma, configuração de IA e gerenciador de atletas.",
            position="bottom",
        ),
        TourStep(
            title="Suporte",
            description="Email de contato e FAQs respondendo perguntas comuns sobre dados e funcionalidades.",
            position="bottom",
        ),
    ]

    return TourOverlay(page, "help_tour", steps, on_complete, dark=False)


def restart_tour(page: ft.Page, tour_id: str):
    """Reinicia um tour marcando como não visto."""
    prefs = app_state._read_prefs_file()
    if "_seen_tours" in prefs:
        prefs["_seen_tours"].pop(tour_id, None)
        app_state._write_prefs_file(prefs)
