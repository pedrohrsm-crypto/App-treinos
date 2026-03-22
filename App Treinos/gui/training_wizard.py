"""
Training Wizard - Assistente de Criação de Planos de Treinamento
=================================================================

Wizard completo para coleta de dados e geração de planos personalizados.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from gui.theme import theme
from gui.wizard_steps import PeriodoStep, DistanciaStep
from training_planner import Athlete, TrainerInfo, TrainingPlanGenerator, ExcelExporter
from core.database import db_manager
from pdf_exporter import PDFExporter
from training_manager import training_manager


class TrainingWizard:
    """Wizard completo de criação de planos de treinamento."""
    
    def __init__(self, parent, trainer_info, on_complete):
        self.parent = parent
        self.trainer_info = trainer_info
        self.on_complete = on_complete
        self.current_step = 0
        self.collected_data = {}
        
        # Container principal
        self.frame = tk.Frame(parent, bg=theme.colors['bg_secondary'])
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Criar estrutura
        self._create_structure()
        
        # Definir etapas
        self.steps = [
            ('Dados do Atleta', self._create_athlete_step),
            ('Modalidade', self._create_sport_step),
            ('Período', self._create_period_step),
            ('Distância e Fisiologia', self._create_distance_step),
            ('Disponibilidade', self._create_availability_step),
            ('Revisão e Geração', self._create_review_step)
        ]
        
        # Carregar primeira etapa
        self._load_step(0)
    
    def _create_structure(self):
        """Cria estrutura básica do wizard."""
        # Header
        header = tk.Frame(self.frame, bg=theme.colors['bg_white'], height=100)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # Linha separadora
        tk.Frame(header, bg=theme.colors['border_light'], height=2).pack(fill='x', side='bottom')
        
        header_content = tk.Frame(header, bg=theme.colors['bg_white'])
        header_content.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Logo e título
        tk.Label(
            header_content,
            text="🏃",
            font=(theme.fonts['primary'], 35),
            bg=theme.colors['bg_white'],
            fg=theme.colors['primary']
        ).pack(side='left', padx=(0, 15))
        
        title_frame = tk.Frame(header_content, bg=theme.colors['bg_white'])
        title_frame.pack(side='left', fill='y')
        
        title_content = tk.Frame(title_frame, bg=theme.colors['bg_white'])
        title_content.pack(expand=True)
        
        tk.Label(
            title_content,
            text="Novo Plano de Treinamento",
            font=(theme.fonts['primary'], theme.font_sizes['heading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w')
        
        self.step_label = tk.Label(
            title_content,
            text="Etapa 1 de 6",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        )
        self.step_label.pack(anchor='w')
        
        # Botão fechar
        close_btn = tk.Button(
            header_content,
            text="✕",
            font=(theme.fonts['primary'], 20),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
            activebackground=theme.colors['error'],
            activeforeground=theme.colors['text_light'],
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self._cancel
        )
        close_btn.pack(side='right', padx=10)
        
        # Progress bar
        self.progress_frame = tk.Frame(self.frame, bg=theme.colors['bg_secondary'], height=8)
        self.progress_frame.pack(fill='x')
        
        self.progress_bar = tk.Frame(self.progress_frame, bg=theme.colors['primary'], height=8)
        self.progress_bar.pack(side='left', fill='y')
        
        # Container de conteúdo
        self.content_area = tk.Frame(self.frame, bg=theme.colors['bg_secondary'])
        self.content_area.pack(fill='both', expand=True)
        
        # Footer com botões
        footer = tk.Frame(self.frame, bg=theme.colors['bg_white'], height=80)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        tk.Frame(footer, bg=theme.colors['border_light'], height=2).pack(fill='x', side='top')
        
        footer_content = tk.Frame(footer, bg=theme.colors['bg_white'])
        footer_content.pack(fill='both', expand=True, padx=40, pady=15)
        
        # Botões de navegação
        self.btn_prev = tk.Button(
            footer_content,
            text="← Anterior",
            font=(theme.fonts['primary'], theme.font_sizes['button']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
            activebackground=theme.colors['bg_secondary'],
            relief='solid',
            bd=1,
            cursor='hand2',
            command=self._prev_step,
            state='disabled'
        )
        self.btn_prev.pack(side='left', ipadx=20, ipady=8)
        
        self.btn_next = tk.Button(
            footer_content,
            text="Próximo →",
            font=(theme.fonts['primary'], theme.font_sizes['button'], 'bold'),
            bg=theme.colors['primary'],
            fg=theme.colors['text_light'],
            activebackground=theme.colors['accent_hover'],
            relief='flat',
            cursor='hand2',
            command=self._next_step
        )
        self.btn_next.pack(side='right', ipadx=20, ipady=8)
    
    def _update_progress(self):
        """Atualiza barra de progresso."""
        progress = (self.current_step + 1) / len(self.steps)
        width = int(self.frame.winfo_width() * progress)
        self.progress_bar.config(width=width)
        
        # Atualizar label
        self.step_label.config(text=f"Etapa {self.current_step + 1} de {len(self.steps)}")
        
        # Atualizar botões
        self.btn_prev.config(state='normal' if self.current_step > 0 else 'disabled')
        
        if self.current_step == len(self.steps) - 1:
            self.btn_next.config(text="Gerar Plano ✓")
        else:
            self.btn_next.config(text="Próximo →")
    
    def _load_step(self, step_index):
        """Carrega uma etapa específica."""
        # Limpar conteúdo atual
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        self.current_step = step_index
        step_name, step_creator = self.steps[step_index]
        
        # Criar nova etapa
        self.current_step_widget = step_creator()
        
        self._update_progress()
    
    def _next_step(self):
        """Avança para próxima etapa."""
        # Validar etapa atual
        if hasattr(self.current_step_widget, 'validate'):
            if not self.current_step_widget.validate():
                return
        
        # Coletar dados
        if hasattr(self.current_step_widget, 'get_data'):
            data = self.current_step_widget.get_data()
            self.collected_data.update(data)
        
        # Última etapa - gerar plano
        if self.current_step == len(self.steps) - 1:
            self._generate_plan()
            return
        
        # Avançar
        self._load_step(self.current_step + 1)
    
    def _prev_step(self):
        """Volta para etapa anterior."""
        if self.current_step > 0:
            self._load_step(self.current_step - 1)
    
    def _cancel(self):
        """Cancela o wizard."""
        resposta = messagebox.askyesno(
            "Cancelar Criação",
            "Tem certeza que deseja cancelar?\n\nTodos os dados serão perdidos."
        )
        
        if resposta:
            self.frame.destroy()
            self.on_complete()
    
    # ==================== ETAPAS DO WIZARD ====================
    
    def _create_athlete_step(self):
        """Etapa 1: Dados do Atleta."""
        step = tk.Frame(self.content_area, bg=theme.colors['bg_secondary'])
        step.pack(fill='both', expand=True, padx=60, pady=40)
        
        # Título
        tk.Label(
            step,
            text="👤 Dados do Atleta",
            font=(theme.fonts['primary'], theme.font_sizes['title'], 'bold'),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w', pady=(0, 10))
        
        tk.Label(
            step,
            text="Preencha as informações básicas do atleta",
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_secondary']
        ).pack(anchor='w', pady=(0, 30))
        
        # Card com formulário
        form_card = tk.Frame(step, bg=theme.colors['bg_white'])
        form_card.pack(fill='both', expand=True)
        form_card.config(highlightbackground=theme.colors['border_light'], highlightthickness=1)
        
        form_content = tk.Frame(form_card, bg=theme.colors['bg_white'])
        form_content.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Nome
        tk.Label(
            form_content,
            text="Nome Completo *",
            font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w', pady=(0, 5))
        
        step.nome_var = tk.StringVar(value=self.collected_data.get('nome', ''))
        nome_entry = tk.Entry(
            form_content,
            textvariable=step.nome_var,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            relief='solid',
            bd=1
        )
        nome_entry.pack(fill='x', ipady=8, pady=(0, 20))
        nome_entry.focus()
        
        # Idade, Gênero, Peso, Altura em grid
        grid_frame = tk.Frame(form_content, bg=theme.colors['bg_white'])
        grid_frame.pack(fill='x', pady=(0, 20))
        
        # Idade
        col1 = tk.Frame(grid_frame, bg=theme.colors['bg_white'])
        col1.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        tk.Label(
            col1,
            text="Idade *",
            font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w', pady=(0, 5))
        
        step.idade_var = tk.StringVar(value=self.collected_data.get('idade', ''))
        tk.Entry(
            col1,
            textvariable=step.idade_var,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            relief='solid',
            bd=1,
            width=10
        ).pack(fill='x', ipady=8)
        
        # Gênero
        col2 = tk.Frame(grid_frame, bg=theme.colors['bg_white'])
        col2.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        tk.Label(
            col2,
            text="Gênero *",
            font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w', pady=(0, 5))
        
        step.genero_var = tk.StringVar(value=self.collected_data.get('genero', 'Masculino'))
        genero_combo = ttk.Combobox(
            col2,
            textvariable=step.genero_var,
            values=['Masculino', 'Feminino', 'Outro'],
            state='readonly',
            font=(theme.fonts['primary'], theme.font_sizes['body'])
        )
        genero_combo.pack(fill='x', ipady=8)
        
        # Peso e Altura
        grid_frame2 = tk.Frame(form_content, bg=theme.colors['bg_white'])
        grid_frame2.pack(fill='x', pady=(0, 20))
        
        # Peso
        col3 = tk.Frame(grid_frame2, bg=theme.colors['bg_white'])
        col3.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        tk.Label(
            col3,
            text="Peso (kg) *",
            font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w', pady=(0, 5))
        
        step.peso_var = tk.StringVar(value=self.collected_data.get('peso', ''))
        tk.Entry(
            col3,
            textvariable=step.peso_var,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            relief='solid',
            bd=1
        ).pack(fill='x', ipady=8)
        
        # Altura
        col4 = tk.Frame(grid_frame2, bg=theme.colors['bg_white'])
        col4.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        tk.Label(
            col4,
            text="Altura (cm) *",
            font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w', pady=(0, 5))
        
        step.altura_var = tk.StringVar(value=self.collected_data.get('altura', ''))
        tk.Entry(
            col4,
            textvariable=step.altura_var,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            relief='solid',
            bd=1
        ).pack(fill='x', ipady=8)
        
        # Funções de validação e coleta
        def validate():
            if not step.nome_var.get().strip():
                messagebox.showerror("Erro", "Nome é obrigatório.")
                return False
            
            try:
                idade = int(step.idade_var.get())
                if idade < 1 or idade > 120:
                    messagebox.showerror("Erro", "Idade deve estar entre 1 e 120.")
                    return False
            except ValueError:
                messagebox.showerror("Erro", "Idade deve ser um número.")
                return False
            
            try:
                peso = float(step.peso_var.get())
                if peso < 20 or peso > 300:
                    messagebox.showerror("Erro", "Peso deve estar entre 20 e 300 kg.")
                    return False
            except ValueError:
                messagebox.showerror("Erro", "Peso deve ser um número.")
                return False
            
            try:
                altura = float(step.altura_var.get())
                if altura < 50 or altura > 250:
                    messagebox.showerror("Erro", "Altura deve estar entre 50 e 250 cm.")
                    return False
            except ValueError:
                messagebox.showerror("Erro", "Altura deve ser um número.")
                return False
            
            return True
        
        def get_data():
            return {
                'nome': step.nome_var.get().strip(),
                'idade': int(step.idade_var.get()),
                'genero': step.genero_var.get(),
                'peso': float(step.peso_var.get()),
                'altura': float(step.altura_var.get())
            }
        
        step.validate = validate
        step.get_data = get_data
        
        return step
    
    def _create_sport_step(self):
        """Etapa 2: Modalidade Esportiva."""
        step = tk.Frame(self.content_area, bg=theme.colors['bg_secondary'])
        step.pack(fill='both', expand=True, padx=60, pady=40)
        
        # Título
        tk.Label(
            step,
            text="🏃 Modalidade Esportiva",
            font=(theme.fonts['primary'], theme.font_sizes['title'], 'bold'),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w', pady=(0, 10))
        
        tk.Label(
            step,
            text="Selecione a modalidade para o plano de treinamento",
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_secondary']
        ).pack(anchor='w', pady=(0, 30))
        
        # Cards de esportes
        sports_container = tk.Frame(step, bg=theme.colors['bg_secondary'])
        sports_container.pack(fill='both', expand=True)
        
        step.esporte_var = tk.StringVar(value=self.collected_data.get('esporte', ''))
        
        esportes = [
            ('Triathlon', '🏊‍♂️🚴‍♂️🏃', theme.colors['primary']),
            ('Corrida', '🏃', theme.colors['analogous_2']),
            ('Natação', '🏊‍♂️', theme.colors['info']),
            ('Ciclismo', '🚴‍♂️', theme.colors['analogous_1']),
            ('Duathlon Natação e Corrida', '🏊‍♂️🏃', theme.colors['triadic_1']),
            ('Duathlon Ciclismo e Corrida', '🚴‍♂️🏃', theme.colors['triadic_2'])
        ]
        
        # Grid 2x3
        for i, (nome, icon, color) in enumerate(esportes):
            row = i // 3
            col = i % 3
            
            card = self._create_sport_card(sports_container, nome, icon, color, step.esporte_var)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Configurar grid
        for i in range(3):
            sports_container.columnconfigure(i, weight=1)
        for i in range(2):
            sports_container.rowconfigure(i, weight=1)
        
        def validate():
            if not step.esporte_var.get():
                messagebox.showerror("Erro", "Selecione uma modalidade esportiva.")
                return False
            return True
        
        def get_data():
            return {'esporte': step.esporte_var.get()}
        
        step.validate = validate
        step.get_data = get_data
        
        return step
    
    def _create_sport_card(self, parent, nome, icon, color, var):
        """Cria card de seleção de esporte."""
        card = tk.Frame(parent, bg=theme.colors['bg_white'], cursor='hand2')
        card.config(highlightbackground=theme.colors['border_light'], highlightthickness=2)
        
        # Barra colorida
        top_bar = tk.Frame(card, bg=color, height=6)
        top_bar.pack(fill='x')
        
        # Conteúdo
        content = tk.Frame(card, bg=theme.colors['bg_white'])
        content.pack(fill='both', expand=True, pady=20)
        
        # Ícone
        tk.Label(
            content,
            text=icon,
            font=(theme.fonts['primary'], 40),
            bg=theme.colors['bg_white']
        ).pack(pady=(10, 10))
        
        # Nome
        tk.Label(
            content,
            text=nome,
            font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
            wraplength=180
        ).pack(pady=(0, 10))
        
        # Indicador de seleção
        indicator = tk.Label(
            content,
            text="",
            font=(theme.fonts['primary'], 16),
            bg=theme.colors['bg_white']
        )
        indicator.pack()
        
        def update_selection():
            if var.get() == nome:
                card.config(highlightbackground=color, highlightthickness=3)
                indicator.config(text="✓ Selecionado", fg=color)
            else:
                card.config(highlightbackground=theme.colors['border_light'], highlightthickness=2)
                indicator.config(text="")
        
        def on_click(e=None):
            var.set(nome)
            update_selection()
        
        # Bind eventos
        for widget in [card, content, top_bar, indicator]:
            widget.bind('<Button-1>', on_click)
        
        # Atualizar se já selecionado
        var.trace('w', lambda *args: update_selection())
        update_selection()
        
        return card
    
    def _create_period_step(self):
        """Etapa 3: Período de Treinamento."""
        step_widget = PeriodoStep(self.content_area, self)
        step_widget.pack(fill='both', expand=True)
        
        # Carregar dados anteriores se existirem
        if 'semanas_ate_prova' in self.collected_data:
            step_widget.data['semanas'].set(self.collected_data['semanas_ate_prova'])
        
        return step_widget
    
    def _create_distance_step(self):
        """Etapa 4: Distância e Fisiologia."""
        step_widget = DistanciaStep(self.content_area, self)
        step_widget.pack(fill='both', expand=True)
        
        # Atualizar distâncias baseado no esporte selecionado
        if 'esporte' in self.collected_data:
            step_widget.update_distancias(self.collected_data['esporte'])
        
        # Carregar dados anteriores
        if 'limiar_lactato' in self.collected_data:
            step_widget.data['limiar'].set(str(self.collected_data['limiar_lactato']))
        if 'vo2_max' in self.collected_data:
            step_widget.data['vo2max'].set(str(self.collected_data['vo2_max']))
        
        return step_widget
    
    def _create_availability_step(self):
        """Etapa 5: Disponibilidade."""
        step = tk.Frame(self.content_area, bg=theme.colors['bg_secondary'])
        step.pack(fill='both', expand=True, padx=60, pady=40)
        
        # Título
        tk.Label(
            step,
            text="📅 Disponibilidade",
            font=(theme.fonts['primary'], theme.font_sizes['title'], 'bold'),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w', pady=(0, 10))
        
        tk.Label(
            step,
            text="Quantos dias por semana o atleta pode treinar?",
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_secondary']
        ).pack(anchor='w', pady=(0, 30))
        
        # Card
        card = tk.Frame(step, bg=theme.colors['bg_white'])
        card.pack(fill='both', expand=True)
        card.config(highlightbackground=theme.colors['border_light'], highlightthickness=1)
        
        card_content = tk.Frame(card, bg=theme.colors['bg_white'])
        card_content.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Slider
        tk.Label(
            card_content,
            text="Dias de treino por semana:",
            font=(theme.fonts['primary'], theme.font_sizes['heading']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(pady=(0, 30))
        
        step.dias_var = tk.IntVar(value=self.collected_data.get('dias_semana', 4))
        
        # Display do valor
        value_display = tk.Label(
            card_content,
            textvariable=step.dias_var,
            font=(theme.fonts['primary'], 72, 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['primary']
        )
        value_display.pack(pady=(0, 10))
        
        tk.Label(
            card_content,
            text="dias",
            font=(theme.fonts['primary'], theme.font_sizes['heading']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(pady=(0, 40))
        
        # Slider
        slider = tk.Scale(
            card_content,
            from_=1,
            to=7,
            orient='horizontal',
            variable=step.dias_var,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            length=500,
            showvalue=0,
            bd=0,
            highlightthickness=0,
            troughcolor=theme.colors['bg_secondary'],
            activebackground=theme.colors['accent_hover'],
            bg=theme.colors['primary']
        )
        slider.pack()
        
        # Legenda
        legend_frame = tk.Frame(card_content, bg=theme.colors['bg_white'])
        legend_frame.pack(fill='x', pady=(20, 0))
        
        tk.Label(
            legend_frame,
            text="1 dia\n(Mínimo)",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
            justify='center'
        ).pack(side='left')
        
        tk.Label(
            legend_frame,
            text="7 dias\n(Máximo)",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
            justify='center'
        ).pack(side='right')
        
        def validate():
            return True
        
        def get_data():
            return {'dias_semana': step.dias_var.get()}
        
        step.validate = validate
        step.get_data = get_data
        
        return step
    
    def _create_review_step(self):
        """Etapa 6: Revisão e Geração."""
        step = tk.Frame(self.content_area, bg=theme.colors['bg_secondary'])
        step.pack(fill='both', expand=True, padx=60, pady=40)
        
        # Título
        tk.Label(
            step,
            text="✓ Revisão dos Dados",
            font=(theme.fonts['primary'], theme.font_sizes['title'], 'bold'),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w', pady=(0, 10))
        
        tk.Label(
            step,
            text="Revise as informações antes de gerar o plano",
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_secondary']
        ).pack(anchor='w', pady=(0, 30))
        
        # Card de revisão
        card = tk.Frame(step, bg=theme.colors['bg_white'])
        card.pack(fill='both', expand=True)
        card.config(highlightbackground=theme.colors['border_light'], highlightthickness=1)
        
        card_content = tk.Frame(card, bg=theme.colors['bg_white'])
        card_content.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Criar resumo
        dados = self.collected_data
        
        resumo = f"""
👤 ATLETA
   Nome: {dados.get('nome', 'N/A')}
   Idade: {dados.get('idade', 'N/A')} anos
   Gênero: {dados.get('genero', 'N/A')}
   Peso: {dados.get('peso', 'N/A')} kg
   Altura: {dados.get('altura', 'N/A')} cm

🏃 MODALIDADE
   Esporte: {dados.get('esporte', 'N/A')}
   Distância: {dados.get('distancia_prova', 'N/A')}

⏱️ PERÍODO
   Semanas até a prova: {dados.get('semanas_ate_prova', 'N/A')}

💓 DADOS FISIOLÓGICOS
   Limiar de Lactato: {dados.get('limiar_lactato', 'N/A')} bpm
   VO2 Max: {dados.get('vo2_max', 'N/A')} ml/kg/min

📅 DISPONIBILIDADE
   Dias por semana: {dados.get('dias_semana', 'N/A')}
        """
        
        text_widget = tk.Text(
            card_content,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
            relief='flat',
            wrap='word',
            height=15
        )
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', resumo.strip())
        text_widget.config(state='disabled')
        
        # Separador
        tk.Frame(
            card_content,
            bg=theme.colors['border_light'],
            height=1
        ).pack(fill='x', pady=20)
        
        # Opção de formato de exportação
        tk.Label(
            card_content,
            text="📄 Formato de Exportação",
            font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w', pady=(0, 10))
        
        step.export_format = tk.StringVar(value='excel')
        
        formats_frame = tk.Frame(card_content, bg=theme.colors['bg_white'])
        formats_frame.pack(anchor='w', pady=(0, 10))
        
        # Opção Excel
        excel_radio = tk.Radiobutton(
            formats_frame,
            text="📊 Excel (.xlsx) - Formato editável com múltiplas abas",
            variable=step.export_format,
            value='excel',
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
            activebackground=theme.colors['bg_white'],
            selectcolor=theme.colors['bg_secondary']
        )
        excel_radio.pack(anchor='w', pady=5)
        
        # Opção PDF
        pdf_radio = tk.Radiobutton(
            formats_frame,
            text="📄 PDF (.pdf) - Formato profissional para impressão",
            variable=step.export_format,
            value='pdf',
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
            activebackground=theme.colors['bg_white'],
            selectcolor=theme.colors['bg_secondary']
        )
        pdf_radio.pack(anchor='w', pady=5)
        
        # Opção Ambos
        both_radio = tk.Radiobutton(
            formats_frame,
            text="📊📄 Ambos - Gerar Excel e PDF simultaneamente",
            variable=step.export_format,
            value='both',
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
            activebackground=theme.colors['bg_white'],
            selectcolor=theme.colors['bg_secondary']
        )
        both_radio.pack(anchor='w', pady=5)
        
        def validate():
            return True
        
        def get_data():
            return {'export_format': step.export_format.get()}
        
        step.validate = validate
        step.get_data = get_data
        
        return step
    
    def _generate_plan(self):
        """Gera o plano de treinamento."""
        try:
            # Criar objeto Athlete
            athlete = Athlete(
                nome=self.collected_data['nome'],
                idade=self.collected_data['idade'],
                genero=self.collected_data['genero'],
                peso=self.collected_data['peso'],
                altura=self.collected_data['altura'],
                esporte=self.collected_data['esporte'],
                distancia_prova=self.collected_data['distancia_prova'],
                semanas_ate_prova=self.collected_data['semanas_ate_prova'],
                dias_semana=self.collected_data['dias_semana'],
                limiar_lactato=self.collected_data['limiar_lactato'],
                vo2_max=self.collected_data['vo2_max'],
                trainer=self.trainer_info
            )
            
            # Gerar plano
            generator = TrainingPlanGenerator(athlete)
            plano = generator.get_full_training_plan()
            
            # Obter diretório específico do profissional
            plans_dir = training_manager.get_plans_directory(self.trainer_info)
            
            # Obter formato de exportação
            export_format = self.collected_data.get('export_format', 'excel')
            
            filenames = []
            excel_path = None
            pdf_path = None
            
            # Exportar conforme formato selecionado
            if export_format in ['excel', 'both']:
                # Exportar para Excel no diretório do profissional
                exporter = ExcelExporter(athlete, plano, is_full_plan=True, output_dir=plans_dir)
                excel_path = exporter.export_to_excel()
                filenames.append(('Excel', excel_path))
            
            if export_format in ['pdf', 'both']:
                # Exportar para PDF no diretório do profissional
                pdf_exporter = PDFExporter(athlete, plano, is_full_plan=True, output_dir=plans_dir)
                pdf_path = pdf_exporter.export_to_pdf()
                filenames.append(('PDF', pdf_path))
            
            # Registrar treino no sistema de gerenciamento
            training_manager.register_training(
                self.trainer_info,
                athlete,
                excel_path=excel_path,
                pdf_path=pdf_path
            )
            
            # Mensagem de sucesso
            if len(filenames) == 1:
                format_name, filename = filenames[0]
                messagebox.showinfo(
                    "Plano Gerado com Sucesso!",
                    f"O plano de treinamento foi gerado e salvo em {format_name}:\n\n{filename}\n\n"
                    f"Total de {len(plano)} treinos criados para {athlete.semanas_ate_prova} semanas.\n\n"
                    f"📋 Dados do Treinador incluídos:\n"
                    f"• Nome: {athlete.trainer.nome_completo}\n"
                    f"• CPF: {athlete.trainer.formatar_cpf()}\n"
                    f"• CREF: {athlete.trainer.formatar_cref()}\n\n"
                    f"🔒 Este treino está salvo no seu diretório pessoal e apenas você pode acessá-lo."
                )
            else:
                files_text = '\n'.join([f"• {fmt}: {fname}" for fmt, fname in filenames])
                messagebox.showinfo(
                    "Plano Gerado com Sucesso!",
                    f"O plano de treinamento foi gerado nos seguintes formatos:\n\n{files_text}\n\n"
                    f"Total de {len(plano)} treinos criados para {athlete.semanas_ate_prova} semanas.\n\n"
                    f"📋 Dados do Treinador incluídos:\n"
                    f"• Nome: {athlete.trainer.nome_completo}\n"
                    f"• CPF: {athlete.trainer.formatar_cpf()}\n"
                    f"• CREF: {athlete.trainer.formatar_cref()}\n\n"
                    f"🔒 Este treino está salvo no seu diretório pessoal e apenas você pode acessá-lo."
                )
            
            # Voltar ao dashboard
            self.frame.destroy()
            self.on_complete()
            
        except Exception as e:
            messagebox.showerror(
                "Erro ao Gerar Plano",
                f"Ocorreu um erro ao gerar o plano:\n\n{str(e)}"
            )
