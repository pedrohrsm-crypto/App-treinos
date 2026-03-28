"""
Tela de Integração com APIs de Fitness
=======================================

Permite conectar Strava / Garmin e importar atividades.
"""

import tkinter as tk
from tkinter import messagebox
import webbrowser
from pathlib import Path

from gui.theme import theme
from gui.modern_widgets import AnimatedButton, RoundedFrame
from i18n import t


class FitnessScreen:
    """Tela de integração com plataformas de fitness."""

    def __init__(self, parent, trainer_info, credential, on_back):
        self.parent = parent
        self.trainer_info = trainer_info
        self.credential = credential
        self.on_back = on_back
        self._connector = None
        self._activities = []

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
            text=f"⌚  {t('fitness_title')}",
            font=(theme.fonts['primary'], theme.font_sizes['heading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
        ).pack(side='left', padx=(20, 0))

    # ── Conteúdo ─────────────────────────────────────────────────

    def _create_content(self):
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

        canvas.bind_all(
            '<MouseWheel>',
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), 'units'),
        )

        self._create_strava_section(self.scroll_frame)
        self._create_garmin_section(self.scroll_frame)
        self._create_activities_section(self.scroll_frame)

    # ── Strava ───────────────────────────────────────────────────

    def _create_strava_section(self, parent):
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

        # Título Strava
        title_row = tk.Frame(inner, bg=theme.colors['bg_white'])
        title_row.pack(fill='x', pady=(0, 15))

        tk.Label(
            title_row,
            text="🔶  Strava",
            font=(theme.fonts['primary'], theme.font_sizes['subheading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
        ).pack(side='left')

        # Status badge
        connected = self._is_strava_connected()
        status_text = t('fitness_connected') if connected else t('fitness_not_connected')
        status_color = theme.colors['success'] if connected else theme.colors['text_secondary']

        tk.Label(
            title_row,
            text=f"●  {status_text}",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=status_color,
        ).pack(side='right')

        tk.Label(
            inner,
            text=t('fitness_strava_desc'),
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
            wraplength=700,
            justify='left',
        ).pack(anchor='w', pady=(0, 15))

        # Campos de configuração
        config_frame = tk.Frame(inner, bg=theme.colors['bg_white'])
        config_frame.pack(fill='x', pady=(0, 15))

        # Client ID
        tk.Label(
            config_frame,
            text="Client ID:",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
        ).pack(anchor='w', pady=(0, 3))

        self.strava_client_id_var = tk.StringVar()
        tk.Entry(
            config_frame,
            textvariable=self.strava_client_id_var,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightbackground=theme.colors['border_light'],
            highlightcolor=theme.colors['primary'],
        ).pack(fill='x', ipady=8, pady=(0, 10))

        # Client Secret
        tk.Label(
            config_frame,
            text="Client Secret:",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
        ).pack(anchor='w', pady=(0, 3))

        self.strava_client_secret_var = tk.StringVar()
        tk.Entry(
            config_frame,
            textvariable=self.strava_client_secret_var,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            show='•',
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightbackground=theme.colors['border_light'],
            highlightcolor=theme.colors['primary'],
        ).pack(fill='x', ipady=8, pady=(0, 10))

        # Botões
        btn_frame = tk.Frame(inner, bg=theme.colors['bg_white'])
        btn_frame.pack(fill='x')

        connect_btn = AnimatedButton(
            btn_frame,
            text=t('fitness_connect_strava'),
            font=(theme.fonts['primary'], theme.font_sizes['button'], 'bold'),
            bg_color=theme.colors['primary'],
            fg_color=theme.colors['text_light'],
            hover_bg=theme.colors['accent_hover'],
            hover_fg=theme.colors['text_light'],
            active_bg=theme.colors['accent_hover'],
            corner_radius=8,
            padding_x=20,
            padding_y=10,
            command=self._connect_strava,
        )
        connect_btn.pack(side='left', padx=(0, 10))

        if connected:
            import_btn = AnimatedButton(
                btn_frame,
                text=t('fitness_import_activities'),
                font=(theme.fonts['primary'], theme.font_sizes['button'], 'bold'),
                bg_color=theme.colors['analogous_1'],
                fg_color=theme.colors['text_light'],
                hover_bg=theme.colors['analogous_2'],
                hover_fg=theme.colors['text_light'],
                active_bg=theme.colors['analogous_2'],
                corner_radius=8,
                padding_x=20,
                padding_y=10,
                command=self._import_strava_activities,
            )
            import_btn.pack(side='left')

        # Link de ajuda
        help_label = tk.Label(
            inner,
            text=t('fitness_strava_help'),
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['primary'],
            cursor='hand2',
        )
        help_label.pack(anchor='w', pady=(10, 0))
        help_label.bind('<Enter>', lambda e: help_label.config(
            font=(theme.fonts['primary'], theme.font_sizes['small'], 'underline')
        ))
        help_label.bind('<Leave>', lambda e: help_label.config(
            font=(theme.fonts['primary'], theme.font_sizes['small'])
        ))

    # ── Garmin (em breve) ────────────────────────────────────────

    def _create_garmin_section(self, parent):
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

        title_row = tk.Frame(inner, bg=theme.colors['bg_white'])
        title_row.pack(fill='x', pady=(0, 10))

        tk.Label(
            title_row,
            text="🟢  Garmin Connect",
            font=(theme.fonts['primary'], theme.font_sizes['subheading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
        ).pack(side='left')

        tk.Label(
            title_row,
            text=t('fitness_coming_soon'),
            font=(theme.fonts['primary'], theme.font_sizes['small'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
        ).pack(side='right')

        tk.Label(
            inner,
            text=t('fitness_garmin_desc'),
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
            wraplength=700,
            justify='left',
        ).pack(anchor='w')

    # ── Lista de atividades importadas ───────────────────────────

    def _create_activities_section(self, parent):
        self._activities_parent = parent
        self._activities_section_frame = tk.Frame(parent, bg=theme.colors['bg_secondary'])
        self._activities_section_frame.pack(fill='x')
        self._refresh_activities_ui()

    def _refresh_activities_ui(self):
        for w in self._activities_section_frame.winfo_children():
            w.destroy()

        if not self._activities:
            return

        section = RoundedFrame(
            self._activities_section_frame,
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
            text=t('fitness_imported_activities'),
            font=(theme.fonts['primary'], theme.font_sizes['subheading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
        ).pack(anchor='w', pady=(0, 15))

        sport_icons = {
            'Corrida': '🏃', 'Ciclismo': '🚴', 'Natação': '🏊',
            'Triathlon': '🏊🚴🏃', 'Caminhada': '🚶',
        }

        for act in self._activities[:20]:
            row = tk.Frame(inner, bg=theme.colors['bg_secondary'], padx=12, pady=8)
            row.pack(fill='x', pady=2)

            icon = sport_icons.get(act.sport, '🏅')
            tk.Label(
                row, text=icon,
                font=(theme.fonts['primary'], 16),
                bg=theme.colors['bg_secondary'],
            ).pack(side='left', padx=(0, 10))

            info = tk.Frame(row, bg=theme.colors['bg_secondary'])
            info.pack(side='left', fill='x', expand=True)

            tk.Label(
                info,
                text=act.name,
                font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
                bg=theme.colors['bg_secondary'],
                fg=theme.colors['text_primary'],
                anchor='w',
            ).pack(anchor='w')

            detail = f"{act.sport}  ·  {act.distance_km} km  ·  {act.duration_minutes:.0f} min"
            if act.avg_heart_rate:
                detail += f"  ·  ❤️ {act.avg_heart_rate:.0f} bpm"
            tk.Label(
                info,
                text=detail,
                font=(theme.fonts['primary'], theme.font_sizes['small']),
                bg=theme.colors['bg_secondary'],
                fg=theme.colors['text_secondary'],
                anchor='w',
            ).pack(anchor='w')

            # Data
            date_str = act.date[:10] if act.date else '—'
            tk.Label(
                row,
                text=date_str,
                font=(theme.fonts['primary'], theme.font_sizes['small']),
                bg=theme.colors['bg_secondary'],
                fg=theme.colors['text_secondary'],
            ).pack(side='right')

    # ── Ações ────────────────────────────────────────────────────

    def _is_strava_connected(self) -> bool:
        try:
            from fitness_connectors import StravaConnector
            token_path = Path(__file__).parent.parent / "data" / ".strava_token.json"
            if token_path.exists():
                connector = StravaConnector("", "", token_path=str(token_path))
                return connector.is_connected()
        except Exception:
            pass
        return False

    def _connect_strava(self):
        client_id = self.strava_client_id_var.get().strip()
        client_secret = self.strava_client_secret_var.get().strip()

        if not client_id or not client_secret:
            messagebox.showerror(
                t('fitness_error_title'),
                t('fitness_error_credentials'),
            )
            return

        try:
            from fitness_connectors import StravaConnector
            connector = StravaConnector(
                client_id=client_id,
                client_secret=client_secret,
                token_path=str(
                    Path(__file__).parent.parent / "data" / ".strava_token.json"
                ),
            )
            auth_url = connector.authorize_url()
            self._connector = connector

            # Abrir browser para autorização
            webbrowser.open(auth_url)

            # Pedir o código de callback
            self._show_code_dialog(connector)
        except Exception as e:
            messagebox.showerror(t('fitness_error_title'), str(e))

    def _show_code_dialog(self, connector):
        dialog = tk.Toplevel(self.parent)
        dialog.title(t('fitness_auth_title'))
        dialog.geometry("500x280")
        dialog.configure(bg=theme.colors['bg_secondary'])
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()

        header = tk.Frame(dialog, bg=theme.colors['primary'], height=60)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(
            header,
            text=f"🔶  {t('fitness_auth_title')}",
            font=(theme.fonts['primary'], theme.font_sizes['subheading'], 'bold'),
            bg=theme.colors['primary'],
            fg=theme.colors['text_light'],
        ).pack(expand=True)

        content = tk.Frame(dialog, bg=theme.colors['bg_secondary'])
        content.pack(fill='both', expand=True, padx=30, pady=20)

        tk.Label(
            content,
            text=t('fitness_auth_instructions'),
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_primary'],
            wraplength=440,
            justify='left',
        ).pack(anchor='w', pady=(0, 15))

        tk.Label(
            content,
            text=t('fitness_auth_code_label'),
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_secondary'],
        ).pack(anchor='w', pady=(0, 3))

        code_var = tk.StringVar()
        code_entry = tk.Entry(
            content,
            textvariable=code_var,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            relief='solid', bd=1,
            highlightthickness=2,
            highlightbackground=theme.colors['border_light'],
            highlightcolor=theme.colors['primary'],
        )
        code_entry.pack(fill='x', ipady=8)
        code_entry.focus()

        def do_exchange():
            code = code_var.get().strip()
            if not code:
                return
            try:
                connector.exchange_token(code)
                dialog.destroy()
                messagebox.showinfo(
                    t('fitness_success_title'),
                    t('fitness_success_connected'),
                )
                # Recriar tela para atualizar estado
                self.frame.destroy()
                FitnessScreen(
                    self.parent, self.trainer_info,
                    self.credential, self.on_back,
                )
            except Exception as e:
                messagebox.showerror(t('fitness_error_title'), str(e))

        code_entry.bind('<Return>', lambda e: do_exchange())

        btn_frame = tk.Frame(content, bg=theme.colors['bg_secondary'])
        btn_frame.pack(fill='x', pady=(15, 0))

        tk.Button(
            btn_frame, text=t('btn_cancel'),
            font=(theme.fonts['primary'], theme.font_sizes['button']),
            bg=theme.colors['bg_white'], fg=theme.colors['text_secondary'],
            relief='solid', bd=1, cursor='hand2',
            command=dialog.destroy,
        ).pack(side='right', ipadx=15, ipady=5)

        tk.Button(
            btn_frame, text=t('btn_confirm'),
            font=(theme.fonts['primary'], theme.font_sizes['button'], 'bold'),
            bg=theme.colors['primary'], fg=theme.colors['text_light'],
            activebackground=theme.colors['accent_hover'],
            relief='flat', cursor='hand2',
            command=do_exchange,
        ).pack(side='right', padx=(0, 10), ipadx=15, ipady=5)

    def _import_strava_activities(self):
        try:
            from fitness_connectors import StravaConnector
            token_path = Path(__file__).parent.parent / "data" / ".strava_token.json"
            connector = StravaConnector("", "", token_path=str(token_path))

            self._activities = connector.get_activities(limit=30)

            if self._activities:
                self._refresh_activities_ui()
                messagebox.showinfo(
                    t('fitness_success_title'),
                    t('fitness_import_success', count=len(self._activities)),
                )
            else:
                messagebox.showinfo(
                    t('fitness_title'),
                    t('fitness_no_activities'),
                )
        except Exception as e:
            messagebox.showerror(t('fitness_error_title'), str(e))

    def _go_back(self):
        self.frame.destroy()
        self.on_back()
