"""
Interface de Gerenciamento de Treinos
=====================================

Tela para visualizar, editar e exportar treinos criados.
Apenas o profissional criador pode acessar seus próprios treinos.
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess
import platform
from pathlib import Path

from gui.theme import theme
from training_manager import training_manager


class TrainingListScreen:
    """Tela de listagem e gerenciamento de treinos."""
    
    def __init__(self, parent, trainer_info, on_back):
        """
        Inicializa a tela de listagem.
        
        Args:
            parent: Widget pai
            trainer_info: Informações do treinador
            on_back: Callback para voltar ao dashboard
        """
        self.parent = parent
        self.trainer_info = trainer_info
        self.on_back = on_back
        
        # Container principal
        self.frame = tk.Frame(parent, bg=theme.colors['bg_secondary'])
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Criar estrutura
        self._create_header()
        self._create_content()
    
    def _create_header(self):
        """Cria cabeçalho da tela."""
        header = tk.Frame(self.frame, bg=theme.colors['bg_white'], height=100)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # Linha separadora
        tk.Frame(header, bg=theme.colors['border_light'], height=2).pack(fill='x', side='bottom')
        
        header_content = tk.Frame(header, bg=theme.colors['bg_white'])
        header_content.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Botão voltar
        btn_back = tk.Button(
            header_content,
            text="← Voltar",
            font=(theme.fonts['primary'], theme.font_sizes['button']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary'],
            activebackground=theme.colors['bg_secondary'],
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self._go_back
        )
        btn_back.pack(side='left', padx=(0, 20))
        
        # Título
        title_frame = tk.Frame(header_content, bg=theme.colors['bg_white'])
        title_frame.pack(side='left', fill='y')
        
        title_content = tk.Frame(title_frame, bg=theme.colors['bg_white'])
        title_content.pack(expand=True)
        
        tk.Label(
            title_content,
            text="📝 Meus Treinos",
            font=(theme.fonts['primary'], theme.font_sizes['heading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(anchor='w')
        
        # Estatísticas
        stats = training_manager.get_statistics(self.trainer_info)
        tk.Label(
            title_content,
            text=f"{stats['total_plans']} planos criados • {stats['unique_athletes']} atletas",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(anchor='w')
    
    def _create_content(self):
        """Cria conteúdo principal com lista de treinos."""
        content = tk.Frame(self.frame, bg=theme.colors['bg_secondary'])
        content.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Obter treinos do profissional
        plans = training_manager.get_trainer_plans(self.trainer_info)
        
        if not plans:
            # Mensagem de lista vazia
            empty_frame = tk.Frame(content, bg=theme.colors['bg_white'])
            empty_frame.pack(expand=True, fill='both')
            empty_frame.config(highlightbackground=theme.colors['border_light'], highlightthickness=1)
            
            empty_content = tk.Frame(empty_frame, bg=theme.colors['bg_white'])
            empty_content.pack(expand=True, padx=40, pady=60)
            
            tk.Label(
                empty_content,
                text="📭",
                font=(theme.fonts['primary'], 72),
                bg=theme.colors['bg_white']
            ).pack(pady=(0, 20))
            
            tk.Label(
                empty_content,
                text="Nenhum treino criado ainda",
                font=(theme.fonts['primary'], theme.font_sizes['heading'], 'bold'),
                bg=theme.colors['bg_white'],
                fg=theme.colors['text_primary']
            ).pack(pady=(0, 10))
            
            tk.Label(
                empty_content,
                text="Clique em 'Novo Plano' no dashboard para criar seu primeiro treino",
                font=(theme.fonts['primary'], theme.font_sizes['body']),
                bg=theme.colors['bg_white'],
                fg=theme.colors['text_secondary']
            ).pack()
            
        else:
            # Container com scroll para lista de treinos
            canvas = tk.Canvas(content, bg=theme.colors['bg_secondary'], highlightthickness=0)
            scrollbar = tk.Scrollbar(content, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=theme.colors['bg_secondary'])
            
            scrollable_frame.bind(
                '<Configure>',
                lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Criar card para cada treino
            for plan in plans:
                self._create_plan_card(scrollable_frame, plan).pack(fill='x', pady=(0, 15))
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
    
    def _create_plan_card(self, parent, plan):
        """Cria card de um treino."""
        card = tk.Frame(parent, bg=theme.colors['bg_white'])
        card.config(highlightbackground=theme.colors['border_light'], highlightthickness=1)
        
        # Barra colorida lateral
        color_bar = tk.Frame(card, bg=theme.colors['primary'], width=6)
        color_bar.pack(side='left', fill='y')
        
        # Conteúdo
        content = tk.Frame(card, bg=theme.colors['bg_white'])
        content.pack(side='left', fill='both', expand=True, padx=25, pady=20)
        
        # Linha 1: Nome do atleta e esporte
        top_row = tk.Frame(content, bg=theme.colors['bg_white'])
        top_row.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            top_row,
            text=f"👤 {plan.athlete_name}",
            font=(theme.fonts['primary'], theme.font_sizes['heading'], 'bold'),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_primary']
        ).pack(side='left')
        
        tk.Label(
            top_row,
            text=f"{plan.sport} • {plan.distance}",
            font=(theme.fonts['primary'], theme.font_sizes['body']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(side='left', padx=(15, 0))
        
        # Linha 2: Detalhes
        details_row = tk.Frame(content, bg=theme.colors['bg_white'])
        details_row.pack(fill='x', pady=(0, 15))
        
        # Idade e gênero
        athlete_data = plan.athlete_data
        details_text = f"{athlete_data.get('idade', 'N/A')} anos • {athlete_data.get('genero', 'N/A')} • "
        details_text += f"{plan.weeks} semanas • IMC: {athlete_data.get('imc', 'N/A'):.1f}"
        
        tk.Label(
            details_row,
            text=details_text,
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(side='left')
        
        # Data de criação
        from datetime import datetime
        created_date = datetime.fromisoformat(plan.created_at).strftime("%d/%m/%Y às %H:%M")
        tk.Label(
            details_row,
            text=f"📅 Criado em {created_date}",
            font=(theme.fonts['primary'], theme.font_sizes['small']),
            bg=theme.colors['bg_white'],
            fg=theme.colors['text_secondary']
        ).pack(side='right')
        
        # Linha 3: Botões de ação
        actions_row = tk.Frame(content, bg=theme.colors['bg_white'])
        actions_row.pack(fill='x')
        
        # Botão Abrir Excel (se existir)
        if plan.excel_path and os.path.exists(plan.excel_path):
            btn_excel = tk.Button(
                actions_row,
                text="📊 Abrir Excel",
                font=(theme.fonts['primary'], theme.font_sizes['button']),
                bg=theme.colors['success'],
                fg=theme.colors['text_light'],
                activebackground=theme.colors['accent_hover'],
                relief='flat',
                cursor='hand2',
                command=lambda p=plan.excel_path: self._open_file(p)
            )
            btn_excel.pack(side='left', ipadx=12, ipady=6, padx=(0, 10))
        
        # Botão Abrir PDF (se existir)
        if plan.pdf_path and os.path.exists(plan.pdf_path):
            btn_pdf = tk.Button(
                actions_row,
                text="📄 Abrir PDF",
                font=(theme.fonts['primary'], theme.font_sizes['button']),
                bg=theme.colors['triadic_1'],
                fg=theme.colors['text_light'],
                activebackground=theme.colors['accent_hover'],
                relief='flat',
                cursor='hand2',
                command=lambda p=plan.pdf_path: self._open_file(p)
            )
            btn_pdf.pack(side='left', ipadx=12, ipady=6, padx=(0, 10))
        
        # Botão Exportar Novamente
        btn_export = tk.Button(
            actions_row,
            text="💾 Exportar",
            font=(theme.fonts['primary'], theme.font_sizes['button']),
            bg=theme.colors['primary'],
            fg=theme.colors['text_light'],
            activebackground=theme.colors['accent_hover'],
            relief='flat',
            cursor='hand2',
            command=lambda p=plan: self._show_export_options(p)
        )
        btn_export.pack(side='left', ipadx=12, ipady=6, padx=(0, 10))
        
        # Botão Deletar
        btn_delete = tk.Button(
            actions_row,
            text="🗑️ Deletar",
            font=(theme.fonts['primary'], theme.font_sizes['button']),
            bg=theme.colors['bg_secondary'],
            fg=theme.colors['text_secondary'],
            activebackground=theme.colors['error'],
            activeforeground=theme.colors['text_light'],
            relief='flat',
            cursor='hand2',
            command=lambda p=plan: self._delete_plan(p)
        )
        btn_delete.pack(side='right', ipadx=12, ipady=6)
        
        return card
    
    def _open_file(self, filepath):
        """Abre arquivo no aplicativo padrão do sistema."""
        try:
            system = platform.system()
            if system == 'Windows':
                os.startfile(filepath)
            elif system == 'Darwin':  # macOS
                subprocess.run(['open', filepath])
            else:  # Linux
                subprocess.run(['xdg-open', filepath])
        except Exception as e:
            messagebox.showerror(
                "Erro ao Abrir Arquivo",
                f"Não foi possível abrir o arquivo:\n\n{str(e)}"
            )
    
    def _show_export_options(self, plan):
        """Mostra opções de exportação."""
        messagebox.showinfo(
            "Exportar Plano",
            f"Funcionalidade de re-exportação em desenvolvimento.\n\n"
            f"Arquivos já exportados:\n"
            f"• Excel: {os.path.basename(plan.excel_path) if plan.excel_path else 'N/A'}\n"
            f"• PDF: {os.path.basename(plan.pdf_path) if plan.pdf_path else 'N/A'}"
        )
    
    def _delete_plan(self, plan):
        """Deleta um plano após confirmação."""
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja deletar o plano de treinamento de:\n\n"
            f"👤 {plan.athlete_name}\n"
            f"🏃 {plan.sport} - {plan.distance}\n\n"
            f"Esta ação não pode ser desfeita!"
        )
        
        if resposta:
            success, message = training_manager.delete_plan(self.trainer_info, plan.id)
            
            if success:
                messagebox.showinfo("Plano Deletado", message)
                # Recarregar tela
                self.frame.destroy()
                TrainingListScreen(self.parent, self.trainer_info, self.on_back)
            else:
                messagebox.showerror("Erro ao Deletar", message)
    
    def _go_back(self):
        """Volta para o dashboard."""
        self.frame.destroy()
        self.on_back()
