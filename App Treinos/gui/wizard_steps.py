"""
Wizard Steps Adicionais - App Treinos GUI
==========================================

Etapas do assistente para coleta completa de dados.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from gui.theme import theme


class PeriodoStep(tk.Frame):
    """Etapa 3: Período de Treinamento."""
    
    def __init__(self, parent, wizard_ref):
        super().__init__(parent, bg=theme.colors['bg_primary'])
        self.wizard = wizard_ref
        self.data = {}
        self._create_ui()
    
    def _create_ui(self):
        """Cria interface."""
        # Header
        header = ttk.Frame(self, style='Card.TFrame')
        header.pack(fill='x', padx=theme.spacing['xl'], pady=theme.spacing['md'])
        
        ttk.Label(header, text="📅 Período de Treinamento",
                 style='Heading.TLabel').pack(
            anchor='w', padx=theme.spacing['md'], pady=(theme.spacing['md'], theme.spacing['xs'])
        )
        
        ttk.Label(header, text="Configure o tempo até sua prova").pack(
            anchor='w', padx=theme.spacing['md'], pady=(0, theme.spacing['md'])
        )
        
        # Body
        body = ttk.Frame(self)
        body.pack(fill='both', expand=True, padx=theme.spacing['xl'], pady=theme.spacing['md'])
        
        # Modo de entrada
        self.data['modo'] = tk.StringVar(value="data")
        
        ttk.Radiobutton(body, text="📅 Informar data da prova",
                       variable=self.data['modo'], value="data",
                       command=self._toggle_mode).pack(anchor='w', pady=theme.spacing['sm'])
        
        # Frame para data
        self.data_frame = ttk.Frame(body)
        self.data_frame.pack(fill='x', pady=theme.spacing['sm'], padx=theme.spacing['xl'])
        
        ttk.Label(self.data_frame, text="Data da prova (DD/MM/AAAA):").pack(anchor='w')
        self.data['data_prova'] = tk.StringVar()
        ttk.Entry(self.data_frame, textvariable=self.data['data_prova'],
                 width=20).pack(anchor='w', pady=theme.spacing['xs'])
        ttk.Label(self.data_frame, text="Ex: 15/08/2026, 03/12/2026",
                 foreground=theme.colors['text_disabled'],
                 font=(theme.fonts['primary'], theme.font_sizes['small'])).pack(anchor='w')
        
        ttk.Separator(body, orient='horizontal').pack(fill='x', pady=theme.spacing['md'])
        
        ttk.Radiobutton(body, text="📊 Informar número de semanas",
                       variable=self.data['modo'], value="semanas",
                       command=self._toggle_mode).pack(anchor='w', pady=theme.spacing['sm'])
        
        # Frame para semanas
        self.semanas_frame = ttk.Frame(body)
        self.semanas_frame.pack(fill='x', pady=theme.spacing['sm'], padx=theme.spacing['xl'])
        
        ttk.Label(self.semanas_frame, text="Semanas até a prova:").pack(anchor='w')
        
        scale_frame = ttk.Frame(self.semanas_frame)
        scale_frame.pack(anchor='w', pady=theme.spacing['xs'])
        
        self.data['semanas'] = tk.IntVar(value=12)
        ttk.Scale(scale_frame, from_=1, to=52, variable=self.data['semanas'],
                 orient='horizontal', length=300).pack(side='left')
        ttk.Label(scale_frame, textvariable=self.data['semanas'],
                 font=(theme.fonts['primary'], theme.font_sizes['heading'], 'bold')).pack(
            side='left', padx=theme.spacing['md']
        )
        ttk.Label(scale_frame, text="semanas").pack(side='left')
        
        self._toggle_mode()
    
    def _toggle_mode(self):
        """Alterna entre modos de entrada."""
        modo = self.data['modo'].get()
        if modo == "data":
            for child in self.data_frame.winfo_children():
                child.config(state='normal')
            for child in self.semanas_frame.winfo_children():
                if isinstance(child, (ttk.Entry, ttk.Scale)):
                    child.config(state='disabled')
        else:
            for child in self.data_frame.winfo_children():
                if isinstance(child, (ttk.Entry, ttk.Scale)):
                    child.config(state='disabled')
            for child in self.semanas_frame.winfo_children():
                child.config(state='normal')
    
    def validate(self):
        """Valida período."""
        modo = self.data['modo'].get()
        
        if modo == "data":
            try:
                data_str = self.data['data_prova'].get().strip()
                data = datetime.strptime(data_str, "%d/%m/%Y")
                
                if data <= datetime.now():
                    messagebox.showerror("Erro", "A data da prova deve ser futura.")
                    return False
                
                dias = (data - datetime.now()).days
                semanas = (dias + 6) // 7
                
                if semanas > 52:
                    messagebox.showwarning("Aviso",
                        f"A data informada resulta em {semanas} semanas.\n"
                        "O sistema está limitado a 52 semanas (1 ano).\n"
                        "Ajustando para 52 semanas.")
                    self.data['semanas_calculadas'] = 52
                else:
                    self.data['semanas_calculadas'] = semanas
                
                return True
            except ValueError:
                messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/AAAA.")
                return False
        else:
            semanas = self.data['semanas'].get()
            self.data['semanas_calculadas'] = semanas
            return True
    
    def get_data(self):
        """Retorna dados."""
        return {'semanas_ate_prova': self.data.get('semanas_calculadas', 12)}


class DistanciaStep(tk.Frame):
    """Etapa 4: Distância e Dados Fisiológicos."""
    
    def __init__(self, parent, wizard_ref):
        super().__init__(parent, bg=theme.colors['bg_primary'])
        self.wizard = wizard_ref
        self.data = {}
        self._create_ui()
    
    def _create_ui(self):
        """Cria interface."""
        # Header
        header = ttk.Frame(self, style='Card.TFrame')
        header.pack(fill='x', padx=theme.spacing['xl'], pady=theme.spacing['md'])
        
        ttk.Label(header, text="🎯 Distância e Fisiologia",
                 style='Heading.TLabel').pack(
            anchor='w', padx=theme.spacing['md'], pady=(theme.spacing['md'], theme.spacing['xs'])
        )
        
        ttk.Label(header, text="Configure a distância da prova e dados fisiológicos").pack(
            anchor='w', padx=theme.spacing['md'], pady=(0, theme.spacing['md'])
        )
        
        # Body
        body = ttk.Frame(self)
        body.pack(fill='both', expand=True, padx=theme.spacing['xl'], pady=theme.spacing['md'])
        
        # Distâncias por esporte
        self.distancias_map = {
            'Triathlon': ['Sprint', 'Olímpico', 'Meio Ironman', 'Ironman'],
            'Corrida': ['5K', '10K', 'Meia Maratona', 'Maratona'],
            'Natação': ['1500m', '3000m', '5000m'],
            'Ciclismo': ['40K', '80K', '160K']
        }
        
        # Distância
        ttk.Label(body, text="Distância da prova:", font=(theme.fonts['primary'],
                 theme.font_sizes['body'], 'bold')).pack(anchor='w', pady=(0, theme.spacing['xs']))
        
        self.data['distancia'] = tk.StringVar()
        self.combo_distancia = ttk.Combobox(body, textvariable=self.data['distancia'],
                                           state='readonly', width=37)
        self.combo_distancia.pack(anchor='w', pady=theme.spacing['sm'])
        
        ttk.Separator(body, orient='horizontal').pack(fill='x', pady=theme.spacing['md'])
        
        # Dados fisiológicos
        ttk.Label(body, text="💓 Dados Fisiológicos", font=(theme.fonts['primary'],
                 theme.font_sizes['subheading'], 'bold')).pack(anchor='w',
                 pady=(theme.spacing['md'], theme.spacing['sm']))
        
        # Limiar de lactato
        ttk.Label(body, text="Limiar de Lactato (bpm):").pack(anchor='w')
        self.data['limiar'] = tk.StringVar(value="165")
        ttk.Entry(body, textvariable=self.data['limiar'], width=15).pack(
            anchor='w', pady=theme.spacing['xs'])
        ttk.Label(body, text="Ex: 165, 172.5, 180",
                 foreground=theme.colors['text_disabled'],
                 font=(theme.fonts['primary'], theme.font_sizes['small'])).pack(anchor='w')
        
        # VO2 Max
        ttk.Label(body, text="VO2 Max (ml/kg/min):", style='TLabel').pack(
            anchor='w', pady=(theme.spacing['md'], 0))
        self.data['vo2max'] = tk.StringVar(value="50")
        ttk.Entry(body, textvariable=self.data['vo2max'], width=15).pack(
            anchor='w', pady=theme.spacing['xs'])
        ttk.Label(body, text="Ex: 45.5, 52, 68.3",
                 foreground=theme.colors['text_disabled'],
                 font=(theme.fonts['primary'], theme.font_sizes['small'])).pack(anchor='w')
    
    def update_distancias(self, esporte):
        """Atualiza combo de distâncias baseado no esporte."""
        distancias = self.distancias_map.get(esporte, [])
        self.combo_distancia['values'] = distancias
        if distancias:
            self.combo_distancia.current(0)
    
    def validate(self):
        """Valida distância e fisiologia."""
        try:
            if not self.data['distancia'].get():
                messagebox.showerror("Erro", "Selecione a distância da prova.")
                return False
            
            limiar = float(self.data['limiar'].get())
            if not (100 <= limiar <= 220):
                messagebox.showerror("Erro",
                    "Limiar de lactato deve estar entre 100 e 220 bpm.")
                return False
            
            vo2max = float(self.data['vo2max'].get())
            if not (20 <= vo2max <= 90):
                messagebox.showerror("Erro",
                    "VO2 Max deve estar entre 20 e 90 ml/kg/min.")
                return False
            
            return True
        except ValueError:
            messagebox.showerror("Erro", "Valores fisiológicos devem ser numéricos.")
            return False
    
    def get_data(self):
        """Retorna dados."""
        return {
            'distancia_prova': self.data['distancia'].get(),
            'limiar_lactato': float(self.data['limiar'].get()),
            'vo2_max': float(self.data['vo2max'].get())
        }
