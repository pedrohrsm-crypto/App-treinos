"""
Dashboard de Progresso
======================

Tela de visualização de estatísticas e progresso dos treinos.
Exibe métricas resumidas, distribuição por esporte e planos recentes.
"""

import tkinter as tk
from datetime import datetime

from gui.theme import theme
from gui.modern_widgets import AnimatedButton, RoundedFrame
from training_manager import training_manager
from i18n import t


class ProgressDashboard:
    """Dashboard com estatísticas e progresso do treinador."""

    def __init__(self, parent, trainer_info, credential, on_back):
        self.parent = parent
        self.trainer_info = trainer_info
        self.credential = credential
        self.on_back = on_back

        # Carregar dados
        self.plans = training_manager.get_trainer_plans(trainer_info)
        self.stats = training_manager.get_statistics(trainer_info)

        # Container principal
        self.frame = tk.Frame(parent, bg=theme.colors['bg_secondary'])
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._create_header()
        self._create_content()

    # ── Header ───────────────────────────────────────────────────

    def _create_header(self):
        header_container = tk.Frame(
            self.frame, bg=theme.colors['bg_secondary'], height=100
        )
        header_container.pack(fill='x', side='top', padx=20, pady=(20, 0))
        header_container.pack_propagate(False)

        header = RoundedFrame(
            header_container,
            bg_color=theme.colors['bg_white'],
            corner_radius=16,
            shadow_color=theme.colors['shadow'],
            shadow_offset=4,
        )
        header.pack(fill='both', expand=True)

        inner = tk.Frame(header.frame, bg=theme.colors['bg_white'])
        inner.pack(fill='both', expand=True, padx=30, pady=15)

        # Botão voltar
        back_btn = AnimatedButton(
            inner,
            text=t('btn_back'),
            font=(theme.fonts['primary'], theme.font_sizes['small'], 'bold'),
            bg_color=theme.colors['bg_secondary'],
            fg_color=theme.colors['text_primary'],
            hover_bg=theme.colors['primary'],
            hover_fg=theme.colors['text_light'],
            active_bg=theme.colors['primary'],
            corner_radius=8,
            padding_x=15,
            padding_y=8,
            command=self._go_back,
        )
        back_btn.pack(side='left')

        tk.Label(
            inner,
            text=f"📊  {t('progress_title')}",
            font=(theme.fonts['primary'], theme.font_sizes['heading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
        ).pack(side='left', padx=(20, 0))

    # ── Conteúdo ─────────────────────────────────────────────────

    def _create_content(self):
        # Scrollable container
        outer = tk.Frame(self.frame, bg=theme.colors['bg_secondary'])
        outer.pack(fill='both', expand=True, padx=20, pady=20)

        canvas = tk.Canvas(outer, bg=theme.colors['bg_secondary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(outer, orient='vertical', command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg=theme.colors['bg_secondary'])

        self.scroll_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all')),
        )
        canvas.create_window((0, 0), window=self.scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Bind mousewheel
        canvas.bind_all(
            '<MouseWheel>',
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), 'units'),
        )

        # Seções
        self._create_stats_row(self.scroll_frame)
        self._create_sports_chart(self.scroll_frame)
        self._create_recent_plans(self.scroll_frame)
        self._create_changelog_section(self.scroll_frame)

        if not self.plans:
            self._create_empty_state(self.scroll_frame)

    # ── Cartões de estatísticas ──────────────────────────────────

    def _create_stats_row(self, parent):
        row = tk.Frame(parent, bg=theme.colors['bg_secondary'])
        row.pack(fill='x', pady=(0, 20))

        stats = [
            ("📋", str(self.stats['total_plans']), t('progress_plans_created'), theme.colors['primary']),
            ("👥", str(self.stats['unique_athletes']), t('progress_unique_athletes'), theme.colors['analogous_1']),
            (
                "🏅",
                str(len(self.stats['sports_distribution'])),
                t('progress_sports'),
                theme.colors['analogous_2'],
            ),
            (
                "📅",
                self._format_date(self.stats.get('latest_plan')),
                t('progress_latest'),
                theme.colors['triadic_1'],
            ),
        ]

        for icon, value, label, color in stats:
            self._create_stat_card(row, icon, value, label, color)

    def _create_stat_card(self, parent, icon, value, label, accent_color):
        card = RoundedFrame(
            parent,
            bg_color=theme.colors['bg_white'],
            corner_radius=12,
            shadow_color=theme.colors['shadow'],
            shadow_offset=3,
        )
        card.pack(side='left', expand=True, fill='both', padx=8)

        inner = tk.Frame(card.frame, bg=theme.colors['bg_white'])
        inner.pack(expand=True, pady=20, padx=15)

        # Barra colorida de topo
        bar = tk.Frame(card.frame, bg=accent_color, height=4)
        bar.pack(fill='x', side='top')
        bar.pack_propagate(False)
        bar.lift()

        tk.Label(
            inner,
            text=icon,
            font=(theme.fonts['primary'], 28),
            bg=theme.colors['bg_white'],
        ).pack()

        tk.Label(
            inner,
            text=value,
            font=(theme.fonts['primary'], theme.font_sizes['heading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
        ).pack(pady=(5, 2))

        tk.Label(
            inner,
            text=label,
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
        ).pack()

    # ── Gráfico de distribuição por esporte ──────────────────────

    def _create_sports_chart(self, parent):
        if not self.stats['sports_distribution']:
            return

        section = RoundedFrame(
            parent,
            bg_color=theme.colors['bg_white'],
            corner_radius=12,
            shadow_color=theme.colors['shadow'],
            shadow_offset=3,
        )
        section.pack(fill='x', pady=(0, 20), padx=8)

        inner = tk.Frame(section.frame, bg=theme.colors['bg_white'])
        inner.pack(fill='x', padx=25, pady=20)

        tk.Label(
            inner,
            text=t('progress_distribution'),
            font=(theme.fonts['primary'], theme.font_sizes['subheading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
        ).pack(anchor='w', pady=(0, 15))

        distribution = self.stats['sports_distribution']
        max_count = max(distribution.values()) if distribution else 1

        sport_colors = {
            'Corrida': theme.colors['primary'],
            'Ciclismo': theme.colors['analogous_1'],
            'Natação': theme.colors['analogous_2'],
            'Triathlon': theme.colors['triadic_1'],
            'Duathlon (Natação+Corrida)': theme.colors['triadic_2'],
            'Duathlon (Ciclismo+Corrida)': theme.colors['complementary'],
        }
        default_color = theme.colors['primary']

        for sport, count in sorted(distribution.items(), key=lambda x: -x[1]):
            row = tk.Frame(inner, bg=theme.colors['bg_white'])
            row.pack(fill='x', pady=4)

            tk.Label(
                row,
                text=sport,
                font=(theme.fonts['primary'], theme.font_sizes['body']),
                bg=theme.colors['bg_white'],
                fg=theme.colors['text_primary'],
                width=28,
                anchor='w',
            ).pack(side='left')

            bar_bg = tk.Frame(row, bg=theme.colors['bg_tertiary'], height=24)
            bar_bg.pack(side='left', fill='x', expand=True, padx=(10, 10))
            bar_bg.pack_propagate(False)

            ratio = count / max_count
            color = sport_colors.get(sport, default_color)

            bar_fill = tk.Frame(bar_bg, bg=color, height=24)
            bar_fill.place(relx=0, rely=0, relwidth=max(ratio, 0.05), relheight=1)

            tk.Label(
                row,
                text=str(count),
                font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
                bg=theme.colors['bg_white'],
                fg=theme.colors['text_primary'],
                width=4,
                anchor='e',
            ).pack(side='right')

    # ── Planos recentes ──────────────────────────────────────────

    def _create_recent_plans(self, parent):
        if not self.plans:
            return

        section = RoundedFrame(
            parent,
            bg_color=theme.colors['bg_white'],
            corner_radius=12,
            shadow_color=theme.colors['shadow'],
            shadow_offset=3,
        )
        section.pack(fill='x', pady=(0, 20), padx=8)

        inner = tk.Frame(section.frame, bg=theme.colors['bg_white'])
        inner.pack(fill='x', padx=25, pady=20)

        tk.Label(
            inner,
            text=t('progress_recent'),
            font=(theme.fonts['primary'], theme.font_sizes['subheading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
        ).pack(anchor='w', pady=(0, 15))

        # Exibir até 10 planos recentes
        for plan in self.plans[:10]:
            self._create_plan_row(inner, plan)

    def _create_plan_row(self, parent, plan):
        row = tk.Frame(
            parent,
            bg=theme.colors['bg_secondary'],
            padx=15,
            pady=10,
        )
        row.pack(fill='x', pady=3)

        # Ícone do esporte
        sport_icons = {
            'Corrida': '🏃',
            'Ciclismo': '🚴',
            'Natação': '🏊',
            'Triathlon': '🏊🚴🏃',
            'Duathlon (Natação+Corrida)': '🏊🏃',
            'Duathlon (Ciclismo+Corrida)': '🚴🏃',
        }
        icon = sport_icons.get(plan.sport, '🏅')

        tk.Label(
            row,
            text=icon,
            font=(theme.fonts['primary'], 18),
            bg=theme.colors['bg_secondary'],
        ).pack(side='left', padx=(0, 12))

        info = tk.Frame(row, bg=theme.colors['bg_secondary'])
        info.pack(side='left', fill='x', expand=True)

        tk.Label(
            info,
            text=plan.athlete_name,
            font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_primary'],
            anchor='w',
        ).pack(anchor='w')

        detail_text = f"{plan.sport} · {plan.distance} · {plan.weeks} semanas"
        tk.Label(
            info,
            text=detail_text,
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_secondary'],
            anchor='w',
        ).pack(anchor='w')

        # Data
        tk.Label(
            row,
            text=self._format_date(plan.created_at),
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_secondary'],
        ).pack(side='right')

    # ── Histórico de alterações ──────────────────────────────────

    def _create_changelog_section(self, parent):
        changelog = training_manager.get_changelog(self.trainer_info, limit=20)
        if not changelog:
            return

        section = RoundedFrame(
            parent,
            bg_color=theme.colors['bg_white'],
            corner_radius=12,
            shadow_color=theme.colors['shadow'],
            shadow_offset=3,
        )
        section.pack(fill='x', pady=(0, 20), padx=8)

        inner = tk.Frame(section.frame, bg=theme.colors['bg_white'])
        inner.pack(fill='x', padx=25, pady=20)

        tk.Label(
            inner,
            text=t('progress_changelog'),
            font=(theme.fonts['primary'], theme.font_sizes['subheading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
        ).pack(anchor='w', pady=(0, 15))

        action_icons = {
            'created': '🆕',
            'deleted': '🗑️',
            'exported': '📤',
            'updated': '✏️',
        }

        for entry in changelog:
            row = tk.Frame(inner, bg=theme.colors['bg_secondary'], padx=12, pady=8)
            row.pack(fill='x', pady=2)

            icon = action_icons.get(entry.action, '📝')
            tk.Label(
                row,
                text=icon,
                font=(theme.fonts['primary'], 14),
                bg=theme.colors['bg_secondary'],
            ).pack(side='left', padx=(0, 10))

            tk.Label(
                row,
                text=entry.details,
                font=(theme.fonts['primary'], theme.font_sizes['small']),
                bg=theme.colors['bg_secondary'],
                fg=theme.colors['text_primary'],
                anchor='w',
            ).pack(side='left', fill='x', expand=True)

            tk.Label(
                row,
                text=self._format_datetime(entry.timestamp),
                font=(theme.fonts['primary'], theme.font_sizes['small']),
                bg=theme.colors['bg_secondary'],
                fg=theme.colors['text_secondary'],
            ).pack(side='right')

    # ── Estado vazio ─────────────────────────────────────────────

    def _create_empty_state(self, parent):
        container = tk.Frame(parent, bg=theme.colors['bg_secondary'])
        container.pack(expand=True, fill='both', pady=60)

        tk.Label(
            container,
            text="📭",
            font=(theme.fonts['primary'], 60),
            bg=theme.colors['bg_secondary'],
        ).pack()

        tk.Label(
            container,
            text=t('progress_empty'),
            font=(theme.fonts['primary'], theme.font_sizes['subheading'], 'bold'),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_primary'],
        ).pack(pady=(15, 5))

        tk.Label(
            container,
            text=t('progress_empty_hint'),
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_secondary'],
        ).pack()

    # ── Utilidades ───────────────────────────────────────────────

    def _format_date(self, iso_str):
        if not iso_str:
            return "—"
        try:
            dt = datetime.fromisoformat(iso_str)
            return dt.strftime("%d/%m/%Y")
        except (ValueError, TypeError):
            return "—"

    def _format_datetime(self, iso_str):
        if not iso_str:
            return "—"
        try:
            dt = datetime.fromisoformat(iso_str)
            return dt.strftime("%d/%m/%Y %H:%M")
        except (ValueError, TypeError):
            return "—"

    def _go_back(self):
        self.frame.destroy()
        self.on_back()
