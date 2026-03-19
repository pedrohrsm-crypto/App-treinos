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
        """Cria cabeçalho do dashboard."""
        header = tk.Frame(self.frame, bg=theme.colors['bg_white'], height=100)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # Container interno com padding
        header_content = tk.Frame(header, bg=theme.colors['bg_white'])
        header_content.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Logo e título à esquerda
        left_frame = tk.Frame(header_content, bg=theme.colors['bg_white'])
        left_frame.pack(side='left')
        
        tk.Label(
            left_frame,
            text="🏃",
            font=(theme.fonts['primary'], 40),
            bg=theme.colors['bg_white'],
            fg=theme.colors['primary']
        ).pack(side='left', padx=(0, 15))
        
        title_frame = tk.Frame(left_frame, bg=theme.colors['bg_white'])
        title_frame.pack(side='left')
        
        tk.Label(
            title_frame,
            text="App Treinos",
            font=(theme.fonts['primary'], theme.font_sizes['heading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w')
        
        tk.Label(
            title_frame,
            text="Sistema Profissional de Planejamento",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(anchor='w')
        
        # Info do usuário à direita
        user_frame = tk.Frame(header_content, bg=theme.colors['bg_white'])
        user_frame.pack(side='right')
        
        tk.Label(
            user_frame,
            text="👤",
            font=(theme.fonts['primary'], 24),
            bg=theme.colors['bg_white'],
            fg=theme.colors['primary']
        ).pack(side='left', padx=(0, 10))
        
        user_info = tk.Frame(user_frame, bg=theme.colors['bg_white'])
        user_info.pack(side='left')
        
        # Exibir nome do usuário ou credencial
        nome_usuario = self.credential.get('nome', 'Usuário') if isinstance(self.credential, dict) else 'Usuário'
        cref_usuario = self.credential.get('cref', '') if isinstance(self.credential, dict) else self.credential
        
        tk.Label(
            user_info,
            text=nome_usuario,
            font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='e')
        
        tk.Label(
            user_info,
            text=f"CREF: {cref_usuario}",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(anchor='e')
    
    def _create_content(self):
        """Cria conteúdo principal com hero cards."""
        content = tk.Frame(self.frame, bg=theme.colors['bg_secondary'])
        content.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Título da seção
        tk.Label(
            content,
            text="O que você deseja fazer?",
            font=(theme.fonts['primary'], theme.font_sizes['title'], 'bold'),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_primary']
        ).pack(pady=(0, 30))
        
        # Container para os cards
        cards_container = tk.Frame(content, bg=theme.colors['bg_secondary'])
        cards_container.pack(expand=True)
        
        # Hero Card 1: Criar Treino
        self._create_hero_card(
            cards_container,
            title="Criar Treino",
            icon="➕",
            description="Crie um novo plano de\ntreinamento personalizado",
            color=theme.colors['primary'],
            command=lambda: self._on_card_click('create')
        ).pack(side='left', padx=20)
        
        # Hero Card 2: Editar Treino
        self._create_hero_card(
            cards_container,
            title="Editar Treino",
            icon="✏️",
            description="Edite ou visualize planos\nde treinamento existentes",
            color=theme.colors['analogous_2'],
            command=lambda: self._on_card_click('edit')
        ).pack(side='left', padx=20)
    
    def _create_hero_card(self, parent, title, icon, description, color, command):
        """Cria um hero card."""
        # Container do card
        card = tk.Frame(
            parent,
            bg=theme.colors['bg_white'],
            relief='flat',
            bd=0,
            cursor='hand2'
        )
        
        # Configurar tamanho fixo
        card.config(width=theme.sizes['hero_card_width'], 
                   height=theme.sizes['hero_card_height'])
        card.pack_propagate(False)
        
        # Adicionar sombra
        card.config(highlightbackground=theme.colors['shadow_strong'],
                   highlightthickness=2)
        
        # Ícone
        icon_label = tk.Label(
            card,
            text=icon,
            font=(theme.fonts['primary'], 64),
            bg=theme.colors['bg_white'],
            fg=color
        )
        icon_label.pack(pady=(30, 10))
        
        # Título
        title_label = tk.Label(
            card,
            text=title,
            font=(theme.fonts['primary'], theme.font_sizes['card_title'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        )
        title_label.pack()
        
        # Descrição
        desc_label = tk.Label(
            card,
            text=description,
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
            justify='center'
        )
        desc_label.pack(pady=(5, 20))
        
        # Efeito hover
        def on_enter(e):
            card.config(bg=theme.colors['bg_tertiary'])
            icon_label.config(bg=theme.colors['bg_tertiary'])
            title_label.config(bg=theme.colors['bg_tertiary'])
            desc_label.config(bg=theme.colors['bg_tertiary'])
        
        def on_leave(e):
            card.config(bg=theme.colors['bg_white'])
            icon_label.config(bg=theme.colors['bg_white'])
            title_label.config(bg=theme.colors['bg_white'])
            desc_label.config(bg=theme.colors['bg_white'])
        
        # Bind eventos
        for widget in [card, icon_label, title_label, desc_label]:
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
            widget.bind('<Button-1>', lambda e: command())
        
        return card
    
    def _on_card_click(self, action):
        """Trata clique nos cards."""
        self.frame.destroy()
        if action == 'create':
            self.on_create_training()
        else:
            self.on_edit_training()


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
        DashboardScreen(
            self.root,
            credential,
            self._show_create_training_wizard,
            self._show_edit_training
        )
    
    def _show_create_training_wizard(self):
        """Mostra wizard de criação de treino."""
        # TODO: Implementar wizard completo
        # Por enquanto, mostrar mensagem
        messagebox.showinfo(
            "Criar Treino",
            "O wizard completo de criação de treino será carregado aqui.\n\n"
            "Incluirá as etapas:\n"
            "1. Dados do Atleta\n"
            "2. Modalidade e Disponibilidade\n"
            "3. Objetivos e Metas\n"
            "4. Geração do Plano"
        )
    
    def _show_edit_training(self):
        """Mostra tela de edição de treino."""
        # TODO: Implementar lista de treinos e edição
        messagebox.showinfo(
            "Editar Treino",
            "A funcionalidade de edição será implementada em breve.\n\n"
            "Permitirá:\n"
            "• Listar treinos criados\n"
            "• Editar treinos existentes\n"
            "• Visualizar histórico\n"
            "• Exportar relatórios"
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
