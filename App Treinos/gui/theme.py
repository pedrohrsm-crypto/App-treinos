"""
GUI Theme Module - Tema Acessível para App Treinos
==================================================

Este módulo define cores, fontes e estilos com foco em acessibilidade
e conformidade com WCAG 2.1 (Web Content Accessibility Guidelines).
"""

import tkinter as tk
from tkinter import ttk
import platform


class AccessibleTheme:
    """Tema acessível com alto contraste e design responsivo."""
    
    def __init__(self):
        self.system = platform.system()
        
        # Paleta de cores profissional e acolhedora
        self.colors = {
            # Cores principais - Paleta customizada
            'primary': '#68b2c2',        # Azul turquesa (cor primária)
            'complementary': '#c27968',  # Coral/terracota
            'analogous_1': '#68c2a6',    # Verde-azulado
            'analogous_2': '#6885c2',    # Azul
            'triadic_1': '#7968c2',      # Roxo
            'triadic_2': '#c268b2',      # Magenta
            
            # Fundos
            'bg_primary': '#68b2c2',     # Fundo principal (cor primária)
            'bg_secondary': '#f0f8fa',   # Fundo claro (derivado da primária)
            'bg_tertiary': '#e6f4f7',    # Fundo alternativo
            'bg_white': '#FFFFFF',       # Branco puro
            'bg_card': '#FFFFFF',        # Fundo de cards
            
            # Texto - alto contraste
            'text_primary': '#1a1a1a',   # Texto principal (quase preto)
            'text_secondary': '#4a4a4a', # Texto secundário
            'text_disabled': '#9a9a9a',  # Texto desabilitado
            'text_light': '#FFFFFF',     # Texto claro (sobre fundos escuros)
            
            # Destaques e hover
            'accent_primary': '#68b2c2',
            'accent_hover': '#5a9eb0',   # Tom mais escuro da primária
            'accent_active': '#4c8a9e',  # Tom ainda mais escuro
            
            # Estados
            'success': '#68c2a6',        # Verde análogo
            'warning': '#c27968',        # Coral complementar
            'error': '#c26868',          # Vermelho suave
            'info': '#6885c2',           # Azul análogo
            
            # Bordas e sombras
            'border_light': '#d0e8ed',   # Borda clara (derivada da primária)
            'border_medium': '#a8cfd9',  # Borda média
            'border_dark': '#68b2c2',    # Borda escura (primária)
            'shadow': '#b3d9e0',         # Sombra suave (tom claro da primária)
            'shadow_strong': '#8fc6d1'   # Sombra forte (tom médio da primária)
        }
        
        # Fontes do sistema (sans-serif)
        self.fonts = self._get_system_fonts()
        
        # Tamanhos de fonte (escaláveis e acolhedores)
        self.font_sizes = {
            'splash': 48,      # Logo/Splash screen
            'title': 32,       # Títulos principais
            'heading': 24,     # Cabeçalhos
            'subheading': 18,  # Subcabeçalhos
            'body': 14,        # Texto corpo
            'small': 12,       # Texto pequeno
            'button': 14,      # Botões
            'card_title': 20   # Título de cards
        }
        
        # Espaçamentos (em pixels)
        self.spacing = {
            'xs': 4,
            'sm': 8,
            'md': 16,
            'lg': 24,
            'xl': 32
        }
        
        # Dimensões de componentes
        self.sizes = {
            'button_height': 50,
            'input_height': 45,
            'label_width': 200,
            'min_width': 1000,
            'min_height': 700,
            'card_width': 280,
            'card_height': 200,
            'hero_card_width': 350,
            'hero_card_height': 250
        }
    
    def _get_system_fonts(self):
        """Retorna fontes do sistema adequadas."""
        if self.system == 'Windows':
            family = 'Segoe UI'
            fallback = 'Arial'
        elif self.system == 'Darwin':  # macOS
            family = 'SF Pro Text'
            fallback = 'Helvetica Neue'
        else:  # Linux
            family = 'Ubuntu'
            fallback = 'DejaVu Sans'
        
        return {
            'primary': family,
            'fallback': fallback,
            'monospace': 'Consolas' if self.system == 'Windows' else 'Monaco'
        }
    
    def configure_ttk_style(self, root):
        """Configura o estilo ttk com o tema acessível."""
        style = ttk.Style(root)
        
        # Tema base
        style.theme_use('clam')
        
        # TLabel
        style.configure('TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=(self.fonts['primary'], self.font_sizes['body']))
        
        style.configure('Title.TLabel',
                       font=(self.fonts['primary'], self.font_sizes['title'], 'bold'))
        
        style.configure('Heading.TLabel',
                       font=(self.fonts['primary'], self.font_sizes['heading'], 'bold'))
        
        style.configure('Subheading.TLabel',
                       font=(self.fonts['primary'], self.font_sizes['subheading'], 'bold'))
        
        # TButton
        style.configure('TButton',
                       font=(self.fonts['primary'], self.font_sizes['button']),
                       padding=(self.spacing['md'], self.spacing['sm']),
                       background=self.colors['accent_primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor=self.colors['accent_active'])
        
        style.map('TButton',
                 background=[('active', self.colors['accent_hover']),
                           ('pressed', self.colors['accent_active']),
                           ('disabled', self.colors['bg_tertiary'])],
                 foreground=[('disabled', self.colors['text_disabled'])])
        
        # Primary Button (destaque)
        style.configure('Primary.TButton',
                       font=(self.fonts['primary'], self.font_sizes['button'], 'bold'),
                       padding=(self.spacing['lg'], self.spacing['md']))
        
        # TEntry
        style.configure('TEntry',
                       font=(self.fonts['primary'], self.font_sizes['body']),
                       fieldbackground='white',
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       relief='solid')
        
        # TCombobox
        style.configure('TCombobox',
                       font=(self.fonts['primary'], self.font_sizes['body']),
                       fieldbackground='white',
                       foreground=self.colors['text_primary'],
                       borderwidth=1)
        
        # TFrame
        style.configure('TFrame',
                       background=self.colors['bg_primary'])
        
        style.configure('Card.TFrame',
                       background=self.colors['bg_secondary'],
                       relief='raised',
                       borderwidth=1)
        
        # TNotebook (abas)
        style.configure('TNotebook',
                       background=self.colors['bg_primary'],
                       borderwidth=0)
        
        style.configure('TNotebook.Tab',
                       font=(self.fonts['primary'], self.font_sizes['body'], 'bold'),
                       padding=(self.spacing['lg'], self.spacing['md']),
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'])
        
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent_primary']),
                           ('active', self.colors['bg_tertiary'])],
                 foreground=[('selected', 'white')])
        
        # Progressbar
        style.configure('TProgressbar',
                       background=self.colors['accent_primary'],
                       troughcolor=self.colors['bg_tertiary'],
                       borderwidth=0,
                       thickness=20)
        
        # Separator
        style.configure('TSeparator',
                       background=self.colors['border_light'])
        
        return style
    
    def get_validation_color(self, is_valid):
        """Retorna cor para validação de campo."""
        return self.colors['success'] if is_valid else self.colors['error']


# Instância global do tema
theme = AccessibleTheme()
