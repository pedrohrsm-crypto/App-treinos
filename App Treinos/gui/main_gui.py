"""
App Treinos - Interface Gráfica Principal v2.0
===============================================

Interface gráfica moderna com splash screen, login e dashboard.
Experiência de usuário otimizada para profissionais de Educação Física.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import sys
from pathlib import Path

# Adicionar diretórios ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from gui.theme import theme
from core.database import db_manager
from gui.register_screen import RegisterScreen
from gui.admin_panel import AdminPanel
from gui.training_wizard import TrainingWizard
from gui.training_list import TrainingListScreen
from training_planner import TrainerInfo
from pdf_exporter import PDFExporter
from tkinter import filedialog
from pathlib import Path


class SplashScreen:
    """Tela inicial com logo e nome do aplicativo."""
    
    def __init__(self, parent, on_complete):
        self.parent = parent
        self.on_complete = on_complete
        self.alpha = 0.0
        self.fade_in = True
        
        # Pré-calcular valores RGB para otimização
        self._cache_rgb_values()
        
        # Container principal
        self.frame = tk.Frame(parent, bg=theme.colors['bg_primary'])
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Container centralizado
        center_frame = tk.Frame(self.frame, bg=theme.colors['bg_primary'])
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Logo placeholder (será substituído posteriormente)
        self.logo_label = tk.Label(
            center_frame,
            text="🏃",
            font=(theme.fonts['primary'], 120),
            bg=theme.colors['bg_primary'],
            fg=theme.colors['text_light']
        )
        self.logo_label.pack(pady=(0, 20))
        
        # Nome do aplicativo
        self.app_name = tk.Label(
            center_frame,
            text="App Treinos",
            font=(theme.fonts['primary'], theme.font_sizes['splash'], 'bold'),
            bg=theme.colors['bg_primary'],
            fg=theme.colors['text_light']
        )
        self.app_name.pack()
        
        # Subtítulo
        self.subtitle = tk.Label(
            center_frame,
            text="Sistema Profissional de Planejamento Esportivo",
            font=(theme.fonts['primary'], theme.font_sizes['subheading']),
            bg=theme.colors['bg_primary'],
            fg=theme.colors['text_light']
        )
        self.subtitle.pack(pady=(10, 0))
        
        # Iniciar animação
        self.animate()
    
    def _cache_rgb_values(self):
        """Pré-calcula valores RGB para otimizar interpolação."""
        bg = theme.colors['bg_primary']
        fg = theme.colors['text_light']
        
        self.r1 = int(bg[1:3], 16)
        self.g1 = int(bg[3:5], 16)
        self.b1 = int(bg[5:7], 16)
        
        self.r2 = int(fg[1:3], 16)
        self.g2 = int(fg[3:5], 16)
        self.b2 = int(fg[5:7], 16)
        
        # Pré-calcular deltas
        self.dr = self.r2 - self.r1
        self.dg = self.g2 - self.g1
        self.db = self.b2 - self.b1
    
    def animate(self):
        """Anima o fade in e fade out."""
        if self.fade_in:
            self.alpha += 0.05
            if self.alpha >= 1.0:
                self.alpha = 1.0
                self.fade_in = False
                # Esperar 2 segundos no estado visível
                self.parent.after(2000, self.animate)
                return
        else:
            self.alpha -= 0.05
            if self.alpha <= 0.0:
                self.alpha = 0.0
                self.frame.destroy()
                self.on_complete()
                return
        
        # Atualizar opacidade dos elementos
        # Converter alpha para cor (simulação de opacidade com cor)
        self._update_colors()
        
        # Continuar animação
        self.parent.after(50, self.animate)
    
    def _update_colors(self):
        """Atualiza cores para simular fade (otimizado com cache)."""
        # Interpolação otimizada usando valores pré-calculados
        r = int(self.r1 + self.dr * self.alpha)
        g = int(self.g1 + self.dg * self.alpha)
        b = int(self.b1 + self.db * self.alpha)
        
        text_color = f'#{r:02x}{g:02x}{b:02x}'
        
        self.app_name.config(fg=text_color)
        self.subtitle.config(fg=text_color)
        self.logo_label.config(fg=text_color)
    
    def _interpolate_color(self, color1, color2, alpha):
        """Interpola entre duas cores (mantido para compatibilidade)."""
        # Converter hex para RGB
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        # Interpolar
        r = int(r1 + (r2 - r1) * alpha)
        g = int(g1 + (g2 - g1) * alpha)
        b = int(b1 + (b2 - b1) * alpha)
        
        # Converter de volta para hex
        return f'#{r:02x}{g:02x}{b:02x}'


class LoginScreen:
    """Tela de login com CPF ou CREF."""
    
    def __init__(self, parent, on_login):
        self.parent = parent
        self.on_login = on_login
        
        # Container principal
        self.frame = tk.Frame(parent, bg=theme.colors['bg_secondary'])
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Container centralizado (responsivo)
        # Calcula largura: 90% da janela ou 600px, o que for menor
        self.frame.update_idletasks()
        max_width = min(int(parent.winfo_width() * 0.9), 600)
        max_height = int(parent.winfo_height() * 0.9)
        
        center_frame = tk.Frame(self.frame, bg=theme.colors['bg_white'], 
                               relief='flat', bd=0)
        center_frame.place(relx=0.5, rely=0.5, anchor='center', 
                          width=max_width, height=max_height)
        
        # Adicionar sombra (simulada com borda)
        center_frame.config(highlightbackground=theme.colors['shadow_strong'],
                          highlightthickness=2)
        
        # Canvas com scrollbar para conteúdo grande
        self.canvas = tk.Canvas(center_frame, bg=theme.colors['bg_white'], 
                          highlightthickness=0, bd=0)
        self.scrollbar = tk.Scrollbar(center_frame, orient='vertical', 
                                      command=self.canvas.yview,
                                      bg=theme.colors['bg_secondary'],
                                      troughcolor=theme.colors['bg_white'])
        
        # Frame interno para o conteúdo
        content_wrapper = tk.Frame(self.canvas, bg=theme.colors['bg_white'])
        
        # Configurar canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        
        # Criar janela no canvas
        canvas_window = self.canvas.create_window((0, 0), window=content_wrapper, anchor='nw')
        
        # Atualizar scrollregion quando o conteúdo mudar
        def configure_scroll(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))
            # Centralizar conteúdo se menor que canvas
            canvas_width = self.canvas.winfo_width()
            content_width = content_wrapper.winfo_reqwidth()
            if content_width < canvas_width:
                x_offset = (canvas_width - content_width) // 2
                self.canvas.coords(canvas_window, x_offset, 0)
            else:
                self.canvas.coords(canvas_window, 0, 0)
            
            # Mostrar/ocultar scrollbar conforme necessário
            content_height = content_wrapper.winfo_reqheight()
            canvas_height = self.canvas.winfo_height()
            if content_height > canvas_height:
                self.scrollbar.pack(side='right', fill='y')
            else:
                self.scrollbar.pack_forget()
        
        content_wrapper.bind('<Configure>', configure_scroll)
        self.canvas.bind('<Configure>', configure_scroll)
        
        # Habilitar scroll com mouse wheel
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        self.canvas.bind_all('<MouseWheel>', on_mousewheel)
        
        # Bind de redimensionamento da janela
        def on_resize(event=None):
            new_max_width = min(int(parent.winfo_width() * 0.9), 600)
            new_max_height = int(parent.winfo_height() * 0.9)
            center_frame.place_configure(width=new_max_width, height=new_max_height)
        
        parent.bind('<Configure>', on_resize, add='+')
        
        # Armazenar referência ao content_wrapper para ajustes dinâmicos
        self.content_wrapper = content_wrapper
        self.center_frame = center_frame
        
        # Logo pequeno (tamanho ajustável)
        self.logo = tk.Label(
            content_wrapper,
            text="🏃",
            font=(theme.fonts['primary'], 80),
            bg=theme.colors['bg_white'],
            fg=theme.colors['primary']
        )
        self.logo.pack(pady=(30, 10))
        
        # Título
        self.title = tk.Label(
            content_wrapper,
            text="Bem-vindo!",
            font=(theme.fonts['primary'], theme.font_sizes['title'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        )
        self.title.pack(pady=(0, 5))
        
        # Subtítulo
        self.subtitle = tk.Label(
            content_wrapper,
            text="Faça login para continuar",
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        )
        self.subtitle.pack(pady=(0, 20))
        
        # Campo de entrada (responsivo com padding adaptativo)
        input_frame = tk.Frame(content_wrapper, bg=theme.colors['bg_white'])
        input_frame.pack(pady=10, padx=40, fill='x')
        
        label = tk.Label(
            input_frame,
            text="CPF ou CREF (somente números):",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        )
        label.pack(anchor='w', pady=(0, 5))
        
        self.credential_var = tk.StringVar()
        self.credential_entry = tk.Entry(
            input_frame,
            textvariable=self.credential_var,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightbackground=theme.colors['border_light'],
            highlightcolor=theme.colors['primary']
        )
        self.credential_entry.pack(fill='x', ipady=10)
        self.credential_entry.focus()
        
        # Campo de senha
        label_senha = tk.Label(
            input_frame,
            text="Senha:",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        )
        label_senha.pack(anchor='w', pady=(15, 5))
        
        self.senha_var = tk.StringVar()
        self.senha_entry = tk.Entry(
            input_frame,
            textvariable=self.senha_var,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            show='•',
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightbackground=theme.colors['border_light'],
            highlightcolor=theme.colors['primary']
        )
        self.senha_entry.pack(fill='x', ipady=10)
        
        # Bind Enter key
        self.credential_entry.bind('<Return>', lambda e: self.senha_entry.focus())
        self.senha_entry.bind('<Return>', lambda e: self._do_login())
        
        # Botão de login (responsivo)
        login_btn = tk.Button(
            content_wrapper,
            text="Entrar",
            font=(theme.fonts['primary'], theme.font_sizes['button'], 'bold'),
            bg=theme.colors['primary'],
            fg=theme.colors['text_light'],
            activebackground=theme.colors['accent_hover'],
            activeforeground=theme.colors['text_light'],
            relief='flat',
            cursor='hand2',
            command=self._do_login
        )
        login_btn.pack(pady=(20, 10), padx=40, fill='x', ipady=12)
        
        # Separador (responsivo)
        separator_frame = tk.Frame(content_wrapper, bg=theme.colors['bg_white'])
        separator_frame.pack(pady=15, fill='x', padx=40)
        
        tk.Frame(separator_frame, bg=theme.colors['border_light'], height=1).pack(
            side='left', fill='x', expand=True, padx=(0, 10)
        )
        tk.Label(
            separator_frame,
            text="ou",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(side='left')
        tk.Frame(separator_frame, bg=theme.colors['border_light'], height=1).pack(
            side='left', fill='x', expand=True, padx=(10, 0)
        )
        
        # Botão de cadastro (responsivo)
        cadastro_btn = tk.Button(
            content_wrapper,
            text="Criar Nova Conta",
            font=(theme.fonts['primary'], theme.font_sizes['button'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['primary'],
            activebackground=theme.colors['bg_secondary'],
            activeforeground=theme.colors['primary'],
            relief='solid',
            bd=2,
            cursor='hand2',
            highlightthickness=0,
            command=self._show_register
        )
        cadastro_btn.config(highlightbackground=theme.colors['primary'])
        cadastro_btn.pack(pady=(10, 20), padx=40, fill='x', ipady=12)
        
        # Rodapé - Acesso Administrativo
        footer_frame = tk.Frame(content_wrapper, bg=theme.colors['bg_white'])
        footer_frame.pack(pady=(20, 30))
        
        admin_link = tk.Label(
            footer_frame,
            text="🔐 Acesso Administrativo",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
            cursor='hand2'
        )
        admin_link.pack()
        admin_link.bind('<Button-1>', lambda e: self._admin_login())
        admin_link.bind('<Enter>', lambda e: admin_link.config(
            fg=theme.colors['primary'], 
            font=(theme.fonts['primary'], theme.font_sizes['small'], 'underline')
        ))
        admin_link.bind('<Leave>', lambda e: admin_link.config(
            fg=theme.colors['text_secondary'],
            font=(theme.fonts['primary'], theme.font_sizes['small'])
        ))
    
    def _do_login(self):
        """Realiza o login com autenticação no banco de dados."""
        credential = self.credential_var.get().strip()
        senha = self.senha_var.get()
        
        if not credential:
            messagebox.showerror("Erro", "Por favor, digite seu CPF ou CREF.")
            self.credential_entry.focus()
            return
        
        if not senha:
            messagebox.showerror("Erro", "Por favor, digite sua senha.")
            self.senha_entry.focus()
            return
        
        # Validação básica
        if len(credential) < 4:
            messagebox.showerror("Erro", "Credencial inválida. Digite CPF (11 dígitos) ou CREF (4-6 dígitos).")
            self.credential_entry.focus()
            return
        
        # Autenticar no banco de dados
        sucesso, usuario = db_manager.autenticar_usuario(credential, senha)
        
        if sucesso:
            self.frame.destroy()
            self.on_login(usuario)
        else:
            messagebox.showerror(
                "Erro de Autenticação",
                "CPF/CREF ou senha incorretos.\n\n"
                "Se ainda não tem cadastro, clique em 'Criar Nova Conta'."
            )
            self.senha_var.set('')
            self.senha_entry.focus()
    
    def _show_register(self):
        """Mostra tela de cadastro."""
        self.frame.destroy()
        RegisterScreen(self.parent, 
                      on_success=lambda: LoginScreen(self.parent, self.on_login),
                      on_back=lambda: LoginScreen(self.parent, self.on_login))
    
    def _admin_login(self):
        """Login administrativo."""
        # Pedir senha de administrador
        senha = simpledialog.askstring(
            "Acesso Administrativo",
            "Digite a senha de administrador:",
            show='•'
        )
        
        if senha is None:
            return
        
        # Verificar credenciais (usuário fixo: admin, senha: adminDB)
        if db_manager.autenticar_admin("admin", senha):
            # Abrir painel de administração
            AdminPanel(self.parent)
        else:
            messagebox.showerror(
                "Acesso Negado",
                "Senha de administrador incorreta."
            )


class DashboardScreen:
    """Dashboard principal com hero cards."""
    
    def __init__(self, parent, credential, on_create_training, on_edit_training):
        self.parent = parent
        self.credential = credential
        self.on_create_training = on_create_training
        self.on_edit_training = on_edit_training
        
        # Container principal
        self.frame = tk.Frame(parent, bg=theme.colors['bg_secondary'])
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Header
        self._create_header()
        
        # Conteúdo principal
        self._create_content()
    
    def _create_header(self):
        """Cria cabeçalho do dashboard com layout responsivo."""
        # Header com altura ajustada
        header = tk.Frame(self.frame, bg=theme.colors['bg_white'], height=120)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # Linha de separação inferior (sombra sutil)
        separator = tk.Frame(header, bg=theme.colors['border_light'], height=2)
        separator.pack(fill='x', side='bottom')
        
        # Container interno com padding adequado
        header_content = tk.Frame(header, bg=theme.colors['bg_white'])
        header_content.pack(fill='both', expand=True, padx=40, pady=15)
        
        # === LADO ESQUERDO: Logo e Título ===
        left_frame = tk.Frame(header_content, bg=theme.colors['bg_white'])
        left_frame.pack(side='left', fill='y')
        
        # Container para centralização vertical
        left_content = tk.Frame(left_frame, bg=theme.colors['bg_white'])
        left_content.pack(expand=True)
        
        # Logo
        logo_label = tk.Label(
            left_content,
            text="🏃",
            font=(theme.fonts['primary'], 45),
            bg=theme.colors['bg_white'],
            fg=theme.colors['primary']
        )
        logo_label.pack(side='left', padx=(0, 20))
        
        # Títulos
        title_frame = tk.Frame(left_content, bg=theme.colors['bg_white'])
        title_frame.pack(side='left', fill='y')
        
        # Container para centralização vertical dos textos
        title_content = tk.Frame(title_frame, bg=theme.colors['bg_white'])
        title_content.pack(expand=True)
        
        tk.Label(
            title_content,
            text="App Treinos",
            font=(theme.fonts['primary'], theme.font_sizes['heading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w', pady=(0, 2))
        
        tk.Label(
            title_content,
            text="Sistema Profissional de Planejamento Esportivo",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(anchor='w')
        
        # === LADO DIREITO: Info do Usuário e Logout ===
        right_frame = tk.Frame(header_content, bg=theme.colors['bg_white'])
        right_frame.pack(side='right', fill='y')
        
        # Container para centralização vertical
        right_content = tk.Frame(right_frame, bg=theme.colors['bg_white'])
        right_content.pack(expand=True)
        
        # Informações do usuário
        user_info_container = tk.Frame(right_content, bg=theme.colors['bg_white'])
        user_info_container.pack(side='left', padx=(0, 25))
        
        # Ícone do usuário
        tk.Label(
            user_info_container,
            text="👤",
            font=(theme.fonts['primary'], 28),
            bg=theme.colors['bg_white'],
            fg=theme.colors['primary']
        ).pack(side='left', padx=(0, 12))
        
        # Textos do usuário
        user_info = tk.Frame(user_info_container, bg=theme.colors['bg_white'])
        user_info.pack(side='left')
        
        # Exibir nome do usuário ou credencial
        nome_usuario = self.credential.get('nome', 'Usuário') if isinstance(self.credential, dict) else 'Usuário'
        cref_usuario = self.credential.get('cref', '') if isinstance(self.credential, dict) else self.credential
        
        # Truncar nome se muito longo
        nome_exibicao = nome_usuario if len(nome_usuario) <= 30 else nome_usuario[:27] + '...'
        
        tk.Label(
            user_info,
            text=nome_exibicao,
            font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='e', pady=(0, 2))
        
        tk.Label(
            user_info,
            text=f"CREF: {cref_usuario}",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(anchor='e')
        
        # Separador vertical
        separator_v = tk.Frame(
            right_content, 
            bg=theme.colors['border_medium'], 
            width=2
        )
        separator_v.pack(side='left', fill='y', padx=15, pady=10)
        
        # Botão de logout com melhor alinhamento
        logout_container = tk.Frame(right_content, bg=theme.colors['bg_white'])
        logout_container.pack(side='left')
        
        logout_btn = tk.Button(
            logout_container,
            text="🚪  Sair",
            font=(theme.fonts['primary'], theme.font_sizes['small'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['error'],
            activebackground=theme.colors['bg_secondary'],
            activeforeground=theme.colors['error'],
            relief='solid',
            bd=1,
            cursor='hand2',
            command=self._logout
        )
        logout_btn.pack(side='left', padx=8, ipadx=15, ipady=8)
        logout_btn.config(highlightbackground=theme.colors['error'], highlightthickness=0)
        
        # Efeito hover no botão logout
        def on_logout_enter(e):
            logout_btn.config(bg=theme.colors['error'], fg=theme.colors['text_light'])
        
        def on_logout_leave(e):
            logout_btn.config(bg=theme.colors['bg_white'], fg=theme.colors['error'])
        
        logout_btn.bind('<Enter>', on_logout_enter)
        logout_btn.bind('<Leave>', on_logout_leave)
    
    def _create_content(self):
        """Cria conteúdo principal com hero cards."""
        content = tk.Frame(self.frame, bg=theme.colors['bg_secondary'])
        content.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Título da seção com saudação personalizada
        nome_usuario = self.credential.get('nome', 'Profissional') if isinstance(self.credential, dict) else 'Profissional'
        primeiro_nome = nome_usuario.split()[0] if nome_usuario else 'Profissional'
        
        tk.Label(
            content,
            text=f"Olá, {primeiro_nome}! O que você deseja fazer hoje?",
            font=(theme.fonts['primary'], theme.font_sizes['title'], 'bold'),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_primary']
        ).pack(pady=(0, 15))
        
        tk.Label(
            content,
            text="Escolha uma opção abaixo para começar",
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_secondary']
        ).pack(pady=(0, 40))
        
        # Container para os cards
        cards_container = tk.Frame(content, bg=theme.colors['bg_secondary'])
        cards_container.pack(expand=True)
        
        # Hero Card 1: Novo Plano
        self._create_hero_card(
            cards_container,
            title="Novo Plano",
            icon="📋",
            description="Crie um novo plano de treinamento personalizado para seu atleta",
            color=theme.colors['primary'],
            command=lambda: self._on_card_click('create')
        ).pack(side='left', padx=15)
        
        # Hero Card 2: Editar Plano
        self._create_hero_card(
            cards_container,
            title="Editar Plano",
            icon="📝",
            description="Visualize, edite ou exporte planos de treinamento já criados",
            color=theme.colors['analogous_1'],
            command=lambda: self._on_card_click('edit')
        ).pack(side='left', padx=15)
        
        # Hero Card 3: Exportar PDF
        self._create_hero_card(
            cards_container,
            title="Exportar PDF",
            icon="📄",
            description="Exporte planos de treinamento em formato PDF profissional",
            color=theme.colors['triadic_1'],
            command=lambda: self._on_card_click('export_pdf')
        ).pack(side='left', padx=15)
        
        # Hero Card 3: Exportar PDF
        self._create_hero_card(
            cards_container,
            title="Exportar PDF",
            icon="📄",
            description="Exporte planos de treinamento em formato PDF profissional",
            color=theme.colors['triadic_1'],
            command=lambda: self._on_card_click('export_pdf')
        ).pack(side='left', padx=15)
    
    def _create_hero_card(self, parent, title, icon, description, color, command):
        """Cria um hero card moderno e interativo."""
        # Container externo para sombra
        card_wrapper = tk.Frame(
            parent,
            bg=theme.colors['bg_secondary'],
            relief='flat',
            bd=0
        )
        
        # Container do card
        card = tk.Frame(
            card_wrapper,
            bg=theme.colors['bg_white'],
            relief='flat',
            bd=0,
            cursor='hand2'
        )
        card.pack(padx=4, pady=4)  # Espaço para sombra
        
        # Configurar tamanho fixo
        card.config(width=theme.sizes['hero_card_width'], 
                   height=theme.sizes['hero_card_height'])
        card.pack_propagate(False)
        
        # Borda arredondada (simulada)
        card.config(highlightbackground=theme.colors['border_light'],
                   highlightthickness=2)
        
        # Barra colorida no topo
        top_bar = tk.Frame(card, bg=color, height=8)
        top_bar.pack(fill='x', side='top')
        top_bar.pack_propagate(False)
        
        # Container do conteúdo
        content_frame = tk.Frame(card, bg=theme.colors['bg_white'])
        content_frame.pack(fill='both', expand=True)
        
        # Ícone com círculo de fundo
        icon_container = tk.Frame(content_frame, bg=theme.colors['bg_white'])
        icon_container.pack(pady=(25, 10))
        
        # Círculo de fundo para o ícone
        icon_bg = tk.Frame(
            icon_container,
            bg=theme.colors['bg_secondary'],
            width=90,
            height=90
        )
        icon_bg.pack_propagate(False)
        icon_bg.pack()
        
        icon_label = tk.Label(
            icon_bg,
            text=icon,
            font=(theme.fonts['primary'], 48),
            bg=theme.colors['bg_secondary'],
            fg=color
        )
        icon_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título
        title_label = tk.Label(
            content_frame,
            text=title,
            font=(theme.fonts['primary'], theme.font_sizes['card_title'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary'],
            wraplength=theme.sizes['hero_card_width'] - 40  # Deixa margem
        )
        title_label.pack(pady=(5, 5))
        
        # Descrição com wrap
        desc_label = tk.Label(
            content_frame,
            text=description,
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
            justify='center',
            wraplength=theme.sizes['hero_card_width'] - 50  # Texto não corta
        )
        desc_label.pack(pady=(0, 10), padx=10)
        
        # Indicador "clique aqui"
        action_label = tk.Label(
            content_frame,
            text="Clique para começar →",
            font=(theme.fonts['primary'], theme.font_sizes['small'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=color
        )
        action_label.pack(pady=(0, 10))
        
        # Efeito hover aprimorado
        def on_enter(e):
            card.config(bg=theme.colors['bg_tertiary'])
            content_frame.config(bg=theme.colors['bg_tertiary'])
            icon_container.config(bg=theme.colors['bg_tertiary'])
            icon_bg.config(bg=color)
            icon_label.config(bg=color, fg=theme.colors['text_light'])
            title_label.config(bg=theme.colors['bg_tertiary'], 
                             font=(theme.fonts['primary'], theme.font_sizes['card_title'], 'bold underline'))
            desc_label.config(bg=theme.colors['bg_tertiary'])
            action_label.config(bg=theme.colors['bg_tertiary'])
            card.config(highlightbackground=color, highlightthickness=3)
        
        def on_leave(e):
            card.config(bg=theme.colors['bg_white'])
            content_frame.config(bg=theme.colors['bg_white'])
            icon_container.config(bg=theme.colors['bg_white'])
            icon_bg.config(bg=theme.colors['bg_secondary'])
            icon_label.config(bg=theme.colors['bg_secondary'], fg=color)
            title_label.config(bg=theme.colors['bg_white'],
                             font=(theme.fonts['primary'], theme.font_sizes['card_title'], 'bold'))
            desc_label.config(bg=theme.colors['bg_white'])
            action_label.config(bg=theme.colors['bg_white'])
            card.config(highlightbackground=theme.colors['border_light'], highlightthickness=2)
        
        # Bind eventos para todos os widgets
        for widget in [card, content_frame, icon_container, icon_bg, icon_label, 
                      title_label, desc_label, action_label, top_bar]:
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
            widget.bind('<Button-1>', lambda e: command())
        
        return card_wrapper
    
    def _on_card_click(self, action):
        """Trata clique nos cards."""
        if action == 'create':
            self.frame.destroy()
            self.on_create_training()
        elif action == 'edit':
            self.frame.destroy()
            self.on_edit_training()
        elif action == 'export_pdf':
            self._show_pdf_export_dialog()
    
    def _logout(self):
        """Realiza logout e volta para tela de login."""
        resposta = messagebox.askyesno(
            "Confirmar Logout",
            "Tem certeza que deseja sair?\n\nVocê será redirecionado para a tela de login."
        )
        
        if resposta:
            self.frame.destroy()
            LoginScreen(self.parent, lambda credential: DashboardScreen(
                self.parent,
                credential,
                self.on_create_training,
                self.on_edit_training
            ))
    
    def _show_pdf_export_dialog(self):
        """Mostra diálogo para exportação em PDF."""
        # Criar janela de diálogo
        dialog = tk.Toplevel(self.parent)
        dialog.title("Exportar Plano em PDF")
        dialog.geometry("600x400")
        dialog.configure(bg=theme.colors['bg_secondary'])
        dialog.resizable(False, False)
        
        # Centralizar janela
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg=theme.colors['primary'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📄 Exportar Plano em PDF",
            font=(theme.fonts['primary'], theme.font_sizes['heading'], 'bold'),
            bg=theme.colors['primary'],
            fg=theme.colors['text_light']
        ).pack(expand=True)
        
        # Content
        content = tk.Frame(dialog, bg=theme.colors['bg_secondary'])
        content.pack(fill='both', expand=True, padx=40, pady=30)
        
        tk.Label(
            content,
            text="Como deseja exportar o plano de treinamento?",
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_primary']
        ).pack(pady=(0, 30))
        
        # Opção 1: Criar novo plano em PDF
        option1_frame = tk.Frame(content, bg=theme.colors['bg_white'])
        option1_frame.pack(fill='x', pady=(0, 15))
        option1_frame.config(highlightbackground=theme.colors['border_light'], highlightthickness=1)
        
        option1_content = tk.Frame(option1_frame, bg=theme.colors['bg_white'])
        option1_content.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            option1_content,
            text="🆕 Criar Novo Plano em PDF",
            font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w')
        
        tk.Label(
            option1_content,
            text="Crie um novo plano de treinamento e exporte diretamente em formato PDF profissional",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
            wraplength=480,
            justify='left'
        ).pack(anchor='w', pady=(5, 10))
        
        btn_new = tk.Button(
            option1_content,
            text="Criar Novo →",
            font=(theme.fonts['primary'], theme.font_sizes['button']),
            bg=theme.colors['primary'],
            fg=theme.colors['text_light'],
            activebackground=theme.colors['accent_hover'],
            relief='flat',
            cursor='hand2',
            command=lambda: self._start_pdf_creation_wizard(dialog)
        )
        btn_new.pack(anchor='w', ipadx=15, ipady=5)
        
        # Opção 2: Converter Excel para PDF
        option2_frame = tk.Frame(content, bg=theme.colors['bg_white'])
        option2_frame.pack(fill='x', pady=(0, 15))
        option2_frame.config(highlightbackground=theme.colors['border_light'], highlightthickness=1)
        
        option2_content = tk.Frame(option2_frame, bg=theme.colors['bg_white'])
        option2_content.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            option2_content,
            text="🔄 Converter Plano Existente",
            font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w')
        
        tk.Label(
            option2_content,
            text="Selecione um plano Excel já criado e converta para PDF (em desenvolvimento)",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
            wraplength=480,
            justify='left'
        ).pack(anchor='w', pady=(5, 10))
        
        btn_convert = tk.Button(
            option2_content,
            text="Em breve",
            font=(theme.fonts['primary'], theme.font_sizes['button']),
            bg=theme.colors['text_light'],
            fg=theme.colors['text_light'],
            relief='flat',
            state='disabled'
        )
        btn_convert.pack(anchor='w', ipadx=15, ipady=5)
        
        # Footer
        footer = tk.Frame(dialog, bg=theme.colors['bg_secondary'])
        footer.pack(fill='x', padx=40, pady=(0, 20))
        
        tk.Button(
            footer,
            text="Cancelar",
            font=(theme.fonts['primary'], theme.font_sizes['button']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
            activebackground=theme.colors['bg_secondary'],
            relief='solid',
            bd=1,
            cursor='hand2',
            command=dialog.destroy
        ).pack(side='right', ipadx=20, ipady=8)
    
    def _start_pdf_creation_wizard(self, dialog_window):
        """Inicia wizard de criação com exportação em PDF."""
        dialog_window.destroy()
        
        # Destruir dashboard atual
        self.frame.destroy()
        
        # Criar TrainerInfo a partir das credenciais
        trainer = TrainerInfo(
            nome=self.credential['nome'],
            cref=self.credential['cref'],
            email=self.credential.get('email', '')
        )
        
        # Criar wizard - na última etapa o usuário poderá escolher PDF
        TrainingWizard(
            self.parent,
            trainer,
            lambda: DashboardScreen(
                self.parent,
                self.credential,
                self.on_create_training,
                self.on_edit_training
            )
        )


class AppTreinosGUI:
    """Interface Gráfica Principal do App Treinos v2.0."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("App Treinos - Sistema de Planejamento Esportivo")
        
        # Configurar tema
        theme.configure_ttk_style(self.root)
        
        # Configurar janela
        self._setup_window()
        
        # Iniciar com splash screen
        self._show_splash()
    
    def _setup_window(self):
        """Configura janela principal."""
        # Tamanho mínimo reduzido para permitir maior flexibilidade
        min_width = 400
        min_height = 500
        self.root.minsize(min_width, min_height)
        
        # Tamanho inicial
        initial_width = theme.sizes['min_width']
        initial_height = theme.sizes['min_height']
        
        # Centralizar na tela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - initial_width) // 2
        y = (screen_height - initial_height) // 2
        self.root.geometry(f"{initial_width}x{initial_height}+{x}+{y}")
        
        # Permitir redimensionamento
        self.root.resizable(True, True)
        
        # Cor de fundo
        self.root.configure(bg=theme.colors['bg_primary'])
    
    def _show_splash(self):
        """Mostra splash screen."""
        SplashScreen(self.root, self._show_login)
    
    def _show_login(self):
        """Mostra tela de login."""
        LoginScreen(self.root, self._show_dashboard)
    
    def _show_dashboard(self, credential):
        """Mostra dashboard."""
        self.credential = credential
        DashboardScreen(
            self.root,
            credential,
            lambda: self._show_create_training_wizard(credential),
            self._show_edit_training
        )
    
    def _show_create_training_wizard(self, credential):
        """Mostra wizard de criação de treino."""
        # Criar TrainerInfo a partir das credenciais
        trainer = TrainerInfo(
            nome=credential['nome'],
            cref=credential['cref'],
            email=credential.get('email', '')
        )
        
        # Criar wizard
        TrainingWizard(
            self.root,
            trainer,
            lambda: self._show_dashboard(credential)
        )
    
    def _show_edit_training(self):
        """Mostra tela de listagem e edição de treinos."""
        # Criar TrainerInfo a partir das credenciais
        trainer_info = TrainerInfo(
            nome=self.credential['nome'],
            cref=self.credential['cref'],
            email=self.credential.get('email', '')
        )
        
        # Mostrar tela de listagem de treinos
        TrainingListScreen(
            self.root,
            trainer_info,
            lambda: self._show_dashboard(self.credential)
        )
    
    def run(self):
        """Inicia a aplicação."""
        self.root.mainloop()


def main():
    """Função principal."""
    app = AppTreinosGUI()
    app.run()


if __name__ == "__main__":
    main()
