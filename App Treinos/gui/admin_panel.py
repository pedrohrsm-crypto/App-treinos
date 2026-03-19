"""
Painel de Administração - App Treinos
======================================

Interface para gerenciamento de usuários cadastrados.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

# Adicionar diretórios ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from gui.theme import theme
from core.database import db_manager


class AdminPanel:
    """Painel de administração de usuários."""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Painel de Administração - App Treinos")
        self.window.geometry("900x600")
        self.window.transient(parent)
        
        # Criar interface
        self._create_ui()
        
        # Carregar usuários
        self.carregar_usuarios()
    
    def _create_ui(self):
        """Cria interface do painel."""
        # Header
        header = tk.Frame(self.window, bg=theme.colors['primary'], height=60)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text="🔐 Painel de Administração",
            font=(theme.fonts['primary'], 20, 'bold'),
            bg=theme.colors['primary'],
            fg=theme.colors['text_light']
        ).pack(pady=15)
        
        # Toolbar
        toolbar = tk.Frame(self.window, bg=theme.colors['bg_white'], height=50)
        toolbar.pack(fill='x', padx=20, pady=10)
        
        tk.Button(
            toolbar,
            text="🔄 Atualizar",
            font=(theme.fonts['primary'], 11),
            bg=theme.colors['primary'],
            fg=theme.colors['text_light'],
            relief='flat',
            cursor='hand2',
            command=self.carregar_usuarios
        ).pack(side='left', padx=5)
        
        tk.Button(
            toolbar,
            text="➕ Novo Usuário",
            font=(theme.fonts['primary'], 11),
            bg=theme.colors['accent'],
            fg=theme.colors['text_light'],
            relief='flat',
            cursor='hand2',
            command=self.adicionar_usuario
        ).pack(side='left', padx=5)
        
        # Tabela de usuários
        table_frame = tk.Frame(self.window, bg=theme.colors['bg_white'])
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(table_frame, orient='vertical')
        h_scroll = ttk.Scrollbar(table_frame, orient='horizontal')
        
        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Nome', 'CPF', 'CREF', 'Email', 'Cadastro', 'Último Acesso', 'Status'),
            show='headings',
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set
        )
        
        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)
        
        # Configurar colunas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('CPF', text='CPF')
        self.tree.heading('CREF', text='CREF')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Cadastro', text='Data Cadastro')
        self.tree.heading('Último Acesso', text='Último Acesso')
        self.tree.heading('Status', text='Status')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Nome', width=150)
        self.tree.column('CPF', width=100)
        self.tree.column('CREF', width=100)
        self.tree.column('Email', width=150)
        self.tree.column('Cadastro', width=120)
        self.tree.column('Último Acesso', width=120)
        self.tree.column('Status', width=80, anchor='center')
        
        # Layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Botões de ação
        action_frame = tk.Frame(self.window, bg=theme.colors['bg_white'])
        action_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(
            action_frame,
            text="✏️ Editar",
            font=(theme.fonts['primary'], 11),
            bg=theme.colors['accent_hover'],
            fg=theme.colors['text_light'],
            relief='flat',
            cursor='hand2',
            command=self.editar_usuario
        ).pack(side='left', padx=5)
        
        tk.Button(
            action_frame,
            text="🗑️ Desativar",
            font=(theme.fonts['primary'], 11),
            bg='#e74c3c',
            fg=theme.colors['text_light'],
            relief='flat',
            cursor='hand2',
            command=self.desativar_usuario
        ).pack(side='left', padx=5)
        
        tk.Button(
            action_frame,
            text="❌ Fechar",
            font=(theme.fonts['primary'], 11),
            bg=theme.colors['text_secondary'],
            fg=theme.colors['text_light'],
            relief='flat',
            cursor='hand2',
            command=self.window.destroy
        ).pack(side='right', padx=5)
    
    def carregar_usuarios(self):
        """Carrega lista de usuários do banco."""
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar usuários
        usuarios = db_manager.listar_usuarios()
        
        # Inserir na tabela
        for user in usuarios:
            status = "✅ Ativo" if user['ativo'] else "❌ Inativo"
            cadastro = user['data_cadastro'][:10] if user['data_cadastro'] else '-'
            ultimo_acesso = user['ultimo_acesso'][:10] if user['ultimo_acesso'] else 'Nunca'
            
            self.tree.insert('', 'end', values=(
                user['id'],
                user['nome'],
                user['cpf'] or '-',
                user['cref'] or '-',
                user['email'] or '-',
                cadastro,
                ultimo_acesso,
                status
            ))
    
    def adicionar_usuario(self):
        """Abre janela para adicionar novo usuário."""
        EditUserDialog(self.window, None, self.carregar_usuarios)
    
    def editar_usuario(self):
        """Edita usuário selecionado."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar.")
            return
        
        item = self.tree.item(selection[0])
        user_id = item['values'][0]
        EditUserDialog(self.window, user_id, self.carregar_usuarios)
    
    def desativar_usuario(self):
        """Desativa usuário selecionado."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um usuário para desativar.")
            return
        
        item = self.tree.item(selection[0])
        user_id = item['values'][0]
        nome = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Desativar usuário '{nome}'?"):
            sucesso, msg = db_manager.deletar_usuario(user_id)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.carregar_usuarios()
            else:
                messagebox.showerror("Erro", msg)


class EditUserDialog:
    """Diálogo para editar/adicionar usuário."""
    
    def __init__(self, parent, user_id=None, callback=None):
        self.user_id = user_id
        self.callback = callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Novo Usuário" if user_id is None else "Editar Usuário")
        self.window.geometry("400x450")
        self.window.transient(parent)
        self.window.grab_set()
        
        self._create_ui()
        
        if user_id:
            self._load_user_data()
    
    def _create_ui(self):
        """Cria interface do diálogo."""
        # Container principal
        main_frame = tk.Frame(self.window, bg=theme.colors['bg_white'], padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Campos
        fields = [
            ('Nome Completo:', 'nome'),
            ('CPF (11 dígitos):', 'cpf'),
            ('CREF:', 'cref'),
            ('Email:', 'email'),
            ('Senha:', 'senha')
        ]
        
        self.entries = {}
        
        for label_text, field_name in fields:
            tk.Label(
                main_frame,
                text=label_text,
                font=(theme.fonts['primary'], 11),
                bg=theme.colors['bg_white'],
                fg=theme.colors['text_primary']
            ).pack(anchor='w', pady=(10, 2))
            
            if field_name == 'senha':
                entry = tk.Entry(
                    main_frame,
                    font=(theme.fonts['primary'], 12),
                    show='•',
                    relief='solid',
                    bd=1
                )
            else:
                entry = tk.Entry(
                    main_frame,
                    font=(theme.fonts['primary'], 12),
                    relief='solid',
                    bd=1
                )
            
            entry.pack(fill='x', ipady=8)
            self.entries[field_name] = entry
        
        # Botões
        btn_frame = tk.Frame(main_frame, bg=theme.colors['bg_white'])
        btn_frame.pack(pady=30)
        
        tk.Button(
            btn_frame,
            text="💾 Salvar",
            font=(theme.fonts['primary'], 12, 'bold'),
            bg=theme.colors['primary'],
            fg=theme.colors['text_light'],
            relief='flat',
            cursor='hand2',
            command=self._salvar
        ).pack(side='left', padx=5, ipadx=20, ipady=10)
        
        tk.Button(
            btn_frame,
            text="❌ Cancelar",
            font=(theme.fonts['primary'], 12),
            bg=theme.colors['text_secondary'],
            fg=theme.colors['text_light'],
            relief='flat',
            cursor='hand2',
            command=self.window.destroy
        ).pack(side='left', padx=5, ipadx=20, ipady=10)
    
    def _load_user_data(self):
        """Carrega dados do usuário para edição."""
        # TODO: Implementar carregamento de dados
        pass
    
    def _salvar(self):
        """Salva usuário."""
        nome = self.entries['nome'].get().strip()
        cpf = self.entries['cpf'].get().strip()
        cref = self.entries['cref'].get().strip()
        email = self.entries['email'].get().strip()
        senha = self.entries['senha'].get()
        
        # Validações
        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório")
            return
        
        if not cpf and not cref:
            messagebox.showerror("Erro", "Informe CPF ou CREF")
            return
        
        if not senha and self.user_id is None:
            messagebox.showerror("Erro", "Senha é obrigatória para novo usuário")
            return
        
        # Validação de senha: 6-12 caracteres, sem espaços
        if senha:
            if ' ' in senha:
                messagebox.showerror("Erro", "A senha não pode conter espaços.")
                return
            
            if len(senha) < 6 or len(senha) > 12:
                messagebox.showerror("Erro", 
                    "A senha deve ter entre 6 e 12 caracteres.\n" +
                    "Aceita letras maiúsculas, minúsculas, números e caracteres especiais.")
                return
        
        # Cadastrar
        sucesso, msg = db_manager.cadastrar_usuario(cpf, cref, nome, senha, email)
        
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            if self.callback:
                self.callback()
            self.window.destroy()
        else:
            messagebox.showerror("Erro", msg)
