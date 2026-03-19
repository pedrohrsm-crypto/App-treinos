"""
Tela de Cadastro - App Treinos
===============================

Interface para cadastro de novos usuários.
"""

import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

# Adicionar diretórios ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from gui.theme import theme
from core.database import db_manager


class RegisterScreen:
    """Tela de cadastro de novos usuários."""
    
    def __init__(self, parent, on_success, on_back):
        self.parent = parent
        self.on_success = on_success
        self.on_back = on_back
        
        # Container principal
        self.frame = tk.Frame(parent, bg=theme.colors['bg_secondary'])
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Container centralizado (responsivo)
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
        
        # Logo pequeno
        logo = tk.Label(
            content_wrapper,
            text="📝",
            font=(theme.fonts['primary'], 80),
            bg=theme.colors['bg_white'],
            fg=theme.colors['primary']
        )
        logo.pack(pady=(30, 10))
        
        # Título
        title = tk.Label(
            content_wrapper,
            text="Criar Nova Conta",
            font=(theme.fonts['primary'], theme.font_sizes['title'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        )
        title.pack(pady=(0, 5))
        
        # Subtítulo
        subtitle = tk.Label(
            content_wrapper,
            text="Preencha seus dados para cadastro",
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        )
        subtitle.pack(pady=(0, 20))
        
        # Formulário
        form_frame = tk.Frame(content_wrapper, bg=theme.colors['bg_white'])
        form_frame.pack(pady=10, padx=40, fill='x')
        
        # Campo: Nome Completo
        tk.Label(
            form_frame,
            text="Nome Completo:",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(anchor='w', pady=(0, 5))
        
        self.nome_var = tk.StringVar()
        self.nome_entry = tk.Entry(
            form_frame,
            textvariable=self.nome_var,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightbackground=theme.colors['border_light'],
            highlightcolor=theme.colors['primary']
        )
        self.nome_entry.pack(fill='x', ipady=10)
        self.nome_entry.focus()
        
        # Campo: CPF
        tk.Label(
            form_frame,
            text="CPF (somente números):",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(anchor='w', pady=(15, 5))
        
        self.cpf_var = tk.StringVar()
        self.cpf_entry = tk.Entry(
            form_frame,
            textvariable=self.cpf_var,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightbackground=theme.colors['border_light'],
            highlightcolor=theme.colors['primary']
        )
        self.cpf_entry.pack(fill='x', ipady=10)
        
        # Campo: CREF
        tk.Label(
            form_frame,
            text="CREF (ex: 123456-G/SP):",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(anchor='w', pady=(15, 5))
        
        self.cref_var = tk.StringVar()
        self.cref_entry = tk.Entry(
            form_frame,
            textvariable=self.cref_var,
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightbackground=theme.colors['border_light'],
            highlightcolor=theme.colors['primary']
        )
        self.cref_entry.pack(fill='x', ipady=10)
        
        # Campo: Senha
        tk.Label(
            form_frame,
            text="Senha (6 a 12 caracteres, sem espaços):",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(anchor='w', pady=(15, 5))
        
        self.senha_var = tk.StringVar()
        self.senha_entry = tk.Entry(
            form_frame,
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
        
        # Bind Enter para próximo campo
        self.nome_entry.bind('<Return>', lambda e: self.cpf_entry.focus())
        self.cpf_entry.bind('<Return>', lambda e: self.cref_entry.focus())
        self.cref_entry.bind('<Return>', lambda e: self.senha_entry.focus())
        self.senha_entry.bind('<Return>', lambda e: self._registrar())
        
        # Botão Registrar
        registrar_btn = tk.Button(
            content_wrapper,
            text="✅ Registrar",
            font=(theme.fonts['primary'], theme.font_sizes['button'], 'bold'),
            bg=theme.colors['primary'],
            fg=theme.colors['text_light'],
            activebackground=theme.colors['accent_hover'],
            activeforeground=theme.colors['text_light'],
            relief='flat',
            cursor='hand2',
            command=self._registrar
        )
        registrar_btn.pack(pady=(20, 10), padx=40, fill='x', ipady=12)
        
        # Botão Voltar
        voltar_btn = tk.Button(
            content_wrapper,
            text="← Voltar",
            font=(theme.fonts['primary'], theme.font_sizes['button'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['primary'],
            activebackground=theme.colors['bg_secondary'],
            activeforeground=theme.colors['primary'],
            relief='solid',
            bd=2,
            cursor='hand2',
            highlightthickness=0,
            command=self._voltar
        )
        voltar_btn.config(highlightbackground=theme.colors['primary'])
        voltar_btn.pack(pady=(10, 30), padx=40, fill='x', ipady=12)
    
    def _registrar(self):
        """Processa o registro do usuário."""
        # Obter valores
        nome = self.nome_var.get().strip()
        cpf = self.cpf_var.get().strip().replace('.', '').replace('-', '')
        cref = self.cref_var.get().strip()
        senha = self.senha_var.get()
        
        # Validações
        if not nome:
            messagebox.showerror("Erro", "Por favor, informe seu nome completo.")
            self.nome_entry.focus()
            return
        
        if not cpf or len(cpf) != 11:
            messagebox.showerror("Erro", "CPF deve conter exatamente 11 dígitos.")
            self.cpf_entry.focus()
            return
        
        if not cref:
            messagebox.showerror("Erro", "Por favor, informe seu CREF.")
            self.cref_entry.focus()
            return
        
        if not senha:
            messagebox.showerror("Erro", "Por favor, defina uma senha.")
            self.senha_entry.focus()
            return
        
        # Validação de senha: 6-12 caracteres, sem espaços
        if ' ' in senha:
            messagebox.showerror("Erro", "A senha não pode conter espaços.")
            self.senha_entry.focus()
            return
        
        if len(senha) < 6 or len(senha) > 12:
            messagebox.showerror("Erro", 
                "A senha deve ter entre 6 e 12 caracteres.\n" +
                "Aceita letras maiúsculas, minúsculas, números e caracteres especiais.")
            self.senha_entry.focus()
            return
        
        # Tentar cadastrar no banco de dados
        sucesso, mensagem = db_manager.cadastrar_usuario(
            cpf=cpf,
            cref=cref,
            nome=nome,
            senha=senha,
            email=""
        )
        
        if sucesso:
            # Mostrar mensagem de sucesso
            messagebox.showinfo("Sucesso!", "Usuário cadastrado com sucesso!")
            
            # Destruir tela de cadastro
            self.frame.destroy()
            
            # Retornar ao login
            if self.on_success:
                self.on_success()
        else:
            # Mostrar erro
            messagebox.showerror("Erro no Cadastro", mensagem)
    
    def _voltar(self):
        """Volta para a tela de login sem salvar."""
        self.frame.destroy()
        if self.on_back:
            self.on_back()

